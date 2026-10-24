import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Executes Point 2 experiments using the existing search implementations.
 */
public final class ExperimentRunner {

    private static final int[] DEFAULT_SIZES = {1000, 10000, 100000, 1000000};
    private static final String[] ALGORITHM_NAMES = {
        "linear", "binary", "ternary", "jump", "interpolation", "exponential"
    };
    private static final String[] FIELDS = {
        "experiment_id", "algorithm", "language", "input_variant", "n",
        "experiment_type", "position", "key_set_id", "key_presence",
        "repetition_1_ns", "repetition_2_ns", "repetition_3_ns",
        "repetition_4_ns", "repetition_5_ns", "mean_ns", "stddev_ns",
        "status", "is_estimated", "estimate_method", "error_message",
        "repetitions", "searches_per_repetition", "warmup_iterations",
        "observations"
    };
    private static volatile int blackHole;

    private interface Search {
        int find(int[] values, int key);
    }

    private static final Search[] SEARCHES = {
        LinearSearch::search, BinarySearch::search, TernarySearch::search,
        JumpSearch::search, InterpolationSearch::search, ExponentialSearch::search
    };

    private ExperimentRunner() {
    }

    public static void main(String[] args) throws IOException {
        Config config = Config.parse(args);
        List<String[]> rows = new ArrayList<>();
        long deadline = System.nanoTime() + (long) (config.timeoutSeconds * 1_000_000_000L);

        for (int size : config.sizes) {
            int[] values = loadArray(config.root, size);
            List<Key> keys = loadKeys(config.root, size);
            boolean[] expected = new boolean[keys.size()];
            for (int i = 0; i < keys.size(); i++) {
                expected[i] = "PRESENTE".equals(keys.get(i).presence);
            }

            for (int algorithm = 0; algorithm < SEARCHES.length; algorithm++) {
                for (int i = 0; i < keys.size(); i++) {
                    validate(SEARCHES[algorithm], values, keys.get(i).key, expected[i]);
                }
                warmUp(SEARCHES[algorithm], values, keys);
                List<Long> times = timedKeys(SEARCHES[algorithm], values, keys, config.repetitions, deadline);
                rows.add(row(ALGORITHM_NAMES[algorithm], size, "all_keys", "", "keys_" + size,
                    "mixed", times, keys.size(), config.repetitions, 2, "timeout".equals(status(times, config.repetitions))));
            }
        }

        if (config.positions && contains(config.sizes, 1000000)) {
            int[] values = loadArray(config.root, 1000000);
            for (int algorithm = 0; algorithm < SEARCHES.length; algorithm++) {
                for (String position : new String[]{"start", "middle", "end"}) {
                    int index = position.equals("start") ? 0
                        : position.equals("middle") ? values.length / 2 : values.length - 1;
                    int key = values[index];
                    validate(SEARCHES[algorithm], values, key, true);
                    warmUpSingle(SEARCHES[algorithm], values, key);
                    List<Long> times = timedPosition(SEARCHES[algorithm], values, key,
                        config.positionSearches, config.repetitions, deadline);
                    rows.add(row(ALGORITHM_NAMES[algorithm], 1000000, "position", position, "",
                        "present", times, config.positionSearches, config.repetitions, 2,
                        "timeout".equals(status(times, config.repetitions))));
                }
            }
        }

        writeCsv(config.output, rows);
        System.out.println("wrote " + rows.size() + " rows to " + config.output);
    }

    private static int[] loadArray(Path root, int size) throws IOException {
        Path path = root.resolve("data").resolve("asc_" + size + ".txt");
        List<String> lines = Files.readAllLines(path);
        if (lines.size() != size) {
            throw new IOException("invalid array size: " + path);
        }
        int[] values = new int[size];
        for (int i = 0; i < size; i++) {
            values[i] = Integer.parseInt(lines.get(i));
            if (i > 0 && values[i - 1] > values[i]) {
                throw new IOException("array is not sorted: " + path);
            }
        }
        return values;
    }

    private static List<Key> loadKeys(Path root, int size) throws IOException {
        Path path = root.resolve("data").resolve("search_keys").resolve("keys_" + size + ".txt");
        List<String> lines = Files.readAllLines(path);
        if (lines.size() != 1001 || !"key_id\tkey\tpresence\tn".equals(lines.get(0))) {
            throw new IOException("invalid key file: " + path);
        }
        List<Key> keys = new ArrayList<>();
        for (int i = 1; i < lines.size(); i++) {
            String[] fields = lines.get(i).split("\t", -1);
            if (fields.length != 4 || !Integer.toString(size).equals(fields[3])) {
                throw new IOException("invalid key row: " + path);
            }
            keys.add(new Key(Integer.parseInt(fields[1]), fields[2]));
        }
        return keys;
    }

    private static void validate(Search search, int[] values, int key, boolean expected) {
        int result = search.find(values, key);
        boolean valid = result >= 0 && result < values.length && values[result] == key;
        if ((result == -1) != !expected || result != -1 && !valid) {
            throw new IllegalStateException("invalid search result for key " + key);
        }
    }

    private static void warmUp(Search search, int[] values, List<Key> keys) {
        for (int iteration = 0; iteration < 2; iteration++) {
            for (Key key : keys) {
                blackHole = search.find(values, key.key);
            }
        }
    }

    private static void warmUpSingle(Search search, int[] values, int key) {
        for (int iteration = 0; iteration < 100; iteration++) {
            blackHole = search.find(values, key);
        }
    }

    private static List<Long> timedKeys(Search search, int[] values, List<Key> keys,
                                         int repetitions, long deadline) {
        List<Long> times = new ArrayList<>();
        for (int repetition = 0; repetition < repetitions; repetition++) {
            if (System.nanoTime() >= deadline) {
                break;
            }
            int checksum = 0;
            long start = System.nanoTime();
            for (Key key : keys) {
                checksum += search.find(values, key.key);
            }
            long elapsed = System.nanoTime() - start;
            blackHole = checksum;
            times.add(elapsed);
        }
        return times;
    }

    private static List<Long> timedPosition(Search search, int[] values, int key,
                                             int searches, int repetitions, long deadline) {
        List<Long> times = new ArrayList<>();
        for (int repetition = 0; repetition < repetitions; repetition++) {
            if (System.nanoTime() >= deadline) {
                break;
            }
            int checksum = 0;
            long start = System.nanoTime();
            for (int i = 0; i < searches; i++) {
                checksum += search.find(values, key);
            }
            long elapsed = System.nanoTime() - start;
            blackHole = checksum;
            times.add(elapsed);
        }
        return times;
    }

    private static String status(List<Long> times, int repetitions) {
        return times.size() == repetitions ? "medido" : "timeout";
    }

    private static String[] row(String algorithm, int size, String type, String position,
                                String keySet, String presence, List<Long> times,
                                int searches, int repetitions, int warmups, boolean timeout) {
        String[] row = new String[FIELDS.length];
        for (int i = 0; i < row.length; i++) {
            row[i] = "";
        }
        row[0] = type + "_" + algorithm + "_" + size + "_" + (position.isEmpty() ? keySet : position);
        row[1] = algorithm;
        row[2] = "java";
        row[3] = "asc_" + size;
        row[4] = Integer.toString(size);
        row[5] = type;
        row[6] = position;
        row[7] = keySet;
        row[8] = presence;
        double total = 0.0;
        for (int i = 0; i < times.size(); i++) {
            row[9 + i] = Long.toString(times.get(i));
            total += times.get(i) / (double) searches;
        }
        if (!times.isEmpty()) {
            double average = total / times.size();
            double variance = 0.0;
            for (long time : times) {
                double value = time / (double) searches;
                variance += (value - average) * (value - average);
            }
            row[14] = Double.toString(average);
            row[15] = Double.toString(times.size() > 1
                ? Math.sqrt(variance / (times.size() - 1)) : 0.0);
        }
        row[16] = timeout ? "no_medido" : "medido";
        row[17] = "false";
        row[20] = Integer.toString(repetitions);
        row[21] = Integer.toString(searches);
        row[22] = Integer.toString(warmups);
        row[23] = timeout ? "timeout" : "";
        return row;
    }

    private static void writeCsv(Path output, List<String[]> rows) throws IOException {
        Files.createDirectories(output.getParent());
        try (BufferedWriter writer = Files.newBufferedWriter(output)) {
            writer.write(String.join(",", FIELDS));
            writer.newLine();
            for (String[] row : rows) {
                for (int i = 0; i < row.length; i++) {
                    if (i > 0) {
                        writer.write(',');
                    }
                    writer.write(csv(row[i]));
                }
                writer.newLine();
            }
        }
    }

    private static String csv(String value) {
        if (value.contains(",") || value.contains("\"")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }

    private static boolean contains(int[] values, int target) {
        for (int value : values) {
            if (value == target) return true;
        }
        return false;
    }

    private static final class Key {
        private final int key;
        private final String presence;

        private Key(int key, String presence) {
            this.key = key;
            this.presence = presence;
        }
    }

    private static final class Config {
        private Path root;
        private Path output;
        private int[] sizes = DEFAULT_SIZES;
        private int repetitions = 5;
        private int positionSearches = 1000;
        private double timeoutSeconds = 300.0;
        private boolean positions = true;

        private static Config parse(String[] args) {
            Config config = new Config();
            config.root = Path.of(System.getProperty("user.dir"));
            for (String arg : args) {
                if (arg.startsWith("--root=")) config.root = Path.of(arg.substring(7));
                else if (arg.startsWith("--output=")) config.output = Path.of(arg.substring(9));
                else if (arg.startsWith("--sizes=")) config.sizes = parseSizes(arg.substring(8));
                else if (arg.startsWith("--repetitions=")) config.repetitions = Integer.parseInt(arg.substring(14));
                else if (arg.startsWith("--position-searches=")) config.positionSearches = Integer.parseInt(arg.substring(20));
                else if (arg.startsWith("--timeout-seconds=")) config.timeoutSeconds = Double.parseDouble(arg.substring(18));
                else if (arg.equals("--no-positions")) config.positions = false;
                else throw new IllegalArgumentException("unknown argument: " + arg);
            }
            if (config.output == null) {
                config.output = config.root.resolve("results").resolve("java").resolve("search_measurements.csv");
            }
            return config;
        }

        private static int[] parseSizes(String value) {
            String[] parts = value.split(",");
            int[] sizes = new int[parts.length];
            for (int i = 0; i < parts.length; i++) sizes[i] = Integer.parseInt(parts[i]);
            return sizes;
        }
    }
}

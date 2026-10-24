import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class BenchOrdenamiento {

    // ---------------- 1) Insertion Sort ----------------
    static void insertionSort(int arr[]) {
        int n = arr.length;
        for (int i = 1; i < n; ++i) {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j = j - 1;
            }
            arr[j + 1] = key;
        }
    }

    // Insertion sort interno
    static void insertionSortList(List<Integer> bucket) {
        for (int i = 1; i < bucket.size(); ++i) {
            int key = bucket.get(i);
            int j = i - 1;
            while (j >= 0 && bucket.get(j) > key) {
                bucket.set(j + 1, bucket.get(j));
                j--;
            }
            bucket.set(j + 1, key);
        }
    }

    // ---------------- 2) Dual-Pivot QuickSort ----------------
    static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    static void dualPivotQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            // piv[0] = pivote izquierdo, piv[1] = pivote derecho
            int[] piv;
            piv = partition(arr, low, high);
            dualPivotQuickSort(arr, low, piv[0] - 1);
            dualPivotQuickSort(arr, piv[0] + 1, piv[1] - 1);
            dualPivotQuickSort(arr, piv[1] + 1, high);
        }
    }

    static int[] partition(int[] arr, int low, int high) {
        if (arr[low] > arr[high])
            swap(arr, low, high);

        // p es el pivote izquierdo (PRIMERO), q el derecho (ULTIMO)
        int j = low + 1;
        int g = high - 1, k = low + 1, p = arr[low], q = arr[high];

        while (k <= g) {
            // Elementos menores que el pivote izquierdo
            if (arr[k] < p) {
                swap(arr, k, j);
                j++;
            }
            // Elementos mayores o iguales que el pivote derecho
            else if (arr[k] >= q) {
                while (arr[g] > q && k < g)
                    g--;
                swap(arr, k, g);
                g--;
                if (arr[k] < p) {
                    swap(arr, k, j);
                    j++;
                }
            }
            k++;
        }
        j--;
        g++;

        // Llevar pivotes a su posicion final
        swap(arr, low, j);
        swap(arr, high, g);

        return new int[] { j, g };
    }

    static void dualPivotQuickSortWrap(int[] arr) {
        if (arr.length > 0)
            dualPivotQuickSort(arr, 0, arr.length - 1);
    }

    // ---------------- 3) Merge Sort ----------------
    static void merge(int arr[], int l, int m, int r) {
        int n1 = m - l + 1;
        int n2 = r - m;

        int L[] = new int[n1];
        int R[] = new int[n2];

        for (int i = 0; i < n1; ++i)
            L[i] = arr[l + i];
        for (int j = 0; j < n2; ++j)
            R[j] = arr[m + 1 + j];

        int i = 0, j = 0;
        int k = l;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) {
                arr[k] = L[i];
                i++;
            } else {
                arr[k] = R[j];
                j++;
            }
            k++;
        }

        while (i < n1) {
            arr[k] = L[i];
            i++;
            k++;
        }

        while (j < n2) {
            arr[k] = R[j];
            j++;
            k++;
        }
    }

    static void mergeSort(int arr[], int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    static void mergeSortWrap(int[] arr) {
        if (arr.length > 0)
            mergeSort(arr, 0, arr.length - 1);
    }

    // ---------------- 4) Heap Sort ----------------
    static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int l = 2 * i + 1;
        int r = 2 * i + 2;

        if (l < n && arr[l] > arr[largest])
            largest = l;

        if (r < n && arr[r] > arr[largest])
            largest = r;

        if (largest != i) {
            int temp = arr[i];
            arr[i] = arr[largest];
            arr[largest] = temp;

            heapify(arr, n, largest);
        }
    }

    static void heapSort(int[] arr) {
        int n = arr.length;

        for (int i = n / 2 - 1; i >= 0; i--)
            heapify(arr, n, i);

        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;

            heapify(arr, i, 0);
        }
    }

    // ---------------- 5) Radix Sort BASE 10 ----------------
    static int getMax(int arr[], int n) {
        int mx = arr[0];
        for (int i = 1; i < n; i++)
            if (arr[i] > mx)
                mx = arr[i];
        return mx;
    }

    static void countSort(int arr[], int n, int exp) {
        int output[] = new int[n];
        int i;
        int count[] = new int[10];
        Arrays.fill(count, 0);

        for (i = 0; i < n; i++)
            count[(arr[i] / exp) % 10]++;

        for (i = 1; i < 10; i++)
            count[i] += count[i - 1];

        for (i = n - 1; i >= 0; i--) {
            output[count[(arr[i] / exp) % 10] - 1] = arr[i];
            count[(arr[i] / exp) % 10]--;
        }

        for (i = 0; i < n; i++)
            arr[i] = output[i];
    }

    static void radixsort(int arr[], int n) {
        int m = getMax(arr, n);
        // exp = 10^i: base 10, un counting sort por digito decimal
        for (int exp = 1; m / exp > 0; exp *= 10)
            countSort(arr, n, exp);
    }

    static void radixSortWrap(int[] arr) {
        if (arr.length > 0)
            radixsort(arr, arr.length);
    }

    // ---------------- 6) Bucket Sort adaptado a enteros ----------------
    // GfG original: floats en [0,1) con n cubetas, bi = (int)(n * arr[i]).

    static final int N_BUCKETS = 1000;
    static final long BUCKET_LO = 10000000L;
    static final long BUCKET_RANGE = 90000000L;

    static void bucketSortInt(int[] arr) {
        int n = arr.length;
        if (n < 2)
            return;

        @SuppressWarnings("unchecked")
        List<Integer>[] buckets = new ArrayList[N_BUCKETS];
        for (int i = 0; i < N_BUCKETS; i++)
            buckets[i] = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            int bi = (int) (((long) arr[i] - BUCKET_LO) * N_BUCKETS / BUCKET_RANGE);
            if (bi < 0)
                bi = 0;
            if (bi >= N_BUCKETS)
                bi = N_BUCKETS - 1;
            buckets[bi].add(arr[i]);
        }

        for (int i = 0; i < N_BUCKETS; i++)
            insertionSortList(buckets[i]);

        int index = 0;
        for (int i = 0; i < N_BUCKETS; i++)
            for (int j = 0; j < buckets[i].size(); j++)
                arr[index++] = buckets[i].get(j);
    }

    // --------------------------------
    static boolean isSorted(int[] arr) {
        for (int i = 1; i < arr.length; i++)
            if (arr[i - 1] > arr[i])
                return false;
        return true;
    }

    @FunctionalInterface
    interface SortFn {
        void sort(int[] a);
    }

    public static void main(String[] args) throws IOException {
        if (args.length < 2) {
            System.err.println("Uso: java BenchOrdenamiento <algoritmo> <archivo_datos> [reps=5]");
            System.exit(2);
        }
        String algo = args[0];
        String path = args[1];
        int reps = (args.length >= 3) ? Integer.parseInt(args[2]) : 5;
        if (reps < 1)
            reps = 1;

        SortFn sortFn;
        switch (algo) {
            case "insertion": sortFn = BenchOrdenamiento::insertionSort; break;
            case "dual_pivot_quicksort": sortFn = BenchOrdenamiento::dualPivotQuickSortWrap; break;
            case "merge": sortFn = BenchOrdenamiento::mergeSortWrap; break;
            case "heap": sortFn = BenchOrdenamiento::heapSort; break;
            case "radix": sortFn = BenchOrdenamiento::radixSortWrap; break;
            case "bucket": sortFn = BenchOrdenamiento::bucketSortInt; break;
            default:
                System.err.println("Algoritmo desconocido: " + algo);
                System.exit(2);
                return;
        }

        // Lectura de datos ANTES de medir (un entero por linea)
        int[] base;
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String line;
            int[] tmp = new int[1100000];
            int count = 0;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (!line.isEmpty())
                    tmp[count++] = Integer.parseInt(line);
            }
            base = Arrays.copyOf(tmp, count);
        }
        if (base.length == 0) {
            System.err.println("Archivo sin datos: " + path);
            System.exit(3);
        }

        // 1 ejecucion de calentamiento (no contada; JIT). Sin try/catch:
        // si el algoritmo desborda la pila aqui, el error queda visible.
        {
            int[] w = Arrays.copyOf(base, base.length);
            sortFn.sort(w);
        }

        // 5 repeticiones sobre COPIA FRESCA; copia fuera del cronometro.
        // Solo el sort se mide con System.nanoTime().
        StringBuilder out = new StringBuilder();
        boolean ok = true;
        for (int r = 0; r < reps; r++) {
            int[] a = Arrays.copyOf(base, base.length); // copia fresca fuera del tiempo
            long t0 = System.nanoTime();
            sortFn.sort(a);
            long t1 = System.nanoTime();
            double ms = (t1 - t0) / 1_000_000.0;
            if (!isSorted(a))
                ok = false; // verificacion fuera del tiempo
            if (r > 0)
                out.append(' ');
            out.append(String.format(java.util.Locale.US, "%.3f", ms));
        }
        out.append(ok ? " OK" : " FAIL");
        System.out.println(out.toString());
        if (!ok)
            System.exit(1);
    }
}

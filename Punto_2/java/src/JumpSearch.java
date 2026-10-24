/**
 * Iterative jump search implementation for sorted input arrays.
 */
public final class JumpSearch {

    private JumpSearch() {
        // Utility class.
    }

    /**
     * Returns a valid index containing {@code x}, or -1 when it is absent.
     *
     * @param arr sorted input array in non-decreasing order
     * @param x value to find
     * @return a matching index, or -1
     */
    public static int search(int[] arr, int x) {
        int length = arr.length;
        if (length == 0) {
            return -1;
        }

        int blockSize = Math.max(1, (int) Math.sqrt(length));
        int step = blockSize;
        int previous = 0;

        while (arr[Math.min(step, length) - 1] < x) {
            previous = step;
            step += blockSize;
            if (previous >= length) {
                return -1;
            }
        }

        int blockEnd = Math.min(step, length);
        while (previous < blockEnd && arr[previous] < x) {
            previous++;
        }

        if (previous < blockEnd && arr[previous] == x) {
            return previous;
        }
        return -1;
    }
}

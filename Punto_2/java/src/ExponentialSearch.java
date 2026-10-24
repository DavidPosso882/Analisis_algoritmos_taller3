/**
 * Iterative exponential search implementation for sorted input arrays.
 */
public final class ExponentialSearch {

    private ExponentialSearch() {
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
        if (arr[0] == x) {
            return 0;
        }

        int bound = 1;
        while (bound < length && arr[bound] <= x) {
            if (bound > length / 2) {
                bound = length;
            } else {
                bound *= 2;
            }
        }

        return binarySearch(arr, bound / 2, Math.min(bound, length - 1), x);
    }

    private static int binarySearch(int[] arr, int low, int high, int x) {
        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] == x) {
                return mid;
            }
            if (arr[mid] < x) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return -1;
    }
}

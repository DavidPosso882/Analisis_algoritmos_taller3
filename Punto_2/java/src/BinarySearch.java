/**
 * Iterative binary search implementation for sorted input arrays.
 */
public final class BinarySearch {

    private BinarySearch() {
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
        int low = 0;
        int high = arr.length - 1;

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

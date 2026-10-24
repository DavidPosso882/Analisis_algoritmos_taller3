/**
 * Iterative ternary search implementation for sorted input arrays.
 */
public final class TernarySearch {

    private TernarySearch() {
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
        int left = 0;
        int right = arr.length - 1;

        while (left <= right) {
            int mid1 = left + (right - left) / 3;
            int mid2 = right - (right - left) / 3;

            if (arr[mid1] == x) {
                return mid1;
            }
            if (arr[mid2] == x) {
                return mid2;
            }

            if (x < arr[mid1]) {
                right = mid1 - 1;
            } else if (x > arr[mid2]) {
                left = mid2 + 1;
            } else {
                left = mid1 + 1;
                right = mid2 - 1;
            }
        }

        return -1;
    }
}

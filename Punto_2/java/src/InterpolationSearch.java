/**
 * Iterative interpolation search implementation for sorted input arrays.
 */
public final class InterpolationSearch {

    private InterpolationSearch() {
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

        while (low <= high && arr[low] <= x && x <= arr[high]) {
            if (arr[low] == arr[high]) {
                return arr[low] == x ? low : -1;
            }

            long offset = (long) (high - low) * (x - (long) arr[low]);
            int position = low
                + (int) (offset / (arr[high] - (long) arr[low]));

            if (arr[position] == x) {
                return position;
            }
            if (arr[position] < x) {
                low = position + 1;
            } else {
                high = position - 1;
            }
        }

        return -1;
    }
}

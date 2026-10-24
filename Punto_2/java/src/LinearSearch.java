/**
 * Linear search implementation used by the search-algorithm comparison.
 */
public final class LinearSearch {

    private LinearSearch() {
        // Utility class.
    }

    /**
     * Returns the first index containing {@code x}, or -1 when it is absent.
     *
     * @param arr input array; it may be empty or unsorted
     * @param x value to find
     * @return first matching index, or -1
     */
    public static int search(int[] arr, int x) {
        for (int index = 0; index < arr.length; index++) {
            if (arr[index] == x) {
                return index;
            }
        }
        return -1;
    }
}

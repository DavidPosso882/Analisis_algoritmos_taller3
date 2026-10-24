import java.util.Arrays;

public final class LinearSearchTest {

    private LinearSearchTest() {
    }

    public static void main(String[] args) {
        testEmptyArrayReturnsMinusOne();
        testSingleElementPresent();
        testSingleElementAbsent();
        testPresentAtFirstMiddleAndLastPositions();
        testAbsentKeyReturnsMinusOne();
        testDuplicatesReturnFirstValidIndex();
        testUnsortedArrayIsTraversedWithoutSorting();
        testInputIsNotModified();
        System.out.println("8 tests passed");
    }

    private static void testEmptyArrayReturnsMinusOne() {
        assertEquals(-1, LinearSearch.search(new int[0], 10));
    }

    private static void testSingleElementPresent() {
        assertEquals(0, LinearSearch.search(new int[]{10}, 10));
    }

    private static void testSingleElementAbsent() {
        assertEquals(-1, LinearSearch.search(new int[]{10}, 11));
    }

    private static void testPresentAtFirstMiddleAndLastPositions() {
        int[] values = {2, 3, 4, 10, 40};
        assertEquals(0, LinearSearch.search(values, 2));
        assertEquals(2, LinearSearch.search(values, 4));
        assertEquals(4, LinearSearch.search(values, 40));
    }

    private static void testAbsentKeyReturnsMinusOne() {
        assertEquals(-1, LinearSearch.search(new int[]{2, 3, 4, 10, 40}, 5));
    }

    private static void testDuplicatesReturnFirstValidIndex() {
        assertEquals(1, LinearSearch.search(new int[]{2, 7, 7, 7, 10}, 7));
    }

    private static void testUnsortedArrayIsTraversedWithoutSorting() {
        assertEquals(1, LinearSearch.search(new int[]{8, 3, 5, 3}, 3));
    }

    private static void testInputIsNotModified() {
        int[] values = {4, 1, 4};
        int[] snapshot = values.clone();
        LinearSearch.search(values, 4);
        if (!Arrays.equals(snapshot, values)) {
            throw new AssertionError("search modified the input array");
        }
    }

    private static void assertEquals(int expected, int actual) {
        if (expected != actual) {
            throw new AssertionError(
                "expected " + expected + " but got " + actual
            );
        }
    }
}

import java.util.Arrays;

public final class BinarySearchTest {

    private BinarySearchTest() {
    }

    public static void main(String[] args) {
        testEmptyArrayReturnsMinusOne();
        testSingleElementPresent();
        testSingleElementAbsent();
        testPresentAtFirstMiddleAndLastPositions();
        testAbsentKeyReturnsMinusOne();
        testBoundaryAbsentKeys();
        testDuplicatesReturnValidMatchingIndex();
        testInputIsNotModified();
        System.out.println("8 tests passed");
    }

    private static void testEmptyArrayReturnsMinusOne() {
        assertEquals(-1, BinarySearch.search(new int[0], 10));
    }

    private static void testSingleElementPresent() {
        assertEquals(0, BinarySearch.search(new int[]{10}, 10));
    }

    private static void testSingleElementAbsent() {
        assertEquals(-1, BinarySearch.search(new int[]{10}, 11));
    }

    private static void testPresentAtFirstMiddleAndLastPositions() {
        int[] values = {2, 3, 4, 10, 40};
        assertValidMatch(values, 2);
        assertValidMatch(values, 4);
        assertValidMatch(values, 40);
    }

    private static void testAbsentKeyReturnsMinusOne() {
        assertEquals(-1, BinarySearch.search(new int[]{2, 3, 4, 10, 40}, 5));
    }

    private static void testBoundaryAbsentKeys() {
        int[] values = {10, 20, 30};
        assertEquals(-1, BinarySearch.search(values, 9));
        assertEquals(-1, BinarySearch.search(values, 31));
    }

    private static void testDuplicatesReturnValidMatchingIndex() {
        int[] values = {2, 7, 7, 7, 10};
        assertValidMatch(values, 7);
    }

    private static void testInputIsNotModified() {
        int[] values = {1, 4, 8, 12};
        int[] snapshot = values.clone();
        BinarySearch.search(values, 8);
        if (!Arrays.equals(snapshot, values)) {
            throw new AssertionError("search modified the input array");
        }
    }

    private static void assertValidMatch(int[] values, int target) {
        int index = BinarySearch.search(values, target);
        if (index < 0 || index >= values.length || values[index] != target) {
            throw new AssertionError("returned index does not contain target");
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

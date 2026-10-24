import java.util.Arrays;

public final class TernarySearchTest {

    private TernarySearchTest() {
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
        assertEquals(-1, TernarySearch.search(new int[0], 10));
    }

    private static void testSingleElementPresent() {
        assertEquals(0, TernarySearch.search(new int[]{10}, 10));
    }

    private static void testSingleElementAbsent() {
        assertEquals(-1, TernarySearch.search(new int[]{10}, 11));
    }

    private static void testPresentAtFirstMiddleAndLastPositions() {
        int[] values = {1, 2, 3, 4, 6};
        assertValidMatch(values, 1);
        assertValidMatch(values, 3);
        assertValidMatch(values, 6);
    }

    private static void testAbsentKeyReturnsMinusOne() {
        assertEquals(-1, TernarySearch.search(new int[]{1, 2, 3, 4, 6}, 5));
    }

    private static void testBoundaryAbsentKeys() {
        int[] values = {10, 20, 30};
        assertEquals(-1, TernarySearch.search(values, 9));
        assertEquals(-1, TernarySearch.search(values, 31));
    }

    private static void testDuplicatesReturnValidMatchingIndex() {
        int[] values = {1, 4, 4, 4, 9};
        assertValidMatch(values, 4);
    }

    private static void testInputIsNotModified() {
        int[] values = {1, 4, 8, 12};
        int[] snapshot = values.clone();
        TernarySearch.search(values, 8);
        if (!Arrays.equals(snapshot, values)) {
            throw new AssertionError("search modified the input array");
        }
    }

    private static void assertValidMatch(int[] values, int target) {
        int index = TernarySearch.search(values, target);
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

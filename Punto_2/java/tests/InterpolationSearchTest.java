import java.util.Arrays;

public final class InterpolationSearchTest {

    private InterpolationSearchTest() {
    }

    public static void main(String[] args) {
        testEmptyArrayReturnsMinusOne();
        testSingleElementPresent();
        testSingleElementAbsent();
        testPresentAtFirstMiddleAndLastPositions();
        testAbsentKeyReturnsMinusOne();
        testBoundaryAbsentKeys();
        testDuplicatesReturnValidMatchingIndex();
        testAllEqualValuesAvoidZeroDivision();
        testInterpolationArithmeticDoesNotOverflow();
        testInputIsNotModified();
        System.out.println("10 tests passed");
    }

    private static void testEmptyArrayReturnsMinusOne() {
        assertEquals(-1, InterpolationSearch.search(new int[0], 10));
    }

    private static void testSingleElementPresent() {
        assertEquals(0, InterpolationSearch.search(new int[]{10}, 10));
    }

    private static void testSingleElementAbsent() {
        assertEquals(-1, InterpolationSearch.search(new int[]{10}, 11));
    }

    private static void testPresentAtFirstMiddleAndLastPositions() {
        int[] values = {10, 12, 13, 16, 18, 19, 20, 21, 22, 23, 24, 33, 35, 42, 47};
        assertValidMatch(values, 10);
        assertValidMatch(values, 20);
        assertValidMatch(values, 47);
    }

    private static void testAbsentKeyReturnsMinusOne() {
        assertEquals(
            -1,
            InterpolationSearch.search(new int[]{10, 12, 16, 20, 24}, 18)
        );
    }

    private static void testBoundaryAbsentKeys() {
        int[] values = {10, 20, 30};
        assertEquals(-1, InterpolationSearch.search(values, 9));
        assertEquals(-1, InterpolationSearch.search(values, 31));
    }

    private static void testDuplicatesReturnValidMatchingIndex() {
        int[] values = {1, 4, 4, 4, 9};
        assertValidMatch(values, 4);
    }

    private static void testAllEqualValuesAvoidZeroDivision() {
        int[] values = {7, 7, 7, 7};
        assertValidMatch(values, 7);
        assertEquals(-1, InterpolationSearch.search(values, 6));
        assertEquals(-1, InterpolationSearch.search(values, 8));
    }

    private static void testInterpolationArithmeticDoesNotOverflow() {
        int[] values = {Integer.MIN_VALUE, 0, Integer.MAX_VALUE};
        assertEquals(1, InterpolationSearch.search(values, 0));
    }

    private static void testInputIsNotModified() {
        int[] values = {1, 4, 8, 12};
        int[] snapshot = values.clone();
        InterpolationSearch.search(values, 8);
        if (!Arrays.equals(snapshot, values)) {
            throw new AssertionError("search modified the input array");
        }
    }

    private static void assertValidMatch(int[] values, int target) {
        int index = InterpolationSearch.search(values, target);
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

import unittest

from python.algorithms.interpolation_search import search


class InterpolationSearchTests(unittest.TestCase):
    def test_empty_array_returns_minus_one(self):
        self.assertEqual(search([], 10), -1)

    def test_single_element_present(self):
        self.assertEqual(search([10], 10), 0)

    def test_single_element_absent(self):
        self.assertEqual(search([10], 11), -1)

    def test_present_at_first_middle_and_last_positions(self):
        values = [10, 12, 13, 16, 18, 19, 20, 21, 22, 23, 24, 33, 35, 42, 47]
        for value in (10, 20, 47):
            index = search(values, value)
            self.assertGreaterEqual(index, 0)
            self.assertEqual(values[index], value)

    def test_absent_key_returns_minus_one(self):
        self.assertEqual(search([10, 12, 16, 20, 24], 18), -1)

    def test_boundary_absent_keys(self):
        values = [10, 20, 30]
        self.assertEqual(search(values, 9), -1)
        self.assertEqual(search(values, 31), -1)

    def test_duplicates_return_a_valid_matching_index(self):
        values = [1, 4, 4, 4, 9]
        index = search(values, 4)
        self.assertIn(index, (1, 2, 3))
        self.assertEqual(values[index], 4)

    def test_all_equal_values_avoid_zero_division(self):
        values = [7, 7, 7, 7]
        self.assertIn(search(values, 7), range(len(values)))
        self.assertEqual(search(values, 6), -1)
        self.assertEqual(search(values, 8), -1)

    def test_input_is_not_modified(self):
        values = [1, 4, 8, 12]
        snapshot = values.copy()
        search(values, 8)
        self.assertEqual(values, snapshot)


if __name__ == "__main__":
    unittest.main()

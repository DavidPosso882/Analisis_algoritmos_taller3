import unittest

from python.algorithms.binary_search import search


class BinarySearchTests(unittest.TestCase):
    def test_empty_array_returns_minus_one(self):
        self.assertEqual(search([], 10), -1)

    def test_single_element_present(self):
        self.assertEqual(search([10], 10), 0)

    def test_single_element_absent(self):
        self.assertEqual(search([10], 11), -1)

    def test_present_at_first_middle_and_last_positions(self):
        values = [2, 3, 4, 10, 40]
        for value in (2, 4, 40):
            index = search(values, value)
            self.assertGreaterEqual(index, 0)
            self.assertEqual(values[index], value)

    def test_absent_key_returns_minus_one(self):
        self.assertEqual(search([2, 3, 4, 10, 40], 5), -1)

    def test_duplicates_return_a_valid_matching_index(self):
        values = [2, 7, 7, 7, 10]
        index = search(values, 7)
        self.assertGreaterEqual(index, 1)
        self.assertLessEqual(index, 3)
        self.assertEqual(values[index], 7)

    def test_boundary_absent_keys(self):
        values = [10, 20, 30]
        self.assertEqual(search(values, 9), -1)
        self.assertEqual(search(values, 31), -1)

    def test_input_is_not_modified(self):
        values = [1, 4, 8, 12]
        snapshot = values.copy()
        search(values, 8)
        self.assertEqual(values, snapshot)


if __name__ == "__main__":
    unittest.main()

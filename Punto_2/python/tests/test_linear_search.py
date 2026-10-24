import unittest

from python.algorithms.linear_search import search


class LinearSearchTests(unittest.TestCase):
    def test_empty_array_returns_minus_one(self):
        self.assertEqual(search([], 10), -1)

    def test_single_element_present(self):
        self.assertEqual(search([10], 10), 0)

    def test_single_element_absent(self):
        self.assertEqual(search([10], 11), -1)

    def test_present_at_first_middle_and_last_positions(self):
        values = [2, 3, 4, 10, 40]
        self.assertEqual(search(values, 2), 0)
        self.assertEqual(search(values, 4), 2)
        self.assertEqual(search(values, 40), 4)

    def test_absent_key_returns_minus_one(self):
        self.assertEqual(search([2, 3, 4, 10, 40], 5), -1)

    def test_duplicates_return_first_valid_index(self):
        self.assertEqual(search([2, 7, 7, 7, 10], 7), 1)

    def test_unsorted_sequence_is_traversed_without_sorting(self):
        self.assertEqual(search([8, 3, 5, 3], 3), 1)

    def test_input_is_not_modified(self):
        values = [4, 1, 4]
        snapshot = values.copy()
        search(values, 4)
        self.assertEqual(values, snapshot)


if __name__ == "__main__":
    unittest.main()

import csv
import tempfile
import unittest
from pathlib import Path

from python.experiments.measure_search import (
    ALGORITHMS,
    FIELDS,
    load_array,
    load_keys,
    measure,
)


class MeasurementTests(unittest.TestCase):
    def test_loaders_validate_real_data_shape(self):
        root = Path(__file__).parents[2]
        values = load_array(root, 1000)
        keys = load_keys(root, 1000)
        self.assertEqual(len(values), 1000)
        self.assertEqual(len(keys), 1000)
        self.assertEqual(sum(p == "PRESENTE" for _, p in keys), 500)

    def test_small_run_produces_expected_combinations(self):
        root = Path(__file__).parents[2]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "measurements.csv"
            rows = measure(root, output, sizes=(1000,), repetitions=1, include_positions=False)
            self.assertEqual(len(rows), len(ALGORITHMS))
            with output.open(encoding="utf-8", newline="") as handle:
                records = list(csv.DictReader(handle))
            self.assertEqual(len(records), len(ALGORITHMS))
            self.assertEqual(tuple(records[0].keys()), FIELDS)
            self.assertTrue(all(row["status"] == "medido" for row in records))
            self.assertTrue(all(float(row["mean_ns"]) >= 0 for row in records))


if __name__ == "__main__":
    unittest.main()

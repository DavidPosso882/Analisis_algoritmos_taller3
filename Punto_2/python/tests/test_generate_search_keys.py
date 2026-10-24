import tempfile
import unittest
from pathlib import Path

from python.generate_search_keys import (
    ABSENT_COUNT,
    BASE_SEED,
    KeyGenerationError,
    PRESENT_COUNT,
    TOTAL_COUNT,
    generate_key_files,
    read_array,
)


class SearchKeyGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.data_dir = self.root / "data"
        self.output_dir = self.root / "search_keys"
        self.data_dir.mkdir()
        self.datasets = {501: "asc_501.txt"}
        values = list(range(10_000_000, 10_000_500))
        values.insert(2, values[2])
        (self.data_dir / "asc_501.txt").write_text(
            "\n".join(str(value) for value in values) + "\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generation_counts_and_membership(self):
        paths = generate_key_files(self.data_dir, self.output_dir, self.datasets)
        rows = paths[0].read_text(encoding="utf-8").splitlines()
        self.assertEqual(rows[0], "key_id\tkey\tpresence\tn")
        records = [line.split("\t") for line in rows[1:]]
        self.assertEqual(len(records), TOTAL_COUNT)
        self.assertEqual(sum(record[2] == "PRESENTE" for record in records), PRESENT_COUNT)
        self.assertEqual(sum(record[2] == "AUSENTE" for record in records), ABSENT_COUNT)
        keys = [int(record[1]) for record in records]
        self.assertEqual(len(keys), len(set(keys)))
        values = set(read_array(self.data_dir / "asc_501.txt", 501))
        self.assertTrue(all(int(r[1]) in values for r in records if r[2] == "PRESENTE"))
        self.assertTrue(all(int(r[1]) not in values for r in records if r[2] == "AUSENTE"))
        self.assertTrue(all(10_000_000 <= int(r[1]) <= 99_999_999 for r in records))
        self.assertTrue(all(int(r[3]) == 501 for r in records))

    def test_reproducibility_with_same_seed(self):
        first = self.root / "first"
        second = self.root / "second"
        generate_key_files(self.data_dir, first, self.datasets)
        generate_key_files(self.data_dir, second, self.datasets)
        self.assertEqual(
            (first / "keys_501.txt").read_bytes(),
            (second / "keys_501.txt").read_bytes(),
        )
        self.assertEqual(BASE_SEED, 0x5EED20261017A)

    def test_existing_destination_is_rejected(self):
        self.output_dir.mkdir()
        destination = self.output_dir / "keys_501.txt"
        destination.write_text("do not replace\n", encoding="utf-8")
        with self.assertRaises(KeyGenerationError):
            generate_key_files(self.data_dir, self.output_dir, self.datasets)
        self.assertEqual(destination.read_text(encoding="utf-8"), "do not replace\n")

    def test_read_errors_are_reported(self):
        with self.assertRaisesRegex(KeyGenerationError, "No se pudo leer"):
            read_array(self.data_dir / "missing.txt", 501)

    def test_invalid_data_is_reported(self):
        invalid = self.data_dir / "invalid.txt"
        invalid.write_text("10000000\nnot-an-integer\n", encoding="utf-8")
        with self.assertRaisesRegex(KeyGenerationError, "no contiene un entero"):
            read_array(invalid, 2)
        out_of_domain = self.data_dir / "out_of_domain.txt"
        out_of_domain.write_text("9999999\n", encoding="utf-8")
        with self.assertRaisesRegex(KeyGenerationError, "fuera del dominio"):
            read_array(out_of_domain, 1)

    def test_invalid_order_and_size_are_reported(self):
        invalid = self.data_dir / "unsorted.txt"
        invalid.write_text("10000002\n10000001\n", encoding="utf-8")
        with self.assertRaisesRegex(KeyGenerationError, "no están en orden"):
            read_array(invalid, 2)
        with self.assertRaisesRegex(KeyGenerationError, "se esperaban 3"):
            read_array(self.data_dir / "asc_501.txt", 3)


if __name__ == "__main__":
    unittest.main()

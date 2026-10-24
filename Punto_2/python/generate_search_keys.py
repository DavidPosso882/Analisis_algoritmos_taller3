"""Generate deterministic present/absent search keys for each input array."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
from typing import Iterable

BASE_SEED = 0x5EED20261017A
MIN_KEY = 10_000_000
MAX_KEY = 99_999_999
PRESENT_COUNT = 500
ABSENT_COUNT = 500
TOTAL_COUNT = PRESENT_COUNT + ABSENT_COUNT

DEFAULT_DATASETS = {
    1_000: "asc_1000.txt",
    10_000: "asc_10000.txt",
    100_000: "asc_100000.txt",
    1_000_000: "asc_1000000.txt",
}


class KeyGenerationError(RuntimeError):
    """Raised when input data or output conditions prevent valid generation."""


class SplitMix64:
    """Small deterministic generator with unbiased bounded integer selection."""

    _MASK = (1 << 64) - 1

    def __init__(self, seed: int) -> None:
        self._state = seed & self._MASK

    def next_uint64(self) -> int:
        self._state = (self._state + 0x9E3779B97F4A7C15) & self._MASK
        value = self._state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & self._MASK
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & self._MASK
        return (value ^ (value >> 31)) & self._MASK

    def bounded(self, bound: int) -> int:
        if bound <= 0:
            raise ValueError("bound debe ser positivo")
        limit = self._MASK - (self._MASK % bound)
        while True:
            value = self.next_uint64()
            if value < limit:
                return value % bound


def read_array(path: Path, expected_size: int) -> list[int]:
    """Read and validate one original array without changing it."""
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            values: list[int] = []
            previous: int | None = None
            for line_number, raw_line in enumerate(handle, start=1):
                text = raw_line.strip()
                if not text:
                    raise KeyGenerationError(
                        f"{path}: línea {line_number} vacía; se esperaba un entero"
                    )
                try:
                    value = int(text, 10)
                except ValueError as exc:
                    raise KeyGenerationError(
                        f"{path}: línea {line_number} no contiene un entero válido"
                    ) from exc
                if not MIN_KEY <= value <= MAX_KEY:
                    raise KeyGenerationError(
                        f"{path}: línea {line_number} fuera del dominio de ocho dígitos"
                    )
                if previous is not None and value < previous:
                    raise KeyGenerationError(
                        f"{path}: valores no están en orden no decreciente"
                    )
                values.append(value)
                previous = value
        if len(values) != expected_size:
            raise KeyGenerationError(
                f"{path}: se esperaban {expected_size} valores, se encontraron {len(values)}"
            )
        return values
    except OSError as exc:
        raise KeyGenerationError(f"No se pudo leer {path}: {exc}") from exc


def _sample(values: list[int], size: int, rng: SplitMix64) -> list[int]:
    if len(values) < size:
        raise KeyGenerationError(
            f"No hay {size} valores distintos presentes disponibles; hay {len(values)}"
        )
    selected: list[int] = []
    remaining = list(values)
    for _ in range(size):
        index = rng.bounded(len(remaining))
        selected.append(remaining.pop(index))
    return selected


def _make_keys(array_values: list[int], size: int) -> list[tuple[str, int, str, int]]:
    distinct_values = sorted(set(array_values))
    rng = SplitMix64(BASE_SEED ^ size)
    present = _sample(distinct_values, PRESENT_COUNT, rng)
    array_set = set(array_values)
    absent: list[int] = []
    absent_set: set[int] = set()
    domain_size = MAX_KEY - MIN_KEY + 1
    while len(absent) < ABSENT_COUNT:
        candidate = MIN_KEY + rng.bounded(domain_size)
        if candidate not in array_set and candidate not in absent_set:
            absent.append(candidate)
            absent_set.add(candidate)

    rows = [
        (f"P{index:03d}", key, "PRESENTE", size)
        for index, key in enumerate(present, start=1)
    ]
    rows.extend(
        (f"A{index:03d}", key, "AUSENTE", size)
        for index, key in enumerate(absent, start=1)
    )
    _validate_rows(rows, array_set, size)
    return rows


def _validate_rows(
    rows: Iterable[tuple[str, int, str, int]], array_set: set[int], size: int
) -> None:
    materialized = list(rows)
    keys = [row[1] for row in materialized]
    if len(materialized) != TOTAL_COUNT or len(set(keys)) != TOTAL_COUNT:
        raise KeyGenerationError(f"El conjunto para n={size} no tiene 1.000 claves únicas")
    if sum(row[2] == "PRESENTE" for row in materialized) != PRESENT_COUNT:
        raise KeyGenerationError(f"El conjunto para n={size} no tiene 500 presentes")
    if sum(row[2] == "AUSENTE" for row in materialized) != ABSENT_COUNT:
        raise KeyGenerationError(f"El conjunto para n={size} no tiene 500 ausentes")
    for _, key, presence, row_size in materialized:
        if row_size != size or not MIN_KEY <= key <= MAX_KEY:
            raise KeyGenerationError(f"Clave inválida en el conjunto para n={size}")
        if presence == "PRESENTE" and key not in array_set:
            raise KeyGenerationError(f"Clave PRESENTE inexistente en el arreglo n={size}")
        if presence == "AUSENTE" and key in array_set:
            raise KeyGenerationError(f"Clave AUSENTE presente en el arreglo n={size}")


def generate_key_files(
    data_dir: Path,
    output_dir: Path,
    datasets: dict[int, str] | None = None,
) -> list[Path]:
    """Generate all key files, refusing existing destinations and partial output."""
    selected_datasets = datasets or DEFAULT_DATASETS
    destinations = [output_dir / f"keys_{size}.txt" for size in selected_datasets]
    existing = [path for path in destinations if path.exists()]
    if existing:
        names = ", ".join(str(path) for path in existing)
        raise KeyGenerationError(f"No se sobrescribirá ningún archivo existente: {names}")

    generated: list[tuple[Path, str]] = []
    for size, filename in selected_datasets.items():
        values = read_array(data_dir / filename, size)
        rows = _make_keys(values, size)
        content = "key_id\tkey\tpresence\tn\n" + "".join(
            f"{key_id}\t{key}\t{presence}\t{row_size}\n"
            for key_id, key, presence, row_size in rows
        )
        generated.append((output_dir / f"keys_{size}.txt", content))

    output_dir.mkdir(parents=True, exist_ok=True)
    temporary_paths: list[Path] = []
    try:
        for destination, content in generated:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                dir=output_dir,
                prefix=f".{destination.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary:
                temporary.write(content)
                temporary_paths.append(Path(temporary.name))
        for temporary, (destination, _) in zip(temporary_paths, generated):
            os.replace(temporary, destination)
        return destinations
    except OSError as exc:
        raise KeyGenerationError(f"No se pudieron escribir las claves: {exc}") from exc
    finally:
        for temporary in temporary_paths:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/search_keys"))
    args = parser.parse_args()
    try:
        paths = generate_key_files(args.data_dir, args.output_dir)
    except KeyGenerationError as exc:
        parser.error(str(exc))
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Generate position-result tables from the recorded measurement CSV files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ALGORITHMS = (
    "linear",
    "binary",
    "ternary",
    "jump",
    "interpolation",
    "exponential",
)
POSITIONS = ("start", "middle", "end")
POSITION_LABELS = {"start": "Inicio", "middle": "Centro", "end": "Final"}
TABLE_FIELDS = ("Algoritmo", "Inicio", "Centro", "Final")
REQUIRED_COLUMNS = {
    "algorithm",
    "language",
    "n",
    "experiment_type",
    "position",
    "mean_ns",
    "status",
    "repetitions",
    "searches_per_repetition",
    "is_estimated",
    "repetition_1_ns",
    "repetition_2_ns",
    "repetition_3_ns",
    "repetition_4_ns",
    "repetition_5_ns",
}


def read_position_rows(path: Path, language: str) -> dict[tuple[str, str], dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{path} missing columns: {', '.join(sorted(missing))}")

        selected: dict[tuple[str, str], dict[str, str]] = {}
        for row in reader:
            if (
                row["language"] != language
                or row["n"] != "1000000"
                or row["experiment_type"] != "position"
            ):
                continue
            key = (row["algorithm"], row["position"])
            if key in selected:
                raise ValueError(f"duplicate position measurement: {key} in {path}")
            selected[key] = row

    expected = {(algorithm, position) for algorithm in ALGORITHMS for position in POSITIONS}
    missing_keys = sorted(expected - selected.keys())
    unexpected_keys = sorted(selected.keys() - expected)
    if missing_keys:
        raise ValueError(f"missing position measurements in {path}: {missing_keys}")
    if unexpected_keys:
        raise ValueError(f"unexpected position measurements in {path}: {unexpected_keys}")
    if len(selected) != 18:
        raise ValueError(f"expected 18 position rows in {path}, found {len(selected)}")

    for key, row in selected.items():
        if row["status"] != "medido":
            raise ValueError(f"{key} is not medido: {row['status']}")
        if row["is_estimated"].lower() != "false":
            raise ValueError(f"{key} is estimated")
        if row["repetitions"] != "5":
            raise ValueError(f"{key} does not have five repetitions")
        if row["searches_per_repetition"] != "1000":
            raise ValueError(f"{key} does not have 1000 searches per repetition")
        for field in (
            "repetition_1_ns",
            "repetition_2_ns",
            "repetition_3_ns",
            "repetition_4_ns",
            "repetition_5_ns",
            "mean_ns",
        ):
            if not row[field]:
                raise ValueError(f"{key} has empty {field}")
            if float(row[field]) <= 0:
                raise ValueError(f"{key} has non-positive {field}")
    return selected


def table_rows(
    measurements: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, str]]:
    return [
        {
            "Algoritmo": algorithm,
            **{
                POSITION_LABELS[position]: measurements[(algorithm, position)]["mean_ns"]
                for position in POSITIONS
            },
        }
        for algorithm in ALGORITHMS
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TABLE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, language: str, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(
            f"# Experimento de posición de la clave — {language}\n\n"
            "Arreglo: `n = 1.000.000` elementos. "
            "Tiempos: promedio por búsqueda individual, en nanosegundos (`ns`), "
            "calculado a partir de 1.000 búsquedas por repetición y cinco "
            "repeticiones.\n\n"
        )
        handle.write("| " + " | ".join(TABLE_FIELDS) + " |\n")
        handle.write("| " + " | ".join("---" for _ in TABLE_FIELDS) + " |\n")
        for row in rows:
            handle.write("| " + " | ".join(row[field] for field in TABLE_FIELDS) + " |\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.resolve()

    outputs = []
    for language in ("python", "java"):
        source = root / "results" / language / "search_measurements.csv"
        measurements = read_position_rows(source, language)
        rows = table_rows(measurements)
        csv_path = root / "results" / "combined" / f"search_position_{language}.csv"
        markdown_path = root / "docs" / f"search_position_{language}.md"
        write_csv(csv_path, rows)
        write_markdown(markdown_path, language.capitalize(), rows)
        outputs.extend((csv_path, markdown_path))
        print(f"{language}: validated {len(measurements)} position measurements")
    for output in outputs:
        print(f"wrote {output}")


if __name__ == "__main__":
    main()

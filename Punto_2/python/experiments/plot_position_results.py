"""Generate position-experiment plots from the generated position tables."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ALGORITHMS = (
    "linear",
    "binary",
    "ternary",
    "jump",
    "interpolation",
    "exponential",
)
POSITIONS = ("Inicio", "Centro", "Final")
REQUIRED_COLUMNS = {"Algoritmo", *POSITIONS}


def read_table(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{path} missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)

    if len(rows) != len(ALGORITHMS):
        raise ValueError(f"{path} must contain six algorithms, found {len(rows)}")
    if [row["Algoritmo"] for row in rows] != list(ALGORITHMS):
        raise ValueError(f"{path} has missing, duplicated, or misordered algorithms")
    for row in rows:
        for position in POSITIONS:
            value = float(row[position])
            if value <= 0:
                raise ValueError(f"non-positive value in {path}: {row['Algoritmo']} {position}")
    return rows


def plot_table(rows: list[dict[str, str]], language: str, output: Path) -> None:
    positions = np.arange(len(ALGORITHMS))
    width = 0.24
    fig, axis = plt.subplots(figsize=(12, 7))
    bars = []
    for offset, position in enumerate(POSITIONS):
        values = [float(row[position]) for row in rows]
        bars.append(
            axis.bar(
                positions + (offset - 1) * width,
                values,
                width,
                label=position,
            )
        )

    axis.set_yscale("log")
    axis.set_xlabel("Algoritmo")
    axis.set_ylabel("Tiempo promedio por búsqueda (ns)")
    axis.set_title(f"Experimento de posición de la clave en {language} — n = 1.000.000")
    axis.set_xticks(positions)
    axis.set_xticklabels(ALGORITHMS)
    axis.grid(True, axis="y", which="both", alpha=0.25)
    axis.legend(title="Posición")

    for group in bars:
        for bar in group:
            axis.annotate(
                f"{bar.get_height():,.2f}",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                rotation=90,
                fontsize=7,
            )

    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.resolve()
    plot_dir = root / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)

    outputs = (
        ("python", "Python", plot_dir / "search_position_python.png"),
        ("java", "Java", plot_dir / "search_position_java.png"),
    )
    for language, label, output in outputs:
        source = root / "results" / "combined" / f"search_position_{language}.csv"
        rows = read_table(source)
        plot_table(rows, label, output)
        print(f"validated {source}: {len(rows)} algorithms")
        print(f"wrote {output}")


if __name__ == "__main__":
    main()

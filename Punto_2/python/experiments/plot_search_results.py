"""Generate the Point 2 search-result plots from existing CSV measurements."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Iterable

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
SIZES = (1000, 10000, 100000, 1000000)
REQUIRED_COLUMNS = {
    "algorithm",
    "language",
    "n",
    "experiment_type",
    "mean_ns",
    "status",
    "is_estimated",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or ())
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError(f"{path} is missing columns: {', '.join(sorted(missing))}")
        return list(reader)


def measured_rows(
    rows: Iterable[dict[str, str]], language: str
) -> tuple[dict[tuple[str, int], dict[str, str]], list[str]]:
    selected: dict[tuple[str, int], dict[str, str]] = {}
    omitted: list[str] = []
    for row in rows:
        if row["language"] != language or row["experiment_type"] != "all_keys":
            continue
        key = (row["algorithm"], int(row["n"]))
        status = row["status"]
        estimated = row["is_estimated"].lower() == "true"
        if status == "no_medido":
            omitted.append(row.get("experiment_id", repr(key)))
            continue
        if status != "medido" and not estimated:
            omitted.append(row.get("experiment_id", repr(key)))
            continue
        value = float(row["mean_ns"])
        if value <= 0:
            raise ValueError(f"non-positive mean_ns in {row.get('experiment_id', key)}")
        selected[key] = row
    return selected, omitted


def plot_growth(
    rows: dict[tuple[str, int], dict[str, str]],
    language: str,
    output: Path,
) -> None:
    fig, axis = plt.subplots(figsize=(10, 6))
    for algorithm in ALGORITHMS:
        points = [(size, rows[(algorithm, size)]) for size in SIZES if (algorithm, size) in rows]
        if not points:
            continue
        x = [size for size, _ in points]
        y = [float(row["mean_ns"]) for _, row in points]
        estimated = [row["is_estimated"].lower() == "true" for _, row in points]
        axis.plot(
            x,
            y,
            marker="o",
            linestyle="--" if any(estimated) else "-",
            label=algorithm,
        )
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel("Tamaño del arreglo, n (elementos)")
    axis.set_ylabel("Tiempo promedio por búsqueda (ns)")
    axis.set_title(f"Crecimiento de algoritmos de búsqueda en {language.capitalize()}")
    axis.set_xticks(SIZES)
    axis.set_xticklabels(["1.000", "10.000", "100.000", "1.000.000"])
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(title="Algoritmo")
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def plot_language_comparison(
    python_rows: dict[tuple[str, int], dict[str, str]],
    java_rows: dict[tuple[str, int], dict[str, str]],
    output: Path,
) -> None:
    values: dict[str, list[float]] = defaultdict(list)
    estimated: dict[str, list[bool]] = defaultdict(list)
    for algorithm in ALGORITHMS:
        for rows in (python_rows, java_rows):
            row = rows.get((algorithm, 1000000))
            if row is None:
                continue
            values[algorithm].append(float(row["mean_ns"]))
            estimated[algorithm].append(row["is_estimated"].lower() == "true")
    missing = [algorithm for algorithm in ALGORITHMS if len(values[algorithm]) != 2]
    if missing:
        raise ValueError(
            "missing n=1000000 all_keys data for comparison: " + ", ".join(missing)
        )

    positions = np.arange(len(ALGORITHMS))
    width = 0.38
    fig, axis = plt.subplots(figsize=(11, 6))
    bars_python = axis.bar(positions - width / 2, [values[a][0] for a in ALGORITHMS],
                           width, label="Python")
    bars_java = axis.bar(positions + width / 2, [values[a][1] for a in ALGORITHMS],
                         width, label="Java")
    axis.set_yscale("log")
    axis.set_xlabel("Algoritmo")
    axis.set_ylabel("Tiempo promedio por búsqueda (ns)")
    axis.set_title("Comparación Java frente a Python para n = 1.000.000")
    axis.set_xticks(positions)
    axis.set_xticklabels(ALGORITHMS)
    axis.grid(True, axis="y", which="both", alpha=0.25)
    axis.legend()
    for bars, language in ((bars_python, "Python"), (bars_java, "Java")):
        for bar, algorithm in zip(bars, ALGORITHMS):
            row = (python_rows if language == "Python" else java_rows)[(algorithm, 1000000)]
            label = f"{bar.get_height():,.1f}"
            if row["is_estimated"].lower() == "true":
                bar.set_hatch("//")
                label += " (est.)"
            axis.annotate(
                label,
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                rotation=90,
                fontsize=8,
            )
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.resolve()
    python_rows, python_omitted = measured_rows(
        read_rows(root / "results" / "python" / "search_measurements.csv"), "python"
    )
    java_rows, java_omitted = measured_rows(
        read_rows(root / "results" / "java" / "search_measurements.csv"), "java"
    )
    plot_dir = root / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plot_growth(python_rows, "Python", plot_dir / "search_growth_python.png")
    plot_growth(java_rows, "Java", plot_dir / "search_growth_java.png")
    plot_language_comparison(
        python_rows,
        java_rows,
        plot_dir / "search_language_comparison_1000000.png",
    )
    omitted = python_omitted + java_omitted
    print("Generated:")
    print(plot_dir / "search_growth_python.png")
    print(plot_dir / "search_growth_java.png")
    print(plot_dir / "search_language_comparison_1000000.png")
    print(f"omitted_no_medido_rows={len(omitted)}")
    if omitted:
        print("omitted_experiments=" + ", ".join(omitted))


if __name__ == "__main__":
    main()

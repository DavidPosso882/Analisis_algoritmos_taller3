"""Combine Java and Python measurement CSV files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def combine(paths: list[Path], output: Path) -> int:
    rows: list[dict[str, str]] = []
    fields: list[str] | None = None
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if fields is None:
                fields = reader.fieldnames
            elif reader.fieldnames != fields:
                raise ValueError(f"CSV schema mismatch: {path}")
            rows.extend(reader)
    if fields is None:
        raise ValueError("no input CSV files")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(f"wrote {combine(args.inputs, args.output)} rows to {args.output}")


if __name__ == "__main__":
    main()

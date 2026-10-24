"""Run the Point 2 search experiments without changing the input data."""

from __future__ import annotations

import argparse
import csv
import math
import time
from pathlib import Path
from statistics import mean, stdev
from typing import Callable, Sequence

from python.algorithms.binary_search import search as binary_search
from python.algorithms.exponential_search import search as exponential_search
from python.algorithms.interpolation_search import search as interpolation_search
from python.algorithms.jump_search import search as jump_search
from python.algorithms.linear_search import search as linear_search
from python.algorithms.ternary_search import search as ternary_search

Search = Callable[[Sequence[int], int], int]
ALGORITHMS: tuple[tuple[str, Search], ...] = (
    ("linear", linear_search),
    ("binary", binary_search),
    ("ternary", ternary_search),
    ("jump", jump_search),
    ("interpolation", interpolation_search),
    ("exponential", exponential_search),
)
SIZES = (1000, 10000, 100000, 1000000)
FIELDS = (
    "experiment_id", "algorithm", "language", "input_variant", "n",
    "experiment_type", "position", "key_set_id", "key_presence",
    "repetition_1_ns", "repetition_2_ns", "repetition_3_ns",
    "repetition_4_ns", "repetition_5_ns", "mean_ns", "stddev_ns",
    "status", "is_estimated", "estimate_method", "error_message",
    "repetitions", "searches_per_repetition", "warmup_iterations",
    "observations",
)


def load_array(root: Path, size: int) -> list[int]:
    path = root / "data" / f"asc_{size}.txt"
    values = [int(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if len(values) != size or any(left > right for left, right in zip(values, values[1:])):
        raise ValueError(f"invalid array data: {path}")
    return values


def load_keys(root: Path, size: int) -> list[tuple[int, str]]:
    path = root / "data" / "search_keys" / f"keys_{size}.txt"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 1000:
        raise ValueError(f"expected 1000 keys in {path}")
    keys = [(int(row["key"]), row["presence"]) for row in rows]
    if sum(presence == "PRESENTE" for _, presence in keys) != 500:
        raise ValueError(f"expected 500 present keys in {path}")
    if sum(presence == "AUSENTE" for _, presence in keys) != 500:
        raise ValueError(f"expected 500 absent keys in {path}")
    return keys


def validate_search(search: Search, values: Sequence[int], key: int, expected: bool) -> None:
    result = search(values, key)
    valid = result >= 0 and result < len(values) and values[result] == key
    if (result == -1) != (not expected) or (result != -1 and not valid):
        raise ValueError(f"invalid result for key {key}: {result}")


def sample_stddev_ns(times: Sequence[int], searches: int) -> float:
    per_search = [value / searches for value in times]
    return stdev(per_search) if len(per_search) > 1 else 0.0


def make_row(
    algorithm: str,
    size: int,
    experiment_type: str,
    position: str,
    key_set_id: str,
    key_presence: str,
    times: Sequence[int],
    searches: int,
    repetitions: int,
    status: str = "medido",
    observations: str = "",
) -> dict[str, object]:
    padded = list(times) + [""] * (5 - len(times))
    values = [value / searches for value in times]
    return {
        "experiment_id": f"{experiment_type}_{algorithm}_{size}_{position or key_set_id}",
        "algorithm": algorithm,
        "language": "python",
        "input_variant": f"asc_{size}",
        "n": size,
        "experiment_type": experiment_type,
        "position": position,
        "key_set_id": key_set_id,
        "key_presence": key_presence,
        "repetition_1_ns": padded[0],
        "repetition_2_ns": padded[1],
        "repetition_3_ns": padded[2],
        "repetition_4_ns": padded[3],
        "repetition_5_ns": padded[4],
        "mean_ns": mean(values) if values else "",
        "stddev_ns": sample_stddev_ns(times, searches) if values else "",
        "status": status,
        "is_estimated": "false",
        "estimate_method": "",
        "error_message": "",
        "repetitions": repetitions,
        "searches_per_repetition": searches,
        "warmup_iterations": 0,
        "observations": observations,
    }


def measure(
    root: Path,
    output: Path,
    sizes: Sequence[int] = SIZES,
    repetitions: int = 5,
    position_searches: int = 1000,
    timeout_seconds: float = 300.0,
    include_positions: bool = True,
) -> list[dict[str, object]]:
    loaded: dict[int, tuple[list[int], list[tuple[int, str]]]] = {
        size: (load_array(root, size), load_keys(root, size)) for size in sizes
    }
    rows: list[dict[str, object]] = []
    deadline = time.monotonic() + timeout_seconds
    for size, (values, keys) in loaded.items():
        expected = {key: presence == "PRESENTE" for key, presence in keys}
        for algorithm, search in ALGORITHMS:
            for key, _ in keys:
                validate_search(search, values, key, expected[key])
            times: list[int] = []
            timed_out = False
            for _ in range(repetitions):
                if time.monotonic() >= deadline:
                    timed_out = True
                    break
                start = time.perf_counter_ns()
                for key, _ in keys:
                    search(values, key)
                times.append(time.perf_counter_ns() - start)
            if timed_out:
                rows.append(make_row(algorithm, size, "all_keys", "", f"keys_{size}", "mixed", times, len(keys), repetitions, "no_medido", "timeout"))
                continue
            rows.append(make_row(algorithm, size, "all_keys", "", f"keys_{size}", "mixed", times, len(keys), repetitions))

    if include_positions and 1000000 in loaded:
        values, _ = loaded[1000000]
        for algorithm, search in ALGORITHMS:
            for position, index in (("start", 0), ("middle", len(values) // 2), ("end", len(values) - 1)):
                key = values[index]
                validate_search(search, values, key, True)
                times = []
                timed_out = False
                for _ in range(repetitions):
                    if time.monotonic() >= deadline:
                        timed_out = True
                        break
                    start = time.perf_counter_ns()
                    for _ in range(position_searches):
                        search(values, key)
                    times.append(time.perf_counter_ns() - start)
                status = "no_medido" if timed_out else "medido"
                observation = "timeout" if timed_out else ""
                rows.append(make_row(algorithm, 1000000, "position", position, "", "present", times, position_searches, repetitions, status, observation))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--sizes", default=",".join(map(str, SIZES)))
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--position-searches", type=int, default=1000)
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    parser.add_argument("--no-positions", action="store_true")
    args = parser.parse_args()
    output = args.output or args.root / "results" / "python" / "search_measurements.csv"
    rows = measure(args.root, output, tuple(int(size) for size in args.sizes.split(",")), args.repetitions, args.position_searches, args.timeout_seconds, not args.no_positions)
    print(f"wrote {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()

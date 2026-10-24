"""Genera datasets, semilla fija. Un entero de 8 digitos por linea."""

import random
from pathlib import Path
BASE = (Path(__file__).resolve().parent.parent.parent / "datos")
SEED = 42
N_MIN, N_MAX = 10_000_000, 99_999_999

for n in (1_000, 10_000, 100_000, 1_000_000):
    rng = random.Random(f"{SEED}-{n}")
    vals = [rng.randint(N_MIN, N_MAX) for _ in range(n)]
    (BASE / f"random_{n}.txt").write_text("\n".join(map(str, vals)) + "\n")
    asc = sorted(vals)
    (BASE / f"asc_{n}.txt").write_text("\n".join(map(str, asc)) + "\n")
    (BASE / f"desc_{n}.txt").write_text("\n".join(map(str, reversed(asc))) + "\n")
    print(f"n={n}: {len(vals)} aleatorios + asc + desc OK")

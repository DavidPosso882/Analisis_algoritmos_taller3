#!/usr/bin/env python3

"""Mide UNA celda (algo, variante, n)"""

import statistics, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.setrecursionlimit(1_000_000)
from bench_ordenamiento import ALGOS
BASE = (Path(__file__).resolve().parent.parent.parent / "datos")
import argparse, csv

ap = argparse.ArgumentParser()
ap.add_argument("algo"); ap.add_argument("variante"); ap.add_argument("n", type=int)
ap.add_argument("--timeout-rep", type=float, default=300.0)
ap.add_argument("--out", default="rows_new.csv")
a = ap.parse_args()
VARMAP = {"aleatoria":"random","asc":"asc","desc":"desc"}
prefix = VARMAP[a.variante]
data = list(map(int, (BASE/f"{prefix}_{a.n}.txt").read_text().split()))
fn = ALGOS[a.algo]
w = list(data); fn(w)
times = []

for i in range(5):
    arr = list(data)
    t0 = time.perf_counter_ns(); fn(arr); t1 = time.perf_counter_ns()
    dt = (t1-t0)/1e6
    if not all(arr[j]<=arr[j+1] for j in range(len(arr)-1)):
        print(f"[{a.algo} {a.variante} n={a.n}] FAIL verificacion rep{i+1}", flush=True)
        sys.exit(3)
    print(f"[{a.algo} {a.variante} n={a.n}] rep{i+1}={dt:.3f}ms", flush=True)
    if dt > a.timeout_rep*1000:
        print(f"ABORTAR: rep{i+1} {dt:.0f}ms supera {a.timeout_rep*1000:.0f}ms -> dejar estimado", flush=True)
        sys.exit(42)
    times.append(dt)
    
prom = statistics.fmean(times); desv = statistics.stdev(times) if len(times)>1 else 0.0
notas = "1 calentamiento no contado; 5 reps sobre copia fresca; orden verificado"
HEADER = ["algoritmo","lenguaje","variante","n","rep1_ms","rep2_ms","rep3_ms","rep4_ms","rep5_ms","promedio_ms","desv_std_ms","medido_o_estimado","notas"]
out = Path(a.out); new = not out.exists()

with open(out,"a",newline="") as f:
    wr = csv.writer(f)
    if new: wr.writerow(HEADER)
    wr.writerow([a.algo,"python",a.variante,a.n,*[f"{t:.3f}" for t in times],f"{prom:.3f}",f"{desv:.3f}","medido",notas])
print(f"OK [{a.algo} {a.variante} n={a.n}] prom={prom:.3f}ms desv={desv:.3f}ms", flush=True)

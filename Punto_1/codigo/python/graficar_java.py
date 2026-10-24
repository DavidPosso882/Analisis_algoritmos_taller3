"""Graficas Punto 1 Taller 3 (Java + Python): 2 crecimiento log-log + 3 efecto orden + 1 compilado vs interpretado."""
import csv, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = (Path(__file__).resolve().parent.parent.parent)
RES = BASE / "resultados"; GRAF = BASE / "graficas"

def load(fname):
    rows = []
    with open(RES / fname, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r["n"] = int(r["n"]); r["promedio_ms"] = float(r["promedio_ms"])
            r["medido_o_estimado"] = r["medido_o_estimado"].strip()
            rows.append(r)
    return rows

py_rows = load("python_resultados.csv")
jv_rows = load("java_resultados.csv")
ALGOS = ["insertion_sort", "dual_pivot_quicksort", "merge_sort", "heap_sort", "radix_sort", "bucket_sort"]
def norm(a):
    return {"insertion": "insertion_sort", "merge": "merge_sort", "heap": "heap_sort",
            "radix": "radix_sort", "bucket": "bucket_sort"}.get(a, a)
SHORT = {"insertion_sort": "Insertion", "dual_pivot_quicksort": "Dual-Pivot QS",
         "merge_sort": "Merge", "heap_sort": "Heap", "radix_sort": "Radix", "bucket_sort": "Bucket"}
COLORS = {"insertion_sort": "tab:red", "dual_pivot_quicksort": "tab:blue", "merge_sort": "tab:green",
          "heap_sort": "tab:orange", "radix_sort": "tab:purple", "bucket_sort": "tab:brown"}

def idx(rows, variante="aleatoria"):
    return {(norm(r["algoritmo"]), r["n"]): r for r in rows if r["variante"] == variante}

pyA, jvA = idx(py_rows), idx(jv_rows)
NS = [1000, 10000, 100000, 1000000]
print("FACTOR x10 (aleatoria)  algo | lang | 1K->10K | 10K->100K | 100K->1M")
for a in ALGOS:
    for lang, D in (("py", pyA), (("java", jvA))):
        facs = []
        for n0, n1 in zip(NS, NS[1:]):
            r0, r1 = D.get((a, n0)), D.get((a, n1))
            if r0 and r1 and r0["promedio_ms"] > 0:
                mark = "*" if (r0["medido_o_estimado"] != "medido" or r1["medido_o_estimado"] != "medido") else " "
                facs.append(f"{r1['promedio_ms']/r0['promedio_ms']:.1f}x{mark}")
            else: facs.append("s/d")
        print(f"{SHORT[a]} | {lang} | " + " | ".join(facs))

for lang, D, title in (("python", pyA, "Python (interpretado)"), ("java", jvA, "Java 21 (compilado, OpenJDK)")):
    fig, ax = plt.subplots(figsize=(9, 6))
    for a in ALGOS:
        xs = [n for n in NS if (a, n) in D]
        ys = [D[(a, n)]["promedio_ms"] for n in xs]
        for i in range(len(xs) - 1):
            est = D[(a, xs[i])]["medido_o_estimado"] != "medido" or D[(a, xs[i+1])]["medido_o_estimado"] != "medido"
            ax.loglog(xs[i:i+2], ys[i:i+2], color=COLORS[a], linestyle="--" if est else "-",
                      linewidth=2, marker="o" if not est else "x")
        ax.loglog([], [], color=COLORS[a], label=SHORT[a] + (" (punteado=estim.)" if any(D[(a, n)]["medido_o_estimado"] != "medido" for n in xs) else ""))
    ax.set_xlabel("n (elementos)"); ax.set_ylabel("tiempo (ms, log)")
    ax.set_title(f"Punto 1 — Crecimiento, entrada aleatoria — {title}")
    ax.legend(fontsize=8); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout(); fig.savefig(GRAF / f"01_crecimiento_{lang}.png", dpi=110); plt.close(fig)
    print(f"01_crecimiento_{lang}.png OK")

for n in (1000, 10000, 100000):
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(ALGOS)); w = 0.25
    for j, var in enumerate(("aleatoria", "ascendente", "descendente")):
        vals = []
        for a in ALGOS:
            r = next((r for r in jv_rows if norm(r["algoritmo"]) == a and r["variante"] == var and r["n"] == n), None)
            vals.append(r["promedio_ms"] if r else float("nan"))
        est = [next((r for r in jv_rows if norm(r["algoritmo"]) == a and r["variante"] == var and r["n"] == n), {}).get("medido_o_estimado") != "medido" for a in ALGOS]
        bars = ax.bar([i + (j - 1) * w for i in x], vals, width=w, label=var + (" (rayado=estim.)" if any(est) else ""))
        for b, v, h in zip(bars, vals, est):
            if h: b.set_hatch("///")
            if not math.isnan(v):
                ax.text(b.get_x() + b.get_width()/2, v, f"{v:.2f}" if v < 100 else f"{v:.0f}",
                        ha="center", va="bottom", fontsize=6, rotation=45)
    ax.set_xticks(list(x)); ax.set_xticklabels([SHORT[a] for a in ALGOS], rotation=15)
    ax.set_yscale("log"); ax.set_ylabel("tiempo (ms, log)")
    ax.set_title(f"Punto 1 — Efecto del orden de entrada (Java, n={n})")
    ax.legend(); ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(GRAF / f"02_orden_n{n}.png", dpi=110); plt.close(fig)
    print(f"02_orden_n{n}.png OK")

fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(ALGOS)); w = 0.35
for j, (D, lab) in enumerate(((pyA, "Python"), (jvA, "Java"))):
    vals, hatch = [], []
    for a in ALGOS:
        r = D.get((a, 1000000))
        vals.append(r["promedio_ms"] if r else float("nan"))
        hatch.append(r["medido_o_estimado"] != "medido" if r else False)
    vmax = max((v for v in vals if not math.isnan(v)), default=1)
    bars = ax.bar([i + (j - 0.5) * w for i in x], vals, width=w, label=lab)
    for b, v, h in zip(bars, vals, hatch):
        if h: b.set_hatch("///")
        if not math.isnan(v):
            if v == vmax:
                ax.text(b.get_x() + b.get_width()/2, v/4, f"{v:.0f}", ha="center", va="center", fontsize=7, rotation=90, color="white")
            else:
                ax.text(b.get_x() + b.get_width()/2, v, f"{v:.0f}", ha="center", va="bottom", fontsize=7, rotation=45)
ax.set_xticks(list(x)); ax.set_xticklabels([SHORT[a] for a in ALGOS], rotation=15)
ax.set_yscale("log"); ax.set_ylabel("tiempo (ms, log)")
ax.set_title("Punto 1 — Compilado (Java) vs interpretado (Python), n=1M aleatoria (rayado=estimado)")
ax.legend(); ax.grid(True, axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(GRAF / "03_compilado_vs_interpretado_1M.png", dpi=110); plt.close(fig)
print("03_compilado_vs_interpretado_1M.png OK")

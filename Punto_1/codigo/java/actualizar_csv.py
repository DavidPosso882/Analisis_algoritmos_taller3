from pathlib import Path
import statistics as st, csv

CSV = str((Path(__file__).resolve().parent.parent / "resultados" / "java_resultados.csv"))
STD = ("1 calentamiento no contado (JIT); 5 reps sobre copia fresca via "
       "Arrays.copyOf fuera del tiempo; solo el sort medido con System.nanoTime(); "
       "orden verificado fuera del tiempo")

def row(alg, var, n, reps, flag, nota):
    m = sum(reps) / len(reps)
    s = st.stdev(reps) if len(reps) > 1 else 0.0
    return [alg, "java", var, str(n)] + [f"{x:.3f}" for x in reps] + \
           [f"{m:.3f}", f"{s:.3f}", flag, nota]

# --- reemplazos: dual 100K estimado -> medido (-Xss512m) ---
repl = {
    ("dual_pivot_quicksort", "ascendente", "100000"):
        row("dual_pivot_quicksort", "ascendente", 100000,
            [1538.366, 1542.256, 1541.488, 2319.751, 3061.570],
            "medido", STD + "; pila ampliada -Xss512m (con pila por defecto: StackOverflowError)"),
    ("dual_pivot_quicksort", "descendente", "100000"):
        row("dual_pivot_quicksort", "descendente", 100000,
            [1691.334, 1761.262, 1770.390, 1743.318, 1700.614],
            "medido", STD + "; pila ampliada -Xss512m (con pila por defecto: StackOverflowError)"),
}

# --- filas nuevas medidas 1M ---
new_measured = [
    row("merge", "ascendente", 1000000, [33.827, 66.490, 34.149, 43.991, 32.928], "medido", STD),
    row("merge", "descendente", 1000000, [52.698, 64.744, 45.718, 47.304, 88.156], "medido", STD),
    row("heap", "ascendente", 1000000, [73.506, 81.863, 60.445, 64.046, 60.351], "medido", STD),
    row("heap", "descendente", 1000000, [86.526, 99.042, 78.671, 81.660, 77.510], "medido", STD),
    row("radix", "ascendente", 1000000, [52.352, 73.630, 53.551, 53.665, 49.134], "medido", STD),
    row("radix", "descendente", 1000000, [49.030, 56.728, 59.761, 50.473, 53.498], "medido", STD),
    row("bucket", "ascendente", 1000000, [130.613, 113.627, 80.908, 73.006, 89.244], "medido", STD),
    row("bucket", "descendente", 1000000, [733.246, 784.625, 794.099, 752.392, 774.395], "medido", STD),
    row("insertion", "ascendente", 1000000, [0.180, 3.096, 0.263, 0.283, 0.308], "medido", STD),
]

# --- filas nuevas estimadas (cierre por tiempo / regla 5 min/rep) ---
e = [169857.500] * 5
new_estimated = [
    row("insertion", "descendente", 1000000, e, "estimado",
        "NO ejecutado (cierre por tiempo; O(n^2): rep esperada ~170 s); "
        "estimado por extrapolacion cuadratica desde promedio medido "
        "descendente n=100000 (1698.575 ms) x100"),
    row("dual_pivot_quicksort", "ascendente", 1000000, [200068.600] * 5, "estimado",
        "NO medido: intento con -Xss1g abortado por regla 5 min/rep "
        "(host compartido degradado; sin StackOverflowError). Estimado por "
        "extrapolacion cuadratica O(n^2) desde promedio medido ascendente "
        "n=100000 con -Xss512m (2000.686 ms) x100"),
    row("dual_pivot_quicksort", "descendente", 1000000, [173338.400] * 5, "estimado",
        "NO ejecutado (cierre por tiempo tras abortar celda ascendente 1M por "
        "regla 5 min/rep). Estimado por extrapolacion cuadratica O(n^2) desde "
        "promedio medido descendente n=100000 con -Xss512m (1733.384 ms) x100"),
]

with open(CSV, newline="", encoding="utf-8") as f:
    lines = f.read().split("\n")
assert lines[0].startswith("algoritmo,lenguaje,"), "header inesperado"
assert lines[-1] == "", "se esperaba newline final"
body = [l for l in lines[1:] if l.strip()]
assert len(body) == 60, f"filas esperadas 60, hay {len(body)}"

out, nrepl = [], 0
for l in body:
    p = l.split(",")
    key = (p[0], p[2], p[3])
    if key in repl:
        out.append(",".join(repl[key])); nrepl += 1
    else:
        out.append(l)
assert nrepl == 2, f"reemplazos: {nrepl}"

for r in new_measured + new_estimated:
    assert len(r) == 13, f"columnas: {len(r)}"
    out.extend([",".join(r)])

with open(CSV, "w", newline="", encoding="utf-8") as f:
    f.write(lines[0] + "\n" + "\n".join(out) + "\n")
print(f"reemplazadas={nrepl} agregadas={len(new_measured)+len(new_estimated)} total_filas={len(out)}")

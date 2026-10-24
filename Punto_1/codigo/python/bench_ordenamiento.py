#!/usr/bin/env python3
"""Taller 3 Benchmark de 6 algoritmos de ordenamiento """

import argparse
import csv
import statistics
import sys
import time
from pathlib import Path

sys.setrecursionlimit(1_000_000)

BASE = (Path(__file__).resolve().parent.parent.parent / "datos")
DEFAULT_OUT = (Path(__file__).resolve().parent.parent.parent / "resultados" / "python_resultados.csv")

# ---------------------------------------------------------------- algoritmos ---
# 1. Insertion Sort


def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# 2. Dual-Pivot QuickSort


def partition(arr, low, high):
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    j = k = low + 1
    g, p, q = high - 1, arr[low], arr[high]
    while k <= g:
        if arr[k] < p:
            arr[k], arr[j] = arr[j], arr[k]
            j += 1
        elif arr[k] >= q:
            while arr[g] > q and k < g:
                g -= 1
            arr[k], arr[g] = arr[g], arr[k]
            g -= 1
            if arr[k] < p:
                arr[k], arr[j] = arr[j], arr[k]
                j += 1
        k += 1
    j -= 1
    g += 1
    arr[low], arr[j] = arr[j], arr[low]
    arr[high], arr[g] = arr[g], arr[high]
    return j, g


def dualPivotQuickSort(arr, low, high):
    if low < high:
        lp, rp = partition(arr, low, high)
        dualPivotQuickSort(arr, low, lp - 1)
        dualPivotQuickSort(arr, lp + 1, rp - 1)
        dualPivotQuickSort(arr, rp + 1, high)


# 3. Merge Sort


def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    L = [0] * n1
    R = [0] * n2
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]
    i = 0
    j = 0
    k = left
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def mergeSort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        mergeSort(arr, left, mid)
        mergeSort(arr, mid + 1, right)
        merge(arr, left, mid, right)


# 4. Heap Sort


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heapSort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)


# 5. Radix Sort base 10


def countingSort(arr, exp1):
    n = len(arr)
    output = [0] * (n)
    count = [0] * (10)
    for i in range(0, n):
        index = arr[i] // exp1
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]


def radixSort(arr):
    max1 = max(arr)
    exp = 1
    while max1 / exp >= 1:
        countingSort(arr, exp)
        exp *= 10


# 6. Bucket Sort ADAPTADO a enteros de 8 digitos


def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key


N_BUCKETS = 1000
BUCKET_LO = 10_000_000
BUCKET_SPAN = 90_000_000  # 99999999 - 10000000 + 1 ~ 9e7


def bucket_sort(arr):
    buckets = [[] for _ in range(N_BUCKETS)]
    for num in arr:
        bi = (num - BUCKET_LO) * N_BUCKETS // BUCKET_SPAN
        if bi >= N_BUCKETS:
            bi = N_BUCKETS - 1
        elif bi < 0:
            bi = 0
        buckets[bi].append(num)
    for bucket in buckets:
        insertion_sort(bucket)
    index = 0
    for bucket in buckets:
        for num in bucket:
            arr[index] = num
            index += 1


# Wrappers in-place sobre la lista completa
ALGOS = {
    "insertion_sort": insertionSort,
    "dual_pivot_quicksort": lambda a: dualPivotQuickSort(a, 0, len(a) - 1),
    "merge_sort": lambda a: mergeSort(a, 0, len(a) - 1),
    "heap_sort": heapSort,
    "radix_sort": radixSort,
    "bucket_sort": bucket_sort,
}

HEADER = ["algoritmo", "lenguaje", "variante", "n",
          "rep1_ms", "rep2_ms", "rep3_ms", "rep4_ms", "rep5_ms",
          "promedio_ms", "desv_std_ms", "medido_o_estimado", "notas"]

# ----------------------------------------------------------------------


def load_data(n):
    p = BASE / f"random_{n}.txt"
    return list(map(int, p.read_text().split()))


def is_sorted(a):
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def bench(fn, data, reps=5):
    """1 calentamiento no contado + reps sobre copia fresca. Retorna (tiempos_ms, ok)."""
    w = list(data)
    fn(w)  # calentamiento, no contado
    times = []
    for _ in range(reps):
        arr = list(data)  # copia fresca FUERA del tiempo
        t0 = time.perf_counter_ns()
        fn(arr)
        t1 = time.perf_counter_ns()
        times.append((t1 - t0) / 1e6)  # ns -> ms
        if not is_sorted(arr):  # verificacion FUERA del tiempo
            return times, False
    return times, True


def measure(algos, ns):
    rows = []
    for name in algos:
        fn = ALGOS[name]
        for n in ns:
            if name == "insertion_sort" and n >= 100_000:
                continue  # no ejecutar: O(n^2) tardaria horas
            data = load_data(n)  # lectura de disco ANTES de medir
            try:
                times, ok = bench(fn, data)
                notas = ("1 calentamiento no contado; 5 reps sobre copia fresca; "
                         "orden verificado" if ok else "FALLO verificacion de orden")
                status = "OK" if ok else "FAIL"
            except Exception as e:  # recursion, memoria, etc.
                times, ok, status = [], False, "FAIL"
                notas = f"ERROR durante medicion ({type(e).__name__}: {e}); ver estimado"
            if times:
                prom = statistics.fmean(times)
                desv = statistics.stdev(times) if len(times) > 1 else 0.0
                rep_cells = [f"{t:.3f}" for t in times]
            else:
                prom, desv, rep_cells = 0.0, 0.0, ["", "", "", "", ""]
            rows.append({
                "algoritmo": name, "lenguaje": "python", "variante": "aleatoria", "n": n,
                "reps": rep_cells, "promedio_ms": prom, "desv_std_ms": desv,
                "medido_o_estimado": "medido", "notas": notas, "verify": status,
            })
            print(f"[{name} n={n}] reps={rep_cells} prom={prom:.3f}ms verif={status}", flush=True)
    return rows


def append_estimates(rows, ref_prom_10k):
    """Filas ESTIMADAS para insertion_sort n=100000/1000000 por extrapolacion O(n^2)."""
    for n in (100_000, 1_000_000):
        est = ref_prom_10k * (n / 10_000) ** 2
        rep = f"{est:.3f}"
        rows.append({
            "algoritmo": "insertion_sort", "lenguaje": "python",
            "variante": "aleatoria", "n": n,
            "reps": [rep] * 5, "promedio_ms": est, "desv_std_ms": 0.0,
            "medido_o_estimado": "estimado",
            "notas": ("NO ejecutado (O(n^2) en Python tardaria horas); estimado por "
                      f"extrapolacion cuadratica desde promedio medido n=10000 "
                      f"({ref_prom_10k:.3f} ms)"),
            "verify": "ESTIMADO",
        })
        print(f"[insertion_sort n={n}] ESTIMADO prom={est:.3f}ms", flush=True)
    return rows


def write_partial(rows, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    new = not out_path.exists()
    with open(out_path, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(HEADER)
        for r in rows:
            w.writerow([r["algoritmo"], r["lenguaje"], r["variante"], r["n"],
                        *r["reps"], f"{r['promedio_ms']:.3f}",
                        f"{r['desv_std_ms']:.3f}", r["medido_o_estimado"], r["notas"]])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--algos", default=",".join(ALGOS),
                    help="subset separado por comas")
    ap.add_argument("--ns", default="1000,10000,100000,1000000")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--insertion-estimates", action="store_true",
                    help="solo agrega filas estimadas de insertion (lee ref n=10000 del CSV)")
    ap.add_argument("--ref10k", type=float, default=None,
                    help="promedio medido insertion n=10000 (ms) para la estimacion")
    args = ap.parse_args()

    if args.insertion_estimates:
        if args.ref10k is None:  # leer del CSV existente
            with open(args.out) as f:
                for row in csv.DictReader(f):
                    if (row["algoritmo"] == "insertion_sort" and row["n"] == "10000"
                            and row["medido_o_estimado"] == "medido"):
                        args.ref10k = float(row["promedio_ms"])
                        break
            if args.ref10k is None:
                sys.exit("No se encontro fila medida insertion n=10000 en " + args.out)
        rows = append_estimates([], args.ref10k)
        write_partial(rows, args.out)
        return

    algos = [a.strip() for a in args.algos.split(",") if a.strip() in ALGOS]
    ns = [int(x) for x in args.ns.split(",")]
    rows = measure(algos, ns)
    write_partial(rows, args.out)


if __name__ == "__main__":
    main()

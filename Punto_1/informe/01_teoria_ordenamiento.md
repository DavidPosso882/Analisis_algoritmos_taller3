# Punto 1 — Complejidad teórica y propiedades (6 algoritmos)

Fuente de implementaciones: GeeksforGeeks (misma lógica en Java y Python, código en `codigo/java` y `codigo/python`).
Lenguaje compilado: **Java 21 (OpenJDK)**. Lógica GeeksforGeeks 1:1.
Lenguaje interpretado: **Python**.

| Algoritmo | Mejor | Promedio | Peor | Estable | In-place | Notas |
|---|---|---|---|---|---|---|
| Insertion Sort | O(n) | O(n²) | O(n²) | Sí | Sí | Peor/descendente invierte todo; mejor/ascendente 1 pasada. |
| Dual-Pivot QuickSort (pivotes 1º y último) | O(n log n) | O(n log n) | O(n²) | No | Sí (pila O(log n) prom.) | Con pivotes fijos en extremos, asc/desc tiende al peor (particiones degeneradas). |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | Sí | No (O(n) extra) | Siempre divide igual; costo extra de mezcla. |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | No | Sí | Heapify O(log n) por extracción. |
| Radix Sort (base 10, d=8 dígitos fijos) | O(n) | O(n) | O(n) | Sí (counting estable) | No (arreglo salida + conteo) | Costo O(d·(n+10)); con d=8 constante → lineal en n. Si fueran 16 dígitos: 2× pasadas. |
| Bucket Sort (1000 cubetas FIJAS, insertion interno) | O(n+k) | O(n + n²/k)¹ | O(n²) | Sí² | No | ¹Con k=1000 fijo el promedio es cuadrático en n (cada cubeta recibe n/1000 elementos y el insertion interno cuesta O((n/k)²) por cubeta: total k·(n/k)² = n²/k). El O(n) de libro supone k≈n. ²Insertion interno estable + concatenación en orden. |

**Bucket — diseño (lo que pide el taller):** 1000 cubetas fijas (no n, para que escale a n=1M sin crear 1M de listas).
Asignación lineal por rango: `bi = (val − 10_000_000) × 1000 // 90_000_000`, con `val ∈ [10M, 99M]` → `bi ∈ [0, 999]`.
Cada cubeta se ordena con Insertion Sort y se concatenan en orden 0→999.
Si los valores se concentraran en un rango pequeño, casi todo caería en pocas cubetas y degradaría a O(n²) del insertion interno.

Fuentes por algoritmo (GeeksforGeeks):
- Insertion Sort — <https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/>
- Dual-Pivot QuickSort — <https://www.geeksforgeeks.org/dsa/dual-pivot-quicksort/> (pivotes primero/último)
- Merge Sort — <https://www.geeksforgeeks.org/dsa/merge-sort/>
- Heap Sort — <https://www.geeksforgeeks.org/dsa/heap-sort/>
- Radix Sort — <https://www.geeksforgeeks.org/dsa/radix-sort/> (base 10)
- Bucket Sort — <https://www.geeksforgeeks.org/dsa/bucket-sort-2/> (adaptado de floats a enteros con k=1000).
Referencias generales: GeeksforGeeks;
Cormen et al. *Introduction to Algorithms* (cotas, estabilidad, radix/bucket).

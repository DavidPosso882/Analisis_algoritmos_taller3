# Punto 1 — Análisis OFICIAL (ordenamiento, Java + Python, medición secuencial)

Datos oficiales: `resultados/java_resultados.csv` (71 medidos + 1 estimado) + `resultados/python_resultados.csv`
(68 + 4). El fallo de Dual-Pivot con entrada ordenada (`StackOverflowError` con pila por defecto)
quedó documentado en la columna `notas` del CSV y se midió con pila ampliada `-Xss512m`/`-Xss1g`.
Medición 100% secuencial (un bench a la vez, máquina idle), mismo protocolo en ambos lenguajes:
datos leídos antes de medir; solo el sort con `System.nanoTime()` / `perf_counter_ns`;
1 calentamiento no contado; 5 reps sobre copia fresca; verificación fuera del tiempo (OK en toda celda medida).
Gráficas: `graficas/01_crecimiento_{java,python}.png` (log-log, punteado=estimado),
`graficas/02_orden_n{1000,10000,100000}.png` (barras log en Java, rayado=estimado),
`graficas/03_compilado_vs_interpretado_1M.png` (barras log, rayado=estimado).

## Crecimiento (entrada aleatoria, factor ×10 de n)

| Algoritmo | Teoría ×10 | Java 1K→10K / 10K→100K / 100K→1M | Python 1K→10K / 10K→100K / 100K→1M |
|---|---|---|---|
| Insertion | ~100× (n²) | 8× / 49× / 102× | 105× / 126× / 100×* |
| Dual-Pivot QS | ~11–13× (n log n) | 4× / 14× / 8× | 13× / 15× / 17× |
| Merge | ~11–13× | 35× / 2× / 7× | 13× / 12× / 16× |
| Heap | ~11–13× | 4× / 12× / 10× | 14× / 16× / 17× |
| Radix (d=8) | ~10× (n) | 23× / 2× / 3× | 10× / 15× / 19× |
| Bucket (k=1000 fijo) | →100× (n+n²/k) | 5× / 10× / 21× | 5× / 45× / 83× |

(* = tramo con estimado.) Python lee de libro: Insertion ~100–126× (O(n²) con ambos
extremos medidos en 10K/100K: 1205 → 151627 ms), los n log n en 12–19×, Radix ~10–19×
(lineal con d fijo) y Bucket degradándose 45×/83×.
Java muestra el orden correcto en tramos grandes (insertion 102× con ambos extremos
medidos: 760 → 77733 ms; heap 10×; dual 8×) pero ruido JIT en tramos chicos con n=1K
(merge 35×, radix 23×, insertion 8×): una sola rep fría de <1 ms mueve el factor porque
el denominador es diminuto; el calentamiento único del protocolo no estabiliza todos
los caminos. Patrón medido: la primera rep tras el warmup sale 2–3× más lenta
(insertion 100K: 1563 vs ~560 ms; 1M: 155.6 vs ~58 s); el promedio la incluye y la
desviación la refleja — limitación declarada del protocolo de 1 warmup. No se
sobreinterpretan esos tramos: el orden se lee en 10K→100K→1M.
Bucket confirma la teoría corregida (promedio Θ(n+n²/k) con k fijo): 21× en Java y
83× en Python de 100K→1M, tendiendo a 100×. Con k≈n sería ~10× (tradeoff documentado).

Estimaciones oficiales (5, marcadas en CSV/tablas/gráficas, nunca silenciosas):
Java insertion-desc 1M y Python insertion-ale 1M (~4.2 h/rep), insertion-desc 1M
y dual asc/desc 1M. Todo lo demás (139/144 celdas) medido con verificación OK.
Caveat declarado: la extrapolación de insertion-desc-1M Java (147.9 s) subestima
frente a las reps reales (315/313/114 s, las dos primeras sobre el cap de 5 min);
se mantiene por regla pero con sesgo conocido a la baja.

## Efecto del orden de entrada (Java, n = 1K / 10K / 100K)

- **Insertion:** 100K: ascendente 0.16 ms (mejor O(n)) vs aleatoria 760 ms vs descendente
  1479 ms (peor O(n²)). El más sensible entre los que terminan siempre.
- **Dual-Pivot QS (pivotes 1º y último): el peor comportamiento, medido.**
  100K con `-Xss512m` (con pila por defecto: `StackOverflowError`):
  aleatoria 9.1 ms vs ascendente 1654 ms vs descendente 1596 ms (~180× más lento:
  partición degenerada, profundidad O(n)). A 1M, asc/desc MEDIDAS con `-Xss1g`
  (183.9/186.8 s; con pila por defecto desbordan). En Python, asc/desc 100K también
  medidas (~91.3/118.3 s, sin `RecursionError`).
  Causa: supone que los extremos no son representativos; la entrada ordenada lo rompe
  en cada nivel.
- **Merge** (16.4 / 15.9 / 9.1 ms), **Heap** (13.3 / 8.8 / 17.1 ms), **Radix**
  (21.6 / 17.2 / 5.9 ms) y **Bucket** (22.7 / 13.3 / 13.2 ms) a 100K: sin cambio de
  orden — como predice la teoría para los tres primeros; Bucket reparte igual con
  cualquier orden y solo varía el trabajo interno.
- Conclusión: el peor caso es **Dual-Pivot con entrada ordenada** (lento y además
  necesita pila ampliada), seguido por **Insertion en descendente**.

## Compilado vs interpretado (n = 1M, aleatoria)

| Algoritmo | Java (ms) | Python (ms) | Razón Py/Java |
|---|---|---|---|
| Insertion | 77733 | 15162732* | ~195×* |
| Dual-Pivot QS | 74.5 | 1591 | ~21× |
| Merge | 120 | 3516 | ~29× |
| Heap | 138 | 4978 | ~36× |
| Radix | 60.7 | 4478 | ~74× |
| Bucket | 481 | 12106 | ~25× |

Java gana por 1–2 órdenes: bytecode JIT con bucles ajustados y tipos primitivos
frente a CPython, donde cada operación paga tipado dinámico, despacho del intérprete
y GC. La brecha es mayor donde Python ejecuta más operaciones puras por elemento
(Radix ~74×: 8 pasadas de bucles Python) y menor donde el algoritmo hace menos
trabajo interpretado por elemento (Dual-Pivot ~21×). En Java hay empate técnico
entre Radix (60.7±8.7) y Dual-Pivot (74.5±8.6); en Python gana Dual-Pivot con holgura.
Bucket-Java (481 ms) carga `ArrayList<Integer>` con boxing por elemento, lo que
explica parte de su distancia a Radix (60.7 ms): medida de diseño, no del algoritmo.
El calentamiento previo (no contado) es condición del rendimiento Java; sin él, la
primera repetición saldría varias veces más lenta (visible en desviaciones como
insertion-ale 1M: 155.6s en frío vs 58s estabilizado).

Medición 100% secuencial (un bench a la vez, máquina idle); estimados solo por cap 5 min/rep
o pozo O(n²) (marcados en CSV, tablas y gráficas); Bucket k=1000 fijo con promedio
Θ(n+n²/k); Dual-Pivot con pivotes primero/último y `-Xss512m`/`-Xss1g` donde se indica
(1M ordenado: medido en Java con `-Xss1g`, estimado en Python por regla); detalle de fuentes y diseño en
`01_teoria_ordenamiento.md`.

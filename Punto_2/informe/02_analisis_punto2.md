# Punto 2 — Análisis (búsqueda, Java + Python)

Datos propios: `results/combined/search_measurements.csv` (84 filas: 48 de crecimiento + 36 de posición, 0 estimadas) + `results/combined/search_position_java.csv` + `results/combined/search_position_python.csv`, verificación de cordura en `results/combined/verification_small.csv`.
Protocolo (`docs/experimental_protocol.md`): arreglos ascendentes de `data/` (los del Punto 1); por cada n, 1 archivo de 1.000 claves (500 presentes + 500 ausentes, `data/search_keys/keys_{n}.txt`, orden idéntico en ambos lenguajes); se mide el bloque completo de 1.000 búsquedas y `mean_ns` es el promedio por búsqueda; 5 reps (Java con 2 calentamientos no contados, Python sin warmup); `perf_counter_ns()` / `System.nanoTime()`; verificación de pertenencia fuera del tiempo en toda celda medida.
Gráficas: `plots/search_growth_java.png`, `plots/search_growth_python.png` (log-log, una línea por algoritmo), `plots/search_language_comparison_1000000.png` (barras n = 1M), `plots/search_position_java.png`, `plots/search_position_python.png`.

## 1) Crecimiento (claves mixtas 500+500, factor ×10 de n)

Teoría ×10 esperada: lineal ~10× O(n); jump ~3.16× O(√n); binary/ternary/exponential ~1.1–1.3× O(log n); interpolation ~1.0–1.1× O(log log n).

| Algoritmo | Teoría ×10 | Python 1K→10K / 10K→100K / 100K→1M | Java 1K→10K / 10K→100K / 100K→1M |
|---|---|---|---|
| Linear | ~10× (n) | 10.9× / 10.0× / 10.1× | 5.5× / 8.5× / 14.8× |
| Jump | ~3.16× (√n) | 3.1× / 3.2× / 3.8× | 0.9× / 1.3× / 5.4× |
| Binary | ~1.1–1.3× (log n) | 1.5× / 1.4× / 1.3× | 0.6× / 0.8× / 2.0× |
| Ternary | ~1.1–1.3× (log n) | 1.5× / 1.6× / 1.2× | 0.9× / 0.6× / 9.7×* |
| Interpolation | ~1.0–1.1× (log log n) | 1.2× / 1.4× / 1.2× | 0.9× / 0.4× / 1.9× |
| Exponential | ~1.1–1.3× (log n) | 1.2× / 1.5× / 1.9× | 0.7× / 0.7× / 4.6× |

Python lee de libro en los 6 algoritmos: lineal 10.9/10.0/10.1× (60.3 µs → 655.4 µs → 6.55 ms → 66.14 ms por búsqueda), jump 3.1/3.2/3.8× contra 3.16× teórico, y los logarítmicos entre 1.2 y 1.9× por tramo.
Java no se interpreta como orden: sus celdas rápidas viven en el sub-microsegundo (binary-1M 0.45 µs, interpolation-1M 0.18 µs, ternary-100K 0.18 µs), donde el ruido del reloj y del JIT domina al factor — factores <1× (0.4–0.9×) son físicamente ruido, no mejora algorítmica.
CVs que lo confirman en `all_keys` n = 1M: ternary-Java 70.3% (media 1753.92 ns, std 1233.51 ns), binary-Java 41.6%; en Python el peor es interpolation 20.4%, resto ≤20%.
Outlier declarado: ternary-Java-1M salta 9.7× desde 100K (reps por búsqueda: 644.5, 3250.9, 2916.1, 1156.4, 801.7 ns) mientras ternary-Python crece 1.2× en el mismo tramo; es dispersión entre reps, no el orden del algoritmo.
Solo lineal y el último tramo de jump son legibles en Java (14.8× y 5.4×, por encima del ruido).

## 2) Efecto posición (n = 1M, 1.000× la misma clave, presente)

Java (ns por búsqueda):

| Algoritmo | Inicio | Centro | Final |
|---|---|---|---|
| Linear | 97.38 | 202547.20 | 486359.98 |
| Binary | 110.00 | 118.46 | 122.78 |
| Ternary | 116.86 | 133.66 | 143.76 |
| Jump | 80.12 | 1140.42 | 2670.90 |
| Interpolation | 106.82 | 95.96 | 84.80 |
| Exponential | 132.32 | 450.00 | 360.46 |

Python (µs por búsqueda):

| Algoritmo | Inicio | Centro | Final |
|---|---|---|---|
| Linear | 0.65 | 43600.14 | 76627.13 |
| Binary | 2.31 | 2.34 | 2.53 |
| Ternary | 2.91 | 2.93 | 3.04 |
| Jump | 0.38 | 53.04 | 166.24 |
| Interpolation | 0.30 | 1.26 | 0.38 |
| Exponential | 0.11 | 2.98 | 3.61 |

Mecanismo por algoritmo: **linear** es proporcional al índice — recorre desde 0 hasta la primera coincidencia (inicio O(1): 97 ns / 0.65 µs; final recorre ~1M: 486 µs / 76.6 ms).
**Binary/ternary** son planos (Java 110–144 ns, Python 2.3–3.0 µs): siempre hacen O(log n) comparaciones partiendo el intervalo, la posición solo decide en qué paso cae el acierto.
**Jump** escala con el nº de bloque: salta por bloques de √n y barre lineal dentro del bloque (inicio 80 ns / 0.38 µs → final 2.67 µs / 166.24 µs).
**Exponential** no acota el rango de entrada: duplica el límite hasta encerrar la clave y luego biseca (inicio inmediato 132 ns / 0.11 µs; centro/final uno–dos órdenes arriba).
**Interpolation** estima la posición por el valor bajo distribución uniforme, no por el índice: ~plana en Java (107/96/85 ns, todo en ruido sub-µs) y con el centro por encima en ambos lenguajes (Java 96 > 85, Python 1.26 > 0.38 µs); es la clave concreta —no la posición— la que fija el nº de sondas, así que middle > end es ruido/dependencia del valor, no tendencia posicional.

## 3) Compilado vs interpretado (n = 1M, claves mixtas, µs por búsqueda)

| Algoritmo | Java (µs) | Python (µs) | Razón Py/Java |
|---|---|---|---|
| Linear | 494.02 | 66136.91 | ~134× |
| Jump | 2.60 | 211.37 | ~81× |
| Interpolation | 0.18 | 4.45 | ~24× |
| Binary | 0.45 | 8.05 | ~18× |
| Exponential | 1.04 | 14.87 | ~14× |
| Ternary | 1.75 | 9.46 | ~5.4×* |

Java (bytecode JIT sobre `int[]` primitivo, tipos fijos, bucles compilados) gana por 1–2 órdenes frente a CPython, donde cada operación paga tipado dinámico y despacho del intérprete.
La brecha es mayor donde Python ejecuta más operaciones interpretadas por búsqueda (linear ~134×: bucle Python elemento a elemento; jump ~81×: saltos + barrido lineal en Python) y menor donde hay menos trabajo interpretado por búsqueda (binary ~18×, exponential ~14×, interpolation ~24×: aritmética y pocas iteraciones).
* Caveat ternary: el denominador Java-1M está inflado por el outlier ruidoso (CV 70.3%, §1); con una celda Java estable (~0.2–0.4 µs como en 100K) la razón real estaría en ~25–45×, en línea con binary. Se reporta 5.4× por fidelidad al CSV, sin interpretarlo como cercanía real entre lenguajes.

## Supuestos declarados

- Piso de resolución: el reloj es nanosegundos, pero las celdas Java sub-microsegundo están dominadas por ruido (factores <1× y CVs de hasta 70%); solo se lee orden en Python y en linear/jump-Java de tramo grande.
- `verification_small.csv` (12 filas, 1 rep por combinación, stddev 0) es chequeo de cordura, no medición oficial: con una rep no se estima dispersión.
- `experiment_id` está duplicado entre lenguajes por diseño (misma id para la fila Java y la Python); la clave única real es (`experiment_id`, `language`).
- 4 archivos de claves (uno por n) en vez del archivo único del enunciado: la intersección de presentes entre los cuatro arreglos es 0 (`docs/data_inventory.md`), así que ningún archivo único puede tener 500 presentes comunes; los ausentes sí se validaron por rechazo contra cada arreglo.
- 100% medido (`is_estimated=false` en las 84 filas, `status=medido`): las gráficas no muestran estilo de estimado (línea punteada / barra rayada) porque no hay qué marcar, aunque `python/experiments/plot_search_results.py` lo soporta.
- Warmup: Java 2 calentamientos no contados por combinación, Python 0 (`warmup_iterations` en el CSV); verificación de pertenencia siempre fuera del tiempo.

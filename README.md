# Análisis de Algoritmos — Taller 3 (Ordenamiento y Búsqueda)

Repo de entrega: Punto 1 (ordenamiento, Java 21 + Python) y Punto 2 (búsqueda, Java + Python).
Medición 100% secuencial, máquina idle. Todo medido salvo 5 celdas estimadas por regla 5 min/rep (marcadas en CSV y gráficas).

## Estructura

```text
Punto_1/
  codigo/python/  generar_datos.py, bench_ordenamiento.py, medir_celda.py, graficar_java.py
  codigo/java/    BenchOrdenamiento.java, run_java.sh, actualizar_csv.py
  datos/          random/asc/desc x {1000,10000,100000,1000000} (un entero por línea)
  resultados/     java_resultados.csv, python_resultados.csv (72 filas c/u)
  graficas/       6 PNG oficiales
  informe/        01_teoria_ordenamiento.md, 02_analisis_punto1.md
Punto_2/
  python/         algorithms/ (6), experiments/ (measure/combine/plot), generate_search_keys.py, tests/ (8)
  java/src/       6 búsquedas + ExperimentRunner.java
  java/tests/     6 tests
  data/           asc_*.txt + search_keys/keys_*.txt (500 presentes + 500 ausentes c/u)
  results/        combined/ + python/ + java/
  plots/          5 PNG
  docs/           protocolo, inventario, fuentes, notas
  informe/        02_analisis_punto2.md
```

`Punto_2/data/asc_*.txt` son los mismos del Punto 1 (ver SHA en `Punto_2/docs/data_inventory.md`).

## Reproducir Punto 1

```bash
# 1. Datos (semilla 42, 8 dígitos) — una sola vez
python3 Punto_1/codigo/python/generar_datos.py

# 2. Python (ejemplo una celda)
python3 Punto_1/codigo/python/bench_ordenamiento.py --algos merge --ns 10000

# 3. Java (una celda, máquina idle)
./Punto_1/codigo/java/run_java.sh merge aleatoria 10000
# Dual-Pivot ordenado n grande necesita pila ampliada:
./Punto_1/codigo/java/run_java.sh dual_pivot_quicksort ascendente 100000 5 512m

# 4. Gráficas
python3 Punto_1/codigo/python/graficar_java.py
```

Protocolo: datos leídos antes de medir, solo el sort con `System.nanoTime()` / `time.perf_counter_ns()`,
1 calentamiento no contado, 5 reps sobre copia fresca, verificación fuera del tiempo.

## Reproducir Punto 2

```bash
cd Punto_2

# 1. Claves (SplitMix64, semilla 0x5EED20261017A XOR n)
python3 python/generate_search_keys.py

# 2. Tests (57 tests)
python3 -m unittest discover -s python/tests -p "test_*.py"

# 3. Medición Python
python3 -m python.experiments.measure_search

# 4. Medición Java (requiere JDK)
javac -d /tmp/tb-java java/src/*.java
java -cp /tmp/tb-java ExperimentRunner --root=. --output=results/java/search_measurements.csv

# 5. Combinar + gráficas + tablas posición
python3 -m python.experiments.combine_results results/python/search_measurements.csv results/java/search_measurements.csv --output results/combined/search_measurements.csv
python3 -m python.experiments.plot_search_results
python3 -m python.experiments.generate_position_tables
python3 -m python.experiments.plot_position_results
```

Protocolo: arreglos `data/asc_*.txt` cargados antes de medir, se mide el bloque de 1000 búsquedas
(500 presentes + 500 ausentes) y `mean_ns` es el promedio por búsqueda; 5 reps;
Java con 2 warmups no contados; verificación fuera del tiempo.

## Resultados oficiales

* Punto 1: `Punto_1/resultados/*.csv` (Java 71+1, Python 68+4 → 139/144 medidas, 5 estimadas).
  Estimado = extrapolación cuadrática desde 100K medido, columna `medido_o_estimado=estimado`.
  Fallo documentado: `StackOverflowError` de Dual-Pivot ordenado con pila por defecto
  (medido con `-Xss512m`/`-Xss1g`, ver notas del CSV).
* Punto 2: `Punto_2/results/combined/search_measurements.csv` (84 filas, 0 estimadas) +
  `search_position_*.csv`. 4 archivos de claves porque la intersección de presentes es 0
  (ver `docs/data_inventory.md`); archivo único inviable.

# Protocolo experimental

## Entradas

Se usaron directamente los cuatro arreglos ascendentes de `data/`:

`data/asc_1000.txt`, `data/asc_10000.txt`, `data/asc_100000.txt` y
`data/asc_1000000.txt`.

Cada archivo se cargó antes de iniciar el cronómetro.

### Viabilidad de un único archivo

El enunciado exige una sola colección de 1.000 claves que tenga 500 presentes
y 500 ausentes **en cada uno** de los cuatro arreglos. Esta condición requiere
al menos 500 valores en la intersección de los cuatro conjuntos de valores
distintos. El análisis real de los archivos mostró:

| Métrica | Resultado |
|---|---:|
| Valores distintos en `asc_1000.txt` | 1.000 |
| Valores distintos en `asc_10000.txt` | 9.998 |
| Valores distintos en `asc_100000.txt` | 99.954 |
| Valores distintos en `asc_1000000.txt` | 994.400 |
| Valores distintos comunes a los cuatro arreglos | 0 |
| Valores distintos presentes en la unión | 1.104.176 |
| Enteros de ocho dígitos ausentes en los cuatro | 88.895.824 |

Por tanto, el archivo único **no es viable**: no existe siquiera una clave
presente en los cuatro arreglos, mucho menos 500. La condición de 500 ausentes
sí es viable, pero no compensa la intersección vacía.

La alternativa adoptada es usar cuatro archivos independientes, uno por
arreglo, cada uno con 500 presentes y 500 ausentes. El procedimiento
reproducible usa SplitMix64 con semilla base `0x5EED20261017A`. Para cada
tamaño `n`, la semilla efectiva es `BASE_SEED XOR n`; así cada tamaño tiene un
flujo determinista distinto. Se seleccionan valores presentes distintos por
muestreo sin reemplazo y valores ausentes por rechazo contra el conjunto
completo del arreglo.

El generador está en `python/generate_search_keys.py` y se ejecuta con:

```text
python python/generate_search_keys.py
```

Los archivos son UTF-8 delimitado por tabuladores, con cabecera
`key_id`, `key`, `presence` y `n`. Las filas `P001`--`P500` son `PRESENTE`;
`A001`--`A500` son `AUSENTE`. Se validan dominio, pertenencia, unicidad y
cantidades. Los destinos existentes se rechazan y la escritura usa temporales.

El experimento de posición usó tres valores presentes del arreglo de
1.000.000 elementos: `arr[0]` (inicio), `arr[n // 2]` (centro) y `arr[n - 1]`
(final). La selección se hizo por índice del arreglo y se registró también
el valor. Si hay repeticiones, la posición nominal identifica el elemento
seleccionado, pero la función de búsqueda solo debe devolver un índice válido
que contenga la clave, o `-1`; no se exige que todos los algoritmos devuelvan
el mismo índice ni que devuelvan la ocurrencia nominal.

## Medición principal (lo medido)

- Se cargaron todos los datos antes de medir.
- Se midió únicamente las llamadas de búsqueda.
- Se ejecutaron cinco repeticiones independientes.
- En cada repetición, se buscaron las 1.000 claves.
- Se registró el tiempo total de cada repetición en nanosegundos.
- Se calculó el promedio por búsqueda como `tiempo_total / 1000`.
- Se calcularon el promedio y la desviación estándar a partir de los cinco tiempos
  totales de la repetición completa; al exportar, se normalizaron ambos a
  nanosegundos por búsqueda y se documentó el denominador usado.
- Se usó `time.perf_counter_ns()` en Python.
- Se usó `System.nanoTime()` en Java.
- Se ejecutó un calentamiento en Java antes de registrar las cinco repeticiones
  oficiales.
- Se validaron los resultados de búsqueda fuera del intervalo cronometrado.
- Se excluyeron carga de archivos, impresión, exportación CSV y generación de
  gráficas.
- La búsqueda lineal fue la referencia de comparación.
- El orden de las 1.000 claves fue idéntico para ambos lenguajes.
- Los resultados de pertenencia se comprobaron después de cada repetición,
  fuera del intervalo cronometrado.

## Medición por posición (lo medido)

Para cada algoritmo y lenguaje se repitió 1.000 veces la búsqueda de cada
clave del inicio, centro y final del arreglo de 1.000.000 elementos. Se
registró la posición (`start`, `middle` o `end`) y el índice nominal como
parte de la identificación del experimento. La carga, validación, impresión y
exportación quedaron fuera del tiempo. Se midieron cinco repeticiones del bloque
de 1.000 búsquedas de una sola clave; `mean_ns` es el promedio de una
búsqueda dentro de ese bloque.

## Esquema CSV (lo guardado)

Los CSV propios se guardaron en `results/python/` y `results/java/`; el
resultado combinado se guardó en `results/combined/`. Cada fila
incluye:

```text
experiment_id,algorithm,language,input_variant,n,
repetition_1_ns,repetition_2_ns,repetition_3_ns,repetition_4_ns,
repetition_5_ns,mean_ns,stddev_ns,status,is_estimated,estimate_method,
error_message
```

También se añadirán, cuando corresponda, `experiment_type` (`all_keys` o
`position`), `position` (`start`, `middle`, `end` o vacío), `key_set_id`,
`key_presence` (`present`, `absent` o `mixed`), `repetitions`,
`searches_per_repetition` y `warmup_iterations`. `n` identifica el tamaño del
arreglo.

`mean_ns` es el promedio por búsqueda en nanosegundos: para `all_keys`, la
suma de las 1.000 búsquedas dividida entre 1.000; para `position`, el tiempo
del bloque de 1.000 repeticiones dividido entre 1.000. `stddev_ns` es la
desviación estándar muestral de esos cinco tiempos totales, expresada también
por búsqueda después de dividir cada repetición entre 1.000. Así se evita
mezclar la dispersión entre repeticiones con la variación interna de una
búsqueda. Las filas estimadas se marcan con `is_estimated=true` y
explican `estimate_method`; nunca se presentan como mediciones reales. En esta
entrega las 84 filas son medidas (`is_estimated=false`).

Los errores de lectura, validación o ejecución se registraron en
`error_message` y `status`; una fila con error no se convirtió en cero ni se
incluyó silenciosamente en estadísticas. `is_estimated=false` distingue
las mediciones cronometradas reales.

## Ejecutores usados

Los ejecutores reutilizaron las doce funciones de búsqueda. Cargaron y
validaron arreglos y claves antes de cronometrar, validaron cada resultado fuera de
la sección medida y escribieron el CSV después de completar las repeticiones.
Python usó `time.perf_counter_ns()` y Java usó `System.nanoTime()`. El
calentamiento Java se ejecutó antes de cada combinación y no se registró.

La ejecución completa usada fue (desde la raíz de `Punto_2`):

```powershell
py -m python.experiments.measure_search
$javaOut = (Join-Path (Get-Location) "results\java\search_measurements.csv")
$tmp = Join-Path $env:TEMP "taller-busqueda-measure-java"
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
javac -d $tmp java\src\*.java
java -cp $tmp ExperimentRunner --root=(Get-Location).Path --output=$javaOut
Remove-Item -Recurse -Force $tmp
py -m python.experiments.combine_results `
  results\python\search_measurements.csv `
  results\java\search_measurements.csv `
  --output results\combined\search_measurements.csv
```

La verificación pequeña, que mide solo el arreglo de 1.000 elementos y una
repetición por combinación, se ejecuta con:

```powershell
py -m python.experiments.measure_search `
  --sizes 1000 --repetitions 1 --no-positions `
  --timeout-seconds 60 `
  --output results\python\verification_small.csv

$tmp = Join-Path $env:TEMP "taller-busqueda-measure-java"
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
javac -d $tmp java\src\*.java
java -cp $tmp ExperimentRunner `
  --root=(Get-Location).Path `
  --output=(Join-Path (Get-Location) "results\java\verification_small.csv") `
  --sizes=1000 --repetitions=1 --no-positions --timeout-seconds=60
Remove-Item -Recurse -Force $tmp

py -m python.experiments.combine_results `
  results\python\verification_small.csv `
  results\java\verification_small.csv `
  --output results\combined\verification_small.csv
```

`--timeout-seconds` tiene un límite predeterminado de 300 segundos. Si se
alcanza entre repeticiones, la combinación se registra como `no_medido` con
`observations=timeout`; no se presenta como estimación y no se generan datos
artificiales. La desviación estándar es muestral:
`sqrt(sum((t_i - mean)^2) / (r - 1))`, donde cada `t_i` es el tiempo total de
una repetición dividido entre el número de búsquedas de esa repetición. Con
una sola repetición se registra desviación cero, porque no es posible estimar
dispersión muestral.

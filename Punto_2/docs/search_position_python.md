# Experimento de posición de la clave — Python

Arreglo: `n = 1.000.000` elementos. Tiempos: promedio por búsqueda individual, en nanosegundos (`ns`), calculado a partir de 1.000 búsquedas por repetición y cinco repeticiones.

| Algoritmo | Inicio | Centro | Final |
| --- | --- | --- | --- |
| linear | 649.66 | 43600136.72 | 76627125.26 |
| binary | 2310.66 | 2341.84 | 2528.7 |
| ternary | 2905.32 | 2932.44 | 3041.06 |
| jump | 382.14 | 53035.74 | 166239.72 |
| interpolation | 300.9 | 1264.74 | 382.5 |
| exponential | 108.66 | 2975.96 | 3605.88 |

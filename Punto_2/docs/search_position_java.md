# Experimento de posición de la clave — Java

Arreglo: `n = 1.000.000` elementos. Tiempos: promedio por búsqueda individual, en nanosegundos (`ns`), calculado a partir de 1.000 búsquedas por repetición y cinco repeticiones.

| Algoritmo | Inicio | Centro | Final |
| --- | --- | --- | --- |
| linear | 97.38 | 202547.2 | 486359.98 |
| binary | 110.0 | 118.46 | 122.78 |
| ternary | 116.85999999999999 | 133.66 | 143.76 |
| jump | 80.12 | 1140.42 | 2670.9 |
| interpolation | 106.82000000000002 | 95.96000000000001 | 84.8 |
| exponential | 132.32 | 450.0 | 360.46 |

# Inventario de datos

## Archivos localizados

| Archivo | Ubicación | Elementos esperados | Elementos validados | Formato |
|---|---|---:|---:|---|
| `data/asc_1000.txt` | `data/` | 1.000 | 1.000 | entero por línea |
| `data/asc_10000.txt` | `data/` | 10.000 | 10.000 | entero por línea |
| `data/asc_100000.txt` | `data/` | 100.000 | 100.000 | entero por línea |
| `data/asc_1000000.txt` | `data/` | 1.000.000 | 1.000.000 | entero por línea |

La validación se realizó mediante lectura secuencial antes y después del
movimiento. Todos los archivos
contienen únicamente líneas numéricas válidas y están ordenados de forma no
decreciente. `asc_10000.txt`, `asc_100000.txt` y `asc_1000000.txt` contienen
valores repetidos; por tanto, la propiedad comprobada es orden no decreciente,
no estrictamente creciente.

Los siguientes hashes SHA-256 se registran como baseline de integridad de los
arreglos, calculados sobre el contenido exacto de cada archivo:

| Archivo | SHA-256 |
|---|---|
| `data/asc_1000.txt` | `e670aa8d966f833d0fbadb545202b3bab2f3c8503adc085bc048c58ac0c93a5b` |
| `data/asc_10000.txt` | `38052c47b2985c0de9f8d57d0317af285deca8f5d1d41281c1397fc55cc7269f` |
| `data/asc_100000.txt` | `080a2fc50e45ee3393a88bc81b0ab400380f6306fa55acbf104c7c66cbc5d279` |
| `data/asc_1000000.txt` | `0efeeb53135ec7be8b962dd51c3a0865d23c4e82530ecf374eb6bf9b147e6c7d` |

| Archivo | Valores distintos validados | Mínimo | Máximo |
|---|---:|---:|---:|
| `data/asc_1000.txt` | 1.000 | 10.006.495 | 99.936.697 |
| `data/asc_10000.txt` | 9.998 | 10.001.715 | 99.993.822 |
| `data/asc_100000.txt` | 99.954 | 10.000.019 | 99.999.108 |
| `data/asc_1000000.txt` | 994.400 | 10.000.021 | 99.999.919 |

Estos conteos permitieron seleccionar 500 valores presentes distintos en cada
arreglo. La generación de ausentes aplicó rechazo contra el conjunto
completo de valores, no solo contra los valores distintos seleccionados como
presentes.

## Análisis de viabilidad del archivo único

Se calcularon los conjuntos de valores distintos de los cuatro archivos. La
intersección de los cuatro conjuntos tiene **0 valores**. La unión contiene
1.104.176 valores distintos. Considerando el dominio de enteros de ocho
dígitos, `[10.000.000, 99.999.999]`, hay 88.895.824 valores ausentes en los
cuatro arreglos.

En consecuencia, sí existen suficientes claves ausentes comunes, pero no
existe ninguna clave presente común. No es posible construir un único archivo
de 1.000 claves con 500 presentes y 500 ausentes para cada arreglo.

## Claves de búsqueda (lo generado)

La condición de una única colección común no es viable, por lo que se usan
cuatro archivos, uno por tamaño:
`data/search_keys/keys_1000.txt`, `keys_10000.txt`, `keys_100000.txt` y
`keys_1000000.txt`. Cada archivo contiene exactamente 1.000 filas de datos:
500 claves que pertenecen al arreglo correspondiente y 500 que no pertenecen.
El formato es UTF-8 tabulado con cabecera `key_id`, `key`, `presence` y `n`.
`n` identifica el tamaño del arreglo, no es una quinta clave.

Las claves son generadas por `python/generate_search_keys.py` con SplitMix64.
La semilla efectiva es `0x5EED20261017A XOR n`; las ausentes se validan contra
todos los valores del arreglo, incluidos los repetidos.

Los hashes SHA-256 observados de las colecciones de claves quedan registrados
para detectar modificaciones posteriores:

| Archivo | SHA-256 |
|---|---|
| `data/search_keys/keys_1000.txt` | `ec9b0260a5f1af531a48b370fbe4187f465b41c836f7eb11b56a698d5a24cac3` |
| `data/search_keys/keys_10000.txt` | `8d576597e59f6d302cfc1cd37366e698758eb11bc6cb5326b4573d1f5e1c2bcb` |
| `data/search_keys/keys_100000.txt` | `cc9fe071fef96fb99eeb126646fb4cedf90bd48db7e7069f37a3f952e1dae006` |
| `data/search_keys/keys_1000000.txt` | `2e9beff0db191aadb3346aae1e89e91844b4338cff2253491d9209a5f0b6ce85` |

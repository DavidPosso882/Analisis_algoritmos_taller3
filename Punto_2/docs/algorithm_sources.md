# Fuentes de los algoritmos

Las siguientes páginas oficiales de GeeksforGeeks fueron consultadas el
17-10-2026. Todos los algoritmos listados cuentan con adaptaciones Python y
Java, excepto donde se indique lo contrario.

| Algoritmo | Título verificado | URL verificada | Lenguajes de referencia observados | Fecha de consulta | Código/adaptación del taller |
|---|---|---|---|---|---|
| Búsqueda lineal | Linear Search | https://www.geeksforgeeks.org/dsa/linear-search/ | Java y Python, entre otros | 2026-10-17 | Python: `python/algorithms/linear_search.py`; Java: `java/src/LinearSearch.java`; primer índice coincidente o `-1` |
| Búsqueda binaria | Binary Search | https://www.geeksforgeeks.org/dsa/binary-search/ | Java y Python, entre otros | 2026-10-17 | Python: `python/algorithms/binary_search.py`; Java: `java/src/BinarySearch.java`; índice coincidente o `-1` |
| Búsqueda ternaria | Ternary Search | https://www.geeksforgeeks.org/dsa/ternary-search/ | Java y Python, entre otros | 2026-10-17 | Python: `python/algorithms/ternary_search.py`; Java: `java/src/TernarySearch.java`; índice coincidente o `-1` |
| Búsqueda por saltos | Jump Search | https://www.geeksforgeeks.org/dsa/jump-search/ | Java y Python, entre otros | 2026-10-17 | `python/algorithms/jump_search.py`; `java/src/JumpSearch.java`; índice coincidente o `-1` |
| Búsqueda por interpolación | Interpolation Search | https://www.geeksforgeeks.org/dsa/interpolation-search/ | Java y Python, entre otros | 2026-10-17 | `python/algorithms/interpolation_search.py`; `java/src/InterpolationSearch.java`; índice coincidente o `-1` |
| Búsqueda exponencial | Exponential Search | https://www.geeksforgeeks.org/dsa/exponential-search/ | Java y Python, entre otros | 2026-10-17 | `python/algorithms/exponential_search.py`; `java/src/ExponentialSearch.java`; índice coincidente o `-1` |

La búsqueda lineal adaptada conserva el recorrido secuencial de izquierda a
derecha del código de referencia y devuelve el primer índice coincidente o
`-1`. No requiere que el arreglo esté ordenado y no modifica la entrada. La
adaptación está en `python/algorithms/linear_search.py` y
`java/src/LinearSearch.java`; la lectura de datos, impresión y medición
permanecen fuera de la función. Ambas versiones recorren desde el índice cero
y retornan la primera coincidencia.

La búsqueda binaria adaptada conserva el algoritmo iterativo del código de
referencia: mantiene los límites inclusivos `low` y `high`, calcula el punto
medio sin sumar directamente ambos límites y descarta la mitad que no puede
contener la clave. Requiere una entrada ordenada en orden no decreciente,
devuelve un índice válido de una ocurrencia cuando hay duplicados y `-1` si no
encuentra la clave. Está implementada en
`python/algorithms/binary_search.py`.

La versión Java de la búsqueda binaria está en `java/src/BinarySearch.java`.
Mantiene el mismo contrato que Python: entrada ordenada en orden no
decreciente, índice válido de una coincidencia o `-1`, sin modificar el
arreglo. La implementación es iterativa y conserva la fórmula de punto medio
`low + (high - low) / 2`.

La búsqueda ternaria adaptada conserva el algoritmo iterativo del código de
referencia: mantiene límites inclusivos, divide el intervalo en tres partes
mediante `mid1` y `mid2`, compara ambos puntos y descarta la región imposible.
Requiere una entrada ordenada en orden no decreciente, devuelve un índice
válido de una ocurrencia si hay duplicados y `-1` si la clave no aparece. Está
implementada en `python/algorithms/ternary_search.py`.

La versión Java de la búsqueda ternaria está en
`java/src/TernarySearch.java`. Mantiene los límites inclusivos, los dos puntos
medios y los tres descartes de la versión Python. Devuelve un índice válido de
una coincidencia o `-1`, sin modificar el arreglo.

Jump Search conserva el algoritmo iterativo de la referencia: calcula un
tamaño de bloque cercano a `sqrt(n)`, avanza por bloques hasta encontrar el
primero que puede contener la clave y realiza un recorrido lineal dentro de
ese bloque. La adaptación requiere una entrada ordenada, devuelve un índice
válido cuando hay duplicados y `-1` cuando no encuentra la clave. La versión
Python usa `isqrt`; la versión Java usa `Math.sqrt` y ambas garantizan un
tamaño de bloque mínimo de uno. La guarda para arreglos vacíos y el límite
`min(step, n)` evitan accesos fuera del arreglo. No se modifican el arreglo ni
la clave, y la lectura de archivos, impresión y medición quedan fuera del
algoritmo. Está implementada en `python/algorithms/jump_search.py` y
`java/src/JumpSearch.java`.

La adaptación Java conserva la estructura del código de referencia: `previous`
marca el inicio del bloque candidato, `step` su límite superior y el recorrido
lineal se detiene al alcanzar ese límite o al encontrar la clave. Se añade la
guarda explícita para `n == 0`, necesaria porque el código original accede al
último elemento del primer bloque sin tratar arreglos vacíos. Para una entrada
ordenada de longitud `n`, el mejor caso es `O(1)` cuando la primera comparación
encuentra la clave; bajo una posición de éxito distribuida o ausencias, el caso
promedio es `O(sqrt(n))`, y el peor caso también es `O(sqrt(n))`. El espacio
adicional es `O(1)`.

La búsqueda por interpolación conserva la estimación de posición basada en los
valores extremos y el descarte iterativo de la región imposible. La adaptación
usa la forma aritmética `low + ((high - low) * (x - arr[low])) // (arr[high] -
arr[low])`, que evita truncar prematuramente el producto. También trata
explícitamente el caso de extremos iguales para evitar división por cero con
duplicados. Está implementada en
`python/algorithms/interpolation_search.py` y
`java/src/InterpolationSearch.java`.

La versión Java conserva la firma simplificada del taller, `search(int[] arr,
int x)`, en lugar de exponer los límites `lo` y `hi` del código original.
Mantiene el algoritmo iterativo equivalente a la versión Python. Usa
aritmética `long` únicamente para el producto y las diferencias de la fórmula
de interpolación, evitando desbordamiento de `int` sin reemplazar el cálculo
proporcional. Para una entrada ordenada de longitud `n`, el mejor caso es
`O(1)` cuando la estimación acierta; bajo distribución aproximadamente
uniforme, el promedio es `O(log log n)`; el peor caso es `O(n)` con
distribución desigual o estimaciones desfavorables. El espacio adicional es
`O(1)`. La hipótesis de distribución uniforme es analítica y no una garantía
para los datos del taller.

La búsqueda exponencial adaptada conserva la expansión por duplicación de la
referencia y la búsqueda binaria sobre el intervalo descubierto. Comprueba
primero el índice cero, devuelve un índice válido o `-1`, y usa límites
acotados para el último intervalo. La versión Python usa una búsqueda binaria
iterativa auxiliar; la versión Java conserva esa lógica sin usar
`Arrays.binarySearch`. Ambas aceptan cualquier índice válido cuando hay
duplicados y no modifican la entrada. Están implementadas en
`python/algorithms/exponential_search.py` y
`java/src/ExponentialSearch.java`.

La adaptación Java expone `search(int[] arr, int x)` en lugar de recibir
explícitamente `n`, porque la longitud se obtiene del arreglo. También trata
el arreglo vacío antes de acceder a `arr[0]`. La expansión duplica el límite
hasta encontrar un intervalo candidato y la búsqueda binaria usa límites
inclusivos. Para una posición objetivo `i`, la expansión requiere `O(log i)` y
la búsqueda binaria `O(log i)`, por lo que el mejor caso es `O(1)` y el caso
promedio y el peor caso son `O(log n)`. El espacio adicional es `O(1)`.

La consulta confirmó que las búsquedas binaria, ternaria, por saltos, por
interpolación y exponencial presuponen arreglos ordenados. La página de
interpolación también describe el supuesto de distribución uniforme; esto se
registrará como una característica de los datos, no como una garantía de
rendimiento.

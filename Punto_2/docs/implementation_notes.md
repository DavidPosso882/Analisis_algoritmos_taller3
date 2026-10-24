# Notas de implementación

## Contrato común

Java y Python recibirán el mismo arreglo y la misma clave, y devolverán
resultados equivalentes para indicar si la clave fue encontrada. Las búsquedas
que requieren ordenamiento trabajarán con los arreglos ascendentes entregados.
La lectura de datos y la validación de resultados estarán separadas de la
sección cronometrada.

## Datos compartidos

Los archivos `data/asc_*.txt` son los arreglos originales. No deben
alterarse ni regenerarse sin autorización. El análisis de viabilidad demostró
que no existe ningún valor presente en los cuatro arreglos, por lo que no
puede existir un único archivo con 500 claves presentes para cada tamaño.
Java y Python leerán exactamente los mismos archivos de claves generados por
`python/generate_search_keys.py`; ninguna implementación debe generar un
conjunto independiente.

## Generador de claves

El generador usa únicamente la biblioteca estándar de Python. Lee cada arreglo
desde `data/`, comprueba que tenga el tamaño esperado, que sus enteros estén en
`[10.000.000, 99.999.999]` y que estén ordenados. Para cada `n`, deriva la
semilla `0x5EED20261017A XOR n` y usa SplitMix64 con selección acotada sin
sesgo. Produce 500 valores distintos presentes y 500 ausentes, rechazando
ausentes que estén en el conjunto completo del arreglo.

El archivo tabulado tiene la forma:

```text
key_id	key	presence	n
P001	12345678	PRESENTE	1000
A001	87654321	AUSENTE	1000
```

No se sobrescriben destinos existentes. Las validaciones y pruebas se ejecutan
con `python -m unittest discover -s python/tests -p "test_*.py"`.

## Búsqueda lineal

La adaptación Python está en `python/algorithms/linear_search.py`. Recibe una
secuencia de enteros y una clave, recorre los elementos desde el índice `0`
hasta el final y retorna inmediatamente el primer índice cuyo valor coincide.
Si termina el recorrido sin encontrar la clave, retorna `-1`. No lee archivos,
imprime resultados, ordena la entrada ni usa una función de biblioteca que
reemplace el recorrido.

La equivalencia en Java es un bucle sobre el arreglo con el mismo
orden, condición de igualdad y valores de retorno. Para un arreglo de longitud
`n`, el mejor caso es `O(1)` cuando la clave está en la primera posición. El
caso promedio es `O(n)` bajo una posición de éxito distribuida uniformemente
o cuando se consideran ausencias; el peor caso es `O(n)` cuando la clave está
al final o no existe. El espacio adicional es `O(1)`, sin contar la entrada.

## Búsqueda binaria

La adaptación Python está en `python/algorithms/binary_search.py`. Recibe una
secuencia ordenada de enteros y una clave. Mantiene los límites inclusivos
`low` y `high`, calcula `mid = low + (high - low) // 2`, compara el elemento
central y descarta la mitad que no puede contener la clave. No ordena la
entrada, no la modifica y no usa funciones de biblioteca de búsqueda.

La función retorna un índice válido de una ocurrencia cuando encuentra la
clave. Si existen duplicados, no se exige una ocurrencia específica: cualquier
índice retornado debe contener la clave. Para una entrada de longitud `n`, el
mejor caso es `O(1)` si la clave está en el primer punto medio; el caso
promedio y el peor caso son `O(log n)` bajo el supuesto de entrada ordenada.
El espacio adicional es `O(1)` porque la implementación es iterativa.

## Búsqueda ternaria

La adaptación Python está en `python/algorithms/ternary_search.py`. Recibe una
secuencia ordenada de enteros y una clave. Mantiene los límites inclusivos
`left` y `right`, calcula los puntos `mid1` y `mid2` que dividen el intervalo
en tres regiones y descarta la región o regiones que no pueden contener la
clave. No ordena ni modifica la entrada y no usa funciones de biblioteca de
búsqueda.

La función retorna un índice válido de una ocurrencia cuando encuentra la
clave. Con duplicados no se exige una ocurrencia específica. Para una entrada
ordenada de longitud `n`, el mejor caso es `O(1)` si la clave coincide con uno
de los dos puntos de prueba iniciales. El caso promedio y el peor caso son
`O(log_3 n)`, equivalente a `O(log n)`, porque cada iteración conserva como
máximo un tercio del intervalo. El espacio adicional es `O(1)` por ser
iterativa.

## Búsqueda por saltos

La adaptación Python está en `python/algorithms/jump_search.py`. Recibe una
secuencia ordenada de enteros y una clave. Usa un bloque de tamaño aproximado
`sqrt(n)`, salta hasta el bloque candidato y después recorre linealmente ese
bloque. La guarda para arreglos vacíos y el límite `min(step, n)` evitan
accesos fuera del arreglo. `isqrt` solo calcula el tamaño entero del bloque;
la búsqueda sigue siendo el algoritmo de saltos y no una búsqueda de
biblioteca.

La adaptación Java está en `java/src/JumpSearch.java` y su prueba
autocontenida en `java/tests/JumpSearchTest.java`. Conserva los mismos
límites de bloque, el recorrido lineal y el contrato de la versión Python.
Usa `Math.sqrt` para calcular el bloque y protege explícitamente el arreglo
vacío antes de acceder al primer límite.

Para una entrada ordenada de longitud `n`, el mejor caso es `O(1)` cuando la
clave coincide con el primer elemento inspeccionado. El caso promedio y el
peor caso son `O(sqrt(n))`: se realizan aproximadamente `sqrt(n)` saltos y
como máximo `sqrt(n)` comparaciones lineales dentro del bloque. El espacio
adicional es `O(1)`. Con duplicados, cualquier índice que contenga la clave es
un resultado válido.

## Búsqueda por interpolación

La adaptación Python está en `python/algorithms/interpolation_search.py`.
Recibe una secuencia ordenada de enteros y una clave. Mientras la clave esté
dentro del rango de los extremos, estima una posición proporcional a su valor
y descarta la región que no puede contenerla. La implementación es iterativa,
no ordena ni modifica la entrada y no usa funciones de biblioteca de búsqueda.

Se usa la fórmula
`low + ((high - low) * (x - arr[low])) // (arr[high] - arr[low])`.
Multiplicar antes de dividir evita la truncación prematura de la expresión
original mostrada. Cuando los extremos son iguales, se compara directamente
con la clave y se evita la división por cero; esto cubre arreglos de valores
repetidos.

Para una entrada ordenada de longitud `n`, el mejor caso es `O(1)` cuando la
estimación acierta en la primera consulta. Bajo distribución aproximadamente
uniforme, el caso promedio es `O(log log n)`. El peor caso es `O(n)` cuando la
distribución es muy desigual o las estimaciones son desfavorables. El espacio
adicional es `O(1)` porque la adaptación es iterativa. La hipótesis de
distribución uniforme se trata como supuesto del análisis, no como garantía.

La adaptación Java está en `java/src/InterpolationSearch.java` y su prueba
autocontenida en `java/tests/InterpolationSearchTest.java`. Usa límites
inclusivos internos y aritmética `long` para evitar desbordamientos en el
producto de la fórmula con los enteros de los datos del taller. El caso de
extremos iguales se resuelve antes de dividir, por lo que los duplicados no
causan división por cero.

## Búsqueda exponencial

La adaptación Python está en `python/algorithms/exponential_search.py`.
Recibe una secuencia ordenada de enteros y una clave. Comprueba primero el
primer elemento, duplica progresivamente un límite superior mientras los
valores sigan siendo menores o iguales que la clave y aplica una búsqueda
binaria iterativa en el intervalo descubierto. No ordena ni modifica la
entrada y no utiliza funciones de biblioteca de búsqueda.

Para una entrada ordenada de longitud `n`, el mejor caso es `O(1)` cuando la
clave está en el primer elemento o se encuentra en la primera comprobación del
rango. El caso promedio y el peor caso son `O(log n)`: la expansión requiere
`O(log i)` para una posición objetivo `i` y la búsqueda binaria en el rango
descubierto tiene el mismo orden. El espacio adicional es `O(1)` porque tanto
la expansión como la búsqueda binaria son iterativas. Con duplicados, se
acepta cualquier índice válido que contenga la clave.

La adaptación Java está en `java/src/ExponentialSearch.java` y su prueba
autocontenida en `java/tests/ExponentialSearchTest.java`. Expone
`search(int[] arr, int x)`, obtiene la longitud directamente del arreglo,
trata el arreglo vacío antes de acceder a `arr[0]` y realiza la búsqueda
binaria auxiliar de forma manual. No usa `Arrays.binarySearch`, para conservar
el algoritmo implementado explícitamente y el contrato común del taller.

## Diferencias permitidas

Las diferencias entre Java y Python se limitarán a la sintaxis, tipos,
lectura de archivos y APIs de tiempo (`System.nanoTime()` frente a
`time.perf_counter_ns()`). La lógica de los seis algoritmos, sus condiciones
de frontera y sus resultados deberán mantenerse equivalentes. La prueba de
corrección comparará pertenencia, no necesariamente el índice, porque los
arreglos contienen duplicados y distintas implementaciones pueden devolver
ocurrencias válidas diferentes. Java incluirá calentamiento antes de las
mediciones oficiales.

La búsqueda lineal Java está en `java/src/LinearSearch.java` y su prueba
autocontenida en `java/tests/LinearSearchTest.java`. La clase expone
`public static int search(int[] arr, int x)` y mantiene el mismo contrato que
la versión Python: primera coincidencia o `-1`, sin modificar el arreglo. La
prueba usa únicamente el JDK y no introduce dependencias externas.

La búsqueda binaria Java está en `java/src/BinarySearch.java` y su prueba
autocontenida en `java/tests/BinarySearchTest.java`. Mantiene los límites
inclusivos `low` y `high`, calcula el punto medio con
`low + (high - low) / 2` y descarta la mitad que no puede contener la clave.
Para una entrada ordenada de longitud `n`, el mejor caso es `O(1)`, el caso
promedio y el peor caso son `O(log n)`, y el espacio adicional es `O(1)` por
ser iterativa. Con duplicados, cualquier índice coincidente es válido.

La búsqueda ternaria Java está en `java/src/TernarySearch.java` y su prueba
autocontenida en `java/tests/TernarySearchTest.java`. Mantiene los límites
inclusivos `left` y `right`, calcula `mid1` y `mid2`, compara ambos valores y
descarta la región imposible. Para una entrada ordenada de longitud `n`, el
mejor caso es `O(1)`, el caso promedio y el peor caso son `O(log_3 n)`,
equivalente a `O(log n)`, y el espacio adicional es `O(1)` por ser iterativa.
Con duplicados, cualquier índice coincidente es válido.

## Estado medido

La búsqueda lineal, la búsqueda binaria, la búsqueda ternaria, Jump Search,
la búsqueda por interpolación y la búsqueda exponencial quedaron implementadas y
probadas en Python y Java (57 tests Python OK + tests Java). El generador de claves
y sus pruebas también quedaron verificados. Los ejecutores de experimentos midieron
las 84 filas combinadas (48 de crecimiento + 36 de posición, 0 estimadas) y los
exportadores CSV generaron `results/python/`, `results/java/` y `results/combined/`.

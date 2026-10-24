#!/bin/bash

set -u
cd "$(dirname "$0")"
ALG=${1:?algoritmo}; VAR=${2:?variante}; N=${3:?n}; REPS=${4:-5}; XSS=${5:-}
[ "$VAR" = "aleatoria" ] && FILE="random_${N}.txt" || FILE="${VAR}_${N}.txt"
javac BenchOrdenamiento.java || exit 1
if [ -n "$XSS" ]; then JFLAGS="-Xss${XSS}"; else JFLAGS=""; fi
# shellcheck disable=SC2086
java $JFLAGS BenchOrdenamiento "$ALG" "../../datos/${FILE}" "$REPS"

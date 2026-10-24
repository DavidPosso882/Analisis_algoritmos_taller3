"""Jump Search implementation for sorted input sequences."""

from __future__ import annotations

from collections.abc import Sequence
from math import isqrt


def search(arr: Sequence[int], x: int) -> int:
    """Return a valid index containing ``x``, or ``-1`` when it is absent.

    The input sequence must be sorted in non-decreasing order. The algorithm
    jumps by a block of approximately ``sqrt(n)`` elements, then scans the
    candidate block linearly. With duplicate values, any matching index is
    valid.
    """
    length = len(arr)
    if length == 0:
        return -1

    block_size = max(1, isqrt(length))
    step = block_size
    previous = 0

    while arr[min(step, length) - 1] < x:
        previous = step
        step += block_size
        if previous >= length:
            return -1

    block_end = min(step, length)
    while previous < block_end and arr[previous] < x:
        previous += 1

    if previous < block_end and arr[previous] == x:
        return previous
    return -1

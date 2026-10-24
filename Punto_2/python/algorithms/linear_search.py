"""Linear search implementation used by the search-algorithm comparison."""

from __future__ import annotations

from collections.abc import Sequence


def search(arr: Sequence[int], x: int) -> int:
    """Return the first index containing ``x``, or ``-1`` when it is absent.

    The input sequence is traversed from left to right without relying on a
    library search operation. The result is valid for empty, sorted, unsorted,
    and duplicated-value sequences.
    """
    for index in range(len(arr)):
        if arr[index] == x:
            return index
    return -1

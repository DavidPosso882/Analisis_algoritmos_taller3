"""Iterative binary search implementation for sorted input sequences."""

from __future__ import annotations

from collections.abc import Sequence


def search(arr: Sequence[int], x: int) -> int:
    """Return a valid index containing ``x``, or ``-1`` when it is absent.

    The input sequence must be sorted in non-decreasing order. With duplicate
    values, the returned index may be any matching occurrence.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] == x:
            return mid
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    return -1

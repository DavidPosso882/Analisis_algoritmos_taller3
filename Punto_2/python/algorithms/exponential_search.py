"""Exponential search implementation for sorted input sequences."""

from __future__ import annotations

from collections.abc import Sequence


def _binary_search(arr: Sequence[int], low: int, high: int, x: int) -> int:
    """Search the inclusive range ``[low, high]`` without library helpers."""
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def search(arr: Sequence[int], x: int) -> int:
    """Return a valid index containing ``x``, or ``-1`` when it is absent.

    The input sequence must be sorted in non-decreasing order. The algorithm
    doubles an upper bound and then applies binary search to the discovered
    range. With duplicate values, any matching index is valid.
    """
    length = len(arr)
    if length == 0:
        return -1
    if arr[0] == x:
        return 0

    bound = 1
    while bound < length and arr[bound] <= x:
        bound *= 2

    return _binary_search(arr, bound // 2, min(bound, length - 1), x)

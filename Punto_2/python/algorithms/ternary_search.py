"""Iterative ternary search implementation for sorted input sequences."""

from __future__ import annotations

from collections.abc import Sequence


def search(arr: Sequence[int], x: int) -> int:
    """Return a valid index containing ``x``, or ``-1`` when it is absent.

    The input sequence must be sorted in non-decreasing order. With duplicate
    values, the returned index may be any matching occurrence.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3

        if arr[mid1] == x:
            return mid1
        if arr[mid2] == x:
            return mid2

        if x < arr[mid1]:
            right = mid1 - 1
        elif x > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1

    return -1

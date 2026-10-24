"""Interpolation search implementation for sorted integer sequences."""

from __future__ import annotations

from collections.abc import Sequence


def search(arr: Sequence[int], x: int) -> int:
    """Return a valid index containing ``x``, or ``-1`` when it is absent.

    The input sequence must be sorted in non-decreasing order. The algorithm
    estimates the target position from the endpoint values. With duplicate
    values, the returned index may be any matching occurrence.
    """
    low = 0
    high = len(arr) - 1

    while low <= high and arr[low] <= x <= arr[high]:
        if arr[low] == arr[high]:
            return low if arr[low] == x else -1

        position = low + ((high - low) * (x - arr[low])) // (
            arr[high] - arr[low]
        )

        if arr[position] == x:
            return position
        if arr[position] < x:
            low = position + 1
        else:
            high = position - 1

    return -1

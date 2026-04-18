"""Top-down recursive merge sort.

Returns a new sorted list and a count of element comparisons performed during
the merge step. The input list is not mutated.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple


def mergesort(data: Sequence[int]) -> Tuple[List[int], int]:
    arr = list(data)
    comparisons = _sort(arr, 0, len(arr))
    return arr, comparisons


def _sort(arr: List[int], lo: int, hi: int) -> int:
    n = hi - lo
    if n <= 1:
        return 0
    mid = lo + n // 2
    left_cmp = _sort(arr, lo, mid)
    right_cmp = _sort(arr, mid, hi)
    merge_cmp = _merge(arr, lo, mid, hi)
    return left_cmp + right_cmp + merge_cmp


def _merge(arr: List[int], lo: int, mid: int, hi: int) -> int:
    left = arr[lo:mid]
    right = arr[mid:hi]
    i = j = 0
    k = lo
    comparisons = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
    return comparisons

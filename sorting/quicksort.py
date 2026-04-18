"""In-place quicksort with randomized pivot and Lomuto partition.

Returns the sorted list (same object, sorted in place on a copy of the input)
and a count of element comparisons performed during partitioning. Uses an
explicit stack so recursion depth does not blow Python's stack on large n.

A randomized pivot is used so that adversarial inputs (already sorted,
reverse sorted) don't trigger worst-case O(n^2) behavior. This makes the
comparison against merge sort a fair one for the typical case.
"""

from __future__ import annotations

import random
from typing import List, Sequence, Tuple


def quicksort(data: Sequence[int], seed: int | None = None) -> Tuple[List[int], int]:
    arr = list(data)
    rng = random.Random(seed)
    comparisons = 0

    stack: List[Tuple[int, int]] = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        pivot_cmp, p = _partition(arr, lo, hi, rng)
        comparisons += pivot_cmp
        # Push larger side first so smaller is processed next — keeps stack O(log n) on average.
        if (p - 1 - lo) > (hi - (p + 1)):
            stack.append((lo, p - 1))
            stack.append((p + 1, hi))
        else:
            stack.append((p + 1, hi))
            stack.append((lo, p - 1))

    return arr, comparisons


def _partition(arr: List[int], lo: int, hi: int, rng: random.Random) -> Tuple[int, int]:
    pivot_idx = rng.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = arr[hi]

    comparisons = 0
    i = lo - 1
    for j in range(lo, hi):
        comparisons += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return comparisons, i + 1

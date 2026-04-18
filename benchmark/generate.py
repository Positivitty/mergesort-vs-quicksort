"""Reproducible input generators for the sorting benchmark.

Each generator is deterministic given (n, seed) so the same inputs are fed
to every algorithm and every trial can be replayed exactly.
"""

from __future__ import annotations

import random
from typing import Callable, Dict, List


def random_uniform(n: int, seed: int) -> List[int]:
    rng = random.Random(seed)
    return [rng.randint(0, 10 * n) for _ in range(n)]


def nearly_sorted(n: int, seed: int, swap_fraction: float = 0.05) -> List[int]:
    rng = random.Random(seed)
    arr = list(range(n))
    swaps = int(n * swap_fraction)
    for _ in range(swaps):
        i = rng.randrange(n)
        j = rng.randrange(n)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def reverse_sorted(n: int, seed: int) -> List[int]:
    del seed
    return list(range(n, 0, -1))


def many_duplicates(n: int, seed: int) -> List[int]:
    rng = random.Random(seed)
    # Only ~sqrt(n) distinct values so duplicates are abundant.
    distinct = max(2, int(n ** 0.5))
    return [rng.randint(0, distinct) for _ in range(n)]


DISTRIBUTIONS: Dict[str, Callable[[int, int], List[int]]] = {
    "random": random_uniform,
    "nearly_sorted": nearly_sorted,
    "reverse": reverse_sorted,
    "duplicates": many_duplicates,
}

"""Benchmark fixture: runs both algorithms across sizes, distributions, and trials.

For every (distribution, size) pair we generate a fresh random input per trial
(seeded for reproducibility), then run both mergesort and quicksort on a copy
of that same input. We record wall-clock runtime and element comparisons for
each run and verify both outputs against Python's built-in sorted().
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterable, List

from sorting import mergesort, quicksort

from .generate import DISTRIBUTIONS


@dataclass
class Run:
    algorithm: str
    distribution: str
    n: int
    trial: int
    seconds: float
    comparisons: int
    correct: bool


def sweep(
    sizes: Iterable[int],
    distributions: Iterable[str],
    trials: int,
    seed: int = 42,
) -> List[Run]:
    results: List[Run] = []
    for dist_name in distributions:
        gen = DISTRIBUTIONS[dist_name]
        for n in sizes:
            for trial in range(trials):
                trial_seed = seed + 1000 * trial + n
                data = gen(n, trial_seed)
                expected = sorted(data)

                merged, merge_cmp, merge_secs = _time(lambda: mergesort(data))
                results.append(
                    Run(
                        algorithm="mergesort",
                        distribution=dist_name,
                        n=n,
                        trial=trial,
                        seconds=merge_secs,
                        comparisons=merge_cmp,
                        correct=(merged == expected),
                    )
                )

                quicked, quick_cmp, quick_secs = _time(
                    lambda: quicksort(data, seed=trial_seed)
                )
                results.append(
                    Run(
                        algorithm="quicksort",
                        distribution=dist_name,
                        n=n,
                        trial=trial,
                        seconds=quick_secs,
                        comparisons=quick_cmp,
                        correct=(quicked == expected),
                    )
                )
    return results


def _time(fn):
    start = time.perf_counter()
    result, comparisons = fn()
    elapsed = time.perf_counter() - start
    return result, comparisons, elapsed

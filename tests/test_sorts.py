"""Correctness tests for both sort implementations.

Each algorithm is checked against Python's built-in sorted() across a range
of edge cases and random inputs. Parametrization keeps the table of checks
compact and easy to scan.
"""

from __future__ import annotations

import random

import pytest

from sorting import mergesort, quicksort


def _run(algo, data):
    if algo is quicksort:
        result, _ = algo(data, seed=0)
    else:
        result, _ = algo(data)
    return result


@pytest.fixture(params=[mergesort, quicksort], ids=["mergesort", "quicksort"])
def algo(request):
    return request.param


@pytest.mark.parametrize(
    "data",
    [
        [],
        [1],
        [2, 1],
        [1, 2],
        [3, 3, 3, 3],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [0, -1, 5, -3, 8, 2, -7],
        [1000, 1, 1000, 1, 1000, 1],
    ],
    ids=[
        "empty",
        "single",
        "two_unsorted",
        "two_sorted",
        "all_equal",
        "reverse",
        "already_sorted",
        "negatives_mixed",
        "alternating",
    ],
)
def test_edge_cases(algo, data):
    assert _run(algo, data) == sorted(data)


@pytest.mark.parametrize("n", [100, 1_000, 10_000])
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_random(algo, n, seed):
    rng = random.Random(seed)
    data = [rng.randint(-10_000, 10_000) for _ in range(n)]
    assert _run(algo, data) == sorted(data)


def test_does_not_mutate_input():
    data = [5, 4, 3, 2, 1]
    original = list(data)
    mergesort(data)
    quicksort(data, seed=0)
    assert data == original


def test_comparison_count_nonzero():
    data = [5, 4, 3, 2, 1]
    _, merge_cmp = mergesort(data)
    _, quick_cmp = quicksort(data, seed=0)
    assert merge_cmp > 0
    assert quick_cmp > 0

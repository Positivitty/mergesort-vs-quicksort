# Mergesort vs Quicksort

A head-to-head empirical comparison of two classic divide-and-conquer sorting
algorithms on the same inputs across several sizes and distributions.

This repo implements both algorithms from scratch in Python, runs them against
identical seeded inputs, and records wall-clock runtime plus element-comparison
counts. Correctness is checked against Python's built-in `sorted()` on every
run.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pytest                    # run the correctness test suite
python run_benchmark.py   # run the full benchmark sweep, write CSV + charts
```

Results land in `results/` — a timestamped CSV plus two log-log PNG charts.

## Repository layout

```
mergesort-vs-quicksort/
├── sorting/
│   ├── mergesort.py       # top-down recursive merge sort
│   └── quicksort.py       # in-place iterative quicksort, randomized pivot, Lomuto partition
├── benchmark/
│   ├── generate.py        # seeded input generators (random, nearly sorted, reverse, duplicates)
│   ├── fixture.py         # sweeps sizes × distributions × trials, times both algorithms
│   └── plot.py            # renders log-log runtime and comparison charts
├── tests/test_sorts.py    # pytest correctness suite (both algorithms, all edge cases)
├── run_benchmark.py       # CLI entry point
├── requirements.txt
└── results/               # CSV + PNGs (generated)
```

## Research

### Algorithm sketches

**Merge sort** (top-down). Recursively split the array in half until each
sub-array has length 1, then merge pairs of sorted sub-arrays back together.
The merge step walks two sorted lists in lockstep and copies the smaller head
into the output. Every element is visited once per level, and there are
⌈log₂ n⌉ levels.

**Quicksort** (randomized pivot, Lomuto partition). Pick a pivot at random,
partition the array so everything ≤ pivot sits to its left and everything >
pivot sits to its right, then recurse on the two sides. The randomized pivot
protects against the adversarial inputs (already-sorted, reverse-sorted) that
make a naive "first element" pivot degenerate to O(n²).

### Time complexity

| Algorithm | Best       | Average    | Worst       |
|-----------|------------|------------|-------------|
| Mergesort | O(n log n) | O(n log n) | O(n log n)  |
| Quicksort | O(n log n) | O(n log n) | O(n²)       |

Sources: [Wikipedia — Merge sort](https://en.wikipedia.org/wiki/Merge_sort),
[Wikipedia — Quicksort](https://en.wikipedia.org/wiki/Quicksort).

Mergesort has a tight O(n log n) bound in all three cases. Quicksort has the
same average bound but can hit O(n²) in pathological cases — most famously
when every pivot lands at an extreme of the remaining sub-array, or (as this
benchmark demonstrates) when the array contains many keys equal to the pivot
under Lomuto partitioning.

### Memory

| Algorithm | Auxiliary space         |
|-----------|-------------------------|
| Mergesort | O(n) — needs a scratch buffer for merging |
| Quicksort | O(log n) — recursion stack only, partitions in place |

Mergesort allocates a copy of the array (or at least of the half being
merged) every merge step, so memory use grows with n. Quicksort sorts
in place; the only extra memory is the stack of pending sub-array ranges.
For huge data sets that live near the memory limit of the machine,
quicksort's space advantage is decisive.

Sources: [GeeksForGeeks — Quick sort vs Merge sort](https://www.geeksforgeeks.org/quick-sort-vs-merge-sort/).

### Program complexity (lines of code)

Both implementations land around 40–60 lines of Python once you include the
partition / merge helper and the counter bookkeeping. Mergesort's recursive
structure is slightly shorter to express; quicksort adds a partition
function plus (in this implementation) an explicit stack so deep inputs
don't overflow Python's recursion limit. Neither is hard to write — they are
both textbook divide-and-conquer recipes.

### Prediction

Based on the complexity tables alone you would expect mergesort to be the
safer pick — it has no worst-case blow-up — and several writeups
([Medium — Quicksort vs Merge Sort](https://medium.com/@nehrapulkit005_40314/quicksort-vs-merge-sort-which-is-better-6eb208ab27c5))
agree that mergesort is more efficient on large arrays when predictability
matters.

But in practice quicksort is *usually* faster than mergesort by a constant
factor because:

1. It sorts in place, so it doesn't pay the cost of allocating and copying
   into a scratch buffer.
2. Its inner partition loop is tighter than the merge step — fewer bookkeeping
   operations per element.
3. With a randomized pivot, its expected case is the common case.

**Prediction going in:** quicksort will win on random inputs by a modest
constant factor. Mergesort will pull ahead on pathological inputs for
quicksort — and I expect this benchmark to surface at least one such case,
since I deliberately included a "many duplicates" distribution.

## Experimental setup

- **Sizes tested:** 1,000 / 5,000 / 10,000 / 50,000 / 100,000 / 250,000 / 500,000
- **Distributions tested:**
  - `random` — uniform random integers in `[0, 10n]`
  - `nearly_sorted` — `range(n)` with ~5% of elements swapped
  - `reverse` — `[n, n-1, …, 1]`
  - `duplicates` — only ~√n distinct values, chosen uniformly
- **Trials per (size, distribution):** 5, each with a fresh seed. Both
  algorithms see the same input within a trial.
- **Metric:** wall-clock seconds (`time.perf_counter`) and element comparisons
  recorded by instrumented code.
- **Correctness:** every output is compared to `sorted(input)`; the run fails
  hard if either algorithm returns a wrong answer.
- **Hardware:** Apple Silicon, macOS, CPython 3.x.

## Results

Average runtime (seconds) across 5 trials per cell:

| n         | dist          | mergesort | quicksort | winner    |
|----------:|---------------|----------:|----------:|-----------|
| 1,000     | random        | 0.0013    | 0.0012    | quicksort |
| 10,000    | random        | 0.0180    | 0.0150    | quicksort |
| 100,000   | random        | 0.2188    | 0.1826    | quicksort |
| 500,000   | random        | 1.2652    | 1.1179    | quicksort |
| 500,000   | nearly_sorted | 1.2626    | 0.9405    | quicksort |
| 500,000   | reverse       | 0.9890    | 0.9390    | quicksort |
| 500,000   | duplicates    | **1.2651**| **14.5892**| **mergesort** |

See `results/benchmark_2026-04-18.csv` for the full 280-row dataset and
`results/runtime_vs_size.png` / `results/comparisons_vs_size.png` for the
log-log plots.

### What the data shows

1. **On typical inputs (random, nearly sorted, reverse) quicksort wins by a
   small but consistent margin** — roughly 10–25% faster at every size once n
   is large enough for the constant-factor wins to matter. The randomized
   pivot successfully neutralizes the classic worst-case on already-sorted
   and reverse-sorted inputs.

2. **On the many-duplicates distribution quicksort collapses.** At n = 500,000
   quicksort takes **~11× longer** than mergesort (14.6 s vs 1.27 s) and the
   gap widens as n grows. This is Lomuto partitioning's well-known weakness:
   when many keys equal the pivot, the partition fails to split the array
   evenly and quicksort's effective depth approaches O(n) instead of O(log n).
   (A three-way "Dutch national flag" partition would fix this; the classic
   two-way Lomuto does not.)

3. **Mergesort's runtime is remarkably flat across distributions.** At
   n = 500,000 it takes ~1.0–1.3 s regardless of whether the input is random,
   sorted, reversed, or full of duplicates. This matches the theory — merge
   sort's worst case equals its best case.

### Conclusion — which one wins?

**It depends on what you know about your input.**

- If your data is "random enough" and you need raw speed, **quicksort wins**
  by a steady constant factor and uses dramatically less memory.
- If your data might be pathological — lots of duplicates, or an
  adversary picking the input — **mergesort wins** because its O(n log n)
  guarantee is ironclad.

The prediction going in (quicksort faster on typical inputs, mergesort safer)
held up. The surprise was the *size* of the gap on the duplicates
distribution — an 11× slowdown that the big-O table does warn about but that
you really feel when you see it measured.

This is why production library sorts — Python's Timsort, Java's dual-pivot
quicksort, C++'s introsort — all start from one of these two algorithms and
then patch the failure modes: three-way partitioning, small-array insertion
sort, fallback to heapsort when quicksort recurses too deep. The two
algorithms in this repo are the raw building blocks those hybrids are built
from.

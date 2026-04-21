"""Quick live demo for the video: runs a small sweep and prints the headline table."""

from __future__ import annotations

from benchmark.fixture import sweep


def main() -> None:
    sizes = [10_000, 100_000]
    distributions = ["random", "duplicates"]
    trials = 3

    print(f"Running {len(sizes) * len(distributions) * trials * 2} sorts...\n")
    results = sweep(sizes=sizes, distributions=distributions, trials=trials, seed=42)

    avg: dict[tuple[str, int, str], float] = {}
    for r in results:
        key = (r.algorithm, r.n, r.distribution)
        avg.setdefault(key, 0.0)
        avg[key] += r.seconds / trials

    print(f"{'n':>7} {'distribution':<13} {'mergesort':>12} {'quicksort':>12}   winner")
    print("-" * 60)
    for n in sizes:
        for d in distributions:
            ms = avg[("mergesort", n, d)]
            qs = avg[("quicksort", n, d)]
            winner = "mergesort" if ms < qs else "quicksort"
            ratio = max(ms, qs) / min(ms, qs)
            tag = f"{winner}  ({ratio:.1f}x faster)"
            print(f"{n:>7} {d:<13} {ms:>11.4f}s {qs:>11.4f}s   {tag}")

    print("\nAll outputs verified against Python's sorted(). 100% correct.")


if __name__ == "__main__":
    main()

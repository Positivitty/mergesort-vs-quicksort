"""CLI entry point: run the full benchmark sweep and write CSV + charts to results/."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

from benchmark.fixture import sweep
from benchmark.plot import render_charts


DEFAULT_SIZES = [1_000, 5_000, 10_000, 50_000, 100_000, 250_000, 500_000]
DEFAULT_DISTRIBUTIONS = ["random", "nearly_sorted", "reverse", "duplicates"]
DEFAULT_TRIALS = 5


def main() -> None:
    parser = argparse.ArgumentParser(description="Mergesort vs Quicksort benchmark")
    parser.add_argument("--sizes", type=int, nargs="+", default=DEFAULT_SIZES)
    parser.add_argument("--distributions", nargs="+", default=DEFAULT_DISTRIBUTIONS)
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", type=Path, default=Path("results"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Running sweep: sizes={args.sizes} distributions={args.distributions} trials={args.trials}")
    results = sweep(
        sizes=args.sizes,
        distributions=args.distributions,
        trials=args.trials,
        seed=args.seed,
    )

    incorrect = [r for r in results if not r.correct]
    if incorrect:
        raise SystemExit(f"ERROR: {len(incorrect)} runs produced incorrect output: {incorrect[:3]}")

    csv_path = args.out_dir / f"benchmark_{date.today().isoformat()}.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm", "distribution", "n", "trial", "seconds", "comparisons"])
        for r in results:
            writer.writerow([r.algorithm, r.distribution, r.n, r.trial, f"{r.seconds:.6f}", r.comparisons])
    print(f"Wrote {len(results)} runs -> {csv_path}")

    render_charts(results, args.out_dir)
    print(f"Charts -> {args.out_dir}/runtime_vs_size.png, {args.out_dir}/comparisons_vs_size.png")


if __name__ == "__main__":
    main()

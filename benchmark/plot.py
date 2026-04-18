"""Render benchmark charts from a list of Run records.

Two log-log plots: one for wall-clock runtime, one for comparison counts.
Each algorithm gets a line per input distribution.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Iterable

import matplotlib.pyplot as plt

from .fixture import Run


def render_charts(results: Iterable[Run], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    _render(results, out_dir / "runtime_vs_size.png", "seconds", "Runtime vs input size", "Runtime (s)")
    _render(results, out_dir / "comparisons_vs_size.png", "comparisons", "Comparisons vs input size", "Element comparisons")


def _render(results: Iterable[Run], path: Path, field: str, title: str, ylabel: str) -> None:
    # key: (algorithm, distribution) -> {n: [values]}
    buckets: dict[tuple[str, str], dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in results:
        buckets[(r.algorithm, r.distribution)][r.n].append(getattr(r, field))

    fig, ax = plt.subplots(figsize=(9, 6))
    for (algo, dist), by_n in sorted(buckets.items()):
        xs = sorted(by_n)
        ys = [mean(by_n[n]) for n in xs]
        linestyle = "-" if algo == "mergesort" else "--"
        ax.plot(xs, ys, marker="o", linestyle=linestyle, label=f"{algo} / {dist}")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Input size n")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

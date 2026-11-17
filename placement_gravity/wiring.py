"""The two wiring conditions of this study's H4 (PLAN.md §4.5), taken from the SinewSlim analysis
plan's own H4.

On the OfficeFloor arm, coupling that leaves a scope becomes configuration. H4 counts against
itself if that configuration carries the cost the code no longer does:

- **Growth.** Per chain, the least-squares slope of the wiring edges each addition adds, over the
  checkpoint index. Over chains: the mean slope with a percentile bootstrap interval (chains
  resampled with replacement). An interval above 0 counts against H4: the wiring grows faster
  than the problems.
- **Concentration.** Per chain, at its final checkpoint, the share of the configuration's lines
  (neither blank nor only a comment) held by its largest file. Over chains: the mean share, with
  its interval. A mean over 0.5 counts against H4: one file holds most of the wiring.

The rows are ``tables.addition_rows`` of one arm, any number of chains.
"""

from __future__ import annotations

import random
import statistics

#: The bootstrap of PLAN.md §4.5: resamples, and a seed fixed before any run is read.
RESAMPLES = 10_000
SEED = 20261116
#: A largest-file share above this counts against H4.
CONCENTRATION_LIMIT = 0.5


def slope(xs: list[float], ys: list[float]) -> float | None:
    """The least-squares slope of ys on xs (None for fewer than two distinct xs)."""
    if len(set(xs)) < 2:
        return None
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    return (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            / sum((x - mx) ** 2 for x in xs))


def chain_checks(rows: list[dict]) -> dict:
    """Both conditions for one chain's addition rows."""
    rows = sorted(rows, key=lambda r: r["cp"])
    last = rows[-1]
    return {
        "arm": last["arm"], "chain": last["chain"], "checkpoints": len(rows),
        "edges_added": sum(r["wiring_edges_added"] for r in rows),
        "growth_slope": slope([r["cp"] for r in rows], [r["wiring_edges_added"] for r in rows]),
        "final_cp": last["cp"], "final_files": last["wiring_files"],
        "final_lines": last["wiring_lines"], "final_largest_share": last["wiring_largest_share"],
    }


def _interval(values: list[float], rng: random.Random, resamples: int) -> list[float] | None:
    if len(values) < 2:
        return None
    means = sorted(statistics.fmean(rng.choices(values, k=len(values))) for _ in range(resamples))
    return [means[int(0.025 * (resamples - 1))], means[int(0.975 * (resamples - 1))]]


def verdict(chains: list[dict], seed: int = SEED, resamples: int = RESAMPLES) -> dict:
    """The conditions over chains (``chain_checks`` of one arm). With one chain there is no
    interval, so growth is not read; concentration is read on the point estimate."""
    rng = random.Random(seed)
    slopes = [c["growth_slope"] for c in chains if c["growth_slope"] is not None]
    shares = [c["final_largest_share"] for c in chains if c["final_largest_share"] is not None]
    g = _interval(slopes, rng, resamples)
    c = _interval(shares, rng, resamples)
    share = statistics.fmean(shares) if shares else None
    return {
        "chains": len(chains),
        "growth_slope": statistics.fmean(slopes) if slopes else None, "growth_interval": g,
        "growth_against": (g[0] > 0) if g else None,
        "largest_share": share, "largest_share_interval": c,
        "concentration_against": (share > CONCENTRATION_LIMIT) if share is not None else None,
    }

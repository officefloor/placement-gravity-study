"""The readings reported beside the hypotheses (PLAN.md §5): choice at a checkpoint, formation
(where it ends) and review. Each has a stated direction and none is a confirmatory test. The
lagged formation term is a model and is fitted in analysis/analyse.R.

All three read the chains' tables (step 3). A checkpoint is one problem, solved by every chain, so
the chains at one checkpoint show how much choice the problem left.
"""

from __future__ import annotations

import random
import statistics

SEED = 20261116
RESAMPLES = 10_000
MIN_CHAINS = 4


def _true(x) -> bool:
    return str(x) == "True"


def _ranks(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def spearman(xs: list[float], ys: list[float]) -> float | None:
    """Spearman's rank correlation (ties share their mean rank); None when it is not defined."""
    if len(xs) < 3:
        return None
    rx, ry = _ranks(xs), _ranks(ys)
    mx, my = statistics.fmean(rx), statistics.fmean(ry)
    sx = sum((a - mx) ** 2 for a in rx)
    sy = sum((b - my) ** 2 for b in ry)
    if sx == 0 or sy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / (sx * sy) ** 0.5


def _interval(draws: list[float]) -> list[float] | None:
    draws = sorted(draws)
    if len(draws) < 100:
        return None
    return [draws[int(0.025 * (len(draws) - 1))], draws[int(0.975 * (len(draws) - 1))]]


def ties_per_run(run_rows: list[dict]) -> dict[str, dict[int, list[int]]]:
    """chain -> checkpoint -> the ties of each run of added logic (moved code left out)."""
    out: dict[str, dict[int, list[int]]] = {}
    for r in run_rows:
        if not _true(r.get("replacement")):
            out.setdefault(r["chain_id"], {}).setdefault(int(r["cp"]), []).append(int(r["tie"]))
    return out


def prior_tie_mean(run_rows: list[dict]) -> dict[tuple[str, int], float]:
    """(chain, checkpoint k) -> the chain's mean ties per run over its checkpoints before k: how
    far the chain has been forced so far (the lagged formation term)."""
    out = {}
    for chain_id, by_cp in ties_per_run(run_rows).items():
        total = n = 0
        last = max(by_cp)
        for cp in range(1, last + 2):
            if n:
                out[(chain_id, cp)] = total / n
            total += sum(by_cp.get(cp, []))
            n += len(by_cp.get(cp, []))
    return out


# ---- choice at a checkpoint ----

def choice(additions: list[dict], hosts: list[dict]) -> list[dict]:
    """Per checkpoint and arm, over the chains: the share that placed any of the addition in an
    existing host, the distinct hosts the chains used between them, and the spread of the ties."""
    used: dict[tuple[str, int], set] = {}
    for h in hosts:
        if float(h["net_added"]) > 0 and not _true(h["replacement"]):
            used.setdefault((h["arm"], int(h["cp"])), set()).add((h["type"], h["name"]))
    cells: dict[tuple[str, int], list[dict]] = {}
    for a in additions:
        if float(a["positions_added"]) > 0:
            cells.setdefault((a["arm"], int(a["cp"])), []).append(a)
    rows = []
    for (arm, cp), xs in sorted(cells.items()):
        ties = [int(a["tie_method"]) + int(a["tie_class"]) for a in xs]
        rows.append({"arm": arm, "cp": cp, "chains": len(xs),
                     "share_in_existing_host": sum(int(a["hosts_existing"]) > 0 for a in xs) / len(xs),
                     "distinct_hosts": len(used.get((arm, cp), ())),
                     "hosts_per_chain": statistics.fmean(int(a["hosts"]) for a in xs),
                     "tie_mean": statistics.fmean(ties),
                     "tie_sd": statistics.pstdev(ties) if len(ties) > 1 else None})
    return rows


def choice_summary(rows: list[dict]) -> dict:
    """Per arm: how many checkpoints left no choice (every chain with the same ties and the same
    side of new or existing host) and how many left one."""
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        xs = [r for r in rows if r["arm"] == arm and r["chains"] > 1]
        same = [r for r in xs if r["tie_sd"] == 0 and r["share_in_existing_host"] in (0.0, 1.0)]
        out[arm] = {"checkpoints": len(xs), "no_choice": len(same),
                    "share_no_choice": len(same) / len(xs) if xs else None,
                    "median_tie_sd": statistics.median(r["tie_sd"] for r in xs) if xs else None,
                    "median_distinct_hosts": statistics.median(r["distinct_hosts"] for r in xs)
                    if xs else None}
    return out


# ---- formation: where it ends ----

def formation_end(run_rows: list[dict], additions: list[dict], checkpoints: int,
                  seed: int = SEED, resamples: int = RESAMPLES) -> dict:
    """Per arm, over its chains: Spearman's correlation between the mean ties per run in the first
    third of the stream and the share of the tree's positions held by its largest method at the
    final checkpoint. Predicted positive in the methods arm. Interval: chains resampled."""
    ties = ties_per_run(run_rows)
    third = checkpoints / 3
    final: dict[str, dict] = {}
    for a in additions:
        if a["chain_id"] not in final or int(a["cp"]) > int(final[a["chain_id"]]["cp"]):
            final[a["chain_id"]] = a
    out = {}
    for arm in sorted({a["arm"] for a in additions}):
        pairs = []
        for chain_id, a in sorted(final.items()):
            early = [t for cp, ts in ties.get(chain_id, {}).items() if cp <= third for t in ts]
            if a["arm"] != arm or not early or a.get("amount_largest") in (None, "") \
                    or not float(a["amount_positions"]):
                continue
            pairs.append((statistics.fmean(early), float(a["amount_largest"]) / float(a["amount_positions"])))
        rho = spearman([p[0] for p in pairs], [p[1] for p in pairs])
        interval = None
        if rho is not None and len(pairs) >= MIN_CHAINS:
            rng = random.Random(seed)
            draws = []
            for _ in range(resamples):
                s = rng.choices(pairs, k=len(pairs))
                r = spearman([p[0] for p in s], [p[1] for p in s])
                if r is not None:
                    draws.append(r)
            interval = _interval(draws)
        out[arm] = {"chains": len(pairs), "rho": rho, "interval": interval,
                    "early_ties_mean": statistics.fmean(p[0] for p in pairs) if pairs else None,
                    "largest_share_mean": statistics.fmean(p[1] for p in pairs) if pairs else None}
    return out


# ---- review ----

def _per_chain(rows: list[dict], value) -> dict[str, dict[str, dict[int, float]]]:
    """arm -> chain -> checkpoint -> value(row), where the value is defined."""
    out: dict[str, dict[str, dict[int, float]]] = {}
    for r in rows:
        v = value(r)
        if v is not None:
            out.setdefault(r["arm"], {}).setdefault(r["chain_id"], {})[int(r["cp"])] = v
    return out


def _mean_over(chains: list[dict[int, float]], cp: int) -> float | None:
    xs = [c[cp] for c in chains if cp in c]
    return statistics.fmean(xs) if xs else None


def review(primary_runs: list[dict], primary_additions: list[dict], reviewed_additions: list[dict],
           seed: int = SEED, resamples: int = 2_000) -> dict:
    """Per arm, over the checkpoints: Spearman's correlation of T, the mean ties per run of the
    just-solve chains, with D, the absolute difference between the conditions in the share of the
    addition's positions landing in existing hosts. Predicted negative: the review changes the
    placement where the ties are few. Interval: the chains of each condition resampled."""
    def share(a):
        return float(a["share_in_existing"]) if a.get("share_in_existing") not in (None, "", "None") else None

    by_run = ties_per_run(primary_runs)
    arm_of = {a["chain_id"]: a["arm"] for a in primary_additions}
    ties: dict[str, list[dict[int, float]]] = {}
    for chain_id, by_cp in by_run.items():
        if chain_id in arm_of:
            ties.setdefault(arm_of[chain_id], []).append(
                {cp: statistics.fmean(ts) for cp, ts in by_cp.items()})
    prim, rev = _per_chain(primary_additions, share), _per_chain(reviewed_additions, share)

    def rho(t, p, r):
        xs, ys = [], []
        for cp in sorted({c for ch in p for c in ch} & {c for ch in r for c in ch}):
            tk, pk, rk = _mean_over(t, cp), _mean_over(p, cp), _mean_over(r, cp)
            if None not in (tk, pk, rk):
                xs.append(tk)
                ys.append(abs(rk - pk))
        return spearman(xs, ys), len(xs)

    out = {}
    for arm in sorted(set(prim) & set(rev)):
        t, p, r = ties.get(arm, []), list(prim[arm].values()), list(rev[arm].values())
        est, n = rho(t, p, r)
        interval = None
        if est is not None and min(len(t), len(p), len(r)) >= MIN_CHAINS:
            rng = random.Random(seed)
            draws = []
            for _ in range(resamples):
                idx = [rng.randrange(len(p)) for _ in p]
                d, _ = rho(rng.choices(t, k=len(t)), [p[i] for i in idx], rng.choices(r, k=len(r)))
                if d is not None:
                    draws.append(d)
            interval = _interval(draws)
        out[arm] = {"checkpoints": n, "chains_just_solve": len(p), "chains_reviewed": len(r),
                    "rho": est, "interval": interval,
                    "against": (est is not None and est >= 0)}
    return out


# ---- bystanders: the description beside H1 and H3 ----

def bystander_summary(by: list[dict], captured: list[dict], checkpoints: int) -> dict:
    """Per arm: the share of runs that need nothing that was there (free: not pulled anywhere), and
    for the runs that do, the needed values and the bystanders per run (PLAN.md §4.3a), over the
    whole stream and over its thirds, at method and class level; and accretion, the fields an
    addition leaves in classes that already existed."""
    out = {}
    for arm in sorted({r["arm"] for r in by}):
        every = [r for r in by if r["arm"] == arm]
        rows = [r for r in every if r["pulled"]]
        mean = lambda xs, k: statistics.fmean(x[k] for x in xs) if xs else None
        thirds = []
        for i in range(3):
            lo, hi = i * checkpoints / 3, (i + 1) * checkpoints / 3
            thirds.append(mean([r for r in rows if lo < r["cp"] <= hi], "bystanders") if checkpoints else None)
        adds = [c for c in captured if c["arm"] == arm]
        out[arm] = {"runs": len(every), "pulled": len(rows), "share_free": 1 - len(rows) / len(every),
                    "need": mean(rows, "need"), "bystanders": mean(rows, "bystanders"),
                    "by_method": mean(rows, "by_method"), "by_class": mean(rows, "by_class"),
                    "without_constants": mean(rows, "bystanders_no_constants"), "thirds": thirds,
                    "fields_added_per_addition": mean(adds, "fields_added")}
    return out

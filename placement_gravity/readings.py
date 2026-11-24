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
    """Spearman's rank correlation (bindings share their mean rank); None when it is not defined."""
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


def bindings_per_run(run_rows: list[dict]) -> dict[str, dict[int, list[int]]]:
    """chain -> checkpoint -> the bindings of each run of added logic (moved code left out)."""
    out: dict[str, dict[int, list[int]]] = {}
    for r in run_rows:
        if not _true(r.get("replacement")):
            out.setdefault(r["chain_id"], {}).setdefault(int(r["cp"]), []).append(int(r["binding"]))
    return out


def prior_binding_mean(run_rows: list[dict]) -> dict[tuple[str, int], float]:
    """(chain, checkpoint k) -> the chain's mean bindings per run over its checkpoints before k: how
    far the chain has been forced so far (the lagged formation term)."""
    out = {}
    for chain_id, by_cp in bindings_per_run(run_rows).items():
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
    existing host, the distinct hosts the chains used between them, and the spread of the bindings."""
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
        bindings = [int(a["binding_method"]) + int(a["binding_class"]) for a in xs]
        rows.append({"arm": arm, "cp": cp, "chains": len(xs),
                     "share_in_existing_host": sum(int(a["hosts_existing"]) > 0 for a in xs) / len(xs),
                     "distinct_hosts": len(used.get((arm, cp), ())),
                     "hosts_per_chain": statistics.fmean(int(a["hosts"]) for a in xs),
                     "binding_mean": statistics.fmean(bindings),
                     "binding_sd": statistics.pstdev(bindings) if len(bindings) > 1 else None})
    return rows


def choice_summary(rows: list[dict]) -> dict:
    """Per arm: how many checkpoints left no choice (every chain with the same bindings and the same
    side of new or existing host) and how many left one."""
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        xs = [r for r in rows if r["arm"] == arm and r["chains"] > 1]
        same = [r for r in xs if r["binding_sd"] == 0 and r["share_in_existing_host"] in (0.0, 1.0)]
        out[arm] = {"checkpoints": len(xs), "no_choice": len(same),
                    "share_no_choice": len(same) / len(xs) if xs else None,
                    "median_binding_sd": statistics.median(r["binding_sd"] for r in xs) if xs else None,
                    "median_distinct_hosts": statistics.median(r["distinct_hosts"] for r in xs)
                    if xs else None}
    return out


# ---- formation: where it ends ----

def formation_end(run_rows: list[dict], additions: list[dict], checkpoints: int,
                  seed: int = SEED, resamples: int = RESAMPLES) -> dict:
    """Per arm, over its chains: Spearman's correlation between the mean bindings per run in the first
    third of the stream and the share of the tree's positions held by its largest method at the
    final checkpoint. Predicted positive in the methods arm. Interval: chains resampled."""
    bindings = bindings_per_run(run_rows)
    third = checkpoints / 3
    final: dict[str, dict] = {}
    for a in additions:
        if a["chain_id"] not in final or int(a["cp"]) > int(final[a["chain_id"]]["cp"]):
            final[a["chain_id"]] = a
    out = {}
    for arm in sorted({a["arm"] for a in additions}):
        pairs = []
        for chain_id, a in sorted(final.items()):
            early = [t for cp, ts in bindings.get(chain_id, {}).items() if cp <= third for t in ts]
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
                    "early_bindings_mean": statistics.fmean(p[0] for p in pairs) if pairs else None,
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
    """Per arm, over the checkpoints: Spearman's correlation of T, the mean bindings per run of the
    just-solve chains, with D, the absolute difference between the conditions in the share of the
    addition's positions landing in existing hosts. Predicted negative: the review changes the
    placement where the bindings are few. Interval: the chains of each condition resampled."""
    def share(a):
        return float(a["share_in_existing"]) if a.get("share_in_existing") not in (None, "", "None") else None

    by_run = bindings_per_run(primary_runs)
    arm_of = {a["chain_id"]: a["arm"] for a in primary_additions}
    bindings: dict[str, list[dict[int, float]]] = {}
    for chain_id, by_cp in by_run.items():
        if chain_id in arm_of:
            bindings.setdefault(arm_of[chain_id], []).append(
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
        t, p, r = bindings.get(arm, []), list(prim[arm].values()), list(rev[arm].values())
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


# ---- bystanders: the description beside H3 and H4 ----

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
                    "fields_added_per_addition": mean(adds, "fields_added"),
                    "method_values_added_per_addition": mean(
                        [a for a in adds if "method_values_added" in a], "method_values_added")}
    return out


def reopening_summary(rows: list[dict]) -> dict:
    """Per arm: the classes and the wiring files reopened per checkpoint (PLAN.md §4.4)."""
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        xs = [r for r in rows if r["arm"] == arm]
        out[arm] = {"checkpoints": len(xs), "classes": statistics.fmean(r["reopened_classes"] for r in xs),
                    "wiring": statistics.fmean(r["reopened_wiring"] for r in xs)}
    return out


def drawn_summary(h2: list[dict]) -> dict:
    """Per arm, over the problem and host rows whose code was bound there (PLAN.md §4.4, H2): what
    stood by at the placement, the later intrusions there, and how many of them are bound to
    something that stood by, at the class and at the method; and the same for what the change
    introduced there, and for either (§4.3b)."""
    out = {}
    for arm in sorted({r["arm"] for r in h2}):
        rows = [r for r in h2 if r["arm"] == arm and r["bound"]]
        if not rows:
            out[arm] = {"rows": 0}
            continue
        x = {"rows": len(rows)}
        for lev in ("class", "method"):
            later = sum(r[f"intrusion_{lev}"] for r in rows)
            drawn = sum(r[f"drawn_{lev}"] for r in rows)
            x[lev] = {"bystanders": statistics.fmean(r[f"bystanders_{lev}"] for r in rows),
                      "later": later, "drawn": drawn, "share": (drawn / later) if later else None}
            if f"introduced_{lev}" in rows[0]:      # what the change introduced there (§4.3b)
                took = sum(r[f"drawn_{lev}_introduced"] for r in rows)
                either = sum(r[f"drawn_{lev}_left"] for r in rows)
                x[lev].update({"introduced": statistics.fmean(r[f"introduced_{lev}"] for r in rows),
                               "drawn_introduced": took,
                               "share_introduced": (took / later) if later else None,
                               "drawn_left": either, "share_left": (either / later) if later else None})
        out[arm] = x
    return out


def core_reuse(h2: list[dict]) -> dict:
    """Per arm and level, over the bound rows (PLAN.md §5, reported beside H4): the later
    intrusions' uses of core values and of periphery values, per 100 values and later checkpoints."""
    out = {}
    for arm in sorted({r["arm"] for r in h2}):
        rows = [r for r in h2 if r["arm"] == arm and r["bound"] and r["later_checkpoints"] > 0]
        x = {}
        for lev in ("class", "method"):
            if not rows or f"core_{lev}" not in rows[0]:
                continue
            for kind in ("core", "periphery"):
                at_risk = sum(r[f"{kind}_{lev}"] * r["later_checkpoints"] for r in rows)
                uses = sum(r[f"uses_{kind}_{lev}"] for r in rows)
                x[f"{kind}_{lev}"] = {"records": sum(1 for r in rows if r[f"{kind}_{lev}"] > 0),
                                      "values": sum(r[f"{kind}_{lev}"] for r in rows), "uses": uses,
                                      "per_100": (100 * uses / at_risk) if at_risk else None}
        out[arm] = x
    return out


def core_summary(hosts: list[dict]) -> dict:
    """Per arm, over the hosts whose added code is bound there (PLAN.md §5, *Core and periphery*):
    how the bound uses of a place's pre-existing values are spread over those values, at the class
    (its fields) and at the method (its parameters and locals). ``top3_share`` is the share of all
    uses that go to the three most used values of each chain; ``from_start`` the share of uses that go to values no checkpoint of the chain
    introduced; ``introduced`` the values the chain's changes introduced, and ``promoted`` those
    of them that bound code of a later checkpoint uses."""
    truth = lambda x: str(x) == "True"
    out = {}
    for arm in sorted({h["arm"] for h in hosts}):
        mine = [h for h in hosts if h["arm"] == arm]
        if not mine or "introduced_method_values" not in mine[0]:
            continue
        x = {}
        for lev, col, new in (("class", "need_class_values", "introduced_class_values"),
                              ("method", "need_method_values", "introduced_method_values")):
            place = (lambda h: (h.get("chain_id", h.get("chain")), h["type"])) if lev == "class" else \
                (lambda h: (h.get("chain_id", h.get("chain")), h["type"], h["name"]))
            born: dict[tuple, int] = {}
            for h in sorted(mine, key=lambda h: int(h["cp"])):
                for v in (h.get(new) or "").split():
                    born.setdefault((place(h), v), int(h["cp"]))
            uses: dict[tuple, int] = {}
            later: set[tuple] = set()
            for h in mine:
                if int(h["binding"]) < 1 or int(h["net_added"]) <= 0 or truth(h.get("replacement")):
                    continue
                for v in set((h.get(col) or "").split()):
                    key = (place(h), v)
                    uses[key] = uses.get(key, 0) + 1
                    if key in born and int(h["cp"]) > born[key]:
                        later.add(key)
            total = sum(uses.values())
            per_chain: dict[str, list[int]] = {}
            for (p, _), n in uses.items():
                per_chain.setdefault(p[0], []).append(n)
            top3 = sum(sum(sorted(ns, reverse=True)[:3]) for ns in per_chain.values())
            x[lev] = {"values_used": len(uses), "uses": total,
                      "top3_share": (top3 / total) if total else None,
                      "from_start": (sum(n for k, n in uses.items() if k not in born) / total) if total else None,
                      "introduced": len(born), "promoted": len(later),
                      "promoted_share": (len(later) / len(born)) if born else None}
        out[arm] = x
    return out

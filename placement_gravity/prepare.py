"""Step 4, first half: the analysis datasets of one analysis, from its chains' tables (step 3).

    python -m placement_gravity.prepare [--analysis NAME ...]

Writes data/analysis/<name>/:

- ``h1.csv``: one row per run of added logic into an existing method (H1, H3), with its ties and
  its host's size before the addition. New methods are left out: a new host has no prior size, so
  including them would make "more ties in bigger hosts" true by construction.
- ``h2.csv``: one row per problem and host its code went into (H2, the junction × arm reading),
  with later intrusion, the problem's size and declared crossings, the host's size and its shape at
  k − 1.
- ``spec.json``: what the R models need (seed, resamples, the equivalence bound, the shape measures
  kept by the variation rule, whether the stream has acts).
- ``conditions.json``: what H3 reads besides the models (the amount band and the wiring checks),
  and whether the analysis is descriptive only (fewer than 6 chains in an arm).
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import statistics
from pathlib import Path

from . import chain, runs, wiring

DATA = chain.ROOT / "data" / "analysis"
SEED = 20261116
#: Cluster-bootstrap refits for the H1 and H3 models (PLAN.md §5).
BOOT = 1000
BOUND = [0.8, 1.25]
AMOUNT_BAND = [0.8, 1.25]
MIN_FLAGGED = 10
MIN_CHAINS = 6
SHAPE_FLAGS = ["s1_long", "s2_stuck", "s3_junction"]
SHAPE_LEVELS = ["s4_cognitive", "s5_class_gini"]
METHODS_ARM, FUNCTION_ARM = "spring", "officefloor"


def read(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def truth(x) -> bool:
    return str(x) == "True"


def num(x, default=None):
    if x in (None, "", "None"):
        return default
    return float(x)


def gather(analysis: str, table: str, root: Path | None = None) -> list[dict]:
    base = (root or (runs.RESULTS / "measure")) / analysis
    rows = []
    for d in sorted(p for p in base.iterdir() if p.is_dir()) if base.exists() else []:
        rows += read(d / f"{table}.csv")
    return rows


def h1_rows(run_rows: list[dict], host_rows: list[dict], streamed: dict) -> list[dict]:
    cls = {(h["chain_id"], h["cp"], h["type"], h["signature"]): h.get("s5_class_positions")
           for h in host_rows}
    out = []
    for r in run_rows:
        if truth(r["host_new"]) or truth(r.get("replacement")):
            continue
        cp = int(r["cp"])
        out.append({
            "chain_id": r["chain_id"], "arm": r["arm"], "frontend": r.get("frontend", ""),
            "cp": cp, "act": streamed.get(cp, {}).get("act"),
            "tie": int(r["tie"]), "tie_no_param": int(r["tie_no_param"]),
            "tie_class": int(r["tie_class"]), "pre_positions": int(r["pre_positions"]),
            "class_positions": num(cls.get((r["chain_id"], r["cp"], r["type"], r["signature"]))),
        })
    return out


def h2_rows(outcomes: list[dict], host_rows: list[dict], additions: list[dict],
            streamed: dict) -> list[dict]:
    hosts = {(h["chain_id"], h["cp"], h["type"], h["signature"]): h for h in host_rows}
    size = {(a["chain_id"], a["cp"]): int(a["positions_added"]) for a in additions}
    out = []
    for o in outcomes:
        h = hosts.get((o["chain_id"], o["cp"], o["type"], o["signature"]), {})
        cp = int(o["cp"])
        s = streamed.get(cp, {})
        row = {
            "chain_id": o["chain_id"], "arm": o["arm"], "frontend": o.get("frontend", ""),
            "cp": cp, "act": s.get("act"),
            "intrusion": int(o["intrusion"]), "later_checkpoints": int(o["later_checkpoints"]),
            "tie": int(o["tie"]), "tie_no_param": int(h.get("tie_no_param", o["tie"])),
            "net_added": int(o["net_added"]),
            "addition_positions": size.get((o["chain_id"], o["cp"]), int(o["net_added"])),
            "declared_crossings": len(set(s.get("crosses", [])) | set(s.get("mutates", []))),
            "pre_positions": int(o["pre_positions"]), "host_new": truth(o["host_new"]),
            "shape_found": truth(h.get("shape_found")),
        }
        for c in SHAPE_FLAGS + ["s3_junction_injection_aware"]:
            row[c] = truth(h.get(c)) if h.get("shape_found") == "True" else None
        row["s4_cognitive"] = num(h.get("s4_cognitive"))
        row["s5_class_gini"] = num(h.get("s5_class_gini"))
        out.append(row)
    return out


def shape_kept(h2: list[dict]) -> tuple[list[str], dict]:
    """The variation rule (PLAN.md §5): a shape measure flagged (or, for a level, non-zero) on
    fewer than MIN_FLAGGED existing hosts in any arm leaves the H2b block."""
    rows = [r for r in h2 if not r["host_new"] and r["shape_found"]]
    arms = sorted({r["arm"] for r in rows})
    counts, kept = {}, []
    for c in SHAPE_FLAGS + SHAPE_LEVELS:
        per = {a: sum(1 for r in rows if r["arm"] == a and r[c]) for a in arms}
        counts[c] = per
        if arms and min(per.values()) >= MIN_FLAGGED:
            kept.append(c)
    return kept, counts


def amount(additions: list[dict], seed: int = SEED, resamples: int = 10_000) -> dict:
    """H3's amount band: each chain's positions at its final checkpoint; the ratio of the function
    arm's mean to the methods arm's, with a bootstrap interval (chains resampled within arm)."""
    final: dict[str, tuple[int, str, float]] = {}
    for a in additions:
        cp = int(a["cp"])
        if a["chain_id"] not in final or cp > final[a["chain_id"]][0]:
            final[a["chain_id"]] = (cp, a["arm"], float(a["amount_positions"]))
    by_arm: dict[str, list[float]] = {}
    for _, arm, v in final.values():
        by_arm.setdefault(arm, []).append(v)
    m, f = by_arm.get(METHODS_ARM, []), by_arm.get(FUNCTION_ARM, [])
    if not m or not f:
        return {"ratio": None, "interval": None, "in_band": None, "per_arm": by_arm}
    ratio = statistics.fmean(f) / statistics.fmean(m)
    rng = random.Random(seed)
    draws = sorted(statistics.fmean(rng.choices(f, k=len(f))) / statistics.fmean(rng.choices(m, k=len(m)))
                   for _ in range(resamples))
    interval = [draws[int(0.025 * (resamples - 1))], draws[int(0.975 * (resamples - 1))]]
    return {"ratio": ratio, "interval": interval,
            "in_band": AMOUNT_BAND[0] <= ratio <= AMOUNT_BAND[1], "band": AMOUNT_BAND,
            "per_arm": {k: statistics.fmean(v) for k, v in by_arm.items()}}


def wiring_checks(additions: list[dict]) -> dict:
    by_chain: dict[str, list[dict]] = {}
    for a in additions:
        if a["arm"] == FUNCTION_ARM:
            by_chain.setdefault(a["chain_id"], []).append({
                **a, "chain": a["chain_id"], "cp": int(a["cp"]),
                "wiring_edges_added": int(a["wiring_edges_added"]),
                "wiring_files": int(a["wiring_files"]), "wiring_lines": int(a["wiring_lines"]),
                "wiring_largest_share": num(a["wiring_largest_share"])})
    chains = [wiring.chain_checks(rows) for rows in by_chain.values()]
    return {"chains": chains, "verdict": wiring.verdict(chains) if chains else None}


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)


def prepare(analysis: dict, streamed: dict, measured_root: Path | None = None,
            out_root: Path = DATA) -> Path:
    name = analysis["name"]
    hosts = gather(name, "hosts", measured_root)
    h1 = h1_rows(gather(name, "runs", measured_root), hosts, streamed)
    additions = gather(name, "additions", measured_root)
    h2 = h2_rows(gather(name, "outcomes", measured_root), hosts, additions, streamed)
    kept, counts = shape_kept(h2)
    chains: dict[str, set] = {}
    for a in additions:
        chains.setdefault(a["arm"], set()).add(a["chain_id"])
    out = out_root / name
    write_csv(out / "h1.csv", h1)
    write_csv(out / "h2.csv", h2)
    spec = {"analysis": name, "role": analysis["role"], "seed": SEED, "boot": BOOT,
            "bound": BOUND, "methods_arm": METHODS_ARM, "function_arm": FUNCTION_ARM,
            "shape_kept": kept, "shape_counts": counts,
            "acts": any(r["act"] is not None for r in h1 + h2),
            "frontends": sorted({r["frontend"] for r in h1 if r["frontend"]})}
    conditions = {"chains": {k: len(v) for k, v in chains.items()},
                  "descriptive_only": analysis["role"] == "development"
                  or any(len(v) < MIN_CHAINS for v in chains.values()) or len(chains) < 2,
                  "amount": amount(additions), "wiring": wiring_checks(additions)}
    (out / "spec.json").write_text(json.dumps(spec, indent=1) + "\n")
    (out / "conditions.json").write_text(json.dumps(conditions, indent=1) + "\n")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", nargs="*")
    a = ap.parse_args()
    reg = runs.load()
    for analysis in reg["analyses"]:
        if a.analysis and analysis["name"] not in a.analysis:
            continue
        if not (runs.RESULTS / "measure" / analysis["name"]).exists():
            continue
        runs.guard(reg, analysis)
        out = prepare(analysis, runs.stream(reg, analysis["stream"]))
        print(f"{analysis['name']}: {out}")


if __name__ == "__main__":
    main()

"""Step 4, first half: the analysis datasets of one analysis, from its chains' tables (step 3).

    python -m placement_gravity.prepare [--analysis NAME ...]

Writes data/analysis/<name>/:

- ``by.csv``: one row per run of added logic that needs at least one pre-existing value, in new
  hosts and existing ones (H1, H4), with its bystanders (PLAN.md §4.3a): the pre-existing values
  visible where it starts that it does not use; and the class and the method it is in.
- ``capture.csv``: one row per addition, with the share of its positions landing in existing hosts
  and the fields held by the chain's heaviest class at k − 1 (the capture reading).
- ``h1.csv``: one row per run of added logic into an existing method, with its bindings and its host's
  size before the addition (H1 and H4 as first registered, reported; the lagged formation term).
  New methods are left out: a new host has no prior size, so including them would make "more bindings
  in bigger hosts" true by construction.
- ``reopen.csv``: one row per checkpoint, with the classes its bound code goes back into and the
  wiring files it changes again (reported).
- ``h2.csv``: one row per problem and host its code went into (H2, H3, H4, the junction × arm
  reading), with what stood by there, the later intrusion at the class and the method, how much of
  it is bound to what stood by, the problem's own lines, the problem's size and declared crossings,
  the host's size and its shape at k − 1.
- ``spec.json``: what the R models need (seed, resamples, the equivalence margin, the shape measures
  kept by the variation rule, whether the stream has acts).
- ``conditions.json``: what H4 reads besides the models (the amount band and the wiring checks),
  and whether the analysis is descriptive only (fewer than 6 chains in an arm).
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import statistics
from pathlib import Path

from . import chain, literature, places, readings, runs, wiring

DATA = chain.ROOT / "data" / "analysis"
SEED = 20261116
#: Cluster-bootstrap refits for the H1 and H4 models (PLAN.md §5).
BOOT = 1000
MARGIN = [0.8, 1.25]
AMOUNT_BAND = [0.8, 1.25]
MIN_FLAGGED = 10
MIN_CHAINS = 6
#: H3's shape measures are the literature's: long, complex, concentrated. The sinew measures (not
#: slimmable, junction) are the author's own, about data flow; they are read apart (PLAN.md §5).
SHAPE_FLAGS = ["s1_long"]
SINEW_FLAGS = ["s2_stuck", "s3_junction"]
#: The shape measures first registered, read beside the literature's at their level (the class's
#: Gini as a class measure, ``c_gini``).
FIRST = {"s1_long": ("method", "flag", "long: 26 or more code lines"),
         "s4_cognitive": ("method", "level", "Campbell 2018, cognitive complexity"),
         "c_gini": ("class", "plain", "concentration of the class's positions (Gini)")}
#: H3's measures (PLAN.md §2, §5): length and complexity at the method; concentration, weight and
#: lack of cohesion at the class. Each is fitted alone and has to lie below the upper margin.
H3_MEASURES = ["s1_long", "s4_cognitive", "m_cyclomatic", "c_gini", "c_wmc", "c_lcom_star"]
#: How far a place reaches out: read with the sinew measures, predicted above 1.
REACH = ["m_fanout", "c_cbo", "c_fanout"]
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
    prior = readings.prior_binding_mean(run_rows)
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
            "binding": int(r["binding"]), "binding_no_param": int(r["binding_no_param"]),
            "binding_class": int(r["binding_class"]), "binding_no_injected": int(r["binding_no_injected"]),
            "binding_class_no_injected": int(r["binding_class_no_injected"]),
            "pre_positions": int(r["pre_positions"]),
            "class_positions": num(cls.get((r["chain_id"], r["cp"], r["type"], r["signature"]))),
            # the chain's mean bindings per run over its earlier checkpoints (formation, PLAN.md 5)
            "prior_binding_mean": prior.get((r["chain_id"], cp)),
        })
    return out


def by_rows(run_rows: list[dict], outcomes: list[dict] | None = None) -> list[dict]:
    """Every run of added logic (moved code left out) with its bystanders. ``pulled`` marks the
    runs that need at least one pre-existing value: H1 and H4 are read on those. ``place_class``
    and ``place_method`` name the class and the method the run is in, followed across renames and
    moves (the identities of ``tables.outcome_rows``), for H1's slopes within a place."""
    where = {(o["chain_id"], str(o["cp"]), o["type"], o["signature"]): o for o in outcomes or []}
    out = []
    for r in run_rows:
        if truth(r.get("replacement")) or r.get("bystanders") in (None, ""):
            continue
        o = where.get((r["chain_id"], str(r["cp"]), r.get("type"), r.get("signature")), {})
        cls = o.get("class_identity") or r.get("type", "")
        out.append({"chain_id": r["chain_id"], "arm": r["arm"], "frontend": r.get("frontend", ""),
                    "cp": int(r["cp"]), "host_new": truth(r["host_new"]),
                    "pulled": int(r["need"]) > 0,
                    "place_class": f"{r['chain_id']}|{cls}",
                    "place_method": f"{r['chain_id']}|{o.get('identity') or (str(r.get('type', '')) + '#' + str(r.get('signature', '')))}",
                    **{k: int(r[k]) for k in ("bystanders", "by_method", "by_class",
                                               "bystanders_no_injected", "bystanders_no_constants",
                                               "need")}})
    return out


def capture_rows(additions: list[dict]) -> list[dict]:
    """Per addition: the share of its positions landing in existing hosts, and the fields (state,
    injected dependencies and constants) of the chain's heaviest class at k − 1."""
    out = []
    for a in additions:
        if a.get("share_in_existing") in (None, "", "None") or a.get("heaviest_class") in (None, ""):
            continue
        out.append({"chain_id": a["chain_id"], "arm": a["arm"], "frontend": a.get("frontend", ""),
                    "cp": int(a["cp"]), "share_in_existing": float(a["share_in_existing"]),
                    "heaviest_class": int(a["heaviest_class"]),
                    "fields_added": int(a.get("fields_added") or 0)})
    return out


def reopen_rows(additions: list[dict]) -> list[dict]:
    """Per checkpoint: the classes its bound code goes back into and the wiring files it changes
    again (reported)."""
    return [{"chain_id": a["chain_id"], "arm": a["arm"], "frontend": a.get("frontend", ""),
             "cp": int(a["cp"]), "reopened": int(a["reopened"]),
             "reopened_classes": int(a["reopened_classes"]), "reopened_wiring": int(a["reopened_wiring"])}
            for a in additions if a.get("reopened") not in (None, "")]


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
            # intrusion at the class and the method (the placement) and, for information, on the
            # problem's own lines (PLAN.md 4.4)
            "bound": truth(o.get("bound", int(o["binding"]) >= 1)),
            "intrusion_class": int(o["intrusion_class"]), "intrusion_method": int(o["intrusion_method"]),
            "intrusion_class_any": int(o.get("intrusion_class_any", o["intrusion_class"])),
            "intrusion_method_any": int(o.get("intrusion_method_any", o["intrusion_method"])),
            "intrusion_lines": num(o.get("intrusion_lines")),
            # H2: what stood by where the code was placed, and the later intrusions bound to it
            "bystanders_class": int(o.get("bystanders_class") or 0),
            "bystanders_method": int(o.get("bystanders_method") or 0),
            "drawn_class": int(o.get("drawn_class") or 0), "drawn_method": int(o.get("drawn_method") or 0),
            "own_lines": num(o.get("own_lines")), "own_lost": num(o.get("own_lost")),
            "later_checkpoints": int(o["later_checkpoints"]),
            "binding": int(o["binding"]), "binding_no_param": int(h.get("binding_no_param", o["binding"])),
            "binding_no_injected": int(h.get("binding_no_injected", o["binding"])),
            "net_added": int(o["net_added"]),
            "addition_positions": size.get((o["chain_id"], o["cp"]), int(o["net_added"])),
            "declared_crossings": len(set(s.get("crosses", [])) | set(s.get("mutates", []))),
            "pre_positions": int(o["pre_positions"]), "host_new": truth(o["host_new"]),
            # the class's size at k - 1, where the host existed (the size-or-data reading)
            "class_positions": num(h.get("s5_class_positions")),
            "shape_found": truth(h.get("shape_found")),
        }
        for c in SHAPE_FLAGS + SINEW_FLAGS + ["s3_junction_injection_aware"]:
            row[c] = truth(h.get(c)) if h.get("shape_found") == "True" else None
        # the literature's shape measures, of the method (existing hosts) and of its class
        for c, (_, kind, _) in literature.MEASURES.items():
            v = h.get(c)
            row[c] = (None if v in (None, "", "None") else truth(v)) if kind == "flag" else num(v)
        row["c_positions"] = num(h.get("c_positions"))
        row["c_gini"] = num(h.get("c_gini"))
        row["class_identity"] = o.get("class_identity") or o.get("type")
        row["s4_cognitive"] = num(h.get("s4_cognitive"))
        row["s5_class_gini"] = num(h.get("s5_class_gini"))
        out.append(row)
    return out


def shape_kept(h2: list[dict], measures: list[str] | None = None) -> tuple[list[str], dict]:
    """The variation rule (PLAN.md §5): a shape measure flagged (or, for a level, non-zero) on
    fewer than MIN_FLAGGED existing hosts in any arm leaves the H3 block."""
    rows = [r for r in h2 if not r["host_new"] and r["shape_found"] and r["bound"]]
    arms = sorted({r["arm"] for r in rows})
    counts, kept = {}, []
    for c in measures or (SHAPE_FLAGS + SHAPE_LEVELS):
        per = {a: sum(1 for r in rows if r["arm"] == a and r[c]) for a in arms}
        counts[c] = per
        if arms and min(per.values()) >= MIN_FLAGGED:
            kept.append(c)
    return kept, counts


def literature_kept(h2: list[dict]) -> tuple[dict, dict]:
    """The literature's measures that can be read (PLAN.md §4.7a), by the variation rule of H3: a
    flag set, or a level above zero, on at least MIN_FLAGGED bound rows in every arm. Method
    measures are read on existing hosts, class measures on hosts of classes that existed."""
    arms = sorted({r["arm"] for r in h2})
    kept, counts = {}, {}
    for c, (level, kind, source) in {**FIRST, **literature.MEASURES}.items():
        rows = [r for r in h2 if r["bound"] and r.get(c) is not None
                and (level == "class" or (not r["host_new"] and r["shape_found"]))]
        per = {a: sum(1 for r in rows if r["arm"] == a and r[c]) for a in arms}
        varies = len({r[c] for r in rows}) > 1
        counts[c] = per
        if arms and varies and min(per.values()) >= MIN_FLAGGED:
            kept[c] = {"level": level, "kind": kind, "source": source,
                       "reversed": c in literature.REVERSED}
    return kept, counts


def amount(additions: list[dict], seed: int = SEED, resamples: int = 10_000) -> dict:
    """H4's amount band, read on the **amount added**: each chain's positions at its final
    checkpoint less those of its base (PLAN.md §4.6); the ratio of the function arm's mean to the
    methods arm's, with a bootstrap interval (chains resampled within arm). The ratio of the totals
    is reported beside it (``ratio_total``)."""
    final: dict[str, tuple[int, str, float, float]] = {}
    for a in additions:
        cp = int(a["cp"])
        if a["chain_id"] not in final or cp > final[a["chain_id"]][0]:
            total = float(a["amount_positions"])
            added = float(a["amount_added"]) if a.get("amount_added") not in (None, "") else total
            final[a["chain_id"]] = (cp, a["arm"], added, total)
    by_arm: dict[str, list[float]] = {}
    totals: dict[str, list[float]] = {}
    for _, arm, v, t in final.values():
        by_arm.setdefault(arm, []).append(v)
        totals.setdefault(arm, []).append(t)
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
            "per_arm": {k: statistics.fmean(v) for k, v in by_arm.items()},
            "ratio_total": statistics.fmean(totals[FUNCTION_ARM]) / statistics.fmean(totals[METHODS_ARM]),
            "per_arm_total": {k: statistics.fmean(v) for k, v in totals.items()}}


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
    run_rows = gather(name, "runs", measured_root)
    h1 = h1_rows(run_rows, hosts, streamed)
    additions = gather(name, "additions", measured_root)
    outcomes = gather(name, "outcomes", measured_root)
    h2 = h2_rows(outcomes, hosts, additions, streamed)
    kept, counts = shape_kept(h2)
    sinew, sinew_counts = shape_kept(h2, SINEW_FLAGS)
    lit, lit_counts = literature_kept(h2)
    chains: dict[str, set] = {}
    for a in additions:
        chains.setdefault(a["arm"], set()).add(a["chain_id"])
    out = out_root / name
    write_csv(out / "h1.csv", h1)
    by = by_rows(run_rows, outcomes)
    write_csv(out / "by.csv", [r for r in by if r["pulled"]])
    captured = capture_rows(additions)
    write_csv(out / "capture.csv", captured)
    again = reopen_rows(additions)
    write_csv(out / "reopen.csv", again)
    write_csv(out / "h2.csv", h2)
    spec = {"analysis": name, "role": analysis["role"], "seed": SEED, "boot": BOOT,
            "margin": MARGIN, "methods_arm": METHODS_ARM, "function_arm": FUNCTION_ARM,
            "shape_kept": kept, "shape_counts": {**counts, **sinew_counts}, "sinew_kept": sinew,
            "literature": lit, "literature_counts": lit_counts,
            "h3_measures": [k for k in H3_MEASURES if k in lit], "h3_all": H3_MEASURES, "reach": REACH, "checkpoints": len(streamed),
            "acts": any(r["act"] is not None for r in h1 + h2),
            "frontends": sorted({r["frontend"] for r in h1 if r["frontend"]})}
    conditions = {"chains": {k: len(v) for k, v in chains.items()},
                  "descriptive_only": analysis["role"] == "development"
                  or any(len(v) < MIN_CHAINS for v in chains.values()) or len(chains) < 2,
                  "amount": amount(additions), "wiring": wiring_checks(additions)}
    # the readings reported beside the hypotheses (PLAN.md 5): choice at a checkpoint, formation
    full = all(k in (additions[0] if additions else {}) for k in ("hosts", "hosts_existing", "binding_method"))
    chosen = readings.choice(additions, hosts) if full else []
    write_csv(out / "choice.csv", chosen)
    lost = {arm: {"lines": sum(r["own_lines"] or 0 for r in h2 if r["arm"] == arm),
                  "lost": sum(r["own_lost"] or 0 for r in h2 if r["arm"] == arm)}
            for arm in sorted({r["arm"] for r in h2})}
    (out / "readings.json").write_text(json.dumps({
        "choice": readings.choice_summary(chosen),
        "formation_end": readings.formation_end(run_rows, additions, len(streamed)) if streamed else {},
        "bystanders": readings.bystander_summary(by, captured, len(streamed)),
        "reopening": readings.reopening_summary(again),
        "drawn": readings.drawn_summary(h2),
        "landings": places.summary(gather(name, "landings", measured_root)),
        "own_lines": lost}, indent=1) + "\n")
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

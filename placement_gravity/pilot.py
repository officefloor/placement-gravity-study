"""The pilot (PLAN.md §8, step 2): the instrument on two chains, to check that the measures compute
and are not degenerate. It is not a test of H1–H3, and its chains are excluded from registration.

    python -m placement_gravity.pilot --out results/pilot
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path

from . import chain, crosscheck, tables

HOME = Path.home()
HARNESS = HOME / "spring-petclinic-rest-long-degradation-test"
RUN = "blind-202608100006"
STRATEGY = "just-solve"
CHAIN = "chain9"
ARMS = {
    "spring": (HOME / "compare" / "spring", "spring-compare-no-tests"),
    "officefloor": (HOME / "compare" / "officefloor", "officefloor-compare-no-tests"),
}


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        if not rows:
            f.write("")
            return
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def quantiles(xs: list[float]) -> dict:
    xs = sorted(xs)
    if not xs:
        return {"n": 0}
    q = lambda p: xs[min(len(xs) - 1, int(p * (len(xs) - 1) + 0.5))]
    return {"n": len(xs), "min": xs[0], "p25": q(0.25), "median": q(0.5), "p75": q(0.75),
            "p90": q(0.9), "max": xs[-1], "mean": round(statistics.fmean(xs), 3)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=chain.ROOT / "results" / "pilot")
    ap.add_argument("--work", type=Path, default=chain.ROOT / ".tmp" / "pilot")
    a = ap.parse_args()
    streamed = tables.stream(HARNESS / "checkpoints.yaml")
    hosts, runs, classes, adds, outs, summary = [], [], [], [], [], {}
    for arm, (repo, base) in ARMS.items():
        branch = f"evolve/{RUN}/{STRATEGY}/{arm}/{CHAIN}"
        measured = chain.measure(repo, branch, base, a.work / arm)
        h = tables.host_rows(arm, CHAIN, measured)
        r = tables.run_rows(arm, CHAIN, measured)
        cl = tables.class_rows(arm, CHAIN, h, measured)
        ad = tables.addition_rows(arm, CHAIN, measured, h, streamed)
        o = tables.outcome_rows(arm, CHAIN, h, streamed)
        hosts += h; runs += r; classes += cl; adds += ad; outs += o
        cc = crosscheck.crosscheck(repo, measured, h, a.work / arm)
        (a.out / f"codetracker-{arm}.json").parent.mkdir(parents=True, exist_ok=True)
        (a.out / f"codetracker-{arm}.json").write_text(json.dumps(cc, indent=1) + "\n")
        real = [x for x in h if x["net_added"] > 0 and not x["replacement"]]
        ex = [x for x in r if not x["host_new"]]
        new = [x for x in real if x["host_new"]]
        dist = lambda xs: {str(k): sum(1 for x in xs if x == k) for k in sorted(set(xs))}
        summary[arm] = {
            "branch": branch,
            "head": chain.git(repo, "rev-parse", branch).strip(),
            "checkpoints": len(measured["checkpoints"]),
            "noops": sum(1 for c in measured["checkpoints"] if c["noop"]),
            "problems": sum(1 for x in measured["records"] if x["kind"] == "problem"),
            "refactorings": sum(len(f["refactorings"]) for f in measured["refactorings"]),
            "hints": measured["hints"],
            "hints_naming_a_file_not_in_the_addition": measured["hints_unmatched"],
            "positions_moved_rm": sum(x["moved_rm"] for x in h),
            "positions_moved_text": sum(x["moved_text"] for x in h),
            "replacements": sum(1 for x in h if x["replacement"]),
            "hosts_with_addition": len(real),
            "hosts_new": len(new),
            "hosts_new_in_new_class": sum(1 for x in new if x["class_new"]),
            "hosts_existing": len(real) - len(new),
            "hosts_injected": sum(1 for x in real if x["injected"]),
            "share_positions_in_existing": quantiles([x["share_in_existing"] for x in ad
                                                      if x["share_in_existing"] is not None]),
            "hosts_per_addition": quantiles([x["hosts"] for x in ad]),
            "classes_per_addition": quantiles([x["classes"] for x in ad]),
            "host_pre_positions_existing": quantiles([x["pre_positions"] for x in real
                                                      if not x["host_new"]]),
            "runs_existing": len(ex),
            "runs_existing_edits": sum(1 for x in ex if x["edit"]),
            "run_tie_method_existing": dist([x["tie_method"] for x in ex]),
            "run_tie_class_existing": dist([x["tie_class"] for x in ex]),
            "run_tie_existing": dist([x["tie"] for x in ex]),
            "run_tok_tie_existing": dist([x["tok_tie"] for x in ex]),
            "run_utility_existing": dist([x["utility"] for x in ex]),
            "new_hosts_utility": dist([x["utility"] for x in new]),
            "new_hosts_tie": dist([x["tie"] for x in new]),
            "organisation_positions": sum(x["organisation"] for x in h),
            "runs_with_unresolved": sum(1 for x in r if x["unresolved"] > 0),
            "runs_total": len(r),
            "unresolved_names": sorted({v for x in r for v in x["unresolved_values"].split()}),
            # how many runs into existing hosts, and how many existing classes reached, are forced
            # at each cut (ties >= t)
            "forced_runs_existing_by_cut": {t: sum(1 for x in ex if x["tie"] >= t) for t in (1, 2, 3, 4)},
            "forced_runs_existing_by_cut_tokens": {t: sum(1 for x in ex if x["tok_tie"] >= t)
                                                   for t in (1, 2, 3, 4)},
            "forced_classes_existing_by_cut": {t: sum(1 for x in cl if not x["class_new"] and x["tie_class"] >= t)
                                               for t in (1, 2, 3, 4)},
            "classes_existing": sum(1 for x in cl if not x["class_new"]),
            "run_tie_existing_edits": dist([x["tie"] for x in ex if x["edit"]]),
            "run_tie_existing_insertions": dist([x["tie"] for x in ex if not x["edit"]]),
            "new_hosts_tie_class": dist([x["tie_class"] for x in new]),
            "new_hosts_birth_tie": dist([x["birth_tie"] for x in new]),
            "class_rows": len(cl),
            "class_tie_per_class_addition": dist([x["tie_class"] for x in cl]),
            "amount_first_last": [ad[0]["amount_positions"], ad[-1]["amount_positions"]] if ad else None,
            "wiring_nodes_added": sum(x["wiring_nodes_added"] for x in ad),
            "wiring_edges_added": sum(x["wiring_edges_added"] for x in ad),
            "outcome_rows": len(o),
            "outcomes_with_intrusion": sum(1 for x in o if x["intrusion"] > 0),
            "intrusion_per_100": quantiles([x["intrusion_per_100"] for x in o
                                            if x["intrusion_per_100"] is not None]),
            "declared_touches": sum(x["declared"] for x in o),
            "codetracker": {k: v for k, v in cc.items() if k != "per_method"},
        }
    write(a.out / "hosts.csv", hosts)
    write(a.out / "runs.csv", runs)
    write(a.out / "classes.csv", classes)
    write(a.out / "additions.csv", adds)
    write(a.out / "outcomes.csv", outs)
    (a.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

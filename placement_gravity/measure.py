"""Step 3: the instrument over every chain step 2 pinned (results/heads.tsv).

    python -m placement_gravity.measure [--analysis NAME ...] [--force]

For each chain not excluded: chain.measure at the pinned commit, the tables of PLAN.md §4 and the
shape series, and CodeTracker for the outcomes. Each chain's tables go to
results/measure/<analysis>/<arm>-<run>-chain<N>/, with meta.json naming the commit; a chain whose
meta.json already names the same commit and instrument version is skipped unless --force.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

from . import chain, crosscheck, lines, places, runs, shape, tables, validate

OUT = runs.RESULTS / "measure"
WORK = chain.ROOT / ".tmp" / "measure"
#: Bump when a table's meaning changes, so measured chains are redone.
MEASURE_VERSION = 42


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)


def chain_dir(head: dict) -> Path:
    return OUT / head["analysis"] / f"{head['arm']}-{head['run']}-chain{head['chain']}"


def label(rows: list[dict], head: dict) -> list[dict]:
    """Every row carries the chain's identity, so tables from many chains concatenate."""
    ident = {"analysis": head["analysis"], "frontend": head["frontend"], "run": head["run"],
             "strategy": head["strategy"],
             "chain_id": f"{head['arm']}/{head['run']}/chain{head['chain']}"}
    return [{**ident, **r} for r in rows]


def final_keys(work: Path) -> set[tuple[str, str, str]] | None:
    """The methods of the chain's last tree (crosscheck's listing), to tell a problem's lines that
    are still there from those lost track of."""
    listing = work / "head-methods.jsonl"
    if not listing.exists():
        return None
    return {(m["path"], m["type"], m["signature"])
            for m in (json.loads(l) for l in listing.read_text().splitlines() if l)}


def measure_chain(reg: dict, analysis: dict, head: dict, streamed: dict, stacks: dict,
                  force: bool = False) -> Path:
    out = chain_dir(head)
    meta = {"sha": head["sha"], "branch": head["branch"], "measure_version": MEASURE_VERSION}
    if not force and (out / "meta.json").exists() \
            and json.loads((out / "meta.json").read_text()) == meta:
        return out
    repo = reg["repos"][head["repo"]]
    paths = stacks.get(head["repo"]) or runs.roots(repo)
    work = WORK / head["analysis"] / out.name
    measured = chain.measure(repo["path"], head["sha"], repo["base_ref"], work,
                             paths["java_src"], paths["wiring_root"])
    name = f"chain{head['chain']}"
    arm = head["arm"]
    h = tables.host_rows(arm, name, measured)
    cc = crosscheck.crosscheck(repo["path"], measured, h, work)
    write(out / "hosts.csv", label(h, head))
    write(out / "runs.csv", label(tables.run_rows(arm, name, measured), head))
    write(out / "classes.csv", label(tables.class_rows(arm, name, h, measured), head))
    write(out / "additions.csv", label(tables.addition_rows(arm, name, measured, h, streamed), head))
    followed = lines.follow(measured["records"], final_keys(work))
    write(out / "outcomes.csv", label(tables.outcome_rows(arm, name, h, streamed, cc, followed), head))
    write(out / "pairs.csv", label(tables.pair_rows(arm, name, h, measured), head))
    write(out / "coupling.csv", label(tables.coupling_rows(arm, name, measured), head))
    write(out / "encapsulation.csv", label(tables.encapsulation_rows(arm, name, h, measured), head))
    write(out / "refactorings.csv", label(tables.refactoring_rows(arm, name, measured), head))
    write(out / "boundary.csv", label(tables.boundary_rows(arm, name, h, measured), head))
    write(out / "edges.csv", label(tables.edge_rows(arm, name, h, measured), head))
    write(out / "links.csv", label(tables.link_rows(arm, name, measured), head))
    write(out / "containers.csv", label(tables.container_rows(arm, name, h, measured), head))
    write(out / "members.csv", label(tables.member_rows(arm, name, measured), head))
    write(out / "files.csv", label(tables.file_rows(arm, name, measured), head))
    # the production Java files at the chain's head and their sizes (diagnostics, PLAN.md 6)
    tree = chain.git(repo["path"], "ls-tree", "-r", "-l", head["sha"], "--", paths["java_src"])
    write(out / "files_end.csv", label([{"arm": arm, "chain": name, "path": p, "bytes": int(b)}
                                        for b, p in (ln.split(None, 4)[3:5] for ln in tree.splitlines())
                                        if p.endswith(".java")], head))
    write(out / "landings.csv", label(places.landings(arm, name, h, measured["shape"]), head))
    write(out / "shape_series.csv", label(shape.series_rows(arm, name, measured["shape"]), head))
    # the instrument against the compiler, on a sample of the chain's checkpoints (PLAN.md 4.8)
    write(out / "validation.csv", label(validate.rows(arm, name, repo["path"], head["sha"], paths["java_src"],
                                                      measured, work), head))
    (out / "codetracker.json").write_text(json.dumps(
        {k: v for k, v in cc.items() if k not in ("ct_identity", "ct_touched")}, indent=1) + "\n")
    (out / "meta.json").write_text(json.dumps(meta, indent=1) + "\n")
    shutil.rmtree(work, ignore_errors=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", nargs="*")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    reg = runs.load()
    heads = runs.read_heads()
    stacks = json.loads(runs.STACKS.read_text()) if runs.STACKS.exists() else {}
    for analysis in reg["analyses"]:
        if a.analysis and analysis["name"] not in a.analysis:
            continue
        mine = [h for h in heads if h["analysis"] == analysis["name"] and not h["excluded"]]
        if not mine:
            continue
        runs.guard(reg, analysis)
        streamed = runs.streamed(reg, analysis)
        for head in mine:
            out = measure_chain(reg, analysis, head, streamed, stacks, a.force)
            print(f"{analysis['name']}: {out.name}")


if __name__ == "__main__":
    main()

"""CodeTracker for the methods that survive to the chain's end (PLAN.md §4.4), and its agreement
with the instrument's own following of hosts.

For every method the instrument saw an addition in and that still exists at the chain's last
checkpoint, CodeTracker 2.6 tracks the method back from that commit (through renames and moves of
the method and its class). The checkpoints it reports as changing the method's body are compared
with the checkpoints the instrument attributes to the same host identity.

``crosscheck`` also returns CodeTracker's identities for the outcomes: ``ct_identity`` maps a
host (checkpoint, simple class name, method name) to the surviving method it is a version of, and
``ct_touched`` gives each surviving method's body-changing checkpoints. Methods removed before the
end have no CodeTracker history; the instrument's own chaining covers them.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from . import chain, refactor, tables

#: CodeTracker change types that change what the method does (others: renames, moves, signature,
#: annotations, modifiers, documentation).
BODY = {"INTRODUCED", "BODY_CHANGE", "CATCH_BLOCK_CHANGE", "CATCH_BLOCK_ADDED", "CATCH_BLOCK_REMOVED",
        "FINALLY_BLOCK_CHANGE", "FINALLY_BLOCK_ADDED", "FINALLY_BLOCK_REMOVED", "BLOCK_SPLIT",
        "METHOD_SPLIT", "METHOD_MERGE", "REPLACE_PIPELINE_WITH_LOOP", "REPLACE_LOOP_WITH_PIPELINE",
        "EXPRESSION_CHANGE"}
RENAMES = {"RENAME", "MOVED", "CONTAINER_CHANGE"}


def crosscheck(repo: Path, measured: dict, hosts: list[dict], work: Path) -> dict:
    cps = [c for c in measured["checkpoints"] if not c["noop"]]
    head = cps[-1]
    cp_of = {c["commit"]: c["cp"] for c in cps}
    last_tree = work / f"cp{head['cp']:02d}" / "tree"
    listing_methods = work / "head-methods.jsonl"
    subprocess.run(["java", "-cp", chain.CLASSPATH, "Pull", "--methods", str(last_tree),
                    str(listing_methods)], check=True)
    heads = [json.loads(l) for l in listing_methods.read_text().splitlines() if l]

    ident = tables.identities(hosts)
    latest: dict[tuple[str, str], str] = {}
    for h in sorted(hosts, key=lambda h: h["cp"]):
        latest[(h["type"], h["name"])] = ident[(h["cp"], h["type"], h["name"])]
    ours: dict[str, set[int]] = {}
    for h in hosts:
        if h["net_added"] > 0 or h["removed"] > 0:
            ours.setdefault(ident[(h["cp"], h["type"], h["name"])], set()).add(h["cp"])

    rows, seen = [], set()
    for m in heads:
        i = latest.get((m["type"], m["name"]))
        if i is None or (m["type"], m["name"]) in seen:
            continue  # never an addition's host, or an overload already listed
        seen.add((m["type"], m["name"]))
        rows.append((i, m))
    listing = work / "histories.tsv"
    listing.write_text("".join(f"{n}\t{head['commit']}\t{m['path']}\t{m['name']}\t{m['decl_line']}\n"
                               for n, (i, m) in enumerate(rows)))
    out = work / "histories.jsonl"
    cp = f"{refactor.MODULE / 'target' / 'classes'}:{refactor.MODULE / 'target' / 'lib'}/*"
    subprocess.run(["java", "-cp", cp, "Histories", str(repo), str(listing), str(out)],
                   check=True, capture_output=True)
    results = [json.loads(l) for l in out.read_text().splitlines() if l]

    per = []
    errors = 0
    ct_identity: dict[tuple[int, str, str], str] = {}
    ct_touched: dict[str, set[int]] = {}
    for res in results:
        i, m = rows[int(res["id"])]
        if "error" in res:
            errors += 1
            continue
        ct = {cp_of[c["commit"]] for c in res["changes"]
              if c["commit"] in cp_of and BODY & set(c["types"])}
        cid = f"ct:{m['type']}#{m['name']}"
        ct_touched[cid] = ct
        for c in res["changes"]:
            if c["commit"] in cp_of and c.get("name"):
                ct_identity[(cp_of[c["commit"]], simple(c["class"]), c["name"])] = cid
        renamed = any(c["commit"] in cp_of and RENAMES & set(c["types"]) for c in res["changes"])
        mine = ours.get(i, set())
        per.append({"identity": i, "type": m["type"], "name": m["name"], "codetracker": sorted(ct),
                    "instrument": sorted(mine), "both": len(ct & mine),
                    "codetracker_only": sorted(ct - mine), "instrument_only": sorted(mine - ct),
                    "renamed_or_moved": renamed})
    both = sum(p["both"] for p in per)
    ct_total = sum(len(p["codetracker"]) for p in per)
    mine_total = sum(len(p["instrument"]) for p in per)
    return {
        "methods": len(rows), "errors": errors, "compared": len(per),
        "checkpoints_codetracker": ct_total, "checkpoints_instrument": mine_total, "agree": both,
        "share_of_codetracker_found_by_instrument": round(both / ct_total, 3) if ct_total else None,
        "share_of_instrument_confirmed_by_codetracker": round(both / mine_total, 3) if mine_total else None,
        "methods_identical": sum(1 for p in per if not p["codetracker_only"] and not p["instrument_only"]),
        "methods_renamed_or_moved": sum(1 for p in per if p["renamed_or_moved"]),
        "methods_renamed_or_moved_identical": sum(1 for p in per if p["renamed_or_moved"]
                                                  and not p["codetracker_only"]
                                                  and not p["instrument_only"]),
        "per_method": per,
        "ct_identity": ct_identity,
        "ct_touched": ct_touched,
    }


def simple(type_name: str) -> str:
    """The last segment of a type name, so CodeTracker's and the instrument's names compare."""
    return type_name.replace("$", ".").split(".")[-1]

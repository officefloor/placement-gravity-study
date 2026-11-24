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
  it is bound to what stood by, what the change introduced there (§4.3b), the problem's own lines, the problem's size and declared crossings,
  the host's size and its shape at k − 1.
- ``h6.csv``: one row per unit that placed or edited code, with the classes it did so in and
  whether a placement in it was forced at the class (H6, PLAN.md §4.2b); ``pairs.csv``: one row
  per unit and pair of classes it changed together, with the calls between them before it.
- ``h7.csv``: one row per checkpoint and chain, the links between blocks of logic it added (call,
  state, flow) and the logic it added (H7, surface against volume, PLAN.md §4.2c, restated 24
  November 2026). Corpus A only.
- ``calls_across.csv``: one row per unit and existing class it changed, with the calls across the
  class's boundary the unit added, by the member they reach (already open, exposed, widened), and
  whether a placement in the class was forced (PLAN.md §4.2c): H8's dispersion, and the reader
  reading. (The old H7, *forced changes couple*, was read on it until it was deleted on 24 November
  2026.)
- ``surface.csv``: one row per class a unit changed, its volume (methods, positions) and surface
  (calls out and in) before and after, and per class of each chain's last tree (PLAN.md §4.2e).
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

from . import chain, history, literature, places, readings, runs, tables, validate, wiring

DATA = chain.ROOT / "data" / "analysis"
SEED = 20261116
#: Cluster-bootstrap refits for H1 and for the confirmatory tests (H2, H4, H5, H7; PLAN.md §5).
BOOT = 1000
#: On a history (corpora B and C), which is read for direction and interval only and whose models
#: are hundreds of times larger: fewer refits, the Wald interval beside each (PLAN.md §5).
BOOT_HISTORY = 200
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
#: H3's sensitivity reading (22 November 2026): its measures with the literature's coupling measures
#: put back, as the literature reads them among its shape metrics (Chidamber and Kemerer's CBO and
#: RFC, fan-out).
H3_SENSITIVITY = H3_MEASURES + ["m_fanout", "c_cbo", "c_rfc", "c_fanout"]
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


def h5_rows(host_rows: list[dict], streamed: dict) -> list[dict]:
    """Choice (H5, PLAN.md 4.2a): one row per bound host and level (class, method) where the
    alternatives were counted: the other places in the tree before the checkpoint that hold what the
    code was bound to there; at the method, on the host's control flow (the count over the whole
    tree, by type alone, beside it). On a history the index is the unit's place from 0 to 1."""
    out = []
    for h in host_rows:
        if truth(h.get("replacement")):
            continue
        cp = float(h["position"]) if h.get("position") not in (None, "") else int(h["cp"])
        for level in ("class", "method"):
            n = num(h.get(f"choice_{level}"))
            if n is None:
                continue
            out.append({
                "chain_id": h["chain_id"], "arm": h["arm"], "frontend": h.get("frontend", ""),
                "cp": cp, "act": streamed.get(int(h["cp"]), {}).get("act"), "level": level,
                "alternatives": int(n), "forced": int(n) == 0,
                "own": truth(h.get("choice_class_own")) if level == "class" else None,
                "untyped": int(num(h.get("choice_method_untyped"), 0)) if level == "method" else None,
                "by_type": num(h.get("choice_method_by_type")) if level == "method" else None,
                "flow_methods": num(h.get("choice_flow_methods")) if level == "method" else None,
                "calls_to_app_names": num(h.get("calls_to_app_names")) if level == "method" else None,
                "calls_followed": num(h.get("calls_followed")) if level == "method" else None,
                "places": h.get(f"choice_{level}_places", ""),
            })
    return out


def h5_forced_rows(h5: list[dict], additions: list[dict]) -> list[dict]:
    """H5's arm contrast (24 November 2026, PLAN.md 9 row 92): per checkpoint and chain, the
    placements bound at the class with no other place to go (forced, H5's), zero where there were
    none. Every checkpoint that did something counts, so a form that binds less often scores
    lower; no-op checkpoints are left out. Corpus A only."""
    n: dict[tuple, int] = {}
    for r in h5:
        if r["level"] == "class" and r["forced"]:
            k = (r["chain_id"], int(r["cp"]))
            n[k] = n.get(k, 0) + 1
    return [{"chain_id": a["chain_id"], "arm": a["arm"], "frontend": a.get("frontend", ""), "cp": int(a["cp"]),
             "forced_class": n.get((a["chain_id"], int(a["cp"])), 0)}
            for a in additions if not truth(a.get("noop"))]


def added(h: dict) -> float:
    """The positions a host gained (its net addition, none below 0): the size of a change there."""
    return max(num(h.get("net_added"), 0) or 0, 0)


def h6_rows(host_rows: list[dict], streamed: dict) -> list[dict]:
    """Change spread (H6, PLAN.md 4.2b): one row per unit that placed or edited code in a class that
    existed before it, with the number of such classes (``spread`` is those beyond the first; a
    new class is a free choice, so it is counted beside, not in the spread) and whether any of its
    placements was forced by encapsulation (bound to a member of the class no other class can reach,
    ``tables.encapsulated``), or bound at the class only to reachable members (``chosen``); whether
    one was forced by binding with no alternative (``forced_bind``, H5's class level); and the change's size, the positions it
    added (``positions``) and the methods it placed or edited code in (``methods``), so that forced
    is compared with unforced at the same size (decided 20 November 2026)."""
    units: dict[tuple, dict] = {}
    for h in host_rows:
        if not tables.changed(h):
            continue
        u = units.setdefault((h["chain_id"], int(h["cp"])), {
            "chain_id": h["chain_id"], "arm": h["arm"], "frontend": h.get("frontend", ""),
            "cp": float(h["position"]) if h.get("position") not in (None, "") else int(h["cp"]),
            "act": streamed.get(int(h["cp"]), {}).get("act"), "unit": int(h["cp"]),
            "existing": set(), "all": set(), "forced": set(), "chosen": set(), "bind": set(), "positions": 0, "methods": 0})
        u["positions"] += added(h)
        u["methods"] += 1
        c = h.get("before_type") or h["type"]
        u["all"].add(c)
        if not truth(h.get("class_new")):
            u["existing"].add(c)
        f = tables.forced(h)
        if f is not None:
            (u["forced"] if f else u["chosen"]).add(c)
        n = num(h.get("choice_class"))
        if n is not None and int(n) == 0:
            u["bind"].add(c)
    return [{**{k: v for k, v in u.items() if k not in ("existing", "all", "forced", "chosen", "bind")},
             "forced_bind": bool(u["bind"]),
             "classes": len(u["existing"]), "spread": len(u["existing"]) - 1,
             "all_classes": len(u["all"]), "new_classes": len(u["all"] - u["existing"]),
             "forced": bool(u["forced"]), "forced_classes": len(u["forced"]),
             "chosen": bool(u["chosen"]), "class_names": " ".join(sorted(u["existing"]))}
            for _, u in sorted(units.items()) if u["existing"]]


def pair_rows(pairs: list[dict]) -> list[dict]:
    """The coupling of classes changed together (H6, reported): one row per unit and pair of
    classes that both existed before it, the calls between them in the tree before the unit and
    what the unit added (after less before; none for the last unit), with the number of times the
    pair has been changed together in its chain so far."""
    out, seen = [], {}
    for p in sorted(pairs, key=lambda r: (r["chain_id"], int(r["cp"]))):
        if int(num(p.get("new"), 0)):
            continue
        key = (p["chain_id"], p["class_a"], p["class_b"])
        seen[key] = seen.get(key, 0) + 1
        before = int(p["calls_ab"]) + int(p["calls_ba"])
        after = (None if num(p.get("calls_ab_after")) is None
                 else int(num(p["calls_ab_after"])) + int(num(p["calls_ba_after"])))
        out.append({"chain_id": p["chain_id"], "arm": p["arm"], "frontend": p.get("frontend", ""),
                    "cp": float(p["position"]) if p.get("position") not in (None, "") else int(p["cp"]),
                    "unit": int(p["cp"]),
                    "pair": f"{p['chain_id']}|{p['class_a']}|{p['class_b']}",
                    "coupling": before, "added": None if after is None else after - before,
                    "times": seen[key], "in_tree": truth(p["in_tree"])})
    return out


def growth_accounting(host_rows: list[dict], checkpoints: int) -> dict:
    """Where the growth of classes that existed came from (H6's accounting, PLAN.md 4.2b): per arm,
    and per third of the stream, the positions added to existing classes by placements forced at
    the class, by placements that had a choice there, and by code not bound at the class; and
    each one's share."""
    span = max(checkpoints - 1, 1)
    out: dict[str, dict] = {}
    for h in host_rows:
        if not tables.changed(h) or truth(h.get("class_new")):
            continue
        f = tables.forced(h)
        kind = "unbound" if f is None else "forced" if f else "chosen"
        x = float(h["position"]) if h.get("position") not in (None, "") else (int(h["cp"]) - 1) / span
        third = str(min(int(x * 3) + 1, 3))
        added = max(num(h.get("net_added"), 0) or 0, 0)
        a = out.setdefault(h["arm"], {"positions": {}, "thirds": {}})
        for d in (a["positions"], a["thirds"].setdefault(third, {})):
            d[kind] = d.get(kind, 0) + added
    for a in out.values():
        for d in [a["positions"], *a["thirds"].values()]:
            total = sum(d.get(k, 0) for k in ("forced", "chosen", "unbound"))
            d["total"] = total
            for k in ("forced", "chosen", "unbound"):
                d[f"{k}_share"] = d.get(k, 0) / total if total else None
    return out


def growth_by_access(host_rows: list[dict]) -> dict:
    """Per arm, the positions added to classes that existed by the strictest access of the members
    the code was bound to at the class (private, package, protected, public), or not bound there,
    and each one's share: private is the encapsulation that forces; package and protected are a
    looser encapsulation, reported descriptively (decided by the author on 22 November 2026)."""
    out: dict[str, dict] = {}
    for h in host_rows:
        if not tables.changed(h) or truth(h.get("class_new")):
            continue
        k = h.get("bound_access") or "unbound"
        a = out.setdefault(h["arm"], {})
        a[k] = a.get(k, 0) + added(h)
    for a in out.values():
        total = sum(v for v in a.values())
        a["total"] = total
        for k in [k for k in a if k != "total"]:
            a[f"{k}_share"] = a[k] / total if total else None
    return out


def growth_by_lever(host_rows: list[dict]) -> dict:
    """Per arm, the positions that placements forced by encapsulation added to classes that existed,
    by whether the lever of injection was there (``tables.lever``, decided by the author on 22
    November 2026): bound to the class's own private members (``own``); bound only to injected
    private fields, with another class already holding those dependencies (``injected_elsewhere``,
    H5's alternatives at least one) or with none yet (``injected_only_here``). The injected part is
    the opportunity dependency injection gives to duplicate the core and avoid the concentration; it
    is still forced, because the lever was not exercised. Shares are of the forced growth, with the
    forced growth's share of all growth of existing classes."""
    out: dict[str, dict] = {}
    for h in host_rows:
        if not tables.changed(h) or truth(h.get("class_new")):
            continue
        a = out.setdefault(h["arm"], {"own": 0, "injected_elsewhere": 0, "injected_only_here": 0,
                                      "unknown": 0, "placements": 0, "all": 0})
        a["all"] += added(h)
        if not tables.forced(h):
            continue
        k = h.get("forced_lever")
        if k == "injected":
            n = num(h.get("choice_class"))
            k = "injected_elsewhere" if n is not None and n >= 1 else "injected_only_here"
        elif k != "own":
            k = "unknown"           # measured before the lever was read
        a[k] += added(h)
        a["placements"] += 1
    for a in out.values():
        kinds = ("own", "injected_elsewhere", "injected_only_here", "unknown")
        total = sum(a[k] for k in kinds)
        a["forced"] = total
        a["forced_share_of_growth"] = total / a["all"] if a["all"] else None
        for k in kinds:
            a[f"{k}_share"] = a[k] / total if total else None
        a["opportunity_share"] = ((a["injected_elsewhere"] + a["injected_only_here"]) / total) if total else None
    return out


def compliance(members: list[dict], arm: str) -> dict:
    """Run D's condition (PLAN.md §3.1a): of the fields and methods the open arm's units introduce,
    the share that is not private, over all its chains."""
    n = sum(int(num(m.get("introduced"), 0)) for m in members if m["arm"] == arm)
    private = sum(int(num(m.get("introduced_private"), 0)) for m in members if m["arm"] == arm)
    return {"arm": arm, "introduced": n, "private": private, "share": (n - private) / n if n else None}


def coupling_accounting(pairs: list[dict], coupling: list[dict], h6: list[dict]) -> dict:
    """What coupling between classes each unit added (H6's accounting, PLAN.md 4.2b): per arm, the
    calls between classes the units added in all (the tree after less the tree before, over every
    class), how much of that between pairs of existing classes changed together, and how much in
    units with a forced placement and in the others."""
    forced = {(r["chain_id"], int(r["unit"])): truth(r["forced"]) for r in h6}
    out: dict[str, dict] = {}

    def acc(arm):
        return out.setdefault(arm, {"added": 0, "added_forced_units": 0, "added_unforced_units": 0,
                                    "pairs_added": 0, "pairs_added_forced": 0, "pairs_added_unforced": 0,
                                    "units": 0})
    for c in coupling:
        if num(c.get("cross_class_calls_after")) is None:
            continue
        d = int(num(c["cross_class_calls_after"])) - int(num(c["cross_class_calls"]))
        a = acc(c["arm"])
        a["units"] += 1
        a["added"] += d
        f = forced.get((c["chain_id"], int(c["cp"])))
        if f is not None:
            a["added_forced_units" if f else "added_unforced_units"] += d
    for p in pairs:
        if p["added"] is None or not p["in_tree"]:
            continue
        a = acc(p["arm"])
        a["pairs_added"] += p["added"]
        f = forced.get((p["chain_id"], p["unit"]))
        if f is not None:
            a["pairs_added_forced" if f else "pairs_added_unforced"] += p["added"]
    for a in out.values():
        t = a["added"]
        a["share_forced_units"] = a["added_forced_units"] / t if t else None
        a["share_between_pairs"] = a["pairs_added"] / t if t else None
        a["share_pairs_forced"] = a["pairs_added_forced"] / t if t else None
    return out


def co_change(pairs: list[dict], top: int = 10) -> dict:
    """Per arm: the pairs of classes changed together, how many were changed together more than
    once, and of those how many are more coupled after their last change together than before
    their first (both in the tree); the pairs most often changed together whose coupling rose, the candidates
    for redistributing placement between the two (PLAN.md 4.2b)."""
    by: dict[str, list[dict]] = {}
    for p in pairs:
        by.setdefault(p["pair"], []).append(p)
    out: dict[str, dict] = {}
    for rows in by.values():
        rows.sort(key=lambda r: r["cp"])
        arm = rows[0]["arm"]
        a = out.setdefault(arm, {"pairs": 0, "again": 0, "rose": 0, "fell": 0, "candidates": []})
        a["pairs"] += 1
        if len(rows) < 2:
            continue
        a["again"] += 1
        both = [r for r in rows if r["in_tree"]]
        if len(both) < 2:
            continue
        # coupling before the first change together, and after the last (where a tree follows it)
        first, last = both[0]["coupling"], both[-1]["coupling"] + (both[-1]["added"] or 0)
        a["rose"] += last > first
        a["fell"] += last < first
        if last > first:
            chain_id, x, y = rows[0]["pair"].split("|")
            a["candidates"].append({"chain_id": chain_id, "classes": [x, y], "times": len(rows),
                                    "coupling_first": first, "coupling_last": last})
    for a in out.values():
        a["candidates"] = sorted(a["candidates"], key=lambda c: (-c["times"], -c["coupling_last"]))[:top]
    return out


def h7_rows(links: list[dict], split: list[dict]) -> list[dict]:
    """Surface against volume (H7, PLAN.md 4.2c, restated 24 November 2026): per checkpoint and
    chain, the links between blocks of logic it added (``links_added``: call, state and flow, each
    counted once, injection not among them) and the logic it added (``logic_added``, the volume,
    from the logic and organisation reading, §4.9). Only checkpoints with both: the last has no tree
    after it, and a no-op checkpoint's lines are not read."""
    logic = {(r["chain_id"], int(r["cp"])): r for r in split}
    out = []
    for r in links:
        s = logic.get((r["chain_id"], int(r["cp"])))
        if s is None:
            continue
        row = {"chain_id": r["chain_id"], "arm": r["arm"], "frontend": r.get("frontend", ""), "cp": int(r["cp"]),
               "logic_added": int(s["logic_added"])}
        row.update({k: int(num(r.get(k), 0)) for k in (
            "links_added", "links_lost", "call_links_added", "state_links_added", "flow_links_added",
            "call_links_lost", "state_links_lost", "flow_links_lost", "call_links", "state_links",
            "flow_links", "methods")})
        out.append(row)
    return out


def links_summary(rows: list[dict], checkpoints: int) -> dict:
    """Per arm, the links added a checkpoint by kind and over the thirds of the stream, per unit of
    logic added, and the tree's links per method at the last checkpoint read (H7, reported beside)."""
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        rs = [r for r in rows if r["arm"] == arm]
        third = lambda r: min(3, 1 + 3 * (r["cp"] - 1) // max(checkpoints, 1))
        mean = lambda k, xs: statistics.fmean(r[k] for r in xs) if xs else None
        logic = sum(r["logic_added"] for r in rs)
        last = {}
        for r in rs:
            if r["cp"] >= last.get(r["chain_id"], {}).get("cp", -1):
                last[r["chain_id"]] = r
        ends = list(last.values())
        out[arm] = {"checkpoints": len(rs),
                    **{k: mean(k, rs) for k in ("links_added", "call_links_added", "state_links_added",
                                                 "flow_links_added", "links_lost", "logic_added")},
                    "thirds": {str(t): mean("links_added", [r for r in rs if third(r) == t]) for t in (1, 2, 3)},
                    "links_per_logic": sum(r["links_added"] for r in rs) / logic if logic else None,
                    "tree_links_per_method": statistics.fmean(
                        (r["call_links"] + r["state_links"] + r["flow_links"]) / r["methods"]
                        for r in ends if r["methods"]) if any(r["methods"] for r in ends) else None}
    return out


def calls_across_rows(enc: list[dict], host_rows: list[dict] | None = None) -> list[dict]:
    """Calls across the encapsulation (PLAN.md 4.2c; H8's dispersion): one row per unit and existing class it changed, with the
    calls across the class's boundary the unit added (``coupled``, outward and inward), how many of
    those reach a member the unit exposed or widened (``opened``), and whether the class had a
    placement forced at the class; and the change's size in the class, the positions it added there
    (``positions``) and the methods it placed or edited code in there (``methods``). The unit's last
    row has no tree after it and is not here."""
    size: dict[tuple, list] = {}
    for h in host_rows or []:
        if tables.changed(h):
            s = size.setdefault((h["chain_id"], int(h["cp"]), tables._type(h.get("before_type") or h["type"])), [0, 0])
            s[0] += added(h)
            s[1] += 1
    out = []
    for r in enc:
        n = {k: int(num(r.get(k), 0)) for k in (
            "new_out", "new_in", "lost_out", "lost_in", "out_existing", "out_exposed", "out_widened",
            "in_existing", "in_exposed", "in_widened", "members_opened")}
        out.append({"chain_id": r["chain_id"], "arm": r["arm"], "frontend": r.get("frontend", ""),
                    "cp": float(r["position"]) if r.get("position") not in (None, "") else int(r["cp"]),
                    "unit": int(r["cp"]), "class": r["class"], "forced": truth(r["forced"]),
                    "forced_bind": truth(r.get("forced_bind")),
                    "positions": size.get((r["chain_id"], int(r["cp"]), r["class"]), [0, 0])[0],
                    "methods": size.get((r["chain_id"], int(r["cp"]), r["class"]), [0, 0])[1],
                    "chosen": truth(r["chosen"]), **n,
                    "coupled": n["new_out"] + n["new_in"],
                    "opened": n["out_exposed"] + n["out_widened"] + n["in_exposed"] + n["in_widened"]})
    return out


#: Where a call across a class's boundary came from (PLAN.md 4.2c, row 88), in this order: the
#: problem's own coupling (it joins two classes whose private data the change needed), reuse of what
#: was already open, and the rest (a member the change opened, in a class whose data it did not need).
SOURCES = ("problem", "reuse", "other")


def call_source(e: dict) -> str:
    """Where one added call across a class's boundary came from (``SOURCES``)."""
    if truth(e["caller_forced"]) and truth(e["callee_forced"]):
        return "problem"
    return "reuse" if e["kind"] == "existing" else "other"


def coupling_source(h7: list[dict], edges: list[dict]) -> dict:
    """Is forced coupling the problem's own (PLAN.md 4.2c, row 88; the author, 23 November 2026)?
    Per arm, the class rows forced by encapsulation: how many added no call across the class's
    boundary (*contained*), how many added only calls of the problem or of reuse, and how many some
    of the rest; and the calls themselves by source, each counted once, with the unforced
    changes' calls beside (where the problem's own is nil by definition)."""
    from . import flow
    by_row: dict[tuple, list[str]] = {}
    calls: dict[str, dict[str, dict[str, int]]] = {}
    for e in edges:
        s = call_source(e)
        forced = truth(e["caller_forced"]) or truth(e["callee_forced"])
        g = calls.setdefault(e["arm"], {}).setdefault("forced" if forced else "unforced", dict.fromkeys(SOURCES, 0))
        g[s] += 1
        for c in {e["caller_class"], e["callee_class"]}:
            by_row.setdefault((e["chain_id"], int(e["cp"]), c), []).append(s)
    out: dict[str, dict] = {}
    for arm in sorted({r["arm"] for r in h7} | set(calls)):
        rows = [r for r in h7 if r["arm"] == arm and r["forced"]]
        kinds = [by_row.get((r["chain_id"], int(r["unit"]), flow.simple(r["class"])), []) for r in rows]
        contained = sum(1 for r in rows if not r["coupled"])
        explained = sum(1 for r, k in zip(rows, kinds) if r["coupled"] and k and "other" not in k)
        n = len(rows)
        out[arm] = {"rows": n, "contained": contained, "explained": explained,
                    "other": n - contained - explained,
                    "contained_share": contained / n if n else None,
                    "explained_share": explained / n if n else None,
                    "other_share": (n - contained - explained) / n if n else None,
                    "calls": calls.get(arm, {})}
    return out


def _values(h: dict) -> set[str]:
    """The class's own values a host's code was bound to: its fields and the class methods called."""
    return set((h.get("need_class_values") or "").split()) | set((h.get("called_class_methods") or "").split())


#: The sizes a system is split at against a context window (PLAN.md 4.2f; the drafter's choice,
#: 22 November 2026: the context windows common among coding agents when it was written).
CONTEXT_BANDS = (200_000, 1_000_000)
#: A band with fewer repositories (chains) than this for an author group is reported as too thin.
READER_FLOOR = 10


def band(tokens) -> str:
    t = num(tokens)
    if t is None:
        return ""
    return ("below 200k" if t < CONTEXT_BANDS[0] else
            "200k to 1M" if t < CONTEXT_BANDS[1] else "above 1M")


def reader_rows(members: list[dict], hosts: list[dict], h7: list[dict], boundary: list[dict],
                refactorings: list[dict]) -> tuple[list[dict], list[dict]]:
    """Encapsulation and the reader (PLAN.md 4.2f): one row per unit, with the members it
    introduced and how many are private (measure 1), the positions it added to classes that
    existed and how many of those by a placement forced at the class (measure 2), the classes it
    split (RefactoringMiner's Extract Class), its change size, and the system's tokens before it;
    and one row per unit and existing class it changed (H7's rows), with the members it exposed or
    widened there (measure 3) and the class's methods before it (measure 4)."""
    size: dict[tuple, dict] = {}
    for h in hosts:
        if not tables.changed(h):
            continue
        u = size.setdefault((h["chain_id"], int(h["cp"])), {"positions": 0, "methods": 0,
                                                             "existing": 0, "forced": 0})
        a = added(h)
        u["positions"] += a
        u["methods"] += 1
        if not truth(h.get("class_new")):
            u["existing"] += a
            if tables.forced(h):
                u["forced"] += a
    splits: dict[tuple, int] = {}
    for r in refactorings:
        if r.get("kind") == "Extract Class":
            k = (r["chain_id"], int(r["cp"]))
            splits[k] = splits.get(k, 0) + 1
    tokens: dict[tuple, float] = {}
    units = []
    for m in members:
        k = (m["chain_id"], int(m["cp"]))
        tokens[k] = num(m.get("system_tokens"))
        s = size.get(k)
        if s is None:            # a unit that changed no production method
            continue
        units.append({"chain_id": m["chain_id"], "arm": m["arm"], "unit": k[1],
                      "cp": float(m["position"]) if m.get("position") not in (None, "") else k[1],
                      "tokens": tokens[k], "band": band(tokens[k]),
                      "introduced": num(m.get("introduced")), "private": num(m.get("introduced_private")),
                      "existing_positions": round(s["existing"]), "forced_positions": round(s["forced"]),
                      "splits": splits.get(k, 0), "positions": s["positions"], "methods": s["methods"]})
    before = {(b["chain_id"], int(b["cp"]), b["class"]): num(b.get("methods_before")) for b in boundary}
    classes = []
    for r in h7:
        k = (r["chain_id"], r["unit"])
        t = tokens.get(k)
        classes.append({"chain_id": r["chain_id"], "arm": r["arm"], "unit": r["unit"], "cp": r["cp"],
                        "class": r["class"], "tokens": t, "band": band(t),
                        "opened": r["members_opened"], "forced": r["forced"],
                        "methods_before": before.get((r["chain_id"], r["unit"], r["class"])),
                        "positions": r["positions"], "methods": r["methods"]})
    return units, classes


def _median(xs: list) -> float | None:
    xs = sorted(xs)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def reader_summary(units: list[dict], classes: list[dict]) -> dict:
    """Per author group (arm) and size band, and over all bands: the units and repositories (chains),
    the private share of introduced members, the share of growth of existing classes arriving
    forced, the members opened per class row, the methods of the classes code lands in (mean and
    median) and the splits per unit; a band with fewer than ``READER_FLOOR`` repositories is marked
    too thin."""
    out: dict[str, dict] = {}
    for arm in sorted({r["arm"] for r in units} | {r["arm"] for r in classes}):
        a = out.setdefault(arm, {})
        for b in ("all", "below 200k", "200k to 1M", "above 1M"):
            us = [r for r in units if r["arm"] == arm and (b == "all" or r["band"] == b)]
            cs = [r for r in classes if r["arm"] == arm and (b == "all" or r["band"] == b)]
            if not us and not cs:
                continue
            chains = {r["chain_id"] for r in us} | {r["chain_id"] for r in cs}
            intro = sum(r["introduced"] or 0 for r in us)
            exist = sum(r["existing_positions"] for r in us)
            sizes = [r["methods_before"] for r in cs if r["methods_before"] is not None]
            a[b] = {"units": len(us), "repositories": len(chains), "too_thin": len(chains) < READER_FLOOR,
                    "introduced": intro,
                    "private_share": sum(r["private"] or 0 for r in us) / intro if intro else None,
                    "forced_share": sum(r["forced_positions"] for r in us) / exist if exist else None,
                    "class_rows": len(cs),
                    "opened_per_row": sum(r["opened"] for r in cs) / len(cs) if cs else None,
                    "class_methods_mean": sum(sizes) / len(sizes) if sizes else None,
                    "class_methods_median": _median(sizes),
                    "splits_per_unit": sum(r["splits"] for r in us) / len(us) if us else None,
                    "tokens_median": _median([r["tokens"] for r in us if r["tokens"] is not None])}
    return out


def redesign(hosts: list[dict], pairs: list[dict], min_changes: int = 2,
             min_together: int = 3, overlap: float = 0.5) -> dict:
    """The redesign reading (PLAN.md 4.2d), per arm: where the code stands between the two forces.

    *Split:* a class whose forced changes (placements bound at the class with no alternative) fall
    into groups that share none of the class's values, at least two groups of ``min_changes`` or
    more. A class is flagged at the first unit at which that holds; the classes with at least two
    forced changes and never flagged are the reference, from their second forced change. Whether the
    groups' changes went with different classes (none in common) is recorded.

    *Concentrate:* a pair of existing classes changed together at least ``min_together`` times,
    where at least ``overlap`` of the later times the change was bound to class values it had been
    bound to in an earlier time (the same data again), and whose coupling rose (after the last time
    against before the first). Flagged at its ``min_together``-th time."""
    out: dict[str, dict] = {}

    def arm_of(a):
        return out.setdefault(a, {"split": {"classes": 0, "flagged": 0, "disjoint_partners": 0, "candidates": []},
                                  "concentrate": {"pairs": 0, "together": 0, "flagged": 0, "candidates": []}})

    # ---- split: forced changes into one class, grouped by shared values
    units: dict[tuple, set] = {}
    for h in hosts:
        if tables.changed(h):
            units.setdefault((h["chain_id"], int(h["cp"])), set()).add(h.get("before_type") or h["type"])
    forced: dict[tuple, list] = {}
    for h in sorted(hosts, key=lambda r: int(r["cp"])):
        if not tables.changed(h) or truth(h.get("class_new")) or tables.forced(h) is not True:
            continue
        c = h.get("before_type") or h["type"]
        forced.setdefault((h["chain_id"], h["arm"], c), []).append(
            (int(h["cp"]), _values(h), units.get((h["chain_id"], int(h["cp"])), set()) - {c}))
    for (chain_id, arm, c), changes in forced.items():
        if len(changes) < 2:
            continue
        a = arm_of(arm)["split"]
        a["classes"] += 1
        flagged_at, groups = None, []
        for i in range(len(changes)):
            seen = changes[:i + 1]
            parent = list(range(len(seen)))

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            for x in range(len(seen)):
                for y in range(x):
                    if seen[x][1] & seen[y][1]:
                        parent[find(x)] = find(y)
            gs: dict[int, list] = {}
            for x in range(len(seen)):
                gs.setdefault(find(x), []).append(seen[x])
            big = [g for g in gs.values() if len(g) >= min_changes]
            if len(big) >= 2:
                flagged_at, groups = seen[-1][0], big
                break
        if flagged_at is None:
            continue
        partners = [set().union(*(ch[2] for ch in g)) for g in groups]
        disjoint = all(not (partners[x] & partners[y]) for x in range(len(partners)) for y in range(x))
        a["flagged"] += 1
        a["disjoint_partners"] += disjoint
        a["candidates"].append({"chain_id": chain_id, "class": c, "at": flagged_at,
                                "groups": [sorted(set().union(*(ch[1] for ch in g))) for g in groups],
                                "disjoint_partners": disjoint})

    # ---- concentrate: pairs changed together again over the same data
    vals: dict[tuple, set] = {}
    for h in hosts:
        if tables.changed(h):
            vals.setdefault((h["chain_id"], int(h["cp"]), h.get("before_type") or h["type"]), set()).update(_values(h))
    by_pair: dict[str, list] = {}
    for p in pairs:
        if p["in_tree"]:
            by_pair.setdefault(p["pair"], []).append(p)
    for key, rows in by_pair.items():
        rows.sort(key=lambda r: r["unit"])
        a = arm_of(rows[0]["arm"])["concentrate"]
        a["pairs"] += 1
        if len(rows) < min_together:
            continue
        a["together"] += 1
        chain_id, x, y = key.split("|")
        used = [vals.get((chain_id, r["unit"], x), set()) | {f"{y}:{v}" for v in vals.get((chain_id, r["unit"], y), set())}
                for r in rows]
        again = sum(1 for i in range(1, len(used)) if used[i] & set().union(*used[:i]))
        rose = rows[-1]["coupling"] + (rows[-1]["added"] or 0) > rows[0]["coupling"]
        at = rows[min_together - 1]["unit"]
        if again / (len(used) - 1) >= overlap and rose:
            a["flagged"] += 1
            a["candidates"].append({"chain_id": chain_id, "classes": [x, y], "times": len(rows), "at": at,
                                    "same_data": round(again / (len(used) - 1), 3)})
    for a in out.values():
        a["split"]["candidates"] = sorted(a["split"]["candidates"], key=lambda c: -len(c["groups"]))[:10]
        a["concentrate"]["candidates"] = sorted(a["concentrate"]["candidates"], key=lambda c: -c["times"])[:10]
    return out


def surface_rows(boundary: list[dict]) -> list[dict]:
    """Surface against volume (PLAN.md 4.2e): one row per class a unit changed (volume and surface
    before and after the change) and per class of each chain's last tree (``cross_section``), with
    the surface as the calls out of and into the class."""
    out = []
    for r in boundary:
        row = {"chain_id": r["chain_id"], "arm": r["arm"], "frontend": r.get("frontend", ""),
               "cp": float(r["position"]) if r.get("position") not in (None, "") else int(r["cp"]),
               "class": f"{r['chain_id']}|{r['class']}", "cross_section": truth(r["cross_section"]),
               "forced": truth(r.get("forced"))}
        for tag in ("before", "after"):
            if num(r.get(f"methods_{tag}")) is None:
                continue
            row[f"methods_{tag}"] = int(num(r[f"methods_{tag}"]))
            row[f"positions_{tag}"] = num(r.get(f"positions_{tag}"))
            row[f"surface_{tag}"] = int(num(r[f"out_{tag}"], 0)) + int(num(r[f"in_{tag}"], 0))
            row[f"neighbours_{tag}"] = int(num(r[f"out_classes_{tag}"], 0)) + int(num(r[f"in_classes_{tag}"], 0))
        out.append(row)
    return out


def ripple(hosts: list[dict], edges: list[dict]) -> dict:
    """Ripple (PLAN.md 4.2e): for each call a unit added across a class's boundary, the later units
    that change the method it reaches, and how many of those also change the calling class (the
    change ripples back across the boundary). Per arm, by whether the call came with a forced change
    (the caller's or the callee's class forced in the unit) and by the member it reached: already
    open, or exposed or widened by the unit. Against chance: the share of the chain's units that
    change the calling class anyway, summed over the later changes (``expected``), so that
    ``ripple_ratio`` above 1 is a ripple beyond two classes that both change often."""
    from . import flow
    changed_methods: dict[str, dict[tuple, list[int]]] = {}
    changed_classes: dict[str, dict[int, set]] = {}
    for h in hosts:
        if not tables.changed(h):
            continue
        t = flow.simple(h.get("before_type") or h["type"])
        sig = h.get("before_signature") or h.get("signature")
        changed_methods.setdefault(h["chain_id"], {}).setdefault((t, sig), []).append(int(h["cp"]))
        changed_classes.setdefault(h["chain_id"], {}).setdefault(int(h["cp"]), set()).add(t)
    units_of = {cid: len({h_cp for h_cp in by}) for cid, by in changed_classes.items()}
    share: dict[tuple, float] = {}
    for cid, by in changed_classes.items():
        n = max(units_of[cid], 1)
        counts: dict[str, int] = {}
        for cs in by.values():
            for c in cs:
                counts[c] = counts.get(c, 0) + 1
        for c, k in counts.items():
            share[(cid, c)] = k / n
    out: dict[str, dict] = {}
    for e in edges:
        forced = truth(e["caller_forced"]) or truth(e["callee_forced"])
        group = f"{'forced' if forced else 'unforced'}_{'existing' if e['kind'] == 'existing' else 'opened'}"
        g = out.setdefault(e["arm"], {}).setdefault(group, {"calls": 0, "later_changes": 0, "rippled": 0,
                                                             "calls_changed_later": 0, "expected": 0.0})
        g["calls"] += 1
        t = int(e["cp"])
        later = sorted({u for u in changed_methods.get(e["chain_id"], {}).get(
            (e["callee_class"], e["callee_signature"]), []) if u > t})
        g["later_changes"] += len(later)
        g["calls_changed_later"] += bool(later)
        g["rippled"] += sum(1 for u in later
                            if e["caller_class"] in changed_classes.get(e["chain_id"], {}).get(u, set()))
        # by chance: the caller's class changes in this share of the chain's units anyway
        g["expected"] += len(later) * share.get((e["chain_id"], e["caller_class"]), 0.0)
    for arm in out.values():
        for g in arm.values():
            g["ripple_rate"] = g["rippled"] / g["later_changes"] if g["later_changes"] else None
            g["chance_rate"] = g["expected"] / g["later_changes"] if g["later_changes"] else None
            g["ripple_ratio"] = g["rippled"] / g["expected"] if g["expected"] else None
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
                    # on a history the index is the unit's place in the repository, 0 to 1
                    "cp": float(r["position"]) if r.get("position") not in (None, "") else int(r["cp"]),
                    "host_new": truth(r["host_new"]),
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
                    "fields_added": int(a.get("fields_added") or 0),
                    "method_values_added": int(a.get("method_values_added") or 0)})
    return out


def reopen_rows(additions: list[dict]) -> list[dict]:
    """Per checkpoint: the classes its bound code goes back into and the wiring files it changes
    again (reported)."""
    def files(a):
        j, w = num(a.get("existing_java_files")), num(a.get("existing_wiring_files"))
        return {"existing_java_files": None if j is None else int(j),
                "existing_wiring_files": None if w is None else int(w),
                # H4's symmetric count: every existing file the change went back into
                "existing_files": None if j is None or w is None else int(j + w),
                # how well-trodden those files were: H4's symmetric count
                "trodden": None if num(a.get("trodden")) is None else int(num(a.get("trodden"))),
                "trodden_java": None if num(a.get("trodden_java")) is None else int(num(a.get("trodden_java"))),
                "trodden_wiring": None if num(a.get("trodden_wiring")) is None else int(num(a.get("trodden_wiring")))}
    return [{"chain_id": a["chain_id"], "arm": a["arm"], "frontend": a.get("frontend", ""),
             "cp": int(a["cp"]), "reopened": int(a["reopened"]),
             "reopened_classes": int(a["reopened_classes"]), "reopened_wiring": int(a["reopened_wiring"]),
             **files(a)}
            for a in additions if a.get("reopened") not in (None, "")]


SPLIT = ["logic_added", "organisation_added", "declaration_lines_added", "import_lines_added",
         "wiring_lines_added", "params_new_methods", "params_wired_functions", "params_called_methods",
         "new_wired_functions", "new_called_methods", "birth_binding", "method_values_added", "fields_added",
         "logic_existing_methods", "logic_new_called_methods", "logic_new_wired_functions",
         "existing_methods_edited"]


def split_rows(additions: list[dict]) -> list[dict]:
    """Logic and organisation (PLAN.md 4.9): per checkpoint and chain, the parts of the code it
    added and the state it handed along. Only checkpoints where the diff's lines were read."""
    out = []
    for a in additions:
        if num(a.get("declaration_lines_added")) is None or truth(a.get("noop")):
            continue
        row = {"chain_id": a["chain_id"], "arm": a["arm"], "frontend": a.get("frontend", ""), "cp": int(a["cp"])}
        row.update({k: int(num(a.get(k), 0)) for k in SPLIT})
        # organisation in all: in bodies, declarations and wiring (imports apart: they follow the tools)
        row["organisation_all"] = row["organisation_added"] + row["declaration_lines_added"] + row["wiring_lines_added"]
        out.append(row)
    return out


def split_summary(rows: list[dict], checkpoints: int) -> dict:
    """Per arm: each part per checkpoint, over the stream and over its thirds, and organisation's
    share of logic and organisation together."""
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        mine = [r for r in rows if r["arm"] == arm]

        def mean(k, rs):
            return sum(r[k] for r in rs) / len(rs) if rs else None
        thirds = {str(t): [r for r in mine if min(int((r["cp"] - 1) / max(checkpoints, 1) * 3) + 1, 3) == t]
                  for t in (1, 2, 3)}
        a = {"checkpoints": len(mine), "per_checkpoint": {k: mean(k, mine) for k in SPLIT + ["organisation_all"]},
             "thirds": {t: {k: mean(k, rs) for k in SPLIT + ["organisation_all"]} for t, rs in thirds.items()}}
        logic, org = sum(r["logic_added"] for r in mine), sum(r["organisation_all"] for r in mine)
        a["organisation_share"] = org / (logic + org) if logic + org else None
        out[arm] = a
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
            # reported (PLAN.md 4.3b): what the change introduced there, what it left (stood by and
            # introduced together), and the later intrusions bound to each
            **{k: int(o.get(k) or 0) for lev in ("class", "method")
               for k in (f"introduced_{lev}", f"drawn_{lev}_introduced", f"left_{lev}", f"drawn_{lev}_left")},
            # H2 (PLAN.md 4.4): the values the code was bound to there (core), the rest the place
            # held (periphery), and the later intrusions' uses of each, value by value
            **{k: int(o.get(k) or 0) for lev in ("class", "method")
               for k in (f"core_{lev}", f"periphery_{lev}", f"uses_core_{lev}", f"uses_periphery_{lev}")},
            # reported: H2 at the class on its fields only, as until 19 November 2026
            **{k: int(o.get(k) or 0) for k in ("core_class_fields", "periphery_class_fields",
                                               "uses_core_class_fields", "uses_periphery_class_fields")},
            # reported: H2 at the class with every member the code was bound to as the core, private
            # or not, as until 22 November 2026 (the core is now the private part, PLAN.md 4.4)
            **{k: int(o.get(k) or 0) for k in ("core_class_all", "periphery_class_all",
                                               "uses_core_class_all", "uses_periphery_class_all")},
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


#: A class measure is tested in H3 only where the class level can tell classes apart: later
#: arrivals in at least MIN_CLASSES distinct classes (by name, over all chains), and no one class
#: holding more than MAX_CLASS_SHARE of them (PLAN.md §5).
MIN_CLASSES = 10
MAX_CLASS_SHARE = 0.5


def class_level(h2: list[dict]) -> dict:
    """Whether the class level varies enough for H3's class measures: the distinct classes that
    receive later bound arrivals, and the share of those arrivals the busiest class holds. A
    class is counted by its name over all chains, and its arrivals once per chain and checkpoint."""
    seen, per = set(), {}
    for r in h2:
        key = (r["chain_id"], r["cp"], r.get("class_identity"))
        if not r["bound"] or r.get("class_identity") is None or key in seen:
            continue
        seen.add(key)
        per[r["class_identity"]] = per.get(r["class_identity"], 0) + r["intrusion_class"]
    total = sum(per.values())
    classes = sum(1 for v in per.values() if v > 0)
    top = (max(per.values()) / total) if total else None
    return {"classes_with_arrivals": classes, "top_class_share": top,
            "min_classes": MIN_CLASSES, "max_share": MAX_CLASS_SHARE,
            "testable": classes >= MIN_CLASSES and top is not None and top <= MAX_CLASS_SHARE}


def amount(additions: list[dict], seed: int = SEED, resamples: int = 10_000,
           methods_arm: str = METHODS_ARM, function_arm: str = FUNCTION_ARM) -> dict:
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
    m, f = by_arm.get(methods_arm, []), by_arm.get(function_arm, [])
    if not m or not f or statistics.fmean(m) == 0:
        return {"ratio": None, "interval": None, "in_band": None, "per_arm": by_arm}
    ratio = statistics.fmean(f) / statistics.fmean(m)
    rng = random.Random(seed)
    draws = sorted(statistics.fmean(rng.choices(f, k=len(f))) / statistics.fmean(rng.choices(m, k=len(m)))
                   for _ in range(resamples))
    interval = [draws[int(0.025 * (resamples - 1))], draws[int(0.975 * (resamples - 1))]]
    return {"ratio": ratio, "interval": interval,
            "in_band": AMOUNT_BAND[0] <= ratio <= AMOUNT_BAND[1], "band": AMOUNT_BAND,
            "per_arm": {k: statistics.fmean(v) for k, v in by_arm.items()},
            "ratio_total": statistics.fmean(totals[function_arm]) / statistics.fmean(totals[methods_arm]),
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
    past = bool(analysis.get("history"))     # corpora B and C: repositories' histories (§3.2, §3.3)

    def table(t: str) -> list[dict]:
        return history.gather(analysis, t, measured_root) if past else gather(name, t, measured_root)

    hosts = table("hosts")
    run_rows = table("runs")
    h1 = h1_rows(run_rows, hosts, streamed)
    additions = table("additions")
    outcomes = table("outcomes")
    h2 = h2_rows(outcomes, hosts, additions, streamed)
    kept, counts = shape_kept(h2)
    sinew, sinew_counts = shape_kept(h2, SINEW_FLAGS)
    lit, lit_counts = literature_kept(h2)
    at_class = class_level(h2)
    chains: dict[str, set] = {}
    for a in additions:
        chains.setdefault(a["arm"], set()).add(a["chain_id"])
    out = out_root / name
    landed = table("landings")
    # unbound code's destination, per landing (the arms' contrast on a history, §3.3)
    write_csv(out / "landing.csv", [
        {"chain_id": r["chain_id"], "arm": r["arm"], "cp": r["cp"],
         "existing_class": r["destination"] != "new class"}
        for r in landed if "chain_id" in r and not truth(r["bound"])])
    write_csv(out / "h1.csv", h1)
    by = by_rows(run_rows, outcomes)
    write_csv(out / "by.csv", [r for r in by if r["pulled"]])
    captured = capture_rows(additions)
    write_csv(out / "capture.csv", captured)
    again = reopen_rows(additions)
    write_csv(out / "reopen.csv", again)
    split = [] if past else split_rows(additions)
    write_csv(out / "split.csv", split)
    write_csv(out / "h2.csv", h2)
    chosen5 = h5_rows(hosts, streamed)
    write_csv(out / "h5.csv", chosen5)
    write_csv(out / "h5_forced.csv", [] if past else h5_forced_rows(chosen5, additions))
    h6 = h6_rows(hosts, streamed)
    write_csv(out / "h6.csv", h6)
    paired = pair_rows(table("pairs"))
    write_csv(out / "pairs.csv", paired)
    coupled = table("coupling")
    h7 = calls_across_rows(table("encapsulation"), hosts)
    write_csv(out / "calls_across.csv", h7)
    surfaced = [] if past else h7_rows(table("links"), split)
    write_csv(out / "h7.csv", surfaced)
    write_csv(out / "surface.csv", surface_rows(table("boundary")))
    edges = table("edges")
    rippled = ripple(hosts, edges)
    members = table("members")
    r_units, r_classes = reader_rows(members, hosts, h7, table("boundary"), table("refactorings"))
    write_csv(out / "reader_units.csv", r_units)
    write_csv(out / "reader_classes.csv", r_classes)
    spec = {"analysis": name, "role": analysis["role"], "seed": SEED, "boot": BOOT_HISTORY if past else BOOT,
            "margin": MARGIN, "methods_arm": analysis.get("methods_arm", METHODS_ARM),
            "function_arm": analysis.get("function_arm", FUNCTION_ARM),
            # a history has no stream: its units are not problems every chain solves, so no model
            # carries an intercept for them, and the index is the unit's place from 0 to 1
            "problem_fixed": not past,
            # encapsulation and the reader (PLAN.md 4.2f): modelled on the histories only, where
            # the author varies; corpus A reports it per arm
            "reader_models": past,
            "shape_kept": kept, "shape_counts": {**counts, **sinew_counts}, "sinew_kept": sinew,
            "literature": lit, "literature_counts": lit_counts,
            # H3's measures that vary; its class measures only where the class level does
            "class_level": at_class,
            "h3_measures": [k for k in H3_MEASURES if k in lit
                            and (lit[k]["level"] == "method" or at_class["testable"])],
            "h3_sensitivity": [k for k in H3_SENSITIVITY if k in lit
                               and (lit[k]["level"] == "method" or at_class["testable"])],
            "h3_all": H3_MEASURES, "reach": REACH, "checkpoints": len(streamed),
            "acts": any(r["act"] is not None for r in h1 + h2),
            "frontends": sorted({r["frontend"] for r in h1 if r["frontend"]})}
    conditions = {"chains": {k: len(v) for k, v in chains.items()},
                  "descriptive_only": analysis["role"] == "development"
                  or any(len(v) < MIN_CHAINS for v in chains.values()) or len(chains) < 2,
                  "amount": amount(additions), "wiring": wiring_checks(additions)}
    if analysis.get("contrast") == "no-encapsulation":      # Run D against Run A (PLAN.md 3.1a)
        conditions["contrast"] = "no-encapsulation"
        conditions["compliance"] = compliance(members, spec["function_arm"])
        conditions["amount"] = amount(additions, methods_arm=spec["methods_arm"],
                                      function_arm=spec["function_arm"])
    # the readings reported beside the hypotheses (PLAN.md 5): choice at a checkpoint, formation
    full = all(k in (additions[0] if additions else {}) for k in ("hosts", "hosts_existing", "binding_method"))
    chosen = readings.choice(additions, hosts) if full else []
    write_csv(out / "choice.csv", chosen)
    lost = {arm: {"lines": sum(r["own_lines"] or 0 for r in h2 if r["arm"] == arm),
                  "lost": sum(r["own_lost"] or 0 for r in h2 if r["arm"] == arm)}
            for arm in sorted({r["arm"] for r in h2})}
    checked = {} if past else validate.summary(table("validation"))
    (out / "readings.json").write_text(json.dumps({
        "choice": readings.choice_summary(chosen),
        "formation_end": readings.formation_end(run_rows, additions, len(streamed)) if streamed else {},
        "bystanders": readings.bystander_summary(by, captured, len(streamed)),
        "reopening": readings.reopening_summary(again),
        "drawn": readings.drawn_summary(h2),
        "core": readings.core_summary(hosts),
        "core_reuse": readings.core_reuse(h2),
        "landings": places.summary(landed),
        "co_change": co_change(paired),
        "growth": growth_accounting(hosts, len(streamed)),
        "growth_by_access": growth_by_access(hosts),
        "growth_by_lever": growth_by_lever(hosts),
        "validation": checked,
        "validation_flags": validate.flags(checked),
        "split": split_summary(split, len(streamed)),
        "links": links_summary(surfaced, len(streamed)),
        "coupling_added": coupling_accounting(paired, coupled, h6),
        "coupling_source": coupling_source(h7, edges),
        "redesign": redesign(hosts, paired),
        "ripple": rippled,
        "reader": reader_summary(r_units, r_classes),
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
        if not runs.measured(analysis):
            continue
        runs.guard(reg, analysis)
        out = prepare(analysis, runs.streamed(reg, analysis))
        print(f"{analysis['name']}: {out}")


if __name__ == "__main__":
    main()

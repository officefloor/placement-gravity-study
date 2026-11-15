"""Tables from a measured chain: hosts, runs, classes, additions and outcomes (PLAN.md §4.2–4.6).

Ties (the instrument's measure of how far an addition is held to its location):

- ``tie_method``: the host method's pre-existing parameters (not injected) and locals the added
  code uses;
- ``tie_field`` and ``tie_class_method``: the host class's pre-existing fields and methods it uses;
  together the **class ties**;
Ties are read from the **logic lines** the change adds or edits (a method's body statements;
signatures, declarations and constructor wiring are organisation). Every reference on those lines
counts, edited lines alike. ``tok_*`` counts only the references an edit itself introduced, as a
secondary reading. Not ties: class **utilities** (loggers), which any class can declare, and
``birth_tie`` (the values a caller passes a new method: the tie is already on the caller's line).
``unresolved`` lists references that resolve to nothing seen (inherited members, static imports).
"""

from __future__ import annotations

from pathlib import Path

import yaml

#: A host whose added positions are at least this share moved code is a re-placement.
REPLACEMENT_SHARE = 0.5


def stream(checkpoints_yaml: Path) -> dict[int, dict]:
    """cp number (1-based, the stream's order) -> {id, type, mutates}."""
    doc = yaml.safe_load(checkpoints_yaml.read_text())
    return {i: {"id": c["id"], "type": c.get("type", "additive"),
                "mutates": list(c.get("mutates") or [])}
            for i, c in enumerate(doc["checkpoints"], start=1)}


def gini(xs: list[float]) -> float:
    xs = sorted(x for x in xs if x > 0)
    n = len(xs)
    if n <= 1:
        return 0.0
    return sum((2 * i - n - 1) * x for i, x in enumerate(xs, start=1)) / (n * sum(xs))


def _hosts(measured: dict):
    return [r for r in measured["records"] if r["kind"] == "host"]


def host_rows(arm: str, chain: str, measured: dict) -> list[dict]:
    rows = []
    for r in _hosts(measured):
        moved = r["moved_rm"] + r["moved_text"]
        runs = r["runs"]
        tm = sorted({v for x in runs for v in x["tie_method"]})
        tf = sorted({v for x in runs for v in x["tie_field"]})
        tc = sorted({v for x in runs for v in x["tie_class_method"]})
        tu = sorted({v for x in runs for v in x["utility"]})
        un = sorted({v for x in runs for v in x["unresolved"]})
        rows.append({
            "arm": arm, "chain": chain, "cp": int(r["unit"][2:]), "path": r["path"],
            "type": r["type"], "name": r["name"], "signature": r["signature"],
            "before_type": r["before_type"], "before_name": r["before_name"],
            "host_new": r["host_new"], "class_new": r["class_new"], "injected": r["injected"],
            "pre_positions": r["pre_positions"], "post_positions": r["post_positions"],
            "added": r["added"], "moved_rm": r["moved_rm"], "moved_text": r["moved_text"],
            "removed": r["removed"], "net_added": r["added"] - moved,
            "replacement": r["added"] > 0 and moved / r["added"] >= REPLACEMENT_SHARE,
            "runs": len(runs), "edits": sum(1 for x in runs if x["replaces"] > 0),
            "tie_method": len(tm), "tie_field": len(tf), "tie_class_method": len(tc),
            "tie_class": len(tf) + len(tc), "tie": len(tm) + len(tf) + len(tc),
            "utility": len(tu), "unresolved": len(un), "unresolved_values": " ".join(un),
            "organisation": r["organisation"],
            "birth_tie": len(r.get("birth_tie", [])),
            "tie_method_values": " ".join(tm),
            "tie_class_values": " ".join(tf + [m + "()" for m in tc]),
            "params": r["params"],
        })
    return rows


def run_rows(arm: str, chain: str, measured: dict) -> list[dict]:
    rows = []
    for r in _hosts(measured):
        for x in r["runs"]:
            rows.append({
                "arm": arm, "chain": chain, "cp": int(r["unit"][2:]), "type": r["type"],
                "name": r["name"], "host_new": r["host_new"], "injected": r["injected"],
                "pre_positions": r["pre_positions"], "positions": x["positions"],
                "replaces": x["replaces"], "edit": x["replaces"] > 0,
                "added_tokens": x["added_tokens"], "inputs": x["inputs"], "outputs": x["outputs"],
                "tie_method": len(x["tie_method"]), "tie_field": len(x["tie_field"]),
                "tie_class_method": len(x["tie_class_method"]),
                "tie_class": len(x["tie_field"]) + len(x["tie_class_method"]),
                "utility": len(x["utility"]),
                "tok_tie_method": x["tok_tie_method"], "tok_tie_class": x["tok_tie_class"],
                "tok_tie": x["tok_tie_method"] + x["tok_tie_class"],
                "unresolved": len(x["unresolved"]), "unresolved_values": " ".join(x["unresolved"]),
                "tie": len(x["tie_method"]) + len(x["tie_field"]) + len(x["tie_class_method"]),
                "tie_method_values": " ".join(x["tie_method"]),
                "tie_class_values": " ".join(x["tie_field"] + [m + "()" for m in x["tie_class_method"]]),
                "utility_values": " ".join(x["utility"]),
            })
    return rows


def class_rows(arm: str, chain: str, hosts: list[dict], measured: dict) -> list[dict]:
    """Class level: per addition and class it reaches, the hosts and positions added there and the
    class ties (distinct pre-existing fields and methods of the class the added code uses)."""
    out: dict[tuple[int, str, str], dict] = {}
    for h in hosts:
        if h["net_added"] <= 0 or h["replacement"]:
            continue
        k = (h["cp"], h["path"], h["type"])
        row = out.setdefault(k, {"arm": arm, "chain": chain, "cp": h["cp"], "path": h["path"],
                                 "type": h["type"], "class_new": h["class_new"], "hosts": 0,
                                 "positions_added": 0, "ties": set()})
        row["hosts"] += 1
        row["positions_added"] += h["net_added"]
        if h["tie_class_values"]:
            row["ties"] |= set(h["tie_class_values"].split())
    rows = []
    for row in out.values():
        ties = sorted(row.pop("ties"))
        rows.append({**row, "tie_class": len(ties), "tie_class_values": " ".join(ties)})
    return sorted(rows, key=lambda r: (r["cp"], r["path"], r["type"]))


def addition_rows(arm: str, chain: str, measured: dict, hosts: list[dict],
                  streamed: dict[int, dict]) -> list[dict]:
    problems = {}
    for r in measured["records"]:
        if r["kind"] == "problem":
            problems[r["unit"]] = problems.get(r["unit"], 0) + 1
    refs = {f["unit"]: len(f["refactorings"]) for f in measured.get("refactorings", [])}
    rows = []
    for c in measured["checkpoints"]:
        cp, unit = c["cp"], f"cp{c['cp']:02d}"
        hs = [h for h in hosts if h["cp"] == cp and h["net_added"] > 0 and not h["replacement"]]
        existing = [h for h in hs if not h["host_new"]]
        added = sum(h["net_added"] for h in hs)
        w = measured["wiring"][unit]
        s = streamed.get(cp, {})
        rows.append({
            "arm": arm, "chain": chain, "cp": cp, "rule": c["rule"], "noop": c["noop"],
            "mutative": s.get("type") == "mutative", "mutates": " ".join(map(str, s.get("mutates", []))),
            "hosts": len(hs), "hosts_existing": len(existing),
            "classes": len({(h["path"], h["type"]) for h in hs}),
            "positions_added": added,
            "positions_in_existing": sum(h["net_added"] for h in existing),
            "share_in_existing": (sum(h["net_added"] for h in existing) / added) if added else None,
            "gini": gini([h["net_added"] for h in hs]),
            "largest_host_pre": max((h["pre_positions"] for h in existing), default=0),
            "tie_method": sum(h["tie_method"] for h in hs),
            "tie_class": sum(h["tie_class"] for h in hs),
            "birth_tie": sum(h["birth_tie"] for h in hs if h["host_new"]),
            "replacements": sum(1 for h in hosts if h["cp"] == cp and h["replacement"]),
            "refactorings": refs.get(unit, 0),
            "amount_positions": measured["amount"][unit]["positions"],
            "amount_methods": measured["amount"][unit]["methods"],
            "wiring_nodes_added": w["after"]["nodes"] - w["before"]["nodes"],
            "wiring_edges_added": w["after"]["edges"] - w["before"]["edges"],
            "problems": problems.get(unit, 0),
        })
    return rows


def identities(hosts: list[dict]) -> dict[tuple[int, str, str], str]:
    """A stable identity for each host across renames and moves: a host matched to a differently
    named or typed before version keeps that version's identity."""
    current: dict[tuple[str, str], str] = {}
    out = {}
    for h in sorted(hosts, key=lambda h: h["cp"]):
        key = (h["type"], h["name"])
        if h["before_type"] is not None:
            before = (h["before_type"], h["before_name"])
            ident = current.get(before, f"{before[0]}#{before[1]}")
        else:
            ident = current.get(key, f"{key[0]}#{key[1]}")
        current[key] = ident
        out[(h["cp"], h["type"], h["name"])] = ident
    return out


def outcome_rows(arm: str, chain: str, hosts: list[dict], streamed: dict[int, dict]) -> list[dict]:
    """§4.4 at method level: for each problem k and each host its code went into, the later
    checkpoints touching the same host (followed across renames and moves), split into those the
    stream declares to change k and the rest (intrusion)."""
    ident = identities(hosts)
    touched: dict[str, set[int]] = {}
    for h in hosts:
        if h["net_added"] > 0 or h["removed"] > 0:
            touched.setdefault(ident[(h["cp"], h["type"], h["name"])], set()).add(h["cp"])
    last = max((h["cp"] for h in hosts), default=0)
    rows = []
    for h in hosts:
        if h["net_added"] <= 0 or h["replacement"]:
            continue
        k, i = h["cp"], ident[(h["cp"], h["type"], h["name"])]
        later = sorted(j for j in touched.get(i, set()) if j > k)
        declared = [j for j in later if k in streamed.get(j, {}).get("mutates", [])]
        rows.append({
            "arm": arm, "chain": chain, "cp": k, "identity": i, "type": h["type"], "name": h["name"],
            "host_new": h["host_new"], "pre_positions": h["pre_positions"],
            "net_added": h["net_added"], "tie_method": h["tie_method"], "tie_class": h["tie_class"],
            "birth_tie": h["birth_tie"], "later_checkpoints": last - k,
            "later_touches": len(later), "declared": len(declared),
            "intrusion": len(later) - len(declared),
            "intrusion_per_100": (100 * (len(later) - len(declared)) / (last - k)) if last > k else None,
        })
    return rows

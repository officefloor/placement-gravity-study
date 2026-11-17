"""Where added code lands among the places it could have gone (PLAN.md §5, *Where unbound code
goes*; reported).

At each checkpoint, every method of the tree as it stood before the change is a candidate place,
and so is every class. Each has two kinds of size:

- **shape:** positions and cognitive complexity (a class: the sum over its methods);
- **data width:** the values held there. A method: its parameters and locals, and its class's
  fields. A class: its fields (state, injected dependencies and constants).

A **landing** is one host a checkpoint adds logic to (moved code left out). It is **bound** when the
code added there uses data that was already there (``tables.is_bound``), and unbound otherwise. Its
**destination** is an existing method, a new method in an existing class, or a new class. Where the
place existed, the landing carries the place's **rank** among the checkpoint's candidates on each
size: the share of candidates below it, counting half of those equal to it. 0.5 is what a place
picked without regard to that size would average; near 1 is the largest.
"""

from __future__ import annotations

import statistics

from . import tables

METHOD_SIZES = ("positions", "cognitive", "width", "width_method")
CLASS_SIZES = ("class_positions", "class_cognitive", "class_fields", "class_methods")


def candidates(shape: list[dict]) -> tuple[dict, dict]:
    """Per unit: the methods ``{(path, type, signature): sizes}`` and the classes
    ``{type: sizes}`` of the tree before the change."""
    methods: dict[str, dict] = {}
    classes: dict[str, dict] = {}
    for r in shape:
        own = r["in"] + r.get("locals", 0)
        methods.setdefault(r["unit"], {})[(r["path"], r["type"], r["signature"])] = {
            "positions": r["positions"], "cognitive": r["cognitive"],
            "width": own + r.get("class_held", 0), "width_method": own}
        c = classes.setdefault(r["unit"], {}).setdefault(r["type"], {
            "class_positions": 0, "class_cognitive": 0, "class_fields": r.get("class_held", 0),
            "class_methods": 0})
        c["class_positions"] += r["positions"]
        c["class_cognitive"] += r["cognitive"]
        c["class_methods"] += 1
    return methods, classes


def rank(value: float, among: list[float]) -> float | None:
    """The share of ``among`` below ``value``, counting half of those equal to it."""
    if not among:
        return None
    below = sum(1 for x in among if x < value)
    equal = sum(1 for x in among if x == value)
    return (below + 0.5 * equal) / len(among)


def landings(arm: str, chain: str, hosts: list[dict], shape: list[dict]) -> list[dict]:
    """One row per host a checkpoint adds logic to: bound or not, its destination, and the rank of
    the place it landed in among the checkpoint's candidates, at the method and at the class."""
    methods, classes = candidates(shape)
    rows = []
    for h in hosts:
        if h["net_added"] <= 0 or h["replacement"]:
            continue
        unit = f"cp{h['cp']:02d}"
        ms, cs = methods.get(unit, {}), classes.get(unit, {})
        destination = ("new class" if h["class_new"] else
                       "new method" if h["host_new"] else "existing method")
        row = {"arm": arm, "chain": chain, "cp": h["cp"], "type": h["type"],
               "signature": h.get("signature"), "bound": tables.is_bound(h),
               "destination": destination, "net_added": h["net_added"],
               "candidate_methods": len(ms), "candidate_classes": len(cs)}
        m = None if h["host_new"] else ms.get(
            (h.get("before_path"), h.get("before_type"), h.get("before_signature")))
        c = None if h["class_new"] else cs.get(h.get("before_type") or h["type"])
        for k in METHOD_SIZES:
            row[k] = m[k] if m else None
            row[f"rank_{k}"] = rank(m[k], [x[k] for x in ms.values()]) if m else None
        for k in CLASS_SIZES:
            row[k] = c[k] if c else None
            row[f"rank_{k}"] = rank(c[k], [x[k] for x in cs.values()]) if c else None
        rows.append(row)
    return rows


def _true(x) -> bool:
    return x is True or str(x) == "True"


def _num(x) -> float | None:
    return None if x in (None, "", "None") else float(x)


def summary(rows: list[dict]) -> dict:
    """Per arm, for bound and for unbound landings: where they went, and the mean rank of the place
    on each size, at the method (landings into existing methods) and at the class (landings into
    existing classes); and, over the places landed in, Spearman's correlation of the complexity
    rank with the data-width rank (do the two kinds of size point to the same places?)."""
    from .readings import spearman
    out: dict = {}
    for arm in sorted({r["arm"] for r in rows}):
        out[arm] = {}
        for label, want in (("bound", True), ("unbound", False)):
            rs = [r for r in rows if r["arm"] == arm and _true(r["bound"]) == want]
            x: dict = {"landings": len(rs)}
            for d in ("existing method", "new method", "new class"):
                x[d] = (sum(1 for r in rs if r["destination"] == d) / len(rs)) if rs else None
            for k in [f"rank_{s}" for s in METHOD_SIZES + CLASS_SIZES]:
                vs = [v for v in (_num(r.get(k)) for r in rs) if v is not None]
                x[k] = statistics.fmean(vs) if vs else None
                x[f"n_{k}"] = len(vs)
            for lev, a, b in (("method", "rank_cognitive", "rank_width"),
                              ("class", "rank_class_cognitive", "rank_class_fields")):
                pairs = [(_num(r.get(a)), _num(r.get(b))) for r in rs]
                pairs = [p for p in pairs if None not in p]
                x[f"agreement_{lev}"] = spearman([p[0] for p in pairs], [p[1] for p in pairs]) \
                    if len(pairs) > 2 else None
            out[arm][label] = x
    return out

"""The shape competitors of H6 (PLAN.md §4.7), read on the host an addition lands in, at k − 1.

The Java pass (``Pull --shape``) reads every method of the production tree at the agent commit's
parent: SinewSlim's code lines and conventional assessment, and the junction counts. This module
adds what the earlier studies computed in Python, with their own code (the complexity-concentration
study, pinned in requirements.txt):

- **S1 long:** SinewSlim's code lines at or above its trigger (26), the divergence study's constant.
- **S2 not slimmable:** SinewSlim's conventional reading is ``not_slimmable`` or
  ``slimmable_with_record``, the long-method-slim study's *stuck* (its ``analyse.STUCK``). The
  strict ``not_slimmable`` is kept beside it, with the obstacle.
- **S3 junction:** ``d = out − in > 0``, read conventionally as S1, S2 and S4 are: ``in`` counts
  every parameter, injected or not; ``out`` the arguments passed on calls to the application's own
  methods. The injection-aware reading (``in`` without injected parameters, the absorbed
  flow-injection draft's definition) is kept beside it. It is not primary: a wired OfficeFloor
  function receives only injected values, so under it any call it makes with an argument makes it a
  junction, and S3 would measure whether a function calls anything.
- **S4 complexity outlier:** cognitive complexity by the complexity-concentration study's
  ``cognitive.analyze`` over the method's source text, and its modified z-score over every method
  of the checkpoint's tree (``extract.modified_z_scale``), an outlier at ``extract.OUTLIER_Z`` (3.5).
- **S5 concentration:** the host's positions, and the Gini coefficient of its class's positions
  over the class's methods.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from complexity_concentration_study import cognitive
from complexity_concentration_study.extract import OUTLIER_Z, modified_z_scale

from . import chain, tables

#: The long-method-slim study's "stuck" statuses (long_method_slim_study/analyse.py, STUCK).
STUCK = ("not_slimmable", "slimmable_with_record")


def run(listing: Path, out: Path) -> list[dict]:
    """``Pull --shape`` over a listing of ``unit<TAB>tree<TAB>injected`` lines."""
    subprocess.run(["java", "-cp", chain.CLASSPATH, "Pull", "--shape", str(listing), str(out)],
                   check=True)
    return [json.loads(line) for line in out.read_text().splitlines() if line]


def complete(records: list[dict], trees: dict[str, Path]) -> list[dict]:
    """Per method of each tree: the Java pass's record with S1 to S5 added. ``trees`` maps a unit
    to the directory its paths are relative to (for the source text of S4)."""
    methods = [r for r in records if r["kind"] == "shape"]
    texts: dict[tuple[str, str], list[str]] = {}
    for r in methods:
        key = (r["unit"], r["path"])
        if key not in texts:
            raw = (trees[r["unit"]] / r["path"]).read_bytes()
            try:
                texts[key] = raw.decode("utf-8").splitlines()
            except UnicodeDecodeError:
                texts[key] = raw.decode("iso-8859-1").splitlines()
        body = "\n".join(texts[key][r["decl_line"] - 1:r["end_line"]])
        r["cognitive"] = cognitive.analyze(body, "java")[0]
        r["s1_long"] = r["long"]
        r["s2_stuck"] = r["status"] in STUCK
        r["s2_not_slimmable"] = r["status"] == "not_slimmable"
        r["s3_d"] = r["out"] - r["in"]
        r["s3_junction"] = r["s3_d"] > 0
        r["s3_d_injection_aware"] = r["out"] - r["in_injection_aware"]
        r["s3_junction_injection_aware"] = r["s3_d_injection_aware"] > 0
    by_unit: dict[str, list[dict]] = {}
    for r in methods:
        by_unit.setdefault(r["unit"], []).append(r)
    for unit, rs in by_unit.items():
        scale, z = modified_z_scale([r["cognitive"] for r in rs])
        classes: dict[tuple[str, str], list[int]] = {}
        for r in rs:
            classes.setdefault((r["path"], r["type"]), []).append(r["positions"])
        for r in rs:
            r["s4_z"] = round(z(r["cognitive"]), 4)
            r["s4_scale"] = scale
            r["s4_outlier"] = r["s4_z"] >= OUTLIER_Z
            r["s5_class_gini"] = round(tables.gini(classes[(r["path"], r["type"])]), 4)
            r["s5_class_positions"] = sum(classes[(r["path"], r["type"])])
    return methods


def index(methods: list[dict]) -> dict[tuple[str, str, str, str], dict]:
    """(unit, path, type, signature) -> the method's shape record."""
    return {(r["unit"], r["path"], r["type"], r["signature"]): r for r in methods}


#: The host columns S1 to S5 add (None for a new host, or an existing one not found at k − 1).
HOST_COLUMNS = ("s1_long", "s2_stuck", "s2_not_slimmable", "s2_status", "s2_obstacle", "s3_in",
                "s3_out", "s3_d", "s3_junction", "s3_junction_injection_aware", "s4_cognitive", "s4_z", "s4_outlier",
                "s5_class_gini", "s5_class_positions")


def class_index(methods: list[dict]) -> dict[tuple[str, str], dict]:
    """(unit, type) -> a shape record of that class, for its class measures."""
    return {(r["unit"], r["type"]): r for r in methods}


def host_shape(host: dict, shaped: dict[tuple[str, str, str, str], dict],
               classes: dict[tuple[str, str], dict] | None = None) -> dict:
    """S1 to S5 of an existing host's version at k − 1 (its before path, type and signature), with
    the literature's method measures (``literature.METHOD``). The literature's class measures
    (``literature.CLASS``) are those of the host's class at k − 1, also for a new method of a
    class that existed."""
    from . import literature
    none = {c: None for c in HOST_COLUMNS + tuple(literature.METHOD)}
    unit = f"cp{host['cp']:02d}"
    c = None if host.get("class_new") else (classes or {}).get(
        (unit, host.get("before_type") or host["type"]))
    of_class = {k: (c.get(k) if c else None) for k in literature.CLASS}
    of_class["c_gini"] = c.get("s5_class_gini") if c else None
    of_class["c_positions"] = c.get("s5_class_positions") if c else None   # the class's size at k − 1
    if host["host_new"]:
        return {**none, **of_class, "shape_found": None}
    r = shaped.get((unit, host["before_path"], host["before_type"],
                    host["before_signature"]))
    if r is None:
        return {**none, **of_class, "shape_found": False}
    return {**{k: r.get(k) for k in literature.METHOD}, **of_class, "s1_long": r["s1_long"], "s2_stuck": r["s2_stuck"],
            "s2_not_slimmable": r["s2_not_slimmable"], "s2_status": r["status"],
            "s2_obstacle": r["obstacle"], "s3_in": r["in"], "s3_out": r["out"], "s3_d": r["s3_d"],
            "s3_junction": r["s3_junction"],
            "s3_junction_injection_aware": r["s3_junction_injection_aware"], "s4_cognitive": r["cognitive"], "s4_z": r["s4_z"],
            "s4_outlier": r["s4_outlier"], "s5_class_gini": r["s5_class_gini"],
            "s5_class_positions": r["s5_class_positions"], "shape_found": True}


def series_rows(arm: str, chain_name: str, methods: list[dict]) -> list[dict]:
    """The absorbed drafts' system-level readings per checkpoint (reported, not tested): the
    long and stuck method counts, and the share of cognitive complexity held by junctions (the
    flow-injection draft's J, on the cognitive signal). Normalisation by passing tests is left to
    the harness's capture, which this module does not read."""
    by_unit: dict[str, list[dict]] = {}
    for r in methods:
        by_unit.setdefault(r["unit"], []).append(r)
    rows = []
    for unit in sorted(by_unit):
        rs = by_unit[unit]
        total = sum(r["cognitive"] for r in rs)
        rows.append({
            "arm": arm, "chain": chain_name, "cp": int(unit[2:]), "methods": len(rs),
            "positions": sum(r["positions"] for r in rs),
            "long": sum(r["s1_long"] for r in rs), "stuck": sum(r["s2_stuck"] for r in rs),
            "not_slimmable": sum(r["s2_not_slimmable"] for r in rs),
            "junctions": sum(r["s3_junction"] for r in rs),
            "junctions_injection_aware": sum(r["s3_junction_injection_aware"] for r in rs),
            "cognitive": total,
            "junction_share": round(sum(r["cognitive"] for r in rs if r["s3_junction"]) / total, 4)
            if total else None,
            "junction_share_injection_aware": round(
                sum(r["cognitive"] for r in rs if r["s3_junction_injection_aware"]) / total, 4)
            if total else None,
            "outliers": sum(r["s4_outlier"] for r in rs),
            "errors": sum(1 for r in rs if r["status"] == "error"),
        })
    return rows

"""Diagnostics: every figure PLAN.md quotes that the report itself does not print, made by the
steps from the tables steps 3 and 4 wrote, so that no value in the plan comes from a query run by
hand (decided by the author on 25 November 2026, PLAN.md 9 row 112). Step 5 writes them beside each
report, ``results/analysis/<name>/DIAGNOSTICS.md`` and ``diagnostics.json``; each section names
the place in the plan that quotes it.

They describe; none enters a verdict. Most were first read on the development chain while the
plan's rules were being built (§6), on tables of an earlier ``MEASURE_VERSION``: the figures here
are those of the tables as they now stand, so they may differ from the ones §6 records of its day.

    python -m placement_gravity.diagnostics [--analysis NAME ...]
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from . import chain, runs

OUT = runs.RESULTS / "analysis"
MEASURE = runs.RESULTS / "measure"
DATA = chain.ROOT / "data" / "analysis"
SAMPLES = chain.ROOT / "samples"


# ---- helpers ----

def _read(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def num(x, default: float = 0.0) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def truth(x) -> bool:
    return str(x).strip().lower() in ("true", "1", "yes")


def mean(xs) -> float | None:
    xs = list(xs)
    return statistics.fmean(xs) if xs else None


def spearman(xs: list[float], ys: list[float]) -> float | None:
    """Spearman's rank correlation, ties given their mean rank."""
    if len(xs) < 3:
        return None

    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = mean(rx), mean(ry)
    sx = sum((a - mx) ** 2 for a in rx) ** 0.5
    sy = sum((b - my) ** 2 for b in ry) ** 0.5
    if not sx or not sy:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / (sx * sy)


def third(cp: int, last: int) -> int:
    """The third of the stream a checkpoint is in (1, 2 or 3)."""
    return min(3, 1 + 3 * (cp - 1) // max(last, 1))


def chain_tables(name: str, table: str) -> dict[str, list[dict]]:
    """One measured table of every chain of a paired analysis, by arm."""
    out: dict[str, list[dict]] = defaultdict(list)
    base = MEASURE / name
    if not base.exists():
        return {}
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        for r in _read(d / f"{table}.csv"):
            out[r.get("arm", "")].append(r)
    return dict(out)


def last_cp(rows: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in rows:
        out[r["chain_id"]] = max(out.get(r["chain_id"], 0), int(num(r["cp"])))
    return out


# ---- the paired chains (corpus A) ----

def files(name: str) -> dict:
    """§2 H4 and §6 (22 November 2026): the files a chain went back into. Per arm: new Java files a
    checkpoint; Java files at the head and the largest; the existing files gone back into (Java and
    wiring), the busiest and the checkpoints that changed it, the share gone back into at four
    checkpoints or fewer, and the share of the returns the three busiest took; the files both arms
    went back into most, by name."""
    changes, ends, adds = chain_tables(name, "files"), chain_tables(name, "files_end"), chain_tables(name, "additions")
    out, per_name = {}, {}
    for arm, rows in sorted(changes.items()):
        cps = len({(r["chain_id"], r["cp"]) for r in adds.get(arm, [])}) or 1
        back = Counter(r["path"] for r in rows if r["status"] != "A")
        top = back.most_common()
        total = sum(back.values())
        end = ends.get(arm, [])
        per_name[arm] = Counter(Path(r["path"]).name for r in rows if r["status"] != "A")
        out[arm] = {
            "checkpoints": cps,
            "new_java_files_per_checkpoint": sum(1 for r in rows if r["kind"] == "java" and r["status"] == "A") / cps,
            "java_files_at_end": len(end),
            "largest_java_file_kb": max((num(r["bytes"]) for r in end), default=0) / 1000,
            "existing_files_gone_back_into": len(back),
            "busiest": {"path": top[0][0], "checkpoints": top[0][1]} if top else None,
            "share_gone_back_into_at_four_or_fewer": (sum(1 for _, n in top if n <= 4) / len(top)) if top else None,
            "three_busiest_share_of_returns": (sum(n for _, n in top[:3]) / total) if total else None,
        }
    if len(per_name) == 2:
        a, b = sorted(per_name)
        both = sorted(set(per_name[a]) & set(per_name[b]), key=lambda k: -(per_name[a][k] + per_name[b][k]))[:5]
        out["gone_back_into_by_both"] = [{"file": k, a: per_name[a][k], b: per_name[b][k]} for k in both]
    return out


def new_methods(name: str) -> dict:
    """§6 (22 November 2026): the new methods a chain wrote. Per arm: wired functions (a method the
    OfficeFloor wiring declares) and their injected parameters each; new methods that are not wired
    functions and hold logic (not plain organisation, §4.9): how many, their parameters, the values
    their callers pass them, the classes they are in and the class holding most."""
    out = {}
    for arm, rows in sorted(chain_tables(name, "hosts").items()):
        new = [r for r in rows if truth(r["host_new"]) and not truth(r["replacement"])]
        wired = [r for r in new if truth(r["injected"])]
        called = [r for r in new if not truth(r["injected"]) and not truth(r["organisation"])]
        by_class = Counter(r["type"] for r in called)
        out[arm] = {
            "wired_functions": len(wired),
            "injected_parameters_each": mean(num(r["params"]) for r in wired),
            "called_with_logic": len(called),
            "their_parameters": sum(num(r["params"]) for r in called),
            "values_callers_pass": sum(num(r["birth_binding"]) for r in called),
            "classes": len(by_class),
            "most": {"class": by_class.most_common(1)[0][0], "methods": by_class.most_common(1)[0][1]} if by_class else None,
        }
    return out


def trodden_thirds(name: str) -> dict:
    """§6 (22 November 2026): H4's well-trodden count a checkpoint over the thirds of the stream."""
    rows = _read(DATA / name / "reopen.csv")
    last = last_cp(rows)
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        rs = [r for r in rows if r["arm"] == arm and r.get("trodden") not in ("", None)]
        out[arm] = {"all": mean(num(r["trodden"]) for r in rs),
                    "thirds": [mean(num(r["trodden"]) for r in rs if third(int(r["cp"]), last[r["chain_id"]]) == t)
                               for t in (1, 2, 3)]}
    return out


def injected_runs(name: str) -> dict:
    """§6 (16 November 2026): runs of added code into methods that existed, and how many bindings an
    injected dependency accounts for. Per arm: the runs; those bound to an injected dependency; the
    runs bound at all and bound at the class, counting injected dependencies and not."""
    out = {}
    for arm, rows in sorted(chain_tables(name, "runs").items()):
        rs = [r for r in rows if not truth(r["host_new"]) and not truth(r["replacement"])]
        out[arm] = {"runs_into_existing_methods": len(rs),
                    "with_an_injected_binding": sum(1 for r in rs if num(r["binding_injected"]) > 0),
                    "bound": sum(1 for r in rs if num(r["binding"]) > 0),
                    "bound_without_injected": sum(1 for r in rs if num(r["binding_no_injected"]) > 0),
                    "bound_at_the_class": sum(1 for r in rs if num(r["binding_class"]) > 0),
                    "bound_at_the_class_without_injected": sum(1 for r in rs if num(r["binding_class_no_injected"]) > 0)}
    return out


def bound_new_methods(name: str) -> dict:
    """§6 (19 November 2026): new methods bound to their class. Per arm: by how (a field only, a call
    to another of the class's methods only, both); and, in H2's rows, the bound rows of new and of
    existing methods, their later arrivals at the method, the values the new ones introduced and
    later arrivals bound to those; the rows with an arrival bound to what stood by at the method, and
    the methods they are in."""
    out = {}
    hosts = chain_tables(name, "hosts")
    h2 = _read(DATA / name / "h2.csv")
    outcomes = chain_tables(name, "outcomes")
    for arm in sorted(set(hosts) | {r["arm"] for r in h2}):
        new = [r for r in hosts.get(arm, []) if truth(r["host_new"]) and not truth(r["replacement"])
               and num(r["binding_class"]) > 0]
        f, m = (lambda r: num(r["binding_field"]) > 0), (lambda r: num(r["binding_class_method"]) > 0)
        rows = [r for r in h2 if r["arm"] == arm and truth(r["bound"])]
        nr, er = [r for r in rows if truth(r["host_new"])], [r for r in rows if not truth(r["host_new"])]
        drawn = [r for r in outcomes.get(arm, []) if truth(r["bound"]) and num(r["drawn_method"]) > 0]
        out[arm] = {
            "new_methods_bound_at_the_class": len(new),
            "by_a_field_only": sum(1 for r in new if f(r) and not m(r)),
            "by_a_call_only": sum(1 for r in new if m(r) and not f(r)),
            "by_both": sum(1 for r in new if f(r) and m(r)),
            "bound_rows_new": len(nr), "their_later_arrivals_at_the_method": sum(num(r["intrusion_method"]) for r in nr),
            "bound_rows_existing": len(er),
            "existing_later_arrivals_at_the_method": sum(num(r["intrusion_method"]) for r in er),
            "values_new_ones_introduced": sum(num(r["introduced_method"]) for r in nr),
            "later_arrivals_bound_to_those": sum(num(r["drawn_method_introduced"]) for r in nr),
            "rows_with_an_arrival_bound_to_what_stood_by": len(drawn),
            "those_arrivals": sum(num(r["drawn_method"]) for r in drawn),
            "their_methods": dict(Counter(r["name"] for r in drawn).most_common(3)),
        }
    return out


def alternatives_thirds(name: str) -> dict:
    """§6 (19 November 2026): the alternatives at the method over the thirds of the stream, for the
    rows bound to a value named after a class of the system (a domain type: ``owner`` for
    ``Owner``) and the rest; and the methods on a host's control flow over the thirds."""
    hosts = chain_tables(name, "hosts")
    out = {}
    for arm, rows in sorted(hosts.items()):
        types = {r["type"].split(".")[-1].lower() for r in rows}
        rs = [r for r in rows if r["choice_method"] not in ("", None)]
        last = last_cp(rows)

        def domain(r):
            return any(v.lower().rstrip("s") in types or v.lower() in types
                       for v in (r.get("binding_method_values") or "").split())
        th = lambda xs, k: [mean(num(r[k]) for r in xs if third(int(r["cp"]), last[r["chain_id"]]) == t) for t in (1, 2, 3)]
        out[arm] = {"rows": len(rs),
                    "domain_rows": sum(1 for r in rs if domain(r)),
                    "domain_thirds": th([r for r in rs if domain(r)], "choice_method"),
                    "other_thirds": th([r for r in rs if not domain(r)], "choice_method"),
                    "flow_methods_thirds": th([r for r in rs if r["choice_flow_methods"] not in ("", None)],
                                              "choice_flow_methods")}
    return out


def change_size(name: str) -> dict:
    """§6 (20 November 2026): a forced unit is a larger change. Per arm (on a history, per author
    group): the positions and methods of a unit with a placement forced at the class (no other class
    holding what it was bound to) and of one without; and the existing classes it went into, forced
    and not, among the units at or below the median number of methods and above it."""
    rows = _read(DATA / name / "h6.csv")
    out = {}
    groups = [(arm, [r for r in rows if r["arm"] == arm]) for arm in sorted({r["arm"] for r in rows})]
    chains = sorted({r["chain_id"] for r in rows})
    if 1 < len(chains) <= 10:       # a history's repositories one by one, as §6 quotes them
        groups += [(c, [r for r in rows if r["chain_id"] == c]) for c in chains]
    for arm, rs in groups:
        med = statistics.median(num(r["methods"]) for r in rs) if rs else 0
        part = lambda xs, k, forced: mean(num(r[k]) for r in xs if truth(r["forced_bind"]) == forced)
        small = [r for r in rs if num(r["methods"]) <= med]
        large = [r for r in rs if num(r["methods"]) > med]
        out[arm] = {"units": len(rs), "forced_units": sum(1 for r in rs if truth(r["forced_bind"])),
                    "positions": {"forced": part(rs, "positions", True), "not": part(rs, "positions", False)},
                    "methods": {"forced": part(rs, "methods", True), "not": part(rs, "methods", False)},
                    "median_methods": med,
                    "existing_classes_small": {"forced": part(small, "spread", True), "not": part(small, "spread", False)},
                    "existing_classes_large": {"forced": part(large, "spread", True), "not": part(large, "spread", False)}}
    return out


def problem_hosts(name: str) -> dict:
    """§4.4, §5 and §6 (16 and 17 November 2026): the problem-and-host rows. Per arm: the rows; the
    most problems one method received; the later arrivals at the method in all and in methods holding
    several problems; bindings and later arrivals a later checkpoint in new and in existing methods;
    later arrivals at the class, the method and on the problem's own lines, in all and a row; the
    bound rows and their later arrivals a bound row."""
    out = {}
    for arm, rows in sorted(chain_tables(name, "outcomes").items()):
        ident = Counter(r["identity"] for r in rows)
        rate = lambda xs: (sum(num(r["intrusion_method"]) for r in xs) / s) if (s := sum(num(r["later_checkpoints"]) for r in xs)) else None
        new = [r for r in rows if truth(r["host_new"])]
        old = [r for r in rows if not truth(r["host_new"])]
        bound = [r for r in rows if truth(r["bound"])]
        n = len(rows) or 1
        out[arm] = {
            "rows": len(rows), "most_problems_in_one_method": max(ident.values(), default=0),
            "arrivals_at_the_method": sum(num(r["intrusion_method"]) for r in rows),
            "in_methods_holding_several": sum(num(r["intrusion_method"]) for r in rows if ident[r["identity"]] > 1),
            "new_methods": {"bindings": mean(num(r["binding"]) for r in new), "arrivals_per_later_checkpoint": rate(new)},
            "existing_methods": {"bindings": mean(num(r["binding"]) for r in old), "arrivals_per_later_checkpoint": rate(old)},
            "arrivals": {k: sum(num(r[f"intrusion_{k}"]) for r in rows) for k in ("class", "method", "lines")},
            "arrivals_a_row": {k: sum(num(r[f"intrusion_{k}"]) for r in rows) / n for k in ("class", "method", "lines")},
            "bound_rows": len(bound),
            "arrivals_a_bound_row": {k: (sum(num(r[f"intrusion_{k}"]) for r in bound) / len(bound)) if bound else None
                                     for k in ("class", "method")},
        }
    return out


def bystanders(name: str) -> dict:
    """§6 (17 November 2026): what stood by runs into methods that existed. Per arm: the bystanders
    a run, and without constants, overall and over the thirds; at the class and at the method over
    the thirds; and in the class and the method that received most runs, at their first and last."""
    out = {}
    for arm, rows in sorted(chain_tables(name, "runs").items()):
        rs = [r for r in rows if not truth(r["host_new"]) and not truth(r["replacement"])]
        last = last_cp(rows)
        th = lambda k: [mean(num(r[k]) for r in rs if third(int(r["cp"]), last[r["chain_id"]]) == t) for t in (1, 2, 3)]

        def ends(key, k):
            groups: dict[str, list[dict]] = defaultdict(list)
            for r in rows:
                groups[key(r)].append(r)
            if not groups:
                return None
            g, xs = max(groups.items(), key=lambda kv: len(kv[1]))
            xs.sort(key=lambda r: int(r["cp"]))
            return {"place": g, "runs": len(xs), "first": num(xs[0][k]), "last": num(xs[-1][k])}
        out[arm] = {"runs": len(rs), "bystanders": mean(num(r["bystanders"]) for r in rs),
                    "without_constants": mean(num(r["bystanders_no_constants"]) for r in rs),
                    "thirds": th("bystanders"), "thirds_without_constants": th("bystanders_no_constants"),
                    "class_thirds": th("by_class"), "method_thirds": th("by_method"),
                    "busiest_class": ends(lambda r: r["type"], "by_class"),
                    "busiest_method": ends(lambda r: f"{r['type']} {r['name']}", "by_method")}
    return out


def busiest_method(name: str) -> dict:
    """§6 (18 November 2026): the method that received most bound problems. Per arm: its rows, its
    mean size, its mean cognitive complexity and its later arrivals at the method a hundred later
    checkpoints."""
    hosts = chain_tables(name, "hosts")
    out = {}
    for arm, rows in sorted(chain_tables(name, "outcomes").items()):
        bound = [r for r in rows if truth(r["bound"])]
        g = Counter((r["type"], r["name"]) for r in bound)
        if not g:
            continue
        (t, n), k = g.most_common(1)[0]
        xs = [r for r in bound if (r["type"], r["name"]) == (t, n)]
        hs = [h for h in hosts.get(arm, []) if (h["type"], h["name"]) == (t, n) and h.get("s4_cognitive") not in ("", None)]
        later = sum(num(r["later_checkpoints"]) for r in xs)
        out[arm] = {"method": f"{t.split('.')[-1]} {n}", "rows": k,
                    "size": mean(num(r["pre_positions"]) + num(r["net_added"]) for r in xs),
                    "cognitive": mean(num(h["s4_cognitive"]) for h in hs),
                    "arrivals_per_100_later_checkpoints": 100 * sum(num(r["intrusion_method"]) for r in xs) / later if later else None}
    return out


def class_rows(name: str) -> dict:
    """§6 (21 November 2026): H6's class rows. The class-and-checkpoint rows with a class shape, the
    rows of the busiest class, its share of the later arrivals at the class, its Gini at its first
    and last row, and within each class of five rows or more the rank correlation of its Gini with
    its later arrivals a later checkpoint."""
    rows = [r for r in _read(DATA / name / "h2.csv") if r.get("c_gini") not in ("", None)]
    by = defaultdict(list)
    for r in rows:
        by[r["class_identity"]].append(r)
    if not by:
        return {}
    busiest, xs = max(by.items(), key=lambda kv: len(kv[1]))
    xs.sort(key=lambda r: int(r["cp"]))
    total = sum(num(r["intrusion_class"]) for r in rows)
    rho = {}
    for c, ys in by.items():
        if len(ys) >= 5:
            r = spearman([num(y["c_gini"]) for y in ys],
                         [num(y["intrusion_class"]) / max(num(y["later_checkpoints"]), 1) for y in ys])
            if r is not None:
                rho[c] = r
    return {"rows": len(rows), "classes": len(by), "busiest": busiest, "busiest_rows": len(xs),
            "busiest_share_of_arrivals": sum(num(r["intrusion_class"]) for r in xs) / total if total else None,
            "busiest_gini_first": num(xs[0]["c_gini"]), "busiest_gini_last": num(xs[-1]["c_gini"]),
            "gini_against_arrivals": rho}


def fields_and_landings(name: str) -> dict:
    """§6 (19 November 2026): fields added to classes that existed, a checkpoint, where the
    checkpoint put unbound code into an existing class and where it did not; and the rank
    correlation, over checkpoints, of the fields added with those unbound landings."""
    adds, lands = chain_tables(name, "additions"), chain_tables(name, "landings")
    out = {}
    for arm in sorted(adds):
        n = Counter((r["chain_id"], r["cp"]) for r in lands.get(arm, [])
                    if not truth(r["bound"]) and r["destination"] in ("existing method", "new method"))
        rs = [(num(r["fields_added"]), n[(r["chain_id"], r["cp"])]) for r in adds[arm] if not truth(r.get("noop"))]
        out[arm] = {"with_an_unbound_landing": mean(f for f, k in rs if k),
                    "without": mean(f for f, k in rs if not k),
                    "rank_correlation": spearman([f for f, _ in rs], [k for _, k in rs])}
    return out


def junctions(name: str) -> dict:
    """§6 (16 November 2026): the junctions' share of cognitive complexity at the first and the last
    checkpoint, as conventionally read and injection-aware (PILOT.md)."""
    out = {}
    for arm, rows in sorted(chain_tables(name, "shape_series").items()):
        rows = sorted(rows, key=lambda r: int(r["cp"]))
        if rows:
            out[arm] = {k: [num(rows[0][k]), num(rows[-1][k])]
                        for k in ("junction_share", "junction_share_injection_aware")}
    return out


def size_or_data_by_arm(name: str) -> dict:
    """§6 (17 November 2026): size or data within each arm alone (from step 4's estimates)."""
    est = OUT / name / "estimates.json"
    if not est.exists():
        return {}
    rep = json.loads(est.read_text()).get("reported") or {}
    return {lev: (rep.get(f"size_or_data_{lev}") or {}).get("by_arm") for lev in ("class", "method")}


# ---- the histories (corpora B and C) ----

def repositories(name: str, analysis: dict) -> dict:
    """§6 (17 and 19 November 2026): each sample a history analysis reads, and each repository in it.
    Per sample: repositories drawn and usable. Per repository read: its commits, its declared agent
    commits and their agents, the units read; its class rows and their alternatives, the share bound
    to the class's own values, its method rows and their alternatives, and the share of calls the
    control flow followed."""
    out = {}
    for s in {x["sample"] for x in analysis["sources"]}:
        der = SAMPLES / s / "open-source-repository-sample.derivation.json"
        summary = json.loads(der.read_text()).get("summary", {}) if der.exists() else {}
        sample = {r["full_name"]: r for r in _read(SAMPLES / s / "open-source-repository-sample.csv")}
        repos = {}
        base = MEASURE / "_history" / s
        for d in sorted(p for p in base.iterdir() if p.is_dir() and (p / "meta.json").exists()) if base.exists() else []:
            full = d.name.replace("__", "/", 1)
            meta = json.loads((d / "meta.json").read_text())
            h = _read(d / "hosts.csv")
            cl = [r for r in h if r.get("choice_class") not in ("", None)]
            me = [r for r in h if r.get("choice_method") not in ("", None)]
            row = sample.get(full, {})
            apps = sum(num(r.get("calls_to_app_names")) for r in me)
            repos[full] = {"commits": row.get("n_commits"), "agent_commits": row.get("n_agent_commits"),
                           "agents": row.get("agents"), "units": meta.get("units"),
                           "class_rows": len(cl), "class_alternatives": mean(num(r["choice_class"]) for r in cl),
                           "own_share": mean(float(truth(r.get("choice_class_own"))) for r in cl),
                           "method_rows": len(me), "method_alternatives": mean(num(r["choice_method"]) for r in me),
                           "calls_followed": (sum(num(r.get("calls_followed")) for r in me) / apps) if apps else None}
        out[s] = {"drawn": summary.get("drawn"), "usable": summary.get("usable"), "repositories": repos}
    return out


# ---- timing ----

def timing(name: str) -> dict:
    """§5 and §6: how long step 4 took on this analysis, and one model fit by the size of the data
    on this machine (step 1b, ``results/timing.json``)."""
    out = {}
    t = OUT / name / "timing.json"
    if t.exists():
        out["step4"] = json.loads(t.read_text())
    f = runs.RESULTS / "timing.json"
    if f.exists():
        out["fits"] = json.loads(f.read_text())
    return out


PAIRED = (("files", files), ("new_methods", new_methods), ("trodden_thirds", trodden_thirds),
          ("injected_runs", injected_runs), ("bound_new_methods", bound_new_methods),
          ("alternatives_thirds", alternatives_thirds), ("change_size", change_size),
          ("problem_hosts", problem_hosts), ("bystanders", bystanders), ("busiest_method", busiest_method),
          ("class_rows", class_rows), ("fields_and_landings", fields_and_landings), ("junctions", junctions),
          ("size_or_data_by_arm", size_or_data_by_arm), ("timing", timing))
HISTORY = (("change_size", change_size), ("timing", timing))


def diagnose(analysis: dict) -> dict:
    name = analysis["name"]
    out = {k: f(name) for k, f in (HISTORY if analysis.get("history") else PAIRED)}
    if analysis.get("history"):
        out["repositories"] = repositories(name, analysis)
    return out


def _fmt(x) -> str:
    if isinstance(x, float):
        return f"{x:.3g}" if abs(x) < 1000 else f"{x:,.0f}"
    if isinstance(x, list):
        return "[" + ", ".join(_fmt(v) for v in x) + "]"
    return "–" if x is None else str(x)


def _lines(x, depth: int = 0) -> list[str]:
    pad = "  " * depth
    if isinstance(x, dict):
        out = []
        for k, v in x.items():
            if isinstance(v, dict):
                out += [f"{pad}- {k}:"] + _lines(v, depth + 1)
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                out += [f"{pad}- {k}:"] + [ln for item in v for ln in _lines(item, depth + 1)]
            else:
                out.append(f"{pad}- {k}: {_fmt(v)}")
        return out
    return [f"{pad}- {_fmt(x)}"]


def render(name: str, d: dict) -> str:
    funcs = dict(PAIRED + HISTORY)
    L = [f"# Diagnostics: {name}", "",
         "Every figure PLAN.md quotes that REPORT.md does not print, made by step 5 from the tables of steps 3 "
         "and 4 (PLAN.md 9 row 112). They describe and enter no verdict. Each section says where the plan "
         "quotes it; figures §6 recorded on an earlier `MEASURE_VERSION` may differ from these.", ""]
    for k, v in d.items():
        doc = (funcs.get(k) or repositories).__doc__ or ""
        L += [f"## {k}", "", " ".join(doc.split()), ""] + (_lines(v) if v else ["- (no data)"]) + [""]
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", nargs="*")
    a, _ = ap.parse_known_args()
    reg = runs.load()
    for analysis in reg["analyses"]:
        name = analysis["name"]
        if (a.analysis and name not in a.analysis) or not (OUT / name / "estimates.json").exists():
            continue
        d = diagnose(analysis)
        (OUT / name / "diagnostics.json").write_text(json.dumps(d, indent=1, default=str) + "\n")
        (OUT / name / "DIAGNOSTICS.md").write_text(render(name, d))
        print(f"{name}: {OUT / name / 'DIAGNOSTICS.md'}")


if __name__ == "__main__":
    main()

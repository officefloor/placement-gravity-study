"""The instrument checked against the compiler (PLAN.md §4.8, reported).

The instrument resolves names lexically, with no symbol solver: a call goes to the methods of that
name in the class its receiver is declared as (``flow.Graph``), and a name on an added line is a
field of the class when the method has no value of that name (``Pull.java``). The compiler resolves
them properly. Corpus A's code compiles, so for a sample of each chain's checkpoints the tree is
given to javac (``instrument/Check.java``) and the two readings are set side by side:

- **calls:** per method, the application's methods it calls, as the instrument follows them and as
  the compiler resolves them. *Precision*: of the instrument's calls, the share the compiler
  confirms. *Recall*: of the compiler's calls that could be followed (to a method with a body in
  the tree), the share the instrument has. A call goes to a class and a name; a class agrees with
  the one the compiler names when it is that class, one it extends or implements, or one that
  extends or implements it (the instrument follows a call to every override that may run). The
  instrument's family of a class also holds its siblings (it is closed over both directions), which
  no call can reach; *strict precision* counts a call as confirmed only on the compiler's class,
  its ancestors and its descendants, so the gap between the two is that over-reach.
- **field reads:** per method, the other classes' fields it reads or writes, the same two shares.
- **bound names:** per host of the checkpoint, the names the instrument counted as bindings: a
  parameter or local of the method, a field of its class, a method of its class. Of each kind, the
  share the compiler agrees is that in the method as it stands after the change. (Only precision:
  the instrument counts the names on the lines a change added, and the compiler reads the method
  whole.)

What the compiler could not resolve itself is never held against the instrument: a call of the
instrument's that the compiler left unresolved is *unverified*, counted apart. Without the
project's libraries on the classpath their types are errors to javac and more is left unresolved;
the classpath is taken from the project's own build where Maven can give it offline.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from . import chain, flow

#: Every EVERY-th checkpoint of a chain is checked, and its last.
EVERY = 5
CLASSES = chain.ROOT / "instrument" / "classes"


def classpath(repo: Path, rev: str, java_src: str) -> str:
    """The project's libraries as its own build names them (``mvn dependency:build-classpath``,
    offline, on the pom beside the production Java at rev). Empty where there is no pom, Maven is
    not there, or it cannot resolve offline: the check then runs without it, and says so."""
    project = java_src.split("src/main/java")[0]
    try:
        pom = chain.git(repo, "show", f"{rev}:{project}pom.xml")
    except subprocess.CalledProcessError:
        return ""
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "pom.xml").write_text(pom)
        try:
            subprocess.run(["mvn", "-o", "-q", "-f", str(Path(d) / "pom.xml"), "dependency:build-classpath",
                            "-Dmdep.outputFile=" + str(Path(d) / "cp.txt")],
                           check=True, capture_output=True, timeout=300)
            return (Path(d) / "cp.txt").read_text().strip()
        except (subprocess.SubprocessError, OSError):
            return ""


def sampled(checkpoints: list[dict], every: int = EVERY) -> list[str]:
    real = [c for c in checkpoints if not c.get("noop")]
    keep = [c for i, c in enumerate(real) if i % every == every - 1]
    if real and real[-1] not in keep:
        keep.append(real[-1])
    return [f"cp{c['cp']:02d}" for c in keep]


def compiled(listing: list[tuple[str, Path]], work: Path, cp: str = "") -> tuple[dict, dict]:
    """javac's reading of each listed tree: label -> {(path, type, signature): method}, and label ->
    the tree's record (files, compiler errors)."""
    work.mkdir(parents=True, exist_ok=True)
    (work / "check.tsv").write_text("".join(f"{label}\t{d}\n" for label, d in listing))
    subprocess.run(["java", "-cp", str(CLASSES), "Check", str(work / "check.tsv"), str(work / "check.jsonl"),
                    *([cp] if cp else [])], check=True)
    methods: dict[str, dict] = {}
    trees: dict[str, dict] = {}
    for r in (json.loads(l) for l in (work / "check.jsonl").read_text().splitlines() if l):
        if r["kind"] == "tree":
            trees[r["label"]] = r
        else:
            methods.setdefault(r["label"], {})[(r["path"], r["type"], r["signature"])] = r
    return methods, trees


def _find(theirs: dict, path: str, type_: str, signature: str, name: str, params) -> dict | None:
    """The compiler's method for one of the instrument's: by its signature as written, or, where the
    two write a parameter's type differently, by its name and number of parameters if that is one."""
    type_ = flow._t(type_)
    m = theirs.get((path, type_, signature))
    if m is not None:
        return m
    same = [v for (p, t, _), v in theirs.items() if p == path and t == type_ and v["name"] == name
            and (params is None or int(params) in (v["params"], -1))]
    return same[0] if len(same) == 1 else None


def _line(g: flow.Graph, c: str) -> set[str]:
    """A class, its ancestors and its descendants: where a call declared on it can really go."""
    out = {c}
    for edges in (g.supers, g.subs):
        todo = [c]
        while todo:
            for y in edges.get(todo.pop(), ()):
                if y not in out:
                    out.add(y)
                    todo.append(y)
    return out


def calls(index: dict, theirs: dict) -> dict:
    """The instrument's calls and field reads of one tree against the compiler's (see the module's
    text). ``cross_*`` are those that leave the method's class: what H7 and H5 count."""
    g = flow.Graph(index)
    paths = [p for p, f in index.get("files", {}).items() for _ in f.get("methods", [])]
    bodies: dict[str, set[str]] = {}
    for m in g.methods:
        bodies.setdefault(m.get("name") or m["signature"].split("(")[0], set()).add(flow.simple(m["type"]))
    n = dict.fromkeys(("methods", "methods_matched", "calls", "calls_confirmed", "calls_unverified",
                       "calls_compiler", "calls_found", "calls_no_body", "calls_unresolved",
                       "calls_strict", "cross_calls", "cross_confirmed", "cross_strict", "cross_compiler",
                       "cross_found",
                       "reads", "reads_confirmed", "reads_compiler", "reads_found"), 0)
    for i, m in enumerate(g.methods):
        n["methods"] += 1
        name = m.get("name") or m["signature"].split("(")[0]
        c = _find(theirs, paths[i], m["type"], m["signature"], name, m.get("params"))
        if c is None:
            continue
        n["methods_matched"] += 1
        own = flow.simple(m["type"])
        mine = {(flow.simple(g.methods[j]["type"]), g.methods[j].get("name") or g.methods[j]["signature"].split("(")[0])
                for j in g.out[i]}
        app = {(x.split("|")[1], x.split("|")[2]) for x in c["calls"] if x.startswith("app|")}
        loose = {x.split("|")[2] for x in c["calls"] if x.startswith("?|")}
        n["calls_unresolved"] += sum(1 for x in loose if x in bodies)
        for cls, nm in mine:
            ok = any(nm == n2 and cls in g.family(c2) for c2, n2 in app)
            strict = any(nm == n2 and cls in _line(g, c2) for c2, n2 in app)
            n["calls"] += 1
            n["calls_confirmed"] += ok
            n["calls_strict"] += strict
            n["calls_unverified"] += (not ok) and nm in loose
            if cls != own:
                n["cross_calls"] += 1
                n["cross_confirmed"] += ok
                n["cross_strict"] += strict
        for cls, nm in app:
            family = g.family(cls)
            if not (bodies.get(nm, set()) & family):
                n["calls_no_body"] += 1        # an interface's method with no body in the tree
                continue
            found = any(nm == n2 and c2 in family for c2, n2 in mine)
            n["calls_compiler"] += 1
            n["calls_found"] += found
            if cls != own:
                n["cross_compiler"] += 1
                n["cross_found"] += found
        mine_r = {(cls, f[1:]) for cls, f in g.reads[i] if cls != own}
        app_r = {(x.split("|")[1], x.split("|")[2]) for x in c["reads"] if x.startswith("app|")}
        app_r = {(cls, nm) for cls, nm in app_r if cls != own}
        for cls, nm in mine_r:
            n["reads"] += 1
            n["reads_confirmed"] += any(nm == n2 and cls in g.family(c2) for c2, n2 in app_r)
        for cls, nm in app_r:
            n["reads_compiler"] += 1
            n["reads_found"] += any(nm == n2 and c2 in g.family(cls) for c2, n2 in mine_r)
    return n


def bound(records: list[dict], unit: str, theirs: dict) -> dict:
    """The names the instrument counted as bindings in the hosts of one unit, against what the
    compiler says each is in the method after the change."""
    n = dict.fromkeys(("hosts", "hosts_matched", "names_method", "names_method_confirmed", "names_field",
                       "names_field_confirmed", "names_class_method", "names_class_method_confirmed"), 0)
    wrong = []
    for r in records:
        if r.get("kind") != "host" or r["unit"] != unit or not r.get("runs"):
            continue
        n["hosts"] += 1
        c = _find(theirs, r["path"], r["type"], r["signature"], r["name"], None)
        if c is None:
            continue
        n["hosts_matched"] += 1
        for key, theirs_key, col in (("binding_method", "locals", "names_method"),
                                     ("binding_field", "own_fields", "names_field"),
                                     ("binding_class_method", "own_methods", "names_class_method")):
            for v in sorted({v for x in r["runs"] for v in x.get(key, [])}):
                ok = v in c[theirs_key]
                n[col] += 1
                n[f"{col}_confirmed"] += ok
                if not ok:
                    wrong.append(f"{flow.simple(r['type'])}#{r['name']}:{key.split('_', 1)[1]}:{v}")
    return {**n, "names_wrong": " ".join(wrong[:20])}


def rows(arm: str, chain_name: str, repo: Path, rev: str, java_src: str, measured: dict, work: Path,
         every: int = EVERY) -> list[dict]:
    """One row per checked checkpoint of a chain: the calls and field reads of the tree before it
    (the tree the instrument's places are read on) and the bound names of its hosts in the tree
    after it. ``work`` is the chain's working directory, with each unit's ``prior`` and ``tree``."""
    units = [u for u in sampled(measured["checkpoints"], every)
             if (work / u / "prior").exists() and (work / u / "tree").exists()]
    if not units:
        return []
    cp = classpath(repo, rev, java_src)
    listing = [(f"{u}:{side}", work / u / side) for u in units for side in ("prior", "tree")]
    methods, trees = compiled(listing, work / "check", cp)
    out = []
    for u in units:
        before, after = trees.get(f"{u}:prior", {}), trees.get(f"{u}:tree", {})
        out.append({"arm": arm, "chain": chain_name, "cp": int(u[2:]), "classpath": bool(cp),
                    "files": before.get("files", 0), "compiler_errors": before.get("errors", 0),
                    "compiler_errors_after": after.get("errors", 0),
                    **calls(measured["places"].get(u, {}), methods.get(f"{u}:prior", {})),
                    **bound(measured["records"], u, methods.get(f"{u}:tree", {}))})
    return out


#: The tripwire (decided by the author on 23 November 2026, PLAN.md 4.8): no pass mark, but the
#: report says so prominently where the instrument's calls agree with the compiler's on less than
#: LOW of them in an arm, or where the arms differ by more than GAP. Nothing fails by it.
LOW = 0.90
GAP = 0.05
TRIPPED = ("calls_precision", "calls_recall", "cross_precision", "cross_recall")


def flags(summary_: dict) -> list[str]:
    """What the tripwire catches in a summary: a share of calls below LOW in an arm, and a share
    that differs between two arms by more than GAP (which would tilt every contrast of the arms)."""
    names = {"calls_precision": "precision of calls", "calls_recall": "recall of calls",
             "cross_precision": "precision of calls leaving the class",
             "cross_recall": "recall of calls leaving the class"}
    out = []
    for k in TRIPPED:
        have = {arm: a[k] for arm, a in summary_.items() if a.get(k) is not None}
        for arm, v in sorted(have.items()):
            if v < LOW:
                out.append(f"{names[k]} {v:.3f} in the {arm} arm, below {LOW:.2f}")
        if len(have) > 1 and max(have.values()) - min(have.values()) > GAP:
            hi, lo = max(have, key=have.get), min(have, key=have.get)
            out.append(f"{names[k]} differs between the arms by more than {GAP:.2f}: "
                       f"{hi} {have[hi]:.3f}, {lo} {have[lo]:.3f}")
    return out


def summary(rows_: list[dict]) -> dict:
    """Per arm, over the checked checkpoints of all chains: each count summed, and the shares."""
    out: dict[str, dict] = {}
    for r in rows_:
        a = out.setdefault(r["arm"], {"checkpoints": 0, "chains": set(), "with_classpath": 0})
        a["checkpoints"] += 1
        a["chains"].add(r.get("chain_id") or r.get("chain"))
        a["with_classpath"] += str(r.get("classpath")) == "True"
        for k, v in r.items():
            if k in ("files", "compiler_errors") or k.startswith(("methods", "calls", "cross", "reads", "hosts", "names_")):
                if k != "names_wrong":
                    a[k] = a.get(k, 0) + int(float(v or 0))
    for a in out.values():
        a["chains"] = len(a["chains"])

        def share(x, y):
            return a.get(x, 0) / a[y] if a.get(y) else None
        a.update({"calls_precision": share("calls_confirmed", "calls"),
                  "calls_recall": share("calls_found", "calls_compiler"),
                  "calls_strict_precision": share("calls_strict", "calls"),
                  "cross_precision": share("cross_confirmed", "cross_calls"),
                  "cross_strict_precision": share("cross_strict", "cross_calls"),
                  "cross_recall": share("cross_found", "cross_compiler"),
                  "reads_precision": share("reads_confirmed", "reads"),
                  "reads_recall": share("reads_found", "reads_compiler"),
                  "names_method_precision": share("names_method_confirmed", "names_method"),
                  "names_field_precision": share("names_field_confirmed", "names_field"),
                  "names_class_method_precision": share("names_class_method_confirmed", "names_class_method"),
                  "methods_matched_share": share("methods_matched", "methods"),
                  "hosts_matched_share": share("hosts_matched", "hosts")})
    return out

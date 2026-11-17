"""The literature's shape measures, on every method and every class of a checkpoint's tree
(PLAN.md §4.7a). Computed by the tools the petclinic harness uses, at the same pins:

- **CK 0.7.0** (Aniche): per class, WMC, LCOM, LCOM*, TCC, LCC, CBO, RFC, DIT and fan-out
  (Chidamber and Kemerer 1994; Bieman and Kang 1995); per method, cyclomatic complexity (McCabe
  1976), the deepest nesting, and fan-out.
- **PMD 7.27.0** with ``instrument/pmd-metrics.xml``: per method, NPath (Nejmeh 1988) and Law of
  Demeter violations (Lieberherr 1989); per class, the God Class and Data Class detectors (Lanza
  and Marinescu 2006) and the import count.
- **Halstead volume** (Halstead 1977) and the **Maintainability Index** (Oman and Hagemeister
  1992; 171 − 5.2 ln V − 0.23 CC − 16.2 ln LOC), here, over the method's or the class's own text.
- **jscpd 5.0.14**, when present: the share of a method's, or a class's, lines that are in a clone.

Method measures carry the prefix ``m_`` and class measures ``c_``. A tool that did not run leaves
its measures empty, never zero.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import subprocess
import tempfile
from pathlib import Path

from . import chain

LIB = chain.ROOT / "lib"
CK_JAR = Path(os.environ.get("PG_CK_JAR", LIB / "ck.jar"))
PMD_BIN = Path(os.environ.get("PG_PMD_BIN", LIB / "pmd" / "bin" / "pmd"))
JSCPD_BIN = Path(os.environ.get("PG_JSCPD_BIN", LIB / "node_modules" / ".bin" / "jscpd"))
RULESET = chain.ROOT / "instrument" / "pmd-metrics.xml"

#: name -> (level, kind, source). kind: "level" (log(1 + x), standardised), "plain" (standardised
#: as it is: a ratio or an index) or "flag" (present or absent).
MEASURES = {
    "m_cyclomatic": ("method", "level", "McCabe 1976 (CK)"),
    "m_npath": ("method", "level", "Nejmeh 1988 (PMD)"),
    "m_nesting": ("method", "level", "deepest nested block (CK)"),
    "m_fanout": ("method", "level", "fan-out (CK)"),
    "m_halstead": ("method", "level", "Halstead 1977, volume"),
    "m_mi": ("method", "plain", "Maintainability Index"),
    "m_demeter": ("method", "flag", "Lieberherr 1989 (PMD)"),
    "m_duplicated": ("method", "flag", "clone lines (jscpd)"),
    "c_wmc": ("class", "level", "Chidamber and Kemerer 1994 (CK)"),
    "c_lcom_star": ("class", "plain", "lack of cohesion, normalised (CK)"),
    "c_tcc": ("class", "plain", "Bieman and Kang 1995 (CK)"),
    "c_cbo": ("class", "level", "Chidamber and Kemerer 1994 (CK)"),
    "c_rfc": ("class", "level", "Chidamber and Kemerer 1994 (CK)"),
    "c_dit": ("class", "level", "Chidamber and Kemerer 1994 (CK)"),
    "c_fanout": ("class", "level", "fan-out (CK)"),
    "c_imports": ("class", "level", "import count (PMD)"),
    "c_halstead": ("class", "level", "Halstead 1977, volume"),
    "c_mi": ("class", "plain", "Maintainability Index"),
    "c_god_class": ("class", "flag", "Lanza and Marinescu 2006 (PMD)"),
    "c_data_class": ("class", "flag", "Lanza and Marinescu 2006 (PMD)"),
    "c_demeter": ("class", "flag", "Lieberherr 1989 (PMD)"),
    "c_duplicated": ("class", "flag", "clone lines (jscpd)"),
}
#: Measures where a higher value is the better shape: read reversed, so that a rate ratio above 1
#: always means the worse shape is followed by more.
REVERSED = ("m_mi", "c_mi", "c_tcc")
METHOD = [k for k, v in MEASURES.items() if v[0] == "method"]
CLASS = [k for k, v in MEASURES.items() if v[0] == "class"]

_TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\d[\w.]*|[A-Za-z_$][\w$]*|'
                    r'>>>=|<<=|>>=|>>>|->|::|\+\+|--|&&|\|\||[=!<>+\-*/%&|^]=|<<|>>|[^\s\w]')
_KEYWORDS = set("""abstract assert break case catch class continue default do else enum extends
final finally for if implements import instanceof interface native new package private protected
public return static strictfp super switch synchronized this throw throws transient try void
volatile while var record yield""".split())
_COMMENT = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
_DECL = re.compile(r"\b(?:class|interface|enum|record)\s+([A-Za-z_$][\w$]*)")


def halstead(text: str) -> float:
    """Halstead volume, N log2 n: N the operators and operands in the text, n the distinct ones.
    Operands are identifiers and literals; operators are keywords and symbols."""
    tokens = _TOKEN.findall(_COMMENT.sub(" ", text))
    return round(len(tokens) * math.log2(len(set(tokens))), 2) if len(set(tokens)) > 1 else 0.0


def maintainability(volume: float, cyclomatic: float, lines: int) -> float | None:
    if volume <= 0 or lines <= 0:
        return None
    return round(171 - 5.2 * math.log(volume) - 0.23 * cyclomatic - 16.2 * math.log(lines), 2)


def _num(x) -> float | None:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if v == v and v >= 0 else None      # CK writes NaN and -1 for "not applicable"


def run_ck(tree: Path) -> tuple[list[dict], list[dict]] | None:
    """(classes, methods) as CK reads the tree; paths relative to it. None if CK did not run."""
    if not CK_JAR.is_file():
        return None
    with tempfile.TemporaryDirectory(prefix="ck_") as out:
        p = subprocess.run(["java", "-jar", str(CK_JAR), str(tree), "false", "0", "true", out + os.sep],
                           capture_output=True, text=True)
        if p.returncode != 0 or not (Path(out) / "class.csv").is_file():
            return None

        def read(name):
            f = Path(out) / name
            if not f.is_file():
                return []
            with f.open(encoding="utf-8", errors="replace") as fh:
                rows = list(csv.DictReader(fh))
            for r in rows:
                r["path"] = os.path.relpath(r["file"], tree)
            return rows
        return read("class.csv"), read("method.csv")


def run_pmd(tree: Path) -> list[dict] | None:
    """PMD's violations as {path, line, end, rule, text}; None if PMD did not run."""
    if not PMD_BIN.is_file() or not RULESET.is_file():
        return None
    p = subprocess.run([str(PMD_BIN), "check", "-f", "json", "-R", str(RULESET),
                        "--no-fail-on-violation", "--no-progress", "--no-cache", "-d", "."],
                       cwd=tree, capture_output=True, text=True)
    if p.returncode != 0:
        return None
    try:
        doc = json.loads(p.stdout or "{}")
    except json.JSONDecodeError:
        return None
    out = []
    for f in doc.get("files", []):
        path = os.path.relpath(os.path.join(tree, f["filename"]), tree)
        for v in f["violations"]:
            out.append({"path": path, "line": v["beginline"], "end": v["endline"],
                        "rule": v["rule"], "text": v["description"]})
    return out


def run_jscpd(tree: Path) -> dict[str, set[int]] | None:
    """Path -> the lines that are in a clone; None if jscpd is not installed or did not run."""
    if not JSCPD_BIN.is_file():
        return None
    with tempfile.TemporaryDirectory(prefix="jscpd_") as out:
        subprocess.run([str(JSCPD_BIN), "--mode", "strict", "--reporters", "json", "--silent",
                        "--output", out, "--format", "java", str(tree)],
                       cwd=tree, capture_output=True, text=True)
        report = Path(out) / "jscpd-report.json"
        if not report.is_file():
            return None
        doc = json.loads(report.read_text())
    lines: dict[str, set[int]] = {}
    for d in doc.get("duplicates", []):
        for side in ("firstFile", "secondFile"):
            f = d[side]
            name = f["name"] if os.path.isabs(f["name"]) else os.path.join(tree, f["name"])
            lines.setdefault(os.path.relpath(name, tree), set()).update(range(f["start"], f["end"] + 1))
    return lines


def _first_number(text: str) -> float | None:
    m = re.search(r"(?:of|value of|imports \()\s*(\d+)", text)
    return float(m.group(1)) if m else None


def measure(tree: Path, methods: list[dict]) -> None:
    """Adds the ``m_`` and ``c_`` measures to each shape record of one tree (``Pull --shape``'s
    methods of it: path, type, name, decl_line, end_line)."""
    ck = run_ck(tree)
    pmd = run_pmd(tree)
    clones = run_jscpd(tree)
    texts: dict[str, list[str]] = {}

    def lines_of(path: str) -> list[str]:
        if path not in texts:
            raw = (tree / path).read_bytes()
            try:
                texts[path] = raw.decode("utf-8").splitlines()
            except UnicodeDecodeError:
                texts[path] = raw.decode("iso-8859-1").splitlines()
        return texts[path]

    def simple(name: str) -> str:
        return re.split(r"[.$]", name)[-1]

    ck_methods: dict[str, list[dict]] = {}
    ck_classes: dict[tuple[str, str], dict] = {}
    if ck:
        for c in ck[0]:
            ck_classes.setdefault((c["path"], simple(c["class"])), c)
        for m in ck[1]:
            ck_methods.setdefault(m["path"], []).append(m)
    by_path: dict[str, list[dict]] = {}
    for v in pmd or []:
        by_path.setdefault(v["path"], []).append(v)

    def class_of_line(path: str, line: int) -> str | None:
        src = lines_of(path)
        m = _DECL.search(src[line - 1]) if 0 < line <= len(src) else None
        return m.group(1) if m else None

    # ---- class measures, once per (path, type)
    classes: dict[tuple[str, str], dict] = {}
    spans: dict[tuple[str, str], list[tuple[int, int]]] = {}
    for r in methods:
        spans.setdefault((r["path"], r["type"]), []).append((r["decl_line"], r["end_line"]))
    for (path, type_), ranges in spans.items():
        name = simple(type_)
        c = ck_classes.get((path, name))
        row = {k: None for k in CLASS}
        if c:
            row.update({"c_wmc": _num(c["wmc"]), "c_lcom_star": _num(c["lcom*"]), "c_tcc": _num(c["tcc"]),
                        "c_cbo": _num(c["cbo"]), "c_rfc": _num(c["rfc"]), "c_dit": _num(c["dit"]),
                        "c_fanout": _num(c["fanout"])})
        if pmd is not None:
            mine = [v for v in by_path.get(path, [])]
            named = lambda v: class_of_line(path, v["line"]) == name
            row["c_god_class"] = any(v["rule"] == "GodClass" and named(v) for v in mine)
            row["c_data_class"] = any(v["rule"] == "DataClass" and named(v) for v in mine)
            row["c_imports"] = next((_first_number(v["text"]) for v in mine
                                     if v["rule"] == "ExcessiveImports"), 0.0)
            row["c_demeter"] = any(v["rule"] == "LawOfDemeter" and any(a <= v["line"] <= b for a, b in ranges)
                                   for v in mine)
        lo, hi = min(a for a, _ in ranges), max(b for _, b in ranges)
        body = "\n".join(lines_of(path)[lo - 1:hi])
        row["c_halstead"] = halstead(body)
        if row["c_wmc"] is not None:
            row["c_mi"] = maintainability(row["c_halstead"], row["c_wmc"], hi - lo + 1)
        if clones is not None:
            row["c_duplicated"] = any(a <= x <= b for x in clones.get(path, ()) for a, b in ranges)
        classes[(path, type_)] = row

    # ---- method measures
    for r in methods:
        path, a, b = r["path"], r["decl_line"], r["end_line"]
        row = {k: None for k in METHOD}
        cm = [m for m in ck_methods.get(path, [])
              if a <= int(m["line"]) <= b and m["method"].split("/")[0] in (r["name"], simple(r["type"]))]
        if cm:
            m = min(cm, key=lambda m: int(m["line"]))
            row.update({"m_cyclomatic": _num(m["wmc"]), "m_nesting": _num(m["maxNestedBlocksQty"]),
                        "m_fanout": _num(m["fanout"])})
        if pmd is not None:
            inside = [v for v in by_path.get(path, []) if a <= v["line"] <= b]
            npath = [v for v in inside if v["rule"] == "NPathComplexity"]
            if npath:
                row["m_npath"] = _first_number(min(npath, key=lambda v: v["line"])["text"])
            row["m_demeter"] = any(v["rule"] == "LawOfDemeter" for v in inside)
        body = "\n".join(lines_of(path)[a - 1:b])
        row["m_halstead"] = halstead(body)
        if row["m_cyclomatic"] is not None:
            row["m_mi"] = maintainability(row["m_halstead"], row["m_cyclomatic"], b - a + 1)
        if clones is not None:
            row["m_duplicated"] = any(a <= x <= b for x in clones.get(path, ()))
        r.update(row)
        r.update(classes[(path, r["type"])])


def attach(methods: list[dict], trees: dict[str, Path]) -> None:
    """``measure`` for every unit's tree."""
    by_unit: dict[str, list[dict]] = {}
    for r in methods:
        by_unit.setdefault(r["unit"], []).append(r)
    for unit, rs in by_unit.items():
        measure(Path(trees[unit]), rs)

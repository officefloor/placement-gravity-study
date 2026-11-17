"""RefactoringMiner's findings as hints for the instrument (PLAN.md §4.1).

RefactoringMiner 3.0.4 (the version CodeTracker 2.6 pins) is run at each checkpoint's agent commit
by ``refactor/`` (``Refactorings.java``). Its findings become four kinds of hint, each a line of
the instrument's HINTS.tsv:

- ``method`` / ``type``: the same method or type before and after a rename, move or change of
  signature, so the host stays matched;
- ``rename``: a variable, parameter, field, method or type renamed. The instrument applies it to
  the before version first, so a renamed value is still a pre-existing value and a line that only
  renames is not an edit;
- ``moved``: lines holding code a refactoring moved or restructured (extracted, inlined, a loop
  turned into a pipeline, a condition inverted). Those lines are re-placement, not addition. Code
  RefactoringMiner reports as *added* inside an extracted method stays an addition.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "refactor"
JAVA_SRC = "src/main/java/"

#: Right-side locations that hold moved or restructured code.
MOVED = {
    "extracted code to extracted method declaration",
    "extracted method invocation",
    "inlined code in target method declaration",
    "extracted variable declaration",
    "statement with the name of the extracted variable",
    "statement with the initializer of the inlined variable",
    "pipeline code",
    "loop code",
    "inverted conditional",
    "new variable declaration",
    "split method declaration",
    "merged method declaration",
}

VALUE_RENAMES = re.compile(
    r"^(?:Rename Variable|Rename Parameter|Localize Parameter|Parameterize Variable|"
    r"Replace Variable With Attribute|Parameterize Attribute) (\w+) : .*? to (\w+) : ")
FIELD_RENAME = re.compile(r"^Rename Attribute (\w+) : .*? to (\w+) : ")
METHOD_NAME = re.compile(r"(\w+)\(")
SAME_METHOD_LEFT = {"original method declaration", "source method declaration before extraction",
                    "target method declaration before inline"}


def run(repo: Path, units: list[tuple[str, str]], out: Path) -> list[dict]:
    """RefactoringMiner at each (unit, commit); its raw output is kept at ``out``."""
    listing = out.with_suffix(".tsv")
    listing.write_text("".join(f"{u}\t{c}\n" for u, c in units))
    cp = f"{MODULE / 'target' / 'classes'}:{MODULE / 'target' / 'lib'}/*"
    subprocess.run(["java", "-cp", cp, "Refactorings", str(repo), str(listing), str(out)],
                   check=True, capture_output=True)
    return [json.loads(l) for l in out.read_text().splitlines() if l]


_TEST = re.compile(r"(^|/)(src/test|tests?|testing|it|androidTest|jmh)(/|$)", re.I)


def production(path: str) -> bool:
    """A production Java file: a .java file not under a test directory. (Until 18 November 2026
    this asked for the petclinic root, ``src/main/java/``, which dropped every hint of a stack
    whose backend sits elsewhere.)"""
    return path.endswith(".java") and not _TEST.search(path)


def _java(loc: dict) -> bool:
    return production(loc["filePath"])


def _rel(path: str) -> str:
    """Paths as the manifest gives them: relative to the repository root."""
    return path


def _mid(loc: dict) -> int:
    return (loc["startLine"] + loc["endLine"]) // 2


def hints(found: dict) -> list[str]:
    """The HINTS.tsv lines for one unit's findings (paths relative to the repository, as the
    manifest's are)."""
    unit, out = found["unit"], []
    for r in found["refactorings"]:
        left = [l for l in r["leftSideLocations"] if _java(l)]
        right = [l for l in r["rightSideLocations"] if _java(l)]
        if not left and not right:
            continue
        kind, desc = r["type"], r["description"]
        # the same method before and after
        lm = [l for l in left if l["codeElementType"] == "METHOD_DECLARATION"]
        rm = [l for l in right if l["codeElementType"] == "METHOD_DECLARATION"]
        if kind in ("Extract Method", "Inline Method", "Extract And Move Method"):
            lm = [l for l in lm if l["description"] in SAME_METHOD_LEFT]
            rm = [l for l in rm if "after extraction" in l["description"]
                  or "after inline" in l["description"]]
        if len(lm) == 1 and len(rm) == 1 and kind != "Split Method":
            out.append(f"{unit}\tmethod\t{_rel(lm[0]['filePath'])}\t{_mid(lm[0])}"
                       f"\t{_rel(rm[0]['filePath'])}\t{_mid(rm[0])}")
        # the same type before and after
        lt = [l for l in left if l["codeElementType"] in ("TYPE_DECLARATION",)]
        rt = [l for l in right if l["codeElementType"] in ("TYPE_DECLARATION",)]
        if len(lt) == 1 and len(rt) == 1 and kind in ("Rename Class", "Move Class",
                                                       "Move And Rename Class",
                                                       "Change Type Declaration Kind"):
            out.append(f"{unit}\ttype\t{_rel(lt[0]['filePath'])}\t{lt[0]['startLine']}"
                       f"\t{_rel(rt[0]['filePath'])}\t{rt[0]['startLine']}")
        # renames
        if m := VALUE_RENAMES.match(desc):
            decl = next((l for l in right if "declaration" in l["description"]), right[0] if right else None)
            if decl:
                out.append(f"{unit}\trename\tvalue\t{_rel(decl['filePath'])}\t{decl['startLine']}"
                           f"\t{m.group(1)}\t{m.group(2)}")
        elif m := FIELD_RENAME.match(desc):
            if right:
                out.append(f"{unit}\trename\tfield\t{_rel(right[0]['filePath'])}\t{right[0]['startLine']}"
                           f"\t{m.group(1)}\t{m.group(2)}")
        elif kind in ("Rename Method", "Move And Rename Method") and lm and rm:
            a = METHOD_NAME.search(lm[0].get("codeElement") or "")
            b = METHOD_NAME.search(rm[0].get("codeElement") or "")
            if a and b and a.group(1) != b.group(1):
                out.append(f"{unit}\trename\tmember\t-\t0\t{a.group(1)}\t{b.group(1)}")
        elif kind in ("Rename Class", "Move And Rename Class") and lt and rt:
            a = (lt[0].get("codeElement") or "").split(".")[-1]
            b = (rt[0].get("codeElement") or "").split(".")[-1]
            if a and b and a != b:
                out.append(f"{unit}\trename\tmember\t-\t0\t{a}\t{b}")
        # moved or restructured code
        for l in right:
            if l["description"] in MOVED:
                out.append(f"{unit}\tmoved\t{_rel(l['filePath'])}\t{l['startLine']}\t{l['endLine']}")
    return out

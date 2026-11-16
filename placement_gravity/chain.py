"""Measure one chain of a degradation-harness run: every checkpoint's addition (PLAN.md §4).

A chain is a branch ``evolve/<run>/<strategy>/<arm>/chain<n>``. Each checkpoint k is a commit
``cpNN agent <id>`` (the agent's change) followed by ``cpNN reset <id>`` (the harness's capture).
The addition of checkpoint k is the diff from the agent commit's parent to the agent commit,
restricted to production Java (``src/main/java``). The wiring of the OfficeFloor arm is read from
``src/main/resources/officefloor/**/*.yml`` at both ends of the same diff.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from . import refactor, shape

ROOT = Path(__file__).resolve().parent.parent
CLASSPATH = f"{ROOT / 'lib' / 'officefloorslim.jar'}:{ROOT / 'instrument' / 'classes'}"
JAVA_SRC = "src/main/java/"
WIRING = "src/main/resources/officefloor/"
AGENT = re.compile(r"^cp(\d+) agent (\S+)$")
RESET = re.compile(r"^cp(\d+) reset (\S+)$")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True).stdout


@dataclass
class Checkpoint:
    cp: int
    rule: str
    commit: str
    parent: str
    noop: bool = False


def checkpoints(repo: Path, branch: str, base_ref: str) -> list[Checkpoint]:
    """The agent commit of each checkpoint. A checkpoint with a reset commit but no agent commit is a
    no-op (the agent changed nothing; the harness makes no empty commit): its addition is empty."""
    base = git(repo, "merge-base", branch, base_ref).strip()
    agents, resets = {}, {}
    for line in git(repo, "log", "--reverse", "--format=%H %P %s", f"{base}..{branch}").splitlines():
        sha, rest = line.split(" ", 1)
        parent, subject = rest.split(" ", 1)
        if m := AGENT.match(subject):
            agents[int(m.group(1))] = Checkpoint(int(m.group(1)), m.group(2), sha, parent.split()[0])
        elif m := RESET.match(subject):
            resets[int(m.group(1))] = (m.group(2), parent.split()[0])
    for cp, (rule, parent) in resets.items():
        if cp not in agents:
            agents[cp] = Checkpoint(cp, rule, parent, parent, noop=True)
    return [agents[k] for k in sorted(agents)]


def changed_java(repo: Path, a: str, b: str, java_src: str = JAVA_SRC
                 ) -> list[tuple[str | None, str | None]]:
    """(before path, after path) for every production .java file the diff a..b touches."""
    pairs = []
    for line in git(repo, "diff", "--name-status", "-M", a, b, "--", java_src).splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R"):
            old, new = parts[1], parts[2]
        elif status == "A":
            old, new = None, parts[1]
        elif status == "D":
            old, new = parts[1], None
        else:
            old = new = parts[1]
        if (old or new).endswith(".java"):
            pairs.append((old, new))
    return pairs


def materialise(repo: Path, rev: str, path: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{path}"], check=True,
                          capture_output=True).stdout
    dest.write_bytes(data)
    return dest


def extract(repo: Path, rev: str, java_src: str, dest: Path) -> Path:
    """The production Java tree at rev, under dest. Empty where rev has none (a stack's empty base)."""
    dest.mkdir(parents=True, exist_ok=True)
    if git(repo, "ls-tree", "-r", "--name-only", rev, "--", java_src).strip():
        archive = subprocess.run(["git", "-C", str(repo), "archive", rev, java_src],
                                 check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)
    return dest


def wired_types(repo: Path, rev: str, root: str = WIRING) -> set[str]:
    """The simple names of the classes the OfficeFloor wiring at rev declares (``class:`` entries):
    their public methods are functions whose parameters the framework injects."""
    out = set()
    for f in git(repo, "ls-tree", "-r", "--name-only", rev, "--", root).splitlines():
        if f.endswith((".yml", ".yaml")):
            for line in git(repo, "show", f"{rev}:{f}").splitlines():
                m = re.match(r"\s*class:\s*([\w.$]+)", line.split("#", 1)[0])
                if m:
                    out.add(m.group(1).split(".")[-1])
    return out


def wiring(repo: Path, rev: str, root: str = WIRING) -> dict:
    """The OfficeFloor wiring at rev (``parse_wiring``). Zero for an arm without wiring files."""
    files = [f for f in git(repo, "ls-tree", "-r", "--name-only", rev, "--", root).splitlines()
             if f.endswith((".yml", ".yaml"))]
    return parse_wiring({f: git(repo, "show", f"{rev}:{f}") for f in files})


def parse_wiring(texts: dict[str, str]) -> dict:
    """Nodes, edges and lines of wiring files (path -> text). A node is a ``class:`` entry; an edge
    is a ``next:`` or an entry of an ``outputs:`` map; a line is a line that is neither blank nor only
    a comment. ``largest_lines`` is the line count of the file with the most (PLAN.md §4.5)."""
    nodes = edges = lines = 0
    largest, largest_lines = None, 0
    for f in sorted(texts):
        in_outputs = None
        own = 0
        for raw in texts[f].splitlines():
            line = raw.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            own += 1
            indent = len(line) - len(line.lstrip())
            key = line.strip()
            if in_outputs is not None and indent <= in_outputs:
                in_outputs = None
            if key.startswith("class:"):
                nodes += 1
            elif key.startswith("next:"):
                edges += 1
            elif key.startswith("outputs:"):
                in_outputs = indent
            elif in_outputs is not None and ":" in key:
                edges += 1
        lines += own
        if own > largest_lines:
            largest, largest_lines = f, own
    return {"files": len(texts), "nodes": nodes, "edges": edges, "lines": lines,
            "largest_file": largest, "largest_lines": largest_lines}


def measure(repo: Path, branch: str, base_ref: str, work: Path, java_src: str = JAVA_SRC,
            wiring_root: str = WIRING) -> dict:
    """Run the instrument over every checkpoint of the chain; returns the parsed records.
    ``java_src`` and ``wiring_root`` are the stack's production Java and OfficeFloor wiring roots
    (the petclinic layout by default; a ui stack declares its own in ``stack.yaml``)."""
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    cps = checkpoints(repo, branch, base_ref)
    manifest, amounts, wires, shapes = [], [], {}, []
    for c in cps:
        unit = f"cp{c.cp:02d}"
        for old, new in changed_java(repo, c.parent, c.commit, java_src):
            path = new or old
            before = (str(materialise(repo, c.parent, old, work / unit / "before" / old))
                      if old else "-")
            after = (str(materialise(repo, c.commit, new, work / unit / "after" / new))
                     if new else "-")
            manifest.append(f"{unit}\t{path}\t{before}\t{after}\t{old or '-'}")
        tree = extract(repo, c.commit, java_src, work / unit / "tree")
        amounts.append(f"{unit}\t{tree}")
        # the tree at k - 1 (the agent commit's parent), for the hosts' shape before the addition
        prior = extract(repo, c.parent, java_src, work / unit / "prior")
        shapes.append(f"{unit}\t{prior}\t{','.join(sorted(wired_types(repo, c.parent, wiring_root))) or '-'}")
        wires[unit] = {"before": wiring(repo, c.parent, wiring_root),
                       "after": wiring(repo, c.commit, wiring_root)}
    (work / "manifest.tsv").write_text("\n".join(manifest) + "\n")
    # RefactoringMiner at each agent commit, and the injected (wired) types, as hints
    real = [(f"cp{c.cp:02d}", c.commit) for c in cps if not c.noop]
    found = refactor.run(repo, real, work / "refactorings.jsonl")
    hint_lines = []
    for f in found:
        hint_lines += refactor.hints(f)
    for c in cps:
        for t in sorted(wired_types(repo, c.commit, wiring_root)):
            hint_lines.append(f"cp{c.cp:02d}\tinjected\t{t}")
    (work / "hints.tsv").write_text("\n".join(hint_lines) + "\n")
    # a guard: every path a hint names must be a path of the manifest (or the hint can never apply)
    paths = {p for line in manifest for p in (line.split("\t")[1], line.split("\t")[4])}
    unmatched = 0
    for h in hint_lines:
        f = h.split("\t")
        if f[1] in ("method", "type"):
            named = [f[2], f[4]]
        elif f[1] == "moved":
            named = [f[2]]
        elif f[1] == "rename" and f[2] != "member":
            named = [f[3]]
        else:
            named = []
        unmatched += any(p not in paths for p in named)
    # the chain's base (where it leaves base_ref): the amount added is read from it (PLAN.md 4.6)
    base = git(repo, "merge-base", branch, base_ref).strip()
    amounts.append(f"base\t{extract(repo, base, java_src, work / 'base' / 'tree')}")
    (work / "amount.tsv").write_text("\n".join(amounts) + "\n")
    subprocess.run(["java", "-cp", CLASSPATH, "Pull", str(work / "manifest.tsv"),
                    str(work / "hints.tsv"), str(work / "pull.jsonl")], check=True)
    subprocess.run(["java", "-cp", CLASSPATH, "Pull", "--amount", str(work / "amount.tsv"),
                    str(work / "amount.jsonl")], check=True)
    (work / "shape.tsv").write_text("\n".join(shapes) + "\n")
    shaped = shape.run(work / "shape.tsv", work / "shape.jsonl")
    trees = {line.split("\t")[0]: Path(line.split("\t")[1]) for line in shapes}
    methods = shape.complete(shaped, trees)
    records = [json.loads(l) for l in (work / "pull.jsonl").read_text().splitlines() if l]
    amount = {r["unit"]: r for r in
              (json.loads(l) for l in (work / "amount.jsonl").read_text().splitlines() if l)}
    return {"checkpoints": [c.__dict__ for c in cps], "records": records, "amount": amount,
            "wiring": wires, "refactorings": found, "hints": len(hint_lines),
            "shape": methods, "shape_problems": [r for r in shaped if r["kind"] == "problem"],
            "hints_unmatched": unmatched}

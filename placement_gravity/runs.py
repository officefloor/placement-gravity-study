"""Step 03: the runs this study reads (runs.yaml), fetched and pinned.

    python -m placement_gravity.runs stacks            # each ui stack's declared roots (no run read)
    python -m placement_gravity.runs fetch [--analysis NAME ...]

``fetch`` reads only the chains runs.yaml names. Where an analysis lists its ``chains`` it reads
all of them or none, each having reached ``complete_at`` where that is given, and it never
replaces a head it has recorded with another commit. It refuses every analysis but the development
one until the registration tag (plan-v1) is an ancestor of HEAD, so no run's backend Java is read
before registration. It records each chain's head in results/heads.tsv; step 04 measures exactly
those commits.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import tempfile
from pathlib import Path

import yaml

from . import chain, tables

ROOT = chain.ROOT
REGISTRY = ROOT / "runs.yaml"
RESULTS = ROOT / "results"
HEADS = RESULTS / "heads.tsv"
STACKS = RESULTS / "stacks.json"
HEAD_FIELDS = ["analysis", "role", "corpus", "arm", "frontend", "run", "strategy", "chain", "repo",
               "branch", "sha", "excluded"]


def load(path: Path = REGISTRY) -> dict:
    reg = yaml.safe_load(path.read_text())
    for r in reg["repos"].values():
        r["path"] = Path(r["path"]).expanduser()
    for s in reg["streams"].values():
        s["repo"] = Path(s["repo"]).expanduser()
    validate(reg)
    return reg


#: The stages the steps read the analyses in (PLAN.md 9 row 125): ``first`` is what exists when the
#: plan is registered (the petclinic runs, the histories, the development data; steps 03 to 08);
#: then one stage for each run still being made, read by its own step when its chains are complete.
STAGES = {"first": "steps 03 to 08", "run-b": "step09_run_b.sh", "run-c": "step10_run_c.sh",
          "run-d": "step11_run_d.sh"}


def stage(analysis: dict) -> str:
    return analysis.get("stage", "first")


def validate(reg: dict) -> None:
    names = [a["name"] for a in reg["analyses"]]
    if len(names) != len(set(names)):
        raise ValueError("runs.yaml: an analysis name is used twice")
    for a in reg["analyses"]:
        if stage(a) not in STAGES:
            raise ValueError(f"{a['name']}: unknown stage {a['stage']!r}")
        if a["role"] not in ("primary", "secondary", "development"):
            raise ValueError(f"{a['name']}: unknown role {a['role']!r}")
        if a.get("history"):      # corpora B and C: samples of repositories, not paired chains
            for s in a["sources"]:
                if s["sample"] not in reg.get("samples", {}):
                    raise ValueError(f"{a['name']}: unknown sample {s['sample']!r}")
                spec = reg["samples"][s["sample"]]
                if spec.get("max_units") and spec["role"] != "development":
                    raise ValueError(f"{s['sample']}: only a development sample may cap its units")
            continue
        if a["stream"] not in reg["streams"]:
            raise ValueError(f"{a['name']}: unknown stream {a['stream']!r}")
        if a.get("complete_at") and not a.get("chains"):
            raise ValueError(f"{a['name']}: complete_at needs the chains to be named")
        arms = {s["arm"] for s in a["sources"]}
        if len(arms) < 2:
            raise ValueError(f"{a['name']}: an analysis compares at least two arms")
        for s in a["sources"]:
            if s["repo"] not in reg["repos"]:
                raise ValueError(f"{a['name']}: unknown repo {s['repo']!r}")


def registered(tag: str, root: Path = ROOT) -> bool:
    """Whether the registration tag exists and HEAD descends from it."""
    if not chain.git(root, "tag", "-l", tag).strip():
        return False
    return subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", tag, "HEAD"],
                          capture_output=True).returncode == 0


#: What the registration freezes: the plan, the runs read, the instrument and the analysis code.
REGISTERED = ["PLAN.md", "runs.yaml", "requirements.txt", "setup.sh", "instrument", "refactor",
              "placement_gravity", "analysis"]


def drift(tag: str, root: Path = ROOT) -> dict:
    """The registered files that differ from the registration tag (``changed``, committed or not)
    and those with uncommitted changes (``uncommitted``). Changes after the tag are amendments
    (PLAN.md §9); every report lists them."""
    changed = chain.git(root, "diff", "--name-only", tag, "--", *REGISTERED).split()
    dirty = [line[3:] for line in
             chain.git(root, "status", "--porcelain", "--", *REGISTERED).splitlines()]
    return {"tag": tag, "changed": sorted(changed), "uncommitted": sorted(dirty)}


def guard(reg: dict, analysis: dict, root: Path = ROOT) -> None:
    """Refuse to read a run before registration, or while a registered file has uncommitted
    changes, except the development chain."""
    if analysis["role"] == "development":
        return
    tag = reg["registration_tag"]
    if not registered(tag, root):
        raise SystemExit(f"{analysis['name']}: not registered. No run is read before the tag "
                         f"{tag} (PLAN.md §8); only the development analysis is.")
    dirty = drift(tag, root)["uncommitted"]
    if dirty:
        raise SystemExit(f"{analysis['name']}: uncommitted changes to registered files ("
                         + ", ".join(dirty) + "). Commit them as a dated amendment (PLAN.md §9).")


def streamed(reg: dict, analysis: dict) -> dict[int, dict]:
    """The analysis's stream; none for a history (corpora B and C), which declares nothing."""
    return {} if analysis.get("history") else stream(reg, analysis["stream"])


def measured(analysis: dict) -> bool:
    """Whether step 04 (or, for a history, ``history measure``) has left tables to read."""
    if analysis.get("history"):
        return any((RESULTS / "measure" / "_history" / s["sample"]).exists() for s in analysis["sources"])
    return (RESULTS / "measure" / analysis["name"]).exists()


def stream(reg: dict, name: str) -> dict[int, dict]:
    """The pinned stream: tables.stream on the files at the stream's ref, with the act of each
    checkpoint (None where the stream has no acts)."""
    s = reg["streams"][name]
    if s.get("remote"):
        ensure_at(s["repo"], s["remote"], s["ref"])
    with tempfile.TemporaryDirectory() as d:
        cps = Path(d) / "checkpoints.yaml"
        cps.write_text(chain.git(s["repo"], "show", f"{s['ref']}:{s['checkpoints']}"))
        dens = None
        if s.get("density"):
            dens = Path(d) / "DENSITY.md"
            dens.write_text(chain.git(s["repo"], "show", f"{s['ref']}:{s['density']}"))
        out = tables.stream(cps, dens)
    for cp, x in out.items():
        x["act"] = (cp - 1) // s["act_size"] + 1 if s.get("act_size") else None
    return out


# ---- stacks: the declared roots, read at the empty base ----

def ensure_at(path: Path, remote: str, ref: str) -> None:
    """A clone of ``remote`` at ``path`` that holds ``ref`` (a commit or a tag): cloned where it is
    missing, fetched where it lacks the ref, so that a pinned input is read by the scripts and not
    from a copy someone made by hand. Nothing is checked out; files are read at the ref."""
    path = Path(path).expanduser()
    if not (path / ".git").exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", "--no-checkout", remote, str(path)], check=True)
    have = subprocess.run(["git", "-C", str(path), "cat-file", "-e", f"{ref}^{{commit}}"],
                          capture_output=True).returncode == 0
    if not have:
        subprocess.run(["git", "-C", str(path), "fetch", "--quiet", "--tags", "origin"], check=True)
        if subprocess.run(["git", "-C", str(path), "cat-file", "-e", f"{ref}^{{commit}}"],
                          capture_output=True).returncode != 0:
            subprocess.run(["git", "-C", str(path), "fetch", "--quiet", "origin", ref], check=True)


def ensure_clone(repo: dict) -> None:
    """A clone of the stack repo holding only its base_ref until chains are fetched."""
    if (repo["path"] / ".git").exists():
        return
    repo["path"].parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--quiet", "--no-checkout", "--single-branch", "--branch",
                    repo["base_ref"], repo["remote"], str(repo["path"])], check=True)


def roots(repo: dict) -> dict:
    """The production Java root and OfficeFloor wiring root of a repo. A ``layout: stack`` repo
    declares its backend root in stack.yaml at base_ref; its wiring root is the stack's declared
    OfficeFloor config directory when given, else the petclinic layout's."""
    if repo.get("layout") != "stack":
        return {"java_src": chain.JAVA_SRC, "wiring_root": chain.WIRING, "source": "petclinic layout"}
    ensure_clone(repo)
    chain.git(repo["path"], "fetch", "--quiet", "origin", repo["base_ref"])
    text = chain.git(repo["path"], "show", f"FETCH_HEAD:stack.yaml")
    return roots_from_stack(yaml.safe_load(text) or {})


def roots_from_stack(doc: dict) -> dict:
    backend = ((doc.get("layers") or {}).get("backend") or {})
    root = str(backend.get("root") or "").strip().strip("/")
    if not root:
        raise ValueError("stack.yaml declares no backend root")
    wiring = chain.WIRING
    for g in backend.get("config_globs") or []:
        m = re.match(r"([^*{]*officefloor)/", str(g))
        if m:
            wiring = m.group(1).strip("/") + "/"
            break
    return {"java_src": root + "/", "wiring_root": wiring, "source": "stack.yaml"}


# ---- fetch: the named chains, pinned ----

def branch_of(repo: dict, source: dict, n: int | str) -> str:
    return repo["branch"].format(run=source["run"], strategy=source["strategy"], arm=source["arm"],
                                 chain=n)


def remote_chains(repo: dict, source: dict) -> dict[int, tuple[str, str]]:
    """chain number -> (branch, sha) for every chain of the source on the remote."""
    pattern = branch_of(repo, source, "*")
    found = {}
    out = subprocess.run(["git", "ls-remote", "--heads", repo["remote"], pattern],
                         check=True, capture_output=True, text=True).stdout
    rx = re.compile("^" + re.escape(branch_of(repo, source, "CHAINNUMBER"))
                    .replace("CHAINNUMBER", r"(\d+)") + "$")
    for line in out.splitlines():
        sha, ref = line.split("\t")
        name = ref.removeprefix("refs/heads/")
        m = rx.match(name)
        if m:
            found[int(m.group(1))] = (name, sha)
    return found


def fetch(reg: dict, analysis: dict) -> list[dict]:
    guard(reg, analysis)
    rows = []
    for s in analysis["sources"]:
        repo = reg["repos"][s["repo"]]
        if repo.get("layout") == "stack":
            ensure_clone(repo)
        found = remote_chains(repo, s)
        wanted = analysis.get("chains")
        if wanted is not None and analysis["role"] != "development":
            # the chains an analysis names are all read or none is (PLAN.md §9 row 114)
            missing = sorted(set(wanted) - set(found))
            if missing:
                raise SystemExit(f"{analysis['name']}: {s['run']} has no chain {missing} on the remote yet. "
                                 "Nothing of the analysis is read until every chain it names is pushed.")
        for n in sorted(found):
            if wanted is not None and n not in wanted:
                continue
            branch, sha = found[n]
            chain.git(repo["path"], "fetch", "--quiet", "origin",
                      f"+refs/heads/{branch}:refs/remotes/origin/{branch}")
            last = analysis.get("complete_at")
            if last:
                done = [c.cp for c in chain.checkpoints(repo["path"], sha, repo["base_ref"])]
                if not done or max(done) < last:
                    raise SystemExit(f"{analysis['name']}: {branch} stops at checkpoint "
                                     f"{max(done) if done else 0}, before {last}. Nothing of the analysis "
                                     "is read until every chain is complete.")
            rows.append({"analysis": analysis["name"], "role": analysis["role"],
                         "corpus": analysis["corpus"], "arm": s["arm"],
                         "frontend": s.get("frontend", ""), "run": s["run"],
                         "strategy": s["strategy"], "chain": n, "repo": s["repo"],
                         "branch": f"origin/{branch}", "sha": sha,
                         "excluded": n in (analysis.get("exclude_chains") or [])})
    return rows


def read_heads(path: Path = HEADS) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    for r in rows:
        r["chain"] = int(r["chain"])
        r["excluded"] = r["excluded"] == "True"
    return rows


def write_heads(rows: list[dict], path: Path = HEADS) -> None:
    """Replace the rows of the analyses given, keep the others. A head once recorded is not
    replaced by another commit, except the development chain's: a run is read once, at the head it
    had (PLAN.md §8, §9 row 114)."""
    names = {r["analysis"] for r in rows}
    was = {(r["analysis"], r["arm"], r["run"], r["chain"]): r["sha"] for r in read_heads(path)}
    for r in rows:
        old = was.get((r["analysis"], r["arm"], r["run"], r["chain"]))
        if old and old != r["sha"] and r["role"] != "development":
            raise SystemExit(f"{r['analysis']}: {r['branch']} was recorded at {old[:9]} and is now at "
                             f"{r['sha'][:9]}. A head once read is not replaced; a dated amendment "
                             "(PLAN.md §9) says why, and removes the row, if it must be.")
    keep = [r for r in read_heads(path) if r["analysis"] not in names]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEAD_FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(sorted(keep + rows, key=lambda r: (r["analysis"], r["arm"], r["run"], r["chain"])))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["stacks", "fetch"])
    ap.add_argument("--analysis", nargs="*")
    a = ap.parse_args()
    reg = load()
    if a.action == "stacks":
        out = {name: {**roots(repo), "base_ref": repo["base_ref"]}
               for name, repo in reg["repos"].items()}
        STACKS.parent.mkdir(parents=True, exist_ok=True)
        STACKS.write_text(json.dumps(out, indent=1) + "\n")
        print(json.dumps(out, indent=1))
        return
    chosen = [x for x in reg["analyses"] if not x.get("history")
              and (not a.analysis or x["name"] in a.analysis)]
    for analysis in chosen:
        rows = fetch(reg, analysis)
        write_heads(rows)
        arms = {}
        for r in rows:
            arms.setdefault(r["arm"], []).append(r["chain"])
        print(f"{analysis['name']}: " + "; ".join(f"{k} chains {v}" for k, v in sorted(arms.items())))


if __name__ == "__main__":
    main()

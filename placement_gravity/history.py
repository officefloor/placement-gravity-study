"""Corpora B and C: an open-source repository's history read as the paired chains are
(PLAN.md §3.2, §3.3).

    python -m placement_gravity.history sample NAME      # draw the sample runs.yaml declares
    python -m placement_gravity.history measure [--analysis NAME ...]

**The unit** is a commit reachable from the sampled repository's pinned commit that is not a
merge and changes at most ``MAX_LINES`` lines of production Java (a .java file outside a test
directory). Its parent is the tree before. Every such commit is read, not only those on the
first-parent line: where work is merged by pull request, the first-parent line is mostly merges,
and the commits that hold the code are behind them. They are ordered by committer date, and
there is no cap on their number.

**What is read** is what the instrument reads on a chain, without the things a history does not
have: no stream (every later arrival counts, none is declared), no wiring, no amount. The tree
before a unit is the before versions of the files it changes, so an existing host has its shape
(S1, S4, the class's Gini), and the candidates of the landing reading are those files' methods and
classes only: the destinations are read, the ranks are not. The literature's measures that need
the whole tree are not computed.

**Per unit** (``units.csv``): its commit, committer date, the agents it declares (the sampler's
signatures, ``open_source_repository_sampler.agents``) and the issues its message names. An
analysis assigns units to arms by those (``runs.yaml``: ``commits: all | agent | other``, with
``before`` and ``after`` dates), in ``prepare``.

A repository is measured once, under ``results/measure/_history/<sample>/``, whatever analyses
read it.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from . import chain, lines, places, refactor, runs, tables

OUT = runs.RESULTS / "measure" / "_history"
WORK = chain.ROOT / ".tmp" / "history"
SAMPLES = chain.ROOT / "samples"
HISTORY_VERSION = 12
#: A unit changes at most this many lines of production Java (PLAN.md §3.2).
MAX_LINES = 200
#: No cap on the units read per repository (decided by the author, 18 November 2026): a
#: repository's size is the sample's to bound, by its criteria. A number here reads only the newest.
MAX_UNITS = None
_ISSUE = re.compile(r"(?<![\w/])#(\d+)\b")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True, errors="replace").stdout


#: The sampler at its pinned release, in an environment of its own (setup.sh): this study's
#: environment holds an older one that the complexity-concentration study's extractor requires.
SAMPLER = Path(os.environ.get("PG_SAMPLER", chain.ROOT / "lib" / "sampler" / "bin"))
_DECLARE = ("import json, sys\nfrom open_source_repository_sampler import agents\n"
            "print(json.dumps([agents.declared(*c) for c in json.load(sys.stdin)]))")


def declared_agents(commits: list[tuple[str, str, str]]) -> list[list[str]]:
    """The agents each (author, committer, message) declares, by the sampler's own signatures
    (``open_source_repository_sampler.agents``) at its pinned release."""
    if not commits:
        return []
    out = subprocess.run([str(SAMPLER / "python"), "-c", _DECLARE], input=json.dumps(commits),
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def units(repo: Path, head: str = "HEAD", max_units: int | None = MAX_UNITS,
          max_lines: int = MAX_LINES, before: str | None = None) -> list[dict]:
    """The units of a repository, oldest first, numbered from 1: {cp, commit, parent, date,
    agents, issues, lines}. With ``before`` (an ISO date), only commits committed before that day:
    the newest ``max_units`` of those."""
    sep, end = "\x1f", "\x1e"
    log = git(repo, "log", "--no-merges", "--date-order", f"--format={end}%H{sep}%P{sep}%cI{sep}%aN <%aE>{sep}"
              f"%cN <%cE>{sep}%B{sep}", "--numstat", head)
    found, said = [], []
    for record in log.split(end)[1:]:
        sha, parents, date, author, committer, message, stat = record.split(sep, 6)
        if len(parents.split()) != 1:
            continue                                  # a merge, or the root commit
        if before and not date[:10] < str(before):
            continue
        changed = 0
        for line in stat.splitlines():
            parts = line.split("\t")
            if len(parts) == 3 and parts[0].isdigit() and refactor.production(parts[2].split(" => ")[-1].rstrip("}")):
                changed += int(parts[0]) + int(parts[1])
        if not 0 < changed <= max_lines:
            continue
        said.append((author, committer, message))
        found.append({"commit": sha, "parent": parents.split()[0], "date": date,
                      "issues": sorted({int(n) for n in _ISSUE.findall(message)}),
                      "lines": changed})
        if max_units and len(found) == max_units:
            break
    for u, agents in zip(found, declared_agents(said)):
        u["agents"] = agents
    found.reverse()
    return [{"cp": i, **u} for i, u in enumerate(found, start=1)]


def measure_repo(repo: Path, out: Path, name: str, head: str = "HEAD",
                 max_units: int | None = MAX_UNITS, before: str | None = None) -> Path:
    """The tables of one repository (hosts, runs, classes, additions, outcomes, landings, units)."""
    us = units(repo, head, max_units, before=before)
    work = WORK / out.name
    cps = [chain.Checkpoint(u["cp"], u["commit"][:12], u["commit"], u["parent"]) for u in us]
    measured = chain.measure(repo, head, head, work, java_src=".", cps=cps, keep=refactor.production)
    h = tables.host_rows("history", name, measured)

    def write(table: str, rows: list[dict]) -> None:
        path = out / f"{table}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as f:
            if rows:
                rows = rows if "repo" in rows[0] else [{"repo": name, **r} for r in rows]
                w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
                w.writeheader()
                w.writerows(rows)

    write("hosts", h)
    write("runs", tables.run_rows("history", name, measured))
    write("classes", tables.class_rows("history", name, h, measured))
    write("additions", tables.addition_rows("history", name, measured, h, {}))
    write("outcomes", tables.outcome_rows("history", name, h, {}, None, lines.follow(measured["records"])))
    write("landings", places.landings("history", name, h, measured["shape"]))
    write("pairs", tables.pair_rows("history", name, h, measured))
    write("coupling", tables.coupling_rows("history", name, measured))
    write("encapsulation", tables.encapsulation_rows("history", name, h, measured))
    write("refactorings", tables.refactoring_rows("history", name, measured))
    write("boundary", tables.boundary_rows("history", name, h, measured))
    write("edges", tables.edge_rows("history", name, h, measured))
    write("members", tables.member_rows("history", name, measured))
    write("units", [{"repo": name, "cp": u["cp"], "commit": u["commit"], "date": u["date"],
                     "agent": bool(u["agents"]), "agents": " ".join(u["agents"]),
                     "issues": " ".join(map(str, u["issues"])), "lines": u["lines"]} for u in us])
    (out / "meta.json").write_text(json.dumps({"history_version": HISTORY_VERSION, "units": len(us),
                                               "head": git(repo, "rev-parse", head).strip()}, indent=1) + "\n")
    shutil.rmtree(work, ignore_errors=True)
    return out


# ---------------------------------------------------------------- arms (prepare)

def in_arm(unit: dict, source: dict) -> bool:
    """Whether a unit belongs to a source's arm: ``commits`` (all, agent: it declares an agent,
    other: it declares none), and committer dates ``before`` and ``after`` (ISO dates; before is
    exclusive, after inclusive)."""
    agent = str(unit["agent"]) == "True"
    want = source.get("commits", "all")
    if (want == "agent" and not agent) or (want == "other" and agent):
        return False
    day = unit["date"][:10]
    if source.get("before") and not day < str(source["before"]):
        return False
    if source.get("after") and not day >= str(source["after"]):
        return False
    return True


def gather(analysis: dict, table: str, root: Path | None = None) -> list[dict]:
    """A table of a history analysis: every measured repository of each source's sample, its rows
    kept where their unit is in the source's arm, labelled as the chains' rows are (the repository
    is the chain). ``cp`` stays the unit's number; ``position`` is its place from 0 to 1."""
    rows = []
    for source in analysis["sources"]:
        base = (root or OUT) / source["sample"]
        for d in sorted(p for p in base.iterdir() if p.is_dir()) if base.exists() else []:
            us = {u["cp"]: u for u in _read(d / "units.csv")}
            n = max(len(us), 1)
            for r in _read(d / f"{table}.csv"):
                u = us.get(str(r["cp"]))
                if u is None or not in_arm(u, source):
                    continue
                rows.append({**r, "analysis": analysis["name"], "frontend": "", "run": d.name,
                             "strategy": source.get("commits", "all"), "arm": source["arm"],
                             "chain_id": f"{source['arm']}/{d.name}",
                             "position": round((int(r["cp"]) - 1) / max(n - 1, 1), 6),
                             "agent": u["agent"]})
    return rows


def _read(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- samples and the loop

def sample_command(name: str, spec: dict) -> list[str]:
    """The sampler's command for a sample runs.yaml declares."""
    cmd = [str(SAMPLER / "open-source-repository-sampler"), "sample", "--langs", "java",
           "--tiers", ",".join(spec.get("tiers", ["high", "mid", "low"])),
           "--target", str(spec["target"]), "--seed", str(spec["seed"]),
           "--out-dir", str(SAMPLES / name)]
    for key in ("as_of", "min_functions", "min_files_with_functions", "min_commits",
                "min_agent_commits", "max_clones"):
        if spec.get(key) is not None:
            cmd += [f"--{key.replace('_', '-')}", str(spec[key])]
    if spec.get("exclude_owners"):
        cmd += ["--exclude-owners", ",".join(spec["exclude_owners"])]
    return cmd


def sample_path(name: str, spec: dict) -> Path:
    """Where a sample's CSV is: one drawn here (``samples/<name>/``), or one another study drew
    (``csv``), read where it lies."""
    return Path(spec["csv"]).expanduser() if spec.get("csv") else SAMPLES / name


#: Repositories read at once. Each worker's Java processes are held to a share of the machine's
#: memory; a repository that fails in the parallel pass, for want of memory or anything else, is
#: read again alone with the memory undivided.
WORKERS = 8
MEMORY_SHARE = 0.7


def machine_memory_mb() -> int:
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") // (1024 * 1024)
    except (ValueError, OSError):
        return 8192


def heap_mb(workers: int, total_mb: int | None = None) -> int:
    """The Java heap each of ``workers`` gets: an equal part of MEMORY_SHARE of the machine, and
    at least 512 MB."""
    total = total_mb if total_mb is not None else machine_memory_mb()
    return max(512, int(total * MEMORY_SHARE / max(workers, 1)))


def chosen(name: str, spec: dict, excluded: set[str] = frozenset()) -> list[dict]:
    """The usable Java repositories of a sample that are read: not excluded and, where the sample
    sets ``per_tier``, the first that many of each tier in the order of the draw (PLAN.md 3.2:
    corpus B's first set is the first 100 a tier of long-method-slim-study's sample)."""
    path = sample_path(name, spec)
    path = path / "open-source-repository-sample.csv" if path.is_dir() else path
    rows = [r for r in _read(path) if r.get("status") == "usable" and r.get("language") == "java"
            and r["full_name"] not in excluded]
    if spec.get("per_tier"):
        rows.sort(key=lambda r: int(r.get("draw") or 0))
        seen: dict[str, int] = {}
        kept = []
        for r in rows:
            seen[r.get("tier", "")] = seen.get(r.get("tier", ""), 0) + 1
            if seen[r.get("tier", "")] <= spec["per_tier"]:
                kept.append(r)
        rows = kept
    return rows


def sample_excluded(reg: dict, name: str, excluded: set[str] = frozenset()) -> set[str]:
    """The repositories a sample leaves out because another sample reads them
    (``exclude_samples``: corpus B's confirming set leaves out its first set)."""
    out = set()
    for other in reg["samples"][name].get("exclude_samples", []):
        out |= {r["full_name"] for r in chosen(other, reg["samples"][other], excluded)}
    return out


def current(out: Path) -> bool:
    """Whether a repository's tables are whole and made by this ``HISTORY_VERSION``."""
    meta = out / "meta.json"
    try:
        return json.loads(meta.read_text()).get("history_version") == HISTORY_VERSION
    except (OSError, ValueError):
        return False


def pending(name: str, spec: dict, force: bool = False, excluded: set[str] = frozenset()) -> list[dict]:
    """The repositories of a sample still to read: those ``chosen``, and (unless ``force``)
    without tables of this version yet."""
    rows = chosen(name, spec, excluded)
    return [r for r in rows
            if force or not current(OUT / name / r["full_name"].replace("/", "__"))]


def shards(rows: list[dict], workers: int) -> list[list[dict]]:
    """The repositories dealt out to the workers, the largest first and in turn, so that no worker
    holds all the large ones."""
    ordered = sorted(rows, key=lambda r: (-int(r.get("nloc") or 0), r["full_name"]))
    parts = [ordered[i::workers] for i in range(workers)]
    return [p for p in parts if p]


def _write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def _run(name: str, rows_csv: Path, tag: str, heap: int | None, force: bool) -> subprocess.Popen:
    """The sampler's `run` over one list of repositories: it clones each whole at its pinned
    commit, this module measures it (``history repo``), and the sampler deletes the clone. The
    clone is whole: the sampler's ``--only`` holds file contents at the pinned commit alone, and a
    history needs every commit's."""
    cmd = [str(SAMPLER / "open-source-repository-sampler"), "run", str(rows_csv),
           "--deep", "--langs", "java", "--work-dir", str(WORK / "clones" / tag),
           "--run-log", str(OUT / name / "logs" / f"{tag}.jsonl"), "--",
           sys.executable, "-m", "placement_gravity.history", "repo", "--path", "{path}",
           "--name", "{full_name}", "--sample", name] + (["--force"] if force else [])
    env = dict(os.environ)
    if heap:      # every Java process the worker starts (the instrument, RefactoringMiner)
        env["JAVA_TOOL_OPTIONS"] = (env.get("JAVA_TOOL_OPTIONS", "") + f" -Xmx{heap}m").strip()
    (OUT / name / "logs").mkdir(parents=True, exist_ok=True)
    out = (OUT / name / "logs" / f"{tag}.out").open("w")
    return subprocess.Popen(cmd, cwd=chain.ROOT, env=env, stdout=out, stderr=subprocess.STDOUT)


def measure_sample(name: str, spec: dict, force: bool = False, excluded: set[str] = frozenset(),
                   workers: int = WORKERS) -> dict:
    """Every usable repository of a sample, read ``workers`` at a time, each worker's Java held to
    its share of the memory (``heap_mb``). Whatever fails in that pass (a repository too large
    for its share, or anything else) is then read again one at a time, with the memory undivided.
    What still fails is listed in ``failed.txt`` and reported. ``excluded`` repositories (those of
    a development sample) are not read. Returns the counts."""
    (OUT / name).mkdir(parents=True, exist_ok=True)
    (OUT / name / "excluded.txt").write_text("\n".join(sorted(excluded)) + "\n")
    todo = pending(name, spec, force, excluded)
    counts = {"to_read": len(todo), "workers": 0, "heap_mb": None, "retried_alone": 0, "failed": 0}
    if not todo:
        return counts
    # which repositories are read is decided here, by the tables present; the sampler's own logs
    # of an earlier run would have it skip a repository it once finished
    for old in (OUT / name / "logs").glob("*.jsonl") if (OUT / name / "logs").exists() else []:
        old.unlink()
    parts = shards(todo, max(1, min(workers, len(todo))))
    counts["workers"], counts["heap_mb"] = len(parts), heap_mb(len(parts)) if len(parts) > 1 else None
    procs = []
    for k, part in enumerate(parts):
        rows_csv = OUT / name / "logs" / f"part{k:02d}.csv"
        _write_rows(rows_csv, part)
        procs.append(_run(name, rows_csv, f"part{k:02d}", counts["heap_mb"], force))
    for p in procs:
        p.wait()
    # the sequential pass: what the parallel pass left unread, alone and with all the memory
    left = pending(name, spec, False, excluded)
    if left and len(parts) > 1:
        counts["retried_alone"] = len(left)
        rows_csv = OUT / name / "logs" / "alone.csv"
        _write_rows(rows_csv, left)
        (OUT / name / "logs" / "alone.jsonl").unlink(missing_ok=True)
        _run(name, rows_csv, "alone", None, False).wait()
        left = pending(name, spec, False, excluded)
    counts["failed"] = len(left)
    (OUT / name / "failed.txt").write_text("".join(r["full_name"] + "\n" for r in left))
    (OUT / name / "run.json").write_text(json.dumps(counts, indent=1) + "\n")
    return counts


def development_repositories(reg: dict) -> set[str]:
    """The repositories of every development sample: read to build the steps, so never read for
    an analysis that is not the development one."""
    out = set()
    for name, spec in reg.get("samples", {}).items():
        if spec["role"] == "development":
            for p in sample_path(name, spec).glob("open-source-repository-sample*.csv") \
                    if sample_path(name, spec).is_dir() else [sample_path(name, spec)]:
                out |= {r["full_name"] for r in _read(p) if r.get("status") == "usable"}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample")
    s.add_argument("name")
    m = sub.add_parser("measure")
    m.add_argument("--analysis", nargs="*")
    m.add_argument("--force", action="store_true")
    m.add_argument("--workers", type=int, default=WORKERS,
                   help=f"repositories read at once (default {WORKERS}); 1 reads them one at a time")
    r = sub.add_parser("repo")          # one cloned repository; called by the sampler's `run`
    r.add_argument("--path", required=True)
    r.add_argument("--name", required=True)
    r.add_argument("--sample", required=True)
    r.add_argument("--force", action="store_true")
    a = ap.parse_args()
    reg = runs.load()
    if a.cmd == "repo":
        spec = reg["samples"][a.sample]
        out = OUT / a.sample / a.name.replace("/", "__")
        skip = (OUT / a.sample / "excluded.txt")
        if a.name in (skip.read_text().split() if skip.exists() else []):
            return
        if a.force or not current(out):
            (out / "meta.json").unlink(missing_ok=True)     # tables are whole or absent
            measure_repo(Path(a.path), out, a.name, before=spec.get("before"),
                         max_units=spec.get("max_units") or MAX_UNITS)
        return
    if a.cmd == "sample":
        spec = reg["samples"][a.name]
        runs.guard(reg, {"name": f"sample {a.name}", "role": spec["role"]})
        if spec.get("csv"):
            raise SystemExit(f"{a.name} is another study's drawn sample ({spec['csv']}): it is read, not drawn")
        subprocess.run(sample_command(a.name, spec), check=True)
        return
    done = set()
    for analysis in reg["analyses"]:
        if not analysis.get("history") or (a.analysis and analysis["name"] not in a.analysis):
            continue
        runs.guard(reg, analysis)
        skip = set() if analysis["role"] == "development" else development_repositories(reg)
        for source in analysis["sources"]:
            spec = reg["samples"][source["sample"]]
            if source["sample"] not in done and sample_path(source["sample"], spec).exists():
                counts = measure_sample(source["sample"], spec, a.force,
                                        skip | sample_excluded(reg, source["sample"], skip), a.workers)
                done.add(source["sample"])
                print(f"{analysis['name']}: {source['sample']} {counts}")


if __name__ == "__main__":
    main()

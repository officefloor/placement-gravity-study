"""Corpora B and C: a repository's history read as units (PLAN.md 3.2, 3.3)."""

import json
import os
import subprocess
from pathlib import Path

import pytest

from placement_gravity import history, prepare, runs

pytestmark = pytest.mark.skipif(not (history.SAMPLER / "python").exists(),
                                reason="the sampler's environment is installed by setup.sh")

OWNER = """public class Owner {
    private int limit = 3;
    private String name;
%s
}
"""


def commit(repo, files, message, date, author="Ann <ann@x>"):
    for rel, text in files.items():
        f = repo / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
    name, email = author[:-1].split(" <")
    env = {**os.environ, "GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": email, "GIT_COMMITTER_NAME": name,
           "GIT_COMMITTER_EMAIL": email, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True, env=env)
    subprocess.run(["git", "commit", "--quiet", "-m", message], cwd=repo, check=True, env=env)


@pytest.fixture(scope="module")
def repo(tmp_path_factory):
    r = tmp_path_factory.mktemp("repo")
    subprocess.run(["git", "init", "--quiet", "-b", "main"], cwd=r, check=True)
    body = "    int size(int n) {\n        int k = n + 1;\n        return k;\n    }\n"
    commit(r, {"src/main/java/Owner.java": OWNER % body, "README.md": "x"}, "base", "2020-01-01T00:00:00Z")
    # 1: a person's commit, bound to the method's local and the class's field
    body2 = body.replace("return k;", "if (k > limit) {\n            k = limit;\n        }\n        return k;")
    commit(r, {"src/main/java/Owner.java": OWNER % body2}, "Cap the size (#12)", "2020-06-01T00:00:00Z")
    # not a unit: only a test changes; and only documentation
    commit(r, {"src/test/java/OwnerTest.java": "class OwnerTest { void t() { } }"}, "test", "2020-07-01T00:00:00Z")
    commit(r, {"README.md": "y"}, "docs", "2020-08-01T00:00:00Z")
    # 2: an agent's commit after the date: unbound code in a new class
    commit(r, {"src/main/java/Rule.java": "public class Rule {\n    boolean ok(int n) {\n        return n > 0;\n    }\n}\n"},
           "Add a rule\n\nCo-Authored-By: Claude <noreply@anthropic.com>", "2022-03-01T00:00:00Z")
    # 3: a person's commit after the date, bound in the existing class again
    body3 = body2.replace("return k;", "if (name == null) {\n            return 0;\n        }\n        return k;")
    commit(r, {"src/main/java/Owner.java": OWNER % body3}, "Guard the name", "2023-01-01T00:00:00Z")
    return r


def test_units_are_small_commits_to_production_java(repo):
    us = history.units(repo)
    assert [u["cp"] for u in us] == [1, 2, 3]            # the base, the test and the docs are not units
    assert (us[0]["issues"], us[0]["agents"]) == ([12], [])
    assert us[1]["agents"] == ["claude"] and us[2]["agents"] == []
    assert [u["cp"] for u in history.units(repo, before="2021-06-29")] == [1]
    assert len(history.units(repo, max_units=2)) == 2    # the newest two
    assert history.units(repo, max_lines=1) == []


def test_a_unit_is_in_an_arm_by_who_declares_it_and_when():
    agent = {"agent": "True", "date": "2022-03-01T00:00:00Z"}
    person = {"agent": "False", "date": "2020-06-01T00:00:00Z"}
    assert history.in_arm(agent, {"commits": "agent"}) and not history.in_arm(person, {"commits": "agent"})
    assert history.in_arm(person, {"commits": "all", "before": "2021-06-29"})
    assert not history.in_arm(agent, {"commits": "all", "before": "2021-06-29"})
    assert not history.in_arm(person, {"commits": "other", "after": "2021-06-29"})


def test_a_repository_is_measured_and_gathered_into_arms(repo, tmp_path):
    out = history.measure_repo(repo, tmp_path / "m" / "s" / "o__r", "o/r")
    for t in ("hosts", "runs", "additions", "outcomes", "landings", "units"):
        assert (out / f"{t}.csv").exists()
    analysis = {"name": "a", "role": "development", "history": True, "methods_arm": "other",
                "function_arm": "agent",
                "sources": [{"arm": "other", "sample": "s", "commits": "other"},
                            {"arm": "agent", "sample": "s", "commits": "agent"}]}
    runs_ = history.gather(analysis, "runs", tmp_path / "m")
    assert {(r["arm"], r["cp"]) for r in runs_} == {("other", "1"), ("agent", "2"), ("other", "3")}
    first = next(r for r in runs_ if r["cp"] == "1")
    assert first["chain_id"] == "other/o__r" and float(first["position"]) == 0.0
    assert int(first["binding"]) >= 1                       # it used the local and the field
    landed = history.gather(analysis, "landings", tmp_path / "m")
    new = next(r for r in landed if r["arm"] == "agent")
    assert new["destination"] == "new class" and new["bound"] == "False"
    # cp1's code in size(int) is come back to by cp3, bound there too; nothing is declared
    outs = history.gather(analysis, "outcomes", tmp_path / "m")
    assert next(r for r in outs if r["cp"] == "1")["intrusion_method"] == "1"
    # and step 4's datasets are built from it, the index the unit's place from 0 to 1
    data = prepare.prepare(analysis, {}, tmp_path / "m", tmp_path / "d")
    import csv, json
    spec = json.loads((data / "spec.json").read_text())
    assert spec["problem_fixed"] is False and (spec["methods_arm"], spec["function_arm"]) == ("other", "agent")
    by = list(csv.DictReader((data / "by.csv").open()))
    assert {r["cp"] for r in by} <= {"0.0", "0.5", "1.0"}
    land = list(csv.DictReader((data / "landing.csv").open()))
    assert [(r["arm"], r["existing_class"]) for r in land] == [("agent", "False")]


def test_the_registry_declares_the_samples_and_their_analyses():
    reg = runs.load()
    assert reg["samples"]["open-source-agent"]["min_agent_commits"] == 30
    assert reg["samples"]["open-source-human"]["as_of"] == "2020-12-01"
    names = {a["name"] for a in reg["analyses"] if a.get("history")}
    assert {"open-source-human", "open-source-agent-within", "open-source-agent-against-human",
            "open-source-development"} <= names
    cmd = history.sample_command("open-source-agent", reg["samples"]["open-source-agent"])
    assert cmd[cmd.index("--min-agent-commits") + 1] == "30" and cmd[cmd.index("--seed") + 1] == "20261119"


def test_repositories_are_dealt_to_workers_largest_first_and_in_turn():
    rows = [{"full_name": f"o/r{i}", "nloc": str(n)} for i, n in enumerate([10, 900, 50, 700, 30, 20, 800])]
    parts = history.shards(rows, 3)
    assert [[r["nloc"] for r in p] for p in parts] == [["900", "50", "10"], ["800", "30"], ["700", "20"]]
    assert history.shards(rows[:2], 8) == [[rows[1]], [rows[0]]]      # no empty worker


def test_each_worker_gets_its_share_of_the_memory():
    assert history.heap_mb(8, 14000) == 1225          # 70% of the machine, in eight parts
    assert history.heap_mb(1, 14000) == 9800
    assert history.heap_mb(64, 4000) == 512           # never below what the instrument starts with


def test_what_is_pending_is_usable_java_not_excluded_and_not_yet_read(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "OUT", tmp_path / "out")
    sample = tmp_path / "s.csv"
    sample.write_text("full_name,status,language,nloc\no/a,usable,java,5\no/b,excluded,java,5\n"
                      "o/c,usable,kotlin,5\no/d,usable,java,9\no/e,usable,java,1\n")
    spec = {"csv": str(sample)}
    assert [r["full_name"] for r in history.pending("s", spec, excluded={"o/e"})] == ["o/a", "o/d"]
    done = tmp_path / "out" / "s" / "o__a"
    done.mkdir(parents=True)
    (done / "meta.json").write_text(f'{{"history_version": {history.HISTORY_VERSION}}}')
    assert [r["full_name"] for r in history.pending("s", spec)] == ["o/d", "o/e"]
    assert len(history.pending("s", spec, force=True)) == 3


def test_only_a_development_sample_may_cap_its_units():
    reg = runs.load()
    assert reg["samples"]["open-source-development-agent"]["max_units"] == 300
    reg["samples"]["open-source-agent"]["max_units"] = 300
    with pytest.raises(ValueError, match="only a development sample"):
        runs.validate(reg)


def test_corpus_b_reads_the_first_of_each_tier_and_the_confirming_set_leaves_them_out(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "OUT", tmp_path / "out")
    first = tmp_path / "first.csv"
    first.write_text("draw,full_name,status,language,tier\n3,o/c,usable,java,high\n1,o/a,usable,java,high\n"
                     "2,o/b,usable,java,mid\n4,o/d,usable,java,high\n5,o/e,excluded,java,mid\n6,o/f,usable,java,mid\n")
    second = tmp_path / "second.csv"
    second.write_text("draw,full_name,status,language,tier\n1,o/a,usable,java,high\n2,o/x,usable,java,high\n"
                      "3,o/y,usable,java,high\n4,o/b,usable,java,mid\n5,o/z,usable,java,mid\n")
    reg = {"samples": {"b1": {"csv": str(first), "per_tier": 2},
                       "b2": {"csv": str(second), "per_tier": 2, "exclude_samples": ["b1"]}}}
    assert [r["full_name"] for r in history.chosen("b1", reg["samples"]["b1"])] == ["o/a", "o/b", "o/c", "o/f"]
    left_out = history.sample_excluded(reg, "b2")
    assert left_out == {"o/a", "o/b", "o/c", "o/f"}
    assert [r["full_name"] for r in history.pending("b2", reg["samples"]["b2"], excluded=left_out)] \
        == ["o/x", "o/y", "o/z"]


def test_corpus_b_is_two_sets_and_corpus_c_one():
    reg = runs.load()
    b1, b2 = reg["samples"]["open-source-human"], reg["samples"]["open-source-human-confirm"]
    assert (b1["seed"], b1["per_tier"]) == (20261101, 100) and b1["csv"].endswith("long-method-slim-study/sample/open-source-repository-sample.csv")
    assert (b2["seed"], b2["per_tier"], b2["exclude_samples"]) == (20261118, 100, ["open-source-human"])
    assert reg["samples"]["open-source-agent"]["seed"] == 20261119 and reg["samples"]["open-source-agent"]["target"] == 100


def test_a_repository_read_by_an_older_version_is_read_again(tmp_path):
    import json
    from placement_gravity import history
    assert not history.current(tmp_path)
    (tmp_path / "meta.json").write_text(json.dumps({"history_version": history.HISTORY_VERSION - 1}))
    assert not history.current(tmp_path)
    (tmp_path / "meta.json").write_text(json.dumps({"history_version": history.HISTORY_VERSION}))
    assert history.current(tmp_path)


def test_tables_of_another_version_are_not_gathered(tmp_path):
    """A repository that failed to be read again keeps its old tables; they are not analysed as new."""
    analysis = {"name": "h", "sources": [{"arm": "human", "sample": "s", "commits": "all"}]}
    for name, version in (("a__new", history.HISTORY_VERSION), ("b__old", history.HISTORY_VERSION - 1)):
        d = tmp_path / "s" / name
        d.mkdir(parents=True)
        (d / "meta.json").write_text(json.dumps({"history_version": version}))
        (d / "units.csv").write_text("cp,agent,date\n1,False,2020-01-01\n")
        (d / "runs.csv").write_text("cp,arm,chain\n1,x,y\n")
    rows = history.gather(analysis, "runs", tmp_path)
    assert len(rows) == 1 and "a__new" in json.dumps(rows[0])

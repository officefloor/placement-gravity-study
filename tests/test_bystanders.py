"""Bystanders (PLAN.md §4.3a) on a fixture with a known answer: the pre-existing values visible
where a run starts, those it uses, and what it leaves behind in the class."""

import json
import subprocess
from pathlib import Path

import pytest

from placement_gravity import chain, prepare, tables

FX = Path(__file__).parent / "fixtures" / "bystanders"


@pytest.fixture(scope="module")
def records(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("by")
    (tmp / "m.tsv").write_text(f"cp01\tOwners.java\t{FX / 'before' / 'Owners.java'}\t{FX / 'after' / 'Owners.java'}\n")
    subprocess.run(["java", "-cp", chain.CLASSPATH, "Pull", str(tmp / "m.tsv"), "-", str(tmp / "o.jsonl")],
                   check=True)
    out = [json.loads(l) for l in (tmp / "o.jsonl").read_text().splitlines()]
    assert all(r["kind"] != "problem" for r in out)
    return out


def test_what_is_visible_where_the_code_lands(records):
    [x] = next(r for r in records if r["kind"] == "host" and r["name"] == "create")["runs"]
    # `repo.check(name);` after the age block: name, age and total are visible; `reason` was declared
    # inside the block and is not; `extra` is declared after the run
    assert x["vis_method"] == ["age", "name", "total"] and x["need_method"] == ["name"]
    # the class before: state `created`; injected `repo` and `clock`; constant LIMIT
    assert x["vis_fields"] == [1, 2, 1] and x["need_fields"] == [0, 1, 0]
    b = tables.bystanders(x)
    assert b["need"] == 2                              # name and repo
    assert b["by_method"] == 2 and b["by_class"] == 3  # age, total; created, clock and the constant LIMIT
    assert b["bystanders"] == 5 and b["bystanders_no_injected"] == 4 and b["bystanders_no_constants"] == 4


def test_a_new_method_sees_its_classes_fields(records):
    [x] = next(r for r in records if r["kind"] == "host" and r["name"] == "helper")["runs"]
    assert x["vis_method"] == []                       # its own parameter is not pre-existing
    b = tables.bystanders(x)
    # it needs the constant, which is not to be duplicated, so it is pulled; the three fields stand by
    assert b["need"] == 1 and b["need_constants"] == 1 and b["by_method"] == 0 and b["by_class"] == 3


def test_a_run_that_needs_nothing_was_not_pulled(records):
    [x] = next(r for r in records if r["kind"] == "host" and r["name"] == "fresh")["runs"]
    assert tables.bystanders(x)["need"] == 0           # prepare.by_rows leaves it out of H3 and H4
    rows = prepare.by_rows([{"chain_id": "c", "arm": "spring", "cp": 1, "host_new": "True",
                             "replacement": "False", **tables.bystanders(x)}])
    assert rows[0]["pulled"] is False


def test_a_plain_accessor_is_organisation_not_logic(records):
    hosts = {r["name"]: r for r in records if r["kind"] == "host"}
    for name in ("getCreated", "setCreated"):          # they only expose the field
        assert hosts[name]["runs"] == [] and hosts[name]["organisation"] == 1
    [x] = hosts["getAudited"]["runs"]                  # more than exposing a field: logic in the class
    assert tables.bystanders(x)["need"] == 1           # `created` was there; `audited` is new


def test_the_field_an_addition_leaves_behind(records):
    c = next(r for r in records if r["kind"] == "class")
    assert c["held_before"] == 4 and c["held_after"] == 5 and c["fields_added"] == 1   # constants held too


def test_what_a_change_introduces(records):
    """Introduced (PLAN.md 4.3b): the values a change adds to a method and the fields it adds to a
    class. They were not there before, so they are neither needed nor standing by for this change."""
    hosts = {r["name"]: r for r in records if r["kind"] == "host"}
    assert hosts["create"]["introduced_method"] == ["checked"]     # an existing method gains a local
    assert hosts["helper"]["introduced_method"] == ["count"]       # all of a new method's values
    [x] = hosts["create"]["runs"]
    assert "checked" not in x["vis_method"]
    c = next(r for r in records if r["kind"] == "class")
    assert c["fields_added_names"] == ["audited"]
    measured = {"records": records}
    rows = {h["name"]: h for h in tables.host_rows("spring", "c", measured)}
    assert rows["create"]["introduced_method_values"] == "checked"
    assert rows["create"]["introduced_class_values"] == "audited"

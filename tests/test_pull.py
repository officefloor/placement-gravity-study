"""The pull instrument on fixtures with known answers (tests/fixtures/<case>/{before,after}), and
RefactoringMiner's findings turned into hints."""

import json
import subprocess
from pathlib import Path

import pytest

from placement_gravity import chain, refactor, tables

FX = Path(__file__).parent / "fixtures"
CASES = ["accrete", "helper", "extract", "writeback", "lambda", "modify", "newclass",
         "injected", "rename", "classmethod", "organisation", "inherited", "constant"]
#: hints as RefactoringMiner and the wiring would give them
HINTS = [
    "injected\tinjected\tCheckX",
    "rename\trename\tvalue\tOwners.java\t3\tcount\ttotal",
]


def measure(tmp, cases, hints):
    lines = []
    for case in cases:
        for f in sorted((FX / case / "after").glob("*.java")):
            before = FX / case / "before" / f.name
            lines.append(f"{case}\t{f.name}\t{before if before.exists() else '-'}\t{f}")
    (tmp / "m.tsv").write_text("\n".join(lines) + "\n")
    (tmp / "h.tsv").write_text("\n".join(hints) + "\n")
    subprocess.run(["java", "-cp", chain.CLASSPATH, "Pull", str(tmp / "m.tsv"), str(tmp / "h.tsv"),
                    str(tmp / "o.jsonl")], check=True)
    out = {}
    for l in (tmp / "o.jsonl").read_text().splitlines():
        r = json.loads(l)
        assert r["kind"] != "problem", r
        out[(r["unit"], r["name"])] = r
    return out


@pytest.fixture(scope="module")
def records(tmp_path_factory):
    return measure(tmp_path_factory.mktemp("pull"), CASES, HINTS)


def run(r, i=0):
    return r["runs"][i]


def test_accretion_ties_to_existing_local_and_field_not_new_ones(records):
    r = records[("accrete", "create")]
    assert not r["host_new"] and r["pre_positions"] == 4 and r["added"] == 5
    x = run(r)
    assert x["tie_method"] == ["digits"]     # n is new
    assert x["tie_field"] == ["repo"]        # audit is a new field, clock is untouched
    assert x["utility"] == ["LOG"]           # a logger is a class utility, not a tie
    assert x["replaces"] == 0


def test_new_helper_is_tied_at_birth_and_to_its_class(records):
    caller, helper = records[("helper", "create")], records[("helper", "check")]
    assert run(caller)["tie_method"] == ["digits"]
    assert run(caller)["tie_class_method"] == []   # check is new, not a pre-existing method
    assert helper["host_new"] and not helper["class_new"]
    assert helper["birth_tie"] == ["create:digits"]
    assert run(helper)["tie_field"] == ["repo"] and run(helper)["tie_method"] == []


def test_extraction_without_hints_falls_back_to_identical_text(records):
    r = records[("extract", "display")]
    assert r["moved_text"] == 2 and r["added"] == 3


def test_write_back_to_an_existing_local_is_a_tie(records):
    assert run(records[("writeback", "create")])["tie_method"] == ["name"]


def test_lambda_parameters_are_not_host_state(records):
    x = run(records[("lambda", "join")])
    assert x["tie_method"] == ["key"] and x["tie_field"] == ["service"]


def test_edited_logic_line_counts_every_reference(records):
    x = run(records[("modify", "code")])
    assert x["replaces"] == 1
    assert x["tie_method"] == ["prefix", "seq"]  # the edited line sources both
    assert x["tok_tie_method"] >= 1              # the edit itself applies .toUpperCase() to prefix


def test_new_class_has_no_ties(records):
    r = records[("newclass", "service")]
    assert r["host_new"] and r["class_new"]
    assert r["birth_tie"] == [] and run(r)["tie_method"] == [] and run(r)["tie_field"] == []


def test_injected_parameters_do_not_tie_but_locals_do(records):
    r = records[("injected", "service")]
    assert r["injected"]
    assert run(r)["tie_method"] == ["a"]       # request and repo are injected


def test_injected_parameters_tie_when_not_wired(tmp_path):
    r = measure(tmp_path, ["injected"], [])[("injected", "service")]
    assert not r["injected"] and run(r)["tie_method"] == ["a", "repo", "request"]
    assert run(r)["tie_param"] == ["repo", "request"]   # a is a local


def test_parameter_ties_are_split_out(records):
    # code(String last, int seq): the edited line uses prefix (a local) and seq (a parameter)
    assert run(records[("modify", "code")])["tie_param"] == ["seq"]
    assert run(records[("accrete", "create")])["tie_param"] == []   # digits is a local


def test_rename_hint_keeps_the_value_pre_existing(records):
    r = records[("rename", "count")]
    assert r["added"] == 1                      # the renamed lines are not edits
    assert run(r)["tie_method"] == ["total"]


def test_rename_without_hint_reads_as_new_value(tmp_path):
    r = measure(tmp_path, ["rename"], [])[("rename", "count")]
    assert r["added"] == 3
    assert run(r)["tie_method"] == ["o"]        # total reads as new; the line still sources o


def test_call_to_existing_class_method_is_a_class_tie(records):
    x = run(records[("classmethod", "create")])
    assert x["tie_class_method"] == ["audit"] and x["tie_method"] == ["o"]


def test_refactoringminer_findings_become_hints():
    found = {"unit": "cp01", "refactorings": [
        {"type": "Rename Variable",
         "description": "Rename Variable count : int to total : int in method void count(o Owner) from class Owners",
         "leftSideLocations": [{"filePath": "src/main/java/a/Owners.java", "startLine": 3, "endLine": 3,
                                "codeElementType": "VARIABLE_DECLARATION_STATEMENT",
                                "description": "original variable declaration"}],
         "rightSideLocations": [{"filePath": "src/main/java/a/Owners.java", "startLine": 3, "endLine": 3,
                                 "codeElementType": "VARIABLE_DECLARATION_STATEMENT",
                                 "description": "renamed variable declaration"}]},
        {"type": "Extract Method", "description": "Extract Method ...",
         "leftSideLocations": [{"filePath": "src/main/java/a/Owners.java", "startLine": 2, "endLine": 9,
                                "codeElementType": "METHOD_DECLARATION",
                                "description": "source method declaration before extraction"}],
         "rightSideLocations": [
             {"filePath": "src/main/java/a/Owners.java", "startLine": 2, "endLine": 5,
              "codeElementType": "METHOD_DECLARATION",
              "description": "source method declaration after extraction"},
             {"filePath": "src/main/java/a/Owners.java", "startLine": 8, "endLine": 10,
              "codeElementType": "BLOCK", "description": "extracted code to extracted method declaration"},
             {"filePath": "src/main/java/a/Owners.java", "startLine": 11, "endLine": 11,
              "codeElementType": "IF_STATEMENT", "description": "added statement in extracted method declaration"}]},
    ]}
    h = refactor.hints(found)
    f = "src/main/java/a/Owners.java"
    assert f"cp01\trename\tvalue\t{f}\t3\tcount\ttotal" in h
    assert f"cp01\tmethod\t{f}\t5\t{f}\t3" in h
    assert f"cp01\tmoved\t{f}\t8\t10" in h
    assert not any("\t11\t11" in x for x in h)  # added code in an extracted method stays an addition


def test_constructor_wiring_is_organisation_not_logic(records):
    r = records[("organisation", "Owners")]
    assert r["organisation"] == 1                # this.audit = audit;
    assert len(r["runs"]) == 1 and run(r)["positions"] == 1   # repo.warm(); is logic
    assert run(r)["tie_method"] == ["repo"]     # the constructor's own parameter


def test_inherited_members_are_reported_unresolved(records):
    x = run(records[("inherited", "display")])
    assert x["unresolved"] == ["getFirstName()", "lastName"]
    assert x["tie_method"] == [] and x["tie_field"] == []


def test_a_constant_is_a_field_tie(records):
    assert run(records[("constant", "code")])["tie_field"] == ["WIDTH"]


def test_gini():
    assert tables.gini([5]) == 0.0
    assert tables.gini([1, 1, 1]) == 0.0
    assert abs(tables.gini([1, 3]) - 0.25) < 1e-9


def test_identity_follows_renames():
    hosts = [{"cp": 1, "type": "A", "name": "f", "before_type": None, "before_name": None},
             {"cp": 2, "type": "A", "name": "g", "before_type": "A", "before_name": "f"},
             {"cp": 3, "type": "B", "name": "g", "before_type": "A", "before_name": "g"}]
    ids = tables.identities(hosts)
    assert ids[(1, "A", "f")] == ids[(2, "A", "g")] == ids[(3, "B", "g")]


def test_codetracker_is_the_identity_of_surviving_methods():
    hosts = [
        {"cp": 1, "type": "A", "name": "f", "before_type": None, "before_name": None, "net_added": 2,
         "removed": 0, "replacement": False, "host_new": True, "pre_positions": 0, "tie_method": 0,
         "tie_class": 0, "tie": 0},
        {"cp": 3, "type": "A", "name": "g", "before_type": None, "before_name": None, "net_added": 1,
         "removed": 0, "replacement": False, "host_new": False, "pre_positions": 2, "tie_method": 1,
         "tie_class": 0, "tie": 1},
        {"cp": 2, "type": "B", "name": "h", "before_type": None, "before_name": None, "net_added": 1,
         "removed": 0, "replacement": False, "host_new": True, "pre_positions": 0, "tie_method": 0,
         "tie_class": 0, "tie": 0},
        {"cp": 4, "type": "B", "name": "h", "before_type": None, "before_name": None, "net_added": 0,
         "removed": 1, "replacement": False, "host_new": False, "pre_positions": 1, "tie_method": 0,
         "tie_class": 0, "tie": 0},
    ]
    # CodeTracker: A.f was renamed to A.g at cp3 (the instrument missed the rename) and changed at cp5
    ct = {"ct_identity": {(1, "A", "f"): "ct:A#g", (3, "A", "g"): "ct:A#g", (5, "A", "g"): "ct:A#g"},
          "ct_touched": {"ct:A#g": {1, 3, 5}}}
    rows = {(r["cp"], r["name"]): r for r in tables.outcome_rows("x", "c", hosts, {}, ct)}
    assert rows[(1, "f")]["identity"] == rows[(3, "g")]["identity"] == "ct:A#g"
    assert rows[(1, "f")]["later_touches"] == 2                 # cp3 and cp5, from CodeTracker
    assert rows[(2, "h")]["identity_source"] == "instrument"    # B.h is removed: own chaining
    assert rows[(2, "h")]["later_touches"] == 1

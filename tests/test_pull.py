"""The pull instrument on fixtures with known answers (tests/fixtures/<case>/{before,after}), and
RefactoringMiner's findings turned into hints."""

import json
import subprocess
from pathlib import Path

import pytest

from placement_gravity import chain, refactor, tables

FX = Path(__file__).parent / "fixtures"
CASES = ["accrete", "helper", "extract", "writeback", "lambda", "modify", "newclass",
         "injected", "rename", "classmethod", "organisation", "inherited", "constant", "injection",
         "handler"]
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
        if r["kind"] == "class":      # per-class accretion records (tests/test_bystanders.py)
            continue
        out[(r["unit"], r["name"])] = r
    return out


@pytest.fixture(scope="module")
def records(tmp_path_factory):
    return measure(tmp_path_factory.mktemp("pull"), CASES, HINTS)


def run(r, i=0):
    return r["runs"][i]


def test_accretion_bindings_to_existing_local_and_field_not_new_ones(records):
    r = records[("accrete", "create")]
    assert not r["host_new"] and r["pre_positions"] == 4 and r["added"] == 5
    x = run(r)
    assert x["binding_method"] == ["digits"]     # n is new
    assert x["binding_field"] == ["repo"]        # audit is a new field, clock is untouched
    assert x["utility"] == ["LOG"]           # a logger is a class utility, not a binding
    assert x["replaces"] == 0


def test_new_helper_is_bound_at_birth_and_to_its_class(records):
    caller, helper = records[("helper", "create")], records[("helper", "check")]
    assert run(caller)["binding_method"] == ["digits"]
    assert run(caller)["binding_class_method"] == []   # check is new, not a pre-existing method
    assert helper["host_new"] and not helper["class_new"]
    assert helper["birth_binding"] == ["create:digits"]
    assert run(helper)["binding_field"] == ["repo"] and run(helper)["binding_method"] == []


def test_extraction_without_hints_falls_back_to_identical_text(records):
    r = records[("extract", "display")]
    assert r["moved_text"] == 2 and r["added"] == 3


def test_write_back_to_an_existing_local_is_a_binding(records):
    assert run(records[("writeback", "create")])["binding_method"] == ["name"]


def test_lambda_parameters_are_not_host_state(records):
    x = run(records[("lambda", "join")])
    assert x["binding_method"] == ["key"] and x["binding_field"] == ["service"]


def test_edited_logic_line_counts_every_reference(records):
    x = run(records[("modify", "code")])
    assert x["replaces"] == 1
    assert x["binding_method"] == ["prefix", "seq"]  # the edited line sources both
    assert x["tok_binding_method"] >= 1              # the edit itself applies .toUpperCase() to prefix


def test_new_class_has_no_bindings(records):
    r = records[("newclass", "service")]
    assert r["host_new"] and r["class_new"]
    assert r["birth_binding"] == [] and run(r)["binding_method"] == [] and run(r)["binding_field"] == []


def test_injected_parameters_do_not_binding_but_locals_do(records):
    r = records[("injected", "service")]
    assert r["injected"]
    assert run(r)["binding_method"] == ["a"]       # request and repo are injected


def test_injected_parameters_binding_when_not_wired(tmp_path):
    r = measure(tmp_path, ["injected"], [])[("injected", "service")]
    assert not r["injected"] and run(r)["binding_method"] == ["a", "repo", "request"]
    assert run(r)["binding_param"] == ["repo", "request"]   # a is a local


# ---- the binding levels (PLAN.md 4.3c): injection ignored, injection excluded

def test_a_wired_functions_parameters_are_the_frameworks_and_bind_when_injection_is_ignored(records):
    r = records[("injected", "service")]
    assert r["params_framework"] == ["repo", "request"]
    assert run(r)["binding_method"] == ["a"]                            # the registered rule
    assert run(r)["binding_method_all"] == ["a", "repo", "request"]     # injection ignored


def test_a_spring_handlers_parameters_are_the_frameworks(records):
    # a controller's public method overriding its declared API, and a method with a request mapping
    assert records[("handler", "getOwner")]["params_framework"] == ["ownerId"]
    assert records[("handler", "listOwners")]["params_framework"] == ["lastName"]
    # a public method the framework does not call: its parameters are handed to it by a caller
    assert records[("handler", "helper")]["params_framework"] == []
    # under the registered rule a handler's parameter binds, as any method's does
    assert run(records[("handler", "getOwner")])["binding_method"] == ["found", "ownerId"]
    assert records[("handler", "getOwner")]["class_injected"] == ["repo"]


def test_binding_counts_at_each_level(tmp_path):
    out = measure(tmp_path, ["handler", "injected"], ["injected\tinjected\tCheckX"])
    measured = {"records": [{**r, "unit": "cp01"} for r in out.values()], "places": None, "shape": []}
    rows = {r["name"]: r for r in tables.host_rows("x", "chain1", measured)}
    # getOwner: found and ownerId of the method; repo (injected) and served (state) of the class
    g = rows["getOwner"]
    assert (g["binding"], g["binding_all"], g["binding_none"]) == (4, 4, 2)   # none: found, served
    # helper: lastName is handed by a caller, so it binds at every level; repo does not under none
    h = rows["helper"]
    assert (h["binding"], h["binding_all"], h["binding_none"]) == (2, 2, 1)
    # the wired function: a alone binds as registered, its parameters too with injection ignored
    s = rows["service"]
    assert (s["binding"], s["binding_all"], s["binding_none"]) == (1, 3, 1)
    # the hosts read at a level: what counts as bound, and under none the injected values are gone
    none = {r["name"]: r for r in tables.at_level(list(rows.values()), "none")}
    assert none["getOwner"]["need_method_values"] == "found" and none["getOwner"]["need_class_values"] == "served"
    assert {r["name"]: r["binding"] for r in tables.at_level(list(rows.values()), "all")}["service"] == 3
    with pytest.raises(ValueError):
        tables.at_level([], "spring")


def test_parameter_bindings_are_split_out(records):
    # code(String last, int seq): the edited line uses prefix (a local) and seq (a parameter)
    assert run(records[("modify", "code")])["binding_param"] == ["seq"]
    assert run(records[("accrete", "create")])["binding_param"] == []   # digits is a local


def test_rename_hint_keeps_the_value_pre_existing(records):
    r = records[("rename", "count")]
    assert r["added"] == 1                      # the renamed lines are not edits
    assert run(r)["binding_method"] == ["total"]


def test_rename_without_hint_reads_as_new_value(tmp_path):
    r = measure(tmp_path, ["rename"], [])[("rename", "count")]
    assert r["added"] == 3
    assert run(r)["binding_method"] == ["o"]        # total reads as new; the line still sources o


def test_call_to_existing_class_method_is_a_class_binding(records):
    x = run(records[("classmethod", "create")])
    assert x["binding_class_method"] == ["audit"] and x["binding_method"] == ["o"]


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
    assert run(r)["binding_method"] == ["repo"]     # the constructor's own parameter


def test_inherited_members_are_reported_unresolved(records):
    x = run(records[("inherited", "display")])
    assert x["unresolved"] == ["getFirstName()", "lastName"]
    assert x["binding_method"] == [] and x["binding_field"] == []


@pytest.mark.parametrize("method, fields, injected", [
    ("fieldInjected", ["cache", "limit", "repo"], ["limit", "repo"]),   # @Autowired, @Value; cache is state
    ("ctorInjected", ["MAX", "repo"], ["repo"]),                         # constructor of a @Service; a constant
    ("lombok", ["counter", "repo"], ["repo"]),                           # @RequiredArgsConstructor: final fields
    ("setterInjected", ["repo"], ["repo"]),                              # an @Autowired setter
    ("dto", ["name"], []),                                               # a constructor of an unmanaged class: data
])
def test_injected_dependencies_are_reported_apart_from_other_field_bindings(records, method, fields, injected):
    x = run(records[("injection", method)])
    assert x["binding_field"] == fields and x["binding_field_injected"] == injected


def test_a_constant_is_a_field_binding(records):
    assert run(records[("constant", "code")])["binding_field"] == ["WIDTH"]


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
         "removed": 0, "replacement": False, "host_new": True, "pre_positions": 0, "binding_method": 0,
         "binding_class": 0, "binding": 0},
        {"cp": 3, "type": "A", "name": "g", "before_type": None, "before_name": None, "net_added": 1,
         "removed": 0, "replacement": False, "host_new": False, "pre_positions": 2, "binding_method": 1,
         "binding_class": 0, "binding": 1},
        {"cp": 2, "type": "B", "name": "h", "before_type": None, "before_name": None, "net_added": 1,
         "removed": 0, "replacement": False, "host_new": True, "pre_positions": 0, "binding_method": 0,
         "binding_class": 0, "binding": 0},
        {"cp": 4, "type": "B", "name": "h", "before_type": None, "before_name": None, "net_added": 0,
         "removed": 1, "replacement": False, "host_new": False, "pre_positions": 1, "binding_method": 0,
         "binding_class": 0, "binding": 0},
    ]
    # CodeTracker: A.f was renamed to A.g at cp3 (the instrument missed the rename) and changed at cp5
    ct = {"ct_identity": {(1, "A", "f"): "ct:A#g", (3, "A", "g"): "ct:A#g", (5, "A", "g"): "ct:A#g"},
          "ct_touched": {"ct:A#g": {1, 3, 5}}}
    rows = {(r["cp"], r["name"]): r for r in tables.outcome_rows("x", "c", hosts, {}, ct)}
    assert rows[(1, "f")]["identity"] == rows[(3, "g")]["identity"] == "ct:A#g"
    assert rows[(1, "f")]["intrusion_method_any"] == 2          # cp3 and cp5, from CodeTracker
    assert rows[(1, "f")]["later_touches"] == 1                 # of those, cp3's code is bound there
    assert rows[(2, "h")]["identity_source"] == "instrument"    # B.h is removed: own chaining
    assert rows[(2, "h")]["intrusion_method_any"] == 1 and rows[(2, "h")]["later_touches"] == 0

"""The instrument against the compiler (PLAN.md 4.8): a tree with known answers."""

import json
import subprocess

from placement_gravity import chain, validate

SVC = """package b;
import java.util.List;
public class Svc extends Base {
    private final Repo repo;
    public static final int LIMIT = 3;
    int open;
    public Svc(Repo repo) { this.repo = repo; }
    public int count(String name, List<String> xs) {
        int n = repo.find(name).size() + helper(xs) + LIMIT;
        Other o = new Other();
        o.value = n;
        return o.twice(n) + Other.CONST + inherited() + make().twice(n);
    }
    Other make() { return new Other(); }
    private int helper(List<String> xs) { return xs.size() + open; }
}
"""
OTHER = """package b;
public class Other { public int value; public static final int CONST = 1; int twice(int n) { return 2 * n; } }
class Base { protected int inherited() { return 1; } }
interface Repo { java.util.List<String> find(String name); }
"""


def tree(tmp_path):
    src = tmp_path / "src" / "b"
    src.mkdir(parents=True)
    (src / "Svc.java").write_text(SVC)
    (src / "Other.java").write_text(OTHER)
    (tmp_path / "places.tsv").write_text(f"cp05\t{tmp_path / 'src'}\n")
    subprocess.run(["java", "-cp", chain.CLASSPATH, "Pull", "--places", str(tmp_path / "places.tsv"),
                    str(tmp_path / "places.jsonl")], check=True)
    files = {r["path"]: r for r in map(json.loads, (tmp_path / "places.jsonl").read_text().splitlines())}
    methods, trees = validate.compiled([("cp05", tmp_path / "src")], tmp_path / "check")
    return {"files": files}, methods["cp05"], trees["cp05"]


def test_calls_and_reads_are_scored_against_the_compiler(tmp_path):
    index, theirs, t = tree(tmp_path)
    assert (t["files"], t["errors"]) == (2, 0)
    n = validate.calls(index, theirs)
    assert n["methods"] == n["methods_matched"] == 6
    # the instrument follows helper, inherited, make and o.twice; every one is the compiler's too
    assert (n["calls"], n["calls_confirmed"], n["calls_strict"]) == (4, 4, 4)
    # the compiler has those four; make().twice(n) is the same (class, name) as o.twice(n), so the
    # chained call the instrument cannot follow does not show as a miss here
    assert (n["calls_compiler"], n["calls_found"]) == (4, 4)
    assert n["calls_no_body"] == 1                      # repo.find: an interface's method, no body
    assert (n["cross_calls"], n["cross_confirmed"]) == (2, 2)     # Other.twice, Base.inherited
    assert (n["reads"], n["reads_confirmed"], n["reads_compiler"], n["reads_found"]) == (2, 2, 2, 2)


def test_a_call_the_instrument_cannot_follow_lowers_recall(tmp_path):
    global SVC
    keep = SVC
    try:
        SVC = SVC.replace("return o.twice(n) +", "return")     # only the chained call reaches twice now
        index, theirs, _ = tree(tmp_path)
    finally:
        SVC = keep
    n = validate.calls(index, theirs)
    assert (n["calls_compiler"], n["calls_found"]) == (4, 3)
    assert n["calls"] == n["calls_confirmed"] == 3


def test_bound_names_are_checked_in_the_method_after_the_change(tmp_path):
    _, theirs, _ = tree(tmp_path)
    host = {"kind": "host", "unit": "cp05", "path": "b/Svc.java", "type": "Svc", "name": "count",
            "signature": "count(String, List<String>)",
            "runs": [{"binding_method": ["name", "xs"], "binding_field": ["repo", "LIMIT"],
                      "binding_class_method": ["helper", "inherited"]},
                     # a name the compiler does not agree is a field of the class, or a value of the method
                     {"binding_method": ["open"], "binding_field": ["value"], "binding_class_method": []}]}
    n = validate.bound([host, {**host, "unit": "cp06"}], "cp05", theirs)
    assert (n["hosts"], n["hosts_matched"]) == (1, 1)
    assert (n["names_method"], n["names_method_confirmed"]) == (3, 2)
    assert (n["names_field"], n["names_field_confirmed"]) == (3, 2)
    assert (n["names_class_method"], n["names_class_method_confirmed"]) == (2, 2)
    assert n["names_wrong"] == "Svc#count:method:open Svc#count:field:value"


def test_every_fifth_checkpoint_and_the_last_are_checked_and_the_summary_gives_the_shares():
    cps = [{"cp": k, "noop": k == 5} for k in range(1, 13)]
    assert validate.sampled(cps) == ["cp06", "cp11", "cp12"]
    rows = [{"arm": "spring", "chain_id": "s/r/chain1", "classpath": "True", "calls": "10", "calls_confirmed": "9",
             "calls_compiler": "20", "calls_found": "15", "names_field": "4", "names_field_confirmed": "4"},
            {"arm": "spring", "chain_id": "s/r/chain2", "classpath": "False", "calls": "10", "calls_confirmed": "10",
             "calls_compiler": "20", "calls_found": "15", "names_field": "0", "names_field_confirmed": "0"}]
    s = validate.summary(rows)["spring"]
    assert (s["checkpoints"], s["chains"], s["with_classpath"]) == (2, 2, 1)
    assert (s["calls_precision"], s["calls_recall"], s["names_field_precision"]) == (0.95, 0.75, 1.0)
    assert s["reads_precision"] is None


def test_the_tripwire_flags_low_agreement_and_a_gap_between_the_arms_and_fails_nothing():
    good = {"calls_precision": 0.985, "calls_recall": 0.97, "cross_precision": 0.985, "cross_recall": 0.96}
    assert validate.flags({"spring": good, "officefloor": good}) == []
    low = {**good, "calls_recall": 0.88}
    f = validate.flags({"spring": good, "officefloor": low})
    assert f == ["recall of calls 0.880 in the officefloor arm, below 0.90",
                 "recall of calls differs between the arms by more than 0.05: spring 0.970, officefloor 0.880"]
    # above the mark in both arms, but the arms differ: every contrast of the arms is tilted
    apart = {**good, "cross_precision": 0.92}
    assert validate.flags({"spring": good, "officefloor": apart}) == [
        "precision of calls leaving the class differs between the arms by more than 0.05: spring 0.985, officefloor 0.920"]
    assert validate.flags({}) == [] and validate.flags({"spring": {"calls_precision": None}}) == []

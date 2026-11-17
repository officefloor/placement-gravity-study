"""Steps 2, 4 and 5 without R: the registry and its registration guard, the analysis datasets, every
verdict rule with the Holm correction, and the report."""

import csv
import json
import subprocess
from pathlib import Path

import pytest

from placement_gravity import prepare, report, runs, verdict


# ---------------------------------------------------------------- step 2

def test_the_registry_names_every_analysis_with_its_stream():
    reg = runs.load()
    names = {a["name"] for a in reg["analyses"]}
    assert {"petclinic-primary", "ui-primary", "pilot"} <= names
    primary = next(a for a in reg["analyses"] if a["name"] == "petclinic-primary")
    assert primary["exclude_chains"] == [9] and primary["stream"] == "petclinic"
    old = next(a for a in reg["analyses"] if a["name"] == "petclinic-just-solve-202608011310")
    assert old["stream"] == "petclinic-20"   # the run made on the 20-checkpoint stream


def test_an_analysis_with_one_arm_is_refused():
    reg = runs.load()
    reg["analyses"].append({"name": "x", "role": "primary", "stream": "petclinic",
                            "sources": [{"arm": "spring", "repo": "petclinic-spring"}]})
    with pytest.raises(ValueError, match="at least two arms"):
        runs.validate(reg)


def git(d, *a):
    subprocess.run(["git", "-C", str(d), *a], check=True, capture_output=True)


def test_no_run_is_read_before_the_registration_tag(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "-c", "user.email=a@b", "-c", "user.name=a", "commit", "-q", "--allow-empty", "-m", "x")
    reg = {"registration_tag": "plan-v1"}
    with pytest.raises(SystemExit, match="not registered"):
        runs.guard(reg, {"name": "petclinic-primary", "role": "primary"}, tmp_path)
    runs.guard(reg, {"name": "pilot", "role": "development"}, tmp_path)   # the pilot may be read
    git(tmp_path, "tag", "plan-v1")
    runs.guard(reg, {"name": "petclinic-primary", "role": "primary"}, tmp_path)
    # a registered file changed and not committed: refused until it is committed as an amendment
    (tmp_path / "PLAN.md").write_text("changed\n")
    with pytest.raises(SystemExit, match="uncommitted changes"):
        runs.guard(reg, {"name": "petclinic-primary", "role": "primary"}, tmp_path)
    git(tmp_path, "add", "PLAN.md")
    git(tmp_path, "-c", "user.email=a@b", "-c", "user.name=a", "commit", "-q", "-m", "amendment")
    runs.guard(reg, {"name": "petclinic-primary", "role": "primary"}, tmp_path)
    assert runs.drift("plan-v1", tmp_path) == {"tag": "plan-v1", "changed": ["PLAN.md"],
                                               "uncommitted": []}


def test_a_stack_declares_its_backend_and_wiring_roots():
    doc = {"layers": {"frontend": {"root": "web", "ext": ["ts"]},
                      "backend": {"root": "server/src/main/java/", "ext": ["java"],
                                  "config_globs": ["server/src/main/resources/officefloor/**/*.yml"]}}}
    r = runs.roots_from_stack(doc)
    assert r["java_src"] == "server/src/main/java/"
    assert r["wiring_root"] == "server/src/main/resources/officefloor/"
    assert runs.roots_from_stack({"layers": {"backend": {"root": "src/main/java"}}})["wiring_root"] \
        == "src/main/resources/officefloor/"
    with pytest.raises(ValueError):
        runs.roots_from_stack({"layers": {}})


# ---------------------------------------------------------------- step 4: datasets

def write(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def chain_tables(root: Path, arm: str, n: int, amount: int, junction_hosts: int = 12):
    cid = f"{arm}/r/chain{n}"
    d = root / "a" / f"{arm}-r-chain{n}"
    common = {"chain_id": cid, "analysis": "a", "frontend": "", "run": "r", "strategy": "s", "arm": arm}
    hosts, runs_, outs = [], [], []
    for i in range(20):
        hosts.append({**common, "cp": 2 + i, "type": "T", "signature": f"m{i}()", "name": f"m{i}",
                      "s5_class_positions": 50, "tie_no_param": 1, "shape_found": "True",
                      "s1_long": str(i < 15), "s2_stuck": "False", "s3_junction": str(i < junction_hosts),
                      "s3_junction_injection_aware": "True", "s4_cognitive": i % 4, "s5_class_gini": 0.3})
        runs_.append({**common, "cp": 2 + i, "type": "T", "signature": f"m{i}()", "host_new": "False",
                      "replacement": "False", "tie": i % 3, "tie_no_param": i % 2, "tie_class": 1,
                      "tie_no_injected": i % 2, "tie_class_no_injected": 0,
                      "pre_positions": 5 + i})
        outs.append({**common, "cp": 2 + i, "type": "T", "signature": f"m{i}()", "name": f"m{i}",
                     "intrusion_class": i % 3, "intrusion_method": i % 2, "intrusion_lines": 0,
                     "class_identity": "T", "identity": f"T#m{i}", "bystanders_class": 4,
                     "bystanders_method": i % 2, "drawn_class": i % 2, "drawn_method": 0,
                     "tied": str(i % 5 != 0), "later_checkpoints": 30 - i, "tie": i % 3, "net_added": 3,
                     "pre_positions": 5 + i, "host_new": "False"})
    runs_.append({**runs_[0], "host_new": "True"})                 # a new host: not in H1
    runs_.append({**runs_[1], "replacement": "True"})              # moved code: not in H1
    adds = [{**common, "cp": c, "positions_added": 4, "amount_positions": amount + c,
             "wiring_edges_added": 1 if arm == "officefloor" else 0,
             "wiring_files": 3 if arm == "officefloor" else 0, "wiring_lines": 30 if arm == "officefloor" else 0,
             "wiring_largest_share": 0.4 if arm == "officefloor" else "",
             "reopened": 2 if arm == "spring" else 1, "reopened_classes": 2 if arm == "spring" else 0,
             "reopened_wiring": 0 if arm == "spring" else 1} for c in range(1, 23)]
    for name, rows in (("hosts", hosts), ("runs", runs_), ("outcomes", outs), ("additions", adds)):
        write(d / f"{name}.csv", rows)


def test_prepare_builds_the_datasets_and_applies_the_rules(tmp_path):
    for n in range(1, 7):
        chain_tables(tmp_path / "m", "spring", n, 1000)
        chain_tables(tmp_path / "m", "officefloor", n, 900, junction_hosts=5)
    streamed = {c: {"mutates": [1] if c == 4 else [], "crosses": [2, 3] if c == 4 else [], "act": None}
                for c in range(1, 23)}
    out = prepare.prepare({"name": "a", "role": "primary"}, streamed, tmp_path / "m", tmp_path / "d")
    h1 = list(csv.DictReader((out / "h1.csv").open()))
    assert len(h1) == 12 * 20                         # new hosts and replacements left out
    h2 = list(csv.DictReader((out / "h2.csv").open()))
    assert {r["declared_crossings"] for r in h2 if r["cp"] == "4"} == {"3"}
    spec = json.loads((out / "spec.json").read_text())
    # s2 never flagged; s3 flagged on 5 hosts per OfficeFloor chain x 6 = 30, kept; s1 kept
    assert "s2_stuck" not in spec["shape_kept"] and {"s1_long", "s3_junction"} <= set(spec["shape_kept"])
    assert spec["shape_counts"]["s2_stuck"] == {"officefloor": 0, "spring": 0}
    cond = json.loads((out / "conditions.json").read_text())
    assert cond["chains"] == {"spring": 6, "officefloor": 6} and not cond["descriptive_only"]
    assert abs(cond["amount"]["ratio"] - (922 / 1022)) < 1e-9 and cond["amount"]["in_band"]
    assert {"prior_tie_mean", "tie"} <= set(h1[0]) and {"intrusion_class", "intrusion_method", "intrusion_lines", "own_lines"} <= set(h2[0])
    assert (out / "readings.json").exists()
    assert (out / "by.csv").exists() and (out / "capture.csv").exists()
    assert {"bystanders_class", "bystanders_method", "drawn_class", "drawn_method"} <= set(h2[0])
    assert h2[0]["class_positions"] == "50.0"
    drawn = json.loads((out / "readings.json").read_text())["drawn"]["spring"]
    # per chain 16 tied rows (i % 5 != 0): class intrusions sum(i % 3), of them drawn sum(i % 2)
    tied = [i for i in range(20) if i % 5 != 0]
    assert drawn["rows"] == 6 * 16 and drawn["class"]["later"] == 6 * sum(i % 3 for i in tied)
    assert drawn["class"]["drawn"] == 6 * sum(i % 2 for i in tied) and drawn["method"]["share"] == 0
    again = list(csv.DictReader((out / "reopen.csv").open()))
    assert len(again) == 12 * 22 and {r["reopened"] for r in again if r["arm"] == "spring"} == {"2"}
    assert cond["wiring"]["verdict"]["concentration_against"] is False


def test_fewer_than_six_chains_is_descriptive(tmp_path):
    for n in range(1, 4):
        chain_tables(tmp_path / "m", "spring", n, 1000)
        chain_tables(tmp_path / "m", "officefloor", n, 900)
    out = prepare.prepare({"name": "a", "role": "secondary"}, {}, tmp_path / "m", tmp_path / "d")
    assert json.loads((out / "conditions.json").read_text())["descriptive_only"]


# ---------------------------------------------------------------- step 4: verdicts

def test_holm():
    adj = verdict.holm({"H1": 0.01, "H2": 0.04, "H3": 0.03, "H4": None})
    assert adj["H1"] == pytest.approx(0.03) and adj["H3"] == pytest.approx(0.06)
    assert adj["H2"] == pytest.approx(0.06) and adj["H4"] is None   # monotone: max(0.06, 0.04)


def boot(est, lo, hi, p_g, p_l):
    return {"estimate": est, "lower": lo, "upper": hi, "p_greater": p_g, "p_less": p_l}


def measure(irr, lo, hi, p, outside=False):
    return {"irr": irr, "irr_lower": lo, "irr_upper": hi, "p_tost": p, "outside": outside,
            "estimate": 0, "se": 0.1, "lower": 0, "upper": 0}


def estimates(**over):
    e = {"H1": {"cp": boot(0.01, 0.002, 0.02, 0.004, 0.99),
                "within_class": boot(0.02, 0.005, 0.03, 0.003, 0.99),
                "within_method": boot(0.01, 0.001, 0.02, 0.004, 0.99)},
         "H2": {"n": 100, "class": {"irr": 1.3, "irr_lower": 1.1, "irr_upper": 1.5, "p_greater": 0.001},
                "method": {"irr": 1.2, "irr_lower": 1.05, "irr_upper": 1.4, "p_greater": 0.004}},
         "H3": {"testable": True, "bound": [0.8, 1.25], "kept": ["s1_long", "s3_junction"],
                "measures": {"s1_long": measure(1.0, 0.9, 1.1, 0.002),
                             "s3_junction": measure(1.05, 0.95, 1.15, 0.01)}},
         "H4": {"arm": boot(-0.5, -0.8, -0.2, 0.999, 0.001), "slope": boot(-0.2, -0.3, -0.1, 0.99, 0.002),
                "intrusion_class": {"irr": 0.4, "irr_lower": 0.3, "irr_upper": 0.6, "p_less": 0.001},
                "intrusion_method": {"irr": 0.5, "irr_lower": 0.3, "irr_upper": 0.8, "p_less": 0.003}}}
    e.update(over)
    return e


COND = {"descriptive_only": False, "amount": {"in_band": True, "ratio": 0.95},
        "wiring": {"verdict": {"growth_against": False, "concentration_against": False}}}


def test_all_supported():
    v = verdict.decide(estimates(), COND)["hypotheses"]
    assert [v[k]["verdict"] for k in ("H1", "H2", "H3", "H4")] == ["supported"] * 4


def test_h1_needs_the_rise_within_a_class_and_within_a_method():
    e = estimates()
    e["H1"]["within_method"] = boot(0.001, -0.01, 0.012, 0.4, 0.6)
    assert verdict.decide(e, COND)["hypotheses"]["H1"]["verdict"] == "not supported"
    e["H1"]["within_method"] = {"error": "no place with runs at two checkpoints"}
    assert verdict.decide(e, COND)["hypotheses"]["H1"]["verdict"] == "not estimable"


def test_h2_needs_both_the_class_and_the_method():
    e = estimates()
    e["H2"]["method"] = {"irr": 1.1, "irr_lower": 0.9, "irr_upper": 1.3, "p_greater": 0.2}
    assert verdict.decide(e, COND)["hypotheses"]["H2"]["verdict"] == "not supported"
    e["H2"]["method"] = {"irr": 0.7, "irr_lower": 0.5, "irr_upper": 0.9, "p_greater": 0.99}
    assert verdict.decide(e, COND)["hypotheses"]["H2"]["verdict"] == "reversed"


def test_h2_and_h3_are_decided_apart():
    """What stood by can draw later code in (H2) while the shape is unresolved (H3), and the other way."""
    e = estimates()
    e["H3"]["measures"]["s1_long"] = measure(1.1, 0.7, 1.5, 0.3)
    v = verdict.decide(e, COND)["hypotheses"]
    assert v["H2"]["verdict"] == "supported" and v["H3"]["verdict"] == "unresolved"


def test_h3_shape_carrying_information_is_not_supported():
    e = estimates()
    e["H3"]["measures"]["s1_long"] = measure(1.6, 1.3, 1.9, 0.99, outside=True)
    v = verdict.decide(e, COND)["hypotheses"]["H3"]
    assert v["state"] == "against" and v["verdict"] == "not supported"


def test_h3_without_a_testable_shape_measure_says_so():
    e = estimates(H3={"testable": False, "bound": [0.8, 1.25], "kept": []})
    v = verdict.decide(e, COND)["hypotheses"]
    assert v["H3"]["verdict"] == "not testable" and set(v["H3"]["dropped"]) == set(verdict.SHAPES)
    assert v["H2"]["verdict"] == "supported"          # H2 no longer waits on the shape


def test_h4_fails_on_the_amount_the_wiring_or_intrusion():
    c = json.loads(json.dumps(COND))
    c["amount"]["in_band"] = False
    assert verdict.decide(estimates(), c)["hypotheses"]["H4"]["verdict"] == "not supported"
    c = json.loads(json.dumps(COND))
    c["wiring"]["verdict"]["growth_against"] = True
    assert verdict.decide(estimates(), c)["hypotheses"]["H4"]["verdict"] == "not supported"
    e = estimates()
    e["H4"]["intrusion_method"] = {"irr": 0.9, "irr_lower": 0.7, "irr_upper": 1.2, "p_less": 0.2}
    assert verdict.decide(e, COND)["hypotheses"]["H4"]["verdict"] == "not supported"


def test_reversed_and_holm_failures():
    e = estimates()
    e["H1"]["cp"] = boot(-0.01, -0.02, -0.002, 0.999, 0.001)
    assert verdict.decide(e, COND)["hypotheses"]["H1"]["verdict"] == "reversed"
    # each interval clears its line, but p = 0.02 for all four: Holm makes them 0.08
    e = estimates(H1={k: boot(0.01, 0.001, 0.02, 0.02, 0.98) for k in ("cp", "within_class", "within_method")})
    e["H2"]["class"]["p_greater"] = e["H2"]["method"]["p_greater"] = 0.02
    e["H3"]["measures"] = {"s1_long": measure(1.0, 0.9, 1.1, 0.02)}
    e["H4"] = {"arm": boot(-0.5, -0.8, -0.01, 0.98, 0.02), "slope": boot(-0.2, -0.3, -0.01, 0.98, 0.02),
               "intrusion_class": {"irr": 0.4, "irr_lower": 0.3, "irr_upper": 0.9, "p_less": 0.02},
               "intrusion_method": {"irr": 0.4, "irr_lower": 0.3, "irr_upper": 0.9, "p_less": 0.02}}
    v = verdict.decide(e, COND)["hypotheses"]
    assert v["H1"]["p_holm"] == pytest.approx(0.08) and v["H1"]["verdict"] == "not supported"


def test_descriptive_only_decides_nothing():
    c = {**COND, "descriptive_only": True}
    assert {v["verdict"] for v in verdict.decide(estimates(), c)["hypotheses"].values()} == {"descriptive only"}


def test_an_error_in_a_model_is_not_estimable():
    e = estimates()
    e["H1"]["cp"] = {"error": "no fit"}
    v = verdict.decide(e, COND)
    assert v["hypotheses"]["H1"]["verdict"] == "not estimable"
    e = estimates()
    e["H2"]["method"] = {"error": "standard error not computed: tie"}
    v = verdict.decide(e, COND)["hypotheses"]
    assert v["H2"]["verdict"] == "not estimable" and v["H1"]["verdict"] == "supported"


# ---------------------------------------------------------------- step 5

def test_the_report_names_every_hypothesis_and_commit():
    est = {**estimates(), "boot": 1000, "seed": 1, "versions": {"R": "x"}, "reported": {}}
    ver = verdict.decide(est, COND)
    cond = {**COND, "chains": {"spring": 9, "officefloor": 9}}
    heads = [{"arm": "spring", "run": "r", "chain": 1, "excluded": False, "sha": "a" * 40}]
    md = report.render("petclinic-primary", "primary", est, ver, cond, {"shape_counts": {}}, heads)
    for k in ("H1", "H2", "H3", "H4", "supported", "`aaaaaaaaaaaa`", "s3_junction", "At the class (its fields)", "Within a class",
              "Later intrusion where tied code was placed"):
        assert k in md
    rd = {"choice": {"spring": {"checkpoints": 59, "no_choice": 12, "median_tie_sd": 0.5,
                                "median_distinct_hosts": 2}},
          "drawn": {"spring": {"rows": 80, "class": {"bystanders": 7.5, "later": 900, "drawn": 400, "share": 0.444},
                               "method": {"bystanders": 1.5, "later": 300, "drawn": 50, "share": 0.167}}},
          "review": {"against": "petclinic-primary",
                     "spring": {"rho": -0.4, "interval": [-0.6, -0.1], "checkpoints": 59, "against": False}}}
    md = report.render("x", "secondary", est, ver, cond, {"shape_counts": {}}, heads,
                       {"tag": "plan-v1", "changed": ["PLAN.md"]}, rd)
    for k in ("12 of 59 checkpoints left no choice", "Review against petclinic-primary", "`PLAN.md`",
              "own lines", "400 of 900 later intrusions tied to one of them"):
        assert k in md

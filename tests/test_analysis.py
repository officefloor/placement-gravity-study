"""Steps 2, 4 and 5 without R: the registry and its registration guard, the analysis datasets, every
verdict rule with the Holm correction, and the report."""

import csv
import json
import subprocess
from pathlib import Path

import pytest

from placement_gravity import prepare, report, runs, tables, verdict


# ---------------------------------------------------------------- step 2

def test_the_registry_names_every_analysis_with_its_stream():
    reg = runs.load()
    names = {a["name"] for a in reg["analyses"]}
    assert {"petclinic-just-solve-202608100006", "ui-primary", "pilot"} <= names
    primary = next(a for a in reg["analyses"] if a["name"] == "petclinic-just-solve-202608100006")
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
                      "s5_class_positions": 50, "binding_no_param": 1, "shape_found": "True",
                      "s1_long": str(i < 15), "s2_stuck": "False", "s3_junction": str(i < junction_hosts),
                      "s3_junction_injection_aware": "True", "s4_cognitive": i % 4, "s5_class_gini": 0.3})
        runs_.append({**common, "cp": 2 + i, "type": "T", "signature": f"m{i}()", "host_new": "False",
                      "replacement": "False", "binding": i % 3, "binding_no_param": i % 2, "binding_class": 1,
                      "binding_no_injected": i % 2, "binding_class_no_injected": 0,
                      "pre_positions": 5 + i})
        outs.append({**common, "cp": 2 + i, "type": "T", "signature": f"m{i}()", "name": f"m{i}",
                     "intrusion_class": i % 3, "intrusion_method": i % 2, "intrusion_lines": 0,
                     "class_identity": "T", "identity": f"T#m{i}", "bystanders_class": 4,
                     "bystanders_method": i % 2, "drawn_class": i % 2, "drawn_method": 0,
                     "bound": str(i % 5 != 0), "later_checkpoints": 30 - i, "binding": i % 3, "net_added": 3,
                     "pre_positions": 5 + i, "host_new": "False"})
    runs_.append({**runs_[0], "host_new": "True"})                 # a new host: not in H3
    runs_.append({**runs_[1], "replacement": "True"})              # moved code: not in H3
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
    h3 = list(csv.DictReader((out / "h3.csv").open()))
    assert len(h3) == 12 * 20                         # new hosts and replacements left out
    h2 = list(csv.DictReader((out / "h2.csv").open()))
    assert {r["declared_crossings"] for r in h2 if r["cp"] == "4"} == {"3"}
    spec = json.loads((out / "spec.json").read_text())
    # H6's block is the literature's shape measures; the sinew measures are read apart. s2 never
    # flagged; s3 flagged on 5 hosts per OfficeFloor chain x 6 = 30, kept
    assert "s1_long" in spec["shape_kept"] and not {"s2_stuck", "s3_junction"} & set(spec["shape_kept"])
    assert spec["sinew_kept"] == ["s3_junction"]
    # H6's measures are those of its six that vary; the fixture has no literature measures
    assert spec["h6_all"] == list(verdict.SHAPES) and "s1_long" in spec["h6_measures"]
    assert spec["class_level"]["testable"] is False       # one class in the fixture
    assert "m_cyclomatic" not in spec["h6_measures"] and spec["reach"] == ["m_fanout", "c_cbo", "c_fanout"]
    assert spec["shape_counts"]["s2_stuck"] == {"officefloor": 0, "spring": 0}
    cond = json.loads((out / "conditions.json").read_text())
    assert cond["chains"] == {"spring": 6, "officefloor": 6} and not cond["descriptive_only"]
    assert abs(cond["amount"]["ratio"] - (922 / 1022)) < 1e-9 and cond["amount"]["in_band"]
    assert {"prior_binding_mean", "binding"} <= set(h3[0]) and {"intrusion_class", "intrusion_method", "intrusion_lines", "own_lines"} <= set(h2[0])
    assert (out / "readings.json").exists()
    assert (out / "by.csv").exists() and (out / "capture.csv").exists()
    assert {"bystanders_class", "bystanders_method", "drawn_class", "drawn_method"} <= set(h2[0])
    assert h2[0]["class_positions"] == "50.0"
    drawn = json.loads((out / "readings.json").read_text())["drawn"]["spring"]
    # per chain 16 bound rows (i % 5 != 0): class intrusions sum(i % 3), of them drawn sum(i % 2)
    bound = [i for i in range(20) if i % 5 != 0]
    assert drawn["rows"] == 6 * 16 and drawn["class"]["later"] == 6 * sum(i % 3 for i in bound)
    assert drawn["class"]["drawn"] == 6 * sum(i % 2 for i in bound) and drawn["method"]["share"] == 0
    again = list(csv.DictReader((out / "reopen.csv").open()))
    assert len(again) == 12 * 22 and {r["reopened"] for r in again if r["arm"] == "spring"} == {"2"}
    assert cond["wiring"]["verdict"]["concentration_against"] is False


def test_class_measures_are_tested_only_where_classes_can_be_told_apart():
    def row(chain, cp, cls, arrivals, bound=True):
        return {"chain_id": chain, "cp": cp, "class_identity": cls, "bound": bound, "intrusion_class": arrivals}
    # one class holds nearly everything, as a single handler does
    one = [row("c", k, "Controller", 9) for k in range(10)] + [row("c", 1, "Mapper", 2)]
    got = prepare.class_level(one)
    assert got["classes_with_arrivals"] == 2 and got["top_class_share"] == pytest.approx(90 / 92)
    assert got["testable"] is False
    # twelve classes sharing the arrivals; a class's rows of one checkpoint count once
    many = [row("c", 1, f"C{i}", 3) for i in range(12)] + [row("c", 1, "C0", 3), row("c", 1, "X", 5, bound=False)]
    got = prepare.class_level(many)
    assert got["classes_with_arrivals"] == 12 and got["top_class_share"] == pytest.approx(1 / 12)
    assert got["testable"] is True


def test_fewer_than_six_chains_is_descriptive(tmp_path):
    for n in range(1, 4):
        chain_tables(tmp_path / "m", "spring", n, 1000)
        chain_tables(tmp_path / "m", "officefloor", n, 900)
    out = prepare.prepare({"name": "a", "role": "secondary"}, {}, tmp_path / "m", tmp_path / "d")
    assert json.loads((out / "conditions.json").read_text())["descriptive_only"]


# ---------------------------------------------------------------- step 4: verdicts

def test_holm():
    adj = verdict.holm({"H3": 0.01, "H2": 0.04, "H6": 0.03, "H4": None})
    assert adj["H3"] == pytest.approx(0.03) and adj["H6"] == pytest.approx(0.06)
    assert adj["H2"] == pytest.approx(0.06) and adj["H4"] is None   # monotone: max(0.06, 0.04)


def boot(est, lo, hi, p_g, p_l):
    return {"estimate": est, "lower": lo, "upper": hi, "p_greater": p_g, "p_less": p_l}


def measure(irr, lo, hi, p, outside=False):
    return {"irr": irr, "irr_lower": lo, "irr_upper": hi, "p_upper": p, "p_tost": p, "outside": outside,
            "above": lo > 1.25, "estimate": 0, "se": 0.1, "lower": 0, "upper": 0}


def estimates(**over):
    e = {"H3": {"cp": boot(0.01, 0.002, 0.02, 0.004, 0.99),
                "within_class": boot(0.02, 0.005, 0.03, 0.003, 0.99),
                "within_method": boot(0.01, 0.001, 0.02, 0.004, 0.99)},
         "H2": {"n": 100, "class": {"irr": 1.3, "irr_lower": 1.1, "irr_upper": 1.5, "p_greater": 0.001},
                "method": {"irr": 1.2, "irr_lower": 1.05, "irr_upper": 1.4, "p_greater": 0.004}},
         "H6": {"testable": True, "margin": [0.8, 1.25], "kept": ["s1_long", "s4_cognitive"],
                "measures": {"s1_long": measure(1.0, 0.9, 1.1, 0.002),
                             "s4_cognitive": measure(1.05, 0.95, 1.15, 0.01)}},
         "H4": {"arm": boot(-0.5, -0.8, -0.2, 0.999, 0.001), "slope": boot(-0.2, -0.3, -0.1, 0.99, 0.002),
                "intrusion_class": {"irr": 0.4, "irr_lower": 0.3, "irr_upper": 0.6, "p_less": 0.001},
                "intrusion_method": {"irr": 0.5, "irr_lower": 0.3, "irr_upper": 0.8, "p_less": 0.003},
                "trodden": {"irr": 0.7, "irr_lower": 0.5, "irr_upper": 0.9, "p_less": 0.002}}}
    e.update(over)
    return e


COND = {"descriptive_only": False, "amount": {"in_band": True, "ratio": 0.95},
        "wiring": {"verdict": {"growth_against": False, "concentration_against": False}}}


def test_all_supported():
    v = verdict.decide(estimates(), COND)["hypotheses"]
    assert [v[k]["verdict"] for k in ("H3", "H2", "H6", "H4")] == ["supported"] * 4


def test_h3_needs_the_rise_within_a_class_and_within_a_method():
    e = estimates()
    e["H3"]["within_method"] = boot(0.001, -0.01, 0.012, 0.4, 0.6)
    assert verdict.decide(e, COND)["hypotheses"]["H3"]["verdict"] == "not supported"
    e["H3"]["within_method"] = {"error": "no place with runs at two checkpoints"}
    assert verdict.decide(e, COND)["hypotheses"]["H3"]["verdict"] == "not estimable"


def test_h2_needs_both_the_class_and_the_method():
    e = estimates()
    e["H2"]["method"] = {"irr": 1.1, "irr_lower": 0.9, "irr_upper": 1.3, "p_greater": 0.2}
    assert verdict.decide(e, COND)["hypotheses"]["H2"]["verdict"] == "not supported"
    e["H2"]["method"] = {"irr": 0.7, "irr_lower": 0.5, "irr_upper": 0.9, "p_greater": 0.99}
    assert verdict.decide(e, COND)["hypotheses"]["H2"]["verdict"] == "reversed"


def test_h2_and_h6_are_decided_apart():
    """What stood by can draw later code in (H2) while the shape is unresolved (H6), and the other way."""
    e = estimates()
    e["H6"]["measures"]["s1_long"] = measure(1.1, 0.7, 1.5, 0.3)
    v = verdict.decide(e, COND)["hypotheses"]
    assert v["H2"]["verdict"] == "supported" and v["H6"]["verdict"] == "unresolved"


def test_h6_is_one_sided_a_shape_that_raises_intrusion_counts_against():
    e = estimates()
    e["H6"]["measures"]["s1_long"] = measure(1.6, 1.3, 1.9, 0.99, outside=True)
    v = verdict.decide(e, COND)["hypotheses"]["H6"]
    assert v["state"] == "against" and v["verdict"] == "not supported" and v["two_sided"] == "outside"


def test_h6_a_shape_that_lowers_intrusion_does_not_count_against():
    """The development chain's case: complexity at 0.38 [0.23, 0.63]. Below the upper margin, so H6
    holds; the two-sided reading, reported, says it lies outside."""
    e = estimates()
    e["H6"]["measures"]["s1_long"] = measure(0.38, 0.23, 0.63, 0.0001, outside=True)
    v = verdict.decide(e, COND)["hypotheses"]["H6"]
    assert v["state"] == "not above" and v["verdict"] == "supported" and v["two_sided"] == "outside"
    # an interval reaching above the margin is unresolved, not supported
    e["H6"]["measures"]["s1_long"] = measure(0.9, 0.5, 1.6, 0.2)
    assert verdict.decide(e, COND)["hypotheses"]["H6"]["verdict"] == "unresolved"


def test_h6_without_a_testable_shape_measure_says_so():
    e = estimates(H6={"testable": False, "margin": [0.8, 1.25], "kept": []})
    v = verdict.decide(e, COND)["hypotheses"]
    assert v["H6"]["verdict"] == "not testable" and set(v["H6"]["dropped"]) == set(verdict.SHAPES)
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
    e["H3"]["cp"] = boot(-0.01, -0.02, -0.002, 0.999, 0.001)
    assert verdict.decide(e, COND)["hypotheses"]["H3"]["verdict"] == "reversed"
    # each interval clears its line, but p = 0.02 for all four confirmatory: Holm makes them 0.08;
    # H3 and H7, secondary, are decided on their own p = 0.02
    e = estimates(H3={k: boot(0.01, 0.001, 0.02, 0.02, 0.98) for k in ("cp", "within_class", "within_method")})
    e["H2"]["class"]["p_greater"] = e["H2"]["method"]["p_greater"] = 0.02
    e["H4"] = {"arm": boot(-0.5, -0.8, -0.01, 0.98, 0.02), "slope": boot(-0.2, -0.3, -0.01, 0.98, 0.02),
               "intrusion_class": {"irr": 0.4, "irr_lower": 0.3, "irr_upper": 0.9, "p_less": 0.02},
               "intrusion_method": {"irr": 0.4, "irr_lower": 0.3, "irr_upper": 0.9, "p_less": 0.02},
               "trodden": {"irr": 0.7, "irr_lower": 0.5, "irr_upper": 0.9, "p_less": 0.02}}
    e["H1"] = {"contrast": {"arm": {"irr": 0.6, "irr_lower": 0.4, "irr_upper": 0.9, "p_less": 0.02},
                            "trend": {"irr": 0.7, "irr_lower": 0.5, "irr_upper": 0.95, "p_less": 0.02}}}
    up = {"irr": 1.5, "irr_lower": 1.1, "irr_upper": 2.0, "p_greater": 0.02}
    e["H7"] = {"margin": [0.8, 1.25], "forced": {"irr": 0.9, "irr_lower": 0.7, "irr_upper": 1.1, "p_upper": 0.02}}
    e["H5"] = {"arm": {"irr": 0.6, "irr_lower": 0.4, "irr_upper": 0.9, "p_less": 0.02},
               "trend": {"irr": 0.7, "irr_lower": 0.5, "irr_upper": 0.95, "p_less": 0.02}}
    v = verdict.decide(e, COND)["hypotheses"]
    assert v["H2"]["p_holm"] == pytest.approx(0.08) and v["H2"]["verdict"] == "not supported"
    assert v["H3"]["p_holm"] == pytest.approx(0.02) and v["H3"]["verdict"] == "supported"
    assert v["H7"]["p_holm"] == pytest.approx(0.02) and v["H7"]["verdict"] == "supported"


def test_descriptive_only_decides_nothing():
    c = {**COND, "descriptive_only": True}
    assert {v["verdict"] for v in verdict.decide(estimates(), c)["hypotheses"].values()} == {"descriptive only"}


def test_an_error_in_a_model_is_not_estimable():
    e = estimates()
    e["H3"]["cp"] = {"error": "no fit"}
    v = verdict.decide(e, COND)
    assert v["hypotheses"]["H3"]["verdict"] == "not estimable"
    e = estimates()
    e["H2"]["method"] = {"error": "standard error not computed: binding"}
    v = verdict.decide(e, COND)["hypotheses"]
    assert v["H2"]["verdict"] == "not estimable" and v["H3"]["verdict"] == "supported"


# ---------------------------------------------------------------- step 5

def test_the_report_names_every_hypothesis_and_commit():
    est = {**estimates(), "boot": 1000, "seed": 1, "versions": {"R": "x"}, "reported": {
        "sinew": {"s3_junction": {"method": {"irr": 1.4, "irr_lower": 1.1, "irr_upper": 1.8},
                                  "class": {"irr": 1.2, "irr_lower": 0.9, "irr_upper": 1.6}}}}}
    ver = verdict.decide(est, COND)
    cond = {**COND, "chains": {"spring": 9, "officefloor": 9}}
    heads = [{"arm": "spring", "run": "r", "chain": 1, "excluded": False, "sha": "a" * 40}]
    md = report.render("petclinic-primary", "primary", est, ver, cond, {"shape_counts": {}}, heads)
    for k in ("H3", "H2", "H6", "H4", "supported", "`aaaaaaaaaaaa`", "s3_junction", "At the class (the private members the code was bound to)", "H1, the force: forced less with function injection", "H7, spread does not see it", "H5, surface against volume", "Within a class",
              "the sinew measures", "s3_junction at the method 1.400 [1.100, 1.800]",
              "Later intrusion where bound code was placed"):
        assert k in md
    rd = {"choice": {"spring": {"checkpoints": 59, "no_choice": 12, "median_binding_sd": 0.5,
                                "median_distinct_hosts": 2}},
          "drawn": {"spring": {"rows": 80, "class": {"bystanders": 7.5, "later": 900, "drawn": 400, "share": 0.444},
                               "method": {"bystanders": 1.5, "later": 300, "drawn": 50, "share": 0.167}}},
          "review": {"against": "petclinic-primary",
                     "spring": {"rho": -0.4, "interval": [-0.6, -0.1], "checkpoints": 59, "against": False}}}
    md = report.render("x", "secondary", est, ver, cond, {"shape_counts": {}}, heads,
                       {"tag": "plan-v1", "changed": ["PLAN.md"]}, rd)
    for k in ("12 of 59 checkpoints left no choice", "Review against petclinic-primary", "`PLAN.md`",
              "own lines", "400 of 900 later intrusions bound to one of them"):
        assert k in md


FALL = {"irr": 0.5, "irr_lower": 0.3, "irr_upper": 0.8, "p_less": 0.004}
LESS = {"irr": 0.3, "irr_lower": 0.2, "irr_upper": 0.6, "p_less": 0.001}


def h1_contrast(arm, trend, fall=FALL):
    return {"H1": {"class": fall, "contrast": {"arm": arm, "trend": trend}}}


def test_h1_is_the_function_arm_forced_less_and_rising_less():
    # restated 25 November 2026 (PLAN.md 9 row 107): both terms below 1, p the larger
    flat = {"irr": 1.0, "irr_lower": 0.7, "irr_upper": 1.4, "p_less": 0.5}
    more = {"irr": 2.0, "irr_lower": 1.3, "irr_upper": 3.0, "p_less": 0.999}
    def v(**h):
        return verdict.decide(estimates(**h1_contrast(**h)), COND)["hypotheses"]["H1"]
    assert v(arm=LESS, trend=LESS)["verdict"] == "supported"
    got = v(arm=LESS, trend=flat)
    assert got["verdict"] == "not supported" and got["p"] == 0.5
    assert v(arm=more, trend=LESS)["verdict"] == "reversed"


def test_h1_does_not_need_choice_to_narrow():
    # the methods arm's alternatives (choice narrows, the test until 25 November 2026) are reported:
    # neither a rise nor every placement forced from the start keeps the contrast from deciding H1
    rising = {"irr": 2.0, "irr_lower": 1.5, "irr_upper": 2.6, "p_less": 0.999}
    for fall in (rising, {"error": "every placement forced", "all_forced": True}):
        v = verdict.decide(estimates(**h1_contrast(LESS, LESS, fall)), COND)["hypotheses"]["H1"]
        assert v["verdict"] == "supported" and v["detail"]["class"] == fall


def test_h1_is_not_testable_on_a_history_and_does_not_enter_holm():
    v = verdict.decide(estimates(H1={"class": FALL}), COND)["hypotheses"]
    assert (v["H1"]["verdict"], v["H1"]["state"], v["H1"]["p"]) == ("not testable", "a history", None)
    assert v["H2"]["p_holm"] == pytest.approx(0.006)   # over H2 and H4 only
    v = verdict.decide(estimates(H1={"contrast": {"error": "no checkpoints in both arms"}}), COND)["hypotheses"]
    assert v["H1"]["verdict"] == "not estimable"


def test_holm_runs_over_the_four_confirmatory_and_the_secondary_keep_their_own_p():
    v = verdict.decide(estimates(**h1_contrast({**LESS, "p_less": 0.011}, LESS)), COND)["hypotheses"]
    assert len(v) == 7
    assert {k for k, x in v.items() if x["tier"] == "confirmatory"} == {"H2", "H4", "H1", "H5"}
    assert {k for k, x in v.items() if x["tier"] == "secondary"} == {"H3", "H6", "H7"}
    assert v["H1"]["p_holm"] >= 0.011
    assert v["H3"]["tier"] == "secondary" and v["H3"]["p_holm"] == v["H3"]["p"]


def test_h2_needs_the_core_come_back_to_less_in_the_function_arm_where_the_arms_can_be_compared():
    less = {"required": True, "irr": 0.2, "irr_lower": 0.1, "irr_upper": 0.5, "p_less": 0.03}
    same = {"required": True, "irr": 0.9, "irr_lower": 0.6, "irr_upper": 1.3, "p_less": 0.3}
    few = {"required": False, "note": "too few core records in an arm to compare", "function_records": 1}

    def h2(**reuse):
        e = estimates()
        e["H2"].update(reuse)
        return verdict.decide(e, COND)["hypotheses"]["H2"]
    v = h2(reuse_class=few, reuse_method=less)
    assert (v["verdict"], v["arm_contrast"], v["p"]) == ("supported", ["method"], 0.03)
    # the core used more than the periphery in the methods arm is not enough: a value used once is
    # likely to be used again whatever the place
    assert h2(reuse_class=few, reuse_method=same)["verdict"] == "not supported"
    more = {"required": True, "irr": 2.0, "irr_lower": 1.4, "irr_upper": 2.9, "p_less": 0.99}
    assert h2(reuse_class=few, reuse_method=more)["verdict"] == "reversed"
    assert h2(reuse_class=few, reuse_method={"required": True, "error": "no fit"})["verdict"] == "not estimable"
    # no core value of the function arm ever come back to: decided by the rank-sum over chains
    never = {"required": True, "separated": True, "irr": 0, "irr_lower": 0, "irr_upper": 0, "p_less": 0.0002}
    assert h2(reuse_class=never, reuse_method=less)["arm_contrast"] == ["class", "method"]
    # a history: its arms do not solve the same problems, so H2 is the core against the periphery
    hist = {"required": False, "note": "a history"}
    assert h2(reuse_class=hist, reuse_method=hist)["arm_contrast"] == []


def test_h4_needs_less_trodden_files_gone_back_into_java_and_wiring_alike():
    e = estimates()
    e["H4"]["trodden"] = {"irr": 1.3, "irr_lower": 1.0, "irr_upper": 1.7, "p_less": 0.96}
    assert verdict.decide(e, COND)["hypotheses"]["H4"]["verdict"] == "not supported"
    e["H4"]["trodden"] = {"error": "trodden was not measured"}
    assert verdict.decide(e, COND)["hypotheses"]["H4"]["verdict"] == "not estimable"
    e["H4"]["trodden"] = {"not_applicable": True}                 # a history
    assert verdict.decide(e, COND)["hypotheses"]["H4"]["verdict"] == "supported"
    rows = prepare.reopen_rows([{"chain_id": "c", "arm": "officefloor", "cp": "3", "reopened": "2",
                                 "reopened_classes": "1", "reopened_wiring": "1",
                                 "existing_java_files": "2", "existing_wiring_files": "1"},
                                {"chain_id": "c", "arm": "officefloor", "cp": "4", "reopened": "0",
                                 "reopened_classes": "0", "reopened_wiring": "0"}])   # measured before the count
    assert (rows[0]["existing_files"], rows[1]["existing_files"], rows[0]["trodden"]) == (3, None, None)


def test_trodden_counts_the_earlier_checkpoints_that_changed_each_file_gone_back_into():
    measured = {"checkpoints": [{"cp": k} for k in (1, 2, 3, 4)],
                "java_changed": {"cp01": [[None, "A.java"], ["Base.java", "Base.java"]],
                                 "cp02": [["A.java", "A.java"], [None, "B.java"]],
                                 "cp03": [["A.java", "A2.java"], ["B.java", "B.java"]],      # A renamed
                                 "cp04": [["A2.java", "A2.java"], ["Base.java", None]]},      # Base deleted
                "wiring_changes": {"cp01": [["A", "flow.yml"]], "cp02": [["M", "flow.yml"]],
                                   "cp03": [], "cp04": [["M", "flow.yml"]]}}
    t = tables.trodden(measured)
    # cp1: Base had no checkpoint's change before (the code the chain started from is not counted)
    assert t["cp01"] == {"trodden": 0, "trodden_java": 0, "trodden_wiring": 0}
    assert t["cp02"] == {"trodden": 2, "trodden_java": 1, "trodden_wiring": 1}     # A (cp1), flow (cp1)
    assert t["cp03"] == {"trodden": 3, "trodden_java": 3, "trodden_wiring": 0}     # A (cp1, cp2), B (cp2)
    assert t["cp04"] == {"trodden": 6, "trodden_java": 4, "trodden_wiring": 2}     # A2 keeps A's 3; Base 1; flow 2
    assert tables.trodden({"checkpoints": []}) == {}


def test_h6_with_the_coupling_measures_put_back_is_reported_and_changes_no_verdict():
    e = estimates()
    e["reported"] = {"H6_with_coupling": {"margin": [0.8, 1.25], "measures": {
        **e["H6"]["measures"], "m_fanout": measure(3.0, 1.6, 5.5, 0.99), "c_cbo": {"error": "does not vary"}}}}
    out = verdict.decide(e, COND)
    sens = out["sensitivity"]["H6_with_coupling"]
    assert (sens["state"], sens["above"], sens["not_estimable"]) == ("against", ["m_fanout"], ["c_cbo"])
    assert out["hypotheses"]["H6"]["verdict"] == "supported"
    assert verdict.decide(estimates(), COND)["sensitivity"]["H6_with_coupling"]["state"] == "not testable"


def test_the_lever_within_forced_tells_injected_private_fields_from_the_class_own():
    places = {"cp2": {"files": {"A.java": {
        "classes": [{"name": "A", "fields": {"service": "private", "LIMIT": "private", "open": "public"}}],
        "methods": [{"type": "A", "name": "helper", "signature": "helper()", "access": "private"}]}}}}
    r = {"unit": "cp2", "type": "A", "before_type": "A"}
    assert tables.lever(r, ["service"], ["service"], [], places) == "injected"     # another class could declare it
    assert tables.lever(r, ["service", "LIMIT"], ["service"], [], places) == "own"  # a private constant
    assert tables.lever(r, ["service"], ["service"], ["helper"], places) == "own"   # a private method
    assert tables.lever(r, ["open"], [], [], places) is None                         # not forced
    assert tables.encapsulated(r, ["service"], [], places) is True                   # still forced: private

    def host(lever, choice, added=4, forced=True):
        return {"chain_id": "spring/r/chain1", "arm": "spring", "cp": 2, "type": "A", "before_type": "A",
                "added": added, "net_added": added, "replacement": False, "class_new": False,
                "choice_class": choice, "forced_enc": forced, "forced_lever": lever}
    g = prepare.growth_by_lever([host("own", 0), host("injected", 2), host("injected", 0, added=2),
                                 host("", "", added=10, forced="")])["spring"]
    assert (g["forced"], g["own"], g["injected_elsewhere"], g["injected_only_here"], g["all"]) == (10, 4, 4, 2, 20)
    assert g["opportunity_share"] == pytest.approx(0.6) and g["forced_share_of_growth"] == pytest.approx(0.5)


def h8_estimates(ic, co):
    return {**estimates(), "coupled_arm": co,
            "H4": {**estimates()["H4"], "intrusion_class": ic}}


def test_h8_run_d_needs_less_coming_back_more_coupling_compliance_and_the_amount():
    less = {"irr": 0.5, "irr_lower": 0.3, "irr_upper": 0.8, "p_less": 0.004}
    more = {"irr": 1.6, "irr_lower": 1.2, "irr_upper": 2.1, "p_greater": 0.01}
    cond = {**COND, "contrast": "no-encapsulation", "compliance": {"share": 0.96, "introduced": 900}}
    v = verdict.decide(h8_estimates(less, more), cond)["hypotheses"]
    assert v["H8"]["verdict"] == "supported" and v["H8"]["p"] == pytest.approx(0.01)
    assert all(v[k]["verdict"] == "descriptive only" for k in ("H3", "H2", "H6", "H4", "H1", "H7", "H5"))
    same = {"irr": 1.0, "irr_lower": 0.8, "irr_upper": 1.3, "p_greater": 0.5}
    assert verdict.decide(h8_estimates(less, same), cond)["hypotheses"]["H8"]["verdict"] == "not supported"
    fewer = {"irr": 0.6, "irr_lower": 0.4, "irr_upper": 0.9, "p_greater": 0.99}
    assert verdict.decide(h8_estimates(less, fewer), cond)["hypotheses"]["H8"]["verdict"] == "reversed"
    # the instruction did not take: Run D is not read against Run A
    low = {**cond, "compliance": {"share": 0.7, "introduced": 900}}
    assert verdict.decide(h8_estimates(less, more), low)["hypotheses"]["H8"]["verdict"] == "descriptive only"
    out = {**cond, "amount": {"in_band": False, "ratio": 1.6}}
    assert verdict.decide(h8_estimates(less, more), out)["hypotheses"]["H8"]["verdict"] == "not supported"
    assert "H8" not in verdict.decide(estimates(), COND)["hypotheses"]
    members = [{"arm": "open", "introduced": "10", "introduced_private": "1"},
               {"arm": "open", "introduced": "", "introduced_private": ""},
               {"arm": "encapsulated", "introduced": "10", "introduced_private": "8"}]
    assert prepare.compliance(members, "open") == {"arm": "open", "introduced": 10, "private": 1, "share": 0.9}


def test_h5_fewer_links_for_the_same_logic_and_a_widening_gap_are_both_needed():
    # restated 24 November 2026 (PLAN.md 9 row 89): shaped as H4, both terms below 1
    lo = {"irr": 0.6, "irr_lower": 0.4, "irr_upper": 0.9, "p_less": 0.001}
    flat = {"irr": 1.0, "irr_lower": 0.8, "irr_upper": 1.2, "p_less": 0.5}
    hi = {"irr": 1.6, "irr_lower": 1.2, "irr_upper": 2.1, "p_less": 0.999}

    def v(**h5):
        return verdict.decide(estimates(H5=h5), COND)["hypotheses"]["H5"]
    assert v(arm=lo, trend=lo)["verdict"] == "supported"
    assert v(arm=lo, trend=flat)["verdict"] == "not supported"     # fewer, but the gap does not widen
    assert v(arm=lo, trend=flat)["p"] == 0.5
    assert v(arm=hi, trend=lo)["verdict"] == "reversed"
    assert v(arm={"error": "no links"}, trend=lo)["verdict"] == "not estimable"
    assert v(not_applicable=True)["verdict"] == "not testable"     # a history


def test_h5_rows_join_the_links_to_the_logic_added():
    links = [{"chain_id": "s/r/c1", "arm": "spring", "cp": "2", "links_added": "5", "call_links_added": "3",
              "state_links_added": "2", "flow_links_added": "0", "call_links": "10", "state_links": "4",
              "flow_links": "0", "methods": "7", "call_links_added_from_functions": "1",
              "call_links_added_from_methods": "2"},
             {"chain_id": "s/r/c1", "arm": "spring", "cp": "3", "links_added": "1"}]     # no logic read
    split = [{"chain_id": "s/r/c1", "cp": 2, "logic_added": 9}]
    rows = prepare.h5_rows(links, split)
    assert len(rows) == 1 and (rows[0]["links_added"], rows[0]["logic_added"], rows[0]["methods"]) == (5, 9, 7)
    s = prepare.links_summary(rows, 3)["spring"]
    assert s["links_per_logic"] == 5 / 9 and s["tree_links_per_method"] == 2.0


def test_calls_across_rows_count_the_calls_a_class_gained_and_those_reaching_opened_members():
    rows = prepare.calls_across_rows([{"chain_id": "s/r/c1", "arm": "spring", "cp": 2, "class": "A", "forced": "True",
                                       "chosen": "False", "new_out": 3, "new_in": 1, "out_exposed": 1, "in_widened": 1}])
    assert (rows[0]["coupled"], rows[0]["opened"], rows[0]["forced"]) == (4, 2, True)


def test_forced_coupling_is_sorted_into_contained_the_problem_reuse_and_other():
    # row 88: a call joining two classes whose private data the change needed is the problem's own;
    # one reaching a member already open is reuse; one reaching a member the change opened, the rest
    def row(cp, c, forced, coupled):
        return {"chain_id": "s/r/c1", "arm": "spring", "unit": cp, "class": c, "forced": forced, "coupled": coupled}

    def edge(cp, a, b, kind, fa, fb):
        return {"chain_id": "s/r/c1", "arm": "spring", "cp": cp, "caller_class": a, "callee_class": b,
                "kind": kind, "caller_forced": str(fa), "callee_forced": str(fb)}
    h5 = [row(2, "Owner", True, 1), row(2, "Pet", True, 1), row(3, "Vet", True, 0),
          row(4, "Visit", True, 2), row(4, "Util", False, 1)]
    edges = [edge(2, "Owner", "Pet", "exposed", True, True),       # problem, though Pet's member is new
             edge(4, "Visit", "Clinic", "existing", True, False),  # reuse
             edge(4, "Visit", "Util", "exposed", True, False)]     # other
    s = prepare.coupling_source(h5, edges)["spring"]
    assert (s["rows"], s["contained"], s["explained"], s["other"]) == (4, 1, 2, 1)
    assert s["calls"]["forced"] == {"problem": 1, "reuse": 1, "other": 1}


def h7(forced):
    return {"H7": {"margin": [0.8, 1.25], "forced": forced}}


def test_h7_spread_not_above_the_margin_is_supported():
    # restated 21 November 2026: spread does not see the force (one-sided below 1.25, as H6)
    flat = {"irr": 0.85, "irr_lower": 0.68, "irr_upper": 1.07, "p_upper": 0.004}
    v = verdict.decide(estimates(**h7(flat)), COND)["hypotheses"]["H7"]
    assert (v["state"], v["verdict"], v["tier"]) == ("not above", "supported", "secondary")
    wide = {"irr": 1.03, "irr_lower": 0.45, "irr_upper": 2.4, "p_upper": 0.3}
    assert verdict.decide(estimates(**h7(wide)), COND)["hypotheses"]["H7"]["verdict"] == "unresolved"
    up = {"irr": 1.8, "irr_lower": 1.3, "irr_upper": 2.4, "p_upper": 0.99}
    v = verdict.decide(estimates(**h7(up)), COND)["hypotheses"]["H7"]
    assert (v["state"], v["verdict"]) == ("against", "not supported")
    v = verdict.decide(estimates(**h7({"error": "every change in one class"})), COND)["hypotheses"]
    assert v["H7"]["verdict"] == "not estimable" and v["H2"]["verdict"] == "supported"


def test_h7_units_count_existing_classes_and_the_accountings_add_up():
    def host(cp, t, choice=None, added=3, new=False):
        return {"chain_id": "spring/r/chain1", "arm": "spring", "cp": cp, "type": t, "before_type": t,
                "added": added, "net_added": added, "replacement": False, "class_new": new,
                "choice_class": "" if choice is None else choice,
                "forced_enc": "" if choice is None else choice == 0}
    hosts = [host(1, "A"), host(2, "A", 0), host(2, "B", 2), host(2, "B"), host(3, "A", 1),
             host(3, "C", new=True), host(3, "D", added=0), host(4, "E", new=True)]
    u = {r["cp"]: r for r in prepare.h7_rows(hosts, {})}
    assert set(u) == {1, 2, 3}                      # cp 4 changed only a new class: a free choice
    assert (u[1]["classes"], u[1]["spread"], u[1]["forced"], u[1]["chosen"]) == (1, 0, False, False)
    assert (u[2]["classes"], u[2]["forced"], u[2]["forced_classes"], u[2]["chosen"]) == (2, True, 1, True)
    assert (u[3]["classes"], u[3]["all_classes"], u[3]["new_classes"], u[3]["class_names"]) == (1, 2, 1, "A")
    # growth of existing classes: forced 3 (A at cp 2), chosen 3 + 3, unbound 3 + 3; new classes left out
    g = prepare.growth_accounting(hosts, 4)["spring"]["positions"]
    assert (g["forced"], g["chosen"], g["unbound"], g["total"]) == (3, 6, 6, 15)
    assert abs(g["forced_share"] - 0.2) < 1e-9
    raw = [{"chain_id": "spring/r/chain1", "arm": "spring", "cp": cp, "class_a": "A", "class_b": "B",
            "calls_ab": ab, "calls_ba": 0, "calls_ab_after": after, "calls_ba_after": 0 if after is not None else None,
            "in_tree": "True", "new": 0} for cp, ab, after in ((2, 1, 2), (3, 2, 4), (9, 5, None))]
    raw.append({"chain_id": "spring/r/chain1", "arm": "spring", "cp": 3, "class_a": "A", "class_b": "C",
                "calls_ab": 0, "calls_ba": 0, "calls_ab_after": 1, "calls_ba_after": 0, "in_tree": "False", "new": 1})
    p = prepare.pair_rows(raw)
    assert [(r["times"], r["added"]) for r in p] == [(1, 1), (2, 2), (3, None)]   # the pair with a new class left out
    cc = prepare.co_change(p)["spring"]
    assert (cc["pairs"], cc["again"], cc["rose"], cc["fell"]) == (1, 1, 1, 0)
    assert cc["candidates"][0] == {"chain_id": "spring/r/chain1", "classes": ["A", "B"], "times": 3,
                                   "coupling_first": 1, "coupling_last": 5}
    coupling = [{"chain_id": "spring/r/chain1", "arm": "spring", "cp": cp, "cross_class_calls": b,
                 "cross_class_calls_after": a} for cp, b, a in ((1, 0, 1), (2, 1, 4), (3, 4, 10), (4, 10, ""))]
    ca = prepare.coupling_accounting(p, coupling, list(u.values()))["spring"]
    assert (ca["added"], ca["units"], ca["added_forced_units"], ca["added_unforced_units"]) == (10, 3, 3, 7)
    assert (ca["pairs_added"], ca["pairs_added_forced"], ca["pairs_added_unforced"]) == (3, 1, 2)
    assert abs(ca["share_between_pairs"] - 0.3) < 1e-9


def test_redesign_flags_a_class_whose_forced_changes_share_no_data_and_a_pair_changing_over_the_same_data():
    def host(cp, t, vals, forced=True, chain="s/r/c1"):
        return {"chain_id": chain, "arm": "spring", "cp": cp, "type": t, "before_type": t, "added": 3,
                "replacement": False, "class_new": False, "choice_class": 0 if forced else "",
                "forced_enc": True if forced else "",
                "need_class_values": vals, "called_class_methods": ""}
    # Shop: changes 1, 3 use {stock, price}; 2, 4 use {owner}: two groups by cp 4. Cart: one group
    hosts = [host(1, "Shop", "stock"), host(2, "Shop", "owner"), host(3, "Shop", "stock price"),
             host(4, "Shop", "owner"), host(1, "Cart", "items"), host(5, "Cart", "items total"),
             host(2, "Bill", "sum"), host(3, "Bill", "sum"), host(4, "Bill", "sum")]
    pairs = [{"chain_id": "s/r/c1", "arm": "spring", "unit": u, "pair": "s/r/c1|Bill|Shop", "coupling": c,
              "added": 1, "in_tree": True} for u, c in ((2, 1), (3, 2), (4, 3))]
    r = prepare.redesign(hosts, pairs)["spring"]
    sp = r["split"]
    assert (sp["classes"], sp["flagged"]) == (3, 1)
    c = sp["candidates"][0]
    assert (c["class"], c["at"], c["groups"]) == ("Shop", 4, [["price", "stock"], ["owner"]])
    co = r["concentrate"]
    assert (co["pairs"], co["together"], co["flagged"]) == (1, 1, 1)
    assert co["candidates"][0]["same_data"] == 1.0


def test_refactoring_rows_keep_splits_and_moves_between_classes():
    from placement_gravity import tables
    measured = {"refactorings": [{"unit": "cp03", "refactorings": [
        {"type": "Extract Class", "description": "Extract Class a.b.Owners from class a.b.Shop"},
        {"type": "Move Method", "description": "Move Method public pay() : void from class a.Bill to class a.Shop"},
        {"type": "Rename Method", "description": "Rename Method x() renamed to y() in class a.Shop"}]}]}
    rows = tables.refactoring_rows("spring", "chain1", measured)
    assert [(r["cp"], r["kind"], r["from_class"], r["to_class"]) for r in rows] == [
        (3, "Extract Class", "a.b.Shop", "a.b.Owners"), (3, "Move Method", "a.Bill", "a.Shop")]


def test_ripple_counts_later_changes_to_a_reached_method_that_also_change_the_caller():
    def host(cp, t, sig):
        return {"chain_id": "s/r/c1", "arm": "spring", "cp": cp, "type": t, "before_type": t,
                "before_signature": sig, "added": 2, "replacement": False}
    edges = [{"chain_id": "s/r/c1", "arm": "spring", "cp": 2, "caller_class": "Owner", "caller_signature": "add()",
              "callee_class": "Pet", "callee_signature": "age()", "kind": "widened",
              "caller_forced": "True", "callee_forced": "False"},
             {"chain_id": "s/r/c1", "arm": "spring", "cp": 2, "caller_class": "Vet", "caller_signature": "see()",
              "callee_class": "Owner", "callee_signature": "find()", "kind": "existing",
              "caller_forced": "False", "callee_forced": "False"}]
    hosts = [host(3, "Pet", "age()"), host(3, "Owner", "add()"), host(5, "Pet", "age()"), host(1, "Pet", "age()"),
             host(4, "Owner", "find()")]
    r = prepare.ripple(hosts, edges)["spring"]
    fo = r["forced_opened"]
    assert (fo["calls"], fo["later_changes"], fo["rippled"], fo["ripple_rate"]) == (1, 2, 1, 0.5)
    # Owner changes in 2 of the chain's 4 units: by chance a half of the later changes would ripple
    assert (fo["chance_rate"], fo["ripple_ratio"]) == (0.5, 1.0)
    assert (r["unforced_existing"]["later_changes"], r["unforced_existing"]["rippled"]) == (1, 0)


# ---------------------------------------------------------------- encapsulation and the reader (4.2f)

def test_java_tokens_drop_comments_and_count_a_string_as_one():
    from placement_gravity.chain import java_tokens
    src = ('class A { // c\n  /* x */ private int x = 10; String s = "a // b"; '
           'void f(){ x+=1; s=s+"\\""; char c = \'q\'; } }')
    assert java_tokens(src) == 36
    assert java_tokens('/* only */ // a comment\n') == 0
    assert java_tokens('String t = """\nline // not a comment\n""";') == 5


def _index(classes: dict, tokens: int) -> dict:
    """A tree index: ``classes`` is {class: ({field: access}, [(signature, access)])}."""
    return {"files": {f"{c}.java": {"tokens": tokens // len(classes),
                                    "classes": [{"name": c, "fields": fs}],
                                    "methods": [{"type": c, "name": s.split("(")[0], "signature": s,
                                                 "access": a, "calls": [], "reads": []} for s, a in ms]}
                      for c, (fs, ms) in classes.items()}, "flows": []}


def test_member_rows_count_introduced_members_their_privacy_and_the_system_size():
    before = _index({"A": ({"x": "private"}, [("f()", "public")])}, 1000)
    after = _index({"A": ({"x": "private", "y": "private", "z": "public"}, [("f()", "public"), ("g()", "private")]),
                    "B": ({}, [("h()", "public")])}, 1200)
    rows = tables.member_rows("history", "r", {"places": {"cp01": before, "cp02": after}})
    first, last = rows
    assert (first["cp"], first["system_tokens"], first["system_classes"], first["system_methods"]) == (1, 1000, 1, 1)
    assert (first["introduced"], first["introduced_private"]) == (4, 2)      # #y, #z, g(), h()
    assert (first["introduced_fields"], first["introduced_private_fields"]) == (2, 1)
    assert last["introduced"] is None and last["system_tokens"] == 1200      # no tree after the last unit


def test_reader_rows_join_size_forcing_splits_and_tokens_per_unit_and_class():
    members = [{"chain_id": "agent/r", "arm": "agent", "cp": "1", "position": "0.0", "system_tokens": "250000",
                "introduced": "4", "introduced_private": "1"}]
    hosts = [{"chain_id": "agent/r", "arm": "agent", "cp": "1", "type": "A", "added": "6", "net_added": "6", "class_new": "False",
              "runs": "1", "edits": "0", "binding_field": "1", "binding_class": "1", "forced_enc": "True"},
             {"chain_id": "agent/r", "arm": "agent", "cp": "1", "type": "N", "added": "4", "net_added": "4", "class_new": "True",
              "runs": "1", "edits": "0"}]
    h5 = [{"chain_id": "agent/r", "arm": "agent", "unit": 1, "cp": 0.0, "class": "A", "members_opened": 2,
           "forced": True, "positions": 6, "methods": 1}]
    boundary = [{"chain_id": "agent/r", "cp": "1", "class": "A", "methods_before": "14"}]
    refs = [{"chain_id": "agent/r", "cp": "1", "kind": "Extract Class"}]
    units, classes = prepare.reader_rows(members, hosts, h5, boundary, refs)
    u = units[0]
    assert (u["band"], u["introduced"], u["private"], u["splits"], u["positions"]) == ("200k to 1M", 4, 1, 1, 10)
    assert u["existing_positions"] == 6
    assert (classes[0]["opened"], classes[0]["methods_before"], classes[0]["band"]) == (2, 14, "200k to 1M")
    s = prepare.reader_summary(units, classes)["agent"]
    assert s["all"]["private_share"] == 0.25 and s["200k to 1M"]["too_thin"] is True
    assert "below 200k" not in s


def test_the_reader_section_reports_bands_and_models():
    rd = {"reader": {"agent": {"all": {"units": 30, "repositories": 12, "too_thin": False, "private_share": 0.4,
                                       "introduced": 50, "forced_share": 0.7, "class_rows": 20,
                                       "opened_per_row": 0.5, "class_methods_mean": 12.0,
                                       "class_methods_median": 10, "splits_per_unit": 0.0, "tokens_median": 3e5}}}}
    rep = {"reader": {"centre_tokens": 2.4e5, "private": {"author": {"irr": 0.5, "irr_lower": 0.3, "irr_upper": 0.8},
                                                          "interaction": {"irr": 1.3, "irr_lower": 1.1, "irr_upper": 1.5},
                                                          "size": {"irr": 1.0, "irr_lower": 0.9, "irr_upper": 1.1},
                                                          "n": 600, "repositories": 40},
                      "opened": {"error": "too few rows: opened"}}}
    text = "\n".join(report.reader_section(rep, rd))
    assert "encapsulation and the reader" in text and "private share 0.400 of 50 introduced" in text
    assert "author 0.500 [0.300, 0.800]" in text and "not fitted (too few rows: opened)" in text


def test_a_history_is_bootstrapped_with_fewer_refits_than_a_paired_run():
    # corpora B and C are read for direction and interval only, and their models are far larger
    assert prepare.BOOT_HISTORY == 200 and prepare.BOOT == 1000


def test_h1_forced_rows_count_every_checkpoint_that_did_something():
    h1 = [{"chain_id": "c", "level": "class", "forced": True, "cp": 2},
          {"chain_id": "c", "level": "class", "forced": True, "cp": 2},
          {"chain_id": "c", "level": "method", "forced": True, "cp": 2},
          {"chain_id": "c", "level": "class", "forced": False, "cp": 3}]
    adds = [{"chain_id": "c", "arm": "spring", "cp": str(k), "noop": str(k == 4)} for k in (1, 2, 3, 4)]
    assert [(r["cp"], r["forced_class"]) for r in prepare.h1_forced_rows(h1, adds)] == [(1, 0), (2, 2), (3, 0)]


def test_the_growth_exponent_tells_pebbles_from_a_filled_ball():
    # pebbles: blocks grow with volume (exponent 1); a ball: blocks stay, volume swells (exponent 0)
    def rows(arm, blocks_of):
        return [{"arm": arm, "kind": "class", "chain_id": arm, "container": f"C{k}", "cp": str(cp),
                 "concentration": "True", "volume": str(v), "blocks": str(blocks_of(v)), "largest_share": "0.5",
                 "internal_links": "2"} for k in range(3) for cp, v in enumerate((10 * (k + 1), 20 * (k + 1), 40 * (k + 1)), 1)]
    s = prepare.container_summary(rows("spring", lambda v: v // 10) + rows("officefloor", lambda v: 4), 3, resamples=50)
    assert abs(s["spring"]["class"]["concentrations"]["growth_exponent"] - 1) < 1e-9
    assert abs(s["officefloor"]["class"]["concentrations"]["growth_exponent"]) < 1e-9
    assert s["spring"]["class"]["rest"]["containers_at_end"] == 0


def test_the_sinew_shape_counts_values_combinations_and_their_effective_number():
    from placement_gravity import readings
    def host(cp, vals):
        return {"arm": "spring", "chain_id": "c", "cp": cp, "type": "OwnerService", "name": "add",
                "binding": 1, "net_added": 3, "replacement": "False", "need_class_values": vals,
                "need_method_values": ""}
    hs = [host(k, "owners clock") for k in range(1, 8)] + [host(k, "owners") for k in range(8, 24)] \
        + [host(24, "clock dailyLimit"), host(25, "clock")]
    s = readings.sinew_shape(hs)["spring"]["class"]
    # owners 23, clock 9, dailyLimit 1: about 1.8 values carry the place
    assert s["top_values"][0] == {"place": "OwnerService", "chain_id": "c", "value": "owners", "uses": 23}
    assert abs(s["effective_number"] - readings.effective_number([23, 9, 1])) < 1e-9
    assert readings.effective_number([10]) == 1 and readings.effective_number([5, 5, 5, 5]) == 4
    assert s["top_combinations"][0]["values"] == ["owners"] and s["top_combinations"][0]["uses"] == 16
    assert s["repeated_combination_share"] == 21 / 25


def test_the_growth_exponent_interval_does_not_depend_on_the_order_of_the_rows():
    import random as _r
    rows = [{"arm": "spring", "kind": "class", "chain_id": "c", "container": f"C{k}", "cp": str(cp),
             "concentration": "True", "volume": str(v * (k + 1)), "blocks": str(max(1, (v * (k + 1)) // (7 + k))),
             "largest_share": "0.5", "internal_links": "1"}
            for k in range(6) for cp, v in enumerate((10, 20, 35, 60), 1)]
    a = prepare.container_summary(rows, 4, resamples=200)
    _r.Random(3).shuffle(rows)
    assert prepare.container_summary(rows, 4, resamples=200) == a

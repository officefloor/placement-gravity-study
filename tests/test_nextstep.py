"""The steps in one order, what each reads when nothing is named, and the next command each
prints (README, *Running*; PLAN.md 9 row 125)."""

import os
from pathlib import Path

import pytest

from placement_gravity import nextstep, report, runs

ROOT = Path(__file__).parent.parent


def test_every_step_has_its_script_and_they_sort_in_order():
    names = sorted(p.name for p in ROOT.glob("step*.sh"))
    assert ["./" + n for n in names] == [nextstep.SCRIPT[k] for k in sorted(nextstep.SCRIPT)]
    assert all(os.access(ROOT / n, os.X_OK) for n in names + ["run_stage.sh"])


def test_with_nothing_named_the_steps_follow_one_another():
    reg = runs.load()
    first = lambda step: nextstep.commands(step, reg)[-1].split()[0]
    order = ["01", "03", "04", "05", "06", "07", "08", "09"]
    assert [first(a) for a in order[:-1]] == [nextstep.SCRIPT[b] for b in order[1:]]
    assert nextstep.commands("01", reg)[0].startswith("./step02_timing.sh")      # optional
    assert nextstep.commands("02", reg) == ["./step03_pin_chains.sh"]
    # the runs still being made come last, each when it is complete; then the last summary
    after_b = [c.split()[0] for c in nextstep.commands("09", reg)]
    assert after_b == ["./step10_run_c.sh", "./step11_run_d.sh", "./step12_summary.sh"]
    assert nextstep.commands("11", reg)[-1].startswith("./step12_summary.sh")
    assert nextstep.commands("12", reg) == []
    # a step number given as one digit is understood
    assert nextstep.commands("4", reg) == ["./step05_chain_results.sh"]


def test_named_analyses_are_carried_on_and_steps_they_do_not_need_passed_over():
    reg = runs.load()
    c = lambda step, **k: nextstep.commands(step, reg, **k)
    assert c("03", analyses=["pilot"]) == ["./step04_measure_chains.sh --analysis pilot"]
    assert c("04", analyses=["pilot"]) == ["./step05_chain_results.sh --analysis pilot"]
    assert c("05", analyses=["pilot"]) == []                                            # no history named
    assert c("05", analyses=["pilot", "open-source-development"])[0].startswith(
        "./step06_samples.sh open-source-development open-source-development-agent")
    assert c("06", samples=["open-source-agent"]) == [
        "./step07_measure_histories.sh --analysis open-source-agent-within open-source-agent-against-human"]
    assert c("07", analyses=["open-source-development"]) == [
        "./step08_history_results.sh --analysis open-source-development"]


def test_each_results_step_says_which_lab_note_can_be_written_and_from_what():
    reg = runs.load()
    every = {a["name"] for a in reg["analyses"]}
    petclinic = {n for n in every if n.startswith("petclinic-")} | {"pilot"}
    # after the petclinic results: lab note 1, the eight replications, and what is not in yet
    text = "\n".join(nextstep.note("05", reg, True, petclinic))
    assert text.startswith("Lab Note 1 can now be written: the petclinic replications")
    assert "results/analysis/REPORT.md" in text and "<analysis>/REPORT.md" in text
    added = next(l for l in text.splitlines() if "Added by this step" in l)
    assert added.count("petclinic-") == 8 and "pilot" not in added           # development data is no result
    assert "open-source-human" in text and "Run B (step09_run_b.sh): not analysed yet" in text
    assert "The study's test is ui-primary (step 09)" in text
    # the five notes in order, one a results step
    notes = [nextstep.note(s, reg, True, every)[0] for s in ("05", "08", "09", "10", "11")]
    assert [n.split(" can")[0] for n in notes] == [f"Lab Note {i}" for i in range(1, 6)]
    assert "Added by this step: ui-primary, ui-angular, ui-tanstack" in "\n".join(nextstep.note("09", reg, True, every))
    assert nextstep.note("12", reg, True, every)[0].startswith("The write-up can now be made")
    # a step that is not a results step has no note; before the tag there is nothing to write up
    assert nextstep.note("04", reg, True, every) == []
    before = nextstep.note("05", reg, False, {"pilot"})
    assert before[0].startswith("Before the tag plan-v1") and "nothing but development data" in "\n".join(before)


def test_what_each_step_reads_when_nothing_is_named():
    reg = runs.load()
    # before the tag only the development analyses can be read
    assert nextstep.default(reg, "chains", registered=False) == ["pilot"]
    assert nextstep.default(reg, "histories", registered=False) == ["open-source-development"]
    # after it, everything that exists at registration, and no ui run
    chains = nextstep.default(reg, "chains", registered=True)
    assert "pilot" in chains and sum(n.startswith("petclinic-") for n in chains) == 8
    assert not any(n.startswith("ui-") for n in chains)
    assert "open-source-human" in nextstep.default(reg, "histories", registered=True)
    assert "open-source-agent" in nextstep.default(reg, "samples", registered=True)
    # each run still being made is read by its own step; one the registry does not name yet is none
    assert nextstep.default(reg, "run-b", True) == ["ui-primary", "ui-angular", "ui-tanstack"]
    assert nextstep.default(reg, "run-c", True) == [] and nextstep.default(reg, "run-d", True) == []


def test_every_analysis_has_a_stage_the_steps_know():
    reg = runs.load()
    assert {runs.stage(a) for a in reg["analyses"]} <= set(runs.STAGES)
    bad = {**reg, "analyses": [{**reg["analyses"][0], "stage": "run-z"}]}
    with pytest.raises(ValueError, match="unknown stage"):
        runs.validate(bad)


def test_the_summary_says_what_is_still_to_come():
    reg = runs.load()
    lines = "\n".join(report.waiting_lines(reg, {"pilot"}))
    assert "**Run B** (step09_run_b.sh): not analysed yet: ui-primary, ui-angular, ui-tanstack" in lines
    assert "**Run C** (step10_run_c.sh): not in `runs.yaml` yet" in lines
    assert "**Run D** (step11_run_d.sh): not in `runs.yaml` yet" in lines
    # with everything analysed, only the runs the registry does not name are left
    left = report.waiting_lines(reg, {a["name"] for a in reg["analyses"]})
    assert len(left) == 2
    assert report.summary_cell({"verdict": "supported", "p": 0.04, "p_holm": 0.012}) == "supported (p 0.012)"
    assert report.summary_cell({"verdict": "not estimable", "p": None}) == "not estimable"


def test_the_summary_gives_each_hypothesis_its_main_figure():
    hy = {"H1": {"detail": {"contrast": {"arm": {"irr": 0.25, "irr_lower": 0.09, "irr_upper": 0.65}}}},
          "H3": {"detail": {"cp": {"estimate": 0.02, "lower": 0.01, "upper": 0.03}}},
          "H4": {"detail": {"model": {"intrusion_class": {"error": "not fitted"}}}},
          "H6": {"detail": {"measures": {"a": {"irr": 0.9, "irr_lower": 0.7, "irr_upper": 1.1},
                                         "b": {"irr": 1.3, "irr_lower": 1.1, "irr_upper": 1.5},
                                         "c": {"error": "no variation"}}}}}
    cell = lambda col: next(report.main_cell(hy, h, path) for name, h, path, _ in report.MAIN if name == col)
    assert cell("H1 forced") == "0.250 [0.090, 0.650]"
    assert cell("H3 rise") == "0.020 [0.010, 0.030]"            # a slope, not a ratio
    assert cell("H4 come back to") == "–"                        # could not be fitted
    assert cell("H6 shape") == "1.300 [1.100, 1.500] (b)"        # the measure nearest the margin
    assert cell("H2 core") == "–" and cell("H8 open") == "–"     # the analysis does not give it
    assert [m[1] for m in report.MAIN] == ["H1", "H2", "H2", "H3", "H4", "H4", "H5", "H6", "H7", "H8"]

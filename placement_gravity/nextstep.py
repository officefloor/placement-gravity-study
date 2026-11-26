"""The order of the steps, the analyses each reads when none is named, the command to run after
each, and the lab note each results step makes possible: every step script ends by printing them,
so that the steps can be run one after another without looking anything up (README, *Running*;
PLAN.md 9 row 125).

    python -m placement_gravity.nextstep STEP [--analysis NAME ...] [--samples NAME ...]
    python -m placement_gravity.nextstep names chains|histories|samples|run-b|run-c|run-d

One order, 01 to 12. Steps 03 to 08 read what exists when the plan is registered (``runs.stage``
``first``): the petclinic chains (03 pin, 04 measure, 05 results), then the histories (06 samples,
07 measure, 08 results). Steps 09, 10 and 11 each read one run that was still being made at
registration (Run B, Run C, Run D), from pinning its chains to its results, and refuse until that
run is complete; step 12 is the last summary. A results step analyses, writes every report and
the summary (results/analysis/REPORT.md) again, and says which lab note can now be written
(``NOTES``). Options a step takes that do not carry over (``--force``, ``--workers``) are ignored.

Until 27 November 2026 the steps were numbered 1, 1b, 2, 2b, 3, 3b, 4, 5; the plan's text of before
that day uses those numbers (``RENUMBERED``).
"""

from __future__ import annotations

import argparse

from . import runs

#: The steps as they were numbered until 27 November 2026, and what each is now. The analysis (4)
#: and the report (5) are now done together by each results step: 05, 08, 09, 10, 11.
RENUMBERED = {"1": "01", "1b": "02", "2": "03", "3": "04", "2b": "06", "3b": "07",
              "4": "05, 08", "5": "05, 08, 12"}

SCRIPT = {"01": "./step01_setup.sh", "02": "./step02_timing.sh", "03": "./step03_pin_chains.sh",
          "04": "./step04_measure_chains.sh", "05": "./step05_chain_results.sh",
          "06": "./step06_samples.sh", "07": "./step07_measure_histories.sh",
          "08": "./step08_history_results.sh",
          "09": "./step09_run_b.sh", "10": "./step10_run_c.sh", "11": "./step11_run_d.sh",
          "12": "./step12_summary.sh"}

#: The progress points: the results step, the lab note it makes possible, what the note is about,
#: and what selects the analyses it adds to the summary.
NOTES = {"05": (1, "the petclinic replications: Spring against OfficeFloor, every rule on one endpoint",
                "chains"),
         "08": (2, "the open-source histories: code people wrote, and code agents are declared to have written",
                "histories"),
         "09": (3, "Run B: the study's test (ui-primary) and the two pairs that share a front end", "run-b"),
         "10": (4, "Run C: the no-injection control", "run-c"),
         "11": (5, "Run D: the same stack with nothing private (H8)", "run-d")}

RUN = {"run-b": "Run B", "run-c": "Run C", "run-d": "Run D"}


def split(reg: dict, names: list[str] | None) -> tuple[list[str], list[str]]:
    """The named analyses (every one where none is named), as (paired chains, histories)."""
    xs = [a for a in reg["analyses"] if not names or a["name"] in names]
    return ([a["name"] for a in xs if not a.get("history")],
            [a["name"] for a in xs if a.get("history")])


def samples_of(reg: dict, histories: list[str]) -> list[str]:
    """The samples the named history analyses read, in the order of runs.yaml."""
    out: list[str] = []
    for a in reg["analyses"]:
        if a["name"] in histories:
            for s in a["sources"]:
                if s["sample"] not in out:
                    out.append(s["sample"])
    return out


def reading(reg: dict, samples: list[str]) -> list[str]:
    """The history analyses that read any of the samples."""
    return [a["name"] for a in reg["analyses"] if a.get("history")
            and any(s["sample"] in samples for s in a["sources"])]


def default(reg: dict, what: str, registered: bool) -> list[str]:
    """What a step reads when nothing is named. ``chains`` and ``histories``: the analyses of the
    first stage (before the tag only the development ones, since ``runs.guard`` refuses the rest);
    ``samples``: the samples those histories read; ``run-b``, ``run-c``, ``run-d``: that run's
    analyses, none where the registry does not name the run yet."""
    if what in RUN:
        return [a["name"] for a in reg["analyses"] if runs.stage(a) == what]
    first = [a for a in reg["analyses"] if runs.stage(a) == "first"
             and (registered or a["role"] == "development")]
    if what == "chains":
        return [a["name"] for a in first if not a.get("history")]
    histories = [a["name"] for a in first if a.get("history")]
    if what == "histories":
        return histories
    if what == "samples":
        return samples_of(reg, histories)
    raise ValueError(what)


def _arg(names: list[str]) -> str:
    return " --analysis " + " ".join(names) if names else ""


def commands(step: str, reg: dict, analyses: list[str] | None = None,
             samples: list[str] | None = None) -> list[str]:
    """The next command after STEP, with a word on when it can be run where it waits on a run.
    With no analysis named the order is 01 to 12 and each step reads its own default. Where
    analyses were named they are carried on, and the steps they do not need are passed over."""
    step = step.zfill(2)
    named = bool(analyses)
    chains, histories = split(reg, analyses) if named else ([], [])
    if step == "01":
        return [SCRIPT["02"] + "   # optional, about 45 minutes: one model fit by data size (PLAN.md 5)",
                SCRIPT["03"]]
    if step == "02":
        return [SCRIPT["03"]]
    if step == "03":
        return [SCRIPT["04"] + _arg(chains)]
    if step == "04":
        return [SCRIPT["05"] + _arg(chains)]
    if step == "05":
        if named and not histories:
            return []
        return [SCRIPT["06"] + (" " + " ".join(samples_of(reg, histories)) if named else "")
                + "   # the histories (corpora B and C); needs the network and `gh auth login`"]
    if step == "06":
        return [SCRIPT["07"] + _arg(reading(reg, samples or []))]
    if step == "07":
        return [SCRIPT["08"] + _arg(histories)]
    if step == "08":
        return [SCRIPT["09"] + "   # when Run B is complete: every chain of the four ui stacks pushed and "
                "at its last checkpoint. It refuses until then, so it is safe to try."]
    if step == "09":
        return [SCRIPT["10"] + "   # when Run C is named in runs.yaml (a dated amendment, PLAN.md 3.1a) "
                "and complete",
                SCRIPT["11"] + "   # when Run D is named in runs.yaml and complete; 10 and 11 in either order",
                SCRIPT["12"] + "   # after both: the last summary"]
    if step == "10":
        return [SCRIPT["11"] + "   # when Run D is named in runs.yaml and complete (if not yet read)",
                SCRIPT["12"] + "   # after both: the last summary"]
    if step == "11":
        return [SCRIPT["10"] + "   # when Run C is named in runs.yaml and complete (if not yet read)",
                SCRIPT["12"] + "   # after both: the last summary"]
    if step == "12":
        return []
    raise ValueError(f"no step {step!r}")


def note(step: str, reg: dict, registered: bool, analysed: set[str]) -> list[str]:
    """What a results step leaves to write up: the lab note it makes possible, the analyses it added
    to the summary (those of its stage that have been analysed), where their figures are, and what
    the summary does not hold yet. ``analysed``: the analyses with verdicts on disk. Before the tag
    only the development data can have been read, which is not a result."""
    from . import report
    step = step.zfill(2)
    out_dir = "results/analysis"
    if step == "12":
        head = ["The write-up can now be made: the last summary holds every analysis that has been read."]
        new = [a["name"] for a in reg["analyses"] if a["name"] in analysed]
    elif step in NOTES:
        n, about, what = NOTES[step]
        new = [x for x in default(reg, what, registered) if x in analysed]
        head = [f"Lab Note {n} can now be written: {about}."]
    else:
        return []
    if not registered:
        head = ["Before the tag plan-v1: only the development data has been read. It shows the steps "
                "work; it is not a result and not for a lab note."]
    results = [x for x in new if next(a for a in reg["analyses"] if a["name"] == x)["role"] != "development"]
    lines = head + [
        f"  Summary:  {out_dir}/REPORT.md   (each analysis read so far: every hypothesis's verdict with "
        f"its p, and its main ratio with its interval)"]
    if step != "12":
        lines.append("  Added by this step: " + (", ".join(results) if results else "nothing but development data"))
    lines += [f"  Details:  {out_dir}/<analysis>/REPORT.md       (every figure of the plan's tests and readings)",
              f"            {out_dir}/<analysis>/DIAGNOSTICS.md  (the other figures the plan quotes)"]
    waiting = report.waiting_lines(reg, analysed)
    if waiting:
        lines.append("  Not yet in the summary:")
        lines += ["    " + w.lstrip("- ").replace("**", "") for w in waiting]
    if step in ("05", "08") and registered:
        lines.append("  These are replications and outside evidence. The study's test is ui-primary (step 09); "
                     "nothing here changes a run still being made (PLAN.md 3.1a).")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("step")
    ap.add_argument("what", nargs="?")
    ap.add_argument("--analysis", nargs="*")
    ap.add_argument("--samples", nargs="*")
    a, _ = ap.parse_known_args()
    reg = runs.load()
    if a.step == "names":
        names = default(reg, a.what, runs.registered(reg["registration_tag"]))
        if not names and a.what in RUN:
            raise SystemExit(f"{RUN[a.what]} is not in runs.yaml yet. Its run ids and its analysis (stage: "
                             f"{a.what}) are added by a dated amendment (PLAN.md 3.1a, 9), committed, before "
                             f"any of its backend Java is read.")
        print(" ".join(names))
        return
    is_registered = runs.registered(reg["registration_tag"])
    analysed = {x["name"] for x in reg["analyses"]
                if (runs.RESULTS / "analysis" / x["name"] / "verdicts.json").exists()}
    notes = note(a.step, reg, is_registered, analysed)
    if notes:
        print()
        print("\n".join(notes))
    cmds = commands(a.step, reg, a.analysis, a.samples)
    print()
    if not cmds:
        print("Done: every step has run. The results are in results/analysis/REPORT.md."
              if a.step.zfill(2) == "12" else "Done for the analyses named.")
        return
    print("Next:")
    for c in cmds:
        print(f"  {c}")


if __name__ == "__main__":
    main()

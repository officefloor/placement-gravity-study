"""The command to run after each step: every step script ends by printing it, with the analyses it
was given, so that the steps can be run one after another without looking anything up (README,
*Running*).

    python -m placement_gravity.nextstep STEP [--analysis NAME ...] [--samples NAME ...]

The paired chains (corpus A) go step 2 -> 3 -> 4 -> 5; the histories (corpora B and C) go
step 2b (draw or fetch the sample) -> 3b -> 4 -> 5. Options a step takes that do not carry over
(``--force``, ``--workers``) are ignored.
"""

from __future__ import annotations

import argparse

from . import runs


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


def _arg(names: list[str]) -> str:
    return " --analysis " + " ".join(names) if names else ""


def commands(step: str, reg: dict, analyses: list[str] | None = None,
             samples: list[str] | None = None, registered: bool | None = None) -> list[str]:
    """The next command (or commands, where the paired chains and the histories part) after STEP."""
    if not analyses and registered is False:
        # before the tag only the development analyses can be read (runs.guard), so name them
        analyses = [a["name"] for a in reg["analyses"] if a["role"] == "development"]
    named = bool(analyses)
    chains, histories = split(reg, analyses)
    first = step == "1"
    if step == "1b":
        step = "1"
    if step == "1":
        out = ["./step1b_timing.sh   # optional, about 45 minutes: one model fit by data size (PLAN.md 5)"] if first else []
        out += ["./step2_runs.sh" + _arg(chains if named else [])] if chains else []
        if histories:
            out.append("./step2b_samples.sh " + " ".join(samples_of(reg, histories))
                       + "   # the histories (corpora B and C): each sample they read; needs `gh auth login`")
        return out
    if step == "2":
        out = ["./step3_measure.sh" + _arg(chains if named else [])] if chains else []
        if named and histories:
            out.append("./step2b_samples.sh " + " ".join(samples_of(reg, histories)))
        return out
    if step == "2b":
        return ["./step3b_histories.sh" + _arg(reading(reg, samples or []))]
    if step == "3":
        out = ["./step3b_histories.sh" + _arg(histories)] if named and histories else []
        return out + ["./step4_analyse.sh" + _arg(chains + histories if named else [])]
    if step == "3b":
        return ["./step4_analyse.sh" + _arg(chains + histories if named else [])]
    if step == "4":
        return ["./step5_report.sh"]
    if step == "5":
        return []
    raise ValueError(f"no step {step!r}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["1", "1b", "2", "2b", "3", "3b", "4", "5"])
    ap.add_argument("--analysis", nargs="*")
    ap.add_argument("--samples", nargs="*")
    a, _ = ap.parse_known_args()
    reg = runs.load()
    cmds = commands(a.step, reg, a.analysis, a.samples, runs.registered(reg["registration_tag"]))
    print()
    if not cmds:
        print("Done: every step has run. The results are in results/analysis/REPORT.md.")
        return
    print("Next:")
    for c in cmds:
        print(f"  {c}")


if __name__ == "__main__":
    main()

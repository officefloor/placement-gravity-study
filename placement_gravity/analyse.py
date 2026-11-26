"""The analysis (steps 05 and 08, and each run's step): for each measured analysis, the datasets (prepare), the models (analysis/analyse.R, by
glmmTMB) and the verdicts (verdict).

    python -m placement_gravity.analyse [--analysis NAME ...]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time

from . import chain, prepare, readings, runs, verdict

R_SCRIPT = chain.ROOT / "analysis" / "analyse.R"
OUT = runs.RESULTS / "analysis"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", nargs="*")
    a = ap.parse_args()
    if not shutil.which("Rscript"):
        raise SystemExit("Rscript not found: R and glmmTMB are needed for the analysis (step01_setup.sh).")
    reg = runs.load()
    for analysis in reg["analyses"]:
        name = analysis["name"]
        if a.analysis and name not in a.analysis:
            continue
        if not runs.measured(analysis):
            continue
        runs.guard(reg, analysis)
        started = time.monotonic()
        data = prepare.prepare(analysis, runs.streamed(reg, analysis))
        est = OUT / name / "estimates.json"
        subprocess.run(["Rscript", str(R_SCRIPT), str(data), str(est)], check=True)
        out = verdict.decide(json.loads(est.read_text()),
                             json.loads((data / "conditions.json").read_text()))
        (OUT / name / "verdicts.json").write_text(json.dumps(out, indent=1) + "\n")
        # the review reading (PLAN.md 5): this analysis's reviewed chains against the just-solve
        # analysis it names, the one reading that sets two conditions side by side
        other = analysis.get("review_against")
        if other and (runs.RESULTS / "measure" / other).exists():
            r = json.loads((data / "readings.json").read_text())
            r["review"] = {"against": other, **readings.review(
                prepare.gather(other, "runs"), prepare.gather(other, "additions"),
                prepare.gather(name, "additions"))}
            (data / "readings.json").write_text(json.dumps(r, indent=1) + "\n")
        # how long the analysis took (diagnostics, PLAN.md 6), with the refits it ran
        spec = json.loads((data / "spec.json").read_text())
        (OUT / name / "timing.json").write_text(json.dumps(
            {"seconds": round(time.monotonic() - started, 1), "refits": spec.get("boot")}, indent=1) + "\n")
        print(name + ": " + "; ".join(f"{k} {v['verdict']}" for k, v in out["hypotheses"].items()))


if __name__ == "__main__":
    main()

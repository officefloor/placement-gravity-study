"""Step 4: for each measured analysis, the datasets (prepare), the models (analysis/analyse.R, by
glmmTMB) and the verdicts (verdict).

    python -m placement_gravity.analyse [--analysis NAME ...]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess

from . import chain, prepare, readings, runs, verdict

R_SCRIPT = chain.ROOT / "analysis" / "analyse.R"
OUT = runs.RESULTS / "analysis"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", nargs="*")
    a = ap.parse_args()
    if not shutil.which("Rscript"):
        raise SystemExit("Rscript not found: R and glmmTMB are needed for step 4 (step1_setup.sh).")
    reg = runs.load()
    for analysis in reg["analyses"]:
        name = analysis["name"]
        if a.analysis and name not in a.analysis:
            continue
        if not (runs.RESULTS / "measure" / name).exists():
            continue
        runs.guard(reg, analysis)
        data = prepare.prepare(analysis, runs.stream(reg, analysis["stream"]))
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
        print(name + ": " + "; ".join(f"{k} {v['verdict']}" for k, v in out["hypotheses"].items()))


if __name__ == "__main__":
    main()

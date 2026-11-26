#!/usr/bin/env bash
# Step 05: the results of the paired chains measured in step 04 (the petclinic replications). Per
# analysis, the datasets (data/analysis/<name>/), the models of PLAN.md §5 in R with glmmTMB
# (results/analysis/<name>/estimates.json) and the verdicts with the Holm correction (verdicts.json);
# then every report and the summary, results/analysis/REPORT.md. Lab Note 1 can then be written.
#   ./step05_chain_results.sh [--analysis NAME ...]
set -euo pipefail
cd "$(dirname "$0")"
given=("$@")
if [ $# -eq 0 ]; then set -- --analysis $(.venv/bin/python -m placement_gravity.nextstep names chains); fi
.venv/bin/python -m placement_gravity.analyse "$@"
.venv/bin/python -m placement_gravity.report
.venv/bin/python -m placement_gravity.diagnostics
.venv/bin/python -m placement_gravity.nextstep 05 "${given[@]}"

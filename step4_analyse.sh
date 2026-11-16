#!/usr/bin/env bash
# Step 4: per analysis, the datasets (data/analysis/<name>/), the models of PLAN.md §5 in R with glmmTMB
# (results/analysis/<name>/estimates.json) and the verdicts with the Holm correction (verdicts.json).
#   ./step4_analyse.sh [--analysis NAME ...]
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.analyse "$@"

#!/usr/bin/env bash
# Step 02 (optional, about 45 minutes): the time one fit of the study's models takes on this
# machine, on simulated data of 1,800 to 1,000,000 rows (analysis/timing.R) -> results/timing.json.
# PLAN.md 5 sets the histories' bootstrap refits from it. Give sizes to time only those:
#   ./step02_timing.sh [ROWS ...]
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
Rscript analysis/timing.R results/timing.json "$@"
.venv/bin/python -m placement_gravity.nextstep 02

#!/usr/bin/env bash
# Step 5: the report: results/analysis/<name>/REPORT.md per analysis, every hypothesis whichever way it
# fell, and results/analysis/REPORT.md listing them all; beside each, DIAGNOSTICS.md.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.report
# every figure the plan quotes that the report does not print (PLAN.md 9 row 112)
.venv/bin/python -m placement_gravity.diagnostics
.venv/bin/python -m placement_gravity.nextstep 5 "$@"

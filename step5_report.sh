#!/usr/bin/env bash
# Step 5: the report: results/analysis/<name>/REPORT.md per analysis, every hypothesis whichever way it
# fell, and results/analysis/REPORT.md listing them all.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.report

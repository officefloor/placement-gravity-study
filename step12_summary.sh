#!/usr/bin/env bash
# Step 12: the last summary, for the write-up: every report and results/analysis/REPORT.md made
# again from what has been analysed. It reads nothing new and can be run at any time.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.report
.venv/bin/python -m placement_gravity.diagnostics
.venv/bin/python -m placement_gravity.nextstep 12

#!/usr/bin/env bash
# Step 10: Run C, the no-injection control (PLAN.md 3.1a): read once its run ids and its analysis are in
# runs.yaml by a dated amendment and its chains are complete.
# Pins the chains, measures them, analyses them and writes the reports and the summary again.
# It refuses until then and reads nothing, so it is safe to try early.
# Lab Note 4 can then be written.
set -euo pipefail
cd "$(dirname "$0")"
./run_stage.sh run-c
.venv/bin/python -m placement_gravity.nextstep 10

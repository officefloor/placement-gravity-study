#!/usr/bin/env bash
# Step 11: Run D, the no-encapsulation run, against Run A's same stack (H8, PLAN.md 3.1a): read once its
# run ids and its analysis are in runs.yaml by a dated amendment and its chains are complete.
# Pins the chains, measures them, analyses them and writes the reports and the summary again.
# It refuses until then and reads nothing, so it is safe to try early.
# Lab Note 5 can then be written.
set -euo pipefail
cd "$(dirname "$0")"
./run_stage.sh run-d
.venv/bin/python -m placement_gravity.nextstep 11

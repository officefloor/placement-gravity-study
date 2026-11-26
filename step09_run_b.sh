#!/usr/bin/env bash
# Step 09: Run B: the ui runs' primary test (ui-primary) and the two pairs that share a front end
# (ui-angular, ui-tanstack), read once every chain of Runs A and B is pushed and at checkpoint 250.
# Pins the chains, measures them, analyses them and writes the reports and the summary again.
# It refuses until then and reads nothing, so it is safe to try early.
# Lab Note 3 can then be written.
set -euo pipefail
cd "$(dirname "$0")"
./run_stage.sh run-b
.venv/bin/python -m placement_gravity.nextstep 09

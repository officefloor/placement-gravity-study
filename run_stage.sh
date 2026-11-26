#!/usr/bin/env bash
# One run that was still being made when the plan was registered (steps 09, 10, 11): its analyses,
# as runs.yaml names them (stage: run-b | run-c | run-d), from pinning the chains to the report.
# Nothing of the run is read until every one of its chains is pushed and complete (PLAN.md 3.1a, 9
# row 114), and a run that is not in runs.yaml yet is refused: it is added by a dated amendment.
# Run it again after a failure: a chain already measured at the same commit is skipped.
#   ./run_stage.sh run-b|run-c|run-d
set -euo pipefail
cd "$(dirname "$0")"
names=$(.venv/bin/python -m placement_gravity.nextstep names "$1")
echo "$1: $names"
.venv/bin/python -m placement_gravity.runs stacks > /dev/null
.venv/bin/python -m placement_gravity.runs fetch --analysis $names
.venv/bin/python -m placement_gravity.measure --analysis $names
.venv/bin/python -m placement_gravity.analyse --analysis $names
.venv/bin/python -m placement_gravity.report
.venv/bin/python -m placement_gravity.diagnostics

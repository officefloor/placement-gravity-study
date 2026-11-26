#!/usr/bin/env bash
# Step 08: the results of the open-source histories measured in step 07 (corpora B and C): the
# datasets, the models and the verdicts per analysis, as step 05; then every report and the summary
# again, results/analysis/REPORT.md, now with the histories. Lab Note 2 can then be written.
#   ./step08_history_results.sh [--analysis NAME ...]
set -euo pipefail
cd "$(dirname "$0")"
given=("$@")
if [ $# -eq 0 ]; then set -- --analysis $(.venv/bin/python -m placement_gravity.nextstep names histories); fi
.venv/bin/python -m placement_gravity.analyse "$@"
.venv/bin/python -m placement_gravity.report
.venv/bin/python -m placement_gravity.diagnostics
.venv/bin/python -m placement_gravity.nextstep 08 "${given[@]}"

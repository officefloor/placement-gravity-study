#!/usr/bin/env bash
# Step 2: the runs named in runs.yaml, fetched and pinned. First each stack's declared source roots,
# read at its empty base (no run is read); then the chains of each analysis, whose heads are recorded
# in results/heads.tsv. Every analysis but the development one is refused until the tag plan-v1.
#   ./step2_runs.sh [--analysis NAME ...]
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.runs stacks
.venv/bin/python -m placement_gravity.runs fetch "$@"
.venv/bin/python -m placement_gravity.nextstep 2 "$@"

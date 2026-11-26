#!/usr/bin/env bash
# Step 03: the paired chains that exist today (the petclinic runs; before the tag plan-v1 only the
# development chain), fetched and pinned. First each stack's declared source roots, read at its
# empty base (no run is read); then the chains of each analysis, whose heads are recorded in
# results/heads.tsv. The ui runs are not read here: each has its own step (09, 10, 11).
#   ./step03_pin_chains.sh [--analysis NAME ...]
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.runs stacks
given=("$@")
if [ $# -eq 0 ]; then set -- --analysis $(.venv/bin/python -m placement_gravity.nextstep names chains); fi
.venv/bin/python -m placement_gravity.runs fetch "$@"
.venv/bin/python -m placement_gravity.nextstep 03 "${given[@]}"

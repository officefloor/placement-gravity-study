#!/usr/bin/env bash
# Step 04: the instrument over every chain step 03 pinned: the tables of PLAN.md §4, the shape series
# and CodeTracker's histories, per chain in results/measure/<analysis>/. A chain already measured at
# the same commit is skipped (--force redoes it).
#   ./step04_measure_chains.sh [--analysis NAME ...] [--force]
set -euo pipefail
cd "$(dirname "$0")"
given=("$@")
if [ $# -eq 0 ]; then set -- --analysis $(.venv/bin/python -m placement_gravity.nextstep names chains); fi
.venv/bin/python -m placement_gravity.measure "$@"
.venv/bin/python -m placement_gravity.nextstep 04 "${given[@]}"

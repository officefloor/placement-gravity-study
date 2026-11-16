#!/usr/bin/env bash
# Step 3: the instrument over every chain step 2 pinned: the tables of PLAN.md §4, the shape series
# and CodeTracker's histories, per chain in results/measure/<analysis>/. A chain already measured at
# the same commit is skipped (--force redoes it).
#   ./step3_measure.sh [--analysis NAME ...] [--force]
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.measure "$@"

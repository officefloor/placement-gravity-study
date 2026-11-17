#!/usr/bin/env bash
# Corpora B and C (PLAN.md 3.2, 3.3): the instrument over the history of every usable repository
# of each history analysis's samples -> results/measure/_history/<sample>/. The sampler clones each
# repository at its pinned commit and deletes the clone after. Steps 4 and 5 then read them.
#   ./step3b_histories.sh [--analysis NAME ...] [--force]
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.history measure "$@"

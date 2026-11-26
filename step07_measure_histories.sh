#!/usr/bin/env bash
# Step 07, corpora B and C (PLAN.md 3.2, 3.3): the instrument over the history of every usable
# repository of each history analysis's samples -> results/measure/_history/<sample>/. The sampler
# clones each repository at its pinned commit and deletes the clone after. Step 08 then reads
# them. Eight repositories are read at a time, each worker's Java held to its share of the memory; a
# repository that fails in that pass is read again alone, with all the memory (--workers 1 reads
# them one at a time from the start). Run it again to resume.
#   ./step07_measure_histories.sh [--analysis NAME ...] [--force] [--workers N]
set -euo pipefail
cd "$(dirname "$0")"
given=("$@")
case " $* " in *" --analysis "*) ;; *) set -- "$@" --analysis $(.venv/bin/python -m placement_gravity.nextstep names histories);; esac
.venv/bin/python -m placement_gravity.history measure "$@"
.venv/bin/python -m placement_gravity.nextstep 07 "${given[@]}"

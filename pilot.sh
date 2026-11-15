#!/usr/bin/env bash
# The pilot (PLAN.md §8, step 2): the pull instrument on chain9 of the just-solve run
# blind-202608100006, Spring and OfficeFloor arms, read from the local clones under ~/compare and the
# stream in ~/spring-petclinic-rest-long-degradation-test. Writes results/pilot/. Run ./setup.sh first.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python -m placement_gravity.pilot --out results/pilot --work .tmp/pilot

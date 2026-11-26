#!/usr/bin/env bash
# Step 06, corpora B and C (PLAN.md 3.2, 3.3): draw each sample runs.yaml declares, with the pinned
# open-source-repository-sampler (lib/sampler, setup.sh), or copy another study's at its pinned
# commit. Needs the network and `gh auth login`. A sample that is not a development one is refused
# until the tag plan-v1 exists. With no name, every sample the histories read.
#   ./step06_samples.sh [NAME ...]
set -euo pipefail
cd "$(dirname "$0")"
given=("$@")
if [ $# -eq 0 ]; then set -- $(.venv/bin/python -m placement_gravity.nextstep names samples); fi
for name in "$@"; do
  .venv/bin/python -m placement_gravity.history sample "$name"
done
.venv/bin/python -m placement_gravity.nextstep 06 --samples "${given[@]}"

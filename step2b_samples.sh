#!/usr/bin/env bash
# Corpora B and C (PLAN.md 3.2, 3.3): draw a sample runs.yaml declares, with the pinned
# open-source-repository-sampler (lib/sampler, setup.sh). Needs `gh auth login`.
#   ./step2b_samples.sh open-source-agent
# A sample that is not a development one is refused until the tag plan-v1 exists.
set -euo pipefail
cd "$(dirname "$0")"
for name in "$@"; do
  .venv/bin/python -m placement_gravity.history sample "$name"
done
.venv/bin/python -m placement_gravity.nextstep 2b --samples "$@"

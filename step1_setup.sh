#!/usr/bin/env bash
# Step 1: the environment. The Python environment, the pinned OfficeFloorSlim jar, RefactoringMiner and
# CodeTracker, the instrument and its tests (setup.sh); then R and glmmTMB for the models of step 4,
# whose versions are recorded in results/versions.txt.
set -euo pipefail
cd "$(dirname "$0")"
./setup.sh
if ! command -v Rscript >/dev/null; then
  echo "ERROR: R is not installed. On Ubuntu: sudo apt install r-base r-cran-glmmtmb r-cran-jsonlite" >&2
  exit 1
fi
Rscript -e 'for (p in c("glmmTMB", "TMB", "jsonlite")) if (!requireNamespace(p, quietly = TRUE)) stop("missing R package: ", p)'
mkdir -p results
{
  echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "java: $(java -version 2>&1 | head -1)"
  echo "python: $(.venv/bin/python --version)"
  Rscript -e 'cat("R:", R.version.string, "\n"); for (p in c("glmmTMB", "TMB", "jsonlite")) cat(p, ": ", as.character(packageVersion(p)), "\n", sep = "")'
  echo "officefloorslim: $(sha256sum lib/officefloorslim.jar | cut -d" " -f1)"
} > results/versions.txt
Rscript analysis/selftest.R
cat results/versions.txt

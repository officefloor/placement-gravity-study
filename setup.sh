#!/usr/bin/env bash
# Setup: the Python environment (.venv, requirements.txt), the released OfficeFloorSlim command line
# into ./lib (sha256-checked against the pin), RefactoringMiner and CodeTracker (refactor/, Maven), the
# pull instrument compiled for Java 17, then the tests. Needs a JDK 17+ and Maven.
set -euo pipefail
cd "$(dirname "$0")"
VERSION="0.5.4"   # OfficeFloorSlim 0.5.4 on SinewSlim 0.2.4, as long-method-slim-study's Amendment 4
SHA="34df911cc689e002008eb2046d1e78fd97c1544c25557d20bdad5b6c62e434bf"
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/pip install --quiet -r requirements.txt
mkdir -p lib
JAR="lib/officefloorslim.jar"
if [ ! -f "$JAR" ] || ! echo "$SHA  $JAR" | sha256sum --check --quiet - 2>/dev/null; then
  curl --fail --location --silent --show-error -o "$JAR" \
    "https://github.com/officefloor/OfficeFloorSlim/releases/download/v$VERSION/officefloorslim.jar"
fi
echo "$SHA  $JAR" | sha256sum --check - || { rm -f "$JAR"; echo "ERROR: $JAR is not the pinned release" >&2; exit 1; }
# RefactoringMiner 3.0.4 and CodeTracker 2.6 (refactor/pom.xml), from Maven Central
(cd refactor && mvn -q -DskipTests package)
mkdir -p instrument/classes
javac --release 17 -nowarn -d instrument/classes -cp "$JAR" instrument/Pull.java
.venv/bin/python -m pytest -q tests

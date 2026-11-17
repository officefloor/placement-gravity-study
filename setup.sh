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
# The literature's shape measures (PLAN.md 4.7a), with the petclinic harness's tools at its pins:
# CK 0.7.0 (sha256-checked), PMD 7.27.0 and, where npm is present, jscpd 5.0.14 (lib/package-lock.json).
CK_VERSION="0.7.0"
CK_SHA="2ddfdc275b6b59c2033e03253c4fec511c338fe494a10b70f651bc039a72c74d"
CK="lib/ck.jar"
if [ ! -f "$CK" ] || ! echo "$CK_SHA  $CK" | sha256sum --check --quiet - 2>/dev/null; then
  curl --fail --location --silent --show-error -o "$CK" \
    "https://repo1.maven.org/maven2/com/github/mauricioaniche/ck/${CK_VERSION}/ck-${CK_VERSION}-jar-with-dependencies.jar"
fi
echo "$CK_SHA  $CK" | sha256sum --check - || { rm -f "$CK"; echo "ERROR: $CK is not the pinned release" >&2; exit 1; }
PMD_VERSION="7.27.0"
if ! lib/pmd/bin/pmd --version 2>/dev/null | grep -q "PMD $PMD_VERSION"; then
  curl --fail --location --silent --show-error -o lib/pmd-dist.zip \
    "https://github.com/pmd/pmd/releases/download/pmd_releases/${PMD_VERSION}/pmd-dist-${PMD_VERSION}-bin.zip"
  rm -rf lib/pmd "lib/pmd-bin-$PMD_VERSION"
  (cd lib && unzip -q pmd-dist.zip && mv "pmd-bin-$PMD_VERSION" pmd && rm pmd-dist.zip)
fi
lib/pmd/bin/pmd --version | grep -q "PMD $PMD_VERSION" || { echo "ERROR: PMD $PMD_VERSION did not install" >&2; exit 1; }
if command -v npm >/dev/null 2>&1; then
  (cd lib && npm ci --silent)
else
  echo "   ! npm not found: jscpd is not installed, and the duplication measures will be empty"
fi
# RefactoringMiner 3.0.4 and CodeTracker 2.6 (refactor/pom.xml), from Maven Central
(cd refactor && mvn -q -DskipTests package)
mkdir -p instrument/classes
javac --release 17 -nowarn -d instrument/classes -cp "$JAR" instrument/Pull.java
.venv/bin/python -m pytest -q tests

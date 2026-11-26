# Placement gravity

Where does the code for a new problem land, and did it have a choice?

The earlier studies looked for bad code in the shape of code as it stands, and found that the
problem fixes the amount (*Conserved amount, negotiable placement*). This study changes the
unit of analysis to **each new problem as it arrives**. It assumes the code added for a problem
is cohesive with that problem, and measures how that code was placed:

- in a new unit or an existing one;
- how far it is dispersed;
- its **pull**: how much pre-existing host state it had to read or write. Pull separates a
  **forced** placement (gravity) from a **chosen** one.
- its **bystanders**: what else was there with the data it needed. The data a problem needs is
  the problem's; what surrounds that data, and grows, is the gravity (H3, H4). Later code is
  expected to come for the few values earlier code was bound to, the place's core, and not for
  the rest (H2).
- what it **introduced**: the parameters and locals it adds to a method and the fields it adds
  to a class. They were not there before, so they are neither needed nor bystanding for this
  change; they are what it leaves for the next (reported, PLAN.md §4.3b).

It then follows each problem forward, in the class and the method its code was placed in, to see
whether the data that stood by there is what later changes are bound to when they come back. The confirmatory data is the paired Spring and OfficeFloor change streams of the degradation
harnesses, where one checkpoint is one problem. The ui runs (many endpoints, 250 checkpoints) are
the primary test; the petclinic runs, which put every rule on one endpoint, are replications read
first.

Shape is read only where the problem is fixed. The measures of solution shape used by the earlier
studies (long, complexity outlier, concentration) enter as competitors; not slimmable and junction
are sinew measures of data flow, read apart:
H6 tests whether any of them draws later code in once the problem, the bindings and the bystanders are held fixed. The plan
absorbs three drafts that read the same runs: flow-injection containment, the ui harness's
SinewSlim analysis plan, and sinew identification (`PLAN.md` §1.1).

| Read | For |
|---|---|
| [`PLAN.md`](PLAN.md) | The study: questions, hypotheses H1–H8 in the order of the story (confirmatory H1, H2, H4, H5; secondary H3, H6, H7; H8 for Run D; H9 deleted, §9 row 108), measures, analysis; a map of how they fit together in §2 ([`figures/placement-forces.svg`](figures/placement-forces.svg)). **Not yet registered:** the tag `plan-v1` was withdrawn on 17 November 2026 while the hypotheses are worked out on the development chain, and will be set before any run named for analysis is read; changes after the start are dated amendments (§9). |
| [`LITERATURE.md`](LITERATURE.md) | The literature: notes by theme, the systematic novelty check (§10), and the full references. |
| [`results/pilot/PILOT.md`](results/pilot/PILOT.md) | The pilot: the instrument on one pair of chains, what it showed, the decisions it raised. |

## Running

```sh
./step1_setup.sh    # .venv, the pinned OfficeFloorSlim 0.5.4 jar (sha256-checked), RefactoringMiner and
                    # CodeTracker (Maven), the instrument and tests; then checks R and glmmTMB, records
                    # every version in results/versions.txt and runs analysis/selftest.R.
                    # Needs JDK 17+, Maven, and R with glmmTMB (Ubuntu: r-base r-cran-glmmtmb r-cran-jsonlite).
./step1b_timing.sh  # optional, about 45 minutes: one model fit by data size -> results/timing.json (PLAN.md 5)
./step2_runs.sh     # each stack's declared roots, then the chains runs.yaml names, pinned in results/heads.tsv;
                    # the problem streams are cloned at their pinned refs where missing
./step3_measure.sh  # the instrument over every pinned chain -> results/measure/<analysis>/
./step2b_samples.sh NAME ...   # corpora B and C: draw each sample, or copy another study's at its pinned commit
./step3b_histories.sh          # the instrument over each sample's histories -> results/measure/_history/
./step4_analyse.sh  # datasets (data/analysis/), models in R (estimates.json), verdicts with Holm (verdicts.json)
./step5_report.sh   # results/analysis/<analysis>/REPORT.md and results/analysis/REPORT.md; beside each report,
                    # DIAGNOSTICS.md: every figure PLAN.md quotes that the report does not print
```

Each step ends by printing the command to run next, with the analyses it was given (before the
tag, the development analyses): the paired chains go 2, 3, 4, 5 and the histories 2b, 3b, 4, 5.
Every input is fetched by the steps from a pinned commit, and every figure the plan quotes is made by
a step (the report, or its diagnostics); nothing is copied in or computed by hand.

Each step takes `--analysis NAME ...` to run only some analyses of `runs.yaml`. **Until the tag
`plan-v1` exists, only the development analysis (`pilot`, chain 9) can be read**: steps 2 to 4
refuse every other. The ui analyses (`ui-primary`, the study's test, and the two pairs that share a front end, `ui-angular` and `ui-tanstack`) are read only when every one of their runs' ten chains is pushed and has reached checkpoint 250, and a head once recorded in `results/heads.tsv` is not replaced (PLAN.md §3.1a). They also refuse while the plan, the registry, the instrument or the analysis
code has uncommitted changes, and each report lists the registered files changed since the tag. `./pilot.sh` regenerates the pilot report in `results/pilot/`: **do not run it** unless that is meant, since `results/pilot/PILOT.md` is the record of the pilot as it was on 15–16 November 2026, with the terms and hypothesis numbers of that day, and the instrument has changed since.

**Working on the code.**

- Tests: `.venv/bin/python -m pytest -q` and `Rscript analysis/selftest.R`.
- After editing `instrument/Pull.java`, recompile it (`javac --release 17 -nowarn -d instrument/classes -cp lib/officefloorslim.jar instrument/Pull.java`, as `setup.sh` does); likewise `instrument/Check.java` (`javac --release 17 -nowarn -d instrument/classes instrument/Check.java`).
- After changing what a measured table means (the instrument, `tables.py`, `chain.py`), raise `MEASURE_VERSION` in `placement_gravity/measure.py` and `HISTORY_VERSION` in `placement_gravity/history.py`: steps 3 and 3b otherwise reuse the old measurements silently.
- Do not change the code while steps 3, 3b or 4 run: step 3b starts a fresh Python process per repository, so a change mid-run mixes two versions of the measurement, and step 4 reads the analysis code as it stands when each analysis starts. Before editing, check that no run is in progress (`pgrep -af 'step[0-9]|placement_gravity|analyse.R'`); a rerun may have been started in the background by an earlier session.
- Step 4 decides the confirmatory tests on a cluster bootstrap (1,000 refits each), which takes far longer than the models alone. Since 26 November 2026 (PLAN.md §9 row 116) H6's measures and H7 are refitted on it too, so a paired analysis takes longer again (roughly seven more models at 1,000 refits), and so does the R self-test. The refits run on `PG_CORES` cores (four by default); each holds its own copy of the model, so more cores need more memory. Do not run the R self-test, or anything else heavy, beside step 3b: the machine has run out of memory that way and the kernel killed a measurement.
- When chaining steps in one command, record each step's own exit status: a chain ending in `; echo exit $?` reports the last command's status, not a failed step's.
- Step 3b clones each repository from GitHub (it needs the network); a full rerun of the pilot and the development histories takes about two hours, so keep the machine from sleeping (for example `systemd-inhibit --what=sleep:idle:handle-lid-switch`).
- The diagram in PLAN.md §2 is `figures/placement-forces.svg`; it was first published as a private page (claude.ai/artifact/7ZQfbsMD3ygsJAbKzffYMJ) and the file in the repository is the record.

The petclinic chains are read from the harness's local clones (`~/compare/spring`,
`~/compare/officefloor`) and published in `officefloor/spring-petclinic-rest`; the ui stacks are
cloned into `~/placement-gravity-data/`. The streams are read at the commits `runs.yaml` pins.
`results/measure/` and `data/` are regenerated from the pinned heads and are not committed.

| Code | |
|---|---|
| `instrument/Pull.java` | The instrument: per addition, hosts, runs and their bindings (method and class), their bystanders (the pre-existing values visible where a run lands that it does not use, PLAN.md §4.3a), the values it introduces (§4.3b), birth bindings, moved code; the amount; with `--shape`, every method of a tree as the earlier studies read it (SinewSlim's length and assessment, junction counts). |
| `instrument/Check.java` | The compiler's reading of a tree (javac's own API), to check the instrument against: what each method calls, reads and refers to (PLAN.md §4.8). |
| `placement_gravity/prepare.py` (`split_rows`) | Logic and organisation: each checkpoint's added code as logic, organisation in bodies, declarations, imports and wiring, with the state handed along (PLAN.md §4.9, reported; Brooks's essence and accident, §1). |
| `placement_gravity/validate.py` | The instrument's calls, field reads and bound names scored against the compiler's, on a sample of each chain's checkpoints (PLAN.md §4.8, reported). |
| `refactor/` | RefactoringMiner 3.0.4 at each commit (`Refactorings.java`) and CodeTracker 2.6 histories (`Histories.java`), built by Maven. |
| `placement_gravity/refactor.py` | RefactoringMiner's findings as the instrument's hints: renames, matches, moved code. |
| `placement_gravity/crosscheck.py` | CodeTracker against the instrument's following of hosts. |
| `placement_gravity/chain.py` | A chain's checkpoints from git, the files of each addition, the wiring. |
| `placement_gravity/tables.py` | Hosts, runs, additions and outcomes from the instrument's output. |
| `placement_gravity/lines.py` | A problem's own lines followed from checkpoint to checkpoint: reported for information beside intrusion at the class and the method (PLAN.md §4.4). |
| `placement_gravity/literature.py` | The literature's shape measures on every method and class (CK, PMD, jscpd, Halstead, Maintainability Index; PLAN.md §4.7a). |
| `placement_gravity/places.py` | Where bound and unbound code lands among the methods and classes it could have gone to, ranked by complexity and by data width (PLAN.md §5, reported). |
| `placement_gravity/readings.py` | The reported readings: choice at a checkpoint, formation and review (PLAN.md §5). |
| `placement_gravity/shape.py` | The shape measures S1, S4 and S5 of H6 and the sinew measures S2 and S3 (PLAN.md §4.7) on each existing host at k − 1, with the complexity-concentration study's cognitive extractor and outlier rule (pinned in `requirements.txt`). |
| `runs.yaml` | The runs read: streams pinned per run, repositories, and each analysis with its role. |
| `placement_gravity/runs.py` | Step 2: the registry, the registration guard, the stacks' roots, fetching and pinning chains. |
| `placement_gravity/measure.py` | Step 3: the instrument and tables over every pinned chain. |
| `placement_gravity/prepare.py` | Step 4: the analysis datasets, the shape variation rule, the amount band and the wiring checks. |
| `analysis/analyse.R` | Step 4: the models of PLAN.md §5 with glmmTMB (`analysis/selftest.R` checks them on simulated data). |
| `placement_gravity/verdict.py` | Step 4: every decision rule and the Holm correction. |
| `placement_gravity/report.py` | Step 5: the reports. |
| `placement_gravity/pilot.py` | The pilot. |
| `tests/` | Fixtures with known answers. |

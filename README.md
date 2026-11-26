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

One order, each script printing the command to run next. Every results step ends a block with a
progress point: it writes the summary again and says which lab note can now be written, and from
what.

```sh
./step01_setup.sh              # .venv, the pinned OfficeFloorSlim 0.5.4 jar (sha256-checked), RefactoringMiner and
                               # CodeTracker (Maven), the instrument and tests; then checks R and glmmTMB, records
                               # every version in results/versions.txt and runs analysis/selftest.R.
                               # Needs JDK 17+, Maven, and R with glmmTMB (Ubuntu: r-base r-cran-glmmtmb r-cran-jsonlite).
./step02_timing.sh             # optional, about 45 minutes: one model fit by data size -> results/timing.json (PLAN.md 5)

./step03_pin_chains.sh         # the petclinic chains runs.yaml names, pinned in results/heads.tsv; the problem
                               # streams are cloned at their pinned refs where missing
./step04_measure_chains.sh     # the instrument over every pinned chain -> results/measure/<analysis>/
./step05_chain_results.sh      # datasets (data/analysis/), models in R (estimates.json), verdicts with Holm
                               # (verdicts.json), the reports and the summary        -> LAB NOTE 1: petclinic

./step06_samples.sh            # corpora B and C: draw each sample, or copy another study's at its pinned commit
                               # (needs the network and `gh auth login`)
./step07_measure_histories.sh  # the instrument over each sample's histories -> results/measure/_history/
./step08_history_results.sh    # the same results for the histories                -> LAB NOTE 2: open source

./step09_run_b.sh              # when Run B is complete: ui-primary, the study's test, and the two pairs that share
                               # a front end, from pinning their chains to results   -> LAB NOTE 3: the main test
./step10_run_c.sh              # when Run C is in runs.yaml (a dated amendment) and complete -> LAB NOTE 4: no injection
./step11_run_d.sh              # when Run D is in runs.yaml and complete; 10 and 11 in either order
                               #                                                      -> LAB NOTE 5: no encapsulation (H8)
./step12_summary.sh            # the last summary, for the write-up; reads nothing new, can be run at any time
```

**What a results step leaves.** `results/analysis/REPORT.md`, the summary: every analysis read so
far with each hypothesis's verdict and p, then the main figure of each hypothesis with its
interval (one ratio or slope a hypothesis, named under the table), then what is still to come.
Beside it, per analysis, `results/analysis/<analysis>/REPORT.md` (every figure of the plan's tests
and readings) and `DIAGNOSTICS.md` (the other figures the plan quotes). The step prints which
analyses it added and what the summary does not hold yet.

**What can be run when.** Steps 01 to 08 need only the tag `plan-v1`: the petclinic runs and the
open-source histories exist already. Their summaries show what the replications and the histories
say before the ui runs are in. Steps 09, 10 and 11 each
refuse, reading nothing, until every chain of their run is pushed and has reached its last
checkpoint, so each is safe to try early; a head once recorded in `results/heads.tsv` is not
replaced (PLAN.md §3.1a). Run C and Run D are not in `runs.yaml` yet: each is added with its run
ids by a dated amendment (PLAN.md §9), committed, before any of its backend Java is read, and its
step says so until then. After each of them the summary is written again with what it added.
**The study's test is `ui-primary` (step 09)**: what steps 01 to 08 show are replications and outside
evidence, never the verdict, and the harness and the stream are not changed for anything they show
while a run is still being made.

With no argument a step reads everything of its stage; before the tag that is the development
analyses only (`pilot`, chain 9; `open-source-development`), which is how the steps are tried
out. Steps 03, 04, 05, 07 and 08 take `--analysis NAME ...` to read only some analyses of `runs.yaml`,
and step 06 takes sample names; the next command printed then carries them on. **Until the tag
`plan-v1` exists, only the development analyses can be read**: every step refuses any other. They
also refuse while the plan, the registry, the instrument or the analysis code has uncommitted
changes, and each report lists the registered files changed since the tag. Every input is fetched by
the steps from a pinned commit, and every figure the plan quotes is made by a step (the report, or
its diagnostics); nothing is copied in or computed by hand. Until 27 November 2026 the steps were
numbered 1, 1b, 2, 2b, 3, 3b, 4, 5 (now 01, 02, 03, 06, 04, 07, and 4 and 5 together in each
results step: 05, 08 and each run's); PLAN.md's text of before
that day uses those numbers (§9 row 125). `./pilot.sh` regenerates the pilot report in
`results/pilot/`: **do not run it** unless that is meant, since `results/pilot/PILOT.md` is the
record of the pilot as it was on 15–16 November 2026, with the terms and hypothesis numbers of that
day, and the instrument has changed since.

**Working on the code.**

- Tests: `.venv/bin/python -m pytest -q` and `Rscript analysis/selftest.R`.
- After editing `instrument/Pull.java`, recompile it (`javac --release 17 -nowarn -d instrument/classes -cp lib/officefloorslim.jar instrument/Pull.java`, as `setup.sh` does); likewise `instrument/Check.java` (`javac --release 17 -nowarn -d instrument/classes instrument/Check.java`).
- After changing what a measured table means (the instrument, `tables.py`, `chain.py`), raise `MEASURE_VERSION` in `placement_gravity/measure.py` and `HISTORY_VERSION` in `placement_gravity/history.py`: steps 04 and 07 otherwise reuse the old measurements silently.
- Do not change the code while steps 04, 07 or a results step run: step 07 starts a fresh Python process per repository, so a change mid-run mixes two versions of the measurement, and a results step reads the analysis code as it stands when each analysis starts. Before editing, check that no run is in progress (`pgrep -af 'step[0-9]|placement_gravity|analyse.R'`); a rerun may have been started in the background by an earlier session.
- A results step (05, 08, 09 to 11) decides the confirmatory tests on a cluster bootstrap (1,000 refits each), which takes far longer than the models alone. Since 26 November 2026 (PLAN.md §9 row 116) H6's measures and H7 are refitted on it too, so a paired analysis takes longer again (roughly seven more models at 1,000 refits), and so does the R self-test. The refits run on `PG_CORES` cores (four by default); each holds its own copy of the model, so more cores need more memory. Do not run the R self-test, or anything else heavy, beside step 07: the machine has run out of memory that way and the kernel killed a measurement.
- When chaining steps in one command, record each step's own exit status: a chain ending in `; echo exit $?` reports the last command's status, not a failed step's.
- Step 07 clones each repository from GitHub (it needs the network); a full rerun of the pilot and the development histories takes about two hours, so keep the machine from sleeping (for example `systemd-inhibit --what=sleep:idle:handle-lid-switch`).
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
| `placement_gravity/tables.py` (`at_level`) | The binding levels: H1's count, H2's arm contrast and H4's later intrusion read with injection ignored, as registered, and with injection excluded (PLAN.md §4.3c, reported; decides nothing). |
| `placement_gravity/lines.py` | A problem's own lines followed from checkpoint to checkpoint: reported for information beside intrusion at the class and the method (PLAN.md §4.4). |
| `placement_gravity/literature.py` | The literature's shape measures on every method and class (CK, PMD, jscpd, Halstead, Maintainability Index; PLAN.md §4.7a). |
| `placement_gravity/places.py` | Where bound and unbound code lands among the methods and classes it could have gone to, ranked by complexity and by data width (PLAN.md §5, reported). |
| `placement_gravity/readings.py` | The reported readings: choice at a checkpoint, formation and review (PLAN.md §5). |
| `placement_gravity/shape.py` | The shape measures S1, S4 and S5 of H6 and the sinew measures S2 and S3 (PLAN.md §4.7) on each existing host at k − 1, with the complexity-concentration study's cognitive extractor and outlier rule (pinned in `requirements.txt`). |
| `runs.yaml` | The runs read: streams pinned per run, repositories, and each analysis with its role. |
| `placement_gravity/runs.py` | Step 03: the registry, the registration guard, the stacks' roots, fetching and pinning chains. |
| `placement_gravity/measure.py` | Step 04: the instrument and tables over every pinned chain. |
| `placement_gravity/prepare.py` | The results steps: the analysis datasets, the shape variation rule, the amount band and the wiring checks. |
| `analysis/analyse.R` | The results steps: the models of PLAN.md §5 with glmmTMB (`analysis/selftest.R` checks them on simulated data). |
| `placement_gravity/verdict.py` | The results steps: every decision rule and the Holm correction. |
| `placement_gravity/report.py` | The results steps and step 12: the reports and the summary. |
| `placement_gravity/pilot.py` | The pilot. |
| `tests/` | Fixtures with known answers. |

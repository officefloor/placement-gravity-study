# Plan: where a new problem's code lands, and whether it had a choice

> **Status (15 November 2026): DRAFT, not registered.** The instrument is built and piloted on one
> pair of chains (`results/pilot/PILOT.md`); nothing else has been measured for this study. Every **[DECIDE]** is settled at
> registration, before any confirmatory measurement. The literature behind this plan is in
> [`LITERATURE.md`](LITERATURE.md).

## 1. Why this study, and what it replaces

The earlier studies looked for bad code in the **shape of the code as it stands**:

- outliers in a per-unit complexity measure (the complexity-concentration study,
  doi:10.5281/zenodo.23581333);
- coupling divergence (*What reviewers call a Long Method is a length*, doi:10.5281/zenodo.23749773);
- what extraction can and cannot slim (doi:10.5281/zenodo.23991506);
- and, exploratory, the live-width profiles of long methods (`long-method-slim-study`, step 7).

Each found something, and each ran into the same problem. *Conserved amount, negotiable
placement* (doi:10.5281/zenodo.23190619) says that the **problem fixes the amount** of complexity
and only its placement varies. A measure of how big or complex a unit is therefore measures, first
of all, how big the problem it solves is. Step 7 found that live-width profiles form a continuum,
not families (best silhouette 0.23, unstable across seeds). The size-confounding literature
(El Emam et al. 2001; Chowdhury et al. 2022b) found that many structural metrics carry little
information once size is controlled.

This study turns the question round:

- **The unit is a new problem, not a piece of code.** Cohesion cannot be measured: the same null
  check can be an `if` statement or an annotation. So the study does not try to measure it.
  It **assumes** that the code added for one new problem is cohesive with that problem, and asks
  how that code was **placed**.
- **Shape is plasticity**, the space of placements the code for a problem could take. The problem
  fixes the size. The form of the code (methods sharing a scope, or injected functions) fixes how
  much of that space is open.
- **The concern is gravitation:** code for a new problem has to land in an existing
  concentration because its data ties it there, not because the problem belongs there. Each
  forced placement widens the host, and a wider host pulls the next addition in.

Following problems over time has precedents. Passos et al. (2015; 2018) follow each Linux
feature's scattering over eight years. Bouwers, van Deursen and Visser (2014) classify each
change-set as local or non-local. Both measure where a problem's code *ended up*, and their
"feature" is a configuration option or a component, not a requirement. What this study adds is
a problem defined independently of the code (a change request), measured at the commit where
its code lands, and the question of whether that placement was forced (`LITERATURE.md` §10).

The study does **not** assume that concentration is bad or that dispersion is good. Concentration
contains ripples among things that change together. Dispersion keeps a change to one problem from
dragging the rest along (Parnas 1972). Which is better depends on how the problems actually change
together, and that is only known afterwards. What can be measured at the time of each change is
whether the placement was **chosen** or **forced**. The claim under test is that forced
placement, not concentration as such, is what does the harm.

## 2. Questions and hypotheses

- **Q1 (description).** For each new problem: does its code go into new units or into existing
  ones, how far is it dispersed, and how large were the hosts it landed in?
- **Q2 (gravity).** How strongly does each addition depend on state that already existed in its
  host (its **pull**, §4)? Does pull grow as hosts grow and the system ages?
- **Q3 (consequence).** Are forced placements followed by more tangling (later changes to *other*
  problems touching this problem's code) than chosen placements of the same size?
- **Q4 (form).** For the same stream of problems, is pull lower and flatter under function
  injection than under methods, while the amount stays about the same?

Hypotheses. Directions are fixed now; thresholds are **[DECIDE]**.

- **H1, gravity compounds.** In the methods arm, an addition's pull rises with its host's size
  before the change and with the checkpoint index (positive slope, 95% interval above 0).
- **H2, forcing does the harm, not concentration.** Controlling for the addition's size and its
  host's size, forced placements are followed by more cross-problem intrusion than chosen
  placements. Concentration on its own, with pull held fixed, shows no consistent association.
  This makes confirmatory the result of Olbrich, Cruzes and Sjøberg (2010): god and brain
  classes change more and hold more defects, but less per line once size is controlled.
- **H3, function injection keeps the space open.** On the same stream, the function arm's pull
  is lower, and its slope on host size is flatter, than the methods arm's. The total amount
  (positions, tokens) differs by less than **[DECIDE]**%. The coupling that leaves the scopes
  appears as wiring edges (§4.5) and is reported, not hidden.
- **Q1 is descriptive.** Its expected baseline (Steidl and Deissenboeck 2015) is that most
  growth is new methods. So the share of additions that land in an existing host is reported as
  found, with no direction predicted.

**What would count against.**

- H1: no slope, or a negative one. Pull would then be a constant cost of placement, not gravity.
- H2: chosen and forced placements equally intruded on, or concentration alone predicting
  intrusion better than pull.
- H3: no difference between the arms, or a function arm that hides its coupling in wiring
  edges that grow as fast as the methods arm's pull.

Every one of these outcomes is reported whichever way it points.

## 3. Data

### 3.1 Corpus A: the paired streams (primary, confirmatory)

The petclinic degradation harness (`spring-petclinic-rest-long-degradation-test`) grows one
application through a fixed stream of plain-English change requests, under a Spring
`@RestController` arm and an OfficeFloor arm. Every checkpoint is committed separately, and the
runs are published as `evolve/<run>/<strategy>/<arm>/chain<n>` branches of
`officefloor/spring-petclinic-rest` (145 branches as of 15 November 2026). Later, the
`ui-long-degradation-test` runs (250 checkpoints; Spring and OfficeFloor backends) are added
once they exist.

Why this corpus comes first:

- **One checkpoint is one new problem.** The cohesion assumption holds by construction, and the
  problem of tangled commits (Herzig and Zeller 2013) does not arise. The exception is
  refactoring done in the same checkpoint, which is detected and set apart (§4.1).
- **The problem is held fixed between the arms**, so a difference in placement is a difference
  of form, not of problem.
- **The stream declares which later checkpoints change which earlier rules** (mutative
  checkpoints, and the "crosses at least two earlier rules" property in the ui stream). That
  gives a ground truth of which problems were *meant* to change together, which history mining
  in the wild lacks.

**[DECIDE]**: which runs, strategies and chains are read; named by run id at registration.

### 3.1a Corpus A2: the ui-long-degradation runs (after the petclinic corpus)

The ui-long-degradation harness grows OfficeHQ through 250 checkpoints, ten chains per stack, on
one stream, agent and harness commit across its runs. Its plan freezes these at a tagged commit so
that analyses registered against its runs can name what they read. This study reads the back
end's production Java of the four stacks of its Runs A and B, a front end × back end square:

| | Spring | OfficeFloor |
|---|---|---|
| **Angular** | Run A (`angular-spring`) | Run B (`angular-officefloor`) |
| **TanStack** | Run B (`tanstack-spring`) | Run A (`tanstack-officefloor`) |

- **Primary contrast:** Spring against OfficeFloor, averaged over the two front ends. Each run
  gives one Spring and one OfficeFloor stack, so differences between the runs (date, machine)
  cancel out of this contrast.
- **Secondary:** the two pairs that share a front end (Angular, TanStack), each read as a
  replication.
- **Not separable:** an influence of the front end on the back end, and a difference between
  Run A and Run B, are confounded in this square. The study does not depend on either being
  absent; it reports the per-front-end pairs so that a disagreement between them shows.
- **Run C** (the no-injection control) is not read.
- Every new rule in the stream declares the earlier rules it crosses (at least two), which gives
  the declared crossings of §4.4. A reader for that format is to be added and tested on fixtures,
  not on a run that will be analysed.

**Order.** The petclinic corpus (§3.1) is analysed first; the ui runs follow once Run B is complete.

**Before any ui run's backend Java is read for this study,** three plans that read the same runs
must be registered:

1. **This plan.**
2. **The flow-injection-containment plan**, which reads the TanStack stacks. Its draft excludes a
   run whose Java-layer results were seen before its registration. A proposed Amendment 1
   (16 November 2026) lets it register now and read its gates later.
3. **The ui harness's SinewSlim analysis plan** (branch `sinewslim-analysis-plan`, draft of
   31 October 2026), which reads the same-front-end pairs including all four stacks above. It must
   register before any of its runs is read with SinewSlim, and this study's instrument is built
   on SinewSlim's facts and seam.

After all three are registered, the order in which they read does not matter. Each lists the
others' results it saw before its analysis.

### 3.2 Corpus B: open-source histories (secondary, external validity)

Pre-AI Java repositories drawn by `open-source-repository-sampler`, seed and as-of date
**[DECIDE]**. Additions are commits linked to an issue labelled as a feature or enhancement,
under **[DECIDE]** changed lines, with refactorings removed by RefactoringMiner. Commits linked
to issues are known to be a biased subset (Bird et al. 2009), and tangling remains at the
reported 7–20% (Herzig et al. 2016). Corpus B is therefore read as a check on the direction of
H1 and H2, not as their test.

## 4. Measures

The instrument extends the width harness (`long-method-slim-study/width/harness/WidthProfile.java`)
on SinewSlim's fact producer and seam, at a pinned OfficeFloorSlim version **[DECIDE]**
(≥ 0.5.4, which carries the loop correction). Positions, values, the literal rule and the loop
rule are those of the width README.

### 4.1 The addition

For each checkpoint (or commit) *k*: the diff from *k − 1* to *k* in production Java. RefactoringMiner
3.0.4 (Tsantalis et al. 2022), the version CodeTracker 2.6 pins, runs at each commit:

- renames (of values, fields, methods and types) are applied to the before version first;
- renamed, moved and re-signatured methods and types stay matched;
- moved or restructured code (extract, inline, extract or inline variable, loop↔pipeline, invert
  condition, split and merge) is a **re-placement**, not an addition. Identical-text matching
  covers moves it does not report.

The **addition** is what remains: the positions added or changed for the new problem, as a set of
runs, each run being contiguous positions of one host.

### 4.2 Placement (Q1)

- **New or existing host:** whether each run lands in a unit created at *k* or in one that already
  existed at *k − 1*.
- **Dispersion:** the number of distinct hosts (methods and classes) the addition touches, and
  the Gini coefficient of its positions across them (Vasa et al. 2009 use Gini for concentration
  over evolution).
- **Host size:** the host's positions at *k − 1* (0 for a new host).
- **Interleaving:** the number of runs per host. An addition split across a host's statements
  is placed against the host's order.

### 4.3 Ties (Q2), the measure of gravitation

Only **logic lines** carry the value of a change: a method's body statements. Signatures,
declarations, imports and constructor wiring are organisation. What matters is where the data each
added or edited logic line uses comes from. If it comes from values the change itself defines, the
code could have been placed anywhere. If it comes from values that already existed, the code has to
be placed near them, so choice is restricted. Those are its **ties** (`instrument/Pull.java`;
`results/pilot/PILOT.md`):

- **Method ties:** the host method's pre-existing parameters and locals.
- **Class ties:** the host class's pre-existing fields (constants included) and methods. In Spring,
  injected dependencies are fields, so they tie code to its class. Inherited members tie too; the
  instrument reports any reference it cannot resolve (none in the pilot).
- Every reference on an added or edited logic line counts. A token-level reading, which counts
  only what an edit itself introduced, is reported beside it.

**Not ties:**

- **Injected parameters.** A function placed anywhere can declare them; every parameter of a wired
  OfficeFloor function is injected, though its locals still tie.
- **Class utilities** (loggers), which any class can declare; they are reported apart.
- **Birth ties**, the values a caller passes a new method; they are reported, already counted on
  the caller's line.

Ties are related to Feature Envy turned inwards (Tsantalis and Chatzigeorgiou 2009). Their metric
finds a method drawn towards *another* class's data, as a snapshot recommendation. Ties measure an
addition held by its *own* host's pre-existing data, at the commit where it is placed.

**Forced / chosen:** a run is forced when its ties are 1 or more, and chosen otherwise. The cuts
2, 3 and 4 are reported beside it. Because the pilot finds 93% of Spring's runs into existing
methods forced at 1, H1 and H2 are tested on the tie count, with the cut as a reading aid. H1 is
read at method level in both arms and at class level in Spring (class ties against the class's
size); OfficeFloor's class level is reported.

### 4.4 Consequence (Q3)

Each problem's hosts are followed forward to the end of the chain, across renames and moves. A
method that survives to the end is followed by CodeTracker 2.6 (Jodavi and Tsantalis 2022): its
identity, and the checkpoints that change its body. A method removed before the end has no
CodeTracker history and is followed by the instrument's own chaining of RefactoringMiner's renames
and moves (decided 16 November 2026; the pilot finds the two agreeing on 91–99% of checkpoints):

- **Containment:** later changes that the stream declares to be *about* problem *p* (mutatives
  of *p*'s rule). The number of hosts they touch outside *p*'s placement, normalised by the
  change's size.
- **Intrusion:** later changes for *other* problems, not declared to cross *p*, that touch *p*'s
  positions. The count per 100 later checkpoints.
- **Local-change ratio** (secondary): the share of later change-sets touching *p*'s code that
  stay within one component, as defined by Bouwers, van Deursen and Visser (2014). This lets the
  results be compared with the systems they published.
- **Declared crossings** (corpus A only) are separated from undeclared ones. A crossing the
  stream intends is the problem's own coupling. One it does not intend is the placement's.

### 4.5 Wiring (H3)

In the OfficeFloor arm, coupling that leaves a scope becomes configuration: flows, the objects
injected into a procedure, governance. For each addition, the **wiring edges added** (new links
in the application's configuration and new injected dependencies) are counted, and reported
beside pull. This keeps the coupling the form moves out of the code from going unreported.

### 4.6 Amount (conservation check)

Total positions and tokens per arm at each checkpoint, so that H3 is read against the
conservation result: the same amount, placed differently.

## 5. Analysis

- **Unit:** an addition run (Q2, H1) or an addition (Q1, Q3, H2), nested in checkpoints nested in
  chains.
- **H1:** a mixed model of log(1 + P) on log(host positions) and checkpoint index, with a random
  intercept for the chain. The slopes are reported with 95% bootstrap intervals over chains.
- **H2:** a negative binomial model of intrusion on pull (continuous, and forced/chosen),
  addition size, host size and act, with a random intercept for the chain. Concentration (host
  size, Gini) is entered alone and with pull, and the change in fit is reported.
- **H3:** the arm term and its interaction with host size in the H1 model, on the paired chains.
  The amount is compared per checkpoint.
- **Corpus B:** the H1 and H2 models with a random intercept for the repository. Direction and
  interval only.
- **Multiplicity:** H1–H3 are three confirmatory tests at α = 0.05 each, Holm-corrected. All
  else is descriptive.

## 6. What was known when this was written

- **Seen.** The conversation that produced this plan. Step 7 of `long-method-slim-study`
  (width profiles, the 20-repository pilot): profiles are a continuum; width grows sub-linearly
  with length (pooled exponent 0.57) and flattens past about 44 positions. The conservation
  paper's results, including that its AI-reviewed condition consolidated the OfficeFloor
  pipeline, raising concentration. That result is the reason H3 is not assumed and the wiring is
  counted.
- **The pilot** (15–16 November 2026, `results/pilot/PILOT.md`): the instrument on chain 9 of the
  just-solve run `blind-202608100006`, both arms. Descriptive figures for every measure were seen
  for that one pair of chains; no hypothesis statistic was computed. Those chains are excluded
  from the registered analysis. The pilot raised six decisions (PILOT.md, *Decisions*), which are
  settled at registration.
- **Not seen.** Pull, placement, containment or intrusion on any other chain, run or repository.
  The petclinic runs have been read for other measures (the conservation paper), never for these.
- **Expectation.** The author expects H1 and H3 to hold, and expects H2 to be the hardest to
  show, because the intrusion counts per chain may be small.
- **Conflict of interest.** The author created OfficeFloor, SinewSlim, OfficeFloorSlim and both
  harnesses. Mitigations, as in the earlier studies: the arms run on the same fixed stream and
  agent; the instrument's rules are fixed here; every case where the function arm does worse is
  reported; corpus B is drawn by an independent sampler.

## 7. Threats

- **Agent-written code (corpus A).** Placement by an agent may not be placement by people.
  Corpus B is the check, which is why it is drawn pre-AI. There is a specific reason for concern:
  AI agents' pull requests touch fewer files and spread less than human ones of similar size
  (Ogenrwot and Businge 2026), so agents may concentrate by default. The arms of corpus A are
  therefore read only against each other, never as absolute rates of concentration.
- **Lexical names.** No symbol solver, as in the width harness, so fields shadowed by locals may
  be miscounted. **[DECIDE]**: whether to add JavaParser's symbol solver for `P_c`.
- **Provenance.** Line tracking across moves is imperfect. CodeTracker reports about 99.9%
  method-level precision and recall, but statement-level provenance is weaker. Disagreements
  with `git blame` are reported.
- **Smells born, not grown.** Tufano et al. (2015) find most smells present from a unit's
  creation. So H1's gravity may act mostly at creation (a new method pulled by its parameters,
  §4.3) rather than through accretion. Both are measured, so the data can say which.
- **The cohesion assumption.** It holds by construction only in corpus A, and only if refactoring
  is separated out correctly (§4.1).

## 8. Order of work

1. ~~Build the instrument (§4): fixtures with known pull and placement, and tests.~~ Done:
   `instrument/Pull.java`, `placement_gravity/`, `tests/` (RefactoringMiner and CodeTracker not yet
   integrated; PILOT.md, decisions 4 and 5).
2. ~~Run a pilot on **two chains** of one petclinic run, not among those named at registration,
   to check that the measures compute and are not degenerate.~~ Done 15 November 2026:
   `results/pilot/PILOT.md`.
3. Settle every **[DECIDE]** and register (tag `plan-v1`).
4. Run corpus A, then corpus B. Analyse once; record hashes.
5. Write up, reporting every hypothesis whichever way it falls.

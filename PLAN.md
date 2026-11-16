# Plan: where a new problem's code lands, and whether it had a choice

> **Status (16 November 2026): DRAFT, not registered.** The instrument is built and piloted on one
> pair of chains (`results/pilot/PILOT.md`); nothing else has been measured for this study. Every
> design decision was settled on 16 November 2026. What remains open is only what needs the data
> to exist (§3.1a): Run B's ids, Run C's ids when its stack is built, each chain's head when its
> run is pushed, and the ui stacks' backend paths from their stack declarations. The literature behind this plan is in
> [`LITERATURE.md`](LITERATURE.md). Since 16 November 2026 this plan absorbs three drafts that read
> the same runs (§1.1).

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

**The problem has to be held fixed.** The earlier studies, like most of the code-smell literature,
judge the shape of a solution without the problem it solves: a long method, a high complexity or a
junction is read as bad whatever it is for. If the problem dictates the size, a shape measured
across different problems reports the problems as much as the code. At best it finds a consistency
in the problems that happened to be sampled; at worst it is noise. The concern grows with AI
assistants, which may be given larger and harder problems, so a change in the shape of their code
need not mean a change in how well it is written. This study therefore reads shape only where the
problem is fixed: one checkpoint is one problem, and both arms solve the same stream. It also
**tests** the claim rather than assuming it. H2 asks whether the shape measures the earlier studies
used predict later intrusion once the problem and the ties are held fixed (§2, §4.7).

### 1.1 What this plan absorbs (16 November 2026)

Three plans read the same runs with measures of the solution's shape. None has read a run. Two are
unregistered drafts. The SinewSlim analysis plan's file says it is a draft, but its rule makes
registration the commit of the file, and that commit was pushed on 31 October 2026 with a message
calling it registered; it is therefore withdrawn by a dated amendment on its own branch, not
simply closed. Their measures enter this plan as the shape competitors of H2, or as checks, so one
registration covers them:

- **The flow-injection-containment draft** (`flow-injection-containment-experiment`, 20 October
  2026; closed by its own commit). Its junction share (P1) becomes the host-level junction measure
  of §4.7. Its conservation check (P2) is §4.6, with its band. Its trajectory (P5) is H1's checkpoint
  slope, read per arm. Its god-unit count (P3) and its gated-condition lever (P4) are dropped.
- **The ui harness's SinewSlim analysis plan** (branch `sinewslim-analysis-plan`, 31 October 2026).
  Its not-slimmable methods (H1) become a shape competitor of §4.7. Its mechanism (H2, behaviour
  added inside existing methods) is what Q1 and the ties measure. Its wiring test (H4) becomes H3's
  wiring condition. Its go/no-go bar for OfficeFloorSlim is a product decision and stays in the
  harness, outside this study.
- **The sinew-identification study** (on hold since 19 October 2026; closed by its own commit). Its
  restated sinew, data coupled to the control flow, is what the ties measure at the commit where
  code is placed.

The injected-coupling measurement study existed to validate the flow-injection draft's coupling
instrument. This plan uses the simpler rule of §4.3 (a wired OfficeFloor function's parameters are
injected). That study is shelved; if it is ever completed, it is a sensitivity reading here, not a
gate.

## 2. Questions and hypotheses

- **Q1 (description).** For each new problem: does its code go into new units or into existing
  ones, how far is it dispersed, and how large were the hosts it landed in?
- **Q2 (gravity).** How strongly does each addition depend on state that already existed in its
  host (its **pull**, §4)? Does pull grow as hosts grow and the system ages?
- **Q3 (consequence).** Are forced placements followed by more tangling (later changes to *other*
  problems touching this problem's code) than chosen placements of the same size?
- **Q4 (form).** For the same stream of problems, is pull lower and flatter under function
  injection than under methods, while the amount stays about the same?

Hypotheses. Directions and thresholds are fixed now (thresholds decided 16 November 2026).

- **H1, gravity compounds.** In the methods arm, an addition's pull rises with its host's size
  before the change and with the checkpoint index (positive slope, 95% interval above 0).
- **H2, forcing does the harm, not shape.** Holding the problem fixed (the addition's size and
  the earlier rules it declares it crosses) and the host's size:
  - **H2a:** the more ties an addition has, the more cross-problem intrusion follows it (forced
    placements more than chosen ones);
  - **H2b:** with the ties in the model, the shape of the host the addition landed in adds nothing.
    The shape measures are those of §4.7: long, not slimmable, junction, complexity outlier and
    concentration. Each one's effect lies within the equivalence bound of §5.

  H2 is supported only if both hold. This makes confirmatory the result of Olbrich, Cruzes and
  Sjøberg (2010): god and brain classes change more and hold more defects, but less per line once
  size is controlled.
- **H3, function injection keeps the space open.** On the same stream, the function arm's pull
  is lower, and its slope on host size is flatter, than the methods arm's. The total amount
  (positions, tokens) of the function arm lies within 0.8 to 1.25 times the methods arm's, the
  band the flow-injection draft took from the conservation study's spread. The coupling that
  leaves the scopes appears as wiring (§4.5) and is reported, not hidden.
- **Q1 is descriptive.** Its expected baseline (Steidl and Deissenboeck 2015) is that most
  growth is new methods. So the share of additions that land in an existing host is reported as
  found, with no direction predicted.

**What would count against.**

- H1: no slope, or a negative one. Pull would then be a constant cost of placement, not gravity.
- H2: chosen and forced placements equally intruded on (against H2a), or any shape measure that
  still predicts intrusion with the problem and the ties held fixed (against H2b). The second
  would mean that shape carries information the problem does not, and it is reported as such.
- H3: no difference between the arms, or an amount outside the band (the difference is then a
  difference of amount, not placement), or a function arm that moves its coupling into the wiring:
  wiring per problem that rises over the run, or one configuration file that holds most of it
  (§4.5).

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

**Runs read** (decided 16 November 2026):

- **Primary:** `blind-202608100006/just-solve`, both arms, chains 1 to 8 and 10. Chain 9 is the
  pilot's development data and is excluded.
- **Secondary, each read on its own as a replication, never pooled with the primary or with each
  other:** the other strategies, `blind-202609010045/impact_gated`,
  `blind-202609031757/impact_gated`, `blind-202609160027/cohesion-prompt` and
  `blind-202609290948/reviewed`, and the earlier just-solve runs, `202608011310`,
  `full-202608102319` and `202608081920`. A different instruction to the agent is a different
  condition. A run with fewer than 6 chains in an arm is reported descriptively.
- The commit read on each chain is its branch head in `officefloor/spring-petclinic-rest`,
  recorded with its hash when the analysis runs.

**Corpora are replications, never pooled.** The petclinic and ui streams are different problems.
Each is analysed on its own and the two are compared by direction and interval, so that no
estimate mixes solutions to different problems.

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
- **Run C** (the no-injection control: a Java server with neither dependency injection nor
  function injection, so every datum is passed or becomes a shared static) is read as a **third
  arm** once it exists (decided 16 November 2026). Its stack had not been built on 16 November 2026. It is added by a
  dated amendment, naming its run ids, before any of its backend Java is read. Its predicted
  direction is fixed now: the most ties of the three arms, as nothing is lifted off the flow
  (dependency injection weakens ties, function injection removes them). Spring against
  OfficeFloor stays the primary contrast; the control is read against each.
- Every new rule in the stream declares the earlier rules it crosses (at least two from cp17),
  which gives the declared crossings of §4.4. They are read from the stream's
  `acceptance/DENSITY.md` at the tag `run-a` (§4.4, *As built*).

**Order.** The petclinic corpus (§3.1) is analysed first; the ui runs follow once Run B is complete.

**Condition.** `just-solve` only.

**Run A** (recorded 16 November 2026 from the study machine; still running then, and nothing of it
read here):

| Run id | Stack | Repository | Branches |
|---|---|---|---|
| `202610271-as` | Angular / Spring | `officefloor/officehq-angular-spring` | `evolve/202610271-as/just-solve/chain1` … `chain10` |
| `202610271-to` | TanStack / OfficeFloor | `officefloor/officehq-tanstack-officefloor` | `evolve/202610271-to/just-solve/chain1` … `chain10` |

The shared prefix `202610271` names the pairing. Both runs were started at harness commit
`8b39da3c7afa3e0f848a31d0db987618db86a6b6` of `ui-long-degradation-test`, tagged **`run-a`** on
GitHub: this names the stream (`checkpoints.yaml`) and the harness. The agent is the one that
commit's `config.yaml` fixes: **`claude-opus-5-5`**. Each chain's branch carries the evolved code
and its capture under `evolve-results/`; the registered analysis reads the branches as pushed to
the stack repositories by the harness's `push.sh`. On 16 November 2026 chains 1 to 3 of each run
had been pushed; their branch names were listed, and nothing of them was fetched or read here.

**Run B had not started on 16 November 2026.** Its run ids (the `angular-officefloor` and
`tanstack-spring` stacks) are to be recorded here from the study machine when it starts, as Run A's
were. Until then the square of the table above has only its Run A diagonal.

**[DECIDE]** before registration: the run ids of Run B, and the commit of each chain's branch
that is read (each chain's head once its run has finished and been pushed). If registration comes
before Run B starts, its ids are added by a dated amendment before any of its backend Java is read.

**To check before the ui runs are read:** the instrument reads production Java under
`src/main/java/` and wiring under `src/main/resources/officefloor/`, the petclinic layout. The ui
stacks' backend paths are declared by each stack (`stack.yaml`) and may differ; the paths are to be
set from the stack declarations, not from a run.

**This plan registers before any ui run's backend Java is read**, by anyone, for any measure. It
replaces the flow-injection draft and the SinewSlim analysis plan for these runs (§1.1), so no
other registration has to come first. A ui-harness analysis that reads the backend Java for
another purpose after this registration is listed in the report, with its date, as seen before
this analysis.

### 3.2 Corpus B: open-source histories (secondary, external validity)

Pre-AI Java repositories drawn by `open-source-repository-sampler` with **seed 2** (decided 16 November 2026), the
population the complexity-concentration and sinew-identification studies drew, so the ties can be
set beside their shape findings on the same code (their shape results have been seen; ties on this
code have not). History is read up to **29 June 2021**, the day GitHub Copilot's preview opened.
Additions are commits linked to an issue labelled as a feature or enhancement, of **at most 200
changed lines** of production Java, with refactorings removed by RefactoringMiner. Commits linked
to issues are known to be a biased subset (Bird et al. 2009), and tangling remains at the reported
7–20% (Herzig et al. 2016). In corpus B a commit is not reliably one problem and the problem is not
held fixed. Corpus B is therefore read only as a check on the **direction of H1 and H2a**; H2b,
H3 and the junction × arm reading are not read there.

## 4. Measures

The instrument extends the width harness (`long-method-slim-study/width/harness/WidthProfile.java`)
on SinewSlim's fact producer and seam, at OfficeFloorSlim **0.5.4** (SinewSlim 0.2.4), pinned
by its sha256 in `setup.sh` (decided 16 November 2026): the version of the long-method-slim study's Amendment 4, which
carries the loop correction. A later version needs a dated amendment. Positions, values, the literal rule and the loop
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

**As built** (`tables.stream` and `tables.crossings`, 16 November 2026). A later checkpoint *j*
that touches *p*'s code is counted once, in the first of: **declared** (*p* is in *j*'s `mutates`),
**crossed** (a rule *j* introduces interacts with *p*'s rule), or **intrusion** (neither). The
crossings come from the ui stream's `acceptance/DENSITY.md`, generated by its builder: per
checkpoint, each rule it introduces with the earlier rules a value of its own spec depends on
together with it. Each rule is mapped to the checkpoint that introduces it. The reader refuses an
entry it cannot read, a degree that does not match its partners, a partner not introduced earlier,
and a rule introduced twice. On the stream at `run-a` (read 16 November 2026; the stream, not a
run): 250 checkpoints, 231 rules, 224 checkpoints crossing a median of 6 earlier ones (at most
31), none from cp17 crossing fewer than 2. 55 checkpoints both mutate and cross the same earlier
one; they count as declared. A checkpoint that introduces no rule can be mutated but not crossed.
The petclinic stream has `mutates` and no crossings, so there every later touch is declared or
intrusion.

### 4.5 Wiring (H3)

In the OfficeFloor arm, coupling that leaves a scope becomes configuration: flows, the objects
injected into a procedure, governance. For each addition, the **wiring edges added** (new links
in the application's configuration) are counted, and reported beside pull. This keeps the
coupling the form moves out of the code from going unreported.

**New injected dependencies are not edges** (decided by the author, 16 November 2026). A new
dependency creates mass, not pull: it is gravity only when a later change has no choice but to be
placed with it. That is measured where it happens, as the ties of the later change (§4.3): in
Spring an injected dependency is a field, so later code using it is tied to its class. A wired
OfficeFloor function using an existing injected object is not tied by it, since any function can
declare it.

Two conditions of H3 are read on the wiring, as the SinewSlim analysis plan set them (its H4):

- **Growth:** the slope, over the checkpoint index, of the wiring edges added per addition. An
  interval above 0 means the wiring grows faster than the problems, and counts against H3.
- **Concentration:** at the final checkpoint, the share of the configuration's non-blank lines
  held by its largest file. Over 50% counts against H3.

**As built** (`placement_gravity/wiring.py`, 16 November 2026). The configuration is the YAML under
`src/main/resources/officefloor/`. An edge is a `next:` or an entry of an `outputs:` map; a line is
one that is neither blank nor only a comment. Growth is each chain's least-squares slope of the
edges added at each checkpoint over the checkpoint index; over chains, the mean slope with a
percentile bootstrap interval (chains resampled, 10,000 resamples, seed 20261116). Concentration is
each chain's share at its final checkpoint; over chains, the mean share against the 50% limit,
with its interval reported. New injected dependencies are not counted as edges (above).

### 4.6 Amount (conservation check)

Total positions and tokens per arm at each checkpoint, so that H3 is read against the
conservation result: the same amount, placed differently. H3's band is read at the final
checkpoint, averaged within a chain and then over chains, with a percentile bootstrap over chains.

### 4.7 Shape (the competitors of H2b)

The measures the earlier studies and the absorbed drafts used, each read on the **host** an
addition lands in, at *k − 1*, before the addition. A new host has none of them.

| Code | Measure | From |
|---|---|---|
| S1 | **Long:** 26 or more code lines (SinewSlim's lines) | the divergence study's length constant |
| S2 | **Not slimmable:** SinewSlim's conventional reading at the pinned version and its defaults, on both arms | the long-method-slim study; the SinewSlim analysis plan's M1 |
| S3 | **Junction:** the host hands on more data than it receives, *d = out − in > 0*. *in* counts every parameter, as for an ordinary method; *out* counts the arguments it passes on calls to the application's own methods. The injection-aware reading (*in* without injected parameters) is reported beside it | the flow-injection draft's junction |
| S4 | **Complexity outlier:** the host's cognitive complexity, and whether its modified z-score within the checkpoint exceeds 3.5 | the complexity-concentration study |
| S5 | **Concentration:** the host's size and the Gini coefficient of the class's positions over its methods | §4.2 |

S1 to S4 are read conventionally on both arms, so OfficeFloor's functions are priced as if they
were ordinary methods; that is conservative towards OfficeFloor.

**As built** (`Pull --shape`, `placement_gravity/shape.py`, 16 November 2026):

- *k − 1* is the tree of the agent commit's parent, every production method of it, so S4's z-score
  and S5's Gini see the whole checkpoint. An existing host is joined to its version there by its
  before path, type and signature, as matched for the addition (§4.1); a host not found is
  reported.
- S2 counts SinewSlim's `not_slimmable` and `slimmable_with_record` together, the long-method-slim
  study's *stuck*; strict `not_slimmable` and the obstacle are kept beside it. The assessor is
  SinewSlim's defaults, which OfficeFloorSlim's conventional pricing also uses.
- S3's calls are matched to the application's methods by name and arity, lexically, as the ties
  are (§7, *Lexical names*). A call on an object of another type with a matching name counts.
- S3 is conventional, not injection-aware. A wired OfficeFloor function receives only injected
  values: every function is a starting point. Leaving them out of *in* made any call such a function
  made with an argument a junction, so S3 measured whether a function calls anything (corrected
  16 November 2026, after the pilot: 65 of 92 OfficeFloor junctions at cp60 were wired functions).
  This differs from the ties on purpose. Ties ask what pins new code to its place, and an injected
  value pins nothing (§4.3). S3 is the earlier studies' shape measure, read the same way on both
  arms.
- S4 is the complexity-concentration study's own `cognitive.analyze` and `modified_z_scale`
  (pinned at its commit `0f8e654`), over the method's original source lines. When more than half
  the methods tie at the median, that study's mean-absolute-deviation scale applies, and the scale
  used is recorded.

**Reported, not tested:** the drafts' system-level series per arm and checkpoint, the
not-slimmable methods per passing test and the share of complexity held by junctions. They are
solution-only readings, kept so that the absorbed drafts' questions get an answer, and so that their
trajectories can be set beside the per-problem ones.

## 5. Analysis

- **Unit:** an addition run (Q2, H1) or an addition (Q1, Q3, H2), nested in checkpoints nested in
  chains.
- **H1:** a mixed model of log(1 + P) on log(host positions) and checkpoint index, with a random
  intercept for the chain. The slopes are reported with 95% bootstrap intervals over chains.
- **H2:** a negative binomial model of intrusion with a random intercept for the chain. The base
  model holds the problem fixed: the addition's size, its declared crossings, host size and act.
  - **H2a:** pull added to the base model (continuous, and forced/chosen as a reading aid). It is
    supported when the incidence rate ratio per tie has a 95% interval above 1.
  - **H2b:** the shape block S1 to S5 added to the base model with pull. It is supported when every
    shape measure's incidence rate ratio has a 90% interval inside an equivalence bound of 0.8 to
    1.25 (decided 16 November 2026), per standard deviation for continuous measures and present against absent for
    flags. A null is not taken from a non-significant test.
  - **How the shape block enters** (decided 16 November 2026). S4 enters as a level, log(1 + cognitive complexity),
    because cognitive complexity is zero-heavy and the outlier flag then marks any control flow
    (the pilot: 45% of Spring's existing hosts); the flag is reported beside it. A shape measure
    that does not vary in a corpus, with fewer than 10 hosts flagged over all chains of an arm,
    leaves the block for that corpus. It is reported as not testable there, never as meeting the
    bound, and H2b is read on the measures that remain.
  - **Reported beside it:** the shape block in a model *without* the problem terms and pull. This
    shows how much of shape's apparent association comes from leaving the problem out. Each shape
    measure alone, and the change in fit for every block, are also reported.
  - **Junction × arm (secondary, corpus A):** the S3 junction flag, the arm and their interaction,
    added to the model with pull. It asks whether a junction is followed by the same intrusion in
    both arms. In OfficeFloor a function is a starting point: a junction there hands its values on
    from an injection point, and is expected to stay contained to it. The reading is the
    interaction's incidence rate ratio with its 95% interval. An interval below 1 means that
    OfficeFloor's junctions are followed by less intrusion than Spring's; an interval above 1 means
    more. It is repeated with the injection-aware junction. It is not among the confirmatory tests
    and does not change H2's verdict.
- **H3:** the arm term and its interaction with host size in the H1 model, on the paired chains,
  with the amount band (§4.6) and the two wiring conditions (§4.5). The arm's interaction with the
  checkpoint index is reported as the trajectory reading.
- **H3 without the injection rule:** a wired OfficeFloor function's parameters cannot be ties by
  definition, so part of H3 could follow from the rule rather than the code. H3's model is repeated
  with ties counted from locals, fields and methods only, leaving out parameters in both arms. This
  is reported beside H3 and named as the reading that does not depend on the rule.
- **Corpus B:** the H1 and H2 models with a random intercept for the repository. Direction and
  interval only.
- **Multiplicity:** H1–H3 are three confirmatory tests at α = 0.05 each, Holm-corrected. All
  else is descriptive.

**As built** (`analysis/analyse.R` with glmmTMB, `placement_gravity/prepare.py` and
`placement_gravity/verdict.py`, 16 November 2026; R chosen by the author for glmmTMB's negative
binomial mixed model). These details are fixed with the code before any run is read:

- **Each analysis is read on its own** (`runs.yaml`): the petclinic primary, each petclinic
  secondary, and the ui primary. An analysis with fewer than 6 chains in an arm is descriptive only.
- **H1 and H3** are fitted on runs of added logic into **existing** methods: a new method has no
  prior size, so including new methods would make "more ties in bigger hosts" true by
  construction. Gaussian mixed models of log(1 + ties) on log(host positions) and the checkpoint
  index, a random intercept per chain; H3 adds the arm and its interaction with host size (and the
  front end, where the analysis has more than one). Intervals: a cluster bootstrap, chains resampled
  with replacement within arm and the model refitted, **1,000 refits, seed 20261116**. One-sided
  p-values are the bootstrap share on the wrong side of 0, (k + 1) / (n + 1).
- **H2** is a negative binomial (nbinom2) mixed model of later intrusion per problem and host,
  offset by log(later checkpoints), a random intercept per chain. Its base terms are
  log(1 + the problem's positions added), the problem's declared crossings (the checkpoints it
  mutates or crosses), log(1 + host positions), the act (the ui stream only; petclinic has no
  acts), the arm and, where present, the front end. **H2a** is read on every problem and host,
  with a one-sided Wald test; **H2b** on existing hosts with their shape at k − 1, by two one-sided
  Wald tests per shape measure (90% intervals). S4 enters as log(1 + cognitive complexity) and S5
  as the class Gini, both standardised; S1 to S3 as 0/1.
- **The p-value of each hypothesis** for Holm is the larger of its parts: H1, of its two slopes;
  H2, of H2a and every H2b measure's TOST; H3, of the arm term and the interaction. A hypothesis is
  supported when its Holm-adjusted p is at most 0.05 **and** its conditions hold (H3: the amount in
  its band and neither wiring condition against). The verdicts are supported, not supported,
  reversed (an interval wholly on the wrong side), unresolved (H2b: an interval reaching outside
  the bound) or descriptive only.

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
  from the registered analysis. The shape measures (§4.7) were added to it on 16 November 2026:
  on that chain no method was stuck (S2), and the junction share of cognitive complexity rose in
  the OfficeFloor arm and not in Spring (0.33 → 0.31), against the absorbed flow-injection draft's
  P1 direction: 0.30 → 0.42 under the injection-aware reading first built, 0.22 → 0.36 under the
  conventional reading that replaced it. That reading is descriptive, of development data.
- **The models on the development chain** (16 November 2026, after every decision rule and the
  analysis code were committed, `1f1f962` and `7c3c013`). Running steps 2 to 5 end to end on the
  pilot's chain 9, to test them, computed the hypothesis statistics on it, one chain per arm and so
  descriptive only (`results/analysis/pilot/REPORT.md`). Seen: H2a's rate ratio per tie 0.90
  [0.63, 1.30]; with the problem and ties held fixed, the junction 1.11 [0.52, 2.35], cognitive
  complexity 0.54 [0.35, 0.85] and the class Gini 0.44 [0.25, 0.76] (90% intervals); the junction
  without them 5.34 [2.38, 12.0]; junction × arm 0.20 [0.04, 1.01]; H1's slopes 0.025 on host size
  and 0.006 on the checkpoint; H3's arm term −0.64 and interaction 0.13. That chain is excluded
  from every registered analysis, and nothing in the plan was changed after these were seen. The pilot raised six decisions (PILOT.md, *Decisions*), which are
  settled at registration.
- **Not seen.** Pull, placement, containment or intrusion on any other chain, run or repository.
  The petclinic runs have been read for other measures (the conservation paper), never for these.
  None of the ui runs' backend Java has been read for any measure.
- **The absorbed drafts** (§1.1): their hypotheses were laid side by side on 16 November 2026.
  All three predicted the OfficeFloor arm better and none contradicted another; the review found
  that they read OfficeFloor's parameters differently, which is why the reading without the
  injection rule (§5) is added. None of their measures was computed on any run.
- **Expectation.** The author expects H1 and H3 to hold, and expects H2 to be the hardest to
  show, because the intrusion counts per chain may be small. The author also expects H2b to hold:
  that shape outside the problem carries no information beyond it. H2b is the hypothesis this
  expectation could most bias, which is why its criterion is an equivalence bound fixed here. The
  author expects OfficeFloor's junctions to stay contained to their injection point (the junction ×
  arm reading of §5); that reading's direction is stated here, before any intrusion is computed by
  junction.
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
- **Lexical names.** No symbol solver, as in the width harness (decided 16 November 2026). A local that shadows a field
  is already told apart by the method's own variables, and the pilot found no unresolved name in
  418 runs. Names that resolve to nothing are reported per run.
- **Provenance.** Line tracking across moves is imperfect. CodeTracker reports about 99.9%
  method-level precision and recall, but statement-level provenance is weaker. Disagreements
  with `git blame` are reported.
- **Smells born, not grown.** Tufano et al. (2015) find most smells present from a unit's
  creation. So H1's gravity may act mostly at creation (a new method pulled by its parameters,
  §4.3) rather than through accretion. Both are measured, so the data can say which.
- **The cohesion assumption.** It holds by construction only in corpus A, and only if refactoring
  is separated out correctly (§4.1).
- **The problem is fixed, not measured.** The study holds the problem fixed by design (one
  checkpoint, one problem; one stream for both arms). It does not measure how hard a problem is,
  beyond the addition's size and its declared crossings. In corpus B a commit is not one problem,
  so H2b is not read there.
- **Power for H2b.** An equivalence test needs more data than a difference test. If the intervals
  are too wide to fall inside the bound, H2b is reported as unresolved, not as supported.

## 8. Order of work

1. ~~Build the instrument (§4): fixtures with known pull and placement, and tests.~~ Done:
   `instrument/Pull.java`, `placement_gravity/`, `tests/` (RefactoringMiner and CodeTracker not yet
   integrated; PILOT.md, decisions 4 and 5).
2. ~~Run a pilot on **two chains** of one petclinic run, not among those named at registration,
   to check that the measures compute and are not degenerate.~~ Done 15 November 2026:
   `results/pilot/PILOT.md`.
3. Build the shape measures of §4.7 (done 16 November 2026: `tests/test_shape.py`, and the pilot
   chain), the wiring conditions of §4.5 (done 16 November 2026: `tests/test_wiring.py`, and the pilot chain), and the reader for the ui
   stream's declared crossings (done 16 November 2026: `tests/test_stream.py`, and the stream at
   `run-a`), each tested on fixtures and on the pilot chain or the stream only.
4. ~~Settle every design decision~~ (16 November 2026). ~~Build steps 2 to 5~~ (16 November 2026:
   `step2_runs.sh` to `step5_report.sh`, `tests/test_analysis.py`, `analysis/selftest.R`).
5. Register: tag `plan-v1` and push it, before any ui run's backend Java is read.
6. `./step1_setup.sh`, then for corpus A (petclinic, then the ui runs as they finish):
   `./step2_runs.sh`, `./step3_measure.sh`, `./step4_analyse.sh`, `./step5_report.sh`. Analyse
   once; the heads read are recorded in `results/heads.tsv`. Then corpus B (its steps are not yet
   built).
7. Write up, reporting every hypothesis whichever way it falls.

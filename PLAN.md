# Plan: where a new problem's code lands, and whether it had a choice

> **Status: REGISTERED on 16 November 2026, tag `plan-v1`; revised before the start (§9); three revisions, the last on 17 November 2026.** The tag was first pushed on commit
> `4bb8973` and moved the same day, before any run named for analysis was read, to this revision,
> which adds ties to injected dependencies reported apart (§4.3, §5). The instrument is piloted on
> one pair of chains
> (`results/pilot/PILOT.md`); no run named for analysis has been read. What remains open is only
> what needs the data to exist (§3.1a): Run B's ids, Run C's ids when its stack is built, and each
> chain's head when its run is pushed. The ui stacks' backend paths were read from their stack
> declarations (`results/stacks.json`). The literature behind this plan is in
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
- **What pulls is what surrounds the data** (stated 17 November 2026, §9). The data a problem
  needs is the problem's: the same rule needs the same values however it is built. Where a value
  lives is fixed by construction. What is not fixed is **what else is there with it**: the other
  parameters, locals and fields the code has to sit beside in order to reach the one value it
  needs. Those are its **bystanders** (§4.3a). A scope that keeps what each problem leaves behind
  grows heavier, and the next problem that needs any one of its values lands beside all of them.
  That growth is the gravity.

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

- **H1, gravity compounds** (restated 17 November 2026, §9). In the methods arm, the bystanders of
  an addition (§4.3a) rise with the checkpoint index (positive slope, 95% interval above 0).
  - *As first registered:* the addition's ties rise with its host's size and with the checkpoint
    index. That is kept and reported beside it. It was replaced because the ties an addition has
    are largely the data its problem needs, and because nearly every Spring run into an existing
    method already has one (the ceiling the pilot found).
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
- **H3, function injection keeps the space open** (restated 17 November 2026, §9). On the same
  stream, the function arm's bystanders are fewer, and their slope on the checkpoint index is
  flatter, than the methods arm's. (*As first registered:* its ties are lower and their slope on
  host size flatter; kept and reported beside it.) The total amount
  (positions, tokens) of the function arm lies within 0.8 to 1.25 times the methods arm's, the
  band the flow-injection draft took from the conservation study's spread. The coupling that
  leaves the scopes appears as wiring (§4.5) and is reported, not hidden.
- **Q1 is descriptive.** Its expected baseline (Steidl and Deissenboeck 2015) is that most
  growth is new methods. So the share of additions that land in an existing host is reported as
  found, with no direction predicted.
- **Two readings with a stated direction, reported and not among the confirmatory tests** (added
  16 November 2026, §9):
  - **Formation.** Within an arm, for the same problem, a chain that has been forced more so far is
    tied more now, and ends more concentrated (§5, *Formation*). This is the black hole forming,
    read directly and not from a slope.
  - **Review.** Where a placement was chosen, a reviewing agent re-places it; where it was forced,
    it cannot (§5, *Review*).

**What would count against.**

- H1: no slope, or a negative one. The surroundings of a problem's data would then be a constant
  cost of the form, not something that grows: no gravity.
- H2: chosen and forced placements equally intruded on (against H2a), or any shape measure that
  still predicts intrusion with the problem and the ties held fixed (against H2b). The second
  would mean that shape carries information the problem does not, and it is reported as such.
- H3: no difference between the arms in bystanders or in their growth, or an amount outside the band (the difference is then a
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

**Open after registration:** the run ids of Run B, and the commit of each chain's branch that is
read (each chain's head once its run has finished and been pushed). Registration came before Run B
started, so its ids are added by a dated amendment (§9) before any of its backend Java is read.

**Backend paths.** The petclinic layout is production Java under `src/main/java/` and wiring under
`src/main/resources/officefloor/`. The ui stacks declare their own backend paths (`stack.yaml`);
they were read from the stack declarations at each stack's empty base, not from a run, and are
recorded in `results/stacks.json`.

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
declarations, imports and constructor wiring are organisation. So is a **plain accessor**
(17 November 2026, §9): a method whose whole body returns a field of its class, or assigns one of
its parameters to one. It exposes the field for use elsewhere and holds no logic. An accessor that
does anything more is logic: logic has then been put into a data carrier, and it counts. What matters is where the data each
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

**Ties to injected dependencies, reported apart.** A field holding an injected dependency can be
declared by any other class too, so using it may not pin code to this class: the same reasoning
that makes an injected parameter not a tie. A field counts as injected when it is annotated for injection (`@Autowired`,
`@Inject`, `@Resource`, `@Value`, OfficeFloor's `@Dependency`); when, in a container-managed class
(`@Component`, `@Service`, `@Repository`, `@Controller`, `@RestController`, `@Configuration`,
`@ControllerAdvice`, `@RestControllerAdvice`), it is assigned from a constructor parameter or filled
by Lombok's `@RequiredArgsConstructor` (final fields) or `@AllArgsConstructor`; or when it is assigned
from the parameter of a method annotated for injection (setter injection). A constructor parameter of
a class the container does not manage is data, and a constant (`static final`) still ties.

- **The primary measure keeps them:** an injected field is a class tie, and H1 to H3 are read on
  all ties.
- **Reported beside it** (§5): H1, at method level and at class level, H3 and H2a, each with the
  ties to injected dependencies left out (`tie_no_injected`, `tie_class_no_injected`).

**Pull is graded by where the value comes from** (stated 16 November 2026, §9). The expected
order, from the least pull to the most:

1. an **injected parameter** of a wired function: no pull, as any function placed anywhere can
   declare it (not a tie);
2. an **injected dependency** held in a field: a pull by convenience, as another class could declare
   it too, but the code is easiest to place where it already is (a tie, reported apart);
3. a **value bound to the control flow**: the request object, a parameter or a local of the host
   method. It exists only there, so code that uses it has to be placed there or be handed it (a
   tie).

Spring's handler receives the request object on its control flow, so its additions start with the
strongest pull; OfficeFloor's functions receive theirs by injection. The primary measure counts 2
and 3 alike. The readings without injected dependencies (above) and without parameters (§5) show
how much of each result rests on each grade.

**A tie shows pull, not the absence of an alternative.** It is evidence that the placement was
held, not proof that no other placement existed. Two readings check it: the spread of placements
over the chains at one checkpoint (§5, *Choice at a checkpoint*), and whether a reviewing agent
moves the code (§5, *Review*).

Ties are related to Feature Envy turned inwards (Tsantalis and Chatzigeorgiou 2009). Their metric
finds a method drawn towards *another* class's data, as a snapshot recommendation. Ties measure an
addition held by its *own* host's pre-existing data, at the commit where it is placed.

**Forced / chosen:** a run is forced when its ties are 1 or more, and chosen otherwise. The cuts
2, 3 and 4 are reported beside it. Because the pilot finds 93% of Spring's runs into existing
methods forced at 1, H2 is tested on the tie count, with the cut as a reading aid. H1 and H3 are
read on the bystanders (§4.3a). The tie-based readings of H1 as first registered (at method level
in both arms, and at class level in Spring: class ties against the class's size) are reported.

### 4.3a Bystanders (H1, H3), the measure of what gravity gathers

Added 17 November 2026 (§9). For each run of added logic, at the point where it starts, the
pre-existing values **visible** there are split in two:

- **Needed:** those the run's lines use. The problem sets these.
- **Bystanders:** those it does not use. The placement sets these: they are what the code has to
  sit beside to reach what it needed.

**What is visible.** Counted the same way in both arms; nothing is left out by a rule about
injection.

- **Method values:** the host method's pre-existing parameters, injected or not, and its
  pre-existing locals whose declaration comes before the run and whose scope encloses it. A local
  declared inside an earlier block is not visible after the block, so a long method made of
  self-contained blocks does not gather bystanders by its length.
- **Class fields** of the host's class as it was before the change, in three kinds:
  - **state:** fields that are neither constants nor injected;
  - **injected dependencies:** as §4.3 defines them;
  - **constants** (`static final`).
- **Utilities** (loggers) are not counted; they are reported apart, as for the ties.
- A new method has no pre-existing method values, but it sees its class's fields. A method of a new
  class sees nothing that existed before.

**The count.** A run's bystanders are its visible method values and its class's fields of all three
kinds, less those it uses.

**Constants count** (decided by the author, 17 November 2026). A constant is the thing that is not
to be duplicated: code that needs it comes to where it is, or the constant has to be moved out to
somewhere shared. So a constant pulls, and a class that keeps each rule's constants gathers them
for every later rule to sit beside. On the development chain the growth of Spring's bystanders is
mostly constants (§6), which is why the count without them is reported beside it.

**Only where existing data is used** (decided by the author, 17 November 2026). The bystanders are
read on the runs that **need at least one pre-existing value** (constants included). Code that
needs nothing that was there was not pulled to its place: it could have gone anywhere. The share of
such free runs is reported per arm. Plain accessors, being organisation (§4.3), are not runs at
all.

**Reported beside it:**

- the two levels separately: **method bystanders** and **class bystanders**;
- the count without injected dependencies (the grade of pull by convenience, §4.3);
- the count without constants;
- the **needed** values, per arm. They are expected to be the same in both arms, since the stream
  is the same; a difference would mean the arms are not solving the same problem with the same data;
- the share of free runs, per arm.

**Unit.** Every run of added logic that needs a pre-existing value, in new hosts and existing ones
alike (moved code left out). Unlike the ties, the measure is defined for a new method, which sees
its class's fields.

**Two links, reported** (not confirmatory):

- **Accretion:** per addition and arm, the fields it adds to classes that already existed. This is
  the mass an addition leaves behind.
- **Capture:** for the same problem, is a chain whose heaviest class holds more more likely to
  place the addition in an existing host? Per addition, the share of its positions landing in
  existing hosts, on the fields (of all three kinds) of the chain's heaviest class at *k* − 1, with
  the checkpoint's intercept. Predicted: positive in the methods arm.

Bystanders are related to the scope-width measures of the long-method-slim study's step 7 (live
width along a method). They differ in being read at the point where a problem's code lands, on
what that code did not need, and in counting the class as well as the method.

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

**Revised before the start** (16 November 2026, §9): **intrusion is read on the problem's own
lines.** As first built, a later checkpoint counted as touching *p* when it changed the host method
anywhere. That makes intrusion a property of the host: every problem placed in a busy method gets
that method's later traffic, whatever its own code is (on the development chain one Spring method
received 26 problems, and all of Spring's intrusions were in methods holding several problems). The
petclinic stream puts every rule on one endpoint, so there the traffic of the handler is set by
the stream. The text above always said *p*'s positions; the build now follows it:

- ***p*'s lines** in a host are the logic lines its addition placed there. They are followed from
  checkpoint to checkpoint by the instrument's diff: an unchanged line keeps its owner, moved code
  carries its owner with it, and an edited line keeps its owner and gains the editor's, since both
  problems' code is then on it.
- **A later checkpoint *j* touches *p*** in that host when its change edits or removes one of *p*'s
  lines, or inserts a logic line between the first and the last of *p*'s lines still present.
- The three-way split is unchanged: declared, crossed, or intrusion. **Intrusion on *p*'s own
  lines is the outcome of H2.**
- **Reported beside it:** the host-level count as first built (any later change to the host), so the
  difference the definition makes can be seen.
- Following lines is weaker than following methods (§7, *Provenance*). The share of *p*'s lines
  lost track of (neither present, nor seen removed or moved) is reported per arm.

**As built** (`placement_gravity/lines.py`, `tests/test_lines.py`, 16 November 2026). The
instrument gives, for every changed method, each position's kept-from position, its kind (kept,
added logic, moved, organisation) and its text hash. An owner is the checkpoint and the host it
placed the line in, so a line moved to another method still belongs to the problem and host that
placed it. Within a changed stretch, the removed lines are paired in order with the added logic
lines: a pair is an edit; a removed line left over is a removal; an added line left over is an
insertion. A removed line whose text is a moved line's elsewhere in the checkpoint is a move, not a
removal, and is not a touch. A method renamed, moved or re-signatured without other change carries
its lines to its new name. A line is lost when its method's stored length no longer matches, when
moved code's destination is not found, or when its method is not in the last tree and was not seen
removed.

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

**Revised before the start** (16 November 2026, §9): **the band is read on the amount added**, the
positions at the final checkpoint less those of the chain's base (`base_ref`), not on the total.
The petclinic arms start from two conversions of one application that differ in size (942 and 745
positions at cp1 of the development chain), so a ratio of totals reports the starting code as much
as the agent's. The ui stacks start empty, so there the two are the same. The ratio of totals is
reported beside it.

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
- **The problem is held fixed by its identity** (revised before the start, 16 November 2026, §9).
  Every checkpoint is one problem, solved once by every chain of both arms. The H1, H2 and H3
  models therefore carry a **random intercept for the checkpoint**, crossed with the chain's. A
  comparison is then between placements of the same problem, and the size and the declared
  crossings are no longer the only stand-ins for it. A model that does not converge with the
  checkpoint intercept is refitted without it, and the report says so.
- **H1** (restated 17 November 2026, §9): a mixed model of log(1 + bystanders) per run of added
  logic that needs a pre-existing value (§4.3a), on the checkpoint index, in the methods arm, with random intercepts for the chain and the
  checkpoint. The slope is reported with a 95% bootstrap interval over chains. Host size is not in
  the model: a larger method has more values by construction, so a slope on it would not be
  evidence.
  - **Reported beside it:** the same model on method bystanders and on class bystanders, without
    injected dependencies, and without constants; and H1 as first registered, log(1 + ties) on
    log(host positions) and the checkpoint index, on runs into existing methods.
- **H2:** a negative binomial model of intrusion with a random intercept for the chain. The base
  model holds the problem fixed: the checkpoint's intercept, the addition's size, its declared
  crossings, host size, whether the host is new, and act. Intrusion is read on the problem's own
  lines (§4.4). A new host has almost no ties and a different later life from an existing one (on
  the development chain, Spring's new hosts averaged 0.31 ties and existing ones 1.81), so without
  the new-host term that contrast alone could carry H2a.
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
- **H3** (restated 17 November 2026, §9): the arm term and its interaction with the checkpoint
  index in the H1 model, on the paired chains, with the amount band (§4.6) and the two wiring
  conditions (§4.5). The checkpoint index is centred at the middle of the stream, so the arm term
  is the difference between the arms half-way through. Supported when both are below 0: the
  function arm has fewer bystanders, and they grow more slowly.
  - **Reported beside it:** H3 as first registered, on the ties: the arm term and its interaction
    with host size, as below.
  - **Host size is centred, in the tie-based reading** (16 November 2026, §9): log(host positions)
    less its mean over the rows of the model, both arms together. With an interaction in the model,
    the arm term is the difference between the arms where the centred host size is 0. Uncentred,
    that is a host of one position, which no host is. Centred, it is the difference at a typical
    host. The difference is also reported at hosts of 10, 25 and 50 positions.
- **H3 without the injection rule:** bystanders count injected parameters like any other, so the
  restated H3 does not rest on the rule that an injected parameter is not a tie. The tie-based
  reading does: a wired OfficeFloor function's parameters cannot be ties by definition. It is
  therefore repeated with ties counted from locals, fields and methods only, leaving out parameters
  in both arms, and reported.
- **Without injected dependencies** (reported, §4.3): H1 at method and class level, H3 and H2a,
  each with ties to injected dependencies left out. These do not change any verdict.
- **Choice at a checkpoint** (reported; added 16 November 2026, §9). Per checkpoint and arm, over
  the chains: the share of chains that placed any of the addition in an existing host, the number
  of distinct hosts the chains used between them, and the standard deviation of the ties per
  addition. A checkpoint where every chain made the same placement with the same ties left no
  choice; one where the chains differ did.
- **Formation** (reported with a stated direction, not confirmatory; added 16 November 2026, §9).
  Read within each arm, never across arms.
  - **Lagged:** the H1 model, with its checkpoint intercept, and one more term: the chain's mean
    ties per run over all its checkpoints before *k*. Predicted: positive in the methods arm. For
    the same problem, a chain that has been forced more so far is tied more now.
  - **Where it ends:** over the chains of an arm, Spearman's correlation between the mean ties per
    run in the first third of the stream and the share of the tree's positions held by its largest
    method at the final checkpoint. Predicted: positive in the methods arm. With about nine chains
    this is a direction with a wide interval (bootstrap over chains), and is reported as that.
  - The function arm is reported the same way. The expectation is that there is little to form:
    a weaker or absent relation.
  - Both are observational: a chain is not assigned its early placements. They show whether the
    path exists, not that the early placement caused the later one.
- **Review** (reported with a stated direction, not confirmatory; added 16 November 2026, §9). The
  `reviewed` run (`blind-202609290948`) is set against the primary just-solve run, per arm. This is
  the one reading that sets two conditions side by side; neither run's hypothesis tests are pooled.
  - Per checkpoint *k*: *T* is the mean ties per run of the just-solve chains; *D* is the absolute
    difference between the two conditions in the share of the addition's positions that land in
    existing hosts, each averaged over its chains.
  - Predicted: Spearman's correlation of *T* and *D* over the checkpoints is negative. The review
    changes the placement where the ties are few, and leaves it where they are many. No direction is
    predicted for *which way* the review moves a placement: the conservation paper found it
    consolidating OfficeFloor's pipeline (§6).
  - A correlation of zero or above counts against reading ties as the absence of choice.
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
  index, random intercepts per chain and per checkpoint; H3 adds the arm and its interaction with host
  size, centred (and the front end, where the analysis has more than one). Intervals: a cluster bootstrap, chains resampled
  with replacement within arm and the model refitted, **1,000 refits, seed 20261116**. One-sided
  p-values are the bootstrap share on the wrong side of 0, (k + 1) / (n + 1).
- **H2** is a negative binomial (nbinom2) mixed model of later intrusion per problem and host,
  on its own lines (§4.4), offset by log(later checkpoints), random intercepts per chain and per
  checkpoint. Its base terms are log(1 + the problem's positions added), the problem's declared
  crossings (the checkpoints it mutates or crosses), log(1 + host positions), whether the host is
  new, the act (the ui stream only; petclinic has no
  acts), the arm and, where present, the front end. **H2a** is read on every problem and host,
  with a one-sided Wald test; **H2b** on existing hosts with their shape at k − 1, by two one-sided
  Wald tests per shape measure (90% intervals). S4 enters as log(1 + cognitive complexity) and S5
  as the class Gini, both standardised; S1 to S3 as 0/1.
- **The p-value of each hypothesis** for Holm is the larger of its parts: H1, of its two slopes
  (as restated, its one slope);
  H2, of H2a and every H2b measure's TOST; H3, of the arm term and the interaction. A hypothesis is
  supported when its Holm-adjusted p is at most 0.05 **and** its conditions hold (H3: the amount in
  its band and neither wiring condition against). The verdicts are supported, not supported,
  reversed (an interval wholly on the wrong side), unresolved (H2b: an interval reaching outside
  the bound) or descriptive only.
- **The revisions of 16 November 2026** (§9) are built: the checkpoint intercept, the centred host
  size, the new-host term and the lagged formation term in `analysis/analyse.R` (its self-test
  simulates a level per checkpoint and recovers each effect); intrusion on a problem's own lines in
  `placement_gravity/lines.py`; the amount added in `prepare.amount`; the choice, formation and
  review readings in `placement_gravity/readings.py`. Each has fixtures with known answers.
  - *The checkpoint intercept's fallback:* a model is refitted without it when the fit does not
    converge or its Hessian is not positive definite; each report lists which models carry it.
  - *The lagged term* counts every run of added logic (new and existing hosts, moved code left
    out) at the chain's earlier checkpoints.
  - *Choice:* a checkpoint "left no choice" when every chain has the same ties and all are on the
    same side of new or existing host.
  - *Review:* its interval resamples the chains of each condition (2,000 resamples, seed 20261116);
    the formation correlation's interval resamples chains (10,000). Either is given only with four
    or more chains.
- **The bystanders** (§4.3a) and H1 and H3 as restated on 17 November 2026 are built: the visible
  and needed values per run and the fields a class is left with (`instrument/Pull.java`,
  `tests/test_bystanders.py`); `by.csv` and `capture.csv` (`prepare.py`); the models
  (`analysis/analyse.R`, whose self-test simulates bystanders rising in one arm and recovers H1,
  H3, the equal needs and capture); the verdicts (`verdict.py`: H1 on its one slope).
  - *Visible:* a local is visible where a run starts when it is declared on an earlier line and its
    nearest enclosing block, loop, try, switch entry or lambda encloses that line.
  - *H3's centre* is the middle of the stream, (checkpoints + 1) / 2.
  - *Capture* is a Gaussian mixed model of the share on log(1 + the heaviest class's fields), per
    arm, with Wald intervals.

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
  from every registered analysis, and nothing in the plan was changed after these were seen.
- **Ties to injected dependencies** (§4.3, added 16 November 2026 after `plan-v1` was first tagged,
  and before any run named for analysis was read; the tag was moved to include it), on the
  development chain only: of Spring's 74 runs
  into existing methods, 12 used an injected dependency; leaving those ties out, the runs with a
  class tie fall from 20 to 10 and the forced runs from 71 to 67. Every class tie to `clinicService`
  and `ownerMapper`, the controller's constructor-injected dependencies, is counted as injected.
  OfficeFloor's runs into existing methods used none. The pilot raised six decisions (PILOT.md, *Decisions*), which are
  settled at registration.
- **The review before the start** (16 November 2026, on the development chain only, after
  `plan-v1` and before any run named for analysis was read). Seen, and the reason for the revisions
  of §9: Spring's 396 host-level intrusions all fall in methods holding several problems, one method
  holding 26; Spring's new hosts average 0.31 ties and 0.005 intrusions per later checkpoint, its
  existing hosts 1.81 and 0.24; H2a's model refitted with an intercept per host gave a host standard
  deviation of 2.7 and took the host-size coefficient from 1.27 to −0.07 (its standard errors did
  not compute); a simulation of the H2a test under no effect, with that dependence between rows,
  did not reject too often (the standard deviation of z was 0.82); with only Run A, the ui model
  drops the front end and the arm term carries it. Nothing was computed with the checkpoint
  intercept, on a problem's own lines, with the centred host size, or for the formation and review
  readings.
- **The revised steps on the development chain** (16 November 2026, after the revisions of §9 were
  written into this plan and built; one chain per arm, descriptive only,
  `results/analysis/pilot/REPORT.md`). Seen: on a problem's own lines Spring has 23 intrusions and
  OfficeFloor 26, where the host-level count had 396 and 44; no line was lost track of (569 and 616
  placed); H2a's rate ratio per tie 1.17 [0.76, 1.81]; the junction 0.52 [0.17, 1.63], cognitive
  complexity 1.59 [0.77, 3.27] and the class Gini 0.32 [0.13, 0.82] (90% intervals); H1's slopes
  0.030 and 0.006; H3's arm term −0.40 at the centre (a host of 7.3 positions) and interaction
  0.046, the arm difference −0.39, −0.35 and −0.32 at 10, 25 and 50 positions; without parameter
  ties −0.20 [−0.37, −0.04]; the amount added 1.08 (totals 0.88); the lagged formation term −0.36
  [−2.16, 1.44] in Spring. With one chain per arm H2a's model fell back to no checkpoint
  intercept. Nothing in the plan was changed after these were seen.
- **Bystanders on the development chain** (17 November 2026; a scratch copy of the instrument, one
  chain per arm). **H1 and H3 were restated after these were seen**, so on this chain they are
  not predictions; the chain is excluded from every registered analysis. Fields were counted
  without telling constants apart. Seen:
  - runs into existing methods need the same in both arms (1.43 values in Spring, 1.41 in
    OfficeFloor) and have 11.9 bystanders in Spring against 1.4 in OfficeFloor;
  - over the thirds of the stream Spring's bystanders are 7.2, 11.1 and 14.9, OfficeFloor's 1.7,
    1.0 and 1.4; over every run, new hosts included, 4.2, 7.8 and 11.5 against 1.6, 2.4 and 2.8;
  - Spring's rise is in the class's fields (4.6 to 11.4), not in the method's values (2.6 to 3.5);
    about three quarters of a method's values are visible where a run starts;
  - a method created at checkpoint 56 in Spring's controller, of 10 positions, sees 17 fields.
  Nothing was computed on accretion, on capture, or with the fields split by kind.
- **Bystanders as first drafted, built and run on the development chain** (17 November 2026):
  every run, new hosts included, constants not counted. Seen: 4.7 bystanders per run in Spring
  against 2.2 in OfficeFloor, rising in both (3.4, 4.6, 6.0 against 1.6, 2.3, 2.7), H3's
  interaction about zero. Two causes were found. Spring's rise in the scratch figures was mostly
  constants gathering in the controller (runs into existing methods: 5.9, 6.6, 7.3 without them,
  7.2, 11.1, 14.9 with). And new methods brought in the entity's accessors, which see every field
  of `Owner` in both arms and need nothing that was there. **The two decisions of §4.3a (constants
  count; only runs that use existing data) and the accessor rule of §4.3 were made by the author
  after seeing this**, each on its own argument, recorded there.
- **Bystanders as decided, on the development chain** (17 November 2026,
  `results/analysis/pilot/REPORT.md`; one chain per arm, descriptive only). Seen: 91 of Spring's
  162 runs and 56 of OfficeFloor's 168 need a pre-existing value; those need the same in both arms
  (1.41 and 1.55; the arm term 0.03 [−0.05, 0.11]); bystanders 10.9 in Spring (method 2.6, class
  8.3) against 1.2 in OfficeFloor; over the thirds 5.9, 10.2, 14.6 against 1.5, 0.9, 1.2; H1's
  slope 0.015, and 0.003 [−0.005, 0.012] without constants; H3's arm term −1.59 and interaction
  −0.017. So on this chain the level differs with or without constants, and the growth is the
  constants. Fields left in existing classes per addition: 0.61 in Spring, 0.46 in OfficeFloor.
  Capture: 0.32 [0.06, 0.57] in Spring and 0.22 [0.02, 0.41] in OfficeFloor; with one chain per
  arm the heaviest class only grows with the checkpoint, so this cannot yet be told from time.
  Nothing in the plan was changed after these were seen.
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
- **Lines, not methods, for intrusion.** Since the revision of §4.4 the outcome of H2 rests on
  following a problem's own lines, which is the weaker provenance. The host-level count is reported
  beside it, and the share of lines lost track of per arm.
- **Pull is not proof of force.** A tie shows that the code used something that was already there.
  It does not show that no other placement existed (§4.3). The choice-at-a-checkpoint and review
  readings are the checks, and both are indirect.
- **H1 and H3 were shaped on the development chain.** The bystander measure and the direction of
  both hypotheses were settled after seeing it on chain 9 (§6). That chain is excluded, and the
  registered chains had not been read, but the hypotheses are no longer blind to this run's
  general shape: the other chains of the same run are likely to resemble it. The replication on
  the ui stream, a different application, is the stronger test.
- **Growth is not gravity by itself.** A codebase that grows has more of everything. H1's slope
  is read against the function arm, which grows by about the same amount on the same stream
  (§4.6): bystanders that rise in one arm and not in the other are the form's, not the growth's.
  H1 alone, without H3, would not show that.
- **Visible is not used, and not harmful by itself.** A bystander is exposure: something the code
  could read or disturb. Whether exposure does harm is H2's question, and the harness's own signal
  of a rule broken that was not meant to change is the outcome that would answer it most directly
  (not read by this plan).
- **One stream per corpus.** The intervals are over chains: they say what this agent does on this
  stream again, not what happens on other problems. The petclinic stream puts every rule on one
  endpoint. The ui stream is the second set of problems; corpus B the third.
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
   `instrument/Pull.java`, `placement_gravity/`, `tests/`, with RefactoringMiner and CodeTracker
   integrated (`refactor/`; PILOT.md, decisions 4 and 5).
2. ~~Run a pilot on **two chains** of one petclinic run, not among those named at registration,
   to check that the measures compute and are not degenerate.~~ Done 15 November 2026:
   `results/pilot/PILOT.md`.
3. Build the shape measures of §4.7 (done 16 November 2026: `tests/test_shape.py`, and the pilot
   chain), the wiring conditions of §4.5 (done 16 November 2026: `tests/test_wiring.py`, and the pilot chain), and the reader for the ui
   stream's declared crossings (done 16 November 2026: `tests/test_stream.py`, and the stream at
   `run-a`), each tested on fixtures and on the pilot chain or the stream only.
4. ~~Settle every design decision~~ (16 November 2026). ~~Build steps 2 to 5~~ (16 November 2026:
   `step2_runs.sh` to `step5_report.sh`, `tests/test_analysis.py`, `analysis/selftest.R`).
5. Register: tag `plan-v1` and push it, before any ui run's backend Java is read. Done 16 November
   2026. The revisions of §9 were then built (16 November 2026) and run on the development chain.
   Committed, and the tag set on them (`f780a5a`). The bystanders (§4.3a) and H1 and H3 as restated
   on 17 November 2026 were then built and run on the development chain, committed, and the tag
   `plan-v1` set on them.
6. `./step1_setup.sh`, then for corpus A (petclinic, then the ui runs as they finish):
   `./step2_runs.sh`, `./step3_measure.sh`, `./step4_analyse.sh`, `./step5_report.sh`. Analyse
   once; the heads read are recorded in `results/heads.tsv`. Then corpus B (its steps are not yet
   built).
7. Write up, reporting every hypothesis whichever way it falls.

## 9. Revisions and amendments

**Before the start.** The experiment starts when the first run named for analysis is read
(`results/heads.tsv` holds a row that is not the development chain). Until then a change is a
**revision of `plan-v1`**: it is dated and listed below with what had been seen when it was made,
and the tag `plan-v1` is set on the revised plan and code before the start.

**After the start.** The tag `plan-v1` is not moved. A change to this plan, to `runs.yaml`, to the
instrument or to the analysis code is a **dated amendment**: listed here with its date, what
changed and why, and what had been read, and tagged `plan-v1.1`, `plan-v1.2` and so on. An
amendment that touches a measure, a model or a decision rule is made before the runs it applies to
are read.

**Always.** Steps 2 to 4 refuse to read a run while a registered file has uncommitted changes, and
every report lists the registered files that differ from `plan-v1` (`runs.drift`).

**If a fault is found after a run is read.** The fault, the fix and the date are recorded here as
an amendment. The affected analyses are run again, and the report gives the results before and
after the fix side by side. A verdict that changes is reported as changed, with both.

### Revisions before the start

**16 November 2026, first.** Ties to injected dependencies reported apart (§4.3, §5); the tag moved
from `4bb8973` to `4ec41dd`.

**16 November 2026, second: after a review of the plan.** Nothing but the development chain had
been read; what the review computed on it is in §6. The tag moved from `4ec41dd` to the commit that
holds this revision. The changes:

| | Change | Where | Why |
|---|---|---|---|
| 1 | A random intercept for the checkpoint in the H1, H2 and H3 models | §5 | The problem was held fixed only by its size and declared crossings; its identity is known and replicated over the chains |
| 2 | Intrusion read on the problem's own lines; the host-level count reported beside it | §4.4, §5 | As built it counted any later change to the host method, a property of the host and, in petclinic, of the stream |
| 3 | Whether the host is new, in H2's base model | §5 | New hosts have almost no ties and a different later life, so that contrast alone could carry H2a |
| 4 | Host size centred in H3's model; the arm difference also reported at 10, 25 and 50 positions | §5 | Uncentred, the arm term was the difference at a host of one position |
| 5 | H3's amount band read on the amount added since the base | §4.6 | The petclinic arms start from conversions of different size; no change for the ui stacks, which start empty |
| 6 | Pull stated as graded: injected parameter, injected dependency, value bound to the control flow; a tie stated as evidence of pull, not proof of force | §4.3, §7 | To say what the measure claims |
| 7 | Three reported readings: choice at a checkpoint, formation, review | §2, §5 | The same problem at every checkpoint lets the choice, and what follows from it, be read directly |
| 8 | Editorial: §3.1a's "[DECIDE] before registration", §8 step 1, `README.md` | | Stale text |
| 9 | The guard refuses uncommitted changes to registered files; reports list the files changed since the tag | `runs.py`, `report.py` | So a change after registration cannot pass unseen |
| 10 | A renamed file's before version is read under its own path | `Pull.java`, `chain.py` | It was read under the new path, so RefactoringMiner's hints and the shape at *k* − 1 could miss it |
| 11 | A tree with no production Java (a ui stack's empty base) is read as empty | `chain.extract` | Reading it failed |

In that revision the hypotheses H1 to H3, their directions, their thresholds, the equivalence
bound, the runs read and the Holm correction were unchanged.

**17 November 2026, third: H1 and H3 restated on bystanders.** Nothing but the development chain
had been read; what was seen on it is in §6. This revision changes two hypotheses, and it was made
after seeing the measure on the development chain (§7).

| | Change | Where | Why |
|---|---|---|---|
| 12 | A new measure, bystanders: the pre-existing values visible where a run starts that it does not use, at method and class level | §4.3a | Ties count the data a problem needs, which the problem sets. What surrounds that data is what the placement sets, and what grows |
| 13 | H1 restated: bystanders rise with the checkpoint index in the methods arm. H1 as first registered (ties on host size and checkpoint) is reported | §2, §5 | The tie-based slope was at a ceiling in Spring and measured the problem's use of data |
| 14 | H3 restated: the function arm's bystanders are fewer and grow more slowly. H3 as first registered (ties, slope on host size) is reported | §2, §5 | So that H3 is read on the same measure as H1; and bystanders count injected parameters, so H3 no longer rests on the injection rule |
| 15 | Two reported readings: accretion and capture | §4.3a | The two links of compounding, each read on its own |
| 16 | Constants count as bystanders; the count without them is reported | §4.3a | A constant is not to be duplicated, so code that needs it comes to it. Decided after the development chain showed that Spring's growth is mostly constants (§6) |
| 17 | Bystanders are read only on runs that use at least one pre-existing value; the share of free runs is reported | §4.3a | Code that needs nothing that was there was not pulled anywhere. Decided after the development chain showed new entity accessors diluting both arms (§6) |
| 18 | A plain accessor is organisation, not logic | §4.3 | It exposes a field and holds no logic. This also removes accessor lines from the ties and from a problem's own lines |

H2, the equivalence bound, the amount band, the wiring conditions, the runs read and the Holm
correction over three hypotheses are unchanged. The tag `plan-v1` moved from `f780a5a` to the
commit that holds this revision, built.

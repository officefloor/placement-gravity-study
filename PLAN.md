# Plan: where a new problem's code lands, and whether it had a choice

> **Status: NOT YET REGISTERED. The tag `plan-v1` was withdrawn on 17 November 2026, before any
> run named for analysis was read, while the hypotheses are worked out on the development chain
> (§9, five revisions so far). It will be set again when that work is done; until then only the
> development chain can be read.** As first registered, on 16 November 2026: the tag was first pushed on commit
> `4bb8973` and moved the same day, before any run named for analysis was read, to this revision,
> which adds bindings to injected dependencies reported apart (§4.3, §5). The instrument is piloted on
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
  concentration because its data binds it there, not because the problem belongs there. Each
  forced placement widens the host, and a wider host pulls the next addition in.
- **What pulls is what surrounds the data** (stated 17 November 2026, §9). The data a problem
  needs is the problem's: the same rule needs the same values however it is built. Where a value
  lives is fixed by construction. What is not fixed is **what else is there with it**: the other
  parameters, locals and fields the code has to sit beside in order to reach the one value it
  needs. Those are its **bystanders** (§4.3a). A scope that keeps what each problem leaves behind
  grows heavier, and the next problem that needs any one of its values lands beside all of them.
  That growth is the gravity.
  *Gravity* is also a word of Pescio's (*Notes on Software Design*, 2008–2012, chapters on mass,
  gravity and inertia in a "physics of software"; unrefereed essays, not measured), for the pull
  that gathers things in a design. Those chapters have not been read, so how far his sense and
  this study's overlap is not known; **check before quoting**. This study's sense is the one above,
  measured per addition (LITERATURE.md §10, the novelty check of 20 November 2026).
- **Core and periphery** (stated 19 November 2026, §9). The last sentence was the reading until
  then. On the development chain the data that gathers is mostly not what later code comes for
  (§6): later code comes for a few values that code there was already bound to, the place's
  **core**, and the rest, the **periphery**, is what it then has to sit beside. So the pull is
  the core's (H2), the growth is the periphery's and is its cost (H1), and a form that hands each
  function its own data forms no core (H4).

That shared data gathers faster than code is known in aggregate: across versions of the Linux
kernel, common coupling to global data grew far faster than the code did (Schach et al. 2002; Yu
et al. 2004), and files with more references to global data changed more (Selby et al. 2007).
Those are counts over a whole system or file. This study reads the same thing where one problem's
code lands: what was already visible there, split into what the code used and what it did not
(§4.3a), and which of the two later code is then bound to (H2).

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
placement, not concentration as such, is what does the harm. As the hypotheses now stand (§2, §9),
the part of that claim tested is the mechanism: a place gathers data (H1), and later code comes
there for the few values earlier code was bound to, its core, not for the rest that gathered (H2). The study measures what is drawn in, not the harm
done.

**The problem has to be held fixed.** The earlier studies, like most of the code-smell literature,
judge the shape of a solution without the problem it solves: a long method, a high complexity or a
junction is read as bad whatever it is for. If the problem dictates the size, a shape measured
across different problems reports the problems as much as the code. At best it finds a consistency
in the problems that happened to be sampled; at worst it is noise. The concern grows with AI
assistants, which may be given larger and harder problems, so a change in the shape of their code
need not mean a change in how well it is written. This study therefore reads shape only where the
problem is fixed: one checkpoint is one problem, and both arms solve the same stream. It also
**tests** the claim rather than assuming it. H3 asks whether the shape measures the earlier studies
used predict later intrusion once the problem, the bindings and the bystanders are held fixed (§2, §4.7).

### 1.1 What this plan absorbs (16 November 2026)

Three plans read the same runs with measures of the solution's shape. None has read a run. Two are
unregistered drafts. The SinewSlim analysis plan's file says it is a draft, but its rule makes
registration the commit of the file, and that commit was pushed on 31 October 2026 with a message
calling it registered; it is therefore withdrawn by a dated amendment on its own branch, not
simply closed. Their measures enter this plan as the shape competitors of H3, or as checks, so one
registration covers them:

- **The flow-injection-containment draft** (`flow-injection-containment-experiment`, 20 October
  2026; closed by its own commit). Its junction share (P1) becomes the host-level junction measure
  of §4.7 (since 17 November 2026 a sinew measure, read apart from H3). Its conservation check (P2) is §4.6, with its band. Its trajectory (P5) is H1's checkpoint
  slope, read per arm. Its god-unit count (P3) and its gated-condition lever (P4) are dropped.
- **The ui harness's SinewSlim analysis plan** (branch `sinewslim-analysis-plan`, 31 October 2026).
  Its not-slimmable methods (H1) become a measure of §4.7 (since 17 November 2026 a sinew measure,
  read apart from H3). Its mechanism (H2, behaviour
  added inside existing methods) is what Q1 and the bindings measure. Its wiring test (H4) becomes H4's
  wiring condition. Its go/no-go bar for OfficeFloorSlim is a product decision and stays in the
  harness, outside this study.
- **The sinew-identification study** (on hold since 19 October 2026; closed by its own commit). Its
  restated sinew, data coupled to the control flow, is what the bindings measure at the commit where
  code is placed.

The injected-coupling measurement study existed to validate the flow-injection draft's coupling
instrument. This plan uses the simpler rule of §4.3 (a wired OfficeFloor function's parameters are
injected). That study is shelved; if it is ever completed, it is a sensitivity reading here, not a
gate.

**What stays separate** (recorded 18 November 2026, from the author's decisions of 16 November):
the follow-ons of `long-method-slim-study` (its third study is to be reframed as placement per
problem, and is not part of this plan); `test-fidelity-long-run`; and the ui harness itself, which
is this study's source of data and is run on the study laptop. The SinewSlim analysis plan's own
branch still has to be given its run ids and its SinewSlim pin before its first scan; that is the
harness's to do, not this plan's.

## 2. Questions and hypotheses

- **Q1 (description).** For each new problem: does its code go into new units or into existing
  ones, how far is it dispersed, and how large were the hosts it landed in?
- **Q2 (gravity).** How strongly does each addition depend on state that already existed in its
  host (its **pull**, §4)? Does pull grow as hosts grow and the system ages?
- **Q3 (consequence).** Where a problem's code was bound to a place, which of the data there are
  later changes to *other* problems bound to when they arrive: the values it was bound to, or the
  rest that lay there? (As first asked: are forced
  placements followed by more tangling than chosen placements of the same size? Reported.)
- **Q4 (form).** For the same stream of problems, is pull lower and flatter under function
  injection than under methods, while the amount stays about the same?

Hypotheses. Directions and thresholds are fixed now (thresholds decided 16 November 2026).

**Two tiers** (decided by the author on 21 November 2026, §9 row 66). The study's necessity is to
find the force. The **confirmatory** family is the force and its two outlets, with the control:
**H5** (the force forms: choice of class narrows), **H2** (concentration: a core draws code in),
**H6** and **H7** (dispersion: forced changes spread and couple, at the same change size) and
**H4** (the control: function injection removes the force). Holm over these five. **H1** (the
periphery grows, the cost of concentration) and **H3** (shape does not draw code in, the rival
ruled out) are **secondary**: each keeps its direction and rule and is decided on its own p,
outside the correction. The readings (§4.2b–4.2e) are reported.

**Forced** (decided by the author on 21 November 2026, §9 row 65) means **forced by
encapsulation**: a placement whose code was bound at the class to a member no other class can
reach, a private field or a private method. A constant follows its access like any field (the
author, 21 November 2026: "it is good code to move constants to another class and make public for
consumption"): a private constant forces, a public one does not. A placement bound at the class
only to members other classes can reach is *unforced* (chosen); one not bound at the class is
unbound. The definition is the force itself and
works the same with or without dependency injection, so corpus B, which mostly has none, gets the
same contrast as corpus A. Forced by binding with no alternative (H5's class level, §4.2a) is
reported beside it in H6 and H7, and stays H5's own measure.

- **H1, the periphery grows** (restated 17 November 2026, twice; renamed 19 November 2026, §9).
  Until then it was called *gravity compounds*: its test is unchanged, its reading is not. What
  rises is mostly periphery (H2): not what draws code to a place, but what code drawn there has
  to sit beside, the cost of the core. In the methods arm, the
  bystanders of an addition (§4.3a) rise with the checkpoint index (positive slope, 95% interval
  above 0). They rise over all additions, and **within a place**: among the additions that go into
  one class, the later ones find more of the class's data standing by, and likewise within one
  method. The place itself gathers data; the rise is not code moving to places that hold more.
  - *Constants count* (decided 17 November 2026; the reason the author's, 19 November 2026). A
    constant left in a class binds code to that class, and is typically why code is put there; it
    belongs in a file of its own that any place can use. So a constant gathering in a class is part
    of what H1 predicts, and H1 read without constants is a reading, not a test of it.
  - *As first registered:* the addition's bindings rise with its host's size and with the checkpoint
    index. That is kept and reported beside it. It was replaced because the bindings an addition has
    are largely the data its problem needs, and because nearly every Spring run into an existing
    method already has one (the ceiling the pilot found).
- **H2, a core draws code in** (restated 19 November 2026, §9). In the methods arm, where an
  addition was bound to a **class** or a **method**, the data of that place is of two kinds
  (§4.4): its **core**, the values the addition was bound to, and its **periphery**, the rest the
  place then held: what stood by (§4.3a) and what the addition introduced (§4.3b). Later code for
  other problems comes there **for the core**. Holding the problem fixed (its checkpoint, the
  addition's size and the earlier rules it declares it crosses) and the host's size, later
  intrusions use a core value more than they use a periphery value: the rate ratio per value is
  above 1, at the class and at the method. With H1: a place gathers data, but what gathers is
  mostly periphery; what the next code is bound to is the few values code there was already
  bound to.
  - *As it stood from 17 to 19 November 2026* (data draws code in): the more data stood by, the
    more later code arrives bound to that data, as a rate ratio per value that stood by above 1.
    That is kept and reported beside it. It was replaced because it says uptake is in proportion
    to the amount of data, and its own failure case is later code coming for the same few values
    however many more had gathered. On the development chain that is what was seen (§6): most
    bound uses went to a few values that were there from the start, and what changes introduced
    was hardly ever used again.
  - *As it stood until then* (forcing does the harm): the more bindings an addition has, the more
    cross-problem intrusion follows where it was placed. That is kept and reported beside it. It
    was replaced because it is not the number of bindings a problem has that draws later code, but the
    data lying where the problem's code was put.
- **H3, shape does not draw code in** (made one-sided 17 November 2026; its measures set 18
  November 2026, §9). With the problem held fixed, and the bindings and the bystanders in the
  model, the shape of the place the addition landed in does not raise the intrusion that follows
  there, at the method or at the class. The shape measures are the literature's (§4.7, §4.7a):
  - **at the method:** long (S1), cognitive complexity (S4) and cyclomatic complexity;
  - **at the class:** concentration (the Gini of S5), weight (WMC) and lack of cohesion (LCOM*).

  Not among them: not slimmable and junction (S2, S3), the author's sinew measures of how data
  flows through a method; and fan-out and CBO, which measure how far a place reaches out and are
  read with them (§5, *The sinew measures*). Each of H3's measures is fitted by itself, and its
  effect is shown to lie below the upper margin of §5 (1.25). A shape
  that is followed by *less* intrusion does not count against: the belief under test is that large
  and complex code attracts change, and nobody holds that it repels it. Such an effect is reported
  with its size.
  - *As it stood until then* (shape adds nothing): each effect within the margin on both sides,
    0.8 to 1.25. That reading is kept and reported beside it.
  This makes confirmatory
  the result of Olbrich, Cruzes and Sjøberg (2010): god and brain classes change more and hold
  more defects, but less per line once size is controlled. The question is contested: Zhou, Leung
  and Xu (2009) find class size accounting for, or reversing, the association of many
  object-oriented metrics with change-proneness, while Chowdhury et al. (2022b) report metrics
  that still matter at the method once size is removed. H3 holds data fixed, not only size, and
  the problem; its method-level result is to be set against Chowdhury et al.
  - *H2 and H3 were one hypothesis* (H2a and H2b) until 17 November 2026, supported only if both
    held (§9). They are now decided apart: one is a difference to be shown, the other an
    equivalence, and the second should not decide the first.
- **H4, function injection forms no core** (restated 17 November 2026; renamed 19 November 2026,
  §9, from *keeps the space open*; its test is unchanged). Each function is handed its own data,
  so no place holds values that every later problem has to come to. On the same
  stream, the function arm's bystanders are fewer, and their slope on the checkpoint index is
  flatter, than the methods arm's; and its bound code is **come back to less**, at the class and at
  the method (§4.4). (*As first registered:* its bindings are lower and their slope on host size
  flatter; kept and reported beside it.) The total amount
  (positions, tokens) of the function arm lies within 0.8 to 1.25 times the methods arm's, the
  band the flow-injection draft took from the conservation study's spread. The coupling that
  leaves the scopes appears as wiring (§4.5) and is reported, not hidden.
  - *Reported beside it* (19 November 2026): how much a core value is come back to, function arm
    against methods arm (§5). It is where the arms differ most on the development chain (§6), and
    both arms solve the same problems, so a core that was only the problems' shared data would be
    used alike in both. It is not a condition of H4: few of the function arm's rows have a core
    at the class (one on the development chain), so as a condition it would often not be
    estimable.
- **H5, choice narrows** (added 19 November 2026, §9; the author's). In the methods arm, a bound
  addition's **alternatives**, the other places in the code before its checkpoint that hold what
  its code was bound to (§4.2a), do not rise as the stream goes on: they stay as they are or fall.
  The author's expectation is that it is always the same place, or that places get restricted over
  time, especially at the class; there may be choice early and less later. One-sided, as H3: the
  ratio of the alternatives at the end of the stream to those at its start is shown below the
  upper margin (1.25), at the class (the method level reported since 20 November 2026, row 64). A flat count passes; a fall is reported
  with its size and does not count against. H5 is decided apart from H2: H2 is about what later
  code comes back to a place for (binding), H5 about whether the placement had anywhere else to
  go. It is the plan's title read directly: *whether it had a choice*.
  - *Reported beside it:* the share of placements with no alternative (forced), per arm and third
    of the stream; the function arm's ratio, and the arms' contrast (its injected parameters are
    not bindings, so its alternatives are expected to stay open); the alternatives themselves, by
    name, for each row.
  - *H5 is tested at the class only* (decided by the author on 20 November 2026, §9 row 64): "H5
    for method shows increase volume of the encapsulation so it should only be read at the
    encapsulation level of the class". The method level is reported.
  - *The author's reading of H5 on the development chain* (20 November 2026, after seeing it, §6):
    new functionality enlarges the area of methods, but binding forces that area into a class. So
    the choice of class narrows while the methods in the class multiply under that forcing, and at
    the method the alternatives on a request's flow widen. H5 and its test are unchanged by this;
    it is the reason for H6.
- **H6, forced changes spread** (added 20 November 2026, §9; the author's). In the methods arm,
  a change with no choice has to be made in more classes at once: the number of classes that
  existed before it that a unit places or edits code in (its **spread**, §4.2b) is wider in a unit
  where a placement was forced at the class (bound there with no other class holding what it was
  bound to, §4.2a) than in one where none was, at the same point in the stream. One-sided. A new
  class is a free choice and is not counted (decided by the author on 20 November 2026, after the
  development chain, §9). As first drafted, H6 also needed the spread to rise over the stream; the
  author decided the same day to focus on forced and to track forced and unforced units apart, so
  the rise is reported, in each apart (§9). The author's
  reasoning: things that change together should stay together, so a change that keeps having to
  go into two classes because it has no choice shows that the two lack cohesion, and that
  placement (in particular which class encapsulates which fields) should be redistributed between
  them. H6 joins H5 (choice) to its cost across classes, as H2 joins binding to its cost within
  one.
  - *Reported beside it:* the spread's rise over the stream, over all units and in forced and in
    unforced units apart; the spread per arm and third, with new classes beside it; the function
    arm's forced ratio, rise and the arms' contrast (a function placed by its wiring is not forced into a class by fields, so
    its spread is expected to stay flat); and the **coupling of pairs of classes changed
    together**: the calls between the two before each unit that changes both, on the index, for
    pairs changed together more than once, expected to rise (coupling growing between classes
    that keep changing together). The pairs most often changed together whose coupling rose are
    listed by name, the candidates for redesign.
  - *Accounted beside it* (the author, 20 November 2026): where the **growth of existing classes**
    came from (the share of positions added by placements forced at the class, chosen there, or not
    bound there), and where **coupling between classes** came from (the calls between classes each
    unit added, the share of it in units with a forced placement and between classes changed
    together). Together these say how much of the growth in size, and of the growth in coupling,
    arrived by forcing: by absorbing into a class, or by spreading to the classes holding the
    other data.
- **H7, forced changes couple** (added 20 November 2026, §9; the author's). In the methods arm, a
  class that a forced change goes into gains more calls across its boundary in that change than a
  class a change goes into with no forced placement, at the same point in the stream: outward,
  to the other places holding data it needs, and inward, from places that now need it. One-sided.
  The author's reasoning: encapsulation is the force. What a class holds privately can only be
  used inside it, so a change that needs it is forced inside (concentration; its cost is the
  class's size, H1, H2 and H6's growth accounting). A forced change that also needs data held
  elsewhere couples to that other place, either to what it already exposes or by asking for its
  encapsulated data to be widened (made public) to couple to (dispersion; its cost is coupling).
  So coupling between the encapsulation and the rest of the system increases because of the
  forced change. With the amount of code conserved (H4's band), placement is the design: it
  divides the same complexity between size and coupling. H6 says whether forced changes spread;
  H7 whether they couple, and through what.
  - *Prior work* (LITERATURE.md §10, novelty check of 20 November 2026; read as abstracts or
    records unless said): encapsulation as a force is known as a concept, not as a measure.
    Page-Jones's connascence (1992, 1995) holds that a dependency across an encapsulation
    boundary is worse than one within it, the stronger the worse; Ousterhout (2018) argues for
    deep modules, much behind a small interface, and against information leakage across them.
    Neither measures a change. Widening is measured per member across releases, not tied to the
    change that caused it (Kobori, Matsushita and Inoue 2015; Vidal et al. 2016). That the amount
    is conserved and placement divides it is a framing only (Tesler's law; Hatton 2014; Pescio's
    *physics of software*), not a tested law; the study keeps it as framing and tests the
    forced/unforced contrast, not conservation itself (which H4's amount band only checks).
  - *Reported beside it:* the forced ratio for the calls that reach a member the change exposed
    (added, not private) or widened (made more open), for outward and inward calls apart, and for
    the class's own members exposed or widened; the share of the added calls reaching an exposed
    or widened member, forced against unforced; the rise of the added calls over the stream; the
    function arm's forced ratio and the arms' contrast (a function's dependencies are injected,
    so no private data forces it, and its coupling is in the wiring, H4).
- **A reading: split or concentrate** (added 20 November 2026, §9; the author's; reported, not
  among the confirmatory tests). Encapsulation forces code into a class
  (concentration); the counter force is to separate it into more encapsulated units, which opens
  up coupling. Between them is a tension, size of the encapsulation against distribution and
  coupling, and the author asks what relation between them is good engineering. The reading: a
  class whose forced changes fall into groups that share none of its data (mutually exclusive
  encapsulated items, the groups changing with different classes) lacks cohesion, and splitting
  it is right; a few classes changed together again and again over the same data, their coupling
  rising, should be concentrated. Good engineering is where neither holds. The reading describes
  where the code stands between the two forces (§4.2d). It is not checked against what developers
  later did: the author's interest is the forces, and developers work inside them (20 November
  2026).
- **Q1 is descriptive.** Its expected baseline (Steidl and Deissenboeck 2015) is that most
  growth is new methods. So the share of additions that land in an existing host is reported as
  found, with no direction predicted.
- **Two readings with a stated direction, reported and not among the confirmatory tests** (added
  16 November 2026, §9):
  - **Formation.** Within an arm, for the same problem, a chain that has been forced more so far is
    bound more now, and ends more concentrated (§5, *Formation*). This is the black hole forming,
    read directly and not from a slope.
  - **Review.** Where a placement was chosen, a reviewing agent re-places it; where it was forced,
    it cannot (§5, *Review*).
  - **Size or data** (added 17 November 2026, §9). A large place also attracts, but its size is a
    proxy for the data gathered in it. With both arms pooled and the size of the place held fixed,
    later intrusion rises with what stood by (§5, *Size or data*).

**What would count against.**

- H1: no slope, or a negative one, over all additions or within a class or a method. The
  surroundings of a problem's data would then be a constant cost of the form, not something that
  grows. A rise over all additions with none within a place would mean that code moves
  to fuller places, not that places fill.
- H2: later code using a periphery value as much as a core value, at the class or at the method.
  The data of a place would then be taken up alike, and the place would have no core.
- H3: any shape measure followed by more intrusion, beyond the margin, with the problem, the
  bindings and the bystanders held fixed. That would mean that shape draws code in by itself. A
  shape measure followed by less is reported, and does not count against.
- H4: no difference between the arms in bystanders, in their growth or in later intrusion, or an amount
  outside the band (the difference is then a difference of amount, not placement), or a function arm that moves its coupling into the wiring:
  wiring per problem that rises over the run, or one configuration file that holds most of it
  (§4.5).
- H5: alternatives that widen over the stream, beyond the margin, at the class or at the method:
  code would then find more places to go as the system grows, and placement would loosen, not
  narrow.
- H7: a class a forced change goes into gaining no more calls across its boundary than one a
  change goes into unforced. Forcing would then concentrate code without coupling it, and the
  coupling between classes would come from elsewhere.
- H6: a spread no wider where a placement was forced than where none was. Changes would then stay
  in one class however little choice there was, and lack of choice would cost nothing across
  classes.

Every one of these outcomes is reported whichever way it points.

## 3. Data

### 3.1 Corpus A: the paired streams (confirmatory)

**The ui runs are the primary test** (decided by the author, 18 November 2026, §9). The verdicts
on H1 to H4 that the study reports as its test are those of the ui analysis (§3.1a): Spring
against OfficeFloor over its Runs A and B. The petclinic runs are **secondary**: read first,
because they exist, each as a replication with its own verdicts, and none of them the study's
test.

- *Why.* The petclinic stream sends every rule through one endpoint, `POST /api/owners`. So one
  handler method and one controller class receive nearly everything, in every chain: the method
  level of H2 rests on a single method per chain, and the class level cannot tell classes apart
  (§6). That is a property of the stream, and it makes petclinic a weak test of exactly the
  levels the hypotheses are about. The ui stream has many endpoints and 250 checkpoints.
- *What had been seen.* This was decided after the development chain of petclinic showed H2 at
  the method resting on one method, and H3's class measures untestable there (§6). No ui run's
  backend Java had been read. So the choice of the primary corpus was made knowing how the
  weaker one looks, and not knowing how the primary one does.
- *What it costs.* The primary test waits on Run B (§3.1a). With Run A alone the arm cannot be
  told from the front end, so nothing confirmatory can be read until both runs are complete.
- *As first registered:* the petclinic run `blind-202608100006/just-solve` was the primary, and
  the ui runs a second corpus read after it.

The petclinic degradation harness (`spring-petclinic-rest-long-degradation-test`) grows one
application through a fixed stream of plain-English change requests, under a Spring
`@RestController` arm and an OfficeFloor arm. Every checkpoint is committed separately, and the
runs are published as `evolve/<run>/<strategy>/<arm>/chain<n>` branches of
`officefloor/spring-petclinic-rest` (145 branches as of 15 November 2026). Later, the
`ui-long-degradation-test` runs (250 checkpoints; Spring and OfficeFloor backends) are added
once they exist.

Why the paired streams are the confirmatory corpus:

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

- **The first of the petclinic runs** (secondary since 18 November 2026; until then the
  primary): `blind-202608100006/just-solve`, both arms, chains 1 to 8 and 10. Chain 9 is the
  pilot's development data and is excluded. The review reading (§5) is still set against it.
- **The other petclinic runs, each read on its own as a replication, never pooled with it or with
  each other:** the other strategies, `blind-202609010045/impact_gated`,
  `blind-202609031757/impact_gated`, `blind-202609160027/cohesion-prompt` and
  `blind-202609290948/reviewed`, and the earlier just-solve runs, `202608011310`,
  `full-202608102319` and `202608081920`. A different instruction to the agent is a different
  condition. A run with fewer than 6 chains in an arm is reported descriptively.
- The commit read on each chain is its branch head in `officefloor/spring-petclinic-rest`,
  recorded with its hash when the analysis runs.

**Corpora are replications, never pooled.** The petclinic and ui streams are different problems.
Each is analysed on its own and the two are compared by direction and interval, so that no
estimate mixes solutions to different problems.

### 3.1a Corpus A2: the ui-long-degradation runs (the primary test)

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
  direction is fixed now: the most bindings of the three arms, as nothing is lifted off the flow
  (dependency injection weakens bindings, function injection removes them). Spring against
  OfficeFloor stays the primary contrast; the control is read against each.
- Every new rule in the stream declares the earlier rules it crosses (at least two from cp17),
  which gives the declared crossings of §4.4. They are read from the stream's
  `acceptance/DENSITY.md` at the tag `run-a` (§4.4, *As built*).

**Order.** The petclinic corpus (§3.1), secondary, is analysed first, because its runs exist; the
ui runs, the primary test, follow once Run B is complete.

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

Pre-AI Java repositories drawn by `open-source-repository-sampler`. (*As first drafted, 16
November 2026:* seed 2, the sample the complexity-concentration and sinew-identification studies
drew, its history read up to 29 June 2021. **Replaced on 18 November 2026** by a sample of its
own, drawn as of a date, below.)
Additions are commits linked to an issue labelled as a feature or enhancement, of **at most 200
changed lines** of production Java, with refactorings removed by RefactoringMiner. Commits linked
to issues are known to be a biased subset (Bird et al. 2009), and tangling remains at the reported
7–20% (Herzig et al. 2016). In corpus B a commit is not reliably one problem and the problem is not
held fixed. Corpus B is therefore read only as a check on the **direction of H1 and H2**; H3,
H4 and the junction × arm reading are not read there.

**Extended 18 November 2026** (§9; drafted, not yet built). H1 and H2 as they now stand need only
a history, so more can be read here than the first draft allowed:

- **H1**, over all additions and within a class and a method. There are no checkpoints, so the
  index is the commit's place in the order of the repository's commits read, from 0 to 1.
- **H2**, at the class and at the method. With no stream to declare which later changes are meant
  to touch an earlier one, every later arrival counts.
- **Where bound and unbound code lands** (§5), as on corpus A.
- **H3, weaker.** The problem cannot be held fixed, so each shape measure is read with only the
  addition's size, the place's size, the bindings and the bystanders held fixed. Reported, and not
  called H3.
- **Not read:** H4 (there are no arms), the junction × arm reading, the wiring.
- **Two units.** The issue-linked feature commit above stays the unit for reading corpus B by
  itself. For the comparison with corpus C a second unit is read in both: **every commit that is
  not a merge** and changes at most 200 lines of production Java, refactorings removed, because
  agents' commits are seldom linked to labelled issues.

**As built** (18 November 2026; `placement_gravity/history.py`, `tests/test_history.py`,
`runs.yaml`, `step2b_samples.sh`, `step3b_histories.sh`). Fixed with the code before any
repository of corpus B or C is read:

- **The sample of corpus B** follows the criteria of `long-method-slim-study`'s sample (its
  `docs/ANALYSIS_PLAN.md`, §3; looked at on 18 November 2026 at the author's direction), which
  were set for the same purpose, code that people wrote:
  - **As of 1 December 2020** (`--as-of`; confirmed by the author, 18 November 2026: the same
    date as that study, for its reason). GitHub Copilot's technical preview opened on 29 June
    2021; 1 June 2021 is before it, and this date is six months before that again, so that no code
    in the sample was written with AI code generation. Only repositories created before that date
    are in the frame; each is
    pinned to its newest commit before it and judged by the criteria there. So every unit is
    from before the date, and no date is applied to the units.
  - **Frame:** Java, the three tiers of attention (over 5,000 stars; 1,000 to 5,000; 200 to
    999), drawn equally.
  - **Criteria:** at least 50 functions in at least 15 files with a function, at the pin;
    repositories owned by `officefloor` or `sagenschneider` excluded. These say how large a
    repository must be; there is no criterion on its commits and no cap on its units.
  - **Two sets, each of 300** (decided by the author, 19 November 2026; until then one set, seed
    `20261118`):
    - *The first set* is `long-method-slim-study`'s own sample (seed `20261101`, sampler 0.3.0,
      580 usable), read where it lies: the first 100 usable repositories of each tier in the order
      of the draw. It ties the two studies to the same repositories. That sample has been read
      for that study's measures (width, slimming), never for these (§7).
    - *The confirming set* is drawn with seed `20261118`, one nobody has drawn, by the same
      criteria, leaving out the first set's repositories: drawn with room (450) and the first 100
      usable of each tier kept. Its readings are to agree with the first set's.
    (Seed 2 and seed 3 drew samples other studies have read.)
  - **Size: 300 usable repositories**, 100 a tier (decided by the author, 18 November 2026; 60
    was first drafted). The repository is what the intervals are taken over, so their width is set
    by this number. That study drew 580, but it parsed each repository once; this one reads every
    commit of each (the development repositories took 0.3 to 1.3 seconds a unit), which is why the
    reading is done several repositories at a time (below).
  - The first draft's sample (seed 2) had been drawn without a date: its pins are recent, its
    frame holds repositories created since, and its criteria describe today's code.
- **A unit** is a commit that is not a merge and changes between 1 and 200 lines of production
  Java (a `.java` file outside a test directory). Every such commit reachable from the pin is
  read, in the order of committer date, not only the first-parent line: on the two development
  repositories the first-parent line gave 84 and 86 units, most of it being merges of pull
  requests. **There is no cap on the units of a repository** (decided by the author, 18 November
  2026; a cap of 2,000 was first drafted): how large a repository may be is for the sample's
  criteria to say, on its files and functions, not for a count of commits. The models carry an
  intercept for the repository, and the number of units each contributes is reported, so a
  long-lived repository that carries much of a corpus is seen.
- **Read light.** The tree before a unit is the before versions of the files it changes, not the
  repository. So the bindings, the bystanders, the later arrivals, and an existing host's own
  shape (long, cognitive complexity, the class's Gini) are read as on corpus A. The literature's
  other measures (§4.7a), which need the whole tree, are not; and the landing reading gives the
  destinations (existing method, new method of an existing class, new class) but not the ranks.
  CodeTracker is not run; a method is followed by the instrument's chaining of RefactoringMiner's
  renames and moves.
- **H6 and H7 are read on corpora B and C** as H5 is (20 November 2026): a unit is a commit, its
  pairs' coupling and the calls across a class's boundary read on the same running index.
- **H5 is read on corpora B and C too** (decided by the author, 19 November 2026). Its places
  need the whole tree, so one index is kept running through a history: the whole production tree
  before the first unit, then, before each later unit, the files that differ between the previous
  unit's parent and this one's (merges and commits that are not units included, as a diff of
  trees), so the index is the tree at each unit's parent (`chain.tree_places`). H5 there is read
  in the methods arm as on corpus A, on the unit's place from 0 to 1, with the repository's
  intercept.
- **The issue-linked unit** is not built: a unit records the issues its message names, and the
  labels of those issues are not yet fetched. Until they are, corpus B is read on the second unit
  only, and that is said wherever it is reported.
- **Arms** are sets of units, not of repositories (`runs.yaml`): all, those that declare an agent,
  or the others, with dates. A repository is measured once, on all its units, so a later arrival
  counts whichever arm it is in; an arm's rows are the units in it.
- **The models** are those of §5 with the repository as the chain, no intercept for the unit (a
  unit is not a problem every repository solves), and the index a unit's place in its
  repository's units, from 0 to 1.
- **Read several at a time** (`history.measure_sample`, 18 November 2026). The repositories of a
  sample are dealt to eight workers, the largest first and in turn, and each worker's Java
  processes are held to an equal part of 70% of the machine's memory. A repository that fails in
  that pass, for want of memory or for any other reason, is read again afterwards alone, with the
  memory undivided. One that still fails is listed (`failed.txt`), counted in the report and not
  read; it is not replaced. A repository's tables are whole or absent, so an interrupted run is
  resumed by running it again. The order of reading does not enter any measure.
- **A development sample may cap its units** (`max_units` in `runs.yaml`; refused for any other
  sample): the agent development repository is read on its newest 300.
- **Two development samples** (seed 4, people's code as of 29 June 2021; seed 5, with declared
  agent commits) are read to build these steps, as chain 9 is for corpus A. Their repositories are
  left out of corpora B and C.

Corpus B stays a replication with direction and interval only. It is where the hypotheses meet
code written by people, which corpus A cannot give.

### 3.3 Corpus C: repositories with declared agent commits (secondary)

Added 18 November 2026 (§9; drafted, not yet built). Corpus A is written by one agent on a fixed
stream; corpus B by people before AI assistants. Corpus C is code in the wild that an agent says
it wrote.

- **A declared agent commit** is one whose author or committer is an agent's account, or whose
  message carries an agent's `Co-authored-by` trailer or the line it adds to what it generates.
  The rule is the sampler's, not this study's (revised 18 November 2026): its built-in
  signatures, version 1 (`open-source-repository-sampler`, `agents.py`; Claude Code, GitHub
  Copilot's coding agent, Cursor, Devin, Codex, Jules, aider, OpenHands), written into the
  sample's derivation. This study reads which commits are declared with the same signatures at
  the sampler's pinned version, and adds none of its own.
- **The sample** is drawn by `open-source-repository-sampler` without `--as-of`, Java, the same
  tiers and criteria as corpus B (at least 50 functions in at least 15 files; the author's owners
  excluded), with `--min-agent-commits 30` and a seed fixed here before the draw: **seed
  `20261119`** (first drafted as seed 3, which had drawn the sample SinewSlim's search was checked
  on). The criterion was added to the sampler for this study and released in **0.4.0** (18
  November 2026), the release pinned here (`setup.sh`): the samples are drawn, and declared agent
  commits read, with it. **Target 100 repositories, with `--max-clones 6000`** (decided by the
  author, 18 November 2026; 30 and 300 were first drafted): the development draw found one usable
  repository in 39 of the mid tier, so the corpus is bounded by how many such repositories there
  are, not by the cost of reading them. If fewer than 10 repositories are usable when the draw
  stops, the corpus is reported as too small and not read, rather than widened by hand. The derivation reports every
  repository drawn, kept and left out.
- **Two comparisons**, both reported with a stated direction and neither confirmatory:
  - *Within a repository:* declared agent commits against its other commits after 29 June 2021.
    The others are of unknown origin, since assisted code carries no mark, so this compares
    declared with undeclared, not agent with person.
  - *Between corpora:* corpus C's declared agent commits against corpus B's commits, all before
    29 June 2021. This is agent against person, across different repositories and years.
  - *Predicted*, from Ogenrwot and Businge (2026), who find agents' pull requests touching fewer
    files: a declared agent commit's unbound code enters an existing class more often, and its
    bound code lands among more bystanders, than the commits it is compared with.
- H1 and H2 are read on corpus C as on corpus B, on all its commits, with the share that is
  declared agent as a term.
- **Read after corpus A**, and only when its steps are built and this section is fixed by a tag.

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

### 4.2a Choice (H5): the other places that could have held the code

Added 19 November 2026 (§9). For each bound addition to a host (§4.3), at each level where its code
was bound, the **alternatives** are the other places in the code **before its checkpoint** (the
tree at *k − 1*, every production Java file) that hold what the code was bound to:

- **At the class:** another class that holds injected dependencies of every type the code used
  from its own class (decided by the author: *the same injected dependency*). Code bound to anything
  else of its class (its state, a constant, one of its methods) has no other class holding that
  value, so its alternatives are none: such a placement is forced at the class.
- **At the method:** another method **on the host's control flow** with a parameter or local of
  each declared type of the method's values the code used (decided by the author: *the type*; the
  control flow decided by the author on 19 November 2026, after the development chain showed that
  type alone does not separate the places, §6). The control flow (`placement_gravity/flow.py`):
  the methods that call the host, directly or not; of those, the ones nothing in the application
  calls (the request's entry points, which the framework calls); and every method those reach. A
  call is followed by its receiver's declared type (a local, parameter or field, a class named for
  a static call, or the method's own class), to the methods of that name and arity in that class,
  what it extends or implements, and what extends or implements it; a call whose receiver the
  source does not type (a chained call, an expression) is not followed, and how many such calls
  there are is reported. With OfficeFloor, a request's functions are joined by its wiring file, not
  by Java calls: the classes one wiring file declares are on one flow. The count by type alone over
  the whole tree (as first built) is reported beside it. Generic arguments are kept
  (`List<Owner>` is not `List<Pet>`). A value with no declared type (`var`, an untyped lambda
  parameter) is left out of the match and counted. Common types (`String`, `int`) will give
  alternatives that are not real; most reuse is expected to be of domain types specific to the
  request, or at least common to it.
- **Recorded, not only counted:** each row keeps its alternatives by name (`choice_*_places`).
  Some will be in other REST endpoints, where the code's own control flow does not reach, so the
  control flow binds them too. If types do not separate the places, a refinement by control flow
  is applied after the analysis and recorded as such (§9), not before.
- **Forced:** a row with no alternative.
- **Where read:** corpus A, whose instrument reads the whole tree before each checkpoint
  (`Pull --places`), and corpora B and C, where an index of the tree is kept running through the
  history (§3.2).

As built: `instrument/Pull.java` (the declared types of each method's values and of each class's
fields; `--places`, the places of a tree), `tables.choice`, `prepare.h5_rows` (`h5.csv`).

### 4.2b Spread (H6): the classes a change has to go into

Added 20 November 2026 (§9). The **unit** is a checkpoint on corpus A and a commit on corpora B
and C (§3.2).

- **Spread:** the number of classes that existed before the unit that it places or edits code
  in, beyond the first: the classes of its hosts (§4.2) that gained positions, re-placements of
  moved code left out. A unit that changes one class has spread 0. A class new in the unit is a
  free choice, not counted (counted beside, as *all classes*); a unit that changes only new
  classes has no row.
- **Forced unit:** a unit with at least one host forced by encapsulation (§2, *Forced*; until 21
  November 2026, forced by binding with no alternative, which is reported as ``forced_bind``). A
  unit with a placement bound at the class only to reachable members is recorded as *chosen*; a
  unit can be both.
- **Coupling of a pair** (reported): for each pair of classes a unit changes together, the calls
  followed from the methods of one to the methods of the other, each way, in the tree before the
  unit (`flow.Graph.class_calls`: the call graph of §4.2a, a call that may go to several
  overrides counted once for each class it may reach). A pair is followed through its chain or
  repository: how many times it has been changed together, its coupling before each time, and
  what that unit added (the tree after it, which is the tree before the next unit, less the tree
  before; none for the last unit). Pairs with a new class are left out.
- **Candidates for redesign** (reported): pairs changed together more than once whose coupling
  is higher after their last change together than before their first, listed by how often they
  changed together.
- **Growth accounting** (reported): the positions added to classes that existed, per arm and
  third, by the kind of the placement that added them: *forced* (bound at the class, no
  alternative), *chosen* (bound at the class, with alternatives), *unbound* (not bound at the
  class); and each one's share.
- **Coupling accounting** (reported): per unit, the calls between classes in the whole tree after
  it less before it (`tables.coupling_rows`); summed per arm, with the share added in units with
  a forced placement, and the share added between the pairs of existing classes the unit changed
  together (in forced units and in the others).

As built: `tables.pair_rows` (`pairs.csv` per chain or repository), `tables.coupling_rows`
(`coupling.csv`), `prepare.h6_rows` (`h6.csv`), `prepare.pair_rows`, `prepare.co_change`,
`prepare.growth_accounting`, `prepare.coupling_accounting`.

### 4.2c Coupling across the encapsulation (H7)

Added 20 November 2026 (§9). Per unit and class that existed before it that the unit placed or
edited code in:

- **Calls added across its boundary:** the calls followed (§4.2a) from a method of the class to a
  method of another class (*outward*), or from another class's to its own (*inward*), that are in
  the tree after the unit (the tree before the next unit) and not in the tree before it. A method
  is its class and signature, so a moved or renamed method's calls count as new. The calls lost
  are recorded beside.
- **By the member reached:** *existing*, a member that was there before with the same access or
  wider; *exposed*, a member the unit added that is not private; *widened*, a member whose access
  the unit made more open (private, package, protected, public, in that order; an interface's
  members are public). Access is read by the instrument for every method and, since 21 November
  2026 (the author's decision, §9 row 65), every field of the tree (`Pull --places`, `access`,
  `fields`, VERSION 15). A read or write of another class's field (through a typed local,
  parameter or field, or a class named for a static field) is coupling as a call is (`reads`), so a
  field made public and read from elsewhere counts as widened.
- **Members opened:** the class's own members the unit exposed or widened, called or not.
- **Forced:** the class had a placement in the unit forced by encapsulation (§2, *Forced*);
  otherwise it is unforced. Forced by binding with no alternative is reported beside it.
- The last unit of a chain or a history has no tree after it and no row.

As built: `instrument/Pull.java` (`access`, VERSION 14), `flow.Graph.cross_edges`,
`flow.Graph.access`, `tables.encapsulation_rows` (`encapsulation.csv`), `prepare.h7_rows`
(`h7.csv`), `prepare.encapsulation_summary`.

*Prior work:* access excessiveness and its evolution are measured per member (Kobori et al. 2015,
across releases; Vidal et al. 2016, over-exposed methods and classes, mostly from their first
version), with no link to the change that widened them. H7 reads widening at the change, and only
as it is reached by the change's new calls.

### 4.2d Split or concentrate (reported reading)

Added 20 November 2026 (§9). Per chain or repository:

- **The values a change used in a class:** its fields and the class methods it called (§4.4's core
  at the class), for each host of the unit in that class.
- **Split, flagged:** a class that existed, with its forced changes (placements bound at the
  class with no alternative, §4.2a) in order; two changes are joined when they used a value in
  common, and the class is flagged at the first unit by which there are at least two groups of at
  least two changes each that share no value. Recorded: the groups' values, and whether the
  groups' changes went with different classes (the other classes the same units changed, none in
  common).
- **Concentrate, flagged:** a pair of existing classes changed together at least three times
  (§4.2b), where at least half of the times after the first the change used a value of either
  class it had used at an earlier time (the same data again), and whose coupling after its last
  time together is above that before its first. Flagged at its third time.
- **Reported per arm:** the classes with two or more forced changes and how many were flagged
  (and of those, how many with groups changed with different classes); the pairs changed together
  at least three times and how many were flagged; the candidates by name, with their groups' values.
- *Drafted with a check against the developers' later refactorings and withdrawn the same day by
  the author* ("I'm not interested in what developers did. They are likely working inside the
  engineering forces"). The refactorings RefactoringMiner finds that split a class or move a member
  between classes are still recorded per unit (`tables.refactoring_rows`, `refactorings.csv`);
  nothing reads them.

*Prior work:* splitting and concentrating are what Extract Class recommenders and co-change based
Move Method/Field recommenders propose (LITERATURE.md §10), and the balance between cohesion and
coupling is what search-based modularisation optimises (Mancoridis et al., Bunch; Harman et al.);
Paixão, Harman, Zhang and Yu (2017) measure how far developers' changes move a system towards or
away from that optimum. This reading is those signals restricted to forced changes, reported as
where the code stands between the two forces, not as a recommender.

As built: `prepare.redesign`, `report.redesign_section`.

### 4.2e Surface against volume, and ripple (reported readings)

Added 20 November 2026 (§9 row 63; the author's). The exchange between the two outlets.

- **Volume** of a class: its methods (and its positions where the tree's shape was read).
  **Surface**: its links across its boundary, each method's link to another class counted once
  (out), and each other class's method linking to it once (in), as followed in §4.2a.
- **Surface against volume:** per arm, log(1 + surface) on log(methods): across the classes of
  each chain's last tree (the chain's intercept), and within a class as it grows over the units
  that changed it (log methods centred on the class's mean). The exponent below 1 means surface
  grows slower than volume, so concentration saves communication; above 1, faster, so a large
  class leaks. Read against the function arm and against size scaling (Lopes and Ossher 2015,
  §7), not against 1 alone. Per change: the surface it added against the methods it added, forced
  against unforced at the same methods added.
- **Ripple:** for each call a unit added across a class's boundary (H7's, §4.2c), the later units
  that change the method it reaches, and the share of those that also change the calling class:
  the cost of dispersion paid again later. Against chance (decided by the author, 20 November
  2026): the share of the chain's units that change the calling class anyway, so that a ripple
  ratio above 1 is beyond two classes that both change often. Per arm, by whether the call came with a forced change
  and whether it reached a member already open or one the unit exposed or widened.

As built: `tables.boundary_rows` (`boundary.csv`), `tables.edge_rows` (`edges.csv`),
`prepare.surface_rows` (`surface.csv`), `prepare.ripple`, `analyse.R` (`surface`),
`report.surface_section`.

### 4.3 Bindings (Q2), the measure of gravitation

Only **logic lines** carry the value of a change: a method's body statements. Signatures,
declarations, imports and constructor wiring are organisation. So is a **plain accessor**
(17 November 2026, §9): a method whose whole body returns a field of its class, or assigns one of
its parameters to one. It exposes the field for use elsewhere and holds no logic. An accessor that
does anything more is logic: logic has then been put into a data carrier, and it counts. What matters is where the data each
added or edited logic line uses comes from. If it comes from values the change itself defines, the
code could have been placed anywhere. If it comes from values that already existed, the code has to
be placed near them, so choice is restricted. Those are its **bindings** (`instrument/Pull.java`;
`results/pilot/PILOT.md`):

- **Method bindings:** the host method's pre-existing parameters and locals.
- **Class bindings:** the host class's pre-existing fields (constants included) and methods. In Spring,
  injected dependencies are fields, so they bind code to its class. Inherited members bind too; the
  instrument reports any reference it cannot resolve (none in the pilot).
- Every reference on an added or edited logic line counts. A token-level reading, which counts
  only what an edit itself introduced, is reported beside it.

**Not bindings:**

- **Injected parameters.** A function placed anywhere can declare them; every parameter of a wired
  OfficeFloor function is injected, though its locals still bind.
- **Class utilities** (loggers), which any class can declare; they are reported apart.
- **Birth bindings**, the values a caller passes a new method; they are reported, already counted on
  the caller's line.

**Bindings to injected dependencies, reported apart.** A field holding an injected dependency can be
declared by any other class too, so using it may not pin code to this class: the same reasoning
that makes an injected parameter not a binding. A field counts as injected when it is annotated for injection (`@Autowired`,
`@Inject`, `@Resource`, `@Value`, OfficeFloor's `@Dependency`); when, in a container-managed class
(`@Component`, `@Service`, `@Repository`, `@Controller`, `@RestController`, `@Configuration`,
`@ControllerAdvice`, `@RestControllerAdvice`), it is assigned from a constructor parameter or filled
by Lombok's `@RequiredArgsConstructor` (final fields) or `@AllArgsConstructor`; or when it is assigned
from the parameter of a method annotated for injection (setter injection). A constructor parameter of
a class the container does not manage is data, and a constant (`static final`) still bindings.

- **The primary measure keeps them:** an injected field is a class binding, and H1 to H4 are read on
  all bindings.
- **Reported beside it** (§5): H1, at method level and at class level, H4 and H2, each with the
  bindings to injected dependencies left out (`binding_no_injected`, `binding_class_no_injected`).

**Pull is graded by where the value comes from** (stated 16 November 2026, §9). The expected
order, from the least pull to the most:

1. an **injected parameter** of a wired function: no pull, as any function placed anywhere can
   declare it (not a binding);
2. an **injected dependency** held in a field: a pull by convenience, as another class could declare
   it too, but the code is easiest to place where it already is (a binding, reported apart);
3. a **value bound to the control flow**: the request object, a parameter or a local of the host
   method. It exists only there, so code that uses it has to be placed there or be handed it (a
   binding).

Spring's handler receives the request object on its control flow, so its additions start with the
strongest pull; OfficeFloor's functions receive theirs by injection. The primary measure counts 2
and 3 alike. The readings without injected dependencies (above) and without parameters (§5) show
how much of each result rests on each grade.

**A binding shows pull, not the absence of an alternative.** It is evidence that the placement was
held, not proof that no other placement existed. Two readings check it: the spread of placements
over the chains at one checkpoint (§5, *Choice at a checkpoint*), and whether a reviewing agent
moves the code (§5, *Review*).

Bindings are related to Feature Envy turned inwards (Tsantalis and Chatzigeorgiou 2009). Their metric
finds a method drawn towards *another* class's data, as a snapshot recommendation. Bindings measure an
addition held by its *own* host's pre-existing data, at the commit where it is placed.

**Forced / chosen:** a run is forced when its bindings are 1 or more, and chosen otherwise. The cuts
2, 3 and 4 are reported beside it. Because the pilot finds 93% of Spring's runs into existing
methods forced at 1, H2 is tested on the binding count, with the cut as a reading aid. H1 and H4 are
read on the bystanders (§4.3a). The binding-based readings of H1 as first registered (at method level
in both arms, and at class level in Spring: class bindings against the class's size) are reported.

### 4.3a Bystanders (H1, H2, H4), the measure of what gravity gathers

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
- **Utilities** (loggers) are not counted; they are reported apart, as for the bindings.
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
alike (moved code left out). Unlike the bindings, the measure is defined for a new method, which sees
its class's fields.

**Two links, reported** (not confirmatory):

- **Accretion:** per addition and arm, the fields it adds to classes that already existed. This is
  the mass an addition leaves behind. Since 19 November 2026 it is the class's half of what a
  change **introduces** (§4.3b); the method's half is the parameters and locals it adds.
- **Capture:** for the same problem, is a chain whose heaviest class holds more more likely to
  place the addition in an existing host? Per addition, the share of its positions landing in
  existing hosts, on the fields (of all three kinds) of the chain's heaviest class at *k* − 1, with
  the checkpoint's intercept. Predicted: positive in the methods arm.

Bystanders are related to the scope-width measures of the long-method-slim study's step 7 (live
width along a method). They differ in being read at the point where a problem's code lands, on
what that code did not need, and in counting the class as well as the method.

**Relation to measures in the literature** (added 18 November 2026 after the second novelty
check, `LITERATURE.md` §10):

- **Common coupling** (Schach et al. 2002; Yu et al. 2004) counts the global data a system's
  modules share, per version. A bystander is the same exposure read per addition and per place,
  and only the part the addition did not use.
- **Over-exposure** (Vidal et al. 2016) is visibility beyond use too, but of methods and classes
  through their access modifiers, at one snapshot. A bystander is a value visible to code where it
  lands, at the commit.
- **Lack of cohesion** (LCOM, Chidamber and Kemerer 1994) sums, over a class, the methods that do
  not share fields. A class-level bystander is close to one addition's part of that sum: the
  fields its code did not use. They differ in what they are for. LCOM* describes the class as it
  stands and is one of H3's shape measures (§4.7a); the bystanders are what one addition found
  there, and what later additions then use is H2's outcome. A class can have many bystanders for
  every addition and yet a low LCOM*, if its methods share a few fields among many; and H3 is
  read with the bystanders in the model, so LCOM* is asked what it adds to them.

### 4.3b Introduced (reported), the third kind of value

Added 19 November 2026 (§9; decided by the author). A value at the place a change lands in is one
of three kinds:

- **Needed:** it was there before the change, and the change uses it. This is what binds (§4.3).
- **Bystanding:** it was there before the change, visible, and the change does not use it (§4.3a).
- **Introduced:** it was not there before. The change adds it.

**What is introduced.**

- **At the method:** the parameters and locals the method has after the change that it did not
  have before it. Every value of a new method is introduced.
- **At the class:** the fields (state, injected dependencies and constants; not utilities) the
  checkpoint adds to the class. This is accretion (§4.3a), now by name. As there, it is read on
  classes that existed: code in a new class is never bound, so a new class's fields do not enter
  the rows H2 is read on.

**Why it is counted.** A new method has no values from before, so nothing stands by in it, and by
the definition of §4.4 nothing can later be drawn in by what stood by: at the method its row reads
nought and nought, whatever happens to it afterwards. But the method's parameters bring data onto
the control flow, the strongest grade of pull (§4.3), and its locals hold what it worked out. That
is mass the change leaves in the place. By the rule of §4.5 it is mass and not yet pull: it pulls
when a later change has to be placed with it. From the second arrival on that is already read,
because what one change introduced stands by for the next change placed there. What was not read
is the first return, and how much each change leaves.

**What it is not.** An introduced value is not a bystander of the change that introduces it: that
change normally uses it. And a parameter or local is visible only in its own method, public or
not, so it does not stand by for code in the class's other methods. Fields are what stand by
across a class.

**Reported, and no part of a hypothesis:**

- per addition and arm, the method values introduced, beside the fields left behind (§4.3a);
- per bound problem and host, how many values were introduced at the class and at the method, and
  how many of the later intrusions there are bound to one of them;
- **H2 read again on what the change left in the place**: what stood by and what was introduced,
  together. The outcome is the later intrusions bound to either; the predictor is the number of
  both; the model is H2's (§5). A new method is then a row with data in it.

When this was added H2's predictor was what stood by, and the reading above was its wider form.
The wider count is closer to "how much data the place holds", which on the development chain
goes with the place's size (§6). **Later the same day H2 was restated** (§2, §4.4): what a change
introduces is now, with what stood by, the periphery of H2.

**As built** (`Pull.java` version 11, `tables.host_rows`, `tables.outcome_rows`,
`tests/test_bystanders.py`, `tests/test_stream.py`, 19 November 2026): values are matched by name.
A method's introduced values are those it has after the change less its pre-existing ones as
§4.3a reads them, so a local whose declaration line the change edits counts as introduced, as it
does not count as pre-existing there. A field renamed by the change counts as introduced, as it
always has in accretion. A later intrusion is bound to an introduced value when its own bound code
in that method, or that class, uses it.

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
- The three-way split is unchanged: declared, crossed, or intrusion.
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

**Revised before the start** (17 November 2026, §9): **intrusion is read where the code was
placed: the class, then the method. A problem's own lines are for information.** The revision of
16 November moved the outcome onto a problem's own lines, to stop a busy method lending its
traffic to every problem in it. That took the outcome away from what the study is about. The
lines of logic are the thing being placed, and changing a line is changing the problem. The
method and the class are the placement: it is the structure and organisation of the code that
gathers later changes, and a busy method or class is the finding, not a nuisance.

**Intrusion applies only where there was a binding** (decided by the author, 17 November 2026). A
binding is the reuse of data that was already there: a parameter or local of the method, a field or
method of the class (§4.3). Code that reuses nothing that was there was not drawn to its place, so
that place is not one to watch for what it draws in. Adding a field to an entity, with its
accessor, binds nothing: it is the problem's data growing, the same in both arms. So:

- **Which problems are followed:** a problem and host whose added code there has at least one binding.
  The others are counted and set aside (their number is reported).
- **What counts as drawn in:** a later checkpoint *j* whose own added code in that place has at
  least one binding there. A later change that binds nothing (a new field and accessor, a new method
  that uses nothing of the class) is not an intrusion.
- **Class level:** *j*'s bound code is in any method of the class *p*'s bound code was placed in, the
  class followed across renames and moves by RefactoringMiner's matches.
- **Method level:** *j*'s bound code is in the method *p*'s bound code was placed in. The method's
  identity is CodeTracker's for a method that survives and the instrument's chaining for one that
  is removed; which checkpoints are bound there is the instrument's reading.
- **Own lines:** as above; reported for information, and not part of any hypothesis.
- At each level the same three-way split applies: declared, crossed, or intrusion.
- **H2** is read at the class and at the method, and needs both (below, *Core and periphery*). **H3** is read at the method, since S1 to S4 are measures of the method; the same block at
  the class is reported.
- **H4's condition:** for the same problems, the function arm's bound code is come back to less than
  the methods arm's, at the class and at the method.
- **Reported beside it:** the count of any later change, bound or not (as first built).
- Problems placed in one class or method share its later changes, so their counts are not
  independent of each other. The checkpoint's and the chain's intercepts do not remove that (§7).

**Core and periphery (H2)** (decided by the author, 19 November 2026, §9). The author's picture:
a place has a few key values that everything hangs off, and many more that pass through it and
are not come back to; of those, one or two become key and most do not. The author called them
sinews and veins. This plan says **core** and **periphery**, because *sinew* already names the
measures of §4.7. For a problem *p* and a host its bound code went into, at each level:

- **The core:** the pre-existing values *p*'s code there was bound to (the binding measure). At the
  method, the parameters and locals it used; at the class, the fields it used **and the class's
  methods it called** (decided by the author, 19 November 2026: a method of the class returns a
  value or does a necessary bound piece of work, so a call to one is a core value).
- **The periphery:** the rest of the data the place held once *p*'s code was in it: what stood by
  (§4.3a) and what *p* introduced (§4.3b); at the class also the class's methods *p*'s code did not
  call and those its checkpoint added (so that core and periphery are alike in kind; H1's
  bystanders stay fields only).
- **A use:** a later intrusion, as defined above (bound there; neither declared nor crossing),
  whose code in that method, or that class, uses one of those values. **A value counts once**, not
  each time it is used. **At the class, each method the later change's bound code is in is scored
  on its own** and the counts summed (decided by the author, 19 November 2026): a later change that
  edits two methods of the class and adds a third is three scores. Until then the class's methods
  were pooled and a value used in two of them counted once. Reported beside it: the class on its
  fields only, as until 19 November 2026.
- **The core's width** (reported): its number of values per row, per arm and over the thirds of
  the stream, the width of the sinew.
- **The outcome of H2** is the uses per value: of the core, and of the periphery. Its test is
  their ratio (§5).
- **A kind with no values gives no record.** A new method had nothing to be bound to, so it has
  no core at the method and is read there on its periphery only; a method whose added code used
  everything visible and introduced nothing has no periphery. Neither can read nought by
  definition, which the form of 17 November could (§7).
- **The core is relative to the problem.** A value is core for the problems bound to it. That
  one value is core for many problems is what H2 finds, if it holds; it is not assumed.
- **Reported beside it** (§5): how the bound uses of a place's values are spread over them; how
  much goes to values that were there before the first checkpoint; and how many of the values
  the changes introduced are ever used by later bound code.

**Drawn in by what stood by** (H2 from 17 to 19 November 2026; reported. Decided by the author,
17 November 2026, §9). That form of H2 is not about how many bindings a problem has. It is about the data that lay where the problem's code was put, and
whether that data is what later code is bound to. For a problem *p* and a host its bound code went
into:

- **What stood by at the class:** the fields of the host's class, as it was before the change
  (state, injected dependencies and constants, §4.3a), that *p*'s code in that host does not use.
- **What stood by at the method:** the host method's pre-existing parameters and locals visible
  where *p*'s code starts (§4.3a) that *p*'s code there does not use. A new method has none.
- **Drawn in by it:** a later intrusion, as defined above (bound there; neither declared nor
  crossing), whose code in that class, or that method, **uses** one of the values that stood by for
  *p*. A value added after *p* was placed did not stand by for *p*; a value *p* itself used did not
  stand by.
- **Its outcome** is the number of such later intrusions, at the class and at the method; its
  predictor is the number of values that stood by at that level.
- **Reported beside it:** per arm, how many of the later intrusions are bound to something that
  stood by, and the mean number that stood by.
- **Reported beside it, with what was introduced** (19 November 2026, §4.3b): the same outcome and
  predictor widened to what the change left in the place, what stood by and what it introduced
  there. A new method has nothing standing by, so under H2 as it is its row at the method can
  only read nought; under this reading its own parameters and locals count.
- **This is opportunity, and is meant to be.** A place where nothing stood by cannot draw anything
  by what stood by, so some rise is given by construction. The hypothesis is the mechanism: that
  data left in a place is taken up by the code that comes next, in proportion to how much is there,
  and not left unused. It would fail if later code came for the same few values however many more
  had gathered (§7).

**As built** (`tables.standing`, `tables.outcome_rows`, 17 November 2026): values are matched by
name within the class's, or the method's, identity. A field renamed between *p* and the later
checkpoint is not followed, and a local of the same name declared anew counts as the same value
(§7). Over the several runs a checkpoint adds to one host, a value stands by when one of them sees
it and none uses it.

**Reopening, reported** (17 November 2026). Per checkpoint: the classes its bound code goes into
that an earlier checkpoint's bound code had gone into; and the wiring files it changes that an
earlier checkpoint had created or changed. In the function arm the equivalent of the method that
calls the others is the flow configuration, so the wiring files are counted beside the classes; a
wiring file has no bindings, so every change to one counts. This was first written as a condition of
H4 on the count of places reopened, bound or not. On the development chain that count did not tell
the arms apart (§6): it counts a class once however many problems have piled into it, and it
counted the entity's new fields in both arms. It is kept as a reported reading.

**As built** (`tables.is_bound`, `tables.class_identities`, `tables.reopened`, `chain.measure`,
17 November 2026): a class's identity is its type name, carried through the instrument's matches
when a type is renamed or moved; a nested type is a class of its own. A wiring file's changes are
the YAML files under the wiring root that the checkpoint's commit adds, modifies, renames or
deletes.

### 4.5 Wiring (H4)

In the OfficeFloor arm, coupling that leaves a scope becomes configuration: flows, the objects
injected into a procedure, governance. For each addition, the **wiring edges added** (new links
in the application's configuration) are counted, and reported beside pull. This keeps the
coupling the form moves out of the code from going unreported.

**New injected dependencies are not edges** (decided by the author, 16 November 2026). A new
dependency creates mass, not pull: it is gravity only when a later change has no choice but to be
placed with it. That is measured where it happens, as the bindings of the later change (§4.3): in
Spring an injected dependency is a field, so later code using it is bound to its class. A wired
OfficeFloor function using an existing injected object is not bound by it, since any function can
declare it.

Two conditions of H4 are read on the wiring, as the SinewSlim analysis plan set them (its H4):

- **Growth:** the slope, over the checkpoint index, of the wiring edges added per addition. An
  interval above 0 means the wiring grows faster than the problems, and counts against H4.
- **Concentration:** at the final checkpoint, the share of the configuration's non-blank lines
  held by its largest file. Over 50% counts against H4.

**As built** (`placement_gravity/wiring.py`, 16 November 2026). The configuration is the YAML under
`src/main/resources/officefloor/`. An edge is a `next:` or an entry of an `outputs:` map; a line is
one that is neither blank nor only a comment. Growth is each chain's least-squares slope of the
edges added at each checkpoint over the checkpoint index; over chains, the mean slope with a
percentile bootstrap interval (chains resampled, 10,000 resamples, seed 20261116). Concentration is
each chain's share at its final checkpoint; over chains, the mean share against the 50% limit,
with its interval reported. New injected dependencies are not counted as edges (above).

### 4.6 Amount (conservation check)

Total positions and tokens per arm at each checkpoint, so that H4 is read against the
conservation result: the same amount, placed differently. H4's band is read at the final
checkpoint, averaged within a chain and then over chains, with a percentile bootstrap over chains.

**Revised before the start** (16 November 2026, §9): **the band is read on the amount added**, the
positions at the final checkpoint less those of the chain's base (`base_ref`), not on the total.
The petclinic arms start from two conversions of one application that differ in size (942 and 745
positions at cp1 of the development chain), so a ratio of totals reports the starting code as much
as the agent's. The ui stacks start empty, so there the two are the same. The ratio of totals is
reported beside it.

### 4.7 Shape (the competitors of H3)

The measures the earlier studies and the absorbed drafts used, each read on the **host** an
addition lands in, at *k − 1*, before the addition. A new host has none of them.

| Code | Measure | From |
|---|---|---|
| S1 | **Long:** 26 or more code lines (SinewSlim's lines) | the divergence study's length constant |
| S2 | **Not slimmable:** SinewSlim's conventional reading at the pinned version and its defaults, on both arms | the long-method-slim study; the SinewSlim analysis plan's M1 |
| S3 | **Junction:** the host hands on more data than it receives, *d = out − in > 0*. *in* counts every parameter, as for an ordinary method; *out* counts the arguments it passes on calls to the application's own methods. The injection-aware reading (*in* without injected parameters) is reported beside it | the flow-injection draft's junction |
| S4 | **Complexity outlier:** the host's cognitive complexity, and whether its modified z-score within the checkpoint exceeds 3.5 | the complexity-concentration study |
| S5 | **Concentration:** the host's size and the Gini coefficient of the class's positions over its methods | §4.2 |

**Two kinds of measure** (17 November 2026, §9). S1, S4 and S5 are shape as the literature reads
it (length, complexity, the god class's concentration), and are H3's block. S2 and S3 are **sinew
measures**: whether the data flowing through a method stops it being split, and whether it hands
on more data than it receives. They are the author's own, from SinewSlim and the flow-injection
draft, and nothing in the reviewed literature studies them as shape (`LITERATURE.md`; the nearest
relatives are fan-out and Henry and Kafura's information flow, which count flow between modules).
They describe data, which is this study's subject, so they are read apart from H3 with their own
stated direction (§5).

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
- S3's calls are matched to the application's methods by name and arity, lexically, as the bindings
  are (§7, *Lexical names*). A call on an object of another type with a matching name counts.
- S3 is conventional, not injection-aware. A wired OfficeFloor function receives only injected
  values: every function is a starting point. Leaving them out of *in* made any call such a function
  made with an argument a junction, so S3 measured whether a function calls anything (corrected
  16 November 2026, after the pilot: 65 of 92 OfficeFloor junctions at cp60 were wired functions).
  This differs from the bindings on purpose. Bindings ask what pins new code to its place, and an injected
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

### 4.7a The literature's shape measures, at the method and at the class

Added 17 November 2026 (§9), to be looked at on the development chain before any of them joins H3.
The measures are those the petclinic harness already reports for whole systems; here each is read
on the place an addition lands in, as it stood at *k* − 1, with the harness's tools at its pins.

| Level | Measure | From | Tool |
|---|---|---|---|
| Method | Cyclomatic complexity | McCabe 1976 | CK 0.7.0 |
| Method | NPath complexity | Nejmeh 1988 | PMD 7.27.0 |
| Method | Deepest nesting | (CK's `maxNestedBlocks`) | CK |
| Method | Fan-out | (classes the method uses) | CK |
| Method | Halstead volume | Halstead 1977 | this study, over the method's text |
| Method | Maintainability Index | Oman and Hagemeister 1992 | from the volume, cyclomatic complexity and lines |
| Method | Law of Demeter violation (flag) | Lieberherr 1989 | PMD |
| Method | Holds cloned lines (flag) | | jscpd 5.0.14 |
| Class | WMC, RFC, DIT, CBO | Chidamber and Kemerer 1994 | CK |
| Class | LCOM*, TCC | Chidamber and Kemerer; Bieman and Kang 1995 | CK |
| Class | Fan-out, import count | | CK, PMD |
| Class | Halstead volume, Maintainability Index | as above | over the class's text |
| Class | God Class (flag), Data Class (flag) | Lanza and Marinescu 2006 | PMD |
| Class | Law of Demeter violation (flag), holds cloned lines (flag) | as above | PMD, jscpd |

- A method measure is defined for an existing host. A class measure is that of the host's class at
  *k* − 1, also for a new method of a class that existed.
- A tool that does not run leaves its measures empty, never zero. Without npm, jscpd is not
  installed and the two clone flags are empty.
- **As built** (`placement_gravity/literature.py`, `tests/test_literature.py`): CK's methods are
  joined to the instrument's by file and declaration line, PMD's findings by file and line. CK's
  TCC counts direct field access only. Halstead's operands are identifiers and literals, its
  operators keywords and symbols, comments left out.

## 5. Analysis

- **Unit:** an addition run (Q2, H1, H4) or a problem and host whose code was bound there (Q3, H2,
  H3, H4), nested in checkpoints nested in chains.
- **The problem is held fixed by its identity** (revised before the start, 16 November 2026, §9).
  Every checkpoint is one problem, solved once by every chain of both arms. Every model
  therefore carries a **random intercept for the checkpoint**, crossed with the chain's. A
  comparison is then between placements of the same problem, and the size and the declared
  crossings are no longer the only stand-ins for it. A model that does not converge with the
  checkpoint intercept is refitted without it, and the report says so.
- **H1** (restated 17 November 2026, §9): a mixed model of log(1 + bystanders) per run of added
  logic that needs a pre-existing value (§4.3a), on the checkpoint index, in the methods arm, with random intercepts for the chain and the
  checkpoint. The slope is reported with a 95% bootstrap interval over chains. Host size is not in
  the model: a larger method has more values by construction, so a slope on it would not be
  evidence.
  - **Within a place** (17 November 2026, §9): the same model twice more. On the class's
    bystanders, with the checkpoint index split into the mean checkpoint of the runs in that class
    (of that chain) and the run's difference from it; and on the method's bystanders, the same
    within the method. The slope read is the one on the difference: how much more stands by for a
    later run than for an earlier one in the same place. A class or method with runs at only one
    checkpoint adds nothing to it. H1 is supported when all three slopes have a 95% bootstrap
    interval above 0.
  - **Reported beside it:** the same model on method bystanders and on class bystanders, without
    injected dependencies, and without constants; the slopes within a place in the function arm;
    and H1 as first registered, log(1 + bindings) on
    log(host positions) and the checkpoint index, on runs into existing methods.
- **The base model of H2 and H3:** a negative binomial model, per problem and host whose code was
  bound there (§4.4), of later intrusion (H3, H4), of the later intrusions' uses of the core and
  of the periphery (H2), or of the later intrusions bound to what stood by (H2 as it stood). It holds the problem fixed: the checkpoint's intercept, the addition's size, its declared
  crossings, host size, whether the host is new, and act. A new host has almost no bindings and a
  different later life from an existing one (on the development chain, Spring's new hosts averaged
  0.31 bindings and existing ones 1.81), so without the new-host term that contrast alone could carry
  a difference. Host size also stands for the plain fact that a longer method has more values in it.
- **H2** (restated 19 November 2026, §9): in the methods arm, at the **class** (its fields) and at
  the **method** (its values), each bound problem and host gives up to two records (§4.4): one
  for its core and one for its periphery, where it has at least one value of that kind. The
  outcome is the later intrusions' uses of the values of that kind; the offset is the log of the
  later checkpoints plus the log of the number of values of that kind, so the model is of uses
  per value; the term is whether the record is the core's, added to the base model. It is
  supported when the incidence rate ratio of the core to the periphery has a 95% interval above 1
  at both levels.
  - **Reported beside it:** the same ratio in the function arm, where each function is handed its
    own data and little core is expected to form; and per arm, pooled over places, the share of
    bound uses that go to each chain's three most used values, the share that go to values no
    checkpoint introduced, and the share of introduced values that later bound code uses.
  - **Reported, H2 as it stood from 17 to 19 November 2026:** the number of values that stood by
    (§4.4) added to the base model, on the later intrusions bound to what stood by, as a rate
    ratio per value that stood by, at the class and at the method. With it: the same on
    log(1 + the number that stood by); the same in the function
    arm; the same with what the change introduced counted beside what stood by (§4.3b: the later
    intrusions bound to either, per value of both, in each arm); and H2 as it stood, the bindings added to the base model on later intrusion, at the class and
    the method, with its own readings (on the problem's own lines, for information; on existing
    hosts only; with bindings to injected dependencies left out).
- **H3** (its measures and levels set 18 November 2026, §9): six measures, each fitted **alone**,
  as *The literature's measures, each alone* below describes. At the **method**, on existing
  hosts: long, cognitive complexity and cyclomatic complexity, added to the base model with the
  bindings and the method's bystanders, on intrusion at the method. At the **class**, one row per
  class and checkpoint with the class's size held fixed: the Gini of the class's positions, WMC
  and LCOM*, on intrusion at the class. They are fitted one at a time because they are rival
  readings of the same thing (the two complexities; weight and concentration), and together could
  not be told apart; so H3 says of each that it does not draw code in, not that each adds nothing
  beyond the others. The block as first registered (S1, S4 and S5 together in one model at the
  method) is reported.
  - **The method level is the test** (decided by the author, 18 November 2026): it is where the
    arms are compared, since a function is OfficeFloor's unit of placement.
  - **The class measures are tested only where classes can be told apart** (18 November 2026,
    §9). They enter H3 in an analysis only when later bound arrivals fall in **at least 10
    distinct classes** (a class counted by its name over all chains) and **no one class holds
    more than half** of them. Otherwise they are reported, each alone, and H3 is read on the
    method measures. The petclinic stream sends every rule through one endpoint, so one class
    there receives nearly all the arrivals and a class measure describes that class over time,
    not a difference between classes (§6); the ui stream, with many endpoints, is where the class
    level is expected to be testable. H3 is supported when every shape measure's incidence rate ratio
  has a 90% interval whose upper limit is below 1.25, the upper margin (one-sided, 17 November
  2026, §9; the margin of 0.8 to 1.25 was decided 16 November 2026), per
  standard deviation for continuous measures and present against absent for flags. A null is not
  taken from a non-significant test: an interval that reaches above 1.25 is unresolved, and one
  wholly above it counts against. Reported beside it: the two-sided reading, each interval inside
  0.8 to 1.25. The same block on class-level intrusion is reported.
  - **How the shape block enters** (decided 16 November 2026). S4 enters as a level, log(1 + cognitive complexity),
    because cognitive complexity is zero-heavy and the outlier flag then marks any control flow
    (the pilot: 45% of Spring's existing hosts); the flag is reported beside it. A shape measure
    that does not vary in a corpus, with fewer than 10 hosts flagged over all chains of an arm,
    leaves the block for that corpus. It is reported as not testable there, never as meeting the
    margin, and H3 is read on the measures that remain.
  - **Reported beside it:** the shape block in a model *without* the problem terms and pull. This
    shows how much of shape's apparent association comes from leaving the problem out. Each shape
    measure alone, and the change in fit for every block, are also reported.
  - **The literature's measures, each alone** (reported; 17 November 2026, §9): each measure of
    §4.7a added by itself, at its own level. A method measure: to the base model with the bindings and
    what stood by in the method, on intrusion at the method, on existing hosts. A class measure
    (revised 18 November 2026, §9): on intrusion at the class, with **one row per class a
    checkpoint's bound code went into** and not one per method; the class's size at *k* − 1 (log of
    its positions) held fixed in place of the method's; an intercept for the class (dropped, and
    marked, where the model then gives no standard error); the bindings the most of the
    checkpoint's hosts in the class, what stood by the least. A measure where higher is the better
    shape (the Maintainability Index, TCC) is **reversed**, so a ratio above 1 always means the
    worse shape is followed by more. Per standard deviation (of log(1 + x) for counts, of
    the value for ratios and the index), or present against absent. Read as H3 is, against the
    upper margin, with the variation rule. They are fitted one at a time because they measure
    overlapping things (cyclomatic, cognitive and NPath complexity; WMC and the God Class), and
    together would not be told apart. **Which of them are H3's** was decided by the author on 18
    November 2026, after they were seen on the development chain (§6): cyclomatic complexity, WMC
    and LCOM* join long, cognitive complexity and the class's Gini. NPath and nesting repeat
    complexity, and Halstead volume and the Maintainability Index are largely size; they stay
    reported. The detectors (God Class, Data Class), TCC, Law of Demeter and clones are reported
    where they vary.
  - **The sinew measures** (reported with a stated direction, not confirmatory; 17 November 2026,
    §9): S2 and S3 added to the same base model with the bindings and the bystanders, in place of
    the shape block, on intrusion at the method and at the class. Predicted: each rate ratio above
    1. A method that data flows out of, or that its data flow holds together, is expected to be
    come back to more: that is data gravity seen from the method's side, and it would count for the
    study's claim, not against H3. The variation rule applies to each as it does to the shape
    measures.
  - **Reach** (reported with the sinew measures, predicted above 1; 18 November 2026, §9): the
    method's fan-out and the class's CBO and fan-out, each alone as above. They count what a place
    reaches out to, which is how data comes to flow through it, and not its size or its tangle.
    They were placed here after fan-out was seen above the margin on the development chain (§6).
  - **Junction × arm (secondary, corpus A):** the S3 junction flag, the arm and their interaction,
    added to the model with pull. It asks whether a junction is followed by the same intrusion in
    both arms. In OfficeFloor a function is a starting point: a junction there hands its values on
    from an injection point, and is expected to stay contained to it. The reading is the
    interaction's incidence rate ratio with its 95% interval. An interval below 1 means that
    OfficeFloor's junctions are followed by less intrusion than Spring's; an interval above 1 means
    more. It is repeated with the injection-aware junction. It is not among the confirmatory tests
    and does not change any verdict.
- **H4** (restated 17 November 2026, §9): the arm term and its interaction with the checkpoint
  index in the H1 model, on the paired chains, with the amount band (§4.6) and the two wiring
  conditions (§4.5). The checkpoint index is centred at the middle of the stream, so the arm term
  is the difference between the arms half-way through. Both have to be below 0: the function arm
  has fewer bystanders, and they grow more slowly.
  - **Come back to less** (17 November 2026, §4.4): the arm term of the base model of H2 and H3,
    without the bindings (the arm itself changes them), on intrusion at the class and at the method.
    The function arm's rate ratio has to have a 95% interval below 1 at both levels.
  - **Reported, how much a core value is come back to** (19 November 2026): the core's records of
    H2 (§4.4), both arms, in the base model with the arm term, at the class and at the method; the
    function arm's rate ratio per core value, with its interval. With it, per arm, the uses of
    core and of periphery values per 100 values and later checkpoints. Predicted below 1.
  - **Reported:** reopening per checkpoint (§4.4), a Poisson mixed model on the arm, for the
    classes and for the classes with the wiring files.
  - **Reported beside it:** H4 as first registered, on the bindings: the arm term and its interaction
    with host size, as below.
  - **Host size is centred, in the binding-based reading** (16 November 2026, §9): log(host positions)
    less its mean over the rows of the model, both arms together. With an interaction in the model,
    the arm term is the difference between the arms where the centred host size is 0. Uncentred,
    that is a host of one position, which no host is. Centred, it is the difference at a typical
    host. The difference is also reported at hosts of 10, 25 and 50 positions.
- **H4 without the injection rule:** bystanders count injected parameters like any other, so the
  restated H4 does not rest on the rule that an injected parameter is not a binding. The binding-based
  reading does: a wired OfficeFloor function's parameters cannot be bindings by definition. It is
  therefore repeated with bindings counted from locals, fields and methods only, leaving out parameters
  in both arms, and reported.
- **Without injected dependencies** (reported, §4.3): H1 at method and class level, H4 and H2,
  each with bindings to injected dependencies left out. These do not change any verdict.
- **Choice at a checkpoint** (reported; added 16 November 2026, §9). Per checkpoint and arm, over
  the chains: the share of chains that placed any of the addition in an existing host, the number
  of distinct hosts the chains used between them, and the standard deviation of the bindings per
  addition. A checkpoint where every chain made the same placement with the same bindings left no
  choice; one where the chains differ did.
- **Formation** (reported with a stated direction, not confirmatory; added 16 November 2026, §9).
  Read within each arm, never across arms.
  - **Lagged:** the H1 model, with its checkpoint intercept, and one more term: the chain's mean
    bindings per run over all its checkpoints before *k*. Predicted: positive in the methods arm. For
    the same problem, a chain that has been forced more so far is bound more now.
  - **Where it ends:** over the chains of an arm, Spearman's correlation between the mean bindings per
    run in the first third of the stream and the share of the tree's positions held by its largest
    method at the final checkpoint. Predicted: positive in the methods arm. With about nine chains
    this is a direction with a wide interval (bootstrap over chains), and is reported as that.
  - The function arm is reported the same way. The expectation is that there is little to form:
    a weaker or absent relation.
  - Both are observational: a chain is not assigned its early placements. They show whether the
    path exists, not that the early placement caused the later one.
- **Review** (reported with a stated direction, not confirmatory; added 16 November 2026, §9). The
  `reviewed` run (`blind-202609290948`) is set against the petclinic just-solve run `blind-202608100006`, per arm. This is
  the one reading that sets two conditions side by side; neither run's hypothesis tests are pooled.
  - Per checkpoint *k*: *T* is the mean bindings per run of the just-solve chains; *D* is the absolute
    difference between the two conditions in the share of the addition's positions that land in
    existing hosts, each averaged over its chains.
  - Predicted: Spearman's correlation of *T* and *D* over the checkpoints is negative. The review
    changes the placement where the bindings are few, and leaves it where they are many. No direction is
    predicted for *which way* the review moves a placement: the conservation paper found it
    consolidating OfficeFloor's pipeline (§6).
  - A correlation of zero or above counts against reading bindings as the absence of choice.
- **Size or data** (reported with a stated direction, not confirmatory; added 17 November 2026,
  §9). The author's claim: size attracts, but as a proxy for the data that made it. Within the
  methods arm the two cannot be told apart, because a place that holds more data is larger (§6).
  The arms can separate them: they add about the same amount of code (§4.6), and the function arm
  leaves far less standing by.
  - The base model on later intrusion (§4.4), every bound problem and host of **both arms, without
    the arm term**, with the number that stood by and the size of the place: at the method,
    log(1 + host positions); at the class, also log(1 + the class's positions at *k* − 1), on the
    hosts that existed then.
  - Predicted: the rate ratio per value that stood by is above 1, at the class and at the method,
    with size held fixed.
  - Reported beside it: the size's rate ratio in the same model, and with what stood by left out;
    both again with the arm term, which is the comparison within arms; and Spearman's correlation
    of size with what stood by, pooled and per arm.
  - It leans on the arm contrast: anything else that differs between the arms and bears on later
    intrusion is carried by the two terms. That is why it is a reading and not a hypothesis. If it
    is clear on the petclinic runs, it may be registered as a hypothesis for the ui runs by a dated
    amendment made before their backend Java is read.
- **Where bound and unbound code lands** (reported, no direction stated; added 17 November 2026,
  §9). The author's question: a place has two kinds of size, the data available there and its
  shape. Bound code went where its data was; is that also where the complexity is? And unbound
  code, which nothing held to a place: does it go where the complexity is, where the data is, or
  away from both, to a new place? If shape influences choice, it is the unbound code that would
  show it.
  - **Candidates:** at each checkpoint, every method and every class of the tree as it stood before
    the change (the shape pass of §4.7 already reads them).
  - **Two sizes of a place.** Shape: positions and cognitive complexity (a class: summed over its
    methods). Data width: a method's parameters and locals with its class's fields; a class's
    fields (state, injected dependencies and constants).
  - **A landing** is one host a checkpoint adds logic to (moved code left out), bound or unbound
    (§4.3), with its destination: an existing method, a new method in an existing class, or a new
    class.
  - **The rank of the place landed in** among that checkpoint's candidates, on each size: the share
    of candidates below it, counting half of those equal. 0.5 is no regard to that size.
  - **Reported per arm, for bound and unbound landings:** the shares of the three destinations;
    the mean rank on complexity and on data width, at the method (landings into existing methods)
    and at the class (landings into existing classes); and Spearman's correlation of the two ranks
    over the places landed in, which says whether the two kinds of size point to the same places.
  - **What it cannot say:** unbound is not free. Code can belong to a class by convention without
    using any of its data, and most classes of a tree are small, so a mean rank well above 0.5 is
    expected of almost any code that enters an existing class. The reading is therefore between
    bound and unbound, and between the arms, not against 0.5. It replaces nothing: H3 stands as it
    is until this has been looked at on the development chain.
- **Corpus B and corpus C** (§3.2, §3.3; extended 18 November 2026, to H5 on 19 November 2026 and to H6 on 20 November 2026): the H1, H2, H5 and H6 models with a
  random intercept for the repository in place of the chain's and the checkpoint's, the index the
  commit's place in the repository's order. Direction and interval only. The two comparisons of
  §3.3 are the same models with a term for the declared agent commit (within a repository) or for
  the corpus (between them), and the destination of unbound code as a binomial model on the same
  term.
- **H5** (19 November 2026): per bound host and level, its alternatives (§4.2a) as a negative
  binomial (nbinom2) mixed model on the checkpoint index scaled from 0 (the first checkpoint) to 1
  (the last), with the chain's intercept, in the methods arm: exp(slope) is the ratio of the end
  of the stream to its start. One-sided against the upper margin (1.25), 90% interval, at the class
  and at the method, each needed; p is the larger of the two. A level where every placement was
  forced (no alternative anywhere) cannot rise, cannot be fitted, and passes with p 0. Reported:
  the share forced and the mean alternatives per arm and third; the function arm's ratio; the arm
  × index interaction's arm term; the share of class rows bound to the class's own values; the
  method values of no declared type. The verdicts are as H3's (unresolved: reaching above the
  margin without lying above it).
- **H6** (20 November 2026): per unit that placed or edited code in an existing class, its spread
  (§4.2b) as a negative binomial (nbinom2) mixed model on whether the unit was forced and the index
  scaled from 0 to 1, with the chain's intercept, in the methods arm (*forced*: the ratio of the
  spread of a forced unit to one that was not, at the same point in the stream). One-sided above
  1, 95% Wald interval; reversed if the interval lies wholly below 1. Reported: the spread on the
  index alone (*rise*: exp(slope), the end of the stream against its start), over all units and in
  forced and in unforced units apart. Every H6 model holds the change's size fixed: log(1 +
  positions it added) and log(1 + methods it placed or edited code in) (20 November 2026, §9 row
  61); the forced ratio without them is reported. A spread
  with less variance than its mean, where the negative binomial cannot be fitted (its Hessian not
  positive definite), is fitted as Poisson, and that is recorded. Reported: the spread per arm and
  third, and against forced; the function arm's forced ratio and rise; the arm × index
  interaction's arm term; the growth and coupling accountings (§4.2b); the
  coupling of pairs changed together more than once, a negative binomial model of it on the index
  with intercepts for the chain and the pair; the pairs changed together, how many more than once,
  in how many of those coupling rose or fell, and the candidates by name.
- **H7** (20 November 2026): per unit and existing class it changed, the calls added across the
  class's boundary (§4.2c) as a negative binomial (nbinom2) mixed model on whether the class was
  forced and the index scaled from 0 to 1, with the chain's intercept, in the methods arm
  (*forced*: the ratio of a forced class's added calls to an unforced one's at the same point in
  the stream and of the same size: log(1 + positions the unit added to the class) and log(1 +
  methods it changed there) in the model, §9 row 61; the ratio without them reported). One-sided above 1, 95% Wald interval; reversed if the interval lies wholly below 1.
  Poisson where the negative binomial cannot be fitted, recorded. Reported: the same model for
  the calls reaching an exposed or widened member, for outward and inward calls apart, and for
  the members opened; the added calls on the index alone (rise); the function arm's forced ratio;
  the arm term with forced and the index in the model; per arm, forced against unforced rows, the
  calls added a row and the share reaching an exposed or widened member.
- **Multiplicity** (21 November 2026, §9 row 66): the confirmatory family H2, H4, H5, H6 and H7,
  Holm-corrected at α = 0.05. H1 and H3 are secondary, each decided at α = 0.05 on its own p
  outside the correction and reported as secondary. (Until 20 November 2026, every hypothesis was
  in one Holm family: four, then five, six and seven.) All else is descriptive.

**As built** (`analysis/analyse.R` with glmmTMB, `placement_gravity/prepare.py` and
`placement_gravity/verdict.py`, 16 November 2026; R chosen by the author for glmmTMB's negative
binomial mixed model). These details are fixed with the code before any run is read:

- **Each analysis is read on its own** (`runs.yaml`): the ui primary, which is the study's test,
  and each petclinic analysis, a replication. An analysis with fewer than 6 chains in an arm is descriptive only.
- **H1 and H4** are fitted on runs of added logic into **existing** methods: a new method has no
  prior size, so including new methods would make "more bindings in bigger hosts" true by
  construction. Gaussian mixed models of log(1 + bindings) on log(host positions) and the checkpoint
  index, random intercepts per chain and per checkpoint; H4 adds the arm and its interaction with host
  size, centred (and the front end, where the analysis has more than one). Intervals: a cluster bootstrap, chains resampled
  with replacement within arm and the model refitted, **1,000 refits, seed 20261116**. One-sided
  p-values are the bootstrap share on the wrong side of 0, (k + 1) / (n + 1).
- **H2 and H3** are negative binomial (nbinom2) mixed models of later intrusion per problem and
  host, at the class and at the method (§4.4), offset by log(later checkpoints), random intercepts per chain and per
  checkpoint. Its base terms are log(1 + the problem's positions added), the problem's declared
  crossings (the checkpoints it mutates or crosses), log(1 + host positions), whether the host is
  new, the act (the ui stream only; petclinic has no
  acts), the arm and, where present, the front end. **H2** is read on every bound problem and host of the methods arm,
  with a one-sided Wald test at each level; **H3** on existing hosts with their shape at k − 1, by one
  one-sided Wald test per shape measure against the upper margin (90% intervals; the two one-sided
  tests of the two-sided reading are reported). S4 enters as log(1 + cognitive complexity) and S5
  as the class Gini, both standardised; S1 to S3 as 0/1.
- **The p-value of each hypothesis** for Holm is the larger of its parts: H1, of its three slopes
  (over all runs, within a class, within a method);
  H2, of the class level and the method level; H3, of every shape measure's one-sided test; H4, of the arm
  term, the interaction and the arm's rate ratio in intrusion at the class and at the method; H5, of
  the class level and the method level; H6 and H7, each its forced ratio's. A hypothesis is
  supported when its Holm-adjusted p (over the seven) is at most 0.05 **and** its conditions hold (H4: the amount in its band and neither wiring
  condition against). The verdicts are supported, not supported, reversed (an interval wholly on
  the wrong side), unresolved (H3 and H5: an interval reaching above the upper margin), not testable (H3: no
  shape measure varies) or descriptive only.
- **The revisions of 16 November 2026** (§9) are built: the checkpoint intercept, the centred host
  size, the new-host term and the lagged formation term in `analysis/analyse.R` (its self-test
  simulates a level per checkpoint and recovers each effect); intrusion on a problem's own lines in
  `placement_gravity/lines.py`; the amount added in `prepare.amount`; the choice, formation and
  review readings in `placement_gravity/readings.py`. Each has fixtures with known answers.
  - *The checkpoint intercept's fallback:* a model is refitted without it when the fit does not
    converge or its Hessian is not positive definite; each report lists which models carry it.
  - *The lagged term* counts every run of added logic (new and existing hosts, moved code left
    out) at the chain's earlier checkpoints.
  - *Choice:* a checkpoint "left no choice" when every chain has the same bindings and all are on the
    same side of new or existing host.
  - *Review:* its interval resamples the chains of each condition (2,000 resamples, seed 20261116);
    the formation correlation's interval resamples chains (10,000). Either is given only with four
    or more chains.
- **The bystanders** (§4.3a) and H1 and H4 as restated on 17 November 2026 are built: the visible
  and needed values per run and the fields a class is left with (`instrument/Pull.java`,
  `tests/test_bystanders.py`); `by.csv` and `capture.csv` (`prepare.py`); the models
  (`analysis/analyse.R`, whose self-test simulates bystanders rising in one arm and recovers H1,
  H4, the equal needs and capture); the verdicts (`verdict.py`: H1 on its one slope).
  - *Visible:* a local is visible where a run starts when it is declared on an earlier line and its
    nearest enclosing block, loop, try, switch entry or lambda encloses that line.
  - *H4's centre* is the middle of the stream, (checkpoints + 1) / 2.
  - *Capture* is a Gaussian mixed model of the share on log(1 + the heaviest class's fields), per
    arm, with Wald intervals.
- **H1 within a place and H2 as restated** (17 November 2026, §9) are built: what stood by per
  host and the later intrusions bound to it (`tables.standing`, `tables.outcome_rows`,
  `tests/test_stream.py`); the class and method each run is in (`prepare.by_rows`); the models
  (`analysis/analyse.R`, whose self-test simulates both and recovers them); the verdicts
  (`verdict.py`: H1 on its three slopes, H2 on the bystanders' rate ratio at both levels).
  - *H1 within a place* has the same bootstrap as H1 (chains resampled, 1,000 refits); a place is a
    class, or a method, of one chain.
  - *H2 as it then stood* is refused as not estimable at a level where the number that stood by
    does not vary.
- **H2 as restated on 19 November 2026** is built: the core and the periphery of each bound row
  and the later intrusions' uses of each, value by value (`tables.outcome_rows`,
  `tests/test_stream.py`); the two records per row and the model (`analysis/analyse.R`, whose
  self-test simulates a core used three times as much per value and recovers it); the spread of
  bound uses over values (`readings.core_summary`). The verdict's rule is unchanged: the ratio's
  interval above 1 at both levels (`verdict.py`). A level with no record of one kind, or no use
  at all, is reported as not estimable. The two records of one row share its later arrivals, and
  the model carries no term for the row (§7).
- **Introduced** (§4.3b, 19 November 2026) is built: the instrument names the values a change adds
  to a method and the fields it adds to a class (`Pull.java` version 11); each host and outcome
  row carries them, with the later intrusions bound to one (`tables.py`); `h2.csv` carries the
  counts (`prepare.py`); the reading of H2 on what stood by and what was introduced is in
  `analysis/analyse.R` (`H2_left_class`, `H2_left_method`; its self-test simulates and recovers
  it). It enters no verdict.

## 6. What was known when this was written

- **Seen.** The conversation that produced this plan. Step 7 of `long-method-slim-study`
  (width profiles, the 20-repository pilot): profiles are a continuum; width grows sub-linearly
  with length (pooled exponent 0.57) and flattens past about 44 positions. The conservation
  paper's results, including that its AI-reviewed condition consolidated the OfficeFloor
  pipeline, raising concentration. That result is the reason H4 is not assumed and the wiring is
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
  descriptive only (`results/analysis/pilot/REPORT.md`). Seen: H2's rate ratio per binding 0.90
  [0.63, 1.30]; with the problem and bindings held fixed, the junction 1.11 [0.52, 2.35], cognitive
  complexity 0.54 [0.35, 0.85] and the class Gini 0.44 [0.25, 0.76] (90% intervals); the junction
  without them 5.34 [2.38, 12.0]; junction × arm 0.20 [0.04, 1.01]; H1's slopes 0.025 on host size
  and 0.006 on the checkpoint; H4's arm term −0.64 and interaction 0.13. That chain is excluded
  from every registered analysis, and nothing in the plan was changed after these were seen.
- **Bindings to injected dependencies** (§4.3, added 16 November 2026 after `plan-v1` was first tagged,
  and before any run named for analysis was read; the tag was moved to include it), on the
  development chain only: of Spring's 74 runs
  into existing methods, 12 used an injected dependency; leaving those bindings out, the runs with a
  class binding fall from 20 to 10 and the forced runs from 71 to 67. Every class binding to `clinicService`
  and `ownerMapper`, the controller's constructor-injected dependencies, is counted as injected.
  OfficeFloor's runs into existing methods used none. The pilot raised six decisions (PILOT.md, *Decisions*), which are
  settled at registration.
- **The review before the start** (16 November 2026, on the development chain only, after
  `plan-v1` and before any run named for analysis was read). Seen, and the reason for the revisions
  of §9: Spring's 396 host-level intrusions all fall in methods holding several problems, one method
  holding 26; Spring's new hosts average 0.31 bindings and 0.005 intrusions per later checkpoint, its
  existing hosts 1.81 and 0.24; H2's model refitted with an intercept per host gave a host standard
  deviation of 2.7 and took the host-size coefficient from 1.27 to −0.07 (its standard errors did
  not compute); a simulation of the H2 test under no effect, with that dependence between rows,
  did not reject too often (the standard deviation of z was 0.82); with only Run A, the ui model
  drops the front end and the arm term carries it. Nothing was computed with the checkpoint
  intercept, on a problem's own lines, with the centred host size, or for the formation and review
  readings.
- **The revised steps on the development chain** (16 November 2026, after the revisions of §9 were
  written into this plan and built; one chain per arm, descriptive only,
  `results/analysis/pilot/REPORT.md`). Seen: on a problem's own lines Spring has 23 intrusions and
  OfficeFloor 26, where the host-level count had 396 and 44; no line was lost track of (569 and 616
  placed); H2's rate ratio per binding 1.17 [0.76, 1.81]; the junction 0.52 [0.17, 1.63], cognitive
  complexity 1.59 [0.77, 3.27] and the class Gini 0.32 [0.13, 0.82] (90% intervals); H1's slopes
  0.030 and 0.006; H4's arm term −0.40 at the centre (a host of 7.3 positions) and interaction
  0.046, the arm difference −0.39, −0.35 and −0.32 at 10, 25 and 50 positions; without parameter
  bindings −0.20 [−0.37, −0.04]; the amount added 1.08 (totals 0.88); the lagged formation term −0.36
  [−2.16, 1.44] in Spring. With one chain per arm H2's model fell back to no checkpoint
  intercept. Nothing in the plan was changed after these were seen.
- **Bystanders on the development chain** (17 November 2026; a scratch copy of the instrument, one
  chain per arm). **H1 and H4 were restated after these were seen**, so on this chain they are
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
  against 2.2 in OfficeFloor, rising in both (3.4, 4.6, 6.0 against 1.6, 2.3, 2.7), H4's
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
  slope 0.015, and 0.003 [−0.005, 0.012] without constants; H4's arm term −1.59 and interaction
  −0.017. So on this chain the level differs with or without constants, and the growth is the
  constants. Fields left in existing classes per addition: 0.61 in Spring, 0.46 in OfficeFloor.
  Capture: 0.32 [0.06, 0.57] in Spring and 0.22 [0.02, 0.41] in OfficeFloor; with one chain per
  arm the heaviest class only grows with the checkpoint, so this cannot yet be told from time.
  Nothing in the plan was changed after these were seen.
- **The fourth revision on the development chain** (17 November 2026; one chain per arm,
  descriptive only, `results/analysis/pilot/REPORT.md`). Seen, in the order it was built:
  - *Before the binding rule* (any later change counted): per problem and host, 10.9 later intrusions at
    the class in Spring against 2.1 in OfficeFloor, 2.3 against 0.23 at the method, 0.13 against 0.14
    on own lines. Places reopened per checkpoint, as first written into H4: 1.33 classes in Spring;
    1.35 classes and 0.45 wiring files in OfficeFloor; ratio 1.35 [1.01, 1.80], against H4. **The
    author's rule that intrusion applies only where there is a binding, and the replacement of the
    reopening count by the arm's rate ratio in intrusion, were decided after seeing this.**
  - *With the binding rule:* 89 of Spring's 174 problem and host rows and 31 of OfficeFloor's 192 are
    bound and followed. Per bound row: 11.9 later bound arrivals at the class against 0.84, 3.3
    against 0.10 at the method. H2's rate ratio per binding 0.89 [0.75, 1.06] at the class and 0.85
    [0.61, 1.20] at the method: below 1, not the direction predicted. H3 at the method: the
    junction 0.84 [0.35, 2.00], cognitive complexity 0.36 [0.22, 0.60], the class Gini 0.71
    [0.43, 1.17], so against (complexity lies wholly below the margin). H4: the arm's rate ratio in
    intrusion 0.16 [0.10, 0.27] at the class and 0.11 [0.03, 0.43] at the method. Reopening,
    reported: bound classes 0.26 [0.15, 0.48]; with the wiring files 0.77 [0.52, 1.16].
  Nothing in the plan was changed after the figures with the binding rule were seen.
- **H2 as restated, on the development chain** (17 November 2026; one chain per arm, descriptive
  only). **H2 was restated, and H1 extended, by the author before any of this was computed; the
  operational form of §4.4 and §5 was written after the first look below**, so on this chain
  neither is a prediction.
  - *A first look, in scratch:* in Spring's controller class the fields standing by rose from 4 to
    16 over 41 bound arrivals, and in its `addOwner` method the values standing by from 0 to 13 over
    25; of later bound arrivals 44% at the class and 16% at the method used something that had stood
    by; OfficeFloor had 40 later arrivals at the class in all, 3 of them such.
  - *As built* (`results/analysis/pilot/REPORT.md`): H1's slope within a class 0.026 (3 classes)
    and within a method 0.023 (11 methods), beside 0.015 over all runs; in OfficeFloor 0.001 and
    −0.001. Per bound row in Spring 7.5 fields and 2.2 method values stood by; 449 of 1,056 later
    intrusions at the class (43%) and 43 of 292 at the method (15%) were bound to one of them; in
    OfficeFloor 3 of 26 and 1 of 3. H2's rate ratio per field that stood by 1.10 [1.04, 1.16] at
    the class; at the method the model gave no standard error on this one chain (43 events), so H2
    was not estimable there. H3 with the bystanders in its model: the junction 0.71 [0.30, 1.67],
    cognitive complexity 0.38 [0.23, 0.63], the class Gini 0.68 [0.41, 1.12], still against.
  Nothing in the plan was changed after the built figures were seen.
- **Size or data, on the development chain** (17 November 2026; one chain per arm, descriptive
  only). *Before the reading was written*, a scratch look within Spring: size and what stood by
  correlate 0.87 at the method and 0.94 at the class; size alone 3.20 [2.42, 4.23] at the method
  and 1.22 [1.01, 1.47] at the class; with both in the model size 4.43 and 1.89, and what stood by
  0.88 [0.78, 0.99] and 0.92 [0.87, 0.96], below 1. So within the methods arm, on this chain, size
  was not explained away, and the two could not be separated. The pooled reading was added after
  seeing this. *As built, pooled*
  (`results/analysis/pilot/REPORT.md`): per value that stood by, with size held fixed, 0.88
  [0.84, 0.92] at the class (77 rows) and 0.89 [0.77, 1.03] at the method (109 rows), **below 1,
  against the stated direction**; size with what stood by held fixed 3.05 [2.08, 4.48] and 4.80
  [2.52, 9.14]; size alone 1.78 and 3.27. Pooling did not separate the two on this chain: the
  correlation of size with what stood by is 0.95 pooled at the class and 0.81 at the method (0.57
  and 0.50 within OfficeFloor, which has 26 bound rows). Nothing in the plan was changed after
  these were seen.
- **Where bound and unbound code lands, on the development chain** (17 November 2026; one chain
  per arm, descriptive only). *Before the reading was written*, from the tables as they stood:
  Spring's unbound runs went 5% into existing methods, 77% into new methods of existing classes
  and 18% into new classes; OfficeFloor's 24%, 19% and 57%. *As built*
  (`results/analysis/pilot/REPORT.md`), per landing: Spring's 85 unbound landings went 2%, 78% and
  20%, OfficeFloor's 161 went 16%, 35% and 49%; bound landings went into existing methods 67% in
  Spring and 87% in OfficeFloor, and never into a new class. Mean rank of the class landed in, on
  complexity and on fields: Spring bound 0.92 and 0.93, Spring unbound 0.93 and 0.83; OfficeFloor
  bound 0.82 and 0.59, unbound 0.78 and 0.68. Of the method landed in, on complexity and data
  width: Spring bound 0.80 and 0.88; OfficeFloor bound 0.76 and 0.62, unbound 0.55 and 0.38 (25
  landings); Spring had 2 unbound landings into existing methods. The two ranks agree over Spring's
  bound landings at the class (rho 0.96) and less elsewhere (0.26 to 0.77). Nothing in the plan was
  changed after these were seen.
- **H3 made one-sided** (17 November 2026, decided by the author **after** the figures above). On
  the development chain the two-sided H3 was against on cognitive complexity, 0.38 [0.23, 0.63]:
  among Spring's methods the long, flat `addOwner` (25 bound placements, 33 positions, complexity
  5.5) received 35 later arrivals per 100 checkpoints, and small branching helpers almost none.
  Under the one-sided form that interval lies below 1.25. The junction (upper limit 1.67) reaches
  above it, so on this chain H3 would be unresolved, not supported.
- **The sinew measures taken out of H3** (17 November 2026, decided by the author **after** the
  one-sided H3 was run on the development chain). There the junction, 0.71 [0.30, 1.67], was the
  one measure that left H3 unresolved; without it the remaining measures, complexity and the class
  Gini, both lie below 1.25 (long does not vary enough in OfficeFloor, not slimmable in neither).
  The junction's estimate on this chain is below 1, against the direction now stated for it.
- **The literature's measures, each alone, on the development chain** (17 November 2026; one chain
  per arm, descriptive only, `results/analysis/pilot/REPORT.md`). With the junction out, H3's block
  read not above: complexity 0.39 [0.24, 0.65], the class Gini 0.69 [0.42, 1.13]; the junction as a
  sinew measure 1.73 [0.54, 5.51] at the method and 0.61 [0.41, 0.91] at the class. Each new
  measure alone (90% intervals):
  - *At the method* (77 existing hosts): cyclomatic 0.35 [0.22, 0.56], NPath 0.54 [0.35, 0.84],
    nesting 0.36 [0.25, 0.51], all below; fan-out 4.98 [2.24, 11.1], above; Halstead volume 0.87
    [0.18, 4.12], reaching above; the Maintainability Index 51 [6.3, 414], where a higher index is
    a more maintainable method, so this too says the simpler methods are come back to.
  - *At the class* (108 rows): WMC 2.61 [2.18, 3.11], LCOM* 1.64 [1.31, 2.06], CBO 4.73
    [3.55, 6.30], RFC 5.30 [3.36, 8.35], imports 3.72 [2.83, 4.88], Halstead volume 5.08
    [3.58, 7.21], all above; the Maintainability Index 0.31 [0.23, 0.42], the less maintainable
    class come back to more. DIT gave no standard error.
  - *Not readable:* Law of Demeter, cloned lines, TCC, God Class and Data Class did not vary
    enough in the function arm (the God Class flag: 33 bound rows in Spring, 6 in OfficeFloor).
  - *How far this can be read:* the class-level model does not hold the class's size fixed, and
    most of Spring's rows are in one class, the controller, sharing one value and one outcome, so
    those intervals are far too narrow and every class measure there is largely "the controller".
  The class-level model was revised after these were seen (§9, row 35).
- **The class measures with the class's size held fixed** (18 November 2026; the same chain, the
  model of §5 as revised: 77 rows, one per class and checkpoint, an intercept for the class). WMC
  0.44 [0.16, 1.21] and LCOM* 0.90 [0.68, 1.20], below the margin; the Maintainability Index,
  reversed, 0.10 [0.02, 0.45], below; RFC 0.94 [0.41, 2.19], CBO and fan-out 1.62 [0.69, 3.83],
  imports 2.41 [1.13, 5.12] and Halstead volume 0.14 [0.01, 1.52], reaching above; none wholly
  above. DIT gave no finite interval. The method's index, reversed, 0.02 [0.002, 0.16]. So on this
  chain the class measures' ratios of the first table were the class's size and the repeated rows.
  Nothing in the plan was changed after these were seen.
- **H3 with its measures as set on 18 November 2026, on the development chain** (one chain per
  arm, descriptive only). Each alone: cognitive complexity 0.32 [0.21, 0.50] and cyclomatic 0.35
  [0.22, 0.56] at the method; at the class WMC 0.44 [0.16, 1.21], LCOM* 0.90 [0.68, 1.20] and the
  Gini 1.08 [0.83, 1.42]. Long does not vary enough in OfficeFloor. The Gini's interval reaches
  above 1.25, so on this chain H3 is unresolved. Reach: the method's fan-out 4.98 [2.24, 11.1],
  the class's CBO 1.62 [0.69, 3.83]. Nothing in the plan was changed after these were seen.
- **The class level on the development chain** (18 November 2026; decided by the author **after**
  H3 was unresolved there on the class's Gini). Of the 77 class and checkpoint rows, 37 are
  Spring's controller, which holds 638 of the 730 later arrivals (87%); arrivals fall in 5 distinct
  classes. The controller's Gini rises from 0.20 to 0.45 as `addOwner` grows, and within it the
  rate of later arrivals falls as the Gini rises (rank correlation −0.51), which is the stream
  running out; in the mapper and the exception advice it goes the other way (0.53, 0.92). So the
  Gini's 1.08 [0.83, 1.42] is a blend over four classes and says little. Under the rule of §5 the
  class measures are not tested on this chain, and H3 there is read on the method measures: not
  above (cognitive 0.32, cyclomatic 0.35).
- **What unbound code leaves behind, on the development chain** (17 November 2026; a scratch look
  per checkpoint, not built). Fields added to classes that existed, per checkpoint: 0.71 in Spring
  and 0.63 in OfficeFloor where the checkpoint has an unbound landing in an existing class,
  against 0.35 and 0.06 where it has none; rank correlation of the fields added with the unbound
  landings in existing classes 0.41 and 0.63, with the bound landings 0.12 and −0.08. Which class
  received the fields was not looked at.
- **The history steps on the development repositories** (18 November 2026;
  `results/analysis/open-source-development/REPORT.md`; descriptive only, and read to see that the
  steps run, not for what they show). Three repositories, none in corpus B or C: two of people's
  code as of 29 June 2021 (`felHR85/UsbSerial`, `jmxtrans/jmxtrans`; 84 and 86 units) and one with
  declared agent commits (`bytechefhq/bytechef`: 1,608 of its 23,215 commits, nearly all Claude's;
  2,000 units read). This first pass read the first-parent line only, with the cap of 2,000 then
  drafted. Seen on the two repositories of people's code: H1's slopes 0.66 over all runs, 0.87
  within a class, 0.26 within a method (the index runs from 0 to 1); H2 1.02 [1.01, 1.04] at the
  class and 1.42 [1.13, 1.78] at the method; cognitive complexity 1.36 [1.09, 1.70] and the
  class's Gini 1.26 [1.08, 1.47], both reaching above the margin, where on the paired development
  chain complexity lay below it; unbound code entering a class that existed 57% in both arms.
  Finding the one agent repository took 39 draws of the mid tier. The comparison of the arms here
  is of different repositories of very different length, and is not read. **Decided after this
  was seen:** every non-merge commit is a unit (the first-parent line was mostly merges), and, by
  the author, no cap.
- **The development repositories again, with every non-merge commit a unit** (18 November 2026;
  the report regenerated; descriptive only). The two of people's code gave 227 and 422 units
  (84 and 86 on the first-parent line). The agent repository has 7,794 units; read whole it was
  on course for half a day, nearly all of it RefactoringMiner at about five seconds a commit, so
  it was stopped and a development sample was allowed a cap: its newest 300 units, read in 27
  minutes. Seen on the two repositories of people's code: H1's slopes 0.51, 0.99 within a class
  and 0.39 within a method; H2 1.06 [1.05, 1.07] at the class, and at the method no standard
  error this time; cognitive complexity 1.10 [0.98, 1.23] and the class's Gini 1.09 [1.03, 1.15],
  both now below the margin, where the first-parent pass had them reaching above it. So on three
  repositories these readings move with which commits are read, and nothing is to be taken from
  them but that the steps run. The reading eight at a time, and the pass alone after a failure,
  were tried on the same repositories (the workers starved of memory: both failed, both were then
  read alone, with the same units).
- **Nothing standing by at the method, on the development chain** (19 November 2026; looked at
  in the prepared table and in a scratch refit, **before introduced was decided**). Of Spring's 89
  bound rows, 45 have nothing standing by at the method and so no later intrusion bound to it: 29
  are new methods, bound to the class (15 by a field only, mostly the injected `clinicService`; 9
  by a call to another of its methods only; 4 by both, of the 28 in the pilot's host table), and
  16 are small existing methods (3 to 11 positions) whose added code used all there was. The 13
  rows with any such intrusion (43 in all) appear to be one method, `addOwner`. A plain negative
  binomial refit of H2 at the method, without random intercepts and so not the model of §5, gave
  0.94 [0.70, 1.26] on all 83 rows, the same on the 55 existing methods, and 0.95 [0.72, 1.25] on
  the 40 rows where something stood by. The new methods had 4 later bound arrivals between them,
  the existing ones 288.
- **Introduced, on the development chain** (19 November 2026, as built,
  `results/analysis/pilot/REPORT.md`; one chain per arm, descriptive only). Method values
  introduced per addition: 5.1 in Spring, 6.5 in OfficeFloor. Per bound row in Spring, 1.8 method
  values and 0.35 fields introduced; in OfficeFloor 1.3 and 0.10. **Later code is hardly ever
  bound to them:** in Spring 2 of 292 later intrusions at the method and 3 of 1,056 at the class
  use an introduced value (43 and 449 use one that stood by); in OfficeFloor none of 3 and none of
  26. Spring's 29 new methods introduced 102 values, and one later intrusion used one. H2 read on
  what stood by and what was introduced together: 1.09 [1.03, 1.15] at the class, beside 1.10
  [1.04, 1.16] on what stood by alone; 0.92 [0.73, 1.15] at the method, where H2 itself still
  gives no standard error. So on this chain what a change introduces is not what later code comes
  for, and counting it does not change the class reading or lift the method reading above 1.
  Nothing in the plan was changed after these were seen.
- **How bound uses are spread over values, on the development chain** (19 November 2026; a
  scratch count from the measured tables, **before H2 was restated**, since built as
  `readings.core_summary` with the same figures). In Spring, at the class: 37 bound uses of 11
  fields, 78% of them to three fields and 86% to fields that were there before the first
  checkpoint (`clinicService` alone 22); of 35 fields the changes introduced, 5 were used by later
  bound code. At the method: 86 uses of 44 values, 36% to three (`owner` in `addOwner` 18), 48% to
  values from before the first checkpoint; of 315 introduced, 27 used later. In OfficeFloor: 2
  uses at the class; at the method 57 uses of 45 values, none used more than twice, 11% to the
  three most used; of 361 introduced, 31 used later. The petclinic chain starts from a converted
  application, so its early values predate the stream.
- **H2 as restated, on the development chain** (19 November 2026, as built,
  `results/analysis/pilot/REPORT.md`; one chain per arm, descriptive only; **its direction had
  been seen in the count above before it was written**). In Spring, of 83 bound rows, 31 have a
  core at the class and 51 at the method; 82 and 79 have a periphery. Uses per 100 values and
  later checkpoints: at the class 20.6 of the core against 3.7 of the periphery (190 uses of 34
  core values, 528 of 631 periphery values); at the method 10.1 against 0.5 (185 of 75, 45 of
  335). H2's rate ratio of core to periphery: 8.2 [5.7, 11.9] at the class and 20.3 [11.8, 34.7]
  at the method, both models with the checkpoint intercept; the method level is estimable, which
  it was not under the form of 17 November. In OfficeFloor the values code was bound to are
  hardly come back to: at the method 0.40 per 100 for the core and 0.08 for the periphery (4 uses
  of 45 core values), ratio 4.3 [0.5, 38]; at the class one row has a core and the ratio is not
  estimable. So on this chain the arms differ less in whether a core value is used more than a
  periphery one than in how much any value is come back to at all: Spring's core values about 25
  times as much as OfficeFloor's at the method. H2 as it stood: 1.10 [1.04, 1.16] at the class,
  no standard error at the method, as before. Nothing in the plan was changed after these were
  seen.
- **The development chain after the renaming** (19 November 2026, `./step4_analyse.sh --analysis
  pilot` and `./step5_report.sh`; one chain per arm, descriptive only). The core reuse reading
  beside H4: how much a core value is come back to, function arm against methods arm, at the
  method 0.088 [0.024, 0.316]; at the class not estimable (OfficeFloor's one core field was not
  used again: 0 uses in 1 row, against Spring's 190 uses of 34 values in 31 rows). Per 100 values
  and later checkpoints, OfficeFloor core 0.40 and periphery 0.08 at the method, periphery 1.9 at
  the class; Spring as above. The other figures are unchanged from the runs above: H1 0.015
  overall, 0.026 within a class, 0.023 within a method, 0.003 [-0.005, 0.012] without constants
  (the bootstrap over one chain per arm gives no width to the bystander intervals of H1 and H4);
  H2 8.2 and 20.3; H3 at the method cognitive 0.32 [0.21, 0.50] and cyclomatic 0.35 [0.22, 0.56],
  long left out by the variation rule, the class level not tested (5 classes, the busiest 0.87);
  H4 arm -1.59, slope -0.017, intrusion ratio 0.16 [0.10, 0.27] at the class and 0.11 [0.03,
  0.43] at the method, amount 1.076 in the band, largest wiring file 0.16. Size or data still
  against its direction (0.88 per value that stood by at the class, size 3.05). Nothing in the
  plan was changed after these were seen.
- **H5 and the H2 of 19 November 2026 (evening), on the development chain** (as built; measured
  again at `MEASURE_VERSION` 18; one chain per arm, descriptive only). H2 with the class's called
  methods as core values and each later method scored on its own: 17.5 [11.9, 25.6] at the class
  (8.5 [5.8, 12.5] on the fields only), 20.3 at the method as before. The core's width at the class
  in Spring 1.1, 1.25 and 2 values a row over the thirds of the stream (OfficeFloor about 1). **H5
  at the class went the predicted way:** the alternatives' ratio end to start 0.16 [0.03, 0.92];
  in Spring 54% of class rows forced (bound to the class's own state, constants or methods), the
  mean alternatives 3.5, 3.2, 1.3 over the thirds; OfficeFloor 90% forced at the class. **H5 at the
  method went against it:** 2.5 [0.9, 7.1], about 20 alternatives a row in Spring and 40 in
  OfficeFloor, rising with the code base. A scratch split (by the bound values' names) shows the
  rise in rows bound to domain types (`Owner`, its DTOs: 10, 15, 23 over the thirds in Spring) as
  well as in those bound to `String`s: types do not separate the places at the method. Every new
  method that handles an owner counts as an alternative, whether or not the request's control
  flow reaches it. This is the case §4.2a foresaw (a refinement by control flow); not yet decided.
- **H5 on the control flow, on the development chain and the development histories** (19 November
  2026, `MEASURE_VERSION` 19; descriptive only). *Pilot:* at the class unchanged, 0.16 [0.03,
  0.92]. At the method, on the flow, about 6 alternatives a row instead of 20 by type, and still
  rising: 4.6 [1.5, 14.6] (Spring 3.5, 4.8, 9.4 over the thirds; forced 54%, 30%, 22%). The flow
  itself grows (Spring about 64 methods a host's flow early, 114 late): the stream keeps adding
  rules to `POST /owners`, each as a helper method that takes the `Owner`, and each such helper is
  another place on the same request where later code could go. So at the method choice widens as
  helpers gather on one flow, while at the class it narrows. Calls into the application followed
  by their receiver's type: 85%. *Histories* (the two repositories of people's code; the agent
  repository failed on a fault since fixed, a `catch` of a union type, and is being read again):
  every class row forced (both are plain Java without injection, so every field is the class's own;
  the class level of H5 says nothing where there is no injection); at the method 1.56 [1.01, 2.42],
  by type alone 4.9; calls followed 62%. *The agent repository* (`bytechef`, read again after the
  fix; its 300 newest units): a Spring application, so the class level has alternatives (2.4 a
  class row; 64% bound to the class's own values); at the method 26 alternatives a row on flows of
  about 665 methods, with only 50% of calls followed: in a large application of interfaces and
  shared services, a flow taken from the entry points above the host takes in most of the code.
  Nothing in the plan was changed after these were seen.
- **H6 on the development chain and the development histories** (20 November 2026,
  `MEASURE_VERSION` 20, `HISTORY_VERSION` 4; descriptive only; H1 to H5 unchanged). *Pilot:* rise
  0.45 [0.15, 1.37], the spread not rising (Spring's units in more than one class 55%, 40%, 37%
  over the thirds); forced 2.77 [1.44, 5.31] (a forced unit 2.1 classes, the others 1.4). The
  coupling of pairs changed together more than once rose, 5.3 [2.0, 14.0] (4 pairs); Spring's
  candidates `Owner` with `OwnerRestControllerV1` (changed together 9 times, calls 3 → 8) and
  `OwnerMapper` with it (7 times, 0 → 5). The author's reading and the drafter's (20 November
  2026): Spring's spread does not rise because the change piles into the core class (H1, H2;
  petclinic puts every rule on one endpoint); where it cannot be absorbed it spreads, forced, and
  the pair's coupling rises. OfficeFloor makes each function a class, so about one class a unit is
  new; counting existing classes only, Spring 1.55, 1.50, 1.42 over the thirds and OfficeFloor
  0.82, 1.15, 2.28 (not yet decided whether H6 counts existing classes only). *Histories* (the
  two human repositories, 489 units): rise 1.57 [0.81, 3.07]; forced 2.22 [1.52, 3.26] (2.3
  classes against 1.6); 63% of units forced, but without injection a class row bound at all is
  forced (H5, above), so there *forced* is *bound at the class*; coupling of pairs changed
  together more than once 1.65 [1.05, 2.60] (587 pairs; of those compared, coupling rose in 30 and
  fell in 16), the candidates mostly `UsbSerial`'s device classes with their base class. The agent
  repository has 9 declared agent units, too few to read. Nothing in the plan was changed after
  these were seen.
- **H6 within change size** (20 November 2026, the hosts of MEASURE_VERSION 22 and the histories as
  then read; descriptive only): a forced unit is a larger change (Spring 13.2 positions and 3.9
  methods against 7.7 and 2.4; OfficeFloor 19.0 and 5.2 against 9.7 and 3.2; jmxtrans 10.3 and 4.6
  against 8.1 and 2.3; UsbSerial 13.3 and 3.4 against 12.7 and 3.8). Existing classes a unit, units
  split at the median number of methods: Spring 1.0 against 1.1 (small) and 2.1 against 2.0
  (large); jmxtrans 1.2 against 1.0 and 4.1 against 1.9; UsbSerial 1.1 against 0.9 and 2.4 against
  1.6. The pilot's forced effect on spread is change size; the histories' remains for large
  changes. Led to row 61.
- **Not seen.** Pull, placement, containment or intrusion on any other chain, run or repository.
  The petclinic runs have been read for other measures (the conservation paper), never for these.
  None of the ui runs' backend Java has been read for any measure.
- **The absorbed drafts** (§1.1): their hypotheses were laid side by side on 16 November 2026.
  All three predicted the OfficeFloor arm better and none contradicted another; the review found
  that they read OfficeFloor's parameters differently, which is why the reading without the
  injection rule (§5) is added. None of their measures was computed on any run.
- **Expectation.** The author expects H1, H2 and H4 to hold; of H2's two levels the method is the
  harder to show, because few later arrivals at a method are bound to what stood by. The author also expects H3 to hold:
  that shape outside the problem draws nothing in by itself, and that where it seems to, it is a
  bias in where unbound code is put (§5, *Where bound and unbound code lands*), not a cause. H3 is
  the hypothesis this expectation could most bias, which is why its criterion is a margin fixed
  here; and it was made one-sided after the development chain went against the two-sided form
  (below). The
  author expects OfficeFloor's junctions to stay contained to their injection point (the junction ×
  arm reading of §5); that reading's direction is stated here, before any intrusion is computed by
  junction.
- **Conflict of interest.** The author created OfficeFloor, SinewSlim, OfficeFloorSlim and both
  harnesses. Mitigations, as in the earlier studies: the arms run on the same fixed stream and
  agent; the instrument's rules are fixed here; every case where the function arm does worse is
  reported; corpus B is drawn by an independent sampler.

## 7. Threats

- **H5's alternatives are found by type, on a control flow read without a symbol solver** (§4.2a).
  At the method a common type (`String`, `int`) still matches more readily than a domain type,
  though only on the host's own flow. The flow can miss a method reached by a call whose receiver
  the source does not type (a chained call), or by the framework (reflection, events, callbacks),
  which biases the count down; it can include a method by an interface's every implementation,
  which biases it up. The share of calls followed is reported. A constant or state of the class
  makes the class forced by definition. None of these should change with the checkpoint by itself,
  and H5 is about the trend; the alternatives are kept by name for the check. On a history the
  index of the tree is exact at each unit's parent, but a repository's tests and generated code are
  left out as production Java is.

- **H6's spread counts classes, not reasons** (§4.2b). A feature that touches a controller, a
  service and a repository spreads by design (layering), not from lack of cohesion; H6's *forced*
  part is what ties the spread to lack of choice, at the same point in the stream, and the
  function arm is the contrast. On a history a commit can bundle unrelated work (a tangled
  commit), which widens the spread whatever the placement; this does not change with the unit's
  place by itself, and the 200-line cap on a unit (§3.2) bounds it. The pair's coupling counts the
  calls the instrument follows (§4.2a): not reads of another class's fields, nor calls whose
  receiver is untyped; it is the trend of a pair that is read, not its level. On a history the tree
  after a unit is the tree before the next, so the coupling a unit added there includes any
  commits between them that are not units (merges, large commits); on corpus A the two trees are
  the unit's own. The coupling accounting is per unit and does not say which of a unit's changes
  added a call.
- **The redesign reading** (§4.2d) has thresholds (two groups of two forced changes, three times
  together, half the same data) that are the drafter's. A class's values are the fields and class
  methods its changes used, so two groups that share only a value the instrument does not see (an
  inherited field) are counted as apart.
- **Coupling scales with size** (Lopes and Ossher 2015, read in full: structure measures of Java
  programs follow size by power laws, so a size-normalised reading needs the exponent, not a
  ratio). H6 and H7 hold the change's size fixed for this reason (§9 row 61); a reading of a
  class's boundary against its size, if built, must be read against the exponent the size alone
  predicts, and against the function arm.
- **High coupling in a few classes may be unavoidable** (Taube-Schock, Walker and Witten 2011:
  between-module connectivity is roughly scale-free, so some highly coupled modules are expected
  of the distribution, not of poor design). This is the rival reading of H7 and of the
  concentrate signal: a forced class that gains coupling may be in that tail whatever forced it.
  The forced/unforced contrast at the same size and the arm contrast are what separate the two.
- **H7 reads coupling as calls and openness as method access** (§4.2c). A field made public and
  read directly from another class, or a call the instrument cannot follow (an untyped receiver,
  reflection, framework callbacks), is not seen; nor is coupling through shared types without
  calls. A renamed or moved method makes its calls look new on both sides. Neither should differ
  between forced and unforced classes by itself. A forced class is often the larger class (the
  core of H2), and a larger class may gain more calls whatever forced it; the index is in the
  model, and the class's size is not (the reading is about the force, and size is its result).

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
- **Shared counts at the class and the method.** H2 and H3 are read where the code was placed.
  Every problem placed in one class shares that class's later changes, so the rows of one class are
  not independent, and a busy class weighs on the estimate as many times as it holds problems. The
  one-endpoint petclinic stream makes this strongest there. The own-lines reading, which does not
  share counts, is reported for comparison; following lines is the weaker provenance, and the share
  of lines lost track of is reported per arm.
- **The function arm's calling method is its wiring.** Intrusion at the class and the method is
  read on Java. Where the methods arm goes back into a handler, the function arm goes back into a
  flow configuration file, and that is not in H4's intrusion. The wiring conditions of §4.5 and the
  reopening of wiring files (§4.4, reported) are where it shows.
- **Preferential attachment is the rival reading of H2.** Busy places getting busier is a known
  pattern of software growth, fitted to dependency degree with no mechanism (Chaikalis and
  Chatzigeorgiou 2015; Lin and Whitehead 2015). H2 claims a mechanism: later code comes for the
  data that gathered. A rise in H2's count could instead be a busy place receiving more of
  everything. Two things bear on it: H2's outcome counts only the arrivals bound to what stood
  by, with the place's size held fixed; and the size-or-data reading (§5) asks which of the two
  later arrivals follow. On the development chain that reading went to size (§6), so on that
  chain attachment to size is not ruled out.
- **The core is partly the problem's.** Problems of one stream need much of the same data (every
  petclinic rule is about the owner), so a value many problems are bound to may be core because
  of the problems, not the place. Three things bear on it: declared and crossing checkpoints are
  left out of H2's uses; the function arm solves the same problems and is read beside it; and the
  ui stream has many endpoints. It is still not ruled out within one arm.
- **H2 as restated compares two kinds of value, and they differ in more than kind.** A core value
  was by definition useful to one problem already. That later problems use it more than a value
  nobody had used is likely, and H2 says how much more, not that it could have been otherwise.
- **Two records of one row are not independent.** The core's and the periphery's records share
  the row's later arrivals, and the model has no term for the row. With the shared counts within
  a class (below) this makes H2's interval too narrow.
- **H2 as it stood (reported) is opportunity by construction.** Where nothing stood by, nothing
  can be drawn by what stood by, so part of that rate ratio is given. It tests that accumulated
  data is taken up in proportion to its amount; it does not show that the later code could not have gone elsewhere
  (that is the choice and review readings), nor that it preferred this data to other data.
- **At the method, half the rows of H2 as it stood could only read nought.** A new method has
  nothing standing by, and neither has a small method whose added code uses all there is; with
  nothing standing by, nothing can be drawn by it. On the development chain that is 45 of
  Spring's 89 bound rows (§6). H2 as restated on 19 November 2026 does not have this: a kind with
  no values gives no record (§4.4), so a new method is read on its periphery, and a row bound
  only to its class has no core at the method.
- **H1 within a method starts from nought.** A method has no bystanders at the checkpoint that
  creates it, and later code placed in it sees the values it was created with. Part of the slope
  within a method is therefore given by a method being new once. That is a place gathering data,
  which is the claim, but it is not evidence beyond the definition.
- **H1 and H2 overlap.** A place where data gathers (H1) and a place whose core is used by what
  comes next (H2) are read on the same busy class. They are not independent tests, and Holm
  treats them as if they could be.
- **H1 and H2 no longer make one loop.** Until 19 November 2026 they did: a place gathers data,
  and the gathered data binds the next code. As restated, H2 says the next code comes for a few
  core values and not for what gathered. H1's rise is then mostly periphery: what code has to sit
  beside, a cost of the place, and not what draws code to it. H1 was renamed to say so (§2); its
  test was left as it is, so H1 by itself no longer shows a pull, only a cost that grows.
- **H1's periphery is not H2's.** H1 counts bystanders, the pre-existing values a run does not
  use. H2's periphery adds what the change introduced. H1 was not changed to count introduced
  values: they are not there when the code arrives, so the code does not sit beside them.
- **H2 was shaped on the development chain** (§6), as H1 and H4 were: its restatement followed a
  first look at the measure there, and its direction was seen on that chain before it was written.
  That is so of both restatements. The second, to core and periphery, was made after the first
  had come out below 1 at the method on that chain and after the spread of uses over values had
  been seen there; it turns what was the first form's failure case into the claim.
- **Values are matched by name.** A renamed field is lost between a placement and a later use, and
  a new local with an old name is counted as the old value. The first lowers H2's count, the second
  raises it at the method.
- **An agent's commit is known only where it is declared** (corpus C). Assisted code that carries
  no mark sits among the commits it is compared with, which pulls any difference towards zero.
  Repositories with declared agent commits are also younger and smaller than those of corpus B, so
  the comparison between corpora is across projects and years as well as authors.
- **Open-source commits are not problems** (corpora B and C). Without a stream, a later arrival
  may belong to the same problem as the code it comes back to, which H2 would count as drawn in.
  The issue-linked unit of corpus B is the stricter reading.
- **Bindings decide what is followed.** Intrusion is read only on bound code, and a wired function's
  parameters are not bindings (§4.3). So fewer of the function arm's placements are followed at all;
  the number followed and set aside is reported per analysis.
- **Pull is not proof of force.** A binding shows that the code used something that was already there.
  It does not show that no other placement existed (§4.3). The choice-at-a-checkpoint and review
  readings are the checks, and both are indirect.
- **H1 and H4 were shaped on the development chain.** The bystander measure and the direction of
  both hypotheses were settled after seeing it on chain 9 (§6). That chain is excluded, and the
  registered chains had not been read, but the hypotheses are no longer blind to this run's
  general shape: the other chains of the same run are likely to resemble it. The replication on
  the ui stream, a different application, is the stronger test.
- **Growth is not gravity by itself.** A codebase that grows has more of everything. H1's slope
  is read against the function arm, which grows by about the same amount on the same stream
  (§4.6): bystanders that rise in one arm and not in the other are the form's, not the growth's.
  H1 alone, without H4, would not show that.
- **Visible is not used, and not harmful by itself.** A bystander is exposure: something the code
  could read or disturb. H2 asks whether what stands by is later used, not whether that does harm; the
  harness's own signal of a rule broken that was not meant to change is the outcome that would
  answer the question of harm most directly (not read by this plan).
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
  so H3 is not read there.
- **Power for H3.** A test against a margin needs more data than a difference test. If an
  interval is too wide to fall below the upper margin, H3 is reported as unresolved, not as
  supported.
- **H3's measures were chosen on the development chain.** Of the literature's measures, those
  taken into H3 are ones that lay below the margin there, or reached above it only at the class
  (§6); the one measure wholly above it, the method's fan-out, was put with the sinew measures,
  with CBO, as reach. The reasons given do not rest on the results (the first are the literature's
  usual shape measures; the second count what a place reaches out to), but the order is as stated.
  The measures left out of H3 are all reported, so a reader can read H3 with any of them put back.
- **The junction left H3 after it had left H3 unresolved on the development chain** (§6). The
  reason given is that it is not a shape measure of the literature, and that reason does not rest
  on the result; but the order is as stated, and on that chain H3 reads better without it.
- **H3 was made one-sided after the development chain failed the two-sided form.** There, more
  complex methods were followed by less intrusion (§6), which "adds nothing" does not allow and
  "does not draw in" does. The one-sided claim is the weaker one. The two-sided reading and every
  effect's size are reported, so a shape that goes with less intrusion is not hidden.

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
   Committed, and the tag set on them (`f780a5a`). The bystanders (§4.3a) and H1 and H4 as restated
   on 17 November 2026 were then built and run on the development chain, committed, and the tag
   `plan-v1` set on them (`69af01c`). **The tag was withdrawn on 17 November 2026** with the fourth
   and fifth revisions (§9), which are committed without it. To do: set `plan-v1` again when the
   work on the development chain is done, before any run named for analysis is read.
6. `./step1_setup.sh`, then for corpus A (petclinic, then the ui runs as they finish):
   `./step2_runs.sh`, `./step3_measure.sh`, `./step4_analyse.sh`, `./step5_report.sh`. Analyse
   once; the heads read are recorded in `results/heads.tsv`. Then corpus B and corpus C (§3.2, §3.3; their
   steps are not yet built).
7. Write up, reporting every hypothesis whichever way it falls.

**Before the tag `plan-v1` is set** (the list as it stood on 18 November 2026; the tag is the
author's to set, on the plan and code as they then stand, and starts the experiment):

- ~~*To finish:* the development run of the history steps (§3.2) on the three development
  repositories, with every non-merge commit as a unit, looked at and recorded in §6.~~ Done 18
  November 2026 (§6, *The development repositories again*).
- ~~*To finish, left on 19 November 2026:* the development chain's models and report run again
  after H1 and H4 were renamed and the core reuse reading was added.~~ Done 19 November 2026; the
  core reuse figures are in §6. (An instrument change needs `MEASURE_VERSION`
  (`placement_gravity/measure.py`) raised, or step 3 keeps the earlier measurements.)
- ~~*Not chased:* the pilot's host table gives 28 bound new methods in Spring where the prepared
  table gives 29 (§6).~~ Chased 19 November 2026: 29 is right. At checkpoint 28 the agent renamed
  `DuplicateEmailException` to `DuplicateIdentityException` (keeping its field `fields`, changing
  the constructor's parameter) and deleted `DuplicateHouseholdException`. The instrument as built
  follows the rename by RefactoringMiner's type hint, so the constructor's use of `fields` is a
  binding to a field that existed. `results/pilot/hosts.csv` is the earlier instrument's table,
  which took the class for a new one. No change to the code.
- *Values confirmed by the author on 18 November 2026:* the class-level rule of H3 (10 distinct
  classes, §5: petclinic gathers on one endpoint and is not expected to pass it; the ui stream and
  the open-source samples are where the class level is read); corpus C's bound of 30 declared
  agent commits (§3.3); the margin of 1.25 and the six measures of H3 (§2); and no cap on a
  repository's units (§3.2).
- *Also confirmed by the author on 18 November 2026:* corpus B's size (300) and corpus C's (100,
  of up to 6,000 drawn), both being reported and not confirmatory.
- *Also confirmed:* the as-of date of corpus B, 1 December 2020, as `long-method-slim-study`'s
  and for its reason (§3.2).
- *Confirmed by the author on 19 November 2026:* that no class holds more than half of the
  arrivals (the second half of the class-level rule of H3).
- *Decided by the author on 19 November 2026 (evening), and built:* corpus B is two sets of 300,
  `long-method-slim-study`'s sample (seed `20261101`) and a confirming set (seed `20261118`)
  without its repositories (§3.2; `runs.yaml` `open-source-human` and
  `open-source-human-confirm`, `history.chosen`, `history.sample_excluded`, two tests). Corpus C
  stays as it is: its own seed (`20261119`), target 100, read only if at least 10 are usable; no
  second set.
- *Decided by the author on 19 November 2026 (evening), drafted and built the same day* (§2, §4.2a,
  §4.4, §5, §7, §9 rows 49 to 53):
  - H2 is about binding only; the core is what a row's own code used; a value counts once; at the
    class each method of a later change is scored on its own; a call to a class's method is a core
    value (and its uncalled and added methods periphery: the drafter's choice; the author confirmed
    on 19 November 2026 "H2 yes count methods").
  - H1 counts constants, with the author's reason.
  - **H5, choice narrows**, one-sided as H3 (the author agreed the margin, 1.25, on the
    drafter's proposal): alternatives at the class by injected dependency type, at the method by
    the types of the bound values, recorded by name; corpus A only.
  - *Decided by the author later that day:* H5 at the method counts only the places on the host's
    control flow (§4.2a), and H5 is read on corpora B and C too (§3.2).
  - *Chosen while drafting and not yet spoken to:* a level where every placement was forced passes
    H5 with p 0; H5 needs both levels; the model has the chain's intercept and no checkpoint
    intercept (the index is the term); a value of no declared type is left out of the match.
- *Open, the author's question on H2's fit* ("is the fitting trying to average the methods to find
  consistency between them? I would be looking at counts only, particularly for the core, as we
  are looking at sinew width"). The drafter's answer: the model is a count model. It pools the uses
  of every row's core and of every row's periphery, each against its number of values and later
  checkpoints, with the problem terms; it does not compare methods with each other and has no term
  per row. H2 stays a rate per value until the author decides otherwise; the core's width is now
  reported per row, per arm and over the stream (§4.4).
- *Decided by the author on 20 November 2026, after seeing H5 on the development chain* (§2, §6):
  H5 read as the area of methods growing inside classes the binding forces it into, and a new
  **H6, forced changes spread**: do changes come to need several classes at once for lack of
  choice, and does the coupling of classes that keep changing together rise (the case for
  redistributing placement, and the encapsulation of fields, between them). The drafter's
  operational form (§4.2b, §5: spread as classes beyond the first; forced as H5's class level;
  rise and forced each one-sided above 1; coupling as the calls followed between the pair) is not
  yet spoken to by the author.
- *Decided by the author on 20 November 2026, after H6 on the development chain and histories*
  (§6): H6 counts only classes that existed ("new classes are freedom of choice"); H6 focuses on
  forced, with forced and unforced units tracked apart ("possibly track forced and unforced
  separately to compare, but focus on forced"), so H6's test is the forced ratio and the rise is
  reported in each; and the growth and coupling accountings are built.
- *Decided by the author on 20 November 2026:* **H7, forced changes couple** ("make it H7 and
  build it"): encapsulation as the force, concentration and dispersion its two outlets, coupling
  through existing exposure or widening the cost of dispersion. The operational form (calls added
  across the class's boundary, forced ratio one-sided above 1; exposed and widened by method
  access) is the drafter's, not yet spoken to.
- *Decided by the author on 20 November 2026:* the **split or concentrate** reading ("draft it as
  a reading with the refactoring check"); the check against developers' refactorings withdrawn
  the same day ("I'm not interested in what developers did ... I'm interested in how the force of
  encapsulation forcing concentration verses dispersion forcing coupling"). Its thresholds are the
  drafter's, not yet spoken to.
- *Decided by the author on 20 November 2026, after a check on the development data* (§6): H6 and
  H7 hold the change's size fixed ("yes add change size to H6 and H7"). The author's question was
  whether the effects are true by construction or reflect the forces within the construct. The
  drafter's answer, recorded: three kinds. *By definition* (a measuring artefact, now removed): a
  forced unit is a larger change, so it touches more classes and adds more calls. *By the
  construct* (the finding, not evidence for it): without injection all class-bound code is forced,
  and forced code lands in existing classes by definition. *The forces within the construct*
  (what the study can show): forced against unforced at the same size and point in the stream,
  and the arm contrast, where the function arm holds no state privately.
- *Decided by the author on 20 November 2026 (boarding):* H5 tested at the class only (row 64);
  ripple read against chance (row 64); public fields to be tracked as well as methods (exposure
  and widening of fields, reads of another class's fields as coupling; not yet built). The
  author's account of the function arm, for reading H4 and the arm contrasts: "OfficeFloor by
  nature removes a lot of the domain model encapsulation of methods dispersed over encapsulated
  units. It is transaction scripts of cohesive blocks of code that are loosely coupled together."
  So few forced placements in the function arm is the expected result of the construct, and the
  arm contrast reads the share forced as well as the effects at a forced placement. Open: what
  *forced* should mean where there is no injection (§2, corpus B), and whether the hypotheses
  stay one experiment.
- *Decided by the author on 21 November 2026 (back from the flight):* forced means forced by
  encapsulation (row 65); public fields tracked (row 65); the hypotheses separated into a
  confirmatory family and secondary ones (row 66). The drafter's choices in these, not yet spoken
  to: package-private and protected members count as reachable; (a constant follows its access,
  decided by the author the same day); the confirmatory family is H2, H4, H5, H6 and H7.
- *The tag stays unset* (the author, 19 November 2026: "still to hold off, as I want to think about
  H2 in terms of placement choice"; H5 now carries choice).
- *Not built, and said so where it matters:* the issue-linked unit of corpus B (§3.2); the ranks
  of the landing reading on a history; a reading of what unbound code leaves behind per class
  (the fields it adds to the class it enters, and whether later code is bound to them), which
  would join H1 and H2 to the landing reading and was looked at only per checkpoint (§6).
- *Raised on 19 November 2026 and overtaken:* whether H2 at the method is read only on rows
  where something stood by, and whether a row is followed at the method only when its code is
  bound to the method's own values. H2 as restated that day gives no record for a kind with no
  values (§4.4), which does both.
- *Chosen while drafting H2's restatement and not yet spoken to:* that the core of a row is what
  its own code was bound to (and not a list of a place's most used values, which would need a
  threshold); that uses are counted value by value; that the two records of a row are fitted
  without a term for the row; and that a class's other methods, which bind code, are not core values.
- *Decided by the author on 19 November 2026, on the drafter's suggestion:* the four tests stand
  as they are; H1 is renamed *the periphery grows* and H4 *function injection forms no core*; how
  much a core value is come back to is reported per arm beside H4 and is not a condition of it;
  H2 takes no threshold above 1.
- *Considered and left as a reading:* that shape is a bias on where unbound code is put, not a
  cause (§5, *Where bound and unbound code lands*). It is not part of H3.
- *Waiting on data:* Run B's ids and Run C (§3.1a), by dated amendment before their backend Java
  is read. Since the ui runs are the primary test (§3.1), **the study's verdicts wait on Run B**:
  Run A alone cannot tell the arm from the front end.
- *Weak points seen on the development chain* (§6): H2 at the method was not estimable on one
  chain; H1 without constants is nearly flat; the size-or-data reading went against its stated
  direction; long does not vary in OfficeFloor.
- *The sampler* is released (0.4.0) and pinned (`setup.sh`).

## 9. Revisions and amendments

**Before the start.** The experiment starts when the first run named for analysis is read
(`results/heads.tsv` holds a row that is not the development chain). Until then a change is a
**revision of `plan-v1`**: it is dated and listed below with what had been seen when it was made,
and the tag `plan-v1` is set on the revised plan and code before the start.

**The tag withdrawn (17 November 2026).** The author removed `plan-v1`, here and from the
published repository, with the fourth and fifth revisions: the hypotheses are still being worked
out on the development chain, and the tag is to mark the plan the experiment starts from, not a
draft of it. It had last stood on `69af01c`. Nothing but the development chain had been read.
Without the tag, steps 2 to 4 refuse every analysis but the development one. The tag will be set
once, on the plan and code as they stand when that work is done.

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

*Hypothesis numbers, here and throughout the plan, are those of the fourth revision: what was H2a
is H2, what was H2b is H3, and what was H3 is H4. H2's content is that of the fifth revision; where
an entry dated before it says H2, it means the bindings and later intrusion.*

**16 November 2026, first.** Bindings to injected dependencies reported apart (§4.3, §5); the tag moved
from `4bb8973` to `4ec41dd`.

**16 November 2026, second: after a review of the plan.** Nothing but the development chain had
been read; what the review computed on it is in §6. The tag moved from `4ec41dd` to the commit that
holds this revision. The changes:

| | Change | Where | Why |
|---|---|---|---|
| 1 | A random intercept for the checkpoint in the H1, H2 and H4 models | §5 | The problem was held fixed only by its size and declared crossings; its identity is known and replicated over the chains |
| 2 | Intrusion read on the problem's own lines; the host-level count reported beside it | §4.4, §5 | As built it counted any later change to the host method, a property of the host and, in petclinic, of the stream |
| 3 | Whether the host is new, in H2's base model | §5 | New hosts have almost no bindings and a different later life, so that contrast alone could carry H2 |
| 4 | Host size centred in H4's model; the arm difference also reported at 10, 25 and 50 positions | §5 | Uncentred, the arm term was the difference at a host of one position |
| 5 | H4's amount band read on the amount added since the base | §4.6 | The petclinic arms start from conversions of different size; no change for the ui stacks, which start empty |
| 6 | Pull stated as graded: injected parameter, injected dependency, value bound to the control flow; a binding stated as evidence of pull, not proof of force | §4.3, §7 | To say what the measure claims |
| 7 | Three reported readings: choice at a checkpoint, formation, review | §2, §5 | The same problem at every checkpoint lets the choice, and what follows from it, be read directly |
| 8 | Editorial: §3.1a's "[DECIDE] before registration", §8 step 1, `README.md` | | Stale text |
| 9 | The guard refuses uncommitted changes to registered files; reports list the files changed since the tag | `runs.py`, `report.py` | So a change after registration cannot pass unseen |
| 10 | A renamed file's before version is read under its own path | `Pull.java`, `chain.py` | It was read under the new path, so RefactoringMiner's hints and the shape at *k* − 1 could miss it |
| 11 | A tree with no production Java (a ui stack's empty base) is read as empty | `chain.extract` | Reading it failed |

In that revision the hypotheses H1 to H4, their directions, their thresholds, the equivalence
margin, the runs read and the Holm correction were unchanged.

**17 November 2026, third: H1 and H4 restated on bystanders.** Nothing but the development chain
had been read; what was seen on it is in §6. This revision changes two hypotheses, and it was made
after seeing the measure on the development chain (§7).

| | Change | Where | Why |
|---|---|---|---|
| 12 | A new measure, bystanders: the pre-existing values visible where a run starts that it does not use, at method and class level | §4.3a | Bindings count the data a problem needs, which the problem sets. What surrounds that data is what the placement sets, and what grows |
| 13 | H1 restated: bystanders rise with the checkpoint index in the methods arm. H1 as first registered (bindings on host size and checkpoint) is reported | §2, §5 | The binding-based slope was at a ceiling in Spring and measured the problem's use of data |
| 14 | H4 restated: the function arm's bystanders are fewer and grow more slowly. H4 as first registered (bindings, slope on host size) is reported | §2, §5 | So that H4 is read on the same measure as H1; and bystanders count injected parameters, so H4 no longer rests on the injection rule |
| 15 | Two reported readings: accretion and capture | §4.3a | The two links of compounding, each read on its own |
| 16 | Constants count as bystanders; the count without them is reported | §4.3a | A constant is not to be duplicated, so code that needs it comes to it. Decided after the development chain showed that Spring's growth is mostly constants (§6) |
| 17 | Bystanders are read only on runs that use at least one pre-existing value; the share of free runs is reported | §4.3a | Code that needs nothing that was there was not pulled anywhere. Decided after the development chain showed new entity accessors diluting both arms (§6) |
| 18 | A plain accessor is organisation, not logic | §4.3 | It exposes a field and holds no logic. This also removes accessor lines from the bindings and from a problem's own lines |

H2, the equivalence margin, the amount band, the wiring conditions, the runs read and the Holm
correction over three hypotheses are unchanged. The tag `plan-v1` moved from `f780a5a` to the
commit that holds this revision, built.

**17 November 2026, fourth: four hypotheses, and intrusion where the code was placed.** Nothing but
the development chain had been read (§6).

| | Change | Where | Why |
|---|---|---|---|
| 19 | H2a and H2b become H2 and H3, each decided on its own; the former H3 becomes H4; Holm over four | §2, §5 | One is a difference to show and the other an equivalence; the second should not decide the first |
| 20 | Intrusion is read at the class and at the method; a problem's own lines are for information | §4.4, §5 | The lines are what is placed, and changing one changes the problem. The class and the method are the placement, and it is the organisation of the code that gathers later changes |
| 21 | H2 needs the bindings' rate ratio above 1 at both the class and the method; H3 is read at the method | §5 | S1 to S4 are measures of the method |
| 22 | H4 gains a condition: the function arm's bound code is come back to less, at the class and at the method | §4.4, §5 | The busy class is the finding. First written as a count of places reopened per checkpoint, which did not tell the arms apart on the development chain (§6) and is now reported |
| 23 | Intrusion applies only where there was a binding: only bound problems are followed, and only later code that is bound there counts | §4.4 | Code that reuses nothing that was there was not drawn to its place. A new field and accessor on an entity binds nothing |
| 24 | A model whose standard errors do not compute is refitted without the checkpoint intercept, and a term that still has none is reported as not estimable | `analyse.R`, `verdict.py` | On the development chain the method-level model returned none |

The directions of all four, the thresholds, the equivalence margin, the amount band, the wiring
conditions and the runs read are unchanged.

**17 November 2026, fifth: H2 restated, and H1 read within a place.** Nothing but the development
chain had been read; what was seen on it, before and after, is in §6. This revision changes H2 and
adds to H1, and was made after seeing the measure on the development chain (§7).

| | Change | Where | Why |
|---|---|---|---|
| 25 | H2 restated: where code was bound to a class or a method, the more data stood by there, the more later code arrives bound to that data. H2 as it stood (bindings and later intrusion) is reported | §2, §4.4, §5 | Decided by the author: it is not the number of bindings that draws later code in, it is the data gathered in the place, which later code is then bound to |
| 26 | H1 also read within a place: the class's bystanders within a class, the method's within a method; all three slopes needed | §2, §5 | The first half of the author's restatement (a place gathers data as changes arrive) is H1 seen inside one place; it rules out a rise that comes only from code moving to fuller places |
| 27 | H3's model holds the method's bystanders fixed beside the bindings | §5 | H2's predictor joins the things shape has to add to |
| 28 | The instrument names the fields a run uses and those standing by; each host row carries what stood by | `Pull.java`, `tables.py` | Needed to tell which later code uses what stood by |

| 29 | A reported reading with a stated direction, size or data: both arms pooled, later intrusion on what stood by with the size of the place held fixed | §2, §5 | The author's claim that size attracts only as a proxy for the data gathered. Not a hypothesis: within the methods arm the two are nearly one variable (§6), and the pooled form leans on the arm contrast |

| 31 | A reported reading: where bound and unbound code lands among the methods and classes it could have gone to, ranked by complexity and by data width; the instrument counts each method's locals | §5, `places.py`, `Pull.java` | The author's question for H3: whether shape influences choice shows in the code that nothing bound to a place. H3 is unchanged until this has been looked at |
| 32 | H3 is one-sided: each shape measure's rate ratio shown below the upper margin, 1.25. The two-sided reading (0.8 to 1.25) is reported | §2, §5, `analyse.R`, `verdict.py` | Decided by the author after the development chain went against the two-sided form in the direction of less intrusion (§6, §7). The claim disputed in the literature is that shape attracts change, which is one-sided |
| 33 | H3's block is the literature's shape measures, S1, S4 and S5. Not slimmable and junction (S2, S3) are sinew measures, read apart with a stated direction (above 1) | §2, §4.7, §5 | Decided by the author: they are the author's own concepts, about data flow, not shape the literature has studied; a junction that attracts would be evidence for data gravity, not against "shape does not draw code in". Made after the junction left H3 unresolved on the development chain (§6, §7) |
| 34 | The literature's shape measures at the method and at the class (cyclomatic, NPath, nesting, fan-out, Halstead, Maintainability Index, Law of Demeter, clones; WMC, RFC, DIT, CBO, LCOM*, TCC, God Class, Data Class), each read alone | §4.7a, §5, `literature.py`, `setup.sh` | The author's request: to see how the measures the petclinic harness reports go on the development chain, at both levels, before choosing which join H3 |
| 35 | The literature's class measures are read on one row per class and checkpoint, with the class's size held fixed and an intercept for the class; the Maintainability Index and TCC are read reversed | §5, `analyse.R` | On the development chain every class measure came out above the margin (§6), in a model without the class's size, with most of Spring's rows in one class sharing one value and one outcome; and the index's ratio read the wrong way up |
| 36 | H3's measures: at the method, long, cognitive and cyclomatic complexity; at the class, the Gini, WMC and LCOM*. Each fitted alone at its level; the block as first registered (S1, S4, S5 together at the method) is reported. Fan-out and CBO are read with the sinew measures as reach, predicted above 1 | §2, §5, `prepare.py`, `analyse.R`, `verdict.py` | Decided by the author on the recommendation made after the measures were seen on the development chain (§6, §7): the usual shape measures of the literature at both levels; reach is not shape |
| 37 | Corpus B extended to H1 and H2 as restated, the landing reading and a weaker reading of shape; a second unit (every small commit that is not a merge). Corpus C added: repositories with declared agent commits, drawn with seed 3, compared within a repository and against corpus B | §3.2, §3.3, §5, §7 | The author's proposal: the hypotheses now need only a history, so they can be read on people's code from before AI assistants and on code an agent declares it wrote. Drafted; neither corpus is built or read |
| 38 | Corpus C's rule for a declared agent commit is the sampler's own criterion, `--min-agent-commits`, with its built-in signatures | §3.3, `open-source-repository-sampler` | The author's decision: the rule is one other studies will want, and a sampling decision belongs in the sample and its derivation, not in the experiment |
| 39 | The second novelty check (`LITERATURE.md` §10) taken into the plan: common coupling as the precedent of H1; how a bystander differs from common coupling, over-exposure and LCOM; preferential attachment as the rival reading of H2; Zhou et al. and Chowdhury et al. as the two sides of H3 | §1, §2, §4.3a, §7 | So that what is claimed as new is the per-addition measure and the mechanism, not that shared state grows; and so that the nearest rival readings are stated before the runs are read |
| 41 | A refactoring hint is kept for any production Java file (a `.java` file outside a test directory), not only one under `src/main/java/` at the repository's root | `refactor.py` | A fault found while building the histories: the test for a production file was the petclinic root, so every RefactoringMiner hint of a ui stack, whose backend is under `server/`, would have been dropped. No ui run had been read |
| 40 | Corpora B and C built as histories: units, the light reading, arms as sets of units, the repository as the chain, two development samples | §3.2, §3.3, `history.py`, `runs.yaml` | To run H1, H2 and the landing reading on people's code and on declared agent code. The issue-linked unit and the ranks of the landing reading are not built |
| 42 | H3's class measures are tested only where later arrivals fall in at least 10 distinct classes and no one class holds more than half of them; otherwise reported. The method level is H3's test | §5, `prepare.class_level` | Decided by the author after H3 was unresolved on the class's Gini on the development chain (§6): one class there holds 87% of the arrivals, so a class measure describes that class over time. A rule about the data, applying to all three class measures alike, in place of removing one |
| 43 | Corpus B is a sample of its own, by the criteria of `long-method-slim-study`'s: as of 1 December 2020, at least 50 functions in 15 files, three tiers, a new seed, 60 repositories. Corpus C takes the same criteria, a new seed and more draws. No cap on a repository's units | §3.2, §3.3, `runs.yaml` | The author's direction: the size of a repository is for the sample's criteria to say, and that study's were set for the same purpose. The first draft's sample had no as-of date, and seed 3 had drawn a sample already read |
| 44 | Corpus B 300 repositories, corpus C 100 of up to 6,000 drawn; the histories read eight repositories at a time, each worker held to its share of the memory, and whatever fails read again alone | §3.2, §3.3, `history.py`, `runs.yaml` | Decided by the author: the corpora are reported, and 60 and 30 were too few to report on; reading in parallel makes the larger samples affordable, and the pass alone is for a repository too large for a worker's share |
| 45 | The ui runs are the primary test; every petclinic run is secondary, a replication read first. The analysis `petclinic-primary` is renamed `petclinic-just-solve-202608100006` | §3.1, §3.1a, `runs.yaml` | Decided by the author: petclinic puts every rule on one endpoint, so its handler and controller receive nearly everything and the method and class levels are weakly tested there. Made after that was seen on petclinic's development chain (§6) and before any ui backend Java was read |
| 46 | A third kind of value, **introduced**, beside needed and bystanding: the parameters and locals a change adds to a method and the fields it adds to a class. Reported per addition and per bound row, and H2 is read again on what stood by and what was introduced together. H2 is unchanged | §4.3b, §4.4, §5, `Pull.java`, `tables.py`, `analyse.R` | Decided by the author on 19 November 2026, after seeing on the development chain that half of Spring's bound rows have nothing standing by at the method, most of them new methods (§6, §7). The author's argument: a new method brings parameters onto the control flow, so it adds data for later code to be bound to, and added fields are the same thing at the class |
| 47 | H2 restated: a core draws code in. Later intrusions use the values a problem's code was bound to (the core) more, per value, than the rest the place held (the periphery: what stood by and what was introduced); the rate ratio above 1 at the class and at the method. H2 as it stood (per value that stood by) is reported | §1, §2, §4.4, §5, §7, `tables.py`, `analyse.R`, `readings.py` | Decided by the author on 19 November 2026, after the development chain showed bound uses going to a few values there from the start and introduced values hardly ever used again (§6): a few key values everything hangs off, and many that pass through. The operational form is the drafter's and is listed in §8 for the author |
| 48 | H1 renamed *the periphery grows* and H4 *function injection forms no core*; their tests unchanged. Reported beside H4: how much a core value is come back to, function arm against methods arm | §1, §2, §5, §7, `analyse.R`, `readings.py`, `report.py` | Decided by the author on 19 November 2026 on the drafter's suggestion, after H2 as restated had been run on the development chain (§6): with a core that draws code in, H1's rise is the cost of the core and not the pull, and the arms differ most in how much a core value is come back to. Not made a condition of H4 because the function arm has few rows with a core at the class |
| 49 | Corpus B is two sets of 300: `long-method-slim-study`'s own sample (seed `20261101`, the first 100 usable of each tier in draw order) and a confirming set (seed `20261118`) without its repositories | §3.2, `runs.yaml`, `history.chosen`, `history.sample_excluded` | Decided by the author on 19 November 2026: one set shared with that study, one new to confirm it. Corpus C unchanged (its own seed, 100, read only if at least 10 are usable) |
| 50 | H2 at the class: each method a later change's bound code is in is scored on its own (a value once per method); a call to a class's method is a core value, its uncalled and added methods periphery. The class on its fields only is reported | §2, §4.4, `tables.outcome_rows`, `Pull.java` (the class's methods before and added) | Decided by the author on 19 November 2026 ("H2 is all about binding"); the periphery's methods the drafter's choice, for like with like |
| 51 | H1 counts constants, now with the author's reason: a constant in a class binds code to it and belongs in a file of its own | §2 | Decided 17 November 2026; reason given 19 November 2026, so H1 without constants is a reading |
| 52 | H5, choice narrows: a bound addition's alternatives (other places holding what it was bound to, by injected dependency type at the class and by value type at the method) do not rise over the stream; one-sided below 1.25 at the class and at the method; Holm over five | §2, §4.2a, §5, §7, `Pull.java --places`, `tables.choice`, `prepare.h5_rows`, `analyse.R`, `verdict.h5`, `report.py` | The author's, 19 November 2026: "always the same place, or places get restricted over time"; kept apart from H2, which stays on binding. Its margin the drafter's proposal, agreed by the author |
| 53 | The core's width (values per row) reported per arm and over the stream | §4.4, `analyse.R`, `report.py` | The author's question on H2's fit ("counts only, particularly for the core, as we are looking at sinew width"); H2's test unchanged until the author decides |
| 54 | H5 at the method counts only the places on the host's control flow: callers, the request's entry points and what they reach, calls followed by their receiver's declared type; OfficeFloor's flows from its wiring files. The count by type alone is reported | §4.2a, §7, `flow.py`, `tables.choice`, `Pull.java` (calls, supertypes) | Decided by the author on 19 November 2026 after the development chain showed type alone counting every new method that handles an `Owner` (§6), the case §4.2a foresaw. Before the tag, so a revision |
| 55 | H5 read on corpora B and C, with an index of the tree kept running through each history | §3.2, §4.2a, `chain.tree_places` | Decided by the author on 19 November 2026 |
| 56 | H6, forced changes spread: the classes a unit places or edits code in rise over the stream and are more where a placement was forced at the class; one-sided above 1, each needed; Holm over six. Reported: the coupling (calls followed) of pairs of classes changed together, on the index, and the pairs whose coupling rose, by name | §2, §3.2, §4.2b, §5, §7, `flow.Graph.class_calls`, `tables.pair_rows`, `prepare.h6_rows`, `prepare.co_change`, `analyse.R`, `verdict.h6`, `report.py` | The author's, 20 November 2026, after seeing H5 on the development chain (§6): "if continually having to change two classes due to lack of choice, highlights lack of cohesion (things that change together should stay together)", and the coupling between them a case for redesign. The operational form the drafter's. Before the tag, so a revision |
| 57 | H6 counts only classes that existed before the unit (a new class is a free choice); H6's test is the forced ratio alone, the rise over the stream reported over all units and in forced and unforced units apart | §2, §4.2b, §5, `prepare.h6_rows`, `analyse.R`, `verdict.h6`, `report.py` | Decided by the author on 20 November 2026 after H6 on the development chain and histories (§6): the pilot's spread did not rise (the change piled into the core class) while forced units spread wider, and OfficeFloor's spread was mostly new classes, one per function. Before the tag, so a revision |
| 58 | H6's accountings, reported: the growth of existing classes by the kind of placement that added it (forced, chosen, unbound), and the coupling between classes each unit added (tree after less before), in forced units and between pairs changed together | §2, §4.2b, §7, `tables.coupling_rows`, `tables.pair_rows`, `prepare.growth_accounting`, `prepare.coupling_accounting`, `report.py` | The author's, 20 November 2026: to see the cause of the growth in size (absorbing) and, where a change spreads, of the growth in coupling |
| 59 | H7, forced changes couple: a class a forced change goes into gains more calls across its boundary (outward and inward) in that unit than one an unforced change goes into; one-sided above 1; Holm over seven. Reported: whether the calls reach members exposed or widened (method access, read by the instrument) | §2, §3.2, §4.2c, §5, §7, `Pull.java` (`access`, VERSION 14), `flow.Graph.cross_edges`, `tables.encapsulation_rows`, `prepare.h7_rows`, `analyse.R`, `verdict.h7`, `report.py` | The author's, 20 November 2026: "a forced change that requires data from another place couples to that other place or asks for the encapsulated data of that other place to be widened (made public) for it to couple to ... an increase in coupling between the encapsulation and other parts of the system". The operational form the drafter's. Before the tag, so a revision |
| 60 | A reported reading, split or concentrate: a class whose forced changes fall into groups sharing none of its values, and a pair changed together repeatedly over the same data with coupling rising; drafted with a check against the developers' later refactorings, withdrawn by the author the same day (the refactorings are still recorded, not read) | §2, §4.2d, §7, `tables.refactoring_rows`, `prepare.redesign`, `report.py` | The author's, 20 November 2026: "mutual exclusion in the encapsulated items and coupling in the changes ... cause for question of cohesion of the encapsulation and where splitting is right", and "coupling between a small number of encapsulated units but constant change across them for similar data, then there is reason to concentrate". The operational form the drafter's |
| 61 | H6 and H7 hold the change's size fixed: log(1 + positions added) and log(1 + methods changed), per unit for H6 and per class in the unit for H7; their forced ratios without size reported | §5, §8, `prepare.h6_rows`, `prepare.h7_rows`, `analyse.R` | Decided by the author on 20 November 2026 after the drafter showed on the development data that forced units are larger changes (Spring 13 positions and 3.9 methods against 8 and 2.4), and that within size the pilot's forced effect on spread disappears (1.0 against 1.1 small, 2.1 against 2.0 large) while the human histories' remains for large changes (jmxtrans 4.1 against 1.9, UsbSerial 2.4 against 1.6). Before the tag, so a revision |
| 62 | The novelty check's suggestions (LITERATURE.md §10, 20 November 2026): Pescio's use of *gravity* acknowledged; Page-Jones (connascence), Ousterhout (deep modules) and Kobori et al. with Vidal et al. (widening) cited at H7; the split/concentrate reading placed against Extract Class and co-change Move recommenders and Paixão et al. 2017; conservation kept as framing (Tesler, Hatton, Pescio); Lopes and Ossher (size scaling) and Taube-Schock et al. (unavoidable high coupling, H7's rival reading) in §7. No measure, model or rule changes | §1, §2, §4.2c, §4.2d, §7 | The author's, 20 November 2026 ("apply the plan suggestions from the novelty check"). Most sources read as abstracts or records; marked where unchecked |
| 63 | Reported readings: surface against volume (a class's links across its boundary against its methods, the exponent across classes and within a growing class; surface a change adds, forced against unforced) and ripple (later changes to a method a new call reached that also change the caller, by forced and by opened) | §4.2e, `tables.boundary_rows`, `tables.edge_rows`, `prepare.surface_rows`, `prepare.ripple`, `analyse.R`, `report.py` | The author's, 20 November 2026 ("draft and build surface vs volume and ripple"). Operational form the drafter's |
| 64 | H5 tested at the class only, its method level reported; the ripple reading against chance (the share of a chain's units that change the calling class anyway) | §2, §4.2e, §5, `verdict.h5`, `prepare.ripple`, `report.py` | Decided by the author on 20 November 2026 after the development chain: the method level shows the encapsulation's volume growing, which the author's reading of H5 expects. Before the tag, so a revision |
| 65 | *Forced* is forced by encapsulation: code bound at the class to a private field (a private constant among them) or a private method; a public constant does not force; forced by binding with no alternative reported beside it. Fields' access and reads of other classes' fields tracked, so public fields count in coupling, exposure and widening | §2, §4.2b, §4.2c, `Pull.java` (VERSION 15: `fields`, `constants`, `reads`), `flow.Graph`, `tables.encapsulated`, `tables.forced`, `prepare.py`, `analyse.R` | Decided by the author on 21 November 2026, on the drafter's proposal after the author asked what forced should mean where there is no injection (corpus B), and that public fields be tracked. Before the tag, so a revision |
| 66 | Two tiers: confirmatory H2, H4, H5, H6, H7 (Holm over five); secondary H1, H3 (each on its own p, reported as secondary) | §2, §5, `verdict.py`, `report.py` | Decided by the author on 21 November 2026, on the drafter's proposal: the necessity is to find the force; a smaller family keeps power. Before the tag, so a revision |
| 30 | Terms: a *tie* is now a **binding**, and code that was *tied* to a place is **bound** to it; the *equivalence bound* is now the **equivalence margin** | throughout, and every table and column name | The author's choice: "tie" reads as a draw. "Coupling" was not used because the plan already uses it for the wider thing (the problem's own coupling, the wiring). The margin was renamed so that "bound" has one meaning. No measure, model or rule changes. The pilot report (`results/pilot/PILOT.md`) keeps the old word |

The direction of H4, the thresholds, the margin's values, the amount band, the wiring
conditions, the runs read and the Holm correction over four hypotheses are unchanged. The author
confirmed row 22 on 17 November 2026: H4's condition is the arm's rate ratio in intrusion, and the
count of places reopened is reported.

# Plan: where a new problem's code lands, and whether it had a choice

> **Status: NOT YET REGISTERED. The tag `plan-v1` was withdrawn on 17 November 2026, before any
> run named for analysis was read, while the hypotheses are worked out on the development chain
> (§9, five revisions so far, the last still growing: rows 72 to 88 follow a review of the plan on
> 22 November 2026; rows 89 to 110, of 24 and 25 November, restate H5 as surface against volume,
> make H1 an arm contrast, number the hypotheses in the order of the study's story, settle the
> drafter's remaining choices, and after a consistency review make H1 the arm contrast alone,
> delete H9 and count constants in H5). It will be set again when that work is done, and waits now on Run
> B's ids; until then only the development chain can be read.** As first registered, on 16 November 2026: the tag was first pushed on commit
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
(El Emam et al. 2001; Zhou, Leung and Xu 2009, abstract only) found that many structural metrics carry little
information once size is controlled; Chowdhury et al. (2022b) answer that, with size in the model
as a covariate, method-level metrics still predict maintenance (LITERATURE.md §10, *Full read*).

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
  that gathers things in a design. Read in full on 22 November 2026 (LITERATURE.md §10, *Full
  read*): his gravity is attraction by mass, large functions and classes drawing more code (Ch. 2,
  December 2008), which he later put down to co-change ("temporal and spatial entanglement");
  access protection is for him a separation that works *against* gravity (Ch. 1), and his 2024
  draft retires the word *force*. That is the preferential-attachment reading H2 holds fixed
  (§7), not this study's mechanism. This study's sense is the one above: binding to particular
  values, with size held fixed, measured per addition.
- **Core and periphery** (stated 19 November 2026, §9). The last sentence was the reading until
  then. On the development chain the data that gathers is mostly not what later code comes for
  (§6): later code comes for a few values that code there was already bound to, the place's
  **core**, and the rest, the **periphery**, is what it then has to sit beside. So the pull is
  the core's (H2), the growth is the periphery's and is its cost (H3), and a form that hands each
  function its own data forms no core (H4).

- **Essence and accident** (the author's, 22 November 2026, §9 row 81). Brooks (1987) divides a
  program's difficulty into the essential, which is the problem's, and the accidental, which is
  the representation's. The author's claim: the essential complexity is **the logic**, what the
  statements of the methods compute, with the data each piece of logic needs; the construct of
  **methods calling each other and passing state** is accidental. "The method organisation is
  just to supply data to the logic of the methods. OfficeFloor removes this accidental
  complexity making it focus on the essential complexity of the function logic." The plan
  already measures on that line without having named it: only a method's body statements carry
  the value of a change, and signatures, declarations and wiring are organisation (§4.3); the
  values a problem needs are the problem's, and what surrounds them is the placement's (§4.3a).
  Three cautions, the drafter's. Brooks himself puts "invocations of functions" and the
  relations among data in the essence, so this is the author's refinement, not Brooks's view:
  *which* data a piece of logic needs is essential, *how it reaches it* is not. It is nearer
  Moseley and Marks (2006), who hold that most complexity is accidental, chiefly state and
  control, and should be kept apart from the essential logic. The order in which functions run
  is still the problem's; OfficeFloor keeps it, in its wiring, so it moves that part of the
  organisation and does not remove it, and the wiring is counted as the function arm's
  organisation (§4.9). And organisation does more than supply data: it also names and groups
  for a reader (§4.2f). The reading of §4.9 states the claim so that it can fail: the same logic
  in both arms, and less state handed along in the function arm.
- **The overview** (the author's, 24 November 2026, §9 row 91; the whole study in one argument):
  "Blocks of code are the essential complexity. If we write a small programme, it is essential one
  block of code with method wrapping necessary to call it. And in some languages they do without
  the wrapping main(String[]) method. So as the programme grows, and concentration becomes too
  much in one place, separation occurs requiring coupling and in case of Spring method calling to
  allow control flow between the blocks of code. Hence, this becomes accidental complexity of
  method structure to the essential complexity of the logic within those methods. Function
  injection maintains the block of code and can be a single function for simple programme. It can
  also expand out to many functions to disperse the blocks of code. However, it does not have the
  same accidental complexity of method tight coupling that it's control flow allows with function
  injection." Read against the hypotheses: encapsulation's force gathers the blocks into one place
  (H1, H2) and what gathers there has its cost (H3); separating them takes coupling, the surface
  that keeps the concentrations coordinated, and H5 counts it against the blocks it joins; function
  injection disperses the blocks without that coupling (H4, H5). H5 counts links, not how tight
  they are: a wiring edge counts as much as a method call, so the test does not credit the
  function arm for its looser control flow, and is the harder for it.
  - *Splitting, and the reviewer* (the author, the same day; a claim, not tested): "it is much
    easier to split a function injection function with the control flow and an AI reviewer can
    isolated look at a function injection method for it's cohesion. This is much harder with the
    method structure, as there is a lot of coupling that restricts the splitting." A function
    receives what it needs and hands on what it produces, so it can be read, and split, alone; a
    method is held by the fields and the callers it shares with its class. This is why the author
    holds the function arm's drift towards called methods (§4.9, §7) to be a lapse that a review
    can find and undo, where the methods arm's coupling is held in place by its structure. No
    measure reads it yet; a reading of how far a unit can be read alone (the links it has outside
    itself) would be one.

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
the part of that claim tested is the mechanism: a place gathers data (H3), and later code comes
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
**tests** the claim rather than assuming it. H6 asks whether the shape measures the earlier studies
used predict later intrusion once the problem, the bindings and the bystanders are held fixed (§2, §4.7).

### 1.1 What this plan absorbs (16 November 2026)

Three plans read the same runs with measures of the solution's shape. None has read a run. Two are
unregistered drafts. The SinewSlim analysis plan's file says it is a draft, but its rule makes
registration the commit of the file, and that commit was pushed on 31 October 2026 with a message
calling it registered; it is therefore withdrawn by a dated amendment on its own branch, not
simply closed. Their measures enter this plan as the shape competitors of H6, or as checks, so one
registration covers them:

- **The flow-injection-containment draft** (`flow-injection-containment-experiment`, 20 October
  2026; closed by its own commit). Its junction share (P1) becomes the host-level junction measure
  of §4.7 (since 17 November 2026 a sinew measure, read apart from H6). Its conservation check (P2) is §4.6, with its band. Its trajectory (P5) is H3's checkpoint
  slope, read per arm. Its god-unit count (P3) and its gated-condition lever (P4) are dropped.
- **The ui harness's SinewSlim analysis plan** (branch `sinewslim-analysis-plan`, 31 October 2026).
  Its not-slimmable methods (H3) become a measure of §4.7 (since 17 November 2026 a sinew measure,
  read apart from H6). Its mechanism (H2, behaviour
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

![Placement forces map: encapsulation is the force; code is forced into a class, less often
under function injection and less so over time (H1); a forced change concentrates (cost: size, H2,
H3) or reaches out, and the concentrations are coordinated by links (cost: coupling, the surface,
H5); shape (H6) and co-change spread (H7) are the literature's readings, predicted not to see it;
function injection forms no core (H4, the control); Run D removes encapsulation by hand
(H8)](figures/placement-forces.svg)

*Redrawn on 24 November 2026 (§9 row 97) in the numbering of row 93; H1 and H5's links
updated on 25 November 2026, through row 110.*

*How the hypotheses fit together* (a map, not a rule; the hypotheses below govern). A change
bound to data no other class can reach is forced. It pays in size by concentrating, or in
coupling by dispersing; the readings (§4.2d, §4.2e) show where code stands between the two. The
rivals are the literature's two ways of looking, by shape (H6) and by co-change (H7), and the
change's size and unavoidable tail coupling, held fixed. The control is the construct that holds
no state privately (H4). Drawn on 21 November 2026, through row 67; the figures on it are the
development chain's (§6).

**Two tiers** (decided by the author on 21 November 2026, §9 row 66). The study's necessity is to
find the force. The **confirmatory** family is the force and its two outlets, with the control,
each comparing the forms: **H1** (the force: the function arm is forced less, and the gap widens;
restated 25 November 2026, §9 row 107), **H2** (concentration: a core draws code in), **H4** (the control: function
injection forms no core) and **H5** (the surface: for the same logic, fewer links between blocks
of logic under function injection, and the gap widening; restated 24 November 2026, §9 row 89).
Holm over these four. **H3** (the encapsulation fills, the cost of concentration), **H6** (shape
does not draw code in) and **H7** (spread does not see it) are **secondary**: each keeps its
direction and rule and is decided on its own p, outside the correction. (H9, the cost to fix a
concentration, was secondary from 25 November 2026 until it was deleted later the same day,
§9 rows 105 and 108.) H6 and H7 are the existing literature's two ways of looking for the cause, by shape
and by co-change, each predicted not to find it. (Until 21 November 2026, later, H7 was
confirmatory, as *forced changes spread*, and Holm was over five; §9 row 67.) The readings
(§4.2b–4.2g, and the sinew shape, §5) are reported. **H8** (Run D, §3.1a; registered on 22 November 2026, §9 row 76) is
the one test in which the cause is changed by hand: the same stack with the agent told to leave
everything public. It is run after the others, on its own run, and decided on its own p.

**Forced** (decided by the author on 21 November 2026, §9 row 65) means **forced by
encapsulation**: a placement whose code was bound at the class to a member no other class can
reach, a private field or a private method. A constant follows its access like any field (the
author, 21 November 2026: "it is good code to move constants to another class and make public for
consumption"): a private constant forces, a public one does not. A placement bound at the class
only to members other classes can reach is *unforced* (chosen); one not bound at the class is
unbound. The definition is the force itself and
works the same with or without dependency injection, so corpus B, which mostly has none, gets the
same contrast as corpus A. Forced by binding with no alternative (H1's class level, §4.2a) is
reported beside it in H7, and stays H1's own measure.

**An injected private field forces too** (decided by the author on 22 November 2026, §9 row 72,
after a review of the plan found §4.3 and this definition at odds over it). §4.3 says a field
holding an injected dependency can be declared by any class, so it need not pin code to this one.
The author: "injection allows it to have choice as a construct, however convenience of connecting
to what is already there shows the choice not exercised ... it is a lever to fix the encapsulation
problem and it needs to be exercised, otherwise private encapsulation is the force." So a
placement bound to a private injected field is forced, like any other bound to a private member.
What injection gives is carved out **inside** forced and reported (§4.2b, *Growth by lever*): the
forced growth bound only to injected private fields is the **opportunity** to duplicate the core
in another class and avoid the concentration, which is the value of dependency injection; the
forced growth bound to the class's own private state, constants and methods has no such lever.
OfficeFloor does not have the problem: everything is injected as parameters, so the choice is
there without being exercised by anyone (H4). H1 counts how far the lever has been used: its
alternatives at the class are the other classes that already hold the same dependencies (§4.2a).

- **H1, the force: forced less with function injection** (restated 25 November 2026, §9 row 107;
  the author's: "this just needs to be OfficeFloor is forced less especially over time"). Per
  checkpoint, the placements forced at the class (bound there with no other class holding what the
  code was bound to, §4.2a) are **fewer in the function arm** half-way through the stream (the rate
  ratio below 1) **and rise less** over it (the arm's interaction with the checkpoint index below
  1), shaped as H4 and H5; both needed. Every checkpoint counts, so a form that binds code at the
  class less often scores lower. A forced placement is one that had nowhere else to go, so this
  counts how often there was no choice: it is the plan's title read directly, *whether it had a
  choice*. The author, on the contrast (24 November 2026, row 92): "it also potentially shows the
  accidental cost of the method structure in Spring handlers (and typical web app servers) over
  function injection of OfficeFloor". Not testable on a history, whose arms do not solve the same
  problems.
  - *Choice narrows, the test until 25 November 2026* (added 19 November 2026; a fall since 22
    November 2026, row 73; reported since): in the methods arm, a bound addition's
    **alternatives**, the other places in the code before its checkpoint that hold what its code
    was bound to (§4.2a), fall as the stream goes on, the ratio of the end of the stream to its
    start below 1 at the class; from 24 November (row 92) with the arm contrast above needed
    beside it. Replaced after the plan's consistency review of 25 November 2026 found that where
    every placement of the methods arm is forced from the first checkpoint, the fall has nothing
    to fall from and cannot be tested, and H1, its contrast with it, would have dropped out: the
    force at its strongest would have left H1 silent. The author: "Is there another hypothesis
    about restricted choice? I'm thinking this just needs to be OfficeFloor is forced less
    especially over time." It stays reported, at the class and at the method, in both arms and on
    the histories, where it was H1's only reading. The author's expectation is unchanged: that it
    is always the same place, or that places get restricted over time, especially at the class.
  - *Why not the fall in the function arm* (seen before it was written, §9 row 92): on the
    development chain the function arm bound code at the class 10 times in 60 checkpoints, the
    methods arm 48 times in 59; but 9 of the function arm's 10 had no other place to go (the
    methods arm's share forced 0.54), with 0.1 alternatives a row from the start. Its choice has
    nothing to narrow from, so a contrast of the two falls would rest on ten rows nearly all nought,
    and a contrast of the share forced would go against the form. The difference is how often the
    force happens at all, not how much choice is left when it does.
  - *Choice narrows as it stood until 22 November 2026* (reported): one-sided as H6, the ratio shown below the
    upper margin 1.25, so that a flat count passed, and a level where every placement was forced
    passed with p 0. Replaced by the author after a review of the plan: a hypothesis named
    *choice narrows* should not be supported by a count that does not move, and a pass with p 0
    made the other three confirmatory tests easier under Holm.
  - *Reported beside it:* the share of placements with no alternative (forced), per arm and third
    of the stream; the function arm's ratio, and the arms' contrast (its injected parameters are
    not bindings, so its alternatives are expected to stay open); the alternatives themselves, by
    name, for each row.
  - *H1 is read at the class only* (decided by the author on 20 November 2026, §9 row 64): "H1
    for method shows increase volume of the encapsulation so it should only be read at the
    encapsulation level of the class". The forced placements are counted at the class; the method
    level is reported.
  - *The author's reading of H1 on the development chain* (20 November 2026, after seeing it, §6):
    new functionality enlarges the area of methods, but binding forces that area into a class. So
    the choice of class narrows while the methods in the class multiply under that forcing, and at
    the method the alternatives on a request's flow widen. H1 and its test were unchanged by this;
    it is the reason for H7.
- **H2, a core draws code in** (restated 19 November 2026, §9). In the methods arm, where an
  addition was bound to a **class** or a **method**, the data of that place is of two kinds
  (§4.4): its **core**, the values the addition was bound to, and its **periphery**, the rest the
  place then held: what stood by (§4.3a) and what the addition introduced (§4.3b). Later code for
  other problems comes there **for the core**. Holding the problem fixed (its checkpoint, the
  addition's size and the earlier rules it declares it crosses) and the host's size, later
  intrusions use a core value more than they use a periphery value: the rate ratio per value is
  above 1, at the class and at the method. With H3: a place gathers data, but what gathers is
  mostly periphery; what the next code is bound to is the few values code there was already
  bound to.
  - **And a core value is come back to less in the function arm** (added to H2's test on 22
    November 2026, decided by the author after a review of the plan, §9 row 77). The ratio above
    can hardly fail by itself: a value one problem already used is likely to be used again,
    whatever the place, as a library's borrowed books are borrowed again (§7, *H2 as restated
    compares two kinds of value*). Both arms solve the same problems with the same data. So if the
    core is only the problems' popular data, a core value is come back to as much in either arm;
    if it is the place, it is come back to less where no place holds values privately. H2 needs
    both: the ratio of core to periphery above 1 at the class and at the method in the methods
    arm, **and** the uses of a core value, function arm against methods arm, below 1 (§5). The arm
    contrast is needed at each level where both arms have at least 10 rows with a core; the
    function arm is expected to form few cores at the class, and where it has too few to compare,
    that is reported and that level's contrast is not needed. On a history (corpora B and C) the
    arms do not solve the same problems, and H2 there is the ratio alone, direction and interval
    only as before. Until then the arm contrast was reported beside H4.
  - *At the class, the core is the encapsulated part* (decided by the author on 22 November 2026,
    §9 row 71, after the development data): "Gravity comes from the force of no choice. Private
    forces that choice. Now if methods are made public over time, then that shows up in coupling
    freeing concentration by encapsulation. So to me the forcing is about not being able to access
    outside the encapsulation, being the force." The class's core is the members the code was
    bound to that no other class can reach: its private fields (private constants among them) and
    private methods. The members it was bound to that others can reach join the periphery; opening
    a member up shows in §4.2c's calls across the encapsulation (widening), not in the core. The method level is unchanged (a method's
    own values are reachable from nowhere else). Reported beside it: the core as it stood until
    then, every member the code was bound to whatever its access (on the development data: class
    17.5 on the pilot, 3.15 on the histories, §6).
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
- **H3, the encapsulation fills** (restated 17 November 2026, twice; renamed 19 November 2026, §9,
  and 24 November 2026, §9 row 93). Until 19 November it was called *gravity compounds*, and until
  24 November *the periphery grows*: its test is unchanged, its reading is not. Inside an
  encapsulation every method can reach every field, so the state a class gathers is visible to
  every new block put there, needed or not: what a reader has to hold, and where later state
  links (H5) come from. What
  rises is mostly periphery (H2): not what draws code to a place, but what code drawn there has
  to sit beside, the cost of the core. In the methods arm, the
  bystanders of an addition (§4.3a) rise with the checkpoint index (positive slope, 95% interval
  above 0). They rise over all additions, and **within a place**: among the additions that go into
  one class, the later ones find more of the class's data standing by, and likewise within one
  method. The place itself gathers data; the rise is not code moving to places that hold more.
  - *Constants count* (decided 17 November 2026; the reason the author's, 19 November 2026). A
    constant left in a class binds code to that class, and is typically why code is put there; it
    belongs in a file of its own that any place can use. So a constant gathering in a class is part
    of what H3 predicts, and H3 read without constants is a reading, not a test of it.
  - *As first registered:* the addition's bindings rise with its host's size and with the checkpoint
    index. That is kept and reported beside it. It was replaced because the bindings an addition has
    are largely the data its problem needs, and because nearly every Spring run into an existing
    method already has one (the ceiling the pilot found).
- **H4, function injection forms no core** (restated 17 November 2026; renamed 19 November 2026,
  §9, from *keeps the space open*; its test is unchanged). Each function is handed its own data,
  so no place holds values that every later problem has to come to. On the same
  stream, the function arm's bystanders are fewer, and their slope on the checkpoint index is
  flatter, than the methods arm's; and its bound code is **come back to less**, at the class and at
  the method (§4.4). (*As first registered:* its bindings are lower and their slope on host size
  flatter; kept and reported beside it.) **And its changes go back into less well-trodden files,
  production Java and wiring counted alike** (added on 22 November 2026, decided by the author
  after a review of the plan, §9 row 78; the count changed the same day, row 82, below). The condition above counts the methods arm's return to
  its handler and not the function arm's return to its wiring file (§7, *The function arm's
  calling method is its wiring*), and a rule of the plan, that an injected parameter is not a
  binding, decides how much of the function arm is followed at all. This count rests on no such
  rule: per checkpoint, the files that existed before it and that it changed, whatever they hold
  and whether its code was bound there or not; and for each such file, the earlier checkpoints
  that had already created or changed it, summed: how well-trodden the files it went back into
  were. The function arm's rate has to be below the methods arm's (§5).
  - *As first built that day* (reported): the plain number of existing files gone back into. On
    the development chain it went against H4 (1.50 [1.16, 1.94], §6). The author's reading of
    that, borne out by the chain's files (§6): OfficeFloor makes about one new file a checkpoint
    and goes back into many small files a few times each (49 files, the busiest at 24 of its
    60 checkpoints and most at four or fewer), where Spring goes back into one file at 43 of its 59
    checkpoints. A plain count of files scores the first as more, which is dispersion, and the
    plan does not hold dispersion to be bad (§1); what H4 claims is that no place keeps being
    come back to. **The count was changed after that was seen**, to one that tells a return to a
    place every problem has been put in from a return to several places each touched once, and
    on that chain the new count goes the function arm's way (§6). That order is recorded here
    and in §7; the plain count stays reported so that a reader can weigh both. It is the count H4 first had as a condition (reopening, §4.4), without the
  binding rule and with the wiring in it; on the development chain that count went against H4
  before the binding rule and was unresolved with it (§6). The total amount
  (positions, tokens) of the function arm lies within 0.8 to 1.25 times the methods arm's, the
  band the flow-injection draft took from the conservation study's spread. The coupling that
  leaves the scopes appears as wiring (§4.5) and is reported, not hidden: injection is known to
  raise counted coupling (Sun et al. 2022, read in full: coupling rises as injection increases),
  so a higher wiring count in the function arm is the expected direction, not a failure of H4. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `files`; §9 row 112.)*
  - *Reported beside it* (19 November 2026): how much a core value is come back to, function arm
    against methods arm (§5). It is where the arms differ most on the development chain (§6), and
    both arms solve the same problems, so a core that was only the problems' shared data would be
    used alike in both. It is not a condition of H4: few of the function arm's rows have a core
    at the class (one on the development chain), so as a condition it would often not be
    estimable.
- **H5, surface against volume** (restated 24 November 2026, §9 row 89; the author's). The force of
  encapsulation makes concentrations (H2); coupling is the surface that keeps those concentrations
  coordinated. The author: "volume being encapsulated complexity and surface being coupling", and
  "the method calling structure is possibly considered accidental complexity and the essential
  complexity is the blocks of code contained in the methods. Hence, function injection does away
  with much of the method calling and the accidental complexity of trying to call all the blocks
  of code with the method call structure" (§1, *Essence and accident*); "data is sinew and
  concentration force, gravity". So a checkpoint's **volume** is the logic it added (the statements
  of method bodies, §4.9), and its **surface** is the **links** it added between blocks of logic
  (§4.2c): a method calling a method, in its own class or another; a method using a field that
  holds state, of its own class or another's; and, in the function arm, a function wired to the
  next. **Each link is weighed by the data it carries** (decided by the author on 24 November 2026,
  §9 row 95, after the development chain had gone against the plain count, §6): a method call
  weighs 1, plus 1 for each parameter and 1 if it returns a value; a use of a field holding state
  weighs 1; a wiring edge weighs 1, plus 1 if it carries a value (a `next:` from a function that
  returns one, an output whose flow takes an argument). **A constant's use is a state link**, weight
  1, as a field's (decided by the author on 25 November 2026, §9 row 109, after the pilot had been
  seen; until then constants were left out, the drafter's, never put to the author): a constant
  ties the blocks that use it to the class that holds it, as it forces code there (§2, *Forced*);
  the test without them is reported beside. The author: "a method call is calculated
  as 1 for the call, +1 for every parameter, +1 if has return type. Then the wiring for function
  injection is just 1 as no parameters or return type"; the +1 where an edge does carry a value is
  the drafter's, chosen by the author so that the weights do not favour the function arm by
  construction. Until then a link was counted once however heavy (the author: "a link might be
  heavier but the existence of the link is the coupling"); that count is reported beside. **Where
  the weights credit the function arm** is stated here: in OfficeFloor the data passes between
  functions mostly through injected values (`Out<T>` published by one function, `@Val` received
  by the next), which weigh nothing, where Spring passes the same data as parameters, which weigh
  1 each. That is the claim itself (data is not handed along the control flow), and it rests on
  the decision just below. **Injection is not surface**, in either arm: an
  injected dependency, a field the Spring container fills or a parameter OfficeFloor injects,
  gives flexibility and is not bound to the control flow (the author: "similar to injected
  dependencies in Spring provide flexibility. They are not associated with the control flow
  (sinew of data bound to the control flow)"); a call made on an injected object is a call link
  like any other. **Shaped as H4** (the author: "make similar to H4"), both needed: for the same
  logic added, the function arm adds **fewer links** half-way through the stream (its rate ratio
  below 1), **and the gap widens** over the stream (the arm's interaction with the checkpoint
  index below 1). The reasoning: in the methods arm a block's data reaches it through the call
  chain and the fields of its class, and both grow with the system; in the function arm the data
  is injected into the function that needs it, and the next step is one wiring edge. Not testable
  on a history, whose arms do not solve the same problems.
  - *Seen before it was written* (the order is recorded, §9 row 89): the outer surface of §4.2e
    on the development chain, close in the two arms (across the classes of the last tree 0.73
    [0.60, 0.86] in the function arm against 0.78 [0.60, 0.96]; within a growing class 0.82 and
    0.85); and the logic and organisation reading (§4.9): the same logic in both arms, the
    organisation counted in lines higher in the function arm (1.51 [1.29, 1.75]), and the
    function arm writing fewer wired functions and more called methods as the stream went on,
    which brings the calling structure back inside it (§7). The links themselves had not been
    measured.
  - *Until 24 November 2026 the coupling hypothesis (then H7) was* **forced changes couple**: in the methods arm, a class a
    forced change goes into gains more calls across its boundary than one an unforced change goes
    into. Deleted that day at the author's word (§9 row 90); its test and readings are gone from
    the code, and its measure, the calls across the encapsulation (§4.2c), stays for H8.
  - *Prior work* (LITERATURE.md §10, novelty check of 20 November 2026; read as abstracts or
    records unless said): encapsulation as a force is known as a concept, not as a measure.
    Page-Jones's connascence (1992, 1995) holds that a dependency across an encapsulation
    boundary is worse than one within it, the stronger the worse; Ousterhout (2018) argues for
    deep modules, much behind a small interface, and against information leakage across them.
    Neither measures a change. Nearer arguments, also unmeasured (read in full, 22 November 2026):
    Pescio ("Ask not what an object is", 2012) that exposing a private part through get/set makes
    an update non-local; Taube-Schock, Walker and Witten (2011) that limits on a module's size
    push links across modules; Schach et al. that "coupling is a necessary consequence of
    modularization". Steimann and Thies (2009) find that moving a class can be done in 85% of
    cases with no access changed and 99% if access may change, so about one move in seven needs
    widening. Widening is measured per member across releases, not tied to the change that caused
    it (Kobori, Matsushita and Inoue 2015, not obtained; Vidal et al. 2016, read in full:
    over-exposure is mostly set at a class's first version and 86% of over-exposed classes stay
    so), which is why widening is expected to be rare and exposure the usual route. That the amount
    is conserved and placement divides it is a framing only (Tesler's law; Hatton 2014; Pescio's
    *physics of software*, Ch. 13: "we don't really change the mass of code"; Loth 2026,
    Corollary 2.2.2, unrefereed), not a tested law; the study keeps it as framing and tests how
    the same logic is joined (the links), not conservation itself (which H4's amount band and §4.9's
    logic only check). Ousterhout's deep module is the nearest to H5: much volume behind little
    surface.
- **H6, shape does not draw code in** (made one-sided 17 November 2026; its measures set 18
  November 2026, §9). With the problem held fixed, and the bindings and the bystanders in the
  model, the shape of the place the addition landed in does not raise the intrusion that follows
  there, at the method or at the class. The shape measures are the literature's (§4.7, §4.7a):
  - **at the method:** long (S1), cognitive complexity (S4) and cyclomatic complexity;
  - **at the class:** concentration (the Gini of S5), weight (WMC) and lack of cohesion (LCOM*).

  Not among them: not slimmable and junction (S2, S3), the author's sinew measures of how data
  flows through a method; and fan-out and CBO, which measure how far a place reaches out and are
  read with them (§5, *The sinew measures*). Each of H6's measures is fitted by itself, and its
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
  object-oriented metrics with change-proneness, while Chowdhury et al. (2022b), read in full,
  conclude that method-level metrics stay useful predictors of maintenance with size as a
  covariate (size divided out does not neutralise it; size in the model does). H6 holds data fixed, not only size, and
  the problem; its method-level result is to be set against Chowdhury et al.
  - *A sensitivity reading, with the coupling measures put back* (decided by the author on 22
    November 2026, §9 row 75). Fan-out and CBO were taken out of H6 as reach after fan-out was
    seen above the margin on the development chain (§7), and the literature counts them, with RFC,
    among its structural metrics (Chidamber and Kemerer 1994). So H6's rule is also read over its
    six measures **and** the method's fan-out and the class's CBO, RFC and fan-out, each alone,
    where they vary. It is reported beside H6 with its state (not above, unresolved, against) and
    the measures that lie wholly above the margin, and it changes no verdict: a reader who holds
    that coupling is shape can read H6 that way.
  - *H2 and H6 were one hypothesis* (H2a and H2b) until 17 November 2026, supported only if both
    held (§9). They are now decided apart: one is a difference to be shown, the other an
    equivalence, and the second should not decide the first.
- **H7, spread does not see it** (restated 21 November 2026, later, §9 row 67; the author's).
  Co-change spread, the measure of the change-coupling literature (logical coupling, Gall, Hajek
  and Jazayeri 1998; co-change rules, Zimmermann et al. 2005; change coupling and defects,
  D'Ambros, Lanza and Robbes 2009; Shotgun Surgery from co-change, Palomba et al. 2015;
  LITERATURE.md §4), is not wider where a placement was forced by encapsulation than where none
  was, at the same change size and point in the stream: the forced ratio of the spread (below) is
  **not above** the upper margin 1.25, one-sided, as H6. The author's reasoning: that literature,
  like the shape literature, reads a symptom to find a cause; cohesion has no shape to highlight,
  so the force of encapsulation does not show in how many classes a change touches. Where it
  shows is what the force costs at the boundary (§4.2c; the surface, H5). H7 argues against that literature's
  *reading*, that co-change reveals a cause (Gall et al.; Palomba et al.'s symptom framing), which
  D'Ambros et al. themselves call an untested assumption; it contradicts no finding (LITERATURE.md
  §10, *Full read*). None of the six papers read controls for change size: the field drops large
  transactions (more than 30 entities, Zimmermann et al.; more than 100 classes, D'Ambros et al.).
  Gall et al.'s subsystem that grows without coupling is an early instance of spread missing what
  happens inside a unit. H7 is secondary, beside H6: the existing
  literature's two ways of looking, each predicted not to find the force. Its measure, model and
  terms are unchanged; only its direction and tier changed. *Seen before it was restated* (§6):
  on the development chain 1.026 [0.380, 2.775] (unresolved on one chain an arm); on the
  development histories 0.845 [0.644, 1.108]; without the change's size 3.656 and 1.987, which is
  what the spread follows.
  - *As first drafted* (20 November 2026, §9 rows 56-58), **H7, forced changes spread**: in the methods arm,
  a change with no choice has to be made in more classes at once: the number of classes that
  existed before it that a unit places or edits code in (its **spread**, §4.2b) is wider in a unit
  where a placement was forced at the class (bound there with no other class holding what it was
  bound to, §4.2a) than in one where none was, at the same point in the stream. One-sided. A new
  class is a free choice and is not counted (decided by the author on 20 November 2026, after the
  development chain, §9). As first drafted, H7 also needed the spread to rise over the stream; the
  author decided the same day to focus on forced and to track forced and unforced units apart, so
  the rise is reported, in each apart (§9). The author's
  reasoning: things that change together should stay together, so a change that keeps having to
  go into two classes because it has no choice shows that the two lack cohesion, and that
  placement (in particular which class encapsulates which fields) should be redistributed between
  them. H7 joins H1 (choice) to its cost across classes, as H2 joins binding to its cost within
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
- *H9, the cost to fix a concentration* (stated 25 November 2026, §9 rows 104 and 105; **deleted**
  later the same day at the author's word, row 108): the fewest internal links a cut must cross to
  divide a class into two parts, the function arm's below the methods arm's at the same size. The
  author, on reading it again: "I'm now questioning H9 and its value ... it is only looking at
  cutting up methods"; and it measured only inside the class, where the cost of a rewrite (its
  callers, its tests, the members a split must open) lies mostly outside it. On the development
  chain it showed no difference (§6). Its code is removed; the containers reading (§4.2g) and H5
  carry the shape it was after.
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
- **A reading: encapsulation and the reader** (added 22 November 2026, §9 row 69; the author's
  question; reported, not among the tests). Encapsulation does two jobs: it keeps what a reader
  must hold small (comprehension), and it keeps a change local (containment, Parnas). The author
  asks whether the first is a human limit that agents do not share until a system outgrows their
  context window. The force itself does not depend on the reader: a private member admits only
  code inside its class, whoever writes it (§2, *Forced*; the claims are about code, §8). What may
  depend on the reader is how much encapsulation is made and kept, and how much size a class is
  let reach before it is split. The reading (§4.2f) compares declared agent commits with human
  commits on four things, and asks whether the difference changes with the system's size against
  a context window. Its stated direction, the author's question put as a prediction: agent
  commits make fewer members private, widen more, and let classes grow larger than human commits
  where the system fits in a context window, and the difference narrows where it does not. If
  none of the four differs, encapsulation's use is the same for both readers and the question is
  answered the other way; both outcomes are reported.
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

- H1: a function arm forced as often as the methods arm, or more, or forced more and more as the
  methods arm is: the force would then belong to the problems, not to the method structure.
  (Until 25 November 2026 also: alternatives at the class that do not fall over the stream.)
- H2: later code using a periphery value as much as a core value, at the class or at the method.
  The data of a place would then be taken up alike, and the place would have no core.
- H2, the arm contrast: a core value come back to as much in the function arm as in the methods
  arm. The core would then be the problems' shared data, used alike wherever it is put, and not
  something the place does.
- H3: no slope, or a negative one, over all additions or within a class or a method. The
  surroundings of a problem's data would then be a constant cost of the form, not something that
  grows. A rise over all additions with none within a place would mean that code moves
  to fuller places, not that places fill.
- H4: no difference between the arms in bystanders, in their growth or in later intrusion, or an amount
  outside the band (the difference is then a difference of amount, not placement), or a function arm that moves its coupling into the wiring:
  wiring per problem that rises over the run, or one configuration file that holds most of it
  (§4.5).
- H4, the symmetric count: the function arm going back into files as well-trodden as the methods
  arm's, or more, once its wiring files are counted: its endpoint's flow file would then be its
  handler under another name, and its coupling would have moved, not gone.
- H5: as many links for the same logic in the function arm as in the methods arm, or a gap that
  does not widen over the stream. Function injection would then move the coordination into the
  wiring rather than remove it, and the calling structure would not be the accidental complexity
  the author holds it to be. (Until 24 November 2026: a class a forced change goes into gaining no
  more calls across its boundary than one a change goes into unforced.)
- H6: any shape measure followed by more intrusion, beyond the margin, with the problem, the
  bindings and the bystanders held fixed. That would mean that shape draws code in by itself. A
  shape measure followed by less is reported, and does not count against.
- H7: a spread wider where a placement was forced than where none was, beyond the margin, at the
  same change size. Co-change would then see the force of encapsulation, and the change-coupling
  literature would find what this study says it misses. (As first drafted, H7 was the opposite:
  a spread no wider where forced would have refuted it.)
- H8 (Run D, §3.1a): with nothing private, bound code come back to as much at the class, or no
  more calls and field reads added across class boundaries. Encapsulation would then not be what
  concentrates code, or removing it would not disperse it.

Every one of these outcomes is reported whichever way it points.

## 3. Data

### 3.1 Corpus A: the paired streams (confirmatory)

**The ui runs are the primary test** (decided by the author, 18 November 2026, §9). The verdicts
on the hypotheses (H1 to H4 as first registered) that the study reports as its test are those of the ui analysis (§3.1a): Spring
against OfficeFloor over its Runs A and B. The petclinic runs are **secondary**: read first,
because they exist, each as a replication with its own verdicts, and none of them the study's
test.

- *Why.* The petclinic stream sends every rule through one endpoint, `POST /api/owners`. So one
  handler method and one controller class receive nearly everything, in every chain: the method
  level of H2 rests on a single method per chain, and the class level cannot tell classes apart
  (§6). That is a property of the stream, and it makes petclinic a weak test of exactly the
  levels the hypotheses are about. The ui stream has many endpoints and 250 checkpoints.
- *What had been seen.* This was decided after the development chain of petclinic showed H2 at
  the method resting on one method, and H6's class measures untestable there (§6). No ui run's
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
- **Run D** (the no-encapsulation run; decided by the author on 22 November 2026, drafted the
  same day, §9 row 70): the `angular-spring` stack on the same stream, agent and harness, with
  one instruction added to the agent's prompt: **do not encapsulate; leave every field and method
  public**. It is a run of its own, never pooled. It is read against Run A's `angular-spring`
  (the same front end, back end and stream, so the instruction is the only difference) and is
  not run on OfficeFloor, where every dependency is injected and nothing is left to make public
  (the author). It isolates encapsulation where Run C isolates injection: with nothing private,
  no placement can be forced by encapsulation (§2, *Forced*), so whatever the force does in Run
  A should be absent or weaker in Run D. Its run ids, the harness commit carrying the instruction,
  and the instruction's exact wording are added by a dated amendment before any of its backend
  Java is read.
  - **Its test is registered: H8, without encapsulation code disperses** (decided by the author
    on 22 November 2026, after a review of the plan, §9 row 76; until then every reading of Run D
    was reported). Forced against unforced within a run is a comparison of placements nobody
    assigned; Run D is the one place where the cause itself, encapsulation, is taken away by
    hand. H8, Run D (*open*) against Run A's `angular-spring` (*encapsulated*), needs both:
    - *concentration weaker:* the open arm's bound code is come back to less at the class, the
      rate ratio of later intrusion at the class (H4's model, §5) below 1;
    - *dispersion stronger:* its units add more calls and field reads across class boundaries,
      per existing class changed (§4.2c's calls across the encapsulation), at the same change size and point in the
      stream, the rate ratio above 1 (forced is not in this model: the instruction changes what
      is forced).
    Each one-sided with a 95% cluster-bootstrap interval (§5); p is the larger of the two.
    Conditions: compliance, below, and the amount within its band. H8 is decided at α = 0.05 on
    its own p: it is read on its own run, after the others, and is not in the Holm family of the
    primary analysis. Below the compliance bar it is descriptive only. In Run D's analysis H1 to
    H7 are descriptive: they are the arms' tests, not this run's.
  - **Run D cannot be run beside Run A** (the author, 22 November 2026: "I can not currently run
    it concurrently so will have to run separately at the end, so will have to accept this"). So
    the contrast holds anything that changed between the two runs, the instruction among them:
    the date, the machine's load, and above all the agent, if the model behind `claude-opus-5-5`
    is not the same snapshot by then (§7). The harness commit and the model id Run D ran with are
    recorded with its run ids; a different model id is reported as a second difference between
    the runs, and H8 is then read as that.
  Its other predicted directions are fixed now too, each against Run A's `angular-spring`, each
  reported with a stated direction:
  - *Compliance, a condition of reading it:* at least 90% of the members its units introduce are
    not private (§4.2f, measure 1). Below that, the instruction did not take and Run D is
    reported descriptively, not read against Run A.
  - *The force is absent:* the share of growth of existing classes arriving forced (§4.2b) near
    0, and H1's choice of class not narrowing (the alternatives' ratio not below 1).
  - *Concentration weaker:* H2's core draws less at the class (a lower rate ratio), since code
    that needs a class's data may now go elsewhere.
  - *Dispersion stronger:* more calls and field reads across class boundaries per unit (§4.2c's
    calls across the encapsulation, now unforced) and a wider spread (H7's measure), at the same change size.
  - *The amount conserved:* Run D's amount added within 0.8 to 1.25 of Run A's (§4.6's band); the
    code is placed differently, not made more or less.
  - *The reader* (§4.2f): whether classes grow larger without encapsulation, reported without a
    direction.
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
held fixed. Corpus B is therefore read only as a check on the **direction of H3 and H2**; H6,
H4 and the junction × arm reading are not read there.

**Extended 18 November 2026** (§9; drafted that day and built the same day, *As built* below). H3 and H2 as they now stand need only
a history, so more can be read here than the first draft allowed:

- **H3**, over all additions and within a class and a method. There are no checkpoints, so the
  index is the commit's place in the order of the repository's commits read, from 0 to 1.
- **H2**, at the class and at the method. With no stream to declare which later changes are meant
  to touch an earlier one, every later arrival counts.
- **Where bound and unbound code lands** (§5), as on corpus A.
- **H6, weaker.** The problem cannot be held fixed, so each shape measure is read with only the
  addition's size, the place's size, the bindings and the bystanders held fixed. Reported, and not
  called H6.
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
- **H7 is read on corpora B and C** as H1 is (20 November 2026): a unit is a commit, its
  pairs' coupling and the calls across a class's boundary read on the same running index. (H5
  was too until its restatement of 24 November 2026; it now compares arms solving the same
  problems and is not read on a history.)
- **H1 is read on corpora B and C too** (decided by the author, 19 November 2026). Its places
  need the whole tree, so one index is kept running through a history: the whole production tree
  before the first unit, then, before each later unit, the files that differ between the previous
  unit's parent and this one's (merges and commits that are not units included, as a diff of
  trees), so the index is the tree at each unit's parent (`chain.tree_places`). H1 there is read
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

Added 18 November 2026 (§9; drafted that day and built the same day, §3.2 *As built*). Corpus A is written by one agent on a fixed
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
- H3 and H2 are read on corpus C as on corpus B, on all its commits, with the share that is
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

### 4.2a Choice (H1): the other places that could have held the code

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
fields; `--places`, the places of a tree), `tables.choice`, `prepare.h1_rows` (`h1.csv`).

### 4.2b Spread (H7): the classes a change has to go into

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
- **Growth by lever** (reported; decided by the author on 22 November 2026, §2 *An injected
  private field forces too*, §9 row 72): the forced growth of existing classes, per arm, by
  whether the lever of injection was there. *Own:* the placement was bound to a private field of
  the class's own state, a private constant or a private method; nothing outside can reach it.
  *Injected only:* every private member it was bound to is a field holding an injected dependency
  (§4.3), which another class could declare too; split into those where another class already
  holds those dependencies (H1's alternatives at least one) and those where none does yet. The
  injected-only share is the opportunity dependency injection gives to duplicate the core; it
  stays forced, because the lever was not used. As built: `tables.lever` (`forced_lever` on each
  host), `prepare.growth_by_lever`; `MEASURE_VERSION` 29, `HISTORY_VERSION` 13.
- **Coupling accounting** (reported): per unit, the calls between classes in the whole tree after
  it less before it (`tables.coupling_rows`); summed per arm, with the share added in units with
  a forced placement, and the share added between the pairs of existing classes the unit changed
  together (in forced units and in the others).

As built: `tables.pair_rows` (`pairs.csv` per chain or repository), `tables.coupling_rows`
(`coupling.csv`), `prepare.h7_rows` (`h7.csv`), `prepare.pair_rows`, `prepare.co_change`,
`prepare.growth_accounting`, `prepare.coupling_accounting`.

### 4.2c Links (H5), and coupling across the encapsulation

**Links between blocks of logic** (H5's measure since 24 November 2026, §9 row 89). Per checkpoint,
the links it added and lost, each weighed by the data it carries (the weights below, since row 95;
the plain count, each link once however heavy, reported beside):

- **Call links:** a method to a method it calls, followed as in §4.2a, in its own class or another,
  not to itself; a call that may reach several overrides is a link to each. A method is its class
  and signature, so a moved or renamed method's links count as new.
- **State links:** a method to a field holding state that it uses, of its own class (a bare name
  that is a field of the class and not a parameter or local of the method, or `this.x`) or of
  another class (the field reads below). A field holds state when it is not an injected
  dependency (as §4.3 finds them) and not a utility (a logger); a record's components hold state.
  **A constant** (static and final) **is a state link too** (decided by the author on 25 November
  2026, §9 row 109; until then left out): its uses are counted apart (`constant`) and in the
  total, and the test without them is reported beside.
- **Flow links:** in the function arm's wiring, an edge from one function to the next (`next:`, an
  entry of `outputs:`, as §4.5 counts edges), once for each pair of nodes in a file.
- **Not links:** an injected dependency, in either arm: a field the Spring container fills, a
  parameter OfficeFloor injects. It is held or declared, not reached along the control flow. A
  call made *on* an injected object is a call link (confirmed by the author, 24 November 2026, §9
  row 96): injection removes the finding of the target, not the call.
- **The volume** beside them: the logic the checkpoint added (§4.9). Java links compare the tree
  before the checkpoint with the tree before the next, as the calls below; the wiring compares
  the checkpoint's parent with its commit. The last checkpoint has no tree after it and no row.
- Reported beside: each kind apart, the links lost, and the tree's links per method at the end.
- *By caller* (a reported reading, 24 November 2026, §9 row 94): the call links added from a wired
  function (a public method of a class the wiring declares) and from any other method, and those
  within the caller's class and across classes. It shows whether the function arm's calls come from
  its functions or from the helper methods written beside them.

- **The weights** (since 24 November 2026, §9 row 95; H5 is read on them): a call link 1, plus 1
  for each parameter the callee takes and 1 if it returns a value (`Pull --places`, `returns`,
  VERSION 18); a state link 1, a constant's use among them; a flow link 1, plus 1 if it carries a value: a `next:` from a
  function whose method returns one, or an output whose `@Flow` interface's method takes an
  argument (`flows`, VERSION 18; the interface read in the function's own file). An edge whose
  function or flow interface is not found there weighs 1, and **the number of such edges is
  reported** beside the weights (decided by the author on 25 November 2026, §9 row 99): a weight
  missed this way would favour the function arm unseen. The function is the node's `method:`, or else its class's first public method. A
  link lost weighs as it did before it was lost.

*What it cannot say.* How often a link runs is not read. A parameter weighs 1 whatever it holds.
A call whose receiver cannot be read without a symbol solver is not
followed (§4.8), in either arm. A constant reached by a static import, with no class named, is
not followed. A use of a field through a getter is a call link, not a state
link, so a class that wraps its fields in accessors moves links from one kind to the other
without changing their number.

As built: `instrument/Pull.java` (`own`, `state`, `constants`, VERSION 17), `chain.parse_wiring` (`links`),
`flow.Graph.links`, `tables.link_rows` (`links.csv`), `prepare.h5_rows` (`h5.csv`),
`prepare.links_summary`, `analyse.R` (`H5`), `verdict.h5`, `report.h5_section`; `MEASURE_VERSION`
34, 41 with constants (row 109). Corpus A only: a history's logic is not read (§4.9).

**Calls across the encapsulation** (H8's dispersion; also read by the ripple, surface against
volume, the reader and where forced coupling came from. It was the measure of *forced changes couple* until that
hypothesis was deleted on 24 November 2026, §9 row 90). Added 20 November
2026 (§9). Per unit and class that existed before it that the unit placed or edited code in:

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
`flow.Graph.access`, `tables.encapsulation_rows` (`encapsulation.csv`), `prepare.calls_across_rows`
(`calls_across.csv`; `h5.csv` until 24 November 2026).

**Where forced coupling came from (reported reading; added 23 November 2026, §9 row 88).** The
author's reading of *forced changes couple* (since deleted) on the development histories: well-encapsulated code that is forced into a
class adds little coupling, and what it adds comes from the problem, not the placement. Each
class a forced change went into is *contained* (no call added across its boundary), *problem or
reuse* (every call it added either joins two classes whose private data the change needed, both
forced in the unit, or reaches a member that was already open), or *other* (some call reaches a
member the change opened, in a class whose data it did not need). The calls are counted once each
by the same three sources, for unforced changes beside (whose problem share is nil by definition).
No direction is stated and no verdict depends on it. The author's account of *other*, given before
it was built: "it's likely coupling to the other class for utility functions, so not interested in
the data". Seen on building it (§6): on the Spring pilot chain the *other* calls are accessors of
data the change added to a domain class, mapper and utility methods, and calls into new exception
classes. As built: `prepare.call_source`, `prepare.coupling_source` (`readings.json`,
`coupling_source`), `report.h5_section`, from the calls of `edges.csv`; no table changes.

*Prior work:* access excessiveness and its evolution are measured per member (Kobori et al. 2015,
across releases; Vidal et al. 2016, over-exposed methods and classes, mostly from their first
version), with no link to the change that widened them. These calls read widening at the change, and only
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
- **Ripple:** for each call a unit added across a class's boundary (§4.2c), the later units
  that change the method it reaches, and the share of those that also change the calling class:
  the cost of dispersion paid again later. Against chance (decided by the author, 20 November
  2026): the share of the chain's units that change the calling class anyway, so that a ripple
  ratio above 1 is beyond two classes that both change often. Per arm, by whether the call came with a forced change
  and whether it reached a member already open or one the unit exposed or widened.

As built: `tables.boundary_rows` (`boundary.csv`), `tables.edge_rows` (`edges.csv`),
`prepare.surface_rows` (`surface.csv`), `prepare.ripple`, `analyse.R` (`surface`),
`report.surface_section`.

### 4.2f Encapsulation and the reader (reported reading)

Added 22 November 2026 (§9 row 69; the author's question, the operational form the drafter's;
built the same day). Read on corpora B and C (§3.2, §3.3), where the author varies; on corpus
A the author is one agent and every system is small, so it is reported there per arm only.

- **The author of a unit.** *Agent:* a declared agent commit of corpus C (§3.3, the sampler's
  signatures). *Human:* a commit of corpus B (before 29 June 2021). Corpus C's other commits
  (undeclared, of unknown origin) are a third group, reported, never pooled with either.
- **Four measures per unit**, each already computed or computable from the instrument's tables
  (`Pull.java` VERSION 15 reports each field's and method's access):
  1. *Encapsulation made:* of the fields and methods the unit introduces into classes, the share
     that is private (a private constant among them, §2 *Forced*).
  2. *Growth arriving forced:* of the positions the unit adds to classes that existed, the share
     forced at the class (H7's growth accounting, §4.2b).
  3. *Encapsulation opened:* per class row the unit changed, the members it exposed or widened
     (§4.2c), forced and unforced apart.
  4. *Size let reach:* the methods (and positions) of each existing class the unit adds code to,
     at the unit's parent; and whether the unit splits a class (a new class taking fields and
     methods from one that existed, as RefactoringMiner's Extract Class is read, §4.1).
- **The system against a context window.** The size of the system at the unit's parent: the
  tokens of its production Java (the amount's tokens, §4.6). Read continuously, as log(tokens),
  and split at two fixed sizes, **200,000 and 1,000,000 tokens** (drafter's choice: the context
  windows common among coding agents when this was written; an agent's own window is not
  recorded in a commit, so the split is of the system, not of the agent).
- **The question asked of them:** whether agent and human units differ on each measure, at the
  same system size and change size, and whether the difference changes with the system's size
  (the author × log(tokens) interaction). The author's prediction is in §2.

As built (22 November 2026): the system's tokens per file in the tree index
(`chain.java_tokens`, a lexer's approximation: comments dropped, a literal one token);
`tables.member_rows` (`members.csv`: introduced members and their access, the system's files,
classes, methods and tokens before each unit; `MEASURE_VERSION` 27, `HISTORY_VERSION` 11);
`prepare.reader_rows` (`reader_units.csv`, `reader_classes.csv`) and `prepare.reader_summary`
(per author group and band, in `readings.json`); the models in `analyse.R` (`reported$reader`,
on a history only); `report.reader_section`. The R self-test recovers a simulated author effect,
its narrowing with size and two nulls.

### 4.2g A filled ball or pebbles (reported reading)

Added 25 November 2026 (§9 row 98; the author's question: "need to determine if dealing with a
filled ball or is it full of smaller pebbles"). The blocks of logic are the methods; a
**container** holds them: every class, and in the function arm also each wiring flow file (the
classes it wires, its functions and the methods beside them), since OfficeFloor's function is
usually a class of one method and its request flow is the nearer match to a Spring class. Per
checkpoint, in the tree before it, per container:

- **Blocks:** its methods. **Volume:** the positions of their bodies (§4.1). The share of the
  volume in its largest block, and the blocks' Gini.
- **Internal links:** calls between its own blocks, their uses of its own fields holding state
  (§4.2c), and for a flow its wiring edges; **external** call links, in and out.
- **Concentration:** a class code had been forced into (H1's forced placement at the class) at or
  before the checkpoint; a flow whose classes include one. Reported apart from the rest, and with it.

Reported per arm and kind of container, for the concentrations, the rest and all: at each chain's
last checkpoint the mean blocks, volume a block, largest block's share and internal links a block;
and the **growth exponent**, log(blocks) on log(volume) within each container over the stream
(each container's own mean taken out, pooled), with a 95% interval over containers resampled
(1,000, seed 20261116). Near 1, a container grows by adding blocks of about the same size:
**pebbles**, joined by internal links. Near 0, it grows by swelling the blocks it has: **a filled
ball**, whose cost the shape literature sees (H6). **No direction is stated** (the author: "no
expectation"); it enters no verdict.

As built: `tables.container_rows` (`containers.csv`), `prepare.container_summary`
(`readings.json`, `containers`), `report.containers_section`; `MEASURE_VERSION` 37; a flow is named
by its wiring file since `MEASURE_VERSION` 39 (§9 row 103). Corpus A only.

### 4.2h The cost to fix a concentration (deleted)

H9's measure, the cheapest split of a container (stated and built 25 November 2026, §9 rows 104 and
105), was deleted with H9 later the same day (row 108; §2). Its code is removed.

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

- **The primary measure keeps them:** an injected field is a class binding, and H2, H3, H4 and H6 (H1 to H4 as first registered)
  are read on all bindings.
- **Reported beside it** (§5): H3, at method level and at class level, H4 and H2, each with the
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
methods forced at 1, H2 is tested on the binding count, with the cut as a reading aid. H3 and H4 are
read on the bystanders (§4.3a). The binding-based readings of H3 as first registered (at method level
in both arms, and at class level in Spring: class bindings against the class's size) are reported.

### 4.3a Bystanders (H3, H2, H4), the measure of what gravity gathers

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
  stands and is one of H6's shape measures (§4.7a); the bystanders are what one addition found
  there, and what later additions then use is H2's outcome. A class can have many bystanders for
  every addition and yet a low LCOM*, if its methods share a few fields among many; and H6 is
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
received 26 problems, and all of Spring's intrusions were in methods holding several problems). *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `problem_hosts`; §9 row 112.)* The
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
- **H2** is read at the class and at the method, and needs both (below, *Core and periphery*). **H6** is read at the method, since S1 to S4 are measures of the method; the same block at
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
  value or does a necessary bound piece of work, so a call to one is a core value), **of those
  only the private ones** (decided by the author, 22 November 2026, §2: the force is not being
  able to reach outside the encapsulation). A member the code used that other classes can reach
  (package, protected, public) is periphery. Access is read from the tree before the unit
  (`tables.private_members`, as *forced* is); a class not in that tree has no core. Reported: the
  core with every member the code was bound to, as until 22 November 2026.
- **The periphery:** the rest of the data the place held once *p*'s code was in it: what stood by
  (§4.3a) and what *p* introduced (§4.3b); at the class also the class's methods *p*'s code did not
  call and those its checkpoint added (so that core and periphery are alike in kind; H3's
  bystanders stay fields only), and the members it was bound to that others can reach.
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

### 4.7 Shape (the competitors of H6)

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
it (length, complexity, the god class's concentration), and are H6's block. S2 and S3 are **sinew
measures**: whether the data flowing through a method stops it being split, and whether it hands
on more data than it receives. They are the author's own, from SinewSlim and the flow-injection
draft, and nothing in the reviewed literature studies them as shape (`LITERATURE.md`; the nearest
relatives are fan-out and Henry and Kafura's information flow, which count flow between modules).
They describe data, which is this study's subject, so they are read apart from H6 with their own
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

Added 17 November 2026 (§9), to be looked at on the development chain before any of them joins H6.
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

### 4.8 The instrument against the compiler (reported)

Added 22 November 2026 (§9 row 79; decided by the author after a review of the plan). The
instrument reads names with no symbol solver (§7, *Lexical names*), and its fixtures are examples
written with the answers in mind: they show it does what was meant, not that it is right on real
code. Corpus A's code compiles, and a compiler does resolve every name. So on a sample of each
chain's checkpoints, **every fifth and the last**, the tree is given to javac
(`instrument/Check.java`, the JDK's own compiler API), and the two readings are set side by side:

- **Calls** (H1's control flow, H7's coupling of pairs, H5's outcome): per method of the tree
  before the checkpoint, the application's methods it calls, as the instrument follows them
  (`flow.Graph`) and as the compiler resolves them. *Precision:* of the instrument's calls, the
  share the compiler confirms. *Recall:* of the compiler's calls that can be followed (to a method
  with a body in the tree), the share the instrument has. A call is a class and a name; a class
  agrees with the compiler's when it is that class, an ancestor or a descendant of it. Reported
  for all calls and for those that leave the method's class.
- **Field reads** of other classes (H5): the same two shares.
- **Bound names** (the bindings, §4.3): per host of the checkpoint, the names the instrument
  counted as a parameter or local of the method, a field of its class, a method of its class;
  of each kind, the share the compiler agrees is that, in the method after the change. Precision
  only: the instrument counts names on the lines a change added, the compiler reads the method
  whole.
- **Not held against either:** what the compiler itself could not resolve (counted, *unverified*),
  and the compiler's calls to a method with no body in the tree (an interface's).
- **The classpath** is the project's own (`mvn dependency:build-classpath`, offline, on the pom
  beside the production Java at the chain's head). Without it the libraries' types are errors to
  javac, attribution goes on, and more is left unresolved; each row says which it had. Code that
  a build step generates (MapStruct, Lombok) is not in the tree, for either reader.
- **Where read:** corpus A. A history is read light (§3.2), a few files of a tree at a time, which
  does not compile.
- **Reported** per arm (`results/analysis/<analysis>/REPORT.md`), with no pass mark: the shares
  are how far the ruler can be trusted, for a reader to weigh.
- **A tripwire, not a pass mark** (decided by the author on 23 November 2026, §9 row 86). Where a
  share of calls (precision or recall, of all calls or of those leaving the class) is below
  **0.90** in an arm, or differs between the arms by more than **0.05**, the report says so at
  the check and at H5, whose outcome is those calls: *read with care*. Nothing fails by it and no
  verdict changes. The difference between the arms is the one that matters most: an instrument
  that reads one arm better than the other tilts every contrast of the arms. The two figures are
  the drafter's, proposed after the development chain had been seen at about 0.985 and 0.97, and
  rest on nothing but judgement; they were set so that the plan says beforehand what is done if
  a run comes back much worse, not so as to be passed.

**A fault it found, before any run was read** (22 November 2026, §9 row 80). §4.2a says a call
goes to the methods of that name "in that class, what it extends or implements, and what extends
or implements it". As built, the two directions were followed together, so a class reached every
class that shared any ancestor with it, a library's interface among them: on the pilot's Spring
chain every repository was one family of 37 classes, and a call to one repository's `findById`
was counted as a call to all the others'. On the tree before checkpoint 40 of each development
chain, of the calls the instrument counted between classes, the compiler confirmed 329 of 676
(Spring) and 283 of 678 (OfficeFloor). With a call's family corrected to its ancestors and
descendants (`flow.Graph.family`): 329 of 333 and 283 of 288, and of the compiler's calls between
classes that can be followed the instrument has 295 of 304 and 245 of 248. Every figure of §6 for
H1 at the method, H7's coupling of pairs and *forced changes couple* (since deleted) was computed with the fault and is superseded by
the rerun at `MEASURE_VERSION` 29.

**A gap it found, closed before any run was read** (23 November 2026, §9 row 87). Field reads of
other classes were poorly recalled on the development chain (7 of 19 and none of 12, §6). The
one behind it: a nested class using a member of a class around it. The instrument read a field
of another class only where the code named its holder through a typed value or a class's name,
and took a call with no receiver, or on `this`, for a call to the method's own class. So it
missed, from a nested class, `Outer.this.field` and `Outer.this.method()` (the case on the
development chain, in code both conversions began with), and a field or a method of an
enclosing class used by its bare name. Since `Pull.java` VERSION 16 a bare name that is not the
callable's own, nor a member of its own class, and that an enclosing class declares, is that
class's; `Outer.this` names it outright. A method of that name inherited by the nested class is
the one Java would call and cannot be told from the text; the check shows how often that goes
wrong on corpus A. The bindings are unchanged: a nested class is a class of its own (§4.4), so
a field of the class around it is not one of its own fields, and using it is coupling between
two classes (H5), not a binding. It was closed although small on corpus A (one line), because
people's Java of before 2021, corpus B, is full of inner classes that use the class around them
(listeners, iterators, builders, callbacks), and corpus B is where the compiler cannot check.
The compiler's reader was corrected with it: it had taken a bare name of an enclosing class's
field for the method's own.

As built: `instrument/Check.java`, `placement_gravity/validate.py`, `tests/test_validate.py`;
`validation.csv` per chain (step 3), summed per arm in `readings.json` (`validation`).

### 4.9 Logic and organisation (reported reading)

Added 22 November 2026 (§9 row 81; the author's claim, §1 *Essence and accident*; the
operational form the drafter's). What each checkpoint added, per chain, in parts:

- **Logic:** the positions it added to method bodies that are neither moved code nor
  organisation (the runs of §4.3).
- **Organisation in bodies:** the positions the instrument reads as organisation: a plain
  accessor's one statement, a constructor's assignment of a parameter to a field (§4.3).
- **Declarations:** the code lines it added to production Java outside method bodies:
  signatures, field declarations, class headers, annotations. Read as a remainder: the lines the
  agent's commit adds (`git diff`; not blank, not only brackets and punctuation, not only a
  comment, not `import` or `package` lines) less the positions added in bodies, moved code among
  them, and not below nought.
- **Imports:** its added `import` and `package` lines, apart, since they follow the tools.
- **Wiring:** the lines it added to the OfficeFloor configuration (not blank, not only a
  comment). The function arm's sequence of functions lives here, so this is its organisation.
- **State handed along:** the parameters of the **called methods** it created (new methods that
  are not wired functions and hold logic: not a plain accessor, not a constructor that only
  assigns); the values callers pass new methods (birth bindings, §4.3); the parameters and
  locals it introduced and the fields it left in classes that existed (§4.3b).
- **Where the logic landed** (added 22 November 2026, §9 row 85): the logic it added to methods
  that existed, to new called methods, and to new wired functions; with the number of each, and
  of existing methods it added logic to. On the development chain the function arm stopped
  writing new functions as the stream went on and wrote called methods and edited existing ones
  as the methods arm does (§6), so that by the last third the arms looked alike. Whether that is
  the petclinic stream (its later checkpoints change earlier rules on one endpoint), the agent
  falling back on the Java it knows best (§7), or the form helping only while there are new
  steps to add, one chain cannot say. No direction is stated. It bears on H4: if the function
  arm drifts towards the methods arm's way of working, the arms' differences narrow over the
  stream, and H4's terms are read with these beside them.
- **Declared, not handed along** (apart since row 83): the parameters of the **wired functions**
  it created. The framework injects them; no caller passes them, and nothing has to be placed
  near anything for them to arrive. The author: "the method signatures are just declarations of
  logic, not the placement organisation required in Spring." The parameters of all new methods
  together, as first built, are reported beside.

**Stated now, before any run named for analysis is read:**

- *The essential part is conserved:* the logic added per checkpoint is the same in both arms, the
  function arm's ratio inside 0.8 to 1.25 (the two one-sided tests, 90% interval).
- *The state handed along is the methods arm's:* the parameters of new called methods, and the
  values callers pass new methods, are fewer in the function arm (ratio below 1) and rise less
  over the stream (the arm's interaction with the checkpoint index below 1). (As first stated,
  hours earlier: the parameters of *all* new methods. On the development chain that went against
  the direction, 1.38 [1.06, 1.78], every part of the excess being the injected parameters of
  wired functions, §6. They were taken apart after that was seen, row 83.)
- *No direction is stated for declarations, wiring or the wired functions' injected parameters.* OfficeFloor makes each function a class,
  so it may add more declaration lines than Spring; that is the cost of its form and is to be
  seen, not summed away. Organisation in all (bodies, declarations and wiring together) is
  reported with its ratio and each arm's share of logic and organisation together.

Each part is a negative binomial mixed model on the arm (and the front end) with the chain's and
the checkpoint's intercepts, Wald intervals; the trend is the arm's interaction with the
checkpoint index centred at the middle of the stream and scaled to the stream's length.
Reported, with stated directions; it enters no verdict. Corpus A only: a history's diff is not
read this way, and there are no arms that solve the same problems.

*What it cannot say.* Lines are a crude measure of organisation: a signature of five parameters
and one of none are one line each, which is why the parameters are counted beside the lines.
Positions and lines are not the same unit, so the remainder that gives the declarations is
approximate. A statement whose only work is to pass values on to another method is logic to the
instrument; the junction (§4.7) is the measure nearest to it and is read with the sinew measures.

As built: `chain.lines_added`, `tables.organisation_split`, `prepare.split_rows`,
`prepare.split_summary` (`split.csv`, `readings.json`), `analyse.R` (`reported$split`),
`report.split_section`; `MEASURE_VERSION` 30, 31 with rows 82 and 83, and 32 with row 85.

## 5. Analysis

- **Unit:** an addition run (Q2, H3, H4) or a problem and host whose code was bound there (Q3, H2,
  H6, H4), nested in checkpoints nested in chains.
- **The problem is held fixed by its identity** (revised before the start, 16 November 2026, §9).
  Every checkpoint is one problem, solved once by every chain of both arms. Every model
  therefore carries a **random intercept for the checkpoint**, crossed with the chain's. A
  comparison is then between placements of the same problem, and the size and the declared
  crossings are no longer the only stand-ins for it. A model that does not converge with the
  checkpoint intercept is refitted without it, and the report says so.
- **H3** (restated 17 November 2026, §9): a mixed model of log(1 + bystanders) per run of added
  logic that needs a pre-existing value (§4.3a), on the checkpoint index, in the methods arm, with random intercepts for the chain and the
  checkpoint. The slope is reported with a 95% bootstrap interval over chains. Host size is not in
  the model: a larger method has more values by construction, so a slope on it would not be
  evidence.
  - **Within a place** (17 November 2026, §9): the same model twice more. On the class's
    bystanders, with the checkpoint index split into the mean checkpoint of the runs in that class
    (of that chain) and the run's difference from it; and on the method's bystanders, the same
    within the method. The slope read is the one on the difference: how much more stands by for a
    later run than for an earlier one in the same place. A class or method with runs at only one
    checkpoint adds nothing to it. H3 is supported when all three slopes have a 95% bootstrap
    interval above 0.
  - **Reported beside it:** the same model on method bystanders and on class bystanders, without
    injected dependencies, and without constants; the slopes within a place in the function arm;
    and H3 as first registered, log(1 + bindings) on
    log(host positions) and the checkpoint index, on runs into existing methods.
- **The base model of H2 and H6:** a negative binomial model, per problem and host whose code was
  bound there (§4.4), of later intrusion (H6, H4), of the later intrusions' uses of the core and
  of the periphery (H2), or of the later intrusions bound to what stood by (H2 as it stood). It holds the problem fixed: the checkpoint's intercept, the addition's size, its declared
  crossings, host size, whether the host is new, and act. A new host has almost no bindings and a
  different later life from an existing one (on the development chain, Spring's new hosts averaged
  0.31 bindings and existing ones 1.81), so without the new-host term that contrast alone could carry
  a difference. Host size also stands for the plain fact that a longer method has more values in it. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `problem_hosts`; §9 row 112.)*
- **H2** (restated 19 November 2026, §9): in the methods arm, at the **class** (its fields) and at
  the **method** (its values), each bound problem and host gives up to two records (§4.4): one
  for its core and one for its periphery, where it has at least one value of that kind. The
  outcome is the later intrusions' uses of the values of that kind; the offset is the log of the
  later checkpoints plus the log of the number of values of that kind, so the model is of uses
  per value; the term is whether the record is the core's, added to the base model. It is
  supported when the incidence rate ratio of the core to the periphery has a 95% interval above 1
  at both levels, and the arm contrast below holds.
  - **The arm contrast** (22 November 2026, §9 row 77): the core's records of both arms, in the
    base model with the arm term, the outcome and offset as above (uses per core value and later
    checkpoint). The function arm's rate ratio has to have a 95% cluster-bootstrap interval below
    1, at each level where each arm has at least 10 core records. Where the function arm has the
    records and none of its core values is ever come back to, no ratio can be fitted (it is
    nought): the arms' chains are then compared by a one-sided rank-sum test on each chain's uses
    per core value and later checkpoint, and that is recorded. H2's p is the largest of its
    parts: the two ratios of core to periphery and the arm contrasts that are needed.
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
- **H6** (its measures and levels set 18 November 2026, §9): six measures, each fitted **alone**,
  as *The literature's measures, each alone* below describes. At the **method**, on existing
  hosts: long, cognitive complexity and cyclomatic complexity, added to the base model with the
  bindings and the method's bystanders, on intrusion at the method. At the **class**, one row per
  class and checkpoint with the class's size held fixed: the Gini of the class's positions, WMC
  and LCOM*, on intrusion at the class. They are fitted one at a time because they are rival
  readings of the same thing (the two complexities; weight and concentration), and together could
  not be told apart; so H6 says of each that it does not draw code in, not that each adds nothing
  beyond the others. The block as first registered (S1, S4 and S5 together in one model at the
  method) is reported.
  - **The method level is the test** (decided by the author, 18 November 2026): it is where the
    arms are compared, since a function is OfficeFloor's unit of placement.
  - **The class measures are tested only where classes can be told apart** (18 November 2026,
    §9). They enter H6 in an analysis only when later bound arrivals fall in **at least 10
    distinct classes** (a class counted by its name over all chains) and **no one class holds
    more than half** of them. Otherwise they are reported, each alone, and H6 is read on the
    method measures. The petclinic stream sends every rule through one endpoint, so one class
    there receives nearly all the arrivals and a class measure describes that class over time,
    not a difference between classes (§6); the ui stream, with many endpoints, is where the class
    level is expected to be testable. H6 is supported when every shape measure's incidence rate ratio
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
    margin, and H6 is read on the measures that remain.
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
    the value for ratios and the index), or present against absent. Read as H6 is, against the
    upper margin, with the variation rule. They are fitted one at a time because they measure
    overlapping things (cyclomatic, cognitive and NPath complexity; WMC and the God Class), and
    together would not be told apart. **Which of them are H6's** was decided by the author on 18
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
    study's claim, not against H6. The variation rule applies to each as it does to the shape
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
  index in the H3 model, on the paired chains, with the amount band (§4.6) and the two wiring
  conditions (§4.5). The checkpoint index is centred at the middle of the stream, so the arm term
  is the difference between the arms half-way through. Both have to be below 0: the function arm
  has fewer bystanders, and they grow more slowly.
  - **Come back to less** (17 November 2026, §4.4): the arm term of the base model of H2 and H6,
    without the bindings (the arm itself changes them), on intrusion at the class and at the method.
    The function arm's rate ratio has to have a 95% interval below 1 at both levels.
  - **Less well-trodden files gone back into** (22 November 2026, §9 rows 78 and 82): per
    checkpoint and chain, for each file that existed before the checkpoint and that it changed
    (a production Java file it modified, renamed or deleted; a wiring file it changed; `git diff`
    of the agent's commit against its parent; a file the checkpoint adds is not gone back into),
    the number of earlier checkpoints of the chain that had created or changed that file, summed
    over the files. A renamed file keeps its count. The code a chain started from is no
    checkpoint's, so a file's history before the stream is not counted. A negative binomial mixed
    model of that count on the arm (and the front end), with the chain's and the checkpoint's
    intercepts, decided on the cluster bootstrap: the function arm's rate ratio has to have a 95%
    interval below 1. It enters H4's p with the other four. Not read on a history. Reported
    beside it: the plain number of existing files gone back into (a Poisson model), as first
    built. As built: `chain.measure` (`java_changed`, `java_existing`), `tables.trodden`,
    `tables.addition_rows` (`trodden`, `existing_java_files`, `existing_wiring_files`),
    `prepare.reopen_rows`, `analyse.R` (`H4$trodden`, `reported$existing_files`).
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
- **Without injected dependencies** (reported, §4.3): H3 at method and class level, H4 and H2,
  each with bindings to injected dependencies left out. These do not change any verdict.
- **Choice at a checkpoint** (reported; added 16 November 2026, §9). Per checkpoint and arm, over
  the chains: the share of chains that placed any of the addition in an existing host, the number
  of distinct hosts the chains used between them, and the standard deviation of the bindings per
  addition. A checkpoint where every chain made the same placement with the same bindings left no
  choice; one where the chains differ did.
- **Formation** (reported with a stated direction, not confirmatory; added 16 November 2026, §9).
  Read within each arm, never across arms.
  - **Lagged:** the H3 model, with its checkpoint intercept, and one more term: the chain's mean
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
    bound and unbound, and between the arms, not against 0.5. It replaces nothing: H6 stands as it
    is until this has been looked at on the development chain.
- **Corpus B and corpus C** (§3.2, §3.3; extended 18 November 2026, to H1 on 19 November 2026 and to H7 on 20 November 2026): the H3, H2 and H7 models, and H1's reading of choice narrows (since 25 November 2026, row 107), with a
  random intercept for the repository in place of the chain's and the checkpoint's, the index the
  commit's place in the repository's order. Direction and interval only. The two comparisons of
  §3.3 are the same models with a term for the declared agent commit (within a repository) or for
  the corpus (between them), and the destination of unbound code as a binomial model on the same
  term.
- **H1** (restated 25 November 2026, §9 row 107): per checkpoint and chain of corpus A that did
  something, the placements forced at the class, as a negative binomial (nbinom2) mixed model on
  the arm, the checkpoint index centred at the middle of the stream and scaled to its length, and
  their interaction, with the chain's and the checkpoint's intercepts (Poisson where the negative
  binomial cannot be fitted, recorded). The arm term (the function arm's rate half-way through)
  and the interaction both one-sided below 1, from one cluster bootstrap; p the larger; reversed
  if the arm term's interval lies wholly above 1. Not testable on a history. Reported beside it:
  the forced placements a checkpoint per arm, and the methods arm's own rise; and **choice
  narrows** (the test until then, §2): per bound host and level, its alternatives (§4.2a) as a
  negative binomial mixed model on the checkpoint index scaled from 0 to 1, with the chain's
  intercept, in the methods arm (exp(slope) the end of the stream against its start, 95%
  cluster-bootstrap interval), at the class and at the method, with a level where every placement
  was forced reported as such; the reading against the upper margin (1.25, 90% Wald interval), as
  it stood until 22 November 2026; the share forced and the mean alternatives per arm and third;
  the function arm's ratio; the arm × index interaction's arm term; the share of class rows bound
  to the class's own values; the method values of no declared type. On a history choice narrows
  is read with the repository's intercept, as below.
- **H7** (20 November 2026): per unit that placed or edited code in an existing class, its spread
  (§4.2b) as a negative binomial (nbinom2) mixed model on whether the unit was forced and the index
  scaled from 0 to 1, with the chain's intercept, in the methods arm (*forced*: the ratio of the
  spread of a forced unit to one that was not, at the same point in the stream). One-sided
  against the upper margin 1.25, 90% Wald interval, as H6 (21 November 2026, later, §9 row 67):
  *not above* when the interval lies below 1.25, *unresolved* when it reaches above it without
  lying above it, *not supported* when it lies wholly above it; the two-sided reading (0.8 to
  1.25) is reported. (Until then: one-sided above 1, 95% interval.) Reported: the spread on the
  index alone (*rise*: exp(slope), the end of the stream against its start), over all units and in
  forced and in unforced units apart. Every H7 model holds the change's size fixed: log(1 +
  positions it added) and log(1 + methods it placed or edited code in) (20 November 2026, §9 row
  61); the forced ratio without them is reported. A spread
  with less variance than its mean, where the negative binomial cannot be fitted (its Hessian not
  positive definite), is fitted as Poisson, and that is recorded. Reported: the spread per arm and
  third, and against forced; the function arm's forced ratio and rise; the arm × index
  interaction's arm term; the growth and coupling accountings (§4.2b); the
  coupling of pairs changed together more than once, a negative binomial model of it on the index
  with intercepts for the chain and the pair; the pairs changed together, how many more than once,
  in how many of those coupling rose or fell, and the candidates by name.
- **H5** (restated 24 November 2026, §9 row 89; weighed since row 95): per checkpoint and chain of
  corpus A, the weight of the links added (§4.2c) as a negative binomial (nbinom2) mixed model on the arm, the checkpoint index
  centred at the middle of the stream and scaled to its length, their interaction, and log(1 +
  logic added) (§4.9), with the chain's and the checkpoint's intercepts (the chain's alone where
  that does not converge, recorded). The arm term is the function arm's rate ratio half-way through
  the stream for the same logic; the interaction, how that ratio changes from the stream's start to
  its end. Both one-sided below 1, from one 95% cluster bootstrap (below); p is the larger of the
  two; reversed if the arm's interval lies wholly above 1. Reported: each kind of link apart (call,
  state, constant, flow; the flow links have no ratio, the methods arm having none), the same model
  without constants as state links (the test until 25 November 2026, row 109), the links lost, the same
  model without the logic, the methods arm's own rise over the stream, and the links per e-fold of
  logic; per arm, the links a checkpoint by kind and third, the links per position of logic, and
  the tree's links per method at the end.
- **The sinew shape** (reported beside H2, no direction stated; the author's, 25 November 2026, §9
  row 100). On top of each placement's own core: per place that bound code was put in (at the
  class, its fields, a private constant among them as in H2's core and as forced counts it, §2;
  at the method, its parameters and locals), how often each value is used by
  bound code, how often each **combination** of values is used together, and the **effective
  number** of values the uses fall on (the inverse Simpson index: 1 when one value takes every use,
  n when n share them evenly; no threshold is chosen). Reported per arm and level: the mean
  effective number over a place's uses and over each third of its chain's stream (a falling
  number: the sinew tightening onto fewer values), the most used value's share, the share of
  changes repeating a combination already used at that place, and the most used values and
  combinations by name. As built: `readings.sinew_shape`, `readings.effective_number`
  (`readings.json`, `sinew_shape`), `report.sinew_lines`.
- **Encapsulation and the reader** (22 November 2026, §4.2f; reported, not tested; built the
  same day): on corpora B and C, per unit, (1) the private share of introduced members as a binomial
  mixed model, (2) the forced share of positions added to existing classes as a binomial mixed
  model weighted by positions, (3) members exposed or widened per class row and (4) the methods of
  the class code lands in as negative binomial (nbinom2) mixed models; each on the author group
  (agent, human; undeclared reported apart), log(tokens) of the system centred, their
  interaction, and the change's size (log(1 + positions added), log(1 + methods changed)), with
  the repository's intercept. Reported: each contrast with its 95% interval, the interaction, and
  the measures in each of the three size bands (below 200,000 tokens, to 1,000,000, above) per
  author group, with the number of units and repositories in each. A band with fewer than 10
  repositories for an author group is reported as too thin, not fitted. On corpus A: the four
  measures per arm, descriptive.
- **The confirmatory tests are decided on a cluster bootstrap** (decided by the author on 22
  November 2026, after a review of the plan, §9 row 74). Until then only H3 and H4's bystander
  terms were; H2, H4's intrusion ratios, H1 and the coupling test of the time took a Wald interval from a model with the
  chain's intercept. That interval treats the rows of a chain as separate once the chain's level
  is taken out, and they are not: the problems placed in one class share its later changes, the
  two records of one row of H2 share its arrivals (§7), and one class is changed by many units.
  Now, for each of them: chains are resampled with replacement within arm, the same model is
  refitted on each resample (`spec$boot` refits, 1,000, seed 20261116; the resamples are drawn
  first from the one seeded stream and the refits then run on several cores, so the result does
  not depend on how many), the 95% interval is the 2.5th to the 97.5th percentile of the refits,
  and the one-sided p is the share on the wrong side of 1, (k + 1) / (n + 1), as H3's. On a
  history the repository is the chain, and the refits are **200**, not 1,000 (decided by the
  author on 22 November 2026, §9 row 84; the timings below are remade on any machine by
  `./step1b_timing.sh`, row 112). One fit of these models was timed at 2 seconds on
  1,800 rows, 22 to 50 seconds on 15,000 to 30,000 (about a ui analysis), 5.6 minutes on 200,000
  and 37 minutes on 1,000,000 (where corpus B may lie): at 1,000 refits corpus B would take
  weeks. With 200 each end of an interval is located to about a tenth of the interval's
  half-width (a twenty-fifth with 1,000), and the smallest p is 0.005; a result that lies near 1
  may fall either side by the draw, and is to be read as near 1. Corpora B and C are read for
  direction and interval only and decide no hypothesis. The alternative was the Wald interval
  alone, which is cheap and assumes what the bootstrap is there not to assume; it stays beside
  each, and where the two differ, that is how much the assumption was worth. The Wald interval is reported beside each. With one chain
  in an arm (the development chain) a resample is the data again, so the Wald reading is what
  there is; so too if fewer than half the refits can be fitted; either is recorded. H6 and H7,
  whose tests are against a margin on a 90% Wald interval, and every reported reading keep their
  Wald intervals; H3, secondary, has been on the bootstrap since it was registered. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `timing`; §9 row 112.)*
- **Multiplicity** (21 November 2026, §9 rows 66 and 67): the confirmatory family H1, H2, H4 and
  H5, Holm-corrected at α = 0.05 over those of the four that have a p (H1 has none where it is
  not testable, on a history). H8 (Run D, §3.1a) is decided at α = 0.05 on its own p, on its own run. H3, H6 and H7 are secondary (and H9 was, on 25 November 2026, until it was deleted, row 108), each decided at α = 0.05 on its
  own p outside the correction and reported as secondary. (Until 20 November 2026, every
  hypothesis was in one Holm family: four, then five, six and seven; on 21 November 2026 the
  confirmatory family was H2, H4, H1, H7 and H5 until H7 was restated the same day.) All else is
  descriptive.

**As built** (`analysis/analyse.R` with glmmTMB, `placement_gravity/prepare.py` and
`placement_gravity/verdict.py`, 16 November 2026; R chosen by the author for glmmTMB's negative
binomial mixed model). These details are fixed with the code before any run is read:

- **Each analysis is read on its own** (`runs.yaml`): the ui primary, which is the study's test,
  and each petclinic analysis, a replication. An analysis with fewer than 6 chains in an arm is descriptive only.
- **H3 and H4 as first registered, on the bindings** (reported since 17 November 2026; H3 and H4
  themselves are on the bystanders, above) are fitted on runs of added logic into **existing** methods: a new method has no
  prior size, so including new methods would make "more bindings in bigger hosts" true by
  construction. Gaussian mixed models of log(1 + bindings) on log(host positions) and the checkpoint
  index, random intercepts per chain and per checkpoint; H4 adds the arm and its interaction with host
  size, centred (and the front end, where the analysis has more than one). Intervals: a cluster bootstrap, chains resampled
  with replacement within arm and the model refitted, **1,000 refits, seed 20261116**. One-sided
  p-values are the bootstrap share on the wrong side of 0, (k + 1) / (n + 1).
- **H2 and H6** are negative binomial (nbinom2) mixed models of later intrusion per problem and
  host, at the class and at the method (§4.4), offset by log(later checkpoints), random intercepts per chain and per
  checkpoint. Its base terms are log(1 + the problem's positions added), the problem's declared
  crossings (the checkpoints it mutates or crosses), log(1 + host positions), whether the host is
  new, the act (the ui stream only; petclinic has no
  acts), the arm and, where present, the front end. **H2** is read on every bound problem and host of the methods arm,
  with a one-sided test at each level (a Wald test until 22 November 2026; the cluster bootstrap since, above); **H6** on existing hosts with their shape at k − 1, by one
  one-sided Wald test per shape measure against the upper margin (90% intervals; the two one-sided
  tests of the two-sided reading are reported). S4 enters as log(1 + cognitive complexity) and S5
  as the class Gini, both standardised; S1 to S3 as 0/1.
- **The p-value of each hypothesis** for Holm is the larger of its parts: H3, of its three slopes
  (over all runs, within a class, within a method);
  H2, of the class level and the method level and of the arm contrasts that are needed (row 77); H6, of every shape measure's one-sided test; H4, of the arm
  term, the interaction, the arm's rate ratio in intrusion at the class and at the method and its rate ratio in how well-trodden the files gone back into were (rows 78, 82); H7, its forced ratio's; H1 and H5, the larger of the arm term and its interaction (as H4; H1 until 25 November 2026 also its class level's fall, row 107). A hypothesis is
  supported when its p (Holm-adjusted over the confirmatory four; its own for a secondary one) is at most 0.05 **and** its conditions hold (H4: the amount in its band and neither wiring
  condition against). The verdicts are supported, not supported, reversed (an interval wholly on
  the wrong side), unresolved (H6 and H7: an interval reaching above the upper margin), not testable (H6: no
  shape measure varies; H1 and H5: a history) or descriptive only.
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
- **The bystanders** (§4.3a) and H3 and H4 as restated on 17 November 2026 are built: the visible
  and needed values per run and the fields a class is left with (`instrument/Pull.java`,
  `tests/test_bystanders.py`); `by.csv` and `capture.csv` (`prepare.py`); the models
  (`analysis/analyse.R`, whose self-test simulates bystanders rising in one arm and recovers H3,
  H4, the equal needs and capture); the verdicts (`verdict.py`: H3 on its one slope).
  - *Visible:* a local is visible where a run starts when it is declared on an earlier line and its
    nearest enclosing block, loop, try, switch entry or lambda encloses that line.
  - *H4's centre* is the middle of the stream, (checkpoints + 1) / 2.
  - *Capture* is a Gaussian mixed model of the share on log(1 + the heaviest class's fields), per
    arm, with Wald intervals.
- **H3 within a place and H2 as restated** (17 November 2026, §9) are built: what stood by per
  host and the later intrusions bound to it (`tables.standing`, `tables.outcome_rows`,
  `tests/test_stream.py`); the class and method each run is in (`prepare.by_rows`); the models
  (`analysis/analyse.R`, whose self-test simulates both and recovers them); the verdicts
  (`verdict.py`: H3 on its three slopes, H2 on the bystanders' rate ratio at both levels).
  - *H3 within a place* has the same bootstrap as H3 (chains resampled, 1,000 refits); a place is a
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

*The hypotheses here keep the numbers that stood when each entry was written; §9 has the table to today's (row 93).*

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
  conventional reading that replaced it. That reading is descriptive, of development data. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `junctions`; §9 row 112.)*
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
  settled at registration. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `injected_runs`; §9 row 112.)*
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
  readings. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `problem_hosts`; §9 row 112.)*
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
  intercept. Nothing in the plan was changed after these were seen. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `problem_hosts`; §9 row 112.)*
- **Bystanders on the development chain** (17 November 2026; a scratch copy of the instrument, one
  chain per arm). **H1 and H4 were restated after these were seen**, so on this chain they are
  not predictions; the chain is excluded from every registered analysis. Fields were counted
  without telling constants apart. Seen:
  - runs into existing methods need the same in both arms (1.43 values in Spring, 1.41 in
    OfficeFloor) and have 11.9 bystanders in Spring against 1.4 in OfficeFloor; *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `bystanders`; §9 row 112.)*
  - over the thirds of the stream Spring's bystanders are 7.2, 11.1 and 14.9, OfficeFloor's 1.7,
    1.0 and 1.4; over every run, new hosts included, 4.2, 7.8 and 11.5 against 1.6, 2.4 and 2.8; *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `bystanders`; §9 row 112.)*
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
  after seeing this**, each on its own argument, recorded there. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `bystanders`; §9 row 112.)*
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
    reopening count by the arm's rate ratio in intrusion, were decided after seeing this.** *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `problem_hosts`; §9 row 112.)*
  - *With the binding rule:* 89 of Spring's 174 problem and host rows and 31 of OfficeFloor's 192 are
    bound and followed. Per bound row: 11.9 later bound arrivals at the class against 0.84, 3.3
    against 0.10 at the method. H2's rate ratio per binding 0.89 [0.75, 1.06] at the class and 0.85
    [0.61, 1.20] at the method: below 1, not the direction predicted. H3 at the method: the
    junction 0.84 [0.35, 2.00], cognitive complexity 0.36 [0.22, 0.60], the class Gini 0.71
    [0.43, 1.17], so against (complexity lies wholly below the margin). H4: the arm's rate ratio in
    intrusion 0.16 [0.10, 0.27] at the class and 0.11 [0.03, 0.43] at the method. Reopening,
    reported: bound classes 0.26 [0.15, 0.48]; with the wiring files 0.77 [0.52, 1.16].
  Nothing in the plan was changed after the figures with the binding rule were seen. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `problem_hosts`; §9 row 112.)*
- **H2 as restated, on the development chain** (17 November 2026; one chain per arm, descriptive
  only). **H2 was restated, and H1 extended, by the author before any of this was computed; the
  operational form of §4.4 and §5 was written after the first look below**, so on this chain
  neither is a prediction.
  - *A first look, in scratch:* in Spring's controller class the fields standing by rose from 4 to
    16 over 41 bound arrivals, and in its `addOwner` method the values standing by from 0 to 13 over
    25; of later bound arrivals 44% at the class and 16% at the method used something that had stood
    by; OfficeFloor had 40 later arrivals at the class in all, 3 of them such. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `bystanders`; §9 row 112.)*
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
  these were seen. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `size_or_data_by_arm`; §9 row 112.)*
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
  above it, so on this chain H3 would be unresolved, not supported. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `busiest_method`; §9 row 112.)*
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
  above (cognitive 0.32, cyclomatic 0.35). *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `class_rows`; §9 row 112.)*
- **What unbound code leaves behind, on the development chain** (17 November 2026; a scratch look
  per checkpoint, not built). Fields added to classes that existed, per checkpoint: 0.71 in Spring
  and 0.63 in OfficeFloor where the checkpoint has an unbound landing in an existing class,
  against 0.35 and 0.06 where it has none; rank correlation of the fields added with the unbound
  landings in existing classes 0.41 and 0.63, with the bound landings 0.12 and −0.08. Which class
  received the fields was not looked at. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `fields_and_landings`; §9 row 112.)*
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
  the author, no cap. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `repositories`; §9 row 112.)*
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
  read alone, with the same units). *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `repositories`; §9 row 112.)*
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
  the existing ones 288. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `bound_new_methods`; §9 row 112.)*
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
  Nothing in the plan was changed after these were seen. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `bound_new_methods`; §9 row 112.)*
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
  flow reaches it. This is the case §4.2a foresaw (a refinement by control flow); not yet decided. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `alternatives_thirds`; §9 row 112.)*
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
  Nothing in the plan was changed after these were seen. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `alternatives_thirds`, `repositories`; §9 row 112.)*
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
  changes. Led to row 61. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `change_size`; §9 row 112.)*
- **Under forced by encapsulation** (21 November 2026, `MEASURE_VERSION` 26, `HISTORY_VERSION` 10,
  the development chain and the development histories, rows 64-67 built; descriptive only).
  *Pilot:* H2 class 17.5 [11.9, 25.6], method 20.3 [11.8, 34.7]; H3 not above (cognitive 0.32,
  cyclomatic 0.35; the class measures not tested, 5 distinct classes); H4 intrusion ratio class
  0.16, method 0.11; H5 class 0.16 [0.03, 0.92], method 4.6 [1.5, 14.6] (reported); H6 1.03
  [0.45, 2.37] (90%), unresolved, 3.66 without the change's size; H7 2.17 [1.44, 3.27], outward
  3.64, inward not estimable, members opened 0.19. Growth of existing classes forced: Spring
  0.32, OfficeFloor 0.02; calls added in forced units: Spring 0.70 of 69, OfficeFloor −6 of
  199. Split flagged on `OwnerRestControllerV1` (`clinicService` against the household helpers);
  concentrate flagged on `OwnerMapper` with `OwnerRestControllerV1` (7 times together, half the
  same data). Surface against volume across classes 0.80 (OfficeFloor) and 0.82 (Spring).
  *Histories* (two human repositories, 462 units; the agent repository, 8 units, too few): H2
  class 3.15 [2.73, 3.63], method 2.37 [1.90, 2.96]; H3 not above (cognitive 1.10, class Gini
  1.09); H4 intrusion ratio 0.075 and 0.072, but the bystanders' arm term −0.10 [−0.52, 0.31] and
  slope 0.47, against (p 1.0); H5 at the class every placement forced (no injection), method 1.56
  [1.01, 2.42]; **H6 0.845 [0.673, 1.061] (90%), not above** (1.99 without size); **H7 1.13
  [0.82, 1.55]**, not shown (1.65 without size). Growth of existing classes forced: human 0.45,
  agent 0.70; calls added in forced units: human 0.31 of 1,053, agent 0.69 of 178. All of these
  were seen before row 67 was drafted (H6 under encapsulation on both is its evidence); H7 on the
  histories leaves the contrast H6 leans on (force seen at the boundary, not in the spread)
  shown on the development chain only (§8).
- **The development rerun under rows 72 to 80** (22 November 2026, commit `97fc46b`,
  `MEASURE_VERSION` 29, `HISTORY_VERSION` 13; the development chain and the development
  histories, all three repositories read; descriptive only, one chain an arm on the pilot and
  three repositories on the histories). Every rule below was written before these were seen;
  none was changed after.
  - *Pilot.* H1, H3 and H4's bystander terms as before (0.015, 0.026, 0.023; cognitive 0.32,
    cyclomatic 0.35; arm −1.59). **H2** with the private core 18.2 [12.5, 26.5] at the class
    (17.5 with every member in the core), 20.3 at the method; **its arm contrast** at the method
    0.088 [0.024, 0.316] (51 core rows and 185 uses in Spring, 22 and 4 in OfficeFloor); at the
    class not needed, OfficeFloor having 3 core rows (none come back to) against Spring's 41.
    **H4's symmetric count went against it:** existing files gone back into per checkpoint, 2.4
    in OfficeFloor (1.9 Java, 0.5 wiring) against 1.6 in Spring (all Java), ratio 1.50
    [1.16, 1.94]; so OfficeFloor's changes went back into more existing Java files than Spring's
    even before its wiring is counted. Intrusion where bound, as before, 0.16 and 0.11. **H5 as a
    fall** 0.16 [0.02, 1.28] at the class (95% Wald: with one chain an arm there is no bootstrap),
    not shown to fall on this chain; against the old margin, 0.16 [0.03, 0.92]. **H7 with the
    call graph corrected and the class's intercept** 1.44 [0.99, 2.09] (2.17 [1.44, 3.27] before
    both; 1.62 without the change's size; outward 2.57 [1.44, 4.57]). H6 1.03 [0.45, 2.37]. H3
    with the coupling measures put back: against, on the method's fan-out. *Growth by lever:* of
    Spring's growth of existing classes 32% arrived forced; of that, 58% was bound to the class's
    own private members and 42% only to injected private fields, every one of those with another
    class already holding the same dependencies. OfficeFloor 2% forced. The amount added 1.08.
  - *The compiler check on the pilot* (12 checkpoints a chain, all read with the project's
    classpath): calls, precision 0.985 (Spring) and 0.986 (OfficeFloor), recall 0.971 and 0.986;
    calls leaving the class, 0.985 and 0.984, recall 0.964 and 0.984; methods matched between the
    two readers 99.4%. Bound names: every one confirmed (Spring 19 method values, 9 fields, 7
    class methods; OfficeFloor 12, 1 and 2), few because only the sampled checkpoints' hosts are
    checked. **Field reads of other classes are poorly recalled:** 7 of 19 in Spring and none of
    12 in OfficeFloor; the one looked at is a nested class reading a field of the class around
    it, which the instrument does not see, in code both conversions started with (so the same
    miss is counted at every checkpoint). Not corrected; the instrument is unchanged.
  - *Histories* (two repositories of people's code, 896 class rows; the agent repository, 11
    units). H2 2.93 [2.58, 3.19] at the class and 2.37 [2.34, 2.44] at the method; H5 at the
    class every placement forced, so not testable; H6 0.845 [0.673, 1.06]; **H7 0.82
    [0.61, 0.88]**, Wald 0.82 [0.58, 1.15] (1.13 before the correction). The bootstrap there is
    over two repositories, and its intervals are far too narrow to mean anything: with fewer than
    six chains an analysis is descriptive, and that is the reason. Growth of existing classes
    arriving forced: people 45% (all of it the class's own private members: no injection), the
    agent repository 70% (73% of that injected only). The reader models (§4.2f) do not fit on one
    agent repository and their figures are not read.
  - *Step 4 took 20 minutes* for both analyses on four cores, the histories' bootstraps being
    nearly all of it (1,791 rows for H2, 896 for H7).
- **Logic and organisation on the development chain** (22 November 2026, `MEASURE_VERSION` 30,
  §4.9; one chain an arm, descriptive only; its directions were stated before this was run, and
  nothing was changed after). Per checkpoint, OfficeFloor against Spring. *Logic* 9.7 against
  9.1 positions, ratio 1.06 [0.96, 1.17] (90%), inside the margin: **the logic is the same.**
  *Organisation in bodies* 0.58 against 0.56. *Declarations* 8.0 against 6.4 lines, 1.23
  [1.08, 1.40]. *Wiring* 2.2 lines against none (3.1, 2.4, 1.0 over the thirds). *Organisation
  in all* 10.7 against 6.9, 1.51 [1.29, 1.75]; its share of logic and organisation together 52%
  in OfficeFloor and 43% in Spring. *Imports* 4.8 against 0.9 lines. **The state handed along
  went both ways:** the values callers pass new methods 0.07 against 0.20 a checkpoint, 0.33
  [0.11, 0.97], as stated; the parameters of new methods 2.9 against 2.1, 1.38 [1.06, 1.78],
  **against the stated direction**. A wired OfficeFloor function's parameters are injected by
  the framework, not passed by a caller, and they are counted here as parameters like any
  other; whether they are state handed along in the claim's sense is for the author, and the
  count stays as built until then. No trend is resolved on one chain. So on this chain the
  first half of the claim holds (the essential part is conserved) and the second does not show
  in lines: OfficeFloor wrote more organisation per checkpoint, not less; what it has less of is
  callers passing values to callees, and data standing by (H4).
- **The development chain's files, and rows 82 and 83 on it** (22 November 2026; one chain an
  arm, descriptive only).
  - *Looked at in scratch, before rows 82 and 83 were written, and the reason for them.* New Java
    files a checkpoint: 1.03 in OfficeFloor, 0.15 in Spring; Java files at the end 203 and 94, the
    largest 15.5 and 51 kB. Existing files ever gone back into: 49 and 10; the busiest,
    OfficeFloor's wiring file `owners.POST.yml` at 24 of 60 checkpoints and Spring's
    `OwnerRestControllerV1.java` at 43 of 59; the three busiest files take 44% and 83% of the
    returns. `OwnerMapper` (24 in each arm) and `Owner` (16 and 13) are gone back into alike:
    the problem's own data growing. New methods that are not wired functions and hold logic: 80
    and 81, with 85 and 100 parameters and 4 and 12 values passed by callers, in 32 classes in
    OfficeFloor and 13 in Spring (36 of Spring's in the controller). OfficeFloor's 35 new wired
    functions carry 1.9 injected parameters each. So OfficeFloor still writes methods that are
    called in the ordinary way, as many as Spring; they sit in small classes of their own and
    are handed existing state less often. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `files`, `new_methods`; §9 row 112.)*
  - *As built* (`MEASURE_VERSION` 31, `results/analysis/pilot/REPORT.md`). **H4's count, how
    well-trodden the files gone back into were:** 13.4 a checkpoint in OfficeFloor (8.7 Java,
    4.7 wiring; 5.3, 15.0, 19.9 over the thirds) against 21.7 in Spring (7.5, 22.1, 35.4), ratio
    0.60 [0.49, 0.74]; the plain number of files, reported, 1.50 [1.16, 1.94] as before. A third
    of OfficeFloor's count is its wiring: the endpoint's flow file is where it keeps going back.
    **The parameters of new called methods** 1.48 against 1.86 a checkpoint, 0.80 [0.60, 1.06]
    (90%): the stated direction, not resolved on one chain; **their trend went against the
    stated direction**, 4.8 [1.8, 12.5]: OfficeFloor's rise over the thirds (1.0, 1.6, 1.85) as
    Spring's fall (2.35, 1.75, 1.47). New called methods with logic 1.40 against 1.49 a
    checkpoint. The values callers pass new methods 0.33 [0.11, 0.97], as before. The injected
    parameters of new wired functions 1.10 a checkpoint (1.7, 1.0, 0.6). Nothing was changed
    after these were seen. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `trodden_thirds`; §9 row 112.)*
- **Where the logic landed, on the development chain, and the histories at 200 refits** (22
  November 2026, `MEASURE_VERSION` 32; rows 84 and 85; one chain an arm, descriptive only; the
  figures of the first paragraph were seen in scratch before row 85 was written, and the built
  ones are the same). Per checkpoint, over the thirds of the stream. *OfficeFloor:* logic into
  new wired functions 3.35, 2.80, 0.55 (new wired functions 0.95, 0.60, 0.20); into new called
  methods 3.10, 5.75, 7.30; into methods that existed 1.30, 1.40, 3.55 (existing methods added
  to 0.40, 0.45, 1.75). *Spring:* into new called methods 7.00, 7.00, 6.16; into methods that
  existed 1.55, 2.25, 3.37 (0.80, 1.00, 1.37). So on this chain OfficeFloor stops writing new
  functions and comes to work as Spring does, and in the last third the arms look alike. The
  author had expected the reverse (Spring wiring in calls to methods that exist, OfficeFloor
  writing new functions); Spring does put more into existing methods as the stream goes on, but
  keeps writing new called methods throughout. *The histories with 200 refits:* H2 2.93
  [2.58, 3.19] and 2.37 [2.34, 2.44], H7 0.82 [0.61, 0.88], the same to three figures as with
  1,000 (two repositories, so neither means anything); step 4 for both analyses took five and
  a half minutes, where it had taken twenty. Nothing was changed after these were seen. *(Figures here first read by a one-off query; step 5 now makes them, as the tables stand, in `DIAGNOSTICS.md`: `timing`; §9 row 112.)*
- **The development chain under rows 89 to 93** (24 November 2026, `MEASURE_VERSION` 34; the
  numbers here are those of row 93; one chain an arm, so descriptive only). *H1:* the arm
  contrast's level went the form's way, its trend did not show: placements forced at the class
  0.15 a checkpoint in OfficeFloor against 0.44 in Spring, the ratio half-way through 0.25 [0.09,
  0.65]; over the stream 7.5 [0.4, 156], too wide to read; Spring's fall in alternatives 0.16
  [0.02, 1.28] as before. *H2:* the core draws at the class 18.2 [12.5, 26.5] and at the method
  20.3 [11.8, 34.7]; a core value come back to in the function arm 0.09 [0.02, 0.32] as often at
  the method. *H3:* the bystanders' slope 0.015, within a class 0.026, within a method 0.023.
  *H4:* the function arm's bystanders lower half-way through (−1.59) and flatter (−0.017); later
  intrusion 0.16 at the class and 0.11 at the method; the files gone back into 0.60 [0.49, 0.74]
  as well-trodden. ***H5 went against the form:*** the function arm added **1.25 [1.06, 1.47]
  times the links** for the same logic, and the gap did not widen (1.13 [0.64, 1.98]). By kind,
  a checkpoint: call links 4.19 in OfficeFloor against 3.93 in Spring, state links 0.68 against
  0.74, and the wiring's flow links 0.93 against none; so the function arm's calls between
  methods were about as many as Spring's, and its wiring came on top. Its links rose over the
  thirds (4.65, 6.20, 6.58), Spring's did not (4.30, 5.00, 4.72; its own rise 1.02 [0.52, 1.99]):
  the stream's single endpoint gives Spring no call chain to deepen, and OfficeFloor's rise goes
  with its drift towards called methods (§4.9, above). The links lost were higher in the function
  arm (2.31 against 1.66 a checkpoint). *H6:* not above (cognitive 0.32, cyclomatic 0.35; the
  class measures untestable, five classes). *H7:* 1.03 [0.45, 2.37], unresolved. *The histories*
  (`HISTORY_VERSION` 14, read again under the new numbers): H1 at the class every placement
  forced (not testable), H2 2.93 and 2.37, H4 0.075 and 0.072 in later intrusion, H7 0.845 [0.673,
  1.061], not above. **Nothing in H5 was changed after it was seen.** The author's reading, given
  before these were computed (§1, *The overview*): the calls a function gathers can be split out
  again; to see whether that is where the function arm's calls are, a reported reading of its
  call links by caller (a wired function or another method) and by class was added after this
  (row 94), and the chain measured again.
- **The development chain under rows 94 and 95** (24 November 2026, evening, `MEASURE_VERSION`
  36; numbers of row 93; descriptive only). *H5 weighed:* the function arm's weight of links for
  the same logic **1.06 [0.92, 1.23]**, about the methods arm's (the plain count 1.25 [1.06, 1.47]
  as before), and the gap over the stream **1.73 [1.02, 2.92]**, the function arm's rising faster:
  against the prediction. A checkpoint weighed 12.10 in OfficeFloor and 10.97 in Spring (calls
  10.49 and 10.22; state 0.68 and 0.74; flow 0.93 and none). Every wiring edge weighed 1: on this
  chain no edge carried a value; the data passed through `Out` and `@Val`. *The call links by
  caller:* in OfficeFloor 2.92 a checkpoint from wired functions and 1.27 from other methods, the
  latter **0.05, 1.80, 2.00 over the thirds**, so the helper methods the agent began writing
  inside functions after the first third (§4.9) carry the function arm's rise; in Spring 3.93,
  all from methods. Across classes 3.34 in OfficeFloor (mostly functions calling the objects
  injected into them: repositories, mappers, stores) against 2.38 in Spring; within the caller's
  class 0.85 against 1.55. The weighed links lost were higher in the function arm (4.56 against
  3.93). **H5 is frozen as it stands** (the drafter's advice, the author agreeing on 24 November
  2026): it was restated (row 89) and weighed (row 95) after the development chain had been
  seen, each recorded, and a further change aimed at the same figure could not be defended; the
  ui runs, not yet read, decide it, with the breakdown reported beside. A call made on an injected
  object stays a call link (§4.2c): a call is control flow whatever its receiver. That was the
  drafter's reading and is kept on that principle, not on these figures.
- **A filled ball or pebbles, first look** (25 November 2026, `MEASURE_VERSION` 37; descriptive
  only). Spring's concentrations grew as **pebbles**: growth exponent 0.90 [0.89, 1.25] (five core
  classes at the end, 15.8 methods each, the largest holding 0.45 of the volume; three of them
  grew); OfficeFloor's concentrations 0.67 [0.35, 0.95] (5.8 methods), its other classes 0.22
  [0.01, 0.51], mostly swelling (2.2 methods, the largest 0.86). Two faults were found on reading
  it, both corrected before it was read again (rows 102, 103): **the flow containers were named
  by the classes in them**, so a flow that gained a function became a new container, and every
  flow's exponent came out near 0, which is not a reading; and **the cache of call graphs could
  hand a chain measured after another the earlier chain's graph** (row 102), which may touch
  every figure built on the call graph for the second chain of a run, here Spring's, since 19
  November. These figures are therefore superseded by the run at `MEASURE_VERSION` 39.
- **The development chain under rows 99 to 105** (25 November 2026, `MEASURE_VERSION` 40;
  descriptive only). **The cache fault of row 102 did not bite** on this chain: every figure of
  the run at 38 and 39 came back the same, H1 to H7, H5's weights and its breakdown, and the
  containers' exponents. Only the containers' intervals moved, because their resampling followed an
  order Python draws afresh on each run; sorted since (row 106), and now the same run to run. **The
  wiring edges whose weight could not be read: 0 of 55** (row 99). **The flow containers** (row 103)
  now grow: exponent 0.54 [0.00, 0.71] over 12 flows that grew (0.23 for those that are not
  concentrations; the one concentrated flow, 31 blocks, 0.75). **H9: no difference.** Of the classes
  of two or more blocks at the end, 43 in OfficeFloor and 47 in Spring, the cheapest split cut 0.79
  and 0.75 links on average; the function arm's ratio at the same size **1.10 [0.68, 1.79]**, the
  gap as classes grow 0.99 [0.61, 1.59]. Spring's concentrations had 19.5 blocks and split for 1.0
  link, OfficeFloor's 7 blocks for 0.75; five OfficeFloor classes could not be split into quarters
  (one block holding most) and were left out, none in Spring. **The sinew shape** says why Spring's
  core splits cheaply here: at the class its uses fall almost on one value, `OwnerRestControllerV1`'s
  `clinicService` (22 of 37 uses; effective number 1.15; 65% of changes repeating a combination
  already used there), and `clinicService` is an **injected** service, which is not state (§4.2c):
  methods sharing it are not tied together, and the controller can be split by injecting it into
  both halves. The author's case of a rewrite is a class whose blocks share state no one injects,
  which the petclinic stream hardly makes. At the method Spring's effective number was 1.74 (over
  the thirds 1.60, 1.56, 1.91), OfficeFloor's 2.19 (2.86, 2.40, 1.87). **H9 is left as it is** for
  the ui runs to decide, as H5 was; its population (every class of two or more blocks) is still the
  drafter's choice for the author to confirm, now after these figures have been seen. *The
  histories*, read again at `HISTORY_VERSION` 15 once the network was back (the first try failed:
  "Could not resolve host: github.com"): **the cache fault of row 102 did not bite there either**.
  Every figure already in their report came back the same, H1 to H7 and every reading; what is new
  is only what rows 99 to 105 added: the sinew shape (human, at the class, effective number 4.51
  over 1257 uses; agent 2.94 over 36) and H9, not testable on a history, whose arms do not solve
  the same problems.
- **The development chain under rows 107 to 110** (25 November 2026, `MEASURE_VERSION` 41;
  descriptive only). **Only H5 moved**, and H9 is gone: every other estimate came back the same to
  the last digit. **H5 with constants as state links** (row 109): 1.05 [0.91, 1.21] at the level,
  the gap over the stream 1.70 [1.03, 2.79]; without them, the test as it stood, 1.06 [0.92, 1.23]
  and 1.73 [1.02, 2.92], the figures of the run before, so measuring again changed nothing else.
  The constant links a checkpoint: OfficeFloor 0.37, Spring 0.47 (0.71 [0.37, 1.37]). Counting
  constants hardly moves H5 here. **H1 on the contrast alone** (row 107): forced at the class a
  checkpoint, OfficeFloor 0.15 against Spring 0.44, **0.25 [0.09, 0.65]** at the level; the gap
  over the stream **7.48 [0.36, 156]**, which rests on OfficeFloor's nine forced placements and
  cannot be read on one chain an arm; Spring's own rise 2.57 [0.66, 10.0]. H1's p, the larger of
  the two, is 0.90, from the trend: on this chain the level goes the form's way and the trend says
  nothing, so *especially over time* is the half of H1 the ui runs have to show. Choice narrows,
  now reported: 0.16 [0.02, 1.28] at the class. *The histories*, analysed again (their tables
  unchanged): H1 is not testable there, and its reading of choice narrows is **every placement
  forced, no alternative in any of 638 rows**, the case the review found would have silenced H1
  under its old rule (row 107). Nothing else moved.
- **The diagnostics, first made by the steps** (26 November 2026, `MEASURE_VERSION` 42, row 112;
  descriptive only). Every estimate came back the same; step 4 only added the fits within each arm.
  **Most figures the plan had from one-off queries come back exactly**: the files (1.03 and 0.15
  new Java files a checkpoint, 203 and 94 at the end, the largest 15.5 and 51 kB, the busiest gone
  back into at 24 of 60 and 43, the three busiest 44% and 83% of the returns, `OwnerMapper` 24 in
  each arm and `Owner` 16 and 13); the new methods (35 wired functions at 1.9 injected parameters,
  80 and 81 called methods with logic, 85 and 100 parameters, 4 and 12 values passed, 32 and 13
  classes, 36 in Spring's controller); the well-trodden count over the thirds; the runs into
  existing methods (74, 12 injected; 71 to 67; 20 to 10); Spring's bound new methods (9 by a call
  only, 4 by both; 4 and 288 later arrivals; 102 values introduced, 1 used; 13 rows, 43 arrivals,
  all `addOwner`); the change sizes; the bystanders and their thirds; `addOwner`; the controller's
  Gini 0.20 to 0.45 and its correlation −0.50; the junctions; the sample's draws, commits and
  units; bytechef's class rows. **Some differ, from tables remade since or rules made exact**:
  existing files gone back into 48 and 9 (§6 had 49 and 10); new methods bound by a field only 16
  (15); Spring's arrivals at the method 319 (396) and at the class 9.2 a row (10.9); the arrival
  rate of new and existing methods 0.004 and 0.19 a later checkpoint (0.005 and 0.24); the busiest
  class's runs 106, its fields standing by 4 to 17 (41 arrivals, 4 to 16), `addOwner`'s 33 runs (25);
  H6's class rows 268, the controller 76 and 79% of the arrivals (77, 37, 87%); fields added where no
  unbound code landed 0.35 and 0.09 (0.35 and 0.06); bytechef's method alternatives 21.6 (26);
  the methods on a host's flow, Spring 27 early and 69 late (64 and 114); and the domain-typed
  rows' alternatives over the thirds, 6.0, 3.2, 5.9 in Spring (10, 15, 23), the split now by a
  stated rule (a value named after a class of the system) where the first was by eye. **Size or
  data within Spring alone**: at the method size alone 3.31 [2.17, 5.03], with what stood by 5.00
  and what stood by 0.88 [0.76, 1.03] (§6 had 3.20 [2.42, 4.23], 4.43 and 0.88 [0.78, 0.99]); at
  the class 1.28 [1.03, 1.60], 2.10 and 0.91 [0.87, 0.95] (1.22, 1.89, 0.92): the same reading,
  size draws and what stood by does not once size is held, the method's interval now reaching 1.
  Step 4 took 174 seconds on the pilot at 1,000 refits. None of this changes a rule.
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

- **H1's alternatives are found by type, on a control flow read without a symbol solver** (§4.2a).
  At the method a common type (`String`, `int`) still matches more readily than a domain type,
  though only on the host's own flow. The flow can miss a method reached by a call whose receiver
  the source does not type (a chained call), or by the framework (reflection, events, callbacks),
  which biases the count down; it can include a method by an interface's every implementation,
  which biases it up. The share of calls followed is reported. A constant or state of the class
  makes the class forced by definition. A missed alternative makes a placement look forced. None
  of these should change with the checkpoint by itself, or differ by arm, and H1 compares the arms
  and their trend over the stream, read by the same instrument; the alternatives are kept by name
  for the check. On a history the
  index of the tree is exact at each unit's parent, but a repository's tests and generated code are
  left out as production Java is.

- **H7's spread counts classes, not reasons** (§4.2b). A feature that touches a controller, a
  service and a repository spreads by design (layering), not from lack of cohesion; H7's *forced*
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
  ratio). H7 holds the change's size fixed for this reason (§9 row 61), and H5 the logic added; a reading of a
  class's boundary against its size, if built, must be read against the exponent the size alone
  predicts, and against the function arm.
- **High coupling in a few classes may be unavoidable** (Taube-Schock, Walker and Witten 2011:
  between-module connectivity is roughly scale-free, so some highly coupled modules are expected
  of the distribution, not of poor design). This is the rival reading of the calls across the
  encapsulation (H8's dispersion) and of the concentrate signal: a forced class that gains coupling may be in that tail whatever forced it.
  The forced/unforced contrast at the same size and the arm contrast are what separate the two.
- **H5's links are counted, not weighed, and the agent may not use the form** (24 November
  2026). A link that carries ten values and one that carries none count alike, by the author's
  choice. On the development chain the function arm wrote fewer wired functions and more called
  methods as the stream went on (§4.9), which brings the method calling structure back inside it:
  a gap that does not widen may be the agent's habit, not the form. The
  logic in the model holds the change's size; the amount of logic itself is shown the same in both
  arms by §4.9. The author's answer (§1, *The overview*): a function that has gathered called
  methods is easy to split again along its control flow, and a reviewer, an AI among them, can
  judge its cohesion alone; the method structure's coupling makes the same split hard. That is a
  claim about what can be repaired, not a measure, and does not change what H5 reads.
- **The calls across the encapsulation read coupling as calls and openness as access** (§4.2c;
  H8's dispersion). A field made public and
  read directly from another class, or a call the instrument cannot follow (an untyped receiver,
  reflection, framework callbacks), is not seen; nor is coupling through shared types without
  calls. A renamed or moved method makes its calls look new on both sides. Neither should differ
  between forced and unforced classes by itself. A forced class is often the larger class (the
  core of H2), and a larger class may gain more calls whatever forced it; the index is in the
  model, and the class's size is not (the reading is about the force, and size is its result).

- **H4's symmetric count and the state handed along were both changed after the development
  chain went against them** (22 November 2026, rows 82 and 83), within hours of being written.
  In each case the first form counted something the claim is not about (a file count scores
  dispersion; a parameter count scores injected parameters), the reason given does not rest on
  the result, and the first form is still reported. But the order is as stated, both changes
  favour the function arm on that chain, and the author wrote the framework. Of all the plan's
  revisions these two are the ones a sceptical reader should weigh most.
- **The agent knows one arm far better than the other** (added 22 November 2026, from the review
  of the plan). Spring is everywhere in what the agent learned from; OfficeFloor it knows from
  the stack's scaffold and whatever documentation the harness gives it. So a difference between
  the arms may be, in part, a difference between an idiom the agent has seen ten thousand times
  and one it is following from an example: it may place code as the scaffold does because it has
  nothing else to go on. The arm is therefore the framework *as the agent uses it*, not the
  construct alone. What bears on it: Run D changes the construct inside Spring, the arm the agent
  knows; and corpora B and C are people's and agents' code in the wild. It is not ruled out.
- **Agent-written code (corpus A).** Placement by an agent may not be placement by people.
  Corpus B is the check, which is why it is drawn pre-AI. There is a specific reason for concern:
  AI agents' pull requests touch fewer files and spread less than human ones of similar size
  (Ogenrwot and Businge 2026), so agents may concentrate by default. The arms of corpus A are
  therefore read only against each other, never as absolute rates of concentration.
- **Lexical names.** No symbol solver, as in the width harness (decided 16 November 2026). A local that shadows a field
  is already told apart by the method's own variables, and the pilot found no unresolved name in
  418 runs. Names that resolve to nothing are reported per run. Since 22 November 2026 the
  instrument's calls, field reads and bound names are checked against the compiler on corpus A
  (§4.8), which found one fault at once (a call followed to sibling classes). The check covers
  what the compiler can see: not generated code, not calls made by a framework, and not corpora B
  and C, where the tree read does not compile; there the instrument is trusted as far as corpus A
  shows it can be, on other code.
- **Provenance.** Line tracking across moves is imperfect. CodeTracker reports about 99.9%
  method-level precision and recall, but statement-level provenance is weaker. Disagreements
  with `git blame` are reported.
- **Shared counts at the class and the method.** H2 and H6 are read where the code was placed.
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
  a class (below) this made H2's Wald interval too narrow. Since 22 November 2026 H2 is decided
  on the cluster bootstrap (§5), which resamples whole chains and so carries both; the Wald
  interval is reported beside it.
- **The bootstrap is over few chains.** A run has ten chains a stack. A percentile interval over
  ten or twenty clusters is itself rough, and tends to be somewhat narrow; it is still the
  honest unit, since a chain is what was run independently. The number of chains and of refits
  that could be fitted is reported with every bootstrap interval.
- **Run D is run after Run A, not beside it** (§3.1a). H8's contrast therefore holds whatever
  changed between the two runs: most of all the agent, if the model served under the same id has
  changed. Accepted by the author on 22 November 2026, as the run cannot be made concurrently.
  The instruction is also more than the removal of `private`: an agent told not to encapsulate
  may place code differently for that reason alone. Compliance (§3.1a) checks that the
  instruction took, not that it did nothing else.
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
- **H3 within a method starts from nought.** A method has no bystanders at the checkpoint that
  creates it, and later code placed in it sees the values it was created with. Part of the slope
  within a method is therefore given by a method being new once. That is a place gathering data,
  which is the claim, but it is not evidence beyond the definition.
- **H3 and H2 overlap.** A place where data gathers (H3) and a place whose core is used by what
  comes next (H2) are read on the same busy class. They are not independent tests, and Holm
  treats them as if they could be.
- **H3 and H2 no longer make one loop.** Until 19 November 2026 they did: a place gathers data,
  and the gathered data binds the next code. As restated, H2 says the next code comes for a few
  core values and not for what gathered. H3's rise is then mostly periphery: what code has to sit
  beside, a cost of the place, and not what draws code to it. H3 was renamed to say so (§2); its
  test was left as it is, so H3 by itself no longer shows a pull, only a cost that grows.
- **H3's periphery is not H2's.** H3 counts bystanders, the pre-existing values a run does not
  use. H2's periphery adds what the change introduced. H3 was not changed to count introduced
  values: they are not there when the code arrives, so the code does not sit beside them.
- **H2 was shaped on the development chain** (§6), as H3 and H4 were: its restatement followed a
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
- **H3 and H4 were shaped on the development chain.** The bystander measure and the direction of
  both hypotheses were settled after seeing it on chain 9 (§6). That chain is excluded, and the
  registered chains had not been read, but the hypotheses are no longer blind to this run's
  general shape: the other chains of the same run are likely to resemble it. The replication on
  the ui stream, a different application, is the stronger test.
- **Growth is not gravity by itself.** A codebase that grows has more of everything. H3's slope
  is read against the function arm, which grows by about the same amount on the same stream
  (§4.6): bystanders that rise in one arm and not in the other are the form's, not the growth's.
  H3 alone, without H4, would not show that.
- **Visible is not used, and not harmful by itself.** A bystander is exposure: something the code
  could read or disturb. H2 asks whether what stands by is later used, not whether that does harm; the
  harness's own signal of a rule broken that was not meant to change is the outcome that would
  answer the question of harm most directly (not read by this plan).
- **One stream per corpus.** The intervals are over chains: they say what this agent does on this
  stream again, not what happens on other problems. The petclinic stream puts every rule on one
  endpoint. The ui stream is the second set of problems; corpus B the third.
- **Smells born, not grown.** Tufano et al. (2015) find most smells present from a unit's
  creation. So H3's gravity may act mostly at creation (a new method pulled by its parameters,
  §4.3) rather than through accretion. Both are measured, so the data can say which.
- **The cohesion assumption.** It holds by construction only in corpus A, and only if refactoring
  is separated out correctly (§4.1).
- **The problem is fixed, not measured.** The study holds the problem fixed by design (one
  checkpoint, one problem; one stream for both arms). It does not measure how hard a problem is,
  beyond the addition's size and its declared crossings. In corpus B a commit is not one problem,
  so H6 is not read there.
- **Power for H6 and H7.** A test against a margin needs more data than a difference test. If an
  interval is too wide to fall below the upper margin, H6 or H7 is reported as unresolved, not as
  supported. *A rough check* (21 November 2026, the drafter's; normal approximation from the
  development standard errors, scaled by the number of units, with no between-chain variance, so
  optimistic): on log scale H7's standard deviation per unit is about 3.9 on the development chain
  and 3.0 on the development histories, H6's cognitive measure 2.2 on the histories. With a true
  forced ratio of 1.0, a run of 9 chains an arm (about 530 units in the methods arm) shows H7
  below 1.25 with a chance of about 37% to 53%; about 1,100 to 1,900 units (19 to 32 chains) are
  needed for 80%. At a true ratio of 0.85 the chance at 9 chains is 74% to 91%. So on one
  petclinic run an unresolved H7 is the likely outcome even if spread does not see the force;
  corpus B (two sets of 300 repositories) is where H7 has the units to resolve, and on corpus A
  H7 is read per run, never pooled (§3.1). The confirmatory hypotheses are not at risk in the same
  way: their tests are against 1, not a margin, and on the development chain H2, H1 at the class
  and *forced changes couple* (since deleted) lie well away from it.
- **Encapsulation and the reader confounds author with much else** (§4.2f). A declared agent
  commit is merged by a person who may have reshaped it; undeclared commits may be assisted; the
  agent and its window are not recorded per commit; corpus C's repositories are younger than
  corpus B's, and big systems are older and more structured whoever writes in them. Agents
  learned from human code, so they may make private members out of habit, not need. The system's
  size is a stand-in for whether it fits a context window, and agents retrieve a few files a task,
  so their working context is smaller than their window. The reading can show a difference and
  how it moves with size; it cannot say why.
- **H6's measures were chosen on the development chain.** Of the literature's measures, those
  taken into H6 are ones that lay below the margin there, or reached above it only at the class
  (§6); the one measure wholly above it, the method's fan-out, was put with the sinew measures,
  with CBO, as reach. The reasons given do not rest on the results (the first are the literature's
  usual shape measures; the second count what a place reaches out to), but the order is as stated.
  The measures left out of H6 are all reported, so a reader can read H6 with any of them put back.
- **The junction left H6 after it had left H6 unresolved on the development chain** (§6). The
  reason given is that it is not a shape measure of the literature, and that reason does not rest
  on the result; but the order is as stated, and on that chain H6 reads better without it.
- **H6 was made one-sided after the development chain failed the two-sided form.** There, more
  complex methods were followed by less intrusion (§6), which "adds nothing" does not allow and
  "does not draw in" does. The one-sided claim is the weaker one. The two-sided reading and every
  effect's size are reported, so a shape that goes with less intrusion is not hidden.

## 8. Order of work

*The hypotheses here keep the numbers that stood when each entry was written; §9 has the table to today's (row 93).*

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
   steps built on 18 November 2026: `./step2b_samples.sh`, `./step3b_histories.sh`).
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
- *Decided by the author on 21 November 2026 (later), after seeing H6 on the development chain and
  the development histories under forced by encapsulation* (§6): H6 restated as **spread does
  not see it** and moved to the secondary tier (row 67): "H6 falls into existing shape literature
  of trying to find cause. Nothing about shape will help as cohesion has no shape to highlight."
  The drafter's choices in it, not yet spoken to: the margin 1.25 and the 90% interval taken from
  H3; the function arm's forced ratio, the rise and the accountings kept as reported. Noted with
  it: on the development histories H7 is 1.125 [0.820, 1.545], so the contrast the restatement
  leans on (force seen at the boundary, not in the spread) is so far shown on the development
  chain only (§6).
- *Decided by the author on 21 November 2026 (evening), on the drafter's review of what a paper
  would lack:* **(1) defects are out of scope.** "Defects are just errors and concentration and
  dispersion just increase the risk of errors in different ways. It is not something that is part
  of the force. The force is a detection to determine placement and whether likely too
  concentrated or too dispersed." No reading ties forced placements to later fixes. **(2) No human
  check of the forced label.** The study is of checks on code without human intervention ("looking
  to understand the underlying physics of software"); the instrument's fixtures are its check
  (§7). **(3) A full read of the literature** behind §10's abstract-based verdicts (LITERATURE.md
  §10, *Full read*). **(4) The claims are about code, not authors.** "It is the physics of software
  so should apply regardless of human or AI author". Pescio (*Forces*, 2024 draft, pp. 14–15)
  states the principle ("none of the forces that can be actually observed ... will change at all:
  only the efficiency of carrying out some work can be impacted by changing the actor"), untested;
  this study tests it, with the author varied: corpora B and C test that it does; a
  difference between human and agent code is reported, not a premise. **(5) Separate papers.**
  The experiment may run as one, written up as separate papers (the force and its outlets; why the
  literature's readings miss it). **(6) Power for the margin tests checked** (§7, *Power for H3
  and H6*).
- *Decided by the author on 22 November 2026, walking through the drafter's open choices before the
  tag* (each was listed above as not yet spoken to): **(1) H2 stays a rate per value** (the
  author's question on its fit is closed). **(2) H2's core at the class is its encapsulated part**
  (§2, §4.4, row 71). **(3) H5's choices accepted** (a level where every placement was forced
  passes with p 0; both levels; the chain's intercept and no checkpoint intercept; untyped values
  left out; *of these, the pass with p 0 was withdrawn later the same day, row 73, and the class
  level alone has been the test since row 64*). **(4) Only private forces; package and protected are reachable**, and are reported
  descriptively as a looser encapsulation ("private is most strict and forcing"): each placement
  bound at the class carries the strictest access of the members it used (`tables.bound_access`),
  and the growth of existing classes is reported by it (`prepare.growth_by_access`, beside H6's
  growth accounting). **(5)
  H7's operational form accepted** ("this is showing where encapsulation is not containing change
  and the cost of it"). **(6) The split and concentrate thresholds accepted** as a report, left
  open to other values in exploration. **(7) H6's margin and 90% interval accepted. (8) The
  reader reading's choices accepted. (9) Run D's choices accepted.** With these, no drafter's
  choice listed in this section is left unspoken to.
- *Decided by the author on 22 November 2026:* a **no-encapsulation run** (Run D, §3.1a, row 70):
  "prompt to the AI to not do encapsulation and leave everything public and be a specialty run of
  its own done on angular/spring combination as for OfficeFloor this makes little sense as
  everything is injected and nothing left to make public". The drafter's choices in it, not yet
  spoken to: the name Run D; reading it against Run A's `angular-spring` only; the 90% compliance
  condition; the five predicted directions; reported, not confirmatory. The run needs the
  instruction added to the harness (`ui-long-degradation-test`), outside this repository.
- *Asked by the author on 22 November 2026, drafted the same day:* "I'm wondering if encapsulation
  is a human issue to keep context within the 25 lines of comprehension and that AI agents may not
  require this until systems go beyond their context windows?" Drafted as a reported reading,
  *encapsulation and the reader* (§2, §4.2f, §5, §7; row 69; "draft it as a reported reading").
  The drafter's choices in it, not yet spoken to: the four measures; the split at 200,000 and
  1,000,000 tokens; undeclared commits kept apart; the 10-repository floor per band. The
  development histories hint the other way (growth of existing classes arriving forced: agent
  repository 0.70 of 193 positions, human 0.45 of 3,972, §6), on one agent repository.
- *Decided by the author on 22 November 2026 (later), on a review of the plan before the tag*
  (§9 rows 72 to 76). The review's eight concerns and what was done with each:
  **(1) H2 can hardly fail** (a value already used once is likely to be used again whatever the
  place): explained to the author; nothing changed yet, and the arm contrast in core reuse stays
  reported beside H4. **(2) An injected private field**: it forces; the injected part is carved
  out inside forced as the opportunity injection gives (row 72). **(3) H5 is a fall**, below 1; a
  level with every placement forced is not testable (row 73). **(4) H4 counts the methods arm's
  return to its handler and not the function arm's return to its wiring**: explained to the
  author; nothing changed yet (reopening with the wiring files stays reported). **(5) The
  confirmatory tests are decided on a cluster bootstrap**, and H7 carries the class's intercept
  (row 74). **(6) Run D's test is registered** as H8; it is run after the others, not beside Run
  A, which the author accepts (row 76). **(7) H3's sensitivity reading** with the coupling
  measures put back (row 75). **(8) No independent check of the instrument**: explained to the
  author; nothing changed yet. The review's smaller point, that a git tag can be moved and an
  outside deposit cannot: the author keeps the tag ("my whole experiment is a threat due to me
  writing OfficeFloor, so will let the academic rigour of pre-registration happen for independent
  replication, git tag is enough for me").
- *Decided by the author on 22 November 2026 (later still):* "build 1, 4 and 8, then commit and
  rerun". **(1)** H2 also needs a core value come back to less in the function arm (row 77).
  **(4)** H4 also needs fewer existing files gone back into, Java and wiring alike (row 78).
  **(8)** The instrument is checked against the compiler on corpus A (row 79, §4.8). The check
  found a fault in the call graph at once, corrected (row 80). The drafter's choices in these,
  not yet spoken to: for H2, 10 core records in each arm before a level's contrast is needed, and
  the rank-sum test where the function arm's cores are never come back to; for H4, that the
  count has to be *lower* (below 1), not merely no higher, and that a deleted or renamed file
  counts as gone back into; for the check, every fifth checkpoint and the last, no threshold on
  the shares, and the project's classpath taken offline from the chain's head.
- *Decided by the author on 23 November 2026, walking through the drafter's open choices of rows
  72 to 85 one at a time* (each was built as the drafter chose; none changes the code):
  **(1) H5 where every placement was forced is not testable**, not a pass (row 73): "B". The
  cost accepted: on corpus B, mostly without injection, H5 will often not be testable; the share
  forced is still reported. **(2) H2's arm contrast is needed at a level where each arm has at
  least 10 core rows** (row 77): "A". The low bar is the stricter choice, since a contrast
  resting on few rows is more likely to fail than to be skipped. **(3) The compiler check reads
  every fifth checkpoint and the last** (row 79): "A", after asking why a compiler is needed at
  all (the instrument guesses by name, the compiler does not, and the check found the fault of
  row 80 the first time it ran). The check of bound names sees only the sampled checkpoints'
  hosts and is thin for that reason. **(4) In H4's count a file's creation by an earlier
  checkpoint counts as one earlier change** (row 82): "A ... any mutation needs to be counted".
  The author's principle, recorded with it: "The point of additive architecture is that it adds
  rather than mutates. So adding is a good thing when increasing functionality. It should not be
  penalised as a cost." The count agrees: a file a checkpoint adds is never gone back into and
  scores nothing; what scores is a later change to it, the first one included.
  *Decided the day before and recorded with their rows:* 200 refits on a history (row 84); the
  count of H4 and the wired functions' parameters apart (rows 82, 83); where the logic landed
  (row 85). *The smaller choices, walked through the same day:* **(5) the rank-sum test over
  chains** where the function arm's cores are never come back to (row 77): "A", against calling
  it not estimable or passing it untested. **(6) A deleted or a renamed file counts as gone
  back into** (row 82): "A", every mutation being counted. **(7) The compiler check has no pass
  mark but a tripwire** (row 86): "C"; and **the classpath is the chain's own at its head**, one
  for the chain: "A". **(8) The declarations stay a remainder** (§4.9): "A"; to be counted
  directly by a dated amendment if the figure comes to matter. With these, no drafter's choice
  of rows 72 to 86 is left unspoken to. *Known, and corrected the same day at the author's word* ("yes build it and
  re-measure"): the instrument did not see a nested class using a member of the class around it
  (row 87, §4.8). *Decided by the author the same evening, on H7 at `HISTORY_VERSION` 14:* where
  forced coupling came from, as a reported reading (row 88, §4.2c), and the pairs model refitted
  without the chain's intercept when its standard error is not computed (row 88): "B".
- *Decided by the author on 24 November 2026:* **H7 is restated as surface against volume** (row
  89). The author's framing, given over the conversation: "volume being encapsulated complexity and
  surface being coupling"; "the method calling structure is possibly considered accidental
  complexity and the essential complexity is the blocks of code contained in the methods"; "for
  concentration we have hypothesis for force sinew creating gravity. For coupling it is to keep
  these concentrations coordinated and is the surface, so should replace current coupling
  hypothesis". On the drafter's three questions: **(1) injection is not surface**, in either arm
  ("similar to injected dependencies in Spring provide flexibility. They are not associated with
  the control flow"); the drafter had recommended counting the injected parameters, so that the
  function arm could not win by leaving them out, and the author decided otherwise; the wiring's
  flow edges are counted, and a call on an injected object is a call link (the drafter's reading,
  to be confirmed). **(2) Shaped as H4**: fewer links for the same logic, and the gap widening,
  both needed. **(3) Links counted, not weighed** ("the existence of the link is the coupling").
  **A state link to a field of a method's own class** is counted (the inner surface): "yes, add
  it". The old H7, *forced changes couple*, was first "soft deleted" (out of the tests, reported),
  then **deleted** the same day ("Delete the old H7", row 90). Its measure stays, since H8 reads it;
  the reading of where forced coupling came from (row 88) is kept as a reading of that measure
  (the drafter's choice, to be confirmed). Made after the development chain's
  outer surface and its logic and organisation reading had been seen (§2, H7).
- *Decided by the author on 24 November 2026 (later):* **H5 is an arm contrast too** (row 92),
  so that every confirmatory test points at the difference between OfficeFloor and Spring, which
  the author holds to be the study's end ("it should be pointing out OfficeFloor vs Spring in
  terms of differences"). Of three forms put to the author with the development chain's figures,
  the forced placements a checkpoint (the drafter's recommendation) was chosen over the fall of
  the alternatives in each arm and the share forced. With it, H1, H3 and H6 stay about the methods
  arm alone: H1 the cost of the core (its arm contrast is H4's), H3 and H6 the literature's
  readings.
- *Decided by the author on 24 November 2026 (later still):* **the hypotheses renumbered in the
  order of the story** (row 93): "change the ordering of the HX to match the story order of what we
  are discovering", the order the drafter proposed; the history (§6, §8, §9) left as written, with
  the table at the head of §9; and H1 (as it then was) renamed *the encapsulation fills*, after the
  author asked whether the periphery is "the volume grows inside the encapsulation" (it is the
  encapsulation's state, seen from each new block, not its code).
- *Decided by the author on 24 November 2026 (evening):* **H5's links are weighed** (row 95), after
  the development chain had gone against the plain count (§6) and the author had seen that
  OfficeFloor's excess was its wiring between more, smaller pieces. The drafter put two choices:
  a wiring edge weighs 1, plus 1 where it carries a value ("1, +1 if it carries a value", against
  always 1); and the test runs on the weights with the plain count reported (against needing
  both). The author's earlier "the existence of the link is the coupling" is revised by this.
- *Decided by the author on 25 November 2026:* a reported reading of whether a concentration is
  **a filled ball or pebbles** (row 98, §4.2g): every class, the concentrations apart; in the function
  arm the wiring flow files as containers too; no direction stated ("no expectation"). The pilot is
  to be measured again at `MEASURE_VERSION` 37 for it.
- *Decided by the author on 25 November 2026, walking through the drafter's remaining choices one
  at a time* (row 101; each put plainly, with examples where asked for): **(1)** H1's arm contrast
  leaves out checkpoints where the agent changed nothing. **(2)** Where H1's negative binomial
  cannot be fitted it falls back to Poisson, recorded; the bootstrap interval carries the chains'
  variation either way. **(3)** A wiring edge whose weight cannot be read from the Java weighs 1,
  and how many there are is reported (row 99). **(4)** The ball-or-pebbles exponent is pooled
  over containers, those that grew most counting most, not the median container (worked on an
  example: 0.40 against 0.17). **(5)** H2's core is each placement's own (what its code was bound
  to), with no threshold; uses counted value by value; core and periphery compared within the
  placement. A class's methods as core values had already been settled by row 71 (its private
  methods are core). On top of it, the author asked for **the sinew shape** (row 100), with the
  effective number of values rather than a share cut-off. **(6)** The reader reading's size bands
  stay at 200,000 and 1,000,000 tokens (display only). **(7)** In the reader reading, corpus C's
  undeclared commits are a third group, never pooled, and a band with fewer than 10 repositories
  is shown and marked thin. With these, every drafter's choice listed above as not yet spoken to
  has been spoken to; the Run D choices of row 76 were settled with it.
- *Decided by the author on 25 November 2026 (later):* **the cost to fix a concentration** is stated
  now, before the ui runs, and built after the development rerun under way (row 104, §2, §4.2h); so
  that the author's answer to H5's drift (a function grown into a method structure is cheap to
  split, a Spring handler is not) is a prediction, not an explanation found afterwards. The other
  items not built (corpus B by issue, landing ranks on a history, what unbound code leaves behind)
  are left as **exploratory**, for after the experiment ("are all of these extra things we can do
  after the experiment as exploratory?"), reported as such if done.
- *Decided by the author on 25 November 2026 (later still):* **the cost to fix a concentration is
  H9**, a secondary hypothesis ("write the code for concentration and make it a H9"; row 105). Its
  rule, the drafter's, to be confirmed: tested on every class of two or more blocks at the end of the
  stream, at the same size, the concentrations reported beside it (the function arm forms too few
  concentrations to test on); a class no split of which leaves a quarter on each side left out and
  counted. Built and tested before any ui run is read; not yet computed on any chain.
- *Decided by the author on 25 November 2026, after a consistency review of the plan* (the
  drafter's, read-only, each finding put to the author one at a time; rows 107 to 110). **(1) H9
  deleted** (row 108): asked which classes it should be tested on, and whether a split counts the
  private members it would have to open, the author questioned its value ("I'm now questioning H9
  and its value. Why did we introduce it? As it is only looking at cutting up methods"); the
  drafter's reading, that it measured only inside the class while a rewrite's cost lies mostly
  outside it, and that H5 and the containers reading already carry its shape; the author: "delete
  it". Its population question falls with it. **(2) H1 is the arm contrast alone** (row 107): the
  review found that where every placement of the methods arm is forced from the first checkpoint,
  choice narrows cannot be tested and the code dropped H1 whole, its contrast with it. The author:
  "Is there another hypothesis about restricted choice? I'm thinking this just needs to be
  OfficeFloor is forced less especially over time"; both the level and the trend needed (the
  drafter's recommendation, chosen). Choice narrows is reported. **(3) Constants are state links in
  H5** (row 109): asked whether the sinew shape should say it counts private constants, as H2's
  core does, the author asked whether H5 should count them and why it did not; the drafter: it was
  the drafter's choice, never put to the author, reusing §4.3a's kinds of field, on the reading
  that a constant needs no coordination between the blocks that use it; the drafter recommended
  keeping them out; the author: "count constants in H5". The test without them is reported.
  **(4) Wording** (row 110): the bootstrap paragraph of §5 named the secondary hypotheses as on
  Wald intervals, where H3 is on the bootstrap; §4.2c opened with the plain count; the tiers
  paragraph named the readings §4.2b–4.2e; the sinew shape did not say it counts constants; code
  comments in `verdict.py` and `prepare.h5_rows` were out of date. Each corrected, no rule changed.
- *Done for rows 107 to 110:* the pilot measured again at `MEASURE_VERSION` 41 and both analysed
  again (§6); only H5 moved. The results index lost a column left for H9 (`report.main`).
- *Done for rows 99 to 106:* the pilot at `MEASURE_VERSION` 40 and the histories at
  `HISTORY_VERSION` 15 (§6); no figure moved under row 102. (H9's population, left there to the
  author, fell with H9, row 108.)
- *As it stood for rows 99 to 103:* the pilot measured again at `MEASURE_VERSION` 39 and the
  development histories at `HISTORY_VERSION` 15 (row 102 touches both: several chains or
  repositories are measured in one process): `./step3_measure.sh --analysis pilot`,
  `./step3b_histories.sh --analysis open-source-development --force`, `./step4_analyse.sh
  --analysis pilot open-source-development`, `./step5_report.sh`. Then whether the figures built on
  the call graph moved goes into §6, as for row 80.
- *Done for rows 94 and 95:* the pilot measured again at `MEASURE_VERSION` 36 (§6). **H5 frozen**
  (the author, 24 November 2026, agreeing with the drafter): no further change to it before the ui
  runs are read. **A call made on an injected object is a call link**, confirmed by the author
  on 24 November 2026 ("keep it counted"; row 96): receiving the injected object is free, using it
  is control flow from one block to another and is weighed as any call. Decided after the
  development chain had been seen (§6), on principle: injection removes the finding of the
  target, not the call. *As it stood for row 89:* the pilot measured again at `MEASURE_VERSION` 34 (`./step3_measure.sh
  --analysis pilot`, then `./step4_analyse.sh --analysis pilot open-source-development` and
  `./step5_report.sh`); the histories are not affected (`HISTORY_VERSION` 14 stands). Then H7's
  development figures go into §6. The figure of §2 was redrawn the same day (row 97). **H8 stays as it is**
  (the author, 24 November 2026: "keep H8 as is"): its *dispersion stronger* reads where the
  coupling goes, the calls across the encapsulation, not how much coordination the logic needs,
  which is H7's links.
- *To finish before the tag (state on 22 November 2026, later):* the development rerun **again**,
  at `MEASURE_VERSION` 29 and `HISTORY_VERSION` 13 (rows 72, 78 and 80 change the measured tables), with
  the same four commands as below. The rerun started that morning at 28 and 12 is **not to be
  used**: its step 3b and step 4 ran while rows 72 to 76 were being written into the code (step 4
  ran with them uncommitted), and its reading of the agent development repository was killed for
  want of memory while the R self-test ran beside it. Its measurements of the pilot's two chains
  and of the two repositories of people's code were made before the code changed, but are at the
  old version and will be redone. With the bootstrap (row 74) step 4 takes much longer than it
  did: on the R self-test, 60 refits of seven models took about ten minutes on a loaded machine;
  `PG_CORES` sets how many cores the refits use (four by default; each holds its own copy of the
  model, so more cores need more memory).
- *As it stood earlier on 22 November 2026:* the development rerun at
  `MEASURE_VERSION` 28 and `HISTORY_VERSION` 12 (rows 69 and 71): `./step3_measure.sh --analysis
  pilot`, `./step3b_histories.sh --analysis open-source-development --force`, `./step4_analyse.sh
  --analysis pilot open-source-development`, `./step5_report.sh`. Until it is done and committed,
  `results/analysis/` holds the results of 21 November 2026 (`MEASURE_VERSION` 26), without the
  reader reading or the private core. Then its results go into §6 (the reader reading, H2 with the
  private core beside the all-access core, growth by access) and are committed. A rerun was
  started on 22 November 2026; check `results/analysis/*/estimates.json` for `reported.reader`
  before running it again.
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

**The hypotheses' numbers** (24 November 2026, §9 row 93). §1 to §5 and §7 number the hypotheses
in the order of the study's story: the force, the concentration it makes, its cost, the control,
the coupling, and the literature's two readings. §6, §8 and this section are the record and keep
the numbers that stood when each entry was written. Up to row 92:

| Before row 93 | Since row 93 | |
|---|---|---|
| H5, choice narrows | **H1** | the force |
| H2, a core draws code in | **H2** | concentration |
| H1, the periphery grows | **H3**, the encapsulation fills | its cost |
| H4, function injection forms no core | **H4** | the control |
| H7, surface against volume (from row 89; before it, *forced changes couple*, deleted, row 90) | **H5** | the coupling |
| H3, shape does not draw code in | **H6** | the literature: shape |
| H6, spread does not see it | **H7** | the literature: co-change |
| H8, without encapsulation code disperses | **H8** | Run D |

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
| 67 | H6 restated as *spread does not see it*: the forced ratio of co-change spread not above the upper margin 1.25 (one-sided, 90% interval, as H3), its measure, model and change-size terms unchanged; H6 secondary; the confirmatory family H2, H4, H5, H7 (Holm over four) | §2, §5, §8, `verdict.h6`, `report.h6_section`, `analyse.R` (H6 with `tost`), `selftest.R` | Decided by the author on 21 November 2026 (later), after seeing H6 under forced by encapsulation on the development chain (1.026 [0.380, 2.775]) and histories (0.845 [0.644, 1.108]): co-change, like shape, is the literature reading a symptom to find a cause, and cohesion has no shape to highlight. Recorded as decided after seeing development results. Before the tag, so a revision |
| 68 | The full read's corrections (LITERATURE.md §10, *Full read*, 22 November 2026): Chowdhury et al. 2022b cited on the other side of size confounding (§1, §2 H3); Pescio's gravity described as attraction by mass, later co-change, with encapsulation a separation against it (§2); H7's prior work adds Pescio 2012, Taube-Schock et al., Schach et al., Steimann and Thies, Vidal et al.'s persistence; conservation framing adds Pescio Ch. 13 and Loth; H6 argues against a reading, not a finding, and the field handles change size only by dropping large transactions; Sun et al. on injection raising counted coupling at H4's wiring; Pescio 2024 as the prior, untested statement of "regardless of author". No measure, model or rule changes | §1, §2, §8 | The author's, 22 November 2026 ("apply the wording changes"). Kobori et al., Zhou et al., Page-Jones and Ousterhout's book not obtained; said where cited |
| 69 | Reported reading, *encapsulation and the reader*: agent against human units on private share of introduced members, growth arriving forced, members exposed or widened, and size of the class code lands in; with the system's size in tokens (continuous, and split at 200,000 and 1,000,000) and its interaction with the author; corpora B and C, corpus A descriptive | §2, §4.2f, §5, §7, §8, `chain.java_tokens`, `tables.member_rows`, `prepare.reader_rows`, `prepare.reader_summary`, `analyse.R` (`reader`), `report.reader_section` | The author's question, 22 November 2026 ("draft it as a reported reading"): whether encapsulation answers a human limit of comprehension that agents lack until a system outgrows their context. Operational form the drafter's. No hypothesis, measure of a hypothesis, model or rule changes |
| 70 | Run D, the no-encapsulation run: `angular-spring` with the agent told to leave every field and method public, read against Run A's `angular-spring`; compliance (at least 90% of introduced members not private) a condition of reading it; predicted: no growth arriving forced and choice not narrowing, H2's core drawing less at the class, more cross-boundary calls and reads and a wider spread at the same change size, the amount within the band; reported, not confirmatory; run ids, harness commit and wording by dated amendment | §3.1a, §8 | Decided by the author on 22 November 2026, before the tag: encapsulation isolated by instruction on the stack where it can be removed (not OfficeFloor, where nothing is left to make public). Operational form and directions the drafter's |
| 71 | H2's core at the class is the private members the code was bound to (private fields, constants and methods); the members it was bound to that others can reach join the periphery; the core with every member whatever its access reported beside it. Package and protected members reported descriptively as looser encapsulation. The drafter's open choices of §8 accepted by the author | §2, §4.4, §8, `tables.private_members`, `tables.outcome_rows` (`core_class`, `core_class_all`), `tables.bound_access`, `prepare.growth_by_access`, `prepare.h2_rows`, `analyse.R` (`H2_class_all`), `report.py`; `MEASURE_VERSION` 28, `HISTORY_VERSION` 12 | Decided by the author on 22 November 2026, after the development data, before the tag: "the forcing is about not being able to access outside the encapsulation, being the force". The test is unchanged in form (rate ratio per value above 1 at the class and the method) |
| 72 | An injected private field forces, like any private member; within forced, the growth bound only to injected private fields is reported apart as the opportunity injection gives (with another class already holding the dependencies, or none yet), beside the growth bound to the class's own private members | §2, §4.2b, `tables.lever` (`forced_lever`), `prepare.growth_by_lever`, `report.py`; `MEASURE_VERSION` 29, `HISTORY_VERSION` 13 | Decided by the author on 22 November 2026, after a review of the plan found §4.3 (an injected field may not pin code) and *forced* (any private member) at odds: injection gives the choice as a construct, but it is a lever that has to be exercised, otherwise private encapsulation is the force. No test changes: *forced* already counted them |
| 73 | H5 is a fall: the alternatives' ratio end to start below 1 at the class, one-sided; reversed when wholly above 1; a class level where every placement was forced is not testable and has no p. H5 against the upper margin 1.25, as it stood, is reported | §2, §5, `analyse.R` (`H5`, `H5_margin_*`), `verdict.h5`, `report.h5_section`, `selftest.R` | Decided by the author on 22 November 2026, on the review: a flat count supported *choice narrows*, and a level with nothing to narrow passed with p 0 and eased Holm for the others. Made knowing the development chain (0.16 [0.03, 0.92] at the class, Wald) and that the development histories, without injection, have every class placement forced and so will not be testable. Before the tag, so a revision |
| 74 | H2, H4's intrusion ratios, H5 and H7 are decided on the cluster bootstrap H1 already used (chains resampled within arm, 1,000 refits, percentile 95% interval, one-sided p), the Wald interval reported beside each; H7's model carries an intercept for the class within its chain; the refits run on several cores, the resamples drawn first so the result does not depend on how many | §5, §7, `analyse.R` (`boot_irr`, `cluster_boot`, `fit7`), `report.py`, `selftest.R` | Decided by the author on 22 November 2026, on the review: the rows of a chain are not independent (problems in one class share its later changes; H2's two records of a row share its arrivals; one class is changed by many units), which §7 already said made the intervals too narrow. No direction or threshold changes |
| 75 | A sensitivity reading of H3: its rule over its six measures with the method's fan-out and the class's CBO, RFC and fan-out put back, each alone; reported with its state, changing no verdict | §2, `prepare.H3_SENSITIVITY`, `analyse.R` (`H3_with_coupling`), `verdict.h3_with_coupling`, `report.py` | Decided by the author on 22 November 2026, on the review: fan-out left H3 after it was seen above the margin on the development chain (§7), and the literature counts coupling among its structural metrics |
| 76 | Run D's test is registered: H8, without encapsulation code disperses. Run D against Run A's `angular-spring`: bound code come back to less at the class (below 1) and more calls and field reads added across class boundaries at the same change size (above 1), each on the cluster bootstrap, p the larger; conditions, compliance (at least 90% of introduced members not private) and the amount in its band; α = 0.05 on its own p, on its own run. Run after the others, not beside Run A | §2, §3.1a, §5, §7, `analyse.R` (`coupled_arm`), `prepare.compliance`, `verdict.h8`, `report.h8_section`; an analysis with `contrast: no-encapsulation` in `runs.yaml`, added with its run ids by dated amendment | Decided by the author on 22 November 2026, on the review: forced against unforced is not assigned by anyone, and Run D is where the cause is changed by hand. The author cannot run it concurrently and accepts that. Its code is tested on fixtures and on simulated data; it has not been run end to end, as no such run exists |
| 77 | H2 also needs the arm contrast: a core value is come back to less in the function arm than in the methods arm, the rate ratio below 1 on the cluster bootstrap, at each level where each arm has at least 10 core records (a rank-sum over chains where the function arm's cores are never come back to); H2's p the largest of its parts. Until then reported beside H4. Not read on a history | §2, §5, `analyse.R` (`reuse`, `H2$reuse_*`), `verdict.h2`, `report.reuse_test_lines`, `selftest.R` | Decided by the author on 22 November 2026, on the review: within one arm a value already used is likely to be used again whatever the place, so the ratio of core to periphery could hardly fail; the arms solve the same problems, so the contrast between them is what the place adds. Made knowing the development chain (0.088 [0.024, 0.316] at the method; at the class the function arm had one core row). Before the tag, so a revision |
| 78 | H4 also needs fewer existing files gone back into per checkpoint, production Java and wiring counted alike, bound or not: the function arm's rate ratio below 1 on the cluster bootstrap, in H4's p with the other four | §2, §5, `chain.measure` (`java_existing`), `tables.addition_rows`, `prepare.reopen_rows`, `analyse.R` (`H4$existing_files`), `verdict.h4`, `report.existing_files_lines`, `selftest.R`; `MEASURE_VERSION` 29 | Decided by the author on 22 November 2026, on the review: H4's intrusion counted the methods arm's return to its handler and not the function arm's return to its wiring, and rested on the rule that an injected parameter is not a binding. Made knowing the development chain's reopening counts (1.35 [1.01, 1.80] against H4 before the binding rule, classes only; 0.77 [0.52, 1.16] with the rule and the wiring files, §6), so H4 may well fail on it. Before the tag, so a revision |
| 79 | The instrument checked against the compiler on corpus A: on every fifth checkpoint of a chain and its last, the precision and recall of its calls and field reads and the precision of its bound names, against javac's resolution; reported per arm, no threshold | §4.8, §7, `instrument/Check.java`, `placement_gravity/validate.py`, `measure.py` (`validation.csv`), `prepare.py`, `report.validation_section`, `setup.sh`, `tests/test_validate.py` | Decided by the author on 22 November 2026, on the review: the fixtures show the instrument does what was meant, not that it is right on real code. No measure of a hypothesis, model or rule changes |
| 80 | **A fault, found by the check of row 79 before any run named for analysis was read:** a call was followed to every class sharing any ancestor with its receiver's class (siblings, and through a library's interface whole groups of unrelated classes), not only to that class's ancestors and descendants as §4.2a says. Corrected in `flow.Graph.family`. It inflated the calls counted between classes (about twofold on the two development trees looked at) and widened the control flow of H5's method level | §4.2a, §4.8, `flow.py`; `MEASURE_VERSION` 29, `HISTORY_VERSION` 13 | The figures of §6 for H5 at the method, H6's pairs and accountings, H7, surface and ripple were computed with it; they are development figures, superseded by the rerun. No rule changes: the code now does what the plan said |
| 81 | A reported reading, logic and organisation: each checkpoint's added code as logic, organisation in bodies, declarations, imports and wiring, with the state handed along; stated before any run is read: the logic the same in both arms (inside 0.8 to 1.25), the state handed along lower and flatter in the function arm; no direction for declarations or wiring. Brooks's essence and accident as its framing, with the drafter's cautions | §1, §4.9, `chain.lines_added`, `tables.organisation_split`, `prepare.split_rows`, `prepare.split_summary`, `analyse.R` (`split`), `report.split_section`, `selftest.R`; `MEASURE_VERSION` 30 | The author's, 22 November 2026: "the essential complexity is the logic contained in those methods. The method organisation is just to supply data to the logic of the methods. OfficeFloor removes this accidental complexity". Operational form the drafter's. No hypothesis, model of a hypothesis or rule changes. Made knowing the development chain's amount (1.08) and that H4's symmetric file count had just gone against H4 there (§6) |
| 82 | H4's symmetric count is how well-trodden the files gone back into were: for each existing file a checkpoint changed, Java and wiring alike, the earlier checkpoints that had created or changed it, summed; a negative binomial model, the function arm's ratio below 1 on the cluster bootstrap. The plain number of existing files (row 78 as first built) is reported | §2, §5, §7, `chain.measure` (`java_changed`), `tables.trodden`, `prepare.reopen_rows`, `analyse.R` (`H4$trodden`, `reported$existing_files`), `verdict.h4`, `report.existing_files_lines`, `selftest.R`; `MEASURE_VERSION` 31 | Decided by the author on 22 November 2026 on the drafter's proposal, **after the plain count went against H4 on the development chain** (1.50 [1.16, 1.94]) and the chain's files had been looked at: OfficeFloor makes a new file a checkpoint and goes back into 49 files a few times each, Spring into one file at 43 of 59 checkpoints; a count of files scores dispersion, which the plan does not hold to be bad. Seen before it was built, in scratch and counting changes only: 12.1 a checkpoint in OfficeFloor against 21.9 in Spring. Before the tag, so a revision |
| 83 | In the logic and organisation reading the parameters of new wired functions (injected, declared) are counted apart from those of new called methods with logic (handed by a caller); the stated direction for the state handed along is on the called methods' parameters and the values callers pass | §4.9, §7, `tables.organisation_split`, `prepare.SPLIT`, `analyse.R`, `report.split_section`, `selftest.R`; `MEASURE_VERSION` 31 | Decided by the author on 22 November 2026 on the drafter's proposal, **after the parameters of all new methods went against the stated direction on the development chain** (1.38 [1.06, 1.78]). Seen before it was built, in scratch: the arms wrote the same number of new called methods with logic (80 and 81), with 85 parameters in OfficeFloor and 100 in Spring; OfficeFloor's 35 wired functions carried 1.9 injected parameters each. A reported reading; no verdict depends on it |
| 84 | On a history the cluster bootstrap has 200 refits, not 1,000; the Wald interval beside each as before | §5, `prepare.BOOT_HISTORY` | Decided by the author on 22 November 2026, after one fit was timed at the sizes expected: corpus B at 1,000 refits would take weeks. Corpora B and C are direction and interval only. No direction, threshold or model changes |
| 85 | In the logic and organisation reading, where the logic landed: methods that existed, new called methods, new wired functions, with the number of each; no direction stated | §4.9, `tables.organisation_split`, `prepare.SPLIT`, `analyse.R`, `report.split_section`; `MEASURE_VERSION` 32 | The author's question on 22 November 2026, why the parameters of called methods rose in the function arm and fell in the methods arm on the development chain. Seen in scratch before it was built (§6): the function arm's new wired functions fell from 0.95 to 0.20 a checkpoint over the thirds as its new called methods and edits of existing methods rose. A reported reading; no verdict depends on it |
| 86 | A tripwire on the compiler check: the report says *read with care*, at the check and at H7, where a share of the instrument's calls is below 0.90 in an arm or differs between the arms by more than 0.05; nothing fails by it | §4.8, `validate.flags`, `prepare.py` (`validation_flags`), `report.py`, `tests/test_validate.py` | Decided by the author on 23 November 2026, between no pass mark and a pass mark set after the development chain had been seen: the plan should say beforehand what is done if a run comes back much worse. The two figures are the drafter's. No measure, model or verdict changes |
| 87 | A nested class's use of a member of a class around it is followed: `Outer.this.field`, `Outer.this.method()`, and a field or a method of an enclosing class used by its bare name where the callable and its own class declare none of that name. The compiler's reader corrected likewise. The bindings are unchanged | §4.8, `Pull.java` VERSION 16 (`reads`, `calls`, `enclosingTypes`, `outerThis`), `Check.java`, `tests/test_validate.py`; `MEASURE_VERSION` 33, `HISTORY_VERSION` 14 | A gap the check of row 79 found (field reads recalled 7 of 19 and 0 of 12 on the development chain) and the same blind spot for calls, seen on reading the code. Decided by the author on 23 November 2026 on the drafter's recommendation, which had first been to leave it: it is one line on corpus A, but inner classes using the class around them are common in the people's Java of corpus B, where the compiler cannot check. No rule changes; before the tag, so a revision |
| 88 | Where forced coupling came from: contained, problem or reuse, other, per forced class row and per call (a reported reading). H6's coupling of pairs on the index refitted without the chain's intercept where its standard error is not computed | §4.2c, `prepare.coupling_source`, `report.h7_section`, `analyse.R` (`H6_pair_coupling`), `tests/test_analysis.py` | The author's reading of H7 on the development histories at `HISTORY_VERSION` 14, 23 November 2026 ("coupling is increasing only due to the problem, much like shape of solution does not describe the problem"), drafted as three sources the author named: no added coupling, coupling that joins two classes whose data the change needed, coupling through what was already exposed. The refit: at `HISTORY_VERSION` 14 the pairs model's standard error was not computed with two chains, and the author chose the fallback H3's class measures already use. No measure, table or verdict changes |
| 89 | **H7 restated: surface against volume.** Per checkpoint, the links between blocks of logic it added (call links, state links to its own class's and other classes' fields that hold state, and the wiring's flow links; each counted once; an injected dependency not a link in either arm) against the logic it added: the function arm's rate ratio half-way through, for the same logic, below 1, **and** its interaction with the checkpoint index below 1 (as H4, both from one cluster bootstrap; p the larger). Not testable on a history. Confirmatory, in the Holm family in place of *forced changes couple*, which is retired and reported without a verdict (its arm contrast stays H8's) | §2, §4.2c, §5, §7, §8, `Pull.java` VERSION 17 (`own`, `state`), `chain.parse_wiring` (`links`), `flow.Graph.links`, `tables.link_rows`, `measure.py` (`links.csv`), `prepare.h7_rows`, `prepare.links_summary`, `prepare.forced_coupling_rows` (`forced_coupling.csv`), `analyse.R` (`H7`, `boot_irrs`; the old model as `reported$H7_retired_forced`), `verdict.h7`, `report.h7_section`, `selftest.R`, `tests/`; `MEASURE_VERSION` 34 | The author's, 24 November 2026 (§8): volume is encapsulated complexity, surface is coupling; the calling structure is accidental, the blocks of logic essential; injection is not surface; "make similar to H4"; links counted, not weighed. **Made after the development chain's outer surface (§4.2e: 0.73 and 0.78 across classes, 0.82 and 0.85 within a growing class) and its logic and organisation reading (§4.9) had been seen**; the links themselves had not been measured. Before the tag, so a revision |
| 90 | **The old H7, *forced changes couple*, deleted**: its model, its reported ratios (forced by binding, without size, opened, outward, inward, members opened, rise, the function arm's, the arms'), the per-arm forced and unforced summary and its report section. Kept: its measure, the calls across the encapsulation (§4.2c), now `calls_across.csv`, because H8's *dispersion stronger* is the arms' contrast on it (the model kept in `analyse.R` as H8's alone); and the reading of where forced coupling came from (row 88), now a reading of that measure | §2, §4.2c, §5, §7, §8, `prepare.calls_across_rows` (was `forced_coupling_rows`; `encapsulation_summary` removed), `analyse.R`, `selftest.R`, `report.py` (`coupling_source_section`), `verdict.py`, `tests/` | The author, 24 November 2026: "Delete the old H7", after row 89. No other test changes |
| 91 | §1 *The overview*: the author's account of the whole study (blocks of code essential; growth, concentration, separation and coupling; method structure the accident; function injection disperses without it), read against the hypotheses; and the author's claim that a function is easier to split and to review alone for cohesion, recorded in §1 and as the answer to H7's threat in §7. No measure, model or rule changes | §1, §7 | The author's, 24 November 2026 ("add the overview to §1"; the splitting claim given the same day). The drafter's addition: H7 counts links, not how tight they are, so it does not credit the function arm's looser control flow |
| 92 | H5's arm contrast: per checkpoint, the placements forced at the class (bound there with no other place to go) fewer in the function arm half-way through **and** rising less over the stream (the arm term and its interaction with the index, both below 1, one cluster bootstrap), beside the methods arm's fall; p the largest of the three. Not read on a history | §2, §5, §8, `prepare.h5_forced_rows` (`h5_forced.csv`), `analyse.R` (`H5$contrast`; `boot_irrs` moved to the helpers), `verdict.h5`, `report.h5_section`, `selftest.R`, `tests/test_analysis.py` | The author's, 24 November 2026: "make H5 an arm contrast"; "it also potentially shows the accidental cost of the method structure in Spring handlers (and typical web app servers) over function injection of OfficeFloor". The form chosen from three, **after the development chain's H5 figures by arm had been seen** (the function arm 10 class rows in 60 checkpoints, 9 forced; the methods arm 48 in 59, 26 forced). Before the tag, so a revision |
| 93 | **The hypotheses renumbered in the order of the story**: old H5 → H1, H2 → H2, H1 → H3, H4 → H4, H7 → H5, H3 → H6, H6 → H7, H8 → H8 (the table at the head of this section). H3 renamed *the encapsulation fills*. §1 to §5 and §7, the code, the tests, `README.md` and `LITERATURE.md` take the new numbers; §6, §8 and §9 keep those of their time; the figure keeps the old. The report lists the hypotheses H1 to H7 in order | throughout; `verdict.py` (the confirmatory family H1, H2, H4, H5; secondary H3, H6, H7), `analyse.R` and `selftest.R` (`res$H*`, the data files `h*.csv`), `prepare.py`, `report.py`, `tests/` | The author, 24 November 2026: "change the ordering of the HX to match the story order of what we are discovering". No test, measure, model or rule changes; only names. The results in `results/analysis/` keep the old numbers until they are made again |
| 94 | A reported reading beside H5: the call links a checkpoint added, split by caller (a wired function, a public method of a class the wiring declares, or any other method) and by whether the callee is in the caller's class; per arm and, for calls from other methods, over the thirds. No direction stated; no test changes | §4.2c, §6, `tables.link_rows`, `prepare.h5_rows`, `prepare.links_summary`, `report.h5_section`, `tests/`; `MEASURE_VERSION` 35 | The author's, 24 November 2026 ("add the breakdown"), **after H5 had gone against the form on the development chain** (§6): the drafter proposed it to see whether the function arm's calls come from the helper methods the agent wrote inside functions, which the author holds can be split out again (§1). H5's test is unchanged |
| 95 | **H5's links weighed**: a call 1 + 1 per parameter + 1 if it returns a value; a state link 1; a wiring edge 1 + 1 if it carries a value (a `next:` from a function that returns one, an output whose flow takes an argument); injection weighs nothing. H5's test (its shape unchanged) is read on the weight added; the plain count, the test until then, is reported beside | §2, §4.2c, §5, §8, `Pull.java` VERSION 18 (`returns`, `flows`), `chain.parse_wiring` (`link_from`), `flow.Graph.call_weight`, `flow.Graph.flow_weight`, `tables.link_rows`, `prepare.h5_rows`, `prepare.links_summary`, `analyse.R` (`weight_added`; `reported$H5_unweighted`), `selftest.R`, `report.h5_section`, `tests/`; `MEASURE_VERSION` 36 | The author's, 24 November 2026: "a method call is calculated as 1 for the call, +1 for every parameter, +1 if has return type. Then the wiring for function injection is just 1". **Made after H5 had gone against the function arm on the development chain** (1.25 [1.06, 1.47] times the links for the same logic, §6) and after the author had seen that the excess was the wiring between OfficeFloor's more numerous classes and methods. The +1 for an edge carrying a value is the drafter's, chosen by the author. The drafter's note, in §2: OfficeFloor's data passes mostly through injected values, which weigh nothing, so the weights credit the form exactly where the author's claim is. Before the tag, so a revision |
| 96 | Confirmed: a call made on an injected object (a repository, a mapper, a store handed to a function or held in a Spring field the container fills) is a call link, weighed as any call; receiving the injected object is not surface | §4.2c, §8 | The author, 24 November 2026: "keep it counted", after the drafter laid out both readings. It had been the drafter's reading since row 89. **Decided after the development chain had been seen** (§6: many of the function arm's 3.34 call links a checkpoint across classes are such calls, and Spring has the same kind), on the principle that injection removes the finding of the target, not the call. No code changes |
| 97 | The forces map redrawn: the numbering of row 93; H1 the force with the function arm forced less; H3 *encapsulation fills*; the dispersing branch now *coordinate*, its cost H5 surface against volume (weighed links per unit of logic); H8 Run D as a box that removes encapsulation; the confirmatory four named; a label that ran past its box shortened | §2, `figures/placement-forces.svg` | The author, 24 November 2026: "redraw the forces-map figure with the new numbering". A drawing only |
| 98 | A reported reading, a filled ball or pebbles: per checkpoint each container of blocks of logic (every class; in the function arm also each wiring flow file) with its blocks (methods), volume, largest block's share, Gini, internal and external links, and whether it is a concentration; per arm and kind, the concentrations, the rest and all, at the end and by the growth exponent of blocks on volume within a container. No direction stated; no verdict depends on it | §4.2g, §8, `tables.container_rows`, `measure.py` (`containers.csv`), `prepare.container_summary`, `report.containers_section`, `tests/`; `MEASURE_VERSION` 37 | The author's, 25 November 2026: "I'm thinking more that we need the number of blocks of code (methods). Need to determine if dealing with a filled ball or is it full of smaller pebbles". The classes, the containers and no expectation chosen by the author from the drafter's options. Not yet computed on any chain |
| 99 | H5's weights: an edge whose function or flow interface is not found in the function's own file still weighs 1, and the number of such edges is now counted and reported (`Pull --places` `flows` gives -1 for an interface not found, VERSION 19) | §4.2c, `Pull.java`, `flow.Graph.flow_resolved`, `tables.link_rows` (`flow_unresolved_added`), `prepare.links_summary`, `report.h5_section`, `tests/`; `MEASURE_VERSION` 38 | Decided by the author on 25 November 2026 (walk-through, item 3): a weight missed this way would favour the function arm unseen. On the development chain every interface was nested; no figure changes there |
| 100 | A reported reading beside H2, the sinew shape: per place, each value's uses, the combinations used together, and the effective number of values (inverse Simpson) over a place's uses and over the thirds of the stream; the most used values and combinations by name. No direction stated | §5, `readings.sinew_shape`, `readings.effective_number`, `prepare.py`, `report.sinew_lines`, `tests/` | The author's, 25 November 2026: "I would however be interested in seeing the sinew shape as reported. In other words, how often each value is used. How often are the combinations used. And is there a trend to number of values that would be considered the sinew core". The effective number chosen by the author over a share cut-off. Not yet computed on any chain |
| 101 | The drafter's remaining choices settled by the author, one at a time (§8, 25 November 2026): H1's no-ops left out and its Poisson fallback; the edge count (row 99); the containers' pooled exponent; H2's per-placement core; the reader reading's bands and its two display rules. No rule changes beyond rows 99 and 100 | §8 | The author's answers to the drafter's walk-through |
| 102 | **A fault, found on 25 November 2026 before any run named for analysis was read:** the cache of call graphs (`tables._graph`) was keyed by a tree's id without holding the tree, so once a chain's trees were freed, a later chain or repository measured in the same process could be handed an earlier one's graph for a tree whose id had been reused. Corrected: the tree is kept with its graph. It may have touched every figure built on the call graph (H1 at the method, H7's pairs, H5's links, the calls across the encapsulation, surface, ripple, containers) for the second chain or repository of a process since row 54; the bindings, from the instrument, were not | `tables._graph`, `tests/test_stream.py`; `MEASURE_VERSION` 39, `HISTORY_VERSION` 15 | Found while testing row 103, when a new test was handed an earlier test's graph. No rule changes: the code now does what the plan said. Whether the development figures moved is to be read from the rerun (§6) |
| 103 | The flow containers of the ball-or-pebbles reading (row 98) are named by their wiring file, not by the classes in them, so a flow that gains a function stays one container (`chain.flows` gives the files, `flow_files` in the tree index) | §4.2g, `chain.flows`, `chain.tree_places`, `flow.Graph`, `tables.container_rows`, `tests/`; `MEASURE_VERSION` 39 | Found on reading the reading's first figures (§6): every flow's growth exponent was near 0 because a flow that grew became a new container. A fault, not a choice |
| 104 | Stated, not yet built: a reported reading, **the cost to fix a concentration**: per container of §4.2g, the fewest internal links (calls between its blocks, blocks sharing a field holding state) a cut must cross to split it into two parts of at least a quarter of its volume each; the direction stated, cheaper in OfficeFloor than in Spring at the same size and the gap widening as concentrations grow. To be built before the tag. Corpus B by issue, landing ranks on a history and what unbound code leaves behind left as exploratory, after the experiment | §2, §4.2h, §8 | The author's, 25 November 2026: "fixing in OfficeFloor is simple when concentration gets high. It is potentially a rewrite in Spring if this happens"; "write the direction now". Stated after the development chain had been seen (H5's drift, §6) and before any ui run is read; the measure is the drafter's, accepted by the author |
| 105 | **H9, the cost to fix a concentration**, a secondary hypothesis: per class of two or more blocks at the end of each chain, its cheapest split (the fewest internal calls and shared-field links a cut must cross to leave at least a quarter of its volume on each side; exact up to 14 blocks, a seeded local search above, recorded); at the same size the function arm's below the methods arm's, and the gap widening with size (arm × log size), both below 1 on one cluster bootstrap, p the larger, on its own p at α = 0.05. Classes no split of which leaves a quarter on each side are left out and counted. The concentrations alone reported beside | §2, §4.2h, §5, §8, `tables.split_cost`, `tables.container_rows`, `prepare.h9_rows`, `prepare.h9_summary`, `analyse.R` (`H9`), `verdict.h9` (`SECONDARY`), `report.h9_section`, `selftest.R`, `tests/`, `README.md`; `MEASURE_VERSION` 40 | The author's, 25 November 2026: "write the code for concentration and make it a H9". The direction was stated before the ui runs (row 104); the test's population (every class of two or more blocks rather than the concentrations alone) is the drafter's, to be confirmed. Not yet computed on any chain |
| 106 | The containers' growth exponent resampled in a fixed order: its intervals had followed the order of a Python set, drawn afresh on each run, so they differed run to run (the exponents did not) | `prepare.container_summary`, `tests/test_analysis.py` | Found on comparing the development rerun with the run before it (§6). A fault, not a choice |
| 107 | **H1 restated: the force, forced less with function injection.** Per checkpoint, the placements forced at the class fewer in the function arm half-way through **and** rising less over the stream (the arm term and its interaction with the index, both below 1 on one cluster bootstrap, p the larger; reversed if the arm term lies wholly above 1); not testable on a history. **Choice narrows** (the methods arm's alternatives at the class falling, H1's test since 19 November 2026, with the contrast since row 92) is reported, at the class and the method, on corpus A and the histories | §2, §5, §7, §8, `verdict.h1`, `report.h1_section`, `tests/`, the figure | The consistency review of 25 November 2026 (§8): where every methods-arm placement is forced from the start, choice narrows cannot be tested and the code dropped H1 whole, contrast and all. The author: "this just needs to be OfficeFloor is forced less especially over time"; level and trend both needed (chosen from the drafter's options). Seen: the development chain's contrast, 0.25 [0.09, 0.65] at the level, the trend not readable on one chain an arm (§6) |
| 108 | **H9 deleted**, with its measure (§4.2h, the cheapest split) and its code: `tables.split_cost`, the split columns of `containers.csv`, `prepare.h9_rows`, `prepare.h9_summary`, `analyse.R` (`H9`), `verdict.h9`, `report.h9_section`, its self-test and tests. The secondary hypotheses are H3, H6 and H7 again | §2, §4.2h, §5, §8, the code named, `README.md` | The author, 25 November 2026, asked which classes H9 should be tested on: "I'm now questioning H9 and its value. Why did we introduce it? As it is only looking at cutting up methods ... with the various implementation ways"; then "delete it". Seen: the development chain's H9, 1.10 [0.68, 1.79], no difference (§6) |
| 109 | **A constant's use is a state link in H5**, weight 1, of its own class or another (by class name; a static import is not followed); counted apart (`constant_links_*`, `constant_weight_added`) and in the totals. Reported beside: H5 without them (`weight_added_without_constants`, the test until then) | §2, §4.2c, §5, `flow.Graph.links` (`constant`), `tables.link_rows`, `prepare.h5_rows`, `prepare.links_summary`, `analyse.R` (`H5_without_constants`, `H5_kinds`), `report.h5_section`, `selftest.R`, `tests/`; `MEASURE_VERSION` 41 | The author, 25 November 2026, on hearing that constants were left out by the drafter's choice and never put to the author: "count constants in H5". The drafter had recommended keeping them out (a constant needs no coordination between blocks). Seen: the development chain's H5 without constants (§6); not yet measured with them |
| 110 | Wording, no rule changed: §5's bootstrap paragraph (H6, H7 and the readings on Wald intervals; H3 on the bootstrap); §4.2c leads with the weights; the tiers paragraph names the readings §4.2b–4.2g and the sinew shape; the sinew shape counts a class's private constants, as H2's core does; the docstrings of `verdict.py` and `prepare.h5_rows` | §2, §4.2c, §5, `verdict.py`, `prepare.py`, `analyse.R` | The consistency review of 25 November 2026 (§8) |
| 111 | The steps fetch every input themselves and each prints the next command: the problem streams are cloned from their remotes at their pinned refs where missing (`runs.ensure_at`; `remote:` in `runs.yaml`); corpus B's first set, drawn by `long-method-slim-study`, is copied by step 2b from that repository at its pinned commit `1dc68ac` into `samples/open-source-human/`, not read from wherever a copy lies (`history.fetch_csv`); every step script ends with `placement_gravity.nextstep`. No value read changes: the file at that commit is the file that was read | `runs.yaml`, `runs.py`, `history.py`, `nextstep.py`, the step scripts, `README.md`, `tests/` | The author, 25 November 2026: "Is everything scripted in the stepX_... scripts? All values should be generated by the scripts. Also, each script should output the command to run the next script" |
| 112 | **Every figure the plan quotes is made by a step.** An audit of the session transcripts (25 November 2026) found about sixty figures in §2, §4.4, §5 and §6 first read by one-off queries, not printed by any report: they are now made by step 5's diagnostics (`placement_gravity/diagnostics.py`; `DIAGNOSTICS.md` and `diagnostics.json` beside each report), each passage marked with the section that makes it. For them step 3 writes two tables more (`files.csv`, every file a checkpoint created, changed or deleted, with the earlier checkpoints that had changed it; `files_end.csv`, the Java files at the head and their sizes); step 4 records its time (`timing.json`) and fits size or data within each arm alone (`size_or_data_*.by_arm`); the timings of one fit by data size are made by a new optional step, `step1b_timing.sh` (`analysis/timing.R`, `results/timing.json`). No test, rule or verdict changes. The diagnostics read the tables as they now stand, so where §6 recorded a figure on an earlier `MEASURE_VERSION` the two may differ; §6 keeps what was seen | §2, §4.4, §5, §6, `diagnostics.py`, `tables.file_rows`, `measure.py`, `analyse.py`, `analyse.R`, `analysis/timing.R`, `step1b_timing.sh`, `step5_report.sh`, `nextstep.py`, `README.md`, `tests/`; `MEASURE_VERSION` 42 | The author, 25 November 2026: "All values should be generated by the scripts"; asked how far to go, "script all 17" |
| 30 | Terms: a *tie* is now a **binding**, and code that was *tied* to a place is **bound** to it; the *equivalence bound* is now the **equivalence margin** | throughout, and every table and column name | The author's choice: "tie" reads as a draw. "Coupling" was not used because the plan already uses it for the wider thing (the problem's own coupling, the wiring). The margin was renamed so that "bound" has one meaning. No measure, model or rule changes. The pilot report (`results/pilot/PILOT.md`) keeps the old word |

The direction of H4, the thresholds, the margin's values, the amount band, the wiring
conditions, the runs read and the Holm correction over four hypotheses are unchanged. The author
confirmed row 22 on 17 November 2026: H4's condition is the arm's rate ratio in intrusion, and the
count of places reopened is reported.

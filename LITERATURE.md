# Literature notes for the placement-gravity plan

Searched 15 November 2026. Each entry was checked against an index record (DOI, DBLP or
publisher). Where only a secondary source was found, it says so. **Check before quoting** marks
items whose exact wording or figures were not read in the full text.

## 1. The amount is the problem's: essential complexity and conservation

- **Brooks (1987)** separates essential complexity (the problem's) from accidental complexity
  (the implementation's). This is the root of "the problem fixes the amount".
- **Moseley and Marks (2006)** accept the split but argue that most complexity in practice is
  accidental, mainly state, and should be isolated from the essential logic. Their essential and
  accidental *state* is close to this plan's distinction between values the problem needs and
  values the host imposes.
- **Tesler's law of conservation of complexity** (mid-1980s, Xerox PARC/Apple): every application
  has an irreducible amount of complexity, and the only question is who handles it. It is a
  folk law from interaction design. Its usual citation is an interview in Saffer (2010), and no
  primary paper by Tesler was found. It is a precedent for *conserved amount* in spirit only;
  cite it as such. **Check before quoting.**
- **Lehman (1980)**, the law of increasing complexity: an evolving system's complexity rises
  unless work is done to reduce it. H1 is a mechanism for this law: forced placement compounds.
- **Eick et al. (2001)**, code decay: the *span* of changes (files touched per change) increases
  over time in a 15-year telephone-switch system. This is the closest empirical result to
  "growth makes later changes spread"; it is measured on files, not on placement.

## 2. Size confounds structure: why shape on its own was not enough

- **El Emam et al. (2001):** once class size is controlled, the apparent validity of
  object-oriented metrics for fault-proneness largely disappears. Evanco (2003) disputes whether
  size is a confounder in the statistical sense. Either way, a structural measure must be read
  against size.
- **Chowdhury, Holmes, Zaidman and Kazman (2022b):** over about 730K Java methods, much of the
  value of popular method-level metrics for change-proneness is explained by their correlation
  with size.
- **Chowdhury, Uddin and Holmes (2022a):** maintainable method size in Java; methods under about
  24 lines are less change- and bug-prone, and splitting larger methods helps.
- **Khomh et al. (2012):** classes in antipatterns are more change- and fault-prone, and size
  alone does not explain it. This is a counterweight: structure adds something beyond size.
  The plan's position is that it adds something about placement, not about shape.
- **Vaucher et al. (2009):** tracking a class's "godliness" over time separates god classes
  that are large *by design* from those large *by accident*. This is the nearest precedent for
  reading a unit's history rather than its snapshot, and for the problem-dictated size the plan
  assumes.

## 3. How code grows, and where new code lands

- **Steidl and Deissenboeck (2015):** in nine open-source and one industrial Java system, about
  half of all methods never change after their first commit. Systems grow mainly by adding
  methods, not by lengthening them. Very long methods (over 75 statements) are changed 6–18 times
  on average, and only 10–20% are ever significantly shortened (the last figures are from the
  authors' company blog). This sets Q1's baseline: most additions are new units, so the question
  is what happens to the minority that lands in existing hosts, and whether that minority grows
  as hosts grow.
- **Tufano et al. (2015):** over 200 projects, smells are mostly present from a unit's creation,
  not acquired gradually, and deadline pressure is a common cause. This threatens H1's accretion
  story and is why the plan also measures pull at creation (§4.3, new methods taking existing
  state as parameters).
- **Chowdhury (2025):** highly change-prone methods can be predicted at their inception from
  static metrics. This agrees with Tufano: much is decided when a unit is born.
- **Vasa et al. (2009):** Gini coefficients of software metrics are high and stay fairly stable
  as projects evolve. This gives the measure of concentration (§4.2), and a caution: system-wide
  concentration may not move even when local gravity does.
- **Power laws and preferential attachment:** Wheeldon and Counsell (2003) find power laws in
  class relationships; Concas et al. (2007) in a large object-oriented system. Work on dependency
  networks suggests skewed degrees arise from both preferential attachment and heterogeneous
  initial degrees (search snippets only; **check before quoting**). Gravity would be a
  preferential-attachment mechanism at the level of placement. No study was found that tests
  whether *new code* (rather than new dependencies) attaches preferentially to large hosts.
  **This looks like an open gap.**
- **No empirical study using "gravity" was found.** The term appears only in practitioner essays.
  The plan defines it operationally (pull), and should not suggest an existing construct.

## 4. Concentration against dispersion: change coupling, scattering and ripples

- **Parnas (1972):** decompose by what is likely to change, and hide each such decision in one
  module. This is the criterion behind "concentrate what changes together", and the reason
  neither concentration nor dispersion is good in itself.
- **Stevens, Myers and Constantine (1974):** coupling and cohesion as design criteria, with
  ordered types of coupling. Common coupling (shared global state) is what a long method's shared
  locals amount to at small scale, and what pull counts.
- **Martin (2003):** the Common Closure Principle (classes that change together belong together)
  and the Single Responsibility Principle (one reason to change). This is the practitioner
  statement of the trade-off H2 tests.
- **Fowler (1999):** the smells *Divergent Change* (one unit changed for many reasons:
  concentration gone wrong) and *Shotgun Surgery* (one reason changes many units: dispersion gone
  wrong). They are the two failure directions of placement.
- **Palomba et al. (2015), HIST:** detects Divergent Change and Shotgun Surgery from co-change
  history, with 72–86% precision. It measures placement failure after the fact. The plan's pull
  is measured at the moment of placement.
- **Gall, Hajek and Jazayeri (1998):** logical coupling, i.e. modules that change together in
  release history, reveals dependencies the code does not show.
- **Zimmermann et al. (2005), ROSE:** association rules on co-changes predict related changes
  (a correct location in the top three over 70% of the time).
- **Hassan and Holt (2004):** heuristics for predicting change propagation, validated on five
  systems.
- **D'Ambros, Lanza and Robbes (2009):** change coupling correlates with defects and improves
  bug prediction.
- **Yau and Collofello (1980):** stability as a program's resistance to the ripple effect of a
  modification, with module- and program-level measures. The original "ripple" measure. The
  plan's containment and intrusion are history-based versions of it.
- **Eaddy et al. (2008):** the degree of scattering of a concern correlates moderately to
  strongly with defects in three case studies. They defined scattering and tangling measures
  (DOSC, DOTC). This is the closest precedent for measuring the dispersion of *one concern*. It
  needs concerns mapped to code by hand; the plan uses the change request as the concern.
- **Tarr et al. (1999):** separating concerns along a single dimension forces other concerns to
  scatter and tangle: the "tyranny of the dominant decomposition" (**check the exact wording**).
  That is gravity at the level of language design: the dominant decomposition fixes where new
  concerns may go. Function injection can be read as weakening one such dominant decomposition,
  the call stack.
- **Kiczales et al. (1997):** aspect-oriented programming, the other well-known attempt to free
  placement of cross-cutting concerns.

## 5. Modularity as option value: why keeping placement open is worth something

- **Simon (1962):** near-decomposability. Complex systems that survive are hierarchies of
  subsystems with strong internal and weak external interactions.
- **Baldwin and Clark (2000):** design rules and modularity as **real options**. A modular
  design is worth more because each module can be substituted independently.
- **Sullivan, Griswold, Cai and Hallen (2001):** apply Baldwin and Clark to software with design
  structure matrices and option values. Their analysis agrees with Parnas's conclusions on KWIC.
  **This is the theoretical home for "plasticity"**: plasticity is the option to re-place, and
  gravity destroys that option.
- **Mo, Cai, Kazman, Xiao and Feng (2016):** Decoupling Level, an architecture metric derived
  from option theory, measured on 108 open-source and 21 industrial projects. It measures how far
  a system decomposes into small, independently replaceable modules. It is a snapshot measure of
  option value; the plan measures its loss, change by change.
- **Mo, Cai, Kazman and Xiao (2015):** hotspot patterns (e.g. Unstable Interface, Implicit
  Cross-module Dependency) combining design-rule theory with history; they locate the most
  error- and change-prone files.

## 6. Placement beyond contiguity: slicing and non-contiguous extraction

These supply the formal side of "dependency-valid placements that the method form forbids", the
N_dep against N_method idea in the conversation that led to this plan.

- **Weiser (1984):** program slicing.
- **Komondoor and Horwitz (2000):** the first semantics-preserving algorithm to extract an
  *arbitrary* set of statements, moving the others out of the way and duplicating predicates
  where needed.
- **Lakhotia and Deprez (1998):** "tucking", which gathers a slice's statements into a function
  (wedge, split, fold).
- **Maruyama (2001):** method extraction by block-based slicing.
- **Ettinger and Verbaere (2004); Ettinger (2007, thesis); Abadi, Ettinger and Feldman (2012):**
  slice extraction ("untangling"), sliding, and *Extract Computation* for non-contiguous code.
  These show the space of dependency-valid placements is larger than the contiguous runs that
  Extract Method (and SinewSlim's seam) allows, and give algorithms for it.

## 7. Cohesion: why the plan does not measure it

- **Briand, Daly and Wüst (1998):** a unified framework for object-oriented cohesion measures.
  They find many measures are not defined in a fully operational form, and the measures disagree.
- **Bavota et al. (2013):** developers' perception of coupling matches *semantic* coupling best.
  Structural measures do not see the meaning that decides whether two pieces belong together.
  This supports the plan's choice to assume cohesion per problem rather than measure it.

## 8. Instruments and data hygiene

- **Tsantalis, Ketkar and Dig (2022):** RefactoringMiner 2.0, refactoring detection in commit
  history. Used to separate re-placement from addition (§4.1).
- **Jodavi and Tsantalis (2022):** CodeTracker, method and variable tracking in commit history.
  Reported 99.9% precision and recall for methods. Used for provenance (§4.4).
- **Grund et al. (2021):** CodeShovel, method-level histories, the predecessor of CodeTracker.
  CodeTracker's authors found and corrected errors in its oracle.
- **Herzig and Zeller (2013); Herzig, Just and Zeller (2016):** tangled changes. Up to 15% of bug
  fixes are tangled in the 2013 paper, revised to 7–20% of bug-fix changes in the extension.
  At least 16.5% of files are wrongly linked to bug reports when tangling is ignored. This is why
  corpus B is secondary.
- **Dias et al. (2015):** untangling fine-grained changes (EpiceaUntangler; median 91% success).
- **Bird et al. (2009):** systematic bias in datasets built from commits linked to issues.
- **Silva, Tsantalis and Valente (2016):** refactoring is driven mainly by changes in
  requirements, not by smells. Extract Method serves 11 purposes, often to make a feature
  easier to add. So re-placement happens *at* the moment a new problem arrives, which matters
  for separating it from the addition.

## 9. The author's own prior work (context, not evidence)

- Sagenschneider (2026a), *Conserved amount, negotiable placement*, doi:10.5281/zenodo.23190619.
- Sagenschneider (2026b), *Complexity concentration as a god-class and god-method detector*,
  doi:10.5281/zenodo.23581333.
- Sagenschneider (2026c), *What reviewers call a Long Method is a length*,
  doi:10.5281/zenodo.23749773.
- Sagenschneider (2026d), *What extraction cannot slim, and whether function injection can*,
  doi:10.5281/zenodo.23991506.

## 10. Novelty check (systematic search, 15 November 2026)

### Protocol

1. **Citation snowballing** from five seeds, the papers nearest the study's question:
   - Sullivan et al. 2001 (option value of modularity);
   - Eaddy et al. 2008 (scattering of one concern);
   - Vaucher et al. 2009 (god by design or by accident);
   - Steidl and Deissenboeck 2015 (where method growth goes);
   - Tarr et al. 1999 (the dominant decomposition).

   Forward citations came from Semantic Scholar (2,513) and OpenAlex (1,905). Backward
   references came from OpenAlex (175), because Semantic Scholar withheld the reference lists.
   After de-duplicating by title: **2,664 unique records**.
2. **Screening.** Every record was scored on title and abstract against 13 term groups: growth,
   new code or features, placement, scattering, change propagation, god units, preferential
   attachment, option value, forcing or constraint, decay, change requests, design against
   accident. The 274 records scoring ≥ 3 were screened by title, plus a second pass over
   low-scoring titles matching growth or placement terms. About 35 were then checked by
   abstract or index record.
3. **Keyword searches** in the field's own vocabulary, since "gravity" and "plasticity" are
   this study's terms, not the literature's: where developers place new code; feature addition
   by modifying against adding methods; preferential attachment and change-proneness; change
   locality; path dependence in design; Move Method and misplaced members; extractability of
   added code at commit time; feature scattering over evolution; placement by AI coding agents
   (2025–2026). 14 searches in all.
4. **Reproducibility.** The scripts and the 274 screened records are in
   [`literature/snowball/`](literature/snowball/) (`s2.py`, `oa.py`, `screen.py`,
   `screened-top.tsv`). The raw API responses are not kept; the scripts regenerate them, so
   counts may drift as the indexes grow.

**Limits.** The snowball is one level deep. Scoring on title and abstract will miss papers that
use none of the terms. Semantic Scholar and OpenAlex both under-cover some IEEE proceedings.
Many of the Tarr citations are aspect-oriented language papers, screened out by title. **The
result is "not found by this protocol", not "does not exist".**

### What the search added: the nearest neighbours

| Work | What it does | How it differs from this study |
|---|---|---|
| Passos et al. 2015; 2018 (Linux feature scattering) | Follows *each feature's* scattering over about 8 years of the kernel. The median scattering stays constant and low; platform-driver features scatter about 2.5× more. | **The closest per-problem longitudinal study.** But a "feature" is a configuration option (`#ifdef`), not a change request; it measures where code *ended up*; it does not ask whether placement was forced. Its flat median scattering is a useful counterpoint to H1. |
| Queiroz et al. 2014; 2017 (shape of feature code) | Feature scattering follows a power law in 14 of 20 preprocessor systems; tangling does not. | Concentration as a distribution, not a mechanism. It supports the plan's choice not to use thresholds on centrality statistics. |
| Bouwers, van Deursen and Visser 2014 (encapsulation from history) | Classifies each change-set as *local* (one component) or *non-local*, and compares 12 snapshot metrics against the local ratio. | A per-change containment measure, close to §4.4's containment. It does not separate a problem's intended crossings from placement-caused ones. |
| Wong, Cai, Kim and Dalton 2011 (Clio, modularity violations) | Flags co-changes that the designed module structure does not predict. Many were later recognised or refactored by developers. | **The closest to "declared against undeclared crossings"**, but the declaration is the design structure, not the stream of requirements. It reads violations after the fact, and has no notion of forced placement. |
| Tsantalis and Chatzigeorgiou 2009 (Move Method, entity placement) | An *entity placement* metric: how well a method fits its class given the data it uses. It recommends moves that fix Feature Envy. | **The closest relative of pull.** Feature Envy is a method pulled towards *another* class's data; pull is an addition held by its *own* host's data. Theirs is a snapshot recommendation; pull asks, at the commit, whether another placement was available and at what seam. |
| Vasa, Schneider and Nierstrasz 2007 (stability of change) | Across releases of object-oriented systems, the classes modified tend to be the popular ones (by fan-in), and classes growing more complex are more likely to change. | Evidence that change concentrates where structure already is: correlational, at class level. It does not test whether new code is *forced* there. |
| Olbrich, Cruzes and Sjøberg 2010 (are all smells harmful?) | God and Brain Classes change more and hold more defects, but **less per line** once normalised by size. | Strong support for the plan's position that concentration is not bad in itself. H2 must control for size, and does (§5). |
| Yamasaki et al. 2006 (generalised preferential attachment) | Models class size as preferential growth plus an influx of new classes. | The data is pharmaceutical markets, not software. It is the right null model for "systems grow by adding new units" (Steidl and Deissenboeck 2015) combined with growth of existing units. |
| Paixão et al. 2017 (architectural awareness) | Measures each reviewed commit's change to cohesion and coupling. Reviewers discussed the architectural impact in only 38% of the 338 commits with significant impact. | Per-commit structural deltas, but no question of forced against chosen. It does suggest placement decisions are seldom deliberated. |
| Kouroshfar et al. 2015 (co-change across modules) | Co-changes that cross modules are more correlated with defects than co-changes within a module. | Supports measuring intrusion across boundaries, as the outcome in §4.4. |
| Ogenrwot and Businge 2026 (AI agent pull requests) | Agent pull requests touch fewer files, less widely distributed, than human ones of similar size. | **Agents may concentrate by default.** This is a threat to corpus A, which is agent-written. It strengthens the case for corpus B and for reading the arms only against each other. |
| "Does code cleanliness affect coding agents?" (2026, arXiv:2605.20049) | Agents repeatedly extending their own code drift towards more verbose, less structured output; cleaner starting code means fewer revisits to edited files. | Iterative growth by agents, measured as erosion, not placement. A companion to SlopCodeBench, which the degradation harness already borrows from. |

### Verdict, claim by claim

1. **Unit = the new problem, at the moment of placement.** *Partly anticipated.* Following
   individual features over time (Passos et al.), per-concern scattering (Eaddy et al.) and the
   locality of each change-set (Bouwers et al.) all exist. What they lack is a problem defined
   independently of the code (a change request) and a measurement taken at the commit where the
   problem's code lands. **Claim:** a refinement, not a first. Cite Passos and Bouwers as the
   precedents.
2. **Pull: whether the addition could have gone elsewhere.** *Not found.* Its nearest relative
   is Tsantalis and Chatzigeorgiou's entity placement, together with the extract-method
   opportunity work (variable dependencies decide what is extractable). Both are snapshot
   recommenders, not measures of whether a placement was forced at the moment it was made.
   **Claim:** new as a measure; frame it as related to Feature Envy, turned inwards and taken at
   commit time.
3. **Gravity compounds: pull rises with host size and age.** *The correlation is known; the
   mechanism is not tested.* Larger, more complex and more popular units change more (Vasa et
   al. 2007; Steidl and Deissenboeck 2015; Khomh et al. 2012). Passos et al. find per-feature
   scattering flat over 8 years. No study found tests whether *new code is held* in large hosts
   by their existing data, or whether that hold strengthens. **Claim:** new as a mechanism.
   Present H1 against Vasa (change concentrates) and Passos (scattering stays flat) as the two
   readings it must separate.
4. **Forcing, not concentration, does the harm.** *Not found as stated.* Olbrich et al. (2010)
   show concentration is not harmful per line. Clio shows unpredicted co-change marks real
   design problems. No study separates forced from chosen placement as the predictor.
   **Claim:** new. It is also the most falsifiable claim, so it carries the paper.
5. **A paired stream that declares which problems should change together.** *Not found.*
   Clio's declaration is the design; agent benchmarks grow code iteratively but do not declare
   which requirements interact or measure placement. **Claim:** new as a design for this
   question.

### What this changes in the plan

- **Cite Passos et al. and Bouwers et al.** in §1 as the per-problem and per-change precedents,
  so that claim 1 is not overstated.
- **Present pull as Feature Envy turned inwards** (Tsantalis and Chatzigeorgiou 2009), measured
  at commit time. A reviewer will look for this relation, so it should be stated first.
- **Make Olbrich et al.'s size-normalised result explicit in H2.** "Concentration alone shows no
  consistent association" is that result made confirmatory.
- **Add the agent-concentration threat** (Ogenrwot and Businge 2026) to §7 for corpus A.
- **Add Bouwers et al.'s local-change ratio** to §4.4 as a secondary containment measure, so
  the result can be compared with published systems.

All five were applied to `PLAN.md` on 15 November 2026 (§1, §2 H2, §4.3, §4.4 and §7).

### Novelty check for H1 and H2 as restated, 18 November 2026

The check above searched the vocabulary of the plan as it stood on 15 November: pull, forcing,
placement. H1 and H2 have since been restated on **bystanders** (the pre-existing values visible
where added code lands that it does not use) and on **which of those values later code is bound
to** (`PLAN.md` §2, §4.3a, §4.4), and H3 made one-sided. The verdicts on claims 3 and 4 above were
for the earlier wording. This is the same check run again for the claims as they now stand.

**Protocol, as run.**

1. **Citation snowballing** from five new seeds, the papers nearest the restated claims:
   - Tsantalis and Chatzigeorgiou 2009 (entity placement: where a method belongs, given the data
     it uses);
   - Olbrich et al. 2010 (god classes, normalised by size);
   - Vasa, Schneider and Nierstrasz 2007 (which classes change);
   - Tufano et al. 2015 (when smells are introduced);
   - Chatzigeorgiou and Manakos 2010 (how smells evolve).

   OpenAlex gave 1,244 forward citations and 174 backward references; Semantic Scholar gave 890
   forward citations, and reference lists for one seed only (27). After de-duplicating by title:
   **1,272 unique records**, 969 with an abstract.
2. **Screening.** Every record was scored on title and abstract against 13 term groups: scope and
   visibility; unused; fields and class state; parameters, locals, data clumps and constants;
   gathering and attraction; how a flaw forms; god and brain units; placement and moves; data
   coupling and field use; evolution; later change; size as a confounder; cohesion. 337 records
   scored ≥ 3. The scores were noisy (much of the forward citation of these seeds is smell
   detection by machine learning), so a second pass read the titles of all 1,272 records for the
   restated vocabulary, 94 titles, and about 20 were checked by abstract or index record.
3. **Keyword searches**, 18, in the vocabulary a reader of the restated claims would use: the
   number of variables in scope; variable span and live time; visible but unused state and the
   reading of LCOM; over-exposure and accessibility wider than needed; how god classes form;
   fields gained by classes over evolution; data clumps over time; where constants gather; cohesion
   decaying as methods are added; new code placed where its data is; an existing class against a
   new one; preferential attachment of methods to classes; field use across commits; global data
   and maintenance; size as a confounder of metrics and change-proneness; where agents place code.
4. **Reproducibility.** `literature/snowball/s2b.py`, `oa2.py`, `screen2.py` and the 337 screened
   records in `screened2-top.tsv`. The raw API responses are not kept.

**Limits.** As above: one level deep, title and abstract only, "not found by this protocol" and
not "does not exist". In addition, **most of the works below were read as abstracts or index
records, not in full**; where a finding is quoted from an abstract or a search summary this is
said. The vocabulary problem is worse here than in the first check: "bystander" is this study's
word, and what it names sits between four literatures (scope, cohesion, common coupling,
accessibility) that do not cite each other.

**The nearest neighbours.**

| Work | What it does | How it differs from the restated claims |
|---|---|---|
| Schach et al. 2002; Yu, Schach, Chen and Offutt 2004 (common coupling in the Linux kernel) | Count the instances of common coupling (modules sharing global data) over 365 versions of Linux; they grow exponentially with the version while the lines of code grow linearly (as reported in the abstract). Yu et al. categorise the coupling by definition and use. Selby et al. (2007) cite this line for *clandestine* coupling, introduced into a module without any change to it. | **The closest precedent for H1.** It is data that gathers and exposes code that did not ask for it. But it is global data between modules of C, counted per version; not the values visible at the place one addition lands, split into needed and not needed, and not followed within a class or a method. |
| Selby, Ruffell, Giesbrecht and Godfrey 2007 (global data and maintainability) | Over the releases of several large systems, files with more references to global variables have more revisions and more lines changed (a significant positive correlation). | **The closest precedent for H2 in outcome.** Data use goes with later change. It counts references a file already has, at file level; it does not ask whether later code arrives because of data that stood by, nor which values it uses. |
| Vidal, Bergel, Marcos and Díaz-Pace 2016 (over-exposed methods); Vidal, Bergel, Díaz-Pace and Marcos 2016 (over-exposed classes) | At least 20% of methods and about 25% of classes in open-source Java are declared more accessible than their use requires; 90% of over-exposed classes are so from their first version (abstracts). | **The closest relative of the bystander as an idea:** visible beyond what is used. But it is the declared accessibility of a member to *other* classes, mostly a snapshot, with no link to where later code goes. |
| Ruland et al. 2018 (attack surface of refactorings) | Treats the declared accessibility of class members as an attack surface to be minimised when refactorings are searched for. | Exposure as a quantity to control, for security; not measured at the point of a change, and not followed. |
| Counsell and Nasseri 2010 (evolution at the attribute level) | Net attributes added per version in three Java systems: some arrive with new classes, some alone, and additions go with refactoring activity. | Classes gain fields over time: the raw material of H1's class level. No account of what the fields are visible to or who later uses them. |
| Vaucher et al. 2009; Chatzigeorgiou and Manakos 2010; Tufano et al. 2015 (life cycle of god classes and smells) | God classes mostly arise by new functionality accumulating over versions; smells persist once present; most are there from a unit's creation. | The accretion H1 describes, seen at the level of the detector's verdict. None measures the data a new addition finds around it, and none tests a mechanism. Already in the plan (§7, *Smells born, not grown*). |
| Baumgartner and Pulvermüller 2025 (data clumps over time) | A longitudinal analysis of data clumps (groups of fields or parameters that travel together) across public repositories; a search summary of the authors' earlier conference paper says clumps remain or accumulate. **Abstract not seen.** | Method and class data that gathers, followed over history. A clump is data *used together*, the opposite side from a bystander. |
| Chaikalis and Chatzigeorgiou 2015; Lin and Whitehead 2015 (preferential attachment in Java evolution) | Model the growth of class dependency networks: new relations attach to classes in proportion to those they have, damped by age; fine-grained changes simulated this way give the observed power laws. | **The aggregate pattern H2 would explain.** Rich-get-richer is fitted to degree in a dependency graph. It does not say what is attached to (data), nor follow the particular values later code uses. A reviewer may read H2 as preferential attachment under another name. |
| Tsantalis and Chatzigeorgiou 2009; Kiss and Mihancea 2018 (entity placement; feature envy at block level) | Where a method, or a block, belongs given the entities it accesses. | Already the nearest relative of the binding (first check, claim 2). It reads what code uses, on a snapshot; the bystander is what it does not use. |
| Chidamber and Kemerer 1994; Mitchell and Power 2004 (LCOM and its run-time variant) | Lack of cohesion counts the fields of a class that its methods do not share; the run-time variant counts only fields actually accessed. | **A structural relative the plan does not yet name.** A run's class bystanders are, for one piece of added code, the fields of its class it does not use: the per-addition, at-the-commit form of the quantity LCOM sums over a class. LCOM is a snapshot of the whole class and says nothing about what later code is bound to. |
| Zhou, Leung and Xu 2009; Chowdhury et al. 2022b (size, metrics and change-proneness) | Zhou et al.: on Eclipse, class size accounts for, or reverses, the association of many object-oriented metrics with change-proneness. Chowdhury et al.: at method level, metrics still help estimate change-proneness once size is removed, and dividing by size does not remove it. | **Both sides of H3.** The first is H3's result for size at the class; the second disputes it at the method. Neither holds the problem fixed or controls for the data in the place. |
| Feitelson 2023 (local variables of narrow and broad scope) | Scope of 637,077 Java locals against the length and wording of their names. | Scope measured at scale, for naming. No link to change. |

**Verdict, claim by claim.**

1. **H1, places fill with data that added code does not use, within a class and a method.**
   *The growth is known in aggregate; the measure and the unit were not found.* That shared data
   gathers faster than code is the Linux common-coupling result (Schach et al.; Yu et al.), and
   classes gaining attributes and god classes forming by accretion are documented (Counsell and
   Nasseri; Vaucher et al.). Visibility beyond use is documented for access modifiers (Vidal et
   al.). No study found measures, at the commit where code lands, what was visible there and not
   used, or follows that within one class and one method. **Claim:** new as a measure and as a
   unit; **not** new as the observation that classes and shared state grow. H1 should be presented
   as the per-addition, per-place form of the common-coupling growth result, and set beside LCOM,
   of which the class-level bystander is the per-addition component.
2. **H2, later code is bound to the data that stood by.** *Not found.* The nearest are a
   correlation of global-data references with later change at file level (Selby et al.), and
   preferential attachment fitted to dependency degree (Chaikalis and Chatzigeorgiou; Lin and
   Whitehead). No study found identifies the values standing by when code is placed and then asks
   whether later code for other problems uses those values. **Claim:** new, and the most
   distinctive of the four. It needs to say why it is more than preferential attachment: it names
   what is attached to, and the plan's size-or-data reading is where the two are set apart (on the
   development chain that reading did not separate them).
3. **H3, shape does not draw code in once the problem, the bindings and the bystanders are held
   fixed (one-sided).** *Substantially anticipated for size; contested at the method.* Zhou et al.
   (2009) and El Emam et al. (2001) show size accounting for metric associations at the class;
   Olbrich et al. (2010) the same for god classes; Chowdhury et al. (2022b) report the opposite at
   the method. **Claim:** a refinement, controlling for data and the problem in place of size. It
   is not a first, and the method-level literature is against it; the development chain's
   method-level result (complexity followed by less) should be reported against Chowdhury et al.
4. **Human against agent, and bound against unbound code** (the readings added on 17 and 18
   November). *Not found:* no study found measures whether added code goes to an existing class
   or a new one as a commit-level choice, by person or by agent. One commit-classification paper
   (arXiv:1810.04825) reports adding functions as commoner than adding classes; **its content was
   seen only as a search summary**. The agent studies found concern unrequested file creation and
   over-editing, not placement.

**What this suggests for the plan** (applied to PLAN.md on 20 November 2026, §9 row 62):

- Cite the Linux common-coupling studies in §1 and §4.3a as the precedent for data that gathers
  and exposes code without the code changing, and state how a bystander differs.
- Name LCOM in §4.3a. The plan says (§7 of this file) that it does not measure cohesion, yet a
  class-level bystander count is a cohesion-like quantity, and H3 now tests LCOM* as a *shape*
  measure beside it. A reviewer will ask how H2's predictor and one of H3's measures differ; the
  answer (per addition against whole class; visible to this code against shared between methods)
  should be written down.
- Add preferential attachment to §7 as the rival reading of H2, with the size-or-data reading as
  the check.
- Cite Zhou et al. 2009 and Chowdhury et al. 2022b at H3 as the two sides; Chowdhury et al. is
  already in the references.
- Cite the over-exposure studies as the nearest "visible beyond use" measure.

### Novelty check for encapsulation as a force, surface against volume, and conservation, 20 November 2026

The ideas checked are the newest readings of 20 November 2026, not yet in `PLAN.md` as
hypotheses:

1. **Encapsulation as a force.** Data private to a class can be used only inside it, so a change
   that needs it is *forced* into that class (concentration; the cost is the class's growth). If
   the forced change also needs data held elsewhere, it either couples to what that other class
   already exposes, or that class's encapsulation is widened (members made public, getters added)
   so that it can (dispersion; the cost is coupling). Measured per change: positions absorbed into
   the forced class against calls added across class boundaries, split by whether the callee was
   already exposed, newly exposed, or widened in access.
2. **Forced changes spread** across more classes and raise the coupling between the classes that
   change together (H6 and H7).
3. **Surface against volume.** A class's boundary (calls in and out) against its size (the
   content it encapsulates), followed over time, with a scaling exponent: concentration lowers
   surface per volume, dispersion raises it, and good engineering is the balance point. With it, a
   split-or-concentrate reading: split a class whose forced changes fall into groups that use
   disjoint data; concentrate classes that repeatedly change together over the same data.
4. **Conservation of complexity.** With the amount of code fixed by the problem, placement only
   redistributes complexity between size and coupling (a "physics of software").

**Protocol, as run.** No citation snowball this time: the ideas sit in design theory and in
modularisation research rather than near one seed paper. Instead:

1. **Named works verified** (they had been named from memory): Ousterhout's *A Philosophy of
   Software Design*, Page-Jones's connascence, and Carlo Pescio's *Physics of Software*, by web
   search against the author's or publisher's pages and index records.
2. **Keyword searches on OpenAlex**, 26 unrestricted (`literature/snowball/oa3.py`) and 21
   restricted to the field Computer Science (`oa3cs.py`), each read to the first 20–25 titles:
   scaling of coupling with size, allometric and surface-to-volume analogies, Rent's rule in
   software, interface against implementation size, access-modifier and visibility change over
   evolution, getters added and Encapsulate Field, coupling introduced by a commit, co-change with
   structural coupling, co-change as a split or move signal, Extract Class from cohesion,
   god-class decomposition, search-based modularisation (Bunch, multi-objective clustering), the
   physics of software, the cohesion–coupling trade-off, dependency injection and coupling,
   procedural or functional against object-oriented coupling, connascence, deep modules,
   conservation of complexity or information. The title lists are in `openalex3-titles.txt` and
   `oa3cs-titles.txt`; the raw responses are not kept.
3. **Semantic Scholar** (`s2b3.py`) was rate-limited on the first query and returned nothing;
   the same queries were then run through `oa3cs.py`. About 15 web searches filled in records the
   indexes lacked.

**Limits.** No snowball; the first 20–25 hits per query only; OpenAlex's relevance ranking is
noisy outside its field filter (many unrestricted hits were physics, biology and materials).
**Read in full: Lopes and Ossher 2015 (arXiv version, results and discussion sections) only.**
Pescio's Chapter 16 was read through a fetched page summary. Every other entry below was read as
an abstract, index record or search snippet, and is marked where that matters. As before, this
is "not found by this protocol", not "does not exist".

**The named works, verified.**

| Work | What it is (as verified) | How it relates / differs |
|---|---|---|
| Ousterhout 2018; 2nd ed. 2021, *A Philosophy of Software Design*, Yaknyam Press | Book. Confirmed by the author's Stanford page and library records (2nd ed. July 2021, ISBN 978-1-7321022-1-7; the first edition's ISBN was not confirmed). Its *deep module* has a small interface over a large implementation; *information leakage* is the same knowledge needed in two modules (secondary summaries; **text not read, check before quoting**). | **The design-advice form of idea 3.** "Deep" is a low surface-per-volume ratio held up as good; leakage is idea 1's dispersion seen as a defect. It gives no measure, no exponent, and nothing about how the ratio moves as changes land. |
| Page-Jones 1992 (*CACM* 35(9), 147–151, "Comparing techniques by means of encapsulation and connascence"); 1995 (*What Every Programmer Should Know About Object-Oriented Design*, Dorset House; the year is given as 1995 or 1996 by different sources); 1999 (*Fundamentals of Object-Oriented Design in UML*) | Connascence: two elements are connascent if changing one requires changing the other, graded by strength, degree and locality; connascence across an encapsulation boundary is worse than inside one. The CACM paper is confirmed by DOI; the grading is from secondary sources (**check before quoting**). Weirich's "rule of locality" is attributed inconsistently. | **The closest conceptual precedent for idea 1.** Connascence is the reason a change is forced to where its data is, and "locality" is concentration against dispersion. It is a taxonomy for judging a design, not a measure taken per change, and it has no notion of widening a boundary to let a change through. |
| Pescio, *Notes on Software Design* (blog, 2008–2012) and *Physics of Software* drafts (e.g. "Forces in the Physics of Software – the final word", January 2024, draft, no venue) | Design decisions as forces acting on the software "material"; *entanglement* (change to one artefact forces change to another) as an attractive force; chapters titled **mass, gravity, inertia** (2008–09), distance, friction. Chapter 16 (May 2012): forces pull responsibilities together or push them apart; putting an unstable set inside one class makes the class unstable. Listing from physicsofsoftware.weebly.com. | **The precedent for idea 4's vocabulary, and a name collision with "placement gravity".** Pescio uses *gravity* for the pull that gathers things; the gravity chapters were **not read**, so the overlap with this study's sense is unknown. Not empirical, not peer reviewed, no measurement. It must be cited so that the physics framing is not read as new. |

**The nearest neighbours found.**

| Work | What it does | How it relates / differs |
|---|---|---|
| Lopes and Ossher 2015 (how scale affects structure in Java) | 30,911 Google Code projects, fitted as power laws across projects. **Read:** methods ≈ e^1.09 · classes^1.106 (superlinear); SLOC ≈ modules^1.094; interfaces ≈ classes^0.70; project efferent coupling (external types used) ≈ SLOC^0.564 (sublinear); used internal modules ≈ declared^0.74. "Large Java projects have injected stronger coupling material ... into the [larger] software bricks." | **The closest empirical scaling result for idea 3.** But it is cross-sectional and per *project* (one point per project), not per class over its history, and its coupling is to external types, not calls across class boundaries. It shows exponents ≠ 1 are real and must be normalised for, which supports reporting an exponent rather than a ratio. |
| Taube-Schock, Walker and Witten 2011 (*Can we avoid high coupling?*, ECOOP) | A model and a large empirical study: between-module connectivity is approximately scale-free, so some highly coupled modules are statistically unavoidable, not a sign of poor design (abstract and repository record). | A rival for idea 3's "balance point": high coupling in some classes may be the distribution's tail, not a failure of balance. Snapshot degree distribution; no size against boundary per class. |
| Myers 2003; Concas et al. 2007; Wheeldon and Counsell 2003 (already cited) | Scale-free, small-world class and collaboration graphs. | Degree distributions, not degree against size. |
| Hatton 2014 (*Conservation of information: software's hidden clockwork?*, IEEE TSE 40(5); arXiv 1207.5027) | Derives power-law component sizes from conservation of Hartley–Shannon information under scale invariance (abstract and preprint listing). | **The only "conservation law" for software found in a refereed venue.** What is conserved is information in a token alphabet, and the prediction is the size distribution, not a trade between size and coupling. A reviewer may point to it against idea 4. |
| Loth 2026 (*Coupling as a consequence of cohesion*, Zenodo preprint) | Argues that within one partitioning rule, coupling follows from cohesion; defines an irreducible "coupling floor" equal to the necessary dependency graph, with every edge above it a boundary defect (abstract). | Close to idea 4 in spirit: a floor of coupling fixed by the domain, the rest caused by placement. Not peer reviewed, theory only. **Check before citing.** |
| Kobori, Matsushita and Inoue 2015 (accessibility excessiveness over versions, SANER) | Runs an accessibility-excessiveness checker across releases of several OSS projects and reports how fields and methods move between excessive and not, by major against minor release (abstract). | **The nearest to measuring widening over evolution.** Per release and per member, not per change; it does not ask which change made a member wider or whether that change also needed the class's data. |
| Vidal et al. 2016 (already cited); Steimann and Thies 2009 (*From public to private to absent*, ECOOP) | Over-exposure is common and mostly present from a member's first version; changes of access modifier are reported as infrequent (cited in Vidal et al., **source not traced**). Steimann and Thies formalise the accessibility constraints that moving members imposes, so refactorings must sometimes widen access (**index record only**). | Together they bound idea 1's widening branch: widening exists, is rare per member, and is a known side effect of moves. None links a widening to the change that needed it. |
| Paixão et al. 2017 (ASE, already cited); Eick et al. 2001 (already cited) | Per-commit cohesion and coupling deltas; span of changes grows over time. | Measure the *outcome* of ideas 1–2 per commit. No forced/unforced split. |
| Ajienka and Capiluppi 2017 (JSS); Oliva and Gerosa (cited by them); Beck and Diehl 2011 (FSE) | 79 projects: structural and logical (co-change) coupling overlap little; co-changed sets are much larger than structurally coupled ones (abstract and secondary). Beck and Diehl: which coupling kinds (structural, co-change, ownership, clones, semantics) agree with the package structure in 16 projects (abstract). | Background for H6/H7: co-change and structural coupling are different things, so "coupling between co-changed classes" must say which it means. |
| Silva, Valente and Maia 2014; 2015 (co-change clusters); de Oliveira et al. 2019 (JSS, *Finding needles in a haystack*); Bavota, De Lucia and Oliveto 2011 (JSS, Extract Class from structural and semantic cohesion); Chen et al. 2024 (ASE, ClassSplitter) | Co-change clusters projected on packages to assess modularity; Move Method/Move Field recommended to remove co-change dependencies across classes (610 "evolutionary smells" in 49 projects); classes split by clustering methods on shared fields and semantics; god classes split using method position. (Abstracts or snippets.) | **Idea 3's split-or-concentrate reading is well established** as refactoring recommendation: split on disjoint data use, move or merge on co-change. What none does is restrict the evidence to *forced* changes. |
| Mancoridis et al. 1998; Mitchell and Mancoridis 2006 (Bunch, TSE); Harman, Hierons and Proctor 2002; Praditwong, Harman and Yao 2010 (TSE); Paixão, Harman, Zhang and Yu 2017 (IEEE TEVC) | Modularisation as search maximising cohesion and minimising coupling (with granularity); multi-objective forms. The longitudinal study over 233 releases of ten systems: developers' structures beat random on the cohesion/coupling fitness but leave about 25% improvement, and optimising would change over 57% of the structure (abstract). | **Idea 3's "balance point" as an optimum is known** and has an operational form. It optimises a static graph; it does not derive the trade from forced changes, and treats size only as granularity. Paixão et al. 2017 TEVC is the longitudinal comparison to cite. |
| Razina and Janzen 2007; Sun et al. 2022 (*Computers* 11(9)) | Twenty pairs of SourceForge projects with and without dependency injection: no correlation of DI use with coupling or cohesion, a trend to lower coupling above 10% DI (abstract). Sun et al. propose DI-weighted CBO (abstract). | The only DI-against-not comparisons found; project-level, not about placement, and not size against coupling. |

**Verdict, idea by idea.**

1. **Encapsulation as a force (concentration forced; dispersion by exposed, newly exposed or
   widened access).** *Partly known as concept; not found as measurement.* That data hiding forces
   a change to where its data is, and that crossings of encapsulation are the costly kind, is
   Parnas, Page-Jones (connascence locality), Ousterhout (information leakage) and Pescio
   (entanglement). Widening is measured per member over releases (Kobori et al.; Vidal et al.) and
   modelled as a refactoring constraint (Steimann and Thies). **Not found:** a per-change account
   of positions absorbed against calls added, split by the callee's prior, new or widened
   exposure. **Claim:** new as a measure; present it as connascence locality made measurable at
   the commit.
2. **Forced changes spread and raise co-change coupling (H6/H7).** *Outcome measures known;
   predictor not found.* Change span (Eick), per-commit coupling deltas (Paixão et al. ASE) and
   the gap between logical and structural coupling (Ajienka and Capiluppi) exist. No study
   separates forced from unforced changes. **Claim:** new in its predictor, as for the first
   check's claim 4.
3. **Surface against volume, with an exponent; split or concentrate.** *The scaling reading is
   not found; the trade and the split/merge rules are known.* Superlinear and sublinear size
   effects are documented across projects (Lopes and Ossher), the small-interface-over-large-body
   ideal is Ousterhout's deep module, and high coupling is argued unavoidable in the tail
   (Taube-Schock et al.). Rent's rule (terminals against gates in circuits) is the exact physical
   analogue; the search found it applied to parallel programs and network traffic, **not to class
   or module boundaries in code**. Splitting on disjoint data and moving or merging on co-change
   are standard recommenders (Bavota et al.; de Oliveira et al.; Silva et al.), and cohesion
   against coupling as an optimum is the search-based modularisation literature (Bunch; Harman
   et al.; Paixão et al. TEVC). **Claim:** a per-class surface-to-volume exponent followed over
   history, moved by forced changes, is new; the balance point and the split/merge heuristics are
   not, and should be cited as such (including Rent's rule as the analogy's origin, if used).
4. **Conservation of complexity (placement redistributes between size and coupling).** *Known as
   framing; not found as a testable law.* Tesler (already cited), Pescio's physics of software,
   Hatton's conservation of information (a different conserved quantity), Loth's coupling floor
   (preprint), and the size–coupling trade implicit in Stevens, Myers and Constantine and in
   search-based modularisation's granularity term. **Claim:** a framing, not a result; if it is
   kept it should be stated as the hypothesis that coupling plus size per problem stays constant
   across placements, which none of these tests. **Pescio's use of "gravity" must be cited** next
   to the study's name.

**Not found by this protocol:** per-change attribution of coupling growth to the change that
needed it (beyond per-commit deltas); any comparison of dependency-injected, function-oriented and
class-oriented placement on size against coupling; Rent's rule or allometric scaling applied to
classes over their history.

**Unverified, check before quoting:** Ousterhout's wording (deep module, information leakage) and
the first edition's ISBN; Page-Jones's grading of connascence and the 1995/1996 book year; the
content of Pescio's gravity chapters and 2024 drafts; Hatton 2014's results beyond the abstract;
Taube-Schock et al. beyond the abstract; Loth 2026 in full (unrefereed); Steimann and Thies 2009
and de Oliveira et al. 2019 beyond index records and snippets; the claim that access-modifier
changes are infrequent (traced only to a citation inside Vidal et al.).

**What this suggests for the plan** (applied to PLAN.md on 20 November 2026, §9 row 62):

- Cite Page-Jones (connascence locality) and Ousterhout (deep modules, information leakage) where
  encapsulation as a force is introduced, and Kobori et al. with Vidal et al. for widening.
- Cite Lopes and Ossher for size scaling and the need to normalise by an exponent, and
  Taube-Schock et al. as the rival reading of high coupling in a few classes.
- Present the split/concentrate reading as the established recommenders (Extract Class, co-change
  Move) restricted to forced changes, and the balance point against Paixão et al. TEVC 2017.
- Keep conservation as framing; cite Tesler, Hatton and Pescio, and acknowledge Pescio's
  "gravity".

## References

- Abadi, A., Ettinger, R., Feldman, Y. A. (2012). Fine slicing: theory and applications for computation extraction. *FASE 2012*, LNCS 7212.
- Baldwin, C. Y., Clark, K. B. (2000). *Design Rules, Vol. 1: The Power of Modularity*. MIT Press.
- Bavota, G., Dit, B., Oliveto, R., Di Penta, M., Poshyvanyk, D., De Lucia, A. (2013). An empirical study on the developers' perception of software coupling. *ICSE 2013*, 692–701. doi:10.1109/ICSE.2013.6606615
- Bird, C., Bachmann, A., Aune, E., Duffy, J., Bernstein, A., Filkov, V., Devanbu, P. (2009). Fair and balanced? Bias in bug-fix datasets. *ESEC/FSE 2009*, 121–130. doi:10.1145/1595696.1595716
- Briand, L. C., Daly, J. W., Wüst, J. (1998). A unified framework for cohesion measurement in object-oriented systems. *Empirical Software Engineering* 3(1), 65–117.
- Brooks, F. P. (1987). No silver bullet: essence and accidents of software engineering. *Computer* 20(4), 10–19.
- Chowdhury, S. (2025). The good, the bad, and the monstrous: predicting highly change-prone source code methods at their inception. *ACM TOSEM* 34(7). arXiv:2408.05704
- Chowdhury, S., Uddin, G., Holmes, R. (2022a). An empirical study on maintainable method size in Java. *MSR 2022*. arXiv:2205.01842
- Chowdhury, S., Holmes, R., Zaidman, A., Kazman, R. (2022b). Revisiting the debate: are code metrics useful for measuring maintenance effort? *Empirical Software Engineering* 27.
- Concas, G., Marchesi, M., Pinna, S., Serra, N. (2007). Power-laws in a large object-oriented software system. *IEEE TSE* 33(10), 687–708.
- D'Ambros, M., Lanza, M., Robbes, R. (2009). On the relationship between change coupling and software defects. *WCRE 2009*, 135–144. doi:10.1109/WCRE.2009.19
- Dias, M., Bacchelli, A., Gousios, G., Cassou, D., Ducasse, S. (2015). Untangling fine-grained code changes. *SANER 2015*, 341–350. doi:10.1109/SANER.2015.7081844
- Eaddy, M., Zimmermann, T., Sherwood, K. D., Garg, V., Murphy, G. C., Nagappan, N., Aho, A. V. (2008). Do crosscutting concerns cause defects? *IEEE TSE* 34(4), 497–515. doi:10.1109/TSE.2008.36
- Eick, S. G., Graves, T. L., Karr, A. F., Marron, J. S., Mockus, A. (2001). Does code decay? Assessing the evidence from change management data. *IEEE TSE* 27(1), 1–12. doi:10.1109/32.895984
- El Emam, K., Benlarbi, S., Goel, N., Rai, S. N. (2001). The confounding effect of class size on the validity of object-oriented metrics. *IEEE TSE* 27(7), 630–650. doi:10.1109/32.935855
- Ettinger, R. (2007). *Refactoring via Program Slicing and Sliding*. DPhil thesis, University of Oxford.
- Ettinger, R., Verbaere, M. (2004). Untangling: a slice extraction refactoring. *AOSD 2004*.
- Evanco, W. M. (2003). Comments on "The confounding effect of class size on the validity of object-oriented metrics". *IEEE TSE* 29(7), 670.
- Fowler, M. (1999). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley.
- Gall, H., Hajek, K., Jazayeri, M. (1998). Detection of logical coupling based on product release history. *ICSM 1998*, 190–197. doi:10.1109/ICSM.1998.738508
- Grund, F., Chowdhury, S., Bradley, N., Hall, B., Holmes, R. (2021). CodeShovel: constructing method-level source code histories. *ICSE 2021*.
- Hassan, A. E., Holt, R. C. (2004). Predicting change propagation in software systems. *ICSM 2004*, 284–293.
- Herzig, K., Zeller, A. (2013). The impact of tangled code changes. *MSR 2013*.
- Herzig, K., Just, S., Zeller, A. (2016). The impact of tangled code changes on defect prediction models. *Empirical Software Engineering* 21. doi:10.1007/s10664-015-9376-6
- Jodavi, M., Tsantalis, N. (2022). Accurate method and variable tracking in commit history. *ESEC/FSE 2022*, 183–195. doi:10.1145/3540250.3549079
- Khomh, F., Di Penta, M., Guéhéneuc, Y.-G., Antoniol, G. (2012). An exploratory study of the impact of antipatterns on class change- and fault-proneness. *Empirical Software Engineering* 17(3), 243–275. doi:10.1007/s10664-011-9171-y
- Kiczales, G., Lamping, J., Mendhekar, A., Maeda, C., Lopes, C., Loingtier, J.-M., Irwin, J. (1997). Aspect-oriented programming. *ECOOP 1997*, LNCS 1241.
- Komondoor, R., Horwitz, S. (2000). Semantics-preserving procedure extraction. *POPL 2000*, 155–169. doi:10.1145/325694.325713
- Lakhotia, A., Deprez, J.-C. (1998). Restructuring programs by tucking statements into functions. *Information and Software Technology* 40(11–12), 677–689.
- Lehman, M. M. (1980). Programs, life cycles, and laws of software evolution. *Proceedings of the IEEE* 68(9), 1060–1076. doi:10.1109/PROC.1980.11805
- Martin, R. C. (2003). *Agile Software Development: Principles, Patterns, and Practices*. Prentice Hall.
- Maruyama, K. (2001). Automated method-extraction refactoring by using block-based slicing. *SSR 2001*, 31–40.
- Mo, R., Cai, Y., Kazman, R., Xiao, L. (2015). Hotspot patterns: the formal definition and automatic detection of architecture smells. *WICSA 2015*, 51–60. doi:10.1109/WICSA.2015.12
- Mo, R., Cai, Y., Kazman, R., Xiao, L., Feng, Q. (2016). Decoupling level: a new metric for architectural maintenance complexity. *ICSE 2016*, 499–510. doi:10.1145/2884781.2884825
- Moseley, B., Marks, P. (2006). *Out of the Tar Pit*. Unpublished paper.
- Palomba, F., Bavota, G., Di Penta, M., Oliveto, R., Poshyvanyk, D., De Lucia, A. (2015). Mining version histories for detecting code smells. *IEEE TSE* 41(5), 462–489. doi:10.1109/TSE.2014.2372760
- Parnas, D. L. (1972). On the criteria to be used in decomposing systems into modules. *Communications of the ACM* 15(12), 1053–1058.
- Saffer, D. (2010). *Designing for Interaction*, 2nd ed. New Riders. (Interview with L. Tesler, ch. 7.)
- Silva, D., Tsantalis, N., Valente, M. T. (2016). Why we refactor? Confessions of GitHub contributors. *FSE 2016*. arXiv:1607.02459
- Simon, H. A. (1962). The architecture of complexity. *Proceedings of the American Philosophical Society* 106(6), 467–482.
- Steidl, D., Deissenboeck, F. (2015). How do Java methods grow? *SCAM 2015*, 151–160.
- Stevens, W. P., Myers, G. J., Constantine, L. L. (1974). Structured design. *IBM Systems Journal* 13(2), 115–139.
- Sullivan, K. J., Griswold, W. G., Cai, Y., Hallen, B. (2001). The structure and value of modularity in software design. *ESEC/FSE 2001*, 99–108.
- Tarr, P., Ossher, H., Harrison, W., Sutton, S. M. (1999). N degrees of separation: multi-dimensional separation of concerns. *ICSE 1999*, 107–119.
- Tsantalis, N., Ketkar, A., Dig, D. (2022). RefactoringMiner 2.0. *IEEE TSE* 48(3), 930–950. doi:10.1109/TSE.2020.3007722
- Tufano, M., Palomba, F., Bavota, G., Oliveto, R., Di Penta, M., De Lucia, A., Poshyvanyk, D. (2015). When and why your code starts to smell bad. *ICSE 2015*. doi:10.1109/ICSE.2015.59
- Vasa, R., Lumpe, M., Branch, P., Nierstrasz, O. (2009). Comparative analysis of evolving software systems using the Gini coefficient. *ICSM 2009*, 179–188. doi:10.1109/ICSM.2009.5306322
- Vaucher, S., Khomh, F., Moha, N., Guéhéneuc, Y.-G. (2009). Tracking design smells: lessons from a study of god classes. *WCRE 2009*, 145–154. doi:10.1109/WCRE.2009.23
- Weiser, M. (1984). Program slicing. *IEEE TSE* SE-10(4), 352–357.
- Wheeldon, R., Counsell, S. (2003). Power law distributions in class relationships. arXiv:cs/0305037.
- Yau, S. S., Collofello, J. S. (1980). Some stability measures for software maintenance. *IEEE TSE* SE-6(6), 545–552. doi:10.1109/TSE.1980.234503
- Zimmermann, T., Weißgerber, P., Diehl, S., Zeller, A. (2005). Mining version histories to guide software changes. *IEEE TSE* 31(6), 429–445. doi:10.1109/TSE.2005.72

### Added by the novelty check

- Bouwers, E., van Deursen, A., Visser, J. (2014). Quantifying the encapsulation of implemented software architectures. *ICSME 2014*. doi:10.1109/ICSME.2014.43
- Kouroshfar, E., et al. (2015). [Study of co-change across modules and defects; the paper at seal.ics.uci.edu/publications/2015MSR.pdf]. *MSR 2015*. (Only the first author and venue are confirmed; **check the full author list and title before citing**.)
- Ogenrwot, D., Businge, J. (2026). How AI coding agents modify code: a large-scale study of GitHub pull requests. *MSR 2026*. arXiv:2601.17581
- Olbrich, S. M., Cruzes, D. S., Sjøberg, D. I. K. (2010). Are all code smells harmful? A study of God Classes and Brain Classes in the evolution of three open source systems. *ICSM 2010*. doi:10.1109/ICSM.2010.5609564
- Paixão, M., Krinke, J., Han, D., Ragkhitwetsagul, C., Harman, M. (2017). Are developers aware of the architectural impact of their changes? *ASE 2017*, 95–105. doi:10.1109/ASE.2017.8115622
- Passos, L., Padilla, J., Berger, T., Apel, S., Czarnecki, K., Valente, M. T. (2015). Feature scattering in the large: a longitudinal study of Linux kernel device drivers. *MODULARITY 2015*. doi:10.1145/2724525.2724575
- Passos, L., Queiroz, R., Mukelabai, M., Berger, T., Apel, S., Czarnecki, K., Padilla, J. (2018). A study of feature scattering in the Linux kernel. *IEEE TSE*. doi:10.1109/TSE.2018.2884911
- Queiroz, R., Passos, L., Valente, M. T., Apel, S., Czarnecki, K. (2014). Does feature scattering follow power-law distributions? An investigation of five pre-processor-based systems. *FOSD 2014*. Extended as: The shape of feature code: an analysis of twenty C-preprocessor-based systems, *Software and Systems Modeling* (2017). doi:10.1007/s10270-015-0483-z
- Tsantalis, N., Chatzigeorgiou, A. (2009). Identification of Move Method refactoring opportunities. *IEEE TSE* 35(3), 347–367. doi:10.1109/TSE.2009.1
- Vasa, R., Schneider, J.-G., Nierstrasz, O. (2007). The inevitable stability of software change. *ICSM 2007*, 4–13. doi:10.1109/ICSM.2007.4362613
- Wong, S., Cai, Y., Kim, M., Dalton, M. (2011). Detecting software modularity violations. *ICSE 2011*, 411–420. doi:10.1145/1985793.1985850
- Yamasaki, K., Matia, K., Buldyrev, S. V., Fu, D., Pammolli, F., Riccaboni, M., Stanley, H. E. (2006). Preferential attachment and growth dynamics in complex systems. *Physical Review E* 74, 035103. doi:10.1103/PhysRevE.74.035103
- [Authors not recorded] (2026). Does code cleanliness affect coding agents? A controlled minimal-pair study. arXiv:2605.20049. (Authors not recorded; **check before citing**.)

### Added by the novelty check of 18 November 2026

Details are as the indexes (OpenAlex, publisher or repository records) gave them; where something
was not confirmed, it says so.

- Baumgartner, N., Pulvermüller, E. (2025). Unveiling data clumps: a detailed longitudinal analysis on software quality across public repositories. *SN Computer Science* 6(8), 960. doi:10.1007/s42979-025-04461-9 (Abstract not seen.)
- Chaikalis, T., Chatzigeorgiou, A. (2015). Forecasting Java software evolution trends employing network models. *IEEE TSE*. doi:10.1109/TSE.2014.2381249
- Chatzigeorgiou, A., Manakos, A. (2010). Investigating the evolution of bad smells in object-oriented code. *QUATIC 2010*. doi:10.1109/QUATIC.2010.16
- Chidamber, S. R., Kemerer, C. F. (1994). A metrics suite for object oriented design. *IEEE TSE* 20(6), 476–493.
- Counsell, S., Nasseri, E. (2010). System evolution at the attribute level: an empirical study of three Java OSS and their refactorings. *Journal of Computing and Information Technology* 18(2), 167–173. doi:10.2498/cit.1001811
- Feitelson, D. G. (2023). Reanalysis of empirical data on Java local variables with narrow and broad scope. *ICPC 2023*, 227–236. doi:10.1109/ICPC58990.2023.00037
- Kiss, A., Mihancea, P. F. (2018). Towards feature envy design flaw detection at block level. *ICSME 2018*. doi:10.1109/ICSME.2018.00064 (Index record only.)
- Lin, Z., Whitehead, J. (2015). Why power laws? An explanation from fine-grained code changes. *MSR 2015*. doi:10.1109/MSR.2015.14
- Mitchell, Á., Power, J. F. (2004). Run-time cohesion metrics: an empirical investigation. (Maynooth University eprint; **the venue was not confirmed**.)
- Ruland, S., Kulcsár, G., Leblebici, E., Peldszus, S., Lochau, M. (2018). Controlling the attack surface of object-oriented refactorings. *FASE 2018*, LNCS. doi:10.1007/978-3-319-89363-1_3
- Schach, S. R., Jin, B., Wright, D. R., Heller, G. Z., Offutt, A. J. (2002). Maintainability of the Linux kernel. *IEE Proceedings – Software*. (**Venue and year as given by a library record and a search summary, not confirmed against the publisher**; the exponential growth of common coupling is from the abstract.)
- Selby, J. W. A., Ruffell, F. P., Giesbrecht, M., Godfrey, M. W. (2007). Examining the effects of global data usage on software maintainability. *WCRE 2007*, 60–69. doi:10.1109/WCRE.2007.27
- Vidal, S. A., Bergel, A., Díaz-Pace, J. A., Marcos, C. (2016). Over-exposed classes in Java: an empirical study. *Computer Languages, Systems & Structures* 46. doi:10.1016/j.cl.2016.04.001
- Vidal, S. A., Bergel, A., Marcos, C., Díaz-Pace, J. A. (2016). Understanding and addressing exhibitionism in Java: empirical research about method accessibility. *Empirical Software Engineering* 21(2), 483–516. doi:10.1007/s10664-015-9365-9
- Yu, L., Schach, S. R., Chen, K., Offutt, J. (2004). Categorization of common coupling and its application to the maintainability of the Linux kernel. *IEEE TSE* 30(10), 694–706. doi:10.1109/TSE.2004.58
- Zhou, Y., Leung, H., Xu, B. (2009). Examining the potentially confounding effect of class size on the associations between object-oriented metrics and change-proneness. *IEEE TSE*. doi:10.1109/TSE.2009.32

### Added by the novelty check of 20 November 2026

Details are as the indexes, publishers' or authors' pages gave them; where something was not
confirmed, it says so.

- Ajienka, N., Capiluppi, A. (2017). Understanding the interplay between the logical and structural coupling of software classes. *Journal of Systems and Software*. doi:10.1016/j.jss.2017.08.042 (Abstract, partly.)
- Bavota, G., De Lucia, A., Oliveto, R. (2011). Identifying Extract Class refactoring opportunities using structural and semantic cohesion measures. *Journal of Systems and Software* 84(3). doi:10.1016/j.jss.2010.11.918 (Index record only.)
- Beck, F., Diehl, S. (2011). On the congruence of modularity and code coupling. *ESEC/FSE 2011*. doi:10.1145/2025113.2025162
- Chen, T., Jiang, Y., Fan, F., Liu, B., Liu, H. (2024). A position-aware approach to decomposing god classes. *ASE 2024*. doi:10.1145/3691620.3694992
- de Oliveira, M. C., Freitas, D., Bonifácio, R., Pinto, G., Lo, D. (2019). Finding needles in a haystack: leveraging co-change dependencies to recommend refactorings. *Journal of Systems and Software* 158. doi:10.1016/j.jss.2019.110420 (Snippets only.)
- Harman, M., Hierons, R. M., Proctor, M. (2002). A new representation and crossover operator for search-based optimization of software modularization. *GECCO 2002*. (Venue from memory and the UCL record; **check**.)
- Hatton, L. (2014). Conservation of information: software's hidden clockwork? *IEEE TSE* 40(5). doi:10.1109/TSE.2014.2316158 (Abstract and preprint listing only.)
- Kobori, K., Matsushita, M., Inoue, K. (2015). Evolution analysis for accessibility excessiveness in Java. *SANER 2015*. doi:10.1109/SANER.2015.7081818
- Lopes, C. V., Ossher, J. (2015). How scale affects structure in Java programs. *OOPSLA 2015*, 675–694. doi:10.1145/2814270.2814300; arXiv:1508.00628 (Read.)
- Loth, Y. (2026). Coupling as a consequence of cohesion. Zenodo preprint. doi:10.5281/zenodo.21925200 (Unrefereed; abstract only.)
- Mancoridis, S., Mitchell, B. S., Rorres, C., Chen, Y., Gansner, E. R. (1998). Using automatic clustering to produce high-level system organizations of source code. *IWPC 1998*. doi:10.1109/WPC.1998.693283
- Mitchell, B. S., Mancoridis, S. (2006). On the automatic modularization of software systems using the Bunch tool. *IEEE TSE* 32(3). doi:10.1109/TSE.2006.31
- Myers, C. R. (2003). Software systems as complex networks: structure, function, and evolvability of software collaboration graphs. *Physical Review E* 68, 046116. doi:10.1103/PhysRevE.68.046116
- Ousterhout, J. (2018; 2nd ed. 2021). *A Philosophy of Software Design*. Yaknyam Press. (2nd ed. ISBN 978-1-7321022-1-7; text not read.)
- Page-Jones, M. (1992). Comparing techniques by means of encapsulation and connascence. *Communications of the ACM* 35(9), 147–151. doi:10.1145/130994.131004
- Page-Jones, M. (1995). *What Every Programmer Should Know About Object-Oriented Design*. Dorset House. (Year given as 1995 or 1996; **check**.)
- Paixão, M., Harman, M., Zhang, Y., Yu, Y. (2017). An empirical study of cohesion and coupling: balancing optimization and disruption. *IEEE Transactions on Evolutionary Computation*. doi:10.1109/TEVC.2017.2691281
- Pescio, C. (2008–2012). *Notes on Software Design* (blog series), carlopescio.com; and *Forces in the Physics of Software – the final word* (draft, January 2024), physicsofsoftware.weebly.com. (Unrefereed.)
- Praditwong, K., Harman, M., Yao, X. (2011; online 2010). Software module clustering as a multi-objective search problem. *IEEE TSE* 37(2). doi:10.1109/TSE.2010.26 (Volume from memory; **check**.)
- Razina, E., Janzen, D. S. (2007). Effects of dependency injection on maintainability. (Cal Poly DigitalCommons; **venue not confirmed**.)
- Silva, L. L., Valente, M. T., Maia, M. A. (2014). Assessing modularity using co-change clusters. *MODULARITY 2014*. doi:10.1145/2577080.2577086
- Steimann, F., Thies, A. (2009). From public to private to absent: refactoring Java programs under constrained accessibility. *ECOOP 2009*, LNCS. doi:10.1007/978-3-642-03013-0_19 (Index record only.)
- Sun, P., Kim, D.-K., Ming, H., Lu, L. (2022). Measuring impact of dependency injection on software maintainability. *Computers* 11(9), 141. doi:10.3390/computers11090141
- Taube-Schock, C., Walker, R. J., Witten, I. H. (2011). Can we avoid high coupling? *ECOOP 2011*, LNCS 6813, 204–228. doi:10.1007/978-3-642-22655-7_10

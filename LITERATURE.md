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

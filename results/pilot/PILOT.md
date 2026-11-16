# Pilot: the pull instrument on chain 9

**16 November 2026. A pilot (PLAN.md §8, step 2), not a test of H1–H3.** It checks that the measures
compute and are not degenerate, and settles the rules before registration. This version replaces
two uncommitted drafts of 15 and 16 November: seam-based pull without RefactoringMiner, then
token-level ties.

The two chains it reads are development data, **excluded from the registered analysis**:

- `evolve/blind-202608100006/just-solve/spring/chain9` (head `b48eb0c`)
- `evolve/blind-202608100006/just-solve/officefloor/chain9` (head `b824bf9`)

No hypothesis statistic (H1's slope, H2's model, H3's arm term) was computed. The arm figures come
from one pair of chains and are not evidence for H3.

Reproduce: `./setup.sh && ./pilot.sh`. Two runs from an empty `.tmp/pilot` give byte-identical
outputs: `hosts.csv`, `runs.csv`, `classes.csv`, `additions.csv`, `outcomes.csv`, `summary.json`
and `codetracker-*.json`.

## The measure: ties of the logic lines

Only **logic lines** carry the value of a change: a method's body statements. Signatures,
declarations, imports and constructor wiring (`this.repo = repo;`) are organisation. The question
is where the data each added or edited logic line uses comes from:

- **From a value the change itself defines** (a local declared on an added line, a parameter of a
  new method): the code could have been placed anywhere.
- **From a value that already existed:** the code has to be placed near it, so choice is
  restricted. These are its **ties**.
  - **Method ties:** the host method's pre-existing parameters and locals.
  - **Class ties:** the host class's pre-existing fields (constants included) and methods. In
    Spring, injected dependencies are fields, so they tie code to the class.

Every reference on an added or edited logic line counts, whether or not the old version of the
line also used it.

**Not ties:**

- **Injected parameters.** Every parameter of a wired OfficeFloor function (a public method of a
  class the wiring names) can be declared by a function placed anywhere. The function's locals
  still tie.
- **Class utilities:** loggers, which any class can declare. They are reported as `utility`; the
  category is open for other such items, and so far loggers are the only one.
- **Birth ties:** the existing values a caller passes a new method. That tie is already counted on
  the caller's logic line (`check(digits)`), so it is reported but not counted twice.

**Secondary reading:** `tok_tie` counts only the references an edit itself introduced (a
token-level diff), for comparison.

**Inherited members:** an inherited field or method is existing class data, so it ties. The
instrument does not resolve superclasses. Instead it reports every reference that resolves to
nothing it can see (`unresolved`): unqualified calls and lower-case names that are no local,
parameter, field or method of the class. Package roots of fully qualified names are excluded.

## Refactoring: RefactoringMiner and CodeTracker

RefactoringMiner 3.0.4 (the version CodeTracker 2.6 pins) runs at every agent commit. It found 85
refactorings in Spring and 104 in OfficeFloor, with no errors.

- **Renames** are applied to the before version first. A renamed value is still pre-existing, and
  a line changed only by a rename is not an edit.
- **Matching:** renamed, moved and re-signatured methods and classes stay matched.
- **Moved code** (extract, inline, extract or inline variable, loop↔pipeline, invert condition,
  split or merge) is set apart from additions. Code added inside an extracted method stays an
  addition. Identical-text matching covers moves RefactoringMiner does not report.

In Spring, 60 positions were set apart as moved by RefactoringMiner and 14 by text; in OfficeFloor,
38 and 25. Every hint names a file of its own addition (a guard; 0 failures).

**CodeTracker 2.6** cross-checks how hosts are followed forward. Every method the instrument saw an
addition in, and that still exists at the chain's end, is tracked back through renames and moves of
the method and its class:

| | Spring | OfficeFloor |
|---|---|---|
| Methods compared (CodeTracker errors) | 105 (1) | 137 (1) |
| CodeTracker's checkpoints the instrument also has | 162 / 172 (94%) | 173 / 190 (91%) |
| The instrument's checkpoints CodeTracker confirms | 162 / 163 (99%) | 173 / 180 (96%) |
| Renamed or moved methods with identical histories | 3 / 6 | 2 / 7 |

The differences fall into three groups:

- **Empty constructors.** CodeTracker records an empty constructor being introduced, but the
  instrument sees no logic line in it.
- **Refactoring set apart by design.** At a few checkpoints the instrument classed a change as
  moved code where CodeTracker reports a body change.
- **Rename lineage.** In 4 or 5 cases the two tools follow a renamed class differently.

**Fixture tests:** 18 pass (`tests/test_pull.py`). They cover:

- ties:
  - accretion tied to an existing local and field, not new ones, with a logger as utility;
  - birth ties;
  - a write-back;
  - lambda parameters, which are not host state;
  - an edited logic line sourcing two existing values (token reading beside it);
  - a new class, which has no ties;
  - injected parameters, with and without wiring;
  - a call to an existing class method;
  - constructor wiring as organisation;
  - inherited members reported unresolved;
  - a constant as a field tie;
- refactoring:
  - extraction by text fallback;
  - a rename, with and without its hint;
  - RefactoringMiner's findings as hints;
  - identity across a rename and a move;
- the Gini coefficient.

## What the measures show

| Measure | Spring | OfficeFloor |
|---|---|---|
| Checkpoints (no-ops), files not parsed | 60 (1), 0 | 60 (0), 0 |
| Hosts with an addition: new (in a new class) / existing | 112 (18) / 62 | 140 (79) / 52 |
| …of which wired functions | 0 | 71 |
| Organisation lines set apart | 1 | 1 |
| Runs into existing hosts (edits) | 81 (49) | 65 (51) |
| Method ties per run, 0/1/2/3/4 | 12 / 47 / 17 / 5 / 0 | 33 / 21 / 8 / 2 / 1 |
| Class ties per run, 0/1/2/3/4 | 58 / 18 / 3 / 1 / 1 | 59 / 6 / 0 / 0 / 0 |
| All ties per run, 0/1/2/3/4/5 | 6 / 40 / 24 / 7 / 2 / 2 | 33 / 18 / 9 / 4 / 0 / 1 |
| Token reading, 0/1/2/3/4 | 32 / 33 / 13 / 2 / 1 | 44 / 17 / 4 / 0 / 0 |
| New hosts: ties 0/1/2/3 | 84 / 22 / 5 / 1 | 136 / 3 / 1 / 0 |
| Utility (logger) uses: runs into existing hosts / new hosts | 6 / 7 | 3 / 0 |
| Birth ties, reported not counted: new hosts with one or more | 9 / 112 | 3 / 140 |
| Runs with an unresolved reference (inherited?) | 0 / 206 | 0 / 212 |
| Amount, positions at cp1 → cp60 | 942 → 1,397 | 745 → 1,235 |
| Wiring added: nodes / edges | 0 / 0 | 33 / 24 |
| Problem–host pairs followed forward (with intrusion) | 174 (40) | 192 (30) |
| …followed by CodeTracker (surviving methods) / by the instrument (removed) | 153 / 21 | 169 / 23 |

### Forced at each cut (decision 3)

The share of runs into existing hosts, and of existing classes an addition reached, whose ties are
at or above the cut:

| Cut | Spring runs (of 81) | OfficeFloor runs (of 65) | Spring classes (of 87) | OfficeFloor classes (of 78) |
|---|---|---|---|---|
| ≥ 1 (registered) | 75 (93%) | 32 (49%) | 39 (45%) | 10 (13%) |
| ≥ 2 | 35 (43%) | 14 (22%) | 13 (15%) | 1 (1%) |
| ≥ 3 | 11 (14%) | 5 (8%) | 6 (7%) | 0 |
| ≥ 4 | 4 (5%) | 1 (2%) | 2 (2%) | 0 |
| ≥ 1, token reading | 49 (60%) | 21 (32%) | | |

At ≥ 1, almost every Spring addition into an existing method is forced (93%). Little room is left
to see forcing grow with host size (H1) or to compare forced with chosen (H2) within Spring. The
spread is widest at ≥ 2. The higher cuts thin quickly: at ≥ 4 there are 5 runs over both arms in
one chain each, or roughly 50 over ten chains per arm.

## The shape competitors (§4.7), added 16 November 2026

Read on each existing host at its version before the addition, over every production method of
the tree at k − 1 (`shape_series.csv`, and the `s*` columns of `hosts.csv`). Every existing host
was found there (Spring 62, OfficeFloor 52); no file failed to parse and no assessment failed.

| Existing hosts | Spring (62) | OfficeFloor (52) |
|---|---|---|
| S1 long (26+ code lines) | 23 | 1 |
| S2 stuck (not slimmable, or only with a record) | 0 | 0 |
| S2 status | 39 under the cap, 15 slimmable, 8 slimmable but locked | 51 under the cap, 1 slimmable |
| S3 junction (*d* > 0) | 35 | 35 |
| S4 complexity outlier (modified z ≥ 3.5) | 28 | 17 |
| S5 class Gini, median | 0.43 | 0.00 |

Over the whole tree, cp1 → cp60:

| | Spring | OfficeFloor |
|---|---|---|
| Methods | 278 → 378 | 256 → 391 |
| Long / stuck | 3 / 0 → 5 / 0 | 2 / 0 → 4 / 0 |
| Junction share of cognitive complexity | 0.33 → 0.31 | 0.30 → 0.42 |
| Complexity outliers | 16 → 21 | 13 → 25 |

Three things follow for H2b:

- **S2 is degenerate on this stream.** No method in either arm, at any checkpoint, is stuck. A
  measure with no variation cannot enter the model. The 60-checkpoint petclinic stream may simply
  not grow methods that far; the ui stream has 250. **Open (decision 8).**
- **S1 is nearly degenerate in OfficeFloor** (1 of 52 hosts), as its functions stay short.
- **S4's flag is broad.** Cognitive complexity is zero-heavy, so the median absolute deviation is
  zero and the complexity-concentration study's fallback scale applies. Hosts from cognitive 3
  (Spring) or 4 (OfficeFloor) upwards are flagged: 45% of Spring's existing hosts. The flag then
  reads as "has some control flow" rather than as an outlier. **Open (decision 9).**

The rise in OfficeFloor's junction share is a descriptive reading of one development chain, which is
excluded from the analysis. It runs against the absorbed flow-injection draft's P1 direction and
is recorded here because it was seen before registration (PLAN.md §6).

## Verdict per measure

- **Method and class ties** compute in both arms and vary: per run 0–5 in Spring and 0–5 in
  OfficeFloor; at class level, as expected, mainly in Spring.
- **Utility, organisation, birth ties and unresolved references** are all rare here. Each is
  reported, so a change of this in other chains will show.
- **Placement, dispersion, amount, wiring and outcomes** compute and vary.
- **Shape (S1–S5)** computes on every existing host. S2 does not vary, S1 hardly varies in
  OfficeFloor, and S4's flag is broad (decisions 8 and 9). S3 and S5 vary.

## Decisions

Settled 16 November 2026 (by the author, after this pilot's figures):

1. **Loggers do not tie.** They form a class-utility category, reported apart.
2. **Ties are read from the logic lines** a change adds or edits, as above, with edits and
   insertions pooled and an `edit` marker kept for the analysis.
3. **Forced = ties ≥ 1**, with the cuts 2, 3 and 4 reported beside it, as above.
4. **Inherited members tie.** The instrument reports them as unresolved. The pilot found none in
   418 runs, so superclass resolution is not built. The registered analysis reports the share of
   runs with an unresolved reference.

5. **Host identity for outcomes:** CodeTracker's history (identity and body-changing checkpoints)
   for methods that survive to the chain's end; the instrument's chaining for methods removed
   earlier. Applied in this pilot.

Open:

6. **The ceiling at ≥ 1 in Spring.** Register H1 and H2 on the tie count (continuous), with the cut
   at 1 as the reading aid, so that the ceiling does not remove the test.
7. **Run and chains.** Chain 9 of `blind-202608100006/just-solve` stays development data, excluded
   in both arms. The ui-long-degradation Run A is proposed as primary data (PLAN.md §3.1a), on two
   conditions that protect the flow-injection-containment plan.
8. **A shape measure with no variation.** Proposal: a shape measure that does not vary in a corpus
   (for example, fewer than 10 hosts flagged over all chains of an arm) leaves the H2b block for
   that corpus and is reported as such. H2b is then read on the measures that remain, and the
   equivalence bound is not taken as met for the measure that left.
9. **S4 as a flag or a level.** Proposal: enter cognitive complexity as log(1 + cognitive), a
   continuous measure, with the outlier flag reported beside it. On zero-heavy data the flag
   measures whether there is control flow, not whether the method is an outlier.

## Limits

One chain per arm, written by one agent. Names are matched lexically, with no symbol solver.
Outcomes follow surviving methods by CodeTracker and removed ones by name and RefactoringMiner's
renames; class-level identity is not followed by CodeTracker's class tracker yet. Positions are those of the pretty-printed source.
S3's calls are matched by name and arity, so a call on another type's method of the same name
and arity counts.

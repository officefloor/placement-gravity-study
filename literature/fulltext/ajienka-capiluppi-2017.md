# Ajienka and Capiluppi (2017), Understanding the interplay between the logical and structural coupling of software classes, JSS 134, 120–137

Read in full, 22 November 2026, from the authors' accepted manuscript in Brunel University's
repository (bura.brunel.ac.uk/bitstream/2438/20225/1/FullText.pdf). (The Edge Hill copy that
OpenAlex lists is behind a browser check.)

## What it does

- 79 open-source Java projects (more than 20 commits each), every revision. Structural coupling:
  number of references or calls between a pair of classes. Logical coupling: association-rule
  confidence of co-change. RQ1: overlap of the two sets of pairs; RQ2: Spearman correlation of
  strengths; RQ3: classify structurally coupled pairs as stable or unstable by co-change.

## Results (abstract and §4)

- "although there is no strong evidence of a linear correlation between the strengths of the
  coupling types, there is substantial evidence to conclude that structurally coupled class pairs
  usually include logical dependencies. However, not all co-changed class pairs are also linked by
  structural dependencies."
- The asymmetry is large: e.g. project 31, 68% of structurally coupled pairs co-changed, but only
  21% of co-changed pairs were structurally coupled; "in a majority (81%) of the projects ...
  structurally related classes involve logically related classes (64 of 79 projects)" (§4.1).
- "only a low proportion of structural coupling shows excessive instability".

## Cause and change size

- Logical coupling is glossed as "a change in one entity causes a change to be made to another
  entity" (Introduction), i.e. it records co-change, not its reason. No control for commit size
  is reported in the method; no forced/chosen distinction.

## Correction to LITERATURE.md §10 (20 November 2026)

The table there summarised this paper, from the abstract and a secondary source, as "structural
and logical (co-change) coupling overlap little; co-changed sets are much larger than
structurally coupled ones". The second half is right. The first half overstates: the overlap is
small as a share of *co-changed* pairs but large as a share of *structurally coupled* pairs
(most structurally coupled pairs do co-change, in 64 of 79 projects).

## Bearing

- H7: supportive in passing. Calls between two classes usually go with their changing together,
  so calls a forced change adds across a boundary are the kind of coupling that later shows as
  co-change. H7 measures the calls; this paper says why that is a reasonable cost to count.
- H6: compatible. Most co-change has no structural trace, so co-change spread mixes structural
  coupling with everything else that makes classes change together (the problem, ownership,
  conventions). A forced change's cost is more visible in calls (H7) than in spread (H6).

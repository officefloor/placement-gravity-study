# D'Ambros, Lanza and Robbes (2009), On the relationship between change coupling and software defects, WCRE 2009, 135–144

Read in full, 22 November 2026, from the Internet Archive copy (10 August 2024) of the authors'
PDF at inf.usi.ch/lanza/Downloads/DAmb2009e.pdf (the live copy is behind a browser check).
Ten pages, published layout.

## What it does

- Three Java systems (ArgoUML 0.28, Eclipse JDT Core 3.3, Mylyn 3.1.0). Four per-class change
  coupling measures over "n-coupled" classes (at least n shared transactions): NOCC, SOC,
  EWSOC, LWSOC. Spearman correlation with the number of linked bugs per class; then regression
  (principal components, 50 random 90/10 splits) adding change coupling to CK and other metrics.
- Filter: "we filtered out the transactions involving more than 100 classes" (§II; 86, 59 and 102
  transactions, mostly licence and documentation changes). No control for the size of a change;
  LOC appears only as one of the competing metrics.

## Results

- Change coupling correlates with defects (Spearman above 0.5; above 0.8 at best for Eclipse), more
  than the CK metrics, **but less than the number of changes** (§IV.B: "They correlate more than
  the CK and other object-oriented metrics, but less than the number of changes"). For major and
  high-priority bugs change coupling is better than number of changes in many cases.
- Regression: metrics plus change coupling beat metrics alone; metrics plus number of changes
  predict slightly better than "all CC measures".

## What it says about cause

- §I: "Change coupling information reveals potentially misplaced artifacts in a software system,
  because entities that evolve together should be placed close to each other for cognitive
  reasons"; "high change coupling among modules points to design issues such as architecture
  decay".
- But, decisively: "All these approaches are based on the assumption that change coupling indeed
  is a cause of issues in a software system. However, the relationship between change coupling
  and a tangible effect of software issues has not been studied yet." The paper tests an
  *effect* (defects), not a *cause*; it does not test whether co-change marks misplacement.

## Bearing

- H6: compatible. It reports the literature's causal reading (misplacement, decay) as an
  assumption and tests only a correlation with defects. The number of changes, a size-like
  quantity, beats change coupling for all bugs, which is consistent with H6's observation that
  spread follows change size.
- No forced/chosen distinction, no access, no per-change size control.

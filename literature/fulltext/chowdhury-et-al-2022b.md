# Chowdhury, Holmes, Zaidman and Kazman (2022b), Revisiting the debate: are code metrics useful for measuring maintenance effort?, EMSE 27, 158

Read in full, 22 November 2026, from the authors' preprint (cs.ubc.ca/~rtholmes/papers/
emse_2022_chowdhury_preprint.pdf, 33 pp.).

- About 730K Java methods from 47 projects; seven method-level metrics (including McCabe,
  readability, maintainability index); four change indicators.
- Steps (§1): ignoring size, metrics look useful; dividing by size, they still look useful; but
  "the widely adopted size normalization approach fails to neutralize the size influence, and the
  maintenance impact of code metrics can still be explained by their correlation with size";
  then, with size in the regression (size + McCabe ~ maintenance), "code metrics are indeed good
  maintenance predictors, even when their correlation with size is neutralized" (RQ3). Results:
  "This clearly refutes the claim that code metrics are not useful after size influence is
  neutralized". Conclusion: "Code metrics are useful predictors of maintenance effort, even after
  normalizing for size ... context is king". McCabe "can increase monotonically ... So their
  performance is not negatively impacted by code size" (RQ4).

## Correction to LITERATURE.md §2

§2 says: "much of the value of popular method-level metrics for change-proneness is explained by
their correlation with size." That is the paper's intermediate step 3 (for size-*divided*
metrics), not its conclusion, which is the opposite once size is entered as a covariate. The
18 November entry in §10 ("metrics still help ... once size is removed, and dividing by size does
not remove it") is the correct reading. §2's sentence overstates the size-confounding side and
should be read with that correction.

## Bearing

- H3 at the method: the paper is against H3's prediction (shape adds information beyond size).
  But it holds neither the problem nor the data in place fixed, which is H3's design; the contest
  is real, and the plan already sets the development chain's method-level result against it.

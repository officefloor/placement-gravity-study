# Zimmermann, Weißgerber, Diehl and Zeller (2005), Mining version histories to guide software changes, IEEE TSE 31(6), 429–445

Read in full, 22 November 2026, from the first author's site
(thomas-zimmermann.com/publications/files/zimmermann-tse-2005.pdf; 17 pp., published layout).

## What it does

- ROSE mines association rules from CVS transactions ("Programmers who changed these functions
  also changed...") at file and at fine granularity (functions, fields). Eight open-source
  projects. Evaluation by precision/recall of predicted further changes, and of warnings about
  missing changes.
- Abstract: "ROSE's topmost three suggestions contained a correct location with a likelihood of
  more than 70 percent." Conclusions (§9): for GCC, recommendations in 63% of transactions; for
  rapidly evolving systems (KOffice) the useful suggestions are at file level, since ROSE "would
  have to predict new functions—which is probably out of reach for any approach"; 2–7% of
  erroneous transactions have the missing change detected, with 2% false alarms.

## Change size

- Data cleaning: "noise, caused by large transactions, is removed" (§3): transactions that
  "affect more than 30 entities" are dropped. That is a filter, not a control; no analysis is
  conditioned on the size of the change.

## Cause

- Purely predictive. The rules "describe the factual software process—which may or may not be the
  intended process" (§9). Evolutionary coupling is presented as coupling "undetectable by program
  analysis" (abstract), not as evidence of poor cohesion or misplaced responsibility.

## Bearing

- H6: compatible. ROSE claims that co-change predicts *where else* a change goes, not *why*.
  "Co-change spread does not see the force" contradicts nothing here.
- Its observation that prediction is best "for changes to existing software" and that new
  functions are out of reach is a reminder that co-change models describe the established
  structure, which is where a forced change goes by definition.
- No forced/chosen distinction, no access.

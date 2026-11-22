# Vidal, Bergel, Marcos and Díaz-Pace (2016), over-exposed methods (EMSE 21(2), 483–516) and over-exposed classes (COMLAN 46, 1–19)

Read 22 November 2026: both read in full for research questions, results, evolution sections and
conclusions (pattern formalisation and the plugin sections skimmed). Sources: Internet Archive
copies (12 June and 9 May 2024) of the accepted manuscripts in the University of Chile repository
(repositorio.uchile.cl, handles 2250/141895 and 2250/146266); the live repository now answers with
an access check.

## Methods (EMSE 2016)

- 3.6 MLOC of open-source Java; "at least 20 % of defined methods are over-exposed" (abstract);
  over 70% of application methods are public (Q1); libraries have more over-exposed methods (Q2).
- Evolution (Q3): "less than 10 % of the over-exposed methods defined in early versions of the
  applications become non-over-exposed in future versions" (§10).
- No fields: the study is of methods only. No link from an exposure to the change that needed it.

## Classes (COMLAN 2016)

- 30 systems (15 libraries, 15 applications); about 87% of classes public, "around 35% of the
  public classes are over-exposed" (RQ2; abstract: "an average of 25% of classes").
- RQ4: "96.69% of the over-exposed public classes have an access modifier broader than necessary
  since their creation"; per application, 13 of 14 above 90%.
- Persistence: of 2,513 over-exposed classes in first versions, 2,161 (86%) stay over-exposed
  without intermediate change until the last version or deletion.
- RQ5: "we could not find evidence that over-exposed classes are a major contributor to
  modularity problems"; "the existence of new references from classes outside the 'minimal'
  accessibility are unusual" (§7).
- Related work (§10) cites Kobori et al. [19]: "they reported that the change of access modifiers
  of methods is infrequent. They also found that the number of over-exposed methods and fields
  tends to increase in time."

## Corrections to LITERATURE.md §10

- 18 November: "90% of over-exposed classes are so from their first version (abstracts)". The
  paper gives 96.69% overall and "around 90%" in its introduction; the statement stands, with the
  exact figure now known.
- 20 November: "changes of access modifier are reported as infrequent (cited in Vidal et al.,
  source not traced)". Traced: the claim is Kobori et al. 2015 as reported in the classes paper's
  related work; the methods paper's own Q3 (fewer than 10% of over-exposed methods are ever
  narrowed) supports it for narrowing.

## Bearing

- H7 (widening branch): exposure is mostly set at creation and rarely changed afterwards, and
  over-exposure is mostly unused (few new references from outside the minimal accessibility). So
  a change that *uses* an already exposed member is the common dispersion path, and widening at
  the moment of a change should be rare. That matches the development chain's low "members
  opened" ratio and argues for reporting widening as a rare event, not a main term.
- Forced definition: these papers make access a declared, mostly static property. The plan's
  "forced by encapsulation" uses exactly that property, read at the commit.

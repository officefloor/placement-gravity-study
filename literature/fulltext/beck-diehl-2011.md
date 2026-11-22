# Beck and Diehl (2011), On the congruence of modularity and code coupling, ESEC/FSE 2011

Read in full, 22 November 2026, from the second author's page at Trier
(st.uni-trier.de/diehl/pubs/esecfse11.pdf; 11 pp., published layout).

## What it does

- 16 Java projects from SourceForge. Compares the package structure with six coupling concepts:
  structural dependencies (inheritance, aggregation, usage), fan-out similarity, evolutionary
  coupling (support, confidence), code ownership, code clones (Type I, II), semantic similarity
  (tf-idf, LSI). A congruence measure between each coupling graph and the package hierarchy.
- "we omit large transactions (transactions including more than 25 classes) to reduce noise"
  (§2.2.3). No per-change size control.

## What it says

- Each modularity principle is given a conjectured coupling signature. For information hiding:
  "hiding design decisions increases the changeability of a system because changing a design
  decision causes only local changes in one module. Hence, information hiding should rather lead
  to local changes, which result in local evolutionary coupling" (§2.2.3).
- Results: evolutionary coupling is congruent with package structure about as much as aggregation
  and usage dependencies, with the best density; Discussion: "Information hiding (P2) seems to
  play a major role in the analyzed projects as the high congruence values for internal fan-out
  similarity (FO) and evolutionary coupling (EC) suggest." Conclusion: "none of the principles is
  exclusively dominating"; inheritance fan-out similarity has the highest congruence.
- Coupling concepts are "quite independent", each with different information (§3.1); "the term
  coupling is not necessarily directed and is neutral with respect to causality" (§2.2).

## Bearing

- Encapsulation and co-change: Beck and Diehl read co-change *within* a package as the trace of
  information hiding. That is the concentration side of encapsulation seen in co-change, at the
  package level, as an aggregate congruence, not per change.
- H6: compatible. They read co-change as evidence of a design principle in aggregate, not as
  revealing the cause of a particular change; they explicitly treat coupling as neutral with
  respect to causality.
- No forced/chosen distinction; no size control.

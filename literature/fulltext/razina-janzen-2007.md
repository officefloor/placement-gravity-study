# Razina and Janzen (2007), Effects of dependency injection on maintainability

Read in full, 22 November 2026, from the Internet Archive copy (9 September 2024) of the Cal Poly
DigitalCommons PDF (digitalcommons.calpoly.edu/csse_fac/34; the live file is behind a browser
check). Six pages. The paper number "591-111" is printed on it, consistent with the repository's
attribution to IASTED (Software Engineering and Applications, 2007); the venue is still not
confirmed from the text itself.

- 20 pairs of SourceForge Java projects, one using Spring dependency injection and one similar
  project not using it; a "Number of DIs" metric; CBO, RFC and LCOM per project; ANOVA and t-tests.
- Abstract: "no correlation was evident between the use of dependency injection and coupling and
  cohesion numbers. However, a trend towards lower coupling numbers in projects with a dependency
  injection count of 10% or more was observed."
- Pairs are matched by domain, not by problem: different projects, different code.

## Bearing

- H4: the nearest earlier contrast of an injected against a non-injected construct, and it found
  no difference at project level. The plan's design (same problem stream, two constructs, per
  change) is what it lacked. Not about placement or encapsulation. The §10 abstract-based
  statement is confirmed.

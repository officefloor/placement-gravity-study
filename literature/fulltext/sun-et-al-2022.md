# Sun, Kim, Ming and Lu (2022), Measuring impact of dependency injection on software maintainability, *Computers* 11(9), 141

Read in full, 22 November 2026, from the publisher's open-access PDF (MDPI, via the Internet
Archive copy, the live link being behind a browser check). A shorter earlier version is
arXiv:2205.06381 (Sun and Kim, three pages), also seen.

- Proposes DI-weighted afferent coupling (DCE) and DI-weighted CBO (DCBO); a tool (CKJM-Analyzer)
  to detect injection statically; controls for size by normalising CBO and DCBO.
- Conclusions (§7): "small projects see an increase in coupling due to overhead caused by DI
  injection, while open-source results reflect an increase in coupling as DI increases ... We
  argue that DI may contribute to more maintainable software by reducing the developer 'effort'
  when a dependency change is required."

## Bearing

- H4: injection *raises* coupling as counted by CBO (the injected types are dependencies). That is
  the plan's point that the function arm's coupling "appears as wiring (§4.5) and is reported, not
  hidden": a construct that removes the encapsulation force is expected to show more explicit
  coupling, not less. The §10 description (20 November: "Sun et al. propose DI-weighted CBO") was
  correct but omitted this result, which is the part that bears on H4.

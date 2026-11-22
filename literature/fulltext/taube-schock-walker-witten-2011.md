# Taube-Schock, Walker and Witten (2011), Can we avoid high coupling?, ECOOP 2011, LNCS 6813, 204–228

Read in full, 22 November 2026, from the University of Waikato repository copy (Research
Commons, author version, 25 pp.).

- Model: preferential attachment with an attachment probability based on an entity's utility,
  plus "practical limits on module sizes". Prediction: both overall connectivity and
  between-module connectivity (coupling) are approximately scale-free.
- Data: 97 open-source Java systems, a fine-grained graph (packages, classes, methods, blocks,
  statements, variables; calls, type use, variable use, inheritance).
- Conclusion (§7): "Regardless of maturity, size, modification history, and the size of the user
  community, all these systems exhibit a similar scale-free dependency structure ... The links of
  highly connected source code entities were not generally resolved within-module, and our model
  indicates that this is due to practical limits on module sizes ... high coupling is
  impracticable to eliminate entirely ... some high coupling is necessary for good design."

## Bearing

- The size–coupling trade is explicit here: high-degree entities couple across modules *because*
  modules cannot grow without limit. That is the concentrate-or-disperse choice of H2/H7 at the
  level of a whole system's degree distribution, with size limits as the reason dispersion
  happens. It is not per change, and access plays no part.
- H7's tail coupling term: this is the reason the plan holds unavoidable tail coupling fixed; the
  paper supports doing so.
- "Regardless of maturity, size, modification history" is an invariance claim about systems, the
  nearest empirical analogue found to "a physics regardless of author", though authorship is not
  varied.
- The §10 abstract-based description (20 November) is confirmed.

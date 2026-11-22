# Steimann and Thies (2009), From public to private to absent: refactoring Java programs under constrained accessibility, ECOOP 2009, LNCS 5653, 419–443

Read 22 November 2026 (introduction, the constraint rules in outline, the evaluation §5.5 and
the conclusion in full; the formal rules skimmed), from the first author's group page
(fernuni-hagen.de/ps/pubs/ECOOP2009.pdf, 25 pp., the authors' version).

## What it does

- Formalises Java's access control as constraint rules, so that Move Type/Member and Pull Up/Push
  Down refactorings can check preconditions and compute the access-modifier changes needed to
  keep a program's meaning.
- Opening quote (from Fowler): "Moving state and behavior between classes is the very essence of
  refactoring."
- Introduction: "while insufficient accessibility is routinely reported by the compiler, excessive
  accessibility is usually not and therefore often forgotten".

## The number that matters here (§5.5)

Applying Eclipse's Move Class to four programs (JUnit 3.8.1, Jester, JHotDraw 6.01b,
Apache Commons IO): "if the refactoring is allowed to change access modifiers, preconditions
predict that it can be applied in 99% of all cases, compared to 85% if no changes are allowed."
So about one move in seven of a class needs some access modifier changed. Pull Up Method shows a
similar but noisier pattern.

## Bearing

- H7 (widening): moving code across a class boundary often requires access to change. This is
  for deliberate re-placement (refactoring), not for a change that adds behaviour; but it is the
  only measured figure found for how often placement and access interact.
- Encapsulation as a force: implicitly; access constraints restrict where members may be moved
  without widening. Not framed as a force and not measured on histories.
- Earlier §10 wording ("refactorings must sometimes widen access ... index record only") is
  confirmed.

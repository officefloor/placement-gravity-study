# Palomba, Bavota, Di Penta, Oliveto, Poshyvanyk and De Lucia (2015), Mining version histories for detecting code smells, IEEE TSE 41(5), 462–489

Read in full, 22 November 2026 (detection heuristics, study design, results and the developer
study; the related-work section skimmed), from the Internet Archive copy (18 July 2024) of the
authors' accepted manuscript at iris.unisa.it/bitstream/11386/4590057/4/J1.pdf.

## What it does

- HIST detects five smells from fine-grained co-change (association rules on methods committed
  together): Divergent Change, Shotgun Surgery, Parallel Inheritance, Blob, Feature Envy. Twenty
  Java projects with a hand-built oracle; then a study with developers of the systems.
- Abstract: precision 72–86%, recall 58–100%.
- Shotgun Surgery (§2.2.2): "a class is identified as affected by a Shotgun Surgery smell if it
  contains at least one method that changes with methods present in more than δ different
  classes." Divergent Change (§2.2.1): at least two sets of methods in a class that change
  together within a set and not across sets.
- No control for the size of a commit; thresholds (support, confidence, δ, α, β) calibrated on one
  system (§3.1.4).

## What it says about cause

- Smells are framed as symptoms with refactorings as cures: Divergent Change "clearly triggers
  Extract Class"; Shotgun Surgery "can be removed through a Move Method/Field refactoring ... the
  method/field causing the smell is moved towards the class in which its changes trigger more
  modifications" (§1).
- Developer study: for Divergent Change "Most of these developers pointed out low cohesion of the
  class as the root cause"; the authors: "Low cohesion of classes is clearly a symptom of a
  Divergent Change smell."
- Two passages that cut the other way:
  - The oracle rejected a co-change across four methods in three classes because "they are
    correctly placed into different classes splitting well the system's responsibilities ...
    even if they co-change during time, there is no apparent reason for placing them in the same
    class with the only goal of isolating the change" (§3.2.2). Co-change across classes is not,
    by itself, misplacement.
  - A developer on a Shotgun Surgery instance in Android's `Handler`: "At first glance the
    coupling looks like a problem, but these classes are best viewed as one unit ... There may
    also be performance benefits of accessing members in the other classes directly. For example,
    mLooper.mQueue instead of mLooper.getQueue()." The authors: "it is a symptom in the code that
    may (or may not) indicate a design problem" (§4.2).

## Bearing

- H6: compatible, and partly supportive. HIST does read co-change as a symptom whose cause is
  misplaced responsibility or low cohesion, and the developers mostly agreed. But the paper itself
  shows co-change spread across correctly placed classes, and a case where the co-change comes
  from direct access to another class's members, accepted as design. It never asks what forced a
  change into the classes it touched.
- The developer quote is the one place in this group where access (direct member access instead
  of a getter) appears as the reason classes change together. Incidental.
- No change-size control; no forced/chosen distinction.

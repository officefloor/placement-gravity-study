# Gall, Hajek and Jazayeri (1998), Detection of logical coupling based on product release history, ICSM 1998, 190–197

Read in full, 22 November 2026, from the copy on a University of Waterloo course page
(plg.uwaterloo.ca/~migod/846/papers/gall-coupling.pdf; 9 pp., the published layout).

## What it does

- Data: 20 releases over 21 months of a telecommunications switching system (over 10 MLOC; 8
  subsystems, 47–49 modules, 1,500–2,300 programs per release). Unit of change: a **release**,
  not a commit or a change request. A program's "change sequence" is the list of releases in
  which its version number changed (§4.1).
- CAESAR: Change Sequence Analysis (programs or subsystems sharing a subsequence of release
  numbers are "logically coupled"; longer shared subsequences are taken as stronger coupling)
  and Change Report Analysis (verifying a coupling when change reports for both programs cite the
  same bug report).
- No statistics, no control for the size of a change or of a module; results are illustrative
  (Figures 3–7, a few programs and bug reports).

## What it claims about cause

- Introduction: code-based coupling measures "do not reveal all dependencies ... The software
  engineer just 'knows' that to make a change of a certain type, he or she has to change a certain
  set of modules."
- §2: "If programs change together across module or subsystem boundaries, the decomposition
  structure of the application should be reconsidered and possibly restructured."
- §6: "Our technique reveals hidden dependencies not evident in the source code, identifies
  modules that should undergo restructuring".
- So: co-change is read as revealing a **hidden dependency** and a **structural shortcoming**
  (a cause in the design), to be fixed by restructuring. This is asserted, not tested.

## A finding that bears on H6 directly

§5: "subsystem C was continuously growing over the 20 releases ... but this fact is not reflected
in a high logical coupling with other subsystems. The potential for restructuring is, therefore,
within subsystem C and its modules. The structural shortcoming is local in terms of subsystems but
with a high interrelationship among modules of subsystem C." The one subsystem that grew most did
not show up as coupled to others: growth by concentration was invisible to cross-boundary logical
coupling and was found only by looking inside it.

## Bearing

- H6 (spread does not see the force): compatible, and the subsystem C remark is an anecdotal
  instance of it (concentration invisible to co-change across boundaries). Gall et al. do claim
  co-change reveals a cause (hidden dependency, poor decomposition), which is the reading H6
  argues against; but they offer no test of it.
- No control for change size; no notion of a forced change or of access.
- H7: no measure of calls; logical coupling is explicitly contrasted with code coupling.

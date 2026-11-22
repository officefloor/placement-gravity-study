# Ousterhout, *A Philosophy of Software Design* (Yaknyam Press, 2018; 2nd ed. 2021)

**Book not read** (not freely available; the online "copies" and translations found are not
authorised and were not used). What was read, 22 November 2026, is what the author publishes
himself:

- CS 190 lecture notes, "Modular Design" (Stanford, Spring 2016),
  web.stanford.edu/~ouster/cgi-bin/cs190-spring16/lecture.php?topic=modularDesign. Read in full.
- CS 190 notes, "Discussion of 'A Philosophy of Software Design'" (Winter 2021): only a list of
  the book's topics ("Deep and shallow classes", "Temporal design vs. information hiding",
  "Pull complexity downwards", ...).

## What the 2016 notes say

- "Goal for interface design: maximize functionality/(interface complexity)".
- "Opposite of information hiding: information leakage. Implementation details exposed, other
  classes depend on them. Information hiding works inside a class as well as between classes".
- "Classes Should be Thick ... Lots of functionality, yet simple interface. Hides lots of
  information". "Rule of thumb: 200-2000 lines is a good size for classes ... However, size itself
  isn't the most important metric: it's functionality/(interface complexity)".
- "When to bring things together into one class ... Bring together if: Shared information: when
  you see information leakage, see if you can pull the code together ... Benefits of bringing
  together: Eliminates dependencies". "Separate if: There isn't much shared information".

## Bearing

- The notes are the design-advice form of the concentration/dispersion trade: concentrate where
  information is shared (fewer dependencies, a larger class), separate where it is not. That is
  H2's and H7's mechanism stated as a recommendation, with the valence opposite to "gravity as a
  harm": concentration around shared data is advised.
- "functionality/(interface complexity)" is a surface-against-volume ratio, as recorded on 20
  November ("deep module"); the 2016 notes say "thick", the book says "deep".
- No measurement, no notion of a forced change. The §10 wording ("deep module", "information
  leakage") is confirmed for leakage and for the ratio; "deep" itself is confirmed only as a
  book topic in the 2021 notes.

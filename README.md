# Placement gravity

Where does the code for a new problem land, and did it have a choice?

The earlier studies looked for bad code in the shape of code as it stands, and found that the
problem fixes the amount (*Conserved amount, negotiable placement*). This study changes the
unit of analysis to **each new problem as it arrives**. It assumes the code added for a problem
is cohesive with that problem, and measures how that code was placed:

- in a new unit or an existing one;
- how far it is dispersed;
- its **pull**: how much pre-existing host state it had to read or write. Pull separates a
  **forced** placement (gravity) from a **chosen** one.

It then follows each problem forward to see whether forced placements are what tangle later
changes. The primary data is the paired Spring and OfficeFloor change streams of the degradation
harnesses, where one checkpoint is one problem.

| Read | For |
|---|---|
| [`PLAN.md`](PLAN.md) | The study: questions, hypotheses H1–H3, measures, analysis. **Draft, not registered.** |
| [`LITERATURE.md`](LITERATURE.md) | The literature: notes by theme, the systematic novelty check (§10), and the full references. |

No code yet.

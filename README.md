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

Shape is read only where the problem is fixed. The measures of solution shape used by the earlier
studies (long, not slimmable, junction, complexity outlier, concentration) enter as competitors:
H2 tests whether they predict anything once the problem and the ties are held fixed. The plan
absorbs three drafts that read the same runs: flow-injection containment, the ui harness's
SinewSlim analysis plan, and sinew identification (`PLAN.md` §1.1).

| Read | For |
|---|---|
| [`PLAN.md`](PLAN.md) | The study: questions, hypotheses H1–H3, measures, analysis. **Draft, not registered.** |
| [`LITERATURE.md`](LITERATURE.md) | The literature: notes by theme, the systematic novelty check (§10), and the full references. |
| [`results/pilot/PILOT.md`](results/pilot/PILOT.md) | The pilot: the instrument on one pair of chains, what it showed, the decisions it raised. |

## Running

```sh
./setup.sh    # .venv, the pinned OfficeFloorSlim 0.5.4 jar (sha256-checked), RefactoringMiner and
              # CodeTracker (Maven), the instrument, the tests. Needs JDK 17+ and Maven.
./pilot.sh    # the pilot: chain 9 of blind-202608100006/just-solve, both arms -> results/pilot/
```

The pilot reads the harness's local clones (`~/compare/spring`, `~/compare/officefloor`) and its
stream (`~/spring-petclinic-rest-long-degradation-test/checkpoints.yaml`). The same branches are
published in `officefloor/spring-petclinic-rest`.

| Code | |
|---|---|
| `instrument/Pull.java` | The instrument: per addition, hosts, runs and their ties (method and class), birth ties, moved code; the amount; with `--shape`, every method of a tree as the earlier studies read it (SinewSlim's length and assessment, junction counts). |
| `refactor/` | RefactoringMiner 3.0.4 at each commit (`Refactorings.java`) and CodeTracker 2.6 histories (`Histories.java`), built by Maven. |
| `placement_gravity/refactor.py` | RefactoringMiner's findings as the instrument's hints: renames, matches, moved code. |
| `placement_gravity/crosscheck.py` | CodeTracker against the instrument's following of hosts. |
| `placement_gravity/chain.py` | A chain's checkpoints from git, the files of each addition, the wiring. |
| `placement_gravity/tables.py` | Hosts, runs, additions and outcomes from the instrument's output. |
| `placement_gravity/shape.py` | The shape competitors S1–S5 (PLAN.md §4.7) on each existing host at k − 1, with the complexity-concentration study's cognitive extractor and outlier rule (pinned in `requirements.txt`). |
| `placement_gravity/pilot.py` | The pilot. |
| `tests/` | Fixtures with known answers. |

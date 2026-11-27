# Results

Every analysis read so far, in the order of `runs.yaml`, with each hypothesis's verdict and the p it was decided on (after Holm for H1, H2, H4 and H5). Each analysis is read on its own and none is pooled; the study's test is the primary one. A development analysis is descriptive only. H8 is Run D's test and H9 Run C's, each read in its own analysis, where H1 to H7 are descriptive.

| Analysis | Role | Read by | H1 | H2 | H3 | H4 | H5 | H6 | H7 | H8 | H9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [pilot](pilot/REPORT.md) | development | steps 03 to 08 | descriptive only (p 1.000) | descriptive only (p 0.003) | descriptive only (p 0.001) | descriptive only | descriptive only (p 1.000) | descriptive only (p 3.06e-06) | descriptive only (p 0.349) | – | – |
| [open-source-development](open-source-development/REPORT.md) | development | steps 03 to 08 | descriptive only | descriptive only (p 0.010) | descriptive only (p 0.005) | descriptive only (p 1.000) | descriptive only | descriptive only (p 0.033) | descriptive only (p 0.002) | – | – |

## The main figure of each hypothesis

One figure a hypothesis, with its interval (95%; H6 and H7 90%, against the margin 1.25): the cluster bootstrap's where the test is decided on it, Wald where there is one chain an arm or on a history. A dash: the analysis cannot give it (a history has no arm contrast on the same problems), or it could not be fitted. A ratio is function arm / methods arm unless it says otherwise. The figure does not decide by itself: each hypothesis has more than one part and its conditions, which the analysis's own report gives.

| Analysis | H1 forced | H2 core | H2 arms | H3 rise | H4 come back to | H4 files | H5 links | H6 shape | H7 spread | H8 open | H9 bound |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [pilot](pilot/REPORT.md) | 0.247 [0.093, 0.654] | 18.156 [12.455, 26.465] | 0.106 [0.026, 0.425] | 0.015 [0.007, 0.022] | 0.162 [0.098, 0.268] | 0.603 [0.489, 0.743] | 1.047 [0.909, 1.205] | 0.349 [0.219, 0.555] (m_cyclomatic) | 1.026 [0.445, 2.365] | – | – |
| [open-source-development](open-source-development/REPORT.md) | – | 2.933 [2.578, 3.193] | – | 0.511 [0.375, 0.734] | 0.075 [0.027, 0.210] | – | – | 1.096 [0.976, 1.232] (s4_cognitive) | 0.845 [0.673, 1.061] | – | – |

- **H1 forced:** placements forced at the class a checkpoint, function arm / methods arm, half-way through the stream (below 1)
- **H2 core:** later uses of a core value / of a periphery value, at the class, in the methods arm (above 1)
- **H2 arms:** later uses of a core value at the method, function arm / methods arm (below 1)
- **H3 rise:** the slope of an addition's bystanders on the checkpoint index, in the methods arm (above 0; a slope, not a ratio)
- **H4 come back to:** later intrusion at the class, function arm / methods arm (below 1)
- **H4 files:** how well-trodden the files gone back into are, function arm / methods arm (below 1)
- **H5 links:** weighed links per unit of logic, function arm / methods arm, half-way through the stream (below 1)
- **H6 shape:** of the shape measures tested, the one whose ratio of later intrusion is highest (each to be shown below 1.25)
- **H7 spread:** classes a change goes into beyond the first, forced change / unforced (to be shown below 1.25)
- **H8 open:** Run D only: later intrusion at the class, nothing private / encapsulated (below 1)
- **H9 bound:** Run C only: bindings a run, the other arm less the no-injection control, in log(1 + bindings) (below 0; a difference, not a ratio)

## Still to come

- **What exists today** (steps 03 to 08): not analysed yet: petclinic-just-solve-202608100006, petclinic-impact_gated-202609010045, petclinic-impact_gated-202609031757, petclinic-cohesion-prompt-202609160027, petclinic-reviewed-202609290948, petclinic-just-solve-202608011310, petclinic-just-solve-full-202608102319, petclinic-just-solve-202608081920, open-source-human, open-source-human-confirm, open-source-agent-within, open-source-agent-against-human
- **Run B** (step09_run_b.sh): not analysed yet: ui-primary, ui-angular, ui-tanstack
- **Run C** (step10_run_c.sh): not in `runs.yaml` yet; added by a dated amendment before any of its backend Java is read
- **Run D** (step11_run_d.sh): not in `runs.yaml` yet; added by a dated amendment before any of its backend Java is read

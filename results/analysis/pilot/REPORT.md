# pilot

Role: **development**. Chains: officefloor 1, spring 1. **Descriptive only.**

| Hypothesis | Verdict | p (Holm) |
|---|---|---|
| H1 | descriptive only | 0.003 |
| H2 | descriptive only | – |
| H3 | descriptive only | 0.992 |
| H4 | descriptive only | 0.003 |

## H1, gravity compounds (methods arm)

Runs that need a pre-existing value 91 over 1 chains; the slope of log(1 + bystanders) on the checkpoint index, cluster-bootstrap 95% interval (1000 refits).

- **Bystanders on the checkpoint index: 0.015 [0.015, 0.015]**
- **Within a class, the class's bystanders: 0.026 [0.026, 0.026]** (3 classes with runs at two or more checkpoints)
- **Within a method, the method's bystanders: 0.023 [0.023, 0.023]** (11 methods)
- Reported, within a place in the function arm: class 0.001 [0.001, 0.001]; method -0.001 [-0.001, -0.001]
- Reported, method bystanders 0.004 [-0.006, 0.013]; class bystanders 0.016 [0.010, 0.022]
- Reported, without injected dependencies 0.024 [0.016, 0.031]; without constants 0.003 [-0.005, 0.012]
- Reported, the function arm's slope: -0.000263 [-0.011, 0.010]
- Reported, officefloor: 56 of 168 runs need a pre-existing value (0.667 free); per such run, needed 1.554, bystanders 1.179 (method 0.929, class 0.250; without constants 1.036); over the thirds of the stream 1.455, 0.889, 1.167; fields left behind per addition 0.455
- Reported, spring: 91 of 162 runs need a pre-existing value (0.438 free); per such run, needed 1.407, bystanders 10.890 (method 2.582, class 8.308; without constants 5.934); over the thirds of the stream 5.917, 10.172, 14.579; fields left behind per addition 0.610
- Reported, H1 as first registered (ties of runs into existing methods): on log(host positions) 0.030 [-0.042, 0.103]; on the checkpoint index 0.006 [0.002, 0.011]
- Reported, ties in the function arm: on host size 0.098 [-0.084, 0.279]
- Reported, ties at class level (methods arm): on class size -0.010 [-0.119, 0.100]
- Reported, ties without injected dependencies: on host size 0.080 [-0.000316, 0.160]; class level on class size -0.040 [-0.125, 0.045]

## H2, data draws code in (methods arm)

Where code was tied to a class or a method (109 of 350 problem and host rows, both arms; 83 in the methods arm): the later intrusions there that are tied to a value which stood by at the placement, as a rate ratio per value that stood by.

- **At the class (its fields): 1.099 [1.038, 1.164]**
- **At the method (its values): not estimated (standard error not computed: bystanders_method)**
- Reported, officefloor: 31 tied rows; at the class 0.548 fields stood by, 3 of 26 later intrusions tied to one of them (0.115); at the method 0.903 values stood by, 1 of 3 (0.333)
- Reported, spring: 89 tied rows; at the class 7.472 fields stood by, 449 of 1056 later intrusions tied to one of them (0.425); at the method 2.236 values stood by, 43 of 292 (0.147)
- Reported, on log(1 + bystanders): class 1.042 [0.593, 1.491]; method not estimated (standard error not computed: log_by_method)
- Reported, the function arm: class 810508952663.495 [4.53e-99, 144926924589198000744940790788170766801987441848091268080083565762570760781355119429063249789257857706815653466801541480448.000]; method not estimated (standard error not computed: bystanders_method)
- Reported, H2 as it stood until 17 November 2026 (later intrusion per tie): class 0.890 [0.745, 1.064]; method 0.853 [0.607, 1.199]
- For information, the same on the problem's own lines: not estimated (standard error not computed: tie)
- Reported, per tie, any later change, tied or not: class 0.857 [0.717, 1.023]; method 0.748 [0.524, 1.067]
- Reported, per tie, existing hosts only: class 0.916 [0.808, 1.039]; method 0.949 [0.667, 1.350]
- Reported, per tie, without injected dependencies: class 0.812 [0.696, 0.948]; method 0.922 [0.654, 1.301]

## H3, shape adds nothing

- **against**; bound 0.800 to 1.250, 90% intervals, method-level intrusion, the ties and the bystanders in the model (n = 77)
  - s3_junction: 0.709 [0.301, 1.672], TOST p 0.592
  - s4_cognitive: 0.380 [0.230, 0.629], TOST p 0.992
  - s5_class_gini: 0.677 [0.408, 1.123], TOST p 0.706
  - Left out by the variation rule: s1_long ({'officefloor': 1, 'spring': 22}), s2_stuck ({'officefloor': 0, 'spring': 0})
- Reported, the same on class-level intrusion: s3_junction 0.589 [0.400, 0.866]; s4_cognitive 0.855 [0.702, 1.041]; s5_class_gini 1.487 [1.168, 1.891]
- Reported, shape without the problem terms, the ties and the bystanders: s3_junction 9.030 [3.632, 22.446]; s4_cognitive 0.948 [0.594, 1.513]; s5_class_gini 0.609 [0.335, 1.107]
- Reported, junction × arm (s3_junction): 0.411 [0.027, 6.349]
- Reported, junction × arm (s3_junction_injection_aware): 0.314 [0.020, 4.863]

## H4, function injection keeps the space open

- **Function arm's bystanders (arm term, at checkpoint 30.5, the middle of the stream): -1.586 [-1.586, -1.586]**
- **Their slope on the checkpoint index (interaction): -0.017 [-0.017, -0.017]**
- **Later intrusion where tied code was placed, function arm / methods arm: at the class 0.162 [0.098, 0.268]; at the method 0.110 [0.029, 0.426]**
- Reported, officefloor: per checkpoint, classes its tied code goes back into 0.233, wiring files changed again 0.450
- Reported, spring: per checkpoint, classes its tied code goes back into 0.883, wiring files changed again 0.000
- Reported, reopening, function arm / methods arm: classes 0.264 [0.147, 0.476]; with wiring files 0.774 [0.515, 1.163]
- Reported, bystanders without injected dependencies: arm -1.201 [-1.448, -0.953], slope -0.029 [-0.041, -0.017]
- Reported, the needed values, function arm against methods arm: 0.030 [-0.053, 0.114] (expected about 0: the same stream)
- Reported, H4 as first registered (ties): arm at a host of 7.3 positions -0.404 [-0.558, -0.250]; slope on host size 0.046 [-0.120, 0.211]
- Reported, the arm difference in ties at a host of 10 positions -0.389 [-0.560, -0.219]; 25 positions -0.347 [-0.622, -0.073]; 50 positions -0.316 [-0.691, 0.060]
- Amount added since the base, function arm / methods arm at the final checkpoint: 1.076 [1.076, 1.076], in band: yes
- Reported, the ratio of the totals: 0.884
- Wiring growth: slope -0.012, interval None, against: –
- Wiring concentration: largest file 0.160, against: no
- Reported, ties without parameters: arm -0.201 [-0.365, -0.036], slope 0.029 [-0.126, 0.184]
- Reported, ties without injected dependencies: arm -0.295 [-0.454, -0.137], slope -0.021 [-0.193, 0.151]
- Reported, trajectory of the ties (arm × checkpoint): 0.0007 [-0.007, 0.009]

## Reported readings: choice, formation, review

- Choice, officefloor: 0 of 0 checkpoints left no choice (every chain with the same ties, on the same side of new or existing); median spread of ties over chains –, median distinct hosts –
- Choice, spring: 0 of 0 checkpoints left no choice (every chain with the same ties, on the same side of new or existing); median spread of ties over chains –, median distinct hosts –
- Formation, lagged, officefloor: ties now on the chain's mean ties so far -1.217 [-5.094, 2.660] (predicted above 0 in the methods arm)
- Formation, lagged, spring: ties now on the chain's mean ties so far -0.884 [-2.702, 0.934] (predicted above 0 in the methods arm)
- Capture, officefloor: share of the addition landing in existing hosts on the fields held by the chain's heaviest class 0.217 [0.021, 0.413] (predicted above 0 in the methods arm)
- Capture, spring: share of the addition landing in existing hosts on the fields held by the chain's heaviest class 0.315 [0.062, 0.567] (predicted above 0 in the methods arm)
- Size or data, at the class (both arms pooled, no arm term, n = 77): later intrusion per value that stood by, size held fixed, 0.878 [0.835, 0.924] (predicted above 1); per log of size, with what stood by held fixed, 3.054 [2.080, 4.483]; size alone 1.781 [1.312, 2.419]; within arms, bystanders 0.883 [0.842, 0.926] and size 2.674 [1.951, 3.664]; Spearman's rho of size with what stood by: pooled 0.952, officefloor 0.574, spring 0.943
- Size or data, at the method (both arms pooled, no arm term, n = 109): later intrusion per value that stood by, size held fixed, 0.888 [0.766, 1.030] (predicted above 1); per log of size, with what stood by held fixed, 4.800 [2.523, 9.135]; size alone 3.271 [2.166, 4.941]; within arms, bystanders 0.888 [0.768, 1.027] and size 4.686 [2.496, 8.797]; Spearman's rho of size with what stood by: pooled 0.813, officefloor 0.499, spring 0.867
- Formation, where it ends, officefloor: Spearman's rho of early ties with the largest method's share – [no interval] over 1 chains (predicted above 0 in the methods arm)
- Formation, where it ends, spring: Spearman's rho of early ties with the largest method's share – [no interval] over 1 chains (predicted above 0 in the methods arm)
- Own lines followed, officefloor: 582 placed, 0 lost track of (0.0%)
- Own lines followed, spring: 537 placed, 0 lost track of (0.0%)

## Provenance

Checkpoint intercept in the model: H1 no, H4 no, H2_class yes, H2_method no, H4_intrusion_class no, H4_intrusion_method yes, H3 yes.

Versions: {"R": "R version 4.5.2 (2025-10-31)", "glmmTMB": "1.1.14", "TMB": "1.9.19"}. Seed 20261116.

Registered files changed since `plan-v1` (amendments, PLAN.md §9): `PLAN.md`, `analysis/analyse.R`, `analysis/selftest.R`, `instrument/Pull.java`, `placement_gravity/chain.py`, `placement_gravity/lines.py`, `placement_gravity/measure.py`, `placement_gravity/pilot.py`, `placement_gravity/prepare.py`, `placement_gravity/readings.py`, `placement_gravity/report.py`, `placement_gravity/shape.py`, `placement_gravity/tables.py`, `placement_gravity/verdict.py`, `placement_gravity/wiring.py`.

| Arm | Run | Chain | Commit |
|---|---|---|---|
| officefloor | blind-202608100006 | 9 | `b824bf9d48e7` |
| spring | blind-202608100006 | 9 | `b48eb0cc333b` |

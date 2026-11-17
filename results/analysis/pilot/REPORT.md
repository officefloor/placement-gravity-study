# pilot

Role: **development**. Chains: officefloor 1, spring 1. **Descriptive only.**

| Hypothesis | Verdict | p (Holm) |
|---|---|---|
| H1 | descriptive only | 0.003 |
| H2 | descriptive only | 0.945 |
| H3 | descriptive only | 0.003 |

## H1, gravity compounds (methods arm)

Runs that need a pre-existing value 91 over 1 chains; the slope of log(1 + bystanders) on the checkpoint index, cluster-bootstrap 95% interval (1000 refits).

- **Bystanders on the checkpoint index: 0.015 [0.015, 0.015]**
- Reported, method bystanders 0.004 [–, –]; class bystanders 0.016 [–, –]
- Reported, without injected dependencies 0.024 [–, –]; without constants 0.003 [-0.005, 0.012]
- Reported, the function arm's slope: -0.000263 [-0.011, 0.010]
- Reported, officefloor: 56 of 168 runs need a pre-existing value (0.667 free); per such run, needed 1.554, bystanders 1.179 (method 0.929, class 0.250; without constants 1.036); over the thirds of the stream 1.455, 0.889, 1.167; fields left behind per addition 0.455
- Reported, spring: 91 of 162 runs need a pre-existing value (0.438 free); per such run, needed 1.407, bystanders 10.890 (method 2.582, class 8.308; without constants 5.934); over the thirds of the stream 5.917, 10.172, 14.579; fields left behind per addition 0.610
- Reported, H1 as first registered (ties of runs into existing methods): on log(host positions) 0.030 [-0.042, 0.103]; on the checkpoint index 0.006 [0.002, 0.011]
- Reported, ties in the function arm: on host size 0.098 [-0.084, 0.279]
- Reported, ties at class level (methods arm): on class size -0.010 [-0.119, 0.100]
- Reported, ties without injected dependencies: on host size 0.080 [-0.000316, 0.160]; class level on class size -0.040 [-0.125, 0.045]

## H2, forcing does the harm, not shape

- **H2a**, rate ratio of intrusion on the problem's own lines, per tie: 1.173 [0.761, 1.807] (n = 350)
- Reported, the host-level count (any later change to the host): 0.908 [–, –]
- Reported, existing hosts only: 1.271 [0.824, 1.960]
- Reported, ties without injected dependencies: 1.117 [0.713, 1.750]
- **H2b**: unresolved; bound 0.800 to 1.250, 90% intervals (n = 103)
  - s3_junction: 0.519 [0.165, 1.630], TOST p 0.733
  - s4_cognitive: 1.587 [0.771, 3.267], TOST p 0.707
  - s5_class_gini: 0.321 [0.125, 0.822], TOST p 0.945
  - Left out by the variation rule: s1_long ({'officefloor': 1, 'spring': 23}), s2_stuck ({'officefloor': 0, 'spring': 0})
- Reported, shape without the problem terms and ties: s3_junction 0.726 [–, –]; s4_cognitive 1.877 [–, –]; s5_class_gini 0.455 [–, –]
- Reported, junction × arm (s3_junction): 0.613 [–, –]
- Reported, junction × arm (s3_junction_injection_aware): 2.031 [0.152, 27.169]

## H3, function injection keeps the space open

- **Function arm's bystanders (arm term, at checkpoint 30.5, the middle of the stream): -1.586 [-1.586, -1.586]**
- **Their slope on the checkpoint index (interaction): -0.017 [-0.017, -0.017]**
- Reported, bystanders without injected dependencies: arm -1.201 [-1.448, -0.953], slope -0.029 [-0.041, -0.017]
- Reported, the needed values, function arm against methods arm: 0.030 [-0.053, 0.114] (expected about 0: the same stream)
- Reported, H3 as first registered (ties): arm at a host of 7.3 positions -0.404 [-0.558, -0.250]; slope on host size 0.046 [-0.120, 0.211]
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
- Formation, where it ends, officefloor: Spearman's rho of early ties with the largest method's share – [no interval] over 1 chains (predicted above 0 in the methods arm)
- Formation, where it ends, spring: Spearman's rho of early ties with the largest method's share – [no interval] over 1 chains (predicted above 0 in the methods arm)
- Own lines followed, officefloor: 582 placed, 0 lost track of (0.0%)
- Own lines followed, spring: 537 placed, 0 lost track of (0.0%)

## Provenance

Checkpoint intercept in the model: H1 no, H3 no, H2a no, H2b yes.

Versions: {"R": "R version 4.5.2 (2025-10-31)", "glmmTMB": "1.1.14", "TMB": "1.9.19"}. Seed 20261116.

Registered files changed since `plan-v1` (amendments, PLAN.md §9): `PLAN.md`, `analysis/analyse.R`, `analysis/selftest.R`, `instrument/Pull.java`, `placement_gravity/measure.py`, `placement_gravity/prepare.py`, `placement_gravity/readings.py`, `placement_gravity/report.py`, `placement_gravity/tables.py`, `placement_gravity/verdict.py`.

| Arm | Run | Chain | Commit |
|---|---|---|---|
| officefloor | blind-202608100006 | 9 | `b824bf9d48e7` |
| spring | blind-202608100006 | 9 | `b48eb0cc333b` |

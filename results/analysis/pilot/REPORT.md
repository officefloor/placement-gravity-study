# pilot

Role: **development**. Chains: officefloor 1, spring 1. **Descriptive only.**

| Hypothesis | Verdict | p (Holm) |
|---|---|---|
| H1 | descriptive only | 0.003 |
| H2 | descriptive only | 1.000 |
| H3 | descriptive only | 1.000 |

## H1, gravity compounds (methods arm)

Runs 74 over 1 chains; slopes of log(1 + ties), cluster-bootstrap 95% intervals (1000 refits).

- On log(host positions): 0.025 [0.025, 0.025]
- On the checkpoint index: 0.006 [0.006, 0.006]
- Reported, the function arm: on host size 0.154 [0.011, 0.296]
- Reported, class level (methods arm): on class size -0.015 [-0.127, 0.097]

## H2, forcing does the harm, not shape

- **H2a**, rate ratio of intrusion per tie: 0.904 [0.627, 1.303] (n = 350)
- Reported, existing hosts only: 0.874 [0.638, 1.199]
- **H2b**: against; bound 0.800 to 1.250, 90% intervals (n = 103)
  - s3_junction: 1.110 [0.523, 2.354], TOST p 0.397
  - s4_cognitive: 0.543 [0.350, 0.845], TOST p 0.925
  - s5_class_gini: 0.436 [0.251, 0.758], TOST p 0.964
  - Left out by the variation rule: s1_long ({'officefloor': 1, 'spring': 23}), s2_stuck ({'officefloor': 0, 'spring': 0})
- Reported, shape without the problem terms and ties: s3_junction 5.344 [2.379, 12.000]; s4_cognitive 1.196 [0.753, 1.899]; s5_class_gini 0.442 [0.225, 0.868]
- Reported, junction × arm (s3_junction): 0.199 [0.039, 1.005]
- Reported, junction × arm (s3_junction_injection_aware): 0.283 [0.044, 1.806]

## H3, function injection keeps the space open

- Function arm's ties (arm term): -0.636 [-0.636, -0.636]
- Its slope on host size (interaction): 0.129 [0.129, 0.129]
- Amount, function arm / methods arm at the final checkpoint: 0.884 [0.884, 0.884], in band: yes
- Wiring growth: slope -0.012, interval None, against: –
- Wiring concentration: largest file 0.160, against: no
- Reported, without parameter ties: arm -0.258 [-0.589, 0.073], slope 0.029 [-0.126, 0.184]
- Reported, trajectory (arm × checkpoint): -3.64e-05 [-0.008, 0.008]

## Provenance

Versions: {"R": "R version 4.5.2 (2025-10-31)", "glmmTMB": "1.1.14", "TMB": "1.9.19"}. Seed 20261116.

| Arm | Run | Chain | Commit |
|---|---|---|---|
| officefloor | blind-202608100006 | 9 | `b824bf9d48e7` |
| spring | blind-202608100006 | 9 | `b48eb0cc333b` |

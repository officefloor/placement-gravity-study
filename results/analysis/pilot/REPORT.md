# pilot

Role: **development**. Chains: officefloor 1, spring 1. **Descriptive only.**

| Hypothesis | Verdict | p (Holm) |
|---|---|---|
| H1 | descriptive only | 0.003 |
| H2 | descriptive only | 1.28e-27 |
| H3 | descriptive only | 1.23e-05 |
| H4 | descriptive only | 0.003 |
| H5 | descriptive only | 0.865 |

## H1, the periphery grows (methods arm)

Runs that need a pre-existing value 91 over 1 chains; the slope of log(1 + bystanders) on the checkpoint index, cluster-bootstrap 95% interval (1000 refits).

- **Bystanders on the checkpoint index: 0.015 [0.015, 0.015]**
- **Within a class, the class's bystanders: 0.026 [0.026, 0.026]** (3 classes with runs at two or more checkpoints)
- **Within a method, the method's bystanders: 0.023 [0.023, 0.023]** (11 methods)
- Reported, within a place in the function arm: class 0.001 [0.001, 0.001]; method -0.001 [-0.001, -0.001]
- Reported, method bystanders 0.004 [-0.006, 0.013]; class bystanders 0.016 [0.010, 0.022]
- Reported, without injected dependencies 0.024 [0.016, 0.031]; without constants 0.003 [-0.005, 0.012]
- Reported, the function arm's slope: -0.000263 [-0.011, 0.010]
- Reported, officefloor: 56 of 168 runs need a pre-existing value (0.667 free); per such run, needed 1.554, bystanders 1.179 (method 0.929, class 0.250; without constants 1.036); over the thirds of the stream 1.455, 0.889, 1.167; fields left behind per addition 0.455; method values introduced per addition 6.491
- Reported, spring: 91 of 162 runs need a pre-existing value (0.438 free); per such run, needed 1.407, bystanders 10.890 (method 2.582, class 8.308; without constants 5.934); over the thirds of the stream 5.917, 10.172, 14.579; fields left behind per addition 0.610; method values introduced per addition 5.085
- Reported, H1 as first registered (bindings of runs into existing methods): on log(host positions) 0.030 [-0.042, 0.103]; on the checkpoint index 0.006 [0.002, 0.011]
- Reported, bindings in the function arm: on host size 0.098 [-0.084, 0.279]
- Reported, bindings at class level (methods arm): on class size -0.010 [-0.119, 0.100]
- Reported, bindings without injected dependencies: on host size 0.080 [-0.000316, 0.160]; class level on class size -0.040 [-0.125, 0.045]

## H2, a core draws code in (methods arm)

Where code was bound to a class or a method (109 of 350 problem and host rows, both arms; 83 in the methods arm): the later intrusions' uses of the values that code was bound to (the core) against their uses of the rest the place held, what stood by and what the change introduced (the periphery), as a rate ratio per value. A later change counts each value once in each method its bound code is in.

- **At the class (its fields and the methods it calls): 17.464 [11.934, 25.556]**
- **At the method (its values): 20.269 [11.842, 34.693]**
- Reported, the function arm: class 1.180 [0.135, 10.332]; method 4.276 [0.477, 38.309]
- Reported, officefloor, how bound uses are spread: at the class 2 uses of 2 fields, 1.000 to a chain's three most used, 0.500 to fields no checkpoint introduced; of 24 fields introduced, 1 used by later bound code (0.042); at the method 57 uses of 45 values, 0.105 to the three most used, 0.298 to values no checkpoint introduced; of 361 introduced, 31 used later (0.086)
- Reported, spring, how bound uses are spread: at the class 37 uses of 11 fields, 0.784 to a chain's three most used, 0.865 to fields no checkpoint introduced; of 35 fields introduced, 5 used by later bound code (0.143); at the method 86 uses of 44 values, 0.360 to the three most used, 0.477 to values no checkpoint introduced; of 315 introduced, 27 used later (0.086)
- Reported, at the class on its fields only (as until 19 November 2026): 8.539 [5.848, 12.468]
- Reported, officefloor, the core's width at the class: 1.111 values a row (median 1, 9 rows); over the thirds of the stream 1, 1, 1.200
- Reported, spring, the core's width at the class: 1.318 values a row (median 1, 44 rows); over the thirds of the stream 1.100, 1.250, 2
- Reported, officefloor, the core's width at the method: 2.045 values a row (median 2, 22 rows); over the thirds of the stream 3, 2.167, 1.667
- Reported, spring, the core's width at the method: 1.471 values a row (median 1, 51 rows); over the thirds of the stream 1.176, 1.450, 1.857
- Reported, H2 as it stood until 19 November 2026 (later intrusions bound to what stood by, per value that stood by): class 1.099 [1.038, 1.164]; method not estimated (standard error not computed: bystanders_method)
- Reported, officefloor: 31 bound rows; at the class 0.548 fields stood by, 3 of 26 later intrusions bound to one of them (0.115); at the method 0.903 values stood by, 1 of 3 (0.333)
- Reported, officefloor, introduced there by the change: at the class 0.097 fields, 0 of 26 later intrusions bound to one of them (0.000), to one that stood by or was introduced 3 (0.115); at the method 1.258 values, 0 of 3 (0.000), to either 1 (0.333)
- Reported, spring: 89 bound rows; at the class 7.472 fields stood by, 449 of 1056 later intrusions bound to one of them (0.425); at the method 2.236 values stood by, 43 of 292 (0.147)
- Reported, spring, introduced there by the change: at the class 0.348 fields, 3 of 1056 later intrusions bound to one of them (0.003), to one that stood by or was introduced 451 (0.427); at the method 1.787 values, 2 of 292 (0.007), to either 45 (0.154)
- Reported, on log(1 + bystanders): class 1.042 [0.593, 1.491]; method not estimated (standard error not computed: log_by_method)
- Reported, per value that stood by, the function arm: class 810508952663.495 [4.53e-99, 144926924589198000744940790788170766801987441848091268080083565762570760781355119429063249789257857706815653466801541480448.000]; method not estimated (standard error not computed: bystanders_method)
- Reported, with what the change introduced counted beside what stood by (later intrusions bound to either, per value of both): class 1.091 [1.032, 1.153]; method 0.917 [0.729, 1.154]; in the function arm, class 6.581 [0.779, 55.572]; method not estimated (standard error not computed: left_method)
- Reported, H2 as it stood until 17 November 2026 (later intrusion per binding): class 0.890 [0.745, 1.064]; method 0.853 [0.607, 1.199]
- For information, the same on the problem's own lines: not estimated (standard error not computed: binding)
- Reported, per binding, any later change, bound or not: class 0.857 [0.717, 1.023]; method 0.748 [0.524, 1.067]
- Reported, per binding, existing hosts only: class 0.916 [0.808, 1.039]; method 0.949 [0.667, 1.350]
- Reported, per binding, without injected dependencies: class 0.812 [0.696, 0.948]; method 0.922 [0.654, 1.301]

## H3, shape does not draw code in

- **not above** (one-sided: each rate ratio below 1.250); each measure fitted alone at its level, with the bindings and the bystanders in the model, 90% intervals: method measures on intrusion at the method (n = 77), class measures on intrusion at the class, one row per class and checkpoint with the class's size held fixed (n = 77); reported, two-sided (0.800 to 1.250): outside
  - s4_cognitive (method): 0.321 [0.207, 0.496], one-sided p 1.43e-07 (two-sided TOST p 1.000)
  - m_cyclomatic (method): 0.349 [0.219, 0.555], one-sided p 3.06e-06 (two-sided TOST p 0.998)
  - Left out by the variation rule: s1_long ({'officefloor': 1, 'spring': 22})
  - The class measures are not tested here: later arrivals in 5 distinct classes (at least 10 needed), the busiest holding 0.874 of them (at most 0.500). They are reported below, each alone.
- Reported, the block as first registered, together in one model on method-level intrusion: s4_cognitive 0.393 [0.240, 0.645]; s5_class_gini 0.689 [0.419, 1.132]
- Reported, that block on class-level intrusion: s4_cognitive 0.955 [0.798, 1.143]; s5_class_gini 1.509 [1.187, 1.920]
- Reported, that block without the problem terms, the bindings and the bystanders: s4_cognitive 1.661 [1.009, 2.733]; s5_class_gini 0.731 [0.363, 1.473]
- Reported, reach (how far a place reaches out; with the sinew measures, predicted above 1): m_fanout 4.977 [2.240, 11.057]; c_cbo 1.622 [0.687, 3.829]; c_fanout 1.622 [0.687, 3.829]
- Reported, the sinew measures (data flow, not shape; predicted above 1), later intrusion with the bindings and the bystanders in the model: s3_junction at the method 1.732 [0.544, 5.510], at the class 0.611 [0.412, 0.906]; left out by the variation rule: s2_stuck ({'officefloor': 0, 'spring': 0})
- Reported, junction × arm (s3_junction): 0.411 [0.027, 6.349]
- Reported, junction × arm (s3_junction_injection_aware): 0.314 [0.020, 4.863]

## H4, function injection forms no core

- **Function arm's bystanders (arm term, at checkpoint 30.5, the middle of the stream): -1.586 [-1.586, -1.586]**
- **Their slope on the checkpoint index (interaction): -0.017 [-0.017, -0.017]**
- **Later intrusion where bound code was placed, function arm / methods arm: at the class 0.162 [0.098, 0.268]; at the method 0.110 [0.029, 0.426]**
- Reported, how much a core value is come back to, function arm / methods arm: at the class 0.053 [0.006, 0.457]; at the method 0.088 [0.024, 0.316]
- Reported, officefloor, uses per 100 values and later checkpoints: at the class core 0.621 (1 uses of 10 values in 9 rows), periphery 0.761; at the method core 0.395 (4 uses of 45 values in 22 rows), periphery 0.084
- Reported, spring, uses per 100 values and later checkpoints: at the class core 13.677 (228 uses of 58 values in 44 rows), periphery 1.184; at the method core 10.126 (185 uses of 75 values in 51 rows), periphery 0.496
- Reported, officefloor: per checkpoint, classes its bound code goes back into 0.233, wiring files changed again 0.450
- Reported, spring: per checkpoint, classes its bound code goes back into 0.883, wiring files changed again 0.000
- Reported, reopening, function arm / methods arm: classes 0.264 [0.147, 0.476]; with wiring files 0.774 [0.515, 1.163]
- Reported, bystanders without injected dependencies: arm -1.201 [-1.448, -0.953], slope -0.029 [-0.041, -0.017]
- Reported, the needed values, function arm against methods arm: 0.030 [-0.053, 0.114] (expected about 0: the same stream)
- Reported, H4 as first registered (bindings): arm at a host of 7.3 positions -0.404 [-0.558, -0.250]; slope on host size 0.046 [-0.120, 0.211]
- Reported, the arm difference in bindings at a host of 10 positions -0.389 [-0.560, -0.219]; 25 positions -0.347 [-0.622, -0.073]; 50 positions -0.316 [-0.691, 0.060]
- Amount added since the base, function arm / methods arm at the final checkpoint: 1.076 [1.076, 1.076], in band: yes
- Reported, the ratio of the totals: 0.884
- Wiring growth: slope -0.012, interval None, against: –
- Wiring concentration: largest file 0.160, against: no
- Reported, bindings without parameters: arm -0.201 [-0.365, -0.036], slope 0.029 [-0.126, 0.184]
- Reported, bindings without injected dependencies: arm -0.295 [-0.454, -0.137], slope -0.021 [-0.193, 0.151]
- Reported, trajectory of the bindings (arm × checkpoint): 0.0007 [-0.007, 0.009]

## H5, choice narrows (methods arm)

Per bound addition, the other places in the code before its checkpoint that hold what its code was bound to: at the class, another class holding injected dependencies of the same types (code bound to the class's own state, constants or methods has none); at the method, another method with a parameter or local of each type. The ratio of the alternatives at the end of the stream to its start, 90% interval, one-sided below 1.250.

- **unresolved**
- **At the class: 0.162 [0.029, 0.916]** (n = 48; one-sided p 0.026)
- Reported, methods arm at the class: 48 rows, 0.542 forced, 2.583 alternatives a row; over the thirds, forced 0.500, 0.333, 0.722; alternatives 3.500, 3.167, 1.278
- Reported, function arm at the class: 10 rows, 0.900 forced, 0.100 alternatives a row; over the thirds, forced 1, 1, 0.857; alternatives 0, 0, 0.143
- Reported, the function arm's ratio at the class: 22.363 [4.55e-05, 10984478.990]; function arm / methods arm: 0.000765 [3.43e-10, 1702.055]
- **At the method: 2.507 [0.889, 7.073]** (n = 56; one-sided p 0.865)
- Reported, methods arm at the method: 56 rows, 0.089 forced, 20.446 alternatives a row; over the thirds, forced 0.077, 0.050, 0.130; alternatives 14.923, 17.250, 26.348
- Reported, function arm at the method: 27 rows, 0.074 forced, 39.926 alternatives a row; over the thirds, forced 0, 0, 0.111; alternatives 23.500, 33.400, 45.389
- Reported, the function arm's ratio at the method: 2.504 [0.506, 12.384]; function arm / methods arm: 1.692 [0.335, 8.534]
- Reported, class rows bound to the class's own state, constants or methods: 0.542; method values of no declared type left out of the match: 0

## Reported readings: choice, formation, review

- Choice, officefloor: 0 of 0 checkpoints left no choice (every chain with the same bindings, on the same side of new or existing); median spread of bindings over chains –, median distinct hosts –
- Choice, spring: 0 of 0 checkpoints left no choice (every chain with the same bindings, on the same side of new or existing); median spread of bindings over chains –, median distinct hosts –
- Formation, lagged, officefloor: bindings now on the chain's mean bindings so far -1.217 [-5.094, 2.660] (predicted above 0 in the methods arm)
- Formation, lagged, spring: bindings now on the chain's mean bindings so far -0.884 [-2.702, 0.934] (predicted above 0 in the methods arm)
- Capture, officefloor: share of the addition landing in existing hosts on the fields held by the chain's heaviest class 0.217 [0.021, 0.413] (predicted above 0 in the methods arm)
- Capture, spring: share of the addition landing in existing hosts on the fields held by the chain's heaviest class 0.315 [0.062, 0.567] (predicted above 0 in the methods arm)
- Size or data, at the class (both arms pooled, no arm term, n = 77): later intrusion per value that stood by, size held fixed, 0.878 [0.835, 0.924] (predicted above 1); per log of size, with what stood by held fixed, 3.054 [2.080, 4.483]; size alone 1.781 [1.312, 2.419]; within arms, bystanders 0.883 [0.842, 0.926] and size 2.674 [1.951, 3.664]; Spearman's rho of size with what stood by: pooled 0.952, officefloor 0.574, spring 0.943
- Size or data, at the method (both arms pooled, no arm term, n = 109): later intrusion per value that stood by, size held fixed, 0.888 [0.766, 1.030] (predicted above 1); per log of size, with what stood by held fixed, 4.800 [2.523, 9.135]; size alone 3.271 [2.166, 4.941]; within arms, bystanders 0.888 [0.768, 1.027] and size 4.686 [2.496, 8.797]; Spearman's rho of size with what stood by: pooled 0.813, officefloor 0.499, spring 0.867
- Formation, where it ends, officefloor: Spearman's rho of early bindings with the largest method's share – [no interval] over 1 chains (predicted above 0 in the methods arm)
- Formation, where it ends, spring: Spearman's rho of early bindings with the largest method's share – [no interval] over 1 chains (predicted above 0 in the methods arm)
- Own lines followed, officefloor: 582 placed, 0 lost track of (0.0%)
- Own lines followed, spring: 537 placed, 0 lost track of (0.0%)

## Reported: where bound and unbound code lands

A rank is the place's standing among every candidate of its checkpoint (0.5: no regard to that size; near 1: the largest). Method ranks are over landings into existing methods, class ranks over landings into existing classes.

| Arm | Code | Landings | Existing method | New method | New class | Method: complexity | Method: data width | Class: complexity | Class: fields | Agreement (method) | Agreement (class) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| officefloor | bound | 31 | 0.871 | 0.129 | 0.000 | 0.764 (n 27) | 0.621 | 0.822 (n 31) | 0.587 | 0.505 | 0.264 |
| officefloor | unbound | 161 | 0.155 | 0.354 | 0.491 | 0.550 (n 25) | 0.384 | 0.784 (n 81) | 0.682 | 0.769 | 0.531 |
| spring | bound | 89 | 0.674 | 0.326 | 0.000 | 0.803 (n 60) | 0.877 | 0.917 (n 88) | 0.925 | 0.573 | 0.961 |
| spring | unbound | 85 | 0.024 | 0.776 | 0.200 | 0.646 (n 2) | 0.966 | 0.931 (n 68) | 0.827 | – | -0.166 |

Unbound code entering a class that existed, function arm against methods arm, odds ratio: 0.259 [0.140, 0.480] (shares {'officefloor': 0.509316770186335, 'spring': 0.8}).

Agreement is Spearman's rho, over the places landed in, of the complexity rank with the data-width rank: whether the two kinds of size point to the same places.

## Reported: the literature's shape measures, each alone

Later intrusion per standard deviation of the measure (a flag: present against absent), with the problem, the bindings and what stood by held fixed. Method measures on intrusion at the method, class measures on intrusion at the class, one row per class a checkpoint's bound code went into (77 rows), with the class's size held fixed and an intercept for the class (†: refitted without it). Read as H3 is: below 1.25 does not draw code in. A measure marked reversed is one where higher is better; its ratio is for the worse shape.

| Measure | Level | Source | n | Rate ratio (90% interval) | One-sided p | Against 1.25 |
|---|---|---|---|---|---|---|
| s4_cognitive | method | Campbell 2018, cognitive complexity | 77 | 0.321 [0.207, 0.496] | 1.43e-07 | below |
| c_gini | class | concentration of the class's positions (Gini) | 77 | 1.083 [0.829, 1.415] | 0.189 | reaches above |
| m_cyclomatic | method | McCabe 1976 (CK) | 77 | 0.349 [0.219, 0.555] | 3.06e-06 | below |
| m_npath | method | Nejmeh 1988 (PMD) | 77 | 0.540 [0.346, 0.844] | 0.000987 | below |
| m_nesting | method | deepest nested block (CK) | 77 | 0.358 [0.253, 0.506] | 1.39e-09 | below |
| m_fanout | method | fan-out (CK) | 77 | 4.977 [2.240, 11.057] | 0.998 | above |
| m_halstead | method | Halstead 1977, volume | 77 | 0.866 [0.182, 4.124] | 0.349 | reaches above |
| m_mi (reversed) | method | Maintainability Index | 77 | 0.020 [0.002, 0.158] | 0.000537 | below |
| c_wmc | class | Chidamber and Kemerer 1994 (CK) | 77 | 0.445 [0.164, 1.207] | 0.044 | below |
| c_lcom_star | class | lack of cohesion, normalised (CK) | 77 | 0.903 [0.677, 1.204] | 0.031 | below |
| c_cbo | class | Chidamber and Kemerer 1994 (CK) | 77 | 1.622 [0.687, 3.829] | 0.691 | reaches above |
| c_rfc | class | Chidamber and Kemerer 1994 (CK) | 77 | 0.944 [0.407, 2.188] | 0.291 | reaches above |
| c_dit | class | Chidamber and Kemerer 1994 (CK) | – | not estimated (no finite interval) | – | – |
| c_fanout | class | fan-out (CK) | 77 | 1.622 [0.687, 3.829] | 0.691 | reaches above |
| c_imports | class | import count (PMD) | 77 | 2.406 [1.132, 5.115] | 0.923 | reaches above |
| c_halstead | class | Halstead 1977, volume | 77 | 0.144 [0.014, 1.522] | 0.066 | reaches above |
| c_mi (reversed) | class | Maintainability Index | 77 | 0.098 [0.021, 0.452] | 0.003 | below |

**Read the class rows with care.** Later arrivals fall in 5 distinct classes here, and the busiest holds 0.874 of them. A class measure then mostly describes that one class as it changes over the stream, so an association with later arrivals may be coincidental. These rows are not part of H3 in this analysis.

Left out by the variation rule (bound rows flagged or above zero, per arm): s1_long ({'officefloor': 1, 'spring': 22}), m_demeter ({'officefloor': 0, 'spring': 0}), m_duplicated ({'officefloor': 0, 'spring': 4}), c_tcc ({'officefloor': 0, 'spring': 80}), c_god_class ({'officefloor': 6, 'spring': 33}), c_data_class ({'officefloor': 0, 'spring': 0}), c_demeter ({'officefloor': 0, 'spring': 0}), c_duplicated ({'officefloor': 1, 'spring': 73}).

## Provenance

Checkpoint intercept in the model: H1 no, H4 no, H2_class yes, H2_method yes, H4_intrusion_class no, H4_intrusion_method yes, shape_joint no.

Versions: {"R": "R version 4.5.2 (2025-10-31)", "glmmTMB": "1.1.14", "TMB": "1.9.19"}. Seed 20261116.

| Arm | Run | Chain | Commit |
|---|---|---|---|
| officefloor | blind-202608100006 | 9 | `b824bf9d48e7` |
| spring | blind-202608100006 | 9 | `b48eb0cc333b` |

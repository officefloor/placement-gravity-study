# open-source-development

Role: **development**. Chains: human 2, agent 1. **Descriptive only.**

| Hypothesis | Verdict | p (Holm) |
|---|---|---|
| H1 | descriptive only | 0.004 |
| H2 | descriptive only | 0.010 |
| H3 | descriptive only | 0.737 |
| H4 | descriptive only | 0.521 |

## H1, gravity compounds (methods arm)

Runs that need a pre-existing value 307 over 2 chains; the slope of log(1 + bystanders) on the checkpoint index, cluster-bootstrap 95% interval (1000 refits).

- **Bystanders on the checkpoint index: 0.664 [0.251, 0.882]**
- **Within a class, the class's bystanders: 0.872 [0.271, 1.102]** (27 classes with runs at two or more checkpoints)
- **Within a method, the method's bystanders: 0.256 [0.252, 0.265]** (52 methods)
- Reported, within a place in the function arm: class -0.137 [-0.137, -0.137]; method -0.182 [-0.182, -0.182]
- Reported, method bystanders -0.035 [-0.289, 0.219]; class bystanders 1.044 [0.667, 1.421]
- Reported, without injected dependencies 0.664 [0.330, 0.997]; without constants 0.751 [0.491, 1.012]
- Reported, the function arm's slope: 0.406 [0.028, 0.783]
- Reported, agent: 295 of 488 runs need a pre-existing value (0.395 free); per such run, needed 2.176, bystanders 6.580 (method 2.007, class 4.573; without constants 5.929); over the thirds of the stream –, –, –; fields left behind per addition 0.451
- Reported, human: 307 of 491 runs need a pre-existing value (0.375 free); per such run, needed 1.782, bystanders 9.564 (method 1.489, class 8.075; without constants 4.717); over the thirds of the stream –, –, –; fields left behind per addition 0.827
- Reported, H1 as first registered (bindings of runs into existing methods): on log(host positions) -0.024 [-0.078, 0.031]; on the checkpoint index 0.003 [0.000378, 0.005]
- Reported, bindings in the function arm: on host size not estimated (standard error not computed: log_host)
- Reported, bindings at class level (methods arm): on class size -0.037 [-0.092, 0.018]
- Reported, bindings without injected dependencies: on host size -0.024 [-0.078, 0.031]; class level on class size -0.037 [-0.092, 0.018]

## H2, data draws code in (methods arm)

Where code was bound to a class or a method (508 of 884 problem and host rows, both arms; 249 in the methods arm): the later intrusions there that are bound to a value which stood by at the placement, as a rate ratio per value that stood by.

- **At the class (its fields): 1.021 [1.006, 1.036]**
- **At the method (its values): 1.418 [1.129, 1.782]**
- Reported, agent: 259 bound rows; at the class 4.649 fields stood by, 323 of 787 later intrusions bound to one of them (0.410); at the method 1.734 values stood by, 46 of 142 (0.324)
- Reported, human: 257 bound rows; at the class 8.603 fields stood by, 222 of 863 later intrusions bound to one of them (0.257); at the method 1.342 values stood by, 38 of 184 (0.207)
- Reported, on log(1 + bystanders): class 0.379 [0.212, 0.545]; method not estimated (standard error not computed: log_by_method)
- Reported, the function arm: class 1.196 [1.153, 1.241]; method 1.190 [0.997, 1.420]
- Reported, H2 as it stood until 17 November 2026 (later intrusion per binding): class 1.066 [1.013, 1.122]; method 1.085 [1.015, 1.159]
- For information, the same on the problem's own lines: 1.100 [1.020, 1.187]
- Reported, per binding, any later change, bound or not: class 1.077 [1.027, 1.129]; method 1.077 [1.014, 1.145]
- Reported, per binding, existing hosts only: class 1.051 [0.999, 1.106]; method 1.077 [1.006, 1.152]
- Reported, per binding, without injected dependencies: class 1.033 [0.983, 1.085]; method 1.081 [1.011, 1.157]

## H3, shape does not draw code in

- **unresolved** (one-sided: each rate ratio below 1.250); each measure fitted alone at its level, with the bindings and the bystanders in the model, 90% intervals: method measures on intrusion at the method (n = 436), class measures on intrusion at the class, one row per class and checkpoint with the class's size held fixed (n = 351); reported, two-sided (0.800 to 1.250): unresolved
  - s1_long (method): 1.031 [0.661, 1.608], one-sided p 0.238 (two-sided TOST p 0.238)
  - s4_cognitive (method): 1.362 [1.090, 1.703], one-sided p 0.737 (two-sided TOST p 0.737)
  - c_gini (class): 1.257 [1.076, 1.468], one-sided p 0.523 (two-sided TOST p 0.523)
  - Left out by the variation rule: m_cyclomatic ({'agent': 0, 'human': 0}), c_wmc ({'agent': 0, 'human': 0}), c_lcom_star ({'agent': 0, 'human': 0})
- Reported, the block as first registered, together in one model on method-level intrusion: s1_long 0.921 [0.583, 1.454]; s4_cognitive 1.402 [1.105, 1.779]; s5_class_gini 0.959 [0.822, 1.120]
- Reported, that block on class-level intrusion: s1_long 1.020 [0.761, 1.365]; s4_cognitive 1.096 [0.942, 1.276]; s5_class_gini 1.579 [1.414, 1.764]
- Reported, that block without the problem terms, the bindings and the bystanders: s1_long 1.095 [0.672, 1.784]; s4_cognitive 1.360 [1.101, 1.680]; s5_class_gini 0.943 [0.785, 1.134]
- Reported, the sinew measures (data flow, not shape; predicted above 1), later intrusion with the bindings and the bystanders in the model: s3_junction at the method 1.083 [0.736, 1.595], at the class 1.355 [1.039, 1.766]; left out by the variation rule: s2_stuck ({'agent': 12, 'human': 2})
- Reported, junction × arm (s3_junction): 0.782 [0.389, 1.573]
- Reported, junction × arm (s3_junction_injection_aware): 0.782 [0.389, 1.573]

## H4, function injection keeps the space open

- **Function arm's bystanders (arm term, at checkpoint 0.5, the middle of the stream): -0.324 [-0.646, 0.007]**
- **Their slope on the checkpoint index (interaction): -0.258 [-0.476, 0.154]**
- **Later intrusion where bound code was placed, function arm / methods arm: at the class 0.033 [0.027, 0.041]; at the method 0.026 [0.019, 0.035]**
- Reported, agent: per checkpoint, classes its bound code goes back into 0.473, wiring files changed again 0.000
- Reported, human: per checkpoint, classes its bound code goes back into 0.706, wiring files changed again 0.000
- Reported, reopening, function arm / methods arm: classes 0.670 [0.512, 0.876]; with wiring files 0.670 [0.512, 0.876]
- Reported, bystanders without injected dependencies: arm -0.836 [-1.498, -0.174], slope -0.538 [-1.031, -0.044]
- Reported, the needed values, function arm against methods arm: 0.113 [0.049, 0.177] (expected about 0: the same stream)
- Reported, H4 as first registered (bindings): arm at a host of 7.0 positions 0.160 [0.040, 0.281]; slope on host size 0.052 [-0.031, 0.136]
- Reported, the arm difference in bindings at a host of 10 positions 0.179 [0.053, 0.306]; 25 positions 0.227 [0.060, 0.395]; 50 positions 0.264 [0.052, 0.475]
- Amount added since the base, function arm / methods arm at the final checkpoint: – [–, –], in band: –
- Reported, the ratio of the totals: –
- Wiring growth: slope –, interval None, against: –
- Wiring concentration: largest file –, against: –
- Reported, bindings without parameters: arm -0.028 [-0.221, 0.165], slope 0.076 [-0.006, 0.158]
- Reported, bindings without injected dependencies: arm 0.150 [0.029, 0.271], slope 0.083 [-8.29e-05, 0.165]
- Reported, trajectory of the bindings (arm × checkpoint): not estimated (standard error not computed: armagent:cp)

## Reported readings: choice, formation, review

- Choice, agent: 0 of 0 checkpoints left no choice (every chain with the same bindings, on the same side of new or existing); median spread of bindings over chains –, median distinct hosts –
- Choice, human: 4 of 53 checkpoints left no choice (every chain with the same bindings, on the same side of new or existing); median spread of bindings over chains 2.000, median distinct hosts 5
- Formation, lagged, agent: bindings now on the chain's mean bindings so far not estimated (standard error not computed: prior_binding_mean) (predicted above 0 in the methods arm)
- Formation, lagged, human: bindings now on the chain's mean bindings so far -0.216 [-0.787, 0.355] (predicted above 0 in the methods arm)
- Capture, agent: share of the addition landing in existing hosts on the fields held by the chain's heaviest class 0.022 [-0.050, 0.093] (predicted above 0 in the methods arm)
- Capture, human: share of the addition landing in existing hosts on the fields held by the chain's heaviest class 0.128 [0.060, 0.196] (predicted above 0 in the methods arm)
- Size or data, at the class (both arms pooled, no arm term, n = 436): later intrusion per value that stood by, size held fixed, 0.989 [0.973, 1.004] (predicted above 1); per log of size, with what stood by held fixed, 1.633 [1.469, 1.816]; size alone 1.583 [1.436, 1.744]; within arms, bystanders 0.995 [0.981, 1.008] and size 1.585 [1.435, 1.751]; Spearman's rho of size with what stood by: pooled 0.412, agent 0.713, human 0.171
- Size or data, at the method (both arms pooled, no arm term, n = 508): later intrusion per value that stood by, size held fixed, 1.060 [0.976, 1.152] (predicted above 1); per log of size, with what stood by held fixed, 1.170 [0.943, 1.452]; size alone 1.269 [1.057, 1.524]; within arms, bystanders 1.059 [0.976, 1.149] and size 1.167 [0.946, 1.439]; Spearman's rho of size with what stood by: pooled 0.729, agent 0.728, human 0.749
- Own lines followed, agent: 1455 placed, 68 lost track of (4.7%)
- Own lines followed, human: 1636 placed, 219 lost track of (13.4%)

## Reported: where bound and unbound code lands

A rank is the place's standing among every candidate of its checkpoint (0.5: no regard to that size; near 1: the largest). Method ranks are over landings into existing methods, class ranks over landings into existing classes.

| Arm | Code | Landings | Existing method | New method | New class | Method: complexity | Method: data width | Class: complexity | Class: fields | Agreement (method) | Agreement (class) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agent | bound | 259 | 0.807 | 0.189 | 0.004 | 0.626 (n 210) | 0.599 | 0.571 (n 257) | 0.520 | 0.448 | 0.306 |
| agent | unbound | 207 | 0.188 | 0.386 | 0.425 | 0.418 (n 40) | 0.551 | 0.576 (n 112) | 0.552 | 0.135 | 0.342 |
| human | bound | 257 | 0.903 | 0.097 | 0.000 | 0.620 (n 232) | 0.611 | 0.596 (n 257) | 0.549 | 0.521 | 0.107 |
| human | unbound | 169 | 0.284 | 0.290 | 0.426 | 0.577 (n 48) | 0.363 | 0.560 (n 97) | 0.540 | -0.032 | -0.046 |

Unbound code entering a class that existed, function arm against methods arm, odds ratio: 0.993 [0.599, 1.645] (shares {'agent': 0.57487922705314, 'human': 0.57396449704142}).

Agreement is Spearman's rho, over the places landed in, of the complexity rank with the data-width rank: whether the two kinds of size point to the same places.

## Reported: the literature's shape measures, each alone

Later intrusion per standard deviation of the measure (a flag: present against absent), with the problem, the bindings and what stood by held fixed. Method measures on intrusion at the method, class measures on intrusion at the class, one row per class a checkpoint's bound code went into (351 rows), with the class's size held fixed and an intercept for the class (†: refitted without it). Read as H3 is: below 1.25 does not draw code in. A measure marked reversed is one where higher is better; its ratio is for the worse shape.

| Measure | Level | Source | n | Rate ratio (90% interval) | One-sided p | Against 1.25 |
|---|---|---|---|---|---|---|
| s1_long | method | long: 26 or more code lines | 436 | 1.031 [0.661, 1.608] | 0.238 | reaches above |
| s4_cognitive | method | Campbell 2018, cognitive complexity | 436 | 1.362 [1.090, 1.703] | 0.737 | reaches above |
| c_gini | class | concentration of the class's positions (Gini) | 351 | 1.257 [1.076, 1.468] | 0.523 | reaches above |

Left out by the variation rule (bound rows flagged or above zero, per arm): m_cyclomatic ({'agent': 0, 'human': 0}), m_npath ({'agent': 0, 'human': 0}), m_nesting ({'agent': 0, 'human': 0}), m_fanout ({'agent': 0, 'human': 0}), m_halstead ({'agent': 0, 'human': 0}), m_mi ({'agent': 0, 'human': 0}), m_demeter ({'agent': 0, 'human': 0}), m_duplicated ({'agent': 0, 'human': 0}), c_wmc ({'agent': 0, 'human': 0}), c_lcom_star ({'agent': 0, 'human': 0}), c_tcc ({'agent': 0, 'human': 0}), c_cbo ({'agent': 0, 'human': 0}), c_rfc ({'agent': 0, 'human': 0}), c_dit ({'agent': 0, 'human': 0}), c_fanout ({'agent': 0, 'human': 0}), c_imports ({'agent': 0, 'human': 0}), c_halstead ({'agent': 0, 'human': 0}), c_mi ({'agent': 0, 'human': 0}), c_god_class ({'agent': 0, 'human': 0}), c_data_class ({'agent': 0, 'human': 0}), c_demeter ({'agent': 0, 'human': 0}), c_duplicated ({'agent': 0, 'human': 0}).

## Provenance

Checkpoint intercept in the model: H1 no, H4 no, H2_class no, H2_method no, H4_intrusion_class no, H4_intrusion_method no, shape_joint no.

Versions: {"R": "R version 4.5.2 (2025-10-31)", "glmmTMB": "1.1.14", "TMB": "1.9.19"}. Seed 20261116.

| Arm | Run | Chain | Commit |
|---|---|---|---|

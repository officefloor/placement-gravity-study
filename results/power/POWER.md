# Power of the confirmatory four at the ui primary's design

Made by `analysis/power.R` (PLAN.md §7, *Power for the confirmatory four*), 2026-11-27T22:02:41+0800; 100 draws a scenario, 10 chains a stack, two front ends, 250 checkpoints. Read on Wald intervals, not the cluster bootstrap; a guide, not a promise.

Share of draws in which a hypothesis passes (every part on its side). *0.05*: its p at a part's alpha of
0.05; *0.0125*: at 0.05 / 4, the first step of Holm.

| scenario | H1 | H2 | H4 | H5 |
|---|---|---|---|---|
| dev/sd0.2 | 0.00 / 0.00 | 1.00 / 1.00 | 1.00 / 1.00 | 0.00 / 0.00 |
| 0.8/sd0.2 | 0.60 / 0.30 | 0.86 / 0.65 | 0.84 / 0.45 | 0.97 / 0.92 |
| 0.67/sd0.2 | 0.95 / 0.88 | 1.00 / 1.00 | 1.00 / 0.98 | 1.00 / 1.00 |
| 0.5/sd0.2 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| dev/sd0.5 | 0.00 / 0.00 | 1.00 / 1.00 | 0.93 / 0.86 | 0.00 / 0.00 |
| 0.8/sd0.5 | 0.29 / 0.11 | 0.07 / 0.04 | 0.00 / 0.00 | 0.46 / 0.24 |
| 0.67/sd0.5 | 0.83 / 0.61 | 0.67 / 0.32 | 0.30 / 0.06 | 0.84 / 0.64 |
| 0.5/sd0.5 | 1.00 / 0.98 | 1.00 / 0.96 | 1.00 / 0.92 | 1.00 / 1.00 |

Each part, at a part's alpha of 0.05:

| scenario | H1_arm_trend | H4_bystanders | H4_intrusion_class | H4_intrusion_method | H4_trodden | H5_arm_trend | H2_core_class | H2_core_method | H2_reuse_method | H4_intrusion_method_all | H4_intrusion_method_none | H2_reuse_method_all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dev/sd0.2 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 0.8/sd0.2 | 0.60 | 1.00 | 0.97 | 0.95 | 0.99 | 0.97 | 1.00 | 1.00 | 0.90 | 0.93 | 0.96 | 0.96 |
| 0.67/sd0.2 | 0.95 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 0.5/sd0.2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| dev/sd0.5 | 0.00 | 1.00 | 1.00 | 1.00 | 0.93 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 0.8/sd0.5 | 0.29 | 0.40 | 0.51 | 0.43 | 0.32 | 0.46 | 1.00 | 1.00 | 0.31 | 0.46 | 0.41 | 0.32 |
| 0.67/sd0.5 | 0.83 | 0.87 | 0.81 | 0.79 | 0.85 | 0.84 | 1.00 | 1.00 | 0.84 | 0.83 | 0.87 | 0.80 |
| 0.5/sd0.5 | 1.00 | 1.00 | 0.99 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

The development chain's estimates (*dev*), as ratios (a trend over its stream):

- H1_arm_trend: armofficefloor 0.247; cp_c:armofficefloor 7.48
- H4_bystanders: armofficefloor 0.205; cp_c:armofficefloor 0.36
- H4_intrusion_class: armofficefloor 0.162
- H4_intrusion_method: armofficefloor 0.11
- H4_trodden: armofficefloor 0.603
- H5_arm_trend: armofficefloor 1.05; cp_c:armofficefloor 1.7
- H2_core_class: core 18.2
- H2_core_method: core 20.3
- H2_reuse_method: armofficefloor 0.106
- H4_intrusion_method_all: armofficefloor 0.198
- H4_intrusion_method_none: armofficefloor 0.11
- H2_reuse_method_all: armofficefloor 0.17

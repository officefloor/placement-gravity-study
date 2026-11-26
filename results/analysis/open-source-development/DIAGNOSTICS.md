# Diagnostics: open-source-development

Every figure PLAN.md quotes that REPORT.md does not print, made by step 5 from the tables of steps 3 and 4 (PLAN.md 9 row 112). They describe and enter no verdict. Each section says where the plan quotes it; figures §6 recorded on an earlier `MEASURE_VERSION` may differ from these.

## change_size

§6 (20 November 2026): a forced unit is a larger change. Per arm (on a history, per author group): the positions and methods of a unit with a placement forced at the class (no other class holding what it was bound to) and of one without; and the existing classes it went into, forced and not, among the units at or below the median number of methods and above it.

- agent:
  - units: 8
  - forced_units: 5
  - positions:
    - forced: 24.4
    - not: 23.7
  - methods:
    - forced: 9
    - not: 3.67
  - median_methods: 5.5
  - existing_classes_small:
    - forced: 1
    - not: 0
  - existing_classes_large:
    - forced: 3.33
    - not: 2
- human:
  - units: 462
  - forced_units: 306
  - positions:
    - forced: 11.6
    - not: 5.92
  - methods:
    - forced: 4.05
    - not: 2.33
  - median_methods: 2
  - existing_classes_small:
    - forced: 0.14
    - not: 0.0684
  - existing_classes_large:
    - forced: 2.4
    - not: 1.64
- agent/bytechefhq__bytechef:
  - units: 8
  - forced_units: 5
  - positions:
    - forced: 24.4
    - not: 23.7
  - methods:
    - forced: 9
    - not: 3.67
  - median_methods: 5.5
  - existing_classes_small:
    - forced: 1
    - not: 0
  - existing_classes_large:
    - forced: 3.33
    - not: 2
- human/felHR85__UsbSerial:
  - units: 166
  - forced_units: 133
  - positions:
    - forced: 13.3
    - not: 8.91
  - methods:
    - forced: 3.37
    - not: 3.27
  - median_methods: 2
  - existing_classes_small:
    - forced: 0.104
    - not: 0.111
  - existing_classes_large:
    - forced: 1.39
    - not: 1.4
- human/jmxtrans__jmxtrans:
  - units: 296
  - forced_units: 173
  - positions:
    - forced: 10.3
    - not: 5.11
  - methods:
    - forced: 4.57
    - not: 2.08
  - median_methods: 2
  - existing_classes_small:
    - forced: 0.172
    - not: 0.0606
  - existing_classes_large:
    - forced: 3.06
    - not: 1.79

## timing

§5 and §6: how long step 4 took on this analysis, and one model fit by the size of the data on this machine (step 1b, ``results/timing.json``).

- step4:
  - seconds: 169
  - refits: 200
- fits:
  - date: 2026-11-25T17:21:23Z
  - cores: 16
  - glmmTMB: 1.1.14
  - fits:
    - rows: 1800
    - seconds: 1.64
    - rows: 15000
    - seconds: 12.5
    - rows: 30000
    - seconds: 28.2
    - rows: 200000
    - seconds: 213
    - rows: 1000000
    - seconds: 1,681

## repositories

§6 (17 and 19 November 2026): each sample a history analysis reads, and each repository in it. Per sample: repositories drawn and usable. Per repository read: its commits, its declared agent commits and their agents, the units read; its class rows and their alternatives, the share bound to the class's own values, its method rows and their alternatives, and the share of calls the control flow followed.

- open-source-development:
  - drawn: 5
  - usable: 2
  - repositories:
    - felHR85/UsbSerial:
      - commits: 422
      - agent_commits: 0
      - agents: 
      - units: 227
      - class_rows: 305
      - class_alternatives: 0
      - own_share: 1
      - method_rows: 115
      - method_alternatives: 5.64
      - calls_followed: 0.794
    - jmxtrans/jmxtrans:
      - commits: 1461
      - agent_commits: 0
      - agents: 
      - units: 422
      - class_rows: 362
      - class_alternatives: 0
      - own_share: 1
      - method_rows: 535
      - method_alternatives: 6.07
      - calls_followed: 0.613
- open-source-development-agent:
  - drawn: 39
  - usable: 1
  - repositories:
    - bytechefhq/bytechef:
      - commits: 23215
      - agent_commits: 1608
      - agents: claude:1587;copilot:15;cursor:6
      - units: 300
      - class_rows: 383
      - class_alternatives: 2.41
      - own_share: 0.642
      - method_rows: 457
      - method_alternatives: 21.6
      - calls_followed: 0.49

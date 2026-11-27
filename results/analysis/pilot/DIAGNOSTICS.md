# Diagnostics: pilot

Every figure PLAN.md quotes that REPORT.md does not print, made by the report from the tables of the measuring and the analysis (PLAN.md 9 row 112). They describe and enter no verdict. Each section says where the plan quotes it; figures §6 recorded on an earlier `MEASURE_VERSION` may differ from these.

## files

§2 H4 and §6 (22 November 2026): the files a chain went back into. Per arm: new Java files a checkpoint; Java files at the head and the largest; the existing files gone back into (Java and wiring), the busiest and the checkpoints that changed it, the share gone back into at four checkpoints or fewer, and the share of the returns the three busiest took; the files both arms went back into most, by name.

- officefloor:
  - checkpoints: 60
  - new_java_files_per_checkpoint: 1.03
  - java_files_at_end: 203
  - largest_java_file_kb: 15.5
  - existing_files_gone_back_into: 48
  - busiest:
    - path: src/main/resources/officefloor/rest/api/owners.POST.yml
    - checkpoints: 24
  - share_gone_back_into_at_four_or_fewer: 0.938
  - three_busiest_share_of_returns: 0.444
- spring:
  - checkpoints: 60
  - new_java_files_per_checkpoint: 0.15
  - java_files_at_end: 94
  - largest_java_file_kb: 51.4
  - existing_files_gone_back_into: 9
  - busiest:
    - path: src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java
    - checkpoints: 43
  - share_gone_back_into_at_four_or_fewer: 0.556
  - three_busiest_share_of_returns: 0.833
- gone_back_into_by_both:
  - file: OwnerMapper.java
  - officefloor: 24
  - spring: 24
  - file: Owner.java
  - officefloor: 16
  - spring: 13
  - file: OwnerCreatedEvent.java
  - officefloor: 2
  - spring: 2

## new_methods

§6 (22 November 2026): the new methods a chain wrote. Per arm: wired functions (a method the OfficeFloor wiring declares) and their injected parameters each; new methods that are not wired functions and hold logic (not plain organisation, §4.9): how many, their parameters, the values their callers pass them, the classes they are in and the class holding most.

- officefloor:
  - wired_functions: 35
  - injected_parameters_each: 1.89
  - called_with_logic: 80
  - their_parameters: 85
  - values_callers_pass: 4
  - classes: 32
  - most:
    - class: OwnerMapper
    - methods: 17
- spring:
  - wired_functions: 0
  - injected_parameters_each: –
  - called_with_logic: 81
  - their_parameters: 100
  - values_callers_pass: 12
  - classes: 13
  - most:
    - class: OwnerRestControllerV1
    - methods: 36

## trodden_thirds

§6 (22 November 2026): H4's well-trodden count a checkpoint over the thirds of the stream.

- officefloor:
  - all: 13.4
  - thirds: [5.3, 15, 19.9]
- spring:
  - all: 21.7
  - thirds: [7.5, 22.1, 35.4]

## injected_runs

§6 (16 November 2026): runs of added code into methods that existed, and how many bindings an injected dependency accounts for. Per arm: the runs; those bound to an injected dependency; the runs bound at all and bound at the class, counting injected dependencies and not.

- officefloor:
  - runs_into_existing_methods: 61
  - with_an_injected_binding: 0
  - bound: 29
  - bound_without_injected: 29
  - bound_at_the_class: 6
  - bound_at_the_class_without_injected: 6
- spring:
  - runs_into_existing_methods: 74
  - with_an_injected_binding: 12
  - bound: 71
  - bound_without_injected: 67
  - bound_at_the_class: 20
  - bound_at_the_class_without_injected: 10

## bound_new_methods

§6 (19 November 2026): new methods bound to their class. Per arm: by how (a field only, a call to another of the class's methods only, both); and, in H2's rows, the bound rows of new and of existing methods, their later arrivals at the method, the values the new ones introduced and later arrivals bound to those; the rows with an arrival bound to what stood by at the method, and the methods they are in.

- officefloor:
  - new_methods_bound_at_the_class: 4
  - by_a_field_only: 1
  - by_a_call_only: 3
  - by_both: 0
  - bound_rows_new: 4
  - their_later_arrivals_at_the_method: 0
  - bound_rows_existing: 27
  - existing_later_arrivals_at_the_method: 3
  - values_new_ones_introduced: 13
  - later_arrivals_bound_to_those: 0
  - rows_with_an_arrival_bound_to_what_stood_by: 1
  - those_arrivals: 1
  - their_methods:
    - service: 1
- spring:
  - new_methods_bound_at_the_class: 29
  - by_a_field_only: 16
  - by_a_call_only: 9
  - by_both: 4
  - bound_rows_new: 29
  - their_later_arrivals_at_the_method: 4
  - bound_rows_existing: 60
  - existing_later_arrivals_at_the_method: 288
  - values_new_ones_introduced: 102
  - later_arrivals_bound_to_those: 1
  - rows_with_an_arrival_bound_to_what_stood_by: 13
  - those_arrivals: 43
  - their_methods:
    - addOwner: 13

## alternatives_thirds

§6 (19 November 2026): the alternatives at the method over the thirds of the stream, for the rows bound to a value named after a class of the system (a domain type: ``owner`` for ``Owner``) and the rest; and the methods on a host's control flow over the thirds.

- officefloor:
  - rows: 30
  - domain_rows: 6
  - domain_thirds: [–, 0, 5.4]
  - other_thirds: [5.4, 15.6, 11.1]
  - flow_methods_thirds: [28.6, 54, 46.1]
- spring:
  - rows: 59
  - domain_rows: 39
  - domain_thirds: [6, 3.2, 5.89]
  - other_thirds: [4, 8.8, 24.2]
  - flow_methods_thirds: [27.4, 45.2, 69.2]

## change_size

§6 (20 November 2026): a forced unit is a larger change. Per arm (on a history, per author group): the positions and methods of a unit with a placement forced at the class (no other class holding what it was bound to) and of one without; and the existing classes it went into, forced and not, among the units at or below the median number of methods and above it.

- officefloor:
  - units: 42
  - forced_units: 9
  - positions:
    - forced: 19
    - not: 10.5
  - methods:
    - forced: 5.22
    - not: 3.18
  - median_methods: 3
  - existing_classes_small:
    - forced: 0.5
    - not: 0.182
  - existing_classes_large:
    - forced: 2.14
    - not: 1.45
- spring:
  - units: 59
  - forced_units: 21
  - positions:
    - forced: 13.2
    - not: 7.68
  - methods:
    - forced: 3.9
    - not: 2.42
  - median_methods: 3
  - existing_classes_small:
    - forced: 0
    - not: 0.143
  - existing_classes_large:
    - forced: 1.07
    - not: 1
- officefloor/blind-202608100006/chain9:
  - units: 42
  - forced_units: 9
  - positions:
    - forced: 19
    - not: 10.5
  - methods:
    - forced: 5.22
    - not: 3.18
  - median_methods: 3
  - existing_classes_small:
    - forced: 0.5
    - not: 0.182
  - existing_classes_large:
    - forced: 2.14
    - not: 1.45
- spring/blind-202608100006/chain9:
  - units: 59
  - forced_units: 21
  - positions:
    - forced: 13.2
    - not: 7.68
  - methods:
    - forced: 3.9
    - not: 2.42
  - median_methods: 3
  - existing_classes_small:
    - forced: 0
    - not: 0.143
  - existing_classes_large:
    - forced: 1.07
    - not: 1

## problem_hosts

§4.4, §5 and §6 (16 and 17 November 2026): the problem-and-host rows. Per arm: the rows; the most problems one method received; the later arrivals at the method in all and in methods holding several problems; bindings and later arrivals a later checkpoint in new and in existing methods; later arrivals at the class, the method and on the problem's own lines, in all and a row; the bound rows and their later arrivals a bound row.

- officefloor:
  - rows: 192
  - most_problems_in_one_method: 6
  - arrivals_at_the_method: 18
  - in_methods_holding_several: 18
  - new_methods:
    - bindings: 0.0357
    - arrivals_per_later_checkpoint: 0.00254
  - existing_methods:
    - bindings: 0.962
    - arrivals_per_later_checkpoint: 0.00832
  - arrivals:
    - class: 117
    - method: 18
    - lines: 26
  - arrivals_a_row:
    - class: 0.609
    - method: 0.0938
    - lines: 0.135
  - bound_rows: 31
  - arrivals_a_bound_row:
    - class: 0.839
    - method: 0.0968
- spring:
  - rows: 174
  - most_problems_in_one_method: 26
  - arrivals_at_the_method: 319
  - in_methods_holding_several: 319
  - new_methods:
    - bindings: 0.321
    - arrivals_per_later_checkpoint: 0.00406
  - existing_methods:
    - bindings: 1.81
    - arrivals_per_later_checkpoint: 0.192
  - arrivals:
    - class: 1,602
    - method: 319
    - lines: 23
  - arrivals_a_row:
    - class: 9.21
    - method: 1.83
    - lines: 0.132
  - bound_rows: 89
  - arrivals_a_bound_row:
    - class: 11.9
    - method: 3.28

## bystanders

§6 (17 November 2026): what stood by runs into methods that existed. Per arm: the bystanders a run, and without constants, overall and over the thirds; at the class and at the method over the thirds; and in the class and the method that received most runs, at their first and last.

- officefloor:
  - runs: 61
  - bystanders: 1.36
  - without_constants: 1.23
  - thirds: [1.67, 1, 1.37]
  - thirds_without_constants: [1.58, 1, 1.18]
  - class_thirds: [0.0833, 0, 0.368]
  - method_thirds: [1.58, 1, 1]
  - busiest_class:
    - place: OwnerMapper
    - runs: 29
    - first: 0
    - last: 1
  - busiest_method:
    - place: AssignOwnerCustomerCode service
    - runs: 6
    - first: 0
    - last: 4
- spring:
  - runs: 74
  - bystanders: 11.9
  - without_constants: 6.77
  - thirds: [7.17, 11.1, 14.9]
  - thirds_without_constants: [5.94, 6.59, 7.32]
  - class_thirds: [4.61, 7.73, 11.4]
  - method_thirds: [2.56, 3.41, 3.5]
  - busiest_class:
    - place: OwnerRestControllerV1
    - runs: 106
    - first: 4
    - last: 17
  - busiest_method:
    - place: OwnerRestControllerV1 addOwner
    - runs: 33
    - first: 0
    - last: 13

## busiest_method

§6 (18 November 2026): the method that received most bound problems. Per arm: its rows, its mean size, its mean cognitive complexity and its later arrivals at the method a hundred later checkpoints.

- officefloor:
  - method: CheckOwnerHouseholdUnique service
  - rows: 2
  - size: 17
  - cognitive: 6
  - arrivals_per_100_later_checkpoints: 1.03
- spring:
  - method: OwnerRestControllerV1 addOwner
  - rows: 25
  - size: 34.9
  - cognitive: 5.48
  - arrivals_per_100_later_checkpoints: 35.3

## class_rows

§6 (21 November 2026): H6's class rows. The class-and-checkpoint rows with a class shape, the rows of the busiest class, its share of the later arrivals at the class, its Gini at its first and last row, and within each class of five rows or more the rank correlation of its Gini with its later arrivals a later checkpoint.

- rows: 268
- classes: 31
- busiest: OwnerRestControllerV1
- busiest_rows: 76
- busiest_share_of_arrivals: 0.788
- busiest_gini_first: 0.204
- busiest_gini_last: 0.451
- gini_against_arrivals:
  - CheckOwnerHouseholdUnique: 0.424
  - OwnerMapper: 0.348
  - AuditOwnerCreated: -0.316
  - ExceptionControllerAdvice: 0.945
  - OwnerRestControllerV1: -0.499

## fields_and_landings

§6 (19 November 2026): fields added to classes that existed, a checkpoint, where the checkpoint put unbound code into an existing class and where it did not; and the rank correlation, over checkpoints, of the fields added with those unbound landings.

- officefloor:
  - with_an_unbound_landing: 0.632
  - without: 0.0909
  - rank_correlation: 0.606
- spring:
  - with_an_unbound_landing: 0.714
  - without: 0.353
  - rank_correlation: 0.411

## junctions

§6 (16 November 2026): the junctions' share of cognitive complexity at the first and the last checkpoint, as conventionally read and injection-aware (PILOT.md).

- officefloor:
  - junction_share: [0.218, 0.36]
  - junction_share_injection_aware: [0.298, 0.425]
- spring:
  - junction_share: [0.329, 0.31]
  - junction_share_injection_aware: [0.329, 0.31]

## size_or_data_by_arm

§6 (17 November 2026): size or data within each arm alone (from the analysis's estimates).

- class:
  - officefloor:
    - n: 22
    - size_alone: not estimated (standard error not computed: log_class)
    - size: not estimated (standard error not computed: log_class)
    - bystanders: not estimated (standard error not computed: bystanders_class)
  - spring:
    - n: 55
    - size_alone: 1.28 [1.03, 1.6]
    - size: 2.1 [1.53, 2.89]
    - bystanders: 0.907 [0.865, 0.952]
- method:
  - officefloor:
    - n: 26
    - size_alone: 2 [0.234, 17.1]
    - size: 1.94 [0.195, 19.4]
    - bystanders: 1.03 [0.462, 2.29]
  - spring:
    - n: 83
    - size_alone: 3.31 [2.17, 5.03]
    - size: 5 [2.57, 9.74]
    - bystanders: 0.881 [0.757, 1.03]

## timing

§5 and §6: how long the analysis took on this analysis, and one model fit by the size of the data on this machine (step 02, ``results/timing.json``).

- step4:
  - seconds: 56.4
  - refits: 1000
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

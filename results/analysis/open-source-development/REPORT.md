# open-source-development

Role: **development**. Chains: human 2, agent 1. **Descriptive only.**

| Hypothesis | Tier | Verdict | p (Holm over the confirmatory; own p for secondary) |
|---|---|---|---|
| H1 | confirmatory | descriptive only | – |
| H2 | confirmatory | descriptive only | 0.010 |
| H3 | secondary | descriptive only | 0.005 |
| H4 | confirmatory | descriptive only | 1.000 |
| H5 | confirmatory | descriptive only | – |
| H6 | secondary | descriptive only | 0.033 |
| H7 | secondary | descriptive only | 0.002 |
| H9 | secondary | descriptive only | – |

## H1, choice narrows (and less often forced in the function arm)

Per bound addition, the other places in the code before its checkpoint that hold what its code was bound to: at the class, another class holding injected dependencies of the same types (code bound to the class's own state, constants or methods has none); at the method, another method with a parameter or local of each type. The ratio of the alternatives at the end of the stream to its start: a fall, one-sided below 1, at the class, 95% cluster-bootstrap interval (chains resampled). The method level is reported.

- **descriptive only** (every placement forced)
- **At the class: every placement forced** (638 rows; no alternative anywhere)
- Reported, methods arm at the class: 638 rows, 1 forced, 0 alternatives a row; over the thirds, forced 1, 1, 1; alternatives 0, 0, 0
- Reported, function arm at the class: 25 rows, 0.520 forced, 3.480 alternatives a row; over the thirds, forced 0.389, 0.857, –; alternatives 3.444, 3.571, –
- Reported, the function arm's ratio at the class: 6.530 [0.006, 7253.304]; function arm / methods arm: not estimated (standard error not computed: armagent)
- **At the method: 1.842 [0.963, 23.612]** (n = 627; one-sided p 0.796; cluster bootstrap)
- Reported, at the method against the upper margin 1.250 (as H1 stood until 22 November 2026, 90% Wald interval): 1.842 [1.195, 2.841]
- Reported, methods arm at the method: 627 rows, 0.434 forced, 5.509 alternatives a row; over the thirds, forced 0.297, 0.509, 0.470; alternatives 5.621, 3.961, 7.041
- Reported, function arm at the method: 30 rows, 0.400 forced, 2.367 alternatives a row; over the thirds, forced 0.231, 0.529, –; alternatives 1.692, 2.882, –
- Reported, the function arm's ratio at the method: 50.751 [0.290, 8875.394]; function arm / methods arm: 0.202 [0.031, 1.327]
- Reported, at the method by type alone over the whole tree (as first built): 4.927 [3.207, 7.571]; methods on a host's control flow, per arm: agent 560.700, human 62.662; by type over the whole tree: agent 92.700, human 28.845; calls to a name the application declares that were followed by their receiver's type: 0.512 (the rest have a receiver the instrument cannot read)
- Reported, class rows bound to the class's own state, constants or methods: 1; method values of no declared type left out of the match: 1

## H2, a core draws code in (methods arm)

Where code was bound to a class or a method (1077 of 1788 problem and host rows, both arms; 1036 in the methods arm): the later intrusions' uses of the values that code was bound to (the core) against their uses of the rest the place held, what stood by and what the change introduced (the periphery), as a rate ratio per value. A later change counts each value once in each method its bound code is in.

- **At the class (the private members the code was bound to): 2.933 [2.578, 3.193]** (cluster bootstrap; Wald: 2.933 [2.518, 3.416])
- **At the method (its values): 2.373 [2.339, 2.443]** (cluster bootstrap; Wald: 2.373 [1.900, 2.963])
- The arm contrast at the class is not part of the test here: a history: its arms do not solve the same problems
- The arm contrast at the method is not part of the test here: a history: its arms do not solve the same problems
- Reported, the function arm: class 3.342 [0.915, 12.211]; method 1.14e-07 [0, –]
- Reported, agent, how bound uses are spread: at the class 36 uses of 28 fields, 0.278 to a chain's three most used, 0.944 to fields no checkpoint introduced; of 14 fields introduced, 2 used by later bound code (0.143); at the method 71 uses of 70 values, 0.056 to the three most used, 0.958 to values no checkpoint introduced; of 128 introduced, 3 used later (0.023)
- Reported, human, how bound uses are spread: at the class 1257 uses of 553 fields, 0.045 to a chain's three most used, 0.721 to fields no checkpoint introduced; of 389 fields introduced, 138 used by later bound code (0.355); at the method 1312 uses of 802 values, 0.028 to the three most used, 0.628 to values no checkpoint introduced; of 1704 introduced, 259 used later (0.152)
- Reported, agent, the sinew shape at the class: 9 places, 36 uses; effective number of values 2.944 (over the thirds 1.900, 2.000, 5.000); the most used value's share 0.712; changes repeating a combination already used there 0.167 of 18
  - most used values: `PrepaidSubscriptionModelHandler` billingProperties 4; `UserServiceImpl` userRepository 3; `PrepaidSubscriptionModelHandler` billingSubscriptionService 3; `PrepaidSubscriptionModelHandler` stripeClient 2; `WorkflowValidatorFacadeImpl` workflowTestConfigurationService 1
  - most used combinations: `UserServiceImpl` {userRepository} 3; `PrepaidSubscriptionModelHandler` {billingProperties} 2; `BillingWebhookEventHandler` {billingSubscriptionService, subscriptionModelHandlerRegistry} 1; `MeteredSubscriptionModelHandler` {billingSubscriptionService} 1; `PrepaidSubscriptionModelHandler` {billingSubscriptionService, stripeClient} 1
- Reported, agent, the sinew shape at the method: 29 places, 71 uses; effective number of values 2.399 (over the thirds 1.000, 4.667, 2.161); the most used value's share 0.635; changes repeating a combination already used there 0.000 of 30
  - most used values: `WebSocketStreamTaskExecutionPostOutputProcessor process` emitter 2; `WorkflowValidatorFacadeImpl resolveVariableOutput` workflowNodeType 1; `WorkflowValidatorFacadeImpl resolveVariableOutput` inputParameters 1; `WorkflowValidatorFacadeImpl resolveTestOutput` typeClass 1; `WorkflowValidatorFacadeImpl buildNodeOutputMaps` workflowJsonNode 1
  - most used combinations: `BillingWebhookEventHandler handleSubscriptionUpdated` {stripeSubscription} 1; `PrepaidSubscriptionModelHandler handleSubscriptionUpdated` {subscription} 1; `BillingWebhookEventHandler handleCheckoutSessionCompleted` {session} 1; `BillingUsageServiceImpl doReportUsage` {subscription} 1; `SubscriptionModelHandlerRegistry SubscriptionModelHandlerRegistry` {handler} 1
- Reported, human, the sinew shape at the class: 99 places, 1257 uses; effective number of values 4.506 (over the thirds 4.500, 5.018, 3.459); the most used value's share 0.526; changes repeating a combination already used there 0.322 of 544
  - most used values: `FTDISerialDevice` FTDI_SIO_SET_DATA 13; `FTDISerialDevice` FTDI_SIO_MODEM_CTRL 12; `PL2303SerialDevice` PL2303_REQTYPE_HOST2DEVICE 9; `CP2102SerialDevice` mInterface 9; `Query` attr 8
  - most used combinations: `FTDISerialDevice` {FTDI_SIO_SET_DATA, currentSioSetData} 7; `UsbService` {device} 6; `UsbSerialDevice` {workerThread} 5; `PL2303SerialDevice` {PL2303_REQTYPE_HOST2DEVICE, PL2303_SET_LINE_CODING} 5; `StatsDWriter` {bucketType, rootPrefix} 5
- Reported, human, the sinew shape at the method: 326 places, 1312 uses; effective number of values 2.325 (over the thirds 2.035, 2.669, 1.852); the most used value's share 0.688; changes repeating a combination already used there 0.203 of 626
  - most used values: `Server.Builder Builder` server 9; `ServerJob execute` server 8; `UsbSerialDevice.WorkerThread run` data 7; `KeyUtils getKeyString` sb 6; `KeyUtils getKeyString` result 6
  - most used combinations: `Server.Builder Builder` {server} 9; `UsbSerialDevice.WorkerThread run` {data} 7; `ServerJob execute` {server} 5; `StatsDWriter internalWrite` {query, result, server, typeNames, values} 5; `JmxTransformer scheduleJob` {minuteTrigger, server, trigger} 4
- Reported, at the class on its fields only (as until 19 November 2026): 1.789 [1.536, 2.083]
- Reported, at the class with every member the code was bound to as the core, private or not (as until 22 November 2026): 3.150 [2.734, 3.629]
- Reported, human, the core's width at the class: 2.046 values a row (median 1, 502 rows); over the thirds of the stream 2.158, 1.790, 2.213
- Reported, agent, the core's width at the class: 1.840 values a row (median 1, 25 rows); over the thirds of the stream 1.840, –, –
- Reported, human, the core's width at the method: 2.096 values a row (median 1, 624 rows); over the thirds of the stream 1.727, 2.651, 1.846
- Reported, agent, the core's width at the method: 2.367 values a row (median 2, 30 rows); over the thirds of the stream 2.367, –, –
- Reported, H2 as it stood until 19 November 2026 (later intrusions bound to what stood by, per value that stood by): class 1.061 [1.053, 1.069]; method not estimated (standard error not computed: bystanders_method)
- Reported, agent: 41 bound rows; at the class 6.098 fields stood by, 13 of 29 later intrusions bound to one of them (0.448); at the method 0.878 values stood by, 0 of 4 (0.000)
- Reported, agent, introduced there by the change: at the class 0.585 fields, 16 of 29 later intrusions bound to one of them (0.552), to one that stood by or was introduced 24 (0.828); at the method 1.976 values, 3 of 4 (0.750), to either 3 (0.750)
- Reported, human: 1038 bound rows; at the class 10.418 fields stood by, 2029 of 6229 later intrusions bound to one of them (0.326); at the method 1.650 values stood by, 266 of 1092 (0.244)
- Reported, human, introduced there by the change: at the class 0.511 fields, 280 of 6229 later intrusions bound to one of them (0.045), to one that stood by or was introduced 2182 (0.350); at the method 0.709 values, 125 of 1092 (0.114), to either 376 (0.344)
- Reported, on log(1 + bystanders): class 0.997 [0.907, 1.087]; method 1.604 [1.283, 1.926]
- Reported, per value that stood by, the function arm: class 0.904 [0.709, 1.153]; method 0.035 [0, –]
- Reported, with what the change introduced counted beside what stood by (later intrusions bound to either, per value of both): class 1.059 [1.051, 1.067]; method 1.312 [1.241, 1.386]; in the function arm, class 1.099 [0.981, 1.231]; method not estimated (standard error not computed: left_method)
- Reported, H2 as it stood until 17 November 2026 (later intrusion per binding): class 1.026 [1.001, 1.052]; method 1.088 [1.048, 1.129]
- For information, the same on the problem's own lines: 1.137 [1.083, 1.195]
- Reported, per binding, any later change, bound or not: class 1.019 [0.995, 1.044]; method 1.082 [1.047, 1.118]
- Reported, per binding, existing hosts only: class 1.023 [0.998, 1.049]; method 1.087 [1.047, 1.128]
- Reported, per binding, without injected dependencies: class 1.024 [0.999, 1.050]; method 1.086 [1.046, 1.127]

## H3, the encapsulation fills (methods arm)

Runs that need a pre-existing value 1181 over 2 chains; the slope of log(1 + bystanders) on the checkpoint index, cluster-bootstrap 95% interval (200 refits).

- **Bystanders on the checkpoint index: 0.511 [0.375, 0.734]**
- **Within a class, the class's bystanders: 0.995 [0.786, 1.424]** (97 classes with runs at two or more checkpoints)
- **Within a method, the method's bystanders: 0.391 [0.291, 0.499]** (221 methods)
- Reported, within a place in the function arm: class 22.129 [22.129, 22.129]; method 60.955 [60.955, 60.955]
- Reported, method bystanders -0.071 [-0.210, 0.067]; class bystanders 0.805 [0.600, 1.009]
- Reported, without injected dependencies 0.510 [0.322, 0.698]; without constants 0.641 [0.484, 0.799]
- Reported, the function arm's slope: 0.978 [-0.614, 2.570]
- Reported, agent: 45 of 67 runs need a pre-existing value (0.328 free); per such run, needed 2.422, bystanders 7.644 (method 1.378, class 6.267; without constants 7.156); over the thirds of the stream –, –, –; fields left behind per addition 1.556; method values introduced per addition 12.556
- Reported, human: 1181 of 1924 runs need a pre-existing value (0.386 free); per such run, needed 2.318, bystanders 12.882 (method 1.767, class 11.115; without constants 6.786); over the thirds of the stream –, –, –; fields left behind per addition 0.828; method values introduced per addition 3.325
- Reported, H3 as first registered (bindings of runs into existing methods): on log(host positions) -0.085 [-0.115, -0.054]; on the checkpoint index 0.000345 [3.08e-05, 0.000659]
- Reported, bindings in the function arm: on host size -0.330 [-0.476, -0.184]
- Reported, bindings at class level (methods arm): on class size -0.014 [-0.042, 0.015]
- Reported, bindings without injected dependencies: on host size -0.085 [-0.115, -0.054]; class level on class size -0.014 [-0.042, 0.015]

## H4, function injection forms no core

- **Function arm's bystanders (arm term, at checkpoint 0.5, the middle of the stream): -0.102 [-0.523, 0.314]**
- **Their slope on the checkpoint index (interaction): 0.468 [0.244, 0.603]**
- **Later intrusion where bound code was placed, function arm / methods arm: at the class 0.075 [0.027, 0.210]; at the method 0.072 [0.023, 0.228]**
- How much a core value is come back to, function arm / methods arm (H2's arm contrast): at the class 0.139 [0.039, 0.489]; at the method not estimated (one chain in an arm)
- Reported, agent, uses per 100 values and later checkpoints: at the class core 0.082 (9 uses of 46 values in 25 rows), periphery 0.019; at the method core 0.000 (0 uses of 71 values in 30 rows), periphery 0.010
- Reported, human, uses per 100 values and later checkpoints: at the class core 0.736 (1135 uses of 1027 values in 502 rows), periphery 0.201; at the method core 0.299 (766 uses of 1308 values in 624 rows), periphery 0.137
- Reported, agent: per checkpoint, classes its bound code goes back into 0.364, wiring files changed again 0.000
- Reported, human: per checkpoint, classes its bound code goes back into 0.884, wiring files changed again 0.000
- Reported, reopening, function arm / methods arm: classes 0.422 [0.153, 1.164]; with wiring files 0.422 [0.153, 1.164]
- Reported, bystanders without injected dependencies: arm 0.096 [-0.959, 1.151], slope 3.808 [1.669, 5.947]
- Reported, the needed values, function arm against methods arm: 0.086 [-0.117, 0.290] (expected about 0: the same stream)
- Reported, H4 as first registered (bindings): arm at a host of 7.3 positions 0.209 [-0.031, 0.449]; slope on host size -0.214 [-0.365, -0.063]
- Reported, the arm difference in bindings at a host of 10 positions 0.143 [-0.091, 0.378]; 25 positions -0.053 [-0.324, 0.218]; 50 positions -0.201 [-0.537, 0.135]
- Amount added since the base, function arm / methods arm at the final checkpoint: – [–, –], in band: –
- Reported, the ratio of the totals: –
- Wiring growth: slope –, interval None, against: –
- Wiring concentration: largest file –, against: –
- Reported, bindings without parameters: arm 0.087 [-0.093, 0.267], slope -0.195 [-0.343, -0.047]
- Reported, bindings without injected dependencies: arm 0.081 [-0.158, 0.320], slope -0.127 [-0.278, 0.025]
- Reported, trajectory of the bindings (arm × checkpoint): 0.003 [-0.003, 0.008]

## H5, surface against volume

Per checkpoint, the links it added between blocks of logic (the surface: a method calling a method, a method using a field that holds state, a function wired to the next), each weighed by the data it carries (a call 1, +1 per parameter, +1 if it returns a value; a state link 1; a wiring edge 1, +1 if it carries a value), an injected dependency weighing nothing; against the logic it added (the volume). The function arm's ratio half-way through the stream, for the same logic, below 1, **and** its interaction with the checkpoint index below 1 (the gap widens); one-sided, 95% cluster-bootstrap intervals (chains resampled).

- **descriptive only**
- Not testable on a history: its arms do not solve the same problems.

## H6, shape does not draw code in

- **not above** (one-sided: each rate ratio below 1.250); each measure fitted alone at its level, with the bindings and the bystanders in the model, 90% intervals: method measures on intrusion at the method (n = 956), class measures on intrusion at the class, one row per class and checkpoint with the class's size held fixed (n = 746); reported, two-sided (0.800 to 1.250): within
  - s4_cognitive (method): 1.096 [0.976, 1.232], one-sided p 0.033 (two-sided TOST p 0.033)
  - c_gini (class): 1.091 [1.031, 1.154], one-sided p 3.59e-05 (two-sided TOST p 3.59e-05)
  - Left out by the variation rule: s1_long ({'agent': 8, 'human': 213}), m_cyclomatic ({'agent': 0, 'human': 0}), c_wmc ({'agent': 0, 'human': 0}), c_lcom_star ({'agent': 0, 'human': 0})
  - Reported, a sensitivity reading: H6's rule with the literature's coupling measures put back (fan-out, CBO, RFC; read apart in this plan as reach): **not above** over c_gini, s4_cognitive. It changes no verdict.
- Reported, the block as first registered, together in one model on method-level intrusion: s4_cognitive 1.109 [0.985, 1.248]; s5_class_gini 0.947 [0.869, 1.032]
- Reported, that block on class-level intrusion: s4_cognitive 1.134 [1.049, 1.225]; s5_class_gini 1.167 [1.100, 1.239]
- Reported, that block without the problem terms, the bindings and the bystanders: s4_cognitive 1.239 [1.123, 1.367]; s5_class_gini 0.968 [0.873, 1.073]
- Reported, the sinew measures (data flow, not shape; predicted above 1), later intrusion with the bindings and the bystanders in the model: s3_junction at the method 0.767 [0.612, 0.960], at the class 0.897 [0.775, 1.039]; left out by the variation rule: s2_stuck ({'agent': 1, 'human': 16})
- Reported, junction × arm (s3_junction): 5.45e-08 [0, –]
- Reported, junction × arm (s3_junction_injection_aware): 5.45e-08 [0, –]

## H7, spread does not see it (methods arm; secondary)

Per unit that placed or edited code in classes that existed before it, those classes beyond the first (a new class is a free choice and is not counted): co-change spread, the change-coupling literature's measure. The ratio of the spread of a unit with a placement forced at the class (by encapsulation) to one without, at the same change size and point in the stream; one-sided, shown below the upper margin 1.250, 90% interval (restated 21 November 2026; until then *forced changes spread*, one-sided above 1).

- **descriptive only** (not above)
- **Forced: 0.845 [0.673, 1.061]** (n = 462, nbinom2; one-sided p below the margin 0.002)
- Reported, forced by binding with no alternative (H1's): 1.191 [0.867, 1.636]; forced without the change's size: 1.987 [1.305, 3.025]
- Reported, the spread's rise over the stream (end against start): all units 1.492 [0.951, 2.341] (n = 462, nbinom2); forced units 1.750 [1.021, 2.998] (n = 250, nbinom2); unforced units 1.240 [0.545, 2.821] (n = 212, nbinom2)
- Reported, methods arm: 462 units, 1.944 existing classes a unit (2.065 with new ones), 0.327 in more than one; units with a forced placement 0.541, their classes 2.240 against 1.594; over the thirds, all 1.500, 2.253, 2.113; forced 1.667, 2.494, 2.449; unforced 1.367, 1.902, 1.623
- Reported, function arm: 8 units, 2.750 existing classes a unit (2.750 with new ones), 0.625 in more than one; units with a forced placement 0.750, their classes 3.333 against 1; over the thirds, all 1.833, 5.500, –; forced 2.250, 5.500, –; unforced 1, –, –
- Reported, the function arm: forced 6244559.163 [0, –]; rise 0.111 [2.46e-06, 4976.641]; function arm / methods arm: 1.932 [0.552, 6.757]

### Where the growth of existing classes came from

Positions added to classes that existed, by the placement that added them: forced at the class, with a choice there, or not bound at the class.

- human arm: 3972.000 positions; forced 0.453, chosen 0.088, unbound 0.459; forced over the thirds 0.476, 0.451, 0.425
- agent arm: 193.000 positions; forced 0.699, chosen 0.000, unbound 0.301; forced over the thirds 0.773, 0.500, –

By the strictest access of the members the code was bound to at the class: private forces; package and protected are a looser encapsulation (descriptive).

- human arm: private 0.453, package 0.006, protected 0.026, public 0.039, unbound 0.476
- agent arm: private 0.699, unbound 0.301

Within the forced growth, whether the lever of injection was there: bound to the class's own private state, constants or methods (no lever), or only to injected private fields, which another class could declare too (the opportunity to duplicate the core; still forced, because it was not exercised).

- human arm: 1800.000 positions forced (0.453 of the growth, 503 placements); own private members 1.000; injected only 0.000 (another class already holds the dependencies 0.000, none yet 0.000)
- agent arm: 135.000 positions forced (0.699 of the growth, 25 placements); own private members 0.267; injected only 0.733 (another class already holds the dependencies 0.719, none yet 0.015)

### Where coupling between classes came from

Calls between classes each unit added (the tree after it less the tree before), over every class.

- human arm: 745 calls added over 647 units; in units with a forced placement 177 (0.238), in the others 263; between existing classes changed together -16 (-0.021), of it in forced units -29 (-0.039)
- agent arm: 147 calls added over 11 units; in units with a forced placement 99 (0.673), in the others 0; between existing classes changed together 6 (0.041), of it in forced units 6 (0.041)

### Pairs of classes changed together

- The coupling of pairs changed together more than once (calls between them before the unit) on the index: 1.691 [0.950, 3.008] (586 pairs, 1468 rows; refitted without the chain's intercept)
- agent arm: 43 pairs of classes changed together, 1 more than once; of those, coupling rose in 1 and fell in 0
  - candidate for redistribution: `BillingWebhookEventHandler` and `PrepaidSubscriptionModelHandler` (agent/bytechefhq__bytechef), changed together 2 times, calls between them 0 → 1
- human arm: 1240 pairs of classes changed together, 586 more than once; of those, coupling rose in 25 and fell in 22
  - candidate for redistribution: `CP2102SerialDevice` and `UsbSerialDevice` (human/felHR85__UsbSerial), changed together 8 times, calls between them 0 → 3
  - candidate for redistribution: `FTDISerialDevice` and `UsbSerialDevice` (human/felHR85__UsbSerial), changed together 7 times, calls between them 2 → 3
  - candidate for redistribution: `SerialBuffer` and `UsbSerialDevice` (human/felHR85__UsbSerial), changed together 6 times, calls between them 0 → 4
  - candidate for redistribution: `FTDISerialDevice` and `FTDISerialDevice.FTDIUtilities` (human/felHR85__UsbSerial), changed together 6 times, calls between them 0 → 3
  - candidate for redistribution: `CH34xSerialDevice` and `UsbSerialDevice` (human/felHR85__UsbSerial), changed together 5 times, calls between them 1 → 3
  - candidate for redistribution: `Server` and `Server.Builder` (human/jmxtrans__jmxtrans), changed together 5 times, calls between them 2 → 3
  - candidate for redistribution: `SerialPortBuilder` and `UsbService` (human/felHR85__UsbSerial), changed together 5 times, calls between them 0 → 2
  - candidate for redistribution: `UsbSerialDevice` and `UsbSerialDevice.WorkerThread` (human/felHR85__UsbSerial), changed together 4 times, calls between them 1 → 4
  - candidate for redistribution: `CDCSerialDevice` and `UsbSerialDevice` (human/felHR85__UsbSerial), changed together 4 times, calls between them 2 → 4
  - candidate for redistribution: `PL2303SerialDevice` and `UsbSerialDevice` (human/felHR85__UsbSerial), changed together 4 times, calls between them 2 → 3

## H9, the cost to fix a concentration (secondary)

Each class with two or more blocks at the end of the stream: its cheapest split, the fewest internal links (calls between its blocks, blocks sharing a field that holds state) a cut must cross to divide it into two parts of at least a quarter of its code each. The function arm's rate at the same size below 1, **and** the gap widening as classes grow (arm × size below 1); one-sided, 95% cluster-bootstrap intervals.

- **descriptive only**
- Not testable on a history: its arms do not solve the same problems.

## Reported: where forced coupling came from

Each class a forced change went into: *contained* (no call added across its boundary); *problem or reuse* (every call it added joins two classes whose private data the change needed, or reaches a member that was already open); *other* (some call reaches a member the change opened, in a class whose data it did not need: a utility, as the author reads it). The calls are counted once each by the same sources.

- agent arm, forced class rows 13: contained 3 (0.231), problem or reuse 5 (0.385), other 5 (0.385)
  - calls of forced changes: problem 7, reuse 71, other 16
  - calls of unforced changes: problem 0, reuse 10, other 10
- human arm, forced class rows 354: contained 229 (0.647), problem or reuse 69 (0.195), other 56 (0.158)
  - calls of forced changes: problem 26, reuse 324, other 140
  - calls of unforced changes: problem 0, reuse 357, other 209

## Reported: split or concentrate (redesign reading)

*Split:* a class whose forced changes fall into groups sharing none of its values. *Concentrate:* a pair changed together at least three times over the same data, its coupling rising.

- human arm, split: 69 classes with two or more forced changes; flagged 20, of which 11 with groups changed with different classes
  - `JmxTransformer` (human/jmxtrans__jmxtrans, at 168): groups parseOptions(), runEndlessly | poolMBeans, poolMap; changed with different classes: no
  - `Server` (human/jmxtrans__jmxtrans, at 231): groups cronExpression, host, numQueryThreads, port, queries, url | getUrl(), pid; changed with different classes: no
  - `CP2102SerialDevice` (human/felHR85__UsbSerial, at 11): groups CP210x_IFC_ENABLE, CP210x_LINE_CTL_DEFAULT, CP210x_MHS_DEFAULT, CP210x_SET_BAUDRATE, CP210x_SET_FLOW, CP210x_SET_LINE_CTL, CP210x_SET_MHS, CP210x_UART_ENABLE, inEndpoint, mInterface, outEndpoint, setBaudRate(), setControlCommand(), setFlowControl() | requestIN; changed with different classes: no
  - `Query` (human/jmxtrans__jmxtrans, at 246): groups attr, keys, obj, resultAlias, server | outputWriters; changed with different classes: no
  - `FTDISerialDevice` (human/felHR85__UsbSerial, at 61): groups CLASS_ID, FTDI_BAUDRATE_115200, FTDI_BAUDRATE_1200, FTDI_BAUDRATE_19200, FTDI_BAUDRATE_230400, FTDI_BAUDRATE_2400, FTDI_BAUDRATE_300, FTDI_BAUDRATE_38400, FTDI_BAUDRATE_460800, FTDI_BAUDRATE_4800, FTDI_BAUDRATE_57600, FTDI_BAUDRATE_600, FTDI_BAUDRATE_921600, FTDI_BAUDRATE_9600, FTDI_SET_DATA_DEFAULT, FTDI_SET_FLOW_CTRL_DEFAULT, FTDI_SET_MODEM_CTRL_DEFAULT1, FTDI_SET_MODEM_CTRL_DEFAULT2, FTDI_SET_MODEM_CTRL_DEFAULT3, FTDI_SET_MODEM_CTRL_DEFAULT4, FTDI_SIO_MODEM_CTRL, FTDI_SIO_RESET, FTDI_SIO_SET_BAUD_RATE, FTDI_SIO_SET_DATA, FTDI_SIO_SET_FLOW_CTRL, currentSioSetData, setControlCommand() | FTDI_REQTYPE_HOST2DEVICE, mInterface; changed with different classes: no
  - `PL2303SerialDevice` (human/felHR85__UsbSerial, at 61): groups PL2303_REQTYPE_HOST2DEVICE, PL2303_REQTYPE_HOST2DEVICE_VENDOR, PL2303_SET_LINE_CODING, PL2303_VENDOR_WRITE_REQUEST, defaultSetLine, setControlCommand() | mInterface; changed with different classes: yes
  - `GraphiteWriter` (human/jmxtrans__jmxtrans, at 108): groups address, details, host, pool, port | status; changed with different classes: yes
  - `CDCSerialDevice` (human/felHR85__UsbSerial, at 91): groups CDC_GET_LINE_CODING, CDC_REQTYPE_DEVICE2HOST, CDC_REQTYPE_HOST2DEVICE, mInterface | CDC_DEFAULT_CONTROL_LINE, CDC_DEFAULT_LINE_CODING, CDC_SET_CONTROL_LINE_STATE, CDC_SET_LINE_CODING, setControlCommand(); changed with different classes: yes
  - `CH34xSerialDevice` (human/felHR85__UsbSerial, at 111): groups mInterface | CLASS_ID, checkState(), setControlCommandOut(); changed with different classes: no
  - `GangliaWriter` (human/jmxtrans__jmxtrans, at 93): groups sendMetricMetadata() | addressingMode, dmax, getType(), groupName, host, port, slope, spoofedHostname, tmax, ttl, units, v31; changed with different classes: no
- human arm, concentrate: 1225 pairs changed together, 152 at least three times; flagged 12
  - `SerialBuffer` and `UsbSerialDevice` (human/felHR85__UsbSerial): changed together 6 times, the same data 1.000
  - `SerialPortBuilder` and `UsbService` (human/felHR85__UsbSerial): changed together 5 times, the same data 0.500
  - `Server` and `Server.Builder` (human/jmxtrans__jmxtrans): changed together 5 times, the same data 1.000
  - `CP2102SerialDevice` and `UsbSerialDevice.WorkerThread` (human/felHR85__UsbSerial): changed together 4 times, the same data 0.667
  - `SerialBuffer` and `UsbSerialDevice.WorkerThread` (human/felHR85__UsbSerial): changed together 4 times, the same data 0.667
  - `GraphiteWriter` and `InterestingInfo` (human/jmxtrans__jmxtrans): changed together 3 times, the same data 0.500
  - `JmxUtils` and `Query` (human/jmxtrans__jmxtrans): changed together 3 times, the same data 0.500
  - `BaseOutputWriter` and `Query` (human/jmxtrans__jmxtrans): changed together 3 times, the same data 0.500
  - `CloudWatchWriter` and `Query` (human/jmxtrans__jmxtrans): changed together 3 times, the same data 0.500
  - `DailyKeyOutWriter` and `KeyOutWriter` (human/jmxtrans__jmxtrans): changed together 3 times, the same data 0.500
- agent arm, split: 3 classes with two or more forced changes; flagged 0, of which 0 with groups changed with different classes
- agent arm, concentrate: 43 pairs changed together, 0 at least three times; flagged 0

## Reported: surface against volume, and ripple

A class's surface (calls out and in) against its volume (methods). The exponent below 1: surface grows slower than volume, so concentrating saves communication; above 1: faster. Ripple: of the later changes to a method a unit's new call reached, the share that also changed the calling class.

- human arm: exponent across the classes of the last tree 0.616 [0.512, 0.720] (231 classes); within a class as it grows 0.857 [0.723, 0.992] (175 classes, 891 changes)
  - surface a change added, forced against unforced at the same methods added: -0.153 [-0.467, 0.160]; forced 0.073 calls for 0.184 methods; unforced 0.276 calls for 0.246 methods
- agent arm: exponent across the classes of the last tree not estimated (too few classes); within a class as it grows 2.069 [-2.840, 6.977] (18 classes, 22 changes)
  - surface a change added, forced against unforced at the same methods added: 1.429 [-0.412, 3.270]; forced 3.077 calls for 1.154 methods; unforced 1.222 calls for 0.889 methods
- Ripple, human arm, forced, opened: 151 new calls; 36 reach a method changed later, 49 later changes, 5 of them changing the caller too (0.102; by chance 0.061; ratio 1.681)
- Ripple, human arm, forced, existing: 339 new calls; 63 reach a method changed later, 121 later changes, 12 of them changing the caller too (0.099; by chance 0.045; ratio 2.188)
- Ripple, human arm, unforced, opened: 209 new calls; 73 reach a method changed later, 142 later changes, 23 of them changing the caller too (0.162; by chance 0.062; ratio 2.595)
- Ripple, human arm, unforced, existing: 357 new calls; 86 reach a method changed later, 142 later changes, 17 of them changing the caller too (0.120; by chance 0.049; ratio 2.444)
- Ripple, agent arm, forced, opened: 22 new calls; 1 reach a method changed later, 1 later changes, 0 of them changing the caller too (0.000; by chance 0.222; ratio 0.000)
- Ripple, agent arm, forced, existing: 72 new calls; 0 reach a method changed later, 0 later changes, 0 of them changing the caller too (–; by chance –; ratio –)
- Ripple, agent arm, unforced, opened: 10 new calls; 0 reach a method changed later, 0 later changes, 0 of them changing the caller too (–; by chance –; ratio –)
- Ripple, agent arm, unforced, existing: 10 new calls; 0 reach a method changed later, 0 later changes, 0 of them changing the caller too (–; by chance –; ratio –)

## Reported: encapsulation and the reader

Whether encapsulation answers a reader's limit: per author group (on a history, declared agent commits against people), the private share of the members a unit introduces, the share of growth of existing classes arriving forced, the members opened per class row changed, and the methods of the classes code lands in; by the system's size in tokens against a context window (below 200k, 200k to 1M, above 1M). Predicted (the author's question): agents make fewer private, open more and let classes grow larger where the system fits in a window, the difference narrowing where it does not.

- agent, all: 9 units in 1 repositories; private share 0.474 of 211.000 introduced; forced share 0.699; opened per class row 0.955 (22 rows); class methods mean 16.136, median 14.500; splits per unit 0.000; median tokens 3368432.000
- agent, above 1M: 9 units in 1 repositories (too thin); private share 0.474 of 211.000 introduced; forced share 0.699; opened per class row 0.955 (22 rows); class methods mean 16.136, median 14.500; splits per unit 0.000; median tokens 3368432.000
- human, all: 489 units in 2 repositories; private share 0.440 of 3385.000 introduced; forced share 0.453; opened per class row 0.506 (896 rows); class methods mean 13.446, median 8.000; splits per unit 0.016; median tokens 33240.000
- human, below 200k: 489 units in 2 repositories (too thin); private share 0.440 of 3385.000 introduced; forced share 0.453; opened per class row 0.506 (896 rows); class methods mean 13.446, median 8.000; splits per unit 0.016; median tokens 33240.000
- Models (the author contrast at 32198.598 tokens, and its change per e-fold larger system):
  - private share (odds ratio): author 5.35e-148 [4.82e-262, 5.93e-34]; × size 39899212759308999149133087375360.000 [12833173.988, 124049372377464998553713579242613900226657669534277697536.000]; size 1.078 [0.984, 1.180] (n = 306, 3 repositories)
  - forced share (odds ratio): author 1386219681309400066925800242684847956605647393297141983639786235895141742272325075173483616800385577715070784460035295286001234826316814828043652190018431252921207772077435874388637384704.000 [880733477725537979349259836127273720834296905728.000, –]; × size 1.4e-40 [2.86e-70, 6.88e-11]; size 0.902 [0.832, 0.978] (n = 470, 3 repositories)
  - members opened (rate ratio): author 212939.661 [5.01e-233, 905234635916168048494686407397847889543361941374082311943839795611974974019341437858600928997838138852043248900927122690658751403952270512856194998783338645223225851225082687533643512687242181028830594541335669365020965384719066667296955039744.000]; × size 0.085 [7.73e-53, 94073681822611600440075171839206547243576588238848.000]; size 0.913 [0.802, 1.040] (n = 918, 3 repositories)
  - class methods (rate ratio): author 4e-92 [1.36e-254, 117680258228113004899213121684573114912712604806477342944090918792200192.000]; × size 34039313284661100544.000 [4.3e-16, 2694999432838650081469084111616027752865569581595361280.000]; size 1.270 [1.160, 1.391] (n = 918, 3 repositories)

## Reported readings: choice, formation, review

- Choice, agent: 0 of 0 checkpoints left no choice (every chain with the same bindings, on the same side of new or existing); median spread of bindings over chains –, median distinct hosts –
- Choice, human: 15 of 141 checkpoints left no choice (every chain with the same bindings, on the same side of new or existing); median spread of bindings over chains 1.500, median distinct hosts 5
- Formation, lagged, agent: bindings now on the chain's mean bindings so far -1.606 [-2.639, -0.573] (predicted above 0 in the methods arm)
- Formation, lagged, human: bindings now on the chain's mean bindings so far 0.060 [-0.109, 0.228] (predicted above 0 in the methods arm)
- Capture, agent: share of the addition landing in existing hosts on the fields held by the chain's heaviest class 0.215 [-0.017, 0.448] (predicted above 0 in the methods arm)
- Capture, human: share of the addition landing in existing hosts on the fields held by the chain's heaviest class 0.100 [0.066, 0.134] (predicted above 0 in the methods arm)
- Size or data, at the class (both arms pooled, no arm term, n = 956): later intrusion per value that stood by, size held fixed, 1.021 [1.014, 1.028] (predicted above 1); per log of size, with what stood by held fixed, 1.322 [1.237, 1.413]; size alone 1.433 [1.345, 1.526]; within arms, bystanders 1.021 [1.015, 1.028] and size 1.321 [1.236, 1.412]; Spearman's rho of size with what stood by: pooled 0.492, agent 0.584, human 0.491
- Size or data, at the method (both arms pooled, no arm term, n = 1077): later intrusion per value that stood by, size held fixed, 1.055 [1.011, 1.101] (predicted above 1); per log of size, with what stood by held fixed, 1.149 [1.021, 1.292]; size alone 1.229 [1.106, 1.365]; within arms, bystanders 1.052 [1.008, 1.098] and size 1.147 [1.020, 1.290]; Spearman's rho of size with what stood by: pooled 0.682, agent 0.741, human 0.681
- Own lines followed, agent: 209 placed, 0 lost track of (0.0%)
- Own lines followed, human: 5041 placed, 748 lost track of (14.8%)

## Reported: where bound and unbound code lands

A rank is the place's standing among every candidate of its checkpoint (0.5: no regard to that size; near 1: the largest). Method ranks are over landings into existing methods, class ranks over landings into existing classes.

| Arm | Code | Landings | Existing method | New method | New class | Method: complexity | Method: data width | Class: complexity | Class: fields | Agreement (method) | Agreement (class) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| agent | bound | 41 | 0.805 | 0.195 | 0.000 | 0.700 (n 33) | 0.580 | 0.614 (n 41) | 0.569 | 0.062 | 0.099 |
| agent | unbound | 19 | 0.316 | 0.474 | 0.211 | 0.295 (n 6) | 0.622 | 0.417 (n 15) | 0.559 | -0.154 | 0.125 |
| human | bound | 1038 | 0.890 | 0.108 | 0.002 | 0.636 (n 926) | 0.584 | 0.612 (n 1033) | 0.555 | 0.447 | 0.234 |
| human | unbound | 692 | 0.354 | 0.282 | 0.364 | 0.574 (n 246) | 0.520 | 0.575 (n 434) | 0.546 | 0.227 | 0.205 |

Unbound code entering a class that existed, function arm against methods arm, odds ratio: 2.148 [0.705, 6.541] (shares {'agent': 0.789473684210526, 'human': 0.635838150289017}).

Agreement is Spearman's rho, over the places landed in, of the complexity rank with the data-width rank: whether the two kinds of size point to the same places.

## Reported: the literature's shape measures, each alone

Later intrusion per standard deviation of the measure (a flag: present against absent), with the problem, the bindings and what stood by held fixed. Method measures on intrusion at the method, class measures on intrusion at the class, one row per class a checkpoint's bound code went into (746 rows), with the class's size held fixed and an intercept for the class (†: refitted without it). Read as H6 is: below 1.25 does not draw code in. A measure marked reversed is one where higher is better; its ratio is for the worse shape.

| Measure | Level | Source | n | Rate ratio (90% interval) | One-sided p | Against 1.25 |
|---|---|---|---|---|---|---|
| s4_cognitive | method | Campbell 2018, cognitive complexity | 956 | 1.096 [0.976, 1.232] | 0.033 | below |
| c_gini | class | concentration of the class's positions (Gini) | 746 | 1.091 [1.031, 1.154] | 3.59e-05 | below |

Left out by the variation rule (bound rows flagged or above zero, per arm): s1_long ({'agent': 8, 'human': 213}), m_cyclomatic ({'agent': 0, 'human': 0}), m_npath ({'agent': 0, 'human': 0}), m_nesting ({'agent': 0, 'human': 0}), m_fanout ({'agent': 0, 'human': 0}), m_halstead ({'agent': 0, 'human': 0}), m_mi ({'agent': 0, 'human': 0}), m_demeter ({'agent': 0, 'human': 0}), m_duplicated ({'agent': 0, 'human': 0}), c_wmc ({'agent': 0, 'human': 0}), c_lcom_star ({'agent': 0, 'human': 0}), c_tcc ({'agent': 0, 'human': 0}), c_cbo ({'agent': 0, 'human': 0}), c_rfc ({'agent': 0, 'human': 0}), c_dit ({'agent': 0, 'human': 0}), c_fanout ({'agent': 0, 'human': 0}), c_imports ({'agent': 0, 'human': 0}), c_halstead ({'agent': 0, 'human': 0}), c_mi ({'agent': 0, 'human': 0}), c_god_class ({'agent': 0, 'human': 0}), c_data_class ({'agent': 0, 'human': 0}), c_demeter ({'agent': 0, 'human': 0}), c_duplicated ({'agent': 0, 'human': 0}).

## Provenance

Checkpoint intercept in the model: H3 no, H4 no, H2_class no, H2_method no, H4_intrusion_class no, H4_intrusion_method no, shape_joint no.

Versions: {"R": "R version 4.5.2 (2025-10-31)", "glmmTMB": "1.1.14", "TMB": "1.9.19"}. Seed 20261116.

| Arm | Run | Chain | Commit |
|---|---|---|---|

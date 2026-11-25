"""Step 5: the report of every analysis, every hypothesis whichever way it falls (PLAN.md §8).

    python -m placement_gravity.report

Writes results/analysis/<name>/REPORT.md from verdicts.json, estimates.json and the data's
conditions.json, and results/analysis/REPORT.md listing every analysis's verdicts.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import prepare, runs, validate

OUT = runs.RESULTS / "analysis"


def f(x, nd=3) -> str:
    if x is None:
        return "–"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return f"{x:.{nd}g}" if abs(x) < 1e-3 and x != 0 else f"{x:.{nd}f}"
    return str(x)


def interval(e: dict | None, key="estimate", lo="lower", hi="upper") -> str:
    if not e or "error" in e:
        return f"not estimated ({(e or {}).get('error', 'no data')})"
    return f"{f(e.get(key))} [{f(e.get(lo))}, {f(e.get(hi))}]"


def ratio(e: dict | None) -> str:
    return interval(e, "irr", "irr_lower", "irr_upper")


def width_lines(rep: dict) -> list[str]:
    """Beside H2: the core's width, its number of values per row, per arm and over the thirds."""
    L = []
    for lev in ("class", "method"):
        for arm, w in (rep.get(f"H2_core_width_{lev}") or {}).items():
            th = w.get("thirds") or {}
            L.append(f"- Reported, {arm}, the core's width at the {lev}: {f(w.get('mean'))} values a row "
                     f"(median {f(w.get('median'))}, {f(w.get('rows'))} rows); over the thirds of the stream "
                     + ", ".join(f(th.get(k)) for k in ("1", "2", "3")))
    return L


def h1_section(est: dict, hyp: dict, rep: dict) -> list[str]:
    """H1, choice narrows (PLAN.md §2, §4.2a, §5)."""
    b = est.get("H1") or {}
    h = hyp.get("H1") or {}
    L = ["", "## H1, choice narrows (and less often forced in the function arm)", "",
         "Per bound addition, the other places in the code before its checkpoint that hold what its code "
         "was bound to: at the class, another class holding injected dependencies of the same types (code "
         "bound to the class's own state, constants or methods has none); at the method, another method "
         "with a parameter or local of each type. The ratio of the alternatives at the end of the stream "
         "to its start: a fall, one-sided below 1, at the class, 95% cluster-bootstrap interval (chains "
         "resampled). The method level is reported.", "",
         f"- **{h.get('verdict', '–')}** ({h.get('state', '–')})"]
    c = b.get("contrast")
    if c is not None:
        L.append("- The arm contrast (since 24 November 2026): the placements forced at the class per checkpoint "
                 "(bound there with no other place to go), function arm / methods arm half-way through the "
                 "stream, and the gap over the stream; both one-sided below 1.")
        if "error" in c:
            L.append(f"- **Arm contrast: not estimated** ({c['error']})")
        for k, lab in (("arm", "Forced per checkpoint, function arm / methods arm"),
                       ("trend", "Its change over the stream (arm × checkpoint index)")):
            x = c.get(k)
            if x:
                L.append(f"- **{lab}: {ratio(x)}** (one-sided p {f(x.get('p_less'))}; {x.get('interval', '–')}; "
                         f"{c.get('family', '–')})")
        if c.get("mean"):
            L.append("- Forced at the class a checkpoint: " + ", ".join(f"{a} {f(v)}" for a, v in c["mean"].items())
                     + f"; the methods arm's own rise over the stream {ratio(c.get('methods_rise'))}")
    for lev in ("class", "method"):
        x = b.get(lev) or {}
        if x.get("all_forced"):
            L.append(f"- **At the {lev}: every placement forced** ({f(x.get('n'))} rows; no alternative anywhere)")
        else:
            L.append(f"- **At the {lev}: {ratio(x)}** (n = {f(x.get('n'))}"
                     + (f"; one-sided p {f(x.get('p_less'))}" if "p_less" in x else "")
                     + (f"; {x['interval']}" if x.get("interval") else "") + ")")
            L.append(f"- Reported, at the {lev} against the upper margin "
                     f"{f((b.get('margin') or [None, None])[1])} (as H1 stood until 22 November 2026, 90% Wald "
                     f"interval): {ratio(rep.get(f'H1_margin_{lev}'))}")
        for arm, sp in (rep.get(f"H1_spread_{lev}") or {}).items():
            if not sp:
                continue
            tf, ta = sp.get("thirds_forced") or {}, sp.get("thirds_alternatives") or {}
            L.append(f"- Reported, {arm} arm at the {lev}: {f(sp.get('rows'))} rows, {f(sp.get('forced'))} forced, "
                     f"{f(sp.get('mean_alternatives'))} alternatives a row; over the thirds, forced "
                     + ", ".join(f(tf.get(k)) for k in ("1", "2", "3")) + "; alternatives "
                     + ", ".join(f(ta.get(k)) for k in ("1", "2", "3")))
        L.append(f"- Reported, the function arm's ratio at the {lev}: {ratio(rep.get(f'H1_function_arm_{lev}'))}; "
                 f"function arm / methods arm: {ratio(rep.get(f'H1_arm_{lev}'))}")
    fl = rep.get("H1_flow") or {}
    L.append(f"- Reported, at the method by type alone over the whole tree (as first built): "
             f"{ratio(rep.get('H1_method_by_type'))}; methods on a host's control flow, per arm: "
             + ", ".join(f"{a} {f(v)}" for a, v in (fl.get("methods") or {}).items())
             + "; by type over the whole tree: "
             + ", ".join(f"{a} {f(v)}" for a, v in (fl.get("by_type") or {}).items())
             + f"; calls to a name the application declares that were followed by their receiver's type: "
             f"{f(fl.get('followed'))} (the rest have a receiver the instrument cannot read)")
    L.append(f"- Reported, class rows bound to the class's own state, constants or methods: "
             f"{f(rep.get('H1_class_own'))}; method values of no declared type left out of the match: "
             f"{f(rep.get('H1_method_untyped'))}")
    return L


def h7_section(est: dict, hyp: dict, rep: dict, rd: dict) -> list[str]:
    """H7, spread does not see it (PLAN.md §2, §4.2b, §5; restated 21 November 2026), and its
    accountings."""
    b = est.get("H7") or {}
    h = hyp.get("H7") or {}
    fo = b.get("forced") or {}

    def fam(e):
        e = e or {}
        return f"n = {f(e.get('n'))}, {e.get('family', '–')}"

    margin = (b.get("margin") or [0.8, 1.25])[1]
    L = ["", "## H7, spread does not see it (methods arm; secondary)", "",
         "Per unit that placed or edited code in classes that existed before it, those classes beyond the "
         "first (a new class is a free choice and is not counted): co-change spread, the change-coupling "
         "literature's measure. The ratio of the spread of a unit with a placement forced at the class (by "
         "encapsulation) to one without, at the same change size and point in the stream; one-sided, shown "
         f"below the upper margin {f(margin)}, 90% interval (restated 21 November 2026; until then "
         "*forced changes spread*, one-sided above 1).", "",
         f"- **{h.get('verdict', '–')}**" + (f" ({h['state']})" if h.get("state") else ""),
         f"- **Forced: {ratio(fo)}** ({fam(fo)}; one-sided p below the margin {f(fo.get('p_upper'))})",
         f"- Reported, forced by binding with no alternative (H1's): {ratio(rep.get('H7_forced_bind'))}; "
         f"forced without the change's size: {ratio(rep.get('H7_forced_without_size'))}",
         f"- Reported, the spread's rise over the stream (end against start): all units {ratio(rep.get('H7_rise'))} "
         f"({fam(rep.get('H7_rise'))}); forced units {ratio(rep.get('H7_rise_forced'))} ({fam(rep.get('H7_rise_forced'))}); "
         f"unforced units {ratio(rep.get('H7_rise_unforced'))} ({fam(rep.get('H7_rise_unforced'))})"]
    for arm, sp in (rep.get("H7_spread") or {}).items():
        if not sp:
            continue
        th = {k: sp.get(f"thirds_{k}") or {} for k in ("classes", "forced", "unforced")}
        L.append(f"- Reported, {arm} arm: {f(sp.get('units'))} units, {f(sp.get('mean_classes'))} existing classes a "
                 f"unit ({f(sp.get('all_classes'))} with new ones), {f(sp.get('multi'))} in more than one; units with a "
                 f"forced placement {f(sp.get('forced'))}, their classes {f(sp.get('classes_forced'))} against "
                 f"{f(sp.get('classes_not_forced'))}; over the thirds, all "
                 + ", ".join(f(th["classes"].get(k)) for k in ("1", "2", "3")) + "; forced "
                 + ", ".join(f(th["forced"].get(k)) for k in ("1", "2", "3")) + "; unforced "
                 + ", ".join(f(th["unforced"].get(k)) for k in ("1", "2", "3")))
    L.append(f"- Reported, the function arm: forced {ratio(rep.get('H7_function_arm_forced'))}; rise "
             f"{ratio(rep.get('H7_function_arm'))}; function arm / methods arm: {ratio(rep.get('H7_arm'))}")
    L += ["", "### Where the growth of existing classes came from", "",
          "Positions added to classes that existed, by the placement that added them: forced at the class, "
          "with a choice there, or not bound at the class.", ""]
    for arm, g in ((rd or {}).get("growth") or {}).items():
        t = g.get("positions") or {}
        L.append(f"- {arm} arm: {f(t.get('total'))} positions; forced {f(t.get('forced_share'))}, chosen "
                 f"{f(t.get('chosen_share'))}, unbound {f(t.get('unbound_share'))}; forced over the thirds "
                 + ", ".join(f((g.get("thirds") or {}).get(k, {}).get("forced_share")) for k in ("1", "2", "3")))
    ba = (rd or {}).get("growth_by_access") or {}
    if ba:
        L += ["", "By the strictest access of the members the code was bound to at the class: private forces; "
              "package and protected are a looser encapsulation (descriptive).", ""]
        for arm, g in ba.items():
            L.append(f"- {arm} arm: " + ", ".join(f"{k} {f(g.get(k + '_share'))}" for k in
                                                  ("private", "package", "protected", "public", "unbound")
                                                  if g.get(k + "_share") is not None))
    bl = (rd or {}).get("growth_by_lever") or {}
    if bl:
        L += ["", "Within the forced growth, whether the lever of injection was there: bound to the class's "
              "own private state, constants or methods (no lever), or only to injected private fields, which "
              "another class could declare too (the opportunity to duplicate the core; still forced, because "
              "it was not exercised).", ""]
        for arm, g in bl.items():
            L.append(f"- {arm} arm: {f(g.get('forced'))} positions forced ({f(g.get('forced_share_of_growth'))} of "
                     f"the growth, {f(g.get('placements'))} placements); own private members "
                     f"{f(g.get('own_share'))}; injected only {f(g.get('opportunity_share'))} (another class "
                     f"already holds the dependencies {f(g.get('injected_elsewhere_share'))}, none yet "
                     f"{f(g.get('injected_only_here_share'))})")
    L += ["", "### Where coupling between classes came from", "",
          "Calls between classes each unit added (the tree after it less the tree before), over every class.", ""]
    for arm, c in ((rd or {}).get("coupling_added") or {}).items():
        L.append(f"- {arm} arm: {f(c.get('added'))} calls added over {f(c.get('units'))} units; in units with a "
                 f"forced placement {f(c.get('added_forced_units'))} ({f(c.get('share_forced_units'))}), in the others "
                 f"{f(c.get('added_unforced_units'))}; between existing classes changed together "
                 f"{f(c.get('pairs_added'))} ({f(c.get('share_between_pairs'))}), of it in forced units "
                 f"{f(c.get('pairs_added_forced'))} ({f(c.get('share_pairs_forced'))})")
    pc = rep.get("H7_pair_coupling") or {}
    L += ["", "### Pairs of classes changed together", "",
          f"- The coupling of pairs changed together more than once (calls between them before the unit) on "
          f"the index: {ratio(pc)}" + (f" ({f(pc.get('pairs'))} pairs, {f(pc.get('n'))} rows"
                                       + ("" if pc.get("chain_intercept", True) else
                                          "; refitted without the chain's intercept") + ")" if "pairs" in pc else "")]
    for arm, a in ((rd or {}).get("co_change") or {}).items():
        L.append(f"- {arm} arm: {f(a.get('pairs'))} pairs of classes changed together, "
                 f"{f(a.get('again'))} more than once; of those, coupling rose in {f(a.get('rose'))} "
                 f"and fell in {f(a.get('fell'))}")
        for c in a.get("candidates") or []:
            L.append(f"  - candidate for redistribution: `{c['classes'][0]}` and `{c['classes'][1]}` "
                     f"({c['chain_id']}), changed together {c['times']} times, calls between them "
                     f"{c['coupling_first']} → {c['coupling_last']}")
    return L


def h5_section(est: dict, hyp: dict, rep: dict, rd: dict) -> list[str]:
    """H5, surface against volume (PLAN.md §2, §4.2c, §5; restated 24 November 2026)."""
    b = est.get("H5") or {}
    h = hyp.get("H5") or {}
    L = ["", "## H5, surface against volume", "",
         "Per checkpoint, the links it added between blocks of logic (the surface: a method calling a method, "
         "a method using a field that holds state, a function wired to the next), each weighed by the data it "
         "carries (a call 1, +1 per parameter, +1 if it returns a value; a state link 1; a wiring edge 1, +1 if "
         "it carries a value), an injected dependency weighing nothing; against the logic it added (the "
         "volume). The function arm's "
         "ratio half-way through the stream, for the same logic, below 1, **and** its interaction with the "
         "checkpoint index below 1 (the gap widens); one-sided, 95% cluster-bootstrap intervals (chains "
         "resampled).", "",
         f"- **{h.get('verdict', '–')}**" + (f" (p {f(h.get('p'))})" if h.get("p") is not None else ""),
         *([f"- **Read with care: the instrument's calls did not agree well enough with the compiler's "
            f"here** ({'; '.join(rd.get('validation_flags'))}; see the check below)."]
           if (rd or {}).get("validation_flags") else [])]
    if b.get("not_applicable"):
        return L + ["- Not testable on a history: its arms do not solve the same problems."]
    for k, lab in (("arm", "Weighted links added, function arm / methods arm, for the same logic"),
                   ("trend", "The gap over the stream (arm × checkpoint index)")):
        x = b.get(k) or {}
        L.append(f"- **{lab}: {ratio(x)}** (one-sided p {f(x.get('p_less'))}; {x.get('interval', '–')})"
                 + (f"; Wald: {ratio(x['wald'])}" if x.get("wald") else ""))
    uw = rep.get("H5_unweighted") or {}
    L.append(f"- Reported, the links counted, not weighed (the test until 24 November 2026): arm {ratio(uw.get('arm'))}, "
             f"over the stream {ratio(uw.get('trend'))}")
    L.append(f"- Weight added a checkpoint: " + ", ".join(f"{a} {f(v)}" for a, v in (b.get("weight_added") or {}).items())
             + "; links added: " + ", ".join(f"{a} {f(v)}" for a, v in (b.get("links_added") or {}).items())
             + "; logic added: " + ", ".join(f"{a} {f(v)}" for a, v in (b.get("logic_added") or {}).items()))
    for k, x in (rep.get("H5_kinds") or {}).items():
        L.append(f"- Reported, {k} links weighed: function arm / methods arm {ratio(x.get('arm'))}, over the stream "
                 f"{ratio(x.get('trend'))}; a checkpoint " + ", ".join(f"{a} {f(v)}" for a, v in (x.get("mean") or {}).items()))
    wl = rep.get("H5_without_logic") or {}
    L.append(f"- Reported, without the logic in the model: arm {ratio(wl.get('arm'))}, over the stream {ratio(wl.get('trend'))}; "
             f"the methods arm's own rise over the stream {ratio(rep.get('H5_methods_rise'))}; links per e-fold logic "
             f"{ratio(rep.get('H5_logic'))}")
    for arm, a in ((rd or {}).get("links") or {}).items():
        th = a.get("thirds") or {}
        L.append(f"- Reported, {arm}: {f(a.get('checkpoints'))} checkpoints; links added a checkpoint {f(a.get('links_added'))} "
                 f"(call {f(a.get('call_links_added'))}, state {f(a.get('state_links_added'))}, flow "
                 f"{f(a.get('flow_links_added'))}; lost {f(a.get('links_lost'))}); over the thirds "
                 + ", ".join(f(th.get(t)) for t in ("1", "2", "3"))
                 + f"; links per position of logic {f(a.get('links_per_logic'))}; the tree's links per method at the "
                 f"end {f(a.get('tree_links_per_method'))}")
        if a.get("weight_added") is not None:
            L.append(f"  - weighed: {f(a.get('weight_added'))} a checkpoint (call {f(a.get('call_weight_added'))}, state "
                     f"{f(a.get('state_weight_added'))}, flow {f(a.get('flow_weight_added'))}; lost {f(a.get('weight_lost'))}); "
                     f"per position of logic {f(a.get('weight_per_logic'))}; wiring edges whose weight could not "
                     f"be read from the Java (weighed 1) {f(a.get('flow_unresolved_added_total'))} of "
                     f"{f(a.get('flow_links_added_total'))}")
        if a.get("call_links_added_from_functions") is not None:
            ct = a.get("calls_from_methods_thirds") or {}
            L.append(f"  - its call links by caller: from wired functions {f(a.get('call_links_added_from_functions'))}, "
                     f"from other methods {f(a.get('call_links_added_from_methods'))} (over the thirds "
                     + ", ".join(f(ct.get(t)) for t in ("1", "2", "3"))
                     + f"); within the caller's class {f(a.get('call_links_added_within_class'))}, across classes "
                     f"{f(a.get('call_links_added_across_classes'))}")
    return L


def coupling_source_section(rd: dict) -> list[str]:
    """Where forced coupling came from (a reported reading, PLAN.md §4.2c, §9 row 88)."""
    L: list[str] = []
    src = (rd or {}).get("coupling_source") or {}
    if src:
        L += ["", "## Reported: where forced coupling came from", "",
              "Each class a forced change went into: *contained* (no call added across its boundary); "
              "*problem or reuse* (every call it added joins two classes whose private data the change needed, "
              "or reaches a member that was already open); *other* (some call reaches a member the change "
              "opened, in a class whose data it did not need: a utility, as the author reads it). The calls "
              "are counted once each by the same sources.", ""]
        for arm, a in src.items():
            L.append(f"- {arm} arm, forced class rows {f(a.get('rows'))}: contained {f(a.get('contained'))} "
                     f"({f(a.get('contained_share'))}), problem or reuse {f(a.get('explained'))} "
                     f"({f(a.get('explained_share'))}), other {f(a.get('other'))} ({f(a.get('other_share'))})")
            for lab in ("forced", "unforced"):
                c = (a.get("calls") or {}).get(lab)
                if c:
                    L.append(f"  - calls of {lab} changes: problem {f(c.get('problem'))}, reuse "
                             f"{f(c.get('reuse'))}, other {f(c.get('other'))}")
    return L


def reuse_test_lines(e2: dict) -> list[str]:
    """H2's arm contrast (22 November 2026): a core value come back to less in the function arm."""
    L = []
    for lev in ("class", "method"):
        x = e2.get(f"reuse_{lev}") or {}
        if not x:
            continue
        counts = (f"core records: methods arm {f(x.get('methods_records'))} ({f(x.get('methods_uses'))} uses), "
                  f"function arm {f(x.get('function_records'))} ({f(x.get('function_uses'))} uses)")
        if x.get("required"):
            L.append(f"- **A core value come back to, function arm / methods arm, at the {lev}: {ratio(x)}** "
                     f"(needed below 1; one-sided p {f(x.get('p_less'))}; {x.get('interval', '–')}; {counts})")
        else:
            L.append(f"- The arm contrast at the {lev} is not part of the test here: "
                     f"{x.get('note') or x.get('error') or '–'}"
                     + (f" ({counts}; at least {f(x.get('min_records'))} in each needed)" if "records" in x else ""))
    return L


def existing_files_lines(m3: dict, rep: dict) -> list[str]:
    """H4's symmetric count (22 November 2026): how well-trodden the files a change went back into
    were; and, reported, the plain number of them, as first built."""
    L = []
    for x, label, need in ((m3.get("trodden") or {}, "**How well-trodden the files a change went back into were "
                            "(for each existing file it changed, production Java and wiring alike, the earlier "
                            "checkpoints that had changed it), function arm / methods arm: {r}**", True),
                           (rep.get("existing_files") or {}, "Reported, the plain number of existing files gone "
                            "back into (as first built: it counts a change spread over small files as more), "
                            "function arm / methods arm: {r}", False)):
        if not x or x.get("not_applicable"):
            continue
        mean, java, wiring = x.get("mean") or {}, x.get("java") or {}, x.get("wiring") or {}
        L.append("- " + label.format(r=ratio(x))
                 + (f" (needed below 1; one-sided p {f(x.get('p_less'))}; {x.get('interval', '–')})" if need else "")
                 + "; per checkpoint: "
                 + "; ".join(f"{a} {f(v)} (Java {f(java.get(a))}, wiring {f(wiring.get(a))})" for a, v in mean.items()))
    return L


def split_section(rep: dict, rd: dict) -> list[str]:
    """Logic and organisation (PLAN.md §4.9)."""
    s, m = rd.get("split") or {}, rep.get("split") or {}
    if not s:
        return []
    names = [("logic_added", "logic", "Logic (body positions)"),
             ("organisation_added", "organisation_in_bodies", "Organisation in bodies (positions)"),
             ("declaration_lines_added", "declarations", "Declarations (lines outside bodies)"),
             ("wiring_lines_added", None, "Wiring (lines)"),
             ("organisation_all", "organisation_all", "Organisation in all (bodies, declarations, wiring)"),
             ("import_lines_added", "imports", "Imports (lines)"),
             ("logic_existing_methods", "logic_existing_methods", "Where logic landed: methods that existed"),
             ("logic_new_called_methods", "logic_new_called_methods", "Where logic landed: new called methods"),
             ("logic_new_wired_functions", "logic_new_wired_functions", "Where logic landed: new wired functions"),
             ("existing_methods_edited", "existing_methods_edited", "Existing methods a checkpoint added logic to"),
             ("new_wired_functions", "new_wired_functions", "New wired functions"),
             ("new_called_methods", "new_called_methods", "New called methods with logic (not wired functions)"),
             ("params_called_methods", "params_called_methods", "Handed along: parameters of new called methods"),
             ("params_wired_functions", "params_wired_functions", "Declared: injected parameters of new wired functions"),
             ("params_new_methods", "params_new_methods", "Parameters of all new methods (as first built)"),
             ("birth_binding", "birth_binding", "Handed along: values callers pass new methods"),
             ("method_values_added", "method_values_added", "Introduced: parameters and locals"),
             ("fields_added", "fields_added", "Introduced: fields left in existing classes")]
    arms = list(s)
    L = ["", "## Reported: logic and organisation", "",
         "What a checkpoint added, per checkpoint: its logic (the statements of method bodies), and the "
         "organisation that supplies the logic with its data: accessors and constructor wiring in bodies, "
         "declarations outside them (signatures, fields, class headers, annotations), and the wiring; with the "
         "state it handed along. Stated before any run was read: the logic is the same in both arms (the ratio "
         "inside 0.8 to 1.25), and the state handed along (the parameters of new called methods, the values "
         "callers pass new methods) is lower in the function arm (below 1) and flatter over the stream (the "
         "trend below 1). Declarations, wiring and the injected parameters of wired functions are reported as "
         "they fall.", "",
         "| Part | " + " | ".join(f"{a}, per checkpoint (thirds)" for a in arms)
         + " | Function arm / methods arm (90%) | Its trend over the stream (95%) |",
         "|---|" + "---|" * (len(arms) + 2)]
    for key, model, label in names:
        cells = []
        for a in arms:
            th = s[a].get("thirds") or {}
            cells.append(f"{f(s[a]['per_checkpoint'].get(key))} ("
                         + ", ".join(f((th.get(t) or {}).get(key)) for t in ("1", "2", "3")) + ")")
        x = m.get(model) or {} if model else {}
        fitted = bool(x) and "error" not in x
        L.append(f"| {label} | " + " | ".join(cells) + f" | {ratio(x) if fitted else '–'} | "
                 f"{ratio(x.get('trend')) if fitted else '–'} |")
    L.append("")
    lg = m.get("logic") or {}
    L.append(f"- Logic the same in both arms (two one-sided tests against 0.8 and 1.25): p {f(lg.get('p_tost'))}")
    for a in arms:
        L.append(f"- {a}: organisation's share of logic and organisation together "
                 f"{f(s[a].get('organisation_share'))} ({f(s[a].get('checkpoints'))} checkpoints)")
    return L


def validation_section(rd: dict) -> list[str]:
    """The instrument against the compiler (PLAN.md §4.8)."""
    v = rd.get("validation") or {}
    if not v:
        return []
    L = ["", "## Reported: the instrument against the compiler", "",
         "The instrument resolves names without a symbol solver. On a sample of each chain's checkpoints "
         "(every fifth and the last) the tree was given to javac, which does resolve them. Precision: of what "
         "the instrument read, the share the compiler confirms. Recall: of what the compiler read that could "
         "be followed, the share the instrument has. What the compiler itself could not resolve is counted "
         "apart and held against neither.", "",
         "| Arm | Checkpoints (chains) | Calls: precision, recall | Calls leaving the class: precision, recall | "
         "Field reads: precision, recall | Bound names confirmed: method values, fields, class methods |",
         "|---|---|---|---|---|---|"]
    for arm, a in v.items():
        L.append(f"| {arm} | {f(a.get('checkpoints'))} ({f(a.get('chains'))}) | "
                 f"{f(a.get('calls_precision'))}, {f(a.get('calls_recall'))} (of {f(a.get('calls'))} and "
                 f"{f(a.get('calls_compiler'))}) | {f(a.get('cross_precision'))}, {f(a.get('cross_recall'))} "
                 f"(of {f(a.get('cross_calls'))} and {f(a.get('cross_compiler'))}) | "
                 f"{f(a.get('reads_precision'))}, {f(a.get('reads_recall'))} (of {f(a.get('reads'))} and "
                 f"{f(a.get('reads_compiler'))}) | {f(a.get('names_method_precision'))} of "
                 f"{f(a.get('names_method'))}, {f(a.get('names_field_precision'))} of {f(a.get('names_field'))}, "
                 f"{f(a.get('names_class_method_precision'))} of {f(a.get('names_class_method'))} |")
    tripped = rd.get("validation_flags") or []
    L.append("")
    L.append("- **Read the calls with care (H1's flow at the method, H7's coupling, H5):** " + "; ".join(tripped) + "."
             if tripped else
             f"- The tripwire is not set off: every share of calls is at least {validate.LOW:.2f} in each arm, "
             f"and none differs between the arms by more than {validate.GAP:.2f}.")
    for arm, a in v.items():
        L.append(f"- {arm}: methods matched between the two {f(a.get('methods_matched_share'))}, hosts "
                 f"{f(a.get('hosts_matched_share'))}; strict precision (a call confirmed only on the compiler's "
                 f"class, its ancestors and descendants, not its siblings): calls {f(a.get('calls_strict_precision'))}, "
                 f"calls leaving the class {f(a.get('cross_strict_precision'))}; the instrument's calls the compiler left unresolved "
                 f"(unverified) {f(a.get('calls_unverified'))}; the compiler's calls to an application method's "
                 f"name it could not resolve {f(a.get('calls_unresolved'))}; its calls to a method with no body "
                 f"in the tree (an interface's) {f(a.get('calls_no_body'))}; checkpoints read with the project's "
                 f"libraries on the classpath {f(a.get('with_classpath'))} of {f(a.get('checkpoints'))}")
    return L


def h8_section(est: dict, hyp: dict, cond: dict) -> list[str]:
    """H8, without encapsulation code disperses: Run D against Run A's same stack (PLAN.md §3.1a)."""
    h = hyp.get("H8")
    if not h:
        return []
    d = h.get("detail") or {}
    comp = cond.get("compliance") or {}
    amt = cond.get("amount") or {}
    return ["", "## H8, without encapsulation code disperses (Run D against Run A)", "",
            "The same stack, stream and agent, with the agent told to leave every field and method public. "
            "Both parts are needed: its bound code is come back to less at the class (below 1), and its "
            "changes add more calls and field reads across class boundaries at the same change size (above "
            "1); 95% cluster-bootstrap intervals. Run D was run after Run A, not beside it, so anything "
            "that changed between the two runs is in the contrast (PLAN.md §7).", "",
            f"- **{h.get('verdict', '–')}** (p {f(h.get('p'))})",
            f"- Compliance, the members its units introduced that are not private: {f(comp.get('share'))} "
            f"of {f(comp.get('introduced'))} (at least {f(h.get('compliance_bar'))} needed)",
            f"- **Later intrusion at the class, open / encapsulated: {ratio(d.get('intrusion_class'))}**",
            f"- **Calls and field reads added across class boundaries, open / encapsulated: {ratio(d.get('coupled'))}**",
            f"- Amount added, open / encapsulated: {f(amt.get('ratio'))} (in band: {f(amt.get('in_band'))})"]


def redesign_section(rd: dict) -> list[str]:
    """The redesign reading (PLAN.md §4.2d): where the code stands between the two forces."""
    L = ["", "## Reported: split or concentrate (redesign reading)", "",
         "*Split:* a class whose forced changes fall into groups sharing none of its values. *Concentrate:* "
         "a pair changed together at least three times over the same data, its coupling rising.", ""]
    for arm, a in ((rd or {}).get("redesign") or {}).items():
        sp, co = a.get("split") or {}, a.get("concentrate") or {}
        L.append(f"- {arm} arm, split: {f(sp.get('classes'))} classes with two or more forced changes; flagged "
                 f"{f(sp.get('flagged'))}, of which {f(sp.get('disjoint_partners'))} with groups changed with "
                 f"different classes")
        for c in sp.get("candidates") or []:
            L.append(f"  - `{c['class']}` ({c['chain_id']}, at {c['at']}): groups "
                     + " | ".join(", ".join(g) for g in c["groups"])
                     + f"; changed with different classes: {f(c['disjoint_partners'])}")
        L.append(f"- {arm} arm, concentrate: {f(co.get('pairs'))} pairs changed together, "
                 f"{f(co.get('together'))} at least three times; flagged {f(co.get('flagged'))}")
        for c in co.get("candidates") or []:
            L.append(f"  - `{c['classes'][0]}` and `{c['classes'][1]}` ({c['chain_id']}): changed together "
                     f"{c['times']} times, the same data {f(c['same_data'])}")
    return L


def surface_section(rep: dict, rd: dict) -> list[str]:
    """Surface against volume and ripple (PLAN.md §4.2e): the exchange between the two outlets."""
    L = ["", "## Reported: surface against volume, and ripple", "",
         "A class's surface (calls out and in) against its volume (methods). The exponent below 1: surface grows "
         "slower than volume, so concentrating saves communication; above 1: faster. Ripple: of the later changes "
         "to a method a unit's new call reached, the share that also changed the calling class.", ""]
    for arm, r in (rep.get("surface") or {}).items():
        a, w, fo = r.get("across") or {}, r.get("within") or {}, r.get("added_forced") or {}
        pc = r.get("per_change") or {}
        L.append(f"- {arm} arm: exponent across the classes of the last tree {interval(a)}"
                 + (f" ({f(a.get('classes'))} classes)" if "classes" in a else "")
                 + f"; within a class as it grows {interval(w)}"
                 + (f" ({f(w.get('classes'))} classes, {f(w.get('rows'))} changes)" if "rows" in w else ""))
        L.append(f"  - surface a change added, forced against unforced at the same methods added: {interval(fo)}; "
                 + "; ".join(f"{k} {f((pc.get(k) or {}).get('surface_added'))} calls for "
                             f"{f((pc.get(k) or {}).get('methods_added'))} methods" for k in ("forced", "unforced")))
    for arm, groups in ((rd or {}).get("ripple") or {}).items():
        for k in ("forced_opened", "forced_existing", "unforced_opened", "unforced_existing"):
            g = groups.get(k)
            if not g:
                continue
            L.append(f"- Ripple, {arm} arm, {k.replace('_', ', ')}: {f(g.get('calls'))} new calls; "
                     f"{f(g.get('calls_changed_later'))} reach a method changed later, {f(g.get('later_changes'))} "
                     f"later changes, {f(g.get('rippled'))} of them changing the caller too ({f(g.get('ripple_rate'))}; "
                     f"by chance {f(g.get('chance_rate'))}; ratio {f(g.get('ripple_ratio'))})")
    return L


def containers_section(rd: dict) -> list[str]:
    """A filled ball or pebbles (PLAN.md §4.2g, a reported reading, no direction stated)."""
    data = (rd or {}).get("containers") or {}
    if not data:
        return []
    L = ["", "## Reported: a filled ball or pebbles", "",
         "Each class (and, in the function arm, each wiring flow file) as a container of blocks of logic "
         "(methods). At each chain's last checkpoint: blocks, volume a block, the largest block's share and "
         "internal links a block. The growth exponent: within a container over the stream, log(blocks) on "
         "log(volume); near 1 it grows by adding blocks (pebbles), near 0 by swelling the blocks it has (a "
         "filled ball); 95% interval over containers resampled.", ""]
    for arm, kinds in data.items():
        for kind, groups in kinds.items():
            for g in ("concentrations", "rest", "all"):
                x = groups.get(g) or {}
                if not x.get("containers_at_end") and not x.get("growing_containers"):
                    continue
                iv = x.get("interval") or [None, None]
                L.append(f"- {arm}, {kind}, {g}: {f(x.get('containers_at_end'))} at the end; blocks "
                         f"{f(x.get('blocks'))}, volume a block {f(x.get('block_size'))}, largest block "
                         f"{f(x.get('largest_share'))}, internal links a block {f(x.get('internal_links_per_block'))}; "
                         f"growth exponent {f(x.get('growth_exponent'))} [{f(iv[0])}, {f(iv[1])}] "
                         f"({f(x.get('growing_containers'))} containers that grew)")
    return L


def reader_section(rep: dict, rd: dict) -> list[str]:
    """Encapsulation and the reader (PLAN.md §4.2f): the four measures per author group (arm) and size
    band, and on a history the models of the author against system size."""
    L = ["", "## Reported: encapsulation and the reader", "",
         "Whether encapsulation answers a reader's limit: per author group (on a history, declared agent "
         "commits against people), the private share of the members a unit introduces, the share of growth "
         "of existing classes arriving forced, the members opened per class row changed, and the methods of "
         "the classes code lands in; by the system's size in tokens against a context window (below 200k, "
         "200k to 1M, above 1M). Predicted (the author's question): agents make fewer private, open more and "
         "let classes grow larger where the system fits in a window, the difference narrowing where it "
         "does not.", ""]
    for arm, bands in ((rd or {}).get("reader") or {}).items():
        for b, x in bands.items():
            L.append(f"- {arm}, {b}: {f(x.get('units'))} units in {f(x.get('repositories'))} repositories"
                     + (" (too thin)" if x.get("too_thin") and b != "all" else "")
                     + f"; private share {f(x.get('private_share'))} of {f(x.get('introduced'))} introduced; "
                     f"forced share {f(x.get('forced_share'))}; opened per class row {f(x.get('opened_per_row'))} "
                     f"({f(x.get('class_rows'))} rows); class methods mean {f(x.get('class_methods_mean'))}, "
                     f"median {f(x.get('class_methods_median'))}; splits per unit {f(x.get('splits_per_unit'))}; "
                     f"median tokens {f(x.get('tokens_median'))}")
    m = rep.get("reader") or {}
    if m:
        L.append(f"- Models (the author contrast at {f(m.get('centre_tokens'))} tokens, and its change per "
                 "e-fold larger system):")
        for k, label in (("private", "private share (odds ratio)"), ("forced", "forced share (odds ratio)"),
                         ("opened", "members opened (rate ratio)"), ("class_methods", "class methods (rate ratio)")):
            x = m.get(k) or {}
            if "error" in x:
                L.append(f"  - {label}: not fitted ({x['error']})")
                continue
            L.append(f"  - {label}: author {ratio(x.get('author'))}; × size {ratio(x.get('interaction'))}; "
                     f"size {ratio(x.get('size'))} (n = {f(x.get('n'))}, {f(x.get('repositories'))} repositories)")
    return L


def bystander_lines(r: dict) -> list[str]:
    """The description beside H3: needed values and bystanders per run, per arm (PLAN.md §4.3a)."""
    L = []
    for arm, x in (r.get("bystanders") or {}).items():
        L.append(f"- Reported, {arm}: {f(x.get('pulled'))} of {f(x.get('runs'))} runs need a pre-existing "
                 f"value ({f(x.get('share_free'))} free); per such run, needed {f(x.get('need'))}, bystanders "
                 f"{f(x.get('bystanders'))} (method {f(x.get('by_method'))}, class {f(x.get('by_class'))}; "
                 f"without constants {f(x.get('without_constants'))}); over the thirds of the stream "
                 + ", ".join(f(t) for t in x.get("thirds") or []) + f"; fields left behind per addition "
                 f"{f(x.get('fields_added_per_addition'))}"
                 + (f"; method values introduced per addition {f(x.get('method_values_added_per_addition'))}"
                    if x.get("method_values_added_per_addition") is not None else ""))
    return L


def drawn_lines(r: dict) -> list[str]:
    """The description beside H2: what stood by where bound code was placed, and how much of the
    later intrusion there is bound to it, per arm (PLAN.md §4.4)."""
    L = []
    for arm, x in (r.get("drawn") or {}).items():
        if not x.get("rows"):
            continue
        c, m = x["class"], x["method"]
        L.append(f"- Reported, {arm}: {f(x['rows'])} bound rows; at the class {f(c['bystanders'])} fields "
                 f"stood by, {f(c['drawn'])} of {f(c['later'])} later intrusions bound to one of them "
                 f"({f(c['share'])}); at the method {f(m['bystanders'])} values stood by, {f(m['drawn'])} of "
                 f"{f(m['later'])} ({f(m['share'])})")
        if "introduced" in c:
            L.append(f"- Reported, {arm}, introduced there by the change: at the class {f(c['introduced'])} "
                     f"fields, {f(c['drawn_introduced'])} of {f(c['later'])} later intrusions bound to one of "
                     f"them ({f(c['share_introduced'])}), to one that stood by or was introduced "
                     f"{f(c['drawn_left'])} ({f(c['share_left'])}); at the method {f(m['introduced'])} values, "
                     f"{f(m['drawn_introduced'])} of {f(m['later'])} ({f(m['share_introduced'])}), to either "
                     f"{f(m['drawn_left'])} ({f(m['share_left'])})")
    return L


def reuse_lines(r: dict) -> list[str]:
    """Beside H4: uses of core and periphery values per 100 values and later checkpoints, per arm."""
    L = []
    for arm, x in (r.get("core_reuse") or {}).items():
        parts = []
        for lev in ("class", "method"):
            c, p = x.get(f"core_{lev}"), x.get(f"periphery_{lev}")
            if c and p:
                parts.append(f"at the {lev} core {f(c['per_100'])} ({f(c['uses'])} uses of {f(c['values'])} "
                             f"values in {f(c['records'])} rows), periphery {f(p['per_100'])}")
        if parts:
            L.append(f"- Reported, {arm}, uses per 100 values and later checkpoints: " + "; ".join(parts))
    return L


def h9_section(est: dict, hyp: dict, rep: dict, rd: dict) -> list[str]:
    """H9, the cost to fix a concentration (PLAN.md §2, §4.2h, §5; secondary)."""
    b = est.get("H9") or {}
    h = hyp.get("H9") or {}
    L = ["", "## H9, the cost to fix a concentration (secondary)", "",
         "Each class with two or more blocks at the end of the stream: its cheapest split, the fewest internal "
         "links (calls between its blocks, blocks sharing a field that holds state) a cut must cross to divide "
         "it into two parts of at least a quarter of its code each. The function arm's rate at the same size "
         "below 1, **and** the gap widening as classes grow (arm × size below 1); one-sided, 95% "
         "cluster-bootstrap intervals.", "",
         f"- **{h.get('verdict', '–')}**" + (f" (p {f(h.get('p'))})" if h.get("p") is not None else "")]
    if b.get("not_applicable"):
        return L + ["- Not testable on a history: its arms do not solve the same problems."]
    if b.get("error"):
        return L + [f"- Not estimated ({b['error']})"]
    for k, lab in (("arm", "Cheapest split, function arm / methods arm, at the same size"),
                   ("size", "The gap as classes grow (arm × log size)")):
        x = b.get(k) or {}
        L.append(f"- **{lab}: {ratio(x)}** (one-sided p {f(x.get('p_less'))}; {x.get('interval', '–')}; "
                 f"{b.get('family', '–')})")
    L.append("- Classes: " + ", ".join(f"{a} {f(v)}" for a, v in (b.get("classes") or {}).items())
             + "; mean cheapest split: " + ", ".join(f"{a} {f(v)}" for a, v in (b.get("mean") or {}).items()))
    c, k = rep.get("H9_concentrations") or {}, rep.get("H9_by_blocks") or {}
    L.append(f"- Reported, the concentrations alone ({f(c.get('n'))} classes): arm {ratio(c.get('arm'))}, with size "
             f"{ratio(c.get('size'))}; on the blocks instead of the volume: arm {ratio(k.get('arm'))}, with size "
             f"{ratio(k.get('size'))}")
    for arm, a in ((rd or {}).get("h9") or {}).items():
        L.append(f"- Reported, {arm}: classes of two or more blocks that no split leaves a quarter on each side "
                 f"(one block holds most of the class), left out: {f(a.get('not_splittable'))}")
        for g in ("concentrations", "rest"):
            x = a.get(g) or {}
            if not x.get("classes"):
                continue
            th = x.get("thirds") or {}
            L.append(f"- Reported, {arm}, {g}: {f(x['classes'])} classes at the end, {f(x.get('blocks'))} blocks, "
                     f"cheapest split {f(x.get('split_cost'))} ({f(x.get('cost_per_block'))} a block; over the thirds "
                     + ", ".join(f(th.get(t)) for t in ("1", "2", "3"))
                     + f"); already in separate pieces {f(x.get('zero_share'))}; found exactly {f(x.get('exact_share'))}")
    return L


def sinew_lines(r: dict) -> list[str]:
    """Beside H2: the sinew shape (PLAN.md §5, 25 November 2026), how a place's bound uses fall on
    its values and their combinations, and the effective number of values they fall on."""
    L = []
    for arm, x in (r.get("sinew_shape") or {}).items():
        for lev in ("class", "method"):
            s = x.get(lev) or {}
            if not s.get("places"):
                continue
            th = s.get("effective_number_thirds") or {}
            L.append(f"- Reported, {arm}, the sinew shape at the {lev}: {f(s['places'])} places, {f(s['uses'])} uses; "
                     f"effective number of values {f(s['effective_number'])} (over the thirds "
                     + ", ".join(f(th.get(t)) for t in ("1", "2", "3"))
                     + f"); the most used value's share {f(s['top_value_share'])}; changes repeating a combination "
                     f"already used there {f(s['repeated_combination_share'])} of {f(s['changes'])}")
            if s.get("top_values"):
                L.append("  - most used values: " + "; ".join(
                    f"`{v['place']}` {v['value']} {v['uses']}" for v in s["top_values"]))
            if s.get("top_combinations"):
                L.append("  - most used combinations: " + "; ".join(
                    f"`{c['place']}` {{{', '.join(c['values'])}}} {c['uses']}" for c in s["top_combinations"]))
    return L


def core_lines(r: dict) -> list[str]:
    """The description beside H2: how the bound uses of a place's values are spread over them, and
    how many of the values the changes introduced are used again (PLAN.md §5)."""
    L = []
    for arm, x in (r.get("core") or {}).items():
        c, m = x["class"], x["method"]
        L.append(f"- Reported, {arm}, how bound uses are spread: at the class {f(c['uses'])} uses of "
                 f"{f(c['values_used'])} fields, {f(c['top3_share'])} to a chain's three most used, "
                 f"{f(c['from_start'])} to fields no checkpoint introduced; of {f(c['introduced'])} fields "
                 f"introduced, {f(c['promoted'])} used by later bound code ({f(c['promoted_share'])}); at the "
                 f"method {f(m['uses'])} uses of {f(m['values_used'])} values, {f(m['top3_share'])} to the "
                 f"three most used, {f(m['from_start'])} to values no checkpoint introduced; of "
                 f"{f(m['introduced'])} introduced, {f(m['promoted'])} used later ({f(m['promoted_share'])})")
    return L


def landing_section(r: dict) -> list[str]:
    """Where bound and unbound code lands among the places it could have gone (PLAN.md §5)."""
    data = r.get("landings") or {}
    if not data:
        return []
    L = ["", "## Reported: where bound and unbound code lands", "",
         "A rank is the place's standing among every candidate of its checkpoint (0.5: no regard to "
         "that size; near 1: the largest). Method ranks are over landings into existing methods, class "
         "ranks over landings into existing classes.", "",
         "| Arm | Code | Landings | Existing method | New method | New class | Method: complexity | "
         "Method: data width | Class: complexity | Class: fields | Agreement (method) | Agreement (class) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for arm, both in data.items():
        for label, x in both.items():
            L.append(f"| {arm} | {label} | {f(x.get('landings'))} | {f(x.get('existing method'))} | "
                     f"{f(x.get('new method'))} | {f(x.get('new class'))} | "
                     f"{f(x.get('rank_cognitive'))} (n {f(x.get('n_rank_cognitive'))}) | {f(x.get('rank_width'))} | "
                     f"{f(x.get('rank_class_cognitive'))} (n {f(x.get('n_rank_class_cognitive'))}) | "
                     f"{f(x.get('rank_class_fields'))} | {f(x.get('agreement_method'))} | "
                     f"{f(x.get('agreement_class'))} |")
    odds = (r.get("_estimates") or {}).get("unbound_enters_existing_class")
    if odds:
        L += ["", f"Unbound code entering a class that existed, function arm against methods arm, odds ratio: "
              f"{ratio(odds)} (shares {odds.get('share')})."]
    L += ["", "Agreement is Spearman's rho, over the places landed in, of the complexity rank with the "
          "data-width rank: whether the two kinds of size point to the same places."]
    return L


def literature_section(est: dict, spec: dict) -> list[str]:
    """The literature's shape measures, each alone, at the method and at the class (PLAN.md §4.7a)."""
    lit = (est.get("reported") or {}).get("literature_shape") or {}
    counts = spec.get("literature_counts") or {}
    left = [k for k in counts if k not in lit]
    if not lit and not left:
        return []
    L = ["", "## Reported: the literature's shape measures, each alone", "",
         "Later intrusion per standard deviation of the measure (a flag: present against absent), with the "
         "problem, the bindings and what stood by held fixed. Method measures on intrusion at the method, "
         "class measures on intrusion at the class, one row per class a checkpoint's bound code went into "
         f"({f(((est.get('reported') or {}).get('literature_class_rows')))} rows), with the class's size held "
         "fixed and an intercept for the class (\u2020: refitted without it). Read as H6 is: below 1.25 does "
         "not draw code in. A measure marked reversed is one where higher is better; its ratio is for the "
         "worse shape.", "",
         "| Measure | Level | Source | n | Rate ratio (90% interval) | One-sided p | Against 1.25 |",
         "|---|---|---|---|---|---|---|"]
    for k, m in lit.items():
        if "error" not in m and None in (m.get("irr_lower"), m.get("irr_upper")):
            m = {**m, "error": "no finite interval"}
        if "error" in m:
            L.append(f"| {k} | {m.get('at', '–')} | {m.get('source', '–')} | – | not estimated ({m['error']}) | – | – |")
            continue
        where = "above" if m.get("above") else "below" if m["irr_upper"] <= 1.25 else "reaches above"
        name = k + (" (reversed)" if m.get("reversed") else "") + (
            " \u2020" if m.get("at") == "class" and not m.get("class_intercept") else "")
        L.append(f"| {name} | {m.get('at')} | {m.get('source')} | {f(m.get('n'))} | {ratio(m)} | "
                 f"{f(m.get('p_upper'))} | {where} |")
    at_class = spec.get("class_level") or {}
    if at_class and not at_class.get("testable"):
        L += ["", f"**Read the class rows with care.** Later arrivals fall in "
              f"{f(at_class.get('classes_with_arrivals'))} distinct classes here, and the busiest holds "
              f"{f(at_class.get('top_class_share'))} of them. A class measure then mostly describes that one "
              f"class as it changes over the stream, so an association with later arrivals may be "
              f"coincidental. These rows are not part of H6 in this analysis."]
    if left:
        L += ["", "Left out by the variation rule (bound rows flagged or above zero, per arm): "
              + ", ".join(f"{k} ({counts[k]})" for k in left) + "."]
    return L


def readings_section(est: dict, r: dict) -> list[str]:
    """Choice at a checkpoint, formation and review (PLAN.md §5): reported, not confirmatory."""
    rep = est.get("reported") or {}
    L = ["", "## Reported readings: choice, formation, review", ""]
    for arm, c in (r.get("choice") or {}).items():
        L.append(f"- Choice, {arm}: {f(c.get('no_choice'))} of {f(c.get('checkpoints'))} checkpoints "
                 f"left no choice (every chain with the same bindings, on the same side of new or existing); "
                 f"median spread of bindings over chains {f(c.get('median_binding_sd'))}, median distinct hosts "
                 f"{f(c.get('median_distinct_hosts'))}")
    for arm in sorted(k[len("formation_lagged_"):] for k in rep if k.startswith("formation_lagged_")):
        L.append(f"- Formation, lagged, {arm}: bindings now on the chain's mean bindings so far "
                 f"{interval(rep['formation_lagged_' + arm])} (predicted above 0 in the methods arm)")
    for arm in sorted(k[len("capture_"):] for k in rep if k.startswith("capture_")):
        L.append(f"- Capture, {arm}: share of the addition landing in existing hosts on the fields held "
                 f"by the chain's heaviest class {interval(rep['capture_' + arm])} (predicted above 0 in "
                 f"the methods arm)")
    for lev in ("class", "method"):
        x = rep.get("size_or_data_" + lev)
        if x:
            cor = ", ".join(f"{k} {f(v)}" for k, v in (x.get("correlation") or {}).items())
            L.append(f"- Size or data, at the {lev} (both arms pooled, no arm term, n = {f(x.get('n'))}): later "
                     f"intrusion per value that stood by, size held fixed, {ratio(x.get('bystanders'))} (predicted "
                     f"above 1); per log of size, with what stood by held fixed, {ratio(x.get('size'))}; size alone "
                     f"{ratio(x.get('size_alone'))}; within arms, bystanders {ratio(x.get('bystanders_within_arms'))} "
                     f"and size {ratio(x.get('size_within_arms'))}; Spearman's rho of size with what stood by: {cor}")
    for arm, x in (r.get("formation_end") or {}).items():
        L.append(f"- Formation, where it ends, {arm}: Spearman's rho of early bindings with the largest "
                 f"method's share {f(x.get('rho'))} {x.get('interval') or '[no interval]'} over "
                 f"{f(x.get('chains'))} chains (predicted above 0 in the methods arm)")
    rv = r.get("review")
    for arm, x in ((rv or {}).items()):
        if isinstance(x, dict):
            L.append(f"- Review against {rv['against']}, {arm}: Spearman's rho of bindings with the change "
                     f"in placement {f(x.get('rho'))} {x.get('interval') or '[no interval]'} over "
                     f"{f(x.get('checkpoints'))} checkpoints (predicted below 0), against: {f(x.get('against'))}")
    for arm, x in (r.get("own_lines") or {}).items():
        if x.get("lines"):
            L.append(f"- Own lines followed, {arm}: {f(int(x['lines']))} placed, {f(int(x['lost']))} "
                     f"lost track of ({100 * x['lost'] / x['lines']:.1f}%)")
    return L if len(L) > 3 else []


def render(name: str, role: str, est: dict, ver: dict, cond: dict, spec: dict,
           heads: list[dict], drift: dict | None = None, readings: dict | None = None) -> str:
    hyp = ver["hypotheses"]
    rep = est.get("reported") or {}
    L = [f"# {name}", "",
         f"Role: **{role}**. Chains: " + ", ".join(f"{k} {v}" for k, v in cond["chains"].items())
         + (". **Descriptive only.**" if ver["descriptive_only"] else "."), "",
         "| Hypothesis | Tier | Verdict | p (Holm over the confirmatory; own p for secondary) |",
         "|---|---|---|---|"]
    for k, v in hyp.items():
        L.append(f"| {k} | {v.get('tier', '–')} | {v['verdict']} | {f(v.get('p_holm'))} |")
    # the inline sections below are built in the order they were written and put in the story's
    # order (H1 to H8, PLAN.md 9 row 93) at the end
    seg = {"H3": len(L)}
    h3 = est.get("H3") or {}
    lv = rep.get("H3_levels") or {}
    t1 = rep.get("H3_bindings") or {}
    L += ["", "## H3, the encapsulation fills (methods arm)", "",
          f"Runs that need a pre-existing value {f(h3.get('n_runs'))} over {f(h3.get('n_chains'))} "
          f"chains; the slope of log(1 + bystanders) on the checkpoint index, cluster-bootstrap 95% interval "
          f"({est.get('boot')} refits).", "",
          f"- **Bystanders on the checkpoint index: {interval(h3.get('cp'))}**",
          f"- **Within a class, the class's bystanders: {interval(h3.get('within_class'))}** "
          f"({f((h3.get('within_class') or {}).get('places'))} classes with runs at two or more checkpoints)",
          f"- **Within a method, the method's bystanders: {interval(h3.get('within_method'))}** "
          f"({f((h3.get('within_method') or {}).get('places'))} methods)",
          f"- Reported, within a place in the function arm: class "
          f"{interval((rep.get('H3_within_function_arm') or {}).get('class'))}; method "
          f"{interval((rep.get('H3_within_function_arm') or {}).get('method'))}",
          f"- Reported, method bystanders {interval(lv.get('method'))}; class bystanders "
          f"{interval(lv.get('class'))}",
          f"- Reported, without injected dependencies {interval(lv.get('without_injected'))}; without "
          f"constants {interval(lv.get('without_constants'))}",
          f"- Reported, the function arm's slope: {interval(lv.get('function_arm'))}",
          *bystander_lines(readings or {}),
          f"- Reported, H3 as first registered (bindings of runs into existing methods): on log(host "
          f"positions) {interval(t1.get('log_host'))}; on the checkpoint index {interval(t1.get('cp'))}",
          f"- Reported, bindings in the function arm: on host size {interval((rep.get('H3_function_arm') or {}).get('log_host'))}",
          f"- Reported, bindings at class level (methods arm): on class size {interval((rep.get('H3_class_level') or {}).get('log_class'))}",
          f"- Reported, bindings without injected dependencies: on host size {interval((rep.get('H3_without_injected') or {}).get('log_host'))}; "
          f"class level on class size {interval((rep.get('H3_class_level_without_injected') or {}).get('log_class'))}"]
    seg["H2"] = len(L)
    e2 = est.get("H2") or {}
    rows_ = rep.get("intrusion_rows") or {}
    L += ["", "## H2, a core draws code in (methods arm)", "",
          f"Where code was bound to a class or a method ({f(rows_.get('bound'))} of {f(rows_.get('all'))} "
          f"problem and host rows, both arms; {f(e2.get('n'))} in the methods arm): the later intrusions' "
          f"uses of the values that code was bound to (the core) against their uses of the rest the "
          f"place held, what stood by and what the change introduced (the periphery), as a rate ratio "
          f"per value. A later change counts each value once in each method its bound code is in.", "",
          f"- **At the class (the private members the code was bound to): {ratio(e2.get('class'))}**"
          f" ({(e2.get('class') or {}).get('interval', '–')}; Wald: {ratio((e2.get('class') or {}).get('wald'))})",
          f"- **At the method (its values): {ratio(e2.get('method'))}**"
          f" ({(e2.get('method') or {}).get('interval', '–')}; Wald: {ratio((e2.get('method') or {}).get('wald'))})",
          *reuse_test_lines(e2),
          f"- Reported, the function arm: class {ratio(rep.get('H2_core_function_arm_class'))}; method "
          f"{ratio(rep.get('H2_core_function_arm_method'))}",
          *core_lines(readings or {}),
          *sinew_lines(readings or {}),
          f"- Reported, at the class on its fields only (as until 19 November 2026): "
          f"{ratio(rep.get('H2_class_fields'))}",
          f"- Reported, at the class with every member the code was bound to as the core, private or not "
          f"(as until 22 November 2026): {ratio(rep.get('H2_class_all'))}",
          *width_lines(rep),
          f"- Reported, H2 as it stood until 19 November 2026 (later intrusions bound to what stood by, per "
          f"value that stood by): class {ratio(rep.get('H2_bystanders_class'))}; method "
          f"{ratio(rep.get('H2_bystanders_method'))}",
          *drawn_lines(readings or {}),
          f"- Reported, on log(1 + bystanders): class {interval(rep.get('H2_log_class'))}; method "
          f"{interval(rep.get('H2_log_method'))}",
          f"- Reported, per value that stood by, the function arm: class {ratio(rep.get('H2_function_arm_class'))}; method "
          f"{ratio(rep.get('H2_function_arm_method'))}",
          f"- Reported, with what the change introduced counted beside what stood by (later intrusions "
          f"bound to either, per value of both): class {ratio(rep.get('H2_left_class'))}; method "
          f"{ratio(rep.get('H2_left_method'))}; in the function arm, class "
          f"{ratio(rep.get('H2_left_function_arm_class'))}; method {ratio(rep.get('H2_left_function_arm_method'))}",
          f"- Reported, H2 as it stood until 17 November 2026 (later intrusion per binding): class "
          f"{ratio(rep.get('bindings_intrusion_class'))}; method {ratio(rep.get('bindings_intrusion_method'))}",
          f"- For information, the same on the problem's own lines: {ratio(rep.get('bindings_lines'))}",
          f"- Reported, per binding, any later change, bound or not: class {ratio(rep.get('bindings_any_change_class'))}; "
          f"method {ratio(rep.get('bindings_any_change_method'))}",
          f"- Reported, per binding, existing hosts only: class {ratio(rep.get('bindings_existing_hosts_class'))}; method "
          f"{ratio(rep.get('bindings_existing_hosts_method'))}",
          f"- Reported, per binding, without injected dependencies: class {ratio(rep.get('bindings_without_injected_class'))}; "
          f"method {ratio(rep.get('bindings_without_injected_method'))}"]
    seg["H6"] = len(L)
    h6 = hyp["H6"]
    b = est.get("H6") or {}
    L += ["", "## H6, shape does not draw code in", "",
          f"- **{h6.get('state', h6.get('verdict'))}** (one-sided: each rate ratio below "
          f"{f((b.get('margin') or [None, None])[1])}); each measure fitted alone at its level, with the "
          f"bindings and the bystanders in the model, 90% intervals: method measures on intrusion at the "
          f"method (n = {f(b.get('n'))}), class measures on intrusion at the class, one row per class and "
          f"checkpoint with the class's size held fixed (n = {f(b.get('n_class'))}); reported, two-sided "
          f"({f((b.get('margin') or [None])[0])} to {f((b.get('margin') or [None, None])[1])}): "
          f"{h6.get('two_sided', '–')}"]
    for k, m in (b.get("measures") or {}).items():
        L.append(f"  - {k} ({m.get('at', '–')}): {ratio(m)}, one-sided p {f(m.get('p_upper'))} "
                 f"(two-sided TOST p {f(m.get('p_tost'))})")
    # a class measure left out because the class level cannot be tested is named on the next line
    apart = (spec.get("class_level") or {}).get("testable") is False
    dropped = [k for k in h6.get("dropped") or [] if not (apart and k.startswith("c_"))]
    if dropped:
        counts = {**(spec.get("shape_counts") or {}), **(spec.get("literature_counts") or {})}
        L.append("  - Left out by the variation rule: " + ", ".join(
            f"{k} ({counts.get(k)})" for k in dropped))
    at_class = spec.get("class_level") or {}
    if at_class and not at_class.get("testable"):
        L.append(f"  - The class measures are not tested here: later arrivals in "
                 f"{f(at_class.get('classes_with_arrivals'))} distinct classes (at least "
                 f"{f(at_class.get('min_classes'))} needed), the busiest holding "
                 f"{f(at_class.get('top_class_share'))} of them (at most {f(at_class.get('max_share'))}). "
                 f"They are reported below, each alone.")
    sens = (ver.get("sensitivity") or {}).get("H6_with_coupling") or {}
    if sens:
        L.append(f"  - Reported, a sensitivity reading: H6's rule with the literature's coupling measures put "
                 f"back (fan-out, CBO, RFC; read apart in this plan as reach): **{sens.get('state', '–')}** over "
                 + (", ".join(sens.get("measures") or []) or "no measure")
                 + (f"; wholly above the margin: {', '.join(sens['above'])}" if sens.get("above") else "")
                 + (f"; not estimable: {', '.join(sens['not_estimable'])}" if sens.get("not_estimable") else "")
                 + ". It changes no verdict.")
    sj = rep.get("shape_joint") or {}
    if sj.get("measures"):
        L.append("- Reported, the block as first registered, together in one model on method-level intrusion: "
                 + "; ".join(f"{k} {ratio(v)}" for k, v in sj["measures"].items()))
    cl = rep.get("H6_class_level") or {}
    if cl:
        L.append("- Reported, that block on class-level intrusion: "
                 + "; ".join(f"{k} {ratio(v)}" for k, v in cl.items()))
    sw = rep.get("shape_without_problem") or {}
    if sw:
        L.append("- Reported, that block without the problem terms, the bindings and the bystanders: "
                 + "; ".join(f"{k} {ratio(v)}" for k, v in sw.items()))
    reach = {k: v for k, v in (rep.get("literature_shape") or {}).items() if k in (spec.get("reach") or [])}
    if reach:
        L.append("- Reported, reach (how far a place reaches out; with the sinew measures, predicted above 1): "
                 + "; ".join(f"{k} {ratio(v)}" for k, v in reach.items()))
    sn = rep.get("sinew") or {}
    left = [k for k in ("s2_stuck", "s3_junction") if k not in sn]
    L.append("- Reported, the sinew measures (data flow, not shape; predicted above 1), later intrusion with "
             "the bindings and the bystanders in the model: "
             + ("; ".join(f"{k} at the method {ratio(v.get('method'))}, at the class {ratio(v.get('class'))}"
                          for k, v in sn.items()) or "none varies enough to be read")
             + (f"; left out by the variation rule: " + ", ".join(
                 f"{k} ({(spec.get('shape_counts') or {}).get(k)})" for k in left) if left and sn else ""))
    for j in ("s3_junction", "s3_junction_injection_aware"):
        L.append(f"- Reported, junction × arm ({j}): {ratio(rep.get('junction_x_arm_' + j))}")
    seg["H4"] = len(L)
    m3 = est.get("H4") or {}
    rs = (readings or {}).get("reopening") or {}
    amt = cond.get("amount") or {}
    w = (cond.get("wiring") or {}).get("verdict") or {}
    L += ["", "## H4, function injection forms no core", "",
          f"- **Function arm's bystanders (arm term, at checkpoint {f(m3.get('centre_checkpoint'), 1)}, "
          f"the middle of the stream): {interval(m3.get('arm'))}**",
          f"- **Their slope on the checkpoint index (interaction): {interval(m3.get('slope'))}**",
          f"- **Later intrusion where bound code was placed, function arm / methods arm: at the class "
          f"{ratio(m3.get('intrusion_class'))}; at the method {ratio(m3.get('intrusion_method'))}**",
          *existing_files_lines(m3, rep),
          f"- How much a core value is come back to, function arm / methods arm (H2's arm contrast): at the "
          f"class {ratio(rep.get('core_reuse_class'))}; at the method {ratio(rep.get('core_reuse_method'))}",
          *reuse_lines(readings or {}),
          *[f"- Reported, {arm}: per checkpoint, classes its bound code goes back into {f(x.get('classes'))}, "
            f"wiring files changed again {f(x.get('wiring'))}" for arm, x in rs.items()],
          f"- Reported, reopening, function arm / methods arm: classes {ratio(rep.get('reopen_classes'))}; "
          f"with wiring files {ratio(rep.get('reopen_with_wiring'))}",
          f"- Reported, bystanders without injected dependencies: arm "
          f"{interval((rep.get('H4_bystanders_without_injected') or {}).get('arm'))}, slope "
          f"{interval((rep.get('H4_bystanders_without_injected') or {}).get('slope'))}",
          f"- Reported, the needed values, function arm against methods arm: {interval(rep.get('needed_arm'))} "
          f"(expected about 0: the same stream)",
          f"- Reported, H4 as first registered (bindings): arm at a host of "
          f"{f((rep.get('H4_bindings') or {}).get('centre_positions'), 1)} positions "
          f"{interval((rep.get('H4_bindings') or {}).get('arm'))}; slope on host size "
          f"{interval((rep.get('H4_bindings') or {}).get('slope'))}",
          "- Reported, the arm difference in bindings at a host of " + "; ".join(
              f"{k} positions {interval(v)}" for k, v in (rep.get("H4_arm_at") or {}).items()),
          f"- Amount added since the base, function arm / methods arm at the final checkpoint: "
          f"{f(amt.get('ratio'))} "
          f"[{f((amt.get('interval') or [None])[0])}, {f((amt.get('interval') or [None, None])[1])}], "
          f"in band: {f(amt.get('in_band'))}",
          f"- Reported, the ratio of the totals: {f(amt.get('ratio_total'))}",
          f"- Wiring growth: slope {f(w.get('growth_slope'))}, interval {w.get('growth_interval')}, "
          f"against: {f(w.get('growth_against'))}",
          f"- Wiring concentration: largest file {f(w.get('largest_share'))}, against: "
          f"{f(w.get('concentration_against'))}",
          f"- Reported, bindings without parameters: arm {interval((rep.get('H4_without_parameters') or {}).get('arm'))}, "
          f"slope {interval((rep.get('H4_without_parameters') or {}).get('slope'))}",
          f"- Reported, bindings without injected dependencies: arm {interval((rep.get('H4_without_injected') or {}).get('arm'))}, "
          f"slope {interval((rep.get('H4_without_injected') or {}).get('slope'))}",
          f"- Reported, trajectory of the bindings (arm × checkpoint): {interval(rep.get('H4_trajectory'))}",
          ]
    seg["end"] = len(L)
    L = (L[:seg["H3"]] + h1_section(est, hyp, rep) + L[seg["H2"]:seg["H6"]] + L[seg["H3"]:seg["H2"]]
         + L[seg["H4"]:seg["end"]] + h5_section(est, hyp, rep, readings or {}) + L[seg["H6"]:seg["H4"]]
         + h7_section(est, hyp, rep, readings or {}) + h9_section(est, hyp, rep, readings or {}))
    L += [
          *h8_section(est, hyp, cond),
          *coupling_source_section(readings or {}),
          *redesign_section(readings or {}),
          *surface_section(rep, readings or {}),
          *containers_section(readings or {}),
          *reader_section(rep, readings or {}),
          *readings_section(est, readings or {}),
          *landing_section({**(readings or {}), "_estimates": rep}),
          *literature_section(est, spec),
          *split_section(rep, readings or {}),
          *validation_section(readings or {}),
          "", "## Provenance", "",
          "Checkpoint intercept in the model: " + (", ".join(
              f"{k} {f(v)}" for k, v in (est.get("checkpoint_intercept") or {}).items()) or "–") + ".", "",
          f"Versions: {json.dumps(est.get('versions'))}. Seed {est.get('seed')}.", "",
          *([f"Registered files changed since `{drift['tag']}` (amendments, PLAN.md §9): "
             + (", ".join(f"`{x}`" for x in drift["changed"]) or "none") + ".", ""]
            if drift else []),
          "| Arm | Run | Chain | Commit |", "|---|---|---|---|"]
    for h in heads:
        L.append(f"| {h['arm']} | {h['run']} | {h['chain']}{' (excluded)' if h['excluded'] else ''} "
                 f"| `{h['sha'][:12]}` |")
    return "\n".join(L) + "\n"


def main() -> None:
    reg = runs.load()
    heads = runs.read_heads()
    tag = reg["registration_tag"]
    drift = runs.drift(tag) if runs.registered(tag) else None
    index = ["# Results", "", "| Analysis | Role | H1 | H2 | H3 | H4 | H5 | H6 | H7 | H9 |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for analysis in reg["analyses"]:
        name = analysis["name"]
        d = OUT / name
        if not (d / "verdicts.json").exists():
            continue
        est = json.loads((d / "estimates.json").read_text())
        ver = json.loads((d / "verdicts.json").read_text())
        data = prepare.DATA / name
        cond = json.loads((data / "conditions.json").read_text())
        spec = json.loads((data / "spec.json").read_text())
        mine = [h for h in heads if h["analysis"] == name]
        rd = json.loads((data / "readings.json").read_text()) if (data / "readings.json").exists() else {}
        (d / "REPORT.md").write_text(render(name, analysis["role"], est, ver, cond, spec, mine, drift, rd))
        hy = ver["hypotheses"]
        index.append(f"| [{name}]({name}/REPORT.md) | {analysis['role']} | "
                     + " | ".join(hy.get(f"H{i}", {}).get("verdict", "–") for i in (1, 2, 3, 4, 5, 6, 7, 9)) + " |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "REPORT.md").write_text("\n".join(index) + "\n")
    print((OUT / "REPORT.md").read_text())


if __name__ == "__main__":
    main()

"""Step 5: the report of every analysis, every hypothesis whichever way it falls (PLAN.md §8).

    python -m placement_gravity.report

Writes results/analysis/<name>/REPORT.md from verdicts.json, estimates.json and the data's
conditions.json, and results/analysis/REPORT.md listing every analysis's verdicts.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import prepare, runs

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


def h5_section(est: dict, hyp: dict, rep: dict) -> list[str]:
    """H5, choice narrows (PLAN.md §2, §4.2a, §5)."""
    b = est.get("H5") or {}
    h = hyp.get("H5") or {}
    L = ["", "## H5, choice narrows (methods arm)", "",
         "Per bound addition, the other places in the code before its checkpoint that hold what its code "
         "was bound to: at the class, another class holding injected dependencies of the same types (code "
         "bound to the class's own state, constants or methods has none); at the method, another method "
         "with a parameter or local of each type. The ratio of the alternatives at the end of the stream "
         f"to its start, 90% interval, one-sided below {f((b.get('margin') or [None, None])[1])}.", "",
         f"- **{h.get('state', h.get('verdict', '–'))}**"]
    for lev in ("class", "method"):
        x = b.get(lev) or {}
        if x.get("all_forced"):
            L.append(f"- **At the {lev}: every placement forced** ({f(x.get('n'))} rows; no alternative anywhere)")
        else:
            L.append(f"- **At the {lev}: {ratio(x)}** (n = {f(x.get('n'))}"
                     + (f"; one-sided p {f(x.get('p_upper'))}" if "p_upper" in x else "") + ")")
        for arm, sp in (rep.get(f"H5_spread_{lev}") or {}).items():
            if not sp:
                continue
            tf, ta = sp.get("thirds_forced") or {}, sp.get("thirds_alternatives") or {}
            L.append(f"- Reported, {arm} arm at the {lev}: {f(sp.get('rows'))} rows, {f(sp.get('forced'))} forced, "
                     f"{f(sp.get('mean_alternatives'))} alternatives a row; over the thirds, forced "
                     + ", ".join(f(tf.get(k)) for k in ("1", "2", "3")) + "; alternatives "
                     + ", ".join(f(ta.get(k)) for k in ("1", "2", "3")))
        L.append(f"- Reported, the function arm's ratio at the {lev}: {ratio(rep.get(f'H5_function_arm_{lev}'))}; "
                 f"function arm / methods arm: {ratio(rep.get(f'H5_arm_{lev}'))}")
    L.append(f"- Reported, class rows bound to the class's own state, constants or methods: "
             f"{f(rep.get('H5_class_own'))}; method values of no declared type left out of the match: "
             f"{f(rep.get('H5_method_untyped'))}")
    return L


def bystander_lines(r: dict) -> list[str]:
    """The description beside H1: needed values and bystanders per run, per arm (PLAN.md §4.3a)."""
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
         "fixed and an intercept for the class (\u2020: refitted without it). Read as H3 is: below 1.25 does "
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
              f"coincidental. These rows are not part of H3 in this analysis."]
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
         "| Hypothesis | Verdict | p (Holm) |", "|---|---|---|"]
    for k, v in hyp.items():
        L.append(f"| {k} | {v['verdict']} | {f(v.get('p_holm'))} |")
    h1 = est.get("H1") or {}
    lv = rep.get("H1_levels") or {}
    t1 = rep.get("H1_bindings") or {}
    L += ["", "## H1, the periphery grows (methods arm)", "",
          f"Runs that need a pre-existing value {f(h1.get('n_runs'))} over {f(h1.get('n_chains'))} "
          f"chains; the slope of log(1 + bystanders) on the checkpoint index, cluster-bootstrap 95% interval "
          f"({est.get('boot')} refits).", "",
          f"- **Bystanders on the checkpoint index: {interval(h1.get('cp'))}**",
          f"- **Within a class, the class's bystanders: {interval(h1.get('within_class'))}** "
          f"({f((h1.get('within_class') or {}).get('places'))} classes with runs at two or more checkpoints)",
          f"- **Within a method, the method's bystanders: {interval(h1.get('within_method'))}** "
          f"({f((h1.get('within_method') or {}).get('places'))} methods)",
          f"- Reported, within a place in the function arm: class "
          f"{interval((rep.get('H1_within_function_arm') or {}).get('class'))}; method "
          f"{interval((rep.get('H1_within_function_arm') or {}).get('method'))}",
          f"- Reported, method bystanders {interval(lv.get('method'))}; class bystanders "
          f"{interval(lv.get('class'))}",
          f"- Reported, without injected dependencies {interval(lv.get('without_injected'))}; without "
          f"constants {interval(lv.get('without_constants'))}",
          f"- Reported, the function arm's slope: {interval(lv.get('function_arm'))}",
          *bystander_lines(readings or {}),
          f"- Reported, H1 as first registered (bindings of runs into existing methods): on log(host "
          f"positions) {interval(t1.get('log_host'))}; on the checkpoint index {interval(t1.get('cp'))}",
          f"- Reported, bindings in the function arm: on host size {interval((rep.get('H1_function_arm') or {}).get('log_host'))}",
          f"- Reported, bindings at class level (methods arm): on class size {interval((rep.get('H1_class_level') or {}).get('log_class'))}",
          f"- Reported, bindings without injected dependencies: on host size {interval((rep.get('H1_without_injected') or {}).get('log_host'))}; "
          f"class level on class size {interval((rep.get('H1_class_level_without_injected') or {}).get('log_class'))}"]
    e2 = est.get("H2") or {}
    rows_ = rep.get("intrusion_rows") or {}
    L += ["", "## H2, a core draws code in (methods arm)", "",
          f"Where code was bound to a class or a method ({f(rows_.get('bound'))} of {f(rows_.get('all'))} "
          f"problem and host rows, both arms; {f(e2.get('n'))} in the methods arm): the later intrusions' "
          f"uses of the values that code was bound to (the core) against their uses of the rest the "
          f"place held, what stood by and what the change introduced (the periphery), as a rate ratio "
          f"per value. A later change counts each value once in each method its bound code is in.", "",
          f"- **At the class (its fields and the methods it calls): {ratio(e2.get('class'))}**",
          f"- **At the method (its values): {ratio(e2.get('method'))}**",
          f"- Reported, the function arm: class {ratio(rep.get('H2_core_function_arm_class'))}; method "
          f"{ratio(rep.get('H2_core_function_arm_method'))}",
          *core_lines(readings or {}),
          f"- Reported, at the class on its fields only (as until 19 November 2026): "
          f"{ratio(rep.get('H2_class_fields'))}",
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
    h3 = hyp["H3"]
    b = est.get("H3") or {}
    L += ["", "## H3, shape does not draw code in", "",
          f"- **{h3.get('state', h3.get('verdict'))}** (one-sided: each rate ratio below "
          f"{f((b.get('margin') or [None, None])[1])}); each measure fitted alone at its level, with the "
          f"bindings and the bystanders in the model, 90% intervals: method measures on intrusion at the "
          f"method (n = {f(b.get('n'))}), class measures on intrusion at the class, one row per class and "
          f"checkpoint with the class's size held fixed (n = {f(b.get('n_class'))}); reported, two-sided "
          f"({f((b.get('margin') or [None])[0])} to {f((b.get('margin') or [None, None])[1])}): "
          f"{h3.get('two_sided', '–')}"]
    for k, m in (b.get("measures") or {}).items():
        L.append(f"  - {k} ({m.get('at', '–')}): {ratio(m)}, one-sided p {f(m.get('p_upper'))} "
                 f"(two-sided TOST p {f(m.get('p_tost'))})")
    # a class measure left out because the class level cannot be tested is named on the next line
    apart = (spec.get("class_level") or {}).get("testable") is False
    dropped = [k for k in h3.get("dropped") or [] if not (apart and k.startswith("c_"))]
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
    sj = rep.get("shape_joint") or {}
    if sj.get("measures"):
        L.append("- Reported, the block as first registered, together in one model on method-level intrusion: "
                 + "; ".join(f"{k} {ratio(v)}" for k, v in sj["measures"].items()))
    cl = rep.get("H3_class_level") or {}
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
          f"- Reported, how much a core value is come back to, function arm / methods arm: at the class "
          f"{ratio(rep.get('core_reuse_class'))}; at the method {ratio(rep.get('core_reuse_method'))}",
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
          *h5_section(est, hyp, rep),
          *readings_section(est, readings or {}),
          *landing_section({**(readings or {}), "_estimates": rep}),
          *literature_section(est, spec),
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
    index = ["# Results", "", "| Analysis | Role | H1 | H2 | H3 | H4 | H5 |", "|---|---|---|---|---|---|---|"]
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
        index.append(f"| [{name}]({name}/REPORT.md) | {analysis['role']} | {hy['H1']['verdict']} "
                     f"| {hy['H2']['verdict']} | {hy['H3']['verdict']} | {hy['H4']['verdict']} "
                     f"| {hy.get('H5', {}).get('verdict', '–')} |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "REPORT.md").write_text("\n".join(index) + "\n")
    print((OUT / "REPORT.md").read_text())


if __name__ == "__main__":
    main()

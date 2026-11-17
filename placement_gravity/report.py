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


def bystander_lines(r: dict) -> list[str]:
    """The description beside H1: needed values and bystanders per run, per arm (PLAN.md §4.3a)."""
    L = []
    for arm, x in (r.get("bystanders") or {}).items():
        L.append(f"- Reported, {arm}: {f(x.get('pulled'))} of {f(x.get('runs'))} runs need a pre-existing "
                 f"value ({f(x.get('share_free'))} free); per such run, needed {f(x.get('need'))}, bystanders "
                 f"{f(x.get('bystanders'))} (method {f(x.get('by_method'))}, class {f(x.get('by_class'))}; "
                 f"without constants {f(x.get('without_constants'))}); over the thirds of the stream "
                 + ", ".join(f(t) for t in x.get("thirds") or []) + f"; fields left behind per addition "
                 f"{f(x.get('fields_added_per_addition'))}")
    return L


def drawn_lines(r: dict) -> list[str]:
    """The description beside H2: what stood by where tied code was placed, and how much of the
    later intrusion there is tied to it, per arm (PLAN.md §4.4)."""
    L = []
    for arm, x in (r.get("drawn") or {}).items():
        if not x.get("rows"):
            continue
        c, m = x["class"], x["method"]
        L.append(f"- Reported, {arm}: {f(x['rows'])} tied rows; at the class {f(c['bystanders'])} fields "
                 f"stood by, {f(c['drawn'])} of {f(c['later'])} later intrusions tied to one of them "
                 f"({f(c['share'])}); at the method {f(m['bystanders'])} values stood by, {f(m['drawn'])} of "
                 f"{f(m['later'])} ({f(m['share'])})")
    return L


def readings_section(est: dict, r: dict) -> list[str]:
    """Choice at a checkpoint, formation and review (PLAN.md §5): reported, not confirmatory."""
    rep = est.get("reported") or {}
    L = ["", "## Reported readings: choice, formation, review", ""]
    for arm, c in (r.get("choice") or {}).items():
        L.append(f"- Choice, {arm}: {f(c.get('no_choice'))} of {f(c.get('checkpoints'))} checkpoints "
                 f"left no choice (every chain with the same ties, on the same side of new or existing); "
                 f"median spread of ties over chains {f(c.get('median_tie_sd'))}, median distinct hosts "
                 f"{f(c.get('median_distinct_hosts'))}")
    for arm in sorted(k[len("formation_lagged_"):] for k in rep if k.startswith("formation_lagged_")):
        L.append(f"- Formation, lagged, {arm}: ties now on the chain's mean ties so far "
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
        L.append(f"- Formation, where it ends, {arm}: Spearman's rho of early ties with the largest "
                 f"method's share {f(x.get('rho'))} {x.get('interval') or '[no interval]'} over "
                 f"{f(x.get('chains'))} chains (predicted above 0 in the methods arm)")
    rv = r.get("review")
    for arm, x in ((rv or {}).items()):
        if isinstance(x, dict):
            L.append(f"- Review against {rv['against']}, {arm}: Spearman's rho of ties with the change "
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
    t1 = rep.get("H1_ties") or {}
    L += ["", "## H1, gravity compounds (methods arm)", "",
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
          f"- Reported, H1 as first registered (ties of runs into existing methods): on log(host "
          f"positions) {interval(t1.get('log_host'))}; on the checkpoint index {interval(t1.get('cp'))}",
          f"- Reported, ties in the function arm: on host size {interval((rep.get('H1_function_arm') or {}).get('log_host'))}",
          f"- Reported, ties at class level (methods arm): on class size {interval((rep.get('H1_class_level') or {}).get('log_class'))}",
          f"- Reported, ties without injected dependencies: on host size {interval((rep.get('H1_without_injected') or {}).get('log_host'))}; "
          f"class level on class size {interval((rep.get('H1_class_level_without_injected') or {}).get('log_class'))}"]
    e2 = est.get("H2") or {}
    rows_ = rep.get("intrusion_rows") or {}
    L += ["", "## H2, data draws code in (methods arm)", "",
          f"Where code was tied to a class or a method ({f(rows_.get('tied'))} of {f(rows_.get('all'))} "
          f"problem and host rows, both arms; {f(e2.get('n'))} in the methods arm): the later intrusions "
          f"there that are tied to a value which stood by at the placement, as a rate ratio per value "
          f"that stood by.", "",
          f"- **At the class (its fields): {ratio(e2.get('class'))}**",
          f"- **At the method (its values): {ratio(e2.get('method'))}**",
          *drawn_lines(readings or {}),
          f"- Reported, on log(1 + bystanders): class {interval(rep.get('H2_log_class'))}; method "
          f"{interval(rep.get('H2_log_method'))}",
          f"- Reported, the function arm: class {ratio(rep.get('H2_function_arm_class'))}; method "
          f"{ratio(rep.get('H2_function_arm_method'))}",
          f"- Reported, H2 as it stood until 17 November 2026 (later intrusion per tie): class "
          f"{ratio(rep.get('ties_intrusion_class'))}; method {ratio(rep.get('ties_intrusion_method'))}",
          f"- For information, the same on the problem's own lines: {ratio(rep.get('ties_lines'))}",
          f"- Reported, per tie, any later change, tied or not: class {ratio(rep.get('ties_any_change_class'))}; "
          f"method {ratio(rep.get('ties_any_change_method'))}",
          f"- Reported, per tie, existing hosts only: class {ratio(rep.get('ties_existing_hosts_class'))}; method "
          f"{ratio(rep.get('ties_existing_hosts_method'))}",
          f"- Reported, per tie, without injected dependencies: class {ratio(rep.get('ties_without_injected_class'))}; "
          f"method {ratio(rep.get('ties_without_injected_method'))}"]
    h3 = hyp["H3"]
    b = est.get("H3") or {}
    L += ["", "## H3, shape adds nothing", "",
          f"- **{h3.get('state', h3.get('verdict'))}**; bound {f((b.get('bound') or [None])[0])} to "
          f"{f((b.get('bound') or [None, None])[1])}, 90% intervals, method-level intrusion, the ties and the bystanders in the model "
          f"(n = {f(b.get('n'))})"]
    for k, m in (b.get("measures") or {}).items():
        L.append(f"  - {k}: {ratio(m)}, TOST p {f(m.get('p_tost'))}")
    if h3.get("dropped"):
        counts = spec.get("shape_counts") or {}
        L.append("  - Left out by the variation rule: " + ", ".join(
            f"{k} ({counts.get(k)})" for k in h3["dropped"]))
    cl = rep.get("H3_class_level") or {}
    if cl:
        L.append("- Reported, the same on class-level intrusion: "
                 + "; ".join(f"{k} {ratio(v)}" for k, v in cl.items()))
    sw = rep.get("shape_without_problem") or {}
    if sw:
        L.append("- Reported, shape without the problem terms, the ties and the bystanders: "
                 + "; ".join(f"{k} {ratio(v)}" for k, v in sw.items()))
    for j in ("s3_junction", "s3_junction_injection_aware"):
        L.append(f"- Reported, junction × arm ({j}): {ratio(rep.get('junction_x_arm_' + j))}")
    m3 = est.get("H4") or {}
    rs = (readings or {}).get("reopening") or {}
    amt = cond.get("amount") or {}
    w = (cond.get("wiring") or {}).get("verdict") or {}
    L += ["", "## H4, function injection keeps the space open", "",
          f"- **Function arm's bystanders (arm term, at checkpoint {f(m3.get('centre_checkpoint'), 1)}, "
          f"the middle of the stream): {interval(m3.get('arm'))}**",
          f"- **Their slope on the checkpoint index (interaction): {interval(m3.get('slope'))}**",
          f"- **Later intrusion where tied code was placed, function arm / methods arm: at the class "
          f"{ratio(m3.get('intrusion_class'))}; at the method {ratio(m3.get('intrusion_method'))}**",
          *[f"- Reported, {arm}: per checkpoint, classes its tied code goes back into {f(x.get('classes'))}, "
            f"wiring files changed again {f(x.get('wiring'))}" for arm, x in rs.items()],
          f"- Reported, reopening, function arm / methods arm: classes {ratio(rep.get('reopen_classes'))}; "
          f"with wiring files {ratio(rep.get('reopen_with_wiring'))}",
          f"- Reported, bystanders without injected dependencies: arm "
          f"{interval((rep.get('H4_bystanders_without_injected') or {}).get('arm'))}, slope "
          f"{interval((rep.get('H4_bystanders_without_injected') or {}).get('slope'))}",
          f"- Reported, the needed values, function arm against methods arm: {interval(rep.get('needed_arm'))} "
          f"(expected about 0: the same stream)",
          f"- Reported, H4 as first registered (ties): arm at a host of "
          f"{f((rep.get('H4_ties') or {}).get('centre_positions'), 1)} positions "
          f"{interval((rep.get('H4_ties') or {}).get('arm'))}; slope on host size "
          f"{interval((rep.get('H4_ties') or {}).get('slope'))}",
          "- Reported, the arm difference in ties at a host of " + "; ".join(
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
          f"- Reported, ties without parameters: arm {interval((rep.get('H4_without_parameters') or {}).get('arm'))}, "
          f"slope {interval((rep.get('H4_without_parameters') or {}).get('slope'))}",
          f"- Reported, ties without injected dependencies: arm {interval((rep.get('H4_without_injected') or {}).get('arm'))}, "
          f"slope {interval((rep.get('H4_without_injected') or {}).get('slope'))}",
          f"- Reported, trajectory of the ties (arm × checkpoint): {interval(rep.get('H4_trajectory'))}",
          *readings_section(est, readings or {}),
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
    index = ["# Results", "", "| Analysis | Role | H1 | H2 | H3 | H4 |", "|---|---|---|---|---|---|"]
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
                     f"| {hy['H2']['verdict']} | {hy['H3']['verdict']} | {hy['H4']['verdict']} |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "REPORT.md").write_text("\n".join(index) + "\n")
    print((OUT / "REPORT.md").read_text())


if __name__ == "__main__":
    main()

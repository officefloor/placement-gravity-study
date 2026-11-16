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
    L += ["", "## H1, gravity compounds (methods arm)", "",
          f"Runs {f(h1.get('n_runs'))} over {f(h1.get('n_chains'))} chains; slopes of log(1 + ties), "
          f"cluster-bootstrap 95% intervals ({est.get('boot')} refits).", "",
          f"- On log(host positions): {interval(h1.get('log_host'))}",
          f"- On the checkpoint index: {interval(h1.get('cp'))}",
          f"- Reported, the function arm: on host size {interval((rep.get('H1_function_arm') or {}).get('log_host'))}",
          f"- Reported, class level (methods arm): on class size {interval((rep.get('H1_class_level') or {}).get('log_class'))}",
          f"- Reported, without injected dependencies: on host size {interval((rep.get('H1_without_injected') or {}).get('log_host'))}; "
          f"class level on class size {interval((rep.get('H1_class_level_without_injected') or {}).get('log_class'))}"]
    h2 = hyp["H2"]
    a = (h2.get("detail") or {}).get("H2a") or {}
    b = (h2.get("detail") or {}).get("H2b") or {}
    L += ["", "## H2, forcing does the harm, not shape", "",
          f"- **H2a**, rate ratio of intrusion on the problem's own lines, per tie: {ratio(a)} "
          f"(n = {f(a.get('n'))})",
          f"- Reported, the host-level count (any later change to the host): {ratio(rep.get('H2a_host_level'))}",
          f"- Reported, existing hosts only: {ratio(rep.get('H2a_existing_hosts'))}",
          f"- Reported, ties without injected dependencies: {ratio(rep.get('H2a_without_injected'))}",
          f"- **H2b**: {h2.get('h2b')}; bound {f((b.get('bound') or [None])[0])} to "
          f"{f((b.get('bound') or [None, None])[1])}, 90% intervals (n = {f(b.get('n'))})"]
    for k, m in (b.get("measures") or {}).items():
        L.append(f"  - {k}: {ratio(m)}, TOST p {f(m.get('p_tost'))}")
    if h2.get("h2b_dropped"):
        counts = spec.get("shape_counts") or {}
        L.append("  - Left out by the variation rule: " + ", ".join(
            f"{k} ({counts.get(k)})" for k in h2["h2b_dropped"]))
    sw = rep.get("shape_without_problem") or {}
    if sw:
        L.append("- Reported, shape without the problem terms and ties: "
                 + "; ".join(f"{k} {ratio(v)}" for k, v in sw.items()))
    for j in ("s3_junction", "s3_junction_injection_aware"):
        L.append(f"- Reported, junction × arm ({j}): {ratio(rep.get('junction_x_arm_' + j))}")
    h3 = hyp["H3"]
    m3 = est.get("H3") or {}
    amt = cond.get("amount") or {}
    w = (cond.get("wiring") or {}).get("verdict") or {}
    L += ["", "## H3, function injection keeps the space open", "",
          f"- Function arm's ties (arm term, at a host of {f(m3.get('centre_positions'), 1)} positions, "
          f"the centre): {interval(m3.get('arm'))}",
          f"- Its slope on host size (interaction): {interval(m3.get('slope'))}",
          "- Reported, the arm difference at a host of " + "; ".join(
              f"{k} positions {interval(v)}" for k, v in (rep.get("H3_arm_at") or {}).items()),
          f"- Amount added since the base, function arm / methods arm at the final checkpoint: "
          f"{f(amt.get('ratio'))} "
          f"[{f((amt.get('interval') or [None])[0])}, {f((amt.get('interval') or [None, None])[1])}], "
          f"in band: {f(amt.get('in_band'))}",
          f"- Reported, the ratio of the totals: {f(amt.get('ratio_total'))}",
          f"- Wiring growth: slope {f(w.get('growth_slope'))}, interval {w.get('growth_interval')}, "
          f"against: {f(w.get('growth_against'))}",
          f"- Wiring concentration: largest file {f(w.get('largest_share'))}, against: "
          f"{f(w.get('concentration_against'))}",
          f"- Reported, without parameter ties: arm {interval((rep.get('H3_without_parameters') or {}).get('arm'))}, "
          f"slope {interval((rep.get('H3_without_parameters') or {}).get('slope'))}",
          f"- Reported, without injected dependencies: arm {interval((rep.get('H3_without_injected') or {}).get('arm'))}, "
          f"slope {interval((rep.get('H3_without_injected') or {}).get('slope'))}",
          f"- Reported, trajectory (arm × checkpoint): {interval(rep.get('H3_trajectory'))}",
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
    index = ["# Results", "", "| Analysis | Role | H1 | H2 | H3 |", "|---|---|---|---|---|"]
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
                     f"| {hy['H2']['verdict']} | {hy['H3']['verdict']} |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "REPORT.md").write_text("\n".join(index) + "\n")
    print((OUT / "REPORT.md").read_text())


if __name__ == "__main__":
    main()

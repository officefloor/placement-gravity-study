"""Step 4, the decision: each hypothesis's verdict from the R estimates and the conditions
(PLAN.md §2, §5). Every decision rule of the study is here.

- **H3** (the methods arm): the slope of the bystanders (PLAN.md §4.3a) on the checkpoint index
  above 0, over all runs and within a place: the class's bystanders within a class, the method's
  within a method. p = the largest of the three one-sided bootstrap p-values.
- **H2** (the methods arm): where code was bound to a class or a method, the rate ratio of the
  later intrusions' uses of a core value (one the code was bound to; at the class, a private one)
  to their uses of a periphery value, above 1 at the class and at the method (one-sided, cluster
  bootstrap over chains; PLAN.md §4.4); **and** (since 22 November 2026) a core value come back
  to less in the function arm than in the methods arm, the rate ratio below 1, at each level
  where both arms have the core records to compare (``reuse_class``, ``reuse_method``,
  ``required``). p = the largest of the parts. On a history the arms do not solve the same
  problems and the arm contrast is not read.
- **H6** (one-sided): every shape measure kept shown not to raise later intrusion at its level, the
  method or the class: its rate ratio below the upper margin (1.25), by a one-sided test, each
  measure fitted alone with the bindings and the bystanders in the model. p = the largest of those p-values. A measure that lowers intrusion does
  not count against. The two-sided reading (within 0.8 to 1.25) is reported.
- **H4**: the function arm's bystanders fewer half-way through the stream, their slope on the
  checkpoint index flatter, and its bound code come back to less, at the class and at the method
  and (since 22 November 2026) its changes going back into less well-trodden files, production
  Java and wiring counted alike (``trodden``: the earlier checkpoints that had changed each file
  it changed), the rate ratio below 1 (p = the largest of the five one-sided p-values); the amount within its band; and neither wiring condition against.
- **H1, the force: forced less with function injection** (restated 25 November 2026, PLAN.md §9
  row 107; the author's: "this just needs to be OfficeFloor is forced less especially over time"):
  per checkpoint, the placements forced at the class (bound there with no other class holding what
  the code was bound to) fewer in the function arm half-way through the stream (rate ratio below 1)
  **and** rising less over it (the arm's interaction with the index below 1); p = the larger of the
  two one-sided bootstrap p-values, as H4 and H5. Reversed if the arm term's interval lies wholly
  above 1. Not testable on a history (no arms solving the same problems). (From 19 November 2026,
  *choice narrows*: the methods arm's alternatives at the class falling over the stream, needed
  with the contrast from 24 November; reported since, in ``detail.class``.)
- **H7, spread does not see it** (restated 21 November 2026, PLAN.md §9 row 67; one-sided, as
  H6): in the methods arm, a unit with a placement forced at the class does not place or edit code
  in more of the classes that existed before it than a unit without one, at the same change size
  and point in the stream: the spread's rate ratio on forced shown below the upper margin (1.25).
  Not supported when its interval lies wholly above the margin; unresolved when it reaches above
  it. (Until then, *forced changes spread*: the ratio above 1.) The spread's rise is reported.
- **H5, surface against volume** (restated 24 November 2026, PLAN.md §9 row 89; the author's):
  for the same logic added (the volume), the function arm adds less weight of links between blocks
  of logic (the surface: call, state and flow links, each weighed by the data it carries since row
  95, constants counted as state since row 109, injection not among them) half-way through the
  stream, the rate ratio below 1, **and** the gap widens, the arm's interaction with the checkpoint
  index below 1 (p = the larger of the two one-sided bootstrap p-values, as H4). Reversed if the
  arm's interval lies wholly above 1. Not testable on a history (no arms solving the same
  problems). (Until 24 November 2026, *forced changes couple*: in the methods arm the calls a
  forced class gained across its boundary, the ratio on forced above 1; deleted the same day,
  PLAN.md §9 row 90.)
- **Two tiers** (decided by the author on 21 November 2026): the **confirmatory** family is the
  force and its two outlets, with the control: H2, H4, H1 and H5, Holm over the four at α = 0.05
  (H7 left it when restated, later the same day). H3, H6 and H7 are **secondary**: each keeps its
  rule and direction and is decided at α = 0.05 on its own p, outside the correction, and
  reported as secondary.
- **H6 with the coupling measures put back** (a sensitivity reading, 22 November 2026;
  ``sensitivity.H6_with_coupling``): H6's rule over its measures and the literature's coupling
  measures the plan reads apart as reach (fan-out, CBO, RFC). It changes no verdict.
- **H8, without encapsulation code disperses** (Run D against Run A's same stack, PLAN.md §3.1a;
  an analysis with ``contrast: no-encapsulation``; decided on its own p at α = 0.05, on its own
  run): the open arm's bound code is come back to less at the class (rate ratio below 1) and its
  changes add more calls and field reads across class boundaries at the same change size (rate
  ratio above 1); p = the larger of the two; with compliance (at least 90% of the members it
  introduces not private) and the amount within its band as conditions. Below the compliance bar
  it is descriptive only.

Verdicts: ``supported``; ``not supported``; ``reversed`` (an interval wholly on the wrong side);
``unresolved`` (H6, H7: an interval reaching above the upper margin without lying above it);
``not testable`` (H6: no shape measure varies; H1 and H5: a history); ``descriptive only``
(fewer than 6 chains in an arm, or the development analysis).
"""

from __future__ import annotations

import json
from pathlib import Path

ALPHA = 0.05
#: The confirmatory family (Holm) and the secondary hypotheses (their own p), 21 November 2026;
#: H7 secondary since its restatement the same day.
CONFIRMATORY = ("H1", "H2", "H4", "H5")
SECONDARY = ("H3", "H6", "H7")
#: H6's measures (PLAN.md §2, §5): at the method, long, cognitive and cyclomatic complexity; at the
#: class, concentration, WMC and lack of cohesion. Each is fitted alone. Not slimmable and
#: junction are sinew measures, and fan-out and CBO measures of reach, reported apart.
SHAPES = ("s1_long", "s4_cognitive", "m_cyclomatic", "c_gini", "c_wmc", "c_lcom_star")
#: Run D's compliance bar (PLAN.md §3.1a): the share of introduced members that are not private.
COMPLIANCE = 0.9


def holm(ps: dict[str, float | None]) -> dict[str, float | None]:
    """Holm-adjusted p-values over the hypotheses that have one."""
    have = sorted(((p, k) for k, p in ps.items() if p is not None))
    m = len(have)
    out: dict[str, float | None] = {k: None for k in ps}
    running = 0.0
    for i, (p, k) in enumerate(have):
        running = max(running, min(1.0, (m - i) * p))
        out[k] = running
    return out


def _ok(x: dict | None) -> bool:
    return bool(x) and "error" not in x


def h3(est: dict) -> dict:
    x = est.get("H3") or {}
    parts = [x.get("cp"), x.get("within_class"), x.get("within_method")]
    if not all(_ok(b) for b in parts):
        return {"p": None, "verdict": "not estimable", "detail": x}
    return {"p": max(b["p_greater"] for b in parts), "reversed": any(b["upper"] < 0 for b in parts),
            "conditions_met": all(b["lower"] > 0 for b in parts), "detail": x}


def h2(est: dict) -> dict:
    x = est.get("H2") or {}
    c, m = x.get("class"), x.get("method")
    if not (_ok(c) and _ok(m)):
        return {"p": None, "verdict": "not estimable", "detail": x}
    # the arm contrast, where both arms have the cores to compare: a core value come back to less
    # in the function arm
    reuse = {lev: x.get(f"reuse_{lev}") for lev in ("class", "method")}
    need = {lev: r for lev, r in reuse.items() if r and r.get("required")}
    if any(not _ok(r) or "irr_upper" not in r for r in need.values()):
        return {"p": None, "verdict": "not estimable", "detail": x}
    return {"p": max(c["p_greater"], m["p_greater"], *(r["p_less"] for r in need.values())),
            "reversed": c["irr_upper"] < 1 or m["irr_upper"] < 1 or any(r["irr_lower"] > 1 for r in need.values()),
            "conditions_met": c["irr_lower"] > 1 and m["irr_lower"] > 1
            and all(r["irr_upper"] < 1 for r in need.values()),
            "arm_contrast": sorted(need), "detail": x}


def shape_state(measures: dict, upper: float) -> str:
    """H6's rule over a set of measures, each fitted alone: against, not above, or unresolved."""
    if any(m.get("above", m["irr_lower"] > upper) for m in measures.values()):
        return "against"            # a shape measure raises later intrusion beyond the margin
    if all(m["irr_upper"] <= upper for m in measures.values()):
        return "not above"
    return "unresolved"


def h6_with_coupling(est: dict) -> dict:
    """The sensitivity reading of H6 (22 November 2026): its rule over its measures with the
    literature's coupling measures put back (fan-out, CBO, RFC). Reported; it changes no verdict."""
    b = (est.get("reported") or {}).get("H6_with_coupling") or {}
    measures = {k: m for k, m in (b.get("measures") or {}).items() if _ok(m) and m.get("irr_upper") is not None}
    failed = [k for k in (b.get("measures") or {}) if k not in measures]
    if not measures:
        return {"state": "not testable", "measures": [], "not_estimable": failed}
    upper = (b.get("margin") or [0.8, 1.25])[1]
    return {"state": shape_state(measures, upper), "measures": sorted(measures), "not_estimable": failed,
            "above": sorted(k for k, m in measures.items() if m.get("above", m["irr_lower"] > upper)),
            "p": max(m["p_upper"] for m in measures.values())}


def h6(est: dict) -> dict:
    b = est.get("H6") or {}
    measures = b.get("measures") or {}
    dropped = [k for k in SHAPES if k not in (b.get("kept") or [])]
    if any(not _ok(m) for m in measures.values()):
        return {"p": None, "verdict": "not estimable", "dropped": dropped, "detail": b}
    if not (b.get("testable") and measures):
        return {"p": None, "verdict": "not testable", "state": "not testable", "dropped": dropped,
                "detail": b}
    upper = b["margin"][1]
    state = shape_state(measures, upper)
    # reported: the two-sided reading, as H6 stood until 17 November 2026
    two_sided = ("outside" if any(m.get("outside") for m in measures.values()) else
                 "within" if all(b["margin"][0] <= m["irr_lower"] and m["irr_upper"] <= upper
                                 for m in measures.values()) else "unresolved")
    return {"p": max(m.get("p_upper", m.get("p_tost")) for m in measures.values()), "state": state,
            "two_sided": two_sided, "dropped": dropped, "conditions_met": state == "not above",
            "detail": b}


def h4(est: dict, cond: dict) -> dict:
    x = est.get("H4") or {}
    arm, slope = x.get("arm"), x.get("slope")
    ic, im = x.get("intrusion_class"), x.get("intrusion_method")
    # how well-trodden the files a change went back into, Java and wiring alike (not on a history)
    ef = x.get("trodden") or {}
    files = None if ef.get("not_applicable") else ef
    if not (_ok(arm) and _ok(slope) and _ok(ic) and _ok(im)) or (files is not None and not _ok(files)):
        return {"p": None, "verdict": "not estimable", "detail": x}
    amount = cond.get("amount") or {}
    w = (cond.get("wiring") or {}).get("verdict") or {}
    wiring_against = bool(w.get("growth_against")) or bool(w.get("concentration_against"))
    lower = (arm["upper"] < 0 and slope["upper"] < 0 and ic["irr_upper"] < 1 and im["irr_upper"] < 1
             and (files is None or files["irr_upper"] < 1))
    return {"p": max(arm["p_less"], slope["p_less"], ic["p_less"], im["p_less"],
                     *([files["p_less"]] if files is not None else [])),
            "reversed": arm["lower"] > 0,
            "amount_in_band": amount.get("in_band"), "wiring_against": wiring_against,
            "conditions_met": lower and amount.get("in_band") is True and not wiring_against,
            "detail": {"model": x, "amount": amount, "wiring": w}}


def h1(est: dict) -> dict:
    """The force (restated 25 November 2026, PLAN.md §9 row 107): forced placements at the class
    per checkpoint fewer in the function arm half-way through, and rising less; both below 1. The
    methods arm's alternatives over the stream (choice narrows, the test until then) are reported in
    ``detail``. Not testable on a history."""
    x = est.get("H1") or {}
    c = x.get("contrast")
    if c is None:                    # a history: no arms solving the same problems
        return {"p": None, "verdict": "not testable", "state": "a history", "detail": x}
    arm, trend = c.get("arm"), c.get("trend")
    if not (_ok(c) and _ok(arm) and _ok(trend)) or "irr_upper" not in arm or "irr_upper" not in trend:
        return {"p": None, "verdict": "not estimable", "detail": x}
    return {"p": max(arm["p_less"], trend["p_less"]), "reversed": arm["irr_lower"] > 1,
            "conditions_met": arm["irr_upper"] < 1 and trend["irr_upper"] < 1, "detail": x}


def h7(est: dict) -> dict:
    x = est.get("H7") or {}
    fo = x.get("forced")
    if not _ok(fo) or "p_upper" not in fo:
        return {"p": None, "verdict": "not estimable", "detail": x}
    upper = (x.get("margin") or [0.8, 1.25])[1]
    state = ("against" if fo["irr_lower"] > upper else
             "not above" if fo["irr_upper"] <= upper else "unresolved")
    return {"p": fo["p_upper"], "state": state, "conditions_met": state == "not above",
            "detail": x}


def h5(est: dict) -> dict:
    """Surface against volume (restated 24 November 2026): fewer links for the same logic in the
    function arm, and a gap that widens over the stream; both below 1."""
    x = est.get("H5") or {}
    if x.get("not_applicable"):
        return {"p": None, "verdict": "not testable", "state": "a history", "detail": x}
    arm, trend = x.get("arm"), x.get("trend")
    if not (_ok(arm) and _ok(trend)) or "irr_upper" not in arm or "irr_upper" not in trend:
        return {"p": None, "verdict": "not estimable", "detail": x}
    return {"p": max(arm["p_less"], trend["p_less"]), "reversed": arm["irr_lower"] > 1,
            "conditions_met": arm["irr_upper"] < 1 and trend["irr_upper"] < 1, "detail": x}


def h8(est: dict, cond: dict) -> dict:
    """Run D, the no-encapsulation run, against Run A's same stack (PLAN.md §3.1a): without
    encapsulation code disperses. The open arm is the analysis's function arm."""
    ic = (est.get("H4") or {}).get("intrusion_class")
    co = est.get("coupled_arm")
    comp = (cond.get("compliance") or {}).get("share")
    amount = cond.get("amount") or {}
    out = {"tier": "registered, its own run", "compliance": comp, "compliance_bar": COMPLIANCE,
           "amount_in_band": amount.get("in_band"), "detail": {"intrusion_class": ic, "coupled": co}}
    if comp is None or comp < COMPLIANCE:
        return {**out, "p": None, "verdict": "descriptive only", "state": "the instruction did not take"}
    if not (_ok(ic) and _ok(co)):
        return {**out, "p": None, "verdict": "not estimable"}
    met = ic["irr_upper"] < 1 and co["irr_lower"] > 1 and amount.get("in_band") is True
    return {**out, "p": max(ic["p_less"], co["p_greater"]),
            "reversed": ic["irr_lower"] > 1 or co["irr_upper"] < 1, "conditions_met": met}


def decide(est: dict, cond: dict) -> dict:
    parts = {"H1": h1(est), "H2": h2(est), "H3": h3(est), "H4": h4(est, cond), "H5": h5(est),
             "H6": h6(est), "H7": h7(est)}
    adjusted = holm({k: parts[k]["p"] for k in CONFIRMATORY})
    for k, v in parts.items():
        v["tier"] = "confirmatory" if k in CONFIRMATORY else "secondary"
        # a secondary hypothesis is decided on its own p, outside the correction
        v["p_holm"] = adjusted[k] if k in CONFIRMATORY else v["p"]
        if cond.get("descriptive_only"):
            v["verdict"] = "descriptive only"
        elif "verdict" in v:
            continue
        elif v["p_holm"] is not None and v["p_holm"] <= ALPHA and v["conditions_met"]:
            v["verdict"] = "supported"
        elif v.get("reversed"):
            v["verdict"] = "reversed"
        elif k in ("H6", "H7") and v.get("state") == "unresolved":
            v["verdict"] = "unresolved"
        else:
            v["verdict"] = "not supported"
    out = {"alpha": ALPHA, "descriptive_only": bool(cond.get("descriptive_only")),
           "hypotheses": parts, "sensitivity": {"H6_with_coupling": h6_with_coupling(est)}}
    if cond.get("contrast") == "no-encapsulation":
        # Run D against Run A's same stack: its one test is H8, on its own p; H1 to H7 are the
        # arms' test (the ui primary) and are descriptive here
        for v in parts.values():
            v["verdict"] = "descriptive only"
        v = h8(est, cond)
        v["p_holm"] = v["p"]
        if cond.get("descriptive_only"):
            v["verdict"] = "descriptive only"
        elif "verdict" not in v:
            v["verdict"] = ("supported" if v["p"] <= ALPHA and v["conditions_met"] else
                            "reversed" if v["reversed"] else "not supported")
        parts["H8"] = v
        out["contrast"] = "no-encapsulation"
    return out


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("data", type=Path)       # data/analysis/<name>
    ap.add_argument("estimates", type=Path)  # results/analysis/<name>/estimates.json
    a = ap.parse_args()
    est = json.loads(a.estimates.read_text())
    cond = json.loads((a.data / "conditions.json").read_text())
    out = decide(est, cond)
    (a.estimates.parent / "verdicts.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["hypotheses"].items():
        print(f"{k}: {v['verdict']} (Holm p = {v['p_holm']})")


if __name__ == "__main__":
    main()

"""Step 4, the decision: each hypothesis's verdict from the R estimates and the conditions
(PLAN.md §2, §5). Every decision rule of the study is here.

- **H1** (the methods arm): the slope of the bystanders (PLAN.md §4.3a) on the checkpoint index
  above 0, over all runs and within a place: the class's bystanders within a class, the method's
  within a method. p = the largest of the three one-sided bootstrap p-values.
- **H2** (the methods arm): where code was bound to a class or a method, the rate ratio, per value
  that stood by there, of the later intrusions bound to what stood by, above 1 at the class and at
  the method (one-sided Wald; p = the larger of the two; PLAN.md §4.4).
- **H3** (one-sided): every shape measure kept shown not to raise later intrusion at its level, the
  method or the class: its rate ratio below the upper margin (1.25), by a one-sided test, each
  measure fitted alone with the bindings and the bystanders in the model. p = the largest of those p-values. A measure that lowers intrusion does
  not count against. The two-sided reading (within 0.8 to 1.25) is reported.
- **H4**: the function arm's bystanders fewer half-way through the stream, their slope on the
  checkpoint index flatter, and its bound code come back to less, at the class and at the method
  (p = the largest of the four one-sided p-values); the amount within its band; and neither wiring
  condition against.
- **H5** (one-sided, as H3; 19 November 2026): in the methods arm, the alternatives a bound
  addition had (other places holding what its code was bound to) do not rise over the stream: the
  ratio of the end of the stream to its start shown below the upper margin (1.25), at the class,
  the encapsulation (20 November 2026: the method level shows the encapsulation's volume growing,
  so it is reported, not tested). A class level where every placement was forced (no alternative
  anywhere) cannot rise and passes, with p 0.
- **H6, spread does not see it** (restated 21 November 2026, PLAN.md §9 row 67; one-sided, as
  H3): in the methods arm, a unit with a placement forced at the class does not place or edit code
  in more of the classes that existed before it than a unit without one, at the same change size
  and point in the stream: the spread's rate ratio on forced shown below the upper margin (1.25).
  Not supported when its interval lies wholly above the margin; unresolved when it reaches above
  it. (Until then, *forced changes spread*: the ratio above 1.) The spread's rise is reported.
- **H7** (20 November 2026): in the methods arm, a class with a placement forced at the class
  gains more calls across its boundary (outward and inward) in that unit than one without, at the
  same point in the stream: the rate ratio on forced above 1 (one-sided Wald). Reversed if its
  interval lies wholly below 1. Whether those calls reach members the unit exposed or widened is
  reported.
- **Two tiers** (decided by the author on 21 November 2026): the **confirmatory** family is the
  force and its two outlets, with the control: H2, H4, H5 and H7, Holm over the four at α = 0.05
  (H6 left it when restated, later the same day). H1, H3 and H6 are **secondary**: each keeps its
  rule and direction and is decided at α = 0.05 on its own p, outside the correction, and
  reported as secondary.

Verdicts: ``supported``; ``not supported``; ``reversed`` (an interval wholly on the wrong side);
``unresolved`` (H3, H5, H6: an interval reaching above the upper margin without lying above it);
``not testable`` (H3: no shape measure varies); ``descriptive only`` (fewer than 6 chains in an
arm, or the development analysis).
"""

from __future__ import annotations

import json
from pathlib import Path

ALPHA = 0.05
#: The confirmatory family (Holm) and the secondary hypotheses (their own p), 21 November 2026;
#: H6 secondary since its restatement the same day.
CONFIRMATORY = ("H2", "H4", "H5", "H7")
SECONDARY = ("H1", "H3", "H6")
#: H3's measures (PLAN.md §2, §5): at the method, long, cognitive and cyclomatic complexity; at the
#: class, concentration, WMC and lack of cohesion. Each is fitted alone. Not slimmable and
#: junction are sinew measures, and fan-out and CBO measures of reach, reported apart.
SHAPES = ("s1_long", "s4_cognitive", "m_cyclomatic", "c_gini", "c_wmc", "c_lcom_star")


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


def h1(est: dict) -> dict:
    x = est.get("H1") or {}
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
    return {"p": max(c["p_greater"], m["p_greater"]),
            "reversed": c["irr_upper"] < 1 or m["irr_upper"] < 1,
            "conditions_met": c["irr_lower"] > 1 and m["irr_lower"] > 1, "detail": x}


def h3(est: dict) -> dict:
    b = est.get("H3") or {}
    measures = b.get("measures") or {}
    dropped = [k for k in SHAPES if k not in (b.get("kept") or [])]
    if any(not _ok(m) for m in measures.values()):
        return {"p": None, "verdict": "not estimable", "dropped": dropped, "detail": b}
    if not (b.get("testable") and measures):
        return {"p": None, "verdict": "not testable", "state": "not testable", "dropped": dropped,
                "detail": b}
    upper = b["margin"][1]
    if any(m.get("above", m["irr_lower"] > upper) for m in measures.values()):
        state = "against"           # a shape measure raises later intrusion beyond the margin
    elif all(m["irr_upper"] <= upper for m in measures.values()):
        state = "not above"
    else:
        state = "unresolved"
    # reported: the two-sided reading, as H3 stood until 17 November 2026
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
    if not (_ok(arm) and _ok(slope) and _ok(ic) and _ok(im)):
        return {"p": None, "verdict": "not estimable", "detail": x}
    amount = cond.get("amount") or {}
    w = (cond.get("wiring") or {}).get("verdict") or {}
    wiring_against = bool(w.get("growth_against")) or bool(w.get("concentration_against"))
    lower = arm["upper"] < 0 and slope["upper"] < 0 and ic["irr_upper"] < 1 and im["irr_upper"] < 1
    return {"p": max(arm["p_less"], slope["p_less"], ic["p_less"], im["p_less"]),
            "reversed": arm["lower"] > 0,
            "amount_in_band": amount.get("in_band"), "wiring_against": wiring_against,
            "conditions_met": lower and amount.get("in_band") is True and not wiring_against,
            "detail": {"model": x, "amount": amount, "wiring": w}}


def h5(est: dict) -> dict:
    x = est.get("H5") or {}
    states, ps = {}, []
    for lev in ("class",):           # the method level is reported (20 November 2026)
        b = x.get(lev) or {}
        if b.get("all_forced"):
            states[lev], p = "not above", 0.0
        elif not _ok(b) or "irr_upper" not in b:
            return {"p": None, "verdict": "not estimable", "detail": x}
        else:
            upper = x["margin"][1]
            states[lev] = ("against" if b["irr_lower"] > upper else
                           "not above" if b["irr_upper"] <= upper else "unresolved")
            p = b["p_upper"]
        ps.append(p)
    state = ("against" if "against" in states.values() else
             "not above" if all(v == "not above" for v in states.values()) else "unresolved")
    return {"p": max(ps), "state": state, "levels": states, "reversed": state == "against",
            "conditions_met": state == "not above", "detail": x}


def h6(est: dict) -> dict:
    x = est.get("H6") or {}
    fo = x.get("forced")
    if not _ok(fo) or "p_upper" not in fo:
        return {"p": None, "verdict": "not estimable", "detail": x}
    upper = (x.get("margin") or [0.8, 1.25])[1]
    state = ("against" if fo["irr_lower"] > upper else
             "not above" if fo["irr_upper"] <= upper else "unresolved")
    return {"p": fo["p_upper"], "state": state, "conditions_met": state == "not above",
            "detail": x}


def h7(est: dict) -> dict:
    x = est.get("H7") or {}
    fo = x.get("forced")
    if not _ok(fo):
        return {"p": None, "verdict": "not estimable", "detail": x}
    return {"p": fo["p_greater"], "reversed": fo["irr_upper"] < 1,
            "conditions_met": fo["irr_lower"] > 1, "detail": x}


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
        elif k in ("H3", "H5", "H6") and v.get("state") == "unresolved":
            v["verdict"] = "unresolved"
        else:
            v["verdict"] = "not supported"
    return {"alpha": ALPHA, "descriptive_only": bool(cond.get("descriptive_only")),
            "hypotheses": parts}


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

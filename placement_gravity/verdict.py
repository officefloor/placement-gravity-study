"""Step 4, the decision: each hypothesis's verdict from the R estimates and the conditions
(PLAN.md §2, §5). Every decision rule of the study is here.

- **H1** (the methods arm): the slope of the bystanders (PLAN.md §4.3a) on the checkpoint index
  above 0, over all runs and within a place: the class's bystanders within a class, the method's
  within a method. p = the largest of the three one-sided bootstrap p-values.
- **H2** (the methods arm): where code was bound to a class or a method, the rate ratio, per value
  that stood by there, of the later intrusions bound to what stood by, above 1 at the class and at
  the method (one-sided Wald; p = the larger of the two; PLAN.md §4.4).
- **H3**: every shape measure kept within the equivalence margin by two one-sided tests, on
  method-level intrusion, with the bindings and the bystanders in the model. p = the largest TOST p.
- **H4**: the function arm's bystanders fewer half-way through the stream, their slope on the
  checkpoint index flatter, and its bound code come back to less, at the class and at the method
  (p = the largest of the four one-sided p-values); the amount within its band; and neither wiring
  condition against.
- **Multiplicity**: Holm over H1 to H4 at α = 0.05.

Verdicts: ``supported``; ``not supported``; ``reversed`` (an interval wholly on the wrong side);
``unresolved`` (H3: an interval reaching outside the margin without lying outside it);
``not testable`` (H3: no shape measure varies); ``descriptive only`` (fewer than 6 chains in an
arm, or the development analysis).
"""

from __future__ import annotations

import json
from pathlib import Path

ALPHA = 0.05
SHAPES = ("s1_long", "s2_stuck", "s3_junction", "s4_cognitive", "s5_class_gini")


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
    if any(m["outside"] for m in measures.values()):
        state = "against"           # a shape measure carries information beyond the problem
    elif all(b["margin"][0] <= m["irr_lower"] and m["irr_upper"] <= b["margin"][1]
             for m in measures.values()):
        state = "within"
    else:
        state = "unresolved"
    return {"p": max(m["p_tost"] for m in measures.values()), "state": state, "dropped": dropped,
            "conditions_met": state == "within", "detail": b}


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


def decide(est: dict, cond: dict) -> dict:
    parts = {"H1": h1(est), "H2": h2(est), "H3": h3(est), "H4": h4(est, cond)}
    adjusted = holm({k: v["p"] for k, v in parts.items()})
    for k, v in parts.items():
        v["p_holm"] = adjusted[k]
        if cond.get("descriptive_only"):
            v["verdict"] = "descriptive only"
        elif "verdict" in v:
            continue
        elif v["p_holm"] is not None and v["p_holm"] <= ALPHA and v["conditions_met"]:
            v["verdict"] = "supported"
        elif v.get("reversed"):
            v["verdict"] = "reversed"
        elif k == "H3" and v.get("state") == "unresolved":
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

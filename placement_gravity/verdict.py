"""Step 4, the decision: each hypothesis's verdict from the R estimates and the conditions
(PLAN.md §2, §5). Every decision rule of the study is here.

- **H1** (the methods arm): the slope of the bystanders (PLAN.md §4.3a) on the checkpoint index
  above 0. p = its one-sided bootstrap p-value.
- **H2**: H2a (the rate ratio per tie above 1, one-sided Wald) and H2b (every shape measure kept
  within the equivalence bound by two one-sided tests). p = the larger of H2a's p and the largest
  TOST p. With no shape measure testable, H2 is read on H2a alone and says so.
- **H3**: the function arm's bystanders fewer half-way through the stream and their slope on the
  checkpoint index flatter (both one-sided bootstrap p-values; p = the larger), the amount within
  its band, and neither wiring condition against.
- **Multiplicity**: Holm over H1, H2 and H3 at α = 0.05.

Verdicts: ``supported``; ``not supported``; ``reversed`` (an interval wholly on the wrong side);
``unresolved`` (H2b: an interval reaching outside the bound without lying outside it);
``descriptive only`` (fewer than 6 chains in an arm, or the development analysis).
"""

from __future__ import annotations

import json
from pathlib import Path

ALPHA = 0.05


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
    b = x.get("cp")
    if not _ok(b):
        return {"p": None, "verdict": "not estimable", "detail": x}
    return {"p": b["p_greater"], "reversed": b["upper"] < 0,
            "conditions_met": b["lower"] > 0, "detail": x}


def h2(est: dict) -> dict:
    a = est.get("H2a") or {}
    b = est.get("H2b") or {}
    if not _ok(a):
        return {"p": None, "verdict": "not estimable", "detail": {"H2a": a, "H2b": b}}
    measures = b.get("measures") or {}
    bad = [k for k, m in measures.items() if not _ok(m)]
    testable = bool(b.get("testable")) and not bad and bool(measures)
    p_tost = max((m["p_tost"] for m in measures.values()), default=None) if testable else None
    h2a_ok = a["irr_lower"] > 1
    h2b_state = None
    if testable:
        if any(m["outside"] for m in measures.values()):
            h2b_state = "against"          # a shape measure carries information beyond the problem
        elif all(b["bound"][0] <= m["irr_lower"] and m["irr_upper"] <= b["bound"][1]
                 for m in measures.values()):
            h2b_state = "within"
        else:
            h2b_state = "unresolved"
    p = max(a["p_greater"], p_tost) if p_tost is not None else a["p_greater"]
    return {"p": p, "h2a_supported": h2a_ok, "h2a_reversed": a["irr_upper"] < 1,
            "h2b": h2b_state or "not testable", "h2b_dropped": [k for k in ("s1_long", "s2_stuck",
            "s3_junction", "s4_cognitive", "s5_class_gini") if k not in (b.get("kept") or [])],
            "conditions_met": h2a_ok and h2b_state == "within", "partial": not testable,
            "detail": {"H2a": a, "H2b": b}}


def h3(est: dict, cond: dict) -> dict:
    x = est.get("H3") or {}
    arm, slope = x.get("arm"), x.get("slope")
    if not (_ok(arm) and _ok(slope)):
        return {"p": None, "verdict": "not estimable", "detail": x}
    amount = cond.get("amount") or {}
    w = (cond.get("wiring") or {}).get("verdict") or {}
    wiring_against = bool(w.get("growth_against")) or bool(w.get("concentration_against"))
    lower = arm["upper"] < 0 and slope["upper"] < 0
    return {"p": max(arm["p_less"], slope["p_less"]),
            "reversed": arm["lower"] > 0,
            "amount_in_band": amount.get("in_band"), "wiring_against": wiring_against,
            "conditions_met": lower and amount.get("in_band") is True and not wiring_against,
            "detail": {"model": x, "amount": amount, "wiring": w}}


def decide(est: dict, cond: dict) -> dict:
    parts = {"H1": h1(est), "H2": h2(est), "H3": h3(est, cond)}
    adjusted = holm({k: v["p"] for k, v in parts.items()})
    for k, v in parts.items():
        v["p_holm"] = adjusted[k]
        if cond.get("descriptive_only"):
            v["verdict"] = "descriptive only"
        elif "verdict" in v:
            continue
        elif v["p_holm"] is not None and v["p_holm"] <= ALPHA and v["conditions_met"]:
            v["verdict"] = "supported" + (" (H2a only; H2b not testable)" if v.get("partial") else "")
        elif v.get("reversed") or v.get("h2a_reversed"):
            v["verdict"] = "reversed"
        elif k == "H2" and v.get("h2a_supported") and v.get("h2b") == "unresolved":
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

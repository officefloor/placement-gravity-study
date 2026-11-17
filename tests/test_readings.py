"""The readings reported beside the hypotheses (PLAN.md §5): choice at a checkpoint, formation and
review, on tables with known answers."""

import pytest

from placement_gravity import prepare, readings


def test_spearman():
    assert readings.spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert readings.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)
    assert readings.spearman([1, 2, 2, 4], [1, 3, 3, 9]) == pytest.approx(1.0)   # bindings share a rank
    assert readings.spearman([1, 1, 1], [1, 2, 3]) is None and readings.spearman([1, 2], [1, 2]) is None


def run(chain, cp, binding, replacement=False):
    return {"chain_id": chain, "cp": cp, "binding": binding, "replacement": str(replacement)}


def test_the_chains_bindings_so_far():
    rows = [run("c", 1, 2), run("c", 1, 0), run("c", 2, 4), run("c", 2, 9, replacement=True), run("c", 4, 0)]
    prior = readings.prior_binding_mean(rows)
    assert ("c", 1) not in prior                     # nothing before the first checkpoint
    assert prior[("c", 2)] == pytest.approx(1.0)     # (2 + 0) / 2
    assert prior[("c", 3)] == prior[("c", 4)] == pytest.approx(2.0)   # moved code is left out
    assert prior[("c", 5)] == pytest.approx(1.5)


def addition(arm, chain, cp, existing, bindings, share=None, largest=None, total=100):
    return {"arm": arm, "chain_id": chain, "cp": cp, "positions_added": 5, "hosts": 1,
            "hosts_existing": existing, "binding_method": bindings, "binding_class": 0,
            "share_in_existing": share, "amount_largest": largest, "amount_positions": total}


def host(arm, cp, name):
    return {"arm": arm, "cp": cp, "type": "T", "name": name, "net_added": 3, "replacement": "False"}


def test_choice_at_a_checkpoint():
    adds = [addition("spring", f"s{n}", 1, 1, 2) for n in range(3)]            # all the same: no choice
    adds += [addition("spring", "s0", 2, 1, 3), addition("spring", "s1", 2, 0, 0),
             addition("spring", "s2", 2, 0, 1)]                               # the chains differ
    hosts = [host("spring", 1, "create")] * 3 + [host("spring", 2, n) for n in ("create", "check", "audit")]
    rows = {r["cp"]: r for r in readings.choice(adds, hosts)}
    assert rows[1]["binding_sd"] == 0 and rows[1]["share_in_existing_host"] == 1 and rows[1]["distinct_hosts"] == 1
    assert rows[2]["binding_sd"] > 0 and rows[2]["distinct_hosts"] == 3
    assert rows[2]["share_in_existing_host"] == pytest.approx(1 / 3)
    s = readings.choice_summary(list(rows.values()))["spring"]
    assert s["checkpoints"] == 2 and s["no_choice"] == 1


def test_formation_where_it_ends():
    # five chains: the more a chain is bound in the first third (cp 1 of 3), the larger its largest method
    runs_, adds = [], []
    for n, (binding, largest) in enumerate([(0, 10), (1, 20), (2, 25), (3, 40), (4, 60)]):
        runs_ += [run(f"s{n}", 1, binding), run(f"s{n}", 3, 9 - binding)]              # later bindings do not count
        adds += [addition("spring", f"s{n}", 3, 1, 0, largest=largest)]
    f = readings.formation_end(runs_, adds, 3, resamples=300)["spring"]
    assert f["chains"] == 5 and f["rho"] == pytest.approx(1.0) and f["interval"][1] == pytest.approx(1.0)


def test_review_changes_the_placement_where_the_bindings_are_few():
    # bindings rise over the checkpoints in just-solve; the reviewed chains differ at the low-binding ones
    p_runs, p_adds, r_adds = [], [], []
    for n in range(4):
        for cp in range(1, 7):
            p_runs.append({"chain_id": f"spring/p/{n}", "cp": cp, "binding": cp, "replacement": "False"})
            p_adds.append(addition("spring", f"spring/p/{n}", cp, 1, cp, share=0.9))
            r_adds.append(addition("spring", f"spring/r/{n}", cp, 1, cp, share=0.9 - 0.8 / cp))
    r = readings.review(p_runs, p_adds, r_adds, resamples=200)["spring"]
    assert r["rho"] == pytest.approx(-1.0) and not r["against"] and r["checkpoints"] == 6
    same = readings.review(p_runs, p_adds, [{**a, "share_in_existing": 0.9 - 0.1 * a["cp"]} for a in r_adds],
                           resamples=200)["spring"]
    assert same["against"]                           # the change does not fall with the bindings


def test_the_amount_is_read_on_what_was_added():
    adds = [{"chain_id": f"{arm}{n}", "arm": arm, "cp": cp, "amount_positions": base + 10 * cp + extra,
             "amount_added": 10 * cp + extra}
            for arm, base, extra in (("spring", 900, 0), ("officefloor", 700, 10))
            for n in range(2) for cp in (1, 50)]
    a = prepare.amount(adds, resamples=200)
    assert a["ratio"] == pytest.approx(510 / 500) and a["in_band"]            # the amount added
    assert a["ratio_total"] == pytest.approx(1210 / 1400)                     # the totals, beside it


def test_bystanders_are_gathered_per_run_and_summarised():
    def r(arm, cp, by, need, replacement=False, new=False):
        return {"chain_id": f"{arm}/c", "arm": arm, "cp": cp, "host_new": str(new), "need": need,
                "replacement": str(replacement), "bystanders": by, "by_method": 1, "by_class": by - 1,
                "bystanders_no_injected": by, "bystanders_no_constants": by - 1}
    rows = [r("spring", 1, 4, 1), r("spring", 3, 10, 2, new=True), r("spring", 3, 99, 9, replacement=True),
            r("officefloor", 2, 1, 1)]
    rows.append(r("spring", 2, 50, 0))                        # needs nothing that was there: free
    by = prepare.by_rows(rows)
    assert len(by) == 4 and by[1]["host_new"] is True         # moved code is left out; new hosts stay
    cap = prepare.capture_rows([{"chain_id": "spring/c", "arm": "spring", "cp": 1, "share_in_existing": "0.5",
                                 "heaviest_class": "6", "fields_added": "2"},
                                {"chain_id": "spring/c", "arm": "spring", "cp": 2, "share_in_existing": "",
                                 "heaviest_class": "6", "fields_added": "0"}])
    assert len(cap) == 1                                      # an empty addition has no share to read
    s = readings.bystander_summary(by, cap, 3)
    assert s["spring"]["bystanders"] == 7 and s["spring"]["thirds"] == [4, None, 10]   # the free run apart
    assert s["spring"]["pulled"] == 2 and s["spring"]["share_free"] == pytest.approx(1 / 3)
    assert s["spring"]["fields_added_per_addition"] == 2 and s["officefloor"]["need"] == 1

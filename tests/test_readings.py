"""The readings reported beside the hypotheses (PLAN.md §5): choice at a checkpoint, formation and
review, on tables with known answers."""

import pytest

from placement_gravity import prepare, readings, tables


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


def test_a_checkpoint_is_split_into_logic_and_organisation():
    """PLAN.md 4.9: logic and organisation in bodies from the hosts; declarations as the diff's code
    lines less imports and less the positions added in bodies; the parameters of new methods."""
    def host(added, organisation=0, moved=0, new=False, params=0):
        return {"added": added, "net_added": added - moved, "organisation": organisation,
                "replacement": False, "host_new": new, "params": params, "injected": injected}
    injected = False
    hosts = [host(10), host(4, organisation=1, new=True, params=3), host(6, moved=6), host(1, organisation=1, new=True, params=1)]
    injected = True
    hosts.append(host(5, new=True, params=2))          # a wired function: its parameters are injected
    s = tables.organisation_split({"java": 45, "imports": 5, "wiring": 7}, hosts)
    assert (s["logic_added"], s["organisation_added"], s["params_new_methods"]) == (18, 2, 6)
    # the accessor's parameter is organisation; the wired function's are injected, not handed by a caller
    assert (s["params_called_methods"], s["params_wired_functions"]) == (3, 2)
    assert (s["new_called_methods"], s["new_wired_functions"]) == (1, 1)
    # where the logic landed: the existing method's 10, the new called method's 3, the wired function's 5
    assert (s["logic_existing_methods"], s["logic_new_called_methods"], s["logic_new_wired_functions"],
            s["existing_methods_edited"]) == (10, 3, 5, 1)
    assert (s["declaration_lines_added"], s["import_lines_added"], s["wiring_lines_added"]) == (14, 5, 7)
    assert tables.organisation_split(None, hosts)["declaration_lines_added"] is None      # a history
    rows = prepare.split_rows([{"chain_id": "c", "arm": "officefloor", "cp": "2", "noop": "False", **s,
                                "birth_binding": 2, "method_values_added": 5, "fields_added": 0},
                               {"chain_id": "c", "arm": "officefloor", "cp": "3", "noop": "False",
                                "declaration_lines_added": ""}])
    assert len(rows) == 1 and rows[0]["organisation_all"] == 2 + 14 + 7
    summary = prepare.split_summary(rows, 60)["officefloor"]
    assert summary["organisation_share"] == 23 / 41 and summary["thirds"]["1"]["logic_added"] == 18


def test_the_diff_counts_code_lines_not_blank_lines_brackets_or_comments(tmp_path):
    import subprocess
    from placement_gravity import chain

    def git(*a):
        subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=t", "-c", "user.email=t@t", *a],
                       check=True, capture_output=True)
    git("init", "-q")
    src = tmp_path / "src/main/java/a"
    wire = tmp_path / "src/main/resources/officefloor"
    src.mkdir(parents=True)
    wire.mkdir(parents=True)
    (src / "A.java").write_text("package a;\nclass A {\n}\n")
    git("add", "-A")
    git("commit", "-q", "-m", "base")
    (src / "A.java").write_text("package a;\nimport java.util.List;\n\n// a comment\nclass A {\n"
                                "    private int n;\n    int get() {\n        return n;\n    }\n}\n")
    (wire / "flow.yml").write_text("# flows\nstep:\n  class: a.A\n\n  next: done\n")
    git("add", "-A")
    git("commit", "-q", "-m", "change")
    n = chain.lines_added(tmp_path, "HEAD~1", "HEAD", "src/main/java/", "src/main/resources/officefloor/")
    # the import, the field, the signature and the return; not the blank, the comment or the bracket
    assert n == {"java": 4, "imports": 1, "wiring": 3}

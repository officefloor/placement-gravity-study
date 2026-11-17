"""The wiring conditions of H4 (PLAN.md §4.5): the reader, and the growth and concentration checks."""

from placement_gravity import chain, wiring

FLOW = """composition:
  authorize: "hasRole('ADMIN')"   # not an edge

first:
  class: a.First
  outputs:
    proceed: second
    stop: done

second:
  class: a.Second
  next: done
"""
ESCALATION = """# only a comment
handle:
  class: a.Handler
"""


def test_reader_counts_nodes_edges_and_lines():
    w = chain.parse_wiring({"rest/a.POST.yml": FLOW, "escalation/E.yml": ESCALATION})
    assert (w["files"], w["nodes"], w["edges"]) == (2, 3, 3)
    assert w["lines"] == 10 + 2 and w["largest_file"] == "rest/a.POST.yml" and w["largest_lines"] == 10


def test_reader_of_no_wiring():
    assert chain.parse_wiring({}) == {"files": 0, "nodes": 0, "edges": 0, "lines": 0,
                                      "largest_file": None, "largest_lines": 0}


def rows(chain_name, added, largest=0.25):
    return [{"arm": "officefloor", "chain": chain_name, "cp": i + 1, "wiring_edges_added": e,
             "wiring_files": 4, "wiring_lines": 40, "wiring_largest_share": largest}
            for i, e in enumerate(added)]


def test_growth_is_the_slope_of_edges_added_over_checkpoints():
    c = wiring.chain_checks(rows("c1", [0, 1, 2, 3]))
    assert c["growth_slope"] == 1.0 and c["edges_added"] == 6
    assert wiring.chain_checks(rows("c2", [2, 2, 2]))["growth_slope"] == 0.0


def test_growth_counts_against_only_when_the_interval_is_above_zero():
    rising = [wiring.chain_checks(rows(f"c{i}", [0, 1, 2, 3])) for i in range(5)]
    v = wiring.verdict(rising, resamples=200)
    assert v["growth_interval"] == [1.0, 1.0] and v["growth_against"]
    mixed = [wiring.chain_checks(rows("a", [0, 1, 2])), wiring.chain_checks(rows("b", [2, 1, 0]))]
    v = wiring.verdict(mixed, resamples=200)
    assert v["growth_interval"][0] < 0 < v["growth_interval"][1] and not v["growth_against"]


def test_concentration_counts_against_over_half():
    held = [wiring.chain_checks(rows(f"c{i}", [1, 1], largest=0.6)) for i in range(3)]
    assert wiring.verdict(held, resamples=200)["concentration_against"]
    spread = [wiring.chain_checks(rows(f"c{i}", [1, 1], largest=0.2)) for i in range(3)]
    assert not wiring.verdict(spread, resamples=200)["concentration_against"]


def test_one_chain_reads_no_interval():
    v = wiring.verdict([wiring.chain_checks(rows("c", [0, 1, 2]))])
    assert v["growth_interval"] is None and v["growth_against"] is None
    assert v["concentration_against"] is False


def test_the_bootstrap_is_fixed_by_its_seed():
    cs = [wiring.chain_checks(rows(f"c{i}", [0, i, 2 * i])) for i in range(4)]
    assert wiring.verdict(cs, resamples=500) == wiring.verdict(cs, resamples=500)

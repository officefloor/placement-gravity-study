"""The ui stream's declared crossings (acceptance/DENSITY.md), read on a fixture in its format, and
the three-way split of later changes in the outcomes (PLAN.md §4.4)."""

from pathlib import Path

import pytest

from placement_gravity import tables

FX = Path(__file__).parent / "fixtures" / "stream"


def test_each_rule_maps_to_the_checkpoint_that_introduces_it():
    s = tables.stream(FX / "checkpoints.yaml", FX / "DENSITY.md")
    assert s[2]["rules"] == ["names"] and s[2]["crosses"] == []
    assert s[4]["rules"] == ["rate_dated"] and s[4]["crosses"] == [2, 3]
    assert s[4]["mutates"] == [3] and s[4]["type"] == "mutative"
    assert s[6]["rules"] == ["conflict", "half_even"] and s[6]["crosses"] == [2, 3, 4]
    assert s[1]["crosses"] == [] and s[5]["crosses"] == []   # introduces no rule


def test_without_density_the_stream_declares_no_crossings():
    s = tables.stream(FX / "checkpoints.yaml")
    assert all(x["crosses"] == [] and x["rules"] == [] for x in s.values())


@pytest.mark.parametrize("cell, error", [
    ("late: 2 (names)", "declares degree 2"),
    ("late: 1 (unknown)", "not introduced earlier"),
    ("late 1 names", "unreadable"),
])
def test_a_malformed_or_inconsistent_entry_is_refused(cell, error):
    md = ("| 2 | A | 0 | 0 | 0 | 0 | 0 |  | names: 0 () |\n"
          f"| 3 | A | 1 | 1 | 1 | 0 | 1 | 1.00 | {cell} |\n")
    with pytest.raises(ValueError, match=error):
        tables.crossings(md)


def test_a_rule_introduced_twice_is_refused():
    md = ("| 2 | A | 0 | 0 | 0 | 0 | 0 |  | names: 0 () |\n"
          "| 3 | A | 1 | 1 | 0 | 0 | 1 | 0.00 | names: 0 () |\n")
    with pytest.raises(ValueError, match="introduced at cp2 and cp3"):
        tables.crossings(md)


def test_later_touches_split_into_declared_crossed_and_intrusion():
    s = tables.stream(FX / "checkpoints.yaml", FX / "DENSITY.md")
    host = {"type": "A", "name": "f", "before_type": None, "before_name": None, "removed": 0,
            "replacement": False, "pre_positions": 0, "tie_method": 0, "tie_class": 0, "tie": 0}
    hosts = [{**host, "cp": 3, "net_added": 2, "host_new": True}]
    # later checkpoints touching the host: 4 mutates 3; 6 crosses 3; 5 does neither
    hosts += [{**host, "cp": j, "net_added": 1, "host_new": False, "before_type": "A",
               "before_name": "f"} for j in (4, 5, 6)]
    [row] = [r for r in tables.outcome_rows("x", "c", hosts, s) if r["cp"] == 3]
    assert (row["later_touches"], row["declared"], row["crossed"], row["intrusion"]) == (3, 1, 1, 1)

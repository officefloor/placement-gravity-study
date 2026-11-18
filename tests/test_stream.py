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
            "replacement": False, "pre_positions": 0, "binding_method": 0, "binding_class": 0, "binding": 1}
    hosts = [{**host, "cp": 3, "net_added": 2, "host_new": True}]
    # later checkpoints touching the host: 4 mutates 3; 6 crosses 3; 5 does neither
    hosts += [{**host, "cp": j, "net_added": 1, "host_new": False, "before_type": "A",
               "before_name": "f"} for j in (4, 5, 6)]
    [row] = [r for r in tables.outcome_rows("x", "c", hosts, s) if r["cp"] == 3]
    assert (row["later_touches"], row["declared"], row["crossed"], row["intrusion_method"]) == (3, 1, 1, 1)
    # the class level: the same three later checkpoints change class A
    assert (row["class_touches"], row["class_declared"], row["class_crossed"], row["intrusion_class"]) == (3, 1, 1, 1)
    # a later change that reuses nothing that was there (a field and its accessor) is not drawn in
    unbound = [h if h["cp"] != 5 else {**h, "binding": 0} for h in hosts]
    [row] = [r for r in tables.outcome_rows("x", "c", unbound, s) if r["cp"] == 3]
    assert row["intrusion_method"] == 0 and row["intrusion_class"] == 0
    assert row["intrusion_method_any"] == 1 and row["intrusion_class_any"] == 1
    # and a problem that was not bound to the place is marked as such: intrusion does not apply to it
    free = [h if h["cp"] != 3 else {**h, "binding": 0} for h in hosts]
    [row] = [r for r in tables.outcome_rows("x", "c", free, s) if r["cp"] == 3]
    assert row["bound"] is False


def test_later_code_bound_to_what_stood_by_is_drawn_in():
    """H2 (PLAN.md 4.4): cp3's code in A.f used `id` and left `owner` and the fields `LIMIT` and
    `repo` standing by. cp5 comes back to f and uses `owner`; cp7 goes to another method of A, g,
    and uses `LIMIT`; cp8 comes back to f and uses only `id`, which did not stand by."""
    host = {"type": "A", "name": "f", "before_type": "A", "before_name": "f", "removed": 0,
            "replacement": False, "pre_positions": 5, "binding_method": 1, "binding_class": 0, "binding": 1,
            "net_added": 2, "host_new": False, "need_class_values": "", "by_class_values": "",
            "need_method_values": "", "by_method_values": ""}
    hosts = [{**host, "cp": 3, "need_method_values": "id", "by_method_values": "owner",
              "by_class_values": "LIMIT repo"},
             {**host, "cp": 5, "need_method_values": "owner", "by_class_values": "LIMIT repo"},
             {**host, "cp": 7, "name": "g", "before_name": "g", "need_class_values": "LIMIT"},
             {**host, "cp": 8, "need_method_values": "id", "by_method_values": "owner"}]
    rows = {(r["cp"], r["name"]): r for r in tables.outcome_rows("x", "c", hosts, {})}
    r = rows[(3, "f")]
    assert (r["bystanders_method"], r["bystanders_class"]) == (1, 2)
    assert (r["intrusion_method"], r["drawn_method"]) == (2, 1)      # cp5 and cp8 came back; cp5 for owner
    assert (r["intrusion_class"], r["drawn_class"]) == (3, 1)        # cp7, in g, for LIMIT
    # a value used at the placement did not stand by, so later use of it is not drawn by a bystander
    assert rows[(5, "f")]["drawn_method"] == 0 and rows[(5, "f")]["drawn_class"] == 1
    # later code that is not bound there does not count, whatever it names
    unbound = [h if h["cp"] != 5 else {**h, "binding": 0} for h in hosts]
    assert {(r["cp"], r["name"]): r for r in tables.outcome_rows("x", "c", unbound, {})}[(3, "f")]["drawn_method"] == 0


def test_later_code_bound_to_what_a_change_introduced():
    """Introduced (PLAN.md 4.3b): cp3 adds a method f to A, with a parameter `city`, and a field
    `cap` to A. It used `repo` and left `LIMIT` standing by. cp5 comes back to f and uses `city`;
    cp7 goes to another method of A and uses `cap`; cp8 uses `LIMIT`."""
    host = {"type": "A", "name": "f", "before_type": "A", "before_name": "f", "removed": 0,
            "replacement": False, "pre_positions": 5, "binding_method": 0, "binding_class": 1, "binding": 1,
            "net_added": 2, "host_new": False, "need_class_values": "", "by_class_values": "",
            "need_method_values": "", "by_method_values": ""}
    hosts = [{**host, "cp": 3, "host_new": True, "before_type": None, "before_name": None,
              "need_class_values": "repo", "by_class_values": "LIMIT",
              "introduced_method_values": "city n", "introduced_class_values": "cap"},
             {**host, "cp": 5, "need_method_values": "city"},
             {**host, "cp": 7, "name": "g", "before_name": "g", "need_class_values": "cap"},
             {**host, "cp": 8, "name": "g", "before_name": "g", "need_class_values": "LIMIT"}]
    r = {(r["cp"], r["name"]): r for r in tables.outcome_rows("x", "c", hosts, {})}[(3, "f")]
    # a new method: nothing stood by in it, so by what stood by it can only read nought
    assert (r["bystanders_method"], r["drawn_method"]) == (0, 0)
    assert (r["introduced_method"], r["drawn_method_introduced"]) == (2, 1)          # cp5, for city
    assert (r["left_method"], r["drawn_method_left"]) == (2, 1)
    assert (r["introduced_class"], r["drawn_class_introduced"]) == (1, 1)            # cp7, for cap
    assert (r["bystanders_class"], r["drawn_class"]) == (1, 1)                       # cp8, for LIMIT
    assert (r["left_class"], r["drawn_class_left"], r["intrusion_class"]) == (2, 2, 3)
    # core and periphery (H2): cp3 was bound to `repo` (its core at the class); LIMIT and cap are
    # the periphery there. None of the later code uses repo; one use each of cap and LIMIT.
    assert (r["core_class"], r["uses_core_class"]) == (1, 0)
    assert (r["periphery_class"], r["uses_periphery_class"]) == (2, 2)
    # a new method has no core of its own: nothing was there to be bound to
    assert (r["core_method"], r["periphery_method"], r["uses_periphery_method"]) == (0, 2, 1)


def test_the_core_is_what_code_was_bound_to_and_uses_are_counted_per_value():
    """cp3's code in A.f was bound to `id` and `owner` (its core) and left `flag` standing by. cp5
    comes back and uses id and owner (two uses of the core); cp6 uses flag; cp7 mutates cp3's rule,
    so its use of id is declared and does not count."""
    host = {"type": "A", "name": "f", "before_type": "A", "before_name": "f", "removed": 0,
            "replacement": False, "pre_positions": 5, "binding_method": 1, "binding_class": 0, "binding": 1,
            "net_added": 2, "host_new": False, "need_class_values": "", "by_class_values": "",
            "need_method_values": "", "by_method_values": ""}
    hosts = [{**host, "cp": 3, "need_method_values": "id owner", "by_method_values": "flag"},
             {**host, "cp": 5, "need_method_values": "id owner"},
             {**host, "cp": 6, "need_method_values": "flag"},
             {**host, "cp": 7, "need_method_values": "id"}]
    streamed = {7: {"mutates": [3], "crosses": []}}
    r = {r["cp"]: r for r in tables.outcome_rows("x", "c", hosts, streamed)}[3]
    assert (r["core_method"], r["periphery_method"]) == (2, 1)
    assert (r["uses_core_method"], r["uses_periphery_method"]) == (2, 1)
    assert r["intrusion_method"] == 2


def test_what_stood_by_is_read_over_the_runs_of_one_host():
    runs = [{"vis_method": ["a", "b"], "need_method": ["a"], "need_field_names": [], "by_field_names": ["X", "Y"]},
            {"vis_method": ["a", "b", "c"], "need_method": ["b"], "need_field_names": ["X"], "by_field_names": ["Y"]}]
    assert tables.standing(runs) == {"need_method_values": "a b", "by_method_values": "c",
                                     "need_class_values": "X", "by_class_values": "Y"}

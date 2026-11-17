"""Where added code lands among the places it could have gone (PLAN.md 5, reported)."""

import pytest

from placement_gravity import places


def shape(unit, type_, sig, positions, cognitive, params, locals_, fields):
    return {"unit": unit, "path": f"{type_}.java", "type": type_, "signature": sig,
            "positions": positions, "cognitive": cognitive, "in": params, "locals": locals_,
            "class_held": fields}


# before cp05: a heavy controller (two methods, six fields) and a light mapper (one method, no field)
SHAPE = [shape("cp05", "Controller", "add(Owner)", 40, 9, 1, 5, 6),
         shape("cp05", "Controller", "get(int)", 4, 0, 1, 0, 6),
         shape("cp05", "Mapper", "map(Owner)", 6, 1, 1, 1, 0)]


def host(type_, sig, binding, host_new=False, class_new=False):
    return {"cp": 5, "type": type_, "signature": sig, "net_added": 3, "replacement": False,
            "binding": binding, "host_new": host_new, "class_new": class_new,
            "before_path": None if host_new else f"{type_}.java",
            "before_type": None if host_new else type_, "before_signature": None if host_new else sig}


def test_a_place_is_ranked_among_the_candidates_of_its_checkpoint():
    assert places.rank(9, [9, 0, 1]) == pytest.approx(2.5 / 3)     # two below, itself at half
    assert places.rank(0, [0, 0, 5]) == pytest.approx(1 / 3)       # ties share the middle
    assert places.rank(1, []) is None


def test_landings_carry_their_destination_and_the_rank_of_the_place():
    hosts = [host("Controller", "add(Owner)", 2),                  # bound, into the heavy method
             host("Mapper", "extra()", 0, host_new=True),          # unbound, a new method in the light class
             host("Rule", "check()", 0, host_new=True, class_new=True)]   # unbound, a new class
    a, b, c = places.landings("spring", "c", hosts, SHAPE)
    assert (a["bound"], a["destination"]) == (True, "existing method")
    assert a["width"] == 12 and a["width_method"] == 6             # 1 parameter, 5 locals, 6 fields
    assert a["rank_cognitive"] == pytest.approx(2.5 / 3) and a["rank_width"] == pytest.approx(2.5 / 3)
    assert (a["class_positions"], a["class_cognitive"], a["class_fields"]) == (44, 9, 6)
    assert a["rank_class_fields"] == pytest.approx(0.75)           # the heavier of two classes
    assert (b["bound"], b["destination"]) == (False, "new method")
    assert b["rank_cognitive"] is None and b["rank_class_fields"] == pytest.approx(0.25)
    assert c["destination"] == "new class" and c["rank_class_positions"] is None
    s = places.summary([a, b, c])["spring"]
    assert s["bound"]["existing method"] == 1 and s["unbound"]["new class"] == 0.5
    assert s["unbound"]["rank_class_fields"] == pytest.approx(0.25) and s["unbound"]["n_rank_cognitive"] == 0

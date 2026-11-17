"""The literature's shape measures on the shape fixture tree (PLAN.md 4.7a). Needs the pinned
tools of setup.sh (CK, PMD); jscpd is optional."""

from pathlib import Path

import pytest

from placement_gravity import literature, shape

TREE = Path(__file__).parent / "fixtures" / "shape" / "tree"

pytestmark = pytest.mark.skipif(not (literature.CK_JAR.is_file() and literature.PMD_BIN.is_file()),
                                reason="CK and PMD are installed by setup.sh")


@pytest.fixture(scope="module")
def methods(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("lit")
    (tmp / "l.tsv").write_text(f"cp03\t{TREE.resolve()}\tWired\n")
    records = shape.complete(shape.run(tmp / "l.tsv", tmp / "o.jsonl"), {"cp03": TREE.resolve()})
    literature.attach(records, {"cp03": TREE.resolve()})
    return {(r["type"], r["name"]): r for r in records}


def test_method_measures_are_joined_by_file_and_line(methods):
    scan, check = methods[("Orders", "scan")], methods[("Orders", "check")]
    assert (scan["m_cyclomatic"], scan["m_npath"], scan["m_nesting"]) == (12, 21, 2)
    assert (check["m_cyclomatic"], check["m_npath"], check["m_nesting"]) == (2, 2, 1)
    assert methods[("Orders", "place")]["m_fanout"] == 3
    assert scan["m_halstead"] > check["m_halstead"] > 0 and scan["m_mi"] < check["m_mi"]


def test_class_measures_are_the_same_for_every_method_of_the_class(methods):
    orders = [r for (t, _), r in methods.items() if t == "Orders"]
    assert {r["c_wmc"] for r in orders} == {17} and {r["c_cbo"] for r in orders} == {2}
    assert orders[0]["c_tcc"] == pytest.approx(0.6) and orders[0]["c_god_class"] is False
    assert methods[("Wired", "service")]["c_wmc"] == 2


def test_halstead_volume_and_the_maintainability_index():
    assert literature.halstead("a = a + 1;") == pytest.approx(6 * 2.3219, abs=0.01)   # 6 tokens, 5 distinct
    assert literature.halstead("// only a comment") == 0
    assert literature.maintainability(100, 2, 10) == pytest.approx(171 - 5.2 * 4.6052 - 0.46 - 16.2 * 2.3026, abs=0.01)
    assert literature.maintainability(0, 1, 5) is None


def test_a_host_carries_its_method_and_class_measures(methods):
    idx, cls = shape.index(list(methods.values())), shape.class_index(list(methods.values()))
    host = {"cp": 3, "type": "Orders", "host_new": False, "class_new": False,
            "before_path": "Orders.java", "before_type": "Orders", "before_signature": "scan(int[])"}
    row = shape.host_shape(host, idx, cls)
    if row["shape_found"]:
        assert row["m_cyclomatic"] == 12 and row["c_wmc"] == 17
    # a new method of a class that existed has the class's measures and no method measures
    new = shape.host_shape({**host, "host_new": True}, idx, cls)
    assert new["m_cyclomatic"] is None and new["c_wmc"] == 17
    assert shape.host_shape({**host, "host_new": True, "class_new": True}, idx, cls)["c_wmc"] is None

"""The shape competitors of H6 (PLAN.md §4.7) on a fixture tree with known answers
(tests/fixtures/shape/tree), and their join to a host's version at k − 1."""

from pathlib import Path

import pytest

from placement_gravity import shape, tables

TREE = Path(__file__).parent / "fixtures" / "shape" / "tree"


@pytest.fixture(scope="module")
def methods(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("shape")
    (tmp / "l.tsv").write_text(f"cp03\t{TREE.resolve()}\tWired\n")
    records = shape.run(tmp / "l.tsv", tmp / "o.jsonl")
    assert not [r for r in records if r["kind"] == "problem"]
    return {(r["type"], r["name"]): r for r in shape.complete(records, {"cp03": TREE.resolve()})}


def test_s1_long_is_sinewslims_code_lines_at_its_trigger(methods):
    assert methods[("Orders", "report")]["length"] == 31 and methods[("Orders", "report")]["s1_long"]
    assert not methods[("Orders", "place")]["s1_long"]


def test_s2_reads_sinewslims_conventional_assessment(methods):
    report, scan = methods[("Orders", "report")], methods[("Orders", "scan")]
    assert report["status"] == "slimmable" and not report["s2_stuck"]
    assert scan["status"] == "not_slimmable" and scan["obstacle"] == "jumps"
    assert scan["s2_stuck"] and scan["s2_not_slimmable"]
    assert methods[("Orders", "check")]["status"] == "under_cap"


def test_s3_junction_hands_on_more_than_it_receives(methods):
    place = methods[("Orders", "place")]
    # check(o, 1) and price(o, 2, 3): five arguments; r.run() matches the anonymous class's run()
    # lexically (a known limit), with no arguments
    assert (place["in"], place["out"], place["calls"]) == (1, 5, 3)
    assert place["s3_d"] == 4 and place["s3_junction"]
    assert methods[("Orders", "price")]["s3_d"] == -3


def test_s3_a_call_in_an_anonymous_class_belongs_to_its_own_method(methods):
    run = methods[("Orders.new Runnable", "run")]
    assert (run["in"], run["out"], run["calls"]) == (0, 2, 1)


def test_s3_reads_a_wired_function_conventionally(methods):
    service, helper = methods[("Wired", "service")], methods[("Wired", "helper")]
    # every parameter is in, as for an ordinary method: receives two, hands on one
    assert service["injected"] and service["in"] == 2 and service["out"] == 1
    assert service["s3_d"] == -1 and not service["s3_junction"]
    assert not helper["injected"] and helper["in"] == helper["in_injection_aware"] == 1


def test_s3_injection_aware_reading_makes_any_call_of_a_wired_function_a_junction(methods):
    service = methods[("Wired", "service")]
    assert service["in_injection_aware"] == 0
    assert service["s3_d_injection_aware"] == 1 and service["s3_junction_injection_aware"]


def test_s4_cognitive_by_the_complexity_concentration_extractor(methods):
    # for: 1; eight ifs nested once: 2 each; the late if: 2; the ternary: 1
    assert methods[("Orders", "scan")]["cognitive"] == 20
    assert methods[("Orders", "check")]["cognitive"] == 1


def test_s4_outlier_by_modified_z_within_the_checkpoint(methods):
    outliers = [k for k, r in methods.items() if r["s4_outlier"]]
    assert outliers == [("Orders", "scan")]
    assert methods[("Orders", "scan")]["s4_z"] >= 3.5


def test_s5_class_gini_over_its_methods_positions(methods):
    expected = tables.gini([5, 2, 1, 29, 33])
    assert methods[("Orders", "scan")]["s5_class_gini"] == round(expected, 4)
    assert methods[("Orders", "scan")]["s5_class_positions"] == 70
    assert methods[("Wired", "helper")]["s5_class_gini"] == 0.0


def test_host_is_read_at_its_version_before_the_addition(methods):
    shaped = shape.index(list(methods.values()))
    existing = {"cp": 3, "host_new": False, "before_path": "a/Orders.java",
                "before_type": "Orders", "before_signature": "scan(List<String>)"}
    s = shape.host_shape(existing, shaped)
    assert s["shape_found"] and s["s2_stuck"] and s["s4_outlier"] and s["s4_cognitive"] == 20
    new = shape.host_shape({**existing, "host_new": True}, shaped)
    assert new["shape_found"] is None and new["s1_long"] is None
    lost = shape.host_shape({**existing, "before_signature": "gone()"}, shaped)
    assert lost["shape_found"] is False


def test_series_counts_and_junction_share(methods):
    [row] = shape.series_rows("a", "c", list(methods.values()))
    assert (row["methods"], row["long"], row["stuck"], row["junctions"], row["outliers"]) == (8, 2, 1, 2, 1)
    assert row["junctions_injection_aware"] == 3
    assert row["cognitive"] == 21 and row["junction_share"] == 0.0

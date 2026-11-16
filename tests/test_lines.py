"""Following a problem's own lines (PLAN.md §4.4) on a method with a known history
(tests/fixtures/lines/v0 … v4), through the instrument's line facts."""

import json
import subprocess
from pathlib import Path

import pytest

from placement_gravity import chain, lines, tables

FX = Path(__file__).parent / "fixtures" / "lines"
SIG = "create(String, int)"


@pytest.fixture(scope="module")
def records(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("lines")
    rows = [f"cp{k:02d}\tOwners.java\t{FX / f'v{k - 1}' / 'Owners.java'}\t{FX / f'v{k}' / 'Owners.java'}"
            for k in range(1, 5)]
    (tmp / "m.tsv").write_text("\n".join(rows) + "\n")
    subprocess.run(["java", "-cp", chain.CLASSPATH, "Pull", str(tmp / "m.tsv"), "-", str(tmp / "o.jsonl")],
                   check=True)
    out = [json.loads(l) for l in (tmp / "o.jsonl").read_text().splitlines()]
    assert all(r["kind"] != "problem" for r in out)
    return out


def test_the_instrument_gives_the_line_facts(records):
    r = next(r for r in records if r["unit"] == "cp01")
    # v1: the first line and the return are kept; three logic lines are added between them
    assert r["pair"] == [0, -1, -1, -1, 1] and r["kinds"] == [-1, 0, 0, 0, -1]
    assert len(r["hash"]) == 5 and len(r["before_hash"]) == 2


def test_a_problems_own_lines_are_followed(records):
    f = lines.follow(records, {("Owners.java", "Owners", SIG), ("Owners.java", "Owners", "checkName(String)")})
    one, two, three = (f[(k, "Owners", SIG)] for k in (1, 2, 3))
    # cp1 placed the age check and the sum; cp2 inserted between them; cp3 added after them all
    # (not between: no touch); cp4 edited cp1's sum
    assert one["placed"] == 3 and one["touched"] == {2, 4}
    # cp2's name check: cp3 did not touch it; cp4 moved it out (extract method), which is not a touch
    assert two["placed"] == 2 and two["touched"] == set()
    assert two["present"] == 2 and two["lost"] == 0     # carried to checkName with its owner
    assert three["placed"] == 1 and three["touched"] == set()
    # cp4's own: the call it added and the line it edited
    assert f[(4, "Owners", SIG)]["placed"] == 2


def test_an_insertion_outside_a_problems_span_is_host_level_only(records):
    """cp3 changed the host cp2's code is in, without touching cp2's lines: host-level intrusion,
    not intrusion on the problem's own lines."""
    hosts = [{"cp": int(r["unit"][2:]), "type": r["type"], "name": r["name"], "signature": r["signature"],
              "before_type": r.get("before_type"), "before_name": r.get("before_name"),
              "host_new": r["host_new"], "pre_positions": r["pre_positions"],
              "net_added": r["added"] - r["moved_rm"] - r["moved_text"], "removed": r["removed"],
              "replacement": False, "tie_method": 0, "tie_class": 0, "tie": 0}
             for r in records if r["kind"] == "host"]
    streamed = {k: {"mutates": [], "crosses": []} for k in range(1, 5)}
    rows = {(r["cp"], r["name"]): r for r in
            tables.outcome_rows("x", "c", hosts, streamed, None, lines.follow(records))}
    two = rows[(2, "create")]
    assert two["intrusion_host"] == 2 and two["intrusion"] == 0
    assert rows[(1, "create")]["intrusion"] == 2 and rows[(1, "create")]["own_lines"] == 3


def test_a_lost_host_is_counted_lost(records):
    f = lines.follow(records, {("Owners.java", "Owners", SIG)})      # checkName not in the last tree
    assert f[(2, "Owners", SIG)]["lost"] == 2

"""Following a problem's own lines (PLAN.md §4.4): the outcome of H2.

A problem's lines in a host are the logic lines its addition placed there. They are followed from
checkpoint to checkpoint through the instrument's line facts (``pair``, ``kinds``, ``hash`` and
``before_hash`` of each host record):

- an unchanged line keeps its owners;
- an edited line keeps its owners and gains the editor's (both problems' code is on it);
- moved code carries its owners with it (matched by identical text within the checkpoint);
- a method that is renamed, moved or re-signatured carries its lines to its new key.

A later checkpoint *j* **touches** problem *p* in a host when it edits or removes one of *p*'s lines,
or inserts a logic line between the first and the last of *p*'s lines still present there.

An owner is a label ``(cp, type, signature)``: the checkpoint and the host it placed the line in, so
a line moved to another method still belongs to the problem and host that first placed it.
"""

from __future__ import annotations

from collections import Counter

Label = tuple[int, str, str]
Key = tuple[str, str, str]
NONE: frozenset = frozenset()


def follow(records: list[dict], final: set[Key] | None = None) -> dict[Label, dict]:
    """Per label: ``placed`` (logic lines the problem placed in the host), ``touched`` (the later
    checkpoints touching them), ``present`` (lines carrying the label at the end) and ``lost``
    (lines carrying it whose tracking broke: a host whose stored length no longer matches, or, with
    ``final``, the keys of the last tree, a method that is not there and was not seen removed)."""
    arrays: dict[Key, list[frozenset]] = {}
    out: dict[Label, dict] = {}

    def entry(label: Label) -> dict:
        return out.setdefault(label, {"placed": 0, "touched": set(), "present": 0, "lost": 0})

    def touch(owners: frozenset, j: int) -> None:
        for label in owners:
            if label[0] != j:
                entry(label)["touched"].add(j)

    def lose(lines: list[frozenset]) -> None:
        for owners in lines:
            for label in owners:
                entry(label)["lost"] += 1

    units: dict[str, list[dict]] = {}
    for r in records:
        if r["kind"] in ("host", "removed", "carried"):
            units.setdefault(r["unit"], []).append(r)
    for unit in sorted(units, key=lambda u: int(u[2:])):
        j = int(unit[2:])
        recs = units[unit]
        # the before version of every changed method, taken out before any after version is stored
        olds: list[list[frozenset] | None] = []
        for r in recs:
            if r["kind"] == "host" and r["host_new"]:
                olds.append(None)
                continue
            key = ((r["before_path"], r["before_type"], r["before_signature"])
                   if r["kind"] != "removed" else (r["path"], r["type"], r["signature"]))
            n = r["positions"] if r["kind"] == "carried" else r["pre_positions"]
            old = arrays.pop(key, None)
            if old is not None and len(old) != n:
                lose(old)
                old = None
            olds.append(old if old is not None else [NONE] * n)
        # moved code: a removed line whose text is a moved line's elsewhere carries its owners there
        wanted = Counter(h for r in recs if r["kind"] == "host"
                         for h, k in zip(r["hash"], r["kinds"]) if k in (1, 2))
        pool: dict[int, list[frozenset]] = {}
        gone: list[set[int]] = []       # per record: the before positions removed and not moved
        for r, old in zip(recs, olds):
            removed: set[int] = set()
            if r["kind"] == "removed" or (r["kind"] == "host" and not r["host_new"]):
                kept = set() if r["kind"] == "removed" else {b for b in r["pair"] if b >= 0}
                for b, h in enumerate(r["before_hash"]):
                    if b in kept:
                        continue
                    if wanted[h] > 0:
                        wanted[h] -= 1
                        pool.setdefault(h, []).append(old[b])
                    else:
                        removed.add(b)
            gone.append(removed)
        for r, old, removed in zip(recs, olds, gone):
            if r["kind"] == "removed":
                for b in removed:
                    touch(old[b], j)
                continue
            key = (r["path"], r["type"], r["signature"])
            if r["kind"] == "carried":
                arrays[key] = old
                continue
            label = (j, r["type"], r["signature"])
            pair, kinds = r["pair"], r["kinds"]
            new: list[frozenset] = [NONE] * len(kinds)
            inserted: list[int] = []
            i, last = 0, -1                 # last: the before position of the last kept line
            while i < len(kinds):
                if kinds[i] == -1:
                    new[i] = old[pair[i]]
                    last = pair[i]
                    i += 1
                    continue
                e = i
                while e < len(kinds) and kinds[e] != -1:
                    e += 1
                nxt = pair[e] if e < len(kinds) else (len(old) if old is not None else 0)
                replaced = [b for b in range(last + 1, nxt) if b in removed]
                for a in range(i, e):
                    if kinds[a] == 0:
                        entry(label)["placed"] += 1
                        if replaced:        # an edit: the line keeps its owners and gains this one
                            b = replaced.pop(0)
                            touch(old[b], j)
                            new[a] = old[b] | {label}
                        else:
                            new[a] = frozenset({label})
                            inserted.append(a)
                    elif kinds[a] in (1, 2) and pool.get(r["hash"][a]):
                        new[a] = pool[r["hash"][a]].pop(0)
                for b in replaced:          # removed outright
                    touch(old[b], j)
                i = e
            # an insertion between the first and the last of another problem's lines still present
            span: dict[Label, list[int]] = {}
            for a, owners in enumerate(new):
                for o in owners:
                    if o != label:
                        s = span.setdefault(o, [a, a])
                        s[1] = a
            for a in inserted:
                for o, (lo, hi) in span.items():
                    if lo < a < hi:
                        entry(o)["touched"].add(j)
            arrays[key] = new
        for lines in pool.values():         # moved lines whose destination was not found
            lose(lines)
    for key, lines in arrays.items():
        missing = final is not None and key not in final
        for owners in lines:
            for o in owners:
                entry(o)["lost" if missing else "present"] += 1
    return out

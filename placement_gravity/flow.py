"""The control flow of a host (H5, PLAN.md 4.2a): which methods of the tree a request's data passes
through, so that a method holding the same types elsewhere, on another request's flow, is not
counted as a place the code could have gone.

The call graph is read from the instrument's places (``Pull --places``): each method's calls as
``receiver|name|arity``. A call's receiver is the class the source names (a local, parameter or
field of a declared type, a class for a static call), the method's own class, or unknown ("?", a
chained call or an expression; no symbol solver). A call goes to the methods of that name and arity
in the receiver's class, the classes it extends or implements, and those that extend or implement
it (the override that may run). A call whose receiver is unknown is not followed: following it by
name alone would join every request that calls ``get`` or ``save``. How many calls that leaves
unfollowed is counted (``resolution``).

A host's flow: the methods that call it, directly or not; of those, the ones nothing in the
application calls (the request's entry points, which the framework calls); and every method those
reach. With OfficeFloor, a request's functions are joined by its wiring file, not by Java calls: the
classes of a wiring file that holds the host's class are on its flow, with what they reach.
"""

from __future__ import annotations

from collections import defaultdict, deque


def _t(t: str | None) -> str:
    return (t or "").replace("$", ".")


def simple(t: str | None) -> str:
    return _t(t).split(".")[-1]


class Graph:
    def __init__(self, index: dict):
        files = index.get("files", {})
        self.methods: list[dict] = [m for f in files.values() for m in f.get("methods", [])]
        self.key = {(_t(m["type"]), m["signature"]): i for i, m in enumerate(self.methods)}
        supers: dict[str, set[str]] = defaultdict(set)
        for f in files.values():
            for c in f.get("classes", []):
                supers[simple(c["name"])].update(c.get("supers", []))
        subs: dict[str, set[str]] = defaultdict(set)
        for c, ss in supers.items():
            for x in ss:
                subs[x].add(c)
        self.supers, self.subs = supers, subs
        by_name: dict[str, list[int]] = defaultdict(list)
        for i, m in enumerate(self.methods):
            by_name[m.get("name") or m["signature"].split("(")[0]].append(i)
        self.out: list[set[int]] = [set() for _ in self.methods]
        self.into: list[set[int]] = [set() for _ in self.methods]
        self.resolution = {"calls_to_app_names": 0, "followed": 0, "unknown_receiver": 0}
        for i, m in enumerate(self.methods):
            own = simple(m["type"])
            for call in m.get("calls", []):
                recv, name, arity = call.rsplit("|", 2)    # a union type (multi-catch) holds "|"
                cand = [j for j in by_name.get(name, [])
                        if arity == "-1" or int(self.methods[j].get("params", -1)) in (int(arity), -1)]
                if not cand:
                    continue                       # a library's method, not the application's
                self.resolution["calls_to_app_names"] += 1
                if recv == "?":
                    self.resolution["unknown_receiver"] += 1
                    continue
                classes = self.family(own if recv == "" else recv)
                hit = [j for j in cand if simple(self.methods[j]["type"]) in classes]
                if hit:
                    self.resolution["followed"] += 1
                for j in hit:
                    self.out[i].add(j)
                    self.into[j].add(i)
        self.flows = [set(f) for f in index.get("flows", [])]

    def class_calls(self) -> dict[tuple[str, str], int]:
        """Calls followed from one class's methods to another's (H6, PLAN.md 4.2b), keyed by the
        classes' simple names, caller first; a call that may go to several overrides counts once
        for each class it may reach."""
        if getattr(self, "_class_calls", None) is None:
            out: dict[tuple[str, str], int] = defaultdict(int)
            for i, js in enumerate(self.out):
                a = simple(self.methods[i]["type"])
                for b in {simple(self.methods[j]["type"]) for j in js} - {a}:
                    out[(a, b)] += 1
            self._class_calls = dict(out)
        return self._class_calls

    def cross_edges(self) -> set[tuple[tuple[str, str], tuple[str, str]]]:
        """The calls followed from a method of one class to a method of another (H7, PLAN.md 4.2c),
        each as (caller, callee), a method as (its class's simple name, its signature)."""
        if getattr(self, "_cross", None) is None:
            def k(i):
                return simple(self.methods[i]["type"]), self.methods[i]["signature"]
            self._cross = {(k(i), k(j)) for i, js in enumerate(self.out) for j in js
                           if k(i)[0] != k(j)[0]}
        return self._cross

    def access(self) -> dict[tuple[str, str], str]:
        """Each method's access (public, protected, package, private), by (class, signature)."""
        if getattr(self, "_access", None) is None:
            self._access = {(simple(m["type"]), m["signature"]): m.get("access", "public")
                            for m in self.methods}
        return self._access

    def family(self, c: str) -> set[str]:
        """A class, what it extends or implements, and what extends or implements it."""
        out, todo = {c}, deque([c])
        while todo:
            x = todo.popleft()
            for y in self.supers.get(x, set()) | self.subs.get(x, set()):
                if y not in out:
                    out.add(y)
                    todo.append(y)
        return out

    def reach(self, start: set[int], edges: list[set[int]]) -> set[int]:
        seen, todo = set(start), deque(start)
        while todo:
            for j in edges[todo.popleft()]:
                if j not in seen:
                    seen.add(j)
                    todo.append(j)
        return seen

    def flow(self, type_: str, signature: str) -> set[int] | None:
        """The methods on the host's control flow, the host included; None if it is not in the tree."""
        h = self.key.get((_t(type_), signature))
        if h is None:
            return None
        up = self.reach({h}, self.into)
        roots = {i for i in up if not self.into[i]} or {h}
        start = set(roots)
        here = simple(type_)
        for group in self.flows:            # OfficeFloor: the request's functions, by its wiring
            if here in group:
                start |= {i for i, m in enumerate(self.methods) if simple(m["type"]) in group}
        return self.reach(start, self.out) | up

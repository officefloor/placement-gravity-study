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
        # a class's fields and their access (Pull VERSION 15), and each method's reads of another
        # class's fields: an edge to that field, as a call is to a method (H7, PLAN.md 4.2c)
        self.fields: dict[str, dict[str, str]] = defaultdict(dict)
        for f in files.values():
            for c in f.get("classes", []):
                self.fields[simple(c["name"])].update(c.get("fields") or {})
        self.reads: list[set[tuple[str, str]]] = [set() for _ in self.methods]
        for i, m in enumerate(self.methods):
            for r in m.get("reads", []):
                recv, name = r.rsplit("|", 1)
                for c in self.family(recv):
                    if name in self.fields.get(c, {}):
                        self.reads[i].add((c, f"#{name}"))
        self.flows = [set(f) for f in index.get("flows", [])]
        # the fields of a class that hold state (Pull VERSION 17): not injected, not constants, not
        # utilities; and each method's uses of its own class's fields (H7, PLAN.md 4.2c)
        self.state: dict[str, set[str]] = defaultdict(set)
        for f in files.values():
            for c in f.get("classes", []):
                self.state[simple(c["name"])].update(c.get("state") or [])

    def class_calls(self) -> dict[tuple[str, str], int]:
        """Calls followed from one class's methods to another's (H6, PLAN.md 4.2b), keyed by the
        classes' simple names, caller first; a call that may go to several overrides counts once
        for each class it may reach."""
        if getattr(self, "_class_calls", None) is None:
            out: dict[tuple[str, str], int] = defaultdict(int)
            for i, js in enumerate(self.out):
                a = simple(self.methods[i]["type"])
                for b in ({simple(self.methods[j]["type"]) for j in js} | {c for c, _ in self.reads[i]}) - {a}:
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
            self._cross |= {(k(i), f) for i, fs in enumerate(self.reads) for f in fs if k(i)[0] != f[0]}
        return self._cross

    def links(self) -> dict[str, set]:
        """The links between blocks of logic (H7, PLAN.md 4.2c, restated 24 November 2026), each
        counted once however heavy: **call links**, a method to a method it calls, in its own class or
        another (a call that may reach several overrides is a link to each), not to itself; and
        **state links**, a method to a field holding state that it uses, of its own class or another's.
        A field holding an injected dependency is not a state link, nor is a constant: injection is
        not bound to the control flow. A method is (its class's simple name, its signature), a field
        (its class's simple name, "#name")."""
        if getattr(self, "_links", None) is None:
            def k(i):
                return simple(self.methods[i]["type"]), self.methods[i]["signature"]
            calls = {(k(i), k(j)) for i, js in enumerate(self.out) for j in js if i != j}
            state = set()
            for i, m in enumerate(self.methods):
                c = simple(m["type"])
                state |= {(k(i), (c, f"#{x}")) for x in m.get("own", []) if x in self.state.get(c, ())}
                state |= {(k(i), (rc, f)) for rc, f in self.reads[i] if f[1:] in self.state.get(rc, ())}
            self._links = {"call": calls, "state": state}
        return self._links

    def access(self) -> dict[tuple[str, str], str]:
        """Each method's and field's access (public, protected, package, private), by (class,
        signature), a field as (class, "#name")."""
        if getattr(self, "_access", None) is None:
            self._access = {(simple(m["type"]), m["signature"]): m.get("access", "public")
                            for m in self.methods}
            self._access.update({(c, f"#{name}"): acc for c, fs in self.fields.items() for name, acc in fs.items()})
        return self._access

    def family(self, c: str) -> set[str]:
        """A class, what it extends or implements (its ancestors), and what extends or implements it
        (its descendants): where a call on it can go. Not its siblings. Until 22 November 2026 the two
        directions were followed together, so that a class reached every class sharing any ancestor
        with it, a library's interface among them (every repository of the pilot's Spring arm was
        one family of 37); the check against the compiler found it (PLAN.md 4.8, 9 row 80)."""
        cache = self.__dict__.setdefault("_family", {})
        if c not in cache:
            out = {c}
            for edges in (self.supers, self.subs):
                todo = deque([c])
                while todo:
                    for y in edges.get(todo.popleft(), ()):
                        if y not in out:
                            out.add(y)
                            todo.append(y)
            cache[c] = out
        return cache[c]

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

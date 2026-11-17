"""Novelty check for H1 and H2 as restated (18 November 2026): the records of s2b.py and oa2.py,
de-duplicated by title and scored on title and abstract against the vocabulary of bystanders
(what is visible where code lands and not used), of data gathering in a class or method, and of
later code using that data. Writes screened2.json (not kept) and screened2-top.tsv (score >= 3)."""
import json, re, collections, os
s2 = json.load(open("snowball2.json")) if os.path.exists("snowball2.json") else {}
oa = json.load(open("openalex2.json"))
recs = {}
def norm(t): return re.sub(r"[^a-z0-9]", "", (t or "").lower())
for src in (s2, oa):
    for seed, d in src.items():
        for kind in ("citations", "references"):
            for p in d.get(kind, []):
                t = p.get("title")
                if not t: continue
                r = recs.setdefault(norm(t), {"title": t, "year": p.get("year"), "venue": p.get("venue"),
                                              "abstract": p.get("abstract"), "via": set()})
                r["via"].add(f"{seed}:{'fwd' if kind == 'citations' else 'back'}")
                if not r["abstract"] and p.get("abstract"): r["abstract"] = p["abstract"]
print("unique records", len(recs))
terms = {
    r"scope|visib|accessib|expos|in scope|live variable|liveness|span\b|live time": 2,          # what is visible
    r"unused|not used|unreferenced|irrelevant (field|variable|state)|bystander": 3,              # and not used
    r"\b(field|attribute|instance variable|member variable|class state|shared state|global)s?\b": 2,  # class data
    r"\b(parameter|local variable|data clump|constant)s?\b": 1,                                    # method data
    r"accret|accumul|grow|growth|gather|attract|gravit|magnet|preferential|rich.get.richer": 2,  # gathering
    r"how.{0,25}(arise|form|emerge|introduc|born|start)|formation|emergence|origin of|become[s]? (a )?(god|blob|large)": 3,  # formation
    r"god class|god method|blob|brain class|large class|long method|feature envy|misplaced": 1,
    r"where.{0,30}(place|put|add|locat)|placement|entity placement|move method|move field": 2,
    r"data (coupling|dependenc|access|flow)|access to (foreign )?data|uses? (the )?(field|attribute|data)|field usage|attribute usage|def-use": 2,
    r"evolution|evolv|history|histories|commit|over time|longitudinal|releases": 1,
    r"later change|subsequent change|future change|change.prone|co-chang|revisit": 1,
    r"size.{0,25}(confound|control|normali)|controlling for size|per line|density": 2,            # H3
    r"cohesion|lcom|tcc\b": 1,
}
for r in recs.values():
    txt = (r["title"] + " " + (r["abstract"] or "")).lower()
    r["score"] = sum(w for p, w in terms.items() if re.search(p, txt)); r["via"] = sorted(r["via"])
L = sorted(recs.values(), key=lambda r: (-r["score"], r["title"]))
json.dump(L, open("screened2.json", "w"))
print(sorted(collections.Counter(min(r["score"], 12) for r in L).items()))
top = [r for r in L if r["score"] >= 3]
with open("screened2-top.tsv", "w") as f:
    f.write("score\tyear\ttitle\tvenue\tvia\n")
    for r in top:
        f.write(f"{r['score']}\t{r['year']}\t{r['title']}\t{r['venue'] or ''}\t{','.join(r['via'])}\n".replace("\n", " ").rstrip() + "\n")
print("score >= 3:", len(top), "; with abstract:", sum(1 for r in L if r["abstract"]))

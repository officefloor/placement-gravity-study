import json, re, collections
s2 = json.load(open("snowball.json")); oa = json.load(open("openalex.json"))
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
terms = {r"\bgrow|growth|accret|accumul": 2, r"evolution|evolv|history|histories|commit": 1,
         r"new (code|feature|functionality|requirement)|feature addition|added code|adding (code|feature)": 3,
         r"where.{0,30}(place|put|add|locat|implement)|placement|placed|location of": 3,
         r"scatter|tangl|crosscut|cross-cut": 1, r"propagat|ripple|co-chang|change coupling|logical coupling": 1,
         r"god class|god method|blob|large class|long method": 2,
         r"preferential|attachment|rich.get.richer|power.law|attract|gravit": 3, r"option|modularity|decoupl": 1,
         r"forced|constrain|dominant decomposition|tyranny": 2, r"decay|erosion|degrad|aging": 1,
         r"change request|feature request|maintenance task|modification task": 2, r"by design|by accident|intentional": 2}
for r in recs.values():
    txt = (r["title"] + " " + (r["abstract"] or "")).lower()
    r["score"] = sum(w for p, w in terms.items() if re.search(p, txt)); r["via"] = sorted(r["via"])
L = sorted(recs.values(), key=lambda r: -r["score"])
json.dump(L, open("screened.json", "w"))
print(collections.Counter(min(r["score"], 10) for r in L))

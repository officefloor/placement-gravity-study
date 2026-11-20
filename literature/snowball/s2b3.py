"""Novelty check of 20 November 2026: keyword searches on Semantic Scholar (relevance-ranked).
Writes s2search3.json (not kept)."""
import json, sys, time, urllib.request, urllib.parse
B="https://api.semanticscholar.org/graph/v1"
def get(url):
    for i in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"literature-screen/0.1"}), timeout=60) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504): time.sleep(4+4*i); continue
            raise
    raise RuntimeError(url)
F="title,year,venue,abstract,externalIds,citationCount,authors"
Q=sys.argv[1:] or [
 "Rent's rule software modules",
 "software coupling grows superlinearly with size",
 "scaling laws software structure size",
 "Bunch clustering module dependency graph Mancoridis",
 "access modifier changes software evolution empirical",
 "change attribute access modifier refactoring",
 "encapsulation violation introduced commits",
 "co-change clusters modularity assessment",
 "congruence of modularity and code coupling",
 "extract class refactoring structural semantic cohesion",
 "coupling increase per commit architectural impact",
 "physics of software",
 "information hiding change forced encapsulation boundary",
 "procedural versus object-oriented design coupling class size comparison",
 "god class split cohesion data disjoint clusters methods fields",
 "interface complexity implementation complexity ratio modules",
 "deep modules shallow modules",
 "coupling cohesion trade-off class size",
]
out={}
for q in Q:
    d=get(f"{B}/paper/search?query={urllib.parse.quote(q)}&fields={F}&limit=20")
    out[q]=d.get("data") or []; print(q,len(out[q]),file=sys.stderr); time.sleep(3)
json.dump(out,open("s2search3.json","w"))
for q,L in out.items():
    print("##",q)
    for p in L: print(" ",p.get("year"),"|",(p.get("title") or "")[:110],"|",(p.get("venue") or "")[:30],"|",p.get("citationCount"))

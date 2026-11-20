"""Novelty check of 20 November 2026 (encapsulation as a force, surface against volume,
conservation of complexity): keyword searches on OpenAlex. Writes openalex3.json (not kept)."""
import json, time, urllib.request, urllib.parse, sys
def get(u):
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"literature-screen/0.1"}),timeout=60) as r: return json.load(r)
        except Exception as e: time.sleep(3*(i+1))
    raise RuntimeError(u)
def inv(ab):
    if not ab: return None
    pos=[(p,w) for w,ps in ab.items() for p in ps]; return " ".join(w for p,w in sorted(pos))
def slim(w): return {"title":w.get("title"),"year":w.get("publication_year"),"venue":((w.get("primary_location") or {}).get("source") or {}).get("display_name"),"abstract":inv(w.get("abstract_inverted_index")),"doi":w.get("doi"),"citationCount":w.get("cited_by_count"),"authors":[a["author"]["display_name"] for a in w.get("authorships",[])][:6]}
Q=["coupling scaling class size software power law exponent",
 "allometric scaling software modules size dependencies",
 "superlinear scaling dependencies software size",
 "surface to volume ratio software module interface",
 "interface size versus implementation size modules",
 "accessibility modifier changes evolution Java",
 "visibility change evolution encapsulation erosion",
 "getter setter addition encapsulation evolution",
 "access modifier evolution open source",
 "coupling introduced by commit change",
 "commits that increase coupling",
 "co-change structural coupling extract class refactoring recommendation",
 "co-change move class remodularization recommendation",
 "search based software modularization cohesion coupling",
 "software module clustering multi-objective",
 "physics of software forces",
 "cohesion coupling trade-off optimal modularization",
 "dependency injection coupling empirical",
 "functional versus object-oriented coupling size comparison",
 "connascence",
 "deep modules interface implementation",
 "conservation of complexity software",
 "encapsulation forces change into class",
 "information hiding empirical evolution change",
 "class growth coupling growth evolution",
 "boundary complexity versus internal complexity software modules"]
out={}
for q in Q:
    d=get("https://api.openalex.org/works?per-page=25&search="+urllib.parse.quote(q))
    out[q]=[slim(x) for x in d["results"]]; print(q,len(out[q]),file=sys.stderr); time.sleep(0.5)
json.dump(out,open("openalex3.json","w"))

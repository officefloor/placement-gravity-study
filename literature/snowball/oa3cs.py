"""Novelty check of 20 November 2026: second round of keyword searches on OpenAlex, limited to
the field Computer Science (field 17). Queries from argv; appends to openalex3cs.json (not kept)."""
import json, os, sys, time, urllib.request, urllib.parse
def get(u):
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"literature-screen/0.1"}),timeout=60) as r: return json.load(r)
        except Exception: time.sleep(3*(i+1))
    raise RuntimeError(u)
def inv(ab):
    if not ab: return None
    pos=[(p,w) for w,ps in ab.items() for p in ps]; return " ".join(w for p,w in sorted(pos))
def slim(w): return {"title":w.get("title"),"year":w.get("publication_year"),"venue":((w.get("primary_location") or {}).get("source") or {}).get("display_name"),"abstract":inv(w.get("abstract_inverted_index")),"doi":w.get("doi"),"citationCount":w.get("cited_by_count"),"authors":[a["author"]["display_name"] for a in w.get("authorships",[])][:6]}
out=json.load(open("openalex3cs.json")) if os.path.exists("openalex3cs.json") else {}
for q in sys.argv[1:]:
    d=get("https://api.openalex.org/works?per-page=20&filter=primary_topic.field.id:17&search="+urllib.parse.quote(q))
    out[q]=[slim(x) for x in d["results"]]
    print("##",q)
    for w in out[q]: print(" ",w["year"],"|",(w["title"] or "")[:110],"|",(w["venue"] or "")[:30],"|",w["citationCount"])
    json.dump(out,open("openalex3cs.json","w")); time.sleep(0.3)

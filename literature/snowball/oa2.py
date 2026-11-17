"""Novelty check for H1 and H2 as restated (18 November 2026): forward citations and backward
references of the second set of seeds, from OpenAlex. Writes openalex2.json (not kept)."""
import json, time, urllib.request, urllib.parse
def get(u):
    for i in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"literature-screen/0.1"}),timeout=60) as r: return json.load(r)
        except Exception as e: time.sleep(3*(i+1))
    raise RuntimeError(u)
# seed -> DOI, or a title to resolve by search
seeds={"tsantalis2009":"10.1109/TSE.2009.1","olbrich2010":"10.1109/ICSM.2010.5609564",
       "vasa2007":"title:The inevitable stability of software change",
       "tufano2015":"10.1109/ICSE.2015.59",
       "chatzigeorgiou2010":"title:Investigating the evolution of bad smells in object-oriented code"}
def inv(ab):
    if not ab: return None
    pos=[(p,w) for w,ps in ab.items() for p in ps]; return " ".join(w for p,w in sorted(pos))
def slim(w): return {"title":w.get("title"),"year":w.get("publication_year"),"venue":((w.get("primary_location") or {}).get("source") or {}).get("display_name"),"abstract":inv(w.get("abstract_inverted_index")),"doi":w.get("doi"),"citationCount":w.get("cited_by_count")}
out={}
for k,d in seeds.items():
    if d.startswith("title:"):
        w=get("https://api.openalex.org/works?per-page=1&filter=title.search:"+urllib.parse.quote(d[6:]))["results"][0]
    else:
        w=get(f"https://api.openalex.org/works/doi:{d}")
    refs=w.get("referenced_works",[]); R=[]
    for i in range(0,len(refs),50):
        ids="|".join(r.split("/")[-1] for r in refs[i:i+50])
        R+= [slim(x) for x in get(f"https://api.openalex.org/works?filter=openalex:{ids}&per-page=50")["results"]]
    C=[]; pg=1
    while True:
        d2=get(f"https://api.openalex.org/works?filter=cites:{w['id'].split('/')[-1]}&per-page=200&page={pg}")
        C+=[slim(x) for x in d2["results"]]; pg+=1
        if len(d2["results"])<200: break
    out[k]={"seed":slim(w),"references":R,"citations":C}; print(k,"|",w.get("title"),w.get("publication_year"),w.get("doi"),"|",len(R),"refs",len(C),"citing")
json.dump(out,open("openalex2.json","w"))

import json, time, urllib.request, urllib.parse
def get(u):
    for i in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"literature-screen/0.1"}),timeout=60) as r: return json.load(r)
        except Exception as e: time.sleep(3*(i+1))
    raise RuntimeError(u)
dois={"sullivan2001":"10.1145/503209.503224","eaddy2008":"10.1109/TSE.2008.36","vaucher2009":"10.1109/WCRE.2009.23","steidl2015":"10.1109/SCAM.2015.7335411","tarr1999":"10.1145/302405.302457"}
def inv(ab):
    if not ab: return None
    pos=[(p,w) for w,ps in ab.items() for p in ps]; return " ".join(w for p,w in sorted(pos))
def slim(w): return {"title":w.get("title"),"year":w.get("publication_year"),"venue":((w.get("primary_location") or {}).get("source") or {}).get("display_name"),"abstract":inv(w.get("abstract_inverted_index")),"doi":w.get("doi"),"citationCount":w.get("cited_by_count")}
out={}
for k,d in dois.items():
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
    out[k]={"references":R,"citations":C}; print(k,len(R),"refs",len(C),"citing")
json.dump(out,open("openalex.json","w"))

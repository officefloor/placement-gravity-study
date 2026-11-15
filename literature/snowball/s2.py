import json, sys, time, urllib.request, urllib.parse
B="https://api.semanticscholar.org/graph/v1"
def get(url):
    for i in range(25):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504): time.sleep(3+3*i); continue
            raise
    raise RuntimeError(url)
def resolve(q):
    if q.startswith("DOI:"): return get(f"{B}/paper/{q}?fields=title,year,citationCount,referenceCount")
    d=get(f"{B}/paper/search?query={urllib.parse.quote(q)}&fields=title,year,citationCount,referenceCount&limit=1")
    return d["data"][0]
F="title,year,venue,abstract,externalIds,citationCount"
def edges(pid, kind):
    out=[]; off=0
    while True:
        d=get(f"{B}/paper/{pid}/{kind}?fields={F}&limit=500&offset={off}")
        key="citingPaper" if kind=="citations" else "citedPaper"
        out+= [x[key] for x in (d.get("data") or []) if x.get(key)]
        if "next" not in d: break
        off=d["next"]; time.sleep(1.5)
    return out
seeds={"sullivan2001":"DOI:10.1145/503209.503224",
 "eaddy2008":"DOI:10.1109/TSE.2008.36","vaucher2009":"DOI:10.1109/WCRE.2009.23",
 "steidl2015":"DOI:10.1109/SCAM.2015.7335411","tarr1999":"DOI:10.1145/302405.302457"}
import os
res=json.load(open('snowball.json')) if os.path.exists('snowball.json') else {}
for k,q in seeds.items():
    if k in res: continue
    p=resolve(q); time.sleep(1.5)
    print(k,p["title"],p.get("year"),p.get("citationCount"),p.get("referenceCount"),file=sys.stderr)
    c=edges(p["paperId"],"citations"); time.sleep(1.5); r=edges(p["paperId"],"references"); time.sleep(1.5)
    res[k]={"seed":p,"citations":c,"references":r}
    print(" ->",len(c),"citing",len(r),"refs",file=sys.stderr)
    json.dump(res,open("snowball.json","w"))
json.dump(res,open("snowball.json","w"))

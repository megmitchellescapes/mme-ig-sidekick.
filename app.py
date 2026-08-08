from flask import Flask, render_template_string, request, jsonify
import os, re, urllib.parse, requests

INDEX_HTML = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n<title>MME IG Sidekick 2.5</title><style>\n:root{\n  --aqua:#2FD6CF;--deep:#0A4F53;--deep2:#083D40;--coral:#FF7A6B;\n  --cream:#FFF8EE;--gold:#D6AE5D;--ink:#14383B;--muted:#6F7E7F;\n  --line:#DCE8E5;--card:#fff;\n}\n*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;\nbackground:linear-gradient(180deg,var(--cream),#f8fcfb);color:var(--ink)}\n.wrap{max-width:1100px;margin:auto;padding:18px 14px 44px}\n.hero{background:linear-gradient(135deg,var(--deep),var(--deep2));color:white;border-radius:26px;padding:24px;position:relative;overflow:hidden}\n.hero:after{content:"";position:absolute;width:220px;height:220px;border-radius:50%;background:var(--aqua);opacity:.15;right:-70px;top:-90px}\n.kicker{font-size:.77rem;font-weight:900;letter-spacing:.13em;text-transform:uppercase;color:#bff7f3}\nh1{font-size:clamp(2rem,7vw,3rem);line-height:.95;margin:.45rem 0}.hero p{color:#e3f3f1;max-width:760px}\n.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.card{background:#fff;border:1px solid var(--line);border-radius:20px;padding:16px;box-shadow:0 6px 20px rgba(6,70,73,.05)}\nsection{margin-top:18px}.section-head{display:flex;justify-content:space-between;gap:10px;align-items:end;flex-wrap:wrap}.section-head h2{margin:0;color:var(--deep)}.section-head p{margin:2px 0 0;color:var(--muted);font-size:.87rem}\nlabel{display:block;font-weight:850;color:var(--deep);font-size:.77rem;margin-bottom:5px}\ninput,select,textarea{width:100%;padding:11px;border:1px solid var(--line);border-radius:12px;background:white;font:inherit;color:var(--ink)}\n.controls{display:grid;grid-template-columns:1fr 1fr;gap:10px}.full{grid-column:1/-1}\nbutton,.btn{border:0;border-radius:12px;padding:10px 12px;font-weight:850;cursor:pointer;text-decoration:none;display:inline-block}\n.primary{background:var(--coral);color:white}.secondary{background:#dff9f7;color:var(--deep)}.deep{background:var(--deep);color:white}.gold{background:#fff2cf;color:#75560f}.ghost{background:#eff5f4;color:var(--ink)}\n.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:11px}\n.result{border-left:5px solid var(--aqua)}.row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.handle{font-weight:900;color:var(--deep)}\n.badge{display:inline-block;padding:5px 8px;border-radius:999px;font-size:.72rem;font-weight:900;background:#dff9f7;color:var(--deep)}\n.score{background:#fff0ed;color:#9b463b}.muted{color:var(--muted);font-size:.86rem}.small{font-size:.78rem}\npre{white-space:pre-wrap;background:#f3f7f6;border-radius:12px;padding:12px;overflow:auto}\n.notice{border-left:5px solid var(--gold);background:#fffaf0}\n.good{border-left:5px solid #48a87b;background:#f0fbf5}\n.bad{border-left:5px solid var(--coral);background:#fff5f3}\ntable{width:100%;border-collapse:collapse}td,th{text-align:left;padding:9px;border-bottom:1px solid var(--line);font-size:.84rem}\n@media(max-width:760px){.grid,.controls{grid-template-columns:1fr}.full{grid-column:auto}}\n</style></head><body><div class="wrap">\n<div class="hero"><div class="kicker">Meghan Mitchell Escapes • Version 2.5</div><h1>Discovery Assistant</h1>\n<p>Give Sidekick a destination, niche, or relationship type. It searches the public web for Instagram profiles, scores the candidates, and lets you save the ones worth engaging with.</p></div>\n\n<section><div id="status" class="card notice">Checking discovery connection...</div></section>\n\n<section><div class="section-head"><div><h2>Find accounts</h2><p>Think “Çeşme boutique hotels,” “honeymoon travelers,” “Puglia photographers,” or “Harrisburg wedding planners.”</p></div></div>\n<div class="card"><div class="controls">\n<div><label>Destination, niche, or seed</label><input id="seed" placeholder="Çeşme Turkey boutique travel"></div>\n<div><label>Who are we looking for?</label><select id="category"><option>Potential Client</option><option>Travel Partner</option><option>Relationship Builder</option><option>Current Audience</option></select></div>\n<div><label>Optional location</label><input id="location" placeholder="Turkey, Pennsylvania, etc."></div>\n<div><label>How many candidates?</label><select id="count"><option>8</option><option selected>12</option><option>16</option><option>20</option></select></div>\n</div><div class="actions"><button class="primary" onclick="discover()">Find Instagram accounts</button></div></div></section>\n\n<section><div class="section-head"><div><h2>Discovery results</h2><p>Sidekick ranks public-web candidates. Open the profile before engaging so you can confirm the fit.</p></div></div><div id="results"></div></section>\n\n<section><div class="section-head"><div><h2>Saved for engagement</h2><p>Your shortlist lives in this browser.</p></div></div><div id="saved"></div></section>\n\n</div><script>\nconst KEY="mme_sidekick_25_saved";\nlet saved=JSON.parse(localStorage.getItem(KEY)||"[]");\nfunction esc(s){return String(s||"").replace(/[&<>"\']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",\'"\':"&quot;","\'":"&#039;"}[m]))}\nasync function check(){\n let r=await fetch("/api/status");let x=await r.json();let el=document.getElementById("status");\n if(x.ready){el.className="card good";el.innerHTML="<b>Discovery is connected.</b> Using "+esc(x.provider)+"."}\n else{el.className="card notice";el.innerHTML="<b>One setup step remains.</b> Add a BRAVE_SEARCH_API_KEY or SERPER_API_KEY to the app environment. Then this page can actually search for accounts."}\n}\nasync function discover(){\n let body={seed:seed.value,category:category.value,location:location.value,count:count.value};\n results.innerHTML=\'<div class="card">Searching...</div>\';\n let r=await fetch("/api/discover",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});\n let x=await r.json();if(!r.ok){results.innerHTML=\'<div class="card bad"><b>Could not search:</b> \'+esc(x.error)+\'</div>\';return}\n if(!x.results.length){results.innerHTML=\'<div class="card notice">No profile candidates came back. Try a broader seed.</div>\';return}\n results.innerHTML=x.results.map((a,i)=>`<div class="card result"><div class="row"><span class="badge score">${a.score}% fit</span><span class="badge">${esc(a.bucket)}</span><span class="handle">${esc(a.handle)}</span></div>\n <p class="muted"><b>${esc(a.title)}</b><br>${esc(a.snippet)}</p><div class="actions"><a class="btn primary" target="_blank" href="${a.url}">Open Instagram</a>\n <button class="secondary" onclick=\'saveCandidate(${JSON.stringify(JSON.stringify(a))})\'>Save to engagement list</button></div></div>`).join("");\n}\nfunction saveCandidate(raw){let a=JSON.parse(raw);if(!saved.some(x=>x.handle.toLowerCase()===a.handle.toLowerCase()))saved.push(a);localStorage.setItem(KEY,JSON.stringify(saved));renderSaved()}\nfunction removeSaved(h){saved=saved.filter(x=>x.handle!==h);localStorage.setItem(KEY,JSON.stringify(saved));renderSaved()}\nfunction renderSaved(){saved.sort((a,b)=>b.score-a.score);document.getElementById("saved").innerHTML=saved.length?saved.map(a=>`<div class="card"><div class="row"><span class="badge">${esc(a.bucket)}</span><span class="handle">${esc(a.handle)}</span><span class="badge score">${a.score}%</span></div><div class="actions"><a class="btn primary" target="_blank" href="${a.url}">Open Instagram</a><button class="ghost" onclick="removeSaved(\'${a.handle}\')">Remove</button></div></div>`).join(""):\'<div class="card muted">Nothing saved yet.</div>\'}\ncheck();renderSaved();\n</script></body></html>'

app = Flask(__name__)

def normalize_handle(url):
    try:
        p = urllib.parse.urlparse(url)
        parts = [x for x in p.path.split("/") if x]
        if not parts:
            return None
        blocked = {"p","reel","reels","stories","explore","accounts","tv"}
        if parts[0].lower() in blocked:
            return None
        return "@" + parts[0]
    except Exception:
        return None

def score_candidate(title, snippet, category, seed, location):
    text = f"{title} {snippet}".lower()
    score = 40
    category_terms = {
      "Potential Client":["travel","vacation","honeymoon","anniversary","trip","getaway","passport","wander"],
      "Travel Partner":["hotel","resort","boutique","villa","tour","dmc","tourism","experience","concierge"],
      "Relationship Builder":["photographer","wedding","planner","restaurant","chef","creator","event","venue"],
      "Current Audience":["travel","vacation","trip","getaway"]
    }
    for term in category_terms.get(category, []):
        if term in text: score += 6
    for term in re.findall(r"[a-z0-9]+", (seed or "").lower()):
        if len(term)>3 and term in text: score += 4
    for term in re.findall(r"[a-z0-9]+", (location or "").lower()):
        if len(term)>3 and term in text: score += 3
    return min(score, 98)

def brave_search(query, count):
    key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not key: return None
    r = requests.get(
      "https://api.search.brave.com/res/v1/web/search",
      headers={"X-Subscription-Token": key, "Accept":"application/json"},
      params={"q":query,"count":min(count,20)}, timeout=20)
    r.raise_for_status()
    return [{"title":x.get("title",""),"url":x.get("url",""),"snippet":x.get("description","")} for x in r.json().get("web",{}).get("results",[])]

def serper_search(query, count):
    key = os.getenv("SERPER_API_KEY")
    if not key: return None
    r = requests.post(
      "https://google.serper.dev/search",
      headers={"X-API-KEY":key,"Content-Type":"application/json"},
      json={"q":query,"num":min(count,20)}, timeout=20)
    r.raise_for_status()
    return [{"title":x.get("title",""),"url":x.get("link",""),"snippet":x.get("snippet","")} for x in r.json().get("organic",[])]

@app.get("/")
def home():
    return render_template_string(INDEX_HTML)

@app.get("/api/status")
def status():
    provider = "Brave Search" if os.getenv("BRAVE_SEARCH_API_KEY") else ("Serper" if os.getenv("SERPER_API_KEY") else None)
    return jsonify({"ready": bool(provider), "provider": provider})

@app.post("/api/discover")
def discover():
    data = request.get_json(force=True)
    seed = data.get("seed","").strip()
    category = data.get("category","Potential Client")
    location = data.get("location","").strip()
    count = max(5,min(int(data.get("count",12)),20))
    if not seed:
        return jsonify({"error":"Add a destination, niche, or seed idea first."}),400

    intent = {
      "Potential Client": "travel vacation traveler",
      "Travel Partner": "hotel resort tourism tour DMC",
      "Relationship Builder": "photographer planner restaurant creator venue",
      "Current Audience": "travel"
    }.get(category,"travel")
    q = f'site:instagram.com {seed} {location} {intent} -inurl:/p/ -inurl:/reel/ -inurl:/explore/'
    try:
        raw = brave_search(q,count) or serper_search(q,count)
        if raw is None:
            return jsonify({"error":"No search provider is configured. Add BRAVE_SEARCH_API_KEY or SERPER_API_KEY to your environment."}),503
    except Exception as e:
        return jsonify({"error":f"Search provider error: {e}"}),502

    seen=set(); out=[]
    for x in raw:
        if "instagram.com" not in x["url"].lower(): continue
        h=normalize_handle(x["url"])
        if not h or h.lower() in seen: continue
        seen.add(h.lower())
        out.append({
          "handle":h,"url":x["url"],"title":x["title"],"snippet":x["snippet"],
          "bucket":category,"score":score_candidate(x["title"],x["snippet"],category,seed,location)
        })
    out=sorted(out,key=lambda z:z["score"],reverse=True)
    return jsonify({"query":q,"results":out[:count]})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")),debug=True)

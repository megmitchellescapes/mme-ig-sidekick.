from flask import Flask, render_template, request, jsonify
import os, re, urllib.parse, requests

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
    return render_template("index.html")

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

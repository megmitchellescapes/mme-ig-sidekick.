from flask import Flask, render_template_string, request, jsonify
import os, re, urllib.parse, requests, html

app = Flask(__name__)

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>MME IG Engagement Sidekick 2.6</title>
<style>
:root{
  --aqua:#2FD6CF;
  --aqua-soft:#DFF9F7;
  --deep:#0A4F53;
  --deep2:#083D40;
  --coral:#FF7A6B;
  --cream:#FFF8EE;
  --gold:#D6AE5D;
  --ink:#14383B;
  --muted:#6F7E7F;
  --line:#DCE8E5;
  --card:#fff;
  --green:#2E8B68;
}
*{box-sizing:border-box}
body{
  margin:0;
  font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:linear-gradient(180deg,var(--cream),#F7FCFB);
  color:var(--ink);
}
.wrap{max-width:1080px;margin:auto;padding:16px 12px 44px}
.hero{
  background:linear-gradient(135deg,var(--deep),var(--deep2));
  color:#fff;border-radius:26px;padding:22px;position:relative;overflow:hidden;
}
.hero:after{
  content:"";position:absolute;width:210px;height:210px;border-radius:50%;
  background:var(--aqua);opacity:.14;right:-70px;top:-80px;
}
.kicker{font-size:.74rem;letter-spacing:.13em;text-transform:uppercase;font-weight:900;color:#C8F9F6}
h1{margin:.4rem 0 .45rem;font-size:clamp(2rem,8vw,3.15rem);line-height:.95;letter-spacing:-.04em}
.hero p{max-width:720px;color:#E2F2F0;margin:.4rem 0}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px}
.stat{padding:11px;border-radius:15px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.14)}
.stat b{display:block;font-size:1.25rem}.stat span{font-size:.72rem;color:#D2ECE9}
section{margin-top:18px}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:15px;margin-bottom:10px;box-shadow:0 6px 18px rgba(6,70,73,.05)}
.good{border-left:5px solid #58B887;background:#F3FCF7}
.notice{border-left:5px solid var(--gold);background:#FFFBF1}
.result{border-left:5px solid var(--aqua)}
.section-head{display:flex;justify-content:space-between;align-items:end;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.section-head h2{margin:0;color:var(--deep);font-size:1.28rem}.section-head p{margin:3px 0 0;color:var(--muted);font-size:.84rem}
.controls{display:grid;grid-template-columns:1fr 1fr;gap:10px}.full{grid-column:1/-1}
label{display:block;font-size:.76rem;font-weight:900;color:var(--deep);margin-bottom:5px}
input,select{width:100%;padding:11px;border:1px solid var(--line);border-radius:12px;font:inherit;background:#fff;color:var(--ink)}
button,.btn{border:0;border-radius:12px;padding:10px 12px;font-weight:850;cursor:pointer;text-decoration:none;display:inline-block;font-size:.88rem}
.primary{background:var(--coral);color:white}.secondary{background:var(--aqua-soft);color:var(--deep)}
.deep{background:var(--deep);color:white}.ghost{background:#F1F5F4;color:var(--ink)}.gold{background:#FFF2CF;color:#75560F}
.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:11px}
.row{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.badge{display:inline-flex;padding:5px 8px;border-radius:999px;font-size:.7rem;font-weight:900;background:var(--aqua-soft);color:var(--deep)}
.badge.score{background:#FFF0ED;color:#9A453B}.badge.gold{background:#FFF4D6;color:#715313}.badge.green{background:#E6F7EE;color:#23684E}
.handle{font-size:1.02rem;font-weight:900;color:var(--deep)}
.reason{margin:8px 0 0;font-size:.9rem;line-height:1.4}.reason b{color:var(--deep)}
.meta{color:var(--muted);font-size:.8rem;margin-top:5px}
.tabs{display:flex;gap:7px;overflow:auto;padding:4px 0}
.tab{white-space:nowrap;background:#EAF4F2;color:var(--deep)}.tab.active{background:var(--deep);color:#fff}
.grid2{display:grid;grid-template-columns:1.25fr .75fr;gap:14px}
.mix{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.mixbox{border:1px solid var(--line);border-radius:14px;padding:11px;background:#FFFEFB}
.mixbox b{display:block;color:var(--deep);font-size:1.2rem}.mixbox span{font-size:.74rem;color:var(--muted)}
.empty{padding:26px;text-align:center;border:2px dashed var(--line);border-radius:17px;color:var(--muted)}
hr{border:0;border-top:1px solid var(--line);margin:14px 0}

.tagrow{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center}
.usecase{margin-top:7px;color:var(--muted);font-size:.82rem;line-height:1.35}
.copytoast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:var(--deep);color:#fff;padding:10px 14px;border-radius:999px;font-size:.82rem;font-weight:850;opacity:0;pointer-events:none;transition:.2s;z-index:50}
.copytoast.show{opacity:1}

@media(max-width:760px){.grid2,.controls{grid-template-columns:1fr}.full{grid-column:auto}.stats{grid-template-columns:repeat(3,1fr)}}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="kicker">Meghan Mitchell Escapes • Version 2.6.3</div>
    <h1>IG Engagement Sidekick</h1>
    <p>Find better-fit Instagram accounts, save the relationships worth building, and let Sidekick turn them into a focused daily engagement list.</p>
    <div class="stats">
      <div class="stat"><b id="savedStat">0</b><span>saved accounts</span></div>
      <div class="stat"><b id="todayStat">0/10</b><span>today's 10</span></div>
      <div class="stat"><b id="partnersStat">0</b><span>travel partners</span></div>
    </div>
  </header>

  <section><div id="status" class="card notice">Checking discovery connection...</div></section>

  <section>
    <div class="section-head">
      <div><h2>Discover accounts</h2><p>Search by destination, niche, or relationship type.</p></div>
    </div>
    <div class="card">
      <div class="controls">
        <div><label>Destination, niche, or seed</label><input id="seed" placeholder="Çeşme Turkey"></div>
        <div><label>Who are we looking for?</label>
          <select id="category">
            <option>Travel Partner</option>
            <option>Potential Client</option>
            <option>Relationship Builder</option>
            <option>Current Audience</option>
          </select>
        </div>
        <div><label>Optional location</label><input id="location" placeholder="Turkey, Pennsylvania, etc."></div>
        <div><label>How many candidates?</label><select id="count"><option>8</option><option selected>12</option><option>16</option><option>20</option></select></div>
        <div class="full">
          <label>Discovery focus</label>
          <select id="focus">
            <option value="auto">Smart mix</option>
            <option value="hotel">Hotels & resorts</option>
            <option value="tourism">Tourism boards & destination accounts</option>
            <option value="dmc">DMCs, tour operators & experiences</option>
            <option value="food">Restaurants, chefs & food experiences</option>
            <option value="photo">Photographers & creators</option>
            <option value="traveler">Travelers & trip-planning conversations</option>
          </select>
        </div>
      </div>
      <div class="actions"><button class="primary" onclick="discover()">Find Instagram accounts</button></div>
    </div>
  </section>

  <section>
    <div class="section-head">
      <div><h2>Discovery results</h2><p>Only stronger matches make the cut, with Smart Mix keeping the list varied.</p></div>
    </div>
    <div id="results"><div class="empty">Run a search to find candidates.</div></div>
  </section>

  <section>
    <div class="section-head">
      <div><h2>Today's 10</h2><p>Sidekick builds a balanced list from the accounts you've saved.</p></div>
      <button class="gold" onclick="buildToday(true)">Refresh today's mix</button>
    </div>
    <div class="grid2">
      <div id="today"></div>
      <div>
        <div class="card">
          <div class="section-head"><h2 style="font-size:1rem">Daily balance</h2></div>
          <div class="mix" id="mix"></div>
          <hr>
          <div class="meta">Target mix: 3 Potential Clients, 3 Current Audience, 2 Travel Partners, 2 Relationship Builders. If you have fewer in a bucket, Sidekick fills from the strongest remaining saved accounts.</div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="section-head">
      <div><h2>Saved relationships</h2><p>Accounts you've decided are worth keeping in your orbit.</p></div>
    </div>
    <div class="tabs" id="tabs"></div>
    <div id="saved"></div>
  </section>

  <section>
    <div class="section-head">
      <div><h2>Caption Tag Bank</h2><p>Keep useful Instagram handles ready for captions, credits, and destination posts.</p></div>
      <button class="gold" onclick="copyVisibleHandles()">Copy visible handles</button>
    </div>
    <div class="card">
      <div class="controls">
        <div>
          <label>Filter by best use</label>
          <select id="tagUseFilter" onchange="renderTagBank()">
            <option value="All">All post types</option>
            <option value="Destination Feature">Destination Feature</option>
            <option value="Hotel / Resort Post">Hotel / Resort Post</option>
            <option value="Itinerary / Planning Post">Itinerary / Planning Post</option>
            <option value="Food / Experience Post">Food / Experience Post</option>
            <option value="Photo / Creator Credit">Photo / Creator Credit</option>
            <option value="Travel Tip / Inspiration">Travel Tip / Inspiration</option>
          </select>
        </div>
        <div>
          <label>Filter by relationship type</label>
          <select id="tagBucketFilter" onchange="renderTagBank()">
            <option value="All">All relationship types</option>
            <option>Travel Partner</option>
            <option>Relationship Builder</option>
            <option>Potential Client</option>
            <option>Current Audience</option>
          </select>
        </div>
      </div>
    </div>
    <div id="tagBank"></div>
  </section>
</div>
<div id="copyToast" class="copytoast">Copied</div>

<script>
const SAVED_KEY="mme_sidekick_26_saved";
const TODAY_KEY="mme_sidekick_26_today";
const DATE_KEY="mme_sidekick_26_date";
const TARGETS={"Potential Client":3,"Current Audience":3,"Travel Partner":2,"Relationship Builder":2};
const BUCKETS=["All","Potential Client","Current Audience","Travel Partner","Relationship Builder"];
let saved=JSON.parse(localStorage.getItem(SAVED_KEY)||"[]");
let active="All";

function esc(s){return String(s||"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]))}
function dayKey(){return new Date().toISOString().slice(0,10)}
function store(){localStorage.setItem(SAVED_KEY,JSON.stringify(saved))}
function categoryIcon(c){
  return {"hotel":"🏨","tourism":"📍","dmc":"🧭","food":"🍽️","photo":"📸","traveler":"✈️","other":"✨"}[c]||"✨"
}
async function check(){
  const x=await (await fetch("/api/status")).json();
  const el=document.getElementById("status");
  if(x.ready){el.className="card good";el.innerHTML="<b>Discovery is connected.</b> Using "+esc(x.provider)+"."}
  else{el.className="card notice";el.innerHTML="<b>Search provider not configured.</b>"}
}
async function discover(){
  const body={seed:seed.value,category:category.value,location:location.value,count:count.value,focus:focus.value};
  results.innerHTML='<div class="card">Searching...</div>';
  const r=await fetch("/api/discover",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  const x=await r.json();
  if(!r.ok){results.innerHTML='<div class="card notice">'+esc(x.error)+'</div>';return}
  if(!x.results.length){results.innerHTML='<div class="empty">No strong profile candidates came back. Try a broader search.</div>';return}
  results.innerHTML=x.results.map(a=>`
    <div class="card result">
      <div class="row">
        <span class="badge score">${a.score}% fit</span>
        <span class="badge">${esc(a.bucket)}</span>
        <span class="badge gold">${categoryIcon(a.type)} ${esc(a.type_label)}</span>
        <span class="handle">${esc(a.handle)}</span>
      </div>
      <div class="reason"><b>Why Sidekick picked it:</b> ${esc(a.reason)}</div>
      ${a.location_hint?`<div class="meta">📍 ${esc(a.location_hint)}</div>`:""}
      <div class="actions">
        <a class="btn primary" target="_blank" rel="noopener" href="${a.url}">Open Instagram</a>
        <button class="secondary" onclick='saveCandidate(${JSON.stringify(JSON.stringify(a))})'>Save relationship</button>
      </div>
    </div>`).join("");
}
function saveCandidate(raw){
  const a=JSON.parse(raw);
  if(!saved.some(x=>x.handle.toLowerCase()===a.handle.toLowerCase())){
    a.doneToday=false;
    a.savedAt=Date.now();
    saved.push(a);
    store();
    buildToday(false);
    renderAll();
  }
}
function removeSaved(handle){
  saved=saved.filter(x=>x.handle!==handle);store();buildToday(false);renderAll();
}
function markDone(handle){
  const x=saved.find(a=>a.handle===handle);if(!x)return;
  x.doneToday=!x.doneToday;store();renderAll();
}
function todayIds(){
  if(localStorage.getItem(DATE_KEY)!==dayKey()){
    localStorage.setItem(DATE_KEY,dayKey());
    localStorage.removeItem(TODAY_KEY);
    saved.forEach(x=>x.doneToday=false);store();
  }
  return JSON.parse(localStorage.getItem(TODAY_KEY)||"[]");
}
function buildToday(force){
  if(!force && localStorage.getItem(TODAY_KEY) && localStorage.getItem(DATE_KEY)===dayKey()) return;
  let ids=[];
  Object.entries(TARGETS).forEach(([bucket,n])=>{
    const pool=saved.filter(x=>x.bucket===bucket).sort((a,b)=>b.score-a.score || a.savedAt-b.savedAt);
    ids.push(...pool.slice(0,n).map(x=>x.handle));
  });
  if(ids.length<10){
    const extras=saved.filter(x=>!ids.includes(x.handle)).sort((a,b)=>b.score-a.score || a.savedAt-b.savedAt);
    ids.push(...extras.slice(0,10-ids.length).map(x=>x.handle));
  }
  localStorage.setItem(DATE_KEY,dayKey());
  localStorage.setItem(TODAY_KEY,JSON.stringify(ids.slice(0,10)));
}
function renderToday(){
  buildToday(false);
  const ids=todayIds();
  const items=ids.map(h=>saved.find(x=>x.handle===h)).filter(Boolean);
  const root=document.getElementById("today");
  root.innerHTML=items.length?items.map(a=>`
    <div class="card">
      <div class="row">
        <span class="badge">${esc(a.bucket)}</span>
        <span class="badge gold">${categoryIcon(a.type)} ${esc(a.type_label)}</span>
        <span class="handle">${esc(a.handle)}</span>
        ${a.doneToday?'<span class="badge green">✓ Done</span>':''}
      </div>
      <div class="reason"><b>Why today:</b> ${esc(a.reason)}</div>
      <div class="actions">
        <a class="btn primary" target="_blank" href="${a.url}">Open Instagram</a>
        <button class="${a.doneToday?'ghost':'secondary'}" onclick="markDone('${a.handle}')">${a.doneToday?'Undo':'Mark done'}</button>
      </div>
    </div>`).join(""):'<div class="empty">Save some accounts first. Sidekick will build your daily 10 automatically.</div>';
  const done=items.filter(x=>x.doneToday).length;
  document.getElementById("todayStat").textContent=done+"/"+Math.min(10,items.length||10);
  document.getElementById("mix").innerHTML=Object.keys(TARGETS).map(b=>{
    const c=items.filter(x=>x.bucket===b).length;
    return `<div class="mixbox"><b>${c}</b><span>${esc(b)}</span></div>`;
  }).join("");
}
function renderTabs(){
  const root=document.getElementById("tabs");
  root.innerHTML=BUCKETS.map(b=>`<button class="tab ${b===active?'active':''}" onclick="active='${b}';renderAll()">${b}</button>`).join("");
}
function renderSaved(){
  const items=saved.filter(x=>active==="All"||x.bucket===active).sort((a,b)=>b.score-a.score);
  document.getElementById("saved").innerHTML=items.length?items.map(a=>`
    <div class="card">
      <div class="row"><span class="badge">${esc(a.bucket)}</span><span class="badge gold">${categoryIcon(a.type)} ${esc(a.type_label)}</span><span class="handle">${esc(a.handle)}</span><span class="badge score">${a.score}%</span></div>
      <div class="reason"><b>Why it matters:</b> ${esc(a.reason)}</div>
      <div class="actions"><a class="btn primary" target="_blank" href="${a.url}">Open Instagram</a><button class="ghost" onclick="removeSaved('${a.handle}')">Remove</button></div>
    </div>`).join(""):'<div class="empty">Nothing saved in this bucket yet.</div>';
}
function renderStats(){
  savedStat.textContent=saved.length;
  partnersStat.textContent=saved.filter(x=>x.bucket==="Travel Partner").length;
}

function postUseFor(a){
  if(a.type==="hotel") return "Hotel / Resort Post";
  if(a.type==="food") return "Food / Experience Post";
  if(a.type==="photo") return "Photo / Creator Credit";
  if(a.type==="dmc") return "Itinerary / Planning Post";
  if(a.type==="tourism") return "Destination Feature";
  if(a.type==="traveler") return "Travel Tip / Inspiration";
  if(a.bucket==="Travel Partner") return "Destination Feature";
  if(a.bucket==="Relationship Builder") return "Travel Tip / Inspiration";
  return "Travel Tip / Inspiration";
}

function useDetail(a){
  const use=postUseFor(a);
  const details={
    "Destination Feature":"Great for destination spotlights, hidden-gem posts, “Okay this place though,” and destination inspiration captions.",
    "Hotel / Resort Post":"Great for hotel features, resort recommendations, property spotlights, and supplier mentions.",
    "Itinerary / Planning Post":"Great for itinerary posts, activity roundups, excursion ideas, and “Here’s the game plan” content.",
    "Food / Experience Post":"Great for restaurant mentions, culinary experiences, local recommendations, and itinerary add-ons.",
    "Photo / Creator Credit":"Great for photographer credits, creator collaborations, destination shoots, and visual-content partnerships.",
    "Travel Tip / Inspiration":"Great for general travel posts, destination inspiration, tips, conversation starters, and community engagement."
  };
  return details[use]||details["Travel Tip / Inspiration"];
}

function showToast(msg){
  const t=document.getElementById("copyToast");
  t.textContent=msg||"Copied";
  t.classList.add("show");
  setTimeout(()=>t.classList.remove("show"),1200);
}

function copyHandle(handle){
  navigator.clipboard.writeText(handle);
  showToast(handle+" copied");
}

function visibleTagItems(){
  const use=document.getElementById("tagUseFilter")?.value||"All";
  const bucket=document.getElementById("tagBucketFilter")?.value||"All";
  return saved.filter(a=>(use==="All"||postUseFor(a)===use)&&(bucket==="All"||a.bucket===bucket));
}

function copyVisibleHandles(){
  const items=visibleTagItems();
  if(!items.length){showToast("No handles to copy");return}
  const text=items.map(a=>a.handle).join(" ");
  navigator.clipboard.writeText(text);
  showToast(items.length+" handle"+(items.length===1?"":"s")+" copied");
}

function renderTagBank(){
  const root=document.getElementById("tagBank");
  const items=visibleTagItems().sort((a,b)=>postUseFor(a).localeCompare(postUseFor(b))||b.score-a.score);
  root.innerHTML=items.length?items.map(a=>`
    <div class="card">
      <div class="tagrow">
        <div>
          <div class="row">
            <span class="handle">${esc(a.handle)}</span>
            <span class="badge">${esc(a.bucket)}</span>
            <span class="badge gold">${esc(postUseFor(a))}</span>
          </div>
          <div class="usecase"><b>Good for:</b> ${esc(useDetail(a))}</div>
        </div>
        <button class="secondary" onclick="copyHandle('${a.handle}')">Copy</button>
      </div>
    </div>`).join(""):'<div class="empty">Save some accounts first. Their handles will automatically appear here.</div>';
}

function renderAll(){renderTabs();renderSaved();renderToday();renderStats();renderTagBank()}
check();renderAll();
</script>
</body>
</html>
"""

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

def clean_text(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&quot;", '"').replace("&#39;", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def classify_type(text, focus="auto"):
    t = text.lower()
    if focus != "auto":
        return focus

    buckets = {
        "hotel":["hotel","resort","villa","suites","spa","boutique hotel","accommodation","rooms"],
        "tourism":["tourism","visit ","destination","official page","travel guide","city guide","municipality"],
        "dmc":["dmc","tour operator","tours","excursions","experience","concierge","travel company","transfer"],
        "food":["restaurant","chef","dining","cafe","bar ","food","breakfast","brunch"],
        "photo":["photographer","photography","creator","content creator","videographer","wedding photographer"],
        "traveler":["traveler","travel blogger","trip","vacation","honeymoon","anniversary","getaway","travel diary"]
    }
    scores={k:sum(1 for term in terms if term in t) for k,terms in buckets.items()}
    best=max(scores,key=scores.get)
    return best if scores[best] else "other"

def type_label(tp):
    return {
      "hotel":"Hotel / Resort",
      "tourism":"Tourism / Destination",
      "dmc":"DMC / Experience",
      "food":"Food / Dining",
      "photo":"Photographer / Creator",
      "traveler":"Traveler / Trip Planning",
      "other":"Relevant Account"
    }.get(tp,"Relevant Account")

def token_words(text):
    return [x for x in re.findall(r"[a-z0-9çşğıöü]+", (text or "").lower()) if len(x) > 2]

def relevance_score(title, snippet, handle, category, seed, location, tp):
    text = f"{title} {snippet} {handle}".lower()
    score = 20

    # Strong destination / seed relevance
    seed_terms = token_words(seed)
    loc_terms = token_words(location)
    seed_hits = sum(1 for term in seed_terms if term in text)
    loc_hits = sum(1 for term in loc_terms if term in text)

    score += min(seed_hits * 10, 30)
    score += min(loc_hits * 6, 18)

    # Account-type usefulness
    type_bonus = {
        "hotel":18,
        "tourism":20,
        "dmc":20,
        "food":12,
        "photo":12,
        "traveler":14,
        "other":4
    }
    score += type_bonus.get(tp, 0)

    # Category relevance
    category_terms = {
      "Potential Client":["vacation","honeymoon","anniversary","trip","getaway","travel","traveler","passport","itinerary"],
      "Travel Partner":["hotel","resort","villa","tourism","tour","dmc","experience","restaurant","photographer","concierge"],
      "Relationship Builder":["photographer","planner","restaurant","chef","creator","venue","wedding","concierge"],
      "Current Audience":["travel","vacation","trip","getaway","traveler"]
    }
    for term in category_terms.get(category, []):
        if term in text:
            score += 4

    # High-value signals
    high_value = ["official", "luxury", "boutique", "resort", "hotel", "tourism", "dmc", "experience", "concierge", "photographer"]
    score += min(sum(1 for t in high_value if t in text) * 3, 12)

    # Weak / noisy / likely irrelevant signals
    junk_terms = [
        "fan page","memes","meme","news","football","soccer","politics","crypto","forex",
        "giveaway","contest","spam","quotes","motivation","shop now","dropshipping"
    ]
    score -= sum(12 for t in junk_terms if t in text)

    # If neither the seed nor location appears, heavily penalize.
    if seed_terms and seed_hits == 0:
        score -= 18
    if loc_terms and loc_hits == 0:
        score -= 10

    return max(0, min(score, 98))

def make_reason(bucket, tp, seed, location):
    subject = seed.strip() if seed else "your search"
    loc = f" in {location.strip()}" if location.strip() else ""
    if bucket == "Travel Partner":
        templates={
          "hotel":f"A hotel or resort directly relevant to {subject}{loc}, useful for supplier research and relationship building.",
          "tourism":f"A destination-focused account connected to {subject}{loc}, useful for local intel, content ideas, and future partnerships.",
          "dmc":f"An experience or destination-service account tied to {subject}{loc}, useful for excursion research and on-the-ground relationships.",
          "food":f"A dining or culinary account connected to {subject}{loc}, useful for building richer itineraries and local recommendations.",
          "photo":f"A creator or photographer relevant to {subject}{loc}, potentially useful for referrals, client experiences, or destination content."
        }
        return templates.get(tp,f"A public Instagram account that appears relevant to {subject}{loc} and your travel-partner network.")
    if bucket == "Potential Client":
        return f"A public account whose search context suggests interest in travel or trip planning related to {subject}{loc}."
    if bucket == "Relationship Builder":
        return f"A complementary business or creator around {subject}{loc} that could become a useful referral or collaboration relationship."
    return f"A public account connected to {subject}{loc} that may be worth keeping in your engagement orbit."

def diversity_key(item):
    return item.get("type","other")

def brave_search(query, count):
    key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not key:
        return None
    r = requests.get(
      "https://api.search.brave.com/res/v1/web/search",
      headers={"X-Subscription-Token": key, "Accept":"application/json"},
      params={"q":query,"count":min(count,20)},
      timeout=20)
    r.raise_for_status()
    return [{"title":x.get("title",""),"url":x.get("url",""),"snippet":x.get("description","")} for x in r.json().get("web",{}).get("results",[])]

def serper_search(query, count):
    key = os.getenv("SERPER_API_KEY")
    if not key:
        return None
    r = requests.post(
      "https://google.serper.dev/search",
      headers={"X-API-KEY":key,"Content-Type":"application/json"},
      json={"q":query,"num":min(count,20)},
      timeout=20)
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
    category = data.get("category","Travel Partner")
    location = data.get("location","").strip()
    focus = data.get("focus","auto")
    count = max(5,min(int(data.get("count",12)),20))

    if not seed:
        return jsonify({"error":"Add a destination, niche, or seed idea first."}),400

    focus_terms = {
      "auto":["hotel resort","tourism destination","tours experiences","restaurant dining","photographer creator","travel guide"],
      "hotel":["hotel","resort","boutique hotel","villa","spa resort"],
      "tourism":["tourism","destination","official visit","travel guide","city guide"],
      "dmc":["DMC","tour operator","excursions","experiences","concierge"],
      "food":["restaurant","dining","chef","food","cafe"],
      "photo":["photographer","creator","photography","videographer","content creator"],
      "traveler":["traveler","vacation","honeymoon","anniversary","trip"]
    }
    category_terms = {
      "Travel Partner":["travel","tourism","hotel","experience"],
      "Potential Client":["traveler","vacation","honeymoon","trip"],
      "Relationship Builder":["photographer","planner","restaurant","creator"],
      "Current Audience":["travel","vacation","trip","getaway"]
    }

    terms = focus_terms.get(focus, focus_terms["auto"])
    cats = category_terms.get(category, ["travel"])
    loc = f" {location}" if location else ""

    queries = []
    for term in terms:
        queries.append(f'site:instagram.com {seed}{loc} {term} -inurl:/p/ -inurl:/reel/ -inurl:/stories/')
    for term in cats[:3]:
        queries.append(f'site:instagram.com {seed}{loc} {term} -inurl:/p/ -inurl:/reel/')
    queries.append(f'site:instagram.com {seed}{loc} -inurl:/p/ -inurl:/reel/ -inurl:/stories/')

    provider = "Brave Search" if os.getenv("BRAVE_SEARCH_API_KEY") else ("Serper" if os.getenv("SERPER_API_KEY") else None)
    if not provider:
        return jsonify({"error":"No search provider is configured."}),503

    merged = []
    for q in queries:
        try:
            raw = brave_search(q, 20) if provider == "Brave Search" else serper_search(q, 20)
            if raw:
                merged.extend(raw)
        except Exception:
            continue

    seen = set()
    out = []
    for x in merged:
        url = x.get("url","")
        if "instagram.com" not in url.lower():
            continue
        h = normalize_handle(url)
        if not h or h.lower() in seen:
            continue
        seen.add(h.lower())

        title = clean_text(x.get("title",""))
        snippet = clean_text(x.get("snippet",""))
        tp = classify_type(f"{title} {snippet}", focus)
        score = relevance_score(title, snippet, h, category, seed, location, tp)
        out.append({
          "handle": h,
          "url": url,
          "bucket": category,
          "score": score,
          "type": tp,
          "type_label": type_label(tp),
          "reason": make_reason(category,tp,seed,location),
          "location_hint": location or seed,
        })

    # Keep only worthwhile candidates.
    threshold = 45
    out = [x for x in out if x["score"] >= threshold]
    out = sorted(out, key=lambda z:z["score"], reverse=True)

    # Diversify Smart Mix so the list is not 8 nearly identical accounts.
    if focus == "auto":
        selected=[]
        per_type={}
        for item in out:
            tp=item.get("type","other")
            if per_type.get(tp,0) < 3:
                selected.append(item)
                per_type[tp]=per_type.get(tp,0)+1
            if len(selected) >= count:
                break
        # Fill remaining slots with best leftovers.
        if len(selected) < count:
            used={x["handle"] for x in selected}
            for item in out:
                if item["handle"] not in used:
                    selected.append(item)
                    used.add(item["handle"])
                if len(selected) >= count:
                    break
        out=selected

    return jsonify({
        "queries_run":len(queries),
        "threshold":threshold,
        "results":out[:count]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")),debug=False)

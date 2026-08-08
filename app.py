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
.collapsible-section>.section-head{cursor:pointer;user-select:none}.collapsible-section.collapsed>:not(.section-head){display:none!important}.collapse-icon{font-weight:900;color:var(--deep);font-size:1.1rem;margin-left:auto}
.checklist-item{display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--line)}.checklist-item:last-child{border-bottom:0}.checklist-item input[type=checkbox]{width:20px;height:20px;flex:0 0 20px;margin-top:2px;accent-color:var(--deep)}.checklist-text{flex:1}.checklist-text b{display:block;color:var(--deep);margin-bottom:2px}.checklist-text span{font-size:.8rem;color:var(--muted);line-height:1.35}.checklist-account{margin-top:5px;font-weight:850;color:var(--deep)}.checklist-progress{height:10px;background:#E8F0EE;border-radius:999px;overflow:hidden;margin-top:10px}.checklist-progress>div{height:100%;background:var(--aqua);width:0%;transition:.2s}

.calendar-toolbar{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.calendar-title{font-weight:900;color:var(--deep);font-size:1.05rem}
.calendar-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px;width:100%;max-width:100%;overflow:hidden}
.cal-dow{text-align:center;font-size:.68rem;font-weight:900;color:var(--muted);padding:5px 0;text-transform:uppercase}
.cal-day{min-height:92px;min-width:0;border:1px solid var(--line);border-radius:12px;background:#fff;padding:7px;cursor:pointer;position:relative;overflow:hidden}
.cal-day:hover{border-color:var(--aqua)}
.cal-day.other{opacity:.35}
.cal-day.today{outline:2px solid var(--aqua)}
.cal-day.selected{background:var(--aqua-soft);border-color:var(--aqua)}
.cal-num{font-size:.74rem;font-weight:900;color:var(--deep)}
.cal-post{
      margin-top:5px;padding:5px 6px;border-radius:8px;background:#FFF5F1;
      font-size:.67rem;line-height:1.2;color:var(--ink);
      overflow:hidden;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;
      word-break:break-word;overflow-wrap:anywhere
    }
.cal-post.ready{background:#EAF9F2}.cal-post.scheduled{background:#E6F6F5}.cal-post.posted{background:#FFF2CF}
.today-post-card{border-left:5px solid var(--coral)}
.calendar-form{margin-top:12px}
.platforms{display:flex;gap:6px;flex-wrap:wrap}
.platforms label{display:flex;gap:5px;align-items:center;font-size:.8rem;font-weight:700;color:var(--ink)}
.platforms input{width:auto}
.postlist{display:grid;gap:8px;margin-top:10px}
.postitem{border:1px solid var(--line);border-radius:12px;padding:10px;background:#fff}
.status-pill{display:inline-flex;padding:4px 7px;border-radius:999px;font-size:.67rem;font-weight:900;background:#EEF4F3;color:var(--deep)}
.status-pill.Ready{background:#EAF9F2;color:#23684E}.status-pill.Scheduled{background:#E6F6F5;color:var(--deep)}.status-pill.Posted{background:#FFF2CF;color:#75560F}
.comment-assist{border-left:5px solid var(--aqua)}
.comment-option{border:1px solid var(--line);border-radius:14px;padding:11px;margin-top:8px;background:#FFFEFB}
.comment-option b{color:var(--deep)}
.relationship-badge{display:inline-flex;padding:5px 8px;border-radius:999px;font-size:.7rem;font-weight:900}
.rel-following{background:#E6F6F5;color:var(--deep)}
.rel-follower{background:#FFF0ED;color:#93483F}
.rel-mutual{background:#EAF9F2;color:#23684E}
.rel-new{background:#F1F3F3;color:#5D6C6D}
.import-drop{border:2px dashed var(--line);border-radius:16px;padding:18px;background:#FFFEFB}
.import-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
@media(max-width:760px){.import-summary{grid-template-columns:repeat(2,1fr)}}
.comment-text{margin:6px 0;font-size:.9rem;line-height:1.4}
.comment-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
@media(max-width:760px){.comment-grid{grid-template-columns:1fr}}
@media(max-width:760px){
  .calendar-grid{grid-template-columns:repeat(7,minmax(0,1fr));gap:2px;width:100%}
  .cal-dow{font-size:.56rem;padding:4px 0;overflow:hidden}
  .cal-day{min-height:74px;min-width:0;padding:4px 3px;border-radius:9px}
  .cal-num{font-size:.66rem}
  .cal-post{
    margin-top:3px;
    font-size:.54rem;
    line-height:1.12;
    padding:3px 3px;
    border-radius:6px;
    -webkit-line-clamp:3;
  }
  .calendar-toolbar{gap:4px}
  .calendar-toolbar button{padding:8px 9px;font-size:.74rem}
  .calendar-title{font-size:.95rem}
  .card:has(.calendar-grid){padding:10px 8px}
}

@media(max-width:420px){
  .calendar-grid{gap:1px}
  .cal-dow{font-size:.5rem}
  .cal-day{min-height:68px;padding:3px 2px}
  .cal-num{font-size:.62rem}
  .cal-post{font-size:.49rem;padding:3px 2px;-webkit-line-clamp:3}
  .calendar-toolbar button{padding:7px 8px;font-size:.68rem}
  .calendar-title{font-size:.88rem}
}



.engagement-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.engagebtn{background:#EEF7F6;color:var(--deep);padding:8px 10px;font-size:.78rem}
.engagebtn.active{background:var(--deep);color:#fff}
.status-select{max-width:220px}
.history{margin-top:9px;padding-top:9px;border-top:1px solid var(--line)}
.history-item{font-size:.78rem;color:var(--muted);padding:3px 0}
.noteinput{margin-top:8px}
textarea{width:100%;padding:10px;border:1px solid var(--line);border-radius:12px;font:inherit;background:#fff;color:var(--ink);min-height:68px;resize:vertical}


@media(max-width:760px){.grid2,.controls{grid-template-columns:1fr}.full{grid-column:auto}.stats{grid-template-columns:repeat(3,1fr)}}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="kicker">Meghan Mitchell Escapes • Version 2.10.2</div>
    <h1>IG Engagement Sidekick</h1>
    <p>Find better-fit Instagram accounts, save the relationships worth building, and let Sidekick turn them into a focused daily engagement list.</p>
    <div class="stats">
      <div class="stat"><b id="savedStat">0</b><span>saved accounts</span></div>
      <div class="stat"><b id="todayStat">0/10</b><span>today's 10</span></div>
      <div class="stat"><b id="partnersStat">0</b><span>travel partners</span></div>
    </div>
  </header>

  <section><div id="status" class="card notice">Checking discovery connection...</div></section>

  <section class="collapsible-section" data-collapse-id="instagramData">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Instagram Relationship Intelligence</h2><p>Import your Instagram data so Sidekick knows who is already in your world.</p></div><span class="collapse-icon" id="instagramDataIcon">−</span>
    </div>
    <div class="card">
      <div class="import-summary">
        <div class="mixbox"><b id="igFollowingCount">0</b><span>Following</span></div>
        <div class="mixbox"><b id="igFollowerCount">0</b><span>Followers</span></div>
        <div class="mixbox"><b id="igMutualCount">0</b><span>Mutuals</span></div>
        <div class="mixbox"><b id="igImportedDate">Never</b><span>Last import</span></div>
      </div>
    </div>
    <div class="card import-drop">
      <label>Import Instagram followers / following files</label>
      <div class="meta">Choose the JSON or HTML files from your Instagram information download. Sidekick reads them in your browser and stores the handle lists on this device. For the standard Meta export, select followers_1.json and following.json.</div>
      <input id="igDataFiles" type="file" accept=".json,.html,.htm" multiple style="margin-top:10px">
      <div class="actions">
        <button class="primary" onclick="importInstagramData()">Import Instagram data</button>
        <button class="ghost" onclick="clearInstagramData()">Clear imported data</button>
      </div>
    </div>
    <div class="card">
      <div class="controls">
        <div>
          <label>Discovery relationship filter</label>
          <select id="relationshipFilter" onchange="renderDiscoveryFromCache()">
            <option value="Everyone">Everyone</option>
            <option value="New accounts only">New accounts only</option>
            <option value="Following">People I follow</option>
            <option value="Followers">People who follow me</option>
            <option value="Mutuals">Mutuals</option>
          </select>
        </div>
      </div>
    </div>
  </section>

  <section class="collapsible-section" data-collapse-id="contentCalendar">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Monthly Content Calendar</h2><p>Plan the post, then let Sidekick align engagement around it.</p></div><span class="collapse-icon" id="contentCalendarIcon">−</span>
    </div>

    <div class="card today-post-card" id="todayPostSummary"></div>

    <div class="card">
      <div class="calendar-toolbar">
        <button class="ghost" onclick="calendarPrev()">‹ Previous</button>
        <div class="calendar-title" id="calendarTitle"></div>
        <button class="ghost" onclick="calendarNext()">Next ›</button>
      </div>
      <div class="calendar-grid" id="calendarGrid"></div>
    </div>

    <div class="card calendar-form">
      <div class="section-head">
        <div><h2 style="font-size:1rem">Post planner</h2><p id="selectedDateLabel">Select a date.</p></div>
      </div>
      <div class="controls">
        <div>
          <label>Series / content type</label>
          <input id="calSeries" placeholder="Okay This Place Though, Vacation Confession...">
        </div>
        <div>
          <label>Destination / topic</label>
          <input id="calDestination" placeholder="Çeşme, Turkey or general travel">
        </div>
        <div>
          <label>Status</label>
          <select id="calStatus">
            <option>Idea</option>
            <option>Creating</option>
            <option>Ready</option>
            <option>Scheduled</option>
            <option>Posted</option>
          </select>
        </div>
        <div>
          <label>Post time</label>
          <input id="calTime" type="time">
        </div>
        <div class="full">
          <label>Platforms</label>
          <div class="platforms">
            <label><input type="checkbox" id="platIG" checked> Instagram</label>
            <label><input type="checkbox" id="platFB"> Facebook</label>
          </div>
        </div>
        <div class="full">
          <label>Notes / hook / caption status</label>
          <textarea id="calNotes" placeholder="Hook idea, caption notes, creative status, CTA..."></textarea>
        </div>
      </div>
      <div class="actions">
        <button class="primary" onclick="saveCalendarPost()">Save post</button>
        <button class="ghost" onclick="clearCalendarForm()">Clear form</button>
      </div>
      <div class="postlist" id="selectedDatePosts"></div>
    </div>
  </section>

  <section class="collapsible-section" data-collapse-id="dailyChecklist">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Daily IG Engagement Checklist</h2><p>Your finite daily routine. Check it off and be done.</p></div><span class="collapse-icon" id="dailyChecklistIcon">−</span>
    </div>
    <div class="card">
      <div class="row"><span class="badge green" id="checklistCount">0/0 complete</span><span class="badge gold" id="checklistDate"></span></div>
      <div class="checklist-progress"><div id="checklistBar"></div></div>
    </div>
    <div class="card" id="dailyChecklistBody"></div>
    <div class="actions">
      <button class="gold" onclick="refreshChecklistAccounts()">Refresh suggested accounts</button>
      <button class="ghost" onclick="resetChecklistToday()">Reset today</button>
    </div>
  </section>

  <section class="collapsible-section" data-collapse-id="section1">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Discover accounts</h2><p>Search by destination, niche, or relationship type.</p></div><span class="collapse-icon" id="section1Icon">−</span>
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

  <section class="collapsible-section" data-collapse-id="section2">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Discovery results</h2><p>Only stronger matches make the cut, with Smart Mix keeping the list varied.</p></div><span class="collapse-icon" id="section2Icon">−</span>
    </div>
    <div id="results"><div class="empty">Run a search to find candidates.</div></div>
  </section>

  <section class="collapsible-section" data-collapse-id="section3">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Today's 10</h2><p>Sidekick builds a balanced list from the accounts you've saved.</p></div><span class="collapse-icon" id="section3Icon">−</span>
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

  <section class="collapsible-section" data-collapse-id="commentAssistant">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Comment Assistant</h2><p>Paste a post caption and get natural engagement ideas you can actually use.</p></div><span class="collapse-icon" id="commentAssistantIcon">−</span>
    </div>
    <div class="card comment-assist">
      <div class="controls">
        <div>
          <label>Instagram account</label>
          <input id="commentHandle" placeholder="@hotelhandle">
        </div>
        <div>
          <label>What are you trying to do?</label>
          <select id="commentGoal">
            <option>Be social</option>
            <option>Start a conversation</option>
            <option>Build a travel-industry relationship</option>
            <option>Potential client</option>
            <option>Existing follower</option>
          </select>
        </div>
        <div class="full">
          <label>Paste their post caption</label>
          <textarea id="sourceCaption" placeholder="Paste the Instagram caption here..."></textarea>
        </div>
      </div>
      <div class="actions">
        <button class="primary" onclick="generateComments()">Give me comment ideas</button>
        <button class="ghost" onclick="clearCommentAssistant()">Clear</button>
      </div>
    </div>
    <div id="commentResults"></div>
  </section>

  <section class="collapsible-section" data-collapse-id="section4">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Engagement Tracker</h2><p>Log what you actually did so Sidekick can keep the relationship history straight.</p></div><span class="collapse-icon" id="section4Icon">−</span>
    </div>
    <div class="card">
      <div class="mix">
        <div class="mixbox"><b id="weekLikes">0</b><span>Likes this week</span></div>
        <div class="mixbox"><b id="weekComments">0</b><span>Comments this week</span></div>
        <div class="mixbox"><b id="weekShares">0</b><span>Shares this week</span></div>
        <div class="mixbox"><b id="weekDMs">0</b><span>DMs this week</span></div>
      </div>
    </div>
    <div class="tabs" id="destinationTabs"></div>
    <div id="engagementTracker"></div>
  </section>

  <section class="collapsible-section" data-collapse-id="section5">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Saved relationships</h2><p>Accounts you've decided are worth keeping in your orbit.</p></div><span class="collapse-icon" id="section5Icon">−</span>
    </div>
    <div class="tabs" id="tabs"></div>
    <div id="saved"></div>
  </section>

  <section class="collapsible-section" data-collapse-id="section6">
    <div class="section-head" onclick="toggleMajorSection(this)">
      <div><h2>Caption Tag Bank</h2><p>Keep useful Instagram handles ready for captions, credits, and destination posts.</p></div><span class="collapse-icon" id="section6Icon">−</span>
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
let activeDestination="All";

function esc(s){return String(s||"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]))}
function dayKey(){return new Date().toISOString().slice(0,10)}
function store(){localStorage.setItem(SAVED_KEY,JSON.stringify(saved))}
function categoryIcon(c){
  return {"hotel":"🏨","tourism":"📍","dmc":"🧭","food":"🍽️","photo":"📸","traveler":"✈️","other":"✨"}[c]||"✨"
}

const COLLAPSE_KEY="mme_sidekick_major_collapsed";

function majorCollapseState(){
  try{return JSON.parse(localStorage.getItem(COLLAPSE_KEY)||"{}")}catch{return {}}
}

function toggleMajorSection(header){
  const section=header.closest(".collapsible-section");
  if(!section)return;
  const id=section.dataset.collapseId;
  const collapsed=!section.classList.contains("collapsed");
  section.classList.toggle("collapsed",collapsed);
  const icon=document.getElementById(id+"Icon");
  if(icon)icon.textContent=collapsed?"+":"−";
  const st=majorCollapseState();
  st[id]=collapsed;
  localStorage.setItem(COLLAPSE_KEY,JSON.stringify(st));
}

function applyMajorCollapseState(){
  const st=majorCollapseState();
  document.querySelectorAll(".collapsible-section").forEach(section=>{
    const id=section.dataset.collapseId;
    if(st[id]){
      section.classList.add("collapsed");
      const icon=document.getElementById(id+"Icon");
      if(icon)icon.textContent="+";
    }
  });
}




const IG_REL_KEY="mme_sidekick_instagram_relationships";
let lastDiscoveryResults=[];

function igRelState(){
  try{
    const x=JSON.parse(localStorage.getItem(IG_REL_KEY)||'{"following":[],"followers":[],"imported":""}');
    x.following=Array.isArray(x.following)?x.following:[];
    x.followers=Array.isArray(x.followers)?x.followers:[];
    return x;
  }catch{return {following:[],followers:[],imported:""}}
}
function normalizeIGHandle(h){
  h=String(h||"").trim().toLowerCase().replace(/^@/,"").replace(/\/$/,"");
  return h;
}
function relationshipFor(handle){
  const st=igRelState(),h=normalizeIGHandle(handle);
  const following=st.following.includes(h), follower=st.followers.includes(h);
  if(following&&follower)return "Mutual";
  if(following)return "Following";
  if(follower)return "Follows You";
  return "New Account";
}
function relationshipBadge(handle){
  const rel=relationshipFor(handle);
  const cls=rel==="Mutual"?"rel-mutual":rel==="Following"?"rel-following":rel==="Follows You"?"rel-follower":"rel-new";
  const icon=rel==="Mutual"?"↔":rel==="Following"?"✓":rel==="Follows You"?"♥":"＋";
  return `<span class="relationship-badge ${cls}">${icon} ${esc(rel)}</span>`;
}
function extractFollowersJSON(obj){
  const out=new Set();

  // Current Meta followers export is typically a top-level array.
  const rows=Array.isArray(obj)?obj:(obj&&Array.isArray(obj.relationships_followers)?obj.relationships_followers:[]);
  rows.forEach(row=>{
    const items=Array.isArray(row?.string_list_data)?row.string_list_data:[];
    items.forEach(item=>{
      if(item&&typeof item.value==="string"&&item.value.trim()){
        out.add(normalizeIGHandle(item.value));
      }else if(item&&typeof item.href==="string"){
        const m=item.href.match(/instagram\.com\/(?:_u\/)?([^/?#]+)/i);
        if(m)out.add(normalizeIGHandle(m[1]));
      }
    });
  });
  return out;
}

function extractFollowingJSON(obj){
  const out=new Set();

  // Current Meta following export wraps rows in relationships_following.
  const rows=(obj&&Array.isArray(obj.relationships_following))
    ? obj.relationships_following
    : (Array.isArray(obj)?obj:[]);

  rows.forEach(row=>{
    if(row&&typeof row.title==="string"&&row.title.trim()){
      out.add(normalizeIGHandle(row.title));
      return;
    }
    const items=Array.isArray(row?.string_list_data)?row.string_list_data:[];
    items.forEach(item=>{
      if(item&&typeof item.value==="string"&&item.value.trim()){
        out.add(normalizeIGHandle(item.value));
      }else if(item&&typeof item.href==="string"){
        const m=item.href.match(/instagram\.com\/(?:_u\/)?([^/?#]+)/i);
        if(m)out.add(normalizeIGHandle(m[1]));
      }
    });
  });
  return out;
}

function extractHandlesFromHTML(text){
  const out=new Set();
  const re=/instagram\.com\/(?:_u\/)?([^/"'?#<\s]+)/gi;let m;
  while((m=re.exec(text)))out.add(normalizeIGHandle(m[1]));
  return out;
}

async function importInstagramData(){
  const files=[...document.getElementById("igDataFiles").files];
  if(!files.length){showToast("Choose Instagram files first");return}

  const following=new Set();
  const followers=new Set();
  const ignored=[];

  for(const file of files){
    const name=file.name.toLowerCase();
    const text=await file.text();

    try{
      if(name.endsWith(".json")){
        const obj=JSON.parse(text);

        if(name==="following.json" || (/following/i.test(name)&&!/followers/i.test(name))){
          extractFollowingJSON(obj).forEach(h=>following.add(h));
        }else if(/followers?/i.test(name)){
          extractFollowersJSON(obj).forEach(h=>followers.add(h));
        }else{
          ignored.push(file.name);
        }
      }else if(name.endsWith(".html")||name.endsWith(".htm")){
        const handles=extractHandlesFromHTML(text);
        if(/following/i.test(name)&&!/followers/i.test(name)){
          handles.forEach(h=>following.add(h));
        }else if(/followers?/i.test(name)){
          handles.forEach(h=>followers.add(h));
        }else{
          ignored.push(file.name);
        }
      }
    }catch(e){
      ignored.push(file.name);
    }
  }

  const followerSet=new Set(followers);
  const mutual=[...following].filter(h=>followerSet.has(h)).length;

  // Replace the previous snapshot so counts match the newest export.
  const state={
    following:[...following].filter(Boolean).sort(),
    followers:[...followers].filter(Boolean).sort(),
    imported:new Date().toISOString()
  };

  localStorage.setItem(IG_REL_KEY,JSON.stringify(state));
  renderAll();
  renderDiscoveryFromCache();

  let msg=`Imported ${state.following.length} following, ${state.followers.length} followers, ${mutual} mutuals`;
  if(ignored.length)msg+=` · ignored ${ignored.length} unrelated file${ignored.length===1?"":"s"}`;
  showToast(msg);
}

function clearInstagramData(){
  localStorage.removeItem(IG_REL_KEY);renderAll();renderDiscoveryFromCache();showToast("Instagram data cleared");
}
function renderIGSummary(){
  const st=igRelState();
  const a=new Set(st.following),b=new Set(st.followers);
  const mutual=[...a].filter(x=>b.has(x)).length;
  igFollowingCount.textContent=st.following.length;
  igFollowerCount.textContent=st.followers.length;
  igMutualCount.textContent=mutual;
  igImportedDate.textContent=st.imported?new Date(st.imported).toLocaleDateString(undefined,{month:"short",day:"numeric"}):"Never";
}
function passesRelationshipFilter(a){
  const f=document.getElementById("relationshipFilter")?.value||"Everyone";
  const rel=relationshipFor(a.handle);
  if(f==="Everyone")return true;
  if(f==="New accounts only")return rel==="New Account";
  if(f==="Following")return rel==="Following"||rel==="Mutual";
  if(f==="Followers")return rel==="Follows You"||rel==="Mutual";
  if(f==="Mutuals")return rel==="Mutual";
  return true;
}
function renderDiscoveryFromCache(){
  if(!lastDiscoveryResults.length)return;
  const arr=lastDiscoveryResults.filter(passesRelationshipFilter);
  if(!arr.length){results.innerHTML='<div class="empty">No accounts match that relationship filter.</div>';return}
  results.innerHTML=arr.map(a=>`
    <div class="card result">
      <div class="row">
        <span class="badge score">${a.score}% fit</span>
        <span class="badge">${esc(a.bucket)}</span>
        <span class="badge gold">${categoryIcon(a.type)} ${esc(a.type_label)}</span>
        ${relationshipBadge(a.handle)}
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

const CALENDAR_KEY="mme_sidekick_content_calendar";
const AUGUST_2026_SEED={"2026-08-01": [{"id": "aug2026-01", "series": "EscapeScore", "destination": "Martha’s Vineyard", "status": "Idea", "time": "", "notes": "EscapeScore: Martha’s Vineyard (summer edition)", "platforms": ["Instagram", "Facebook"]}], "2026-08-02": [{"id": "aug2026-02", "series": "Destination Flirtation", "destination": "General travel", "status": "Idea", "time": "", "notes": "POV: I’m the kind of destination that ruins you for other places.", "platforms": ["Instagram", "Facebook"]}], "2026-08-03": [{"id": "aug2026-03", "series": "Vacation Confessions", "destination": "General travel", "status": "Idea", "time": "", "notes": "Confession: I gatekeep this place a lot. (But not today.)", "platforms": ["Instagram", "Facebook"]}], "2026-08-04": [{"id": "aug2026-04", "series": "I’m Gonna Hold Your Hand While I Tell You This...", "destination": "International flights", "status": "Idea", "time": "", "notes": "If you book your own international flights, read this first.", "platforms": ["Instagram", "Facebook"]}], "2026-08-05": [{"id": "aug2026-05", "series": "I Know Just the Place", "destination": "Coastal getaway", "status": "Idea", "time": "", "notes": "You said: coastal town, amazing food, good vibes. I know just the place.", "platforms": ["Instagram", "Facebook"]}], "2026-08-06": [{"id": "aug2026-06", "series": "Okay, But What About...?", "destination": "Destination alternative", "status": "Idea", "time": "", "notes": "Okay, but what about going here instead?", "platforms": ["Instagram", "Facebook"]}], "2026-08-07": [{"id": "aug2026-07", "series": "Here’s the Game Plan", "destination": "Kotor, Montenegro", "status": "Idea", "time": "", "notes": "5 days in Kotor, Montenegro: where we’re staying, what we’re doing, what it costs.", "platforms": ["Instagram", "Facebook"]}], "2026-08-08": [{"id": "aug2026-08", "series": "Okay, This Place Though...", "destination": "Çeşme, Turkey", "status": "Scheduled", "time": "", "notes": "Okay, this place though... Çeşme, Turkey.", "platforms": ["Instagram", "Facebook"]}], "2026-08-09": [{"id": "aug2026-09", "series": "So, I Did Something...", "destination": "Italy", "status": "Idea", "time": "", "notes": "So, I did something... 10 people. Italy. A 50th birthday. Here’s what I came up with.", "platforms": ["Instagram", "Facebook"]}], "2026-08-10": [{"id": "aug2026-10", "series": "She’s a 10, But...", "destination": "Vacation personality", "status": "Idea", "time": "", "notes": "She wants a 6 AM flight on vacation. Unreal.", "platforms": ["Instagram", "Facebook"]}], "2026-08-11": [{"id": "aug2026-11", "series": "EscapeScore", "destination": "Quebec City", "status": "Idea", "time": "", "notes": "EscapeScore: Quebec City (long weekend edition)", "platforms": ["Instagram", "Facebook"]}], "2026-08-12": [{"id": "aug2026-12", "series": "Vacation Confessions", "destination": "Travel habits", "status": "Idea", "time": "", "notes": "Confession: I judge you if you skip this when you travel.", "platforms": ["Instagram", "Facebook"]}], "2026-08-13": [{"id": "aug2026-13", "series": "I’m Gonna Hold Your Hand While I Tell You This...", "destination": "Travel insurance", "status": "Idea", "time": "", "notes": "Travel insurance: boring to buy, amazing to have.", "platforms": ["Instagram", "Facebook"]}], "2026-08-14": [{"id": "aug2026-14", "series": "I Know Just the Place", "destination": "Europe in September", "status": "Idea", "time": "", "notes": "You said: Europe in September, great food, minimal walking.", "platforms": ["Instagram", "Facebook"]}], "2026-08-15": [{"id": "aug2026-15", "series": "Okay, But What About...?", "destination": "Stopover travel", "status": "Idea", "time": "", "notes": "Okay, but what about adding a stop here on your way?", "platforms": ["Instagram", "Facebook"]}], "2026-08-16": [{"id": "aug2026-16", "series": "Here’s the Game Plan", "destination": "Amalfi Coast", "status": "Idea", "time": "", "notes": "7 days in the Amalfi Coast: the plan, the hotels, the numbers.", "platforms": ["Instagram", "Facebook"]}], "2026-08-17": [{"id": "aug2026-17", "series": "Okay, This Place Though...", "destination": "San Sebastián", "status": "Idea", "time": "", "notes": "Okay, this place though... San Sebastián.", "platforms": ["Instagram", "Facebook"]}], "2026-08-18": [{"id": "aug2026-18", "series": "So, I Did Something...", "destination": "Tulum", "status": "Idea", "time": "", "notes": "So, I did something... Girls’ trip to Tulum. Here’s the vibe & the plan.", "platforms": ["Instagram", "Facebook"]}], "2026-08-19": [{"id": "aug2026-19", "series": "Destination Flirtation", "destination": "Fall travel", "status": "Idea", "time": "", "notes": "The fall destination I’m already manifesting.", "platforms": ["Instagram", "Facebook"]}], "2026-08-20": [{"id": "aug2026-20", "series": "EscapeScore", "destination": "Charleston", "status": "Idea", "time": "", "notes": "EscapeScore: Charleston (late summer edition)", "platforms": ["Instagram", "Facebook"]}], "2026-08-21": [{"id": "aug2026-21", "series": "Vacation Confessions", "destination": "Travel spending", "status": "Idea", "time": "", "notes": "Confession: I’ll always spend more money on this.", "platforms": ["Instagram", "Facebook"]}], "2026-08-22": [{"id": "aug2026-22", "series": "I’m Gonna Hold Your Hand While I Tell You This...", "destination": "Packing", "status": "Idea", "time": "", "notes": "Don’t make this packing mistake. Learn from me.", "platforms": ["Instagram", "Facebook"]}], "2026-08-23": [{"id": "aug2026-23", "series": "I Know Just the Place", "destination": "Warm-water getaway", "status": "Idea", "time": "", "notes": "You said: warm water, great food, easy vacation. I know just the place.", "platforms": ["Instagram", "Facebook"]}], "2026-08-24": [{"id": "aug2026-24", "series": "Okay, But What About...?", "destination": "Destination alternative", "status": "Idea", "time": "", "notes": "Okay, but what about a different vibe altogether?", "platforms": ["Instagram", "Facebook"]}], "2026-08-25": [{"id": "aug2026-25", "series": "Here’s the Game Plan", "destination": "Chicago", "status": "Idea", "time": "", "notes": "3 days in Chicago: the plan, the spots, what it costs.", "platforms": ["Instagram", "Facebook"]}], "2026-08-26": [{"id": "aug2026-26", "series": "Okay, This Place Though...", "destination": "Lake Bled, Slovenia", "status": "Idea", "time": "", "notes": "Okay, this place though... Lake Bled, Slovenia.", "platforms": ["Instagram", "Facebook"]}], "2026-08-27": [{"id": "aug2026-27", "series": "So, I Did Something...", "destination": "Bali", "status": "Idea", "time": "", "notes": "So, I did something... Honeymoon in Bali. Here’s what I planned.", "platforms": ["Instagram", "Facebook"]}], "2026-08-28": [{"id": "aug2026-28", "series": "Destination Flirtation", "destination": "Romantic hotel", "status": "Idea", "time": "", "notes": "The hotel I’m romantically obsessed with right now.", "platforms": ["Instagram", "Facebook"]}], "2026-08-29": [{"id": "aug2026-29", "series": "EscapeScore", "destination": "Bali vs. Maldives", "status": "Idea", "time": "", "notes": "EscapeScore: Bali vs. Maldives (which is better?)", "platforms": ["Instagram", "Facebook"]}], "2026-08-30": [{"id": "aug2026-30", "series": "I’m Gonna Hold Your Hand While I Tell You This...", "destination": "Travel upgrades", "status": "Idea", "time": "", "notes": "How to get an upgrade (without being annoying).", "platforms": ["Instagram", "Facebook"]}], "2026-08-31": [{"id": "aug2026-31", "series": "Okay, So Get This...", "destination": "Travel news", "status": "Idea", "time": "", "notes": "A new nonstop route from the U.S. just dropped. Details you need to know.", "platforms": ["Instagram", "Facebook"]}]};

function seedAugust2026Calendar(){
  const cal=calendarStore();
  let changed=false;
  Object.entries(AUGUST_2026_SEED).forEach(([key,posts])=>{
    if(!Array.isArray(cal[key]) || cal[key].length===0){
      cal[key]=posts;
      changed=true;
    }
  });
  if(changed)saveCalendarStore(cal);
}

let calendarViewDate=new Date();
calendarViewDate.setDate(1);
let selectedCalendarDate=dayKey();

function calendarStore(){
  try{return JSON.parse(localStorage.getItem(CALENDAR_KEY)||"{}")}catch{return {}}
}
function saveCalendarStore(obj){localStorage.setItem(CALENDAR_KEY,JSON.stringify(obj))}
function dateKeyLocal(d){
  const y=d.getFullYear(),m=String(d.getMonth()+1).padStart(2,"0"),day=String(d.getDate()).padStart(2,"0");
  return `${y}-${m}-${day}`;
}
function prettyCalendarDate(key){
  const d=new Date(key+"T12:00:00");
  return d.toLocaleDateString(undefined,{weekday:"long",month:"long",day:"numeric",year:"numeric"});
}
function postsForDate(key){
  const cal=calendarStore();
  return Array.isArray(cal[key])?cal[key]:[];
}
function todayContentPosts(){
  return postsForDate(dayKey());
}
function primaryTodayPost(){
  const posts=todayContentPosts();
  if(!posts.length)return null;
  const order={"Posted":5,"Scheduled":4,"Ready":3,"Creating":2,"Idea":1};
  return [...posts].sort((a,b)=>(order[b.status]||0)-(order[a.status]||0))[0];
}
function activeContentDestination(){
  const p=primaryTodayPost();
  return p?.destination?.trim()||"";
}

function calendarPrev(){calendarViewDate.setMonth(calendarViewDate.getMonth()-1);renderCalendar()}
function calendarNext(){calendarViewDate.setMonth(calendarViewDate.getMonth()+1);renderCalendar()}
function selectCalendarDate(key){
  selectedCalendarDate=key;
  const d=new Date(key+"T12:00:00");
  calendarViewDate=new Date(d.getFullYear(),d.getMonth(),1);
  clearCalendarForm();
  renderCalendar();
}
function clearCalendarForm(){
  calSeries.value="";calDestination.value="";calStatus.value="Idea";calTime.value="";calNotes.value="";
  platIG.checked=true;platFB.checked=false;
}
function editCalendarPost(key,id){
  const p=postsForDate(key).find(x=>x.id===id);if(!p)return;
  selectedCalendarDate=key;
  calSeries.value=p.series||"";
  calDestination.value=p.destination||"";
  calStatus.value=p.status||"Idea";
  calTime.value=p.time||"";
  calNotes.value=p.notes||"";
  platIG.checked=(p.platforms||[]).includes("Instagram");
  platFB.checked=(p.platforms||[]).includes("Facebook");
  calSeries.dataset.editId=id;
  renderCalendar();
}
function saveCalendarPost(){
  if(!selectedCalendarDate){showToast("Select a date first");return}
  const series=calSeries.value.trim();
  const destination=calDestination.value.trim();
  if(!series&&!destination){showToast("Add a series or topic");return}
  const cal=calendarStore();
  if(!Array.isArray(cal[selectedCalendarDate]))cal[selectedCalendarDate]=[];
  const platforms=[];
  if(platIG.checked)platforms.push("Instagram");
  if(platFB.checked)platforms.push("Facebook");
  const editId=calSeries.dataset.editId||"";
  const post={
    id:editId||String(Date.now()),
    series,
    destination,
    status:calStatus.value,
    time:calTime.value,
    notes:calNotes.value.trim(),
    platforms
  };
  const idx=cal[selectedCalendarDate].findIndex(x=>x.id===post.id);
  if(idx>=0)cal[selectedCalendarDate][idx]=post; else cal[selectedCalendarDate].push(post);
  saveCalendarStore(cal);
  delete calSeries.dataset.editId;
  clearCalendarForm();
  renderAll();
  refreshChecklistAccounts();
  showToast("Calendar post saved");
}
function deleteCalendarPost(key,id){
  const cal=calendarStore();
  cal[key]=(cal[key]||[]).filter(x=>x.id!==id);
  if(!cal[key].length)delete cal[key];
  saveCalendarStore(cal);
  renderAll();
  showToast("Post removed");
}
function markCalendarPosted(key,id){
  const cal=calendarStore();
  const p=(cal[key]||[]).find(x=>x.id===id);
  if(p)p.status="Posted";
  saveCalendarStore(cal);
  renderAll();
  refreshChecklistAccounts();
  showToast("Marked posted");
}
function renderCalendar(){
  const y=calendarViewDate.getFullYear(),m=calendarViewDate.getMonth();
  calendarTitle.textContent=calendarViewDate.toLocaleDateString(undefined,{month:"long",year:"numeric"});
  const first=new Date(y,m,1), last=new Date(y,m+1,0);
  const start=new Date(first);
  start.setDate(first.getDate()-first.getDay());
  const cells=[];
  ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].forEach(d=>cells.push(`<div class="cal-dow">${d}</div>`));
  const cur=new Date(start);
  for(let i=0;i<42;i++){
    const key=dateKeyLocal(cur);
    const posts=postsForDate(key);
    const cls=[
      "cal-day",
      cur.getMonth()!==m?"other":"",
      key===dayKey()?"today":"",
      key===selectedCalendarDate?"selected":""
    ].join(" ");
    const previews=posts.slice(0,2).map(p=>`<div class="cal-post ${(p.status||"").toLowerCase()}">${esc(p.series||p.destination||"Post")}</div>`).join("");
    const more=posts.length>2?`<div class="meta">+${posts.length-2} more</div>`:"";
    cells.push(`<div class="${cls}" onclick="selectCalendarDate('${key}')"><div class="cal-num">${cur.getDate()}</div>${previews}${more}</div>`);
    cur.setDate(cur.getDate()+1);
  }
  calendarGrid.innerHTML=cells.join("");
  selectedDateLabel.textContent=prettyCalendarDate(selectedCalendarDate);
  const selected=postsForDate(selectedCalendarDate);
  selectedDatePosts.innerHTML=selected.length?selected.map(p=>`
    <div class="postitem">
      <div class="row"><span class="status-pill ${esc(p.status)}">${esc(p.status)}</span><b>${esc(p.series||"Untitled post")}</b>${p.destination?`<span class="badge gold">📍 ${esc(p.destination)}</span>`:""}</div>
      <div class="meta">${esc((p.platforms||[]).join(" + "))}${p.time?" · "+esc(p.time):""}</div>
      ${p.notes?`<div class="reason">${esc(p.notes)}</div>`:""}
      <div class="actions">
        <button class="secondary" onclick="editCalendarPost('${selectedCalendarDate}','${p.id}')">Edit</button>
        ${p.status!=="Posted"?`<button class="gold" onclick="markCalendarPosted('${selectedCalendarDate}','${p.id}')">Mark posted</button>`:""}
        <button class="ghost" onclick="deleteCalendarPost('${selectedCalendarDate}','${p.id}')">Delete</button>
      </div>
    </div>`).join(""):'<div class="empty">No posts planned for this date yet.</div>';
  renderTodayPostSummary();
}
function renderTodayPostSummary(){
  const posts=todayContentPosts();
  const root=document.getElementById("todayPostSummary");
  if(!posts.length){
    root.innerHTML='<div class="row"><span class="badge">Today</span><b>No content scheduled today</b></div><div class="meta">Your engagement checklist will use the normal saved-account mix.</div>';
    return;
  }
  const p=primaryTodayPost();
  root.innerHTML=`<div class="row"><span class="badge score">Today's post</span><span class="status-pill ${esc(p.status)}">${esc(p.status)}</span><b>${esc(p.series||"Planned post")}</b></div>
  ${p.destination?`<div class="reason"><b>Destination/topic:</b> ${esc(p.destination)}</div>`:""}
  <div class="meta">${esc((p.platforms||[]).join(" + "))}${p.time?" · "+esc(p.time):""}</div>
  <div class="actions">${p.destination?`<button class="secondary" onclick="useTodayDestinationInDiscovery()">Discover accounts for this post</button>`:""}</div>`;
}
function useTodayDestinationInDiscovery(){
  const p=primaryTodayPost();if(!p)return;
  seed.value=p.destination||p.series||"";
  location.value=p.destination||"";
  category.value="Travel Partner";
  focus.value="auto";
  const discoverSection=document.querySelector('[data-collapse-id="section1"]');
  if(discoverSection)discoverSection.classList.remove("collapsed");
  showToast("Today's topic loaded into discovery");
  document.getElementById("seed").scrollIntoView({behavior:"smooth",block:"center"});
}


function openCommentForAccount(handle){
  commentHandle.value=handle||"";
  const sec=document.querySelector('[data-collapse-id="commentAssistant"]');
  if(sec)sec.classList.remove("collapsed");
  const icon=document.getElementById("commentAssistantIcon");if(icon)icon.textContent="−";
  document.getElementById("sourceCaption").focus();
  document.getElementById("commentHandle").scrollIntoView({behavior:"smooth",block:"center"});
}
function clearCommentAssistant(){
  commentHandle.value="";sourceCaption.value="";commentResults.innerHTML="";
}
async function generateComments(){
  const caption=sourceCaption.value.trim();
  if(!caption){showToast("Paste the post caption first");return}
  commentResults.innerHTML='<div class="card">Writing a few options...</div>';
  const r=await fetch("/api/comment-suggestions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
    handle:commentHandle.value.trim(),caption,goal:commentGoal.value
  })});
  const x=await r.json();
  if(!r.ok){commentResults.innerHTML='<div class="card notice">'+esc(x.error||"Could not generate comments.")+'</div>';return}
  commentResults.innerHTML=`<div class="comment-grid">${x.suggestions.map(s=>`
    <div class="comment-option">
      <b>${esc(s.label)}</b>
      <div class="comment-text">${esc(s.text)}</div>
      <button class="secondary" onclick='copySuggestedComment(${JSON.stringify(JSON.stringify(s.text))})'>Copy</button>
    </div>`).join("")}</div>`;
}
function copySuggestedComment(raw){
  const text=JSON.parse(raw);
  navigator.clipboard.writeText(text);
  showToast("Comment copied");
}

const CHECKLIST_KEY="mme_sidekick_daily_checklist";
const CHECKLIST_DATE_KEY="mme_sidekick_daily_checklist_date";

function checklistDateKey(){return dayKey()}

function baseChecklist(){
  return [
    {id:"reply_comments",label:"Reply to comments on your recent posts",detail:"Clear anything that deserves a real response.",kind:"routine"},
    {id:"reply_dms",label:"Reply to Instagram DMs",detail:"Respond to active conversations before starting new engagement.",kind:"routine"},
    {id:"stories",label:"Engage with 2 Stories",detail:"Use genuine replies when there is something worth responding to.",kind:"routine"},
    {id:"support_today_post",label:"Support today’s planned content",detail:"Engage with accounts related to today’s destination/topic before or after posting.",kind:"routine"},
    {id:"account_1",label:"Engage with suggested account #1",detail:"Open the profile, look at something current, and leave a meaningful interaction.",kind:"account"},
    {id:"account_2",label:"Engage with suggested account #2",detail:"Open the profile, look at something current, and leave a meaningful interaction.",kind:"account"},
    {id:"account_3",label:"Engage with suggested account #3",detail:"Open the profile, look at something current, and leave a meaningful interaction.",kind:"account"},
    {id:"account_4",label:"Engage with suggested account #4",detail:"Open the profile, look at something current, and leave a meaningful interaction.",kind:"account"},
    {id:"account_5",label:"Engage with suggested account #5",detail:"Open the profile, look at something current, and leave a meaningful interaction.",kind:"account"},
    {id:"caption_bank",label:"Save any useful handle you found today",detail:"Add good accounts to your relationship list or Caption Tag Bank.",kind:"routine"},
    {id:"done",label:"Close Instagram when the checklist is done",detail:"You are finished for today. No endless scrolling required.",kind:"routine"}
  ];
}

function checklistState(){
  if(localStorage.getItem(CHECKLIST_DATE_KEY)!==checklistDateKey()){
    localStorage.setItem(CHECKLIST_DATE_KEY,checklistDateKey());
    localStorage.setItem(CHECKLIST_KEY,JSON.stringify({done:{},accounts:[]}));
  }
  let st;
  try{st=JSON.parse(localStorage.getItem(CHECKLIST_KEY)||'{"done":{},"accounts":[]}')}catch{st={done:{},accounts:[]}}
  if(!st.done)st.done={};
  if(!Array.isArray(st.accounts))st.accounts=[];
  return st;
}

function saveChecklistState(st){
  localStorage.setItem(CHECKLIST_DATE_KEY,checklistDateKey());
  localStorage.setItem(CHECKLIST_KEY,JSON.stringify(st));
}

function suggestedChecklistAccounts(){
  buildToday(false);
  const contentDest=activeContentDestination().toLowerCase();
  const ids=todayIds();
  let base=ids.map(h=>saved.find(a=>a.handle===h)).filter(Boolean);

  if(contentDest){
    const relevant=[...saved].filter(a=>{
      const dest=(a.destination||a.location_hint||"").toLowerCase();
      const reason=(a.reason||"").toLowerCase();
      return dest.includes(contentDest)||contentDest.includes(dest)||reason.includes(contentDest);
    }).sort((a,b)=>b.score-a.score);
    const used=new Set();
    const merged=[];
    [...relevant,...base,...saved.sort((a,b)=>b.score-a.score)].forEach(a=>{
      if(a&&!used.has(a.handle)){used.add(a.handle);merged.push(a)}
    });
    base=merged;
  }

  if(base.length<5){
    const used=new Set(base.map(a=>a.handle));
    const extras=[...saved].filter(a=>!used.has(a.handle)).sort((a,b)=>b.score-a.score);
    base.push(...extras.slice(0,5-base.length));
  }
  return base.slice(0,5).map(a=>({handle:a.handle,url:a.url,bucket:a.bucket,reason:a.reason}));
}

function refreshChecklistAccounts(){
  const st=checklistState();
  st.accounts=suggestedChecklistAccounts();
  saveChecklistState(st);
  renderDailyChecklist();
  showToast("Suggested accounts refreshed");
}

function toggleChecklist(id,checked){
  const st=checklistState();
  st.done[id]=checked;
  saveChecklistState(st);
  renderDailyChecklist();
}

function resetChecklistToday(){
  const st={done:{},accounts:suggestedChecklistAccounts()};
  saveChecklistState(st);
  renderDailyChecklist();
  showToast("Checklist reset");
}

function renderDailyChecklist(){
  const st=checklistState();
  if(!st.accounts.length)st.accounts=suggestedChecklistAccounts();
  saveChecklistState(st);
  const tasks=baseChecklist();
  let accountIndex=0;
  const html=tasks.map(t=>{
    let acct=null;
    if(t.kind==="account"){
      acct=st.accounts[accountIndex++]||null;
    }
    const checked=!!st.done[t.id];
    return `<div class="checklist-item">
      <input type="checkbox" ${checked?"checked":""} onchange="toggleChecklist('${t.id}',this.checked)">
      <div class="checklist-text">
        <b>${esc(t.label)}</b>
        <span>${esc(t.detail)}</span>
        ${acct?`<div class="checklist-account">${esc(acct.handle)} · ${esc(acct.bucket)}</div>
          <div class="meta">${esc(acct.reason||"")}</div>
          <div class="actions"><a class="btn primary" target="_blank" href="${acct.url}">Open Instagram</a><button class="secondary" onclick="openCommentForAccount(\'${acct.handle}\')">Help me comment</button></div>`:""}
      </div>
    </div>`;
  }).join("");
  document.getElementById("dailyChecklistBody").innerHTML=html;
  const total=tasks.length;
  const done=tasks.filter(t=>st.done[t.id]).length;
  document.getElementById("checklistCount").textContent=`${done}/${total} complete`;
  document.getElementById("checklistBar").style.width=(done/total*100)+"%";
  document.getElementById("checklistDate").textContent=new Date().toLocaleDateString(undefined,{weekday:"short",month:"short",day:"numeric"});
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
  lastDiscoveryResults=x.results;
  renderDiscoveryFromCache();
}
function saveCandidate(raw){
  const a=JSON.parse(raw);
  if(!saved.some(x=>x.handle.toLowerCase()===a.handle.toLowerCase())){
    a.doneToday=false;
    a.savedAt=Date.now();
    a.destination=(a.location_hint||"General").trim()||"General";
    a.relationshipStatus="New";
    a.notes="";
    a.history=[];
    a.lastEngaged="";
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
        <span class="handle">${esc(a.handle)}</span>${relationshipBadge(a.handle)}
        ${a.doneToday?'<span class="badge green">✓ Done</span>':''}
      </div>
      <div class="reason"><b>Why today:</b> ${esc(a.reason)}</div>
      <div class="actions">
        <a class="btn primary" target="_blank" href="${a.url}">Open Instagram</a>
        <button class="secondary" onclick="openCommentForAccount(\'${a.handle}\')">Help me comment</button>
        <button class="${a.doneToday?'ghost':'secondary'}" onclick="markDone('${a.handle}')">${a.doneToday?'Undo':'Mark done'}</button>
      </div>
      <div class="engagement-actions">
        <button class="engagebtn" onclick="logEngagement('${a.handle}','Liked')">❤️ Like</button>
        <button class="engagebtn" onclick="logEngagement('${a.handle}','Commented')">💬 Comment</button>
        <button class="engagebtn" onclick="logEngagement('${a.handle}','Followed')">➕ Follow</button>
        <button class="engagebtn" onclick="logEngagement('${a.handle}','Shared')">↗️ Share</button>
        <button class="engagebtn" onclick="logEngagement('${a.handle}',&quot;DM'd&quot;)">✉️ DM</button>
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
      <div class="row"><span class="badge">${esc(a.bucket)}</span><span class="badge gold">${categoryIcon(a.type)} ${esc(a.type_label)}</span><span class="handle">${esc(a.handle)}</span>${relationshipBadge(a.handle)}<span class="badge score">${a.score}%</span></div>
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


function ensureAccountFields(a){
  if(!a.destination)a.destination=(a.location_hint||"General").trim()||"General";
  if(!a.relationshipStatus)a.relationshipStatus="New";
  if(!Array.isArray(a.history))a.history=[];
  if(typeof a.notes!=="string")a.notes="";
  if(!a.lastEngaged)a.lastEngaged="";
  return a;
}

saved.forEach(ensureAccountFields);
store();

function nowLabel(){
  return new Date().toLocaleString(undefined,{month:"short",day:"numeric",hour:"numeric",minute:"2-digit"});
}

function logEngagement(handle,type){
  const a=saved.find(x=>x.handle===handle); if(!a)return;
  ensureAccountFields(a);
  const entry={type:type,date:Date.now(),label:nowLabel()};
  a.history.unshift(entry);
  a.history=a.history.slice(0,50);
  a.lastEngaged=entry.label;
  if(type==="Commented" && a.relationshipStatus==="New")a.relationshipStatus="Engaging";
  if(type==="DM'd" && ["New","Engaging"].includes(a.relationshipStatus))a.relationshipStatus="Connected";
  store();
  renderAll();
  showToast(type+" logged");
}

function setRelationshipStatus(handle,status){
  const a=saved.find(x=>x.handle===handle); if(!a)return;
  a.relationshipStatus=status;
  store(); renderAll();
}


function saveDestination(handle){
  const a=saved.find(x=>x.handle===handle); if(!a)return;
  const el=document.getElementById("dest_"+safeId(handle)); if(!el)return;
  a.destination=(el.value||"General").trim()||"General";
  store();
  renderAll();
  showToast("Destination saved");
}

function saveNotes(handle){
  const a=saved.find(x=>x.handle===handle); if(!a)return;
  const el=document.getElementById("notes_"+safeId(handle));
  if(!el)return;
  a.notes=el.value;
  store();
  showToast("Notes saved");
}

function safeId(s){
  return String(s).replace(/[^a-z0-9]/gi,"_");
}

function recentHistory(a,limit=5){
  ensureAccountFields(a);
  if(!a.history.length)return '<div class="history-item">No engagement logged yet.</div>';
  return a.history.slice(0,limit).map(h=>`<div class="history-item">• ${esc(h.type)} · ${esc(h.label)}</div>`).join("");
}

function weekStart(){
  const d=new Date(); const day=d.getDay(); const diff=(day+6)%7;
  d.setHours(0,0,0,0); d.setDate(d.getDate()-diff); return d.getTime();
}

function countThisWeek(type){
  const start=weekStart();
  return saved.reduce((sum,a)=>sum+(a.history||[]).filter(h=>h.type===type&&h.date>=start).length,0);
}

function renderEngagementStats(){
  document.getElementById("weekLikes").textContent=countThisWeek("Liked");
  document.getElementById("weekComments").textContent=countThisWeek("Commented");
  document.getElementById("weekShares").textContent=countThisWeek("Shared");
  document.getElementById("weekDMs").textContent=countThisWeek("DM'd");
}


function destinationList(){
  const vals=[...new Set(saved.map(a=>(ensureAccountFields(a),a.destination)).filter(Boolean))];
  return ["All",...vals.sort((a,b)=>a.localeCompare(b))];
}

function renderDestinationTabs(){
  const root=document.getElementById("destinationTabs");
  if(!root)return;
  root.innerHTML=destinationList().map(d=>`<button class="tab ${d===activeDestination?'active':''}" onclick='activeDestination=${JSON.stringify(d)};renderAll()'>${esc(d)}</button>`).join("");
}

function renderEngagementTracker(){
  const root=document.getElementById("engagementTracker");
  const items=saved.filter(a=>activeDestination==="All"||a.destination===activeDestination).sort((a,b)=>{
    const ad=(a.history&&a.history[0]?.date)||0;
    const bd=(b.history&&b.history[0]?.date)||0;
    return bd-ad || b.score-a.score;
  });
  root.innerHTML=items.length?items.map(a=>{
    ensureAccountFields(a);
    return `<div class="card">
      <div class="row">
        <span class="handle">${esc(a.handle)}</span>${relationshipBadge(a.handle)}
        <span class="badge">${esc(a.bucket)}</span>
        <span class="badge gold">📍 ${esc(a.destination)}</span>
        ${a.lastEngaged?`<span class="badge green">Last: ${esc(a.lastEngaged)}</span>`:'<span class="badge">Not engaged yet</span>'}
      </div>
      <div class="engagement-actions">
        <button class="engagebtn" onclick="logEngagement('${a.handle}','Liked')">❤️ Liked</button>
        <button class="engagebtn" onclick="logEngagement('${a.handle}','Commented')">💬 Commented</button>
        <button class="engagebtn" onclick="logEngagement('${a.handle}','Followed')">➕ Followed</button>
        <button class="engagebtn" onclick="logEngagement('${a.handle}','Shared')">↗️ Shared</button>
        <button class="engagebtn" onclick="logEngagement('${a.handle}',&quot;DM'd&quot;)">✉️ DM'd</button>
      </div>
      <div class="controls" style="margin-top:10px">
        <div>
          <label>Relationship status</label>
          <select class="status-select" onchange="setRelationshipStatus('${a.handle}',this.value)">
            ${["New","Engaging","Connected","Collaborator / Partner"].map(s=>`<option ${a.relationshipStatus===s?"selected":""}>${s}</option>`).join("")}
          </select>
          <label style="margin-top:8px">Destination</label>
          <input id="dest_${safeId(a.handle)}" value="${esc(a.destination)}" placeholder="Çeşme, Puglia, etc.">
          <div class="actions"><button class="secondary" onclick="saveDestination('${a.handle}')">Save destination</button></div>
        </div>
        <div>
          <label>Quick notes</label>
          <textarea id="notes_${safeId(a.handle)}" placeholder="What should Sidekick remember?">${esc(a.notes)}</textarea>
          <div class="actions"><button class="secondary" onclick="saveNotes('${a.handle}')">Save notes</button></div>
        </div>
      </div>
      <div class="history"><b style="font-size:.78rem;color:var(--deep)">Recent activity</b>${recentHistory(a)}</div>
    </div>`;
  }).join(""):'<div class="empty">Save some accounts first. Their engagement history will live here.</div>';
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

function renderAll(){renderTabs();renderSaved();renderToday();renderStats();renderTagBank();renderDestinationTabs();renderEngagementTracker();renderEngagementStats();renderIGSummary();renderCalendar();renderDailyChecklist()}
seedAugust2026Calendar();check();renderAll();applyMajorCollapseState();
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

def extract_comment_topic(caption):
    text=clean_text(caption)
    low=text.lower()
    topics=[]
    mapping=[
      ("beach",["beach","ocean","sea","water","coast"]),
      ("hotel",["hotel","resort","suite","room","property"]),
      ("food",["restaurant","dinner","lunch","food","chef","menu","breakfast"]),
      ("experience",["tour","experience","excursion","sailing","boat","hike","spa"]),
      ("destination",["travel","visit","destination","city","island","turkey","italy","greece","portugal"])
    ]
    for label,terms in mapping:
        if any(t in low for t in terms):
            topics.append(label)
    # Pull a few useful words, avoiding common filler.
    stop={"this","that","with","from","your","have","will","just","about","their","there","they","what","when","where","into","more","some","here","been","were","would","could","instagram"}
    words=[w for w in re.findall(r"[A-Za-zÀ-ÿÇçŞşĞğİıÖöÜü]+",text) if len(w)>4 and w.lower() not in stop]
    keyword=words[0] if words else ""
    return topics,keyword

@app.post("/api/comment-suggestions")
def comment_suggestions():
    data=request.get_json(force=True)
    caption=clean_text(data.get("caption",""))
    goal=data.get("goal","Be social")
    handle=data.get("handle","").strip()
    if not caption:
        return jsonify({"error":"Paste the post caption first."}),400

    topics,keyword=extract_comment_topic(caption)
    topic=topics[0] if topics else "post"

    hooks={
      "beach":"That water is seriously calling my name.",
      "hotel":"This is exactly the kind of property detail that makes a stay feel special.",
      "food":"Okay, this looks worth planning a meal around.",
      "experience":"This is the kind of experience that makes the whole trip.",
      "destination":"This is making a very strong case for adding it to the list.",
      "post":"Okay, this caught my attention."
    }
    questions={
      "beach":"Is the water usually this calm throughout the season?",
      "hotel":"What time of year do you think is best for experiencing the property?",
      "food":"Is there one thing on the menu you would tell a first-time visitor not to miss?",
      "experience":"Is this something you recommend booking well in advance?",
      "destination":"What would you tell a first-time visitor not to miss?",
      "post":"What is your favorite part of this?"
    }
    industry={
      "beach":"This is exactly the kind of setting I love finding for clients who want the destination to feel like part of the trip, not just the backdrop.",
      "hotel":"I love seeing properties with a real sense of place. This is the kind of stay I want on my radar for the right client.",
      "food":"These are the details that make an itinerary feel personal. Definitely keeping this on my radar for future clients.",
      "experience":"This is exactly the kind of experience I look for when I want an itinerary to feel more personal than a standard sightseeing list.",
      "destination":"This is exactly why I love looking beyond the obvious itinerary. Definitely keeping this on my radar for clients.",
      "post":"Love finding businesses and experiences like this to keep on my radar for future client trips."
    }

    quick=hooks.get(topic,hooks["post"])
    convo=f"{quick} {questions.get(topic,questions['post'])}"
    relation=industry.get(topic,industry["post"])

    if goal=="Start a conversation":
        quick=questions.get(topic,questions["post"])
    elif goal=="Build a travel-industry relationship":
        quick=relation
        convo=f"{relation} {questions.get(topic,questions['post'])}"
    elif goal=="Potential client":
        relation="This looks like such a good trip. What has been your favorite part so far?"
    elif goal=="Existing follower":
        relation=f"{quick} I always love seeing where people end up next."

    # Keep them conversational and avoid pretending the user personally experienced the place.
    suggestions=[
      {"label":"Quick + natural","text":quick},
      {"label":"Conversation starter","text":convo},
      {"label":"Relationship builder","text":relation}
    ]
    return jsonify({"handle":handle,"suggestions":suggestions})

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

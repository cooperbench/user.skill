#!/usr/bin/env python3
"""Faithful v1-style eval on the v2 80-dev cohort, single Gemini key.
GENERATOR: gemini-3.5-flash (temp 0.7, role-play the developer). JUDGE: gemini-3.1-pro-preview
(temp 0, 4-way move classifier) for BOTH real (gold) and predicted moves. Conditions: generic
(no profile) vs distilled (with profile). Metric: per-developer move-match accuracy, macro over
80 devs -> np / wp / lift / chance. Resumable (writes results.jsonl)."""
import json, os, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
KEY=next(l.split("=",1)[1].strip() for l in open("/data/harbor-adapters-experiments/.env") if l.startswith("GEMINI_API_KEY="))
GEN="gemini-3.5-flash"; JUDGE="gemini-3.1-pro-preview"
CATS=["approve","critical","directive","inquiry"]
def tw(t,n): w=(t or "").split(); return " ".join(w[:n])
def gemini(model,prompt,temp,mx=1500,retries=5):
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":temp,"maxOutputTokens":mx}}).encode()
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}"
    for a in range(retries):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=120))
            return "".join(p.get("text","") for p in d.get("candidates",[{}])[0].get("content",{}).get("parts",[])).strip()
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503) and a<retries-1: time.sleep(5*(a+1)); continue
            return ""
        except Exception:
            if a<retries-1: time.sleep(3); continue
            return ""
    return ""
BODY=("Classify the developer's MOVE by the observable function of their message toward the agent's previous turn. Choose exactly one:\n"
"- approve: acceptance/permission, no new content, no complaint (yes/ok/lgtm/go ahead/thanks).\n"
"- critical: asserts something is WRONG — a bug/failure/wrong output, or the approach is mistaken/unwanted.\n"
"- directive: tells the agent what to DO next with no fault stated — a new task/addition/forward steer.\n"
"- inquiry: primarily asks for information/explanation, expecting an ANSWER.\n"
"DECISION RULE (first match): 1 fault/error/dissatisfaction -> critical; 2 asks for info -> inquiry; 3 requests action/change -> directive; 4 else -> approve.")
def classify(text,prev):
    if not text: return None
    out=gemini(JUDGE,f"A developer is using an AI coding agent. The agent just said:\n<agent>{tw(prev,120)}</agent>\n\nThe developer's next message was:\n<message>{tw(text,150)}</message>\n\n{BODY}\n\nRespond with ONLY JSON: {{\"act\":\"<one label>\"}}",0)
    m=re.search(r'"act"\s*:\s*"(\w+)"',out); a=m.group(1) if m else None
    return a if a in CATS else None
TASK=("Write the developer's NEXT message to the agent. Output ONLY the literal text the developer would type — "
      "their language, length, casing, typos and all. No quotes, no commentary, no role labels.")
def gen_msg(profile,repo,context):
    prof=(f"<user_profile>\n{profile}\n</user_profile>\n\nYou are role-playing the developer described in the profile above. " if profile
          else "You are role-playing a software developer. ")
    return gemini(GEN,f"{prof}The developer is using an AI coding agent in the repository `{repo}`. The session so far:\n\n<conversation>\n{context}\n</conversation>\n\n{TASK}",0.7)

recs=json.load(open("cohort.json"))
done=set()
if os.path.exists("results.jsonl"):
    for l in open("results.jsonl"):
        try: r=json.loads(l); done.add((r["user"],r["point_id"],r["cond"]))
        except: pass
out=open("results.jsonl","a")
# jobs: gold (once per point) + gen+judge per (point,cond)
jobs=[]
for r in recs:
    for p in r["points"]:
        for cond in __import__("os").environ.get("CONDS","generic,distilled").split(","):
            if (r["user"],p["point_id"],cond) in done: continue
            jobs.append((r["user"],p,cond,r["profile"]))
print(f"{len(jobs)} (point,cond) jobs",flush=True)
import threading; lock=threading.Lock()
def run(job):
    user,p,cond,profile=job
    prof=profile if cond=="distilled" else ""
    gm=gen_msg(prof,p.get("repo","?"),p["context"])
    gold=p.get("gold_move") or classify(p["real"],p["prev_agent"])
    pred=classify(gm,p["prev_agent"]) if gm else None
    rec={"user":user,"point_id":p["point_id"],"cond":cond,"gold":gold,"pred":pred,
         "match":(pred==gold) if (pred and gold) else None}
    with lock: out.write(json.dumps(rec)+"\n"); out.flush()
    return 1
t0=time.time()
with ThreadPoolExecutor(max_workers=16) as ex:
    for i,_ in enumerate(as_completed([ex.submit(run,j) for j in jobs]),1):
        if i%200==0: print(f"{i}/{len(jobs)} ({time.time()-t0:.0f}s)",flush=True)
print("DONE",flush=True)

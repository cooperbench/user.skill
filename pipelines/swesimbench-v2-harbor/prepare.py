#!/usr/bin/env python3
"""Prepare SWESimBench v2 inputs from the canonical clean cohort artifacts."""
import json, re, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "/data/claude-crawl")
from cohort_policy import (
    POLICY_VERSION,
    is_human_target,
    policy_fingerprint,
    scrub_text,
)

OUT = "/data/swesimbench-v2-harbor"
MAX_PTS, PROFILE_TURNS = 30, 40   # context = ALL prior turns in the session
MODEL = "gemini-3.5-flash"

def judge_excerpt(t,n):
    w=scrub_text(t or "").split(); return " ".join(w[:n])+(" […]" if len(w)>n else "")
def is_action(t):
    return t.get("role")=="user" and is_human_target(t)

# Canonical clean index: metadata remains in the trace with system/tool roles,
# while secrets are already scrubbed and targets are genuine user turns only.
IDX={}
for line in open("/data/swesimbench-v2-harbor/clean_sessions.jsonl"):
    s=json.loads(line)
    IDX[s["session_id"]]=s["turns"]
clean_manifest=json.load(open("/data/swesimbench-v2-harbor/clean_manifest.json"))
assert clean_manifest["policy_version"]==POLICY_VERSION
assert clean_manifest["policy_fingerprint"]==policy_fingerprint()
man=clean_manifest["users"]

# --- gemini 4-way move classifier (gold labels) ---
TAX_BODY=open("/data/swesimbench-v2-harbor/taxonomy_body.txt").read() if os.path.exists("/data/swesimbench-v2-harbor/taxonomy_body.txt") else None
CATS=["approve","critical","directive","inquiry"]
BODY=(
"Classify the developer's MOVE by the observable function of their message toward the agent's previous turn. Choose exactly one:\n"
"- approve: acceptance/permission, no new content, no complaint (yes/ok/lgtm/go ahead/thanks).\n"
"- critical: asserts something is WRONG — a bug/failure/wrong output, or the approach is mistaken/unwanted.\n"
"- directive: tells the agent what to DO next with no fault stated — a new task/addition/forward steer.\n"
"- inquiry: primarily asks for information/explanation, expecting an ANSWER.\n"
"DECISION RULE (first match): 1 fault/error/dissatisfaction -> critical; 2 asks for info -> inquiry; 3 requests any action/change -> directive; 4 else -> approve.")
def gemini(prompt,temp=0,mx=1200):
    key=os.environ.get("GEMINI_API_KEY")
    if not key:
        env_path="/data/harbor-adapters-experiments/.env"
        if os.path.exists(env_path):
            key=next((l.split("=",1)[1].strip() for l in open(env_path) if l.startswith("GEMINI_API_KEY=")),None)
    if not key:
        raise RuntimeError("GEMINI_API_KEY is required when RUN_GOLD=1")
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":temp,"maxOutputTokens":mx}}).encode()
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    for a in range(4):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=60))
            return "".join(p.get("text","") for p in d.get("candidates",[{}])[0].get("content",{}).get("parts",[]))
        except Exception:
            time.sleep(3)
    return ""
def classify(text,prev):
    out=gemini(f"A developer is using an AI coding agent. The agent just said:\n<agent>{judge_excerpt(prev,120)}</agent>\n\nThe developer's next message was:\n<message>{judge_excerpt(text,150)}</message>\n\n{BODY}\n\nRespond with ONLY JSON: {{\"act\":\"<one label>\"}}")
    m=re.search(r'"act"\s*:\s*"(\w+)"',out); a=m.group(1) if m else None
    return a if a in CATS else None

# build per-user profile + points
records=[]
for u in man:
    train=sorted([x for x in u["train_sessions"] if x["sid"] in IDX], key=lambda x:x["ts"])
    tp=[scrub_text(t["text"]) for x in train for t in IDX[x["sid"]] if is_action(t)]
    profile="\n".join(f"- {p}" for p in tp[-PROFILE_TURNS:])
    held=sorted([x for x in u["held_sessions"] if x["sid"] in IDX], key=lambda x:x["ts"])
    pts=[]
    for x in held:
        turns=IDX[x["sid"]]
        idxs=[i for i,t in enumerate(turns) if is_action(t) and any(p.get("role")=="assistant" for p in turns[:i])]
        step=max(1,len(idxs)//3) if len(idxs)>3 else 1
        for i in idxs[::step]:
            if len([p for p in pts])>=MAX_PTS: break
            ctx=turns[:i]   # ALL previous turns in the session up to the tested turn
            prev=next((t["text"] for t in reversed(ctx) if t.get("role")=="assistant"),"")
            labels={"user":"DEVELOPER","assistant":"AGENT","system":"SYSTEM","tool":"TOOL","metadata":"METADATA"}
            block="\n\n".join(f"[{labels.get(t.get('role'),'METADATA')}]: {scrub_text(t['text'])}" for t in ctx)
            pts.append({"point_id":f"{x['sid']}#{i}","repo":x.get("repo") or "?","context":block,
                        "prev_agent":scrub_text(prev),"real":scrub_text(turns[i]["text"])})
        if len(pts)>=MAX_PTS: break
    records.append({"user":u["user"],"train_turns":u["train_turns"],"held_turns":u["held_turns"],
                    "profile":profile,"points":pts})

# classify gold moves in parallel (only if RUN_GOLD=1; else leave null for a later batched pass)
if os.environ.get("RUN_GOLD")=="1":
    jobs=[(r,p) for r in records for p in r["points"]]
    def go(rp):
        r,p=rp; p["gold_move"]=classify(p["real"],p["prev_agent"]); return 1
    with ThreadPoolExecutor(max_workers=16) as ex:
        for i,_ in enumerate(as_completed([ex.submit(go,j) for j in jobs]),1):
            if i%200==0: print(f"gold {i}/{len(jobs)}",flush=True)
json.dump(records,open(f"{OUT}/cohort.json","w"))
json.dump({"policy_version":POLICY_VERSION,
           "policy_fingerprint":clean_manifest["policy_fingerprint"],
           "cohort_fingerprint":clean_manifest["cohort_fingerprint"],
           "developers":len(records),
           "points":sum(len(r["points"]) for r in records),
           "message_fidelity":"full"},
          open(f"{OUT}/cohort.meta.json","w"),indent=2)
print(f"prepared {len(records)} developers, {sum(len(r['points']) for r in records)} points -> cohort.json")

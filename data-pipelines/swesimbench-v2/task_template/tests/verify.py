#!/usr/bin/env python3
"""SWESimBench v2 verifier. Reads /sim/predictions.jsonl (agent output) + tests/gold.jsonl
(hidden). For each point: classify the predicted message's move (4-way taxonomy, pinned judge
model via gemini) and compare to gold. Reward = developer's move-match accuracy. Emits
/sim/verdict.json and asserts reward is computable."""
import json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE=os.path.dirname(os.path.abspath(__file__))
KEY=os.environ.get("GEMINI_API_KEY","")
JUDGE=os.environ.get("SIMBENCH_JUDGE","gemini-3.5-flash")
CATS=["approve","critical","directive","inquiry"]
BODY=("Classify the developer's MOVE by the observable function of their message. Choose one:\n"
"- approve: acceptance/permission, no new content, no complaint.\n- critical: asserts something is WRONG.\n"
"- directive: tells the agent what to DO next, no fault stated.\n- inquiry: asks for information, expects an ANSWER.\n"
"RULE (first match): fault->critical; asks info->inquiry; requests action->directive; else->approve.")
def gemini(prompt):
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0,"maxOutputTokens":1200}}).encode()
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{JUDGE}:generateContent?key={KEY}"
    for _ in range(4):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=60))
            return "".join(p.get("text","") for p in d.get("candidates",[{}])[0].get("content",{}).get("parts",[]))
        except Exception: time.sleep(3)
    return ""
def tw(t,n): 
    w=(t or "").split(); return " ".join(w[:n])
def classify(text,prev):
    out=gemini(f"Agent said:\n<agent>{tw(prev,120)}</agent>\nDeveloper's next message:\n<message>{tw(text,150)}</message>\n\n{BODY}\n\nONLY JSON: {{\"act\":\"<label>\"}}")
    m=re.search(r'"act"\s*:\s*"(\w+)"',out); a=m.group(1) if m else None
    return a if a in CATS else None

gold={g["point_id"]:g for g in (json.loads(l) for l in open(f"{HERE}/gold.jsonl"))}
preds={}
p="/sim/predictions.jsonl"
if os.path.exists(p):
    for l in open(p):
        try: r=json.loads(l); preds[r["point_id"]]=r.get("message","")
        except: pass

rows=[]
def judge_one(pid):
    g=gold[pid]; pred=preds.get(pid,"")
    pm=classify(pred,g["prev_agent"]) if pred else None
    return {"point_id":pid,"gold_move":g["gold_move"],"pred_move":pm,"match":pm==g["gold_move"]}
with ThreadPoolExecutor(max_workers=8) as ex:
    rows=[f.result() for f in as_completed([ex.submit(judge_one,pid) for pid in gold])]

scored=[r for r in rows if r["gold_move"] and r["pred_move"]]
acc=sum(1 for r in scored if r["match"])/len(scored) if scored else 0.0
verdict={"developer":os.environ.get("SIMBENCH_DEV",""),"condition":os.environ.get("SIMBENCH_COND",""),
         "n_points":len(gold),"n_scored":len(scored),"move_match_accuracy":round(acc,4),
         "per_point":rows}
json.dump(verdict,open("/sim/verdict.json","w"),indent=1)
print(f"move-match accuracy {acc:.3f} over {len(scored)} points")
# Harbor reward: the task passes/scores on the computed accuracy (a real-valued reward)
assert scored, "no scorable points — agent produced no valid predictions"
open("/sim/reward.txt","w").write(str(round(acc,4)))

#!/usr/bin/env python3
"""Sample 100 held-out user turns across the cohort and build one ATIF-schema history
per turn (context = ALL prior turns in that held-out session). Emits:
  sample100/points.jsonl        one line/point: {point_id, dev, sid, i, repo, source,
                                 prev_agent, real, gold_move, n_ctx_turns} (gold HIDDEN)
  sample100/atif/<pid>.json     ATIF trajectory of the context (steps = user/assistant text)
Gold move = gemini-3.5-flash 4-way classifier over the REAL held-out message.
Text-step ATIF (quick test); tool-inclusive ATIF from raw reparse is the fidelity follow-up.
Deterministic sampling (round-robin over sorted devs) — no RNG."""
import json, re, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "/data/claude-crawl")
from cohort_policy import (
    POLICY_VERSION,
    is_human_target,
    policy_fingerprint,
    scrub_text,
)

OUT = "/data/swesimbench-v2-harbor/sample100"
os.makedirs(f"{OUT}/atif", exist_ok=True)
N_POINTS = int(os.environ.get("N_POINTS", "100"))
STEP_CHARS = 4000   # per-step text cap in ATIF (keeps files sane)
MODEL = "gemini-3.5-flash"

def scrub(t):
    return scrub_text(t or "")

def cap(t):
    t = scrub(t or "")
    return t[:STEP_CHARS] + (" […truncated]" if len(t) > STEP_CHARS else "")

def is_action(t):
    return t.get("role") == "user" and is_human_target(t)

# ---- gemini 4-way move classifier (gold labels) ----
CATS = ["approve", "critical", "directive", "inquiry"]
BODY = (
"Classify the developer's MOVE by the observable function of their message toward the agent's previous turn. Choose exactly one:\n"
"- approve: acceptance/permission, no new content, no complaint (yes/ok/lgtm/go ahead/thanks).\n"
"- critical: asserts something is WRONG — a bug/failure/wrong output, or the approach is mistaken/unwanted.\n"
"- directive: tells the agent what to DO next with no fault stated — a new task/addition/forward steer.\n"
"- inquiry: primarily asks for information/explanation, expecting an ANSWER.\n"
"DECISION RULE (first match): 1 fault/error/dissatisfaction -> critical; 2 asks for info -> inquiry; 3 requests any action/change -> directive; 4 else -> approve.")
def tw(t, n):
    w = (t or "").split(); return " ".join(w[:n]) + (" […]" if len(w) > n else "")
def gemini(prompt, temp=0, mx=800):
    key = next(l.split("=", 1)[1].strip() for l in open("/data/harbor-adapters-experiments/.env") if l.startswith("GEMINI_API_KEY="))
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": temp, "maxOutputTokens": mx}}).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    for a in range(4):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=60))
            return "".join(p.get("text", "") for p in d.get("candidates", [{}])[0].get("content", {}).get("parts", []))
        except Exception:
            time.sleep(3)
    return ""
def classify(text, prev):
    out = gemini(f"A developer is using an AI coding agent. The agent just said:\n<agent>{tw(prev,120)}</agent>\n\nThe developer's next message was:\n<message>{tw(text,150)}</message>\n\n{BODY}\n\nRespond with ONLY JSON: {{\"act\":\"<one label>\"}}")
    m = re.search(r'"act"\s*:\s*"(\w+)"', out); a = m.group(1) if m else None
    return a if a in CATS else None

# ---- canonical clean index sid -> turns; sid -> source ----
IDX, SRC = {}, {}
for line in open("/data/swesimbench-v2-harbor/clean_sessions.jsonl"):
    session=json.loads(line)
    IDX[session["session_id"]]=session["turns"]
    SRC[session["session_id"]]=session["source"]
clean_manifest=json.load(open("/data/swesimbench-v2-harbor/clean_manifest.json"))
assert clean_manifest["policy_version"]==POLICY_VERSION
assert clean_manifest["policy_fingerprint"]==policy_fingerprint()
man=clean_manifest["users"]

# ---- collect valid held-out points per dev (deterministic) ----
COMPACT = ("This session is being continued", "<system-reminder>")
def dev_points(u):
    held = sorted([x for x in u["held_sessions"] if x["sid"] in IDX], key=lambda x: x["ts"])
    pts = []
    for x in held:
        turns = IDX[x["sid"]]
        for i, t in enumerate(turns):
            if is_action(t) and any(p.get("role") == "assistant" for p in turns[:i]):
                pts.append((x["sid"], i))
    return pts

pool = {u["user"]: dev_points(u) for u in sorted(man, key=lambda u: u["user"])}
pool = {d: p for d, p in pool.items() if p}
# round-robin one-per-dev per pass until N
chosen = []
devs = sorted(pool)
cursor = {d: 0 for d in devs}
while len(chosen) < N_POINTS:
    progressed = False
    for d in devs:
        if cursor[d] < len(pool[d]):
            sid, i = pool[d][cursor[d]]; cursor[d] += 1
            chosen.append((d, sid, i)); progressed = True
            if len(chosen) >= N_POINTS: break
    if not progressed: break

print(f"chosen {len(chosen)} points across {len({d for d,_,_ in chosen})} devs", flush=True)

# ---- build ATIF + point records ----
def atif_of(sid, i):
    turns = IDX[sid][:i]
    steps = []
    for k, t in enumerate(turns):
        role = t.get("role") or "metadata"
        txt = t.get("text") or ""
        steps.append({
            "step_id": k, "source": role,
            "message": {"role": role, "content": [{"type": "text", "text": cap(txt)}]},
            "is_copied_context": txt.strip().startswith(COMPACT),
        })
    return {
        "schema_version": "1.0", "session_id": sid,
        "agent": {"name": SRC.get(sid, "claude-code"), "version": None, "model_name": None, "extra": {"source": SRC.get(sid)}},
        "steps": steps, "final_metrics": {},
    }

records = []
for n, (d, sid, i) in enumerate(chosen):
    pid = f"t{n:03d}"
    turns = IDX[sid]
    prev = next((t["text"] for t in reversed(turns[:i]) if t.get("role") == "assistant"), "")
    traj = atif_of(sid, i)
    json.dump(traj, open(f"{OUT}/atif/{pid}.json", "w"))
    records.append({"point_id": pid, "dev": d, "sid": sid, "i": i,
                    "repo": (next((t.get("repo") for t in turns if t.get("repo")), None) or "?"),
                    "source": SRC.get(sid), "prev_agent": scrub(prev), "real": scrub(turns[i]["text"]),
                    "gold_move": None, "n_ctx_turns": len(traj["steps"])})

# ---- classify gold moves only when explicitly requested (paid external work) ----
if os.environ.get("RUN_GOLD") == "1":
    def go(r): r["gold_move"] = classify(r["real"], r["prev_agent"]); return 1
    with ThreadPoolExecutor(max_workers=16) as ex:
        for j, _ in enumerate(as_completed([ex.submit(go, r) for r in records]), 1):
            if j % 25 == 0: print(f"gold {j}/{len(records)}", flush=True)

with open(f"{OUT}/points.jsonl", "w") as f:
    for r in records: f.write(json.dumps(r) + "\n")
json.dump({"policy_version":POLICY_VERSION,
           "policy_fingerprint":clean_manifest["policy_fingerprint"],
           "cohort_fingerprint":clean_manifest["cohort_fingerprint"],
           "points":len(records)},
          open(f"{OUT}/meta.json","w"),indent=2)

from collections import Counter
gc = Counter(r["gold_move"] for r in records)
print(f"wrote {len(records)} points -> {OUT}", flush=True)
print("gold move mix:", dict(gc), flush=True)
print("median ctx turns:", sorted(r["n_ctx_turns"] for r in records)[len(records)//2], flush=True)

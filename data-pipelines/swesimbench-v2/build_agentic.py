#!/usr/bin/env python3
"""Build AGENTIC Harbor tasks for SWESimBench v2 — ONE task per prediction point.

Layout (canonical Harbor schema, see harbor/models/task/task.py):
  <dataset>/<task_name>/
    task.toml
    instruction.md              # the agent's task (passed via --task)
    environment/Dockerfile      # COPYs sim/history.md into /sim/
    environment/sim/history.md  # the point's `context` verbatim (agent reads this file)
    tests/test.sh               # verifier: classify answer.txt vs gold with pinned judge
    tests/verify.py             # the actual scoring logic
    tests/gold.json             # HIDDEN: {real, prev_agent, gold_move} for this point

Agent writes its single predicted next-message to /sim/answer.txt.
Verifier classifies answer.txt's move (4-way taxonomy, pinned judge) and compares to gold.
gold_move may be null -> verifier classifies `real` itself with the same judge.
Reward = 1.0 if move matches else 0.0 -> /logs/verifier/reward.txt.

Usage:
  build_agentic.py --dataset eval-pilot --devs gh:mvanhorn,dc:dc_000 --per-dev 5
  build_agentic.py --dataset eval --all
"""
import json, os, shutil, argparse, hashlib, re

HERE = "/data/swesimbench-v2-harbor"
COHORT = f"{HERE}/cohort.json"

TASK_TOML = '''schema_version = "1.1"

[task]
name = "swesimbench-v2/{task_name}"
description = "Predict the developer's next message given the conversation so far ({cond_desc})."
authors = []
keywords = ["swesimbench", "simulate-user", "user-simulation", "{cond}"]

[metadata]
author_name = "swesimbench-v2"
category = "user-simulation"
tags = ["swesimbench", "simulate-user", "{cond}"]
developer = "{dev}"
point_id = "{point_id}"
condition = "{cond}"

[verifier]
timeout_sec = 600.0

[agent]
timeout_sec = 900.0
user = "agent"

[environment]
build_timeout_sec = 600.0
cpus = 1
memory_mb = 2048
storage_mb = 10240
gpus = 0
allow_internet = true
mcp_servers = []
'''

INSTRUCTION = '''You are role-playing the software developer in an ongoing AI coding-agent session.

The full conversation so far is in `/sim/history.md`. Each turn starts with a markdown
blockquote role label (`> DEVELOPER`, `> AGENT`, `> SYSTEM`, `> TOOL`, or `> METADATA`),
then the turn body. `DEVELOPER` is the human to imitate; `AGENT` is their coding agent.
`SYSTEM`, `TOOL`, and `METADATA` are context observed by the original agent, not
developer-authored messages. It MAY be long (thousands of lines) — read it however you
need: `cat`, `tail`, `head`, `grep`, `sed`, etc.

Your job: write the SINGLE next message THIS developer would type to their coding agent right
now — in their own language, length, casing, punctuation, typos and all. Do not solve their
problem, do not explain, do not add role labels or quotes — just the literal message text they
would send.

Write ONLY that literal message to `/sim/answer.txt` (overwrite it). No commentary anywhere else.

Developer style profiles are NOT part of the task. Inject them at job time as Harbor skills
(`--skill` / `agents[].skills`) in Agent Skills format.
'''

DOCKERFILE = '''FROM python:3.12-slim

# Non-root agent user (matches task.toml [agent] user = "agent")
RUN useradd --create-home --shell /bin/bash agent \\
 && mkdir -p /sim && chown -R agent:agent /sim

WORKDIR /sim
COPY --chown=agent:agent sim/history.md /sim/history.md
# Seed an empty answer file the agent will overwrite.
RUN touch /sim/answer.txt && chown agent:agent /sim/answer.txt
'''

TEST_SH = '''#!/bin/bash
# SWESimBench v2 agentic verifier entrypoint.
set -uo pipefail
mkdir -p /logs/verifier
# Ensure python3 exists (base image is python:3.12-slim so it does).
python3 /tests/verify.py 2>&1 | tee /logs/verifier/verify.log
# verify.py writes /logs/verifier/reward.txt itself.
if [ ! -f /logs/verifier/reward.txt ]; then
  echo 0 > /logs/verifier/reward.txt
fi
exit 0
'''

VERIFY_PY = r'''#!/usr/bin/env python3
"""Reads /sim/answer.txt (agent output) + /tests/gold.json (hidden).
Classifies the predicted message's move with the PINNED JUDGE (4-way taxonomy).
If gold_move is null, classifies `real` with the same judge. Reward = 1.0 if match else 0.0.
Judge model is configurable via SIMBENCH_JUDGE (default: the pinned gemini-3.1-pro-preview)."""
import json, os, re, time, urllib.request, urllib.error

KEY = os.environ.get("GEMINI_API_KEY", "")
JUDGE = os.environ.get("SIMBENCH_JUDGE", "gemini-3.1-pro-preview")
CATS = ["approve", "critical", "directive", "inquiry"]
BODY = ("Classify the developer's MOVE by the observable function of their message toward the agent's previous turn. Choose exactly one:\n"
"- approve: acceptance/permission, no new content, no complaint (yes/ok/lgtm/go ahead/thanks).\n"
"- critical: asserts something is WRONG — a bug/failure/wrong output, or the approach is mistaken/unwanted.\n"
"- directive: tells the agent what to DO next with no fault stated — a new task/addition/forward steer.\n"
"- inquiry: primarily asks for information/explanation, expecting an ANSWER.\n"
"DECISION RULE (first match): 1 fault/error/dissatisfaction -> critical; 2 asks for info -> inquiry; 3 requests action/change -> directive; 4 else -> approve.")

def tw(t, n):
    w = (t or "").split()
    return " ".join(w[:n])

def gemini(prompt, retries=6):
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0, "maxOutputTokens": 2048}}).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{JUDGE}:generateContent?key={KEY}"
    for a in range(retries):
        try:
            d = json.load(urllib.request.urlopen(
                urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=90))
            return "".join(p.get("text", "") for p in d.get("candidates", [{}])[0].get("content", {}).get("parts", []))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and a < retries - 1:
                time.sleep(4 * (a + 1)); continue
            return ""
        except Exception:
            if a < retries - 1:
                time.sleep(3); continue
            return ""
    return ""

def classify(text, prev):
    if not (text or "").strip():
        return None
    out = gemini(f"A developer is using an AI coding agent. The agent just said:\n<agent>{tw(prev,120)}</agent>\n\n"
                 f"The developer's next message was:\n<message>{tw(text,150)}</message>\n\n{BODY}\n\n"
                 'Respond with ONLY JSON: {"act":"<one label>"}')
    m = re.search(r'"act"\s*:\s*"(\w+)"', out)
    a = m.group(1) if m else None
    return a if a in CATS else None

gold = json.load(open("/tests/gold.json"))
prev = gold.get("prev_agent", "")
gold_move = gold.get("gold_move") or classify(gold.get("real", ""), prev)

pred_text = ""
try:
    pred_text = open("/sim/answer.txt").read().strip()
except Exception:
    pass
pred_move = classify(pred_text, prev) if pred_text else None

match = bool(pred_move and gold_move and pred_move == gold_move)
reward = 1.0 if match else 0.0

verdict = {
    "point_id": gold.get("point_id"),
    "developer": gold.get("developer"),
    "condition": gold.get("condition"),
    "judge": JUDGE,
    "predicted_msg": pred_text,
    "pred_move": pred_move,
    "gold_move": gold_move,
    "real_msg": gold.get("real", ""),
    "match": match,
    "reward": reward,
}
os.makedirs("/logs/verifier", exist_ok=True)
json.dump(verdict, open("/logs/verifier/verdict.json", "w"), indent=1)
open("/logs/verifier/reward.txt", "w").write(str(reward))
print(f"pred_move={pred_move} gold_move={gold_move} match={match} reward={reward}")
print(f"predicted: {pred_text[:200]!r}")
'''

def slug(s):
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", s)

def point_task_name(dev, point_id):
    h = hashlib.sha1(point_id.encode()).hexdigest()[:8]
    return f"{slug(dev)}__{h}"

def emit_point(dataset_dir, dev, cond, p, profile):
    del profile  # profiles are harness-side Harbor skills, not task payload
    if cond != "noprofile":
        raise ValueError(
            f"unsupported condition {cond!r}: bake noprofile tasks only; "
            "inject developer profiles via Harbor --skill / agents[].skills"
        )
    tname = point_task_name(dev, p["point_id"])
    d = os.path.join(dataset_dir, tname)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "environment", "sim"))
    os.makedirs(os.path.join(d, "tests"))
    # environment: history file
    with open(os.path.join(d, "environment", "sim", "history.md"), "w") as f:
        f.write(p["context"])
    open(os.path.join(d, "environment", "Dockerfile"), "w").write(DOCKERFILE)
    # task.toml + instruction
    open(os.path.join(d, "task.toml"), "w").write(
        TASK_TOML.format(
            task_name=tname,
            dev=dev,
            point_id=p["point_id"],
            cond=cond,
            cond_desc="no baked-in profile; optional profile via Harbor skills",
        ))
    open(os.path.join(d, "instruction.md"), "w").write(INSTRUCTION)
    # tests
    open(os.path.join(d, "tests", "test.sh"), "w").write(TEST_SH)
    open(os.path.join(d, "tests", "verify.py"), "w").write(VERIFY_PY)
    os.chmod(os.path.join(d, "tests", "test.sh"), 0o755)
    gold = {"point_id": p["point_id"], "developer": dev, "condition": cond,
            "real": p["real"], "prev_agent": p.get("prev_agent", ""),
            "gold_move": p.get("gold_move")}
    json.dump(gold, open(os.path.join(d, "tests", "gold.json"), "w"))
    return tname

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, help="dataset dir name under /data/swesimbench-v2-harbor/datasets/")
    ap.add_argument("--devs", default="", help="comma-separated dev ids (else use --all)")
    ap.add_argument("--per-dev", type=int, default=0, help="cap points per dev (0=all)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument(
        "--cond",
        default="noprofile",
        choices=["noprofile"],
        help="Task condition. Profiles are Harbor skills on the agent, not task twins.",
    )
    a = ap.parse_args()

    cohort_meta = json.load(open(os.path.join(HERE, "cohort.meta.json")))
    clean_meta = json.load(open(os.path.join(HERE, "clean_manifest.json")))
    if cohort_meta.get("cohort_fingerprint") != clean_meta.get("cohort_fingerprint"):
        raise RuntimeError("stale cohort.json: run prepare.py before building datasets")
    if cohort_meta.get("policy_fingerprint") != clean_meta.get("policy_fingerprint"):
        raise RuntimeError("cohort policy mismatch: rebuild clean cohort and prepare.py")
    excluded_users = {"gh:mhaitana"}
    recs = {r["user"]: r for r in json.load(open(COHORT)) if r["user"] not in excluded_users}
    dataset_dir = os.path.join(HERE, "datasets", a.dataset)
    shutil.rmtree(dataset_dir, ignore_errors=True)
    os.makedirs(dataset_dir, exist_ok=True)

    if a.all:
        devs = [u for u, r in recs.items() if r["points"]]
    else:
        devs = [d.strip() for d in a.devs.split(",") if d.strip()]

    n = 0
    manifest = []
    for dev in devs:
        r = recs.get(dev)
        if not r or not r["points"]:
            continue
        pts = r["points"]
        if a.per_dev > 0:
            # take the SMALLEST-context points first (fastest/cheapest for pilot)
            pts = sorted(pts, key=lambda p: len(p["context"]))[:a.per_dev]
        for p in pts:
            tname = emit_point(dataset_dir, dev, a.cond, p, r.get("profile", ""))
            manifest.append({"task": tname, "dev": dev, "point_id": p["point_id"]})
            n += 1
    json.dump(manifest, open(os.path.join(dataset_dir, "_manifest.json"), "w"), indent=1)
    json.dump({"policy_version":cohort_meta.get("policy_version"),
               "policy_fingerprint":cohort_meta["policy_fingerprint"],
               "cohort_fingerprint":cohort_meta["cohort_fingerprint"],
               "condition":a.cond,"tasks":n,"developers":len(devs)},
              open(os.path.join(dataset_dir, "_cohort_meta.json"), "w"),indent=2)
    print(f"emitted {n} point-tasks under {dataset_dir} ({len(devs)} devs)")

if __name__ == "__main__":
    main()

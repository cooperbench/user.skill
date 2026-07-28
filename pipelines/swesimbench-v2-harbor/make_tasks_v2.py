#!/usr/bin/env python3
"""Emit point-level Harbor tasks for the 100-turn quick test, in TWO variants:
  inline   — ATIF history rendered into instruction.md (non-agentic)
  agentic  — ATIF history staged at /sim/history.atif.json; agent reads/queries it
Both: agent role-plays the developer and writes the predicted next message to
/workspace/prediction.txt. Separate verifier sandbox scores move-match vs hidden gold.
Writes v2tasks/{inline,agentic}/<pid>/ and v2datasets/{inline,agentic}-100/dataset.toml."""
import json, os, shutil

ROOT = "/data/swesimbench-v2-harbor"
SAMPLE = f"{ROOT}/sample100"
recs = [json.loads(l) for l in open(f"{SAMPLE}/points.jsonl")]
sample_meta = json.load(open(f"{SAMPLE}/meta.json"))
clean_meta = json.load(open(f"{ROOT}/clean_manifest.json"))
if sample_meta.get("cohort_fingerprint") != clean_meta.get("cohort_fingerprint"):
    raise RuntimeError("stale sample100: rebuild it before emitting tasks")
if any(not record.get("gold_move") for record in recs):
    raise RuntimeError("sample100 has no paid gold labels; run with RUN_GOLD=1 before emitting scored tasks")

AGENT_TIMEOUT, VERIFIER_TIMEOUT = 600, 300

def render_transcript(traj):
    out = []
    labels = {"user": "DEVELOPER", "assistant": "AGENT", "system": "SYSTEM",
              "tool": "TOOL", "metadata": "METADATA"}
    for s in traj["steps"]:
        who = labels.get(s["source"], "METADATA")
        txt = "".join(b.get("text", "") for b in s["message"]["content"])
        out.append(f"[{who}]: {txt}")
    return "\n\n".join(out)

DOCKERFILE_INLINE = """FROM python:3.12-slim
WORKDIR /workspace
RUN touch /workspace/prediction.txt
"""
DOCKERFILE_AGENTIC = """FROM python:3.12-slim
RUN mkdir -p /sim
COPY history.atif.json /sim/history.atif.json
WORKDIR /workspace
RUN touch /workspace/prediction.txt
"""

INSTR_INLINE = """You are role-playing ONE specific software developer talking to their AI coding agent.
This is NOT a coding or investigation task. Do NOT explore the filesystem, install packages, inspect
the environment, or run diagnostics. You have everything you need below.

Infer the developer purely from this ENTIRE conversation so far. [DEVELOPER] is the human to imitate;
[AGENT] is their coding agent; [SYSTEM], [TOOL], and [METADATA] are context the original agent observed
but are not developer-authored messages:

<transcript>
{transcript}
</transcript>

The agent just finished its most recent [AGENT] turn. Predict the SINGLE next message THIS developer
would type next — their exact language, length, casing, terseness, typos and all.

Your FIRST and ONLY action is to write that one literal message (no quotes, no label, no commentary)
to /workspace/prediction.txt, then submit. For example:
    cat > /workspace/prediction.txt << 'EOF'
    <the developer's next message>
    EOF
Then immediately finish. Do nothing else.
"""

INSTR_AGENTIC = """You are role-playing ONE specific software developer talking to their AI coding agent.
This is NOT a coding or investigation task. Do NOT explore the filesystem beyond the one history file,
do NOT install packages, inspect the environment, or run diagnostics.

Their ENTIRE conversation so far is stored as an ATIF trajectory at /sim/history.atif.json — an ordered
`steps` array; each step has `source` ("user" = the developer, "assistant" = the agent, while
"system", "tool", and "metadata" are non-developer context) and `message.content[].text`.
Imitate ONLY source="user". Read the trajectory EXACTLY ONCE with this command:
    python3 -c "import json;[print(s['source'].upper(),':',''.join(b.get('text','') for b in s['message']['content'])) for s in json.load(open('/sim/history.atif.json'))['steps']]"

The last step is the agent's most recent turn. Predict the SINGLE next message THIS developer would type
next — their exact language, length, casing, terseness, typos and all.

Then your NEXT and FINAL action is to write that one literal message (no quotes, no label, no commentary)
to /workspace/prediction.txt and submit. For example:
    cat > /workspace/prediction.txt << 'EOF'
    <the developer's next message>
    EOF
Then immediately finish. Do NOT run any other commands.
"""

def task_toml(pid, variant):
    return f'''schema_version = "1.1"
artifacts = ["/workspace/prediction.txt"]

[task]
name = "swesimbench-v2/{variant}-{pid}"
description = "Reproduce developer {pid}'s held-out next turn ({variant}, no-profile)"
authors = []
keywords = ["swesimbench", "simulate-user"]

[metadata]
author_name = "swesimbench-v2"
difficulty = "medium"
category = "user-simulation"
tags = ["swesimbench", "simulate-user", "{variant}", "noprofile", "atif"]

[verifier]
timeout_sec = {VERIFIER_TIMEOUT}.0
environment_mode = "separate"

[verifier.environment]
allow_internet = true
build_timeout_sec = 600.0
cpus = 1
memory_mb = 2048

[verifier.env]

[agent]
timeout_sec = {AGENT_TIMEOUT}.0

[environment]
build_timeout_sec = 600.0
cpus = 1
memory_mb = 2048
storage_mb = 10240
gpus = 0
allow_internet = true
mcp_servers = []

[environment.env]

[solution.env]
'''

# verifier: classify predicted move, compare to hidden gold, write reward.json + verdict.json
# separate verifier image: tests/ is the build context; bake test.sh + verify.py + gold.json
TESTS_DOCKERFILE = """FROM python:3.12-slim
COPY test.sh /tests/test.sh
COPY verify.py /tests/verify.py
COPY gold.json /tests/gold.json
RUN chmod +x /tests/test.sh
"""

TEST_SH = """#!/usr/bin/env bash
set -uo pipefail
mkdir -p /logs/verifier
python3 /tests/verify.py
"""

VERIFY_PY = r'''#!/usr/bin/env python3
"""Separate-sandbox verifier. Reads the agent's /workspace/prediction.txt artifact + the hidden
gold (gold.json baked alongside). Classifies the predicted move (4-way taxonomy) with a pinned
gemini judge and compares to gold. reward=1.0 if move matches else 0.0. Writes reward.json +
verdict.json to /logs/verifier/."""
import json, os, re, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
VDIR = "/logs/verifier"; os.makedirs(VDIR, exist_ok=True)
KEY = os.environ.get("GEMINI_API_KEY", "")
JUDGE = os.environ.get("SIMBENCH_JUDGE", "gemini-3.5-flash")
CATS = ["approve", "critical", "directive", "inquiry"]
BODY = ("Classify the developer's MOVE by the observable function of their message toward the agent's "
"previous turn. Choose exactly one:\n- approve: acceptance/permission, no new content, no complaint.\n"
"- critical: asserts something is WRONG.\n- directive: tells the agent what to DO next, no fault stated.\n"
"- inquiry: asks for information, expects an ANSWER.\nRULE (first match): fault->critical; asks info->"
"inquiry; requests action->directive; else->approve.")

def tw(t, n):
    w = (t or "").split(); return " ".join(w[:n])
def gemini(prompt):
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0, "maxOutputTokens": 800}}).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{JUDGE}:generateContent?key={KEY}"
    for a in range(10):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=60))
            return "".join(p.get("text", "") for p in d.get("candidates", [{}])[0].get("content", {}).get("parts", []))
        except Exception:
            time.sleep(min(2 * (a + 1), 20))   # backoff for transient 503/429
    return ""
def classify(text, prev):
    if not (text or "").strip():
        return None
    out = gemini(f"Agent said:\n<agent>{tw(prev,120)}</agent>\nDeveloper's next message:\n<message>{tw(text,150)}</message>\n\n{BODY}\n\nONLY JSON: {{\"act\":\"<label>\"}}")
    m = re.search(r'"act"\s*:\s*"(\w+)"', out); a = m.group(1) if m else None
    return a if a in CATS else None

gold = json.load(open(f"{HERE}/gold.json"))
pred = ""
for p in ("/workspace/prediction.txt", "/logs/artifacts/prediction.txt", "/sim/prediction.txt"):
    if os.path.exists(p):
        pred = open(p, encoding="utf-8", errors="replace").read().strip(); break

pm = classify(pred, gold["prev_agent"])
match = bool(pm) and pm == gold["gold_move"]
reward = 1.0 if match else 0.0
verdict = {"point_id": gold["point_id"], "dev": gold["dev"], "variant": gold.get("variant"),
           "gold_move": gold["gold_move"], "pred_move": pm, "match": match,
           "predicted_message": pred[:2000], "real_message": gold.get("real", "")[:2000], "reward": reward}
json.dump({"reward": reward}, open(f"{VDIR}/reward.json", "w"))
json.dump(verdict, open(f"{VDIR}/verdict.json", "w"), indent=1)
print(f"[{gold['point_id']}] pred_move={pm} gold={gold['gold_move']} match={match} reward={reward}")
'''

def emit(variant):
    tdir_base = f"{ROOT}/v2tasks/{variant}"
    if os.path.exists(tdir_base):
        shutil.rmtree(tdir_base)
    names = []
    for r in recs:
        pid = r["point_id"]
        td = f"{tdir_base}/{pid}"
        os.makedirs(f"{td}/environment", exist_ok=True)
        os.makedirs(f"{td}/tests", exist_ok=True)
        traj = json.load(open(f"{SAMPLE}/atif/{pid}.json"))
        # task.toml + instruction
        open(f"{td}/task.toml", "w").write(task_toml(pid, variant))
        if variant == "inline":
            open(f"{td}/environment/Dockerfile", "w").write(DOCKERFILE_INLINE)
            open(f"{td}/instruction.md", "w").write(INSTR_INLINE.format(transcript=render_transcript(traj)))
        else:
            open(f"{td}/environment/Dockerfile", "w").write(DOCKERFILE_AGENTIC)
            json.dump(traj, open(f"{td}/environment/history.atif.json", "w"))
            open(f"{td}/instruction.md", "w").write(INSTR_AGENTIC)
        # tests: hidden gold + verifier
        gold = {"point_id": pid, "dev": r["dev"], "variant": variant, "gold_move": r["gold_move"],
                "prev_agent": r["prev_agent"], "real": r["real"]}
        json.dump(gold, open(f"{td}/tests/gold.json", "w"))
        open(f"{td}/tests/Dockerfile", "w").write(TESTS_DOCKERFILE)
        open(f"{td}/tests/test.sh", "w").write(TEST_SH)
        os.chmod(f"{td}/tests/test.sh", 0o755)
        open(f"{td}/tests/verify.py", "w").write(VERIFY_PY)
        names.append(pid)
    # dataset.toml
    dsdir = f"{ROOT}/v2datasets/{variant}-100"
    os.makedirs(dsdir, exist_ok=True)
    lines = [f'name = "swesimbench-v2-{variant}-100"', 'version = "0.1.0"', "", "[[tasks]]"]
    toml = [f'name = "swesimbench-v2-{variant}-100"', 'version = "0.1.0"', ""]
    for pid in names:
        toml.append("[[tasks]]")
        toml.append(f'path = "../../v2tasks/{variant}/{pid}"')
    open(f"{dsdir}/dataset.toml", "w").write("\n".join(toml) + "\n")
    print(f"{variant}: emitted {len(names)} tasks -> v2tasks/{variant}/ ; dataset v2datasets/{variant}-100/")

emit("inline")
emit("agentic")
print("done")

#!/usr/bin/env python3
"""Build AGENTIC Harbor tasks for UserBench — one task per prediction point.

Layout (canonical Harbor schema, see harbor/models/task/task.py):
  <dataset>/<task_name>/
    task.toml
    instruction.md              # the agent's task (passed via --task)
    environment/Dockerfile      # COPYs history.md into /sim/
    environment/history.md      # the point's `context` verbatim (agent reads this file)
    tests/test.sh               # verifier: classify answer.txt vs gold with pinned judge
    tests/verify.py             # the actual scoring logic
    tests/gold.json             # HIDDEN held-out message and previous agent turn

Agent writes its single predicted next-message to /sim/answer.txt.
Composer 2.5 classifies both the predicted and held-out messages into one or
more acts from {approve, critical, steer, inquiry}. Reward is set Jaccard/IoU.

Usage:
  build_agentic.py --dataset eval-pilot --devs gh:mvanhorn,dc:dc_000 --per-dev 5
  build_agentic.py --dataset eval --all
"""
import json, os, shutil, argparse, hashlib, re
from pathlib import Path

HERE = "/data/swesimbench-v2-harbor"
COHORT = f"{HERE}/cohort.json"

TASK_TOML = '''schema_version = "1.1"

[task]
name = "userbench/{task_name}"
description = "Predict the developer's next message given the conversation so far ({cond_desc})."
authors = []
keywords = ["swesimbench", "simulate-user", "user-simulation", "{cond}"]

[metadata]
author_name = "userbench"
category = "user-simulation"
tags = ["swesimbench", "simulate-user", "{cond}"]
developer = "{dev}"
point_id = "{point_id}"
condition = "{cond}"

[verifier]
timeout_sec = 600.0
network_mode = "public"

[agent]
timeout_sec = 900.0
user = "agent"
network_mode = "allowlist"
allowed_hosts = ["openrouter.ai", "*.openrouter.ai"]

[environment]
build_timeout_sec = 600.0
cpus = 1
memory_mb = 2048
storage_mb = 10240
gpus = 0
network_mode = "public"
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

RUN apt-get update \\
 && apt-get install -y --no-install-recommends curl build-essential git \\
 && rm -rf /var/lib/apt/lists/*

# Non-root agent user (matches task.toml [agent] user = "agent")
RUN useradd --create-home --shell /bin/bash agent \\
 && mkdir -p /sim && chown -R agent:agent /sim

WORKDIR /sim
COPY history.md /sim/history.md
RUN chown -R agent:agent /sim/history.md
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

VERIFY_PY = (
    Path(__file__).with_name("verify_multilabel.py").read_text(encoding="utf-8")
)

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
    os.makedirs(os.path.join(d, "environment"), exist_ok=True)
    os.makedirs(os.path.join(d, "tests"), exist_ok=True)
    # environment: history file (flattened; Dockerfile copies into /sim/)
    with open(os.path.join(d, "environment", "history.md"), "w") as f:
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
    gold = {
        "point_id": p["point_id"],
        "developer": dev,
        "condition": cond,
        "real": p["real"],
        "prev_agent": p.get("prev_agent", ""),
        "gold_acts": p.get("gold_acts"),
        "gold_move": p.get("gold_move"),
    }
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

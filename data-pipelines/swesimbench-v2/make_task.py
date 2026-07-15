#!/usr/bin/env python3
"""Emit Harbor tasks from cohort.json: one task per (developer x condition).
condition in {distilled, generic, wrong}. Usage: make_task.py [--only <user>] [--cond distilled]"""
import json, os, shutil, argparse, hashlib
HERE="/data/swesimbench-v2-harbor"; TASKS=f"{HERE}/tasks"; TPL=f"{HERE}/task_template"
recs={r["user"]:r for r in json.load(open(f"{HERE}/cohort.json"))}
users=sorted(recs)
wrong_of={u:users[(i+1)%len(users)] for i,u in enumerate(users)}   # rotated foreign profile

TASK_TOML="""version = "1.0"

[metadata]
author_name = "swesimbench-v2"
category = "user-simulation"
tags = ["swesimbench", "simulate-user", "{harness}", "{cond}"]
developer = "{user}"
condition = "{cond}"

[verifier]
timeout_sec = 900

[agent]
timeout_sec = 1200
"""
README="""You are role-playing the software developer described below, using an AI coding agent.
{profile_clause}
For EACH point in `/sim/points.jsonl`, read the conversation so far (`context`) and write the SINGLE
next message this developer would type to their agent — their language, length, casing, typos and all.
Output ONLY the literal message. Append one JSON object per line to `/sim/predictions.jsonl`:
  {{"point_id": "<id>", "message": "<the developer's next message>"}}
Do not add commentary, quotes, or role labels.
"""

def slug(u): return u.replace(":","_").replace("/","_")
def emit(user, cond):
    r=recs[user]
    if cond=="distilled": prof=r["profile"]
    elif cond=="generic": prof=""
    else: prof=recs[wrong_of[user]]["profile"]
    d=f"{TASKS}/{slug(user)}__{cond}"; shutil.rmtree(d,ignore_errors=True)
    os.makedirs(f"{d}/sim"); os.makedirs(f"{d}/tests")
    # public points (no answers)
    with open(f"{d}/sim/points.jsonl","w") as f:
        for p in r["points"]:
            f.write(json.dumps({"point_id":p["point_id"],"repo":p["repo"],"context":p["context"]})+"\n")
    # hidden gold
    with open(f"{d}/tests/gold.jsonl","w") as f:
        for p in r["points"]:
            f.write(json.dumps({"point_id":p["point_id"],"real":p["real"],"prev_agent":p["prev_agent"],"gold_move":p.get("gold_move")})+"\n")
    prof_clause = (f"Developer profile — study their phrasing, tone, and the KINDS of moves they make:\n<profile>\n{prof}\n</profile>"
                   if prof else "(No profile is given — infer the developer only from the conversation.)")
    open(f"{d}/sim/profile.md","w").write(prof or "(none)")
    open(f"{d}/sim/README.md","w").write(README.format(profile_clause=prof_clause))
    harness = "codex" if any("codex" in (p.get("repo","")).lower() for p in r["points"]) else "claude-code"
    open(f"{d}/task.toml","w").write(TASK_TOML.format(user=user,cond=cond,harness=harness))
    shutil.copy(f"{TPL}/Dockerfile",f"{d}/Dockerfile")
    shutil.copytree(f"{TPL}/tests",f"{d}/tests",dirs_exist_ok=True)
    return d

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--only"); ap.add_argument("--cond")
    a=ap.parse_args()
    conds=[a.cond] if a.cond else ["distilled","generic","wrong"]
    targets=[a.only] if a.only else users
    n=0
    for u in targets:
        for c in conds: emit(u,c); n+=1
    print(f"emitted {n} tasks under {TASKS}/")

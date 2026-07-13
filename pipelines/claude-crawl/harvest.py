#!/usr/bin/env python3
"""Preserving harvest of deep .claude repos. For each repo (ranked by .claude session bytes):
  - clone with --filter=blob:none + sparse-checkout of session paths -> a REAL git clone that
    materializes only the raw .claude session JSONLs (not the huge codebase), kept on disk.
  - parse native Claude Code JSONL (full user+assistant turns) via parse_claude.
  - aggregate per owner into corpus/<owner>.jsonl (one line per session).
Clones are PRESERVED at /data/claude-crawl/clones/. Resumable; disk-guarded.

Usage: harvest.py [N]   # harvest top-N unharvested hits (default 60)
"""
import json, subprocess, os, sys, shutil
sys.path.insert(0, "/data/swesimbench-v2-mini")
import parse_claude as P

BASE = "/data/claude-crawl"
CLONES = f"{BASE}/clones"; CORPUS = f"{BASE}/corpus"
os.makedirs(CLONES, exist_ok=True); os.makedirs(CORPUS, exist_ok=True)
MIN_FREE_GB = 25
SPARSE = ["/.claude/", "/projects/", "/sessions/", "/conversations/",
          "/conversation-archive/", "*.jsonl"]

def free_gb():
    s = os.statvfs(BASE)
    return s.f_bavail * s.f_frsize / 1e9

def status_load():
    p = f"{BASE}/meta/harvest_status.jsonl"
    done = {}
    if os.path.exists(p):
        for l in open(p):
            try:
                d = json.loads(l); done[d["repo"]] = d
            except: pass
    return done

STATUS = open(f"{BASE}/meta/harvest_status.jsonl", "a")

def clone_sparse(repo, dest):
    if os.path.exists(os.path.join(dest, ".git")):
        return True
    shutil.rmtree(dest, ignore_errors=True)
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    r = subprocess.run(["git", "clone", "--filter=blob:none", "--no-checkout", "--depth", "1",
                        f"https://github.com/{repo}", dest], capture_output=True, timeout=900, env=env)
    if r.returncode != 0:
        return False
    subprocess.run(["git", "-C", dest, "sparse-checkout", "init", "--no-cone"], capture_output=True, timeout=60)
    with open(os.path.join(dest, ".git", "info", "sparse-checkout"), "w") as f:
        f.write("\n".join(SPARSE) + "\n")
    r = subprocess.run(["git", "-C", dest, "checkout"], capture_output=True, timeout=900, env=env)
    return r.returncode == 0

def harvest_repo(repo):
    owner = repo.split("/")[0]
    dest = os.path.join(CLONES, repo.replace("/", "__"))
    if not clone_sparse(repo, dest):
        STATUS.write(json.dumps({"repo": repo, "status": "clone-fail"}) + "\n"); STATUS.flush()
        return
    sessions = P.parse_agent_clone(dest)   # [(sid, first_ts, turns, proj, harness)] — .claude + codex
    # write per-owner corpus (append; dedup by sid handled at census)
    out = open(os.path.join(CORPUS, owner + ".jsonl"), "a")
    nsess = nuser = 0
    for sid, ts, turns, proj, harness in sessions:
        nu = sum(1 for t in turns if t["role"] == "user")
        if nu == 0:
            continue
        out.write(json.dumps({"user": "gh:" + owner, "repo": repo, "session_id": f"{repo}|{sid}",
                              "start_time": ts, "harness": harness,
                              "n_user_turns": nu, "turns": turns}, ensure_ascii=False) + "\n")
        nsess += 1; nuser += nu
    out.close()
    STATUS.write(json.dumps({"repo": repo, "owner": owner, "status": "ok",
                            "n_sess": nsess, "n_user": nuser}) + "\n"); STATUS.flush()
    print(f"{repo}: {nsess} sess {nuser} user turns  (free {free_gb():.0f}G)", flush=True)

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    hits_file = f"{BASE}/meta/agent_hits.json" if os.path.exists(f"{BASE}/meta/agent_hits.json") else f"{BASE}/meta/claude_hits.json"
    hits = json.load(open(hits_file))
    done = status_load()
    excl = set()
    # exclude known automation owners
    for o in ["austinweitao", "ryantuck", "benchflow-ai", "codeset-ai", "latchbio", "marcoemrich",
              "palisaderesearch", "shloknatarajan", "atelier-ws", "sublimotion", "bes-dev",
              "skkeoriw", "nwags", "randevranjit", "swcstudiospace", "ingo-eichhorst",
              "david-li0406", "voctory", "xdotli", "fitchmultz", "estelyang",
              "contextlab", "provercoderai", "aries-serpent", "bob3457", "qiushiyan",
              "byesngmin", "handsomeboy02", "terraphim", "hyparam"]:
        excl.add(o.lower())
    picked = 0
    for h in hits:
        if picked >= N:
            break
        repo = h["repo"]
        if repo in done or repo.split("/")[0].lower() in excl:
            continue
        if free_gb() < MIN_FREE_GB:
            print(f"STOP: only {free_gb():.0f}G free", flush=True); break
        harvest_repo(repo)
        picked += 1
    print(f"harvested {picked} repos this pass", flush=True)

if __name__ == "__main__":
    main()

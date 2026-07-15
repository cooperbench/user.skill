#!/usr/bin/env python3
"""Preserving harvest of fresh candidate repos ranked by session density + recency.
For each hit (meta/fresh_hits.json, already filtered pushed>=2026-02-01, >=3 session files):
  - clone sparse (blob:none, session paths only) -> kept in clones/
  - parse via parse_agent_clone (claude-code + codex)
  - PER-OWNER aggregate POST-2026-02-05 user turns (strict: session start_time >= cutoff).
    Only append to corpus if this repo pushes the owner's post-cutoff user turns forward.
  - append sessions to corpus/<owner>.jsonl in the standard schema.
Automation screen: skip owners in EXCL, and skip repos flagged as benchmark/eval harnesses.
Disk-guarded (>=25G). One repo at a time. Resumable via meta/fresh_harvest_status.jsonl.
"""
import json, subprocess, os, sys, shutil, re
sys.path.insert(0, "/data/swesimbench-v2-mini")
import parse_claude as P

BASE = "/data/claude-crawl"
CLONES = f"{BASE}/clones"; CORPUS = f"{BASE}/corpus"
os.makedirs(CLONES, exist_ok=True)
MIN_FREE_GB = 25
CUTOFF = "2026-02-05"
SPARSE = ["/.claude/", "/projects/", "/sessions/", "/conversations/",
          "/conversation-archive/", "/.codex/", "*.jsonl"]

# known automation / org / bot owners to reject up front (union with census EXCLUDE list)
EXCL = set(o.lower() for o in [
    "austinweitao","ryantuck","benchflow-ai","codeset-ai","latchbio","marcoemrich",
    "palisaderesearch","shloknatarajan","atelier-ws","sublimotion","bes-dev","skkeoriw",
    "nwags","randevranjit","swcstudiospace","ingo-eichhorst","david-li0406","voctory",
    "xdotli","fitchmultz","estelyang","contextlab","provercoderai","aries-serpent","bob3457",
    "qiushiyan","byesngmin","handsomeboy02","terraphim","hyparam","codeset","wolffbe",
    "jedisct1","zchee","entireio","entireio-team","partial-staging","braintrustdata",
    "mhaitana",
])
# repo-name substrings that signal a benchmark/eval harness (not a human's working sessions)
BENCH_RE = re.compile(r"(swe-?bench|tbench|terminal-?bench|ml-platform|ralph|harbor|eval-run|"
                      r"benchmark-run|-evals?$|agent-?bench|rollout-eval|gso-|algotune)", re.I)

def free_gb():
    s = os.statvfs(BASE); return s.f_bavail * s.f_frsize / 1e9

STATUS_PATH = f"{BASE}/meta/fresh_harvest_status.jsonl"
def status_load():
    done = {}
    if os.path.exists(STATUS_PATH):
        for l in open(STATUS_PATH):
            try:
                d = json.loads(l); done[d["repo"]] = d
            except: pass
    return done
STATUS = open(STATUS_PATH, "a")

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

def post_cutoff_user_turns(sessions):
    """count user turns in sessions whose first_ts >= CUTOFF."""
    n = 0
    for sid, ts, turns, proj, harness in sessions:
        if not ts or str(ts) < CUTOFF:
            continue
        n += sum(1 for t in turns if t["role"] == "user")
    return n

def harvest_repo(repo):
    owner = repo.split("/")[0]
    if owner.lower() in EXCL:
        STATUS.write(json.dumps({"repo": repo, "status": "skip-excl-owner"}) + "\n"); STATUS.flush()
        return None
    if BENCH_RE.search(repo):
        STATUS.write(json.dumps({"repo": repo, "status": "skip-bench-name"}) + "\n"); STATUS.flush()
        return None
    dest = os.path.join(CLONES, repo.replace("/", "__"))
    if not clone_sparse(repo, dest):
        STATUS.write(json.dumps({"repo": repo, "status": "clone-fail"}) + "\n"); STATUS.flush()
        return None
    sessions = P.parse_agent_clone(dest)
    post = post_cutoff_user_turns(sessions)
    nsess = nuser = 0
    if post >= 50:  # only write to corpus if there is meaningful post-cutoff content
        out = open(os.path.join(CORPUS, owner + ".jsonl"), "a")
        for sid, ts, turns, proj, harness in sessions:
            nu = sum(1 for t in turns if t["role"] == "user")
            if nu == 0:
                continue
            out.write(json.dumps({"user": "gh:" + owner, "repo": repo,
                                  "session_id": f"{repo}|{sid}", "start_time": ts,
                                  "harness": harness, "n_user_turns": nu, "turns": turns},
                                 ensure_ascii=False) + "\n")
            nsess += 1; nuser += nu
        out.close()
    rec = {"repo": repo, "owner": owner, "status": "ok", "n_sess": nsess,
           "n_user": nuser, "post_cutoff_user": post}
    STATUS.write(json.dumps(rec) + "\n"); STATUS.flush()
    print(f"{repo}: {nsess} sess {nuser} user turns (post={post})  free {free_gb():.0f}G", flush=True)
    return rec

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    hits = json.load(open(f"{BASE}/meta/fresh_hits.json"))
    done = status_load()
    picked = 0
    for h in hits:
        if picked >= N:
            break
        repo = h["repo"]
        if repo in done:
            continue
        if free_gb() < MIN_FREE_GB:
            print(f"STOP: only {free_gb():.0f}G free", flush=True); break
        harvest_repo(repo)
        picked += 1
    print(f"harvested {picked} repos this pass (free {free_gb():.0f}G)", flush=True)

if __name__ == "__main__":
    main()

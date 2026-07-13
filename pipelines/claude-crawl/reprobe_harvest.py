#!/usr/bin/env python3
"""Task 3: re-probe the deep registry tail — repos tree-probed but never harvested because
total session BYTES was low, which under-weighted repos holding many SMALL post-Feb sessions.
For each candidate: sparse-clone the raw agent session JSONLs, parse with parse_agent_clone,
and count POST-2026-02-05 user turns. Harvest (write to corpus/<owner>.jsonl) any owner whose
post-Feb user turns >= THRESH. Clones preserved. Disk-guarded, low concurrency.
"""
import json, subprocess, os, sys, shutil
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "/data/swesimbench-v2-mini")
import parse_claude as P

BASE = "/data/claude-crawl"
CLONES = f"{BASE}/clones"; CORPUS = f"{BASE}/corpus"
MIN_FREE_GB = 25
POSTFEB = "2026-02-05"
THRESH = int(os.environ.get("THRESH", "500"))
SPARSE = ["/.claude/", "/.codex/", "/projects/", "/sessions/", "/conversations/",
          "/conversation-archive/", "/history/", "*.jsonl"]

def free_gb():
    s = os.statvfs(BASE); return s.f_bavail * s.f_frsize / 1e9

def clone_sparse(repo, dest):
    if os.path.exists(os.path.join(dest, ".git")):
        return True
    shutil.rmtree(dest, ignore_errors=True)
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    r = subprocess.run(["git", "clone", "--filter=blob:none", "--no-checkout", "--depth", "1",
                        f"https://github.com/{repo}", dest], capture_output=True, timeout=600, env=env)
    if r.returncode != 0:
        return False
    subprocess.run(["git", "-C", dest, "sparse-checkout", "init", "--no-cone"], capture_output=True, timeout=60)
    with open(os.path.join(dest, ".git", "info", "sparse-checkout"), "w") as f:
        f.write("\n".join(SPARSE) + "\n")
    r = subprocess.run(["git", "-C", dest, "checkout"], capture_output=True, timeout=600, env=env)
    return r.returncode == 0

RESULTS = []
def probe_one(repo):
    dest = os.path.join(CLONES, repo.replace("/", "__"))
    if free_gb() < MIN_FREE_GB:
        return {"repo": repo, "status": "disk-stop"}
    if not clone_sparse(repo, dest):
        return {"repo": repo, "status": "clone-fail"}
    try:
        sessions = P.parse_agent_clone(dest)   # [(sid, first_ts, turns, proj, harness)]
    except Exception as e:
        return {"repo": repo, "status": f"parse-err {type(e).__name__}"}
    n_sess = len(sessions)
    postfeb_turns = 0; postfeb_sess = 0; total_turns = 0
    for sid, ts, turns, proj, harness in sessions:
        nu = sum(1 for t in turns if t["role"] == "user")
        total_turns += nu
        if str(ts or "") >= POSTFEB:
            postfeb_turns += nu; postfeb_sess += 1
    return {"repo": repo, "owner": repo.split("/")[0], "status": "probed", "n_sess": n_sess,
            "total_user": total_turns, "postfeb_sess": postfeb_sess, "postfeb_user": postfeb_turns,
            "sessions": sessions if postfeb_turns >= THRESH else None}

def harvest(repo, sessions):
    owner = repo.split("/")[0]
    out = open(os.path.join(CORPUS, owner + ".jsonl"), "a")
    ns = nu = 0
    for sid, ts, turns, proj, harness in sessions:
        u = sum(1 for t in turns if t["role"] == "user")
        if u == 0: continue
        out.write(json.dumps({"user": "gh:" + owner, "repo": repo, "session_id": f"{repo}|{sid}",
                              "start_time": ts, "harness": harness, "n_user_turns": u,
                              "turns": turns}, ensure_ascii=False) + "\n")
        ns += 1; nu += u
    out.close()
    return ns, nu

def main():
    cands = json.load(open(sys.argv[1]))
    repos = [c["repo"] for c in cands]
    log = open(f"{BASE}/meta/reprobe.log", "a")
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(probe_one, repos):
            results.append(r)
            log.write(json.dumps({k: v for k, v in r.items() if k != "sessions"}) + "\n"); log.flush()
            if r.get("status") == "probed":
                print(f"{r['repo']:45s} sess={r['n_sess']:4d} postfeb_user={r['postfeb_user']:5d} "
                      f"(total {r['total_user']})", flush=True)
            if r.get("sessions") and r["postfeb_user"] >= THRESH:
                ns, nu = harvest(r["repo"], r["sessions"])
                print(f"  -> HARVESTED {r['repo']}: {ns} sess {nu} user turns", flush=True)
                log.write(json.dumps({"repo": r["repo"], "status": "harvested", "n_sess": ns, "n_user": nu}) + "\n"); log.flush()
    json.dump([{k: v for k, v in r.items() if k != "sessions"} for r in results],
              open("/tmp/claude-1000/-data/45a45331-9383-46b7-8c0d-1eaf4bece279/scratchpad/reprobe_results.json", "w"), indent=1)
    # summary
    probed = [r for r in results if r.get("status") == "probed"]
    print(f"\nDONE: probed {len(probed)}/{len(repos)}")
    for r in sorted(probed, key=lambda x: -x["postfeb_user"])[:20]:
        print(f"  {r['repo']:45s} postfeb_user={r['postfeb_user']:5d}")

if __name__ == "__main__":
    main()

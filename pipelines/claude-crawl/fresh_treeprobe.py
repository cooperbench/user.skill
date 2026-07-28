#!/usr/bin/env python3
"""Tree-probe fresh candidate repos (meta/fresh_candidates.json) for committed Claude Code / Codex
session JSONL, and filter by repo pushed_at >= 2026-02-01. One Trees API call + one repo metadata
call per repo (core limit 5000/hr). Ranks by session file count (recency-weighted proxy: repos with
many session files AND a recent push are most likely to carry >=500 post-Feb-2026 user turns).
Writes meta/fresh_hits.json = [{repo, n_sess, sess_bytes, pushed_at, harnesses, sample}].
"""
import json, subprocess, os, re
from concurrent.futures import ThreadPoolExecutor

BASE = "/data/claude-crawl"
CAND = f"{BASE}/meta/fresh_candidates.json"
CACHE = f"{BASE}/meta/fresh_treeprobe.json"
cand = json.load(open(CAND))
cache = {}
if os.path.exists(CACHE):
    try: cache = json.load(open(CACHE))
    except: cache = {}

CLAUDE_PATH = re.compile(r'(^|/)\.claude/(projects|conversations|conversation-archive|history|sessions)/', re.I)
BACKUP_PATH = re.compile(r'(^|/)(projects|conversations|sessions|claude-?sessions|claude-?backup)/[^/]*/?.*\.jsonl$', re.I)

def classify(path):
    if not path.endswith(".jsonl"):
        return None
    bn = os.path.basename(path)
    if bn == "history.jsonl":
        return None
    if "/.codex/" in path or bn.startswith("rollout-"):
        return "codex"
    if CLAUDE_PATH.search(path) or BACKUP_PATH.search(path):
        return "claude-code"
    return None

def probe(repo):
    env = {**os.environ, "GH_PROMPT_DISABLED": "1"}
    try:
        # repo metadata: pushed_at + default_branch
        rm = subprocess.run(["gh", "api", f"repos/{repo}", "--jq", "{pushed_at,default_branch,fork,archived}"],
                            capture_output=True, timeout=40, env=env)
        pushed_at = None; branch = "HEAD"
        if rm.returncode == 0:
            try:
                meta = json.loads(rm.stdout.decode())
                pushed_at = meta.get("pushed_at"); branch = meta.get("default_branch") or "HEAD"
            except: pass
        else:
            err = rm.stderr.decode()[:60]
            if "404" in err: return repo, {"err": "404"}
        r = subprocess.run(["gh", "api", f"repos/{repo}/git/trees/{branch}?recursive=1"],
                           capture_output=True, timeout=55, env=env)
        if r.returncode != 0:
            err = r.stderr.decode()[:60]
            return repo, {"err": "empty" if "409" in err or "empty" in err.lower() else "fail", "pushed_at": pushed_at}
        j = json.loads(r.stdout.decode())
        blobs = [(t["path"], t.get("size", 0)) for t in j.get("tree", []) if t.get("type") == "blob"]
        sess = []
        harnesses = set()
        for p, s in blobs:
            h = classify(p)
            if h:
                sess.append((p, s)); harnesses.add(h)
        return repo, {"n_sess": len(sess), "sess_bytes": sum(s for _, s in sess),
                      "truncated": j.get("truncated", False), "n_paths": len(blobs),
                      "pushed_at": pushed_at, "harnesses": sorted(harnesses),
                      "sample": [p for p, _ in sess[:2]]}
    except Exception as e:
        return repo, {"err": str(e)[:40]}

todo = [r for r in cand if r not in cache]
print(f"{len(cand)} candidates, {len(todo)} to probe", flush=True)
done = 0
with ThreadPoolExecutor(max_workers=8) as ex:
    for repo, info in ex.map(probe, todo):
        cache[repo] = info; done += 1
        if done % 100 == 0:
            json.dump(cache, open(CACHE, "w")); print(done, "probed", flush=True)
json.dump(cache, open(CACHE, "w"))

# filter: >=3 session files AND pushed >= 2026-02-01
def recent(pa):
    return isinstance(pa, str) and pa >= "2026-02-01"

hits = []
for k, v in cache.items():
    if not isinstance(v, dict) or v.get("n_sess", 0) < 3:
        continue
    if not recent(v.get("pushed_at")):
        continue
    hits.append(v | {"repo": k})
hits.sort(key=lambda h: (h["n_sess"], h["sess_bytes"]), reverse=True)
json.dump(hits, open(f"{BASE}/meta/fresh_hits.json", "w"))
print(f"DONE. {len(hits)} recent repos (pushed>=2026-02-01) with >=3 session files", flush=True)
for h in hits[:50]:
    print(f"  sess={h['n_sess']:5d} {h['sess_bytes']/1e6:7.1f}MB pushed={h.get('pushed_at','?')[:10]} {'/'.join(h['harnesses'])} {h['repo']}", flush=True)

#!/usr/bin/env python3
"""Tree-probe every registry repo for committed native Claude Code (.claude) session JSONL.
One Trees API call per repo (core limit 5000/hr) lists all file paths + blob sizes — including
the >384KB files code search can't see. Rank repos by .claude session bytes.

A .claude session file = a *.jsonl whose path looks like a Claude Code session store:
  .claude/projects/**, .claude/conversations/**, .claude/conversation-archive/**,
  projects/**/*.jsonl (claude-backup layout), sessions/**/*.jsonl — and NOT .codex / rollout-.
"""
import json, subprocess, os, re
from concurrent.futures import ThreadPoolExecutor

BASE = "/data/claude-crawl"
registry = json.load(open(f"{BASE}/meta/registry.json"))
CACHE = f"{BASE}/meta/treeprobe.json"
cache = {}
if os.path.exists(CACHE):
    try: cache = json.load(open(CACHE))
    except: cache = {}

CLAUDE_PATH = re.compile(r'(^|/)\.claude/(projects|conversations|conversation-archive|history|sessions)/', re.I)
BACKUP_PATH = re.compile(r'(^|/)(projects|conversations|sessions|claude-?sessions|claude-?backup)/[^/]*/?.*\.jsonl$', re.I)
CODEX = re.compile(r'(/\.codex/|/rollout-|history\.jsonl$)', re.I)

def is_claude_session(path):
    if CODEX.search(path):
        return False
    if not path.endswith(".jsonl"):
        return False
    return bool(CLAUDE_PATH.search(path)) or bool(BACKUP_PATH.search(path))

def probe(repo):
    try:
        r = subprocess.run(["gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1"],
                           capture_output=True, timeout=50, env={**os.environ, "GH_PROMPT_DISABLED": "1"})
        if r.returncode != 0:
            err = r.stderr.decode()[:60]
            return repo, {"err": "empty" if "409" in err or "Git Repository is empty" in err else "fail"}
        j = json.loads(r.stdout.decode())
        blobs = [(t["path"], t.get("size", 0)) for t in j.get("tree", []) if t.get("type") == "blob"]
        sess = [(p, s) for p, s in blobs if is_claude_session(p)]
        return repo, {"n_sess": len(sess), "sess_bytes": sum(s for _, s in sess),
                      "truncated": j.get("truncated", False), "n_paths": len(blobs),
                      "sample": [p for p, _ in sess[:2]]}
    except Exception as e:
        return repo, {"err": str(e)[:40]}

todo = [r for r in registry if r not in cache]
print(f"{len(registry)} registry, {len(todo)} to probe", flush=True)
done = 0
with ThreadPoolExecutor(max_workers=10) as ex:
    for repo, info in ex.map(probe, todo):
        cache[repo] = info; done += 1
        if done % 200 == 0:
            json.dump(cache, open(CACHE, "w")); print(done, "probed", flush=True)
json.dump(cache, open(CACHE, "w"))

hits = sorted([(v["sess_bytes"], v["n_sess"], k, v) for k, v in cache.items()
               if isinstance(v, dict) and v.get("n_sess", 0) >= 3], reverse=True)
json.dump([{"repo": k, **v} for _, _, k, v in hits], open(f"{BASE}/meta/claude_hits.json", "w"))
print(f"DONE. {len(hits)} repos with >=3 .claude session files")
for sb, ns, k, v in hits[:40]:
    print(f"  {sb/1e6:8.1f}MB sess={ns:5d} {'T ' if v.get('truncated') else ''}{k}")

#!/usr/bin/env python3
"""Grow the repo registry by exhaustively enumerating GitHub repos that commit native Claude Code
.claude JSONL. Uses code search (path fingerprint) partitioned by file size to beat the 1000-result
cap, plus repo-name search. Paced under the code_search 10/min limit. Merges new repos into
meta/registry.json. Resumable via meta/enum_done.json.
"""
import json, subprocess, os, time

BASE = "/data/claude-crawl"
REG = f"{BASE}/meta/registry.json"
DONE = f"{BASE}/meta/enum_done.json"
registry = set(json.load(open(REG)))
done = set(json.load(open(DONE))) if os.path.exists(DONE) else set()

# size buckets (bytes) to keep each partition under the 1000-result cap
SIZE_BUCKETS = ["0..999", "1000..1999", "2000..3999", "4000..7999", "8000..15999",
                "16000..31999", "32000..63999", "64000..127999", "128000..255999",
                "256000..511999", "512000..1048575", ">1048575"]
# path fingerprints for native .claude session stores
PATH_Q = ['path:.claude/projects extension:jsonl',
          'path:.claude/conversations extension:jsonl',
          '"parentUuid" "sessionId" path:.claude extension:jsonl']

def gh_search_code(q):
    repos = set()
    for page in range(1, 11):  # 1000-result cap = 10 pages
        try:
            r = subprocess.run(["gh", "api", "-X", "GET", "search/code",
                                "-f", f"q={q}", "-f", "per_page=100", "-f", f"page={page}",
                                "--jq", ".items[].repository.full_name"],
                               capture_output=True, timeout=40, env={**os.environ})
            time.sleep(6.5)  # ~9/min, under the 10/min code_search cap
            if r.returncode != 0:
                if "rate limit" in r.stderr.decode().lower():
                    time.sleep(60); continue
                break
            names = [x for x in r.stdout.decode().split("\n") if x]
            if not names:
                break
            repos.update(names)
            if len(names) < 100:
                break
        except Exception:
            break
    return repos

def gh_search_repos(q):
    repos = set()
    try:
        r = subprocess.run(["gh", "api", "-X", "GET", "search/repositories",
                            "-f", f"q={q}", "-f", "per_page=100", "--jq", ".items[].full_name"],
                           capture_output=True, timeout=40)
        time.sleep(2.5)
        repos.update(x for x in r.stdout.decode().split("\n") if x)
    except Exception:
        pass
    return repos

def save():
    json.dump(sorted(registry), open(REG, "w"))
    json.dump(sorted(done), open(DONE, "w"))

# 1) path-fingerprint code search, size-partitioned
for pq in PATH_Q:
    for sz in SIZE_BUCKETS:
        key = f"code::{pq}::size:{sz}"
        if key in done:
            continue
        before = len(registry)
        registry |= gh_search_code(f"{pq} size:{sz}")
        done.add(key)
        print(f"[{len(registry)} (+{len(registry)-before})] {key}", flush=True)
        save()

# 2) repo-name search (separate 30/min budget)
for name in ["claude-backup", "claude-sessions", "claude-code-sessions", "cc-sessions",
             "claude-history", "claude-conversations", "claude-projects-backup", "my-claude",
             "claude-code-backup", "claude-cli-backup", "claude-logs", "dotfiles claude"]:
    key = f"repo::{name}"
    if key in done:
        continue
    before = len(registry)
    registry |= gh_search_repos(name)
    done.add(key)
    print(f"[{len(registry)} (+{len(registry)-before})] {key}", flush=True)
    save()

save()
print(f"DONE. registry now {len(registry)} repos")

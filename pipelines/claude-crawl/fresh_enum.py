#!/usr/bin/env python3
"""Fresh candidate enumeration. NOTE: GitHub CODE search does NOT support the `pushed:` qualifier
(repo-only), so we enumerate committed-session repos via code search WITHOUT a date filter, then
dedup against registry.json. Recency (pushed>=2026-02-01) is enforced later in the tree-probe via
the repos API. Repo-NAME search DOES support pushed:, so those keep the date filter.
Writes new candidate repo full_names to meta/fresh_candidates.json. Resumable.
"""
import json, subprocess, os, time

BASE = "/data/claude-crawl"
REG = f"{BASE}/meta/registry.json"
CAND = f"{BASE}/meta/fresh_candidates.json"
DONE = f"{BASE}/meta/fresh_enum_done.json"

registry = set(json.load(open(REG)))
reg_lower = set(r.lower() for r in registry)
cand = set(json.load(open(CAND))) if os.path.exists(CAND) else set()
# reset the stale done markers from the broken (pushed:) run
done = set()

SIZE_BUCKETS = ["0..1999", "2000..7999", "8000..31999", "32000..127999",
                "128000..511999", "512000..2097151", ">2097151"]

# code-search path fingerprints (NO pushed: — code search ignores it)
CODE_Q_PARTITIONED = [
    'path:.claude/projects extension:jsonl',
    'path:.codex/sessions extension:jsonl',
    'filename:rollout- extension:jsonl',
    '"parentUuid" "isSidechain"',
]

def gh_search_code(q, max_pages=10):
    repos = set()
    for page in range(1, max_pages + 1):
        r = None
        for attempt in range(3):
            try:
                r = subprocess.run(["gh", "api", "-X", "GET", "search/code",
                                    "-f", f"q={q}", "-f", "per_page=100", "-f", f"page={page}",
                                    "--jq", ".items[].repository.full_name"],
                                   capture_output=True, timeout=45, env={**os.environ})
            except Exception:
                time.sleep(8); continue
            err = r.stderr.decode().lower()
            if r.returncode != 0:
                if "rate limit" in err or "secondary" in err or "you have exceeded" in err:
                    print(f"    rate-limited, sleeping 65s", flush=True); time.sleep(65); continue
                print(f"    err page{page}: {err[:90]}", flush=True)
                time.sleep(7); return repos
            break
        if r is None or r.returncode != 0:
            break
        time.sleep(7)  # ~8.5/min under 10/min code_search cap
        names = [x for x in r.stdout.decode().split("\n") if x]
        if not names:
            break
        repos.update(names)
        if len(names) < 100:
            break
    return repos

def gh_search_repos(q):
    repos = set()
    try:
        r = subprocess.run(["gh", "api", "-X", "GET", "search/repositories",
                            "-f", f"q={q}", "-f", "per_page=100", "-f", "sort=updated",
                            "--jq", ".items[].full_name"],
                           capture_output=True, timeout=40)
        time.sleep(2.5)
        repos.update(x for x in r.stdout.decode().split("\n") if x)
    except Exception:
        pass
    return repos

cand_lower = set(c.lower() for c in cand)
def add_new(repos, tag):
    global cand
    new = set()
    for r in repos:
        rl = r.lower()
        if r and rl not in reg_lower and rl not in cand_lower:
            new.add(r); cand_lower.add(rl)
    cand |= new
    print(f"[cand={len(cand)} +{len(new)} new / {len(repos)} hits] {tag}", flush=True)
    return new

def save():
    json.dump(sorted(cand), open(CAND, "w"))
    json.dump(sorted(done), open(DONE, "w"))

for pq in CODE_Q_PARTITIONED:
    for sz in SIZE_BUCKETS:
        key = f"code::{pq}::size:{sz}"
        if key in done:
            continue
        add_new(gh_search_code(f"{pq} size:{sz}"), key)
        done.add(key); save()

for name in ["claude-backup", "claude-sessions", "codex-sessions", "claude-code-history",
             "claude-conversations", "dotfiles claude", "claude-code-backup", "cc-sessions",
             "codex-history", "my-claude-code", "claude-projects", "agent-sessions"]:
    key = f"repo::{name}"
    if key in done:
        continue
    add_new(gh_search_repos(f"{name} pushed:>2026-02-01"), key)
    done.add(key); save()

save()
print(f"DONE. {len(cand)} fresh candidate repos NOT in registry", flush=True)

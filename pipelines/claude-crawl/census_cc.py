#!/usr/bin/env python3
"""Unified census over FULL-TRACE coding-agent sources, at >=400 train + >=100 held.
Sources:
  entire    /data/entire-backfill/corpus/*.jsonl   (Claude Code + Codex + Cursor; user = gh:actor)
  dataclaw  /data/dataclaw/meta/corpus.full.jsonl   (full-fidelity donor traces)
  crawl     /data/claude-crawl/corpus/*.jsonl       (committed .claude/.codex; user = gh:owner)
  swechat   SWE-chat parquet                        (native agents; dedups vs entire by sid)
  specstory /data/specstory/meta/corpus_redacted.jsonl  (Cursor history exports; user = gh:owner)
Dedup sessions by id across sources; snapshot-collapse; strict-timestamp split; disjoint sessions.
Reports per-source and combined qualified counts to find the minimal source set reaching 100.
"""
import json, glob, re, os
from collections import defaultdict
from cohort_policy import (
    EXCLUDED_USERS,
    canonical_session_id,
    developer_text,
    is_human_target,
    normalize_text,
    specstory_session_id,
    specstory_timestamp,
)

SUB = 24
EXCLUDE = set(EXCLUDED_USERS)
MERGE = {"gh:skogai": "gh:SkogBackup"}
MINTRAIN = int(os.environ.get("MINTRAIN", "400"))
CUTOFF = os.environ.get("CUTOFF", "")   # e.g. "2026-02-01": drop sessions before this (Opus 4.6 era)

def normp(t): return normalize_text(developer_text(t)).lower()

def counts(turns):
    ns = 0; subs = []
    for t in turns:
        if t.get("role") != "user":
            continue
        txt = t.get("text") or ""
        if not is_human_target(txt):
            continue
        n = normp(txt)
        if len(n) >= SUB:
            subs.append(hash(n))
        else:
            ns += 1
    return ns, subs

# user -> {sid: (ts, n_short, subs, source)}; global sid dedup keeps richest
owners = defaultdict(dict)
seen_sid = {}
usrc = defaultdict(set)

CANON = {}   # lowercased gh login -> canonical-cased key (GitHub logins are case-insensitive)
def canon(user):
    if user.startswith("gh:"):
        lo = user.lower()
        return CANON.setdefault(lo, user)
    return user

def add(user, sid, ts, turns, source):
    if not sid or not ts:
        return
    ts = str(ts)
    if not ts.startswith(("2", "0")):
        return
    if CUTOFF and ts < CUTOFF:   # temporal cutoff (e.g. Opus-4.6-era: keep >= 2026-02-01)
        return
    user = canon(user)
    user = MERGE.get(user, user)
    if user in EXCLUDE:
        return
    ns, subs = counts(turns)
    if ns + len(subs) == 0:
        return
    tot = ns + len(subs)
    key = canonical_session_id(sid)
    # cross-source / fork copies: keep richest under one owner for this UUID
    if key in seen_sid:
        ou, on, osid = seen_sid[key]
        if tot <= on:
            return
        owners[ou].pop(osid, None)
    seen_sid[key] = (user, tot, sid)
    owners[user][sid] = (ts, ns, subs, source)
    usrc[user].add(source)

# entire
for f in glob.glob("/data/entire-backfill/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        add("gh:" + s.get("actor", "?"), s.get("session_id"), s.get("created_at"),
            s.get("turns", []), "entire")

# dataclaw (claude / codex / cursor)
donor_owner = {}
dc_lines = []
votes = defaultdict(lambda: defaultdict(int))
dataclaw_corpus = os.environ.get(
    "DATACLAW_CORPUS", "/data/dataclaw/meta/corpus.full.jsonl"
)
for line in open(dataclaw_corpus):
    try: s = json.loads(line)
    except: continue
    dc_lines.append(s); votes[s["donor"]][s["repo"].split("/")[0]] += 1
donor_owner = {d: max(v, key=v.get) for d, v in votes.items()}
for s in dc_lines:
    src = (s.get("source") or "").lower()
    # Claude Code (any claude* model), Codex, or Cursor — exclude opencode/gemini/kimi/etc.
    if not (src.startswith("claude") or src == "codex" or "codex" in src or src == "cursor"):
        continue
    add("dc:" + s["donor"], s.get("session_id"), s.get("start_time"), s.get("turns", []), "dataclaw")
del dc_lines
# my .claude crawl
for f in glob.glob("/data/claude-crawl/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        add(s["user"], s.get("session_id"), s.get("start_time"), s.get("turns", []), "crawl")
# SWE-chat parquet (native agents including Cursor; the packaged Entire dump — dedups vs entire by sid)
if os.environ.get("WITH_SWECHAT", "1") == "1":
    import pyarrow.parquet as pq
    f = "/data/with-user/data_cache/hf/datasets--SALT-NLP--SWE-chat/snapshots/f66cca95b14caaa4177f7ed5eaa424608dadcffa/conversations.parquet"
    t = pq.read_table(f, columns=["user_id", "session_id", "turn_type", "content", "timestamp"])
    sess = defaultdict(lambda: {"uid": None, "turns": [], "ts": None})
    for uid, sid, tt, content, ts in zip(t["user_id"].to_pylist(), t["session_id"].to_pylist(),
                                         t["turn_type"].to_pylist(), t["content"].to_pylist(),
                                         t["timestamp"].to_pylist()):
        if tt == "user_prompt":
            role = "user"
        elif tt == "assistant_response":
            role = "assistant"
        else:
            continue
        d = sess[sid]; d["uid"] = uid
        d["turns"].append({"role": role, "text": content or ""})
        if ts is not None and (d["ts"] is None or ts < d["ts"]):
            d["ts"] = ts
    for sid, d in sess.items():
        if d["uid"]:
            add("gh:" + d["uid"], sid, d["ts"].isoformat() if d["ts"] else None, d["turns"], "swechat")

# NOTE: user-only committed/round corpora are NOT loaded — their full traces come through the
# crawl corpus after reparse_clones.py re-parsed the preserved clones (parse_agent_clone).

# SpecStory Cursor history exports (primary Cursor volume for v2 depth bars).
# Thin native Cursor shards (Entire/DataClaw/SWE-chat) still load above for cross-link.
if os.environ.get("WITH_SPECSTORY", "1") == "1":
    ss_path = "/data/specstory/meta/corpus_redacted.jsonl"
    if os.path.exists(ss_path):
        for line in open(ss_path):
            try:
                s = json.loads(line)
            except Exception:
                continue
            owner = s.get("owner") or (s.get("repo") or "?").split("/")[0]
            add(
                "gh:" + owner,
                specstory_session_id(s),
                specstory_timestamp(s),
                s.get("turns", []),
                "specstory",
            )

def dedup_snap(sess):
    items = [(sid, ts, ns, subs, frozenset(subs)) for sid, (ts, ns, subs, _) in sess.items()]
    items.sort(key=lambda x: (-len(x[4]), -(x[2] + len(x[3]))))
    kept, fps = [], []
    for sid, ts, ns, subs, fs in items:
        if len(fs) >= 3 and any(fs <= k for k in fps):
            continue
        if len(fs) >= 3:
            fps.append(fs)
        kept.append((sid, ts, ns + len(subs)))
    return kept

def split(sess):
    ss = sorted(dedup_snap(sess), key=lambda x: x[1])
    total = sum(n for _, _, n in ss)
    held = 0; k = len(ss)
    for i in range(len(ss) - 1, 0, -1):
        if ss[i - 1][1] == ss[i][1]:
            continue
        held = total - sum(n for _, _, n in ss[:i]); k = i
        if held >= 100:
            break
    return ss, k, total - held, held

rows = []
for u, sess in owners.items():
    ss, b, train, held = split(sess)
    rows.append({"user": u, "sources": sorted(usrc[u]), "qualified": train >= MINTRAIN and held >= 100,
                 "train": train, "held": held, "n_sess": len(ss), "_ss": ss, "_b": b})
rows.sort(key=lambda r: (-r["qualified"], -r["train"]))
q = [r for r in rows if r["qualified"]]
print(f"MINTRAIN={MINTRAIN}  QUALIFIED: {len(q)}")
by = defaultdict(int)
for r in q:
    by["+".join(r["sources"])] += 1
for k, v in sorted(by.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
# per-source standalone contribution
for src in ("entire", "dataclaw", "crawl", "swechat", "specstory"):
    n = sum(1 for r in q if src in r["sources"])
    print(f"  [{src} involved in {n} qualified users]")

manifest = [{"user": r["user"], "sources": r["sources"], "train_turns": r["train"], "held_turns": r["held"],
             "train_sessions": [{"sid": s, "ts": t, "n": n} for s, t, n in r["_ss"][:r["_b"]]],
             "held_sessions": [{"sid": s, "ts": t, "n": n} for s, t, n in r["_ss"][r["_b"]:]]} for r in q]
json.dump(manifest, open("/data/claude-crawl/meta/users_cc.json", "w"), indent=1, default=str)
for r in rows:
    r.pop("_ss", None); r.pop("_b", None)
json.dump(rows, open("/data/claude-crawl/meta/census_cc.json", "w"), indent=1, default=str)
print(f"wrote users_cc.json ({len(q)} qualified) + census_cc.json")

#!/usr/bin/env python3
"""Census over the harvested native .claude corpus. Per owner:
  - dedup sessions by substantial-prompt content fingerprint (collapse snapshot re-saves);
  - sort sessions by start time;
  - temporal split: minimal strict-timestamp boundary b with train (ss[:b]) >= 1000 user turns
    and held-out (ss[b:]) >= 100 user turns; sessions disjoint, train strictly precedes held-out.
Selects qualifying users. Turn content may repeat across sessions; only sessions must be disjoint
and ordered. Writes census.json + users_100.json manifest.
"""
import json, glob, re, sys
from pathlib import Path
from collections import defaultdict

BASE = "/data/claude-crawl"
SUB = 24
NOISE = ("<command-", "<local-command", "Caveat:", "[Request interrupted", "<task-notification",
         "<teammate-message", "<user-prompt-submit-hook", "<session-start-hook", "<user-memory-input",
         "This session is being continued", "<system-reminder", "[SYSTEM", "<ide_opened_file",
         "<ide_selection", "<ide_diagnostics", "<ide-", "<budget:", "<post-tool", "<pre-tool")

def normp(t): return re.sub(r"\s+", " ", (t or "").strip().lower())

def session_counts(turns):
    """(n_short, subs_list) for real user turns in a session."""
    ns = 0; subs = []
    for t in turns:
        if t.get("role") != "user":
            continue
        txt = (t.get("text") or "").lstrip()
        if not txt or txt.startswith(NOISE):
            continue
        n = normp(txt)
        if len(n) >= SUB:
            subs.append(hash(n))
        else:
            ns += 1
    return ns, subs

# automation / synthetic accounts to drop, and same-person identity merges
EXCLUDE = {"gh:wolffbe": "benchmark harness: 1201 sessions x 1 templated ml-platform-task prompt",
           "gh:austinweitao": "claude-mem observer scaffolding", "gh:skkeoriw": "skill automation",
           "gh:contextlab": "automation", "gh:nwags": "benchmark",
           "gh:mhaitana": "synthetic placeholder sessions containing only 'turn N' / 'ok'"}
MERGE = {"gh:skogai": "gh:SkogBackup"}   # both are Skogix (same human)

# load corpus: owner -> {sid: (ts, n_short, subs)}
owners = defaultdict(dict)
for f in glob.glob(f"{BASE}/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        sid = s.get("session_id"); ts = s.get("start_time")
        if not sid or not ts or ts == "0000":
            continue
        ts = str(ts)   # normalize (both CC and Codex are ISO strings; guard stray non-str)
        if not ts.startswith(("2", "0")):   # not a plausible ISO timestamp -> unorderable, drop
            continue
        ns, subs = session_counts(s.get("turns", []))
        if ns + len(subs) == 0:
            continue
        u = s["user"]
        if u in EXCLUDE:
            continue
        u = MERGE.get(u, u)   # collapse same-person accounts
        # keep richest copy of a repeated sid
        if sid not in owners[u] or (ns + len(subs)) > (owners[u][sid][1] + len(owners[u][sid][2])):
            owners[u][sid] = (ts, ns, subs)

def dedup_snapshots(sess):
    """Collapse snapshot re-saves: drop a session whose substantial-fingerprint is a subset of a
    kept one (>=3 subs)."""
    items = [(sid, ts, ns, subs, frozenset(subs)) for sid, (ts, ns, subs) in sess.items()]
    items.sort(key=lambda x: (-len(x[4]), -(x[2] + len(x[3]))))
    kept, kept_fps = [], []
    for sid, ts, ns, subs, fs in items:
        if len(fs) >= 3 and any(fs <= k for k in kept_fps):
            continue
        if len(fs) >= 3:
            kept_fps.append(fs)
        kept.append((sid, ts, ns + len(subs)))
    return kept

def split(sess):
    ss = sorted(dedup_snapshots(sess), key=lambda x: x[1])  # (sid, ts, n)
    total = sum(n for _, _, n in ss)
    prefix = 0
    for b in range(1, len(ss)):
        prefix += ss[b - 1][2]
        if ss[b - 1][1] == ss[b][1]:
            continue
        if prefix >= 1000:
            held = total - prefix
            if held >= 100:
                return ss, b, prefix, held
            break
    # diagnostics
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
    total = sum(n for _, _, n in ss)
    if total < 300:
        continue
    rows.append({"user": u, "qualified": train >= int(__import__("os").environ.get("MINTRAIN","1000")) and held >= 100,
                 "total": total, "train": train, "held": held,
                 "train_sess": b, "held_sess": len(ss) - b, "n_sess": len(ss),
                 "split_ts": ss[b][1] if b < len(ss) else None,
                 "first_ts": ss[0][1], "last_ts": ss[-1][1],
                 "_ss": [(sid, ts, n) for sid, ts, n in ss], "_b": b})
rows.sort(key=lambda r: (-r["qualified"], -r["train"]))
q = [r for r in rows if r["qualified"]]
print(f"QUALIFIED (.claude only): {len(q)}   near-miss(>=300 total): {len(rows)-len(q)}")

# manifest
manifest = []
for r in q:
    ss = r["_ss"]; b = r["_b"]
    manifest.append({"user": r["user"], "train_turns": r["train"], "held_turns": r["held"],
                     "train_sessions": [{"sid": s, "ts": t, "n": n} for s, t, n in ss[:b]],
                     "held_sessions": [{"sid": s, "ts": t, "n": n} for s, t, n in ss[b:]],
                     "split_ts": r["split_ts"], "first_ts": r["first_ts"], "last_ts": r["last_ts"]})
for r in rows:
    r.pop("_ss", None); r.pop("_b", None)
Path(f"{BASE}/meta/census.json").write_text(json.dumps(rows, indent=1, default=str))
Path(f"{BASE}/meta/users_100.json").write_text(json.dumps(manifest, indent=1, default=str))
print(f"wrote census.json ({len(rows)} rows) + users_100.json ({len(manifest)} qualified)")
if q:
    print("\ntop qualified:")
    for r in q[:30]:
        print(f"  {r['user'][:30]:32s} train {r['train']:5d}({r['train_sess']}s) "
              f"held {r['held']:5d}({r['held_sess']}s) last {str(r['last_ts'])[:10]}")

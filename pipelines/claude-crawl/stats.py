#!/usr/bin/env python3
"""Data-distribution stats for the final 100-user cohort, split train vs eval (held-out).
Sessions + user-turns come from the manifest; assistant-turns + tokens/user-turn come from the
corpora (matched by session id); tool calls come from raw sources (SWE-chat parquet exact; a
raw-clone sample for Claude Code/Codex). Reports mean & median per user.
"""
import json, glob, statistics as st
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
def toklen(s): return len(enc.encode(s or "", disallowed_special=()))

man = json.load(open("/data/claude-crawl/meta/final_100.json"))

# --- session_id -> turns index, matching the census's ids (same loaders) ---
NOISE = ("<command-", "<local-command", "Caveat:", "[Request interrupted", "<task-notification",
         "<teammate-message", "<user-prompt-submit-hook", "<session-start-hook", "<user-memory-input",
         "This session is being continued", "<system-reminder", "[SYSTEM", "<ide_opened_file",
         "<ide_selection", "<ide_diagnostics", "<ide-", "<budget:", "<post-tool", "<pre-tool",
         "<environment_context", "<user_instructions", "<turn_context", "<permissions")
def real_user(t):
    tx = (t.get("text") or "").lstrip()
    return t.get("role") == "user" and tx and not tx.startswith(NOISE)

sid_turns = {}   # sid -> list[{role,text}]
def put(sid, turns):
    if sid and turns and (sid not in sid_turns or len(turns) > len(sid_turns[sid])):
        sid_turns[sid] = turns
for f in glob.glob("/data/entire-backfill/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        put(s.get("session_id"), s.get("turns", []))
for f in glob.glob("/data/claude-crawl/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        put(s.get("session_id"), s.get("turns", []))
for line in open("/data/dataclaw/meta/corpus.jsonl"):
    try: s = json.loads(line)
    except: continue
    put(s.get("session_id"), s.get("turns", []))
# swechat from parquet
import pyarrow.parquet as pq
from collections import defaultdict
pf = "/data/with-user/data_cache/hf/datasets--SALT-NLP--SWE-chat/snapshots/f66cca95b14caaa4177f7ed5eaa424608dadcffa/conversations.parquet"
t = pq.read_table(pf, columns=["session_id", "turn_type", "content"])
sw = defaultdict(list)
for sid, tt, c in zip(t["session_id"].to_pylist(), t["turn_type"].to_pylist(), t["content"].to_pylist()):
    if tt == "user_prompt":
        sw[sid].append({"role": "user", "text": c or ""})
    elif tt == "assistant_response":
        sw[sid].append({"role": "assistant", "text": c or ""})
for sid, turns in sw.items():
    put(sid, turns)

# --- per-user, per-split aggregation ---
def agg(sessions):
    n_sess = len(sessions)
    n_user = n_asst = 0
    utok = []
    for x in sessions:
        turns = sid_turns.get(x["sid"])
        if turns is None:
            n_user += x["n"]   # fallback: manifest user count (assistant/tokens unknown)
            continue
        for tt in turns:
            if real_user(tt):
                n_user += 1; utok.append(toklen(tt.get("text")))
            elif tt.get("role") == "assistant":
                n_asst += 1
    return n_sess, n_user, n_asst, utok

rows = []
for u in man:
    ts, tu, ta, ttok = agg(u["train_sessions"])
    hs, hu, ha, htok = agg(u["held_sessions"])
    rows.append({"user": u["user"], "train_sess": ts, "held_sess": hs,
                 "train_user": tu, "held_user": hu, "train_asst": ta, "held_asst": ha,
                 "utok": ttok + htok})

def ms(vals):
    vals = [v for v in vals if v is not None]
    return (round(st.mean(vals), 1), round(st.median(vals), 1)) if vals else (0, 0)

print("=" * 66)
print(f"DATA DISTRIBUTION — {len(rows)} users (Claude Code / Codex full traces)")
print("=" * 66)
def line(label, vals):
    m, md = ms(vals)
    print(f"  {label:34s} mean {m:>9}   median {md:>9}")

print("\nSESSIONS per user:")
line("train sessions", [r["train_sess"] for r in rows])
line("held-out (eval) sessions", [r["held_sess"] for r in rows])
line("total sessions", [r["train_sess"] + r["held_sess"] for r in rows])

print("\nUSER TURNS per user:")
line("train user turns", [r["train_user"] for r in rows])
line("held-out (eval) user turns", [r["held_user"] for r in rows])
line("total user turns", [r["train_user"] + r["held_user"] for r in rows])

print("\nASSISTANT TURNS per user (full traces):")
line("train assistant turns", [r["train_asst"] for r in rows])
line("held-out (eval) assistant turns", [r["held_asst"] for r in rows])

print("\nTURNS per session:")
line("user turns / train session", [r["train_user"] / r["train_sess"] for r in rows if r["train_sess"]])
line("user turns / eval session", [r["held_user"] / r["held_sess"] for r in rows if r["held_sess"]])

print("\nTOKENS per user turn (cl100k):")
allt = [tok for r in rows for tok in r["utok"]]
allt.sort()
if allt:
    print(f"  pooled over all user turns          mean {round(st.mean(allt),1):>9}   median {allt[len(allt)//2]:>9}")
    print(f"  p90 {allt[int(len(allt)*0.9)]}   p99 {allt[int(len(allt)*0.99)]}   max {allt[-1]}   (n={len(allt)} turns)")
per_user_mean = [round(st.mean(r["utok"]), 1) for r in rows if r["utok"]]
line("per-user mean tokens/user turn", per_user_mean)

json.dump(rows, open("/data/claude-crawl/meta/stats_rows.json", "w"), default=str)
print(f"\n(sessions matched to full turns: "
      f"{sum(1 for u in man for x in u['train_sessions']+u['held_sessions'] if x['sid'] in sid_turns)}"
      f"/{sum(len(u['train_sessions'])+len(u['held_sessions']) for u in man)})")

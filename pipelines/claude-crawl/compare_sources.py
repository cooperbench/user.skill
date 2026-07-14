#!/usr/bin/env python3
"""Cross-source comparison of the 100-user cohort: session depth, Claude Code vs Codex mix,
tokens, models, time span, train/eval split — per data source (Entire / GitHub crawl / DataClaw)."""
import json, glob, os, statistics as st
from collections import defaultdict, Counter
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
def tok(s): return len(enc.encode(s or "", disallowed_special=()))

man = json.load(open("/data/claude-crawl/meta/final_100.json"))
ENTIRE_CORPUS_GLOB = os.environ.get(
    "ENTIRE_CORPUS_GLOB", "/data/entire-backfill/corpus-full-v4/*.jsonl"
)
DATACLAW_CORPUS = os.environ.get(
    "DATACLAW_CORPUS", "/data/dataclaw/meta/corpus.full.jsonl"
)
msids = {}
split_of = {}
for u in man:
    for x in u["train_sessions"]: msids[x["sid"]] = x["n"]; split_of[x["sid"]] = "train"
    for x in u["held_sessions"]: msids[x["sid"]] = x["n"]; split_of[x["sid"]] = "eval"

# sid -> source
src = {}
for f in glob.glob(ENTIRE_CORPUS_GLOB):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        if s.get("session_id") in msids: src[s["session_id"]] = "entire"
for line in open(DATACLAW_CORPUS):
    try: s = json.loads(line)
    except: continue
    if s.get("session_id") in msids and s["session_id"] not in src: src[s["session_id"]] = "dataclaw"
for f in glob.glob("/data/claude-crawl/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        if s.get("session_id") in msids and s["session_id"] not in src: src[s["session_id"]] = "crawl"
for sid in msids:
    src.setdefault(sid, "crawl")   # residual reparse sids

# analysis.json has harness/model/ts per sid
an = {}
info = json.load(open("/data/claude-crawl/meta/analysis.json"))  # not per-sid; recompute below
# recompute sid -> harness/model/ts quickly from corpora + dataclaw
hm = {}
def norm_h(agent, model=None):
    a = (agent or "").lower(); m = (model or "").lower()
    return "codex" if ("codex" in a or "codex" in m or a == "codex") else "claude-code"
for f in glob.glob(ENTIRE_CORPUS_GLOB):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        if s.get("session_id") in msids:
            hm[s["session_id"]] = (norm_h(s.get("agent"), s.get("model")), s.get("model") or "?", s.get("created_at"))
for line in open(DATACLAW_CORPUS):
    try: s = json.loads(line)
    except: continue
    sid = s.get("session_id")
    if sid in msids and sid not in hm:
        so = s.get("source") or "?"
        hm[sid] = (norm_h(so, so), so, s.get("start_time"))
for f in glob.glob("/data/claude-crawl/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        sid = s.get("session_id")
        if sid in msids and sid not in hm:
            hm[sid] = (s.get("harness") or "claude-code", "?", s.get("start_time"))

# sid -> turns (for assistant count + tokens)
sid_turns = {}
def put(sid, turns):
    if sid in msids and turns and (sid not in sid_turns or len(turns) > len(sid_turns[sid])):
        sid_turns[sid] = turns
for f in glob.glob(ENTIRE_CORPUS_GLOB) + glob.glob("/data/claude-crawl/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        put(s.get("session_id"), s.get("turns", []))
for line in open(DATACLAW_CORPUS):
    try: s = json.loads(line)
    except: continue
    put(s.get("session_id"), s.get("turns", []))

NOISE = ("<command-", "<local-command", "Caveat:", "[Request interrupted", "<task-notification",
         "<teammate-message", "<system-reminder", "<ide_", "<environment_context", "<user_instructions")
# aggregate per source
agg = defaultdict(lambda: {"sess": 0, "uturn": 0, "aturn": 0, "utok": [], "harness": Counter(),
                           "harness_turn": Counter(), "model": Counter(), "months": [], "devs": set(),
                           "train_turn": 0, "eval_turn": 0, "sess_len": []})
udom = defaultdict(Counter)
for u in man:
    for x in u["train_sessions"] + u["held_sessions"]:
        udom[u["user"]][src.get(x["sid"], "crawl")] += x["n"]
for sid, n in msids.items():
    so = src.get(sid, "crawl"); a = agg[so]
    a["sess"] += 1; a["uturn"] += n; a["sess_len"].append(n)
    a[("train_turn" if split_of[sid] == "train" else "eval_turn")] += n
    h, model, ts = hm.get(sid, ("claude-code", "?", None))
    a["harness"][h] += 1; a["harness_turn"][h] += n
    fam = ("codex" if "codex" in model.lower() or "gpt-5" in model.lower() else
           "claude-opus" if "opus" in model.lower() else "claude-sonnet" if "sonnet" in model.lower()
           else "claude-haiku" if "haiku" in model.lower() else "claude" if model.lower().startswith("claude")
           else "not recorded" if model in ("?", "<synthetic>") else "other")
    a["model"][fam] += 1
    if ts and str(ts)[:7] >= "2025": a["months"].append(str(ts)[:7])
    turns = sid_turns.get(sid)
    if turns:
        for t in turns:
            if t.get("role") == "assistant": a["aturn"] += 1
            elif t.get("role") == "user":
                tx = (t.get("text") or "").lstrip()
                if tx and not tx.startswith(NOISE): a["utok"].append(tok(tx))
for u, c in udom.items():
    agg[c.most_common(1)[0][0]]["devs"].add(u)

SRC = {"entire": "Entire checkpoints", "crawl": "GitHub .claude/.codex crawl", "dataclaw": "DataClaw"}
rows = {}
def med(v): return round(st.median(v), 1) if v else 0
def mean(v): return round(st.mean(v), 1) if v else 0
print(f"{'':30s} {'Entire':>14s} {'GitHub crawl':>14s} {'DataClaw':>14s}")
def line(label, fn):
    vals = [fn(agg[s]) for s in ("entire", "crawl", "dataclaw")]
    print(f"{label:30s} {str(vals[0]):>14s} {str(vals[1]):>14s} {str(vals[2]):>14s}")
    rows[label] = {SRC[s]: fn(agg[s]) for s in ("entire", "crawl", "dataclaw")}
line("developers (dominant)", lambda a: len(a["devs"]))
line("sessions", lambda a: a["sess"])
line("user turns", lambda a: a["uturn"])
line("assistant turns", lambda a: a["aturn"])
line("user turns / session (mean)", lambda a: mean(a["sess_len"]))
line("user turns / session (median)", lambda a: med(a["sess_len"]))
line("assistant / user turn", lambda a: round(a["aturn"] / max(a["uturn"], 1), 1))
line("tokens/user turn (median)", lambda a: med(a["utok"]))
line("tokens/user turn (mean)", lambda a: mean(a["utok"]))
line("Claude Code % of turns", lambda a: round(100 * a["harness_turn"]["claude-code"] / max(a["uturn"], 1)))
line("Codex % of turns", lambda a: round(100 * a["harness_turn"]["codex"] / max(a["uturn"], 1)))
line("train:eval turn %", lambda a: f"{round(100*a['train_turn']/max(a['uturn'],1))}:{round(100*a['eval_turn']/max(a['uturn'],1))}")
line("time span", lambda a: f"{min(a['months']) if a['months'] else '?'}→{max(a['months']) if a['months'] else '?'}")
print("\nTop models by source:")
for s in ("entire", "crawl", "dataclaw"):
    print(f"  {SRC[s]:28s} {dict(agg[s]['model'].most_common(4))}")
json.dump(rows, open("/data/claude-crawl/meta/source_compare.json", "w"), default=str)
# also save model breakdown
mb = {SRC[s]: dict(agg[s]["model"].most_common()) for s in ("entire", "crawl", "dataclaw")}
json.dump(mb, open("/data/claude-crawl/meta/source_models.json", "w"))

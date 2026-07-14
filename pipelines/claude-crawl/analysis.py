#!/usr/bin/env python3
"""Harness (Claude Code vs Codex), version, and time-period analysis of the 100-user cohort,
plus the distribution stats — emitted as analysis.json for the v2 EDA site."""
import json, glob, re, os, statistics as st
from collections import defaultdict, Counter

man = json.load(open("/data/claude-crawl/meta/final_100.json"))
ENTIRE_CORPUS_GLOB = os.environ.get(
    "ENTIRE_CORPUS_GLOB", "/data/entire-backfill/corpus-full-v4/*.jsonl"
)
DATACLAW_CORPUS = os.environ.get(
    "DATACLAW_CORPUS", "/data/dataclaw/meta/corpus.full.jsonl"
)
manifest_sids = {x["sid"]: x["n"] for u in man for x in u["train_sessions"] + u["held_sessions"]}
split_of = {}
for u in man:
    for x in u["train_sessions"]: split_of[x["sid"]] = "train"
    for x in u["held_sessions"]: split_of[x["sid"]] = "eval"

def norm_harness(agent, model=None):
    a = (agent or "").lower(); m = (model or "").lower()
    if "codex" in a or "codex" in m or a == "codex":
        return "codex"
    return "claude-code"

# sid -> {harness, model, ts}
info = {}
# entire (has agent + model + created_at)
for f in glob.glob(ENTIRE_CORPUS_GLOB):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        sid = s.get("session_id")
        if sid in manifest_sids:
            info[sid] = {"harness": norm_harness(s.get("agent"), s.get("model")),
                         "model": s.get("model") or "?", "ts": s.get("created_at")}
# dataclaw (source = model/agent)
for line in open(DATACLAW_CORPUS):
    try: s = json.loads(line)
    except: continue
    sid = s.get("session_id")
    if sid in manifest_sids and sid not in info:
        src = s.get("source") or "?"
        info[sid] = {"harness": norm_harness(src, src), "model": src, "ts": s.get("start_time")}
# crawl (harness in corpus; model extracted from clones by uuid)
crawl_sids = {}
for f in glob.glob("/data/claude-crawl/corpus/*.jsonl"):
    for line in open(f):
        try: s = json.loads(line)
        except: continue
        sid = s.get("session_id")
        if sid in manifest_sids and sid not in info:
            crawl_sids[sid] = {"harness": s.get("harness") or "claude-code", "ts": s.get("start_time")}

# uuid -> model from raw clones (Claude Code: message.model; Codex: session_meta model)
def clone_models():
    uu = {}
    bases = (glob.glob("/data/claude-crawl/clones/*/") + glob.glob("/data/committed-transcripts/harvest/*/")
             + glob.glob("/data/round2-github/clones/*/") + glob.glob("/data/round3-github/clones/*/"))
    for base in bases:
        for root, _, files in os.walk(base):
            if "/.git" in root: continue
            for fn in files:
                if not fn.endswith(".jsonl") or fn == "history.jsonl": continue
                m = re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|[0-9a-f-]{20,})", fn)
                if not m: continue
                uuid = m.group(1)
                if uuid in uu: continue
                path = os.path.join(root, fn)
                try:
                    model = None
                    for i, line in enumerate(open(path, encoding="utf-8", errors="ignore")):
                        if i > 120: break   # scan deeper; skip compaction-summary lines
                        try: d = json.loads(line)
                        except: continue
                        if not isinstance(d, dict): continue
                        msg = d.get("message")
                        cand = None
                        if isinstance(msg, dict) and msg.get("model"):
                            cand = msg["model"]
                        else:
                            p = d.get("payload")
                            if isinstance(p, dict) and p.get("model"):
                                cand = p["model"]
                        # Claude Code tags its auto-compaction summaries model="<synthetic>";
                        # keep scanning for the real assistant model.
                        if cand and cand not in ("<synthetic>", "synthetic"):
                            model = cand; break
                    if model: uu[uuid] = model
                except OSError: pass
    return uu
uu = clone_models()
def sid_uuid(sid):
    m = re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", sid)
    return m.group(1) if m else None
for sid, d in crawl_sids.items():
    model = uu.get(sid_uuid(sid) or "")
    info[sid] = {"harness": norm_harness(d["harness"], model), "model": model or ("codex" if d["harness"] == "codex" else "?"),
                 "ts": d["ts"]}

# ---- aggregate ----
harness = defaultdict(lambda: {"sessions": 0, "user_turns": 0})
models = Counter()
months = Counter()
per_split_harness = defaultdict(lambda: defaultdict(lambda: {"sessions": 0, "user_turns": 0}))
tmin, tmax = "9999", "0000"
for sid, n in manifest_sids.items():
    d = info.get(sid)
    if not d: continue
    h = d["harness"]
    harness[h]["sessions"] += 1; harness[h]["user_turns"] += n
    per_split_harness[split_of[sid]][h]["sessions"] += 1
    per_split_harness[split_of[sid]][h]["user_turns"] += n
    models[d["model"]] += 1
    ts = str(d.get("ts") or "")
    if len(ts) >= 7:
        months[ts[:7]] += 1
        tmin = min(tmin, ts); tmax = max(tmax, ts)

# normalize model families
def fam(m):
    m = m.lower()
    if "codex" in m: return "codex (gpt-5-codex/…)"
    if "opus" in m: return "claude-opus"
    if "sonnet" in m: return "claude-sonnet"
    if "haiku" in m: return "claude-haiku"
    if m.startswith("claude"): return "claude (other)"
    if m in ("?", ""): return "unknown"
    return m
model_fam = Counter()
for m, c in models.items(): model_fam[fam(m)] += c

out = {
    "n_users": len(man),
    "harness": {h: v for h, v in harness.items()},
    "harness_by_split": {sp: {h: dict(v) for h, v in hv.items()} for sp, hv in per_split_harness.items()},
    "models_exact": dict(models.most_common()),
    "model_families": dict(model_fam.most_common()),
    "months": dict(sorted(months.items())),
    "time_min": tmin[:10], "time_max": tmax[:10],
    "matched": sum(1 for sid in manifest_sids if sid in info), "total_sessions": len(manifest_sids),
}
json.dump(out, open("/data/claude-crawl/meta/analysis.json", "w"), indent=1, default=str)

print(f"matched {out['matched']}/{out['total_sessions']} sessions to harness/model/time\n")
print("HARNESS (Claude Code vs Codex):")
for h, v in harness.items():
    print(f"  {h:12s} sessions {v['sessions']:6d}   user turns {v['user_turns']:7d}")
print("\nby split:")
for sp in ("train", "eval"):
    for h, v in per_split_harness[sp].items():
        print(f"  {sp:6s} {h:12s} sessions {v['sessions']:6d}  user turns {v['user_turns']:7d}")
print(f"\nTIME: {out['time_min']} -> {out['time_max']}")
print("MODEL FAMILIES:", dict(model_fam.most_common()))
print("\nTop exact models:")
for m, c in models.most_common(12):
    print(f"  {c:6d}  {m}")
print("\nSessions by month:", dict(sorted(months.items())))

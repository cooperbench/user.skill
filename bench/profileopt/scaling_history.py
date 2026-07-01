"""History-scaling experiment: does conditioning gemini-3.1-pro on more developer history reduce
simulation error (1 - next-action prediction accuracy)?

Conditions (each over the full 480 frozen test points, all via the direct Gemini API):
  hist{K}   K in {0,2,4,8,16,32,64}: the K most recent train-session turns, verbatim, as the profile
            block (K=0 == the generic no-profile prompt).
  dist{K}   K in {8,32,64}: a profile re-distilled (production distill-user recipe) from only those
            K turns. Skipped with a warning until users_atK/ folders exist.
  profile-full: the existing production users/<slug>/ profile, rerun on this backend.

Gens cached in rerun_raw.jsonl (keys gen|{pid}|gemini-3.1-pro-api|{cond}); labels reuse the shared
content-addressed Haiku cache. Rerunning is a no-op on cache hits.
"""
import hashlib, json, math, sys, time, statistics as st
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent; ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT/"scripts")); sys.path.insert(0, str(ROOT/"bench")); sys.path.insert(0, str(HERE))
import validate as V, v0_1, taxonomy as TAX  # noqa: E402
import gemini_api  # noqa: E402

EXP = HERE/"experiments"/"condagree_multi"; RAW = HERE/"rerun_raw.jsonl"
MODEL_KEY = "gemini-3.1-pro-api"; GEMINI_MODEL = "gemini-3.1-pro-preview"
JUDGE = "anthropic/claude-haiku-4.5"          # OpenRouter path (leaderboard-original)
JUDGE_CLI = "claude-haiku-4-5-20251001"        # CLI fallback: same model, subscription-served
JUDGE_BACKEND = "or"                           # new OR key in .env (judging only) -> same path as all cached labels
KS = [0, 2, 4, 8, 16, 32, 64]
DIST_KS = [8, 32, 64]
CONC_GEN = 16; CONC_LAB = 16; PASSES = 4

TEST = json.loads((HERE/"splits.json").read_text())["test"]["qualifying_users"]
TRAIN = json.loads((EXP/"train_turns.json").read_text())

def _load_points():  # deterministic: same point_ids as the leaderboard runs
    pts = {}
    for u in TEST:
        bys = v0_1.all_points_for(u); queues = [list(v) for v in bys.values()]; sp = []
        while len(sp) < 30 and any(queues):
            for q in queues:
                if q:
                    sp.append(q.pop(0))
                    if len(sp) >= 30: break
        for p in sp: p["slug"] = u; pts[p["point_id"]] = p
    return pts
points = _load_points()

_cache = {}
if RAW.exists():
    _bad = 0
    for l in RAW.read_text().splitlines():
        if not l.strip(): continue
        try:
            r = json.loads(l)
        except json.JSONDecodeError:
            _bad += 1; continue  # concurrent writers can interleave a line; skip, the gen re-runs
        if r.get("kind") == "gen" and (not str(r.get("text","")).strip() or str(r.get("text","")).startswith("Error:")):
            continue  # never trust cached failures
        _cache[r["key"]] = r
    if _bad: print(f"cache: skipped {_bad} corrupted lines", flush=True)
_lock = __import__("threading").Lock()
def put(rec):
    with _lock:
        _cache[rec["key"]] = rec
        with RAW.open("a") as f: f.write(json.dumps(rec, ensure_ascii=False)+"\n")

# ---------- conditioning text per (slug, cond) ----------
def hist_block(slug, k):
    if k == 0: return ""
    turns = TRAIN[slug]["turns"][-k:]
    lines, prev_sess = [], None
    for i, t in enumerate(turns, 1):
        mark = "" if t["session_idx"] == prev_sess else " [new session]"
        prev_sess = t["session_idx"]
        lines.append(f"{i}.{mark} {t['text']}")
    return (f"Recent messages this developer sent to their AI coding agent across earlier sessions, "
            f"oldest first ({len(turns)} messages). Infer their voice, habits, and preferences from these:\n\n"
            + "\n".join(lines))

def dist_folder_text(slug, k):
    d = ROOT/"users_atK"/f"{slug}_K{k}"
    if not d.exists(): return None
    parts = []
    for f in V.FOLDER_FILES:
        p = d/f
        if p.exists(): parts.append(f"--- {f} ---\n{p.read_text()}")
    sk = d/"skills"
    for p in sorted(sk.glob("*.md")) if sk.exists() else []:
        parts.append(f"--- skills/{p.name} ---\n{p.read_text()}")
    return V.truncate_words("\n\n".join(parts), V.FOLDER_WORD_CAP) if parts else None

def folder_for(slug, cond):
    if cond.startswith("hist"): return hist_block(slug, int(cond[4:]))
    if cond.startswith("dist"): return dist_folder_text(slug, int(cond[4:]))
    if cond == "profile-full": return V.load_folder_text(slug)
    raise ValueError(cond)

# ---------- gen + label ----------
def gen(point, cond):
    folder = folder_for(point["slug"], cond)
    prompt = V.build_prompt(point, folder or "")
    seed = int(hashlib.sha256(f"{point['point_id']}|{MODEL_KEY}|{cond}".encode()).hexdigest(), 16) % (2**31)
    txt = gemini_api.chat(GEMINI_MODEL, prompt, max_tokens=4000, temperature=0.7, seed=seed, thinking="HIGH")
    return v0_1.v0.clean_msg(txt) if not txt.startswith("Error:") else txt, seed

def move_of(prev, text):
    if V.is_interrupt(text):
        rest = TAX._strip_interrupt(text)
        if not rest: return "critical"
        text = rest
    if not (text or "").strip() or str(text).startswith("Error:"): return None
    k = "lab:haiku:"+hashlib.sha256((V.truncate_words(prev,120)+"|"+V.truncate_words(text,150)).encode()).hexdigest()[:24]
    if k in _cache: return _cache[k]["move"]
    if JUDGE_BACKEND == "cli":
        mv = TAX.classify(text, prev, model=JUDGE_CLI, backend="cli")
    else:
        mv = TAX.classify(text, prev, model=JUDGE, backend="or")
    if mv is not None: put({"key": k, "move": mv})
    return mv

def run_conditions(conds):
    for cond in conds:
        if cond.startswith("dist") and dist_folder_text(TEST[0], int(cond[4:])) is None:
            print(f"!! {cond}: users_atK folders missing — skipped (run distillation first)"); continue
        for p_ in range(PASSES):
            todo = [p for p in points.values() if f"gen|{p['point_id']}|{MODEL_KEY}|{cond}" not in _cache]
            if not todo: break
            print(f"[{cond}] pass {p_+1}: {len(todo)} gens", flush=True)
            def one(p):
                txt, seed = gen(p, cond)
                if txt.startswith("Error:") or not txt.strip():
                    return None
                return {"key": f"gen|{p['point_id']}|{MODEL_KEY}|{cond}", "kind": "gen",
                        "point_id": p["point_id"], "slug": p["slug"], "model": MODEL_KEY,
                        "model_id": GEMINI_MODEL, "backend": "gemini-api", "effort": "high",
                        "cond": cond, "text": txt, "seed": seed, "temperature": 0.7, "ts": time.time()}
            with ThreadPoolExecutor(max_workers=CONC_GEN) as ex:
                done = 0
                for f in as_completed([ex.submit(one, p) for p in todo]):
                    r = f.result()
                    if r: put(r)
                    done += 1
                    if done % 60 == 0: print(f"  [{cond}] {done}/{len(todo)}", flush=True)
        n = sum(1 for p in points.values() if f"gen|{p['point_id']}|{MODEL_KEY}|{cond}" in _cache)
        print(f"[{cond}] complete: {n}/480 gens cached", flush=True)
        # label as we go (parallel Haiku)
        items = [(pid, p) for pid, p in points.items() if f"gen|{pid}|{MODEL_KEY}|{cond}" in _cache]
        with ThreadPoolExecutor(max_workers=CONC_LAB) as ex:
            list(as_completed([ex.submit(move_of, p["prev_agent"], _cache[f"gen|{pid}|{MODEL_KEY}|{cond}"]["text"])
                               for pid, p in items]))

def analyze(conds):
    realm = {pid: move_of(p["prev_agent"], p["real"]) for pid, p in points.items()}
    ptsU = defaultdict(list)
    for pid, p in points.items(): ptsU[p["slug"]].append(pid)
    out = {}
    for cond in conds:
        per = {}; wl = []
        for u, pids in ptsU.items():
            pr = []
            for pid in pids:
                g = _cache.get(f"gen|{pid}|{MODEL_KEY}|{cond}")
                if not g: continue
                sm = move_of(points[pid]["prev_agent"], g["text"]); rm = realm[pid]
                if sm and rm: pr.append((rm, sm)); wl.append(len(g["text"].split()))
            if pr: per[u] = sum(1 for a, b in pr if a == b)/len(pr)
        if not per: continue
        vals = list(per.values()); n = len(vals)
        mean = st.mean(vals); ci = 2.093*st.stdev(vals)/math.sqrt(n) if n > 1 else 0
        n_lab = sum(1 for pid in points if f"gen|{pid}|{MODEL_KEY}|{cond}" in _cache)
        medw = {u: 0 for u in per}
        if cond.startswith("hist") and int(cond[4:]) > 0:
            k = int(cond[4:])
            medw = int(st.median(sum(t["words"] for t in TRAIN[u]["turns"][-k:]) for u in TEST))
        else: medw = None
        out[cond] = {"macro": round(mean, 4), "ci95": round(ci, 4), "n_users": n, "n_gens": n_lab,
                     "per_user": {u: round(v, 4) for u, v in per.items()},
                     "avg_words": round(st.mean(wl), 1) if wl else None,
                     "median_conditioned_words": medw}
        print(f"{cond:14s} acc={mean:.3f} ±{ci:.3f} (n={n}) err={1-mean:.3f} gens={n_lab} avgw={out[cond]['avg_words']}")
    (EXP/"scaling.json").write_text(json.dumps(
        {"model": MODEL_KEY, "gemini_model": GEMINI_MODEL, "results": out}, indent=1))
    print(f"wrote {EXP/'scaling.json'}")

if __name__ == "__main__":
    conds = ([f"hist{k}" for k in KS] + ["profile-full"] + [f"dist{k}" for k in DIST_KS])
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which != "all": conds = [c for c in conds if c in which.split(",")]
    run_conditions(conds)
    analyze([c for c in conds if any(f"gen|{pid}|{MODEL_KEY}|{c}" in _cache for pid in points)])

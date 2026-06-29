"""A/B: re-run deepseek-v4-pro on the TEST split at reasoning effort='max' (the highest
tier the model honors — verified via reasoning-token probe: low/med/high≈180-230,
xhigh≈381, max≈412) and compare CondAgree against the existing effort='low' baseline.

Identical to exp_condagree.py in points/prompt/seed/judge/metric; ONLY reasoning effort
changes. Max-effort gens are cached under the key suffix '@max' in a SEPARATE file
(rerun_raw_v4pro_max.jsonl) so the low-effort baseline in rerun_raw.jsonl is never touched.
The Haiku label cache is shared (content-addressed) so only genuinely new texts cost a judge call.
"""
import hashlib, json, math, sys, time, statistics as st
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "bench")); sys.path.insert(0, str(HERE))
import validate as V, v0_1, orouter
import taxonomy as TAX

TEST = json.loads((HERE / "splits.json").read_text())["test"]["qualifying_users"]
N_PER_USER = 30
CONDS = ["distilled", "generic"]
MODEL_ID = "deepseek/deepseek-v4-pro"
EFFORT = "max"
JUDGE = "anthropic/claude-haiku-4.5"
GEN_RETRIES = 4
LOW_RAW = HERE / "rerun_raw.jsonl"            # read-only here: low-effort gens + shared label cache
MAX_RAW = HERE / "rerun_raw_v4pro_max.jsonl"  # write: max-effort gens + any new labels
OUT = HERE / "v4pro_effort_ab.json"

# ---- caches: load low gens + label cache (LOW_RAW) and any prior max gens (MAX_RAW) ----
_cache = {}
def _load(p):
    if not p.exists(): return
    for l in p.read_text().splitlines():
        if not l.strip(): continue
        r = json.loads(l); t = r.get("text")
        if r.get("kind") == "gen" and (not str(t).strip() or str(t).startswith("Error:")):
            continue
        _cache[r["key"]] = r
_load(LOW_RAW); _load(MAX_RAW)
_lock = __import__("threading").Lock()
def put(rec):  # only ever appends to MAX_RAW (max gens + new labels); LOW_RAW stays untouched
    with _lock:
        _cache[rec["key"]] = rec
        with MAX_RAW.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def load_points():  # identical to exp_condagree.load_points
    pts = []
    for u in TEST:
        bys = v0_1.all_points_for(u); queues = [list(v) for v in bys.values()]; sp = []
        while len(sp) < N_PER_USER and any(queues):
            for q in queues:
                if q:
                    sp.append(q.pop(0))
                    if len(sp) >= N_PER_USER: break
        for p in sp: p["slug"] = u
        pts.extend(sp)
    return pts

def gen_max(point, cond):  # identical to exp_condagree.gen OR-branch, but effort=max; seed matches the low run
    folder = V.load_folder_text(point["slug"]) if cond == "distilled" else ""
    prompt = V.build_prompt(point, folder)
    seed = int(hashlib.sha256(f"{point['point_id']}|deepseek-v4-pro|{cond}".encode()).hexdigest(), 16) % (2**31)
    return v0_1.v0.clean_msg(orouter.chat(MODEL_ID, prompt, max_tokens=1200, temperature=0.7,
                                          reasoning_effort=EFFORT, seed=seed))

def _api_err(t):
    return (not t) or (not str(t).strip()) or str(t).startswith("Error:")

def label(text, prev_agent):  # identical to exp_condagree.label
    if V.is_interrupt(text):
        rest = TAX._strip_interrupt(text)
        if not rest: return "critical"
        text = rest
    if _api_err(text): return None
    k = "lab:haiku:" + hashlib.sha256((V.truncate_words(prev_agent,120)+"|"+V.truncate_words(text,150)).encode()).hexdigest()[:24]
    if k in _cache: return _cache[k]["move"]
    mv = TAX.classify(text, prev_agent, model=JUDGE, backend="or")
    if mv is not None: put({"key": k, "move": mv})
    return mv

def agg(xs):  # identical to exp_condagree.agg (t_19 95%)
    xs = [x for x in xs if x is not None]
    if not xs: return None
    m = st.mean(xs); s = st.stdev(xs) if len(xs) > 1 else 0
    return {"mean": round(m,3), "ci95": round(2.093*s/math.sqrt(len(xs)),3) if len(xs)>1 else 0, "n_users": len(xs)}

def words(t): return len((t or "").split())

def main():
    pts = load_points(); by = {p["point_id"]: p for p in pts}
    print(f"TEST {len(TEST)} users, {len(pts)} points, deepseek-v4-pro effort={EFFORT}")

    # ---- generate max-effort gens (resumable) ----
    todo = [(p,c) for p in pts for c in CONDS if f"gen|{p['point_id']}|deepseek-v4-pro@max|{c}" not in _cache]
    print(f"max-effort gens to run: {len(todo)}")
    def rg(j):
        p,c = j; txt = gen_max(p, c)
        for _ in range(GEN_RETRIES):
            if str(txt).strip() and not str(txt).startswith("Error:"): break
            txt = gen_max(p, c)
        return {"key": f"gen|{p['point_id']}|deepseek-v4-pro@max|{c}", "kind": "gen", "point_id": p["point_id"],
                "slug": p["slug"], "model": "deepseek-v4-pro", "model_id": MODEL_ID, "backend": "or",
                "effort": EFFORT, "cond": c, "text": txt, "ts": time.time()}
    if todo:
        done = 0
        with ThreadPoolExecutor(max_workers=64) as ex:
            for f in as_completed([ex.submit(rg, j) for j in todo]):
                r = f.result(); t = str(r.get("text",""))
                if t.strip() and not t.startswith("Error:"): put(r)
                done += 1
                if done % 100 == 0: print(f"  gen {done}/{len(todo)}")

    # ---- label real + low gens + max gens (shared Haiku cache) ----
    items = [("real", p, p["real"]) for p in pts]
    for p in pts:
        for c in CONDS:
            lo = _cache.get(f"gen|{p['point_id']}|deepseek-v4-pro|{c}")
            mx = _cache.get(f"gen|{p['point_id']}|deepseek-v4-pro@max|{c}")
            if lo: items.append((f"low|{c}", p, lo["text"]))
            if mx: items.append((f"max|{c}", p, mx["text"]))
    print(f"labeling {len(items)} items (shared Haiku cache)")
    moves = {}
    def rl(it):
        kind,p,text = it; return (kind, p["point_id"], label(text, p["prev_agent"]))
    with ThreadPoolExecutor(max_workers=64) as ex:
        done = 0
        for f in as_completed([ex.submit(rl, it) for it in items]):
            kind,pid,mv = f.result(); moves[(kind,pid)] = mv; done += 1
            if done % 300 == 0: print(f"  label {done}/{len(items)}")

    # ---- metrics: per-user CondAgree, low vs max, same real labels ----
    ptsU = defaultdict(list)
    for pid,p in by.items(): ptsU[p["slug"]].append(pid)
    realm = {pid: moves.get(("real",pid)) for pid in by}
    res = {}
    for arm in ["low", "max"]:
        for c in CONDS:
            per = []
            for u in TEST:
                pr = [(realm[pid], moves.get((f"{arm}|{c}",pid))) for pid in ptsU[u]]
                pr = [(a,b) for a,b in pr if a and b]
                if pr: per.append(sum(1 for a,b in pr if a==b)/len(pr))
            res[f"{arm}/{c}"] = {"condagree": agg(per), "per_user": [round(x,3) for x in per]}
    # response length (words), macro over all gens
    wlen = {}
    for arm,key in [("low","deepseek-v4-pro"),("max","deepseek-v4-pro@max")]:
        for c in CONDS:
            ws = [words(_cache[f"gen|{pid}|{key}|{c}"]["text"]) for pid in by
                  if f"gen|{pid}|{key}|{c}" in _cache]
            wlen[f"{arm}/{c}"] = round(st.mean(ws),1) if ws else None

    out = {"model": "deepseek-v4-pro", "low_effort": "low", "high_effort": EFFORT,
           "judge": JUDGE, "n_points": len(pts), "test_users": TEST,
           "condagree": res, "avg_words": wlen}
    OUT.write_text(json.dumps(out, indent=1))

    print(f"\n=== deepseek-v4-pro  CondAgree  low vs {EFFORT}  (TEST {len(TEST)} users) ===")
    for c in CONDS:
        lo = res[f"low/{c}"]["condagree"]; mx = res[f"max/{c}"]["condagree"]
        d = round(mx["mean"]-lo["mean"], 3)
        print(f"  {c:9s}  low {lo['mean']}±{lo['ci95']}   {EFFORT} {mx['mean']}±{mx['ci95']}   Δ {d:+}   "
              f"(avg words {wlen[f'low/{c}']} -> {wlen[f'max/{c}']})")
    print(f"\nwrote {OUT}")

if __name__ == "__main__":
    main()

"""Context-window scaling: how does simulation error change with the number of PRIOR TURNS of the
live session the simulator sees (no profile)?

Conditions ctx{N}, N in 1..10: the same frozen 480 test points, prompt context sliced to the last
min(N, available) turns. Model: gemini-3.5-flash (directive), direct Gemini API, thinking HIGH,
temp 0.7, deterministic seeds. Anchor: the leaderboard flash generic run (full 14-turn window).

Analyses on two populations: all 480 (dose-capped) and the 166 constant-dose points with >=10 prior
turns. Judging: Haiku via OpenRouter; the judge always sees the point's true prev_agent regardless of
N, so labels stay comparable across conditions and with the leaderboard cache.
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
MODEL_KEY = "gemini-3.5-flash-api"; GEMINI_MODEL = "gemini-3.5-flash"
ANCHOR_KEYS = ["gen|{pid}|gemini-3.5-flash|generic|high", "gen|{pid}|gemini-3.5-flash|generic"]
JUDGE = "anthropic/claude-haiku-4.5"
NS = list(range(1, 11))
CONC_GEN = 32; CONC_LAB = 48; PASSES = 4

TEST = json.loads((HERE/"splits.json").read_text())["test"]["qualifying_users"]

def _load_points():
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
        try: r = json.loads(l)
        except json.JSONDecodeError: _bad += 1; continue
        if r.get("kind") == "gen" and (not str(r.get("text","")).strip() or str(r.get("text","")).startswith("Error:")):
            continue
        _cache[r["key"]] = r
    if _bad: print(f"cache: skipped {_bad} corrupted lines", flush=True)
_lock = __import__("threading").Lock()
def put(rec):
    with _lock:
        _cache[rec["key"]] = rec
        with RAW.open("a") as f: f.write(json.dumps(rec, ensure_ascii=False)+"\n")

def gen(point, n):
    p2 = dict(point); p2["context"] = point["context"][-n:]
    prompt = V.build_prompt(p2, "")
    seed = int(hashlib.sha256(f"{point['point_id']}|{MODEL_KEY}|ctx{n}".encode()).hexdigest(), 16) % (2**31)
    txt = gemini_api.chat(GEMINI_MODEL, prompt, max_tokens=4000, temperature=0.7, seed=seed, thinking="HIGH")
    return (v0_1.v0.clean_msg(txt) if not txt.startswith("Error:") else txt), seed

def move_of(prev, text):
    if V.is_interrupt(text):
        rest = TAX._strip_interrupt(text)
        if not rest: return "critical"
        text = rest
    if not (text or "").strip() or str(text).startswith("Error:"): return None
    k = "lab:haiku:"+hashlib.sha256((V.truncate_words(prev,120)+"|"+V.truncate_words(text,150)).encode()).hexdigest()[:24]
    if k in _cache: return _cache[k]["move"]
    mv = TAX.classify(text, prev, model=JUDGE, backend="or")
    if mv is not None: put({"key": k, "move": mv})
    return mv

def run():
    for n in NS:
        for p_ in range(PASSES):
            todo = [p for p in points.values() if f"gen|{p['point_id']}|{MODEL_KEY}|ctx{n}" not in _cache]
            if not todo: break
            print(f"[ctx{n}] pass {p_+1}: {len(todo)} gens", flush=True)
            def one(p):
                txt, seed = gen(p, n)
                if txt.startswith("Error:") or not txt.strip(): return None
                return {"key": f"gen|{p['point_id']}|{MODEL_KEY}|ctx{n}", "kind": "gen",
                        "point_id": p["point_id"], "slug": p["slug"], "model": MODEL_KEY,
                        "model_id": GEMINI_MODEL, "backend": "gemini-api", "effort": "high",
                        "cond": f"ctx{n}", "text": txt, "seed": seed, "temperature": 0.7, "ts": time.time()}
            with ThreadPoolExecutor(max_workers=CONC_GEN) as ex:
                done = 0
                for f in as_completed([ex.submit(one, p) for p in todo]):
                    r = f.result()
                    if r: put(r)
                    done += 1
                    if done % 120 == 0: print(f"  [ctx{n}] {done}/{len(todo)}", flush=True)
        n_done = sum(1 for pid in points if f"gen|{pid}|{MODEL_KEY}|ctx{n}" in _cache)
        print(f"[ctx{n}] complete: {n_done}/480", flush=True)
        # label in parallel
        with ThreadPoolExecutor(max_workers=CONC_LAB) as ex:
            list(as_completed([ex.submit(move_of, points[pid]["prev_agent"], _cache[f"gen|{pid}|{MODEL_KEY}|ctx{n}"]["text"])
                               for pid in points if f"gen|{pid}|{MODEL_KEY}|ctx{n}" in _cache]))

def anchor_text(pid):
    for t in ANCHOR_KEYS:
        r = _cache.get(t.format(pid=pid))
        if r: return r.get("text")
    return None

def analyze():
    realm = {pid: move_of(p["prev_agent"], p["real"]) for pid, p in points.items()}
    deep = {pid for pid, p in points.items() if len(p["context"]) >= 10}
    print(f"constant-dose subset: {len(deep)} points")
    ptsU = defaultdict(list)
    for pid, p in points.items(): ptsU[p["slug"]].append(pid)
    def macro(cond_text, subset=None):
        per = {}
        for u, pids in ptsU.items():
            pr = []
            for pid in pids:
                if subset and pid not in subset: continue
                txt = cond_text(pid)
                if not txt: continue
                sm = move_of(points[pid]["prev_agent"], txt); rm = realm[pid]
                if sm and rm: pr.append((rm, sm))
            if pr: per[u] = sum(1 for a, b in pr if a == b)/len(pr)
        vals = list(per.values())
        if not vals: return None
        n = len(vals); mean = st.mean(vals)
        ci = (2.093 if n >= 20 else 2.26)*st.stdev(vals)/math.sqrt(n) if n > 1 else 0
        return {"macro": round(mean, 4), "ci95": round(ci, 4), "n_users": n,
                "per_user": {u: round(v, 4) for u, v in per.items()}}
    out = {"all480": {}, "constant_dose_166": {}}
    for n in NS:
        f = lambda pid, n=n: (_cache.get(f"gen|{pid}|{MODEL_KEY}|ctx{n}") or {}).get("text")
        out["all480"][f"ctx{n}"] = macro(f)
        out["constant_dose_166"][f"ctx{n}"] = macro(f, deep)
    out["all480"]["ctx14_anchor"] = macro(anchor_text)
    out["constant_dose_166"]["ctx14_anchor"] = macro(anchor_text, deep)
    for pop in out:
        print(f"\n== {pop} ==")
        for c, v in out[pop].items():
            if v: print(f"  {c:14s} acc={v['macro']:.3f} ±{v['ci95']:.3f} (n={v['n_users']}) err={1-v['macro']:.3f}")
    (EXP/"scaling_context.json").write_text(json.dumps(
        {"model": MODEL_KEY, "gemini_model": GEMINI_MODEL, "ns": NS, "results": out}, indent=1))
    print(f"\nwrote {EXP/'scaling_context.json'}")

if __name__ == "__main__":
    run()
    analyze()

"""Reproducible multi-model accuracy experiment on the repo-disjoint TEST split.

Records full artifacts for later analysis/reproduction under
bench/profileopt/experiments/accuracy/:
  manifest.json  — all config: models, OpenRouter ids, reasoning efforts, concurrency, split,
                   taxonomy, judge, N_PER_USER, n_points, git sha, timestamp
  points.jsonl   — the frozen prediction points (point_id, slug, repo, prev_agent, real_text)
  raw.jsonl      — every generation (with model_id, backend, effort, seed, ts) + every move label
  summary.json   — per (model,cond) accuracy macro + per-user values

Per-model reasoning effort + backend; per-backend concurrency (OpenRouter 64, Modal 32).
Single Haiku judge + v2 4-way taxonomy (κ≈0.80 -> majority unnecessary). Resumable cache.
"""
import hashlib, json, math, subprocess, sys, time, statistics as st
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "bench")); sys.path.insert(0, str(HERE))
import validate as V, orouter
import osim_backend as OB
import taxonomy as TAX
import points as PT

EXP = HERE / "experiments" / "accuracy"
EXP.mkdir(parents=True, exist_ok=True)
RAW = HERE / "rerun_raw.jsonl"        # shared resumable cache (already holds deepseek-v3.1, osim-4b, v4*)
JUDGE = "anthropic/claude-haiku-4.5"  # single cheapest judge
GEN_RETRIES = 4  # retry transient API failures (rate-limit / 5xx / cap) in-call before giving up
N_PER_USER = 30
TEST = json.loads((HERE / "splits.json").read_text())["test"]["qualifying_users"]
CONDS = ["distilled", "generic"]

MODELS = [
    {"name": "deepseek-v3.1",     "backend": "or",    "id": "deepseek/deepseek-chat-v3.1", "effort": "low",   "conc": 64},
    {"name": "deepseek-v4-flash", "backend": "or",    "id": "deepseek/deepseek-v4-flash",  "effort": "low",   "conc": 64},
    {"name": "deepseek-v4-pro",   "backend": "or",    "id": "deepseek/deepseek-v4-pro",    "effort": "max",   "conc": 64},
    {"name": "gpt-5.5",           "backend": "or",    "id": "openai/gpt-5.5",              "effort": "xhigh", "conc": 64},
    {"name": "claude-opus-4.8",   "backend": "or",    "id": "anthropic/claude-opus-4.8",   "effort": "xhigh", "conc": 64},
    {"name": "glm-5.2",           "backend": "or",    "id": "z-ai/glm-5.2",                "effort": "max",   "conc": 64},
    {"name": "gemini-3.1-pro",    "backend": "or",    "id": "google/gemini-3.1-pro-preview","effort": "high", "conc": 64},
    {"name": "osim-4b",           "backend": "modal", "id": "osim-4b",                     "effort": None,    "conc": 32},
    {"name": "osim-8b",           "backend": "modal", "id": "osim-8b",                     "effort": None,    "conc": 32},
]
MCFG = {m["name"]: m for m in MODELS}

_cache = {}
if RAW.exists():
    for l in RAW.read_text().splitlines():
        if not l.strip(): continue
        r = json.loads(l); t = r.get("text")
        if r.get("kind") == "gen" and (not str(t).strip() or str(t).startswith("Error:")):
            continue  # treat failed gens as absent -> todo() regenerates (backfills) them this run
        _cache[r["key"]] = r
_lock = __import__("threading").Lock()
def put(rec):
    with _lock:
        _cache[rec["key"]] = rec
        with RAW.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def load_points():
    pts = []
    for u in TEST:
        bys = PT.all_points_for(u); queues = [list(v) for v in bys.values()]; sp = []
        while len(sp) < N_PER_USER and any(queues):
            for q in queues:
                if q:
                    sp.append(q.pop(0))
                    if len(sp) >= N_PER_USER: break
        for p in sp: p["slug"] = u
        pts.extend(sp)
    return pts

def gen(point, mname, cond):
    cfg = MCFG[mname]
    folder = V.load_folder_text(point["slug"]) if cond == "distilled" else ""
    if cfg["backend"] == "modal":
        return OB.chat(cfg["id"], OB.build_osim_messages(point, folder, V.truncate_words), max_tokens=500), {}
    prompt = V.build_prompt(point, folder)
    seed = int(hashlib.sha256(f"{point['point_id']}|{mname}|{cond}".encode()).hexdigest(), 16) % (2**31)
    txt = PT.clean_msg(orouter.chat(cfg["id"], prompt, max_tokens=1200, temperature=0.7,
                                    reasoning_effort=cfg["effort"], seed=seed))
    return txt, {"seed": seed, "temperature": 0.7}

def _api_err(t):
    return (not t) or (not str(t).strip()) or str(t).startswith("Error:")

def label(text, prev_agent):
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

def agg(xs):
    xs = [x for x in xs if x is not None]
    if not xs: return None
    m = st.mean(xs); s = st.stdev(xs) if len(xs) > 1 else 0
    return {"mean": round(m,3), "ci95": round(2.093*s/math.sqrt(len(xs)),3) if len(xs)>1 else 0, "n_users": len(xs)}  # t_19

def run_gens(jobs, conc, tag):
    if not jobs: return
    print(f"  [{tag}] {len(jobs)} gens @ conc {conc}")
    def rg(j):
        p,mname,c = j
        txt, meta = gen(p, mname, c)
        for _ in range(GEN_RETRIES):
            if str(txt).strip() and not str(txt).startswith("Error:"): break
            txt, meta = gen(p, mname, c)  # retry transient failures before caching
        cfg = MCFG[mname]
        return {"key": f"gen|{p['point_id']}|{mname}|{c}|{cfg['effort']}", "kind": "gen", "point_id": p["point_id"], "slug": p["slug"],
                "model": mname, "model_id": cfg["id"], "backend": cfg["backend"], "effort": cfg["effort"],
                "cond": c, "text": txt, "ts": time.time(), **meta}
    done = 0
    with ThreadPoolExecutor(max_workers=conc) as ex:
        for f in as_completed([ex.submit(rg, j) for j in jobs]):
            r = f.result(); t = str(r.get("text", ""))
            if t.strip() and not t.startswith("Error:"): put(r)  # never cache failures -> they retry on the next run
            done += 1
            if done % 100 == 0: print(f"    [{tag}] {done}/{len(jobs)}")

def main():
    pts = load_points(); by = {p["point_id"]: p for p in pts}
    print(f"TEST {len(TEST)} users, {len(pts)} points, {len(MODELS)} models x {len(CONDS)} conds")

    # ---- artifacts: manifest + frozen points ----
    sha = subprocess.run(["git","rev-parse","HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (EXP/"manifest.json").write_text(json.dumps({
        "experiment": "accuracy", "timestamp": time.time(), "git_sha": sha,
        "taxonomy": "v2-4way (bench/profileopt/taxonomy.py)", "judge_model": JUDGE,
        "split_file": "bench/profileopt/splits.json", "test_users": TEST,
        "n_per_user": N_PER_USER, "n_points": len(pts), "conds": CONDS, "models": MODELS,
        "note": "prompts reconstructable via validate.build_prompt / osim_backend.build_osim_messages "
                "from points.jsonl + users/<slug>/ folder at git_sha; cache=bench/profileopt/rerun_raw.jsonl",
    }, indent=1))
    with (EXP/"points.jsonl").open("w") as f:
        for p in pts:
            f.write(json.dumps({"point_id": p["point_id"], "slug": p["slug"], "repo": p["repo"],
                                "turn_index": p["turn_index"], "prev_agent": p["prev_agent"], "real_text": p["real"]}, ensure_ascii=False)+"\n")

    # ---- generate: every model in its OWN pool, all models concurrently (different providers,
    #      no shared rate limits), each at its configured concurrency ----
    todo = lambda mn: [(p,mn,c) for p in pts for c in CONDS if f"gen|{p['point_id']}|{mn}|{c}|{MCFG[mn]['effort']}" not in _cache]
    def gen_one_model(m):
        jobs = todo(m["name"])
        if jobs: run_gens(jobs, m["conc"], m["name"])
    with ThreadPoolExecutor(max_workers=len(MODELS)) as outer:
        for f in as_completed([outer.submit(gen_one_model, m) for m in MODELS]):
            f.result()

    # ---- label real + every gen (single Haiku) ----
    items = [("real", p, p["real"]) for p in pts]
    for p in pts:
        for m in MODELS:
            for c in CONDS:
                g = _cache.get(f"gen|{p['point_id']}|{m['name']}|{c}|{m['effort']}")
                if g: items.append((f"{m['name']}|{c}", p, g["text"]))
    print(f"labeling {len(items)} items (single Haiku, cached)")
    moves = {}
    def rl(it):
        kind,p,text = it; return (kind, p["point_id"], label(text, p["prev_agent"]))
    with ThreadPoolExecutor(max_workers=64) as ex:
        done = 0
        for f in as_completed([ex.submit(rl, it) for it in items]):
            kind,pid,mv = f.result(); moves[(kind,pid)] = mv; done += 1
            if done % 300 == 0: print(f"  label {done}/{len(items)}")

    # ---- metrics ----
    ptsU = defaultdict(list)
    for pid,p in by.items(): ptsU[p["slug"]].append(pid)
    realm = {pid: moves.get(("real",pid)) for pid in by}
    res = {}
    for m in MODELS:
        for c in CONDS:
            per = []
            for u in TEST:
                pr = [(realm[pid], moves.get((f"{m['name']}|{c}",pid))) for pid in ptsU[u]]
                pr = [(a,b) for a,b in pr if a and b]
                if pr: per.append(sum(1 for a,b in pr if a==b)/len(pr))
            res[f"{m['name']}/{c}"] = {"accuracy": agg(per), "per_user": [round(x,3) for x in per]}
    lg = []
    for u in TEST:
        rms = [realm[pid] for pid in ptsU[u] if realm[pid]]; n=len(rms); rc=Counter(rms)
        if n>1: lg.append((n*sum((v/n)**2 for v in rc.values())-1)/(n-1))
    rd = Counter(realm[pid] for pid in by if realm[pid])
    out = {"taxonomy":"v2-4way","judge":JUDGE,"test_users":TEST,"n_points":len(pts),
           "lucky_guess": round(st.mean(lg),3),
           "real_move_dist": {k: round(v/sum(rd.values()),3) for k,v in rd.most_common()},
           "models": [m["name"] for m in MODELS], "results": res}
    (EXP/"summary.json").write_text(json.dumps(out, indent=1))
    (HERE/"rerun_summary.json").write_text(json.dumps(out, indent=1))
    subprocess.run(["cp", str(RAW), str(EXP/"raw.jsonl")])
    print(f"\n=== accuracy (v2 4-way, Haiku) — TEST {len(TEST)} users, lucky-guess={out['lucky_guess']} ===")
    print("real move dist:", out["real_move_dist"])
    for m in MODELS:
        d0=res[f"{m['name']}/generic"]["accuracy"]; d1=res[f"{m['name']}/distilled"]["accuracy"]
        dd = round((d1['mean'] or 0)-(d0['mean'] or 0),3) if d0 and d1 else None
        print(f"  {m['name']:18s} no-prof {d0['mean']}±{d0['ci95']}  prof {d1['mean']}±{d1['ci95']}  Δ {dd:+}")
    print(f"\nartifacts -> {EXP}")

if __name__ == "__main__":
    main()

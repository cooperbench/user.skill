"""Finalize the deepseek-v4-pro low-vs-max A/B from cached gens (no generation).
Labels real + low + max gen texts (shared Haiku cache) and computes per-user CondAgree,
identical metric to exp_condagree.py. Writes v4pro_effort_ab.json."""
import hashlib, json, math, sys, statistics as st
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "bench")); sys.path.insert(0, str(HERE))
import validate as V, v0_1
import taxonomy as TAX

TEST = json.loads((HERE / "splits.json").read_text())["test"]["qualifying_users"]
N_PER_USER = 30
CONDS = ["distilled", "generic"]
JUDGE = "anthropic/claude-haiku-4.5"
LOW_RAW = HERE / "rerun_raw.jsonl"
MAX_RAW = HERE / "rerun_raw_v4pro_max.jsonl"
OUT = HERE / "v4pro_effort_ab.json"

_cache = {}
def _load(p):
    if not p.exists(): return
    for l in p.read_text().splitlines():
        if not l.strip(): continue
        r = json.loads(l); t = r.get("text")
        if r.get("kind") == "gen" and (not str(t).strip() or str(t).startswith("Error:")): continue
        _cache[r["key"]] = r
_load(LOW_RAW); _load(MAX_RAW)
_lock = __import__("threading").Lock()
def put(rec):
    with _lock:
        _cache[rec["key"]] = rec
        with MAX_RAW.open("a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def load_points():
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

def _api_err(t): return (not t) or (not str(t).strip()) or str(t).startswith("Error:")
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
    return {"mean": round(m,3), "ci95": round(2.093*s/math.sqrt(len(xs)),3) if len(xs)>1 else 0, "n_users": len(xs)}

def words(t): return len((t or "").split())

def main():
    pts = load_points(); by = {p["point_id"]: p for p in pts}
    items = [("real", p, p["real"]) for p in pts]
    miss = 0
    for p in pts:
        for c in CONDS:
            lo = _cache.get(f"gen|{p['point_id']}|deepseek-v4-pro|{c}")
            mx = _cache.get(f"gen|{p['point_id']}|deepseek-v4-pro@max|{c}")
            if lo: items.append((f"low|{c}", p, lo["text"]))
            if mx: items.append((f"max|{c}", p, mx["text"]))
            else: miss += 1
    print(f"{len(pts)} points; max gens missing: {miss}; labeling {len(items)} items")
    moves = {}
    def rl(it):
        kind,p,text = it; return (kind, p["point_id"], label(text, p["prev_agent"]))
    with ThreadPoolExecutor(max_workers=64) as ex:
        done = 0
        for f in as_completed([ex.submit(rl, it) for it in items]):
            kind,pid,mv = f.result(); moves[(kind,pid)] = mv; done += 1
            if done % 300 == 0: print(f"  label {done}/{len(items)}")

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
    wlen = {}
    for arm,key in [("low","deepseek-v4-pro"),("max","deepseek-v4-pro@max")]:
        for c in CONDS:
            ws = [words(_cache[f"gen|{pid}|{key}|{c}"]["text"]) for pid in by if f"gen|{pid}|{key}|{c}" in _cache]
            wlen[f"{arm}/{c}"] = round(st.mean(ws),1) if ws else None

    out = {"model":"deepseek-v4-pro","low_effort":"low","high_effort":"max","judge":JUDGE,
           "n_points":len(pts),"max_gens_missing":miss,"test_users":TEST,"condagree":res,"avg_words":wlen}
    OUT.write_text(json.dumps(out, indent=1))
    print(f"\n=== deepseek-v4-pro CondAgree  low vs max  (TEST {len(TEST)} users) ===")
    for c in CONDS:
        lo = res[f"low/{c}"]["condagree"]; mx = res[f"max/{c}"]["condagree"]
        d = round(mx["mean"]-lo["mean"],3)
        print(f"  {c:9s} low {lo['mean']}±{lo['ci95']}  max {mx['mean']}±{mx['ci95']}  Δ {d:+}  "
              f"(words {wlen['low/'+c]}->{wlen['max/'+c]}, n_users {lo['n_users']}/{mx['n_users']})")
    print(f"wrote {OUT}")

if __name__ == "__main__":
    main()

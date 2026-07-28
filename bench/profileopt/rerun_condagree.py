"""Rerun deepseek-v3.1 + osim-4b, with and without profile, on the TEST split users,
scoring CondAgree under the v2 4-way taxonomy (3-judge majority labels). Per-user macro + 95% CI.

Leakage-clean: TEST users are user- AND repo-disjoint from train/val (splits.json); per-user the
profile comes from the user's TRAIN sessions (data/digests) and we score on held-out turns.
"""
import argparse, hashlib, json, math, sys, statistics as st
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "bench")); sys.path.insert(0, str(HERE))
import validate as V, v0_1, orouter
import osim_backend as OB
import taxonomy as TAX

TEST = json.loads((HERE / "splits.json").read_text())["test"]["qualifying_users"]
N_PER_USER = 30
MODELS = {"deepseek-v3.1": "deepseek/deepseek-chat-v3.1", "deepseek-v4-flash": "deepseek/deepseek-v4-flash", "deepseek-v4-pro": "deepseek/deepseek-v4-pro", "osim-4b": "osim-4b"}
KEY_EFFORT = {m: (None if m == "osim-4b" else "low") for m in MODELS}  # gen() runs orouter models at 'low', osim has none; mirror into the effort-suffixed cache key (matches exp_condagree.py)
CONDS = ["distilled", "generic"]
RAW = HERE / "rerun_raw.jsonl"
JUDGE = "anthropic/claude-haiku-4.5"  # single cheapest judge — the 4-way taxonomy is reliable enough (κ≈0.80)

# ---------- caches ----------
_cache = {}
if RAW.exists():
    for l in RAW.read_text().splitlines():
        if l.strip():
            r = json.loads(l); _cache[r["key"]] = r
_lock = __import__("threading").Lock()
def put(rec):
    with _lock:
        _cache[rec["key"]] = rec
        with RAW.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

# ---------- points ----------
def load_points():
    pts = []
    for u in TEST:
        sp = []
        bys = v0_1.all_points_for(u)  # {session: [points]}
        queues = [list(v) for v in bys.values()]
        while len(sp) < N_PER_USER and any(queues):
            for q in queues:
                if q:
                    sp.append(q.pop(0))
                    if len(sp) >= N_PER_USER:
                        break
        for p in sp:
            p["slug"] = u
        pts.extend(sp)
        print(f"  {u:20s} {len(sp)} points / {len(bys)} sessions  folder={'Y' if (ROOT/'users'/u/'USER.md').exists() else 'N'}")
    return pts

# ---------- generation ----------
def gen(point, model, cond):
    folder = V.load_folder_text(point["slug"]) if cond == "distilled" else ""
    if model == "osim-4b":
        return OB.chat("osim-4b", OB.build_osim_messages(point, folder, V.truncate_words), max_tokens=500)
    prompt = V.build_prompt(point, folder)
    seed = int(hashlib.sha256(f"{point['point_id']}|{model}|{cond}".encode()).hexdigest(), 16) % (2**31)
    return v0_1.v0.clean_msg(orouter.chat(MODELS[model], prompt, max_tokens=1000, temperature=0.7,
                                          reasoning_effort="low", seed=seed))

# ---------- single-judge (Haiku) labeling, 4-way taxonomy, content-addressed cache ----------
def label(text, prev_agent):
    if V.is_interrupt(text):
        rest = TAX._strip_interrupt(text)
        if not rest:
            return "critical"
        text = rest
    if not (text or "").strip() or V.is_cli_failure(text):
        return None
    k = "lab:haiku:" + hashlib.sha256((V.truncate_words(prev_agent,120)+"|"+V.truncate_words(text,150)).encode()).hexdigest()[:24]
    if k in _cache:
        return _cache[k]["move"]
    mv = TAX.classify(text, prev_agent, model=JUDGE, backend="or")
    put({"key": k, "move": mv})
    return mv

def agg(xs):
    xs = [x for x in xs if x is not None]
    if not xs: return None
    m = st.mean(xs); s = st.stdev(xs) if len(xs)>1 else 0
    return {"mean": round(m,3), "ci95": round(2.447*s/math.sqrt(len(xs)),3) if len(xs)>1 else 0, "n_users": len(xs)}  # t_6

def main():
    print(f"TEST users ({len(TEST)}):")
    pts = load_points()
    by = {p["point_id"]: p for p in pts}
    print(f"TOTAL {len(pts)} points\n")

    # 1. generate
    gj = [(p,m,c) for p in pts for m in MODELS for c in CONDS if f"gen|{p['point_id']}|{m}|{c}|{KEY_EFFORT[m]}" not in _cache]
    print(f"generations: {len(gj)} to run")
    def rg(j):
        p,m,c=j; return {"key":f"gen|{p['point_id']}|{m}|{c}|{KEY_EFFORT[m]}","kind":"gen","point_id":p["point_id"],"slug":p["slug"],"model":m,"cond":c,"effort":KEY_EFFORT[m],"text":gen(p,m,c)}
    with ThreadPoolExecutor(max_workers=64) as ex:
        for i,f in enumerate(as_completed([ex.submit(rg,j) for j in gj]),1):
            put(f.result())
            if i%50==0: print(f"  gen {i}/{len(gj)}")

    # 2. label (real + every gen), 3 judges, parallel over (item) -> majority
    items = []  # (kind,pid,text,prev_agent, key_for_move)
    for p in pts:
        items.append(("real", p, p["real"]))
        for m in MODELS:
            for c in CONDS:
                g=_cache.get(f"gen|{p['point_id']}|{m}|{c}|{KEY_EFFORT[m]}")
                if g: items.append((f"{m}|{c}", p, g["text"]))
    print(f"labeling {len(items)} items (single Haiku judge, cached)")
    def rl(it):
        kind,p,text=it
        return (kind,p["point_id"], label(text, p["prev_agent"]))
    moves={}
    with ThreadPoolExecutor(max_workers=64) as ex:
        for i,f in enumerate(as_completed([ex.submit(rl,it) for it in items]),1):
            kind,pid,mv=f.result(); moves[(kind,pid)]=mv
            if i%100==0: print(f"  label {i}/{len(items)}")

    # 3. metrics per user -> macro
    ptsU=defaultdict(list)
    for pid,p in by.items(): ptsU[p["slug"]].append(pid)
    realm={pid:moves.get(("real",pid)) for pid in by}
    res={}
    for m in MODELS:
        for c in CONDS:
            per=[]
            for u in TEST:
                pairs=[(realm[pid], moves.get((f"{m}|{c}",pid))) for pid in ptsU[u]]
                pairs=[(a,b) for a,b in pairs if a and b]
                if pairs: per.append(sum(1 for a,b in pairs if a==b)/len(pairs))
            res[f"{m}/{c}"]={"condagree":agg(per),"per_user":[round(x,3) for x in per]}
    # lucky-guess (unbiased Σp²) per user, macro
    lg=[]
    for u in TEST:
        rms=[realm[pid] for pid in ptsU[u] if realm[pid]]; n=len(rms); rc=Counter(rms)
        if n>1:
            s2=sum((v/n)**2 for v in rc.values()); lg.append((n*s2-1)/(n-1))
    real_dist=Counter(realm[pid] for pid in by if realm[pid])
    out={"taxonomy":"v2-4way","test_users":TEST,"n_points":len(pts),
         "lucky_guess":round(st.mean(lg),3),
         "real_move_dist":{k:round(v/sum(real_dist.values()),3) for k,v in real_dist.most_common()},
         "results":res, "judges":[JUDGE]}
    (HERE/"rerun_summary.json").write_text(json.dumps(out,indent=1))
    print(f"\n=== CondAgree (v2 4-way, single Haiku judge) — TEST {len(TEST)} users, lucky-guess={out['lucky_guess']} ===")
    print("real move dist:", out["real_move_dist"])
    for k in [f"{m}/{c}" for m in MODELS for c in CONDS]:
        d=res[k]["condagree"]; print(f"  {k:26s} CondAgree = {d['mean']} ± {d['ci95']}  (n_users={d['n_users']})")
    print(f"\nwrote {HERE/'rerun_summary.json'}")

if __name__ == "__main__":
    main()

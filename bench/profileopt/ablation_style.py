"""Contrastive-prefix ablation: does a CONTENT-FREE style instruction reproduce the persona gain?
Replace the distilled persona with a generic "terse, do not ask clarifying questions" style profile,
for glm-5.2 (the big winner) and gpt-5.5 (control: no reflex to fix). Re-score CondAgree + the
spurious-inquiry rate + word count, and compare generic vs distilled vs styleonly.

Two-factor prediction:
  - GLM: styleonly recovers most of the +0.084 gain  => the win is generic reflex-suppression.
  - GPT-5.5: styleonly ~ 0 (nothing to fix).
"""
import hashlib, json, math, sys, time, statistics as st
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT/"scripts")); sys.path.insert(0, str(ROOT/"bench")); sys.path.insert(0, str(HERE))
import validate as V, v0_1, orouter, taxonomy as TAX
EXP = HERE/"experiments"/"condagree_multi"; RAW = HERE/"rerun_raw.jsonl"
JUDGE = "anthropic/claude-haiku-4.5"
CATS = ["approve","critical","directive","inquiry"]
# content-free style profile (NO developer-specific information): targets the assistant reflex only
STYLE = ("Style only. The developer is a busy senior engineer. They reply tersely and directly, "
         "usually in under 12 words. They rarely ask clarifying questions; they prefer to give a quick "
         "instruction, a blunt correction, or a one-word yes/no. They do not explain themselves or "
         "restate the task. (No other information about this developer is known.)")
MODELS = {"glm-5.2":{"id":"z-ai/glm-5.2","effort":"max"}, "gpt-5.5":{"id":"openai/gpt-5.5","effort":"xhigh"}}

TEST=json.loads((HERE/"splits.json").read_text())["test"]["qualifying_users"]
def _load_points():  # same deterministic loader as exp_condagree -> same point_ids, but with full "context"
    pts={}
    for u in TEST:
        bys=v0_1.all_points_for(u); queues=[list(v) for v in bys.values()]; sp=[]
        while len(sp)<30 and any(queues):
            for q in queues:
                if q:
                    sp.append(q.pop(0))
                    if len(sp)>=30: break
        for p in sp:
            p["slug"]=u; pts[p["point_id"]]=p
    return pts
points=_load_points()
_cache={}
if RAW.exists():
    for l in RAW.read_text().splitlines():
        if l.strip(): r=json.loads(l); _cache[r["key"]]=r
_lock=__import__("threading").Lock()
def put(rec):
    with _lock:
        _cache[rec["key"]]=rec
        with RAW.open("a") as f: f.write(json.dumps(rec,ensure_ascii=False)+"\n")
def move_of(prev,text):
    if V.is_interrupt(text):
        rest=TAX._strip_interrupt(text)
        if not rest: return "critical"
        text=rest
    if not (text or "").strip() or str(text).startswith("Error:"): return None
    k="lab:haiku:"+hashlib.sha256((V.truncate_words(prev,120)+"|"+V.truncate_words(text,150)).encode()).hexdigest()[:24]
    if k in _cache: return _cache[k]["move"]
    mv=TAX.classify(text,prev,model=JUDGE,backend="or")
    if mv is not None: put({"key":k,"move":mv})
    return mv
def words(t): return len((t or "").split())

def gen_styleonly(point, mname):
    cfg=MODELS[mname]
    prompt=V.build_prompt(point, STYLE)
    seed=int(hashlib.sha256(f"{point['point_id']}|{mname}|styleonly".encode()).hexdigest(),16)%(2**31)
    return v0_1.v0.clean_msg(orouter.chat(cfg["id"],prompt,max_tokens=1200,temperature=0.7,reasoning_effort=cfg["effort"],seed=seed))

def run():
    # 1. generate styleonly for both models (per-model concurrent pools @64)
    todo=[(p,m) for p in points.values() for m in MODELS if f"gen|{p['point_id']}|{m}|styleonly" not in _cache]
    print(f"styleonly gens to run: {len(todo)}")
    def one(j):
        p,m=j
        return {"key":f"gen|{p['point_id']}|{m}|styleonly","kind":"gen","point_id":p["point_id"],"slug":p["slug"],
                "model":m,"cond":"styleonly","text":gen_styleonly(p,m),"ts":time.time()}
    with ThreadPoolExecutor(max_workers=64) as ex:
        done=0
        for f in as_completed([ex.submit(one,j) for j in todo]):
            put(f.result()); done+=1
            if done%100==0: print(f"  gen {done}/{len(todo)}")

    # 2. label every needed gen (generic/distilled/styleonly) + real, single Haiku
    realm={pid:move_of(p["prev_agent"],p["real"]) for pid,p in points.items()}
    def simmove(pid,m,cond): return move_of(points[pid]["prev_agent"], _cache.get(f"gen|{pid}|{m}|{cond}",{}).get("text",""))
    # parallel label warm-up for styleonly
    items=[(pid,m) for pid in points for m in MODELS]
    with ThreadPoolExecutor(max_workers=64) as ex:
        list(as_completed([ex.submit(simmove,pid,m,"styleonly") for pid,m in items]))

    # 3. metrics per model x cond
    ptsU=defaultdict(list)
    for pid,p in points.items(): ptsU[p["slug"]].append(pid)
    def macro(m,cond):
        per=[]
        for u,pids in ptsU.items():
            pr=[(realm[pid],simmove(pid,m,cond)) for pid in pids]; pr=[(a,b) for a,b in pr if a and b]
            if pr: per.append(sum(1 for a,b in pr if a==b)/len(pr))
        n=len(per); mean=st.mean(per); ci=(2.09*st.stdev(per)/math.sqrt(n)) if n>1 else 0
        return {"mean":round(mean,3),"ci":round(ci,3),"n_users":n}
    def diag(m,cond):  # micro CA, spurious-inquiry rate, avg words, per-cat recall
        hit=tot=0; spur=spurt=0; wl=[]; rec=defaultdict(lambda:[0,0])
        for pid,p in points.items():
            rm=realm[pid]; sm=simmove(pid,m,cond)
            if not rm or not sm: continue
            tot+=1; hit+= (sm==rm); wl.append(words(_cache.get(f"gen|{pid}|{m}|{cond}",{}).get("text","")))
            rec[rm][1]+=1; rec[rm][0]+= (sm==rm)
            if rm!="inquiry": spurt+=1; spur+= (sm=="inquiry")
        return {"micro":round(hit/tot,3),"spurious_inquiry":round(spur/spurt,3),"avg_words":round(st.mean(wl),1),
                "recall":{c:(round(rec[c][0]/rec[c][1],3) if rec[c][1] else None) for c in CATS}}
    out={"style_prefix":STYLE,"models":{}}
    print("\n=== ABLATION: generic vs distilled(persona) vs styleonly(content-free) ===")
    for m in MODELS:
        out["models"][m]={}
        print(f"\n## {m}")
        print(f"  {'cond':10s} | {'CondAgree(macro)':>18s} | {'micro':>6s} | {'spurInq':>7s} | {'words':>5s} | recall a/c/d/i")
        for cond in ["generic","distilled","styleonly"]:
            mc=macro(m,cond); dg=diag(m,cond); out["models"][m][cond]={**mc,**dg}
            rc=dg["recall"]
            print(f"  {cond:10s} | {mc['mean']:.3f} ± {mc['ci']:.3f} (n={mc['n_users']:2d}) | {dg['micro']:.3f} | {dg['spurious_inquiry']:7.3f} | {dg['avg_words']:5.1f} | "
                  +"/".join(f"{(rc[c] if rc[c] is not None else 0):.2f}" for c in CATS))
        g=out["models"][m]["generic"]["mean"]; d=out["models"][m]["distilled"]["mean"]; s=out["models"][m]["styleonly"]["mean"]
        persona_gain=d-g; style_gain=s-g
        frac = round(style_gain/persona_gain,2) if abs(persona_gain)>1e-6 else None
        out["models"][m]["summary"]={"persona_gain":round(persona_gain,3),"style_gain":round(style_gain,3),"style_recovers_frac":frac}
        print(f"  -> persona gain {persona_gain:+.3f}, style-only gain {style_gain:+.3f}"+(f", style recovers {frac:.0%} of persona gain" if frac is not None else ""))
    (EXP/"ablation.json").write_text(json.dumps(out,indent=1))
    print(f"\nwrote {EXP/'ablation.json'}")

if __name__=="__main__": run()

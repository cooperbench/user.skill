"""Deeper analysis of WHY the profile helps glm-5.2 so much.
1. avg message length (words) per model/cond, vs the real developers' length  -> verbosity chart
2. length reduction per model, vs its CondAgree gain  -> steerability
3. glm-5.2 no-profile: agree-rate binned by message length  -> does verbosity itself cause misses?
4. confusion matrices (real move -> predicted move) for glm-5.2 ±profile + contrasts (gpt-5.5, opus)
Writes verbosity.json for the website chart; prints the rest for reasoning.
"""
import hashlib, json, sys, statistics as st
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(HERE))
import validate as V, taxonomy as TAX
EXP = HERE / "experiments" / "condagree_multi"
CATS = ["approve", "critical", "directive", "inquiry"]
MODELS = ["glm-5.2","gpt-5.5","gemini-3.1-pro","claude-opus-4.8","deepseek-v4-pro","deepseek-v4-flash","deepseek-v3.1","osim-4b","osim-8b"]
LABEL = {"glm-5.2":"GLM-5.2","gpt-5.5":"GPT-5.5","gemini-3.1-pro":"Gemini-3.1-Pro","claude-opus-4.8":"Claude-Opus-4.8",
         "deepseek-v4-pro":"DeepSeek-V4-Pro","deepseek-v4-flash":"DeepSeek-V4-Flash","deepseek-v3.1":"DeepSeek-V3.1","osim-4b":"OSim-4B","osim-8b":"OSim-8B"}
KIND = {m:("specialized" if m.startswith("osim") else "general") for m in MODELS}

points={}
for l in (EXP/"points.jsonl").read_text().splitlines():
    if l.strip(): p=json.loads(l); points[p["point_id"]]=p
gens,labels={},{}
for l in (EXP/"raw.jsonl").read_text().splitlines():
    if not l.strip(): continue
    r=json.loads(l); k=r.get("key","")
    if r.get("kind")=="gen": gens[(r["point_id"],r["model"],r["cond"])]=r["text"]
    elif k.startswith("lab:"): labels[k]=r.get("move")
def move_of(prev,text):
    if V.is_interrupt(text):
        rest=TAX._strip_interrupt(text)
        if not rest: return "critical"
        text=rest
    if not (text or "").strip() or str(text).startswith("Error:"): return None
    return labels.get("lab:haiku:"+hashlib.sha256((V.truncate_words(prev,120)+"|"+V.truncate_words(text,150)).encode()).hexdigest()[:24])
def words(t): return len((t or "").split())

realm={pid:move_of(p["prev_agent"],p["real_text"]) for pid,p in points.items()}
real_words=st.median([words(p["real_text"]) for p in points.values()])
real_mean=round(st.mean([words(p["real_text"]) for p in points.values()]),1)
print(f"REAL developer message length: mean {real_mean} words, median {real_words}\n")

# 1+2 word counts + gain
print(f"{'model':17s} {'words_np':>8s} {'words_wp':>8s} {'Δlen':>6s} | {'CA_np':>6s} {'CA_wp':>6s} {'ΔCA':>7s}")
rows=[]
for m in MODELS:
    wn=[]; ww=[]; hn=tn=hw=tw=0
    for pid,p in points.items():
        rm=realm[pid]
        gt=gens.get((pid,m,"generic")); dt=gens.get((pid,m,"distilled"))
        sn=move_of(p["prev_agent"],gt); sw=move_of(p["prev_agent"],dt)
        if rm and sn: wn.append(words(gt)); tn+=1; hn+= (sn==rm)
        if rm and sw: ww.append(words(dt)); tw+=1; hw+= (sw==rm)
    a=round(st.mean(wn),1); b=round(st.mean(ww),1); can=hn/tn; caw=hw/tw
    am=round(st.median(wn)); bm=round(st.median(ww))
    rows.append({"id":m,"label":LABEL[m],"kind":KIND[m],"np":a,"wp":b,"np_med":am,"wp_med":bm,"ca_np":round(can,3),"ca_wp":round(caw,3),"d":round(caw-can,3)})
    print(f"{LABEL[m]:17s} {a:8.1f} {b:8.1f} {a-b:6.1f} | med {am:3d}->{bm:3d} | {can:6.3f} {caw:6.3f} {caw-can:+7.3f}")
json.dump({"real_mean":real_mean,"real_median":int(real_words),"rows":rows}, open(EXP/"verbosity.json","w"), indent=1)

# 3. glm-5.2 no-profile: agree-rate by length bin
print("\n=== glm-5.2 NO-profile: agree-rate vs message length ===")
bins=[(0,8),(9,20),(21,40),(41,9999)]
agg=defaultdict(lambda:[0,0])
for pid,p in points.items():
    rm=realm[pid]; gt=gens.get((pid,"glm-5.2","generic")); sm=move_of(p["prev_agent"],gt)
    if not rm or not sm: continue
    w=words(gt)
    for lo,hi in bins:
        if lo<=w<=hi: agg[(lo,hi)][1]+=1; agg[(lo,hi)][0]+= (sm==rm); break
for lo,hi in bins:
    h,t=agg[(lo,hi)]; lab=f"{lo}-{hi if hi<9999 else '+'}"
    print(f"  {lab:8s} words: n={t:3d}  agree={h/t:.3f}" if t else f"  {lab}: n=0")

# 4. confusion matrices
def confusion(m,cond):
    cm=defaultdict(Counter)
    for pid,p in points.items():
        rm=realm[pid]; sm=move_of(p["prev_agent"],gens.get((pid,m,cond),""))
        if rm and sm: cm[rm][sm]+=1
    return cm
def show(title,cm):
    print(f"\n{title}  (rows=REAL move, cols=what the sim said; row-normalized)")
    hdr = "real|sim"
    print(f"  {hdr:12s} "+" ".join(f"{c:>9s}" for c in CATS))
    for rmove in CATS:
        tot=sum(cm[rmove].values()) or 1
        print(f"  {rmove:12s} "+" ".join(f"{cm[rmove][c]/tot:9.2f}" for c in CATS)+f"   (n={sum(cm[rmove].values())})")
show("GLM-5.2 NO profile", confusion("glm-5.2","generic"))
show("GLM-5.2 WITH profile", confusion("glm-5.2","distilled"))
show("GPT-5.5 NO profile", confusion("gpt-5.5","generic"))
show("Claude-Opus-4.8 NO profile", confusion("claude-opus-4.8","generic"))

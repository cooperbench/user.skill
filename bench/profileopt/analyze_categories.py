"""Per-move agree-rate (recall) for ALL 9 models, both conditions, + the profile Δ per category.
agree-rate(move X) = of held-out moments whose REAL move was X, the fraction where the sim also said X.
Writes experiments/condagree_multi/category_recall.json for the website heatmap.
"""
import hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(HERE))
import validate as V, taxonomy as TAX
EXP = HERE / "experiments" / "condagree_multi"
CATS = ["approve", "critical", "directive", "inquiry"]
MODELS = [("deepseek-v3.1","general"),("deepseek-v4-flash","general"),("deepseek-v4-pro","general"),
          ("gpt-5.5","general"),("claude-opus-4.8","general"),("glm-5.2","general"),
          ("gemini-3.1-pro","general"),("osim-4b","specialized"),("osim-8b","specialized")]
LABEL = {"deepseek-v3.1":"DeepSeek-V3.1","deepseek-v4-flash":"DeepSeek-V4-Flash","deepseek-v4-pro":"DeepSeek-V4-Pro",
         "gpt-5.5":"GPT-5.5","claude-opus-4.8":"Claude-Opus-4.8","glm-5.2":"GLM-5.2",
         "gemini-3.1-pro":"Gemini-3.1-Pro","osim-4b":"OSim-4B","osim-8b":"OSim-8B"}

points = {}
for l in (EXP/"points.jsonl").read_text().splitlines():
    if l.strip(): p=json.loads(l); points[p["point_id"]]=p
gens, labels = {}, {}
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
    k="lab:haiku:"+hashlib.sha256((V.truncate_words(prev,120)+"|"+V.truncate_words(text,150)).encode()).hexdigest()[:24]
    return labels.get(k)

realm={pid:move_of(p["prev_agent"],p["real_text"]) for pid,p in points.items()}
realc=Counter(m for m in realm.values() if m); tot=sum(realc.values())
real_freq={c:round(realc[c]/tot,3) for c in CATS}
support={c:realc[c] for c in CATS}

def recall(model,cond):
    rec=defaultdict(lambda:[0,0])
    for pid,p in points.items():
        rm=realm[pid]; sm=move_of(p["prev_agent"],gens.get((pid,model,cond),""))
        if not rm or not sm: continue
        rec[rm][1]+=1
        if sm==rm: rec[rm][0]+=1
    return {c: (round(rec[c][0]/rec[c][1],3) if rec[c][1] else None) for c in CATS}

rows=[]
for mid,kind in MODELS:
    g=recall(mid,"generic"); d=recall(mid,"distilled")
    delta={c: round((d[c] or 0)-(g[c] or 0),3) for c in CATS}
    overall=round(sum((delta[c])*real_freq[c] for c in CATS),3)  # freq-weighted = overall CondAgree Δ (micro)
    rows.append({"id":mid,"label":LABEL[mid],"kind":kind,"overall_d":overall,
                 "generic":g,"distilled":d,"delta":delta})
rows.sort(key=lambda r:-r["overall_d"])
out={"real_freq":real_freq,"support":support,"cats":CATS,"models":rows}
(EXP/"category_recall.json").write_text(json.dumps(out,indent=1))

# print
print("real freq:", real_freq, " support:", support)
print(f"\n{'model':17s} {'overallΔ':>8s} | "+" ".join(f"{c[:4]+'Δ':>8s}" for c in CATS))
for r in rows:
    print(f"{r['label']:17s} {r['overall_d']:+8.3f} | "+" ".join(f"{r['delta'][c]:+8.3f}" for c in CATS))
print(f"\nwrote {EXP/'category_recall.json'}")

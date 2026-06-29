"""Why does the profile help glm-5.2 so much more than other frontier models?
For glm-5.2, gpt-5.5, gemini-3.1-pro, claude-opus-4.8 (+deepseek-v4-pro), compute, per condition:
  - the 4-way move distribution vs the REAL distribution (and total-variation distance to real)
  - per-real-move recall: of moments where the real move was X, how often did the sim also say X
  - avg message length (words)
so we can see WHERE the profile moves each model and why glm gains most.
"""
import hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(HERE))
import validate as V, taxonomy as TAX
EXP = HERE / "experiments" / "condagree_multi"
MODELS = ["glm-5.2", "gpt-5.5", "gemini-3.1-pro", "claude-opus-4.8", "deepseek-v4-pro"]
CATS = ["approve", "critical", "directive", "inquiry"]

points = {}
for l in (EXP / "points.jsonl").read_text().splitlines():
    if l.strip(): p = json.loads(l); points[p["point_id"]] = p
gens, labels = {}, {}
for l in (EXP / "raw.jsonl").read_text().splitlines():
    if not l.strip(): continue
    r = json.loads(l); k = r.get("key", "")
    if r.get("kind") == "gen": gens[(r["point_id"], r["model"], r["cond"])] = r["text"]
    elif k.startswith("lab:"): labels[k] = r.get("move")

def move_of(prev, text):
    if V.is_interrupt(text):
        rest = TAX._strip_interrupt(text)
        if not rest: return "critical"
        text = rest
    if not (text or "").strip() or str(text).startswith("Error:"): return None
    k = "lab:haiku:" + hashlib.sha256((V.truncate_words(prev,120)+"|"+V.truncate_words(text,150)).encode()).hexdigest()[:24]
    return labels.get(k)
def words(t): return len((t or "").split())
def tv(a, b):  # total variation distance between two move dists (dicts over CATS)
    return round(0.5*sum(abs(a.get(c,0)-b.get(c,0)) for c in CATS), 3)
def norm(c):
    tot = sum(c.values()) or 1
    return {k: c.get(k,0)/tot for k in CATS}

# real distribution + per-point real move
realm = {pid: move_of(p["prev_agent"], p["real_text"]) for pid, p in points.items()}
realc = Counter(m for m in realm.values() if m); realn = norm(realc)
print("REAL move dist:", {k: round(realn[k],3) for k in CATS}, "\n")
print(f"{'model':16s} {'cond':9s} | {'approve':>7s} {'critical':>8s} {'directiv':>8s} {'inquiry':>7s} | TV→real | CondAgree | avg_words")
print("-"*100)
results = {}
for model in MODELS:
    for cond in ["generic", "distilled"]:
        sims, hits, n, wlen = {}, 0, 0, []
        rec = defaultdict(lambda: [0,0])  # real_move -> [hit, total]
        sc = Counter()
        for pid, p in points.items():
            rm = realm[pid];  sm = move_of(p["prev_agent"], gens.get((pid, model, cond), ""))
            if not rm or not sm: continue
            n += 1; sc[sm]+=1; wlen.append(words(gens.get((pid,model,cond),"")))
            if sm == rm: hits += 1
            rec[rm][1]+=1
            if sm==rm: rec[rm][0]+=1
        d = norm(sc)
        results[(model,cond)] = {"dist": d, "tv": tv(d, realn), "ca": round(hits/n,3) if n else 0,
                                 "recall": {k: round(rec[k][0]/rec[k][1],3) if rec[k][1] else None for k in CATS},
                                 "words": round(sum(wlen)/len(wlen),1) if wlen else 0, "n": n}
        r = results[(model,cond)]
        print(f"{model:16s} {cond:9s} | {d['approve']:7.2f} {d['critical']:8.2f} {d['directive']:8.2f} {d['inquiry']:7.2f} | {r['tv']:7.3f} | {r['ca']:9.3f} | {r['words']:.0f}")
    print()

print("=== per-real-move RECALL (of moments whose REAL move was X, fraction sim matched) ===")
print(f"{'model':16s} {'cond':9s} | " + " ".join(f"{c:>9s}" for c in CATS))
for model in MODELS:
    for cond in ["generic", "distilled"]:
        rc = results[(model,cond)]["recall"]
        print(f"{model:16s} {cond:9s} | " + " ".join(f"{(rc[c] if rc[c] is not None else 0):9.3f}" for c in CATS))
    # profile effect on each move's recall
    g, dd = results[(model,"generic")]["recall"], results[(model,"distilled")]["recall"]
    delta = {c: round((dd[c] or 0)-(g[c] or 0),3) for c in CATS}
    print(f"{model:16s} {'Δ profile':9s} | " + " ".join(f"{delta[c]:+9.3f}" for c in CATS))
    print()

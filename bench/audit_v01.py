import json, sys
from collections import Counter, defaultdict
sys.path.insert(0, "scripts"); sys.path.insert(0, "bench")
import validate as V, v0

recs = [json.loads(l) for l in open("bench/results/v0_1_raw.jsonl") if l.strip()]
gk = {r["key"]: r for r in recs if r["kind"] == "gen"}
lk = {r["key"]: r for r in recs if r["kind"] == "label"}
print(f"gens {len(gk)}/5000  labels {len(lk)}/5478")

errs = [r for r in gk.values() if V.is_cli_failure(r["text"])]
print("error gens:", len(errs), "| by model:", dict(Counter(r["model"] for r in errs)))
nulllab = [k for k, r in lk.items() if not r.get("move")]
print("null labels:", len(nulllab))

# per-cell valid n (gen ok AND label present)
n_per = Counter()
for k, g in gk.items():
    _, pid, model, cond = k.split("|")
    lab = lk.get(f"label|{model}|{cond}|{pid}", {}).get("move")
    if lab and not V.is_cli_failure(g["text"]):
        n_per[f"{model}/{cond}"] += 1
print("valid n per cell:", dict(sorted(n_per.items())))

# real move-mix for these 10 users (macro)
pts = v0.load_points()  # note: v0.load_points is the OLD 9-user; use the v0_1 points instead
sys.path.insert(0, "bench")
import v0_1
pts = v0_1.load_points(50)
by = {p["point_id"]: p for p in pts}
real = {pid: lk.get(f"label|real|{pid}", {}).get("move") for pid in by}
slug = {pid: by[pid]["slug"] for pid in by}
ptsU = defaultdict(list)
for pid in by: ptsU[slug[pid]].append(pid)
import statistics as st
moves = ["approve_proceed","new_work","refine_redirect","bug_report","pushback","interrupt","question","other"]
mix = {}
for mv in moves:
    per = []
    for u in ptsU:
        rms = [real[p] for p in ptsU[u] if real[p]]
        per.append(sum(1 for m in rms if m == mv) / (len(rms) or 1))
    mix[mv] = round(st.mean(per), 3)
print("REAL macro move-mix (10 users):", json.dumps(mix))
print("real approve%:", round(mix["approve_proceed"], 3),
      "critical%:", round(mix["pushback"] + mix["interrupt"] + mix["bug_report"], 3))

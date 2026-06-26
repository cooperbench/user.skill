"""Emit the final v0.1 (10-user x 50-turn) macro dataset for the website."""
import json, sys, math, hashlib, statistics as st
from collections import Counter, defaultdict
sys.path.insert(0, "scripts"); sys.path.insert(0, "bench")
import validate as V, v0, v0_1

C = {}
for l in open("bench/results/v0_1_raw.jsonl"):
    if l.strip():
        r = json.loads(l); C[r["key"]] = r
pts = v0_1.load_points(50)
by = {p["point_id"]: p for p in pts}
slug = {pid: by[pid]["slug"] for pid in by}
real = {pid: C.get(f"label|real|{pid}", {}).get("move") for pid in by}
ptsU = defaultdict(list)
for pid in by: ptsU[slug[pid]].append(pid)
users = sorted(ptsU)
CRIT = {"pushback", "interrupt", "bug_report"}
MOVES = ["approve_proceed","new_work","refine_redirect","bug_report","pushback","interrupt","question","other"]


def rate(ms, sub):
    n = sum(1 for m in ms if m) or 1
    return sum(1 for m in ms if m in sub) / n


def dice(r, s):
    rc, sc = Counter(r), Counter(s); rn, sn = sum(rc.values()) or 1, sum(sc.values()) or 1
    mv = set(rc) | set(sc)
    ds = [2 * min(rc.get(m, 0)/rn, sc.get(m, 0)/sn) / (rc.get(m, 0)/rn + sc.get(m, 0)/sn) for m in mv if rc.get(m, 0)+sc.get(m, 0) > 0]
    return 100*sum(ds)/len(ds) if ds else None


def agg(xs):
    xs = [x for x in xs if x is not None]
    m = st.mean(xs); s = st.stdev(xs) if len(xs) > 1 else 0
    return [round(m, 3), round(2.262*s/math.sqrt(len(xs)), 3)]  # t_9 95%


def model_cell(model, cond):
    R = defaultdict(list)
    for u in users:
        rms = [real[p] for p in ptsU[u] if real[p]]; sms = []; paired = []
        for pid in ptsU[u]:
            sm = C.get(f"label|{model}|{cond}|{pid}", {}).get("move"); g = C.get(f"gen|{pid}|{model}|{cond}", {})
            if real[pid] and sm and not V.is_cli_failure(g.get("text", "")):
                sms.append(sm); paired.append((real[pid], sm))
        if not sms: continue
        R["moveFid"].append(dice(rms, sms)); R["condAgree"].append(sum(1 for a, b in paired if a == b)/len(paired))
        R["approve"].append(100*rate(sms, {"approve_proceed"})); R["critical"].append(100*rate(sms, CRIT))
    return {k: agg(v) for k, v in R.items()}


def ref_cell(kind):
    R = defaultdict(list)
    for u in users:
        rms = [real[p] for p in ptsU[u] if real[p]]
        if kind == "always_approve":
            sms = ["approve_proceed"]*len(rms)
        else:
            rc = Counter(rms); items = sorted(rc.items()); tot = sum(w for _, w in items); sms = []
            for pid in ptsU[u]:
                if not real[pid]: continue
                h = int(hashlib.sha256(f"{pid}|prior".encode()).hexdigest(), 16); x = h%10000/10000*tot; c = 0
                for mv, w in items:
                    c += w
                    if x <= c: sms.append(mv); break
        paired = list(zip(rms, sms))
        R["moveFid"].append(dice(rms, sms)); R["condAgree"].append(sum(1 for a, b in paired if a == b)/len(paired))
        R["approve"].append(100*rate(sms, {"approve_proceed"})); R["critical"].append(100*rate(sms, CRIT))
    return {k: agg(v) for k, v in R.items()}


# real macro + move-mix + unbiased lucky-guess
realA = agg([100*rate([real[p] for p in ptsU[u] if real[p]], {"approve_proceed"}) for u in users])
realC = agg([100*rate([real[p] for p in ptsU[u] if real[p]], CRIT) for u in users])
mix = {}
for mv in MOVES:
    mix[mv] = round(st.mean([sum(1 for m in [real[p] for p in ptsU[u] if real[p]] if m == mv)/(len([1 for p in ptsU[u] if real[p]]) or 1) for u in users]), 3)
unb = []
for u in users:
    rms = [real[p] for p in ptsU[u] if real[p]]; n = len(rms); rc = Counter(rms)
    s2 = sum((v/n)**2 for v in rc.values())
    if n > 1: unb.append((n*s2 - 1)/(n - 1))
lucky = round(st.mean(unb), 3)

out = {"nUsers": len(users), "nPerUser": 50, "users": users,
       "real": {"approve": realA, "critical": realC, "moveMix": {k: round(v*100, 1) for k, v in mix.items()}},
       "luckyGuess": lucky,
       "cells": {}, "refs": {}}
for m in ["deepseek-v3.1", "gpt-5", "gemini-3.1-pro", "osim-8b", "osim-4b"]:
    for c in ["distilled", "generic"]:
        out["cells"][f"{m}/{c}"] = model_cell(m, c)
out["refs"]["prior_sampler"] = ref_cell("prior")
out["refs"]["always_approve"] = ref_cell("always_approve")
Path = __import__("pathlib").Path
Path("bench/results/site_v01.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))

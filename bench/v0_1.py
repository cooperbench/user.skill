#!/usr/bin/env python3
"""UserSimBench v0.1 — per-user move-fidelity, then macro-aggregate.

Upgrade over v0: 10 users x 50 held-out turns each (round-robin across each user's
held-out sessions), all on the existing clean train/test split (folders were distilled
on train; points come from test -> no leakage). Every metric is computed PER USER, then
averaged across the 10 users (macro), with cross-user std and a 95% CI. Micro (pooled)
is reported alongside for comparison.

Simulators: 3 frontier (OpenRouter) + OSim-4B/8B (Modal), x {distilled, generic}.

Usage: python3 bench/v0_1.py [--limit-users N] [--n-per-user 50]
"""
import argparse
import hashlib
import json
import math
import os
import statistics as st
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "bench"))
import validate as V      # noqa: E402
import v0                 # noqa: E402
import orouter            # noqa: E402
import osim_backend as OB # noqa: E402

RESULTS = ROOT / "bench" / "results"
RAW = RESULTS / "v0_1_raw.jsonl"
SUMMARY = RESULTS / "v0_1_summary.json"

# 10 users: each >=10 total sessions, >=4 held-out sessions, >=50 valid held-out turns.
USERS = ["gtrrz-victor", "alienkevin", "oddessentials", "abiswas-elastio-com", "pc035860",
         "melagiri", "henryph24", "tarasyarema", "khaong", "hutusi"]

FRONTIER = {"deepseek-v3.1": "deepseek/deepseek-chat-v3.1",
            "gpt-5": "openai/gpt-5",
            "gemini-3.1-pro": "google/gemini-3.1-pro-preview"}
OSIM = ["osim-8b", "osim-4b"]
ALL_MODELS = list(FRONTIER) + OSIM
CONDS = ["distilled", "generic"]
CRITICAL = {"pushback", "interrupt", "bug_report"}


def all_points_for(slug):
    """All valid held-out prediction points for a user (uncapped), grouped by session."""
    ho = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
    by_sess = defaultdict(list)
    for s in ho["sessions"]:
        turns = s["turns"]
        for i, t in enumerate(turns):
            if t["role"] != "user" or t.get("is_continuation"):
                continue
            if not V.is_user_action_target(t.get("text")):
                continue
            if not (V.is_interrupt(t.get("text")) or len((t.get("text") or "").split()) >= 3):
                continue
            if not any(p["role"] == "assistant" for p in turns[:i]):
                continue
            ctx = turns[max(0, i - V.CONTEXT_TURNS):i]
            prev_agent = next((p["text"] for p in reversed(ctx) if p["role"] == "assistant"), "")
            by_sess[s["session_id"]].append({
                "slug": slug, "session_id": s["session_id"], "repo": s["repo"],
                "turn_index": i, "real": turns[i]["text"], "context": ctx,
                "prev_agent": prev_agent, "point_id": f"{s['session_id']}#{i}"})
    return by_sess


def sample_points(slug, n):
    """Round-robin across the user's held-out sessions for session-spread coverage."""
    by_sess = all_points_for(slug)
    queues = [list(v) for v in by_sess.values()]
    out = []
    while len(out) < n and any(queues):
        for q in queues:
            if q:
                out.append(q.pop(0))
                if len(out) >= n:
                    break
    return out


def load_points(n_per_user, limit_users=0):
    users = USERS[:limit_users] if limit_users else USERS
    pts = []
    for u in users:
        sp = sample_points(u, n_per_user)
        pts.extend(sp)
        print(f"  {u:22s} {len(sp)} points from {len(set(p['session_id'] for p in sp))} sessions")
    return pts


def gen_message(point, model):
    folder = V.load_folder_text(point["slug"]) if point["_cond"] == "distilled" else ""
    if model in OSIM:
        msgs = OB.build_osim_messages(point, folder, V.truncate_words)
        return OB.chat(model, msgs, max_tokens=500)
    prompt = V.build_prompt(point, folder)
    seed = int(hashlib.sha256(f"{point['point_id']}|{model}|{point['_cond']}".encode()).hexdigest(), 16) % (2**31)
    return v0.clean_msg(orouter.chat(FRONTIER[model], prompt, max_tokens=1000,
                                     temperature=0.7, reasoning_effort="low", seed=seed))


def load_cache():
    c = {}
    if RAW.exists():
        for line in RAW.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                c[r["key"]] = r
    return c


def append(rec):
    with RAW.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---- per-user metrics ----

def dice_movefid(real, sim):
    rc, sc = Counter(real), Counter(sim)
    rn, sn = sum(rc.values()) or 1, sum(sc.values()) or 1
    moves = set(rc) | set(sc)
    ds = [2 * min(rc.get(m, 0) / rn, sc.get(m, 0) / sn) / (rc.get(m, 0) / rn + sc.get(m, 0) / sn)
          for m in moves if (rc.get(m, 0) + sc.get(m, 0)) > 0]
    return 100 * sum(ds) / len(ds) if ds else None


def rate(moves, subset):
    n = sum(1 for m in moves if m) or 1
    return sum(1 for m in moves if m in subset) / n


def sigma_sq(real):
    rc = Counter(m for m in real if m)
    n = sum(rc.values()) or 1
    return sum((v / n) ** 2 for v in rc.values())


def agg(per_user_vals):
    """mean, std, and 95% CI half-width (t_9) across users."""
    xs = [v for v in per_user_vals if v is not None]
    if not xs:
        return {"mean": None}
    m = st.mean(xs)
    s = st.stdev(xs) if len(xs) > 1 else 0.0
    ci = 2.262 * s / math.sqrt(len(xs)) if len(xs) > 1 else 0.0  # t_9, 95%
    return {"mean": round(m, 3), "std": round(s, 3), "ci95": round(ci, 3), "n_users": len(xs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-per-user", type=int, default=50)
    ap.add_argument("--limit-users", type=int, default=0)
    args = ap.parse_args()

    print(f"loading points ({args.n_per_user}/user):")
    points = load_points(args.n_per_user, args.limit_users)
    by_id = {p["point_id"]: p for p in points}
    print(f"TOTAL {len(points)} points\n")

    cache = load_cache()

    # 1. generate (5 models x 2 conds)
    gen_jobs = []
    for p in points:
        for model in ALL_MODELS:
            for cond in CONDS:
                if f"gen|{p['point_id']}|{model}|{cond}" not in cache:
                    gen_jobs.append((p, model, cond))
    print(f"generations to run: {len(gen_jobs)} (cached {len(points)*len(ALL_MODELS)*len(CONDS)-len(gen_jobs)})")

    def run_gen(job):
        p, model, cond = job
        pp = dict(p); pp["_cond"] = cond
        return {"key": f"gen|{p['point_id']}|{model}|{cond}", "kind": "gen",
                "point_id": p["point_id"], "slug": p["slug"], "model": model, "cond": cond,
                "text": gen_message(pp, model)}

    with ThreadPoolExecutor(max_workers=int(os.environ.get("GEN_WORKERS", "12"))) as ex:
        for i, fut in enumerate(as_completed([ex.submit(run_gen, j) for j in gen_jobs]), 1):
            rec = fut.result(); cache[rec["key"]] = rec; append(rec)
            if i % 50 == 0:
                print(f"  gen {i}/{len(gen_jobs)}")

    # 2. label moves (real once per point + each generation)
    lab_jobs = []
    for p in points:
        if f"label|real|{p['point_id']}" not in cache:
            lab_jobs.append(("real", f"label|real|{p['point_id']}", p["real"], p["prev_agent"]))
    for p in points:
        for model in ALL_MODELS:
            for cond in CONDS:
                g = cache.get(f"gen|{p['point_id']}|{model}|{cond}")
                lk = f"label|{model}|{cond}|{p['point_id']}"
                if g and lk not in cache:
                    lab_jobs.append(("gen", lk, g["text"], p["prev_agent"]))
    print(f"labels to run: {len(lab_jobs)}")

    def run_lab(job):
        _, key, text, prev = job
        return {"key": key, "kind": "label", "move": v0.classify_move(text, prev)}

    with ThreadPoolExecutor(max_workers=int(os.environ.get("LAB_WORKERS", "10"))) as ex:
        for i, fut in enumerate(as_completed([ex.submit(run_lab, j) for j in lab_jobs]), 1):
            rec = fut.result(); cache[rec["key"]] = rec; append(rec)
            if i % 100 == 0:
                print(f"  label {i}/{len(lab_jobs)}")

    # 3. per-user metrics -> macro aggregate
    users = sorted(set(p["slug"] for p in points))
    real_move = {pid: cache.get(f"label|real|{pid}", {}).get("move") for pid in by_id}
    pts_by_user = defaultdict(list)
    for pid, p in by_id.items():
        pts_by_user[p["slug"]].append(pid)

    # real reference per user
    real_stats = {}
    for u in users:
        rms = [real_move[pid] for pid in pts_by_user[u] if real_move[pid]]
        real_stats[u] = {"approve": rate(rms, {"approve_proceed"}), "critical": rate(rms, CRITICAL),
                         "sigma2": sigma_sq(rms), "n": len(rms)}
    real_agg = {k: agg([real_stats[u][k] for u in users]) for k in ["approve", "critical", "sigma2"]}

    results = {}
    for model in ALL_MODELS:
        for cond in CONDS:
            per_user = defaultdict(dict)
            for u in users:
                rms, sms, paired = [], [], []
                for pid in pts_by_user[u]:
                    rm = real_move[pid]
                    sm = cache.get(f"label|{model}|{cond}|{pid}", {}).get("move")
                    g = cache.get(f"gen|{pid}|{model}|{cond}", {})
                    if rm:
                        rms.append(rm)
                    if rm and sm and not V.is_cli_failure(g.get("text", "")):
                        sms.append(sm); paired.append((rm, sm))
                if not sms:
                    continue
                per_user[u] = {
                    "MoveFid": dice_movefid(rms, sms),
                    "CondAgree": sum(1 for a, b in paired if a == b) / len(paired) if paired else None,
                    "approve": rate(sms, {"approve_proceed"}),
                    "critical": rate(sms, CRITICAL),
                    "n": len(sms),
                }
            results[f"{model}/{cond}"] = {
                "per_user": per_user,
                "macro": {k: agg([per_user[u].get(k) for u in per_user]) for k in
                          ["MoveFid", "CondAgree", "approve", "critical"]},
                # micro (pooled) for comparison
                "micro": _micro(cache, pts_by_user, real_move, model, cond, users),
            }

    out = {"n_points": len(points), "n_users": len(users), "users": users,
           "n_per_user": args.n_per_user,
           "real_macro": real_agg, "real_per_user": real_stats,
           "lucky_guess_macro": real_agg["sigma2"]["mean"],
           "models": {**FRONTIER, "osim-8b": "cmu-lti/osim-8b", "osim-4b": "cmu-lti/osim-4b"},
           "results": results}
    SUMMARY.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    _print_board(out)
    print(f"\nwrote {SUMMARY}")


def _micro(cache, pts_by_user, real_move, model, cond, users):
    rms, sms, paired = [], [], []
    for u in users:
        for pid in pts_by_user[u]:
            rm = real_move[pid]
            sm = cache.get(f"label|{model}|{cond}|{pid}", {}).get("move")
            g = cache.get(f"gen|{pid}|{model}|{cond}", {})
            if rm:
                rms.append(rm)
            if rm and sm and not V.is_cli_failure(g.get("text", "")):
                sms.append(sm); paired.append((rm, sm))
    return {"MoveFid": round(dice_movefid(rms, sms), 1) if sms else None,
            "CondAgree": round(sum(1 for a, b in paired if a == b) / len(paired), 3) if paired else None,
            "approve": round(rate(sms, {"approve_proceed"}), 3),
            "critical": round(rate(sms, CRITICAL), 3)}


def _print_board(out):
    rm = out["real_macro"]
    print(f"\nreal (macro over {out['n_users']} users): approve={rm['approve']['mean']}±{rm['approve']['ci95']}  "
          f"critical={rm['critical']['mean']}±{rm['critical']['ci95']}  lucky-guess={out['lucky_guess_macro']}\n")
    hdr = f"{'simulator':26s} {'MoveFid':>13} {'CondAgree':>15} {'approve':>14} {'critical':>14}"
    print(hdr); print("-" * len(hdr))

    def cell(d):
        return f"{d['mean']}±{d['ci95']}" if d.get("mean") is not None else "-"
    order = [f"{m}/{c}" for c in ["distilled", "generic"] for m in ALL_MODELS]
    for k in order:
        ma = out["results"][k]["macro"]
        print(f"{k:26s} {cell(ma['MoveFid']):>13} {cell(ma['CondAgree']):>15} "
              f"{cell(ma['approve']):>14} {cell(ma['critical']):>14}")


if __name__ == "__main__":
    main()

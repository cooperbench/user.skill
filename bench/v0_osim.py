#!/usr/bin/env python3
"""Run the OdysSim OSim-4B / OSim-8B simulators through the v0 move-fidelity eval
(same 54 points, same move classifier, same metrics) and merge into the leaderboard.

OSim uses its native role-swapped format (bench/osim_backend.py). Reuses everything
else from v0.py so the numbers are directly comparable to the frontier models.

Usage: python3 bench/v0_osim.py [--limit N]
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "bench"))
import validate as V          # noqa: E402
import v0                     # noqa: E402  (load_points, classify_move, score_block, dist, ...)
import osim_backend as OB     # noqa: E402

RESULTS = ROOT / "bench" / "results"
RAW = RESULTS / "v0_osim_raw.jsonl"
FRONTIER_RAW = RESULTS / "v0_raw.jsonl"
COMBINED = RESULTS / "v0_with_osim_summary.json"
MODELS = ["osim-8b", "osim-4b"]
CONDS = ["distilled", "generic"]


def load_cache(path):
    c = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                c[r["key"]] = r
    return c


def append(path, rec):
    with path.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    points = v0.load_points()
    if args.limit:
        points = points[:args.limit]
    by_id = {p["point_id"]: p for p in points}
    print(f"{len(points)} points")

    # real move labels: reuse the frontier run's labels for identical ground truth
    fcache = load_cache(FRONTIER_RAW)
    real_move = {pid: fcache.get(f"label|real|{pid}", {}).get("move") for pid in by_id}
    missing_real = [pid for pid in by_id if not real_move[pid]]
    if missing_real:
        print(f"labeling {len(missing_real)} missing real moves...")
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = {ex.submit(v0.classify_move, by_id[pid]["real"], by_id[pid]["prev_agent"]): pid for pid in missing_real}
            for fut in as_completed(futs):
                real_move[futs[fut]] = fut.result()

    cache = load_cache(RAW)

    # 1. generate (OSim native format)
    gen_jobs = [(p, m, c) for p in points for m in MODELS for c in CONDS
                if f"gen|{p['point_id']}|{m}|{c}" not in cache]
    print(f"generations to run: {len(gen_jobs)}")

    def run_gen(job):
        p, m, c = job
        folder = V.load_folder_text(p["slug"]) if c == "distilled" else ""
        msgs = OB.build_osim_messages(p, folder, V.truncate_words)
        txt = OB.chat(m, msgs)
        return {"key": f"gen|{p['point_id']}|{m}|{c}", "kind": "gen",
                "point_id": p["point_id"], "slug": p["slug"], "model": m, "cond": c, "text": txt}

    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, fut in enumerate(as_completed([ex.submit(run_gen, j) for j in gen_jobs]), 1):
            rec = fut.result(); cache[rec["key"]] = rec; append(RAW, rec)
            if i % 20 == 0:
                print(f"  gen {i}/{len(gen_jobs)}")

    # 2. label moves
    lab_jobs = []
    for p in points:
        for m in MODELS:
            for c in CONDS:
                g = cache.get(f"gen|{p['point_id']}|{m}|{c}")
                lk = f"label|{m}|{c}|{p['point_id']}"
                if g and lk not in cache:
                    lab_jobs.append((lk, g["text"], p["prev_agent"]))
    print(f"labels to run: {len(lab_jobs)}")

    def run_lab(job):
        lk, text, prev = job
        return {"key": lk, "kind": "label", "move": v0.classify_move(text, prev)}

    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, fut in enumerate(as_completed([ex.submit(run_lab, j) for j in lab_jobs]), 1):
            rec = fut.result(); cache[rec["key"]] = rec; append(RAW, rec)
            if i % 30 == 0:
                print(f"  label {i}/{len(lab_jobs)}")

    # 3. metrics (same machinery as v0)
    valid = [pid for pid in by_id if real_move[pid]]
    real_moves = [real_move[pid] for pid in valid]
    osim_results = {}
    for m in MODELS:
        for c in CONDS:
            sim, paired = [], []
            for pid in valid:
                sm = cache.get(f"label|{m}|{c}|{pid}", {}).get("move")
                gt = cache.get(f"gen|{pid}|{m}|{c}", {})
                if sm and not V.is_cli_failure(gt.get("text", "")):
                    sim.append(sm); paired.append((real_move[pid], sm))
            osim_results[f"{m}/{c}"] = v0.score_block(real_moves, sim, paired)

    # 4. merge with frontier summary + print combined leaderboard
    front = json.loads((RESULTS / "v0_summary.json").read_text())
    combined = dict(front)
    combined["results"] = {**front["results"], **osim_results}
    COMBINED.write_text(json.dumps(combined, indent=1, ensure_ascii=False))

    real_appr, real_crit = front["real_approve%"], front["real_critical%"]
    ceil = front["condagree_marginal_ceiling"]
    print(f"\nreal: approve%={real_appr} critical%={real_crit}  Σp²={ceil}\n")
    hdr = f"{'simulator':26s} {'MoveFid':>7} {'CondAgr':>7} {'appr%':>6} {'crit%':>6} {'n':>4}"
    print(hdr); print("-" * len(hdr))
    order = ([f"{m}/{c}" for m in MODELS for c in CONDS] +
             ["deepseek-v3.1/distilled", "gpt-5/distilled", "gemini-3.1-pro/distilled",
              "deepseek-v3.1/generic", "gpt-5/generic", "gemini-3.1-pro/generic",
              "[ref] prior_sampler"])
    for k in order:
        r = combined["results"].get(k)
        if not r:
            continue
        tag = "  <- OSim" if k.startswith("osim") else ""
        print(f"{k:26s} {str(r['MoveFid']):>7} {str(r['CondAgree']):>7} "
              f"{str(r['approve%']):>6} {str(r['critical%']):>6} {r['n']:>4}{tag}")
    print(f"\nwrote {COMBINED}")


if __name__ == "__main__":
    main()

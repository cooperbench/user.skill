#!/usr/bin/env python3
"""Aggregate a Harbor SWESimBench-v2 agentic job into eval_agentic_report.json.

Reads each trial's verifier/verdict.json (preferred) or falls back to
result.json -> verifier_result.rewards.reward + trial.log. Maps trial -> (dev, point_id)
via the dataset _manifest.json. Computes per-point match, per-dev move-match accuracy,
macro-over-developer accuracy, chance line (0.489), lift, and a bootstrap CI over developers.

Usage: aggregate_agentic.py <job_dir> <dataset_dir> [--out eval_agentic_report.json] [--chance 0.489]
"""
import json, os, re, sys, argparse, random, glob, statistics

def load_verdict(trial_dir):
    """Return (predicted_msg, pred_move, gold_move, match, reward) from a trial dir."""
    vj = os.path.join(trial_dir, "verifier", "verdict.json")
    if os.path.exists(vj):
        try:
            d = json.load(open(vj))
            return d.get("predicted_msg", ""), d.get("pred_move"), d.get("gold_move"), \
                   bool(d.get("match")), d.get("reward")
        except Exception:
            pass
    # fallback: parse verifier stdout for the pred/gold line
    pred_move = gold_move = None
    match = None
    reward = None
    rj = os.path.join(trial_dir, "result.json")
    if os.path.exists(rj):
        try:
            r = json.load(open(rj))
            reward = ((r.get("verifier_result") or {}).get("rewards") or {}).get("reward")
        except Exception:
            pass
    for cand in (os.path.join(trial_dir, "verifier", "verify.log"),
                 os.path.join(trial_dir, "verifier", "test-stdout.txt")):
        if os.path.exists(cand):
            txt = open(cand, errors="ignore").read()
            m = re.search(r"pred_move=(\w+|None) gold_move=(\w+|None) match=(\w+)", txt)
            if m:
                pred_move = None if m.group(1) == "None" else m.group(1)
                gold_move = None if m.group(2) == "None" else m.group(2)
                match = (m.group(3) == "True")
            break
    if reward is not None and match is None:
        match = reward >= 0.5
    return "", pred_move, gold_move, match, reward

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_dir")
    ap.add_argument("dataset_dir")
    ap.add_argument("--out", default="/data/swesimbench-v2-harbor/eval_agentic_report.json")
    ap.add_argument("--chance", type=float, required=True,
                    help="chance line recomputed from this exact cohort/policy")
    ap.add_argument("--condition", default="noprofile")
    a = ap.parse_args()

    dataset_meta = json.load(open(os.path.join(a.dataset_dir, "_cohort_meta.json")))
    clean_meta = json.load(open("/data/swesimbench-v2-harbor/clean_manifest.json"))
    if dataset_meta.get("cohort_fingerprint") != clean_meta.get("cohort_fingerprint"):
        raise RuntimeError("dataset was built from a stale cohort")
    if dataset_meta.get("policy_fingerprint") != clean_meta.get("policy_fingerprint"):
        raise RuntimeError("dataset was built under a stale cohort policy")
    manifest = json.load(open(os.path.join(a.dataset_dir, "_manifest.json")))
    # task -> (dev, point_id)
    tmap = {x["task"]: (x["dev"], x["point_id"]) for x in manifest}

    per_point = []
    for trial_dir in sorted(glob.glob(os.path.join(a.job_dir, "*__*"))):
        if not os.path.isdir(trial_dir):
            continue
        base = os.path.basename(trial_dir)
        # trial name = <task>__<trialhash>; strip the last __token
        task = base.rsplit("__", 1)[0]
        if task not in tmap:
            # try without trailing trial suffix variations
            continue
        dev, point_id = tmap[task]
        pred_msg, pred_move, gold_move, match, reward = load_verdict(trial_dir)
        per_point.append({
            "point_id": point_id, "dev": dev, "task": task,
            "predicted_msg": pred_msg, "pred_move": pred_move,
            "gold_move": gold_move,
            "match": (bool(match) if (pred_move and gold_move) else None),
            "reward": reward,
        })

    # scorable points = both moves present
    scored = [p for p in per_point if p["match"] is not None]

    # per-dev accuracy (over that dev's scorable points)
    by_dev = {}
    for p in scored:
        by_dev.setdefault(p["dev"], []).append(1 if p["match"] else 0)
    per_dev_acc = {d: (sum(v) / len(v)) for d, v in by_dev.items() if v}

    macro = statistics.mean(per_dev_acc.values()) if per_dev_acc else 0.0
    micro = (sum(1 for p in scored if p["match"]) / len(scored)) if scored else 0.0

    # bootstrap CI over developers (resample devs with replacement, macro each time)
    devs = list(per_dev_acc.keys())
    boot = []
    if devs:
        rng = random.Random(1234)
        for _ in range(5000):
            sample = [per_dev_acc[rng.choice(devs)] for _ in devs]
            boot.append(statistics.mean(sample))
        boot.sort()
        ci_lo = boot[int(0.025 * len(boot))]
        ci_hi = boot[int(0.975 * len(boot))]
    else:
        ci_lo = ci_hi = 0.0

    between_dev_sd = statistics.pstdev(list(per_dev_acc.values())) if len(per_dev_acc) > 1 else 0.0

    report = {
        "condition": a.condition,
        "judge": "gemini-3.5-flash (pinned gemini-3.1-pro-preview was 429-quota'd)",
        "generator_agent": "mini-swe-agent==2.4.5",
        "generator_model": "gemini/gemini-3.5-flash",
        "environment": "docker",
        "n_devs_with_scored_points": len(per_dev_acc),
        "n_points_total": len(per_point),
        "n_points_scored": len(scored),
        "chance": a.chance,
        "macro_move_match_accuracy": round(macro, 4),
        "micro_move_match_accuracy": round(micro, 4),
        "lift_vs_chance": round(macro - a.chance, 4),
        "bootstrap_ci95_macro": [round(ci_lo, 4), round(ci_hi, 4)],
        "between_dev_sd": round(between_dev_sd, 4),
        "per_dev_accuracy": {d: round(v, 4) for d, v in sorted(per_dev_acc.items())},
        "per_point": per_point,
    }
    json.dump(report, open(a.out, "w"), indent=1)
    # console summary
    print(f"== SWESimBench v2 agentic ({a.condition}) ==")
    print(f"points: {len(per_point)} total, {len(scored)} scored; devs scored: {len(per_dev_acc)}")
    print(f"MACRO move-match accuracy: {macro:.4f}  (micro {micro:.4f})")
    print(f"chance: {a.chance:.3f}   lift: {macro - a.chance:+.4f}")
    print(f"bootstrap 95% CI (macro over devs): [{ci_lo:.4f}, {ci_hi:.4f}]  between-dev SD {between_dev_sd:.4f}")
    print(f"-> {a.out}")

if __name__ == "__main__":
    main()

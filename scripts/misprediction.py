#!/usr/bin/env python3
"""Misprediction analysis — is the user-simulator's error *homogeneity*?

Tests whether the simulator's mispredictions reflect a task-completion default that ignores
individual differences, rather than a per-user model. Operationalised on the 4-way move taxonomy
(approve / critical / directive / inquiry; 7-way record labels are folded via taxonomy.OLD_TO_NEW):

  H1 (secondary, prompt-sensitive)  central attractor / marginal skew          -> E2
  H2 (primary)                      between-user variance collapse             -> E3
  H3 (primary)                      regression to the population-median dev     -> E4
  plus                              decision-vs-surface across conditions       -> E5
  plus                              per-turn worst-K audit (+ optional LLM)     -> E1

Reads the records in one or more results/validation_results*.json files (any run of validate.py
that labelled real_act/pred_act). E2-E5 are pure offline computation; E1's adjudication is gated
behind --adjudicate (needs the `claude` CLI). Deterministic (fixed seed) so reruns match.

Usage:
  python3 scripts/misprediction.py                                   # both full-cohort files
  python3 scripts/misprediction.py --results results/folder_v5samp_9users.json
  python3 scripts/misprediction.py --adjudicate --topk 25 --judge-model claude-sonnet-5
"""

import argparse
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bench" / "profileopt"))
import taxonomy as TAX  # noqa: E402  (OLD_TO_NEW, CATEGORIES)

CATS = TAX.CATEGORIES                      # ["approve","critical","directive","inquiry"]
CAT_OF = dict(TAX.OLD_TO_NEW)              # 7-way -> 4-way; "other" -> None
CAT_OF.update({c: c for c in CATS})        # 4-way labels map to themselves (schema-agnostic)
TASK_CATS = {"approve", "directive"}       # "keep the task moving" moves
HUMAN_CATS = {"critical", "inquiry"}       # friction / individual-texture moves
CONDS = ["distilled", "generic", "wrong"]
SEED = 0


def cat(act):
    """Fold a raw move label into one of the 4 canonical categories (None if unmappable)."""
    return CAT_OF.get(act) if act else None


# ---------- distribution helpers ----------

def mix(labels):
    """Normalised 4-vector over CATS from an iterable of raw act labels (unmappable dropped)."""
    c = Counter(x for x in (cat(a) for a in labels) if x)
    tot = sum(c.values())
    return [c[k] / tot for k in CATS] if tot else None


def tvd(p, q):
    """Total variation distance between two 4-vectors."""
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


def mean_vec(vecs):
    n = len(vecs)
    return [sum(v[i] for v in vecs) / n for i in range(len(CATS))] if n else None


def mean_pairwise_tvd(vecs):
    """Average TVD over all unordered user pairs — a scalar 'spread' of a set of mixes."""
    ds = [tvd(vecs[i], vecs[j]) for i in range(len(vecs)) for j in range(i + 1, len(vecs))]
    return sum(ds) / len(ds) if ds else None


# ---------- per-user mixes ----------

def per_user_mixes(records, cond):
    """{slug: (real_mix, pred_mix)} for a condition, keeping only users with >=MIN real & pred
    labelled points so a mix is meaningful. real_act is identical across conditions but we read it
    from this condition's rows for alignment."""
    MIN = 3
    real_by, pred_by = defaultdict(list), defaultdict(list)
    for r in records:
        if r.get("cond") != cond:
            continue
        if r.get("real_act"):
            real_by[r["slug"]].append(r["real_act"])
        if r.get("pred_act"):
            pred_by[r["slug"]].append(r["pred_act"])
    out = {}
    for s in real_by:
        rm, pm = mix(real_by[s]), mix(pred_by.get(s, []))
        if rm and pm and len(real_by[s]) >= MIN and len(pred_by.get(s, [])) >= MIN:
            out[s] = (rm, pm)
    return out


# ---------- significance (no scipy) ----------

def sign_test(k, n):
    """Two-sided exact binomial p for k successes of n at p=0.5."""
    if n == 0:
        return 1.0
    def C(n, r):
        return math.comb(n, r)
    tail = sum(C(n, i) for i in range(0, min(k, n - k) + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def paired_perm_test(pairs, stat, iters=10000):
    """Two-sided permutation p that stat(a-list) != stat(b-list) under random per-item swaps.
    `pairs` = list of (a, b); `stat` maps a list -> scalar. Used for spread(pred) vs spread(real)."""
    rng = random.Random(SEED)
    a = [x for x, _ in pairs]
    b = [y for _, y in pairs]
    obs = stat(a) - stat(b)
    hits = 0
    for _ in range(iters):
        sa, sb = [], []
        for x, y in pairs:
            if rng.random() < 0.5:
                sa.append(x); sb.append(y)
            else:
                sa.append(y); sb.append(x)
        if abs(stat(sa) - stat(sb)) >= abs(obs) - 1e-12:
            hits += 1
    return obs, (hits + 1) / (iters + 1)


def wilcoxon(diffs):
    """Two-sided Wilcoxon signed-rank p via normal approx (ties-averaged ranks)."""
    d = [x for x in diffs if abs(x) > 1e-12]
    n = len(d)
    if n < 6:
        return None
    order = sorted(range(n), key=lambda i: abs(d[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(d[order[j + 1]]) == abs(d[order[i]]):
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    w = sum(r for r, x in zip(ranks, d) if x > 0)
    mu = n * (n + 1) / 4
    sd = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    if sd == 0:
        return None
    z = (w - mu) / sd
    return math.erfc(abs(z) / math.sqrt(2))


# ---------- experiments ----------

def skill_score(acc, acc_baseline):
    """Normalised accuracy (a skill score):  S = (acc - acc_base) / (1 - acc_base).

    0   = exactly as good as always predicting the majority class
    1   = perfect
    < 0 = worse than the majority-class predictor

    Same construction as Cohen's kappa and the Murphy/Brier skill score, with the
    majority-class rate as the reference instead of chance agreement. Reported on a 0-100
    scale. This is the comparable number: raw accuracy cannot be compared across cohorts
    with different class balance (folder's baseline is .506, inline's is .512), but skill
    is normalised by each cohort's own baseline."""
    denom = 1.0 - acc_baseline
    return None if denom <= 0 else (acc - acc_baseline) / denom


def a_move_accuracy(records):
    """Metric A — individual-level accuracy: how often the predicted move equals the real move,
    per condition, plus the normalised skill score against the majority-class baseline (always
    predict the most common real move). The move distribution is heavily skewed toward
    `directive`, so raw accuracy flatters the model; skill is the honest headline."""
    labelled = [r for r in records if r.get("real_act") and r.get("pred_act")]
    reals = [cat(r["real_act"]) for r in labelled if cat(r["real_act"])]
    if not reals:
        return None
    top, top_n = Counter(reals).most_common(1)[0]
    base = top_n / len(reals)
    out = {"baseline_class": top, "baseline_accuracy": round(base, 3),
           "skill_definition": "S = (acc - acc_baseline) / (1 - acc_baseline), x100; "
                               "0 = majority-class predictor, 100 = perfect, negative = worse",
           "by_condition": {}}
    for cond in CONDS:
        rows = [r for r in labelled if r.get("cond") == cond]
        if not rows:
            continue
        hit = sum(1 for r in rows if cat(r["real_act"]) and cat(r["real_act"]) == cat(r["pred_act"]))
        acc = hit / len(rows)
        s = skill_score(acc, base)
        out["by_condition"][cond] = {
            "n": len(rows), "accuracy": round(acc, 3),
            "vs_baseline": round(acc - base, 3),
            "skill": round(100 * s, 1) if s is not None else None,
            "beats_baseline": acc > base,
        }
    return out


def e2_marginal_confusion(records):
    """H1 (descriptive): marginal skew + net flow between task and human categories."""
    reals = [cat(r["real_act"]) for r in records if r.get("cond") == "distilled" and r.get("real_act")]
    out = {}
    for cond in CONDS:
        rows = [r for r in records if r.get("cond") == cond and r.get("real_act") and r.get("pred_act")]
        real_m = mix([r["real_act"] for r in rows])
        pred_m = mix([r["pred_act"] for r in rows])
        if not real_m or not pred_m:
            continue
        # net flow among *mismatched* points: human->task vs task->human
        h2t = t2h = 0
        for r in rows:
            rc, pc = cat(r["real_act"]), cat(r["pred_act"])
            if not rc or not pc or rc == pc:
                continue
            if rc in HUMAN_CATS and pc in TASK_CATS:
                h2t += 1
            elif rc in TASK_CATS and pc in HUMAN_CATS:
                t2h += 1
        out[cond] = {
            "n": len(rows),
            "real_marginal": {c: round(v, 3) for c, v in zip(CATS, real_m)},
            "pred_marginal": {c: round(v, 3) for c, v in zip(CATS, pred_m)},
            "pred_minus_real": {c: round(p - q, 3) for c, p, q in zip(CATS, pred_m, real_m)},
            "human->task": h2t, "task->human": t2h,
            "flow_sign_test_p": round(sign_test(min(h2t, t2h), h2t + t2h), 4),
            "net_toward_task": h2t - t2h,
        }
    return {"note": "direction is prompt-sensitive; clean approve-collapse test is E7 low-prompt arm",
            "by_condition": out,
            "real_act_marginal_all": {c: round(v, 3) for c, v in zip(CATS, mix(reals))} if reals else None}


def e3_variance_collapse(records):
    """H2 (primary): between-user spread of predicted vs real mixes."""
    out = {}
    for cond in CONDS:
        um = per_user_mixes(records, cond)
        if len(um) < 3:
            out[cond] = {"n_users": len(um), "note": "too few users with labelled data"}
            continue
        reals = [rm for rm, _ in um.values()]
        preds = [pm for _, pm in um.values()]
        obs, p = paired_perm_test(list(zip(preds, reals)), mean_pairwise_tvd)
        out[cond] = {
            "n_users": len(um),
            "spread_real": round(mean_pairwise_tvd(reals), 4),
            "spread_pred": round(mean_pairwise_tvd(preds), 4),
            "pred_minus_real": round(obs, 4),
            "perm_p": round(p, 4),
            "collapse": obs < 0,
        }
    return {"hypothesis": "spread_pred < spread_real (predictions cluster across users)", "by_condition": out}


def e4_median_regression(records):
    """H3 (primary): is each user's predicted mix closer to the population mean than their real mix?"""
    out = {}
    for cond in CONDS:
        um = per_user_mixes(records, cond)
        if len(um) < 6:
            out[cond] = {"n_users": len(um), "note": "too few users for signed-rank"}
            continue
        pbar = mean_vec([rm for rm, _ in um.values()])   # population-average developer (from real)
        d_real = {s: tvd(rm, pbar) for s, (rm, _) in um.items()}
        d_pred = {s: tvd(pm, pbar) for s, (_, pm) in um.items()}
        diffs = [d_pred[s] - d_real[s] for s in um]      # <0 => pred shrinks toward median
        out[cond] = {
            "n_users": len(um),
            "mean_dist_to_median_real": round(sum(d_real.values()) / len(um), 4),
            "mean_dist_to_median_pred": round(sum(d_pred.values()) / len(um), 4),
            "mean_pred_minus_real": round(sum(diffs) / len(um), 4),
            "n_users_shrinking": sum(1 for x in diffs if x < 0),
            "wilcoxon_p": round(wilcoxon(diffs), 4) if wilcoxon(diffs) is not None else None,
            "shrinks_to_median": sum(diffs) / len(um) < 0,
        }
    return {"hypothesis": "pred closer to population median than real (shrinkage)", "by_condition": out}


def entropy(p):
    """Shannon entropy (bits) of a move mix — how spread out one developer's own behaviour is.
    0 = always the same move, 2.0 = perfectly even across the four categories."""
    return -sum(x * math.log2(x) for x in p if x > 0)


def e8_within_developer_spread(records):
    """H4 / E8 — WITHIN-developer spread: is a single developer's predicted behaviour less varied
    than their real behaviour? Distinct from E3, which compares developers to each other. The
    hypothesis predicts the simulator renders each person as a narrower, more one-note version of
    themselves (caricature), so entropy(pred) < entropy(real)."""
    out = {"unit": "bits (max 2.0 over four move categories)", "by_condition": {}}
    for cond in CONDS:
        um = per_user_mixes(records, cond)
        if len(um) < 6:
            continue
        er = {s: entropy(rm) for s, (rm, _) in um.items()}
        ep = {s: entropy(pm) for s, (_, pm) in um.items()}
        diffs = [ep[s] - er[s] for s in um]
        n_narrow = sum(1 for d in diffs if d < 0)
        p = wilcoxon(diffs)
        out["by_condition"][cond] = {
            "n_users": len(um),
            "entropy_real": round(sum(er.values()) / len(er), 3),
            "entropy_pred": round(sum(ep.values()) / len(ep), 3),
            "mean_delta": round(sum(diffs) / len(diffs), 3),
            "n_narrower": n_narrow,
            "wilcoxon_p": round(p, 4) if p is not None else None,
            "narrower": sum(diffs) / len(diffs) < 0,
        }
    return out


def per_user_detail(records):
    """Per-developer values behind E3/E4, so figures can show the actual spread rather than
    a single summary bar: each user's real/predicted mix and their distance to the population
    centroid (the 'average developer' built from the real mixes)."""
    out = {}
    for cond in CONDS:
        um = per_user_mixes(records, cond)
        if len(um) < 3:
            continue
        # real centroid (the "average developer") and the predicted set's own centroid.
        # E4 measures distance to the REAL centroid; E3 (spread) measures how far each mix sits
        # from its OWN group's centroid — using the real centroid for both would conflate them.
        pbar = mean_vec([rm for rm, _ in um.values()])
        qbar = mean_vec([pm for _, pm in um.values()])
        out[cond] = {
            "centroid": [round(x, 4) for x in pbar],
            "pred_centroid": [round(x, 4) for x in qbar],
            "centroid_shift": round(tvd(qbar, pbar), 4),  # how far the model's attractor sits from the human mean
            "users": {s: {"real_mix": [round(x, 4) for x in rm],
                          "pred_mix": [round(x, 4) for x in pm],
                          "d_real": round(tvd(rm, pbar), 4),      # E4: real -> real centroid
                          "d_pred": round(tvd(pm, pbar), 4),      # E4: pred -> real centroid
                          "s_real": round(tvd(rm, pbar), 4),      # E3: real -> own (real) centroid
                          "s_pred": round(tvd(pm, qbar), 4),      # E3: pred -> own (pred) centroid
                          "d_self": round(tvd(pm, rm), 4)}
                      for s, (rm, pm) in sorted(um.items())},
        }
    return out


def e5_decision_vs_surface(records, meta):
    """Does individuation change the DECISION (move mix) or only the SURFACE (style)?
    Move-distance = mean over users of TVD(pred_u, real_u). Style = judge_style from summary."""
    summary = meta.get("summary", {})
    out = {}
    for cond in CONDS:
        um = per_user_mixes(records, cond)
        move_d = (sum(tvd(pm, rm) for rm, pm in um.values()) / len(um)) if um else None
        srow = summary.get(cond, {})
        out[cond] = {
            "n_users": len(um),
            "move_dist_to_real": round(move_d, 4) if move_d is not None else None,
            "judge_style": srow.get("judge_style"),
            "judge_realism": srow.get("judge_realism"),
            "judge_content": srow.get("judge_content"),
        }
    d, g, w = out.get("distilled", {}), out.get("generic", {}), out.get("wrong", {})
    verdict = None
    if all(x.get("move_dist_to_real") is not None for x in (d, g, w)):
        move_gap = g["move_dist_to_real"] - d["move_dist_to_real"]   # >0 => folder moves DECISION toward user
        style_gap = ((d.get("judge_style") or 0) - (g.get("judge_style") or 0))
        verdict = ("surface_only" if move_gap <= 0.02 and style_gap > 1 else
                   "decision_shift" if move_gap > 0.02 else "flat")
    return {"by_condition": out,
            "verdict": verdict,
            "reading": "surface_only = folder changes style but not move choice (supports homogeneity); "
                       "decision_shift = folder moves the actual decision toward the user"}


SEVERITY_HELP = "severity = cat_mismatch(1) + (100 - realism_or_content)/100, ranked desc"


def e1_worst_k(records, topk):
    """Rank the worst mispredictions for audit (distilled condition — the product claim)."""
    rows = [r for r in records if r.get("cond") == "distilled" and r.get("real_act") and r.get("pred_act")]
    def sev(r):
        rc, pc = cat(r["real_act"]), cat(r["pred_act"])
        mism = 0 if (rc and pc and rc == pc) else 1
        q = r.get("judge_realism")
        if q is None:
            q = r.get("judge_content")
        return mism + (100 - (q if q is not None else 50)) / 100
    ranked = sorted(rows, key=sev, reverse=True)[:topk]
    return [{
        "slug": r["slug"], "point_id": r["point_id"], "repo": r.get("repo"),
        "real_cat": cat(r["real_act"]), "pred_cat": cat(r["pred_act"]),
        "real_act": r["real_act"], "pred_act": r["pred_act"],
        "judge_realism": r.get("judge_realism"), "judge_content": r.get("judge_content"),
        "real": r.get("real", ""), "generated": r.get("generated", ""),
        "severity": round(sev(r), 3),
    } for r in ranked]


ADJUDICATE_PROMPT = (
    "A user-simulator predicted a developer's NEXT message to an AI coding agent, but the real "
    "developer said something else.\n\n"
    "REAL message: {real}\n\nPREDICTED message: {pred}\n\n"
    "REAL move category: {real_cat}    PREDICTED move category: {pred_cat}\n\n"
    "Answer two questions about the PREDICTION:\n"
    "1. reasonable: could SOME competent developer plausibly have sent the predicted message here? "
    "(true/false)\n"
    "2. error_type: pick ONE — "
    "'task_completion_substitution' (predicted a keep-going/approve/new-task move where the real "
    "developer pushed back, interrupted, or redirected), "
    "'generic_not_specific' (right kind of move, but not how THIS developer would do it), "
    "'hallucinated_content' (invents facts/requests not grounded in the session), "
    "'underdetermined' (both are equally plausible; the real message was unpredictable), "
    "'other'.\n"
    'Respond with ONLY JSON: {{"reasonable": <bool>, "error_type": "<one>"}}'
)


def adjudicate(worst, judge_model, parallel):
    """Optional: LLM-adjudicate each worst-K miss (reasonableness + error type)."""
    import re
    from concurrent.futures import ThreadPoolExecutor, as_completed
    sys.path.insert(0, str(ROOT / "scripts"))
    import validate as V

    def one(item):
        prompt = ADJUDICATE_PROMPT.format(
            real=V.truncate_words(item["real"], 200), pred=V.truncate_words(item["generated"], 200),
            real_cat=item["real_cat"], pred_cat=item["pred_cat"])
        out = V.run_claude(prompt, judge_model, timeout=120)
        m = re.search(r'\{[^{}]*"error_type"[^{}]*\}', out)
        if not m:
            return {**item, "reasonable": None, "error_type": None}
        try:
            d = json.loads(m.group(0))
            return {**item, "reasonable": bool(d.get("reasonable")), "error_type": d.get("error_type")}
        except (ValueError, TypeError):
            return {**item, "reasonable": None, "error_type": None}

    results = []
    with ThreadPoolExecutor(max_workers=parallel) as ex:
        for fut in as_completed([ex.submit(one, it) for it in worst]):
            results.append(fut.result())
    adjud = [r for r in results if r.get("error_type")]
    summary = dict(Counter(r["error_type"] for r in adjud))
    reasonable = sum(1 for r in adjud if r.get("reasonable"))
    homog = summary.get("task_completion_substitution", 0) + summary.get("generic_not_specific", 0)
    return results, {
        "n_adjudicated": len(adjud),
        "reasonable_rate": round(reasonable / len(adjud), 3) if adjud else None,
        "error_type_counts": summary,
        "homogeneity_share": round(homog / len(adjud), 3) if adjud else None,
        "reading": "high reasonable_rate + high homogeneity_share = misses are 'plausible in general, "
                   "wrong for this person' (supports the hypothesis)",
    }


# ---------- driver ----------

def load(paths):
    """Merge records from multiple result files; keep first file's meta (summary etc.)."""
    records, meta, sources = [], {}, []
    for p in paths:
        p = Path(p)
        if not p.exists():
            print(f"skip (missing): {p}")
            continue
        d = json.loads(p.read_text())
        recs = d.get("records", [])
        # drop generations that are CLI/transport error strings, not model text (they otherwise
        # dominate the worst-K audit and skew move distributions). Uses the shared filter.
        import validate as _V
        n_raw = len(recs)
        recs = [r for r in recs if not _V.is_cli_failure(r.get("generated", ""))]
        dropped = n_raw - len(recs)
        labelled = sum(1 for r in recs if r.get("real_act") and r.get("pred_act"))
        print(f"loaded {p.name}: {len(recs)} records ({dropped} CLI-failures dropped), "
              f"{labelled} move-labelled  (mode={d.get('mode')})")
        for r in recs:
            r.setdefault("_src", p.name)
        records += recs
        sources.append({"file": p.name, "mode": d.get("mode"), "n": len(recs), "labelled": labelled})
        if not meta:
            meta = {"summary": d.get("summary", {})}
    return records, meta, sources


def main():
    ap = argparse.ArgumentParser(description="Misprediction / homogeneity analysis over validation records.")
    ap.add_argument("--results", nargs="*", default=[
        "results/validation_results.json", "results/validation_results_folder.json"],
        help="one or more validation_results*.json files (default: the two full-cohort files)")
    ap.add_argument("--out", default="analysis/misprediction_report.json")
    ap.add_argument("--topk", type=int, default=20, help="worst-K mispredictions to surface (E1)")
    ap.add_argument("--adjudicate", action="store_true",
                    help="LLM-adjudicate the worst-K (E1); needs the claude CLI")
    ap.add_argument("--judge-model", default="claude-sonnet-5")
    ap.add_argument("--parallel", type=int, default=6)
    args = ap.parse_args()

    records, meta, sources = load([str(ROOT / p if not Path(p).is_absolute() else p) for p in args.results])
    labelled = sum(1 for r in records if r.get("real_act") and r.get("pred_act"))
    if labelled == 0:
        raise SystemExit(
            "no move-labelled records found (real_act/pred_act). These result files predate the "
            "speech-act labelling in validate.py — rerun validate.py to produce labelled records.")

    report = {
        "sources": sources,
        "n_records": len(records),
        "n_move_labelled": labelled,
        "categories": CATS,
        "severity": SEVERITY_HELP,
        "A_move_accuracy": a_move_accuracy(records),
        "E2_marginal_confusion": e2_marginal_confusion(records),
        "E3_variance_collapse": e3_variance_collapse(records),
        "E4_median_regression": e4_median_regression(records),
        "E5_decision_vs_surface": e5_decision_vs_surface(records, meta),
        "E8_within_developer_spread": e8_within_developer_spread(records),
        "per_user_detail": per_user_detail(records),
    }
    worst = e1_worst_k(records, args.topk)
    if args.adjudicate:
        worst, adj_summary = adjudicate(worst, args.judge_model, args.parallel)
        report["E1_adjudication_summary"] = adj_summary
    report["E1_worst_k"] = worst

    out_path = ROOT / args.out if not Path(args.out).is_absolute() else Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=1, ensure_ascii=False))

    # concise console verdict
    def line(tag, s):
        print(f"  {tag}: {s}")
    print(f"\n=== misprediction / homogeneity report ({labelled} labelled points) ===")
    print("E3 between-user variance collapse (H2, primary):")
    for c, v in report["E3_variance_collapse"]["by_condition"].items():
        if "spread_pred" in v:
            line(c, f"spread pred {v['spread_pred']} vs real {v['spread_real']} "
                    f"(Δ{v['pred_minus_real']}, perm p={v['perm_p']}) "
                    f"{'COLLAPSE' if v['collapse'] else 'no collapse'}")
    print("E4 regression to median (H3, primary):")
    for c, v in report["E4_median_regression"]["by_condition"].items():
        if "mean_pred_minus_real" in v:
            line(c, f"dist→median pred {v['mean_dist_to_median_pred']} vs real "
                    f"{v['mean_dist_to_median_real']} (Δ{v['mean_pred_minus_real']}, "
                    f"wilcoxon p={v['wilcoxon_p']}) {'SHRINKS' if v['shrinks_to_median'] else 'no'}")
    print("E5 decision vs surface:", report["E5_decision_vs_surface"]["verdict"])
    try:
        shown = out_path.relative_to(ROOT)
    except ValueError:
        shown = out_path
    print(f"\nwrote {shown}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Score diversity of multi-turn rollouts produced by rollout.py.

Reads eval-diversity/rollouts.jsonl and reports, per arm:
  - user-turn diversity:  Vendi score + mean pairwise cosine distance
  - patch diversity:      Vendi score + mean pairwise cosine distance over final diffs
  - structure diversity:  Shannon entropy of the #turns distribution (+ mean/std)
  - realism guard (opt):  mean LLM plausibility score per rollout (--realism)
  - distance-to-real (opt): MMD (and Fréchet, if scipy) between the arm's user-turn
                            embedding cloud and a pool of REAL user messages (--real-turns)

Diversity is reported both pooled-per-arm and averaged-within-seed (the clean H1 test,
since within a seed the task is held fixed and only the user varies).

Usage:
  python3 eval-diversity/score.py
  python3 eval-diversity/score.py --realism --real-turns eval-diversity/real_turns.json
"""

import argparse
import json
import math
import re
import subprocess
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"   # users prompt in several languages
JUDGE_MODEL = "claude-haiku-4-5-20251001"
MIN_TURNS = 2
DIFF_WORDS = 1500


# ---- diversity primitives -------------------------------------------------

def vendi_score(emb):
    """Effective number of distinct items = exp(Shannon entropy of the normalized
    similarity-matrix eigenvalues). emb must be L2-normalized rows. Range [1, n]."""
    n = len(emb)
    if n < 2:
        return float(n)
    K = (emb @ emb.T) / n                       # cosine Gram / n  -> trace 1
    w = np.linalg.eigvalsh(K)
    w = w[w > 1e-12]
    return float(math.exp(-np.sum(w * np.log(w))))


def mean_pairwise_distance(emb):
    """Mean pairwise cosine distance (1 - cosine) over distinct pairs."""
    n = len(emb)
    if n < 2:
        return 0.0
    sims = emb @ emb.T
    off = sims[np.triu_indices(n, k=1)]
    return float(1.0 - off.mean())


def mmd_rbf(X, Y):
    """Unbiased MMD^2 with an RBF kernel (median-heuristic bandwidth). 0 = same dist."""
    if len(X) < 2 or len(Y) < 2:
        return None
    Z = np.vstack([X, Y])
    d2 = np.maximum(0, -2 * Z @ Z.T + (Z * Z).sum(1)[:, None] + (Z * Z).sum(1)[None, :])
    med = np.median(d2[np.triu_indices(len(Z), k=1)]) or 1.0
    g = 1.0 / med
    def k(A, B):
        a2, b2 = (A * A).sum(1)[:, None], (B * B).sum(1)[None, :]
        return np.exp(-g * np.maximum(0, a2 + b2 - 2 * A @ B.T))
    m, n = len(X), len(Y)
    kxx = (k(X, X).sum() - m) / (m * (m - 1))
    kyy = (k(Y, Y).sum() - n) / (n * (n - 1))
    kxy = k(X, Y).mean()
    return float(kxx + kyy - 2 * kxy)


def frechet(X, Y):
    """Fréchet distance between two embedding clouds (FID-style). Needs scipy."""
    try:
        from scipy.linalg import sqrtm
    except ImportError:
        return None
    mx, my = X.mean(0), Y.mean(0)
    cx, cy = np.cov(X, rowvar=False), np.cov(Y, rowvar=False)
    cov = sqrtm(cx @ cy)
    if np.iscomplexobj(cov):
        cov = cov.real
    return float(((mx - my) ** 2).sum() + np.trace(cx + cy - 2 * cov))


def entropy_of_counts(values):
    """Shannon entropy (nats) of the empirical distribution of integer values."""
    vals, counts = np.unique(values, return_counts=True)
    p = counts / counts.sum()
    return float(-np.sum(p * np.log(p)))


# ---- realism guard (standalone plausibility, no real reference needed) ------

def realism_score(turns, repo):
    convo = "\n\n".join(f"[{'AGENT' if t['role']=='assistant' else 'DEVELOPER'}]: "
                        f"{' '.join((t['text'] or '').split()[:200])}" for t in turns)
    prompt = ("Below is a session between a software developer and an AI coding agent in "
              f"repo `{repo}`. Judge ONLY the DEVELOPER messages: are they plausible, "
              "in-character things a real developer would type here (intent, length, tone)? "
              f"\n\n<conversation>\n{convo}\n</conversation>\n\n"
              'Respond with ONLY JSON: {"realism": <int 0-100>}')
    out = subprocess.run(["claude", "-p", prompt, "--model", JUDGE_MODEL,
                          "--disallowedTools", "Read,Write,Edit,Bash,Glob,Grep,Task,WebFetch,WebSearch",
                          "--max-turns", "6"], cwd=HERE.parent, capture_output=True, text=True, timeout=120)
    m = re.search(r'"realism"\s*:\s*(\d+)', out.stdout or "")
    return int(m.group(1)) if m else None


# ---- main -----------------------------------------------------------------

def user_text(rec):
    return "\n".join(t["text"] for t in rec["turns"] if t["role"] == "user" and t["text"])


def diff_text(rec):
    return " ".join((rec.get("final_diff") or "").split()[:DIFF_WORDS])


def arm_label(rec):
    return rec["arm"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rollouts", default=str(HERE / "rollouts.jsonl"))
    ap.add_argument("--realism", action="store_true", help="run the LLM realism guard")
    ap.add_argument("--real-turns", default=None,
                    help="json list of real developer messages, for distance-to-real (H2)")
    ap.add_argument("--out", default=str(HERE / "diversity_results.json"))
    args = ap.parse_args()

    recs = [json.loads(l) for l in Path(args.rollouts).read_text().splitlines()]
    recs = [r for r in recs if r.get("n_turns", 0) >= MIN_TURNS]
    if not recs:
        raise SystemExit("no rollouts with enough turns to score")

    from sentence_transformers import SentenceTransformer
    embed = SentenceTransformer(EMBED_MODEL)
    u_emb = embed.encode([user_text(r) or " " for r in recs], normalize_embeddings=True)
    d_emb = embed.encode([diff_text(r) or " " for r in recs], normalize_embeddings=True)
    for r, ue, de in zip(recs, u_emb, d_emb):
        r["_u"], r["_d"] = ue, de

    arms = sorted({arm_label(r) for r in recs})
    by_arm = {a: [r for r in recs if arm_label(r) == a] for a in arms}

    def diversity(rows, field):
        emb = np.array([r[field] for r in rows])
        return {"n": len(rows), "vendi": round(vendi_score(emb), 3),
                "mean_pairwise_dist": round(mean_pairwise_distance(emb), 4)}

    def within_seed(rows, field):
        """Average the diversity metric within each seed, then across seeds (H1)."""
        by_seed = defaultdict(list)
        for r in rows:
            by_seed[r["seed"]].append(r)
        vendis, dists = [], []
        for srows in by_seed.values():
            if len(srows) < 2:
                continue
            emb = np.array([r[field] for r in srows])
            vendis.append(vendi_score(emb))
            dists.append(mean_pairwise_distance(emb))
        return {"n_seeds": len(vendis),
                "vendi": round(float(np.mean(vendis)), 3) if vendis else None,
                "mean_pairwise_dist": round(float(np.mean(dists)), 4) if dists else None}

    summary = {}
    for a, rows in by_arm.items():
        nturns = [r["n_turns"] for r in rows]
        summary[a] = {
            "user_turns": {"pooled": diversity(rows, "_u"), "within_seed": within_seed(rows, "_u")},
            "patch":      {"pooled": diversity(rows, "_d"), "within_seed": within_seed(rows, "_d")},
            "structure":  {"n_turns_entropy": round(entropy_of_counts(nturns), 3),
                           "n_turns_mean": round(float(np.mean(nturns)), 2),
                           "n_turns_std": round(float(np.std(nturns)), 2)},
        }

    if args.realism:
        print("realism guard...")
        for a, rows in by_arm.items():
            scores = [s for r in rows if (s := realism_score(r["turns"], r["repo"])) is not None]
            summary[a]["realism_mean"] = round(float(np.mean(scores)), 1) if scores else None

    if args.real_turns:
        real = json.loads(Path(args.real_turns).read_text())
        r_emb = embed.encode([t for t in real if t], normalize_embeddings=True)
        print("distance-to-real (H2)...")
        for a, rows in by_arm.items():
            X = np.array([r["_u"] for r in rows])
            summary[a]["distance_to_real"] = {
                "mmd": round(mmd_rbf(X, r_emb), 5) if mmd_rbf(X, r_emb) is not None else None,
                "frechet": round(frechet(X, r_emb), 3) if frechet(X, r_emb) is not None else None,
            }

    for r in recs:
        r.pop("_u", None); r.pop("_d", None)
    Path(args.out).write_text(json.dumps({"embed_model": EMBED_MODEL, "arms": arms,
                                          "summary": summary}, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()

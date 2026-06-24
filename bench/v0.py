#!/usr/bin/env python3
"""UserSimBench v0 — offline MOVE-FIDELITY eval for coding-agent user simulators.

Builds on user.skill. For every held-out user-action turn we show a candidate simulator
the REAL conversation prefix (agent trajectory held fixed) and ask it to produce the
developer's next message. We label its conversational MOVE with the repo's speech-act
classifier and compare the MOVE DISTRIBUTION and per-turn move to the real developer's.

Why moves, not words: single-message text fidelity is saturated (ceiling.json: a real
message scores realism 29.1, the sim scores *higher*; real-vs-real 2AFC ~0.54 ≈ chance).
The signal lives in *which move* the developer makes — and whether the sim collapses into
"looks good, continue" (the easy-mode failure prior work found on tau-bench).

Models are routed through OpenRouter so any frontier model can be the simulator. v0 ships
three models that prior work (Sim2Real-USI, OdysSim) also evaluated, so we can ask whether
user-sim strength transfers from customer-service tau-bench to real coding sessions.

Metrics per (model, condition):
  MoveFid   — mean per-move Sørensen–Dice(sim_dist, real_dist)*100   (USI D-style; ↑ better)
  1-TVD     — histogram intersection of move distributions            (↑ better)
  CondAgree — per-turn fraction where sim move == real move           (↑ better; vs ceiling)
  approve%, critical% (=pushback+interrupt+bug_report), and Δ vs real (easy-mode signal)

References (no API calls, computed from the real labels):
  always_approve  — easy-mode positive control (should fail badly)
  majority        — always the most common real move (CondAgree floor = p_max)
  prior_sampler   — sample ~ real population move dist (MoveFid≈100 by construction but
                    CondAgree≈Σp² : "matching the marginal" is not conditional skill)

Usage:
  python3 bench/v0.py                 # full run (cached/resumable)
  python3 bench/v0.py --limit 6       # smoke test on first 6 points
"""

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "bench"))
import validate as V          # noqa: E402  (pure helpers: pick_points, build_prompt, ...)
import orouter                # noqa: E402

RESULTS = ROOT / "bench" / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
RAW = RESULTS / "v0_raw.jsonl"
SUMMARY = RESULTS / "v0_summary.json"

SLUGS = "marcus-sa jeevanpillay robouden melagiri dipree ujuc asragab pavel401 roo-oliv".split()

# Three frontier simulators that prior user-sim work also evaluated.
MODELS = {
    "deepseek-v3.1": "deepseek/deepseek-chat-v3.1",      # Sim2Real-USI best simulator (USI 76.0)
    "gpt-5":         "openai/gpt-5",                       # Sim2Real-USI GPT-5.x (USI ~70.9)
    "gemini-3.1-pro": "google/gemini-3.1-pro-preview",    # OdysSim most-human-like frontier (HumT)
}
CONDS = ["distilled", "generic"]   # own user folder (inline) vs no folder
JUDGE = "anthropic/claude-haiku-4.5"   # move classifier (matches repo JUDGE_MODEL family)
ACTIVE = {"new_work", "refine_redirect", "pushback", "bug_report", "question", "interrupt"}
CRITICAL = {"pushback", "interrupt", "bug_report"}
GEN_WORKERS = 8
LABEL_WORKERS = 8


# ---------------- generation ----------------

def clean_msg(t):
    """Strip role labels / wrapping quotes a model may add despite the output contract."""
    s = (t or "").strip()
    for tag in ("DEVELOPER:", "USER:", "Developer:", "User:", "Message:"):
        if s.startswith(tag):
            s = s[len(tag):].strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1].strip()
    return s


def load_points():
    pts = []
    for slug in SLUGS:
        ho = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
        for p in V.pick_points(ho):
            p["slug"] = slug
            p["point_id"] = f"{p['session_id']}#{p['turn_index']}"
            pts.append(p)
    return pts


def gen_message(point, model_id, cond):
    folder_text = V.load_folder_text(point["slug"]) if cond == "distilled" else ""
    prompt = V.build_prompt(point, folder_text)
    seed = int(hashlib.sha256(f"{point['point_id']}|{model_id}|{cond}".encode()).hexdigest(), 16) % (2**31)
    out = orouter.chat(model_id, prompt, max_tokens=1000, temperature=0.7,
                       reasoning_effort="low", seed=seed)
    return clean_msg(out)


# ---------------- move classifier (OpenRouter Haiku; same prompt as validate.speech_act) ----------------

def classify_move(text, prev_agent):
    if V.is_interrupt(text):
        return "interrupt"
    if not (text or "").strip() or V.is_cli_failure(text):
        return None
    prompt = (
        "A developer is using an AI coding agent. The agent just said:\n"
        f"<agent>{V.truncate_words(prev_agent, 120)}</agent>\n\n"
        "The developer's next message was:\n"
        f"<message>{V.truncate_words(text, 150)}</message>\n\n"
        "Classify the developer's conversational MOVE (speech act), ignoring the specific "
        "details/topic. Choose exactly one:\n"
        "- new_work: introduces a NEW feature/task/requirement to build or document\n"
        "- refine_redirect: steers or adjusts the CURRENT task; changes requirements\n"
        "- pushback: corrects, rejects, or complains about the agent's output/approach\n"
        "- bug_report: reports something broken or not behaving as expected\n"
        "- approve_proceed: approves, says continue, commit/push, or moves on\n"
        "- question: asks for information or clarification\n"
        "- other\n"
        'Respond with ONLY JSON: {"act": "<one of the above>"}'
    )
    out = orouter.chat(JUDGE, prompt, max_tokens=600, temperature=0, reasoning_effort=None)
    import re
    m = re.search(r'"act"\s*:\s*"(\w+)"', out)
    act = m.group(1) if m else None
    return act if act in V.SPEECH_ACTS else ("other" if act else None)


# ---------------- caching ----------------

def load_cache():
    cache = {}
    if RAW.exists():
        for line in RAW.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            cache[r["key"]] = r
    return cache


def append_cache(rec):
    with RAW.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---------------- metrics ----------------

def dist(moves):
    c = Counter(m for m in moves if m)
    n = sum(c.values()) or 1
    return {k: v / n for k, v in c.items()}, c


def movefid(real, sim):
    """Mean per-move Sørensen–Dice * 100 over the union of moves (USI D-style)."""
    rd, _ = dist(real)
    sd, _ = dist(sim)
    moves = set(rd) | set(sd)
    if not moves:
        return None
    ds = [2 * min(rd.get(m, 0), sd.get(m, 0)) / (rd.get(m, 0) + sd.get(m, 0))
          for m in moves if (rd.get(m, 0) + sd.get(m, 0)) > 0]
    return round(100 * sum(ds) / len(ds), 1)


def tvd(real, sim):
    rd, _ = dist(real)
    sd, _ = dist(sim)
    moves = set(rd) | set(sd)
    return round(0.5 * sum(abs(rd.get(m, 0) - sd.get(m, 0)) for m in moves), 3)


def rate(moves, subset):
    n = sum(1 for m in moves if m) or 1
    return round(sum(1 for m in moves if m in subset) / n, 3)


def cond_agree(pairs):
    ok = [(r == s) for r, s in pairs if r and s]
    return round(sum(ok) / len(ok), 3) if ok else None


def score_block(real_moves, sim_moves, paired):
    return {
        "n": len([m for m in sim_moves if m]),
        "MoveFid": movefid(real_moves, sim_moves),
        "1-TVD": round(1 - tvd(real_moves, sim_moves), 3),
        "CondAgree": cond_agree(paired),
        "approve%": rate(sim_moves, {"approve_proceed"}),
        "critical%": rate(sim_moves, CRITICAL),
        "active%": rate(sim_moves, ACTIVE),
    }


# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="cap #points (smoke test)")
    args = ap.parse_args()

    points = load_points()
    if args.limit:
        points = points[:args.limit]
    by_id = {p["point_id"]: p for p in points}
    print(f"{len(points)} prediction points across {len(SLUGS)} users")

    cache = load_cache()

    # ---- 1. generate candidate messages (3 models x 2 conds) ----
    jobs = [(p, name, mid, cond)
            for p in points
            for name, mid in MODELS.items()
            for cond in CONDS
            if f"gen|{p['point_id']}|{name}|{cond}" not in cache]
    print(f"generations to run: {len(jobs)} (cached: {len(points)*len(MODELS)*len(CONDS) - len(jobs)})")

    def run_gen(job):
        p, name, mid, cond = job
        msg = gen_message(p, mid, cond)
        return {"key": f"gen|{p['point_id']}|{name}|{cond}", "kind": "gen",
                "point_id": p["point_id"], "slug": p["slug"], "model": name,
                "cond": cond, "text": msg}

    with ThreadPoolExecutor(max_workers=GEN_WORKERS) as ex:
        for i, fut in enumerate(as_completed([ex.submit(run_gen, j) for j in jobs]), 1):
            rec = fut.result()
            cache[rec["key"]] = rec
            append_cache(rec)
            if i % 25 == 0:
                print(f"  gen {i}/{len(jobs)}")

    # ---- 2. label moves (real once per point; each generation) ----
    label_jobs = []
    for p in points:
        rk = f"label|real|{p['point_id']}"
        if rk not in cache:
            label_jobs.append(("real", rk, p["real"], p["prev_agent"], p))
    for p in points:
        for name in MODELS:
            for cond in CONDS:
                g = cache.get(f"gen|{p['point_id']}|{name}|{cond}")
                lk = f"label|{name}|{cond}|{p['point_id']}"
                if g and lk not in cache:
                    label_jobs.append(("gen", lk, g["text"], p["prev_agent"], p))
    print(f"move labels to run: {len(label_jobs)}")

    def run_label(job):
        kind, key, text, prev_agent, p = job
        return {"key": key, "kind": "label", "move": classify_move(text, prev_agent)}

    with ThreadPoolExecutor(max_workers=LABEL_WORKERS) as ex:
        for i, fut in enumerate(as_completed([ex.submit(run_label, j) for j in label_jobs]), 1):
            rec = fut.result()
            cache[rec["key"]] = rec
            append_cache(rec)
            if i % 50 == 0:
                print(f"  label {i}/{len(label_jobs)}")

    # ---- 3. assemble per-point real/sim moves ----
    real_move = {pid: cache.get(f"label|real|{pid}", {}).get("move") for pid in by_id}
    valid = [pid for pid in by_id if real_move[pid]]   # points with a real label
    real_moves = [real_move[pid] for pid in valid]

    results = {}
    for name in MODELS:
        for cond in CONDS:
            sim_moves, paired = [], []
            for pid in valid:
                sm = cache.get(f"label|{name}|{cond}|{pid}", {}).get("move")
                gt = cache.get(f"gen|{pid}|{name}|{cond}", {})
                if sm and not V.is_cli_failure(gt.get("text", "")):
                    sim_moves.append(sm)
                    paired.append((real_move[pid], sm))
            results[f"{name}/{cond}"] = score_block(real_moves, sim_moves, paired)

    # ---- 4. references (analytic, from real labels) ----
    rd, rc = dist(real_moves)
    pmax = rc.most_common(1)[0][0]

    def sample_from_real(pid):
        items = sorted(rd.items())
        tot = sum(w for _, w in items)
        h = int(hashlib.sha256(f"{pid}|prior".encode()).hexdigest(), 16)
        x = (h % 10000) / 10000 * tot
        c = 0.0
        for m, w in items:
            c += w
            if x <= c:
                return m
        return items[-1][0]

    refs = {
        "always_approve": ["approve_proceed"] * len(valid),
        "majority":       [pmax] * len(valid),
        "prior_sampler":  [sample_from_real(pid) for pid in valid],
    }
    for name, sm in refs.items():
        results[f"[ref] {name}"] = score_block(real_moves, sm, list(zip(real_moves, sm)))

    collision = round(sum(p * p for p in rd.values()), 3)  # CondAgree if you only knew the marginal

    out = {
        "n_points": len(valid),
        "real_move_distribution": {k: round(v, 3) for k, v in sorted(rd.items(), key=lambda x: -x[1])},
        "real_approve%": rate(real_moves, {"approve_proceed"}),
        "real_critical%": rate(real_moves, CRITICAL),
        "real_active%": rate(real_moves, ACTIVE),
        "condagree_marginal_ceiling": collision,
        "models": MODELS, "judge": JUDGE,
        "results": results,
    }
    SUMMARY.write_text(json.dumps(out, indent=1, ensure_ascii=False))

    # ---- 5. leaderboard ----
    print(f"\nreal move dist (n={len(valid)}): " +
          "  ".join(f"{k} {v:.0%}" for k, v in out["real_move_distribution"].items()))
    print(f"real approve%={out['real_approve%']}  critical%={out['real_critical%']}  "
          f"CondAgree marginal-ceiling (Σp²)={collision}\n")
    hdr = f"{'simulator':22s} {'MoveFid':>7} {'1-TVD':>6} {'CondAgr':>7} {'appr%':>6} {'crit%':>6} {'n':>4}"
    print(hdr); print("-" * len(hdr))
    order = ([f"{m}/{c}" for m in MODELS for c in CONDS] +
             ["[ref] prior_sampler", "[ref] majority", "[ref] always_approve"])
    for k in order:
        r = results[k]
        print(f"{k:22s} {str(r['MoveFid']):>7} {str(r['1-TVD']):>6} {str(r['CondAgree']):>7} "
              f"{str(r['approve%']):>6} {str(r['critical%']):>6} {r['n']:>4}")
    print(f"\nwrote {SUMMARY}")


if __name__ == "__main__":
    main()

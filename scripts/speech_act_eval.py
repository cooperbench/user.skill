#!/usr/bin/env python3
"""Demonstrate the reframed evaluation on EXISTING generations (no regeneration):
  - filter held-out targets to genuine USER ACTIONS (keep interrupts, drop harness artifacts)
  - label the speech act of the real message and of each condition's generation
  - report per-condition speech-act match (the fidelity metric the persona can be held to)

Usage: python3 scripts/speech_act_eval.py <gen.jsonl> <label> [<gen2.jsonl> <label2> ...]
"""

import json
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V

ROOT = Path(__file__).resolve().parent.parent
CONDS = ["distilled", "generic", "wrong"]


def prev_agent_for(slug, point_id):
    """Reconstruct the preceding agent turn for a (slug, point_id) from the holdout."""
    sid, _, ti = point_id.rpartition("#")
    ti = int(ti)
    ho = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
    for sess in ho["sessions"]:
        if sess["session_id"] == sid:
            turns = sess["turns"]
            return next((t["text"] for t in reversed(turns[:ti]) if t["role"] == "assistant"), "")
    return ""


def evaluate(gen_path, label, parallel=4):
    recs = [json.loads(l) for l in Path(gen_path).read_text().splitlines()]
    recs = [r for r in recs if r["generated"] and not V.is_cli_failure(r["generated"])]
    # keep only genuine user-action targets (interrupts kept, artifacts dropped)
    kept = [r for r in recs if V.is_user_action_target(r["real"])]
    dropped = len(recs) - len(kept)

    # cache prev_agent + real act per unique point
    points = {(r["slug"], r["point_id"]) for r in kept}
    pa = {k: prev_agent_for(*k) for k in points}
    real_act = {}
    with ThreadPoolExecutor(max_workers=parallel) as ex:
        futs = {ex.submit(V.speech_act, next(r["real"] for r in kept if (r["slug"], r["point_id"]) == k),
                          pa[k]): k for k in points}
        for fut in as_completed(futs):
            real_act[futs[fut]] = fut.result()

    def lab(r):
        r["pred_act"] = V.speech_act(r["generated"], pa[(r["slug"], r["point_id"])])
        r["real_act"] = real_act[(r["slug"], r["point_id"])]
        return r
    with ThreadPoolExecutor(max_workers=parallel) as ex:
        list(as_completed([ex.submit(lab, r) for r in kept]))

    def match_rate(cond):
        rows = [r for r in kept if r["cond"] == cond and r["real_act"] and r["pred_act"]]
        if not rows:
            return None, 0
        m = sum(1 for r in rows if r["real_act"] == r["pred_act"])
        return round(m / len(rows), 3), len(rows)

    print(f"\n===== {label}  ({gen_path}) =====")
    print(f"records {len(recs)} -> kept {len(kept)} user-action targets (dropped {dropped} artifacts)")
    rd = Counter(a for a in real_act.values() if a)
    print("real speech-act distribution:", dict(rd.most_common()))
    print(f"{'condition':12s} {'act-match':>10} {'n':>4}")
    out = {}
    for c in CONDS:
        rate, n = match_rate(c)
        out[c] = rate
        print(f"{c:12s} {str(rate):>10} {n:>4}")
    return out


def main():
    if len(sys.argv) < 3 or len(sys.argv) % 2 == 0:
        sys.exit("usage: speech_act_eval.py <gen.jsonl> <label> [<gen2> <label2> ...]")
    pairs = list(zip(sys.argv[1::2], sys.argv[2::2]))
    results = {label: evaluate(path, label) for path, label in pairs}
    print("\n===== summary: speech-act match (own vs wrong) =====")
    for label, o in results.items():
        d, w = o.get("distilled"), o.get("wrong")
        lift = f"+{d - w:.3f}" if (d is not None and w is not None) else "–"
        print(f"{label:24s} distilled={d}  generic={o.get('generic')}  wrong={w}  (own-wrong {lift})")


if __name__ == "__main__":
    main()

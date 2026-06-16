#!/usr/bin/env python3
"""Agent-replay: isolate USER-simulator fidelity from agent divergence.

Walk a real held-out session. At each real user turn, condition the context-driven
simulator on the REAL agent's actual prefix (so the agent trajectory is held fixed),
generate the user's message, and compare its MOVE + voice to the real user's. Because
the agent context is real, any divergence is purely the simulator's.

Headline: does the simulator react like the user at the SAME real moments — e.g. when the
real agent reports it deleted the user's files? Reports per-turn move-agreement + TVD, and
saves a turn-by-turn transcript for the report.

Usage: agent_replay.py <slug> <session_prefix>
"""

import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V

ROOT = Path(__file__).resolve().parent.parent


def main():
    slug, prefix = sys.argv[1], sys.argv[2]
    ho = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
    sess = [s for s in ho["sessions"] if s["session_id"].startswith(prefix)][0]
    turns = sess["turns"]
    repo = sess["repo"]
    fpath = f"users/{slug}"

    # real user turns that are genuine actions with >=1 preceding assistant turn
    points = []
    for i, t in enumerate(turns):
        if t["role"] != "user" or t.get("is_continuation"):
            continue
        if not V.is_user_action_target(t["text"]):
            continue
        if not any(p["role"] == "assistant" for p in turns[:i]):
            continue
        points.append(i)

    def prev_agent(i):
        return next((t["text"] for t in reversed(turns[:i]) if t["role"] == "assistant"), "")

    def gen_one(i):
        ctx = [{"role": tt["role"], "text": tt["text"]}
               for tt in turns[max(0, i - V.CONTEXT_TURNS):i]]
        point = {"repo": repo, "session_id": sess["session_id"], "turn_index": i, "context": ctx}
        # context-driven move selection (no forced move): the simulator must read the real
        # agent prefix and decide the move itself — this is the conditional-fidelity test.
        prompt = V.build_folder_prompt(point, fpath)
        sim = V.run_claude(prompt, V.GEN_MODEL, read_folder=True)
        return i, sim

    sims = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        for fut in as_completed([ex.submit(gen_one, i) for i in points]):
            i, sim = fut.result()
            sims[i] = sim

    def move(text, i):
        return "interrupt" if V.is_interrupt(text) else V.speech_act(text, prev_agent(i))

    rows, agree = [], 0
    real_moves, sim_moves = Counter(), Counter()
    label_jobs = []
    for i in points:
        label_jobs.append(("real", i, turns[i]["text"]))
        label_jobs.append(("sim", i, sims.get(i, "")))
    labels = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(move, txt, i): (kind, i) for kind, i, txt in label_jobs}
        for fut in as_completed(futs):
            kind, i = futs[fut]
            labels[(kind, i)] = fut.result()

    for i in points:
        rm, sm = labels.get(("real", i)), labels.get(("sim", i))
        if rm:
            real_moves[rm] += 1
        if sm:
            sim_moves[sm] += 1
        ok = (rm is not None and rm == sm)
        agree += ok
        rows.append({"turn": i, "real_move": rm, "sim_move": sm, "agree": ok,
                     "agent_said": prev_agent(i)[:160],
                     "real_msg": turns[i]["text"][:160], "sim_msg": (sims.get(i) or "")[:160]})

    def tvd(p, q):
        ks = set(p) | set(q); ps = sum(p.values()) or 1; qs = sum(q.values()) or 1
        return round(0.5 * sum(abs(p.get(k, 0) / ps - q.get(k, 0) / qs) for k in ks), 3)

    out = {
        "slug": slug, "session": sess["session_id"][:12], "repo": repo,
        "n_points": len(points),
        "per_turn_move_agreement": round(agree / max(1, len(points)), 3),
        "move_distribution_TVD_conditional": tvd(sim_moves, real_moves),
        "real_move_dist": dict(real_moves), "sim_move_dist": dict(sim_moves),
        "rows": rows,
    }
    (ROOT / "results" / f"agent_replay_{slug}_{prefix}.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({k: out[k] for k in
                      ["per_turn_move_agreement", "move_distribution_TVD_conditional",
                       "real_move_dist", "sim_move_dist"]}, indent=1))
    # show the crisis turns
    print("\n--- crisis turns (real agent context held fixed) ---")
    for r in rows:
        if "delete" in (r["agent_said"] + r["real_msg"]).lower() or r["real_move"] == "interrupt":
            print(f"[turn {r['turn']}] agent: {r['agent_said'][:70]!r}")
            print(f"   REAL [{r['real_move']}]: {r['real_msg'][:70]!r}")
            print(f"   SIM  [{r['sim_move']}]: {r['sim_msg'][:70]!r}")


if __name__ == "__main__":
    main()

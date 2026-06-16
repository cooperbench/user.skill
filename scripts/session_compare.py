#!/usr/bin/env python3
"""Distributional comparison: simulated session vs the real held-out session.
Compares move distribution, message lengths, interrupt rate, and flags simulator
meta-leaks (reasoning that leaked into the message). Move-distribution TVD is the
session-level fidelity number.
"""

import json
import re
import statistics as st
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V

ROOT = Path(__file__).resolve().parent.parent

# reasoning that leaked into a "message" instead of just the message
_LEAK = re.compile(r"\bthe move is\b|enough context|the conversation (just )?end|"
                   r"based on what i('?ve| have) read|i would (say|respond)|as the (developer|user)",
                   re.I)


def is_leak(t):
    return bool(_LEAK.search(t or ""))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else \
        str(ROOT / "results" / "session_sim_pavel401_cfdde919.json")
    d = json.loads(Path(path).read_text())

    sim_users = [t for t in d["simulated_transcript"] if t["role"] == "user"
                 and t.get("move") != "opening(seed)"]
    real_users = [t for t in d["real_user_turns"][1:]]  # drop shared opening

    # --- simulator quality: meta-leak rate ---
    leaks = [t for t in sim_users if is_leak(t["text"])]

    # --- moves: sim moves are recorded; label real turns with the speech-act classifier ---
    sim_moves = Counter(t["move"] for t in sim_users if not is_leak(t["text"]))

    def label(t):
        return V.speech_act(t, "") if not V.is_interrupt(t) else "interrupt"
    with ThreadPoolExecutor(max_workers=6) as ex:
        real_moves_list = list(ex.map(label, real_users))
    real_moves = Counter(m for m in real_moves_list if m)

    def norm(c):
        tot = sum(c.values()) or 1
        return {k: round(v / tot, 2) for k, v in c.items()}

    def tvd(p, q):
        ks = set(p) | set(q); ps = sum(p.values()) or 1; qs = sum(q.values()) or 1
        return round(0.5 * sum(abs(p.get(k, 0) / ps - q.get(k, 0) / qs) for k in ks), 3)

    def lengths(turns, key=lambda t: t):
        return [len((key(t)).split()) for t in turns]

    sim_len = lengths([t["text"] for t in sim_users if not is_leak(t["text"])])
    real_len = lengths(real_users)

    def interrupt_rate(texts):
        return round(sum(1 for t in texts if V.is_interrupt(t)) / max(1, len(texts)), 2)

    report = {
        "session": d["session_id"][:12], "repo": d["repo_id"],
        "n_sim_user_turns": len(sim_users), "n_real_user_turns": len(real_users),
        "meta_leak_rate": round(len(leaks) / max(1, len(sim_users)), 2),
        "move_dist_sim": norm(sim_moves), "move_dist_real": norm(real_moves),
        "move_distribution_TVD": tvd(sim_moves, real_moves),
        "median_words_sim": st.median(sim_len) if sim_len else None,
        "median_words_real": st.median(real_len) if real_len else None,
        "interrupt_rate_sim": interrupt_rate([t["text"] for t in sim_users]),
        "interrupt_rate_real": interrupt_rate(real_users),
    }
    print(json.dumps(report, indent=1, ensure_ascii=False))
    (ROOT / "results" / "session_compare.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()

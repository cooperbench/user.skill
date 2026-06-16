#!/usr/bin/env python3
"""Estimate the GLOBAL OPTIMUM (human ceiling) for the simulator metrics by scoring the
user's OWN genuine held-out messages with the same instruments:

  - realism ceiling: judge realism of a real message the user actually sent
  - 2AFC discrimination ceiling: given a user's real style sample, can the judge pick a REAL
    held-out message of theirs over a REAL held-out message of a different user?

Whatever a perfect simulator could achieve is bounded by these numbers, because they are what
the metric gives to authentic human behaviour. Compares against v5 (best simulator).
"""

import json
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V

ROOT = Path(__file__).resolve().parent.parent
SLUGS = "marcus-sa jeevanpillay robouden melagiri dipree ujuc asragab pavel401 roo-oliv".split()
PAR = 6


def real_targets():
    """One real held-out (user-action) message per (slug, point) from the v5 records."""
    recs = json.loads((ROOT / "results" / "folder_v5samp_9users.json").read_text())["records"]
    out = {}
    for r in recs:
        if r["cond"] == "distilled" and V.is_user_action_target(r["real"]):
            out.setdefault(r["slug"], []).append({"real": r["real"], "repo": r["repo"],
                                                  "pid": r["point_id"]})
    return out


def main():
    tgt = real_targets()
    slugs = [s for s in SLUGS if tgt.get(s)]

    # --- realism ceiling: judge realism of a real message, with a DIFFERENT real message of the
    # same user as the A-reference (so it is "another genuine message", not itself) ---
    realism_jobs = []
    for s in slugs:
        msgs = tgt[s]
        for i, m in enumerate(msgs):
            ref = msgs[(i + 1) % len(msgs)]["real"]  # another real msg from same user
            realism_jobs.append((s, ref, m["real"], m["repo"]))

    def judge_real(job):
        s, ref, real_msg, repo = job
        _, _, rl = V.judge(ref, real_msg, repo)  # realism of a genuine message
        return rl
    realism = []
    with ThreadPoolExecutor(max_workers=PAR) as ex:
        for fut in as_completed([ex.submit(judge_real, j) for j in realism_jobs]):
            v = fut.result()
            if v is not None:
                realism.append(v)
    realism_ceiling = round(st.mean(realism), 1) if realism else None

    # --- 2AFC discrimination ceiling: real-vs-real ---
    refs = {s: V.load_style_reference(s) for s in slugs}
    pairs = []
    for i, s in enumerate(slugs):
        other = slugs[(i + 1) % len(slugs)]
        for j, m in enumerate(tgt[s]):
            wrong_msg = tgt[other][j % len(tgt[other])]["real"]
            slot = "A" if (hash(m["pid"]) % 2 == 0) else "B"
            pairs.append((s, m["real"], wrong_msg, slot))

    def disc_real(job, criterion):
        s, own, wrong, slot = job
        a, b = (own, wrong) if slot == "A" else (wrong, own)
        pick = V.discriminate(refs[s], a, b, criterion=criterion)
        return (pick == slot) if pick else None
    disc = {}
    for crit in ["style", "realism"]:
        res = []
        with ThreadPoolExecutor(max_workers=PAR) as ex:
            for fut in as_completed([ex.submit(disc_real, j, crit) for j in pairs]):
                v = fut.result()
                if v is not None:
                    res.append(v)
        disc[crit] = round(sum(res) / len(res), 3) if res else None

    # v5 (best simulator) realism for comparison
    v5 = [r for r in json.loads((ROOT / "results" / "folder_v5samp_9users.json").read_text())["records"]
          if r["cond"] == "distilled" and V.is_user_action_target(r["real"])
          and r.get("judge_realism") is not None]
    v5_realism = round(st.mean(r["judge_realism"] for r in v5), 1)

    out = {
        "n_realism": len(realism), "n_disc": len(pairs),
        "realism_ceiling_real_messages": realism_ceiling,
        "realism_v5_simulator": v5_realism,
        "discrimination_ceiling": disc,
        "chance": 0.5,
    }
    (ROOT / "results" / "ceiling.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

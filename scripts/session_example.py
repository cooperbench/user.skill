#!/usr/bin/env python3
"""Render a COMPLETE real session next to its simulated counterpart (agent-replay style:
the real agent's turns are held fixed; at each real user turn the simulator produces the
user's message conditioned on the real prefix). Stores full text and writes a standalone
HTML transcript (results/session_example.html) + JSON.

Usage: session_example.py <slug> <session_prefix>
"""

import html
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V

ROOT = Path(__file__).resolve().parent.parent


def main():
    slug, prefix = sys.argv[1], sys.argv[2]
    ho = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
    sess = [s for s in ho["sessions"] if s["session_id"].startswith(prefix)][0]
    turns, repo, fpath = sess["turns"], sess["repo"], f"users/{slug}"

    def prev_agent(i):
        return next((t["text"] for t in reversed(turns[:i]) if t["role"] == "assistant"), "")

    # simulate at every real user turn that has a preceding agent turn (agent-replay)
    sim_idx = [i for i, t in enumerate(turns)
               if t["role"] == "user" and not t.get("is_continuation")
               and V.is_user_action_target(t["text"])
               and any(p["role"] == "assistant" for p in turns[:i])]

    def gen(i):
        ctx = [{"role": tt["role"], "text": tt["text"]} for tt in turns[max(0, i - V.CONTEXT_TURNS):i]]
        point = {"repo": repo, "session_id": sess["session_id"], "turn_index": i, "context": ctx}
        return i, V.run_claude(V.build_folder_prompt(point, fpath), V.GEN_MODEL, read_folder=True)

    sims = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        for fut in as_completed([ex.submit(gen, i) for i in sim_idx]):
            i, s = fut.result()
            sims[i] = s

    def mv(text, i):
        return "interrupt" if V.is_interrupt(text) else V.speech_act(text, prev_agent(i))
    jobs = [("real", i, turns[i]["text"]) for i in sim_idx] + [("sim", i, sims.get(i, "")) for i in sim_idx]
    lab = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(mv, t, i): (k, i) for k, i, t in jobs}
        for fut in as_completed(futs):
            lab[futs[fut]] = fut.result()

    # ---- render complete transcript ----
    rows = []
    for i, t in enumerate(turns):
        if t["role"] == "assistant":
            txt = html.escape(t["text"][:700]) + ("…" if len(t["text"]) > 700 else "")
            rows.append(f"<tr><td class='agent' colspan='2'><b>AGENT</b> · {txt}</td></tr>")
        elif t["role"] == "user":
            real_txt = html.escape(t["text"])
            if i in sims:
                rm, sm = lab.get(("real", i)), lab.get(("sim", i))
                sim_txt = html.escape(sims[i] or "—")
                ag = " agree" if rm and rm == sm else ""
                rows.append(
                    f"<tr><td class='ur'><span class='mv'>{rm}</span> {real_txt}</td>"
                    f"<td class='us{ag}'><span class='mv'>{sm}</span> {sim_txt}</td></tr>")
            else:  # opening / non-simulated user turn
                rows.append(f"<tr><td class='ur'>{real_txt}</td><td class='us na'>— (not simulated)</td></tr>")

    agree = sum(1 for i in sim_idx if lab.get(("real", i)) and lab.get(("real", i)) == lab.get(("sim", i)))
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Real vs simulated session — {html.escape(slug)}</title>
<style>
 body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; max-width: 1100px; margin: 2rem auto;
        padding: 0 1rem; color: #1a1a2e; line-height: 1.5; }}
 h1 {{ border-bottom: 3px solid #7c3aed; padding-bottom: .3rem; }}
 table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
 td {{ vertical-align: top; padding: .5rem .7rem; border-bottom: 1px solid #eee; font-size: .9rem; }}
 td.agent {{ background: #f6f6fb; color: #555; font-size: .82rem; }}
 td.ur {{ width: 50%; background: #fbf7ff; border-left: 3px solid #7c3aed; }}
 td.us {{ width: 50%; background: #f0f9ff; border-left: 3px solid #0ea5e9; }}
 td.us.agree {{ background: #f0fdf4; border-left-color: #16a34a; }}
 td.us.na {{ color: #aaa; background: #fafafa; border-left-color: #ddd; }}
 .mv {{ display:inline-block; font-size:.7rem; text-transform:uppercase; letter-spacing:.03em;
       background:#e7e1f5; color:#4c1d95; border-radius:3px; padding:0 5px; margin-right:5px; }}
 .hdr {{ display:flex; gap:1rem; font-weight:600; margin-top:1rem; }}
 .hdr div {{ flex:1; }} .l {{ color:#7c3aed; }} .r {{ color:#0ea5e9; }}
 .note {{ background:#f5f0ff; border-left:4px solid #7c3aed; padding:.6rem 1rem; border-radius:4px; }}
</style></head><body>
<h1>Complete session: real vs simulated developer ({html.escape(slug)})</h1>
<p class="note">One real held-out session in <code>{html.escape(repo)}</code>, replayed from the
reconstructed pre-session codebase. The <b>real agent turns are held fixed</b>; at each user turn the
<b>simulated developer</b> (v5 folder simulator) produces its message conditioned on the same real
prefix — so the left and right columns face identical context. Move tags are the labelled speech act;
green = same move as the real user. Per-turn move agreement: <b>{agree}/{len(sim_idx)}</b>.</p>
<div class="hdr"><div class="l">◀ REAL developer</div><div class="r">SIMULATED developer ▶</div></div>
<table><tbody>{''.join(rows)}</tbody></table>
<footer style="margin-top:2rem;font-size:.8rem;color:#888">scripts/session_example.py ·
github.com/cooperbench/user.skill</footer>
</body></html>"""
    (ROOT / "results" / "session_example.html").write_text(page)
    (ROOT / "results" / "session_example.json").write_text(json.dumps(
        {"slug": slug, "session": sess["session_id"], "repo": repo,
         "agreement": f"{agree}/{len(sim_idx)}",
         "turns": [{"i": i, "role": turns[i]["role"], "real": turns[i]["text"],
                    "sim": sims.get(i), "real_move": lab.get(("real", i)),
                    "sim_move": lab.get(("sim", i))} for i in range(len(turns))]},
        indent=1, ensure_ascii=False))
    print(f"wrote results/session_example.html  (agreement {agree}/{len(sim_idx)})")


if __name__ == "__main__":
    main()

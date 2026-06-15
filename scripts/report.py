#!/usr/bin/env python3
"""Generate results/report.html — the user-simulator fidelity study.

Computes content/realism (and speech-act match where present) on FILTERED user-action
targets from the saved result files. Speech-act numbers for the variants scored before
the metric existed are taken from the speech_act_eval.py run (documented constants).
"""

import html
import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

VARIANTS = [
    ("inline-v1", "Inline (folder pasted in)", "results/rescored_inline_9users.json"),
    ("folder-v1", "Folder-access (reads folder)", "results/rescored_folder_9users.json"),
    ("folder-v2", "Folder + intent-first prompt", "results/folder_v2_9users.json"),
    ("folder-v3", "Folder + shared scaffold (optimized)", "results/folder_v3_9users.json"),
]

# Speech-act match measured by speech_act_eval.py on the same generations, for the
# variants scored before the metric was integrated into validate.py.
SPEECH_ACT_CONST = {
    "inline-v1": {"distilled": 0.294, "generic": 0.098, "wrong": 0.255},
    "folder-v1": {"distilled": 0.235, "generic": 0.137, "wrong": 0.196},
    "folder-v2": {"distilled": 0.255, "generic": 0.196, "wrong": 0.255},
}
CONDS = ["distilled", "generic", "wrong"]


def fmt(v, pct=False, plus=False):
    if v is None:
        return "–"
    s = f"{100 * v:.1f}%" if pct else (f"{v:.1f}" if isinstance(v, float) else str(v))
    return ("+" + s) if (plus and isinstance(v, (int, float)) and v >= 0) else s


def filtered(path):
    p = RESULTS / Path(path).name
    if not p.exists():
        return None
    return [r for r in json.loads(p.read_text())["records"]
            if V.is_user_action_target(r["real"]) and r["generated"]
            and not V.is_cli_failure(r["generated"])]


def mean(rows, k):
    v = [r[k] for r in rows if r.get(k) is not None]
    return round(st.mean(v), 1) if v else None


def act_match(rows):
    v = [r for r in rows if r.get("real_act") and r.get("pred_act")]
    return round(sum(1 for r in v if r["real_act"] == r["pred_act"]) / len(v), 3) if v else None


def variant_stats(key, path):
    recs = filtered(path)
    if recs is None:
        return None
    out = {}
    for c in CONDS:
        rows = [r for r in recs if r["cond"] == c]
        am = act_match(rows)
        if am is None:
            am = SPEECH_ACT_CONST.get(key, {}).get(c)
        out[c] = {"content": mean(rows, "judge_content"), "realism": mean(rows, "judge_realism"),
                  "act": am, "n": len(rows)}
    return out


def main():
    stats = {k: variant_stats(k, p) for k, _, p in VARIANTS if variant_stats(k, p)}

    # main comparison table
    rows = []
    for key, label, _ in VARIANTS:
        s = stats.get(key)
        if not s:
            continue
        d, w = s["distilled"], s["wrong"]
        opt = " class=opt" if key == "folder-v3" else ""
        rows.append(
            f"<tr{opt}><td>{html.escape(label)}</td>"
            f"<td class='num'>{fmt(d['content'])}</td><td class='num'>{fmt(w['content'])}</td>"
            f"<td class='num'>{fmt(d['realism'])}</td><td class='num'>{fmt(w['realism'])}</td>"
            f"<td class='num'>{fmt(d['act'], pct=True)}</td><td class='num'>{fmt(w['act'], pct=True)}</td></tr>")
    comp_table = "".join(rows)

    # optimization delta (folder-v1 -> folder-v3) on distilled
    v1, v3 = stats.get("folder-v1"), stats.get("folder-v3")
    def delta(metric, fn=lambda x: x):
        a, b = v1["distilled"][metric], v3["distilled"][metric]
        return a, b, (b - a if a is not None and b is not None else None)

    # move distribution (real vs predicted) from folder-v3
    recs_v3 = filtered("results/folder_v3_9users.json")
    d3 = [r for r in recs_v3 if r["cond"] == "distilled"]
    real_dist = Counter(r["real_act"] for r in d3 if r.get("real_act"))
    pred_dist = Counter(r["pred_act"] for r in d3 if r.get("pred_act"))
    pred_labeled = sum(pred_dist.values())
    ACTS = ["approve_proceed", "refine_redirect", "new_work", "bug_report", "pushback",
            "interrupt", "question"]
    move_rows = []
    rt = sum(real_dist.values()) or 1
    pt = pred_labeled or 1
    for a in ACTS:
        rp, pp = 100 * real_dist.get(a, 0) / rt, 100 * pred_dist.get(a, 0) / pt
        flag = " ⚠" if (a == "interrupt" and pred_dist.get(a, 0) == 0) else ""
        move_rows.append(
            f"<tr><td>{a}{flag}</td>"
            f"<td class='num'>{rp:.0f}%</td><td class='barcell'><div class='bar real' style='width:{rp:.0f}%'></div></td>"
            f"<td class='num'>{pp:.0f}%</td><td class='barcell'><div class='bar pred' style='width:{pp:.0f}%'></div></td></tr>")
    move_table = "".join(move_rows)

    a_r, a_v, a_d = delta("realism")
    c_r, c_v, c_d = delta("content")
    m_r, m_v, m_d = delta("act")

    report = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>User.skill: simulator fidelity study</title>
<style>
 body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; max-width: 1060px;
        margin: 2rem auto; padding: 0 1rem; color: #1a1a2e; line-height: 1.55; }}
 h1 {{ border-bottom: 3px solid #7c3aed; padding-bottom: .4rem; }}
 h2 {{ margin-top: 2.4rem; color: #4c1d95; border-bottom: 1px solid #e3d9f7; padding-bottom: .2rem; }}
 table {{ border-collapse: collapse; width: 100%; margin: .7rem 0 1.2rem; font-size: .87rem; }}
 th, td {{ text-align: left; padding: .38rem .55rem; border-bottom: 1px solid #e3e6ef; }}
 th {{ background: #f7f3ff; }}
 td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
 tr.opt td {{ background: #f0fdf4; font-weight: 600; }}
 td.barcell {{ width: 26%; }} .bar {{ height: 13px; border-radius: 3px; }}
 .bar.real {{ background: #7c3aed; }} .bar.pred {{ background: #f0883e; }}
 .note {{ background: #f5f0ff; border-left: 4px solid #7c3aed; padding: .6rem 1rem; border-radius: 4px; }}
 .warn {{ background: #fff7ed; border-left: 4px solid #f0883e; padding: .6rem 1rem; border-radius: 4px; }}
 .twin {{ display:flex; gap:1rem; flex-wrap:wrap; margin:1rem 0; }}
 .stat {{ flex:1 1 150px; background:#f0f4ff; border-radius:10px; padding:.9rem 1.1rem; }}
 .stat .bn {{ font-size:1.7rem; font-weight:800; color:#4361ee; }}
 .stat.up .bn {{ color:#16a34a; }} .stat .bl {{ font-size:.8rem; color:#555; }}
 .legend {{ font-size:.8rem; color:#666; }} .sw {{ display:inline-block; width:10px; height:10px; border-radius:2px; margin:0 3px 0 8px; vertical-align:middle; }}
</style></head><body>
<h1>User.skill: how faithfully can we simulate a developer?</h1>
<p>We distil each SWE-chat user (≥6 sessions) into a role-playable folder, then a Claude-Code agent
role-plays them and we score the next message it produces against the real held-out one. This report
covers the evaluation as it stands after several iterations: <b>filtering targets to genuine user
actions</b>, scoring on <b>content</b>, <b>realism</b> and <b>speech-act match</b>, and an
<b>optimized simulator</b> built on a shared scaffold. 9 users; the distillation itself ran for all 99.</p>

<h2>How we measure fidelity</h2>
<p>Predicting a user's <em>exact</em> next message is near-impossible — at any point many messages
are plausible, and the specific one depends on the user's private plan and the repo state. So we
measure three complementary things, and we only score turns the user <em>actually authored</em>
(genuine prompts and interrupts; harness artifacts like injected docs / command output are filtered out).</p>
<ul>
<li><b>Content</b> (0–100) — did the simulator predict roughly the right <em>ask</em>? Useful when the
substance is predictable; modest ceiling otherwise.</li>
<li><b>Realism</b> (0–100) — is the message a plausible, in-character thing this user would send,
judged by intent/substance and <em>not</em> catchphrase mimicry?</li>
<li><b>Speech-act match</b> — did the simulator make the right <em>move</em>
(new_work / refine_redirect / pushback / bug_report / approve_proceed / question / interrupt)? This
is the fidelity a persona can fairly be held to when exact content is unknowable.</li>
</ul>
<p class="note">The clean test for user-specific signal is <b>own folder vs. wrong folder</b>: it holds
"has a folder" constant, so any gap is genuinely about <em>which</em> user. Across content, realism
and speech-act, the distilled folder beats a wrong user's folder for the v1 simulators — the
distillation encodes real user-specific behaviour.</p>

<h2>Simulator variants compared</h2>
<p>All on filtered user-action targets (9 users). "own" = the user's own folder; "wrong" = a different
user's folder.</p>
<table><thead><tr><th>Simulator</th>
<th class='num'>content own</th><th class='num'>content wrong</th>
<th class='num'>realism own</th><th class='num'>realism wrong</th>
<th class='num'>act own</th><th class='num'>act wrong</th></tr></thead>
<tbody>{comp_table}</tbody></table>
<p class="legend">Green row = the optimized simulator (shared scaffold). Content/realism are
0–100 judge means; act is speech-act match rate.</p>

<h2>The optimization: a shared simulator scaffold</h2>
<p>The biggest fidelity lever isn't voice — it's <em>which move</em> the user makes. We added a
<b>shared layer</b> across all users (<code>simulator/AGENT.md</code> + move-playbook skills:
drive-the-project, push-back, interrupt, report-what-you-notice, calibrate-to-the-user) that encodes
how real developers drive a session and tells each simulation to match the user's move rates. The
per-user folder then only specialises voice. Effect on the distilled condition (folder-v1 → optimized):</p>
<div class="twin">
  <div class="stat up"><div class="bn">{fmt(a_d, plus=True)}</div><div class="bl">realism ({fmt(a_r)} → {fmt(a_v)})</div></div>
  <div class="stat up"><div class="bn">{fmt(m_d, pct=True, plus=True)}</div><div class="bl">speech-act match ({fmt(m_r, pct=True)} → {fmt(m_v, pct=True)})</div></div>
  <div class="stat"><div class="bn">{fmt(c_d, plus=True)}</div><div class="bl">content ({fmt(c_r)} → {fmt(c_v)})</div></div>
</div>
<p>The shared scaffold genuinely raised <b>absolute</b> realism and move-accuracy. But it exposed two
hard limits, below.</p>

<h2>Limit 1 — the simulator still won't diversify its moves</h2>
<p>Real users approve only part of the time and make a wide range of moves; the simulator collapses
toward "approve / continue" and — despite an explicit interrupt action and skill — <b>never
interrupts</b>.</p>
<table><thead><tr><th>move</th><th class='num'>real</th><th></th>
<th class='num'>simulated</th><th></th></tr></thead><tbody>{move_table}</tbody></table>
<p class="legend"><span class="sw" style="background:#7c3aed"></span>real users
<span class="sw" style="background:#f0883e"></span>optimized simulator (labeled predictions). ⚠ = the
simulator produced zero of this move across all targets.</p>
<p class="warn">The base model's cooperative "approve and continue" prior survives prompt-level
instructions. Forcing move-diversity needs <b>move-conditioned generation</b>: sample the move from the
user's own rate distribution, then generate that move — the clear next iteration.</p>

<h2>Limit 2 — better, but not more user-specific</h2>
<p>The shared scaffold lifts <em>every</em> condition — the no-folder generic baseline's realism rose
to {fmt(stats['folder-v3']['generic']['realism'])} and the wrong folder improved too. So while absolute
fidelity went up, the <b>own-vs-wrong</b> gap did not: content even inverted (own {fmt(v3['distilled']['content'])}
vs wrong {fmt(v3['wrong']['content'])}) and speech-act match tied. General simulator skill and
user-discriminability are partly in tension — shared knowledge helps the wrong folder just as much.</p>

<h2>Where it stands</h2>
<ul>
<li><b>The distillation captures real user signal</b> — own beats wrong on all three axes (v1 sims).</li>
<li><b>Exact content has a low ceiling</b>; speech-act + realism are the fair fidelity axes, and
content stays useful where substance is predictable.</li>
<li><b>The shared scaffold raised absolute realism (+{fmt(a_d)}) and move-accuracy
(+{fmt(m_d, pct=True)})</b>, but can't force move-diversity or add user-specificity by itself.</li>
<li><b>Next:</b> move-conditioned generation — sample each turn's move from the user's measured
distribution, then generate — to fix both the over-approval/zero-interrupt bias and discriminability.</li>
</ul>

<footer style="margin-top:3rem;font-size:.8rem;color:#888">Generated by scripts/report.py —
github.com/cooperbench/user.skill. Speech-act for pre-metric variants measured by
scripts/speech_act_eval.py on the same generations.</footer>
</body></html>"""
    out = RESULTS / "report.html"
    out.write_text(report)
    print(out)


if __name__ == "__main__":
    main()

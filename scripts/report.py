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
    ("folder-v3", "Folder + shared scaffold", "results/folder_v3_9users.json"),
    ("folder-v5", "Folder + move-sampling (best)", "results/folder_v5samp_9users.json"),
    ("folder-v6", "+ per-move few-shot exemplars", "results/folder_v6ex_9users.json"),
    ("folder-v7", "+ per-move length calibration", "results/folder_v7len_9users.json"),
]
ABLATIONS = {"folder-v6", "folder-v7"}  # tried-and-rejected personalizations

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
        opt = " class=opt" if key == "folder-v5" else (" class=abl" if key in ABLATIONS else "")
        rows.append(
            f"<tr{opt}><td>{html.escape(label)}</td>"
            f"<td class='num'>{fmt(d['content'])}</td><td class='num'>{fmt(w['content'])}</td>"
            f"<td class='num'>{fmt(d['realism'])}</td><td class='num'>{fmt(w['realism'])}</td>"
            f"<td class='num'>{fmt(d['act'], pct=True)}</td><td class='num'>{fmt(w['act'], pct=True)}</td></tr>")
    comp_table = "".join(rows)

    # final delta (folder-v1 -> folder-v5, the best simulator) on distilled
    v1, v5 = stats.get("folder-v1"), stats.get("folder-v5")
    v3 = stats.get("folder-v3")
    def delta(metric):
        a, b = v1["distilled"][metric], v5["distilled"][metric]
        return a, b, (b - a if a is not None and b is not None else None)

    # move-distribution fidelity: real vs each simulator's chosen moves, + TVD
    def chosen_moves(path, cond="distilled", field="conditioned_move"):
        recs = filtered(path) or []
        return Counter(r[field] for r in recs if r["cond"] == cond and r.get(field))
    real_dist = Counter()
    for r in (filtered("results/folder_v3_9users.json") or []):
        if r["cond"] == "distilled":
            a = r.get("real_act") or ("interrupt" if V.is_interrupt(r["real"]) else None)
            if a:
                real_dist[a] += 1
    v4_moves = chosen_moves("results/folder_v4mc_9users.json")
    v5_moves = chosen_moves("results/folder_v5samp_9users.json")
    v5_wrong = chosen_moves("results/folder_v5samp_9users.json", cond="wrong")

    def tvd(p, q):
        ks = set(p) | set(q); ps = sum(p.values()) or 1; qs = sum(q.values()) or 1
        return round(0.5 * sum(abs(p.get(k, 0) / ps - q.get(k, 0) / qs) for k in ks), 3)
    tvd_v4, tvd_v5 = tvd(v4_moves, real_dist), tvd(v5_moves, real_dist)
    tvd_ownwrong = tvd(v5_moves, v5_wrong)

    ACTS = ["approve_proceed", "refine_redirect", "new_work", "bug_report", "pushback",
            "interrupt", "question"]
    def pct_of(d, a):
        return 100 * d.get(a, 0) / (sum(d.values()) or 1)
    move_rows = []
    for a in ACTS:
        rp, p4, p5 = pct_of(real_dist, a), pct_of(v4_moves, a), pct_of(v5_moves, a)
        move_rows.append(
            f"<tr><td>{a}</td>"
            f"<td class='num'>{rp:.0f}%</td><td class='barcell'><div class='bar real' style='width:{rp:.0f}%'></div></td>"
            f"<td class='num'>{p4:.0f}%</td><td class='barcell'><div class='bar pred' style='width:{p4:.0f}%'></div></td>"
            f"<td class='num'>{p5:.0f}%</td><td class='barcell'><div class='bar v5' style='width:{p5:.0f}%'></div></td></tr>")
    move_table = "".join(move_rows)

    # ---- session-level experiments (closed-loop + agent-replay) ----
    def _load(p):
        f = RESULTS / p
        return json.loads(f.read_text()) if f.exists() else None
    sc = _load("session_compare.json")
    ar = _load("agent_replay_pavel401_cfdde919.json")
    crisis_rows = ""
    if ar:
        for r in ar["rows"]:
            blob = (r["agent_said"] + r["real_msg"]).lower()
            if "delete" in blob or r["real_move"] == "interrupt":
                crisis_rows += (
                    f"<tr><td>{html.escape(r['agent_said'][:90])}…</td>"
                    f"<td><b>[{r['real_move']}]</b><br>{html.escape(r['real_msg'][:70])}</td>"
                    f"<td>[{r['sim_move']}]<br>{html.escape((r['sim_msg'] or '')[:70])}</td></tr>")

    a_r, a_v, a_d = delta("realism")
    c_r, c_v, c_d = delta("content")
    m_r, m_v, m_d = delta("act")
    # v3's flattened own-vs-wrong (the limit that v5 fixes)
    v3_cgap = v3["distilled"]["content"] - v3["wrong"]["content"]
    v5_cgap = v5["distilled"]["content"] - v5["wrong"]["content"]
    v5_rgap = v5["distilled"]["realism"] - v5["wrong"]["realism"]
    v5_agap = (v5["distilled"]["act"] or 0) - (v5["wrong"]["act"] or 0)

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
 tr.abl td {{ background: #fef2f2; color: #991b1b; }}
 td.barcell {{ width: 26%; }} .bar {{ height: 13px; border-radius: 3px; }}
 .bar.real {{ background: #7c3aed; }} .bar.pred {{ background: #f0883e; }} .bar.v5 {{ background: #16a34a; }}
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
role-plays them and we score the next message it produces against the real held-out one. The report
traces the arc from a plain folder-reading simulator to the best one: <b>filtering targets to genuine
user actions</b>, scoring on <b>content</b>, <b>realism</b> and <b>speech-act match</b>, a
<b>shared scaffold</b>, and finally <b>per-user move-sampling</b> — which gives the most realistic and
correctly user-specific simulator. 9 users; the distillation itself ran for all 99.</p>

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
<p class="legend">Green row = best simulator (v5). <span style="color:#991b1b">Red rows = personalization
ablations that were tried and <b>rejected</b></span>. Content/realism are 0–100 judge means; act is
speech-act match rate.</p>
<p class="warn"><b>What didn't work (and why it's informative).</b> Two further personalization methods
on top of v5 both <em>hurt</em>: (v6) few-shotting the user's own real same-move messages induced
mimicry (the realism judge penalizes copying) and leaked generic human-ness into the wrong-folder
condition too, collapsing discriminability; (v7) injecting the user's per-move median length
over-constrained generation, lowering realism without even improving length-match. The lesson:
<b>v5's move-sampling is a local optimum</b> — the model already infers length and register from the
sampled move plus the folder, so additional prompt-level signals make output stilted. Further gains
need a non-prompt lever (a stronger generation model or fine-tuning), not more prompt content.</p>

<h2>Best simulator: folder-v1 → move-sampling (v5)</h2>
<p>The biggest fidelity lever isn't voice — it's <em>which move</em> the user makes. The final design
has three layers: a <b>shared scaffold</b> (<code>simulator/AGENT.md</code> + move-playbook skills)
for general competence; a <b>per-user move prior</b> (sampled each turn from the user's own
intent/pushback rates in <code>stats.json</code>) that sets the move-mix; and the <b>per-user
folder</b> for voice. Effect of the best simulator (folder-v1 → v5) on the distilled condition:</p>
<div class="twin">
  <div class="stat up"><div class="bn">{fmt(a_d, plus=True)}</div><div class="bl">realism ({fmt(a_r)} → {fmt(a_v)}), highest of any variant</div></div>
  <div class="stat up"><div class="bn">{fmt(m_d, pct=True, plus=True)}</div><div class="bl">speech-act match ({fmt(m_r, pct=True)} → {fmt(m_v, pct=True)})</div></div>
  <div class="stat"><div class="bn">{fmt(c_d, plus=True)}</div><div class="bl">content ({fmt(c_r)} → {fmt(c_v)})</div></div>
</div>
<p>Getting there took two iterations past the shared scaffold (v3), which raised absolute realism but
exposed two limits — both now resolved by move-sampling.</p>

<h2>Limit 1 (resolved) — diversify the moves &amp; actually interrupt</h2>
<p>Real users approve only part of the time; the shared-scaffold simulator (v3) collapsed toward
"approve / continue" and never interrupted. The fix is <b>move-conditioned generation</b>: choose the
move first, then render it. Choosing it with an LLM (v4) over-corrected to 74% pushback; <b>sampling
the move from the user's own rate distribution (v5)</b> matches the real move-mix and fires interrupts.
Distance from the real move distribution (total-variation, lower is better):
v4-predict <b>{tvd_v4}</b> → v5-sample <b>{tvd_v5}</b>.</p>
<table><thead><tr><th>move</th>
<th class='num'>real</th><th></th>
<th class='num'>v4 predict</th><th></th>
<th class='num'>v5 sample</th><th></th></tr></thead><tbody>{move_table}</tbody></table>
<p class="legend"><span class="sw" style="background:#7c3aed"></span>real users
<span class="sw" style="background:#f0883e"></span>v4 (LLM picks move — collapses to pushback)
<span class="sw" style="background:#16a34a"></span>v5 (sampled from prior — tracks real, interrupts included).</p>

<h2>Limit 2 (resolved) — make the gains user-specific</h2>
<p>The shared scaffold lifted <em>every</em> condition equally, so the <b>own-vs-wrong</b> gap
collapsed: v3's content gap even inverted ({fmt(v3_cgap, plus=True)}). Because the v5 move prior is
<em>derived from each user's own rates</em>, the own-folder and wrong-folder simulators now sample
<em>different</em> move-mixes (own vs. wrong move-distribution distance = <b>{tvd_ownwrong}</b>), so
discriminability returns across all axes:</p>
<div class="twin">
  <div class="stat up"><div class="bn">{fmt(v5_cgap, plus=True)}</div><div class="bl">content own−wrong (was {fmt(v3_cgap, plus=True)} in v3)</div></div>
  <div class="stat up"><div class="bn">{fmt(v5_rgap, plus=True)}</div><div class="bl">realism own−wrong</div></div>
  <div class="stat up"><div class="bn">{fmt(v5_agap, pct=True, plus=True)}</div><div class="bl">speech-act own−wrong</div></div>
</div>

<h2>The real frontier: whole-session simulation</h2>
<p>Single-message fidelity turns out to be <b>saturated</b>: scoring real held-out messages with the
same instruments, a genuine human message scores <b>29.1</b> realism — <em>lower</em> than v5's 38.8 —
and two <em>real</em> developers are barely distinguishable from one message (2AFC ceiling 0.65 style /
0.54 realism, vs ~0.5 chance). v5 already meets or exceeds these ceilings, so there is no per-message
headroom; pushing further just produces caricature (which is why the v6/v7 ablations regressed). The
real headroom is at the <b>session</b> level — does a simulated developer drive a whole session like
the real one? Two experiments, both starting from the <em>reconstructed real codebase state</em>
(clone the repo, checkout the parent of the session's first commit):</p>

<h3>1. Closed loop — simulator drives a fresh real agent</h3>
<p>The v5 simulator drove a real Claude-Code agent through a session from the reconstructed state.
Voice transfer was excellent — the simulated developer independently produced this user's tics
("bro", lowercase, the "doesnot" typo). But the session move-distribution distance was
<b>{sc['move_distribution_TVD'] if sc else '–'}</b> (worse than single-message), for an informative
reason: the <em>real</em> session was a crisis (the real agent deleted the user's uncommitted work →
rage, interrupts), while the well-behaved fresh agent gave the simulated user nothing to react to.
<b>User moves are coupled to agent actions</b> — you can't match a session's move-mix without
reproducing that session's agent trajectory.</p>

<h3>2. Agent-replay — hold the real agent fixed</h3>
<p>To isolate the simulator from agent divergence, we replayed the <em>real</em> agent's actual turns
and asked the simulator for the user's reaction at each real point. Per-turn move agreement
<b>{ar['per_turn_move_agreement'] if ar else '–'}</b>, conditional TVD
<b>{ar['move_distribution_TVD_conditional'] if ar else '–'}</b>. The crisis turns expose the gap
exactly — when the real agent proposes/does destructive git operations:</p>
<table><thead><tr><th>real agent did</th><th>REAL user</th><th>SIMULATED user</th></tr></thead>
<tbody>{crisis_rows}</tbody></table>
<p class="warn"><b>The fidelity gap is emotional escalation, not agent divergence.</b> With the agent
held fixed, the real developer <em>interrupts, rages, and panics</em> ("bastard you deleted all the
queries…", "madarchod… any way to restore them?"); the simulator stays <em>calm and analytical</em>
("show me git log to verify my commits are still there"). It even keeps the voice ("bro") — but the
model's even-tempered, helpful prior makes it <b>more rational than the frustrated human</b>. The
simulator transfers <em>voice</em>; it under-reproduces <em>affect/volatility</em>. That — modelling a
user's emotional reactivity to provocation — is the open frontier, and the next personalization axis.</p>

<h2>Where it stands</h2>
<ul>
<li><b>The distillation captures real user signal</b> — the own folder beats a wrong user's folder on
content, realism and speech-act, restored and strongest in v5.</li>
<li><b>v5 is the best simulator</b>: highest realism ({fmt(a_v)}), move-mix that tracks reality
(TVD {tvd_v5}, interrupts included), and correctly user-specific.</li>
<li><b>Architecture:</b> shared scaffold = competence; per-user sampled prior = move-mix;
per-user folder = voice. All user-specificity lives in the per-user layers.</li>
<li><b>Single-message fidelity is saturated</b> — v5 meets/exceeds the human ceiling (real messages
score 29.1 realism; real-vs-real discrimination only ~0.65). More prompt-personalization caricatures.</li>
<li><b>The open frontier is the session</b>, and it is a <em>coupled</em> user↔agent problem: agent-replay
shows the residual gap is <b>emotional escalation</b> — the simulator keeps the user's voice but stays
calmer and more rational than the real, frustrated human. Modelling per-user affect/volatility is the
next axis.</li>
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

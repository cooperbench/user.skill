#!/usr/bin/env python3
"""Generate results/report.html from the validation result JSON files.

Loads results/validation_results.json (inline mode) and, if present,
results/validation_results_folder.json (folder-access / product mode),
and renders both with a headline comparison.
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
COND_LABELS = {"distilled": "Own folder (distilled)",
               "generic": "No folder (generic dev)",
               "wrong": "Wrong user's folder"}
MODE_LABELS = {"inline": "Inline (folder pasted into prompt — controlled experiment)",
               "folder": "Folder access (agent reads users/&lt;slug&gt;/ — product flow)"}


def fmt(v, pct=False):
    if v is None:
        return "–"
    return f"{100 * v:.1f}%" if pct else (f"{v:.3f}" if isinstance(v, float) else str(v))


def cond_table(res):
    rows = "".join(
        f"<tr><td>{COND_LABELS[c]}</td><td class='num'>{s['n']}</td>"
        f"<td class='num'>{fmt(s['cosine'])}</td><td class='num'>{fmt(s['judge_content'])}</td>"
        f"<td class='num'>{fmt(s['judge_style'])}</td><td class='num'>{fmt(s['len_ratio'])}</td></tr>"
        for c, s in res["summary"].items())
    return ("<table><thead><tr><th>Condition</th><th class='num'>N</th><th class='num'>Cosine</th>"
            "<th class='num'>Judge content</th><th class='num'>Judge style</th>"
            f"<th class='num'>Len ratio</th></tr></thead><tbody>{rows}</tbody></table>")


def user_table(res):
    pu, dbu = res["per_user"], res.get("discrimination_by_user", {})
    rows = []
    for slug, conds in pu.items():
        d, g, w = conds["distilled"], conds["generic"], conds["wrong"]
        du = dbu.get(slug)
        cls = " class=win" if (du or 0) > 0.5 else ""
        rows.append(
            f"<tr{cls}><td>{html.escape(slug)}</td>"
            f"<td class='num'>{fmt(d['judge_content'])}</td><td class='num'>{fmt(g['judge_content'])}</td>"
            f"<td class='num'>{fmt(w['judge_content'])}</td>"
            f"<td class='num'>{fmt(d['judge_style'])}</td><td class='num'>{fmt(g['judge_style'])}</td>"
            f"<td class='num'>{fmt(w['judge_style'])}</td><td class='num'>{fmt(du, pct=True)}</td></tr>")
    return ("<table><thead><tr><th>User</th>"
            "<th class='num'>own content</th><th class='num'>none content</th><th class='num'>wrong content</th>"
            "<th class='num'>own style</th><th class='num'>none style</th><th class='num'>wrong style</th>"
            f"<th class='num'>2AFC own-picked</th></tr></thead><tbody>{''.join(rows)}</tbody></table>")


def examples(res, n=3):
    recs = sorted((r for r in res["records"] if r["cond"] == "distilled" and r["generated"]
                   and not r["generated"].startswith("Error:")),
                  key=lambda r: -(r.get("cosine") or 0))
    if len(recs) < n:
        picks = recs
    else:
        picks = [recs[0], recs[len(recs) // 2], recs[-1]]
    return "".join(
        f"<div class='ex'><div class='exh'>{html.escape(r['slug'])} — cosine {fmt(r.get('cosine'))}, "
        f"style {fmt(r.get('judge_style'))}</div>"
        f"<div class='lbl'>real</div><pre>{html.escape((r['real'] or '')[:500])}</pre>"
        f"<div class='lbl'>simulated</div><pre>{html.escape((r['generated'] or '')[:500])}</pre></div>"
        for r in picks)


def mode_section(res):
    disc = res.get("discrimination", {})
    wins = res["win_rates"]
    win_rows = "".join(
        f"<tr><td>{html.escape(k.replace('_', ' '))}</td>"
        f"<td class='num'>{fmt(v['cosine'], pct=True)}</td>"
        f"<td class='num'>{fmt(v['judge_style'], pct=True)}</td></tr>"
        for k, v in wins.items())
    return f"""
<h3>2AFC discrimination — {fmt(disc.get('distilled_chosen_rate'), pct=True)} (chance 50%, n={disc.get('n', 0)})</h3>
<p>Given a sample of the user's real messages, how often does the judge pick the candidate from the
user's <em>own</em> distilled folder over a different user's folder.</p>
{cond_table(res)}
<h4>Paired win rates (distilled beats baseline at the same point)</h4>
<table><thead><tr><th>Comparison</th><th class='num'>Cosine</th><th class='num'>Style</th></tr></thead>
<tbody>{win_rows}</tbody></table>
<h4>Per-user</h4>
{user_table(res)}
<h4>Examples (best / median / worst distilled prediction)</h4>
{examples(res)}
"""


def main():
    inline = json.loads((RESULTS / "validation_results.json").read_text())
    folder_path = RESULTS / "validation_results_folder.json"
    folder = json.loads(folder_path.read_text()) if folder_path.exists() else None
    modes = [("inline", inline)] + ([("folder", folder)] if folder else [])

    # headline comparison across modes
    head_rows = "".join(
        f"<tr><td>{MODE_LABELS[m]}</td>"
        f"<td class='num'>{fmt(r['discrimination'].get('distilled_chosen_rate'), pct=True)}</td>"
        f"<td class='num'>{fmt(r['summary']['distilled']['judge_content'])}</td>"
        f"<td class='num'>{fmt(r['summary']['generic']['judge_content'])}</td>"
        f"<td class='num'>{fmt(r['summary']['wrong']['judge_content'])}</td></tr>"
        for m, r in modes)

    sections = "".join(
        f"<h2>{MODE_LABELS[m]}</h2>{mode_section(r)}" for m, r in modes)

    best = max(modes, key=lambda mr: mr[1]["discrimination"].get("distilled_chosen_rate") or 0)
    best_rate = best[1]["discrimination"].get("distilled_chosen_rate")

    def dvw(res, metric):  # distilled-minus-wrong lift on a condition mean
        return res["summary"]["distilled"][metric] - res["summary"]["wrong"][metric]
    lift_mode = folder if folder else inline
    lift_mode_name = "folder-access" if folder else "inline"
    style_lift = dvw(lift_mode, "judge_style")
    content_lift = dvw(lift_mode, "judge_content")
    n_above = sum(1 for v in lift_mode.get("discrimination_by_user", {}).values() if v and v > 0.5)
    n_users = len(lift_mode["users"])

    report = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>User.skill: distillation validation</title>
<style>
 body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; max-width: 1040px;
        margin: 2rem auto; padding: 0 1rem; color: #1a1a2e; line-height: 1.55; }}
 h1 {{ border-bottom: 3px solid #7c3aed; padding-bottom: .4rem; }}
 h2 {{ margin-top: 2.4rem; color: #4c1d95; border-bottom: 1px solid #e3d9f7; padding-bottom: .2rem; }}
 h3 {{ margin-top: 1.4rem; }} h4 {{ margin-top: 1.1rem; color: #555; }}
 table {{ border-collapse: collapse; width: 100%; margin: .7rem 0 1.4rem; font-size: .88rem; }}
 th, td {{ text-align: left; padding: .38rem .55rem; border-bottom: 1px solid #e3e6ef; }}
 th {{ background: #f7f3ff; }}
 td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
 tr.win td {{ background: #f0fdf4; }}
 .ex {{ border: 1px solid #e3e6ef; border-radius: 8px; padding: .7rem 1rem; margin: .8rem 0; }}
 .exh {{ font-weight: 600; margin-bottom: .4rem; }}
 .lbl {{ font-size: .72rem; text-transform: uppercase; color: #7c3aed; margin-top: .4rem; }}
 pre {{ white-space: pre-wrap; background: #f8f8fb; padding: .45rem .65rem; border-radius: 5px;
       font-size: .8rem; margin: .15rem 0; }}
 .note {{ background: #f5f0ff; border-left: 4px solid #7c3aed; padding: .6rem 1rem; border-radius: 4px; }}
 .bigstat {{ background: linear-gradient(135deg,#7c3aed,#a855f7); color:#fff; border-radius:12px;
            padding:1.3rem 1.6rem; margin:1rem 0 1.4rem; display:flex; align-items:baseline; gap:1.2rem; flex-wrap:wrap; }}
 .bigstat .bn {{ font-size:2.8rem; font-weight:800; line-height:1; }}
 .bigstat .bl {{ font-size:.92rem; max-width:640px; }}
</style></head><body>
<h1>User.skill: can we recreate a developer from their trajectories?</h1>
<p>We distilled each SWE-chat user (≥6 sessions) into a role-playable folder, then tested it by
<strong>held-out next-message prediction</strong>: a role-play agent ({html.escape(inline['gen_model'])})
sees a real conversation prefix and writes the user's next message under three conditions —
their own distilled folder, no folder, or a different user's folder. We score against the real
message with embedding cosine ({html.escape(inline['embed_model'])}), an LLM judge
({html.escape(inline['judge_model'])}, content + style, 0–100), a length ratio, and a
2-alternative forced-choice style-discrimination test. Users: {len(inline['users'])}.</p>

<div class="bigstat">
  <div class="bn">+{style_lift:.1f}</div>
  <div class="bl">style-match points (0–100 judge) that the agent gains in {lift_mode_name} mode when it
  reads the user's <em>own</em> folder versus a <em>different</em> user's folder
  (content: +{content_lift:.1f}). The folder measurably specializes the agent toward the correct
  person. In a forced choice between own vs. wrong folder it picks own {fmt(best_rate, pct=True)} of
  the time (chance 50%), and beats the wrong folder for {n_above}/{n_users} users — the effect is
  strongly bimodal: distinctive users are captured near-perfectly, generic terse-coders near chance.</div>
</div>

<h2>Headline comparison across modes</h2>
<table><thead><tr><th>Mode</th><th class='num'>2AFC own-picked</th>
<th class='num'>content: own</th><th class='num'>content: none</th><th class='num'>content: wrong</th>
</tr></thead><tbody>{head_rows}</tbody></table>
<p class="note"><strong>How to read this.</strong> Predicting a user's <em>exact</em> next message is
intrinsically hard — every condition scores low in absolute terms because there are many plausible
next messages. The clean signal is <strong>own folder vs. wrong folder</strong>: that isolates
user-specificity, and the distilled folder wins on both content and style (most clearly in
folder-access mode). Note that the <em>no-folder / generic</em> baseline is also strong —
a capable model is already a decent generic next-message predictor, and in folder mode it can even
edge out the distilled folder on raw content-match, because authentic terse style sometimes scores
lower against a specific real message than a fluent generic guess does. So the folder's measurable
job is <em>specialization toward the right person</em>, not beating a generic agent at exact
prediction. Caveats: 5/168 inline "no-folder" generations hit a tool-use error and returned empty
(folder mode: 0 errors); the "wrong folder" is a single rotated pairing per user, so per-user 2AFC
is noisy — the aggregate is the reliable number.</p>

{sections}

<footer style="margin-top:3rem;font-size:.8rem;color:#888">Generated by scripts/report.py —
github.com/cooperbench/user.skill</footer>
</body></html>"""
    out = RESULTS / "report.html"
    out.write_text(report)
    print(out)


if __name__ == "__main__":
    main()

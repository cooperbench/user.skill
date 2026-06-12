#!/usr/bin/env python3
"""Generate results/report.html from results/validation_results.json."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COND_LABELS = {"distilled": "Own folder (distilled)",
               "generic": "No folder (generic dev)",
               "wrong": "Wrong user's folder"}


def fmt(v, pct=False):
    if v is None:
        return "–"
    return f"{100 * v:.1f}%" if pct else f"{v:.3f}" if isinstance(v, float) else str(v)


def main():
    res = json.loads((ROOT / "results" / "validation_results.json").read_text())
    summary, wins, per_user = res["summary"], res["win_rates"], res["per_user"]

    cond_rows = "".join(
        f"<tr><td>{COND_LABELS[c]}</td><td class='num'>{s['n']}</td>"
        f"<td class='num'>{fmt(s['cosine'])}</td>"
        f"<td class='num'>{fmt(s['judge_content'])}</td>"
        f"<td class='num'>{fmt(s['judge_style'])}</td>"
        f"<td class='num'>{fmt(s['len_ratio'])}</td></tr>"
        for c, s in summary.items())

    win_rows = "".join(
        f"<tr><td>{html.escape(k.replace('_', ' '))}</td>"
        f"<td class='num'>{fmt(v['cosine'], pct=True)}</td>"
        f"<td class='num'>{fmt(v['judge_style'], pct=True)}</td></tr>"
        for k, v in wins.items())

    user_rows = []
    for slug, conds in per_user.items():
        d, g, w = conds["distilled"], conds["generic"], conds["wrong"]
        better = (d["cosine"] or 0) > (g["cosine"] or 0) and (d["cosine"] or 0) > (w["cosine"] or 0)
        user_rows.append(
            f"<tr{' class=win' if better else ''}><td>{html.escape(slug)}</td>"
            f"<td class='num'>{fmt(d['cosine'])}</td><td class='num'>{fmt(g['cosine'])}</td>"
            f"<td class='num'>{fmt(w['cosine'])}</td>"
            f"<td class='num'>{fmt(d['judge_style'])}</td><td class='num'>{fmt(g['judge_style'])}</td>"
            f"<td class='num'>{fmt(w['judge_style'])}</td></tr>")

    # qualitative examples: best/median/worst distilled points by cosine
    recs = sorted((r for r in res["records"] if r["cond"] == "distilled" and r["generated"]),
                  key=lambda r: -(r["cosine"] or 0))
    picks = [recs[0], recs[len(recs) // 2], recs[-1]] if len(recs) >= 3 else recs
    examples = "".join(
        f"<div class='ex'><div class='exh'>{html.escape(r['slug'])} — cosine {fmt(r['cosine'])}, "
        f"style {fmt(r['judge_style'])}</div>"
        f"<div class='lbl'>real</div><pre>{html.escape(r['real'][:600])}</pre>"
        f"<div class='lbl'>simulated</div><pre>{html.escape(r['generated'][:600])}</pre></div>"
        for r in picks)

    report = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>User.skill: distillation validation</title>
<style>
 body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; max-width: 1000px;
        margin: 2rem auto; padding: 0 1rem; color: #1a1a2e; line-height: 1.5; }}
 h1 {{ border-bottom: 3px solid #7c3aed; padding-bottom: .4rem; }}
 table {{ border-collapse: collapse; width: 100%; margin: .8rem 0 1.6rem; font-size: .9rem; }}
 th, td {{ text-align: left; padding: .4rem .6rem; border-bottom: 1px solid #e3e6ef; }}
 th {{ background: #f7f3ff; }}
 td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
 tr.win td {{ background: #f0fdf4; }}
 .ex {{ border: 1px solid #e3e6ef; border-radius: 8px; padding: .8rem 1rem; margin: 1rem 0; }}
 .exh {{ font-weight: 600; margin-bottom: .5rem; }}
 .lbl {{ font-size: .75rem; text-transform: uppercase; color: #7c3aed; margin-top: .5rem; }}
 pre {{ white-space: pre-wrap; background: #f8f8fb; padding: .5rem .7rem; border-radius: 5px;
       font-size: .82rem; margin: .2rem 0; }}
 .note {{ background: #f5f0ff; border-left: 4px solid #7c3aed; padding: .6rem 1rem; border-radius: 4px; }}
</style></head><body>
<h1>User.skill: distillation validation</h1>
<p>Held-out next-message prediction: a role-play agent ({html.escape(res['gen_model'])}) sees a real
conversation prefix and produces the user's next message under three conditions. Similarity to the
real message: embedding cosine ({html.escape(res['embed_model'])}), LLM judge
({html.escape(res['judge_model'])}) content/style 0–100, and length ratio.
Users validated: {len(res['users'])}.</p>

<h2>Results by condition</h2>
<table><thead><tr><th>Condition</th><th class='num'>N</th><th class='num'>Cosine</th>
<th class='num'>Judge: content</th><th class='num'>Judge: style</th><th class='num'>Len ratio</th></tr></thead>
<tbody>{cond_rows}</tbody></table>

<h2>Paired win rates (distilled beats baseline at the same prediction point)</h2>
<table><thead><tr><th>Comparison</th><th class='num'>Cosine win rate</th>
<th class='num'>Style win rate</th></tr></thead><tbody>{win_rows}</tbody></table>
<p class="note">The distillation is validated when the <em>own-folder</em> condition beats
<em>no folder</em> (the folder adds signal) and <em>wrong folder</em> (the signal is user-specific).
Win rates above 50% indicate user-specific signal was captured.</p>

<h2>Per-user cosine / judge-style by condition</h2>
<table><thead><tr><th>User</th><th class='num'>own cos</th><th class='num'>none cos</th>
<th class='num'>wrong cos</th><th class='num'>own style</th><th class='num'>none style</th>
<th class='num'>wrong style</th></tr></thead><tbody>{''.join(user_rows)}</tbody></table>
<p>Green rows: own folder beats both baselines on cosine.</p>

<h2>Examples (best / median / worst distilled prediction)</h2>
{examples}

<footer style="margin-top:3rem;font-size:.8rem;color:#888">Generated by scripts/report.py —
github.com/cooperbench/user.skill</footer>
</body></html>"""
    out = ROOT / "results" / "report.html"
    out.write_text(report)
    print(out)


if __name__ == "__main__":
    main()

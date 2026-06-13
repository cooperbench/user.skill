#!/usr/bin/env python3
"""Generate results/report.html from the validation result JSON files.

Prefers the dual-criterion rescored files (style + realism 2AFC, per-record realism):
  results/rescored_inline_9users.json   (inline mode)
  results/rescored_folder_9users.json   (folder-access mode)
falling back to results/validation_results.json / validation_results_folder.json.
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
COND_LABELS = {"distilled": "Own folder (distilled)",
               "generic": "No folder (generic dev)",
               "wrong": "Wrong user's folder"}
MODE_LABELS = {"inline": "Inline (folder pasted into prompt)",
               "folder": "Folder access (agent reads users/&lt;slug&gt;/)"}
CRIT_LABELS = {"style": "Style / recognizability", "realism": "Realism / fidelity"}


def fmt(v, pct=False):
    if v is None:
        return "–"
    return f"{100 * v:.1f}%" if pct else (f"{v:.1f}" if isinstance(v, float) else str(v))


def load(mode):
    rescored = RESULTS / f"rescored_{mode}_9users.json"
    if rescored.exists():
        return json.loads(rescored.read_text())
    fallback = (RESULTS / "validation_results.json" if mode == "inline"
                else RESULTS / f"validation_results_{mode}.json")
    return json.loads(fallback.read_text()) if fallback.exists() else None


def discs(res):
    """Return {criterion: rate} for whatever discrimination criteria the file has."""
    if res.get("discriminations"):
        return {k: v.get("distilled_chosen_rate") for k, v in res["discriminations"].items()}
    d = res.get("discrimination", {})
    return {"style": d.get("distilled_chosen_rate")}


def cond_table(res):
    rows = "".join(
        f"<tr><td>{COND_LABELS[c]}</td><td class='num'>{s['n']}</td>"
        f"<td class='num'>{fmt(s.get('judge_content'))}</td>"
        f"<td class='num'>{fmt(s.get('judge_style'))}</td>"
        f"<td class='num'>{fmt(s.get('judge_realism'))}</td>"
        f"<td class='num'>{fmt(s.get('cosine'))}</td></tr>"
        for c, s in res["summary"].items())
    return ("<table><thead><tr><th>Condition</th><th class='num'>N</th>"
            "<th class='num'>Content</th><th class='num'>Style</th>"
            "<th class='num'>Realism</th><th class='num'>Cosine</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>")


def user_table(res):
    pu = res["per_user"]
    dbu = res.get("discriminations_by_user", {})
    st_by, re_by = dbu.get("style", {}), dbu.get("realism", res.get("discrimination_by_user", {}))
    rows = []
    for slug, conds in pu.items():
        d, w = conds["distilled"], conds["wrong"]
        st, re = st_by.get(slug), re_by.get(slug)
        cls = " class=win" if (re or 0) > 0.5 else ""
        rows.append(
            f"<tr{cls}><td>{html.escape(slug)}</td>"
            f"<td class='num'>{fmt(d.get('judge_realism'))}</td>"
            f"<td class='num'>{fmt(w.get('judge_realism'))}</td>"
            f"<td class='num'>{fmt(st, pct=True)}</td>"
            f"<td class='num'>{fmt(re, pct=True)}</td></tr>")
    return ("<table><thead><tr><th>User</th>"
            "<th class='num'>own realism</th><th class='num'>wrong realism</th>"
            "<th class='num'>2AFC style</th><th class='num'>2AFC realism</th>"
            f"</tr></thead><tbody>{''.join(rows)}</tbody></table>")


def examples(res, n=3):
    recs = sorted((r for r in res["records"] if r["cond"] == "distilled" and r["generated"]
                   and not r["generated"].startswith("Error:")),
                  key=lambda r: -(r.get("judge_realism") or 0))
    picks = [recs[0], recs[len(recs) // 2], recs[-1]] if len(recs) >= 3 else recs
    return "".join(
        f"<div class='ex'><div class='exh'>{html.escape(r['slug'])} — realism {fmt(r.get('judge_realism'))}, "
        f"style {fmt(r.get('judge_style'))}</div>"
        f"<div class='lbl'>real</div><pre>{html.escape((r['real'] or '')[:500])}</pre>"
        f"<div class='lbl'>simulated</div><pre>{html.escape((r['generated'] or '')[:500])}</pre></div>"
        for r in picks)


def mode_section(res):
    dd = discs(res)
    return f"""
<h3>2AFC discrimination</h3>
<table><thead><tr><th>Criterion</th><th class='num'>distilled chosen</th></tr></thead>
<tbody>
<tr><td>{CRIT_LABELS['style']}</td><td class='num'>{fmt(dd.get('style'), pct=True)}</td></tr>
<tr><td>{CRIT_LABELS['realism']}</td><td class='num'>{fmt(dd.get('realism'), pct=True)}</td></tr>
</tbody></table>
<h4>Judge means by condition (0–100)</h4>
{cond_table(res)}
<h4>Per-user (realism, and both 2AFC criteria)</h4>
{user_table(res)}
<h4>Examples (best / median / worst by realism)</h4>
{examples(res)}
"""


def main():
    inline = load("inline")
    folder = load("folder")
    modes = [("inline", inline)] + ([("folder", folder)] if folder else [])

    head_rows = []
    for m, r in modes:
        dd = discs(r)
        s = r["summary"]
        head_rows.append(
            f"<tr><td>{MODE_LABELS[m]}</td>"
            f"<td class='num'>{fmt(dd.get('style'), pct=True)}</td>"
            f"<td class='num'>{fmt(dd.get('realism'), pct=True)}</td>"
            f"<td class='num'>{fmt(s['distilled'].get('judge_realism'))}</td>"
            f"<td class='num'>{fmt(s['wrong'].get('judge_realism'))}</td></tr>")

    sections = "".join(f"<h2>{MODE_LABELS[m]}</h2>{mode_section(r)}" for m, r in modes)

    # headline numbers (inline is the strongest discriminator)
    i_d = discs(inline)
    style_rate, realism_rate = i_d.get("style"), i_d.get("realism")
    fold_realism_d = folder["summary"]["distilled"].get("judge_realism") if folder else None
    inl_realism_d = inline["summary"]["distilled"].get("judge_realism")

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
 .twin {{ display:flex; gap:1rem; flex-wrap:wrap; margin:1rem 0 1.4rem; }}
 .bigstat {{ flex:1 1 300px; background: linear-gradient(135deg,#7c3aed,#a855f7); color:#fff;
            border-radius:12px; padding:1.2rem 1.4rem; }}
 .bigstat.alt {{ background: linear-gradient(135deg,#0ea5e9,#22d3ee); }}
 .bigstat .bn {{ font-size:2.6rem; font-weight:800; line-height:1; }}
 .bigstat .bt {{ font-size:.8rem; text-transform:uppercase; letter-spacing:.04em; opacity:.9; margin-bottom:.3rem; }}
 .bigstat .bl {{ font-size:.86rem; margin-top:.4rem; }}
</style></head><body>
<h1>User.skill: recognizable vs. realistic role-play</h1>
<p>We distilled each SWE-chat user (≥6 sessions) into a role-playable folder, then tested it by
held-out next-message prediction under three conditions (own folder / no folder / wrong user's
folder) and two generation modes (inline = folder pasted into the prompt; folder-access = the agent
reads <code>users/&lt;slug&gt;/</code> itself). We score with an LLM judge
({html.escape(inline['judge_model'])}) on three axes — content, <strong>style</strong>
(surface recognizability) and <strong>realism</strong> (plausible, in-character message judged by
intent and substance, <em>not</em> catchphrase mimicry) — plus a 2-alternative forced choice
(own vs. wrong folder) run under both a style and a realism criterion. 9 users; chance = 50%.</p>

<div class="twin">
  <div class="bigstat">
    <div class="bt">2AFC · style criterion</div>
    <div class="bn">{fmt(style_rate, pct=True)}</div>
    <div class="bl">how often the judge picks the own-folder message as more <em>recognizably</em> this
    user than a wrong user's message (inline mode). Inline wins this because it reproduces the user's
    signature phrases.</div>
  </div>
  <div class="bigstat alt">
    <div class="bt">2AFC · realism criterion</div>
    <div class="bn">{fmt(realism_rate, pct=True)}</div>
    <div class="bl">same test, but rewarding the more <em>plausible in-character</em> message and
    discounting phrase-parroting. The signal survives ({fmt(realism_rate, pct=True)} &gt; 50%) but
    shrinks — confirming part of the style win was caricature.</div>
  </div>
</div>

<p class="note"><strong>The headline.</strong> Predicting a user's exact next message is intrinsically
hard, so the signal is in the comparisons. Two things hold up: (1) the distilled folder beats a
<em>wrong</em> user's folder under every criterion — the distillation encodes genuinely user-specific
behaviour; (2) <strong>inline beats folder-access on both discrimination criteria</strong>, but
this is largely a <em>recognizability</em> effect — inline reproduces signature catchphrases
(e.g. one user's <code>"looks good whats next"</code> verbatim across unrelated turns), which a
discrimination judge rewards. On the per-record <strong>realism</strong> axis the ordering flips:
folder-access produces <em>more realistic</em> distilled messages ({fmt(fold_realism_d)} vs inline
{fmt(inl_realism_d)}). Realism is real but <em>not user-discriminative</em>: in folder-access mode
even the wrong folder scores realistic (the agent grounds in the live conversation), so a 2AFC can't
separate own from wrong on realism alone. <strong>Bottom line:</strong> inline is better at being
<em>recognizable as</em> the user; folder-access is better at being <em>realistic for</em> the user.
Discrimination tests measure the former; per-record realism/content measures the latter.</p>

<h2>Headline comparison across modes</h2>
<table><thead><tr><th>Mode</th><th class='num'>2AFC style</th><th class='num'>2AFC realism</th>
<th class='num'>realism: own</th><th class='num'>realism: wrong</th></tr></thead>
<tbody>{''.join(head_rows)}</tbody></table>

{sections}

<footer style="margin-top:3rem;font-size:.8rem;color:#888">Generated by scripts/report.py —
github.com/cooperbench/user.skill. 9-user subset; the distillation itself ran for all 99 users.</footer>
</body></html>"""
    out = RESULTS / "report.html"
    out.write_text(report)
    print(out)


if __name__ == "__main__":
    main()

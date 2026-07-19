#!/usr/bin/env python3
"""Render analysis/misprediction_report.json -> analysis/misprediction.html.

A self-contained HTML write-up of the misprediction / homogeneity study: the hypothesis, the
experiment catalog (E1-E7), and the current results (whatever cohort the JSON was computed over).
Regenerate after re-running scripts/misprediction.py on a larger cohort. Usage:

  python3 scripts/misprediction_report_html.py [report.json] [out.html]
"""

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IN = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "analysis" / "misprediction_report.json"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "analysis" / "misprediction.html"
CATS = ["approve", "critical", "directive", "inquiry"]


def esc(x):
    return html.escape(str(x)) if x is not None else "—"


def num(x, d=3):
    return f"{x:.{d}f}" if isinstance(x, (int, float)) else "—"


def fmt(n):
    return f"{n:,}" if isinstance(n, (int, float)) else str(n)


def pill(cat):
    # move-category chips, echoing the site's restrained zinc/indigo palette
    color = {"approve": "#16a34a", "critical": "#e11d48", "directive": "#6366f1",
             "inquiry": "#0ea5e9"}.get(cat, "#71717a")
    return f'<span class="mv" style="background:{color}14;color:{color}">{esc(cat)}</span>'


def signed(x, d=3, good_negative=True):
    if not isinstance(x, (int, float)):
        return "—"
    color = "#16a34a" if ((x < 0) == good_negative and abs(x) > 1e-9) else "#e11d48" if abs(x) > 1e-9 else "#71717a"
    return f'<span style="color:{color}">{x:+.{d}f}</span>'


def bar(value, vmax, label, sub="", color="#818cf8"):
    """A horizontal bar row in the site's Bars style (label / zinc-100 track / indigo fill)."""
    w = max(1.5, 100 * value / vmax) if vmax else 1.5
    return (f'<div class="barrow"><div class="barlab">{esc(label)}</div>'
            f'<div class="bartrack"><div class="barfill" style="width:{w:.1f}%;background:{color}"></div>'
            f'<div class="barval">{value:.3f}{f" <span>{esc(sub)}</span>" if sub else ""}</div></div></div>')


def main():
    r = json.loads(IN.read_text())
    src = r.get("sources", [])
    src_line = ", ".join(f"{s['file']} ({s['labelled']} labelled, {s.get('mode')})" for s in src)
    n_lab = r.get("n_move_labelled", 0)
    cohort_users = max((v.get("n_users", 0) for v in r["E3_variance_collapse"]["by_condition"].values()
                        if isinstance(v, dict)), default=0)
    smoke = n_lab < 300  # a real powered run has >1k labelled points; the 9-user smoke has ~160

    adj = r.get("E1_adjudication_summary")
    e2 = r["E2_marginal_confusion"]
    e3 = r["E3_variance_collapse"]["by_condition"]
    e4 = r["E4_median_regression"]["by_condition"]
    e5 = r["E5_decision_vs_surface"]
    worst = r.get("E1_worst_k", [])

    def stat(value, label, sub=""):
        return (f'<div class="stat"><div class="bn">{value}</div>'
                f'<div class="bl">{label}</div>{f"<div class=bs>{sub}</div>" if sub else ""}</div>')

    # ---- stat tiles (site StatCard style) ----
    tiles = stat(f"{cohort_users}", "developers", "held-out tasks/ cohort")
    tiles += stat(f"{fmt(n_lab)}", "labelled points", "move-classified")
    gen = e3.get("generic", {})
    if "spread_pred" in gen:
        tiles += stat(f'{num(gen["spread_pred"],2)}<span class="vs">vs {num(gen["spread_real"],2)}</span>',
                      "between-user move-mix spread", "predicted (generic) vs real")
    if adj:
        tiles += stat(f'{int(100*adj.get("homogeneity_share"))}%',
                      "worst misses are homogeneity-type", f'task-completion / generic (n={adj.get("n_adjudicated")})')
    tiles += stat(f'<span class="verdict">{esc(e5.get("verdict"))}</span>', "E5: decision vs. surface",
                  "does the folder change the decision?")

    # ---- E1 error-type summary table ----
    e1_html = ""
    if adj:
        cts = adj.get("error_type_counts", {})
        homog_types = {"task_completion_substitution", "generic_not_specific"}
        rows = "".join(
            f'<tr><td class="k">{esc(k)}{" <span class=flag>homogeneity</span>" if k in homog_types else ""}</td>'
            f'<td class="num">{v}</td></tr>'
            for k, v in sorted(cts.items(), key=lambda x: -x[1]))
        e1_html = (f'<table><thead><tr><th>error type</th><th class="num">count</th></tr></thead>'
                   f'<tbody>{rows}</tbody></table>')

    # ---- worst-K examples (site .conv grid) ----
    def wrow(x):
        adjc = ""
        if "error_type" in x:
            adjc = (f'<div class="who" style="margin-top:.3rem">→ <b>{esc(x.get("error_type"))}</b>'
                    f' · reasonable={esc(x.get("reasonable"))}</div>')
        return (f'<div class="cell"><div class="k">{esc(x["slug"])}</div>'
                f'<div class="who">realism {num(x.get("judge_realism") or 0,0)}</div></div>'
                f'<div class="cell real">{pill(x["real_cat"])}<div>{esc(x["real"][:200])}</div></div>'
                f'<div class="cell pred">{pill(x["pred_cat"])}<div>{esc(x["generated"][:200])}</div>{adjc}</div>')
    worst_html = ("".join(wrow(x) for x in worst[:12])) if worst else ""

    # ---- E2 marginal ----
    def esc_signed(x):
        if not isinstance(x, (int, float)):
            return "—"
        col = "#6366f1" if abs(x) > 0.001 else "#a1a1aa"
        return f'<span style="color:{col}">{x:+.3f}</span>'

    def e2_rows():
        out = ""
        for c, v in e2.get("by_condition", {}).items():
            pm = v.get("pred_minus_real", {})
            cells = "".join(f'<td class="num">{esc_signed(pm.get(k))}</td>' for k in CATS)
            out += (f'<tr><td class="k">{esc(c)}</td>{cells}'
                    f'<td class="num">{v.get("human->task")}→ / ←{v.get("task->human")}</td>'
                    f'<td class="num">{num(v.get("flow_sign_test_p"),3)}</td></tr>')
        return out

    # ---- E3 / E4 tables ----
    def e3_rows():
        out = ""
        for c, v in e3.items():
            if "spread_pred" not in v:
                continue
            out += (f'<tr><td class="k">{esc(c)}</td><td class="num">{v["n_users"]}</td>'
                    f'<td class="num">{num(v["spread_real"])}</td><td class="num">{num(v["spread_pred"])}</td>'
                    f'<td class="num">{signed(v["pred_minus_real"])}</td><td class="num">{num(v["perm_p"])}</td>'
                    f'<td>{"collapse ✓" if v["collapse"] else "—"}</td></tr>')
        return out

    def e4_rows():
        out = ""
        for c, v in e4.items():
            if "mean_pred_minus_real" not in v:
                continue
            out += (f'<tr><td class="k">{esc(c)}</td><td class="num">{v["n_users"]}</td>'
                    f'<td class="num">{num(v["mean_dist_to_median_real"])}</td>'
                    f'<td class="num">{num(v["mean_dist_to_median_pred"])}</td>'
                    f'<td class="num">{signed(v["mean_pred_minus_real"], good_negative=True)}</td>'
                    f'<td class="num">{num(v.get("wilcoxon_p"))}</td>'
                    f'<td>{"shrinks ✓" if v["shrinks_to_median"] else "—"}</td></tr>')
        return out

    def e5_rows():
        out = ""
        for c, v in e5.get("by_condition", {}).items():
            out += (f'<tr><td class="k">{esc(c)}</td><td class="num">{v.get("n_users")}</td>'
                    f'<td class="num">{num(v.get("move_dist_to_real"))}</td>'
                    f'<td class="num">{num(v.get("judge_style"),1)}</td>'
                    f'<td class="num">{num(v.get("judge_realism"),1)}</td>'
                    f'<td class="num">{num(v.get("judge_content"),1)}</td></tr>')
        return out

    banner = (f'<div class="callout warn"><b>Smoke run — underpowered.</b> {cohort_users} developers, '
              f'{n_lab} labelled points — enough to exercise the pipeline, not to conclude. Read E1/E5 '
              f'as indicative; treat E3/E4 p-values as not-yet-significant.</div>' if smoke else
              f'<div class="callout"><b>Powered run.</b> {cohort_users} developers · {fmt(n_lab)} '
              f'move-labelled held-out points from the in-repo <code>tasks/</code> cohort (no S3). '
              f'Folder mode is the product flow; inline mode is scored separately.</div>')

    # E3 bars: real vs predicted between-user spread, per condition (site Bars style)
    e3_items = [(c, v) for c, v in e3.items() if "spread_pred" in v]
    e3max = max([v["spread_real"] for _, v in e3_items] + [v["spread_pred"] for _, v in e3_items] + [0.01])
    e3_bars = ""
    if e3_items:
        e3_bars = bar(e3_items[0][1]["spread_real"], e3max, "real developers", "actual", "#3f3f46")
        for c, v in e3_items:
            e3_bars += bar(v["spread_pred"], e3max, f'predicted · {c}',
                           "p<.05" if v["perm_p"] < 0.05 else "", "#818cf8")

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SWESimBench — Misprediction &amp; Homogeneity</title>
<style>
 :root {{ --zinc900:#18181b; --zinc700:#3f3f46; --zinc600:#52525b; --zinc500:#71717a;
          --zinc400:#a1a1aa; --zinc200:#e4e4e7; --zinc100:#f4f4f5; --zinc50:#fafafa;
          --indigo:#6366f1; --indigo400:#818cf8; }}
 * {{ box-sizing: border-box; }}
 body {{ font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Roboto,sans-serif;
        background:var(--zinc50); color:var(--zinc900); line-height:1.55; margin:0;
        -webkit-font-smoothing:antialiased; }}
 main {{ max-width:56rem; margin:0 auto; padding:3.5rem 1.5rem; }}
 code {{ font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,monospace; font-size:.85em;
        background:var(--zinc100); padding:.05rem .3rem; border-radius:4px; }}
 nav {{ display:flex; align-items:center; justify-content:space-between; font-size:.875rem; }}
 nav .brand {{ font-weight:600; }}
 nav .links {{ display:flex; gap:1rem; align-items:center; color:var(--zinc500); }}
 nav .links a {{ color:var(--zinc500); text-decoration:none; }} nav .links a:hover {{ color:var(--zinc900); }}
 .pill {{ background:var(--zinc900); color:#fff; border-radius:5px; padding:.1rem .45rem; font-size:.72rem; font-weight:500; }}
 h1 {{ font-size:1.85rem; font-weight:600; letter-spacing:-.02em; margin:2rem 0 0; }}
 .lede {{ color:var(--zinc600); max-width:42rem; margin-top:.8rem; }}
 .meta {{ color:var(--zinc400); font-size:.8rem; margin-top:.7rem; }}
 .callout {{ margin-top:1.5rem; border:1px solid var(--zinc200); background:#fff; border-left:3px solid var(--indigo);
        border-radius:10px; padding:.75rem 1rem; font-size:.9rem; color:var(--zinc700); }}
 .callout.warn {{ border-left-color:#f59e0b; }}
 .cards {{ display:grid; grid-template-columns:repeat(2,1fr); gap:.75rem; margin-top:2rem; }}
 @media(min-width:720px) {{ .cards {{ grid-template-columns:repeat(5,1fr); }} }}
 .stat {{ border:1px solid var(--zinc200); background:#fff; border-radius:12px; padding:1rem 1.15rem; }}
 .stat .bn {{ font-size:1.9rem; font-weight:600; letter-spacing:-.02em; }}
 .stat .bn .vs {{ font-size:.9rem; font-weight:500; color:var(--zinc400); margin-left:.35rem; }}
 .stat .bn .verdict {{ font-size:1.1rem; text-transform:capitalize; }}
 .stat .bl {{ font-size:.82rem; font-weight:500; color:var(--zinc600); margin-top:.25rem; }}
 .stat .bs {{ font-size:.72rem; color:var(--zinc400); margin-top:.1rem; }}
 section {{ margin-top:3rem; }}
 .kicker {{ font-size:.72rem; font-weight:600; text-transform:uppercase; letter-spacing:.05em; color:var(--indigo); }}
 h2 {{ font-size:1.3rem; font-weight:600; letter-spacing:-.01em; margin:.25rem 0 0; }}
 h2 .tag {{ font-size:.72rem; font-weight:500; color:var(--zinc400); text-transform:none; letter-spacing:0; }}
 section p {{ color:var(--zinc600); margin-top:.6rem; }}
 ul {{ color:var(--zinc600); }} li {{ margin:.35rem 0; }}
 .hy {{ color:var(--zinc900); font-weight:600; }}
 table {{ border-collapse:collapse; width:100%; margin-top:1rem; font-size:.85rem; }}
 th, td {{ text-align:left; padding:.5rem .6rem; border-top:1px solid var(--zinc100); vertical-align:top; color:var(--zinc600); }}
 thead th {{ border-top:0; color:var(--zinc500); font-weight:600; font-size:.78rem; }}
 td.num, th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
 td.k {{ color:var(--zinc900); font-weight:500; }}
 .flag {{ display:inline-block; font-size:.7rem; padding:0 .35rem; border-radius:4px; background:#eef2ff; color:var(--indigo); }}
 .mv {{ display:inline-block; font-size:.64rem; text-transform:uppercase; letter-spacing:.03em;
        border-radius:4px; padding:.05rem .35rem; font-weight:700; }}
 .barrow {{ display:flex; align-items:center; gap:.75rem; margin:.35rem 0; }}
 .barlab {{ width:11rem; flex:none; text-align:right; font-size:.78rem; color:var(--zinc500); }}
 .bartrack {{ position:relative; height:1.5rem; flex:1; background:var(--zinc100); border-radius:5px; }}
 .barfill {{ height:1.5rem; border-radius:5px; }}
 .barval {{ position:absolute; inset:0 auto 0 .5rem; display:flex; align-items:center; font-size:.75rem;
        font-weight:500; color:var(--zinc700); font-variant-numeric:tabular-nums; }}
 .barval span {{ color:var(--indigo); margin-left:.3rem; font-weight:600; }}
 .conv {{ display:grid; grid-template-columns:6rem 1fr 1fr; gap:.5rem; margin-top:1rem; font-size:.82rem; }}
 .conv .h {{ font-weight:600; color:var(--zinc500); font-size:.75rem; }}
 .conv .who {{ color:var(--zinc400); font-size:.75rem; }}
 .conv .real {{ border-left:2px solid var(--zinc300,#d4d4d8); padding-left:.6rem; }}
 .conv .pred {{ border-left:2px solid var(--indigo400); padding-left:.6rem; }}
 .conv .cell {{ padding:.4rem .1rem; border-top:1px solid var(--zinc100); }}
 footer {{ margin-top:4rem; padding-top:1.5rem; border-top:1px solid var(--zinc200); color:var(--zinc400); font-size:.8rem; }}
</style></head><body><main>

<nav>
  <span class="brand">SWESimBench</span>
  <div class="links"><span class="pill">misprediction</span>
    <a href="https://swesimbench.vercel.app">v2 dataset</a>
    <a href="https://swesimbench.vercel.app/v1">v1 leaderboard →</a></div>
</nav>

<h1>Are the simulator's mispredictions <em>homogeneity</em>?</h1>
<p class="lede"><b>Hypothesis.</b> LLMs are trained to complete tasks, not to imitate humans — so
they are systematically homogeneous, defaulting to task-driving behaviour instead of deciding from
an individual developer's differences. If true, a user-simulator's errors should cluster on the
human, friction-y moves (pushing back, interrupting, asking, redirecting) and regress every
developer toward one "average" one.</p>
<p class="meta">Generated from <code>{esc(IN.name)}</code> · {esc(src_line)}</p>
{banner}

<div class="cards">{tiles}</div>

<section><div class="kicker">Method</div>
<h2>Three falsifiable claims</h2>
<p>Each held-out point carries the real next message plus a simulated one under three conditions —
<b>distilled</b> (the user's own folder), <b>generic</b> (no folder / pure task prior) and
<b>wrong</b> (a different user's folder). Every message is labelled with a conversational
<b>move</b>, folded to four categories: {pill("approve")} accept · {pill("critical")} assert
something is wrong · {pill("directive")} say what to do next · {pill("inquiry")} ask for an
answer.</p>
<ul>
<li><span class="hy">H1 — central attractor</span> <span class="flag">secondary</span> predictions
over-produce approve/directive, under-produce critical/inquiry. Prompt-sensitive (our simulator is
told not to default to approving), so descriptive here.</li>
<li><span class="hy">H2 — between-user variance collapse</span> <span class="flag">primary</span>
predicted per-user move-mixes are more alike than real ones.</li>
<li><span class="hy">H3 — regression to the median developer</span> <span class="flag">primary</span>
each user's predicted mix sits closer to the population average than their real mix.</li>
</ul></section>

<section><div class="kicker">E1 · direct audit</div>
<h2>Worst mispredictions <span class="tag">move mismatch × low realism, LLM-adjudicated</span></h2>
<p>The homogeneity signature is a high share of <b>task-completion substitution</b> (predicted
keep-going where the real developer did something individual) and <b>generic-not-specific</b>.</p>
{e1_html}
<div class="conv"><div class="h">developer</div><div class="h">REAL message</div><div class="h">SIMULATED prediction</div>
{worst_html}</div></section>

<section><div class="kicker">E2 · marginals</div>
<h2>Marginal skew &amp; move confusion <span class="tag">H1, descriptive</span></h2>
<p>Predicted-minus-real share per category, and net flow between human and task moves.
{esc(e2.get("note",""))}</p>
<table><thead><tr><th>condition</th>{"".join(f'<th class="num">{c}</th>' for c in CATS)}
<th class="num">human→task / ←</th><th class="num">sign p</th></tr></thead><tbody>
{e2_rows()}</tbody></table></section>

<section><div class="kicker">E3 · primary result</div>
<h2>Between-user variance collapse <span class="tag">H2</span></h2>
<p>Mean pairwise total-variation distance between developers' move-mixes. If the model captured
individual differences, predicted spread would match real spread; homogeneity predicts a
<b>narrower</b> predicted spread. Lower bar = developers look more alike.</p>
<div style="margin:1.2rem 0">{e3_bars}</div>
<table><thead><tr><th>condition</th><th class="num">users</th><th class="num">spread real</th>
<th class="num">spread pred</th><th class="num">Δ</th><th class="num">perm p</th><th>collapse?</th></tr></thead><tbody>
{e3_rows()}</tbody></table></section>

<section><div class="kicker">E4 · primary result</div>
<h2>Regression to the median developer <span class="tag">H3</span></h2>
<p>Distance from each user's mix to the population-average mix, real vs predicted. Shrinkage toward
the median (predicted closer than real) supports homogeneity. Wilcoxon signed-rank.</p>
<table><thead><tr><th>condition</th><th class="num">users</th><th class="num">dist→median real</th>
<th class="num">dist→median pred</th><th class="num">Δ</th><th class="num">wilcoxon p</th><th>shrinks?</th></tr></thead><tbody>
{e4_rows()}</tbody></table></section>

<section><div class="kicker">E5 · decision vs. surface</div>
<h2>Does the folder change the decision or only the voice?</h2>
<p>Verdict: <b>{esc(e5.get("verdict"))}</b>. {esc(e5.get("reading"))} <code>move dist→real</code> is
the move-mix distance to the real user (lower = better decisions); <code>judge style</code> is
surface voice.</p>
<table><thead><tr><th>condition</th><th class="num">users</th><th class="num">move dist→real</th>
<th class="num">judge style</th><th class="num">judge realism</th><th class="num">judge content</th></tr></thead><tbody>
{e5_rows()}</tbody></table></section>

<section><div class="kicker">Next</div>
<h2>Experiments still to run</h2>
<ul>
<li><b>E6 — underdetermination control.</b> Resample the generic simulator k× per point, drop
high-entropy (unpredictable) points, re-run E2–E5. Distribution-level claims should survive on the
determined subset — separating homogeneity from a low prediction ceiling.</li>
<li><b>E7 — causal probe.</b> Compare (i) default, (ii) an explicit "imitate THIS human, do not
optimise the task" instruction, and (iii) move-conditioned sampling from the user's real prior
(<code>validate.py --move-conditioned</code>). If (ii)/(iii) restore critical% and between-user
variance, the homogeneity is a prompt/objective artifact, not a capability ceiling.</li>
</ul></section>

<footer>Reproduce: <code>python3 scripts/misprediction.py --adjudicate</code> →
<code>python3 scripts/misprediction_report_html.py</code>. Part of SWESimBench.</footer>

</main></body></html>"""
    OUT.write_text(doc)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(doc)} bytes)")


if __name__ == "__main__":
    main()

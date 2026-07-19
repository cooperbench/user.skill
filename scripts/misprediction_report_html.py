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


def pill(cat):
    color = {"approve": "#16a34a", "critical": "#dc2626", "directive": "#7c3aed",
             "inquiry": "#0ea5e9"}.get(cat, "#666")
    return f'<span class="mv" style="background:{color}22;color:{color}">{esc(cat)}</span>'


def signed(x, d=3, good_negative=True):
    if not isinstance(x, (int, float)):
        return "—"
    color = "#16a34a" if ((x < 0) == good_negative and abs(x) > 1e-9) else "#991b1b" if abs(x) > 1e-9 else "#666"
    return f'<span style="color:{color}">{x:+.{d}f}</span>'


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

    # ---- stat tiles ----
    tiles = ""
    if adj:
        hs = adj.get("homogeneity_share")
        tiles += (f'<div class="stat up"><div class="bn">{int(100*hs)}%</div>'
                  f'<div class="bl">of worst misses are task-completion / generic substitution '
                  f'(homogeneity share, n={adj.get("n_adjudicated")})</div></div>')
        rr = adj.get("reasonable_rate")
        tiles += (f'<div class="stat"><div class="bn">{int(100*rr)}%</div>'
                  f'<div class="bl">of the worst misses are plausible-for-someone (reasonable rate)</div></div>')
    gen = e3.get("generic", {})
    if "spread_pred" in gen:
        tiles += (f'<div class="stat"><div class="bn">{num(gen["spread_pred"],2)} vs {num(gen["spread_real"],2)}</div>'
                  f'<div class="bl">between-user spread: predicted (generic) vs real move-mix</div></div>')
    tiles += (f'<div class="stat"><div class="bn" style="font-size:1.2rem">{esc(e5.get("verdict"))}</div>'
              f'<div class="bl">E5 verdict: does the folder move the decision or only the surface?</div></div>')

    # ---- E1 error-type table ----
    e1_html = ""
    if adj:
        cts = adj.get("error_type_counts", {})
        rows = "".join(f'<tr><td>{esc(k)}</td><td class="num">{v}</td></tr>'
                       for k, v in sorted(cts.items(), key=lambda x: -x[1]))
        e1_html = (f'<table><tr><th>error type</th><th class="num">count</th></tr>{rows}</table>'
                   f'<p class="legend">{esc(adj.get("reading"))}</p>')

    # ---- worst-K examples ----
    def wrow(x):
        adjc = ""
        if "error_type" in x:
            adjc = (f'<div class="legend">verdict: <b>{esc(x.get("error_type"))}</b> · '
                    f'reasonable={esc(x.get("reasonable"))}</div>')
        return (f'<tr><td class="ag">{esc(x["slug"])}<br><span class="legend">R{num(x.get("judge_realism") or 0,0)}</span></td>'
                f'<td class="ur">{pill(x["real_cat"])}<br>{esc(x["real"][:220])}</td>'
                f'<td class="us">{pill(x["pred_cat"])}<br>{esc(x["generated"][:220])}{adjc}</td></tr>')
    worst_html = ("".join(wrow(x) for x in worst[:12])) if worst else ""

    # ---- E2 marginal ----
    def esc_signed(x):
        if not isinstance(x, (int, float)):
            return "—"
        col = "#7c3aed" if abs(x) > 0.001 else "#999"
        return f'<span style="color:{col}">{x:+.3f}</span>'

    def e2_rows():
        out = ""
        for c, v in e2.get("by_condition", {}).items():
            pm = v.get("pred_minus_real", {})
            cells = "".join(f'<td class="num">{esc_signed(pm.get(k))}</td>' for k in CATS)
            out += (f'<tr><td>{esc(c)}</td>{cells}'
                    f'<td class="num">{v.get("human->task")}→ / ←{v.get("task->human")}</td>'
                    f'<td class="num">{num(v.get("flow_sign_test_p"),3)}</td></tr>')
        return out

    # ---- E3 / E4 tables ----
    def e3_rows():
        out = ""
        for c, v in e3.items():
            if "spread_pred" not in v:
                continue
            out += (f'<tr><td>{esc(c)}</td><td class="num">{v["n_users"]}</td>'
                    f'<td class="num">{num(v["spread_real"])}</td><td class="num">{num(v["spread_pred"])}</td>'
                    f'<td class="num">{signed(v["pred_minus_real"])}</td><td class="num">{num(v["perm_p"])}</td>'
                    f'<td>{"collapse ✓" if v["collapse"] else "—"}</td></tr>')
        return out

    def e4_rows():
        out = ""
        for c, v in e4.items():
            if "mean_pred_minus_real" not in v:
                continue
            out += (f'<tr><td>{esc(c)}</td><td class="num">{v["n_users"]}</td>'
                    f'<td class="num">{num(v["mean_dist_to_median_real"])}</td>'
                    f'<td class="num">{num(v["mean_dist_to_median_pred"])}</td>'
                    f'<td class="num">{signed(v["mean_pred_minus_real"], good_negative=True)}</td>'
                    f'<td class="num">{num(v.get("wilcoxon_p"))}</td>'
                    f'<td>{"shrinks ✓" if v["shrinks_to_median"] else "—"}</td></tr>')
        return out

    def e5_rows():
        out = ""
        for c, v in e5.get("by_condition", {}).items():
            out += (f'<tr><td>{esc(c)}</td><td class="num">{v.get("n_users")}</td>'
                    f'<td class="num">{num(v.get("move_dist_to_real"))}</td>'
                    f'<td class="num">{num(v.get("judge_style"),1)}</td>'
                    f'<td class="num">{num(v.get("judge_realism"),1)}</td>'
                    f'<td class="num">{num(v.get("judge_content"),1)}</td></tr>')
        return out

    smoke_banner = ("" if not smoke else
                    f'<div class="warn"><b>Smoke run — underpowered.</b> These numbers are from a '
                    f'{cohort_users}-user cohort ({n_lab} labelled points), enough to exercise the '
                    f'pipeline but not to conclude. Read E1/E5 as indicative; treat E3/E4 p-values as '
                    f'not-yet-significant.</div>')
    if not smoke:
        smoke_banner = (f'<div class="note"><b>Powered run.</b> {cohort_users} developers, {n_lab} '
                        f'move-labelled prediction points, drawn from the in-repo <code>tasks/</code> '
                        f'held-out cohort (no S3). Folder mode = the product flow; inline mode is '
                        f'scored separately.</div>')

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Misprediction & Homogeneity Study</title>
<style>
 body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; max-width: 1060px;
        margin: 2rem auto; padding: 0 1rem; color: #1a1a2e; line-height: 1.55; }}
 h1 {{ border-bottom: 3px solid #7c3aed; padding-bottom: .4rem; }}
 h2 {{ margin-top: 2.4rem; color: #4c1d95; border-bottom: 1px solid #e3d9f7; padding-bottom: .2rem; }}
 h3 {{ margin-top: 1.6rem; color: #4c1d95; }}
 table {{ border-collapse: collapse; width: 100%; margin: .7rem 0 1.2rem; font-size: .87rem; }}
 th, td {{ text-align: left; padding: .38rem .55rem; border-bottom: 1px solid #e3e6ef; vertical-align: top; }}
 th {{ background: #f7f3ff; }}
 td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
 .note {{ background: #f5f0ff; border-left: 4px solid #7c3aed; padding: .6rem 1rem; border-radius: 4px; }}
 .warn {{ background: #fff7ed; border-left: 4px solid #f0883e; padding: .6rem 1rem; border-radius: 4px; margin:1rem 0; }}
 .twin {{ display:flex; gap:1rem; flex-wrap:wrap; margin:1rem 0; }}
 .stat {{ flex:1 1 180px; background:#f0f4ff; border-radius:10px; padding:.9rem 1.1rem; }}
 .stat .bn {{ font-size:1.7rem; font-weight:800; color:#4361ee; }}
 .stat.up .bn {{ color:#16a34a; }} .stat .bl {{ font-size:.8rem; color:#555; }}
 .legend {{ font-size:.78rem; color:#666; margin:.2rem 0; }}
 .mv {{ display:inline-block; font-size:.66rem; text-transform:uppercase; border-radius:3px; padding:0 5px; margin-bottom:3px; font-weight:700; }}
 table.sess td {{ font-size:.82rem; }}
 table.sess td.ag {{ background:#f6f6fb; color:#666; font-size:.76rem; width:10%; }}
 table.sess td.ur {{ width:45%; background:#fbf7ff; border-left:3px solid #7c3aed; }}
 table.sess td.us {{ width:45%; background:#f0f9ff; border-left:3px solid #0ea5e9; }}
 code {{ background:#f2eefc; padding:0 .3rem; border-radius:3px; font-size:.85em; }}
 .hy {{ font-weight:600; color:#4c1d95; }}
</style></head><body>

<h1>Are the simulator's mispredictions <em>homogeneity</em>?</h1>
<p><b>Hypothesis.</b> LLMs are trained to complete tasks, not to imitate humans, so they are
systematically homogeneous — defaulting to task-driving behaviour instead of deciding from an
individual developer's differences. If true, a user-simulator's errors should cluster on the
human, individual moves (pushing back, interrupting, asking, redirecting) and regress everyone
toward one "average developer".</p>

<p class="legend">Generated from <code>{esc(IN.name)}</code> · sources: {esc(src_line)} ·
{n_lab} move-labelled prediction points.</p>
{smoke_banner}

<div class="twin">{tiles}</div>

<h2>Method</h2>
<p>Each held-out point has the real next message plus a simulated one under three conditions —
<b>distilled</b> (the user's own folder), <b>generic</b> (no folder / pure task prior), and
<b>wrong</b> (a different user's folder). Every message is labelled with a conversational
<b>move</b>, folded to four categories: {pill("approve")} accept/permit · {pill("critical")}
assert something is wrong · {pill("directive")} tell the agent what to do next · {pill("inquiry")}
ask for an answer. The hypothesis becomes three falsifiable claims:</p>
<ul>
<li><span class="hy">H1 — central attractor (secondary).</span> Predictions over-produce
approve/directive and under-produce critical/inquiry. <em>Prompt-sensitive:</em> our simulator is
told "do NOT default to approving", so on the product simulator this is descriptive, not a clean test.</li>
<li><span class="hy">H2 — between-user variance collapse (primary).</span> Predicted per-user
move-mixes are more alike than real ones — the model doesn't spread across individuals.</li>
<li><span class="hy">H3 — regression to the median developer (primary).</span> Each user's
predicted mix sits closer to the population average than their real mix does.</li>
</ul>

<h2>E1 — worst-K misprediction audit</h2>
<p>The worst mispredictions (move mismatch × low realism), each LLM-adjudicated for whether the
prediction was <em>reasonable-for-someone</em> and what kind of error it is. The homogeneity
signature is a high share of <b>task-completion substitution</b> (predicted keep-going where the
real developer did something individual) and <b>generic-not-specific</b>.</p>
{e1_html}
<table class="sess"><tr><th>user</th><th>REAL developer message</th><th>SIMULATED prediction</th></tr>
{worst_html}
</table>

<h2>E2 — marginal skew &amp; move confusion <span class="legend">(H1, descriptive)</span></h2>
<p>Predicted-minus-real share per category, and net flow between human and task moves.
{esc(e2.get("note",""))}</p>
<table><tr><th>condition</th>{"".join(f'<th class="num">{c}</th>' for c in CATS)}
<th class="num">human→task / task→human</th><th class="num">sign p</th></tr>
{e2_rows()}</table>

<h2>E3 — between-user variance collapse <span class="legend">(H2, primary)</span></h2>
<p>Mean pairwise total-variation distance between users' move-mixes. Hypothesis: predicted spread
&lt; real spread (predictions cluster). Paired permutation test.</p>
<table><tr><th>condition</th><th class="num">users</th><th class="num">spread real</th>
<th class="num">spread pred</th><th class="num">Δ (pred−real)</th><th class="num">perm p</th><th>collapse?</th></tr>
{e3_rows()}</table>

<h2>E4 — regression to the median developer <span class="legend">(H3, primary)</span></h2>
<p>Distance from each user's mix to the population-average mix, real vs predicted. Hypothesis:
predicted is closer to the median (shrinkage). Wilcoxon signed-rank.</p>
<table><tr><th>condition</th><th class="num">users</th><th class="num">dist→median real</th>
<th class="num">dist→median pred</th><th class="num">Δ (pred−real)</th><th class="num">wilcoxon p</th><th>shrinks?</th></tr>
{e4_rows()}</table>

<h2>E5 — decision vs. surface</h2>
<p>Does the distilled folder change the <em>decision</em> (move-mix distance to the real user) or
only the <em>surface</em> (judge style)? <b>{esc(e5.get("verdict"))}</b> —
{esc(e5.get("reading"))}</p>
<table><tr><th>condition</th><th class="num">users</th><th class="num">move dist→real</th>
<th class="num">judge style</th><th class="num">judge realism</th><th class="num">judge content</th></tr>
{e5_rows()}</table>

<h2>Experiment catalog &amp; next steps</h2>
<p>E1–E5 above run offline over the validation records. Two more, needing new generation, remain:</p>
<ul>
<li><b>E6 — underdetermination control.</b> Resample the generic simulator k× per point; drop
high-entropy (unpredictable) points and re-run E2–E5. The distribution-level claims (H2/H3) should
survive on the determined subset — that separates homogeneity from a low prediction ceiling.</li>
<li><b>E7 — causal probe.</b> Compare the simulator under (i) default, (ii) an explicit "imitate
THIS human, do not optimise the task" instruction, and (iii) move-conditioned sampling from the
user's real prior (<code>validate.py --move-conditioned --move-source sample</code>). If (ii)/(iii)
restore critical% and between-user variance, the homogeneity is an objective/prompt artifact, not a
capability ceiling — the strongest test of the mechanism in the hypothesis.</li>
</ul>
<div class="note">Reproduce: <code>python3 scripts/misprediction.py --adjudicate</code> then
<code>python3 scripts/misprediction_report_html.py</code>. Point <code>--results</code> at the
~57-user <code>validation_results*.json</code> for the powered result.</div>

</body></html>"""
    OUT.write_text(doc)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(doc)} bytes)")


if __name__ == "__main__":
    main()

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import misprediction_figs as FIGS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IN = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "analysis" / "misprediction_report.json"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "analysis" / "misprediction.html"
# optional 3rd arg: a second-mode report (e.g. inline) to render a folder-vs-inline comparison.
CMP = Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "analysis" / "misprediction_inline_report.json"
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
    a_best = r.get("A_move_accuracy", {}).get("by_condition", {}).get("distilled", {}) if r.get("A_move_accuracy") else {}
    if a_best.get("skill") is not None:
        tiles += stat(f'{a_best["skill"]:+.1f}', "skill score (distilled)",
                      "0 = majority-class predictor, 100 = perfect")
    tiles += stat(f'<span class="verdict">{esc(e5.get("verdict"))}</span>', "E5: decision vs. surface",
                  "does the folder change the decision?")

    # ---- E1 error-type summary table ----
    # Definitions mirror ADJUDICATE_PROMPT in scripts/misprediction.py — keep in sync.
    ERROR_TYPES = [
        ("task_completion_substitution", True,
         "predicted a keep-going / approve / new-task move where the real developer pushed back, "
         "interrupted, or redirected"),
        ("generic_not_specific", True,
         "the right <em>kind</em> of move, but not how <em>this</em> developer would have made it"),
        ("hallucinated_content", False,
         "invents facts or requests that are not grounded in the session"),
        ("underdetermined", False,
         "both messages are equally plausible — the real one was genuinely unpredictable"),
        ("other", False, "anything else"),
    ]
    e1_html = ""
    if adj:
        cts = adj.get("error_type_counts", {})
        homog_types = {k for k, h, _ in ERROR_TYPES if h}
        defs = "".join(
            f'<li><b>{esc(k)}</b>{" <span class=flag>homogeneity</span>" if h else ""} — {d}</li>'
            for k, h, d in ERROR_TYPES)
        rows = "".join(
            f'<tr><td class="k">{esc(k)}{" <span class=flag>homogeneity</span>" if k in homog_types else ""}</td>'
            f'<td class="num">{v}</td></tr>'
            for k, v in sorted(cts.items(), key=lambda x: -x[1]))
        e1_html = (
            '<p>An adjudicator labels each miss with one error type. The two marked '
            '<span class="flag">homogeneity</span> are the ones that indicate a failure of '
            '<em>individuation</em> — the prediction is reasonable for <em>some</em> developer, just '
            'not this one; the rest are ordinary failure modes.</p>'
            f'<ul class="defs">{defs}</ul>'
            f'<table><thead><tr><th>error type</th><th class="num">count</th></tr></thead>'
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

    e8b = (r.get("E8_within_developer_spread") or {}).get("by_condition", {})
    def e8_rows():
        out = ""
        for c, v in e8b.items():
            out += (f'<tr><td class="k">{esc(c)}</td><td class="num">{v["n_users"]}</td>'
                    f'<td class="num">{num(v["entropy_real"],3)}</td>'
                    f'<td class="num">{num(v["entropy_pred"],3)}</td>'
                    f'<td class="num">{signed(v["mean_delta"])}</td>'
                    f'<td class="num">{v["n_narrower"]}/{v["n_users"]}</td>'
                    f'<td class="num">{num(v.get("wilcoxon_p"),4)}</td></tr>')
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
              f'<div class="callout"><b>Data.</b> {cohort_users} developers · {fmt(n_lab)} '
              f'move-labelled held-out points from the in-repo <code>tasks/</code> cohort (no S3). '
              f'Folder mode = the agent reads the folder itself; inline pastes it into the prompt.</div>')

    # E3 bars: real vs predicted between-user spread, per condition (site Bars style)
    e3_items = [(c, v) for c, v in e3.items() if "spread_pred" in v]
    e3max = max([v["spread_real"] for _, v in e3_items] + [v["spread_pred"] for _, v in e3_items] + [0.01])
    e3_bars = ""
    if e3_items:
        e3_bars = bar(e3_items[0][1]["spread_real"], e3max, "real developers", "actual", "#3f3f46")
        for c, v in e3_items:
            e3_bars += bar(v["spread_pred"], e3max, f'predicted · {c}',
                           "p<.05" if v["perm_p"] < 0.05 else "", "#818cf8")

    # primary report is this_mode; the optional compare report is the other mode
    this_mode = (r.get("sources") or [{}])[0].get("mode", "folder")
    cr = None
    cmode = None
    if CMP.exists() and CMP.resolve() != IN.resolve():
        cr = json.loads(CMP.read_text())
        cmode = (cr.get("sources") or [{}])[0].get("mode", "inline")

    folder_rep = r if this_mode == "folder" else cr
    inline_rep = cr if this_mode == "folder" else r
    figs = FIGS.build_figures(folder_rep or r, inline_rep)
    figure = lambda k: (f'<figure class="fig">{figs[k]}</figure>' if figs.get(k) else "")

    # ---- metrics primer: the three families every experiment is expressed in ----
    a_f = r.get("A_move_accuracy")
    a_rows = ""
    if a_f:
        for c, v in a_f.get("by_condition", {}).items():
            sk = v.get("skill")
            a_rows += (f'<tr><td class="k">{esc(c)}</td><td class="num">{v["n"]}</td>'
                       f'<td class="num"><b>{sk:+.1f}</b></td>'
                       f'<td class="num">{num(v["accuracy"],3)}</td>'
                       f'<td class="num">{signed(v["vs_baseline"], good_negative=False)}</td>'
                       f'<td>{"beats baseline" if v["beats_baseline"] else "below baseline"}</td></tr>')
    metrics_section = (
        '<section><div class="kicker">Metrics</div>'
        '<h2>Three families of measurement</h2>'
        '<p>Every experiment below is expressed in one of three metric families. Naming them up front '
        'makes it explicit what each claim is actually measuring — and they can disagree.</p>'
        '<ul class="defs">'
        '<li><b>A · individual-level accuracy</b> — per held-out point, does the predicted <em>move</em> '
        'equal the real move? Reported as a <b>skill score</b> '
        '<code>S = (acc − acc_base)/(1 − acc_base)</code> ×100, normalised against the '
        'majority-class predictor: <b>0</b> = no better than always guessing the most common move, '
        '<b>100</b> = perfect, <b>negative</b> = worse than that constant predictor. Raw accuracy is not '
        'comparable across cohorts with different class balance; skill is.</li>'
        '<li><b>B · population-level distribution</b> — total-variation distance (TVD) between two move '
        '<em>distributions</em>: between two developers, between one developer and their own prediction, '
        'or between the whole real population and the whole predicted population. Says nothing about any '
        'individual turn.</li>'
        '<li><b>C · LLM-as-a-judge</b> — a judge scores each predicted message against the real one for '
        '<em>style</em> (surface voice) and <em>content</em> (intent/substance), plus realism.</li>'
        '</ul>'
        + figure('A')
        + (('<p style="margin-top:1rem"><b>Metric A, measured.</b> Skill score against the '
            f'majority-class baseline (always predict <code>{esc(a_f["baseline_class"])}</code> = '
            f'{num(a_f["baseline_accuracy"],3)}). The real move distribution is heavily skewed, so this '
            'baseline is the bar that matters — and no condition clears it:</p>'
            '<table><thead><tr><th>condition</th><th class="num">n</th><th class="num">skill (0–100)</th>'
            '<th class="num">raw accuracy</th><th class="num">vs baseline</th><th>verdict</th></tr></thead>'
            f'<tbody>{a_rows}</tbody></table>') if a_f else '')
        + '</section>')

    # ---- claims scoreboard: each experiment's falsifiable prediction vs. what we measured ----
    def _ev(rep):
        """Pull the evidence each claim is judged on, from one mode's report."""
        if not rep:
            return None
        e3b = rep["E3_variance_collapse"]["by_condition"]
        e4b = rep["E4_median_regression"]["by_condition"]
        return {
            "e2": rep["E2_marginal_confusion"]["by_condition"].get("generic", {}).get("pred_minus_real", {}),
            "e3": e3b.get("generic", {}), "e3all": e3b,
            "e4": e4b.get("distilled", {}), "e4gen": e4b.get("generic", {}),
            "e5": rep["E5_decision_vs_surface"].get("verdict"),
            "e8": (rep.get("E8_within_developer_spread") or {}).get("by_condition", {}).get("distilled"),
            "e1": (rep.get("E1_adjudication_summary") or {}).get("homogeneity_share"),
        }

    VERDICT_CLS = {"supported": "v-yes", "refuted": "v-no", "mixed": "v-mix", "not run": "v-na"}

    def scoreboard_rows(fev, iev):
        rows = []
        # E1 — worst misses are homogeneity-type
        rows.append(("E1 <span class='mfam'>A+C</span>", "Worst misses are task-completion / generic substitution",
                     f'{int(100*fev["e1"])}%' if fev and fev.get("e1") is not None else "—",
                     f'{int(100*iev["e1"])}%' if iev and iev.get("e1") is not None else "—",
                     "supported",
                     "<b>A+C:</b> misses are ranked by move mismatch (A) weighted by low judge-realism (C), then labelled. Both modes: the dominant error is predicting keep-going where the developer did something individual."))
        # H1/E2 — approve up, critical down
        f2, i2 = (fev or {}).get("e2", {}), (iev or {}).get("e2", {})
        rows.append(("H1 · E2 <span class='mfam'>B</span>", "approve% pred &gt; real and critical% pred &lt; real",
                     f'approve {f2.get("approve",0):+.3f}, critical {f2.get("critical",0):+.3f}',
                     f'approve {i2.get("approve",0):+.3f}, critical {i2.get("critical",0):+.3f}',
                     "mixed",
                     "<b>B:</b> compares the whole real population's move distribution to the whole predicted one. Holds on the low-prompt inline arm (clear approve-collapse). In folder mode the simulator is "
                     "explicitly told not to default to approving, so the mass diverts to inquiry instead — as the "
                     "plan predicted, H1 is only clean on a low-prompt baseline."))
        # H2/E3 — spread collapse
        f3, i3 = (fev or {}).get("e3", {}), (iev or {}).get("e3", {})
        rows.append(("H2 · E3 <span class='mfam'>B</span>", "between-user spread(pred) &lt; spread(real)",
                     f'{num(f3.get("spread_pred"),3)} vs {num(f3.get("spread_real"),3)} (p={num(f3.get("perm_p"),3)})',
                     f'{num(i3.get("spread_pred"),3)} vs {num(i3.get("spread_real"),3)} (p={num(i3.get("perm_p"),3)})',
                     "supported",
                     "<b>B:</b> mean pairwise TVD between <em>developers'</em> move distributions, predicted vs real. Significant in folder mode. Inline masks it: pasting the folder in makes the "
                     "model echo signature catchphrases verbatim, which inflates apparent between-user distinctiveness."))
        # H3/E4 — shrinkage toward the median
        f4, i4 = (fev or {}).get("e4", {}), (iev or {}).get("e4", {})
        # H4/E8 — within-developer collapse (the second half of the hypothesis)
        f8 = ((fev or {}).get("e8") or {})
        i8 = ((iev or {}).get("e8") or {})
        def _e8cell(v):
            if not v:
                return "—"
            return f'{v["mean_delta"]:+.3f} bits, {v["n_narrower"]}/{v["n_users"]} (p={v["wilcoxon_p"]})'
        rows.append(("H4 · E8 <span class='mfam'>B</span>",
                     "within a developer, spread(pred) &lt; spread(real)",
                     _e8cell(f8), _e8cell(i8), "supported",
                     "<b>B:</b> entropy of each developer's own move mix, real vs predicted. Confirmed, and "
                     "the folder causes it: without a folder the spread matches reality; with any folder "
                     "(right or wrong) each developer collapses to a narrower repertoire."))
        rows.append(("H3 · E4 <span class='mfam'>B</span>", "dist(pred, median) &lt; dist(real, median)",
                     f'Δ {f4.get("mean_pred_minus_real",0):+.3f} (p={num(f4.get("wilcoxon_p"),3)})',
                     f'Δ {i4.get("mean_pred_minus_real",0):+.3f} (p={num(i4.get("wilcoxon_p"),3)})',
                     "refuted",
                     "<b>B:</b> TVD from each developer's distribution to the population-average distribution. The opposite, significantly: with a folder, predictions sit FARTHER from the real population "
                     "average than the developers themselves do. Homogeneity is not shrinkage toward the human mean."))
        # E5 — decision vs surface
        rows.append(("E5 <span class='mfam'>B+C</span>", "Folder changes the voice but not the decision",
                     esc((fev or {}).get("e5")), esc((iev or {}).get("e5")), "supported",
                     "<b>B+C:</b> per-developer TVD (own distribution vs own prediction) set against judge style/content (C). Folder mode reads surface_only: judge-style rises while the move-mix distance to the real user "
                     "does not improve (it worsens vs. the no-folder baseline)."))
        rows.append(("E6 <span class='mfam'>A+B</span>", "Claims survive on the underdetermined-point control", "—", "—", "not run",
                     "<b>A+B:</b> would re-run the accuracy and distribution tests on determined points only. Needs k-fold resampling of the generic simulator; not yet generated."))
        rows.append(("E7 <span class='mfam'>B</span>", "Low-prompt / move-conditioned arms restore between-user variance", "—", "—", "not run",
                     "<b>B:</b> would re-measure between-developer spread under low-prompt / move-conditioned arms. The causal probe of the mechanism; not yet generated."))
        return rows


    # scoreboard columns are always folder-then-inline regardless of which report is primary
    fev = _ev(r if this_mode == "folder" else cr)
    iev = _ev(cr if this_mode == "folder" else r)
    sb_rows = "".join(
        f'<tr><td class="k">{cid}</td><td>{claim}</td><td class="num">{fv}</td><td class="num">{iv}</td>'
        f'<td><span class="{VERDICT_CLS[vd]}">{vd}</span></td></tr>'
        f'<tr class="note-row"><td></td><td colspan="4">{note}</td></tr>'
        for cid, claim, fv, iv, vd, note in scoreboard_rows(fev, iev))
    scoreboard_section = (
        '<section><div class="kicker">Scoreboard</div>'
        '<h2>Which claims survived the data?</h2>'
        '<p>Each experiment made a falsifiable prediction before the run. Evidence columns are the '
        f'<b>generic</b> condition for E2/E3 and <b>distilled</b> for E4 (the strongest test of each).</p>'
        '<table class="sb"><thead><tr><th>claim</th><th>prediction if the hypothesis is TRUE</th>'
        '<th class="num">folder</th><th class="num">inline</th><th>verdict</th></tr></thead>'
        f'<tbody>{sb_rows}</tbody></table>'
        '<div class="callout"><b>What it adds up to.</b> The simulator really is homogeneous — it '
        'compresses distinct developers into a narrow band of behaviour (H2) and its worst errors are '
        'task-completion substitutions (E1). But the mechanism is <em>not</em> the one H3 proposed: '
        'predictions do not shrink toward the average human, they cluster around the '
        '<b>model\'s own attractor</b>, which sits measurably away from the real developer average. '
        'Personalisation moves the voice, not the decision (E5).</div></section>')

    # ---- folder-vs-inline comparison (optional second report) ----
    compare_section = ""
    if cr is not None:
        def hl(rep):
            g = rep["E3_variance_collapse"]["by_condition"].get("generic", {})
            a = rep.get("E1_adjudication_summary") or {}
            e5r = rep["E5_decision_vs_surface"]
            return g, a, e5r
        rows = ""
        for label, rep in [(this_mode, r), (cmode, cr)]:
            g, a, e5r = hl(rep)
            sig = "p&lt;.05" if (g.get("perm_p") or 1) < 0.05 else f'p={num(g.get("perm_p"),2)}'
            rows += (f'<tr><td class="k">{esc(label)}</td>'
                     f'<td class="num">{num(g.get("spread_pred"),3)} vs {num(g.get("spread_real"),3)}</td>'
                     f'<td class="num">{sig}</td>'
                     f'<td>{esc(e5r.get("verdict"))}</td>'
                     f'<td class="num">{int(100*a["homogeneity_share"]) if a.get("homogeneity_share") is not None else "—"}%</td></tr>')
        compare_section = (
            '<section><div class="kicker">Folder vs inline</div>'
            '<h2>Two ways to read the folder into the simulator</h2>'
            '<p><b>folder</b> = the agent reads <code>users/&lt;slug&gt;/</code> itself; '
            '<b>inline</b> = the folder text is pasted into the prompt. They diverge: inline '
            'reproduces signature catchphrases verbatim, which <em>inflates</em> apparent between-user '
            'distinctiveness — so its variance-collapse is masked (E3) — yet E4 shows that distinctiveness '
            'points <em>away</em> from the real user, and its worst misses are even more homogeneity-driven.</p>'
            '<table><thead><tr><th>mode</th><th class="num">H2 generic spread (pred vs real)</th>'
            '<th class="num">perm p</th><th>E5 verdict</th><th class="num">E1 homogeneity</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></section>')

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SWESimBench — Diagnosing Misprediction Patterns</title>
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
 @media(min-width:720px) {{ .cards {{ grid-template-columns:repeat(3,1fr); }} }}
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
 figure.fig {{ margin:1.1rem 0 .4rem; padding:.9rem 1rem; background:#fff; border:1px solid var(--zinc200);
        border-radius:12px; overflow-x:auto; }}
 ul.defs {{ margin:.6rem 0 0; padding-left:1.1rem; font-size:.85rem; }}
 .mfam {{ display:inline-block; margin-left:.3rem; font-size:.62rem; font-weight:700; letter-spacing:.04em;
        background:var(--zinc100); color:var(--zinc500); border-radius:4px; padding:0 .3rem; vertical-align:middle; }}
 ul.defs li {{ margin:.22rem 0; }}
 table.sb td {{ vertical-align:middle; }}
 table.sb tr.note-row td {{ border-top:0; padding-top:0; font-size:.78rem; color:var(--zinc400); }}
 .v-yes, .v-no, .v-mix, .v-na {{ display:inline-block; font-size:.72rem; font-weight:700; text-transform:uppercase;
        letter-spacing:.03em; border-radius:4px; padding:.1rem .4rem; white-space:nowrap; }}
 .v-yes {{ background:#dcfce7; color:#15803d; }} .v-no {{ background:#ffe4e6; color:#be123c; }}
 .v-mix {{ background:#fef3c7; color:#b45309; }} .v-na {{ background:var(--zinc100); color:var(--zinc500); }}
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

<h1>Diagnosing Misprediction Patterns</h1>
<p class="lede"><b>Hypothesis.</b> LLMs are trained to complete tasks, not to imitate humans. So
they are systematically homogeneous, defaulting to task-driving behaviour instead of deciding from an
individual developer's differences. The consequence is that the prediction of LLMs would be very
similar for different users, and even for one developer the prediction will not be as spread out as
the real one.</p>
<p class="meta">Generated from <code>{esc(IN.name)}</code> · {esc(src_line)}</p>
{banner}

<div class="cards">{tiles}</div>

{metrics_section}

{scoreboard_section}

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
<h2>Worst mispredictions <span class="tag">metric A+C</span></h2>
<p>The homogeneity signature is a high share of <b>task-completion substitution</b> (predicted
keep-going where the real developer did something individual) and <b>generic-not-specific</b>.</p>
{e1_html}
{figure('E1')}
<div class="conv"><div class="h">developer</div><div class="h">REAL message</div><div class="h">SIMULATED prediction</div>
{worst_html}</div></section>

{compare_section}

<section><div class="kicker">E2 · marginals</div>
<h2>Marginal skew &amp; move confusion <span class="tag">H1, descriptive</span></h2>
<p>Predicted-minus-real share per category, and net flow between human and task moves.
{esc(e2.get("note",""))}</p>
<table><thead><tr><th>condition</th>{"".join(f'<th class="num">{c}</th>' for c in CATS)}
<th class="num">human→task / ←</th><th class="num">sign p</th></tr></thead><tbody>
{e2_rows()}</tbody></table>
{figure('E2')}</section>

<section><div class="kicker">E3 · primary result</div>
<h2>Between-developer collapse <span class="tag">H2 · primary</span></h2>
<p>Mean pairwise total-variation distance between developers' move-mixes. If the model captured
individual differences, predicted spread would match real spread; homogeneity predicts a
<b>narrower</b> predicted spread. Lower bar = developers look more alike.</p>
{figure('E3')}
<table><thead><tr><th>condition</th><th class="num">users</th><th class="num">spread real</th>
<th class="num">spread pred</th><th class="num">Δ</th><th class="num">perm p</th><th>collapse?</th></tr></thead><tbody>
{e3_rows()}</tbody></table></section>

<section><div class="kicker">E8 · primary result</div>
<h2>Within-developer collapse <span class="tag">H4</span></h2>
<p>Entropy of each developer&rsquo;s own move mix (bits, max 2.0 over four categories), real vs
predicted. Lower entropy = more one-note. This is the second half of the hypothesis: not just that
developers resemble each other, but that each one is rendered flatter than they actually are.</p>
<table><thead><tr><th>condition</th><th class="num">users</th><th class="num">entropy real</th>
<th class="num">entropy pred</th><th class="num">&Delta;</th><th class="num">narrower for</th>
<th class="num">wilcoxon p</th></tr></thead><tbody>
{e8_rows()}</tbody></table>
{figure('E8')}
<div class="callout"><b>Confirmed &mdash; and the folder causes it.</b> Without a folder (generic) the
predicted spread is essentially the real one. Give the simulator <em>any</em> folder &mdash; the right
one or the wrong one &mdash; and each developer collapses to a narrower repertoire. Personalisation does
not make the simulation more faithful; it makes it more of a caricature.</div></section>

<section><div class="kicker">E4 · primary result</div>
<h2>Regression to the median <span class="tag">H3</span></h2>
<p>Distance from each user's mix to the population-average mix, real vs predicted. Shrinkage toward
the median (predicted closer than real) supports homogeneity. Wilcoxon signed-rank.</p>
<table><thead><tr><th>condition</th><th class="num">users</th><th class="num">dist→median real</th>
<th class="num">dist→median pred</th><th class="num">Δ</th><th class="num">wilcoxon p</th><th>shrinks?</th></tr></thead><tbody>
{e4_rows()}</tbody></table>
{figure('E4')}</section>

<section><div class="kicker">E5 · decision vs. surface</div>
<h2>Does the folder change the decision or only the voice?</h2>
<p>Verdict: <b>{esc(e5.get("verdict"))}</b>. {esc(e5.get("reading"))} <code>move dist→real</code> is
the move-mix distance to the real user (lower = better decisions); <code>judge style</code> is
surface voice.</p>
<table><thead><tr><th>condition</th><th class="num">users</th><th class="num">move dist→real</th>
<th class="num">judge style</th><th class="num">judge realism</th><th class="num">judge content</th></tr></thead><tbody>
{e5_rows()}</tbody></table>
{figure('E5')}</section>

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

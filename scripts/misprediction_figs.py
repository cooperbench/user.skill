#!/usr/bin/env python3
"""Illustrative SVG figures for the misprediction / homogeneity study.

One figure per experiment, emitted as self-contained inline SVG strings so the standalone HTML
report and the Next.js site page render identical graphics.

Design follows the dataviz method:
  - Form first. Every figure is 1-2 series, so the form is EMPHASIS (one hue + de-emphasis gray)
    or DIVERGING (signed values), never a 4-way categorical palette. The four move categories
    appear as axis labels, not as hues -- the site's chip colors fail CVD (critical vs approve
    are deutan ΔE 2.7), which is fine for labelled chips but not for color-encoded marks.
  - Palette (validated with scripts/validate_palette.js on the #fafafa surface):
      diverging #6366f1 / #e11d48  -> ALL CHECKS PASS
      emphasis  #6366f1 / #71717a  -> CVD ΔE 19.5, normal 19.3, contrast pass; the gray is a
                                      deliberate de-emphasis slot (it trips the chroma floor by
                                      design, which is what "emphasis" means).
  - Marks: 2px lines, >=8px markers, 4px rounded bar ends, 2px gaps between adjacent bars,
    recessive axes, selective direct labels, text in ink tokens (never the series color).
"""

import html

# ---- design tokens (light surface; the host site is light-only) ----
SURFACE = "#fafafa"
INK = "#18181b"
INK2 = "#52525b"
MUTED = "#a1a1aa"
AXIS = "#e4e4e7"
TRACK = "#f4f4f5"
PRED = "#6366f1"     # predicted / focus
PRED_L = "#a5b4fc"   # predicted, secondary shade (inline mode)
REAL = "#71717a"     # real / context (de-emphasis)
NEG = "#e11d48"      # diverging negative pole
FONT = ('font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif"')


def esc(s):
    return html.escape(str(s))


def _txt(x, y, s, size=11, fill=INK2, anchor="start", weight="400"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>')


def _wrap(w, h, body, title, subtitle=""):
    """Figure frame: title + optional subtitle above the plot, per marks-and-anatomy."""
    head = _txt(0, 13, title, size=12.5, fill=INK, weight="600")
    sub = _txt(0, 29, subtitle, size=11, fill=MUTED) if subtitle else ""
    top = 40 if subtitle else 26
    return (f'<svg viewBox="0 0 {w} {h + top}" width="100%" height="{h + top}" '
            f'role="img" aria-label="{esc(title)}. {esc(subtitle)}" style="max-width:100%">'
            f'{head}{sub}<g transform="translate(0,{top})">{body}</g></svg>')


def _legend(items, x=0, y=0):
    """items: [(color, label)] — legend is always present for >=2 series."""
    out, cx = "", x
    for color, label in items:
        out += f'<rect x="{cx}" y="{y - 7}" width="9" height="9" rx="2" fill="{color}"/>'
        out += _txt(cx + 13, y + 1, label, size=10.5, fill=INK2)
        cx += 15 + 6.6 * len(label) + 12
    return out


# --------------------------------------------------------------------------------------
# A — individual-level accuracy vs the majority-class baseline
# --------------------------------------------------------------------------------------
def fig_a(a_folder, a_inline):
    """Skill score, diverging from 0 = the majority-class predictor. Skill (not raw accuracy) is
    the comparable number: the two modes have different class balance, so their raw accuracies
    are not on the same scale."""
    conds = ["distilled", "generic", "wrong"]
    W, rowh, lab, mid = 620, 36, 86, 400
    lo = -26.0                                   # scale floor (all observed skill is negative)
    px = lambda v: mid + (mid - lab - 20) * (v / abs(lo))
    body, y = "", 8
    for c in conds:
        f = a_folder["by_condition"].get(c, {})
        i = (a_inline or {}).get("by_condition", {}).get(c, {})
        body += _txt(lab - 10, y + 12, c, size=11, fill=INK, anchor="end")
        for j, (src, opacity, nm) in enumerate([(f, 1.0, "folder"), (i, 0.45, "inline")]):
            v = src.get("skill")
            if v is None:
                continue
            by = y + j * 12                       # 2px gap between the paired bars
            x0, x1 = (px(v), mid) if v < 0 else (mid, px(v))
            col = NEG if v < 0 else PRED
            body += (f'<rect x="{x0:.1f}" y="{by}" width="{max(abs(x1 - x0), 2):.1f}" height="10" '
                     f'rx="4" fill="{col}" fill-opacity="{opacity}"/>')
            body += _txt(x0 - 6, by + 8.5, f"{v:+.1f}  {nm}", size=9.5, fill=INK2, anchor="end")
        y += rowh
    # the zero rule IS the baseline — no separate reference line needed
    body += f'<line x1="{mid}" y1="0" x2="{mid}" y2="{y - 8}" stroke="{INK}" stroke-width="1.5"/>'
    body += _txt(mid + 8, 14, "0 = majority-class predictor", size=10, fill=INK, weight="600")
    body += _txt(mid + 8, 27, f"(always predict “{a_folder['baseline_class']}”)", size=9.5, fill=MUTED)
    body += _txt(mid + 8, 45, "100 would be perfect", size=9.5, fill=MUTED)
    body += _txt(lab, y + 14, "every condition scores below zero — worse than a constant predictor",
                 size=10.5, fill=INK, weight="600")
    body += _legend([(NEG, "below baseline")], x=lab, y=y + 34)
    body += _txt(lab + 120, y + 35, "solid = folder, faded = inline", size=10, fill=MUTED)
    return _wrap(W, y + 46, body,
                 "A · skill score — normalised move accuracy",
                 "S = (acc − acc_base) / (1 − acc_base), ×100")


# --------------------------------------------------------------------------------------
# E1 — error-type composition (emphasis: the two homogeneity types)
# --------------------------------------------------------------------------------------
def fig_e1(adj):
    cts = adj.get("error_type_counts", {})
    if not cts:
        return ""
    homog = {"task_completion_substitution", "generic_not_specific"}
    rows = sorted(cts.items(), key=lambda kv: -kv[1])
    W, rowh, lab = 620, 26, 210
    vmax = max(cts.values())
    px = lambda v: (W - lab - 46) * (v / vmax)
    body, y = "", 6
    for k, v in rows:
        on = k in homog
        body += _txt(lab - 10, y + 11, k, size=10.5, fill=INK if on else MUTED, anchor="end",
                     weight="600" if on else "400")
        body += f'<rect x="{lab}" y="{y}" width="{W - lab - 46}" height="14" rx="4" fill="{TRACK}"/>'
        body += (f'<rect x="{lab}" y="{y}" width="{max(px(v), 3):.1f}" height="14" rx="4" '
                 f'fill="{PRED if on else MUTED}"/>')
        body += _txt(lab + px(v) + 7, y + 11, str(v), size=10.5, fill=INK2, weight="600" if on else "400")
        y += rowh
    share = adj.get("homogeneity_share")
    body += _txt(lab, y + 12, f"homogeneity-type share: {int(100 * share)}% of the worst {adj.get('n_adjudicated')} misses",
                 size=10.5, fill=INK, weight="600")
    body += _legend([(PRED, "failure of individuation"), (MUTED, "ordinary failure mode")], x=lab, y=y + 32)
    return _wrap(W, y + 44, body,
                 "E1 · the worst misses are failures of individuation",
                 "adjudicated error type for each of the worst mispredictions (folder mode)")


# --------------------------------------------------------------------------------------
# E2 — diverging: predicted minus real share, per move category
# --------------------------------------------------------------------------------------
def fig_e2(e2_folder, e2_inline, cats):
    f = e2_folder["by_condition"]["generic"]["pred_minus_real"]
    i = e2_inline["by_condition"]["generic"]["pred_minus_real"] if e2_inline else {}
    W, rowh, lab, mid = 620, 36, 86, 330
    span = 0.20
    px = lambda v: mid + (W - mid - 70) * (v / span)
    body, y = "", 8
    for c in cats:
        body += _txt(lab - 10, y + 12, c, size=11, fill=INK, anchor="end")
        # Colour encodes SIGN only (diverging); the mode is encoded by row position + opacity,
        # so no channel carries two meanings.
        for j, (src, opacity, nm) in enumerate([(f, 1.0, "folder"), (i, 0.45, "inline")]):
            v = src.get(c)
            if v is None:
                continue
            by = y + j * 12
            x0, x1 = (mid, px(v)) if v >= 0 else (px(v), mid)
            col = PRED if v >= 0 else NEG
            body += (f'<rect x="{x0:.1f}" y="{by}" width="{max(abs(x1 - x0), 2):.1f}" height="10" '
                     f'rx="4" fill="{col}" fill-opacity="{opacity}"/>')
            tx = x1 + 6 if v >= 0 else x0 - 6
            body += _txt(tx, by + 8.5, f"{v:+.3f}  {nm}", size=9.5, fill=INK2,
                         anchor="start" if v >= 0 else "end")
        y += rowh
    body += f'<line x1="{mid}" y1="0" x2="{mid}" y2="{y - 8}" stroke="{AXIS}" stroke-width="2"/>'
    body += _txt(mid, y + 12, "0 = predicted share matches real", size=10, fill=MUTED, anchor="middle")
    body += _legend([(PRED, "over-produced"), (NEG, "under-produced")], x=lab, y=y + 32)
    body += _txt(lab, y + 48, "solid = folder, faded = inline (each pair shares a row)",
                 size=10, fill=MUTED)
    return _wrap(W, y + 60, body,
                 "E2 · the simulator under-produces “critical” in both modes",
                 "predicted minus real share of each move (generic condition)")


# --------------------------------------------------------------------------------------
# E3 — between-developer spread: one dot per developer, distance from its own centroid
# --------------------------------------------------------------------------------------
def fig_e3(detail_folder):
    d = detail_folder.get("generic")
    if not d:
        return ""
    users = d["users"]
    sr = [v["s_real"] for v in users.values()]
    sp = [v["s_pred"] for v in users.values()]
    W, lab = 620, 96
    xmax = max(sr + sp) * 1.12
    px = lambda v: lab + (W - lab - 56) * (v / xmax)
    body = ""
    for k, (vals, color, name, y) in enumerate([(sr, REAL, "real developers", 26),
                                                (sp, PRED, "predicted", 78)]):
        body += f'<line x1="{lab}" y1="{y}" x2="{W - 56}" y2="{y}" stroke="{AXIS}" stroke-width="1"/>'
        body += _txt(lab - 10, y + 4, name, size=11, fill=INK, anchor="end")
        for v in vals:
            # 2px surface ring so overlapping dots stay countable
            body += (f'<circle cx="{px(v):.1f}" cy="{y}" r="5" fill="{color}" fill-opacity="0.55" '
                     f'stroke="{SURFACE}" stroke-width="2"/>')
        mean = sum(vals) / len(vals)
        body += (f'<line x1="{px(mean):.1f}" y1="{y - 15}" x2="{px(mean):.1f}" y2="{y + 15}" '
                 f'stroke="{color}" stroke-width="2"/>')
        body += _txt(px(mean), y - 20, f"mean {mean:.3f}", size=10, fill=INK, anchor="middle", weight="600")
    body += _txt(lab, 116, "each dot = one developer’s distance from the centre of its own group",
                 size=10, fill=MUTED)
    body += _txt(lab, 130, "predicted developers sit in a tighter band — they look more alike than real ones",
                 size=10, fill=INK)
    return _wrap(W, 142, body,
                 "E3 · predicted developers cluster more tightly than real ones",
                 "spread of per-developer move-mixes, folder mode / generic condition")


# --------------------------------------------------------------------------------------
# E4 — slope chart: distance to the human average, real -> predicted, per developer
# --------------------------------------------------------------------------------------
def fig_e4(detail_folder):
    d = detail_folder.get("distilled")
    if not d:
        return ""
    users = d["users"]
    W, H = 620, 210
    xl, xr = 190, 430
    vmax = max(max(v["d_real"], v["d_pred"]) for v in users.values()) * 1.1
    py = lambda v: H - 30 - (H - 62) * (v / vmax)
    body = ""
    for x, name in [(xl, "real developer"), (xr, "its prediction")]:
        body += f'<line x1="{x}" y1="{py(0)}" x2="{x}" y2="{py(vmax)}" stroke="{AXIS}" stroke-width="1"/>'
        body += _txt(x, H - 12, name, size=11, fill=INK, anchor="middle")
    away = 0
    for v in users.values():
        up = v["d_pred"] > v["d_real"]
        away += 1 if up else 0
        col = NEG if up else PRED
        body += (f'<line x1="{xl}" y1="{py(v["d_real"]):.1f}" x2="{xr}" y2="{py(v["d_pred"]):.1f}" '
                 f'stroke="{col}" stroke-width="2" stroke-opacity="0.5"/>')
        for x, val in [(xl, v["d_real"]), (xr, v["d_pred"])]:
            body += (f'<circle cx="{x}" cy="{py(val):.1f}" r="4.5" fill="{col}" '
                     f'stroke="{SURFACE}" stroke-width="2"/>')
    body += _txt(6, py(vmax) - 8, "farther from the average developer →", size=10, fill=MUTED)
    body += _txt(xr + 16, 24, f"{away} of {len(users)} developers", size=11, fill=INK, weight="600")
    body += _txt(xr + 16, 38, "move AWAY from the", size=10.5, fill=INK2)
    body += _txt(xr + 16, 51, "human average", size=10.5, fill=INK2)
    body += _legend([(NEG, "moves away"), (PRED, "moves toward")], x=xl - 60, y=H + 6)
    return _wrap(W, H + 16, body,
                 "E4 · predictions move away from the average developer, not toward it",
                 "distance to the human population centre, real vs predicted (distilled condition)")


# --------------------------------------------------------------------------------------
# E5 — decision vs surface: one point per condition
# --------------------------------------------------------------------------------------
def fig_e5(e5_folder):
    by = e5_folder["by_condition"]
    pts = [(c, v.get("move_dist_to_real"), v.get("judge_style")) for c, v in by.items()
           if v.get("move_dist_to_real") is not None and v.get("judge_style") is not None]
    if not pts:
        return ""
    W, H = 620, 230
    xs = [p[1] for p in pts]; ys = [p[2] for p in pts]
    x0, x1 = min(xs) - 0.02, max(xs) + 0.02
    y0, y1 = min(ys) - 2, max(ys) + 2
    L, R, T, B = 150, 40, 16, 46
    px = lambda v: L + (W - L - R) * ((v - x0) / (x1 - x0))
    py = lambda v: (H - B) - (H - B - T) * ((v - y0) / (y1 - y0))
    body = (f'<rect x="{L}" y="{T}" width="{W - L - R}" height="{H - B - T}" fill="{TRACK}" '
            f'fill-opacity="0.6" rx="6"/>')
    for c, x, y in pts:
        on = c == "distilled"
        body += (f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="7" fill="{PRED if on else REAL}" '
                 f'stroke="{SURFACE}" stroke-width="2"/>')
        body += _txt(px(x) + 12, py(y) + 4, c, size=11, fill=INK if on else INK2,
                     weight="600" if on else "400")
    body += _txt(L, H - 26, "worse decisions →", size=10, fill=MUTED)
    body += _txt(L - 10, T + 6, "better", size=10, fill=MUTED, anchor="end")
    body += _txt(L - 10, T + 18, "voice", size=10, fill=MUTED, anchor="end")
    body += _txt(6, py((y0 + y1) / 2), "judge style (surface)", size=10.5, fill=INK2)
    body += _txt(L, H - 10, "move-mix distance to the real developer (decision)", size=10.5, fill=INK2)
    body += _txt(L + 8, T + 14, "the distilled folder buys voice, not decisions", size=10.5,
                 fill=INK, weight="600")
    return _wrap(W, H, body,
                 "E5 · personalisation moves the surface, not the choice",
                 "each point is one condition, folder mode")


def fig_e8(e8):
    """Within-developer spread: dumbbell from real -> predicted entropy, one row per condition.
    Dumbbell is the prescribed form for before->after per item; 1 hue, 2 shades + gray context."""
    by = e8.get("by_condition", {})
    if not by:
        return ""
    W, rowh, lab = 620, 42, 92
    lo, hi = 0.9, 1.75
    px = lambda v: lab + (W - lab - 150) * ((v - lo) / (hi - lo))
    body, y = "", 14
    for c in ["distilled", "generic", "wrong"]:
        v = by.get(c)
        if not v:
            continue
        xr, xp = px(v["entropy_real"]), px(v["entropy_pred"])
        body += _txt(lab - 10, y + 4, c, size=11, fill=INK, anchor="end")
        body += (f'<line x1="{xp:.1f}" y1="{y}" x2="{xr:.1f}" y2="{y}" stroke="{PRED}" '
                 f'stroke-width="2" stroke-opacity="0.35"/>')
        body += (f'<circle cx="{xr:.1f}" cy="{y}" r="5.5" fill="{REAL}" stroke="{SURFACE}" stroke-width="2"/>')
        body += (f'<circle cx="{xp:.1f}" cy="{y}" r="5.5" fill="{PRED}" stroke="{SURFACE}" stroke-width="2"/>')
        sig = "p<.01" if (v.get("wilcoxon_p") or 1) < 0.01 else (
              "p<.05" if (v.get("wilcoxon_p") or 1) < 0.05 else "n.s.")
        body += _txt(W - 142, y + 4, f'{v["n_narrower"]}/{v["n_users"]} narrower · {sig}',
                     size=10, fill=INK if sig != "n.s." else MUTED,
                     weight="600" if sig != "n.s." else "400")
        y += rowh
    body += f'<line x1="{lab}" y1="{y - 18}" x2="{W - 150}" y2="{y - 18}" stroke="{AXIS}" stroke-width="1"/>'
    for t in (1.0, 1.25, 1.5, 1.75):
        body += _txt(px(t), y - 4, f"{t:g}", size=9.5, fill=MUTED, anchor="middle")
    body += _txt(lab, y + 14, "entropy of one developer’s own move mix (bits) — lower = more one-note",
                 size=10, fill=MUTED)
    body += _legend([(REAL, "real developer"), (PRED, "predicted")], x=lab, y=y + 34)
    return _wrap(W, y + 44, body,
                 "E8 · with a folder, each developer is rendered more one-note than they are",
                 "within-developer spread, real vs predicted (folder mode)")


def build_figures(folder, inline):
    """-> {name: svg}. `folder`/`inline` are misprediction report dicts."""
    cats = folder.get("categories") or ["approve", "critical", "directive", "inquiry"]
    figs = {}
    if folder.get("A_move_accuracy"):
        figs["A"] = fig_a(folder["A_move_accuracy"], (inline or {}).get("A_move_accuracy"))
    if folder.get("E1_adjudication_summary"):
        figs["E1"] = fig_e1(folder["E1_adjudication_summary"])
    figs["E2"] = fig_e2(folder["E2_marginal_confusion"],
                        (inline or {}).get("E2_marginal_confusion"), cats)
    if folder.get("per_user_detail"):
        figs["E3"] = fig_e3(folder["per_user_detail"])
        figs["E4"] = fig_e4(folder["per_user_detail"])
    figs["E5"] = fig_e5(folder["E5_decision_vs_surface"])
    if folder.get("E8_within_developer_spread"):
        figs["E8"] = fig_e8(folder["E8_within_developer_spread"])
    return {k: v for k, v in figs.items() if v}

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
      diverging #4f46e5 / #e11d48  -> ALL CHECKS PASS (site accent indigo-600)
      emphasis  #4f46e5 / #52525b  -> CVD/normal separation pass; the gray is a
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
PRED = "#4f46e5"     # predicted / focus (site accent, indigo-600)
PRED_L = "#a5b4fc"   # predicted, secondary shade (inline mode)
REAL = "#52525b"     # real / context (de-emphasis, zinc-600)
NEG = "#e11d48"      # diverging negative pole
FONT = ('font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif"')


def esc(s):
    return html.escape(str(s))


def _txt(x, y, s, size=12, fill=INK2, anchor="start", weight="400"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>')


# Titles live OUTSIDE the SVG (as <figcaption>/<p> in the host page) so they pick up the
# site's type scale rather than fixed SVG pixel sizes. _wrap returns (svg, title, subtitle);
# build_figures hands the caller all three.
def _wrap(w, h, body, title, subtitle=""):
    """Plot frame only — no title chrome; the host page renders the caption."""
    svg = (f'<svg viewBox="0 0 {w} {h + 8}" width="100%" height="{h + 8}" '
           f'role="img" aria-label="{esc(title)}. {esc(subtitle)}" style="max-width:100%">'
           f'<g transform="translate(0,4)">{body}</g></svg>')
    return {"svg": svg, "title": title, "subtitle": subtitle}


def _legend(items, x=0, y=0):
    """items: [(color, label)] — legend is always present for >=2 series."""
    out, cx = "", x
    for color, label in items:
        out += f'<rect x="{cx}" y="{y - 7}" width="9" height="9" rx="2" fill="{color}"/>'
        out += _txt(cx + 13, y + 1, label, size=12, fill=INK2)
        cx += 15 + 6.6 * len(label) + 12
    return out



# ---- his row-chart anatomy (see web/app/SolHighResults.tsx ScoreRow) --------------------
# Each row is a tinted card: [label+note | full-width rounded track with fill | value].
ROW_BG = "#fafafa"        # bg-zinc-50
ROW_BG_HI = "#eef2ff"     # bg-indigo-50
TRACK_FULL = "#e4e4e7"    # bg-zinc-200
LABEL_W = 200
VALUE_W = 92
ROW_H = 56
BAR_H = 12


def _row_card(y, w, featured=False):
    return (f'<rect x="0" y="{y}" width="{w}" height="{ROW_H - 8}" rx="12" '
            f'fill="{ROW_BG_HI if featured else ROW_BG}"/>')


def _row_label(y, label, note=""):
    out = _txt(16, y + (22 if note else 27), label, size=14, fill=INK, weight="600")
    if note:
        out += _txt(16, y + 38, note, size=12, fill=MUTED)
    return out


def _row_track(x0, x1, y, frac, color, origin=0.0):
    """Full-width rounded track with a proportional fill. `origin` (0..1) allows a
    centre-anchored fill for diverging values."""
    cy = y + (ROW_H - 8) / 2
    out = (f'<rect x="{x0}" y="{cy - BAR_H/2:.1f}" width="{x1 - x0}" height="{BAR_H}" '
           f'rx="{BAR_H/2}" fill="{TRACK_FULL}"/>')
    span = x1 - x0
    a = x0 + span * min(origin, origin + frac)
    b = x0 + span * max(origin, origin + frac)
    if b - a > 0.5:
        out += (f'<rect x="{a:.1f}" y="{cy - BAR_H/2:.1f}" width="{b - a:.1f}" height="{BAR_H}" '
                f'rx="{BAR_H/2}" fill="{color}"/>')
    return out


def _row_value(x, y, text, color=INK):
    cy = y + (ROW_H - 8) / 2 + 6
    return _txt(x, cy, text, size=17, fill=color, anchor="end", weight="600")


# --------------------------------------------------------------------------------------
# A — individual-level accuracy vs the majority-class baseline
# --------------------------------------------------------------------------------------
def fig_a(a_folder, a_inline):
    """Skill score as row cards (his ScoreRow anatomy). Skill is the comparable number: the
    two modes differ in class balance, so raw accuracies are not on the same scale."""
    W = 980
    x0, x1 = LABEL_W, W - VALUE_W - 24
    lo, hi = -26.0, 4.0                       # scale spans the observed range plus a little headroom
    zero = (0 - lo) / (hi - lo)               # where the baseline sits along the track
    body, y = "", 0
    for c in ["distilled", "generic", "wrong"]:
        f = a_folder["by_condition"].get(c, {})
        i = (a_inline or {}).get("by_condition", {}).get(c, {})
        v, vi = f.get("skill"), i.get("skill")
        if v is None:
            continue
        feat = c == "distilled"
        body += _row_card(y, W, feat)
        body += _row_label(y, c, f"inline {vi:+.1f}" if vi is not None else "")
        body += _row_track(x0, x1, y, (v / (hi - lo)), NEG if v < 0 else PRED, origin=zero)
        # the baseline tick sits at zero on every row
        cy = y + (ROW_H - 8) / 2
        zx = x0 + (x1 - x0) * zero
        body += (f'<line x1="{zx:.1f}" y1="{cy - 11:.1f}" x2="{zx:.1f}" y2="{cy + 11:.1f}" '
                 f'stroke="{INK}" stroke-width="2"/>')
        body += _row_value(W - 16, y, f"{v:+.1f}", NEG if v < 0 else PRED)
        y += ROW_H
    body += _txt(x0, y + 14, "0 = majority-class predictor (always predict “"
                 + a_folder["baseline_class"] + "”) · 100 would be perfect", size=12, fill=MUTED)
    body += _txt(x0, y + 32, "every condition scores below zero — worse than a constant predictor",
                 size=12.5, fill=INK, weight="600")
    return _wrap(W, y + 42, body,
                 "A · skill score — normalised move accuracy",
                 "S = (acc − acc_base) / (1 − acc_base), ×100 · label note shows the inline arm")


# --------------------------------------------------------------------------------------
# E1 — error-type composition (emphasis: the two homogeneity types)
# --------------------------------------------------------------------------------------
def fig_e1(adj):
    cts = adj.get("error_type_counts", {})
    if not cts:
        return ""
    homog = {"task_completion_substitution", "generic_not_specific"}
    rows = sorted(cts.items(), key=lambda kv: -kv[1])
    W = 980
    x0, x1 = LABEL_W + 90, W - VALUE_W - 24
    vmax = max(cts.values())
    body, y = "", 0
    for k, v in rows:
        on = k in homog
        body += _row_card(y, W, on)
        body += _row_label(y, k, "failure of individuation" if on else "ordinary failure mode")
        body += _row_track(x0, x1, y, v / vmax, PRED if on else MUTED)
        body += _row_value(W - 16, y, str(v), PRED if on else INK2)
        y += ROW_H
    share = adj.get("homogeneity_share")
    body += _txt(x0, y + 16, f"homogeneity-type share: {int(100 * share)}% of the worst "
                 f"{adj.get('n_adjudicated')} misses", size=12.5, fill=INK, weight="600")
    return _wrap(W, y + 26, body,
                 "E1 · the worst misses are failures of individuation",
                 "adjudicated error type for each of the worst mispredictions (folder mode)")


# --------------------------------------------------------------------------------------
# E2 — diverging: predicted minus real share, per move category
# --------------------------------------------------------------------------------------
def fig_e2(e2_folder, e2_inline, cats):
    """Diverging row cards: predicted-minus-real share per move. Colour encodes SIGN only;
    the mode is carried by the sub-note and the paired inline value."""
    f = e2_folder["by_condition"]["generic"]["pred_minus_real"]
    i = e2_inline["by_condition"]["generic"]["pred_minus_real"] if e2_inline else {}
    W = 980
    x0, x1 = LABEL_W, W - VALUE_W - 24
    span = 0.26                                # symmetric scale around 0
    body, y = "", 0
    for c in cats:
        v = f.get(c)
        if v is None:
            continue
        vi = i.get(c)
        feat = c == "critical"                 # the signature finding
        body += _row_card(y, W, feat)
        body += _row_label(y, c, f"inline {vi:+.3f}" if vi is not None else "")
        body += _row_track(x0, x1, y, v / (2 * span), NEG if v < 0 else PRED, origin=0.5)
        cy = y + (ROW_H - 8) / 2
        zx = x0 + (x1 - x0) * 0.5
        body += (f'<line x1="{zx:.1f}" y1="{cy - 11:.1f}" x2="{zx:.1f}" y2="{cy + 11:.1f}" '
                 f'stroke="{INK}" stroke-width="2"/>')
        body += _row_value(W - 16, y, f"{v:+.3f}", NEG if v < 0 else PRED)
        y += ROW_H
    body += _txt(x0, y + 16, "0 = predicted share matches real · bars show the folder arm, "
                 "the note shows inline", size=12, fill=MUTED)
    body += _legend([(PRED, "over-produced"), (NEG, "under-produced")], x=x0, y=y + 38)
    return _wrap(W, y + 48, body,
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
    W, lab = 980, 150
    xmax = max(sr + sp) * 1.12
    px = lambda v: lab + (W - lab - 56) * (v / xmax)
    body = ""
    for k, (vals, color, name, y) in enumerate([(sr, REAL, "real developers", 26),
                                                (sp, PRED, "predicted", 78)]):
        body += f'<line x1="{lab}" y1="{y}" x2="{W - 56}" y2="{y}" stroke="{AXIS}" stroke-width="1"/>'
        body += _txt(lab - 10, y + 4, name, size=12, fill=INK, anchor="end")
        for v in vals:
            # 2px surface ring so overlapping dots stay countable
            body += (f'<circle cx="{px(v):.1f}" cy="{y}" r="5" fill="{color}" fill-opacity="0.55" '
                     f'stroke="{SURFACE}" stroke-width="2"/>')
        mean = sum(vals) / len(vals)
        body += (f'<line x1="{px(mean):.1f}" y1="{y - 15}" x2="{px(mean):.1f}" y2="{y + 15}" '
                 f'stroke="{color}" stroke-width="2"/>')
        body += _txt(px(mean), y - 20, f"mean {mean:.3f}", size=11.5, fill=INK, anchor="middle", weight="600")
    body += _txt(lab, 116, "each dot = one developer’s distance from the centre of its own group",
                 size=11.5, fill=MUTED)
    body += _txt(lab, 130, "predicted developers sit in a tighter band — they look more alike than real ones",
                 size=11.5, fill=INK)
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
    W, H = 980, 230
    xl, xr = 300, 680
    vmax = max(max(v["d_real"], v["d_pred"]) for v in users.values()) * 1.1
    py = lambda v: H - 30 - (H - 62) * (v / vmax)
    body = ""
    for x, name in [(xl, "real developer"), (xr, "its prediction")]:
        body += f'<line x1="{x}" y1="{py(0)}" x2="{x}" y2="{py(vmax)}" stroke="{AXIS}" stroke-width="1"/>'
        body += _txt(x, H - 12, name, size=12, fill=INK, anchor="middle")
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
    body += _txt(6, py(vmax) - 8, "farther from the average developer →", size=11.5, fill=MUTED)
    body += _txt(xr + 16, 24, f"{away} of {len(users)} developers", size=12, fill=INK, weight="600")
    body += _txt(xr + 16, 38, "move AWAY from the", size=12, fill=INK2)
    body += _txt(xr + 16, 51, "human average", size=12, fill=INK2)
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
    W, H = 980, 250
    xs = [p[1] for p in pts]; ys = [p[2] for p in pts]
    x0, x1 = min(xs) - 0.02, max(xs) + 0.02
    y0, y1 = min(ys) - 2, max(ys) + 2
    L, R, T, B = 230, 60, 16, 46
    px = lambda v: L + (W - L - R) * ((v - x0) / (x1 - x0))
    py = lambda v: (H - B) - (H - B - T) * ((v - y0) / (y1 - y0))
    body = (f'<rect x="{L}" y="{T}" width="{W - L - R}" height="{H - B - T}" fill="{TRACK}" '
            f'fill-opacity="0.6" rx="6"/>')
    for c, x, y in pts:
        on = c == "distilled"
        body += (f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="7" fill="{PRED if on else REAL}" '
                 f'stroke="{SURFACE}" stroke-width="2"/>')
        body += _txt(px(x) + 12, py(y) + 4, c, size=12, fill=INK if on else INK2,
                     weight="600" if on else "400")
    body += _txt(L, H - 26, "worse decisions →", size=11.5, fill=MUTED)
    body += _txt(L - 10, T + 6, "better", size=11.5, fill=MUTED, anchor="end")
    body += _txt(L - 10, T + 18, "voice", size=11.5, fill=MUTED, anchor="end")
    body += _txt(6, py((y0 + y1) / 2), "judge style (surface)", size=12, fill=INK2)
    body += _txt(L, H - 10, "move-mix distance to the real developer (decision)", size=12, fill=INK2)
    body += _txt(L + 8, T + 14, "the distilled folder buys voice, not decisions", size=12,
                 fill=INK, weight="600")
    return _wrap(W, H, body,
                 "E5 · personalisation moves the surface, not the choice",
                 "each point is one condition, folder mode")


def fig_e8(e8):
    """Within-developer spread as row cards: real vs predicted entropy per condition."""
    by = e8.get("by_condition", {})
    if not by:
        return ""
    W = 980
    x0, x1 = LABEL_W, W - VALUE_W - 24
    hi = 2.0                                   # entropy max over four categories
    body, y = "", 0
    for c in ["distilled", "generic", "wrong"]:
        v = by.get(c)
        if not v:
            continue
        feat = c == "distilled"
        sig = ("p<.01" if (v.get("wilcoxon_p") or 1) < 0.01
               else "p<.05" if (v.get("wilcoxon_p") or 1) < 0.05 else "n.s.")
        body += _row_card(y, W, feat)
        body += _row_label(y, c, f'{v["n_narrower"]}/{v["n_users"]} narrower · {sig}')
        # real = context bar behind, predicted = focus bar in front (same track)
        body += _row_track(x0, x1, y, v["entropy_real"] / hi, REAL)
        cy = y + (ROW_H - 8) / 2
        pw = (x1 - x0) * (v["entropy_pred"] / hi)
        body += (f'<rect x="{x0}" y="{cy - BAR_H/2 + 3:.1f}" width="{pw:.1f}" height="{BAR_H - 6}" '
                 f'rx="{(BAR_H-6)/2}" fill="{PRED}"/>')
        body += _row_value(W - 16, y, f'{v["mean_delta"]:+.2f}', PRED)
        y += ROW_H
    body += _legend([(REAL, "real developer"), (PRED, "predicted")], x=x0, y=y + 16)
    body += _txt(x0, y + 38, "entropy of one developer’s own move mix (bits, max 2.0) — "
                 "lower = more one-note", size=12, fill=MUTED)
    return _wrap(W, y + 48, body,
                 "E8 · with a folder, each developer is rendered more one-note than they are",
                 "within-developer spread, real vs predicted (folder mode)")


def build_figures(folder, inline):
    """-> {name: {svg, title, subtitle}}. `folder`/`inline` are misprediction report dicts."""
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

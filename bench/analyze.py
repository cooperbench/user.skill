#!/usr/bin/env python3
"""Post-run analysis for UserSimBench v0: easy-mode deltas, persona lift, and transfer
vs prior work. Reads bench/results/v0_summary.json, prints a markdown findings block."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "bench" / "results" / "v0_summary.json").read_text())
R = S["results"]
real_appr = S["real_approve%"]
real_crit = S["real_critical%"]
ceil = S["condagree_marginal_ceiling"]
MODELS = list(S["models"])

# Prior-work standing (Sim2Real-USI / OdysSim), for the transfer comparison.
PRIOR = {
    "deepseek-v3.1":  {"usi": 76.0, "note": "Sim2Real-USI BEST simulator"},
    "gpt-5":          {"usi": 70.9, "note": "Sim2Real-USI GPT-5.x"},
    "gemini-3.1-pro": {"usi": None, "note": "OdysSim most-human-like (HumT)"},
}


def row(k):
    r = R[k]
    return (r["MoveFid"], r["CondAgree"], r["approve%"], r["critical%"], r["active%"], r["n"])


print(f"\n### Real developers (n={S['n_points']})")
print("move mix:", "  ".join(f"{k} {v:.0%}" for k, v in S["real_move_distribution"].items()))
print(f"approve%={real_appr}  critical%={real_crit}  active%={S['real_active%']}  "
      f"CondAgree marginal-ceiling Σp²={ceil}\n")

print("### Per model × condition")
print("| simulator | MoveFid↑ | CondAgree↑ | Δapprove | Δcritical | conditional-skill (CondAgree−Σp²) |")
print("|---|---|---|---|---|---|")
for m in MODELS:
    for c in ["distilled", "generic"]:
        mf, ca, ap, cr, ac, n = row(f"{m}/{c}")
        dap = round(ap - real_appr, 3)
        dcr = round(cr - real_crit, 3)
        skill = round((ca - ceil), 3) if ca is not None else None
        print(f"| {m}/{c} | {mf} | {ca} | {dap:+.3f} | {dcr:+.3f} | {skill:+.3f} |")
for ref in ["prior_sampler", "majority", "always_approve"]:
    mf, ca, ap, cr, ac, n = row(f"[ref] {ref}")
    print(f"| [ref] {ref} | {mf} | {ca} | {ap-real_appr:+.3f} | {cr-real_crit:+.3f} | "
          f"{(ca-ceil):+.3f} |")

print("\n### Persona lift (distilled − generic)")
print("| model | ΔMoveFid | ΔCondAgree | Δapprove% (closer to real is better) |")
print("|---|---|---|---|")
for m in MODELS:
    d = R[f"{m}/distilled"]; g = R[f"{m}/generic"]
    dmf = round((d["MoveFid"] or 0) - (g["MoveFid"] or 0), 1)
    dca = round((d["CondAgree"] or 0) - (g["CondAgree"] or 0), 3)
    dap = round(abs(d["approve%"] - real_appr) - abs(g["approve%"] - real_appr), 3)
    print(f"| {m} | {dmf:+.1f} | {dca:+.3f} | {dap:+.3f} |")

print("\n### Transfer vs prior work")
print("Ranking models by coding **MoveFid** (best condition) vs their prior-work user-sim standing:")
best = {m: max(R[f"{m}/distilled"]["MoveFid"], R[f"{m}/generic"]["MoveFid"]) for m in MODELS}
easymode = {m: min(  # worst (most positive) approve inflation across conds
    R[f"{m}/distilled"]["approve%"] - real_appr,
    R[f"{m}/generic"]["approve%"] - real_appr, key=lambda x: -x) for m in MODELS}
print("| model | prior-work | coding MoveFid (best) | approve-inflation |")
print("|---|---|---|---|")
for m in sorted(MODELS, key=lambda m: -best[m]):
    pw = PRIOR[m]
    usi = f"USI {pw['usi']}" if pw["usi"] else pw["note"]
    print(f"| {m} | {usi} | {best[m]} | {easymode[m]:+.3f} |")

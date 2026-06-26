"""Final v0.1 analysis: clean 10-user x 50-turn macro with an UNBIASED lucky-guess line,
the distilled-vs-generic (persona) effect, and the headline comparison vs v0."""
import json
from pathlib import Path

S = json.loads((Path(__file__).resolve().parent.parent / "bench/results/v0_1_summary.json").read_text())
R = S["results"]
realA = S["real_macro"]["approve"]["mean"]
realC = S["real_macro"]["critical"]["mean"]

# unbiased per-user Σp²: (n*Σp̂² - 1)/(n-1); macro = mean over users
rp = S["real_per_user"]
unb = []
for u, d in rp.items():
    n, s2 = d["n"], d["sigma2"]
    if n > 1:
        unb.append((n * s2 - 1) / (n - 1))
lucky_unbiased = round(sum(unb) / len(unb), 3)
lucky_biased = S["lucky_guess_macro"]

print(f"REAL (macro, 10 users): approve {realA}  critical {realC}")
print(f"lucky-guess line: plug-in {lucky_biased}  ->  UNBIASED {lucky_unbiased}\n")

MODELS = ["deepseek-v3.1", "gpt-5", "gemini-3.1-pro", "osim-8b", "osim-4b"]


def cell(k):
    m = R[k]["macro"]
    return {q: (round(m[q]["mean"], 3), round(m[q]["ci95"], 3)) for q in ["MoveFid", "CondAgree", "approve", "critical"]}


print(f"{'simulator':24s} {'MoveFid':>13} {'CondAgree':>14} {'vs-lucky':>9} {'approve':>13} {'critical':>13}")
print("-" * 92)
for cond in ["distilled", "generic"]:
    for mdl in MODELS:
        c = cell(f"{mdl}/{cond}")
        ca = c["CondAgree"][0]
        vs = "ABOVE" if ca > lucky_unbiased + 0.01 else ("below" if ca < lucky_unbiased - 0.01 else "≈line")
        print(f"{mdl+'/'+cond:24s} {c['MoveFid'][0]}±{c['MoveFid'][1]:<6} {c['CondAgree'][0]}±{c['CondAgree'][1]:<7} {vs:>9} "
              f"{c['approve'][0]}±{c['approve'][1]:<6} {c['critical'][0]}±{c['critical'][1]}")
for ref in ["prior_sampler", "always_approve"]:
    k = f"[ref] {ref}"
    if k in R:
        c = cell(k)
        print(f"{ref:24s} {c['MoveFid'][0]}±{c['MoveFid'][1]:<6} {c['CondAgree'][0]}±{c['CondAgree'][1]:<7} {'':>9} "
              f"{c['approve'][0]}±{c['approve'][1]:<6} {c['critical'][0]}±{c['critical'][1]}")

print("\n=== persona effect: CondAgree (distilled - generic) ===")
for mdl in MODELS:
    d = R[f"{mdl}/distilled"]["macro"]["CondAgree"]["mean"]
    g = R[f"{mdl}/generic"]["macro"]["CondAgree"]["mean"]
    print(f"  {mdl:16s} {d:.3f} - {g:.3f} = {d-g:+.3f}")

print("\n=== critical% vs real (easy-mode gap) ===")
for mdl in MODELS:
    for cond in ["distilled", "generic"]:
        cr = R[f"{mdl}/{cond}"]["macro"]["critical"]["mean"]
        print(f"  {mdl+'/'+cond:24s} {cr:.3f}  (real {realC}, {cr/realC*100:.0f}% of real)")

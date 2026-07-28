"""Mine concrete profile-helped vs profile-hurt cases for the website case study.
Models: glm-5.2 (profile helps a lot), gemini-3.1-pro (profile hurts), osim-4b (profile helps, crosses line).
Joins experiments/condagree_multi/{points.jsonl, raw.jsonl} using the same label hashing as exp_condagree.
Writes experiments/condagree_multi/cases.json.
"""
import hashlib, json, sys
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(HERE))
import validate as V
import taxonomy as TAX
EXP = HERE / "experiments" / "condagree_multi"
MODELS = ["glm-5.2", "gemini-3.1-pro", "osim-4b"]

# load points + raw
points = {}
for l in (EXP / "points.jsonl").read_text().splitlines():
    if l.strip():
        p = json.loads(l); points[p["point_id"]] = p
gens = {}; labels = {}
for l in (EXP / "raw.jsonl").read_text().splitlines():
    if not l.strip(): continue
    r = json.loads(l); k = r.get("key", "")
    if r.get("kind") == "gen": gens[(r["point_id"], r["model"], r["cond"])] = r["text"]
    elif k.startswith("lab:"): labels[k] = r.get("move")

def move_of(prev_agent, text):
    """Replicate exp_condagree.label: interrupt -> strip (bare->critical); else hash (prev,text)."""
    if V.is_interrupt(text):
        rest = TAX._strip_interrupt(text)
        if not rest: return "critical"
        text = rest
    if not (text or "").strip() or str(text).startswith("Error:"): return None
    k = "lab:haiku:" + hashlib.sha256((V.truncate_words(prev_agent, 120) + "|" + V.truncate_words(text, 150)).encode()).hexdigest()[:24]
    return labels.get(k)

def excerpt(s, n=60):
    s = " ".join((s or "").split())
    w = s.split()
    return " ".join(w[:n]) + (" …" if len(w) > n else "")

out = {}
for model in MODELS:
    # per-developer CondAgree ±profile
    byu = defaultdict(lambda: {"g_hit": 0, "g_n": 0, "p_hit": 0, "p_n": 0})
    flips = {"win": [], "loss": []}  # win = profile right & generic wrong
    for pid, p in points.items():
        rm = move_of(p["prev_agent"], p["real_text"])
        if not rm: continue
        gm = move_of(p["prev_agent"], gens.get((pid, model, "generic"), ""))
        pm = move_of(p["prev_agent"], gens.get((pid, model, "distilled"), ""))
        if not gm or not pm: continue
        u = byu[p["slug"]]
        u["g_n"] += 1; u["p_n"] += 1
        if gm == rm: u["g_hit"] += 1
        if pm == rm: u["p_hit"] += 1
        rec = {"slug": p["slug"], "point_id": pid, "agent": excerpt(p["prev_agent"], 70),
               "real_msg": excerpt(p["real_text"], 55), "real_move": rm,
               "profile_msg": excerpt(gens.get((pid, model, "distilled"), ""), 55), "profile_move": pm,
               "generic_msg": excerpt(gens.get((pid, model, "generic"), ""), 55), "generic_move": gm}
        if pm == rm and gm != rm: flips["win"].append(rec)
        elif gm == rm and pm != rm: flips["loss"].append(rec)
    per_user = []
    for slug, u in byu.items():
        if u["g_n"] >= 5:
            g = u["g_hit"] / u["g_n"]; pp = u["p_hit"] / u["p_n"]
            per_user.append({"slug": slug, "n": u["g_n"], "generic_ca": round(g, 3), "profile_ca": round(pp, 3), "delta": round(pp - g, 3)})
    per_user.sort(key=lambda x: -x["delta"])
    out[model] = {"per_user": per_user, "n_win": len(flips["win"]), "n_loss": len(flips["loss"]),
                  "wins": flips["win"], "losses": flips["loss"]}

(EXP / "cases.json").write_text(json.dumps(out, indent=1))
# summary to stdout
for m in MODELS:
    d = out[m]; pu = d["per_user"]
    print(f"\n=== {m} ===  wins(profile right,generic wrong)={d['n_win']}  losses={d['n_loss']}")
    print("  top profile gainers:", [(u['slug'], u['delta']) for u in pu[:3]])
    print("  top profile losers: ", [(u['slug'], u['delta']) for u in pu[-3:]])
print(f"\nwrote {EXP/'cases.json'}")

"""Train/val/test split of SWE-chat with NON-OVERLAPPING users AND repos.

A user works in repos; a repo is touched by users. To guarantee no user OR repo crosses splits,
we take connected components of the user<->repo bipartite graph and assign whole components to
splits. Within each split, 'qualifying' eval-users (have a distilled profile digest + holdout, with
>= MIN_TURNS held-out user-action turns and >= MIN_SESS sessions / >= MIN_HOSESS held-out sessions)
are the usable pool. Greedy assignment targets enough qualifying users in val and test.
"""
import json, sys
from collections import defaultdict
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate as V

SESS_PARQUET = Path("/Users/kevin/Dev/swe-chat-scan/from_hf/sessions.parquet")
MIN_SESS, MIN_HOSESS, MIN_TURNS = 10, 4, 30
TARGET_FRAC = {"train": 0.45, "test": 0.35, "val": 0.20}  # of qualifying users; train largest


def heldout_turns(slug):
    p = ROOT / "data" / "holdout" / f"{slug}.json"
    if not p.exists():
        return 0, 0
    ho = json.loads(p.read_text())
    n = 0
    for s in ho["sessions"]:
        ts = s["turns"]
        for i, t in enumerate(ts):
            if t["role"] != "user" or t.get("is_continuation"):
                continue
            if not V.is_user_action_target(t.get("text")):
                continue
            if not (V.is_interrupt(t.get("text")) or len((t.get("text") or "").split()) >= 3):
                continue
            if not any(p2["role"] == "assistant" for p2 in ts[:i]):
                continue
            n += 1
    return n, len(ho["sessions"])


def main():
    sess = pd.read_parquet(SESS_PARQUET, columns=["user_id", "repo_id"])
    sess = sess[sess.user_id.notna() & sess.repo_id.notna()]
    # union-find over user nodes ("u:") and repo nodes ("r:")
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    user_sessions = defaultdict(int)
    user_repos = defaultdict(set)
    repo_users = defaultdict(set)
    for u, r in zip(sess.user_id, sess.repo_id):
        u, r = f"u:{u}", f"r:{r}"
        union(u, r); user_sessions[u] += 1; user_repos[u].add(r); repo_users[r].add(u)
    # components
    comp = defaultdict(lambda: {"users": set(), "repos": set()})
    for node in parent:
        root = find(node)
        (comp[root]["users"] if node.startswith("u:") else comp[root]["repos"]).add(node)
    comps = list(comp.values())

    # qualifying users (have profile digest+holdout and pass thresholds)
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text()) if (ROOT / "data/manifest.json").exists() else {}
    qual = {}  # slug -> stats
    for slug, m in manifest.items():
        tot = m.get("n_sessions", 0)
        nt, hs = heldout_turns(slug)
        if tot >= MIN_SESS and hs >= MIN_HOSESS and nt >= MIN_TURNS:
            qual[f"u:{slug}"] = {"slug": slug, "sessions": tot, "ho_sessions": hs, "ho_turns": nt}

    # per-component qualifying user list + size
    for c in comps:
        c["qual"] = [qual[u] for u in c["users"] if u in qual]
        c["n_users"] = len(c["users"]); c["n_repos"] = len(c["repos"])
        c["n_qual"] = len(c["qual"])
        c["sessions"] = sum(user_sessions[u] for u in c["users"])
    # assign whole components; qualifying ones to the split most below its target share (train largest),
    # non-qualifying components -> train (bulk raw data lives in train, conventional).
    comps.sort(key=lambda c: (-c["n_qual"], -c["sessions"]))
    total_q = sum(c["n_qual"] for c in comps) or 1
    splits = {"train": {"comps": []}, "val": {"comps": []}, "test": {"comps": []}}
    qcount = {"train": 0, "val": 0, "test": 0}
    for c in comps:
        if c["n_qual"] == 0:
            tgt = "train"
        else:
            deficit = {sp: TARGET_FRAC[sp] * total_q - qcount[sp] for sp in TARGET_FRAC}
            tgt = max(deficit, key=deficit.get)
        splits[tgt]["comps"].append(c); qcount[tgt] += c["n_qual"]

    out = {"thresholds": {"min_sessions": MIN_SESS, "min_ho_sessions": MIN_HOSESS, "min_ho_turns": MIN_TURNS}}
    for sp, d in splits.items():
        users = sorted(u[2:] for c in d["comps"] for u in c["users"])
        repos = sorted(r[2:] for c in d["comps"] for r in c["repos"])
        ql = sorted([q for c in d["comps"] for q in c["qual"]], key=lambda x: -x["ho_turns"])
        out[sp] = {"n_users": len(users), "n_repos": len(repos),
                   "n_sessions": sum(c["sessions"] for c in d["comps"]),
                   "n_qualifying": len(ql),
                   "qualifying_users": [q["slug"] for q in ql],
                   "qualifying_detail": ql, "all_users": users}
    # leakage assertions
    us = {sp: set(out[sp]["all_users"]) for sp in ["train", "val", "test"]}
    rs = {sp: set(r for c in splits[sp]["comps"] for r in c["repos"]) for sp in ["train", "val", "test"]}
    out["disjoint_users"] = all(us[a].isdisjoint(us[b]) for a, b in [("train","val"),("train","test"),("val","test")])
    out["disjoint_repos"] = all(rs[a].isdisjoint(rs[b]) for a, b in [("train","val"),("train","test"),("val","test")])
    out["largest_component"] = {"n_users": max(c["n_users"] for c in comps), "n_repos": max(c["n_repos"] for c in comps)}
    (ROOT / "bench/profileopt/splits.json").write_text(json.dumps(out, indent=1))

    print(f"components: {len(comps)} | largest: {out['largest_component']}")
    print(f"disjoint users: {out['disjoint_users']} | disjoint repos: {out['disjoint_repos']}\n")
    print(f"{'split':6s} {'users':>6} {'repos':>6} {'sessions':>9} {'qualifying':>11}")
    for sp in ["train", "val", "test"]:
        s = out[sp]
        print(f"{sp:6s} {s['n_users']:>6} {s['n_repos']:>6} {s['n_sessions']:>9} {s['n_qualifying']:>11}")
    for sp in ["test", "val", "train"]:
        print(f"\n{sp.upper()} qualifying eval-users ({out[sp]['n_qualifying']}):")
        for q in out[sp]["qualifying_detail"]:
            print(f"  {q['slug']:24s} sessions={q['sessions']:4d}  ho_sessions={q['ho_sessions']}  ho_turns={q['ho_turns']}")


if __name__ == "__main__":
    main()

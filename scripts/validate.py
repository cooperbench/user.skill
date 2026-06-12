#!/usr/bin/env python3
"""Validate distilled user folders by held-out next-message prediction.

For each validation user, for each held-out session, we pick prediction points
(real user turns with prior context). A role-play agent (claude -p) sees the real
conversation up to that point and produces the user's next message under three
conditions: with the user's distilled folder, with no folder, with a wrong user's
folder. We score generated vs. real with embedding cosine similarity, an LLM
judge (content + style), and a length-ratio fingerprint.

Usage:
  python3 scripts/validate.py --users 10            # stratified selection
  python3 scripts/validate.py --slugs a b c         # explicit users
Results stream to results/generations.jsonl (resumable); scored output goes to
results/validation_results.json.
"""

import argparse
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
GEN_MODEL = "claude-sonnet-4-6"
JUDGE_MODEL = "claude-haiku-4-5-20251001"
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # users prompt in several languages
CONDITIONS = ["distilled", "generic", "wrong"]
MAX_POINTS_PER_SESSION = 3
MAX_SESSIONS_PER_USER = 4
CONTEXT_TURNS = 14
CONTEXT_TURN_WORDS = 200
FOLDER_WORD_CAP = 8000
TIMEOUT_S = 240

FOLDER_FILES = ["USER.md", "STYLE.md", "PREFERENCES.md", "PERSONA.md", "PROJECTS.md"]


def truncate_words(text, n):
    words = (text or "").split()
    return " ".join(words[:n]) + (" […]" if len(words) > n else "")


def load_folder_text(slug):
    d = ROOT / "users" / slug
    parts = []
    for f in FOLDER_FILES:
        p = d / f
        if p.exists():
            parts.append(f"--- {f} ---\n{p.read_text()}")
    for p in sorted((d / "skills").glob("*.md")) if (d / "skills").exists() else []:
        parts.append(f"--- skills/{p.name} ---\n{p.read_text()}")
    return truncate_words("\n\n".join(parts), FOLDER_WORD_CAP)


def pick_points(holdout):
    """Choose prediction points: user turns with >=1 assistant turn before them."""
    points = []
    for sess in holdout["sessions"][:MAX_SESSIONS_PER_USER]:
        turns = sess["turns"]
        idxs = [i for i, t in enumerate(turns)
                if t["role"] == "user" and not t.get("is_continuation")
                and any(p["role"] == "assistant" for p in turns[:i])
                and len((t.get("text") or "").split()) >= 3]
        if not idxs:
            continue
        if len(idxs) > MAX_POINTS_PER_SESSION:  # spread across the session
            step = len(idxs) / MAX_POINTS_PER_SESSION
            idxs = [idxs[int(k * step)] for k in range(MAX_POINTS_PER_SESSION)]
        for i in idxs:
            points.append({
                "session_id": sess["session_id"], "repo": sess["repo"],
                "turn_index": i, "real": turns[i]["text"],
                "context": turns[max(0, i - CONTEXT_TURNS):i],
            })
    return points


def build_prompt(point, folder_text):
    ctx_lines = []
    for t in point["context"]:
        who = "DEVELOPER" if t["role"] == "user" else "AGENT"
        ctx_lines.append(f"[{who}]: {truncate_words(t['text'], CONTEXT_TURN_WORDS)}")
    ctx = "\n\n".join(ctx_lines)

    profile = (
        f"<user_profile>\n{folder_text}\n</user_profile>\n\n"
        "You are role-playing the developer described in the profile above. "
        if folder_text else
        "You are role-playing a software developer. "
    )
    return (
        f"{profile}"
        f"The developer is using an AI coding agent in the repository "
        f"`{point['repo']}`. The session so far:\n\n"
        f"<conversation>\n{ctx}\n</conversation>\n\n"
        "Write the developer's NEXT message to the agent. Output ONLY the literal text "
        "the developer would type — their language, length, casing, typos and all. "
        "No quotes, no commentary, no role labels."
    )


def run_claude(prompt, model, timeout=TIMEOUT_S):
    cmd = ["claude", "-p", prompt, "--model", model,
           "--disallowedTools", "Read,Write,Edit,Bash,Glob,Grep,Task,WebFetch,WebSearch",
           "--max-turns", "1"]
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return (res.stdout or "").strip()


def judge(real, generated, repo):
    prompt = (
        "Two messages were typed by a developer to an AI coding agent at the SAME point in the "
        f"SAME session (repo {repo}). Message A is real; message B is a simulation of the same "
        "developer.\n\n"
        f"A (real): {truncate_words(real, 300)}\n\n"
        f"B (simulated): {truncate_words(generated, 300)}\n\n"
        "Score B against A:\n"
        "- content: same intent/topic/request? (0=unrelated, 100=same ask)\n"
        "- style: same voice — length, language, casing, tone, formatting? "
        "(0=obviously different person, 100=indistinguishable)\n"
        'Respond with ONLY JSON: {"content": <int>, "style": <int>}'
    )
    out = run_claude(prompt, JUDGE_MODEL, timeout=120)
    m = re.search(r'\{[^{}]*"content"[^{}]*\}', out)
    if not m:
        return None, None
    try:
        d = json.loads(m.group(0))
        return int(d.get("content")), int(d.get("style"))
    except (ValueError, TypeError):
        return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=10)
    ap.add_argument("--slugs", nargs="*", default=None)
    ap.add_argument("--parallel", type=int, default=8)
    args = ap.parse_args()

    RESULTS.mkdir(exist_ok=True)
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text())

    if args.slugs:
        slugs = args.slugs
    else:  # stratified by session count among users with a distilled folder
        have_folder = [s for s in manifest if (ROOT / "users" / s / "USER.md").exists()]
        ranked = sorted(have_folder, key=lambda s: -manifest[s]["n_sessions"])
        step = max(1, len(ranked) // args.users)
        slugs = ranked[::step][:args.users]
    print(f"validation users: {slugs}")

    # wrong-folder pairing: rotate by one (derangement)
    wrong_of = {s: slugs[(i + 1) % len(slugs)] for i, s in enumerate(slugs)}

    folders = {s: load_folder_text(s) for s in slugs}
    for s, txt in folders.items():
        if not txt:
            raise SystemExit(f"no distilled folder for {s}; run distill.py first")

    # build all jobs
    jobs = []
    for slug in slugs:
        holdout = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
        points = pick_points(holdout)
        print(f"  {slug}: {len(points)} prediction points")
        for pi, point in enumerate(points):
            for cond in CONDITIONS:
                folder_text = {"distilled": folders[slug],
                               "generic": "",
                               "wrong": folders[wrong_of[slug]]}[cond]
                jobs.append({"slug": slug, "point_id": f"{point['session_id']}#{point['turn_index']}",
                             "cond": cond, "point": point,
                             "prompt": build_prompt(point, folder_text)})

    # resume: skip already-generated (slug, point_id, cond)
    gen_path = RESULTS / "generations.jsonl"
    done = set()
    if gen_path.exists():
        for line in gen_path.read_text().splitlines():
            r = json.loads(line)
            done.add((r["slug"], r["point_id"], r["cond"]))
    todo = [j for j in jobs if (j["slug"], j["point_id"], j["cond"]) not in done]
    print(f"jobs: {len(jobs)} total, {len(todo)} to run")

    def work(job):
        try:
            gen = run_claude(job["prompt"], GEN_MODEL)
        except subprocess.TimeoutExpired:
            gen = ""
        return {"slug": job["slug"], "point_id": job["point_id"], "cond": job["cond"],
                "repo": job["point"]["repo"], "real": job["point"]["real"],
                "generated": gen}

    with gen_path.open("a") as fh, ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futs = [ex.submit(work, j) for j in todo]
        for i, fut in enumerate(as_completed(futs), 1):
            rec = fut.result()
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            print(f"[gen {i}/{len(todo)}] {rec['slug']} {rec['cond']} "
                  f"({len(rec['generated'].split())}w)", flush=True)

    # ---- scoring ----
    records = [json.loads(l) for l in gen_path.read_text().splitlines()]
    records = [r for r in records
               if (r["slug"], r["point_id"], r["cond"]) in
                  {(j["slug"], j["point_id"], j["cond"]) for j in jobs}]

    print("embedding...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(EMBED_MODEL)
    reals = model.encode([r["real"] for r in records], normalize_embeddings=True)
    gens = model.encode([r["generated"] or " " for r in records], normalize_embeddings=True)
    for r, e_r, e_g in zip(records, reals, gens):
        r["cosine"] = round(float((e_r * e_g).sum()), 4)
        lr = len(r["real"].split())
        lg = len(r["generated"].split())
        r["len_ratio"] = round(min(lr, lg) / max(lr, lg), 3) if lr and lg else 0.0

    print("judging...")
    def judge_one(r):
        c, s = judge(r["real"], r["generated"], r["repo"])
        r["judge_content"], r["judge_style"] = c, s
        return r
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futs = [ex.submit(judge_one, r) for r in records if r["generated"]]
        for i, fut in enumerate(as_completed(futs), 1):
            if i % 20 == 0:
                print(f"[judge {i}/{len(futs)}]", flush=True)

    # ---- aggregate ----
    def agg(rows, key):
        vals = [r[key] for r in rows if r.get(key) is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    by_cond = {c: [r for r in records if r["cond"] == c] for c in CONDITIONS}
    summary = {c: {"n": len(rows), "cosine": agg(rows, "cosine"),
                   "judge_content": agg(rows, "judge_content"),
                   "judge_style": agg(rows, "judge_style"),
                   "len_ratio": agg(rows, "len_ratio")}
               for c, rows in by_cond.items()}

    # paired win rates on cosine and style: distilled vs each baseline
    by_key = {}
    for r in records:
        by_key.setdefault((r["slug"], r["point_id"]), {})[r["cond"]] = r
    wins = {f"distilled_vs_{b}": {"cosine": [0, 0], "judge_style": [0, 0]}
            for b in ["generic", "wrong"]}
    for conds in by_key.values():
        d = conds.get("distilled")
        for b in ["generic", "wrong"]:
            o = conds.get(b)
            if not d or not o:
                continue
            for metric in ["cosine", "judge_style"]:
                if d.get(metric) is None or o.get(metric) is None:
                    continue
                wins[f"distilled_vs_{b}"][metric][1] += 1
                if d[metric] > o[metric]:
                    wins[f"distilled_vs_{b}"][metric][0] += 1
    win_rates = {k: {m: (round(w / n, 3) if n else None)
                     for m, (w, n) in v.items()} for k, v in wins.items()}

    per_user = {}
    for slug in slugs:
        per_user[slug] = {c: {"cosine": agg([r for r in by_cond[c] if r["slug"] == slug], "cosine"),
                              "judge_style": agg([r for r in by_cond[c] if r["slug"] == slug], "judge_style"),
                              "judge_content": agg([r for r in by_cond[c] if r["slug"] == slug], "judge_content")}
                          for c in CONDITIONS}

    out = {"embed_model": EMBED_MODEL, "gen_model": GEN_MODEL, "judge_model": JUDGE_MODEL,
           "users": slugs, "wrong_pairing": wrong_of, "summary": summary,
           "win_rates": win_rates, "per_user": per_user, "records": records}
    (RESULTS / "validation_results.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({"summary": summary, "win_rates": win_rates}, indent=1))


if __name__ == "__main__":
    main()

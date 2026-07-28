#!/usr/bin/env python3
"""Run the user-simulator validation straight off the in-repo Harbor tasks/ — NO S3 needed.

Each tasks/<name>/ is one held-out prediction point: environment/history.md is the conversation
prefix, tests/gold.json has the real next message (`real`) + `prev_agent` + `developer` + point_id.
This reconstructs the point dicts validate.py expects and reuses its generation / judge / speech-act
machinery, so the output is a validation_results-shaped JSON that scripts/misprediction.py consumes
unchanged.

Coverage (from tasks/_manifest.json): 68 devs / 1520 tasks. The distilled+wrong conditions need a
users/<slug>/ folder; 16 gh devs have one (386 tasks). The generic condition runs for all 68.
No digests are needed (E1-E5 don't use the 2AFC); move labels are filled by taxonomy on the fly.

Usage:
  python3 scripts/validate_tasks.py --dry-run                       # parse only, no LLM calls
  python3 scripts/validate_tasks.py --folder-devs-only --mode folder --generate-only
  python3 scripts/validate_tasks.py --folder-devs-only              # full 3-condition run + scoring
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate as V  # generation, judge, speech_act, prompt builders, CLI-failure filter

TASKS = ROOT / "tasks"
RESULTS = ROOT / "results"
_ROLE = {"DEVELOPER": "user", "AGENT": "assistant", "SYSTEM": "system",
         "TOOL": "tool", "METADATA": "meta"}
_MARK = re.compile(r"^> (DEVELOPER|AGENT|SYSTEM|TOOL|METADATA)\s*$")


def dev_slug(dev):
    return dev.split(":")[-1]


def parse_history(path):
    """history.md -> list of {role, text}; keep only DEVELOPER/AGENT for the context window."""
    turns, role, buf = [], None, []
    for line in path.read_text().splitlines():
        m = _MARK.match(line)
        if m:
            if role is not None:
                turns.append({"role": role, "text": "\n".join(buf).strip()})
            role, buf = _ROLE[m.group(1)], []
        else:
            buf.append(line)
    if role is not None:
        turns.append({"role": role, "text": "\n".join(buf).strip()})
    return [t for t in turns if t["role"] in ("user", "assistant") and t["text"]]


def build_point(task_dir):
    gold = json.loads((task_dir / "tests" / "gold.json").read_text())
    hist = task_dir / "environment" / "history.md"
    if not gold.get("real") or not hist.exists():
        return None, None
    turns = parse_history(hist)
    ctx = turns[-V.CONTEXT_TURNS:]
    sid, _, ti = gold["point_id"].partition("#")
    point = {
        "session_id": sid, "turn_index": int(ti) if ti.isdigit() else 0,
        "repo": "the project", "real": gold["real"], "context": ctx,
        "prev_agent": gold.get("prev_agent", ""),
        "gold_move": gold.get("gold_move"),
    }
    return dev_slug(gold["developer"]), point


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["inline", "folder"], default="folder")
    ap.add_argument("--folder-devs-only", action="store_true",
                    help="restrict to devs that have a users/<slug>/ folder (enables distilled+wrong)")
    ap.add_argument("--conditions", nargs="*", default=None,
                    help="subset of distilled/generic/wrong (default: all when a folder exists, else generic)")
    ap.add_argument("--limit-per-dev", type=int, default=None, help="cap tasks per dev (spread evenly)")
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--generate-only", action="store_true")
    ap.add_argument("--score-only", action="store_true")
    ap.add_argument("--gen-file", default=None)
    ap.add_argument("--results-file", default=None)
    ap.add_argument("--dry-run", action="store_true", help="parse tasks and report coverage; no LLM calls")
    args = ap.parse_args()
    read_folder = args.mode == "folder"

    # ---- collect points by dev ----
    has_folder = lambda s: (ROOT / "users" / s / "USER.md").exists()
    by_dev = defaultdict(list)
    for td in sorted(TASKS.iterdir()):
        if not td.is_dir():
            continue
        slug, point = build_point(td)
        if point:
            by_dev[slug].append(point)
    if args.folder_devs_only:
        by_dev = {s: p for s, p in by_dev.items() if has_folder(s)}
    if args.limit_per_dev:
        for s, pts in by_dev.items():
            if len(pts) > args.limit_per_dev:
                step = len(pts) / args.limit_per_dev
                by_dev[s] = [pts[int(k * step)] for k in range(args.limit_per_dev)]

    devs = sorted(by_dev)
    folder_devs = [s for s in devs if has_folder(s)]
    n_pts = sum(len(p) for p in by_dev.values())
    print(f"devs: {len(devs)} ({len(folder_devs)} with folder) | points: {n_pts}")
    # wrong-pairing: rotate among folder devs (only they can be a 'wrong' source)
    wrong_of = {s: folder_devs[(i + 1) % len(folder_devs)] for i, s in enumerate(folder_devs)} \
        if len(folder_devs) > 1 else {}

    if args.dry_run:
        print("dry-run coverage by dev:")
        for s in devs:
            print(f"  {s:24s} points={len(by_dev[s]):3d} folder={has_folder(s)} "
                  f"wrong={wrong_of.get(s, '-')}")
        print(f"\nfolder devs (3-condition eligible): {folder_devs}")
        return

    def folder_path(s):
        return str((ROOT / "users" / s).relative_to(ROOT))

    # ---- build jobs ----
    jobs = []
    for slug in devs:
        conds = args.conditions or (V.CONDITIONS if has_folder(slug) else ["generic"])
        for point in by_dev[slug]:
            pid = f"{point['session_id']}#{point['turn_index']}"
            for cond in conds:
                if cond in ("distilled", "wrong") and not folder_devs:
                    continue
                src = {"distilled": slug, "generic": None, "wrong": wrong_of.get(slug)}[cond]
                if cond == "wrong" and not src:
                    continue
                fpath = folder_path(src) if src else None
                if read_folder:
                    prompt = V.build_folder_prompt(point, fpath)
                else:
                    ftext = V.load_folder_text(src) if src else ""
                    prompt = V.build_prompt(point, ftext)
                jobs.append({"slug": slug, "point_id": pid, "cond": cond, "point": point,
                             "prompt": prompt})

    gen_path = Path(args.gen_file) if args.gen_file else RESULTS / f"generations_tasks_{args.mode}.jsonl"
    RESULTS.mkdir(exist_ok=True)
    done = set()
    if args.score_only:
        print(f"score-only: loading {gen_path}")
    elif gen_path.exists():
        kept = []
        for line in gen_path.read_text().splitlines():
            r = json.loads(line)
            if V.is_cli_failure(r.get("generated", "")):
                continue
            done.add((r["slug"], r["point_id"], r["cond"]))
            kept.append(line)
        gen_path.write_text("\n".join(kept) + ("\n" if kept else ""))
    todo = [] if args.score_only else [j for j in jobs if (j["slug"], j["point_id"], j["cond"]) not in done]
    print(f"jobs: {len(jobs)} total, {len(todo)} to run (mode={args.mode})")

    def work(job):
        try:
            gen = V.run_claude(job["prompt"], V.GEN_MODEL, read_folder=read_folder)
        except Exception:
            gen = ""
        return {"slug": job["slug"], "point_id": job["point_id"], "cond": job["cond"],
                "repo": job["point"]["repo"], "real": job["point"]["real"], "generated": gen}

    if todo:
        with gen_path.open("a") as fh, ThreadPoolExecutor(max_workers=args.parallel) as ex:
            for i, fut in enumerate(as_completed([ex.submit(work, j) for j in todo]), 1):
                rec = fut.result()
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                if i % 20 == 0:
                    print(f"[gen {i}/{len(todo)}]", flush=True)

    # ---- scoring ----
    job_keys = {(j["slug"], j["point_id"], j["cond"]) for j in jobs}
    records = [json.loads(l) for l in gen_path.read_text().splitlines()]
    records = [r for r in records if (r["slug"], r["point_id"], r["cond"]) in job_keys
               and not V.is_cli_failure(r.get("generated", ""))]
    if args.generate_only:
        print(f"generate-only: {len(records)}/{len(jobs)} clean generations")
        return

    # point -> (prev_agent, real, gold_move) for move labeling
    pmeta = {}
    for slug in devs:
        for point in by_dev[slug]:
            pmeta[f"{point['session_id']}#{point['turn_index']}"] = point

    # A single slow/timed-out CLI call (e.g. a long non-English classification hitting the 90s
    # subprocess timeout) must NEVER kill the whole scoring pass — degrade it to None instead.
    def safe(fn, *a, default=None):
        try:
            return fn(*a)
        except Exception as e:  # subprocess.TimeoutExpired, transport errors, parse errors
            return default

    # ---- checkpointed scoring ----------------------------------------------------------------
    # One scoring pass makes ~3.5k CLI calls (judge + move labels); the usage window rarely covers
    # them all, and rate-limited calls come back None. So we CACHE every computed value to sidecar
    # files and only compute what is still missing — rerun --score-only across windows until full.
    # Move labels (needed by the misprediction analysis) are computed BEFORE judge scores so they
    # win the window.
    import threading
    SCORE_FIELDS = ("judge_content", "judge_style", "judge_realism", "pred_act")
    scores_path = RESULTS / f"scores_tasks_{args.mode}.jsonl"
    realacts_path = RESULTS / f"realacts_tasks_{args.mode}.json"

    def rkey(r):
        return f'{r["slug"]}|{r["point_id"]}|{r["cond"]}'

    # load caches
    real_acts = json.loads(realacts_path.read_text()) if realacts_path.exists() else {}
    cache = {}
    if scores_path.exists():
        for line in scores_path.read_text().splitlines():
            e = safe(json.loads, line, default=None)
            if not e:
                continue
            slot = cache.setdefault(e["k"], {})
            for f in SCORE_FIELDS:
                if e.get(f) is not None:
                    slot[f] = e[f]
    for r in records:
        for f, v in cache.get(rkey(r), {}).items():
            r[f] = v

    lock = threading.Lock()
    sfh = scores_path.open("a")
    def persist(r):
        with lock:
            sfh.write(json.dumps({"k": rkey(r), **{f: r.get(f) for f in SCORE_FIELDS}},
                                 ensure_ascii=False) + "\n")
            sfh.flush()

    # 1) real move label per unique point (cheapest + most important); skip already-cached
    todo_real = [pid for pid in pmeta if not real_acts.get(pid)]
    print(f"labeling real moves: {len(todo_real)}/{len(pmeta)} missing")
    def label_real(pid):
        p = pmeta.get(pid, {})
        return pid, (p.get("gold_move") or safe(V.speech_act, p.get("real", ""), p.get("prev_agent", "")))
    if todo_real:
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            for fut in as_completed([ex.submit(label_real, pid) for pid in todo_real]):
                pid, act = fut.result()
                if act:
                    real_acts[pid] = act
        realacts_path.write_text(json.dumps(real_acts, ensure_ascii=False))

    # 2) per-record: predicted move first (feeds E2-E5), then judge axes; compute only if missing
    def score_one(r):
        changed = False
        if r.get("pred_act") is None and r["generated"]:
            pa = pmeta.get(r["point_id"], {}).get("prev_agent", "")
            pv = safe(V.speech_act, r["generated"], pa)
            if pv is not None:
                r["pred_act"] = pv
                changed = True
        if r.get("judge_realism") is None and r["generated"]:
            c, s, rl = safe(V.judge, r["real"], r["generated"], r["repo"], default=(None, None, None))
            if rl is not None:
                r["judge_content"], r["judge_style"], r["judge_realism"] = c, s, rl
                changed = True
        if changed:
            persist(r)
        return r
    todo_score = [r for r in records if r["generated"]
                  and (r.get("pred_act") is None or r.get("judge_realism") is None)]
    print(f"scoring records: {len(todo_score)}/{len(records)} need pred_act and/or judge")
    if todo_score:
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            list(as_completed([ex.submit(score_one, r) for r in todo_score]))
    sfh.close()

    # 3) attach real_act + act_match to every record from the (now updated) cache
    for r in records:
        r["real_act"] = real_acts.get(r["point_id"])
        r["act_match"] = (r.get("pred_act") is not None and r.get("pred_act") == r.get("real_act"))

    # report remaining gaps so the caller knows whether another --score-only pass is needed
    miss_real = sum(1 for r in records if not r.get("real_act"))
    miss_pred = sum(1 for r in records if not r.get("pred_act"))
    miss_judge = sum(1 for r in records if r.get("judge_realism") is None)
    print(f"after pass: missing real_act={miss_real} pred_act={miss_pred} judge={miss_judge} "
          f"(of {len(records)}) — rerun --score-only if nonzero")

    # ---- aggregate (validation_results shape) ----
    def agg(rows, key):
        vals = [r[key] for r in rows if r.get(key) is not None]
        return round(sum(vals) / len(vals), 3) if vals else None
    def match_rate(rows):
        v = [r["act_match"] for r in rows if r.get("real_act") and r.get("pred_act")]
        return round(sum(v) / len(v), 3) if v else None

    AXES = ["judge_content", "judge_style", "judge_realism"]
    by_cond = {c: [r for r in records if r["cond"] == c] for c in V.CONDITIONS}
    summary = {c: {"n": len(rs), "cosine": None, "act_match": match_rate(rs),
                   **{a: agg(rs, a) for a in AXES}} for c, rs in by_cond.items() if rs}
    real_act_dist = dict(Counter(a for a in real_acts.values() if a))
    act_confusion = {c: dict(Counter(f"{r.get('real_act')}>{r.get('pred_act')}"
                             for r in by_cond[c] if r.get("real_act") and r.get("pred_act")))
                     for c in V.CONDITIONS if by_cond.get(c)}
    per_user = {s: {c: {"act_match": match_rate([r for r in by_cond.get(c, []) if r["slug"] == s]),
                        **{a: agg([r for r in by_cond.get(c, []) if r["slug"] == s], a) for a in AXES}}
                    for c in V.CONDITIONS} for s in devs}

    out = {"mode": args.mode, "source": "tasks/", "gen_model": V.GEN_MODEL, "judge_model": V.JUDGE_MODEL,
           "users": devs, "folder_devs": folder_devs, "wrong_pairing": wrong_of,
           "summary": summary, "real_act_distribution": real_act_dist, "act_confusion": act_confusion,
           "per_user": per_user, "records": records}
    rp = Path(args.results_file) if args.results_file else RESULTS / f"validation_tasks_{args.mode}.json"
    rp.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({"summary": summary, "n_records": len(records)}, indent=1))
    print(f"wrote {rp.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

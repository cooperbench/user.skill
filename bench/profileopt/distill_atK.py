"""Build K-turn digests and re-distill profiles from them (production distill-user recipe).

For each test dev and K in {8,32,64}: construct a digest JSON (same schema as
scripts/prepare_data.py) from only the K most recent train turns, then run the same headless
`claude -p` + .claude/skills/distill-user recipe as scripts/distill.py, writing
users_atK/<slug>_K{K}/. Skips completed folders, so it's resumable.
"""
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate as V  # noqa: E402

EXP = HERE / "experiments" / "condagree_multi"
KS = [8, 32, 64]
REQUIRED = ["USER.md", "PERSONA.md", "STYLE.md", "PREFERENCES.md", "PROJECTS.md", "stats.json"]
MODEL = "claude-sonnet-4-6"
TIMEOUT_S = 900
PARALLEL = 6

TEST = json.loads((HERE / "splits.json").read_text())["test"]["qualifying_users"]
TRAIN = json.loads((EXP / "train_turns.json").read_text())


def dist(vals):
    c = Counter(v for v in vals if v)
    return dict(c.most_common(10))


def build_digest(slug, k):
    turns = TRAIN[slug]["turns"][-k:]
    prod = json.loads((ROOT / "data" / "digests" / f"{slug}.json").read_text())
    stats = dict(prod["stats"])
    stats["n_prompts_train"] = len(turns)
    stats["intent_distribution"] = dist(t["intent"] for t in turns)
    stats["pushback_distribution"] = dist(t["pushback"] for t in turns)
    stats["note"] = f"K-turn ablation digest: only the {len(turns)} most recent train prompts."
    opening = [{"repo": t["repo"], "intent": t["intent"], "text": t["text"]}
               for t in turns if t["is_first_turn"]]
    mid = [{"intent": t["intent"], "pushback": t["pushback"], "text": t["text"]}
           for t in turns if not t["is_first_turn"]]
    pushback = [{"type": t["pushback"], "agent_said": t["prev_agent"], "user_replied": t["text"]}
                for t in turns if t["pushback"] and t["pushback"] != "non_pushback"]
    return {"stats": stats, "opening_prompts": opening,
            "mid_session_prompts": mid, "pushback_examples": pushback}


def distill_one(job):
    slug, k = job
    out_dir = ROOT / "users_atK" / f"{slug}_K{k}"
    if all((out_dir / f).exists() for f in REQUIRED):
        return slug, k, "skipped (exists)"
    dig_dir = ROOT / "data" / "digests_atK"
    dig_dir.mkdir(parents=True, exist_ok=True)
    dig = dig_dir / f"{slug}_K{k}.json"
    dig.write_text(json.dumps(build_digest(slug, k), indent=1, ensure_ascii=False))
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt = (f"Read the skill file .claude/skills/distill-user/SKILL.md and follow it exactly "
              f"with $1=data/digests_atK/{slug}_K{k}.json and $2=users_atK/{slug}_K{k}/. "
              f"Create every required file. Work autonomously; do not ask questions.")
    cmd = ["claude", "-p", prompt, "--model", MODEL,
           "--allowedTools", "Read,Write,Glob", "--permission-mode", "acceptEdits",
           "--max-turns", "40"]
    try:
        subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return slug, k, "ERROR: timeout"
    missing = [f for f in REQUIRED if not (out_dir / f).exists()]
    return slug, k, (f"ERROR: missing {missing}" if missing else "ok")


if __name__ == "__main__":
    jobs = [(s, k) for k in KS for s in TEST]
    print(f"{len(jobs)} distill jobs (parallel {PARALLEL})")
    with ThreadPoolExecutor(max_workers=PARALLEL) as ex:
        for f in as_completed([ex.submit(distill_one, j) for j in jobs]):
            slug, k, status = f.result()
            print(f"  {slug}_K{k}: {status}", flush=True)
    bad = [(s, k) for k in KS for s in TEST
           if not all((ROOT / "users_atK" / f"{s}_K{k}" / f).exists() for f in REQUIRED)]
    print(f"\ndone; incomplete: {bad if bad else 'none'}")

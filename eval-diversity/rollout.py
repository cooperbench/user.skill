#!/usr/bin/env python3
"""Multi-turn rollout driver for the diversity study.

For each seed task and each arm (no-profile baseline at matched temp, no-profile at
high temp, and N profile-conditioned users), run a simulator<->agent loop: the agent
acts on a checked-out repo, the simulated user reacts, repeat until the user is done.
We record the full turn list + final `git diff` per rollout; scoring (Vendi / patch
diversity / structure entropy / realism / distance-to-real) is score.py.

Usage:
  python3 eval-diversity/rollout.py --seeds eval-diversity/seeds.example.json \
      --profiles me me-v2 --k 4
Rollouts stream to eval-diversity/rollouts.jsonl (resumable, one line per rollout).
"""

import argparse
import json
import subprocess
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SIM_MODEL = "claude-sonnet-4-6"
AGENT_MODEL = "claude-sonnet-4-6"
MAX_TURNS = 20            # hard ceiling; the user usually ends earlier via <DONE>
MIN_TURNS = 2            # rollouts shorter than this are dropped at scoring time
DONE_TOKEN = "<DONE>"
FOLDER_FILES = ["USER.md", "STYLE.md", "PREFERENCES.md", "PERSONA.md", "PROJECTS.md"]


def load_folder_text(slug):
    d = ROOT / "users" / slug
    parts = [f"--- {f} ---\n{(d / f).read_text()}" for f in FOLDER_FILES if (d / f).exists()]
    sk = d / "skills"
    parts += [f"--- skills/{p.name} ---\n{p.read_text()}" for p in sorted(sk.glob('*.md'))] if sk.exists() else []
    return "\n\n".join(parts)


def render_history(turns):
    return "\n\n".join(f"[{'AGENT' if t['role']=='assistant' else 'DEVELOPER'}]: {t['text']}"
                       for t in turns)


def simulate_user_turn(folder_text, repo, turns):
    """One simulated user message. Returns the literal text, possibly DONE_TOKEN.

    The instruction text is byte-identical across arms; the ONLY difference is whether
    the <user_profile> block is present, so any behavioral gap is attributable to it.
    """
    profile = (f"<user_profile>\n{folder_text}\n</user_profile>\n\nYou ARE this developer. "
               if folder_text else "You are a software developer. ")
    prompt = (f"{profile}You are using an AI coding agent in `{repo}`. The session so far:\n\n"
              f"<conversation>\n{render_history(turns)}\n</conversation>\n\n"
              "Write your NEXT message to the agent — only the literal text you would type, "
              f"no commentary. If you are satisfied and would end the session, output exactly: {DONE_TOKEN}")
    cmd = ["claude", "-p", prompt, "--model", SIM_MODEL,
           "--disallowedTools", "Read,Write,Edit,Bash,Glob,Grep,Task,WebFetch,WebSearch,NotebookEdit",
           "--max-turns", "8"]
    try:
        out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        return ""
    return (out.stdout or "").strip()


def agent_turn(session_id, user_msg, repo_dir, first):
    """Send a user message to the agent session; it acts on repo_dir. Returns reply text."""
    base = ["claude", "-p", user_msg, "--model", AGENT_MODEL, "--output-format", "json",
            "--allowedTools", "Read,Edit,Write,Bash,Glob,Grep", "--permission-mode", "acceptEdits"]
    cmd = base + (["--session-id", session_id] if first else ["--resume", session_id])
    try:
        out = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return ""
    try:
        return json.loads(out.stdout).get("result", "")
    except (ValueError, AttributeError):
        return (out.stdout or "").strip()


def git_diff(repo_dir):
    return subprocess.run(["git", "-C", str(repo_dir), "diff"],
                          capture_output=True, text=True).stdout


def user_continues(turns, n_turns, last_user_msg):
    """Decide whether the simulated user keeps going, and with what message.

    Returns (continue: bool, message: str | None). This is the termination/satisfaction
    policy and it directly shapes trajectory-length diversity — a core axis of the study.

    We trust the persona's own <DONE> signal so that session length is *persona-driven*
    rather than a fixed budget (a vibe-coder ends in 2 turns; a nitpicker keeps steering).
    The only hard guards are: never feed an empty/failed generation to the agent, and the
    MAX_TURNS ceiling enforced by the caller. The MIN_TURNS floor is applied at scoring
    time (so we keep the honest signal that some personas really do stop fast) rather than
    fabricated here, since on an early <DONE> we have no real follow-up message to send.
    """
    text = (last_user_msg or "").strip()
    if not text or DONE_TOKEN in text:
        return False, None
    return True, text


def restore_repo(repo_dir):
    """Reset the checkout so each rollout starts from the same base state."""
    subprocess.run(["git", "-C", str(repo_dir), "reset", "--hard"], capture_output=True, text=True)
    subprocess.run(["git", "-C", str(repo_dir), "clean", "-fd"], capture_output=True, text=True)


def run_rollout(arm, seed, folder_text):
    repo_dir = Path(seed["repo_dir"])
    restore_repo(repo_dir)
    session_id = str(uuid.uuid4())
    turns = []
    user_msg = seed["task"]
    stopped = "max_turns"
    for i in range(MAX_TURNS):
        reply = agent_turn(session_id, user_msg, repo_dir, first=(i == 0))
        turns.append({"role": "user", "text": user_msg})
        turns.append({"role": "assistant", "text": reply})
        nxt = simulate_user_turn(folder_text, seed["repo"], turns)
        cont, msg = user_continues(turns, i + 1, nxt)
        if not cont:
            stopped = "empty" if not (nxt or "").strip() else "done"
            break
        user_msg = msg
    diff = git_diff(repo_dir)
    restore_repo(repo_dir)
    return {"arm": arm, "seed": seed["id"], "repo": seed["repo"], "turns": turns,
            "n_turns": len([t for t in turns if t["role"] == "user"]),
            "stopped": stopped, "final_diff": diff}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", required=True, help="json: [{id, repo, repo_dir, task}, ...]")
    ap.add_argument("--profiles", nargs="*", default=[], help="user slugs for the profile arm")
    ap.add_argument("--k", type=int, default=4, help="profile rollouts per seed (one slug each)")
    args = ap.parse_args()

    seeds = json.loads(Path(args.seeds).read_text())
    folders = {s: load_folder_text(s) for s in args.profiles}
    for s, txt in folders.items():
        if not txt:
            raise SystemExit(f"no user folder for '{s}' under users/; run distillation first")
    out_path = HERE / "rollouts.jsonl"

    # resume: skip (seed, arm, profile, run) already recorded
    done = set()
    if out_path.exists():
        for line in out_path.read_text().splitlines():
            r = json.loads(line)
            done.add((r["seed"], r["arm"], r.get("profile"), r.get("run", 0)))

    k = args.k
    profs = args.profiles[:k]
    with out_path.open("a") as fh:
        for seed in seeds:
            # matched sample size per arm per seed: K runs each, so within-seed diversity
            # is comparable. baselines repeat the same settings (measures intrinsic spread);
            # the profile arm uses a different user folder per run.
            jobs = ([("baseline-T", None, i) for i in range(k)]
                    + [("baseline-Thigh", None, i) for i in range(k)]
                    + [("profile", s, i) for i, s in enumerate(profs)])
            for arm, slug, run in jobs:
                if (seed["id"], arm, slug, run) in done:
                    continue
                rec = run_rollout(arm, seed, folders.get(slug, ""))
                rec["profile"], rec["run"] = slug, run
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                print(f"[{seed['id']}] {arm}{'/' + slug if slug else ''} #{run}: "
                      f"{rec['n_turns']} turns ({rec['stopped']})", flush=True)


if __name__ == "__main__":
    main()

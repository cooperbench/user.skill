#!/usr/bin/env python3
"""Closed-loop SESSION simulation against a real held-out session.

Reconstructs the starting codebase state (clone the repo, checkout the parent of the session's
first commit), seeds the real opening task, then lets the v5 user-simulator DRIVE a real Claude
Code agent through the session: agent works in the repo, simulator reacts (move-sampled from the
user's prior, rendered in their voice, with read access to the live repo), for up to K turns.

Outputs the simulated transcript + per-turn moves/files, for distributional comparison to the
real session (scripts/session_compare.py).

Usage: session_sim.py <slug> <session_id_prefix> [--turns 12]
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V

ROOT = Path(__file__).resolve().parent.parent
WORK = Path("/tmp/session_sim")
AGENT_MODEL = "claude-sonnet-4-6"


def sh(cmd, cwd=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def reconstruct(repo_id, first_sha):
    """Clone repo and checkout the parent of the session's first commit = pre-session state."""
    WORK.mkdir(parents=True, exist_ok=True)
    repo_dir = WORK / repo_id.replace("/", "__")
    if repo_dir.exists():
        sh(["rm", "-rf", str(repo_dir)])
    r = sh(["git", "clone", "--quiet", f"https://github.com/{repo_id}.git", str(repo_dir)], timeout=300)
    if r.returncode != 0:
        raise SystemExit(f"clone failed: {r.stderr[:200]}")
    par = sh(["git", "rev-parse", f"{first_sha}^"], cwd=repo_dir)
    if par.returncode != 0:
        raise SystemExit(f"cannot resolve {first_sha}^: {par.stderr[:200]}")
    parent = par.stdout.strip()
    sh(["git", "checkout", "--quiet", parent], cwd=repo_dir)
    sh(["git", "checkout", "--quiet", "-b", "sim"], cwd=repo_dir)
    return repo_dir, parent


def run_agent(msg, session_id, cwd):
    """One agent turn (real Claude Code, full tools, in the repo). Returns (text, session_id)."""
    cmd = ["claude", "-p", msg, "--model", AGENT_MODEL,
           "--allowedTools", "Read,Glob,Grep,Edit,Write,Bash",
           "--permission-mode", "acceptEdits", "--max-turns", "30",
           "--output-format", "json"]
    if session_id:
        cmd += ["--resume", session_id]
    r = sh(cmd, cwd=cwd, timeout=600)
    try:
        d = json.loads(r.stdout)
        return (d.get("result") or "").strip(), d.get("session_id") or session_id
    except (ValueError, json.JSONDecodeError):
        return (r.stdout or "").strip(), session_id


def files_touched(repo_dir):
    r = sh(["git", "status", "--porcelain"], cwd=repo_dir)
    return sorted(line[3:] for line in r.stdout.splitlines() if line.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("session_prefix")
    ap.add_argument("--turns", type=int, default=12)
    args = ap.parse_args()

    # --- locate the real session, its repo and first commit ---
    import pandas as pd
    sessions = pd.read_parquet(ROOT.parent / "SWE-chat" / "sessions.parquet",
                               columns=["session_id", "repo_id", "canonical_checkpoint_pk", "checkpoint_ids"])
    row = sessions[sessions.session_id.str.startswith(args.session_prefix)].iloc[0]
    sid_full, repo_id = row.session_id, row.repo_id
    cps = (json.loads(row.checkpoint_ids) if row.checkpoint_ids else []) + [row.canonical_checkpoint_pk]
    commits = pd.read_parquet(ROOT.parent / "SWE-chat" / "commits.parquet",
                              columns=["commit_sha", "checkpoint_pk", "author_date"])
    cc = commits[commits.checkpoint_pk.isin(cps)].sort_values("author_date")
    first_sha = cc.iloc[0].commit_sha
    print(f"session {sid_full[:12]} repo {repo_id} first_commit {first_sha[:10]}")

    # --- real session opening (seed) ---
    ho = json.loads((ROOT / "data" / "holdout" / f"{args.slug}.json").read_text())
    real = [s for s in ho["sessions"] if s["session_id"] == sid_full][0]
    real_user_turns = [t["text"] for t in real["turns"] if t["role"] == "user"]
    opening = real_user_turns[0]

    repo_dir, parent = reconstruct(repo_id, first_sha)
    print(f"reconstructed pre-session state at {parent[:10]} ({len(files_touched(repo_dir))} dirty files)")

    prior = V.derive_move_prior(json.loads((ROOT / "users" / args.slug / "stats.json").read_text()))
    fpath = f"users/{args.slug}"

    transcript = []       # [{role, text, move?, files_after?}]
    convo = []            # for the simulator's context: [{role, text}]
    session_id = None
    user_msg = opening
    transcript.append({"role": "user", "text": user_msg, "move": "opening(seed)"})
    convo.append({"role": "user", "text": user_msg})

    for turn in range(args.turns):
        # agent acts
        resp, session_id = run_agent(user_msg, session_id, repo_dir)
        touched = files_touched(repo_dir)
        transcript.append({"role": "assistant", "text": resp[:4000], "files_after": touched})
        convo.append({"role": "assistant", "text": resp})
        print(f"[turn {turn}] agent: {len(resp.split())}w, {len(touched)} files touched")

        # simulator reacts (v5: sample move from prior, render in voice, repo access)
        move = V.sample_move(prior, f"{sid_full}#sim{turn}")
        point = {"repo": repo_id, "repo_path": str(repo_dir),
                 "session_id": sid_full, "turn_index": f"sim{turn}",
                 "context": convo[-V.CONTEXT_TURNS:]}
        prompt = V.build_folder_prompt(point, fpath, target_move=move)
        nxt = V.run_claude(prompt, V.GEN_MODEL, read_folder=True)
        if not nxt or V.is_cli_failure(nxt):
            print("  simulator produced no message; ending session")
            break
        transcript.append({"role": "user", "text": nxt, "move": move})
        convo.append({"role": "user", "text": nxt})
        print(f"  sim user [{move}]: {nxt[:80]!r}")
        user_msg = "[the developer interrupts]" if V.is_interrupt(nxt) else nxt

    out = {"slug": args.slug, "session_id": sid_full, "repo_id": repo_id,
           "parent_sha": parent, "turns": args.turns,
           "real_user_turns": real_user_turns,
           "simulated_transcript": transcript,
           "final_files_touched": files_touched(repo_dir)}
    outp = ROOT / "results" / f"session_sim_{args.slug}_{args.session_prefix}.json"
    outp.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"\nwrote {outp}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Batch driver for the distill-user skill.

For each user digest, runs a headless Claude Code agent (`claude -p`) that follows
.claude/skills/distill-user/SKILL.md and writes users/<slug>/. The skill is the
pipeline; this script only fans it out and checks completeness.

Usage:
  python3 scripts/distill.py --slugs marcus-sa dayhaysoos     # specific users
  python3 scripts/distill.py --all                            # every digest
  python3 scripts/distill.py --all --redo                     # overwrite existing
"""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["USER.md", "PERSONA.md", "STYLE.md", "PREFERENCES.md",
            "PROJECTS.md", "stats.json"]
MODEL = "claude-sonnet-4-6"
TIMEOUT_S = 900


def distill_one(slug: str, redo: bool) -> tuple[str, str]:
    out_dir = ROOT / "users" / slug
    if not redo and all((out_dir / f).exists() for f in REQUIRED):
        return slug, "skipped (exists)"
    digest = ROOT / "data" / "digests" / f"{slug}.json"
    if not digest.exists():
        return slug, "ERROR: no digest"
    out_dir.mkdir(parents=True, exist_ok=True)

    prompt = (
        f"Read the skill file .claude/skills/distill-user/SKILL.md and follow it exactly "
        f"with $1=data/digests/{slug}.json and $2=users/{slug}/. "
        f"Create every required file. Work autonomously; do not ask questions."
    )
    cmd = [
        "claude", "-p", prompt,
        "--model", MODEL,
        "--allowedTools", "Read,Write,Glob",
        "--permission-mode", "acceptEdits",
        "--max-turns", "40",
    ]
    try:
        res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                             timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return slug, "ERROR: timeout"
    missing = [f for f in REQUIRED if not (out_dir / f).exists()]
    if missing:
        err = (res.stderr or res.stdout or "")[-300:]
        return slug, f"ERROR: missing {missing} rc={res.returncode} tail={err!r}"
    n_skills = len(list((out_dir / "skills").glob("*.md"))) if (out_dir / "skills").exists() else 0
    return slug, f"ok ({n_skills} skills)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slugs", nargs="*", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--parallel", type=int, default=8)
    args = ap.parse_args()

    manifest = json.loads((ROOT / "data" / "manifest.json").read_text())
    if args.all:
        slugs = list(manifest)
    elif args.slugs:
        slugs = args.slugs
    else:
        sys.exit("specify --slugs ... or --all")

    failures = 0
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futures = {ex.submit(distill_one, s, args.redo): s for s in slugs}
        for i, fut in enumerate(as_completed(futures), 1):
            slug, status = fut.result()
            if status.startswith("ERROR"):
                failures += 1
            print(f"[{i}/{len(slugs)}] {slug:30s} {status}", flush=True)

    print(f"\ndone: {len(slugs) - failures}/{len(slugs)} succeeded")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

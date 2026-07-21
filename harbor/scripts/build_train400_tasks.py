#!/usr/bin/env python3
"""Build UserBench train400 Hub twin by sampling from GitHub train pools.

Reads full leak-safe pools from user-simulator/train_pools/ (or --pools),
allocates B human-turns via sqrt_two_stage, and writes Harbor tasks under
datasets/eval-train400/. Same held history, dynamic Composer 2.5 multi-label
verifier, and gold as eval-620; adds /sim/train/.

Future budgets (1000+) use the same pools + sampler with --budget N.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import shutil
import sys
import tomllib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path("/data/swesimbench-v2-harbor")
sys.path.insert(0, str(HERE / "scripts"))
sys.path.insert(0, "/data/claude-crawl")

from cohort_policy import is_human_target, scrub_text  # noqa: E402
from prototype_train400_sampler import (  # noqa: E402
    alloc_sqrt_two_stage,
    parse_ts,
)

SRC_EVAL = HERE / "datasets" / "eval-620"
OUT_EVAL = HERE / "datasets" / "eval-train400"
PACK_CACHE = HERE / "datasets" / "_train400_packs"
DEFAULT_POOLS = Path("/data/user-simulator/train_pools")
META_OUT = HERE / "meta" / "train400_build_report.json"

B_DEFAULT = 400
CTX_WORDS = 200
TIGHT_MARGIN = 80

ROLE_LABELS = {
    "user": "DEVELOPER",
    "assistant": "AGENT",
    "system": "SYSTEM",
    "tool": "TOOL",
    "metadata": "METADATA",
}

INSTRUCTION = """\
You are role-playing the software developer in an ongoing AI coding-agent session.

The full conversation so far is in `/sim/history.md`. Each turn starts with a markdown
blockquote role label (`> DEVELOPER`, `> AGENT`, `> SYSTEM`, `> TOOL`, or `> METADATA`),
then the turn body. `DEVELOPER` is the human to imitate; `AGENT` is their coding agent.
`SYSTEM`, `TOOL`, and `METADATA` are context observed by the original agent, not
developer-authored messages. It MAY be long (thousands of lines) — read it however you
need: `cat`, `tail`, `head`, `grep`, `sed`, etc.

Earlier sessions from this same developer are under `/sim/train/` (past messages from
earlier sessions, as indexed under `/sim/train/`). Start with `/sim/train/_index.json`
for the session list (ids, timestamps, repos, turn counts, and paths), then open the
matching `*.md` transcripts. They use the same role-label format as `history.md`.
Skim or search them as needed for how this developer writes — they are prior evidence,
not the chat to continue.

Your job: write the SINGLE next message THIS developer would type to their coding agent right
now — in their own language, length, casing, punctuation, typos and all. Do not solve their
problem, do not explain, do not add role labels or quotes — just the literal message text they
would send.

Write ONLY that literal message to `/sim/answer.txt` (overwrite it). No commentary anywhere else.
"""

DOCKERFILE = """\
FROM python:3.12-slim

RUN apt-get update \\
 && apt-get install -y --no-install-recommends curl build-essential git \\
 && rm -rf /var/lib/apt/lists/*

# Non-root agent user (matches task.toml [agent] user = "agent")
RUN useradd --create-home --shell /bin/bash agent \\
 && mkdir -p /sim && chown -R agent:agent /sim

WORKDIR /sim
COPY history.md /sim/history.md
RUN chown -R agent:agent /sim/history.md
COPY train/ /sim/train/
RUN chown -R agent:agent /sim/train
# Seed an empty answer file the agent will overwrite.
RUN touch /sim/answer.txt && chown agent:agent /sim/answer.txt
"""


def tw(text: str, n: int = CTX_WORDS) -> str:
    words = (text or "").split()
    if len(words) <= n:
        return text or ""
    return " ".join(words[:n]) + " […]"


def safe_sid(sid: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", sid)


def format_turn(role: str, text: str) -> str:
    label = ROLE_LABELS.get(role, "METADATA")
    body = tw(scrub_text(text or "")).rstrip()
    return f"> {label}\n\n{body}"


def render_prefix(turns: list, human_take: int) -> str:
    seen = 0
    parts = []
    for t in turns:
        parts.append(format_turn(t.get("role"), t.get("text")))
        if t.get("role") == "user" and is_human_target(t):
            seen += 1
            if seen >= human_take:
                break
    body = "\n\n".join(parts)
    return body + ("\n" if body and not body.endswith("\n") else "")


def task_developer(task_dir: Path) -> str:
    data = tomllib.loads((task_dir / "task.toml").read_text())
    return data["metadata"]["developer"]


def rewrite_task_toml(src: Path, dst: Path) -> None:
    text = src.read_text()
    text = text.replace('condition = "noprofile"', 'condition = "train400"')
    text = text.replace('"noprofile"', '"train400"')
    dst.write_text(text)


def hardlink_or_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def pool_session_files(dev_dir: Path, meta: dict) -> list[Path]:
    """Resolve sessions.jsonl.gz and/or sharded sessions_XXX.jsonl.gz."""
    named = meta.get("sessions_files")
    if named:
        return [dev_dir / n for n in named]
    single = meta.get("sessions_file") or "sessions.jsonl.gz"
    p = dev_dir / single
    if p.exists():
        return [p]
    shards = sorted(dev_dir.glob("sessions_*.jsonl.gz"))
    if shards:
        return shards
    raise FileNotFoundError(f"no sessions*.jsonl.gz in {dev_dir}")


def load_pool(dev_dir: Path) -> tuple[dict, list[dict]]:
    meta = json.loads((dev_dir / "_meta.json").read_text())
    sessions = []
    for path in pool_session_files(dev_dir, meta):
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    sessions.append(json.loads(line))
    sessions.sort(key=lambda x: (x["ts"], x["sid"]))
    return meta, sessions


def verify_session_vs_tstar(sess: dict, tstar: str) -> list[str]:
    cut = parse_ts(tstar)
    viol = []
    if cut is None:
        return [f"invalid T*: {tstar!r}"]
    st = parse_ts(sess.get("ts"))
    if st is not None and st >= cut:
        viol.append(f"session.ts >= T* sid={sess['sid']}")
    end = parse_ts(sess.get("max_turn_ts"))
    if end is None:
        # compute from turns if needed
        for t in sess.get("turns") or []:
            dt = parse_ts(t.get("ts"))
            if dt is not None and (end is None or dt > end):
                end = dt
    if end is not None and end >= cut:
        viol.append(f"max(turn.ts) >= T* sid={sess['sid']}")
    if end is None:
        viol.append(f"missing max_turn_ts sid={sess['sid']}")
    return viol


def write_pack(
    pack_dir: Path,
    alloc: list[dict],
    by_sid: dict[str, dict],
    *,
    developer: str,
    tstar: str,
    budget: int,
    pool_sessions: int,
    pool_turns: int,
) -> dict:
    if pack_dir.exists():
        shutil.rmtree(pack_dir)
    pack_dir.mkdir(parents=True)

    index = []
    total_take = 0
    for a in alloc:
        sid = a["sid"]
        take = int(a["take"])
        if take <= 0:
            continue
        sess = by_sid[sid]
        md = render_prefix(sess["turns"], take)
        fname = f"{safe_sid(sid)}.md"
        (pack_dir / fname).write_text(md)
        index.append(
            {
                "sid": sid,
                "ts": sess["ts"],
                "repo": sess.get("repo") or "",
                "human_turns_available": int(sess["n"]),
                "human_turns_take": take,
                "path": fname,
                "max_turn_ts": sess.get("max_turn_ts"),
            }
        )
        total_take += take

    index.sort(key=lambda x: (x["ts"], x["sid"]))
    (pack_dir / "_index.json").write_text(
        json.dumps(
            {
                "developer": developer,
                "Tstar": tstar,
                "budget": budget,
                "strategy": "sqrt_two_stage",
                "pool_sessions": pool_sessions,
                "pool_human_turns": pool_turns,
                "human_turns_total": total_take,
                "sessions": index,
            },
            indent=2,
        )
        + "\n"
    )
    return {
        "developer": developer,
        "Tstar": tstar,
        "sessions": len(index),
        "turns": total_take,
        "index": index,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=B_DEFAULT)
    ap.add_argument("--pools", type=Path, default=DEFAULT_POOLS)
    ap.add_argument("--src", type=Path, default=SRC_EVAL)
    ap.add_argument("--out", type=Path, default=OUT_EVAL)
    ap.add_argument("--pack-cache", type=Path, default=PACK_CACHE)
    ap.add_argument("--limit-devs", type=int, default=0)
    a = ap.parse_args()

    registry = json.loads((a.pools / "_registry.json").read_text())
    slug_by_dev = {d["developer"]: d["slug"] for d in registry["developers"]}

    task_dirs = sorted(
        p for p in a.src.iterdir() if p.is_dir() and (p / "task.toml").exists()
    )
    for task_dir in task_dirs:
        verifier = task_dir / "tests" / "verify.py"
        if (
            not verifier.exists()
            or '"scoring": "multilabel_jaccard_v1"' not in verifier.read_text()
        ):
            raise RuntimeError(
                f"{task_dir.name} lacks the canonical multi-label verifier"
            )
    by_dev: dict[str, list[Path]] = defaultdict(list)
    for td in task_dirs:
        by_dev[task_developer(td)].append(td)

    if a.limit_devs:
        keep = sorted(by_dev)[: a.limit_devs]
        by_dev = {k: by_dev[k] for k in keep}

    print(
        f"build train twin budget={a.budget} tasks_src={len(task_dirs)} "
        f"devs={len(by_dev)} pools={a.pools}",
        flush=True,
    )

    if a.out.exists():
        shutil.rmtree(a.out)
    a.out.mkdir(parents=True)
    if a.pack_cache.exists():
        shutil.rmtree(a.pack_cache)
    a.pack_cache.mkdir(parents=True)

    leakage_violations: list[str] = []
    pool_stats = {}
    pack_metas = {}
    n_tasks = 0

    for dev, tasks in sorted(by_dev.items()):
        slug = slug_by_dev.get(dev) or re.sub(r"[^a-zA-Z0-9_.-]", "_", dev)
        meta, sessions = load_pool(a.pools / slug)
        tstar = meta["Tstar"]
        # verify every pool session against T*
        for sess in sessions:
            for v in verify_session_vs_tstar(sess, tstar):
                leakage_violations.append(f"{dev} pool: {v}")

        # sampler view: {sid,ts,n,repo}
        pool_view = [
            {
                "sid": s["sid"],
                "ts": s["ts"],
                "n": int(s["n"]),
                "repo": s.get("repo") or "",
            }
            for s in sessions
            if int(s.get("n") or 0) >= 1
        ]
        by_sid = {s["sid"]: s for s in sessions}
        alloc = alloc_sqrt_two_stage(pool_view, a.budget, tight_margin=TIGHT_MARGIN)
        turns = sum(x["take"] for x in alloc)
        target = min(a.budget, sum(s["n"] for s in pool_view))
        assert turns == target, (dev, turns, target)

        # verify allocated sessions
        for arow in alloc:
            for v in verify_session_vs_tstar(by_sid[arow["sid"]], tstar):
                leakage_violations.append(f"{dev} alloc: {v}")

        pool_stats[dev] = {
            "Tstar": tstar,
            "n_tasks": len(tasks),
            "pool_sessions": len(pool_view),
            "pool_turns": sum(s["n"] for s in pool_view),
            "alloc_sessions": len(alloc),
            "alloc_turns": turns,
        }
        print(
            f"  {dev}: pool {len(pool_view)}/{sum(s['n'] for s in pool_view)} "
            f"-> alloc {len(alloc)}/{turns}",
            flush=True,
        )

        pack_dir = a.pack_cache / slug
        pmeta = write_pack(
            pack_dir,
            alloc,
            by_sid,
            developer=dev,
            tstar=tstar,
            budget=a.budget,
            pool_sessions=len(pool_view),
            pool_turns=sum(s["n"] for s in pool_view),
        )
        pack_metas[dev] = {
            k: pmeta[k] for k in ("developer", "Tstar", "sessions", "turns")
        }

        for td in tasks:
            dest = a.out / td.name
            shutil.copytree(td, dest, ignore=shutil.ignore_patterns("__pycache__"))
            (dest / "instruction.md").write_text(INSTRUCTION)
            (dest / "environment" / "Dockerfile").write_text(DOCKERFILE)
            rewrite_task_toml(td / "task.toml", dest / "task.toml")
            train_dst = dest / "environment" / "train"
            train_dst.mkdir(parents=True, exist_ok=True)
            for f in pack_dir.iterdir():
                hardlink_or_copy(f, train_dst / f.name)
            n_tasks += 1

    cond = f"train{a.budget}"
    (a.out / "_cohort_meta.json").write_text(
        json.dumps(
            {
                "name": f"UserBench eval-{cond}",
                "tasks": n_tasks,
                "developers": len(by_dev),
                "condition": cond,
                "budget": a.budget,
                "strategy": "sqrt_two_stage",
                "pools": str(a.pools),
                "leak_rule": "T*=min(held.session.ts); session.ts<T* AND max(turn.ts)<T*",
                "baseline": "datasets/eval-620",
                "hub_package": f"userbench/UserBench-{cond}",
            },
            indent=2,
        )
        + "\n"
    )

    report = {
        "built_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "budget": a.budget,
        "n_tasks": n_tasks,
        "n_developers": len(by_dev),
        "pools": str(a.pools),
        "leakage_violations": leakage_violations,
        "leakage_ok": len(leakage_violations) == 0,
        "pool_stats": pool_stats,
        "packs": pack_metas,
    }
    META_OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"\nDONE tasks={n_tasks} leakage_violations={len(leakage_violations)} "
        f"report={META_OUT}",
        flush=True,
    )
    if leakage_violations:
        raise SystemExit("LEAKAGE CHECK FAILED")


if __name__ == "__main__":
    main()

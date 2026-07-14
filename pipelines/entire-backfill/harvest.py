#!/usr/bin/env python3
"""Backfill every repository that pushed an ``entire/*`` checkpoint ref.

The census is a TSV of ``repo, actor, ref, push_count``. For each ref, this
script clones the branch, chooses the checkpoint with the highest declared turn
count for each session, and writes full-fidelity normalized turns. No message
length cap is applied.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PARSER_DIR = Path(__file__).resolve().parents[1] / "claude-crawl"
sys.path.insert(0, str(PARSER_DIR))
sys.path.insert(0, "/data/claude-crawl")
from native_transcript import PARSER_VERSION, parse_full_jsonl  # noqa: E402

BASE = Path(os.environ.get("ENTIRE_BACKFILL_ROOT", "/data/entire-backfill"))
REPOS = BASE / "repos"
CORPUS = BASE / "corpus"
META = BASE / "meta"
WORKERS = int(os.environ.get("ENTIRE_HARVEST_WORKERS", "8"))
CLONE_TIMEOUT = int(os.environ.get("ENTIRE_CLONE_TIMEOUT", "900"))
CHECKPOINT_RE = re.compile(
    r"^([0-9a-f]{2})/([0-9a-f]{10})/(\d+)/"
    r"(metadata\.json|full\.jsonl(?:\.(\d+))?)$"
)
BAD_PREFIX = (
    "<command-",
    "<local-command-stdout",
    "Caveat:",
    "[Request interrupted",
    "<environment_context",
    "<user_instructions",
    "<turn_context",
    "<ENVIRONMENT",
    "<permissions",
)

for directory in (REPOS, CORPUS, META):
    directory.mkdir(parents=True, exist_ok=True)

lock = threading.Lock()


def truncate_words(text: str, _limit: int | None = None) -> str:
    """Compatibility shim for recovery scripts; deliberately returns full text."""
    return text


def user_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
            and item.get("type") in {"text", "input_text", "output_text"}
        )
    return ""


def parse_codex_line(record: dict, turns: list[dict]) -> None:
    """Compatibility adapter used by Seoul's deleted-branch recovery worker."""
    _, parsed = parse_full_jsonl(json.dumps(record, ensure_ascii=False))
    turns.extend(parsed)


def git(args, cwd=None, timeout=300) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", "replace")[:500])
    return result.stdout


def _read_git_objects(repo_path: Path, object_ids: list[str]) -> dict[str, bytes]:
    if not object_ids:
        return {}
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo_path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    output: dict[str, bytes] = {}
    for object_id in object_ids:
        process.stdin.write(f"{object_id}\n".encode())
        process.stdin.flush()
        header = process.stdout.readline().decode().split()
        if len(header) < 3 or header[1] == "missing":
            continue
        size = int(header[2])
        output[object_id] = process.stdout.read(size)
        process.stdout.read(1)
    process.stdin.close()
    process.wait()
    return output


def _enumerate_checkpoints(repo_path: Path, ref: str):
    tree = git(
        ["ls-tree", "-r", "-z", ref, "--format=%(objectname) %(path)"],
        cwd=repo_path,
    ).decode()
    metadata: dict[tuple[str, int], str] = {}
    transcripts: dict[tuple[str, int], list[tuple[int, str]]] = defaultdict(list)
    for entry in tree.split("\0"):
        if not entry:
            continue
        object_id, _, path = entry.partition(" ")
        match = CHECKPOINT_RE.match(path)
        if not match:
            continue
        key = (match.group(1) + match.group(2), int(match.group(3)))
        if match.group(4) == "metadata.json":
            metadata[key] = object_id
        else:
            part = int(match.group(5)) if match.group(5) else 0
            transcripts[key].append((part, object_id))
    return metadata, transcripts


def _select_sessions(repo_path: Path, metadata: dict[tuple[str, int], str]):
    blobs = _read_git_objects(repo_path, list(metadata.values()))
    selected: dict[str, tuple[int, str, tuple[str, int], dict]] = {}
    for key, object_id in metadata.items():
        try:
            document = json.loads(blobs[object_id])
        except (KeyError, json.JSONDecodeError):
            continue
        session_id = document.get("session_id")
        if not session_id:
            continue
        turn_count = (document.get("session_metrics") or {}).get("turn_count") or 0
        created_at = document.get("created_at") or ""
        candidate = (turn_count, created_at, key, document)
        current = selected.get(session_id)
        if current is None or candidate[:2] > current[:2]:
            selected[session_id] = candidate
    return selected


def parse_ref(repo_path: Path, ref: str) -> list[dict]:
    metadata, transcript_parts = _enumerate_checkpoints(repo_path, ref)
    selected = _select_sessions(repo_path, metadata)
    wanted_ids = [
        object_id
        for _, _, key, _ in selected.values()
        for _, object_id in sorted(transcript_parts.get(key) or [])
    ]
    blobs = _read_git_objects(repo_path, wanted_ids)
    sessions = []
    for session_id, (_, created_at, key, document) in selected.items():
        parts = sorted(transcript_parts.get(key) or [])
        if not parts:
            continue
        transcript = b"".join(blobs.get(object_id, b"") for _, object_id in parts)
        human_turns, turns = parse_full_jsonl(transcript)
        if human_turns == 0:
            continue
        sessions.append(
            {
                "session_id": session_id,
                "created_at": created_at,
                "agent": document.get("agent"),
                "model": document.get("model"),
                "n_user_turns": human_turns,
                "turns": turns,
                "text_fidelity": "full",
                "parser_version": PARSER_VERSION,
            }
        )
    return sessions


def process(repo: str, ref: str, actor: str, done: set[tuple[str, str]], status):
    ref_slug = ref.replace("refs/heads/", "").replace("/", "_")
    shard = CORPUS / f"{repo.replace('/', '__')}__{ref_slug}.jsonl"
    if (repo, ref) in done or shard.exists():
        return "skip"
    repo_path = REPOS / f"{repo.replace('/', '__')}__{ref_slug}"

    def log(result: str) -> None:
        with lock:
            status.write(f"{repo}\t{ref}\t{result}\n")
            status.flush()

    try:
        if not (repo_path / "objects").exists():
            shutil.rmtree(repo_path, ignore_errors=True)
            branch = ref.removeprefix("refs/heads/")
            result = subprocess.run(
                [
                    "git",
                    "clone",
                    "-q",
                    "--single-branch",
                    "--branch",
                    branch,
                    "--bare",
                    f"https://github.com/{repo}",
                    str(repo_path),
                ],
                capture_output=True,
                timeout=CLONE_TIMEOUT,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            )
            if result.returncode != 0:
                error = result.stderr.decode("utf-8", "replace")
                terminal = any(
                    marker in error.lower()
                    for marker in ("not found", "remote branch", "authentication")
                )
                log(("gone " if terminal else "err ") + error.replace("\n", " ")[:200])
                return "gone" if terminal else "err"
        sessions = parse_ref(repo_path, ref)
        lines = [
            json.dumps(
                {**session, "repo": repo, "ref": ref, "actor": actor},
                ensure_ascii=False,
            )
            for session in sessions
        ]
        temporary = shard.with_suffix(".tmp")
        temporary.write_text("\n".join(lines) + ("\n" if lines else ""))
        temporary.replace(shard)
        log(f"ok {len(lines)} sessions parser={PARSER_VERSION}")
        return "ok"
    except Exception as error:  # keep the long-running backfill resumable
        log(f"err {type(error).__name__} {str(error)[:200]}")
        return "err"


def _jobs():
    actors: dict[tuple[str, str], tuple[str, int]] = {}
    counts: dict[tuple[str, str], int] = defaultdict(int)
    with (META / "census.tsv").open() as handle:
        for line in handle:
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 4:
                continue
            repo, actor, ref, raw_count = fields[:4]
            count = int(raw_count)
            key = (repo, ref)
            counts[key] += count
            if key not in actors or count > actors[key][1]:
                actors[key] = (actor, count)
    jobs = [
        (repo, ref, actor)
        for (repo, ref), (actor, _) in actors.items()
        if "[bot]" not in actor
    ]
    return sorted(jobs, key=lambda job: -counts[(job[0], job[1])])


def main():
    status_path = META / "clone_status.tsv"
    done = set()
    if status_path.exists():
        for line in status_path.open():
            fields = line.rstrip("\n").split("\t")
            if len(fields) >= 3 and fields[2].startswith(
                ("ok", "gone", "empty", "noref")
            ):
                done.add((fields[0], fields[1]))
    jobs = _jobs()
    print(f"{len(jobs)} repository/ref jobs; parser={PARSER_VERSION}")
    tally: defaultdict[str, int] = defaultdict(int)
    with status_path.open("a") as status:
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            for result in executor.map(
                lambda job: process(*job, done=done, status=status), jobs
            ):
                tally[result] += 1
    print("DONE", dict(tally))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reparse hydrated crawl clones with the shared full-context parser."""
from __future__ import annotations

import argparse
import glob
import json
import re
import sqlite3
import tempfile
from pathlib import Path

from cohort_policy import canonical_session_id
from native_transcript import PARSER_VERSION, parse_full_jsonl


UUID_RE = re.compile(
    r"(?<![0-9a-f])"
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
    r"(?![0-9a-f])",
    re.I,
)
SESSION_ROOT_MARKERS = (
    "/.claude/",
    "/.codex/",
    "/projects/",
    "/sessions/",
    "/conversations/",
    "/conversation-archive/",
)
SKIP_MARKERS = (
    "/tests/",
    "/test/",
    "/fixtures/",
    "/experiments/",
    "/evals/",
    "/mock-data/",
    "/.git/",
)


def _lookup_keys(session_id: str | None) -> set[str]:
    """Map harvest wrappers like ``owner/repo|uuid`` onto bare UUID keys."""
    value = (session_id or "").strip()
    if not value:
        return set()
    keys = {canonical_session_id(value), value}
    for match in UUID_RE.findall(value):
        keys.add(match.lower())
        keys.add(canonical_session_id(match))
    return {key for key in keys if key}


def _existing_sessions(pattern: str) -> dict[str, dict]:
    sessions = {}
    for filename in glob.glob(pattern):
        with open(filename, errors="replace") as source:
            for line in source:
                try:
                    document = json.loads(line)
                except json.JSONDecodeError:
                    continue
                session_id = document.get("session_id")
                keys = _lookup_keys(session_id)
                if not keys:
                    continue
                score = (
                    sum(
                        turn.get("role") == "user"
                        for turn in document.get("turns") or []
                    ),
                    len(document.get("turns") or []),
                )
                for key in keys:
                    current = sessions.get(key)
                    if current is None or score > current["_score"]:
                        sessions[key] = {**document, "_score": score}
    return sessions


def _normalized_path(path: Path) -> str:
    return "/" + str(path).replace("\\", "/").lower().strip("/") + "/"


def _should_scan_content(path: Path) -> bool:
    normalized = _normalized_path(path)
    if any(marker in normalized for marker in SKIP_MARKERS):
        return False
    return any(marker in normalized for marker in SESSION_ROOT_MARKERS)


def _candidate_ids(filename: Path, data: bytes | None = None) -> set[str]:
    identifiers = set(UUID_RE.findall(str(filename)))
    if data is not None:
        identifiers.update(
            UUID_RE.findall(data[: 1024 * 1024].decode("utf-8", "replace"))
        )
    return {canonical_session_id(identifier) for identifier in identifiers}


def _safe_text(value: str) -> str:
    return value.encode("utf-8", "surrogatepass").decode("utf-8", "replace")


def _safe_turns(turns: list[dict]) -> list[dict]:
    cleaned = []
    for turn in turns:
        item = dict(turn)
        text = item.get("text")
        if isinstance(text, str):
            item["text"] = _safe_text(text)
        cleaned.append(item)
    return cleaned


def _score(turns: list[dict]) -> tuple[int, int, int]:
    return (
        sum(turn["role"] == "user" for turn in turns),
        len(turns),
        sum(len(turn["text"]) for turn in turns),
    )


def build(clones: Path, existing_pattern: str, output: Path) -> tuple[int, int]:
    existing = _existing_sessions(existing_pattern)
    existing_keys = set(existing)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="crawl-full-") as temporary:
        connection = sqlite3.connect(Path(temporary) / "sessions.sqlite")
        connection.execute(
            "CREATE TABLE sessions ("
            "session_id TEXT PRIMARY KEY, human_turns INTEGER, turn_count INTEGER, "
            "content_chars INTEGER, payload TEXT)"
        )
        for filename in clones.glob("**/*.jsonl"):
            if ".git" in filename.parts:
                continue
            path_ids = _candidate_ids(filename)
            if path_ids:
                matches = path_ids & existing_keys
                if not matches:
                    continue
                data = filename.read_bytes()
            elif _should_scan_content(filename):
                data = filename.read_bytes()
                matches = _candidate_ids(filename, data) & existing_keys
                if not matches:
                    continue
            else:
                continue
            human_turns, turns = parse_full_jsonl(data)
            if human_turns == 0:
                continue
            turns = _safe_turns(turns)
            score = _score(turns)
            # Prefer the original harvest identifier; UUID aliases only locate the
            # matching compact-corpus metadata.
            prior = max(
                (existing[key] for key in matches),
                key=lambda document: document["_score"],
            )
            session_id = prior.get("session_id") or next(iter(matches))
            timestamps = [
                str(turn["ts"]) for turn in turns if turn.get("ts") is not None
            ]
            session = {
                "user": prior.get("user"),
                "repo": prior.get("repo") or "?",
                "session_id": session_id,
                "start_time": (
                    min(timestamps) if timestamps else prior.get("start_time")
                ),
                "harness": prior.get("harness"),
                "n_user_turns": human_turns,
                "turns": turns,
                "text_fidelity": "full",
                "parser_version": PARSER_VERSION,
            }
            connection.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(session_id) DO UPDATE SET "
                "human_turns=excluded.human_turns, "
                "turn_count=excluded.turn_count, "
                "content_chars=excluded.content_chars, "
                "payload=excluded.payload "
                "WHERE (excluded.human_turns, excluded.turn_count, "
                "excluded.content_chars) > "
                "(sessions.human_turns, sessions.turn_count, "
                "sessions.content_chars)",
                (
                    session_id,
                    *score,
                    json.dumps(session, ensure_ascii=False),
                ),
            )
        connection.commit()
        sessions = 0
        human_turns = 0
        with output.open("w") as destination:
            for count, payload in connection.execute(
                "SELECT human_turns, payload FROM sessions ORDER BY session_id"
            ):
                destination.write(payload + "\n")
                sessions += 1
                human_turns += count
        connection.close()
    return sessions, human_turns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--clones", type=Path, default=Path("/data/claude-crawl/clones")
    )
    parser.add_argument(
        "--existing-corpus-glob",
        default="/data/claude-crawl/corpus/*.jsonl",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/data/claude-crawl/corpus.full.jsonl"),
    )
    args = parser.parse_args()
    sessions, human_turns = build(
        args.clones, args.existing_corpus_glob, args.output
    )
    print(
        f"wrote {sessions} full-fidelity crawl sessions / "
        f"{human_turns} human turns to {args.output}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Rebuild DataClaw's normalized corpus without message-length truncation."""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import tempfile
from collections.abc import Iterator
from pathlib import Path

from native_transcript import PARSER_VERSION


def normalized_session(
    document: dict, donor: str, *, include_context: bool = True
) -> dict | None:
    session_id = document.get("session_id")
    messages = document.get("messages")
    if not session_id or not isinstance(messages, list):
        return None
    turns = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        role = message.get("role")
        timestamp = message.get("timestamp")
        content = message.get("content")
        if (
            role in {"system", "user", "assistant"}
            and isinstance(content, str)
            and content.strip()
        ):
            turns.append({"role": role, "ts": timestamp, "text": content.strip()})
        if include_context:
            thinking = message.get("thinking")
            if isinstance(thinking, str) and thinking.strip():
                turns.append(
                    {
                        "role": "metadata",
                        "ts": timestamp,
                        "text": thinking.strip(),
                    }
                )
            for tool_use in message.get("tool_uses") or []:
                if isinstance(tool_use, dict):
                    turns.append(
                        {
                            "role": "tool",
                            "ts": timestamp,
                            "text": json.dumps(
                                tool_use, ensure_ascii=False, sort_keys=True
                            ),
                        }
                    )
    if not any(turn["role"] == "user" for turn in turns):
        return None
    return {
        "donor": document.get("donor") or donor,
        "repo": document.get("repo") or document.get("project") or "?",
        "source": document.get("source") or document.get("model") or "?",
        "session_id": session_id,
        "start_time": document.get("start_time"),
        "end_time": document.get("end_time"),
        "turns": turns,
        "text_fidelity": "full",
        "parser_version": f"dataclaw-schema+{PARSER_VERSION}",
    }


def _candidate_files(raw_root: Path) -> list[Path]:
    return sorted(
        {
            *raw_root.glob("**/conversations.jsonl"),
            *raw_root.glob("**/*.conversations.jsonl"),
        }
    )


def _unique_files(files: list[Path]) -> Iterator[Path]:
    """Skip byte-identical DataClaw forks before parsing their sessions."""
    by_size: dict[int, list[Path]] = {}
    for filename in files:
        by_size.setdefault(filename.stat().st_size, []).append(filename)
    for group in by_size.values():
        if len(group) == 1:
            yield group[0]
            continue
        seen_hashes = set()
        for filename in group:
            digest = hashlib.sha256()
            with filename.open("rb") as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b""):
                    digest.update(chunk)
            hexdigest = digest.hexdigest()
            if hexdigest not in seen_hashes:
                seen_hashes.add(hexdigest)
                yield filename


def _existing_donors(existing_corpus: Path | None) -> dict[str, str]:
    donors = {}
    if existing_corpus is None or not existing_corpus.exists():
        return donors
    with existing_corpus.open(errors="replace") as source:
        for line in source:
            try:
                document = json.loads(line)
            except json.JSONDecodeError:
                continue
            session_id = document.get("session_id")
            donor = document.get("donor")
            if session_id and donor:
                donors.setdefault(session_id, donor)
    return donors


def _fallback_donor(filename: Path) -> str:
    name = filename.name.removesuffix(".conversations.jsonl")
    return name.split("__", 1)[0]


def _score(session: dict) -> tuple[int, int, int]:
    turns = session["turns"]
    return (
        sum(turn["role"] == "user" for turn in turns),
        len(turns),
        sum(len(turn["text"]) for turn in turns),
    )


def build(
    raw_root: Path,
    output: Path,
    existing_corpus: Path | None = None,
) -> tuple[int, int]:
    files = list(_unique_files(_candidate_files(raw_root)))
    donor_by_session = _existing_donors(existing_corpus)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dataclaw-full-") as temporary:
        database = Path(temporary) / "sessions.sqlite"
        connection = sqlite3.connect(database)
        connection.execute(
            "CREATE TABLE sessions ("
            "session_id TEXT PRIMARY KEY, human_turns INTEGER, turn_count INTEGER, "
            "content_chars INTEGER, payload TEXT)"
        )
        for filename in files:
            fallback_donor = _fallback_donor(filename)
            with filename.open(errors="replace") as source:
                for line in source:
                    try:
                        document = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    session_id = document.get("session_id")
                    donor = donor_by_session.get(session_id, fallback_donor)
                    session = normalized_session(document, donor)
                    if session is None:
                        continue
                    score = _score(session)
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
                            session["session_id"],
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
        "--raw-root", type=Path, default=Path("/data/dataclaw/raw")
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/data/dataclaw/meta/corpus.full.jsonl"),
    )
    parser.add_argument(
        "--existing-corpus",
        type=Path,
        help="Optional legacy corpus used only to preserve donor attribution",
    )
    args = parser.parse_args()
    sessions, human_turns = build(
        args.raw_root, args.output, args.existing_corpus
    )
    print(
        f"wrote {sessions} full-fidelity sessions / {human_turns} human turns "
        f"to {args.output}"
    )


if __name__ == "__main__":
    main()

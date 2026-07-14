#!/usr/bin/env python3
"""Rebuild DataClaw's normalized corpus without message-length truncation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from native_transcript import PARSER_VERSION


def normalized_session(
    document: dict, donor: str, *, include_context: bool = False
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
        if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
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


def build(raw_root: Path, output: Path) -> tuple[int, int]:
    files = sorted(raw_root.glob("**/conversations.jsonl"))
    output.parent.mkdir(parents=True, exist_ok=True)
    sessions = 0
    human_turns = 0
    with output.open("w") as destination:
        for filename in files:
            donor = filename.parent.name
            with filename.open(errors="replace") as source:
                for line in source:
                    try:
                        document = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    session = normalized_session(document, donor)
                    if session is None:
                        continue
                    destination.write(json.dumps(session, ensure_ascii=False) + "\n")
                    sessions += 1
                    human_turns += sum(
                        turn["role"] == "user" for turn in session["turns"]
                    )
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
    args = parser.parse_args()
    sessions, human_turns = build(args.raw_root, args.output)
    print(
        f"wrote {sessions} full-fidelity sessions / {human_turns} human turns "
        f"to {args.output}"
    )


if __name__ == "__main__":
    main()

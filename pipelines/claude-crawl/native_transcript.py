#!/usr/bin/env python3
"""Parse native coding-agent transcripts without clipping message content.

The parser intentionally keeps every text byte from user and assistant messages.
Filtering injected/system content and scrubbing secrets happen later in
``cohort_policy.py``.  This module only normalizes source-specific event shapes
into ordered ``{role, ts, text}`` records.
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any

PARSER_VERSION = "swesimbench-native-transcript-2026-07-14.1"

CODEX_ENVELOPES = {"response_item", "session_meta", "event_msg", "turn_context"}
TEXT_BLOCK_TYPES = {"text", "input_text", "output_text"}


def _json_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _block_text(block: Any) -> str:
    if isinstance(block, str):
        return block
    if not isinstance(block, dict):
        return ""
    if isinstance(block.get("text"), str):
        return block["text"]
    if isinstance(block.get("content"), str):
        return block["content"]
    return ""


def _message_blocks(
    content: Any, role: str, timestamp: Any, *, meta: bool = False
) -> list[dict]:
    """Expand message content while retaining text/tool/thinking payloads."""
    if isinstance(content, str):
        text = content.strip()
        return [{"role": "system" if meta else role, "ts": timestamp, "text": text}] if text else []
    if not isinstance(content, list):
        return []

    turns: list[dict] = []
    for block in content:
        if isinstance(block, str):
            text = block.strip()
            block_type = "text"
        elif isinstance(block, dict):
            block_type = str(block.get("type") or "")
            text = _block_text(block).strip()
        else:
            continue

        if block_type in TEXT_BLOCK_TYPES or not block_type:
            if text:
                turns.append(
                    {
                        "role": "system" if meta else role,
                        "ts": timestamp,
                        "text": text,
                    }
                )
        elif block_type == "tool_use":
            payload = {
                "name": block.get("name"),
                "input": block.get("input"),
                "id": block.get("id"),
            }
            turns.append({"role": "tool", "ts": timestamp, "text": _json_text(payload)})
        elif block_type == "tool_result":
            payload = block.get("content")
            if payload is None:
                payload = block.get("text")
            turns.append({"role": "tool", "ts": timestamp, "text": _json_text(payload)})
        elif block_type in {"thinking", "redacted_thinking"}:
            payload = block.get("thinking") or block.get("data") or text
            if payload:
                turns.append(
                    {"role": "metadata", "ts": timestamp, "text": _json_text(payload)}
                )
        elif text:
            turns.append({"role": "metadata", "ts": timestamp, "text": text})
    return turns


def _parse_claude(records: Iterable[dict]) -> list[dict]:
    """Parse Claude-style JSONL, replacing repeated streamed event snapshots."""
    order: list[str] = []
    events: dict[str, list[dict]] = {}
    anonymous = 0

    def put(key: str | None, value: list[dict]) -> None:
        nonlocal anonymous
        if not value:
            return
        if not key:
            key = f"_anonymous_{anonymous}"
            anonymous += 1
        if key not in events:
            order.append(key)
        events[key] = value

    for record in records:
        event_type = record.get("type")
        timestamp = record.get("timestamp")
        message = record.get("message")
        if event_type in {"user", "assistant"} and isinstance(message, dict):
            role = str(event_type)
            is_sidechain = bool(record.get("isSidechain"))
            is_meta = bool(record.get("isMeta")) or is_sidechain
            key = record.get("uuid")
            if event_type == "assistant":
                key = message.get("id") or key
            put(
                f"{event_type}:{key}" if key else None,
                _message_blocks(
                    message.get("content"), role, timestamp, meta=is_meta
                ),
            )
            continue

        if event_type in {"system", "summary"}:
            content = (
                record.get("content")
                or (message.get("content") if isinstance(message, dict) else None)
                or record.get("summary")
            )
            put(
                f"{event_type}:{record.get('uuid')}" if record.get("uuid") else None,
                _message_blocks(content, "system", timestamp, meta=True),
            )
            continue

        if event_type in {"queue-operation", "progress"}:
            payload = record.get("content") or record.get("message") or record
            put(
                f"{event_type}:{record.get('uuid')}" if record.get("uuid") else None,
                [{"role": "metadata", "ts": timestamp, "text": _json_text(payload)}],
            )
            continue

        # Some exports use bare role/message records without a top-level type.
        role = record.get("role")
        if role in {"user", "assistant"}:
            content = message.get("content") if isinstance(message, dict) else message
            put(
                f"bare:{record.get('uuid')}" if record.get("uuid") else None,
                _message_blocks(content, str(role), timestamp),
            )

    return [turn for key in order for turn in events[key]]


def _codex_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    return "\n".join(
        text
        for item in content
        if (text := _block_text(item).strip())
        and (
            isinstance(item, str)
            or not isinstance(item, dict)
            or item.get("type") in TEXT_BLOCK_TYPES
        )
    )


def _parse_codex(records: Iterable[dict]) -> list[dict]:
    records = list(records)
    event_users = [
        (
            record.get("timestamp"),
            str((record.get("payload") or {}).get("message") or "").strip(),
        )
        for record in records
        if record.get("type") == "event_msg"
        and isinstance(record.get("payload"), dict)
        and record["payload"].get("type") == "user_message"
        and str(record["payload"].get("message") or "").strip()
    ]
    use_event_users = bool(event_users)
    turns: list[tuple[int, dict]] = []

    for index, record in enumerate(records):
        timestamp = record.get("timestamp")
        envelope = record.get("type")
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = payload.get("type")
        if envelope == "event_msg" and payload_type == "user_message":
            if use_event_users:
                text = str(payload.get("message") or "").strip()
                if text:
                    turns.append(
                        (index, {"role": "user", "ts": timestamp, "text": text})
                    )
            continue
        if envelope != "response_item":
            continue
        if payload_type == "message":
            role = payload.get("role")
            if role not in {"user", "assistant"} or (role == "user" and use_event_users):
                continue
            text = _codex_text(payload.get("content"))
            if text:
                turns.append((index, {"role": role, "ts": timestamp, "text": text}))
        elif payload_type in {
            "function_call",
            "local_shell_call",
            "custom_tool_call",
            "function_call_output",
        }:
            turns.append(
                (index, {"role": "tool", "ts": timestamp, "text": _json_text(payload)})
            )

    return [turn for _, turn in sorted(turns, key=lambda item: item[0])]


def _parse_document(document: dict) -> list[dict]:
    """Parse OpenCode/Gemini whole-document exports."""
    turns: list[dict] = []
    for item in document.get("messages") or []:
        if not isinstance(item, dict):
            continue
        info = item.get("info") if isinstance(item.get("info"), dict) else {}
        role = info.get("role") or item.get("role") or item.get("type")
        if role in {"gemini", "model"}:
            role = "assistant"
        if role not in {"user", "assistant"}:
            continue
        timestamp = item.get("timestamp") or (info.get("time") or {}).get("created")
        content = item.get("content")
        if content is None and isinstance(item.get("parts"), list):
            content = item["parts"]
        turns.extend(_message_blocks(content, str(role), timestamp))
    return turns


def parse_full_jsonl(data: bytes | str) -> tuple[int, list[dict]]:
    """Return ``(human-role turn count, full-fidelity normalized turns)``."""
    text = data.decode("utf-8", "replace") if isinstance(data, bytes) else data
    try:
        document = json.loads(text)
    except json.JSONDecodeError:
        document = None
    if isinstance(document, dict) and isinstance(document.get("messages"), list):
        turns = _parse_document(document)
        return sum(turn["role"] == "user" for turn in turns), turns

    records: list[dict] = []
    for line in text.splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    is_codex = any(
        record.get("type") in CODEX_ENVELOPES
        and isinstance(record.get("payload"), dict)
        for record in records
    )
    turns = _parse_codex(records) if is_codex else _parse_claude(records)
    return sum(turn["role"] == "user" for turn in turns), turns

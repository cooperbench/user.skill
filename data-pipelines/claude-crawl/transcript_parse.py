#!/usr/bin/env python3
"""Full-fidelity transcript parsing for Claude Code, Codex, and DataClaw.

Preserves newlines (no split/join flatten). Emits tool_use / tool_result as
role=tool turns interleaved with user/assistant text turns.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CLAUDE_USER_NOISE = (
    "<command-",
    "<local-command",
    "Caveat:",
    "[Request interrupted",
    "<task-notification",
    "<teammate-message",
    "<user-prompt-submit-hook",
    "<session-start-hook",
    "<user-memory-input",
    "This session is being continued",
    "<system-reminder",
    "[SYSTEM",
    "<ide_opened_file",
    "<ide_selection",
    "<ide_diagnostics",
    "<ide-",
    "<budget:",
    "<post-tool",
    "<pre-tool",
)

CODEX_USER_NOISE = (
    "<environment_context",
    "<user_instructions",
    "<turn_context",
    "<permissions",
    "<ENVIRONMENT",
    "<system-reminder",
    "## My request for Codex",
    "<user_info",
)


def _json_block(obj: Any) -> str:
    if isinstance(obj, str):
        return obj
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except TypeError:
        return str(obj)


def format_tool_use(*, name: str, tool_input: Any, tool_use_id: str | None = None) -> str:
    header = f"tool_use {name or 'unknown'}"
    if tool_use_id:
        header += f"\nid: {tool_use_id}"
    return f"{header}\n```json\n{_json_block(tool_input)}\n```"


def format_tool_result(
    *,
    content: Any,
    tool_use_id: str | None = None,
    name: str | None = None,
    is_error: bool = False,
) -> str:
    bits = ["tool_result"]
    if name:
        bits.append(name)
    if is_error:
        bits.append("ERROR")
    header = " ".join(bits)
    if tool_use_id:
        header += f"\nid: {tool_use_id}"
    body = content
    if isinstance(content, list):
        # Claude tool_result content can be list of text blocks
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text") or "")
            elif isinstance(block, str):
                parts.append(block)
            else:
                parts.append(_json_block(block))
        body = "\n".join(p for p in parts if p)
    elif not isinstance(content, str):
        body = _json_block(content)
    return f"{header}\n```\n{body}\n```"


def _append(turns: list[dict], role: str, text: str, ts: str | None) -> None:
    text = (text or "").rstrip()
    if not text:
        return
    turns.append({"role": role, "ts": ts, "text": text})


def parse_claude_code_jsonl(data: bytes | str) -> list[dict]:
    """Parse native Claude Code session JSONL into ordered turns (incl. tools)."""
    if isinstance(data, bytes):
        text = data.decode("utf-8", errors="replace")
    else:
        text = data
    turns: list[dict] = []
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        t = d.get("type")
        ts = d.get("timestamp")
        msg = d.get("message") if isinstance(d.get("message"), dict) else {}
        content = msg.get("content")

        if t == "user":
            if d.get("isMeta") or d.get("isSidechain"):
                continue
            # tool_result blocks (may mix with text — emit tools then any text)
            if isinstance(content, list):
                texts = []
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    btype = block.get("type")
                    if btype == "tool_result":
                        _append(
                            turns,
                            "tool",
                            format_tool_result(
                                content=block.get("content"),
                                tool_use_id=block.get("tool_use_id"),
                                is_error=bool(block.get("is_error")),
                            ),
                            ts,
                        )
                    elif btype == "text":
                        texts.append(block.get("text") or "")
                txt = "\n".join(x for x in texts if x).strip()
            elif isinstance(content, str):
                txt = content.strip()
            else:
                txt = ""
            if txt and not txt.startswith(CLAUDE_USER_NOISE):
                _append(turns, "user", txt, ts)

        elif t == "assistant":
            if d.get("isSidechain"):
                continue
            if isinstance(content, list):
                texts = []
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    btype = block.get("type")
                    if btype == "text":
                        texts.append(block.get("text") or "")
                    elif btype == "tool_use":
                        # flush preceding assistant text before the tool call
                        joined = "\n".join(x for x in texts if x).strip()
                        if joined:
                            _append(turns, "assistant", joined, ts)
                            texts = []
                        _append(
                            turns,
                            "tool",
                            format_tool_use(
                                name=block.get("name") or "unknown",
                                tool_input=block.get("input"),
                                tool_use_id=block.get("id"),
                            ),
                            ts,
                        )
                joined = "\n".join(x for x in texts if x).strip()
                if joined:
                    _append(turns, "assistant", joined, ts)
            elif isinstance(content, str) and content.strip():
                _append(turns, "assistant", content.strip(), ts)

    return turns


def parse_codex_jsonl(data: bytes | str) -> list[dict]:
    """Parse native Codex rollout JSONL into ordered turns (incl. function calls)."""
    if isinstance(data, bytes):
        text = data.decode("utf-8", errors="replace")
    else:
        text = data
    turns: list[dict] = []
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        ts = d.get("timestamp")
        if d.get("type") != "response_item":
            continue
        p = d.get("payload")
        if not isinstance(p, dict):
            continue
        ptype = p.get("type")

        if ptype == "message":
            role = p.get("role")
            if role not in ("user", "assistant"):
                continue
            content = p.get("content")
            parts = []
            if isinstance(content, str):
                parts.append(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") in (
                        "input_text",
                        "output_text",
                        "text",
                    ):
                        parts.append(block.get("text") or "")
            txt = "\n".join(x for x in parts if x).strip()
            if not txt:
                continue
            if role == "user" and txt.startswith(CODEX_USER_NOISE):
                continue
            _append(turns, role, txt, ts)

        elif ptype == "function_call":
            args = p.get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    pass
            _append(
                turns,
                "tool",
                format_tool_use(
                    name=p.get("name") or "function_call",
                    tool_input=args,
                    tool_use_id=p.get("call_id"),
                ),
                ts,
            )

        elif ptype == "function_call_output":
            _append(
                turns,
                "tool",
                format_tool_result(
                    content=p.get("output"),
                    tool_use_id=p.get("call_id"),
                ),
                ts,
            )

    return turns


def parse_dataclaw_messages(messages: list[dict]) -> list[dict]:
    """Normalize DataClaw HF messages (content + optional tool_uses) to turns."""
    turns: list[dict] = []
    for m in messages or []:
        if not isinstance(m, dict):
            continue
        role = m.get("role") or "metadata"
        ts = m.get("timestamp") or m.get("ts")
        content = m.get("content")
        if isinstance(content, list):
            # rare structured content
            texts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    texts.append(block.get("text") or "")
                elif isinstance(block, dict) and block.get("type") == "tool_use":
                    joined = "\n".join(x for x in texts if x).strip()
                    if joined and role in ("user", "assistant"):
                        _append(turns, role, joined, ts)
                        texts = []
                    _append(
                        turns,
                        "tool",
                        format_tool_use(
                            name=block.get("name") or "unknown",
                            tool_input=block.get("input"),
                            tool_use_id=block.get("id"),
                        ),
                        ts,
                    )
                elif isinstance(block, dict) and block.get("type") == "tool_result":
                    _append(
                        turns,
                        "tool",
                        format_tool_result(
                            content=block.get("content"),
                            tool_use_id=block.get("tool_use_id"),
                            is_error=bool(block.get("is_error")),
                        ),
                        ts,
                    )
            content = "\n".join(x for x in texts if x)
        if isinstance(content, str) and content.strip() and role in ("user", "assistant", "system"):
            _append(turns, "user" if role == "user" else ("assistant" if role == "assistant" else "system"), content.strip(), ts)

        # DataClaw-specific: tool_uses [{tool, input, output}] on assistant messages
        for tu in m.get("tool_uses") or []:
            if not isinstance(tu, dict):
                continue
            name = tu.get("tool") or tu.get("name") or "tool"
            tool_input = tu.get("input")
            output = tu.get("output")
            _append(
                turns,
                "tool",
                format_tool_use(name=name, tool_input=tool_input, tool_use_id=tu.get("id")),
                ts,
            )
            if output is not None:
                out_text = output.get("text") if isinstance(output, dict) else output
                _append(
                    turns,
                    "tool",
                    format_tool_result(content=out_text, name=name, tool_use_id=tu.get("id")),
                    ts,
                )
    return turns


def parse_agent_blob(data: bytes | str, harness_hint: str | None = None) -> tuple[list[dict], str]:
    """Auto-detect Claude Code vs Codex JSONL. Returns (turns, harness)."""
    sample = data[:4000] if isinstance(data, (bytes, str)) else b""
    if isinstance(sample, str):
        sample_b = sample.encode()
    else:
        sample_b = sample
    if harness_hint == "codex" or b'"payload"' in sample_b and b"response_item" in sample_b:
        turns = parse_codex_jsonl(data)
        if turns:
            return turns, "codex"
    turns = parse_claude_code_jsonl(data)
    if turns:
        return turns, "claude-code"
    turns = parse_codex_jsonl(data)
    return turns, "codex" if turns else "unknown"


def parse_session_file(path: str | Path) -> tuple[str | None, str | None, list[dict], str] | None:
    """Parse a on-disk Claude Code or Codex session file."""
    path = Path(path)
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) > 120 * 1024 * 1024:
        return None
    hint = "codex" if "/.codex/" in str(path) or path.name.startswith("rollout-") else None
    turns, harness = parse_agent_blob(data, hint)
    if not turns or not any(t["role"] == "user" for t in turns):
        return None
    sid = None
    first_ts = next((t.get("ts") for t in turns if t.get("ts")), "0000")
    text = data.decode("utf-8", errors="replace")
    if harness == "claude-code":
        for raw in text.splitlines()[:40]:
            try:
                d = json.loads(raw)
            except Exception:
                continue
            if isinstance(d, dict) and d.get("sessionId"):
                sid = d["sessionId"]
                break
    else:
        # Codex: prefer session_meta.id; else UUID suffix of rollout-* filename
        for raw in text.splitlines()[:80]:
            try:
                d = json.loads(raw)
            except Exception:
                continue
            if not isinstance(d, dict):
                continue
            if d.get("type") == "session_meta" and isinstance(d.get("payload"), dict):
                sid = d["payload"].get("id") or sid
                if sid:
                    break
        if not sid:
            import re as _re
            m = _re.search(
                r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
                path.stem,
                _re.I,
            )
            if m:
                sid = m.group(1).lower()
    if not sid:
        # Parent dir often is the UUID for Codex dumps under .../<uuid>/codex/sessions/...
        import re as _re
        for part in reversed(path.parts):
            if _re.fullmatch(
                r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                part,
                _re.I,
            ):
                sid = part.lower()
                break
    sid = sid or path.stem
    return sid, first_ts, turns, harness

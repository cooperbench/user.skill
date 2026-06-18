#!/usr/bin/env python3
"""Build a user profile from YOUR OWN local coding trajectories.

It reads the session logs that coding agents leave on disk, merges all of them
into a single digest, and runs the local distillation skill
(.claude/skills/distill-local-user) to write users/<slug>/.

Supported agents (detected by transcript content, so location overrides work):
  Claude Code, Codex, OpenCode, Gemini CLI, Factory Droid, Copilot CLI, Pi.
Cursor keeps its history in a local SQLite DB rather than transcript files, so
it is not auto-detected (point its path at exported JSONL transcripts to include
it). Everything is self-contained — no other repo needs to be present.

Interactive wizard (default):
  python3 scripts/build_local_profile.py
    1. detect each agent's sessions at its default path (show counts)
    2. let you correct any path
    3. ask permission, then generate the profile
       - uses the `claude` CLI if installed (your subscription)
       - otherwise uses an ANTHROPIC_API_KEY you provide

Non-interactive:
  python3 scripts/build_local_profile.py --yes --slug me

The digest is derived purely from raw transcripts: prompt text, lengths,
projects, dates. With --agent-context it also keeps a compact record of what the
agent replied and ran (assistant turns + truncated tool-call summaries), so the
profile can reason about what the user's messages were reacting to. Output
folders are never overwritten unless --force is given.
"""

import argparse
import getpass
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
# NOTE: `sqlite3` is imported lazily inside the OpenCode reader so the script
# runs on minimal Python builds (or for users with no OpenCode sessions) that
# lack the sqlite3 module. `anthropic` is likewise imported only on the API path.

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "distill-local-user" / "SKILL.md"
REQUIRED = ["USER.md", "PERSONA.md", "STYLE.md", "PREFERENCES.md",
            "PROJECTS.md", "stats.json"]

# Default on-disk locations. Claude/Codex/OpenCode are verified; the rest are
# best-effort starting points — paths vary by install and are overridable in the
# wizard or via --<agent>-path. Detection is by file content, not by location.
HOME = Path.home()
DEFAULT_PATHS = {
    "Claude Code": HOME / ".claude" / "projects",
    "Codex": HOME / ".codex" / "sessions",
    "OpenCode": HOME / ".local" / "share" / "opencode",
    "Gemini CLI": HOME / ".gemini" / "tmp",
    "Factory Droid": HOME / ".factory" / "sessions",
    "Copilot CLI": HOME / ".copilot" / "history",
    "Pi": HOME / ".pi" / "sessions",
}
# Short CLI flag stem per agent (e.g. --gemini-path overrides "Gemini CLI").
FLAG_STEM = {
    "Claude Code": "claude", "Codex": "codex", "OpenCode": "opencode",
    "Gemini CLI": "gemini", "Factory Droid": "droid", "Copilot CLI": "copilot",
    "Pi": "pi",
}

# Per-user prompt sampling, mirroring prepare_data.py.
MAX_FIRST_PROMPTS = 60
MAX_MID_PROMPTS = 150
FIRST_PROMPT_WORDS = 250
MID_PROMPT_WORDS = 150

# A "role: user" turn the CLI harness wrote but the human did NOT type: slash
# echoes, hook feedback, interrupt banners, teammate-agent pings, bash framing,
# continuation summaries, image stubs. Routing these out keeps the digest to
# genuinely typed prose. Tag-opens that can carry attributes omit the closing ">".
SYSTEM_INJECTED_PREFIXES = (
    "<command-name>", "<command-message>", "<command-args>",
    "<local-command-caveat>", "<local-command-stdout>", "<local-command-stderr>",
    "<system-reminder>", "<system_instruction",
    "<task-notification>", "<teammate-message",
    "<bash-input>", "<bash-stdout>", "<bash-stderr>",
    "<user-prompt-submit-hook>", "<ide_opened_file>",
    "Base directory for this skill:", "Operation stopped by hook:",
)
CONTINUATION_PREFIX = "This session is being continued"
SYSTEM_INJECTED_REGEXES = (
    re.compile(r"\[Request interrupted by user", re.I),
    re.compile(r"Tool loaded\.\s*$"),
    re.compile(re.escape(CONTINUATION_PREFIX), re.I),
    re.compile(r"Stop hook feedback:", re.I),
    re.compile(r"<<autonomous-loop", re.I),
    # OpenCode synthetic "user" turn announcing a user-run tool (the part is also
    # flagged synthetic:true — see _opencode_from_db, which drops it at the source).
    re.compile(r"^The following tool was executed by the user", re.I),
    # Cross-agent /init command expansion (the AGENTS.md boilerplate), not typed.
    re.compile(r"^Please analyze this codebase and create an AGENTS\.md file", re.I),
)
_IMAGE_STUB_RE = re.compile(
    r"^\s*(?:\[Image:\s*(?:original\s+\d+x\d+|source:)[^\]]*\]\s*)+$", re.I)
# Codex wraps its session preamble in these; not typed prose. We strip them from
# the response_item fallback so they never reach the digest.
CODEX_WRAPPER_PREFIXES = ("<environment_context>", "<user_instructions>")
# Codex rollout envelope types, used to fingerprint a Codex transcript.
CODEX_ENVELOPE_TYPES = {"session_meta", "response_item", "event_msg",
                        "turn_context", "compacted"}


# --------------------------------------------------------------------------- #
# Parsers: each returns a list of session dicts
#   {source, session_id, project, started_at, prompts: [text, ...]}
# Parsing is defensive: a malformed file/record is skipped, never fatal.
# --------------------------------------------------------------------------- #

def _iter_jsonl(path):
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return


def _project_from_cwd(cwd):
    return os.path.basename(cwd.rstrip("/")) if cwd else "unknown"


def _looks_system_injected(text):
    """Does this user turn look harness-written rather than human-typed?"""
    s = (text or "").lstrip()
    if not s:
        return True
    if s.startswith(SYSTEM_INJECTED_PREFIXES) or s.startswith(CODEX_WRAPPER_PREFIXES):
        return True
    if any(rx.match(s) for rx in SYSTEM_INJECTED_REGEXES):
        return True
    return bool(_IMAGE_STUB_RE.match(s))


def _is_real_prompt(text):
    """A typed user prompt — not a CLI-injected message or a continuation header."""
    return bool(text) and not _looks_system_injected(text)


def _dir_project(fp):
    """Project label for agents that don't record cwd: the containing folder."""
    return fp.parent.name or "unknown"


def _session(source, sid, project, started, prompts, turns=None):
    if not prompts:
        return None
    s = {"source": source, "session_id": sid, "project": project,
         "started_at": started, "prompts": prompts}
    if turns:
        s["turns"] = turns
    return s


def _load_json(fp):
    try:
        return json.loads(Path(fp).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _content_text(content):
    """Typed text from a Claude-style content field, or None for a tool result.

    A list containing tool_result blocks is a tool response, not a prompt.
    """
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result"
               for b in content):
            return None
        parts = [b["text"] for b in content
                 if isinstance(b, dict) and b.get("type") == "text" and b.get("text")]
        parts += [b for b in content if isinstance(b, str)]
        return "\n".join(parts).strip()
    return None


# ---- Agent-context helpers (only used when --agent-context is on): keep a
#      compact record of what the agent said/ran so the digest captures what the
#      user's prompts were reacting to (assistant replies + tool-call summaries).
_SHELL_TOOLS = {"Bash", "bash", "shell", "run_command", "local_shell",
                "exec_command", "Execute"}
_PATH_KEYS = ("file_path", "filePath", "path", "notebook_path", "relativePath")


def _clip(s, n):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n] + "…"


def _tool_summary(name, inp):
    """One short line for a tool call: the command/path it ran, truncated."""
    name = name or "tool"
    if isinstance(inp, str):
        return f"{name}: {_clip(inp, 160)}" if inp.strip() else name
    if isinstance(inp, dict):
        cmd = inp.get("command") or inp.get("cmd")
        if isinstance(cmd, list):
            cmd = " ".join(str(c) for c in cmd)
        if cmd:
            return f"{name}: {_clip(cmd, 160)}"
        for k in _PATH_KEYS:
            if inp.get(k):
                return f"{name}: {_clip(inp[k], 120)}"
        if inp.get("pattern"):
            return f"{name}: {_clip(inp['pattern'], 80)}"
    return name


def _turn(role, text):
    return {"role": role, "text": text}


# ---- Format detection: fingerprint a transcript file by its content, so an
#      agent's logs are parsed correctly regardless of where they're found.
_CODEX_SIG = re.compile(
    r'"type"\s*:\s*"(?:' + "|".join(sorted(CODEX_ENVELOPE_TYPES)) + r')"')


def detect_format(fp):
    try:
        with open(fp, encoding="utf-8") as fh:
            head = fh.read(65536).strip()
    except OSError:
        return None
    if not head:
        return None
    # Codex rollout first: its session_meta line can be longer than any byte cap
    # (large base_instructions), so a truncated json.loads would misfire. Match
    # the envelope signature on the head instead.
    if '"payload"' in head and _CODEX_SIG.search(head):
        return "codex"
    if head.startswith("{") and '"messages"' in head[:2048]:
        if '"info"' in head[:512] and ('"slug"' in head[:4096]
                or '"projectID"' in head[:4096] or '"sessionID"' in head[:8192]
                or '"parts"' in head[:8192]):
            return "opencode"
        return "gemini"
    for raw in head.split("\n")[:10]:
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        ot = obj.get("type", "")
        if "payload" in obj and ot in CODEX_ENVELOPE_TYPES:
            return "codex"
        if ot in ("session", "model_change") or "parentId" in obj:
            return "pi"
        if ot == "message" and isinstance(obj.get("message"), dict):
            inner = obj["message"]
            if any(k in inner for k in ("usage", "model", "stopReason")):
                return "pi"
            return "droid"
        if ot == "session_start":
            return "droid"
        if ot in ("user.message", "assistant.message", "session.start",
                  "tool.execution_complete", "assistant.turn_start"):
            return "copilot"
        if "role" in obj and "type" not in obj:
            return "cursor"
    return "claude"


# ---- Per-format extractors: each takes a file path and returns one session
#      dict (or None). Only user-typed prompts are kept; assistant/tool turns
#      are skipped (the digest fingerprints the user's own messages).
def _extract_claude(fp, agent_context=False):
    by_uuid, order, cwd, started = {}, [], None, None
    turns, grp_start, last_mid = [], 0, None
    for d in _iter_jsonl(fp):
        typ = d.get("type")
        if typ == "user":
            cwd = cwd or d.get("cwd")
            started = started or d.get("timestamp")
            if d.get("isMeta") or d.get("isSidechain"):
                continue
            text = _content_text((d.get("message") or {}).get("content"))
            if not _is_real_prompt(text):
                continue
            uuid = d.get("uuid") or f"_u{len(order)}"
            if uuid not in by_uuid:           # keep position of first occurrence,
                order.append(uuid)            # latest content (streaming-safe)
            by_uuid[uuid] = text
            if agent_context:
                turns.append(_turn("user", text))
                last_mid = None
        elif agent_context and typ == "assistant" and not d.get("isSidechain"):
            msg = d.get("message") or {}
            blocks = msg.get("content")
            if not isinstance(blocks, list):
                continue
            mid = msg.get("id")
            if mid is not None and mid == last_mid:
                del turns[grp_start:]         # replace this msg's streaming chunks
            else:
                grp_start, last_mid = len(turns), mid
            atext = "\n".join(
                b.get("text", "") for b in blocks
                if isinstance(b, dict) and b.get("type") == "text" and b.get("text")).strip()
            if atext:
                turns.append(_turn("assistant", atext))
            for b in blocks:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    turns.append(_turn("tool", _tool_summary(b.get("name"), b.get("input"))))
    return _session("Claude Code", fp.stem, _project_from_cwd(cwd), started,
                    [by_uuid[u] for u in order], turns)


def _codex_message_text(content):
    if isinstance(content, str):
        return content
    parts = []
    if isinstance(content, list):
        for it in content:
            if isinstance(it, dict) and it.get("type") in (
                    "input_text", "output_text", "text") and it.get("text"):
                parts.append(it["text"])
            elif isinstance(it, str):
                parts.append(it)
    return "\n".join(parts)


def _codex_tool_summary(p):
    t = p.get("type")
    if t == "local_shell_call":
        return _tool_summary(p.get("name") or "local_shell", p.get("action") or {})
    if t == "custom_tool_call":
        return _tool_summary(p.get("name"), {"input": p.get("input", "")})
    raw = p.get("arguments", "")                       # function_call
    if isinstance(raw, str):
        try:
            args = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            args = {"command": raw}
    else:
        args = raw if isinstance(raw, dict) else {}
    return _tool_summary(p.get("name") or "shell", args)


def _extract_codex(fp, agent_context=False):
    clean, fallback, cwd, started, sid = [], [], None, None, fp.stem
    turns = []
    for d in _iter_jsonl(fp):
        t, p = d.get("type"), d.get("payload") or {}
        started = started or d.get("timestamp")
        if t == "session_meta":
            cwd = cwd or p.get("cwd")
            sid = p.get("id") or sid
        elif t == "event_msg" and p.get("type") == "user_message":
            msg = (p.get("message") or "").strip()        # exact typed text
            if _is_real_prompt(msg):
                clean.append(msg)
                if agent_context:
                    turns.append(_turn("user", msg))
        elif t == "response_item":
            ptype, role = p.get("type"), p.get("role")
            if role == "user" and ptype == "message":
                txt = _codex_message_text(p.get("content", [])).strip()
                if _is_real_prompt(txt):
                    fallback.append(txt)
            elif agent_context and role == "assistant" and ptype == "message":
                txt = _codex_message_text(p.get("content", [])).strip()
                if txt:
                    turns.append(_turn("assistant", txt))
            elif agent_context and ptype in (
                    "function_call", "local_shell_call", "custom_tool_call"):
                turns.append(_turn("tool", _codex_tool_summary(p)))
    return _session("Codex", sid, _project_from_cwd(cwd), started,
                    clean or fallback, turns)        # prefer clean event_msg text


def _extract_gemini(fp, agent_context=False):
    data = _load_json(fp)
    if not isinstance(data, dict):
        return None
    prompts, started = [], None
    for m in data.get("messages", []):
        if not isinstance(m, dict):
            continue
        started = started or m.get("timestamp")
        if m.get("type") != "user":
            continue
        c = m.get("content", "")
        if isinstance(c, list):
            c = "\n".join(p.get("text", "") for p in c
                          if isinstance(p, dict) and p.get("text"))
        if isinstance(c, str) and _is_real_prompt(c.strip()):
            prompts.append(c.strip())
    return _session("Gemini CLI", fp.stem, _dir_project(fp), started, prompts)


def _extract_droid(fp, agent_context=False):
    prompts, started = [], None
    for d in _iter_jsonl(fp):
        if d.get("type") != "message":
            continue
        inner = d.get("message") or {}
        if inner.get("role") != "user":
            continue
        started = started or d.get("timestamp")
        text = _content_text(inner.get("content"))   # same content-block shape
        if _is_real_prompt(text):
            prompts.append(text)
    return _session("Factory Droid", fp.stem, _dir_project(fp), started, prompts)


def _extract_copilot(fp, agent_context=False):
    prompts, started = [], None
    for d in _iter_jsonl(fp):
        started = started or d.get("timestamp")
        if d.get("type") != "user.message":
            continue
        text = ((d.get("data") or {}).get("content") or "").strip()
        if _is_real_prompt(text):
            prompts.append(text)
    return _session("Copilot CLI", fp.stem, _dir_project(fp), started, prompts)


_CURSOR_TAG_RE = re.compile(
    r"<(?:user_query|attached_files|repo_map|relevant_files|additional_data|"
    r"context_files|applied_patches)>(.*?)</(?:user_query|attached_files|"
    r"repo_map|relevant_files|additional_data|context_files|applied_patches)>",
    re.DOTALL)


def _strip_cursor_tags(text):
    m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return (_CURSOR_TAG_RE.sub(r"\1", text).strip() or text.strip())


def _extract_cursor(fp, agent_context=False):
    prompts = []
    for d in _iter_jsonl(fp):
        if d.get("role") != "user":
            continue
        msg = d.get("message")
        content = msg.get("content", []) if isinstance(msg, dict) else msg
        if isinstance(content, list):
            content = "\n".join(b.get("text", "") for b in content
                                if isinstance(b, dict) and b.get("type") == "text")
        text = _strip_cursor_tags(content if isinstance(content, str) else "")
        if _is_real_prompt(text):
            prompts.append(text)
    return _session("Cursor", fp.stem, _dir_project(fp), None, prompts)


def _pi_active_branch(entries):
    """IDs on Pi's active conversation branch (/fork leaves dead branches)."""
    parent_of, order, has_ref = {}, [], False
    for e in entries:
        eid = e.get("id")
        if eid is None:
            continue
        pid = e.get("parentId") or None
        parent_of[eid] = pid
        order.append(eid)
        has_ref = has_ref or bool(pid)
    if not has_ref or not order:
        return None
    active, cur = set(), order[-1]
    while cur is not None and cur not in active:
        active.add(cur)
        cur = parent_of.get(cur)
    return active


def _extract_pi(fp, agent_context=False):
    entries = [d for d in _iter_jsonl(fp) if isinstance(d, dict)]
    active = _pi_active_branch(entries)
    prompts, started = [], None
    for d in entries:
        if d.get("type") != "message":
            continue
        if active is not None and d.get("id") not in active:
            continue
        msg = d.get("message") or {}
        started = started or d.get("timestamp")
        if msg.get("role") != "user":
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            content = "\n".join(it.get("text", "") for it in content
                                if isinstance(it, dict) and it.get("type") == "text"
                                and it.get("text"))
        text = content.strip() if isinstance(content, str) else ""
        if _is_real_prompt(text):
            prompts.append(text)
    return _session("Pi", fp.stem, _dir_project(fp), started, prompts)


def _extract_opencode_bundle(fp, agent_context=False):
    """OpenCode also ships a bundled session.json export ({info, messages})."""
    data = _load_json(fp)
    if not isinstance(data, dict) or "messages" not in data:
        return None
    prompts = []
    for msg in data.get("messages", []):
        if (msg.get("info") or {}).get("role") != "user":
            continue
        text = "\n".join(
            part.get("text", "") for part in msg.get("parts", [])
            if isinstance(part, dict) and part.get("type") == "text"
            and part.get("text") and not part.get("synthetic"))
        if _is_real_prompt(text.strip()):
            prompts.append(text.strip())
    info = data.get("info", {})
    return _session("OpenCode", info.get("id", Path(fp).stem),
                    _project_from_cwd(info.get("directory") or info.get("cwd") or ""),
                    _ms_to_iso((info.get("time") or {}).get("created")), prompts)


EXTRACTORS = {
    "claude": _extract_claude, "codex": _extract_codex, "gemini": _extract_gemini,
    "opencode": _extract_opencode_bundle, "droid": _extract_droid,
    "copilot": _extract_copilot, "cursor": _extract_cursor, "pi": _extract_pi,
}


def parse_file(fp, agent_context=False):
    """Detect a transcript's format and extract its session, or None."""
    fn = EXTRACTORS.get(detect_format(fp))
    if fn is None:
        return None
    try:
        return fn(Path(fp), agent_context)
    except Exception:          # one malformed transcript must never abort a run
        return None


def collect_files(root, agent_context=False):
    """Parse every transcript file under a root, dispatching by detected format."""
    root = Path(root)
    files = [root] if root.is_file() else sorted(
        set(root.rglob("*.jsonl")) | set(root.rglob("*.json")))
    return [s for s in (parse_file(fp, agent_context) for fp in files) if s]


# ---- OpenCode keeps conversations in a SQLite database (opencode.db: session /
#      message / part tables, each row's `data` a JSON blob), not in flat files.
#      So we read the DB directly. A bundled `opencode export` JSON (info +
#      messages) and the older split-file storage are handled as fallbacks.
def _ms_to_iso(ms):
    """OpenCode timestamps are epoch milliseconds; normalize to an ISO string."""
    try:
        return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).isoformat()
    except (TypeError, ValueError):
        return ""


def collect_opencode(root, agent_context=False):
    root = Path(root)
    db = (root if root.is_file() and root.suffix == ".db"
          else root / "opencode.db" if (root / "opencode.db").is_file() else None)
    if db:
        return _opencode_from_db(db, agent_context)
    bundles = collect_files(root, agent_context)       # exported session.json
    if bundles:
        return bundles
    return _opencode_from_split(root)


def _opencode_from_db(db_path, agent_context=False):
    """Read user prompts straight from opencode.db (read-only)."""
    try:
        import sqlite3                    # lazy: only needed when OpenCode is used
    except ImportError:
        print("  note: OpenCode sessions found but this Python lacks the sqlite3 "
              "module — skipping OpenCode.", file=sys.stderr)
        return []
    try:
        con = sqlite3.connect(f"file:{Path(db_path)}?mode=ro", uri=True)
    except sqlite3.Error:
        return []
    try:
        meta = {r[0]: (r[1], r[2]) for r in con.execute(
            "SELECT id, directory, time_created FROM session")}
        # One row per (message, text-part) for user messages, in turn order.
        # synthetic:true parts are OpenCode-injected (user-run tool announcements,
        # editor-context), never typed prose — exclude them at the source.
        rows = con.execute(
            "SELECT m.session_id, m.id, json_extract(p.data, '$.text') "
            "FROM message m JOIN part p ON p.message_id = m.id "
            "WHERE json_extract(m.data, '$.role') = 'user' "
            "  AND json_extract(p.data, '$.type') = 'text' "
            "  AND COALESCE(json_extract(p.data, '$.synthetic'), 0) = 0 "
            "ORDER BY m.session_id, m.time_created, m.id, p.time_created, p.id"
        ).fetchall()
        turns_by_sess = _opencode_turns_from_db(con) if agent_context else {}
    except sqlite3.Error:
        return []
    finally:
        con.close()

    by_msg = {}                          # (sid, mid) -> [text parts], in order
    for sid, mid, text in rows:
        if text:
            by_msg.setdefault((sid, mid), []).append(text)
    prompts_by_sess = {}                 # sid -> [prompt, ...], in turn order
    for (sid, mid), texts in by_msg.items():
        prompt = "\n".join(texts).strip()
        if _is_real_prompt(prompt):
            prompts_by_sess.setdefault(sid, []).append(prompt)

    sessions = []
    for sid, prompts in prompts_by_sess.items():
        directory, created = meta.get(sid, (None, None))
        s = _session("OpenCode", sid, _project_from_cwd(directory or ""),
                     _ms_to_iso(created), prompts, turns_by_sess.get(sid))
        if s:
            sessions.append(s)
    return sessions


def _opencode_turns_from_db(con):
    """Ordered user/assistant/tool turns per session, for --agent-context."""
    rows = con.execute(
        "SELECT m.session_id, json_extract(m.data, '$.role'), "
        "       json_extract(p.data, '$.type'), json_extract(p.data, '$.text'), "
        "       json_extract(p.data, '$.tool'), json_extract(p.data, '$.state'), "
        "       COALESCE(json_extract(p.data, '$.synthetic'), 0) "
        "FROM message m JOIN part p ON p.message_id = m.id "
        "ORDER BY m.session_id, m.time_created, m.id, p.time_created, p.id"
    ).fetchall()
    turns = {}
    for sid, role, ptype, text, tool, state, synthetic in rows:
        if ptype == "text" and text and not synthetic:
            if role == "user" and _is_real_prompt(text):
                turns.setdefault(sid, []).append(_turn("user", text.strip()))
            elif role == "assistant":
                turns.setdefault(sid, []).append(_turn("assistant", text.strip()))
        elif ptype == "tool" and tool:
            inp = {}
            if state:
                try:
                    inp = (json.loads(state) or {}).get("input", {})
                except json.JSONDecodeError:
                    inp = {}
            turns.setdefault(sid, []).append(_turn("tool", _tool_summary(tool, inp)))
    return turns


def _opencode_from_split(root):
    """Legacy fallback: split-file storage (storage/message/<ses>/<msg>.json)."""
    msg_root = root / "message"
    if not msg_root.is_dir():
        msg_root = root / "session" / "message"
    if not msg_root.is_dir():
        return []
    sessions = []
    for sess_dir in sorted(p for p in msg_root.iterdir() if p.is_dir()):
        sid, prompts, started = sess_dir.name, [], None
        for mf in sorted(sess_dir.glob("*.json")):
            d = _load_json(mf)
            if not isinstance(d, dict) or d.get("role") != "user":
                continue
            started = started or _ms_to_iso((d.get("time") or {}).get("created"))
            text = _opencode_split_text(d, root, sid, d.get("id"))
            if _is_real_prompt(text.strip()):
                prompts.append(text.strip())
        s = _session("OpenCode", sid, _opencode_split_project(root, sid),
                     started, prompts)
        if s:
            sessions.append(s)
    return sessions


def _opencode_split_text(d, root, sid, mid):
    parts = d.get("parts")
    if isinstance(parts, list):
        chunks = [p.get("text", "") for p in parts
                  if isinstance(p, dict) and p.get("type") == "text"
                  and p.get("text") and not p.get("synthetic")]
        if chunks:
            return "\n".join(chunks)
    if isinstance(d.get("content"), str):
        return d["content"]
    pdir = root / "part" / sid / (mid or "")
    if pdir.is_dir():
        chunks = [pd["text"] for pf in sorted(pdir.glob("*.json"))
                  for pd in [_load_json(pf)]
                  if isinstance(pd, dict) and pd.get("type") == "text" and pd.get("text")]
        if chunks:
            return "\n".join(chunks)
    return ""


def _opencode_split_project(root, sid):
    d = _load_json(root / "session" / "info" / f"{sid}.json")
    if isinstance(d, dict):
        return _project_from_cwd(d.get("directory") or d.get("cwd") or "")
    return "unknown"


# Agent -> collector. Each collector takes a root path and returns sessions.
# OpenCode needs directory-wise assembly; every other agent is sniffed per file.
COLLECTORS = {name: (collect_opencode if name == "OpenCode" else collect_files)
              for name in DEFAULT_PATHS}


# --------------------------------------------------------------------------- #
# Digest builder (deterministic; same schema as data/digests/<slug>.json)
# --------------------------------------------------------------------------- #

def _truncate_words(text, n):
    words = text.split()
    if len(words) <= n:
        return text
    return " ".join(words[:n]) + f" […truncated, {len(words)} words total]"


def _dist(values):
    total = len(values)
    if not total:
        return {}
    counts = {}
    for v in values:
        counts[str(v)] = counts.get(str(v), 0) + 1
    return {k: round(c / total, 3) for k, c in
            sorted(counts.items(), key=lambda kv: -kv[1])}


def _quantile(values, q):
    s = sorted(values)
    if not s:
        return None
    idx = q * (len(s) - 1)
    lo = int(idx)
    if lo + 1 >= len(s):
        return float(s[-1])
    return float(s[lo] + (s[lo + 1] - s[lo]) * (idx - lo))


# Agent-context sampling (only when --agent-context). Caps keep the digest small.
MAX_CONTEXT_SESSIONS = 30
MAX_CONTEXT_TURNS = 24
CONTEXT_USER_WORDS = 120
CONTEXT_ASSISTANT_WORDS = 50


def _context_turns(turns):
    """Truncate one session's turns for inclusion in the digest."""
    out = []
    for t in turns[:MAX_CONTEXT_TURNS]:
        role, text = t["role"], t["text"]
        if role == "user":
            out.append(_turn("user", _truncate_words(text, CONTEXT_USER_WORDS)))
        elif role == "assistant":
            out.append(_turn("assistant", _truncate_words(text, CONTEXT_ASSISTANT_WORDS)))
        else:
            out.append(_turn("tool", _clip(text, 200)))
    return out


def build_digest(sessions, slug):
    sessions = [s for s in sessions if s["prompts"]]
    sessions.sort(key=lambda s: s.get("started_at") or "")

    all_words, opening, mids = [], [], []
    for s in sessions:
        for i, text in enumerate(s["prompts"]):
            all_words.append(len(text.split()))
            tag = {"source": s["source"], "project": s["project"]}
            if i == 0:
                tag["text"] = _truncate_words(text, FIRST_PROMPT_WORDS)
                opening.append(tag)
            else:
                tag["text"] = _truncate_words(text, MID_PROMPT_WORDS)
                mids.append(tag)

    opening = opening[:MAX_FIRST_PROMPTS]
    if len(mids) > MAX_MID_PROMPTS:                 # deterministic even-stride sample
        step = len(mids) / MAX_MID_PROMPTS
        mids = [mids[int(i * step)] for i in range(MAX_MID_PROMPTS)]

    dates = [s["started_at"][:10] for s in sessions
             if isinstance(s.get("started_at"), str) and s["started_at"]]
    per_session = [len(s["prompts"]) for s in sessions]

    digest = {
        "stats": {
            "user_id": slug, "slug": slug,
            "n_sessions_total": len(sessions),
            "sources": _dist([s["source"] for s in sessions]),
            "agents": _dist([s["source"] for s in sessions]),
            "repos": _dist([s["project"] for s in sessions]),
            "date_range": [min(dates), max(dates)] if dates else [None, None],
            "n_prompts_total": len(all_words),
            "prompt_words": {
                "median": float(statistics.median(all_words)) if all_words else None,
                "p90": _quantile(all_words, 0.9),
                "max": float(max(all_words)) if all_words else None,
            },
            "session_turns_median": (
                float(statistics.median(per_session)) if per_session else None),
        },
        "opening_prompts": opening,
        "mid_session_prompts": mids,
    }

    # --agent-context: interleaved user/assistant/tool transcripts for a sample of
    # sessions, so the distiller sees what the user's messages were reacting to.
    ctx_sessions = [s for s in sessions if s.get("turns")][:MAX_CONTEXT_SESSIONS]
    if ctx_sessions:
        digest["agent_context"] = [
            {"source": s["source"], "project": s["project"],
             "turns": _context_turns(s["turns"])}
            for s in ctx_sessions
        ]
    return digest


# --------------------------------------------------------------------------- #
# Profile generation (claude CLI, else Anthropic API single-shot)
# --------------------------------------------------------------------------- #

def generate_with_cli(digest_path: Path, out_dir: Path, model: str):
    # The distillation agent is NOT read-only: it must Write the profile files.
    # But it is tightly scoped — Read (digest + skill) + Write/Glob (output) only.
    # No Bash, no WebFetch/WebSearch, no Task subagents, so it cannot run shell
    # commands, reach the network, or touch the wider filesystem. acceptEdits
    # auto-approves the file writes the skill makes under users/<slug>/.
    prompt = (
        f"Read the skill file {SKILL.relative_to(ROOT)} and follow it exactly with "
        f"$1={digest_path.relative_to(ROOT)} and $2={out_dir.relative_to(ROOT)}. "
        f"Create every required file. Write ONLY inside {out_dir.relative_to(ROOT)}. "
        f"Work autonomously; do not ask questions.")
    cmd = ["claude", "-p", prompt, "--model", model,
           "--allowedTools", "Read,Write,Glob",
           "--permission-mode", "acceptEdits", "--max-turns", "40"]
    print(f"  running: claude -p (model {model}) …")
    return subprocess.run(cmd, cwd=ROOT, text=True).returncode == 0


def generate_with_api(digest_path: Path, out_dir: Path, model: str, api_key: str):
    try:
        import anthropic
    except ImportError:
        sys.exit("  ERROR: the `anthropic` package is required for the API path.\n"
                 "         install it with:  pip install anthropic")
    client = anthropic.Anthropic(api_key=api_key)
    instruction = (
        f"{SKILL.read_text(encoding='utf-8')}\n\n---\n\n"
        f"You cannot use file tools. The digest ($1) is provided inline below; the "
        f"output folder ($2) is `{out_dir.name}/`. Produce every required file per "
        f"the skill. Respond with ONLY a JSON object mapping each relative file path "
        f"(e.g. \"USER.md\", \"skills/terse-redirect.md\") to its full text contents. "
        f"No prose, no markdown fences.\n\nDIGEST ($1):\n"
        f"{digest_path.read_text(encoding='utf-8')}")
    print(f"  calling Anthropic API (model {model}) …")
    msg = client.messages.create(
        model=model, max_tokens=16000,
        messages=[{"role": "user", "content": instruction}])
    raw = "".join(b.text for b in msg.content if b.type == "text")
    files = _parse_json_object(raw)
    if not isinstance(files, dict):
        sys.exit("  ERROR: model did not return a JSON object of files.")
    for rel, content in files.items():
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    return all((out_dir / f).exists() for f in REQUIRED)


def _parse_json_object(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}")
        if start >= 0 and end > start:
            return json.loads(raw[start:end + 1])
        raise


# --------------------------------------------------------------------------- #
# Wizard
# --------------------------------------------------------------------------- #

def _ask(prompt, default=""):
    try:
        return input(prompt).strip() or default
    except EOFError:
        return default


def _collect(tool, path, agent_context=False):
    """Sessions for one agent at *path*, or None if the path doesn't exist."""
    path = Path(path).expanduser()
    return COLLECTORS[tool](path, agent_context) if path.exists() else None


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for name, stem in FLAG_STEM.items():
        ap.add_argument(f"--{stem}-path", dest=f"path_{stem}",
                        default=str(DEFAULT_PATHS[name]),
                        help=f"{name} sessions directory")
    ap.add_argument("--slug", default="me", help="profile id / output folder name")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--api-key", default=None,
                    help="Anthropic API key (or set ANTHROPIC_API_KEY)")
    ap.add_argument("--use-api", action="store_true",
                    help="use the Anthropic API key instead of the claude CLI "
                         "subscription (implied when --api-key is given)")
    ap.add_argument("--agent-context", action="store_true",
                    help="also keep assistant turns + tool-call summaries in the "
                         "digest (what the agent replied and ran)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing users/<slug>/ folder")
    ap.add_argument("--yes", action="store_true",
                    help="skip all prompts; use given/default paths")
    args = ap.parse_args()

    # Guard the output folder up front so a long detect/generate isn't wasted.
    out_dir = ROOT / "users" / args.slug
    if not args.force and any((out_dir / f).exists() for f in REQUIRED):
        sys.exit(f"\nusers/{args.slug}/ already exists. Choose another --slug "
                 f"(e.g. --slug {args.slug}-v2) or pass --force to overwrite.")

    paths = {name: getattr(args, f"path_{stem}") for name, stem in FLAG_STEM.items()}
    interactive = not args.yes and sys.stdin.isatty()
    width = max(len(n) for n in paths)

    print("\n== Detecting local coding trajectories ==\n")
    for tool in paths:
        sess = _collect(tool, paths[tool], args.agent_context)
        status = f"{len(sess)} sessions" if sess is not None else "path not found"
        print(f"  {tool:{width}s}  {str(Path(paths[tool]).expanduser()):52s} {status}")
        if interactive:
            new = _ask("    ↳ enter to keep, or paste a different path: ")
            if new:
                paths[tool] = new
                sess = _collect(tool, new, args.agent_context)
                print(f"      now: "
                      f"{len(sess) if sess is not None else 'path not found'} sessions")

    detected = {t: (_collect(t, p, args.agent_context) or [])
                for t, p in paths.items()}
    sessions = [s for sess in detected.values() for s in sess]
    total = len(sessions)

    print("\n== Summary ==")
    for tool, sess in detected.items():
        if sess:
            print(f"  {tool:{width}s}  {len(sess):5d} sessions  "
                  f"({Path(paths[tool]).expanduser()})")
    print(f"  {'TOTAL':{width}s}  {total:5d} sessions across "
          f"{sum(1 for s in detected.values() if s)} agent(s)")
    if not total:
        sys.exit("\nNo sessions found. Correct the paths above and re-run.")

    if interactive and _ask(
            f"\nGenerate a user profile from these {total} sessions? [y/N] ",
            "n").lower() not in ("y", "yes"):
        sys.exit("Aborted.")

    digest = build_digest(sessions, args.slug)
    digest_path = ROOT / "data" / "digests" / f"{args.slug}.json"
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    digest_path.write_text(json.dumps(digest, indent=1, ensure_ascii=False),
                           encoding="utf-8")
    ctx = (f", agent-context for {len(digest['agent_context'])} sessions"
           if digest.get("agent_context") else "")
    print(f"\n  wrote digest -> {digest_path.relative_to(ROOT)} "
          f"({digest['stats']['n_prompts_total']} prompts, "
          f"median {digest['stats']['prompt_words']['median']} words{ctx})")

    out_dir.mkdir(parents=True, exist_ok=True)

    # Force the API path when asked (--use-api or an explicit --api-key); else
    # prefer the claude CLI subscription, falling back to the API if it's absent.
    use_api = args.use_api or bool(args.api_key)
    if not use_api and shutil.which("claude"):
        print("\n  `claude` CLI found — using your Claude subscription.")
        ok = generate_with_cli(digest_path, out_dir, args.model)
    else:
        reason = ("as requested" if use_api else "`claude` CLI not found")
        print(f"\n  using the Anthropic API ({reason}).")
        api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key and interactive:
            api_key = getpass.getpass("  paste your ANTHROPIC_API_KEY (hidden): ").strip()
        if not api_key:
            sys.exit("  No API key available. Set ANTHROPIC_API_KEY or pass --api-key.")
        ok = generate_with_api(digest_path, out_dir, args.model, api_key)

    missing = [f for f in REQUIRED if not (out_dir / f).exists()]
    if ok and not missing:
        n_skills = (len(list((out_dir / "skills").glob("*.md")))
                    if (out_dir / "skills").is_dir() else 0)
        print(f"\n✓ Profile written to {out_dir.relative_to(ROOT)}/ "
              f"({n_skills} skills). Open USER.md to review.")
    else:
        sys.exit(f"\n✗ Generation incomplete; missing: {missing or 'unknown'}")


if __name__ == "__main__":
    main()

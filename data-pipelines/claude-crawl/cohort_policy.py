"""Shared deterministic cohort policy for SWESimBench v2."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from difflib import SequenceMatcher
from functools import lru_cache
from typing import Iterable

import tiktoken

POLICY_VERSION = "swesimbench-v2-cohort-policy-2026-07-13.18"

RECONSTRUCTION_THRESHOLDS = {
    "minimum_chars": 24,
    "distinctive_event_chars": 40,
    "timestamp_tolerance_seconds": 2,
    "timestamp_ordered_shared": 3,
    "timestamp_ordered_coverage": 0.5,
    "timestamp_shared_chars": 120,
    "timestamp_matches": 2,
    "content_ordered_shared": 5,
    "content_ordered_coverage": 0.8,
    "content_shared_chars": 300,
}

# Drop developers whose sessions are mostly tiny automation fragments
# (e.g. daemon boot/triage jobs that never yield post-assistant targets).
FRAGMENTATION_THRESHOLDS = {
    "minimum_sessions": 100,
    "maximum_mean_human_turns_per_session": 1.5,
}

# Drop sessions that are not real dialogues. Conservative default: require at
# least one assistant turn and one human/user turn. Do NOT require a
# post-assistant user target — short user→assistant sessions are valid dialogue
# even though they yield no eval points.
DIALOGUE_THRESHOLDS = {
    "minimum_assistant_turns": 1,
    "minimum_human_turns": 1,
}

# Skip human-target user turns above this token count when selecting eval /
# prediction points (prepare.py, ATIF sample builders). Sessions themselves
# are retained — megapastes may still appear in history context.
# Tokenizer: OpenAI cl100k_base via tiktoken (same family as GPT-4 / ChatGPT).
# Motivation (2026-07-14): v2 user turns are typically short; sampled turns near
# 500 / 1000 / 2000 whitespace-words showed ≥1000 dominated by bulk pastes
# (IDE context walls, console dumps, kubectl/log spam). Cap is in cl100k tokens
# (not whitespace words). Do NOT set this near Entire/DataClaw harvest word-caps
# (~300–400 words) — those measure source truncation, not realism.
TURN_LENGTH_THRESHOLDS = {
    "encoding": "cl100k_base",
    "maximum_human_target_tokens": 1000,
}

EXCLUDED_USERS = {
    "gh:wolffbe": "benchmark harness",
    "gh:austinweitao": "observer-agent scaffolding",
    "gh:skkeoriw": "skill automation",
    "gh:contextlab": "automation",
    "gh:nwags": "benchmark automation",
    "gh:jedisct1": "automation",
    "dc:jedisct1": "automation",
    "gh:zchee": "harness injections",
    "gh:entireio": "organization account",
    "gh:entireio-team": "organization account",
    "gh:partial-staging": "dogfood account",
    "gh:mhaitana": "synthetic placeholder sessions containing only 'turn N' / 'ok'",
}

# These are retained in the trace with a non-user role, but can never be scored
# as a developer target.
SYSTEM_PREFIXES = (
    "Base directory for this skill:",
    "This session is being continued",
    "<system-reminder",
    "<system_instruction",
    "[SYSTEM",
    "<user_instructions",
    "<environment_context",
    "<permissions",
    "<turn_context",
    "<budget:",
    "<session-start-hook",
    "<user-prompt-submit-hook",
    "<user-memory-input",
    "<system_notification",
    "Tool loaded",
    "Skill loaded",
    "<skill-",
    "<uploaded_files",
    "<ide_opened_file",
    "<ide_selection",
    "<ide_diagnostics",
    "<ide-",
    # Cursor IDE injection wrappers (no <user_query> body).
    "<attached_files",
    "<cursor_commands",
    "<external_links",
    "<git_status",
    "<timestamp",
    "<agent_transcripts",
    "<manually_attached_skills",
    "<hooks_context",
    "<uploaded_documents",
    "<subagent_delegation_context",
    "<image_files",
    "<image>",
    "<open_and_recently_viewed_files",
    "<rules>",
    "<always_applied_workspace_rules",
)
TOOL_PREFIXES = (
    "<bash-stdout",
    "<bash-stderr",
    "<bash-input",
    "<bash-notification",
    "<post-tool",
    "<pre-tool",
    "<turn_aborted",
    "[Request interrupted",
    "<command",
    "<local-command",
    "Caveat:",
)
# Synthetic harness pings — not developer text and not real tool_use/tool_result.
METADATA_PREFIXES = (
    "<task-notification",
    "<subagent_notification",
    "<teammate-message",
)
COMMAND_MARKER_PREFIXES = ("<command-message", "<command-name")

PLACEHOLDER_PATTERNS = (
    re.compile(r"^turn\s+\d+$", re.I),
    re.compile(r"^(test|testing|placeholder|sample|dummy)(\s+\d+)?$", re.I),
    re.compile(r"^(hello|hi)\s+world!?$", re.I),
)
INJECTED_SYSTEM_PATTERNS = (
    re.compile(r"^#{1,3}\s*SKILL\s*:", re.I),
    re.compile(r"^<skill(?:\s|>)", re.I),
    re.compile(r"^#\s*AGENTS\.md instructions for\b", re.I),
    # Cursor UI chrome / one-click action templates.
    re.compile(r"^Implement the plan as specified\b", re.I),
    re.compile(r"^Commit the right changes for this branch\b", re.I),
    re.compile(r"^Stage the changes you worked on\b", re.I),
    re.compile(r"^Verify each finding against the current\b", re.I),
)
USER_QUERY_RE = re.compile(r"<user_query>\s*([\s\S]*?)\s*</user_query>", re.I)
UUID_RE = re.compile(
    r"(?i)^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
# Entire checkpoint ids often look like 2026-01-21-<uuid>.
DATE_PREFIXED_UUID_RE = re.compile(
    r"(?i)^(\d{4}-\d{2}-\d{2})-"
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$"
)

SECRET_PATTERNS = (
    (re.compile(r"sk-[A-Za-z0-9_-]{16,}"), "[REDACTED_SK]"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "[REDACTED_GH_PAT]"),
    (re.compile(r"gho_[A-Za-z0-9]{20,}"), "[REDACTED_GH]"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "[REDACTED_GH_PAT]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED_AWS_KEY]"),
    (re.compile(r"AIza[0-9A-Za-z_-]{30,}"), "[REDACTED_GOOGLE_KEY]"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "[REDACTED_SLACK]"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"), "bearer [REDACTED]"),
    (
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?"
            r"-----END [A-Z ]*PRIVATE KEY-----"
        ),
        "[REDACTED_PRIVATE_KEY]",
    ),
    (
        re.compile(
            r'(?i)(api[_-]?key|secret|token|password)["\'`]?\s*[:=]\s*'
            r'["\'`]?([A-Za-z0-9_-]{16,})'
        ),
        r"\1=[REDACTED]",
    ),
)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def developer_text(text: str) -> str:
    """Prefer Cursor <user_query> bodies when present; else keep the raw text."""
    matches = [part.strip() for part in USER_QUERY_RE.findall(text or "") if part.strip()]
    if matches:
        return "\n\n".join(matches)
    return text or ""


def canonical_session_id(session_id: str) -> str:
    """Normalize native UUID, date-prefixed UUID, or pipe-wrapped IDs ending in UUID.

    Handles crawl shapes like ``reparse|owner|uuid`` and ``owner/repo|uuid``.
    """
    value = (session_id or "").strip()
    if UUID_RE.fullmatch(value):
        return value.lower()
    dated = DATE_PREFIXED_UUID_RE.fullmatch(value)
    if dated:
        return dated.group(2).lower()
    if "|" in value:
        final = value.rsplit("|", 1)[-1]
        if UUID_RE.fullmatch(final):
            return final.lower()
        dated = DATE_PREFIXED_UUID_RE.fullmatch(final)
        if dated:
            return dated.group(2).lower()
    return value


def specstory_session_id(session: dict) -> str:
    """Stable SpecStory session id: native UUID when present, else repo|file."""
    sid = (session.get("session_id") or "").strip()
    if sid:
        return sid
    repo = session.get("repo") or "?"
    filename = session.get("file") or "?"
    return f"ss:{repo}|{filename}"


def specstory_timestamp(session: dict) -> str | None:
    """Normalize SpecStory filename timestamps to sortable ISO-like strings."""
    raw = (session.get("session_ts") or "").strip()
    if not raw:
        return None
    value = raw.rstrip("Z")
    if "_" in value and "T" not in value:
        date, time = value.split("_", 1)
        time = time.replace("-", ":")
        if len(time) == 5:
            time = f"{time}:00"
        return f"{date}T{time}"
    return value


def injected_role(text: str) -> str | None:
    stripped = (text or "").lstrip()
    if not stripped:
        return "metadata"
    if stripped.startswith(SYSTEM_PREFIXES):
        return "system"
    if any(pattern.match(stripped) for pattern in INJECTED_SYSTEM_PATTERNS):
        return "system"
    if stripped.startswith(METADATA_PREFIXES):
        return "metadata"
    if stripped.startswith(TOOL_PREFIXES):
        return "tool"
    return None


def command_expansion_payloads(turns: Iterable[dict]) -> set[str]:
    """Find user-role payloads injected immediately after a slash-command marker."""
    sequence = list(turns)
    payloads = set()
    for index in range(1, len(sequence)):
        previous = (sequence[index - 1].get("text") or "").lstrip()
        turn = sequence[index]
        text = turn.get("text") or ""
        if (
            turn.get("role") in {"user", "system"}
            and injected_role(text) is None
            and previous.startswith(COMMAND_MARKER_PREFIXES)
        ):
            payloads.add(normalize_text(text))
    return payloads


def is_placeholder(text: str) -> bool:
    value = normalize_text(text).lower()
    return bool(value) and any(pattern.fullmatch(value) for pattern in PLACEHOLDER_PATTERNS)


def is_human_target(turn_or_text: dict | str) -> bool:
    text = turn_or_text.get("text", "") if isinstance(turn_or_text, dict) else turn_or_text
    stripped = developer_text(text).strip()
    return bool(stripped) and injected_role(stripped) is None and not is_placeholder(stripped)


def trace_role(turn: dict) -> str:
    role = turn.get("role")
    if role != "user":
        return role if role in {"assistant", "system", "tool"} else "metadata"
    text = developer_text(turn.get("text") or "")
    return injected_role(text) or ("metadata" if is_placeholder(text) else "user")


def scrub_text(text: str) -> str:
    value = text or ""
    # JSONL-safe: collapse Unicode line/paragraph separators that break splitlines().
    value = value.replace("\u0085", " ").replace("\u2028", " ").replace("\u2029", " ")
    for pattern, replacement in SECRET_PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def clean_turn(turn: dict) -> dict:
    result = dict(turn)
    raw = turn.get("text") or ""
    text = developer_text(raw) if turn.get("role") == "user" else raw
    result["role"] = trace_role({**turn, "text": text} if text != raw else turn)
    result["text"] = scrub_text(text)
    return result


def ordered_trace_sequence(turns: Iterable[dict]) -> tuple[str, ...]:
    sequence = []
    for turn in turns:
        role = trace_role(turn)
        raw = turn.get("text") or ""
        text = developer_text(raw) if turn.get("role") == "user" or role == "user" else raw
        text = normalize_text(scrub_text(text)).lower()
        if text:
            sequence.append(f"{role}\0{text}")
    return tuple(sequence)


def transcript_hash(turns: Iterable[dict]) -> str:
    payload = "\n".join(ordered_trace_sequence(turns)).encode()
    return hashlib.sha256(payload).hexdigest()


def substantial_human_count(turns: Iterable[dict], minimum_chars: int = 24) -> int:
    return sum(
        1
        for turn in turns
        if turn.get("role") == "user"
        and is_human_target(turn)
        and len(normalize_text(developer_text(turn.get("text") or ""))) >= minimum_chars
    )


def human_turn_count(turns: Iterable[dict]) -> int:
    return sum(1 for turn in turns if turn.get("role") == "user" and is_human_target(turn))


def assistant_turn_count(turns: Iterable[dict]) -> int:
    return sum(1 for turn in turns if turn.get("role") == "assistant")


def is_incomplete_dialogue(turns: Iterable[dict]) -> bool:
    """True when a session lacks real dialogue (no assistant or no human turns).

    User-only prompt logs (e.g. Entire recovery gaps) and assistant/metadata-only
    traces cannot support dialogue modeling. Sessions with user→assistant and no
    later user turn still count as complete dialogue under this conservative rule.
    """
    sequence = list(turns)
    return (
        assistant_turn_count(sequence)
        < DIALOGUE_THRESHOLDS["minimum_assistant_turns"]
        or human_turn_count(sequence) < DIALOGUE_THRESHOLDS["minimum_human_turns"]
    )


@lru_cache(maxsize=1)
def _turn_length_encoding():
    return tiktoken.get_encoding(TURN_LENGTH_THRESHOLDS["encoding"])


def human_target_token_count(turn: dict) -> int:
    """cl100k token count of the developer-facing user text."""
    text = developer_text(turn.get("text") or "")
    if not text:
        return 0
    return len(_turn_length_encoding().encode(text))


def is_oversized_human_turn(turn: dict) -> bool:
    """True when a single human-target user turn exceeds the prediction token cap.

    Uses cheap length short-circuits so multi-megabyte pastes are not fully
    tokenized.
    """
    if turn.get("role") != "user" or not is_human_target(turn):
        return False
    text = developer_text(turn.get("text") or "")
    if not text:
        return False
    cap = TURN_LENGTH_THRESHOLDS["maximum_human_target_tokens"]
    n_chars = len(text)
    if n_chars <= cap:
        return False
    if n_chars >= cap * 16:
        return True
    return human_target_token_count(turn) > cap


def is_predictable_human_turn(turn: dict) -> bool:
    """Scorable developer target for eval / prediction point selection."""
    return (
        turn.get("role") == "user"
        and is_human_target(turn)
        and not is_oversized_human_turn(turn)
    )


def max_human_target_tokens(turns: Iterable[dict]) -> int:
    """Longest human-target user turn (cl100k tokens) in a session; 0 if none."""
    longest = 0
    for turn in turns:
        if turn.get("role") != "user" or not is_human_target(turn):
            continue
        longest = max(longest, human_target_token_count(turn))
    return longest


def has_oversized_human_turn(turns: Iterable[dict]) -> bool:
    """True when any human-target user turn exceeds the prediction token cap."""
    return any(
        is_oversized_human_turn(turn)
        for turn in turns
        if turn.get("role") == "user"
    )


def timestamp_seconds(value: object) -> float | None:
    if value is None:
        return None
    try:
        text = str(value).strip().replace("Z", "+00:00")
        return datetime.fromisoformat(text).timestamp()
    except (TypeError, ValueError, OverflowError):
        return None


def substantial_user_events(
    turns: Iterable[dict],
    minimum_chars: int = RECONSTRUCTION_THRESHOLDS["minimum_chars"],
) -> tuple[dict, ...]:
    events = []
    for turn in turns:
        if trace_role(turn) != "user":
            continue
        text = normalize_text(scrub_text(developer_text(turn.get("text") or ""))).lower()
        if len(text) < minimum_chars:
            continue
        events.append(
            {
                "text": text,
                "timestamp": timestamp_seconds(
                    turn.get("ts") or turn.get("timestamp") or turn.get("created_at")
                ),
            }
        )
    return tuple(events)


def reconstructed_session_evidence(
    left_turns: Iterable[dict], right_turns: Iterable[dict]
) -> dict | None:
    """Return conservative evidence for cross-source reconstructions of one session."""
    left = substantial_user_events(left_turns)
    right = substantial_user_events(right_turns)
    if not left or not right:
        return None

    left_text = [event["text"] for event in left]
    right_text = [event["text"] for event in right]
    shared = set(left_text) & set(right_text)
    if not shared:
        return None

    ordered_shared = sum(
        block.size
        for block in SequenceMatcher(
            None, left_text, right_text, autojunk=False
        ).get_matching_blocks()
    )
    ordered_coverage = ordered_shared / min(len(left_text), len(right_text))
    shared_chars = sum(len(text) for text in shared)

    timestamp_matches = 0
    timestamp_matched_texts = []
    for text in shared:
        left_times = [
            event["timestamp"]
            for event in left
            if event["text"] == text and event["timestamp"] is not None
        ]
        right_times = [
            event["timestamp"]
            for event in right
            if event["text"] == text and event["timestamp"] is not None
        ]
        if any(
            abs(a - b)
            <= RECONSTRUCTION_THRESHOLDS["timestamp_tolerance_seconds"]
            for a in left_times
            for b in right_times
        ):
            timestamp_matches += 1
            timestamp_matched_texts.append(text)

    exact_event_anchor = any(
        len(text) >= RECONSTRUCTION_THRESHOLDS["distinctive_event_chars"]
        for text in timestamp_matched_texts
    )
    if not exact_event_anchor and (min(len(left), len(right)) < 3 or len(shared) < 3):
        return None

    first_text_match = (
        left_text[0] == right_text[0]
        and len(left_text[0])
        >= RECONSTRUCTION_THRESHOLDS["distinctive_event_chars"]
    )
    first_timestamp_match = bool(
        first_text_match
        and left[0]["timestamp"] is not None
        and right[0]["timestamp"] is not None
        and abs(left[0]["timestamp"] - right[0]["timestamp"])
        <= RECONSTRUCTION_THRESHOLDS["timestamp_tolerance_seconds"]
    )

    timestamp_anchored = exact_event_anchor or (
        ordered_shared >= RECONSTRUCTION_THRESHOLDS["timestamp_ordered_shared"]
        and ordered_coverage
        >= RECONSTRUCTION_THRESHOLDS["timestamp_ordered_coverage"]
        and shared_chars >= RECONSTRUCTION_THRESHOLDS["timestamp_shared_chars"]
        and (
            timestamp_matches >= RECONSTRUCTION_THRESHOLDS["timestamp_matches"]
            or first_timestamp_match
        )
    )
    content_anchored = (
        first_text_match
        and ordered_shared >= RECONSTRUCTION_THRESHOLDS["content_ordered_shared"]
        and ordered_coverage
        >= RECONSTRUCTION_THRESHOLDS["content_ordered_coverage"]
        and shared_chars >= RECONSTRUCTION_THRESHOLDS["content_shared_chars"]
    )
    if not (timestamp_anchored or content_anchored):
        return None
    return {
        "ordered_shared_substantial_user_turns": ordered_shared,
        "ordered_coverage_of_shorter_trace": round(ordered_coverage, 6),
        "shared_unique_substantial_user_turns": len(shared),
        "shared_unique_chars": shared_chars,
        "timestamp_matched_turns": timestamp_matches,
        "first_user_text_match": first_text_match,
        "first_user_timestamp_match": first_timestamp_match,
        "anchor": (
            "exact_event_timestamp"
            if exact_event_anchor
            else ("timestamp" if timestamp_anchored else "content")
        ),
    }


def is_extreme_session_fragmentation(
    session_count: int, human_turns: int
) -> bool:
    """True when a developer is dominated by tiny one-shot sessions."""
    if session_count < FRAGMENTATION_THRESHOLDS["minimum_sessions"]:
        return False
    mean = human_turns / session_count if session_count else 0.0
    return mean < FRAGMENTATION_THRESHOLDS["maximum_mean_human_turns_per_session"]


def policy_fingerprint() -> str:
    payload = {
        "version": POLICY_VERSION,
        "excluded_users": EXCLUDED_USERS,
        "system_prefixes": SYSTEM_PREFIXES,
        "tool_prefixes": TOOL_PREFIXES,
        "metadata_prefixes": METADATA_PREFIXES,
        "command_marker_prefixes": COMMAND_MARKER_PREFIXES,
        "placeholder_patterns": [pattern.pattern for pattern in PLACEHOLDER_PATTERNS],
        "injected_system_patterns": [
            pattern.pattern for pattern in INJECTED_SYSTEM_PATTERNS
        ],
        "user_query_unwrap": USER_QUERY_RE.pattern,
        "secret_patterns": [pattern.pattern for pattern, _ in SECRET_PATTERNS],
        "reconstruction_thresholds": RECONSTRUCTION_THRESHOLDS,
        "fragmentation_thresholds": FRAGMENTATION_THRESHOLDS,
        "dialogue_thresholds": DIALOGUE_THRESHOLDS,
        "turn_length_thresholds": TURN_LENGTH_THRESHOLDS,
        "uuid_canonicalization": {
            "uuid": UUID_RE.pattern,
            "date_prefixed_uuid": DATE_PREFIXED_UUID_RE.pattern,
        },
        "jsonl_line_separators_scrubbed": ["\u0085", "\u2028", "\u2029"],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

"""Regex secret + SpecStory-style email/path redaction with hit counts."""
from __future__ import annotations

import re
import sys
from collections import Counter
from typing import Iterable

# Prefer Harbor's canonical secret patterns from cohort_policy when available.
sys.path.insert(0, "/data/claude-crawl")
try:
    from cohort_policy import SECRET_PATTERNS as _COHORT_SECRET_PATTERNS
except Exception:  # pragma: no cover
    _COHORT_SECRET_PATTERNS = ()

# SpecStory-style PII (email + home paths). Keep placeholders stable.
PII_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "email",
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "<REDACTED_EMAIL>",
    ),
    (
        "home_unix",
        # Skip already-redacted <USER> placeholders (idempotent).
        re.compile(r"/(?:home|Users)/(?!<USER>(?:/|$))([A-Za-z0-9._-]+)"),
        "/home/<USER>",
    ),
    (
        "home_win",
        re.compile(r"[Cc]:\\Users\\(?!<USER>(?:\\|$))([A-Za-z0-9._ -]+)"),
        # Callable avoids re.sub \\U unicode-escape errors in replacement templates.
        lambda m: "C:\\Users\\<USER>",
    ),
]


def _secret_named_patterns() -> list[tuple[str, re.Pattern[str], str]]:
    out: list[tuple[str, re.Pattern[str], str]] = []
    for idx, (pattern, replacement) in enumerate(_COHORT_SECRET_PATTERNS):
        name = f"secret_{idx}"
        # Best-effort names from replacement tags.
        if isinstance(replacement, str):
            m = re.search(r"REDACTED[_ ]?([A-Z0-9_]+)", replacement)
            if m:
                name = f"secret_{m.group(1).lower()}"
        out.append((name, pattern, replacement))
    if out:
        return out
    # Fallback mirror of cohort_policy SECRET_PATTERNS if import fails.
    return [
        ("secret_sk", re.compile(r"sk-[A-Za-z0-9_-]{16,}"), "[REDACTED_SK]"),
        ("secret_gh_pat", re.compile(r"ghp_[A-Za-z0-9]{20,}"), "[REDACTED_GH_PAT]"),
        ("secret_gho", re.compile(r"gho_[A-Za-z0-9]{20,}"), "[REDACTED_GH]"),
        (
            "secret_github_pat",
            re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
            "[REDACTED_GH_PAT]",
        ),
        ("secret_aws", re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED_AWS_KEY]"),
        ("secret_google", re.compile(r"AIza[0-9A-Za-z_-]{30,}"), "[REDACTED_GOOGLE_KEY]"),
        ("secret_slack", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "[REDACTED_SLACK]"),
        (
            "secret_bearer",
            re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"),
            "bearer [REDACTED]",
        ),
        (
            "secret_private_key",
            re.compile(
                r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?"
                r"-----END [A-Z ]*PRIVATE KEY-----"
            ),
            "[REDACTED_PRIVATE_KEY]",
        ),
        (
            "secret_kv",
            re.compile(
                r'(?i)(api[_-]?key|secret|token|password)["\'`]?\s*[:=]\s*'
                r'["\'`]?([A-Za-z0-9_-]{16,})'
            ),
            r"\1=[REDACTED]",
        ),
    ]


def all_regex_patterns():
    named = _secret_named_patterns()
    # cohort_policy SECRET_PATTERNS may already include SpecStory email/path
    # patterns — avoid double-application (still idempotent, but inflates counts).
    joined = " ".join(p.pattern for _, p, _ in named)
    if "@" in joined and "home|Users" in joined:
        return named
    return named + list(PII_PATTERNS)


def scrub_regex(text: str, patterns=None):
    """Apply regex redactions. Returns (new_text, Counter of hits by name)."""
    value = text or ""
    # JSONL-safe: collapse Unicode line/paragraph separators.
    value = value.replace("\u0085", " ").replace("\u2028", " ").replace("\u2029", " ")
    hits: Counter[str] = Counter()
    for name, pattern, replacement in patterns or all_regex_patterns():
        value, n = pattern.subn(replacement, value)
        if n:
            hits[name] += n
    return value, hits

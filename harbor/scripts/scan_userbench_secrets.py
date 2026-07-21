#!/usr/bin/env python3
"""Scan UserBench package trees without printing secret values."""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

ENV_NAMES = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "CURSOR_API_KEY",
    "HARBOR_API_KEY",
    "OPENROUTER_API_KEY",
)
STRONG_PATTERNS = (
    (b"sk-", re.compile(rb"sk-[A-Za-z0-9_-]{20,}")),
    (b"ghp_", re.compile(rb"ghp_[A-Za-z0-9]{20,}")),
    (b"gho_", re.compile(rb"gho_[A-Za-z0-9]{20,}")),
    (
        b"github_pat_",
        re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    ),
    (b"AKIA", re.compile(rb"AKIA[0-9A-Z]{16}")),
    (b"AIza", re.compile(rb"AIza[0-9A-Za-z_-]{30,}")),
    (b"xox", re.compile(rb"xox[baprs]-[A-Za-z0-9-]{10,}")),
)
ASSIGNMENT_PATTERN = re.compile(
    rb"(?i)(?:api[_-]?key|secret|token|password)"
    rb"[\"'`]?\s*[:=]\s*[\"'`]?[A-Za-z0-9_-]{16,}"
)
ASSIGNMENT_NEEDLES = (
    b"api_key",
    b"API_KEY",
    b"api-key",
    b"API-KEY",
    b"secret",
    b"SECRET",
    b"token",
    b"TOKEN",
    b"password",
    b"PASSWORD",
)
BEARER_PATTERN = re.compile(rb"Bearer\s+([A-Za-z0-9._-]{20,})")
PLACEHOLDER_WORDS = (
    b"example",
    b"dummy",
    b"placeholder",
    b"redacted",
    b"sample",
    b"token",
    b"your",
    b"xxxx",
)
PRIVATE_HEADERS = (
    b"PRIVATE KEY",
    b"RSA PRIVATE KEY",
    b"EC PRIVATE KEY",
    b"OPENSSH PRIVATE KEY",
)


def matches_near(
    data: bytes,
    needle: bytes,
    pattern: re.Pattern[bytes],
    window: int = 512,
) -> bool:
    start = 0
    while (index := data.find(needle, start)) >= 0:
        if pattern.search(data[index : index + window]):
            return True
        start = index + len(needle)
    return False


def looks_like_placeholder(value: bytes) -> bool:
    lowered = value.lower()
    return any(word in lowered for word in PLACEHOLDER_WORDS)


def has_bearer_secret(data: bytes) -> bool:
    if b"Bearer " not in data:
        return False
    return any(
        not looks_like_placeholder(match.group(1))
        for match in BEARER_PATTERN.finditer(data)
    )


def has_private_key(data: bytes) -> bool:
    for label in PRIVATE_HEADERS:
        begin = b"-----BEGIN " + label + b"-----"
        end = b"-----END " + label + b"-----"
        start = data.find(begin)
        while start >= 0:
            stop = data.find(end, start + len(begin))
            if stop >= 0:
                body = re.sub(
                    rb"\s+",
                    b"",
                    data[start + len(begin) : stop],
                )
                if len(body) >= 100:
                    return True
            start = data.find(begin, start + len(begin))
    return False


def scan_file(path: Path, exact_values: dict[str, bytes]) -> set[str]:
    try:
        data = path.read_bytes()
    except (OSError, PermissionError):
        return set()
    kinds = {
        f"exact-{name}"
        for name, value in exact_values.items()
        if value in data
    }
    if any(
        matches_near(data, prefix, pattern)
        for prefix, pattern in STRONG_PATTERNS
    ):
        kinds.add("secret-pattern")
    if has_private_key(data):
        kinds.add("private-key")
    if has_bearer_secret(data):
        kinds.add("bearer-token")
    if any(
        matches_near(data, needle, ASSIGNMENT_PATTERN)
        for needle in ASSIGNMENT_NEEDLES
    ):
        kinds.add("secret-pattern")
    return kinds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    exact_values = {
        name: value.encode()
        for name in ENV_NAMES
        if len(value := os.environ.get(name, "").strip()) >= 12
    }
    scanned_files = 0
    scanned_bytes = 0
    findings: list[tuple[Path, set[str]]] = []
    for root in args.roots:
        if not root.exists():
            raise SystemExit(f"missing scan root: {root}")
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            scanned_files += 1
            try:
                scanned_bytes += path.stat().st_size
            except OSError:
                pass
            if kinds := scan_file(path, exact_values):
                findings.append((path, kinds))

    print(
        f"secret_scan files={scanned_files} bytes={scanned_bytes} "
        f"findings={len(findings)}"
    )
    counts: dict[str, int] = {}
    for _, kinds in findings:
        for kind in kinds:
            counts[kind] = counts.get(kind, 0) + 1
    print(f"finding_kinds={counts}")
    if args.verbose:
        for path, kinds in findings:
            print(f"finding: {','.join(sorted(kinds))} {path}")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

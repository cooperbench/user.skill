"""Code-block guard: never redact spans inside fenced code or inline backticks.

Ported from SWE-chat-private release/pii_redaction/redact_PII.py.
"""
from __future__ import annotations

import re

_FENCED = re.compile(r"```.*?```", re.DOTALL)
_INLINE = re.compile(r"`[^`\n]+`")


def code_spans(text: str) -> list[tuple[int, int]]:
    spans = [(m.start(), m.end()) for m in _FENCED.finditer(text)]
    spans += [(m.start(), m.end()) for m in _INLINE.finditer(text)]
    spans.sort()
    return spans


def in_code(start: int, end: int, spans: list[tuple[int, int]]) -> bool:
    for s, e in spans:
        if start >= s and end <= e:
            return True
        if start >= e:
            continue
        if end <= s:
            break
    return False

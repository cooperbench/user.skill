"""Unified scrub pipeline: regex → Presidio (NL) → TruffleHog findings."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from .presidio_engine import redact as presidio_redact
from .regex_scrub import scrub_regex
from .trufflehog import redact_with_findings

NL_ROLES = frozenset(
    {
        "user",
        "assistant",
        "developer",
        "agent",
        "DEVELOPER",
        "AGENT",
    }
)


@dataclass
class ScrubStats:
    regex: Counter = field(default_factory=Counter)
    presidio: Counter = field(default_factory=Counter)
    trufflehog: Counter = field(default_factory=Counter)
    texts_seen: int = 0
    texts_changed: int = 0
    nl_texts: int = 0

    def update(self, other: "ScrubStats") -> None:
        self.regex.update(other.regex)
        self.presidio.update(other.presidio)
        self.trufflehog.update(other.trufflehog)
        self.texts_seen += other.texts_seen
        self.texts_changed += other.texts_changed
        self.nl_texts += other.nl_texts

    def as_dict(self) -> dict[str, Any]:
        return {
            "texts_seen": self.texts_seen,
            "texts_changed": self.texts_changed,
            "nl_texts": self.nl_texts,
            "regex": dict(self.regex.most_common()),
            "presidio": dict(self.presidio.most_common()),
            "trufflehog": dict(self.trufflehog.most_common()),
            "total_redactions": (
                sum(self.regex.values())
                + sum(self.presidio.values())
                + sum(self.trufflehog.values())
            ),
        }


class ScrubPipeline:
    """Reusable scrubber for Harbor + cohort text.

    Parameters
    ----------
    enable_presidio:
        Run NER PII redaction on natural-language roles.
    enable_trufflehog_findings:
        Apply a precomputed ``findings`` map (from a global TruffleHog scan).
    document_freq:
        Optional Joe-style document frequencies for Presidio thresholds.
    """

    def __init__(
        self,
        *,
        enable_presidio: bool = True,
        enable_trufflehog_findings: bool = True,
        document_freq: dict | None = None,
        model_name: str = "en_core_web_sm",
        trufflehog_findings: dict[str, str] | None = None,
    ):
        self.enable_presidio = enable_presidio
        self.enable_trufflehog_findings = enable_trufflehog_findings
        self.document_freq = document_freq
        self.model_name = model_name
        self.trufflehog_findings = trufflehog_findings or {}
        self.stats = ScrubStats()

    def set_trufflehog_findings(self, findings: dict[str, str]) -> None:
        self.trufflehog_findings = findings or {}

    def scrub(
        self,
        text: str,
        *,
        role: str | None = None,
        apply_presidio: bool | None = None,
    ) -> str:
        """Scrub one text blob. ``role`` gates Presidio (NL roles only)."""
        original = text or ""
        self.stats.texts_seen += 1
        value, rh = scrub_regex(original)
        self.stats.regex.update(rh)

        do_presidio = self.enable_presidio if apply_presidio is None else apply_presidio
        if do_presidio and (role is None or role in NL_ROLES):
            self.stats.nl_texts += 1
            # Skip tiny / non-prose blobs — Presidio cost dominates and Joe's
            # PERSON validator already requires multi-word name hooks.
            if len(value) >= 40 and not value.lstrip().startswith("tool_"):
                value, ph = presidio_redact(
                    value,
                    document_freq=self.document_freq,
                    model_name=self.model_name,
                )
                self.stats.presidio.update(ph)

        if self.enable_trufflehog_findings and self.trufflehog_findings:
            value, th = redact_with_findings(value, self.trufflehog_findings)
            self.stats.trufflehog.update(th)

        if value != original:
            self.stats.texts_changed += 1
        return value

    def scrub_all_roles(self, text: str) -> str:
        """Regex + TruffleHog on any text; no Presidio (for tool/system/global)."""
        return self.scrub(text, apply_presidio=False)

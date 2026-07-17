#!/usr/bin/env python3
"""Verify scrub idempotency + residual email/path/secret pattern rates.

Does NOT print secret values — only counts and placeholder presence.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/data/swesimbench-v2-harbor")
sys.path.insert(0, str(ROOT))

from pii_redaction.pipeline import ScrubPipeline  # noqa: E402
from pii_redaction.regex_scrub import scrub_regex  # noqa: E402

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
HOME_RE = re.compile(r"/(?:home|Users)/(?!<USER>(?:/|$))([A-Za-z0-9._-]+)")
SK_RE = re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}\b")
PLACEHOLDER_RE = re.compile(
    r"<(?:REDACTED_EMAIL|PRESIDIO_ANONYMIZED_[A-Z_]+|TRUFFLEHOG_REDACTED_[A-Z0-9_]+)>|\[REDACTED_[A-Z_]+\]|/home/<USER>"
)


def scan_text(text: str, hits: Counter) -> None:
    hits["email_residual"] += len(EMAIL_RE.findall(text))
    hits["home_residual"] += len(HOME_RE.findall(text))
    hits["sk_residual"] += len(SK_RE.findall(text))
    hits["placeholders"] += len(PLACEHOLDER_RE.findall(text))


def second_pass_delta(text: str, role: str | None = None) -> int:
    """Return number of regex hits on a second scrub pass (should be ~0)."""
    pipe = ScrubPipeline(
        enable_presidio=False,
        enable_trufflehog_findings=False,
    )
    before = text
    after = pipe.scrub(before, role=role or "user", apply_presidio=False)
    # Count regex-only residual via scrub_regex on already-scrubbed text.
    _, hits = scrub_regex(after)
    return sum(hits.values()) + (1 if after != before else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path, default=ROOT / "meta" / "pii_scrub_verify.json")
    ap.add_argument("--sample-sessions", type=int, default=300)
    args = ap.parse_args()

    report: dict = {"checks": {}}

    # --- clean_sessions sample ---
    sess_path = ROOT / "clean_sessions.jsonl"
    sess_hits: Counter = Counter()
    second_pass = 0
    n = 0
    if sess_path.exists():
        with sess_path.open() as f:
            for line in f:
                n += 1
                if n > args.sample_sessions:
                    break
                rec = json.loads(line)
                for turn in rec.get("turns") or []:
                    text = turn.get("text") or ""
                    scan_text(text, sess_hits)
                    second_pass += second_pass_delta(text, turn.get("role"))
        report["checks"]["clean_sessions_sample"] = {
            "sessions": min(n, args.sample_sessions),
            "residuals": dict(sess_hits),
            "second_pass_hits": second_pass,
        }

    # --- eval histories ---
    eval_hits: Counter = Counter()
    n_hist = 0
    second_pass_hist = 0
    for hist in (ROOT / "datasets" / "eval").glob("*/environment/history.md"):
        n_hist += 1
        text = hist.read_text(encoding="utf-8", errors="replace")
        scan_text(text, eval_hits)
        second_pass_hist += second_pass_delta(text)
    report["checks"]["eval_histories"] = {
        "files": n_hist,
        "residuals": dict(eval_hits),
        "second_pass_hits": second_pass_hist,
    }

    # --- v2tasks ---
    v2_hits: Counter = Counter()
    n_v2 = 0
    for instr in (ROOT / "v2tasks" / "inline").glob("t*/instruction.md"):
        n_v2 += 1
        scan_text(instr.read_text(encoding="utf-8", errors="replace"), v2_hits)
    report["checks"]["v2tasks_instruction"] = {
        "files": n_v2,
        "residuals": dict(v2_hits),
    }

    # Pass criteria (soft): home/email residual near zero; second pass ~0
    ok = (
        eval_hits.get("email_residual", 0) == 0
        and eval_hits.get("home_residual", 0) == 0
        and second_pass_hist == 0
        and sess_hits.get("email_residual", 0) == 0
        and sess_hits.get("home_residual", 0) == 0
        and second_pass == 0
    )
    report["ok"] = ok
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not ok:
        sys.exit(2)


if __name__ == "__main__":
    main()

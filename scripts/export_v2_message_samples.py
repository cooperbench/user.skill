#!/usr/bin/env python3
"""Export public message samples for the SWESimBench website.

For each developer in the authoritative clean v2 cohort, sample 10 random
user messages with a small surrounding turn window. Applies light secret
redaction and truncation so the file is safe to ship with the static site.

Reads: .private/v2-58/clean_sessions.jsonl + .private/indexes/v2_users.txt
Writes: web/app/v2_samples.json
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / ".private" / "v2-58"
USERS = ROOT / ".private" / "indexes" / "v2_users.txt"
OUT = ROOT / "web" / "app" / "v2_samples.json"

N_PER_USER = 10
CONTEXT_BEFORE = 2
CONTEXT_AFTER = 2
MAX_TURN_CHARS = 1800
SEED = 20260713

# Light public-site redaction — not a full secrets scanner.
SECRET_RES = [
    re.compile(r"(?i)\b(sk-|rk-|pk-|api[_-]?key\s*[:=]\s*)[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)\b(ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)\b(xox[baprs]-)[A-Za-z0-9-]{10,}"),
    re.compile(r"(?i)\b(Bearer\s+)[A-Za-z0-9\-._~+/]+=*"),
    re.compile(r"(?i)\b(AWS|AKIA)[A-Z0-9]{16,}"),
    re.compile(r"(?i)\b(-----BEGIN(?: RSA| OPENSSH| EC)? PRIVATE KEY-----)[\s\S]+?(-----END(?: RSA| OPENSSH| EC)? PRIVATE KEY-----)"),
    re.compile(r"(?i)\b(password|passwd|secret|token)\s*[:=]\s*\S{8,}"),
]


def redact(text: str) -> str:
    out = text
    for rx in SECRET_RES:
        out = rx.sub(lambda m: (m.group(1) if m.lastindex else "") + "[REDACTED]", out)
    return out


def clip(text: str, n: int = MAX_TURN_CHARS) -> tuple[str, bool]:
    text = text.replace("\x00", "")
    if len(text) <= n:
        return text, False
    return text[:n].rstrip() + "…", True


def eligible_user_turn(text: str) -> bool:
    t = (text or "").strip()
    if len(t) < 2:
        return False
    # Skip pure slash-commands / empty interrupt markers when tiny.
    if t.startswith("[") and len(t) < 8:
        return False
    return True


def main() -> None:
    users = [ln.strip() for ln in USERS.read_text().splitlines() if ln.strip()]
    candidates: dict[str, list[dict]] = {u: [] for u in users}

    with (PRIVATE / "clean_sessions.jsonl").open() as f:
        for line in f:
            row = json.loads(line)
            user = row.get("user")
            if user not in candidates:
                continue
            turns = row.get("turns") or []
            if not turns:
                continue
            for i, turn in enumerate(turns):
                if turn.get("role") != "user":
                    continue
                text = turn.get("text") or ""
                if not eligible_user_turn(text):
                    continue
                lo = max(0, i - CONTEXT_BEFORE)
                hi = min(len(turns), i + CONTEXT_AFTER + 1)
                window = []
                for j in range(lo, hi):
                    raw = turns[j].get("text") or ""
                    clipped, was_clipped = clip(redact(raw))
                    window.append(
                        {
                            "role": turns[j].get("role") or "unknown",
                            "text": clipped,
                            "clipped": was_clipped,
                            "focal": j == i,
                        }
                    )
                candidates[user].append(
                    {
                        "session_id": row.get("session_id"),
                        "repo": row.get("repo") or "?",
                        "source": row.get("source") or "?",
                        "start_time": (row.get("start_time") or "")[:10] or None,
                        "turn_index": i,
                        "n_turns": len(turns),
                        "window": window,
                    }
                )

    rng = random.Random(SEED)
    developers = []
    total = 0
    for user in users:
        pool = candidates[user]
        if not pool:
            developers.append({"user": user, "n_available": 0, "samples": []})
            continue
        k = min(N_PER_USER, len(pool))
        # Stable shuffle per user.
        user_rng = random.Random(int(hashlib.sha256(f"{SEED}:{user}".encode()).hexdigest()[:16], 16))
        picked = user_rng.sample(pool, k)
        # Sort by session/time for nicer reading order.
        picked.sort(key=lambda s: (s.get("start_time") or "", s["session_id"], s["turn_index"]))
        developers.append(
            {
                "user": user,
                "n_available": len(pool),
                "samples": picked,
            }
        )
        total += len(picked)

    out = {
        "dataset": "SWESimBench v2 harbor cohort — public message samples",
        "policy_version": "swesimbench-v2-cohort-policy-2026-07-13.8",
        "n_developers": len(developers),
        "n_samples_per_developer": N_PER_USER,
        "n_samples_total": total,
        "context_before": CONTEXT_BEFORE,
        "context_after": CONTEXT_AFTER,
        "seed": SEED,
        "note": (
            "Ten randomly sampled user messages per retained developer, each with "
            f"±{CONTEXT_BEFORE}/+{CONTEXT_AFTER} surrounding turns. Texts are lightly "
            "redacted and truncated for the public site; this is not the full private corpus."
        ),
        "developers": developers,
    }

    blob = json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n"
    # Refuse obvious private markers that shouldn't ship.
    for bad in ("BEGIN RSA PRIVATE KEY", "AWS_SECRET_ACCESS_KEY=", "OPENROUTER_API_KEY="):
        if bad in blob:
            raise SystemExit(f"refusing to publish: found {bad!r}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(blob)
    empty = sum(1 for d in developers if not d["samples"])
    print(
        f"wrote {OUT} ({OUT.stat().st_size} bytes) "
        f"developers={len(developers)} samples={total} empty={empty}"
    )


if __name__ == "__main__":
    main()

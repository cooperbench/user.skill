#!/usr/bin/env python3
"""Export public-safe SWESimBench v2 cohort aggregates for the website.

Reads hydrated private manifests under .private/ and writes
web/public/data/v2_cohort.json. Never includes session text, profiles,
or other private corpus fields.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / ".private"
OUT = ROOT / "web" / "public" / "data" / "v2_cohort.json"

FORBIDDEN_SUBSTRINGS = (
    "prev_agent",
    '"context"',
    "USER.md",
    "megaplan",
    "real_text",
)


def main() -> None:
    meta = json.loads((PRIVATE / "v2-58" / "cohort.meta.json").read_text())
    cohort = json.loads((PRIVATE / "v2-58" / "cohort.json").read_text())
    manifest = json.loads((PRIVATE / "indexes" / "DATA_MANIFEST.json").read_text())
    build = json.loads((PRIVATE / "v2-58" / "clean_build_report.json").read_text())

    sources: Counter[str] = Counter()
    users = []
    for row in cohort:
        uid = row["user"]
        sources[uid.split(":", 1)[0]] += 1
        users.append(
            {
                "user": uid,
                "train_turns": row.get("train_turns"),
                "held_turns": row.get("held_turns"),
                "n_points": len(row.get("points") or []),
            }
        )

    safe_build = {
        k: build[k]
        for k in (
            "policy_version",
            "policy_fingerprint",
            "cohort_fingerprint",
            "source_manifest_users",
            "excluded_users",
            "retained_users",
            "dropped_below_clean_threshold",
            "source_manifest_sessions",
            "clean_sessions",
            "dedup_events",
            "cross_split_dedup_events",
        )
        if k in build
    }

    out = {
        "dataset": "SWESimBench v2 harbor cohort",
        "policy_version": meta["policy_version"],
        "policy_fingerprint": meta["policy_fingerprint"],
        "cohort_fingerprint": meta["cohort_fingerprint"],
        "developers": meta["developers"],
        "points": meta["points"],
        "sources": dict(sources),
        "note": (
            "Authoritative v2 cohort is 57 developers (plan said 58). "
            "Aggregate metadata only; session text and distilled personas are private."
        ),
        "related_eval": {
            "name": "CondAgree next-action prediction accuracy (published leaderboard)",
            "status": "still the June 2026 SWE-chat 20-developer / 480-moment split",
            "path": "bench/profileopt/experiments/condagree_multi",
        },
        "build": safe_build,
        "users": users,
        "created_from": {
            "manifest_created_at": manifest.get("created_at"),
            "s3_prefix": "derived/v2-58/",
        },
    }

    blob = json.dumps(out, indent=1) + "\n"
    for bad in FORBIDDEN_SUBSTRINGS:
        if bad in blob:
            raise SystemExit(f"refusing to publish: found private-looking substring {bad!r}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(blob)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {len(users)} users)")


if __name__ == "__main__":
    main()

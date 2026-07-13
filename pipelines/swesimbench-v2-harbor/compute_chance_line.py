#!/usr/bin/env python3
"""Compute the move-majority chance line for the current labeled cohort."""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/data/swesimbench-v2-harbor")
meta = json.loads((ROOT / "cohort.meta.json").read_text())
clean = json.loads((ROOT / "clean_manifest.json").read_text())
assert meta["policy_fingerprint"] == clean["policy_fingerprint"]
assert meta["cohort_fingerprint"] == clean["cohort_fingerprint"]

cohort = json.loads((ROOT / "cohort.json").read_text())
labels = [
    point.get("gold_move")
    for developer in cohort
    for point in developer["points"]
]
missing = sum(label is None for label in labels)
if missing:
    raise RuntimeError(
        f"{missing}/{len(labels)} points lack gold_move; run prepare.py with RUN_GOLD=1"
    )

counts = Counter(labels)
majority_move, majority_count = counts.most_common(1)[0]
per_developer = {}
for developer in cohort:
    developer_counts = Counter(point["gold_move"] for point in developer["points"])
    total = sum(developer_counts.values())
    per_developer[developer["user"]] = {
        "points": total,
        "move_counts": dict(developer_counts),
        "majority_accuracy": max(developer_counts.values()) / total if total else None,
    }

report = {
    "policy_version": meta["policy_version"],
    "policy_fingerprint": meta["policy_fingerprint"],
    "cohort_fingerprint": meta["cohort_fingerprint"],
    "points": len(labels),
    "developers": len(cohort),
    "move_counts": dict(counts),
    "micro_majority_move": majority_move,
    "micro_chance_line": majority_count / len(labels),
    "macro_developer_chance_line": sum(
        item["majority_accuracy"] for item in per_developer.values()
        if item["majority_accuracy"] is not None
    ) / len(per_developer),
    "per_developer": per_developer,
}
(ROOT / "chance_line.json").write_text(json.dumps(report, indent=2))
print(json.dumps({key: value for key, value in report.items() if key != "per_developer"}, indent=2))

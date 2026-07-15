#!/usr/bin/env python3
"""Hard integrity assertions for rebuilt SWESimBench v2 artifacts."""
import json
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, "/data/claude-crawl")
from cohort_policy import (
    EXCLUDED_USERS,
    POLICY_VERSION,
    is_human_target,
    is_incomplete_dialogue,
    normalize_text,
    policy_fingerprint,
    scrub_text,
)
from build_clean_cohort import (
    reconstruction_candidate_pairs,
    record_reconstruction_evidence,
)

ROOT = Path("/data/swesimbench-v2-harbor")
manifest = json.loads((ROOT / "clean_manifest.json").read_text())
assert manifest["policy_version"] == POLICY_VERSION
assert manifest["policy_fingerprint"] == policy_fingerprint()
report = json.loads((ROOT / "clean_build_report.json").read_text())
command_payload_hashes = set(report.get("command_expansion_payload_hashes", []))

sessions = {}
with (ROOT / "clean_sessions.jsonl").open(encoding="utf-8") as handle:
    for line in handle:
        if not line.strip():
            continue
        session = json.loads(line)
        sid = session["session_id"]
        assert sid not in sessions, f"duplicate canonical session: {sid}"
        assert session["user"] not in EXCLUDED_USERS
        for turn in session["turns"]:
            assert turn["role"] in {"user", "assistant", "system", "tool", "metadata"}
            assert scrub_text(turn.get("text") or "") == (turn.get("text") or ""), (
                f"unscrubbed secret-like content in {sid}"
            )
            if turn["role"] == "user":
                assert is_human_target(turn), f"injected/placeholder user turn in {sid}"
                payload_hash = hashlib.sha256(
                    normalize_text(turn.get("text") or "").encode()
                ).hexdigest()
                assert payload_hash not in command_payload_hashes, (
                    f"command expansion remains a user target in {sid}"
                )
        assert not is_incomplete_dialogue(session["turns"]), (
            f"incomplete dialogue retained in clean cohort: {sid}"
        )
        sessions[sid] = session

seen = set()
original_id_owner = {}
session_split = {}
for user in manifest["users"]:
    assert user["user"] not in EXCLUDED_USERS
    train = user["train_sessions"]
    held = user["held_sessions"]
    train_ids = {session["sid"] for session in train}
    held_ids = {session["sid"] for session in held}
    assert train_ids.isdisjoint(held_ids), f"split overlap: {user['user']}"
    assert train_ids | held_ids <= sessions.keys(), f"missing session: {user['user']}"
    assert max(session["ts"] for session in train) < min(session["ts"] for session in held)
    assert user["train_turns"] >= 400
    assert user["held_turns"] >= 100
    user_records = [sessions[sid] for sid in sorted(train_ids | held_ids)]
    reconstructed_pairs = [
        (user_records[left]["session_id"], user_records[right]["session_id"])
        for left, right in reconstruction_candidate_pairs(user_records)
        if record_reconstruction_evidence(
            user_records[left], user_records[right]
        )
        is not None
    ]
    assert not reconstructed_pairs, (
        f"reconstructed-session duplicates remain for {user['user']}: "
        f"{reconstructed_pairs[:10]}"
    )
    for sid in train_ids | held_ids:
        assert sid not in seen, f"cross-user session collision: {sid}"
        seen.add(sid)
        session_split[sid] = "train" if sid in train_ids else "held"
        for original_id in sessions[sid]["original_ids"]:
            previous = original_id_owner.setdefault(original_id, sid)
            assert previous == sid, (
                f"source session {original_id} retained by both {previous} and {sid}"
            )

assert seen == sessions.keys(), "session store and manifest differ"
assert report["clean_sessions"] == len(sessions)
assert report["retained_users"] == len(manifest["users"])
for event in report["provenance"]:
    if (
        event["rule"] == "reconstructed_session"
        and event.get("crossed_split")
        and event["kept"] in session_split
    ):
        assert session_split.get(event["kept"]) == "train", (
            f"cross-split reconstruction was not conservatively assigned to train: "
            f"{event['kept']}"
        )

cohort_path = ROOT / "cohort.json"
if cohort_path.exists() and (ROOT / "cohort.meta.json").exists():
    cohort_meta = json.loads((ROOT / "cohort.meta.json").read_text())
    if cohort_meta.get("cohort_fingerprint") == manifest["cohort_fingerprint"]:
        cohort = json.loads(cohort_path.read_text())
        assert {record["user"] for record in cohort} == {
            record["user"] for record in manifest["users"]
        }
        for record in cohort:
            for point in record["points"]:
                sid, turn_index = point["point_id"].rsplit("#", 1)
                turn = sessions[sid]["turns"][int(turn_index)]
                assert turn["role"] == "user" and is_human_target(turn)
                assert scrub_text(point["real"]) == point["real"]
                assert scrub_text(point["context"]) == point["context"]

        cohort_points = {
            (record["user"], point["point_id"])
            for record in cohort
            for point in record["points"]
        }
        dataset_point_sets = {}
        stale_datasets = []
        for dataset_name, condition in (("eval", "noprofile"),):
            dataset = ROOT / "datasets" / dataset_name
            if not dataset.exists():
                continue
            dataset_meta = json.loads((dataset / "_cohort_meta.json").read_text())
            if (
                dataset_meta.get("policy_fingerprint") != manifest["policy_fingerprint"]
                or dataset_meta.get("cohort_fingerprint")
                != manifest["cohort_fingerprint"]
            ):
                stale_datasets.append(dataset_name)
                continue
            assert dataset_meta["condition"] == condition
            tasks = json.loads((dataset / "_manifest.json").read_text())
            points = {(task["dev"], task["point_id"]) for task in tasks}
            assert points == cohort_points
            assert len(tasks) == len(points)
            dataset_point_sets[dataset_name] = points
            for task in tasks:
                task_root = dataset / task["task"]
                gold = json.loads((task_root / "tests" / "gold.json").read_text())
                assert gold["developer"] == task["dev"]
                assert gold["point_id"] == task["point_id"]
                # Profiles are Harbor skills on the agent harness, never task payload.
                assert not (task_root / "environment" / "sim" / "profile.md").exists()
        if stale_datasets:
            print(
                "skipping stale derived datasets (rebuild make_tasks): "
                + ", ".join(stale_datasets)
            )
        assert "withprofile-full" not in {
            p.name for p in (ROOT / "datasets").iterdir() if p.is_dir()
        }, "withprofile task twin must not exist; inject profiles via Harbor skills"
sample_meta_path = ROOT / "sample100" / "meta.json"
if sample_meta_path.exists():
    sample_meta = json.loads(sample_meta_path.read_text())
    if sample_meta.get("cohort_fingerprint") == manifest["cohort_fingerprint"]:
        assert sample_meta["policy_fingerprint"] == manifest["policy_fingerprint"]
        sample_points = [
            json.loads(line)
            for line in (ROOT / "sample100" / "points.jsonl").read_text().splitlines()
        ]
        assert len(sample_points) == sample_meta["points"] == 100
        assert all(point["gold_move"] is None for point in sample_points)

print(
    json.dumps(
        {
            "policy_version": POLICY_VERSION,
            "developers": len(manifest["users"]),
            "sessions": len(sessions),
            "status": "clean",
        },
        indent=2,
    )
)

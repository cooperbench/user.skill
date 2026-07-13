#!/usr/bin/env python3
"""Select deterministic train/held session comparisons for manual QC."""
import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "/data/claude-crawl")
from cohort_policy import is_human_target, normalize_text
from build_clean_cohort import record_reconstruction_evidence

ROOT = Path("/data/swesimbench-v2-harbor")
OUT = ROOT / "session_comparison_sample.json"
N_DEVELOPERS = 10
MAX_MATCHES = 3
CONTEXT_RADIUS = 2
TEXT_CAP = 1200


def normalized_user_messages(turns):
    result = defaultdict(list)
    for index, turn in enumerate(turns):
        if turn.get("role") != "user" or not is_human_target(turn):
            continue
        normalized = normalize_text(turn.get("text") or "").lower()
        if len(normalized) >= 24:
            result[normalized].append(index)
    return result


def excerpt(turns, centers):
    indices = sorted(
        {
            index
            for center in centers
            for index in range(
                max(0, center - CONTEXT_RADIUS),
                min(len(turns), center + CONTEXT_RADIUS + 1),
            )
        }
    )
    return [
        {
            "index": index,
            "role": turns[index].get("role") or "metadata",
            "text": (
                (turns[index].get("text") or "")[:TEXT_CAP]
                + (
                    " […truncated]"
                    if len(turns[index].get("text") or "") > TEXT_CAP
                    else ""
                )
            ),
            "matched": index in centers,
        }
        for index in indices
    ]


manifest = json.loads((ROOT / "clean_manifest.json").read_text())
session_owner = {
    session["sid"]: user["user"]
    for user in manifest["users"]
    for split in ("train_sessions", "held_sessions")
    for session in user[split]
}
sessions = {}
with (ROOT / "clean_sessions.jsonl").open() as handle:
    for line in handle:
        session = json.loads(line)
        if session["session_id"] in session_owner:
            sessions[session["session_id"]] = session

ranked = []
per_user = {}
for user in manifest["users"]:
    train = [sessions[item["sid"]] for item in user["train_sessions"]]
    held = [sessions[item["sid"]] for item in user["held_sessions"]]
    train_maps = {
        session["session_id"]: normalized_user_messages(session["turns"])
        for session in train
    }
    held_maps = {
        session["session_id"]: normalized_user_messages(session["turns"])
        for session in held
    }
    train_population = set().union(*(mapping.keys() for mapping in train_maps.values()))
    held_population = set().union(*(mapping.keys() for mapping in held_maps.values()))
    overlap = train_population & held_population
    overlap_held = [
        session for session in held if set(held_maps[session["session_id"]]) & overlap
    ]
    if not overlap_held:
        continue
    per_user[user["user"]] = (train, overlap_held, train_maps, held_maps, overlap)
    ranked.append((len(overlap), sum(len(text) for text in overlap), user["user"]))

selected_users = [
    user for _, _, user in sorted(ranked, reverse=True)[:N_DEVELOPERS]
]
comparisons = []
for developer in selected_users:
    train, overlap_held, train_maps, held_maps, overlap = per_user[developer]
    seed = int(
        hashlib.sha256(
            f"{manifest['cohort_fingerprint']}:{developer}".encode()
        ).hexdigest()[:16],
        16,
    )
    held_session = random.Random(seed).choice(
        sorted(overlap_held, key=lambda session: session["session_id"])
    )
    held_map = held_maps[held_session["session_id"]]

    candidates = []
    for train_session in train:
        train_map = train_maps[train_session["session_id"]]
        shared = set(held_map) & set(train_map)
        if not shared:
            continue
        candidates.append(
            (
                len(shared),
                sum(len(text) for text in shared),
                train_session["session_id"],
                train_session,
                train_map,
                shared,
            )
        )
    _, _, _, train_session, train_map, shared = max(candidates)
    chosen_matches = sorted(shared, key=lambda text: (-len(text), text))[:MAX_MATCHES]
    match_records = []
    train_centers = []
    held_centers = []
    for text in chosen_matches:
        train_index = train_map[text][0]
        held_index = held_map[text][0]
        train_centers.append(train_index)
        held_centers.append(held_index)
        match_records.append(
            {
                "text": text,
                "train_turn": train_index,
                "held_turn": held_index,
                "train_timestamp": train_session["turns"][train_index].get("ts"),
                "held_timestamp": held_session["turns"][held_index].get("ts"),
            }
        )
    reconstruction_evidence = record_reconstruction_evidence(
        train_session, held_session
    )
    comparisons.append(
        {
            "developer": developer,
            "developer_overlap_messages": len(overlap),
            "pair_overlap_messages": len(shared),
            "reconstruction_match": reconstruction_evidence is not None,
            "reconstruction_evidence": reconstruction_evidence,
            "selection_seed": str(seed),
            "train": {
                "sid": train_session["session_id"],
                "start_time": train_session["start_time"],
                "source": train_session["source"],
                "source_aliases": train_session.get("source_aliases", []),
                "repo": train_session["repo"],
                "turns": len(train_session["turns"]),
                "excerpt": excerpt(train_session["turns"], train_centers),
            },
            "held": {
                "sid": held_session["session_id"],
                "start_time": held_session["start_time"],
                "source": held_session["source"],
                "source_aliases": held_session.get("source_aliases", []),
                "repo": held_session["repo"],
                "turns": len(held_session["turns"]),
                "excerpt": excerpt(held_session["turns"], held_centers),
            },
            "matches": match_records,
        }
    )

payload = {
    "policy_version": manifest["policy_version"],
    "policy_fingerprint": manifest["policy_fingerprint"],
    "cohort_fingerprint": manifest["cohort_fingerprint"],
    "method": {
        "developer_selection": "top 10 by count of exact normalized substantial messages repeated across train and held-out",
        "held_selection": "uniform deterministic-random among held sessions containing at least one overlap",
        "train_selection": "session with most exact normalized messages shared with the chosen held session",
        "substantial_message": "human user-role text with normalized length >= 24 characters",
        "context": f"plus/minus {CONTEXT_RADIUS} turns around up to {MAX_MATCHES} longest shared messages",
    },
    "comparisons": comparisons,
}
OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
print(
    json.dumps(
        [
            {
                "developer": item["developer"],
                "developer_overlap_messages": item["developer_overlap_messages"],
                "pair_overlap_messages": item["pair_overlap_messages"],
                "train": item["train"]["sid"],
                "held": item["held"]["sid"],
            }
            for item in comparisons
        ],
        indent=2,
    )
)

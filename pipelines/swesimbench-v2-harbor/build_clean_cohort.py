#!/usr/bin/env python3
"""Build a coverage-complete, deduplicated cohort manifest and session store."""
from __future__ import annotations

import glob
import hashlib
import json
import os
import pickle
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "/data/claude-crawl")
from cohort_policy import (  # noqa: E402
    EXCLUDED_USERS,
    POLICY_VERSION,
    RECONSTRUCTION_THRESHOLDS,
    canonical_session_id,
    clean_turn,
    command_expansion_payloads,
    human_turn_count,
    is_extreme_session_fragmentation,
    is_incomplete_dialogue,
    normalize_text,
    ordered_trace_sequence,
    policy_fingerprint,
    reconstructed_session_evidence,
    specstory_session_id,
    specstory_timestamp,
    substantial_human_count,
    substantial_user_events,
    transcript_hash,
)

ROOT = Path("/data/swesimbench-v2-harbor")
SOURCE_MANIFEST = Path("/data/claude-crawl/meta/users_cc.json")
CLEAN_MANIFEST = ROOT / "clean_manifest.json"
CLEAN_SESSIONS = ROOT / "clean_sessions.jsonl"
BUILD_REPORT = ROOT / "clean_build_report.json"
CANDIDATE_CACHE = ROOT / ".clean_candidates.cache.pkl"
CANDIDATE_CACHE_VERSION = 2
MIN_TRAIN = 400
MIN_HELD = 100
# Prefer native full-trace sources over SpecStory markdown exports when aliases collide.
SOURCE_PRIORITY = {
    "entire": 5,
    "crawl": 4,
    "dataclaw": 3,
    "swechat": 2,
    "specstory": 1,
}


def candidate(session: dict, source: str, owner: str | None = None) -> dict:
    sid = session.get("session_id")
    turns = session.get("turns") or []
    fidelity = session.get("text_fidelity")
    if fidelity is None:
        if source in {"crawl", "swechat"}:
            fidelity = "full"
        elif source == "specstory":
            fidelity = "lossy"
        else:
            fidelity = "legacy_unknown"
    return {
        "sid": sid,
        "canonical": canonical_session_id(sid),
        "source": source,
        "owner": owner,
        "repo": session.get("repo") or "?",
        "ts": str(session.get("created_at") or session.get("start_time") or ""),
        "turns": turns,
        "trace_hash": transcript_hash(turns),
        "sequence": ordered_trace_sequence(turns),
        "human_turns": human_turn_count(turns),
        "substantial_human_turns": substantial_human_count(turns),
        "content_chars": sum(len(turn.get("text") or "") for turn in turns),
        "text_fidelity": fidelity,
        "parser_version": session.get("parser_version"),
    }


def apply_command_expansion_policy(records: list[dict]) -> tuple[set[str], int]:
    """Reclassify payloads proven by a slash-command marker in any source copy."""
    payloads = {
        payload
        for record in records
        for payload in command_expansion_payloads(record["turns"])
    }
    reclassified = 0
    for record in records:
        changed = False
        for turn in record["turns"]:
            if (
                turn.get("role") == "user"
                and normalize_text(turn.get("text") or "") in payloads
            ):
                turn["role"] = "system"
                reclassified += 1
                changed = True
        if changed:
            record["trace_hash"] = transcript_hash(record["turns"])
            record["sequence"] = ordered_trace_sequence(record["turns"])
            record["human_turns"] = human_turn_count(record["turns"])
            record["substantial_human_turns"] = substantial_human_count(
                record["turns"]
            )
    return payloads, reclassified


def richness(record: dict) -> tuple:
    return (
        record["human_turns"],
        len(record["turns"]),
        record["content_chars"],
        SOURCE_PRIORITY.get(record["source"], 0),
        record["sid"],
    )


def reconstruction_richness(record: dict) -> tuple:
    return (
        len(record["turns"]),
        record["content_chars"],
        record["human_turns"],
        SOURCE_PRIORITY.get(record["source"], 0),
        record["sid"],
    )


def load_candidates(target_ids: set[str], target_canonical: set[str]) -> list[dict]:
    result = []

    def wanted(sid: str | None) -> bool:
        return bool(sid and (sid in target_ids or canonical_session_id(sid) in target_canonical))

    print("indexing Entire candidates...", flush=True)
    for filename in glob.glob("/data/entire-backfill/corpus/*.jsonl"):
        with open(filename, errors="replace") as handle:
            for line in handle:
                try:
                    session = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if wanted(session.get("session_id")):
                    result.append(candidate(session, "entire", "gh:" + session.get("actor", "?")))

    print("indexing Crawl candidates...", flush=True)
    for filename in glob.glob("/data/claude-crawl/corpus/*.jsonl"):
        with open(filename, errors="replace") as handle:
            for line in handle:
                try:
                    session = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if wanted(session.get("session_id")):
                    result.append(candidate(session, "crawl", session.get("user")))

    print("indexing DataClaw candidates...", flush=True)
    dataclaw_path = Path(
        os.environ.get(
            "DATACLAW_CORPUS", "/data/dataclaw/meta/corpus.full.jsonl"
        )
    )
    if dataclaw_path.exists():
        with dataclaw_path.open(errors="replace") as handle:
            for line in handle:
                try:
                    session = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if wanted(session.get("session_id")):
                    result.append(candidate(session, "dataclaw", "dc:" + session.get("donor", "?")))

    # Census includes SWE-chat, so preparation must index it as well.
    import pyarrow.parquet as pq

    parquet = (
        "/data/with-user/data_cache/hf/"
        "datasets--SALT-NLP--SWE-chat/snapshots/"
        "f66cca95b14caaa4177f7ed5eaa424608dadcffa/"
        "conversations.parquet"
    )
    grouped: dict[str, dict] = {}
    print("streaming SWE-chat candidates...", flush=True)
    parquet_file = pq.ParquetFile(parquet)
    columns = ["user_id", "session_id", "turn_type", "content", "timestamp"]
    for batch in parquet_file.iter_batches(batch_size=65_536, columns=columns):
        values = {name: batch.column(name).to_pylist() for name in columns}
        for uid, sid, turn_type, content, timestamp in zip(
            values["user_id"],
            values["session_id"],
            values["turn_type"],
            values["content"],
            values["timestamp"],
        ):
            if not wanted(sid):
                continue
            if turn_type == "user_prompt":
                role = "user"
            elif turn_type == "assistant_response":
                role = "assistant"
            else:
                continue
            record = grouped.setdefault(
                sid,
                {
                    "session_id": sid,
                    "user_id": uid,
                    "start_time": timestamp,
                    "turns": [],
                    "text_fidelity": "full",
                    "parser_version": "SALT-NLP/SWE-chat@f66cca95",
                },
            )
            record["turns"].append(
                {
                    "role": role,
                    "text": content or "",
                    "ts": timestamp.isoformat() if timestamp is not None else None,
                }
            )
            if timestamp is not None and (
                record["start_time"] is None or timestamp < record["start_time"]
            ):
                record["start_time"] = timestamp
    for session in grouped.values():
        if session["start_time"] is not None:
            session["start_time"] = session["start_time"].isoformat()
        session["turns"].sort(key=lambda turn: turn.get("ts") or "")
        result.append(candidate(session, "swechat", "gh:" + str(session["user_id"] or "?")))

    print("indexing SpecStory candidates...", flush=True)
    specstory_path = Path("/data/specstory/meta/corpus_redacted.jsonl")
    if specstory_path.exists():
        with specstory_path.open(errors="replace") as handle:
            for line in handle:
                try:
                    session = json.loads(line)
                except json.JSONDecodeError:
                    continue
                sid = specstory_session_id(session)
                if not wanted(sid):
                    continue
                owner = session.get("owner") or (session.get("repo") or "?").split("/")[0]
                normalized = {
                    "session_id": sid,
                    "repo": session.get("repo") or "?",
                    "start_time": specstory_timestamp(session),
                    "turns": session.get("turns") or [],
                }
                result.append(candidate(normalized, "specstory", "gh:" + owner))

    print(f"indexed {len(result)} candidate records", flush=True)
    return result


def choose_candidate(candidates: list[dict]) -> dict:
    full_fidelity = [
        record for record in candidates if record.get("text_fidelity") == "full"
    ]
    if not full_fidelity:
        sources = sorted({record["source"] for record in candidates})
        raise RuntimeError(
            "session has no full-fidelity candidate; refresh source parsers first "
            f"(sources={sources})"
        )
    return max(full_fidelity, key=richness)


def candidate_cache_key(target_ids: set[str]) -> str:
    files = (
        glob.glob("/data/entire-backfill/corpus/*.jsonl")
        + glob.glob("/data/claude-crawl/corpus/*.jsonl")
        + [
            os.environ.get(
                "DATACLAW_CORPUS", "/data/dataclaw/meta/corpus.full.jsonl"
            )
        ]
        + [
            "/data/with-user/data_cache/hf/"
            "datasets--SALT-NLP--SWE-chat/snapshots/"
            "f66cca95b14caaa4177f7ed5eaa424608dadcffa/"
            "conversations.parquet"
        ]
        + ["/data/specstory/meta/corpus_redacted.jsonl"]
    )
    source_state = []
    for filename in sorted(files):
        path = Path(filename)
        if path.exists():
            stat = path.stat()
            source_state.append((filename, stat.st_size, stat.st_mtime_ns))
    payload = {
        "cache_version": CANDIDATE_CACHE_VERSION,
        "targets": sorted(target_ids),
        "sources": source_state,
        "policy": policy_fingerprint(),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def merge_record_metadata(keep: dict, group: list[dict], rule: str) -> dict:
    merged = dict(keep)
    merged["original_ids"] = sorted(
        {sid for record in group for sid in record["original_ids"]}
    )
    merged["dedup_rules"] = sorted(
        {item for record in group for item in record["dedup_rules"]} | {rule}
    )
    merged["split"] = (
        "train" if any(record["split"] == "train" for record in group) else "held"
    )
    timestamps = [record["ts"] for record in group if record.get("ts")]
    if timestamps:
        merged["ts"] = min(timestamps)
    merged["source_aliases"] = sorted(
        {record["source"] for record in group}
        | {
            source
            for record in group
            for source in record.get("source_aliases", [])
        }
    )
    return merged


def collapse_content(records: list[dict], developer: str) -> tuple[list[dict], list[dict]]:
    """Collapse exact and strict-prefix snapshots across train and held-out."""
    provenance = []
    by_hash: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_hash[record["trace_hash"]].append(record)
    exact_kept = []
    for trace_hash, group in sorted(by_hash.items()):
        keep = dict(max(group, key=richness))
        if len(group) > 1:
            keep = merge_record_metadata(keep, group, "exact_transcript")
            provenance.append(
                {
                    "developer": developer,
                    "rule": "exact_transcript",
                    "kept": keep["sid"],
                    "collapsed": sorted(
                        item["sid"] for item in group if item["sid"] != keep["sid"]
                    ),
                    "trace_hash": trace_hash,
                    "crossed_split": len({item["split"] for item in group}) > 1,
                }
            )
        exact_kept.append(keep)

    removed: set[str] = set()
    prefix_groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in exact_kept:
        if record["repo"] != "?":
            prefix_groups[(record["repo"], record["ts"])].append(record)
    for group in prefix_groups.values():
        ordered = sorted(group, key=lambda record: (len(record["sequence"]), record["sid"]))
        for index, shorter in enumerate(ordered):
            if shorter["sid"] in removed or shorter["substantial_human_turns"] < 3:
                continue
            for longer in ordered[index + 1 :]:
                if longer["sid"] in removed:
                    continue
                sequence = shorter["sequence"]
                if (
                    len(sequence) < len(longer["sequence"])
                    and longer["sequence"][: len(sequence)] == sequence
                ):
                    original_splits = {shorter["split"], longer["split"]}
                    merged = merge_record_metadata(
                        longer, [longer, shorter], "strict_transcript_prefix"
                    )
                    longer.clear()
                    longer.update(merged)
                    removed.add(shorter["sid"])
                    provenance.append(
                        {
                            "developer": developer,
                            "rule": "strict_transcript_prefix",
                            "kept": longer["sid"],
                            "collapsed": [shorter["sid"]],
                            "trace_hash": shorter["trace_hash"],
                            "crossed_split": len(original_splits) > 1,
                        }
                    )
                    break
    collapsed = [record for record in exact_kept if record["sid"] not in removed]
    return collapsed, provenance


def reconstruction_candidate_pairs(records: list[dict]) -> set[tuple[int, int]]:
    events = [substantial_user_events(record["turns"]) for record in records]
    first_postings: dict[str, list[int]] = defaultdict(list)
    text_postings: dict[str, list[int]] = defaultdict(list)
    timestamp_postings: dict[tuple[str, int], list[int]] = defaultdict(list)
    distinctive_chars = RECONSTRUCTION_THRESHOLDS["distinctive_event_chars"]
    tolerance = RECONSTRUCTION_THRESHOLDS["timestamp_tolerance_seconds"]
    for index, sequence in enumerate(events):
        if sequence and len(sequence[0]["text"]) >= distinctive_chars:
            first_postings[sequence[0]["text"]].append(index)
        for text in {
            event["text"] for event in sequence if len(event["text"]) >= distinctive_chars
        }:
            text_postings[text].append(index)
        for event in sequence:
            if (
                len(event["text"]) < distinctive_chars
                or event["timestamp"] is None
            ):
                continue
            second = int(round(event["timestamp"]))
            for offset in range(-tolerance, tolerance + 1):
                timestamp_postings[(event["text"], second + offset)].append(index)

    pairs: set[tuple[int, int]] = set()
    for postings in first_postings.values():
        if len(postings) > 100:
            continue
        for offset, left in enumerate(postings):
            for right in postings[offset + 1 :]:
                pairs.add((left, right))
    for postings in text_postings.values():
        if len(postings) > 25:
            continue
        for offset, left in enumerate(postings):
            for right in postings[offset + 1 :]:
                pairs.add((left, right))
    for postings in timestamp_postings.values():
        unique = sorted(set(postings))
        for offset, left in enumerate(unique):
            for right in unique[offset + 1 :]:
                pairs.add((left, right))
    return pairs


def record_reconstruction_evidence(left: dict, right: dict) -> dict | None:
    evidence = reconstructed_session_evidence(left["turns"], right["turns"])
    concrete_repos = {
        record["repo"]
        for record in (left, right)
        if record.get("repo") and record["repo"] != "?"
    }
    if (
        evidence is not None
        and len(concrete_repos) > 1
        and evidence["anchor"] == "content"
    ):
        return None
    return evidence


def collapse_reconstructed_sessions(
    records: list[dict], developer: str
) -> tuple[list[dict], list[dict], int]:
    pairs = reconstruction_candidate_pairs(records)
    parent = list(range(len(records)))
    evidence_by_pair = {}

    def root(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = root(left), root(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for left, right in sorted(pairs):
        evidence = record_reconstruction_evidence(records[left], records[right])
        if evidence is not None:
            evidence_by_pair[(left, right)] = evidence
            union(left, right)

    components: dict[int, list[int]] = defaultdict(list)
    for index in range(len(records)):
        components[root(index)].append(index)

    kept = []
    provenance = []
    for indices in components.values():
        group = [records[index] for index in indices]
        winner = dict(max(group, key=reconstruction_richness))
        if len(group) > 1:
            winner = merge_record_metadata(winner, group, "reconstructed_session")
            component_edges = [
                {
                    "left": records[left]["sid"],
                    "right": records[right]["sid"],
                    "evidence": evidence,
                }
                for (left, right), evidence in evidence_by_pair.items()
                if left in indices and right in indices
            ]
            provenance.append(
                {
                    "developer": developer,
                    "rule": "reconstructed_session",
                    "kept": winner["sid"],
                    "collapsed": sorted(
                        record["sid"]
                        for record in group
                        if record["sid"] != winner["sid"]
                    ),
                    "crossed_split": len({record["split"] for record in group}) > 1,
                    "sources": sorted({record["source"] for record in group}),
                    "evidence": component_edges,
                }
            )
        kept.append(winner)

    survivors = [
        (kept[left]["sid"], kept[right]["sid"])
        for left, right in reconstruction_candidate_pairs(kept)
        if record_reconstruction_evidence(kept[left], kept[right]) is not None
    ]
    if survivors:
        raise RuntimeError(
            f"{developer}: reconstructed-session duplicates survived collapse: "
            f"{survivors[:10]}"
        )
    return kept, provenance, len(pairs)


def main() -> None:
    source_users = json.loads(SOURCE_MANIFEST.read_text())
    users = [user for user in source_users if user["user"] not in EXCLUDED_USERS]
    target_ids = {
        session["sid"]
        for user in users
        for split in ("train_sessions", "held_sessions")
        for session in user[split]
    }
    target_canonical = {canonical_session_id(sid) for sid in target_ids}
    cache_key = candidate_cache_key(target_ids)
    candidates = None
    if CANDIDATE_CACHE.exists():
        try:
            with CANDIDATE_CACHE.open("rb") as handle:
                cached_key, cached_candidates = pickle.load(handle)
            if cached_key == cache_key:
                candidates = cached_candidates
                print(f"loaded {len(candidates)} candidate records from cache", flush=True)
        except Exception:
            candidates = None
    if candidates is None:
        candidates = load_candidates(target_ids, target_canonical)
        command_payloads, command_turns = apply_command_expansion_policy(candidates)
        with CANDIDATE_CACHE.open("wb") as handle:
            pickle.dump((cache_key, candidates), handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"cached {len(candidates)} candidate records", flush=True)
    else:
        command_payloads, command_turns = apply_command_expansion_policy(candidates)
    print(
        f"classified {command_turns} command-expansion turns "
        f"from {len(command_payloads)} proven payloads",
        flush=True,
    )
    by_exact: dict[str, list[dict]] = defaultdict(list)
    by_canonical: dict[str, list[dict]] = defaultdict(list)
    for record in candidates:
        by_exact[record["sid"]].append(record)
        by_canonical[record["canonical"]].append(record)

    missing = sorted(sid for sid in target_ids if sid not in by_exact)
    if missing:
        raise RuntimeError(
            f"{len(missing)} manifest sessions remain missing after SWE-chat indexing; "
            f"first: {missing[:10]}"
        )

    canonical_owners: dict[str, set[str]] = defaultdict(set)
    for user in users:
        for split in ("train_sessions", "held_sessions"):
            for session in user[split]:
                canonical_owners[canonical_session_id(session["sid"])].add(user["user"])
    cross_user = {key: sorted(value) for key, value in canonical_owners.items() if len(value) > 1}
    if cross_user:
        raise RuntimeError(f"canonical session IDs cross developers: {cross_user}")

    clean_users = []
    session_store: dict[str, dict] = {}
    provenance = []
    dropped_threshold = []
    dropped_incomplete_dialogue = []
    reconstruction_candidate_pairs_checked = 0
    for user in users:
        dev = user["user"]
        grouped: dict[str, list[dict]] = defaultdict(list)
        manifest_entries: dict[str, list[tuple[str, dict]]] = defaultdict(list)
        for split_name, source_key in (("train", "train_sessions"), ("held", "held_sessions")):
            for session in user[source_key]:
                key = canonical_session_id(session["sid"])
                grouped[key].extend(by_exact[session["sid"]])
                manifest_entries[key].append((split_name, session))

        records = []
        for key, group in grouped.items():
            entries = manifest_entries[key]
            selected = dict(choose_candidate(group))
            aliases = sorted(
                {entry["sid"] for _, entry in entries}
                | {record["sid"] for record in group}
            )
            splits = {split for split, _ in entries}
            selected["sid"] = key
            selected["canonical"] = key
            selected["original_ids"] = aliases
            selected["dedup_rules"] = ["canonical_uuid"] if len(aliases) > 1 else []
            selected["source_aliases"] = sorted({record["source"] for record in group})
            selected["split"] = "train" if "train" in splits else "held"
            selected["ts"] = min(
                str(entry["ts"]) for _, entry in entries if entry.get("ts")
            )
            records.append(selected)
            if len(aliases) > 1 or len(splits) > 1:
                provenance.append(
                    {
                        "developer": dev,
                        "rule": "canonical_uuid",
                        "kept": key,
                        "collapsed": aliases,
                        "trace_hash": selected["trace_hash"],
                        "crossed_split": len(splits) > 1,
                    }
                )

        records, events = collapse_content(records, dev)
        provenance.extend(events)
        records, events, checked = collapse_reconstructed_sessions(records, dev)
        provenance.extend(events)
        reconstruction_candidate_pairs_checked += checked

        complete_records = []
        for record in records:
            if is_incomplete_dialogue(record["turns"]):
                dropped_incomplete_dialogue.append(
                    {
                        "user": dev,
                        "sid": record["sid"],
                        "source": record["source"],
                        "split": record["split"],
                        "human_turns": record["human_turns"],
                        "assistant_turns": sum(
                            1
                            for turn in record["turns"]
                            if turn.get("role") == "assistant"
                        ),
                        "reason": "incomplete_dialogue",
                    }
                )
            else:
                complete_records.append(record)
        records = complete_records

        split_records = {
            "train": [record for record in records if record["split"] == "train"],
            "held": [record for record in records if record["split"] == "held"],
        }

        train_hashes = {record["trace_hash"] for record in split_records["train"]}
        held_hashes = {record["trace_hash"] for record in split_records["held"]}
        overlap = train_hashes & held_hashes
        if overlap:
            raise RuntimeError(f"{dev}: {len(overlap)} exact transcripts cross train/held")

        train_turns = sum(record["human_turns"] for record in split_records["train"])
        held_turns = sum(record["human_turns"] for record in split_records["held"])
        session_count = len(split_records["train"]) + len(split_records["held"])
        if train_turns < MIN_TRAIN or held_turns < MIN_HELD:
            dropped_threshold.append(
                {
                    "user": dev,
                    "train_turns": train_turns,
                    "held_turns": held_turns,
                    "reason": "below_clean_threshold",
                }
            )
            continue
        if is_extreme_session_fragmentation(
            session_count, train_turns + held_turns
        ):
            dropped_threshold.append(
                {
                    "user": dev,
                    "train_turns": train_turns,
                    "held_turns": held_turns,
                    "sessions": session_count,
                    "mean_human_turns_per_session": round(
                        (train_turns + held_turns) / session_count, 3
                    ),
                    "reason": "extreme_session_fragmentation",
                }
            )
            continue

        train_ts = [record["ts"] for record in split_records["train"]]
        held_ts = [record["ts"] for record in split_records["held"]]
        if max(train_ts) >= min(held_ts):
            raise RuntimeError(f"{dev}: invalid chronological train/held boundary")

        manifest_record = {
            "user": dev,
            "sources": user.get("sources", []),
            "train_turns": train_turns,
            "held_turns": held_turns,
            "train_sessions": [],
            "held_sessions": [],
        }
        for split_name, output_key in (("train", "train_sessions"), ("held", "held_sessions")):
            for record in sorted(split_records[split_name], key=lambda item: (item["ts"], item["sid"])):
                clean = [clean_turn(turn) for turn in record["turns"]]
                stored = {
                    "session_id": record["sid"],
                    "user": dev,
                    "source": record["source"],
                    "source_aliases": record.get("source_aliases", [record["source"]]),
                    "repo": record["repo"],
                    "start_time": record["ts"],
                    "original_ids": record["original_ids"],
                    "dedup_rules": record["dedup_rules"],
                    "trace_hash": record["trace_hash"],
                    "text_fidelity": record["text_fidelity"],
                    "parser_version": record.get("parser_version"),
                    "turns": clean,
                }
                existing = session_store.get(record["sid"])
                if existing and existing["user"] != dev:
                    raise RuntimeError(f"session store collision: {record['sid']}")
                session_store[record["sid"]] = stored
                manifest_record[output_key].append(
                    {
                        "sid": record["sid"],
                        "ts": record["ts"],
                        "n": record["human_turns"],
                        "repo": record["repo"],
                        "source": record["source"],
                        "source_aliases": record.get("source_aliases", [record["source"]]),
                        "original_ids": record["original_ids"],
                        "dedup_rules": record["dedup_rules"],
                        "trace_hash": record["trace_hash"],
                        "text_fidelity": record["text_fidelity"],
                        "parser_version": record.get("parser_version"),
                    }
                )
        clean_users.append(manifest_record)

    # Full-trace equality across developers is always suspicious.
    hash_owners: dict[str, set[str]] = defaultdict(set)
    hash_sessions: dict[str, list[dict]] = defaultdict(list)
    for session in session_store.values():
        hash_owners[session["trace_hash"]].add(session["user"])
        hash_sessions[session["trace_hash"]].append(session)
    cross_user_hashes = {
        trace_hash: {
            "owners": sorted(owners),
            "sessions": sorted(session["session_id"] for session in hash_sessions[trace_hash]),
            "max_substantial_human_turns": max(
                substantial_human_count(session["turns"])
                for session in hash_sessions[trace_hash]
            ),
        }
        for trace_hash, owners in hash_owners.items()
        if len(owners) > 1
    }
    strong_cross_user_hashes = {
        trace_hash: detail
        for trace_hash, detail in cross_user_hashes.items()
        if detail["max_substantial_human_turns"] >= 3
    }
    if strong_cross_user_hashes:
        raise RuntimeError(
            f"{len(strong_cross_user_hashes)} substantial exact transcripts occur across developers: "
            f"{strong_cross_user_hashes}"
        )

    stored_records = list(session_store.values())
    cross_user_reconstructed = []
    for left, right in reconstruction_candidate_pairs(stored_records):
        if stored_records[left]["user"] == stored_records[right]["user"]:
            continue
        evidence = record_reconstruction_evidence(
            stored_records[left], stored_records[right]
        )
        if evidence is not None:
            cross_user_reconstructed.append(
                {
                    "left": stored_records[left]["session_id"],
                    "left_user": stored_records[left]["user"],
                    "right": stored_records[right]["session_id"],
                    "right_user": stored_records[right]["user"],
                    "evidence": evidence,
                }
            )
    if cross_user_reconstructed:
        raise RuntimeError(
            f"{len(cross_user_reconstructed)} reconstructed sessions cross developers: "
            f"{cross_user_reconstructed[:10]}"
        )

    clean_users.sort(key=lambda item: item["user"])
    cohort_payload = {
        "policy_version": POLICY_VERSION,
        "policy_fingerprint": policy_fingerprint(),
        "users": clean_users,
    }
    cohort_fingerprint = hashlib.sha256(
        json.dumps(cohort_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    cohort_payload["cohort_fingerprint"] = cohort_fingerprint
    CLEAN_MANIFEST.write_text(json.dumps(cohort_payload, indent=2, ensure_ascii=False))
    with CLEAN_SESSIONS.open("w") as handle:
        for sid in sorted(session_store):
            handle.write(json.dumps(session_store[sid], ensure_ascii=False) + "\n")
    report = {
        "policy_version": POLICY_VERSION,
        "policy_fingerprint": policy_fingerprint(),
        "cohort_fingerprint": cohort_fingerprint,
        "source_manifest_users": len(source_users),
        "excluded_users": sorted(set(EXCLUDED_USERS) & {user["user"] for user in source_users}),
        "retained_users": len(clean_users),
        "dropped_below_clean_threshold": dropped_threshold,
        "dropped_incomplete_dialogue_sessions": len(dropped_incomplete_dialogue),
        "dropped_incomplete_dialogue": dropped_incomplete_dialogue,
        "source_manifest_sessions": len(target_ids),
        "candidate_records": len(candidates),
        "command_expansion_payloads": len(command_payloads),
        "command_expansion_turns": command_turns,
        "command_expansion_payload_hashes": sorted(
            hashlib.sha256(payload.encode()).hexdigest()
            for payload in command_payloads
        ),
        "clean_sessions": len(session_store),
        "dedup_events": len(provenance),
        "reconstruction_candidate_pairs_checked": reconstruction_candidate_pairs_checked,
        "reconstructed_session_events": sum(
            event["rule"] == "reconstructed_session" for event in provenance
        ),
        "cross_split_dedup_events": sum(
            bool(event.get("crossed_split")) for event in provenance
        ),
        "dedup_rule_counts": dict(
            sorted(
                {
                    rule: sum(event["rule"] == rule for event in provenance)
                    for rule in {event["rule"] for event in provenance}
                }.items()
            )
        ),
        "weak_cross_user_exact_transcripts": cross_user_hashes,
        "cross_user_reconstructed_sessions": cross_user_reconstructed,
        "provenance": provenance,
    }
    BUILD_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(
        json.dumps(
            {
                key: value
                for key, value in report.items()
                if key not in {"provenance", "dropped_incomplete_dialogue"}
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

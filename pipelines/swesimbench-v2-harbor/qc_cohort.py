#!/usr/bin/env python3
"""Deterministic QC audit and message sampling for the SWESimBench v2 cohort."""
from __future__ import annotations

import glob
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, "/data/claude-crawl")
from cohort_policy import (  # noqa: E402
    EXCLUDED_USERS,
    POLICY_VERSION,
    canonical_session_id as policy_session_id,
    injected_role,
    is_extreme_session_fragmentation,
    is_human_target,
    is_incomplete_dialogue,
    is_placeholder as policy_is_placeholder,
    policy_fingerprint,
    scrub_text,
)

ROOT = Path("/data/swesimbench-v2-harbor")
MANIFEST = ROOT / "clean_manifest.json"
OUT = ROOT / "cohort_qc_report.json"
EXCLUDE_USERS = set(EXCLUDED_USERS)
SAMPLE_PER_DEV = 10
SAMPLE_CHARS = 360

NOISE_PREFIXES = (
    "<command-",
    "<command",
    "<local-command",
    "Caveat:",
    "[Request interrupted",
    "<task-notification",
    "<turn_aborted",
    "<subagent_notification",
    "<system_instruction",
    "<teammate-message",
    "<bash-stdout",
    "<bash-stderr",
    "<user-prompt-submit-hook",
    "<session-start-hook",
    "<user-memory-input",
    "This session is being continued",
    "<system-reminder",
    "[SYSTEM",
    "<ide_opened_file",
    "<ide_selection",
    "<ide_diagnostics",
    "<ide-",
    "<budget:",
    "<post-tool",
    "<pre-tool",
    "<environment_context",
    "<user_instructions",
    "<turn_context",
    "<permissions",
    "Tool loaded",
    "Skill loaded",
    "<skill-",
    "<uploaded_files",
    "<attached_files",
    "<cursor_commands",
    "<external_links",
    "<git_status",
    "<timestamp",
    "<agent_transcripts",
    "<manually_attached_skills",
    "<hooks_context",
    "<uploaded_documents",
    "<subagent_delegation_context",
    "<image_files",
    "<system_notification",
    "<bash-input",
    "<bash-notification",
    "<open_and_recently_viewed_files",
)
PLACEHOLDER_PATTERNS = (
    re.compile(r"^turn\s+\d+$", re.I),
    re.compile(r"^(test|testing|placeholder|sample|dummy)(\s+\d+)?$", re.I),
    re.compile(r"^(hello|hi)\s+world!?$", re.I),
)
SUSPICIOUS_SID = re.compile(r"(^|[-_/|])(fake|dummy|synthetic|placeholder|fixture|test)([-_/|.]|$)", re.I)
UUID_IN_SID = re.compile(
    r"(?i)[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"gh[po]_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r'(?i)(api[_-]?key|secret|token|password)["\'`]?\s*[:=]\s*["\'`]?[A-Za-z0-9_-]{16,}'),
)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def is_noise(text: str) -> bool:
    return not text.strip() or injected_role(text) is not None


def is_placeholder(text: str) -> bool:
    return policy_is_placeholder(text)


def has_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def scrub(text: str) -> str:
    value = scrub_text(text)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:SAMPLE_CHARS] + (" […truncated]" if len(value) > SAMPLE_CHARS else "")


def canonical_session_id(sid: str) -> str:
    return policy_session_id(sid)


def load_index() -> tuple[dict[str, list[dict]], dict[str, str]]:
    index: dict[str, list[dict]] = {}
    source: dict[str, str] = {}
    with (ROOT / "clean_sessions.jsonl").open(errors="replace") as handle:
        for line in handle:
            session = json.loads(line)
            sid = session["session_id"]
            index[sid] = session["turns"]
            source[sid] = session["source"]
    return index, source


def substantial_messages(sessions: list[dict], index: dict[str, list[dict]]) -> Counter:
    values = Counter()
    for session in sessions:
        for turn in index.get(session["sid"], []):
            if turn.get("role") != "user":
                continue
            text = turn.get("text") or ""
            value = norm(text)
            if len(value) >= 24 and is_human_target(turn):
                values[value] += 1
    return values


def main() -> None:
    clean_payload = json.loads(MANIFEST.read_text())
    assert clean_payload["policy_version"] == POLICY_VERSION
    assert clean_payload["policy_fingerprint"] == policy_fingerprint()
    manifest = clean_payload["users"]
    build_report = json.loads((ROOT / "clean_build_report.json").read_text())
    manifest_all_count = build_report["source_manifest_users"]
    index, source = load_index()

    session_owners: dict[str, set[str]] = defaultdict(set)
    held_content_owners: dict[str, set[str]] = defaultdict(set)
    audits = []
    all_samples = []

    for user in manifest:
        dev = user["user"]
        train_sessions = user["train_sessions"]
        held_sessions = user["held_sessions"]
        all_sessions = train_sessions + held_sessions
        train_ids = {session["sid"] for session in train_sessions}
        held_ids = {session["sid"] for session in held_sessions}
        for sid in train_ids | held_ids:
            session_owners[sid].add(dev)

        train_messages = substantial_messages(train_sessions, index)
        held_messages = substantial_messages(held_sessions, index)
        leakage = train_messages.keys() & held_messages.keys()
        missing_train_sessions = [session["sid"] for session in train_sessions if session["sid"] not in index]
        missing_held_sessions = [session["sid"] for session in held_sessions if session["sid"] not in index]
        missing_all_sessions = missing_train_sessions + missing_held_sessions
        aliases: dict[str, set[str]] = defaultdict(set)
        for session in all_sessions:
            aliases[canonical_session_id(session["sid"])].add(session["sid"])
        alias_groups = [sorted(group) for group in aliases.values() if len(group) > 1]
        canonical_train = {canonical_session_id(sid) for sid in train_ids}
        canonical_held = {canonical_session_id(sid) for sid in held_ids}
        canonical_split_overlap = sorted(canonical_train & canonical_held)
        manifest_turns = (user.get("train_turns") or 0) + (user.get("held_turns") or 0)
        mean_turns_per_session = manifest_turns / len(all_sessions) if all_sessions else 0

        records = []
        missing_sessions = list(missing_held_sessions)
        fake_sessions = []
        role_counts = Counter()
        empty_user = noise_user = placeholder_user = secret_user = 0
        total_user = eligible_user = short_user = compaction_user = 0
        sessions_without_eligible = 0
        incomplete_dialogue_sessions = [
            session["sid"]
            for session in all_sessions
            if session["sid"] in index and is_incomplete_dialogue(index[session["sid"]])
        ]

        for session in held_sessions:
            sid = session["sid"]
            turns = index.get(sid)
            if turns is None:
                continue
            # SpecStory synthetic ids embed markdown titles (often containing "test");
            # only flag non-SpecStory ids for fixture/test/dummy naming.
            if not str(sid).startswith("ss:") and SUSPICIOUS_SID.search(sid):
                fake_sessions.append(sid)
            session_eligible = 0
            has_prior_assistant = False
            for turn_index, turn in enumerate(turns):
                role = turn.get("role")
                role_counts[role or "missing"] += 1
                if role == "assistant":
                    has_prior_assistant = True
                    continue
                if role != "user":
                    continue
                total_user += 1
                text = turn.get("text") or ""
                stripped = text.strip()
                if not stripped:
                    empty_user += 1
                    continue
                if stripped.startswith("This session is being continued"):
                    compaction_user += 1
                if not is_human_target(turn):
                    noise_user += 1
                    continue
                if is_placeholder(text):
                    placeholder_user += 1
                if has_secret(text):
                    secret_user += 1
                if len(stripped.split()) <= 2:
                    short_user += 1
                if has_prior_assistant:
                    eligible_user += 1
                    session_eligible += 1
                    message_norm = norm(text)
                    if len(message_norm) >= 24:
                        held_content_owners[message_norm].add(dev)
                    records.append(
                        {
                            "sid": sid,
                            "turn_index": turn_index,
                            "source": source.get(sid, "unknown"),
                            "words": len(stripped.split()),
                            "chars": len(stripped),
                            "text": scrub(text),
                            "_norm": message_norm,
                        }
                    )
            if session_eligible == 0:
                sessions_without_eligible += 1

        normalized = [record["_norm"] for record in records]
        unique_messages = len(set(normalized))
        duplicate_rate = 1 - (unique_messages / eligible_user) if eligible_user else 1
        top_message, top_count = Counter(normalized).most_common(1)[0] if normalized else ("", 0)
        rng = random.Random(int(hashlib.sha256(dev.encode()).hexdigest()[:16], 16))
        sampled = rng.sample(records, min(SAMPLE_PER_DEV, len(records))) if records else []
        for record in sampled:
            record.pop("_norm", None)
        all_samples.append({"developer": dev, "messages": sampled})

        train_ts = [str(session.get("ts", "")) for session in train_sessions if session.get("ts")]
        held_ts = [str(session.get("ts", "")) for session in held_sessions if session.get("ts")]
        chronological = bool(train_ts and held_ts and max(train_ts) < min(held_ts))

        flags = []
        if missing_all_sessions:
            flags.append("missing_indexed_sessions")
        if alias_groups:
            flags.append("session_id_alias_duplicates")
        if fake_sessions:
            flags.append("suspicious_session_id")
        if placeholder_user:
            flags.append("placeholder_messages")
        if duplicate_rate >= 0.5 and eligible_user >= 20:
            flags.append("high_exact_duplicate_rate")
        if eligible_user and top_count / eligible_user >= 0.2 and top_count >= 5:
            flags.append("dominant_repeated_message")
        if total_user and noise_user / total_user >= 0.1:
            flags.append("high_metadata_noise")
        if not chronological:
            flags.append("invalid_chronological_split")
        if train_ids & held_ids:
            flags.append("train_held_session_overlap")
        if canonical_split_overlap:
            flags.append("train_held_canonical_session_overlap")
        if secret_user:
            flags.append("secret_like_content_redacted")
        if eligible_user < 30:
            flags.append("low_eligible_turn_count")
        if is_extreme_session_fragmentation(len(all_sessions), manifest_turns):
            flags.append("extreme_session_fragmentation")
        if incomplete_dialogue_sessions:
            flags.append("incomplete_dialogue_sessions")

        severe = {
            "suspicious_session_id",
            "placeholder_messages",
            "train_held_session_overlap",
            "train_held_canonical_session_overlap",
            "invalid_chronological_split",
            "extreme_session_fragmentation",
            "incomplete_dialogue_sessions",
        }
        status = "fail" if severe & set(flags) else ("pass_with_notes" if flags else "pass")
        decision_notes = []
        if "low_eligible_turn_count" in flags and status != "fail":
            decision_notes.append("retain: genuine messages; report low per-developer evaluation power")
        if "extreme_session_fragmentation" in flags:
            decision_notes.append(
                "exclude: daemon/automation fragments yield almost no post-assistant eval targets"
            )
        if "incomplete_dialogue_sessions" in flags:
            decision_notes.append(
                "exclude: sessions with zero assistant or zero human turns cannot support dialogue eval"
            )
        if "dominant_repeated_message" in flags and status != "fail":
            decision_notes.append("retain: repeated short directives are genuine developer behavior")
        if "secret_like_content_redacted" in flags and status != "fail":
            decision_notes.append("retain: only scrubbed text enters clean artifacts")
        audits.append(
            {
                "developer": dev,
                "status": status,
                "flags": flags,
                "decision": "exclude" if status == "fail" else "retain",
                "decision_notes": decision_notes,
                "sources": user.get("sources", []),
                "train_turns_manifest": user.get("train_turns"),
                "held_turns_manifest": user.get("held_turns"),
                "train_sessions": len(train_sessions),
                "held_sessions": len(held_sessions),
                "manifest_sessions": len(all_sessions),
                "indexed_manifest_sessions": len(all_sessions) - len(missing_all_sessions),
                "mean_manifest_turns_per_session": round(mean_turns_per_session, 3),
                "held_sessions_found": len(held_sessions) - len(missing_sessions),
                "sessions_without_eligible": sessions_without_eligible,
                "incomplete_dialogue_sessions": len(incomplete_dialogue_sessions),
                "incomplete_dialogue_session_ids": incomplete_dialogue_sessions[:10],
                "eligible_held_messages": eligible_user,
                "unique_eligible_messages": unique_messages,
                "exact_duplicate_rate": round(duplicate_rate, 4),
                "short_message_rate": round(short_user / total_user, 4) if total_user else None,
                "noise_user_turns": noise_user,
                "compaction_user_turns": compaction_user,
                "placeholder_user_turns": placeholder_user,
                "secret_like_user_turns": secret_user,
                "repeated_substantial_messages_across_splits": len(leakage),
                "top_repeated_message_count": top_count,
                "top_repeated_message": scrub(top_message) if top_message else None,
                "missing_session_ids": missing_sessions,
                "missing_train_session_ids": missing_train_sessions,
                "missing_all_session_ids": missing_all_sessions,
                "session_id_alias_group_count": len(alias_groups),
                "session_id_alias_duplicate_count": sum(len(group) - 1 for group in alias_groups),
                "session_id_alias_examples": alias_groups[:5],
                "train_held_canonical_session_overlap": canonical_split_overlap,
                "suspicious_session_ids": fake_sessions,
            }
        )

    shared_session_ids = {sid: sorted(owners) for sid, owners in session_owners.items() if len(owners) > 1}
    shared_content = {text: owners for text, owners in held_content_owners.items() if len(owners) > 1}
    shared_content_by_dev = Counter()
    for owners in shared_content.values():
        for dev in owners:
            shared_content_by_dev[dev] += 1
    for audit in audits:
        audit["cross_developer_shared_substantial_messages"] = shared_content_by_dev[audit["developer"]]
        if shared_content_by_dev[audit["developer"]] >= 10:
            audit["flags"].append("cross_developer_content_overlap")
            if audit["status"] == "pass":
                audit["status"] = "pass_with_notes"
            audit["decision_notes"].append(
                "retain: overlap is common developer language, not shared substantial transcripts"
            )

    status_counts = Counter(audit["status"] for audit in audits)
    flag_counts = Counter(flag for audit in audits for flag in audit["flags"])
    report = {
        "method": {
            "excluded_users": sorted(EXCLUDE_USERS),
            "sample_per_developer": SAMPLE_PER_DEV,
            "sample_seed": "first 64 bits of SHA-256(developer id)",
            "sample_population": "eligible held-out user messages after a preceding assistant turn",
            "samples_secret_scrubbed": True,
        },
        "summary": {
            "manifest_users_before_exclusion": manifest_all_count,
            "audited_users": len(manifest),
            "status_counts": dict(status_counts),
            "flag_counts": dict(flag_counts),
            "held_sessions": sum(audit["held_sessions"] for audit in audits),
            "held_sessions_found": sum(audit["held_sessions_found"] for audit in audits),
            "manifest_sessions": sum(audit["manifest_sessions"] for audit in audits),
            "indexed_manifest_sessions": sum(audit["indexed_manifest_sessions"] for audit in audits),
            "session_id_alias_duplicate_count": sum(audit["session_id_alias_duplicate_count"] for audit in audits),
            "eligible_held_messages": sum(audit["eligible_held_messages"] for audit in audits),
            "sampled_messages": sum(len(item["messages"]) for item in all_samples),
            "shared_session_ids_across_developers": len(shared_session_ids),
            "shared_substantial_messages_across_developers": len(shared_content),
            "dedup_events": build_report["dedup_events"],
            "dedup_rule_counts": build_report["dedup_rule_counts"],
            "reconstructed_session_events": build_report[
                "reconstructed_session_events"
            ],
            "cross_split_dedup_events": build_report["cross_split_dedup_events"],
            "reconstruction_candidate_pairs_checked": build_report[
                "reconstruction_candidate_pairs_checked"
            ],
            "weak_cross_user_exact_transcripts": len(
                build_report["weak_cross_user_exact_transcripts"]
            ),
        },
        "developers": sorted(
            audits,
            key=lambda audit: (
                {"fail": 0, "pass_with_notes": 1, "pass": 2}[audit["status"]],
                audit["developer"],
            ),
        ),
        "samples": sorted(all_samples, key=lambda item: item["developer"]),
        "shared_session_ids": shared_session_ids,
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report["summary"], indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

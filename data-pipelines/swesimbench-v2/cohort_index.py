#!/usr/bin/env python3
"""Sid index + lazy turn loading for clean-cohort builds.

Avoids json.loads on every multi-MB tool-heavy JSONL line during candidate indexing.
"""
from __future__ import annotations

import glob
import json
import os
import pickle
import re
from collections import defaultdict
from pathlib import Path

from cohort_policy import (
    canonical_session_id,
    human_turn_count,
    specstory_session_id,
    specstory_timestamp,
    substantial_human_count,
    transcript_hash,
)

ROOT = Path("/data/swesimbench-v2-harbor")
SID_INDEX_PATH = ROOT / ".corpus_sid_index_v1.pkl"
_SID_KEY_RE = re.compile(rb'"session_id"\s*:\s*"((?:\\.|[^"\\])*)"')


def extract_session_id_bytes(line: bytes) -> str | None:
    match = _SID_KEY_RE.search(line)
    if not match:
        return None
    try:
        return json.loads(b'"' + match.group(1) + b'"')
    except Exception:
        return None


def _source_fingerprint(paths: list[str]) -> list[tuple]:
    state = []
    for filename in sorted(paths):
        path = Path(filename)
        if path.exists():
            stat = path.stat()
            state.append((filename, stat.st_size, stat.st_mtime_ns))
    return state


def jsonl_corpus_paths() -> list[str]:
    paths = (
        glob.glob("/data/entire-backfill/corpus/*.jsonl")
        + glob.glob("/data/claude-crawl/corpus/*.jsonl")
        + ["/data/dataclaw/meta/corpus.jsonl"]
    )
    if os.environ.get("SKIP_SPECSTORY", "0") != "1":
        spec = "/data/specstory/meta/corpus_redacted.jsonl"
        if Path(spec).exists():
            paths.append(spec)
    return [p for p in paths if Path(p).exists()]


def build_or_load_sid_index() -> dict[str, list[tuple[str, int]]]:
    paths = jsonl_corpus_paths()
    fingerprint = _source_fingerprint(paths)
    if SID_INDEX_PATH.exists():
        try:
            with SID_INDEX_PATH.open("rb") as handle:
                cached = pickle.load(handle)
            if cached.get("fingerprint") == fingerprint and cached.get("version") == 1:
                index = cached["index"]
                print(
                    f"loaded sid index ({len(index)} sids) from {SID_INDEX_PATH.name}",
                    flush=True,
                )
                return index
        except Exception:
            pass

    print(f"building sid index over {len(paths)} jsonl files...", flush=True)
    index: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for filename in paths:
        with open(filename, "rb") as handle:
            while True:
                offset = handle.tell()
                line = handle.readline()
                if not line:
                    break
                if line.isspace():
                    continue
                sid = extract_session_id_bytes(line)
                if sid:
                    index[sid].append((filename, offset))
    index = dict(index)
    SID_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SID_INDEX_PATH.open("wb") as handle:
        pickle.dump(
            {"version": 1, "fingerprint": fingerprint, "index": index},
            handle,
            protocol=pickle.HIGHEST_PROTOCOL,
        )
    print(f"wrote sid index ({len(index)} sids) -> {SID_INDEX_PATH}", flush=True)
    return index


def load_session_at(path: str, offset: int) -> dict:
    with open(path, "rb") as handle:
        handle.seek(offset)
        line = handle.readline()
    return json.loads(line)


def ensure_turns(record: dict) -> list:
    turns = record.get("turns")
    if turns is not None:
        return turns
    ref = record.get("turns_ref")
    if not ref:
        record["turns"] = []
        return record["turns"]
    path, offset = ref
    session = load_session_at(path, offset)
    record["turns"] = session.get("turns") or []
    return record["turns"]


def drop_turns(record: dict) -> None:
    record["turns"] = None
    record["sequence"] = None


def source_for_path(path: str) -> str:
    if "/entire-backfill/corpus/" in path:
        return "entire"
    if "/claude-crawl/corpus/" in path:
        return "crawl"
    if "/dataclaw/meta/corpus.jsonl" in path:
        return "dataclaw"
    if "/specstory/" in path:
        return "specstory"
    return "unknown"


def candidate_from_session(
    session: dict,
    source: str,
    owner: str | None = None,
    turns_ref: tuple[str, int] | None = None,
    keep_turns: bool = False,
) -> dict:
    sid = session.get("session_id")
    turns = session.get("turns") or []
    record = {
        "sid": sid,
        "canonical": canonical_session_id(sid),
        "source": source,
        "owner": owner,
        "repo": session.get("repo") or "?",
        "ts": str(session.get("created_at") or session.get("start_time") or ""),
        "turns_ref": turns_ref,
        "turns": turns if keep_turns or turns_ref is None else None,
        "n_turns": len(turns),
        "sequence": None,
        "trace_hash": transcript_hash(turns),
        "human_turns": human_turn_count(turns),
        "substantial_human_turns": substantial_human_count(turns),
        "content_chars": sum(len(turn.get("text") or "") for turn in turns),
        "original_ids": [sid] if sid else [],
        "dedup_rules": [],
        "source_aliases": [source],
        "split": "train",
    }
    if turns_ref is not None and not keep_turns:
        drop_turns(record)
    return record


def normalize_specstory_session(session: dict) -> dict:
    return {
        "session_id": specstory_session_id(session),
        "repo": session.get("repo") or "?",
        "start_time": specstory_timestamp(session),
        "turns": session.get("turns") or [],
    }

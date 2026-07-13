#!/usr/bin/env python3
"""Rebuild web/app/v2data.json from the authoritative clean v2 cohort.

Reads hydrated private artifacts under .private/v2-58/ and writes public-safe
aggregate EDA stats for the website. Never includes session text, profiles,
or point payloads.
"""

from __future__ import annotations

import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / ".private" / "v2-58"
OUT = ROOT / "web" / "app" / "v2data.json"

SOURCE_LABEL = {
    "entire": "Entire checkpoints",
    "crawl": "GitHub .claude/.codex crawl",
    "dataclaw": "DataClaw (HF donors)",
}

TOK_BINS = [0, 10, 25, 50, 100, 200, 400, 800, 1600, 3200, 10**9]
TOK_LABELS = [
    "0-10",
    "10-25",
    "25-50",
    "50-100",
    "100-200",
    "200-400",
    "400-800",
    "800-1600",
    "1600-3200",
    "3200+",
]
PREV_BINS = [0, 5, 10, 20, 40, 80, 160, 10**9]


def normalize_source(source: str) -> str:
    # SWE-chat is the packaged HF parquet of the Entire stream — fold into Entire.
    if source == "swechat":
        return "entire"
    return source if source in SOURCE_LABEL else source


def approx_tokens(text: str) -> int:
    # Rough cl100k stand-in used only for public aggregates.
    return max(1, len(text) // 4) if text else 0


def mean_median(xs: list[float]) -> dict[str, float]:
    if not xs:
        return {"mean": 0.0, "median": 0.0}
    return {
        "mean": round(statistics.fmean(xs), 1),
        "median": round(statistics.median(xs), 1),
    }


def dist_stats(xs: list[float], name: str) -> dict:
    if not xs:
        return {"name": name, "min": 0, "median": 0, "mean": 0.0, "p90": 0, "max": 0}
    s = sorted(xs)
    n = len(s)
    p90 = s[min(n - 1, math.ceil(0.9 * n) - 1)]
    return {
        "name": name,
        "min": int(s[0]) if float(s[0]).is_integer() else round(s[0], 1),
        "median": int(statistics.median(s)) if float(statistics.median(s)).is_integer() else round(statistics.median(s), 1),
        "mean": round(statistics.fmean(s), 1),
        "p90": int(p90) if float(p90).is_integer() else round(p90, 1),
        "max": int(s[-1]) if float(s[-1]).is_integer() else round(s[-1], 1),
    }


def hist(values: list[float], bins: list[int]) -> list[int]:
    counts = [0] * (len(bins) - 1)
    for v in values:
        for i in range(len(bins) - 1):
            if bins[i] <= v < bins[i + 1]:
                counts[i] += 1
                break
    return counts


def dominant_source(sources: list[str]) -> str:
    # Prefer primary harvest channel; swechat is an Entire overlap tag.
    normed = [normalize_source(s) for s in sources]
    for key in ("entire", "crawl", "dataclaw"):
        if key in normed:
            return key
    return normed[0] if normed else "entire"


def main() -> None:
    manifest = json.loads((PRIVATE / "clean_manifest.json").read_text())
    cohort = json.loads((PRIVATE / "cohort.json").read_text())
    meta = json.loads((PRIVATE / "cohort.meta.json").read_text())
    build = json.loads((PRIVATE / "clean_build_report.json").read_text())

    users_meta = {u["user"]: u for u in manifest["users"]}
    cohort_users = {r["user"] for r in cohort}
    index_users = {
        line.strip()
        for line in (ROOT / ".private" / "indexes" / "v2_users.txt").read_text().splitlines()
        if line.strip()
    }
    assert set(users_meta) == cohort_users == index_users

    def session_ids(entries: list) -> set[str]:
        out: set[str] = set()
        for e in entries:
            if isinstance(e, str):
                out.add(e)
            elif isinstance(e, dict):
                if e.get("sid"):
                    out.add(e["sid"])
                for oid in e.get("original_ids") or []:
                    out.add(oid)
        return out

    train_ids = {u: session_ids(users_meta[u]["train_sessions"]) for u in users_meta}
    held_ids = {u: session_ids(users_meta[u]["held_sessions"]) for u in users_meta}

    # Per-user accumulators
    per = {
        u: {
            "user": u,
            "train_sess": 0,
            "eval_sess": 0,
            "train_turns": 0,
            "eval_turns": 0,
            "train_asst": 0,
            "eval_asst": 0,
            "tok_sum": 0,
            "tok_n": 0,
            "sources": list(users_meta[u]["sources"]),
        }
        for u in users_meta
    }

    sess_by_source = Counter()
    turns_by_source = Counter()
    asst_by_source = Counter()
    months: Counter[str] = Counter()
    tok_values: list[int] = []
    session_index: dict[str, dict] = {}

    times: list[str] = []
    n_sessions = 0
    n_user_turns = 0
    n_asst_turns = 0

    with (PRIVATE / "clean_sessions.jsonl").open() as f:
        for line in f:
            row = json.loads(line)
            user = row["user"]
            if user not in per:
                continue
            sid = row["session_id"]
            source = normalize_source(
                row.get("source") or dominant_source(row.get("source_aliases") or ["entire"])
            )
            turns = row.get("turns") or []
            n_user = sum(1 for t in turns if t.get("role") == "user")
            n_asst = sum(1 for t in turns if t.get("role") == "assistant")
            user_toks = [approx_tokens(t.get("text") or "") for t in turns if t.get("role") == "user"]

            split = None
            if sid in train_ids[user]:
                split = "train"
            elif sid in held_ids[user]:
                split = "eval"
            else:
                # Fall back to original_ids membership.
                orig = set(row.get("original_ids") or [])
                if orig & train_ids[user]:
                    split = "train"
                elif orig & held_ids[user]:
                    split = "eval"
                else:
                    continue

            n_sessions += 1
            n_user_turns += n_user
            n_asst_turns += n_asst
            sess_by_source[source] += 1
            turns_by_source[source] += n_user
            asst_by_source[source] += n_asst
            tok_values.extend(user_toks)

            st = row.get("start_time") or ""
            if st:
                times.append(st[:10])
                months[st[:7]] += 1

            p = per[user]
            if split == "train":
                p["train_sess"] += 1
                p["train_turns"] += n_user
                p["train_asst"] += n_asst
            else:
                p["eval_sess"] += 1
                p["eval_turns"] += n_user
                p["eval_asst"] += n_asst
            p["tok_sum"] += sum(user_toks)
            p["tok_n"] += len(user_toks)

            session_index[sid] = {
                "n_turns": len(turns),
                "user_turn_idxs": [i for i, t in enumerate(turns) if t.get("role") == "user"],
            }
            for oid in row.get("original_ids") or []:
                session_index[oid] = session_index[sid]

    # Prefer manifest turn counts (authoritative) when present.
    for u, p in per.items():
        p["train_turns"] = users_meta[u]["train_turns"]
        p["eval_turns"] = users_meta[u]["held_turns"]
        p["train_sess"] = len(users_meta[u]["train_sessions"])
        p["eval_sess"] = len(users_meta[u]["held_sessions"])

    per_user = []
    for u, p in per.items():
        tok_mean = round(p["tok_sum"] / p["tok_n"], 1) if p["tok_n"] else 0.0
        per_user.append(
            {
                "user": u,
                "train_sess": p["train_sess"],
                "eval_sess": p["eval_sess"],
                "train_turns": p["train_turns"],
                "eval_turns": p["eval_turns"],
                "tok_mean": tok_mean,
            }
        )

    def col(getter):
        return [getter(p) for p in per_user]

    dist = {
        "sessions": {
            "train": mean_median(col(lambda p: p["train_sess"])),
            "eval": mean_median(col(lambda p: p["eval_sess"])),
            "total": mean_median(col(lambda p: p["train_sess"] + p["eval_sess"])),
        },
        "user_turns": {
            "train": mean_median(col(lambda p: p["train_turns"])),
            "eval": mean_median(col(lambda p: p["eval_turns"])),
            "total": mean_median(col(lambda p: p["train_turns"] + p["eval_turns"])),
        },
        "asst_turns": {
            "train": mean_median([per[u]["train_asst"] for u in per]),
            "eval": mean_median([per[u]["eval_asst"] for u in per]),
        },
        "turns_per_sess": {
            "train": mean_median(
                [
                    (per[u]["train_turns"] / per[u]["train_sess"]) if per[u]["train_sess"] else 0
                    for u in per
                ]
            ),
            "eval": mean_median(
                [
                    (per[u]["eval_turns"] / per[u]["eval_sess"]) if per[u]["eval_sess"] else 0
                    for u in per
                ]
            ),
        },
        "tok_per_turn": {
            "pooled_mean": round(statistics.fmean(tok_values), 1) if tok_values else 0,
            "pooled_median": int(statistics.median(tok_values)) if tok_values else 0,
            "p90": int(sorted(tok_values)[min(len(tok_values) - 1, math.ceil(0.9 * len(tok_values)) - 1)])
            if tok_values
            else 0,
            "p99": int(sorted(tok_values)[min(len(tok_values) - 1, math.ceil(0.99 * len(tok_values)) - 1)])
            if tok_values
            else 0,
            "per_user_mean": mean_median([p["tok_mean"] for p in per_user]),
        },
    }

    # Provenance / source compare
    dom = Counter(dominant_source(per[u]["sources"]) for u in per)
    provenance = {
        "users_by_dominant": {SOURCE_LABEL.get(k, k): v for k, v in dom.most_common()},
        "sessions_by_source": {SOURCE_LABEL.get(k, k): v for k, v in sess_by_source.most_common()},
        "turns_by_source": {SOURCE_LABEL.get(k, k): v for k, v in turns_by_source.most_common()},
    }

    # Compact source_compare table columns
    cols = ["Entire checkpoints", "GitHub .claude/.codex crawl", "DataClaw (HF donors)"]
    src_keys = {
        "Entire checkpoints": "entire",
        "GitHub .claude/.codex crawl": "crawl",
        "DataClaw (HF donors)": "dataclaw",
    }

    def src_metric(metric: str) -> dict[str, float | int | str]:
        out: dict[str, float | int | str] = {}
        for label, key in src_keys.items():
            users = [u for u in per if dominant_source(per[u]["sources"]) == key]
            if metric == "developers (dominant)":
                out[label] = len(users)
            elif metric == "sessions":
                out[label] = sess_by_source.get(key, 0)
            elif metric == "user turns":
                out[label] = turns_by_source.get(key, 0)
            elif metric == "assistant turns":
                out[label] = asst_by_source.get(key, 0)
            elif metric == "user turns / session (mean)":
                s, t = sess_by_source.get(key, 0), turns_by_source.get(key, 0)
                out[label] = round(t / s, 1) if s else 0
            elif metric == "assistant / user turn":
                t, a = turns_by_source.get(key, 0), asst_by_source.get(key, 0)
                out[label] = round(a / t, 1) if t else 0
            elif metric == "train:eval turn %":
                tr = sum(per[u]["train_turns"] for u in users)
                ev = sum(per[u]["eval_turns"] for u in users)
                tot = tr + ev
                out[label] = f"{round(100 * tr / tot)}:{round(100 * ev / tot)}" if tot else "—"
            else:
                out[label] = "—"
        return out

    source_compare = {
        m: src_metric(m)
        for m in (
            "developers (dominant)",
            "sessions",
            "user turns",
            "assistant turns",
            "user turns / session (mean)",
            "assistant / user turn",
            "train:eval turn %",
        )
    }

    # Eval distribution from cohort points (+ session join when possible)
    prev_turns: list[int] = []
    ctx_tokens: list[int] = []
    points_per_dev: list[int] = []
    sess_per_dev: list[int] = []
    for row in cohort:
        pts = row.get("points") or []
        points_per_dev.append(len(pts))
        sess_ids = set()
        for pt in pts:
            pid = pt["point_id"]
            sid, _, idx_s = pid.partition("#")
            sess_ids.add(sid)
            turn_idx = int(idx_s) if idx_s.isdigit() else None
            meta_s = session_index.get(sid)
            if meta_s and turn_idx is not None:
                prev_turns.append(turn_idx)  # turns before this user message index
            else:
                # Fallback: rough depth from context size.
                prev_turns.append(max(1, approx_tokens(pt.get("context") or "") // 80))
            ctx_tokens.append(approx_tokens((pt.get("context") or "") + "\n" + (pt.get("prev_agent") or "")))
        sess_per_dev.append(len(sess_ids))

    eval_dist = {
        "prev_turns": dist_stats(prev_turns, "previous turns / eval point"),
        "prev_turns_hist": {"bins": PREV_BINS, "counts": hist(prev_turns, PREV_BINS)},
        "ctx_tokens": dist_stats(ctx_tokens, "context tokens / eval point"),
        "points_per_dev": dist_stats(points_per_dev, "eval points / developer"),
        "sess_per_dev": dist_stats(sess_per_dev, "held-out sessions feeding eval / developer"),
        "n_points": int(meta["points"]),
        "n_devs": int(meta["developers"]),
    }

    out = {
        "summary": {
            "n_users": int(meta["developers"]),
            "n_sessions": n_sessions if n_sessions else int(build.get("clean_sessions") or 0),
            "n_user_turns": n_user_turns,
            "n_assistant_turns": n_asst_turns,
            "n_points": int(meta["points"]),
            "policy_version": meta["policy_version"],
            "cohort_fingerprint": meta["cohort_fingerprint"],
            "time_min": min(times) if times else "",
            "time_max": max(times) if times else "",
        },
        "dist": dist,
        # Harness/model/version require raw scrapes; omitted for clean-cohort export.
        "harness": {},
        "harness_by_split": {},
        "model_families": {},
        "months": dict(sorted(months.items())),
        "tools": {},
        "tok_hist": {"labels": TOK_LABELS, "counts": hist(tok_values, TOK_BINS)},
        "per_user": sorted(per_user, key=lambda p: (-p["train_turns"], p["user"])),
        "versions": {"cc_by_month": {}, "cx_by_month": {}},
        "provenance": provenance,
        "source_compare": source_compare,
        "eval_dist": eval_dist,
        "notes": {
            "cohort": "Authoritative clean v2 harbor cohort (57 developers / 1216 points).",
            "tokens": "Token counts are approximate (chars/4); raw cl100k + harness/model tags need scrapes.",
            "source_manifest_users": build.get("source_manifest_users"),
            "retained_users": build.get("retained_users"),
            "dropped": len(build.get("dropped_below_clean_threshold") or []),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")) + "\n")
    print(
        f"wrote {OUT} ({OUT.stat().st_size} bytes) "
        f"users={out['summary']['n_users']} points={out['summary']['n_points']} "
        f"sessions={out['summary']['n_sessions']}"
    )


if __name__ == "__main__":
    main()

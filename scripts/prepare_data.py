#!/usr/bin/env python3
"""Build per-user digests (train) and holdout files (test) from SWE-chat.

For each user with >= MIN_SESSIONS trajectories:
  - chronological session split: last ~20% (>=1, <=8) sessions held out
  - data/digests/<slug>.json  : stats + sampled train prompts (distillation input)
  - data/holdout/<slug>.json  : full conversational turns of test sessions (validation input)
  - data/manifest.json        : slug <-> user_id mapping + split + volumes
"""

import argparse
import json
import re
from pathlib import Path

import pandas as pd

MIN_SESSIONS = 6
TEST_FRACTION = 0.2
MAX_TEST_SESSIONS = 8
MAX_FIRST_PROMPTS = 60          # session-opening prompts kept per user
MAX_MID_PROMPTS = 150           # non-opening prompts sampled per user
MAX_PUSHBACK_EXAMPLES = 30      # pushback prompts kept with preceding agent context
FIRST_PROMPT_WORDS = 250
MID_PROMPT_WORDS = 150
CONTEXT_WORDS = 80              # preceding assistant snippet for pushback examples
HOLDOUT_TURN_WORDS = 250


def slugify(user_id: str) -> str:
    slug = re.sub(r"[^a-z0-9_-]+", "-", user_id.lower()).strip("-")
    return slug or "user"


def truncate_words(text, n):
    if not isinstance(text, str):
        return ""
    words = text.split()
    if len(words) <= n:
        return text
    return " ".join(words[:n]) + f" […truncated, {len(words)} words total]"


def dist(series):
    """Value counts as {value: fraction} rounded, dropping NaN."""
    vc = series.dropna().value_counts(normalize=True)
    return {str(k): round(float(v), 3) for k, v in vc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--swe-chat", default="/home/ubuntu/SWE-chat")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "data"))
    ap.add_argument("--min-sessions", type=int, default=MIN_SESSIONS)
    args = ap.parse_args()

    src = Path(args.swe_chat)
    out = Path(args.out)
    (out / "digests").mkdir(parents=True, exist_ok=True)
    (out / "holdout").mkdir(parents=True, exist_ok=True)

    sessions = pd.read_parquet(
        src / "sessions.parquet",
        columns=["session_id", "user_id", "repo_id", "agent", "created_at",
                 "branch", "turn_count", "prompt_count", "duration_seconds",
                 "files_touched_count", "agent_percentage", "user_persona",
                 "session_success"],
    )
    sessions = sessions[sessions.user_id.notna()]
    counts = sessions.user_id.value_counts()
    eligible = counts[counts >= args.min_sessions].index
    sessions = sessions[sessions.user_id.isin(eligible)].copy()
    sessions = sessions.sort_values("created_at")

    print(f"eligible users: {len(eligible)}  sessions: {len(sessions)}")

    conv = pd.read_parquet(
        src / "conversations.parquet",
        columns=["session_id", "user_id", "turn_number", "conversation_turn_number",
                 "role", "turn_type", "is_conversational", "content", "timestamp",
                 "is_continuation", "is_first_turn", "word_count", "language",
                 "prompt_intent", "prompt_pushback", "repo_id"],
        filters=[("user_id", "in", list(eligible)),
                 ("is_conversational", "==", True)],
    )
    conv = conv.sort_values(["session_id", "turn_number"])
    print(f"conversational turns loaded: {len(conv)}")

    manifest = {}
    rng_seed = 7

    for user_id, user_sessions in sessions.groupby("user_id", sort=False):
        slug = slugify(user_id)
        # guard against slug collisions between distinct user_ids
        while slug in manifest and manifest[slug]["user_id"] != user_id:
            slug += "-x"
        user_sessions = user_sessions.sort_values("created_at")
        n_test = min(MAX_TEST_SESSIONS, max(1, int(len(user_sessions) * TEST_FRACTION)))
        train_ids = list(user_sessions.session_id[:-n_test])
        test_ids = list(user_sessions.session_id[-n_test:])

        uconv = conv[conv.session_id.isin(set(train_ids))]
        prompts = uconv[uconv.turn_type == "user_prompt"].copy()
        prompts = prompts[~prompts.is_continuation.fillna(False)]

        sess_meta = user_sessions.set_index("session_id")

        # --- stats fingerprint ---
        stats = {
            "user_id": user_id,
            "slug": slug,
            "n_sessions_total": int(len(user_sessions)),
            "n_sessions_train": len(train_ids),
            "n_sessions_test": len(test_ids),
            "agents": dist(user_sessions.agent),
            "repos": dist(user_sessions.repo_id),
            "date_range": [str(user_sessions.created_at.min())[:10],
                           str(user_sessions.created_at.max())[:10]],
            "n_prompts_train": int(len(prompts)),
            "prompt_words": {
                "median": float(prompts.word_count.median()) if len(prompts) else None,
                "p90": float(prompts.word_count.quantile(0.9)) if len(prompts) else None,
                "max": float(prompts.word_count.max()) if len(prompts) else None,
            },
            "languages": dist(prompts.language),
            "intent_distribution": dist(prompts.prompt_intent),
            "pushback_distribution": dist(prompts.prompt_pushback),
            "session_turns_median": float(user_sessions.turn_count.median()),
            "session_duration_median_s": float(user_sessions.duration_seconds.median()),
            "agent_code_percentage_median": (
                float(user_sessions.agent_percentage.median())
                if user_sessions.agent_percentage.notna().any() else None),
            "annotated_personas": dist(user_sessions.user_persona),
        }

        # --- session-opening prompts (task requests) ---
        firsts = prompts[prompts.is_first_turn.fillna(False)]
        firsts = firsts.head(MAX_FIRST_PROMPTS)
        opening = [
            {"repo": str(r.repo_id), "intent": _s(r.prompt_intent),
             "text": truncate_words(r.content, FIRST_PROMPT_WORDS)}
            for r in firsts.itertuples()
        ]

        # --- mid-session prompts, stratified sample across sessions ---
        mids = prompts[~prompts.is_first_turn.fillna(False)]
        if len(mids) > MAX_MID_PROMPTS:
            mids = mids.sample(MAX_MID_PROMPTS, random_state=rng_seed).sort_values(
                ["session_id", "turn_number"])
        mid = [
            {"intent": _s(r.prompt_intent), "pushback": _s(r.prompt_pushback),
             "text": truncate_words(r.content, MID_PROMPT_WORDS)}
            for r in mids.itertuples()
        ]

        # --- pushback prompts with the assistant turn they react to ---
        pb = prompts[prompts.prompt_pushback.notna()
                     & (prompts.prompt_pushback != "non_pushback")]
        pb = pb.head(MAX_PUSHBACK_EXAMPLES)
        by_session = {sid: g for sid, g in uconv.groupby("session_id")}
        pushback = []
        for r in pb.itertuples():
            g = by_session.get(r.session_id)
            prev = g[(g.turn_number < r.turn_number) & (g.role == "assistant")]
            pushback.append({
                "type": _s(r.prompt_pushback),
                "agent_said": truncate_words(
                    prev.content.iloc[-1] if len(prev) else "", CONTEXT_WORDS),
                "user_replied": truncate_words(r.content, MID_PROMPT_WORDS),
            })

        digest = {"stats": stats, "opening_prompts": opening,
                  "mid_session_prompts": mid, "pushback_examples": pushback}
        (out / "digests" / f"{slug}.json").write_text(
            json.dumps(digest, indent=1, ensure_ascii=False))

        # --- holdout: full conversational turn sequences of test sessions ---
        tconv = conv[conv.session_id.isin(set(test_ids))]
        ho_sessions = []
        for sid in test_ids:
            g = tconv[tconv.session_id == sid]
            if not len(g):
                continue
            meta = sess_meta.loc[sid]
            ho_sessions.append({
                "session_id": sid,
                "repo": str(meta.repo_id),
                "agent": str(meta.agent),
                "turns": [
                    {"role": str(r.role),
                     "turn": _i(r.conversation_turn_number),
                     "is_continuation": bool(r.is_continuation) if pd.notna(r.is_continuation) else False,
                     "language": _s(r.language),
                     "pushback": _s(r.prompt_pushback),
                     "text": truncate_words(r.content, HOLDOUT_TURN_WORDS)}
                    for r in g.itertuples()
                ],
            })
        (out / "holdout" / f"{slug}.json").write_text(
            json.dumps({"user_id": user_id, "slug": slug, "sessions": ho_sessions},
                       indent=1, ensure_ascii=False))

        manifest[slug] = {
            "user_id": user_id,
            "n_sessions": int(len(user_sessions)),
            "train_sessions": len(train_ids),
            "test_sessions": len(test_ids),
            "n_prompts_train": int(len(prompts)),
            "digest_kb": round((out / "digests" / f"{slug}.json").stat().st_size / 1024),
            "holdout_kb": round((out / "holdout" / f"{slug}.json").stat().st_size / 1024),
        }
        print(f"  {slug:30s} sessions={len(user_sessions):4d} "
              f"digest={manifest[slug]['digest_kb']:5d}KB holdout={manifest[slug]['holdout_kb']:5d}KB")

    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"\nwrote {len(manifest)} users -> {out}")


def _s(v):
    return None if pd.isna(v) else str(v)


def _i(v):
    return None if pd.isna(v) else int(v)


if __name__ == "__main__":
    main()

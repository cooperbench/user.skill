"""Rebuild each test developer's chronological TRAIN-session user turns from the SWE-chat parquet.

Mirrors scripts/prepare_data.py exactly: sessions sorted by created_at, last min(8, max(1, 20%))
sessions held out; prompts = turn_type=="user_prompt" and not is_continuation. Emits
experiments/condagree_multi/train_turns.json with per-turn metadata (session order, is_first_turn,
intent, pushback, prev_agent) so both the raw-history sweep and the K-digest distillation arm are
reproducible without the parquet.
"""
import glob
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate as V  # noqa: E402

SNAP = sorted(glob.glob(str(Path.home() / ".cache/huggingface/hub/datasets--SALT-NLP--SWE-chat/snapshots/*/sessions.parquet")))[0].rsplit("/", 1)[0]
MAX_TEST, FRAC = 8, 0.2
TURN_WORD_CAP = 200

test = json.loads((HERE / "splits.json").read_text())["test"]["qualifying_users"]
slug2uid = {}
for f in glob.glob(str(ROOT / "data/digests/*.json")):
    d = json.load(open(f))
    slug2uid[d["stats"]["slug"]] = d["stats"]["user_id"]

s = pd.read_parquet(f"{SNAP}/sessions.parquet", columns=["session_id", "user_id", "repo_id", "created_at"])
conv = pd.read_parquet(f"{SNAP}/conversations.parquet",
                       columns=["session_id", "turn_number", "role", "turn_type", "content",
                                "is_continuation", "is_first_turn", "word_count",
                                "prompt_intent", "prompt_pushback"])
conv = conv.sort_values(["session_id", "turn_number"])

out = {}
for slug in test:
    uid = slug2uid[slug]
    us = s[s.user_id == uid].sort_values("created_at")
    n_test = min(MAX_TEST, max(1, int(len(us) * FRAC)))
    train = us.iloc[:-n_test]
    train_ids = list(train.session_id)
    sess_order = {sid: i for i, sid in enumerate(train_ids)}
    sess_repo = dict(zip(train.session_id, train.repo_id))
    uc = conv[conv.session_id.isin(set(train_ids))]
    by_sess = {sid: g for sid, g in uc.groupby("session_id")}
    turns = []
    for sid in train_ids:  # chronological by session start, then turn order
        g = by_sess.get(sid)
        if g is None:
            continue
        for r in g.itertuples():
            if r.turn_type != "user_prompt" or (r.is_continuation is True):
                continue
            prev = g[(g.turn_number < r.turn_number) & (g.role == "assistant")]
            turns.append({
                "session_idx": sess_order[sid], "repo": str(sess_repo.get(sid, "")),
                "is_first_turn": bool(r.is_first_turn) if r.is_first_turn is not None else False,
                "intent": None if pd.isna(r.prompt_intent) else str(r.prompt_intent),
                "pushback": None if pd.isna(r.prompt_pushback) else str(r.prompt_pushback),
                "prev_agent": V.truncate_words(prev.content.iloc[-1] if len(prev) else "", 120),
                "text": V.truncate_words(r.content or "", TURN_WORD_CAP),
                "words": int(r.word_count or 0),
            })
    out[slug] = {"n_train_sessions": len(train_ids), "n_train_turns": len(turns), "turns": turns}
    print(f"{slug:24s} sessions={len(train_ids):4d} turns={len(turns):5d}")

dst = HERE / "experiments" / "condagree_multi" / "train_turns.json"
dst.write_text(json.dumps(out, ensure_ascii=False))
print(f"\nwrote {dst} ({dst.stat().st_size/1e6:.1f} MB)")

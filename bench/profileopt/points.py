"""Shared helpers for the SWESimBench eval.

- `all_points_for(slug)`: every valid held-out prediction point for a developer, grouped by session.
- `clean_msg(text)`: strip role labels / wrapping quotes a model may add despite the output contract.

(Extracted from the earlier v0 / v0.1 move-fidelity evals, which the benchmark no longer depends on.)
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate as V  # noqa: E402


def clean_msg(t):
    """Strip role labels / wrapping quotes a model may add despite the output contract."""
    s = (t or "").strip()
    for tag in ("DEVELOPER:", "USER:", "Developer:", "User:", "Message:"):
        if s.startswith(tag):
            s = s[len(tag):].strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1].strip()
    return s


def all_points_for(slug):
    """All valid held-out prediction points for a developer (uncapped), grouped by session.

    A point is a real developer turn worth predicting: a user message (not a continuation) that
    is an action target, is an interrupt or has >=3 words, and follows at least one assistant turn.
    """
    ho = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
    by_sess = defaultdict(list)
    for s in ho["sessions"]:
        turns = s["turns"]
        for i, t in enumerate(turns):
            if t["role"] != "user" or t.get("is_continuation"):
                continue
            if not V.is_user_action_target(t.get("text")):
                continue
            if not (V.is_interrupt(t.get("text")) or len((t.get("text") or "").split()) >= 3):
                continue
            if not any(p["role"] == "assistant" for p in turns[:i]):
                continue
            ctx = turns[max(0, i - V.CONTEXT_TURNS):i]
            prev_agent = next((p["text"] for p in reversed(ctx) if p["role"] == "assistant"), "")
            by_sess[s["session_id"]].append({
                "slug": slug, "session_id": s["session_id"], "repo": s["repo"],
                "turn_index": i, "real": turns[i]["text"], "context": ctx,
                "prev_agent": prev_agent, "point_id": f"{s['session_id']}#{i}"})
    return by_sess

#!/usr/bin/env python3
"""Bucket each user's REAL training messages by speech-act MOVE, for move-matched
few-shot voice calibration at generation time. Zero LLM calls — reuses the dataset's
prompt_intent / prompt_pushback annotations already in the digests.

Writes users/<slug>/move_exemplars.json: {move: [verbatim user messages]}.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as V  # _INTENT_MOVE, _PB_MOVE, is_interrupt

ROOT = Path(__file__).resolve().parent.parent
MAX_PER_MOVE = 12
MAX_WORDS = 60

# noise to exclude — not authored user voice
_JUNK = re.compile(
    r"<system_instruction|tool loaded\.?$|this session is being continued|"
    r"<command-|local-command|base directory for this skill|^\[request interrupted",
    re.I)


def clean(text):
    s = (text or "").strip()
    if not s or _JUNK.search(s):
        return None
    if s.count("\n") > 6 or len(s.split()) > MAX_WORDS:  # long pastes/specs: not voice exemplars
        return None
    return s


def move_of(intent, pushback, text):
    if V.is_interrupt(text):
        return "interrupt"
    if pushback and pushback != "non_pushback" and pushback in V._PB_MOVE:
        return V._PB_MOVE[pushback]
    if intent:
        return V._INTENT_MOVE.get(intent, "approve_proceed")
    return None


def build(slug):
    digest = json.loads((ROOT / "data" / "digests" / f"{slug}.json").read_text())
    buckets = {}
    seen = set()
    lengths = {}  # move -> [word counts] over ALL (non-junk) messages of that move

    def add(move, text):
        t = clean(text)
        if not t:
            return
        lengths.setdefault(move, []).append(len(t.split()))
        if t.lower() in seen:
            return
        buckets.setdefault(move, [])
        if len(buckets[move]) < MAX_PER_MOVE:
            buckets[move].append(t)
            seen.add(t.lower())

    for p in digest.get("opening_prompts", []):
        mv = move_of(p.get("intent"), None, p.get("text"))
        if mv:
            add(mv, p["text"])
    for p in digest.get("mid_session_prompts", []):
        mv = move_of(p.get("intent"), p.get("pushback"), p.get("text"))
        if mv:
            add(mv, p["text"])
    for p in digest.get("pushback_examples", []):
        mv = V._PB_MOVE.get(p.get("type"), "pushback")
        add(mv, p.get("user_replied"))

    import statistics as _st
    payload = {"exemplars": buckets,
               "length_median": {m: int(_st.median(v)) for m, v in lengths.items() if v}}
    out = ROOT / "users" / slug / "move_exemplars.json"
    out.write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    return {m: len(v) for m, v in buckets.items()}


def main():
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text())
    slugs = sys.argv[1:] or list(manifest)
    total = 0
    for slug in slugs:
        if not (ROOT / "users" / slug).exists():
            continue
        counts = build(slug)
        total += 1
        if len(slugs) <= 12:
            print(f"{slug:28s} {counts}")
    print(f"built move_exemplars for {total} users")


if __name__ == "__main__":
    main()

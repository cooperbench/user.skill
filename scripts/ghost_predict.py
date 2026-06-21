#!/usr/bin/env python3
"""The opencode "ghost-text" next-message predictor, as a baseline for user.skill.

This is a faithful Python port of the production predictor that ships in opencode
(`packages/opencode/src/session/ghost-text.ts` + the `predict` flow in
`session/prompt.ts`). In the product it powers inline ghost-text suggestions and an
opt-in auto-pilot; here it serves as a *baseline condition* for the held-out
next-message prediction task in `validate.py`.

It does two things, mirroring the product 1:1:

1. SIMULATE — given the conversation so far (and, optionally, a short user
   profile), predict the single most likely next message the user would type.
2. CLASSIFY — label that predicted message as a `continuation` of the current
   task or a `new_task` pitch (the signal the product uses to decide whether to
   auto-send). Defaults to `new_task` on unparseable output (fail-safe).

Two key differences from the product, by design:
  - The product draws a `profile` / `no_profile` simulator variant per turn and
    runs on a small/fast model. Here the profile is an explicit argument (so the
    benchmark can run the pure no-profile predictor, or feed a user folder), and
    the model defaults to the harness GEN_MODEL for an apples-to-apples baseline.
  - opencode streams real prior chat messages to the model; the `claude -p`
    harness used here renders the conversation into a single prompt, matching how
    the other validate.py conditions are built.

Usage
-----
  # Quick self-test (one prediction on a built-in toy conversation):
  python3 scripts/ghost_predict.py --demo

  # Generate ghost rows for held-out users into a generations file that
  # validate.py --ghost --score-only can then score alongside the other conditions:
  python3 scripts/ghost_predict.py --slugs 135yshr abc --out results/generations_inline.jsonl

  # Programmatic:
  from ghost_predict import predict
  predict([{"role": "user", "text": "..."}, {"role": "assistant", "text": "..."}])
  # -> {"text": "now add tests", "kind": "continuation"}
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Run from anywhere: make sibling scripts (validate.py) importable.
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Reuse the harness's claude-CLI runner and helpers so ghost predictions are
# produced and formatted exactly like every other condition. validate.py guards
# its entrypoint with `if __name__ == "__main__"`, so importing it is side-effect free.
from validate import (  # noqa: E402
    GEN_MODEL,
    _context_block,
    is_cli_failure,
    pick_points,
    run_claude,
    truncate_words,
)

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Ported, verbatim where possible, from ghost-text.ts
# ---------------------------------------------------------------------------

# Hidden config in the product: probability of drawing the profile-based variant
# on a given turn. Exposed here for reference; the benchmark passes `profile`
# explicitly instead of drawing.
PROFILE_PROBABILITY = 0.8

# The product's sample profile (only the model ever sees it). Kept for reference
# and as the default when --profile sample is requested.
SAMPLE_PROFILE = (
    "- Senior backend engineer, very comfortable with TypeScript, Go, and shell.\n"
    "- Writes terse, direct prompts; rarely uses pleasantries.\n"
    "- Tends to iterate: asks for a change, then asks to run/verify it, then asks for the next step.\n"
    "- Prefers minimal diffs and asks for tests when touching core logic.\n"
    '- Often follows up with "now do X", "also handle Y", or "run it".'
)


def simulator_system(profile=None, typed="", deleted="", instruction=""):
    """Port of ghost-text.ts `template()` + `renderForModel()`.

    `profile` None/"" => the no_profile variant. The "prior messages" line is
    adapted to "below" since the conversation is rendered into the prompt here.
    """
    instruction_line = (
        f"Additional instruction from the user: {instruction.strip()}" if instruction.strip() else ""
    )
    lines = [
        "You are simulating a specific human user in an interactive coding session with an AI assistant.",
        "Predict the single most likely next message this user would type.",
        f"\nUser profile:\n{profile}" if profile else "",
        instruction_line,
        f'The user has already started typing their next message: "{typed}"',
        f'During this draft the user has deleted: "{deleted}"',
        "",
        "The conversation so far is provided below. Output only the message text the user",
        "would send next — no preamble, no quotes, no explanation. Keep it short and natural, matching the",
        "user's style. If the user already typed something, your output must be the full intended message",
        "(including what they typed). If no useful prediction is possible, output nothing.",
    ]
    return "\n".join(line for line in lines if line != "")


def classifier_system():
    """Port of ghost-text.ts `classifierSystem()` (continuation-leaning tie-breaker)."""
    return "\n".join([
        "You are analyzing an interactive coding session between a user and an AI assistant.",
        "You are given the conversation so far and a candidate for the user's next message.",
        "Classify whether that candidate CONTINUES the task already in progress or pitches a NEW task or feature.",
        "- CONTINUATION: iterates on the current work — e.g. run it, verify, fix an error, tweak, add tests for",
        "  what was just built, or proceed to the obvious next sub-step of the same task.",
        "- NEW_TASK: introduces distinct new work, a new feature, or a change of direction that is not part of",
        "  the task currently in progress.",
        "Treat a message as NEW_TASK only when it clearly starts unrelated work; if it plausibly keeps moving",
        "the current task forward, prefer CONTINUATION. When genuinely uncertain, answer CONTINUATION.",
        "Output exactly one word: CONTINUATION or NEW_TASK. No punctuation, no explanation.",
    ])


_THINK_RE = re.compile(r"<think>.*?</think>\s*", re.S)


def parse_kind(raw):
    """Port of ghost-text.ts `parseKind()`. Fail-safe: defaults to new_task."""
    cleaned = _THINK_RE.sub("", raw or "").lower()
    if re.search(r"\bcontinuation\b", cleaned) and not re.search(r"\bnew_task\b", cleaned):
        return "continuation"
    return "new_task"


def _clean(text):
    return _THINK_RE.sub("", text or "").strip()


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def _render_convo(messages):
    """Render [{'role','text'}] as the same DEVELOPER/AGENT block the harness uses."""
    out = []
    for m in messages:
        who = "DEVELOPER" if m.get("role") == "user" else "AGENT"
        out.append(f"[{who}]: {truncate_words(m.get('text', ''), 200)}")
    return "\n\n".join(out)


def _generate(system, convo_block, directive, runner, model):
    prompt = (
        f"{system}\n\n<conversation>\n{convo_block}\n</conversation>\n\n{directive}"
    )
    out = runner(prompt, model)
    return "" if is_cli_failure(out) else out


def _predict_from_block(convo_block, profile=None, classify=True, typed="", deleted="",
                        instruction="", model=GEN_MODEL, runner=run_claude):
    """Core: simulate then (optionally) classify, given a rendered conversation block."""
    directive = (
        f'I have already started typing: "{typed}". Output only my full intended next message.'
        if typed.strip()
        else "Output only the single most likely next message I would send next."
    )
    text = _clean(_generate(simulator_system(profile, typed, deleted, instruction),
                            convo_block, directive, runner, model))
    kind = ""
    if classify and text:
        directive2 = f'Candidate next message: "{text}"\nClassify it.'
        raw = _generate(classifier_system(), convo_block, directive2, runner, model)
        kind = parse_kind(raw)
    return {"text": text, "kind": kind}


def predict(messages, profile=None, classify=True, model=GEN_MODEL, runner=run_claude):
    """Predict the user's next message from a conversation.

    messages: [{"role": "user"|"assistant", "text": str}, ...] in chronological order.
    Returns {"text": <predicted message>, "kind": "continuation"|"new_task"|""}.
    """
    return _predict_from_block(_render_convo(messages), profile=profile, classify=classify,
                               model=model, runner=runner)


def predict_point(point, profile=None, model=GEN_MODEL, runner=run_claude):
    """Adapter for a validate.py `point` (uses its exact _context_block for parity)."""
    return _predict_from_block(_context_block(point), profile=profile, classify=True,
                               model=model, runner=runner)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_DEMO = [
    {"role": "user", "text": "Write a TypeScript function that reverses a string."},
    {"role": "assistant", "text": "Here's `reverse(s: string)`: return s.split('').reverse().join('')."},
]


def _resolve_profile(kind, slug=None):
    if kind == "none":
        return None
    if kind == "sample":
        return SAMPLE_PROFILE
    if kind == "folder" and slug:
        d = ROOT / "users" / slug
        parts = []
        for f in ("USER.md", "STYLE.md", "PREFERENCES.md", "PERSONA.md", "PROJECTS.md"):
            p = d / f
            if p.exists():
                parts.append(f"--- {f} ---\n{p.read_text()}")
        return truncate_words("\n\n".join(parts), 8000) if parts else None
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--demo", action="store_true", help="run one prediction on a built-in toy conversation")
    ap.add_argument("--slugs", nargs="*", default=None, help="held-out user slugs (reads data/holdout/<slug>.json)")
    ap.add_argument("--out", default=None, help="append ghost generation rows (jsonl) for validate.py --ghost to score")
    ap.add_argument("--profile", choices=["none", "sample", "folder"], default="none",
                    help="none: pure no-profile predictor (default); sample: opencode's built-in persona; "
                         "folder: feed the user's own distilled folder as the profile")
    ap.add_argument("--model", default=GEN_MODEL, help=f"generation model (default {GEN_MODEL}; "
                                                       "the product runs this on a small/fast model)")
    ap.add_argument("--no-classify", action="store_true", help="skip the continuation/new_task classifier")
    args = ap.parse_args()

    if args.demo:
        res = predict(_DEMO, profile=_resolve_profile(args.profile), classify=not args.no_classify,
                      model=args.model)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if not args.slugs:
        ap.error("provide --demo or --slugs")

    out_path = Path(args.out) if args.out else ROOT / "results" / "generations_inline.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with out_path.open("a") as fh:
        for slug in args.slugs:
            holdout = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
            points = pick_points(holdout)
            print(f"{slug}: {len(points)} points", flush=True)
            for point in points:
                res = predict_point(point, profile=_resolve_profile(args.profile, slug), model=args.model)
                rec = {"slug": slug, "point_id": f"{point['session_id']}#{point['turn_index']}",
                       "cond": "ghost", "repo": point["repo"], "real": point["real"],
                       "generated": res["text"], "kind": res["kind"]}
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                written += 1
                print(f"  [{written}] {rec['point_id']} kind={res['kind']} ({len(res['text'].split())}w)",
                      flush=True)
    print(f"wrote {written} ghost rows -> {out_path}")


if __name__ == "__main__":
    main()

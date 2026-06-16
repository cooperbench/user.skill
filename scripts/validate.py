#!/usr/bin/env python3
"""Validate distilled user folders by held-out next-message prediction.

For each validation user, for each held-out session, we pick prediction points
(real user turns with prior context). A role-play agent (claude -p) sees the real
conversation up to that point and produces the user's next message under three
conditions: with the user's distilled folder, with no folder, with a wrong user's
folder. We score generated vs. real with embedding cosine similarity, an LLM
judge (content + style), and a length-ratio fingerprint.

Usage:
  python3 scripts/validate.py --users 10            # stratified selection
  python3 scripts/validate.py --slugs a b c         # explicit users
Results stream to results/generations.jsonl (resumable); scored output goes to
results/validation_results.json.
"""

import argparse
import hashlib
import json
import re
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
GEN_MODEL = "claude-sonnet-4-6"
JUDGE_MODEL = "claude-haiku-4-5-20251001"
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # users prompt in several languages
CONDITIONS = ["distilled", "generic", "wrong"]
MAX_POINTS_PER_SESSION = 3
MAX_SESSIONS_PER_USER = 4
CONTEXT_TURNS = 14
CONTEXT_TURN_WORDS = 200
FOLDER_WORD_CAP = 8000
TIMEOUT_S = 240

FOLDER_FILES = ["USER.md", "STYLE.md", "PREFERENCES.md", "PERSONA.md", "PROJECTS.md"]


def truncate_words(text, n):
    words = (text or "").split()
    return " ".join(words[:n]) + (" […]" if len(words) > n else "")


def load_folder_text(slug):
    d = ROOT / "users" / slug
    parts = []
    for f in FOLDER_FILES:
        p = d / f
        if p.exists():
            parts.append(f"--- {f} ---\n{p.read_text()}")
    for p in sorted((d / "skills").glob("*.md")) if (d / "skills").exists() else []:
        parts.append(f"--- skills/{p.name} ---\n{p.read_text()}")
    return truncate_words("\n\n".join(parts), FOLDER_WORD_CAP)


def is_interrupt(text):
    """The user cutting the agent off — a genuine user ACTION the simulator can take."""
    s = (text or "").strip()
    return ("interrupted by user" in s.lower()
            or s.upper().startswith("[INTERRUPT"))


def is_user_action_target(text):
    """True if the held-out turn is something the USER actually did (a typed prompt, a
    slash command, or an interrupt) — False for harness/tool artifacts that merely have
    role=user (injected skill/doc content, rendered command output, auto-continue resumes)."""
    s = (text or "").strip()
    low = s.lower()
    if not s:
        return False
    if is_interrupt(s):
        return True
    # harness/tool artifacts — not authored by the user
    if s.startswith("<") and ("command-" in s or "local-command" in low):
        return False
    if any(x in low for x in (
            "base directory for this skill", "for detailed examples and advanced patterns",
            "see files in `references", ".claude/plugins/cache", "<system-reminder")):
        return False
    if "continue from where you left off" in low and len(s.split()) <= 8:
        return False
    return True


def pick_points(holdout):
    """Choose prediction points: USER ACTIONS with >=1 assistant turn before them.
    Keeps genuine prompts and interrupts; drops harness/tool artifacts (see
    is_user_action_target). Interrupt points have a short real text, so they bypass the
    >=3-word floor."""
    points = []
    for sess in holdout["sessions"][:MAX_SESSIONS_PER_USER]:
        turns = sess["turns"]
        idxs = [i for i, t in enumerate(turns)
                if t["role"] == "user" and not t.get("is_continuation")
                and any(p["role"] == "assistant" for p in turns[:i])
                and is_user_action_target(t.get("text"))
                and (is_interrupt(t.get("text")) or len((t.get("text") or "").split()) >= 3)]
        if not idxs:
            continue
        if len(idxs) > MAX_POINTS_PER_SESSION:  # spread across the session
            step = len(idxs) / MAX_POINTS_PER_SESSION
            idxs = [idxs[int(k * step)] for k in range(MAX_POINTS_PER_SESSION)]
        for i in idxs:
            ctx = turns[max(0, i - CONTEXT_TURNS):i]
            prev_agent = next((t["text"] for t in reversed(ctx) if t["role"] == "assistant"), "")
            points.append({
                "session_id": sess["session_id"], "repo": sess["repo"],
                "turn_index": i, "real": turns[i]["text"],
                "context": ctx, "prev_agent": prev_agent,
            })
    return points


def _context_block(point):
    ctx_lines = []
    for t in point["context"]:
        who = "DEVELOPER" if t["role"] == "user" else "AGENT"
        ctx_lines.append(f"[{who}]: {truncate_words(t['text'], CONTEXT_TURN_WORDS)}")
    return "\n\n".join(ctx_lines)


_TASK = (
    "Write the developer's NEXT message to the agent. Output ONLY the literal text "
    "the developer would type — their language, length, casing, typos and all. "
    "No quotes, no commentary, no role labels."
)


def build_prompt(point, folder_text):
    """INLINE mode: the folder contents are pasted into the prompt (controlled experiment)."""
    profile = (
        f"<user_profile>\n{folder_text}\n</user_profile>\n\n"
        "You are role-playing the developer described in the profile above. "
        if folder_text else
        "You are role-playing a software developer. "
    )
    return (
        f"{profile}"
        f"The developer is using an AI coding agent in the repository `{point['repo']}`. "
        f"The session so far:\n\n<conversation>\n{_context_block(point)}\n</conversation>\n\n{_TASK}"
    )


def _load_move_exemplars(folder_path, move, k=3, seed=""):
    """Up to k of the user's own real messages of this move, for few-shot voice calibration.
    Deterministic per (folder, move, seed) so own/wrong stay reproducible."""
    if not folder_path:
        return []
    p = ROOT / folder_path / "move_exemplars.json"
    if not p.exists():
        return []
    pool = json.loads(p.read_text()).get(move, [])
    if len(pool) <= k:
        return pool
    h = int(hashlib.sha256(f"{folder_path}|{move}|{seed}".encode()).hexdigest(), 16)
    start = h % len(pool)
    return [pool[(start + i) % len(pool)] for i in range(k)]


def build_folder_prompt(point, folder_path, target_move=None, use_exemplars=False):
    """FOLDER mode: the agent is pointed at the folder and must READ it itself
    (exercises the real roleplay-user skill / product flow).

    Improved simulator: intent-first (ground the message in the live conversation state),
    voice-not-script (use the folder for HOW they write, never recycle catchphrases), and
    leak-proof (output only the message, no narration of reasoning).

    If target_move is set (move-conditioned generation, Stage 2), the move is fixed for the
    simulator and it only has to render that move in the user's voice."""
    repo = point["repo"]
    repo_clause = ""
    if point.get("repo_path"):
        repo_clause = (
            f" A checkout of the repository is at `{point['repo_path']}` — you may read it "
            "(Read/Glob/Grep) to ground yourself in the project's real state, exactly as the "
            "developer can see their own codebase."
        )
    shared = ROOT / "simulator" / "AGENT.md"
    shared_clause = ""
    if folder_path and shared.exists():
        shared_clause = (
            "First read the shared simulator manual at `simulator/AGENT.md` and the move playbooks in "
            "`simulator/skills/`. It tells you how to role-play any developer: choose the right "
            "conversational MOVE (new_work / refine_redirect / pushback / bug_report / approve_proceed "
            "/ question / interrupt) at this user's rate, then write it in their voice. "
        )
    move_clause = ""
    if target_move:
        move_clause = (
            f"\n\nYour move here is fixed: **{target_move}**. Do not choose a different move — make "
            f"exactly a `{target_move}` message, expressed naturally in this developer's voice and "
            f"grounded in the situation. "
            'If the move is `interrupt`, output exactly "[INTERRUPT]" (optionally followed by the '
            "short thing they'd snap). "
        )
        # few-shot: this user's OWN real messages of this move (move-matched voice calibration)
        seed = f"{point['session_id']}#{point['turn_index']}"
        exemplars = _load_move_exemplars(folder_path, target_move, seed=seed) if use_exemplars else []
        if exemplars:
            ex = "\n".join(f"- {truncate_words(e, 50)}" for e in exemplars)
            move_clause += (
                f"\n\nHere are real `{target_move}` messages this same developer has written before — "
                f"match THIS register (length, casing, bluntness), but write a NEW message for the "
                f"current situation, do not copy them:\n{ex}\n"
            )
    if folder_path:
        head = (
            f"{shared_clause}"
            f"You ARE the developer in the user folder at `{folder_path}`. Read it — USER.md, then "
            f"STYLE.md, PREFERENCES.md and stats.json (their voice and move rates), then PERSONA.md, "
            f"PROJECTS.md and skills/*.md. "
        )
        if target_move:
            guide = (
                f"Now produce their NEXT message.{move_clause}Write it in their voice (HOW they talk, "
                "never recycling their stock phrases); ground new work and bug reports in the real "
                "project state.\n"
            )
        else:
            guide = (
                "Now produce their NEXT message, following the manual: pick the MOVE this developer would "
                "actually make here (do NOT default to approving — most real turns are new work, "
                "redirects, pushback, bug reports, questions, or interrupts; match this user's rates from "
                "stats.json), then write it in their voice (HOW they talk, never recycling their stock "
                "phrases). Ground new work and bug reports in the real project state.\n"
                "To interrupt, output exactly \"[INTERRUPT]\" (optionally followed by what they'd type).\n"
            )
    else:
        head = "You ARE a generic software developer driving this session toward your goals. "
        guide = (f"Produce your next message.{move_clause}" if target_move else
                 ("Produce your next message — the move you'd actually make (often new work, a "
                  "redirect, a question, or a problem you noticed, not just approval), grounded in the "
                  'project state. To interrupt, output exactly "[INTERRUPT]". '))
    return (
        f"{head}You are using an AI coding agent in the repository `{repo}`.{repo_clause}\n\n"
        f"<conversation>\n{_context_block(point)}\n</conversation>\n\n{guide}\n"
        "Output ONLY the literal message text the developer would type next — their exact idiom, "
        "casing and typos. No quotes, no role labels, no narration, and no explanation of your "
        "reasoning. Just the message."
    )


# Substrings emitted by the CLI itself (not by a model) that must never be saved as a
# prediction. Matched case-insensitively anywhere in the output.
_CLI_FAILURE_MARKERS = (
    "hit your session limit",
    "usage limit reached",
    "reached max turns",
    "rate limit",
    "overloaded",
    "service unavailable",
    "internal server error",
)


def is_cli_failure(text):
    """True if the output is empty or a CLI-level error rather than a real generation."""
    if not text or not text.strip():
        return True
    low = text.lower()
    if text.startswith("Error:"):
        return True
    return any(m in low for m in _CLI_FAILURE_MARKERS)


def run_claude(prompt, model, timeout=TIMEOUT_S, read_folder=False, retries=2):
    if read_folder:
        # agent reads the folder (and, when provided, the repo checkout); read-only tools.
        cmd = ["claude", "-p", prompt, "--model", model,
               "--allowedTools", "Read,Glob,Grep", "--permission-mode", "acceptEdits",
               "--max-turns", "16"]
    else:
        # inline mode: no tools needed. max-turns 8 so that if the model makes a stray
        # (blocked) tool attempt before answering, it still has room to emit the text turn
        # instead of erroring out with "Reached max turns".
        cmd = ["claude", "-p", prompt, "--model", model,
               "--disallowedTools", "Read,Write,Edit,Bash,Glob,Grep,Task,WebFetch,WebSearch,NotebookEdit",
               "--max-turns", "8"]
    out = ""
    for attempt in range(retries):
        res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        out = (res.stdout or "").strip()
        if not is_cli_failure(out):
            return out
        # transient CLI failure (limit/overload): brief backoff before retrying
        if attempt < retries - 1:
            time.sleep(15)
    return ""  # never persist a CLI error string as a "generation"


def judge(real, generated, repo):
    prompt = (
        "Two messages were typed by a developer to an AI coding agent at the SAME point in the "
        f"SAME session (repo {repo}). Message A is real; message B is a simulation of the same "
        "developer.\n\n"
        f"A (real): {truncate_words(real, 300)}\n\n"
        f"B (simulated): {truncate_words(generated, 300)}\n\n"
        "Score B against A on three axes:\n"
        "- content: same intent/topic/request as A? (0=unrelated, 100=same ask)\n"
        "- style: same surface voice — length, language, casing, tone, formatting? "
        "(0=obviously different person, 100=indistinguishable)\n"
        "- realism: is B a plausible, in-character next message this developer could genuinely "
        "have sent here — judged by intent and substance, NOT by whether it parrots their pet "
        "phrases? A message that does the right thing in a fresh wording scores HIGH; a recycled "
        "catchphrase that ignores the situation scores LOW. (0=implausible/out-of-character, "
        "100=entirely plausible for them here)\n"
        'Respond with ONLY JSON: {"content": <int>, "style": <int>, "realism": <int>}'
    )
    out = run_claude(prompt, JUDGE_MODEL, timeout=120)
    m = re.search(r'\{[^{}]*"content"[^{}]*\}', out)
    if not m:
        return None, None, None
    try:
        d = json.loads(m.group(0))
        return int(d.get("content")), int(d.get("style")), int(d.get("realism"))
    except (ValueError, TypeError):
        return None, None, None


SPEECH_ACTS = ["new_work", "refine_redirect", "pushback", "bug_report",
               "approve_proceed", "question", "interrupt", "other"]


def speech_act(text, prev_agent):
    """Classify the developer's conversational MOVE (speech act), ignoring specific details.
    Interrupts are detected without an API call; everything else is LLM-classified."""
    if is_interrupt(text):
        return "interrupt"
    if not (text or "").strip():
        return None
    prompt = (
        "A developer is using an AI coding agent. The agent just said:\n"
        f"<agent>{truncate_words(prev_agent, 120)}</agent>\n\n"
        "The developer's next message was:\n"
        f"<message>{truncate_words(text, 150)}</message>\n\n"
        "Classify the developer's conversational MOVE (speech act), ignoring the specific "
        "details/topic. Choose exactly one:\n"
        "- new_work: introduces a NEW feature/task/requirement to build or document\n"
        "- refine_redirect: steers or adjusts the CURRENT task; changes requirements\n"
        "- pushback: corrects, rejects, or complains about the agent's output/approach\n"
        "- bug_report: reports something broken or not behaving as expected\n"
        "- approve_proceed: approves, says continue, commit/push, or moves on\n"
        "- question: asks for information or clarification\n"
        "- other\n"
        'Respond with ONLY JSON: {"act": "<one of the above>"}'
    )
    out = run_claude(prompt, JUDGE_MODEL, timeout=120)
    m = re.search(r'"act"\s*:\s*"(\w+)"', out)
    act = m.group(1) if m else None
    return act if act in SPEECH_ACTS else ("other" if act else None)


_INTENT_MOVE = {"create new code": "new_work", "refactor": "refine_redirect",
                "debug": "bug_report", "understand": "question", "connect": "new_work",
                "git": "approve_proceed", "test": "new_work", "other": "approve_proceed"}
_PB_MOVE = {"correction": "pushback", "rejection": "pushback", "failure_report": "bug_report",
            "pacing_complaint": "pushback", "takeover": "interrupt",
            "requirement_change": "refine_redirect"}


def derive_move_prior(stats):
    """A per-user prior over the 7 moves, from the user's train intent + pushback rates.
    This is the user-specific lever: different users get different move-mixes."""
    intent = stats.get("intent_distribution") or {}
    pb = stats.get("pushback_distribution") or {}
    prior = {a: 0.0 for a in SPEECH_ACTS if a != "other"}
    pb_mass = sum(f for c, f in pb.items() if c in _PB_MOVE)
    for c, f in pb.items():
        if c in _PB_MOVE:
            prior[_PB_MOVE[c]] += f
    f0 = pb.get("non_pushback", max(0.0, 1.0 - pb_mass)) if pb else 1.0
    if intent:
        for it, f in intent.items():
            prior[_INTENT_MOVE.get(it, "approve_proceed")] += f0 * f
    else:
        prior["approve_proceed"] += f0
    tot = sum(prior.values()) or 1.0
    return {k: round(v / tot, 3) for k, v in prior.items() if v > 0}


def sample_move(prior, seed_key):
    """Stage 1 (sampling variant): draw the move from the user's prior, deterministically per
    point so own/wrong differ by their priors. Matches the user's true move-mix — including the
    interrupt rate — instead of letting an LLM argmax 'assertiveness' (which over-picks pushback)."""
    items = sorted((k, v) for k, v in prior.items() if v > 0)
    if not items:
        return None
    tot = sum(w for _, w in items)
    h = int(hashlib.sha256(seed_key.encode()).hexdigest(), 16)
    x = (h % 10_000) / 10_000 * tot
    c = 0.0
    for mv, w in items:
        c += w
        if x <= c:
            return mv
    return items[-1][0]


def predict_move(context_block, prior):
    """Stage 1 of move-conditioned generation: predict the move this user makes next,
    given the conversation and their move-mix prior. Calibrated so it does not collapse
    to approve_proceed the way free generation does."""
    pr = ", ".join(f"{k} {int(100 * v)}%" for k, v in sorted(prior.items(), key=lambda x: -x[1]))
    prompt = (
        "A developer is DRIVING an AI coding session toward their own goals. Across their history "
        f"their move mix is: {pr}.\n\n<conversation>\n{context_block}\n</conversation>\n\n"
        "They are about to send their next message. Which single MOVE will they make? They drive the "
        "project — do NOT assume they just approve; weigh the situation together with their mix "
        "(a developer who often pushes back or introduces work likely does so here too). Options: "
        "new_work, refine_redirect, pushback, bug_report, approve_proceed, question, interrupt.\n"
        'Respond with ONLY JSON: {"move": "<one>"}'
    )
    out = run_claude(prompt, JUDGE_MODEL, timeout=120)
    m = re.search(r'"move"\s*:\s*"(\w+)"', out)
    mv = m.group(1) if m else None
    return mv if mv in SPEECH_ACTS else None


def load_style_reference(slug, n=8):
    """A sample of the user's REAL messages (from the digest), for the 2AFC test.
    These are training-side messages, disjoint from the held-out points being predicted."""
    digest = json.loads((ROOT / "data" / "digests" / f"{slug}.json").read_text())
    pool = [p["text"] for p in digest.get("mid_session_prompts", [])]
    pool += [p["text"] for p in digest.get("opening_prompts", [])]
    pool = [t for t in pool if t and len(t.split()) >= 2]
    # deterministic spread across the pool, prefer shorter messages (the style tells)
    pool = sorted(pool, key=len)[: max(n * 3, n)]
    step = max(1, len(pool) // n)
    return [truncate_words(t, 60) for t in pool[::step][:n]]


_DISC_CRITERIA = {
    # the original metric: rewards surface signature / recognizability (caricature-friendly)
    "style": "Which candidate better matches the writing STYLE of the real developer above — "
             "their length, language, casing, tone and characteristic phrasing?",
    # the (3) metric: rewards content/realism, explicitly discounting catchphrase mimicry
    "realism": "Which candidate is the more REALISTIC next message this developer would actually "
               "send — judged by whether it does the right thing given how they work (intent, "
               "substance, appropriate action)? Ignore superficial mimicry: do NOT reward a "
               "candidate just for copying their pet phrases, and do NOT penalize a plausible, "
               "in-character message for being freshly worded.",
}


def discriminate(reference, cand_a, cand_b, criterion="style"):
    """2AFC: given real reference messages from a developer, which candidate (A/B) better fits
    them under the given criterion ('style' or 'realism')? Returns 'A', 'B', or None."""
    ref = "\n".join(f"- {r}" for r in reference)
    prompt = (
        "Here are real messages a specific developer typed to an AI coding agent:\n"
        f"{ref}\n\n"
        "Two candidate messages were written at a later point in one of their sessions. "
        "Exactly one was produced by a system simulating THIS developer; the other simulates a "
        "DIFFERENT developer.\n\n"
        f"A: {truncate_words(cand_a, 120)}\n\n"
        f"B: {truncate_words(cand_b, 120)}\n\n"
        f"{_DISC_CRITERIA[criterion]} "
        'Respond with ONLY JSON: {"pick": "A"} or {"pick": "B"}.'
    )
    out = run_claude(prompt, JUDGE_MODEL, timeout=120)
    m = re.search(r'"pick"\s*:\s*"([AB])"', out)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=10)
    ap.add_argument("--slugs", nargs="*", default=None)
    ap.add_argument("--parallel", type=int, default=8)
    ap.add_argument("--mode", choices=["inline", "folder"], default="inline",
                    help="inline: paste folder contents into prompt (controlled experiment). "
                         "folder: point the agent at users/<slug>/ and let it Read (product flow).")
    ap.add_argument("--generate-only", action="store_true",
                    help="only fill the generations file (resume-safe); skip embedding/judge/2AFC. "
                         "Use for gentle top-up passes when rate-limited.")
    ap.add_argument("--score-only", action="store_true",
                    help="skip generation; load existing generations and (re)score them. "
                         "Use to re-judge with an updated judge without regenerating.")
    ap.add_argument("--gen-file", default=None,
                    help="override path to the generations jsonl (default results/generations_<mode>.jsonl)")
    ap.add_argument("--results-file", default=None,
                    help="override output results json path")
    ap.add_argument("--repos-dir", default=None,
                    help="dir of repo checkouts (<repos-dir>/<owner>/<repo>); when a target session's "
                         "repo is present, folder-mode simulator is given read access to it (point 3).")
    ap.add_argument("--move-conditioned", action="store_true",
                    help="two-stage generation: Stage 1 picks the move (folder mode); Stage 2 renders "
                         "it in voice. Fixes the approve-collapse / zero-interrupt bias and adds "
                         "user-specificity.")
    ap.add_argument("--move-source", choices=["sample", "predict"], default="sample",
                    help="Stage-1 move source: 'sample' draws from the user's move prior (true "
                         "move-mix incl. interrupts; own!=wrong by construction; no LLM call); "
                         "'predict' uses an LLM classifier over context+prior (tends to over-pick "
                         "pushback). Default sample.")
    ap.add_argument("--exemplars", action="store_true",
                    help="few-shot the user's OWN real messages of the sampled move (from "
                         "users/<slug>/move_exemplars.json) into Stage-2 for move-matched voice.")
    args = ap.parse_args()
    read_folder = args.mode == "folder"
    move_conditioned = args.move_conditioned
    repos_dir = Path(args.repos_dir) if args.repos_dir else None

    RESULTS.mkdir(exist_ok=True)
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text())

    if args.slugs:
        slugs = args.slugs
    else:  # stratified by session count among users with a distilled folder
        have_folder = [s for s in manifest if (ROOT / "users" / s / "USER.md").exists()]
        ranked = sorted(have_folder, key=lambda s: -manifest[s]["n_sessions"])
        step = max(1, len(ranked) // args.users)
        slugs = ranked[::step][:args.users]
    print(f"validation users: {slugs}")

    # wrong-folder pairing: rotate by one (derangement)
    wrong_of = {s: slugs[(i + 1) % len(slugs)] for i, s in enumerate(slugs)}

    folders = {s: load_folder_text(s) for s in slugs}
    for s, txt in folders.items():
        if not txt:
            raise SystemExit(f"no distilled folder for {s}; run distill.py first")

    def folder_path(s):
        return str((ROOT / "users" / s).relative_to(ROOT))

    # per-user move priors (for move-conditioned generation). A flat prior backs the generic cond.
    priors = {}
    for s in set(slugs) | {wrong_of[s] for s in slugs}:
        sp = ROOT / "users" / s / "stats.json"
        priors[s] = derive_move_prior(json.loads(sp.read_text())) if sp.exists() else {}
    flat_prior = {a: round(1 / 7, 3) for a in SPEECH_ACTS if a != "other"}

    # build all jobs
    jobs = []
    point_meta = {}  # point_id -> {prev_agent, real} for speech-act labeling
    for slug in slugs:
        holdout = json.loads((ROOT / "data" / "holdout" / f"{slug}.json").read_text())
        points = pick_points(holdout)
        print(f"  {slug}: {len(points)} prediction points")
        for pi, point in enumerate(points):
            pid = f"{point['session_id']}#{point['turn_index']}"
            point_meta[pid] = {"prev_agent": point.get("prev_agent", ""), "real": point["real"]}
            if repos_dir is not None:
                cand = repos_dir / point["repo"]  # repo is "owner/name"
                if cand.exists():
                    point["repo_path"] = str(cand)
            for cond in CONDITIONS:
                src = {"distilled": slug, "generic": None, "wrong": wrong_of[slug]}[cond]
                job = {"slug": slug, "point_id": pid, "cond": cond, "point": point,
                       "fpath": folder_path(src) if src else None,
                       "prior": priors.get(src) or flat_prior}
                if move_conditioned:
                    job["prompt"] = None  # built in work() after Stage-1 move prediction
                elif read_folder:
                    job["prompt"] = build_folder_prompt(point, job["fpath"])
                else:
                    job["prompt"] = build_prompt(point, folders[src] if src else "")
                jobs.append(job)

    # resume: skip already-generated good records. Drop any CLI-failure records (session limit,
    # overload, max-turns) so they are regenerated and never pollute scoring. Per-mode file.
    gen_path = Path(args.gen_file) if args.gen_file else RESULTS / f"generations_{args.mode}.jsonl"
    done = set()
    if args.score_only:
        print(f"score-only: loading existing generations from {gen_path}, skipping generation")
    elif gen_path.exists():
        kept = []
        dropped = 0
        for line in gen_path.read_text().splitlines():
            r = json.loads(line)
            if is_cli_failure(r.get("generated", "")):
                dropped += 1
                continue
            done.add((r["slug"], r["point_id"], r["cond"]))
            kept.append(line)
        if dropped:
            gen_path.write_text("\n".join(kept) + ("\n" if kept else ""))
            print(f"dropped {dropped} prior CLI-failure generations for regeneration")
    todo = [] if args.score_only else [j for j in jobs if (j["slug"], j["point_id"], j["cond"]) not in done]
    print(f"jobs: {len(jobs)} total, {len(todo)} to run")

    def work(job):
        cond_move = None
        prompt = job["prompt"]
        try:
            if move_conditioned:
                # Stage 1: choose the move — sample from the user's prior (default) or LLM-predict
                if args.move_source == "sample":
                    cond_move = sample_move(job["prior"], f"{job['point_id']}|{job['fpath']}")
                else:
                    cond_move = predict_move(_context_block(job["point"]), job["prior"])
                # Stage 2: render that move (fall back to free generation if Stage 1 failed)
                prompt = build_folder_prompt(job["point"], job["fpath"], target_move=cond_move,
                                             use_exemplars=args.exemplars)
            gen = run_claude(prompt, GEN_MODEL, read_folder=read_folder)
        except subprocess.TimeoutExpired:
            gen = ""
        rec = {"slug": job["slug"], "point_id": job["point_id"], "cond": job["cond"],
               "repo": job["point"]["repo"], "real": job["point"]["real"], "generated": gen}
        if move_conditioned:
            rec["conditioned_move"] = cond_move
        return rec

    if todo:
        with gen_path.open("a") as fh, ThreadPoolExecutor(max_workers=args.parallel) as ex:
            futs = [ex.submit(work, j) for j in todo]
            for i, fut in enumerate(as_completed(futs), 1):
                rec = fut.result()
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                print(f"[gen {i}/{len(todo)}] {rec['slug']} {rec['cond']} "
                      f"({len(rec['generated'].split())}w)", flush=True)

    # ---- scoring ----
    records = [json.loads(l) for l in gen_path.read_text().splitlines()]
    job_keys = {(j["slug"], j["point_id"], j["cond"]) for j in jobs}
    records = [r for r in records if (r["slug"], r["point_id"], r["cond"]) in job_keys]
    bad = [r for r in records if is_cli_failure(r.get("generated", ""))]
    if bad:
        print(f"WARNING: {len(bad)} records still CLI-failures after regeneration; excluded from scoring")
    records = [r for r in records if not is_cli_failure(r.get("generated", ""))]

    if args.generate_only:
        print(f"generate-only: {len(records)}/{len(jobs)} clean generations "
              f"({len(jobs) - len(records)} still missing); skipping scoring")
        return

    print("embedding...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(EMBED_MODEL)
    reals = model.encode([r["real"] for r in records], normalize_embeddings=True)
    gens = model.encode([r["generated"] or " " for r in records], normalize_embeddings=True)
    for r, e_r, e_g in zip(records, reals, gens):
        r["cosine"] = round(float((e_r * e_g).sum()), 4)
        lr = len(r["real"].split())
        lg = len(r["generated"].split())
        r["len_ratio"] = round(min(lr, lg) / max(lr, lg), 3) if lr and lg else 0.0

    print("judging...")
    def judge_one(r):
        c, s, rl = judge(r["real"], r["generated"], r["repo"])
        r["judge_content"], r["judge_style"], r["judge_realism"] = c, s, rl
        return r
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futs = [ex.submit(judge_one, r) for r in records if r["generated"]]
        for i, fut in enumerate(as_completed(futs), 1):
            if i % 20 == 0:
                print(f"[judge {i}/{len(futs)}]", flush=True)

    # ---- speech-act labeling: the REAL move per point, and each generation's move ----
    print("labeling speech acts...")
    real_acts = {}   # point_id -> real speech act (labeled once)
    def label_real(pid):
        meta = point_meta.get(pid, {})
        return pid, speech_act(meta.get("real", ""), meta.get("prev_agent", ""))
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        for fut in as_completed([ex.submit(label_real, pid) for pid in point_meta]):
            pid, act = fut.result()
            real_acts[pid] = act

    def label_gen(r):
        pa = point_meta.get(r["point_id"], {}).get("prev_agent", "")
        r["pred_act"] = speech_act(r["generated"], pa)
        r["real_act"] = real_acts.get(r["point_id"])
        r["act_match"] = (r["pred_act"] is not None and r["pred_act"] == r["real_act"])
        return r
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        list(as_completed([ex.submit(label_gen, r) for r in records if r["generated"]]))

    # ---- aggregate ----
    def agg(rows, key):
        vals = [r[key] for r in rows if r.get(key) is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    def act_match_rate(rows):
        v = [r["act_match"] for r in rows if r.get("real_act") and r.get("pred_act")]
        return round(sum(v) / len(v), 3) if v else None

    JUDGE_AXES = ["judge_content", "judge_style", "judge_realism"]
    by_cond = {c: [r for r in records if r["cond"] == c] for c in CONDITIONS}
    summary = {c: {"n": len(rows), "cosine": agg(rows, "cosine"), "len_ratio": agg(rows, "len_ratio"),
                   "act_match": act_match_rate(rows),
                   **{ax: agg(rows, ax) for ax in JUDGE_AXES}}
               for c, rows in by_cond.items()}
    from collections import Counter
    real_act_dist = dict(Counter(a for a in real_acts.values() if a))
    act_confusion = {c: dict(Counter(f"{r.get('real_act')}>{r.get('pred_act')}"
                                     for r in by_cond[c] if r.get("real_act") and r.get("pred_act")))
                     for c in CONDITIONS}

    # paired win rates: distilled vs each baseline, on cosine + each judge axis
    by_key = {}
    for r in records:
        by_key.setdefault((r["slug"], r["point_id"]), {})[r["cond"]] = r
    win_metrics = ["cosine"] + JUDGE_AXES
    wins = {f"distilled_vs_{b}": {m: [0, 0] for m in win_metrics} for b in ["generic", "wrong"]}
    for conds in by_key.values():
        d = conds.get("distilled")
        for b in ["generic", "wrong"]:
            o = conds.get(b)
            if not d or not o:
                continue
            for metric in win_metrics:
                if d.get(metric) is None or o.get(metric) is None:
                    continue
                wins[f"distilled_vs_{b}"][metric][1] += 1
                if d[metric] > o[metric]:
                    wins[f"distilled_vs_{b}"][metric][0] += 1
    win_rates = {k: {m: (round(w / n, 3) if n else None)
                     for m, (w, n) in v.items()} for k, v in wins.items()}

    # ---- 2AFC discrimination: distilled vs wrong, under TWO criteria ----
    # 'style' rewards surface signature (recognizability); 'realism' rewards in-character
    # content and discounts catchphrase mimicry (the option-(3) metric).
    refs = {s: load_style_reference(s) for s in slugs}
    base_pairs = []  # (key, slug, distilled_text, wrong_text, distilled_slot)
    for key, conds in by_key.items():
        d, w = conds.get("distilled"), conds.get("wrong")
        if not d or not w or not d["generated"] or not w["generated"]:
            continue
        if is_cli_failure(d["generated"]) or is_cli_failure(w["generated"]):
            continue
        slot = "A" if (hash(key[1]) % 2 == 0) else "B"  # cancel position bias
        base_pairs.append((key, key[0], d["generated"], w["generated"], slot))

    def run_discrimination(criterion):
        def disc_one(pair):
            key, slug, d_txt, w_txt, slot = pair
            a, b = (d_txt, w_txt) if slot == "A" else (w_txt, d_txt)
            pick = discriminate(refs[slug], a, b, criterion=criterion)
            return slug, ((pick == slot) if pick else None)
        results = []
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            for fut in as_completed([ex.submit(disc_one, p) for p in base_pairs]):
                results.append(fut.result())
        valid = [c for _, c in results if c is not None]
        agg_disc = {"n": len(valid),
                    "distilled_chosen_rate": round(sum(valid) / len(valid), 3) if valid else None,
                    "chance": 0.5}
        by_user = {}
        for slug in slugs:
            u = [c for s, c in results if s == slug and c is not None]
            by_user[slug] = round(sum(u) / len(u), 3) if u else None
        return agg_disc, by_user

    discriminations, discriminations_by_user = {}, {}
    for crit in ["style", "realism"]:
        print(f"discriminating (2AFC, {crit})...")
        agg_disc, by_user = run_discrimination(crit)
        discriminations[crit] = agg_disc
        discriminations_by_user[crit] = by_user
    # back-compat: top-level `discrimination` keeps the style criterion
    discrimination = discriminations["style"]
    disc_by_user = discriminations_by_user["style"]

    per_user = {}
    for slug in slugs:
        per_user[slug] = {c: {"cosine": agg([r for r in by_cond[c] if r["slug"] == slug], "cosine"),
                              "act_match": act_match_rate([r for r in by_cond[c] if r["slug"] == slug]),
                              **{ax: agg([r for r in by_cond[c] if r["slug"] == slug], ax)
                                 for ax in JUDGE_AXES}}
                          for c in CONDITIONS}

    out = {"mode": args.mode, "embed_model": EMBED_MODEL, "gen_model": GEN_MODEL,
           "judge_model": JUDGE_MODEL, "users": slugs, "wrong_pairing": wrong_of,
           "summary": summary, "win_rates": win_rates,
           "discrimination": discrimination, "discrimination_by_user": disc_by_user,
           "discriminations": discriminations, "discriminations_by_user": discriminations_by_user,
           "real_act_distribution": real_act_dist, "act_confusion": act_confusion,
           "per_user": per_user, "records": records}
    if args.results_file:
        results_path = Path(args.results_file)
    else:
        name = "validation_results.json" if args.mode == "inline" else f"validation_results_{args.mode}.json"
        results_path = RESULTS / name
    results_path.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({"summary": summary, "discriminations": discriminations}, indent=1))


if __name__ == "__main__":
    main()

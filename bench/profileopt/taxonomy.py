"""FINAL move taxonomy (v2) — optimized for inter-judge agreement.

Replaces the 7-way (new_work, refine_redirect, pushback, bug_report, approve_proceed,
question, +other; interrupt via regex) — mean inter-judge κ ≈ 0.65-0.69 — with a 4-way
taxonomy chosen by a κ-search over candidate taxonomies + classifier prompts:

  approve   — pure acceptance / go-ahead, no instruction, no complaint
  critical  — explicitly states the work is defective (bug/error/failure/wrong/reject/revert)
  directive — tells the agent to build/add/change/proceed-with-changes (forward work), no defect
  inquiry   — asks for information/explanation/options, no defect asserted

Mean inter-judge κ (Haiku-4.5 / Sonnet-4.6 / Opus-4.8, via CLI): 0.789, balanced across pairs,
vs 0.647 for the 7-way on the same judges (+0.14). The key was NOT merging alone (that just
relocates confusion) but the ordered "a defect must be explicitly asserted to be critical;
mere direction-change is directive" decision rule.

Downstream continuity (the site's approve%/critical% are preserved):
  approve%  = approve
  critical% = critical            (old pushback + bug_report + interrupt all map here)
  directive = old new_work + refine_redirect
  inquiry   = old question
"""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate as V  # noqa: E402

CATEGORIES = ["approve", "critical", "directive", "inquiry"]

# Remap legacy 7-way labels -> v2 (for reusing old caches / site metrics). 'other' has no v2 home.
OLD_TO_NEW = {
    "approve_proceed": "approve",
    "pushback": "critical", "bug_report": "critical", "interrupt": "critical",
    "new_work": "directive", "refine_redirect": "directive",
    "question": "inquiry",
    "other": None,
}

BODY = (
    "Classify the developer's MOVE about the agent's previous turn by one OBSERVABLE test each. "
    "Choose exactly one (check in order):\n"
    "1. critical — the message explicitly states the work is defective: names a bug/error/failure, says it's "
    "wrong/broken, rejects it, or says 'no/revert/undo'. The mere act of changing direction is NOT critical "
    "unless a defect is asserted.\n"
    "2. inquiry — the message's main act is asking for information/explanation/options and waiting for an "
    "answer (a '?' seeking knowledge), with no defect asserted.\n"
    "3. directive — the message tells the agent to build, add, change, or proceed-with-changes (forward work), "
    "with no defect asserted. Approval plus an instruction is directive.\n"
    "4. approve — the message only accepts or says go ahead, with no instruction and no defect.\n\n"
    "Key tie-breaks: 'fix the failing test' / 'this crashes' -> critical (defect asserted). "
    "'change it to use PUT' / 'also add caching' -> directive (no defect asserted). "
    "'why did you do X?' -> inquiry. 'lgtm' -> approve. 'looks good, now add tests' -> directive.\n\n"
    "EXAMPLES:\n"
    "agent 'Added the endpoint.' -> dev 'it returns 500' -> critical\n"
    "agent 'Added the endpoint.' -> dev 'now add auth to it' -> directive\n"
    "agent 'Refactored to async.' -> dev 'revert that, it deadlocks' -> critical\n"
    "agent 'Refactored to async.' -> dev 'is async safe here?' -> inquiry\n"
    "agent 'Done.' -> dev 'ship it' -> approve"
)

# CLI (subscription) judges by default; OpenRouter ids available when the account has credits.
CLI_JUDGES = {"haiku": "claude-haiku-4-5-20251001", "sonnet": "claude-sonnet-4-6", "opus": "claude-opus-4-8"}
OR_JUDGES = {"haiku": "anthropic/claude-haiku-4.5", "opus": "anthropic/claude-opus-4.8", "gpt5": "openai/gpt-5"}


def _prompt(text, prev_agent):
    return ("A developer is using an AI coding agent. The agent just said:\n"
            f"<agent>{V.truncate_words(prev_agent, 120)}</agent>\n\n"
            "The developer's next message was:\n"
            f"<message>{V.truncate_words(text, 150)}</message>\n\n"
            f"{BODY}\n\n"
            'Respond with ONLY JSON: {"act": "<one label>"}')


def _strip_interrupt(text):
    s = (text or "").strip()
    return re.sub(r'^\[INTERRUPT\]\s*', '', s, flags=re.I).strip()


def classify(text, prev_agent, model="claude-haiku-4-5-20251001", backend="cli"):
    """Classify one message into the v2 4-way taxonomy. Interrupts: classify the text after the
    marker; a bare interrupt (no text) is 'critical' (a corrective cut-off)."""
    if V.is_interrupt(text):
        rest = _strip_interrupt(text)
        if not rest:
            return "critical"
        text = rest
    if not (text or "").strip() or V.is_cli_failure(text):
        return None
    prompt = _prompt(text, prev_agent)
    if backend == "cli":
        out = V.run_claude(prompt, model, timeout=90)
    else:
        sys.path.insert(0, str(ROOT / "bench"))
        import orouter
        out = orouter.chat(model, prompt, max_tokens=900, temperature=0,
                           reasoning_effort=(None if "haiku" in model else "low"))
    if V.is_cli_failure(out):
        return None
    m = re.search(r'"act"\s*:\s*"(\w+)"', out)
    a = m.group(1) if m else None
    return a if a in CATEGORIES else None


def majority_label(text, prev_agent, backend="cli"):
    judges = CLI_JUDGES if backend == "cli" else OR_JUDGES
    per = {j: classify(text, prev_agent, model=mid, backend=backend) for j, mid in judges.items()}
    votes = [v for v in per.values() if v]
    if not votes:
        return None, per
    from collections import Counter
    top = Counter(votes).most_common()
    best = [m for m, c in top if c == top[0][1]]
    return (best[0] if len(best) == 1 else (per.get("haiku") if per.get("haiku") in best else best[0])), per

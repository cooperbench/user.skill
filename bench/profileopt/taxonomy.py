"""FINAL move taxonomy (v2) — optimized for inter-judge agreement.

Replaces the 7-way (new_work, refine_redirect, pushback, bug_report, approve_proceed,
question, +other; interrupt via regex) with a 4-way taxonomy chosen by a κ-search over
candidate taxonomies + classifier prompts and confirmed on a cross-family judge panel.

  approve   — acceptance/permission, no new content, no complaint (incl. thanks/greetings)
  critical  — asserts something is WRONG (bug/failure/wrong output/unwanted approach)
  directive — tells the agent what to DO next, no fault asserted (new task / forward steer)
  inquiry   — asks for information/explanation, expecting an ANSWER

Mean pairwise inter-judge κ on a 120-item sample:
  CROSS-FAMILY (Haiku-4.5 / Opus-4.8 / GPT-5): 0.681 (7-way) -> 0.805 (this 4-way), +0.12,
    balanced (h-o 0.78, h-g 0.77, o-g 0.86), crossing the 0.80 "reliable" bar.
  Claude-family (Haiku/Sonnet/Opus): 0.647 -> ~0.79.
Key: NOT merging alone (that relocates confusion) but the ordered decision rule whose first
test is "is a fault/defect asserted?" — a neutral change of approach is directive, not critical.

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

BODY = """Classify the developer's MOVE by the observable function of their message toward the agent's previous turn. Judge what the message DOES, not its topic. Choose exactly one:

- approve: Signals acceptance or permission with no new content and no complaint — praise, agreement, 'yes/ok/lgtm/go ahead/perfect', a bare go-ahead, or standalone thanks/greetings. The message could be deleted and the agent would just continue.
- critical: Asserts something is WRONG — reports a bug, failure, or wrong output, or says the approach/answer is mistaken or unwanted ('no/that's wrong/you misunderstood/this is broken').
- directive: Tells the agent what to DO next without asserting prior work was wrong — a new task, an addition, or a forward steer/refinement. Imperative or action request with no fault stated.
- inquiry: Primarily asks for information or explanation, expecting an ANSWER rather than an action ('why/how/what/can it...?').

DECISION RULE (top-down, first match wins):
1. States or implies a fault/error/dissatisfaction, or calls the result wrong/unwanted -> critical (even if it also says what to do, and even if phrased as a question like 'why is this still broken?'). NOTE: 'instead/rather/don't' alone do NOT make it critical — a neutral swap of approach with no stated problem is directive.
2. Else asks for information and expects an answer -> inquiry.
3. Else requests/commands any action, new task, or change -> directive.
4. Else (only acceptance/permission/praise/thanks/greeting) -> approve.

EXAMPLES:
Agent: 'I refactored auth into a service.' -> Dev: 'Now also add rate limiting.' -> directive
Agent: 'Switched the parser to regex.' -> Dev: 'Use the AST approach instead.' -> directive (swap, no defect stated)
Agent: 'Switched the parser to regex.' -> Dev: 'Regex misses nested cases — use AST.' -> critical (defect named)
Agent: 'Returns the sorted list.' -> Dev: 'It still returns them unsorted.' -> critical
Agent: 'I added retries with backoff.' -> Dev: 'Why exponential over fixed?' -> inquiry
Agent: 'Tests pass.' -> Dev: 'Great, ship it.' -> approve
Agent: 'Done.' -> Dev: 'Thanks!' -> approve"""

# CLI (subscription) judges by default; OpenRouter ids for the cross-family panel.
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
    return re.sub(r'^\[INTERRUPT\]\s*', '', (text or "").strip(), flags=re.I).strip()


def classify(text, prev_agent, model="claude-haiku-4-5-20251001", backend="cli"):
    """Classify one message into the v2 4-way. Interrupts: classify the text after the marker;
    a bare interrupt (no text) is 'critical' (a corrective cut-off)."""
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

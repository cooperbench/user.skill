---
name: adversarial-test-kickoff
description: When starting a new test session, the user writes (or pastes) a highly structured, numbered adversarial test spec that explicitly instructs the agent to try to break, crash, or find edge cases in the app — not just verify happy paths.
---

# Adversarial test kickoff

The user's opening gambit for test sessions is a detailed numbered checklist that instructs the agent to be adversarial — to hunt for failures, not confirm successes.

**Trigger**: Start of a test session, or after the user rejects a shallow smoke test and wants real coverage.

**Pattern**: Long structured prompt (200–750 words) with:
- An `<environment>` block specifying URL and browser context
- A `<developer_request>` block with a numbered list of 6–10 specific adversarial interactions to attempt
- Language like "Try to BREAK", "Be adversarial", "Hunt for crashes", "Report EVERY bug"
- A `<scope_strategy>` block with coverage guidance
- Each test step includes the expected bad outcome, not just the action

**Example opening line**:
> `Try to break the Markdown editor on http://localhost:5173?file=demo. Hunt for crashes, errors, and edge cases:`

Or more aggressive:
> `Try to BREAK the Markdown editor on http://localhost:5173?file=demo. Be adversarial:`

**Casual variant** (when redirecting mid-session after a rejection):
> `do more testing like try to break the app as much as possible in a subagent and then here fux all of them`

The casual variant is the same intent — find bugs, fix them — but compressed to one sentence with a typo ("fux" for "fix") and no structure.

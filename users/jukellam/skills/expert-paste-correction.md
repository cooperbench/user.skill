---
name: expert-paste-correction
description: Trigger when jukellam is in "Expert Nitpicker" mode — he corrects by pasting entire blocks of subagent-generated technical analysis back as his message, expecting the agent to incorporate them.
---

# Skill: expert-paste-correction

## Behavior

When the agent (via a deepening or review workflow) produces technical findings, jukellam does not paraphrase them. He copies the raw markdown from the subagent result — complete with headers like `### CRITICAL: Existing Code Regressions (Priority 1)`, code blocks, and SQL snippets — and pastes it as his correction prompt.

This pattern appears repeatedly when the plan-deepening agent keeps returning the same summary ("The plan has been deepened and saved. Here's a summary of what was added..."). jukellam's "reply" is a paste of one specific finding from the code review that he wants addressed. He does this once per finding, one at a time, cycling through CRITICAL → High → Medium → Low items.

He also pastes back overall assessment summaries when he wants the agent to take stock: "## Plan Review: Startup Dynasty Draft + Trading System\n\n### Overall Assessment\n\nThis is a well-structured plan..."

## Verbatim examples

After the agent reports plan deepening complete, jukellam sends:

> "### CRITICAL: Existing Code Regressions (Priority 1) #### 1. The `str`/`int` ID type inconsistency will become a liability The codebase has a pervasive anti-pattern: database IDs are `int` in the database but `str` in the dataclass models. Look at `/Users/justin.kellam/Repos/dispersal-draft/app/models.py` line 31: [...]"

> "### DECIMAL HANDLING (Priority 2) #### 15. The SQL budget arithmetic is unsafe In `/Users/justin.kellam/Repos/dispersal-draft/app/state_db.py` line 587: [...]"

> "### TESTING STRATEGY (Priority 3) #### 13. The testing plan is good but missing concurrency tests [...]"

## Role-play note

When producing jukellam in this mode, paste large technical content with no framing before it. No "Can you also address:" — just the raw finding text, as if copy-pasted from a document. The agent is expected to understand the implicit instruction ("incorporate this into the plan").

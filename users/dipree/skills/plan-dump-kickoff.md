---
name: plan-dump-kickoff
description: Trigger when starting a large new feature or bug fix — dipree pastes a complete markdown implementation plan under "Implement the following plan:" and expects full execution. Use for create new code or debug intents on complex tasks.
---

# Skill: plan-dump-kickoff

For non-trivial features, dipree designs the plan himself (often in plan mode) and then dumps it as the opening prompt. He does not ask the agent to design the architecture — he hands over a complete spec and expects implementation. Plans are 300–1200+ words, structured as markdown with headers, code snippets, and file paths.

## Structure

```
Implement the following plan:

# Plan: <Title>

## Context
<Background on what exists and why this is needed>

## Changes

### 1. <File or component>
<Detailed description with code snippets and line references>

### 2. <File or component>
...

## Verification
```bash
<build/lint/test commands>
```

[Optional: transcript reference for additional context]
```

## Verbatim examples (openings)

> "Implement the following plan: # Plan: Wingman status notifications in agent terminal ## Context Wingman status messages (review started, review pending) currently go to stderr, which is invisible in Claude Code's UI..."

> "Implement the following plan: # Fix: Wingman auto-apply never triggers on session close + improve logging ## Context When a user closes a Claude session with a pending `REVIEW.md`, the auto-apply never fires..."

> "Implement the following plan:\n\n# Plan: Remove trail enable/disable commands and related functionality\n\n## Context\nThe user wants to simplify the trails feature by removing the ability to enable/disable trails..."

## Notes

- Plans always include exact file paths and often line numbers
- Code snippets in triple backticks inside the plan
- Verification section with `mise run` commands is common
- Sometimes ends with a transcript reference: "If you need specific details from before exiting plan mode, read the full transcript at: /Users/dip/.claude/projects/..."
- After the plan dump, subsequent prompts revert to one-liners ("commit and push", "push")

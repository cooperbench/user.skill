---
name: plan-dump-kickoff
description: Triggers when cteyton opens a new session with a full pre-written implementation plan. Fires on ~80% of session openings. The message starts with "Implement the following plan:" followed by a structured markdown document.
---

# Plan dump kickoff

cteyton pre-writes the entire implementation plan in plan mode before starting a session. The opening message is always a delegation, never a question. The plan includes:

1. `# Plan: <Title>` or `# Fix: <Title>` heading
2. `## Context` — explains the current state and why the change is needed
3. `## Design Decisions` — pre-made decisions the agent must not second-guess
4. File-by-file change specs with exact file paths, line numbers, before/after code blocks
5. `## Verification` — explicit commands to run (`bun run test`, `bun run lint`, `bun run typecheck`)

The trailing note appears on plan-mode-generated plans:
> `"If you need specific details from before exiting plan mode (like exact code snippets, error messages, or content you generated), read the full transcript at: /Users/cedricteyton/.REDACTED.jsonl"`

## Verbatim examples

> `"Implement the following plan: # Plan: Add nesting guidance to skill Instructions template\n\n## Context\n\nGenerated SKILL.md files have flat bullet lists in the ## Instructions section, even when steps logically contain sub-steps... ## Verification\n- Run bun run test to ensure no regressions\n- Run bun run lint to ensure formatting is clean"`

> `"Implement the following plan: # Fix: Remediation deletion not available for failed remediations\n\n## Context\nWhen a remediation fails (status 'failed'), the user gets stuck in a dead-end state..."`

> `"Update the home page so that it mentions that it's open source."` — (rare: short opener without plan dump)

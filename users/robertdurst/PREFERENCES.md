---
name: preferences-robertdurst
description: What robertDurst corrects, rejects, delegates, and how he drives work sessions
metadata:
  type: user
---

# Preferences: robertDurst

## Pushback distribution

- Non-pushback: **79.6%** — most agent output is accepted and moved past.
- Correction: **19.5%** — about 1 in 5 messages corrects agent behavior.
- Failure report: **0.9%** — rare, but includes pasting actual test output when agent claims success.

## What triggers corrections

1. **Agent asks a clarifying question when the answer is obvious from context.** Robert just answers it tersely: "understand the architecture so I can propose an idea I have" — no acknowledgment of the question, just the directive.

2. **Agent summarizes results and waits when Robert wanted action.** He cuts through: "yep do this" or "let's do it, start building."

3. **Agent claims tests pass when they don't.** Robert pastes the raw terminal output without commentary and expects the agent to read it: "I see this Run cd caffeine_lang && gleam test..."

4. **Agent returns a too-long synthesis.** Robert issues a redirect: "summarize this list. Just bullet points" or "give me a one sentence summary."

5. **Agent waits for other sub-agents to complete and just sends a placeholder status.** Robert doesn't accept "Waiting on the other 9" — he forwards the completed agent's results himself to keep momentum.

## What satisfies him

- Agents that act immediately without asking permission.
- Parallel agent fans that return structured findings.
- Clean architectural recommendations with "before/after" code and file locations.
- Agents that spot correctness issues proactively.
- Concrete metrics: lines eliminated, files modified, LOC saved.

## Workflow habits

- **Plans before building.** Pastes a fully-specified plan document (with tables, code blocks) before handing off a major refactor. Agent implements the plan as written.
- **Multi-phase sequencing.** Explicitly sequences work: "lets first do A + B + C. When done, lets see if D + E make sense."
- **Maintains a running todo list.** References it across turns: "recall our like 10 step todo list?" Expects the agent to track it.
- **Correctness verification pass after implementation.** Spins up 5–10 agents specifically to verify the new code.
- **No commit cadence visible.** Doesn't mention PRs, branches, or commits in session. Seems to work in long continuous sessions.

## Stack / tool preferences visible in prompts

- **Gleam** for compiler, LSP intelligence.
- **TypeScript/Deno** for LSP server protocol layer.
- **Claude Code team agents** for parallel exploration.
- Prefers **data-driven** approaches over boilerplate case statements.
- Values **type-driven design** — wants Gleam's type system to enforce invariants.
- Prefers moving vendor-specific logic to codegen (not generic analysis layers).
- Wants **simpler pipeline** — reduce intermediate data structures, eliminate redundant traversals.

## What he delegates vs. specifies precisely

- **Delegates:** Architecture exploration, correctness verification, research (SRE patterns, industry tools), finding duplication in the codebase.
- **Specifies precisely:** Implementation plans (provides exact file paths, line numbers, before/after code). When he pastes a plan, he expects it followed exactly.

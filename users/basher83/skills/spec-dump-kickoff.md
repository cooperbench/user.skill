---
name: spec-dump-kickoff
description: basher83 opens tailnet-microservices sessions with a large pre-written numbered orchestration spec (500–2000 words) that hard-codes subagent counts, model tiers, file references, commit/push steps, and a scope exit condition. Trigger: starting a new automation loop iteration on the microservices repo.
---

When basher83 opens a session on `tailnet-microservices`, he does not type a task description — he pastes a full orchestration specification. The spec is pre-written (identical across sessions with minor variation), numbered with sub-lettered steps, and covers:

- How to learn the specs (read `specs/*` using up to 500 parallel Sonnet subagents)
- Task source priority (`@TASK.md` overrides `@IMPLEMENTATION_PLAN.md`)
- Agent tier selection (Sonnet for reads/searches, Opus for debugging and architectural decisions, 1 subagent max for build/tests)
- Implementation loop: search before assuming unimplemented, run tests after, update plan on discovery, remove items on resolution
- Commit/push discipline: `git add -A`, descriptive commit message, `git push`
- Hard scope limit: complete exactly ONE phase/logical unit, then exit; the loop restarts with fresh context

The message is not composed in the moment — it reads as a template being invoked. Subsequent prompts in the same session revert to interactive terse mode.

**Example (opening prompt, trimmed for length):**

> 0a. Study `specs/*` with up to 500 parallel Sonnet subagents to learn the service specifications. 0b. If @TASK.md exists, read it — this is your sole task for this iteration. Skip @IMPLEMENTATION_PLAN.md for task selection. Otherwise, study @IMPLEMENTATION_PLAN.md. 0c. Study @AGENTS.md for build commands and code patterns. 1. If @TASK.md exists, that is your SOLE task — implement it, do not consult @IMPLEMENTATION_PLAN.md for task selection. Otherwise, follow @IMPLEMENTATION_PLAN.md and choose the most important item to address. Before making changes, search the codebase (don't assume not implemented) using Sonnet subagents. You may use up to 500 parallel Sonnet subagents for searches/reads and only 1 Sonnet subagent for build/tests. Use Opus subagents when complex reasoning is needed (debugging, architectural decisions). 2. After implementing functionality or resolving problems, run the tests for that unit of code that was improved. [...] 4. When the tests pass: [...] Then `git add -A` then `git commit` [...]. After the commit, `git push`. 5. SCOPE LIMIT: Complete ONE phase or logical unit of work per iteration, then commit, tag, push, and EXIT.

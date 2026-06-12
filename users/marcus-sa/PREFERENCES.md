---
name: marcus-sa-preferences
description: What triggers corrections, what satisfies marcus-sa, workflow habits and tool/stack preferences.
metadata:
  type: user
---

# Preferences: marcus-sa

## Pushback distribution

| Type | Rate |
|------|------|
| non_pushback | 54.4% |
| correction | 34.4% |
| failure_report | 8.6% |
| rejection | 1.6% |
| takeover | 1.0% |

One in three responses gets a correction. He rarely outright rejects (1.6%) but regularly points out a specific mistake.

## What triggers corrections

- **Wrong function/method name called**: Immediately notices `get_project_context` when it should be `get_task_context`. One line, a question mark.
- **Missed uncommitted changes**: After a deliver phase summary, he asks "what about all the uncommitted changes ?" if the agent declared victory without committing.
- **Architectural over-engineering**: Pushes back when the agent adds unnecessary layers, dependencies, or abstractions. "this is super convoluted....", "eliminate whats not needed", "it should not depend on onboarding either."
- **Mock tests instead of real integration**: "lmao, these integration tests are inherntly useless. not one of them tests how a coding agent would actually post the intent." He wants tests against real services, not mocked infrastructure.
- **Naming inconsistency**: Catches when an agent/component is named for its implementation rather than its role ("shouldnt we rename the orchestrator agent to chat agent?").
- **Half-baked tool implementations**: "why are the mcp tools defined for opencode only half baked? they're supposed to be 1:1 to the mcp server."
- **Auth fallback logic that bypasses security**: Blunt when the agent proposes a fallback that would weaken auth.
- **Using wrong SDK/built-in**: "why have we not used the built in functions from MCP SDK's built-in OAuth client ? it seems absurd that we have implemented this ourselves ?"

## What satisfies him

- Agent executes a `/nw:deliver` task end-to-end without intervention.
- Terse one-line acknowledgements ("Tool loaded.", "Continue from where you left off.") — these are non-pushback continuations, not enthusiasm.
- When he says "yes" to a point then corrects the next one — the "yes" is genuine acceptance.
- Correct acceptance tests that assert specific counts, not loops over possibly-empty arrays.

## Workflow habits

**Planning:** Uses the nWave 6-wave framework (DISCOVER→DISCUSS→DESIGN→DEVOPS→DISTILL→DELIVER). Does not free-form plan; fires slash commands at the agent and expects the agent to read the wave's instruction file.

**Testing:** Acceptance-test-driven. Expects acceptance tests to run after every DELIVER phase. Demands tests not skip via `it.skip`. Prefers real services over mocks in acceptance tests; unit tests may use mocks via adapter interfaces. Frequently asks "any tests?" after implementation.

**Git:** Commits are frequent and granular. Common patterns: `commit`, `commit and push`, `commit fixes`, `commit and then try and tune`. Creates PRs by attaching a `PR instructions.md` file and saying `Create a PR`. Merges by asking agent to "Resolve any existing merge conflicts with the remote branch (main). Then, commit and push your changes."

**Debugging:** Attaches CI log files or pastes stack traces without commentary. Expects the agent to diagnose and fix. Minimal description: "Fix the failing CI actions. I've attached the failure logs." or bare "fix" with an attachment.

**Explanations:** Rarely asks for them. When he does, it's a pointed architectural question ("why is there a DEFINE FIELD directory ON agent_session?", "but how does litellm actually proxy to upstream mcp servers?"). He doesn't want docs written — he wants a 1-2 sentence answer.

## Stack/tool preferences (inferred from prompts)

- **Runtime:** Bun
- **Language:** TypeScript
- **Database:** SurrealDB (graph-oriented, SCHEMAFULL tables)
- **AI SDK:** Vercel AI SDK (ai-sdk), Claude Agent SDK for orchestration
- **Testing:** Bun test, acceptance tests in `tests/acceptance/`, evals via evalite
- **CI:** GitHub Actions, ubicloud runners
- **Auth:** OAuth 2.0, DPoP, RAR — no API keys if possible
- **Frontend:** React with shadcn/ui + Tailwind
- **Config location:** `$HOME/.brain/config.json`
- **Agent orchestration:** Conductor (Mac app), nWave workflow
- **No mocking of DB or LLM calls** in acceptance/integration tests

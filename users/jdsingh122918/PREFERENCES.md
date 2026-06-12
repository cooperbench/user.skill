# Preferences: jdsingh122918

## Pushback Distribution

| Type | Rate |
|------|------|
| Non-pushback (accepts output) | 86.7% |
| Correction | 9.1% |
| Failure report | 3.8% |
| Takeover | 0.3% |
| Rejection | 0.1% |

Most sessions run smoothly. Corrections spike when: the agent offers partial scope instead of full scope, when the agent summarizes instead of providing detail, or when the plan has compile-time errors the agent missed.

## What Satisfies

- Agent produces working code with passing tests on first attempt
- Agent uses subagent teams (they almost always want this for multi-file work)
- Agent executes a spec or plan completely without asking for permission for each step
- Agent creates the PR after finishing work
- Agent provides scored/rated analysis with evidence (not just opinions)
- Short, action-confirming replies after large spec pastes

## What Triggers Correction

1. **Partial scope offer**: Agent asks "want me to fix issues 1 and 2?" instead of fixing all issues. User replies with "fix all X using agent teams" or "full scope".
2. **Agent asks for clarification on already-specified work**: If the spec was clear, the agent should execute it.
3. **Plan has compile errors**: User pastes the specific blocker with file+line reference; expects the agent to fix it before continuing.
4. **Agent summarizes rather than does**: "All three review agents are complete. Want me to implement?" → user replies "Lets implement all the recommendations using subagents".
5. **Wrong scope on UI redesign**: Agent proposes too narrow a UI change; user redirects to full reimagination.

## Workflow Habits

**Planning first**: Yes — uses a dedicated brainstorming skill and writing-plans skill that produces a `docs/superpowers/plans/YYYY-MM-DD-feature.md` file. Executes plans via "Execute the plan at docs/plans/..." rather than free-form direction.

**TDD**: Enforced via a SKILL loaded at session start. Tests precede implementation. AAA pattern. Tests in `mod tests` at bottom of each source file.

**Subagent delegation**: Strongly preferred for any task touching > 2 files or requiring investigation. Sends "use agent teams to" as a standing instruction. Parallel dispatching is standard, not exceptional.

**Commit cadence**: Commits at the end of a feature branch ("lets commit the changes to a branch and push the branch to remote"). Does not commit after every phase. Creates PRs after branch is ready ("lets create a PR for this branch").

**PR reviews**: Uses `/pr-review-toolkit:review-pr` slash command. Pastes the review output back as context for fixes. Expects fixes to be applied via agent teams.

**Error handling**: Cares deeply about silent failures. Frequently runs a "hunt for silent failures" agent on PRs. Looks for `let _ = ...`, bare `catch { return }`, swallowed `Result`s, `.ok()` on fallible paths.

**Library docs**: Loads Context7 MCP at the start of implementation sessions to verify current API versions. "use context7 mcp to cross check what versions of libraries are being used"

**Verification**: After fixes, says "verify it now" or "using agent-browser, lets execute the issue and verify that everything is working". Wants active verification, not just compilation success.

## Tool/Stack Preferences

- **Rust backend**: tokio, axum, serde, clap (derive macros), anyhow + thiserror v2, git2, libsql/Turso, tracing
- **Frontend**: React 19 + TypeScript, Vite, Vitest + RTL + MSW, Tailwind CSS
- **Agent tools**: Claude Code (primary), Codex CLI (for judge/cross-model verification), Context7 MCP for library docs
- **CI**: GitHub Actions with `-D warnings` Clippy enforcement
- **Docker**: Used for isolated development (`make dev`, `make factory`)
- **DB**: libsql with Turso for cloud sync; in-memory DB for tests

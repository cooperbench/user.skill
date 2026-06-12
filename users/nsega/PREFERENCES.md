# nsega — Preferences

## Pushback Distribution

- **non_pushback**: 63.6% — majority of the time nsega accepts or simply continues
- **correction**: 22.7% — redirects the agent with a different or more specific directive
- **failure_report**: 9.1% — reports a failure (CI failure URL, selecting a problematic option)
- **rejection**: 4.5% — flat refusal ("no."), rare but unambiguous

## What Triggers Corrections

1. **Agent starts implementing before creating a PR.** nsega's most frequent correction pattern: agent presents a plan/summary and begins work, nsega interrupts with "Create the pull request first, and proceed with the implementation."
2. **Agent fixes the wrong thing.** When offered diagnostic options, nsega selects a specific one rather than accepting the agent's default fix.
3. **Agent skips the plan step.** nsega wants plans written to `.claude/plan/` before code changes.
4. **README or docs are stale after refactoring.** Corrects with "update the REAME to the latest" / "update the README to the latest".

## What Triggers Flat Rejection

- Agent proposes a fix that nsega disagrees with entirely → "no."
- Immediately followed by a correction naming what he actually wants.

## What Satisfies nsega

- Agent follows the plan → PR → implement → commit-per-step sequence without prompting.
- CI passes (lint, build, tests all green).
- Verification confirms MCP tools work end-to-end.
- Agent correctly identifies the specific hook/issue nsega already suspected.

## Workflow Habits

- **Plan-first**: explicitly requests plan creation and storage at `.claude/plan/` before implementation begins.
- **PR-first**: creates the pull request before the first commit lands. Non-negotiable; corrects agent every time this is skipped.
- **Step-by-step commits**: instructs agent to commit and push after each discrete step, keeping the PR up-to-date incrementally.
- **Interrupts freely**: kills agent mid-action when he wants to redirect. Does not apologize or explain the interruption.
- **Does not write tests himself**: delegates test verification ("verify if this mcp works as expected", "Ensure lint, tests, build, and ci-jobs pass successfully.").
- **Does not ask for explanations**: zero requests for "explain why" or "how does this work" — only outcomes matter. The one "understand" session was a review request, not a learning request.
- **Delegates CI fixes by URL**: pastes the PR URL when Actions fail; expects the agent to read and fix without further context.

## Tool/Stack Preferences Visible in Prompts

- Go (slog, staticcheck, make, go build/test)
- MCP protocol (JSON-RPC, `tools/list`, protocol version negotiation)
- GitHub Actions for CI (lint + build/test matrix)
- Emacs + Elisp (vterm, tree-sitter, hook-based config)
- Claude Code as the sole agent (100% of sessions)
- `.claude/plan/` directory for plan persistence
- `settings.local.json` kept out of git, `settings.json` committed

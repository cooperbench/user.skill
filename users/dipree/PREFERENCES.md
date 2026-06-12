---
name: dipree-preferences
description: What dipree corrects, what satisfies him, workflow habits, and tool preferences.
---

# Preferences: dipree

## What triggers corrections (pushback distribution)

- **correction**: 32.8% — the most common pushback; triggered by agent misreading UX intent, missing files in commits, or implementing a workaround instead of the right behavior
- **failure_report**: 11.2% — pastes log output or CI errors verbatim after something silently fails; minimal framing ("nothing is happening", "doesn't seem to be right")
- **takeover**: 4.5% — fires "commit this" or "push it" when agent is summarizing instead of acting
- **rejection**: 2.2% — hard stop + revert when agent goes in a totally wrong direction ("Revert that", "Let's remove all that")

## What specifically triggers corrections

- Agent commits partial/incomplete changes ("There are many more uncommited changes?")
- Agent adds extraneous changes to CLAUDE.md or unrelated files without being asked
- Agent opens a new terminal tab instead of using existing session
- Agent hardcodes values that should come from config/settings
- UX validation missing — agent crashes on empty input instead of showing inline error message
- Agent skips files from commits ("Yes and commit")
- Branch naming doesn't match the actual feature ("Rename the branch, it's actually about adding trail functionality not removing")
- Docs out of date or redundant after code changes

## What satisfies dipree

- Agent executes git ops immediately without confirmation ("I like that the prompt structure is documented." — rare positive feedback)
- Agent correctly implements interactive CLI flows with inline validation
- Visibility into background processes: notifications/log messages that show what wingman is doing
- Clean lint + tests passing
- Draft PRs with precise functional descriptions

## Workflow habits

- **No planning phase unless it's big**: for large features, writes a full markdown plan himself and pastes it as "Implement the following plan:" — does not ask the agent to design
- **Constant commit cadence**: commits after nearly every agent action; does not batch work into fewer commits
- **Cross-repo debugging**: switches between `entireio/cli` and `entire-playground` or `entire.io` to test behavior
- **PR-driven**: creates draft PRs frequently, reviews Copilot/human comments and asks agent to address them
- **Does not write tests himself**: test intent is 0.7%; expects agent to handle test-related work if needed
- **Background task awareness**: forwards task completion notifications verbatim to the agent as his next prompt
- **Review file workflow**: uses `.entire/REVIEW.md` as an integration point — sometimes manually triggers "Read `.entire/REVIEW.md` and address each suggestion"
- **Verifies in sibling repos**: "Look into my cd ../entire-playground repo and analyse..."

## Tool / stack preferences

- Go (primary language)
- `mise` for task running (`mise run fmt`, `mise run lint`, `mise run test:ci`)
- `golangci-lint` v2 for linting (strict: ireturn rules, errcheck)
- GitHub PRs as the primary review surface
- Claude Code as the agent (sole agent used: 100%)
- Cobra for CLI commands
- Interactive TUI prompts (huh/bubbletea style)
- Shadow git branches for trail data storage
- `.entire/` directory for all tool state

## Agent interaction preferences

- Does not want confirmation dialogs for standard ops
- Does not want the agent to ask questions about unrelated uncommitted files — dismiss them
- Wants the agent to infer intent from context, not ask clarifying questions
- Wants background process visibility (systemMessage notifications, not context injection)
- Does not want new tabs opened or new windows spawned
- Prefers the agent to detect and fix its own CI failures before reporting

---
name: dipree-persona
description: Background, expertise, role, and attitude for dipree.
---

# Persona: dipree

## Role and background

- **Role**: Founder/IC (inferred) building `entireio` — a developer tool startup wrapping AI agent hooks into the git workflow
- **Seniority**: Senior–Staff (inferred): designs architecture unprompted, catches subtle phase-check bugs, knows golangci-lint rules, uses `mise`, writes Go with interfaces and subpackage structure
- **Domain expertise**: Go CLI development, git internals (hooks, branches, shadow branches, worktrees), Claude Code hook protocol (UserPromptSubmit, SessionStart, Stop), CI/CD (GitHub Actions, golangci-lint v2), interactive TUI flows (bubbletea/huh style multi-select prompts)

## Working environment

- macOS, zsh, hostname `dip`, user `dip` (inferred from log paths `/Users/dip/Repositories/`)
- Timezone UTC+1 (inferred from wingman.log timestamps)
- Uses `mise` as task runner (`mise run fmt`, `mise run lint`, `mise run test:ci`)
- Has multiple repos checked out: `cli`, `entire-playground`, `entire.io`, `entire.io-1`
- References sibling repos by relative path: `cd ../entire-playground`

## Language

- English only, but non-native markers present (inferred: possibly Dutch or German)
- Consistent typo fingerprint — not random errors, same words misspelled repeatedly
- Occasionally colloquial: "Fuck yes", "Mh...", "slop"
- Writes "Adress" consistently (never "address")

## Attitude toward the agent

- **Conditionally trusting**: hands the agent large spec plans and lets it run; doesn't micromanage implementation details
- **Quickly corrective**: when output deviates from expected UX or behavior, fires a correction immediately with a precise spec
- **Dismissive of agent noise**: ignores agent questions about unrelated files ("Ignore those."), doesn't answer meta-questions
- **Interrupts when misaligned**: uses `[Request interrupted by user]` and `[Request interrupted by user for tool use]` — not afraid to stop a bad trajectory mid-run
- **Sharp when quality is poor**: "Don't update or add anything to the CLAUDE.md with your slop."
- **Does not explain his reasoning** unless prompted; expects the agent to infer intent from context

## Annotated persona distribution

- Expert Nitpicker: 45.5% — catches UX edge cases, specifies exact validation behavior, notices behavioral regressions
- Vague Requester: 40.9% — fires one-liners expecting full execution ("Check the PR comments quickly")
- Mind Changer: 9.1% — revisits decisions mid-session, adjusts specs in real time
- Other: 4.5%

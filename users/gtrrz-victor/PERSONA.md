---
name: gtrrz-victor-persona
description: Background, expertise, role, and attitude for gtrrz-victor
---

# Persona

## Role and background (inferred)

Technical founder or senior IC (inferred) building `entireio/cli` as a commercial product under the `entireio` GitHub org. The tool integrates with AI coding agents via hooks and ships publicly via Homebrew (`brew install entirehq/tap/entire`). Victor manages releases with GoReleaser Pro, tracks issues in Linear, and ships to a real user base — this is not a side project.

## Technical expertise

- **Go**: Deep. References package paths, struct fields, function signatures, and line numbers from memory. Comfortable with `bufio`, `syscall`, interfaces, build tags, and `ldflags`.
- **Git internals**: Advanced. Designs shadow branches, worktrees, and branch naming schemes. Uses `go-git` and raw git plumbing.
- **TypeScript**: Functional. Writes e2e tests with the Anthropic Agent SDK and Vitest; integrates TypeScript hooks for OpenClaw.
- **Toolchain**: `mise` as task runner (`mise run fmt`, `mise run lint`, `mise run test:ci`), GoReleaser Pro for releases, PostHog for analytics, Linear for issue tracking.
- **macOS-first**: Paths like `/Users/gtrrz-victor/…`, mentions Homebrew, `brew update entire`.

## Attitude toward the agent

**Trusting but demanding.** He delegates large implementation tasks freely via plan dumps. But he reads the output carefully — correction rate is 48% — and sends precise technical objections when something is wrong. He does not explain his corrections politely; he states the problem and expects the fix. He sometimes pastes findings from a code review or simplifier tool verbatim and says "eval this feedback" or "do the critical duplicate code."

## Dominant annotated persona

**Expert Nitpicker** (70.1%): Catches edge cases, backward-compatibility issues, nil pointer risks, and subtle logic errors. His corrections reference specific function names, line numbers, and error scenarios.

## Secondary persona

**Vague Requester** (16.9%): Short opening prompts like "fix lint errors", "fix tests", "I am having problems if I start a claude session inside a folder…" with no reproduction steps.

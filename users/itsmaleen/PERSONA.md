# Persona

## Background (inferred)

itsmaleen is likely a founder or solo/early-stage engineer building developer tooling products. (inferred) The two repos — Dispatch (an AI agent command center) and Merry — are personal/company projects, not OSS contributions. The GitHub username and shell prompt `marlin@Marlins-MacBook-Pro` suggest this is a Mac-primary developer working locally on a MacBook Pro.

## Domain expertise

- **Electron app development**: Comfortable with electron-builder, IPC, preload scripts, WindowManager patterns, multi-window architectures.
- **Frontend (React/TypeScript)**: Works with Tailwind, virtual scrolling (`@tanstack/react-virtual`), component-level layout debugging.
- **CI/CD (GitHub Actions)**: Maintains macOS signing workflows, understands certificate/keychain mechanics (though debugging them is painful).
- **Backend**: SQLite, FTS5 full-text search, server bundling for packaged Electron apps, bun runtime.
- **AI tooling**: Building an agent command center product — understands agent sessions, thread memory, console line persistence as product features.

## Seniority signals

Mid-to-senior (inferred). Can reference external open-source projects to inform design ("look into how this project https://github.com/pingdotgg/t3code does memory management"), proposes architectural trade-offs ("I'm leaning towards some kind of lazy load"), and asks the agent to justify decisions ("why do we need an export functions?"). Does not write the code themselves in sessions — delegates implementation entirely to Claude Code.

## Role (inferred)

Founder-level IC. Building the product, making design decisions, managing CI, and merging/pushing to main themselves.

## Attitude toward the agent

**Trusting but impatient.** Gives Claude Code wide latitude (72.7% vague requester), rarely specifies file paths or implementation details up front. But when the agent goes wrong, corrects crisply. Does not micromanage on the happy path — just says "yes go ahead" or "start implementing." Escalates to structured planning when a debugging loop repeats without resolution: "Before making changes again, let's plan what needs to change."

## Tone

Informal, brief, occasionally upbeat ("cool cool commit and push"). Not effusive — skips thank-yous and "great job." Phrases like "can we..." and "let's..." signal collaboration rather than commands, but the register is casual, not formal.

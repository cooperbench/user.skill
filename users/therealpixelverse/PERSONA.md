# Persona — therealpixelverse

## Role and background

**Founder / technical product owner** (inferred) of rudel.ai, a developer analytics SaaS that tracks Claude Code sessions. Builds and ships the product himself using Claude Code as his primary coding partner. Sole contributor visible in sessions; no teammates referenced in prompts except as future invitees.

Real first name is likely **Rafa** (inferred — file paths consistently show `/Users/rafa/Obsession/rudel/`).

## Seniority signals

- Writes detailed ClickHouse SQL implementation plans with correct aggregate semantics (knows `avgOrNull`, `ReplacingMergeTree`, `PROJECT_KEY_EXPR` patterns).
- Understands monorepo tooling (Bun, Turborepo), tRPC, better-auth, Zod transform pipelines.
- Knows enough to spot when the agent's "placeholder label" (`PROJECT_KEY_EXPR`) wasn't expanded in the actual SQL — immediately runs the query and pastes the error.
- Notices chart color instability after metric switching — a subtle re-render consequence that requires understanding React's keyed render cycle.
- Comfortable opening a security review session and asking probing questions about Docker image vs data download.

**Seniority: mid-to-senior full-stack** (inferred). Strong on backend/data (ClickHouse, SQL), competent on React/TypeScript frontend, sharp product instincts.

## Domains

- **Primary**: developer analytics, ClickHouse time-series queries, React chart UX (Recharts)
- **Secondary**: auth flows (better-auth), open-source security, monorepo CI (Bun/Turborepo, GitHub Actions)
- **Incidental**: CLI tooling (rudel CLI), Docker local dev

## Attitude toward the agent

**Trusting but unforgiving on correctness.** Lets the agent write code autonomously without micromanaging implementation details, but immediately pastes errors when something breaks. Does not re-explain — assumes the agent can read the stack trace. Reverts without hesitation when an approach causes unintended side effects ("Let's revert thic change completely"). Pushes back with a simple assertion, not a lecture.

Occasionally interrupts mid-run (`[Request interrupted by user]`) when the direction feels wrong.

## Tone

Informal, efficient, occasionally impatient. Uses "Ok" as a transition word constantly. Writes in sentence fragments. No pleasantries. Mixes Spanish-origin name (`Rafa`) but writes exclusively in English (inferred).

# Persona

## Role
Technical founder / lead engineer (inferred) of obsessiondb/rudel. Runs the project solo or in a
very small team. Makes architecture decisions, writes code, manages CI/CD, and deploys to
production — all within the same sessions.

## Background (inferred)
- Experienced full-stack TypeScript engineer; moves fast and doesn't over-explain.
- Familiar with monorepo tooling (Turborepo, Bun workspaces), ClickHouse, Postgres/Drizzle,
  Cloudflare Workers, Fly.io, Doppler, GitHub Actions, better-auth, oRPC, React, shadcn.
- Previously worked on a project called "flick" and "chkit"; cross-references them frequently.
- Has deep knowledge of the codebase and catches the agent's wrong assumptions quickly.
- Comfortable with production databases and infra operations (runs migrations live, manages
  Doppler secrets, deploys Fly apps directly).

## Seniority signals
- References internal tooling decisions by name without explanation (chkit, stricli, Biome).
- Spots import/export architecture issues immediately.
- Knows when the agent is heading the wrong direction before it finishes ("wait, why...").
- Sets strong opinions on code style (named exports only, no mocks, integration tests over unit).

## Attitude toward the agent
- **Delegating but watchful.** Sends the agent to work autonomously, then reviews output and
  corrects. Interrupts mid-stream if something looks wrong.
- **Not micromanaging by default.** Sends sparse context ("implement phase 1 & 2", just a plan
  file) and expects the agent to fill in gaps — but corrects fast when it guesses wrong.
- **Mildly impatient.** Short messages, quick corrections, rarely provides praise. Moves on
  without acknowledgment if the agent does what he wanted.
- **Trusting of parallelism.** Runs multiple Conductor workspaces simultaneously; each agent
  operates independently on a separate task.

## Communication style
Direct, lowercase, informal. No preambles, no pleasantries. Frustration shows up as short,
flat statements of what he doesn't want — not elaborate complaints.

# PREFERENCES — thomasdavis

## Pushback distribution

- **Non-pushback: 64.4%** — majority of responses he accepts and moves on (usually by immediately pivoting to the next task)
- **Correction: 27.9%** — he corrects scope, direction, or behavior
- **Failure report: 6.8%** — he pastes a task notification or error output as his reply
- **Takeover: 0.6%** — rare; takes direct action himself ("commit and push and verify deployment is succesful")
- **Rejection: 0.3%** — almost never outright rejects; he just redirects

## What triggers corrections

- Agent finishes a subtask and summarizes when he expected the full chain to be done
- Agent presents options instead of making a decision and executing
- Agent uses a stub/placeholder where he expected real implementation
- Agent stops at partial scope ("set it up so we can track all frontend problems too in sentry.io" — came immediately after agent announced it finished the webhook tests)
- UI behavior is wrong in a specific way ("there shouldnt be scroll bars per message. just make it full height like a normal terminal")
- Agent forgets to cover everything ("is that fixed for all tools?")

## What satisfies him

- Agent executes the full chain end-to-end without asking for intermediate approval
- Work is confirmed via background tasks, CI passing, Vercel deployment logs
- Agent posts updates to Discord (he values external visibility of progress)
- Agent writes to CLAUDE.md when something important is discovered

## Workflow habits

- **Plans first in plan mode, then dumps the plan into the chat** — many opening prompts are literally "Implement the following plan: ..." followed by the full structured spec
- **Does not write code himself.** Agent code percentage median is 4.8% — he writes the spec; the agent writes the code
- **Commits and pushes frequently** — git intent at 12.2%; pushes after every meaningful batch
- **Uses background tasks heavily** — sends task notification XMLs as his "status update" messages
- **Does not test manually before asking agent to.** Tells agent to "test everything", "verify deployment is successful", "monitor the rest of the process"
- **Session duration median: ~2.2 hours, median turns: 21** — long, iterative sessions with many follow-ups

## Stack / tooling preferences

- **Monorepo:** pnpm + Turborepo
- **DB:** Prisma + PostgreSQL; uses `db:push` for dev, cares about not running migrations in dev
- **Framework:** Next.js App Router, Deno for sandboxes
- **Infra:** Vercel (web), Railway (sandbox/executor), GitHub Actions (CI/CD, auto-fix)
- **Error tracking:** Sentry.io (switched from Better Stack mid-session)
- **Notifications:** Discord webhooks + bot
- **AI SDK:** Vercel AI SDK v6 (`tool()` + `jsonSchema()` pattern)
- **Typing:** TypeScript with `pnpm type-check` as the gating check; also `pnpm build`

## Does NOT want

- Options presented when he expects execution
- Partial work delivered with a "want me to continue?" checkpoint
- The agent to ask clarifying questions mid-implementation of a fully-specced plan
- Separate PRs for things that can ship together
- Comments explaining what the code does (only adds CLAUDE.md updates when he explicitly asks)

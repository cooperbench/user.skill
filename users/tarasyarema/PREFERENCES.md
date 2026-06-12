# PREFERENCES — tarasyarema

## Pushback Distribution

| Type | Rate |
|------|------|
| Non-pushback (acceptance) | 83.5% |
| Correction | 13.8% |
| Failure report | 2.4% |
| Takeover | 0.1% |
| Rejection | 0.1% |

Most sessions run without correction. When he does push back, it's a correction (pointing out what was missed), not a rejection.

## What Triggers Corrections

1. **Inconsistent implementation coverage** — if `dir` field is added to `send-task.ts` but not to `task-action.ts`, `inbox-delegate.ts`, and two workflow nodes, he will forward the verification table showing every FAIL row. The signal: "all these tools/nodes create tasks via `createTaskExtended()`, which fully supports `dir`. The omission is inconsistent."

2. **Agent declares done too early** — "Adapter review: **all clear**." followed immediately by a task-notification showing the opposite. He doesn't argue; he just pastes the result.

3. **Missing unit/e2e coverage** — "yes pls. before that, did you create units tho? like what is the coverage of the changes?" He expects tests to exist before asking for more.

4. **Not using Docker when Docker was mentioned** — "y pls run w docker!" after agent ran only API-only mode.

5. **Planning agent that's too fast / too shallow** — "you did it so fast... can you check in the planning skill the subagenbts you need to use and ensure you spawn paralel agents to do the work and check specifics? the plan should be crystal clear on what needs to be implemented"

6. **Agent doesn't carry context across parts** — "make sure it applies to previus if makes sense!" — expects the agent to propagate decisions retroactively.

7. **Wrong scope on tests** — "the tests should be based on what was done in this PR! check rpi files" — wants tests grounded in actual changes, not generic.

8. **Not debugging before declaring ready** — "still see did not respond, this one nothing happened" — won't accept "try again" without investigation.

## What Satisfies

- Parallel sub-agents performing work (launches multiple agents simultaneously)
- Phase-by-phase implementation with verification after each phase
- Test results shown as pass/fail counts: "1498 tests passing, 0 failures"
- TypeScript clean compile confirmation: "TypeScript: ✓ Compiles without errors"
- Docker e2e with actual service spin-up (lead + worker + API)
- Plan files with clear phase structure and commit-after-each-phase discipline
- Clean verification reports with ✅/❌ per item

## Workflow Habits

- **Plan-first always** — writes a plan to `thoughts/taras/plans/<date>-<topic>.md` before implementing
- **Research before planning** — `desplega:research` → `desplega:create-plan` → `desplega:review` (plan) → `desplega:implement-plan` → `desplega:verify-plan`
- **Worktree branching** — works in `/Users/taras/worktrees/agent-swarm/<date>-<feature>/`; separate worktrees per feature
- **Commit after each phase** — explicitly asks for this: "commit after each phase"
- **Version bumping before push** — "bump tha version, commit the changes and push"
- **E2e scripts that are reusable** — "create a reusable script", "you may mock slack/github somehow with dummy events"
- **Does NOT ask for explanations** — never asks "can you explain how X works?"; understanding is shown through design decisions

## Stack Preferences Visible in Prompts

- **Runtime:** Bun (not Node): "code it in bun ts pls"
- **Testing:** `bun test`, Biome for lint, TypeScript type checking
- **DB:** SQLite with `bun:sqlite`, migration files in SQL
- **Docker:** Dockerfile.worker, docker-compose, `docker-entrypoint.sh`
- **OAuth:** `oauth4webapi` (chosen over `simple-oauth2`)
- **Schema validation:** Zod everywhere
- **Agent framework:** `desplega:*` and `rpi:*` custom skills
- **Autonomy modes:** Autopilot / Critical / Verbose on implementing skill

## Autonomy Preference

- Defaults to **Critical** for implementation ("don't prompt - implementation is more straightforward")
- Uses **Autopilot** for well-scoped research and planning tasks
- Verbally grants autonomy: "implement all phases consecutively without pausing between phases"

---
name: jukellam-preferences
description: What jukellam corrects, what satisfies him, workflow habits, and stack preferences.
---

# Preferences

## What triggers corrections (30% of turns)

**Agent commits before updating docs.** The most reliable correction trigger: if the agent completes a phase and moves to commit without first updating `CLAUDE.md` and the migration plan markdown, jukellam will stop it and demand the update. He made this explicit and told the agent to add it to `CLAUDE.md` as a standing instruction.

**Agent misidentifies the goal.** When the agent builds the wrong thing (trading system infrastructure when he wanted the startup draft UI), he issues a longer correction that references the authoritative document: "Reference the brainstorm document that spells out what we're trying to do." He does not yell; he reorients calmly.

**Agent asks clarifying questions with an empty feature description.** If a slash-command workflow asks "What would you like to plan?" when the feature description tag is empty, he responds with the reference document or brainstorm name, not a full description: "use the brainstorm document about startup draft."

**Agent does not mark completed plan items.** After completing work, he expects plan files to be updated to reflect progress ("update the plan to mark those background task items as done").

**Subagent output lands with analysis he wants applied.** He pastes entire subagent code-review findings (CRITICAL, High Priority, Medium Priority sections with SQL examples) back as correction prompts. This is his way of directing the agent to incorporate specific technical recommendations into the plan or implementation.

## What satisfies him

- Phase completes fully, all tests pass, committed and pushed in one agent turn.
- Numbered test results table shown ("48/48 ✓", "119/119 ✓").
- Agent asks clarifying questions before starting a big phase (he explicitly requested this).
- Agent documents solutions in `docs/solutions/` after major features.
- Agent keeps `CLAUDE.md` up to date after each phase.

## Workflow habits

- **Plan-first**: Uses `/workflows:plan` before `/workflows:work`. Expects a plan file in `docs/plans/` with dated filename before implementation starts.
- **Phase-by-phase execution**: Never asks for everything at once. Advances one phase per agent turn. Gives explicit go-ahead ("Let's do Phase C") before each.
- **Interrupt-and-pivot**: Regularly interrupts with `[Request interrupted by user]` when he wants to change direction mid-run. Does not wait for the agent to finish.
- **Light manual testing between phases**: Does his own "light testing" on the running app, then gives go-ahead for the next phase.
- **Windows cross-platform testing**: Occasionally tests on a Windows machine and reports platform-specific failures.
- **Solution documentation after completion**: Uses `/workflows:compound` to document recently-solved problems in `docs/solutions/` while context is fresh.
- **No active data migration**: When asked about existing state to migrate, the answer is always "no active state needs to be migrated" or "No, no active draft."
- **Delegates test writing**: Never writes tests himself; always asks the agent to "add pytest testing and manage that as we go."
- **Prefers one PR per feature phase**: Ships work as PRs (PR #1, #2, #3…). Reviews PRs using `/workflows:review PR#N`.

## Stack and tool preferences

- **FastAPI + SQLite** (WAL mode). No migration to Postgres.
- **Resend SDK** for email. Has a domain configured.
- **Render** for deployment. Uses `render.yaml`.
- **pytest** for testing.
- **compound-engineering plugin** for all workflow orchestration. Knows the slash commands fluently.
- **Jinja2 templates** for server-rendered HTML (not a SPA).
- **WebSockets** for real-time draft updates.
- No Docker mentioned. Runs locally with `uvicorn`.
- **Entire** (context tracking tool) added to the repo.
- Does NOT want the agent to use `--no-verify` or skip hooks.

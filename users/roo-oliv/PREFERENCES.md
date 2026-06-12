# Preferences — roo-oliv

## Workflow

**Planning before execution** — roo-oliv uses Claude Code's plan mode to write a full implementation spec (root cause, file paths, line numbers, code snippets, verification steps) before ever asking for code. The agent receives a finished plan, not a problem to solve. This means they never ask "what do you think we should do?" — they've already decided.

**Verification by running the game** — After each implementation, they run the game and report back with logs or screenshots. They do not accept "build succeeded" as done. Real verification = observable behavior in the running program.

**Short sessions, high density** — Median 4 turns, ~9.5 minutes. They don't iterate extensively; they come in with a plan, watch it execute, and either accept or correct once.

**No explanations wanted** — They paste complete implementation specs themselves. They do not ask the agent to explain architecture or suggest approaches. If they want reasoning, they write it in the plan.

**Git is transactional** — Commits and pushes are issued as terse follow-up commands the moment code is ready, not as part of the implementation session.

## What triggers pushback (19% failure report, 9.5% takeover, 4.8% correction)

| Trigger | Behavior |
|---------|----------|
| Code compiles but runtime is broken | Pastes raw logs + one-sentence diagnosis hypothesis |
| Visual bug visible in running game | Attaches macOS screenshot, describes what differs from expected |
| Text/UI element wrong color or z-order | Mentions "same color as background" or "drawn underneath it" as hypothesis |
| Agent pauses waiting for confirmation | Issues next command directly (takeover), skipping acknowledgment |
| Partial success | States exactly what works and exactly what doesn't — never "it's broken" |

## What satisfies them

- Agent implements the plan exactly as specified, with no scope creep.
- Build passes: `dotnet build … — 0 errors`.
- Visible behavior matches the plan's verification checklist.
- Satisfaction expressed by immediately issuing the next task (no praise).

## Stack and tool preferences (visible in prompts)

- **Language**: C# / .NET, MonoGame, DefaultEcs ECS framework.
- **Build**: `dotnet build <ProjectName>.csproj`.
- **VCS**: Git via `gh` CLI for PRs, SSH remotes.
- **OS**: macOS (osascript for notifications, screenshot paths in Portuguese).
- **Editor / IDE**: Claude Code (plan mode heavily used).
- **No testing framework**: Only 3.6% test intent; verification is manual runtime observation.
- **Code style preference**: Targeted, minimal changes — they specify exact line numbers and minimal diffs.

## Delegation vs. specification

roo-oliv specifies precisely and delegates execution only:
- **Never delegates**: Root cause analysis, architecture decisions, file selection, approach.
- **Always delegates**: Writing the actual code changes, running builds, creating commits/PRs.

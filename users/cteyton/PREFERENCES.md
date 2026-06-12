# Preferences: cteyton

## Pushback distribution

| Type | Rate | What it means |
|------|------|---------------|
| Non-pushback | 66.7% | Agent did what was asked; cteyton sends "commit" or moves on |
| Correction | 17.1% | Agent got the logic right but a specific detail is wrong (label, path, wording) |
| Takeover | 10.1% | Agent talked instead of committing; cteyton sends "commit" and does it themselves |
| Failure report | 6.1% | Something broke at runtime; cteyton pastes logs |

## What satisfies cteyton

- Implementation that exactly matches the spec — file paths, line numbers, variable names as specified.
- A commit that happens immediately after `"commit"` with no preamble.
- Changelog updates automatically included when asked (`"commit and update changelog"`).
- Verification steps that run (`bun run test`, `bun run lint`, `bun run typecheck`) and pass silently.
- Agent that reads file paths from `@filename` references without being told the full path.

## What triggers correction

- Wrong label text in the UI: `"Claude Rule should appear as 'Claude Rule', not just 'Rule'"`.
- Missing edge case in a list: `"Mention that github also create '.github/instructions' and '.github/skills'"`.
- Wrong agent/provider shown in a modal: `"the modals shows me 'copilot'"` when Cursor was selected.
- Agent summarizing its own changes at length instead of committing.
- Files displaying under wrong agent section in the UI.

## What triggers failure report

- Runtime exceptions pasted verbatim: `TypeError: undefined is not an object`, `ENOENT`, `ContextError: useContext returned undefined`.
- CLI process failures with exit code 1, empty stdout/stderr.
- DB not updating when API call succeeds: `"It only logs score but it's not updated in DB"`.
- UI showing wrong data after an action: `"Are you sure? Check http://localhost:3000/evaluation/..."`.

## Workflow habits

- **Plan-first, always**: cteyton writes the full implementation plan in plan mode before starting a session. The agent almost never designs; it executes.
- **No iterative design**: Design decisions are pre-made and stated in the plan (`"## Design Decisions (confirmed with user)"`). The agent should not propose alternatives.
- **Verification is mandatory**: Every plan includes a `## Verification` section with `bun run test && bun run lint`. The agent is expected to run these before reporting done.
- **Commit cadence is high**: 27.7% of all prompts are git operations. After every significant change, cteyton asks to commit, often also updating the changelog.
- **No explanations needed**: cteyton never asks "how does this work?" or "why did you do that?". `understand` intent is only 0.4% of sessions.
- **Debug intent is workflow, not crisis**: 9.7% debug. cteyton pastes logs and expects a fix, not a diagnosis walkthrough.
- **Multi-agent workflow**: Occasionally runs parallel agents and re-syncs: `"Another agent worked on your files, he has finished, update your context and continue"`.
- **Interrupts liberally**: Cancels the agent mid-response when they switch to a tool or change their mind. Follows up with `"continue"`.

## Stack preferences (visible in prompts)

- **Runtime**: Bun (`bun run test`, `bun run lint`, `bun run typecheck`, `bun run dev`)
- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: TypeScript with Bun.serve, SQLite
- **Test runner**: `bun test` (1200–1324 tests in suite)
- **Linter**: Biome (`bun run lint`)
- **Build**: `bun run css:build` for Tailwind
- **AI agent CLI flags**: `--output-format json`, `--dangerously-skip-permissions`, `--model haiku`
- **File references**: Uses `@filename` prefix when directing the agent to a specific file
- **Debug mode**: `?debug=true` URL param to gate internal UI features

## Remediation domain conventions (project-specific)

- AGENTS.md is source of truth; CLAUDE.md should only contain `@AGENTS.md` when both coexist.
- Skills in `.claude/skills/`, `.agents/skills/`, `.github/skills/`, `.cursor/skills/`.
- Standards (rules) vs. skills: decisions made at prompt-design time, not left to the agent.
- Changelog (`CHANGELOG.md`) updated with every feature commit.

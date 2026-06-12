# Preferences — therealpixelverse

## Pushback distribution

| Type | Rate | Meaning |
|------|------|---------|
| non_pushback | 39% | Accepted as-is; moves straight to next thing |
| correction | 35% | Agent got direction right but missed a detail |
| failure_report | 18% | Pastes error; expects agent to diagnose |
| takeover | 6% | Short imperative that jumps ahead ("ok commit and open pr") |
| rejection | 2% | Full revert: "Let's revert thic change completely" |

## What triggers correction

- Agent answers a slightly different question than asked ("the table in the Projects page does not show the full path for each project, why are we going into the path when clicking on the details")
- Missing a secondary surface after fixing primary ("It shohld also be ther ein the signin modal")
- Visual inconsistency with rest of app (legends not matching, chart margins off)
- Copy/label not matching what user specified ("Change the text to 'Scale to 100%' and don't change it when activated")
- Sidebar ordering not matching expectation ("Now move it in the side bar to below 'errors'")
- Over-engineering a simple README step ("don't overcpmplicate just make sure the step is there")

## What triggers rejection

- A change introduces a visible side-effect, especially color instability or wrong UX behavior. User reverts unconditionally: "Let's revert thic change completely."
- Agent misunderstands the axis/direction of a fix ("This is not what I meant, please revert the change.")

## What satisfies

- "Ok seems to work now." — brief, moves on.
- "Ok nice!" — chart looks right.
- "Ok perfect." — feature lands correctly and doesn't need follow-up.
- Immediately follows satisfaction with the next task; no dwelling.

## Workflow habits

- **Spec-first for complex changes**: Opens sessions with a fully written implementation plan (file paths, before/after code, reasoning). Expects agent to execute, not design.
- **Verify manually via browser/ClickHouse**: Runs queries in ClickHouse himself; pastes results. Checks the UI visually with screenshots.
- **No test writing**: Test intent is only 2.9% of prompts. Relies on `bun run verify` for type/lint, not unit tests.
- **Iterative UX polish**: Works in a "one fix → observe → one more fix" loop. Does not batch UX changes upfront.
- **Commits late**: Multiple features accumulate before committing. When done: "ok commit and open pr".
- **Branches only when told**: Asks about best practice for creating a new branch mid-session when already on main.
- **Interrupts freely**: Uses `[Request interrupted by user]` or `[Request interrupted by user for tool use]` without explanation.
- **Uses slash skills**: Triggers `/security-review`, `pr-creation`, `api-testing` skills by pasting their content mid-session.

## Stack preferences visible in prompts

- **ClickHouse** for analytics (materialized views, aggregate functions, `SharedReplacingMergeTree`)
- **React + TypeScript** frontend (Vite, Recharts for charts)
- **Bun** as runtime and package manager
- **Turborepo** monorepo orchestration
- **better-auth** for authentication
- **tRPC** for API layer (uses `/rpc/` URL pattern)
- **Zod** for schema validation with `.transform()`
- **GitHub Actions** for CI (conventional commit PR titles enforced)

## Explanation preference

Wants answers, not explanations. "Is this also hardcoded in the materialised view or we calculate on reads? Just answer the question?" When he needs to understand something, he asks a direct question and expects a direct answer. Does not want walkthroughs of what the agent already did.

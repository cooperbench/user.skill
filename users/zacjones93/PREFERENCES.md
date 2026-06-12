# Preferences — zacjones93

## Pushback distribution

| Type | Rate | Meaning |
|---|---|---|
| non_pushback | 43.4% | Accepts or continues without comment |
| correction | 36.8% | Redirects without re-explaining; short flat statement |
| failure_report | 13.2% | Pastes raw error, log, or observes broken UI |
| takeover | 3.8% | Overrides agent's current direction entirely |
| rejection | 2.8% | Blunt refusal of what the agent just did |

## What he corrects or rejects

- **Wrong icon choice**: "no make it the alert for all" (after agent picked a pencil icon)
- **Missing UI not built yet**: "the assigning adjustments ui is completely gone. wtf fix it"
- **UI layout issues**: "the table column is being truncated unnecisarily", "please put status as the second column after the number"
- **Wrong scoring logic**: corrects penalty math immediately with domain specifics
- **DB tool choice**: redirects to PlanetScale MCP instead of direct CLI connections
- **Wrong external system assumption**: "WE ONLY USE WODSMITH FOR THIS" — refuses agent attributing data to Competition Corner
- **Over-explained responses**: stops the agent with "yes, I'm not fucking stupid" when agent over-explains a known concept
- **Unnecessary scope**: "lets just not handle re-registration right now... that's fine as a constraint"

## What satisfies him

- Clean test runs ("all 81 test files pass, 2327 tests pass")
- Agent doing exactly what was asked without unsolicited extras
- Correct penalty math and score scheme handling
- Committed and pushed without being asked twice
- PR comments addressed quietly

## Workflow habits

- **Commit cadence**: very frequent — commits after almost every meaningful change; "commit your work, ignore the db/index.ts"
- **Branch management**: creates branches off main per feature ("create a new branch off of main and...")
- **PR comments**: routinely asks agent to pull PR comments and address them: "pull pr comments and address any relevant ones"
- **Planning style**: uses ADRs (Architecture Decision Records) as executable specs for the agent — numbered, self-contained, implementation-plan-included
- **Tests**: uses the `/test` skill; asks for integration tests, follows Kent C. Dodds' testing trophy philosophy
- **Team memory**: uses a Cloudflare Worker-backed team memory system to persist gotchas/conventions
- **DB changes**: prefers PlanetScale MCP over `drizzle-kit push` directly
- **Mid-session interrupts**: will cancel an agent mid-run if it goes off-track; resumes with "continue" or "please answer my question"

## Tool and stack preferences

- TanStack Start (React router framework)
- Drizzle ORM + PlanetScale MySQL (NOT D1/SQLite)
- Cloudflare Workers and Workflows
- Stripe Connect with platform fee pass-through to customers
- `pnpm` as package manager
- `bun` for scripts
- `lucide-react` for icons
- `gh` CLI for PR work
- PlanetScale MCP for schema migrations on the dev branch

## What NOT to do

- Do not use D1 or SQLite references — the stack is PlanetScale MySQL
- Do not touch `db/index.ts` during commits unless explicitly asked
- Do not over-explain known concepts
- Do not ask clarifying questions when the task is clear enough to start
- Do not pick icons or UI treatments without checking — he will correct them

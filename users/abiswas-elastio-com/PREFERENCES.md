# Preferences

## What triggers corrections (34.8% of prompts)

- **Agent misreads state** — "no, 5 are in todo swim lane and 9 are done" (agent said all 14 were done)
- **Wrong task URLs** — "wait i meant https://taskai.cc/app/projects/1/tasks/17 https://taskai.cc/app/projects/1/tasks/16 https://taskai.cc/app/projects/1/tasks/15"
- **Agent skips deploy step** — "is it deployed to prod? do it and close all tasks"; "it is healthy but did we cimmit, start ci cd pipeline and thewn promote to prod"
- **Feature placed in wrong location** — "actually, wait, it should not be in settings, make it another tab in navigation called Assets"
- **Wrong CI system** — "we use travis, right?"; "we should not be using github at all, this should be fully travis"
- **Agent uses wrong credentials/email** — "use anshuman@biswas.me for this project"
- **Scope creep or wrong staging** — "but also make sure it should be staging and prod, uat is optional unless I explicitly mention it"
- **Performance regression** — "ok, both the API and web tests are taking more than a minute, optimize it please"

## What triggers failure reports (13% of prompts)

- Live URL returning 500 errors or wrong JSON
- Login broken after a migration
- CI pipeline still running when agent said it was done
- Backup not working
- UI changes not visible after deploy

## What satisfies them (50% non-pushback)

- Agent completes the full deploy chain without being asked
- Tests pass and coverage numbers reported
- Tasks closed in TaskAI after completion
- Concise status summary (not verbose) after large tasks
- Agent reuses existing code patterns correctly (e.g., `TestServer` pattern, `copyToClipboard`)

## Workflow habits

**Planning first:** Yes — for large features, pre-writes full "Implement the following plan:" specs with step numbers, file paths, code snippets. Then pastes the entire plan to kick off the session.

**Test-driven:** Cares strongly about coverage (target 80%); uses SonarQube for visibility. Frequently opens sessions with "please fix the remaining tests" or "I want you to figure out a way to write high-quality tests."

**Commit cadence:** Expects commits after logical units of work, not at the end of sessions. After a commit, expects staging deploy + promotion to prod to follow automatically.

**Does NOT ask for explanations:** Issues directives. Receives long structured summaries from subagents without reading them carefully — uses them as continuity artifacts. Will interrupt mid-summary.

**Delegates broadly but audits outcomes:** Gives agent full infrastructure access (SSH, Cloudflare, GitHub Actions) but checks health endpoints, CI logs, and live URLs to verify.

**Dogfoods own product:** Creates tasks in TaskAI to track development work, expects agent to close them via the MCP API. "please solve the tasks\nhttps://taskai.cc/app/projects/1\nThen comment and close"

## Tool/stack preferences

- **CI/CD**: Travis CI (not GitHub Actions for deploys — corrects agent when it uses GitHub)
- **Deploy flow**: `./script/server deploy` → staging → `./script/server promote` → prod
- **Frontend testing**: Vitest (not Jest), Playwright for E2E
- **Linting**: Biome (not ESLint+Prettier), golangci-lint
- **Database**: SQLite for early dev, Postgres for production scale
- **MCP**: Cloudflare MCP for DNS ops, buildme MCP for build tracking, own taskai MCP for task management
- **Code quality**: SonarQube at `sonar.taskai.cc`
- **Media storage**: Cloudinary (user-supplied API keys per project)
- **Real-time**: Yjs + WebSocket + Node.js microservice for collaborative editing

## Interrupts

Interrupts the agent often ("[Request interrupted by user for tool use]"). Does not explain — just resumes with a corrective message or "keep going". Interruption density is high (~10% of all prompts are interrupts), especially during long automated operations.

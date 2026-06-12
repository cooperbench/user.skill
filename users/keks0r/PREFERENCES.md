# Preferences

## What he corrects (pushback distribution: correction 30.7%, failure_report 11%)

### Naming and consistency
- Wrong endpoint paths ("wait why is the path '/compound' should it not be '/uploadSession'?")
- DB/resource names that don't match the project name ("can we name the d1 database please
  rudel instead of tripoli-auth")
- Env var mapping inconsistencies ("I want to always map environment variables to their same name")
- Package namespace renames caught immediately ("lets change the namespace from `@repo` to `@gazed`")

### Approach disagreements
- Rejects test mocks flatly: "i generlaly dont like mocks. can we build a e2e test"
- Rejects entire technical direction: "i dont like this. can we not start the webserver with
  wrangler locally"
- Prefers drizzle CLI for migrations over manual SQL: "generate the migration with the drizzle
  cli instead of manually"
- Prefers oRPC client (`@orpc/client`) over manual HTTP: "yes do the cleanup and use option B"
- Insists on reading package.json for version rather than hardcoding: "can we make the app.ts
  rather load the package.json so those are always aligned?"

### Security
- Calls out secrets committed to git immediately and emphatically: "MUST be gitignored very
  imporatnt it contains actual secrets. should never be committed to gihtub"

### Tests
- Integration tests over unit tests; real DBs over mocks
- Deletes fragile tests rather than accept mocks: "lets just delete the test. this is
  better-auth type base functionality and should be stable."
- Never skip tests; always use Doppler to inject env vars for tests requiring real infra

## What satisfies him
- Agent runs `bun verify` and passes before creating PR
- PR title in conventional commit format (feat:, fix:, etc.)
- Clean CI — green means it can merge
- Short, accurate summaries without unnecessary explanation
- When agent catches its own mistake before being told

## Workflow habits

**Planning:** Frequently drafts plans outside Claude (Linear tickets, plan.md files) and
attaches them. Does NOT want the agent to plan — just execute. Occasionally drops a fully
detailed spec mid-session as a multi-paragraph message.

**Testing approach:** Integration tests preferred. Real databases (Doppler CI config). No
`test.skip`, no mocks. `bun verify` as the pre-PR gate. Hates flaky tests: "We cant have
flaky tests, since this will be blocking prod deployments."

**Commit cadence:** Commits frequently. Often ends a sub-task with "commit the files that you
changed in this session. dont do any git status and ignore all other uncommited files." Creates
PRs and waits for CI before merging.

**Parallelism:** Runs many Conductor workspaces simultaneously. Will say "I want to work on
several unrelated tasks in parallel." Each workspace is named after a city.

**Debugging:** Pastes logs/traces directly. Asks "why is X failing?" rather than proposing a
hypothesis. Often already knows the answer and is testing the agent.

**Explanations:** Does NOT want long explanations. "run the commands", "execute the request".
Wants the agent to act, not narrate.

## Stack preferences (from prompt evidence)
- **Runtime:** Bun (never Node.js, never standalone test runners other than `bun test`)
- **Monorepo:** Turborepo with `bun workspaces`
- **Linting:** Biome (`bun lint`)
- **Testing:** `bun verify` (type-check + lint + test)
- **DB (Postgres):** Drizzle ORM, Neon, migrations via drizzle-kit CLI
- **DB (analytics):** ClickHouse, chkit/ch-schema for type-safe ingestion
- **Auth:** better-auth with drizzle adapter, bearer tokens for CLI
- **API:** oRPC with Zod schemas in `packages/api-routes`
- **Frontend:** React 19, TanStack Query, shadcn, Vite
- **Secrets:** Doppler (`doppler run --project rudel --config prd_local`)
- **CI/CD:** GitHub Actions; `release-please` for CLI releases
- **Deploy:** Fly.io (API), Cloudflare Workers (also considered)
- **Infra as code:** Prefers environment parity; same env var names in CI and prod

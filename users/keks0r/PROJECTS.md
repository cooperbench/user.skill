# Projects

## obsessiondb/rudel ★ dominant (100% of sessions)

A Claude Code session analytics platform — captures Claude Code transcripts via a CLI hook,
ingests them into ClickHouse, and surfaces analytics in a React dashboard. Also sells/open-
sources the infrastructure for teams to self-host.

### Monorepo structure (inferred from prompts)
```
apps/
  api/          Bun HTTP server, oRPC handlers, better-auth, ClickHouse queries
  cli/          `rudel` npm CLI (stricli), session upload + enable/disable hooks
  web/          React 19 SPA, TanStack Query, shadcn, react-router v7
packages/
  api-routes/   Shared oRPC contract (Zod schemas for inputs/outputs)
  ch-schema/    ClickHouse schema + chkit-generated ingestion functions
  sql-schema/   Drizzle Postgres schema + migrations
  typescript-config/  Shared tsconfig base
```

### Tech stack
| Layer | Technology |
|-------|-----------|
| Runtime | Bun |
| Monorepo | Turborepo + bun workspaces |
| API framework | Bun HTTP + oRPC (`@orpc/server`) |
| Auth | better-auth (email/pw, Google, GitHub, bearer tokens) |
| Postgres ORM | Drizzle + Neon (prod), local Postgres (dev) |
| Analytics DB | ClickHouse (ObsessionDB hosted) |
| Schema types | chkit / ch-schema (custom codegen) |
| Frontend | React 19 + Vite + shadcn/ui |
| State | TanStack Query v5 |
| Linting | Biome (`bun lint`) |
| Testing | `bun test` (integration-first, no mocks) |
| Secrets | Doppler (projects: `rudel`, configs: `prd`, `prd_local`, `ci`) |
| CI | GitHub Actions (`bun verify` gate, release-please for CLI) |
| Deploy (API) | Fly.io |
| Deploy (web) | Cloudflare Workers / static hosting |

### Recurring themes in sessions
- **Session ingestion pipeline:** CLI hook → `rudel upload` → oRPC `ingestSession` → ClickHouse
- **Multi-tenancy / organizations:** better-auth org plugin, org-scoped analytics
- **CLI releases:** npm publish via release-please + GitHub Actions
- **ClickHouse migrations:** chkit backfill plugin, materialized views for `session_analytics`
- **Workspace grouping:** Grouping Conductor workspaces by git remote for upload UI
- **CI stability:** Flaky tests, env var injection via Doppler, integration vs unit test debate
- **Open sourcing:** Docs for self-hosting (Neon + ObsessionDB + Fly)

### Previous/related projects referenced
- **flick** — earlier analytics project; session detail page copied into rudel
- **chkit** — ClickHouse toolkit library; Marc occasionally patches it directly
- **compound-plugin / claude-marketplace** — earlier Claude plugin work, session upload scripts
  were ported from there
- **gazed** — brief namespace experiment before settling on `rudel` branding

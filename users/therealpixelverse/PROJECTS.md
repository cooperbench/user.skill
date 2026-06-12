# Projects — therealpixelverse

## obsessiondb/rudel ★ dominant (100% of sessions)

**What it is**: A SaaS analytics dashboard for AI coding sessions — specifically Claude Code sessions. Tracks tokens, costs, productivity, error rates, session duration, and contributor breakdowns. Hosted at `app.rudel.ai`. Open-sourcing is planned.

**Tech stack**:
- **Database**: ClickHouse (analytics, materialized views) + PostgreSQL (auth/user data)
- **Backend**: Bun, tRPC (`/rpc/` routes), better-auth, Zod
- **Frontend**: React, TypeScript, Vite, Recharts (charts), Tailwind (inferred)
- **Monorepo**: Turborepo, Bun workspaces
- **Packages**: `apps/web` (React dashboard), `apps/api` (Bun API server), `apps/cli` (rudel CLI), `packages/api-routes`, `packages/sql-schema`, `packages/ch-schema`
- **CI**: GitHub Actions, conventional commit PR titles enforced, `bun run verify` (lint + type-check + tests)
- **Local dev**: Docker Compose spins up Postgres + ClickHouse locally; `bun run dev:local`

**Recurring themes**:

1. **ClickHouse query debugging** — `PROJECT_KEY_EXPR` / `PROJECT_DISPLAY_EXPR` constant SQL expressions that expand into ClickHouse functions; fragile when data shapes vary (Windows paths, missing git remotes). Recurring 500 errors from aggregate-with-no-GROUP-BY returning `nan`.

2. **Chart UX consistency** — Recharts-based charts must all follow the same legend (right side, vertical, scrollable), x-axis label (no overlap, padded below axis line), stacked bar over stacked area, max 15 series with 15th as "Other". The user nitpicks any chart that deviates.

3. **Project path normalization** — Windows backslash paths (`c:\Personal\...`) break `splitByChar('/', ...)` in ClickHouse. Normalized at ingestion via Zod `.transform()` and at query time via `replaceAll()`.

4. **Open-source security** — Planning to open-source; audited for hardcoded org IDs, production credentials, and data exposure in local dev. Ran `/security-review` skill.

5. **Organization management** — Invite flow (org owners only), share URL UX, README instructions for onboarding teammates.

6. **ROI calculator** — Page computing developer productivity value and cost from token spend; uses hardcoded Sonnet 4 pricing as approximation; has `Weekly Cost Trend` chart and per-project/per-developer tables.

**Key files referenced**:
- `apps/web/src/pages/dashboard/ProjectsListPage.tsx` — project navigation bug
- `apps/api/src/services/project.service.ts` — `PROJECT_DISPLAY_EXPR`, `getProjectDetails`
- `packages/api-routes/src/index.ts` — `IngestSessionInputSchema` with path normalization
- `apps/cli/src/bin/cli.ts` — upload CLI (entry point path changed)
- `apps/web/src/components/charts/DimensionAnalysisChart.tsx` — dimension split charts
- `apps/web/src/pages/dashboard/OrganizationPage.tsx` — invite flow

**Local dev notes** (from sessions):
- API: `http://localhost:4010`
- Web: `http://localhost:4011`
- ClickHouse: `localhost:8123` (default, not exposed to internet)
- Upload: `rudel upload --endpoint http://localhost:4010/rpc`

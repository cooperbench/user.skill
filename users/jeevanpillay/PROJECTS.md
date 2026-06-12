# Projects — jeevanpillay

## lightfastai/lightfast ★ dominant (81.8% of sessions)

**What it is**: A developer intelligence platform that ingests events, builds entity graphs, and surfaces them through a Next.js app and platform API. Includes a monorepo with `apps/app`, `apps/platform`, `apps/www`, and a suite of `packages/` and `vendor/` libraries.

**Tech stack**: Next.js 15, tRPC, Tanstack Query, Inngest, Clerk (auth), Sentry, oRPC, Radix UI, Tailwind, Biome, Turborepo, Drizzle ORM (inferred), Pinecone (vector search), SuperJSON, pino (structured logging).

**Recurring themes**:
- **Observability architecture**: Correlation IDs, tRPC middleware, Inngest middleware, Sentry integration, structured logging. Major ongoing workstream.
- **Error propagation**: tRPC ParseError adoption, client vs. server error routing to Sentry, consolidating EXPECTED_TRPC_ERRORS pattern.
- **Entity-first UI**: Migrating from raw ingest logs to enriched entity graph view. Entity list + entity detail with realtime updates.
- **API layer consolidation**: Route handlers → internal tRPC callers → oRPC; reducing layers; debating single API folder.
- **Sidebar / UI refinements**: Collapsible sidebar for small screens, accordion-like sidebar groups, command palette (cmd+k), hover/active state colors.
- **Custom skills / agent tooling**: Maintains `.agents/skills/` and `.claude/skills/` directories; prunes unused ones aggressively.
- **Clerk + GitHub org integration**: OAuth token inspection, GitHub org migration for team members.

**Key paths referenced**:
- `apps/app/src/components/app-sidebar.tsx`
- `apps/platform/src/instrumentation.ts`
- `vendor/observability/src/trpc.ts`, `inngest.ts`
- `packages/app-trpc/src/react.tsx`, `packages/platform-trpc/src/react.tsx`
- `thoughts/shared/plans/`, `thoughts/shared/research/` (plan/research store)
- `.agents/skills/`, `.claude/skills/` (agent skill store)

---

## lightfastai/climode (16.9% of sessions)

**What it is**: An autonomous AI coding agent — the "Ralph" loop. A state-machine-based planning and build agent that operates on `IMPLEMENTATION_PLAN.md` and `thoughts/shared/specs/`. Built on top of Claude Code skills.

**Tech stack**: TypeScript, Claude Code skill framework, npm packages (inferred: two packages published together).

**Recurring themes**:
- **Ralph loop**: Autonomous plan-loop (State A/B/C) and build-loop that implement one phase per invocation and exit.
- **Package publishing**: Discussing and executing npm publish for two packages.
- **Deep rename**: `codemode` → `climode` rename across the codebase.
- **Git authorship**: All commits were initially signed as Claude; user rewrote history to restore personal authorship.

---

## jeevanpillay/dual (1.3% of sessions)

**What it is**: Personal repo, minimal activity. Only observed prompt is `/implement_plan @thoughts/shared/plans/2026-02-15-v2-to-v3-roadmap.md` — suggests a v2→v3 migration of something personal.

**Tech stack**: Unknown.

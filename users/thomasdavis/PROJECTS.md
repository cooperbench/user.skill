# PROJECTS — thomasdavis

## tpmjs/tpmjs ★ DOMINANT (100% of sessions)

**What it is:** TPMJS is an AI tool registry and composition platform. Users can:
- Browse and install npm-published AI tools (packages following the AI SDK v6 `tool()` + `jsonSchema()` pattern)
- Compose tools into **Collections** (grouped tool sets with shared executor config and env vars)
- Create **Agents** (LLM-backed chat agents that use collections or individual tools)
- Run tools in an **Agent Sandbox** (stateful Deno server with persistent filesystem per conversation)
- Connect remote **Custom MCP Servers** (SSE/HTTP, aggregated into collection's tool set)
- Use local tools via a **Bridge CLI** (local MCP servers)
- Build **Workflows** (visual React Flow canvas, multi-step tool pipelines)
- Store persistent AI memory via a **Memory Service** (embedding-based, semantic search)

**Tech stack:**
- Monorepo: `pnpm` workspaces + Turborepo
- Web app: `apps/web` — Next.js 15 App Router, TypeScript, Prisma/PostgreSQL
- UI library: `packages/ui` — internal component library with Icon system
- DB package: `packages/db` — Prisma schema + generated client
- Types package: `packages/types` — Zod schemas shared across web + tools
- Tool packages: `packages/tools/official/` — individual npm packages per tool set
- Sandbox: `templates/agent-sandbox/` — Deno HTTP server deployed to Railway
- Railway executor: `apps/railway-executor/` — custom tool executor pattern
- Linting: Biome
- Testing: Vitest (unit + integration)

**Recurring themes thomasdavis builds:**
1. **Error auto-fix pipeline:** Sentry → webhook → GitHub issue (labeled `auto-fix`) → Claude Code GitHub Action → PR → Discord notification
2. **Execution tracking:** `ExecutionEvent`, `UserActivity`, `ApiUsageRecord` — he keeps expanding coverage
3. **Sandbox infrastructure:** Stateful Deno sessions, shell/file tools auto-injected when `sandboxEnabled = true`
4. **MCP aggregation:** Custom remote MCP servers + bridge tools + registry tools unified into one collection endpoint
5. **Tool publishing:** `blocks.yml` → `pnpm blocks run <tool>` → npm publish → TPMJS sync
6. **Admin/metrics dashboard:** `StatsSnapshot`, search logs, DAU/WAU/MAU, admin pages

**Key file locations he references:**
- `packages/db/prisma/schema.prisma` — the single source of truth for all models
- `apps/web/src/lib/executors/index.ts` — tool execution routing
- `apps/web/src/lib/agents/build-tools.ts` — agent tool injection + env var cascade
- `apps/web/src/lib/mcp/handlers.ts` — MCP protocol handlers
- `apps/web/src/app/api/` — all API routes (Next.js route handlers)
- `vercel.json` — cron schedules
- `CLAUDE.md` — project-level instructions (he asks agent to update it frequently)
- `.claude/skills/tpmjs-tool-creator` — canonical tool creation guide

**Deployment:**
- Production: Vercel (`tpmjs.com`)
- Sandbox: Railway
- CI: GitHub Actions (includes `claude-auto-fix.yml` for autonomous error remediation)

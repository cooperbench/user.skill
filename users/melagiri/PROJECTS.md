# Projects: melagiri

## melagiri/code-insights ★ dominant repo (100% of sessions)

**What it is**: A developer productivity CLI + web dashboard that syncs AI coding session transcripts (from Claude Code, Codex CLI, Cursor, Copilot) into a local SQLite database, then runs LLM analysis to extract learnings, decisions, summaries, and prompt quality scores.

**Published as**: `@code-insights/cli` on npm (versions tracked: 3.0.0 → 3.0.2 → 3.0.3 → 3.1.2 → 3.3.1 → 3.4.0 → 3.5.0 → 3.6.0 during the observed period)

**Monorepo structure** (inferred from file references):
- `cli/` — Node.js CLI, SQLite DB, sync/analysis commands, `cli/package.json`
- `server/` — Hono HTTP server (`server/src/routes/`, `server/src/llm/`)
- `dashboard/` — React+Vite+shadcn dashboard (`dashboard/src/components/`, `dashboard/src/pages/`, `dashboard/src/hooks/`)
- `docs/` — Product docs (`docs/PRODUCT.md`, `docs/VISION.md`, `docs/ROADMAP.md`), transient plans (`docs/plans/`)

**Tech stack**:
- Runtime: Node.js v22, pnpm workspaces
- Server: Hono + `@hono/node-server`
- Database: SQLite via `better-sqlite3`, migration system (`runMigrations`)
- Dashboard: React, Vite, shadcn/ui, React Query, SSE for streaming
- LLM: Gemini API (observed in use), Claude, configurable provider via `createLLMClient()`
- Analytics/telemetry: PostHog (migrated from Supabase)
- CI: GitHub Actions, `pnpm test` gate
- Tests: Vitest, in-memory SQLite

**Recurring themes in sessions**:
- Parser maintenance for multiple AI tool formats (Claude Code JSONL, Codex CLI Responses API, Cursor, Copilot VS Code/CLI)
- Multi-agent team ceremony: `/start-feature`, `/start-review`, custom agent personas
- Release management: version bump → npm publish → gh release
- LLM analysis pipeline: session analysis prompts, insight extraction (summaries, decisions, learnings, techniques, prompt_quality)
- Dashboard UX iterations: Sessions page, Insights page, Export page, Reflect/Patterns page
- Telemetry: PostHog event capture, custom domain CNAME, supabase→posthog migration
- Doc hygiene: deleting transient plan docs, updating PRODUCT/VISION/ROADMAP

**Companion repo** (referenced but not the primary workspace):
- `../code-insights-web/` — Marketing/web site with docs, updated alongside CLI releases

**GitHub issues / PRs observed**: #71, #74, #77, #88, #90, #91, #92, #93, #94, #95, #100, #106, #108, #109, #110 — all in melagiri/code-insights

---
name: cyyeh-projects
description: Repos cyyeh works in, their tech stacks, and recurring themes
---

# Projects

## cyyeh/duckdb-data-agent ★ dominant (46% of sessions, plus 51% as wanshicheng fork)

An AI chat agent that lets users query DuckDB databases via natural language. The agent uses the Claude Agent SDK to orchestrate SQL generation and chart generation as subagents or tools, then streams results (thinking blocks, SQL queries, charts, answer text) to a React frontend.

**Tech stack:**
- Backend: Python, FastAPI, uvicorn, DuckDB, Claude Agent SDK, langfuse, bifrost (LLM gateway)
- Frontend: React, TypeScript, Vite, Plotly / vega-lite charts, i18n (English + Traditional Chinese)
- Infra: Docker, docker-compose, sidecar containers (containerized Claude Code runtime), Render (deployment)
- LLM routing: bifrost gateway supporting multiple providers (Anthropic, OpenAI-compatible)

**Recurring themes and work:**
- Streaming conversation UI bugs (switching between conversation history tabs breaks in-progress responses)
- Sidecar container lifecycle management (spawning, stopping, skill visibility inside containers)
- Chart rendering: interleaving charts with text in answers, preventing empty-data charts, multiple chart support
- Multi-provider LLM support via bifrost and model rewrite rules (`MODEL_REWRITES`, `FALLBACK_MODEL`, `@haiku/@opus/@sonnet` suffix routing)
- Subagent architecture: sql-analyst and chart-builder subagents, preventing double-sending of data
- File upload feature (CSV, JSON, Parquet, Excel)
- i18n (English / Traditional Chinese) with localStorage preference
- Claude Code skills integration in UI (skill autocomplete, skill enable/disable, sidebar skill list)
- OpenSandbox / agent-sandbox integration for secure container execution
- Langfuse SDK integration for observability
- README maintenance after each major feature

**Notable design decisions:**
- Sidecar container spawned per-session by backend's ContainerManager via Docker SDK (not a static service in docker-compose)
- Uses `print()` instead of `logging.basicConfig()` — explicit project-level rule
- Chart-text interleaving is a hard constraint in system prompt (fights model non-compliance especially with non-Anthropic models)

---

## wanshicheng/duckdb-data-agent (51% of sessions)

The same project as cyyeh/duckdb-data-agent — this is a collaborator fork or the upstream repo. cyyeh works across both, likely pushing feature branches and PRs between them. Same codebase, same stack.

---

## cyyeh/duckdb-web (3% of sessions)

A lighter DuckDB browser IDE — displays query results as interactive tables or markdown. Added charting (Recharts), collapsible thinking blocks, and column type detection for chart auto-configuration.

**Tech stack:**
- React, TypeScript, Vite, Recharts
- DuckDB WASM (browser-side SQL execution, inferred)

**Recurring themes:**
- Collapsible thinking block UI
- Chart configuration panel (bar/line/scatter/pie via Recharts)
- Column profiling for automatic chart axis suggestions

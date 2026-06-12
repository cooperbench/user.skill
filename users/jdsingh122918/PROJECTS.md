# Projects: jdsingh122918

## Dominant Repo: `jdsingh122918/forge` (100% of sessions)

### What It Is

Forge is a Rust CLI tool that orchestrates AI-powered software development. It takes a project spec (`.forge/spec.md`), breaks it into phases, and runs Claude (or a council of models) iteratively against each phase until the phase's promise tag (`<promise>DONE</promise>`) is emitted. It has two major subsystems:

1. **CLI orchestrator** (`src/cmd/run.rs`, `src/orchestrator/`) — sequential or DAG-based phase execution
2. **Factory UI** (`src/factory/`) — a Kanban-style web app where issues are created, pipelines are triggered, and agent output is watched via WebSocket

### Tech Stack

| Layer | Technologies |
|-------|-------------|
| Language | Rust (Edition 2024) + TypeScript |
| Async runtime | tokio |
| Web framework | axum 0.8 |
| CLI parsing | clap (derive macros) |
| Error handling | anyhow + thiserror v2 |
| Serialization | serde + serde_json |
| Database | libsql (async) with Turso cloud sync option |
| Git integration | git2 v0.20 |
| Graph/DAG | petgraph |
| Tracing | tracing + tracing-subscriber |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4 |
| Frontend testing | Vitest + RTL + MSW |
| CI | GitHub Actions, Clippy -D warnings, cargo-audit |
| Docker | bollard 0.20 (container sandbox) |

### Key Modules (as of the session window)

| Path | Purpose |
|------|---------|
| `src/main.rs` | CLI entry point, command dispatch |
| `src/cmd/run.rs` | `forge run` — sequential phase execution loop |
| `src/orchestrator/runner.rs` | ClaudeRunner, council integration, iteration logic |
| `src/dag/` | Parallel phase scheduling (DAG executor) |
| `src/council/` | Multi-model council engine (llm-council style) |
| `src/factory/` | Kanban backend: API, WebSocket, pipeline, DB |
| `src/factory/db/` | Modular async DB layer (post-libsql migration) |
| `src/factory/pipeline/` | Docker sandbox execution, stream parsing |
| `src/review/` | Specialist review system (Security, Performance, Architecture, Simplicity) |
| `src/cmd/autoresearch/` | Autoresearch loop: mutates prompts, benchmarks specialists |
| `ui/src/` | React frontend for Factory |

### Recurring Work Themes

**Council integration**: Wiring the existing but dormant multi-model council (Claude + Codex) into the sequential run loop. Required per-phase opt-in/out, guardrails for misconfigured council, and prompt context plumbing.

**Autoresearch loop**: A self-improvement system that mutates specialist prompts, runs benchmarks, scores output (recall/precision/actionability via FindingMatcher + Scorer), and keeps/discards mutations via git. Tasks T01–T14 were implemented across the session window.

**Factory UI improvements**: Migrating from Kanban to an "autonomous coding agent" UI. Pretty output tab (parsed JSON vs raw), phases backfill, file change tracking, CLI autocomplete.

**Dependency upgrades**: Rust nightly → stable, axum 0.7 → 0.8, bollard 0.18 → 0.20, thiserror 1 → 2, rusqlite → libsql, ESLint 9 → 10.

**Database migration**: rusqlite (sync, Arc<Mutex>) → libsql (native async) with Turso cloud replication.

**Observability**: telemetry module, tracing spans (with `.instrument()` rather than `.entered()` across await points), metrics DB (`MetricsCollector`).

**Code quality**: Periodic "rate the codebase" sessions producing scored assessments on typing, traversability, test coverage, feedback loops, self-documentation.

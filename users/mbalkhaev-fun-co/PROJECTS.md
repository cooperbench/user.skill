# Projects: mbalkhaev-fun-co

## balkhaev/yep ★ (dominant — 100% of sessions)

**What it is**: A developer code-intelligence/analytics tool. Analyzes a codebase and surfaces code quality metrics, risk analysis, trends, patterns, co-change graphs, symbol-level stats, and recommendations. Runs as a CLI (`yep`) with two UIs: a web GUI (React SPA) and a TUI.

**Stack**:
- Monorepo managed with Turbo
- Runtime: Bun
- GUI: React + TypeScript + Vite, deployed to `apps/tui/gui-dist`
- TUI: separate package (`tui`)
- API server: serves on `http://localhost:3838`, all endpoints under `/api/` prefix
- Database: SQLite-adjacent with schema including `code_symbols`, `metadata` fields
- Embeddings: vector embeddings for code indexing (286 files observed)
- PageRank: used for symbol importance scoring
- Git metadata extraction: `gitChangeCount`, `gitAuthorCount`, `gitLastChangeDate`

**CLI commands observed**:
- `bun run build` — builds all packages via turbo
- `yep gui` — serves the web GUI on port 3838
- `yep api` — runs only the API server
- `bun run build && yep gui` — the user's canonical deploy cycle

**Recurring themes in sessions**:
- API routing bugs: endpoints returning HTML instead of JSON (SPA catch-all misconfiguration)
- Code index failures: schema mismatches (`Found field not in schema: metadata`)
- Navigation/routing in the GUI: timeline ↔ code linkage, path handling (full vs. relative)
- Risk analysis endpoint: `/api/risk-analysis?limit=20`
- TypeScript compile errors in `src/components/charts/theme.ts` (JSX in `.ts` file)
- TUI-specific errors separate from desktop errors
- Generating recommendations on click with token cost disclosure

**User's relationship to it**: builder and sole user. Runs it against their own codebase. Treats each session as a focused bug-fix or feature sprint.

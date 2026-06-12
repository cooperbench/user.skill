# Projects: nicksu@polyv.net

## terryso/polymarket-trader ★ dominant (100% of sessions)

**What it is**: A live + paper trading bot for the Polymarket prediction-market platform. The system monitors markets, generates trade signals via an LLM analyzer, executes buy/sell orders through the Polymarket CLOB API, manages positions, and provides a dashboard UI for monitoring.

**Tech stack**:
- Backend: Python 3.11, FastAPI, loguru, SQLAlchemy + SQLite
- Frontend: React/TypeScript dashboard
- CI: GitHub Actions with `black`, `isort`, `pytest`
- API: Polymarket CLOB API (GTC/FAK/FOK orders, orderbook, positions)
- Config: `.env` file (`TRADING_MODE=paper|live`, `DISABLE_CIRCUIT_BREAKER`, `TRADING_ENABLED_ON_START`)
- Agent orchestration: BMAD framework (`_bmad/` directory, agent personas, workflow YAML + XML)

**Recurring themes from sessions**:
- **Exit strategy bugs**: Positions hit take-profit threshold but don't auto-sell; system uses stale cached prices instead of real-time; agent calculates YES vs. NO take-profit direction incorrectly.
- **Circuit breaker / trading state**: `DISABLE_CIRCUIT_BREAKER=true` in `.env` doesn't override DB-persisted `trading_enabled=false`; state not restored on restart.
- **BMAD pipeline execution**: Running story delivery pipeline (`bmad-story-team-deliver`), test architecture (`bmad-tea-testarch-automate`, `bmad-tea-testarch-ci`), code review, sprint planning via BMAD agents.
- **CI formatting failures**: `black` and `isort` checks repeatedly fail after commits; Nick pastes raw CI output for the agent to fix.
- **Trade history UI**: Mismatch between local dashboard and Polymarket website; refactoring from mixed paper/live display to mode-driven display from `.env`.
- **Orderbook API errors**: `PolyApiException[status_code=400, error_message={'error': 'the orderbook ... does not exist'}]` — resolved markets causing sell failures.
- **Position sync**: Polymarket shows 4 positions, local system shows 1 — sync gap between API and local DB.

**File paths referenced**:
- `_bmad/core/tasks/workflow.xml` — BMAD core OS
- `_bmad/bmm/workflows/4-implementation/*/workflow.yaml` — story/dev/code-review/sprint-planning workflows
- `_bmad/tea/workflows/testarch/*/workflow.yaml` — test architecture workflows
- `_bmad-output/implementation-artifacts/` — generated story files
- `src/trading/live_trading.py`, `src/trading/exit_checker.py`, `src/trading/risk_control.py`
- `src/core/state.py`, `src/core/recovery.py`
- `src/storage/database.py`

**Date range**: 2026-02-26 to 2026-02-28 (2-day sprint)

---
name: jukellam-projects
description: Repos and what jukellam does in each, with tech stack and recurring themes.
---

# Projects

## [DOMINANT] jukellam/dispersal-draft

A multi-tenant fantasy football auction draft platform. jukellam is the sole developer and commissioner. All 15 sessions are in this repo.

### What he does here

Everything. He designed the architecture, drove a full single-to-multi-tenant migration (Phases A–H), and added a startup dynasty draft type with a complete trading system. He reviews agent PRs, tests the running app manually on Mac and Windows, and manages deployments on Render.

### Tech stack

- **Backend**: Python, FastAPI, SQLite (WAL mode), Pydantic v2
- **Auth**: Token-based (super admin → commissioner → manager hierarchy)
- **Email**: Resend SDK (`resend` package), `RESEND_API_KEY` env var
- **Frontend**: Jinja2 server-rendered HTML, WebSockets for real-time updates
- **Testing**: pytest with fixtures in conftest.py (~215 tests as of Feb 2026)
- **Deployment**: Render, `render.yaml`
- **CI workflow**: compound-engineering plugin with `/workflows:plan`, `/workflows:work`, `/workflows:review`, `/workflows:compound`, `/workflows:brainstorm`
- **Context tracking**: Entire

### App structure

```
app/
  main.py          — FastAPI app, background auction-expiry task, WebSocket endpoint
  state_db.py      — DraftStateDB class (all business logic, ~1100+ lines)
  models.py        — Pure dataclasses (Player, Auction, Manager, Trade, …)
  database.py      — SQLite connection, transaction() context manager
  auth.py          — Token validation, Depends() helpers
  email.py         — Resend integration, _log_email(), 7 email functions
  websocket.py     — ConnectionManager for multi-tenant WebSocket broadcasts
  routers/
    admin.py       — Commissioner admin panel (~865 lines)
    draft.py       — Manager draft UI
    manager.py     — Manager registration
    requests.py    — Draft request/approval flow (transactional emails here)
    archive.py     — Read-only archive of completed drafts
    trade.py       — Trading system (added in Feb 2026)
  migrations/
    001–009*.sql   — Incremental schema migrations
  templates/       — Jinja2 HTML templates
docs/
  plans/           — Dated implementation plans (2026-MM-DD-feat-*.md)
  solutions/       — Post-implementation knowledge docs
  brainstorms/     — Pre-planning exploration docs
```

### Key milestones completed (as of sessions)

| Phase | What |
|-------|------|
| A | Multi-tenant migration: SQLite, token auth, gated draft creation |
| B | Request/approval flow (super admin panel, commissioner creation form) |
| C–F | Draft lifecycle, player management, bidding, email stubs |
| G | Super admin features (all-drafts view, filtering) |
| H | Archive router, deployment (Render) |
| Post-H | Email delivery via Resend (fixed), email logging (migration 009) |
| PR #1 | Trading system backend: TradingService, 48 tests |
| PR #2 | Trading system frontend + 21 code review fixes |
| PR #3 | Startup dynasty draft UI (reviewed via `/workflows:review PR#3`) |

### Recurring themes

- **Startup dynasty draft type**: Extends existing dispersal-draft with rookie picks, commissioner/direct trades, secondary sale auctions. Jukellam had to correct the agent when it built trading without the startup draft UI.
- **CLAUDE.md discipline**: Always updated after each phase, contains architecture notes, migration progress table, email config, compound-engineering workflow memory.
- **SQLite transaction safety**: `immediate_transaction()` pattern added to prevent TOCTOU races on financial operations.
- **Email reliability**: Resend integration, email logging table (`email_log`), token fallback via super-admin panel and terminal.
- **Future plan**: Dynasty fantasy football analysis app (separate webapp) to be integrated on same Render instance as a different subdomain. Plan is in `DYNASTY_INTEGRATION_PLAN.md`.

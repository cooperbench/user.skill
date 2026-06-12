# PROJECTS — araitatsuya-code

## araitatsuya-code/atena-print ★ dominant (100% of sessions)

**What it is:** A Wails desktop application for printing Japanese postal address labels (宛名印刷). "Atena" (宛名) means addressee/recipient in Japanese — the app manages an address book (住所録) and generates printable label layouts for envelopes and postcards.

**Tech stack:**
- **Desktop framework:** Wails (Go + React bridged as a native desktop app)
- **Backend:** Go with Clean Architecture (entity → usecase → infrastructure layers)
- **Database:** SQLite via `go-sqlite3` + `golang-migrate`
- **Frontend:** React + TypeScript, Zustand for state, Vitest + React Testing Library
- **Build/CI:** GitHub Actions (implied), GitHub Issues with phase labels

**Architecture enforced by user:**
- `entity ← usecase ← infrastructure` dependency direction — violations caught immediately
- Repository interfaces in `internal/repository/`, implementations in `internal/infrastructure/sqlite/`
- DI wired in `main.go`
- Frontend state via Zustand with selector-based subscriptions (not whole-store subscriptions)

**Phase structure (from prompts):**
- Phase 1: 基盤構築 (foundation) — Wails init, Go entities, DB schema, repositories, frontend scaffold
- Phase 2: 住所録 CRUD (address book CRUD)
- Further phases implied by the label system (`phase-3`, `phase-4`, etc.)

**Recurring themes across sessions:**
- Implementing the next GitHub issue in the current phase
- Writing Go table-driven tests and React Vitest tests after implementation
- Responding to PR inline review comments (fetching via `gh api`, replying, fixing)
- Updating issue status and docs after merging
- Enforcing Clean Architecture on each PR

**Key files referenced in prompts:**
- `docs/04-TASK-LIST.md` — master task list by phase
- `docs/` — spec documents referenced during implementation
- `frontend/src/App.tsx` — main React entry point
- `frontend/src/components/address/ContactEditModal.tsx`
- `frontend/src/lib/verticalText.ts` — vertical Japanese text rendering engine
- `internal/entity/`, `internal/repository/`, `internal/infrastructure/sqlite/`
- `.claude/settings.json` — Claude Code project settings

**Notable technical details:**
- Vertical Japanese text rendering (`縦書き`) for address labels: handles 拗音/促音, 長音符 rotation, 句読点 positioning, kanji numeral conversion for addresses
- Surrogate pair handling for Unicode characters in canvas drawing
- mm-to-px conversion for label templates (96 dpi)

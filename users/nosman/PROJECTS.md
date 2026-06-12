# nosman — Projects

## nosman/gossamer ★ (only repo, 100% of sessions)

**gossamer** is a developer observability tool for Claude Code. It captures Claude Code hook
events, indexes checkpoints from the Entire CLI, and presents them in a rich desktop UI.

### What nosman does here

- Builds and evolves the full stack: SQLite schema, Express/WebSocket server, Electron + Mantine UI
- Migrates data storage layer as requirements grow (flat files → SQLite → Prisma → Entire CLI checkpoints)
- Creates new UI screens for sessions, checkpoints, search, open items, pinned entities, session trees
- Debugs live data pipeline issues (polling loop, git OID mapping, WebSocket updates)
- Iterates UI appearance heavily: dark mode, typography, layout, markdown rendering

### Tech stack

| Layer | Technology |
|---|---|
| Desktop shell | Electron |
| UI components | Mantine |
| Frontend framework | React + TypeScript (`.tsx`) |
| Backend server | Express + WebSocket (`ws`) |
| ORM | Prisma |
| Database | SQLite (via better-sqlite3 driver adapter) |
| Full-text search | SQLite FTS5 |
| Checkpoint source | Entire CLI (`entire/checkpoints/v1` branch) |
| Build/types | TypeScript (NodeNext modules) |
| Diff display | diff2html |
| Git integration | gitlog npm library |

### Recurring themes

- **Schema evolution**: repeatedly extends the SQLite schema to capture new checkpoint fields;
  frequent migrations from old to new table names mid-session
- **UI iteration**: most sessions include at least one round of visual correction; dark mode
  compatibility is a persistent issue
- **Session/checkpoint linking**: linking parent→child sessions, checkpoint→git OID mappings,
  open items→sub-sessions — relational integrity is a recurring concern
- **Indexing pipeline**: polling loop to pick up new Entire CLI checkpoints, worktree management,
  git remote handling
- **Open items lifecycle**: surfaces open items from checkpoint metadata, lets user mark status,
  spawn sub-sessions for selected items
- **Search**: FTS5 search across log content with result highlighting and scroll-to-match behavior

### Date range

March 1–26, 2026 (25 days, 29 sessions)

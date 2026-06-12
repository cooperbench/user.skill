# Projects

## savekirk/session-bridge ★ dominant repo (100% of sessions)

**What it is**: A VS Code extension that surfaces AI-coding sessions — recorded by a separate CLI tool called "entire" — inside the VS Code UI. Sessions are stored as git commits on a dedicated checkpoint branch (`entire/checkpoints/v1`). The extension reads them and displays checkpoints, sessions, and conversation transcripts in tree views and a webview panel.

**Tech stack**:
- TypeScript, VS Code Extension API
- git as the storage backend (no database — all reads via `git show`, `git ls-tree`)
- jsonl transcript files (one line per conversation turn)
- Node.js child process spawning (`runCommandAsync`) for git calls
- Webpack or tsc for build (`out/` output directory)

**Key modules** (referenced repeatedly in prompts):
- `src/checkpoints/` — core data layer: `orchestration.ts`, `transcript.ts`, `models.ts`, `store.ts`, `types.ts`, `util.ts`
- `src/components/` — VS Code UI layer: `sessionsTreeView.ts`, `sessionDetailsPanel.ts`, `checkpointTreeView.ts`, `activeSessionTreeView.ts`
- `src/extension.ts` — entry point, wires providers and commands
- `src/workspaceProbe.ts` — detects workspace state (`EntireStatusState`: ENABLED / CLI_MISSING / NOT_GIT_REPO / DISABLED)
- `package.json` — VS Code manifest: commands, tree views, `viewsWelcome` entries

**Recurring themes**:
- Checkpoint selection → session list reload race conditions and crashes
- Session details webview: conversation rendering (user turns, agent text, tool calls, thinking) with avatar/icon design
- Active sessions (live) vs. historical sessions (from checkpoints) — kept in separate tree views
- Data attribution: session metadata must come from the git commit, not the current user's git config
- `viewsWelcome` in `package.json` preferred over custom empty-state components in TypeScript
- Timestamp formatting: time-only for same-day, day+time for multi-day, full date for headers

**Path on developer's machine**: `/Users/savekirk/dev/ai/entire/session-bridge`

# Projects

## itsmaleen/dispatch ★ dominant (54.5% of sessions)

An AI agent command center — an Electron macOS app that hosts Claude Code sessions, displays agent consoles, manages workspaces (folders), and persists console line history in SQLite. The user treats this as the primary product.

**Tech stack:**
- Electron (main + preload + renderer)
- React + TypeScript + Tailwind
- Bun runtime
- SQLite with FTS5 (console line persistence)
- electron-builder for macOS packaging and code signing
- GitHub Actions for CI (build, sign, notarize macOS app)
- PostHog analytics (recently added via @dispatch/analytics package)
- @tanstack/react-virtual for virtualized console output

**Recurring themes in sessions:**
- macOS code signing / notarization failures in GitHub Actions (persistent multi-session debug loop)
- Console output rendering: virtual scrolling, scroll-to-bottom behavior, line limits, FTS5 search
- Multi-phase persistence features with plan files (`.plans/console-line-persistence.md`)
- UI layout: Electron title bar vs. macOS traffic lights overlap, ChatInput icon alignment
- Server bundle packaging: `prepare-server-bundle.mjs` workspace dependency handling
- Multi-window support (WindowManager class, IPC handlers)

**Observed file/path references:**
- `packages/ui/src/components/workspace/Workspace.tsx`
- `packages/server/src/server.ts`
- `prepare-server-bundle.mjs`
- `~/.acc/threads.db` (production SQLite path)
- `.plans/console-line-persistence.md`

---

## itsmaleen/merry (45.5% of sessions)

A companion Electron app (possibly a Claude Code / terminal-adjacent tool — name chosen by the user during a session as a "non-obvious but obvious and cool" rebrand). Overlaps in tech stack with Dispatch.

**Tech stack:**
- Electron
- React + TypeScript + Tailwind
- electron-builder (same macOS signing problems as Dispatch)
- GitHub Actions CI

**Recurring themes in sessions:**
- Same macOS code signing workflow failures (sessions appear to be debugging the same CI infrastructure across both repos)
- Multi-window support feature (prompted with "how can we update this electron app to allow for multiple windows")
- Branding/naming decisions (title bar layout, app icon, name)
- Config system

**Note:** Session content for Merry is less detailed in the digest; many prompts overlap with Dispatch's CI debugging.

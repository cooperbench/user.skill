# Projects

## upamune/xi ★ (dominant — 100% of sessions)

**What it is**: `zi`, a terminal coding-agent CLI. The user is building it from scratch as an infrastructure project: a Bun-compiled binary that wraps an LLM with FS isolation and multi-provider AI support.

**Tech stack**:
- TypeScript, Bun runtime, `bun build --compile` for single-binary distribution
- Vercel AI SDK (`streamText`, tool definitions via Zod)
- `agentfs-sdk` for SQLite-backed agent filesystem (delta layer)
- `just-bash` for bash tool execution inside the agent
- `BunSqliteAdapter` bridging Bun's SQLite to the agentfs interface
- TUI (terminal UI) with keyboard-driven interaction (Ctrl-D exit, Ctrl-C abort)
- GitHub Actions CI (`release.yml`) with `bun run typecheck` gating

**Recurring themes in sessions**:
1. **FS isolation architecture**: Building a Copy-on-Write overlay (Delta layer = AgentFS SQLite, Base layer = real CWD) so the agent sees a consistent view of the filesystem. Major work: `src/fs/overlay-agentfs.ts`, `src/fs/bash-fs-adapter.ts`.
2. **Tool wiring**: Getting `read/write/edit/bash` tool definitions passed correctly into `streamText()` so the LLM can actually call them.
3. **Shutdown UX**: Making `apply` commands visible at session end so the user can push agent changes to the real filesystem.
4. **API key handling**: Early validation with clear errors, retry exclusion for config errors.
5. **Multi-provider support**: Anthropic, OpenAI, Kimi all wired through a single `provider.ts` abstraction.
6. **TUI exit handling**: Ctrl-D graceful shutdown with session diff display.

**Architectural state (from sessions)**:
- Sessions map closely to individual features/bugfixes, each ending with a PR
- PRs observed: `#2` (tool definitions), `#7` (bash FS overlay unification)
- User self-hosts the agent (`~/dist/zi`) and tests it live, discovering bugs by using the tool

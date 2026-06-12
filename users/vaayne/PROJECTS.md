# Projects — vaayne

## vaayne/anna ★ dominant repo (85.7% of sessions)

**What it is**: A full AI assistant framework — "not a go cli, it is a full ai assistant like openclaw, support different channels, having scheduler auto, activate personinal assistant… also having LCM memory system that can keep long chat not loss any context."

**Tech stack**: Go, Atlas (DB migrations), SQLite (migrations reference), CLI via cobra/similar, GitHub Actions (CI with coverage gates), `gh` CLI for releases

**Recurring themes**:
- Restructuring packages: moving things to `internal/`, merging packages that overlap (heartbeat → cron)
- Database migration: replacing hardcoded Go migrations with Atlas-generated SQL migrations
- Plugin system: dual Go (Caddy-style blank import + local `.go` file) and JS (QuickJS/Wazero) plugins with a shared management CLI (`anna plugin add/remove/list/build`)
- Agent extensibility: studying how Pi's extension system works to make anna similarly extensionable
- README and marketing: crafting a full marketing README ("use humenize to improve like a humen write for humen")
- Releases: `new patch release`, `create new release` via `gh`
- CI coverage: reacts to coverage failures by asking for more unit tests

**Key files vaayne references**:
- `@memory/database.go`, `@db/` — memory/DB layer
- `@internal/skills/tool.go` — skill tool dependency concerns
- `handoff.md` — cross-session continuity doc ("read handoff.md and continue")

## vaayne/agent-kit (14.3% of sessions)

**What it is**: A skill-based configuration kit for multiple AI agents (Claude, Pi, Codex, Factory, Amp, Droid), syncing shared skills and agent prompts across different agent directories via `mise.toml` tasks and rsync.

**Tech stack**: `mise.toml` (task runner), rsync, shell, TypeScript extensions (Pi-specific), Markdown skill files

**Recurring themes**:
- Migrating from per-agent sync tasks to a unified skill-based sync
- Managing the `pi-delegate` skill: turning it into a full subagent system with preset agents (oracle, reviewer, worker, ui-engineer, librarian) stored under `skills/pi-delegate/agents/`
- Syncing `~/.agents/skills/` to `~/.claude/skills/` via symlink or rsync
- Removing redundant top-level `agents/` folder once `pi-delegate` handles it
- Improving model selection guidance: dynamic `pi --list-models [search]` instead of hardcoded model names

**Key files vaayne references**:
- `@mise.toml` — task definitions
- `@skills/pi-delegate/` — the delegation skill
- `_AGENTS.md` — shared agent instructions synced to all targets as `AGENTS.md`/`CLAUDE.md`

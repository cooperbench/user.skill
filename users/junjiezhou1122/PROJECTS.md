# Projects: junjiezhou1122

## junjiezhou1122/ClawCorp ★ DOMINANT (100% of sessions)

**What it is**: An AI agent "corporate OS" — a local command center where the user (the "Chairman") manages a hierarchy of AI agents organized like a company. Agents have titles, departments, system prompts, and org-chart relationships. They delegate to each other, send messages, file reports, and work on missions autonomously.

**Core concepts the user cares about**:
- **Hierarchy**: Chairman → executives (CTO, PM, research lead) → team leads → workers. Strict org chart; lower agents cannot contact higher-level agents directly.
- **Missions**: discrete tasks with state (`backlog → todo → in_progress → review → done`), assigned to agents, tracked on a Kanban board
- **Live Log**: WebSocket-streamed real-time stdout from running agent processes
- **MCP tooling**: agents get `escalate`, `delegate`, `report`, `send_message` tools via a ClawCorp MCP server injected at runtime
- **Smart Hire**: natural-language → auto-generate 3 candidates → parallel test → LLM-scored → best candidate auto-hired (Spec 003)
- **Spec-driven development**: specs live in `.specify/specs/`, numbered 001–006+

**Tech stack**:
- Backend: Bun + Hono (port 3001), TypeScript
- Frontend: React + Vite + Tailwind (port 5173)
- Agent runtime: `claude --dangerously-skip-permissions -p "..."` as subprocesses
- Communication: WebSocket hub for live log; JSONL files for message channels
- Storage: flat-file directories (`agents/`, `missions/`, `tasks/`, `channels/`)
- LLM: Anthropic API via `@anthropic-ai/sdk` for meta-prompts (candidate gen, scoring)

**Recurring themes / pain points**:
- Duplicate WebSocket events causing doubled UI cards ("又出现了两个")
- Page refresh killing running agent processes
- Agent workspace isolation and session resumption
- Sub-agent delegation not working as expected ("product manager 好像不会把东西delegate给下面的子agent去做")
- Environment variable injection into spawned claude processes (ANTHROPIC_AUTH_TOKEN not reaching subprocesses)
- Task detail overlay: per-task filtered log, mission tree, artifacts, messages

**Key files referenced**:
- `server/src/lib/SmartHire.ts`, `server/src/routes/tasks.ts`, `server/src/routes/channels.ts`
- `client/src/App.tsx` (monolithic React app)
- `agents/<id>/profile.json`, `missions/<id>/state.json`
- `.specify/specs/001-*` through `006-*`
- `.claude/settings.json` (MCP injection point)

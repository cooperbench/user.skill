---
name: marcus-sa-projects
description: Repos and their themes for marcus-sa.
metadata:
  type: project
---

# Projects: marcus-sa

## marcus-sa/brain ★ dominant (49.6% of sessions)

**Brain** — an AI agent orchestration platform described as "an operating system for autonomous organizations."

### What he does here

Builds and ships the entire platform: backend server, CLI, frontend, CI, infrastructure. Works across all layers.

### Tech stack

- TypeScript / Bun runtime
- SurrealDB (graph model, SCHEMAFULL)
- Vercel AI SDK + Claude Agent SDK
- React + shadcn/ui + Tailwind
- GitHub Actions (ubicloud runners)
- Pulumi (infra)
- MCP (Model Context Protocol) server

### Recurring features/domains

| Feature | Description |
|---------|-------------|
| **Observer Agent** | Semantic grounding — verifies agent claims against graph reality, scores behavior, blacklists dishonest agents |
| **Chat Agent** (was: Orchestrator Agent) | Main conversational agent; renamed from orchestrator |
| **PM Agent** | Subagent for work-item suggestion and creation |
| **Coding Agent Orchestrator** | Spawns Claude Code / Agent SDK sessions; originally OpenCode, migrated to Claude Agent SDK |
| **Brain Proxy / LLM Proxy** | Intercepts Anthropic API calls; captures telemetry (tool calls, reasoning, cost) |
| **MCP Tool Registry** | UI and backend for browsing/managing MCP servers |
| **Learning Library** | Per-agent learnings that can be browsed, edited, deleted by users |
| **IAM / OAuth / DPoP / RAR** | Auth system with Rich Authorization Requests, DPoP token binding, no API keys |
| **Policy CRUD UI** | UI for editing Regorus-evaluated policies |
| **Knowledge Graph** | SurrealDB graph: workspace, project, feature, task, observation, decision, member_of, has_project, etc. |
| **Intent / Evidence system** | Agents post structured intents with evidence pointers into the graph |

### nWave workflow

He drives all feature work through a custom 6-wave CLI workflow embedded as slash commands:
`DISCOVER → DISCUSS → DESIGN → DEVOPS → DISTILL → DELIVER`

Relevant commands: `/nw:deliver`, `/nw:design`, `/nw:discuss`, `/nw:finalize`, `/nw:roadmap`, `/nw:distill`, `/nw-bugfix`, `/nw-review`, `/nw-research`

### Workspace naming convention

Conductors workspaces use city names: `richmond`, `dubai-v1`, `lahore-v1`, `montreal`, `houston-v1`, `manila`, etc.

---

## osabiohq/osabio (50.4% of sessions)

**Osabio** — companion product, likely the client-facing or SaaS layer built on top of Brain infrastructure.

### What he does here

Implements feature-level work (agent creation, task assignment UI, policy evaluation, sandbox provider integration). Appears to be where product features land for end-users.

### Tech stack

Shares Brain's stack. Notable additions: Regorus policy evaluation, sandbox providers (E2B, local Docker).

### Recurring themes

- Agent creation and task assignment UI
- Sandbox provider configuration (local vs cloud)
- Policy evaluation (Regorus/OPA rules)
- MCP server integration
- Error handling around `sandbox_provider_not_configured`

### Relationship to brain

osabio consumes Brain as infrastructure. Changes in brain's MCP server, graph schema, or auth system propagate to osabio. He often fixes osabio issues by tracing them back to a brain configuration or env var.

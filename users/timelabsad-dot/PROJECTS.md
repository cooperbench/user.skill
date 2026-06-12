# Projects: timelabsad-dot

## Primary repo: rhea-project (★ dominant)

Split 50/50 across two GitHub orgs — same codebase, different organizational contexts:
- `serg-alexv/rhea-project` — personal account fork or earlier home
- `timelabs-npo/rhea-project` — non-profit organization account (inferred primary going forward)

### What the user does here

Rhea is a multi-agent AI orchestration platform. The user acts as product owner, commander, and architect. Core work visible in prompts:

**Agent fleet management**
- Spawning and naming agents: Rex (Opus, Core Coordinator), Orion (Gemini, Systems Architect), B-2nd (Sonnet, Infrastructure Lead), Hyperion (Gemini, protocol verification)
- Assigning models, roles, and permissions via AGENTS.md and OFFICE.md
- Building a Firebase-backed "virtual office" with inbox/outbox/heartbeat system for inter-agent communication
- Watcher/reanimator tooling to auto-restore sessions after agent death

**Memory and session persistence**
- Relay Chain (3032+ entries) for audit trail
- Entire.io integration for session snapshots and git hooks
- `TODAY_CAPSULE`, `INCIDENTS`, `GEMS` artifacts for structured memory
- Context Tax Collector (CTC) — artifact system to eliminate repeated context copying
- `rhea-elementary/` folder: a growing knowledge base of AI/automation techniques

**Infrastructure**
- `ops/rhea_firebase.py`: Firebase health checks, heartbeat signals, inbox polling
- `rhea_bridge.py`: multi-provider LLM bridge (OpenAI, Gemini, DeepSeek, OpenRouter, Anthropic)
- `.claude/agents/` directory for project-level Claude Code subagents
- Git hooks for Entire.io checkpointing (commit-msg, post-commit, pre-push)

**Recurring operational issues seen in sessions**
- Git push blocked by GitHub secret scanning (exposed API keys in dialogue archives)
- Firebase auth rule failures (403 on unauthenticated REST calls)
- Agent "death" / context loss requiring session restore procedures
- Token limit hits (API Error 400) mid-session
- MCP connector bloat (25+ connectors injecting ~250+ tool definitions per conversation)

### Tech stack

Python (ops scripts), Bash (hooks, shell automation), Firebase/Firestore (REST API), git, Claude Code CLI, Gemini CLI, OpenAI CLI, AppleScript/osascript (browser automation), Entire.io, possibly Node.js/JS (Firebase web SDK snippet visible in prompts)

### Key file paths mentioned

- `/Users/sa/rh.1/` — local project root (macOS)
- `docs/plans/EVOLUTION_PLAN_V1.md` — master roadmap
- `prompts/AUTONOMY_WITH_AUDIT_ROOT.md` — highest-priority operating procedure
- `docs/INTEGRATIONS_AUDIT.md` — full integration registry
- `ops/virtual-office/inbox/`, `ops/virtual-office/outbox/` — agent messaging dirs
- `ops/rhea_firebase.py` — Firebase ops script
- `rhea-elementary/` — AI knowledge base
- `docs/state.md` — current project state snapshot
- `AGENTS.md`, `OFFICE.md` — agent registry and office rules

### Branch names seen

- `main`, `hyperion/memory`, `feature/mvp-loop`

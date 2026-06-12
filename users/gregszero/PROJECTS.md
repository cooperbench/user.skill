---
name: projects
description: gregszero's repos and the work he does in each one
metadata:
  type: project
---

# Projects

## gregszero/open-fang ★ dominant (100% of sessions)

**What it is:** An AI-first canvas/workspace framework built in Ruby. The user calls it "OpenFang". An embedded Claude Code agent named "Ned" lives inside it, accessible via a terminal-chat footer. The user builds OpenFang itself using Claude Code — meta-development where Claude Code runs inside a framework that Claude Code helps build.

**Tech stack:**
- Backend: Ruby, Roda (web framework), ActiveRecord + SQLite, Puma
- Frontend: Stimulus JS controllers, Turbo Streams (Hotwire), ERB templates, Tailwind CSS (CDN), custom CSS design tokens (HSL-based, light/dark mode)
- AI layer: FastMcp gem (MCP tools), Claude Code CLI (streaming JSON events), Anthropic Messages API
- Infrastructure: rufus-scheduler + fugit (cron), ActiveJob (async jobs), SSE for real-time updates, Xvfb + xdotool + scrot (headless computer use)

**Core architecture concepts:**
- **Canvas (AiPage)**: Persistent named pages in the sidebar. Multiple conversations can share one canvas.
- **Canvas components/widgets**: Self-contained widgets placed on the canvas at absolute (x, y) positions. Each widget has its own Ruby class, optional JS, optional refresh job.
- **Conversation**: A chat session linked optionally to an AiPage. Slug-based URLs (`/:canvas_slug/:chat_slug`).
- **MCP Tools**: Ruby classes subclassing `FastMcp::Tool`, auto-discovered via `ObjectSpace`. 38 tools as of the recording period.
- **Skills**: Ruby classes subclassing `Ai::Skill`, auto-discovered, invokable by the AI agent or scheduler.
- **Jobs**: ActiveJob classes in `ai/jobs/`, auto-discovered.
- **Scheduler**: rufus-scheduler polling for due tasks every 60s, heartbeats every 30s, widget refresh every 5m.
- **Event bus**: `Ai::EventBus.emit(event_name, data)` triggers matching `Ai::Trigger` records.

**Recurring work themes (by intent share):**
1. **Debugging** (22.6%): Turbo Stream not updating in real-time, canvas scroll/drag bugs, agent job errors, SSE subscription issues, authentication errors, missing column errors after migrations.
2. **Feature creation** (20.1%): Computer use agent, notification system, heartbeat monitors, workflow pipelines, Gmail integration, daily briefing skill, canvas-linked notifications, streaming agent responses.
3. **Git** (18.3%): Short commits after each working milestone. "commit", "commit this".
4. **Refactoring** (11%): Design system migration (brutalist → shadcn/ui → terminal green), canvas scroll lock behavior, canvas-first architecture overhaul.
5. **Understanding** (10.4%): Exploring patterns before implementing, asking Ned what it can do, investigating why something failed.

**Key files by recurring appearance:**
- `web/app.rb` — Roda routes
- `web/public/js/controllers/canvas_controller.js` — canvas pan/zoom/drag
- `web/public/js/controllers/chat_footer_controller.js` — two-level tab bar, SSE, canvas/conversation switching
- `web/public/css/style.css` — full design system
- `ai/jobs/agent_executor_job.rb` — runs the Claude Code subprocess for each message
- `workspace/CLAUDE.md` — inner agent system prompt ("Ned's" instructions)
- `workspace/guides/` — modular prompt guides served as MCP resources

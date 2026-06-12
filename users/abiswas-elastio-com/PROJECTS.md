# Projects

## anchoo2kewl/SprintSpark → anchoo2kewl/taskai (DOMINANT — 100% of sessions)

**Status:** Renamed from SprintSpark to TaskAI mid-session-history. Production domain: `taskai.cc`. Staging: `staging.taskai.cc`. The repo rename to `anchoo2kewl/taskai` was part of a full rebrand session.

**What it is:** A full-stack task management SaaS with Kanban board, wiki, MCP server, team management, Cloudinary file storage, email invites, and admin dashboard. Deliberately dogfooded — development tasks are tracked inside the app itself at `https://taskai.cc/app/projects/1`.

**Tech stack:**
- **Backend:** Go, chi router, SQLite → Postgres migration, Zap logging, JWT + API key auth, migrations in `api/internal/db/migrations/`
- **Frontend:** React, TypeScript, Tailwind CSS, Vite, Vitest, React Router, `api.ts` singleton `ApiClient`
- **Infrastructure:** Docker Compose, Nginx, Certbot SSL, Ansible provisioning, Travis CI, webhook-based staging deploys
- **MCP Server:** Deployed at `mcp.taskai.cc`, used for task management from Claude Code
- **Code quality:** SonarQube at `sonar.taskai.cc`, golangci-lint, gosec, Biome
- **Real-time:** Yjs + WebSocket + Node.js microservice (wiki collaborative editing)
- **External services:** Cloudflare DNS, Cloudinary media storage, Brevo email, Google Drive backups

**Recurring themes:**
- Test coverage battles (target 80%, often starting at 7–15%)
- Staging/prod deploy pipeline maintenance (Travis CI, webhook servers, `./script/server` commands)
- Feature-then-task-close cycle (implement → deploy → comment task → close in TaskAI)
- MCP server token minimization ("returning too many tokens that drones and overwhelm the llm")
- Security hygiene (exposed API keys, session tokens, admin-only endpoints)
- Swim lane ↔ status data model integrity

**Server topology (inferred from sessions):**
- Production: `31.97.102.48` (amd64) → `taskai.cc`
- Staging: `129.213.82.37` (arm64) → `staging.taskai.cc`
- SonarQube: prod server, port `9000`, behind Nginx at `sonar.taskai.cc`

**Key files referenced repeatedly:**
- `api/internal/api/cloudinary_handlers.go` (line 505, asset management)
- `api/internal/api/testing.go` (`TestServer` pattern)
- `web/src/lib/api.ts` (`ApiClient`, 60+ methods)
- `web/src/lib/api.hooks.ts` (React hooks)
- `./script/server` (deploy/promote/health commands)
- `deployment/` (Ansible playbooks, Nginx configs, Docker Compose)

## Other repos mentioned (context only)

- `~/play/folioworth.com/` — reference implementation for CI/CD pipeline; user asks agent to mirror this pattern for TaskAI
- `~/play/blog` and `~/play/elephanto` — also use `go-backup` for Google Drive backups; referenced when debugging backup regressions

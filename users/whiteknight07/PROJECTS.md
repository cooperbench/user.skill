# Projects — Whiteknight07

## Whiteknight07/AiTutor ★ (sole repo, 100% of sessions)

**What it is**: A full-stack AI tutoring web application built as a solo UBC honors/capstone project. Deployed at `aitutor.ok.ubc.ca` (accessible via UBC VPN only) on a shared university server (`s216.ok.ubc.ca`, RHEL/CentOS).

**Tech stack**:
- Frontend: React, React Router, Tailwind CSS (v4), shadcn/ui components
- Backend: Express, Better Auth, Prisma
- Database: PostgreSQL 16 (Dockerized, port 54321)
- Runtime: Bun (not Node/npm)
- Process manager: PM2 with `ecosystem.config.cjs`
- Reverse proxy: Apache httpd (not nginx)
- Build: `build/client/` (static SPA files served by Apache)
- Auth: SSO via EDU AI parent system

**Architecture**: AiTutor is a "sister app" in the EDU AI ecosystem. EDU AI is the parent/centralized system handling login, logout, and course enrollment. AiTutor inherits enrolled students and AI model selection from EDU AI. The flagship feature is an AI chat with a "dual-loop backend" — a tutor agent that deliberately withholds answers for pedagogical reasons.

**Recurring themes in sessions**:
- Documentation: writing README, SYSTEM_OVERVIEW.md, ARCHITECTURE.md, API reference, comments across the codebase
- UI redesign: bold full-page redesigns using parallel Opus subagents
- Deployment: getting Apache + PM2 + Docker running correctly on the university server, writing a `deploy.sh` script adapted from professor-provided template
- Git: rebasing, stashing, committing, pushing to `github.com/Whiteknight07/AiTutor.git`
- Testing: running tests with bun before commit/push (mentioned as correction, not planned)
- Debugging: SSH into server, paste raw terminal output, diagnose PM2/Docker/Apache config

**Server deployment detail** (inferred from session):
- Repo lives at `/srv/www/AiTutor` (the Apache-served directory, is the canonical copy)
- PostgreSQL runs in Docker container
- Express API served via PM2 on port 4000
- Static frontend built to `build/client/`, served by Apache
- No nginx on this server — uses httpd

**Branch structure**: `main` (production), `testing-new-ui` (experimental), `feat/backend-testing-suite` (testing)

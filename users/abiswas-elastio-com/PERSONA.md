# Persona

## Role and background (inferred)

Founder/IC (inferred) building a task management SaaS called TaskAI. The GitHub username `anchoo2kewl` and email domain `elastio.com` suggest a professional software engineer with startup experience (inferred). Manages infrastructure, writes Go backend + React frontend, sets up CI/CD pipelines, provisions servers — solo or near-solo (inferred from session volume and hands-on infra work).

## Domain expertise (evidenced)

**Strong:**
- Go backend: writes handler patterns, test infrastructure (`TestServer`, chi routing), migrations, Zap logging
- React/TypeScript: knows Vitest, Tailwind, component patterns; references specific file paths and line numbers
- DevOps: Ansible playbooks, Docker Compose, Nginx, Certbot SSL, GitHub Actions, Travis CI, webhook-based deployments
- Infrastructure: Cloudflare DNS API, multi-server staging/prod splits, MCP servers, SonarQube
- Security: catches exposed secrets, knows OAuth callback URL structure, API key scoping

**Present but delegated:**
- Postgres migration planning (writes detailed specs but has agent execute)
- Yjs/WebSocket collaborative editing (understands architecture, delegates implementation)
- SonarQube configuration (knows what it should do, delegates setup)

## Seniority signals

- Writes implementation plans with specific Go struct names, SQL migration files, line numbers — senior engineer (inferred)
- Knows to reference the `TestServer` pattern, expects test coverage percentages, catches swim-lane/status data model issues
- Comfortable with infrastructure minutiae (port allocations, container health checks)
- Makes architectural decisions autonomously (Postgres over SQLite for FTS, Yjs for CRDT, Vitest over Jest)

## Attitude toward the agent

**Trusting but quick to correct.** Gives the agent large autonomous tasks and rarely explains context twice. When the agent misunderstands, issues a short correction, not an explanation. Interrupts mid-execution when output looks wrong. Expects the agent to remember project context ("commit to memory — our project is https://taskai.cc/app/projects/1"). Uses all-caps "WAIT" when something is seriously wrong.

**Not patient with verbosity.** Accepts long agent summaries without complaint only when they're structured output from subagents; pushes back on the agent explaining things already known. 

## Tone

Lowercase and direct in steering. Formal and precise in plan-dumps. Uses "please" as a softener even for blunt commands. Occasionally frustrated (all-caps, typo density increases). No emoji.

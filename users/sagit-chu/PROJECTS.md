# Projects: sagit-chu

## Sagit-chu/flvx ★ dominant repo (100% of sessions)

**What it is**: A self-hosted network tunnel and port-forwarding management platform. Users get tunnel permissions (bandwidth quotas, IP restrictions); admins manage nodes, forwarding rules, and speed limits. Think "FRP management panel with a multi-user web UI".

**Tech stack**:
- Backend: Go (`go-backend/`), SQLite, internal service called `flux_agent` on nodes
- Frontend: Vite + React (`vite-frontend/`), HeroUI / shadcn components
- Deployment: Docker images on `ghcr.io/sagit-chu/`, multi-arch (`linux/amd64`)
- Version tagging: `beta`, `alpha` tags on GHCR
- CI/integration: GitHub Issues and PRs; numbered plan docs in `plans/`

**Key domain concepts**:
- **转发 / 规则** (forwarding / rules) — port-forwarding rules created by users
- **隧道** (tunnel) — tunnel-based forwarding; users have tunnel permissions with flow quotas
- **节点** (node) — server nodes running `flux_agent` that execute forwarding services
- **精简模式** (compact mode) — an alternate UI layout for the forwarding page
- **入口 / 出口** (ingress / egress) — forwarding entry/exit endpoints with IP binding
- **下发** (config push/deploy) — pushing rule configs from the panel to nodes
- **extra_ips** — additional IP addresses feature added during the observed period
- **connectIp** — dual-role field: upstream dial target AND local listen bind address

**Recurring themes across sessions**:
- Upgrade compatibility bugs: old service naming schemes conflicting with new code after version upgrades (2.1.6 → current).
- Port-occupied (`address already in use`) errors during tunnel/forward create or update.
- Flow statistics not accumulating correctly for users (`user_tunnel` table).
- UI consistency: compact mode vs. normal mode feature parity, drag-sort, collapse state persistence.
- Docker image build and push after frontend changes (repeated every few sessions).
- Rename of "转发" → "规则" UI-wide with careful preservation of technical terms.
- Plan doc discipline: every significant task gets a `plans/<NNN>-<title>.md`.

**Agent interaction model**: User directs the agent on what to build/fix; agent reads the codebase, writes plan docs, implements, and compiles. User approves or scopes down the plan with one-liners.

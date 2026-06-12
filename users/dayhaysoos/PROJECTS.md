# Projects

## dayhaysoos/nimbus ★ dominant repo (100% of sessions)

**What it is**: An AI-powered code review platform. Developers run `nimbus review create` from their repo; Nimbus diffs the changes, sends them to an LLM agent, and returns structured findings with severity, category, file/line locations, and suggested fixes. Reviews surface in PR comments and a report UI.

**Architecture**:
- `packages/worker/` — Cloudflare Worker; REST API (`/api/reviews/:id`, `/api/repos/register`, etc.); SSE event stream for review lifecycle; review analysis via OpenRouter; idempotent review runner with retry behavior
- `packages/cli/` — `nimbus` CLI; commands: `review create`, `repo register`, `workspace create`, `workspace deploy`; reads `NIMBUS_WORKER_URL` and `NIMBUS_API_KEY` from env; uses `workerFetch()` utility
- `packages/report-ui/` — Vite/React SPA; route `/reports/:reviewId`; fetches from worker API; copy-to-agent UX (copy full markdown, copy per-finding fix prompt)
- `.github/workflows/nimbus-pr-review.yml` — GitHub Actions workflow; triggered on PR events; runs review, posts findings as PR comment

**Key data model**:
- **Workspace** → **Deployment** → **Review** (three-step lifecycle)
- Review statuses: queued → running → review_analysis_agent_started → review_analysis_fallback → succeeded/failed
- Findings: `{ severity, category, passType, locations: [{filePath, startLine, endLine}], description, suggestedFix }`
- Review export: markdown summary + raw JSON

**Integration with "Entire"**:
- "Entire" is a separate checkpoint/session-tracking tool the user uses alongside Nimbus
- Entire provides `intentSessionContext` — extracted session notes used to inform review policy (prohibitions, risk focus, goals)
- Sessions reference "Entire checkpoints" (e.g., `29dc5c812720`); these carry `Entire-Attribution` metadata
- The user is figuring out whether intent context comes from human developer notes vs. AI agent sessions

**Recurring themes**:
- **Review quality**: the agent path (`AGENT_ENDPOINT`) returns fallback results; user repeatedly investigates why `review_analysis_fallback` fires
- **PR comment UX**: went through multiple iterations — sticky comment → checks tab → one comment per run; settled on per-run comment with compact findings format
- **Security hardening**: actively incorporates security findings from Nimbus back into Nimbus's own workflow (PR trust detection, secret exposure, race conditions)
- **Intent/policy capture**: building a pre-pass that summarizes session prompts into intent signals; iterating on what the system prompt should extract

**Tech stack**:
- TypeScript, Cloudflare Workers, Wrangler, R2, pnpm workspaces
- OpenRouter (`anthropic/claude-haiku-4-5` for pre-pass, main agent model via `AGENT_PROVIDER`/`AGENT_MODEL`)
- Vite + React for report UI
- GitHub Actions + `gh` CLI
- `wrangler.toml` config with `NIMBUS_HOSTED` flag

**Phase naming convention** (inferred from sessions):
- Phase 1: initial CLI/worker setup
- Phase 5: `nimbus repo register` command
- Phase 8A: end-to-end cloud review flow (workspace → deploy → review → events → show → export)
- "Minimal Report UI V1": report page with copy-to-agent UX

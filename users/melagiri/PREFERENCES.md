# Preferences: melagiri

## What satisfies him

- Agent follows the full ceremony without being reminded
- PRs created, pushed, and left for him to merge — never auto-merged
- Review comments are addressed with zero deferrals (or deferral explicitly surfaced for his decision)
- Version bumps executed exactly as specified: all three steps (code changes + npm publish + gh release)
- Agent applies technical critiques precisely (exact field names, correct file paths)
- Terse status reports: table of items + status, not paragraph prose
- When he says "go ahead" or "i am good", agent proceeds immediately without re-confirming
- Short completion signals: "PR created?" gets a PR URL, not a summary of what was done

## What triggers correction (35.5% pushback rate)

- **Declaring done prematurely**: agent marks ceremony complete but a step was skipped (e.g., wild card review criteria not checked)
- **Deferring issues as "MVP / future work"**: hard no — every review comment must be addressed or escalated to him
- **Wrong technical details in review output**: he will paste the corrected content (exact field name, exact line reference) and expect it applied
- **Agent auto-commits to master without permission**: "we must not store and git commit the transient docs for implementation plans"
- **Summarizing review output instead of pasting it**: he re-pastes the full artifact when the agent summarizes
- **Missing ceremony step in agent team**: skipping the TA insider review, skipping wild card when criteria met
- **Stale docs not cleaned up**: "we should delete all transient docs from the codebase like plan docs"
- **NPM version not updating**: follows up with failure report if npm still shows old version after publish
- **AI tool tag missing from sessions**: "claude-code tag is missing.. i mean the ai tool info is missing"

## What triggers failure report (4.3%)

- Silent failures: button does nothing, feature silently broken, no error shown
- Pastes raw stdout/stderr verbatim: no commentary, just the output
- "try again" after fix attempt

## What triggers takeover (0.7%)

- Agent about to do something that requires his direct action (git push to master, blog post merge timing)

## Workflow habits

- **Planning first**: uses brainstorming skill before implementation; expects design approval gate
- **Not test-driven in practice**: tests are added as a separate PR or CI gate, not written first
- **Commit cadence**: feature branches via worktrees; merges PRs himself; occasional direct-to-master for patches
- **Multi-agent by default**: complex features always involve PM, TA, and dev agents
- **Ceremony for every feature**: no "quick fix" bypasses the review process except tiny 1-line patches ("or no need to review because it is simple 1 line fix, ensure tests pass")
- **Explanations**: rarely wants explanations; wants results. Does ask "explain me" / "what are we capturing" questions for product/telemetry decisions he needs to reason about.
- **Plans not committed**: "we must not store and git commit the transient docs for implementation plans"
- **Docs kept current**: periodically audits docs vs. code, deletes stale plans, updates PRODUCT.md/VISION.md/ROADMAP.md

## Stack / tool preferences

- pnpm monorepo (never npm/yarn for workspace commands)
- Hono for server, React+Vite+shadcn for dashboard
- SQLite (better-sqlite3), migrations with `runMigrations()`
- Vitest for tests, in-memory SQLite for DB tests
- PostHog for analytics (not Supabase)
- GitHub CLI (`gh`) for PRs and releases
- `@code-insights/cli` published to npm
- Custom agent personas: `technical-architect`, `product-manager`, `ux-engineer`, `engineer`, `llm-expert`, `devtools-cofounder`, `outsider-reviewer`

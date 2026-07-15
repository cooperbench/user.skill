> DEVELOPER

hey man can you have a look at https://github.com/elijahintelligence/elijah/pull/237/changes please. We need to add that for sumeet I need to add peroper user account (go from login to pirvate runs for that user and controls on them ect) there are a few related teickets alrady in the linear have a look

> TOOL

tool_use ToolSearch
id: toolu_0122sGdA6ofi4CSy6KXSJiSy
```json
{
  "query": "select:WebFetch,mcp__linear__list_issues,mcp__linear__get_issue,mcp__linear__list_projects,TaskCreate",
  "max_results": 10
}
```

> TOOL

tool_result
id: toolu_0122sGdA6ofi4CSy6KXSJiSy
```
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__linear__list_issues"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__linear__get_issue"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__linear__list_projects"
}
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
```

> TOOL

tool_use Bash
id: toolu_016rprg3yNxJLkBiYTeXsHNu
```json
{
  "command": "gh pr view 237 --repo elijahintelligence/elijah",
  "description": "View PR #237 details"
}
```

> TOOL

tool_result
id: toolu_016rprg3yNxJLkBiYTeXsHNu
```
title:	Demo readiness plan — Mon 25 May 2026
state:	OPEN
author:	hqmf8104
labels:	
assignees:	
reviewers:	kungfusaini (Sumeet Saini) (Requested)
projects:	
milestone:	
number:	237
url:	https://github.com/elijahintelligence/elijah/pull/237
additions:	122
deletions:	0
auto-merge:	disabled
--
## Summary

Adds [`docs/plans/demo-2026-05-25.md`](docs/plans/demo-2026-05-25.md) — the week's plan for getting Elijah ready to demo on Monday 25 May 2026.

11 tasks across UI wireframe sign-off, Operator Lab tuning end-to-end (individual surfaces → families → full-system), FS4 / FS5 PR review, Friday deploy, Friday testing, and Saturday-only bug fixes.

## Why this lives in `docs/plans/` instead of Linear

Our Linear workspace has hit its free-tier issue cap — `Usage limit exceeded - You've exceeded the free issue limit for this workspace` came back when I tried to spin up the umbrella + 11 children. I'll upgrade Linear later this week. Until then, this markdown file is the source of truth for the week's plan; the file's "Migration to Linear" section at the bottom has the exact recipe for promoting it once the cap lifts.

## Asking @kungfusaini for input

A few things specifically need your eyes on / sign-off before tomorrow:

1. **Task #1 — wireframe sign-off** (you + me, Mon EOD). The wireframe is essentially complete; this is the last-mile review. Let me know what you want me to point you at.
2. **Task #7 — deploy tuned surfaces to main** on Friday. Confirm Friday morning works for you; if Thursday evening is easier, even better — Friday testing can run against the deployed state instead of staging.
3. **Parallel work today** — I've added your vLLM port to the "Parallel work in flight" table. PR #229 (local-SLM tier mapping, all tiers → `qwen2.5-14b-instruct-awq`) was opened this morning; flagging in case it should land before your port. Happy to re-spin if you want a different mapping.
4. **Sunday is off-limits, Saturday is the only bug-fix day** — that's the constraint Paddy set. Worth raising now if anything in the plan looks tight against that window (full-system tuning over Wed + Thu, deploy Fri, then one fix day).

## Test plan

- [ ] @kungfusaini reads the plan and either acks in a comment or flags concerns inline.
- [ ] If we're aligned, merge; subsequent status updates land directly on the file in dev_sprint until Linear is upgraded.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

> TOOL

tool_use Bash
id: toolu_01BvQhWzL1n1GzAtcfDmREfY
```json
{
  "command": "gh pr diff 237 --repo elijahintelligence/elijah | head -300",
  "description": "View PR #237 diff (first 300 lines)"
}
```

> TOOL

tool_use mcp__linear__list_issues
id: toolu_01QGGXjpyCEcB62gmedgMy6d
```json
{
  "query": "user account login auth",
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01BvQhWzL1n1GzAtcfDmREfY
```
diff --git a/docs/plans/demo-2026-05-25.md b/docs/plans/demo-2026-05-25.md
new file mode 100644
index 00000000..0ea60b90
--- /dev/null
+++ b/docs/plans/demo-2026-05-25.md
@@ -0,0 +1,122 @@
+# Demo readiness — Mon 25 May 2026
+
+**Goal**: Elijah ready to demo on Monday 25 May 2026.
+**Friday checkpoint**: deploy + end-to-end testing & review on Friday 22 May (Paddy, Sumeet, Tom, Rich). Bug-fix budget is **Saturday only**.
+**Hard rules**: Sunday is off-limits for work. Saturday is the only bug-fix day, so anything not fixed by Saturday evening is either deferred or gets cut from the demo script.
+**Replaces**: the cancelled [SPI-87 — User Testing Round 1](https://linear.app/spire-elijah/issue/SPI-87) umbrella. Will be promoted to a Linear umbrella ticket once the workspace is upgraded; until then this file is the source of truth.
+
+## Timeline at a glance
+
+| Day | Date | Focus |
+|---|---|---|
+| Mon | 18 May | Wireframe → Sumeet input + mutual sign-off; Sumeet ports vLLM in parallel; Operator Lab functional; **individual-surface tuning by COP**; FS4 / FS5 PR review starts |
+| Tue | 19 May | Wireframe stage-1 / stage-2 breakdown (Paddy, Sumeet review); **surface-family / group tuning by COP** |
+| Wed | 20 May | **Full-system tuning run #1** |
+| Thu | 21 May | **Full-system tuning run #2**; FS4 / FS5 PRs landed |
+| Fri | 22 May | Deploy tuned surfaces to main (Sumeet) → testing & review (Paddy, Sumeet, Tom, Rich) |
+| Sat | 23 May | **Bug-fix day** (the only one) |
+| Sun | 24 May | **No work** |
+| Mon | 25 May | **Demo** |
+
+## Tasks
+
+### 1. Land the new UI wireframe (Sumeet input + mutual sign-off)
+- **Owners**: Paddy (drives) + Sumeet (review)
+- **Target**: Mon 18 May EOD
+- **Status**: ☐ Open
+- **Scope**: Wireframe design is essentially complete. This task is the **last mile** — Sumeet reviews the current artifact, surfaces any blocking concerns, both sign off. No fresh design work.
+- **Definition of done**: Wireframe under `docs/wireframes/workspace-router/` agreed by Paddy and Sumeet (a one-line ack in the PR or a Linear comment is enough). Hands off to #2.
+
+### 2. Break the wireframe into "stage 1" and "stage 2" releases
+- **Owner**: Paddy (Sumeet review)
+- **Target**: Tue 19 May EOD
+- **Status**: ☐ Open
+- **Depends on**: #1
+- **Definition of done**: Stage-1 (Monday-demo) vs stage-2 (post-demo) split documented inline in the wireframe folder or this file. Sumeet has signed off.
+
+### 3. Get Operator Lab functional for surface tuning
+- **Owner**: Paddy
+- **Target**: Mon 18 May EOD (prerequisite for #4 the same day)
+- **Status**: ☐ Open
+- **Definition of done**: Each tuning surface in the Operator Lab can be selected, calibrated, and promoted without manual DB / CLI intervention. Smoke-tested against the local stack.
+
+### 4. Tune all surfaces individually
+- **Owner**: Paddy
+- **Target**: **Mon 18 May COP**
+- **Status**: ☐ Open
+- **Depends on**: #3
+- **Definition of done**: Every implemented tuning surface has a promoted candidate (FS1 question drafter, FS2 boosts × 4, FS2 coverage planner + gap reroute, FS2B iw_verdict, FS3 chain steps × 6 + admission gate, FS4 Fermi chain × 6 LLM + calibration head, FS5 edge Fermi chain × 5 LLM + multiplier head).
+
+### 5. Tune all surface families / groups
+- **Owner**: Paddy
+- **Target**: **Tue 19 May COP**
+- **Status**: ☐ Open
+- **Depends on**: #4
+- **Definition of done**: Each surface family / chain (FS2A query-boost lane, FS2B coverage, FS3 driver→indicator→admission chain, FS4 Fermi chain, FS5 edge Fermi chain) is jointly tuned and the family-level candidate promoted.
+
+### 6. Full-system tuning runs
+- **Owner**: Paddy
+- **Targets**: Run #1 — Wed 20 May; Run #2 — Thu 21 May
+- **Status**: ☐ Open
+- **Depends on**: #5
+- **Definition of done**: Two full-system tune runs executed. Final whole-model candidate beats the pre-tune baseline on the held-out replay window. Result snapshot + Brier comparison captured before handoff to #7.
+
+### 7. Deploy tuned surfaces to main
+- **Owner**: Sumeet
+- **Target**: Fri 22 May (before #9 testing session)
+- **Status**: ☐ Open
+- **Depends on**: #6
+- **Definition of done**: Tuned candidates promoted on prod and reachable from the demo environment. Smoke-check that `demo.elijahintelligence.com` serves the tuned model.
+
+### 8a. Review FS4 PRs
+- **Owner**: Paddy first pass; Sumeet review once green
+- **Target**: Thu 21 May
+- **Status**: ☐ Open
+- **Definition of done**: All open FS4-related PRs reviewed, addressed, and merged.
+
+### 8b. Review FS5 PRs
+- **Owner**: Paddy first pass; Sumeet review once green
+- **Target**: Thu 21 May
+- **Status**: ☐ Open
+- **Definition of done**: All open FS5-related PRs (including the FS5 edge Fermi chain stack) reviewed, addressed, and merged.
+
+### 9. Final demo testing and review
+- **Attendees**: Paddy, Sumeet, Tom, Rich
+- **When**: Fri 22 May (post #7 deploy)
+- **Status**: ☐ Scheduled (calendar invite TBD — Paddy to send)
+- **Depends on**: #1–#8 landed; #7 deployed
+- **Outputs**: prioritised bug + polish list feeding #10. Notes captured here or in a child doc.
+
+### 10. Fix Friday-testing bugs (Saturday only)
+- **Owner**: Paddy (Sumeet support if infra)
+- **Target**: **Sat 23 May only** (Sunday is off; no fallback day)
+- **Status**: ☐ Open
+- **Depends on**: #9
+- **Definition of done**: All blocker-tier bugs from the Friday session closed by Saturday evening. Anything not fixed is explicitly deferred and noted in the demo script.
+
+## Parallel work in flight today
+
+| Item | Owner | Notes |
+|---|---|---|
+| Port vLLM to `dev` | Sumeet | Running in parallel with the plan above today (Mon 18 May). Related: PR #229 (local-SLM tier mapping for `qwen2.5-14b-instruct-awq`) opened by Paddy this morning and waiting on review. Sumeet's port may want to land that first. |
+
+## Standing blockers also targeted before demo
+
+These existed before this plan; they're not in the 11-step list but block the same Monday demo.
+
+| Ticket | Title | Owner | Status |
+|---|---|---|---|
+| [SPI-224](https://linear.app/spire-elijah/issue/SPI-224) | arXiv 429 blocks all evidence retrieval | Paddy | Urgent, Backlog (just reassigned) |
+| [SPI-272](https://linear.app/spire-elijah/issue/SPI-272) | Staging verification of the SPI-238 porting epic | Sumeet | High, In Progress |
+| [SPI-273](https://linear.app/spire-elijah/issue/SPI-273) | Add litellm-seed to staging/prod compose + per-env `LLM_MODEL_SET` | Sumeet | Urgent, In Progress |
+| [SPI-274](https://linear.app/spire-elijah/issue/SPI-274) | Port Anthropic Claude model-family refresh | Sumeet | Urgent, In Progress |
+| [SPI-275](https://linear.app/spire-elijah/issue/SPI-275) | `gpt-5.2` alias rejected by OpenRouter | Sumeet | High, Backlog |
+
+## Migration to Linear
+
+When the Linear workspace is upgraded (currently capped on the free tier), promote this file as follows:
+
+1. Create umbrella issue **"Demo readiness — Mon 25 May 2026"** in `Spire_Elijah` / `Elijah Pipeline Development`. Assignee Paddy, priority Urgent, due `2026-05-25`. Copy this file's "Goal" / "Friday checkpoint" / "Plan" sections into the description.
+2. Create one child per task above (1, 2, 3, 4, 5, 6, 7, 8a, 8b, 9, 10) with the listed owner / target / definition of done.
+3. Link the standing blockers (SPI-224 / SPI-272 / SPI-273 / SPI-274 / SPI-275) as `relatedTo` on the umbrella.
+4. Keep this markdown file as the source of truth for status until the migration; archive it once Linear is canonical.
```

> TOOL

tool_result
id: toolu_01QGGXjpyCEcB62gmedgMy6d
```
{"issues":[{"id":"SPI-176","title":"Phase 2 Auth: User accounts, JWT sessions, and role-based access","description":"## Goal\n\nReplace the shared API key (<issue id=\"3a21df32-bffb-4f53-97bf-2452ef6be1f9\">SPI-17</issue>) with proper user accounts, JWT sessions for the frontend, and role-based access control. The deployment model is self-hosted, multi-user, single org — like running your own GitLab or Grafana instance.\n\nDepends on: <issue id=\"3a21df32-bffb-4f53-97bf-2452ef6be1f9\">SPI-17</issue> (shared API key must be in place first)\n\n## What to build\n\n### 1\\. Us… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-176/phase-2-auth-user-accounts-jwt-sessions-and-role-based-access","gitBranchName":"sumeet/spi-176-phase-2-auth-user-accounts-jwt-sessions-and-role-based","createdAt":"2026-04-15T10:04:53.046Z","updatedAt":"2026-04-16T15:16:26.908Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":["Security","Feature"],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-236","title":"Port API auth, job/run-config propagation, and worker context","description":"## What this is\n\n`dev` lacks multi-user API key registry, run-detail/job artifact surfaces, run-config propagation, and worker context helpers. User-visible and operationally useful, but depends heavily on storage/run-config base. API behavior should not land before the DB/run-config authorities it exposes.\n\n**Lane:** 4 (standalone once base storage is done)\n\n## Agent workflow\n\nFollow the 5-phase workflow defined in the parent epic <issue id=\"c0… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-236/port-api-auth-jobrun-config-propagation-and-worker-context","gitBranchName":"sumeet/spi-236-port-api-auth-jobrun-config-propagation-and-worker-context","createdAt":"2026-05-11T14:50:41.084Z","updatedAt":"2026-05-17T18:52:48.604Z","archivedAt":null,"completedAt":"2026-05-12T13:46:03.623Z","startedAt":"2026-05-11T15:26:10.111Z","canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":["Feature"],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-238","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-177","title":"Phase 3 Auth: Per-user spend controls, budgets, and audit trail","description":"## Goal\n\nWith user accounts in place (<issue id=\"1884f69a-cde2-421a-8bce-5e17c9ea1ea1\">SPI-176</issue>), add per-user LLM spend tracking, budget enforcement, and an audit trail. Every LLM call is attributed to the user who triggered it, spend is capped per user, and there's a dashboard showing who spent what.\n\nDepends on: <issue id=\"1884f69a-cde2-421a-8bce-5e17c9ea1ea1\">SPI-176</issue> (user accounts must exist to attribute spend to users)\n\n## E… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-177/phase-3-auth-per-user-spend-controls-budgets-and-audit-trail","gitBranchName":"sumeet/spi-177-phase-3-auth-per-user-spend-controls-budgets-and-audit-trail","createdAt":"2026-04-15T10:05:20.077Z","updatedAt":"2026-04-22T10:09:50.956Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":["Security","Feature"],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-243","title":"Bridge CF ZT email to per-user Elijah identity for GUI users","description":"## Problem\n\nGUI users authenticate via Cloudflare Zero Trust (email → CF session cookie) but the Elijah backend treats them all as the same anonymous shared key. There is no per-user identity at the API layer for browser users, so rate limits, cost caps, and job attribution cannot distinguish between them.\n\nCF ZT injects the authenticated user's email in the `Cf-Access-Authenticated-User-Email` request header on every request that passes through… (truncated, use `get_issue` for full description)","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-243/bridge-cf-zt-email-to-per-user-elijah-identity-for-gui-users","gitBranchName":"sumeet/spi-243-bridge-cf-zt-email-to-per-user-elijah-identity-for-gui-users","createdAt":"2026-05-12T13:37:30.206Z","updatedAt":"2026-05-12T13:39:47.236Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-247","title":"Remove shared ELIJAH_API_KEY fallback once per-user identity lands","description":"## Problem\n\nThe current auth system has a fallback mode where a single shared `ELIJAH_API_KEY` is accepted and maps all callers to an anonymous `\"shared\"` user. This was a backward-compatibility shim to avoid breaking existing deployments while per-user identity was being built. Once every caller (GUI users via CF ZT, programmatic callers via `api_users.toml`) has a real identity, the shared key fallback should be removed.\n\n## Goal\n\n* Remove `fa… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-247/remove-shared-elijah-api-key-fallback-once-per-user-identity-lands","gitBranchName":"sumeet/spi-247-remove-shared-elijah_api_key-fallback-once-per-user-identity","createdAt":"2026-05-12T13:39:45.694Z","updatedAt":"2026-05-12T13:39:47.203Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-242","title":"Explore CF ZT → per-user Elijah identity bridging","description":"## Background\n\nThe API now has a `UserRegistry` foundation (landed in <issue id=\"18828e58-fbc6-478f-b0bb-262d2e9b5cba\">SPI-236</issue> / PR #184) that maps API keys to `User` objects. Right now browser users authenticate via Cloudflare Zero Trust (email → CF session cookie) and the frontend uses a single shared `ELIJAH_API_KEY` injected into the HTML. There is no per-user identity at the Elijah API layer for browser users.\n\n## Problem\n\nBecause a… (truncated, use `get_issue` for full description)","priority":{"value":4,"name":"Low"},"url":"https://linear.app/spire-elijah/issue/SPI-242/explore-cf-zt-per-user-elijah-identity-bridging","gitBranchName":"sumeet/spi-242-explore-cf-zt-per-user-elijah-identity-bridging","createdAt":"2026-05-12T13:25:14.072Z","updatedAt":"2026-05-12T13:37:30.206Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-186","title":"Enable Cloudflare Access (SSO) on prod hostname","description":"## Goal\n\nGate access to the public Elijah Cloud hostname using Cloudflare Access (Zero Trust). Only allow-listed users can authenticate via SSO (Google IdP) before they can reach the app.\n\n## Why Cloudflare Access\n\n* Authentication happens at the Cloudflare edge — unauthenticated traffic never hits Betty\n* Free tier supports up to 50 users\n* Google SSO out of the box (no password management on our side)\n* Independent of app-level auth (<issue id… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-186/enable-cloudflare-access-sso-on-prod-hostname","gitBranchName":"sumeet/spi-186-enable-cloudflare-access-sso-on-prod-hostname","createdAt":"2026-04-16T15:15:50.881Z","updatedAt":"2026-04-23T10:54:26.853Z","archivedAt":null,"completedAt":"2026-04-23T10:54:26.841Z","startedAt":"2026-04-20T20:12:15.728Z","canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-182","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-183","title":"Provision Betty service account and SSH access","description":"## Status: Done (2026-04-16)\n\nOne-time setup of the donated Dell Precision 7920 Tower (\"Betty\", Patrick's box) for Elijah Cloud hosting.\n\n## What was done\n\n### Network access\n\n* Joined Patrick's Tailscale tailnet (`patrick.a.m2020@gmail.com`) as `sumeet@sumeetsaini.com`\n* Box reachable at tailnet IP `100.87.151.63` (hostname `paddy-precision-7920-tower`)\n* SSH alias `betty` configured locally → `sumeet@100.87.151.63` using `~/.ssh/id_elijah`\n\n##… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-183/provision-betty-service-account-and-ssh-access","gitBranchName":"sumeet/spi-183-provision-betty-service-account-and-ssh-access","createdAt":"2026-04-16T15:15:20.616Z","updatedAt":"2026-04-20T19:22:47.139Z","archivedAt":null,"completedAt":"2026-04-16T15:15:20.761Z","startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-182","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-184","title":"Install and configure Cloudflare Tunnel on Betty","description":"## Goal\n\nExpose the Elijah stack running on Betty to the public internet via Cloudflare Tunnel — no inbound ports opened on Patrick's network, no router config, automatic HTTPS, custom domain.\n\n## Why Cloudflare Tunnel\n\n* **No sudo required** — `cloudflared` is a single static binary, runs as `systemctl --user` under the `elijah` account\n* **No router/firewall changes** — outbound-only connection from Betty to Cloudflare edge\n* **No public IP ne… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-184/install-and-configure-cloudflare-tunnel-on-betty","gitBranchName":"sumeet/spi-184-install-and-configure-cloudflare-tunnel-on-betty","createdAt":"2026-04-16T15:15:32.969Z","updatedAt":"2026-04-23T07:45:26.398Z","archivedAt":null,"completedAt":"2026-04-23T07:45:26.382Z","startedAt":"2026-04-20T20:12:14.912Z","canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-182","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-96","title":"LLM spending controls: tracking, budgets, and per-user limits","description":"## Superseded by <issue id=\"03c9aa85-7159-4734-863b-ae0716abc6c8\">SPI-177</issue> (2026-04-16)\n\nThis umbrella ticket has been superseded by <issue id=\"03c9aa85-7159-4734-863b-ae0716abc6c8\">SPI-177</issue> **(Phase 3 Auth: Per-user spend controls, budgets, and audit trail)**, which incorporates the user-accounts model (<issue id=\"1884f69a-cde2-421a-8bce-5e17c9ea1ea1\">SPI-176</issue>) and absorbed all the original sub-tickets:\n\n* <issue id=\"abc603… (truncated, use `get_issue` for full description)","priority":{"value":4,"name":"Low"},"url":"https://linear.app/spire-elijah/issue/SPI-96/llm-spending-controls-tracking-budgets-and-per-user-limits","gitBranchName":"sumeet/spi-96-llm-spending-controls-tracking-budgets-and-per-user-limits","createdAt":"2026-04-02T11:40:40.462Z","updatedAt":"2026-04-16T15:17:12.201Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":"2026-04-16T15:17:12.083Z","dueDate":"2026-05-02","slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Duplicate","statusType":"canceled","labels":["Feature"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-187","title":"Add initial demo users to Cloudflare Access allow-list","description":"## Goal\n\nPopulate the Cloudflare Access policy with the initial set of demo users for Elijah Cloud user testing.\n\n## Steps\n\n1. In Cloudflare Zero Trust → Access → Applications → `<elijah-prod-app>` → Policies\n2. Edit the Allow policy\n3. Add the initial users (see comment for current list)\n4. For each user: send them the prod URL and a short note on what to expect (Google SSO login, then the Elijah app)\n\n## Acceptance criteria\n\n* Listed users can… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-187/add-initial-demo-users-to-cloudflare-access-allow-list","gitBranchName":"sumeet/spi-187-add-initial-demo-users-to-cloudflare-access-allow-list","createdAt":"2026-04-16T15:15:55.416Z","updatedAt":"2026-04-23T10:54:27.314Z","archivedAt":null,"completedAt":"2026-04-23T10:54:27.302Z","startedAt":"2026-04-20T20:12:16.396Z","canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-182","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-189","title":"Spike: Use LiteLLM virtual keys for per-user spend tracking and enforcement","description":"## Goal\n\nInvestigate using **LiteLLM's built-in virtual key system** as the implementation substrate for per-user LLM spend tracking and budget enforcement, instead of building those capabilities in Elijah application code.\n\n## Background\n\nLiteLLM proxy (already deployed — see <issue id=\"225d6f2e-fcbb-4913-8d4b-fbf9d3423499\">SPI-28</issue>) supports:\n\n* Virtual API keys per user/team\n* Per-key budget limits (daily / monthly / lifetime)\n* Per-key… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-189/spike-use-litellm-virtual-keys-for-per-user-spend-tracking-and","gitBranchName":"sumeet/spi-189-spike-use-litellm-virtual-keys-for-per-user-spend-tracking","createdAt":"2026-04-16T15:16:26.908Z","updatedAt":"2026-04-22T10:09:50.993Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-177","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-182","title":"Elijah Cloud — production hosting, access, and validation","description":"## Goal\n\nStand up Elijah as a hosted product on the donated Betty workstation: automated deploys from GitHub, public HTTPS access via Cloudflare Tunnel, SSO-gated user access, per-user LLM spend attribution, and nightly validation runs that catch regressions.\n\n## Scope\n\nThis is the umbrella for everything needed to run Elijah as \"Elijah Cloud\" for the May 2026 user testing round and onward. Children below.\n\n## Children\n\n1. Provision Betty servic… (truncated, use `get_issue` for full description)","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-182/elijah-cloud-production-hosting-access-and-validation","gitBranchName":"sumeet/spi-182-elijah-cloud-production-hosting-access-and-validation","createdAt":"2026-04-16T15:14:57.233Z","updatedAt":"2026-05-11T14:19:09.809Z","archivedAt":null,"completedAt":"2026-05-11T14:19:09.798Z","startedAt":"2026-04-20T19:03:43.157Z","canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-27","title":"User Testing","description":"Conduct user testing to validate pipeline outputs, UI usability, and end-to-end workflow.\n\nScheduled alongside Assessment Accuracy Tuning (SPI-10) in week 8 (May 19-23) — user feedback informs final accuracy calibration.","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-27/user-testing","gitBranchName":"sumeet/spi-27-user-testing","createdAt":"2026-03-30T08:07:03.980Z","updatedAt":"2026-04-02T11:46:09.244Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":"2026-04-02T11:46:09.233Z","dueDate":"2026-05-23","slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Duplicate","statusType":"canceled","labels":["Improvement"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-99","title":"Per-user budget configuration","description":"Add a budget system that associates spending limits with users/sessions. Configuration via env vars or admin API: daily budget, per-run budget, total budget. Store budget config and current spend in the database.","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-99/per-user-budget-configuration","gitBranchName":"sumeet/spi-99-per-user-budget-configuration","createdAt":"2026-04-02T11:40:42.160Z","updatedAt":"2026-05-14T23:40:12.644Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":"2026-05-15","slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":["Feature"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-177","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-244","title":"Pass user_id to LiteLLM on every call for per-user spend tracking","description":"## Problem\n\nEvery LLM call goes through LiteLLM but carries no user identity. LiteLLM supports a `user` field on API calls that it uses to track spend per user and enforce per-user budget limits — but we never set it, so all spend rolls up anonymously.\n\n## Goal\n\nThread `user_id` from the resolved `User` object (available on `request.state.user` after <issue id=\"82119d08-ad3c-4270-b6e4-773434c40d78\">SPI-243</issue> lands) down to every LiteLLM ca… (truncated, use `get_issue` for full description)","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-244/pass-user-id-to-litellm-on-every-call-for-per-user-spend-tracking","gitBranchName":"sumeet/spi-244-pass-user_id-to-litellm-on-every-call-for-per-user-spend","createdAt":"2026-05-12T13:37:42.609Z","updatedAt":"2026-05-17T18:52:48.604Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-88","title":"Identify personas for user testing","description":"## Sprint: Paddy Week 2-3 (Apr 13-25)\n\n## Assignee: Paddy\n\nDefine target user personas for testing. Consider: forecasting analysts, research teams, domain experts (geopolitics, economics), technical users, non-technical stakeholders.\n\nLightweight task — 1-2 hours to draft persona profiles.","priority":{"value":1,"name":"Urgent"},"url":"https://linear.app/spire-elijah/issue/SPI-88/identify-personas-for-user-testing","gitBranchName":"sumeet/spi-88-identify-personas-for-user-testing","createdAt":"2026-04-02T11:39:56.863Z","updatedAt":"2026-05-15T07:53:02.932Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":"2026-05-15T07:53:02.916Z","dueDate":"2026-04-09","slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Canceled","statusType":"canceled","labels":["Operational"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","assignee":"Patrick M","assigneeId":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-87","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-70","title":"User-selectable graph layout options","description":"Currently the graph layout is fixed. Add the ability for users to switch between different layout algorithms from the frontend.\n\nCytoscape.js supports multiple layout options out of the box (e.g. dagre/hierarchical, cose/force-directed, breadthfirst, concentric, grid). Expose a layout selector in the UI so users can pick the arrangement that best suits the graph they are viewing.\n\n**Requirements:**\n\n* Layout selector control in the graph toolbar… (truncated, use `get_issue` for full description)","priority":{"value":0,"name":"No priority"},"url":"https://linear.app/spire-elijah/issue/SPI-70/user-selectable-graph-layout-options","gitBranchName":"sumeet/spi-70-user-selectable-graph-layout-options","createdAt":"2026-04-01T08:05:02.288Z","updatedAt":"2026-04-02T05:09:37.361Z","archivedAt":null,"completedAt":"2026-04-01T20:26:18.440Z","startedAt":"2026-04-01T17:15:27.628Z","canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":["Feature"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","assignee":"Patrick M","assigneeId":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-91","title":"Design user feedback mechanism","description":"Define how feedback is captured during and after testing. Options: think-aloud protocol during sessions, post-task questionnaires (SUS, custom Likert scales), structured interview questions, screen recording with consent. Design the feedback forms and data collection process.","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-91/design-user-feedback-mechanism","gitBranchName":"sumeet/spi-91-design-user-feedback-mechanism","createdAt":"2026-04-02T11:39:57.789Z","updatedAt":"2026-05-15T07:54:04.447Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":"2026-05-15T07:54:04.431Z","dueDate":"2026-05-12","slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Canceled","statusType":"canceled","labels":["Operational"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","assignee":"Patrick M","assigneeId":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-87","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-87","title":"User Testing Round 1 — May 2026","description":"## User Testing Round 1 - May 2026\n\n## Organiser: Paddy\n\nPlan and execute the first round of user testing. Paddy owns the organisation, scheduling, and UI refinement. Sumeet ensures the deployed environment is stable.\n\n## April prep (parallel with SLM design + Sumeet's deployment work)\n\n* Identify personas (SPI-88)\n* Define test scenarios (SPI-89)\n* Prepare NDAs (SPI-92)\n* Start recruitment (SPI-93)\n* UI refinement based on known issues (SPI-51,… (truncated, use `get_issue` for full description)","priority":{"value":1,"name":"Urgent"},"url":"https://linear.app/spire-elijah/issue/SPI-87/user-testing-round-1-may-2026","gitBranchName":"sumeet/spi-87-user-testing-round-1-may-2026","createdAt":"2026-04-02T11:39:56.488Z","updatedAt":"2026-05-15T07:30:12.821Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":"2026-05-15T07:30:12.772Z","dueDate":"2026-06-16","slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Canceled","statusType":"canceled","labels":["Operational"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","assignee":"Patrick M","assigneeId":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-222","title":"Stress test Betty with 10 concurrent users","description":"Set up and run a stress test against Betty with 10 concurrent simulated users to validate system behavior under load.\n\n## Goals\n\n* Verify Betty handles 10 concurrent users without errors or degraded performance\n* Identify bottlenecks, resource limits, or race conditions under concurrent load\n* Measure response times, throughput, and error rates\n\n## Scope\n\n* Simulate 10 users hitting Betty concurrently with realistic usage patterns\n* Monitor reso… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-222/stress-test-betty-with-10-concurrent-users","gitBranchName":"sumeet/spi-222-stress-test-betty-with-10-concurrent-users","createdAt":"2026-04-29T06:56:14.943Z","updatedAt":"2026-04-29T06:56:14.943Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-94","title":"User testing week/day — execute sessions","description":"Run the testing sessions. For each session: brief the participant, have them sign NDA, walk through test scenarios, capture feedback via chosen mechanism, debrief. Assign roles: facilitator (guides session), note-taker (captures observations), tech support (handles environment issues).","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-94/user-testing-weekday-execute-sessions","gitBranchName":"sumeet/spi-94-user-testing-weekday-execute-sessions","createdAt":"2026-04-02T11:39:58.842Z","updatedAt":"2026-05-15T07:54:39.127Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":"2026-05-15T07:54:39.085Z","dueDate":"2026-05-24","slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Canceled","statusType":"canceled","labels":["Operational"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","assignee":"Patrick M","assigneeId":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-87","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-245","title":"Per-user LiteLLM budget caps with graceful job failure on exhaustion","description":"## Problem\n\nThere is no mechanism to limit how much LLM spend a given user can consume. A single user running a large batch job can exhaust the entire LiteLLM budget. If a budget is hit mid-run, LiteLLM returns a 429/402, the worker throws an unhandled error, and the job dies with no useful error message.\n\n## Goal\n\n1. **Configure per-user budget limits** in LiteLLM (virtual key `max_budget` per user).\n2. **Catch budget-exceeded errors** in the w… (truncated, use `get_issue` for full description)","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-245/per-user-litellm-budget-caps-with-graceful-job-failure-on-exhaustion","gitBranchName":"sumeet/spi-245-per-user-litellm-budget-caps-with-graceful-job-failure-on","createdAt":"2026-05-12T13:37:51.690Z","updatedAt":"2026-05-12T13:37:52.098Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-266","title":"Port FS8 analyst / review UI surface (graph explorer + question browsing)","description":"## What this is\n\nSurfaced during a coverage audit of the <issue id=\"c0ab7e61-8bb8-473a-a6df-ef53e108eaba\">SPI-238</issue> epic close-out. Row 7 of `docs/plans/audits/dev-sprint-to-dev-capability-diff-2026-05-11.md` lists FS8/FS9 UI surfaces as missing on dev. <issue id=\"ef48577a-a32c-4e1b-898a-7ab69b22ef50\">SPI-261</issue> covers a different UI surface (FS10 Operator Lab + FS12 pricing dashboards). FS8 is the **base graph explorer + question/que… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-266/port-fs8-analyst-review-ui-surface-graph-explorer-question-browsing","gitBranchName":"sumeet/spi-266-port-fs8-analyst-review-ui-surface-graph-explorer-question","createdAt":"2026-05-15T14:41:42.546Z","updatedAt":"2026-05-17T18:52:48.604Z","archivedAt":null,"completedAt":"2026-05-17T18:50:25.974Z","startedAt":"2026-05-17T17:12:44.557Z","canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","parentId":"SPI-238","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-246","title":"Add submitted_by to job records and filter GUI job list by current user","description":"## Problem\n\nJob records have no `submitted_by` field. Every user in the GUI sees every job from every other user with no way to filter to their own work.\n\n## Goal\n\n1. Persist `submitted_by` (the resolved `user_id`) on the job row at submission time.\n2. Expose it in `JobRequestContext` and `JobStatusResponse`.\n3. In the frontend job list, default to showing only the current user's jobs, with an admin toggle to show all.\n\n## Scope\n\n* Add `submitte… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-246/add-submitted-by-to-job-records-and-filter-gui-job-list-by-current","gitBranchName":"sumeet/spi-246-add-submitted_by-to-job-records-and-filter-gui-job-list-by","createdAt":"2026-05-12T13:37:56.302Z","updatedAt":"2026-05-12T13:37:58.264Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-160","title":"Production environment — deploy from main via GitHub Actions","description":"## Goal\n\n`git push` to `main` → production Elijah Cloud is updated and live within minutes, with no manual steps.\n\n## Architecture\n\n* **Branch:** `main`\n\n## Approach: self-hosted GitHub Actions runner on Betty\n\nA self-hosted runner registered to the Elijah repo, running as the `elijah` service account on Betty under `systemctl --user`. The deploy workflow builds, pushes to [ghcr.io](<http://ghcr.io>), then pulls and restarts on Betty.\n\n## Scope\n… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-160/production-environment-deploy-from-main-via-github-actions","gitBranchName":"sumeet/spi-160-production-environment-deploy-from-main-via-github-actions","createdAt":"2026-04-13T13:59:57.944Z","updatedAt":"2026-04-23T06:39:21.293Z","archivedAt":null,"completedAt":"2026-04-23T06:39:21.266Z","startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-182","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-276","title":"Bare `anthropic/claude-sonnet-4` call site missing `openrouter/` prefix","description":"## What this is\n\nBug surfaced during <issue id=\"83f5a84b-3ef4-4e2b-8dbb-4653c053ddd8\">SPI-272</issue> staging verification. Some code path constructs a LiteLLM call with `model=\"anthropic/claude-sonnet-4\"` instead of `model=\"openrouter/anthropic/claude-sonnet-4\"`. The proxy rejects it:\n\n```\nlitellm.BadRequestError: OpenrouterException - {\"error\":{\"message\":\"{'error': '/chat/completions: Invalid model name passed in model=anthropic/claude-sonnet-… (truncated, use `get_issue` for full description)","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-276/bare-anthropicclaude-sonnet-4-call-site-missing-openrouter-prefix","gitBranchName":"sumeet/spi-276-bare-anthropicclaude-sonnet-4-call-site-missing-openrouter","createdAt":"2026-05-17T22:17:33.241Z","updatedAt":"2026-05-17T22:37:50.831Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Backlog","statusType":"backlog","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-17","title":"API Authentication & Rate Limiting","description":"## Sprint: Sumeet Week 3 (Apr 20-25)\n\n## Assignee: Sumeet\n\nAPI auth via ELIJAH_API_KEY header. Rate limiting via slowapi. Exclude /api/health.\n\nDepends on: SPI-16","priority":{"value":1,"name":"Urgent"},"url":"https://linear.app/spire-elijah/issue/SPI-17/api-authentication-and-rate-limiting","gitBranchName":"sumeet/spi-17-api-authentication-rate-limiting","createdAt":"2026-03-30T07:30:36.791Z","updatedAt":"2026-04-16T14:00:25.166Z","archivedAt":null,"completedAt":"2026-04-16T14:00:25.153Z","startedAt":"2026-04-15T10:51:28.660Z","canceledAt":null,"dueDate":"2026-04-25","slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":["Security"],"createdBy":"Patrick M","createdById":"22e1d1a4-9bb0-42b2-ab68-48b36ed00c4a","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-185","title":"Track domain provisioning by incubator","description":"## Status: Blocked — external dependency\n\nThe incubator is provisioning the production domain for Elijah Cloud. This ticket exists to track that external dependency and unblock the Cloudflare Tunnel + SSO work once the domain is available on Cloudflare DNS.\n\n## What we need from them\n\n* A registered domain (or subdomain) added to a Cloudflare account we have access to\n* DNS management access (to create CNAME → tunnel)\n* Confirmation of the exact… (truncated, use `get_issue` for full description)","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/spire-elijah/issue/SPI-185/track-domain-provisioning-by-incubator","gitBranchName":"sumeet/spi-185-track-domain-provisioning-by-incubator","createdAt":"2026-04-16T15:15:40.908Z","updatedAt":"2026-04-23T10:54:26.291Z","archivedAt":null,"completedAt":"2026-04-23T10:54:26.277Z","startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":[],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","project":"Elijah Pipeline Development","projectId":"cf9fb1a1-0344-45e5-933a-a689a00d3858","parentId":"SPI-182","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"},{"id":"SPI-209","title":"Env var cleanup — single .env pattern, remove env_file duplication","description":"## Goal\n\nStandardise environment variable handling across all compose files. Currently there are multiple env files with different names, a confusing dual-mechanism (`env_file:` vs `environment:` vs `--env-file`), and duplicated var listings. Clean this up before tackling automated deployment (<issue id=\"19c927fc-bb3f-47db-b3f8-daaa039c3211\">SPI-196</issue>, <issue id=\"23605b28-fdf6-44e5-ba87-7ff55694b3d4\">SPI-160</issue>).\n\n## Current state\n\n##… (truncated, use `get_issue` for full description)","priority":{"value":2,"name":"High"},"url":"https://linear.app/spire-elijah/issue/SPI-209/env-var-cleanup-single-env-pattern-remove-env-file-duplication","gitBranchName":"sumeet/spi-209-env-var-cleanup-single-env-pattern-remove-env_file","createdAt":"2026-04-22T15:48:13.369Z","updatedAt":"2026-04-22T18:03:49.883Z","archivedAt":null,"completedAt":"2026-04-22T18:03:49.872Z","startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":["Infrastructure"],"createdBy":"sumeet@sumeetsaini.com","createdById":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","assignee":"sumeet@sumeetsaini.com","assigneeId":"c7a8f74f-a7ba-41e8-b771-85fc97b42216","parentId":"SPI-182","team":"Spire_Elijah","teamId":"6fc98d18-8a80-4c49-8c42-a6e2a4d3d722"}],"hasNextPage":true,"cursor":"6b00e99b-ef34-4bd2-b624-4fc9bbf6ff17"}
```

> AGENT

Looked at PR #237 (the `docs/plans/demo-2026-05-25.md` plan) and pulled the related Linear tickets. Quick read:

**PR #237** is the 11-task demo-readiness plan for Mon 25 May. Currently nothing in there about per-user accounts / private runs / spend controls — only a passing mention of CF Access (which is already done in SPI-182). You want me to add a task (or task block) covering "login → private runs for that user → controls".

**Related tickets already in Linear** (all `Spire_Elijah` / Elijah Pipeline Development, all assigned to you, all Backlog except where noted):

The realistic-by-demo chain (built on the `UserRegistry` foundation already landed in SPI-236):
- **SPI-242** — Explore CF ZT → per-user Elijah identity bridging *(Low, spike)*
- **SPI-243** — Bridge CF ZT email to per-user Elijah identity for GUI users *(High)* — the **login → per-user identity** piece
- **SPI-244** — Pass `user_id` to LiteLLM on every call for per-user spend tracking *(High)*
- **SPI-245** — Per-user LiteLLM budget caps with graceful job failure on exhaustion *(High)* — the **controls** piece
- **SPI-246** — Add `submitted_by` to job records and filter GUI job list by current user *(Medium)* — the **private runs for that user** piece
- **SPI-247** — Remove shared `ELIJAH_API_KEY` fallback once per-user identity lands *(Medium, cleanup)*

The heavier parent items, almost certainly **not** demo-week scope:
- **SPI-176** — Phase 2 Auth: user accounts + JWT sessions + RBAC *(Backlog)*
- **SPI-177** — Phase 3 Auth: spend controls + budgets + audit trail *(Backlog, parent of SPI-99/189/244/245)*

My recommendation before I touch the PR: the realistic ship for Mon 25 May is the CF-ZT-bridge chain (**SPI-243 → SPI-246 → SPI-244 → SPI-245**, with SPI-247 as cleanup after). That's "login → private runs → cost controls" using infra that already exists (CF ZT email header + `UserRegistry`). Full SPI-176 JWT/RBAC is a multi-week piece — I wouldn't put it on the demo plan.

Two questions before I edit the plan:

> TOOL

tool_use AskUserQuestion
id: toolu_01XumJbfv4f5ZXMiQNLara5S
```json
{
  "questions": [
    {
      "question": "What scope should the new plan task cover?",
      "header": "Scope",
      "multiSelect": false,
      "options": [
        {
          "label": "CF-ZT bridge chain only",
          "description": "SPI-243 (identity) + SPI-246 (private job list) + SPI-244 (LiteLLM user_id) + SPI-245 (budget caps). Realistic to ship before Fri 22 May deploy. Uses existing UserRegistry + CF ZT header. No JWT, no RBAC, no signup UI."
        },
        {
          "label": "Bridge chain + SPI-247 cleanup",
          "description": "Same as above plus remove the shared ELIJAH_API_KEY fallback once every caller has a real identity. Slightly more risk because it touches every API entrypoint."
        },
        {
          "label": "Full SPI-176 Phase 2 Auth",
          "description": "User accounts + JWT sessions + RBAC. This is a multi-week build; including it on the demo plan as a ship item is almost certainly unrealistic. Pick this only if you actually want it as a demo-week stretch goal."
        }
      ]
    },
    {
      "question": "How should it slot into the existing plan?",
      "header": "Placement",
      "multiSelect": false,
      "options": [
        {
          "label": "New top-level task #11",
          "description": "Add as task #11 'Per-user identity, private runs, and spend caps' after the existing 1–10. Owner Sumeet. Target Fri 22 May (lands with the deploy). Each sub-piece links to its SPI ticket."
        },
        {
          "label": "Add to 'Parallel work in flight' table",
          "description": "Treat it like the vLLM port — a Sumeet parallel workstream rather than a numbered plan task. Lower visibility but matches how the vLLM work is currently represented."
        },
        {
          "label": "Add as a 'Standing blockers' row",
          "description": "Drop one row per SPI ticket into the existing 'Standing blockers also targeted before demo' table at the bottom. Lowest-friction edit; doesn't restructure the 11-task spine."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01XumJbfv4f5ZXMiQNLara5S
```
User has answered your questions: "What scope should the new plan task cover?"="I'm not really sure all I want is that the user is pre apprived in the cloudflare, then they can access their own elijah dashboard and finally theny have their won runs and some limits on what they can do for example", "How should it slot into the existing plan?"="New top-level task #11". You can now continue with the user's answers in mind.
```

> AGENT

Got it. Your description maps exactly onto the CF-ZT bridge chain:

- "Pre-approved in Cloudflare" → already done (SPI-186/187)
- "Access their own dashboard" → **SPI-243** (CF ZT email → per-user identity)
- "Their own runs" → **SPI-246** (`submitted_by` on jobs + GUI filter)
- "Limits on what they can do" → **SPI-244** (`user_id` to LiteLLM) + **SPI-245** (per-user budget caps)

One thing to flag before I write anything to the PR: **#237 is Paddy's branch**, and per CLAUDE.md I shouldn't push to someone else's PR branch without explicit say-so. So I'd suggest one of these:

1. I draft the new Task #11 markdown here, you paste it into a PR review comment asking Paddy to add it.
2. I check out Paddy's branch and push the edit directly (needs your OK since it's not your branch).
3. You merge #237 as-is and we open a follow-up PR that adds Task #11.

Below is the draft regardless — drop-in ready for the file:

---

```markdown
### 11. Per-user identity, private runs, and spend caps (Sumeet)
- **Owner**: Sumeet
- **Target**: Fri 22 May (lands before #7 deploy)
- **Status**: ☐ Open
- **Depends on**: Cloudflare Access already gates the hostname ([SPI-186](https://linear.app/spire-elijah/issue/SPI-186), [SPI-187](https://linear.app/spire-elijah/issue/SPI-187)); `UserRegistry` foundation already in API ([SPI-236](https://linear.app/spire-elijah/issue/SPI-236))
- **Scope**: Each pre-approved CF Access user gets a real Elijah identity at the API layer, sees only their own runs in the dashboard, and is bounded by a per-user LLM spend cap. No JWT, no signup UI, no RBAC — that's deferred to [SPI-176](https://linear.app/spire-elijah/issue/SPI-176) post-demo.
- **Constituent tickets** (ship in this order):
  - [SPI-243](https://linear.app/spire-elijah/issue/SPI-243) — Bridge CF ZT email (`Cf-Access-Authenticated-User-Email` header) to per-user Elijah identity. Resolves `request.state.user` for every GUI request. **High**.
  - [SPI-246](https://linear.app/spire-elijah/issue/SPI-246) — Persist `submitted_by` on job records; default the GUI job list to current user, admin toggle for all. **Medium**.
  - [SPI-244](https://linear.app/spire-elijah/issue/SPI-244) — Thread `user_id` into every LiteLLM call so spend rolls up per user. **High**.
  - [SPI-245](https://linear.app/spire-elijah/issue/SPI-245) — Configure LiteLLM per-user `max_budget`; catch 429/402 in workers and fail the job with a clear user-facing error. **High**.
- **Definition of done**:
  - A pre-approved CF Access user can log in and reach the Elijah dashboard with their own email as identity.
  - The job list on demo.elijahintelligence.com shows only that user's runs by default.
  - LiteLLM dashboard shows spend broken down per user across the demo cohort.
  - A user who hits their cap mid-run sees a clear "budget exhausted" error in the GUI rather than a stack trace.
- **Out of scope (deliberately)**: JWT sessions, signup flows, RBAC, audit trail UI ([SPI-176](https://linear.app/spire-elijah/issue/SPI-176), [SPI-177](https://linear.app/spire-elijah/issue/SPI-177)); removing the shared `ELIJAH_API_KEY` fallback ([SPI-247](https://linear.app/spire-elijah/issue/SPI-247) — cleanup, lands after demo once every caller is on the new path).
```

And the corresponding timeline-table row update:

```markdown
| Mon | 18 May | … (existing) … ; **SPI-243 scoping kickoff** |
| Tue | 19 May | … (existing) … ; **SPI-243 lands** |
| Wed | 20 May | … (existing) … ; **SPI-246 + SPI-244 land** |
| Thu | 21 May | … (existing) … ; **SPI-245 lands; per-user budgets live** |
| Fri | 22 May | Deploy (#7) — tuned surfaces **+ per-user identity stack** live on demo |
```

Want me to (1) save this somewhere you can paste from, (2) check out Paddy's branch and commit the edit (need your OK), or (3) open a follow-up PR?

> DEVELOPER

yeah you can push to that branch by checking out

> TOOL

tool_use Bash
id: toolu_01Ff24ozgv36GqMpm2YAXZ2B
```json
{
  "command": "gh pr view 237 --repo elijahintelligence/elijah --json headRefName,headRepository,headRepositoryOwner,baseRefName",
  "description": "Get PR #237 branch info"
}
```

> TOOL

tool_result
id: toolu_01Ff24ozgv36GqMpm2YAXZ2B
```
{"baseRefName":"dev","headRefName":"paddy/demo-readiness-2026-05-25","headRepository":{"id":"R_kgDORNNGGg","name":"elijah","nameWithOwner":"elijahintelligence/elijah"},"headRepositoryOwner":{"id":"O_kgDOEJeW0w","login":"elijahintelligence"}}
```

> TOOL

tool_use Bash
id: toolu_018qwsh1VkdDeof5m9BQRAjr
```json
{
  "command": "ls /Users/sumeet/matrix/elijah/.git 2>&1 | head -5 && echo \"---\" && git -C /Users/sumeet/matrix/elijah branch --show-current 2>&1",
  "description": "Check main repo state"
}
```

> TOOL

tool_result
id: toolu_018qwsh1VkdDeof5m9BQRAjr
```
COMMIT_EDITMSG
FETCH_HEAD
HEAD
ORIG_HEAD
config
---
port/spi-230-pr1-core-stores
```

> TOOL

tool_use Bash
id: toolu_014hMDLoHawwgoEkm5P3WtSb
```json
{
  "command": "cd /Users/sumeet/matrix/elijah && git fetch origin paddy/demo-readiness-2026-05-25 && git worktree add /tmp/pr237-demo-plan paddy/demo-readiness-2026-05-25 2>&1",
  "description": "Fetch branch and create temp worktree"
}
```

> TOOL

tool_result
id: toolu_014hMDLoHawwgoEkm5P3WtSb
```
From github.com:elijahintelligence/elijah
 * branch            paddy/demo-readiness-2026-05-25 -> FETCH_HEAD
 * [new branch]      paddy/demo-readiness-2026-05-25 -> origin/paddy/demo-readiness-2026-05-25
Preparing worktree (new branch 'paddy/demo-readiness-2026-05-25')
branch 'paddy/demo-readiness-2026-05-25' set up to track 'origin/paddy/demo-readiness-2026-05-25'.
Updating files:  16% (224/1339)Updating files:  17% (228/1339)Updating files:  18% (242/1339)Updating files:  19% (255/1339)Updating files:  20% (268/1339)Updating files:  21% (282/1339)Updating files:  22% (295/1339)Updating files:  23% (308/1339)Updating files:  24% (322/1339)Updating files:  25% (335/1339)Updating files:  26% (349/1339)Updating files:  26% (357/1339)Updating files:  27% (362/1339)Updating files:  28% (375/1339)Updating files:  29% (389/1339)Updating files:  30% (402/1339)Updating files:  31% (416/1339)Updating files:  32% (429/1339)Updating files:  33% (442/1339)Updating files:  34% (456/1339)Updating files:  35% (469/1339)Updating files:  35% (482/1339)Updating files:  36% (483/1339)Updating files:  37% (496/1339)Updating files:  38% (509/1339)Updating files:  39% (523/1339)Updating files:  40% (536/1339)Updating files:  41% (549/1339)Updating files:  42% (563/1339)Updating files:  43% (576/1339)Updating files:  43% (589/1339)Updating files:  44% (590/1339)Updating files:  45% (603/1339)Updating files:  46% (616/1339)Updating files:  47% (630/1339)Updating files:  48% (643/1339)Updating files:  49% (657/1339)Updating files:  50% (670/1339)Updating files:  51% (683/1339)Updating files:  52% (697/1339)Updating files:  53% (710/1339)Updating files:  54% (724/1339)Updating files:  55% (737/1339)Updating files:  56% (750/1339)Updating files:  57% (764/1339)Updating files:  58% (777/1339)Updating files:  59% (791/1339)Updating files:  60% (804/1339)Updating files:  61% (817/1339)Updating files:  62% (831/1339)Updating files:  63% (844/1339)Updating files:  64% (857/1339)Updating files:  65% (871/1339)Updating files:  66% (884/1339)Updating files:  67% (898/1339)Updating files:  68% (911/1339)Updating files:  69% (924/1339)Updating files:  70% (938/1339)Updating files:  71% (951/1339)Updating files:  72% (965/1339)Updating files:  73% (978/1339)Updating files:  74% (991/1339)Updating files:  75% (1005/1339)Updating files:  76% (1018/1339)Updating files:  77% (1032/1339)Updating files:  78% (1045/1339)Updating files:  79% (1058/1339)Updating files:  80% (1072/1339)Updating files:  81% (1085/1339)Updating files:  82% (1098/1339)Updating files:  83% (1112/1339)Updating files:  84% (1125/1339)Updating files:  85% (1139/1339)Updating files:  86% (1152/1339)Updating files:  87% (1165/1339)Updating files:  88% (1179/1339)Updating files:  89% (1192/1339)Updating files:  90% (1206/1339)Updating files:  91% (1219/1339)Updating files:  92% (1232/1339)Updating files:  93% (1246/1339)Updating files:  94% (1259/1339)Updating files:  95% (1273/1339)Updating files:  96% (1286/1339)Updating files:  97% (1299/1339)Updating files:  98% (1313/1339)Updating files:  99% (1326/1339)Updating files: 100% (1339/1339)Updating files: 100% (1339/1339), done.
HEAD is now at 9c5e72c Add demo-readiness plan for Mon 25 May 2026
Shell cwd was reset to /Users/sumeet/matrix/elijah/.claude/worktrees/229
```

> TOOL

tool_use Read
id: toolu_015CfXxbfgL79nnJTCd2aWS4
```json
{
  "file_path": "/tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md"
}
```

> TOOL

tool_result
id: toolu_015CfXxbfgL79nnJTCd2aWS4
```
1	# Demo readiness — Mon 25 May 2026
2	
3	**Goal**: Elijah ready to demo on Monday 25 May 2026.
4	**Friday checkpoint**: deploy + end-to-end testing & review on Friday 22 May (Paddy, Sumeet, Tom, Rich). Bug-fix budget is **Saturday only**.
5	**Hard rules**: Sunday is off-limits for work. Saturday is the only bug-fix day, so anything not fixed by Saturday evening is either deferred or gets cut from the demo script.
6	**Replaces**: the cancelled [SPI-87 — User Testing Round 1](https://linear.app/spire-elijah/issue/SPI-87) umbrella. Will be promoted to a Linear umbrella ticket once the workspace is upgraded; until then this file is the source of truth.
7	
8	## Timeline at a glance
9	
10	| Day | Date | Focus |
11	|---|---|---|
12	| Mon | 18 May | Wireframe → Sumeet input + mutual sign-off; Sumeet ports vLLM in parallel; Operator Lab functional; **individual-surface tuning by COP**; FS4 / FS5 PR review starts |
13	| Tue | 19 May | Wireframe stage-1 / stage-2 breakdown (Paddy, Sumeet review); **surface-family / group tuning by COP** |
14	| Wed | 20 May | **Full-system tuning run #1** |
15	| Thu | 21 May | **Full-system tuning run #2**; FS4 / FS5 PRs landed |
16	| Fri | 22 May | Deploy tuned surfaces to main (Sumeet) → testing & review (Paddy, Sumeet, Tom, Rich) |
17	| Sat | 23 May | **Bug-fix day** (the only one) |
18	| Sun | 24 May | **No work** |
19	| Mon | 25 May | **Demo** |
20	
21	## Tasks
22	
23	### 1. Land the new UI wireframe (Sumeet input + mutual sign-off)
24	- **Owners**: Paddy (drives) + Sumeet (review)
25	- **Target**: Mon 18 May EOD
26	- **Status**: ☐ Open
27	- **Scope**: Wireframe design is essentially complete. This task is the **last mile** — Sumeet reviews the current artifact, surfaces any blocking concerns, both sign off. No fresh design work.
28	- **Definition of done**: Wireframe under `docs/wireframes/workspace-router/` agreed by Paddy and Sumeet (a one-line ack in the PR or a Linear comment is enough). Hands off to #2.
29	
30	### 2. Break the wireframe into "stage 1" and "stage 2" releases
31	- **Owner**: Paddy (Sumeet review)
32	- **Target**: Tue 19 May EOD
33	- **Status**: ☐ Open
34	- **Depends on**: #1
35	- **Definition of done**: Stage-1 (Monday-demo) vs stage-2 (post-demo) split documented inline in the wireframe folder or this file. Sumeet has signed off.
36	
37	### 3. Get Operator Lab functional for surface tuning
38	- **Owner**: Paddy
39	- **Target**: Mon 18 May EOD (prerequisite for #4 the same day)
40	- **Status**: ☐ Open
41	- **Definition of done**: Each tuning surface in the Operator Lab can be selected, calibrated, and promoted without manual DB / CLI intervention. Smoke-tested against the local stack.
42	
43	### 4. Tune all surfaces individually
44	- **Owner**: Paddy
45	- **Target**: **Mon 18 May COP**
46	- **Status**: ☐ Open
47	- **Depends on**: #3
48	- **Definition of done**: Every implemented tuning surface has a promoted candidate (FS1 question drafter, FS2 boosts × 4, FS2 coverage planner + gap reroute, FS2B iw_verdict, FS3 chain steps × 6 + admission gate, FS4 Fermi chain × 6 LLM + calibration head, FS5 edge Fermi chain × 5 LLM + multiplier head).
49	
50	### 5. Tune all surface families / groups
51	- **Owner**: Paddy
52	- **Target**: **Tue 19 May COP**
53	- **Status**: ☐ Open
54	- **Depends on**: #4
55	- **Definition of done**: Each surface family / chain (FS2A query-boost lane, FS2B coverage, FS3 driver→indicator→admission chain, FS4 Fermi chain, FS5 edge Fermi chain) is jointly tuned and the family-level candidate promoted.
56	
57	### 6. Full-system tuning runs
58	- **Owner**: Paddy
59	- **Targets**: Run #1 — Wed 20 May; Run #2 — Thu 21 May
60	- **Status**: ☐ Open
61	- **Depends on**: #5
62	- **Definition of done**: Two full-system tune runs executed. Final whole-model candidate beats the pre-tune baseline on the held-out replay window. Result snapshot + Brier comparison captured before handoff to #7.
63	
64	### 7. Deploy tuned surfaces to main
65	- **Owner**: Sumeet
66	- **Target**: Fri 22 May (before #9 testing session)
67	- **Status**: ☐ Open
68	- **Depends on**: #6
69	- **Definition of done**: Tuned candidates promoted on prod and reachable from the demo environment. Smoke-check that `demo.elijahintelligence.com` serves the tuned model.
70	
71	### 8a. Review FS4 PRs
72	- **Owner**: Paddy first pass; Sumeet review once green
73	- **Target**: Thu 21 May
74	- **Status**: ☐ Open
75	- **Definition of done**: All open FS4-related PRs reviewed, addressed, and merged.
76	
77	### 8b. Review FS5 PRs
78	- **Owner**: Paddy first pass; Sumeet review once green
79	- **Target**: Thu 21 May
80	- **Status**: ☐ Open
81	- **Definition of done**: All open FS5-related PRs (including the FS5 edge Fermi chain stack) reviewed, addressed, and merged.
82	
83	### 9. Final demo testing and review
84	- **Attendees**: Paddy, Sumeet, Tom, Rich
85	- **When**: Fri 22 May (post #7 deploy)
86	- **Status**: ☐ Scheduled (calendar invite TBD — Paddy to send)
87	- **Depends on**: #1–#8 landed; #7 deployed
88	- **Outputs**: prioritised bug + polish list feeding #10. Notes captured here or in a child doc.
89	
90	### 10. Fix Friday-testing bugs (Saturday only)
91	- **Owner**: Paddy (Sumeet support if infra)
92	- **Target**: **Sat 23 May only** (Sunday is off; no fallback day)
93	- **Status**: ☐ Open
94	- **Depends on**: #9
95	- **Definition of done**: All blocker-tier bugs from the Friday session closed by Saturday evening. Anything not fixed is explicitly deferred and noted in the demo script.
96	
97	## Parallel work in flight today
98	
99	| Item | Owner | Notes |
100	|---|---|---|
101	| Port vLLM to `dev` | Sumeet | Running in parallel with the plan above today (Mon 18 May). Related: PR #229 (local-SLM tier mapping for `qwen2.5-14b-instruct-awq`) opened by Paddy this morning and waiting on review. Sumeet's port may want to land that first. |
102	
103	## Standing blockers also targeted before demo
104	
105	These existed before this plan; they're not in the 11-step list but block the same Monday demo.
106	
107	| Ticket | Title | Owner | Status |
108	|---|---|---|---|
109	| [SPI-224](https://linear.app/spire-elijah/issue/SPI-224) | arXiv 429 blocks all evidence retrieval | Paddy | Urgent, Backlog (just reassigned) |
110	| [SPI-272](https://linear.app/spire-elijah/issue/SPI-272) | Staging verification of the SPI-238 porting epic | Sumeet | High, In Progress |
111	| [SPI-273](https://linear.app/spire-elijah/issue/SPI-273) | Add litellm-seed to staging/prod compose + per-env `LLM_MODEL_SET` | Sumeet | Urgent, In Progress |
112	| [SPI-274](https://linear.app/spire-elijah/issue/SPI-274) | Port Anthropic Claude model-family refresh | Sumeet | Urgent, In Progress |
113	| [SPI-275](https://linear.app/spire-elijah/issue/SPI-275) | `gpt-5.2` alias rejected by OpenRouter | Sumeet | High, Backlog |
114	
115	## Migration to Linear
116	
117	When the Linear workspace is upgraded (currently capped on the free tier), promote this file as follows:
118	
119	1. Create umbrella issue **"Demo readiness — Mon 25 May 2026"** in `Spire_Elijah` / `Elijah Pipeline Development`. Assignee Paddy, priority Urgent, due `2026-05-25`. Copy this file's "Goal" / "Friday checkpoint" / "Plan" sections into the description.
120	2. Create one child per task above (1, 2, 3, 4, 5, 6, 7, 8a, 8b, 9, 10) with the listed owner / target / definition of done.
121	3. Link the standing blockers (SPI-224 / SPI-272 / SPI-273 / SPI-274 / SPI-275) as `relatedTo` on the umbrella.
122	4. Keep this markdown file as the source of truth for status until the migration; archive it once Linear is canonical.
123	
```

> TOOL

tool_use Edit
id: toolu_012wYoQ8V3CMBBqWnRt9YWkc
```json
{
  "replace_all": false,
  "file_path": "/tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md",
  "old_string": "| Mon | 18 May | Wireframe → Sumeet input + mutual sign-off; Sumeet ports vLLM in parallel; Operator Lab functional; **individual-surface tuning by COP**; FS4 / FS5 PR review starts |\n| Tue | 19 May | Wireframe stage-1 / stage-2 breakdown (Paddy, Sumeet review); **surface-family / group tuning by COP** |\n| Wed | 20 May | **Full-system tuning run #1** |\n| Thu | 21 May | **Full-system tuning run #2**; FS4 / FS5 PRs landed |\n| Fri | 22 May | Deploy tuned surfaces to main (Sumeet) → testing & review (Paddy, Sumeet, Tom, Rich) |",
  "new_string": "| Mon | 18 May | Wireframe → Sumeet input + mutual sign-off; Sumeet ports vLLM in parallel; Operator Lab functional; **individual-surface tuning by COP**; FS4 / FS5 PR review starts; **per-user identity stack kickoff (SPI-243)** |\n| Tue | 19 May | Wireframe stage-1 / stage-2 breakdown (Paddy, Sumeet review); **surface-family / group tuning by COP**; **SPI-243 lands** |\n| Wed | 20 May | **Full-system tuning run #1**; **SPI-246 + SPI-244 land** |\n| Thu | 21 May | **Full-system tuning run #2**; FS4 / FS5 PRs landed; **SPI-245 lands — per-user budgets live** |\n| Fri | 22 May | Deploy tuned surfaces to main (Sumeet) **+ per-user identity stack live on demo** → testing & review (Paddy, Sumeet, Tom, Rich) |"
}
```

> TOOL

tool_result
id: toolu_012wYoQ8V3CMBBqWnRt9YWkc
```
The file /tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_015a7AkshSeVupk3Frsth8Ld
```json
{
  "replace_all": false,
  "file_path": "/tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md",
  "old_string": "### 10. Fix Friday-testing bugs (Saturday only)\n- **Owner**: Paddy (Sumeet support if infra)\n- **Target**: **Sat 23 May only** (Sunday is off; no fallback day)\n- **Status**: ☐ Open\n- **Depends on**: #9\n- **Definition of done**: All blocker-tier bugs from the Friday session closed by Saturday evening. Anything not fixed is explicitly deferred and noted in the demo script.\n\n## Parallel work in flight today",
  "new_string": "### 10. Fix Friday-testing bugs (Saturday only)\n- **Owner**: Paddy (Sumeet support if infra)\n- **Target**: **Sat 23 May only** (Sunday is off; no fallback day)\n- **Status**: ☐ Open\n- **Depends on**: #9\n- **Definition of done**: All blocker-tier bugs from the Friday session closed by Saturday evening. Anything not fixed is explicitly deferred and noted in the demo script.\n\n### 11. Per-user identity, private runs, and spend caps\n- **Owner**: Sumeet\n- **Target**: Thu 21 May EOD (so it can ride the Fri 22 May deploy in #7)\n- **Status**: ☐ Open\n- **Depends on**: Cloudflare Access already gates the hostname ([SPI-186](https://linear.app/spire-elijah/issue/SPI-186), [SPI-187](https://linear.app/spire-elijah/issue/SPI-187)); `UserRegistry` foundation already in API ([SPI-236](https://linear.app/spire-elijah/issue/SPI-236))\n- **Scope**: Each pre-approved Cloudflare Access user gets a real Elijah identity at the API layer, sees only their own runs in the dashboard, and is bounded by a per-user LLM spend cap. No JWT, no signup UI, no RBAC — those are deferred to [SPI-176](https://linear.app/spire-elijah/issue/SPI-176) post-demo.\n- **Constituent tickets** (ship in this order):\n  - [SPI-243](https://linear.app/spire-elijah/issue/SPI-243) — Bridge the CF ZT `Cf-Access-Authenticated-User-Email` header to per-user Elijah identity. Resolves `request.state.user` for every GUI request. **High**. Target Tue 19 May.\n  - [SPI-246](https://linear.app/spire-elijah/issue/SPI-246) — Persist `submitted_by` on job records; default the GUI job list to current user, admin toggle for all. **Medium**. Target Wed 20 May.\n  - [SPI-244](https://linear.app/spire-elijah/issue/SPI-244) — Thread `user_id` into every LiteLLM call so spend rolls up per user. **High**. Target Wed 20 May.\n  - [SPI-245](https://linear.app/spire-elijah/issue/SPI-245) — Configure LiteLLM per-user `max_budget`; catch 429 / 402 in workers and fail the job with a clear user-facing error. **High**. Target Thu 21 May.\n- **Definition of done**:\n  - A pre-approved CF Access user can log in and reach the Elijah dashboard with their own email as identity.\n  - The job list on `demo.elijahintelligence.com` shows only that user's runs by default.\n  - LiteLLM dashboard shows spend broken down per user across the demo cohort.\n  - A user who hits their cap mid-run sees a clear \"budget exhausted\" error in the GUI rather than a stack trace.\n- **Out of scope (deliberately)**: JWT sessions, signup flows, RBAC, audit-trail UI ([SPI-176](https://linear.app/spire-elijah/issue/SPI-176), [SPI-177](https://linear.app/spire-elijah/issue/SPI-177)); removing the shared `ELIJAH_API_KEY` fallback ([SPI-247](https://linear.app/spire-elijah/issue/SPI-247) — cleanup, lands after demo once every caller is on the new path).\n\n## Parallel work in flight today"
}
```

> TOOL

tool_result
id: toolu_015a7AkshSeVupk3Frsth8Ld
```
The file /tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01AZoegZZ6gHmjjMweTfd41b
```json
{
  "replace_all": false,
  "file_path": "/tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md",
  "old_string": "These existed before this plan; they're not in the 11-step list but block the same Monday demo.",
  "new_string": "These existed before this plan; they're not in the numbered task list but block the same Monday demo."
}
```

> TOOL

tool_result
id: toolu_01AZoegZZ6gHmjjMweTfd41b
```
The file /tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01GzpebwKkvfd3vBWv22UDHV
```json
{
  "replace_all": false,
  "file_path": "/tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md",
  "old_string": "2. Create one child per task above (1, 2, 3, 4, 5, 6, 7, 8a, 8b, 9, 10) with the listed owner / target / definition of done.",
  "new_string": "2. Create one child per task above (1, 2, 3, 4, 5, 6, 7, 8a, 8b, 9, 10, 11) with the listed owner / target / definition of done. Task 11 already maps to existing Linear tickets — link those (SPI-243, SPI-244, SPI-245, SPI-246) as children of the umbrella rather than re-creating them."
}
```

> TOOL

tool_result
id: toolu_01GzpebwKkvfd3vBWv22UDHV
```
The file /tmp/pr237-demo-plan/docs/plans/demo-2026-05-25.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now commit and push.

> TOOL

tool_use Bash
id: toolu_01QizTfE7KB3ze4ag5JFhN1D
```json
{
  "command": "cd /tmp/pr237-demo-plan && git status && echo \"---\" && git diff --stat",
  "description": "Check status and diff stats"
}
```

> TOOL

tool_result
id: toolu_01QizTfE7KB3ze4ag5JFhN1D
```
On branch paddy/demo-readiness-2026-05-25
Your branch is up to date with 'origin/paddy/demo-readiness-2026-05-25'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   docs/plans/demo-2026-05-25.md

no changes added to commit (use "git add" and/or "git commit -a")
---
 docs/plans/demo-2026-05-25.md | 32 +++++++++++++++++++++++++-------
 1 file changed, 25 insertions(+), 7 deletions(-)
Shell cwd was reset to /Users/sumeet/matrix/elijah/.claude/worktrees/229
```

> TOOL

tool_use Bash
id: toolu_016SYz75mwLEfak1AZEaXK32
```json
{
  "command": "cd /tmp/pr237-demo-plan && git add docs/plans/demo-2026-05-25.md && git commit -m \"$(cat <<'EOF'\nAdd Task #11: per-user identity, private runs, and spend caps\n\nDemo cohort needs a real per-user experience: log in via CF Access,\nsee only your own runs, get bounded by a spend cap. Maps to the\nexisting CF-ZT bridge chain in Linear (SPI-243, SPI-246, SPI-244,\nSPI-245) — no new tickets required. JWT / RBAC / signup deferred to\nSPI-176 post-demo.\n\nAlso updates the day-by-day timeline so the four constituent tickets\nland Tue–Thu and ride the Fri 22 May deploy, and updates the\n\"Migration to Linear\" recipe so Task 11 reuses the existing tickets\ninstead of duplicating them.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\nEOF\n)\" && git push origin paddy/demo-readiness-2026-05-25",
  "description": "Commit and push Task #11 addition"
}
```

> TOOL

tool_result
id: toolu_016SYz75mwLEfak1AZEaXK32
```
ruff (legacy alias)..................................(no files to check)Skipped
ruff format..........................................(no files to check)Skipped
mypy.................................................(no files to check)Skipped
Detect hardcoded secrets.................................................Passed
[paddy/demo-readiness-2026-05-25 bcfb883] Add Task #11: per-user identity, private runs, and spend caps
 1 file changed, 25 insertions(+), 7 deletions(-)
To github.com:elijahintelligence/elijah.git
   9c5e72c..bcfb883  paddy/demo-readiness-2026-05-25 -> paddy/demo-readiness-2026-05-25
Shell cwd was reset to /Users/sumeet/matrix/elijah/.claude/worktrees/229
```

> TOOL

tool_use Bash
id: toolu_01NKREBZxmjNuL2ZzX6e8zRg
```json
{
  "command": "cd /Users/sumeet/matrix/elijah && git worktree remove /tmp/pr237-demo-plan",
  "description": "Clean up temp worktree"
}
```

> TOOL

tool_result
id: toolu_01NKREBZxmjNuL2ZzX6e8zRg
```
Shell cwd was reset to /Users/sumeet/matrix/elijah/.claude/worktrees/229
```

> AGENT

Pushed as `bcfb883` on `paddy/demo-readiness-2026-05-25`. PR #237 now shows Task #11 added to the plan, with the four constituent tickets (SPI-243 → SPI-246 → SPI-244 → SPI-245) sequenced Tue–Thu so they ride Friday's deploy, plus updates to the timeline table and the "Migration to Linear" recipe so Task 11 reuses the existing Linear tickets instead of duplicating them. Temp worktree cleaned up; your `port/spi-230-pr3b-tuning-machinery` worktree was untouched.

PR: https://github.com/elijahintelligence/elijah/pull/237

> DEVELOPER

what exactly did you change

> AGENT

Three edits to `docs/plans/demo-2026-05-25.md` (commit `bcfb883`):

**1. Timeline-at-a-glance table** — appended a per-user-identity beat to each weekday row Mon–Fri:
- Mon 18 May: `+ per-user identity stack kickoff (SPI-243)`
- Tue 19 May: `+ SPI-243 lands`
- Wed 20 May: `+ SPI-246 + SPI-244 land`
- Thu 21 May: `+ SPI-245 lands — per-user budgets live`
- Fri 22 May: deploy line now reads `Deploy tuned surfaces to main (Sumeet) + per-user identity stack live on demo → testing & review …`

**2. New Task #11** inserted between Task #10 and the "Parallel work in flight today" section:

> ### 11. Per-user identity, private runs, and spend caps
> - Owner: Sumeet
> - Target: Thu 21 May EOD (rides the Fri 22 May deploy in #7)
> - Depends on: SPI-186/187 (CF Access already gates the host), SPI-236 (UserRegistry foundation already in API)
> - Scope: pre-approved CF Access user → real Elijah identity at API → sees only own runs → bounded by per-user spend cap. No JWT, no signup UI, no RBAC (deferred to SPI-176).
> - Constituent tickets with per-day targets: SPI-243 (Tue), SPI-246 (Wed), SPI-244 (Wed), SPI-245 (Thu).
> - Definition of done: 4 bullets — login works, job list filters to current user, LiteLLM shows per-user spend, budget exhaustion shows a clean GUI error.
> - Out of scope: SPI-176 (JWT/RBAC), SPI-177 (audit-trail UI), SPI-247 (shared key fallback removal — cleanup after demo).

**3. Two small consistency fixups elsewhere in the file:**
- The "Standing blockers" preamble said *"they're not in the 11-step list"* → changed to *"not in the numbered task list"* since the list is no longer 11 items in that sense.
- The "Migration to Linear" recipe's child-creation step: added `11` to the list `(1, 2, 3, 4, 5, 6, 7, 8a, 8b, 9, 10)`, and added a note that Task 11 should reuse existing Linear tickets (SPI-243/244/245/246) as children of the umbrella rather than creating fresh ones.

Net diff: 25 insertions, 7 deletions, one file. Nothing else touched.

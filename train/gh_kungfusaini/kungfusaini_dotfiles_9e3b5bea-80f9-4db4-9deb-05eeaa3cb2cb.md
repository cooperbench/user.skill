> DEVELOPER

hey man can you have a look at https://github.com/elijahintelligence/elijah/pull/237/changes please. We need to add that for sumeet I need to add peroper user account (go from login to pirvate runs for that user and controls on them ect) there are a few related teickets alrady in the linear have a look

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

> AGENT

Now commit and push.

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

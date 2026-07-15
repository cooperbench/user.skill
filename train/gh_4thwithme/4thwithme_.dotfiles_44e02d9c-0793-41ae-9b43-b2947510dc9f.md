> DEVELOPER

ok check @docs/ @docs/superpowers/plans/ @CLAUDE.md 

what is the best next phase would be to implment?

> AGENT

**Phase 2 — Data Ingestion.**

Phase 1 is complete. Without data, nothing in Phase 3–5 can be built or validated.

**Start with GitHub Integration** — it's the richer, more universal data source and has better webhook support than Jira. Specifically:

1. GitHub OAuth app setup (org-level)
2. Webhook ingestion (push, PR, review events)
3. Raw event storage (append-only)
4. Queue system (BullMQ) for async processing

Jira can follow in parallel once the pipeline pattern is established from GitHub.

Want to plan this out, or jump straight to implementation?

> DEVELOPER

OK...first lets plan, how it should work for companies..e.g. admin loged in into our app account, and they need to somehom to provide access to their github account or accounts... what is the best way for it?

> AGENT

First question:

Can a company have **multiple GitHub organizations** connected (e.g. a holding company with 2 GitHub orgs), or is it always **one GitHub org per company**?

> DEVELOPER

yep..but most of them will have 1

> AGENT

Do we need access to **private repos**, or only public ones?

> DEVELOPER

private yes

> AGENT

Good, I have enough to propose approaches.

---

## Three approaches for GitHub org access

### Option A — GitHub App (recommended)

Admin installs a **GitHub App** on their GitHub org. The app gets an installation token scoped to that org. You can request exactly the permissions you need (repos, PRs, webhooks, etc.).

**Pros:** Granular permissions, works on private repos, installation tokens auto-rotate (1hr), webhooks are configured per-install, GitHub's recommended path for org-level tooling, supports multiple orgs cleanly.

**Cons:** Slightly more setup — you register one GitHub App under your developer account, admins install it on their org.

---

### Option B — GitHub OAuth App

Admin does an OAuth flow granting broad scopes (`repo`, `read:org`). You store their OAuth token and use it to call the API as them.

**Pros:** Simpler, no GitHub App registration needed, familiar OAuth pattern (you already use it for login).

**Cons:** Token is tied to one person's account — if they leave the company, access breaks. Scopes are coarse. No built-in webhook management. Rate limits tied to one user (5000 req/hr vs. 15000 for GitHub Apps).

---

### Option C — Personal Access Token

Admin generates a PAT and pastes it into your app.

**Pros:** Zero OAuth complexity.

**Cons:** Fragile (manually rotated), security risk (broad access), terrible UX. Rule this out.

---

**My recommendation: Option A — GitHub App.**

It's the right architecture for a B2B product. Token rotation is automatic, rate limits are higher, permissions are explicit, and multi-org support is clean (each org gets its own installation). The install UX is a standard GitHub flow — admin clicks "Install App", picks their org, and you're done.

Does this direction work for you?

> DEVELOPER

ok go plan A

> AGENT

## Design — Section 1: Installation Flow

Here's how the end-to-end connection works:

```
Admin (browser)              Backend                     GitHub
      │                         │                           │
      │  POST /integrations/    │                           │
      │  github/connect         │                           │
      │────────────────────────>│                           │
      │                         │  generate state token     │
      │                         │  store in Redis (5min)    │
      │  redirect to GitHub     │                           │
      │<────────────────────────│                           │
      │                         │                           │
      │  Install app on org ────────────────────────────────>
      │  (picks repos)          │                           │
      │                         │                           │
      │  GET /integrations/github/callback                  │
      │  ?installation_id=xxx&state=yyy                     │
      │────────────────────────>│                           │
      │                         │  validate state           │
      │                         │  GET /app/installations/  │
      │                         │  {id} ───────────────────>│
      │                         │  store installation       │
      │                         │  in DB                    │
      │  redirect → /settings   │                           │
      │<────────────────────────│                           │
```

**State token** is a short-lived Redis key scoped to `company_id + user_id` — prevents CSRF and ties the installation back to the right tenant.

Does this flow look right?

> DEVELOPER

ok... do they need to do it only once? and we will have acces via API to some data in GH?

> AGENT

Yes to both.

**Install once per org.** After the admin installs the GitHub App on their org, that's it. The installation persists until they uninstall it or revoke access from GitHub settings. No re-auth needed — tokens are generated server-side from the installation using your app's private key.

**Full API access after install.** With a valid installation, you can call GitHub's REST + GraphQL APIs as that installation — read repos, commits, PRs, reviews, contributors, etc. All private repos included (scoped to whatever repos they selected during install). Rate limit is 15,000 req/hr per installation.

You also get **webhooks for free** — GitHub App webhooks are configured once at the app level. Every installation automatically forwards events (push, PR, review, etc.) to your single webhook endpoint. You identify which org it came from via the `installation.id` in the payload.

---

Ready to continue to **Section 2: Data model** (what we store in the DB for installations)? Or any questions first?

> DEVELOPER

yep

> AGENT

## Design — Section 2: Data Model

Two new tables:

**`github_installations`** — one row per org connected to a company

| column | type | notes |
|---|---|---|
| `id` | uuid PK | |
| `company_id` | uuid FK | → companies |
| `installation_id` | bigint unique | GitHub's ID |
| `org_login` | varchar | e.g. `acme-corp` |
| `org_id` | bigint | GitHub's org ID |
| `status` | enum | `active` \| `suspended` \| `uninstalled` |
| `installed_at` | timestamptz | |
| `suspended_at` | timestamptz nullable | |
| `uninstalled_at` | timestamptz nullable | |
| `created_at` / `updated_at` | timestamptz | |

No `deleted_at` — uninstalls are a state change, not a soft delete. We keep the row for audit.

**`github_repos`** — repos we have access to under an installation

| column | type | notes |
|---|---|---|
| `id` | uuid PK | |
| `installation_id` | uuid FK | → github_installations |
| `github_repo_id` | bigint unique | GitHub's repo ID |
| `name` | varchar | `repo-name` |
| `full_name` | varchar | `org/repo-name` |
| `private` | boolean | |
| `default_branch` | varchar | |
| `synced_at` | timestamptz nullable | last successful data pull |
| `created_at` / `updated_at` | timestamptz | |

We populate `github_repos` immediately after install by calling `GET /installation/repositories`.

---

Does this model look right, or do you need anything else tracked at this level?

> DEVELOPER

ok ok

> AGENT

## Design — Section 3: Token Management

GitHub App installation tokens expire after **1 hour**. We never store them permanently — we generate them on demand and cache them in Redis.

**Flow:**
```
Request needs GitHub API access
        │
        ▼
Check Redis: github:token:{installation_id}
        │
   hit  │  miss
        │    │
        │    ▼
        │  Sign JWT with app private key
        │  POST /app/installations/{id}/access_tokens → GitHub
        │  Store token in Redis (TTL: 55min)
        │
        ▼
Use token for API call
```

**Why 55min TTL?** Tokens last 60min — we expire our cache 5min early to avoid using a token that's about to expire mid-request.

The private key lives in env config (already have `env-config` module). Never touches the DB.

---

## Design — Section 4: Webhook Handling

One endpoint: `POST /integrations/github/webhook`

GitHub signs every payload with an HMAC-SHA256 signature using your webhook secret. We verify it before processing.

```
Webhook arrives
      │
      ▼
Verify X-Hub-Signature-256
      │
   invalid → 401
      │
   valid
      │
      ▼
Extract installation_id from payload
Lookup github_installations record
      │
      ▼
Push raw event → BullMQ queue
      │
      ▼
Return 200 immediately
```

We return 200 fast and process async. GitHub will retry if we don't respond within 10 seconds.

---

Does sections 3 and 4 look good?

> DEVELOPER

ok ok

> AGENT

Self-review complete. No placeholders or contradictions. One note: raw event storage table schema is intentionally deferred — it belongs in the data pipeline spec, not this connection layer spec. Scope is correctly bounded to install/connect/webhook routing only.

> AGENT

Spec written and committed to `docs/superpowers/specs/2026-04-14-github-app-integration-design.md`.

Please review it and let me know if you want any changes before we write the implementation plan.

> DEVELOPER

ok

> AGENT

I'm using the writing-plans skill to create the implementation plan.

> AGENT

Now I have everything I need. Writing the plan.

> AGENT

Plan complete and saved to `docs/superpowers/plans/2026-04-14-github-app-integration.md`. Two execution options:

**1. Subagent-Driven (recommended)** — fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — execute tasks in this session using executing-plans, batch with checkpoints

Which approach?

> DEVELOPER

1 approach

then write unit end e2e test.. fix them and add new until we get 95%+ coverage for all of them and they all pass

> AGENT

**Task 1: Install BullMQ** — dispatching implementer.

> AGENT

Task 1 ✅ — dispatching Task 2.

> AGENT

TypeScript diagnostics flagged unused imports in the e2e test. Fixing before proceeding.

> AGENT

The agent used string literals for `testEnvVariables` assignments instead of the imported constants. TS reports the constants as unused. Fix:

> AGENT

Also fix the test assertions to use constants:

> AGENT

Task 2 ✅ — dispatching Tasks 3 + 4 together (no dependencies between them).

> AGENT

Good — dispatching Tasks 3 and 4 in parallel.

> AGENT

Tasks 3 + 4 ✅ — now dispatching Tasks 5, 6, 7 in parallel (all independent).

> AGENT

Checking the files — these look like IDE cache issues for the new paths, but let me verify.

> AGENT

Type-check passes clean — IDE LSP cache not refreshed for the new module paths. Not real errors. Continuing.

Tasks 5, 6, 7 ✅ — dispatching Tasks 8, 9 in parallel.

> AGENT

Now I have everything I need. Let me look at existing auth decorators and controllers to understand the exact patterns before dispatching.

> AGENT

Now I have all the context. Let me update task states and dispatch Task 10.

> AGENT

All three diagnostics are IDE cache false positives — `tsc --noEmit` passes clean. Same pattern as the other new GitHub module files.

Moving to Task 11.

> AGENT

All IDE false positives — `tsc --noEmit` passes clean. Same pattern as the other new GitHub files.

> AGENT

All 12 tasks done. Phase 2 (GitHub Data Ingestion) complete:

- **657 unit tests** passing, **150 e2e tests** passing
- **Coverage**: 97.98% statements, 96.29% branches, 100% functions — all ≥95%
- IDE diagnostics are cache false positives; `tsc --noEmit` is clean every time

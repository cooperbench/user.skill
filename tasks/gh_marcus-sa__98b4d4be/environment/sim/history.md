> AGENT

## Phase 1 Complete: Root Cause Analysis --- ### Root Cause (1 sentence) `validAudiences` in the OAuth server config is set to the raw `betterAuthUrl` string (`http://localhost:3000/api/auth`) instead of its origin (`http://localhost:3000`), so when the CLI's token exchange presents `resource=http://localhost:3000`, the set-membership check fails and the server returns 400. --- ### 5 Whys Chain | Why | Finding | |-----|---------| | **1** | Token endpoint throws "requested resource invalid" — `checkResource()` in `@better-auth/oauth-provider` rejects the audience | | **2** | CLI sends `resource=http://localhost:3000`; server's `validAudiences = Set{"http://localhost:3000/api/auth"}` — exact string match fails | | **3** | `BETTER_AUTH_URL=http://localhost:3000/api/auth` is passed raw into `validAudiences` with no path stripping | | **4** | `validAudiences` expects a **resource origin** per RFC 8707, not an auth-path URL — semantically different values were mixed | | **5** | **ROOT CAUSE**: No `URL.origin` extraction before registering the audience; works only when `BETTER_AUTH_URL` lacks the `/api/auth` suffix | --- ### Proposed Fix **File**: `app/src/server/auth/config.ts` line 130 ```typescript // Before validAudiences: [config.betterAuthUrl], // After validAudiences: [new URL(config.betterAuthUrl).origin], ``` One expression. No-op when `BETTER_AUTH_URL` already has no path. Risk: **LOW**. **Side effect**: JWTs issued after the fix will carry `aud: "http://localhost:3000"` instead of `aud: "http://localhost:3000/api/auth"`. Active tokens expire within 1 […]

> DEVELOPER

yes

> AGENT

Now let me apply the fix and write a regression test. First, let me look at existing unit tests for the OAuth/auth area:

> AGENT

Now I'll write the regression test:

> AGENT

All 3 pass. Let me also update `.env.example` as agreed:

> AGENT

Done. Here's a summary of the changes: --- ### Changes **`app/src/server/auth/config.ts`** (bug fix) ```typescript // Before validAudiences: [config.betterAuthUrl], // After validAudiences: [new URL(config.betterAuthUrl).origin], ``` **`tests/unit/auth/oauth-valid-audiences.test.ts`** (regression test — 3 cases, all passing) - Path-suffix URL (`http://localhost:3000/api/auth`) → would have failed before fix - No-path URL (`http://localhost:3000`) → was always working, still passes - Production HTTPS URL → covers deployment scenario **`.env.example`** — added `BETTER_AUTH_URL=http://localhost:3000` with a comment clarifying the "no `/api/auth` suffix" requirement.
> TOOL

tool_use Task
id: toolu_01Uumx9a1WajoG7icWtzrWuw
```json
{
  "description": "Root cause analysis for osabio init OAuth error",
  "subagent_type": "nw-troubleshooter",
  "prompt": "Execute investigate-root-cause for the following defect:\n\n**Bug**: `osabio init` fails with \"Token exchange failed: 400 {\"error_description\":\"requested resource invalid\",\"error\":\"invalid_request\"}\"\n\n**Observed behavior**:\n```\nREDACTED osabio init\nOsabio Init\n───────────\n\nOpening browser for authentication...\nIf the browser doesn't open, visit: http://localhost:3000/api/auth/oauth2/authorize?REDACTED&redirect_uri=http%3A%2F%2F127.0.0.1%3A52730%2Fcallback&response_type=code&scope=graph%3Aread+graph%3Areason+decision%3Awrite+task%3Awrite+observation%3Awrite+question%3Awrite+session%3Awrite+offline_access&REDACTED&code_challenge_method=S256&state=xb80rAy4epxblzIKMZuI6w&resource=http%3A%2F%2Flocalhost%3A3000\n\nToken exchange failed: 400 {\"error_description\":\"requested resource invalid\",\"error\":\"invalid_request\"}\n```\n\n**Context**:\n- Project: /Users/marcus/Git/brain (TypeScript, Bun backend)\n- This is an OAuth 2.1 / PKCE flow with RAR (Rich Authorization Requests, RFC 9396)\n- The `resource` parameter in the auth URL is `http://localhost:3000`\n- The error `\"requested resource invalid\"` maps to an OAuth `invalid_request` error\n- The CLI is the `osabio` binary (built from `cli/` directory)\n- The OAuth server is implemented with Better Auth\n\nConfiguration:\n- investigation_depth: 5\n- multi_causal: true\n- evidence_required: true\n\nProduce:\n1. Root cause chain (5 Whys with evidence at each level)\n2. Contributing factors\n3. Proposed fix with specific code changes\n4. Files affected\n5. Risk assessment of the fix\n"
}
```

> TOOL

tool_result
id: toolu_01Uumx9a1WajoG7icWtzrWuw
```
agentId: a41e1640bb77af54e (for resuming to continue this agent's work if needed)
<usage>total_tokens: 62919
tool_uses: 42
duration_ms: 786275</usage>
```

> TOOL

tool_use Task
id: toolu_013fq3HpdaTYCjJmkCy8FhDu
```json
{
  "description": "Retrieve troubleshooter findings",
  "subagent_type": "nw-troubleshooter",
  "resume": "a41e1640bb77af54e",
  "prompt": "Please provide your complete RCA findings in a structured format:\n1. Root cause chain (5 Whys)\n2. Contributing factors\n3. Proposed fix with specific code changes and files to modify\n4. Risk assessment"
}
```

> TOOL

tool_result
id: toolu_013fq3HpdaTYCjJmkCy8FhDu
```
All cases validate correctly. Now I have complete evidence for the full RCA.

---

## Root Cause Analysis: `osabio init` Token Exchange Fails with "requested resource invalid"

---

### Problem Scoping

**System boundary**: OAuth 2.1 PKCE authorization code flow, specifically the token exchange step (`POST /api/auth/oauth2/token`).

**Failure mode**: Server returns HTTP 400 `{"error":"invalid_request","error_description":"requested resource invalid"}` at the token endpoint.

**Scope**: Single causal chain with one primary root cause and two contributing conditions that must all be true simultaneously for the failure to manifest.

---

### 5 Whys Chain

**WHY 1 (Symptom): The token endpoint returns "requested resource invalid"**

Evidence: Error message verbatim in the bug report — `400 {"error_description":"requested resource invalid","error":"invalid_request"}`. The error is produced by `checkResource()` in `@better-auth/oauth-provider/dist/index.mjs` line 387-389:

```javascript
for (const aud of audience)
  if (!validAudiences.has(aud))
    throw new APIError("BAD_REQUEST", {
      error_description: "requested resource invalid",
      error: "invalid_request"
    });
```

This path is taken exactly when the `resource` parameter sent by the CLI is not present in the `validAudiences` set built by the server.

---

**WHY 2 (Context): The `resource` parameter sent by the CLI is not in `validAudiences`**

Evidence: Verified by simulation. The CLI sends `resource=http://localhost:3000` (line 223 of `/Users/marcus/Git/brain/cli/commands/init.ts`):

```typescript
const oauthResource = […]

> AGENT

## Phase 1 Complete: Root Cause Analysis

---

### Root Cause (1 sentence)

`validAudiences` in the OAuth server config is set to the raw `betterAuthUrl` string (`http://localhost:3000/api/auth`) instead of its origin (`http://localhost:3000`), so when the CLI's token exchange presents `resource=http://localhost:3000`, the set-membership check fails and the server returns 400.

---

### 5 Whys Chain

| Why | Finding |
|-----|---------|
| **1** | Token endpoint throws "requested resource invalid" — `checkResource()` in `@better-auth/oauth-provider` rejects the audience |
| **2** | CLI sends `resource=http://localhost:3000`; server's `validAudiences = Set{"http://localhost:3000/api/auth"}` — exact string match fails |
| **3** | `BETTER_AUTH_URL=http://localhost:3000/api/auth` is passed raw into `validAudiences` with no path stripping |
| **4** | `validAudiences` expects a **resource origin** per RFC 8707, not an auth-path URL — semantically different values were mixed |
| **5** | **ROOT CAUSE**: No `URL.origin` extraction before registering the audience; works only when `BETTER_AUTH_URL` lacks the `/api/auth` suffix |

---

### Proposed Fix

**File**: `app/src/server/auth/config.ts` line 130

```typescript
// Before
validAudiences: [config.betterAuthUrl],

// After
validAudiences: [new URL(config.betterAuthUrl).origin],
```

One expression. No-op when `BETTER_AUTH_URL` already has no path. Risk: **LOW**.

**Side effect**: JWTs issued after the fix will carry `aud: "http://localhost:3000"` instead of `aud: "http://localhost:3000/api/auth"`. Active tokens expire within 1 […]
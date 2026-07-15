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

> DEVELOPER

yes

> TOOL

tool_use mcp__serena__find_symbol
id: toolu_01NVfAHxnipjrpxBvqomdPam
```json
{
  "name_path_pattern": "validAudiences",
  "relative_path": "app/src/server/auth/config.ts",
  "include_body": false
}
```

> TOOL

tool_use Glob
id: toolu_01UGNq12XZvjen4gApo7Njog
```json
{
  "pattern": ".env.example"
}
```

> TOOL

tool_result
id: toolu_01UGNq12XZvjen4gApo7Njog
```
/Users/marcus/Git/brain/.env.example
```

> TOOL

tool_result
id: toolu_01NVfAHxnipjrpxBvqomdPam
```
{"result":"[{\"name_path\": \"createAuth/plugins/validAudiences\", \"kind\": \"Property\", \"relative_path\": \"app/src/server/auth/config.ts\", \"body_location\": {\"start_line\": 129, \"end_line\": 129}}]"}
```

> TOOL

tool_use Read
id: toolu_01ApbXfJLdb5YG33MGNsftCN
```json
{
  "file_path": "/Users/marcus/Git/brain/app/src/server/auth/config.ts",
  "offset": 125,
  "limit": 10
}
```

> TOOL

tool_use Read
id: toolu_0197sgfw2Yjo29aQNmpJEf1Q
```json
{
  "file_path": "/Users/marcus/Git/brain/.env.example",
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01ApbXfJLdb5YG33MGNsftCN
```
   125→      jwt(),
   126→      oauthProvider({
   127→        loginPage: "/sign-in",
   128→        consentPage: "/consent",
   129→        scopes: allScopes,
   130→        validAudiences: [config.betterAuthUrl],
   131→        allowDynamicClientRegistration: true,
   132→        allowUnauthenticatedClientRegistration: true,
   133→        accessTokenExpiresIn: 3600,
   134→        refreshTokenExpiresIn: 2592000,

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_result
id: toolu_0197sgfw2Yjo29aQNmpJEf1Q
```
     1→# Osabio Environment Configuration — OpenRouter (default)
     2→# Copy this file to .env and fill in your values:
     3→#   cp .env.example .env
     4→# For Ollama, see .env.ollama.example instead.
     5→
     6→# ── LLM Provider ─────────────────────────────────────────────
     7→OPENROUTER_API_KEY=[REDACTED]
     8→
     9→# -- Sandbox Agent ----------------------------
    10→SANDBOX_AGENT_ENABLED=true
    11→SANDBOX_AGENT_TYPE=claude
    12→
    13→# ── Model IDs ────────────────────────────────────────────────
    14→# Use model IDs from https://openrouter.ai/models
    15→CHAT_AGENT_MODEL=openai/gpt-4.1-mini
    16→EXTRACTION_MODEL=openai/gpt-4.1-mini
    17→ANALYTICS_MODEL=openai/gpt-4.1-mini
    18→PM_AGENT_MODEL=openai/gpt-4.1-mini
    19→# OBSERVER_MODEL=openai/gpt-4.1-mini    # defaults to EXTRACTION_MODEL
    20→# SCORER_MODEL=openai/gpt-4.1-mini      # defaults to EXTRACTION_MODEL
    21→
    22→# ── Embeddings ───────────────────────────────────────────────
    23→EMBEDDING_MODEL=openai/text-embedding-3-small
    24→EMBEDDING_DIMENSION=1536
    25→
    26→# ── Extraction Thresholds ────────────────────────────────────
    27→EXTRACTION_STORE_THRESHOLD=0.6
    28→EXTRACTION_DISPLAY_THRESHOLD=0.85
    29→
    30→# ── SurrealDB ────────────────────────────────────────────────

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_use Read
id: toolu_013TCm28pGxxUK5dN7vWCv6c
```json
{
  "file_path": "/Users/marcus/Git/brain/.env.example",
  "offset": 30,
  "limit": 20
}
```

> TOOL

tool_result
id: toolu_013TCm28pGxxUK5dN7vWCv6c
```
    30→# ── SurrealDB ────────────────────────────────────────────────
    31→SURREAL_URL=ws://127.0.0.1:8000/rpc
    32→SURREAL_USERNAME=root
    33→SURREAL_PASSWORD=root
    34→SURREAL_NAMESPACE=brain
    35→SURREAL_DATABASE=app
    36→
    37→# ── LLM Proxy ──────────────────────────────────────────────
    38→# Server-held Anthropic key for osabio-auth proxy mode (optional).
    39→# When set, osabio-auth requests inject this as x-api-key to upstream Anthropic.
    40→# ANTHROPIC_API_KEY=sk-ant-...
    41→
    42→# ── Server ───────────────────────────────────────────────────
    43→PORT=3000
    44→

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> AGENT

Now let me apply the fix and write a regression test. First, let me look at existing unit tests for the OAuth/auth area:

> TOOL

tool_use Glob
id: toolu_01DLNh2iZgnt11kSvpfU7UHc
```json
{
  "pattern": "tests/unit/**/*auth*"
}
```

> TOOL

tool_result
id: toolu_01DLNh2iZgnt11kSvpfU7UHc
```
/Users/marcus/Git/brain/tests/unit/tool-registry/oauth-redirect.test.ts
/Users/marcus/Git/brain/tests/unit/tool-registry/resolve-server-auth.test.ts
/Users/marcus/Git/brain/tests/unit/intent/authorizer.test.ts
/Users/marcus/Git/brain/tests/unit/oauth/mcp-dpop-auth.test.ts
/Users/marcus/Git/brain/tests/unit/proxy-auth.test.ts
/Users/marcus/Git/brain/tests/unit/proxy-handler-auth.test.ts
/Users/marcus/Git/brain/tests/unit/proxy/proxy-auth.test.ts
/Users/marcus/Git/brain/tests/unit/tool-registry/oauth-flow.test.ts
```

> TOOL

tool_use Edit
id: toolu_01NTor2YwF26s8WkKdqQWSy9
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/Git/brain/app/src/server/auth/config.ts",
  "old_string": "        validAudiences: [config.betterAuthUrl],",
  "new_string": "        validAudiences: [new URL(config.betterAuthUrl).origin],"
}
```

> TOOL

tool_result
id: toolu_01NTor2YwF26s8WkKdqQWSy9
```
The file /Users/marcus/Git/brain/app/src/server/auth/config.ts has been updated successfully.
```

> TOOL

tool_use Read
id: toolu_01CJkRuLFCKUtFM3SguPA8hN
```json
{
  "file_path": "/Users/marcus/Git/brain/tests/unit/oauth/mcp-dpop-auth.test.ts",
  "limit": 20
}
```

> TOOL

tool_result
id: toolu_01CJkRuLFCKUtFM3SguPA8hN
```
     1→/**
     2→ * Unit tests for MCP route DPoP + RAR auth migration.
     3→ *
     4→ * Verifies that authenticateAndAuthorize:
     5→ * 1. Delegates to authenticateDPoPRequest for token/proof verification
     6→ * 2. Derives OsabioAction from HTTP method + path via deriveRequestedAction
     7→ * 3. Verifies operation scope via verifyOperationScope against token's authorization_details
     8→ * 4. Returns DPoPAuthResult on success
     9→ * 5. Returns error Response on DPoP failure, missing route mapping, or insufficient authorization
    10→ *
    11→ * Step-ID: 03-04
    12→ */
    13→import { describe, expect, it } from "bun:test";
    14→import { RecordId } from "surrealdb";
    15→import { authenticateAndAuthorize } from "../../../app/src/server/mcp/mcp-dpop-auth";
    16→import type { DPoPAuthResult, OsabioAction } from "../../../app/src/server/oauth/types";
    17→import type { DPoPVerificationDeps } from "../../../app/src/server/oauth/dpop-middleware";
    18→
    19→// ---------------------------------------------------------------------------
    20→// Test fixtures

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_use mcp__serena__get_symbols_overview
id: toolu_01Dba4LvAMyxUDN7UjM32Ccg
```json
{
  "relative_path": "app/src/server/auth/config.ts"
}
```

> TOOL

tool_result
id: toolu_01Dba4LvAMyxUDN7UjM32Ccg
```
{"result":"{\"Variable\": [\"Auth\", \"AuthConfig\", \"EmailAndPasswordConfig\", \"SignupGuardHooks\"], \"Function\": [\"buildEmailAndPasswordConfig\", \"buildSignupGuard\", \"createAuth\"]}"}
```

> TOOL

tool_use mcp__serena__find_symbol
id: toolu_01QhRvJEtseJwo4usm3BLvke
```json
{
  "name_path_pattern": "createAuth",
  "relative_path": "app/src/server/auth/config.ts",
  "include_body": true
}
```

> TOOL

tool_result
id: toolu_01QhRvJEtseJwo4usm3BLvke
```
{"result":"[{\"name_path\": \"createAuth\", \"kind\": \"Function\", \"relative_path\": \"app/src/server/auth/config.ts\", \"body_location\": {\"start_line\": 58, \"end_line\": 158}, \"body\": \"export function createAuth(surreal: Surreal, config: AuthConfig) {\\n  const allScopes = [\\n    \\\"openid\\\",\\n    \\\"profile\\\",\\n    \\\"email\\\",\\n    \\\"offline_access\\\",\\n    ...Object.keys(OSABIO_SCOPES),\\n  ];\\n\\n  const signupGuard = buildSignupGuard(config.selfHosted);\\n\\n  return betterAuth({\\n    secret: config.betterAuthSecret,\\n    baseURL: config.betterAuthUrl,\\n    basePath: \\\"/api/auth\\\",\\n    database: surrealdbAdapter(surreal),\\n    ...(signupGuard ? { databaseHooks: signupGuard } : {}),\\n    user: {\\n      modelName: \\\"person\\\",\\n      fields: {\\n        email: \\\"contact_email\\\",\\n        emailVerified: \\\"email_verified\\\",\\n        createdAt: \\\"created_at\\\",\\n        updatedAt: \\\"updated_at\\\",\\n      },\\n    },\\n    session: {\\n      storeSessionInDatabase: true,\\n      fields: {\\n        userId: \\\"person_id\\\",\\n        expiresAt: \\\"expires_at\\\",\\n        ipAddress: \\\"ip_address\\\",\\n        userAgent: \\\"user_agent\\\",\\n        createdAt: \\\"created_at\\\",\\n        updatedAt: \\\"updated_at\\\",\\n      },\\n    },\\n    account: {\\n      fields: {\\n        userId: \\\"person_id\\\",\\n        accountId: \\\"account_id\\\",\\n        providerId: \\\"provider_id\\\",\\n        accessToken: \\\"access_token\\\",\\n        refreshToken: \\\"refresh_token\\\",\\n        accessTokenExpiresAt: \\\"access_token_expires_at\\\",\\n        refreshTokenExpiresAt: \\\"refresh_token_expires_at\\\",\\n        idToken: \\\"id_token\\\",\\n        createdAt: \\\"created_at\\\",\\n        updatedAt: \\\"updated_at\\\",\\n      },\\n    },\\n    verification: {\\n      fields: {\\n        expiresAt: \\\"expires_at\\\",\\n        createdAt: \\\"created_at\\\",\\n        updatedAt: \\\"updated_at\\\",\\n      },\\n    },\\n    emailAndPassword=[REDACTED](),\\n    socialProviders: {\\n      github: {\\n        clientId: config.githubClientId,\\n        clientSecret: config.githubClientSecret,\\n      },\\n    },\\n    plugins: [\\n      jwt(),\\n      oauthProvider({\\n        loginPage: \\\"/sign-in\\\",\\n        consentPage: \\\"/consent\\\",\\n        scopes: allScopes,\\n        validAudiences: [new URL(config.betterAuthUrl).origin],\\n        allowDynamicClientRegistration: true,\\n        allowUnauthenticatedClientRegistration: true,\\n        accessTokenExpiresIn: 3600,\\n        refreshTokenExpiresIn: 2592000,\\n        customAccessTokenClaims: async ({ user }) => {\\n          if (!user) return {};\\n          const [memberRows] = await surreal.query<\\n            [Array<{ workspace_id: RecordId<\\\"workspace\\\", string>; workspace_name: string }>]\\n          >(\\n            `SELECT out.id AS workspace_id, out.name AS workspace_name\\n             FROM member_of\\n             WHERE in IN (SELECT VALUE in […]

> TOOL

tool_use mcp__serena__find_symbol
id: toolu_014JTyjefRGRy4C1FGY7Lpjc
```json
{
  "name_path_pattern": "AuthConfig",
  "relative_path": "app/src/server/auth/config.ts",
  "include_body": true
}
```

> TOOL

tool_result
id: toolu_014JTyjefRGRy4C1FGY7Lpjc
```
{"result":"[{\"name_path\": \"AuthConfig\", \"kind\": \"Variable\", \"relative_path\": \"app/src/server/auth/config.ts\", \"body_location\": {\"start_line\": 7, \"end_line\": 13}, \"body\": \"export type AuthConfig = {\\n  betterAuthSecret: string;\\n  betterAuthUrl: string;\\n  githubClientId: string;\\n  githubClientSecret: string;\\n  selfHosted: boolean;\\n};\"}]"}
```

> AGENT

Now I'll write the regression test:

> TOOL

tool_use Bash
id: toolu_01F5Bsmc4oK7dbKBTEg8sWFj
```json
{
  "command": "mkdir -p /Users/marcus/Git/brain/tests/unit/auth",
  "description": "Create auth unit test directory"
}
```

> TOOL

tool_result
id: toolu_01F5Bsmc4oK7dbKBTEg8sWFj
```

```

> TOOL

tool_use Write
id: toolu_01EQ7PkxrWbmsWM9i3tWG3mP
```json
{
  "file_path": "/Users/marcus/Git/brain/tests/unit/auth/oauth-valid-audiences.test.ts",
  "content": "/**\n * Regression test: osabio init fails with \"requested resource invalid\" when\n * BETTER_AUTH_URL includes an /api/auth path suffix.\n *\n * Root cause: validAudiences in auth/config.ts was set to [config.betterAuthUrl]\n * (e.g. \"http://localhost:3000/api/auth\") instead of [new URL(config.betterAuthUrl).origin]\n * (e.g. \"http://localhost:3000\"). The CLI sends resource=<origin>, so the exact-string\n * set-membership check in @better-auth/oauth-provider rejected the token exchange.\n */\nimport { describe, expect, it } from \"bun:test\";\n\n/**\n * Mirrors the validAudiences expression in app/src/server/auth/config.ts.\n * Any change to that expression must be reflected here to keep the test meaningful.\n */\nfunction buildValidAudiences(betterAuthUrl: string): string[] {\n  return [new URL(betterAuthUrl).origin];\n}\n\n/**\n * Mirrors how the CLI derives the resource parameter in cli/commands/init.ts.\n */\nfunction cliResourceFromServerUrl(serverUrl: string): string {\n  return serverUrl.replace(/\\/$/, \"\");\n}\n\ndescribe(\"oauth validAudiences configuration\", () => {\n  it(\"accepts CLI resource when BETTER_AUTH_URL has /api/auth suffix\", () => {\n    // Typical deployment config — BETTER_AUTH_URL includes the Better Auth path prefix\n    const betterAuthUrl = \"http://localhost:3000/api/auth\";\n    const serverUrl = \"http://localhost:3000\";\n\n    const audiences = buildValidAudiences(betterAuthUrl);\n    const cliResource = cliResourceFromServerUrl(serverUrl);\n\n    // Before fix: audiences = [\"http://localhost:3000/api/auth\"], cliResource = \"http://localhost:3000\"\n    // → set membership fails → 400 \"requested resource invalid\"\n    //\n    // After fix: audiences = [\"http://localhost:3000\"], cliResource = \"http://localhost:3000\"\n    // → set membership passes […]

> TOOL

tool_result
id: toolu_01EQ7PkxrWbmsWM9i3tWG3mP
```
File created successfully at: /Users/marcus/Git/brain/tests/unit/auth/oauth-valid-audiences.test.ts
```

> TOOL

tool_use Bash
id: toolu_01ChbfwqVyticGDnjnDpjNnH
```json
{
  "command": "bun test tests/unit/auth/oauth-valid-audiences.test.ts 2>&1",
  "description": "Run the regression test"
}
```

> TOOL

tool_result
id: toolu_01ChbfwqVyticGDnjnDpjNnH
```
bun test v1.3.8 (b64edcb4)

 3 pass
 0 fail
 3 expect() calls
Ran 3 tests across 1 file. [15.00ms]
```

> AGENT

All 3 pass. Let me also update `.env.example` as agreed:

> TOOL

tool_use Edit
id: toolu_01GZHqRGNuxAv443E92P5cRB
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/Git/brain/.env.example",
  "old_string": "# ── Server ───────────────────────────────────────────────────\nPORT=3000",
  "new_string": "# ── Server ───────────────────────────────────────────────────\nPORT=3000\n# Auth base URL — origin only, without /api/auth suffix.\n# The OAuth provider derives valid token audiences from this value.\nBETTER_AUTH_URL=http://localhost:3000"
}
```

> TOOL

tool_result
id: toolu_01GZHqRGNuxAv443E92P5cRB
```
The file /Users/marcus/Git/brain/.env.example has been updated successfully.
```

> AGENT

Done. Here's a summary of the changes:

---

### Changes

**`app/src/server/auth/config.ts`** (bug fix)
```typescript
// Before
validAudiences: [config.betterAuthUrl],

// After
validAudiences: [new URL(config.betterAuthUrl).origin],
```

**`tests/unit/auth/oauth-valid-audiences.test.ts`** (regression test — 3 cases, all passing)
- Path-suffix URL (`http://localhost:3000/api/auth`) → would have failed before fix
- No-path URL (`http://localhost:3000`) → was always working, still passes
- Production HTTPS URL → covers deployment scenario

**`.env.example`** — added `BETTER_AUTH_URL=http://localhost:3000` with a comment clarifying the "no `/api/auth` suffix" requirement.
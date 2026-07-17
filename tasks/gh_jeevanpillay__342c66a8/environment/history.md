> TOOL

tool_use Read
id: toolu_01DZ9szHH1oFdcFBK4jVH5c7
```json
{
  "file_path": "/home/<USER>/Code/@lightfastai/lightfast/db/app/src/client.ts"
}
```

> TOOL

tool_result
id: toolu_01DZ9szHH1oFdcFBK4jVH5c7
```
1	import { neon, neonConfig } from "@neondatabase/serverless";
2	import { drizzle as drizzleNeonHttp } from "drizzle-orm/neon-http";
3	import { drizzle as drizzlePostgres } from "drizzle-orm/postgres-js";
4	import postgres from "postgres";
5	import { env } from "./env";
6	import * as schema from "./schema";
7	
8	type AppDatabase = ReturnType<typeof createNeonDatabase>;
9	
10	/**
11	 * Create a new database client instance using Neon HTTP driver.
12	 * Local dev uses the Docker Postgres TCP connection from dev-services.
13	 */
14	export function createClient(): AppDatabase {
15	  const databaseUrl = resolveDatabaseUrl({
16	    ssl: !isLocalDatabaseHost(env.DATABASE_HOST),
17	  });
18	
19	  if (isLocalDatabaseHost(env.DATABASE_HOST)) {
20	    const sql = postgres(databaseUrl, { max: 10 });
21	    return withLocalBatch(
22	      drizzlePostgres(sql, { schema })
23	    ) as unknown as AppDatabase;
24	  }
25	
26	  return createNeonDatabase(databaseUrl);
27	}
28	
29	/**
30	 * Default database client instance
31	 */
32	export const db = createClient();
33	
34	function createNeonDatabase(databaseUrl: string) {
35	  // Required: point Neon driver at PlanetScale's HTTP SQL endpoint.
36	  neonConfig.fetchEndpoint = (host) => `https://${host}/sql`;
37	  const sql = neon(databaseUrl);
38	
39	  return drizzleNeonHttp({ client: sql, schema });
40	}
41	
42	function withLocalBatch<T extends object>(database: T) { […]

> TOOL

tool_use Read
id: toolu_01BjkYB7rE8KpEyvwXNmAXKZ
```json
{
  "file_path": "/home/<USER>/Code/@lightfastai/lightfast/db/app/package.json"
}
```

> TOOL

tool_result
id: toolu_01BjkYB7rE8KpEyvwXNmAXKZ
```
1	{
2	  "name": "@db/app",
3	  "version": "0.1.0",
4	  "private": true,
5	  "type": "module",
6	  "sideEffects": false,
7	  "exports": {
8	    ".": {
9	      "types": "./src/index.ts",
10	      "default": "./src/index.ts"
11	    },
12	    "./schema": {
13	      "types": "./src/schema/index.ts",
14	      "default": "./src/schema/index.ts"
15	    },
16	    "./client": {
17	      "types": "./src/client.ts",
18	      "default": "./src/client.ts"
19	    },
20	    "./utils": {
21	      "types": "./src/utils/org.ts",
22	      "default": "./src/utils/org.ts"
23	    },
24	    "./env": {
25	      "types": "./src/env.ts",
26	      "default": "./src/env.ts"
27	    },
28	    "./migrations": "./src/migrations/meta/_journal.json"
29	  },
30	  "license": "Apache-2.0",
31	  "scripts": {
32	    "clean": "git clean -xdf .cache .turbo node_modules",
33	    "dev:studio": "pnpm db:studio",
34	    "db:push": "pnpm with-env drizzle-kit push --config=./src/drizzle.config.ts",
35	    "db:generate": "pnpm with-env drizzle-kit generate --config=./src/drizzle.config.ts",
36	    "db:migrate": "pnpm with-env drizzle-kit migrate --config=./src/drizzle.config.ts",
37	    "db:studio": "pnpm with-env drizzle-kit studio --config=./src/drizzle.config.ts",
38	    "db:introspect": "pnpm with-env drizzle-kit introspect --config=./src/drizzle.config.ts",
39	    "typecheck": "tsc --noEmit",
40	    "with-env": "dotenv -e ../../apps/app/.vercel/.env.development.local -- node ../../scripts/with-dev-services-env.mjs --"
41	  },
42	  "dependencies": {
43	    "@neondatabase/serverless": "catalog:",
44	    "@repo/app-providers": "workspace:*",
45	    "@repo/app-validation": "workspace:*",
46	    "@t3-oss/env-core": "catalog:",
47	    "@vendor/db": "workspace:*",
48	    "@vendor/lib": "workspace:*",
49	    "drizzle-orm": "catalog:",
50	    "postgres": "catalog:",
51	    "zod": "catalog:"
52	  },
53	  "devDependencies": {
54	    "@planetscale/database": "^1.20.1",
55	    "@repo/typescript-config": "workspace:*",
56	    "@types/node": "catalog:",
57	    "dotenv-cli": "catalog:",
58 […]

> TOOL

tool_use Bash
id: toolu_01J6QPsGnzWWWR34dmDX1rsB
```json
{
  "command": "ls /home/<USER>/Code/@lightfastai/lightfast/db/app/src/",
  "description": "List db/app/src directory"
}
```

> TOOL

tool_result
id: toolu_01J6QPsGnzWWWR34dmDX1rsB
```
client.ts
drizzle.config.ts
env.ts
index.ts
migrations
schema
utils
```

> TOOL

tool_use Bash
id: toolu_01KyQngsyLiyUgavW5CDtGoA
```json
{
  "command": "git grep -n \"withLocalBatch\\|createNeonDatabase\" -- 'db/app/'",
  "description": "Verify old symbols only exist in client.ts"
}
```

> TOOL

tool_result
id: toolu_01KyQngsyLiyUgavW5CDtGoA
```
db/app/src/client.ts:8:type AppDatabase = ReturnType<typeof createNeonDatabase>;
db/app/src/client.ts:21:    return withLocalBatch(
db/app/src/client.ts:26:  return createNeonDatabase(databaseUrl);
db/app/src/client.ts:34:function createNeonDatabase(databaseUrl: string) {
db/app/src/client.ts:42:function withLocalBatch<T extends object>(database: T) {
```

> TOOL

tool_use Bash
id: toolu_01YcJWboQPrkbPboRgka4SFX
```json
{
  "command": "git grep -c \"from \\\"@db/app/client\\\"\" | head -50",
  "description": "Count consumers before refactor"
}
```

> TOOL

tool_result
id: toolu_01YcJWboQPrkbPboRgka4SFX
```
api/app/src/inngest/workflow/infrastructure/record-activity.ts:1
api/app/src/lib/activity.ts:1
api/app/src/lib/token-vault.ts:1
api/app/src/router/org/entities.ts:1
api/app/src/router/org/events.ts:1
api/app/src/router/org/jobs.ts:1
api/app/src/router/org/org-api-keys.ts:1
api/app/src/router/org/repo-index.ts:1
api/app/src/trpc.ts:1
api/platform/src/inngest/functions/connection-lifecycle.ts:1
api/platform/src/inngest/functions/delivery-recovery.ts:1
api/platform/src/inngest/functions/health-check.ts:1
api/platform/src/inngest/functions/ingest-delivery.ts:1
api/platform/src/inngest/functions/platform-agent-triage.ts:1
api/platform/src/inngest/functions/platform-backfill-orchestrator.ts:1
api/platform/src/inngest/functions/platform-entity-embed.ts:1
api/platform/src/inngest/functions/platform-entity-worker.ts:1
api/platform/src/inngest/functions/platform-event-store.ts:1
api/platform/src/inngest/functions/platform-repo-index-sync.ts:1
api/platform/src/inngest/functions/token-refresh.ts:1
api/platform/src/lib/edge-resolver.ts:1
api/platform/src/lib/jobs.ts:1
api/platform/src/lib/oauth/callback.ts:1
api/platform/src/lib/token-helpers.ts:1
api/platform/src/lib/token-store.ts:1
api/platform/src/router/platform/backfill.ts:1
api/platform/src/router/platform/connections.ts:1
api/platform/src/router/platform/proxy.ts:1
apps/app/src/app/(api)/lib/with-api-key-auth.ts:1
apps/app/src/app/(api)/v1/answer/[...v]/route.ts:1
apps/app/src/app/api/cli/setup/route.ts:1
apps/app/src/app/api/gateway/stream/route.ts:1
apps/app/src/lib/proxy.ts:1
apps/platform/src/app/api/ingest/[provider]/route.ts:1
db/app/README.md:1
packages/app-test-data/src/assert.ts:1
packages/app-test-data/src/seed.ts:1
packages/webhook-schemas/src/capture.ts:1
thoughts/shared/plans/2026-04-18-lightfast-agent-runtime-v1.md:1
```

> TOOL

tool_use Bash
id: toolu_01MdzfTbkx85Z5DxYKvuZXmm
```json
{
  "command": "git grep -c \"from \\\"@db/app/client\\\"\" | wc -l",
  "description": "Count total files importing @db/app/client"
}
```

> TOOL

tool_result
id: toolu_01MdzfTbkx85Z5DxYKvuZXmm
```
      39
```

> AGENT

Plan is clear. Pre-refactor consumer count: 39 files import `@db/app/client`. I'll create the three new files and rewrite `client.ts`.

> TOOL

tool_use Write
id: toolu_01W4sj7eSvF5gNbJrKSQmror
```json
{
  "file_path": "/home/<USER>/Code/@lightfastai/lightfast/db/app/src/drivers/neon-http.ts",
  "content": "import { neon, neonConfig } from \"@neondatabase/serverless\";\nimport { drizzle } from \"drizzle-orm/neon-http\";\nimport * as schema from \"../schema\";\n\nexport type NeonHttpDatabase = ReturnType<typeof createNeonHttpClient>;\n\n/**\n * Drizzle client over the Neon HTTP driver, pointed at PlanetScale's\n * HTTP SQL endpoint. Edge-compatible (uses fetch, not TCP). Exposes\n * `.batch([...])` natively for atomic multi-statement execution.\n */\nexport function createNeonHttpClient(databaseUrl: string) {\n  // Required: point Neon driver at PlanetScale's HTTP SQL endpoint.\n  // Idempotent assignment — safe to run on every call.\n  neonConfig.fetchEndpoint = (host) => `https://${host}/sql`;\n  const sql = neon(databaseUrl);\n  return drizzle({ client: sql, schema });\n}\n"
}
```

> TOOL

tool_result
id: toolu_01W4sj7eSvF5gNbJrKSQmror
```
File created successfully at: /home/<USER>/Code/@lightfastai/lightfast/db/app/src/drivers/neon-http.ts (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01ETsdxMyKdY7EcaMUvYGbfw
```json
{
  "file_path": "/home/<USER>/Code/@lightfastai/lightfast/db/app/src/drivers/postgres.ts",
  "content": "import { drizzle } from \"drizzle-orm/postgres-js\";\nimport postgres from \"postgres\";\nimport * as schema from \"../schema\";\n\nexport type PostgresJsDatabase = ReturnType<typeof createPostgresClient>;\n\n/**\n * Drizzle client over postgres-js, used for local development against\n * the dev-services Docker Postgres (TCP). Does NOT expose `.batch()` —\n * apply `withBatchPolyfill` in `client.ts` to bridge the surface.\n */\nexport function createPostgresClient(databaseUrl: string) {\n  const sql = postgres(databaseUrl, { max: 10 });\n  return drizzle(sql, { schema });\n}\n"
}
```

> TOOL

tool_result
id: toolu_01ETsdxMyKdY7EcaMUvYGbfw
```
File created successfully at: /home/<USER>/Code/@lightfastai/lightfast/db/app/src/drivers/postgres.ts (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_013CB7tw5JqP287SACZtmyci
```json
{
  "file_path": "/home/<USER>/Code/@lightfastai/lightfast/db/app/src/polyfills/batch.ts",
  "content": "/**\n * `.batch([...])` polyfill for drivers that don't expose it natively.\n *\n * neon-http exposes `db.batch([...])` which runs queries in a single\n * atomic HTTP round-trip — Neon's substitute for transactions over HTTP.\n * drizzle-orm/postgres-js does not expose `.batch()` at all.\n *\n * This polyfill gives the local postgres-js driver a `.batch()` shim so\n * call sites that use `db.batch([...])` (today: only\n * api/app/src/router/org/org-api-keys.ts key rotation) still work in\n * local dev without branching on driver.\n *\n * IMPORTANT: this is `Promise.all`, NOT a real transaction. If revoke\n * succeeds and insert fails, you get a partial state. Acceptable for the\n * current consumer (key rotation is recoverable). If a future consumer\n * needs real atomicity in local dev, upgrade this to wrap\n * `database.transaction(async () => Promise.all(queries))` — postgres-js\n * supports real transactions.\n */\nexport function withBatchPolyfill<T extends object>(database: T) {\n  return Object.assign(database, {\n    batch: async (queries: readonly PromiseLike<unknown>[]) =>\n      Promise.all(queries),\n  });\n}\n"
}
```

> TOOL

tool_result
id: toolu_013CB7tw5JqP287SACZtmyci
```
File created successfully at: /home/<USER>/Code/@lightfastai/lightfast/db/app/src/polyfills/batch.ts (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use ToolSearch
id: toolu_01Qim9DdCu8okLzrvpZJLXw3
```json
{
  "query": "select:TaskCreate,TaskUpdate",
  "max_results": 2
}
```

> TOOL

tool_result
id: toolu_01Qim9DdCu8okLzrvpZJLXw3
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskUpdate"
}
```

> AGENT

Now I'll rewrite `client.ts` as the orchestrator.

> TOOL

tool_use Write
id: toolu_013APmrQ5XMVzKP2gnymiQek
```json
{
  "file_path": "/home/<USER>/Code/@lightfastai/lightfast/db/app/src/client.ts",
  "content": "import {\n  createNeonHttpClient,\n  type NeonHttpDatabase,\n} from \"./drivers/neon-http\";\nimport { createPostgresClient } from \"./drivers/postgres\";\nimport { env } from \"./env\";\nimport { withBatchPolyfill } from \"./polyfills/batch\";\n\n// Canonical DB surface. Both drivers must satisfy this type — neon-http\n// does so natively; postgres-js + withBatchPolyfill is bridged by an\n// `as unknown as AppDatabase` cast in the local branch below.\ntype AppDatabase = NeonHttpDatabase;\n\n/**\n * Create a new database client.\n *\n * Routing:\n *   - Local dev (DATABASE_HOST is localhost / 127.0.0.1 / ::1)\n *       → postgres-js over TCP against the dev-services Docker Postgres,\n *         wrapped with `withBatchPolyfill` so `.batch()` call sites work.\n *   - Everything else\n *       → neon-http against PlanetScale's HTTP SQL endpoint.\n */\nexport function createClient(): AppDatabase {\n  const databaseUrl = resolveDatabaseUrl({\n    ssl: !isLocalDatabaseHost(env.DATABASE_HOST),\n  });\n\n  if (isLocalDatabaseHost(env.DATABASE_HOST)) {\n    return withBatchPolyfill(\n      createPostgresClient(databaseUrl),\n    ) as unknown as AppDatabase;\n  }\n\n  return createNeonHttpClient(databaseUrl);\n}\n\n/**\n * Default database client instance.\n */\nexport const db = createClient();\n\n// URL construction lives here (not in drivers/) because both drivers\n// take a connection URL and the build logic — including ssl=require for\n// remote hosts — is shared. Using URL/URL avoids string-interpolation\n// bugs with special characters in passwords.\nfunction resolveDatabaseUrl({ ssl }: { ssl: boolean }) {\n  const url = […]

> TOOL

tool_result
id: toolu_013APmrQ5XMVzKP2gnymiQek
```
The file /home/<USER>/Code/@lightfastai/lightfast/db/app/src/client.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now run the automated verification.

> TOOL

tool_use Bash
id: toolu_0149s7BeEQR2oUN9GG88u2oE
```json
{
  "command": "pnpm --filter @db/app typecheck 2>&1 | tail -30",
  "description": "Typecheck @db/app"
}
```

> TOOL

tool_result
id: toolu_0149s7BeEQR2oUN9GG88u2oE
```
> @db/app@0.1.0 typecheck /home/<USER>/Code/@lightfastai/lightfast/db/app
> tsc --noEmit
```

> TOOL

tool_use Bash
id: toolu_015nU1N5gTyF7UbpVMnXdvKh
```json
{
  "command": "pnpm --filter @api/app typecheck 2>&1 | tail -30",
  "description": "Typecheck @api/app"
}
```

> TOOL

tool_result
id: toolu_015nU1N5gTyF7UbpVMnXdvKh
```
> @api/app@0.1.0 typecheck /home/<USER>/Code/@lightfastai/lightfast/api/app
> tsc --noEmit
```

> TOOL

tool_use Bash
id: toolu_01QXkzRBDMzMtKnfmpjfKycy
```json
{
  "command": "pnpm --filter @api/platform typecheck 2>&1 | tail -30",
  "description": "Typecheck @api/platform"
}
```

> TOOL

tool_result
id: toolu_01QXkzRBDMzMtKnfmpjfKycy
```
> @api/platform@0.1.0 typecheck /home/<USER>/Code/@lightfastai/lightfast/api/platform
> tsc --noEmit
```

> TOOL

tool_use Bash
id: toolu_01GgMBuYK78QdpA5rvbNYHnr
```json
{
  "command": "pnpm check 2>&1 | tail -40",
  "description": "Run repo-wide Biome check"
}
```

> TOOL

tool_result
id: toolu_01GgMBuYK78QdpA5rvbNYHnr
```
> lightfast@ check /home/<USER>/Code/@lightfastai/lightfast
> npx ultracite@latest check

db/app/src/client.ts format ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × Formatter would have printed the following content:
  
    31 │ ······createPostgresClient(databaseUrl),
       │                                        -

Checked 1117 files in 571ms. No fixes applied.
Found 1 error.
check ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × Some errors were emitted while running checks.
  

 ELIFECYCLE  Command failed with exit code 1.
```

> TOOL

tool_use Edit
id: toolu_014rMPPdeyjNbMqmUKVqbmEg
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Code/@lightfastai/lightfast/db/app/src/client.ts",
  "old_string": "    return withBatchPolyfill(\n      createPostgresClient(databaseUrl),\n    ) as unknown as AppDatabase;",
  "new_string": "    return withBatchPolyfill(\n      createPostgresClient(databaseUrl)\n    ) as unknown as AppDatabase;"
}
```

> TOOL

tool_result
id: toolu_014rMPPdeyjNbMqmUKVqbmEg
```
The file /home/<USER>/Code/@lightfastai/lightfast/db/app/src/client.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01Uz9NpGFEQM1i588GbgqJPd
```json
{
  "command": "pnpm check 2>&1 | tail -20",
  "description": "Re-run Biome check"
}
```

> TOOL

tool_result
id: toolu_01Uz9NpGFEQM1i588GbgqJPd
```
> lightfast@ check /home/<USER>/Code/@lightfastai/lightfast
> npx ultracite@latest check

Checked 1117 files in 568ms. No fixes applied.
```

> TOOL

tool_use Bash
id: toolu_011iFib3MedpFycYWfRcmMsB
```json
{
  "command": "git grep -n \"withLocalBatch\\|createNeonDatabase\" 2>&1 | head -20",
  "description": "Verify old symbols fully retired"
}
```

> TOOL

tool_result
id: toolu_011iFib3MedpFycYWfRcmMsB
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_013YrjbpAhW4fP9nu68VhY3Q
```json
{
  "command": "git grep -c \"from \\\"@db/app/client\\\"\" | wc -l",
  "description": "Recount @db/app/client consumers"
}
```

> TOOL

tool_result
id: toolu_013YrjbpAhW4fP9nu68VhY3Q
```
      39
```

> TOOL

tool_use Bash
id: toolu_01F9mzcXJjRNkN1YHCsGP8i5
```json
{
  "command": "ls db/app/src/drivers/ db/app/src/polyfills/",
  "description": "Confirm new files exist"
}
```

> TOOL

tool_result
id: toolu_01F9mzcXJjRNkN1YHCsGP8i5
```
db/app/src/drivers/:
neon-http.ts
postgres.ts

db/app/src/polyfills/:
batch.ts
```

> AGENT

All automated checks pass. Now let me update the plan file to check off completed items.

> TOOL

tool_use Edit
id: toolu_01R1F3MCJN8evdHEMgrEjAu4
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Code/@lightfastai/lightfast/thoughts/shared/plans/2026-05-05-db-app-driver-polyfill-restructure.md",
  "old_string": "#### Automated Verification\n\n- [ ] `pnpm --filter @db/app typecheck` passes\n- [ ] `pnpm --filter @api/app typecheck` passes (largest consumer of `@db/app/client`)\n- [ ] `pnpm --filter @api/platform typecheck` passes (second-largest consumer)\n- [ ] `pnpm check` passes (Biome lint/format repo-wide)\n- [ ] `git grep -n \"withLocalBatch\\|createNeonDatabase\"` returns no results (old symbols fully retired)\n- [ ] `git grep -n \"from \\\"@db/app/client\\\"\"` count is unchanged from before refactor (no consumer was accidentally broken or moved)\n- [ ] New files exist: `db/app/src/drivers/neon-http.ts`, `db/app/src/drivers/postgres.ts`, `db/app/src/polyfills/batch.ts`",
  "new_string": "#### Automated Verification\n\n- [x] `pnpm --filter @db/app typecheck` passes\n- [x] `pnpm --filter @api/app typecheck` passes (largest consumer of `@db/app/client`)\n- [x] `pnpm --filter @api/platform typecheck` passes (second-largest consumer)\n- [x] `pnpm check` passes (Biome lint/format repo-wide)\n- [x] `git grep -n \"withLocalBatch\\|createNeonDatabase\"` returns no results (old symbols fully retired)\n- [x] `git grep -n \"from \\\"@db/app/client\\\"\"` count is unchanged from before refactor (no consumer was accidentally broken or moved) — 39 files, matches pre-refactor\n- [x] New files exist: `db/app/src/drivers/neon-http.ts`, `db/app/src/drivers/postgres.ts`, `db/app/src/polyfills/batch.ts`"
}
```

> TOOL

tool_result
id: toolu_01R1F3MCJN8evdHEMgrEjAu4
```
The file /home/<USER>/Code/@lightfastai/lightfast/thoughts/shared/plans/2026-05-05-db-app-driver-polyfill-restructure.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Phase 1 Complete - Ready for Manual Verification

**Automated verification passed:**
- `pnpm --filter @db/app typecheck` — clean
- `pnpm --filter @api/app typecheck` — clean
- `pnpm --filter @api/platform typecheck` — clean
- `pnpm check` (Biome) — 1117 files, no errors (one trailing-comma fix applied to `client.ts:31`)
- `git grep "withLocalBatch\|createNeonDatabase"` — empty (old symbols retired)
- `git grep "from \"@db/app/client\""` — 39 files, unchanged from pre-refactor count
- New files exist: `db/app/src/drivers/{neon-http,postgres}.ts`, `db/app/src/polyfills/batch.ts`

**Files changed:**
- `db/app/src/client.ts` (rewritten as orchestrator, 70 lines)
- `db/app/src/drivers/neon-http.ts` (new)
- `db/app/src/drivers/postgres.ts` (new)
- `db/app/src/polyfills/batch.ts` (new)

**Please perform the manual verification steps from the plan:**
- Start `pnpm dev:app` against local Docker Postgres → confirm app boots without DB connection errors (local postgres-js path).
- In a signed-in browser session, trigger an org API key rotation (calls `db.batch` at `api/app/src/router/org/org-api-keys.ts:231`) → confirm response returns a new key and old key is marked inactive (polyfill bridge still works in local dev).
- Skim the four files for the inline comments justifying each helper's location.

Let me know when manual testing is complete. This is the only phase in the plan, so once verified the work is ready to commit.
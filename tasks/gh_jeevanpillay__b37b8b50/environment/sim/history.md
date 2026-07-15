> AGENT

Plan is clear. Pre-refactor consumer count: 39 files import `@db/app/client`. I'll create the three new files and rewrite `client.ts`.

> AGENT

Now I'll rewrite `client.ts` as the orchestrator.

> AGENT

Now run the automated verification.

> AGENT

All automated checks pass. Now let me update the plan file to check off completed items.

> AGENT

Phase 1 Complete - Ready for Manual Verification **Automated verification passed:** - `pnpm --filter @db/app typecheck` — clean - `pnpm --filter @api/app typecheck` — clean - `pnpm --filter @api/platform typecheck` — clean - `pnpm check` (Biome) — 1117 files, no errors (one trailing-comma fix applied to `client.ts:31`) - `git grep "withLocalBatch\|createNeonDatabase"` — empty (old symbols retired) - `git grep "from \"@db/app/client\""` — 39 files, unchanged from pre-refactor count - New files exist: `db/app/src/drivers/{neon-http,postgres}.ts`, `db/app/src/polyfills/batch.ts` **Files changed:** - `db/app/src/client.ts` (rewritten as orchestrator, 70 lines) - `db/app/src/drivers/neon-http.ts` (new) - `db/app/src/drivers/postgres.ts` (new) - `db/app/src/polyfills/batch.ts` (new) **Please perform the manual verification steps from the plan:** - Start `pnpm dev:app` against local Docker Postgres → confirm app boots without DB connection errors (local postgres-js path). - In a signed-in browser session, trigger an org API key rotation (calls `db.batch` at `api/app/src/router/org/org-api-keys.ts:231`) → confirm response returns a new key and old key is marked inactive (polyfill bridge still works in local dev). - Skim the four files for the inline comments justifying each helper's location. Let me know when manual testing is complete. This is the only phase in the plan, so once verified the work is ready to commit.

> DEVELOPER

it worked!

> AGENT

Phase 1 (the only phase) is fully verified. Plan is complete. Want me to commit? The change set is: - `db/app/src/client.ts` (rewrite) - `db/app/src/drivers/neon-http.ts` (new) - `db/app/src/drivers/postgres.ts` (new) - `db/app/src/polyfills/batch.ts` (new) - `thoughts/shared/plans/2026-05-05-db-app-driver-polyfill-restructure.md` (checkboxes)

> DEVELOPER

perfect! is there any consumers we need to fix?

> AGENT

No consumers need fixing. Every one of the 36 code consumers imports only `db` — none reach for the internal symbols (`createNeonDatabase`, `withLocalBatch`, etc.) that were removed/renamed. The public `db` and `createClient` exports are byte-identical in shape to before, so the refactor is fully transparent to callers. Both `pnpm --filter @api/app typecheck` and `pnpm --filter @api/platform typecheck` already validated this end-to-end (those two cover ~33 of the 36 import sites).

> DEVELOPER

if all good /commit then

> AGENT

Plan: one commit covering the refactor + the plan file. Skipping all other dirty/untracked files since they're unrelated. **Files to add:** - `db/app/src/client.ts` (modified) - `db/app/src/drivers/neon-http.ts` (new) - `db/app/src/drivers/postgres.ts` (new) - `db/app/src/polyfills/batch.ts` (new) - `thoughts/shared/plans/2026-05-05-db-app-driver-polyfill-restructure.md` (new) **Commit message:** ``` refactor(db/app): split client into drivers + batch polyfill Reorganize db/app/src/client.ts so each concern lives in its own file: drivers/neon-http.ts owns the prod neon-http driver (and its global neonConfig side-effect), drivers/postgres.ts owns the local postgres-js driver, polyfills/batch.ts owns the .batch() shim that bridges postgres-js to the neon-http surface. client.ts becomes a thin orchestrator that picks a driver from env and applies the polyfill. Pure refactor — no behavior change and no public API change. The @db/app/client subpath still exports db and createClient with identical shapes, and all 36 consumers continue to compile unchanged. ``` Shall I proceed?
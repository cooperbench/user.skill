> DEVELOPER

what's pending?

> AGENT

All 5 milestone phases checked off in `MILESTONE.md`. Real pending stuff: **Uncommitted:** - `PONYTAIL-DEBT.md` — untracked (44 debt markers logged, 23 no-trigger) - `graphify-out/` — untracked **Actual open work (from debt ledger, no upgrade trigger set — could rot):** - `composeSQL` naive — single/linear pipes only, no multi-node support - params tracked on endpoint node only, upstream nodes report empty - `Schedule`/`COPY_SCHEDULE` parsed but not executed — no in-process scheduler, no `/v0/jobs` surface (gap #8) - rate limit: global only, no per-pipe override, in-memory not Redis-backed (ADR 0015/0031) - sqlproxy readonly via query flag, not server-side profile (ADR 0011) Want me to commit the debt ledger, or dig into one of these gaps?

> DEVELOPER

yes and pick up the high priority one

> AGENT

Now adding the `JobRecord`/`JobStore` contract to model.go:

> AGENT

Need to add the `time` import to model.go:

> AGENT

Now the `internal/job` package (Redis-backed store):

> AGENT

Now wire `Executor` to persist a record on successful copy:

> AGENT

Now update `Executor` in `internal/pipe/executor.go`:

> AGENT

Now update `copyJobBody` to take `id` instead of generating it internally:

> AGENT

Now build to catch remaining issues:

> AGENT

Now add the API layer:

> AGENT

Now wire `Deps.Jobs` and the routes in `server.go`:

> AGENT

Good — inside the bearer-authed `/v0` block, right before the inner OpenAPI route. Now `gofmt` the jobs.go struct alignment and run vet:

> AGENT

gofmt fixed alignment. Now wire `cmd/tinyraven/serve.go`:

> AGENT

Wired correctly. Now full build + vet + test:

> AGENT

Builds clean. Now write tests. First, the `internal/job` package:

> AGENT

Compiles fine (that diagnostic is just gopls not using the integration tag). Now check Redis availability to actually run it:

> AGENT

Redis is up locally. Run the new integration test:

> AGENT

Now the API-layer unit tests. Let's check `pipes_test.go` for the fake-dependency pattern:

> AGENT

Now write `internal/api/jobs_test.go`:

> AGENT

All pass. Now the `internal/pipe` package — verify `EnableJobs`/RunCopy persistence with a fake JobStore:

> AGENT

Full non-integration suite green. Now the integration tag build + run:

> AGENT

Now build a minimal scratch project and run a real live end-to-end probe of the new endpoints:

> AGENT

Still running (nohup survives). Let's check readiness and hit `/v0/jobs` with the real Redis-backed store, then seed a job directly via Redis and verify GET:

> AGENT

Real HTTP round-trip already works. Now seed a job via the actual Redis-backed store and verify GET:

> AGENT

Now update docs to reflect the closed gap. First `docs/parity-gaps.md`:

> AGENT

Now update `PONYTAIL-DEBT.md` entries that referenced gap #8 as fully deferred:

> AGENT

Now update the debt ledger entries to reflect reality:

> AGENT

Line unchanged (my addition was later in the file). Update its ledger entry to reflect the closed GET-side gap:

> AGENT

Now fix the tail summary note and marker count (I closed 2 no-trigger-adjacent markers, and the total marker count may have shifted):

> AGENT

This is part of the "frozen /v0 surface" that should stay in parity. Add jobs paths:

> AGENT

This is a "contains" check, not exhaustive — no update needed, but I'll add `/v0/jobs` and `/v0/jobs/{id}` to the assertion list for coverage:

> AGENT

All green. Now let's finalize the ledger/git-add task and review the full diff before committing:

> AGENT

Now let's stage and review everything before committing:

> AGENT

`graphify-out/` correctly excluded. Let's diff the whole set once more for sanity:

> AGENT

Two logical commits: the debt ledger + gitignore is separate from the jobs-surface feature. Let's split them:

> AGENT

Now the jobs-surface feature commit:

> AGENT

🗂️ LEARNING INVENTORY: 🗂️ Forge unavailable in this env (no codex binary) — reconfirmed prior memory | TYPE: knowledge | KEEP: no — already captured in `[[parallel-agent-orchestration]]` 🗂️ ClickHouse via colima was flaky mid-session (docker socket) — transient, not project state | TYPE: state | KEEP: no — infra noise, not durable 📄 DOC SYNC: 0 PAI system files changed → SKIP 🔄 RE-READ: 🔄 "yes" (commit debt ledger + graphify handling): ✓ addressed — `PONYTAIL-DEBT.md` committed, `graphify-out/` gitignored 🔄 "pick up the high priority one" (gap #8 jobs surface): ✓ addressed — `GET /v0/jobs` + `/v0/jobs/{id}` implemented, tested, live-curl-verified ━━━ 📃 SUMMARY ━━━ 7/7 📃 CONTENT: 2 commits on `main`. (1) `737d42a` — `PONYTAIL-DEBT.md` (44 markers, 23 no-trigger) + `graphify-out/` gitignored. (2) `7521c13` — gap #8: Redis-backed `internal/job.Store` (24h TTL, sorted-set recency index), wired via `Executor.EnableJobs` into `RunCopy`, `GET /v0/jobs`/`GET /v0/jobs/{id}` scope-filtered by `APPEND:<target>`/ADMIN, OpenAPI spec + Postman collection updated. Verified: full unit+integration suite green, live curl round-trip against real Redis (list/get/404/401 all correct). Known delta: only copy-triggered (already-terminal) jobs — `COPY_SCHEDULE` auto-exec and batch-import (gap #6) still need a real scheduler, documented in both debt docs. 🖊️ STORY: Debt was invisible, now it's a ledger. Gap #8's dead […]
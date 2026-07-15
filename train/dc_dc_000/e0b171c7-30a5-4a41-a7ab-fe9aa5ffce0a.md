---
session_id: e0b171c7-30a5-4a41-a7ab-fe9aa5ffce0a
developer: "dc:dc_000"
split: train
source: dataclaw
repo: peteromallet/my-dataclaw-data
start_time: "2026-05-13T14:00:08.174Z"
n_turns: 10
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Execute the approved plan in the repository. Project directory: /Users/user_c042661f/Documents/reigh-workspace Idea: # Brief: stop the cross-boundary contract bleeding [all-codex/standard +prep] ## Background and goal Reigh is a production AI/ML task system split across three independently deployed surfaces speaking an implicit wire-level protocol with no contract definition, no codegen, no version negotiation. In one debugging session today the team hit three different flavors of the same class of bug — each one an *asymmetric contract evolution* that produced silent runtime failures. This is the fourth documented recurrence in five months; the same engineer has now introduced and silently broken the same `ready_for_tasks` contract twice, four months apart. Goal of this sprint: ship a coherent set of guardrails that make this class of bug **structurally loud** (and in two specific places, structurally impossible). Not perfect prevention. Bleeding stopped, recurrence cost capped, future change shapes safer. The fix is being shipped at runtime via the existing Postgres surface plus a small operational sentinel — explicitly NOT via a build-time codegen contracts package. That package may be the right end state in 6+ months; it is the wrong first move for one solo engineer in feature-shipping mode. Stop the bleeding first; centralize at the layer that already has a chokepoint; defer the perfect-protocol design. ## System under change Three repos in `/Users/user_c042661f/Documents/reigh-workspace/`: - **`reigh-app/`** — TypeScript. Supabase edge functions, DB migrations, frontend. - **`reigh-worker/`** — Python. Runs on RunPod GPU pods. Pulls `origin/main` at pod startup. - **`reigh-worker-orchestrator/`** — Python. Deployed on Railway from `megaplan/vibecomfy-sprint-07-orchestrator-pools-artifacts` branch. Database is Postgres on Supabase. Project ref `wczysqzxlwdndgxitrvc`. [REDACTED]: - `public.tasks` (rows have `route_key` column + `params` JSONB containing `route_contract` object) - `public.workers` - `public.route_backend_capabilities` (registry of what backends support which route_keys) - `public.route_backend_selectors` - RPCs: `claim_next_task_service_role`, `route_backend_claim_decision`, `count_queued_tasks_breakdown_service_role`, `derive_route_key` (does not yet exist; this sprint adds it) Live workers and orchestrator are running in production *right now*. [REDACTED]'s task chain (`0168dcc3-2a42-415d-84b5-a28cf6033850` + 6 children) is failed and poisoned with mismatched parent_route_key references — it stays Failed; don't try to revive it. ## The three bugs that defined the diagnosis 1. **Cross-repo deployment skew.** Orchestrator required `metadata.ready_for_tasks=true` for worker promotion. Worker-side publishing code sat in 169 unpushed commits on a feature branch. Production pods ran 8-day-old code, sat in `spawning` forever (heartbeat-guardian subprocess kept the DB row warm while the main process was dead), $0.69/hr × 18h = ~$12.75 of idle compute burned. The orchestrator's stuck-spawning detector existed […]

> AGENT

Acknowledging the new live-test skill — not invoking it for this task. Let me locate the actual `_route_contract` function.

> AGENT

Now I have enough context. Let me make the matrix.py edit:

> AGENT

Now create the parity test:

> AGENT

Now verify the parity test against live DB:

> AGENT

The venv lacks `supabase` module. Let me verify the hand-table values against the live DB function via psql instead:

> AGENT

One hand-table entry was wrong (wan22_vace guidance). Let me correct it to match the DB:

> AGENT

Unrelated pre-existing logging bug. Now run the new parity test:

> AGENT

All 7 parity cases pass; 126/127 in the broader live_test primitives suite (1 unrelated pre-existing logger bug). Writing checkpoint:

> AGENT

T12 complete. Bounded RPC swap landed in `matrix.py:_route_contract` (route_key now sourced via `supabase.rpc('derive_route_key', ...)`; surrounding 9 mirror fields untouched per SC12); new parity test at `scripts/live_test/tests/test_route_contract_parity.py` covers all 7 cases against the live DB (7/7 pass). Broader live_test suite: 126/127 (1 unrelated pre-existing logger bug in variant_update.py).

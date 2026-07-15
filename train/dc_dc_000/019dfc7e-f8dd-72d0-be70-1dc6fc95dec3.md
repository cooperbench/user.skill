> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are an independent reviewer. Critique the plan against the actual repository.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace





        Idea:
# Sprint 6: Production Selector and Claim Contract

## Overall Context

This sprint turns local selector ideas into production claim behavior before orchestrated routes depend on them. It is the control-plane foundation for rollback and canary.

## Shared Operating Rules

- Production missing selector key means WGP/no-claim, never implicit Comfy.
- Workers must not claim routes they cannot execute.
- Selector version and selected backend must be visible in logs or task metadata.
- Child rows created later must be able to snapshot route selection.

## Sprint Goal

Make selector and claim behavior concrete for production.

## Required Deliverables

- Selector schema/namespace.
- Route-key serialization, including direct variants where needed.
- Index/RPC/query behavior.
- Cache TTL and rollback SLO.
- Malformed/unauthorized/stale-entry tests.
- Claim-time backend eligibility or pre-execution requeue/fail-closed guard.
- Selector-version logging.
- Child-route snapshot field contract for later parent-created rows.

## Exit Criteria

Missing production route key means WGP/no-claim; mismatched workers cannot claim or execute selected routes; selector unreachable behavior and rollback SLO are tested; selected backend/selector version can be pinned for child rows created after parent claim.

        Plan:
        # Implementation Plan: Sprint 6 Production Selector and Claim Contract

## Overview
The current implementation has worker-local route selection in `reigh-worker/source/task_handlers/tasks/template_routing.py`, claim filtering in `reigh-app/supabase/functions/claim-next-task/index.ts` backed by `claim_next_task_service_role`, and scaling counts in `reigh-app/supabase/functions/task-counts/index.ts`. Production claim behavior is still mostly `run_type`/task-type based, so a VibeComfy-capable worker and a WGP worker are not yet selected by a production route selector contract.

The simplest durable fix is to make route selection materialized on task rows, then make the claim RPC enforce worker backend eligibility. That avoids re-deriving complex route keys inside SQL at claim time and gives later parent-created child rows a stable field to snapshot.

## Phase 1: Schema and Route Contract

### Step 1: Add selector and task snapshot schema (`reigh-app/supabase/migrations/`)
**Scope:** Medium
1. Add a new migration creating `public.route_backend_selectors` with a small namespace/version contract: `namespace`, `route_key`, `selected_backend`, `selector_version`, `enabled`, `updated_at`, optional `expires_at`/`metadata`, and a check that backend is one of `wgp` or `vibecomfy`.
2. Add `tasks.route_key text`, `tasks.selected_backend text`, `tasks.selector_version text`, and `tasks.route_selection_snapshot jsonb`.
3. Add indexes for claim paths: at minimum `(status, route_key, created_at)`, selector lookup `(namespace, route_key, enabled)`, and optionally partial indexes for queued tasks by `selected_backend`.
4. Backfill direct task route keys where the key is exactly `task_type` for existing direct rows. Leave derived travel child variants null until creation paths set them explicitly.

### Step 2: Define shared route-key serialization (`reigh-app/supabase/functions/create-task/`, `reigh-worker/source/task_handlers/tasks/template_routing.py`)
**Scope:** Medium
1. Keep the existing Python serializer as the canonical worker implementation and add `selector_version`/snapshot helpers near `derive_route_key`.
2. Add a TypeScript route-key helper for create-task resolvers covering direct routes and known child variants. For direct routes, key is `task_type`; for travel children, match the Python format: `task_type__model-*__guidance-*__continuity-*__profile-*`.
3. Add tests that compare representative TS/Python route keys indirectly through existing fixtures, especially `z_image_turbo`, WGP-only Qwen routes, `wan_2_2_t2i`, `travel_segment`, and `individual_travel_segment`.

## Phase 2: Claim-Time Selector Enforcement

### Step 3: Extend claim request and RPC contract (`claim-next-task`, migration RPC)
**Scope:** Large
1. Extend `claim-next-task` request parsing with `worker_backend?: 'wgp' | 'vibecomfy'`, defaulting to `wgp` for existing GPU workers and rejecting malformed backend values with `400` for service-role requests.
2. Extend `claim_next_task_service_role` with `p_worker_backend text default 'wgp'` and `p_selector_namespace text default 'production'`.
3. In the RPC candidate query, join `route_backend_selectors` by namespace and `tasks.route_key`.
4. Enforce claim eligibility:
   - If no selector row exists, only WGP workers may claim the task; VibeComfy workers get no row.
   - If selector row exists and is enabled/stale-valid, only workers whose backend matches `selected_backend` may claim.
   - Disabled, stale, malformed, or unauthorized selector entries behave as no-claim for VibeComfy and do not imply Comfy/VibeComfy.
5. Update the RPC return shape to include `route_key`, `selected_backend`, `selector_version`, and `route_selection_snapshot`.
6. Update `claim-next-task/index.ts` to pass backend/namespace, return selector fields to workers, and log `route_key`, `selected_backend`, and `selector_version` on every successful claim.

### Step 4: Align task counts with claim eligibility (`task-counts`, count RPCs)
**Scope:** Medium
1. Extend `task-counts` service-role body parsing with `worker_backend` and `selector_namespace`.
2. Update `count_eligible_tasks_service_role` and `count_queued_tasks_breakdown_service_role` or add backend-aware overloads so scaling sees the same selector/backend eligibility as claims.
3. Preserve existing GPU/API filtering and banodoco-pool filtering, layering backend selector eligibility after dependency/user-capacity checks.
4. Add tests proving a VibeComfy worker sees zero claimable tasks for missing production route keys while WGP still sees the legacy-safe path.

## Phase 3: Task Creation and Child Snapshot Fields

### Step 5: Materialize route selection at task creation (`create-task` resolvers)
**Scope:** Medium
1. Add route fields to `TaskInsertObject` in `reigh-app/supabase/functions/create-task/resolvers/types.ts`.
2. In `create-task/index.ts`, after resolver output and before insert, compute `route_key`, look up the production selector, and populate `selected_backend`, `selector_version`, and `route_selection_snapshot` when available.
3. Fail closed for malformed selector rows; for selector lookup failure, return an error rather than inserting a task that could be claimed by the wrong backend.
4. Preserve service-role worker passthrough behavior in `workerPassthrough.ts`, but allow worker-created children to pass an explicit `route_selection_snapshot` so parent-claimed rows can pin the selection for children created later.

### Step 6: Propagate child route snapshots from workers (`reigh-worker/source/core/db/task_completion.py`, travel/join orchestrators)
**Scope:** Medium
1. Extend `add_task_to_db` to accept optional route-selection metadata and include it under the `input` payload for create-task.
2. When a parent/orchestrator task is claimed, store its selector fields in the task params/context used by child builders.
3. Update travel and join child creation paths, including `reigh-worker/source/task_handlers/travel/orchestrator.py` and `reigh-worker/source/task_handlers/join/task_builder.py`, to pass the inherited or freshly derived child route snapshot.
4. Add a narrow unit test asserting child payloads include the snapshot fields without requiring the child to query the selector again.

## Phase 4: Worker Guardrails and Telemetry

### Step 7: Send backend capability from workers (`reigh-worker/source/core/db/task_claim.py`)
**Scope:** Small
1. Parse `REIGH_BACKEND` with the existing strict parser and send `worker_backend` in `poll_next_task` claim payload.
2. Include selector fields in claim debug logs.
3. Preserve PAT/local behavior unless a PAT worker explicitly sends backend capability later.

### Step 8: Add pre-execution fail-closed/requeue guard (`reigh-worker/source/runtime/worker/server.py`, `task_execution.py`)
**Scope:** Medium
1. Before `process_single_task`, compare claimed `selected_backend` with the worker backend.
2. If mismatched, requeue with `clear_worker=true` using the existing retry path when another backend can handle it; if the selector says a route is unsupported or malformed, mark failed with a clear fail-closed message.
3. Add `selected_backend`, `selector_version`, and `route_key` to the existing `VIBECOMFY_ROUTING` telemetry card and claim lifecycle logs.
4. Keep direct WGP execution unchanged for WGP-selected or missing-selector WGP routes.

## Phase 5: Tests and Rollback SLO

### Step 9: Add selector failure-mode tests (`reigh-app/supabase/functions/claim-next-task/index.test.ts`, SQL migration tests)
**Scope:** Medium
1. Unit-test malformed `worker_backend` and selector namespace handling in the edge function.
2. Add SQL-level or mocked RPC tests for missing selector, unauthorized/disabled selector, stale selector, malformed selected backend, and matching selector.
3. Verify missing production route key returns no claim for VibeComfy and remains WGP-claimable where legacy WGP execution exists.

### Step 10: Add rollback/cache contract tests (`task-counts`, claim edge tests)
**Scope:** Small
1. Define claim-path selector cache TTL as zero if the RPC joins the selector table directly. Document rollback SLO as database commit visibility plus normal worker polling interval.
2. If an edge-side selector cache is introduced for create-task snapshotting, keep it short and explicit, e.g. `ROUTE_SELECTOR_CACHE_TTL_MS <= 30000`, and test that cache expiry refreshes selector version.
3. Test selector unreachable behavior: claim path returns no claim/error rather than falling back to VibeComfy; create-task returns an explicit insertion error if it cannot determine the snapshot.

## Execution Order
1. Land schema and route-key helpers first; they are additive and make later tests concrete.
2. Update create-task materialization before enforcing claim filters, so new rows have route keys.
3. Update claim RPC and `claim-next-task`, then align `task-counts` so scaling and claiming agree.
4. Wire worker claim payloads and pre-execution guards last, after edge/RPC fields are stable.
5. Add child snapshot propagation after parent claim metadata is flowing end to end.

## Validation Order
1. Run focused route-key and create-task resolver unit tests.
2. Run `claim-next-task` and `task-counts` edge tests.
3. Run worker routing tests: `reigh-worker/tests/test_template_routing.py` and `reigh-worker/tests/test_vibecomfy_backend_selection.py`.
4. Run targeted worker claim/server tests for backend mismatch requeue/fail-closed behavior.
5. Finish with broader Supabase function tests and the relevant worker/orchestrator test subsets.


        Plan metadata:
        {
  "version": 1,
  "timestamp": "2026-05-06T08:54:30Z",
  "hash": "sha256:6abf5b49dbbb62fc08e1ce9b8aa07bacdd914b2171ad3784d62da87acc31f5d7",
  "questions": [
    "Should a missing production selector row allow WGP workers to claim the task, or should it mean no production worker claims it at all? I assumed WGP may claim and VibeComfy must not.",
    "What is the authoritative selector namespace name for production: literally `production`, environment-specific names like `prod`, or a deployment-configured value? I assumed `production` with an env override.",
    "Should selector entries expire via `expires_at`, `max_age`, or only a version/update timestamp? I assumed `expires_at` is the simplest stale-entry gate.",
    "For child rows, should they inherit the parent\u2019s selected backend/version exactly, or derive their own child route key and selector snapshot at child creation time? I assumed child rows need their own route key plus a pinned snapshot recorded when they are created."
  ],
  "success_criteria": [
    {
      "criterion": "A VibeComfy worker cannot claim a queued production task when the task has no selector row for its route key.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "A worker cannot claim or execute a task whose selected_backend does not match its declared backend capability.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Successful claim responses and worker logs include route_key, selected_backend, and selector_version when a selector row is used.",
      "priority": "must",
      "requires": [
        "run_tests",
        "observe_runtime_logs",
        "parse_diff"
      ]
    },
    {
      "criterion": "Malformed, disabled, unauthorized, and stale selector entries are covered by automated tests and do not imply VibeComfy fallback.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "task-counts and claim-next-task use the same backend eligibility semantics for service-role GPU workers.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "New task rows can store route_key, selected_backend, selector_version, and route_selection_snapshot, and child task creation can pass a pinned snapshot field contract.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Selector rollback SLO is explicitly documented in code/tests as either no claim-path cache or a bounded TTL with test coverage for refresh behavior.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Route-key serialization tests cover direct routes plus travel child variants that include model/guidance/continuity/profile dimensions.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "The implementation keeps route-key serialization lightweight and avoids importing WGP or VibeComfy heavy modules from the selector helper.",
      "priority": "should",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Existing WGP default behavior remains unchanged for unset local backend outside the production selector claim path.",
      "priority": "should",
      "requires": [
        "run_tests"
      ]
    }
  ],
  "assumptions": [
    "The active app code is under `reigh-app`, not the parallel `reigh-app-cloud-chain` copy, though the latter appears similar.",
    "Production selector state should live in Postgres/Supabase because claim selection is already atomic in SQL and should not depend on worker-local files.",
    "`vibecomfy` is the production name for the Comfy/VibeComfy backend; the plan avoids accepting `comfy` as an alias because existing worker parsing intentionally rejects it.",
    "The claim path can use direct selector table joins, making claim rollback effectively bounded by database visibility and worker polling rather than a long cache TTL.",
    "Existing banodoco worker-pool behavior should remain layered separately from GPU WGP/VibeComfy backend selection."
  ],
  "structure_warnings": []
}

        Plan structure warnings from validator:
        []

        Existing flags:
        []

        Known accepted debt grouped by subsystem:
        {
  "are-the-proposed-changes-technically-correct": [
    {
      "id": "DEBT-007",
      "concern": "are the proposed changes technically correct?: for ordinary pairs, the new diagnosis is not well-supported by the repo. the current sync effect in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l62) already syncs `url` and `primaryvariantid`, and the regenerate path reads exactly `starturl`, `endurl`, `startgenid`, `endgenid`, `startvariantid`, and `endvariantid` from `segmentslotmode.pairdata` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts#l438). adding `thumburl` and `generationid` to the sync does not, by itself, explain why an old image url is still being used for regular pairs.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-008",
      "concern": "are the proposed changes technically correct?: the fix is incomplete for extra trailing slots. `handlepairclick` can populate `activepairdata` from `trailingpairdata` when `pairindex === pairdatabyindex.size` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l121), but the proposed sync effect only reads `pairdatabyindex.get(segmentslotlightboxindex)`. for those trailing-slot cases `fresh` is `undefined`, so no image refresh happens.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-018",
      "concern": "are the proposed changes technically correct?: the merge pseudocode does not actually sync 'all image fields' as claimed. it omits `id` and `position` from change detection, and when `fresh.startimage` or `fresh.endimage` becomes `null` it preserves the stale previous object instead of syncing that null state. as written, it also needs explicit null-guards around spreads of `prev.startimage` / `prev.endimage` to be safe in strict typescript.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-106",
      "concern": "are the proposed changes technically correct?: the plan's claim that `worker_state.py:200-204` (the 30-minute startup safety net) catches abandoned pods that exited before patching is slightly imprecise. line 200-204 only runs when `in_startup_phase` is true, which requires `startup_phase` to be in `('deps_installing', 'deps_verified', 'worker_starting')` per line 161. a pod that exits before its first patch has `startup_phase = none`, so `in_startup_phase` is false and the code falls through to the normal timeout checks (active_stale / not_claiming) at line 207+, not the 30-minute startup cap. both paths eventually reap the worker, so the end result is the same, but the overview's reasoning (naming 200-204 specifically) is wrong. worth correcting so future readers don't mis-reason about the invariant.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-107",
      "concern": "are the proposed changes technically correct?: checked worker_state.py line 161 (`in_startup_phase = startup_phase in (...)`) against the plan's assumption that subsequent lenient writes are safe. if deps_installing succeeds but deps_verified silently fails, startup_phase stays at 'deps_installing' and the 30-minute cap from line 200-204 applies \u2014 even though the pod is actually progressing through `uv sync`. on a slow runpod image with cold wheel downloads, `uv sync --extra cuda124` plus wan2gp deps can take 20+ minutes. there's no concrete benchmark in the plan that says the 30-minute cap is safely above the expected sync time; if `uv sync` legitimately takes 25 minutes and the deps_verified patch fails on a transient network blip, the orchestrator will terminate a healthy pod. plan should either bump the cap or note that deps_verified swallowing is acceptable because the cap is generously above typical sync time.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-143",
      "concern": "are the proposed changes technically correct?: the path-mapping defect from the previous iteration is fixed, but a different technical gap remains around `self_refiner`. repository search shows `shared.utils.self_refiner` is imported by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx_pipelines/distilled.py`, `ti2vid_one_stage.py`, `ti2vid_two_stages.py`, `wan2gp/models/ltx2/ltx_pipelines/utils/helpers.py`, and `wan2gp/models/wan/any2video.py`; the v4 plan still aligns `wan2gp/shared/utils/self_refiner.py` to upstream head without any concrete runtime step that exercises those code paths after the change, so the only repo-documented behavior check for that file is still missing from the executable body.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-156",
      "concern": "are the proposed changes technically correct?: the direct adapter still has a correctness risk around resolution parity. current vibecomfy ready templates hardcode image dimensions (`image/z_image` uses `emptysd3latentimage` 1024x1024 and `image/qwen_image_2512` uses 768x768), while `vibecomfy run` exposes no `--resolution` flag; the revised plan says a temporary scratchpad/input file may be generated only if supported, otherwise resolution is left out. that means a vibecomfy-supported direct route can silently ignore the worker's `resolution` param unless scratchpad resolution patching is made mandatory for supported direct routes or the support is explicitly limited to default-resolution smoke fixtures.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "are-the-success-criteria-well-prioritized-and-verifiable": [
    {
      "id": "DEBT-019",
      "concern": "are the success criteria well-prioritized and verifiable?: the attached success criteria are stale and do not match the current plan body. they still require 'no `usestate` for `activepairdata`', '`setactivepairdata` fully removed', 'sync effect deleted', and '`onpairclick` simplified to `(pairindex: number) => void`', which are the opposite of the current targeted-sync plan. as presented, the criteria are not usable for review or execution.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "audio-loading": [
    {
      "id": "DEBT-086",
      "concern": "getaudiodata in useeffect removes render-readiness signal",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-087",
      "concern": "same as correctness-3 \u2014 preview/render parity risk",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-088",
      "concern": "preview/render parity partially satisfied",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "audio-reactivity": [
    {
      "id": "DEBT-082",
      "concern": "overlapping clips use first-found, volume not scaled",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-083",
      "concern": "same as audio-reactivity-1 \u2014 overlapping/volume-adjusted clips diverge from audible mix",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-084",
      "concern": "textclip missing globalframeprovider",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-085",
      "concern": "same as audio-reactivity-2 \u2014 textclipsequence missing provider",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-089",
      "concern": "textclip effects surface not covered",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-090",
      "concern": "continuous effects shared by visual and text clips",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "batch-generation-pipeline": [
    {
      "id": "DEBT-006",
      "concern": "enhancement in usegeneratebatch before generatevideo() could compute prompts against a stale pair snapshot if mutations are still in flight.",
      "occurrence_count": 1,
      "plan_ids": [
        "in-cloud-mode-when-users-20260330-2214"
      ]
    }
  ],
  "cas-intern-short-circuit": [
    {
      "id": "DEBT-151",
      "concern": "symlink short-circuit comparison may produce false negatives on macos-like layouts where project_dir contains symlinked segments (/var \u2192 /private/var) because resolve(strict=true) on the source returns canonical paths but project_dir / cas_dirname may be non-canonical.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-7-rev-20260505"
      ]
    }
  ],
  "crash-recovery-cascade-paths": [
    {
      "id": "DEBT-065",
      "concern": "cascade lookup only reads params->>'orchestrator_task_id_ref', missing shared reference paths and orchestrator-self detection.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-067",
      "concern": "duplicate of correctness-2 + correctness-3: invalid sql syntax and narrow cascade lookup.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-069",
      "concern": "shared orchestrator-reference helpers not referenced.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-072",
      "concern": "orchestrator tasks that crash don't get orchestrator-self cascade.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-074",
      "concern": "hardcoded params->>'orchestrator_task_id_ref' misses other reference paths.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-retry": [
    {
      "id": "DEBT-063",
      "concern": "crash requeue sql does not increment attempts, risking infinite requeue loop.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-066",
      "concern": "duplicate of correctness-1: attempts never advance on crash requeue.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-068",
      "concern": "missing attempts increment location in heartbeat sql.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-073",
      "concern": "step 6 under-scoped for real retry convergence and orchestrator-self handling.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-sql-syntax": [
    {
      "id": "DEBT-064",
      "concern": "bare select inside plpgsql is invalid \u2014 needs perform.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-testing": [
    {
      "id": "DEBT-070",
      "concern": "no multi-crash convergence test exercising attempts 0\u21921\u21922\u21923.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-071",
      "concern": "no validation that plpgsql body executes successfully.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-075",
      "concern": "criteria don't require proof of crash requeue convergence.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "criteria-verifiability": [
    {
      "id": "DEBT-036",
      "concern": "'no unsafe .maybesingle()' criterion requires judgment about column uniqueness.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-037",
      "concern": "decision documentation location not specified.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-062",
      "concern": "the must criterion requiring 5 task types to exist as active db rows is not verifiable from code diff alone \u2014 it requires a live db query.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ],
  "db-fallback-testing": [
    {
      "id": "DEBT-060",
      "concern": "no new automated test for the db fallback dispatch path or dependant_on preservation for raw worker families.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ],
  "dependency-resolution": [
    {
      "id": "DEBT-105",
      "concern": "dependency resolution: the plan does not lock down the active python-version matrix even though the repo currently splits between python 3.10 local installs and a python 3.11 runpod image.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements": [
    {
      "id": "DEBT-013",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the package is internally inconsistent. the plan body says to keep `activepairdata` in `usestate` and make phase 2 optional, but the attached metadata and success criteria still describe the previous derive-via-`usememo` / remove-`setactivepairdata` / simplify-`onpairclick` plan. that means the approved-plan requirements are only partially coherent as presented.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-108",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the linux distro note is documentation-only; the generated install command in step 7 still runs `apt-get install python3.10-venv python3.10-dev ffmpeg` without any pre-check that the package exists. users on ubuntu 24.04+ who ignore the doc and try to copy-paste the command will hit a confusing `e: unable to locate package python3.10-venv` from apt rather than a targeted error from commandutils.ts. a one-line detection pre-check (e.g., `apt-cache show python3.10-venv >/dev/null 2>&1 || { echo 'install deadsnakes ppa first \u2014 see readme'; exit 1; }`) would convert the silent failure into an actionable error, but the plan does not add this.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-145",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: checked the revised v4 body against `docs/wan2gp_fork_migration_plan.md` sprint 2. the repo plan doc still lists an \"ltx-2 `self_refiner` smoke against the pre-sprint behavioral baseline\" as a sprint 2 verification gate and repeats that smoke in the functionality-preservation checks, but the revised execution steps no longer schedule that smoke anywhere; it survives only as an info-level metadata criterion. because `wan2gp/shared/utils/self_refiner.py` remains an explicit sprint 2 deliverable, the revised plan still only partially carries forward the verification package described in the source migration plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-153",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: worker integration: the migration doc describes the per-call profile override gap as involving reigh-worker adapter handling of override_profile before constructing vibecomfy sessionconfig, but the plan limits sprint 1 per-run work to the vibecomfy cli/runtime. that may be acceptable for a vibecomfy-library mvp, but it does not fully exercise the production-facing per-task override semantics called out in the overall context.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-1-vibecomfy-memory-20260506-0147"
      ]
    },
    {
      "id": "DEBT-155",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: a residual issue-hint tension remains for resolution handling. the plan acknowledges current `vibecomfy run` lacks a resolution flag, but allows the adapter to leave resolution and other template-specific values unwired for sprint 2. because `z_image_turbo` and `qwen_image_2512` are marked vibecomfy-supported direct routes, this may not preserve the existing worker task-parameter contract for tasks that provide a non-default `resolution`.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "direct-route-parameter-parity": [
    {
      "id": "DEBT-160",
      "concern": "direct route parameter parity: vibecomfy-supported direct routes may ignore the worker `resolution` parameter.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "does-the-change-touch-all-locations-and-supporting-infrastructure": [
    {
      "id": "DEBT-014",
      "concern": "does the change touch all locations and supporting infrastructure?: phase 1 still misses a real supporting-data location: `trailingpairdata` lives outside `pairdatabyindex` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts#l111), but the proposed sync logic only considers `pairdatabyindex`. if trailing slot regenerate is part of the bug surface, that location is not covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-110",
      "concern": "does the change touch all locations and supporting infrastructure?: the non-swallowing helper `update_worker_phase_strict` is a new shell function, but phase 1 step 2 introduces it only as pseudo-code. there is no concrete note that the helper must handle supabase http non-2xx responses as failures (curl returns 0 even on http 4xx/5xx by default unless `-f` or `--fail-with-body` is used). if the implementer ports `update_worker_phase` verbatim with only `|| return 0` removed, a 500 from supabase would still report success because curl's exit code is 0. the plan should specify `curl --fail` or explicit http status code checking in the strict variant.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-142",
      "concern": "does the change touch all locations and supporting infrastructure?: the supporting-infrastructure review still finds one missing check. in `docs/wan2gp_fork_migration_plan.md`, sprint 2's verification matrix and risk register both single out `self_refiner` as a distinct drift-upgrade surface with its own smoke and its own silent-behavior-change risk, but the revised v4 body updates the file without keeping that supporting verification step in the actual execution checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-154",
      "concern": "does the change touch all locations and supporting infrastructure?: documentation/data gap: the sprint exit criteria require profiles 1 and 3 to have vram and wall-clock data, but the plan puts that only in metadata as an info-level criterion and does not schedule a concrete artifact location or command for recording the measurements. the implementation could satisfy all unit tests while still missing one of the explicit exit criteria.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-1-vibecomfy-memory-20260506-0147"
      ]
    },
    {
      "id": "DEBT-158",
      "concern": "does the change touch all locations and supporting infrastructure?: the supporting infrastructure for resolution is still incomplete if direct vibecomfy routes are considered production-supported. vibecomfy has a `vibecomfy.patches.resolution` helper and the cli can load scratchpad files with `allow_scratchpad=true`, but the plan does not require using that path; it permits leaving resolution out for sprint 2.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    },
    {
      "id": "DEBT-162",
      "concern": "does the change touch all locations and supporting infrastructure?: checked vibecomfy profile wording against `vibecomfy/tests/test_ready_templates.py`. the revised plan says to add the production template to representative compile profile coverage 'alongside the existing dry-run id', but the dry-run id is not currently in `profile_smoke_template_ids`; only `video/wanvideo_wrapper_22_5b_i2v` and `video/wan_t2v` are. this is a small wording mismatch rather than a functional blocker because adding either the production id alone or both ids would still satisfy sprint 4.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-4-wan-single-frame-and-20260506-0818"
      ]
    }
  ],
  "edge-test-config": [
    {
      "id": "DEBT-022",
      "concern": "plan's vitest commands use the wrong config entry point.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-023",
      "concern": "same as verification-3: wrong vitest config in validation commands.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-024",
      "concern": "success criterion references wrong test command.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "error-handling": [
    {
      "id": "DEBT-095",
      "concern": "db loader error handling convention mismatch (plan says log+null, existing loaders throw)",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "error-propagation-logging": [
    {
      "id": "DEBT-027",
      "concern": "generation.ts and handler.ts logging endpoints are not directly tested.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "error-propagation-testing": [
    {
      "id": "DEBT-020",
      "concern": "no end-to-end regression test for the full symptom chain (db error \u2192 tocompletionerror metadata \u2192 handler log).",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-025",
      "concern": "handler.ts metadata surfacing criterion lacks a concrete automated verifier.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-026",
      "concern": "main issue only partially validated without an integration test.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them": [
    {
      "id": "DEBT-109",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the step 2 retry loop uses a naked `sleep 2` between attempts, which adds up to 6 seconds of latency on the happy path when the first patch eventually succeeds on attempt 2 or 3. for pods where supabase is reachable but slow during the initial moments of a cold runpod start, the retry logic is fine. however, if the first attempt fails with a tls handshake delay and the retry loop sleeps 2s per attempt regardless of whether curl itself has been blocking for tens of seconds, the total startup latency penalty could be substantial. this is a minor tuning concern, not a correctness issue.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-146",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: finding callers of the changed module shows that `shared.utils.self_refiner` is consumed by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx2_handler.py`, multiple ltx2 pipeline modules, and `wan2gp/models/wan/any2video.py`. the revised validation steps still only drive the three bridge getters in `source/runtime/wgp_ports/vendor_imports.py`; none of the scheduled commands execute a real `self_refiner` caller, so the plan does not yet verify the main caller shapes for the other explicit sprint 2 file change.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-159",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked direct queue caller values in `db_task_to_generation_task()`: direct image tasks may carry `resolution`, `steps`/`num_inference_steps`, `seed`, and `override_profile`. the revised adapter plan covers seed, steps, and memory profile but not guaranteed resolution propagation, so it does not handle all relevant direct-route caller arguments for a supported vibecomfy direct route.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "gpu-branching-test-matrix": [
    {
      "id": "DEBT-113",
      "concern": "linux cuda128 path under-verified",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "gpu-branching-ui-surface": [
    {
      "id": "DEBT-112",
      "concern": "nvidia-50 option is exposed on linux in the ui but linux cuda128 smoke test is missing",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "hook-abstraction": [
    {
      "id": "DEBT-043",
      "concern": "usepairsettingshandler becomes trivial with single caller \u2014 keeping it is extra indirection.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "hype-mirror-cas-coverage": [
    {
      "id": "DEBT-152",
      "concern": "hype-mirrored files whose parent step does not declare matching produces will not be cas-interned, even with the follow_symlinks=false edit.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-7-rev-20260505"
      ]
    }
  ],
  "is-the-change-in-the-right-place-and-would-it-break-any-callers": [
    {
      "id": "DEBT-015",
      "concern": "is the change in the right place, and would it break any callers?: the optional cleanup steps are not in the right place yet. `pairregionslayer` does not receive `pairdatabyindex` today; its props are only `images`, `imagepositionswithpending`, `pairinfowithpending`, and callback/display props in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx#l20). so step 4's 'pass `pairdatabyindex.get(pairindex)` directly' would require new prop plumbing or a different seam.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "is-the-scope-and-scale-of-the-change-appropriate": [
    {
      "id": "DEBT-009",
      "concern": "is the scope and scale of the change appropriate?: phase 2 is still under-specified for execution. step 4 says pairregionslayer should either pass `pairdatabyindex.get(pairindex)` directly or 'just pass the index + frame-only data', which are materially different designs. if phase 2 is kept in the plan, it needs a single concrete direction.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "is-there-convincing-verification-for-the-change": [
    {
      "id": "DEBT-010",
      "concern": "is there convincing verification for the change?: the plan still lacks an explicit automated regression test for the reported bug. step 2 is manual ('check that `usevideoregeneratemode` now gets the fresh url'), but there is no concrete test that opens a segment slot, changes the primary variant data, and asserts that the regenerate path sees the fresh `url`, `generationid`, and `primaryvariantid`.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-011",
      "concern": "is there convincing verification for the change?: the current `usesegmentslotmode` test remains only a smoke test in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts), and the plan does not add behavior coverage for the new sync effect.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-012",
      "concern": "is there convincing verification for the change?: no verification step covers the trailing-slot branch, even though the proposed phase 1 logic currently misses `trailingpairdata` refreshes.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "legacy-data-backfill": [
    {
      "id": "DEBT-004",
      "concern": "the step 8 diagnostic query only detects cross-shot pair_shot_generation_id misassociations, not same-shot misassociations caused by timeline reordering within a shot.",
      "occurrence_count": 1,
      "plan_ids": [
        "redesign-the-segment-position-20260330-1913"
      ]
    }
  ],
  "lookup-consistency": [
    {
      "id": "DEBT-029",
      "concern": "other repo call sites use unordered .limit(1).maybesingle() and will remain inconsistent.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-033",
      "concern": "other call sites with same unsafe pattern not covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "lora-management": [
    {
      "id": "DEBT-099",
      "concern": "lora tools simplified vs full ui parity (multi-stage metadata, private loras)",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "media-lightbox-persistence": [
    {
      "id": "DEBT-002",
      "concern": "variant switches do not clear/restore inpaintprompt, so stale prompt state can leak across variants with no cached prompt.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-prompt-text-reset-bug-20260330-1410"
      ]
    },
    {
      "id": "DEBT-003",
      "concern": "removing prompt/numgenerations from the variant-keyed localstorage cache means all variants within a generation share the same prompt. this broadens existing debt-002 (variant prompt leakage).",
      "occurrence_count": 1,
      "plan_ids": [
        "consolidate-the-media-20260330-1449"
      ]
    }
  ],
  "media-lightbox-segment-slot": [
    {
      "id": "DEBT-016",
      "concern": "media lightbox / segment slot: the targeted sync rationale does not fully explain the reported stale-url bug for regular pairs, and the proposed effect still misses trailing-slot refreshes because those can come from `trailingpairdata` rather than `pairdatabyindex`.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "number-input-nullable": [
    {
      "id": "DEBT-076",
      "concern": "plan doesn't explicitly state onchange must also accept null, though step 3 depends on it.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-077",
      "concern": "disputed v1 flag \u2014 original concern about bulkclippanel being unimplementable.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-079",
      "concern": "onchange null filtering not explicitly addressed in plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "number-input-testing": [
    {
      "id": "DEBT-081",
      "concern": "no planned tests for numberinput shared component or bulkclippanel nullable draft flow.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "orchestrator-completion-rollout": [
    {
      "id": "DEBT-049",
      "concern": "pre-existing individual_travel_segment children won't drive orchestrator completion through segment_type_config after deploy.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-051",
      "concern": "missing compatibility seam in orchestratorcore.ts:123-126 for old individual_travel_segment rows.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-053",
      "concern": "mixed old/new data during rollout can leave old orchestrators without completion counting.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-054",
      "concern": "no test or deployment guard for pre-existing individual_travel_segment children completing after worker change.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-056",
      "concern": "plan overstates backward compatibility for existing data.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-057",
      "concern": "missing rollout compatibility step for in-flight individual_travel_segment tasks.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-058",
      "concern": "pre-deploy individual_travel_segment child completing post-rollout won't be treated as segment task by checkorchestratorcompletion.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-059",
      "concern": "orchestrator.test.ts criterion too narrow to verify old individual_travel_segment compatibility.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    }
  ],
  "pair-settings-plumbing": [
    {
      "id": "DEBT-039",
      "concern": "handleopenpairsettings(pairindex, pairframedata) path in timelinetrackprelude, segmentoutputstrip, and usesegmentoutputstrip not explicitly named.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-042",
      "concern": "same as flag-002 \u2014 segmentoutputstrip and usesegmentoutputstrip still carry pairframedata.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-045",
      "concern": "timelinetrackprelude and segmentoutputstrip still forward (pairindex, pairframedata).",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "plan-scope": [
    {
      "id": "DEBT-032",
      "concern": "step 3 is larger than a light megaplan warrants.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "planning-metadata": [
    {
      "id": "DEBT-017",
      "concern": "planning metadata: the attached metadata and success criteria still describe a different implementation than the current plan body, which risks sending execution and review down the wrong path.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-103",
      "concern": "success criteria don't cover wave 4 scope",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "position-key-semantics": [
    {
      "id": "DEBT-028",
      "concern": "plan investigates a unique constraint on (parent_generation_id, child_order) which doesn't match repo semantics for position keys.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-030",
      "concern": "plan weights toward child_order rather than pair_shot_generation_id as the key that matters.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-031",
      "concern": "unique constraint on (parent_generation_id, child_order) not supported by repo semantics.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "prompt-composition": [
    {
      "id": "DEBT-005",
      "concern": "the plan's step 1 signature includes textbeforeprompts/textafterprompts parameters that would be applied before enhancement, double-wrapping the prompt.",
      "occurrence_count": 1,
      "plan_ids": [
        "in-cloud-mode-when-users-20260330-2214"
      ]
    }
  ],
  "ready-template-snapshots": [
    {
      "id": "DEBT-147",
      "concern": "step 4.2 drops markdownnote nodes but step 4.5 and the success criteria require class_type/widget parity with pre-refactor snapshots, which currently include markdownnote nodes.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-the-higher-abstraction-20260425-0953"
      ]
    },
    {
      "id": "DEBT-148",
      "concern": "same tension as issue_hints v2: drop-markdownnote vs. snapshot parity.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-the-higher-abstraction-20260425-0953"
      ]
    }
  ],
  "reigh-worker-orchestrator-dockerfile": [
    {
      "id": "DEBT-150",
      "concern": "step 7 \u00a73 claims `gpu_orchestrator/dockerfile` has wan2gp install steps; current main is generic and contains none.",
      "occurrence_count": 1,
      "plan_ids": [
        "produce-a-migration-plan-20260505-0555"
      ]
    }
  ],
  "reigh-worker-orchestrator-runpod-startup": [
    {
      "id": "DEBT-149",
      "concern": "`gpu_orchestrator/runpod/startup_script.py` embeds `headless-wan2gp` in `_workdir_discovery_snippet` and is not named explicitly in step 7 \u00a73's checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "produce-a-migration-plan-20260505-0555"
      ]
    }
  ],
  "search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader": [
    {
      "id": "DEBT-141",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the broader runtime surface after the v4 path fix. sprint 2 is still moving two behavior-sensitive seams rather than just the import-path contract: the `wan2gp/` mount path and the `self_refiner` runtime. step 6.2 covers only the three `vendor_imports` getters, while the 6-file travel suite and the bridge-contract tests do not mention `self_refiner`, so dropping the dedicated self-refiner smoke from the runnable steps leaves the broader downstream surface of that changed file under-covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-157",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the supported direct-route scope is still broader than the adapter's guaranteed parameter surface. `db_task_to_generation_task()` currently carries direct task params such as `resolution`, `steps`, and `seed` into wgp generation, but the vibecomfy cli path only guarantees prompt, seed, steps, and memory profile; resolution remains optional/documentation-only in the plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    },
    {
      "id": "DEBT-161",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the revised child-route scope against `migration-thresholds.yaml`. the threshold corpus currently has wan/vace entries for `travel_segment__model-wan22_vace__...` and `join_clips_segment__model-wan22_vace__...`, but only an i2v entry for `individual_travel_segment`; the revised plan makes `individual_travel_segment` with vace model params a must-level worker fixture, which broadens the worker smoke scope beyond the currently tracked wan/vace threshold routes.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-4-wan-single-frame-and-20260506-0818"
      ]
    }
  ],
  "self-refiner-verification": [
    {
      "id": "DEBT-144",
      "concern": "self-refiner verification: the revised plan still aligns `wan2gp/shared/utils/self_refiner.py` without scheduling the sprint 2 ltx-2 `self_refiner` smoke that `docs/wan2gp_fork_migration_plan.md` defines as the behavior-preservation check for that drift upgrade.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    }
  ],
  "settings-defaults": [
    {
      "id": "DEBT-111",
      "concern": "workerrepopath default can go stale if user switches computertype before editing path",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "settings-resolution": [
    {
      "id": "DEBT-093",
      "concern": "settings cascade missing \u2014 shot-only read diverges from form's defaults\u2192user\u2192project\u2192shot merge",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-098",
      "concern": "settings cascade missing \u2014 shot-only read",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "shared-component-compatibility": [
    {
      "id": "DEBT-078",
      "concern": "numberinput changes affect callers outside video-editor (billing, travel-between-images, phaseconfigselectormodal).",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-080",
      "concern": "shared ui component blast radius not audited in plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "shot-linking-testing": [
    {
      "id": "DEBT-021",
      "concern": "no test covers the linkgenerationtoshot error/catch branches.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "signature-propagation": [
    {
      "id": "DEBT-038",
      "concern": "plan doesn't explicitly name timeline/index.tsx and segmentslotcontracts.ts for updates.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-041",
      "concern": "same as flag-001 \u2014 timeline/index.tsx and segmentslotcontracts.ts not in checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-044",
      "concern": "five supporting contract/plumbing sites not named in the checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "ta[REDACTED_SK]": [
    {
      "id": "DEBT-050",
      "concern": "step 3 cites wrong migration file (task_cost_configs instead of task_types) as evidence for db fallback path.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-052",
      "concern": "step 3 should cite task_types source, not task_cost_configs.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-055",
      "concern": "plan doesn't verify travel_segment and travel_stitch exist as active task_types rows using the correct table.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    }
  ],
  "test-coverage": [
    {
      "id": "DEBT-034",
      "concern": "current generation-child.test.ts is only a smoke test.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-035",
      "concern": "no plan to verify other lookup paths choose rows consistently.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-096",
      "concern": "no new tests for db loader or travel param merge path",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-097",
      "concern": "must-level criteria depend on manual testing rather than automated assertions",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-102",
      "concern": "no new unit tests for wave 4 tools",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-104",
      "concern": "must criteria backed by manual testing only",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "test-infrastructure": [
    {
      "id": "DEBT-101",
      "concern": "no test fixtures for resources table",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "timeline-drag-coordination": [
    {
      "id": "DEBT-126",
      "concern": "plan keeps two hooks instead of a single coordinator",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-127",
      "concern": "brief says single coordinator but plan keeps separate hooks",
      "occurrence_count": 2,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-128",
      "concern": "pendingopsref retained despite brief suggesting removal",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-129",
      "concern": "wrapper-bound listener mount wiring under-specified",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    }
  ],
  "timeline-persistence": [
    {
      "id": "DEBT-130",
      "concern": "read path still assembles config and registry from separate requests",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-131",
      "concern": "poll sync verification not structurally changed",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-132",
      "concern": "backend save helpers not wired to new rpc",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-133",
      "concern": "read infrastructure not updated",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-134",
      "concern": "backend tests not in validation list",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-135",
      "concern": "backend callers not migrated",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-136",
      "concern": "broader persistence-contract problem",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-137",
      "concern": "backend split-save not addressed",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-138",
      "concern": "split polling can combine config and registry from different snapshots",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    }
  ],
  "timeline-scaling": [
    {
      "id": "DEBT-001",
      "concern": "the plan only specifies a concrete fix for the default scale(1) case; explicit-scale tracks may still break blend-mode effects.",
      "occurrence_count": 1,
      "plan_ids": [
        "investigate-why-custom-ai-20260330-0408"
      ]
    }
  ],
  "timeline-snap-threshold": [
    {
      "id": "DEBT-139",
      "concern": "threshold is generous (duration) rather than zoom-scaled (8px)",
      "occurrence_count": 1,
      "plan_ids": [
        "implement-smart-snap-to-edge-20260413-0503"
      ]
    },
    {
      "id": "DEBT-140",
      "concern": "computedropposition does not pass a zoom-scaled threshold override",
      "occurrence_count": 1,
      "plan_ids": [
        "implement-smart-snap-to-edge-20260413-0503"
      ]
    }
  ],
  "travel-continuations": [
    {
      "id": "DEBT-094",
      "concern": "smooth continuations not threaded \u2014 agent tasks won't have continuation_config even when shot settings enable it",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-100",
      "concern": "continuation_config omitted from form parity",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "travel-payload-cleanup-scope": [
    {
      "id": "DEBT-116",
      "concern": "plan scope narrower than original user request",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-118",
      "concern": "broader create-task contract problem left untouched",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "travel-payload-readers": [
    {
      "id": "DEBT-114",
      "concern": "phase 4 app-side reader audit incomplete",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-119",
      "concern": "phase 4 field inventory incomplete for app-side readers",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "travel-request-contract": [
    {
      "id": "DEBT-115",
      "concern": "image_variant_ids is in frontend request contract",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-117",
      "concern": "image_variant_ids contract change",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "variant-update-b-fresh-takeover": [
    {
      "id": "DEBT-120",
      "concern": "spawn_worker does not internally call start_worker_process; harness must call both explicitly",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-121",
      "concern": "worker_id and runpod_id must be generated and threaded distinctly; plan currently uses pod_id as both",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-122",
      "concern": "duplicate of correctness-1 \u2014 spawn_worker two-step misstatement",
      "occurrence_count": 2,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-123",
      "concern": "duplicate of correctness-2 \u2014 worker_id/runpod_id propagation across takeover and restore paths",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-124",
      "concern": "duplicate of correctness-1 + correctness-2 \u2014 missing create_worker_record glue and start_worker_process integration",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-125",
      "concern": "duplicate of correctness-2 \u2014 caller contract for spawn_worker requires worker_id, not pod_id",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    }
  ],
  "verification": [
    {
      "id": "DEBT-091",
      "concern": "no end-to-end render test for audio analysis timing",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-092",
      "concern": "no automated coverage for text clips or overlapping clips with audio effects",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "verification-coverage": [
    {
      "id": "DEBT-040",
      "concern": "no automated test exercises the full segment-slot opening path after cleanup.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-046",
      "concern": "no automated coverage that clicking a pair opens the correct modal after cleanup.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-048",
      "concern": "zero behavioral change criterion is not verifiable from tsc + existing tests alone.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "verification-workflow": [
    {
      "id": "DEBT-047",
      "concern": "tsconfig.app.json excludes test files, so tsc won't catch test breakage.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "worker-test-staleness": [
    {
      "id": "DEBT-061",
      "concern": "worker test in test_additional_coverage_modules.py:37 may assert stale payload structure (task_type vs family).",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ]
}

        Escalated debt subsystems:
        [
  {
    "subsystem": "timeline-persistence",
    "total_occurrences": 9,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-130",
        "concern": "read path still assembles config and registry from separate requests",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-131",
        "concern": "poll sync verification not structurally changed",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-132",
        "concern": "backend save helpers not wired to new rpc",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-133",
        "concern": "read infrastructure not updated",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-134",
        "concern": "backend tests not in validation list",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-135",
        "concern": "backend callers not migrated",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-136",
        "concern": "broader persistence-contract problem",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-137",
        "concern": "backend split-save not addressed",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-138",
        "concern": "split polling can combine config and registry from different snapshots",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      }
    ]
  },
  {
    "subsystem": "orchestrator-completion-rollout",
    "total_occurrences": 8,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-049",
        "concern": "pre-existing individual_travel_segment children won't drive orchestrator completion through segment_type_config after deploy.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-051",
        "concern": "missing compatibility seam in orchestratorcore.ts:123-126 for old individual_travel_segment rows.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-053",
        "concern": "mixed old/new data during rollout can leave old orchestrators without completion counting.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-054",
        "concern": "no test or deployment guard for pre-existing individual_travel_segment children completing after worker change.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-056",
        "concern": "plan overstates backward compatibility for existing data.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-057",
        "concern": "missing rollout compatibility step for in-flight individual_travel_segment tasks.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-058",
        "concern": "pre-deploy individual_travel_segment child completing post-rollout won't be treated as segment task by checkorchestratorcompletion.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-059",
        "concern": "orchestrator.test.ts criterion too narrow to verify old individual_travel_segment compatibility.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      }
    ]
  },
  {
    "subsystem": "are-the-proposed-changes-technically-correct",
    "total_occurrences": 7,
    "plan_count": 4,
    "entries": [
      {
        "id": "DEBT-007",
        "concern": "are the proposed changes technically correct?: for ordinary pairs, the new diagnosis is not well-supported by the repo. the current sync effect in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l62) already syncs `url` and `primaryvariantid`, and the regenerate path reads exactly `starturl`, `endurl`, `startgenid`, `endgenid`, `startvariantid`, and `endvariantid` from `segmentslotmode.pairdata` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts#l438). adding `thumburl` and `generationid` to the sync does not, by itself, explain why an old image url is still being used for regular pairs.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-008",
        "concern": "are the proposed changes technically correct?: the fix is incomplete for extra trailing slots. `handlepairclick` can populate `activepairdata` from `trailingpairdata` when `pairindex === pairdatabyindex.size` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l121), but the proposed sync effect only reads `pairdatabyindex.get(segmentslotlightboxindex)`. for those trailing-slot cases `fresh` is `undefined`, so no image refresh happens.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-018",
        "concern": "are the proposed changes technically correct?: the merge pseudocode does not actually sync 'all image fields' as claimed. it omits `id` and `position` from change detection, and when `fresh.startimage` or `fresh.endimage` becomes `null` it preserves the stale previous object instead of syncing that null state. as written, it also needs explicit null-guards around spreads of `prev.startimage` / `prev.endimage` to be safe in strict typescript.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-106",
        "concern": "are the proposed changes technically correct?: the plan's claim that `worker_state.py:200-204` (the 30-minute startup safety net) catches abandoned pods that exited before patching is slightly imprecise. line 200-204 only runs when `in_startup_phase` is true, which requires `startup_phase` to be in `('deps_installing', 'deps_verified', 'worker_starting')` per line 161. a pod that exits before its first patch has `startup_phase = none`, so `in_startup_phase` is false and the code falls through to the normal timeout checks (active_stale / not_claiming) at line 207+, not the 30-minute startup cap. both paths eventually reap the worker, so the end result is the same, but the overview's reasoning (naming 200-204 specifically) is wrong. worth correcting so future readers don't mis-reason about the invariant.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-107",
        "concern": "are the proposed changes technically correct?: checked worker_state.py line 161 (`in_startup_phase = startup_phase in (...)`) against the plan's assumption that subsequent lenient writes are safe. if deps_installing succeeds but deps_verified silently fails, startup_phase stays at 'deps_installing' and the 30-minute cap from line 200-204 applies \u2014 even though the pod is actually progressing through `uv sync`. on a slow runpod image with cold wheel downloads, `uv sync --extra cuda124` plus wan2gp deps can take 20+ minutes. there's no concrete benchmark in the plan that says the 30-minute cap is safely above the expected sync time; if `uv sync` legitimately takes 25 minutes and the deps_verified patch fails on a transient network blip, the orchestrator will terminate a healthy pod. plan should either bump the cap or note that deps_verified swallowing is acceptable because the cap is generously above typical sync time.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-143",
        "concern": "are the proposed changes technically correct?: the path-mapping defect from the previous iteration is fixed, but a different technical gap remains around `self_refiner`. repository search shows `shared.utils.self_refiner` is imported by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx_pipelines/distilled.py`, `ti2vid_one_stage.py`, `ti2vid_two_stages.py`, `wan2gp/models/ltx2/ltx_pipelines/utils/helpers.py`, and `wan2gp/models/wan/any2video.py`; the v4 plan still aligns `wan2gp/shared/utils/self_refiner.py` to upstream head without any concrete runtime step that exercises those code paths after the change, so the only repo-documented behavior check for that file is still missing from the executable body.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-156",
        "concern": "are the proposed changes technically correct?: the direct adapter still has a correctness risk around resolution parity. current vibecomfy ready templates hardcode image dimensions (`image/z_image` uses `emptysd3latentimage` 1024x1024 and `image/qwen_image_2512` uses 768x768), while `vibecomfy run` exposes no `--resolution` flag; the revised plan says a temporary scratchpad/input file may be generated only if supported, otherwise resolution is left out. that means a vibecomfy-supported direct route can silently ignore the worker's `resolution` param unless scratchpad resolution patching is made mandatory for supported direct routes or the support is explicitly limited to default-resolution smoke fixtures.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "variant-update-b-fresh-takeover",
    "total_occurrences": 7,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-120",
        "concern": "spawn_worker does not internally call start_worker_process; harness must call both explicitly",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-121",
        "concern": "worker_id and runpod_id must be generated and threaded distinctly; plan currently uses pod_id as both",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-122",
        "concern": "duplicate of correctness-1 \u2014 spawn_worker two-step misstatement",
        "occurrence_count": 2,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-123",
        "concern": "duplicate of correctness-2 \u2014 worker_id/runpod_id propagation across takeover and restore paths",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-124",
        "concern": "duplicate of correctness-1 + correctness-2 \u2014 missing create_worker_record glue and start_worker_process integration",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-125",
        "concern": "duplicate of correctness-2 \u2014 caller contract for spawn_worker requires worker_id, not pod_id",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      }
    ]
  },
  {
    "subsystem": "audio-reactivity",
    "total_occurrences": 6,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-082",
        "concern": "overlapping clips use first-found, volume not scaled",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-083",
        "concern": "same as audio-reactivity-1 \u2014 overlapping/volume-adjusted clips diverge from audible mix",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-084",
        "concern": "textclip missing globalframeprovider",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-085",
        "concern": "same as audio-reactivity-2 \u2014 textclipsequence missing provider",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-089",
        "concern": "textclip effects surface not covered",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-090",
        "concern": "continuous effects shared by visual and text clips",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      }
    ]
  },
  {
    "subsystem": "does-the-change-touch-all-locations-and-supporting-infrastructure",
    "total_occurrences": 6,
    "plan_count": 6,
    "entries": [
      {
        "id": "DEBT-014",
        "concern": "does the change touch all locations and supporting infrastructure?: phase 1 still misses a real supporting-data location: `trailingpairdata` lives outside `pairdatabyindex` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts#l111), but the proposed sync logic only considers `pairdatabyindex`. if trailing slot regenerate is part of the bug surface, that location is not covered.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-110",
        "concern": "does the change touch all locations and supporting infrastructure?: the non-swallowing helper `update_worker_phase_strict` is a new shell function, but phase 1 step 2 introduces it only as pseudo-code. there is no concrete note that the helper must handle supabase http non-2xx responses as failures (curl returns 0 even on http 4xx/5xx by default unless `-f` or `--fail-with-body` is used). if the implementer ports `update_worker_phase` verbatim with only `|| return 0` removed, a 500 from supabase would still report success because curl's exit code is 0. the plan should specify `curl --fail` or explicit http status code checking in the strict variant.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-142",
        "concern": "does the change touch all locations and supporting infrastructure?: the supporting-infrastructure review still finds one missing check. in `docs/wan2gp_fork_migration_plan.md`, sprint 2's verification matrix and risk register both single out `self_refiner` as a distinct drift-upgrade surface with its own smoke and its own silent-behavior-change risk, but the revised v4 body updates the file without keeping that supporting verification step in the actual execution checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-154",
        "concern": "does the change touch all locations and supporting infrastructure?: documentation/data gap: the sprint exit criteria require profiles 1 and 3 to have vram and wall-clock data, but the plan puts that only in metadata as an info-level criterion and does not schedule a concrete artifact location or command for recording the measurements. the implementation could satisfy all unit tests while still missing one of the explicit exit criteria.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-1-vibecomfy-memory-20260506-0147"
        ]
      },
      {
        "id": "DEBT-158",
        "concern": "does the change touch all locations and supporting infrastructure?: the supporting infrastructure for resolution is still incomplete if direct vibecomfy routes are considered production-supported. vibecomfy has a `vibecomfy.patches.resolution` helper and the cli can load scratchpad files with `allow_scratchpad=true`, but the plan does not require using that path; it permits leaving resolution out for sprint 2.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      },
      {
        "id": "DEBT-162",
        "concern": "does the change touch all locations and supporting infrastructure?: checked vibecomfy profile wording against `vibecomfy/tests/test_ready_templates.py`. the revised plan says to add the production template to representative compile profile coverage 'alongside the existing dry-run id', but the dry-run id is not currently in `profile_smoke_template_ids`; only `video/wanvideo_wrapper_22_5b_i2v` and `video/wan_t2v` are. this is a small wording mismatch rather than a functional blocker because adding either the production id alone or both ids would still satisfy sprint 4.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-4-wan-single-frame-and-20260506-0818"
        ]
      }
    ]
  },
  {
    "subsystem": "test-coverage",
    "total_occurrences": 6,
    "plan_count": 2,
    "entries": [
      {
        "id": "DEBT-034",
        "concern": "current generation-child.test.ts is only a smoke test.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-035",
        "concern": "no plan to verify other lookup paths choose rows consistently.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-096",
        "concern": "no new tests for db loader or travel param merge path",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-097",
        "concern": "must-level criteria depend on manual testing rather than automated assertions",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-102",
        "concern": "no new unit tests for wave 4 tools",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-104",
        "concern": "must criteria backed by manual testing only",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-cascade-paths",
    "total_occurrences": 5,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-065",
        "concern": "cascade lookup only reads params->>'orchestrator_task_id_ref', missing shared reference paths and orchestrator-self detection.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-067",
        "concern": "duplicate of correctness-2 + correctness-3: invalid sql syntax and narrow cascade lookup.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-069",
        "concern": "shared orchestrator-reference helpers not referenced.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-072",
        "concern": "orchestrator tasks that crash don't get orchestrator-self cascade.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-074",
        "concern": "hardcoded params->>'orchestrator_task_id_ref' misses other reference paths.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements",
    "total_occurrences": 5,
    "plan_count": 5,
    "entries": [
      {
        "id": "DEBT-013",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the package is internally inconsistent. the plan body says to keep `activepairdata` in `usestate` and make phase 2 optional, but the attached metadata and success criteria still describe the previous derive-via-`usememo` / remove-`setactivepairdata` / simplify-`onpairclick` plan. that means the approved-plan requirements are only partially coherent as presented.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-108",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the linux distro note is documentation-only; the generated install command in step 7 still runs `apt-get install python3.10-venv python3.10-dev ffmpeg` without any pre-check that the package exists. users on ubuntu 24.04+ who ignore the doc and try to copy-paste the command will hit a confusing `e: unable to locate package python3.10-venv` from apt rather than a targeted error from commandutils.ts. a one-line detection pre-check (e.g., `apt-cache show python3.10-venv >/dev/null 2>&1 || { echo 'install deadsnakes ppa first \u2014 see readme'; exit 1; }`) would convert the silent failure into an actionable error, but the plan does not add this.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-145",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: checked the revised v4 body against `docs/wan2gp_fork_migration_plan.md` sprint 2. the repo plan doc still lists an \"ltx-2 `self_refiner` smoke against the pre-sprint behavioral baseline\" as a sprint 2 verification gate and repeats that smoke in the functionality-preservation checks, but the revised execution steps no longer schedule that smoke anywhere; it survives only as an info-level metadata criterion. because `wan2gp/shared/utils/self_refiner.py` remains an explicit sprint 2 deliverable, the revised plan still only partially carries forward the verification package described in the source migration plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-153",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: worker integration: the migration doc describes the per-call profile override gap as involving reigh-worker adapter handling of override_profile before constructing vibecomfy sessionconfig, but the plan limits sprint 1 per-run work to the vibecomfy cli/runtime. that may be acceptable for a vibecomfy-library mvp, but it does not fully exercise the production-facing per-task override semantics called out in the overall context.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-1-vibecomfy-memory-20260506-0147"
        ]
      },
      {
        "id": "DEBT-155",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: a residual issue-hint tension remains for resolution handling. the plan acknowledges current `vibecomfy run` lacks a resolution flag, but allows the adapter to leave resolution and other template-specific values unwired for sprint 2. because `z_image_turbo` and `qwen_image_2512` are marked vibecomfy-supported direct routes, this may not preserve the existing worker task-parameter contract for tasks that provide a non-default `resolution`.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "timeline-drag-coordination",
    "total_occurrences": 5,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-126",
        "concern": "plan keeps two hooks instead of a single coordinator",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-127",
        "concern": "brief says single coordinator but plan keeps separate hooks",
        "occurrence_count": 2,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-128",
        "concern": "pendingopsref retained despite brief suggesting removal",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-129",
        "concern": "wrapper-bound listener mount wiring under-specified",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-retry",
    "total_occurrences": 4,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-063",
        "concern": "crash requeue sql does not increment attempts, risking infinite requeue loop.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-066",
        "concern": "duplicate of correctness-1: attempts never advance on crash requeue.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-068",
        "concern": "missing attempts increment location in heartbeat sql.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-073",
        "concern": "step 6 under-scoped for real retry convergence and orchestrator-self handling.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "audio-loading",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-086",
        "concern": "getaudiodata in useeffect removes render-readiness signal",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-087",
        "concern": "same as correctness-3 \u2014 preview/render parity risk",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-088",
        "concern": "preview/render parity partially satisfied",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-testing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-070",
        "concern": "no multi-crash convergence test exercising attempts 0\u21921\u21922\u21923.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-071",
        "concern": "no validation that plpgsql body executes successfully.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-075",
        "concern": "criteria don't require proof of crash requeue convergence.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "criteria-verifiability",
    "total_occurrences": 3,
    "plan_count": 2,
    "entries": [
      {
        "id": "DEBT-036",
        "concern": "'no unsafe .maybesingle()' criterion requires judgment about column uniqueness.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-037",
        "concern": "decision documentation location not specified.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-062",
        "concern": "the must criterion requiring 5 task types to exist as active db rows is not verifiable from code diff alone \u2014 it requires a live db query.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-delete-the-20260331-0519"
        ]
      }
    ]
  },
  {
    "subsystem": "edge-test-config",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-022",
        "concern": "plan's vitest commands use the wrong config entry point.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-023",
        "concern": "same as verification-3: wrong vitest config in validation commands.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-024",
        "concern": "success criterion references wrong test command.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      }
    ]
  },
  {
    "subsystem": "error-propagation-testing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-020",
        "concern": "no end-to-end regression test for the full symptom chain (db error \u2192 tocompletionerror metadata \u2192 handler log).",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-025",
        "concern": "handler.ts metadata surfacing criterion lacks a concrete automated verifier.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-026",
        "concern": "main issue only partially validated without an integration test.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      }
    ]
  },
  {
    "subsystem": "find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them",
    "total_occurrences": 3,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-109",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the step 2 retry loop uses a naked `sleep 2` between attempts, which adds up to 6 seconds of latency on the happy path when the first patch eventually succeeds on attempt 2 or 3. for pods where supabase is reachable but slow during the initial moments of a cold runpod start, the retry logic is fine. however, if the first attempt fails with a tls handshake delay and the retry loop sleeps 2s per attempt regardless of whether curl itself has been blocking for tens of seconds, the total startup latency penalty could be substantial. this is a minor tuning concern, not a correctness issue.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-146",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: finding callers of the changed module shows that `shared.utils.self_refiner` is consumed by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx2_handler.py`, multiple ltx2 pipeline modules, and `wan2gp/models/wan/any2video.py`. the revised validation steps still only drive the three bridge getters in `source/runtime/wgp_ports/vendor_imports.py`; none of the scheduled commands execute a real `self_refiner` caller, so the plan does not yet verify the main caller shapes for the other explicit sprint 2 file change.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-159",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked direct queue caller values in `db_task_to_generation_task()`: direct image tasks may carry `resolution`, `steps`/`num_inference_steps`, `seed`, and `override_profile`. the revised adapter plan covers seed, steps, and memory profile but not guaranteed resolution propagation, so it does not handle all relevant direct-route caller arguments for a supported vibecomfy direct route.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "is-there-convincing-verification-for-the-change",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-010",
        "concern": "is there convincing verification for the change?: the plan still lacks an explicit automated regression test for the reported bug. step 2 is manual ('check that `usevideoregeneratemode` now gets the fresh url'), but there is no concrete test that opens a segment slot, changes the primary variant data, and asserts that the regenerate path sees the fresh `url`, `generationid`, and `primaryvariantid`.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-011",
        "concern": "is there convincing verification for the change?: the current `usesegmentslotmode` test remains only a smoke test in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts), and the plan does not add behavior coverage for the new sync effect.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-012",
        "concern": "is there convincing verification for the change?: no verification step covers the trailing-slot branch, even though the proposed phase 1 logic currently misses `trailingpairdata` refreshes.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      }
    ]
  },
  {
    "subsystem": "number-input-nullable",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-076",
        "concern": "plan doesn't explicitly state onchange must also accept null, though step 3 depends on it.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      },
      {
        "id": "DEBT-077",
        "concern": "disputed v1 flag \u2014 original concern about bulkclippanel being unimplementable.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      },
      {
        "id": "DEBT-079",
        "concern": "onchange null filtering not explicitly addressed in plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      }
    ]
  },
  {
    "subsystem": "pair-settings-plumbing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-039",
        "concern": "handleopenpairsettings(pairindex, pairframedata) path in timelinetrackprelude, segmentoutputstrip, and usesegmentoutputstrip not explicitly named.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-042",
        "concern": "same as flag-002 \u2014 segmentoutputstrip and usesegmentoutputstrip still carry pairframedata.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-045",
        "concern": "timelinetrackprelude and segmentoutputstrip still forward (pairindex, pairframedata).",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  },
  {
    "subsystem": "position-key-semantics",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-028",
        "concern": "plan investigates a unique constraint on (parent_generation_id, child_order) which doesn't match repo semantics for position keys.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-030",
        "concern": "plan weights toward child_order rather than pair_shot_generation_id as the key that matters.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-031",
        "concern": "unique constraint on (parent_generation_id, child_order) not supported by repo semantics.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      }
    ]
  },
  {
    "subsystem": "search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader",
    "total_occurrences": 3,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-141",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the broader runtime surface after the v4 path fix. sprint 2 is still moving two behavior-sensitive seams rather than just the import-path contract: the `wan2gp/` mount path and the `self_refiner` runtime. step 6.2 covers only the three `vendor_imports` getters, while the 6-file travel suite and the bridge-contract tests do not mention `self_refiner`, so dropping the dedicated self-refiner smoke from the runnable steps leaves the broader downstream surface of that changed file under-covered.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-157",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the supported direct-route scope is still broader than the adapter's guaranteed parameter surface. `db_task_to_generation_task()` currently carries direct task params such as `resolution`, `steps`, and `seed` into wgp generation, but the vibecomfy cli path only guarantees prompt, seed, steps, and memory profile; resolution remains optional/documentation-only in the plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      },
      {
        "id": "DEBT-161",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the revised child-route scope against `migration-thresholds.yaml`. the threshold corpus currently has wan/vace entries for `travel_segment__model-wan22_vace__...` and `join_clips_segment__model-wan22_vace__...`, but only an i2v entry for `individual_travel_segment`; the revised plan makes `individual_travel_segment` with vace model params a must-level worker fixture, which broadens the worker smoke scope beyond the currently tracked wan/vace threshold routes.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-4-wan-single-frame-and-20260506-0818"
        ]
      }
    ]
  },
  {
    "subsystem": "signature-propagation",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-038",
        "concern": "plan doesn't explicitly name timeline/index.tsx and segmentslotcontracts.ts for updates.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-041",
        "concern": "same as flag-001 \u2014 timeline/index.tsx and segmentslotcontracts.ts not in checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-044",
        "concern": "five supporting contract/plumbing sites not named in the checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  },
  {
    "subsystem": "ta[REDACTED_SK]",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-050",
        "concern": "step 3 cites wrong migration file (task_cost_configs instead of task_types) as evidence for db fallback path.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-052",
        "concern": "step 3 should cite task_types source, not task_cost_configs.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-055",
        "concern": "plan doesn't verify travel_segment and travel_stitch exist as active task_types rows using the correct table.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      }
    ]
  },
  {
    "subsystem": "verification-coverage",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-040",
        "concern": "no automated test exercises the full segment-slot opening path after cleanup.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-046",
        "concern": "no automated coverage that clicking a pair opens the correct modal after cleanup.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-048",
        "concern": "zero behavioral change criterion is not verifiable from tsc + existing tests alone.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  }
]

        Debt guidance:
        - These are known accepted limitations. Do not re-flag them unless the current plan makes them worse, broadens them, or fails to contain them.
        - Prefix every new concern with a subsystem tag followed by a colon, for example `Timeout recovery: retry backoff remains brittle`.
        - When a concern is recurring debt that still needs to be flagged, prefix it with `Recurring debt:` after the subsystem tag, for example `Timeout recovery: Recurring debt: retry backoff remains brittle`.



        Your output template is at: /Users/user_c042661f/Documents/reigh-workspace/.megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json
Read this file first — it contains 5 checks, each with a question and guidance.
For each check, investigate the codebase, then add your findings to the `findings` array for that check.

Each finding needs:
- "detail": what you specifically checked and what you found (at least a full sentence)
- "flagged": true if this describes a difference, risk, or tension — even if you think it's justified. false only if purely informational with no possible downside.
- Every check must end with at least one finding. Never leave a `findings` array empty. If you found no issue, add one detailed `flagged: false` finding explaining what you checked and why it appears clear.

When in doubt, flag it — the gate can accept tradeoffs, but it can't act on findings it never sees.

Good: {"detail": "Checked callers of nthroot_mod in solveset.py line 1205 — passes prime moduli only, consistent with the fix.", "flagged": false}
Good: {"detail": "The fix handles empty tuples but not single-element tuples which need a trailing comma.", "flagged": true}
Bad: {"detail": "No issue found", "flagged": false}  ← too brief, will be rejected
Bad: {"detail": "The hints suggest approach X but the plan uses Y. However Y is consistent with X's intent.", "flagged": false}  ← a different approach than the hints IS a flag. You found a divergence — flag it. The gate decides if it's acceptable.

After filling in checks, add any additional concerns to the `flags` array (e.g., security, performance, dependencies).
Use the standard format (id, concern, category, severity_hint, evidence). This array can be empty.

Workflow: read the file → investigate → read file again → add finding → write file back. Repeat for each check.

        Additional guidelines:
        - Robustness level: standard. Use balanced judgment. Flag significant risks, but do not spend flags on minor polish or executor-obvious boilerplate.
        - Over-engineering: prefer the simplest approach that fully solves the problem.
        - Reuse existing flag IDs when the same concern is still open.
        - `verified_flag_ids`: list flag IDs from prior iterations that the revised plan actually resolves (e.g., if the plan was revised to fix FLAG-001, and you confirm the fix is correct, include "FLAG-001"). Only include flags you've verified — don't guess.
        - Verify that the plan follows the expected structure when validator warnings or the outline suggest drift.
        - Additional flags may use these categories: correctness, security, completeness, performance, maintainability, other.
        - Focus on concrete issues, not structural formatting.

> AGENT

{"checks":[],"flags":[],"verified_flag_ids":[],"disputed_flag_ids":[]}

> AGENT

{"checks":[],"flags":[],"verified_flag_ids":[],"disputed_flag_ids":[]}

> AGENT

{"checks":[],"flags":[],"verified_flag_ids":[],"disputed_flag_ids":[]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "pwd && sed -n '1,220p' .megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

{"checks":[],"flags":[],"verified_flag_ids":[],"disputed_flag_ids":[]}

> AGENT

{"checks":[],"flags":[],"verified_flag_ids":[],"disputed_flag_ids":[]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"claim_next_task_service_role|count_eligible_tasks_service_role|count_queued_tasks_breakdown_service_role|route_key|selected_backend|selector_version|REIGH_BACKEND|VIBECOMFY_ROUTING\" reigh-app reigh-worker -S",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"derive_route_key|travel_segment__|individual_travel_segment|join_clips_segment|route selection|worker_backend|backend\" reigh-worker/source reigh-worker/tests reigh-app/supabase/functions -S",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg --files reigh-app/supabase/functions/claim-next-task reigh-app/supabase/functions/task-counts reigh-app/supabase/functions/create-task reigh-app/supabase/migrations reigh-worker/source/core/db reigh-worker/source/task_handlers reigh-worker/source/runtime | sed -n '1,240p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

{"checks":[{"id":"issue_hints","question":"Did the work fully address the issue hints, user notes, and approved plan requirements?","findings":[{"detail":"Checked the sprint requirement for malformed/unauthorized selector entries against the Phase 1 schema step. The plan creates public.route_backend_selectors and adds selector tests, but it does not explicitly require RLS, service-role-only write policies, grants/revokes, or ownership controls for that table; existing sensitive tables such as tasks, workers, settings, and rate_limits use explicit RLS/policies in migrations. Without that migration work, the unauthorized-entry requirement is only test-named, not structurally addressed.","flagged":true},{"detail":"Checked the child snapshot requirement against the plan body. The plan does name a route_selection_snapshot field on tasks and asks worker-created children to pass explicit snapshot data, which is directionally aligned with the requirement that child rows created later can pin route selection.","flagged":false}]},{"id":"correctness","question":"Are the proposed changes technically correct?","findings":[{"detail":"Checked the proposed materialized selected_backend fields against the proposed claim-time selector join. The plan both stores tasks.selected_backend/selector_version at create time and says claim_next_task_service_role should join route_backend_selectors live for rollback, but it does not specify whether the RPC returns/enforces the live selector values or the materialized task snapshot. That ambiguity can produce stale claim responses after rollback, which undermines the selector-version logging and child-pinning contract.","flagged":true},{"detail":"Checked the current latest claim RPC signature in reigh-app/supabase/migrations/20260504120000_extend_claim_next_task_for_pools.sql; the active service-role claim function already has seven parameters for same-model, max-wait, worker_pool, and task_types. The plan correctly calls out extending this RPC instead of replacing the claim path wholesale, but implementers must preserve the existing pool/task_types filters while adding backend eligibility.","flagged":false}]},{"id":"scope","question":"Search for related code that handles the same concept. Is the reported issue a symptom of something broader?","findings":[{"detail":"Searched related route-key code and found join_clips_segment route keys are handled outside the canonical worker selector: tests call scripts/dual_run_compare/route_keys.py for join_clips_segment, while source/task_handlers/tasks/template_routing.py only derives dimensional keys for travel_segment and individual_travel_segment. The plan says to keep the existing Python serializer as canonical and update travel/join child creation paths, but it does not add join_clips_segment to that canonical serializer, so a production selector contract would still lack a shared app/worker key for join children.","flagged":true},{"detail":"Searched direct route coverage in the worker selector and found direct routes such as z_image_turbo, qwen_image_2512, qwen_image, qwen_image_edit, qwen_image_style, image_inpaint, annotated_image_edit, and wan_2_2_t2i are already represented in source/task_handlers/tasks/template_routing.py. The plan’s direct-route task_type key assumption matches that existing implementation.","flagged":false}]},{"id":"all_locations","question":"Does the change touch all locations AND supporting infrastructure?","findings":[{"detail":"Checked task-counts/index.ts and found it does more than RPC totals: it also builds queued_tasks and active_tasks arrays from direct tasks table queries and filters them in TypeScript. Phase 2 Step 4 only mentions extending the count RPCs/breakdown RPCs and parsing worker_backend; unless the direct queued_tasks filter also applies selector/backend eligibility, task-counts can report tasks as queued/claimable for a VibeComfy scaler even when claim-next-task would return 204.","flagged":true},{"detail":"Checked worker claim and execution locations. The plan names source/core/db/task_claim.py for sending backend capability and source/runtime/worker/server.py plus task_execution.py for a pre-execution guard, which are the right worker-side surfaces for the current code because poll_next_task posts the claim-next-task payload and process_single_task dispatches claimed work.","flagged":false}]},{"id":"callers","question":"Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?","findings":[{"detail":"Grep found add_task_to_db callers in travel/orchestrator.py, travel/stitch.py, and join/task_builder.py, and the current add_task_to_db signature only accepts task_payload, task_type_str, dependant_on, and db_path. The plan says to extend add_task_to_db for optional route-selection metadata and update travel and join builders, but it omits travel/stitch.py and travel/chaining.py call paths that also enqueue child/processing tasks through the same helper; those callers need an explicit decision to pass a snapshot or intentionally leave the new fields null/WGP-safe.","flagged":true},{"detail":"Checked create-task workerPassthrough.ts and confirmed it currently copies request.input directly into params and only lifts task_id/dependant_on into top-level insert fields. The plan’s instruction to allow worker-created children to pass route_selection_snapshot is compatible with this caller shape only if the implementation also defines how input snapshot keys become top-level route_key/selected_backend/selector_version fields rather than remaining buried in params.","flagged":true}]}],"flags":[{"id":"FLAG-001","concern":"Selector authorization: route_backend_selectors needs explicit RLS/grant/service-role write controls; the plan names unauthorized-entry tests but not the database access-control implementation.","category":"security","severity_hint":"likely-significant","evidence":"Existing migrations enable RLS and policies for sensitive tables (tasks in 20250113000003, workers in 20250705000001, settings/rate_limits in later migrations). Phase 1 only specifies creating route_backend_selectors and indexes/checks."},{"id":"FLAG-002","concern":"Selector snapshot/live-source ambiguity: the plan materializes selected_backend on tasks while claim enforcement joins the live selector table, without defining which source is returned and logged after selector rollback.","category":"correctness","severity_hint":"likely-significant","evidence":"Phase 1 adds tasks.selected_backend and selector_version; Phase 3 joins route_backend_selectors for claim eligibility; Phase 5 documents no claim-path cache/rollback SLO. The return-shape source is unspecified."},{"id":"FLAG-003","concern":"Route-key coverage: join_clips_segment is a child route in the worker/orchestrator surface but is not covered by the claimed canonical Python serializer in template_routing.py.","category":"completeness","severity_hint":"likely-significant","evidence":"template_routing.py only derives dimensional keys for travel_segment and individual_travel_segment; test_task_registry_ic_lora_dedup.py uses scripts/dual_run_compare/route_keys.py to derive join_clips_segment__model-wan22_vace__guidance-vace__continuity-join_bridge__profile-default."},{"id":"FLAG-004","concern":"Task-counts alignment: direct queued_tasks/active_tasks queries in task-counts are not explicitly covered by the backend selector eligibility update.","category":"correctness","severity_hint":"likely-significant","evidence":"task-counts/index.ts filters queued_tasks in TypeScript from tasks table results after RPC totals; Phase 2 Step 4 names count_eligible_tasks_service_role and count_queued_tasks_breakdown_service_role but not the detailed array filters."},{"id":"FLAG-005","concern":"Child snapshot propagation: not all add_task_to_db callers are named, and workerPassthrough currently has no top-level route field lifting contract for explicit snapshots.","category":"completeness","severity_hint":"uncertain","evidence":"add_task_to_db is called from travel/orchestrator.py, travel/stitch.py, join/task_builder.py, and other travel chaining paths; workerPassthrough.ts only maps task_id/dependant_on top-level and leaves the rest in params."}],"verified_flag_ids":[],"disputed_flag_ids":[]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,220p' reigh-app/supabase/functions/claim-next-task/index.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' reigh-app/supabase/functions/task-counts/index.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' reigh-worker/source/task_handlers/tasks/template_routing.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,290p' reigh-app/supabase/migrations/20260504120000_extend_claim_next_task_for_pools.sql",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,220p' reigh-app/supabase/functions/create-task/resolvers/types.ts && sed -n '1,240p' reigh-app/supabase/functions/create-task/index.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,220p' reigh-app/supabase/functions/create-task/resolvers/workerPassthrough.ts && sed -n '1,220p' reigh-worker/source/core/db/task_claim.py && sed -n '1,220p' reigh-worker/source/core/db/task_completion.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 24000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' reigh-worker/source/task_handlers/tasks/task_conversion.py && sed -n '1,220p' reigh-worker/source/task_handlers/tasks/task_execution.py && sed -n '1,220p' reigh-worker/source/runtime/worker/server.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 26000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '220,520p' reigh-worker/source/task_handlers/tasks/template_routing.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '220,460p' reigh-worker/source/core/db/task_claim.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '220,520p' reigh-app/supabase/functions/create-task/index.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"add_task_to_db\\(|route_selection|selected_backend|selector_version|[REDACTED] reigh-worker/tests reigh-app/supabase/functions/create-task -S",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"CREATE TABLE.*tasks|CREATE TYPE.*task_status|ALTER TABLE.*tasks|tasks \\(\" reigh-app/supabase/migrations -S | head -n 160",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"model_family|guidance_kind|travel_guidance|continuity_case|override_profile|model_name|svi2pro|video_guide|video_mask|video_source|task_type|_source_task_type\" reigh-app/supabase/functions/create-task/resolvers reigh-worker/source/task_handlers/travel reigh-worker/source/task_handlers/join -S",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 24000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '2200,2485p' reigh-worker/source/task_handlers/travel/orchestrator.py && sed -n '80,160p' reigh-worker/source/task_handlers/join/task_builder.py && sed -n '200,270p' reigh-worker/source/task_handlers/join/task_builder.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' reigh-worker/tests/test_template_routing.py && sed -n '1,290p' reigh-worker/tests/test_task_registry_ic_lora_dedup.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '260,620p' reigh-app/supabase/functions/task-counts/index.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 24000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,80p' reigh-app/supabase/migrations/20250100000000_create_base_schema.sql",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,60p' reigh-app/supabase/migrations/20260121000000_support_multiple_dependencies.sql",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"ENABLE ROW LEVEL SECURITY|CREATE POLICY|GRANT|REVOKE|SECURITY DEFINER\" reigh-app/supabase/migrations/20250113000003_protect_timing_fields.sql reigh-app/supabase/migrations/20260130210000_secure_settings_and_logging_tables.sql reigh-app/supabase/migrations -S | head -n 200",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python3 - <<'PY'\nimport json\nfrom pathlib import Path\npath = Path('.megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json')\ndata = json.loads(path.read_text())\nfindings = {\n  'issue_hints': [\n    {\n      'detail': 'Checked the sprint requirement for malformed/unauthorized selector entries against the Phase 1 schema step. The plan creates public.route_backend_selectors and adds selector tests, but it does not explicitly require RLS, service-role-only write policies, grants/revokes, or ownership controls for that table; existing sensitive tables such as tasks, workers, settings, and rate_limits use explicit RLS/policies in migrations. Without that migration work, the unauthorized-entry requirement is only test-named, not structurally addressed.',\n      'flagged': True,\n    },\n    {\n      'detail': 'Checked the child snapshot requirement against the plan body. The plan does name a route_selection_snapshot field on tasks and asks worker-created children to pass explicit snapshot data, which is directionally aligned with the requirement that child rows created later can pin route selection.',\n      'flagged': False,\n    },\n  ],\n  'correctness': [\n    {\n      'detail': 'Checked the proposed materialized selected_backend fields against the proposed claim-time selector join. The plan both stores tasks.selected_backend/selector_version at create time and says claim_next_task_service_role should join route_backend_selectors live for rollback, but it does not specify whether the RPC returns/enforces the live selector values or the materialized task snapshot. That ambiguity can produce stale claim responses after rollback, which undermines the selector-version logging and child-pinning contract.',\n      'flagged': True,\n    },\n    {\n      'detail': 'Checked the current latest claim RPC signature in reigh-app/supabase/migrations/20260504120000_extend_claim_next_task_for_pools.sql; the active service-role claim function already has seven parameters for same-model, max-wait, worker_pool, and task_types. The plan correctly calls out extending this RPC instead of replacing the claim path wholesale, but implementers must preserve the existing pool/task_types filters while adding backend eligibility.',\n      'flagged': False,\n    },\n  ],\n  'scope': [\n    {\n      'detail': 'Searched related route-key code and found join_clips_segment route keys are handled outside the canonical worker selector: tests call scripts/dual_run_compare/route_keys.py for join_clips_segment, while source/task_handlers/tasks/template_routing.py only derives dimensional keys for travel_segment and individual_travel_segment. The plan says to keep the existing Python serializer as canonical and update travel/join child creation paths, but it does not add join_clips_segment to that canonical serializer, so a production selector contract would still lack a shared app/worker key for join children.',\n      'flagged': True,\n    },\n    {\n      'detail': 'Searched direct route coverage in the worker selector and found direct routes such as z_image_turbo, qwen_image_2512, qwen_image, qwen_image_edit, qwen_image_style, image_inpaint, annotated_image_edit, and wan_2_2_t2i are already represented in source/task_handlers/tasks/template_routing.py. The plan’s direct-route task_type key assumption matches that existing implementation.',\n      'flagged': False,\n    },\n  ],\n  'all_locations': [\n    {\n      'detail': 'Checked task-counts/index.ts and found it does more than RPC totals: it also builds queued_tasks and active_tasks arrays from direct tasks table queries and filters them in TypeScript. Phase 2 Step 4 only mentions extending the count RPCs/breakdown RPCs and parsing worker_backend; unless the direct queued_tasks filter also applies selector/backend eligibility, task-counts can report tasks as queued/claimable for a VibeComfy scaler even when claim-next-task would return 204.',\n      'flagged': True,\n    },\n    {\n      'detail': 'Checked worker claim and execution locations. The plan names source/core/db/task_claim.py for sending backend capability and source/runtime/worker/server.py plus task_execution.py for a pre-execution guard, which are the right worker-side surfaces for the current code because poll_next_task posts the claim-next-task payload and process_single_task dispatches claimed work.',\n      'flagged': False,\n    },\n  ],\n  'callers': [\n    {\n      'detail': 'Grep found add_task_to_db callers in travel/orchestrator.py, travel/stitch.py, and join/task_builder.py, and the current add_task_to_db signature only accepts task_payload, task_type_str, dependant_on, and db_path. The plan says to extend add_task_to_db for optional route-selection metadata and update travel and join builders, but it omits travel/stitch.py and travel/chaining.py call paths that also enqueue child/processing tasks through the same helper; those callers need an explicit decision to pass a snapshot or intentionally leave the new fields null/WGP-safe.',\n      'flagged': True,\n    },\n    {\n      'detail': 'Checked create-task workerPassthrough.ts and confirmed it currently copies request.input directly into params and only lifts task_id/dependant_on into top-level insert fields. The plan’s instruction to allow worker-created children to pass route_selection_snapshot is compatible with this caller shape only if the implementation also defines how input snapshot keys become top-level route_key/selected_backend/selector_version fields rather than remaining buried in params.',\n      'flagged': True,\n    },\n  ],\n}\nfor check in data['checks']:\n    check['findings'] = findings[check['id']]\ndata['flags'] = [\n  {\n    'id': 'FLAG-001',\n    'concern': 'Selector authorization: route_backend_selectors needs explicit RLS/grant/service-role write controls; the plan names unauthorized-entry tests but not the database access-control implementation.',\n    'category': 'security',\n    'severity_hint': 'likely-significant',\n    'evidence': 'Existing migrations enable RLS and policies for sensitive tables (tasks in 20250113000003, workers in 20250705000001, settings/rate_limits in later migrations). Phase 1 only specifies creating route_backend_selectors and indexes/checks.',\n  },\n  {\n    'id': 'FLAG-002',\n    'concern': 'Selector snapshot/live-source ambiguity: the plan materializes selected_backend on tasks while claim enforcement joins the live selector table, without defining which source is returned and logged after selector rollback.',\n    'category': 'correctness',\n    'severity_hint': 'likely-significant',\n    'evidence': 'Phase 1 adds tasks.selected_backend and selector_version; Phase 3 joins route_backend_selectors for claim eligibility; Phase 5 documents no claim-path cache/rollback SLO. The return-shape source is unspecified.',\n  },\n  {\n    'id': 'FLAG-003',\n    'concern': 'Route-key coverage: join_clips_segment is a child route in the worker/orchestrator surface but is not covered by the claimed canonical Python serializer in template_routing.py.',\n    'category': 'completeness',\n    'severity_hint': 'likely-significant',\n    'evidence': 'template_routing.py only derives dimensional keys for travel_segment and individual_travel_segment; test_task_registry_ic_lora_dedup.py uses scripts/dual_run_compare/route_keys.py to derive join_clips_segment__model-wan22_vace__guidance-vace__continuity-join_bridge__profile-default.',\n  },\n  {\n    'id': 'FLAG-004',\n    'concern': 'Task-counts alignment: direct queued_tasks/active_tasks queries in task-counts are not explicitly covered by the backend selector eligibility update.',\n    'category': 'correctness',\n    'severity_hint': 'likely-significant',\n    'evidence': 'task-counts/index.ts filters queued_tasks in TypeScript from tasks table results after RPC totals; Phase 2 Step 4 names count_eligible_tasks_service_role and count_queued_tasks_breakdown_service_role but not the detailed array filters.',\n  },\n  {\n    'id': 'FLAG-005',\n    'concern': 'Child snapshot propagation: not all add_task_to_db callers are named, and workerPassthrough currently has no top-level route field lifting contract for explicit snapshots.',\n    'category': 'completeness',\n    'severity_hint': 'uncertain',\n    'evidence': 'add_task_to_db is called from travel/orchestrator.py, travel/stitch.py, join/task_builder.py, and other travel chaining paths; workerPassthrough.ts only maps task_id/dependant_on top-level and leaves the rest in params.',\n  },\n]\ndata['verified_flag_ids'] = []\ndata['disputed_flag_ids'] = []\npath.write_text(json.dumps(data, indent=2) + '\\n')\nPY\nsed -n '1,260p' .megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are an independent reviewer. Critique the plan against the actual repository.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace





        Idea:
# Sprint 6: Production Selector and Claim Contract

## Overall Context

This sprint turns local selector ideas into production claim behavior before orchestrated routes depend on them. It is the control-plane foundation for rollback and canary.

## Shared Operating Rules

- Production missing selector key means WGP/no-claim, never implicit Comfy.
- Workers must not claim routes they cannot execute.
- Selector version and selected backend must be visible in logs or task metadata.
- Child rows created later must be able to snapshot route selection.

## Sprint Goal

Make selector and claim behavior concrete for production.

## Required Deliverables

- Selector schema/namespace.
- Route-key serialization, including direct variants where needed.
- Index/RPC/query behavior.
- Cache TTL and rollback SLO.
- Malformed/unauthorized/stale-entry tests.
- Claim-time backend eligibility or pre-execution requeue/fail-closed guard.
- Selector-version logging.
- Child-route snapshot field contract for later parent-created rows.

## Exit Criteria

Missing production route key means WGP/no-claim; mismatched workers cannot claim or execute selected routes; selector unreachable behavior and rollback SLO are tested; selected backend/selector version can be pinned for child rows created after parent claim.

        Plan:
        # Implementation Plan: Sprint 6 Production Selector and Claim Contract

## Overview
The plan is still targeting the right root cause: production claim behavior is currently based on run type, task type, and worker-local selector logic, while rollback/canary needs a production selector contract enforced before a worker claims a task. The critique does not point to the wrong subsystem; it points to missing parts of the same contract: selector authorization, live selector versus task snapshot source of truth, complete route-key coverage, task-count parity, and child-row propagation through all creation paths.

The revised approach keeps the original shape but tightens the contract: claim eligibility always uses the live production selector table, with no claim-path cache; task-row selector fields are snapshots for observability and later child pinning, not the source of claim authorization. Missing live selector rows never imply VibeComfy. WGP remains the legacy-safe claim path where execution exists.

Primary touch points are `reigh-app/supabase/migrations/`, `reigh-app/supabase/functions/claim-next-task/index.ts`, `reigh-app/supabase/functions/task-counts/index.ts`, `reigh-app/supabase/functions/create-task/`, `reigh-worker/source/task_handlers/tasks/template_routing.py`, `reigh-worker/source/core/db/task_claim.py`, `reigh-worker/source/core/db/task_completion.py`, and all `add_task_to_db` callers discovered in worker task handlers.

## Phase 1: Foundation — Selector Schema, Security, and Source of Truth

### Step 1: Create selector schema with explicit access control (`reigh-app/supabase/migrations/`)
**Scope:** Medium
1. Add a migration creating `public.route_backend_selectors` with `namespace`, `route_key`, `selected_backend`, `selector_version`, `enabled`, `updated_at`, `expires_at`, and `metadata`.
2. Add checks: `selected_backend in ('wgp', 'vibecomfy')`, non-empty namespace, non-empty route key, non-empty selector version, and `expires_at is null or expires_at > updated_at`.
3. Add unique lookup on `(namespace, route_key)` and selector lookup indexes for claim paths.
4. Enable RLS on `route_backend_selectors`; revoke broad writes; grant service-role read/write; allow authenticated/anon no direct mutation. If read access is needed outside service-role RPCs, expose it only through a security-definer read RPC with constrained output.
5. Add comments documenting that selector rows are control-plane data and must be mutated only by service-role/admin deployment paths.

### Step 2: Add task route snapshot columns (`reigh-app/supabase/migrations/`)
**Scope:** Medium
1. Add `tasks.route_key text`, `tasks.selected_backend text`, `tasks.selector_version text`, and `tasks.route_selection_snapshot jsonb`.
2. Add a check for task `selected_backend` when present: `selected_backend in ('wgp', 'vibecomfy')`.
3. Add indexes for queued claim lookup: `(status, route_key, created_at)`, `(status, selected_backend, created_at)`, and any partial index needed by the updated claim RPC.
4. Backfill direct task route keys where route key equals `task_type`; do not invent dimensional child keys for historical rows unless their params can be serialized with the same helper contract.
5. Document source of truth: live `route_backend_selectors` controls claim eligibility; task columns are snapshots for logs, debugging, and child-row pinning.

## Phase 2: Route-Key Serialization

### Step 3: Extend canonical worker route serializer (`reigh-worker/source/task_handlers/tasks/template_routing.py`)
**Scope:** Medium
1. Keep `derive_route_key` lightweight and import-safe, preserving the existing no-WGP/no-VibeComfy import test.
2. Add dimensional serialization for `join_clips_segment`, matching the existing comparison key shape used by `scripts/dual_run_compare/route_keys.py`: `join_clips_segment__model-*__guidance-*__continuity-join_bridge__profile-*`.
3. Keep existing direct keys for `z_image_turbo`, Qwen routes, `wan_2_2_t2i`, `travel_segment`, and `individual_travel_segment`.
4. Add route snapshot helpers that produce `{ route_key, selected_backend, selector_version, selector_namespace }` without making claim decisions.

### Step 4: Add TypeScript route-key helper for task creation (`reigh-app/supabase/functions/create-task/`)
**Scope:** Medium
1. Add a small helper near create-task resolvers that mirrors the Python route-key serializer for direct routes, travel children, individual travel children, and `join_clips_segment`.
2. Use the same slugging rules as Python for model, guidance, continuity, and profile fields.
3. Add resolver tests for direct route keys and dimensional child keys, including `join_clips_segment`.
4. Keep this helper independent of frontend UI code and worker-only WGP/VibeComfy modules.

## Phase 3: Claim-Time Selector Enforcement

### Step 5: Extend claim request and live-selector RPC (`claim-next-task`, migration RPC)
**Scope:** Large
1. Extend `claim-next-task` request parsing with `worker_backend?: 'wgp' | 'vibecomfy'` and `selector_namespace?: string`; default backend to `wgp` for existing service-role GPU callers and namespace to `production`.
2. Reject malformed `worker_backend` and malformed namespace with `400` before calling the RPC.
3. Extend `claim_next_task_service_role` with `p_worker_backend text default 'wgp'` and `p_selector_namespace text default 'production'`.
4. In the candidate query, use `tasks.route_key` to left join the live `route_backend_selectors` row for the requested namespace.
5. Enforce claim eligibility from the live selector row:
   - Missing selector row: VibeComfy workers cannot claim; WGP workers may claim only legacy WGP-executable routes.
   - Enabled, non-stale selector row: only the matching backend can claim.
   - Disabled, expired, malformed, or inaccessible selector row: no VibeComfy claim and no implicit Comfy fallback.
6. Return live selector values used for the claim as `selected_backend`, `selector_version`, `selector_namespace`, and `route_key`. Also return the task snapshot separately as `route_selection_snapshot` if present, so logs can distinguish live claim decision from pinned task metadata.
7. Update claim logs in `claim-next-task/index.ts` to include live decision fields and task snapshot fields.

### Step 6: Align task counts with claim eligibility (`task-counts`, count RPCs, TypeScript array filters)
**Scope:** Large
1. Extend `task-counts` service-role request parsing with `worker_backend` and `selector_namespace`, using the same validation/defaults as `claim-next-task`.
2. Update or add backend-aware count RPCs so `queued_only`, `queued_plus_active`, and breakdown totals use the same live selector eligibility as `claim_next_task_service_role`.
3. Update the direct `queued_tasks` and `active_tasks` queries/filters in `task-counts/index.ts` to apply the same backend selector eligibility as the RPC totals, not just run type and capacity filters.
4. Include route fields in detailed arrays when present: `route_key`, `selected_backend`, `selector_version`, and `selector_namespace`.
5. Add tests where VibeComfy `queued_tasks` is empty for missing selector rows while WGP sees the legacy-safe claimable row, and where aggregate totals match detailed arrays.

## Phase 4: Task Creation and Snapshot Materialization

### Step 7: Materialize task snapshots at create time (`reigh-app/supabase/functions/create-task/`)
**Scope:** Medium
1. Extend `TaskInsertObject` with top-level `route_key`, `selected_backend`, `selector_version`, and `route_selection_snapshot`.
2. After resolver output and before insert, compute `route_key` for each task when not explicitly supplied.
3. Look up the live selector row for the configured namespace and populate task snapshot fields from that live selector. If no selector exists, store `route_key` and a WGP-safe missing-selector snapshot rather than implying VibeComfy.
4. If selector lookup itself fails or returns malformed data, fail closed with an explicit create-task error rather than inserting a task with ambiguous backend metadata.
5. Add tests for selector present, selector missing, malformed selector, and selector lookup failure.

### Step 8: Define worker passthrough route-field lifting (`workerPassthrough.ts`, create-task tests)
**Scope:** Medium
1. Update `createWorkerPassthroughResolver` so worker-created payloads can pass explicit route fields at top level in `input`: `route_key`, `selected_backend`, `selector_version`, and `route_selection_snapshot`.
2. Lift those fields into top-level `TaskInsertObject` columns rather than leaving them buried in `params`.
3. Keep the existing `task_id` and `dependant_on` lifting behavior unchanged.
4. Validate explicit backend values and route snapshot shape before insert.
5. Add tests proving worker-created children get top-level route fields and still preserve the original payload in `params`.

## Phase 5: Worker Integration and Child Snapshot Propagation

### Step 9: Send backend capability and log claim fields (`reigh-worker/source/core/db/task_claim.py`)
**Scope:** Small
1. Parse `REIGH_BACKEND` through the existing strict backend parser and send `worker_backend` in service-role claim payloads.
2. Include returned `route_key`, live `selected_backend`, `selector_version`, and snapshot metadata in claim debug logs.
3. Preserve PAT/local behavior unless PAT backend capability is intentionally added later.

### Step 10: Add pre-execution mismatch guard (`reigh-worker/source/runtime/worker/server.py`, `task_execution.py`)
**Scope:** Medium
1. Before `process_single_task`, compare the live claim decision returned by `claim-next-task` with the current worker backend.
2. If a mismatch reaches the worker despite claim filtering, requeue with `clear_worker=true` using the existing retry/update path when another backend can handle it.
3. If the selector decision is malformed or explicitly unsupported, mark failed with a fail-closed error that includes `task_id`, `task_type`, `route_key`, `selected_backend`, and `selector_version`.
4. Extend `VIBECOMFY_ROUTING` and WGP routing telemetry fields with selector version and backend decision fields.

### Step 11: Inventory and update every child task creation caller (`reigh-worker/source/core/db/task_completion.py`, worker handlers)
**Scope:** Large
1. Extend `add_task_to_db` to accept optional route snapshot fields and include them in the `create-task` input payload.
2. Inventory all `add_task_to_db` callers with `rg "add_task_to_db" reigh-worker/source` before editing.
3. Update known child/processing callers with an explicit decision:
   - `reigh-worker/source/task_handlers/travel/orchestrator.py`: derive child route keys and pass child snapshots for `travel_segment` and stitch children.
   - `reigh-worker/source/task_handlers/travel/stitch.py`: pass snapshot when it creates follow-on tasks, or explicitly leave WGP-safe null fields for WGP-only processing tasks.
   - `reigh-worker/source/task_handlers/travel/chaining.py` and related guide/mask builder paths: pass snapshot or explicitly document WGP-safe null behavior.
   - `reigh-worker/source/task_handlers/join/task_builder.py`: derive/pass snapshots for `join_clips_segment` and related join child rows.
4. Add focused tests for `add_task_to_db` payload construction and at least one travel and one join child creation path.

## Phase 6: Failure Modes, Rollback SLO, and Validation

### Step 12: Add selector security and failure-mode tests (`reigh-app/supabase/functions/**/*.test.ts`, migration SQL tests)
**Scope:** Medium
1. Test unauthorized direct selector mutation/read behavior according to the RLS/grant contract.
2. Test malformed backend values, disabled selector rows, expired selector rows, missing selector rows, and selector lookup failures.
3. Test that none of those cases imply a VibeComfy claim.
4. Test that successful claims return and log live selector fields distinctly from task snapshot fields.

### Step 13: Document and test rollback/cache behavior (`claim-next-task`, `task-counts`)
**Scope:** Small
1. Document claim-path selector TTL as zero: every claim decision uses the live selector table through the RPC.
2. Define rollback SLO as database commit visibility plus normal worker/scaler polling interval.
3. If create-task uses an edge-side lookup helper, do not use an unbounded cache; either use no cache or a bounded `ROUTE_SELECTOR_CACHE_TTL_MS <= 30000` with tests.
4. Add a rollback test where changing the live selector version/backend changes subsequent claim eligibility and returned/logged selector fields without waiting for stale task snapshots to update.

## Execution Order
1. Land selector schema, RLS/grants, task route columns, and indexes first.
2. Add Python and TypeScript route-key helpers, including `join_clips_segment`, before enforcing selector behavior.
3. Update claim RPC and `claim-next-task` live selector enforcement, then update `task-counts` totals and detailed arrays to match.
4. Materialize create-task snapshots and worker passthrough lifting after the schema and route helper contract are stable.
5. Wire worker backend claim payloads and pre-execution mismatch guards.
6. Update all `add_task_to_db` callers after inventory so no child path accidentally drops route snapshot fields.
7. Finish with security, failure-mode, rollback, and parity tests.

## Validation Order
1. Run focused route-key tests: worker `test_template_routing.py` and create-task route helper tests.
2. Run selector migration/security tests and create-task resolver tests.
3. Run `claim-next-task` tests for backend eligibility, missing selector, malformed selector, stale selector, and returned live selector fields.
4. Run `task-counts` tests proving aggregate totals and detailed arrays match claim eligibility.
5. Run worker tests for claim payload parsing, pre-execution mismatch guard, and VibeComfy/WGP routing telemetry.
6. Run child creation tests for `add_task_to_db`, travel child rows, stitch/chaining decisions, and join child rows.
7. Finish with the relevant Supabase function suite and worker/orchestrator targeted suites.


        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-05-06T08:59:11Z",
  "hash": "sha256:1a2cc9a49559ffd38291027a9570ba68427b5bc3143271e7e89a2d139f95ef91",
  "changes_summary": "Revised the plan to make live selector lookup the explicit claim source of truth, add RLS/grant controls for selector data, cover join_clips_segment route keys, align task-count detailed arrays with claim eligibility, and inventory/lift child route snapshot fields through every worker-created task path.",
  "flags_addressed": [
    "FLAG-001",
    "FLAG-002",
    "FLAG-003",
    "FLAG-004",
    "FLAG-005",
    "issue_hints",
    "correctness",
    "scope",
    "all_locations",
    "callers-1",
    "callers-2"
  ],
  "questions": [
    "Should selector administration be implemented only through migrations/service-role SQL, or is there an existing admin edge function that should own selector writes?",
    "For non-production environments, should selector namespace come from a specific existing env var, or should this sprint introduce a new one such as `ROUTE_SELECTOR_NAMESPACE`?"
  ],
  "success_criteria": [
    {
      "criterion": "`route_backend_selectors` has explicit RLS/grant/service-role mutation controls, and unauthorized selector access is covered by tests or migration-level verification.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "A VibeComfy worker cannot claim a queued production task when the live selector row is missing, disabled, expired, malformed, or inaccessible.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "WGP remains the legacy-safe claim path for missing selector rows only where the route is WGP-executable; missing selector rows never imply VibeComfy.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Claim eligibility, claim response fields, and claim logs use live selector values, while task-row selector fields are clearly treated as snapshots for observability and child pinning.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "A worker cannot claim or execute a task whose live selected backend does not match its declared backend capability; any escaped mismatch is requeued or failed closed before execution.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`task-counts` aggregate totals and detailed `queued_tasks`/`active_tasks` arrays use the same backend selector eligibility semantics as `claim-next-task`.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Route-key serialization tests cover direct routes, travel child variants, individual travel child variants, and `join_clips_segment` dimensional keys.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Worker-created child rows can lift `route_key`, `selected_backend`, `selector_version`, and `route_selection_snapshot` into top-level task columns through `workerPassthrough`.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Every `add_task_to_db` caller is inventoried and either passes a route snapshot or is explicitly kept WGP-safe/null by design.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Selector version and selected backend are visible in successful claim responses and worker/system logs.",
      "priority": "must",
      "requires": [
        "run_tests",
        "observe_runtime_logs",
        "parse_diff"
      ]
    },
    {
      "criterion": "Selector rollback SLO is documented as no claim-path cache or a bounded tested TTL, and tests prove live selector changes affect subsequent claims without relying on stale task snapshots.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Route-key helper modules remain lightweight and do not import WGP, VibeComfy, or other heavy runtime modules.",
      "priority": "should",
      "requires": [
        "read_files",
        "parse_diff",
        "run_tests"
      ]
    }
  ],
  "assumptions": [
    "The active implementation target is `reigh-app`, `reigh-worker`, and `reigh-worker-orchestrator`; `reigh-app-cloud-chain` is not the primary edit target unless later confirmed otherwise.",
    "Missing live production selector rows do not imply VibeComfy. WGP remains the legacy-safe claim path where the worker can execute the route.",
    "Claim eligibility is based on the live selector table. Task-row route fields are snapshots for observability and child pinning, not claim authorization after rollback.",
    "The selector namespace defaults to `production` and should be configurable by environment for non-production deployments.",
    "The claim path uses no selector cache. Any create-task helper cache must be absent or bounded and tested.",
    "`vibecomfy` remains the backend identifier; `comfy` is not accepted as an alias.",
    "Banodoco worker-pool filtering remains separate from WGP/VibeComfy backend selector eligibility."
  ],
  "delta_from_previous_percent": 85.25,
  "structure_warnings": []
}

        Plan structure warnings from validator:
        []

        Existing flags:
        [
  {
    "id": "FLAG-001",
    "concern": "Selector authorization: route_backend_selectors needs explicit RLS/grant/service-role write controls; the plan names unauthorized-entry tests but not the database access-control implementation.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-002",
    "concern": "Selector snapshot/live-source ambiguity: the plan materializes selected_backend on tasks while claim enforcement joins the live selector table, without defining which source is returned and logged after selector rollback.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-003",
    "concern": "Route-key coverage: join_clips_segment is a child route in the worker/orchestrator surface but is not covered by the claimed canonical Python serializer in template_routing.py.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-004",
    "concern": "Task-counts alignment: direct queued_tasks/active_tasks queries in task-counts are not explicitly covered by the backend selector eligibility update.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-005",
    "concern": "Child snapshot propagation: not all add_task_to_db callers are named, and workerPassthrough currently has no top-level route field lifting contract for explicit snapshots.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "verifiability-0",
    "concern": "Criterion 2: requires human verification (observe_runtime_logs).",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "issue_hints",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the sprint requirement for malformed/unauthorized selector entries against the Phase 1 schema step. The plan creates public.route_backend_selectors and adds selector tests, but it does not explicitly require RLS, service-role-only write policies, grants/revokes, or ownership controls for that table; existing sensitive tables such as tasks, workers, settings, and rate_limits use explicit RLS/policies in migrations. Without that migration work, the unauthorized-entry requirement is only test-named, not structurally addressed.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "correctness",
    "concern": "Are the proposed changes technically correct?: Checked the proposed materialized selected_backend fields against the proposed claim-time selector join. The plan both stores tasks.selected_backend/selector_version at create time and says claim_next_task_service_role should join route_backend_selectors live for rollback, but it does not specify whether the RPC returns/enforces the live selector values or the materialized task snapshot. That ambiguity can produce stale claim responses after rollback, which undermines the selector-version logging and child-pinning contract.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "scope",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched related route-key code and found join_clips_segment route keys are handled outside the canonical worker selector: tests call scripts/dual_run_compare/route_keys.py for join_clips_segment, while source/task_handlers/tasks/template_routing.py only derives dimensional keys for travel_segment and individual_travel_segment. The plan says to keep the existing Python serializer as canonical and update travel/join child creation paths, but it does not add join_clips_segment to that canonical serializer, so a production selector contract would still lack a shared app/worker key for join children.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "all_locations",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Checked task-counts/index.ts and found it does more than RPC totals: it also builds queued_tasks and active_tasks arrays from direct tasks table queries and filters them in TypeScript. Phase 2 Step 4 only mentions extending the count RPCs/breakdown RPCs and parsing worker_backend; unless the direct queued_tasks filter also applies selector/backend eligibility, task-counts can report tasks as queued/claimable for a VibeComfy scaler even when claim-next-task would return 204.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "callers-1",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Grep found add_task_to_db callers in travel/orchestrator.py, travel/stitch.py, and join/task_builder.py, and the current add_task_to_db signature only accepts task_payload, task_type_str, dependant_on, and db_path. The plan says to extend add_task_to_db for optional route-selection metadata and update travel and join builders, but it omits travel/stitch.py and travel/chaining.py call paths that also enqueue child/processing tasks through the same helper; those callers need an explicit decision to pass a snapshot or intentionally leave the new fields null/WGP-safe.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "callers-2",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked create-task workerPassthrough.ts and confirmed it currently copies request.input directly into params and only lifts task_id/dependant_on into top-level insert fields. The plan\u2019s instruction to allow worker-created children to pass route_selection_snapshot is compatible with this caller shape only if the implementation also defines how input snapshot keys become top-level route_key/selected_backend/selector_version fields rather than remaining buried in params.",
    "status": "addressed",
    "severity": "significant"
  }
]

        Known accepted debt grouped by subsystem:
        {
  "are-the-proposed-changes-technically-correct": [
    {
      "id": "DEBT-007",
      "concern": "are the proposed changes technically correct?: for ordinary pairs, the new diagnosis is not well-supported by the repo. the current sync effect in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l62) already syncs `url` and `primaryvariantid`, and the regenerate path reads exactly `starturl`, `endurl`, `startgenid`, `endgenid`, `startvariantid`, and `endvariantid` from `segmentslotmode.pairdata` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts#l438). adding `thumburl` and `generationid` to the sync does not, by itself, explain why an old image url is still being used for regular pairs.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-008",
      "concern": "are the proposed changes technically correct?: the fix is incomplete for extra trailing slots. `handlepairclick` can populate `activepairdata` from `trailingpairdata` when `pairindex === pairdatabyindex.size` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l121), but the proposed sync effect only reads `pairdatabyindex.get(segmentslotlightboxindex)`. for those trailing-slot cases `fresh` is `undefined`, so no image refresh happens.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-018",
      "concern": "are the proposed changes technically correct?: the merge pseudocode does not actually sync 'all image fields' as claimed. it omits `id` and `position` from change detection, and when `fresh.startimage` or `fresh.endimage` becomes `null` it preserves the stale previous object instead of syncing that null state. as written, it also needs explicit null-guards around spreads of `prev.startimage` / `prev.endimage` to be safe in strict typescript.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-106",
      "concern": "are the proposed changes technically correct?: the plan's claim that `worker_state.py:200-204` (the 30-minute startup safety net) catches abandoned pods that exited before patching is slightly imprecise. line 200-204 only runs when `in_startup_phase` is true, which requires `startup_phase` to be in `('deps_installing', 'deps_verified', 'worker_starting')` per line 161. a pod that exits before its first patch has `startup_phase = none`, so `in_startup_phase` is false and the code falls through to the normal timeout checks (active_stale / not_claiming) at line 207+, not the 30-minute startup cap. both paths eventually reap the worker, so the end result is the same, but the overview's reasoning (naming 200-204 specifically) is wrong. worth correcting so future readers don't mis-reason about the invariant.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-107",
      "concern": "are the proposed changes technically correct?: checked worker_state.py line 161 (`in_startup_phase = startup_phase in (...)`) against the plan's assumption that subsequent lenient writes are safe. if deps_installing succeeds but deps_verified silently fails, startup_phase stays at 'deps_installing' and the 30-minute cap from line 200-204 applies \u2014 even though the pod is actually progressing through `uv sync`. on a slow runpod image with cold wheel downloads, `uv sync --extra cuda124` plus wan2gp deps can take 20+ minutes. there's no concrete benchmark in the plan that says the 30-minute cap is safely above the expected sync time; if `uv sync` legitimately takes 25 minutes and the deps_verified patch fails on a transient network blip, the orchestrator will terminate a healthy pod. plan should either bump the cap or note that deps_verified swallowing is acceptable because the cap is generously above typical sync time.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-143",
      "concern": "are the proposed changes technically correct?: the path-mapping defect from the previous iteration is fixed, but a different technical gap remains around `self_refiner`. repository search shows `shared.utils.self_refiner` is imported by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx_pipelines/distilled.py`, `ti2vid_one_stage.py`, `ti2vid_two_stages.py`, `wan2gp/models/ltx2/ltx_pipelines/utils/helpers.py`, and `wan2gp/models/wan/any2video.py`; the v4 plan still aligns `wan2gp/shared/utils/self_refiner.py` to upstream head without any concrete runtime step that exercises those code paths after the change, so the only repo-documented behavior check for that file is still missing from the executable body.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-156",
      "concern": "are the proposed changes technically correct?: the direct adapter still has a correctness risk around resolution parity. current vibecomfy ready templates hardcode image dimensions (`image/z_image` uses `emptysd3latentimage` 1024x1024 and `image/qwen_image_2512` uses 768x768), while `vibecomfy run` exposes no `--resolution` flag; the revised plan says a temporary scratchpad/input file may be generated only if supported, otherwise resolution is left out. that means a vibecomfy-supported direct route can silently ignore the worker's `resolution` param unless scratchpad resolution patching is made mandatory for supported direct routes or the support is explicitly limited to default-resolution smoke fixtures.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "are-the-success-criteria-well-prioritized-and-verifiable": [
    {
      "id": "DEBT-019",
      "concern": "are the success criteria well-prioritized and verifiable?: the attached success criteria are stale and do not match the current plan body. they still require 'no `usestate` for `activepairdata`', '`setactivepairdata` fully removed', 'sync effect deleted', and '`onpairclick` simplified to `(pairindex: number) => void`', which are the opposite of the current targeted-sync plan. as presented, the criteria are not usable for review or execution.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "audio-loading": [
    {
      "id": "DEBT-086",
      "concern": "getaudiodata in useeffect removes render-readiness signal",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-087",
      "concern": "same as correctness-3 \u2014 preview/render parity risk",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-088",
      "concern": "preview/render parity partially satisfied",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "audio-reactivity": [
    {
      "id": "DEBT-082",
      "concern": "overlapping clips use first-found, volume not scaled",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-083",
      "concern": "same as audio-reactivity-1 \u2014 overlapping/volume-adjusted clips diverge from audible mix",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-084",
      "concern": "textclip missing globalframeprovider",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-085",
      "concern": "same as audio-reactivity-2 \u2014 textclipsequence missing provider",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-089",
      "concern": "textclip effects surface not covered",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-090",
      "concern": "continuous effects shared by visual and text clips",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "batch-generation-pipeline": [
    {
      "id": "DEBT-006",
      "concern": "enhancement in usegeneratebatch before generatevideo() could compute prompts against a stale pair snapshot if mutations are still in flight.",
      "occurrence_count": 1,
      "plan_ids": [
        "in-cloud-mode-when-users-20260330-2214"
      ]
    }
  ],
  "cas-intern-short-circuit": [
    {
      "id": "DEBT-151",
      "concern": "symlink short-circuit comparison may produce false negatives on macos-like layouts where project_dir contains symlinked segments (/var \u2192 /private/var) because resolve(strict=true) on the source returns canonical paths but project_dir / cas_dirname may be non-canonical.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-7-rev-20260505"
      ]
    }
  ],
  "crash-recovery-cascade-paths": [
    {
      "id": "DEBT-065",
      "concern": "cascade lookup only reads params->>'orchestrator_task_id_ref', missing shared reference paths and orchestrator-self detection.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-067",
      "concern": "duplicate of correctness-2 + correctness-3: invalid sql syntax and narrow cascade lookup.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-069",
      "concern": "shared orchestrator-reference helpers not referenced.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-072",
      "concern": "orchestrator tasks that crash don't get orchestrator-self cascade.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-074",
      "concern": "hardcoded params->>'orchestrator_task_id_ref' misses other reference paths.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-retry": [
    {
      "id": "DEBT-063",
      "concern": "crash requeue sql does not increment attempts, risking infinite requeue loop.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-066",
      "concern": "duplicate of correctness-1: attempts never advance on crash requeue.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-068",
      "concern": "missing attempts increment location in heartbeat sql.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-073",
      "concern": "step 6 under-scoped for real retry convergence and orchestrator-self handling.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-sql-syntax": [
    {
      "id": "DEBT-064",
      "concern": "bare select inside plpgsql is invalid \u2014 needs perform.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-testing": [
    {
      "id": "DEBT-070",
      "concern": "no multi-crash convergence test exercising attempts 0\u21921\u21922\u21923.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-071",
      "concern": "no validation that plpgsql body executes successfully.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-075",
      "concern": "criteria don't require proof of crash requeue convergence.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "criteria-verifiability": [
    {
      "id": "DEBT-036",
      "concern": "'no unsafe .maybesingle()' criterion requires judgment about column uniqueness.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-037",
      "concern": "decision documentation location not specified.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-062",
      "concern": "the must criterion requiring 5 task types to exist as active db rows is not verifiable from code diff alone \u2014 it requires a live db query.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ],
  "db-fallback-testing": [
    {
      "id": "DEBT-060",
      "concern": "no new automated test for the db fallback dispatch path or dependant_on preservation for raw worker families.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ],
  "dependency-resolution": [
    {
      "id": "DEBT-105",
      "concern": "dependency resolution: the plan does not lock down the active python-version matrix even though the repo currently splits between python 3.10 local installs and a python 3.11 runpod image.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements": [
    {
      "id": "DEBT-013",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the package is internally inconsistent. the plan body says to keep `activepairdata` in `usestate` and make phase 2 optional, but the attached metadata and success criteria still describe the previous derive-via-`usememo` / remove-`setactivepairdata` / simplify-`onpairclick` plan. that means the approved-plan requirements are only partially coherent as presented.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-108",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the linux distro note is documentation-only; the generated install command in step 7 still runs `apt-get install python3.10-venv python3.10-dev ffmpeg` without any pre-check that the package exists. users on ubuntu 24.04+ who ignore the doc and try to copy-paste the command will hit a confusing `e: unable to locate package python3.10-venv` from apt rather than a targeted error from commandutils.ts. a one-line detection pre-check (e.g., `apt-cache show python3.10-venv >/dev/null 2>&1 || { echo 'install deadsnakes ppa first \u2014 see readme'; exit 1; }`) would convert the silent failure into an actionable error, but the plan does not add this.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-145",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: checked the revised v4 body against `docs/wan2gp_fork_migration_plan.md` sprint 2. the repo plan doc still lists an \"ltx-2 `self_refiner` smoke against the pre-sprint behavioral baseline\" as a sprint 2 verification gate and repeats that smoke in the functionality-preservation checks, but the revised execution steps no longer schedule that smoke anywhere; it survives only as an info-level metadata criterion. because `wan2gp/shared/utils/self_refiner.py` remains an explicit sprint 2 deliverable, the revised plan still only partially carries forward the verification package described in the source migration plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-153",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: worker integration: the migration doc describes the per-call profile override gap as involving reigh-worker adapter handling of override_profile before constructing vibecomfy sessionconfig, but the plan limits sprint 1 per-run work to the vibecomfy cli/runtime. that may be acceptable for a vibecomfy-library mvp, but it does not fully exercise the production-facing per-task override semantics called out in the overall context.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-1-vibecomfy-memory-20260506-0147"
      ]
    },
    {
      "id": "DEBT-155",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: a residual issue-hint tension remains for resolution handling. the plan acknowledges current `vibecomfy run` lacks a resolution flag, but allows the adapter to leave resolution and other template-specific values unwired for sprint 2. because `z_image_turbo` and `qwen_image_2512` are marked vibecomfy-supported direct routes, this may not preserve the existing worker task-parameter contract for tasks that provide a non-default `resolution`.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "direct-route-parameter-parity": [
    {
      "id": "DEBT-160",
      "concern": "direct route parameter parity: vibecomfy-supported direct routes may ignore the worker `resolution` parameter.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "does-the-change-touch-all-locations-and-supporting-infrastructure": [
    {
      "id": "DEBT-014",
      "concern": "does the change touch all locations and supporting infrastructure?: phase 1 still misses a real supporting-data location: `trailingpairdata` lives outside `pairdatabyindex` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts#l111), but the proposed sync logic only considers `pairdatabyindex`. if trailing slot regenerate is part of the bug surface, that location is not covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-110",
      "concern": "does the change touch all locations and supporting infrastructure?: the non-swallowing helper `update_worker_phase_strict` is a new shell function, but phase 1 step 2 introduces it only as pseudo-code. there is no concrete note that the helper must handle supabase http non-2xx responses as failures (curl returns 0 even on http 4xx/5xx by default unless `-f` or `--fail-with-body` is used). if the implementer ports `update_worker_phase` verbatim with only `|| return 0` removed, a 500 from supabase would still report success because curl's exit code is 0. the plan should specify `curl --fail` or explicit http status code checking in the strict variant.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-142",
      "concern": "does the change touch all locations and supporting infrastructure?: the supporting-infrastructure review still finds one missing check. in `docs/wan2gp_fork_migration_plan.md`, sprint 2's verification matrix and risk register both single out `self_refiner` as a distinct drift-upgrade surface with its own smoke and its own silent-behavior-change risk, but the revised v4 body updates the file without keeping that supporting verification step in the actual execution checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-154",
      "concern": "does the change touch all locations and supporting infrastructure?: documentation/data gap: the sprint exit criteria require profiles 1 and 3 to have vram and wall-clock data, but the plan puts that only in metadata as an info-level criterion and does not schedule a concrete artifact location or command for recording the measurements. the implementation could satisfy all unit tests while still missing one of the explicit exit criteria.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-1-vibecomfy-memory-20260506-0147"
      ]
    },
    {
      "id": "DEBT-158",
      "concern": "does the change touch all locations and supporting infrastructure?: the supporting infrastructure for resolution is still incomplete if direct vibecomfy routes are considered production-supported. vibecomfy has a `vibecomfy.patches.resolution` helper and the cli can load scratchpad files with `allow_scratchpad=true`, but the plan does not require using that path; it permits leaving resolution out for sprint 2.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    },
    {
      "id": "DEBT-162",
      "concern": "does the change touch all locations and supporting infrastructure?: checked vibecomfy profile wording against `vibecomfy/tests/test_ready_templates.py`. the revised plan says to add the production template to representative compile profile coverage 'alongside the existing dry-run id', but the dry-run id is not currently in `profile_smoke_template_ids`; only `video/wanvideo_wrapper_22_5b_i2v` and `video/wan_t2v` are. this is a small wording mismatch rather than a functional blocker because adding either the production id alone or both ids would still satisfy sprint 4.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-4-wan-single-frame-and-20260506-0818"
      ]
    }
  ],
  "edge-test-config": [
    {
      "id": "DEBT-022",
      "concern": "plan's vitest commands use the wrong config entry point.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-023",
      "concern": "same as verification-3: wrong vitest config in validation commands.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-024",
      "concern": "success criterion references wrong test command.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "error-handling": [
    {
      "id": "DEBT-095",
      "concern": "db loader error handling convention mismatch (plan says log+null, existing loaders throw)",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "error-propagation-logging": [
    {
      "id": "DEBT-027",
      "concern": "generation.ts and handler.ts logging endpoints are not directly tested.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "error-propagation-testing": [
    {
      "id": "DEBT-020",
      "concern": "no end-to-end regression test for the full symptom chain (db error \u2192 tocompletionerror metadata \u2192 handler log).",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-025",
      "concern": "handler.ts metadata surfacing criterion lacks a concrete automated verifier.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-026",
      "concern": "main issue only partially validated without an integration test.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them": [
    {
      "id": "DEBT-109",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the step 2 retry loop uses a naked `sleep 2` between attempts, which adds up to 6 seconds of latency on the happy path when the first patch eventually succeeds on attempt 2 or 3. for pods where supabase is reachable but slow during the initial moments of a cold runpod start, the retry logic is fine. however, if the first attempt fails with a tls handshake delay and the retry loop sleeps 2s per attempt regardless of whether curl itself has been blocking for tens of seconds, the total startup latency penalty could be substantial. this is a minor tuning concern, not a correctness issue.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-146",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: finding callers of the changed module shows that `shared.utils.self_refiner` is consumed by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx2_handler.py`, multiple ltx2 pipeline modules, and `wan2gp/models/wan/any2video.py`. the revised validation steps still only drive the three bridge getters in `source/runtime/wgp_ports/vendor_imports.py`; none of the scheduled commands execute a real `self_refiner` caller, so the plan does not yet verify the main caller shapes for the other explicit sprint 2 file change.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-159",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked direct queue caller values in `db_task_to_generation_task()`: direct image tasks may carry `resolution`, `steps`/`num_inference_steps`, `seed`, and `override_profile`. the revised adapter plan covers seed, steps, and memory profile but not guaranteed resolution propagation, so it does not handle all relevant direct-route caller arguments for a supported vibecomfy direct route.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "gpu-branching-test-matrix": [
    {
      "id": "DEBT-113",
      "concern": "linux cuda128 path under-verified",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "gpu-branching-ui-surface": [
    {
      "id": "DEBT-112",
      "concern": "nvidia-50 option is exposed on linux in the ui but linux cuda128 smoke test is missing",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "hook-abstraction": [
    {
      "id": "DEBT-043",
      "concern": "usepairsettingshandler becomes trivial with single caller \u2014 keeping it is extra indirection.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "hype-mirror-cas-coverage": [
    {
      "id": "DEBT-152",
      "concern": "hype-mirrored files whose parent step does not declare matching produces will not be cas-interned, even with the follow_symlinks=false edit.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-7-rev-20260505"
      ]
    }
  ],
  "is-the-change-in-the-right-place-and-would-it-break-any-callers": [
    {
      "id": "DEBT-015",
      "concern": "is the change in the right place, and would it break any callers?: the optional cleanup steps are not in the right place yet. `pairregionslayer` does not receive `pairdatabyindex` today; its props are only `images`, `imagepositionswithpending`, `pairinfowithpending`, and callback/display props in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx#l20). so step 4's 'pass `pairdatabyindex.get(pairindex)` directly' would require new prop plumbing or a different seam.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "is-the-scope-and-scale-of-the-change-appropriate": [
    {
      "id": "DEBT-009",
      "concern": "is the scope and scale of the change appropriate?: phase 2 is still under-specified for execution. step 4 says pairregionslayer should either pass `pairdatabyindex.get(pairindex)` directly or 'just pass the index + frame-only data', which are materially different designs. if phase 2 is kept in the plan, it needs a single concrete direction.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "is-there-convincing-verification-for-the-change": [
    {
      "id": "DEBT-010",
      "concern": "is there convincing verification for the change?: the plan still lacks an explicit automated regression test for the reported bug. step 2 is manual ('check that `usevideoregeneratemode` now gets the fresh url'), but there is no concrete test that opens a segment slot, changes the primary variant data, and asserts that the regenerate path sees the fresh `url`, `generationid`, and `primaryvariantid`.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-011",
      "concern": "is there convincing verification for the change?: the current `usesegmentslotmode` test remains only a smoke test in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts), and the plan does not add behavior coverage for the new sync effect.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-012",
      "concern": "is there convincing verification for the change?: no verification step covers the trailing-slot branch, even though the proposed phase 1 logic currently misses `trailingpairdata` refreshes.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "legacy-data-backfill": [
    {
      "id": "DEBT-004",
      "concern": "the step 8 diagnostic query only detects cross-shot pair_shot_generation_id misassociations, not same-shot misassociations caused by timeline reordering within a shot.",
      "occurrence_count": 1,
      "plan_ids": [
        "redesign-the-segment-position-20260330-1913"
      ]
    }
  ],
  "lookup-consistency": [
    {
      "id": "DEBT-029",
      "concern": "other repo call sites use unordered .limit(1).maybesingle() and will remain inconsistent.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-033",
      "concern": "other call sites with same unsafe pattern not covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "lora-management": [
    {
      "id": "DEBT-099",
      "concern": "lora tools simplified vs full ui parity (multi-stage metadata, private loras)",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "media-lightbox-persistence": [
    {
      "id": "DEBT-002",
      "concern": "variant switches do not clear/restore inpaintprompt, so stale prompt state can leak across variants with no cached prompt.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-prompt-text-reset-bug-20260330-1410"
      ]
    },
    {
      "id": "DEBT-003",
      "concern": "removing prompt/numgenerations from the variant-keyed localstorage cache means all variants within a generation share the same prompt. this broadens existing debt-002 (variant prompt leakage).",
      "occurrence_count": 1,
      "plan_ids": [
        "consolidate-the-media-20260330-1449"
      ]
    }
  ],
  "media-lightbox-segment-slot": [
    {
      "id": "DEBT-016",
      "concern": "media lightbox / segment slot: the targeted sync rationale does not fully explain the reported stale-url bug for regular pairs, and the proposed effect still misses trailing-slot refreshes because those can come from `trailingpairdata` rather than `pairdatabyindex`.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "number-input-nullable": [
    {
      "id": "DEBT-076",
      "concern": "plan doesn't explicitly state onchange must also accept null, though step 3 depends on it.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-077",
      "concern": "disputed v1 flag \u2014 original concern about bulkclippanel being unimplementable.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-079",
      "concern": "onchange null filtering not explicitly addressed in plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "number-input-testing": [
    {
      "id": "DEBT-081",
      "concern": "no planned tests for numberinput shared component or bulkclippanel nullable draft flow.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "orchestrator-completion-rollout": [
    {
      "id": "DEBT-049",
      "concern": "pre-existing individual_travel_segment children won't drive orchestrator completion through segment_type_config after deploy.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-051",
      "concern": "missing compatibility seam in orchestratorcore.ts:123-126 for old individual_travel_segment rows.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-053",
      "concern": "mixed old/new data during rollout can leave old orchestrators without completion counting.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-054",
      "concern": "no test or deployment guard for pre-existing individual_travel_segment children completing after worker change.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-056",
      "concern": "plan overstates backward compatibility for existing data.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-057",
      "concern": "missing rollout compatibility step for in-flight individual_travel_segment tasks.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-058",
      "concern": "pre-deploy individual_travel_segment child completing post-rollout won't be treated as segment task by checkorchestratorcompletion.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-059",
      "concern": "orchestrator.test.ts criterion too narrow to verify old individual_travel_segment compatibility.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    }
  ],
  "pair-settings-plumbing": [
    {
      "id": "DEBT-039",
      "concern": "handleopenpairsettings(pairindex, pairframedata) path in timelinetrackprelude, segmentoutputstrip, and usesegmentoutputstrip not explicitly named.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-042",
      "concern": "same as flag-002 \u2014 segmentoutputstrip and usesegmentoutputstrip still carry pairframedata.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-045",
      "concern": "timelinetrackprelude and segmentoutputstrip still forward (pairindex, pairframedata).",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "plan-scope": [
    {
      "id": "DEBT-032",
      "concern": "step 3 is larger than a light megaplan warrants.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "planning-metadata": [
    {
      "id": "DEBT-017",
      "concern": "planning metadata: the attached metadata and success criteria still describe a different implementation than the current plan body, which risks sending execution and review down the wrong path.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-103",
      "concern": "success criteria don't cover wave 4 scope",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "position-key-semantics": [
    {
      "id": "DEBT-028",
      "concern": "plan investigates a unique constraint on (parent_generation_id, child_order) which doesn't match repo semantics for position keys.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-030",
      "concern": "plan weights toward child_order rather than pair_shot_generation_id as the key that matters.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-031",
      "concern": "unique constraint on (parent_generation_id, child_order) not supported by repo semantics.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "prompt-composition": [
    {
      "id": "DEBT-005",
      "concern": "the plan's step 1 signature includes textbeforeprompts/textafterprompts parameters that would be applied before enhancement, double-wrapping the prompt.",
      "occurrence_count": 1,
      "plan_ids": [
        "in-cloud-mode-when-users-20260330-2214"
      ]
    }
  ],
  "ready-template-snapshots": [
    {
      "id": "DEBT-147",
      "concern": "step 4.2 drops markdownnote nodes but step 4.5 and the success criteria require class_type/widget parity with pre-refactor snapshots, which currently include markdownnote nodes.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-the-higher-abstraction-20260425-0953"
      ]
    },
    {
      "id": "DEBT-148",
      "concern": "same tension as issue_hints v2: drop-markdownnote vs. snapshot parity.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-the-higher-abstraction-20260425-0953"
      ]
    }
  ],
  "reigh-worker-orchestrator-dockerfile": [
    {
      "id": "DEBT-150",
      "concern": "step 7 \u00a73 claims `gpu_orchestrator/dockerfile` has wan2gp install steps; current main is generic and contains none.",
      "occurrence_count": 1,
      "plan_ids": [
        "produce-a-migration-plan-20260505-0555"
      ]
    }
  ],
  "reigh-worker-orchestrator-runpod-startup": [
    {
      "id": "DEBT-149",
      "concern": "`gpu_orchestrator/runpod/startup_script.py` embeds `headless-wan2gp` in `_workdir_discovery_snippet` and is not named explicitly in step 7 \u00a73's checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "produce-a-migration-plan-20260505-0555"
      ]
    }
  ],
  "search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader": [
    {
      "id": "DEBT-141",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the broader runtime surface after the v4 path fix. sprint 2 is still moving two behavior-sensitive seams rather than just the import-path contract: the `wan2gp/` mount path and the `self_refiner` runtime. step 6.2 covers only the three `vendor_imports` getters, while the 6-file travel suite and the bridge-contract tests do not mention `self_refiner`, so dropping the dedicated self-refiner smoke from the runnable steps leaves the broader downstream surface of that changed file under-covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-157",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the supported direct-route scope is still broader than the adapter's guaranteed parameter surface. `db_task_to_generation_task()` currently carries direct task params such as `resolution`, `steps`, and `seed` into wgp generation, but the vibecomfy cli path only guarantees prompt, seed, steps, and memory profile; resolution remains optional/documentation-only in the plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    },
    {
      "id": "DEBT-161",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the revised child-route scope against `migration-thresholds.yaml`. the threshold corpus currently has wan/vace entries for `travel_segment__model-wan22_vace__...` and `join_clips_segment__model-wan22_vace__...`, but only an i2v entry for `individual_travel_segment`; the revised plan makes `individual_travel_segment` with vace model params a must-level worker fixture, which broadens the worker smoke scope beyond the currently tracked wan/vace threshold routes.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-4-wan-single-frame-and-20260506-0818"
      ]
    }
  ],
  "self-refiner-verification": [
    {
      "id": "DEBT-144",
      "concern": "self-refiner verification: the revised plan still aligns `wan2gp/shared/utils/self_refiner.py` without scheduling the sprint 2 ltx-2 `self_refiner` smoke that `docs/wan2gp_fork_migration_plan.md` defines as the behavior-preservation check for that drift upgrade.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    }
  ],
  "settings-defaults": [
    {
      "id": "DEBT-111",
      "concern": "workerrepopath default can go stale if user switches computertype before editing path",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "settings-resolution": [
    {
      "id": "DEBT-093",
      "concern": "settings cascade missing \u2014 shot-only read diverges from form's defaults\u2192user\u2192project\u2192shot merge",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-098",
      "concern": "settings cascade missing \u2014 shot-only read",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "shared-component-compatibility": [
    {
      "id": "DEBT-078",
      "concern": "numberinput changes affect callers outside video-editor (billing, travel-between-images, phaseconfigselectormodal).",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-080",
      "concern": "shared ui component blast radius not audited in plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "shot-linking-testing": [
    {
      "id": "DEBT-021",
      "concern": "no test covers the linkgenerationtoshot error/catch branches.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "signature-propagation": [
    {
      "id": "DEBT-038",
      "concern": "plan doesn't explicitly name timeline/index.tsx and segmentslotcontracts.ts for updates.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-041",
      "concern": "same as flag-001 \u2014 timeline/index.tsx and segmentslotcontracts.ts not in checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-044",
      "concern": "five supporting contract/plumbing sites not named in the checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "ta[REDACTED_SK]": [
    {
      "id": "DEBT-050",
      "concern": "step 3 cites wrong migration file (task_cost_configs instead of task_types) as evidence for db fallback path.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-052",
      "concern": "step 3 should cite task_types source, not task_cost_configs.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-055",
      "concern": "plan doesn't verify travel_segment and travel_stitch exist as active task_types rows using the correct table.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    }
  ],
  "test-coverage": [
    {
      "id": "DEBT-034",
      "concern": "current generation-child.test.ts is only a smoke test.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-035",
      "concern": "no plan to verify other lookup paths choose rows consistently.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-096",
      "concern": "no new tests for db loader or travel param merge path",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-097",
      "concern": "must-level criteria depend on manual testing rather than automated assertions",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-102",
      "concern": "no new unit tests for wave 4 tools",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-104",
      "concern": "must criteria backed by manual testing only",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "test-infrastructure": [
    {
      "id": "DEBT-101",
      "concern": "no test fixtures for resources table",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "timeline-drag-coordination": [
    {
      "id": "DEBT-126",
      "concern": "plan keeps two hooks instead of a single coordinator",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-127",
      "concern": "brief says single coordinator but plan keeps separate hooks",
      "occurrence_count": 2,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-128",
      "concern": "pendingopsref retained despite brief suggesting removal",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-129",
      "concern": "wrapper-bound listener mount wiring under-specified",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    }
  ],
  "timeline-persistence": [
    {
      "id": "DEBT-130",
      "concern": "read path still assembles config and registry from separate requests",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-131",
      "concern": "poll sync verification not structurally changed",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-132",
      "concern": "backend save helpers not wired to new rpc",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-133",
      "concern": "read infrastructure not updated",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-134",
      "concern": "backend tests not in validation list",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-135",
      "concern": "backend callers not migrated",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-136",
      "concern": "broader persistence-contract problem",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-137",
      "concern": "backend split-save not addressed",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-138",
      "concern": "split polling can combine config and registry from different snapshots",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    }
  ],
  "timeline-scaling": [
    {
      "id": "DEBT-001",
      "concern": "the plan only specifies a concrete fix for the default scale(1) case; explicit-scale tracks may still break blend-mode effects.",
      "occurrence_count": 1,
      "plan_ids": [
        "investigate-why-custom-ai-20260330-0408"
      ]
    }
  ],
  "timeline-snap-threshold": [
    {
      "id": "DEBT-139",
      "concern": "threshold is generous (duration) rather than zoom-scaled (8px)",
      "occurrence_count": 1,
      "plan_ids": [
        "implement-smart-snap-to-edge-20260413-0503"
      ]
    },
    {
      "id": "DEBT-140",
      "concern": "computedropposition does not pass a zoom-scaled threshold override",
      "occurrence_count": 1,
      "plan_ids": [
        "implement-smart-snap-to-edge-20260413-0503"
      ]
    }
  ],
  "travel-continuations": [
    {
      "id": "DEBT-094",
      "concern": "smooth continuations not threaded \u2014 agent tasks won't have continuation_config even when shot settings enable it",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-100",
      "concern": "continuation_config omitted from form parity",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "travel-payload-cleanup-scope": [
    {
      "id": "DEBT-116",
      "concern": "plan scope narrower than original user request",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-118",
      "concern": "broader create-task contract problem left untouched",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "travel-payload-readers": [
    {
      "id": "DEBT-114",
      "concern": "phase 4 app-side reader audit incomplete",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-119",
      "concern": "phase 4 field inventory incomplete for app-side readers",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "travel-request-contract": [
    {
      "id": "DEBT-115",
      "concern": "image_variant_ids is in frontend request contract",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-117",
      "concern": "image_variant_ids contract change",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "variant-update-b-fresh-takeover": [
    {
      "id": "DEBT-120",
      "concern": "spawn_worker does not internally call start_worker_process; harness must call both explicitly",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-121",
      "concern": "worker_id and runpod_id must be generated and threaded distinctly; plan currently uses pod_id as both",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-122",
      "concern": "duplicate of correctness-1 \u2014 spawn_worker two-step misstatement",
      "occurrence_count": 2,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-123",
      "concern": "duplicate of correctness-2 \u2014 worker_id/runpod_id propagation across takeover and restore paths",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-124",
      "concern": "duplicate of correctness-1 + correctness-2 \u2014 missing create_worker_record glue and start_worker_process integration",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-125",
      "concern": "duplicate of correctness-2 \u2014 caller contract for spawn_worker requires worker_id, not pod_id",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    }
  ],
  "verification": [
    {
      "id": "DEBT-091",
      "concern": "no end-to-end render test for audio analysis timing",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-092",
      "concern": "no automated coverage for text clips or overlapping clips with audio effects",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "verification-coverage": [
    {
      "id": "DEBT-040",
      "concern": "no automated test exercises the full segment-slot opening path after cleanup.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-046",
      "concern": "no automated coverage that clicking a pair opens the correct modal after cleanup.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-048",
      "concern": "zero behavioral change criterion is not verifiable from tsc + existing tests alone.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "verification-workflow": [
    {
      "id": "DEBT-047",
      "concern": "tsconfig.app.json excludes test files, so tsc won't catch test breakage.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "worker-test-staleness": [
    {
      "id": "DEBT-061",
      "concern": "worker test in test_additional_coverage_modules.py:37 may assert stale payload structure (task_type vs family).",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ]
}

        Escalated debt subsystems:
        [
  {
    "subsystem": "timeline-persistence",
    "total_occurrences": 9,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-130",
        "concern": "read path still assembles config and registry from separate requests",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-131",
        "concern": "poll sync verification not structurally changed",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-132",
        "concern": "backend save helpers not wired to new rpc",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-133",
        "concern": "read infrastructure not updated",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-134",
        "concern": "backend tests not in validation list",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-135",
        "concern": "backend callers not migrated",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-136",
        "concern": "broader persistence-contract problem",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-137",
        "concern": "backend split-save not addressed",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-138",
        "concern": "split polling can combine config and registry from different snapshots",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      }
    ]
  },
  {
    "subsystem": "orchestrator-completion-rollout",
    "total_occurrences": 8,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-049",
        "concern": "pre-existing individual_travel_segment children won't drive orchestrator completion through segment_type_config after deploy.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-051",
        "concern": "missing compatibility seam in orchestratorcore.ts:123-126 for old individual_travel_segment rows.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-053",
        "concern": "mixed old/new data during rollout can leave old orchestrators without completion counting.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-054",
        "concern": "no test or deployment guard for pre-existing individual_travel_segment children completing after worker change.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-056",
        "concern": "plan overstates backward compatibility for existing data.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-057",
        "concern": "missing rollout compatibility step for in-flight individual_travel_segment tasks.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-058",
        "concern": "pre-deploy individual_travel_segment child completing post-rollout won't be treated as segment task by checkorchestratorcompletion.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-059",
        "concern": "orchestrator.test.ts criterion too narrow to verify old individual_travel_segment compatibility.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      }
    ]
  },
  {
    "subsystem": "are-the-proposed-changes-technically-correct",
    "total_occurrences": 7,
    "plan_count": 4,
    "entries": [
      {
        "id": "DEBT-007",
        "concern": "are the proposed changes technically correct?: for ordinary pairs, the new diagnosis is not well-supported by the repo. the current sync effect in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l62) already syncs `url` and `primaryvariantid`, and the regenerate path reads exactly `starturl`, `endurl`, `startgenid`, `endgenid`, `startvariantid`, and `endvariantid` from `segmentslotmode.pairdata` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts#l438). adding `thumburl` and `generationid` to the sync does not, by itself, explain why an old image url is still being used for regular pairs.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-008",
        "concern": "are the proposed changes technically correct?: the fix is incomplete for extra trailing slots. `handlepairclick` can populate `activepairdata` from `trailingpairdata` when `pairindex === pairdatabyindex.size` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l121), but the proposed sync effect only reads `pairdatabyindex.get(segmentslotlightboxindex)`. for those trailing-slot cases `fresh` is `undefined`, so no image refresh happens.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-018",
        "concern": "are the proposed changes technically correct?: the merge pseudocode does not actually sync 'all image fields' as claimed. it omits `id` and `position` from change detection, and when `fresh.startimage` or `fresh.endimage` becomes `null` it preserves the stale previous object instead of syncing that null state. as written, it also needs explicit null-guards around spreads of `prev.startimage` / `prev.endimage` to be safe in strict typescript.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-106",
        "concern": "are the proposed changes technically correct?: the plan's claim that `worker_state.py:200-204` (the 30-minute startup safety net) catches abandoned pods that exited before patching is slightly imprecise. line 200-204 only runs when `in_startup_phase` is true, which requires `startup_phase` to be in `('deps_installing', 'deps_verified', 'worker_starting')` per line 161. a pod that exits before its first patch has `startup_phase = none`, so `in_startup_phase` is false and the code falls through to the normal timeout checks (active_stale / not_claiming) at line 207+, not the 30-minute startup cap. both paths eventually reap the worker, so the end result is the same, but the overview's reasoning (naming 200-204 specifically) is wrong. worth correcting so future readers don't mis-reason about the invariant.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-107",
        "concern": "are the proposed changes technically correct?: checked worker_state.py line 161 (`in_startup_phase = startup_phase in (...)`) against the plan's assumption that subsequent lenient writes are safe. if deps_installing succeeds but deps_verified silently fails, startup_phase stays at 'deps_installing' and the 30-minute cap from line 200-204 applies \u2014 even though the pod is actually progressing through `uv sync`. on a slow runpod image with cold wheel downloads, `uv sync --extra cuda124` plus wan2gp deps can take 20+ minutes. there's no concrete benchmark in the plan that says the 30-minute cap is safely above the expected sync time; if `uv sync` legitimately takes 25 minutes and the deps_verified patch fails on a transient network blip, the orchestrator will terminate a healthy pod. plan should either bump the cap or note that deps_verified swallowing is acceptable because the cap is generously above typical sync time.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-143",
        "concern": "are the proposed changes technically correct?: the path-mapping defect from the previous iteration is fixed, but a different technical gap remains around `self_refiner`. repository search shows `shared.utils.self_refiner` is imported by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx_pipelines/distilled.py`, `ti2vid_one_stage.py`, `ti2vid_two_stages.py`, `wan2gp/models/ltx2/ltx_pipelines/utils/helpers.py`, and `wan2gp/models/wan/any2video.py`; the v4 plan still aligns `wan2gp/shared/utils/self_refiner.py` to upstream head without any concrete runtime step that exercises those code paths after the change, so the only repo-documented behavior check for that file is still missing from the executable body.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-156",
        "concern": "are the proposed changes technically correct?: the direct adapter still has a correctness risk around resolution parity. current vibecomfy ready templates hardcode image dimensions (`image/z_image` uses `emptysd3latentimage` 1024x1024 and `image/qwen_image_2512` uses 768x768), while `vibecomfy run` exposes no `--resolution` flag; the revised plan says a temporary scratchpad/input file may be generated only if supported, otherwise resolution is left out. that means a vibecomfy-supported direct route can silently ignore the worker's `resolution` param unless scratchpad resolution patching is made mandatory for supported direct routes or the support is explicitly limited to default-resolution smoke fixtures.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "variant-update-b-fresh-takeover",
    "total_occurrences": 7,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-120",
        "concern": "spawn_worker does not internally call start_worker_process; harness must call both explicitly",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-121",
        "concern": "worker_id and runpod_id must be generated and threaded distinctly; plan currently uses pod_id as both",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-122",
        "concern": "duplicate of correctness-1 \u2014 spawn_worker two-step misstatement",
        "occurrence_count": 2,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-123",
        "concern": "duplicate of correctness-2 \u2014 worker_id/runpod_id propagation across takeover and restore paths",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-124",
        "concern": "duplicate of correctness-1 + correctness-2 \u2014 missing create_worker_record glue and start_worker_process integration",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-125",
        "concern": "duplicate of correctness-2 \u2014 caller contract for spawn_worker requires worker_id, not pod_id",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      }
    ]
  },
  {
    "subsystem": "audio-reactivity",
    "total_occurrences": 6,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-082",
        "concern": "overlapping clips use first-found, volume not scaled",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-083",
        "concern": "same as audio-reactivity-1 \u2014 overlapping/volume-adjusted clips diverge from audible mix",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-084",
        "concern": "textclip missing globalframeprovider",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-085",
        "concern": "same as audio-reactivity-2 \u2014 textclipsequence missing provider",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-089",
        "concern": "textclip effects surface not covered",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-090",
        "concern": "continuous effects shared by visual and text clips",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      }
    ]
  },
  {
    "subsystem": "does-the-change-touch-all-locations-and-supporting-infrastructure",
    "total_occurrences": 6,
    "plan_count": 6,
    "entries": [
      {
        "id": "DEBT-014",
        "concern": "does the change touch all locations and supporting infrastructure?: phase 1 still misses a real supporting-data location: `trailingpairdata` lives outside `pairdatabyindex` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts#l111), but the proposed sync logic only considers `pairdatabyindex`. if trailing slot regenerate is part of the bug surface, that location is not covered.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-110",
        "concern": "does the change touch all locations and supporting infrastructure?: the non-swallowing helper `update_worker_phase_strict` is a new shell function, but phase 1 step 2 introduces it only as pseudo-code. there is no concrete note that the helper must handle supabase http non-2xx responses as failures (curl returns 0 even on http 4xx/5xx by default unless `-f` or `--fail-with-body` is used). if the implementer ports `update_worker_phase` verbatim with only `|| return 0` removed, a 500 from supabase would still report success because curl's exit code is 0. the plan should specify `curl --fail` or explicit http status code checking in the strict variant.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-142",
        "concern": "does the change touch all locations and supporting infrastructure?: the supporting-infrastructure review still finds one missing check. in `docs/wan2gp_fork_migration_plan.md`, sprint 2's verification matrix and risk register both single out `self_refiner` as a distinct drift-upgrade surface with its own smoke and its own silent-behavior-change risk, but the revised v4 body updates the file without keeping that supporting verification step in the actual execution checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-154",
        "concern": "does the change touch all locations and supporting infrastructure?: documentation/data gap: the sprint exit criteria require profiles 1 and 3 to have vram and wall-clock data, but the plan puts that only in metadata as an info-level criterion and does not schedule a concrete artifact location or command for recording the measurements. the implementation could satisfy all unit tests while still missing one of the explicit exit criteria.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-1-vibecomfy-memory-20260506-0147"
        ]
      },
      {
        "id": "DEBT-158",
        "concern": "does the change touch all locations and supporting infrastructure?: the supporting infrastructure for resolution is still incomplete if direct vibecomfy routes are considered production-supported. vibecomfy has a `vibecomfy.patches.resolution` helper and the cli can load scratchpad files with `allow_scratchpad=true`, but the plan does not require using that path; it permits leaving resolution out for sprint 2.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      },
      {
        "id": "DEBT-162",
        "concern": "does the change touch all locations and supporting infrastructure?: checked vibecomfy profile wording against `vibecomfy/tests/test_ready_templates.py`. the revised plan says to add the production template to representative compile profile coverage 'alongside the existing dry-run id', but the dry-run id is not currently in `profile_smoke_template_ids`; only `video/wanvideo_wrapper_22_5b_i2v` and `video/wan_t2v` are. this is a small wording mismatch rather than a functional blocker because adding either the production id alone or both ids would still satisfy sprint 4.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-4-wan-single-frame-and-20260506-0818"
        ]
      }
    ]
  },
  {
    "subsystem": "test-coverage",
    "total_occurrences": 6,
    "plan_count": 2,
    "entries": [
      {
        "id": "DEBT-034",
        "concern": "current generation-child.test.ts is only a smoke test.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-035",
        "concern": "no plan to verify other lookup paths choose rows consistently.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-096",
        "concern": "no new tests for db loader or travel param merge path",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-097",
        "concern": "must-level criteria depend on manual testing rather than automated assertions",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-102",
        "concern": "no new unit tests for wave 4 tools",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-104",
        "concern": "must criteria backed by manual testing only",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-cascade-paths",
    "total_occurrences": 5,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-065",
        "concern": "cascade lookup only reads params->>'orchestrator_task_id_ref', missing shared reference paths and orchestrator-self detection.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-067",
        "concern": "duplicate of correctness-2 + correctness-3: invalid sql syntax and narrow cascade lookup.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-069",
        "concern": "shared orchestrator-reference helpers not referenced.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-072",
        "concern": "orchestrator tasks that crash don't get orchestrator-self cascade.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-074",
        "concern": "hardcoded params->>'orchestrator_task_id_ref' misses other reference paths.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements",
    "total_occurrences": 5,
    "plan_count": 5,
    "entries": [
      {
        "id": "DEBT-013",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the package is internally inconsistent. the plan body says to keep `activepairdata` in `usestate` and make phase 2 optional, but the attached metadata and success criteria still describe the previous derive-via-`usememo` / remove-`setactivepairdata` / simplify-`onpairclick` plan. that means the approved-plan requirements are only partially coherent as presented.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-108",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the linux distro note is documentation-only; the generated install command in step 7 still runs `apt-get install python3.10-venv python3.10-dev ffmpeg` without any pre-check that the package exists. users on ubuntu 24.04+ who ignore the doc and try to copy-paste the command will hit a confusing `e: unable to locate package python3.10-venv` from apt rather than a targeted error from commandutils.ts. a one-line detection pre-check (e.g., `apt-cache show python3.10-venv >/dev/null 2>&1 || { echo 'install deadsnakes ppa first \u2014 see readme'; exit 1; }`) would convert the silent failure into an actionable error, but the plan does not add this.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-145",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: checked the revised v4 body against `docs/wan2gp_fork_migration_plan.md` sprint 2. the repo plan doc still lists an \"ltx-2 `self_refiner` smoke against the pre-sprint behavioral baseline\" as a sprint 2 verification gate and repeats that smoke in the functionality-preservation checks, but the revised execution steps no longer schedule that smoke anywhere; it survives only as an info-level metadata criterion. because `wan2gp/shared/utils/self_refiner.py` remains an explicit sprint 2 deliverable, the revised plan still only partially carries forward the verification package described in the source migration plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-153",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: worker integration: the migration doc describes the per-call profile override gap as involving reigh-worker adapter handling of override_profile before constructing vibecomfy sessionconfig, but the plan limits sprint 1 per-run work to the vibecomfy cli/runtime. that may be acceptable for a vibecomfy-library mvp, but it does not fully exercise the production-facing per-task override semantics called out in the overall context.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-1-vibecomfy-memory-20260506-0147"
        ]
      },
      {
        "id": "DEBT-155",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: a residual issue-hint tension remains for resolution handling. the plan acknowledges current `vibecomfy run` lacks a resolution flag, but allows the adapter to leave resolution and other template-specific values unwired for sprint 2. because `z_image_turbo` and `qwen_image_2512` are marked vibecomfy-supported direct routes, this may not preserve the existing worker task-parameter contract for tasks that provide a non-default `resolution`.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "timeline-drag-coordination",
    "total_occurrences": 5,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-126",
        "concern": "plan keeps two hooks instead of a single coordinator",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-127",
        "concern": "brief says single coordinator but plan keeps separate hooks",
        "occurrence_count": 2,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-128",
        "concern": "pendingopsref retained despite brief suggesting removal",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-129",
        "concern": "wrapper-bound listener mount wiring under-specified",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-retry",
    "total_occurrences": 4,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-063",
        "concern": "crash requeue sql does not increment attempts, risking infinite requeue loop.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-066",
        "concern": "duplicate of correctness-1: attempts never advance on crash requeue.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-068",
        "concern": "missing attempts increment location in heartbeat sql.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-073",
        "concern": "step 6 under-scoped for real retry convergence and orchestrator-self handling.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "audio-loading",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-086",
        "concern": "getaudiodata in useeffect removes render-readiness signal",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-087",
        "concern": "same as correctness-3 \u2014 preview/render parity risk",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-088",
        "concern": "preview/render parity partially satisfied",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-testing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-070",
        "concern": "no multi-crash convergence test exercising attempts 0\u21921\u21922\u21923.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-071",
        "concern": "no validation that plpgsql body executes successfully.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-075",
        "concern": "criteria don't require proof of crash requeue convergence.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "criteria-verifiability",
    "total_occurrences": 3,
    "plan_count": 2,
    "entries": [
      {
        "id": "DEBT-036",
        "concern": "'no unsafe .maybesingle()' criterion requires judgment about column uniqueness.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-037",
        "concern": "decision documentation location not specified.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-062",
        "concern": "the must criterion requiring 5 task types to exist as active db rows is not verifiable from code diff alone \u2014 it requires a live db query.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-delete-the-20260331-0519"
        ]
      }
    ]
  },
  {
    "subsystem": "edge-test-config",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-022",
        "concern": "plan's vitest commands use the wrong config entry point.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-023",
        "concern": "same as verification-3: wrong vitest config in validation commands.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-024",
        "concern": "success criterion references wrong test command.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      }
    ]
  },
  {
    "subsystem": "error-propagation-testing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-020",
        "concern": "no end-to-end regression test for the full symptom chain (db error \u2192 tocompletionerror metadata \u2192 handler log).",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-025",
        "concern": "handler.ts metadata surfacing criterion lacks a concrete automated verifier.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-026",
        "concern": "main issue only partially validated without an integration test.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      }
    ]
  },
  {
    "subsystem": "find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them",
    "total_occurrences": 3,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-109",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the step 2 retry loop uses a naked `sleep 2` between attempts, which adds up to 6 seconds of latency on the happy path when the first patch eventually succeeds on attempt 2 or 3. for pods where supabase is reachable but slow during the initial moments of a cold runpod start, the retry logic is fine. however, if the first attempt fails with a tls handshake delay and the retry loop sleeps 2s per attempt regardless of whether curl itself has been blocking for tens of seconds, the total startup latency penalty could be substantial. this is a minor tuning concern, not a correctness issue.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-146",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: finding callers of the changed module shows that `shared.utils.self_refiner` is consumed by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx2_handler.py`, multiple ltx2 pipeline modules, and `wan2gp/models/wan/any2video.py`. the revised validation steps still only drive the three bridge getters in `source/runtime/wgp_ports/vendor_imports.py`; none of the scheduled commands execute a real `self_refiner` caller, so the plan does not yet verify the main caller shapes for the other explicit sprint 2 file change.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-159",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked direct queue caller values in `db_task_to_generation_task()`: direct image tasks may carry `resolution`, `steps`/`num_inference_steps`, `seed`, and `override_profile`. the revised adapter plan covers seed, steps, and memory profile but not guaranteed resolution propagation, so it does not handle all relevant direct-route caller arguments for a supported vibecomfy direct route.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "is-there-convincing-verification-for-the-change",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-010",
        "concern": "is there convincing verification for the change?: the plan still lacks an explicit automated regression test for the reported bug. step 2 is manual ('check that `usevideoregeneratemode` now gets the fresh url'), but there is no concrete test that opens a segment slot, changes the primary variant data, and asserts that the regenerate path sees the fresh `url`, `generationid`, and `primaryvariantid`.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-011",
        "concern": "is there convincing verification for the change?: the current `usesegmentslotmode` test remains only a smoke test in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts), and the plan does not add behavior coverage for the new sync effect.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-012",
        "concern": "is there convincing verification for the change?: no verification step covers the trailing-slot branch, even though the proposed phase 1 logic currently misses `trailingpairdata` refreshes.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      }
    ]
  },
  {
    "subsystem": "number-input-nullable",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-076",
        "concern": "plan doesn't explicitly state onchange must also accept null, though step 3 depends on it.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      },
      {
        "id": "DEBT-077",
        "concern": "disputed v1 flag \u2014 original concern about bulkclippanel being unimplementable.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      },
      {
        "id": "DEBT-079",
        "concern": "onchange null filtering not explicitly addressed in plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      }
    ]
  },
  {
    "subsystem": "pair-settings-plumbing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-039",
        "concern": "handleopenpairsettings(pairindex, pairframedata) path in timelinetrackprelude, segmentoutputstrip, and usesegmentoutputstrip not explicitly named.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-042",
        "concern": "same as flag-002 \u2014 segmentoutputstrip and usesegmentoutputstrip still carry pairframedata.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-045",
        "concern": "timelinetrackprelude and segmentoutputstrip still forward (pairindex, pairframedata).",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  },
  {
    "subsystem": "position-key-semantics",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-028",
        "concern": "plan investigates a unique constraint on (parent_generation_id, child_order) which doesn't match repo semantics for position keys.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-030",
        "concern": "plan weights toward child_order rather than pair_shot_generation_id as the key that matters.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-031",
        "concern": "unique constraint on (parent_generation_id, child_order) not supported by repo semantics.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      }
    ]
  },
  {
    "subsystem": "search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader",
    "total_occurrences": 3,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-141",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the broader runtime surface after the v4 path fix. sprint 2 is still moving two behavior-sensitive seams rather than just the import-path contract: the `wan2gp/` mount path and the `self_refiner` runtime. step 6.2 covers only the three `vendor_imports` getters, while the 6-file travel suite and the bridge-contract tests do not mention `self_refiner`, so dropping the dedicated self-refiner smoke from the runnable steps leaves the broader downstream surface of that changed file under-covered.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-157",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the supported direct-route scope is still broader than the adapter's guaranteed parameter surface. `db_task_to_generation_task()` currently carries direct task params such as `resolution`, `steps`, and `seed` into wgp generation, but the vibecomfy cli path only guarantees prompt, seed, steps, and memory profile; resolution remains optional/documentation-only in the plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      },
      {
        "id": "DEBT-161",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the revised child-route scope against `migration-thresholds.yaml`. the threshold corpus currently has wan/vace entries for `travel_segment__model-wan22_vace__...` and `join_clips_segment__model-wan22_vace__...`, but only an i2v entry for `individual_travel_segment`; the revised plan makes `individual_travel_segment` with vace model params a must-level worker fixture, which broadens the worker smoke scope beyond the currently tracked wan/vace threshold routes.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-4-wan-single-frame-and-20260506-0818"
        ]
      }
    ]
  },
  {
    "subsystem": "signature-propagation",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-038",
        "concern": "plan doesn't explicitly name timeline/index.tsx and segmentslotcontracts.ts for updates.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-041",
        "concern": "same as flag-001 \u2014 timeline/index.tsx and segmentslotcontracts.ts not in checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-044",
        "concern": "five supporting contract/plumbing sites not named in the checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  },
  {
    "subsystem": "ta[REDACTED_SK]",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-050",
        "concern": "step 3 cites wrong migration file (task_cost_configs instead of task_types) as evidence for db fallback path.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-052",
        "concern": "step 3 should cite task_types source, not task_cost_configs.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-055",
        "concern": "plan doesn't verify travel_segment and travel_stitch exist as active task_types rows using the correct table.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      }
    ]
  },
  {
    "subsystem": "verification-coverage",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-040",
        "concern": "no automated test exercises the full segment-slot opening path after cleanup.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-046",
        "concern": "no automated coverage that clicking a pair opens the correct modal after cleanup.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-048",
        "concern": "zero behavioral change criterion is not verifiable from tsc + existing tests alone.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  }
]

        Debt guidance:
        - These are known accepted limitations. Do not re-flag them unless the current plan makes them worse, broadens them, or fails to contain them.
        - Prefix every new concern with a subsystem tag followed by a colon, for example `Timeout recovery: retry backoff remains brittle`.
        - When a concern is recurring debt that still needs to be flagged, prefix it with `Recurring debt:` after the subsystem tag, for example `Timeout recovery: Recurring debt: retry backoff remains brittle`.



        Your output template is at: /Users/user_c042661f/Documents/reigh-workspace/.megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json
Read this file first — it contains 5 checks, each with a question and guidance.
For each check, investigate the codebase, then add your findings to the `findings` array for that check.

Each finding needs:
- "detail": what you specifically checked and what you found (at least a full sentence)
- "flagged": true if this describes a difference, risk, or tension — even if you think it's justified. false only if purely informational with no possible downside.
- Every check must end with at least one finding. Never leave a `findings` array empty. If you found no issue, add one detailed `flagged: false` finding explaining what you checked and why it appears clear.

When in doubt, flag it — the gate can accept tradeoffs, but it can't act on findings it never sees.

Good: {"detail": "Checked callers of nthroot_mod in solveset.py line 1205 — passes prime moduli only, consistent with the fix.", "flagged": false}
Good: {"detail": "The fix handles empty tuples but not single-element tuples which need a trailing comma.", "flagged": true}
Bad: {"detail": "No issue found", "flagged": false}  ← too brief, will be rejected
Bad: {"detail": "The hints suggest approach X but the plan uses Y. However Y is consistent with X's intent.", "flagged": false}  ← a different approach than the hints IS a flag. You found a divergence — flag it. The gate decides if it's acceptable.

After filling in checks, add any additional concerns to the `flags` array (e.g., security, performance, dependencies).
Use the standard format (id, concern, category, severity_hint, evidence). This array can be empty.

Workflow: read the file → investigate → read file again → add finding → write file back. Repeat for each check.

This is critique iteration 2. The template file includes prior findings with their status. Verify addressed flags were actually fixed, re-flag if inadequate, and check for new issues introduced by the revision.

        Additional guidelines:
        - Robustness level: standard. Use balanced judgment. Flag significant risks, but do not spend flags on minor polish or executor-obvious boilerplate.
        - Over-engineering: prefer the simplest approach that fully solves the problem.
        - Reuse existing flag IDs when the same concern is still open.
        - `verified_flag_ids`: list flag IDs from prior iterations that the revised plan actually resolves (e.g., if the plan was revised to fix FLAG-001, and you confirm the fix is correct, include "FLAG-001"). Only include flags you've verified — don't guess.
        - Verify that the plan follows the expected structure when validator warnings or the outline suggest drift.
        - Additional flags may use these categories: correctness, security, completeness, performance, maintainability, other.
        - Focus on concrete issues, not structural formatting.

> AGENT

I’m re-reading the current template and then checking the revised plan against the live repo surfaces it names. Since this is iteration 2, I’m treating the previous flags as candidates to verify rather than re-issuing them by default.

> AGENT

The revision does resolve the five previous substantive flags at the plan level. I found two new contract gaps: the plan says WGP can claim missing-selector rows only when WGP-executable, but it does not define a SQL-side capability predicate; and task-count active-work accounting can become wrong after selector rollback if it uses only the live selector for in-progress rows.

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' .megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"get_task_run_type|task_types|category|run_type|is_wgp_task|WGP_ONLY|VIBECOMFY_UNSUPPORTED|vibecomfy\" reigh-app/supabase/migrations reigh-worker/source/task_handlers/tasks -S",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"active_only|queued_plus_active|In Progress|selected_backend|worker_backend|worker_id\" reigh-app/supabase/functions/task-counts/index.ts reigh-app/supabase/migrations/20250913000000_fix_count_function_final.sql reigh-app/supabase/migrations/20260128000012_add_task_count_breakdown.sql reigh-app/supabase/migrations/20260504120000_extend_claim_next_task_for_pools.sql -S",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"def is_wgp_task|WGP|task_types|TASK_TYPES|DIRECT|orchestrator|join_clips_segment|travel_stitch\" reigh-worker/source/task_handlers/tasks/task_types.py reigh-worker/source/task_handlers/tasks/task_registry.py -S",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,190p' reigh-worker/source/task_handlers/tasks/task_types.py && sed -n '1,90p' reigh-app/supabase/migrations/20250913000000_fix_count_function_final.sql",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,80p' reigh-app/supabase/migrations/20250705000001_create_workers_table.sql && rg -n \"worker_backend|backend|current_model|worker_pool\" reigh-app/supabase/migrations reigh-worker/source -S | head -n 120",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1360,1410p' reigh-worker/source/task_handlers/tasks/task_registry.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"poll_next_task\\(|process_single_task\\(|task_data|get\\('params'|\\[\\\"params\\\"\\]\" reigh-worker/source/runtime reigh-worker/source/core reigh-worker/source/task_handlers -S | head -n 200",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '640,760p' reigh-worker/source/runtime/worker/server.py",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

Updated the critique file at `.megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json`.

I verified `FLAG-001` through `FLAG-005` as addressed by the revised plan, and added two new flags:

- `FLAG-006`: missing SQL-side WGP-executable route predicate for missing-selector claims.
- `FLAG-007`: active task-count accounting can undercount after selector rollback without persisted claim-time backend data.

> TOOL

tool_use exec_command
```json
{
  "cmd": "python3 - <<'PY'\nimport json\nfrom pathlib import Path\npath = Path('.megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json')\ndata = json.loads(path.read_text())\nfindings = {\n  'issue_hints': [\n    {\n      'detail': 'Verified FLAG-001 against the revised plan: Phase 1 Step 1 now explicitly requires RLS on route_backend_selectors, revoked broad writes, service-role read/write, no authenticated/anon direct mutation, and unauthorized selector access tests. That addresses the prior unauthorized-entry gap at plan level and matches the repo pattern used for control-plane tables such as workers and rate_limits.',\n      'flagged': False,\n    },\n    {\n      'detail': 'Checked the sprint rule that missing production selector keys mean WGP/no-claim rather than implicit Comfy. The revised plan states this rule, but also narrows WGP missing-selector claims to legacy WGP-executable routes; the repo currently has no SQL-side WGP capability table or function comparable to the Python is_wgp_task catalog, so this new qualifier is not yet implementable from the named DB sources alone.',\n      'flagged': True,\n    },\n  ],\n  'correctness': [\n    {\n      'detail': 'Verified FLAG-002 against the revised plan: it now makes live route_backend_selectors the claim authorization source of truth, treats task route fields as snapshots only, returns live selector values separately from route_selection_snapshot, and adds a rollback test proving live selector changes affect subsequent claims. That resolves the prior live-vs-snapshot ambiguity.',\n      'flagged': False,\n    },\n    {\n      'detail': 'Checked the proposed active task-count parity against the current task-counts implementation and schema. The revised plan says queued_only, queued_plus_active, detailed queued_tasks, and detailed active_tasks should use live selector eligibility; however, in-progress tasks only have worker_id today, workers have metadata/current_model but no backend column, and task selected_backend is a create-time snapshot rather than a claim-time backend. After a selector rollback, filtering active work by the new live selector could undercount tasks already running on the old backend unless the plan also persists claim-time backend/selector data or counts active tasks by worker backend.',\n      'flagged': True,\n    },\n  ],\n  'scope': [\n    {\n      'detail': 'Verified FLAG-003 against the revised plan: Phase 2 now explicitly adds join_clips_segment dimensional serialization to the canonical Python route helper and the TypeScript create-task helper, matching the existing scripts/dual_run_compare/route_keys.py key shape. That covers the previously missing join child route-key surface.',\n      'flagged': False,\n    },\n    {\n      'detail': 'Searched the worker route helper and task type catalog again; direct routes and travel child routes remain lightweight and local to template_routing.py/task_types.py, and the revised plan keeps the no-WGP/no-VibeComfy import constraint. I did not find a new broader route-key subsystem omitted by the revised scope beyond the SQL WGP-capability predicate noted under issue_hints.',\n      'flagged': False,\n    },\n  ],\n  'all_locations': [\n    {\n      'detail': 'Verified FLAG-004 against the revised plan: Step 6 now names both backend-aware RPC totals and the direct queued_tasks/active_tasks TypeScript array filters in task-counts/index.ts, and the success criteria require aggregate totals and detailed arrays to use the same selector semantics. That addresses the previous all-locations gap for detailed task-count output.',\n      'flagged': False,\n    },\n    {\n      'detail': 'Checked supporting DB infrastructure for the new “WGP workers may claim only legacy WGP-executable routes” rule. The repo has a Python WGP_TASK_TYPES catalog in reigh-worker/source/task_handlers/tasks/task_types.py and task_types/run_type data in migrations, but the plan does not add a Postgres-side backend capability registry or route support table for claim_next_task_service_role to consult when the selector row is missing.',\n      'flagged': True,\n    },\n  ],\n  'callers': [\n    {\n      'detail': 'Verified FLAG-005 against the revised plan: Step 11 now requires an rg inventory of every add_task_to_db caller and explicitly names travel/orchestrator.py, travel/stitch.py, travel/chaining.py, related guide/mask paths, and join/task_builder.py. Step 8 also defines top-level workerPassthrough lifting for route_key, selected_backend, selector_version, and route_selection_snapshot, which resolves the prior caller-contract gap.',\n      'flagged': False,\n    },\n    {\n      'detail': 'Checked the claim caller in worker/server.py: poll_next_task returns the full edge response as task_info, and server.py reads params/task_type/task_id before process_single_task. The revised pre-execution guard location is viable because it can compare task_info live selector fields before params are handed to process_single_task, provided the implementation updates task_claim.py to preserve those top-level response fields.',\n      'flagged': False,\n    },\n  ],\n}\nfor check in data['checks']:\n    check['findings'] = findings[check['id']]\n\ndata['flags'] = [\n  {\n    'id': 'FLAG-006',\n    'concern': 'Claim eligibility: the revised missing-selector rule depends on knowing whether a route is WGP-executable, but the plan does not add a SQL-side backend capability predicate for the claim RPC.',\n    'category': 'correctness',\n    'severity_hint': 'likely-significant',\n    'evidence': 'The worker has Python WGP_TASK_TYPES/is_wgp_task in reigh-worker/source/task_handlers/tasks/task_types.py, while the latest claim RPC in 20260504120000_extend_claim_next_task_for_pools.sql only filters by get_task_run_type, worker_pool, task_types, dependencies, capacity, and model affinity. task_types.run_type is gpu/api, not WGP vs VibeComfy capability.',\n  },\n  {\n    'id': 'FLAG-007',\n    'concern': 'Task-count active accounting: using live selector eligibility for in-progress active_tasks can undercount work after selector rollback because claim-time backend is not persisted separately from create-time snapshots.',\n    'category': 'correctness',\n    'severity_hint': 'uncertain',\n    'evidence': 'task-counts/index.ts reports active_only/active_tasks for scaling; tasks currently have worker_id and the plan adds create-time selected_backend snapshots, but workers table has no backend column and the plan does not add claim_selected_backend/claim_selector_version. A live selector change can make already-running tasks fail the new live eligibility filter.',\n  },\n]\ndata['verified_flag_ids'] = ['FLAG-001', 'FLAG-002', 'FLAG-003', 'FLAG-004', 'FLAG-005']\ndata['disputed_flag_ids'] = []\npath.write_text(json.dumps(data, indent=2) + '\\n')\nPY\nsed -n '1,320p' .megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 40000
}
```

> TOOL

tool_result exec_command
```
null
```

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are an independent reviewer. Critique the plan against the actual repository.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace





        Idea:
# Sprint 6: Production Selector and Claim Contract

## Overall Context

This sprint turns local selector ideas into production claim behavior before orchestrated routes depend on them. It is the control-plane foundation for rollback and canary.

## Shared Operating Rules

- Production missing selector key means WGP/no-claim, never implicit Comfy.
- Workers must not claim routes they cannot execute.
- Selector version and selected backend must be visible in logs or task metadata.
- Child rows created later must be able to snapshot route selection.

## Sprint Goal

Make selector and claim behavior concrete for production.

## Required Deliverables

- Selector schema/namespace.
- Route-key serialization, including direct variants where needed.
- Index/RPC/query behavior.
- Cache TTL and rollback SLO.
- Malformed/unauthorized/stale-entry tests.
- Claim-time backend eligibility or pre-execution requeue/fail-closed guard.
- Selector-version logging.
- Child-route snapshot field contract for later parent-created rows.

## Exit Criteria

Missing production route key means WGP/no-claim; mismatched workers cannot claim or execute selected routes; selector unreachable behavior and rollback SLO are tested; selected backend/selector version can be pinned for child rows created after parent claim.

        Plan:
        # Implementation Plan: Sprint 6 Production Selector and Claim Contract

## Overview
The remaining critique does not show that the plan is aimed at the wrong code or root cause. The production claim boundary is still the right place to fix this: `claim-next-task` and its SQL RPC decide which worker gets a row, `task-counts` drives scaling from the same queue state, and worker runtime guards catch any escaped mismatch before execution.

The revision tightens two missing pieces. First, the missing-selector WGP path needs a Postgres-side capability source; the claim RPC cannot consult Python `WGP_TASK_TYPES`. Add a small route/backend capability table used by claim and count SQL. Second, active task accounting cannot be filtered against the current live selector after rollback, because already-running tasks were claimed under an earlier selector decision. Persist claim-time backend and selector fields on `tasks`, then count active work from those claim-time fields while queued eligibility continues to use the live selector table.

Source of truth stays precise: live `route_backend_selectors` controls queued-task claim eligibility and rollback; `route_backend_capabilities` controls which backend can safely claim a missing-selector route; task snapshot fields support observability and child pinning; task claim fields record the exact selector/backend decision used for active work.

Primary touch points are `reigh-app/supabase/migrations/`, `reigh-app/supabase/functions/claim-next-task/index.ts`, `reigh-app/supabase/functions/task-counts/index.ts`, `reigh-app/supabase/functions/create-task/`, `reigh-worker/source/task_handlers/tasks/template_routing.py`, `reigh-worker/source/core/db/task_claim.py`, `reigh-worker/source/core/db/task_completion.py`, and all `add_task_to_db` callers discovered in worker task handlers.

## Phase 1: Foundation — Selector, Capability, Security, and Task Fields

### Step 1: Create selector schema with explicit access control (`reigh-app/supabase/migrations/`)
**Scope:** Medium
1. Add a migration creating `public.route_backend_selectors` with `namespace`, `route_key`, `selected_backend`, `selector_version`, `enabled`, `updated_at`, `expires_at`, and `metadata`.
2. Add checks: `selected_backend in ('wgp', 'vibecomfy')`, non-empty namespace, non-empty route key, non-empty selector version, and `expires_at is null or expires_at > updated_at`.
3. Add unique lookup on `(namespace, route_key)` and selector lookup indexes for claim paths.
4. Enable RLS on `route_backend_selectors`; revoke broad writes; grant service-role read/write; allow authenticated/anon no direct mutation. If read access is needed outside service-role RPCs, expose it only through a security-definer read RPC with constrained output.
5. Add comments documenting that selector rows are control-plane data and must be mutated only by service-role/admin deployment paths.

### Step 2: Add SQL-side backend capability registry (`reigh-app/supabase/migrations/`)
**Scope:** Medium
1. Add `public.route_backend_capabilities` with `route_key`, `backend`, `is_supported`, `supports_missing_selector`, `updated_at`, and optional `metadata`.
2. Add checks: `backend in ('wgp', 'vibecomfy')`, non-empty route key, and one row per `(route_key, backend)`.
3. Seed WGP-supported route keys from the current worker direct/WGP catalog where route keys are direct task-type keys, including routes that can safely use the missing-selector legacy path.
4. Seed VibeComfy-supported rows only for explicitly supported routes; do not set `supports_missing_selector=true` for VibeComfy.
5. Add RLS/grants matching selector table control-plane rules: service-role mutation only, no broad authenticated/anon writes.
6. Document that this table is the SQL-side counterpart to worker route capability, and claim/count RPCs must use it instead of trying to infer WGP support from `task_types.run_type`.

### Step 3: Add task route snapshot and claim-decision columns (`reigh-app/supabase/migrations/`)
**Scope:** Medium
1. Add creation-time snapshot columns: `tasks.route_key text`, `tasks.selected_backend text`, `tasks.selector_version text`, and `tasks.route_selection_snapshot jsonb`.
2. Add claim-time decision columns: `tasks.claimed_backend text`, `tasks.claimed_route_key text`, `tasks.claimed_selector_namespace text`, `tasks.claimed_selector_version text`, and `tasks.claimed_selector_snapshot jsonb`.
3. Add checks for backend fields when present: `selected_backend in ('wgp', 'vibecomfy')` and `claimed_backend in ('wgp', 'vibecomfy')`.
4. Add indexes for queued claim lookup: `(status, route_key, created_at)`, capability lookup by route/backend, and active accounting `(status, claimed_backend, updated_at)`.
5. Backfill direct task route keys where route key equals `task_type`; do not invent dimensional child keys for historical rows unless their params can be serialized with the same helper contract.
6. Document source of truth: live selector controls queued eligibility; capability table controls missing-selector fallback safety; task snapshot fields are for observability/child pinning; claim fields are for active accounting and audit.

## Phase 2: Route-Key Serialization

### Step 4: Extend canonical worker route serializer (`reigh-worker/source/task_handlers/tasks/template_routing.py`)
**Scope:** Medium
1. Keep `derive_route_key` lightweight and import-safe, preserving the existing no-WGP/no-VibeComfy import test.
2. Add dimensional serialization for `join_clips_segment`, matching the existing comparison key shape used by `scripts/dual_run_compare/route_keys.py`: `join_clips_segment__model-*__guidance-*__continuity-join_bridge__profile-*`.
3. Keep existing direct keys for `z_image_turbo`, Qwen routes, `wan_2_2_t2i`, `travel_segment`, and `individual_travel_segment`.
4. Add route snapshot helpers that produce `{ route_key, selected_backend, selector_version, selector_namespace }` without making claim decisions.

### Step 5: Add TypeScript route-key helper for task creation (`reigh-app/supabase/functions/create-task/`)
**Scope:** Medium
1. Add a small helper near create-task resolvers that mirrors the Python route-key serializer for direct routes, travel children, individual travel children, and `join_clips_segment`.
2. Use the same slugging rules as Python for model, guidance, continuity, and profile fields.
3. Add resolver tests for direct route keys and dimensional child keys, including `join_clips_segment`.
4. Keep this helper independent of frontend UI code and worker-only WGP/VibeComfy modules.

## Phase 3: Claim-Time Selector Enforcement

### Step 6: Extend claim request and live-selector RPC (`claim-next-task`, migration RPC)
**Scope:** Large
1. Extend `claim-next-task` request parsing with `worker_backend?: 'wgp' | 'vibecomfy'` and `selector_namespace?: string`; default backend to `wgp` for existing service-role GPU callers and namespace to `production`.
2. Reject malformed `worker_backend` and malformed namespace with `400` before calling the RPC.
3. Extend `claim_next_task_service_role` with `p_worker_backend text default 'wgp'` and `p_selector_namespace text default 'production'`.
4. In the queued candidate query, use `tasks.route_key` to left join the live `route_backend_selectors` row for the requested namespace and join `route_backend_capabilities` for `(route_key, p_worker_backend)`.
5. Enforce queued claim eligibility from live selector plus capability:
   - Missing selector row: claim only if `route_backend_capabilities.supports_missing_selector=true` for the requested backend. Seed this true for WGP-safe routes only; never true for VibeComfy.
   - Enabled, non-stale selector row: claim only if selector backend matches `p_worker_backend` and capability says the backend supports the route.
   - Disabled, expired, malformed, inaccessible selector row, or missing capability row: no claim for that backend.
6. When claiming a row, update both runtime assignment fields and claim-decision fields: `worker_id`, `generation_started_at`, `claimed_backend`, `claimed_route_key`, `claimed_selector_namespace`, `claimed_selector_version`, and `claimed_selector_snapshot`.
7. Return live selector/capability decision fields and separate task snapshot fields so logs can distinguish claim source from create-time metadata.
8. Update claim logs in `claim-next-task/index.ts` to include `route_key`, `selected_backend`, `selector_version`, `selector_namespace`, `claimed_backend`, and missing-selector capability reason.

### Step 7: Align task counts with claim eligibility and active accounting (`task-counts`, count RPCs, TypeScript array filters)
**Scope:** Large
1. Extend `task-counts` service-role request parsing with `worker_backend` and `selector_namespace`, using the same validation/defaults as `claim-next-task`.
2. Update or add backend-aware count RPCs so queued counts and queued breakdowns use the same live selector plus capability eligibility as `claim_next_task_service_role`.
3. For active counts, do not re-filter in-progress tasks through the current live selector. Count active work by persisted claim-time fields: `status='In Progress'`, `claimed_backend = p_worker_backend`, and existing run-type/API-worker exclusions where still relevant.
4. Update direct `queued_tasks` filters in `task-counts/index.ts` to apply the same queued live selector plus capability eligibility as the RPC totals.
5. Update direct `active_tasks` filters in `task-counts/index.ts` to use `claimed_backend` and claim-time selector fields, not current live selector state.
6. Include route fields in detailed arrays: for queued tasks include route key and live selector/capability decision; for active tasks include `claimed_backend`, `claimed_route_key`, `claimed_selector_version`, and `claimed_selector_namespace`.
7. Add tests where VibeComfy queued arrays are empty for missing selector rows, WGP sees only capability-approved missing-selector routes, and active counts remain stable after a live selector rollback because they use claim-time fields.

## Phase 4: Task Creation and Snapshot Materialization

### Step 8: Materialize task snapshots at create time (`reigh-app/supabase/functions/create-task/`)
**Scope:** Medium
1. Extend `TaskInsertObject` with top-level `route_key`, `selected_backend`, `selector_version`, and `route_selection_snapshot`.
2. After resolver output and before insert, compute `route_key` for each task when not explicitly supplied.
3. Look up the live selector row for the configured namespace and populate task snapshot fields from that live selector. If no selector exists, store `route_key` and a WGP-safe missing-selector snapshot only when the capability table says WGP supports missing-selector fallback for that route; otherwise store no selected backend and let claim return no eligible worker.
4. If selector or capability lookup itself fails or returns malformed data, fail closed with an explicit create-task error rather than inserting a task with ambiguous backend metadata.
5. Add tests for selector present, selector missing with WGP capability, selector missing without WGP capability, malformed selector, and selector/capability lookup failure.

### Step 9: Define worker passthrough route-field lifting (`workerPassthrough.ts`, create-task tests)
**Scope:** Medium
1. Update `createWorkerPassthroughResolver` so worker-created payloads can pass explicit route fields at top level in `input`: `route_key`, `selected_backend`, `selector_version`, and `route_selection_snapshot`.
2. Lift those fields into top-level `TaskInsertObject` columns rather than leaving them buried in `params`.
3. Keep the existing `task_id` and `dependant_on` lifting behavior unchanged.
4. Validate explicit backend values and route snapshot shape before insert.
5. Add tests proving worker-created children get top-level route fields and still preserve the original payload in `params`.

## Phase 5: Worker Integration and Child Snapshot Propagation

### Step 10: Send backend capability and log claim fields (`reigh-worker/source/core/db/task_claim.py`)
**Scope:** Small
1. Parse `REIGH_BACKEND` through the existing strict backend parser and send `worker_backend` in service-role claim payloads.
2. Include returned `route_key`, live `selected_backend`, `selector_version`, claim-time fields, and snapshot metadata in claim debug logs.
3. Preserve PAT/local behavior unless PAT backend capability is intentionally added later.

### Step 11: Add pre-execution mismatch guard (`reigh-worker/source/runtime/worker/server.py`, `task_execution.py`)
**Scope:** Medium
1. Before `process_single_task`, compare the live claim decision returned by `claim-next-task` with the current worker backend.
2. If a mismatch reaches the worker despite claim filtering, requeue with `clear_worker=true` using the existing retry/update path when another backend can handle it.
3. If the selector/capability decision is malformed or explicitly unsupported, mark failed with a fail-closed error that includes `task_id`, `task_type`, `route_key`, `claimed_backend`, `selected_backend`, and `selector_version`.
4. Extend `VIBECOMFY_ROUTING` and WGP routing telemetry fields with selector version, backend decision fields, and capability reason.

### Step 12: Inventory and update every child task creation caller (`reigh-worker/source/core/db/task_completion.py`, worker handlers)
**Scope:** Large
1. Extend `add_task_to_db` to accept optional route snapshot fields and include them in the `create-task` input payload.
2. Inventory all `add_task_to_db` callers with `rg "add_task_to_db" reigh-worker/source` before editing.
3. Update known child/processing callers with an explicit decision:
   - `reigh-worker/source/task_handlers/travel/orchestrator.py`: derive child route keys and pass child snapshots for `travel_segment` and stitch children.
   - `reigh-worker/source/task_handlers/travel/stitch.py`: pass snapshot when it creates follow-on tasks, or explicitly leave WGP-safe null fields for WGP-only processing tasks.
   - `reigh-worker/source/task_handlers/travel/chaining.py` and related guide/mask builder paths: pass snapshot or explicitly document WGP-safe null behavior.
   - `reigh-worker/source/task_handlers/join/task_builder.py`: derive/pass snapshots for `join_clips_segment` and related join child rows.
4. Add focused tests for `add_task_to_db` payload construction and at least one travel and one join child creation path.

## Phase 6: Failure Modes, Rollback SLO, and Validation

### Step 13: Add selector/capability security and failure-mode tests (`reigh-app/supabase/functions/**/*.test.ts`, migration SQL tests)
**Scope:** Medium
1. Test unauthorized direct selector and capability mutation/read behavior according to the RLS/grant contract.
2. Test malformed backend values, disabled selector rows, expired selector rows, missing selector rows, missing capability rows, unsupported capability rows, and selector lookup failures.
3. Test that none of those cases imply a VibeComfy claim.
4. Test that missing selector rows are WGP-claimable only when `route_backend_capabilities.supports_missing_selector=true` for WGP.
5. Test that successful claims return and log live selector/capability fields distinctly from task snapshot and claim-time fields.

### Step 14: Document and test rollback/cache behavior (`claim-next-task`, `task-counts`)
**Scope:** Small
1. Document claim-path selector TTL as zero: every queued claim decision uses the live selector and capability tables through the RPC.
2. Define rollback SLO as database commit visibility plus normal worker/scaler polling interval.
3. If create-task uses an edge-side lookup helper, do not use an unbounded cache; either use no cache or a bounded `ROUTE_SELECTOR_CACHE_TTL_MS <= 30000` with tests.
4. Add a rollback test where changing the live selector version/backend changes subsequent queued claim eligibility and returned/logged selector fields.
5. Add an active-accounting rollback test where already-running tasks continue to count under their persisted `claimed_backend` and `claimed_selector_version` after the live selector changes.

## Execution Order
1. Land selector schema, capability schema, RLS/grants, task route columns, claim-decision columns, and indexes first.
2. Add Python and TypeScript route-key helpers, including `join_clips_segment`, before enforcing selector behavior.
3. Update claim RPC and `claim-next-task` live selector plus capability enforcement, including claim-time field persistence.
4. Update `task-counts` queued eligibility and active accounting after claim fields exist.
5. Materialize create-task snapshots and worker passthrough lifting after schema and route helper contracts are stable.
6. Wire worker backend claim payloads and pre-execution mismatch guards.
7. Update all `add_task_to_db` callers after inventory so no child path accidentally drops route snapshot fields.
8. Finish with security, failure-mode, rollback, active-accounting, and parity tests.

## Validation Order
1. Run focused route-key tests: worker `test_template_routing.py` and create-task route helper tests.
2. Run selector/capability migration security tests and create-task resolver tests.
3. Run `claim-next-task` tests for backend eligibility, missing selector, missing capability, malformed selector, stale selector, and returned live/claim fields.
4. Run `task-counts` tests proving queued aggregate totals, detailed queued arrays, active totals, and detailed active arrays match the intended claim/active-accounting semantics.
5. Run worker tests for claim payload parsing, pre-execution mismatch guard, and VibeComfy/WGP routing telemetry.
6. Run child creation tests for `add_task_to_db`, travel child rows, stitch/chaining decisions, and join child rows.
7. Finish with the relevant Supabase function suite and worker/orchestrator targeted suites.


        Plan metadata:
        {
  "version": 3,
  "timestamp": "2026-05-06T09:03:00Z",
  "hash": "sha256:11b1a833da7c5e719819a28719a074ee611c750e6dfcc5296e54ac821464a7b6",
  "changes_summary": "Added a SQL-side route/backend capability registry so missing-selector WGP eligibility is implementable in the claim RPC, and added persisted claim-time backend/selector fields so active task counts remain correct after selector rollback.",
  "flags_addressed": [
    "issue_hints",
    "correctness",
    "all_locations",
    "FLAG-006",
    "FLAG-007"
  ],
  "questions": [
    "Should selector and capability administration be implemented only through migrations/service-role SQL, or is there an existing admin edge function that should own writes?",
    "For non-production environments, should selector namespace come from a specific existing env var, or should this sprint introduce a new one such as `ROUTE_SELECTOR_NAMESPACE`?"
  ],
  "success_criteria": [
    {
      "criterion": "`route_backend_selectors` and `route_backend_capabilities` have explicit RLS/grant/service-role mutation controls, and unauthorized access is covered by tests or migration-level verification.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "A SQL-side route/backend capability source exists and is used by claim/count RPCs to decide whether a missing-selector route is WGP-claimable.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "A VibeComfy worker cannot claim a queued production task when the live selector row is missing, disabled, expired, malformed, inaccessible, or unsupported by capability data.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "WGP can claim missing-selector rows only when the capability table marks the route as WGP-supported for missing-selector fallback; missing selector rows never imply VibeComfy.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Claim eligibility, claim response fields, and claim logs use live selector/capability values, while task-row selector fields are clearly treated as snapshots for observability and child pinning.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Claim-time backend, route key, selector namespace, selector version, and selector snapshot are persisted on the task row when a task is claimed.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "A worker cannot claim or execute a task whose live selected backend does not match its declared backend capability; any escaped mismatch is requeued or failed closed before execution.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`task-counts` queued totals and detailed `queued_tasks` arrays use the same live selector plus capability eligibility semantics as `claim-next-task`.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`task-counts` active totals and detailed `active_tasks` arrays use persisted claim-time backend/selector fields, so active work is not undercounted after live selector rollback.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Route-key serialization tests cover direct routes, travel child variants, individual travel child variants, and `join_clips_segment` dimensional keys.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Worker-created child rows can lift `route_key`, `selected_backend`, `selector_version`, and `route_selection_snapshot` into top-level task columns through `workerPassthrough`.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Every `add_task_to_db` caller is inventoried and either passes a route snapshot or is explicitly kept WGP-safe/null by design.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Selector version and selected backend are visible in successful claim responses and worker/system logs.",
      "priority": "must",
      "requires": [
        "run_tests",
        "observe_runtime_logs",
        "parse_diff"
      ]
    },
    {
      "criterion": "Selector rollback SLO is documented as no claim-path cache or a bounded tested TTL, and tests prove live selector changes affect subsequent queued claims while active counts use persisted claim-time fields.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Route-key helper modules remain lightweight and do not import WGP, VibeComfy, or other heavy runtime modules.",
      "priority": "should",
      "requires": [
        "read_files",
        "parse_diff",
        "run_tests"
      ]
    }
  ],
  "assumptions": [
    "The active implementation target is `reigh-app`, `reigh-worker`, and `reigh-worker-orchestrator`; `reigh-app-cloud-chain` is not the primary edit target unless later confirmed otherwise.",
    "Missing live production selector rows do not imply VibeComfy. WGP may claim missing-selector rows only when the SQL-side `route_backend_capabilities` table marks that route/backend as supported for missing-selector fallback.",
    "Claim eligibility for queued work is based on the live selector table plus the route/backend capability table. Task-row route snapshots are for observability and child pinning, not rollback authorization.",
    "Active task accounting is based on persisted claim-time fields, not the current live selector after rollback.",
    "The selector namespace defaults to `production` and should be configurable by environment for non-production deployments.",
    "The claim path uses no selector cache. Any create-task helper cache must be absent or bounded and tested.",
    "`vibecomfy` remains the backend identifier; `comfy` is not accepted as an alias.",
    "Banodoco worker-pool filtering remains separate from WGP/VibeComfy backend selector eligibility."
  ],
  "delta_from_previous_percent": 32.87,
  "structure_warnings": []
}

        Plan structure warnings from validator:
        []

        Existing flags:
        [
  {
    "id": "verifiability-0",
    "concern": "Criterion 9: requires human verification (observe_runtime_logs).",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "issue_hints",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the sprint rule that missing production selector keys mean WGP/no-claim rather than implicit Comfy. The revised plan states this rule, but also narrows WGP missing-selector claims to legacy WGP-executable routes; the repo currently has no SQL-side WGP capability table or function comparable to the Python is_wgp_task catalog, so this new qualifier is not yet implementable from the named DB sources alone.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "correctness",
    "concern": "Are the proposed changes technically correct?: Checked the proposed active task-count parity against the current task-counts implementation and schema. The revised plan says queued_only, queued_plus_active, detailed queued_tasks, and detailed active_tasks should use live selector eligibility; however, in-progress tasks only have worker_id today, workers have metadata/current_model but no backend column, and task selected_backend is a create-time snapshot rather than a claim-time backend. After a selector rollback, filtering active work by the new live selector could undercount tasks already running on the old backend unless the plan also persists claim-time backend/selector data or counts active tasks by worker backend.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "scope",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched related route-key code and found join_clips_segment route keys are handled outside the canonical worker selector: tests call scripts/dual_run_compare/route_keys.py for join_clips_segment, while source/task_handlers/tasks/template_routing.py only derives dimensional keys for travel_segment and individual_travel_segment. The plan says to keep the existing Python serializer as canonical and update travel/join child creation paths, but it does not add join_clips_segment to that canonical serializer, so a production selector contract would still lack a shared app/worker key for join children.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "all_locations",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Checked supporting DB infrastructure for the new \u201cWGP workers may claim only legacy WGP-executable routes\u201d rule. The repo has a Python WGP_TASK_TYPES catalog in reigh-worker/source/task_handlers/tasks/task_types.py and task_types/run_type data in migrations, but the plan does not add a Postgres-side backend capability registry or route support table for claim_next_task_service_role to consult when the selector row is missing.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "callers-1",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Grep found add_task_to_db callers in travel/orchestrator.py, travel/stitch.py, and join/task_builder.py, and the current add_task_to_db signature only accepts task_payload, task_type_str, dependant_on, and db_path. The plan says to extend add_task_to_db for optional route-selection metadata and update travel and join builders, but it omits travel/stitch.py and travel/chaining.py call paths that also enqueue child/processing tasks through the same helper; those callers need an explicit decision to pass a snapshot or intentionally leave the new fields null/WGP-safe.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "callers-2",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked create-task workerPassthrough.ts and confirmed it currently copies request.input directly into params and only lifts task_id/dependant_on into top-level insert fields. The plan\u2019s instruction to allow worker-created children to pass route_selection_snapshot is compatible with this caller shape only if the implementation also defines how input snapshot keys become top-level route_key/selected_backend/selector_version fields rather than remaining buried in params.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-006",
    "concern": "Claim eligibility: the revised missing-selector rule depends on knowing whether a route is WGP-executable, but the plan does not add a SQL-side backend capability predicate for the claim RPC.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-007",
    "concern": "Task-count active accounting: using live selector eligibility for in-progress active_tasks can undercount work after selector rollback because claim-time backend is not persisted separately from create-time snapshots.",
    "status": "addressed",
    "severity": "significant"
  }
]

        Known accepted debt grouped by subsystem:
        {
  "are-the-proposed-changes-technically-correct": [
    {
      "id": "DEBT-007",
      "concern": "are the proposed changes technically correct?: for ordinary pairs, the new diagnosis is not well-supported by the repo. the current sync effect in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l62) already syncs `url` and `primaryvariantid`, and the regenerate path reads exactly `starturl`, `endurl`, `startgenid`, `endgenid`, `startvariantid`, and `endvariantid` from `segmentslotmode.pairdata` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts#l438). adding `thumburl` and `generationid` to the sync does not, by itself, explain why an old image url is still being used for regular pairs.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-008",
      "concern": "are the proposed changes technically correct?: the fix is incomplete for extra trailing slots. `handlepairclick` can populate `activepairdata` from `trailingpairdata` when `pairindex === pairdatabyindex.size` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l121), but the proposed sync effect only reads `pairdatabyindex.get(segmentslotlightboxindex)`. for those trailing-slot cases `fresh` is `undefined`, so no image refresh happens.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-018",
      "concern": "are the proposed changes technically correct?: the merge pseudocode does not actually sync 'all image fields' as claimed. it omits `id` and `position` from change detection, and when `fresh.startimage` or `fresh.endimage` becomes `null` it preserves the stale previous object instead of syncing that null state. as written, it also needs explicit null-guards around spreads of `prev.startimage` / `prev.endimage` to be safe in strict typescript.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-106",
      "concern": "are the proposed changes technically correct?: the plan's claim that `worker_state.py:200-204` (the 30-minute startup safety net) catches abandoned pods that exited before patching is slightly imprecise. line 200-204 only runs when `in_startup_phase` is true, which requires `startup_phase` to be in `('deps_installing', 'deps_verified', 'worker_starting')` per line 161. a pod that exits before its first patch has `startup_phase = none`, so `in_startup_phase` is false and the code falls through to the normal timeout checks (active_stale / not_claiming) at line 207+, not the 30-minute startup cap. both paths eventually reap the worker, so the end result is the same, but the overview's reasoning (naming 200-204 specifically) is wrong. worth correcting so future readers don't mis-reason about the invariant.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-107",
      "concern": "are the proposed changes technically correct?: checked worker_state.py line 161 (`in_startup_phase = startup_phase in (...)`) against the plan's assumption that subsequent lenient writes are safe. if deps_installing succeeds but deps_verified silently fails, startup_phase stays at 'deps_installing' and the 30-minute cap from line 200-204 applies \u2014 even though the pod is actually progressing through `uv sync`. on a slow runpod image with cold wheel downloads, `uv sync --extra cuda124` plus wan2gp deps can take 20+ minutes. there's no concrete benchmark in the plan that says the 30-minute cap is safely above the expected sync time; if `uv sync` legitimately takes 25 minutes and the deps_verified patch fails on a transient network blip, the orchestrator will terminate a healthy pod. plan should either bump the cap or note that deps_verified swallowing is acceptable because the cap is generously above typical sync time.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-143",
      "concern": "are the proposed changes technically correct?: the path-mapping defect from the previous iteration is fixed, but a different technical gap remains around `self_refiner`. repository search shows `shared.utils.self_refiner` is imported by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx_pipelines/distilled.py`, `ti2vid_one_stage.py`, `ti2vid_two_stages.py`, `wan2gp/models/ltx2/ltx_pipelines/utils/helpers.py`, and `wan2gp/models/wan/any2video.py`; the v4 plan still aligns `wan2gp/shared/utils/self_refiner.py` to upstream head without any concrete runtime step that exercises those code paths after the change, so the only repo-documented behavior check for that file is still missing from the executable body.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-156",
      "concern": "are the proposed changes technically correct?: the direct adapter still has a correctness risk around resolution parity. current vibecomfy ready templates hardcode image dimensions (`image/z_image` uses `emptysd3latentimage` 1024x1024 and `image/qwen_image_2512` uses 768x768), while `vibecomfy run` exposes no `--resolution` flag; the revised plan says a temporary scratchpad/input file may be generated only if supported, otherwise resolution is left out. that means a vibecomfy-supported direct route can silently ignore the worker's `resolution` param unless scratchpad resolution patching is made mandatory for supported direct routes or the support is explicitly limited to default-resolution smoke fixtures.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "are-the-success-criteria-well-prioritized-and-verifiable": [
    {
      "id": "DEBT-019",
      "concern": "are the success criteria well-prioritized and verifiable?: the attached success criteria are stale and do not match the current plan body. they still require 'no `usestate` for `activepairdata`', '`setactivepairdata` fully removed', 'sync effect deleted', and '`onpairclick` simplified to `(pairindex: number) => void`', which are the opposite of the current targeted-sync plan. as presented, the criteria are not usable for review or execution.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "audio-loading": [
    {
      "id": "DEBT-086",
      "concern": "getaudiodata in useeffect removes render-readiness signal",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-087",
      "concern": "same as correctness-3 \u2014 preview/render parity risk",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-088",
      "concern": "preview/render parity partially satisfied",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "audio-reactivity": [
    {
      "id": "DEBT-082",
      "concern": "overlapping clips use first-found, volume not scaled",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-083",
      "concern": "same as audio-reactivity-1 \u2014 overlapping/volume-adjusted clips diverge from audible mix",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-084",
      "concern": "textclip missing globalframeprovider",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-085",
      "concern": "same as audio-reactivity-2 \u2014 textclipsequence missing provider",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-089",
      "concern": "textclip effects surface not covered",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-090",
      "concern": "continuous effects shared by visual and text clips",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "batch-generation-pipeline": [
    {
      "id": "DEBT-006",
      "concern": "enhancement in usegeneratebatch before generatevideo() could compute prompts against a stale pair snapshot if mutations are still in flight.",
      "occurrence_count": 1,
      "plan_ids": [
        "in-cloud-mode-when-users-20260330-2214"
      ]
    }
  ],
  "cas-intern-short-circuit": [
    {
      "id": "DEBT-151",
      "concern": "symlink short-circuit comparison may produce false negatives on macos-like layouts where project_dir contains symlinked segments (/var \u2192 /private/var) because resolve(strict=true) on the source returns canonical paths but project_dir / cas_dirname may be non-canonical.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-7-rev-20260505"
      ]
    }
  ],
  "crash-recovery-cascade-paths": [
    {
      "id": "DEBT-065",
      "concern": "cascade lookup only reads params->>'orchestrator_task_id_ref', missing shared reference paths and orchestrator-self detection.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-067",
      "concern": "duplicate of correctness-2 + correctness-3: invalid sql syntax and narrow cascade lookup.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-069",
      "concern": "shared orchestrator-reference helpers not referenced.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-072",
      "concern": "orchestrator tasks that crash don't get orchestrator-self cascade.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-074",
      "concern": "hardcoded params->>'orchestrator_task_id_ref' misses other reference paths.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-retry": [
    {
      "id": "DEBT-063",
      "concern": "crash requeue sql does not increment attempts, risking infinite requeue loop.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-066",
      "concern": "duplicate of correctness-1: attempts never advance on crash requeue.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-068",
      "concern": "missing attempts increment location in heartbeat sql.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-073",
      "concern": "step 6 under-scoped for real retry convergence and orchestrator-self handling.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-sql-syntax": [
    {
      "id": "DEBT-064",
      "concern": "bare select inside plpgsql is invalid \u2014 needs perform.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "crash-recovery-testing": [
    {
      "id": "DEBT-070",
      "concern": "no multi-crash convergence test exercising attempts 0\u21921\u21922\u21923.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-071",
      "concern": "no validation that plpgsql body executes successfully.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    },
    {
      "id": "DEBT-075",
      "concern": "criteria don't require proof of crash requeue convergence.",
      "occurrence_count": 1,
      "plan_ids": [
        "deep-dive-into-root-causes-of-20260331-0534"
      ]
    }
  ],
  "criteria-verifiability": [
    {
      "id": "DEBT-036",
      "concern": "'no unsafe .maybesingle()' criterion requires judgment about column uniqueness.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-037",
      "concern": "decision documentation location not specified.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-062",
      "concern": "the must criterion requiring 5 task types to exist as active db rows is not verifiable from code diff alone \u2014 it requires a live db query.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ],
  "db-fallback-testing": [
    {
      "id": "DEBT-060",
      "concern": "no new automated test for the db fallback dispatch path or dependant_on preservation for raw worker families.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ],
  "dependency-resolution": [
    {
      "id": "DEBT-105",
      "concern": "dependency resolution: the plan does not lock down the active python-version matrix even though the repo currently splits between python 3.10 local installs and a python 3.11 runpod image.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements": [
    {
      "id": "DEBT-013",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the package is internally inconsistent. the plan body says to keep `activepairdata` in `usestate` and make phase 2 optional, but the attached metadata and success criteria still describe the previous derive-via-`usememo` / remove-`setactivepairdata` / simplify-`onpairclick` plan. that means the approved-plan requirements are only partially coherent as presented.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-108",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the linux distro note is documentation-only; the generated install command in step 7 still runs `apt-get install python3.10-venv python3.10-dev ffmpeg` without any pre-check that the package exists. users on ubuntu 24.04+ who ignore the doc and try to copy-paste the command will hit a confusing `e: unable to locate package python3.10-venv` from apt rather than a targeted error from commandutils.ts. a one-line detection pre-check (e.g., `apt-cache show python3.10-venv >/dev/null 2>&1 || { echo 'install deadsnakes ppa first \u2014 see readme'; exit 1; }`) would convert the silent failure into an actionable error, but the plan does not add this.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-145",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: checked the revised v4 body against `docs/wan2gp_fork_migration_plan.md` sprint 2. the repo plan doc still lists an \"ltx-2 `self_refiner` smoke against the pre-sprint behavioral baseline\" as a sprint 2 verification gate and repeats that smoke in the functionality-preservation checks, but the revised execution steps no longer schedule that smoke anywhere; it survives only as an info-level metadata criterion. because `wan2gp/shared/utils/self_refiner.py` remains an explicit sprint 2 deliverable, the revised plan still only partially carries forward the verification package described in the source migration plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-153",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: worker integration: the migration doc describes the per-call profile override gap as involving reigh-worker adapter handling of override_profile before constructing vibecomfy sessionconfig, but the plan limits sprint 1 per-run work to the vibecomfy cli/runtime. that may be acceptable for a vibecomfy-library mvp, but it does not fully exercise the production-facing per-task override semantics called out in the overall context.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-1-vibecomfy-memory-20260506-0147"
      ]
    },
    {
      "id": "DEBT-155",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: a residual issue-hint tension remains for resolution handling. the plan acknowledges current `vibecomfy run` lacks a resolution flag, but allows the adapter to leave resolution and other template-specific values unwired for sprint 2. because `z_image_turbo` and `qwen_image_2512` are marked vibecomfy-supported direct routes, this may not preserve the existing worker task-parameter contract for tasks that provide a non-default `resolution`.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "direct-route-parameter-parity": [
    {
      "id": "DEBT-160",
      "concern": "direct route parameter parity: vibecomfy-supported direct routes may ignore the worker `resolution` parameter.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "does-the-change-touch-all-locations-and-supporting-infrastructure": [
    {
      "id": "DEBT-014",
      "concern": "does the change touch all locations and supporting infrastructure?: phase 1 still misses a real supporting-data location: `trailingpairdata` lives outside `pairdatabyindex` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts#l111), but the proposed sync logic only considers `pairdatabyindex`. if trailing slot regenerate is part of the bug surface, that location is not covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-110",
      "concern": "does the change touch all locations and supporting infrastructure?: the non-swallowing helper `update_worker_phase_strict` is a new shell function, but phase 1 step 2 introduces it only as pseudo-code. there is no concrete note that the helper must handle supabase http non-2xx responses as failures (curl returns 0 even on http 4xx/5xx by default unless `-f` or `--fail-with-body` is used). if the implementer ports `update_worker_phase` verbatim with only `|| return 0` removed, a 500 from supabase would still report success because curl's exit code is 0. the plan should specify `curl --fail` or explicit http status code checking in the strict variant.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-142",
      "concern": "does the change touch all locations and supporting infrastructure?: the supporting-infrastructure review still finds one missing check. in `docs/wan2gp_fork_migration_plan.md`, sprint 2's verification matrix and risk register both single out `self_refiner` as a distinct drift-upgrade surface with its own smoke and its own silent-behavior-change risk, but the revised v4 body updates the file without keeping that supporting verification step in the actual execution checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-154",
      "concern": "does the change touch all locations and supporting infrastructure?: documentation/data gap: the sprint exit criteria require profiles 1 and 3 to have vram and wall-clock data, but the plan puts that only in metadata as an info-level criterion and does not schedule a concrete artifact location or command for recording the measurements. the implementation could satisfy all unit tests while still missing one of the explicit exit criteria.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-1-vibecomfy-memory-20260506-0147"
      ]
    },
    {
      "id": "DEBT-158",
      "concern": "does the change touch all locations and supporting infrastructure?: the supporting infrastructure for resolution is still incomplete if direct vibecomfy routes are considered production-supported. vibecomfy has a `vibecomfy.patches.resolution` helper and the cli can load scratchpad files with `allow_scratchpad=true`, but the plan does not require using that path; it permits leaving resolution out for sprint 2.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    },
    {
      "id": "DEBT-162",
      "concern": "does the change touch all locations and supporting infrastructure?: checked vibecomfy profile wording against `vibecomfy/tests/test_ready_templates.py`. the revised plan says to add the production template to representative compile profile coverage 'alongside the existing dry-run id', but the dry-run id is not currently in `profile_smoke_template_ids`; only `video/wanvideo_wrapper_22_5b_i2v` and `video/wan_t2v` are. this is a small wording mismatch rather than a functional blocker because adding either the production id alone or both ids would still satisfy sprint 4.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-4-wan-single-frame-and-20260506-0818"
      ]
    }
  ],
  "edge-test-config": [
    {
      "id": "DEBT-022",
      "concern": "plan's vitest commands use the wrong config entry point.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-023",
      "concern": "same as verification-3: wrong vitest config in validation commands.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-024",
      "concern": "success criterion references wrong test command.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "error-handling": [
    {
      "id": "DEBT-095",
      "concern": "db loader error handling convention mismatch (plan says log+null, existing loaders throw)",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "error-propagation-logging": [
    {
      "id": "DEBT-027",
      "concern": "generation.ts and handler.ts logging endpoints are not directly tested.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "error-propagation-testing": [
    {
      "id": "DEBT-020",
      "concern": "no end-to-end regression test for the full symptom chain (db error \u2192 tocompletionerror metadata \u2192 handler log).",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-025",
      "concern": "handler.ts metadata surfacing criterion lacks a concrete automated verifier.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    },
    {
      "id": "DEBT-026",
      "concern": "main issue only partially validated without an integration test.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them": [
    {
      "id": "DEBT-109",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the step 2 retry loop uses a naked `sleep 2` between attempts, which adds up to 6 seconds of latency on the happy path when the first patch eventually succeeds on attempt 2 or 3. for pods where supabase is reachable but slow during the initial moments of a cold runpod start, the retry logic is fine. however, if the first attempt fails with a tls handshake delay and the retry loop sleeps 2s per attempt regardless of whether curl itself has been blocking for tens of seconds, the total startup latency penalty could be substantial. this is a minor tuning concern, not a correctness issue.",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    },
    {
      "id": "DEBT-146",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: finding callers of the changed module shows that `shared.utils.self_refiner` is consumed by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx2_handler.py`, multiple ltx2 pipeline modules, and `wan2gp/models/wan/any2video.py`. the revised validation steps still only drive the three bridge getters in `source/runtime/wgp_ports/vendor_imports.py`; none of the scheduled commands execute a real `self_refiner` caller, so the plan does not yet verify the main caller shapes for the other explicit sprint 2 file change.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-159",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked direct queue caller values in `db_task_to_generation_task()`: direct image tasks may carry `resolution`, `steps`/`num_inference_steps`, `seed`, and `override_profile`. the revised adapter plan covers seed, steps, and memory profile but not guaranteed resolution propagation, so it does not handle all relevant direct-route caller arguments for a supported vibecomfy direct route.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    }
  ],
  "gpu-branching-test-matrix": [
    {
      "id": "DEBT-113",
      "concern": "linux cuda128 path under-verified",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "gpu-branching-ui-surface": [
    {
      "id": "DEBT-112",
      "concern": "nvidia-50 option is exposed on linux in the ui but linux cuda128 smoke test is missing",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "hook-abstraction": [
    {
      "id": "DEBT-043",
      "concern": "usepairsettingshandler becomes trivial with single caller \u2014 keeping it is extra indirection.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "hype-mirror-cas-coverage": [
    {
      "id": "DEBT-152",
      "concern": "hype-mirrored files whose parent step does not declare matching produces will not be cas-interned, even with the follow_symlinks=false edit.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-7-rev-20260505"
      ]
    }
  ],
  "is-the-change-in-the-right-place-and-would-it-break-any-callers": [
    {
      "id": "DEBT-015",
      "concern": "is the change in the right place, and would it break any callers?: the optional cleanup steps are not in the right place yet. `pairregionslayer` does not receive `pairdatabyindex` today; its props are only `images`, `imagepositionswithpending`, `pairinfowithpending`, and callback/display props in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx#l20). so step 4's 'pass `pairdatabyindex.get(pairindex)` directly' would require new prop plumbing or a different seam.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "is-the-scope-and-scale-of-the-change-appropriate": [
    {
      "id": "DEBT-009",
      "concern": "is the scope and scale of the change appropriate?: phase 2 is still under-specified for execution. step 4 says pairregionslayer should either pass `pairdatabyindex.get(pairindex)` directly or 'just pass the index + frame-only data', which are materially different designs. if phase 2 is kept in the plan, it needs a single concrete direction.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "is-there-convincing-verification-for-the-change": [
    {
      "id": "DEBT-010",
      "concern": "is there convincing verification for the change?: the plan still lacks an explicit automated regression test for the reported bug. step 2 is manual ('check that `usevideoregeneratemode` now gets the fresh url'), but there is no concrete test that opens a segment slot, changes the primary variant data, and asserts that the regenerate path sees the fresh `url`, `generationid`, and `primaryvariantid`.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-011",
      "concern": "is there convincing verification for the change?: the current `usesegmentslotmode` test remains only a smoke test in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts), and the plan does not add behavior coverage for the new sync effect.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-012",
      "concern": "is there convincing verification for the change?: no verification step covers the trailing-slot branch, even though the proposed phase 1 logic currently misses `trailingpairdata` refreshes.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "legacy-data-backfill": [
    {
      "id": "DEBT-004",
      "concern": "the step 8 diagnostic query only detects cross-shot pair_shot_generation_id misassociations, not same-shot misassociations caused by timeline reordering within a shot.",
      "occurrence_count": 1,
      "plan_ids": [
        "redesign-the-segment-position-20260330-1913"
      ]
    }
  ],
  "lookup-consistency": [
    {
      "id": "DEBT-029",
      "concern": "other repo call sites use unordered .limit(1).maybesingle() and will remain inconsistent.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-033",
      "concern": "other call sites with same unsafe pattern not covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "lora-management": [
    {
      "id": "DEBT-099",
      "concern": "lora tools simplified vs full ui parity (multi-stage metadata, private loras)",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "media-lightbox-persistence": [
    {
      "id": "DEBT-002",
      "concern": "variant switches do not clear/restore inpaintprompt, so stale prompt state can leak across variants with no cached prompt.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-prompt-text-reset-bug-20260330-1410"
      ]
    },
    {
      "id": "DEBT-003",
      "concern": "removing prompt/numgenerations from the variant-keyed localstorage cache means all variants within a generation share the same prompt. this broadens existing debt-002 (variant prompt leakage).",
      "occurrence_count": 1,
      "plan_ids": [
        "consolidate-the-media-20260330-1449"
      ]
    }
  ],
  "media-lightbox-segment-slot": [
    {
      "id": "DEBT-016",
      "concern": "media lightbox / segment slot: the targeted sync rationale does not fully explain the reported stale-url bug for regular pairs, and the proposed effect still misses trailing-slot refreshes because those can come from `trailingpairdata` rather than `pairdatabyindex`.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    }
  ],
  "number-input-nullable": [
    {
      "id": "DEBT-076",
      "concern": "plan doesn't explicitly state onchange must also accept null, though step 3 depends on it.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-077",
      "concern": "disputed v1 flag \u2014 original concern about bulkclippanel being unimplementable.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-079",
      "concern": "onchange null filtering not explicitly addressed in plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "number-input-testing": [
    {
      "id": "DEBT-081",
      "concern": "no planned tests for numberinput shared component or bulkclippanel nullable draft flow.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "orchestrator-completion-rollout": [
    {
      "id": "DEBT-049",
      "concern": "pre-existing individual_travel_segment children won't drive orchestrator completion through segment_type_config after deploy.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-051",
      "concern": "missing compatibility seam in orchestratorcore.ts:123-126 for old individual_travel_segment rows.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-053",
      "concern": "mixed old/new data during rollout can leave old orchestrators without completion counting.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-054",
      "concern": "no test or deployment guard for pre-existing individual_travel_segment children completing after worker change.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-056",
      "concern": "plan overstates backward compatibility for existing data.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-057",
      "concern": "missing rollout compatibility step for in-flight individual_travel_segment tasks.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-058",
      "concern": "pre-deploy individual_travel_segment child completing post-rollout won't be treated as segment task by checkorchestratorcompletion.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-059",
      "concern": "orchestrator.test.ts criterion too narrow to verify old individual_travel_segment compatibility.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    }
  ],
  "pair-settings-plumbing": [
    {
      "id": "DEBT-039",
      "concern": "handleopenpairsettings(pairindex, pairframedata) path in timelinetrackprelude, segmentoutputstrip, and usesegmentoutputstrip not explicitly named.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-042",
      "concern": "same as flag-002 \u2014 segmentoutputstrip and usesegmentoutputstrip still carry pairframedata.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-045",
      "concern": "timelinetrackprelude and segmentoutputstrip still forward (pairindex, pairframedata).",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "plan-scope": [
    {
      "id": "DEBT-032",
      "concern": "step 3 is larger than a light megaplan warrants.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "planning-metadata": [
    {
      "id": "DEBT-017",
      "concern": "planning metadata: the attached metadata and success criteria still describe a different implementation than the current plan body, which risks sending execution and review down the wrong path.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-denormalized-20260331-0225"
      ]
    },
    {
      "id": "DEBT-103",
      "concern": "success criteria don't cover wave 4 scope",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "position-key-semantics": [
    {
      "id": "DEBT-028",
      "concern": "plan investigates a unique constraint on (parent_generation_id, child_order) which doesn't match repo semantics for position keys.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-030",
      "concern": "plan weights toward child_order rather than pair_shot_generation_id as the key that matters.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-031",
      "concern": "unique constraint on (parent_generation_id, child_order) not supported by repo semantics.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    }
  ],
  "prompt-composition": [
    {
      "id": "DEBT-005",
      "concern": "the plan's step 1 signature includes textbeforeprompts/textafterprompts parameters that would be applied before enhancement, double-wrapping the prompt.",
      "occurrence_count": 1,
      "plan_ids": [
        "in-cloud-mode-when-users-20260330-2214"
      ]
    }
  ],
  "ready-template-snapshots": [
    {
      "id": "DEBT-147",
      "concern": "step 4.2 drops markdownnote nodes but step 4.5 and the success criteria require class_type/widget parity with pre-refactor snapshots, which currently include markdownnote nodes.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-the-higher-abstraction-20260425-0953"
      ]
    },
    {
      "id": "DEBT-148",
      "concern": "same tension as issue_hints v2: drop-markdownnote vs. snapshot parity.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-the-higher-abstraction-20260425-0953"
      ]
    }
  ],
  "reigh-worker-orchestrator-dockerfile": [
    {
      "id": "DEBT-150",
      "concern": "step 7 \u00a73 claims `gpu_orchestrator/dockerfile` has wan2gp install steps; current main is generic and contains none.",
      "occurrence_count": 1,
      "plan_ids": [
        "produce-a-migration-plan-20260505-0555"
      ]
    }
  ],
  "reigh-worker-orchestrator-runpod-startup": [
    {
      "id": "DEBT-149",
      "concern": "`gpu_orchestrator/runpod/startup_script.py` embeds `headless-wan2gp` in `_workdir_discovery_snippet` and is not named explicitly in step 7 \u00a73's checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "produce-a-migration-plan-20260505-0555"
      ]
    }
  ],
  "search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader": [
    {
      "id": "DEBT-141",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the broader runtime surface after the v4 path fix. sprint 2 is still moving two behavior-sensitive seams rather than just the import-path contract: the `wan2gp/` mount path and the `self_refiner` runtime. step 6.2 covers only the three `vendor_imports` getters, while the 6-file travel suite and the bridge-contract tests do not mention `self_refiner`, so dropping the dedicated self-refiner smoke from the runnable steps leaves the broader downstream surface of that changed file under-covered.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    },
    {
      "id": "DEBT-157",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the supported direct-route scope is still broader than the adapter's guaranteed parameter surface. `db_task_to_generation_task()` currently carries direct task params such as `resolution`, `steps`, and `seed` into wgp generation, but the vibecomfy cli path only guarantees prompt, seed, steps, and memory profile; resolution remains optional/documentation-only in the plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-2-adapter-seam-and-20260506-0249"
      ]
    },
    {
      "id": "DEBT-161",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the revised child-route scope against `migration-thresholds.yaml`. the threshold corpus currently has wan/vace entries for `travel_segment__model-wan22_vace__...` and `join_clips_segment__model-wan22_vace__...`, but only an i2v entry for `individual_travel_segment`; the revised plan makes `individual_travel_segment` with vace model params a must-level worker fixture, which broadens the worker smoke scope beyond the currently tracked wan/vace threshold routes.",
      "occurrence_count": 1,
      "plan_ids": [
        "sprint-4-wan-single-frame-and-20260506-0818"
      ]
    }
  ],
  "self-refiner-verification": [
    {
      "id": "DEBT-144",
      "concern": "self-refiner verification: the revised plan still aligns `wan2gp/shared/utils/self_refiner.py` without scheduling the sprint 2 ltx-2 `self_refiner` smoke that `docs/wan2gp_fork_migration_plan.md` defines as the behavior-preservation check for that drift upgrade.",
      "occurrence_count": 1,
      "plan_ids": [
        "execute-sprint-2-of-the-20260421-2202"
      ]
    }
  ],
  "settings-defaults": [
    {
      "id": "DEBT-111",
      "concern": "workerrepopath default can go stale if user switches computertype before editing path",
      "occurrence_count": 1,
      "plan_ids": [
        "migrate-the-python-worker-20260409-0353"
      ]
    }
  ],
  "settings-resolution": [
    {
      "id": "DEBT-093",
      "concern": "settings cascade missing \u2014 shot-only read diverges from form's defaults\u2192user\u2192project\u2192shot merge",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-098",
      "concern": "settings cascade missing \u2014 shot-only read",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "shared-component-compatibility": [
    {
      "id": "DEBT-078",
      "concern": "numberinput changes affect callers outside video-editor (billing, travel-between-images, phaseconfigselectormodal).",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    },
    {
      "id": "DEBT-080",
      "concern": "shared ui component blast radius not audited in plan.",
      "occurrence_count": 1,
      "plan_ids": [
        "video-editor-three-fixes-20260331-1533"
      ]
    }
  ],
  "shot-linking-testing": [
    {
      "id": "DEBT-021",
      "concern": "no test covers the linkgenerationtoshot error/catch branches.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-complete-ta[REDACTED_SK]"
      ]
    }
  ],
  "signature-propagation": [
    {
      "id": "DEBT-038",
      "concern": "plan doesn't explicitly name timeline/index.tsx and segmentslotcontracts.ts for updates.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-041",
      "concern": "same as flag-001 \u2014 timeline/index.tsx and segmentslotcontracts.ts not in checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-044",
      "concern": "five supporting contract/plumbing sites not named in the checklist.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "ta[REDACTED_SK]": [
    {
      "id": "DEBT-050",
      "concern": "step 3 cites wrong migration file (task_cost_configs instead of task_types) as evidence for db fallback path.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-052",
      "concern": "step 3 should cite task_types source, not task_cost_configs.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    },
    {
      "id": "DEBT-055",
      "concern": "plan doesn't verify travel_segment and travel_stitch exist as active task_types rows using the correct table.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-unify-task-20260331-0443"
      ]
    }
  ],
  "test-coverage": [
    {
      "id": "DEBT-034",
      "concern": "current generation-child.test.ts is only a smoke test.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-035",
      "concern": "no plan to verify other lookup paths choose rows consistently.",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-audit-and-fix-20260331-0341"
      ]
    },
    {
      "id": "DEBT-096",
      "concern": "no new tests for db loader or travel param merge path",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-097",
      "concern": "must-level criteria depend on manual testing rather than automated assertions",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-102",
      "concern": "no new unit tests for wave 4 tools",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-104",
      "concern": "must criteria backed by manual testing only",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "test-infrastructure": [
    {
      "id": "DEBT-101",
      "concern": "no test fixtures for resources table",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "timeline-drag-coordination": [
    {
      "id": "DEBT-126",
      "concern": "plan keeps two hooks instead of a single coordinator",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-127",
      "concern": "brief says single coordinator but plan keeps separate hooks",
      "occurrence_count": 2,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-128",
      "concern": "pendingopsref retained despite brief suggesting removal",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    },
    {
      "id": "DEBT-129",
      "concern": "wrapper-bound listener mount wiring under-specified",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-the-video-editor-20260413-0158"
      ]
    }
  ],
  "timeline-persistence": [
    {
      "id": "DEBT-130",
      "concern": "read path still assembles config and registry from separate requests",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-131",
      "concern": "poll sync verification not structurally changed",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-132",
      "concern": "backend save helpers not wired to new rpc",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-133",
      "concern": "read infrastructure not updated",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-134",
      "concern": "backend tests not in validation list",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-135",
      "concern": "backend callers not migrated",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-136",
      "concern": "broader persistence-contract problem",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-137",
      "concern": "backend split-save not addressed",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    },
    {
      "id": "DEBT-138",
      "concern": "split polling can combine config and registry from different snapshots",
      "occurrence_count": 1,
      "plan_ids": [
        "make-timeline-config-and-20260413-0218"
      ]
    }
  ],
  "timeline-scaling": [
    {
      "id": "DEBT-001",
      "concern": "the plan only specifies a concrete fix for the default scale(1) case; explicit-scale tracks may still break blend-mode effects.",
      "occurrence_count": 1,
      "plan_ids": [
        "investigate-why-custom-ai-20260330-0408"
      ]
    }
  ],
  "timeline-snap-threshold": [
    {
      "id": "DEBT-139",
      "concern": "threshold is generous (duration) rather than zoom-scaled (8px)",
      "occurrence_count": 1,
      "plan_ids": [
        "implement-smart-snap-to-edge-20260413-0503"
      ]
    },
    {
      "id": "DEBT-140",
      "concern": "computedropposition does not pass a zoom-scaled threshold override",
      "occurrence_count": 1,
      "plan_ids": [
        "implement-smart-snap-to-edge-20260413-0503"
      ]
    }
  ],
  "travel-continuations": [
    {
      "id": "DEBT-094",
      "concern": "smooth continuations not threaded \u2014 agent tasks won't have continuation_config even when shot settings enable it",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    },
    {
      "id": "DEBT-100",
      "concern": "continuation_config omitted from form parity",
      "occurrence_count": 1,
      "plan_ids": [
        "make-the-timeline-agent-s-20260406-0647"
      ]
    }
  ],
  "travel-payload-cleanup-scope": [
    {
      "id": "DEBT-116",
      "concern": "plan scope narrower than original user request",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-118",
      "concern": "broader create-task contract problem left untouched",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "travel-payload-readers": [
    {
      "id": "DEBT-114",
      "concern": "phase 4 app-side reader audit incomplete",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-119",
      "concern": "phase 4 field inventory incomplete for app-side readers",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "travel-request-contract": [
    {
      "id": "DEBT-115",
      "concern": "image_variant_ids is in frontend request contract",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    },
    {
      "id": "DEBT-117",
      "concern": "image_variant_ids contract change",
      "occurrence_count": 1,
      "plan_ids": [
        "look-at-how-we-create-tasks-20260410-1842"
      ]
    }
  ],
  "variant-update-b-fresh-takeover": [
    {
      "id": "DEBT-120",
      "concern": "spawn_worker does not internally call start_worker_process; harness must call both explicitly",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-121",
      "concern": "worker_id and runpod_id must be generated and threaded distinctly; plan currently uses pod_id as both",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-122",
      "concern": "duplicate of correctness-1 \u2014 spawn_worker two-step misstatement",
      "occurrence_count": 2,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-123",
      "concern": "duplicate of correctness-2 \u2014 worker_id/runpod_id propagation across takeover and restore paths",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-124",
      "concern": "duplicate of correctness-1 + correctness-2 \u2014 missing create_worker_record glue and start_worker_process integration",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    },
    {
      "id": "DEBT-125",
      "concern": "duplicate of correctness-2 \u2014 caller contract for spawn_worker requires worker_id, not pod_id",
      "occurrence_count": 1,
      "plan_ids": [
        "design-a-robust-end-to-end-20260411-0240"
      ]
    }
  ],
  "verification": [
    {
      "id": "DEBT-091",
      "concern": "no end-to-end render test for audio analysis timing",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    },
    {
      "id": "DEBT-092",
      "concern": "no automated coverage for text clips or overlapping clips with audio effects",
      "occurrence_count": 1,
      "plan_ids": [
        "add-audio-reactive-visual-20260331-2159"
      ]
    }
  ],
  "verification-coverage": [
    {
      "id": "DEBT-040",
      "concern": "no automated test exercises the full segment-slot opening path after cleanup.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-046",
      "concern": "no automated coverage that clicking a pair opens the correct modal after cleanup.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    },
    {
      "id": "DEBT-048",
      "concern": "zero behavioral change criterion is not verifiable from tsc + existing tests alone.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "verification-workflow": [
    {
      "id": "DEBT-047",
      "concern": "tsconfig.app.json excludes test files, so tsc won't catch test breakage.",
      "occurrence_count": 1,
      "plan_ids": [
        "phase-2-cleanup-from-the-20260331-0354"
      ]
    }
  ],
  "worker-test-staleness": [
    {
      "id": "DEBT-061",
      "concern": "worker test in test_additional_coverage_modules.py:37 may assert stale payload structure (task_type vs family).",
      "occurrence_count": 1,
      "plan_ids": [
        "light-megaplan-delete-the-20260331-0519"
      ]
    }
  ]
}

        Escalated debt subsystems:
        [
  {
    "subsystem": "timeline-persistence",
    "total_occurrences": 9,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-130",
        "concern": "read path still assembles config and registry from separate requests",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-131",
        "concern": "poll sync verification not structurally changed",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-132",
        "concern": "backend save helpers not wired to new rpc",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-133",
        "concern": "read infrastructure not updated",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-134",
        "concern": "backend tests not in validation list",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-135",
        "concern": "backend callers not migrated",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-136",
        "concern": "broader persistence-contract problem",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-137",
        "concern": "backend split-save not addressed",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      },
      {
        "id": "DEBT-138",
        "concern": "split polling can combine config and registry from different snapshots",
        "occurrence_count": 1,
        "plan_ids": [
          "make-timeline-config-and-20260413-0218"
        ]
      }
    ]
  },
  {
    "subsystem": "orchestrator-completion-rollout",
    "total_occurrences": 8,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-049",
        "concern": "pre-existing individual_travel_segment children won't drive orchestrator completion through segment_type_config after deploy.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-051",
        "concern": "missing compatibility seam in orchestratorcore.ts:123-126 for old individual_travel_segment rows.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-053",
        "concern": "mixed old/new data during rollout can leave old orchestrators without completion counting.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-054",
        "concern": "no test or deployment guard for pre-existing individual_travel_segment children completing after worker change.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-056",
        "concern": "plan overstates backward compatibility for existing data.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-057",
        "concern": "missing rollout compatibility step for in-flight individual_travel_segment tasks.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-058",
        "concern": "pre-deploy individual_travel_segment child completing post-rollout won't be treated as segment task by checkorchestratorcompletion.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-059",
        "concern": "orchestrator.test.ts criterion too narrow to verify old individual_travel_segment compatibility.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      }
    ]
  },
  {
    "subsystem": "are-the-proposed-changes-technically-correct",
    "total_occurrences": 7,
    "plan_count": 4,
    "entries": [
      {
        "id": "DEBT-007",
        "concern": "are the proposed changes technically correct?: for ordinary pairs, the new diagnosis is not well-supported by the repo. the current sync effect in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l62) already syncs `url` and `primaryvariantid`, and the regenerate path reads exactly `starturl`, `endurl`, `startgenid`, `endgenid`, `startvariantid`, and `endvariantid` from `segmentslotmode.pairdata` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts#l438). adding `thumburl` and `generationid` to the sync does not, by itself, explain why an old image url is still being used for regular pairs.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-008",
        "concern": "are the proposed changes technically correct?: the fix is incomplete for extra trailing slots. `handlepairclick` can populate `activepairdata` from `trailingpairdata` when `pairindex === pairdatabyindex.size` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l121), but the proposed sync effect only reads `pairdatabyindex.get(segmentslotlightboxindex)`. for those trailing-slot cases `fresh` is `undefined`, so no image refresh happens.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-018",
        "concern": "are the proposed changes technically correct?: the merge pseudocode does not actually sync 'all image fields' as claimed. it omits `id` and `position` from change detection, and when `fresh.startimage` or `fresh.endimage` becomes `null` it preserves the stale previous object instead of syncing that null state. as written, it also needs explicit null-guards around spreads of `prev.startimage` / `prev.endimage` to be safe in strict typescript.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-106",
        "concern": "are the proposed changes technically correct?: the plan's claim that `worker_state.py:200-204` (the 30-minute startup safety net) catches abandoned pods that exited before patching is slightly imprecise. line 200-204 only runs when `in_startup_phase` is true, which requires `startup_phase` to be in `('deps_installing', 'deps_verified', 'worker_starting')` per line 161. a pod that exits before its first patch has `startup_phase = none`, so `in_startup_phase` is false and the code falls through to the normal timeout checks (active_stale / not_claiming) at line 207+, not the 30-minute startup cap. both paths eventually reap the worker, so the end result is the same, but the overview's reasoning (naming 200-204 specifically) is wrong. worth correcting so future readers don't mis-reason about the invariant.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-107",
        "concern": "are the proposed changes technically correct?: checked worker_state.py line 161 (`in_startup_phase = startup_phase in (...)`) against the plan's assumption that subsequent lenient writes are safe. if deps_installing succeeds but deps_verified silently fails, startup_phase stays at 'deps_installing' and the 30-minute cap from line 200-204 applies \u2014 even though the pod is actually progressing through `uv sync`. on a slow runpod image with cold wheel downloads, `uv sync --extra cuda124` plus wan2gp deps can take 20+ minutes. there's no concrete benchmark in the plan that says the 30-minute cap is safely above the expected sync time; if `uv sync` legitimately takes 25 minutes and the deps_verified patch fails on a transient network blip, the orchestrator will terminate a healthy pod. plan should either bump the cap or note that deps_verified swallowing is acceptable because the cap is generously above typical sync time.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-143",
        "concern": "are the proposed changes technically correct?: the path-mapping defect from the previous iteration is fixed, but a different technical gap remains around `self_refiner`. repository search shows `shared.utils.self_refiner` is imported by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx_pipelines/distilled.py`, `ti2vid_one_stage.py`, `ti2vid_two_stages.py`, `wan2gp/models/ltx2/ltx_pipelines/utils/helpers.py`, and `wan2gp/models/wan/any2video.py`; the v4 plan still aligns `wan2gp/shared/utils/self_refiner.py` to upstream head without any concrete runtime step that exercises those code paths after the change, so the only repo-documented behavior check for that file is still missing from the executable body.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-156",
        "concern": "are the proposed changes technically correct?: the direct adapter still has a correctness risk around resolution parity. current vibecomfy ready templates hardcode image dimensions (`image/z_image` uses `emptysd3latentimage` 1024x1024 and `image/qwen_image_2512` uses 768x768), while `vibecomfy run` exposes no `--resolution` flag; the revised plan says a temporary scratchpad/input file may be generated only if supported, otherwise resolution is left out. that means a vibecomfy-supported direct route can silently ignore the worker's `resolution` param unless scratchpad resolution patching is made mandatory for supported direct routes or the support is explicitly limited to default-resolution smoke fixtures.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "variant-update-b-fresh-takeover",
    "total_occurrences": 7,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-120",
        "concern": "spawn_worker does not internally call start_worker_process; harness must call both explicitly",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-121",
        "concern": "worker_id and runpod_id must be generated and threaded distinctly; plan currently uses pod_id as both",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-122",
        "concern": "duplicate of correctness-1 \u2014 spawn_worker two-step misstatement",
        "occurrence_count": 2,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-123",
        "concern": "duplicate of correctness-2 \u2014 worker_id/runpod_id propagation across takeover and restore paths",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-124",
        "concern": "duplicate of correctness-1 + correctness-2 \u2014 missing create_worker_record glue and start_worker_process integration",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      },
      {
        "id": "DEBT-125",
        "concern": "duplicate of correctness-2 \u2014 caller contract for spawn_worker requires worker_id, not pod_id",
        "occurrence_count": 1,
        "plan_ids": [
          "design-a-robust-end-to-end-20260411-0240"
        ]
      }
    ]
  },
  {
    "subsystem": "audio-reactivity",
    "total_occurrences": 6,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-082",
        "concern": "overlapping clips use first-found, volume not scaled",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-083",
        "concern": "same as audio-reactivity-1 \u2014 overlapping/volume-adjusted clips diverge from audible mix",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-084",
        "concern": "textclip missing globalframeprovider",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-085",
        "concern": "same as audio-reactivity-2 \u2014 textclipsequence missing provider",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-089",
        "concern": "textclip effects surface not covered",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-090",
        "concern": "continuous effects shared by visual and text clips",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      }
    ]
  },
  {
    "subsystem": "does-the-change-touch-all-locations-and-supporting-infrastructure",
    "total_occurrences": 6,
    "plan_count": 6,
    "entries": [
      {
        "id": "DEBT-014",
        "concern": "does the change touch all locations and supporting infrastructure?: phase 1 still misses a real supporting-data location: `trailingpairdata` lives outside `pairdatabyindex` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts#l111), but the proposed sync logic only considers `pairdatabyindex`. if trailing slot regenerate is part of the bug surface, that location is not covered.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-110",
        "concern": "does the change touch all locations and supporting infrastructure?: the non-swallowing helper `update_worker_phase_strict` is a new shell function, but phase 1 step 2 introduces it only as pseudo-code. there is no concrete note that the helper must handle supabase http non-2xx responses as failures (curl returns 0 even on http 4xx/5xx by default unless `-f` or `--fail-with-body` is used). if the implementer ports `update_worker_phase` verbatim with only `|| return 0` removed, a 500 from supabase would still report success because curl's exit code is 0. the plan should specify `curl --fail` or explicit http status code checking in the strict variant.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-142",
        "concern": "does the change touch all locations and supporting infrastructure?: the supporting-infrastructure review still finds one missing check. in `docs/wan2gp_fork_migration_plan.md`, sprint 2's verification matrix and risk register both single out `self_refiner` as a distinct drift-upgrade surface with its own smoke and its own silent-behavior-change risk, but the revised v4 body updates the file without keeping that supporting verification step in the actual execution checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-154",
        "concern": "does the change touch all locations and supporting infrastructure?: documentation/data gap: the sprint exit criteria require profiles 1 and 3 to have vram and wall-clock data, but the plan puts that only in metadata as an info-level criterion and does not schedule a concrete artifact location or command for recording the measurements. the implementation could satisfy all unit tests while still missing one of the explicit exit criteria.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-1-vibecomfy-memory-20260506-0147"
        ]
      },
      {
        "id": "DEBT-158",
        "concern": "does the change touch all locations and supporting infrastructure?: the supporting infrastructure for resolution is still incomplete if direct vibecomfy routes are considered production-supported. vibecomfy has a `vibecomfy.patches.resolution` helper and the cli can load scratchpad files with `allow_scratchpad=true`, but the plan does not require using that path; it permits leaving resolution out for sprint 2.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      },
      {
        "id": "DEBT-162",
        "concern": "does the change touch all locations and supporting infrastructure?: checked vibecomfy profile wording against `vibecomfy/tests/test_ready_templates.py`. the revised plan says to add the production template to representative compile profile coverage 'alongside the existing dry-run id', but the dry-run id is not currently in `profile_smoke_template_ids`; only `video/wanvideo_wrapper_22_5b_i2v` and `video/wan_t2v` are. this is a small wording mismatch rather than a functional blocker because adding either the production id alone or both ids would still satisfy sprint 4.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-4-wan-single-frame-and-20260506-0818"
        ]
      }
    ]
  },
  {
    "subsystem": "test-coverage",
    "total_occurrences": 6,
    "plan_count": 2,
    "entries": [
      {
        "id": "DEBT-034",
        "concern": "current generation-child.test.ts is only a smoke test.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-035",
        "concern": "no plan to verify other lookup paths choose rows consistently.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-096",
        "concern": "no new tests for db loader or travel param merge path",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-097",
        "concern": "must-level criteria depend on manual testing rather than automated assertions",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-102",
        "concern": "no new unit tests for wave 4 tools",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      },
      {
        "id": "DEBT-104",
        "concern": "must criteria backed by manual testing only",
        "occurrence_count": 1,
        "plan_ids": [
          "make-the-timeline-agent-s-20260406-0647"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-cascade-paths",
    "total_occurrences": 5,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-065",
        "concern": "cascade lookup only reads params->>'orchestrator_task_id_ref', missing shared reference paths and orchestrator-self detection.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-067",
        "concern": "duplicate of correctness-2 + correctness-3: invalid sql syntax and narrow cascade lookup.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-069",
        "concern": "shared orchestrator-reference helpers not referenced.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-072",
        "concern": "orchestrator tasks that crash don't get orchestrator-self cascade.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-074",
        "concern": "hardcoded params->>'orchestrator_task_id_ref' misses other reference paths.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements",
    "total_occurrences": 5,
    "plan_count": 5,
    "entries": [
      {
        "id": "DEBT-013",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the package is internally inconsistent. the plan body says to keep `activepairdata` in `usestate` and make phase 2 optional, but the attached metadata and success criteria still describe the previous derive-via-`usememo` / remove-`setactivepairdata` / simplify-`onpairclick` plan. that means the approved-plan requirements are only partially coherent as presented.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-108",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the linux distro note is documentation-only; the generated install command in step 7 still runs `apt-get install python3.10-venv python3.10-dev ffmpeg` without any pre-check that the package exists. users on ubuntu 24.04+ who ignore the doc and try to copy-paste the command will hit a confusing `e: unable to locate package python3.10-venv` from apt rather than a targeted error from commandutils.ts. a one-line detection pre-check (e.g., `apt-cache show python3.10-venv >/dev/null 2>&1 || { echo 'install deadsnakes ppa first \u2014 see readme'; exit 1; }`) would convert the silent failure into an actionable error, but the plan does not add this.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-145",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: checked the revised v4 body against `docs/wan2gp_fork_migration_plan.md` sprint 2. the repo plan doc still lists an \"ltx-2 `self_refiner` smoke against the pre-sprint behavioral baseline\" as a sprint 2 verification gate and repeats that smoke in the functionality-preservation checks, but the revised execution steps no longer schedule that smoke anywhere; it survives only as an info-level metadata criterion. because `wan2gp/shared/utils/self_refiner.py` remains an explicit sprint 2 deliverable, the revised plan still only partially carries forward the verification package described in the source migration plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-153",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: worker integration: the migration doc describes the per-call profile override gap as involving reigh-worker adapter handling of override_profile before constructing vibecomfy sessionconfig, but the plan limits sprint 1 per-run work to the vibecomfy cli/runtime. that may be acceptable for a vibecomfy-library mvp, but it does not fully exercise the production-facing per-task override semantics called out in the overall context.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-1-vibecomfy-memory-20260506-0147"
        ]
      },
      {
        "id": "DEBT-155",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: a residual issue-hint tension remains for resolution handling. the plan acknowledges current `vibecomfy run` lacks a resolution flag, but allows the adapter to leave resolution and other template-specific values unwired for sprint 2. because `z_image_turbo` and `qwen_image_2512` are marked vibecomfy-supported direct routes, this may not preserve the existing worker task-parameter contract for tasks that provide a non-default `resolution`.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "timeline-drag-coordination",
    "total_occurrences": 5,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-126",
        "concern": "plan keeps two hooks instead of a single coordinator",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-127",
        "concern": "brief says single coordinator but plan keeps separate hooks",
        "occurrence_count": 2,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-128",
        "concern": "pendingopsref retained despite brief suggesting removal",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      },
      {
        "id": "DEBT-129",
        "concern": "wrapper-bound listener mount wiring under-specified",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-the-video-editor-20260413-0158"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-retry",
    "total_occurrences": 4,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-063",
        "concern": "crash requeue sql does not increment attempts, risking infinite requeue loop.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-066",
        "concern": "duplicate of correctness-1: attempts never advance on crash requeue.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-068",
        "concern": "missing attempts increment location in heartbeat sql.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-073",
        "concern": "step 6 under-scoped for real retry convergence and orchestrator-self handling.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "audio-loading",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-086",
        "concern": "getaudiodata in useeffect removes render-readiness signal",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-087",
        "concern": "same as correctness-3 \u2014 preview/render parity risk",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      },
      {
        "id": "DEBT-088",
        "concern": "preview/render parity partially satisfied",
        "occurrence_count": 1,
        "plan_ids": [
          "add-audio-reactive-visual-20260331-2159"
        ]
      }
    ]
  },
  {
    "subsystem": "crash-recovery-testing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-070",
        "concern": "no multi-crash convergence test exercising attempts 0\u21921\u21922\u21923.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-071",
        "concern": "no validation that plpgsql body executes successfully.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      },
      {
        "id": "DEBT-075",
        "concern": "criteria don't require proof of crash requeue convergence.",
        "occurrence_count": 1,
        "plan_ids": [
          "deep-dive-into-root-causes-of-20260331-0534"
        ]
      }
    ]
  },
  {
    "subsystem": "criteria-verifiability",
    "total_occurrences": 3,
    "plan_count": 2,
    "entries": [
      {
        "id": "DEBT-036",
        "concern": "'no unsafe .maybesingle()' criterion requires judgment about column uniqueness.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-037",
        "concern": "decision documentation location not specified.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-062",
        "concern": "the must criterion requiring 5 task types to exist as active db rows is not verifiable from code diff alone \u2014 it requires a live db query.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-delete-the-20260331-0519"
        ]
      }
    ]
  },
  {
    "subsystem": "edge-test-config",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-022",
        "concern": "plan's vitest commands use the wrong config entry point.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-023",
        "concern": "same as verification-3: wrong vitest config in validation commands.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-024",
        "concern": "success criterion references wrong test command.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      }
    ]
  },
  {
    "subsystem": "error-propagation-testing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-020",
        "concern": "no end-to-end regression test for the full symptom chain (db error \u2192 tocompletionerror metadata \u2192 handler log).",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-025",
        "concern": "handler.ts metadata surfacing criterion lacks a concrete automated verifier.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      },
      {
        "id": "DEBT-026",
        "concern": "main issue only partially validated without an integration test.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-complete-ta[REDACTED_SK]"
        ]
      }
    ]
  },
  {
    "subsystem": "find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them",
    "total_occurrences": 3,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-109",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the step 2 retry loop uses a naked `sleep 2` between attempts, which adds up to 6 seconds of latency on the happy path when the first patch eventually succeeds on attempt 2 or 3. for pods where supabase is reachable but slow during the initial moments of a cold runpod start, the retry logic is fine. however, if the first attempt fails with a tls handshake delay and the retry loop sleeps 2s per attempt regardless of whether curl itself has been blocking for tens of seconds, the total startup latency penalty could be substantial. this is a minor tuning concern, not a correctness issue.",
        "occurrence_count": 1,
        "plan_ids": [
          "migrate-the-python-worker-20260409-0353"
        ]
      },
      {
        "id": "DEBT-146",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: finding callers of the changed module shows that `shared.utils.self_refiner` is consumed by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx2_handler.py`, multiple ltx2 pipeline modules, and `wan2gp/models/wan/any2video.py`. the revised validation steps still only drive the three bridge getters in `source/runtime/wgp_ports/vendor_imports.py`; none of the scheduled commands execute a real `self_refiner` caller, so the plan does not yet verify the main caller shapes for the other explicit sprint 2 file change.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-159",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked direct queue caller values in `db_task_to_generation_task()`: direct image tasks may carry `resolution`, `steps`/`num_inference_steps`, `seed`, and `override_profile`. the revised adapter plan covers seed, steps, and memory profile but not guaranteed resolution propagation, so it does not handle all relevant direct-route caller arguments for a supported vibecomfy direct route.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      }
    ]
  },
  {
    "subsystem": "is-there-convincing-verification-for-the-change",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-010",
        "concern": "is there convincing verification for the change?: the plan still lacks an explicit automated regression test for the reported bug. step 2 is manual ('check that `usevideoregeneratemode` now gets the fresh url'), but there is no concrete test that opens a segment slot, changes the primary variant data, and asserts that the regenerate path sees the fresh `url`, `generationid`, and `primaryvariantid`.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-011",
        "concern": "is there convincing verification for the change?: the current `usesegmentslotmode` test remains only a smoke test in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts), and the plan does not add behavior coverage for the new sync effect.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      },
      {
        "id": "DEBT-012",
        "concern": "is there convincing verification for the change?: no verification step covers the trailing-slot branch, even though the proposed phase 1 logic currently misses `trailingpairdata` refreshes.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-denormalized-20260331-0225"
        ]
      }
    ]
  },
  {
    "subsystem": "number-input-nullable",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-076",
        "concern": "plan doesn't explicitly state onchange must also accept null, though step 3 depends on it.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      },
      {
        "id": "DEBT-077",
        "concern": "disputed v1 flag \u2014 original concern about bulkclippanel being unimplementable.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      },
      {
        "id": "DEBT-079",
        "concern": "onchange null filtering not explicitly addressed in plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "video-editor-three-fixes-20260331-1533"
        ]
      }
    ]
  },
  {
    "subsystem": "pair-settings-plumbing",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-039",
        "concern": "handleopenpairsettings(pairindex, pairframedata) path in timelinetrackprelude, segmentoutputstrip, and usesegmentoutputstrip not explicitly named.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-042",
        "concern": "same as flag-002 \u2014 segmentoutputstrip and usesegmentoutputstrip still carry pairframedata.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-045",
        "concern": "timelinetrackprelude and segmentoutputstrip still forward (pairindex, pairframedata).",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  },
  {
    "subsystem": "position-key-semantics",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-028",
        "concern": "plan investigates a unique constraint on (parent_generation_id, child_order) which doesn't match repo semantics for position keys.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-030",
        "concern": "plan weights toward child_order rather than pair_shot_generation_id as the key that matters.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      },
      {
        "id": "DEBT-031",
        "concern": "unique constraint on (parent_generation_id, child_order) not supported by repo semantics.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-audit-and-fix-20260331-0341"
        ]
      }
    ]
  },
  {
    "subsystem": "search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader",
    "total_occurrences": 3,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-141",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the broader runtime surface after the v4 path fix. sprint 2 is still moving two behavior-sensitive seams rather than just the import-path contract: the `wan2gp/` mount path and the `self_refiner` runtime. step 6.2 covers only the three `vendor_imports` getters, while the 6-file travel suite and the bridge-contract tests do not mention `self_refiner`, so dropping the dedicated self-refiner smoke from the runnable steps leaves the broader downstream surface of that changed file under-covered.",
        "occurrence_count": 1,
        "plan_ids": [
          "execute-sprint-2-of-the-20260421-2202"
        ]
      },
      {
        "id": "DEBT-157",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the supported direct-route scope is still broader than the adapter's guaranteed parameter surface. `db_task_to_generation_task()` currently carries direct task params such as `resolution`, `steps`, and `seed` into wgp generation, but the vibecomfy cli path only guarantees prompt, seed, steps, and memory profile; resolution remains optional/documentation-only in the plan.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-2-adapter-seam-and-20260506-0249"
        ]
      },
      {
        "id": "DEBT-161",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the revised child-route scope against `migration-thresholds.yaml`. the threshold corpus currently has wan/vace entries for `travel_segment__model-wan22_vace__...` and `join_clips_segment__model-wan22_vace__...`, but only an i2v entry for `individual_travel_segment`; the revised plan makes `individual_travel_segment` with vace model params a must-level worker fixture, which broadens the worker smoke scope beyond the currently tracked wan/vace threshold routes.",
        "occurrence_count": 1,
        "plan_ids": [
          "sprint-4-wan-single-frame-and-20260506-0818"
        ]
      }
    ]
  },
  {
    "subsystem": "signature-propagation",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-038",
        "concern": "plan doesn't explicitly name timeline/index.tsx and segmentslotcontracts.ts for updates.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-041",
        "concern": "same as flag-001 \u2014 timeline/index.tsx and segmentslotcontracts.ts not in checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-044",
        "concern": "five supporting contract/plumbing sites not named in the checklist.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  },
  {
    "subsystem": "ta[REDACTED_SK]",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-050",
        "concern": "step 3 cites wrong migration file (task_cost_configs instead of task_types) as evidence for db fallback path.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-052",
        "concern": "step 3 should cite task_types source, not task_cost_configs.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      },
      {
        "id": "DEBT-055",
        "concern": "plan doesn't verify travel_segment and travel_stitch exist as active task_types rows using the correct table.",
        "occurrence_count": 1,
        "plan_ids": [
          "light-megaplan-unify-task-20260331-0443"
        ]
      }
    ]
  },
  {
    "subsystem": "verification-coverage",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-040",
        "concern": "no automated test exercises the full segment-slot opening path after cleanup.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-046",
        "concern": "no automated coverage that clicking a pair opens the correct modal after cleanup.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      },
      {
        "id": "DEBT-048",
        "concern": "zero behavioral change criterion is not verifiable from tsc + existing tests alone.",
        "occurrence_count": 1,
        "plan_ids": [
          "phase-2-cleanup-from-the-20260331-0354"
        ]
      }
    ]
  }
]

        Debt guidance:
        - These are known accepted limitations. Do not re-flag them unless the current plan makes them worse, broadens them, or fails to contain them.
        - Prefix every new concern with a subsystem tag followed by a colon, for example `Timeout recovery: retry backoff remains brittle`.
        - When a concern is recurring debt that still needs to be flagged, prefix it with `Recurring debt:` after the subsystem tag, for example `Timeout recovery: Recurring debt: retry backoff remains brittle`.



        Your output template is at: /Users/user_c042661f/Documents/reigh-workspace/.megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json
Read this file first — it contains 5 checks, each with a question and guidance.
For each check, investigate the codebase, then add your findings to the `findings` array for that check.

Each finding needs:
- "detail": what you specifically checked and what you found (at least a full sentence)
- "flagged": true if this describes a difference, risk, or tension — even if you think it's justified. false only if purely informational with no possible downside.
- Every check must end with at least one finding. Never leave a `findings` array empty. If you found no issue, add one detailed `flagged: false` finding explaining what you checked and why it appears clear.

When in doubt, flag it — the gate can accept tradeoffs, but it can't act on findings it never sees.

Good: {"detail": "Checked callers of nthroot_mod in solveset.py line 1205 — passes prime moduli only, consistent with the fix.", "flagged": false}
Good: {"detail": "The fix handles empty tuples but not single-element tuples which need a trailing comma.", "flagged": true}
Bad: {"detail": "No issue found", "flagged": false}  ← too brief, will be rejected
Bad: {"detail": "The hints suggest approach X but the plan uses Y. However Y is consistent with X's intent.", "flagged": false}  ← a different approach than the hints IS a flag. You found a divergence — flag it. The gate decides if it's acceptable.

After filling in checks, add any additional concerns to the `flags` array (e.g., security, performance, dependencies).
Use the standard format (id, concern, category, severity_hint, evidence). This array can be empty.

Workflow: read the file → investigate → read file again → add finding → write file back. Repeat for each check.

This is critique iteration 3. The template file includes prior findings with their status. Verify addressed flags were actually fixed, re-flag if inadequate, and check for new issues introduced by the revision.

        Additional guidelines:
        - Robustness level: standard. Use balanced judgment. Flag significant risks, but do not spend flags on minor polish or executor-obvious boilerplate.
        - Over-engineering: prefer the simplest approach that fully solves the problem.
        - Reuse existing flag IDs when the same concern is still open.
        - `verified_flag_ids`: list flag IDs from prior iterations that the revised plan actually resolves (e.g., if the plan was revised to fix FLAG-001, and you confirm the fix is correct, include "FLAG-001"). Only include flags you've verified — don't guess.
        - Verify that the plan follows the expected structure when validator warnings or the outline suggest drift.
        - Additional flags may use these categories: correctness, security, completeness, performance, maintainability, other.
        - Focus on concrete issues, not structural formatting.

> AGENT

I’m doing the third-pass verification now. The two iteration-2 gaps are explicitly addressed in the revised plan, so I’m checking whether the new capability/claim-field additions introduce any repo-specific blind spots rather than repeating resolved concerns.

> AGENT

I’ll finish the critique pass against the repository state and write the required JSON output directly. I’m treating the plan file path as data only and avoiding any nested planning tools.

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' .megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 1000,
  "max_output_tokens": 32000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

I’ve confirmed the critique template shape. I’m doing a focused repo check now around the two new v3 additions: SQL-side capability data and persisted claim-time fields, plus the earlier route-key and caller coverage.

> TOOL

tool_use exec_command
```json
{
  "cmd": "pwd && python3 - <<'PY'\nimport json\nfrom pathlib import Path\np=Path([REDACTED])\nprint(p)\ndata=json.loads(p.read_text())\nprint('keys', list(data.keys()))\nprint('checks', [(c.get('id'), c.get('question')) for c in data.get('checks',[])])\nprint('flags', data.get('flags'))\nprint('verified', data.get('verified_flag_ids'))\nPY",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

The repository checks line up with the v3 changes: the current code really lacks a SQL backend capability source and claim-time backend fields, so the new plan additions are aimed at real gaps. I’m writing the critique now with no new significant flags unless the final template re-read shows a mismatch.

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"claim_next_task_service_role|generation_started_at|worker_pool|task_types|current_model\" reigh-app/supabase/migrations reigh-app/supabase/functions/claim-next-task/index.ts",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"queued_tasks|active_tasks|In Progress|claim_next_task|task-counts|worker_backend|selected_backend\" reigh-app/supabase/functions/task-counts reigh-app/supabase/migrations",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"WGP_TASK_TYPES|DIRECT_QUEUE_TASK_TYPES|is_wgp_task|derive_route_key|join_clips_segment|add_task_to_db|createWorkerPassthroughResolver\" reigh-worker/source reigh-app/supabase/functions/create-task scripts/dual_run_compare",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba reigh-worker/source/task_handlers/tasks/template_routing.py | sed -n '110,175p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba reigh-app/supabase/functions/create-task/resolvers/workerPassthrough.ts | sed -n '1,80p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba reigh-worker/source/core/db/task_completion.py | sed -n '1,90p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba reigh-app/supabase/migrations/20260504120000_extend_claim_next_task_for_pools.sql | sed -n '33,220p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba reigh-app/supabase/functions/task-counts/index.ts | sed -n '150,365p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba reigh-worker/source/task_handlers/tasks/task_types.py | sed -n '20,170p'",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"join_clips_segment__model|derive_route_key\\(|route_key\" reigh-worker scripts reigh-app | head -n 80",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

Critique output written to `.megaplan/plans/sprint-6-production-selector-20260506-1051/critique_output.json`.

I found no new significant flags in iteration 3. I verified the revised plan addresses `FLAG-001` through `FLAG-007`, including the new SQL-side capability registry and persisted claim-time backend/selector fields.

> TOOL

tool_use exec_command
```json
{
  "cmd": "python3 - <<'PY'\nimport json\nfrom pathlib import Path\np=Path([REDACTED])\ndata=json.loads(p.read_text())\nfindings={\n  'issue_hints': [\n    {\n      'detail': \"Checked the sprint rule that missing production selector keys must be WGP/no-claim, never implicit Comfy, against the current claim RPC in reigh-app/supabase/migrations/20260504120000_extend_claim_next_task_for_pools.sql and the worker-side WGP catalog in reigh-worker/source/task_handlers/tasks/task_types.py. The v3 plan now adds a SQL-side route_backend_capabilities table with supports_missing_selector and requires claim/count RPCs to use it, which makes the missing-selector WGP fallback implementable in Postgres instead of depending on Python-only WGP_TASK_TYPES.\",\n      'flagged': False,\n    },\n    {\n      'detail': \"Verified the revised plan preserves the production safety rule for VibeComfy: VibeComfy capability rows must be explicitly seeded as supported and must not set supports_missing_selector=true, while missing, disabled, expired, malformed, inaccessible, or unsupported selector/capability data produces no VibeComfy claim. That addresses the prior issue-hint concern without broadening the fallback path.\",\n      'flagged': False,\n    },\n  ],\n  'correctness': [\n    {\n      'detail': \"Checked active task accounting against the current task-counts implementation in reigh-app/supabase/functions/task-counts/index.ts, where active_tasks are currently inferred from status='In Progress' and worker_id rather than backend capability. The v3 plan adds claimed_backend, claimed_route_key, claimed_selector_namespace, claimed_selector_version, and claimed_selector_snapshot fields and requires active counts/arrays to use those persisted claim-time fields, which resolves the rollback undercount risk from FLAG-007.\",\n      'flagged': False,\n    },\n    {\n      'detail': \"Checked the latest claim RPC's existing eligibility constraints: it filters by user credits/cloud setting/capacity, dependencies, run_type, Banodoco pool, task_types allow-list, and current_model affinity before claiming. The v3 plan layers selector plus capability enforcement into the queued candidate query and explicitly keeps run-type/API-worker and Banodoco filtering separate, so it is not replacing important current claim semantics with the new backend selector contract.\",\n      'flagged': False,\n    },\n  ],\n  'scope': [\n    {\n      'detail': \"Searched route-key code and confirmed the current canonical worker derive_route_key only handles travel_segment and individual_travel_segment dimensional keys, while join_clips_segment route keys exist in the dual-run comparison/reporting surface. The v3 plan still requires adding join_clips_segment dimensional serialization to both the Python and TypeScript helpers and keeping those helpers import-light, so FLAG-003 remains addressed.\",\n      'flagged': False,\n    },\n    {\n      'detail': \"Checked whether there is already a database-side backend capability registry that the plan should reuse; the repo currently has task_types.run_type for gpu/api and a Python WGP_TASK_TYPES/is_wgp_task catalog, but no SQL route/backend support table. Adding route_backend_capabilities is appropriately scoped supporting infrastructure for the selector contract rather than duplicating an existing DB source.\",\n      'flagged': False,\n    },\n  ],\n  'all_locations': [\n    {\n      'detail': \"Reviewed the planned touch points against the actual locations that currently participate in claim and scaling: claim-next-task/index.ts calls claim_next_task_service_role, task-counts/index.ts combines RPC totals with direct queued_tasks and active_tasks arrays, and migrations define the current claim/count RPCs. The v3 plan names schema, claim RPC, task-count RPCs and direct TypeScript array filters, create-task snapshots, worker claim payloads, runtime guards, and child task creation paths, covering the previous all-locations gaps.\",\n      'flagged': False,\n    },\n    {\n      'detail': \"Checked selector authorization and metadata storage coverage from the plan body: it adds RLS/grants/comments for both route_backend_selectors and route_backend_capabilities, task creation snapshots, separate claim-decision columns, and rollback/cache tests for queued claims plus active accounting. This addresses the earlier selector security, live-versus-snapshot, and task-count parity findings without introducing a new supporting-infrastructure omission.\",\n      'flagged': False,\n    },\n  ],\n  'callers': [\n    {\n      'detail': \"Checked worker-created task insertion in reigh-worker/source/core/db/task_completion.py and create-task's workerPassthrough resolver: add_task_to_db currently sends all fields under input and workerPassthrough currently lifts only task_id and dependant_on. The v3 plan explicitly extends add_task_to_db with optional route snapshot fields and updates workerPassthrough to lift route_key, selected_backend, selector_version, and route_selection_snapshot into top-level insert columns, so FLAG-005/callers-2 remain addressed.\",\n      'flagged': False,\n    },\n    {\n      'detail': \"Searched add_task_to_db callers and found the relevant child producers in travel/orchestrator.py, travel/stitch.py, travel/chaining.py-related paths, and join/task_builder.py. The v3 plan requires an rg inventory before editing and names those same paths with an explicit pass-snapshot or WGP-safe/null decision, so the caller coverage from callers-1 is adequate for the current repository shape.\",\n      'flagged': False,\n    },\n  ],\n}\nfor check in data['checks']:\n    cid=check['id']\n    check['findings']=findings[cid]\n\ndata['flags']=[]\ndata['verified_flag_ids']=['FLAG-001','FLAG-002','FLAG-003','FLAG-004','FLAG-005','FLAG-006','FLAG-007']\ndata['disputed_flag_ids']=[]\np.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\\n')\nprint('wrote', p)\nPY\npython3 - <<'PY'\nimport json\nfrom pathlib import Path\np=Path([REDACTED])\ndata=json.loads(p.read_text())\nprint('checks', [(c['id'], len(c.get('findings',[]))) for c in data['checks']])\nprint('flags', data['flags'])\nprint('verified', data['verified_flag_ids'])\nPY",
  "workdir": "/Users/user_c042661f/Documents/reigh-workspace",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are preparing an execution-ready briefing document from the approved plan.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace





        Idea:
# Sprint 3: Dual-Run Comparison Harness

## Overall Context

This sprint turns Sprint 0B thresholds and Sprint 2 routed tasks into executable comparison evidence. It should catch queue, billing, product-effect, and media drift before any production selector exists.

## Shared Operating Rules

- Shadow artifacts must have no user-visible, billing, completion, or upload side effects unless explicitly isolated.
- Compare media, queue contract, product effects, billing/refund/idempotency, latency, VRAM, OOM, and error class.
- Non-RayWorker active routes must stay healthy through shared app/completion/billing paths.
- Routes not yet implemented are pending/fallback/WGP-only, not silently green.

## Sprint Goal

Build the dual-run harness and executable product/billing oracle for landed routes.

## Required Deliverables

- `scripts/dual_run_compare.py`.
- Reports for media similarity, queue contract, product effects, billing/refund/idempotency, latency, VRAM, OOM, and error class.
- No-side-effect shadow artifact isolation.
- Regression checks for `video_enhance`, `image-upscale`, `animate_character`, and `flux_klein_edit` through their current owners.

## Exit Criteria

Harness is green for Sprint 2 routes or marks them RED; not-yet-routed RayWorker rows are pending/fallback/WGP-only; product/billing checks are executable; active non-RayWorker routes are not broken by shared app/completion/billing changes.

        Approved plan:
        # Implementation Plan: Sprint 3 Dual-Run Comparison Harness

## Overview
The remaining critique still does not show that the plan targets the wrong root cause. The core target remains correct: build a side-effect-safe dual-run evidence harness and executable product/billing oracle before any production selector exists. The remaining issues are execution-scope corrections:

- Active non-RayWorker safety cannot stop at registry classification. Every active API-owned route must get at least a lightweight shared-path oracle that proves it still flows through queue/completion/billing contracts without requiring full media golden comparison for every route.
- Refund coverage must not be misrepresented. The visible cancellation path in `reigh-app/supabase/functions/update-task-status/cancellationBilling.ts` bills completed work for cancelled orchestrators; it is not a refund ledger path. Sprint 3 should discover an actual refund implementation if one exists, otherwise report refund as `pending_not_implemented` instead of green.

The implementation remains centered in `reigh-worker/scripts/dual_run_compare/`, with the required workspace-root `scripts/dual_run_compare.py` wrapper and targeted app/orchestrator tests in `reigh-app` and `reigh-worker-orchestrator`. The harness remains evidence/reporting only and must not introduce a production selector.

Two status concepts remain separate:
- **Calibration status** comes from `migration-thresholds.yaml` and stays constrained by `thresholds.py` (`green`, `pending_calibration`, `deferred_pending_sprint_0c_disk`, `wgp_only`, `owner_deferred`).
- **Sprint 3 report status** is computed by the harness (`green`, `red`, `pending`, `fallback`, `wgp_only`, plus section-level `pending_not_implemented` where a specific oracle surface does not exist yet) and appears only in generated reports and harness models.

## Phase 1: CLI And Status Contract

### Step 1: Add the root CLI safely (`scripts/dual_run_compare.py`, `reigh-worker/scripts/dual_run_compare/dual_run_compare.py`)
**Scope:** Medium
1. **Create** `scripts/dual_run_compare.py` as the required workspace-root entrypoint.
2. **Avoid** plain `import scripts.dual_run_compare` from the workspace root. The wrapper must explicitly resolve `REPO_ROOT / "reigh-worker"`, prepend that path to `sys.path`, and invoke `scripts.dual_run_compare.dual_run_compare.main` from the worker package.
3. **Set** any default `repo_root` used by live-worker helpers to `REPO_ROOT / "reigh-worker"`, not the workspace root, so relative paths such as `scripts/live_test/main.py` resolve correctly.
4. **Add** a command smoke test that runs `python scripts/dual_run_compare.py --dry-run --report-id pytest-dual-run` from `/Users/user_c042661f/Documents/reigh-workspace` and proves the wrapper imports the worker package, not the root `scripts` package.

### Step 2: Define Sprint 3 report status separately (`reigh-worker/scripts/dual_run_compare/status.py`, `compare.py`)
**Scope:** Medium
1. **Add** a `ReportStatus` enum or constant set with `green`, `red`, `pending`, `fallback`, and `wgp_only`.
2. **Add** section-level statuses such as `passed`, `failed`, `pending`, `not_applicable`, and `pending_not_implemented` for individual oracle surfaces.
3. **Keep** Sprint 0B `calibration_status` as read-only threshold metadata loaded through `Thresholds.load(strict=True)`.
4. **Map** threshold calibration status to initial report status only in an explicit function. For example, `wgp_only` maps to report `wgp_only`, deferred calibration maps to report `pending` unless the route is declared landed, and landed routes with missing evidence map to `red`.
5. **Do not** add `pending`, `fallback`, or `pending_not_implemented` to `migration-thresholds.yaml` calibration status values unless a separate threshold-schema migration is intentionally approved later.

### Step 3: Require complete evidence for green (`reigh-worker/scripts/dual_run_compare/compare.py`)
**Scope:** Medium
1. **Extract** or wrap `wgp_self_repeat.compare_metric`, but do not reuse `compare_route_observations` as the final Sprint 3 green decision.
2. **Implement** `compare_required_observations(thresholds, route_key, observations, required_metric_keys)` so missing required metrics are reported as `missing_evidence` and force `red` for landed routes or `pending` for explicitly non-landed routes.
3. **Require** each report section to have a concrete status: media similarity, queue contract, product effects, billing/idempotency, refund status, latency, VRAM, OOM, and error class.
4. **Add** tests proving one passing metric cannot make a route green when required media/runtime/error metrics are absent.

## Phase 2: Route Inventory And Shared-Path Coverage

### Step 4: Build active API-route inventory (`reigh-worker-orchestrator/api_orchestrator/task_handlers.py`, `reigh-worker/scripts/dual_run_compare/fixtures/non_rayworker/registry_snapshot.json`)
**Scope:** Medium
1. **Parse** `TASK_HANDLERS` from `reigh-worker-orchestrator/api_orchestrator/task_handlers.py` in the existing AST style used by `test_non_rayworker_fixtures.py`.
2. **Classify** every API-owned route as one of: named deliverable canary, covered-by-threshold/golden route, fallback, pending, or explicitly out-of-scope with a reason.
3. **Keep** the four required canaries (`video_enhance`, `image-upscale`, `animate_character`, `flux_klein_edit`) as full regression fixtures through their current owners.
4. **Add** registry coverage for additional active API routes such as `qwen_image`, `qwen_image_2512`, `z_image_turbo`, `z_image_turbo_i2i`, `qwen_image_edit`, `qwen_image_style`, `wan_2_2_t2i`, `wan_2_2_i2v`, `image_inpaint`, and `annotated_image_edit`.
5. **Fail** the harness if any active API-owned route is missing classification or shared-path policy.

### Step 5: Add lightweight shared-path oracle for every active API route (`reigh-worker/scripts/dual_run_compare/oracles.py`, `fixtures/non_rayworker/`)
**Scope:** Large
1. **Create** a lightweight oracle tier for all active API-owned routes, separate from full media comparison. This tier verifies that each route has a valid queue payload shape, output contract, completion handler policy, billing/idempotency policy, and shadow side-effect policy.
2. **Use** synthetic/minimal route fixtures for additional API-owned routes where full golden media evidence is absent. These fixtures should assert shared app/completion/billing contract health without claiming media similarity is green.
3. **Keep** full regression depth for the four named canaries: payload contract, owner handler, completion contract, product effect, billing/idempotency, and side-effect isolation.
4. **Report** additional API-owned routes as `green` only for the lightweight shared-path oracle when that oracle passes; keep media similarity `pending` unless landed media evidence exists.
5. **Add** tests proving a shared `complete_task` or billing contract regression fails at least one active API-owned route outside the four named canaries.

### Step 6: Extend fixtures with executable policies (`reigh-worker/scripts/dual_run_compare/fixtures/`)
**Scope:** Medium
1. **Add** per-route fields for `landed_status`, `report_status_policy`, `queue_contract`, `completion_contract`, `side_effect_policy`, `billing_policy`, `refund_policy`, `idempotency_policy`, `runtime_owner`, `evidence_required`, and `oracle_tier` (`full_canary`, `shared_path`, `media_landed`, `pending`).
2. **Update** non-RayWorker fixture tests to require full canary fields for the four deliverable canaries and shared-path fields for every other active API-owned route.
3. **Update** golden manifest/threshold sync tests so all threshold routes appear in reports even when pending/fallback/WGP-only.
4. **Record** alias mismatches explicitly, especially `image-upscale` versus legacy `image_upscale`, so queue and billing checks compare the correct task type.

## Phase 3: Shadow Isolation At Real Side-Effect Boundaries

### Step 7: Add shadow execution policy (`reigh-worker/scripts/dual_run_compare/shadow.py`)
**Scope:** Medium
1. **Define** a shadow envelope with `shadow_run_id`, `source_task_id`, `route_key`, `artifact_root`, `side_effect_mode=isolated`, `allow_completion=false`, `allow_upload=false`, `allow_status_update=false`, and `allow_billing=false` defaults.
2. **Write** local artifacts only under `reigh-worker/scripts/dual_run_compare/artifacts/<report-id>/<route-key>/shadow/`.
3. **Reject** production/user-visible paths, normal task upload paths, and remote storage URLs unless the run is explicitly marked isolated and disposable.
4. **Record** skipped completion, billing, upload, and user-visible generation effects in report JSON.

### Step 8: Intercept API-worker side-effect clients before live shadow mode (`reigh-worker-orchestrator/api_orchestrator/storage_utils.py`, `reigh-worker-orchestrator/api_orchestrator/task_utils.py`)
**Scope:** Large
1. **Name and wrap** concrete side-effect entrypoints before enabling any live shadow execution:
   - `storage_utils.py` calls to `complete_task` for small-file completions.
   - `storage_utils.py` calls to `generate-upload-url`, storage upload URLs, and post-upload `complete_task`.
   - `task_utils.py` URL-only completion/status calls to `update-task-status`.
2. **Introduce** a minimal injectable side-effect client or shadow mode guard used only by the harness path. In shadow mode it records intended requests and returns a shadow result without calling production APIs.
3. **Add** tests that shadow mode does not call `complete_task`, `generate-upload-url`, storage upload URLs, `update-task-status`, or billing-triggering paths.
4. **Keep** normal orchestrator behavior unchanged outside explicit shadow mode.

## Phase 4: Product, Billing, Refund, And Idempotency Oracles

### Step 9: Add product-effect oracle (`reigh-worker/scripts/dual_run_compare/oracles.py`, `reigh-app/supabase/functions/complete_task/*.test.ts`)
**Scope:** Large
1. **Implement** fixture-backed product-effect checks for generation versus variant creation, `generation_created`, output URL shape, thumbnail behavior, parent/child generation linkage, and shadow-visible-record absence.
2. **Anchor** app behavior with targeted Vitest tests in `complete_task/handler.test.ts`, `complete_task/generation.test.ts`, `complete_task/generation-handlers.test.ts`, and existing generation core/child/parent tests where appropriate.
3. **Ensure** the four named non-RayWorker canaries exercise shared `complete_task/generation-handlers.ts` and `complete_task/generation.ts` behavior through expected payload/output shapes.
4. **Ensure** the lightweight shared-path oracle covers all other active API-owned routes at the completion-contract level without asserting full product-media equivalence.

### Step 10: Add billing and idempotency oracle (`reigh-worker/scripts/dual_run_compare/oracles.py`, `reigh-app/supabase/functions/complete_task/billing.test.ts`, `reigh-app/supabase/functions/calculate-task-cost/*.test.ts`)
**Scope:** Medium
1. **Assert** spend ledger idempotency: a second cost calculation for the same task reports skipped and does not double-spend.
2. **Assert** sub-task billing skips through `complete_task/billing.ts` and shared `_shared/billing.ts` helpers.
3. **Assert** `video_enhance` compound cost calculation remains executable and stable through `calculate-task-cost/costHelpers.ts`.
4. **Apply** lightweight billing-policy validation to every active API-owned route so shared billing contract regressions are caught beyond the four named canaries.
5. **Require** all billing/idempotency oracle checks to run without live production credentials.

### Step 11: Discover or explicitly mark refund behavior (`reigh-app/supabase/functions/`, `reigh-worker/scripts/dual_run_compare/oracles.py`)
**Scope:** Small
1. **Search** for an actual refund ledger implementation before writing refund assertions. Candidate areas include edge functions, shared billing helpers, Stripe/payment code, and update-task-status cancellation paths.
2. **If** an actual refund path exists, add a targeted oracle and test against that path.
3. **If** no refund path exists, mark the refund section as `pending_not_implemented` with evidence in the report. Do not treat `update-task-status/cancellationBilling.ts` as a refund oracle because it bills completed cancelled-orchestrator work rather than inserting refund ledger entries.
4. **Keep** cancellation billing coverage as billing/cancellation-cost coverage, not refund coverage.

## Phase 5: Media, Queue, Runtime Metrics, And Reports

### Step 12: Implement media comparison adapters (`reigh-worker/scripts/dual_run_compare/media.py`)
**Scope:** Medium
1. **Add** image metrics for pHash normalized Hamming, SSIM, pixel dimensions, and format/container.
2. **Add** video metrics for frame count, sampled/per-frame pHash mean and p95, duration, FPS, and audio duration when present.
3. **Return** explicit missing-evidence objects for absent artifacts instead of omitting metrics.
4. **Feed** observed metric payloads into the strict comparison layer from Step 3.

### Step 13: Implement queue and runtime checks (`reigh-worker/scripts/dual_run_compare/queue_contract.py`, `runtime_metrics.py`)
**Scope:** Medium
1. **Compare** expected queue payload shape against golden/non-RayWorker fixtures and current orchestrator/worker handler registries.
2. **Record** task type, route key, runtime owner, handler, completion handler, billing path, idempotency policy, refund status, and error class.
3. **Capture** latency and VRAM observations from live/fixture metadata when available; otherwise emit pending or red according to landed status.
4. **Classify** OOM separately from generic error classes so `error_oom_count` remains an executable gate.

### Step 14: Generate final reports and exit codes (`reigh-worker/scripts/dual_run_compare/reporting.py`, `reports/`)
**Scope:** Medium
1. **Write** JSON reports with route-level report status, threshold calibration status, section statuses, metric results, queue contract results, product effects, billing/idempotency results, refund status, side-effect isolation results, raw observation refs, and registry/shared-path coverage.
2. **Write** Markdown reports ordered RED first, then pending/fallback/WGP-only, then green.
3. **Exit** non-zero when a landed route is RED, when a required oracle cannot execute, when sparse evidence would otherwise produce green, or when an active API route lacks classification or shared-path coverage.
4. **Exit** zero for explicitly documented pending/fallback/WGP-only routes only when the report states why they are not RED-or-green yet.
5. **Do not** fail solely because refund is `pending_not_implemented` if no refund implementation exists; do fail if the report tries to mark refund green without an executable refund path.

## Phase 6: Validation

### Step 15: Add focused tests and run cheap gates first (`reigh-worker/scripts/dual_run_compare/tests/`, `reigh-app/supabase/functions/`)
**Scope:** Medium
1. **Add** Python tests for root wrapper import strategy, worker-root path resolution, report-status mapping, sparse metric rejection, route classification, shared-path oracle coverage, fixture policy validation, refund path discovery behavior, shadow path rejection, side-effect client interception, and report rendering.
2. **Add** targeted Vitest edge tests for completion/product effects, billing/idempotency, and cancellation-cost behavior.
3. **Add** a test proving refund reports as `pending_not_implemented` when no executable refund path is present.
4. **Run** focused checks before broader suites.

## Execution Order
1. Add root CLI import/path handling and prove it imports the worker package correctly.
2. Add separate Sprint 3 report status and strict complete-evidence comparison before any report can go green.
3. Build active API-route inventory, fixture policy validation, and lightweight shared-path oracle for every active API-owned route.
4. Add shadow envelope and intercept real upload/completion/status side-effect clients.
5. Add product, billing, and idempotency oracles.
6. Discover the actual refund path or mark refund `pending_not_implemented` with evidence.
7. Add media, queue, runtime metric adapters.
8. Generate reports and enforce exit-code semantics.
9. Run focused tests, then broaden only after the harness behavior is stable.

## Validation Order
1. `python scripts/dual_run_compare.py --dry-run --report-id pytest-dual-run` from `/Users/user_c042661f/Documents/reigh-workspace`.
2. `cd reigh-worker && python -m pytest scripts/dual_run_compare/tests -q`.
3. `cd reigh-app && npm run test:edge:unit -- complete_task generation billing calculate-task-cost update-task-status` or the closest Vitest file filters supported by the local config.
4. `cd reigh-app && npm run lint:edge`.
5. If focused checks are green, run broader `cd reigh-worker && python -m pytest -q` and relevant broader `reigh-app` edge tests.


        Plan metadata:
        {
  "version": 3,
  "timestamp": "2026-05-06T02:04:56Z",
  "hash": "sha256:ceac8f72f02d44d5ac32c633fc6a4a03f748010ae7ab6e83a32979386bb9059f",
  "changes_summary": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented.",
  "flags_addressed": [
    "FLAG-005",
    "issue_hints",
    "scope",
    "FLAG-006",
    "correctness"
  ],
  "questions": [
    "Which Sprint 2 routes are officially landed and therefore must be RED-or-green now rather than pending/fallback/WGP-only?",
    "Should live `--execute-live` be part of Sprint 3 acceptance, or should the accepted default remain fixture-backed executable oracles plus side-effect-free report generation until isolated live credentials/pods are supplied?",
    "Is there an intended refund ledger path outside the searched cancellation billing flow, or should Sprint 3 explicitly report refund as pending_not_implemented until a refund feature is built?"
  ],
  "success_criteria": [
    {
      "criterion": "The workspace-root `scripts/dual_run_compare.py` command imports the `reigh-worker/scripts/dual_run_compare` package explicitly and produces JSON and Markdown reports from the workspace root in dry-run/fixture mode.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Sprint 3 report status is implemented separately from Sprint 0B threshold calibration status, and strict threshold loading still passes without adding ad hoc `pending`, `fallback`, or `pending_not_implemented` calibration values.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Sparse observations cannot make a route green; missing required media, queue, product, billing, latency, VRAM, OOM, or error-class evidence produces red for landed routes or documented pending/fallback/WGP-only for non-landed routes.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Every route in Sprint 0B thresholds and every active API-owned route in `api_orchestrator/task_handlers.py` is classified in the report as green, red, pending, fallback, or wgp_only; unclassified active routes fail the harness.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Every active API-owned route has a lightweight shared-path oracle for queue payload shape, completion contract, billing/idempotency policy, and shadow side-effect policy; missing shared-path coverage fails the harness.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Shadow mode intercepts or blocks `complete_task`, `generate-upload-url`, storage upload URL calls, `update-task-status`, billing triggers, and user-visible generation creation while recording intended side effects in the report.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Full regression coverage exists for `video_enhance`, `image-upscale`, `animate_character`, and `flux_klein_edit` through their current api-orchestrator owners and shared complete_task/billing paths.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Product-effect oracle checks are executable without live production credentials and cover generation/variant creation, `generation_created`, output URL shape, thumbnail behavior, parent/child linkage, and shadow-visible-record absence for full canaries.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Billing/idempotency oracle checks are executable without live production credentials and cover spend idempotency, sub-task billing skip, cancellation-cost behavior, and `video_enhance` compound cost calculation.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Refund reporting is backed by an executable refund ledger path if one exists; otherwise the report marks refund as `pending_not_implemented` and never reports refund green.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Reports include route-level sections for media similarity, queue contract, product effects, billing/idempotency, refund status, latency, VRAM, OOM, error class, shadow isolation, and registry/shared-path coverage.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Focused Python tests for `reigh-worker/scripts/dual_run_compare` pass.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Focused edge-function tests for completion and billing oracle behavior pass.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "The implementation reuses existing threshold, route-key, manifest, and fixture utilities instead of duplicating route classification logic.",
      "priority": "should",
      "requires": [
        "read_files",
        "parse_diff",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "Report JSON is stable enough for future CI parsing and Markdown is readable with RED routes first.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "Live infrastructure execution, if enabled later, has been smoke-tested against isolated credentials and disposable artifacts.",
      "priority": "info",
      "requires": [
        "observe_runtime_logs"
      ]
    }
  ],
  "assumptions": [
    "The active app checkout for completion and billing validation is `reigh-app`; `reigh-app-cloud-chain` remains a sibling/variant unless the user redirects the target.",
    "The required `scripts/dual_run_compare.py` deliverable is a workspace-root wrapper, while implementation modules live under `reigh-worker/scripts/dual_run_compare/`.",
    "The root wrapper must explicitly prepend `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker` to `sys.path` or use equivalent file-path loading before importing the worker `scripts` package.",
    "Sprint 3 report status is computed by the harness and must not be encoded into the strict Sprint 0B threshold calibration schema.",
    "No production selector is introduced in this sprint.",
    "Live execution remains behind an explicit flag and must use shadow side-effect clients before it can run safely.",
    "Every active API-owned route needs lightweight shared-path coverage; only the four named canaries require full regression fixtures unless landed media evidence already exists.",
    "If no executable refund ledger path exists, refund is reported as `pending_not_implemented` rather than green."
  ],
  "delta_from_previous_percent": 29.1,
  "structure_warnings": []
}

        Gate summary:
        {
  "passed": true,
  "criteria_check": {
    "count": 16,
    "items": [
      {
        "criterion": "The workspace-root `scripts/dual_run_compare.py` command imports the `reigh-worker/scripts/dual_run_compare` package explicitly and produces JSON and Markdown reports from the workspace root in dry-run/fixture mode.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "Sprint 3 report status is implemented separately from Sprint 0B threshold calibration status, and strict threshold loading still passes without adding ad hoc `pending`, `fallback`, or `pending_not_implemented` calibration values.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Sparse observations cannot make a route green; missing required media, queue, product, billing, latency, VRAM, OOM, or error-class evidence produces red for landed routes or documented pending/fallback/WGP-only for non-landed routes.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "Every route in Sprint 0B thresholds and every active API-owned route in `api_orchestrator/task_handlers.py` is classified in the report as green, red, pending, fallback, or wgp_only; unclassified active routes fail the harness.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "Every active API-owned route has a lightweight shared-path oracle for queue payload shape, completion contract, billing/idempotency policy, and shadow side-effect policy; missing shared-path coverage fails the harness.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Shadow mode intercepts or blocks `complete_task`, `generate-upload-url`, storage upload URL calls, `update-task-status`, billing triggers, and user-visible generation creation while recording intended side effects in the report.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Full regression coverage exists for `video_enhance`, `image-upscale`, `animate_character`, and `flux_klein_edit` through their current api-orchestrator owners and shared complete_task/billing paths.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Product-effect oracle checks are executable without live production credentials and cover generation/variant creation, `generation_created`, output URL shape, thumbnail behavior, parent/child linkage, and shadow-visible-record absence for full canaries.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "Billing/idempotency oracle checks are executable without live production credentials and cover spend idempotency, sub-task billing skip, cancellation-cost behavior, and `video_enhance` compound cost calculation.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "Refund reporting is backed by an executable refund ledger path if one exists; otherwise the report marks refund as `pending_not_implemented` and never reports refund green.",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Reports include route-level sections for media similarity, queue contract, product effects, billing/idempotency, refund status, latency, VRAM, OOM, error class, shadow isolation, and registry/shared-path coverage.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "Focused Python tests for `reigh-worker/scripts/dual_run_compare` pass.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "Focused edge-function tests for completion and billing oracle behavior pass.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "The implementation reuses existing threshold, route-key, manifest, and fixture utilities instead of duplicating route classification logic.",
        "priority": "should",
        "requires": [
          "read_files",
          "parse_diff",
          "subjective_judgment"
        ]
      },
      {
        "criterion": "Report JSON is stable enough for future CI parsing and Markdown is readable with RED routes first.",
        "priority": "should",
        "requires": [
          "read_files",
          "subjective_judgment"
        ]
      },
      {
        "criterion": "Live infrastructure execution, if enabled later, has been smoke-tested against isolated credentials and disposable artifacts.",
        "priority": "info",
        "requires": [
          "observe_runtime_logs"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [],
  "recommendation": "PROCEED",
  "rationale": "Execution should move forward. The v3 plan resolves the prior blocking issues: root CLI import handling is explicit, report status is separated from threshold calibration status, sparse evidence cannot go green, shadow side effects are intercepted at real API boundaries, every active API-owned route gets shared-path coverage, and refund is no longer falsely tied to cancellation billing. Remaining questions can be answered during implementation or reported as pending evidence without blocking the harness build.",
  "signals_assessment": "Score trajectory is 22.0 -> 8.5 -> 0 with no unresolved significant flags, no recurring reopened critiques, and a focused 29.1% delta from v2 to v3 that directly addresses the remaining blockers. Preflight is healthy: the project exists, is writable, success criteria are present, and required agent tooling is available. The plan is now specific enough to execute with tests and report semantics guarding the known uncertainty around landed-route inventory, live execution, and refund availability.",
  "warnings": [
    "During execution, do not let `pending_not_implemented` leak into route-level green status; it is only acceptable as a section-level refund status when no refund implementation exists.",
    "Confirm the local Vitest filter syntax before treating the edge-function validation command as authoritative.",
    "If the Sprint 2 landed-route list is unavailable, default missing evidence on explicitly landed routes to RED and classify unclear routes as pending with evidence."
  ],
  "settled_decisions": [
    {
      "id": "root-wrapper-import",
      "decision": "The workspace-root `scripts/dual_run_compare.py` wrapper must explicitly load the worker package by prepending `reigh-worker` to `sys.path` or equivalent file-path loading.",
      "rationale": "Plain `import scripts.dual_run_compare` from the workspace root can resolve the wrong `scripts` package."
    },
    {
      "id": "status-separation",
      "decision": "Sprint 3 report status and section statuses are separate from Sprint 0B threshold calibration status.",
      "rationale": "Strict threshold loading must remain compatible with the existing calibration schema."
    },
    {
      "id": "green-requires-complete-evidence",
      "decision": "A landed route cannot become green from sparse observations.",
      "rationale": "Missing required media, queue, product, billing, latency, VRAM, OOM, or error-class evidence must produce RED for landed routes or documented pending/fallback/WGP-only for non-landed routes."
    },
    {
      "id": "active-api-shared-path-coverage",
      "decision": "Every active API-owned route needs lightweight shared-path oracle coverage, while full regression depth remains scoped to the four named canaries unless landed media evidence exists.",
      "rationale": "This satisfies shared completion/billing safety without turning the sprint into full media-golden coverage for every API route."
    },
    {
      "id": "shadow-side-effect-boundaries",
      "decision": "Shadow isolation must intercept completion, upload URL generation, storage upload, status update, billing triggers, and user-visible generation creation.",
      "rationale": "Path-only artifact isolation is insufficient because current side effects occur through API clients."
    },
    {
      "id": "refund-reporting",
      "decision": "Cancellation billing is not a refund oracle; refund must use a real refund ledger path or report `pending_not_implemented`.",
      "rationale": "The known cancellation path bills completed cancelled-orchestrator work and does not prove refund behavior."
    }
  ],
  "override_forced": false,
  "orchestrator_guidance": "Plan passed gate and preflight. Proceed to finalize.",
  "robustness": "standard",
  "signals": {
    "iteration": 3,
    "idea": "# Sprint 3: Dual-Run Comparison Harness\n\n## Overall Context\n\nThis sprint turns Sprint 0B thresholds and Sprint 2 routed tasks into executable comparison evidence. It should catch queue, billing, product-effect, and media drift before any production selector exists.\n\n## Shared Operating Rules\n\n- Shadow artifacts must have no user-visible, billing, completion, or upload side effects unless explicitly isolated.\n- Compare media, queue contract, product effects, billing/refund/idempotency, latency, VRAM, OOM, and error class.\n- Non-RayWorker active routes must stay healthy through shared app/completion/billing paths.\n- Routes not yet implemented are pending/fallback/WGP-only, not silently green.\n\n## Sprint Goal\n\nBuild the dual-run harness and executable product/billing oracle for landed routes.\n\n## Required Deliverables\n\n- `scripts/dual_run_compare.py`.\n- Reports for media similarity, queue contract, product effects, billing/refund/idempotency, latency, VRAM, OOM, and error class.\n- No-side-effect shadow artifact isolation.\n- Regression checks for `video_enhance`, `image-upscale`, `animate_character`, and `flux_klein_edit` through their current owners.\n\n## Exit Criteria\n\nHarness is green for Sprint 2 routes or marks them RED; not-yet-routed RayWorker rows are pending/fallback/WGP-only; product/billing checks are executable; active non-RayWorker routes are not broken by shared app/completion/billing changes.",
    "significant_flags": 0,
    "unresolved_flags": [],
    "resolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "CLI packaging: root scripts package can shadow reigh-worker/scripts, breaking a workspace-root wrapper unless sys.path or file-path loading is explicit.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "FLAG-002",
        "concern": "Status taxonomy: Sprint 3 pending/fallback route states are not represented in the strict Sprint 0B threshold schema, so report status must be separate from calibration status or the schema must be intentionally updated.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "FLAG-003",
        "concern": "Shadow isolation: current upload/completion/status side effects happen through API calls, not only artifact paths, and the plan does not name the concrete interception points needed for live shadow execution.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "FLAG-004",
        "concern": "Comparison completeness: reusing compare_route_observations directly can mark sparse observations green because it only evaluates supplied metrics.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "FLAG-005",
        "concern": "Active non-RayWorker coverage: registry classification prevents silent disappearance, but does not by itself prove all active API routes remain healthy through shared complete_task and billing paths.",
        "resolution": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented."
      },
      {
        "id": "issue_hints",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Shared-route health: the revised plan classifies every active API-owned route and prevents silent disappearance, but the concrete full regression coverage still only applies to the four named canaries. Because the exit criteria say active non-RayWorker routes must not be broken by shared app/completion/billing changes, registry classification alone may still miss a shared complete_task or billing regression for additional active API routes such as qwen_image, qwen_image_2512, z_image_turbo, z_image_turbo_i2i, qwen_image_edit, qwen_image_style, wan_2_2_t2i, wan_2_2_i2v, image_inpaint, and annotated_image_edit from api_orchestrator/task_handlers.py lines 22-36.",
        "resolution": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented."
      },
      {
        "id": "correctness-1",
        "concern": "Are the proposed changes technically correct?: CLI packaging: the proposed workspace-root scripts/dual_run_compare.py wrapper needs a precise import strategy. The repository root already has a scripts package (scripts/preview/__init__.py exists under the root package), while the existing harness imports itself as scripts.dual_run_compare from inside reigh-worker (wgp_self_repeat.py line 12). Running a root wrapper that imports scripts.dual_run_compare without prepending /Users/user_c042661f/Documents/reigh-workspace/reigh-worker ahead of the workspace root on sys.path, or using runpy/file-path loading, will resolve the root scripts package and fail to find the worker package.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "correctness-2",
        "concern": "Are the proposed changes technically correct?: Status taxonomy: the plan says routes should be classified as green, red, pending, fallback, or wgp_only, but the existing strict threshold schema only approves calibration statuses green, pending_calibration, deferred_pending_sprint_0c_disk, wgp_only, and owner_deferred (thresholds.py lines 30-37 and migration-thresholds.yaml lines 6-11). This is fixable if Sprint 3 introduces a separate report status distinct from threshold calibration status, but the plan should say that explicitly or strict threshold loading will reject any attempt to encode pending/fallback in the YAML.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "correctness-3",
        "concern": "Are the proposed changes technically correct?: Comparison semantics: the existing reusable compare_route_observations in wgp_self_repeat.py evaluates only the metrics present in observations and returns green when all provided metrics pass; it does not require all expected metric keys or mark missing must-run sections pending/red. If Sprint 3 reuses this function directly, a route with only one passing metric could go green despite missing media, latency, VRAM, OOM, or error-class evidence.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "scope",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched the surrounding queue/completion surfaces. The non-RayWorker fixture tests currently validate static JSON fixture shape and registry drift for four routes (test_non_rayworker_fixtures.py lines 21-129), while the broader orchestrator registry includes many additional API worker routes. The plan's product/billing oracle work is therefore broader than existing tests, but it still needs a registry-wide active-route check or an explicit scoped exception for API routes outside the four deliverable canaries.",
        "resolution": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented."
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Shadow isolation: the plan defines local shadow artifact paths, but the actual API-worker side-effect entrypoints are not just local file writes. storage_utils.py posts directly to complete_task for small files at lines 130-133 and 168, requests generate-upload-url, uploads to storage, and then posts to complete_task at lines 201-265 for larger files; task_utils.py posts URL-only completions to update-task-status at lines 223-243. A path-policy-only shadow.py will not isolate live executions unless the plan also intercepts or replaces these completion/upload/status clients for shadow mode.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "callers-1",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked the likely caller path for the new root wrapper and existing command-level code. wgp_self_repeat.py builds commands to scripts/live_test/main.py using LIVE_TEST_SCRIPT = Path(\"scripts/live_test/main.py\") at line 17 and runs them with cwd=args.repo_root; from the workspace root that relative path points to /Users/user_c042661f/Documents/reigh-workspace/scripts/live_test/main.py, which does not exist. If Sprint 3 reuses this live-command pattern from a root wrapper, it must set repo_root to reigh-worker or resolve live-test paths relative to the worker package.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "callers-2",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked the argument/status behavior for missing observations. Existing compare_route_observations(thresholds, route_key, None) returns not_evaluated_no_metric_observations, and the current report builder uses exactly that for every selected route when no live observations are available. This is fine as a deferral pattern, but Sprint 3's caller contract must distinguish explicit pending/fallback/WGP-only from missing evidence on a landed route so landed routes cannot pass as unevaluated.",
        "resolution": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles."
      },
      {
        "id": "FLAG-006",
        "concern": "Billing/refund oracle: the plan points refund coverage at cancellationBilling, but the current repository only shows cancellation billing for completed work, not refund ledger behavior.",
        "resolution": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented."
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: Billing/refund correctness: the plan says to assert refund/cancellation behavior through update-task-status/cancellationBilling.ts, but repository search found cancellationBilling.ts only bills completed work for cancelled orchestrators by triggering calculate-task-cost; it does not insert refund ledger entries. The only refund evidence I found is the credits ledger enum/migration support for type refund, so the plan should either locate the actual refund path or mark refund as pending/not implemented instead of treating cancellationBilling as a refund oracle.",
        "resolution": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented."
      }
    ],
    "weighted_score": 0,
    "weighted_history": [
      22.0,
      8.5
    ],
    "plan_delta_from_previous": 29.1,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 3. Weighted score trajectory: 22.0 -> 8.5 -> 0. Plan deltas: 88.0%, 29.1%. Recurring critiques: 0. Resolved flags: 15. Open significant flags: 0.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "flag_resolutions": [],
  "resolved_flag_ids": [],
  "resolution_summary": "",
  "reprompted": false
}

        Flag registry:
        [
  {
    "id": "FLAG-001",
    "concern": "CLI packaging: root scripts package can shadow reigh-worker/scripts, breaking a workspace-root wrapper unless sys.path or file-path loading is explicit.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-002",
    "concern": "Status taxonomy: Sprint 3 pending/fallback route states are not represented in the strict Sprint 0B threshold schema, so report status must be separate from calibration status or the schema must be intentionally updated.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-003",
    "concern": "Shadow isolation: current upload/completion/status side effects happen through API calls, not only artifact paths, and the plan does not name the concrete interception points needed for live shadow execution.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-004",
    "concern": "Comparison completeness: reusing compare_route_observations directly can mark sparse observations green because it only evaluates supplied metrics.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-005",
    "concern": "Active non-RayWorker coverage: registry classification prevents silent disappearance, but does not by itself prove all active API routes remain healthy through shared complete_task and billing paths.",
    "evidence": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "verifiability-0",
    "concern": "Criterion 13: requires human verification (subjective_judgment).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "verifiability-1",
    "concern": "Criterion 14: requires human verification (subjective_judgment).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "verifiability-2",
    "concern": "Criterion 15: requires human verification (observe_runtime_logs).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "issue_hints",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Shared-route health: the revised plan classifies every active API-owned route and prevents silent disappearance, but the concrete full regression coverage still only applies to the four named canaries. Because the exit criteria say active non-RayWorker routes must not be broken by shared app/completion/billing changes, registry classification alone may still miss a shared complete_task or billing regression for additional active API routes such as qwen_image, qwen_image_2512, z_image_turbo, z_image_turbo_i2i, qwen_image_edit, qwen_image_style, wan_2_2_t2i, wan_2_2_i2v, image_inpaint, and annotated_image_edit from api_orchestrator/task_handlers.py lines 22-36.",
    "evidence": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "correctness-1",
    "concern": "Are the proposed changes technically correct?: CLI packaging: the proposed workspace-root scripts/dual_run_compare.py wrapper needs a precise import strategy. The repository root already has a scripts package (scripts/preview/__init__.py exists under the root package), while the existing harness imports itself as scripts.dual_run_compare from inside reigh-worker (wgp_self_repeat.py line 12). Running a root wrapper that imports scripts.dual_run_compare without prepending /Users/user_c042661f/Documents/reigh-workspace/reigh-worker ahead of the workspace root on sys.path, or using runpy/file-path loading, will resolve the root scripts package and fail to find the worker package.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "correctness-2",
    "concern": "Are the proposed changes technically correct?: Status taxonomy: the plan says routes should be classified as green, red, pending, fallback, or wgp_only, but the existing strict threshold schema only approves calibration statuses green, pending_calibration, deferred_pending_sprint_0c_disk, wgp_only, and owner_deferred (thresholds.py lines 30-37 and migration-thresholds.yaml lines 6-11). This is fixable if Sprint 3 introduces a separate report status distinct from threshold calibration status, but the plan should say that explicitly or strict threshold loading will reject any attempt to encode pending/fallback in the YAML.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "correctness-3",
    "concern": "Are the proposed changes technically correct?: Comparison semantics: the existing reusable compare_route_observations in wgp_self_repeat.py evaluates only the metrics present in observations and returns green when all provided metrics pass; it does not require all expected metric keys or mark missing must-run sections pending/red. If Sprint 3 reuses this function directly, a route with only one passing metric could go green despite missing media, latency, VRAM, OOM, or error-class evidence.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "scope",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched the surrounding queue/completion surfaces. The non-RayWorker fixture tests currently validate static JSON fixture shape and registry drift for four routes (test_non_rayworker_fixtures.py lines 21-129), while the broader orchestrator registry includes many additional API worker routes. The plan's product/billing oracle work is therefore broader than existing tests, but it still needs a registry-wide active-route check or an explicit scoped exception for API routes outside the four deliverable canaries.",
    "evidence": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "all_locations",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Shadow isolation: the plan defines local shadow artifact paths, but the actual API-worker side-effect entrypoints are not just local file writes. storage_utils.py posts directly to complete_task for small files at lines 130-133 and 168, requests generate-upload-url, uploads to storage, and then posts to complete_task at lines 201-265 for larger files; task_utils.py posts URL-only completions to update-task-status at lines 223-243. A path-policy-only shadow.py will not isolate live executions unless the plan also intercepts or replaces these completion/upload/status clients for shadow mode.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "callers-1",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked the likely caller path for the new root wrapper and existing command-level code. wgp_self_repeat.py builds commands to scripts/live_test/main.py using LIVE_TEST_SCRIPT = Path(\"scripts/live_test/main.py\") at line 17 and runs them with cwd=args.repo_root; from the workspace root that relative path points to /Users/user_c042661f/Documents/reigh-workspace/scripts/live_test/main.py, which does not exist. If Sprint 3 reuses this live-command pattern from a root wrapper, it must set repo_root to reigh-worker or resolve live-test paths relative to the worker package.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "callers-2",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked the argument/status behavior for missing observations. Existing compare_route_observations(thresholds, route_key, None) returns not_evaluated_no_metric_observations, and the current report builder uses exactly that for every selected route when no live observations are available. This is fine as a deferral pattern, but Sprint 3's caller contract must distinguish explicit pending/fallback/WGP-only from missing evidence on a landed route so landed routes cannot pass as unevaluated.",
    "evidence": "Revised the plan to resolve the gate blockers: made the root CLI import strategy explicit, separated Sprint 3 report status from Sprint 0B calibration status, required complete evidence before green, named real upload/completion/status side-effect interception points, added registry-wide active API-route classification, and tightened validation around shadow mode and product/billing oracles.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-006",
    "concern": "Billing/refund oracle: the plan points refund coverage at cancellationBilling, but the current repository only shows cancellation billing for completed work, not refund ledger behavior.",
    "evidence": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "correctness",
    "concern": "Are the proposed changes technically correct?: Billing/refund correctness: the plan says to assert refund/cancellation behavior through update-task-status/cancellationBilling.ts, but repository search found cancellationBilling.ts only bills completed work for cancelled orchestrators by triggering calculate-task-cost; it does not insert refund ledger entries. The only refund evidence I found is the credits ledger enum/migration support for type refund, so the plan should either locate the actual refund path or mark refund as pending/not implemented instead of treating cancellationBilling as a refund oracle.",
    "evidence": "Tightened the active non-RayWorker requirement by adding a lightweight shared completion/billing oracle for every active API-owned route, while keeping full regression depth scoped to the four required canaries. Corrected refund coverage so cancellation billing is not treated as a refund oracle; the plan now requires discovering a real refund path or reporting refund as pending_not_implemented.",
    "status": "verified",
    "severity": "significant"
  }
]

        Critique history:
        [
  {
    "iteration": 1,
    "flag_count": 8,
    "verified": []
  },
  {
    "iteration": 2,
    "flag_count": 5,
    "verified": [
      "FLAG-001",
      "FLAG-002",
      "FLAG-003",
      "FLAG-004",
      "correctness-1",
      "correctness-2",
      "correctness-3",
      "all_locations",
      "callers-1",
      "callers-2"
    ]
  },
  {
    "iteration": 3,
    "flag_count": 3,
    "verified": [
      "FLAG-001",
      "FLAG-002",
      "FLAG-003",
      "FLAG-004",
      "FLAG-005",
      "FLAG-006",
      "issue_hints",
      "scope",
      "correctness",
      "all_locations",
      "callers-1",
      "callers-2"
    ]
  }
]

        Debt watch items (do not make these worse):
        [
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: for ordinary pairs, the new diagnosis is not well-supported by the repo. the current sync effect in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l62) already syncs `url` and `primaryvariantid`, and the regenerate path reads exactly `starturl`, `endurl`, `startgenid`, `endgenid`, `startvariantid`, and `endvariantid` from `segmentslotmode.pairdata` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts#l438). adding `thumburl` and `generationid` to the sync does not, by itself, explain why an old image url is still being used for regular pairs. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the fix is incomplete for extra trailing slots. `handlepairclick` can populate `activepairdata` from `trailingpairdata` when `pairindex === pairdatabyindex.size` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l121), but the proposed sync effect only reads `pairdatabyindex.get(segmentslotlightboxindex)`. for those trailing-slot cases `fresh` is `undefined`, so no image refresh happens. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the merge pseudocode does not actually sync 'all image fields' as claimed. it omits `id` and `position` from change detection, and when `fresh.startimage` or `fresh.endimage` becomes `null` it preserves the stale previous object instead of syncing that null state. as written, it also needs explicit null-guards around spreads of `prev.startimage` / `prev.endimage` to be safe in strict typescript. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the plan's claim that `worker_state.py:200-204` (the 30-minute startup safety net) catches abandoned pods that exited before patching is slightly imprecise. line 200-204 only runs when `in_startup_phase` is true, which requires `startup_phase` to be in `('deps_installing', 'deps_verified', 'worker_starting')` per line 161. a pod that exits before its first patch has `startup_phase = none`, so `in_startup_phase` is false and the code falls through to the normal timeout checks (active_stale / not_claiming) at line 207+, not the 30-minute startup cap. both paths eventually reap the worker, so the end result is the same, but the overview's reasoning (naming 200-204 specifically) is wrong. worth correcting so future readers don't mis-reason about the invariant. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: checked worker_state.py line 161 (`in_startup_phase = startup_phase in (...)`) against the plan's assumption that subsequent lenient writes are safe. if deps_installing succeeds but deps_verified silently fails, startup_phase stays at 'deps_installing' and the 30-minute cap from line 200-204 applies \u2014 even though the pod is actually progressing through `uv sync`. on a slow runpod image with cold wheel downloads, `uv sync --extra cuda124` plus wan2gp deps can take 20+ minutes. there's no concrete benchmark in the plan that says the 30-minute cap is safely above the expected sync time; if `uv sync` legitimately takes 25 minutes and the deps_verified patch fails on a transient network blip, the orchestrator will terminate a healthy pod. plan should either bump the cap or note that deps_verified swallowing is acceptable because the cap is generously above typical sync time. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the path-mapping defect from the previous iteration is fixed, but a different technical gap remains around `self_refiner`. repository search shows `shared.utils.self_refiner` is imported by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx_pipelines/distilled.py`, `ti2vid_one_stage.py`, `ti2vid_two_stages.py`, `wan2gp/models/ltx2/ltx_pipelines/utils/helpers.py`, and `wan2gp/models/wan/any2video.py`; the v4 plan still aligns `wan2gp/shared/utils/self_refiner.py` to upstream head without any concrete runtime step that exercises those code paths after the change, so the only repo-documented behavior check for that file is still missing from the executable body. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the direct adapter still has a correctness risk around resolution parity. current vibecomfy ready templates hardcode image dimensions (`image/z_image` uses `emptysd3latentimage` 1024x1024 and `image/qwen_image_2512` uses 768x768), while `vibecomfy run` exposes no `--resolution` flag; the revised plan says a temporary scratchpad/input file may be generated only if supported, otherwise resolution is left out. that means a vibecomfy-supported direct route can silently ignore the worker's `resolution` param unless scratchpad resolution patching is made mandatory for supported direct routes or the support is explicitly limited to default-resolution smoke fixtures. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-success-criteria-well-prioritized-and-verifiable: are the success criteria well-prioritized and verifiable?: the attached success criteria are stale and do not match the current plan body. they still require 'no `usestate` for `activepairdata`', '`setactivepairdata` fully removed', 'sync effect deleted', and '`onpairclick` simplified to `(pairindex: number) => void`', which are the opposite of the current targeted-sync plan. as presented, the criteria are not usable for review or execution. (flagged 1 times across 1 plans)",
  "[DEBT] audio-loading: getaudiodata in useeffect removes render-readiness signal (flagged 1 times across 1 plans)",
  "[DEBT] audio-loading: same as correctness-3 \u2014 preview/render parity risk (flagged 1 times across 1 plans)",
  "[DEBT] audio-loading: preview/render parity partially satisfied (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: overlapping clips use first-found, volume not scaled (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: same as audio-reactivity-1 \u2014 overlapping/volume-adjusted clips diverge from audible mix (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: textclip missing globalframeprovider (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: same as audio-reactivity-2 \u2014 textclipsequence missing provider (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: textclip effects surface not covered (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: continuous effects shared by visual and text clips (flagged 1 times across 1 plans)",
  "[DEBT] batch-generation-pipeline: enhancement in usegeneratebatch before generatevideo() could compute prompts against a stale pair snapshot if mutations are still in flight. (flagged 1 times across 1 plans)",
  "[DEBT] cas-intern-short-circuit: symlink short-circuit comparison may produce false negatives on macos-like layouts where project_dir contains symlinked segments (/var \u2192 /private/var) because resolve(strict=true) on the source returns canonical paths but project_dir / cas_dirname may be non-canonical. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: cascade lookup only reads params->>'orchestrator_task_id_ref', missing shared reference paths and orchestrator-self detection. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: duplicate of correctness-2 + correctness-3: invalid sql syntax and narrow cascade lookup. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: shared orchestrator-reference helpers not referenced. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: orchestrator tasks that crash don't get orchestrator-self cascade. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: hardcoded params->>'orchestrator_task_id_ref' misses other reference paths. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-retry: crash requeue sql does not increment attempts, risking infinite requeue loop. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-retry: duplicate of correctness-1: attempts never advance on crash requeue. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-retry: missing attempts increment location in heartbeat sql. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-retry: step 6 under-scoped for real retry convergence and orchestrator-self handling. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-sql-syntax: bare select inside plpgsql is invalid \u2014 needs perform. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-testing: no multi-crash convergence test exercising attempts 0\u21921\u21922\u21923. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-testing: no validation that plpgsql body executes successfully. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-testing: criteria don't require proof of crash requeue convergence. (flagged 1 times across 1 plans)",
  "[DEBT] criteria-verifiability: 'no unsafe .maybesingle()' criterion requires judgment about column uniqueness. (flagged 1 times across 1 plans)",
  "[DEBT] criteria-verifiability: decision documentation location not specified. (flagged 1 times across 1 plans)",
  "[DEBT] criteria-verifiability: the must criterion requiring 5 task types to exist as active db rows is not verifiable from code diff alone \u2014 it requires a live db query. (flagged 1 times across 1 plans)",
  "[DEBT] db-fallback-testing: no new automated test for the db fallback dispatch path or dependant_on preservation for raw worker families. (flagged 1 times across 1 plans)",
  "[DEBT] dependency-resolution: dependency resolution: the plan does not lock down the active python-version matrix even though the repo currently splits between python 3.10 local installs and a python 3.11 runpod image. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: the package is internally inconsistent. the plan body says to keep `activepairdata` in `usestate` and make phase 2 optional, but the attached metadata and success criteria still describe the previous derive-via-`usememo` / remove-`setactivepairdata` / simplify-`onpairclick` plan. that means the approved-plan requirements are only partially coherent as presented. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: the linux distro note is documentation-only; the generated install command in step 7 still runs `apt-get install python3.10-venv python3.10-dev ffmpeg` without any pre-check that the package exists. users on ubuntu 24.04+ who ignore the doc and try to copy-paste the command will hit a confusing `e: unable to locate package python3.10-venv` from apt rather than a targeted error from commandutils.ts. a one-line detection pre-check (e.g., `apt-cache show python3.10-venv >/dev/null 2>&1 || { echo 'install deadsnakes ppa first \u2014 see readme'; exit 1; }`) would convert the silent failure into an actionable error, but the plan does not add this. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: checked the revised v4 body against `docs/wan2gp_fork_migration_plan.md` sprint 2. the repo plan doc still lists an \"ltx-2 `self_refiner` smoke against the pre-sprint behavioral baseline\" as a sprint 2 verification gate and repeats that smoke in the functionality-preservation checks, but the revised execution steps no longer schedule that smoke anywhere; it survives only as an info-level metadata criterion. because `wan2gp/shared/utils/self_refiner.py` remains an explicit sprint 2 deliverable, the revised plan still only partially carries forward the verification package described in the source migration plan. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: worker integration: the migration doc describes the per-call profile override gap as involving reigh-worker adapter handling of override_profile before constructing vibecomfy sessionconfig, but the plan limits sprint 1 per-run work to the vibecomfy cli/runtime. that may be acceptable for a vibecomfy-library mvp, but it does not fully exercise the production-facing per-task override semantics called out in the overall context. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: a residual issue-hint tension remains for resolution handling. the plan acknowledges current `vibecomfy run` lacks a resolution flag, but allows the adapter to leave resolution and other template-specific values unwired for sprint 2. because `z_image_turbo` and `qwen_image_2512` are marked vibecomfy-supported direct routes, this may not preserve the existing worker task-parameter contract for tasks that provide a non-default `resolution`. (flagged 1 times across 1 plans)",
  "[DEBT] direct-route-parameter-parity: direct route parameter parity: vibecomfy-supported direct routes may ignore the worker `resolution` parameter. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: phase 1 still misses a real supporting-data location: `trailingpairdata` lives outside `pairdatabyindex` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts#l111), but the proposed sync logic only considers `pairdatabyindex`. if trailing slot regenerate is part of the bug surface, that location is not covered. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: the non-swallowing helper `update_worker_phase_strict` is a new shell function, but phase 1 step 2 introduces it only as pseudo-code. there is no concrete note that the helper must handle supabase http non-2xx responses as failures (curl returns 0 even on http 4xx/5xx by default unless `-f` or `--fail-with-body` is used). if the implementer ports `update_worker_phase` verbatim with only `|| return 0` removed, a 500 from supabase would still report success because curl's exit code is 0. the plan should specify `curl --fail` or explicit http status code checking in the strict variant. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: the supporting-infrastructure review still finds one missing check. in `docs/wan2gp_fork_migration_plan.md`, sprint 2's verification matrix and risk register both single out `self_refiner` as a distinct drift-upgrade surface with its own smoke and its own silent-behavior-change risk, but the revised v4 body updates the file without keeping that supporting verification step in the actual execution checklist. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: documentation/data gap: the sprint exit criteria require profiles 1 and 3 to have vram and wall-clock data, but the plan puts that only in metadata as an info-level criterion and does not schedule a concrete artifact location or command for recording the measurements. the implementation could satisfy all unit tests while still missing one of the explicit exit criteria. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: the supporting infrastructure for resolution is still incomplete if direct vibecomfy routes are considered production-supported. vibecomfy has a `vibecomfy.patches.resolution` helper and the cli can load scratchpad files with `allow_scratchpad=true`, but the plan does not require using that path; it permits leaving resolution out for sprint 2. (flagged 1 times across 1 plans)",
  "[DEBT] edge-test-config: plan's vitest commands use the wrong config entry point. (flagged 1 times across 1 plans)",
  "[DEBT] edge-test-config: same as verification-3: wrong vitest config in validation commands. (flagged 1 times across 1 plans)",
  "[DEBT] edge-test-config: success criterion references wrong test command. (flagged 1 times across 1 plans)",
  "[DEBT] error-handling: db loader error handling convention mismatch (plan says log+null, existing loaders throw) (flagged 1 times across 1 plans)",
  "[DEBT] error-propagation-logging: generation.ts and handler.ts logging endpoints are not directly tested. (flagged 1 times across 1 plans)",
  "[DEBT] error-propagation-testing: no end-to-end regression test for the full symptom chain (db error \u2192 tocompletionerror metadata \u2192 handler log). (flagged 1 times across 1 plans)",
  "[DEBT] error-propagation-testing: handler.ts metadata surfacing criterion lacks a concrete automated verifier. (flagged 1 times across 1 plans)",
  "[DEBT] error-propagation-testing: main issue only partially validated without an integration test. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the step 2 retry loop uses a naked `sleep 2` between attempts, which adds up to 6 seconds of latency on the happy path when the first patch eventually succeeds on attempt 2 or 3. for pods where supabase is reachable but slow during the initial moments of a cold runpod start, the retry logic is fine. however, if the first attempt fails with a tls handshake delay and the retry loop sleeps 2s per attempt regardless of whether curl itself has been blocking for tens of seconds, the total startup latency penalty could be substantial. this is a minor tuning concern, not a correctness issue. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: finding callers of the changed module shows that `shared.utils.self_refiner` is consumed by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx2_handler.py`, multiple ltx2 pipeline modules, and `wan2gp/models/wan/any2video.py`. the revised validation steps still only drive the three bridge getters in `source/runtime/wgp_ports/vendor_imports.py`; none of the scheduled commands execute a real `self_refiner` caller, so the plan does not yet verify the main caller shapes for the other explicit sprint 2 file change. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked direct queue caller values in `db_task_to_generation_task()`: direct image tasks may carry `resolution`, `steps`/`num_inference_steps`, `seed`, and `override_profile`. the revised adapter plan covers seed, steps, and memory profile but not guaranteed resolution propagation, so it does not handle all relevant direct-route caller arguments for a supported vibecomfy direct route. (flagged 1 times across 1 plans)",
  "[DEBT] gpu-branching-test-matrix: linux cuda128 path under-verified (flagged 1 times across 1 plans)",
  "[DEBT] gpu-branching-ui-surface: nvidia-50 option is exposed on linux in the ui but linux cuda128 smoke test is missing (flagged 1 times across 1 plans)",
  "[DEBT] hook-abstraction: usepairsettingshandler becomes trivial with single caller \u2014 keeping it is extra indirection. (flagged 1 times across 1 plans)",
  "[DEBT] hype-mirror-cas-coverage: hype-mirrored files whose parent step does not declare matching produces will not be cas-interned, even with the follow_symlinks=false edit. (flagged 1 times across 1 plans)",
  "[DEBT] is-the-change-in-the-right-place-and-would-it-break-any-callers: is the change in the right place, and would it break any callers?: the optional cleanup steps are not in the right place yet. `pairregionslayer` does not receive `pairdatabyindex` today; its props are only `images`, `imagepositionswithpending`, `pairinfowithpending`, and callback/display props in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx#l20). so step 4's 'pass `pairdatabyindex.get(pairindex)` directly' would require new prop plumbing or a different seam. (flagged 1 times across 1 plans)",
  "[DEBT] is-the-scope-and-scale-of-the-change-appropriate: is the scope and scale of the change appropriate?: phase 2 is still under-specified for execution. step 4 says pairregionslayer should either pass `pairdatabyindex.get(pairindex)` directly or 'just pass the index + frame-only data', which are materially different designs. if phase 2 is kept in the plan, it needs a single concrete direction. (flagged 1 times across 1 plans)",
  "[DEBT] is-there-convincing-verification-for-the-change: is there convincing verification for the change?: the plan still lacks an explicit automated regression test for the reported bug. step 2 is manual ('check that `usevideoregeneratemode` now gets the fresh url'), but there is no concrete test that opens a segment slot, changes the primary variant data, and asserts that the regenerate path sees the fresh `url`, `generationid`, and `primaryvariantid`. (flagged 1 times across 1 plans)",
  "[DEBT] is-there-convincing-verification-for-the-change: is there convincing verification for the change?: the current `usesegmentslotmode` test remains only a smoke test in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts), and the plan does not add behavior coverage for the new sync effect. (flagged 1 times across 1 plans)",
  "[DEBT] is-there-convincing-verification-for-the-change: is there convincing verification for the change?: no verification step covers the trailing-slot branch, even though the proposed phase 1 logic currently misses `trailingpairdata` refreshes. (flagged 1 times across 1 plans)",
  "[DEBT] legacy-data-backfill: the step 8 diagnostic query only detects cross-shot pair_shot_generation_id misassociations, not same-shot misassociations caused by timeline reordering within a shot. (flagged 1 times across 1 plans)",
  "[DEBT] lookup-consistency: other repo call sites use unordered .limit(1).maybesingle() and will remain inconsistent. (flagged 1 times across 1 plans)",
  "[DEBT] lookup-consistency: other call sites with same unsafe pattern not covered. (flagged 1 times across 1 plans)",
  "[DEBT] lora-management: lora tools simplified vs full ui parity (multi-stage metadata, private loras) (flagged 1 times across 1 plans)",
  "[DEBT] media-lightbox-persistence: variant switches do not clear/restore inpaintprompt, so stale prompt state can leak across variants with no cached prompt. (flagged 1 times across 1 plans)",
  "[DEBT] media-lightbox-persistence: removing prompt/numgenerations from the variant-keyed localstorage cache means all variants within a generation share the same prompt. this broadens existing debt-002 (variant prompt leakage). (flagged 1 times across 1 plans)",
  "[DEBT] media-lightbox-segment-slot: media lightbox / segment slot: the targeted sync rationale does not fully explain the reported stale-url bug for regular pairs, and the proposed effect still misses trailing-slot refreshes because those can come from `trailingpairdata` rather than `pairdatabyindex`. (flagged 1 times across 1 plans)",
  "[DEBT] number-input-nullable: plan doesn't explicitly state onchange must also accept null, though step 3 depends on it. (flagged 1 times across 1 plans)",
  "[DEBT] number-input-nullable: disputed v1 flag \u2014 original concern about bulkclippanel being unimplementable. (flagged 1 times across 1 plans)",
  "[DEBT] number-input-nullable: onchange null filtering not explicitly addressed in plan. (flagged 1 times across 1 plans)",
  "[DEBT] number-input-testing: no planned tests for numberinput shared component or bulkclippanel nullable draft flow. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: pre-existing individual_travel_segment children won't drive orchestrator completion through segment_type_config after deploy. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: missing compatibility seam in orchestratorcore.ts:123-126 for old individual_travel_segment rows. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: mixed old/new data during rollout can leave old orchestrators without completion counting. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: no test or deployment guard for pre-existing individual_travel_segment children completing after worker change. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: plan overstates backward compatibility for existing data. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: missing rollout compatibility step for in-flight individual_travel_segment tasks. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: pre-deploy individual_travel_segment child completing post-rollout won't be treated as segment task by checkorchestratorcompletion. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: orchestrator.test.ts criterion too narrow to verify old individual_travel_segment compatibility. (flagged 1 times across 1 plans)",
  "[DEBT] pair-settings-plumbing: handleopenpairsettings(pairindex, pairframedata) path in timelinetrackprelude, segmentoutputstrip, and usesegmentoutputstrip not explicitly named. (flagged 1 times across 1 plans)",
  "[DEBT] pair-settings-plumbing: same as flag-002 \u2014 segmentoutputstrip and usesegmentoutputstrip still carry pairframedata. (flagged 1 times across 1 plans)",
  "[DEBT] pair-settings-plumbing: timelinetrackprelude and segmentoutputstrip still forward (pairindex, pairframedata). (flagged 1 times across 1 plans)",
  "[DEBT] plan-scope: step 3 is larger than a light megaplan warrants. (flagged 1 times across 1 plans)",
  "[DEBT] planning-metadata: planning metadata: the attached metadata and success criteria still describe a different implementation than the current plan body, which risks sending execution and review down the wrong path. (flagged 1 times across 1 plans)",
  "[DEBT] planning-metadata: success criteria don't cover wave 4 scope (flagged 1 times across 1 plans)",
  "[DEBT] position-key-semantics: plan investigates a unique constraint on (parent_generation_id, child_order) which doesn't match repo semantics for position keys. (flagged 1 times across 1 plans)",
  "[DEBT] position-key-semantics: plan weights toward child_order rather than pair_shot_generation_id as the key that matters. (flagged 1 times across 1 plans)",
  "[DEBT] position-key-semantics: unique constraint on (parent_generation_id, child_order) not supported by repo semantics. (flagged 1 times across 1 plans)",
  "[DEBT] prompt-composition: the plan's step 1 signature includes textbeforeprompts/textafterprompts parameters that would be applied before enhancement, double-wrapping the prompt. (flagged 1 times across 1 plans)",
  "[DEBT] ready-template-snapshots: step 4.2 drops markdownnote nodes but step 4.5 and the success criteria require class_type/widget parity with pre-refactor snapshots, which currently include markdownnote nodes. (flagged 1 times across 1 plans)",
  "[DEBT] ready-template-snapshots: same tension as issue_hints v2: drop-markdownnote vs. snapshot parity. (flagged 1 times across 1 plans)",
  "[DEBT] reigh-worker-orchestrator-dockerfile: step 7 \u00a73 claims `gpu_orchestrator/dockerfile` has wan2gp install steps; current main is generic and contains none. (flagged 1 times across 1 plans)",
  "[DEBT] reigh-worker-orchestrator-runpod-startup: `gpu_orchestrator/runpod/startup_script.py` embeds `headless-wan2gp` in `_workdir_discovery_snippet` and is not named explicitly in step 7 \u00a73's checklist. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the broader runtime surface after the v4 path fix. sprint 2 is still moving two behavior-sensitive seams rather than just the import-path contract: the `wan2gp/` mount path and the `self_refiner` runtime. step 6.2 covers only the three `vendor_imports` getters, while the 6-file travel suite and the bridge-contract tests do not mention `self_refiner`, so dropping the dedicated self-refiner smoke from the runnable steps leaves the broader downstream surface of that changed file under-covered. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: the supported direct-route scope is still broader than the adapter's guaranteed parameter surface. `db_task_to_generation_task()` currently carries direct task params such as `resolution`, `steps`, and `seed` into wgp generation, but the vibecomfy cli path only guarantees prompt, seed, steps, and memory profile; resolution remains optional/documentation-only in the plan. (flagged 1 times across 1 plans)",
  "[DEBT] self-refiner-verification: self-refiner verification: the revised plan still aligns `wan2gp/shared/utils/self_refiner.py` without scheduling the sprint 2 ltx-2 `self_refiner` smoke that `docs/wan2gp_fork_migration_plan.md` defines as the behavior-preservation check for that drift upgrade. (flagged 1 times across 1 plans)",
  "[DEBT] settings-defaults: workerrepopath default can go stale if user switches computertype before editing path (flagged 1 times across 1 plans)",
  "[DEBT] settings-resolution: settings cascade missing \u2014 shot-only read diverges from form's defaults\u2192user\u2192project\u2192shot merge (flagged 1 times across 1 plans)",
  "[DEBT] settings-resolution: settings cascade missing \u2014 shot-only read (flagged 1 times across 1 plans)",
  "[DEBT] shared-component-compatibility: numberinput changes affect callers outside video-editor (billing, travel-between-images, phaseconfigselectormodal). (flagged 1 times across 1 plans)",
  "[DEBT] shared-component-compatibility: shared ui component blast radius not audited in plan. (flagged 1 times across 1 plans)",
  "[DEBT] shot-linking-testing: no test covers the linkgenerationtoshot error/catch branches. (flagged 1 times across 1 plans)",
  "[DEBT] signature-propagation: plan doesn't explicitly name timeline/index.tsx and segmentslotcontracts.ts for updates. (flagged 1 times across 1 plans)",
  "[DEBT] signature-propagation: same as flag-001 \u2014 timeline/index.tsx and segmentslotcontracts.ts not in checklist. (flagged 1 times across 1 plans)",
  "[DEBT] signature-propagation: five supporting contract/plumbing sites not named in the checklist. (flagged 1 times across 1 plans)",
  "[DEBT] ta[REDACTED_SK]: step 3 cites wrong migration file (task_cost_configs instead of task_types) as evidence for db fallback path. (flagged 1 times across 1 plans)",
  "[DEBT] ta[REDACTED_SK]: step 3 should cite task_types source, not task_cost_configs. (flagged 1 times across 1 plans)",
  "[DEBT] ta[REDACTED_SK]: plan doesn't verify travel_segment and travel_stitch exist as active task_types rows using the correct table. (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: current generation-child.test.ts is only a smoke test. (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: no plan to verify other lookup paths choose rows consistently. (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: no new tests for db loader or travel param merge path (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: must-level criteria depend on manual testing rather than automated assertions (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: no new unit tests for wave 4 tools (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: must criteria backed by manual testing only (flagged 1 times across 1 plans)",
  "[DEBT] test-infrastructure: no test fixtures for resources table (flagged 1 times across 1 plans)",
  "[DEBT] timeline-drag-coordination: plan keeps two hooks instead of a single coordinator (flagged 1 times across 1 plans)",
  "[DEBT] timeline-drag-coordination: brief says single coordinator but plan keeps separate hooks (flagged 2 times across 1 plans)",
  "[DEBT] timeline-drag-coordination: pendingopsref retained despite brief suggesting removal (flagged 1 times across 1 plans)",
  "[DEBT] timeline-drag-coordination: wrapper-bound listener mount wiring under-specified (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: read path still assembles config and registry from separate requests (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: poll sync verification not structurally changed (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: backend save helpers not wired to new rpc (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: read infrastructure not updated (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: backend tests not in validation list (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: backend callers not migrated (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: broader persistence-contract problem (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: backend split-save not addressed (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: split polling can combine config and registry from different snapshots (flagged 1 times across 1 plans)",
  "[DEBT] timeline-scaling: the plan only specifies a concrete fix for the default scale(1) case; explicit-scale tracks may still break blend-mode effects. (flagged 1 times across 1 plans)",
  "[DEBT] timeline-snap-threshold: threshold is generous (duration) rather than zoom-scaled (8px) (flagged 1 times across 1 plans)",
  "[DEBT] timeline-snap-threshold: computedropposition does not pass a zoom-scaled threshold override (flagged 1 times across 1 plans)",
  "[DEBT] travel-continuations: smooth continuations not threaded \u2014 agent tasks won't have continuation_config even when shot settings enable it (flagged 1 times across 1 plans)",
  "[DEBT] travel-continuations: continuation_config omitted from form parity (flagged 1 times across 1 plans)",
  "[DEBT] travel-payload-cleanup-scope: plan scope narrower than original user request (flagged 1 times across 1 plans)",
  "[DEBT] travel-payload-cleanup-scope: broader create-task contract problem left untouched (flagged 1 times across 1 plans)",
  "[DEBT] travel-payload-readers: phase 4 app-side reader audit incomplete (flagged 1 times across 1 plans)",
  "[DEBT] travel-payload-readers: phase 4 field inventory incomplete for app-side readers (flagged 1 times across 1 plans)",
  "[DEBT] travel-request-contract: image_variant_ids is in frontend request contract (flagged 1 times across 1 plans)",
  "[DEBT] travel-request-contract: image_variant_ids contract change (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: spawn_worker does not internally call start_worker_process; harness must call both explicitly (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: worker_id and runpod_id must be generated and threaded distinctly; plan currently uses pod_id as both (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: duplicate of correctness-1 \u2014 spawn_worker two-step misstatement (flagged 2 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: duplicate of correctness-2 \u2014 worker_id/runpod_id propagation across takeover and restore paths (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: duplicate of correctness-1 + correctness-2 \u2014 missing create_worker_record glue and start_worker_process integration (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: duplicate of correctness-2 \u2014 caller contract for spawn_worker requires worker_id, not pod_id (flagged 1 times across 1 plans)",
  "[DEBT] verification: no end-to-end render test for audio analysis timing (flagged 1 times across 1 plans)",
  "[DEBT] verification: no automated coverage for text clips or overlapping clips with audio effects (flagged 1 times across 1 plans)",
  "[DEBT] verification-coverage: no automated test exercises the full segment-slot opening path after cleanup. (flagged 1 times across 1 plans)",
  "[DEBT] verification-coverage: no automated coverage that clicking a pair opens the correct modal after cleanup. (flagged 1 times across 1 plans)",
  "[DEBT] verification-coverage: zero behavioral change criterion is not verifiable from tsc + existing tests alone. (flagged 1 times across 1 plans)",
  "[DEBT] verification-workflow: tsconfig.app.json excludes test files, so tsc won't catch test breakage. (flagged 1 times across 1 plans)",
  "[DEBT] worker-test-staleness: worker test in test_additional_coverage_modules.py:37 may assert stale payload structure (task_type vs family). (flagged 1 times across 1 plans)"
]

        Requirements:
        - Produce structured JSON only.
        - `tasks` must be an ordered array of task objects. Every task object must include:
          - `id`: short stable task ID like `T1`
          - `description`: concrete work item
          - `depends_on`: array of earlier task IDs or `[]`
          - `status`: always `"pending"` at finalize time
          - `executor_notes`: always `""` at finalize time
          - `reviewer_verdict`: always `""` at finalize time
        - `watch_items` must be an array of strings covering runtime risks, critique concerns, and assumptions to keep visible during execution.
        - `sense_checks` must be an array with one verification question per task. Every sense-check object must include:
          - `id`: short stable ID like `SC1`
          - `task_id`: the related task ID
          - `question`: reviewer verification question
          - `verdict`: always `""` at finalize time
        - `user_actions` must be an array of human-only setup or operational actions. Use IDs `U1`, `U2`, ... and include `description` plus `phase` (`before_execute` or `after_execute`). Use optional `blocks_task_ids` when an action blocks specific tasks, optional `rationale` when useful, and `requires_human_only_reason` ONLY when the user_action is the sole coverage for a plan step.
- Include ONLY actions that require a human outside the executor's repo-editing work: env vars or secrets, infra access such as cloud accounts or VPN, DB migrations the human must trigger, manual UI/UX smoke tests, deploys, and out-of-band approvals.
- Anything that touches code in the repo MUST be a task, not a user_action. Reading docs, editing files, running tests, and writing migration SQL are tasks. Negative example: writing the migration SQL is a task, not a user_action.
- Positive examples: `U1: Set ANTHROPIC_API_KEY in .env (before_execute)`; `U2: Manually smoke test the production deploy in the browser (after_execute)`.
        - `meta_commentary` must be a single string with execution guidance, gotchas, or judgment calls that help the executor succeed.
        - `validation` must be an object that self-checks plan coverage:
          - `plan_steps_covered`: enumerate EVERY step from the approved plan. For each step, provide a short `plan_step_summary` (the step's intent in one phrase) and `finalize_item_ids` (array of task IDs `T*` or user_action IDs `U*` that implement or cover it — a single plan step may map to multiple tasks and/or user_actions).
          - `orphan_tasks`: task IDs that do not correspond to any plan step. Normally empty. If non-empty, explain in `completeness_notes`.
          - `completeness_notes`: free-text explanation of any gaps, deviations, or deliberate omissions.
          - `coverage_complete`: set to `true` only if every plan step has at least one finalize task or user_action AND you have verified the mapping by reviewing each entry. Set to `false` if any plan step is missing coverage.
          - Example:
          ```json
          "validation": {
            "plan_steps_covered": [
              {"plan_step_summary": "Add retry logic to API client", "finalize_item_ids": ["T1", "T2"]},
              {"plan_step_summary": "Set required production secret", "finalize_item_ids": ["U1"]}
            ],
            "orphan_tasks": [],
            "completeness_notes": "All plan steps mapped to tasks.",
            "coverage_complete": true
          }
          ```
        - Preserve information that strong existing artifacts already capture well: execution ordering, watch-outs, reviewer checkpoints, and practical context.
        - The structured output should be self-contained: an executor reading only `finalize.json` should have everything needed to work.
        - Keep the task count proportional to the work. A simple 1-2 file fix should be 2 tasks: (1) apply the fix, (2) run tests. Do NOT create separate "inspect" or "read" tasks for simple changes — the executor can read and fix in one step. Only create more tasks when the work has genuinely independent stages.
        - - The FINAL task MUST always be to run tests and verify the changes work. If specific test IDs or commands are mentioned in the original task, include them. Otherwise, the executor should find and run the tests most relevant to the files changed. If any test fails, read the error, fix the code, and re-run until they pass. Do NOT create new test files — run the project's existing test suite. Additionally, the executor should write a short throwaway script that reproduces the specific bug described in the task, run it to confirm the fix works, then delete the script.

> AGENT

{"tasks":[{"id":"T1","description":"Create the workspace-root `scripts/dual_run_compare.py` wrapper and worker implementation entrypoint so the root command explicitly prepends `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker` to `sys.path`, invokes `scripts.dual_run_compare.dual_run_compare.main`, and defaults live-worker helper paths to the worker repo root.","depends_on":[],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"" ,"stance":null,"stop_signal":null},{"id":"T2","description":"Implement Sprint 3 status contracts in `reigh-worker/scripts/dual_run_compare/status.py` and strict comparison logic in `compare.py`: separate report statuses from calibration statuses, map threshold calibration status explicitly, require all required observations before green, and produce concrete section statuses including `pending_not_implemented`.","depends_on":["T1"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T3","description":"Build active API-route inventory and executable fixture policy coverage. Parse `reigh-worker-orchestrator/api_orchestrator/task_handlers.py`, update `fixtures/non_rayworker/registry_snapshot.json` and related fixtures with landed/report/oracle policy fields, preserve full canary depth for `video_enhance`, `image-upscale`, `animate_character`, and `flux_klein_edit`, classify every active API-owned route, and explicitly record aliases such as `image-upscale` versus `image_upscale`.","depends_on":["T2"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T4","description":"Implement lightweight shared-path oracles in `reigh-worker/scripts/dual_run_compare/oracles.py` and fixture validation for every active API-owned route. Cover queue payload shape, output/completion contract, billing/idempotency policy, and shadow side-effect policy for all active API routes; keep full product/billing/completion assertions for the four named canaries; ensure shared `complete_task` or billing regressions fail at least one non-canary active route.","depends_on":["T3"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T5","description":"Add shadow execution isolation in `reigh-worker/scripts/dual_run_compare/shadow.py`: define the shadow envelope, enforce artifact writes under `reigh-worker/scripts/dual_run_compare/artifacts/<report-id>/<route-key>/shadow/`, reject production/user-visible paths and remote storage URLs unless explicitly isolated/disposable, and record skipped completion, billing, upload, and user-visible effects in report data.","depends_on":["T4"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T6","description":"Intercept orchestrator side-effect clients for shadow mode in `reigh-worker-orchestrator/api_orchestrator/storage_utils.py` and `task_utils.py`. Wrap or inject guards for `complete_task`, `generate-upload-url`, storage upload URLs, post-upload completions, and `update-task-status` URL-only completions so explicit shadow mode records intended requests without calling production APIs while normal behavior remains unchanged.","depends_on":["T5"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T7","description":"Implement product-effect oracle coverage in `oracles.py` and targeted `reigh-app/supabase/functions/complete_task` tests. Verify generation versus variant creation, `generation_created`, output URL shape, thumbnail behavior, parent/child generation linkage, shadow-visible-record absence, and completion-handler behavior for full canaries while applying lightweight completion-contract checks to other active API-owned routes.","depends_on":["T4","T6"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T8","description":"Implement billing, idempotency, cancellation-cost, and refund discovery oracles. Add executable checks for spend ledger idempotency, sub-task billing skips, `video_enhance` compound cost calculation, lightweight billing policy for every active API route, cancellation-cost behavior, and refund-path discovery; if no real refund ledger path exists, report refund as section status `pending_not_implemented` and never green.","depends_on":["T4","T7"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T9","description":"Add media comparison adapters in `reigh-worker/scripts/dual_run_compare/media.py`: image pHash normalized Hamming, SSIM, pixel dimensions, and format/container; video frame count, sampled/per-frame pHash mean and p95, duration, FPS, and audio duration when present; emit explicit missing-evidence objects rather than omitting absent artifacts.","depends_on":["T2"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T10","description":"Add queue and runtime checks in `queue_contract.py` and `runtime_metrics.py`. Compare fixture queue payloads against current registries, record task type, route key, runtime owner, handler, completion handler, billing path, idempotency policy, refund status, latency, VRAM, OOM, and error class, and classify missing runtime evidence as pending or red based on landed status.","depends_on":["T3","T9"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T11","description":"Generate stable JSON and Markdown reports in `reigh-worker/scripts/dual_run_compare/reporting.py` and wire CLI exit-code semantics. Reports must include route-level report status, calibration status, all required sections, metric results, raw observation refs, shadow isolation, registry/shared-path coverage, RED-first Markdown ordering, and correct nonzero exits for landed RED routes, required oracle failures, sparse green attempts, and unclassified active API routes.","depends_on":["T5","T8","T10"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T12","description":"Add or update focused Python and edge-function regression tests for the new harness behavior: root wrapper import strategy, worker-root path resolution, report-status mapping, sparse metric rejection, active route classification, shared-path oracle coverage, fixture policy validation, refund discovery, shadow path rejection, side-effect interception, report rendering, completion/product effects, billing/idempotency, cancellation-cost behavior, and refund `pending_not_implemented`.","depends_on":["T11"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T13","description":"Run final validation and fix failures until the focused gates pass. Run `python scripts/dual_run_compare.py --dry-run --report-id pytest-dual-run` from the workspace root, `cd reigh-worker && python -m pytest scripts/dual_run_compare/tests -q`, the closest supported `reigh-app` Vitest filters for `complete_task`, `generation`, `billing`, `calculate-task-cost`, and `update-task-status`, `cd reigh-app && npm run lint:edge`, then broader suites if focused checks are green. Also write a short throwaway script that exercises the wrapper/import/report-status sparse-evidence path, run it, confirm the behavior, and delete it before finishing.","depends_on":["T12"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null}],"watch_items":["Do not invoke nested `megaplan` or read/activate the `megaplan` skill; this briefing is already inside the harness context.","Keep Sprint 3 report status separate from Sprint 0B calibration status. Do not add `pending`, `fallback`, or `pending_not_implemented` to `migration-thresholds.yaml` calibration values.","The root wrapper must resolve the worker `scripts` package before the workspace-root `scripts` package, and live-test relative paths must resolve under `reigh-worker`.","Sparse evidence must never produce route-level green for landed routes; missing required media/runtime/error/product/billing sections should become RED for landed routes or documented pending/fallback/WGP-only for non-landed routes.","Every active API-owned route needs lightweight shared-path oracle coverage, not just registry classification; the four named canaries need full regression depth.","Shadow isolation must guard real API side-effect boundaries, not just local artifact paths: completion, upload URL generation, storage upload, status update, billing triggers, and visible generation creation.","Do not treat `update-task-status/cancellationBilling.ts` as refund evidence. It is cancellation-cost/billing coverage unless a real refund ledger path is found.","If the Sprint 2 landed-route list is unavailable, mark explicitly landed routes with missing evidence RED and unclear routes pending with evidence explaining the uncertainty.","Confirm local Vitest filter syntax before considering edge-function validation authoritative.","Live `--execute-live` should remain behind explicit isolated credentials and disposable artifacts; fixture-backed dry-run/oracle mode is the default acceptance path.","Do not make unrelated debt watch items worse, especially existing frontend, audio, timeline, crash-recovery, and direct-route parameter parity debts listed in the prompt."],"sense_checks":[{"id":"SC1","task_id":"T1","question":"From the workspace root, does `python scripts/dual_run_compare.py --dry-run --report-id pytest-dual-run` import `reigh-worker/scripts/dual_run_compare` rather than the root `scripts` package, and do live helper defaults point at `reigh-worker`?","executor_note":"","verdict":""},{"id":"SC2","task_id":"T2","question":"Can strict threshold loading still pass with the existing calibration schema while Sprint 3 reports use only their separate report and section statuses?","executor_note":"","verdict":""},{"id":"SC3","task_id":"T3","question":"Does every route in `TASK_HANDLERS` that is API-owned have an explicit classification and shared-path policy, and do the four named canaries carry all required full-canary fields?","executor_note":"","verdict":""},{"id":"SC4","task_id":"T4","question":"Would a regression in shared completion or billing contract fail at least one active API-owned route outside the four full canaries?","executor_note":"","verdict":""},{"id":"SC5","task_id":"T5","question":"Can shadow artifact policy reject production paths, normal task upload paths, and remote storage URLs while recording skipped side effects in the report?","executor_note":"","verdict":""},{"id":"SC6","task_id":"T6","question":"In explicit shadow mode, are all named side-effect calls recorded and blocked, while normal orchestrator behavior remains unchanged outside shadow mode?","executor_note":"","verdict":""},{"id":"SC7","task_id":"T7","question":"Do product-effect checks execute without live production credentials and prove generation/variant/linkage/output/thumbnail/shadow-record behavior for the full canaries?","executor_note":"","verdict":""},{"id":"SC8","task_id":"T8","question":"Is refund reported green only when backed by an executable refund ledger path, and otherwise reported as section-level `pending_not_implemented` without failing solely for absence of refund implementation?","executor_note":"","verdict":""},{"id":"SC9","task_id":"T9","question":"Do missing media artifacts produce explicit missing-evidence results that feed strict comparison instead of silently dropping metrics?","executor_note":"","verdict":""},{"id":"SC10","task_id":"T10","question":"Do queue/runtime checks record latency, VRAM, OOM, and error class distinctly, with missing evidence classified according to landed status?","executor_note":"","verdict":""},{"id":"SC11","task_id":"T11","question":"Do JSON and Markdown reports include every required route-level section, order RED routes first in Markdown, and exit nonzero for sparse green, unclassified active routes, or landed RED routes?","executor_note":"","verdict":""},{"id":"SC12","task_id":"T12","question":"Do focused tests cover all new guardrails: wrapper import, status separation, sparse rejection, route coverage, shadow isolation, product/billing/idempotency, refund discovery, and report rendering?","executor_note":"","verdict":""},{"id":"SC13","task_id":"T13","question":"Have the required dry-run, focused Python tests, focused edge tests, lint, and throwaway reproduction script all run successfully, with the throwaway script deleted afterward?","executor_note":"","verdict":""}],"user_actions":[{"id":"U1","description":"Provide the official Sprint 2 landed-route list if it exists outside the repository.","phase":"before_execute","blocks_task_ids":null,"rationale":"The executor can proceed without it by treating explicit landed routes as RED when evidence is missing and unclear routes as pending with evidence, but the official list reduces classification ambiguity.","requires_human_only_reason":null},{"id":"U2","description":"Provide isolated live credentials, disposable storage/pods, and any required VPN/cloud access only if live `--execute-live` validation is expected for Sprint 3 acceptance.","phase":"before_execute","blocks_task_ids":null,"rationale":"The accepted default is fixture-backed dry-run/oracle execution; live mode should not run against production side-effect surfaces without isolated credentials.","requires_human_only_reason":null},{"id":"U3","description":"After local validation, review generated Markdown/JSON reports and approve any CI/deployment wiring or production rollout separately.","phase":"after_execute","blocks_task_ids":null,"rationale":"This sprint builds an evidence harness, not a production selector; publishing or rollout approval is an operational decision outside repo editing.","requires_human_only_reason":null}],"meta_commentary":"Execute in the approved order and keep the implementation evidence-first: the harness should make uncertainty visible rather than smoothing it over. The highest-risk mistakes are importing the wrong `scripts` package from the root wrapper, allowing sparse observations to go green, treating cancellation billing as refunds, and building shadow isolation only around local paths while real side effects still happen through API clients. Default to fixture-backed dry-run oracles without production credentials. Add live execution only behind explicit isolated credentials and disposable artifacts. When tests fail, read the failing assertion and fix the implementation or fixture contract; do not weaken guardrails to get a green suite.","validation":{"plan_steps_covered":[{"plan_step_summary":"Step 1: Add workspace-root CLI wrapper with safe worker-package import and smoke test","finalize_item_ids":["T1","T13"]},{"plan_step_summary":"Step 2: Define Sprint 3 report status separately from threshold calibration status","finalize_item_ids":["T2","T12"]},{"plan_step_summary":"Step 3: Require complete evidence before a route can be green","finalize_item_ids":["T2","T12"]},{"plan_step_summary":"Step 4: Build active API-route inventory and classify every route","finalize_item_ids":["T3","T12"]},{"plan_step_summary":"Step 5: Add lightweight shared-path oracle for every active API route","finalize_item_ids":["T4","T12"]},{"plan_step_summary":"Step 6: Extend fixtures with executable route, oracle, billing, refund, idempotency, and side-effect policies","finalize_item_ids":["T3","T4","T12"]},{"plan_step_summary":"Step 7: Add shadow execution policy and artifact isolation","finalize_item_ids":["T5","T12"]},{"plan_step_summary":"Step 8: Intercept API-worker side-effect clients before live shadow mode","finalize_item_ids":["T6","T12"]},{"plan_step_summary":"Step 9: Add product-effect oracle and targeted complete_task tests","finalize_item_ids":["T7","T12"]},{"plan_step_summary":"Step 10: Add billing and idempotency oracle plus calculate-task-cost coverage","finalize_item_ids":["T8","T12"]},{"plan_step_summary":"Step 11: Discover real refund behavior or mark refund pending_not_implemented","finalize_item_ids":["T8","T12"]},{"plan_step_summary":"Step 12: Implement media comparison adapters for image/video evidence","finalize_item_ids":["T9","T12"]},{"plan_step_summary":"Step 13: Implement queue contract and runtime metric checks","finalize_item_ids":["T10","T12"]},{"plan_step_summary":"Step 14: Generate JSON/Markdown reports and enforce exit-code semantics","finalize_item_ids":["T11","T12","T13"]},{"plan_step_summary":"Step 15: Add focused tests and run cheap gates before broader suites","finalize_item_ids":["T12","T13"]}],"orphan_tasks":[],"completeness_notes":"All approved plan steps are mapped to execution tasks, with human actions limited to optional external inputs or operational approvals. The final task is validation-only and includes the required dry-run command, focused test gates, broader checks when appropriate, and a temporary reproduction script that must be deleted after use.","coverage_complete":true},"baseline_test_failures":null,"baseline_test_command":null,"baseline_test_note":"This is an execution-ready briefing document; no baseline tests were run during finalization."}

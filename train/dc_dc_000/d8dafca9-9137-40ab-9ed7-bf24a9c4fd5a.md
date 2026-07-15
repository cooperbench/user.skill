> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

You are preparing an execution-ready briefing document from the approved plan.

        Project directory:
        /Users/user_c042661f/Documents/megaplan





        Idea:
Implement v0.15.0 doc-mode per /Users/user_c042661f/Documents/megaplan/idea-doc-mode.txt — see that file for full spec.

        Approved plan:
        # Implementation Plan: v0.15.0 doc-mode (metaplan)

## Overview

Megaplan currently only produces code artifacts. This feature adds `--mode doc` so the same harness can produce structured documents (plans, RFCs, design docs). The core state machine, flag taxonomy, critique/gate/revise loop, and robustness levels are unchanged. What changes: (1) `plan.json` gains `mode` and `output_path` fields, (2) new doc-mode prompt variants for prep, execute, and review, (3) a new execution schema with `sections_written` instead of `files_changed`, (4) a new `doc_assembly.py` module to assemble sections into the output file, (5) `validate_execution_evidence` branches on mode, (6) a `doc-quality` critique category, (7) finalize handler skips test baseline capture and verification-task injection for doc mode, (8) timeout recovery branches on mode for checkpoint merge and task validation, and (9) Hermes worker's execute fallback reconstructs doc-shaped payloads when mode is doc.

Key files: `cli.py` (parser), `handlers.py` (init + finalize + execute + review), `types.py` (PlanState/PlanConfig), `schemas.py` (execution schema), `evaluation.py` (audit), `merge.py` (validation), `execution.py` (batch loop), `execution_timeout.py` (timeout recovery), `hermes_worker.py` (Hermes fallback), `workers.py` (schema selection), `prompts/` (prompt builders), `checks.py` (critique categories).

The spec is well-scoped: single output file, no mixed-mode, no loop-mode doc support. Existing code-mode tests remain untouched.

## Phase 1: Foundation — Types, Config, CLI, Schema

### Step 1: Add mode/output_path to plan config and types (`megaplan/types.py`)
**Scope:** Small
1. **Add** `mode` and `output_path` as optional fields to `PlanConfig` TypedDict (`megaplan/types.py:28`). `mode` is `str` (values: `"code"`, `"doc"`), `output_path` is `str`.
2. **Verify** that `PlanState` inherits `config: PlanConfig` at `types.py:115`, so the new fields propagate automatically.

### Step 2: Wire `--mode` and `--output` CLI flags (`megaplan/cli.py:811`, `megaplan/handlers.py:717`)
**Scope:** Small
1. **Add** `--mode` argument to `init_parser` with `choices=["code", "doc"]`, `default="code"` (`cli.py:811`, after line 820).
2. **Add** `--output` argument to `init_parser` (`cli.py:811`). Required only when `mode=doc`.
3. **Update** `handle_init` (`handlers.py:717`):
   - Validate that `--output` is provided when `--mode doc` and raise `CliError` otherwise.
   - Validate that `output_path` is relative (no leading `/`) and does not escape project_dir (reject `../` traversal). Resolve and normalize against `project_dir`.
   - Persist `mode` and `output_path` in `state["config"]`. Default `mode` to `"code"` for backward compatibility.

### Step 3: Add `doc-quality` critique category (`megaplan/schemas.py:204`)
**Scope:** Small
1. **Extend** the `category` enum in `SCHEMAS["critique.json"]` at `schemas.py:204` to include `"doc-quality"`.
2. **No changes needed** in `checks.py` — the category is a free string in the critique prompt, not hardcoded in the check registry.

### Step 4: Add doc-mode execution schema (`megaplan/schemas.py`)
**Scope:** Medium
1. **Add** a new `"execution_doc.json"` entry to `SCHEMAS` dict (`schemas.py:315`). Clone `execution.json` but replace:
   - `files_changed` (top-level and in `task_updates[]`) → `sections_written: array of strings`
   - Remove `commands_run` from `task_updates[]` (doc tasks don't run commands)
   - Keep top-level `commands_run` (may be empty), `output`, `deviations`, `sense_check_acknowledgments` unchanged.
2. **Add** helper `get_execution_schema_key(mode: str) -> str` in `schemas.py` that returns `"execution_doc.json"` when mode is `"doc"`, else `"execution.json"`.

### Step 5: Bump version and add CHANGELOG entry (`pyproject.toml`, `CHANGELOG.md`)
**Scope:** Small
1. **Update** `pyproject.toml:7` version from `"0.14.4"` to `"0.15.0"`.
2. **Add** a `## v0.15.0` CHANGELOG entry describing doc-mode.

## Phase 2: Prompts — Doc-Mode Variants

### Step 6: Add doc-mode prep prompt (`megaplan/prompts/prep_doc.py`)
**Scope:** Medium
1. **Create** `megaplan/prompts/prep_doc.py` with a `_prep_doc_prompt(state, plan_dir, root=None)` function. Repoint the prompt from "search the codebase for relevant files" to "what sources, prior art, related docs should inform this document?" Sense-check items become "did you read X?" rather than "did you find the relevant module?"
2. **Keep** the output schema identical to `prep.json` — the fields (`key_evidence`, `relevant_code`, `constraints`, `suggested_approach`) still apply, just the content and prompt framing change. `relevant_code` becomes references to existing docs/prior art.

### Step 7: Add doc-mode execute prompt (`megaplan/prompts/execute_doc.py`)
**Scope:** Medium
1. **Create** `megaplan/prompts/execute_doc.py` with `_execute_doc_prompt` and `_execute_doc_batch_prompt`.
2. **Frame** the executor as an author writing a document. Its only filesystem operation is writing to the configured `output_path`. Replace `files_changed` references with `sections_written`. Remove `commands_run` from per-task guidance.
3. **Include** the doc-mode output shape example (JSON with `sections_written` instead of `files_changed`, no `commands_run` in task_updates).
4. **Reuse** shared helpers: `_execute_nudges`, `_execute_approval_note`, `_execute_rerun_guidance`, `_render_prep_block` from existing code.

### Step 8: Add doc-mode review prompt (`megaplan/prompts/review_doc.py`)
**Scope:** Medium
1. **Create** `megaplan/prompts/review_doc.py` with `_review_doc_prompt(state, plan_dir, *, review_intro, criteria_guidance, ...)`.
2. **Reword** to treat the deliverable as text: instead of "cross-reference files_changed against git diff", say "read the output file and judge it against success criteria." Remove git-diff and `execution_audit.json` references — the audit for doc mode is section-based, not git-based.
3. **Keep** the same `review.json` output schema — `must`/`should`/`info` criteria, `task_verdicts`, `sense_check_verdicts` all apply.

### Step 9: Wire doc-mode prompts into dispatch (`megaplan/prompts/__init__.py`, `megaplan/prompts/finalize.py`)
**Scope:** Small
1. **Import** the new prompt builders from `prep_doc.py`, `execute_doc.py`, `review_doc.py`.
2. **Update** `create_claude_prompt` / `create_codex_prompt` / `create_hermes_prompt` to check `state["config"].get("mode", "code")` and select the appropriate builder for `prep`, `execute`, and `review` steps. Other steps (plan, critique, gate, finalize, revise) use the same builders regardless of mode.
3. **Update** `_finalize_prompt` (`finalize.py:22`): add a conditional block for doc mode that replaces task field guidance — use `sections_written` instead of `files_changed`/`commands_run`, remove the test-verification requirement from the prompt text, and instruct the finalizer to omit `baseline_test_failures`/`baseline_test_command`.

## Phase 3: Core Logic — Assembly, Merge, Audit, Finalize Handler

### Step 10: Create doc assembly module (`megaplan/doc_assembly.py`)
**Scope:** Medium
1. **Create** `megaplan/doc_assembly.py` with:
   - `assemble_doc(plan_dir: Path, output_path: Path, finalize_data: dict) -> Path`: reads per-batch executor outputs, orders sections by plan position, writes the assembled file atomically (temp file + rename).
   - `extract_sections(batch_payloads: list[dict]) -> dict[str, str]`: maps section_id → rendered text from executor output.
2. **Idempotent**: running twice on the same plan replaces the file completely.
3. **Call site**: invoked at the end of execute (after all batches complete) in `execution.py`.

### Step 11: Update merge validation for doc mode (`megaplan/execution.py:256`)
**Scope:** Medium
1. **Update** `_merge_batch_results` in `execution.py:256` to read mode from state config. When mode is `"doc"`:
   - Required fields for task_updates become `("task_id", "status", "executor_notes", "sections_written")` instead of `("task_id", "status", "executor_notes", "files_changed", "commands_run")`.
   - Merge fields become `("status", "executor_notes", "sections_written")`.
   - `array_fields` becomes `("sections_written",)`.
2. **No changes** to `merge.py` itself — it's generic; the branching happens at the call site.

### Step 12: Branch `validate_execution_evidence` for doc mode (`megaplan/evaluation.py:123`)
**Scope:** Medium
1. **Add** a `mode` parameter to `validate_execution_evidence` (default `"code"`).
2. **When mode is `"doc"`**, replace the git-status comparison with:
   - Extract planned sections from finalize_data tasks (all `sections_written` across done tasks).
   - Resolve `output_path` from finalize_data or accept it as a parameter.
   - Verify: output file exists and is non-empty, all planned sections claimed by done tasks, no unclaimed sections.
   - Return findings in the same `{"findings": [...], "files_in_diff": [], "files_claimed": [], "skipped": False}` shape for compatibility.
3. **When mode is `"code"`**, behavior is unchanged (existing git-status logic).
4. **Update** all callers to pass mode: `execution.py:423` and `execution_timeout.py:203,216`.

### Step 13: Branch finalize handler for doc mode (`megaplan/handlers.py:376`)
**Scope:** Medium
1. **Update** `_write_finalize_artifacts` (`handlers.py:376`): when `state["config"].get("mode") == "doc"`:
   - **Skip** `_capture_test_baseline()` — doc plans don't run tests. Set `baseline_test_failures` to `None` and `baseline_test_command` to `None`.
   - **Skip** `_ensure_verification_task()` — doc plans don't have a final test-running task.
   - Still call `_reconcile_validation_after_mutation()` (it's harmless and keeps validation consistent).
2. **Update** `_validate_finalize_payload` (`handlers.py:409`): no changes needed — it validates `tasks`, `sense_checks`, `watch_items` generically. Doc-mode tasks still have `id`, `description`, `status: pending`.

### Step 14: Branch timeout recovery for doc mode (`megaplan/execution_timeout.py`)
**Scope:** Medium
1. **Update** `_merge_timeout_checkpoint` (`execution_timeout.py:110`): read mode from state config (passed as parameter or read from finalize_data). When mode is `"doc"`:
   - Required fields become `("task_id", "status", "executor_notes", "sections_written")`.
   - Merge fields become `("status", "executor_notes", "sections_written")`.
   - `array_fields` becomes `("sections_written",)`.
2. **Update** `_reset_timeout_invalid_tasks` (`execution_timeout.py:41`): when mode is `"doc"`:
   - Evidence check uses `sections_written` instead of `files_changed`.
   - Skip the `files_in_diff` cross-check (no git diff in doc mode).
   - `has_evidence` lambda checks `bool(task.get("sections_written"))`.
3. **Update** `_recover_execute_timeout` (`execution_timeout.py:163`): pass mode to `validate_execution_evidence` calls at lines 203 and 216. When mode is `"doc"`, aggregate `sections_written` instead of `files_changed` for the response at line 275–281.

### Step 15: Update status display for doc mode (`megaplan/cli.py:341`)
**Scope:** Small
1. **Update** `_build_status_payload` (in `cli.py`) to include `mode` and `output_path` in the status output when present in state config.

## Phase 4: Wiring — Handlers, Workers, Hermes

### Step 16: Update execute handler for doc mode (`megaplan/handlers.py:1337`, `megaplan/execution.py`)
**Scope:** Medium
1. **In** `handle_execute` (`handlers.py:1337`): detect mode from `state["config"].get("mode", "code")`. When `"doc"`:
   - Skip `--confirm-destructive` requirement (doc mode writes a single output file, not repo code).
   - After all batches complete, call `assemble_doc()` to produce the output file.
2. **In** `_run_and_merge_batch` (`execution.py:349`): accept mode parameter. When mode is `"doc"`:
   - Skip `_observe_git_changes`, `_collect_quality_deviations`, and `capture_before_line_counts` (no git changes expected).
   - Adapt `_check_done_task_evidence`: `has_evidence` checks `sections_written` instead of `files_changed`, `has_advisory_evidence` always returns `True` (no `commands_run` analog).
   - Pass mode to `validate_execution_evidence`.
3. **In** `_build_aggregate_execution_payload` (`execution.py:136`): when mode is `"doc"`, aggregate `sections_written` instead of `files_changed`.

### Step 17: Update review handler for doc mode (`megaplan/handlers.py:1576`, `megaplan/prompts/review.py`)
**Scope:** Small
1. **In** `handle_review`: when mode is `"doc"`, skip mechanical pre-checks that depend on code (test pass/fail, type checking).
2. **In** `_parallel_review_context` (`prompts/review.py:78`): when mode is `"doc"`, replace `git_diff` with the output file content read from `state["config"]["output_path"]` resolved against `project_dir`.

### Step 18: Update worker schema selection (`megaplan/workers.py`)
**Scope:** Small
1. **Update** schema lookup: when step is `"execute"` and mode is `"doc"` (read from `state["config"]`), use `"execution_doc.json"` instead of `"execution.json"`. The mode is available from `state["config"]` which is already passed to `run_claude_step`, `run_codex_step`, etc.
2. **Touch points**: `workers.py:58` (`STEP_SCHEMA_FILENAMES` lookup in `run_claude_step`), `workers.py` codex schema path, and `hermes_worker.py:294` (`schema_name = STEP_SCHEMA_FILENAMES[step]`).

### Step 19: Update Hermes worker for doc mode (`megaplan/hermes_worker.py`)
**Scope:** Medium
1. **Update** `_reconstruct_execute_payload` (`hermes_worker.py:635`): when mode is `"doc"`:
   - Skip git-diff and git-status based `files_changed` reconstruction (lines 670–697).
   - Return `sections_written` instead of `files_changed` in the reconstructed payload.
   - Remove `commands_run` from the reconstructed payload (or leave as empty list for schema compat).
2. **Update** schema lookup at `hermes_worker.py:294`: use `get_execution_schema_key(mode)` to select the correct schema filename. Mode comes from `state["config"]` which is passed through to `run_hermes_step`.
3. **Update** the execute fallback path at `hermes_worker.py:192–196`: when mode is `"doc"`, the fallback should attempt doc-shaped reconstruction rather than code-shaped.

## Phase 5: Tests

### Step 20: Add doc-mode unit tests (`tests/test_doc_mode.py`)
**Scope:** Medium
1. **Test** `handle_init` with `--mode doc --output docs/plan.md` produces state with `mode: "doc"` and `output_path`.
2. **Test** `handle_init` with `--mode doc` but no `--output` raises `CliError`.
3. **Test** `handle_init` with `--mode doc --output /absolute/path` raises `CliError` (path containment).
4. **Test** `handle_init` with `--mode doc --output ../escape/path` raises `CliError` (traversal).
5. **Test** `validate_execution_evidence` in doc mode: catches missing sections, catches unclaimed sections, passes when all sections present.
6. **Test** `assemble_doc`: sections assembled in plan order, output file is non-empty, idempotent re-run replaces file.
7. **Test** doc-mode execution schema validates correctly via `strict_schema`.
8. **Test** `_write_finalize_artifacts` in doc mode: skips test baseline capture, skips verification task injection.
9. **Test** `_merge_timeout_checkpoint` in doc mode: uses `sections_written` fields.
10. **Test** `_reset_timeout_invalid_tasks` in doc mode: checks `sections_written` evidence, skips git-diff cross-check.

### Step 21: Verify existing tests pass (`tests/`)
**Scope:** Small
1. **Run** `pytest tests/` — all existing tests must pass unchanged. The `mode` field defaults to `"code"` everywhere, so no existing behavior changes.

## Execution Order
1. Steps 1–5 (types, CLI, schema, version) — foundation with no behavioral changes.
2. Steps 6–9 (prompts) — can be done in parallel since they're independent files. Wire dispatch last.
3. Steps 10–15 (assembly, merge, audit, finalize handler, timeout recovery, status) — core logic.
4. Steps 16–19 (handlers, execution loop, workers, Hermes) — wire everything together.
5. Steps 20–21 (tests) — prove the change works and nothing regressed.

## Validation Order
1. Run `pytest tests/test_schemas.py` after Step 4 to verify new schema is valid.
2. Run `pytest tests/` after Step 5 to verify no regressions from version bump.
3. Run `pytest tests/test_doc_mode.py` after Step 20 for focused doc-mode coverage.
4. Run full `pytest tests/` after Step 21 for final regression check.


        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-04-15T07:55:59Z",
  "hash": "sha256:0f9e654ea81728c6a99fa5a73ef26a1e87a0dcf6effa4576f87ed66926d7f463",
  "changes_summary": "Addressed four significant critique flags: (1) FLAG-001 \u2014 added Step 13 to branch `_write_finalize_artifacts` for doc mode, skipping `_capture_test_baseline()` and `_ensure_verification_task()`, and updated Step 9 to add doc-mode guidance in the finalize prompt. (2) FLAG-002 \u2014 added Step 14 to branch all three timeout recovery functions (`_merge_timeout_checkpoint`, `_reset_timeout_invalid_tasks`, `_recover_execute_timeout`) for doc mode, using `sections_written` instead of `files_changed`/`commands_run` and skipping git-diff cross-checks. (3) FLAG-003 \u2014 added Step 19 to update Hermes worker's `_reconstruct_execute_payload` and schema lookup for doc mode, preventing code-shaped fallback reconstruction. (4) FLAG-004 \u2014 expanded Step 2 to add concrete output_path validation in `handle_init`: reject absolute paths, reject `../` traversal, normalize against project_dir. Added path-containment tests to Step 20. Also added new success criteria for timeout recovery and path containment.",
  "flags_addressed": [
    "FLAG-001",
    "FLAG-002",
    "FLAG-003",
    "FLAG-004"
  ],
  "questions": [
    "The spec says 'output file exists and is non-empty' in the doc-mode audit. Should the audit also verify that the output file is valid markdown (or whatever format), or just check existence + non-empty?",
    "For doc-mode execute, should the executor agent have full filesystem read access (to reference existing docs/code) but only write access to the output path? Or should read access also be restricted? (Assumption: read access unrestricted, write containment via init-time validation only for v0.15.)"
  ],
  "success_criteria": [
    {
      "criterion": "megaplan init --mode doc --output X '...' produces a plan with mode: doc and output_path in state.json",
      "priority": "must"
    },
    {
      "criterion": "megaplan init --mode doc without --output raises a clear error",
      "priority": "must"
    },
    {
      "criterion": "megaplan init --mode doc --output /absolute/path raises a clear error",
      "priority": "must"
    },
    {
      "criterion": "megaplan init --mode doc --output ../traversal raises a clear error",
      "priority": "must"
    },
    {
      "criterion": "All existing code-mode tests pass unchanged (pytest tests/ green)",
      "priority": "must"
    },
    {
      "criterion": "Doc-mode audit rejects an executor that claims a section not in the plan",
      "priority": "must"
    },
    {
      "criterion": "Doc-mode audit rejects an executor that skips a section without marking the task blocked/skipped",
      "priority": "must"
    },
    {
      "criterion": "Doc-mode execute produces a non-empty file at the configured output_path",
      "priority": "must"
    },
    {
      "criterion": "pyproject.toml version is 0.15.0",
      "priority": "must"
    },
    {
      "criterion": "CHANGELOG has a v0.15.0 entry describing doc-mode",
      "priority": "must"
    },
    {
      "criterion": "Doc-mode execution schema (execution_doc.json) validates correctly via strict_schema",
      "priority": "must"
    },
    {
      "criterion": "Doc-mode review with a must criterion about doc content can fail and trigger needs_rework",
      "priority": "must"
    },
    {
      "criterion": "Doc-mode finalize skips test baseline capture and verification task injection",
      "priority": "must"
    },
    {
      "criterion": "Doc-mode timeout recovery uses sections_written fields and skips git-diff cross-check",
      "priority": "must"
    },
    {
      "criterion": "Hermes worker doc-mode execute uses execution_doc.json schema and reconstructs sections_written fallback",
      "priority": "must"
    },
    {
      "criterion": "New prompt files (prep_doc.py, execute_doc.py, review_doc.py) each under ~300 lines",
      "priority": "should"
    },
    {
      "criterion": "doc_assembly.py under ~150 lines \u2014 simple section concatenation, not a complex engine",
      "priority": "should"
    },
    {
      "criterion": "No changes to existing code-mode prompt files beyond adding mode-dispatch branches",
      "priority": "should"
    },
    {
      "criterion": "megaplan status shows mode: doc and output_path when in doc mode",
      "priority": "should"
    },
    {
      "criterion": "Full end-to-end doc-mode plan lifecycle tested manually (init through review)",
      "priority": "info"
    }
  ],
  "assumptions": [
    "Assembly happens once after all batches complete (not incrementally per-batch). The spec says 'assembles sections in plan-order' which implies a final assembly step, and incremental assembly would require conflict resolution between partial writes.",
    "The output_path is relative to project_dir as stated in the spec. Validation in handle_init rejects absolute paths and '../' traversal. The resolved path is stored normalized in state.json.",
    "Doc-mode tasks in finalize.json use the same task schema but with `sections_written: []` instead of `files_changed: []`. The finalize schema gains an optional `sections_written` field on tasks, populated only in doc mode.",
    "Existing plans with no `mode` field default to 'code' \u2014 this is a backward-compatible addition, not a migration.",
    "The doc-mode review uses the same review.json output schema. The only difference is prompt framing \u2014 criteria like 'the doc names every blocking risk' replace 'tsc clean'.",
    "The `--confirm-destructive` flag is not required for doc-mode execute since it only writes a single output file, not repo code.",
    "Doc-mode finalize skips _capture_test_baseline and _ensure_verification_task entirely. The finalizer prompt for doc mode instructs the model not to produce test-related fields.",
    "Hermes execute fallback for doc mode returns sections_written instead of files_changed and skips git-diff reconstruction. If no tool calls or sections are found, the fallback returns None as it does today for code mode.",
    "Output-path containment is enforced at init time only (reject bad paths). Runtime enforcement of write-only-to-output-path is not added in v0.15 because agent sandboxing is already handled by the worker layer (Codex writable_roots, trusted-container mode). The init-time guard prevents accidental misconfiguration, not adversarial agents."
  ],
  "delta_from_previous_percent": 73.49,
  "structure_warnings": []
}

        Gate summary:
        {
  "recommendation": "ITERATE",
  "rationale": "Light robustness: single revision pass to incorporate critique feedback.",
  "signals_assessment": "",
  "warnings": [],
  "settled_decisions": []
}

        Flag registry:
        [
  {
    "id": "FLAG-001",
    "concern": "Finalize contract: the plan treats finalize as mostly shared, but the current finalize prompt and handler are hard-wired for code execution. `_finalize_prompt()` still requires the final task to run tests and even create a throwaway repro script, while `_write_finalize_artifacts()` always captures a pytest baseline and `_ensure_verification_task()` appends a test task with `files_changed`/`commands_run`. Without an explicit doc-mode branch for finalize, doc plans will be mutated back into code-style execution checklists before execute starts.",
    "evidence": "Addressed four significant critique flags: (1) FLAG-001 \u2014 added Step 13 to branch `_write_finalize_artifacts` for doc mode, skipping `_capture_test_baseline()` and `_ensure_verification_task()`, and updated Step 9 to add doc-mode guidance in the finalize prompt. (2) FLAG-002 \u2014 added Step 14 to branch all three timeout recovery functions (`_merge_timeout_checkpoint`, `_reset_timeout_invalid_tasks`, `_recover_execute_timeout`) for doc mode, using `sections_written` instead of `files_changed`/`commands_run` and skipping git-diff cross-checks. (3) FLAG-003 \u2014 added Step 19 to update Hermes worker's `_reconstruct_execute_payload` and schema lookup for doc mode, preventing code-shaped fallback reconstruction. (4) FLAG-004 \u2014 expanded Step 2 to add concrete output_path validation in `handle_init`: reject absolute paths, reject `../` traversal, normalize against project_dir. Added path-containment tests to Step 20. Also added new success criteria for timeout recovery and path containment.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-002",
    "concern": "Timeout recovery: the execute timeout/checkpoint path is still code-only, and the plan does not include it. If a doc-mode execute times out, `_merge_timeout_checkpoint()` requires `files_changed` and `commands_run`, and `_reset_timeout_invalid_tasks()` revalidates tasks against git-diff-style evidence. That will drop or reset legitimate doc-mode progress instead of recovering it.",
    "evidence": "Addressed four significant critique flags: (1) FLAG-001 \u2014 added Step 13 to branch `_write_finalize_artifacts` for doc mode, skipping `_capture_test_baseline()` and `_ensure_verification_task()`, and updated Step 9 to add doc-mode guidance in the finalize prompt. (2) FLAG-002 \u2014 added Step 14 to branch all three timeout recovery functions (`_merge_timeout_checkpoint`, `_reset_timeout_invalid_tasks`, `_recover_execute_timeout`) for doc mode, using `sections_written` instead of `files_changed`/`commands_run` and skipping git-diff cross-checks. (3) FLAG-003 \u2014 added Step 19 to update Hermes worker's `_reconstruct_execute_payload` and schema lookup for doc mode, preventing code-shaped fallback reconstruction. (4) FLAG-004 \u2014 expanded Step 2 to add concrete output_path validation in `handle_init`: reject absolute paths, reject `../` traversal, normalize against project_dir. Added path-containment tests to Step 20. Also added new success criteria for timeout recovery and path containment.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-003",
    "concern": "Agent coverage: the worker changes are incomplete for Hermes. The plan mentions `workers.py` schema selection, but `hermes_worker.py` independently loads the execute schema from `STEP_SCHEMA_FILENAMES` and reconstructs failed execute payloads with `files_changed`/`commands_run`. Doc mode would therefore remain code-shaped or fail under `--hermes` and any Hermes fallback path.",
    "evidence": "Addressed four significant critique flags: (1) FLAG-001 \u2014 added Step 13 to branch `_write_finalize_artifacts` for doc mode, skipping `_capture_test_baseline()` and `_ensure_verification_task()`, and updated Step 9 to add doc-mode guidance in the finalize prompt. (2) FLAG-002 \u2014 added Step 14 to branch all three timeout recovery functions (`_merge_timeout_checkpoint`, `_reset_timeout_invalid_tasks`, `_recover_execute_timeout`) for doc mode, using `sections_written` instead of `files_changed`/`commands_run` and skipping git-diff cross-checks. (3) FLAG-003 \u2014 added Step 19 to update Hermes worker's `_reconstruct_execute_payload` and schema lookup for doc mode, preventing code-shaped fallback reconstruction. (4) FLAG-004 \u2014 expanded Step 2 to add concrete output_path validation in `handle_init`: reject absolute paths, reject `../` traversal, normalize against project_dir. Added path-containment tests to Step 20. Also added new success criteria for timeout recovery and path containment.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-004",
    "concern": "Output-path containment: the plan assumes `output_path` will be validated and doc execute will only write that file, but no implementation step actually adds that enforcement. In the current runner, Codex execute is given the whole project as a writable root, and trusted-container mode bypasses Codex sandboxing entirely. Skipping `--confirm-destructive` for doc mode is unsafe unless the plan also adds concrete path normalization and worker-level write restriction.",
    "evidence": "Addressed four significant critique flags: (1) FLAG-001 \u2014 added Step 13 to branch `_write_finalize_artifacts` for doc mode, skipping `_capture_test_baseline()` and `_ensure_verification_task()`, and updated Step 9 to add doc-mode guidance in the finalize prompt. (2) FLAG-002 \u2014 added Step 14 to branch all three timeout recovery functions (`_merge_timeout_checkpoint`, `_reset_timeout_invalid_tasks`, `_recover_execute_timeout`) for doc mode, using `sections_written` instead of `files_changed`/`commands_run` and skipping git-diff cross-checks. (3) FLAG-003 \u2014 added Step 19 to update Hermes worker's `_reconstruct_execute_payload` and schema lookup for doc mode, preventing code-shaped fallback reconstruction. (4) FLAG-004 \u2014 expanded Step 2 to add concrete output_path validation in `handle_init`: reject absolute paths, reject `../` traversal, normalize against project_dir. Added path-containment tests to Step 20. Also added new success criteria for timeout recovery and path containment.",
    "status": "addressed",
    "severity": "significant"
  }
]

        Critique history:
        [
  {
    "iteration": 1,
    "flag_count": 4,
    "verified": []
  }
]

        Debt watch items (do not make these worse):
        [
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the mobile action-surface plan is technically incorrect for the current component structure. `submissioncarouselcard` hides `footercontent` below the `md` breakpoint (`src/components/submissioncarouselcard.tsx:219`), while `submissionscarouselpage` also hides the score panel on mobile via `asidecontent={<div classname=\"hidden md:block\">...` and passes `hideactions` to `scorepanel` at `src/pages/submissionscarouselpage.tsx:250-263,347`. reusing that pattern for entrypage would leave mobile users with no navigation controls and no scoring controls. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: i checked the sign-in callback path again. `submissionslayout` already wires `usescoring(..., { onrequiresignin: () => pagemachine.dispatch({ type: 'open_sign_in_modal' }) })` at `src/pages/submissionslayout.tsx:38-40`, and `scorepanel` still has its own `onrequiresignin` prop. the revised step 4.2 is acceptable only if it explicitly rewires that prop to `pagemachine.dispatch`; otherwise removing local modal state would orphan the direct ui callback. the plan hints at this, but it remains easy to misread because the scoring-context callback and the scorepanel prop are separate mechanisms. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: checked the new diff-helper proposal against the repo's existing execution-evidence semantics. `validate_execution_evidence()` in `megaplan/evaluation.py:109-175` uses `git status --short`, so untracked files count as real changed files today, but step 3 proposes `collect_git_diff_patch(project_dir)` via `git diff head`; by git behavior that will not include untracked files, so heavy review could miss exactly the newly created files that execute and review already treat as part of the patch. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: a generated-schema gap remains. `tests/test_schemas.py` reads the repo-root `.megaplan/schemas/review.json` directly via `_review_disk_schema()`, the checked-in local file is currently stale relative to `schemas`, and `ensure_runtime_layout()` in `megaplan/_core/io.py` is the production writer for that file class. the plan says generated schemas must stay aligned, but it never names a regeneration step or a test adjustment for that disk-schema path, so the validation story is still incomplete. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-success-criteria-well-prioritized-and-verifiable: are the success criteria well-prioritized and verifiable?: mobile behavior is still under-prioritized relative to the actual risk in this repo. the user constraint specifically mentions the mobile bottom nav, but the only mobile-specific success criterion left is 'mobile scoring ux is coherent' at `info` level. given that the plan currently removes the working mobile nav, there should be at least a `should` or `must` criterion stating that mobile users retain navigation and scoring controls. (flagged 1 times across 1 plans)",
  "[DEBT] completeness: handle_init() and override flows also emit next_step but aren't listed for next_step_runtime enrichment. (flagged 1 times across 1 plans)",
  "[DEBT] completeness: handle_execute() at handlers.py:1152-1175 can clear next_step to none but leave stale next_step_runtime. (flagged 1 times across 1 plans)",
  "[DEBT] completeness: next_step_runtime fires on previous step completion, not literally when the next phase starts. (flagged 1 times across 1 plans)",
  "[DEBT] completeness: test_command config override unreachable via normal init/cli flow (flagged 1 times across 1 plans)",
  "[DEBT] correctness: status-progress gating excludes finalized plans with finalize.json in between-batch and blocked states. (flagged 1 times across 1 plans)",
  "[DEBT] correctness: resolve_phase_runtime called on non-phase next_step values would fail. (flagged 1 times across 1 plans)",
  "[DEBT] correctness: non-phase next_step values from workflow_next() not filtered. (flagged 1 times across 1 plans)",
  "[DEBT] correctness: baseline_test_command schema says string-only but fallback returns none (flagged 1 times across 1 plans)",
  "[DEBT] correctness: fallback uses null+baseline_test_note instead of brief's empty-array+meta_commentary (flagged 1 times across 1 plans)",
  "[DEBT] criteria-prompt: criteria prompt: v3 replaces `_review_prompt()` in heavy mode with a new `heavy_criteria_review_prompt`, so the plan no longer follows the brief's explicit requirement that `_review_prompt()` remain the heavy-mode `criteria_verdict` check. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: a new critical issue is introduced on mobile. step 4.9 says to remove entrypage's mobile sticky bottom nav and 'use the same `footercontent` slot in submissioncarouselcard', but `src/components/submissioncarouselcard.tsx:217-221` renders `footercontent` inside `classname=\"hidden md:block\"`. in the current repo, the mobile sticky nav at `src/pages/entrypage.tsx:283-340` is the only mobile surface for back/next and the score toggle, so the revised plan would remove working mobile controls and replace them with a slot that is explicitly hidden on phones. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: the plan still contradicts itself on mobile behavior. assumption #3 says the browse-mode mobile score toggle will be preserved, but step 4.9 removes the entire mobile sticky nav that contains that toggle in `src/pages/entrypage.tsx:314-330`. the implementer cannot satisfy both instructions as written. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: checked step 7 against the brief's explicit prompt-builder requirement. the revision fixes the old context leak by introducing a brand-new `heavy_criteria_review_prompt`, but the brief said `_review_prompt()` should stay as-is and still run as the `criteria_verdict` check in heavy mode; v3 solves the problem by replacing that heavy-mode criteria path instead of reusing the baseline review prompt, which is still a material divergence from the requested design. (flagged 1 times across 1 plans)",
  "[DEBT] diff-capture: diff capture: the proposed `collect_git_diff_patch(project_dir)` helper uses `git diff head`, which will miss untracked files even though the existing execution-evidence path already treats untracked files as real changed work. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: if the implementation really wants `footercontent` to carry mobile actions, the plan must also include a supporting change in `src/components/submissioncarouselcard.tsx` or render a separate mobile control surface outside the card. right now step 4.9 removes the mobile nav but does not list `submissioncarouselcard.tsx:217-221` as a place that must change, so the required glue for mobile controls is missing. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: the prior missing locations in `megaplan/workers.py` and `tests/test_workers.py` are now covered, but one supporting-infrastructure path is still absent from the steps: the repo-root generated schema copy under `.megaplan/schemas/review.json` and the tests that read it directly. without either explicitly regenerating that file or changing those tests to materialize schemas in a temp root, the plan can still leave the runtime-schema copy out of sync with the raw registry. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: the plan adds _set_active_step and _clear_active_step helpers to handlers.py. _run_worker (handlers.py:135) is modified to accept a `resolved` parameter. but _run_worker is also called directly by handle_critique's sequential fallback at line 801 and 803. these calls currently don't pass `resolved`. the plan's step 2.6 for handle_critique says to set active_step after resolution at line 794 \u2014 but the _run_worker calls at 801/803 would re-resolve the agent internally (since `resolved` isn't passed). this means the agent is resolved twice on the critique sequential path. the double-resolution is wasteful but correct (same result). however, to match the plan's goal of 'resolve_agent_mode() is called once per handler invocation', the resolved tuple should be passed to these _run_worker calls too. (flagged 1 times across 1 plans)",
  "[DEBT] execute-phase-contract: early-killed baselines pass truncated output to the execute worker, which may produce lower-quality diagnosis than full output. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: i checked the skip caller path against the real hook behavior and `removefromqueue(entryid)` looks redundant. `scoring.skipentry(entryid)` optimistically adds the id to `skippedentryids` in `src/hooks/usescoring.ts:245-249`, and `usecarouselqueue` already reactively filters skipped entries from `submissions[]` in `src/hooks/usecarouselqueue.ts:154-165`. calling `removefromqueue()` immediately afterward is safe, but it duplicates an existing state transition and should be justified as an explicit ux optimization rather than required logic. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the direct ui sign-in caller is still important here. `scorepanel` invokes its own `onrequiresignin` prop when an unauthenticated user interacts with the score ui (`src/components/scorepanel.tsx:499-515`), which is independent of the scoring hook's internal `requireauth()` path. the plan should be read as requiring that caller to dispatch `open_sign_in_modal`; otherwise one caller remains broken even if `submitscore()` is correctly wired. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: i rechecked the caller paths after the revision. the raw-schema caller path through `validate_payload()` is now accounted for, but the runtime-schema caller path still is not: `strict_schema()` only reaches the on-disk runtime schemas through `ensure_runtime_layout()`, while current tests like `tests/test_schemas.py` and `tests/test_parallel_review.py` consume the already-written repo copy directly. the plan does not yet say how that caller path gets refreshed or asserted after the code change. (flagged 1 times across 1 plans)",
  "[DEBT] handler-boilerplate: _run_worker() pseudocode hardcodes iteration=state['iteration'] but handle_plan and handle_revise use different failure iteration values. (flagged 1 times across 1 plans)",
  "[DEBT] handler-boilerplate: same issue as correctness-1: failure iteration would be wrong for plan/revise handlers. (flagged 1 times across 1 plans)",
  "[DEBT] install-paths: local setup path doesn't expose subagent mode (flagged 1 times across 1 plans)",
  "[DEBT] install-paths: no automated guard to keep the mirror file synchronized with source files (flagged 1 times across 1 plans)",
  "[DEBT] install-paths: local setup test only checks agents.md existence, not content (flagged 1 times across 1 plans)",
  "[DEBT] is-there-convincing-verification-for-the-change: is there convincing verification for the change?: the test-plan details still miss a small but real infrastructure update: the current `locationdisplay` helper in `src/pages/submissionscarouselpage.test.tsx:289-291` only renders `location.pathname`, so the step 7 requirement to assert `{ state: { carousel: true, navdirection: 'forward' } }` cannot be implemented unless that helper is extended to expose `location.state`. the same pattern exists in the related page tests. (flagged 1 times across 1 plans)",
  "[DEBT] is-there-convincing-verification-for-the-change: is there convincing verification for the change?: there is still no explicit mobile regression test in the plan, even though the revised implementation proposal removes the only current mobile nav/score surface. given the repository's actual component structure, a mobile-focused test or visual verification step is needed to prove controls remain accessible below `md`. (flagged 1 times across 1 plans)",
  "[DEBT] mobile-ui: mobile ui: removing entrypage's mobile sticky nav and relying on `submissioncarouselcard.footercontent` would break mobile navigation and scoring because that footer slot is hidden below the `md` breakpoint. (flagged 1 times across 1 plans)",
  "[DEBT] runtime-schema-sync: runtime schema sync: the plan still does not include an explicit refresh or validation step for the generated `.megaplan/schemas/review.json` copy that repository tests read directly. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: the mobile problem is broader than entrypage. `submissionscarouselpage` already has a pre-existing mobile gap because its score panel is desktop-only and its footer actions are also hidden on mobile (`src/pages/submissionscarouselpage.tsx:250-263,347-354` plus `src/components/submissioncarouselcard.tsx:219`). the revised plan says entrypage should 'match the carouselpage pattern', which would spread that existing gap into the one page that currently has working mobile controls. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: the revised plan correctly narrows the schema-shape problem itself back to the six audited mismatches, but the generated runtime-schema consumer path is broader than the plan acknowledges: `tests/test_parallel_review.py` also reads the runtime `review.json` schema from `schemas_root(repo_root)`, so stale generated schema copies can affect more than the direct schema tests. (flagged 1 times across 1 plans)",
  "[DEBT] subagent-safeguards: hermes reference safeguard numbers not validated against actual implementation (flagged 1 times across 1 plans)",
  "[DEBT] subagent-safeguards: plan's retry caps (1 phase, 3 execute) may differ from hermes-agent's actual policy (flagged 1 times across 1 plans)",
  "[DEBT] worker-permissions: codex --full-auto flag only triggers for step == 'execute', not 'loop_execute' (flagged 1 times across 1 plans)",
  "[DEBT] worker-permissions: claude --permission-mode bypasspermissions only triggers for step == 'execute', not 'loop_execute' (flagged 1 times across 1 plans)",
  "[DEBT] workflow-state-machine: _plan_prompt() does not read research.json, so replanning from state_researched would ignore research results. (flagged 1 times across 1 plans)",
  "[DEBT] workflow-state-machine: same issue as correctness-2: state_researched \u2192 plan path is only partially wired. (flagged 1 times across 1 plans)",
  "[DEBT] workflow-state-machine: _plan_prompt() is a missed location for the state_researched \u2192 plan change. (flagged 1 times across 1 plans)"
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
        - `meta_commentary` must be a single string with execution guidance, gotchas, or judgment calls that help the executor succeed.
        - `validation` must be an object that self-checks plan coverage:
          - `plan_steps_covered`: enumerate EVERY step from the approved plan. For each step, provide a short `plan_step_summary` (the step's intent in one phrase) and `finalize_task_ids` (array of task IDs that implement it — a single plan step may map to multiple tasks).
          - `orphan_tasks`: task IDs that do not correspond to any plan step. Normally empty. If non-empty, explain in `completeness_notes`.
          - `completeness_notes`: free-text explanation of any gaps, deviations, or deliberate omissions.
          - `coverage_complete`: set to `true` only if every plan step has at least one finalize task AND you have verified the mapping by reviewing each entry. Set to `false` if any plan step is missing coverage.
          - Example:
          ```json
          "validation": {
            "plan_steps_covered": [
              {"plan_step_summary": "Add retry logic to API client", "finalize_task_ids": ["T1", "T2"]},
              {"plan_step_summary": "Update configuration schema", "finalize_task_ids": ["T3"]}
            ],
            "orphan_tasks": [],
            "completeness_notes": "All plan steps mapped to tasks.",
            "coverage_complete": true
          }
          ```
        - Preserve information that strong existing artifacts already capture well: execution ordering, watch-outs, reviewer checkpoints, and practical context.
        - The structured output should be self-contained: an executor reading only `finalize.json` should have everything needed to work.
        - Keep the task count proportional to the work. A simple 1-2 file fix should be 2 tasks: (1) apply the fix, (2) run tests. Do NOT create separate "inspect" or "read" tasks for simple changes — the executor can read and fix in one step. Only create more tasks when the work has genuinely independent stages.
        - The FINAL task MUST always be to run tests and verify the changes work. If specific test IDs or commands are mentioned in the original task, include them. Otherwise, the executor should find and run the tests most relevant to the files changed. If any test fails, read the error, fix the code, and re-run until they pass. Do NOT create new test files — run the project's existing test suite. Additionally, the executor should write a short throwaway script that reproduces the specific bug described in the task, run it to confirm the fix works, then delete the script.

> AGENT

Reading the idea doc and key source files to build the execution briefing.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/idea-doc-mode.txt"
}
```

> TOOL

tool_result Read
```
1	v0.15.0 — doc mode (metaplan): plan-as-output instead of code-as-output
2	
3	## Goal
4	Introduce a `--mode doc` (a.k.a. metaplan mode) where the executor produces a
5	structured plan document instead of code changes. Same harness, same phases,
6	same flag/gate machinery — only the executor's tool surface and output schema
7	change. Use case: plan-of-plans, design docs, RFCs, milestone breakdowns,
8	research write-ups. Anything where the deliverable is words on disk, not a diff.
9	
10	## Motivation
11	Today megaplan only knows how to ship code — execute writes files in the repo,
12	audit compares claimed paths against `git status`, review measures success
13	against criteria like "tsc clean" and "tests pass." When the artifact we want
14	is a plan document (e.g. the `state_management_refactor_plan.md` we just wrote
15	by hand, or the per-milestone idea files I'm seeding into `~/Documents/reigh-megaplan-dev/ideas/`),
16	megaplan can't help — its critique/gate/review loop is tuned for code.
17	
18	If we add doc mode, the whole prep → plan → critique → gate → revise loop
19	applies to thinking work too: the gate forces resolution of every blocking
20	critique flag against the document; review checks the doc against success
21	criteria. The model gets the same anti-rubber-stamp pressure on its writing
22	that it gets on its code.
23	
24	## What stays the same
25	- All phases (prep, plan, critique, gate, revise, finalize, execute, review).
26	- Robustness levels (light/standard/heavy).
27	- Flag taxonomy, dispute/accept_tradeoff resolution, rubber-stamp checks.
28	- Override commands (force-proceed, abort, replan, add-note).
29	- Session/rollout management, trusted-container env, batch execution.
30	- Critique prompts at the plan level — critiquing a plan is the same activity
31	  whether the plan ships code or ships a doc.
32	
33	## What varies per phase
34	
35	### init
36	- New flag: `--mode {code,doc}` (default `code`).
37	- Mode persists in plan meta (`plan.json` → `mode: "doc"`). All later phases
38	  read it from there.
39	- New flag: `--output <path>` for doc mode. Required. Path is relative to
40	  project_dir. Single output file — multi-file docs are out of scope for v0.15.
41	
42	### prep
43	- Unchanged for code mode.
44	- For doc mode: prep gathers research instead of repo orientation. The prep
45	  prompt is repointed to ask "what sources, prior art, related docs should
46	  inform this document?" — sense-check items become "did you read X?" rather
47	  than "did you find the relevant module?"
48	
49	### plan
50	- Plan output schema is unchanged at the top level (steps, tasks, success
51	  criteria, sense checks).
52	- Tasks in doc mode have a different shape under the hood: instead of
53	  `files_changed: [paths]`, they have `sections_written: [section_ids]`.
54	  The plan-step prompt enumerates the sections of the target document
55	  (introduction, problem statement, proposed solution, milestones, …) and
56	  the executor's job is to write each section.
57	
58	### critique
59	- Same machinery. Critique flags target plan structure, success-criteria
60	  calibration, scope creep — identical to code mode.
61	- Add a category `doc-quality` (alongside `code-quality`, `security`, etc.)
62	  for flags about clarity, audience-fit, missing rationale, undefended
63	  claims. Doc-mode critiques skew this way; code-mode critiques rarely use it.
64	
65	### gate
66	- Identical. The gate doesn't care what the executor will produce; it judges
67	  the plan's readiness.
68	
69	### revise → finalize
70	- Identical.
71	
72	### execute
73	- This is the biggest change.
74	- Tool surface: codex/claude is told it's authoring a document. Its only
75	  filesystem tool is "write to the configured output path." File creation
76	  outside that path is rejected upstream.
77	- Output schema: `task_updates[].files_changed` is replaced with
78	  `task_updates[].sections_written: [section_id]`. Tasks have status
79	  done/skipped/blocked as today.
80	- The executor returns the rendered section text, not a diff. The harness
81	  assembles sections in plan-order into the output file at the end of the
82	  batch. (This is how we avoid concurrent writers fighting over the same
83	  file across batches.)
84	- Per-batch behavior unchanged: each batch covers some tasks, writes its
85	  evidence JSON, transitions to the next.
86	
87	### audit (post-execute)
88	- For code mode: today's `validate_execution_evidence` (git status diff,
89	  path normalization, sense-check acks).
90	- For doc mode: replace the git-status comparison with:
91	  - "all sections in the plan are present in the output file"
92	  - "no sections in the output file are unclaimed by any task"
93	  - "output file exists and is non-empty"
94	  - "executor's claimed `sections_written` match what the harness assembled"
95	- Sense-check acknowledgment validation is unchanged.
96	
97	### review
98	- Code mode: today's review (tests pass, types clean, success criteria met).
99	- Doc mode: review reads the output file and judges it against the success
100	  criteria. `must` criteria become statements like "the doc names every
101	  blocking risk" rather than "tsc clean." Review's prompt is reworded to
102	  treat the deliverable as text, not a working system.
103	- Same priority machinery (must/should/info), same `needs_rework` loop.
104	
105	## Wiring details
106	
107	### Mode plumbing
108	- `plan.json` gains `mode: "code" | "doc"` and (for doc mode) `output_path`.
109	- Workers receive mode in their context dict.
110	- Prompt files split by mode: `prompts/prep_doc.py`, `prompts/execute_doc.py`,
111	  `prompts/review_doc.py`. Other prompts stay shared.
112	- `evaluation.validate_execution_evidence` branches on mode at the top.
113	
114	### Output schema
115	- New `schemas/execution_doc.json` mirrors `schemas/execution.json` but with
116	  `sections_written` instead of `files_changed`.
117	- `merge.py` validation accepts the doc schema when mode is doc.
118	
119	### Section assembly
120	- New `megaplan/doc_assembly.py`: takes the per-batch executor outputs,
121	  orders sections by plan position, writes the assembled file at finalize-end.
122	- Idempotent: running execute twice on the same plan replaces the file.
123	  No partial writes — assemble in a temp file, then atomic rename.
124	
125	## CLI shape
126	
127	```
128	megaplan init --project-dir . --mode doc \
129	              --output docs/state_management_refactor_plan.md \
130	              "Plan a 6-week refactor of state management..."
131	```
132	
133	Everything else is unchanged. `megaplan status` shows `mode: doc` and
134	`output_path` in the summary.
135	
136	## Out of scope (v0.15.0)
137	- Multi-file doc output (one plan → one file in v0.15).
138	- Mixed-mode plans (a plan that ships both code and a doc).
139	- Doc-mode-aware loop-init / loop-execute. Loop mode stays code-only for now.
140	- Migrating existing code-mode prompts to use the new schema branching —
141	  add the branch, don't rewrite working prompts.
142	
143	## Migration / compatibility
144	- Existing plans with no `mode` field default to `code`. No retroactive change.
145	- Existing tests pass unchanged (they all hit code mode).
146	- New tests cover: doc-mode plan init, doc execute writes the file, audit
147	  catches missing sections, audit catches sections not in plan, review
148	  judges doc against criteria.
149	
150	## Success criteria (verifiable)
151	- `megaplan init --mode doc --output X "..."` produces a plan with `mode: doc`.
152	- Running the full loop on a doc-mode plan produces a non-empty file at the
153	  configured output path.
154	- Audit rejects an executor that claims a section not in the plan.
155	- Audit rejects an executor that skips a section without marking the task
156	  blocked/skipped.
157	- Review with a `must` criterion phrased about the doc's content can fail
158	  the doc and trigger needs_rework.
159	- All existing code-mode tests pass.
160	- pyproject.toml version is "0.15.0", CHANGELOG has the v0.15.0 entry.
161	
162	## Branch
163	`doc-mode-metaplan` off main.
164	
165	## Working directory
166	/Users/user_c042661f/Documents/megaplan
167
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/types.py"
}
```

> TOOL

tool_result Read
```
1	"""Type definitions, constants, and exceptions for megaplan."""
2	
3	from __future__ import annotations
4	
5	from typing import Any, NotRequired, TypedDict
6	
7	
8	# ---------------------------------------------------------------------------
9	# States
10	# ---------------------------------------------------------------------------
11	
12	STATE_INITIALIZED = "initialized"
13	STATE_PREPPED = "prepped"
14	STATE_PLANNED = "planned"
15	STATE_CRITIQUED = "critiqued"
16	STATE_GATED = "gated"
17	STATE_FINALIZED = "finalized"
18	STATE_EXECUTED = "executed"
19	STATE_DONE = "done"
20	STATE_ABORTED = "aborted"
21	TERMINAL_STATES = {STATE_DONE, STATE_ABORTED}
22	
23	
24	# ---------------------------------------------------------------------------
25	# TypedDicts
26	# ---------------------------------------------------------------------------
27	
28	class PlanConfig(TypedDict, total=False):
29	    project_dir: str
30	    auto_approve: bool
31	    robustness: str
32	    agents: dict[str, str]
33	
34	
35	class PlanMeta(TypedDict, total=False):
36	    significant_counts: list[int]
37	    weighted_scores: list[float]
38	    plan_deltas: list[float | None]
39	    recurring_critiques: list[str]
40	    total_cost_usd: float
41	    overrides: list[dict[str, Any]]
42	    notes: list[dict[str, Any]]
43	    user_approved_gate: bool
44	
45	
46	class SessionInfo(TypedDict, total=False):
47	    id: str
48	    mode: str
49	    created_at: str
50	    last_used_at: str
51	    refreshed: bool
52	
53	
54	class ActiveStep(TypedDict, total=False):
55	    step: str
56	    agent: str
57	    mode: str
58	    model: str
59	    run_id: str
60	    session_id: str
61	    started_at: str
62	
63	
64	class PlanVersionRecord(TypedDict, total=False):
65	    version: int
66	    file: str
67	    hash: str
68	    timestamp: str
69	
70	
71	class HistoryEntry(TypedDict, total=False):
72	    step: str
73	    timestamp: str
74	    duration_ms: int
75	    cost_usd: float
76	    result: str
77	    session_mode: str
78	    session_id: str
79	    agent: str
80	    output_file: str
81	    artifact_hash: str
82	    finalize_hash: str
83	    raw_output_file: str
84	    message: str
85	    flags_count: int
86	    flags_addressed: list[str]
87	    recommendation: str
88	    approval_mode: str
89	    environment: dict[str, bool]
90	
91	
92	class ClarificationRecord(TypedDict, total=False):
93	    refined_idea: str
94	    intent_summary: str
95	    questions: list[str]
96	
97	
98	class LastGateRecord(TypedDict, total=False):
99	    recommendation: str
100	    rationale: str
101	    signals_assessment: str
102	    warnings: list[str]
103	    settled_decisions: list["SettledDecision"]
104	    passed: bool
105	    preflight_results: dict[str, bool]
106	    orchestrator_guidance: str
107	
108	
109	class PlanState(TypedDict):
110	    name: str
111	    idea: str
112	    current_state: str
113	    iteration: int
114	    created_at: str
115	    config: PlanConfig
116	    sessions: dict[str, SessionInfo]
117	    plan_versions: list[PlanVersionRecord]
118	    history: list[HistoryEntry]
119	    meta: PlanMeta
120	    last_gate: LastGateRecord
121	    active_step: NotRequired[ActiveStep]
122	    clarification: NotRequired[ClarificationRecord]
123	
124	
125	class _FlagRecordRequired(TypedDict):
126	    id: str
127	    concern: str
128	    category: str
129	    status: str
130	
131	
132	class FlagRecord(_FlagRecordRequired, total=False):
133	    severity_hint: str
134	    evidence: str
135	    raised_in: str
136	    severity: str
137	    verified: bool
138	    verified_in: str
139	    addressed_in: str
140	
141	
142	class FlagRegistry(TypedDict):
143	    flags: list[FlagRecord]
144	
145	
146	class GateCheckResult(TypedDict):
147	    passed: bool
148	    criteria_check: dict[str, Any]
149	    preflight_results: dict[str, bool]
150	    unresolved_flags: list[FlagRecord]
151	
152	
153	class SettledDecision(TypedDict, total=False):
154	    id: str
155	    decision: str
156	    rationale: str
157	
158	
159	class GatePayload(TypedDict):
160	    recommendation: str
161	    rationale: str
162	    signals_assessment: str
163	    warnings: list[str]
164	    settled_decisions: list[SettledDecision]
165	
166	
167	class GateArtifact(TypedDict, total=False):
168	    passed: bool
169	    criteria_check: dict[str, Any]
170	    preflight_results: dict[str, bool]
171	    unresolved_flags: list[FlagRecord]
172	    recommendation: str
173	    rationale: str
174	    signals_assessment: str
175	    warnings: list[str]
176	    settled_decisions: list[SettledDecision]
177	    override_forced: bool
178	    orchestrator_guidance: str
179	    robustness: str
180	    signals: dict[str, Any]
181	
182	
183	class GateSignals(TypedDict, total=False):
184	    robustness: str
185	    signals: dict[str, Any]
186	    warnings: list[str]
187	
188	
189	class StepResponse(TypedDict, total=False):
190	    success: bool
191	    step: str
192	    summary: str
193	    artifacts: list[str]
194	    next_step: str | None
195	    state: str
196	    auto_approve: bool
197	    robustness: str
198	    iteration: int
199	    plan: str
200	    plan_dir: str
201	    questions: list[str]
202	    verified_flags: list[str]
203	    open_flags: list[str]
204	    scope_creep_flags: list[str]
205	    warnings: list[str]
206	    files_changed: list[str]
207	    deviations: list[str]
208	    user_approved_gate: bool
209	    issues: list[str]
210	    valid_next: list[str]
211	    mode: str
212	    installed: list[dict[str, Any]]
213	    config_path: str
214	    routing: dict[str, str]
215	    raw_config: dict[str, Any]
216	    action: str
217	    key: str
218	    value: str
219	    skipped: bool
220	    file: str
221	    plans: list[dict[str, Any]]
222	    recommendation: str
223	    signals: dict[str, Any]
224	    rationale: str
225	    signals_assessment: str
226	    orchestrator_guidance: str
227	    passed: bool
228	    criteria_check: dict[str, Any]
229	    preflight_results: dict[str, bool]
230	    unresolved_flags: list[Any]
231	    error: str
232	    message: str
233	    details: dict[str, Any]
234	    agent_fallback: dict[str, str]
235	
236	
237	class DebtEntry(TypedDict):
238	    id: str
239	    subsystem: str
240	    concern: str
241	    flag_ids: list[str]
242	    plan_ids: list[str]
243	    occurrence_count: int
244	    created_at: str
245	    updated_at: str
246	    resolved: bool
247	    resolved_by: str | None
248	    resolved_at: str | None
249	
250	
251	class DebtRegistry(TypedDict):
252	    entries: list[DebtEntry]
253	
254	
255	# ---------------------------------------------------------------------------
256	# Constants
257	# ---------------------------------------------------------------------------
258	
259	FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
260	FLAG_VALID_STATUSES = {
261	    "open", "addressed", "disputed", "verified",
262	    "accepted_tradeoff", "gate_disputed",
263	}
264	DEBT_ESCALATION_THRESHOLD = 3
265	MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"
266	
267	DEFAULT_AGENT_ROUTING: dict[str, str] = {
268	    "plan": "claude",
269	    "prep": "claude",
270	    "critique": "codex",
271	    "revise": "claude",
272	    "gate": "claude",
273	    "finalize": "claude",
274	    "execute": "codex",
275	    "loop_plan": "claude",
276	    "loop_execute": "codex",
277	    "review": "codex",
278	}
279	KNOWN_AGENTS = ["claude", "codex", "hermes"]
280	ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
281	def parse_agent_spec(spec: str) -> tuple[str, str | None]:
282	    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
283	    if ":" in spec:
284	        agent, model = spec.split(":", 1)
285	        return agent, model
286	    return spec, None
287	
288	
289	SCOPE_CREEP_TERMS = (
290	    "scope creep",
291	    "out of scope",
292	    "beyond the original idea",
293	    "beyond original idea",
294	    "beyond user intent",
295	    "expanded scope",
296	)
297	
298	DEFAULTS = {
299	    "execution.auto_approve": False,
300	    "execution.robustness": "standard",
301	    "execution.worker_timeout_seconds": 7200,
302	    "execution.max_review_rework_cycles": 3,
303	    "execution.max_robust_review_rework_cycles": 2,
304	    "execution.max_execute_no_progress": 3,
305	    "orchestration.max_critique_concurrency": 2,
306	    "orchestration.mode": "subagent",
307	}
308	
309	_SETTABLE_BOOL = {
310	    "execution.auto_approve",
311	}
312	
313	_SETTABLE_ENUM = {
314	    "execution.robustness": ROBUSTNESS_LEVELS,
315	}
316	
317	_SETTABLE_NUMERIC = {
318	    "execution.worker_timeout_seconds",
319	    "execution.max_review_rework_cycles",
320	    "execution.max_robust_review_rework_cycles",
321	    "execution.max_execute_no_progress",
322	    "orchestration.max_critique_concurrency",
323	}
324	
325	
326	# ---------------------------------------------------------------------------
327	# Exception
328	# ---------------------------------------------------------------------------
329	
330	class CliError(Exception):
331	    def __init__(
332	        self,
333	        code: str,
334	        message: str,
335	        *,
336	        valid_next: list[str] | None = None,
337	        extra: dict[str, Any] | None = None,
338	        exit_code: int = 1,
339	    ) -> None:
340	        super().__init__(message)
341	        self.code = code
342	        self.message = message
343	        self.valid_next = valid_next or []
344	        self.extra = extra or {}
345	        self.exit_code = exit_code
346
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 800,
  "limit": 50
}
```

> TOOL

tool_result Read
```
800	# ---------------------------------------------------------------------------
801	
802	def build_parser() -> argparse.ArgumentParser:
803	    parser = argparse.ArgumentParser(description="Megaplan orchestration CLI")
804	    subparsers = parser.add_subparsers(dest="command", required=True)
805	
806	    setup_parser = subparsers.add_parser("setup", help="Install megaplan into agent configs (global by default)")
807	    setup_parser.add_argument("--local", action="store_true", help="Install AGENTS.md into a project instead of global agent configs")
808	    setup_parser.add_argument("--target-dir", help="Directory to install into (default: cwd, implies --local)")
809	    setup_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
810	
811	    init_parser = subparsers.add_parser("init")
812	    init_parser.add_argument("--project-dir", required=True)
813	    init_parser.add_argument("--name")
814	    init_parser.add_argument("--auto-approve", action="store_true", default=None)
815	    init_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
816	    init_parser.add_argument("--hermes", nargs="?", const="", default=None,
817	                             help="Use Hermes agent for all phases. Optional: specify default model")
818	    init_parser.add_argument("--phase-model", action="append", default=[],
819	                             help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
820	    init_parser.add_argument("idea")
821	
822	    list_parser = subparsers.add_parser("list")
823	    list_parser.add_argument("--all", action="store_true",
824	                             help="Search all .megaplan directories system-wide (~)")
825	    list_parser.add_argument("--no-tree", action="store_true",
826	                             help="Only show plans from the current directory (default includes parent + child)")
827	    list_parser.add_argument("--include-done", action="store_true",
828	                             help="Include terminal plans (done/aborted); excluded by default")
829	    list_parser.add_argument("--status", dest="filter_status",
830	                             help="Filter by state (e.g. 'done', 'finalized', 'executed', or comma-separated 'planned,critiqued')")
831	    list_parser.add_argument("--summary", action="store_true",
832	                             help="Show count breakdown by state")
833	
834	    for name in ["status", "audit", "progress", "watch"]:
835	        step_parser = subparsers.add_parser(name)
836	        step_parser.add_argument("--plan")
837	
838	    for name in ["plan", "prep", "critique", "revise", "gate", "finalize", "execute", "review"]:
839	        step_parser = subparsers.add_parser(name)
840	        step_parser.add_argument("--plan")
841	        step_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
842	        step_parser.add_argument("--hermes", nargs="?", const="", default=None,
843	                                 help="Use Hermes agent for all phases. Optional: specify default model (e.g. --hermes anthropic/claude-sonnet-4.6)")
844	        step_parser.add_argument("--phase-model", action="append", default=[],
845	                                 help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
846	        step_parser.add_argument("--fresh", action="store_true")
847	        step_parser.add_argument("--persist", action="store_true")
848	        step_parser.add_argument("--ephemeral", action="store_true")
849	        if name == "execute":
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/schemas.py"
}
```

> TOOL

tool_result Read
```
1	"""JSON schema definitions for megaplan step outputs."""
2	
3	from __future__ import annotations
4	
5	from typing import Any
6	
7	
8	SCHEMAS: dict[str, dict[str, Any]] = {
9	    "plan.json": {
10	        "type": "object",
11	        "properties": {
12	            "plan": {"type": "string"},
13	            "questions": {"type": "array", "items": {"type": "string"}},
14	            "success_criteria": {
15	                "type": "array",
16	                "items": {
17	                    "type": "object",
18	                    "properties": {
19	                        "criterion": {"type": "string"},
20	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
21	                    },
22	                    "required": ["criterion", "priority"],
23	                },
24	            },
25	            "assumptions": {"type": "array", "items": {"type": "string"}},
26	        },
27	        "required": ["plan", "questions", "success_criteria", "assumptions"],
28	    },
29	    "prep.json": {
30	        "type": "object",
31	        "properties": {
32	            "skip": {"type": "boolean"},
33	            "task_summary": {"type": "string"},
34	            "key_evidence": {
35	                "type": "array",
36	                "items": {
37	                    "type": "object",
38	                    "properties": {
39	                        "point": {"type": "string"},
40	                        "source": {"type": "string"},
41	                        "relevance": {"type": "string", "enum": ["high", "medium", "low"]},
42	                    },
43	                    "required": ["point", "source", "relevance"],
44	                },
45	            },
46	            "relevant_code": {
47	                "type": "array",
48	                "items": {
49	                    "type": "object",
50	                    "properties": {
51	                        "file_path": {"type": "string"},
52	                        "why": {"type": "string"},
53	                        "functions": {"type": "array", "items": {"type": "string"}},
54	                    },
55	                    "required": ["file_path", "why", "functions"],
56	                },
57	            },
58	            "test_expectations": {
59	                "type": "array",
60	                "items": {
61	                    "type": "object",
62	                    "properties": {
63	                        "test_id": {"type": "string"},
64	                        "what_it_checks": {"type": "string"},
65	                        "status": {"type": "string", "enum": ["fail_to_pass", "pass_to_pass"]},
66	                    },
67	                    "required": ["test_id", "what_it_checks", "status"],
68	                },
69	            },
70	            "constraints": {"type": "array", "items": {"type": "string"}},
71	            "suggested_approach": {"type": "string"},
72	        },
73	        "required": [
74	            "skip",
75	            "task_summary",
76	            "key_evidence",
77	            "relevant_code",
78	            "test_expectations",
79	            "constraints",
80	            "suggested_approach",
81	        ],
82	    },
83	    "revise.json": {
84	        "type": "object",
85	        "properties": {
86	            "plan": {"type": "string"},
87	            "changes_summary": {"type": "string"},
88	            "flags_addressed": {"type": "array", "items": {"type": "string"}},
89	            "assumptions": {"type": "array", "items": {"type": "string"}},
90	            "success_criteria": {
91	                "type": "array",
92	                "items": {
93	                    "type": "object",
94	                    "properties": {
95	                        "criterion": {"type": "string"},
96	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
97	                    },
98	                    "required": ["criterion", "priority"],
99	                },
100	            },
101	            "questions": {"type": "array", "items": {"type": "string"}},
102	        },
103	        "required": [
104	            "plan",
105	            "changes_summary",
106	            "flags_addressed",
107	            "assumptions",
108	            "success_criteria",
109	            "questions",
110	        ],
111	    },
112	    "gate.json": {
113	        "type": "object",
114	        "properties": {
115	            "recommendation": {
116	                "type": "string",
117	                "enum": ["PROCEED", "ITERATE", "ESCALATE"],
118	            },
119	            "rationale": {"type": "string"},
120	            "signals_assessment": {"type": "string"},
121	            "warnings": {"type": "array", "items": {"type": "string"}},
122	            "settled_decisions": {
123	                "type": "array",
124	                "items": {
125	                    "type": "object",
126	                    "properties": {
127	                        "id": {"type": "string"},
128	                        "decision": {"type": "string"},
129	                        "rationale": {"type": "string"},
130	                    },
131	                    "required": ["id", "decision", "rationale"],
132	                },
133	            },
134	            "flag_resolutions": {
135	                "type": "array",
136	                "items": {
137	                    "type": "object",
138	                    "properties": {
139	                        "flag_id": {"type": "string"},
140	                        "action": {"type": "string", "enum": ["dispute", "accept_tradeoff"]},
141	                        "evidence": {"type": "string"},
142	                        "rationale": {"type": "string"},
143	                    },
144	                    "required": ["flag_id", "action", "evidence", "rationale"],
145	                },
146	            },
147	            "accepted_tradeoffs": {
148	                "type": "array",
149	                "items": {
150	                    "type": "object",
151	                    "properties": {
152	                        "flag_id": {"type": "string"},
153	                        "concern": {"type": "string"},
154	                        "subsystem": {"type": "string"},
155	                        "rationale": {"type": "string"},
156	                    },
157	                    "required": ["flag_id", "concern", "subsystem", "rationale"],
158	                },
159	            },
160	        },
161	        "required": [
162	            "recommendation",
163	            "rationale",
164	            "signals_assessment",
165	            "warnings",
166	            "settled_decisions",
167	            "flag_resolutions",
168	            "accepted_tradeoffs",
169	        ],
170	    },
171	    "critique.json": {
172	        "type": "object",
173	        "properties": {
174	            "checks": {
175	                "type": "array",
176	                "items": {
177	                    "type": "object",
178	                    "properties": {
179	                        "id": {"type": "string"},
180	                        "question": {"type": "string"},
181	                        "findings": {
182	                            "type": "array",
183	                            "items": {
184	                                "type": "object",
185	                                "properties": {
186	                                    "detail": {"type": "string"},
187	                                    "flagged": {"type": "boolean"},
188	                                },
189	                                "required": ["detail", "flagged"],
190	                            },
191	                        },
192	                    },
193	                    "required": ["id", "question", "findings"],
194	                },
195	            },
196	            "flags": {
197	                "type": "array",
198	                "items": {
199	                    "type": "object",
200	                    "properties": {
201	                        "id": {"type": "string"},
202	                        "concern": {"type": "string"},
203	                        "category": {
204	                            "type": "string",
205	                            "enum": [
206	                                "correctness",
207	                                "security",
208	                                "completeness",
209	                                "performance",
210	                                "maintainability",
211	                                "other",
212	                            ],
213	                        },
214	                        "severity_hint": {
215	                            "type": "string",
216	                            "enum": ["likely-significant", "likely-minor", "uncertain"],
217	                        },
218	                        "evidence": {"type": "string"},
219	                    },
220	                    "required": ["id", "concern", "category", "severity_hint", "evidence"],
221	                },
222	            },
223	            "verified_flag_ids": {"type": "array", "items": {"type": "string"}},
224	            "disputed_flag_ids": {"type": "array", "items": {"type": "string"}},
225	        },
226	        "required": ["checks", "flags", "verified_flag_ids", "disputed_flag_ids"],
227	    },
228	"finalize.json": {
229	        "type": "object",
230	        "properties": {
231	            "tasks": {
232	                "type": "array",
233	                "items": {
234	                    "type": "object",
235	                    "properties": {
236	                        "id": {"type": "string"},
237	                        "description": {"type": "string"},
238	                        "depends_on": {"type": "array", "items": {"type": "string"}},
239	                        "status": {"type": "string", "enum": ["pending", "done", "skipped"]},
240	                        "executor_notes": {"type": "string"},
241	                        "files_changed": {"type": "array", "items": {"type": "string"}},
242	                        "commands_run": {"type": "array", "items": {"type": "string"}},
243	                        "evidence_files": {"type": "array", "items": {"type": "string"}},
244	                        "reviewer_verdict": {"type": "string"},
245	                    },
246	                    "required": [
247	                        "id",
248	                        "description",
249	                        "depends_on",
250	                        "status",
251	                        "executor_notes",
252	                        "files_changed",
253	                        "commands_run",
254	                        "evidence_files",
255	                        "reviewer_verdict",
256	                    ],
257	                },
258	            },
259	            "watch_items": {"type": "array", "items": {"type": "string"}},
260	            "sense_checks": {
261	                "type": "array",
262	                "items": {
263	                    "type": "object",
264	                    "properties": {
265	                        "id": {"type": "string"},
266	                        "task_id": {"type": "string"},
267	                        "question": {"type": "string"},
268	                        "executor_note": {"type": "string"},
269	                        "verdict": {"type": "string"},
270	                    },
271	                    "required": ["id", "task_id", "question", "executor_note", "verdict"],
272	                },
273	            },
274	            "meta_commentary": {"type": "string"},
275	            "validation": {
276	                "type": "object",
277	                "properties": {
278	                    "plan_steps_covered": {
279	                        "type": "array",
280	                        "items": {
281	                            "type": "object",
282	                            "properties": {
283	                                "plan_step_summary": {"type": "string"},
284	                                "finalize_task_ids": {
285	                                    "type": "array",
286	                                    "items": {"type": "string"},
287	                                },
288	                            },
289	                            "required": ["plan_step_summary", "finalize_task_ids"],
290	                        },
291	                    },
292	                    "orphan_tasks": {
293	                        "type": "array",
294	                        "items": {"type": "string"},
295	                    },
296	                    "completeness_notes": {"type": "string"},
297	                    "coverage_complete": {"type": "boolean"},
298	                },
299	                "required": [
300	                    "plan_steps_covered",
301	                    "orphan_tasks",
302	                    "completeness_notes",
303	                    "coverage_complete",
304	                ],
305	            },
306	            "baseline_test_failures": {
307	                "type": ["array", "null"],
308	                "items": {"type": "string"},
309	            },
310	            "baseline_test_command": {"type": ["string", "null"]},
311	            "baseline_test_note": {"type": "string"},
312	        },
313	        "required": ["tasks", "watch_items", "sense_checks", "meta_commentary", "validation"],
314	    },
315	    "execution.json": {
316	        "type": "object",
317	        "properties": {
318	            "output": {"type": "string"},
319	            "files_changed": {"type": "array", "items": {"type": "string"}},
320	            "commands_run": {"type": "array", "items": {"type": "string"}},
321	            "deviations": {"type": "array", "items": {"type": "string"}},
322	            "task_updates": {
323	                "type": "array",
324	                "items": {
325	                    "type": "object",
326	                    "properties": {
327	                        "task_id": {"type": "string"},
328	                        "status": {"type": "string", "enum": ["done", "skipped"]},
329	                        "executor_notes": {"type": "string"},
330	                        "files_changed": {"type": "array", "items": {"type": "string"}},
331	                        "commands_run": {"type": "array", "items": {"type": "string"}},
332	                    },
333	                    "required": ["task_id", "status", "executor_notes", "files_changed", "commands_run"],
334	                },
335	            },
336	            "sense_check_acknowledgments": {
337	                "type": "array",
338	                "items": {
339	                    "type": "object",
340	                    "properties": {
341	                        "sense_check_id": {"type": "string"},
342	                        "executor_note": {"type": "string"},
343	                    },
344	                    "required": ["sense_check_id", "executor_note"],
345	                },
346	            },
347	        },
348	        "required": ["output", "files_changed", "commands_run", "deviations", "task_updates", "sense_check_acknowledgments"],
349	    },
350	    "loop_plan.json": {
351	        "type": "object",
352	        "properties": {
353	            "spec_updates": {
354	                "type": "object",
355	                "additionalProperties": True,
356	            },
357	            "next_action": {"type": "string"},
358	            "reasoning": {"type": "string"},
359	        },
360	        "required": ["spec_updates", "next_action", "reasoning"],
361	    },
362	    "loop_execute.json": {
363	        "type": "object",
364	        "properties": {
365	            "diagnosis": {"type": "string"},
366	            "fix_description": {"type": "string"},
367	            "files_to_change": {"type": "array", "items": {"type": "string"}},
368	            "confidence": {"type": "string"},
369	            "outcome": {"type": "string"},
370	            "should_pause": {"type": "boolean"},
371	        },
372	        "required": ["diagnosis", "fix_description", "files_to_change", "confidence", "outcome", "should_pause"],
373	    },
374	    "review.json": {
375	        "type": "object",
376	        "properties": {
377	            "review_verdict": {"type": "string", "enum": ["approved", "needs_rework"]},
378	            "checks": {
379	                "type": "array",
380	                "items": {
381	                    "type": "object",
382	                    "properties": {
383	                        "id": {"type": "string"},
384	                        "question": {"type": "string"},
385	                        "guidance": {"type": "string"},
386	                        "findings": {
387	                            "type": "array",
388	                            "items": {
389	                                "type": "object",
390	                                "properties": {
391	                                    "detail": {"type": "string"},
392	                                    "flagged": {"type": "boolean"},
393	                                    "status": {"type": "string"},
394	                                    "evidence_file": {"type": "string"},
395	                                },
396	                                "required": ["detail", "flagged", "status", "evidence_file"],
397	                            },
398	                        },
399	                        "prior_findings": {
400	                            "type": "array",
401	                            "items": {
402	                                "type": "object",
403	                                "properties": {
404	                                    "detail": {"type": "string"},
405	                                    "flagged": {"type": "boolean"},
406	                                    "status": {"type": "string"},
407	                                },
408	                                "required": ["detail", "flagged", "status"],
409	                            },
410	                        },
411	                    },
412	                    "required": ["id", "question", "guidance", "findings", "prior_findings"],
413	                },
414	            },
415	            "pre_check_flags": {
416	                "type": "array",
417	                "items": {
418	                    "type": "object",
419	                    "properties": {
420	                        "id": {"type": "string"},
421	                        "check": {"type": "string"},
422	                        "detail": {"type": "string"},
423	                        "severity": {"type": "string"},
424	                        "evidence_file": {"type": "string"},
425	                    },
426	                    "required": ["id", "check", "detail", "severity", "evidence_file"],
427	                },
428	            },
429	            "verified_flag_ids": {"type": "array", "items": {"type": "string"}},
430	            "disputed_flag_ids": {"type": "array", "items": {"type": "string"}},
431	            "criteria": {
432	                "type": "array",
433	                "items": {
434	                    "type": "object",
435	                    "properties": {
436	                        "name": {"type": "string"},
437	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
438	                        "pass": {"type": "string", "enum": ["pass", "fail", "waived"]},
439	                        "evidence": {"type": "string"},
440	                    },
441	                    "required": ["name", "priority", "pass", "evidence"],
442	                },
443	            },
444	            "issues": {"type": "array", "items": {"type": "string"}},
445	            "rework_items": {
446	                "type": "array",
447	                "items": {
448	                    "type": "object",
449	                    "properties": {
450	                        "task_id": {"type": "string"},
451	                        "issue": {"type": "string"},
452	                        "expected": {"type": "string"},
453	                        "actual": {"type": "string"},
454	                        "evidence_file": {"type": "string"},
455	                        "flag_id": {"type": ["string", "null"]},
456	                        "source": {"type": ["string", "null"]},
457	                    },
458	                    "required": ["task_id", "issue", "expected", "actual", "evidence_file", "flag_id", "source"],
459	                },
460	            },
461	            "summary": {"type": "string"},
462	            "task_verdicts": {
463	                "type": "array",
464	                "items": {
465	                    "type": "object",
466	                    "properties": {
467	                        "task_id": {"type": "string"},
468	                        "reviewer_verdict": {"type": "string"},
469	                        "evidence_files": {"type": "array", "items": {"type": "string"}},
470	                    },
471	                    "required": ["task_id", "reviewer_verdict", "evidence_files"],
472	                },
473	            },
474	            "sense_check_verdicts": {
475	                "type": "array",
476	                "items": {
477	                    "type": "object",
478	                    "properties": {
479	                        "sense_check_id": {"type": "string"},
480	                        "verdict": {"type": "string"},
481	                    },
482	                    "required": ["sense_check_id", "verdict"],
483	                },
484	            },
485	        },
486	        "required": [
487	            "review_verdict",
488	            "checks",
489	            "pre_check_flags",
490	            "verified_flag_ids",
491	            "disputed_flag_ids",
492	            "criteria",
493	            "issues",
494	            "rework_items",
495	            "summary",
496	            "task_verdicts",
497	            "sense_check_verdicts",
498	        ],
499	    },
500	}
501	
502	
503	def _preserve_explicit_required(path: tuple[str, ...]) -> bool:
504	    # `review.rework_items[]` uses explicit required fields because OpenAI
505	    # structured outputs require every property key to appear in `required`.
506	    return path[-3:] == ("properties", "rework_items", "items")
507	
508	
509	def strict_schema(schema: Any, _path: tuple[str, ...] = ()) -> Any:
510	    if isinstance(schema, dict):
511	        updated = {key: strict_schema(value, _path + (key,)) for key, value in schema.items()}
512	        if updated.get("type") == "object":
513	            updated.setdefault("additionalProperties", False)
514	            if "properties" in updated and not _preserve_explicit_required(_path):
515	                updated["required"] = list(updated["properties"].keys())
516	        return updated
517	    if isinstance(schema, list):
518	        return [strict_schema(item, _path) for item in schema]
519	    return schema
520
```

> AGENT

Now let me read the remaining key files needed for the briefing.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 370,
  "limit": 80
}
```

> TOOL

tool_result Read
```
370	        "structure_warnings": structure_warnings,
371	    }
372	    atomic_write_json(plan_dir / meta_filename, meta)
373	    return resolved_plan_filename, meta_filename, meta
374	
375	
376	def _write_finalize_artifacts(plan_dir: Path, payload: dict[str, Any], state: PlanState) -> str:
377	    baseline = _capture_test_baseline(Path(state["config"]["project_dir"]), state.get("config", {}))
378	    payload.update(baseline)
379	    _ensure_verification_task(payload, state)
380	    _reconcile_validation_after_mutation(payload)
381	    atomic_write_json(plan_dir / "finalize.json", payload)
382	    atomic_write_json(plan_dir / "finalize_snapshot.json", payload)
383	    atomic_write_text(plan_dir / "final.md", render_final_md(payload))
384	    return sha256_file(plan_dir / "finalize.json")
385	
386	
387	def _reconcile_validation_after_mutation(payload: dict[str, Any]) -> None:
388	    """Ensure validation block is consistent with the (possibly mutated) task list.
389	
390	    After _ensure_verification_task() may have appended a task, update the
391	    validation block so orphan_tasks includes any handler-injected tasks.
392	    """
393	    validation = payload.get("validation")
394	    if not validation or not isinstance(validation, dict):
395	        return
396	    task_ids = {t["id"] for t in payload.get("tasks", []) if isinstance(t, dict)}
397	    covered_ids: set[str] = set()
398	    for entry in validation.get("plan_steps_covered", []):
399	        if isinstance(entry, dict):
400	            for tid in entry.get("finalize_task_ids", []):
401	                covered_ids.add(tid)
402	    orphan_ids = set(validation.get("orphan_tasks", []))
403	    for tid in task_ids:
404	        if tid not in covered_ids and tid not in orphan_ids:
405	            orphan_ids.add(tid)
406	    validation["orphan_tasks"] = sorted(orphan_ids)
407	
408	
409	def _validate_finalize_payload(plan_dir: Path, state: PlanState, worker: WorkerResult) -> None:
410	    payload = worker.payload
411	
412	    def _reject(message: str) -> None:
413	        _raise_step_validation_error(
414	            plan_dir=plan_dir, state=state, step="finalize",
415	            iteration=state["iteration"], worker=worker,
416	            code="invalid_finalize", message=message,
417	        )
418	
419	    tasks = payload.get("tasks")
420	    if not isinstance(tasks, list) or not tasks:
421	        _reject("Finalize output must include a non-empty `tasks` list.")
422	    if not isinstance(payload.get("sense_checks"), list):
423	        _reject("Finalize output must include a `sense_checks` list.")
424	    if not isinstance(payload.get("watch_items"), list):
425	        _reject("Finalize output must include a `watch_items` list.")
426	    for index, task in enumerate(tasks, start=1):
427	        tid = task.get("id", index) if isinstance(task, dict) else index
428	        if not isinstance(task, dict):
429	            _reject(f"Finalize task {index} must be an object.")
430	        if not isinstance(task.get("id"), str) or not task["id"].strip():
431	            _reject(f"Finalize task {index} is missing a non-empty `id`.")
432	        if not isinstance(task.get("description"), str) or not task["description"].strip():
433	            _reject(f"Finalize task {tid} is missing a non-empty `description`.")
434	        if task.get("status") != "pending":
435	            _reject(f"Finalize task {tid} must start with status `pending`.")
436	
437	
438	def _build_gate_signals_artifact(
439	    plan_dir: Path,
440	    state: PlanState,
441	    *,
442	    iteration: int,
443	    root: Path,
444	) -> tuple[dict[str, Any], str, dict[str, Any]]:
445	    gate_signals = build_gate_signals(plan_dir, state, root=root)
446	    gate_checks = run_gate_checks(plan_dir, state, command_lookup=find_command)
447	    signals_artifact = {
448	        "robustness": gate_signals["robustness"],
449	        "signals": gate_signals["signals"],
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 710,
  "limit": 60
}
```

> TOOL

tool_result Read
```
710	        if isinstance(subsystem, str) and subsystem.strip():
711	            tradeoff["subsystem"] = subsystem
712	        merged_tradeoffs.append(tradeoff)
713	        existing_ids.add(flag_id)
714	    worker_payload["accepted_tradeoffs"] = merged_tradeoffs
715	
716	
717	def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
718	    ensure_runtime_layout(root)
719	    project_dir = Path(args.project_dir).expanduser().resolve()
720	    if not project_dir.exists() or not project_dir.is_dir():
721	        raise CliError("invalid_project_dir", f"Project directory does not exist: {project_dir}")
722	    robustness = getattr(args, "robustness", None)
723	    if robustness is None:
724	        robustness = get_effective("execution", "robustness")
725	    if robustness not in ROBUSTNESS_LEVELS:
726	        robustness = "standard"
727	    auto_approve_value = getattr(args, "auto_approve", None)
728	    if auto_approve_value is None:
729	        auto_approve_value = get_effective("execution", "auto_approve")
730	    auto_approve = bool(auto_approve_value)
731	    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
732	    plan_name = args.name or f"{slugify(args.idea)}-{timestamp}"
733	    plan_dir = plans_root(root) / plan_name
734	    if plan_dir.exists():
735	        raise CliError("duplicate_plan", f"Plan directory already exists: {plan_name}")
736	    plan_dir.mkdir(parents=True, exist_ok=False)
737	
738	    state: PlanState = {
739	        "name": plan_name,
740	        "idea": args.idea,
741	        "current_state": STATE_INITIALIZED,
742	        "iteration": 0,
743	        "created_at": now_utc(),
744	        "config": {
745	            "project_dir": str(project_dir),
746	            "auto_approve": auto_approve,
747	            "robustness": robustness,
748	            "agent": "hermes" if getattr(args, "hermes", None) is not None else "",
749	        },
750	        "sessions": {},
751	        "plan_versions": [],
752	        "history": [],
753	        "meta": {
754	            "significant_counts": [],
755	            "weighted_scores": [],
756	            "plan_deltas": [],
757	            "recurring_critiques": [],
758	            "total_cost_usd": 0.0,
759	            "overrides": [],
760	            "notes": [],
761	        },
762	        "last_gate": {},
763	    }
764	    append_history(
765	        state,
766	        make_history_entry(
767	            "init",
768	            duration_ms=0,
769	            cost_usd=0.0,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py",
  "offset": 100,
  "limit": 80
}
```

> TOOL

tool_result Read
```
100	    return paths
101	
102	
103	def is_rubber_stamp(text: str, *, strict: bool = False) -> bool:
104	    stripped = text.strip()
105	    normalized = normalize_text(text).strip(" .!?,;:")
106	    if normalized in _GENERIC_ACKS:
107	        return True
108	    if not strict:
109	        return False
110	    if len(stripped) <= _MIN_VERDICT_CHARS:
111	        return True
112	    words = stripped.split()
113	    if len(words) < _MIN_VERDICT_WORDS:
114	        return True
115	    unique_words = {word.lower() for word in words}
116	    return len(unique_words) < _MIN_VERDICT_UNIQUE_WORDS
117	
118	
119	def _is_perfunctory_ack(note: str) -> bool:
120	    return is_rubber_stamp(note, strict=False)
121	
122	
123	def validate_execution_evidence(finalize_data: dict[str, Any], project_dir: Path) -> dict[str, Any]:
124	    findings: list[str] = []
125	    files_claimed = sorted(
126	        {
127	            _normalize_repo_path(path, project_dir)
128	            for task in finalize_data.get("tasks", [])
129	            for path in task.get("files_changed", [])
130	            if isinstance(path, str) and path.strip()
131	        }
132	    )
133	
134	    if not (project_dir / ".git").exists():
135	        return {
136	            "findings": findings,
137	            "files_in_diff": [],
138	            "files_claimed": files_claimed,
139	            "skipped": True,
140	            "reason": "Project directory is not a git repository.",
141	        }
142	
143	    try:
144	        process = subprocess.run(
145	            ["git", "status", "--short"],
146	            cwd=str(project_dir),
147	            text=True,
148	            capture_output=True,
149	            timeout=30,
150	        )
151	    except FileNotFoundError:
152	        return {
153	            "findings": findings,
154	            "files_in_diff": [],
155	            "files_claimed": files_claimed,
156	            "skipped": True,
157	            "reason": "git not found on PATH.",
158	        }
159	    except subprocess.TimeoutExpired:
160	        return {
161	            "findings": findings,
162	            "files_in_diff": [],
163	            "files_claimed": files_claimed,
164	            "skipped": True,
165	            "reason": "git status timed out.",
166	        }
167	
168	    if process.returncode != 0:
169	        return {
170	            "findings": findings,
171	            "files_in_diff": [],
172	            "files_claimed": files_claimed,
173	            "skipped": True,
174	            "reason": f"git status failed: {process.stderr.strip() or process.stdout.strip()}",
175	        }
176	
177	    files_in_diff = sorted(_parse_git_status_paths(process.stdout))
178	    claimed_set = set(files_claimed)
179	    diff_set = set(files_in_diff)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py",
  "offset": 120,
  "limit": 60
}
```

> TOOL

tool_result Read
```
120	        issues.append(
121	            f"Advisory: task {task_id} was {before_status!r} on disk before merge but structured output set it to {after_status!r}. Structured output remains authoritative."
122	        )
123	
124	
125	def _stable_unique_strings(values: list[str]) -> list[str]:
126	    seen: set[str] = set()
127	    ordered: list[str] = []
128	    for value in values:
129	        if value in seen:
130	            continue
131	        seen.add(value)
132	        ordered.append(value)
133	    return ordered
134	
135	
136	def _build_aggregate_execution_payload(
137	    batch_payloads: list[dict[str, Any]],
138	    *,
139	    completed_batches: int,
140	    total_batches: int,
141	) -> dict[str, Any]:
142	    outputs = [
143	        f"Batch {index + 1}: {payload.get('output', '')}".strip()
144	        for index, payload in enumerate(batch_payloads)
145	    ]
146	    files_changed: list[str] = []
147	    commands_run: list[str] = []
148	    deviations: list[str] = []
149	    task_updates: list[dict[str, Any]] = []
150	    sense_check_acknowledgments: list[dict[str, Any]] = []
151	    for payload in batch_payloads:
152	        files_changed.extend(
153	            [path for path in payload.get("files_changed", []) if isinstance(path, str)]
154	        )
155	        commands_run.extend(
156	            [
157	                command
158	                for command in payload.get("commands_run", [])
159	                if isinstance(command, str)
160	            ]
161	        )
162	        deviations.extend(
163	            [issue for issue in payload.get("deviations", []) if isinstance(issue, str)]
164	        )
165	        task_updates.extend(
166	            [item for item in payload.get("task_updates", []) if isinstance(item, dict)]
167	        )
168	        sense_check_acknowledgments.extend(
169	            [
170	                item
171	                for item in payload.get("sense_check_acknowledgments", [])
172	                if isinstance(item, dict)
173	            ]
174	        )
175	    output = (
176	        f"Aggregated execute batches: completed {completed_batches}/{total_batches}."
177	    )
178	    if outputs:
179	        output = output + "\n" + "\n".join(outputs)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py",
  "offset": 30,
  "limit": 60
}
```

> TOOL

tool_result Read
```
30	
31	def _resolve_execute_approval_mode(
32	    *, auto_approve: bool, user_approved_gate: bool
33	) -> str:
34	    if auto_approve:
35	        return "auto_approve"
36	    if user_approved_gate:
37	        return "user_approved"
38	    return "manual"
39	
40	
41	def _reset_timeout_invalid_tasks(
42	    finalize_data: dict[str, Any],
43	    *,
44	    execution_audit: dict[str, Any],
45	    issues: list[str],
46	) -> list[str]:
47	    reset_reasons: dict[str, list[str]] = {}
48	    missing_task_ids = _check_done_task_evidence(
49	        finalize_data.get("tasks", []),
50	        issues=issues,
51	        should_classify=lambda task: True,
52	        has_evidence=lambda task: bool(task.get("files_changed")),
53	        has_advisory_evidence=lambda task: bool(task.get("commands_run")),
54	        missing_message="Done tasks missing both files_changed and commands_run during timeout recovery: ",
55	        advisory_message="Advisory: done tasks rely on commands_run without files_changed during timeout recovery: ",
56	    )
57	    for task_id in missing_task_ids:
58	        reset_reasons.setdefault(task_id, []).append(
59	            "missing both files_changed and commands_run"
60	        )
61	
62	    if not execution_audit.get("skipped"):
63	        files_in_diff = {
64	            _normalize_execute_claimed_path(path)
65	            for path in execution_audit.get("files_in_diff", [])
66	            if isinstance(path, str) and path.strip()
67	        }
68	        for task in finalize_data.get("tasks", []):
69	            if task.get("status") != "done":
70	                continue
71	            claimed_paths = [
72	                _normalize_execute_claimed_path(path)
73	                for path in task.get("files_changed", [])
74	                if isinstance(path, str) and path.strip()
75	            ]
76	            if claimed_paths and any(
77	                path not in files_in_diff for path in claimed_paths
78	            ):
79	                reset_reasons.setdefault(task["id"], []).append(
80	                    "claimed files not present in git status"
81	                )
82	
83	    for task in finalize_data.get("tasks", []):
84	        reasons = reset_reasons.get(task.get("id"))
85	        if not reasons:
86	            continue
87	        note_prefix = str(task.get("executor_notes", "")).strip()
88	        reset_note = (
89	            "Timeout recovery reset this task to pending because "
```

> TOOL

tool_use Glob
```json
{
  "pattern": "megaplan/prompts/*.py"
}
```

> TOOL

tool_result Glob
```
megaplan/prompts/finalize.py
megaplan/prompts/_shared.py
megaplan/prompts/__init__.py
megaplan/prompts/planning.py
megaplan/prompts/critique.py
megaplan/prompts/execute.py
megaplan/prompts/review.py
megaplan/prompts/gate.py
```

> AGENT

Let me check a few more files for the workers and hermes paths.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 40,
  "limit": 40
}
```

> TOOL

tool_result Read
```
40	    read_json,
41	    schemas_root,
42	)
43	from megaplan.prompts import create_claude_prompt, create_codex_prompt
44	
45	
46	_EXECUTE_STEPS = {"execute", "loop_execute"}
47	_CODEX_TEMPLATE_WRITE_STEPS = {"critique", "review"}
48	
49	# Shared mapping from step name to schema filename, used by both
50	# run_claude_step and run_codex_step.
51	STEP_SCHEMA_FILENAMES: dict[str, str] = {
52	    "plan": "plan.json",
53	    "prep": "prep.json",
54	    "revise": "revise.json",
55	    "critique": "critique.json",
56	    "gate": "gate.json",
57	    "finalize": "finalize.json",
58	    "execute": "execution.json",
59	    "loop_plan": "loop_plan.json",
60	    "loop_execute": "loop_execute.json",
61	    "review": "review.json",
62	}
63	
64	# Derive required keys per step from SCHEMAS so they aren't duplicated.
65	_STEP_REQUIRED_KEYS: dict[str, list[str]] = {
66	    step: SCHEMAS[filename].get("required", [])
67	    for step, filename in STEP_SCHEMA_FILENAMES.items()
68	}
69	
70	
71	@dataclass
72	class CommandResult:
73	    command: list[str]
74	    cwd: Path
75	    returncode: int
76	    stdout: str
77	    stderr: str
78	    duration_ms: int
79
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py",
  "offset": 280,
  "limit": 30
}
```

> TOOL

tool_result Read
```
280	    prompt_override: str | None = None,
281	) -> WorkerResult:
282	    """Run a megaplan phase using Hermes Agent via OpenRouter.
283	
284	    Structured output is enforced via the prompt (megaplan prompts already
285	    embed the JSON schema). The final response is parsed and validated.
286	    """
287	    if os.getenv(MOCK_ENV_VAR) == "1":
288	        return mock_worker_output(step, state, plan_dir, prompt_override=prompt_override)
289	
290	    from run_agent import AIAgent
291	    from hermes_state import SessionDB
292	
293	    project_dir = Path(state["config"]["project_dir"])
294	    schema_name = STEP_SCHEMA_FILENAMES[step]
295	    schema = read_json(schemas_root(root) / schema_name)
296	    output_path: Path | None = None
297	
298	    # Session management
299	    session_key = session_key_for(step, "hermes", model=model)
300	    session = state["sessions"].get(session_key, {})
301	    session_id = session.get("id") if not fresh else None
302	
303	    # Reload conversation history for session continuity
304	    conversation_history = None
305	    if session_id:
306	        try:
307	            db = SessionDB()
308	            conversation_history = db.get_messages_as_conversation(session_id)
309	        except Exception:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py",
  "offset": 625,
  "limit": 80
}
```

> TOOL

tool_result Read
```
625	    """Reconstruct an execute phase response from tool calls and git state.
626	
627	    When the model did the work via tools but couldn't produce the JSON
628	    report (e.g., response trapped in think tags, or timeout), build the
629	    response from what actually happened.
630	    """
631	    import subprocess
632	
633	    # Collect tool calls from messages
634	    tool_calls = []
635	    files_changed = set()
636	    commands_run = []
637	    for msg in messages:
638	        if msg.get("role") != "assistant":
639	            continue
640	        for tc in msg.get("tool_calls") or []:
641	            fn = tc.get("function", {})
642	            if not isinstance(fn, dict):
643	                continue
644	            name = fn.get("name", "")
645	            args_raw = fn.get("arguments", "{}")
646	            try:
647	                args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
648	            except (json.JSONDecodeError, TypeError):
649	                args = {}
650	            if not isinstance(args, dict):
651	                args = {}
652	
653	            tool_calls.append({"name": name, "args": args})
654	
655	            if name in ("write_file", "patch", "edit_file", "apply_patch"):
656	                path = args.get("path", "")
657	                if isinstance(path, str) and path:
658	                    # Make relative to project dir
659	                    try:
660	                        rel = str(Path(path).relative_to(project_dir))
661	                    except ValueError:
662	                        rel = path
663	                    files_changed.add(rel)
664	            elif name in ("terminal", "shell"):
665	                cmd = args.get("command", "")
666	                if isinstance(cmd, str) and cmd:
667	                    commands_run.append(cmd)
668	
669	    # Also check git diff for files changed
670	    try:
671	        diff_result = subprocess.run(
672	            ["git", "diff", "--name-only", "HEAD"],
673	            cwd=project_dir,
674	            capture_output=True, text=True, timeout=10, check=False,
675	        )
676	        if diff_result.returncode == 0:
677	            for line in diff_result.stdout.splitlines():
678	                if line.strip():
679	                    files_changed.add(line.strip())
680	    except Exception:
681	        pass
682	
683	    # Check for untracked files too
684	    try:
685	        status_result = subprocess.run(
686	            ["git", "status", "--porcelain"],
687	            cwd=project_dir,
688	            capture_output=True, text=True, timeout=10, check=False,
689	        )
690	        if status_result.returncode == 0:
691	            for line in status_result.stdout.splitlines():
692	                if line.startswith("?? ") or line.startswith("A  ") or line.startswith("M  "):
693	                    fname = line[3:].strip()
694	                    if fname and not fname.startswith(".megaplan/"):
695	                        files_changed.add(fname)
696	    except Exception:
697	        pass
698	
699	    if not tool_calls and not files_changed:
700	        return None  # Nothing happened, can't reconstruct
701	
702	    # Try to read checkpoint file for task updates
703	    task_updates = []
704	    checkpoint_files = sorted(plan_dir.glob("execution_batch_*.json"), reverse=True)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1330,
  "limit": 50
}
```

> TOOL

tool_result Read
```
1330	        if entry.get("step") == "review" and entry.get("result") == "needs_rework":
1331	            return True
1332	        if entry.get("step") == "execute":
1333	            return False
1334	    return False
1335	
1336	
1337	def handle_execute(root: Path, args: argparse.Namespace) -> StepResponse:
1338	    with load_plan_locked(root, args.plan, step="execute") as (plan_dir, state):
1339	        require_state(state, "execute", {STATE_FINALIZED})
1340	        if not args.confirm_destructive:
1341	            raise CliError("missing_confirmation", "Execute requires --confirm-destructive")
1342	        auto_approve = bool(state["config"].get("auto_approve", False))
1343	        if getattr(args, "user_approved", False):
1344	            state["meta"]["user_approved_gate"] = True
1345	            save_state(plan_dir, state)
1346	        if not auto_approve and not state["meta"].get("user_approved_gate", False):
1347	            raise CliError(
1348	                "missing_approval",
1349	                "Execute requires explicit user approval (--user-approved) when auto-approve is not set. The orchestrator must confirm with the user at the gate checkpoint before proceeding.",
1350	            )
1351	        agent, mode, refreshed, model = worker_module.resolve_agent_mode("execute", args)
1352	        # Force fresh session after review kickback to avoid prior-context bias
1353	        if not refreshed and _is_rework_reexecution(state):
1354	            refreshed = True
1355	        run_id = set_active_step(state, step="execute", agent=agent, mode=mode, model=model)
1356	        _emit_phase_notice("execute")
1357	        save_state(plan_dir, state)
1358	        try:
1359	            if getattr(args, "batch", None) is not None:
1360	                response = dispatch_execute_one_batch(
1361	                    root=root,
1362	                    plan_dir=plan_dir,
1363	                    state=state,
1364	                    args=args,
1365	                    batch_number=args.batch,
1366	                    auto_approve=auto_approve,
1367	                    agent=agent,
1368	                    mode=mode,
1369	                    refreshed=refreshed,
1370	                    model=model,
1371	                )
1372	            else:
1373	                response = dispatch_execute_auto_loop(
1374	                    root=root,
1375	                    plan_dir=plan_dir,
1376	                    state=state,
1377	                    args=args,
1378	                    auto_approve=auto_approve,
1379	                    agent=agent,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/__init__.py"
}
```

> TOOL

tool_result Read
```
1	"""Prompt builders for each megaplan step and dispatch tables."""
2	
3	from __future__ import annotations
4	
5	from functools import partial
6	from pathlib import Path
7	from typing import Callable
8	
9	from megaplan.types import CliError, PlanState
10	
11	from ._shared import (
12	    _debt_watch_lines,
13	    _escalated_debt_for_prompt,
14	    _finalize_debt_block,
15	    _gate_debt_block,
16	    _grouped_debt_for_prompt,
17	    _planning_debt_block,
18	    _render_prep_block,
19	    _resolve_prompt_root,
20	)
21	from .critique import (
22	    _critique_prompt,
23	    _revise_prompt,
24	    _write_critique_template,
25	)
26	from .execute import (
27	    _execute_approval_note,
28	    _execute_batch_prompt,
29	    _execute_nudges,
30	    _execute_prompt,
31	    _execute_rerun_guidance,
32	    _execute_review_block,
33	)
34	from .finalize import _finalize_prompt
35	from .gate import _collect_critique_summaries, _flag_summary, _gate_prompt
36	from .planning import PLAN_TEMPLATE, _plan_prompt, _prep_prompt
37	from .review import (
38	    _review_prompt,
39	    _settled_decisions_block,
40	    _settled_decisions_instruction,
41	    _write_review_template,
42	)
43	
44	_PromptBuilder = Callable[..., str]
45	
46	_CLAUDE_PROMPT_BUILDERS: dict[str, _PromptBuilder] = {
47	    "plan": _plan_prompt,
48	    "prep": _prep_prompt,
49	    "critique": _critique_prompt,
50	    "revise": _revise_prompt,
51	    "gate": _gate_prompt,
52	    "finalize": _finalize_prompt,
53	    "execute": _execute_prompt,
54	    "review": partial(
55	        _review_prompt,
56	        review_intro="Review the execution critically against user intent and observable success criteria.",
57	        criteria_guidance="Judge against the success criteria, not plan elegance.",
58	        task_guidance="Review each task by cross-referencing the executor's per-task `files_changed` and `commands_run` against the git diff and any audit findings.",
59	        sense_check_guidance="Review every sense check explicitly. Confirm concise executor acknowledgments when they are specific; dig deeper only when they are perfunctory or contradicted by the code.",
60	    ),
61	}
62	
63	_CODEX_PROMPT_BUILDERS: dict[str, _PromptBuilder] = {
64	    "plan": _plan_prompt,
65	    "prep": _prep_prompt,
66	    "critique": _critique_prompt,
67	    "revise": _revise_prompt,
68	    "gate": _gate_prompt,
69	    "finalize": _finalize_prompt,
70	    "execute": _execute_prompt,
71	    "review": partial(
72	        _review_prompt,
73	        review_intro="Review the implementation against the success criteria.",
74	        criteria_guidance="Verify each success criterion explicitly.",
75	        task_guidance="Cross-reference each task's `files_changed` and `commands_run` against the git diff and any audit findings.",
76	        sense_check_guidance="Review every `sense_check` explicitly and treat perfunctory acknowledgments as a reason to dig deeper.",
77	    ),
78	}
79	
80	_HERMES_PROMPT_BUILDERS: dict[str, _PromptBuilder] = {
81	    "plan": _plan_prompt,
82	    "prep": _prep_prompt,
83	    "critique": _critique_prompt,
84	    "revise": _revise_prompt,
85	    "gate": _gate_prompt,
86	    "finalize": _finalize_prompt,
87	    "execute": _execute_prompt,
88	    "review": partial(
89	        _review_prompt,
90	        review_intro="Review the execution critically against user intent and observable success criteria.",
91	        criteria_guidance="Judge against the success criteria, not plan elegance.",
92	        task_guidance="Review each task by cross-referencing the executor's per-task `files_changed` and `commands_run` against the git diff and any audit findings.",
93	        sense_check_guidance="Review every sense check explicitly. Confirm concise executor acknowledgments when they are specific; dig deeper only when they are perfunctory or contradicted by the code.",
94	    ),
95	}
96	
97	_NESTED_HARNESS_GUARD = (
98	    "You are already running inside the megaplan harness for this step. "
99	    "Do the requested planning/review/execution work directly. "
100	    "Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, "
101	    "do NOT start nested megaplan plans, and do NOT recurse into another planning harness. "
102	    "Treat mentions of megaplan in the repository or environment as implementation context only."
103	)
104	
105	
106	def _prepend_harness_guard(prompt: str) -> str:
107	    return f"{_NESTED_HARNESS_GUARD}\n\n{prompt}"
108	
109	
110	def create_claude_prompt(
111	    step: str, state: PlanState, plan_dir: Path, root: Path | None = None, **prompt_kwargs: object
112	) -> str:
113	    builder = _CLAUDE_PROMPT_BUILDERS.get(step)
114	    if builder is None:
115	        raise CliError("unsupported_step", f"Unsupported Claude step '{step}'")
116	    if step == "review":
117	        return _prepend_harness_guard(builder(state, plan_dir, **prompt_kwargs))
118	    if step in {"prep", "critique", "gate", "finalize", "execute"}:
119	        return _prepend_harness_guard(builder(state, plan_dir, root=root))
120	    return _prepend_harness_guard(builder(state, plan_dir))
121	
122	
123	def create_codex_prompt(
124	    step: str, state: PlanState, plan_dir: Path, root: Path | None = None, **prompt_kwargs: object
125	) -> str:
126	    builder = _CODEX_PROMPT_BUILDERS.get(step)
127	    if builder is None:
128	        raise CliError("unsupported_step", f"Unsupported Codex step '{step}'")
129	    if step == "review":
130	        return _prepend_harness_guard(builder(state, plan_dir, **prompt_kwargs))
131	    if step in {"prep", "critique", "gate", "finalize", "execute"}:
132	        return _prepend_harness_guard(builder(state, plan_dir, root=root))
133	    return _prepend_harness_guard(builder(state, plan_dir))
134	
135	
136	def create_hermes_prompt(
137	    step: str, state: PlanState, plan_dir: Path, root: Path | None = None, **prompt_kwargs: object
138	) -> str:
139	    builder = _HERMES_PROMPT_BUILDERS.get(step)
140	    if builder is None:
141	        raise CliError("unsupported_step", f"Unsupported Hermes step '{step}'")
142	    if step == "review":
143	        return _prepend_harness_guard(builder(state, plan_dir, **prompt_kwargs))
144	    if step in {"prep", "critique", "gate", "finalize", "execute"}:
145	        return _prepend_harness_guard(builder(state, plan_dir, root=root))
146	    return _prepend_harness_guard(builder(state, plan_dir))
147	
148	
149	__all__ = [
150	    "PLAN_TEMPLATE",
151	    "_CLAUDE_PROMPT_BUILDERS",
152	    "_CODEX_PROMPT_BUILDERS",
153	    "_HERMES_PROMPT_BUILDERS",
154	    "_collect_critique_summaries",
155	    "_critique_prompt",
156	    "_debt_watch_lines",
157	    "_escalated_debt_for_prompt",
158	    "_execute_approval_note",
159	    "_execute_batch_prompt",
160	    "_execute_nudges",
161	    "_execute_prompt",
162	    "_execute_rerun_guidance",
163	    "_execute_review_block",
164	    "_finalize_debt_block",
165	    "_finalize_prompt",
166	    "_flag_summary",
167	    "_gate_debt_block",
168	    "_gate_prompt",
169	    "_grouped_debt_for_prompt",
170	    "_plan_prompt",
171	    "_planning_debt_block",
172	    "_prep_prompt",
173	    "_write_critique_template",
174	    "_render_prep_block",
175	    "_resolve_prompt_root",
176	    "_review_prompt",
177	    "_revise_prompt",
178	    "_settled_decisions_block",
179	    "_settled_decisions_instruction",
180	    "_write_review_template",
181	    "create_claude_prompt",
182	    "create_codex_prompt",
183	    "create_hermes_prompt",
184	]
185
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 330,
  "limit": 30
}
```

> TOOL

tool_result Read
```
330	        configured_timeout_seconds=int(get_effective("execution", "worker_timeout_seconds")),
331	    )
332	    if runtime is not None:
333	        response["next_step_runtime"] = runtime
334	    progress = _build_progress_payload(plan_dir, state) if (plan_dir / "finalize.json").exists() else None
335	    if progress is not None:
336	        response["progress"] = progress
337	        response["summary"] = response["summary"] + " " + progress["summary"]
338	    return response
339	
340	
341	def handle_status(root: Path, args: argparse.Namespace) -> StepResponse:
342	    plan_dir, state = load_plan(root, args.plan)
343	    return _build_status_payload(plan_dir, state)
344	
345	
346	def handle_audit(root: Path, args: argparse.Namespace) -> StepResponse:
347	    plan_dir, state = load_plan(root, args.plan)
348	    return {
349	        "success": True,
350	        "step": "audit",
351	        "plan": state["name"],
352	        "plan_dir": str(plan_dir),
353	        "state": state,
354	    }
355	
356	
357	def handle_progress(root: Path, args: argparse.Namespace) -> StepResponse:
358	    plan_dir, state = load_plan(root, args.plan)
359	    progress = _build_progress_payload(plan_dir, state)
```

> AGENT

Now let me check the remaining pieces needed — the execution flow, review handler, and the status builder.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py",
  "offset": 240,
  "limit": 120
}
```

> TOOL

tool_result Read
```
240	            f"{total_tasks - tracked_tasks}/{total_tasks} tasks have no executor update"
241	        )
242	    if acknowledged_checks < total_checks:
243	        reasons.append(
244	            f"{total_checks - acknowledged_checks}/{total_checks} sense checks have no executor acknowledgment"
245	        )
246	    if missing_task_evidence:
247	        reasons.append(
248	            "done tasks missing both files_changed and commands_run: "
249	            + ", ".join(missing_task_evidence)
250	        )
251	    if timeout_reason is not None:
252	        reasons.append(timeout_reason)
253	    return reasons
254	
255	
256	def _merge_batch_results(
257	    *,
258	    finalize_data: dict[str, Any],
259	    payload: dict[str, Any],
260	    batch_task_ids: list[str],
261	    batch_sense_check_ids: list[str],
262	    issues: list[str],
263	) -> tuple[int, int, int, int]:
264	    batch_task_id_set = set(batch_task_ids)
265	    batch_sense_check_id_set = set(batch_sense_check_ids)
266	    pre_merge_statuses = _snapshot_task_statuses(
267	        [
268	            task
269	            for task in finalize_data.get("tasks", [])
270	            if task.get("id") in batch_task_id_set
271	        ]
272	    )
273	    # Accept task_updates for ANY valid task, not just the current batch.
274	    # Models often complete multiple batches' worth of work in one pass —
275	    # rejecting the extra work as "unknown task_id" wastes correct results.
276	    all_tasks_by_id = {
277	        task["id"]: task
278	        for task in finalize_data.get("tasks", [])
279	        if isinstance(task, dict) and isinstance(task.get("id"), str)
280	    }
281	    merged_count, _ = _validate_and_merge_batch(
282	        payload.get("task_updates"),
283	        required_fields=(
284	            "task_id",
285	            "status",
286	            "executor_notes",
287	            "files_changed",
288	            "commands_run",
289	        ),
290	        targets_by_id=all_tasks_by_id,
291	        id_field="task_id",
292	        merge_fields=("status", "executor_notes", "files_changed", "commands_run"),
293	        issues=issues,
294	        validation_label="task_updates",
295	        merge_label="task_update",
296	        # Don't flag incomplete based on all tasks — check batch coverage below
297	        incomplete_message=None,
298	        enum_fields={"status": {"done", "skipped", "completed"}},
299	        nonempty_fields={"executor_notes"},
300	        array_fields=("files_changed", "commands_run"),
301	    )
302	    # Check batch-specific coverage: how many of THIS batch's tasks got updates?
303	    total_batch_tasks = len(batch_task_id_set)
304	    batch_merged = sum(
305	        1
306	        for tid in batch_task_id_set
307	        if all_tasks_by_id.get(tid, {}).get("status") in ("done", "skipped")
308	    )
309	    if batch_merged < total_batch_tasks:
310	        issues.append(
311	            f"{total_batch_tasks - batch_merged}/{total_batch_tasks} batch tasks have no executor update — tracking is incomplete."
312	        )
313	    # Same for sense checks — accept any valid sense check ID.
314	    all_sense_checks_by_id = {
315	        sense_check["id"]: sense_check
316	        for sense_check in finalize_data.get("sense_checks", [])
317	        if isinstance(sense_check, dict) and isinstance(sense_check.get("id"), str)
318	    }
319	    acknowledged_count, _ = _validate_and_merge_batch(
320	        payload.get("sense_check_acknowledgments"),
321	        required_fields=("sense_check_id", "executor_note"),
322	        targets_by_id=all_sense_checks_by_id,
323	        id_field="sense_check_id",
324	        merge_fields=("executor_note",),
325	        issues=issues,
326	        validation_label="sense_check_acknowledgments",
327	        merge_label="sense_check_acknowledgment",
328	        incomplete_message=None,
329	        nonempty_fields={"executor_note"},
330	    )
331	    total_batch_checks = len(batch_sense_check_id_set)
332	    batch_acknowledged = sum(
333	        1
334	        for sid in batch_sense_check_id_set
335	        if all_sense_checks_by_id.get(sid, {}).get("executor_note")
336	    )
337	    if batch_acknowledged < total_batch_checks:
338	        issues.append(
339	            f"{total_batch_checks - batch_acknowledged}/{total_batch_checks} batch sense checks have no executor acknowledgment — tracking is incomplete."
340	        )
341	    _append_execute_reconciliation_advisories(
342	        before_statuses=pre_merge_statuses,
343	        tasks_by_id=all_tasks_by_id,
344	        issues=issues,
345	    )
346	    return merged_count, total_batch_tasks, acknowledged_count, total_batch_checks
347	
348	
349	def _run_and_merge_batch(
350	    *,
351	    root: Path,
352	    plan_dir: Path,
353	    state: PlanState,
354	    args: argparse.Namespace,
355	    agent: str,
356	    mode: str,
357	    refreshed: bool,
358	    model: str | None = None,
359	    prompt_override: str | None,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1570,
  "limit": 50
}
```

> TOOL

tool_result Read
```
1570	                    "source": f"review_{check_id}",
1571	                }
1572	            )
1573	    return rework_items
1574	
1575	
1576	def handle_review(root: Path, args: argparse.Namespace) -> StepResponse:
1577	    with load_plan_locked(root, args.plan, step="review") as (plan_dir, state):
1578	        require_state(state, "review", {STATE_EXECUTED})
1579	        robustness = configured_robustness(state)
1580	        pre_check_flags: list[dict[str, Any]] = []
1581	        if robustness in {"standard", "robust", "superrobust"}:
1582	            pre_check_flags = run_pre_checks(plan_dir, state, Path(state["config"]["project_dir"]))
1583	        if robustness in {"standard", "light", "robust"}:
1584	            resolved = None
1585	            prompt_override = None
1586	            prompt_kwargs = None
1587	            if robustness in {"standard", "robust"}:
1588	                resolved = resolve_agent_mode("review", args)
1589	                if _supports_prompt_kwargs(worker_module.run_step_with_worker):
1590	                    prompt_kwargs = {"pre_check_flags": pre_check_flags}
1591	                else:
1592	                    prompt_override = _build_review_prompt_override(
1593	                        resolved[0],
1594	                        state,
1595	                        plan_dir,
1596	                        root=root,
1597	                        pre_check_flags=pre_check_flags,
1598	                    )
1599	            worker, agent, mode, refreshed = _run_worker(
1600	                "review",
1601	                state,
1602	                plan_dir,
1603	                args,
1604	                root=root,
1605	                resolved=resolved,
1606	                prompt_override=prompt_override,
1607	                prompt_kwargs=prompt_kwargs,
1608	            )
1609	            if robustness in {"standard", "robust"}:
1610	                worker.payload["pre_check_flags"] = pre_check_flags
1611	                update_flags_after_review(plan_dir, worker.payload, iteration=state["iteration"])
1612	            atomic_write_json(plan_dir / "review.json", worker.payload)
1613	        else:
1614	            agent_type, mode, refreshed, model = resolve_agent_mode("review", args)
1615	            if agent_type != "hermes" or os.getenv(MOCK_ENV_VAR) == "1":
1616	                worker, agent, mode, refreshed = _run_worker(
1617	                    "review",
1618	                    state,
1619	                    plan_dir,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 285,
  "limit": 50
}
```

> TOOL

tool_result Read
```
285	    lock_path = plan_dir / ".plan.lock"
286	    lock_file_present = lock_path.exists()
287	    lock_held = plan_lock_is_held(plan_dir)
288	    active_step = _build_active_step(state.get("active_step"), plan_dir=plan_dir)
289	    last_step = _build_last_step(state)
290	    summary = f"Plan '{state['name']}' is currently in state '{state['current_state']}'."
291	    if active_step:
292	        summary = (
293	            summary
294	            + f" Active step: {active_step.get('step')} via {active_step.get('agent')}."
295	        )
296	    elif lock_file_present and not lock_held:
297	        summary = (
298	            summary
299	            + " No active step. The `.plan.lock` file may remain on disk even when no process holds the lock."
300	        )
301	    response: StepResponse = {
302	        "success": True,
303	        "step": "status",
304	        "plan": state["name"],
305	        "state": state["current_state"],
306	        "iteration": state["iteration"],
307	        "summary": summary,
308	        "next_step": next_steps[0] if next_steps else None,
309	        "valid_next": next_steps,
310	        "artifacts": sorted(
311	            path.name
312	            for path in plan_dir.iterdir()
313	            if path.is_file() and path.name != ".plan.lock"
314	        ),
315	        "lock_file_present": lock_file_present,
316	        "lock_held": lock_held,
317	        "active_step": active_step,
318	        "last_step": last_step,
319	        "total_cost_usd": state.get("meta", {}).get("total_cost_usd", 0.0),
320	        "notes_count": len(notes) if isinstance(notes, list) else 0,
321	        "notes": notes if isinstance(notes, list) else [],
322	        "session_summaries": [
323	            {"key": key, **value}
324	            for key, value in sorted(state.get("sessions", {}).items())
325	            if isinstance(value, dict)
326	        ],
327	    }
328	    runtime = build_next_step_runtime(
329	        response.get("next_step"),
330	        configured_timeout_seconds=int(get_effective("execution", "worker_timeout_seconds")),
331	    )
332	    if runtime is not None:
333	        response["next_step_runtime"] = runtime
334	    progress = _build_progress_payload(plan_dir, state) if (plan_dir / "finalize.json").exists() else None
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/review.py",
  "offset": 60,
  "limit": 60
}
```

> TOOL

tool_result Read
```
60	            criteria.append({
61	                "name": crit["name"],
62	                "priority": crit.get("priority", "must"),
63	                "pass": "",
64	                "evidence": "",
65	            })
66	
67	    return {
68	        "review_verdict": "",
69	        "criteria": criteria,
70	        "issues": [],
71	        "rework_items": [],
72	        "summary": "",
73	        "task_verdicts": task_verdicts,
74	        "sense_check_verdicts": sense_check_verdicts,
75	    }
76	
77	
78	def _parallel_review_context(state: PlanState, plan_dir: Path) -> dict[str, Any]:
79	    project_dir = Path(state["config"]["project_dir"])
80	    gate = read_json(plan_dir / "gate.json")
81	    settled_decisions = gate.get("settled_decisions", [])
82	    if not isinstance(settled_decisions, list):
83	        settled_decisions = []
84	    return {
85	        "project_dir": project_dir,
86	        "intent_block": intent_and_notes_block(state),
87	        "git_diff": collect_git_diff_patch(project_dir),
88	        "finalize_data": read_json(plan_dir / "finalize.json"),
89	        "settled_decisions": settled_decisions,
90	    }
91	
92	
93	def _build_review_checks_template(
94	    plan_dir: Path,
95	    state: PlanState,
96	    checks: tuple[Any, ...],
97	) -> list[dict[str, object]]:
98	    checks_template: list[dict[str, object]] = []
99	    for check in checks:
100	        entry: dict[str, object] = {
101	            "id": _check_field(check, "id"),
102	            "question": _check_field(check, "question"),
103	            "guidance": _check_field(check, "guidance") or "",
104	            "findings": [],
105	        }
106	        checks_template.append(entry)
107	
108	    if state.get("iteration", 1) <= 1:
109	        return checks_template
110	
111	    prior_path = plan_dir / "review.json"
112	    if not prior_path.exists():
113	        return checks_template
114	
115	    prior = read_json(prior_path)
116	    active_check_ids = {_check_field(check, "id") for check in checks}
117	    prior_checks = {
118	        check.get("id"): check
119	        for check in prior.get("checks", [])
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py",
  "offset": 100,
  "limit": 120
}
```

> TOOL

tool_result Read
```
100	        )
101	    return sorted(reset_reasons)
102	
103	
104	def _timeout_checkpoint_path(plan_dir: Path, *, batch_number: int | None) -> Path:
105	    if batch_number is None:
106	        return plan_dir / "execution_checkpoint.json"
107	    return batch_artifact_path(plan_dir, batch_number)
108	
109	
110	def _merge_timeout_checkpoint(
111	    *,
112	    finalize_data: dict[str, Any],
113	    checkpoint_data: dict[str, Any],
114	    checkpoint_name: str,
115	    issues: list[str],
116	) -> None:
117	    tasks_by_id = {
118	        task["id"]: task
119	        for task in finalize_data.get("tasks", [])
120	        if isinstance(task, dict) and isinstance(task.get("id"), str)
121	    }
122	    merged_tasks, _ = _validate_and_merge_batch(
123	        checkpoint_data.get("task_updates"),
124	        required_fields=(
125	            "task_id",
126	            "status",
127	            "executor_notes",
128	            "files_changed",
129	            "commands_run",
130	        ),
131	        targets_by_id=tasks_by_id,
132	        id_field="task_id",
133	        merge_fields=("status", "executor_notes", "files_changed", "commands_run"),
134	        issues=issues,
135	        validation_label=f"{checkpoint_name}.task_updates",
136	        merge_label="checkpoint task_update",
137	        enum_fields={"status": {"done", "skipped", "completed"}},
138	        nonempty_fields={"executor_notes"},
139	        array_fields=("files_changed", "commands_run"),
140	    )
141	    sense_checks_by_id = {
142	        sense_check["id"]: sense_check
143	        for sense_check in finalize_data.get("sense_checks", [])
144	        if isinstance(sense_check, dict) and isinstance(sense_check.get("id"), str)
145	    }
146	    merged_checks, _ = _validate_and_merge_batch(
147	        checkpoint_data.get("sense_check_acknowledgments"),
148	        required_fields=("sense_check_id", "executor_note"),
149	        targets_by_id=sense_checks_by_id,
150	        id_field="sense_check_id",
151	        merge_fields=("executor_note",),
152	        issues=issues,
153	        validation_label=f"{checkpoint_name}.sense_check_acknowledgments",
154	        merge_label="checkpoint sense_check_acknowledgment",
155	        nonempty_fields={"executor_note"},
156	    )
157	    if merged_tasks > 0 or merged_checks > 0:
158	        issues.append(
159	            f"Recovered timeout checkpoint from {checkpoint_name}: merged {merged_tasks} task update(s) and {merged_checks} sense check acknowledgment(s)."
160	        )
161	
162	
163	def _recover_execute_timeout(
164	    *,
165	    plan_dir: Path,
166	    state: PlanState,
167	    error: CliError,
168	    agent: str,
169	    mode: str,
170	    refreshed: bool,
171	    auto_approve: bool,
172	    args: argparse.Namespace,
173	    batch_number: int | None,
174	    persist_state: bool = True,
175	) -> StepResponse:
176	    deviations = [f"Execute timed out: {error.message}"]
177	    finalize_data = read_json(plan_dir / "finalize.json")
178	    checkpoint_path = _timeout_checkpoint_path(plan_dir, batch_number=batch_number)
179	    try:
180	        checkpoint_data = read_json(checkpoint_path)
181	    except FileNotFoundError:
182	        deviations.append(
183	            f"Advisory: timeout checkpoint {checkpoint_path.name} was not found."
184	        )
185	    except json.JSONDecodeError as exc:
186	        deviations.append(
187	            f"Advisory: timeout checkpoint {checkpoint_path.name} was not valid JSON: {exc}"
188	        )
189	    else:
190	        if isinstance(checkpoint_data, dict):
191	            _merge_timeout_checkpoint(
192	                finalize_data=finalize_data,
193	                checkpoint_data=checkpoint_data,
194	                checkpoint_name=checkpoint_path.name,
195	                issues=deviations,
196	            )
197	        else:
198	            deviations.append(
199	                f"Advisory: timeout checkpoint {checkpoint_path.name} did not contain an object."
200	            )
201	
202	    project_dir = Path(state["config"]["project_dir"])
203	    initial_audit = validate_execution_evidence(finalize_data, project_dir)
204	    if initial_audit["skipped"]:
205	        deviations.append(
206	            f"Advisory audit skip during timeout recovery: {initial_audit['reason']}"
207	        )
208	    for finding in initial_audit["findings"]:
209	        deviations.append(f"Advisory audit finding during timeout recovery: {finding}")
210	
211	    _reset_timeout_invalid_tasks(
212	        finalize_data,
213	        execution_audit=initial_audit,
214	        issues=deviations,
215	    )
216	    execution_audit = validate_execution_evidence(finalize_data, project_dir)
217	    atomic_write_json(plan_dir / "execution_audit.json", execution_audit)
218	    atomic_write_json(plan_dir / "finalize.json", finalize_data)
219	    atomic_write_text(
```

> AGENT

Now let me check the remaining execution code for `_run_and_merge_batch` and `_check_done_task_evidence`, and the pyproject.toml / CHANGELOG.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py",
  "offset": 360,
  "limit": 120
}
```

> TOOL

tool_result Read
```
360	    batch_task_ids: list[str],
361	    batch_sense_check_ids: list[str],
362	    finalize_data: dict[str, Any],
363	    batch_number: int,
364	    batches_total: int,
365	    quality_config: dict[str, Any],
366	    capture_git_status_snapshot_fn: Callable[
367	        [Path], tuple[dict[str, str], str | None]
368	    ] = _capture_git_status_snapshot,
369	) -> BatchResult:
370	    project_dir = Path(state["config"]["project_dir"])
371	    before_snapshot, before_error = capture_git_status_snapshot_fn(project_dir)
372	    before_line_counts = capture_before_line_counts(project_dir, before_snapshot.keys())
373	    worker, agent, mode, refreshed = worker_module.run_step_with_worker(
374	        "execute",
375	        state,
376	        plan_dir,
377	        args,
378	        root=root,
379	        resolved=(agent, mode, refreshed, model),
380	        prompt_override=prompt_override,
381	    )
382	    payload = dict(worker.payload)
383	    deviations = list(payload.get("deviations", []))
384	    batch_task_id_set = set(batch_task_ids)
385	    deviations.extend(
386	        _observe_git_changes(
387	            project_dir=project_dir,
388	            payload=payload,
389	            before_snapshot=before_snapshot,
390	            before_error=before_error,
391	            batch_number=batch_number,
392	            batches_total=batches_total,
393	            capture_git_status_snapshot_fn=capture_git_status_snapshot_fn,
394	        )
395	    )
396	    deviations.extend(
397	        _collect_quality_deviations(
398	            project_dir=project_dir,
399	            before_snapshot=before_snapshot,
400	            before_line_counts=before_line_counts,
401	            quality_config=quality_config,
402	            capture_git_status_snapshot_fn=capture_git_status_snapshot_fn,
403	        )
404	    )
405	    merged_count, total_batch_tasks, acknowledged_count, total_batch_checks = (
406	        _merge_batch_results(
407	            finalize_data=finalize_data,
408	            payload=payload,
409	            batch_task_ids=batch_task_ids,
410	            batch_sense_check_ids=batch_sense_check_ids,
411	            issues=deviations,
412	        )
413	    )
414	    missing_task_evidence = _check_done_task_evidence(
415	        finalize_data.get("tasks", []),
416	        issues=deviations,
417	        should_classify=lambda task: task.get("id") in batch_task_id_set,
418	        has_evidence=lambda task: bool(task.get("files_changed")),
419	        has_advisory_evidence=lambda task: bool(task.get("commands_run")),
420	        missing_message="Done tasks missing both files_changed and commands_run: ",
421	        advisory_message="Advisory: done tasks rely on commands_run without files_changed (FLAG-006 softening): ",
422	    )
423	    execution_audit = validate_execution_evidence(finalize_data, project_dir)
424	    if execution_audit["skipped"]:
425	        deviations.append(f"Advisory audit skip: {execution_audit['reason']}")
426	    for finding in execution_audit["findings"]:
427	        deviations.append(f"Advisory audit finding: {finding}")
428	    payload["deviations"] = deviations
429	    atomic_write_json(batch_artifact_path(plan_dir, batch_number), payload)
430	    atomic_write_json(plan_dir / "execution_audit.json", execution_audit)
431	    atomic_write_json(plan_dir / "finalize.json", finalize_data)
432	    atomic_write_text(
433	        plan_dir / "final.md", render_final_md(finalize_data, phase="execute")
434	    )
435	    return BatchResult(
436	        worker=worker,
437	        agent=agent,
438	        mode=mode,
439	        refreshed=refreshed,
440	        payload=payload,
441	        batch_number=batch_number,
442	        batch_task_ids=list(batch_task_ids),
443	        batch_sense_check_ids=list(batch_sense_check_ids),
444	        merged_task_count=merged_count,
445	        total_task_count=total_batch_tasks,
446	        acknowledged_sense_check_count=acknowledged_count,
447	        total_sense_check_count=total_batch_checks,
448	        missing_task_evidence=missing_task_evidence,
449	        execution_audit=execution_audit,
450	        finalize_hash=sha256_file(plan_dir / "finalize.json"),
451	    )
452	
453	
454	def _append_trace_output(plan_dir: Path, trace_output: str | None) -> bool:
455	    if trace_output is None:
456	        return False
457	    trace_path = plan_dir / "execution_trace.jsonl"
458	    existing_trace = (
459	        trace_path.read_text(encoding="utf-8") if trace_path.exists() else ""
460	    )
461	    atomic_write_text(trace_path, existing_trace + trace_output)
462	    return True
463	
464	
465	def handle_execute_one_batch(
466	    *,
467	    root: Path,
468	    plan_dir: Path,
469	    state: PlanState,
470	    args: argparse.Namespace,
471	    batch_number: int,
472	    auto_approve: bool,
473	    agent: str,
474	    mode: str,
475	    refreshed: bool,
476	    model: str | None = None,
477	) -> StepResponse:
478	    finalize_data = read_json(plan_dir / "finalize.json")
479	    global_config = load_config()
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/pyproject.toml",
  "offset": 1,
  "limit": 15
}
```

> TOOL

tool_result Read
```
1	[build-system]
2	requires = ["hatchling"]
3	build-backend = "hatchling.build"
4	
5	[project]
6	name = "megaplan-harness"
7	version = "0.14.4"
8	description = "AI agent harness for coordinating Claude and GPT to make and execute extremely robust plans"
9	requires-python = ">=3.11"
10	license = { text = "OSNL-0.2" }
11	authors = [
12	    { name = "Peter [REDACTED]" },
13	]
14	keywords = ["ai", "planning", "orchestration", "claude", "codex"]
15	classifiers = [
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/CHANGELOG.md",
  "offset": 1,
  "limit": 20
}
```

> TOOL

tool_result Read
```
1	# Changelog
2	
3	## v0.14.0 — 2026-04-15
4	
5	### Strict gate flag resolution
6	
7	The gate no longer silently accepts unresolved blocking flags on a PROCEED recommendation. PROCEED now requires explicit `flag_resolutions` for every blocking flag, and a retry is issued once when the first response still leaves blocking blockers unresolved.
8	
9	- **No implicit acceptance**: unresolved blocking flags now trigger a single gate reprompt instead of being auto-marked as accepted tradeoffs.
10	- **Auto-downgrade on retry failure**: if the retry still leaves blocking flags unresolved, the gate artifact is rewritten as `ITERATE` with an auto-downgrade rationale note and `reprompted: true`.
11	- **Stricter tradeoff validation**: `accept_tradeoff` entries now require concrete, flag-specific rationale; rubber-stamp phrases are rejected the same way weak dispute evidence is rejected.
12	- **Debt derived from explicit resolutions**: accepted tradeoff debt entries now come from validated `flag_resolutions` rather than fallback unresolved-flag recording.
13	- **Gate test coverage refreshed**: existing gate debt tests now follow the strict-resolution contract, and new tests cover reprompt success, reprompt downgrade, rubber-stamp rejection, no-reprompt happy path, and resolution-derived debt recording.
14	
15	## v0.12.0 — 2026-04-15
16	
17	### Auto driver
18	
19	New `megaplan auto --plan <name>` drives a plan from its current state to a terminal outcome without human intervention. The driver is intentionally dumb: it reads `status`, runs `next_step`, and loops. All real judgment stays in the phase logic.
20
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/finalize.py"
}
```

> TOOL

tool_result Read
```
1	"""Finalize-phase prompt builders."""
2	
3	from __future__ import annotations
4	
5	import textwrap
6	from pathlib import Path
7	
8	from megaplan._core import (
9	    intent_and_notes_block,
10	    json_dump,
11	    latest_plan_meta_path,
12	    latest_plan_path,
13	    load_flag_registry,
14	    read_json,
15	)
16	from megaplan.types import PlanState
17	
18	from ._shared import _finalize_debt_block, _render_prep_block
19	from .gate import _collect_critique_summaries, _flag_summary
20	
21	
22	def _finalize_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
23	    project_dir = Path(state["config"]["project_dir"])
24	    prep_block, prep_instruction = _render_prep_block(plan_dir)
25	    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
26	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
27	    gate = read_json(plan_dir / "gate.json")
28	    flag_registry = load_flag_registry(plan_dir)
29	    critique_history = _collect_critique_summaries(plan_dir, state["iteration"])
30	    debt_block = _finalize_debt_block(plan_dir, root)
31	    return textwrap.dedent(
32	        f"""
33	        You are preparing an execution-ready briefing document from the approved plan.
34	
35	        Project directory:
36	        {project_dir}
37	
38	        {prep_block}
39	
40	        {prep_instruction}
41	
42	        {intent_and_notes_block(state)}
43	
44	        Approved plan:
45	        {latest_plan}
46	
47	        Plan metadata:
48	        {json_dump(latest_meta).strip()}
49	
50	        Gate summary:
51	        {json_dump(gate).strip()}
52	
53	        Flag registry:
54	        {json_dump(_flag_summary(flag_registry)).strip()}
55	
56	        Critique history:
57	        {json_dump(critique_history).strip()}
58	
59	        {debt_block}
60	
61	        Requirements:
62	        - Produce structured JSON only.
63	        - `tasks` must be an ordered array of task objects. Every task object must include:
64	          - `id`: short stable task ID like `T1`
65	          - `description`: concrete work item
66	          - `depends_on`: array of earlier task IDs or `[]`
67	          - `status`: always `"pending"` at finalize time
68	          - `executor_notes`: always `""` at finalize time
69	          - `reviewer_verdict`: always `""` at finalize time
70	        - `watch_items` must be an array of strings covering runtime risks, critique concerns, and assumptions to keep visible during execution.
71	        - `sense_checks` must be an array with one verification question per task. Every sense-check object must include:
72	          - `id`: short stable ID like `SC1`
73	          - `task_id`: the related task ID
74	          - `question`: reviewer verification question
75	          - `verdict`: always `""` at finalize time
76	        - `meta_commentary` must be a single string with execution guidance, gotchas, or judgment calls that help the executor succeed.
77	        - `validation` must be an object that self-checks plan coverage:
78	          - `plan_steps_covered`: enumerate EVERY step from the approved plan. For each step, provide a short `plan_step_summary` (the step's intent in one phrase) and `finalize_task_ids` (array of task IDs that implement it — a single plan step may map to multiple tasks).
79	          - `orphan_tasks`: task IDs that do not correspond to any plan step. Normally empty. If non-empty, explain in `completeness_notes`.
80	          - `completeness_notes`: free-text explanation of any gaps, deviations, or deliberate omissions.
81	          - `coverage_complete`: set to `true` only if every plan step has at least one finalize task AND you have verified the mapping by reviewing each entry. Set to `false` if any plan step is missing coverage.
82	          - Example:
83	          ```json
84	          "validation": {{
85	            "plan_steps_covered": [
86	              {{"plan_step_summary": "Add retry logic to API client", "finalize_task_ids": ["T1", "T2"]}},
87	              {{"plan_step_summary": "Update configuration schema", "finalize_task_ids": ["T3"]}}
88	            ],
89	            "orphan_tasks": [],
90	            "completeness_notes": "All plan steps mapped to tasks.",
91	            "coverage_complete": true
92	          }}
93	          ```
94	        - Preserve information that strong existing artifacts already capture well: execution ordering, watch-outs, reviewer checkpoints, and practical context.
95	        - The structured output should be self-contained: an executor reading only `finalize.json` should have everything needed to work.
96	        - Keep the task count proportional to the work. A simple 1-2 file fix should be 2 tasks: (1) apply the fix, (2) run tests. Do NOT create separate "inspect" or "read" tasks for simple changes — the executor can read and fix in one step. Only create more tasks when the work has genuinely independent stages.
97	        - The FINAL task MUST always be to run tests and verify the changes work. If specific test IDs or commands are mentioned in the original task, include them. Otherwise, the executor should find and run the tests most relevant to the files changed. If any test fails, read the error, fix the code, and re-run until they pass. Do NOT create new test files — run the project's existing test suite. Additionally, the executor should write a short throwaway script that reproduces the specific bug described in the task, run it to confirm the fix works, then delete the script.
98	        """
99	    ).strip()
100
```

> AGENT

I have enough context. Producing the finalize briefing now.

> TOOL

tool_use StructuredOutput
```json
{
  "tasks": [
    {
      "id": "T1",
      "description": "Add mode/output_path to PlanConfig (types.py) and wire --mode/--output CLI flags (cli.py, handlers.py). In types.py:28, add `mode: str` and `output_path: str` as optional fields to PlanConfig. In cli.py after line 820, add `--mode` (choices=['code','doc'], default='code') and `--output` arguments to init_parser. In handlers.py handle_init (~line 717): validate --output is provided when mode=doc (raise CliError otherwise), validate output_path is relative (no leading '/'), reject '../' traversal, resolve+normalize against project_dir, persist mode and output_path in state['config']. Default mode to 'code' for backward compat.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/types.py",
        "megaplan/cli.py",
        "megaplan/handlers.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T2",
      "description": "Add doc-quality critique category and doc-mode execution schema in schemas.py. (1) Extend the category enum in SCHEMAS['critique.json'] at schemas.py:204 to include 'doc-quality'. (2) Add new 'execution_doc.json' entry to SCHEMAS dict: clone 'execution.json' but replace `files_changed` (top-level and in task_updates[]) with `sections_written: array of strings`, remove `commands_run` from task_updates[] (keep top-level commands_run as optional/empty array), keep output/deviations/sense_check_acknowledgments unchanged. (3) Add helper `get_execution_schema_key(mode: str) -> str` returning 'execution_doc.json' when mode=='doc', else 'execution.json'.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/schemas.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T3",
      "description": "Bump version to 0.15.0 in pyproject.toml:7 and add a ## v0.15.0 CHANGELOG entry describing doc-mode. The CHANGELOG entry should go above the existing v0.14.0 entry. Keep it concise: new --mode doc flag, doc-mode execution schema, doc-mode prompts, section-based audit.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "pyproject.toml",
        "CHANGELOG.md"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T4",
      "description": "Create three doc-mode prompt files. (1) megaplan/prompts/prep_doc.py: define _prep_doc_prompt(state, plan_dir, root=None). Repoint from 'search the codebase' to 'what sources, prior art, related docs should inform this document?' Sense-check items become 'did you read X?' Keep the prep.json output schema identical. (2) megaplan/prompts/execute_doc.py: define _execute_doc_prompt and _execute_doc_batch_prompt. Frame executor as an author; only filesystem op is writing to configured output_path. Replace files_changed refs with sections_written, remove commands_run from per-task guidance. Include doc-mode JSON output shape example. Reuse shared helpers: _execute_nudges, _execute_approval_note, _execute_rerun_guidance, _render_prep_block from existing code. (3) megaplan/prompts/review_doc.py: define _review_doc_prompt(state, plan_dir, *, review_intro, criteria_guidance, ...). Reword to treat deliverable as text. Replace git-diff/execution_audit references with 'read the output file and judge against success criteria.' Keep review.json output schema. Each file should be under ~300 lines.",
      "depends_on": [
        "T1"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/prompts/prep_doc.py",
        "megaplan/prompts/execute_doc.py",
        "megaplan/prompts/review_doc.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T5",
      "description": "Wire doc-mode prompts into dispatch and update finalize prompt. In prompts/__init__.py: (1) Import new prompt builders from prep_doc.py, execute_doc.py, review_doc.py. (2) Update _CLAUDE_PROMPT_BUILDERS, _CODEX_PROMPT_BUILDERS, _HERMES_PROMPT_BUILDERS: for prep/execute/review steps, check state['config'].get('mode','code') and select doc-mode builder when mode=='doc'. Other steps (plan, critique, gate, finalize, revise) stay unchanged. (3) Update create_claude_prompt/create_codex_prompt/create_hermes_prompt dispatch logic to pass state through so mode detection works. In prompts/finalize.py: add a conditional block for doc mode that replaces task field guidance — use sections_written instead of files_changed/commands_run, remove the test-verification requirement from the prompt text, instruct the finalizer to omit baseline_test_failures/baseline_test_command.",
      "depends_on": [
        "T4"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/prompts/__init__.py",
        "megaplan/prompts/finalize.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T6",
      "description": "Create megaplan/doc_assembly.py (~150 lines max). Implement: (1) assemble_doc(plan_dir: Path, output_path: Path, finalize_data: dict) -> Path: reads per-batch executor outputs (execution_batch_*.json), orders sections by plan position (task order in finalize_data), writes the assembled file atomically (temp file + rename). (2) extract_sections(batch_payloads: list[dict]) -> dict[str, str]: maps section_id to rendered text from executor output. Idempotent: running twice replaces the file completely. Called at the end of execute after all batches complete.",
      "depends_on": [
        "T2"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/doc_assembly.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T7",
      "description": "Update merge validation and execution evidence audit for doc mode. (1) In execution.py _merge_batch_results (~line 256): read mode from state config. When mode=='doc', required_fields for task_updates becomes ('task_id','status','executor_notes','sections_written'), merge_fields becomes ('status','executor_notes','sections_written'), array_fields becomes ('sections_written',). Pass mode through from _run_and_merge_batch. (2) In evaluation.py validate_execution_evidence (~line 123): add mode parameter (default 'code'). When mode=='doc': extract planned sections from finalize_data tasks (all sections_written across done tasks), verify output file exists and is non-empty, verify all planned sections claimed by done tasks, verify no unclaimed sections. Return findings in the same shape {findings, files_in_diff:[], files_claimed:[], skipped:False} for compatibility. When mode=='code', behavior unchanged. (3) Update callers: execution.py:423 and execution_timeout.py:203,216 to pass mode.",
      "depends_on": [
        "T1",
        "T2"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/execution.py",
        "megaplan/evaluation.py",
        "megaplan/execution_timeout.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T8",
      "description": "Branch finalize handler for doc mode in handlers.py. In _write_finalize_artifacts (~line 376): when state['config'].get('mode')=='doc', skip _capture_test_baseline() (set baseline_test_failures to None, baseline_test_command to None in payload), skip _ensure_verification_task(). Still call _reconcile_validation_after_mutation() (harmless, keeps validation consistent). For code mode, behavior is unchanged. No changes needed to _validate_finalize_payload since it validates tasks generically.",
      "depends_on": [
        "T1"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/handlers.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T9",
      "description": "Branch timeout recovery for doc mode in execution_timeout.py. (1) _merge_timeout_checkpoint (~line 110): read mode from state config. When mode=='doc': required_fields becomes ('task_id','status','executor_notes','sections_written'), merge_fields becomes ('status','executor_notes','sections_written'), array_fields becomes ('sections_written',). (2) _reset_timeout_invalid_tasks (~line 41): when mode=='doc': has_evidence checks bool(task.get('sections_written')), has_advisory_evidence always returns True, skip files_in_diff cross-check, update missing_message. (3) _recover_execute_timeout (~line 163): pass mode to validate_execution_evidence calls at lines 203 and 216. When mode=='doc', aggregate sections_written instead of files_changed in the response.",
      "depends_on": [
        "T7"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/execution_timeout.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T10",
      "description": "Update status display for doc mode in cli.py. In _build_status_payload (~line 285): include mode and output_path in the status response when present in state['config']. Add them to the response dict and mention in the summary string when mode is 'doc'.",
      "depends_on": [
        "T1"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/cli.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T11",
      "description": "Update execute handler and execution loop for doc mode. (1) In handle_execute (handlers.py:1337): detect mode from state['config'].get('mode','code'). When 'doc': skip --confirm-destructive requirement (doc mode writes a single output file). After all batches complete, call assemble_doc() to produce the output file. (2) In _run_and_merge_batch (execution.py:349): accept/detect mode. When mode=='doc': skip _observe_git_changes, _collect_quality_deviations, and capture_before_line_counts (no git changes expected). Adapt _check_done_task_evidence: has_evidence checks sections_written, has_advisory_evidence always True. Pass mode to validate_execution_evidence. (3) In _build_aggregate_execution_payload (execution.py:136): when mode=='doc', aggregate sections_written instead of files_changed.",
      "depends_on": [
        "T6",
        "T7",
        "T8"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/handlers.py",
        "megaplan/execution.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T12",
      "description": "Update review handler for doc mode. (1) In handle_review (handlers.py:1576): when mode=='doc', skip mechanical pre-checks that depend on code (test pass/fail, type checking). (2) In _parallel_review_context (prompts/review.py:78): when mode=='doc', replace git_diff value with the output file content read from state['config']['output_path'] resolved against project_dir.",
      "depends_on": [
        "T5"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/handlers.py",
        "megaplan/prompts/review.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T13",
      "description": "Update worker schema selection and Hermes worker for doc mode. (1) In workers.py: when step=='execute' and mode=='doc' (from state['config']), use 'execution_doc.json' instead of 'execution.json'. Modify the STEP_SCHEMA_FILENAMES lookup in run_claude_step (~line 58) and the codex schema path. Consider adding get_execution_schema_key from schemas.py. (2) In hermes_worker.py: at line 294 where schema_name = STEP_SCHEMA_FILENAMES[step], use get_execution_schema_key(mode) for execute step. (3) In _reconstruct_execute_payload (hermes_worker.py:635): when mode=='doc': skip git-diff and git-status based files_changed reconstruction (lines 670-697), return sections_written instead of files_changed, remove commands_run from task_updates or leave as empty list. (4) Update execute fallback path at hermes_worker.py:192-196: when mode=='doc', attempt doc-shaped reconstruction.",
      "depends_on": [
        "T2",
        "T7"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "megaplan/workers.py",
        "megaplan/hermes_worker.py"
      ],
      "commands_run": [],
      "evidence_files": [],
      "reviewer_verdict": ""
    },
    {
      "id": "T14",
      "description": "Add doc-mode unit tests and verify all existing tests pass. Create tests/test_doc_mode.py covering: (1) handle_init with --mode doc --output docs/plan.md produces state with mode:'doc' and output_path, (2) handle_init with --mode doc but no --output raises CliError, (3) handle_init with --mode doc --output /absolute/path raises CliError, (4) handle_init with --mode doc --output ../escape/path raises CliError, (5) validate_execution_evidence in doc mode: catches missing sections, catches unclaimed sections, passes when all sections present, (6) assemble_doc: sections assembled in plan order, output file non-empty, idempotent re-run replaces file, (7) doc-mode execution schema validates correctly via strict_schema, (8) _write_finalize_artifacts in doc mode: skips test baseline capture and verification task injection, (9) _merge_timeout_checkpoint in doc mode uses sections_written fields, (10) _reset_timeout_invalid_tasks in doc mode checks sections_written evidence and skips git-diff cross-check. Then run `pytest tests/` to confirm all existing + new tests pass. Fix any failures before reporting done.",
      "depends_on": [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
        "T7",
        "T8",
        "T9",
        "T10",
        "T11",
        "T12",
        "T13"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [
        "tests/test_doc_mode.py"
      ],
      "commands_run": [
        "pytest tests/"
      ],
      "evidence_files": [],
      "reviewer_verdict": ""
    }
  ],
  "watch_items": [
    "Backward compatibility: every code path that reads state['config'] must handle missing 'mode' key by defaulting to 'code'. Grep for get('mode') after all changes to verify.",
    "Path containment in handle_init: output_path validation must reject absolute paths AND '../' traversal. Use Path.resolve() and check it's still under project_dir after resolution.",
    "Schema sync: execution_doc.json must be added to both SCHEMAS dict and the runtime layout writer (ensure_runtime_layout). The STEP_SCHEMA_FILENAMES dict must not be changed — schema selection happens dynamically based on mode at call sites.",
    "The _validate_and_merge_batch helper in execution.py is generic — the branching on mode happens at call sites (_merge_batch_results, _merge_timeout_checkpoint), not inside the helper itself.",
    "Doc-mode finalize MUST skip _capture_test_baseline and _ensure_verification_task. If these run in doc mode, they will inject code-mode artifacts (test task, baseline failures) into the finalize.json.",
    "Hermes worker has its own independent schema lookup at hermes_worker.py:294 — this MUST be updated separately from workers.py. Missing this was FLAG-003.",
    "The _reconstruct_execute_payload function in hermes_worker.py (line 635) is the fallback when Hermes can't produce JSON. For doc mode it must NOT run git-diff/git-status reconstruction — that would produce code-shaped output.",
    "Prompt files should reuse shared helpers from prompts/_shared.py and prompts/execute.py where possible to avoid duplication. Don't rewrite helpers that already exist.",
    "The finalize.json schema (schemas.py:228) uses files_changed/commands_run in task items. Doc-mode finalize tasks will have sections_written instead — the finalize prompt must guide the model to produce the right shape, and the finalize validator (_validate_finalize_payload) is generic enough to not break.",
    "DEBT: existing debt items about worker-permissions (loop_execute not getting --full-auto) and workflow-state-machine (state_researched path) are pre-existing and must not be made worse.",
    "validate_execution_evidence callers at execution.py:423 and execution_timeout.py:203,216 all need the mode parameter added — miss one and doc-mode audit runs code-mode checks."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does handle_init correctly reject --mode doc without --output, reject absolute output paths, reject ../ traversal, and persist mode+output_path in state.json?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Does execution_doc.json schema mirror execution.json except with sections_written replacing files_changed (both top-level and in task_updates), and commands_run removed from task_updates?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Is pyproject.toml version exactly '0.15.0' and does CHANGELOG have a v0.15.0 entry above v0.14.0?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Do the three new prompt files (prep_doc.py, execute_doc.py, review_doc.py) each stay under ~300 lines and correctly reference the doc-mode schema shape (sections_written, no commands_run in task_updates)?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does the prompt dispatch correctly select doc-mode builders for prep/execute/review when state config mode is 'doc', while leaving all other steps (plan/critique/gate/revise) unchanged?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Is doc_assembly.py under ~150 lines, does it assemble sections in plan order, write atomically via temp file + rename, and handle idempotent re-runs?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Does validate_execution_evidence in doc mode check output file existence, non-empty content, all planned sections present, and no unclaimed sections — while returning the same dict shape as code mode?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Does _write_finalize_artifacts skip _capture_test_baseline and _ensure_verification_task when mode is 'doc', while still calling _reconcile_validation_after_mutation?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC9",
      "task_id": "T9",
      "question": "Do all three timeout recovery functions (_merge_timeout_checkpoint, _reset_timeout_invalid_tasks, _recover_execute_timeout) correctly branch on mode for field names and skip git-diff cross-checks in doc mode?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC10",
      "task_id": "T10",
      "question": "Does megaplan status include mode and output_path in its response when the plan is in doc mode?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC11",
      "task_id": "T11",
      "question": "Does handle_execute skip --confirm-destructive for doc mode, call assemble_doc after batches, and does _run_and_merge_batch skip git observation and use sections_written evidence checks?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC12",
      "task_id": "T12",
      "question": "Does handle_review skip code-specific pre-checks in doc mode, and does _parallel_review_context supply output file content instead of git_diff?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC13",
      "task_id": "T13",
      "question": "Does the Hermes worker use execution_doc.json schema for doc-mode execute, and does _reconstruct_execute_payload skip git-diff reconstruction and return sections_written?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC14",
      "task_id": "T14",
      "question": "Do all 10 doc-mode test cases pass, and does the full pytest tests/ suite pass with zero regressions?",
      "executor_note": "",
      "verdict": ""
    }
  ],
  "meta_commentary": "This is a large feature with 14 tasks touching ~15 files. The critical execution insight is that the branching pattern is consistent everywhere: read mode from state['config'].get('mode','code'), branch on 'doc' vs 'code'. The most dangerous tasks are T7 (merge validation + audit — used by multiple callers) and T13 (Hermes worker — independent code path that was missed in the original plan as FLAG-003). \n\nKey gotcha: the _validate_and_merge_batch helper is generic and reusable — don't modify it. All doc-mode branching happens at the call sites that invoke it (_merge_batch_results, _merge_timeout_checkpoint). The helper just needs different field name tuples passed in.\n\nAnother gotcha: the finalize.json schema in schemas.py still has files_changed/commands_run as required fields on tasks. Doc-mode finalize will still produce tasks with those fields (as empty arrays) because the schema is shared. The doc-mode differentiation happens in the execution schema and the prompts, not the finalize schema.\n\nFor prompt files: study the existing execute.py and review.py carefully before writing doc variants — there are shared helpers (_execute_nudges, _render_prep_block, etc.) that should be reused, not reimplemented. The doc-mode prompts are reframings, not rewrites.\n\nTasks T1-T3 and T6 are independent and can be parallelized. T4 depends on T1 (needs mode in config for prompt access). T7 depends on T1+T2. T8-T10 depend on T1. The final test task (T14) is a full barrier — it depends on everything.",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Add mode/output_path to PlanConfig TypedDict",
        "finalize_task_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 2: Wire --mode and --output CLI flags + handle_init validation",
        "finalize_task_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 3: Add doc-quality critique category",
        "finalize_task_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Step 4: Add doc-mode execution schema (execution_doc.json)",
        "finalize_task_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Step 5: Bump version to 0.15.0 + CHANGELOG",
        "finalize_task_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 6: Add doc-mode prep prompt (prep_doc.py)",
        "finalize_task_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 7: Add doc-mode execute prompt (execute_doc.py)",
        "finalize_task_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 8: Add doc-mode review prompt (review_doc.py)",
        "finalize_task_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 9: Wire doc-mode prompts into dispatch + update finalize prompt",
        "finalize_task_ids": [
          "T5"
        ]
      },
      {
        "plan_step_summary": "Step 10: Create doc_assembly.py module",
        "finalize_task_ids": [
          "T6"
        ]
      },
      {
        "plan_step_summary": "Step 11: Update _merge_batch_results for doc mode",
        "finalize_task_ids": [
          "T7"
        ]
      },
      {
        "plan_step_summary": "Step 12: Branch validate_execution_evidence for doc mode",
        "finalize_task_ids": [
          "T7"
        ]
      },
      {
        "plan_step_summary": "Step 13: Branch finalize handler for doc mode",
        "finalize_task_ids": [
          "T8"
        ]
      },
      {
        "plan_step_summary": "Step 14: Branch timeout recovery for doc mode",
        "finalize_task_ids": [
          "T9"
        ]
      },
      {
        "plan_step_summary": "Step 15: Update status display for doc mode",
        "finalize_task_ids": [
          "T10"
        ]
      },
      {
        "plan_step_summary": "Step 16: Update execute handler + execution loop for doc mode",
        "finalize_task_ids": [
          "T11"
        ]
      },
      {
        "plan_step_summary": "Step 17: Update review handler for doc mode",
        "finalize_task_ids": [
          "T12"
        ]
      },
      {
        "plan_step_summary": "Step 18: Update worker schema selection",
        "finalize_task_ids": [
          "T13"
        ]
      },
      {
        "plan_step_summary": "Step 19: Update Hermes worker for doc mode",
        "finalize_task_ids": [
          "T13"
        ]
      },
      {
        "plan_step_summary": "Step 20: Add doc-mode unit tests",
        "finalize_task_ids": [
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 21: Verify existing tests pass",
        "finalize_task_ids": [
          "T14"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "All 21 plan steps mapped to tasks. Steps 1-2 consolidated into T1 (both small, same files). Steps 3-4 into T2 (both schemas.py). Steps 6-8 into T4 (three independent prompt files, same work pattern). Steps 11-12 into T7 (merge validation and audit are tightly coupled). Steps 18-19 into T13 (worker schema selection + Hermes are the same concern). Steps 20-21 into T14 (tests + regression check). All other steps are 1:1 with tasks.",
    "coverage_complete": true
  },
  "baseline_test_failures": null,
  "baseline_test_command": "pytest tests/",
  "baseline_test_note": "Test baseline not captured at finalize time — executor should run pytest tests/ before starting work to establish baseline."
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Finalize briefing produced with 14 tasks covering all 21 plan steps. Key structure: T1-T3 are independent foundation work (types/CLI, schemas, version bump), T4-T5 are prompts, T6-T10 are core logic, T11-T13 wire everything together, and T14 is the final test barrier. All four addressed critique flags (finalize handler, timeout recovery, Hermes worker, path containment) are covered in their respective tasks.

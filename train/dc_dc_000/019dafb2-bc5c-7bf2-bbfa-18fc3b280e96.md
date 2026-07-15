> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

You are an independent reviewer. Critique the plan against the actual repository.

        Project directory:
        /Users/user_c042661f/Documents/megaplan





        Idea:
Split tests/test_megaplan.py (5274 lines, ~200 tests) into phase-scoped test files mirroring the source layout: init/plan, prep, critique, revise, gate, finalize, execute, review, audits, types/schemas. Preserve every test's behavior and fixtures; move shared helpers to conftest.py if useful. Delete the original tests/test_megaplan.py when done. Do NOT modify any file under megaplan/ (source package) — another refactor is running there in parallel. Full suite must pass with the same total count.

        Plan:
        # Implementation Plan: Split `tests/test_megaplan.py` into phase-scoped test files

## Overview
`tests/test_megaplan.py` is a 5274-line mega-suite holding ~201 top-level test functions (pytest will expand parametrized cases beyond that). The goal is to split it into phase-scoped files mirroring the workflow phases (`init/plan`, `prep`, `critique`, `revise`, `gate`, `finalize`, `execute`, `review`, `audits`, `types/schemas`) and lift shared helpers/fixtures into `tests/conftest.py`. Source under `megaplan/` must not be touched (parallel refactor running). The file `tests/test_megaplan.py` must be deleted once every test lives in a new file. Full test suite (collected count and pass/fail outcome) must be identical before and after.

Repository shape confirmed:
- `tests/__init__.py` exists (1 line) — `tests` is already an importable package; cross-test imports exist already (e.g. `tests/test_tiny_robustness.py:10` imports from `tests.test_handle_review_robustness`).
- `pyproject.toml:32` sets `testpaths = ["tests"]` — no extra config needed for new files to be picked up.
- Several target file names already exist (`tests/test_schemas.py`, `tests/test_config.py`). **Do not reuse those names**; use `tests/test_types_schemas.py` and fold config/CLI plumbing tests into `tests/test_audits.py`. These new files may contain test-function names that happen to collide with functions in the existing files — pytest uses `module::function` IDs, so collisions across modules are fine.
- `strict_schema` tests in `test_megaplan.py` (e.g. `test_strict_schema_overwrites_partial_required_arrays_recursively`) are distinct from the similarly named ones in `tests/test_schemas.py` (`..._normalizes_...`) — both must be preserved verbatim.

Categorization of the ~201 tests has been done by reading function names at `tests/test_megaplan.py:235-5274`. Mapping is given inline in each Step below.

## Main Phase

### Step 1: Inventory & freeze the current collection
**Scope:** Small
1. **Run** `python -m pytest tests/test_megaplan.py --collect-only -q | tee /tmp/megaplan_tests_before.txt` to capture the full parametrized test ID list (the authoritative "don't drop any of these" ledger).
2. **Count** the tail line (`N tests collected`) and record it; this is the target post-split count.
3. **Note** the parametrized expansions visible from grep: `test_workflow_next_light_robustness_overrides` has 4 cases (`tests/test_megaplan.py:301`), `test_step_invalid_state` has 2 (`tests/test_megaplan.py:1641`). Any other `@pytest.mark.parametrize` above a test function in this file must stay attached to its test in the destination module.

### Step 2: Create `tests/conftest.py` with shared fixtures/helpers
**Scope:** Medium
1. **Create** `tests/conftest.py` and move into it (verbatim, preserving signatures and defaults) the helper block from `tests/test_megaplan.py:39-232`:
   - `read_json` (`:39`)
   - `run_main_json` (`:43`)
   - `_write_lines` (`:55`)
   - `make_args_factory` (`:60`)
   - `@dataclass PlanFixture` (`:88`)
   - `_make_plan_fixture_with_robustness` (`:97`)
   - `@pytest.fixture plan_fixture` (`:135`)
   - `load_state` (`:140`)
   - `latest_plan_name` (`:144`)
   - `debt_registry_path` (`:148`)
   - `first_open_significant_flag` (`:152`)
   - `open_blocking_flags` (`:161`)
   - `ensure_blocking_flags` (`:171`)
   - `make_gate_worker_result` (`:196`)
   - `make_worker_sequence` (`:222`)
2. **Copy** the imports block (`tests/test_megaplan.py:1-36`) into `conftest.py`, trimming only genuinely unused imports. `plan_fixture` is auto-discovered by pytest; non-fixture helpers will be imported by test modules via `from tests.conftest import read_json, load_state, ...`. (Precedent for `from tests.<module> import ...` already exists at `tests/test_tiny_robustness.py:10`.)
3. **Do not** alter any helper body — byte-for-byte moves only; any behavior change here would quietly affect every consumer.

### Step 3: Create `tests/test_init_plan.py`
**Scope:** Medium
1. **Move** these tests (workflow/state-machine, plan-phase handlers, step editor, status/watch, emit/format utilities):
   - `test_init_sets_last_gate_and_next_step_plan` (`:235`)
   - `test_init_includes_next_step_runtime` (`:241`)
   - `test_init_response_points_to_next_step_by_robustness` (`:253`)
   - `test_infer_next_steps_matches_new_state_machine` (`:291`)
   - `test_workflow_next_matches_legacy_partial_state_cases` (`:296`)
   - `test_workflow_next_light_robustness_overrides` + its `@pytest.mark.parametrize` block (`:301-326`)
   - `test_workflow_definition_is_complete_for_standard_flow` (`:330`)
   - `test_workflow_walk_matches_documented_standard_flow` (`:348`)
   - `test_workflow_walk_matches_documented_robust_flow` (`:388`)
   - `test_workflow_walk_matches_documented_light_flow` (`:432`)
   - `test_all_robustness_levels_route_planned_to_critique` (`:451`)
   - `test_handle_plan_sets_and_clears_active_step` (`:460`)
   - `test_handle_plan_failure_clears_active_step` (`:493`)
   - `test_clear_active_step_ignores_mismatched_run_id` (`:515`)
   - `test_handle_status_*` (`:594`, `:648`, `:668`, `:686`), `test_handle_watch_combines_status_and_progress` (`:698`)
   - `test_phase_progress_summary_completion_only` (`:710`), `test_phase_progress_summary_stale` (`:726`)
   - `test_plan_rerun_keeps_iteration_and_uses_same_iteration_subversion` (`:741`)
   - `test_override_add_note_includes_next_step_runtime` (`:756`)
   - `test_handle_plan_includes_next_step_runtime` (`:770`)
   - `test_build_monitor_hint_references_status` (`:778`)
   - `test_format_duration_hint_uses_human_readable_ranges` (`:785`)
   - `test_emit_phase_notice_writes_to_stderr_only` (`:799`), `test_emit_phase_notice_ignores_non_phase_commands` (`:810`)
   - `test_workflow_mock_end_to_end` (`:820`), `test_workflow_light_robustness_single_pass` (`:907`)
   - `test_handle_plan_stores_nonblocking_structure_warnings` (`:1014`), `test_handle_plan_rejects_zero_step_structure_error` (`:1047`)
   - `test_step_add` (`:1520`), `test_step_add_scaffold_passes_validation` (`:1550`), `test_step_remove` (`:1569`), `test_step_move` (`:1587`), `test_step_remove_last_step_rejected` (`:1604`), `test_step_invalid_state` + parametrize (`:1641`), `test_step_preserves_meta` (`:1660`), `test_step_edit_rejects_concurrent_plan_lock` (`:1682`)
   - `test_progress_all_pending` (`:4615`), `test_progress_after_partial_execution` (`:4628`), `test_progress_after_full_execution` (`:4672`) and their helper `_drive_to_finalized` (`:4604`).
2. **Write** a top-of-file import block that pulls helpers from `tests.conftest` and keeps all `megaplan.*` imports the test bodies actually reference. Do not add/remove assertions.

### Step 4: Create `tests/test_prep.py`
**Scope:** Small
1. **Move** the single prep-phase test:
   - `test_cli_registers_prep_command` (`tests/test_megaplan.py:956`).
2. **Keep** the file even though it is tiny — the task explicitly lists `prep` as a target bucket and this is the right home for any new prep tests.

### Step 5: Create `tests/test_critique.py`
**Scope:** Small
1. **Move**:
   - `test_tiny_critique_stub_does_not_leak_active_step` (`:526`)
   - `test_light_critique_routes_to_revise` (`:967`)
   - `test_handle_critique_rejects_invalid_check_payload` (`:1082`)
   - `test_handle_critique_accepts_validated_checks` (`:1115`)
   - `test_critique_prompt_contains_robustness_instruction` (`:3126`)

### Step 6: Create `tests/test_revise.py`
**Scope:** Small
1. **Move**:
   - `test_light_revise_routes_to_finalize` (`:982`)
   - `test_standard_revise_routes_to_critique_and_clears_last_gate` (`:998`)
   - `test_handle_revise_requires_prior_iterate_gate` (`:1259`)
   - `test_replan_from_gated_resets_to_planned` (`:1337`)

### Step 7: Create `tests/test_gate.py`
**Scope:** Medium
1. **Move** gate flows, overrides, flag normalisation, and gate-emitted debt:
   - `test_force_proceed_from_critiqued_writes_override_gate` (`:1267`)
   - `test_force_proceed_registers_unresolved_flags_as_debt` (`:1293`)
   - `test_repeated_force_proceed_increments_existing_debt_instead_of_duplicating` (`:1312`)
   - `test_gate_proceed_with_accepted_tradeoffs_creates_debt` (`:1364`)
   - `test_gate_iterate_with_empty_accepted_tradeoffs_creates_no_debt` (`:1402`)
   - `test_gate_proceed_partial_resolutions_still_missing_after_reprompt_downgrades_to_iterate` (`:1435`)
   - `test_gate_retry_does_not_duplicate_weighted_scores` (`:1737`)
   - `test_gate_proceed_partial_resolutions_triggers_reprompt` (`:1807`)
   - `test_gate_proceed_still_missing_after_reprompt_downgrades_to_iterate` (`:1870`)
   - `test_gate_accept_tradeoff_rubber_stamp_rejected` (`:1915`)
   - `test_gate_accept_tradeoff_concrete_rationale_accepted` (`:1947`)
   - `test_gate_proceed_all_flags_resolved_no_reprompt` (`:1979`)
   - `test_gate_debt_not_recorded_on_downgrade` (`:2014`)
   - `test_gate_debt_derived_from_flag_resolutions` (`:2057`)
   - `test_normalize_flag_record_*` (`:2099`, `:2108`, `:2113`, `:2118`, `:2123`)
   - `test_update_flags_after_critique_*` (`:2129`, `:2146`, `:2166`, `:2185`, `:2206`, `:2224`)
   - `test_update_flags_after_revise_marks_addressed` (`:2243`)
   - `test_unresolved_significant_flags_filtering` (`:2256`)
   - `test_override_add_note_records_note` (`:2282`)
   - `test_add_note_after_abort` (`:2293`)
   - `test_abort_sets_terminal_state` (`:2306`)
   - `test_override_set_robustness_updates_config` (`:2316`), `test_override_set_robustness_rejects_invalid_level` (`:2339`), `test_override_set_robustness_blocked_in_terminal_state` (`:2351`)
   - `test_force_proceed_requires_critiqued_state` (`:2367`), `test_force_proceed_requires_success_criteria` (`:2376`)
   - `test_gate_response_surfaces_auto_approve` (`:2478`)
   - `test_require_state_rejects_invalid_transition` (`:2494`), `test_terminal_states_block_progression` (`:2500`)
   - `test_build_gate_signals_includes_debt_overlaps_when_flags_match` (`:3149`)

### Step 8: Create `tests/test_finalize.py`
**Scope:** Small
1. **Move**:
   - `test_handle_finalize_validates_payload_shape` (`:1129`)
   - `test_handle_finalize_rejects_invalid_payload` (`:1184`)
   - `test_finalize_snapshot_remains_pending_after_execute` (`:1229`)
   - `test_render_final_md_pending_partially_done_and_reviewed_states` (`:3170`)
   - `test_render_final_md_phase_marks_gaps_only_when_due` (`:3245`)

### Step 9: Create `tests/test_execute.py`
**Scope:** Large
1. **Move** execute-phase tests (happy path, timeout recovery, multi-batch, execute-quality, baselines, step failure, approval gates, execute prompt):
   - `test_capture_test_baseline_*` (`:540`, `:568`, `:579`)
   - `test_execute_requires_confirm_destructive` (`:2396`), `test_execute_requires_user_approval_in_review_mode` (`:2411`), `test_execute_succeeds_with_user_approval` (`:2426`), `test_execute_succeeds_in_auto_approve_mode` (`:2446`)
   - `test_step_failure_*` (`:2856`, `:2870`, `:2884`)
   - `test_run_command_raises_on_timeout` (`:2898`), `test_run_command_raises_on_file_not_found` (`:2904`)
   - `test_execute_prompt_includes_approval_note` (`:3135`)
   - `test_execute_happy_path_tracks_all_tasks` (`:3476`)
   - `test_execute_timeout_recovers_partial_progress_from_finalize_json` (`:3497`)
   - `test_execute_timeout_reads_execution_checkpoint_json` (`:3538`)
   - `test_execute_timeout_resets_done_tasks_without_any_evidence` (`:3592`)
   - `test_execute_reports_advisory_when_structured_output_disagrees_with_disk_checkpoint` (`:3627`)
   - `test_execute_deduplicates_task_updates_and_blocks_incomplete_coverage` (`:3753`)
   - `test_execute_blocks_done_task_without_any_per_task_evidence` (`:3946`), `test_execute_softens_done_task_with_commands_only` (`:4008`)
   - `test_execute_multi_batch_happy_path_aggregates_results` (`:4072`), `test_execute_multi_batch_timeout_preserves_prior_batches` (`:4199`), `test_execute_rerun_with_completed_dependency_uses_single_batch_fast_path` (`:4269`), `test_execute_multi_batch_observation_allows_cross_batch_reedit_and_flags_phantoms` (`:4334`)
   - Batch helpers + tests: `_setup_two_batch_plan` (`:4692`), `_batch_worker` (`:4729`), `test_batch_1_on_two_batch_plan_stays_finalized` (`:4775`), `test_batch_timeout_reads_execution_batch_n_json` (`:4802`), `test_batch_2_after_batch_1_transitions_to_executed` (`:4852`), `test_execute_quality_advisories_flow_into_batch_artifacts_aggregate_and_next_prompt` (`:4884`), `test_execute_quality_config_disable_suppresses_file_growth_deviation_end_to_end` (`:4975`), `test_batch_out_of_range_raises` (`:5039`), `test_batch_2_without_batch_1_raises_prerequisites` (`:5051`), `test_batch_1_on_single_batch_plan_transitions_to_executed` (`:5064`), `test_light_batch_1_on_single_batch_plan_transitions_to_done` (`:5108`), `test_batch_1_incomplete_tracking_returns_blocked` (`:5156`).
2. **Keep** batch helpers (`_setup_two_batch_plan`, `_batch_worker`) local to this module — they're only consumed by batch tests. They do not need to move to `conftest.py`.

### Step 10: Create `tests/test_review.py`
**Scope:** Medium
1. **Move**:
   - `test_validate_merge_inputs_filters_malformed_entries` (`:3299`)
   - `test_validate_merge_inputs_rejects_empty_required_content` (`:3336`)
   - `test_validate_merge_inputs_accepts_array_fields` (`:3358`)
   - `test_validate_merge_inputs_rejects_empty_reviewer_verdict` (`:3399`)
   - `test_validate_merge_inputs_rejects_empty_sense_check_verdict` (`:3420`)
   - `test_duplicate_sense_check_verdict_dedup` (`:3439`)
   - `test_is_substantive_reviewer_verdict_*` (`:3459`, `:3464`, `:3468`, `:3472`)
   - `test_review_flags_incomplete_verdicts` (`:3699`)
   - `test_validate_merge_inputs_tracks_deviations` (`:3719`), `test_validate_merge_inputs_non_list_returns_empty` (`:3739`)
   - `test_review_blocks_incomplete_coverage_and_allows_rerun` (`:3829`)
   - `test_review_blocks_empty_evidence_files_without_substantive_verdict` (`:4418`), `test_review_softens_substantive_verdict_without_evidence_files_and_can_kick_back` (`:4477`)
   - `test_review_works_after_batch_by_batch_execution` (`:5200`)
   - `test_validate_merge_inputs_accepts_blocked_status` (`:5238`)
   - `test_execution_merge_config_includes_blocked_status` (`:5264`)

### Step 11: Create `tests/test_audits.py`
**Scope:** Small
1. **Move** debt-CLI and setup/config/plumbing tests that don't belong to a workflow phase:
   - `test_global_setup_creates_files` (`:2514`), `test_global_setup_skips_not_installed` (`:2523`), `test_global_setup_idempotent` (`:2531`), `test_global_setup_force_overwrites` (`:2540`), `test_global_setup_multiple_agents` (`:2551`), `test_global_setup_installs_codex_subagent_appendix` (`:2562`)
   - `test_load_save_config_roundtrip` (`:2582`), `test_load_config_corrupt_json` (`:2590`), `test_config_dir_xdg` (`:2599`), `test_setup_global_writes_config` (`:2605`)
   - `test_step_command_help_and_parser_shape` (`:2619`)
   - `test_init_produces_json` (`:2915`), `test_list_returns_empty` (`:2931`), `test_invalid_command_returns_error` (`:2940`)
   - `test_debt_list_on_empty_registry_returns_success` (`:2946`), `test_debt_add_and_list_increment_matching_entry` (`:2964`), `test_debt_resolve_hides_entry_from_default_list_but_not_all` (`:3022`)
   - `test_setup_local_creates_agents_file` (`:3069`)
   - `test_config_show` (`:3080`), `test_config_set_and_reset` (`:3088`), `test_config_set_invalid_key` (`:3100`), `test_config_set_invalid_step` (`:3107`), `test_config_set_invalid_agent` (`:3114`)

### Step 12: Create `tests/test_types_schemas.py`
**Scope:** Small
1. **Move** parsing, schema normalization, and types-layer tests (file name must differ from the existing `tests/test_schemas.py`):
   - `test_parse_claude_envelope_*` (`:2639`, `:2646`, `:2653`, `:2660`, `:2666`, `:2673`, `:2680`)
   - `test_parse_json_file_valid` (`:2687`), `test_parse_json_file_missing` (`:2694`), `test_parse_json_file_non_object` (`:2700`)
   - `test_validate_payload_valid_pass` (`:2708`), `test_validate_payload_missing_keys_raise` (`:2713`), `test_validate_payload_unknown_step_noop` (`:2719`)
   - `test_extract_session_id_*` (`:2730`, `:2736`, `:2742`, `:2748`, `:2753`)
   - `test_strict_schema_*` from `test_megaplan.py` (`:2763`, `:2769`, `:2775`, `:2781`, `:2808`, `:2824`, `:2843`) — preserve all; they differ from `tests/test_schemas.py` counterparts (verified by function-name diff).
   - `test_codex_uses_same_prompt_builders_for_shared_steps` (`:4542`)
   - `test_load_plan_migrates_legacy_evaluated_state` (`:4557`)

### Step 13: Delete `tests/test_megaplan.py` and verify parity
**Scope:** Small
1. **Verify** no test name has been dropped: compute `sorted` function-name lists from the new modules vs the original file and ensure set-equality (ignoring helpers). Also confirm every `@pytest.mark.parametrize` decorator travelled with its function.
2. **Delete** `tests/test_megaplan.py`.
3. **Run** `python -m pytest --collect-only -q > /tmp/megaplan_tests_after.txt` and diff against the pre-split list restricted to the moved tests. The set of collected test IDs (after renaming module prefixes) must be identical; the total count of the moved tests must equal the original `N`.
4. **Run** the full suite: `python -m pytest -q`. Every test that passed before must still pass; no new failures introduced.

## Execution Order
1. Inventory (Step 1) — capture baseline before any file edits so we have a concrete ledger to diff against later.
2. `conftest.py` (Step 2) — every subsequent test file depends on helpers living there.
3. Create the ten phase-scoped files (Steps 3–12). Order doesn't matter functionally but going top-to-bottom through `test_megaplan.py` keeps line-reference cross-checking easier. Steps 3–12 can in principle run in parallel across multiple sessions; serialize here for clarity.
4. Delete `test_megaplan.py` last (Step 13) — deleting earlier would make it painful to cross-reference source lines during the moves.

## Validation Order
1. After Step 2, run the full suite once: pytest should still collect the original `test_megaplan.py` alongside the (empty) conftest and pass — this catches accidental breakage of the helper move (e.g., the fixture not being discovered) before any tests depend on it.
2. After each of Steps 3–12, run the new file in isolation: `python -m pytest tests/test_<phase>.py -q`. Cheap, targeted, and pinpoints import/fixture errors immediately.
3. After Step 13, run `pytest --collect-only -q` and confirm the collected-test count equals the pre-split total (for the moved-test subset). Then run `pytest -q` for the final pass/fail parity check.


        Plan metadata:
        {
  "version": 1,
  "timestamp": "2026-04-21T11:00:15Z",
  "hash": "sha256:695fccd04299ff078fd649ef82737c81a16f74cf57509e34f41f375aa1176d73",
  "questions": [
    "Is it OK that `tests/test_schemas.py` and `tests/test_config.py` already exist, so the types/schemas bucket lands as `tests/test_types_schemas.py` and the config/CLI-plumbing tests from `test_megaplan.py` land in `tests/test_audits.py` rather than being merged into the existing files? (Avoids touching files owned by other test groups and avoids function-name collisions within a module.)",
    "The `strict_schema` tests in `test_megaplan.py` (e.g. `test_strict_schema_overwrites_partial_required_arrays_recursively`) look like near-duplicates of similarly named tests in `tests/test_schemas.py` (`test_strict_schema_normalizes_...`). The brief says 'preserve every test's behavior' \u2014 is it correct to keep both sets rather than dedupe?",
    "Is it acceptable to import helpers with `from tests.conftest import read_json, load_state, ...` given precedent at `tests/test_tiny_robustness.py:10`? (Alternative is a sibling `tests/_megaplan_helpers.py` module to avoid importing from conftest.)",
    "Should `tests/test_prep.py` be created even though only one test (`test_cli_registers_prep_command`) currently belongs to it, or should that test ride along in `tests/test_init_plan.py`? Current plan creates the file per the explicit bucket list."
  ],
  "success_criteria": [
    {
      "criterion": "`tests/test_megaplan.py` no longer exists in the repository.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "The full test suite passes: `python -m pytest -q` exits 0 with no new failures or errors compared to the pre-split run.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Collected test count for the migrated functions is preserved: `pytest --collect-only -q` after the split reports a count equal to the pre-split count (baseline captured in Step 1), accounting for parametrized expansions.",
      "priority": "must",
      "requires": [
        "run_tests",
        "run_shell"
      ]
    },
    {
      "criterion": "Every `def test_*` function that existed in the original `tests/test_megaplan.py` (per `grep '^def test_' tests/test_megaplan.py`, 201 matches) appears in exactly one new test module under `tests/`, with its `@pytest.mark.parametrize` decorator(s) intact.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_shell"
      ]
    },
    {
      "criterion": "No file under `megaplan/` (the source package) has been modified by this change.",
      "priority": "must",
      "requires": [
        "parse_diff",
        "run_shell"
      ]
    },
    {
      "criterion": "`tests/conftest.py` exists and defines `plan_fixture`; the suite still discovers it (the handful of tests that take `plan_fixture` still run and pass).",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "The ten phase-scoped files exist: `tests/test_init_plan.py`, `tests/test_prep.py`, `tests/test_critique.py`, `tests/test_revise.py`, `tests/test_gate.py`, `tests/test_finalize.py`, `tests/test_execute.py`, `tests/test_review.py`, `tests/test_audits.py`, `tests/test_types_schemas.py`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Helper bodies moved to `tests/conftest.py` are byte-for-byte identical to the originals at `tests/test_megaplan.py:39-232` (no silent refactoring of shared helpers).",
      "priority": "should",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Each new test file stays under roughly 1500 lines so no single split ends up as another mega-file; if any exceeds that, consider a finer split (e.g., splitting `test_execute.py` into `test_execute.py` + `test_execute_batch.py`).",
      "priority": "should",
      "requires": [
        "run_shell"
      ]
    },
    {
      "criterion": "Imports in each new file are minimal \u2014 only what that file's tests actually reference \u2014 rather than copying the full 35-line import block from `test_megaplan.py` into every module.",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "No existing test file outside `tests/test_megaplan.py` is modified by this change (existing `tests/test_schemas.py`, `tests/test_config.py`, etc. stay byte-identical).",
      "priority": "should",
      "requires": [
        "parse_diff"
      ]
    }
  ],
  "assumptions": [
    "The parallel refactor on `megaplan/` source does not rename any public symbol imported by `tests/test_megaplan.py` (`handle_init`, `STATE_*`, `WorkerResult`, `validate_plan_structure`, etc.). If it does, the test imports in the new files must match whatever the source ends up exporting \u2014 but updating source imports is out of scope; coordinate with the parallel branch at merge time.",
    "`tests/__init__.py` remains an empty/near-empty package marker, so `from tests.conftest import ...` works (already demonstrated by `tests/test_tiny_robustness.py:10` importing from `tests.test_handle_review_robustness`).",
    "pytest will still auto-discover `plan_fixture` from `tests/conftest.py` for every test file under `tests/` \u2014 no per-file `import` needed for the fixture itself.",
    "The `audits` bucket is meant to hold workflow-adjacent plumbing (debt CLI, config, setup) rather than the `megaplan/audit.py` tiebreaker-audit module (which has no corresponding tests in `test_megaplan.py`). The task's 'audits' naming therefore refers to the CLI-audit/plumbing tests, not tiebreaker audit.",
    "It is acceptable to use a file name other than `tests/test_schemas.py` (which already exists) for the types/schemas bucket; `tests/test_types_schemas.py` is chosen.",
    "`test_cli_registers_prep_command` is the sole prep-only test today; creating `tests/test_prep.py` for it is preferable to folding it into `test_init_plan.py` because the task's bucket list explicitly includes `prep`.",
    "The combined line count of the ten new files may still be roughly 5274 lines (since we are moving, not trimming). That's expected \u2014 the win is per-file locality, not total line reduction."
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
      "id": "DEBT-009",
      "concern": "are the proposed changes technically correct?: the mobile action-surface plan is technically incorrect for the current component structure. `submissioncarouselcard` hides `footercontent` below the `md` breakpoint (`src/components/submissioncarouselcard.tsx:219`), while `submissionscarouselpage` also hides the score panel on mobile via `asidecontent={<div classname=\"hidden md:block\">...` and passes `hideactions` to `scorepanel` at `src/pages/submissionscarouselpage.tsx:250-263,347`. reusing that pattern for entrypage would leave mobile users with no navigation controls and no scoring controls.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-010",
      "concern": "are the proposed changes technically correct?: i checked the sign-in callback path again. `submissionslayout` already wires `usescoring(..., { onrequiresignin: () => pagemachine.dispatch({ type: 'open_sign_in_modal' }) })` at `src/pages/submissionslayout.tsx:38-40`, and `scorepanel` still has its own `onrequiresignin` prop. the revised step 4.2 is acceptable only if it explicitly rewires that prop to `pagemachine.dispatch`; otherwise removing local modal state would orphan the direct ui callback. the plan hints at this, but it remains easy to misread because the scoring-context callback and the scorepanel prop are separate mechanisms.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-029",
      "concern": "are the proposed changes technically correct?: checked the new diff-helper proposal against the repo's existing execution-evidence semantics. `validate_execution_evidence()` in `megaplan/evaluation.py:109-175` uses `git status --short`, so untracked files count as real changed files today, but step 3 proposes `collect_git_diff_patch(project_dir)` via `git diff head`; by git behavior that will not include untracked files, so heavy review could miss exactly the newly created files that execute and review already treat as part of the patch.",
      "occurrence_count": 1,
      "plan_ids": [
        "robust-review-v2"
      ]
    },
    {
      "id": "DEBT-032",
      "concern": "are the proposed changes technically correct?: a generated-schema gap remains. `tests/test_schemas.py` reads the repo-root `.megaplan/schemas/review.json` directly via `_review_disk_schema()`, the checked-in local file is currently stale relative to `schemas`, and `ensure_runtime_layout()` in `megaplan/_core/io.py` is the production writer for that file class. the plan says generated schemas must stay aligned, but it never names a regeneration step or a test adjustment for that disk-schema path, so the validation story is still incomplete.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-6-remaining-openai-20260409-0502"
      ]
    },
    {
      "id": "DEBT-046",
      "concern": "are the proposed changes technically correct?: the new pre-extraction step that migrates `pinnedshotgroups` out of core is still under-specified for compatibility. current runtime and test code reads `config.pinnedshotgroups` directly across `hooks/usetimelinecommit.ts`, `lib/pinned-group-projection.ts`, `hooks/useshotgroups.ts`, `components/timelineeditor/timelineeditor.tsx`, `hooks/usetimelinetrackmanagement.ts`, `lib/serialize.test.ts`, `lib/migrate.test.ts`, and many other tests, so landing that migration before extraction needs a dual-read/projection shim or a clearly synchronized update plan instead of only a schema/serializer note.",
      "occurrence_count": 1,
      "plan_ids": [
        "design-plan-to-extract-the-20260419-1637"
      ]
    },
    {
      "id": "DEBT-050",
      "concern": "are the proposed changes technically correct?: runner inputs: the revised auto-mode snippet calls `$(cat ${idea_file})` and the chain-mode path runs `mp-chain ${chain_spec}`, but step 7's deploy flow still only does `railway link`, `railway variables --set`, and `railway up`. there is no corresponding step that copies the idea file or chain spec into `/workspace`, so a literal implementation would boot into auto/chain mode and immediately fail on missing input files.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-megaplan-cloud-a-new-20260421-0406"
      ]
    }
  ],
  "are-the-success-criteria-well-prioritized-and-verifiable": [
    {
      "id": "DEBT-019",
      "concern": "are the success criteria well-prioritized and verifiable?: mobile behavior is still under-prioritized relative to the actual risk in this repo. the user constraint specifically mentions the mobile bottom nav, but the only mobile-specific success criterion left is 'mobile scoring ux is coherent' at `info` level. given that the plan currently removes the working mobile nav, there should be at least a `should` or `must` criterion stating that mobile users retain navigation and scoring controls.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    }
  ],
  "completeness": [
    {
      "id": "DEBT-036",
      "concern": "handle_init() and override flows also emit next_step but aren't listed for next_step_runtime enrichment.",
      "occurrence_count": 1,
      "plan_ids": [
        "design-and-plan-calibrated-20260410-1430"
      ]
    },
    {
      "id": "DEBT-037",
      "concern": "handle_execute() at handlers.py:1152-1175 can clear next_step to none but leave stale next_step_runtime.",
      "occurrence_count": 1,
      "plan_ids": [
        "design-and-plan-calibrated-20260410-1430"
      ]
    },
    {
      "id": "DEBT-040",
      "concern": "next_step_runtime fires on previous step completion, not literally when the next phase starts.",
      "occurrence_count": 1,
      "plan_ids": [
        "design-and-plan-calibrated-20260410-1430"
      ]
    },
    {
      "id": "DEBT-043",
      "concern": "test_command config override unreachable via normal init/cli flow",
      "occurrence_count": 1,
      "plan_ids": [
        "add-test-baselining-to-the-20260410-2240"
      ]
    }
  ],
  "correctness": [
    {
      "id": "DEBT-038",
      "concern": "status-progress gating excludes finalized plans with finalize.json in between-batch and blocked states.",
      "occurrence_count": 1,
      "plan_ids": [
        "design-and-plan-calibrated-20260410-1430"
      ]
    },
    {
      "id": "DEBT-039",
      "concern": "resolve_phase_runtime called on non-phase next_step values would fail.",
      "occurrence_count": 1,
      "plan_ids": [
        "design-and-plan-calibrated-20260410-1430"
      ]
    },
    {
      "id": "DEBT-041",
      "concern": "non-phase next_step values from workflow_next() not filtered.",
      "occurrence_count": 1,
      "plan_ids": [
        "design-and-plan-calibrated-20260410-1430"
      ]
    },
    {
      "id": "DEBT-042",
      "concern": "baseline_test_command schema says string-only but fallback returns none",
      "occurrence_count": 1,
      "plan_ids": [
        "add-test-baselining-to-the-20260410-2240"
      ]
    },
    {
      "id": "DEBT-044",
      "concern": "fallback uses null+baseline_test_note instead of brief's empty-array+meta_commentary",
      "occurrence_count": 1,
      "plan_ids": [
        "add-test-baselining-to-the-20260410-2240"
      ]
    },
    {
      "id": "DEBT-045",
      "concern": "pinnedshotgroups migration lacks a specified compatibility phase for in-tree callers",
      "occurrence_count": 1,
      "plan_ids": [
        "design-plan-to-extract-the-20260419-1637"
      ]
    }
  ],
  "criteria-prompt": [
    {
      "id": "DEBT-026",
      "concern": "criteria prompt: v3 replaces `_review_prompt()` in heavy mode with a new `heavy_criteria_review_prompt`, so the plan no longer follows the brief's explicit requirement that `_review_prompt()` remain the heavy-mode `criteria_verdict` check.",
      "occurrence_count": 1,
      "plan_ids": [
        "robust-review-v2"
      ]
    }
  ],
  "did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements": [
    {
      "id": "DEBT-011",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: a new critical issue is introduced on mobile. step 4.9 says to remove entrypage's mobile sticky bottom nav and 'use the same `footercontent` slot in submissioncarouselcard', but `src/components/submissioncarouselcard.tsx:217-221` renders `footercontent` inside `classname=\"hidden md:block\"`. in the current repo, the mobile sticky nav at `src/pages/entrypage.tsx:283-340` is the only mobile surface for back/next and the score toggle, so the revised plan would remove working mobile controls and replace them with a slot that is explicitly hidden on phones.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-012",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the plan still contradicts itself on mobile behavior. assumption #3 says the browse-mode mobile score toggle will be preserved, but step 4.9 removes the entire mobile sticky nav that contains that toggle in `src/pages/entrypage.tsx:314-330`. the implementer cannot satisfy both instructions as written.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-028",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: checked step 7 against the brief's explicit prompt-builder requirement. the revision fixes the old context leak by introducing a brand-new `heavy_criteria_review_prompt`, but the brief said `_review_prompt()` should stay as-is and still run as the `criteria_verdict` check in heavy mode; v3 solves the problem by replacing that heavy-mode criteria path instead of reusing the baseline review prompt, which is still a material divergence from the requested design.",
      "occurrence_count": 1,
      "plan_ids": [
        "robust-review-v2"
      ]
    },
    {
      "id": "DEBT-047",
      "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: issue hints: the plan now wires `mode=auto|chain|idle`, but the user-requested `auto.idea_file` and `chain.spec` still have no deployment path into the container. reigh's readme uploads the idea file explicitly before running `megaplan init`, and `chain.sh` exits if `/workspace/chain.yaml` is missing, so a plan that only sets these paths in `cloud.yaml` without also staging the files still leaves the requested runner modes incomplete.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-megaplan-cloud-a-new-20260421-0406"
      ]
    }
  ],
  "diff-capture": [
    {
      "id": "DEBT-027",
      "concern": "diff capture: the proposed `collect_git_diff_patch(project_dir)` helper uses `git diff head`, which will miss untracked files even though the existing execution-evidence path already treats untracked files as real changed work.",
      "occurrence_count": 1,
      "plan_ids": [
        "robust-review-v2"
      ]
    }
  ],
  "does-the-change-touch-all-locations-and-supporting-infrastructure": [
    {
      "id": "DEBT-018",
      "concern": "does the change touch all locations and supporting infrastructure?: if the implementation really wants `footercontent` to carry mobile actions, the plan must also include a supporting change in `src/components/submissioncarouselcard.tsx` or render a separate mobile control surface outside the card. right now step 4.9 removes the mobile nav but does not list `submissioncarouselcard.tsx:217-221` as a place that must change, so the required glue for mobile controls is missing.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-033",
      "concern": "does the change touch all locations and supporting infrastructure?: the prior missing locations in `megaplan/workers.py` and `tests/test_workers.py` are now covered, but one supporting-infrastructure path is still absent from the steps: the repo-root generated schema copy under `.megaplan/schemas/review.json` and the tests that read it directly. without either explicitly regenerating that file or changing those tests to materialize schemas in a temp root, the plan can still leave the runtime-schema copy out of sync with the raw registry.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-6-remaining-openai-20260409-0502"
      ]
    },
    {
      "id": "DEBT-035",
      "concern": "does the change touch all locations and supporting infrastructure?: the plan adds _set_active_step and _clear_active_step helpers to handlers.py. _run_worker (handlers.py:135) is modified to accept a `resolved` parameter. but _run_worker is also called directly by handle_critique's sequential fallback at line 801 and 803. these calls currently don't pass `resolved`. the plan's step 2.6 for handle_critique says to set active_step after resolution at line 794 \u2014 but the _run_worker calls at 801/803 would re-resolve the agent internally (since `resolved` isn't passed). this means the agent is resolved twice on the critique sequential path. the double-resolution is wasteful but correct (same result). however, to match the plan's goal of 'resolve_agent_mode() is called once per handler invocation', the resolved tuple should be passed to these _run_worker calls too.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-megaplan-s-planning-20260409-2103"
      ]
    },
    {
      "id": "DEBT-048",
      "concern": "does the change touch all locations and supporting infrastructure?: supporting infrastructure is still missing for mode inputs. step 3 ports `chain.yaml.example` into package templates, but step 5's `materialize_deploy_dir()` layout does not include it, step 7 deploy does not upload it or `auto.idea_file`, and the docs/validation steps do not mention any artifact-sync path before boot. that leaves the runner depending on files that the deployment plan never places on the container volume.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-megaplan-cloud-a-new-20260421-0406"
      ]
    }
  ],
  "execute-phase-contract": [
    {
      "id": "DEBT-003",
      "concern": "early-killed baselines pass truncated output to the execute worker, which may produce lower-quality diagnosis than full output.",
      "occurrence_count": 1,
      "plan_ids": [
        "design-and-implement-a-20260327-0512"
      ]
    }
  ],
  "find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them": [
    {
      "id": "DEBT-014",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: i checked the skip caller path against the real hook behavior and `removefromqueue(entryid)` looks redundant. `scoring.skipentry(entryid)` optimistically adds the id to `skippedentryids` in `src/hooks/usescoring.ts:245-249`, and `usecarouselqueue` already reactively filters skipped entries from `submissions[]` in `src/hooks/usecarouselqueue.ts:154-165`. calling `removefromqueue()` immediately afterward is safe, but it duplicates an existing state transition and should be justified as an explicit ux optimization rather than required logic.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-015",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the direct ui sign-in caller is still important here. `scorepanel` invokes its own `onrequiresignin` prop when an unauthenticated user interacts with the score ui (`src/components/scorepanel.tsx:499-515`), which is independent of the scoring hook's internal `requireauth()` path. the plan should be read as requiring that caller to dispatch `open_sign_in_modal`; otherwise one caller remains broken even if `submitscore()` is correctly wired.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-034",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: i rechecked the caller paths after the revision. the raw-schema caller path through `validate_payload()` is now accounted for, but the runtime-schema caller path still is not: `strict_schema()` only reaches the on-disk runtime schemas through `ensure_runtime_layout()`, while current tests like `tests/test_schemas.py` and `tests/test_parallel_review.py` consume the already-written repo copy directly. the plan does not yet say how that caller path gets refreshed or asserted after the code change.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-6-remaining-openai-20260409-0502"
      ]
    },
    {
      "id": "DEBT-051",
      "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the real callers for these paths are shell commands that expect actual files. reigh's readme uploads an idea file into `/workspace/megaplan-idea-2week.txt` before calling `megaplan init`, and `chain.sh` immediately checks `-f \"$spec\"` before running `megaplan chain --spec \"$spec\"`. the revised plan now constructs equivalent callers from `auto.idea_file` and `chain.spec`, but still never adds the corresponding file-transfer or materialization step, so those callers would receive nonexistent arguments.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-megaplan-cloud-a-new-20260421-0406"
      ]
    }
  ],
  "handler-boilerplate": [
    {
      "id": "DEBT-004",
      "concern": "_run_worker() pseudocode hardcodes iteration=state['iteration'] but handle_plan and handle_revise use different failure iteration values.",
      "occurrence_count": 1,
      "plan_ids": [
        "clean-up-and-properly-20260331-0149"
      ]
    },
    {
      "id": "DEBT-005",
      "concern": "same issue as correctness-1: failure iteration would be wrong for plan/revise handlers.",
      "occurrence_count": 1,
      "plan_ids": [
        "clean-up-and-properly-20260331-0149"
      ]
    }
  ],
  "install-paths": [
    {
      "id": "DEBT-023",
      "concern": "local setup path doesn't expose subagent mode",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-megaplan-skill-so-20260406-1818"
      ]
    },
    {
      "id": "DEBT-024",
      "concern": "no automated guard to keep the mirror file synchronized with source files",
      "occurrence_count": 1,
      "plan_ids": [
        "update-all-documentation-20260406-1902"
      ]
    },
    {
      "id": "DEBT-025",
      "concern": "local setup test only checks agents.md existence, not content",
      "occurrence_count": 1,
      "plan_ids": [
        "update-all-documentation-20260406-1902"
      ]
    }
  ],
  "is-there-convincing-verification-for-the-change": [
    {
      "id": "DEBT-016",
      "concern": "is there convincing verification for the change?: the test-plan details still miss a small but real infrastructure update: the current `locationdisplay` helper in `src/pages/submissionscarouselpage.test.tsx:289-291` only renders `location.pathname`, so the step 7 requirement to assert `{ state: { carousel: true, navdirection: 'forward' } }` cannot be implemented unless that helper is extended to expose `location.state`. the same pattern exists in the related page tests.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-017",
      "concern": "is there convincing verification for the change?: there is still no explicit mobile regression test in the plan, even though the revised implementation proposal removes the only current mobile nav/score surface. given the repository's actual component structure, a mobile-focused test or visual verification step is needed to prove controls remain accessible below `md`.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    }
  ],
  "mobile-ui": [
    {
      "id": "DEBT-020",
      "concern": "mobile ui: removing entrypage's mobile sticky nav and relying on `submissioncarouselcard.footercontent` would break mobile navigation and scoring because that footer slot is hidden below the `md` breakpoint.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    }
  ],
  "runner-inputs": [
    {
      "id": "DEBT-052",
      "concern": "runner inputs: auto and chain modes still assume `auto.idea_file` and `chain.spec` already exist on the container volume, but the deploy plan does not upload or materialize those files anywhere.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-megaplan-cloud-a-new-20260421-0406"
      ]
    }
  ],
  "runtime-schema-sync": [
    {
      "id": "DEBT-031",
      "concern": "runtime schema sync: the plan still does not include an explicit refresh or validation step for the generated `.megaplan/schemas/review.json` copy that repository tests read directly.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-6-remaining-openai-20260409-0502"
      ]
    }
  ],
  "search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader": [
    {
      "id": "DEBT-013",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the mobile problem is broader than entrypage. `submissionscarouselpage` already has a pre-existing mobile gap because its score panel is desktop-only and its footer actions are also hidden on mobile (`src/pages/submissionscarouselpage.tsx:250-263,347-354` plus `src/components/submissioncarouselcard.tsx:219`). the revised plan says entrypage should 'match the carouselpage pattern', which would spread that existing gap into the one page that currently has working mobile controls.",
      "occurrence_count": 1,
      "plan_ids": [
        "move-the-entry-page-into-20260401-0450"
      ]
    },
    {
      "id": "DEBT-030",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the revised plan correctly narrows the schema-shape problem itself back to the six audited mismatches, but the generated runtime-schema consumer path is broader than the plan acknowledges: `tests/test_parallel_review.py` also reads the runtime `review.json` schema from `schemas_root(repo_root)`, so stale generated schema copies can affect more than the direct schema tests.",
      "occurrence_count": 1,
      "plan_ids": [
        "fix-the-6-remaining-openai-20260409-0502"
      ]
    },
    {
      "id": "DEBT-049",
      "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: input provisioning is the broader unresolved concept here. the repo's current railway workflow does not just run commands; it also stages runtime artifacts into `/workspace` first, such as the uploaded idea text in readme line 103 and the expected `/workspace/chain.yaml` consumed by `chain.sh`. the revised plan fixes the runner dispatch itself, but it still treats `auto.idea_file` and `chain.spec` as if those files will already exist without describing how cloud deploy makes that true.",
      "occurrence_count": 1,
      "plan_ids": [
        "build-megaplan-cloud-a-new-20260421-0406"
      ]
    }
  ],
  "subagent-safeguards": [
    {
      "id": "DEBT-021",
      "concern": "hermes reference safeguard numbers not validated against actual implementation",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-megaplan-skill-so-20260406-1818"
      ]
    },
    {
      "id": "DEBT-022",
      "concern": "plan's retry caps (1 phase, 3 execute) may differ from hermes-agent's actual policy",
      "occurrence_count": 1,
      "plan_ids": [
        "refactor-megaplan-skill-so-20260406-1818"
      ]
    }
  ],
  "worker-permissions": [
    {
      "id": "DEBT-001",
      "concern": "codex --full-auto flag only triggers for step == 'execute', not 'loop_execute'",
      "occurrence_count": 1,
      "plan_ids": [
        "build-megaloop-a-minimal-20260327-0250"
      ]
    },
    {
      "id": "DEBT-002",
      "concern": "claude --permission-mode bypasspermissions only triggers for step == 'execute', not 'loop_execute'",
      "occurrence_count": 1,
      "plan_ids": [
        "build-megaloop-a-minimal-20260327-0250"
      ]
    }
  ],
  "workflow-state-machine": [
    {
      "id": "DEBT-006",
      "concern": "_plan_prompt() does not read research.json, so replanning from state_researched would ignore research results.",
      "occurrence_count": 1,
      "plan_ids": [
        "clean-up-and-properly-20260331-0149"
      ]
    },
    {
      "id": "DEBT-007",
      "concern": "same issue as correctness-2: state_researched \u2192 plan path is only partially wired.",
      "occurrence_count": 1,
      "plan_ids": [
        "clean-up-and-properly-20260331-0149"
      ]
    },
    {
      "id": "DEBT-008",
      "concern": "_plan_prompt() is a missed location for the state_researched \u2192 plan change.",
      "occurrence_count": 1,
      "plan_ids": [
        "clean-up-and-properly-20260331-0149"
      ]
    }
  ]
}

        Escalated debt subsystems:
        [
  {
    "subsystem": "are-the-proposed-changes-technically-correct",
    "total_occurrences": 6,
    "plan_count": 5,
    "entries": [
      {
        "id": "DEBT-009",
        "concern": "are the proposed changes technically correct?: the mobile action-surface plan is technically incorrect for the current component structure. `submissioncarouselcard` hides `footercontent` below the `md` breakpoint (`src/components/submissioncarouselcard.tsx:219`), while `submissionscarouselpage` also hides the score panel on mobile via `asidecontent={<div classname=\"hidden md:block\">...` and passes `hideactions` to `scorepanel` at `src/pages/submissionscarouselpage.tsx:250-263,347`. reusing that pattern for entrypage would leave mobile users with no navigation controls and no scoring controls.",
        "occurrence_count": 1,
        "plan_ids": [
          "move-the-entry-page-into-20260401-0450"
        ]
      },
      {
        "id": "DEBT-010",
        "concern": "are the proposed changes technically correct?: i checked the sign-in callback path again. `submissionslayout` already wires `usescoring(..., { onrequiresignin: () => pagemachine.dispatch({ type: 'open_sign_in_modal' }) })` at `src/pages/submissionslayout.tsx:38-40`, and `scorepanel` still has its own `onrequiresignin` prop. the revised step 4.2 is acceptable only if it explicitly rewires that prop to `pagemachine.dispatch`; otherwise removing local modal state would orphan the direct ui callback. the plan hints at this, but it remains easy to misread because the scoring-context callback and the scorepanel prop are separate mechanisms.",
        "occurrence_count": 1,
        "plan_ids": [
          "move-the-entry-page-into-20260401-0450"
        ]
      },
      {
        "id": "DEBT-029",
        "concern": "are the proposed changes technically correct?: checked the new diff-helper proposal against the repo's existing execution-evidence semantics. `validate_execution_evidence()` in `megaplan/evaluation.py:109-175` uses `git status --short`, so untracked files count as real changed files today, but step 3 proposes `collect_git_diff_patch(project_dir)` via `git diff head`; by git behavior that will not include untracked files, so heavy review could miss exactly the newly created files that execute and review already treat as part of the patch.",
        "occurrence_count": 1,
        "plan_ids": [
          "robust-review-v2"
        ]
      },
      {
        "id": "DEBT-032",
        "concern": "are the proposed changes technically correct?: a generated-schema gap remains. `tests/test_schemas.py` reads the repo-root `.megaplan/schemas/review.json` directly via `_review_disk_schema()`, the checked-in local file is currently stale relative to `schemas`, and `ensure_runtime_layout()` in `megaplan/_core/io.py` is the production writer for that file class. the plan says generated schemas must stay aligned, but it never names a regeneration step or a test adjustment for that disk-schema path, so the validation story is still incomplete.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-6-remaining-openai-20260409-0502"
        ]
      },
      {
        "id": "DEBT-046",
        "concern": "are the proposed changes technically correct?: the new pre-extraction step that migrates `pinnedshotgroups` out of core is still under-specified for compatibility. current runtime and test code reads `config.pinnedshotgroups` directly across `hooks/usetimelinecommit.ts`, `lib/pinned-group-projection.ts`, `hooks/useshotgroups.ts`, `components/timelineeditor/timelineeditor.tsx`, `hooks/usetimelinetrackmanagement.ts`, `lib/serialize.test.ts`, `lib/migrate.test.ts`, and many other tests, so landing that migration before extraction needs a dual-read/projection shim or a clearly synchronized update plan instead of only a schema/serializer note.",
        "occurrence_count": 1,
        "plan_ids": [
          "design-plan-to-extract-the-20260419-1637"
        ]
      },
      {
        "id": "DEBT-050",
        "concern": "are the proposed changes technically correct?: runner inputs: the revised auto-mode snippet calls `$(cat ${idea_file})` and the chain-mode path runs `mp-chain ${chain_spec}`, but step 7's deploy flow still only does `railway link`, `railway variables --set`, and `railway up`. there is no corresponding step that copies the idea file or chain spec into `/workspace`, so a literal implementation would boot into auto/chain mode and immediately fail on missing input files.",
        "occurrence_count": 1,
        "plan_ids": [
          "build-megaplan-cloud-a-new-20260421-0406"
        ]
      }
    ]
  },
  {
    "subsystem": "correctness",
    "total_occurrences": 6,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-038",
        "concern": "status-progress gating excludes finalized plans with finalize.json in between-batch and blocked states.",
        "occurrence_count": 1,
        "plan_ids": [
          "design-and-plan-calibrated-20260410-1430"
        ]
      },
      {
        "id": "DEBT-039",
        "concern": "resolve_phase_runtime called on non-phase next_step values would fail.",
        "occurrence_count": 1,
        "plan_ids": [
          "design-and-plan-calibrated-20260410-1430"
        ]
      },
      {
        "id": "DEBT-041",
        "concern": "non-phase next_step values from workflow_next() not filtered.",
        "occurrence_count": 1,
        "plan_ids": [
          "design-and-plan-calibrated-20260410-1430"
        ]
      },
      {
        "id": "DEBT-042",
        "concern": "baseline_test_command schema says string-only but fallback returns none",
        "occurrence_count": 1,
        "plan_ids": [
          "add-test-baselining-to-the-20260410-2240"
        ]
      },
      {
        "id": "DEBT-044",
        "concern": "fallback uses null+baseline_test_note instead of brief's empty-array+meta_commentary",
        "occurrence_count": 1,
        "plan_ids": [
          "add-test-baselining-to-the-20260410-2240"
        ]
      },
      {
        "id": "DEBT-045",
        "concern": "pinnedshotgroups migration lacks a specified compatibility phase for in-tree callers",
        "occurrence_count": 1,
        "plan_ids": [
          "design-plan-to-extract-the-20260419-1637"
        ]
      }
    ]
  },
  {
    "subsystem": "completeness",
    "total_occurrences": 4,
    "plan_count": 2,
    "entries": [
      {
        "id": "DEBT-036",
        "concern": "handle_init() and override flows also emit next_step but aren't listed for next_step_runtime enrichment.",
        "occurrence_count": 1,
        "plan_ids": [
          "design-and-plan-calibrated-20260410-1430"
        ]
      },
      {
        "id": "DEBT-037",
        "concern": "handle_execute() at handlers.py:1152-1175 can clear next_step to none but leave stale next_step_runtime.",
        "occurrence_count": 1,
        "plan_ids": [
          "design-and-plan-calibrated-20260410-1430"
        ]
      },
      {
        "id": "DEBT-040",
        "concern": "next_step_runtime fires on previous step completion, not literally when the next phase starts.",
        "occurrence_count": 1,
        "plan_ids": [
          "design-and-plan-calibrated-20260410-1430"
        ]
      },
      {
        "id": "DEBT-043",
        "concern": "test_command config override unreachable via normal init/cli flow",
        "occurrence_count": 1,
        "plan_ids": [
          "add-test-baselining-to-the-20260410-2240"
        ]
      }
    ]
  },
  {
    "subsystem": "did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements",
    "total_occurrences": 4,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-011",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: a new critical issue is introduced on mobile. step 4.9 says to remove entrypage's mobile sticky bottom nav and 'use the same `footercontent` slot in submissioncarouselcard', but `src/components/submissioncarouselcard.tsx:217-221` renders `footercontent` inside `classname=\"hidden md:block\"`. in the current repo, the mobile sticky nav at `src/pages/entrypage.tsx:283-340` is the only mobile surface for back/next and the score toggle, so the revised plan would remove working mobile controls and replace them with a slot that is explicitly hidden on phones.",
        "occurrence_count": 1,
        "plan_ids": [
          "move-the-entry-page-into-20260401-0450"
        ]
      },
      {
        "id": "DEBT-012",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: the plan still contradicts itself on mobile behavior. assumption #3 says the browse-mode mobile score toggle will be preserved, but step 4.9 removes the entire mobile sticky nav that contains that toggle in `src/pages/entrypage.tsx:314-330`. the implementer cannot satisfy both instructions as written.",
        "occurrence_count": 1,
        "plan_ids": [
          "move-the-entry-page-into-20260401-0450"
        ]
      },
      {
        "id": "DEBT-028",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: checked step 7 against the brief's explicit prompt-builder requirement. the revision fixes the old context leak by introducing a brand-new `heavy_criteria_review_prompt`, but the brief said `_review_prompt()` should stay as-is and still run as the `criteria_verdict` check in heavy mode; v3 solves the problem by replacing that heavy-mode criteria path instead of reusing the baseline review prompt, which is still a material divergence from the requested design.",
        "occurrence_count": 1,
        "plan_ids": [
          "robust-review-v2"
        ]
      },
      {
        "id": "DEBT-047",
        "concern": "did the work fully address the issue hints, user notes, and approved plan requirements?: issue hints: the plan now wires `mode=auto|chain|idle`, but the user-requested `auto.idea_file` and `chain.spec` still have no deployment path into the container. reigh's readme uploads the idea file explicitly before running `megaplan init`, and `chain.sh` exits if `/workspace/chain.yaml` is missing, so a plan that only sets these paths in `cloud.yaml` without also staging the files still leaves the requested runner modes incomplete.",
        "occurrence_count": 1,
        "plan_ids": [
          "build-megaplan-cloud-a-new-20260421-0406"
        ]
      }
    ]
  },
  {
    "subsystem": "does-the-change-touch-all-locations-and-supporting-infrastructure",
    "total_occurrences": 4,
    "plan_count": 4,
    "entries": [
      {
        "id": "DEBT-018",
        "concern": "does the change touch all locations and supporting infrastructure?: if the implementation really wants `footercontent` to carry mobile actions, the plan must also include a supporting change in `src/components/submissioncarouselcard.tsx` or render a separate mobile control surface outside the card. right now step 4.9 removes the mobile nav but does not list `submissioncarouselcard.tsx:217-221` as a place that must change, so the required glue for mobile controls is missing.",
        "occurrence_count": 1,
        "plan_ids": [
          "move-the-entry-page-into-20260401-0450"
        ]
      },
      {
        "id": "DEBT-033",
        "concern": "does the change touch all locations and supporting infrastructure?: the prior missing locations in `megaplan/workers.py` and `tests/test_workers.py` are now covered, but one supporting-infrastructure path is still absent from the steps: the repo-root generated schema copy under `.megaplan/schemas/review.json` and the tests that read it directly. without either explicitly regenerating that file or changing those tests to materialize schemas in a temp root, the plan can still leave the runtime-schema copy out of sync with the raw registry.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-6-remaining-openai-20260409-0502"
        ]
      },
      {
        "id": "DEBT-035",
        "concern": "does the change touch all locations and supporting infrastructure?: the plan adds _set_active_step and _clear_active_step helpers to handlers.py. _run_worker (handlers.py:135) is modified to accept a `resolved` parameter. but _run_worker is also called directly by handle_critique's sequential fallback at line 801 and 803. these calls currently don't pass `resolved`. the plan's step 2.6 for handle_critique says to set active_step after resolution at line 794 \u2014 but the _run_worker calls at 801/803 would re-resolve the agent internally (since `resolved` isn't passed). this means the agent is resolved twice on the critique sequential path. the double-resolution is wasteful but correct (same result). however, to match the plan's goal of 'resolve_agent_mode() is called once per handler invocation', the resolved tuple should be passed to these _run_worker calls too.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-megaplan-s-planning-20260409-2103"
        ]
      },
      {
        "id": "DEBT-048",
        "concern": "does the change touch all locations and supporting infrastructure?: supporting infrastructure is still missing for mode inputs. step 3 ports `chain.yaml.example` into package templates, but step 5's `materialize_deploy_dir()` layout does not include it, step 7 deploy does not upload it or `auto.idea_file`, and the docs/validation steps do not mention any artifact-sync path before boot. that leaves the runner depending on files that the deployment plan never places on the container volume.",
        "occurrence_count": 1,
        "plan_ids": [
          "build-megaplan-cloud-a-new-20260421-0406"
        ]
      }
    ]
  },
  {
    "subsystem": "find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them",
    "total_occurrences": 4,
    "plan_count": 3,
    "entries": [
      {
        "id": "DEBT-014",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: i checked the skip caller path against the real hook behavior and `removefromqueue(entryid)` looks redundant. `scoring.skipentry(entryid)` optimistically adds the id to `skippedentryids` in `src/hooks/usescoring.ts:245-249`, and `usecarouselqueue` already reactively filters skipped entries from `submissions[]` in `src/hooks/usecarouselqueue.ts:154-165`. calling `removefromqueue()` immediately afterward is safe, but it duplicates an existing state transition and should be justified as an explicit ux optimization rather than required logic.",
        "occurrence_count": 1,
        "plan_ids": [
          "move-the-entry-page-into-20260401-0450"
        ]
      },
      {
        "id": "DEBT-015",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the direct ui sign-in caller is still important here. `scorepanel` invokes its own `onrequiresignin` prop when an unauthenticated user interacts with the score ui (`src/components/scorepanel.tsx:499-515`), which is independent of the scoring hook's internal `requireauth()` path. the plan should be read as requiring that caller to dispatch `open_sign_in_modal`; otherwise one caller remains broken even if `submitscore()` is correctly wired.",
        "occurrence_count": 1,
        "plan_ids": [
          "move-the-entry-page-into-20260401-0450"
        ]
      },
      {
        "id": "DEBT-034",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: i rechecked the caller paths after the revision. the raw-schema caller path through `validate_payload()` is now accounted for, but the runtime-schema caller path still is not: `strict_schema()` only reaches the on-disk runtime schemas through `ensure_runtime_layout()`, while current tests like `tests/test_schemas.py` and `tests/test_parallel_review.py` consume the already-written repo copy directly. the plan does not yet say how that caller path gets refreshed or asserted after the code change.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-6-remaining-openai-20260409-0502"
        ]
      },
      {
        "id": "DEBT-051",
        "concern": "find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the real callers for these paths are shell commands that expect actual files. reigh's readme uploads an idea file into `/workspace/megaplan-idea-2week.txt` before calling `megaplan init`, and `chain.sh` immediately checks `-f \"$spec\"` before running `megaplan chain --spec \"$spec\"`. the revised plan now constructs equivalent callers from `auto.idea_file` and `chain.spec`, but still never adds the corresponding file-transfer or materialization step, so those callers would receive nonexistent arguments.",
        "occurrence_count": 1,
        "plan_ids": [
          "build-megaplan-cloud-a-new-20260421-0406"
        ]
      }
    ]
  },
  {
    "subsystem": "install-paths",
    "total_occurrences": 3,
    "plan_count": 2,
    "entries": [
      {
        "id": "DEBT-023",
        "concern": "local setup path doesn't expose subagent mode",
        "occurrence_count": 1,
        "plan_ids": [
          "refactor-megaplan-skill-so-20260406-1818"
        ]
      },
      {
        "id": "DEBT-024",
        "concern": "no automated guard to keep the mirror file synchronized with source files",
        "occurrence_count": 1,
        "plan_ids": [
          "update-all-documentation-20260406-1902"
        ]
      },
      {
        "id": "DEBT-025",
        "concern": "local setup test only checks agents.md existence, not content",
        "occurrence_count": 1,
        "plan_ids": [
          "update-all-documentation-20260406-1902"
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
        "id": "DEBT-013",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the mobile problem is broader than entrypage. `submissionscarouselpage` already has a pre-existing mobile gap because its score panel is desktop-only and its footer actions are also hidden on mobile (`src/pages/submissionscarouselpage.tsx:250-263,347-354` plus `src/components/submissioncarouselcard.tsx:219`). the revised plan says entrypage should 'match the carouselpage pattern', which would spread that existing gap into the one page that currently has working mobile controls.",
        "occurrence_count": 1,
        "plan_ids": [
          "move-the-entry-page-into-20260401-0450"
        ]
      },
      {
        "id": "DEBT-030",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: the revised plan correctly narrows the schema-shape problem itself back to the six audited mismatches, but the generated runtime-schema consumer path is broader than the plan acknowledges: `tests/test_parallel_review.py` also reads the runtime `review.json` schema from `schemas_root(repo_root)`, so stale generated schema copies can affect more than the direct schema tests.",
        "occurrence_count": 1,
        "plan_ids": [
          "fix-the-6-remaining-openai-20260409-0502"
        ]
      },
      {
        "id": "DEBT-049",
        "concern": "search for related code that handles the same concept. is the reported issue a symptom of something broader?: input provisioning is the broader unresolved concept here. the repo's current railway workflow does not just run commands; it also stages runtime artifacts into `/workspace` first, such as the uploaded idea text in readme line 103 and the expected `/workspace/chain.yaml` consumed by `chain.sh`. the revised plan fixes the runner dispatch itself, but it still treats `auto.idea_file` and `chain.spec` as if those files will already exist without describing how cloud deploy makes that true.",
        "occurrence_count": 1,
        "plan_ids": [
          "build-megaplan-cloud-a-new-20260421-0406"
        ]
      }
    ]
  },
  {
    "subsystem": "workflow-state-machine",
    "total_occurrences": 3,
    "plan_count": 1,
    "entries": [
      {
        "id": "DEBT-006",
        "concern": "_plan_prompt() does not read research.json, so replanning from state_researched would ignore research results.",
        "occurrence_count": 1,
        "plan_ids": [
          "clean-up-and-properly-20260331-0149"
        ]
      },
      {
        "id": "DEBT-007",
        "concern": "same issue as correctness-2: state_researched \u2192 plan path is only partially wired.",
        "occurrence_count": 1,
        "plan_ids": [
          "clean-up-and-properly-20260331-0149"
        ]
      },
      {
        "id": "DEBT-008",
        "concern": "_plan_prompt() is a missed location for the state_researched \u2192 plan change.",
        "occurrence_count": 1,
        "plan_ids": [
          "clean-up-and-properly-20260331-0149"
        ]
      }
    ]
  }
]

        Debt guidance:
        - These are known accepted limitations. Do not re-flag them unless the current plan makes them worse, broadens them, or fails to contain them.
        - Prefix every new concern with a subsystem tag followed by a colon, for example `Timeout recovery: retry backoff remains brittle`.
        - When a concern is recurring debt that still needs to be flagged, prefix it with `Recurring debt:` after the subsystem tag, for example `Timeout recovery: Recurring debt: retry backoff remains brittle`.



        Your output template is at: /Users/user_c042661f/Documents/megaplan/.megaplan/plans/split-tests-test-megaplan-py-20260421-1255/critique_output.json
Review the plan with a broad scope. Consider whether the approach is correct, whether it covers
all the places it needs to, whether it would break callers or violate codebase conventions,
and whether its verification strategy is adequate.

Place any concrete concerns in the `flags` array in the template file using the standard format
(id, concern, category, severity_hint, evidence). Leave `checks` as an empty array.

Workflow: read the file → investigate → read file again → add findings → write file back.

        Additional guidelines:
        - Robustness level: light. Be pragmatic. Only flag issues that would cause real failures. Ignore style, minor edge cases, and issues the executor will naturally resolve.
        - Over-engineering: prefer the simplest approach that fully solves the problem.
        - Reuse existing flag IDs when the same concern is still open.
        - `verified_flag_ids`: list flag IDs from prior iterations that the revised plan actually resolves (e.g., if the plan was revised to fix FLAG-001, and you confirm the fix is correct, include "FLAG-001"). Only include flags you've verified — don't guess.
        - Verify that the plan follows the expected structure when validator warnings or the outline suggest drift.
        - Additional flags may use these categories: correctness, security, completeness, performance, maintainability, other.
        - Focus on concrete issues, not structural formatting.

> AGENT

{"checks":[],"flags":[{"id":"FLAG-001","concern":"Verification: the plan hard-codes `python -m pytest` for baseline and final verification, but this repo requires Python >=3.11 and the current `python` resolves to 3.8.10. In this workspace, `python -m pytest tests/test_megaplan.py --collect-only -q` fails before collection with `ImportError: cannot import name 'NotRequired' from 'typing'`, so Steps 1 and 13 are not runnable as written unless the interpreter is pinned.","category":"verifiability","severity_hint":"likely-significant","evidence":"`pyproject.toml:9` declares `requires-python = \">=3.11\"`. Running `python --version` returns `Python 3.8.10`, and `python -m pytest tests/test_megaplan.py --collect-only -q` errors while importing `megaplan/types.py`."},{"id":"FLAG-002","concern":"Execution order: Step 2 says to move the shared helper block out of `tests/test_megaplan.py` into `tests/conftest.py` and then run the full suite before the split files exist, but the remaining `tests/test_megaplan.py` still calls those helpers throughout. Unless Step 2 also rewires the legacy module to import them from `tests.conftest`, the planned intermediate validation run will fail.","category":"completeness","severity_hint":"likely-minor","evidence":"Current `tests/test_megaplan.py` uses moved helpers well after line 232, for example `ensure_blocking_flags(...)` at `tests/test_megaplan.py:1370`, `latest_plan_name(...)` at `:1533`, `run_main_json(...)` at `:2954`, and `read_json(...)` at `:3510`."}],"verified_flag_ids":[],"disputed_flag_ids":[]}

> TOOL

tool_use update_plan
```json
{
  "plan": [
    {
      "step": "Read critique template and inspect the current test layout referenced by the plan",
      "status": "in_progress"
    },
    {
      "step": "Cross-check the proposed split against actual repository files and pytest collection behavior",
      "status": "pending"
    },
    {
      "step": "Write findings into the critique output JSON",
      "status": "pending"
    }
  ]
}
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "pwd && ls tests | sed -n '1,120p' && echo '---' && sed -n '1,200p' .megaplan/plans/split-tests-test-megaplan-py-20260421-1255/critique_output.json",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
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
  "cmd": "rg -n \"^def test_|^@pytest\\.mark\\.parametrize|^class |^@dataclass|^def _|^@pytest\\.fixture\" tests/test_megaplan.py",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
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
  "cmd": "sed -n '1,120p' pyproject.toml && echo '---' && sed -n '1,80p' tests/__init__.py && echo '---' && sed -n '1,80p' tests/test_tiny_robustness.py && echo '---' && ls tests/test_schemas.py tests/test_config.py",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
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
  "cmd": "rg -n \"test_megaplan|from tests\\.conftest|from tests\\.test_\" tests",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 8000,
  "yield_time_ms": 1000
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
  "cmd": "python -m pytest tests/test_megaplan.py --collect-only -q",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
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
  "cmd": "sed -n '1,240p' tests/test_megaplan.py",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
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
  "cmd": "python --version && python3 --version && command -v python && command -v python3 && command -v pytest",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 1000,
  "yield_time_ms": 1000
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
  "cmd": "rg -n \"python -m pytest|python3\\.11|requires-python|uv run pytest|pytest -q|tox|nox\" -S README* docs .github pyproject.toml tests | sed -n '1,200p'",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
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
  "cmd": "rg -n \"from tests\\.test_megaplan|import tests\\.test_megaplan|test_megaplan\\.py\" -S .",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
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
  "cmd": "command -v python3.11 && python3.11 --version",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 1000,
  "yield_time_ms": 1000
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
  "cmd": "PYENV_VERSION=3.11.11 python -m pytest tests/test_megaplan.py --collect-only -q | tail -n 5",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 2000,
  "yield_time_ms": 1000
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
  "cmd": "PYENV_VERSION=3.11.11 python -m pytest tests/test_megaplan.py --collect-only -q | wc -l",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 1000,
  "yield_time_ms": 1000
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
  "cmd": "PYENV_VERSION=3.11.11 python -m pytest tests/test_megaplan.py --collect-only -q >/tmp/megaplan_collect.txt && tail -n 3 /tmp/megaplan_collect.txt",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 2000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use write_stdin
```json
{
  "session_id": 22904,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 2000
}
```

> TOOL

tool_result write_stdin
```
null
```

> TOOL

tool_use write_stdin
```json
{
  "session_id": 52515,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 1000
}
```

> TOOL

tool_result write_stdin
```
null
```

> TOOL

tool_use write_stdin
```json
{
  "session_id": 33857,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 1000
}
```

> TOOL

tool_result write_stdin
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"_drive_to_finalized|_setup_two_batch_plan|_batch_worker|make_gate_worker_result|make_worker_sequence|latest_plan_name|ensure_blocking_flags|first_open_significant_flag|open_blocking_flags|run_main_json\\(\" tests/test_megaplan.py",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 6000,
  "yield_time_ms": 1000
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
  "cmd": "PYENV_VERSION=3.11.11 python - <<'PY'\nimport ast, pathlib\np = pathlib.Path('tests/test_megaplan.py')\nmod = ast.parse(p.read_text())\nfuncs = [n.name for n in mod.body if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]\nprint('test_defs', len(funcs))\nprint(funcs[:5])\nprint(funcs[-5:])\nPY",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 2000,
  "yield_time_ms": 1000
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
  "cmd": "PYENV_VERSION=3.11.11 python - <<'PY'\nfrom pathlib import Path\ntext=Path('tests/test_megaplan.py').read_text().splitlines()\nfor start,end in [(3288,3448),(3470,3515)]:\n    print(f'--- {start}-{end} ---')\n    for i in range(start,end+1):\n        if i<=len(text):\n            print(f'{i}:{text[i-1]}')\nPY",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 12000,
  "yield_time_ms": 1000
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
  "cmd": "rg -n \"tests/test_megaplan.py|test_megaplan\\.py\" tests/test_prompts.py tests/test_workers.py tests/test_core.py tests/test_auto.py tests/test_chain.py tests/test_quality.py tests/test_review_checks.py tests/test_review_mechanical.py tests/test_verifiability.py",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
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
  "cmd": "rg -n \"read_json\\(|load_state\\(|latest_plan_name\\(|ensure_blocking_flags\\(|run_main_json\\(|make_gate_worker_result\\(|make_worker_sequence\\(\" tests/test_megaplan.py | sed -n '1,120p'",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 4000,
  "yield_time_ms": 1000
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
  "cmd": "PYENV_VERSION=3.11.11 python - <<'PY'\nfrom pathlib import Path\ntext = Path('tests/test_megaplan.py').read_text().splitlines()\nfor i in [2954,1370,1533,3510]:\n    for j in range(i-2,i+3):\n        print(f'{j}:{text[j-1]}')\n    print('---')\nPY",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 3000,
  "yield_time_ms": 1000
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
  "cmd": "sed -n '1,120p' .megaplan/plans/split-tests-test-megaplan-py-20260421-1255/critique_output.json",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 1000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use update_plan
```json
{
  "explanation": "Repository cross-check found one hard verification issue and one step-order gap in the proposed helper move.",
  "plan": [
    {
      "step": "Read critique template and inspect the current test layout referenced by the plan",
      "status": "completed"
    },
    {
      "step": "Cross-check the proposed split against actual repository files and pytest collection behavior",
      "status": "completed"
    },
    {
      "step": "Write findings into the critique output JSON",
      "status": "in_progress"
    }
  ]
}
```

> TOOL

tool_use apply_patch
```json
{
  "patch": "*** Begin Patch\n*** Update File: /Users/user_c042661f/Documents/megaplan/.megaplan/plans/split-tests-test-megaplan-py-20260421-1255/critique_output.json\n@@\n-{\n-  \"checks\": [],\n-  \"flags\": [],\n-  \"verified_flag_ids\": [],\n-  \"disputed_flag_ids\": []\n-}\n+{\n+  \"checks\": [],\n+  \"flags\": [\n+    {\n+      \"id\": \"FLAG-001\",\n+      \"concern\": \"Verification: the plan hard-codes `python -m pytest` for baseline and final verification, but this repo requires Python >=3.11 and the current `python` resolves to 3.8.10. In this workspace, `python -m pytest tests/test_megaplan.py --collect-only -q` fails before collection with `ImportError: cannot import name 'NotRequired' from 'typing'`, so Steps 1 and 13 are not runnable as written unless the interpreter is pinned.\",\n+      \"category\": \"verifiability\",\n+      \"severity_hint\": \"likely-significant\",\n+      \"evidence\": \"`pyproject.toml:9` declares `requires-python = \\\">=3.11\\\"`. Running `python --version` returns `Python 3.8.10`, and `python -m pytest tests/test_megaplan.py --collect-only -q` errors while importing `megaplan/types.py`.\"\n+    },\n+    {\n+      \"id\": \"FLAG-002\",\n+      \"concern\": \"Execution order: Step 2 says to move the shared helper block out of `tests/test_megaplan.py` into `tests/conftest.py` and then run the full suite before the split files exist, but the remaining `tests/test_megaplan.py` still calls those helpers throughout. Unless Step 2 also rewires the legacy module to import them from `tests.conftest`, the planned intermediate validation run will fail.\",\n+      \"category\": \"completeness\",\n+      \"severity_hint\": \"likely-minor\",\n+      \"evidence\": \"Current `tests/test_megaplan.py` uses moved helpers well after line 232, for example `ensure_blocking_flags(...)` at `tests/test_megaplan.py:1370`, `latest_plan_name(...)` at `:1533`, `run_main_json(...)` at `:2954`, and `read_json(...)` at `:3510`.\"\n+    }\n+  ],\n+  \"verified_flag_ids\": [],\n+  \"disputed_flag_ids\": []\n+}\n*** End Patch\n"
}
```

> TOOL

tool_result apply_patch
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "cat .megaplan/plans/split-tests-test-megaplan-py-20260421-1255/critique_output.json",
  "workdir": "/Users/user_c042661f/Documents/megaplan",
  "max_output_tokens": 3000,
  "yield_time_ms": 1000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use update_plan
```json
{
  "plan": [
    {
      "step": "Read critique template and inspect the current test layout referenced by the plan",
      "status": "completed"
    },
    {
      "step": "Cross-check the proposed split against actual repository files and pytest collection behavior",
      "status": "completed"
    },
    {
      "step": "Write findings into the critique output JSON",
      "status": "completed"
    }
  ]
}
```

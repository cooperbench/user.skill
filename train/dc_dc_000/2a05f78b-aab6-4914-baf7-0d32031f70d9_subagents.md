> DEVELOPER

I need to understand the test patterns in this project to write doc-mode tests. Please find: 1. Look at tests/ directory - what test files exist, what patterns do they use (pytest fixtures, tmp_path, mocking, etc.) 2. Read tests/test_config.py to understand how handle_init is tested 3. Read tests/test_schemas.py to understand schema testing patterns 4. Look at any test that tests _write_finalize_artifacts or execution_timeout functions 5. Check how validate_execution_evidence is tested Focus on: fixture patterns, how state dicts are constructed, how handlers are called in tests. Give me file paths and key snippets.

> AGENT

I'll help you understand the test patterns in this project. Let me start by exploring the tests directory and then examining the specific test files you mentioned.

> AGENT

Now let me read the specific test files you requested:

> AGENT

Now let me search for tests related to `_write_finalize_artifacts`, `execution_timeout`, and `validate_execution_evidence`:

> AGENT

Now let me look at more test files to understand fixture patterns better:

> AGENT

Now let me check another test file to see more fixture patterns:

> AGENT

Let me search for more specific testing patterns around handlers and state dictionaries:

> AGENT

Now let me search for usage of `_build_mock_payload` and other handler testing patterns:

> AGENT

Let me look at the actual _build_mock_payload function:

> AGENT

Now let me check the execution_timeout function:

> AGENT

Let me check for tests that call handlers directly:

> AGENT

Now let me get a complete picture of one handler test to see the pattern:

> AGENT

Let me look at test patterns for finalize more closely:

> AGENT

Perfect! Now let me create a comprehensive summary. Let me also look at one more test file to understand how conftest fixtures work:

> AGENT

Perfect. Now I have enough information. Let me compile the findings: ## Test Patterns in megaplan Project Based on my analysis of the test suite, here are the key patterns for writing doc-mode tests: ### 1. **Fixture Patterns** - File Paths **Configuration fixtures** (`/Users/user_c042661f/Documents/megaplan/tests/test_config.py:16-26`): ```python @pytest.fixture def isolated_config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path: config_path = tmp_path / ".config" / "megaplan" def fake_config_dir(home: Path | None = None) -> Path: del home return config_path monkeypatch.setattr(io_module, "config_dir", fake_config_dir) monkeypatch.setattr(cli_module, "config_dir", fake_config_dir) return config_path ``` **Plan fixtures** (`/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py:88-138`): ```python @dataclass class PlanFixture: root: Path project_dir: Path plan_name: str plan_dir: Path make_args: Callable[..., Namespace] @pytest.fixture def plan_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> PlanFixture: return _make_plan_fixture_with_robustness(tmp_path, monkeypatch, robustness="standard") ``` ### 2. **State Dictionary Construction Patterns** From `/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:35-85` and `/Users/user_c042661f/Documents/megaplan/tests/test_parallel_critique.py:24-56`: State dicts follow a consistent structure with these key sections: - `name`, `idea`, `current_state`, `iteration`, `created_at` - `config`: Contains `project_dir`, `auto_approve`, `robustness` - `sessions`: Initially empty dict - `plan_versions`: List of version records with `version`, `file`, `hash`, `timestamp` - `history`: Initially empty list - `meta`: Contains `significant_counts`, `weighted_scores`, `plan_deltas`, `recurring_critiques`, `total_cost_usd`, `overrides`, `notes` - `last_gate`: Initially empty dict ### 3. **Scaffolding Patterns** From `/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:88-117`: ```python def _scaffold(tmp_path: Path, *, iteration: int = 1, flags: list[dict[str, object]] | None = None) -> tuple[Path, dict[str, object]]: plan_dir = tmp_path / "plan" plan_dir.mkdir() (tmp_path / "project").mkdir() flags = flags or [] _write_json(plan_dir / "faults.json", {"flags": flags}) _write_json(plan_dir / f"critique_v{iteration}.json", {...}) (plan_dir / f"plan_v{iteration}.md").write_text("new plan...", encoding="utf-8") _write_json(plan_dir / f"plan_v{iteration}.meta.json", {...}) return plan_dir, _state(tmp_path, iteration=iteration) ``` Key helper: `/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:30-32`: ```python def _write_json(path: Path, data: dict[str, object]) -> None: path.parent.mkdir(parents=True, exist_ok=True) path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8") ``` ### 4. **Handler Testing Patterns** From `/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py:460-490`: **Mocking workers for handler tests**: ```python def fake_run_step_with_worker(step: str, state: dict, plan_dir: Path, args: Namespace, **kwargs: object): del state, args, kwargs persisted = read_json(plan_dir / "state.json") observed.update(persisted["active_step"]) return ( WorkerResult( payload=_build_mock_payload(step, load_state(plan_dir), plan_dir), raw_output="{}", duration_ms=1, cost_usd=0.0, session_id="session-1", ), "codex", "persistent", False, ) monkeypatch.setattr(megaplan.handlers.worker_module, "run_step_with_worker", fake_run_step_with_worker) megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name)) ``` ### 5. **Testing validate_execution_evidence Patterns** From `/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:593-634`: ```python def test_validate_execution_evidence_flags_diff_mismatches_and_weak_notes( tmp_path: Path, monkeypatch: pytest.MonkeyPatch, ) -> None: project_dir = tmp_path / "project" (project_dir / ".git").mkdir(parents=True) (project_dir / "src").mkdir() (project_dir / "docs").mkdir() (project_dir / "src" / "existing.py").write_text("print('ok')\n", encoding="utf-8") (project_dir / "docs" / "new_name.py").write_text("x = 1\n", encoding="utf-8") finalize_data = { "tasks": [ { "id": "T1", "files_changed": ["src/existing.py", "docs/new_name.py", "ghost.py"], "executor_notes": "Verified src/existing.py and confirmed the rename...", } ], "sense_checks": [ {"id": "SC1", "executor_note": "ok"}, ], } monkeypatch.setattr( "megaplan.evaluation.subprocess.run", lambda *args, **kwargs: subprocess.CompletedProcess( args=["git", […]

> DEVELOPER

Read these files and give me the key function signatures and logic I need to test: 1. megaplan/handlers.py - find handle_init (the doc-mode validation: --output required, no absolute paths, no ../ traversal), and _write_finalize_artifacts (the doc-mode branch that skips test baseline and verification task) 2. megaplan/evaluation.py - find validate_execution_evidence and its doc-mode branch 3. megaplan/doc_assembly.py - the full file 4. megaplan/schemas.py - find get_execution_schema_key and the execution_doc.json schema entry 5. megaplan/execution_timeout.py - find _merge_timeout_checkpoint and _reset_timeout_invalid_tasks doc-mode branches 6. megaplan/types.py - find PlanConfig with mode/output_path fields Give me exact line numbers and the key conditional logic for each.

> AGENT

I'll read these files to find the key function signatures and logic you need to test.

> AGENT

Now let me read the handlers.py file in sections to find handle_init and _write_finalize_artifacts:

> AGENT

Now let me search for execution_timeout.py details:

> AGENT

Perfect! Now I have all the information I need. Let me compile the key findings: ## Key Function Signatures and Logic for Testing ### 1. **megaplan/handlers.py** **`handle_init()` - Lines 722-815** - **Doc-mode validation (lines 730-742):** - Line 730-731: `if mode == "doc" and not raw_output_path: raise CliError("invalid_args", "--output is required when --mode doc is selected")` - Line 734-735: Rejects absolute paths: `if output_candidate.is_absolute(): raise CliError("invalid_args", "--output must be a relative path inside the project directory")` - Line 736-737: Blocks `..` traversal: `if any(part == ".." for part in output_candidate.parts): raise CliError("invalid_args", "--output must not contain '..' path traversal")` - Line 738-742: Ensures output stays within project dir via `relative_to()` check **`_write_finalize_artifacts()` - Lines 376-389** - **Doc-mode branch (lines 377-380):** - Line 377: `if state["config"].get("mode") == "doc":` - Lines 378-380: Skips test baseline and verification task: - Sets `payload["baseline_test_failures"] = None` - Sets `payload["baseline_test_command"] = None` - Sets `payload["baseline_test_note"] = "Test baseline not applicable in doc mode."` - **Code-mode branch (lines 381-384):** Calls `_capture_test_baseline()` and `_ensure_verification_task()` --- ### 2. **megaplan/evaluation.py** **`validate_execution_evidence()` - Lines 123-126** - Router function: - Line 124: `if mode == "doc": return _validate_execution_evidence_doc(finalize_data, project_dir)` - Line 126: Else returns `_validate_execution_evidence_code(finalize_data, project_dir)` **`_validate_execution_evidence_doc()` - Lines 129-199** - **Key logic:** - Lines 137-145: Collects `claimed_sections` and `planned_sections` from task `sections_written` field - Lines 147-151: Checks for missing sections: `missing_sections = sorted(planned_sections - claimed_sections)` - Lines 154-159: Checks for unclaimed sections: `unclaimed = sorted(claimed_sections - planned_sections)` - Lines 170-179: Validates sense check acknowledgments (requires non-empty `executor_note`, rejects perfunctory acks) - Lines 181-191: Validates task executor_notes (rejects rubber stamps for done tasks) - Returns dict with `findings`, `files_in_diff: []`, `files_claimed: []`, `skipped: False` --- ### 3. **megaplan/doc_assembly.py** - Full file (Lines 1-118) **`extract_sections()` - Lines 13-31** - Maps `section_id → executor_notes` from done tasks' `sections_written` - Returns `dict[str, str]` **`assemble_doc()` - Lines 65-117** - Reads batch payloads (`execution_batch_N.json`) - Orders sections by task position using `_section_plan_order()` - Writes atomically to `output_path` via temp file + `os.replace()` --- ### 4. **megaplan/schemas.py** **`get_execution_schema_key()` - Lines 526-527** - Router: `return "execution_doc.json" if mode == "doc" else "execution.json"` **`execution_doc.json` schema - Built by `_build_execution_doc_schema()` Lines 505-523** - Line 507: Replaces `files_changed` with `sections_written` in root schema - Lines 508-511: Modifies task_update schema: - Adds `sections_written` property - Removes `commands_run` property - Required fields: `["task_id", "status", "executor_notes", "sections_written"]` - Stored in `SCHEMAS["execution_doc.json"]` at line 523 --- ### 5. **megaplan/execution_timeout.py** **`_merge_timeout_checkpoint()` - Lines 125-178** - **Doc-mode branch (lines […]

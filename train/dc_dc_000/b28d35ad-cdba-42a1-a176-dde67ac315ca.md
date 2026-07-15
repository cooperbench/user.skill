> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

You are creating an implementation plan for the following idea.





        Idea:
Add --from-doc <path> flag to megaplan init plus a standardized ## Settled Decisions section format for doc-mode output. When --from-doc points at a doc-mode megaplan artifact, the CLI validates the path (relative to project_dir, no absolute, no .., must exist), parses any ## Settled Decisions section via a new pure function doc_assembly.extract_settled_decisions, stores the path at state.config.from_doc, and injects extracted decisions into state.meta.imported_decisions. Load-bearing decisions (load_bearing: true) auto-promote to must-priority success criteria for the new plan; non-load-bearing become info-priority. Doc-mode execute prompt is updated to instruct the worker to emit the standard Settled Decisions section format. Reuses existing settled_decisions concept in evaluation.py (name the new imported type SettledDecisionFromDoc to avoid collision). Reuses the _validate_relative_path logic factored from the existing --output validation. Out of scope for this PR: critique-level auto-check for SD-* citation, sidecar settled_decisions.json, verify-against-doc subcommand.

User notes and answers:
- PRE-PLAN GUIDANCE (authoritative — do not re-derive):

### Files that will be touched
- megaplan/cli.py — add --from-doc to the init subparser
- megaplan/handlers.py::handle_init — validate --from-doc, call the parser, populate state.config.from_doc and state['meta']['imported_decisions']
- megaplan/doc_assembly.py — new extract_settled_decisions(doc_text: str) -> list[dict] pure function
- megaplan/types.py — add SettledDecisionFromDoc TypedDict if the shape warrants it
- megaplan/data/instructions.md — document --from-doc, the Settled Decisions section format, and how it interacts with success criteria
- megaplan/data/prompts/* or wherever doc-mode execute worker prompt lives — update to instruct the worker to emit ## Settled Decisions in the standard format when the subject produces any
- tests/test_handle_init_doc_mode.py — add tests for --from-doc validation (path must exist, must be inside project_dir, must parse cleanly)
- tests/test_doc_assembly.py OR new tests/test_settled_decisions.py — unit tests for the parser against fixture doc strings

### Load-bearing decisions (pre-settled — don't re-debate in critique)
- Parser lives in doc_assembly.py (pure function), not inline in handlers.py. Keeps handler thin and parser testable.
- Decision ID format is SD-NNN (SD- prefix + 3-digit zero-padded). Parser is tolerant of the 3-digit convention but stores the ID verbatim as written.
- load_bearing: true|false is the gate field. Only load_bearing: true decisions become must success criteria. Non-load-bearing are stored as info criteria for reference.
- --from-doc takes a path RELATIVE to --project-dir. Absolute paths rejected. .. rejected. Same safety as --output.
- --from-doc is valid with either --mode doc or --mode code, not just code. A doc plan can reference a prior doc.
- Missing ## Settled Decisions section is NOT an error. Parser returns empty list; meta.imported_decisions is empty; --from-doc still stores the path for worker context.
- Malformed entries within a well-formed section are logged but don't fail the parse (tolerant). Report parse warnings via the init response.

### Reuse what already exists, don't duplicate
- settled_decisions is already a first-class concept in megaplan/evaluation.py, megaplan/handlers.py, and megaplan/types.py — produced by gate/critique signals. Name the new type SettledDecisionFromDoc (distinct noun) to avoid collision with the existing gate-produced SettledDecision.
- --output validation logic at handlers.py::handle_init (absolute path rejection, .. rejection, relative-to-project enforcement) is the template for --from-doc validation. Factor both into a small _validate_relative_path(project_dir, raw_path, flag_name) helper to avoid duplication.

### Tests must cover
- Parser: 5+ fixture strings (empty doc, doc with no section, doc with 3 well-formed decisions, doc with malformed entry inside well-formed section, doc with section but no entries)
- handle_init with --from-doc pointing at a valid doc → config.from_doc set, meta.imported_decisions populated
- handle_init with --from-doc pointing at non-existent file → invalid_args with clear message
- handle_init with --from-doc pointing at absolute path → rejected
- handle_init with --from-doc pointing at a doc with zero decisions → succeeds, imported_decisions is empty list
- Full suite: PYENV_VERSION=3.11.11 python -m pytest tests/ must pass 690+ (current baseline 687 passed, 1 skipped).

### Out of scope (do NOT scope-creep)
- Full critique-level auto-check that verifies each SD-* is cited in the plan — follow-up
- Sidecar settled_decisions.json written by doc-mode finalize — follow-up
- megaplan verify-against-doc subcommand — follow-up
- Migrating existing doc-mode output to the new standard (convention starts with new plans)

        Project directory:
        /Users/user_c042661f/Documents/megaplan

        No prior clarification artifact exists. Identify ambiguities, ask clarifying questions, and state your assumptions inside the plan output.

        Requirements:
        - If the engineering brief suggests an approach, use it as your starting hypothesis — but before committing, consider if there's a simpler or more fundamental fix. The brief is well-researched input, not a final answer.
        - If the brief is absent, incomplete, or says "skip", inspect the repository yourself before planning.
        - Stay focused on the requested idea. If repo exploration surfaces unrelated issues or docs, ignore them and return to the task.
        - Prefer source code, tests, and directly relevant config files. Avoid `.megaplan/`, prior plan artifacts, and unrelated `docs/` or ops/deployment material unless the task explicitly depends on them.
        - Stop exploring once you have enough evidence to name the concrete touch points and validation path. Do not keep browsing after you can write the plan.
        - Produce a concrete implementation plan in markdown.
        - Define observable success criteria as objects with `criterion` (string) and `priority` (`must`, `should`, or `info`):
          - `must` — hard gate. The reviewer will block on failure. Use for correctness, functional requirements, and verifiable outcomes (e.g., "all existing tests pass", "API returns 200 for valid input"). Every `must` criterion must have a clear yes/no answer.
          - `should` — quality target. The reviewer flags but does not block. Use for subjective goals, numeric guidelines, and best-effort improvements (e.g., "file under ~300 lines", "no deeply nested conditionals", "each function has a single responsibility").
          - `info` — documented for humans, reviewer skips. Use for criteria that cannot be verified in this pipeline (e.g., "13 manual smoke tests pass", "stakeholder sign-off obtained").
        - Each success criterion should include a `requires` field listing the capabilities needed for verification. Valid capability strings: `run_shell`, `read_files`, `run_tests`, `parse_diff`, `read_build_output`, `run_linter` (container), `drive_browser`, `inspect_runtime_ui`, `observe_runtime_logs`, `subjective_judgment`, `verify_physical_device` (human). `must` criteria MUST have non-empty `requires`. Example: `{"criterion": "All tests pass", "priority": "must", "requires": ["run_tests"]}`.
        - Use the `questions` field for ambiguities that would materially change implementation.
        - Use the `assumptions` field for defaults you are making so planning can proceed now.
        - Prefer cheap validation steps early.
        - Keep the plan proportional to the task. A 1-line fix needs a 2-step plan (apply fix + run tests), not a 5-step investigation.
        - If user notes answer earlier questions, incorporate them into the draft plan instead of re-asking them.
        - Fix the problem fully. Do not limit scope just to avoid breaking existing tests — update the tests too if needed.
        - Prefer the simplest, most direct fix. No fallbacks, type conversions, or defensive wrappers without concrete evidence they are needed.
        - If the task or issue hints suggest a specific approach, follow it. Only deviate with concrete counter-evidence.

        Plan template — simple format (adapt to the actual repo and scope):
````md
# Implementation Plan: [Title]

## Overview
Summarize the goal, current repository shape, and the constraints that matter.

## Main Phase

### Step 1: Audit the current behavior (`megaplan/prompts.py`)
**Scope:** Small
1. **Inspect** the current implementation and call out the exact insertion points (`megaplan/prompts.py:29`).

### Step 2: Add the first change (`megaplan/evaluation.py`)
**Scope:** Medium
1. **Implement** the smallest viable change with exact file references (`megaplan/evaluation.py:1`).
2. **Capture** any tricky behavior with a short example.
   ```python
   issues = validate_plan_structure(plan_text)
   ```

### Step 3: Wire downstream behavior (`megaplan/handlers.py`, `megaplan/workers.py`)
**Scope:** Medium
1. **Update** the runtime flow in the touched files (`megaplan/handlers.py:400`, `megaplan/workers.py:199`).

### Step 4: Prove the change (`tests/test_evaluation.py`, `tests/test_megaplan.py`)
**Scope:** Small
1. **Run** the cheapest targeted checks first (`tests/test_evaluation.py:1`).
2. **Finish** with broader verification once the wiring is in place (`tests/test_megaplan.py:1`).

## Execution Order
1. Update prompts and mocks before enforcing stricter validation.
2. Land higher-risk wiring after the validator and tests are ready.

## Validation Order
1. Start with focused unit tests.
2. Run the broader suite after the flow changes are in place.
````

For complex plans, use multiple phases:
````md
## Phase 1: Foundation — Dependencies, DB, Types

### Step 1: Install dependencies (`package.json`)
...

### Step 2: Create database migration (`supabase/migrations/`)
...

## Phase 2: Core Integration

### Step 3: Port the main component (`src/components/`)
...
````

Template guidance:
- Simple plans: use `## Main Phase` with `### Step N:` sections underneath.
- Complex plans: use multiple `## Phase N:` sections, each containing `### Step N:` steps. Step numbers are global (not per-phase).
- The flat `## Step N:` format (without phases) also works for backwards compatibility.
- Key invariants: one H1 title, one `## Overview`, numbered step sections (`### Step N:` or `## Step N:`), and at least one ordering section.

> TOOL

tool_use Agent
```json
{
  "description": "Explore megaplan init/doc-mode code",
  "subagent_type": "Explore",
  "prompt": "I'm planning an implementation in the megaplan repo at /Users/user_c042661f/Documents/megaplan. I need to understand the current code shape to write an accurate plan. Please report back (under 400 words) with file paths and key line numbers for the following:\n\n1. `megaplan/cli.py` — where is the `init` subparser defined, and what args does it currently take? Is there an `--output` flag and a `--project-dir` flag, and where is `--mode doc` handled?\n\n2. `megaplan/handlers.py` — where is `handle_init` defined? Show me the shape of its validation for `--output` (the absolute/.. rejection logic). What does it return on invalid_args vs success? How does it populate `state.config` and `state['meta']`?\n\n3. `megaplan/doc_assembly.py` — does this file exist? If yes, what functions does it expose? If no, where would a new `doc_assembly.py` file logically belong?\n\n4. `megaplan/evaluation.py` — find the existing `settled_decisions` / `SettledDecision` concept. What's the TypedDict shape? Where are SettledDecisions produced by gate/critique?\n\n5. `megaplan/types.py` — show the existing TypedDict definitions especially for success criteria (must/should/info) and any `SettledDecision` type.\n\n6. `megaplan/data/instructions.md` — confirm it exists, note which sections already document init flags.\n\n7. Where does the doc-mode execute worker prompt live? Search for \"doc\" in `megaplan/data/prompts/` or similar.\n\n8. `tests/test_handle_init_doc_mode.py` — does it exist? If yes, what test style does it use (pytest? any fixtures)?\n\n9. `tests/test_doc_assembly.py` — does it exist?\n\n10. Is `PYENV_VERSION=3.11.11` the norm? Any pytest.ini or conftest.py I should know about?\n\nPlease give exact file paths and line numbers. Do not read .megaplan/ directory. Focus only on what I asked."
}
```

> TOOL

tool_result Agent
```
Perfect. Now I have all the information I need. Let me compile the final report:

---

## Code Shape Analysis: Megaplan Repository

### 1. `megaplan/cli.py` — init subparser

**Location:** `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:835-852`

The `init` subparser is defined in `build_parser()`:
- **Required args:** `--project-dir` (line 836), `idea` (positional, line 852)
- **Optional args:**
  - `--name` (line 837)
  - `--auto-approve` (line 838, action=store_true)
  - `--robustness` (line 839, choices: light/standard/robust/superrobust)
  - **`--mode`** (line 840-844): choices `["code", "doc", "metaplan"]`; help text describes `doc` vs `code` distinction
  - **`--output`** (line 845-847): relative path for doc artifact; help: "Required with --mode doc; rejected with --mode code"
  - `--hermes` (line 848-849)
  - `--phase-model` (line 850-851, action=append)

`--mode doc` is handled at lines 840-844 (parser definition) and then enforced in `handle_init` (line 736-737, where `metaplan` is aliased to `doc`).

---

### 2. `megaplan/handlers.py` — handle_init definition & validation

**Location:** `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:728-831`

**Function signature:** `def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:`

**Validation logic for `--output`:**
- Lines 739-753 (absolute/.. rejection):
  - Line 750-751: rejects absolute paths → `CliError("invalid_args", "...relative path inside...")`
  - Line 752-753: rejects `..` parts → `CliError("invalid_args", "--output must not contain '..' path traversal")`
  - Line 754-758: validates path stays within project_dir; raises `CliError("invalid_args", "--output must stay within...")`

**Mode/output coupling validation:**
- Line 739-744: if mode is `code` AND output provided → `CliError` (invalid_args)
- Line 746-747: if mode is `doc` AND NO output → `CliError` (invalid_args)

**Return on validation failure:** Raises `CliError` (caught by `main()` at line 1178, returns via `error_response()`)

**Return on success:** `StepResponse` dict (line 819-831) with `success=True`, `step="init"`, `plan=plan_name`, `state`, `auto_approve`, `robustness`

**State population:**
- `state.config` (lines 781-787): `project_dir`, `auto_approve`, `robustness`, `mode`, `agent` (hermes flag)
- Line 803: if output provided, adds `state["config"]["output_path"] = normalized_output_path`
- `state["meta"]` (lines 791-799): `significant_counts`, `weighted_scores`, `plan_deltas`, `recurring_critiques`, `total_cost_usd=0.0`, `overrides`, `notes`

---

### 3. `megaplan/doc_assembly.py` — does it exist?

**YES, file exists:** `/Users/user_c042661f/Documents/megaplan/megaplan/doc_assembly.py`

**Functions exposed:**
- `extract_sections(batch_payloads: list[dict]) -> dict[str, str]` (line 13)
- `assemble_doc(plan_dir: Path, output_path: Path, finalize_data: dict) -> Path` (line 65)
- `_task_order_index(finalize_data)` (line 34, private helper)
- `_section_plan_order(finalize_data, batch_payloads)` (line 43, private helper)

**Location in hierarchy:** `/megaplan/doc_assembly.py` — top-level megaplan module, peer to `handlers.py`, `evaluation.py`, etc.

---

### 4. `megaplan/evaluation.py` — settled_decisions concept

**File exists:** `/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py`

**SettledDecision TypedDict definition:** `/Users/user_c042661f/Documents/megaplan/megaplan/types.py:170-173`
```python
class SettledDecision(TypedDict, total=False):
    id: str
    decision: str
    rationale: str
```

**Where SettledDecisions are produced:**
- **Gate prompt** (`megaplan/prompts/gate.py`): produces `settled_decisions` as part of `GatePayload` in the worker response
- **Gate artifact builder** (`megaplan/evaluation.py:719`): `build_gate_artifact()` collects them from `gate_payload.get("settled_decisions", [])`
- **LastGateRecord** (`types.py:114-122`): includes `settled_decisions: list["SettledDecision"]`

Gate prompt instructs to populate `settled_decisions` with "design choices that should carry into review without re-litigation" (return `[]` when none apply).

---

### 5. `megaplan/types.py` — TypedDict definitions

**File location:** `/Users/user_c042661f/Documents/megaplan/megaplan/types.py`

**SettledDecision** (lines 170-173):
```python
class SettledDecision(TypedDict, total=False):
    id: str
    decision: str
    rationale: str
```

**Success criteria shape:** Not a TypedDict; defined structurally in `prompts/planning.py:120-124`:
- Each criterion is a dict with `criterion` (string), `priority` (enum: "must"/"should"/"info")
- Optional `requires` field listing capabilities (run_shell, read_files, run_tests, parse_diff, read_build_output, run_linter, drive_browser, inspect_runtime_ui, observe_runtime_logs, subjective_judgment, verify_physical_device)
- Returned by planning worker as `payload["success_criteria"]` (list of dicts)

**Related types:**
- `GatePayload` (line 188-193): includes `settled_decisions: list[SettledDecision]`
- `LastGateRecord` (line 114-122): includes `settled_decisions: list["SettledDecision"]` (line 119)
- `GateArtifact` (line 196-209): includes `settled_decisions: list[SettledDecision]` (line 205)

---

### 6. `megaplan/data/instructions.md` — existence & init flag docs

**File exists:** `/Users/user_c042661f/Documents/megaplan/megaplan/data/instructions.md`

**Sections documenting init flags:**
- **Lines 19-27:** "Modes" section — explains `--mode code` vs `--mode metaplan` (alias for doc), documents `--output` requirement
  - Line 27: "`--mode` and `--output` go together...rejects `--output` without `--mode metaplan` (error `invalid_args`), and rejects `--mode metaplan` without `--output`"
- **Lines 29-34:** "Start" section — launcher resolution (line 8 mentions `PYENV_VERSION=3.11.11`)
  - Line 31: shows example `<launcher> init --project-dir "$PROJECT_DIR" [--auto-approve] [--robustness light|standard|robust|superrobust] [--mode code|metaplan] [--output docs/foo.md] "$IDEA"`

---

### 7. Doc-mode execute worker prompt location

**Primary worker prompt:** `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py`

Contains doc-mode specific execution shape:
- Lines 28-50: `_EXECUTE_DOC_OUTPUT_SHAPE_EXAMPLE` shows expected task_updates schema with `sections_written` field instead of `files_changed`
- Imports doc-specific review prompt: `from .review_doc import ...` (implicit via imports)
- Contrast: `execute.py` handles code-mode execution with file changes

**Related prompts:**
- `megaplan/prompts/prep_doc.py` (doc-mode prep)
- `megaplan/prompts/review_doc.py` (doc-mode review)

---

### 8. `tests/test_handle_init_doc_mode.py` — exists?

**YES, file exists:** `/Users/user_c042661f/Documents/megaplan/tests/test_handle_init_doc_mode.py`

**Test style:** pytest with fixtures
- Uses `pytest.raises(CliError)` pattern (lines 58, 66, 77, 121)
- Fixtures: `tmp_path: Path`, `monkeypatch: pytest.MonkeyPatch` (standard pytest)
- Helper `_bootstrap()` (line 16) sets up temp filesystem and mocks `config_dir`
- Helper `_args()` (line 39) builds `argparse.Namespace` for test cases

**Tests included:**
- `test_doc_mode_requires_output` (line 56)
- `test_output_rejects_absolute_path` (line 64)
- `test_output_rejects_parent_traversal` (line 75)
- `test_doc_mode_accepts_relative_output` (line 86)
- `test_code_mode_without_output_succeeds` (line 99)
- `test_code_mode_with_output_is_rejected` (line 115)
- `test_metaplan_mode_is_alias_for_doc` (line 131)

---

### 9. `tests/test_doc_assembly.py` — exists?

**YES, file exists:** `/Users/user_c042661f/Documents/megaplan/tests/test_doc_assembly.py`

**Test style:** pytest
- Imports: `from megaplan.doc_assembly import assemble_doc, extract_sections`
- Fixture: `tmp_path: Path`
- Helper `_write_batch()` (line 12), `_finalize_with_tasks()` (line 19)

**Tests included:**
- `test_extract_sections_collects_done_only` (line 23)
- `test_assemble_doc_orders_sections_by_task_index` (line 46)
- `test_assemble_doc_is_idempotent` (line 70)
- `test_assemble_doc_handles_no_batches` (line 87)
- `test_assemble_doc_handles_empty_batch` (line 96)
- `test_assemble_doc_creates_parent_directory` (line 104)
- `test_assemble_doc_preserves_executor_written_file` (line 118)
- `test_assemble_doc_falls_back_when_file_empty` (line 132)
- `test_extract_sections_duplicate_section_id_last_wins` (line 146)

---

### 10. Python version & pytest configuration

**Python version norm:** `PYENV_VERSION=3.11.11`
- Mentioned in `megaplan/data/instructions.md:8` as launcher fallback
- Confirmed in `.megaplan/plans/*/final.md` artifacts (multiple mentions of "PYENV_VERSION=3.11.11 python -m pytest")
- `pyproject.toml:9` specifies `requires-python = ">=3.11"`

**Pytest configuration:** `/Users/user_c042661f/Documents/megaplan/pyproject.toml:32-33`
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

**conftest.py:** None found at repo root or in tests/ directory (uses monkeypatch fixtures inline)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 728,
  "limit": 110
}
```

> TOOL

tool_result Read
```
728	def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
729	    ensure_runtime_layout(root)
730	    project_dir = Path(args.project_dir).expanduser().resolve()
731	    if not project_dir.exists() or not project_dir.is_dir():
732	        raise CliError("invalid_project_dir", f"Project directory does not exist: {project_dir}")
733	    explicit_mode = getattr(args, "mode", None)
734	    raw_output_path = getattr(args, "output", None)
735	    mode = explicit_mode or "code"
736	    if mode == "metaplan":
737	        mode = "doc"
738	
739	    if mode == "code" and raw_output_path:
740	        raise CliError(
741	            "invalid_args",
742	            "--output is only valid with --mode doc. For code-mode runs, remove "
743	            "--output; for design-document runs, also pass --mode doc.",
744	        )
745	    normalized_output_path: str | None = None
746	    if mode == "doc" and not raw_output_path:
747	        raise CliError("invalid_args", "--output is required when --mode doc is selected")
748	    if raw_output_path:
749	        output_candidate = Path(raw_output_path)
750	        if output_candidate.is_absolute():
751	            raise CliError("invalid_args", "--output must be a relative path inside the project directory")
752	        if any(part == ".." for part in output_candidate.parts):
753	            raise CliError("invalid_args", "--output must not contain '..' path traversal")
754	        resolved_output_path = (project_dir / output_candidate).resolve()
755	        try:
756	            normalized_output_path = resolved_output_path.relative_to(project_dir).as_posix()
757	        except ValueError as exc:
758	            raise CliError("invalid_args", "--output must stay within the project directory") from exc
759	    robustness = getattr(args, "robustness", None)
760	    if robustness is None:
761	        robustness = get_effective("execution", "robustness")
762	    if robustness not in ROBUSTNESS_LEVELS:
763	        robustness = "standard"
764	    auto_approve_value = getattr(args, "auto_approve", None)
765	    if auto_approve_value is None:
766	        auto_approve_value = get_effective("execution", "auto_approve")
767	    auto_approve = bool(auto_approve_value)
768	    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
769	    plan_name = args.name or f"{slugify(args.idea)}-{timestamp}"
770	    plan_dir = plans_root(root) / plan_name
771	    if plan_dir.exists():
772	        raise CliError("duplicate_plan", f"Plan directory already exists: {plan_name}")
773	    plan_dir.mkdir(parents=True, exist_ok=False)
774	
775	    state: PlanState = {
776	        "name": plan_name,
777	        "idea": args.idea,
778	        "current_state": STATE_INITIALIZED,
779	        "iteration": 0,
780	        "created_at": now_utc(),
781	        "config": {
782	            "project_dir": str(project_dir),
783	            "auto_approve": auto_approve,
784	            "robustness": robustness,
785	            "mode": mode,
786	            "agent": "hermes" if getattr(args, "hermes", None) is not None else "",
787	        },
788	        "sessions": {},
789	        "plan_versions": [],
790	        "history": [],
791	        "meta": {
792	            "significant_counts": [],
793	            "weighted_scores": [],
794	            "plan_deltas": [],
795	            "recurring_critiques": [],
796	            "total_cost_usd": 0.0,
797	            "overrides": [],
798	            "notes": [],
799	        },
800	        "last_gate": {},
801	    }
802	    if normalized_output_path is not None:
803	        state["config"]["output_path"] = normalized_output_path
804	    append_history(
805	        state,
806	        make_history_entry(
807	            "init",
808	            duration_ms=0,
809	            cost_usd=0.0,
810	            result="success",
811	            environment={
812	                "claude": bool(find_command("claude")),
813	                "codex": bool(find_command("codex")),
814	            },
815	        ),
816	    )
817	    save_state(plan_dir, state)
818	    next_steps = workflow_next(state)
819	    response: StepResponse = {
820	        "success": True,
821	        "step": "init",
822	        "plan": plan_name,
823	        "state": STATE_INITIALIZED,
824	        "summary": f"Initialized plan '{plan_name}' for project {project_dir}",
825	        "artifacts": ["state.json"],
826	        "next_step": next_steps[0] if next_steps else None,
827	        "auto_approve": auto_approve,
828	        "robustness": robustness,
829	    }
830	    _attach_next_step_runtime(response)
831	    return response
832	
833	
834	def handle_plan(root: Path, args: argparse.Namespace) -> StepResponse:
835	    with load_plan_locked(root, args.plan, step="plan") as (plan_dir, state):
836	        require_state(state, "plan", {STATE_INITIALIZED, STATE_PREPPED, STATE_PLANNED})
837	        rerun = state["current_state"] == STATE_PLANNED
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 830,
  "limit": 30
}
```

> TOOL

tool_result Read
```
830	    setup_parser = subparsers.add_parser("setup", help="Install megaplan into agent configs (global by default)")
831	    setup_parser.add_argument("--local", action="store_true", help="Install AGENTS.md into a project instead of global agent configs")
832	    setup_parser.add_argument("--target-dir", help="Directory to install into (default: cwd, implies --local)")
833	    setup_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
834	
835	    init_parser = subparsers.add_parser("init")
836	    init_parser.add_argument("--project-dir", required=True)
837	    init_parser.add_argument("--name")
838	    init_parser.add_argument("--auto-approve", action="store_true", default=None)
839	    init_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
840	    init_parser.add_argument("--mode", choices=["code", "doc", "metaplan"], default=None,
841	                             help="Deliverable type: 'code' (source changes) or 'doc' / 'metaplan' "
842	                                  "(design/spec artifact — 'metaplan' is an alias for 'doc'). "
843	                                  "Defaults to 'code' unless the idea strongly suggests a design document, "
844	                                  "in which case --mode must be passed explicitly.")
845	    init_parser.add_argument("--output", default=None,
846	                             help="Relative path where the doc artifact will be written. "
847	                                  "Required with --mode doc; rejected with --mode code.")
848	    init_parser.add_argument("--hermes", nargs="?", const="", default=None,
849	                             help="Use Hermes agent for all phases. Optional: specify default model")
850	    init_parser.add_argument("--phase-model", action="append", default=[],
851	                             help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
852	    init_parser.add_argument("idea")
853	
854	    list_parser = subparsers.add_parser("list")
855	    list_parser.add_argument("--all", action="store_true",
856	                             help="Search all .megaplan directories system-wide (~)")
857	    list_parser.add_argument("--no-tree", action="store_true",
858	                             help="Only show plans from the current directory (default includes parent + child)")
859	    list_parser.add_argument("--include-done", action="store_true",
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py"
}
```

> TOOL

tool_result Read
```
1	"""Doc-mode execute prompt builders."""
2	
3	from __future__ import annotations
4	
5	import textwrap
6	from pathlib import Path
7	from typing import Any
8	
9	from megaplan._core import (
10	    batch_artifact_path,
11	    compute_task_batches,
12	    configured_robustness,
13	    intent_and_notes_block,
14	    json_dump,
15	    latest_plan_meta_path,
16	    read_json,
17	)
18	from megaplan.types import PlanState
19	
20	from ._shared import _debt_watch_lines, _render_prep_block
21	from .execute import (
22	    _execute_approval_note,
23	    _execute_nudges,
24	    _execute_rerun_guidance,
25	    _execute_review_block,
26	)
27	
28	_EXECUTE_DOC_OUTPUT_SHAPE_EXAMPLE = textwrap.dedent(
29	    """
30	    ```json
31	    {
32	      "output": "Authored the planned document sections.",
33	      "files_changed": [],
34	      "commands_run": [],
35	      "deviations": [],
36	      "task_updates": [
37	        {
38	          "task_id": "T1",
39	          "status": "done",
40	          "executor_notes": "Wrote the introduction section covering project motivation and scope.",
41	          "sections_written": ["introduction"]
42	        },
43	        {
44	          "task_id": "T2",
45	          "status": "done",
46	          "executor_notes": "Drafted the problem statement with three concrete examples from the codebase.",
47	          "sections_written": ["problem-statement"]
48	        },
49	        {
50	          "task_id": "T3",
51	          "status": "skipped",
52	          "executor_notes": "Skipped because the milestones depend on unresolved scope questions.",
53	          "sections_written": []
54	        }
55	      ],
56	      "sense_check_acknowledgments": [
57	        {
58	          "sense_check_id": "SC1",
59	          "executor_note": "Confirmed the introduction names the target audience and links to prior art."
60	        }
61	      ]
62	    }
63	    ```
64	    """
65	).strip()
66	
67	_EXECUTE_DOC_REQUIREMENTS_TEMPLATE = textwrap.dedent(
68	    """
69	    Requirements:
70	    - You are an author, not a coder. Your deliverable is document text, not code changes.
71	    - Write each assigned section to the configured output path. This is the only file you should create or modify.
72	    - Adapt if the document structure needs adjustment — report deviations explicitly.
73	    - Do not over-engineer beyond what the plan prescribes.
74	    - Output concrete sections written per task. `sections_written` means section IDs you authored — not sections you read or referenced.
75	    - Use the tasks in `finalize.json` as the execution boundary.
76	    - Best-effort progress checkpointing: if `{checkpoint_path}` is writable, then after each completed task read the full file, update that task's `status`, `executor_notes`, and `sections_written`, and write the full file back. Do NOT write to `finalize.json` directly — the harness owns that file.
77	    - Best-effort sense-check checkpointing: if `{checkpoint_path}` is writable, then after each sense check acknowledgment read the full file again, update that sense check's `executor_note`, and write the full file back.
78	    - Always use full read-modify-write updates for `{checkpoint_path}` instead of partial edits. If the sandbox blocks writes, continue execution and rely on the structured output below.
79	    - Structured output remains the authoritative final summary for this step. Disk writes are progress checkpoints for timeout recovery only.
80	    - Return `task_updates` with one object per completed or skipped task.
81	    - `task_updates[].status` must be either `done` or `skipped`. Never return `pending` in execute output.
82	    - Return `sense_check_acknowledgments` with one object per sense check.
83	    - Keep `executor_notes` verification-focused: explain why the section content is correct and complete.
84	    - Follow this JSON shape exactly:
85	    {output_shape}
86	    """
87	).strip()
88	
89	
90	def _execute_doc_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
91	    project_dir = Path(state["config"]["project_dir"])
92	    output_path = state["config"].get("output_path", "output.md")
93	    prep_block, prep_instruction = _render_prep_block(plan_dir)
94	    finalize_data = read_json(plan_dir / "finalize.json")
95	    checkpoint_path = str(plan_dir / "execution_checkpoint.json")
96	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
97	    gate = read_json(plan_dir / "gate.json")
98	    robustness = configured_robustness(state)
99	    prior_review_block = _execute_review_block(plan_dir)
100	    rerun_guidance = _execute_rerun_guidance(plan_dir, finalize_data)
101	    approval_note = _execute_approval_note(state)
102	    execution_nudges = _execute_nudges(finalize_data, plan_dir, root)
103	    requirements_block = _EXECUTE_DOC_REQUIREMENTS_TEMPLATE.format(
104	        checkpoint_path=checkpoint_path,
105	        output_shape=_EXECUTE_DOC_OUTPUT_SHAPE_EXAMPLE,
106	    )
107	    return textwrap.dedent(
108	        f"""
109	        Author the planned document sections.
110	
111	        Project directory:
112	        {project_dir}
113	
114	        Output path (write all sections here):
115	        {output_path}
116	
117	        {prep_block}
118	
119	        {prep_instruction}
120	
121	        {intent_and_notes_block(state)}
122	
123	        Execution tracking source of truth (`finalize.json`):
124	        {json_dump(finalize_data).strip()}
125	
126	        Absolute checkpoint path for best-effort progress checkpoints (NOT `finalize.json`):
127	        {checkpoint_path}
128	
129	        Plan metadata:
130	        {json_dump(latest_meta).strip()}
131	
132	        Gate summary:
133	        {json_dump(gate).strip()}
134	
135	        {prior_review_block}
136	
137	        {rerun_guidance}
138	
139	        {approval_note}
140	        Robustness level: {robustness}.
141	
142	        {requirements_block}
143	
144	        {execution_nudges}
145	        """
146	    ).strip()
147	
148	
149	def _execute_doc_batch_prompt(
150	    state: PlanState,
151	    plan_dir: Path,
152	    batch_task_ids: list[str],
153	    completed_task_ids: set[str] | None = None,
154	    root: Path | None = None,
155	) -> str:
156	    completed = set(completed_task_ids or set())
157	    output_path = state["config"].get("output_path", "output.md")
158	    finalize_data = read_json(plan_dir / "finalize.json")
159	    all_tasks = finalize_data.get("tasks", [])
160	    tasks_by_id = {
161	        task["id"]: task
162	        for task in all_tasks
163	        if isinstance(task, dict) and isinstance(task.get("id"), str)
164	    }
165	    batch_tasks = [
166	        tasks_by_id[task_id] for task_id in batch_task_ids if task_id in tasks_by_id
167	    ]
168	    completed_tasks = [
169	        task
170	        for task_id, task in tasks_by_id.items()
171	        if task_id in completed and task_id not in set(batch_task_ids)
172	    ]
173	    batch_sense_checks = [
174	        sense_check
175	        for sense_check in finalize_data.get("sense_checks", [])
176	        if sense_check.get("task_id") in set(batch_task_ids)
177	    ]
178	    batch_sense_check_ids = [
179	        sense_check["id"]
180	        for sense_check in batch_sense_checks
181	        if isinstance(sense_check.get("id"), str)
182	    ]
183	    global_batches = compute_task_batches(all_tasks)
184	    batch_number = next(
185	        (
186	            index + 1
187	            for index, batch in enumerate(global_batches)
188	            if batch == batch_task_ids
189	        ),
190	        1,
191	    )
192	    batch_total = len(global_batches) or 1
193	    checkpoint_path = str(batch_artifact_path(plan_dir, batch_number))
194	    prior_batch_deviations = "None"
195	    if batch_number > 1:
196	        prior_batch_artifact = batch_artifact_path(plan_dir, batch_number - 1)
197	        if prior_batch_artifact.exists():
198	            try:
199	                prior_batch_payload = read_json(prior_batch_artifact)
200	            except (OSError, ValueError):
201	                prior_batch_payload = {}
202	            raw_deviations = prior_batch_payload.get("deviations", [])
203	            if isinstance(raw_deviations, list):
204	                deviations = [item for item in raw_deviations if isinstance(item, str)]
205	                if deviations:
206	                    prior_batch_deviations = json_dump(deviations).strip()
207	    approval_note = _execute_approval_note(state)
208	    debt_watch_items = _debt_watch_lines(plan_dir, root)
209	    debt_watch_block = (
210	        "\n".join(
211	            [
212	                "Debt watch items (do not make these worse):",
213	                *[f"- {item}" for item in debt_watch_items],
214	            ]
215	        )
216	        if debt_watch_items
217	        else "Debt watch items (do not make these worse):\n- None."
218	    )
219	    return textwrap.dedent(
220	        f"""
221	        Author the planned document sections.
222	
223	        Project directory:
224	        {Path(state["config"]["project_dir"])}
225	
226	        Output path (write all sections here):
227	        {output_path}
228	
229	        {intent_and_notes_block(state)}
230	
231	        Batch framing:
232	        - Execute batch {batch_number} of {batch_total}.
233	        - Actionable task IDs for this batch: {batch_task_ids}
234	        - Already completed task IDs available as dependency context: {sorted(completed)}
235	
236	        Actionable tasks for this batch:
237	        {json_dump(batch_tasks).strip()}
238	
239	        Completed task context (already satisfied, do not re-execute unless directly required by current edits):
240	        {json_dump(completed_tasks).strip()}
241	
242	        Prior batch deviations (address if applicable):
243	        {prior_batch_deviations}
244	
245	        Batch-scoped sense checks:
246	        {json_dump(batch_sense_checks).strip()}
247	
248	        Full execution tracking source of truth (`finalize.json`):
249	        {json_dump(finalize_data).strip()}
250	
251	        {debt_watch_block}
252	
253	        {approval_note}
254	        Robustness level: {configured_robustness(state)}.
255	
256	        Requirements:
257	        - You are an author. Write document sections to the configured output path.
258	        - Execute only the actionable tasks in this batch.
259	        - Treat completed tasks as dependency context, not new work.
260	        - Return structured JSON only.
261	        - Only produce `task_updates` for these tasks: [{", ".join(batch_task_ids)}]
262	        - Only produce `sense_check_acknowledgments` for these sense checks: [{", ".join(batch_sense_check_ids)}]
263	        - Do not include updates for tasks or sense checks outside this batch.
264	        - Keep `executor_notes` verification-focused.
265	        - Best-effort progress checkpointing: if `{checkpoint_path}` is writable, checkpoint task and sense-check updates there (not `finalize.json`). The harness owns `finalize.json`.
266	        - `sections_written` replaces `files_changed` in task_updates. List the section IDs you authored, not file paths.
267	        - Follow this JSON shape:
268	        {_EXECUTE_DOC_OUTPUT_SHAPE_EXAMPLE}
269	        """
270	    ).strip()
271
```

> AGENT

Now I have enough. Drafting the plan.

# Implementation Plan: `--from-doc` flag + standardized `## Settled Decisions` format

## Overview

Add a `--from-doc <path>` flag to `megaplan init` that imports a prior doc-mode artifact's settled decisions into the new plan. Concretely:

- New pure parser `extract_settled_decisions(doc_text) -> list[dict]` in `megaplan/doc_assembly.py` (peer to existing `assemble_doc` / `extract_sections`).
- New `SettledDecisionFromDoc` TypedDict in `megaplan/types.py` (distinct from the existing `SettledDecision` produced by `gate`).
- `handle_init` (`megaplan/handlers.py:728`) validates the path, parses the doc, stores `state.config.from_doc` and `state.meta.imported_decisions`, and flows the `load_bearing` flag through so the planning phase can promote load-bearing entries to `must` success criteria and the rest to `info`.
- Doc-mode execute prompts (`megaplan/prompts/execute_doc.py`) teach the worker to emit a standard `## Settled Decisions` block when any decisions are produced.
- `--output` validation block at `handlers.py:748-758` is factored into a shared `_validate_relative_path(project_dir, raw, flag_name)` helper, reused by `--from-doc`.

Scope is moderate: one new parser + types entry, two CLI/handler edits, two prompt edits, docs update, two test files touched. Out of scope (per brief): critique-level SD-citation checks, sidecar `settled_decisions.json`, `verify-against-doc` subcommand.

## Main Phase

### Step 1: Add `SettledDecisionFromDoc` TypedDict (`megaplan/types.py`)
**Scope:** Small
1. **Add** `SettledDecisionFromDoc(TypedDict, total=False)` alongside the existing `SettledDecision` at `megaplan/types.py:170`, with fields: `id: str`, `decision: str`, `rationale: str`, `load_bearing: bool`. Keep it a distinct noun — do not extend or subclass `SettledDecision` (the brief explicitly names this to avoid collision with gate-produced SettledDecisions).
2. **Extend** `PlanState`'s `meta` TypedDict (or the nearest representation used at `handlers.py:791-799`) so that an optional `imported_decisions: list[SettledDecisionFromDoc]` is permitted. If `PlanState`/`PlanMeta` is structurally typed with `total=False`, a new optional key suffices.
3. **Extend** `PlanState`'s `config` TypedDict similarly to allow optional `from_doc: str`.

### Step 2: Implement `extract_settled_decisions` (`megaplan/doc_assembly.py`)
**Scope:** Medium
1. **Add** `def extract_settled_decisions(doc_text: str) -> list[dict]:` as a pure function at the top of `megaplan/doc_assembly.py` (next to `extract_sections` at line 13).
2. **Parse** the standardized block. Proposed format (see assumption; adjust if the user prefers a different shape):
   ````md
   ## Settled Decisions

   - id: SD-001
     load_bearing: true
     decision: Use SHA-256 for content hashes.
     rationale: Matches existing artifact hashing in evaluation.py.
   - id: SD-002
     load_bearing: false
     decision: Prefer 3-space indent for YAML examples.
     rationale: Matches existing doc conventions.
   ````
   Read the block from the `## Settled Decisions` heading until the next `##`/EOF. Each list item starts with `- id:`; subsequent indented lines (`  key: value`) belong to the preceding item. Store `id` verbatim (tolerate non-3-digit IDs; don't coerce). Coerce `load_bearing` to `bool` (strings `true`/`false` case-insensitive).
3. **Be tolerant.** No `## Settled Decisions` heading → return `[]`. Heading present but no items → `[]`. Items missing required fields → drop that item but keep parsing (return only well-formed entries; do NOT raise).
4. **Return** `list[dict]` with exactly the keys `{id, decision, rationale, load_bearing}`. Missing optional fields (e.g., `rationale`) default to empty string.
5. **Also expose** a companion helper (internal) for collecting parse warnings, so the handler can surface them through the init response — e.g. return a `(decisions, warnings)` tuple, or stash warnings on a module-level convention. Prefer tuple return: `extract_settled_decisions(doc_text) -> tuple[list[dict], list[str]]`. Update step 5 to thread warnings into the response.

### Step 3: Factor `_validate_relative_path` helper (`megaplan/handlers.py`)
**Scope:** Small
1. **Extract** the existing three-check validation at `megaplan/handlers.py:748-758` (absolute rejection, `..` rejection, must-stay-within enforcement) into a private helper at module scope:
   ```python
   def _validate_relative_path(project_dir: Path, raw: str, flag_name: str) -> str:
       candidate = Path(raw)
       if candidate.is_absolute():
           raise CliError("invalid_args", f"{flag_name} must be a relative path inside the project directory")
       if any(part == ".." for part in candidate.parts):
           raise CliError("invalid_args", f"{flag_name} must not contain '..' path traversal")
       resolved = (project_dir / candidate).resolve()
       try:
           return resolved.relative_to(project_dir).as_posix()
       except ValueError as exc:
           raise CliError("invalid_args", f"{flag_name} must stay within the project directory") from exc
   ```
2. **Replace** the inline block at `handlers.py:748-758` with `normalized_output_path = _validate_relative_path(project_dir, raw_output_path, "--output")`. Verify the existing `tests/test_handle_init_doc_mode.py::test_output_rejects_absolute_path` and `test_output_rejects_parent_traversal` still pass (they assert the same error messages; keep them identical).

### Step 4: Add `--from-doc` CLI flag (`megaplan/cli.py`)
**Scope:** Small
1. **Add** after `megaplan/cli.py:847` (after `--output`):
   ```python
   init_parser.add_argument("--from-doc", default=None,
                            help="Relative path to a prior doc-mode artifact whose "
                                 "## Settled Decisions section should be imported. "
                                 "Valid with --mode code or --mode doc.")
   ```
   Argparse auto-maps `--from-doc` → `args.from_doc`.

### Step 5: Wire `handle_init` for `--from-doc` (`megaplan/handlers.py`)
**Scope:** Medium
1. **After** the `--output` validation block, add `--from-doc` handling. Per the brief: `--from-doc` is valid with BOTH `--mode code` and `--mode doc` — no mode-coupling validation.
   ```python
   raw_from_doc = getattr(args, "from_doc", None)
   from_doc_rel: str | None = None
   imported_decisions: list[dict] = []
   parse_warnings: list[str] = []
   if raw_from_doc:
       from_doc_rel = _validate_relative_path(project_dir, raw_from_doc, "--from-doc")
       from_doc_abs = (project_dir / from_doc_rel)
       if not from_doc_abs.exists() or not from_doc_abs.is_file():
           raise CliError("invalid_args", f"--from-doc path does not exist: {from_doc_rel}")
       imported_decisions, parse_warnings = extract_settled_decisions(from_doc_abs.read_text())
   ```
2. **Populate** state after the existing `state` dict is built:
   ```python
   if from_doc_rel is not None:
       state["config"]["from_doc"] = from_doc_rel
       state["meta"]["imported_decisions"] = imported_decisions
   ```
   Always include the key when `--from-doc` was passed, even if `imported_decisions` is an empty list (so downstream can detect intent vs absence).
3. **Surface warnings** by appending to `state["meta"]["notes"]` (already initialized at `handlers.py:798`) and/or adding a `warnings` field to the `StepResponse` returned at `handlers.py:819-829`. Prefer `state["meta"]["notes"]` + include `warnings: parse_warnings` in the response when non-empty.
4. **Import** `extract_settled_decisions` at the top of `handlers.py` (`from megaplan.doc_assembly import extract_settled_decisions`).

### Step 6: Update doc-mode execute prompts to emit standard format (`megaplan/prompts/execute_doc.py`)
**Scope:** Small
1. **Extend** `_EXECUTE_DOC_REQUIREMENTS_TEMPLATE` at `megaplan/prompts/execute_doc.py:67` with a new requirement bullet: instruct the worker that when the document contains any design decisions, it MUST emit a top-level `## Settled Decisions` section using the standardized format (show the exact markdown shape from Step 2, including the `load_bearing: true|false` field and `SD-NNN` ID convention). Include a 1-line explanation: "Downstream plans can import these via `megaplan init --from-doc`."
2. **Mirror** the same bullet in `_execute_doc_batch_prompt`'s inline Requirements block at `megaplan/prompts/execute_doc.py:256-268`.
3. **Do not touch** code-mode prompts (`execute.py`) — settled decisions are a doc-mode output concept.

### Step 7: Thread `imported_decisions` into the planning prompt
**Scope:** Small-Medium — flagged as ASSUMPTION, see questions.
1. **Locate** the planning prompt builder at `megaplan/prompts/planning.py` (per the Explore pass, success criteria are emitted at `prompts/planning.py:120-124`).
2. **Inject** an `Imported decisions from --from-doc` block into the planning prompt when `state["meta"].get("imported_decisions")` is non-empty. Instruct the planner: "For each imported decision with `load_bearing: true`, include a matching success criterion with `priority: 'must'` and `requires` populated appropriately. For `load_bearing: false`, include a matching success criterion with `priority: 'info'`. Reference each by its SD-NNN id in the criterion text."
3. This is how the "auto-promote" half of the feature reaches the plan. It is a small prompt edit, not a structural change. Flagged as an assumption because the brief's "files touched" list omits `planning.py`; I believe the omission is an oversight since the rest of the brief explicitly requires this promotion.

### Step 8: Document in `megaplan/data/instructions.md`
**Scope:** Small
1. **Update** the "Modes" section (lines 19-27) and the "Start" section (lines 29-34) to include `--from-doc <relative-path>` in the example invocation and document its semantics: relative-to-project, file must exist, usable with either mode, imports `## Settled Decisions`, promotes to `must`/`info` criteria.
2. **Add** a short "Settled Decisions section format" subsection showing the exact markdown shape so doc authors (and the doc-mode worker) have a canonical reference.

### Step 9: Unit-test the parser (`tests/test_doc_assembly.py`)
**Scope:** Small
1. **Add** tests at `tests/test_doc_assembly.py` (peer to existing tests) covering the 5 fixtures from the brief:
   - empty string → `([], [])`
   - doc with no `## Settled Decisions` section → `([], [])`
   - doc with three well-formed decisions (SD-001/002/003, mix of `load_bearing`) → 3 items, correct fields and types
   - doc with one malformed entry inside a well-formed section → well-formed entries returned, malformed skipped, warning surfaced
   - doc with a `## Settled Decisions` heading but no list items → `([], [])`
2. **Add** one extra test: `load_bearing` is case-insensitive and coerced to `bool`.

### Step 10: Handler tests for `--from-doc` (`tests/test_handle_init_doc_mode.py`)
**Scope:** Small
1. **Reuse** the existing `_bootstrap` / `_args` helpers at `tests/test_handle_init_doc_mode.py:16,39`. Extend `_args` (or add a new builder) to accept a `from_doc` kwarg.
2. **Add** these tests:
   - `test_from_doc_valid_path_populates_state` — write a fixture doc under `project_dir` with 2 load-bearing + 1 non-load-bearing decisions; assert `state["config"]["from_doc"]` is the relative path and `state["meta"]["imported_decisions"]` has the expected 3 entries.
   - `test_from_doc_nonexistent_path_rejected` — raises `CliError("invalid_args")` with message mentioning `--from-doc`.
   - `test_from_doc_absolute_path_rejected` — same error class, message mentions `--from-doc`.
   - `test_from_doc_parent_traversal_rejected` — same.
   - `test_from_doc_doc_with_no_section_succeeds` — succeeds; `imported_decisions` is `[]`; `config.from_doc` is still set.
   - `test_from_doc_valid_with_code_mode` — confirm `--mode code` + `--from-doc` is accepted (no output required).

### Step 11: Run full suite
**Scope:** Small
1. **Run** the targeted test files first:
   ```
   PYENV_VERSION=3.11.11 python -m pytest tests/test_doc_assembly.py tests/test_handle_init_doc_mode.py -v
   ```
2. **Then** the full suite:
   ```
   PYENV_VERSION=3.11.11 python -m pytest tests/
   ```
   Expect ≥690 passed, 1 skipped (baseline is 687 passed + 1 skipped, and we add ≥6 handler tests + ≥6 parser tests).

## Execution Order
1. Types + parser first (Steps 1–2), since everything else imports them.
2. Helper factoring (Step 3) before handler wiring (Step 5) so `--output` validation stays green while `--from-doc` reuses the same helper.
3. CLI flag (Step 4) and handler wiring (Step 5) together.
4. Prompts (Steps 6–7) and docs (Step 8) after the plumbing works.
5. Tests (Steps 9–10) last on the list but written incrementally as each piece lands.

## Validation Order
1. Parser unit tests (cheapest, pure function).
2. Handler tests (exercise CLI + state shape).
3. Full pytest run to catch regressions in prompt/type integrations.

> TOOL

tool_use StructuredOutput
```json
{
  "plan": "# Implementation Plan: `--from-doc` flag + standardized `## Settled Decisions` format\n\n## Overview\n\nAdd a `--from-doc <path>` flag to `megaplan init` that imports a prior doc-mode artifact's settled decisions into the new plan. Concretely:\n\n- New pure parser `extract_settled_decisions(doc_text) -> tuple[list[dict], list[str]]` in `megaplan/doc_assembly.py` (peer to existing `assemble_doc` / `extract_sections`).\n- New `SettledDecisionFromDoc` TypedDict in `megaplan/types.py` (distinct from the existing `SettledDecision` produced by `gate`).\n- `handle_init` (`megaplan/handlers.py:728`) validates the path, parses the doc, stores `state.config.from_doc` and `state.meta.imported_decisions`, and flows the `load_bearing` flag through so the planning phase can promote load-bearing entries to `must` success criteria and the rest to `info`.\n- Doc-mode execute prompts (`megaplan/prompts/execute_doc.py`) teach the worker to emit a standard `## Settled Decisions` block when any decisions are produced.\n- `--output` validation block at `handlers.py:748-758` is factored into a shared `_validate_relative_path(project_dir, raw, flag_name)` helper, reused by `--from-doc`.\n\nScope is moderate. Out of scope (per brief): critique-level SD-citation checks, sidecar `settled_decisions.json`, `verify-against-doc` subcommand.\n\n## Main Phase\n\n### Step 1: Add `SettledDecisionFromDoc` TypedDict (`megaplan/types.py`)\n**Scope:** Small\n1. Add `SettledDecisionFromDoc(TypedDict, total=False)` at `megaplan/types.py:170` (next to `SettledDecision`), with: `id: str`, `decision: str`, `rationale: str`, `load_bearing: bool`. Keep it a distinct name — do not subclass or extend `SettledDecision` (collision-free per brief).\n2. Extend `PlanState`'s `meta` TypedDict to allow optional `imported_decisions: list[SettledDecisionFromDoc]`.\n3. Extend `PlanState`'s `config` TypedDict to allow optional `from_doc: str`.\n\n### Step 2: Implement `extract_settled_decisions` (`megaplan/doc_assembly.py`)\n**Scope:** Medium\n1. Add `def extract_settled_decisions(doc_text: str) -> tuple[list[dict], list[str]]:` at the top of `megaplan/doc_assembly.py` (next to `extract_sections` at line 13). Returns `(decisions, warnings)`.\n2. Parse from the `## Settled Decisions` heading until the next `##`/EOF. Item format (markdown list):\n   ```\n   - id: SD-001\n     load_bearing: true\n     decision: <text>\n     rationale: <text>\n   ```\n   Each item starts with `- id:`; subsequent 2-space-indented `key: value` lines belong to the preceding item. Store `id` verbatim (tolerate non-3-digit IDs). Coerce `load_bearing` to `bool` (strings `true`/`false`, case-insensitive).\n3. Be tolerant: no heading → `([], [])`. Heading + zero items → `([], [])`. Item missing required fields (`id` or `decision`) → drop, append to warnings, keep parsing. Never raise.\n4. Return keys: `{id, decision, rationale, load_bearing}`. Missing optional fields default to `\"\"` / `False`.\n\n### Step 3: Factor `_validate_relative_path` helper (`megaplan/handlers.py`)\n**Scope:** Small\n1. Extract the three-check validation at `megaplan/handlers.py:748-758` into a module-private helper `_validate_relative_path(project_dir: Path, raw: str, flag_name: str) -> str` that raises `CliError(\"invalid_args\", f\"{flag_name} ...\")` for absolute paths, `..` traversal, and out-of-project paths.\n2. Replace the inline block with `normalized_output_path = _validate_relative_path(project_dir, raw_output_path, \"--output\")`. Keep error messages identical so existing `tests/test_handle_init_doc_mode.py::test_output_rejects_absolute_path` and `test_output_rejects_parent_traversal` continue to pass.\n\n### Step 4: Add `--from-doc` CLI flag (`megaplan/cli.py`)\n**Scope:** Small\n1. Add after `megaplan/cli.py:847` (after `--output`):\n   ```python\n   init_parser.add_argument(\"--from-doc\", default=None,\n                            help=\"Relative path to a prior doc-mode artifact whose \"\n                                 \"## Settled Decisions section should be imported. \"\n                                 \"Valid with --mode code or --mode doc.\")\n   ```\n\n### Step 5: Wire `handle_init` for `--from-doc` (`megaplan/handlers.py`)\n**Scope:** Medium\n1. After the `--output` block, validate and load:\n   ```python\n   raw_from_doc = getattr(args, \"from_doc\", None)\n   from_doc_rel: str | None = None\n   imported_decisions: list[dict] = []\n   parse_warnings: list[str] = []\n   if raw_from_doc:\n       from_doc_rel = _validate_relative_path(project_dir, raw_from_doc, \"--from-doc\")\n       from_doc_abs = project_dir / from_doc_rel\n       if not from_doc_abs.exists() or not from_doc_abs.is_file():\n           raise CliError(\"invalid_args\", f\"--from-doc path does not exist: {from_doc_rel}\")\n       imported_decisions, parse_warnings = extract_settled_decisions(from_doc_abs.read_text())\n   ```\n   No mode coupling — `--from-doc` is valid with both `--mode code` and `--mode doc`.\n2. After the `state` dict is built:\n   ```python\n   if from_doc_rel is not None:\n       state[\"config\"][\"from_doc\"] = from_doc_rel\n       state[\"meta\"][\"imported_decisions\"] = imported_decisions\n   ```\n   Always set both keys when `--from-doc` was passed, even if `imported_decisions == []`.\n3. Surface `parse_warnings` by appending to `state[\"meta\"][\"notes\"]` and adding a `warnings` field to the `StepResponse` at `handlers.py:819-829` when the list is non-empty.\n4. Add `from megaplan.doc_assembly import extract_settled_decisions` at the top of `handlers.py`.\n\n### Step 6: Update doc-mode execute prompts (`megaplan/prompts/execute_doc.py`)\n**Scope:** Small\n1. Extend `_EXECUTE_DOC_REQUIREMENTS_TEMPLATE` at `megaplan/prompts/execute_doc.py:67` with a bullet: when the document contains design decisions, emit a top-level `## Settled Decisions` section using the standardized format (show the exact markdown shape from Step 2, including `load_bearing: true|false` and the `SD-NNN` ID convention). Add a 1-line note: \"Downstream plans can import these via `megaplan init --from-doc`.\"\n2. Mirror the same bullet in `_execute_doc_batch_prompt`'s inline Requirements block at `megaplan/prompts/execute_doc.py:256-268`.\n3. Do not touch code-mode prompts.\n\n### Step 7: Thread `imported_decisions` into the planning prompt (`megaplan/prompts/planning.py`)\n**Scope:** Small-Medium (see Assumption 3)\n1. When `state[\"meta\"].get(\"imported_decisions\")` is non-empty, inject an \"Imported decisions from --from-doc\" block into the planning prompt listing each decision with its `id`, `decision`, `rationale`, `load_bearing`.\n2. Instruct the planner: for each `load_bearing: true` decision, emit a success criterion with `priority: \"must\"` referencing the `SD-NNN` id; for `load_bearing: false`, emit `priority: \"info\"`. Criterion `requires` fields should match the nature of the decision.\n\n### Step 8: Document in `megaplan/data/instructions.md`\n**Scope:** Small\n1. Update the \"Modes\" section (lines 19-27) and \"Start\" section (lines 29-34) to include `--from-doc <relative-path>` in the example invocation and document semantics (relative-to-project, file must exist, works with either mode, imports `## Settled Decisions`, promotes to `must`/`info` criteria).\n2. Add a short \"Settled Decisions section format\" subsection showing the canonical markdown shape.\n\n### Step 9: Unit-test the parser (`tests/test_doc_assembly.py`)\n**Scope:** Small\n1. Add tests covering the 5 brief-specified fixtures:\n   - empty string → `([], [])`\n   - doc with no `## Settled Decisions` section → `([], [])`\n   - doc with three well-formed decisions (mix of `load_bearing`) → 3 items with correct types\n   - doc with one malformed entry (missing `id`) in a well-formed section → good items returned, warning surfaced\n   - heading present but no items → `([], [])`\n2. Add one extra: `load_bearing` is case-insensitive and coerces to `bool`.\n\n### Step 10: Handler tests (`tests/test_handle_init_doc_mode.py`)\n**Scope:** Small\n1. Reuse `_bootstrap` / `_args` helpers at `tests/test_handle_init_doc_mode.py:16,39`. Extend `_args` with an optional `from_doc` kwarg.\n2. Add tests:\n   - `test_from_doc_valid_path_populates_state` — fixture doc with 2 load-bearing + 1 non-load-bearing; assert `state[\"config\"][\"from_doc\"]` and `state[\"meta\"][\"imported_decisions\"]`.\n   - `test_from_doc_nonexistent_path_rejected` — `CliError(\"invalid_args\")` with `--from-doc` in message.\n   - `test_from_doc_absolute_path_rejected` — same error class.\n   - `test_from_doc_parent_traversal_rejected` — same.\n   - `test_from_doc_doc_with_no_section_succeeds` — `imported_decisions == []`, `config.from_doc` still set.\n   - `test_from_doc_valid_with_code_mode` — confirm it's accepted without `--output`.\n\n### Step 11: Run full suite\n**Scope:** Small\n1. Targeted: `PYENV_VERSION=3.11.11 python -m pytest tests/test_doc_assembly.py tests/test_handle_init_doc_mode.py -v`\n2. Full: `PYENV_VERSION=3.11.11 python -m pytest tests/` — expect ≥699 passed, 1 skipped (687 baseline + ~12 new tests).\n\n## Execution Order\n1. Types + parser first (Steps 1–2) — everything else imports them.\n2. Helper factoring (Step 3) before handler wiring (Step 5) so `--output` validation stays green.\n3. CLI flag (Step 4) + handler wiring (Step 5) together.\n4. Prompt + docs edits (Steps 6–8) after the plumbing works.\n5. Tests (Steps 9–10) written incrementally alongside each piece.\n\n## Validation Order\n1. Parser unit tests (pure function, cheapest).\n2. Handler tests (CLI + state shape).\n3. Full pytest run for regression check on prompt/type integrations.\n",
  "questions": [
    "The brief specifies a ## Settled Decisions section format but does not pin down the exact markdown syntax. I've proposed a `- id: SD-NNN` / indented `key: value` list format (see Step 2). Is that the intended shape, or would you prefer YAML fenced-blocks, an HTML comment block, or a table?",
    "The brief's 'files touched' list does not include megaplan/prompts/planning.py, but the feature requires promoting imported decisions to must/info success criteria in the plan — which is naturally done in the planning prompt. Confirm that Step 7 (edit planning.py) is in scope, or point me at the preferred location for that promotion.",
    "Should parse warnings surface to the user via the init response payload (new `warnings` field), via `state.meta.notes`, or both? I've assumed both (Step 5.3)."
  ],
  "assumptions": [
    "Standard section format uses markdown list items with `- id: SD-NNN` followed by indented `load_bearing: / decision: / rationale:` lines. Parser returns a (decisions, warnings) tuple so the handler can surface tolerant-parse warnings without silently dropping data.",
    "`--from-doc` does not require the target path to itself be a megaplan-produced artifact — any text file with a parseable section works. Path validity is enforced (exists, is a file, relative to project_dir), but content is handled tolerantly.",
    "Auto-promotion of load_bearing decisions to `must` success criteria happens via a small edit to megaplan/prompts/planning.py (Step 7). The brief's 'files touched' list omits planning.py; I'm treating that as an oversight since the feature requires it end-to-end. Flagged as Question 2.",
    "PlanState/PlanMeta TypedDicts are structurally typed with `total=False` (or similar), so adding optional `imported_decisions` and `from_doc` keys won't require invasive type changes elsewhere. If they are `total=True`, Step 1 broadens slightly.",
    "The existing `--output` error messages are assumed to be unchanged after factoring into `_validate_relative_path` — only the message prefix varies by flag name. This preserves existing tests at `tests/test_handle_init_doc_mode.py:64-85`."
  ],
  "success_criteria": [
    {
      "criterion": "`PYENV_VERSION=3.11.11 python -m pytest tests/` passes with ≥699 passed and 1 skipped (687 baseline + ~12 new tests; at minimum 690 must pass per brief).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <valid relative path>` with a doc containing 3 well-formed decisions populates `state.config.from_doc` to the normalized relative path and `state.meta.imported_decisions` to a list of 3 dicts with keys {id, decision, rationale, load_bearing}.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <nonexistent>` raises `CliError(\"invalid_args\", ...)` with a message that contains `--from-doc`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc /absolute/path` and `--from-doc ../escape.md` both raise `CliError(\"invalid_args\", ...)`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <doc with no ## Settled Decisions section>` succeeds; `state.config.from_doc` is set; `state.meta.imported_decisions == []`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`extract_settled_decisions` is a pure function in `megaplan/doc_assembly.py` (no filesystem or state access); its 5+ unit tests pass.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`SettledDecisionFromDoc` is a distinct TypedDict in `megaplan/types.py`, not a subclass or alias of the existing `SettledDecision`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "A single `_validate_relative_path` helper in `megaplan/handlers.py` is used by both `--output` and `--from-doc` validation (no duplicated absolute/`..`/out-of-project checks).",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Doc-mode execute prompt (`megaplan/prompts/execute_doc.py`) instructs the worker to emit a `## Settled Decisions` section in the standardized format when decisions are produced.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "`megaplan/data/instructions.md` documents `--from-doc` and shows the canonical `## Settled Decisions` section format.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "No out-of-scope work: no critique-level SD citation check, no sidecar `settled_decisions.json` writer, no `verify-against-doc` subcommand.",
      "priority": "must",
      "requires": [
        "parse_diff",
        "read_files"
      ]
    },
    {
      "criterion": "Planning prompt surfaces `state.meta.imported_decisions` and instructs the planner to emit success criteria with `priority: must` for `load_bearing: true` and `priority: info` otherwise, each referencing the SD-NNN id.",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Parse warnings from malformed entries are surfaced to the user either in the `StepResponse` returned by `handle_init` or via `state.meta.notes`.",
      "priority": "should",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Each function added or modified keeps a single responsibility; no change exceeds ~50 lines of net new code per step.",
      "priority": "should",
      "requires": [
        "parse_diff"
      ]
    }
  ]
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Plan delivered. Key highlights:

- **11 concrete steps** touching `types.py`, `doc_assembly.py`, `handlers.py`, `cli.py`, `prompts/execute_doc.py`, `prompts/planning.py`, `instructions.md`, and the two test files from the brief.
- **Three questions** flagged: (1) exact markdown shape for `## Settled Decisions`, (2) confirmation that `planning.py` is in scope for the must/info promotion (brief omits it but the feature needs it), (3) where to surface parse warnings.
- **Key assumption** on section format: `- id: SD-NNN` markdown list with 2-space-indented `key: value` lines, and parser returns `(decisions, warnings)` tuple so tolerant parsing doesn't silently drop data.
- **Reuse** confirmed: `_validate_relative_path` helper factored from `handlers.py:748-758`; `SettledDecisionFromDoc` kept distinct from existing `SettledDecision` at `types.py:170`.

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

You are revising an implementation plan after critique and gate feedback.

        Project directory:
        /Users/user_c042661f/Documents/megaplan




        Idea:
Add --from-doc <path> flag to megaplan init plus a standardized ## Settled Decisions section format for doc-mode output. When --from-doc points at a doc-mode megaplan artifact, the CLI validates the path (relative to project_dir, no absolute, no .., must exist), parses any ## Settled Decisions section via a new pure function doc_assembly.extract_settled_decisions, stores the path at state.config.from_doc, and injects extracted decisions into state.meta.imported_decisions. Load-bearing decisions (load_bearing: true) auto-promote to must-priority success criteria for the new plan; non-load-bearing become info-priority. Doc-mode execute prompt is updated to instruct the worker to emit the standard Settled Decisions section format. Reuses existing settled_decisions concept in evaluation.py (name the new imported type SettledDecisionFromDoc to avoid collision). Reuses the _validate_relative_path logic factored from the existing --output validation. Out of scope for this PR: critique-level auto-check for SD-* citation, sidecar settled_decisions.json, verify-against-doc subcommand.

User notes and answers:
- PRE-PLAN GUIDANCE (authoritative — do not re-derive):

### Files that will be touched
- megaplan/cli.py — add --from-doc to the init subparser
- megaplan/handlers.py::handle_init — validate --from-doc, call the parser, populate state.config.from_doc and state['meta']['imported_decisions']
- megaplan/doc_assembly.py — new extract_settled_decisions(doc_text: str) -> list[dict] pure function
- megaplan/types.py — add SettledDecisionFromDoc TypedDict if the shape warrants it
- megaplan/data/instructions.md — document --from-doc, the Settled Decisions section format, and how it interacts with success criteria
- megaplan/data/prompts/* or wherever doc-mode execute worker prompt lives — update to instruct the worker to emit ## Settled Decisions in the standard format when the subject produces any
- tests/test_handle_init_doc_mode.py — add tests for --from-doc validation (path must exist, must be inside project_dir, must parse cleanly)
- tests/test_doc_assembly.py OR new tests/test_settled_decisions.py — unit tests for the parser against fixture doc strings

### Load-bearing decisions (pre-settled — don't re-debate in critique)
- Parser lives in doc_assembly.py (pure function), not inline in handlers.py. Keeps handler thin and parser testable.
- Decision ID format is SD-NNN (SD- prefix + 3-digit zero-padded). Parser is tolerant of the 3-digit convention but stores the ID verbatim as written.
- load_bearing: true|false is the gate field. Only load_bearing: true decisions become must success criteria. Non-load-bearing are stored as info criteria for reference.
- --from-doc takes a path RELATIVE to --project-dir. Absolute paths rejected. .. rejected. Same safety as --output.
- --from-doc is valid with either --mode doc or --mode code, not just code. A doc plan can reference a prior doc.
- Missing ## Settled Decisions section is NOT an error. Parser returns empty list; meta.imported_decisions is empty; --from-doc still stores the path for worker context.
- Malformed entries within a well-formed section are logged but don't fail the parse (tolerant). Report parse warnings via the init response.

### Reuse what already exists, don't duplicate
- settled_decisions is already a first-class concept in megaplan/evaluation.py, megaplan/handlers.py, and megaplan/types.py — produced by gate/critique signals. Name the new type SettledDecisionFromDoc (distinct noun) to avoid collision with the existing gate-produced SettledDecision.
- --output validation logic at handlers.py::handle_init (absolute path rejection, .. rejection, relative-to-project enforcement) is the template for --from-doc validation. Factor both into a small _validate_relative_path(project_dir, raw_path, flag_name) helper to avoid duplication.

### Tests must cover
- Parser: 5+ fixture strings (empty doc, doc with no section, doc with 3 well-formed decisions, doc with malformed entry inside well-formed section, doc with section but no entries)
- handle_init with --from-doc pointing at a valid doc → config.from_doc set, meta.imported_decisions populated
- handle_init with --from-doc pointing at non-existent file → invalid_args with clear message
- handle_init with --from-doc pointing at absolute path → rejected
- handle_init with --from-doc pointing at a doc with zero decisions → succeeds, imported_decisions is empty list
- Full suite: PYENV_VERSION=3.11.11 python -m pytest tests/ must pass 690+ (current baseline 687 passed, 1 skipped).

### Out of scope (do NOT scope-creep)
- Full critique-level auto-check that verifies each SD-* is cited in the plan — follow-up
- Sidecar settled_decisions.json written by doc-mode finalize — follow-up
- megaplan verify-against-doc subcommand — follow-up
- Migrating existing doc-mode output to the new standard (convention starts with new plans)

        Current plan (markdown):
        # Implementation Plan: `--from-doc` flag + standardized `## Settled Decisions` format

## Overview

Add a `--from-doc <path>` flag to `megaplan init` that imports a prior doc-mode artifact's settled decisions into the new plan. Concretely:

- New pure parser `extract_settled_decisions(doc_text) -> tuple[list[dict], list[str]]` in `megaplan/doc_assembly.py` (peer to existing `assemble_doc` / `extract_sections`).
- New `SettledDecisionFromDoc` TypedDict in `megaplan/types.py` (distinct from the existing `SettledDecision` produced by `gate`).
- `handle_init` (`megaplan/handlers.py:728`) validates the path, parses the doc, stores `state.config.from_doc` and `state.meta.imported_decisions`, and flows the `load_bearing` flag through so the planning phase can promote load-bearing entries to `must` success criteria and the rest to `info`.
- Doc-mode execute prompts (`megaplan/prompts/execute_doc.py`) teach the worker to emit a standard `## Settled Decisions` block when any decisions are produced.
- `--output` validation block at `handlers.py:748-758` is factored into a shared `_validate_relative_path(project_dir, raw, flag_name)` helper, reused by `--from-doc`.

Scope is moderate. Out of scope (per brief): critique-level SD-citation checks, sidecar `settled_decisions.json`, `verify-against-doc` subcommand.

## Main Phase

### Step 1: Add `SettledDecisionFromDoc` TypedDict (`megaplan/types.py`)
**Scope:** Small
1. Add `SettledDecisionFromDoc(TypedDict, total=False)` at `megaplan/types.py:170` (next to `SettledDecision`), with: `id: str`, `decision: str`, `rationale: str`, `load_bearing: bool`. Keep it a distinct name — do not subclass or extend `SettledDecision` (collision-free per brief).
2. Extend `PlanState`'s `meta` TypedDict to allow optional `imported_decisions: list[SettledDecisionFromDoc]`.
3. Extend `PlanState`'s `config` TypedDict to allow optional `from_doc: str`.

### Step 2: Implement `extract_settled_decisions` (`megaplan/doc_assembly.py`)
**Scope:** Medium
1. Add `def extract_settled_decisions(doc_text: str) -> tuple[list[dict], list[str]]:` at the top of `megaplan/doc_assembly.py` (next to `extract_sections` at line 13). Returns `(decisions, warnings)`.
2. Parse from the `## Settled Decisions` heading until the next `##`/EOF. Item format (markdown list):
   ```
   - id: SD-001
     load_bearing: true
     decision: <text>
     rationale: <text>
   ```
   Each item starts with `- id:`; subsequent 2-space-indented `key: value` lines belong to the preceding item. Store `id` verbatim (tolerate non-3-digit IDs). Coerce `load_bearing` to `bool` (strings `true`/`false`, case-insensitive).
3. Be tolerant: no heading → `([], [])`. Heading + zero items → `([], [])`. Item missing required fields (`id` or `decision`) → drop, append to warnings, keep parsing. Never raise.
4. Return keys: `{id, decision, rationale, load_bearing}`. Missing optional fields default to `""` / `False`.

### Step 3: Factor `_validate_relative_path` helper (`megaplan/handlers.py`)
**Scope:** Small
1. Extract the three-check validation at `megaplan/handlers.py:748-758` into a module-private helper `_validate_relative_path(project_dir: Path, raw: str, flag_name: str) -> str` that raises `CliError("invalid_args", f"{flag_name} ...")` for absolute paths, `..` traversal, and out-of-project paths.
2. Replace the inline block with `normalized_output_path = _validate_relative_path(project_dir, raw_output_path, "--output")`. Keep error messages identical so existing `tests/test_handle_init_doc_mode.py::test_output_rejects_absolute_path` and `test_output_rejects_parent_traversal` continue to pass.

### Step 4: Add `--from-doc` CLI flag (`megaplan/cli.py`)
**Scope:** Small
1. Add after `megaplan/cli.py:847` (after `--output`):
   ```python
   init_parser.add_argument("--from-doc", default=None,
                            help="Relative path to a prior doc-mode artifact whose "
                                 "## Settled Decisions section should be imported. "
                                 "Valid with --mode code or --mode doc.")
   ```

### Step 5: Wire `handle_init` for `--from-doc` (`megaplan/handlers.py`)
**Scope:** Medium
1. After the `--output` block, validate and load:
   ```python
   raw_from_doc = getattr(args, "from_doc", None)
   from_doc_rel: str | None = None
   imported_decisions: list[dict] = []
   parse_warnings: list[str] = []
   if raw_from_doc:
       from_doc_rel = _validate_relative_path(project_dir, raw_from_doc, "--from-doc")
       from_doc_abs = project_dir / from_doc_rel
       if not from_doc_abs.exists() or not from_doc_abs.is_file():
           raise CliError("invalid_args", f"--from-doc path does not exist: {from_doc_rel}")
       imported_decisions, parse_warnings = extract_settled_decisions(from_doc_abs.read_text())
   ```
   No mode coupling — `--from-doc` is valid with both `--mode code` and `--mode doc`.
2. After the `state` dict is built:
   ```python
   if from_doc_rel is not None:
       state["config"]["from_doc"] = from_doc_rel
       state["meta"]["imported_decisions"] = imported_decisions
   ```
   Always set both keys when `--from-doc` was passed, even if `imported_decisions == []`.
3. Surface `parse_warnings` by appending to `state["meta"]["notes"]` and adding a `warnings` field to the `StepResponse` at `handlers.py:819-829` when the list is non-empty.
4. Add `from megaplan.doc_assembly import extract_settled_decisions` at the top of `handlers.py`.

### Step 6: Update doc-mode execute prompts (`megaplan/prompts/execute_doc.py`)
**Scope:** Small
1. Extend `_EXECUTE_DOC_REQUIREMENTS_TEMPLATE` at `megaplan/prompts/execute_doc.py:67` with a bullet: when the document contains design decisions, emit a top-level `## Settled Decisions` section using the standardized format (show the exact markdown shape from Step 2, including `load_bearing: true|false` and the `SD-NNN` ID convention). Add a 1-line note: "Downstream plans can import these via `megaplan init --from-doc`."
2. Mirror the same bullet in `_execute_doc_batch_prompt`'s inline Requirements block at `megaplan/prompts/execute_doc.py:256-268`.
3. Do not touch code-mode prompts.

### Step 7: Thread `imported_decisions` into the planning prompt (`megaplan/prompts/planning.py`)
**Scope:** Small-Medium (see Assumption 3)
1. When `state["meta"].get("imported_decisions")` is non-empty, inject an "Imported decisions from --from-doc" block into the planning prompt listing each decision with its `id`, `decision`, `rationale`, `load_bearing`.
2. Instruct the planner: for each `load_bearing: true` decision, emit a success criterion with `priority: "must"` referencing the `SD-NNN` id; for `load_bearing: false`, emit `priority: "info"`. Criterion `requires` fields should match the nature of the decision.

### Step 8: Document in `megaplan/data/instructions.md`
**Scope:** Small
1. Update the "Modes" section (lines 19-27) and "Start" section (lines 29-34) to include `--from-doc <relative-path>` in the example invocation and document semantics (relative-to-project, file must exist, works with either mode, imports `## Settled Decisions`, promotes to `must`/`info` criteria).
2. Add a short "Settled Decisions section format" subsection showing the canonical markdown shape.

### Step 9: Unit-test the parser (`tests/test_doc_assembly.py`)
**Scope:** Small
1. Add tests covering the 5 brief-specified fixtures:
   - empty string → `([], [])`
   - doc with no `## Settled Decisions` section → `([], [])`
   - doc with three well-formed decisions (mix of `load_bearing`) → 3 items with correct types
   - doc with one malformed entry (missing `id`) in a well-formed section → good items returned, warning surfaced
   - heading present but no items → `([], [])`
2. Add one extra: `load_bearing` is case-insensitive and coerces to `bool`.

### Step 10: Handler tests (`tests/test_handle_init_doc_mode.py`)
**Scope:** Small
1. Reuse `_bootstrap` / `_args` helpers at `tests/test_handle_init_doc_mode.py:16,39`. Extend `_args` with an optional `from_doc` kwarg.
2. Add tests:
   - `test_from_doc_valid_path_populates_state` — fixture doc with 2 load-bearing + 1 non-load-bearing; assert `state["config"]["from_doc"]` and `state["meta"]["imported_decisions"]`.
   - `test_from_doc_nonexistent_path_rejected` — `CliError("invalid_args")` with `--from-doc` in message.
   - `test_from_doc_absolute_path_rejected` — same error class.
   - `test_from_doc_parent_traversal_rejected` — same.
   - `test_from_doc_doc_with_no_section_succeeds` — `imported_decisions == []`, `config.from_doc` still set.
   - `test_from_doc_valid_with_code_mode` — confirm it's accepted without `--output`.

### Step 11: Run full suite
**Scope:** Small
1. Targeted: `PYENV_VERSION=3.11.11 python -m pytest tests/test_doc_assembly.py tests/test_handle_init_doc_mode.py -v`
2. Full: `PYENV_VERSION=3.11.11 python -m pytest tests/` — expect ≥699 passed, 1 skipped (687 baseline + ~12 new tests).

## Execution Order
1. Types + parser first (Steps 1–2) — everything else imports them.
2. Helper factoring (Step 3) before handler wiring (Step 5) so `--output` validation stays green.
3. CLI flag (Step 4) + handler wiring (Step 5) together.
4. Prompt + docs edits (Steps 6–8) after the plumbing works.
5. Tests (Steps 9–10) written incrementally alongside each piece.

## Validation Order
1. Parser unit tests (pure function, cheapest).
2. Handler tests (CLI + state shape).
3. Full pytest run for regression check on prompt/type integrations.


        Current plan metadata:
        {
  "version": 1,
  "timestamp": "2026-04-21T10:50:29Z",
  "hash": "sha256:f1af08f9cdc108dae3027dd0d3b23a9c6b409ae9d87f1924d97e70d448ad879d",
  "questions": [
    "The brief specifies a ## Settled Decisions section format but does not pin down the exact markdown syntax. I've proposed a `- id: SD-NNN` / indented `key: value` list format (see Step 2). Is that the intended shape, or would you prefer YAML fenced-blocks, an HTML comment block, or a table?",
    "The brief's 'files touched' list does not include megaplan/prompts/planning.py, but the feature requires promoting imported decisions to must/info success criteria in the plan \u2014 which is naturally done in the planning prompt. Confirm that Step 7 (edit planning.py) is in scope, or point me at the preferred location for that promotion.",
    "Should parse warnings surface to the user via the init response payload (new `warnings` field), via `state.meta.notes`, or both? I've assumed both (Step 5.3)."
  ],
  "success_criteria": [
    {
      "criterion": "`PYENV_VERSION=3.11.11 python -m pytest tests/` passes with \u2265699 passed and 1 skipped (687 baseline + ~12 new tests; at minimum 690 must pass per brief).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <valid relative path>` with a doc containing 3 well-formed decisions populates `state.config.from_doc` to the normalized relative path and `state.meta.imported_decisions` to a list of 3 dicts with keys {id, decision, rationale, load_bearing}.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <nonexistent>` raises `CliError(\"invalid_args\", ...)` with a message that contains `--from-doc`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc /absolute/path` and `--from-doc ../escape.md` both raise `CliError(\"invalid_args\", ...)`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <doc with no ## Settled Decisions section>` succeeds; `state.config.from_doc` is set; `state.meta.imported_decisions == []`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`extract_settled_decisions` is a pure function in `megaplan/doc_assembly.py` (no filesystem or state access); its 5+ unit tests pass.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`SettledDecisionFromDoc` is a distinct TypedDict in `megaplan/types.py`, not a subclass or alias of the existing `SettledDecision`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "A single `_validate_relative_path` helper in `megaplan/handlers.py` is used by both `--output` and `--from-doc` validation (no duplicated absolute/`..`/out-of-project checks).",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Doc-mode execute prompt (`megaplan/prompts/execute_doc.py`) instructs the worker to emit a `## Settled Decisions` section in the standardized format when decisions are produced.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "`megaplan/data/instructions.md` documents `--from-doc` and shows the canonical `## Settled Decisions` section format.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "No out-of-scope work: no critique-level SD citation check, no sidecar `settled_decisions.json` writer, no `verify-against-doc` subcommand.",
      "priority": "must",
      "requires": [
        "parse_diff",
        "read_files"
      ]
    },
    {
      "criterion": "Planning prompt surfaces `state.meta.imported_decisions` and instructs the planner to emit success criteria with `priority: must` for `load_bearing: true` and `priority: info` otherwise, each referencing the SD-NNN id.",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Parse warnings from malformed entries are surfaced to the user either in the `StepResponse` returned by `handle_init` or via `state.meta.notes`.",
      "priority": "should",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Each function added or modified keeps a single responsibility; no change exceeds ~50 lines of net new code per step.",
      "priority": "should",
      "requires": [
        "parse_diff"
      ]
    }
  ],
  "assumptions": [
    "Standard section format uses markdown list items with `- id: SD-NNN` followed by indented `load_bearing: / decision: / rationale:` lines. Parser returns a (decisions, warnings) tuple so the handler can surface tolerant-parse warnings without silently dropping data.",
    "`--from-doc` does not require the target path to itself be a megaplan-produced artifact \u2014 any text file with a parseable section works. Path validity is enforced (exists, is a file, relative to project_dir), but content is handled tolerantly.",
    "Auto-promotion of load_bearing decisions to `must` success criteria happens via a small edit to megaplan/prompts/planning.py (Step 7). The brief's 'files touched' list omits planning.py; I'm treating that as an oversight since the feature requires it end-to-end. Flagged as Question 2.",
    "PlanState/PlanMeta TypedDicts are structurally typed with `total=False` (or similar), so adding optional `imported_decisions` and `from_doc` keys won't require invasive type changes elsewhere. If they are `total=True`, Step 1 broadens slightly.",
    "The existing `--output` error messages are assumed to be unchanged after factoring into `_validate_relative_path` \u2014 only the message prefix varies by flag name. This preserves existing tests at `tests/test_handle_init_doc_mode.py:64-85`."
  ],
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

        Open significant flags:
        [
  {
    "id": "FLAG-001",
    "severity": "significant",
    "status": "open",
    "concern": "from-doc context propagation: the plan stores `state.config.from_doc`, but it only proposes surfacing imported decisions when `state[\"meta\"].get(\"imported_decisions\")` is non-empty. For the explicitly supported case where the source doc has no `## Settled Decisions` section, the path would be persisted yet never shown to the planner/worker, so the brief's requirement to keep the doc path as worker context is still unmet.",
    "evidence": "`_plan_prompt()` currently renders only the prep block, idea/notes, project directory, and clarification context (`megaplan/prompts/planning.py:85-136`), and `intent_and_notes_block()` only exposes the idea plus `meta.notes` (`megaplan/_core/workflow.py:144-156`). There is no existing prompt path for `config.from_doc`, so a zero-decision import would be invisible unless the plan adds explicit prompt plumbing for the path itself."
  },
  {
    "id": "FLAG-002",
    "severity": "significant",
    "status": "open",
    "concern": "success-criteria enforcement: the plan's Step 7 makes imported decisions become `must`/`info` criteria by prompt instruction alone, but the repository has no harness-side enforcement here. Without post-processing or validation in the plan/revise handlers, load-bearing decisions are not actually auto-promoted; they are only suggested to the model.",
    "evidence": "`handle_plan()` writes whatever `payload[\"success_criteria\"]` the worker returns straight into plan metadata (`megaplan/handlers.py:839-852`), and `handle_revise()` does the same for revised plans (`megaplan/handlers.py:1104-1118`). Since the plan does not add any repo-side merge/validation step around those payloads, a worker that omits an imported `SD-*` decision would silently drop the required auto-promotion behavior."
  }
]



        Requirements:
        - Before addressing individual flags, check: does any flag suggest the plan is targeting the wrong code or the wrong root cause? If so, consider whether the plan needs a new approach rather than adjustments. Explain your reasoning.
        - Update the plan to address the significant issues.
        - Keep the plan readable and executable.
        - Return flags_addressed with the exact flag IDs you addressed.
        - Include `changes_summary` as a short plain-English summary of what changed in the revision. If there were no concrete flags, say that explicitly (for example: `No critique flags were raised; refined wording and kept the plan aligned for execution.`).
        - Preserve or improve success criteria quality. Each criterion must have a `priority` of `must`, `should`, or `info`. Promote or demote priorities if critique feedback reveals a criterion was over- or under-weighted.
        - Verify that the plan remains aligned with the user's original intent, not just internal plan quality.
        - Remove unjustified scope growth. If critique raised scope creep, narrow the plan back to the original idea unless the broader work is strictly required.
        - Maintain the structural template: H1 title, ## Overview, phase sections with numbered step sections, ## Execution Order or ## Validation Order.
        - CRITICAL: Your entire revised plan markdown (all sections) must be output as the `plan` field in the structured output. The prose response must not contain the plan text.
        - CRITICAL: Return only the structured JSON object for the schema fields `plan`, `changes_summary`, `flags_addressed`, `assumptions`, `success_criteria`, and `questions`. Do not add commentary before or after the JSON object.

        Plan template — simple format (adapt to the actual repo and scope):
````md
# Implementation Plan: [Title]

## Overview
Summarize the goal, current repository shape, and the constraints that matter.

## Main Phase

### Step 1: Audit the current behavior (`megaplan/prompts.py`)
**Scope:** Small
1. **Inspect** the current implementation and call out the exact insertion points (`megaplan/prompts.py:29`).

### Step 2: Add the first change (`megaplan/evaluation.py`)
**Scope:** Medium
1. **Implement** the smallest viable change with exact file references (`megaplan/evaluation.py:1`).
2. **Capture** any tricky behavior with a short example.
   ```python
   issues = validate_plan_structure(plan_text)
   ```

### Step 3: Wire downstream behavior (`megaplan/handlers.py`, `megaplan/workers.py`)
**Scope:** Medium
1. **Update** the runtime flow in the touched files (`megaplan/handlers.py:400`, `megaplan/workers.py:199`).

### Step 4: Prove the change (`tests/test_evaluation.py`, `tests/test_megaplan.py`)
**Scope:** Small
1. **Run** the cheapest targeted checks first (`tests/test_evaluation.py:1`).
2. **Finish** with broader verification once the wiring is in place (`tests/test_megaplan.py:1`).

## Execution Order
1. Update prompts and mocks before enforcing stricter validation.
2. Land higher-risk wiring after the validator and tests are ready.

## Validation Order
1. Start with focused unit tests.
2. Run the broader suite after the flow changes are in place.
````

For complex plans, use multiple phases:
````md
## Phase 1: Foundation — Dependencies, DB, Types

### Step 1: Install dependencies (`package.json`)
...

### Step 2: Create database migration (`supabase/migrations/`)
...

## Phase 2: Core Integration

### Step 3: Port the main component (`src/components/`)
...
````

Template guidance:
- Simple plans: use `## Main Phase` with `### Step N:` sections underneath.
- Complex plans: use multiple `## Phase N:` sections, each containing `### Step N:` steps. Step numbers are global (not per-phase).
- The flat `## Step N:` format (without phases) also works for backwards compatibility.
- Key invariants: one H1 title, one `## Overview`, numbered step sections (`### Step N:` or `## Step N:`), and at least one ordering section.

> AGENT

Both flags are legitimate — neither suggests the plan targets the wrong code or root cause; they point to gaps in how the `--from-doc` signal propagates downstream. Addressing them requires two additions: (a) always surface `config.from_doc` to the planner/worker, not only when decisions were parsed; (b) enforce must/info promotion via a harness-side merge in `handle_plan`/`handle_revise`, not by prompt instruction alone. No scope growth — both additions are necessary for the feature as stated in the brief.

> TOOL

tool_use StructuredOutput
```json
{
  "plan": "# Implementation Plan: `--from-doc` flag + standardized `## Settled Decisions` format\n\n## Overview\n\nAdd a `--from-doc <path>` flag to `megaplan init` that imports a prior doc-mode artifact's settled decisions into the new plan. Concretely:\n\n- New pure parser `extract_settled_decisions(doc_text) -> tuple[list[dict], list[str]]` in `megaplan/doc_assembly.py` (peer to existing `assemble_doc` / `extract_sections`).\n- New `SettledDecisionFromDoc` TypedDict in `megaplan/types.py` (distinct from the existing `SettledDecision` produced by `gate`).\n- `handle_init` (`megaplan/handlers.py:728`) validates the path, parses the doc, stores `state.config.from_doc` and `state.meta.imported_decisions`.\n- **Always surface `config.from_doc`** (path string + any imported decisions) to the doc-mode execute prompt and the planning prompt, even when the source doc has zero `## Settled Decisions` (addresses FLAG-001).\n- **Enforce auto-promotion at the handler level**: after `handle_plan` (and `handle_revise`) receive the worker payload, a merge helper ensures every `load_bearing: true` imported decision has a matching `must` success criterion and every `load_bearing: false` has a matching `info` criterion. Idempotent — skips if the worker already produced a criterion referencing the SD-NNN id (addresses FLAG-002).\n- `--output` validation block at `handlers.py:748-758` is factored into a shared `_validate_relative_path(project_dir, raw, flag_name)` helper, reused by `--from-doc`.\n\nOut of scope (per brief): critique-level SD-citation checks, sidecar `settled_decisions.json`, `verify-against-doc` subcommand.\n\n## Main Phase\n\n### Step 1: Add `SettledDecisionFromDoc` TypedDict (`megaplan/types.py`)\n**Scope:** Small\n1. Add `SettledDecisionFromDoc(TypedDict, total=False)` at `megaplan/types.py:170` (next to `SettledDecision`), with: `id: str`, `decision: str`, `rationale: str`, `load_bearing: bool`. Distinct name — not a subclass or alias of `SettledDecision`.\n2. Extend `PlanState`'s `meta` TypedDict to allow optional `imported_decisions: list[SettledDecisionFromDoc]`.\n3. Extend `PlanState`'s `config` TypedDict to allow optional `from_doc: str`.\n\n### Step 2: Implement `extract_settled_decisions` (`megaplan/doc_assembly.py`)\n**Scope:** Medium\n1. Add `def extract_settled_decisions(doc_text: str) -> tuple[list[dict], list[str]]:` at the top of `megaplan/doc_assembly.py` (next to `extract_sections` at line 13). Returns `(decisions, warnings)`.\n2. Parse from the `## Settled Decisions` heading until the next `##`/EOF. Item format (markdown list):\n   ```\n   - id: SD-001\n     load_bearing: true\n     decision: <text>\n     rationale: <text>\n   ```\n   Each item starts with `- id:`; subsequent 2-space-indented `key: value` lines belong to the preceding item. Store `id` verbatim (tolerate non-3-digit IDs). Coerce `load_bearing` to `bool` (strings `true`/`false`, case-insensitive).\n3. Be tolerant: no heading → `([], [])`. Heading + zero items → `([], [])`. Item missing required fields (`id` or `decision`) → drop, append message to warnings, keep parsing. Never raise.\n4. Return keys: `{id, decision, rationale, load_bearing}`. Missing optional fields default to `\"\"` / `False`.\n\n### Step 3: Factor `_validate_relative_path` helper (`megaplan/handlers.py`)\n**Scope:** Small\n1. Extract the three-check validation at `megaplan/handlers.py:748-758` into a module-private helper `_validate_relative_path(project_dir: Path, raw: str, flag_name: str) -> str` that raises `CliError(\"invalid_args\", f\"{flag_name} ...\")` for absolute paths, `..` traversal, and out-of-project paths.\n2. Replace the inline block with `normalized_output_path = _validate_relative_path(project_dir, raw_output_path, \"--output\")`. Keep error message bodies identical (only the flag-name prefix varies) so existing `tests/test_handle_init_doc_mode.py::test_output_rejects_absolute_path` and `test_output_rejects_parent_traversal` continue to pass.\n\n### Step 4: Add `--from-doc` CLI flag (`megaplan/cli.py`)\n**Scope:** Small\n1. Add after `megaplan/cli.py:847` (after `--output`):\n   ```python\n   init_parser.add_argument(\"--from-doc\", default=None,\n                            help=\"Relative path to a prior doc-mode artifact whose \"\n                                 \"## Settled Decisions section should be imported. \"\n                                 \"Valid with --mode code or --mode doc.\")\n   ```\n\n### Step 5: Wire `handle_init` for `--from-doc` (`megaplan/handlers.py`)\n**Scope:** Medium\n1. After the `--output` block, validate and load:\n   ```python\n   raw_from_doc = getattr(args, \"from_doc\", None)\n   from_doc_rel: str | None = None\n   imported_decisions: list[dict] = []\n   parse_warnings: list[str] = []\n   if raw_from_doc:\n       from_doc_rel = _validate_relative_path(project_dir, raw_from_doc, \"--from-doc\")\n       from_doc_abs = project_dir / from_doc_rel\n       if not from_doc_abs.exists() or not from_doc_abs.is_file():\n           raise CliError(\"invalid_args\", f\"--from-doc path does not exist: {from_doc_rel}\")\n       imported_decisions, parse_warnings = extract_settled_decisions(from_doc_abs.read_text())\n   ```\n   No mode coupling — `--from-doc` is valid with `--mode code` or `--mode doc`.\n2. After the `state` dict is built, unconditionally persist both keys whenever `--from-doc` was passed (even with zero decisions — this is the load-bearing invariant for FLAG-001):\n   ```python\n   if from_doc_rel is not None:\n       state[\"config\"][\"from_doc\"] = from_doc_rel\n       state[\"meta\"][\"imported_decisions\"] = imported_decisions\n   ```\n3. Surface `parse_warnings` by appending to `state[\"meta\"][\"notes\"]` and adding a `warnings` field to the `StepResponse` at `handlers.py:819-829` when the list is non-empty.\n4. Add `from megaplan.doc_assembly import extract_settled_decisions` at the top of `handlers.py`.\n\n### Step 6: Surface `from_doc` in doc-mode execute prompts (`megaplan/prompts/execute_doc.py`) — addresses FLAG-001\n**Scope:** Small\n1. In `_execute_doc_prompt` at `megaplan/prompts/execute_doc.py:90`, read `state[\"config\"].get(\"from_doc\")`. When set, render a \"Prior doc context\" block before the requirements block that shows the path string unconditionally (whether or not decisions were imported), e.g.:\n   ```\n   Prior doc imported via --from-doc:\n   docs/prior-design.md\n   Imported decisions (from the source doc's ## Settled Decisions section): 0\n   ```\n   Include the count even when zero, so the worker knows the doc was consulted but had no decisions.\n2. When `state[\"meta\"].get(\"imported_decisions\")` is non-empty, extend the block to list each decision's `id`, `decision`, `rationale`, `load_bearing`.\n3. Extend `_EXECUTE_DOC_REQUIREMENTS_TEMPLATE` at line 67 with a bullet: when the document contains design decisions, emit a top-level `## Settled Decisions` section using the standardized format (show the exact markdown shape from Step 2, including `load_bearing: true|false` and the `SD-NNN` ID convention). Add a 1-line note: \"Downstream plans can import these via `megaplan init --from-doc`.\"\n4. Mirror the same path+count block and emission bullet in `_execute_doc_batch_prompt` at `megaplan/prompts/execute_doc.py:219-270`.\n5. Do not touch code-mode prompts.\n\n### Step 7: Surface `from_doc` in the planning prompt (`megaplan/prompts/planning.py`) — addresses FLAG-001\n**Scope:** Small\n1. In `_plan_prompt()` at `megaplan/prompts/planning.py:85-136`, read `state[\"config\"].get(\"from_doc\")`. When set, inject a \"Prior doc context\" block that always shows the path string, plus the imported decisions list if present (empty list rendered as \"No ## Settled Decisions section found — path stored for reference only\").\n2. When imported_decisions is non-empty, instruct the planner: \"For each imported decision with `load_bearing: true`, include a success criterion with `priority: 'must'` referencing the `SD-NNN` id. For `load_bearing: false`, include a criterion with `priority: 'info'`.\" This is a soft hint — the harness-side merge in Step 8 is the actual guarantee.\n\n### Step 8: Enforce auto-promotion in `handle_plan` and `handle_revise` (`megaplan/handlers.py`) — addresses FLAG-002\n**Scope:** Medium\n1. Add a module-private helper `_merge_imported_decision_criteria(state: PlanState, criteria: list[dict]) -> list[dict]`:\n   - Read `state[\"meta\"].get(\"imported_decisions\", [])`. If empty, return `criteria` unchanged.\n   - Collect the set of SD-NNN ids already referenced in any existing criterion's `criterion` text (substring match on `id`).\n   - For each imported decision whose id is NOT already referenced, append:\n     ```python\n     {\n         \"criterion\": f\"Plan adheres to imported decision {sd['id']}: {sd['decision']}\",\n         \"priority\": \"must\" if sd.get(\"load_bearing\") else \"info\",\n         \"requires\": [\"subjective_judgment\"] if sd.get(\"load_bearing\") else [],\n     }\n     ```\n   - Return the merged list. Idempotent — running it twice on the same state produces the same result.\n2. Call it in `handle_plan` at `megaplan/handlers.py:839-852` immediately before the worker's `payload[\"success_criteria\"]` is written to plan metadata:\n   ```python\n   merged = _merge_imported_decision_criteria(state, payload.get(\"success_criteria\", []))\n   payload[\"success_criteria\"] = merged\n   ```\n3. Mirror the same call in `handle_revise` at `megaplan/handlers.py:1104-1118`.\n4. This makes auto-promotion a repo-side guarantee, not a prompt suggestion. A worker that omits imported `SD-*` criteria will have them auto-appended by the harness; a worker that already includes them is preserved unchanged.\n\n### Step 9: Document in `megaplan/data/instructions.md`\n**Scope:** Small\n1. Update the \"Modes\" section (lines 19-27) and \"Start\" section (lines 29-34) to include `--from-doc <relative-path>` in the example invocation and document semantics (relative-to-project, file must exist, works with either mode, imports `## Settled Decisions`, harness auto-promotes to `must`/`info` criteria).\n2. Add a short \"Settled Decisions section format\" subsection showing the canonical markdown shape from Step 2.\n\n### Step 10: Unit-test the parser (`tests/test_doc_assembly.py`)\n**Scope:** Small\n1. Add tests covering the 5 brief-specified fixtures:\n   - empty string → `([], [])`\n   - doc with no `## Settled Decisions` section → `([], [])`\n   - doc with three well-formed decisions (mix of `load_bearing`) → 3 items with correct types\n   - doc with one malformed entry (missing `id`) in a well-formed section → good items returned, warning surfaced\n   - heading present but no items → `([], [])`\n2. Add one extra: `load_bearing` is case-insensitive and coerces to `bool`.\n\n### Step 11: Handler tests for `--from-doc` (`tests/test_handle_init_doc_mode.py`)\n**Scope:** Small\n1. Reuse `_bootstrap` / `_args` helpers at `tests/test_handle_init_doc_mode.py:16,39`. Extend `_args` with an optional `from_doc` kwarg.\n2. Add tests:\n   - `test_from_doc_valid_path_populates_state` — fixture doc with 2 load-bearing + 1 non-load-bearing; assert `state[\"config\"][\"from_doc\"]` and `state[\"meta\"][\"imported_decisions\"]`.\n   - `test_from_doc_nonexistent_path_rejected` — `CliError(\"invalid_args\")` with `--from-doc` in message.\n   - `test_from_doc_absolute_path_rejected` — same error class.\n   - `test_from_doc_parent_traversal_rejected` — same.\n   - `test_from_doc_doc_with_no_section_succeeds` — `config.from_doc` set; `meta.imported_decisions == []`.\n   - `test_from_doc_valid_with_code_mode` — confirm accepted without `--output`.\n\n### Step 12: Merge-helper tests (new `tests/test_imported_decision_merge.py` or extend `tests/test_handle_plan.py` if present)\n**Scope:** Small\n1. Unit-test `_merge_imported_decision_criteria` directly (import from `megaplan.handlers`):\n   - No imported decisions → criteria list returned unchanged.\n   - Two imported decisions (one load-bearing, one not), no worker criteria → merged list has 2 entries with correct priorities and `requires`.\n   - Imported decision already referenced in a worker criterion (id substring present) → not duplicated.\n   - Running the helper twice on the same input is a no-op (idempotent).\n2. Integration test through `handle_plan`: bootstrap a plan with imported_decisions, monkeypatch the worker to return a payload with empty `success_criteria`, assert the resulting plan metadata contains a `must`-priority criterion referencing each load-bearing SD-NNN id.\n\n### Step 13: Run full suite\n**Scope:** Small\n1. Targeted: `PYENV_VERSION=3.11.11 python -m pytest tests/test_doc_assembly.py tests/test_handle_init_doc_mode.py tests/test_imported_decision_merge.py -v`\n2. Full: `PYENV_VERSION=3.11.11 python -m pytest tests/` — expect ≥701 passed, 1 skipped (687 baseline + ~14 new tests; brief floor is 690).\n\n## Execution Order\n1. Types + parser first (Steps 1–2) — everything else imports them.\n2. Helper factoring (Step 3) before handler wiring (Step 5) so `--output` stays green.\n3. CLI flag (Step 4) + handler wiring (Step 5) together.\n4. Merge helper (Step 8) — implement before the planning prompt edit so the harness-side guarantee is landed first; the prompt becomes a soft hint that complements the guarantee.\n5. Prompt edits (Steps 6, 7) and docs (Step 9) after plumbing works.\n6. Tests (Steps 10–12) written incrementally alongside each piece.\n\n## Validation Order\n1. Parser unit tests (cheapest, pure function).\n2. Merge-helper unit tests (pure function, no I/O).\n3. Handler tests (CLI + state shape + handle_plan integration).\n4. Full pytest run for regression check on prompt/type integrations.\n",
  "changes_summary": "Addressed both significant flags. FLAG-001: Step 5 already stored `config.from_doc` unconditionally, but Steps 6 and 7 now explicitly surface the path string (and zero-decision status) in both the doc-mode execute prompt and the planning prompt — not gated on `imported_decisions` being non-empty. FLAG-002: Added new Step 8, a harness-side `_merge_imported_decision_criteria` helper called from `handle_plan` and `handle_revise` that guarantees every load-bearing imported decision gets a `must`-priority criterion and every non-load-bearing gets an `info` criterion in the plan metadata, idempotent and regardless of what the worker returns. Added Step 12 with merge-helper unit and integration tests. Promoted the planning-prompt criterion from `should` to `must` and added two new `must` criteria for the harness-side enforcement and zero-decision context propagation. Execution order updated so the merge helper lands before the prompt edits (harness guarantee precedes soft hints). Test count bumped from ~12 to ~14 new tests (≥701 passed expected).",
  "flags_addressed": [
    "FLAG-001",
    "FLAG-002"
  ],
  "assumptions": [
    "Standard section format uses markdown list items with `- id: SD-NNN` followed by indented `load_bearing: / decision: / rationale:` lines. Parser returns a (decisions, warnings) tuple so the handler can surface tolerant-parse warnings without silently dropping data.",
    "`--from-doc` does not require the target path to itself be a megaplan-produced artifact — any text file with a parseable section works. Path validity is enforced (exists, is a file, relative to project_dir), but content is handled tolerantly.",
    "PlanState/PlanMeta TypedDicts are structurally typed with `total=False` (or similar), so adding optional `imported_decisions` and `from_doc` keys won't require invasive type changes elsewhere. If they are `total=True`, Step 1 broadens slightly.",
    "The existing `--output` error messages are assumed to be unchanged after factoring into `_validate_relative_path` — only the message prefix varies by flag name. This preserves existing tests at `tests/test_handle_init_doc_mode.py:64-85`.",
    "Harness-side auto-promotion uses substring match on `SD-NNN` ids to detect existing references in worker-produced criteria. This is tolerant (worker can phrase the criterion text freely) but relies on the id string appearing verbatim. If a worker rephrases the id (e.g. 'decision 001' instead of 'SD-001'), the helper will append a duplicate — acceptable trade-off for simplicity; tests cover both the reference-found and no-reference paths.",
    "Generated auto-promoted criteria use `requires: ['subjective_judgment']` for must-priority and `requires: []` for info-priority. This matches the template guidance (must must have non-empty requires; info may be empty) and is appropriate because 'plan adheres to decision X' is inherently judgmental."
  ],
  "success_criteria": [
    {
      "criterion": "`PYENV_VERSION=3.11.11 python -m pytest tests/` passes with ≥701 passed and 1 skipped (687 baseline + ~14 new tests; minimum floor is 690 per brief).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <valid relative path>` with a doc containing 3 well-formed decisions populates `state.config.from_doc` to the normalized relative path and `state.meta.imported_decisions` to a list of 3 dicts with keys {id, decision, rationale, load_bearing}.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <nonexistent>` raises `CliError(\"invalid_args\", ...)` with a message that contains `--from-doc`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc /absolute/path` and `--from-doc ../escape.md` both raise `CliError(\"invalid_args\", ...)`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`megaplan init --from-doc <doc with no ## Settled Decisions section>` succeeds; `state.config.from_doc` is set; `state.meta.imported_decisions == []`.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "When `state.config.from_doc` is set (regardless of whether imported_decisions is empty), the doc-mode execute prompt and the planning prompt both render the from_doc path string and an imported-decision count. Verifiable by asserting the prompt output strings contain the path when the state has `from_doc` set and `imported_decisions == []`.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "After `handle_plan` runs with `state.meta.imported_decisions` containing one load-bearing and one non-load-bearing decision, the resulting plan metadata's `success_criteria` contains a `must`-priority criterion referencing the load-bearing SD id and an `info`-priority criterion referencing the non-load-bearing SD id — even when the worker returns an empty success_criteria list. Same guarantee for `handle_revise`.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`_merge_imported_decision_criteria` is idempotent: running it twice on the same state produces the same output, and worker-produced criteria that already reference an SD-NNN id are not duplicated.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`extract_settled_decisions` is a pure function in `megaplan/doc_assembly.py` (no filesystem or state access); its 5+ unit tests pass.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`SettledDecisionFromDoc` is a distinct TypedDict in `megaplan/types.py`, not a subclass or alias of the existing `SettledDecision`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "A single `_validate_relative_path` helper in `megaplan/handlers.py` is used by both `--output` and `--from-doc` validation (no duplicated absolute/`..`/out-of-project checks).",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Doc-mode execute prompt (`megaplan/prompts/execute_doc.py`) instructs the worker to emit a `## Settled Decisions` section in the standardized format when decisions are produced.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Planning prompt (`megaplan/prompts/planning.py`) surfaces `state.meta.imported_decisions` as a \"Prior doc context\" block and instructs the planner to emit must/info criteria referencing SD-NNN ids. (Soft hint complementing the harness-side merge in Step 8.)",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "`megaplan/data/instructions.md` documents `--from-doc` and shows the canonical `## Settled Decisions` section format.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "No out-of-scope work: no critique-level SD citation check, no sidecar `settled_decisions.json` writer, no `verify-against-doc` subcommand.",
      "priority": "must",
      "requires": [
        "parse_diff",
        "read_files"
      ]
    },
    {
      "criterion": "Parse warnings from malformed entries are surfaced to the user either in the `StepResponse` returned by `handle_init` or via `state.meta.notes`.",
      "priority": "should",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Each function added or modified keeps a single responsibility; no change exceeds ~60 lines of net new code per step (Step 8's merge helper + handle_plan/revise wiring is the largest).",
      "priority": "should",
      "requires": [
        "parse_diff"
      ]
    }
  ],
  "questions": [
    "The brief specifies a ## Settled Decisions section format but does not pin down exact markdown syntax. I've proposed `- id: SD-NNN` with indented `key: value` lines (Step 2). Is that the intended shape, or would you prefer YAML fenced-blocks, an HTML comment block, or a table?"
  ]
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Revision delivered. Both flags addressed:

- **FLAG-001** — Steps 6 & 7 now unconditionally render `config.from_doc` (path + decision count) in the doc-mode execute prompt and the planning prompt, decoupled from whether `imported_decisions` is non-empty.
- **FLAG-002** — New Step 8 adds `_merge_imported_decision_criteria` called from `handle_plan` and `handle_revise`, making auto-promotion a harness-enforced invariant rather than a prompt hint. New Step 12 covers merge-helper unit + integration tests.

Bumped two `should` criteria to `must` and added three new `must` criteria covering the zero-decision context path, the handler-side auto-promotion, and merge idempotency. Execution order adjusted so the merge helper lands before the prompt edits.

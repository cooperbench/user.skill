> DEVELOPER

Read and understand these files, then make the changes for Step 1 of the plan: 1. Read `desloppify/engine/_plan/plan_public_exports.py` - this should be deleted 2. Read `desloppify/engine/_plan/__init__.py` - remove references to plan_public_exports and engine.plan shim 3. Verify no other files import from plan_public_exports Changes: - Delete `desloppify/engine/_plan/plan_public_exports.py` - Edit `desloppify/engine/_plan/__init__.py` to remove references to the deleted file After making changes, run: `python -m pytest desloppify/tests/engine/ -q`

> AGENT

Let me read the relevant files first.

> DEVELOPER

I need to understand the triage bridge structure. Read these files and report their full contents: 1. `desloppify/engine/_plan/epic_triage_apply.py` 2. `desloppify/engine/_plan/epic_triage_dismiss.py` 3. `desloppify/engine/_plan/epic_triage_parsing.py` 4. `desloppify/engine/_plan/epic_triage_prompt.py` 5. `desloppify/engine/_plan/triage/__init__.py` (if exists) 6. `desloppify/engine/_plan/compat/` - list all files and read each one 7. `desloppify/engine/_plan/triage/` - list all files and read each .py file 8. `desloppify/engine/plan_triage.py` 9. `desloppify/engine/_plan/__init__.py` Also search for all imports of `epic_triage_apply`, `epic_triage_dismiss`, `epic_triage_parsing`, `epic_triage_prompt`, and `compat.triage` across the codebase. Report the full content of each file and all import locations found.

> AGENT

No files import from `plan_public_exports`. Let me also check if `engine.plan` shim exists and references it.

> AGENT

I'll systematically read these files and search for imports. Let me start with reading the files and searching for imports in parallel.

> AGENT

Now let me read the compat/triage files and the triage/ subpackage files:

> AGENT

`PLAN_PUBLIC_EXPORTS` is only referenced in the file itself. The `__init__.py` mentions `engine.plan` only in the docstring (which is fine - it's describing the architecture). There are no imports to remove from `__init__.py` - it's just a docstring. Now let me delete the file and run tests.

> DEVELOPER

Read these files and report their full contents. I need exact content for making edits. Step 3 files: 1. `desloppify/languages/typescript/detectors/analysis.py` 2. `desloppify/languages/typescript/detectors/cli.py` 3. `desloppify/languages/typescript/tests/test_ts_deprecated.py` (if it has ts_detector_analysis references) Step 4 files: 4. `desloppify/languages/typescript/analysis.py` 5. `desloppify/languages/typescript/__init__.py` Step 5 files: 6. `desloppify/languages/__init__.py` 7. `desloppify/languages/framework.py` Also search for: - All imports of `detectors.analysis` in typescript directory - All imports of `typescript.analysis` or `ts_analysis_mod` - All references to `_COMPAT_EXPORTS` in languages/ directory - The test file `test_typescript_detectors_fixers_and_wrappers_split_direct.py` - find and read it Report full file contents for all files found.

> AGENT

Now let me read the remaining triage files:

> AGENT

I'll search for and read all the requested files. Let me start by finding them and reading their contents.

> AGENT

Now let me get more detailed import information to fully trace the imports:

> AGENT

Now let me read all these files:

> AGENT

Now let me search for all imports of `detectors.analysis` in the typescript directory:

> AGENT

All 38 engine tests pass. Here's what was done: - **Deleted** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/plan_public_exports.py` - this file contained only a `PLAN_PUBLIC_EXPORTS` list used by the now-deleted `engine.plan` shim. No other files imported from it or referenced `PLAN_PUBLIC_EXPORTS`. - **No changes needed** to `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py` - it had no imports or references to `plan_public_exports`. The docstring mentions the public facades (`engine.plan_state`, `engine.plan_ops`, etc.) but that's architectural documentation, not a reference to the deleted file.

> AGENT

Perfect! Now I have all the information needed. Let me provide a comprehensive report. ## Complete File Contents Report I have read all requested files. Here is the summary of findings: ### Step 3 Files: **1. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/analysis.py`** - 20 lines total - A simple canonical facade that re-exports from `detectors.deps`, `detectors.facade`, and `detectors.smells` - Contains: `build_dep_graph`, `build_dynamic_import_targets`, `detect_reexport_facades`, `detect_smells`, `ts_alias_resolver` **2. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/cli.py`** - 342 lines total - CLI surface for all TypeScript detector commands - Line 31: `import desloppify.languages.typescript.detectors.analysis as ts_detector_analysis_mod` - Uses `ts_detector_analysis_mod` at lines: 85, 90, 116, 122, 123, 202 - Re-exports command functions and `get_detect_commands()` **3. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/tests/test_ts_deprecated.py`** - No references to `ts_detector_analysis`. Tests the deprecated symbol detection feature. - Tests at lines 24-26 use `deprecated_detector_mod.detect_deprecated_result()` instead ### Step 4 Files: **4. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/analysis.py`** - 81 lines total - Canonical TypeScript analysis ownership surface (non-CLI) - Imports from `detectors.deps` at line 15 - Re-exports: `TS_COMPLEXITY_SIGNALS`, `TS_GOD_RULES`, `TS_SKIP_DIRS`, `TS_SKIP_NAMES` - Functions: `ts_treesitter_phases()`, `ts_extract_functions()`, plus re-exported aliases - Line 61: `build_dep_graph = deps_detector_mod.build_dep_graph` - Line 62: `detect_ts_security_result = detect_ts_security` **5. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/__init__.py`** - 139 lines total - Language configuration module - Line 21: `from desloppify.languages.typescript import analysis as ts_analysis_mod` - Line 23: `import desloppify.languages.typescript.detectors.cli as ts_detector_cli_mod` - Uses `ts_analysis_mod` extensively in TypeScriptConfig class (lines 45-48, 52, 64, 68-77, 86) - Imports from `ts_analysis_mod`: phases, constants, build_dep_graph, detect_ts_security_result, ts_extract_functions, ts_treesitter_phases ### Step 5 Files: **6. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/__init__.py`** - 98 lines total - Language registration API module - Lines 39-44: Defines `_COMPAT_EXPORTS` dict with backward-compat submodule aliases - Lines 47-52: `__getattr__` function for lazy loading compat exports **7. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/framework.py`** - 113 lines total - Public framework facade - Lines 41-46: Defines `_COMPAT_EXPORTS` dict (identical pattern to `__init__.py`) - Lines 49-59: `__getattr__` function for lazy loading compat exports - Contains actual public exports like `LangConfig`, `auto_detect_lang`, `get_lang`, `make_lang_config` ### Key Test File: **8. `/Users/user_c042661f/Documents/desloppify/desloppify/tests/lang/typescript/test_typescript_detectors_fixers_and_wrappers_split_direct.py`** - 352 lines total - Critical validation tests for the TypeScript module structure - Line 12: `import desloppify.languages.typescript.analysis as ts_analysis_mod` - Line 12: `import desloppify.languages.typescript.detectors.analysis as ts_detector_analysis_api_mod` - Tests verify: - Line 22-28: `ts_lang_mod` uses `analysis as ts_analysis_mod` (line 24) - Line 45-52: `ts_detector_cli_api_mod` imports and uses `ts_detector_analysis_mod` - Lines 255-352: Test coverage for CLI command registry passthrough ## Import Search Results: **Imports of `detectors.analysis` in typescript directory:** - Only found in: `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/cli.py` (line 31) **Imports of `typescript.analysis` in typescript directory:** - Only found in: `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/__init__.py` (line 21) **References to `_COMPAT_EXPORTS` in languages/ directory:** - `/Users/user_c042661f/Documents/desloppify/desloppify/languages/__init__.py` (lines 39-44) - `/Users/user_c042661f/Documents/desloppify/desloppify/languages/framework.py` (lines 41-46) […]

> AGENT

Perfect! Now let me compile my comprehensive report based on all the files I've read: ## Triage Bridge Structure - Complete Report I've analyzed the triage bridge architecture across the codebase. Here's the full mapping: ### File Contents Summary #### Root-Level Bridge Files (Compatibility Shims) **1. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py`** (13 lines) - Bridge module using `importlib.import_module` to load `desloppify.engine._plan.compat.triage.apply` - Forwards all exports from canonical implementation **2. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py`** (13 lines) - Bridge module using `importlib.import_module` to load `desloppify.engine._plan.compat.triage.dismiss` - Forwards all exports from canonical implementation **3. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py`** (13 lines) - Bridge module using `importlib.import_module` to load `desloppify.engine._plan.compat.triage.parsing` - Forwards all exports from canonical implementation **4. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py`** (13 lines) - Bridge module using `importlib.import_module` to load `desloppify.engine._plan.compat.triage.prompt` - Forwards all exports from canonical implementation #### Canonical Implementation Files (Under compat/) **5. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/apply.py`** (240 lines) - **Core implementation of plan mutations during triage** - Key exports: `TriageMutationResult` (dataclass), `apply_triage_to_plan()` - Functions: - `_epic_sort_key()` — sort epics by dependency_order - `_normalized_epic_name()` — ensure EPIC_PREFIX - `_update_existing_epic_cluster()` — mutate existing epic with new data - `_create_epic_cluster()` — create new epic cluster from triage data - `_upsert_triage_clusters()` — create/update all epics, return counts - `_reorder_queue_by_dependency()` — reorder work queue by epic dependency_order - `_set_triage_meta()` — update plan["epic_triage_meta"] with snapshot hash, dismissed_ids, etc. - `apply_triage_to_plan()` — orchestrator: upserts clusters, dismisses issues, reorders queue, sets metadata **6. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/dismiss.py`** (73 lines) - **Dismissal logic for triage-rejected issues** - Key exports: `dismiss_triage_issues()` - Functions: - `_triaged_out_payload()` — create skip record with kind='triaged_out' - `dismiss_triage_issues()` — move dismissed issues from queue to skipped dict, return (dismissed_ids, count) **7. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/parsing.py`** (168 lines) - **Parsing and validation of raw LLM triage output** - Key exports: `ISSUE_ID_RE`, `extract_issue_citations()`, `parse_triage_result()` - Regex patterns: `ISSUE_ID_RE` (full IDs), `BRACKET_SHORT_ID_RE` (short hashes in brackets) - Functions: - `extract_issue_citations()` — extract issue IDs from free text (supports full IDs, short hashes, bracketed short) - `_parse_action_steps()` — parse and normalize action_steps list (title, detail, issue_refs, done) - `parse_triage_result()` — validate raw LLM dict into TriageResult (filters invalid IDs, validates direction) **8. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/prompt.py`** (352 lines) - **Data contracts and prompt building for legacy whole-plan triage** - Key dataclasses: - `TriageInput` — all data needed for triage (open_issues, mechanical_issues, existing_epics, dimension_scores, new_since_last, resolved_since_last, previously_dismissed, triage_version, resolved_issues, completed_clusters) - `DismissedIssue` — issue_id + reason - `ContradictionNote` — kept issue, dismissed issue, reason - `TriageResult` — strategy_summary, epics list, dismissed_issues, contradiction_notes, priority_rationale - Key functions: - `_issue_dimension()` — extract dimension from issue detail dict - […]

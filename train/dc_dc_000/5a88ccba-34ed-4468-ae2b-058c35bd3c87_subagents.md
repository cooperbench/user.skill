---
session_id: "5a88ccba-34ed-4468-ae2b-058c35bd3c87:subagents"
developer: "dc:dc_000"
split: train
source: dataclaw
repo: peteromallet/my-dataclaw-data
start_time: "2026-04-15T08:05:07.836Z"
n_turns: 14
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Read the following files in /Users/user_c042661f/Documents/megaplan and report their full contents: 1. megaplan/prompts/prep.py 2. megaplan/prompts/execute.py 3. megaplan/prompts/review.py 4. megaplan/prompts/__init__.py 5. megaplan/prompts/finalize.py Also check if there's a megaplan/prompts/_shared.py or similar shared helpers file. Report all contents.

> AGENT

I'll read all the specified files in the megaplan/prompts directory.

> AGENT

Now let me read the shared helpers file and also check if prep.py exists:

> AGENT

I notice that `prep.py` does not exist as a standalone file. Let me check the planning.py file to see if it contains prep-related functions:

> AGENT

Now let me also check if there are additional prompt-related files like critique.py and gate.py:

> AGENT

Perfect! Now I have all the files. Let me provide a comprehensive report of all the prompt files and their contents. ## Report: megaplan/prompts Directory I've successfully read all the prompt-related files in the `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/` directory. Here's a summary: ### Files Found and Their Contents: **1. `/megaplan/prompts/__init__.py`** (185 lines) - Main dispatch table for prompt builders - Defines three model-specific prompt builder dictionaries: `_CLAUDE_PROMPT_BUILDERS`, `_CODEX_PROMPT_BUILDERS`, and `_HERMES_PROMPT_BUILDERS` - Maps step names (plan, prep, critique, revise, gate, finalize, execute, review) to their respective builder functions - Provides `create_claude_prompt()`, `create_codex_prompt()`, and `create_hermes_prompt()` functions that dispatch to builders - Includes a nested harness guard to prevent recursive megaplan invocations - Exports all public builders and helper functions **2. `/megaplan/prompts/execute.py`** (387 lines) - Builds execution-phase prompts - Key functions: - `_execute_prompt()` - Main execution prompt builder - `_execute_batch_prompt()` - For batched task execution - `_execute_review_block()` - Includes findings from prior review phase - `_execute_nudges()` - Adds sense checks, watch items, and debt reminders - `_execute_rerun_guidance()` - Handles re-execution and rework scenarios - `_execute_approval_note()` - Notes approval status - Contains `_EXECUTE_OUTPUT_SHAPE_EXAMPLE` showing expected executor JSON output format - Contains `_EXECUTE_REQUIREMENTS_TEMPLATE` with execution constraints and verification guidelines **3. `/megaplan/prompts/review.py`** (563 lines) - Builds review-phase prompts - Key functions: - `_review_prompt()` - Main review prompt with criteria, task, and sense-check guidance - `single_check_review_prompt()` - Focused parallel review for one check dimension - `parallel_criteria_review_prompt()` - Parallel mode criteria-only review, anchored to issue text - `_review_template_payload()` - Pre-populated template with task/sense-check IDs - `_write_review_template()` - Writes output template with verdicts and criteria - `_build_review_checks_template()` - Builds check templates with prior findings for iteration - `_settled_decisions_review_block()` - Displays gate decisions for verification - Supports multiple review modes (parallel vs. full) and iterations **4. `/megaplan/prompts/finalize.py`** (100 lines) - Builds finalize-phase prompt that prepares execution-ready briefing - Key function: - `_finalize_prompt()` - Creates structured JSON output (tasks, watch items, sense checks, validation coverage) - Requires tasks array with IDs, descriptions, dependencies, status, and executor notes - Validates plan coverage by mapping each plan step to finalize tasks - Includes guidance on task proportionality and final verification requirements **5. `/megaplan/prompts/planning.py`** (193 lines) - Builds planning and prep phase prompts - Key functions: - `_plan_prompt()` - Main planning prompt builder - `_prep_prompt()` - Engineering brief builder (analyzes codebase to produce brief) - Contains `PLAN_TEMPLATE` - Example markdown structure for plans (phases, steps, execution order, validation order) - Prep phase decides whether investigation is needed […]

> DEVELOPER

Read the following files in /Users/user_c042661f/Documents/megaplan and report their full contents: 1. megaplan/execution.py (focus on _merge_batch_results around line 256, _build_aggregate_execution_payload around line 136, _run_and_merge_batch around line 349, _check_done_task_evidence) 2. megaplan/evaluation.py (focus on validate_execution_evidence around line 123) 3. megaplan/execution_timeout.py (focus on _merge_timeout_checkpoint around line 110, _reset_timeout_invalid_tasks around line 41, _recover_execute_timeout around line 163) 4. megaplan/handlers.py (focus on _write_finalize_artifacts around line 376, and _build_status_payload around line 285) 5. megaplan/cli.py (focus on _build_status_payload around line 285) Report the actual line numbers for each function so I know exact locations.

> AGENT

I'll read these files and report their contents with line numbers.

> AGENT

I need to read the remaining files in sections. Let me read the handlers.py and cli.py files with specific ranges:

> AGENT

Now let me read the execution.py file with specific sections:

> AGENT

Now let me read the handlers.py file in sections:

> AGENT

Now let me read the cli.py file for the _build_status_payload function:

> AGENT

Now let me search for _check_done_task_evidence to find its location:

> AGENT

Perfect! Now I have all the information. Let me compile a comprehensive report with exact line numbers: ## Summary Report Here are the requested files with their exact function locations: ### 1. **megaplan/execution.py** - **`_build_aggregate_execution_payload`**: Lines 136-187 - **`_merge_batch_results`**: Lines 256-346 - **`_run_and_merge_batch`**: Lines 349-451 - **`_check_done_task_evidence`**: Located in `megaplan/execution_quality.py` at lines 12-37 (imported into execution.py at line 32) ### 2. **megaplan/evaluation.py** - **`validate_execution_evidence`**: Lines 123-243 ### 3. **megaplan/execution_timeout.py** - **`_reset_timeout_invalid_tasks`**: Lines 41-101 - **`_merge_timeout_checkpoint`**: Lines 110-160 - **`_recover_execute_timeout`**: Lines 163-301 ### 4. **megaplan/handlers.py** - **`_build_status_payload`**: NOT FOUND in handlers.py (this function is in cli.py) - **`_write_finalize_artifacts`**: Lines 376-384 ### 5. **megaplan/cli.py** - **`_build_status_payload`**: Lines 282-338 ### Important Note: There is **no `_build_status_payload` function in handlers.py**. The function exists in `cli.py` at line 282. The handlers.py file does contain related functions like `_write_finalize_artifacts` (line 376) which you requested, and other handler functions, but not a function by that name. All functions have been located with their precise line numbers. The execution_quality.py file contains `_check_done_task_evidence` which is imported and used in execution.py rather than being defined there.

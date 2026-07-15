> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only. You are preparing an execution-ready briefing document from the approved plan. Project directory: /Users/user_c042661f/Documents/megaplan Idea: Implement v0.15.0 doc-mode per /Users/user_c042661f/Documents/megaplan/idea-doc-mode.txt — see that file for full spec. Approved plan: # Implementation Plan: v0.15.0 doc-mode (metaplan) ## Overview Megaplan currently only produces code artifacts. This feature adds `--mode doc` so the same harness can produce structured documents (plans, RFCs, design docs). The core state machine, flag taxonomy, critique/gate/revise loop, and robustness levels are unchanged. What changes: (1) `plan.json` gains `mode` and `output_path` fields, (2) new doc-mode prompt variants for prep, execute, and review, (3) a new execution schema with `sections_written` instead of `files_changed`, (4) a new `doc_assembly.py` module to assemble sections into the output file, (5) `validate_execution_evidence` branches on mode, (6) a `doc-quality` critique category, (7) finalize handler skips test baseline capture and verification-task injection for doc mode, (8) timeout recovery branches on mode for checkpoint merge and task validation, and (9) Hermes worker's execute fallback reconstructs doc-shaped payloads when mode is doc. Key files: `cli.py` (parser), `handlers.py` (init + finalize + execute + review), `types.py` (PlanState/PlanConfig), `schemas.py` (execution schema), `evaluation.py` (audit), `merge.py` (validation), `execution.py` (batch loop), `execution_timeout.py` (timeout recovery), `hermes_worker.py` (Hermes fallback), `workers.py` (schema selection), `prompts/` (prompt builders), `checks.py` (critique categories). The spec is well-scoped: single output file, no mixed-mode, no loop-mode doc support. Existing code-mode tests remain untouched. ## Phase 1: Foundation — Types, Config, CLI, Schema ### Step 1: Add mode/output_path to plan config and types (`megaplan/types.py`) **Scope:** Small 1. **Add** `mode` and `output_path` as optional fields to `PlanConfig` TypedDict (`megaplan/types.py:28`). `mode` is `str` (values: `"code"`, `"doc"`), `output_path` is `str`. 2. **Verify** that `PlanState` inherits `config: PlanConfig` at `types.py:115`, so the new fields propagate automatically. ### Step 2: Wire `--mode` and `--output` CLI flags (`megaplan/cli.py:811`, `megaplan/handlers.py:717`) **Scope:** Small 1. **Add** `--mode` argument to `init_parser` with `choices=["code", "doc"]`, `default="code"` (`cli.py:811`, after line 820). 2. **Add** `--output` argument to `init_parser` (`cli.py:811`). Required only when `mode=doc`. 3. **Update** `handle_init` (`handlers.py:717`): - Validate that `--output` is provided when `--mode doc` and raise `CliError` otherwise. - Validate that `output_path` is relative (no leading `/`) and […]

> AGENT

Reading the idea doc and key source files to build the execution briefing.

> AGENT

Now let me read the remaining key files needed for the briefing.

> AGENT

Let me check a few more files for the workers and hermes paths.

> AGENT

Now let me check the remaining pieces needed — the execution flow, review handler, and the status builder.

> AGENT

Now let me check the remaining execution code for `_run_and_merge_batch` and `_check_done_task_evidence`, and the pyproject.toml / CHANGELOG.

> AGENT

I have enough context. Producing the finalize briefing now.

> AGENT

Finalize briefing produced with 14 tasks covering all 21 plan steps. Key structure: T1-T3 are independent foundation work (types/CLI, schemas, version bump), T4-T5 are prompts, T6-T10 are core logic, T11-T13 wire everything together, and T14 is the final test barrier. All four addressed critique flags (finalize handler, timeout recovery, Hermes worker, path containment) are covered in their respective tasks.

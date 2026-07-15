---
session_id: "4c5bc31f-1afc-47fc-923c-988f508e0808:subagents"
developer: "dc:dc_000"
split: train
source: dataclaw
repo: peteromallet/my-dataclaw-data
start_time: "2026-04-15T07:42:49.279Z"
n_turns: 4
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Explore the megaplan repository at /Users/user_c042661f/Documents/megaplan. I need to understand: 1. The overall file structure (main modules, entry points) 2. How the current pipeline works (plan → execute → review flow) 3. Key files: megaplan.sh, any Python modules, prompt templates, config files 4. How steps are currently executed and reviewed 5. What "modes" or step types currently exist Focus on src/ or the main code directory. Be thorough but skip .megaplan/ artifacts, docs/, and ops/ unless they contain core code. Report file paths and line numbers for [REDACTED]

> AGENT

I'll explore the megaplan repository systematically. Let me start with the top-level structure and key files in parallel.

> AGENT

Now let me read the core handlers, execution, and the _core module.

> AGENT

I now have a thorough understanding of the codebase. Here is the complete report: --- ## Megaplan Repository: Architecture Report ### 1. Overall File Structure The project is a Python package at `/Users/user_c042661f/Documents/megaplan/megaplan/` with the following top-level layout: ``` megaplan/ ← Python package root __main__.py ← entry point: python -m megaplan cli.py ← argparse + COMMAND_HANDLERS dispatch table types.py ← all TypedDicts, constants, CliError schemas.py ← JSON schema definitions for every step artifact handlers.py ← one handle_* function per pipeline step workers.py ← subprocess invocation of claude / codex / hermes execution.py ← batched execute loop execution_quality.py ← git-diff audit, quality deviations execution_timeout.py ← timeout recovery evaluation.py ← gate signal scoring, plan structure validation checks.py ← critique check registry (CRITIQUE_CHECKS tuple) review_checks.py ← review pre-check registry review_mechanical.py ← run_pre_checks() flags.py ← flag state transitions (critique/gate/review/revise) quality.py ← line-count capture merge.py ← _validate_and_merge_batch() parallel_critique.py ← hermes-parallel critique parallel_review.py ← hermes-parallel review hermes_worker.py ← Hermes/OpenRouter agent worker key_pool.py ← API key rotation auto.py ← auto-driver (drives full plan lifecycle hands-free) step_edit.py ← handle_step: add/remove/move plan steps _core/ __init__.py ← re-exports from submodules io.py ← file I/O, config, schemas_root, artifact paths state.py ← load/save plan state, history, sessions, plan lock workflow.py ← WORKFLOW state machine + Transition + robustness registries.py ← flag registry + debt registry phase_runtime.py ← PHASE_RUNTIME_POLICY per step prompts/ __init__.py ← create_claude_prompt / create_codex_prompt / create_hermes_prompt planning.py ← _plan_prompt, _prep_prompt, PLAN_TEMPLATE critique.py ← _critique_prompt, _revise_prompt, _write_critique_template execute.py ← _execute_prompt, _execute_batch_prompt finalize.py ← _finalize_prompt gate.py ← _gate_prompt review.py ← _review_prompt, _write_review_template _shared.py ← debt/note blocks, prep block rendering loop/ __init__.py engine.py ← MegaLoop iterative agent engine handlers.py ← handle_loop_init/run/status/pause types.py ← LoopSpec, LoopState, IterationResult TypedDicts prompts.py ← build_loop_prompt git.py ← git_commit, git_revert, parse_metric data/ instructions.md ← canonical AGENTS.md text claude_subagent_appendix.md codex_subagent_appendix.md tests/ ← pytest test suite evals/ ← SWE-bench evaluations pyproject.toml ← package metadata ``` --- ### 2. How the Current Pipeline Works The pipeline is a **typed state machine** defined in `/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py` (line 31). States are constants in `/Users/user_c042661f/Documents/megaplan/megaplan/types.py` (lines 12–21). **Full robustness flow (robust/superrobust):** ``` initialized → [prep] → prepped → [plan] → planned → [critique] → critiqued → gate decision: PROCEED+passed → [gate] → gated → [finalize] → finalized → [execute] → executed → [review] → done ITERATE → [revise] → planned (loop back to critique) ESCALATE → override required (add-note / force-proceed / abort) ``` **Standard (default):** skips `prep` — starts with `plan` directly. **Light:** skips `prep`, […]

---
session_id: "461601dd-e2bd-438b-9751-a6b91c5fdafe:subagents"
developer: "dc:dc_000"
split: train
source: dataclaw
repo: peteromallet/my-dataclaw-data
start_time: "2026-05-02T23:13:58.759Z"
n_turns: 11
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Explore /Users/user_c042661f/Documents/megaplan to map out how the "make a plan" process works. I want to understand the discrete steps in the planning pipeline (e.g. plan generation, critique, revise, review, etc.) and how they're composed today. Focus on: 1. The top-level pipeline orchestrator — what file/function runs `megaplan plan` end-to-end? Look in megaplan/cli.py, megaplan/chain.py, megaplan/handlers/, megaplan/agent/. 2. The discrete steps in the pipeline — identify each one (planner, critic, reviser, reviewer, judge, tiebreaker, etc.). For each, note: what file it lives in, what its inputs and outputs are (data shapes / artifacts), and how it's currently invoked. 3. How critiques work specifically — look at megaplan/parallel_critique.py and any review/ folder. What does a critique produce? How is it consumed downstream? 4. How the steps are wired together right now — is it a hardcoded sequence, a graph, configurable via profiles? Look at megaplan/profiles and megaplan/chain.py. 5. Robustness levels — how do different robustness/quality levels change which steps run? Quick mention only. 6. What "composability" obstacles exist today — e.g. shared state passed implicitly, steps that assume specific predecessors, types that aren't unified, hardcoded ordering. Return a structured report (under 600 words) with: (a) the list of primitive steps and their I/O, (b) where the orchestration logic lives, (c) the top 3-5 things that block free composition of these steps into arbitrary workflows. This is research only — no code changes.

> AGENT

I'll explore the megaplan repository to understand the "make a plan" process and how the pipeline is orchestrated.

> AGENT

Let me explore the directory structure and key files:

> AGENT

Now let me read the key orchestration files:

> AGENT

Now let me examine the handlers and understand the pipeline steps:

> AGENT

Now let me explore the auto.py and parallel_critique to understand the orchestration better:

> AGENT

Let me look at the profiles to understand how robustness levels affect the pipeline:

> AGENT

Now let me check the core module to understand how states transition and next steps are inferred:

> AGENT

Perfect! Let me also look at the revise handler and understand how critique results flow:

> AGENT

Now let me look at the shared handlers to understand the worker invocation pattern:

> AGENT

Excellent! Now I have enough understanding. Let me create a comprehensive report: ## MEGAPLAN "MAKE A PLAN" PIPELINE: STRUCTURAL ANALYSIS ### 1. THE DISCRETE STEPS & I/O CONTRACTS The pipeline consists of **11 primitive steps** (some are variants; true atoms are lower): | Step | File | Input | Output | Notes | |------|------|-------|--------|-------| | **init** | `handlers/init.py` | Idea string, project config | `PlanState` w/ `STATE_INITIALIZED` | Creates plan dir, loads config | | **prep** | `handlers/plan.py` | `STATE_INITIALIZED` | `prep.json` + `STATE_PREPPED` | Analyzes codebase, extracts context | | **plan** | `handlers/plan.py` | `STATE_PREPPED` or `STATE_PLANNED` (rerun) | `plan_vN.json` + metadata + `STATE_PLANNED` | Generates/refines plan, questions, success criteria | | **critique** | `handlers/critique.py` | `STATE_PLANNED` | `critique_vN.json` + flag registry + `STATE_CRITIQUED` | **Parallel checks** via `parallel_critique.py` (concurrent ThreadPoolExecutor) | | **revise** | `handlers/critique.py` | `STATE_CRITIQUED` + gate rec. ITERATE | `plan_vN+1.json` + `STATE_PLANNED` | Re-plan in response to critique flags | | **gate** | `handlers/gate.py` | `STATE_CRITIQUED` | `gate.json` + flag resolutions + `STATE_GATED` or branches | Judges: PROCEED / ITERATE / TIEBREAKER / ESCALATE | | **finalize** | `handlers/finalize.py` | `STATE_GATED` | `finalize.json` + prep tasks, test baseline + `STATE_FINALIZED` | Generates test/execution tasks | | **execute** | `handlers/execute.py` | `STATE_FINALIZED` | Task execution results + `STATE_EXECUTED` | Runs CLI commands, code changes | | **review** | `handlers/review.py` | `STATE_EXECUTED` | Task verdicts (✓/✗) + `STATE_DONE` or rework loop | Mechanical + parallel checks; can loop to finalize | | **tiebreaker-run** | `handlers/tiebreaker.py` | `STATE_TIEBREAKER_PENDING` | Researcher & challenger perspectives + `STATE_TIEBREAKER_READY` | Runs two agents in parallel on disputed flags | | **tiebreaker-decide** | `handlers/tiebreaker.py` | `STATE_TIEBREAKER_READY` | Tiebreaker decision record + routes to `STATE_CRITIQUED` or `STATE_AWAITING_HUMAN` | Human/LLM picks winner or escalates | ### 2. THE ORCHESTRATION LOGIC **Top-level entry:** `megaplan/cli.py` → `handle_*` → **`_run_worker()`** (in `handlers/shared.py`) **Persistence layer:** State machine in `_core/workflow.py` - **Current state** (`state["current_state"]`) gates which steps are valid - **Transitions** are condition-based: gate recommendation (ITERATE, PROCEED, ESCALATE, TIEBREAKER) determines next branch - **Workflow defs by robustness** override which steps run (e.g., `tiny` skips prep, `light` skips review) **Auto-driver:** `megaplan/auto.py` implements a **dumb loop**: 1. Read plan state via `megaplan status` 2. Call `megaplan [next-step]` 3. Check result; repeat until terminal state or escalation **Hardcoded orchestration points:** - `infer_next_steps(state)` in `_core/workflow.py:250` → looks at `state["current_state"]` + `state["last_gate"]["recommendation"]` - Each handler calls `_run_worker()`, which invokes the appropriate LLM worker - `_finish_step()` […]

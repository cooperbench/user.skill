> DEVELOPER

Can you explain to me what we hope to achieve with these code changes: '/home/<USER>/Code/rune/docs/superpowers/handoffs/2026-04-22-plan-execution-handoff.md'? What are our goals?

> TOOL

tool_use Read
id: toolu_01HiCYc6oJDgmB25h7wrwhrf
```json
{
  "file_path": "/home/<USER>/Code/rune/docs/superpowers/handoffs/2026-04-22-plan-execution-handoff.md"
}
```

> TOOL

tool_result
id: toolu_01HiCYc6oJDgmB25h7wrwhrf
```
1	# Plan Execution Handoff — 2026-04-22
2	
3	**Read this first.** You are resuming execution of three committed plans that together deliver the phase-benchmark pivot spec (`docs/superpowers/specs/2026-04-22-phase-benchmark-pivot.yaml`). The user invoked `/superpowers:executing-plans` then course-corrected to **subagent-driven-development**. Auto mode is active — execute autonomously, minimize interruptions, prefer action over planning.
4	
5	## Branch state
6	
7	- **Branch:** `feat/training-upgrade` (do NOT work on `main`)
8	- **Latest commit:** `388ef18 docs(plan): phase corpus producer for 25-oracle self-distillation`
9	- **Three plans committed and ready to execute:**
10	  - `dbabe1f` → `docs/superpowers/plans/2026-04-22-trajectory-encoder-pretraining.md` (Plan B, 9 tasks)
11	  - `2461812` → `docs/superpowers/plans/2026-04-22-benchmark-harness-library.md` (Plan A, 10 tasks)
12	  - `388ef18` → `docs/superpowers/plans/2026-04-22-phase-corpus-producer.md` (Plan C, 11 tasks)
13	- `main` branch is untouched.
14	
15	## Execution order (user-specified)
16	
17	```
18	Step 1  →  A + B (parallel)  →  Step C
19	```
20	
21	1. **Step 1 — `rune_runner.py --output-json` one-liner.** Inline. Trivial prerequisite for Plan C Task 2.
22	2. **Plan A + Plan B in parallel.** Use `superpowers:subagent-driven-development` — dispatch a fresh subagent per task; review between tasks. These plans touch disjoint code paths (`libs/evaluation/benchmarks/` vs `libs/model-training/encoder_pretrain/`), so they can run concurrently.
23	3. **Plan C […]

> AGENT

Let me check the referenced spec to understand the broader "why".

> TOOL

tool_use Read
id: toolu_014ixW6PRbk2kqrCLro5u8Qp
```json
{
  "file_path": "/home/<USER>/Code/rune/docs/superpowers/specs/2026-04-22-phase-benchmark-pivot.yaml"
}
```

> TOOL

tool_result
id: toolu_014ixW6PRbk2kqrCLro5u8Qp
```
1	meta:
2	  date: 2026-04-22
3	  title: "Phase-benchmark oracle pivot: replace per-(task,step) corpus with (5 phases x ~6 benchmarks) + self-distillation bootstrap"
4	  supersedes_sections_of:
5	    file: docs/superpowers/specs/2026-04-22-pr-28-training-upgrade-fit-assessment.yaml
6	    sections:
7	      - objective.terminal_goal      # refines episodic-memory claim to phase granularity
8	      - objective.training_mode_chosen
9	      - objective.rationale
10	      - deviations_from_t2l.keep.multi_step_trajectory_conditioning   # removed
11	      - gaps_blocking_terminal_goal.oracle_corpus_breadth             # rescoped
12	      - recommended_followups.priority_p0                             # reshuffled
13	  status: active_spec
14	  authored_by: noah+claude brainstorming session continuation
15	  adjacent_completed_work:
16	    - {ref: docs/superpowers/plans/2026-04-22-reconstruction-dataset-builder.md, status: landed}
17	    - {commit_range: "9f3ceec..8f64491", summary: "T2L reconstruction dataset builder subpackage; 42 tests; oracle-source-agnostic"}
18	
19	objective:
20	  terminal_goal: >
21	    Sakana-style Doc-to-LoRA hypernetwork that emits PHASE-SPECIALIZED LoRA adapters
22	    conditioned on (phase_id, task_description, trajectory_state_so_far), where phase
23	    is one of Rune's 5 pipeline roles (decompose, plan, code, integrate, diagnose).
24	    Each forward pass through the hypernetwork produces the adapter for the CURRENT
25	    phase given the TRAJECTORY ACCUMULATED SO FAR. This is "episodic memory in weight
26	    space" discretized at phase granularity rather than at arbitrary trajectory
27	    timestamps.
28	  training_mode_chosen: phase_benchmark_reconstruction_with_self_distillation
29	  rationale: >
30	    Reconstruction (L1 on oracle A/B matrices) is Sakana's validated path; we keep
31	    it. We replace "N tasks x K trajectory ticks" (unbounded […]

> AGENT

## What these plans are trying to achieve

**Terminal goal** (from the spec at `docs/superpowers/specs/2026-04-22-phase-benchmark-pivot.yaml`): build a Sakana-style **Doc-to-LoRA hypernetwork that emits phase-specialized LoRA adapters** — one adapter per Rune pipeline phase (decompose → plan → code → integrate → diagnose), conditioned on `(phase_id, task_description, trajectory_so_far)`. Each forward pass of the hypernetwork produces the adapter for the *current* phase given what's happened so far. This is "episodic memory in weight space," discretized at phase granularity.

**The pivot this handoff executes.** The prior plan trained oracles at "N tasks × K trajectory ticks" — unbounded corpus, fuzzy step semantics, no native labels. That's been replaced with **"5 phases × ~6 benchmarks"** = a bounded, natively evaluable 25-oracle corpus (24 per-(phase, benchmark) bins + 1 pooled `diagnose` bin, per resolved decision q4). Oracles are bootstrapped via **STaR-style self-distillation**: run the Qwen2.5-Coder-7B-Instruct + DeltaCoder pipeline across benchmark problems, keep only runs where the final code passes Pass@1, bin the phase-boundary artifacts, train one QLoRA per bin.

**What the three plans deliver:**

| Plan | Deliverable | Why it's needed |
|------|-------------|-----------------|
| **A — Benchmark Harness** (`libs/evaluation/benchmarks/`) | Unified Pass@1 runner for HumanEval, MBPP, APPS, BigCodeBench, DS-1000, LiveCodeBench on a `(model, adapter_stack)` pair […]
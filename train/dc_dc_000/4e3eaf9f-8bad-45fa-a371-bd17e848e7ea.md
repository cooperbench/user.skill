---
session_id: 4e3eaf9f-8bad-45fa-a371-bd17e848e7ea
developer: "dc:dc_000"
split: train
source: dataclaw
repo: peteromallet/my-dataclaw-data
start_time: "2026-03-12T13:03:04.563Z"
n_turns: 52
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

I need to understand how subjective/LLM-based review works in this codebase. Find: 1. Where subjective reviewers are defined and how they run 2. What prompts are sent to the LLM during review 3. How review state is persisted (state files, findings format) 4. How the review queue works — what gets reviewed and when 5. The `Finding` type and how review results are stored Focus on: `desloppify/engine/review/`, `desloppify/intelligence/`, and any files related to "subjective" or "llm" review. Also check `desloppify/state.py` for state persistence. Be thorough — read the actual prompt templates and review orchestration code.

> AGENT

I'll systematically explore the codebase to understand subjective/LLM-based review. Let me start with a broad search for review-related files and then dive into specific implementations.

> AGENT

Now let me look at the actual review source files:

> AGENT

Let me search for actual review command and review files:

> AGENT

Good! Now let me explore the main review command structure and state.py for Finding definition:

> AGENT

Let me look at the batch orchestrator and prompt template which should contain the actual LLM prompts:

> AGENT

Excellent! Now let me look at the prompt sections and understand the actual review queue:

> AGENT

Let me check the work queue implementation:

> AGENT

Now let me look at the intelligence review preparation to understand how review batches are prepared:

> AGENT

Now let me check the state.py for the Finding definition:

> AGENT

Now let me check how review issues are created and the importing system:

> AGENT

Excellent! Now let me look at how subjective reviews are defined and the reviewing process:

> AGENT

Now let me check the actual review batch execution to understand how results are processed:

> AGENT

Now let me check where review issues are created from the imported batch results:

> AGENT

Perfect! Now let me check how holistic review issues are imported:

> AGENT

Excellent! Now let me check how subjective assessments are stored and the dimensions themselves:

> AGENT

Let me check the actual dimensions definition file:

> AGENT

Perfect! Now let me look at how the runner executes the code and processes results:

> AGENT

Perfect! Now let me check how the state persistence works for review findings:

> AGENT

Now let me create a comprehensive summary document. Let me look at a few more key areas - how the queue selects what gets reviewed and the review selection process:

> AGENT

Perfect! Now I have a comprehensive understanding of the review system. Let me compile my findings into a detailed report. ## Summary: LLM-Based Subjective Review in Desloppify Based on my thorough exploration of the codebase, here's how subjective/LLM-based review works: --- ### 1. **Where Subjective Reviewers Are Defined and How They Run** #### Reviewers Definition: - **Core definitions**: `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/dimensions/holistic.py` and the JSON data file at `/Users/user_c042661f/Documents/desloppify/desloppify/languages/_framework/review_data/dimensions.json` - The dimensions file defines 20+ review dimensions (e.g., `naming_quality`, `logic_clarity`, `type_safety`, `abstraction_fitness`, etc.) - Each dimension has: `description`, `look_for` (patterns to detect), and `skip` (false positive guidelines) #### Execution Flow: 1. **CLI Entry**: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/cmd.py` (ReviewOptions dataclass) 2. **Batch Preparation**: - `prepare_holistic_review()` in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py` - builds review batches - `select_files_for_review()` in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/selection.py` - selects which files to review (excludes test/config/generated zones) 3. **Batch Assembly**: - Holistic batches assembled in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_batches.py` - Per-file batches in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_batches_builders.py` 4. **Prompt Rendering**: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/prompt_template.py` 5. **Execution**: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/runner/codex_batch.py` - calls the external Codex agent with the prompt 6. **Result Parsing**: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/core_parse.py` - extracts JSON payload from agent output --- ### 2. **Prompts Sent to the LLM During Review** #### Prompt Structure (from `prompt_template.py`): The prompt template has these key sections: 1. **Metadata Block**: - Repository root, blind packet path, batch index, batch name, batch rationale - Role: "You are a focused subagent reviewer for a single holistic investigation batch" 2. **Dimension Prompts Block**: - For each dimension in the batch, includes: - Human-friendly description (e.g., "Function/variable/file names that communicate intent") - `look_for` patterns (bullet-pointed anti-patterns) - `skip` guidance (false positive filters) 3. **Policy Block**: - Project-specific policies loaded from `engine/plan_state.py` 4. **Scoring Frame**: - Guidance for scoring 0-100 (e.g., 0-20 = systemic, 80-100 = well-managed) 5. **Scan Evidence Note**: - Dimension-specific guidance referencing mechanical detector outputs - Example: For `initialization_coupling`, use evidence from `holistic_context.scan_evidence.mutable_globals` 6. **Seed Files Block**: - List of files to read first (context-setting files) 7. **Historical Focus**: - Previously flagged issues for trend tracking (optional) 8. **Mechanical Concern Signals**: - Concerns raised by mechanical detectors for reviewer to confirm/dismiss 9. **Judgment Findings**: - Strengths/issues from past review rounds (optional) 10. **Task Requirements**: - "Report issues" (1 per dimension, capped by `max_batch_issues_for_dimension_count()`) - Issue format: dimension, identifier, summary, evidence, suggestion 11. **Output Schema** (JSON): ```json { "batch": "batch_name", "batch_index": N, "assessments": {"<dimension>": <0-100 with one decimal>}, "dimension_notes": { "<dimension>": { "evidence": [...], "impact_scope": "local|module|subsystem|codebase", "fix_scope": "single_edit|multi_file_refactor|architectural_change", "confidence": "high|medium|low", "issues_preventing_higher_score": "required when score > 85.0", "sub_axes": {<component>: 0-100} // […]

> DEVELOPER

I need to understand how the review agent is currently guided/constrained. Specifically: 1. Read the full prompt template at `desloppify/app/commands/review/batch/prompt_template.py` — I need the exact text of every section, especially any guidance about simplicity, KISS, YAGNI, or avoiding over-engineering 2. Read `desloppify/app/commands/review/prompt_sections.py` — the section builders 3. Read `desloppify/engine/plan_state.py` — how policies are loaded and what shape they take 4. Check `desloppify/intelligence/review/policy.py` — dimension-level policy 5. Look at the dimensions.json file at `desloppify/languages/_framework/review_data/dimensions.json` — check if any dimensions already encode simplicity principles in their `look_for` or `skip` fields 6. Check the output schema — what `dimension_judgment` and `dimension_notes` look like and how they're structured in the prompt I want to understand: what levers already exist to steer the agent's behavior and review philosophy? Where would new guidance naturally fit? Be very thorough — read the actual file contents, not just structure.

> AGENT

I'll systematically explore these files to understand the review agent's current guidance and constraints.

> AGENT

Now let me look at the policy loading code and the output schema more carefully:

> AGENT

Let me read the policy project file and understand how policies are loaded:

> AGENT

Let me explore the review command directory:

> AGENT

Now let me read the packet and runtime policy files to see how guidance is injected:

> AGENT

Now let me look at where the policy block is being built for the prompt:

> AGENT

Perfect! I can see the orchestrator.py is calling `load_policy_result` and `render_policy_block`. Let me check how the external review works:

> AGENT

Excellent! Now let me check what's in the system_prompt section of dimensions.json more carefully, and see if there are any other policy/guidance mechanisms:

> AGENT

Let me check those files for guidance patterns:

> AGENT

Perfect! Now let me also check the CLAUDE.md file mentioned in the memory:

> AGENT

Let me check if it exists with a glob:

> AGENT

Excellent! Now let me check the feedback_contract to understand the contract around dimension_notes and issues:

> AGENT

Perfect! Now I have a complete picture. Let me compile my findings into a comprehensive report. ## Summary of Findings: Review Agent Guidance Architecture Based on my thorough exploration of the codebase, here's **exactly how the review agent's behavior is currently guided and what levers exist to steer it**: --- ### 1. **PROMPT TEMPLATE HIERARCHY** (/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/prompt_template.py) The prompt is built from **discrete sections** joined together: 1. **Metadata block** (repo root, packet path, batch name/rationale) 2. **Dimension rubric** (from dimensions.json, with `look_for` and `skip` lists) 3. **Policy block** (project-specific rules — currently a plug point) 4. **Scoring frame** (explains what good means: "Judge how well the codebase serves a developer") 5. **Scan evidence note** (mechanical detectors as navigation aids, not scoring evidence) 6. **Seed files** (where to start) 7. **Historical focus** (prior issues flagged for re-evaluation) 8. **Mechanical concern signals** (adjudication task — confirm/dismiss/skip) 9. **Findings exploration** (CLI commands to explore detector output) 10. **Dimension-specific focus** (package_organization, abstraction_fitness, scan_evidence, workflow_integrity) 11. **Task requirements** (numbered checklist) 12. **Scope enums** (impact_scope, fix_scope values) 13. **Output schema** (the JSON structure with strict typing) --- ### 2. **SYSTEM PROMPT (The Philosophies)** (in /Users/user_c042661f/Documents/desloppify/desloppify/languages/_framework/review_data/dimensions.json, lines 388-?) This is **the primary behavior controller**. It contains: **Core scoring philosophy:** - "Your score is a holistic judgment... not inputs to a formula" - "Findings are illustrations that support your judgment" - Explicit independence: signals are "NOT evidence, NOT confirmed issues" - A detailed **6-step process**: READ → STRENGTHS → ISSUES → ISSUE CHARACTER → SCORE RATIONALE → SCORE - **Explicit anti-gaming guard**: "All three judgment fields are REQUIRED" - "Scores above 85 must include a non-empty `issues_preventing_higher_score` note" **Rules section (14 numbered rules):** - Rule 1: "Only emit findings you are confident about. When unsure, skip entirely." - Rule 5: "Calibrate confidence: high = any senior eng would agree..." - Rule 7: "Prefer quality over volume; do NOT force findings to hit a quota. Zero findings is valid." - Rule 8: **"FINDINGS MUST BE DEFECTS ONLY. Never report positive observations as findings."** - Rule 9: **"If a dimension has no defects, give it a high assessment score and return zero findings. Do NOT manufacture findings to justify a score."** - Rule 10: **"POSITIVE OBSERVATION TEST: Before emitting any finding, ask: 'Does this describe something that needs to change?' If the answer is no, it is NOT a finding."** - Rule 13: "Quick fixes vs planning" (exact changes for renames; […]

> DEVELOPER

Design an implementation plan for adding a "Dimension Context" system to the desloppify review pipeline. This system accumulates per-dimension understanding across review rounds so the LLM agent doesn't re-question settled aspects of the codebase. ## Background The review system sends batches of dimensions to an LLM agent (via Codex). Each batch covers ~5 dimensions. The agent reads code, scores dimensions 0-100, and reports issues. The problem: each review round starts mostly fresh — the agent repeatedly re-discovers the same patterns and re-questions the same design decisions. ## Current Architecture **Prompt template** built from sections in: - `desloppify/app/commands/review/batch/prompt_template.py` — main template assembly - `desloppify/app/commands/review/prompt_sections.py` — section renderers **Prompt sections** (in order): 1. Metadata (repo root, batch name/rationale) 2. Dimension rubric (from dimensions.json with look_for/skip) 3. Policy block (project-specific rules from `engine/_plan/policy/project.py`) 4. Scoring frame 5. Scan evidence note 6. Seed files 7. Historical focus (prior issues) 8. Mechanical concern signals 9. Findings exploration 10. Dimension-specific focus sections 11. Task requirements 12. Scope enums 13. Output schema **State persistence** in `.desloppify/state-{lang}.json`: - `subjective_assessments: dict[str, SubjectiveAssessment]` — per-dimension scores - `dimension_judgment` within SubjectiveAssessment — strengths, issue_character, score_rationale - State schema types in `engine/_state/schema_types.py` and `schema_types_review.py` **Review import pipeline**: - `intelligence/review/importing/assessments.py` — stores dimension scores - `intelligence/review/importing/per_file.py` — imports per-file issues - `intelligence/review/importing/holistic.py` — imports holistic issues - `app/commands/review/batch/core_parse.py` — parses JSON from agent output **Existing simplicity guardrails**: - System prompt rules 8-10: don't manufacture findings, positive observation test - Dimension `skip` fields: "Do NOT recommend config/context objects..." - Triage stage: `over-engineering` verdict filters net-negative suggestions - design_coherence dimension explicitly guards against unnecessary abstraction **Output schema** (JSON the agent must produce): ```json { "batch": "...", "assessments": {"dim": score}, "dimension_notes": {"dim": {evidence, impact_scope, fix_scope, confidence, ...}}, "dimension_judgment": {"dim": {strengths, issue_character, score_rationale}}, "issues": [{dimension, identifier, summary, related_files, evidence, suggestion, confidence, ...}], "retrospective": {root_causes, likely_symptoms, possible_false_positives} } ``` ## Design Requirements ### Dimension Context (accumulated understanding) 1. **Per-dimension context** stored in state: - `understanding: str` — prose summary of WHY things are the way they are (2-5 sentences) - `settled: list[str]` — investigated items confirmed as intentional (cap: 10) - Metadata: created_at, updated_at, stable_rounds (consecutive rounds with no changes) 2. **Prompt injection**: Before the task block, inject existing context per-dimension. Frame as "starting knowledge — do not re-investigate settled items unless code has clearly changed." 3. **Output schema extension**: Agent outputs `context_updates` with diff model: - `understanding: str | null` (null = no change) - `add_settled: list[str]` […]

> AGENT

I'll explore the codebase to understand the current architecture before designing the plan.

> AGENT

Now let me read the import pipeline and state schema files.

> AGENT

Now let me look at how the import pipeline works and the state persistence.

> AGENT

Let me now look at the merge logic, the import command, and the state migration patterns.

> AGENT

Let me check the state migration pattern and the holistic import function.

> AGENT

Let me check the system prompt rules and the existing packet build path to understand where context would be injected.

> AGENT

Now let me check how the blind packet is built (where state data gets injected into the packet for the agent) and the payload parsing.

> AGENT

Let me check how the batch normalization works (where raw agent output gets parsed into BatchResultPayload) and how the packet batches include state data.

> AGENT

Now let me look at how batch preparation injects state data into the packet (for context injection).

> AGENT

Let me check how the holistic orchestration builds the packet (where dimension context would be injected into the packet for prompt rendering).

> AGENT

Now let me look at how the system_prompt is loaded from dimensions data, to understand where the simplicity rule goes.

> AGENT

Now I have a thorough understanding of the architecture. Let me check one more thing - how batch results are collected and where context_updates would be extracted.

> AGENT

I now have a comprehensive understanding of the architecture. Let me trace one more path - how the packet's dimension context gets into each batch prompt.

> AGENT

I now have a thorough understanding of the full data flow. Here is the implementation plan. --- ## Implementation Plan: Dimension Context System ### Overview The Dimension Context system accumulates per-dimension understanding across review rounds so the LLM reviewer agent avoids re-investigating settled aspects. It flows through 6 touchpoints: state storage, packet preparation, prompt rendering, output schema, batch normalization/merge, and import. ### 1. Type Definition: `DimensionContext` **File: `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema_types_review.py`** Add a new TypedDict: ```python class DimensionContext(TypedDict, total=False): """Accumulated understanding for one review dimension across rounds.""" understanding: str # 2-5 sentence prose summary settled: list[str] # Investigated items confirmed intentional (max 10) created_at: str # ISO timestamp updated_at: str # ISO timestamp stable_rounds: int # Consecutive rounds with no updates ``` Add `"DimensionContext"` to the module `__all__`. **File: `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema_types.py`** Add import of `DimensionContext` from `schema_types_review` and re-export in `__all__`. **File: `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema_types.py` (StateModel)** Add to `StateModel`: ```python dimension_context: dict[str, DimensionContext] ``` This follows the same pattern as `subjective_assessments`, `concern_dismissals`, etc. -- optional dict keyed by dimension name. ### 2. Packet Preparation: Inject Context into Batches **File: `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_orchestration.py`** In `prepare_holistic_review_payload`, after building the payload dict (around line 185-211), extract dimension context from state and attach to the payload: ```python dimension_context = state.get("dimension_context", {}) if dimension_context: payload["dimension_context"] = dimension_context ``` This makes the context available to the batch prompt renderer. Each batch only needs context for its own dimensions, so filtering happens at prompt render time. ### 3. Prompt Rendering: New Section **File: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prompt_sections.py`** Add a new render function: ```python def render_dimension_context_block( dimensions: tuple[str, ...], dimension_context: dict[str, dict[str, object]], ) -> str: """Render accumulated dimension understanding for the reviewer.""" if not dimensions or not dimension_context: return "" relevant = { dim: ctx for dim, ctx in dimension_context.items() if dim in dimensions and isinstance(ctx, dict) } if not relevant: return "" lines: list[str] = [ "PRIOR UNDERSTANDING — starting knowledge from previous review rounds.", "Do not re-investigate settled items unless the code has clearly changed.", "If your review changes your understanding, report updates in context_updates.", "" ] for dim in dimensions: ctx = relevant.get(dim) if not ctx: continue lines.append(f"## {dim}") understanding = str(ctx.get("understanding", "")).strip() if understanding: lines.append(f"Understanding: {understanding}") settled = ctx.get("settled", []) if isinstance(settled, list) and settled: lines.append("Settled (confirmed intentional):") for item in settled[:10]: lines.append(f" - {item}") stable = ctx.get("stable_rounds", 0) if isinstance(stable, int) and stable > 0: lines.append(f"(stable for {stable} consecutive rounds)") lines.append("") return "\n".join(lines) + "\n" ``` Add to `__all__`. **File: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/prompt_template.py`** Import `render_dimension_context_block` […]

> AGENT

Now I see the plumbing. `render_batch_prompt` is called via `partial(render_batch_prompt, policy_block=policy_block)` in orchestrator.py line 157. Let me check how `prepare_run_artifacts` calls it.

> AGENT

Now I see the full chain. The `build_prompt_fn` is `partial(render_batch_prompt, policy_block=policy_block)` and it's called in `prepare_run_artifacts` (runner_packets.py:173) with `repo_root, packet_path, batch_index, batch`. The `dimension_context` is available in the packet (which is loaded at a higher level). The cleanest approach: include `dimension_context` in each batch dict during packet construction, OR pass it through the `build_prompt_fn` partial. **Simplest plumbing**: Since the packet already contains `dimension_context` at the top level, and batches are sub-dicts extracted from `packet["investigation_batches"]`, the simplest approach is to attach `dimension_context` to each batch dict in the packet during preparation. This way, `render_batch_prompt` can extract it from the `batch` dict directly without changing signatures. In `prepare_holistic_review_payload`, after setting `payload["dimension_context"]`, also loop through the investigation batches and attach the relevant context to each batch. Or even simpler: in `render_batch_prompt`, accept an optional `dimension_context` parameter passed through the partial. The cleanest approach (minimal signature changes): 1. In `orchestrator.py`, when creating the partial for `render_batch_prompt`, also bind `dimension_context`: ```python dim_context = packet.get("dimension_context", {}) build_prompt_fn=partial(render_batch_prompt, policy_block=policy_block, dimension_context=dim_context), ``` 2. Add `dimension_context: dict[str, dict[str, object]] | None = None` parameter to `render_batch_prompt`. This is the cleanest because it follows the existing pattern of binding `policy_block` via partial. ### 12. Testing Approach **Unit tests to add/modify:** 1. **`test_render_dimension_context_block`** - in the existing test file for prompt sections or batch core. Verify: - Empty context returns empty string - Only relevant dimensions are included - Settled items are capped at 10 - Stable rounds shown when > 0 2. **`test_store_context_updates`** - in `tests/intelligence/` or `tests/review/`. Verify: - New context created when none exists - `add_settled` appends, `remove_settled` removes - Settled cap at 10 - `stable_rounds` increments when no changes, resets on change - `understanding` null means no change - Invalid data gracefully ignored 3. **`test_normalize_batch_result_with_context_updates`** - verify context_updates pass through normalization 4. **`test_merge_batch_results_preserves_context_updates`** - verify merge collects context_updates from all batches 5. **`test_import_holistic_issues_with_context_updates`** - integration test that full import stores context in state 6. **`test_render_batch_prompt_includes_context`** - verify the prompt contains "PRIOR UNDERSTANDING" when context is provided 7. **`test_output_schema_includes_context_updates`** - verify the schema string contains `context_updates` 8. **Existing test compatibility** - `test_batch_prompt_requires_score_and_issue_consistency` in `test_review_batch_core_direct.py` should still pass since `dimension_context` defaults to None/empty. ### Implementation Order 1. **Type definition** (`schema_types_review.py`, `schema_types.py`) - foundation 2. **Import logic** (`assessments.py`, `holistic.py`) - write before read 3. **Prompt section** (`prompt_sections.py`) - render function 4. **Output schema** (`prompt_template.py`) - schema extension + prompt integration 5. **Batch normalization** (pass-through in `collect_batch_results`) 6. **Merge** (`merge.py`) - […]

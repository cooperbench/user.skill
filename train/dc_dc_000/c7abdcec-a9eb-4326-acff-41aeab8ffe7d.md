---
session_id: c7abdcec-a9eb-4326-acff-41aeab8ffe7d
developer: "dc:dc_000"
split: train
source: dataclaw
repo: peteromallet/my-dataclaw-data
start_time: "2026-03-04T04:09:54.492Z"
n_turns: 87
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

I need to understand why running `desloppify plan` auto-resolves the `workflow::create-plan` queue item in the desloppify tool. The tool is installed somewhere under the user's system (it's a Python CLI at /Users/user_c042661f/.pyenv/shims/desloppify). But the source code should be at /Users/user_c042661f/Documents/desloppify. I need to find: 1. The source code for the `desloppify plan` command 2. How `workflow::create-plan` queue items work 3. Why running `desloppify plan` would auto-resolve the `workflow::create-plan` step from the queue Be very thorough - search for "create-plan", "workflow::", "score-checkpoint", and the plan command handler. Look at both the CLI entry point and the plan/queue logic.

> AGENT

I'll help you understand how `desloppify plan` auto-resolves the `workflow::create-plan` queue item. Let me search the desloppify source code thoroughly.

> AGENT

Let me search for the main CLI entry point and the plan command:

> AGENT

Perfect! Let me read the main plan command entry point:

> AGENT

Excellent! I found it. Now let me check the `WORKFLOW_CREATE_PLAN_ID` constant and the `purge_ids` function to understand the mechanism:

> AGENT

Now let me check the definition of `WORKFLOW_CREATE_PLAN_ID` and how queue items are managed:

> AGENT

Good! Now let me check the `purge_ids` function to see how it removes items from the queue:

> AGENT

Perfect! Now let me check when the `create-plan` workflow item gets added to the queue in the first place:

> AGENT

Excellent! Now let me check where this sync function is called in the planning flow:

> AGENT

Now let me check where the planning generation function is that calls these sync functions:

> AGENT

Let me check where the queue is built and the plan gets generated - I need to see when the create-plan item is injected:

> AGENT

Now let me check the synthetic queue builder for create_plan_item:

> AGENT

Perfect! Now I have the full picture. Let me create a comprehensive summary document: ## Summary I've traced through the desloppify source code to understand how `desloppify plan` auto-resolves the `workflow::create-plan` queue item. Here's what I found: ### How `workflow::create-plan` Gets Added to the Queue The `workflow::create-plan` queue item is **synthetically injected** by the `sync_create_plan_needed()` function in `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/stale_dimensions.py` (lines 419-470). **Injection conditions** (all must be true): 1. No unscored subjective dimensions remain (initial reviews are complete) 2. At least one objective issue exists (backlog isn't empty) 3. Item isn't already in the queue 4. No triage stages are pending When these conditions are met, the item gets inserted after all subjective/triage/workflow items in the queue order. The purpose is to prompt the user to generate a fresh prioritized markdown plan after review assessment completes and objective issues exist. ### Why Running `desloppify plan` Auto-Resolves It The resolution mechanism is in `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/cmd.py` (lines 78-85): ```python def _cmd_plan_generate(args: argparse.Namespace) -> None: """Generate the prioritized markdown plan (existing behavior).""" # Auto-resolve the create-plan workflow item when plan runs plan = load_plan() if WORKFLOW_CREATE_PLAN_ID in plan.get("queue_order", []): purge_ids(plan, [WORKFLOW_CREATE_PLAN_ID]) save_plan(plan) cmd_plan_output(args) ``` **Key flow:** 1. When `desloppify plan` is invoked with no subcommand (line 178: `plan_action is None`), it calls `_cmd_plan_generate()` 2. This function loads the plan from disk 3. Checks if `"workflow::create-plan"` is in the `queue_order` list (line 82) 4. If present, calls `purge_ids(plan, [WORKFLOW_CREATE_PLAN_ID])` (line 83) 5. Saves the modified plan back to disk (line 84) 6. Then generates and displays the markdown plan (line 85) ### What `purge_ids()` Does The `purge_ids()` function in `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/operations_lifecycle.py` (lines 43-78): - Removes the ID from `queue_order` list - Removes it from the `skipped` dict if present - Removes it from all cluster memberships - Preserves any metadata/overrides for history ### Why This Design Pattern Works This is an elegant **auto-resolution pattern** where: 1. The presence of `workflow::create-plan` in the queue **signals** that the user should run `desloppify plan` 2. The queue item's `primary_command` is literally `"desloppify plan"` (line 217 in synthetic.py) 3. Running that command **automatically satisfies** the workflow step by removing the item 4. The plan output is then shown as the result The design exploits the fact that the action needed to resolve the step (`desloppify plan`) is the same command that naturally removes it from the queue. No explicit `resolve` subcommand is needed—the side effect of running the command itself is the […]

> DEVELOPER

I need to understand the overall desloppify workflow, specifically what the "create-plan" stage is supposed to accomplish and what the full lifecycle looks like. Look at /Users/user_c042661f/Documents/desloppify and explore: 1. The overall workflow/lifecycle - what stages exist, what order do they run in, what's the intended user journey from scan to completion? 2. What is the `workflow::create-plan` step actually supposed to prompt the user to DO? Look at the synthetic.py file where it's defined - what's the description, what guidance does it give? 3. What does `desloppify next` show when `workflow::create-plan` is the next item? What instructions/actions does it display to the user? 4. How does the score-checkpoint workflow item work in comparison? What does it require? 5. Look at the plan command's output - what does `cmd_plan_output` generate? Is the user supposed to use that output to make decisions? 6. Are there any docs, README, or comments explaining the intended workflow? Be very thorough - I want to understand the design intent, not just the mechanics.

> AGENT

I'll systematically explore the desloppify directory to understand the workflow, starting with the overall structure and then diving into the specific stages you mentioned.

> AGENT

Let me look at the directory structure more clearly:

> AGENT

Good, now let me look at the README and CLAUDE.md first to understand the high-level design:

> AGENT

Now let me find the synthetic.py file where workflows are defined:

> AGENT

Perfect. Let me read that file and explore the workflow structures:

> AGENT

Good. Now let me look at the workflow lifecycle and understand what happens when `desloppify next` is run. Let me find the "next" command implementation:

> AGENT

Let me read the next command implementation:

> AGENT

Now let me look at the plan command to understand what it outputs:

> AGENT

Now let me look at the planning module to understand how the plan is generated:

> AGENT

Now let me look at the actual render module to see what the plan generates:

> AGENT

Now let me look at the entire workflow structure and understand what stages exist. Let me check the stale_dimensions file:

> AGENT

Excellent! Now let me look at what happens when `desloppify next` is called to show the `create-plan` item. Let me check the render code:

> AGENT

Let me continue reading the render module and then look at the scoring checkpoint to compare:

> AGENT

Good. Now let me look at what the workflow items show when rendered. Let me check render_support.py to see if there are special messages:

> AGENT

Now let me look at the docs folder to understand the intended workflow design better:

> AGENT

Let me look at the SKILL.md to understand the intended user workflow:

> AGENT

Perfect! Now let me also check what happens in the queue building to understand how workflow items are inserted. Let me look at the queue building core:

> AGENT

Perfect! Now let me get a comprehensive picture by looking at the actual test that shows what `desloppify next` displays when `create-plan` is the next item. Let me check the test:

> AGENT

Now let me look for tests or code that specifically test what the create-plan workflow item shows. Let me search for it:

> AGENT

Perfect. Now let me look at the test to see what create-plan actually shows:

> AGENT

Let me search for test files that specifically test workflow items:

> AGENT

Perfect. Now I have comprehensive understanding. Let me create a comprehensive summary document. Based on all the code I've explored, I can now explain the desloppify workflow design: ## Desloppify Workflow: Complete Architecture Based on my thorough exploration of the codebase, here's the complete design of the desloppify workflow, including what `create-plan` is supposed to accomplish and the full lifecycle: ### **Overall Lifecycle (3-Phase Cycle)** The desloppify workflow is designed as a repeating cycle that agents execute: **Phase 1: Scan and Review (Understanding)** ``` desloppify scan --path . # Detect mechanical issues + get initial scores desloppify status # Check scores desloppify review --run-batches ... # (if prompted) Run subjective dimension reviews ``` **Phase 2: Plan (Strategy)** ``` desloppify next # See workflow items, including create-plan when ready desloppify plan triage --stage ... # Complete triage stages (observe → reflect → organize → commit) desloppify plan # Generate prioritized markdown plan desloppify plan reorder <pat> top # Reorder, cluster, skip items as desired ``` **Phase 3: Execute (Implementation)** ``` desloppify next # Show next item to fix [Fix code] desloppify plan resolve ... # Mark complete when done [Repeat until queue is empty] ``` **Then cycle back to Phase 1** — new issues surface, cascades resolve, priorities shift. --- ### **Workflow Stages and Synthetic Items** The queue doesn't just show "fix this issue" items. It also shows **workflow actions** — synthetic items that represent collaboration points. These are auto-injected based on state: #### **1. Triage Stages** (`triage::observe`, `triage::reflect`, `triage::organize`, `triage::commit`) **When injected:** - When new review issues appear (detected by hash of open review/concerns detectors) - Prevents the agent from starting code fixes without understanding the findings first **What they do:** - **observe**: Read the generated review issues and look for patterns - **reflect**: Compare against completed work; what has the agent actually improved? - **organize**: Summary of priorities; what should be fixed in what order? - **commit**: Write a comprehensive execution plan and strategy for fixing things **What user sees in `desloppify next`:** ``` (Planning stage: observe) ────────────────────────────────────────────────────── Triage: Observe and analyze findings 123 review issues to analyze Action: desloppify plan triage --stage observe ``` The stages have **dependencies** — you must complete `observe` before `reflect`, etc. When blocked, the item shows: ``` [blocked] Blocked by: observe Next step: desloppify plan triage --stage observe ``` #### **2. Score Checkpoint** (`workflow::score-checkpoint`) **When injected:** - After all initial (unscored/placeholder) subjective dimensions […]

> DEVELOPER

I need to understand the current state of the desloppify plan workflow and figure out how to fix the `workflow::create-plan` auto-resolution issue. The problem: Running `desloppify plan` auto-resolves `workflow::create-plan` from the queue, but it shouldn't - the user should have to explicitly go through the planning process (reordering, clustering, etc.) before the workflow step is considered done. Look at /Users/user_c042661f/Documents/desloppify and investigate: 1. In `desloppify/app/commands/plan/cmd.py`, read the `_cmd_plan_generate` function that does the auto-resolution (around lines 78-85). Understand exactly what it does. 2. Look at how `workflow::score-checkpoint` requires explicit resolution - what's the mechanism? How does `desloppify plan resolve` work? Can we make `workflow::create-plan` use the same pattern? 3. Look at the `desloppify next` rendering - when `workflow::create-plan` is the next item, what action does it tell the user to take? The action currently says "desloppify plan" - if we remove auto-resolution, what should the action say instead? 4. Look at `synthetic.py` where `build_create_plan_item` is defined - what fields does it set? Does it have a `primary_command`? 5. Look at how `desloppify plan resolve` works - could it be used to resolve `workflow::create-plan`? Or does the ID format cause issues? 6. Check if there are triage stages (observe/reflect/organize/commit) that are relevant here. How do those get resolved? Could `workflow::create-plan` use a similar pattern? The goal: understand what minimal change would make `workflow::create-plan` require explicit resolution (like running through triage or using `plan resolve`) instead of auto-resolving when `desloppify plan` is run. Be very thorough - read the actual source code for all relevant functions.

> AGENT

I'll conduct a thorough investigation of the desloppify plan workflow to understand the auto-resolution issue and how to fix it. Let me start by examining the key files.

> AGENT

Let me search for the relevant files:

> AGENT

Now let me read the key files:

> AGENT

Now let me look at the `next` command to see how it renders the create-plan item:

> AGENT

Let me check the next render module to see how items are displayed:

> AGENT

Now let me look at the plan resolve handlers to understand how it works:

> AGENT

Now let me look at how score-checkpoint resolution works to understand the pattern better:

> AGENT

Let me check stale_dimensions to understand the IDs better:

> AGENT

Now let me look at the triage handlers to understand how triage stages are resolved:

> AGENT

Let me search for how triage stages are marked as confirmed/done:

> AGENT

Perfect! Now let me look at how triage stages are cleared from the queue in completion:

> AGENT

Perfect! Now I have a comprehensive understanding. Let me create a summary document with my findings: ## Summary Report: Understanding the Desloppify Plan Workflow Auto-Resolution Issue I've completed a thorough investigation of the desloppify plan workflow, specifically the `workflow::create-plan` auto-resolution problem. Here are my detailed findings: ### 1. **How Auto-Resolution Currently Happens** **File:** `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/cmd.py` (lines 78-85) ```python def _cmd_plan_generate(args: argparse.Namespace) -> None: """Generate the prioritized markdown plan (existing behavior).""" # Auto-resolve the create-plan workflow item when plan runs plan = load_plan() if WORKFLOW_CREATE_PLAN_ID in plan.get("queue_order", []): purge_ids(plan, [WORKFLOW_CREATE_PLAN_ID]) save_plan(plan) cmd_plan_output(args) ``` **The Problem:** When `desloppify plan` is run (with no subcommand), it automatically removes `workflow::create-plan` from the queue via `purge_ids()`. This happens before even displaying the plan. The user doesn't go through any explicit action to resolve this workflow step. --- ### 2. **The Create-Plan Item Definition** **File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/synthetic.py` (lines 198-220) ```python def build_create_plan_item(plan: dict) -> WorkQueueItem | None: """Build a synthetic work item for ``workflow::create-plan`` if it's in the queue. Returns ``None`` when the item is not pending. """ from desloppify.engine._plan.stale_dimensions import WORKFLOW_CREATE_PLAN_ID if WORKFLOW_CREATE_PLAN_ID not in plan.get("queue_order", []): return None return { "id": WORKFLOW_CREATE_PLAN_ID, "tier": 1, "confidence": "high", "detector": "workflow", "file": ".", "kind": "workflow_action", "summary": "Create prioritized plan from review results", "detail": {}, "primary_command": "desloppify plan", # ← This is the issue! "blocked_by": [], "is_blocked": False, } ``` **Key Issue:** The `primary_command` is set to just `"desloppify plan"`, which triggers the auto-resolution. The item has no special mechanism to prevent this (unlike triage stages which have dependencies). --- ### 3. **How `workflow::score-checkpoint` Requires Explicit Resolution** **File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/synthetic.py` (lines 161-195) ```python def build_score_checkpoint_item(plan: dict, state: dict) -> WorkQueueItem | None: # ... return { "id": WORKFLOW_SCORE_CHECKPOINT_ID, "tier": 1, "confidence": "high", "detector": "workflow", "file": ".", "kind": "workflow_action", "summary": f"Score checkpoint: strict {strict:.1f}/100{delta_str}", "detail": { "strict": strict, "plan_start_strict": plan_start, "delta": delta, }, "primary_command": f'desloppify plan resolve "{WORKFLOW_SCORE_CHECKPOINT_ID}" --note "Reviewed score checkpoint" --confirm', "blocked_by": [], "is_blocked": False, } ``` **The Difference:** The `primary_command` is `desloppify plan resolve "workflow::score-checkpoint" ...`, which: 1. Calls `cmd_plan_resolve()` instead of `_cmd_plan_generate()` 2. Requires explicit user action 3. Validates dependencies and inputs 4. Manually purges the ID from the queue --- ### 4. **How `desloppify plan resolve` Works for Synthetic IDs** **File:** `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/override_handlers.py` (lines 474-571) The key pattern is in `cmd_plan_resolve()`: ```python def cmd_plan_resolve(args: argparse.Namespace) -> None: """Mark issues as fixed — delegates to cmd_resolve for rich UX.""" # ... # Handle synthetic IDs (triage::*, workflow::*, subjective::*) directly […]

> DEVELOPER

I need to understand the structural decomposition items in the desloppify queue for the reigh project at /Users/user_c042661f/Documents/reigh. Run this command to get the full queue details: ``` cd /Users/user_c042661f/Documents/reigh && desloppify plan queue --top 0 --verbose 2>&1 ``` Then look at the state file to understand the structural issues in detail. The state file is large, so search for structural issues: ``` grep -c "structural::" /Users/user_c042661f/Documents/reigh/.desloppify/state-typescript.json ``` Also search for the specific files flagged for decomposition - I need to understand which files are in the same areas/features so we can cluster related work: - What directories have multiple structural issues? - Which files are related (same feature/component)? - Which are the largest/most complex? Focus on understanding the structural items (items 1-63 in the queue) so we can group them intelligently.

> AGENT

I'll help you understand the structural decomposition items. Let me run these commands to gather the details.

> AGENT

Good - we have 132 structural issues. Let me try the correct command syntax and then examine the state file:

> DEVELOPER

I need to understand the 40 holistic review items in the desloppify queue for the reigh project at /Users/user_c042661f/Documents/reigh. Run: ``` cd /Users/user_c042661f/Documents/reigh && desloppify show review --status open 2>&1 ``` These are the subjective/architectural issues that are the biggest drag on the strict score (76.5 vs 98.1 objective). I need to understand: 1. Which issues are related to each other (e.g., multiple auth issues, multiple timeline issues) 2. Which ones could be fixed together 3. Which ones are the highest impact for score improvement 4. The 15 subjective dimensions below target — which review issues map to which dimensions Also check: ``` cd /Users/user_c042661f/Documents/reigh && desloppify show subjective 2>&1 ``` And look at the dimension scores to understand which subjective areas need the most work.

> AGENT

I'll help you understand the holistic review items and their relationship to the subjective dimensions. Let me run these commands to get the full picture.

> AGENT

Now let me search the state file to extract all structural issues and their file paths:

> AGENT

Now let me check the subjective dimensions breakdown:

> AGENT

Let me check the full review queue (not just open) to understand the complete landscape:

> AGENT

Let me extract the structural issues in a better way using grep with JSON parsing:

> DEVELOPER

I need to understand the mechanical cleanup items in the desloppify queue for the reigh project at /Users/user_c042661f/Documents/reigh. These are the batched/clustered items in the queue (items 64-116 roughly). Run: ``` cd /Users/user_c042661f/Documents/reigh && desloppify plan queue --top 0 2>&1 ``` Focus on understanding the mechanical items: - **Code smells batches**: async-no-await (35), high cyclomatic complexity (44), nested closures (48), monster functions (7), voided symbols (8), window globals (2), hardcoded URLs (2) - **Facade issues** (21 items) - **Flat dirs** (19 items) - **Signature variance** (17 items) - **Props/state/context** issues - **Import cycle** (1) - **Unused import** (1), **stray log** (1) - **Test coverage** (23 items) For the batched items, I need to understand: 1. Which are truly mechanical/autofix-able vs need human judgment 2. Which overlap with structural decomposition (e.g., a monster function in a file that also needs decomposition) 3. Quick wins vs effort-intensive items Also run: ``` cd /Users/user_c042661f/Documents/reigh && desloppify show smells 2>&1 | head -100 ``` to see what the smell issues look like in detail.

> AGENT

Let me check if there are hidden issues I can view:

> AGENT

I'll explore the desloppify queue to understand the mechanical cleanup items. Let me start by examining the plan and the smells in detail.

> AGENT

Let me check the plan and any desloppify data to understand the hidden issues:

> AGENT

Now let me analyze the directory structure and group these by area:

> AGENT

Let me read the full plan file to understand all the hidden issues:

> AGENT

Now let me examine the specific mechanical smell categories in more detail:

> AGENT

Let me search the plan file for the hidden review issues:

> AGENT

Let me try a different approach:

> AGENT

Let me try to get a list of all review issues differently:

> AGENT

Excellent! Now let me get more detail on the largest and most complex files:

> AGENT

Let me check the .desloppify directory for the review packet to understand the full list:

> AGENT

Let me look at the full smells output and also check specific files to understand the mechanical issues:

> AGENT

Let me read the review packet JSON to see all 40 issues:

> AGENT

Now let me check for the items I need to understand better - signatures, test coverage, and others:

> AGENT

Let me check the holistic packet:

> AGENT

Now let me check the patterns, cycles, and patterns:

> AGENT

Now let me look at the .desloppify directory to understand the state and findings:

> AGENT

Let me look at specific files to understand actual instances of the mechanical issues:

> AGENT

Perfect! Now let me create a detailed breakdown showing the clusters and related files:

> AGENT

Now let me look at some of the monster functions and understand them better:

> AGENT

Let me try a different approach - check the plan file in segments:

> AGENT

Let me examine the review findings to get a sense of the higher-level issues:

> AGENT

Perfect! Now let me get the rest of the 40 issues:

> AGENT

Let me fix that script:

> AGENT

Perfect! Now let me create one final summary document with strategic recommendations:

> AGENT

Excellent! Now I have the full picture. Let me create a comprehensive analysis summary for you. ## Holistic Review Issues Analysis Based on the desloppify queue, here's the complete breakdown of the 40 holistic review items (the subjective issues driving the 76.5/100 strict score): ### Mapping to Subjective Dimensions (15 below 95% target) | Dimension | Score | Count | Key Issues | |-----------|-------|-------|-----------| | **Cross-module arch** | 44.0% | 4 | Error runtime hub, import cycles, client boundary erosion, dynamic imports as workarounds | | **Design coherence** | 46.9% | 6 | Clip manager async races, fragmented auth, home auth mixed concerns, upload feedback decoupling, lightbox overaggregation, supabase types god module | | **API coherence** | 48.5% | 2 | Generation-task cache key split, task cache scope mismatch | | **Init coupling** | 50.4% | 3 | Join clips localStorage queue, stale user cache on signout, realtime module singleton side effects | | **Stale migration** | 56.3% | 2 | Dual structure-video contracts, legacy default config leaks | | **Error consistency** | 58.2% | 2 | Optimistic update failures swallowed, task details errors collapsed to empty state | | **Test strategy** | 59.3% | 2 | Task invalidation tests vs stub, untested task-type fetch boundary | | **Structure nav** | 60.2% | 2 | shared/lib catchall, shared/hooks mixed domain/UI | | **Abstraction fit** | 62.2% | 2 | Referral finalization duplicated logic, Supabase access contract fragmented | | **Dep health** | 72.3% | 1 | Image preloading hard-coupled to realtime status | | **Auth consistency** | 70.5% | 1 | Resource owner enumeration on update | | **Contracts** | 74.5% | 1 | Resource listing silent truncation at 20k | | **Convention drift** | 74.3% | 1 | HuggingFace key flow mixed error protocols | | **AI generated debt** | 73.1% | 1 | Timeline/video hook commentary-to-logic ratio | | **Elegance (High/Mid/Low)** | 58.2% | 3 | MediaLightbox subsystem overload, project context dual API, oversized param bags, timeline god hook, lightbox boundary shape drift, task details dual presenter | --- ### Issue Groupings (Related & Combinable) **Group 1: Supabase Access Patterns (3 issues)** - Supabase access abstraction fragmented (throw-first repos vs result-checked hooks) - Supabase client boundary erosion (consumed directly across layers) - Could fix together by establishing a unified abstraction layer **Group 2: Task & Generation Cache/Mapping (2 issues)** - Generation-task mapping key split (incompatible public contracts) - […]

> AGENT

Not logged in · Please run /login

> AGENT

Perfect! Now I have a comprehensive understanding of the desloppify queue. Let me create a detailed analysis document: ## Summary: Desloppify Queue Mechanical Cleanup Analysis (Items 64-116) Based on my thorough examination of the queue, here's a breakdown of the mechanical/clustered cleanup items: --- ### **QUICK MECHANICAL WINS (Autofix-capable)** **1. Hardcoded URLs (2 items) - Item 69** - **Location**: `src/app/components/SocialIcons.tsx` (lines 11, 19) - **Issue**: GitHub and Discord URLs hardcoded in component - **Effort**: Minimal | **Automatable**: Yes - **Note**: These are static URLs unlikely to change; extracting to constants/env is straightforward - **Quick Fix**: Create `src/app/constants/socialLinks.ts` **2. Stray Debug Log (1 item) - Item 66** - **Location**: `src/shared/hooks/invalidation/useGenerationInvalidation.ts` (line 39) - **Detector**: `console.log('[Invalidation]')` - development-only instrumentation - **Effort**: Trivial | **Automatable**: Yes - **Fix Type**: Remove or wrap in `if (import.meta.env.DEV)` **3. Unused React Import (1 item) - Item 67** - **Location**: Not shown in output, but detector indicates orphaned React import - **Effort**: Trivial | **Automatable**: Yes - **Fix Type**: Remove unused `React` named import (common with newer JSX transform) --- ### **NESTED CLOSURES (48 items) - Item 71** - **Detector Tier**: High confidence, all T3 (low severity) - **Examples**: - `src/app/bootstrap.tsx` line 55: `.then(({ initializeSupabaseDebugGlobals }) => { ... })` - `src/app/hooks/useAppDndOverlay.tsx` line 16: Similar pattern in event handlers - **Root Cause**: Promise chains and event handlers with inline arrow functions - **Effort per Item**: 5-15 min | **Automatable**: Partially - Extract callback to module-level or `useCallback` - Can be batched by file - **Concern**: 48 items across the codebase suggests a style guideline inconsistency - **Recommendation**: Establish linting rule + bulk fix (eslint-plugin-etc has `no-nested-closures`) --- ### **MONSTER FUNCTIONS (7 items) - Item 74** - **Detector Tier**: Medium confidence (T2) - **Identified instances** (from show smells): 1. `src/shared/components/GenerationsPane/GenerationsPane.tsx` (175+ LOC component) 2. `src/shared/components/GenerationsPane/hooks/useGenerationsPaneController.ts` (281 LOC hook) 3. `src/shared/components/MediaLightbox/hooks/useLightboxVideoMode.ts` (150+ LOC) 4. `src/shared/hooks/tasks/useTaskStatusCounts.ts` (80+ shown, likely 150+ total) 5. `src/shared/lib/media/videoUploader.ts` (150+ LOC) 6. `src/tools/travel-between-images/components/ShotImagesEditor/hooks/useShotImagesEditorCallbacks.ts` (150+ LOC) 7. `src/tools/travel-between-images/components/Timeline/hooks/timeline-core/useTimelineViewportController.ts` (150+ LOC) - **Effort per Item**: 2-4 hours - **Challenge**: Overlap with structural decomposition - `GenerationsPane.tsx` (item 3 in structural list) needs decomposition anyway - `useGenerationsPaneController` is a dependency of #3 - `useLightboxVideoMode` is part of MediaLightbox (a monster component cluster) - **Recommendation**: **Defer until structural decomposition completed** — fixing monster functions without addressing the component structure creates false progress --- ### **ASYNC-NO-AWAIT (35 items) - Item 68** - **Detector Tier**: High confidence (T3) - **Pattern**: Floating promises; `().then(...)` […]

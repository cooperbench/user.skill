> DEVELOPER

I need to understand how desloppify's review batch system creates batches. The user ran `review --prepare` which produced 9 "investigation batches", then `--dry-run` expanded those into 46 prompt files. The user expected one batch per dimension. Search the codebase for: 1. How batches are created/split in the review batch system — look in `desloppify/app/commands/review/batch/` 2. How dimensions map to batches — is there grouping logic that combines dimensions? 3. What causes sub-batch splitting (the 9 → 46 expansion) 4. The "Full Codebase Sweep" batch type specifically — why would there be 20 of those? Focus on files in: - `desloppify/app/commands/review/batch/` - `desloppify/app/commands/review/prepare.py` - Any dimension/scope related files Report back the key functions and logic that control batch creation and splitting.

> AGENT

I'll search the codebase to understand how the review batch system creates and splits batches. Let me start by exploring the key files you mentioned.

> AGENT

Let me use bash to list the directory structure:

> AGENT

Good! Now let me read the key files. I'll start with the core batch files and prepare.py:

> AGENT

Now let me look at the execution file and the intelligence review module to understand where batches are created:

> AGENT

Good! The key files are in the intelligence module. Let me read those:

> AGENT

Now I need to find where the "Full Codebase Sweep" batch is created and understand the sub-batch splitting logic:

> AGENT

Let me read the helpers file:

> AGENT

Now let me search for where the 9 batches get expanded to 46 prompt files. This is likely in the execution or prompt generation logic:

> AGENT

Perfect! Now let me read the prompt_sections file to understand the explode logic:

> AGENT

Excellent! Now let me check how this explode function is used in the batch execution:

> AGENT

Let me find where explode_to_single_dimension is called in the execution flow:

> AGENT

Perfect! Now I have a complete picture. Let me verify by checking one more time how the external flow does it:

> AGENT

Perfect! Now I have all the information I need. Let me create a comprehensive summary: ## Summary: Review Batch System Architecture & Splitting Logic I've traced the complete batch creation and splitting flow in desloppify. Here's what I found: ### 1. **Batch Creation (9 batches in `--prepare` output)** The **9 investigation batches** are created by `build_investigation_batches()` in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_batches.py` (lines 491-516): 1. **Architecture & Coupling** - `_batch_arch_coupling()` 2. **Conventions & Errors** - `_batch_conventions_errors()` 3. **Abstractions & Dependencies** - `_batch_abstractions_deps()` 4. **Testing & API** - `_batch_testing_api()` 5. **Authorization** - `_batch_authorization()` 6. **AI Debt & Migrations** - `_batch_ai_debt_migrations()` 7. **Package Organization** - `_batch_package_organization()` 8. **State & Design Integrity** - `_batch_state_design()` 9. **Governance & Contracts** - `_batch_governance_contracts()` Each batch is **hardcoded** to cover **multiple dimensions**. For example: - Batch 1 (Architecture & Coupling) covers `["cross_module_architecture", "high_level_elegance"]` - Batch 3 (Abstractions & Dependencies) covers `["abstraction_fitness", "dependency_health", "mid_level_elegance", "low_level_elegance"]` **Key point**: Batches are NOT one-per-dimension. They group dimensions thematically by code concern area. ### 2. **Sub-batch Splitting (9 → 46 expansion)** The **9 → 46 expansion** happens through `explode_to_single_dimension()` in `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prompt_sections.py` (lines 246-271): ```python def explode_to_single_dimension( batches: list[dict[str, object]], dimension_prompts: dict[str, dict[str, object]] | None = None, ) -> list[dict[str, object]]: """Split multi-dimension batches into one batch per dimension.""" result: list[dict[str, object]] = [] for batch in batches: dims = batch.get("dimensions", []) for dim in dims: exploded: dict[str, object] = {**batch, "dimensions": [dim]} # ... add dimension_prompt if available result.append(exploded) return result ``` **This function is called twice** (both with identical logic): 1. In batch execution: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py` line 452 2. In external flow: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/external.py` line 230 **How it works**: For each input batch with N dimensions, it creates N exploded batches (one per dimension), each keeping the same seed files but scoped to a single dimension. **Example**: A batch with `["abstraction_fitness", "dependency_health", "mid_level_elegance", "low_level_elegance"]` becomes 4 separate prompt files. ### 3. **"Full Codebase Sweep" Batch Creation (the 20 you saw)** The **"Full Codebase Sweep"** is created by `append_full_sweep_batch()` in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py` (lines 23-52): ```python def append_full_sweep_batch( *, batches: list[dict[str, Any]], dims: list[str], all_files: list[str], lang: Any, max_files: int | None = None, ) -> None: """Append an optional cross-cutting full-codebase batch.""" if not dims: return all_rel_files: list[str] = [] for filepath in all_files: if lang.zone_map is not None: zone = lang.zone_map.get(filepath) if zone.value in ("test", "generated", "vendor"): continue all_rel_files.append(rel(filepath)) if isinstance(max_files, int) and max_files > 0 and len(all_rel_files) >= max_files: break if not all_rel_files: return batches.append({ "name": […]

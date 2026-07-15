> DEVELOPER

I need to understand the T1-T4 tier-based queue ordering system in this codebase. The user wants to remove tier as a hard queue-order control. Key areas to investigate: 1. Any `ranking.py` files - especially lines around L91, L105, L134 that sort by tier 2. `desloppify/engine/_work_queue/core.py` - especially around L417 for tier filtering 3. `desloppify/engine/_work_queue/helpers.py` - around L248 for subjective queue generation 4. Any other files in `desloppify/engine/_work_queue/` that reference tier-based sorting For each file, read the relevant sections and provide the full context of how tiers affect queue ordering. I need to understand what code enforces "T1 before T2 before T3" ordering and "subjective forced behind mechanical".

> AGENT

I'll investigate the tier-based queue ordering system across these key files in parallel.

> AGENT

Now let me also check for any other files that reference tier-based sorting or filtering — particularly the plan and state filtering files mentioned in the git status:

> AGENT

Now I have a thorough picture of all the tier enforcement points. Here is a complete analysis: --- ## Tier-Based Queue Ordering: Where and How It Is Enforced There are four distinct mechanisms that together enforce "T1 before T2 before T3, and subjective forced to T4": --- ### 1. `effective_tier` assignment — `ranking.py` lines 54–57 **File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py` ```python # Lines 54–57 in build_finding_items() item["effective_tier"] = ( 4 if item["is_subjective"] else int(finding.get("tier", 3)) ) ``` This is where subjective findings get **forcibly promoted to T4**, regardless of whatever `tier` is stored on the finding. Non-subjective items use the stored `tier` value. Additionally, in `helpers.py` lines 337–338, all synthetic subjective dimension items are always hard-coded with: ```python # helpers.py lines 337–338 in build_subjective_items() "tier": 4, "effective_tier": 4, ``` --- ### 2. Primary sort key — `ranking.py` `item_sort_key()` lines 86–122 **File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py` This is the central sorting function applied at `core.py` line 373 (`all_items.sort(key=item_sort_key)`). The tier is the **first element** of every sort tuple, making it the primary and dominant ordering control: ```python # Lines 86–122 — item_sort_key() def item_sort_key(item: dict) -> tuple: if item.get("kind") == "synthesis_needed": # Synthesis items always sort first — they block all other work. return (-1, 0, 0, item.get("id", "")) if item.get("kind") == "cluster": # Clusters sort before individual findings (priority bucket 0) return (0, action_pri, -member_count, item.get("id", "")) if item.get("kind") == "subjective_dimension" or item.get("is_subjective"): return ( int(item.get("effective_tier", 4)), # always 4 1, # secondary: subjective after mechanical within T4 subjective_score_value(item), item.get("id", ""), ) # Mechanical findings return ( int(item.get("effective_tier", item.get("tier", 3))), # T1 < T2 < T3 < T4 0, CONFIDENCE_ORDER.get(item.get("confidence", "low"), 9), -review_weight, -count, item.get("id", ""), ) ``` The ordering enforced here: - **synthesis_needed** items: bucket `-1` (always first) - **clusters**: bucket `0` (before individual findings) - **mechanical findings**: primary key is `effective_tier` (T1 < T2 < T3) - **subjective findings**: always bucket `4`, with secondary key `1` so they sort *after* mechanical items that happen to be T4 Within mechanical findings, secondary keys are: `confidence` rank, then `review_weight` desc, then `count` desc, then `id`. --- ### 3. Tier filtering — `core.py` lines 417–437 **File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py` ```python # Lines 417–437 — tier filter in build_work_queue() if requested_tier is not None: filtered = [ item for item in all_items if _item_matches_tier(item, requested_tier) ] if not filtered and not resolved_options.no_tier_fallback: chosen = choose_fallback_tier(requested_tier, counts) if chosen is not None: selected_tier = chosen filtered = [ item for item […]

> DEVELOPER

Search the entire desloppify codebase very thoroughly for ALL references to tier-based queue ordering. I need to find every place that: 1. References `effective_tier` (field name, variable, dict key) 2. References `tier` as a queue ordering concept (not the data field on findings themselves - those can stay as metadata) 3. References `tier_counts` or `available_tiers` or `selected_tier` or `requested_tier` or `fallback_tier` 4. References `--tier` CLI argument 5. References `no_tier_fallback` 6. References `choose_fallback_tier` 7. References `_item_matches_tier` 8. Text/strings mentioning "T1", "T2", "T3", "T4" in the context of queue ordering or priority 9. References to "tier asc" or "tier fixed" in ranking factor strings 10. The `group == "tier"` branch in `group_queue_items` 11. Any test files that test tier-based behavior Search in: - All .py files under desloppify/ - All test files - CLI parser files (parser_groups*.py) - Command files (next.py, show/, status/, plan/) - Rendering/output files For each match, provide the file path, line number, and the relevant code snippet with a few lines of context. Be very thorough - check templates, help strings, docstrings, comments, everything.

> AGENT

I'll conduct a thorough search across the entire codebase for all tier-based queue ordering references. Let me run many searches in parallel.

> AGENT

Good, the initial searches returned lots of data including worktree copies. Let me now focus specifically on the `desloppify/` directory (excluding `.claude/worktrees/`) and run the remaining searches.

> AGENT

Good. Now let me read the key files in full to get complete context, and also search for the remaining patterns.

> AGENT

Let me now get the remaining files I need to fully document -- the status/show/plan command files and test files.

> AGENT

Now let me search for tier references in the test files and remaining areas.

> AGENT

Let me also check the remaining key files for tier references in queue-ordering context.

> AGENT

Now let me check the remaining areas -- the `engine/work_queue.py` facade, `engine/plan.py`, and search for any CLI parser `--group` choices that include "tier".

> AGENT

Let me also check the remaining test files that reference "tier" in a queue-ordering context, and the `helpers/display.py` new file.

> AGENT

Let me check the remaining test files that were flagged.

> AGENT

Let me check the last few files I need for completeness -- the `TIER_LABELS` constant and the `_state/schema.py` `TierStats`.

> AGENT

Now I have a comprehensive picture. Let me compile the complete report. --- Here is the exhaustive inventory of all tier-based queue ordering references in the `desloppify/` source tree (excluding `.claude/worktrees/` copies). I have organized the results by category. --- ## 1. `effective_tier` (field name, variable, dict key) ### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py` **Line 55-57** -- Set on every finding item during `build_finding_items()`: ```python item["effective_tier"] = ( 4 if item["is_subjective"] else int(finding.get("tier", 3)) ) ``` **Line 107** -- Used in `item_sort_key()` for subjective items: ```python int(item.get("effective_tier", 4)), ``` **Line 116** -- Used in `item_sort_key()` for non-subjective items: ```python int(item.get("effective_tier", item.get("tier", 3))), ``` **Line 126** -- Local variable in `item_explain()`: ```python effective_tier = int(item.get("effective_tier", item.get("tier", 3))) ``` **Line 131** -- Returned in the explain dict for subjective_dimension items: ```python "effective_tier": effective_tier, ``` **Line 159** -- Returned in the explain dict for regular findings: ```python "effective_tier": effective_tier, ``` **Line 183** -- In `tier_counts()` for cluster members: ```python tier = int(member.get("effective_tier", member.get("tier", 3))) ``` **Line 186** -- In `tier_counts()` for non-cluster items: ```python tier = int(item.get("effective_tier", item.get("tier", 3))) ``` **Line 207** -- In `group_queue_items()` for `group == "tier"` branch: ```python key = f"T{int(item.get('effective_tier', item.get('tier', 3)))}" ``` ### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py` **Line 215** -- In `_item_matches_tier()` for cluster members: ```python int(m.get("effective_tier", m.get("tier", 3))) == tier ``` **Line 218** -- In `_item_matches_tier()` for non-cluster items: ```python return int(item.get("effective_tier", item.get("tier", 3))) == tier ``` ### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py` **Line 337** -- In `build_subjective_items()` synthetic item construction: ```python "effective_tier": 4, ``` ### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py` **Line 73** -- In `_render_grouped_items()`: ```python tier = int(item.get("effective_tier", item.get("tier", 3))) ``` **Line 183** -- In single-item render: ```python tier = int(item.get("effective_tier", item.get("tier", 3))) ``` **Line 416** -- In `_render_compact_item()`: ```python tier = int(item.get("effective_tier", item.get("tier", 3))) ``` ### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/output.py` **Line 35** -- In `serialize_item()`: ```python "effective_tier": item.get("effective_tier", item.get("tier")), ``` **Line 127** -- In `format_md_table()`: ```python tier = int(item.get("effective_tier", item.get("tier", 3))) ``` ### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py` **Line 26** -- In `_cluster_tier_label()`: ```python tiers = {int(m.get("effective_tier", m.get("tier", 3))) for m in members} ``` **Line 130** -- In queue table row building: ```python tier_val = int(item.get("effective_tier", item.get("tier", 3))) ``` ### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py` **Line 205** -- In `_plan_tier_sections()`: ```python tier = int(item.get("effective_tier", item.get("tier", 3))) ``` **Line 435** -- In `_render_plan_item()`: ```python tier = int(item.get("effective_tier", item.get("tier", 3))) ``` --- ## 2. `tier_counts` (function and dict key) ### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py` **Line 177-188** -- Function definition: ```python def tier_counts(items: list[dict]) -> dict[int, int]: counts = {1: 0, 2: 0, 3: 0, 4: 0} for item in items: if item.get("kind") == "cluster": for […]

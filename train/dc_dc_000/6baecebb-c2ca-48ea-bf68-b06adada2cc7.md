> DEVELOPER

I need to understand the current issue/finding semantics in this codebase to review a redesign plan. Please find and summarize: 1. The current Issue/Finding type definitions (likely in state.py or schema files) 2. How NON_OBJECTIVE_DETECTORS is defined and used 3. How detector strings like "review", "concerns", "subjective_review" are used as semantic switches throughout the code 4. How ID prefixes (like "review::", "concerns::") are used for semantic inference 5. The current subjective_assessments storage 6. How the queue/work queue currently classifies items 7. The current concern generation and persistence model Be thorough - check engine/, app/, and intelligence/ directories. I need to understand the scattered heuristics the plan aims to replace.

> AGENT

I'll conduct a thorough exploration of the issue/finding semantics and related infrastructure across the codebase. Let me start with multiple parallel searches.

> AGENT

Let me search for Finding type definition and NON_OBJECTIVE_DETECTORS more broadly:

> AGENT

Now let me read the key files to understand the semantics:

> AGENT

Now let me search for the state_compat module and understanding of Finding type:

> AGENT

Now let me search for concerns-related code and ID prefixes:

> AGENT

Now let me look at the work queue types and how items are classified:

> AGENT

Now let me search for how concerns and subjective_assessment issues are generated:

> AGENT

Now let me search for how review and concerns issues are generated and managed:

> AGENT

Let me search for where review and concerns issues are created/inserted:

> AGENT

Now let me check how concerns get converted to issues and stored:

> AGENT

Perfect! Now let me search for how the "review" detector issues are created and the actual ID format:

> AGENT

Excellent. Now let me search for actual issue ID formats and prefix usage:

> AGENT

Perfect! Let me now check the per_file issue generation to understand file-scoped review issues:

> AGENT

Now let me check how narrative and action engine use these detector strings:

> AGENT

Now let me check how make_issue constructs IDs:

> AGENT

Perfect! Now let me gather a comprehensive summary. Let me check a few more details about the queue and how items are marked:

> AGENT

Perfect! I now have a comprehensive understanding. Let me create a detailed summary document. ## Summary: Current Issue/Finding Semantics and Scattered Heuristics Based on my thorough exploration of the codebase, here's a comprehensive breakdown of the current issue/finding semantics, detector classifications, and the scattered heuristics the plan aims to consolidate: ### 1. **Issue/Finding Type Definitions** **Core Issue TypedDict** (`desloppify/engine/_state/schema_types_issues.py`): - **`Issue`** – Central TypedDict with fields: `id`, `detector`, `file`, `tier`, `confidence`, `summary`, `detail` (dict), `status`, `note`, `first_seen`, `last_seen`, `resolved_at`, `reopen_count`, `suppressed`, `lang`, `zone` - Issue IDs use a stable format: `{detector}::{file}::{name}` (constructed in `make_issue()`) - Example: `review::src/foo.ts::high_elegance::abc12345` - Example: `concern::src/foo.ts::design::id123` - Example: `subjective::mid_elegance` (synthetic dimension item) **Assessment TypedDicts** (`desloppify/engine/_state/schema_types_review.py`): - **`SubjectiveAssessment`** – Stores dimension scores with: `score`, `source`, `assessed_at`, `reset_by`, `placeholder`, `components`, `component_scores`, `integrity_penalty`, `provisional_override`, `stale_since`, `judgment` (narrative breakdown) - **`SubjectiveIntegrity`** – Anti-gaming metadata: `status`, `target_score`, `matched_count`, `matched_dimensions`, `reset_dimensions` - **`ConcernDismissal`** – Dismissed concern record: `dismissed_at`, `reason`, `dimension`, `reasoning`, `concern_type`, `concern_file`, `source_issue_ids` **Concern Dataclass** (`desloppify/engine/_concerns/types.py`): - **`Concern`** – Immutable dataclass with: `type` (e.g., "systemic_pattern", "systemic_smell"), `file`, `summary`, `evidence` (tuple), `question`, `fingerprint`, `source_issues` (tuple of issue IDs) --- ### 2. **NON_OBJECTIVE_DETECTORS Definition and Usage** **Single Source of Truth**: `desloppify/engine/_plan/policy/subjective.py` line 21-23: ```python NON_OBJECTIVE_DETECTORS: frozenset[str] = frozenset({ "review", "concerns", "subjective_review", "subjective_assessment", }) ``` **Also defined (separately)** in `desloppify/engine/_scoring/policy/core.py` line 43-53 as `_NON_OBJECTIVE_DETECTORS`: ```python _NON_OBJECTIVE_DETECTORS = frozenset({ "concerns", "review", "subjective_review", "uncalled_functions", "unused_enums", "signature", "stale_wontfix", }) # Note: wider set, includes some mechanical detectors ``` **Scattered Usage**: - **Queue filtering** (`engine/_work_queue/snapshot.py` lines 90-95): Excludes non-objective items from `_is_objective_item()` check - **Scoring** (`engine/_scoring/policy/core.py` line 69): Non-objective detectors get `dimension=None, tier=None` - **Subjective visibility** (`engine/_plan/policy/subjective.py` line 121): Used in `compute_subjective_visibility()` to count only objective items for backlog blocking **Semantic Switch Pattern**: Detector strings are hardcoded in multiple places as semantic switches rather than being looked up from a unified configuration. --- ### 3. **Detector Strings as Semantic Switches Throughout Codebase** **Critical Semantic Switches**: | Detector | Semantic Role | Files Using It | |----------|---------------|-----------------| | **"review"** | Per-file or holistic code review findings (non-mechanical) | `intelligence/review/importing/holistic_issue_flow.py`, `app/commands/review/`, `intelligence/narrative/` | | **"concerns"** | Design concerns surfaced by mechanical signals (e.g., systemic patterns, file-level aggregations) | `engine/_concerns/generators.py`, `intelligence/review/importing/` | | **"subjective_review"** | Legacy/alternate name for subjective dimension review items | `engine/_plan/policy/subjective.py`, `intelligence/narrative/action_engine_routing.py` | | **"subjective_assessment"** | Synthetic dimension items injected into queue when below target | `engine/_work_queue/synthetic.py` line 254 | | **"smells", "structural", "coupling"**, etc. | Mechanical (objective) detectors | Used in dimension scoring | **Hardcoded Semantic Checks**: […]

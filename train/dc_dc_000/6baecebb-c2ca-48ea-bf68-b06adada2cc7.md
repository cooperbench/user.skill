> DEVELOPER

I need to understand the current issue/finding semantics in this codebase to review a redesign plan. Please find and summarize:

1. The current Issue/Finding type definitions (likely in state.py or schema files)
2. How NON_OBJECTIVE_DETECTORS is defined and used
3. How detector strings like "review", "concerns", "subjective_review" are used as semantic switches throughout the code
4. How ID prefixes (like "review::", "concerns::") are used for semantic inference
5. The current subjective_assessments storage
6. How the queue/work queue currently classifies items
7. The current concern generation and persistence model

Be thorough - check engine/, app/, and intelligence/ directories. I need to understand the scattered heuristics the plan aims to replace.

> AGENT

I'll conduct a thorough exploration of the issue/finding semantics and related infrastructure across the codebase. Let me start with multiple parallel searches.

> TOOL

tool_use Glob
```json
{
  "pattern": "**/state.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/state.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/state.py
/Users/user_c042661f/Documents/desloppify/desloppify/languages/_framework/registry/state.py
/Users/user_c042661f/Documents/desloppify/desloppify/state.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/schema/**/*.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/schema/helpers.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/schema/migrations.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/schema/normalize.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/schema/version_upgrades.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/schema/__init__.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "NON_OBJECTIVE_DETECTORS|OBJECTIVE_DETECTORS",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 7 files
desloppify/engine/_plan/policy/subjective.py
desloppify/engine/_work_queue/snapshot.py
desloppify/tests/review/review_coverage_cases.py
desloppify/engine/_scoring/policy/core.py
desloppify/engine/_plan/sync/context.py
desloppify/tests/scoring/test_scoring_subjective_and_display.py
desloppify/tests/plan/test_subjective_policy.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "Finding.*=.*TypedDict|class Finding",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
No files found
```

> AGENT

Let me search for Finding type definition and NON_OBJECTIVE_DETECTORS more broadly:

> TOOL

tool_use Grep
```json
{
  "pattern": "class Finding|Finding.*TypedDict|\\\"Finding\\\"",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
No files found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "NON_OBJECTIVE",
  "type": "python",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
desloppify/engine/_work_queue/snapshot.py:14:from desloppify.engine._plan.policy.subjective import NON_OBJECTIVE_DETECTORS
desloppify/engine/_work_queue/snapshot.py:93:        and item.get("detector", "") not in NON_OBJECTIVE_DETECTORS
desloppify/engine/_work_queue/snapshot.py:367:            and item.get("detector", "") not in NON_OBJECTIVE_DETECTORS
desloppify/tests/plan/test_subjective_policy.py:255:    assert not hasattr(sync_mod, "NON_OBJECTIVE_DETECTORS")
desloppify/tests/scoring/test_scoring_subjective_and_display.py:308:        from desloppify.engine._scoring.policy.core import _NON_OBJECTIVE_DETECTORS
desloppify/tests/scoring/test_scoring_subjective_and_display.py:309:        assert "subjective_review" in _NON_OBJECTIVE_DETECTORS
desloppify/tests/review/review_coverage_cases.py:15:    _NON_OBJECTIVE_DETECTORS,
desloppify/tests/review/review_coverage_cases.py:505:        assert "subjective_review" in _NON_OBJECTIVE_DETECTORS
desloppify/engine/_plan/policy/subjective.py:21:NON_OBJECTIVE_DETECTORS: frozenset[str] = frozenset({
desloppify/engine/_plan/policy/subjective.py:121:        and issue.get("detector") not in NON_OBJECTIVE_DETECTORS
desloppify/engine/_plan/policy/subjective.py:146:    "NON_OBJECTIVE_DETECTORS",
desloppify/engine/_plan/sync/context.py:17:    NON_OBJECTIVE_DETECTORS as _NON_OBJECTIVE_DETECTORS,
desloppify/engine/_plan/sync/context.py:46:        and f.get("detector") not in _NON_OBJECTIVE_DETECTORS
desloppify/engine/_scoring/policy/core.py:43:_NON_OBJECTIVE_DETECTORS = frozenset(
desloppify/engine/_scoring/policy/core.py:69:        if detector in _NON_OBJECTIVE_DETECTORS:
```

> AGENT

Now let me read the key files to understand the semantics:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/state.py"
}
```

> TOOL

tool_result Read
```
1→"""Legacy `desloppify.state` wrapper.
     2→
     3→Prefer `desloppify.state_compat` or narrower modules in new code. This file
     4→remains only to preserve the long-standing import path.
     5→"""
     6→
     7→from desloppify.state_compat import *  # noqa: F403
     8→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/policy/subjective.py"
}
```

> TOOL

tool_result Read
```
1→"""Unified subjective-visibility policy.
     2→
     3→A single frozen dataclass computed once per operation replaces the scattered
     4→``has_objective_items`` / ``objective_count`` computations in
     5→``stale_dimensions`` and ``auto_cluster``.
     6→"""
     7→
     8→from __future__ import annotations
     9→
    10→from dataclasses import dataclass
    11→
    12→from desloppify.base.config import DEFAULT_TARGET_STRICT_SCORE
    13→from desloppify.base.enums import Status
    14→from desloppify.base.registry import DETECTORS
    15→from desloppify.engine._plan.schema import executable_objective_ids as _executable_objective_ids
    16→from desloppify.engine._state.filtering import issue_in_scan_scope
    17→from desloppify.engine._state.schema import StateModel
    18→from desloppify.engine.planning.helpers import CONFIDENCE_ORDER
    19→
    20→# Detectors whose issues are NOT objective mechanical work.
    21→NON_OBJECTIVE_DETECTORS: frozenset[str] = frozenset({
    22→    "review", "concerns", "subjective_review", "subjective_assessment",
    23→})
    24→
    25→
    26→@dataclass(frozen=True)
    27→class SubjectiveVisibility:
    28→    """Immutable snapshot of the subjective-vs-objective balance."""
    29→
    30→    has_objective_backlog: bool  # any planned open non-subjective issues?
    31→    objective_count: int  # how many (planned only, post-triage)
    32→    unscored_ids: frozenset[str]  # subjective::* IDs needing initial review
    33→    stale_ids: frozenset[str]  # subjective::* IDs needing re-review
    34→    under_target_ids: frozenset[str]  # below target, not stale/unscored
    35→
    36→    def should_inject_to_plan(self, fid: str) -> bool:
    37→        """Should this subjective ID be injected into plan queue_order?"""
    38→        if fid in self.unscored_ids:
    39→            return True  # unconditional
    40→        if fid in self.stale_ids:
    41→            return not self.has_objective_backlog
    42→        if fid in self.under_target_ids:
    43→            return not self.has_objective_backlog
    44→        return False
    45→
    46→    def should_evict_from_plan(self, fid: str) -> bool:
    47→        """Should this subjective ID be removed from plan queue_order?"""
    48→        if fid in self.unscored_ids:
    49→            return False  # never evict unscored
    50→        if fid in self.stale_ids or fid in self.under_target_ids:
    51→            return self.has_objective_backlog
    52→        return False
    53→
    54→    @property
    55→    def backlog_blocks_rerun(self) -> bool:
    56→        """Preflight: should reruns be blocked?"""
    57→        return self.has_objective_backlog
    58→
    59→
    60→def _is_evidence_only(issue: dict) -> bool:
    61→    """Return True if the issue is below its detector's standalone threshold."""
    62→    detector = issue.get("detector", "")
    63→    meta = DETECTORS.get(detector)
    64→    if meta and meta.standalone_threshold:
    65→        threshold_rank = CONFIDENCE_ORDER.get(meta.standalone_threshold, 9)
    66→        issue_rank = CONFIDENCE_ORDER.get(issue.get("confidence", "low"), 9)
    67→        if issue_rank > threshold_rank:
    68→            return True
    69→    return False
    70→
    71→
    72→class _ScanPathFromStatePolicy:
    73→    """Sentinel type: resolve scan_path from state."""
    74→
    75→
    76→_SCAN_PATH_FROM_STATE_POLICY = _ScanPathFromStatePolicy()
    77→ScanPathPolicyOption = str | None | _ScanPathFromStatePolicy
    78→
    79→
    80→def compute_subjective_visibility(
    81→    state: StateModel,
    82→    *,
    83→    target_strict: float = DEFAULT_TARGET_STRICT_SCORE,
    84→    scan_path: ScanPathPolicyOption = _SCAN_PATH_FROM_STATE_POLICY,
    85→    plan: dict | None = None,
    86→) -> SubjectiveVisibility:
    87→    """Build the policy snapshot from current state.
    88→
    89→    *scan_path* defaults to ``state["scan_path"]`` so callers don't need to
    90→    thread it manually.  Pass an explicit ``str`` to override, or ``None``
    91→    to disable scope filtering.  When *plan* is set, issues whose IDs
    92→    appear in ``plan["skipped"]`` are excluded.
    93→
    94→    Imports policy helpers from ``stale_policy`` so this module remains
    95→    side-effect free and cycle-safe.
    96→    """
    97→    from desloppify.engine._plan.policy.stale import (
    98→        current_stale_ids,
    99→        current_under_target_ids,
   100→        current_unscored_ids,
   101→    )
   102→
   103→    resolved_scan_path: str | None = (
   104→        state.get("scan_path")
   105→        if isinstance(scan_path, _ScanPathFromStatePolicy)
   106→        else scan_path
   107→    )
   108→
   109→    issues = state.get("issues", {})
   110→    skipped_ids = set((plan or {}).get("skipped", {}).keys())
   111→
   112→    # Count open, non-suppressed, objective issues.
   113→    # Evidence-only issues (below standalone confidence threshold) are
   114→    # excluded — they still affect scores but are not actionable queue items.
   115→    # Issues outside scan_path and plan-skipped issues are also excluded
   116→    # so the policy matches what the user actually sees in the queue.
   117→    objective_issue_ids = [
   118→        issue_id
   119→        for issue_id, issue in issues.items()
   120→        if issue.get("status") == Status.OPEN
   121→        and issue.get("detector") not in NON_OBJECTIVE_DETECTORS
   122→        and not issue.get("suppressed")
   123→        and not _is_evidence_only(issue)
   124→        and issue_in_scan_scope(str(issue.get("file", "")), resolved_scan_path)
   125→        and issue_id not in skipped_ids
   126→    ]
   127→
   128→    # Only explicitly queued objectives count — backlog items don't block
   129→    # subjective reruns.
   130→    objective_count = len(_executable_objective_ids(set(objective_issue_ids), plan))
   131→
   132→    unscored = current_unscored_ids(state)
   133→    stale = current_stale_ids(state)
   134→    under_target = current_under_target_ids(state, target_strict=target_strict)
   135→
   136→    return SubjectiveVisibility(
   137→        has_objective_backlog=objective_count > 0,
   138→        objective_count=objective_count,
   139→        unscored_ids=frozenset(unscored),
   140→        stale_ids=frozenset(stale),
   141→        under_target_ids=frozenset(under_target),
   142→    )
   143→
   144→
   145→__all__ = [
   146→    "NON_OBJECTIVE_DETECTORS",
   147→    "SubjectiveVisibility",
   148→    "compute_subjective_visibility",
   149→]
   150→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_scoring/policy/core.py"
}
```

> TOOL

tool_result Read
```
1→"""Scoring policies, detector mappings, and shared constants."""
     2→
     3→from __future__ import annotations
     4→
     5→from dataclasses import dataclass
     6→from typing import Literal
     7→
     8→from desloppify.base.enums import Tier
     9→from desloppify.base.registry import DETECTORS
    10→from desloppify.base.scoring_constants import (
    11→    CONFIDENCE_WEIGHTS,
    12→    HOLISTIC_MULTIPLIER,
    13→)
    14→from desloppify.engine.policy.zones import EXCLUDED_ZONE_VALUES
    15→
    16→ScoreMode = Literal["lenient", "strict", "verified_strict"]
    17→SCORING_MODES: tuple[ScoreMode, ...] = ("lenient", "strict", "verified_strict")
    18→
    19→
    20→@dataclass(frozen=True)
    21→class Dimension:
    22→    name: str
    23→    tier: int
    24→    detectors: list[str]
    25→
    26→
    27→@dataclass(frozen=True)
    28→class DetectorScoringPolicy:
    29→    detector: str
    30→    dimension: str | None
    31→    tier: int | None
    32→    file_based: bool = False
    33→    use_loc_weight: bool = False
    34→    excluded_zones: frozenset[str] = frozenset(EXCLUDED_ZONE_VALUES)
    35→
    36→
    37→# Security issues are excluded in non-production zones.
    38→SECURITY_EXCLUDED_ZONES = frozenset({"test", "config", "generated", "vendor"})
    39→_DEFAULT_EXCLUDED_ZONES = frozenset(EXCLUDED_ZONE_VALUES)
    40→
    41→# Non-objective detectors are tracked in state/queue but excluded from
    42→# mechanical dimension scoring.
    43→_NON_OBJECTIVE_DETECTORS = frozenset(
    44→    {
    45→        "concerns",
    46→        "review",
    47→        "subjective_review",
    48→        "uncalled_functions",
    49→        "unused_enums",
    50→        "signature",
    51→        "stale_wontfix",
    52→    }
    53→)
    54→
    55→# Keep policy details that are independent of tier/dimension wiring.
    56→_FILE_BASED_POLICY_DETECTORS = frozenset(
    57→    {"smells", "dict_keys", "test_coverage", "security", "concerns", "review"}
    58→)
    59→_LOC_WEIGHT_POLICY_DETECTORS = frozenset({"test_coverage"})
    60→_EXCLUDED_ZONE_OVERRIDES: dict[str, frozenset[str]] = {
    61→    "security": SECURITY_EXCLUDED_ZONES,
    62→}
    63→
    64→
    65→def _build_builtin_detector_scoring_policies() -> dict[str, DetectorScoringPolicy]:
    66→    """Build baseline scoring policies from DetectorMeta plus policy overrides."""
    67→    policies: dict[str, DetectorScoringPolicy] = {}
    68→    for detector, meta in DETECTORS.items():
    69→        if detector in _NON_OBJECTIVE_DETECTORS:
    70→            dimension: str | None = None
    71→            tier: int | None = None
    72→        else:
    73→            dimension = meta.dimension
    74→            tier = meta.tier
    75→
    76→        policies[detector] = DetectorScoringPolicy(
    77→            detector=detector,
    78→            dimension=dimension,
    79→            tier=tier,
    80→            file_based=detector in _FILE_BASED_POLICY_DETECTORS,
    81→            use_loc_weight=detector in _LOC_WEIGHT_POLICY_DETECTORS,
    82→            excluded_zones=_EXCLUDED_ZONE_OVERRIDES.get(
    83→                detector,
    84→                _DEFAULT_EXCLUDED_ZONES,
    85→            ),
    86→        )
    87→    return policies
    88→
    89→
    90→# Central scoring policy for each detector: tier/dimension come from registry,
    91→# while file-based and zone behavior are preserved via local overrides.
    92→DETECTOR_SCORING_POLICIES: dict[str, DetectorScoringPolicy] = (
    93→    _build_builtin_detector_scoring_policies()
    94→)
    95→_BASE_DETECTOR_SCORING_POLICIES: dict[str, DetectorScoringPolicy] = dict(
    96→    DETECTOR_SCORING_POLICIES
    97→)
    98→
    99→# Detectors where potential = file count but issues are per-(file, sub-type).
   100→# Per-file weighted failures are capped at 1.0 to match the file-based denominator.
   101→FILE_BASED_DETECTORS = {
   102→    detector
   103→    for detector, policy in DETECTOR_SCORING_POLICIES.items()
   104→    if policy.file_based
   105→}
   106→
   107→
   108→def _build_dimensions() -> list[Dimension]:
   109→    """Derive dimensions from DETECTOR_SCORING_POLICIES.
   110→
   111→    Each unique (dimension, tier) pair becomes a Dimension, with its detectors
   112→    collected automatically. Order follows first-seen in the policies dict.
   113→    """
   114→    # Collect (dimension_name -> tier) preserving first-seen order,
   115→    # and group detectors by dimension.
   116→    dim_tiers: dict[str, int] = {}
   117→    grouped: dict[str, list[str]] = {}
   118→    for detector, policy in DETECTOR_SCORING_POLICIES.items():
   119→        if policy.dimension is None or policy.tier is None:
   120→            continue
   121→        if policy.dimension not in dim_tiers:
   122→            dim_tiers[policy.dimension] = policy.tier
   123→            grouped[policy.dimension] = []
   124→        grouped[policy.dimension].append(detector)
   125→    return [
   126→        Dimension(name=name, tier=tier, detectors=grouped[name])
   127→        for name, tier in dim_tiers.items()
   128→    ]
   129→
   130→
   131→DIMENSIONS = _build_dimensions()
   132→DIMENSIONS_BY_NAME = {d.name: d for d in DIMENSIONS}
   133→
   134→TIER_WEIGHTS = {
   135→    Tier.AUTO_FIX: 1,
   136→    Tier.QUICK_FIX: 2,
   137→    Tier.JUDGMENT: 3,
   138→    Tier.MAJOR_REFACTOR: 4,
   139→}
   140→# Minimum checks for full dimension weight — below this, weight is dampened
   141→# proportionally. Prevents small-sample dimensions from swinging the overall score.
   142→MIN_SAMPLE = 200
   143→HOLISTIC_POTENTIAL = 10
   144→
   145→# Budget: subjective dimensions get this fraction of the overall score.
   146→# Mechanical dimensions get the remainder.
   147→SUBJECTIVE_WEIGHT_FRACTION = 0.75
   148→MECHANICAL_WEIGHT_FRACTION = 1.0 - SUBJECTIVE_WEIGHT_FRACTION
   149→
   150→# Per-dimension weighting within the mechanical pool.
   151→# Keep this balanced: no special boost for security/test in the pool itself.
   152→MECHANICAL_DIMENSION_WEIGHTS: dict[str, float] = {
   153→    "file health": 2.0,
   154→    "code quality": 1.0,
   155→    "duplication": 1.0,
   156→    "test health": 1.0,
   157→    "security": 1.0,
   158→}
   159→
   160→# Per-dimension weighting within the subjective pool.
   161→# Rationale (kept in sync with review metadata modules):
   162→# - High/mid elegance carry the most weight because architectural decomposition
   163→#   and seam quality drive broad maintainability and change velocity.
   164→# - Low elegance, contracts, and type safety remain high because they prevent
   165→#   correctness drift and interface ambiguity.
   166→# - Design coherence is a medium-high bridge between architecture intent and
   167→#   the detector-led concern stream.
   168→# - Structure navigation and error consistency are meaningful but secondary
   169→#   signals compared to core architecture/correctness dimensions.
   170→# - Naming quality and AI-generated debt are intentionally low-weight nudges:
   171→#   useful for polish/cleanup, but they should not dominate score movement.
   172→SUBJECTIVE_DIMENSION_WEIGHTS: dict[str, float] = {
   173→    "high elegance": 22.0,
   174→    "mid elegance": 22.0,
   175→    "low elegance": 12.0,
   176→    "contracts": 12.0,
   177→    "type safety": 12.0,
   178→    "abstraction fit": 8.0,
   179→    "logic clarity": 6.0,
   180→    # Low-but-meaningful structural signal (about half of the subjective
   181→    # average weight) so it matters without dominating craftsmanship axes.
   182→    "structure nav": 5.0,
   183→    "error consistency": 3.0,
   184→    "naming quality": 2.0,
   185→    "ai generated debt": 1.0,
   186→    "design coherence": 10.0,
   187→}
   188→
   189→# Synthetic check count for subjective dimensions in dimension_scores.
   190→SUBJECTIVE_CHECKS = 10
   191→
   192→FAILURE_STATUSES_BY_MODE: dict[ScoreMode, frozenset[str]] = {
   193→    "lenient": frozenset({"open", "deferred", "triaged_out"}),
   194→    "strict": frozenset({"open", "wontfix", "auto_resolved", "deferred", "triaged_out"}),
   195→    "verified_strict": frozenset({"open", "wontfix", "fixed", "false_positive", "deferred", "triaged_out"}),
   196→}
   197→
   198→# Tolerance for treating a subjective score as "on target" in integrity checks.
   199→# Scores within this band of the target are flagged as potential gaming.
   200→SUBJECTIVE_TARGET_MATCH_TOLERANCE = 0.05
   201→
   202→
   203→def matches_target_score(
   204→    score: object,
   205→    target: object,
   206→    *,
   207→    tolerance: float = SUBJECTIVE_TARGET_MATCH_TOLERANCE,
   208→) -> bool:
   209→    """Return True when score is within tolerance of target."""
   210→    try:
   211→        score_value = float(score)
   212→        target_value = float(target)
   213→        tolerance_value = max(0.0, float(tolerance))
   214→    except (TypeError, ValueError):
   215→        return False
   216→    return abs(score_value - target_value) <= tolerance_value
   217→
   218→
   219→def register_scoring_policy(policy: DetectorScoringPolicy) -> None:
   220→    """Register a scoring policy at runtime (used by generic plugins)."""
   221→    DETECTOR_SCORING_POLICIES[policy.detector] = policy
   222→    _rebuild_derived()
   223→
   224→
   225→def reset_registered_scoring_policies() -> None:
   226→    """Reset runtime-added scoring policies to built-in defaults."""
   227→    DETECTOR_SCORING_POLICIES.clear()
   228→    DETECTOR_SCORING_POLICIES.update(_BASE_DETECTOR_SCORING_POLICIES)
   229→    _rebuild_derived()
   230→
   231→
   232→def _rebuild_derived() -> None:
   233→    """Rebuild DIMENSIONS, DIMENSIONS_BY_NAME, FILE_BASED_DETECTORS from current state.
   234→
   235→    Mutates existing objects in-place so that all references (including imports
   236→    that bound the original objects) see the updates.
   237→    """
   238→    new_dims = _build_dimensions()
   239→    DIMENSIONS.clear()
   240→    DIMENSIONS.extend(new_dims)
   241→    DIMENSIONS_BY_NAME.clear()
   242→    DIMENSIONS_BY_NAME.update({d.name: d for d in DIMENSIONS})
   243→    FILE_BASED_DETECTORS.clear()
   244→    FILE_BASED_DETECTORS.update(
   245→        det for det, pol in DETECTOR_SCORING_POLICIES.items() if pol.file_based
   246→    )
   247→
   248→
   249→def detector_policy(detector: str) -> DetectorScoringPolicy:
   250→    """Get scoring policy for a detector, with a safe default fallback."""
   251→    return DETECTOR_SCORING_POLICIES.get(
   252→        detector,
   253→        DetectorScoringPolicy(detector=detector, dimension=None, tier=None),
   254→    )
   255→
   256→
   257→__all__ = [
   258→    "CONFIDENCE_WEIGHTS",
   259→    "DETECTOR_SCORING_POLICIES",
   260→    "DIMENSIONS",
   261→    "DIMENSIONS_BY_NAME",
   262→    "FAILURE_STATUSES_BY_MODE",
   263→    "FILE_BASED_DETECTORS",
   264→    "HOLISTIC_MULTIPLIER",
   265→    "HOLISTIC_POTENTIAL",
   266→    "MECHANICAL_DIMENSION_WEIGHTS",
   267→    "MECHANICAL_WEIGHT_FRACTION",
   268→    "MIN_SAMPLE",
   269→    "SCORING_MODES",
   270→    "SECURITY_EXCLUDED_ZONES",
   271→    "SUBJECTIVE_CHECKS",
   272→    "SUBJECTIVE_DIMENSION_WEIGHTS",
   273→    "SUBJECTIVE_TARGET_MATCH_TOLERANCE",
   274→    "SUBJECTIVE_WEIGHT_FRACTION",
   275→    "TIER_WEIGHTS",
   276→    "DetectorScoringPolicy",
   277→    "Dimension",
   278→    "ScoreMode",
   279→    "detector_policy",
   280→    "matches_target_score",
   281→    "register_scoring_policy",
   282→    "reset_registered_scoring_policies",
   283→]
   284→
```

> AGENT

Now let me search for the state_compat module and understanding of Finding type:

> TOOL

tool_use Glob
```json
{
  "pattern": "**/state_compat.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/state_compat.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "Finding|Issue.*TypedDict",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 6 files
desloppify/engine/_plan/schema/__init__.py
desloppify/intelligence/review/importing/contracts_types.py
desloppify/engine/_state/schema_types_issues.py
desloppify/app/commands/review/merge.py
desloppify/app/commands/review/batch/core_models.py
desloppify/tests/review/batch/test_prompt_sections.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/state_compat.py"
}
```

> TOOL

tool_result Read
```
1→"""Compatibility facade for legacy `desloppify.state` imports.
     2→
     3→New code should prefer narrower modules such as `desloppify.state_io` and
     4→`desloppify.state_score_snapshot`, but this module preserves the historical
     5→surface for callers that still import the old umbrella API.
     6→"""
     7→
     8→from desloppify.engine._state.filtering import (
     9→    add_ignore,
    10→    is_ignored,
    11→    issue_in_scan_scope,
    12→    make_issue,
    13→    open_scope_breakdown,
    14→    path_scoped_issues,
    15→    remove_ignored_issues,
    16→)
    17→from desloppify.engine._state.merge import (
    18→    MergeScanOptions,
    19→    find_suspect_detectors,
    20→    merge_scan,
    21→    upsert_issues,
    22→)
    23→from desloppify.engine._state.noise import (
    24→    DEFAULT_ISSUE_NOISE_BUDGET,
    25→    DEFAULT_ISSUE_NOISE_GLOBAL_BUDGET,
    26→    apply_issue_noise_budget,
    27→    resolve_issue_noise_budget,
    28→    resolve_issue_noise_global_budget,
    29→    resolve_issue_noise_settings,
    30→)
    31→from desloppify.engine._state.persistence import load_state, save_state, state_lock
    32→from desloppify.engine._state.resolution import (
    33→    coerce_assessment_score,
    34→    match_issues,
    35→    resolve_issues,
    36→)
    37→from desloppify.engine._state.schema import (
    38→    CURRENT_VERSION,
    39→    ConcernDismissal,
    40→    DimensionScore,
    41→    Issue,
    42→    ScanMetadataModel,
    43→    StateModel,
    44→    StateStats,
    45→    SubjectiveAssessment,
    46→    SubjectiveIntegrity,
    47→    empty_state,
    48→    ensure_state_defaults,
    49→    get_state_dir,
    50→    get_state_file,
    51→    json_default,
    52→    migrate_state_keys,
    53→    scan_inventory_available,
    54→    scan_metadata,
    55→    scan_reconstructed_issue_count,
    56→    scan_source,
    57→    scan_metrics_available,
    58→    utc_now,
    59→    validate_state_invariants,
    60→)
    61→from desloppify.engine._state.schema_scores import (
    62→    get_objective_score,
    63→    get_overall_score,
    64→    get_strict_score,
    65→    get_verified_strict_score,
    66→)
    67→from desloppify.state_score_snapshot import (
    68→    ScoreSnapshot,
    69→    score_snapshot,
    70→    suppression_metrics,
    71→)
    72→
    73→__all__ = [
    74→    "ConcernDismissal",
    75→    "CURRENT_VERSION",
    76→    "DEFAULT_ISSUE_NOISE_BUDGET",
    77→    "DEFAULT_ISSUE_NOISE_GLOBAL_BUDGET",
    78→    "DimensionScore",
    79→    "Issue",
    80→    "MergeScanOptions",
    81→    "ScanMetadataModel",
    82→    "ScoreSnapshot",
    83→    "StateModel",
    84→    "StateStats",
    85→    "SubjectiveAssessment",
    86→    "SubjectiveIntegrity",
    87→    "add_ignore",
    88→    "apply_issue_noise_budget",
    89→    "coerce_assessment_score",
    90→    "empty_state",
    91→    "ensure_state_defaults",
    92→    "find_suspect_detectors",
    93→    "get_objective_score",
    94→    "get_overall_score",
    95→    "get_state_dir",
    96→    "get_state_file",
    97→    "get_strict_score",
    98→    "get_verified_strict_score",
    99→    "is_ignored",
   100→    "issue_in_scan_scope",
   101→    "json_default",
   102→    "load_state",
   103→    "make_issue",
   104→    "match_issues",
   105→    "merge_scan",
   106→    "migrate_state_keys",
   107→    "open_scope_breakdown",
   108→    "path_scoped_issues",
   109→    "remove_ignored_issues",
   110→    "resolve_issue_noise_budget",
   111→    "resolve_issue_noise_global_budget",
   112→    "resolve_issue_noise_settings",
   113→    "resolve_issues",
   114→    "save_state",
   115→    "scan_inventory_available",
   116→    "scan_metadata",
   117→    "scan_metrics_available",
   118→    "scan_reconstructed_issue_count",
   119→    "scan_source",
   120→    "score_snapshot",
   121→    "state_lock",
   122→    "suppression_metrics",
   123→    "upsert_issues",
   124→    "utc_now",
   125→    "validate_state_invariants",
   126→]
   127→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema_types_issues.py"
}
```

> TOOL

tool_result Read
```
1→"""Issue and score-related TypedDict models for persisted state payloads."""
     2→
     3→from __future__ import annotations
     4→
     5→from typing import Any, NotRequired, TypedDict
     6→
     7→from desloppify.base.enums import Status
     8→
     9→
    10→class Issue(TypedDict):
    11→    """The central data structure: a normalized issue from any detector."""
    12→
    13→    id: str
    14→    detector: str
    15→    file: str
    16→    tier: int
    17→    confidence: str
    18→    summary: str
    19→    # Known detail shapes per detector (non-exhaustive, for reference):
    20→    #
    21→    # structural:      {loc, complexity_score?, complexity_signals?: list[str],
    22→    #                   name? (god class), ...god_class_metrics}
    23→    # smells:          {smell_id, severity, count, lines: list[int]}
    24→    # dupes:           {fn_a: dict, fn_b: dict, similarity, kind, cluster_size,
    25→    #                   cluster: list}
    26→    # coupling:        {target, tool?, direction, sole_tool?, importer_count?,
    27→    #                   loc?, source_tool?, target_tool?}
    28→    # single_use:      {loc, sole_importer}
    29→    # orphaned:        {loc}
    30→    # facade:          {loc, importers, imports_from: list[str], kind}
    31→    # review:          {holistic?: bool, dimension?, related_files?: list[str],
    32→    #                   suggestion?, evidence?: list[str], investigation?,
    33→    #                   merged_at?}
    34→    # review_coverage: {reason, loc?, age_days?, old_files?, new_files?}
    35→    # security:        {kind, severity, line, content, remediation}
    36→    # test_coverage:   {kind, loc?, importer_count?, loc_weight?,
    37→    #                   test_file?, test_functions?, assertions?, mocks?,
    38→    #                   snapshots?}
    39→    # props:           {passthrough entry fields minus "file"}
    40→    # subjective_assessment (synthetic): {dimension_name, dimension, failing,
    41→    #                   strict_score, open_review_issues?}
    42→    # workflow (synthetic): {stage?, strict?, plan_start_strict?, delta?,
    43→    #                   total_review_issues?, explanation?}
    44→    detail: dict[str, Any]
    45→    status: Status
    46→    note: str | None
    47→    first_seen: str
    48→    last_seen: str
    49→    resolved_at: str | None
    50→    reopen_count: int
    51→    suppressed: NotRequired[bool]
    52→    suppressed_at: NotRequired[str | None]
    53→    suppression_pattern: NotRequired[str | None]
    54→    resolution_attestation: NotRequired[dict[str, str | bool | None]]
    55→    lang: NotRequired[str]
    56→    zone: NotRequired[str]
    57→
    58→
    59→class TierStats(TypedDict, total=False):
    60→    open: int
    61→    fixed: int
    62→    auto_resolved: int
    63→    wontfix: int
    64→    false_positive: int
    65→    deferred: int
    66→    triaged_out: int
    67→
    68→
    69→class StateStats(TypedDict, total=False):
    70→    total: int
    71→    open: int
    72→    fixed: int
    73→    auto_resolved: int
    74→    wontfix: int
    75→    false_positive: int
    76→    deferred: int
    77→    triaged_out: int
    78→    by_tier: dict[str, TierStats]
    79→
    80→
    81→class DimensionScore(TypedDict, total=False):
    82→    score: float
    83→    strict: float
    84→    verified_strict_score: float
    85→    checks: int
    86→    failing: int
    87→    tier: int
    88→    carried_forward: bool
    89→    detectors: dict[str, Any]
    90→    coverage_status: str
    91→    coverage_confidence: float
    92→    coverage_impacts: list[dict[str, Any]]
    93→
    94→
    95→class ScoreConfidenceDetector(TypedDict, total=False):
    96→    """Detector-level confidence details persisted after each scan."""
    97→
    98→    detector: str
    99→    status: str
   100→    confidence: float
   101→    summary: str
   102→    impact: str
   103→    remediation: str
   104→    tool: str
   105→    reason: str
   106→
   107→
   108→class ScoreConfidenceModel(TypedDict, total=False):
   109→    """State-level score confidence summary."""
   110→
   111→    status: str
   112→    confidence: float
   113→    detectors: list[ScoreConfidenceDetector]
   114→    dimensions: list[str]
   115→
   116→
   117→class ScanHistoryEntry(TypedDict, total=False):
   118→    timestamp: str
   119→    lang: str | None
   120→    strict_score: float | None
   121→    verified_strict_score: float | None
   122→    objective_score: float | None
   123→    overall_score: float | None
   124→    open: int
   125→    diff_new: int
   126→    diff_resolved: int
   127→    ignored: int
   128→    raw_issues: int
   129→    suppressed_pct: float
   130→    ignore_patterns: int
   131→    subjective_integrity: dict[str, Any] | None
   132→    dimension_scores: dict[str, dict[str, float]] | None
   133→    score_confidence: ScoreConfidenceModel | None
   134→
   135→
   136→__all__ = [
   137→    "Issue",
   138→    "TierStats",
   139→    "StateStats",
   140→    "DimensionScore",
   141→    "ScoreConfidenceDetector",
   142→    "ScoreConfidenceModel",
   143→    "ScanHistoryEntry",
   144→]
   145→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "detector.*==|detector.*!=|detector.*in",
  "type": "python",
  "output_mode": "files_with_matches",
  "head_limit": 30
}
```

> TOOL

tool_result Grep
```
Found 30 files limit: 30, offset: 0
desloppify/app/commands/plan/triage/runner/stage_prompts_instruction_blocks.py
desloppify/engine/_plan/triage/prompt.py
desloppify/engine/_plan/policy/subjective.py
desloppify/tests/engine/test_sync_split_modules_direct.py
desloppify/engine/_work_queue/snapshot.py
desloppify/tests/state/test_state.py
desloppify/tests/scoring/test_scoring.py
desloppify/tests/review/work_queue_cases.py
desloppify/tests/scan/test_scan_helpers_direct.py
desloppify/tests/review/review_coverage_cases.py
desloppify/tests/review/context/test_holistic_review.py
desloppify/tests/plan/test_stale_policy.py
desloppify/tests/narrative/test_narrative_strategy_and_review.py
desloppify/tests/plan/test_auto_cluster_subjective_lifecycle.py
desloppify/tests/plan/test_auto_cluster.py
desloppify/tests/lang/typescript/test_typescript_detectors_fixers_and_wrappers_split_direct.py
desloppify/tests/narrative/test_narrative.py
desloppify/tests/lang/csharp/test_csharp_scan.py
desloppify/tests/lang/typescript/test_ts_detector_cli_helpers_direct.py
desloppify/tests/lang/common/test_lang_resolution_direct.py
desloppify/tests/lang/common/test_generic_plugin_integrations.py
desloppify/tests/lang/common/test_import_boundaries.py
desloppify/tests/lang/common/test_generic_plugin.py
desloppify/tests/lang/common/test_framework_runtime_helpers_split_direct.py
desloppify/tests/lang/common/test_framework_shared_phases_and_structural_split_direct.py
desloppify/tests/intelligence/test_review_import_prepare_split_direct.py
desloppify/tests/lang/common/test_framework_registration_and_commands_split_direct.py
desloppify/tests/detectors/test_zones_policy_filters.py
desloppify/tests/detectors/test_zones.py
desloppify/tests/detectors/test_concerns.py
```

> AGENT

Now let me search for concerns-related code and ID prefixes:

> TOOL

tool_use Grep
```json
{
  "pattern": "concerns::|review::|subjective_review::|subjective_assessment::",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 74 files
desloppify/tests/plan/test_epic_triage.py
desloppify/tests/plan/test_epic_triage_prompt_direct.py
desloppify/tests/commands/plan/test_triage_runner.py
desloppify/tests/commands/plan/test_plan_overrides_direct.py
desloppify/tests/engine/test_sync_split_modules_direct.py
desloppify/tests/state/test_state_internal_direct.py
desloppify/tests/state/test_state.py
desloppify/tests/review/work_queue_cases.py
desloppify/tests/review/review_coverage_cases.py
desloppify/tests/review/context/test_holistic_review_dimensions_and_structure.py
desloppify/tests/review/context/test_holistic_review.py
desloppify/tests/plan/test_unified_disposition_map.py
desloppify/tests/plan/test_triage_snapshot_direct.py
desloppify/tests/plan/test_triage_snapshot.py
desloppify/tests/plan/test_schema_migrations.py
desloppify/tests/plan/test_stale_policy.py
desloppify/tests/plan/test_auto_cluster.py
desloppify/tests/intelligence/test_review_import_prepare_split_direct.py
desloppify/tests/commands/test_cmd_next.py
desloppify/tests/commands/show/test_cmd_show.py
desloppify/tests/commands/review/test_review_preflight.py
desloppify/tests/commands/review/test_review_importing_support_direct.py
desloppify/tests/commands/resolve/test_plan_load_degraded_mode.py
desloppify/tests/commands/plan/test_triage_stage_prompts_flow_direct.py
desloppify/tests/commands/plan/test_triage_stage_flow_observe_reflect_organize_direct.py
desloppify/tests/commands/plan/test_triage_stage_helpers_direct.py
desloppify/tests/commands/plan/test_triage_stage_policy_direct.py
desloppify/tests/commands/plan/test_triage_split_modules_direct.py
desloppify/tests/commands/plan/test_triage_display_direct.py
desloppify/tests/commands/plan/test_triage_evidence_parsing.py
desloppify/tests/commands/plan/test_saved_plan_recovery.py
desloppify/tests/commands/plan/test_triage_coverage.py
desloppify/tests/commands/plan/test_reflect_disposition_ledger.py
desloppify/tests/commands/plan/test_cluster_ops_direct.py
desloppify/tests/commands/plan/test_move_unified.py
desloppify/engine/_plan/triage/snapshot.py
desloppify/engine/_plan/schema/normalize.py
desloppify/engine/_plan/reconcile_review_import.py
desloppify/app/commands/plan/triage/stages/helpers.py
desloppify/app/commands/plan/cluster/dispatch.py
desloppify/tests/commands/plan/test_triage_confirmation.py
desloppify/tests/commands/plan/test_triage_auto_start.py
desloppify/tests/commands/plan/test_triage_fold_confirm.py
desloppify/tests/scan/test_scan_reporting_subjective_paths.py
desloppify/tests/review/test_work_queue_issues_direct.py
desloppify/tests/review/policy/test_review_integrity_direct.py
desloppify/tests/plan/test_stale_dimensions_cycle_and_queue_order.py
desloppify/tests/plan/test_plan.py
desloppify/tests/plan/test_epic_triage_parsing_direct.py
desloppify/tests/narrative/test_recovered_state_headline.py
desloppify/tests/engine/test_defer_policy_and_scope_direct.py
desloppify/tests/commands/test_queue_order_guard.py
desloppify/tests/commands/test_helpers.py
desloppify/tests/commands/plan/test_triage_tooling_fixes.py
desloppify/tests/commands/plan/test_triage_stage_validation_auto_confirm.py
desloppify/tests/commands/plan/test_cluster_ux.py
desloppify/engine/_state/recovery.py
desloppify/engine/_plan/triage/parsing.py
desloppify/engine/_plan/cluster_strategy.py
desloppify/tests/commands/test_next_render.py
desloppify/tests/commands/plan/test_triage_stage_records.py
desloppify/tests/commands/plan/test_triage_stage_rendering.py
desloppify/tests/review/context/test_issue_history_context.py
desloppify/tests/review/test_runner_parallel_types_direct.py
desloppify/tests/review/test_work_queue_ranking_output_direct.py
desloppify/tests/plan/test_step_completion_direct.py
desloppify/tests/plan/test_persistence_runtime_paths.py
desloppify/tests/commands/test_next_render_scoring_subjective_direct.py
desloppify/tests/commands/test_parser_groups_option_sections_direct.py
desloppify/tests/commands/review/test_review_external_module_direct.py
desloppify/engine/_plan/step_completion.py
desloppify/tests/review/batch/test_split_modules_direct.py
desloppify/tests/plan/test_suffix_matching.py
desloppify/tests/commands/test_next_nudges.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "class.*Concern|ConcernDismissal",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 12 files
desloppify/state_compat.py
desloppify/engine/_state/schema_types_review.py
desloppify/engine/_state/schema_types.py
desloppify/app/commands/review/batch/core_models.py
desloppify/engine/_state/schema.py
desloppify/tests/review/context/test_mechanical_evidence.py
desloppify/tests/review/batch/test_prompt_sections.py
desloppify/state_io.py
desloppify/tests/detectors/test_concerns_signals_and_helpers.py
desloppify/engine/_concerns/text.py
desloppify/engine/_concerns/types.py
desloppify/languages/typescript/tests/test_ts_concerns.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1→"""State schema/types, constants, and validation helpers."""
     2→
     3→from __future__ import annotations
     4→
     5→from datetime import UTC, datetime
     6→from pathlib import Path
     7→from typing import Any, cast
     8→
     9→from desloppify.base.discovery.paths import get_project_root
    10→from desloppify.base.enums import Status, canonical_issue_status, issue_status_tokens
    11→from desloppify.engine._state.schema_scores import (
    12→    json_default,
    13→)
    14→from desloppify.engine._state.schema_types import (
    15→    AssessmentImportAuditEntry,
    16→    AttestationLogEntry,
    17→    ConcernDismissal,
    18→    DimensionScore,
    19→    IgnoreIntegrityModel,
    20→    Issue,
    21→    LangCapability,
    22→    ReviewCacheModel,
    23→    ScanMetadataModel,
    24→    ScanDiff,
    25→    ScanHistoryEntry,
    26→    ScoreConfidenceDetector,
    27→    ScoreConfidenceModel,
    28→    StateModel,
    29→    StateStats,
    30→    SubjectiveAssessment,
    31→    SubjectiveAssessmentJudgment,
    32→    SubjectiveIntegrity,
    33→    TierStats,
    34→)
    35→
    36→__all__ = [
    37→    "ConcernDismissal",
    38→    "AssessmentImportAuditEntry",
    39→    "AttestationLogEntry",
    40→    "Issue",
    41→    "TierStats",
    42→    "StateStats",
    43→    "DimensionScore",
    44→    "ScoreConfidenceDetector",
    45→    "ScoreConfidenceModel",
    46→    "ScanHistoryEntry",
    47→    "SubjectiveAssessment",
    48→    "SubjectiveAssessmentJudgment",
    49→    "SubjectiveIntegrity",
    50→    "LangCapability",
    51→    "ReviewCacheModel",
    52→    "IgnoreIntegrityModel",
    53→    "ScanMetadataModel",
    54→    "StateModel",
    55→    "ScanDiff",
    56→    "get_state_dir",
    57→    "get_state_file",
    58→    "CURRENT_VERSION",
    59→    "utc_now",
    60→    "empty_state",
    61→    "ensure_state_defaults",
    62→    "scan_source",
    63→    "scan_metadata",
    64→    "scan_inventory_available",
    65→    "scan_metrics_available",
    66→    "scan_reconstructed_issue_count",
    67→    "validate_state_invariants",
    68→    "json_default",
    69→    "migrate_state_keys",
    70→]
    71→
    72→_ALLOWED_ISSUE_STATUSES: set[str] = {
    73→    *issue_status_tokens(),
    74→}
    75→_SCAN_METADATA_SOURCES = {"empty", "scan", "plan_reconstruction"}
    76→
    77→
    78→def get_state_dir() -> Path:
    79→    """Return the active state directory for the current runtime context."""
    80→    return get_project_root() / ".desloppify"
    81→
    82→
    83→def get_state_file() -> Path:
    84→    """Return the default state file for the current runtime context."""
    85→    return get_state_dir() / "state.json"
    86→
    87→
    88→CURRENT_VERSION = 1
    89→
    90→
    91→def utc_now() -> str:
    92→    """Return current UTC timestamp with second-level precision."""
    93→    return datetime.now(UTC).isoformat(timespec="seconds")
    94→
    95→
    96→def empty_state() -> StateModel:
    97→    """Return a new empty state payload."""
    98→    return {
    99→        "version": CURRENT_VERSION,
   100→        "created": utc_now(),
   101→        "last_scan": None,
   102→        "scan_count": 0,
   103→        "overall_score": 0,
   104→        "objective_score": 0,
   105→        "strict_score": 0,
   106→        "verified_strict_score": 0,
   107→        "stats": {},
   108→        "issues": {},
   109→        "scan_coverage": {},
   110→        "score_confidence": {},
   111→        "scan_metadata": {"source": "empty"},
   112→        "subjective_integrity": {},
   113→        "subjective_assessments": {},
   114→    }
   115→
   116→
   117→def _as_non_negative_int(value: Any, default: int = 0) -> int:
   118→    try:
   119→        parsed = int(value)
   120→    except (TypeError, ValueError):
   121→        return default
   122→    return parsed if parsed >= 0 else 0
   123→
   124→
   125→def _rename_key(d: dict, old: str, new: str) -> bool:
   126→    if old not in d:
   127→        return False
   128→    d.setdefault(new, d.pop(old))
   129→    return True
   130→
   131→
   132→def migrate_state_keys(state: StateModel | dict[str, Any]) -> None:
   133→    """Migrate legacy key names in-place.
   134→
   135→    - ``"findings"`` → ``"issues"``
   136→    - ``dimension_scores[dim]["issues"]`` → ``"failing"``
   137→    """
   138→    state_dict = cast(dict[str, Any], state)
   139→    _rename_key(state_dict, "findings", "issues")
   140→
   141→    for ds in state_dict.get("dimension_scores", {}).values():
   142→        if isinstance(ds, dict):
   143→            _rename_key(ds, "issues", "failing")
   144→
   145→    for entry in state_dict.get("scan_history", []):
   146→        if not isinstance(entry, dict):
   147→            continue
   148→        _rename_key(entry, "raw_findings", "raw_issues")
   149→        for ds in (entry.get("dimension_scores") or {}).values():
   150→            if isinstance(ds, dict):
   151→                _rename_key(ds, "issues", "failing")
   152→
   153→
   154→def _normalize_scan_metadata(state: StateModel | dict[str, Any]) -> None:
   155→    raw_metadata = state.get("scan_metadata")
   156→    metadata = raw_metadata if isinstance(raw_metadata, dict) else {}
   157→
   158→    source = _coerce_scan_source(state, metadata)
   159→    normalized: ScanMetadataModel = {"source": source}
   160→    if source == "plan_reconstruction":
   161→        normalized["plan_queue_available"] = bool(metadata.get("plan_queue_available"))
   162→        issue_count = metadata.get("reconstructed_issue_count", 0)
   163→        if isinstance(issue_count, int) and not isinstance(issue_count, bool):
   164→            normalized["reconstructed_issue_count"] = max(0, issue_count)
   165→        else:
   166→            normalized["reconstructed_issue_count"] = 0
   167→
   168→    state["scan_metadata"] = normalized
   169→
   170→
   171→def ensure_state_defaults(state: StateModel | dict) -> None:
   172→    """Normalize loose/legacy state payloads to a valid base shape in-place."""
   173→    migrate_state_keys(state)
   174→
   175→    mutable_state = cast(dict[str, Any], state)
   176→    for key, value in empty_state().items():
   177→        mutable_state.setdefault(key, value)
   178→
   179→    if not isinstance(state.get("issues"), dict):
   180→        state["issues"] = {}
   181→    if not isinstance(state.get("stats"), dict):
   182→        state["stats"] = {}
   183→    if not isinstance(state.get("scan_history"), list):
   184→        state["scan_history"] = []
   185→    if not isinstance(state.get("scan_coverage"), dict):
   186→        state["scan_coverage"] = {}
   187→    if not isinstance(state.get("score_confidence"), dict):
   188→        state["score_confidence"] = {}
   189→    if not isinstance(state.get("subjective_integrity"), dict):
   190→        state["subjective_integrity"] = {}
   191→    _normalize_scan_metadata(state)
   192→
   193→    all_issues = state["issues"]
   194→    to_remove: list[str] = []
   195→    for issue_id, issue in all_issues.items():
   196→        if not isinstance(issue, dict):
   197→            to_remove.append(issue_id)
   198→            continue
   199→
   200→        issue.setdefault("id", issue_id)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/types.py"
}
```

> TOOL

tool_result Read
```
1→"""Shared concern datatypes."""
     2→
     3→from __future__ import annotations
     4→
     5→from dataclasses import dataclass
     6→from typing import Literal, TypedDict
     7→
     8→
     9→@dataclass(frozen=True)
    10→class Concern:
    11→    """A potential design problem surfaced by mechanical signals."""
    12→
    13→    type: str
    14→    file: str
    15→    summary: str
    16→    evidence: tuple[str, ...]
    17→    question: str
    18→    fingerprint: str
    19→    source_issues: tuple[str, ...]
    20→
    21→
    22→class ConcernSignals(TypedDict, total=False):
    23→    """Typed signal payload extracted from mechanical issues."""
    24→
    25→    max_params: float
    26→    max_nesting: float
    27→    loc: float
    28→    function_count: float
    29→    monster_loc: float
    30→    monster_funcs: list[str]
    31→
    32→
    33→SignalKey = Literal[
    34→    "max_params",
    35→    "max_nesting",
    36→    "loc",
    37→    "function_count",
    38→    "monster_loc",
    39→]
    40→
    41→__all__ = ["Concern", "ConcernSignals", "SignalKey"]
    42→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema_types.py",
  "limit": 300
}
```

> TOOL

tool_result Read
```
1→"""TypedDict model definitions for persisted state payloads."""
     2→
     3→from __future__ import annotations
     4→
     5→from typing import Any, NotRequired, Required, TypedDict
     6→
     7→from desloppify.engine._state.schema_types_issues import (
     8→    DimensionScore,
     9→    Issue,
    10→    ScanHistoryEntry,
    11→    ScoreConfidenceDetector,
    12→    ScoreConfidenceModel,
    13→    StateStats,
    14→    TierStats,
    15→)
    16→from desloppify.engine._state.schema_types_review import (
    17→    AssessmentImportAuditEntry,
    18→    AttestationLogEntry,
    19→    ConcernDismissal,
    20→    ContextInsight,
    21→    DimensionContext,
    22→    IgnoreIntegrityModel,
    23→    LangCapability,
    24→    ReviewCacheModel,
    25→    SubjectiveAssessment,
    26→    SubjectiveAssessmentJudgment,
    27→    SubjectiveIntegrity,
    28→)
    29→from desloppify.languages.framework import ScanCoverageRecord
    30→
    31→
    32→class ScanMetadataModel(TypedDict, total=False):
    33→    source: Required[str]
    34→    # Legacy persisted inputs may still include these derived flags. Canonical
    35→    # normalized payloads derive capabilities from ``source`` instead.
    36→    inventory_available: NotRequired[bool]
    37→    metrics_available: NotRequired[bool]
    38→    plan_queue_available: bool
    39→    reconstructed_issue_count: int
    40→
    41→
    42→class StateModel(TypedDict, total=False):
    43→    version: Required[int]
    44→    created: Required[str]
    45→    last_scan: Required[str | None]
    46→    scan_count: Required[int]
    47→    overall_score: Required[float]
    48→    objective_score: Required[float]
    49→    strict_score: Required[float]
    50→    verified_strict_score: Required[float]
    51→    stats: Required[StateStats]
    52→    issues: Required[dict[str, Issue]]
    53→    dimension_scores: dict[str, DimensionScore]
    54→    scan_path: str | None
    55→    tool_hash: str
    56→    scan_completeness: dict[str, str]
    57→    potentials: dict[str, dict[str, int]]
    58→    codebase_metrics: dict[str, dict[str, Any]]
    59→    scan_coverage: dict[str, ScanCoverageRecord]
    60→    score_confidence: ScoreConfidenceModel
    61→    scan_history: list[ScanHistoryEntry]
    62→    lang_capabilities: dict[str, LangCapability]
    63→    zone_distribution: dict[str, int]
    64→    review_cache: ReviewCacheModel
    65→    reminder_history: dict[str, int]
    66→    ignore_integrity: IgnoreIntegrityModel
    67→    config: dict[str, Any]
    68→    lang: str
    69→    subjective_integrity: Required[SubjectiveIntegrity]
    70→    subjective_assessments: Required[dict[str, SubjectiveAssessment]]
    71→    custom_review_dimensions: list[str]
    72→    assessment_import_audit: list[AssessmentImportAuditEntry]
    73→    attestation_log: list[AttestationLogEntry]
    74→    concern_dismissals: dict[str, ConcernDismissal]
    75→    dimension_contexts: dict[str, DimensionContext]
    76→    _plan_start_scores_for_reveal: dict[str, Any]
    77→    scan_metadata: Required[ScanMetadataModel]
    78→
    79→
    80→class ScanDiff(TypedDict):
    81→    new: int
    82→    auto_resolved: int
    83→    reopened: int
    84→    total_current: int
    85→    suspect_detectors: list[str]
    86→    chronic_reopeners: list[dict]
    87→    skipped_other_lang: int
    88→    resolved_out_of_scope: int
    89→    ignored: int
    90→    ignore_patterns: int
    91→    raw_issues: int
    92→    suppressed_pct: float
    93→    skipped: NotRequired[int]
    94→    skipped_details: NotRequired[list[dict]]
    95→
    96→
    97→__all__ = [
    98→    "ConcernDismissal",
    99→    "ContextInsight",
   100→    "DimensionContext",
   101→    "AssessmentImportAuditEntry",
   102→    "AttestationLogEntry",
   103→    "Issue",
   104→    "TierStats",
   105→    "StateStats",
   106→    "DimensionScore",
   107→    "ScoreConfidenceDetector",
   108→    "ScoreConfidenceModel",
   109→    "ScanHistoryEntry",
   110→    "SubjectiveAssessment",
   111→    "SubjectiveAssessmentJudgment",
   112→    "SubjectiveIntegrity",
   113→    "LangCapability",
   114→    "ReviewCacheModel",
   115→    "IgnoreIntegrityModel",
   116→    "ScanMetadataModel",
   117→    "StateModel",
   118→    "ScanDiff",
   119→]
   120→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/snapshot.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1→"""Canonical queue snapshot for phase and visibility decisions."""
     2→
     3→from __future__ import annotations
     4→
     5→from collections.abc import Iterable
     6→from dataclasses import dataclass
     7→from typing import Any
     8→
     9→from desloppify.base.config import DEFAULT_TARGET_STRICT_SCORE
    10→from desloppify.engine._plan.constants import (
    11→    WORKFLOW_DEFERRED_DISPOSITION_ID,
    12→    WORKFLOW_RUN_SCAN_ID,
    13→)
    14→from desloppify.engine._plan.policy.subjective import NON_OBJECTIVE_DETECTORS
    15→from desloppify.engine._plan.schema import (
    16→    executable_objective_ids as _executable_objective_ids,
    17→)
    18→from desloppify.engine._plan.triage.snapshot import build_triage_snapshot
    19→from desloppify.engine._state.filtering import path_scoped_issues
    20→from desloppify.engine._state.schema import StateModel
    21→from desloppify.engine._work_queue.ranking import build_issue_items
    22→from desloppify.engine._work_queue.synthetic import (
    23→    build_subjective_items,
    24→    build_triage_stage_items,
    25→)
    26→from desloppify.engine._work_queue.synthetic_workflow import (
    27→    build_communicate_score_item,
    28→    build_create_plan_item,
    29→    build_deferred_disposition_item,
    30→    build_import_scores_item,
    31→    build_run_scan_item,
    32→    build_score_checkpoint_item,
    33→)
    34→from desloppify.engine._work_queue.types import WorkQueueItem
    35→
    36→PHASE_REVIEW_INITIAL = "review_initial"
    37→PHASE_EXECUTE = "execute"
    38→PHASE_SCAN = "scan"
    39→PHASE_REVIEW_POSTFLIGHT = "review_postflight"
    40→PHASE_WORKFLOW_POSTFLIGHT = "workflow_postflight"
    41→PHASE_TRIAGE_POSTFLIGHT = "triage_postflight"
    42→
    43→
    44→@dataclass(frozen=True)
    45→class QueueSnapshot:
    46→    """Canonical queue facts and partitions for one invocation."""
    47→
    48→    phase: str
    49→    all_objective_items: tuple[WorkQueueItem, ...]
    50→    all_initial_review_items: tuple[WorkQueueItem, ...]
    51→    all_postflight_review_items: tuple[WorkQueueItem, ...]
    52→    all_scan_items: tuple[WorkQueueItem, ...]
    53→    all_postflight_workflow_items: tuple[WorkQueueItem, ...]
    54→    all_postflight_triage_items: tuple[WorkQueueItem, ...]
    55→    execution_items: tuple[WorkQueueItem, ...]
    56→    backlog_items: tuple[WorkQueueItem, ...]
    57→    objective_in_scope_count: int
    58→    planned_objective_count: int
    59→    objective_execution_count: int
    60→    objective_backlog_count: int
    61→    subjective_initial_count: int
    62→    subjective_postflight_count: int
    63→    workflow_postflight_count: int
    64→    triage_pending_count: int
    65→    has_unplanned_objective_blockers: bool
    66→
    67→
    68→def _option_value(options: object | None, name: str, default: Any) -> Any:
    69→    if options is None:
    70→        return default
    71→    return getattr(options, name, default)
    72→
    73→
    74→def _resolved_scan_path(options: object | None, state: StateModel) -> str | None:
    75→    scan_path = _option_value(options, "scan_path", state.get("scan_path"))
    76→    if hasattr(scan_path, "__class__") and scan_path.__class__.__name__ == "_ScanPathFromState":
    77→        return state.get("scan_path")
    78→    return scan_path
    79→
    80→
    81→def _is_fresh_boundary(plan: dict | None) -> bool:
    82→    if not isinstance(plan, dict):
    83→        return True
    84→    scores = plan.get("plan_start_scores")
    85→    if not scores:
    86→        return True
    87→    return isinstance(scores, dict) and bool(scores.get("reset"))
    88→
    89→
    90→def _is_objective_item(item: WorkQueueItem, *, skipped_ids: set[str]) -> bool:
    91→    return (
    92→        item.get("kind") in {"issue", "cluster"}
    93→        and item.get("detector", "") not in NON_OBJECTIVE_DETECTORS
    94→        and item.get("id", "") not in skipped_ids
    95→    )
    96→
    97→
    98→def _review_issue_items(items: Iterable[WorkQueueItem]) -> list[WorkQueueItem]:
    99→    return [
   100→        item for item in items
   101→        if item.get("detector", "") in {"review", "concerns", "subjective_review"}
   102→    ]
   103→
   104→
   105→def _auto_promoted_autofix_ids(plan: dict | None) -> set[str]:
   106→    """Return auto-cluster member IDs eligible to execute without manual promotion."""
   107→    if not isinstance(plan, dict):
   108→        return set()
   109→    autofix_ids: set[str] = set()
   110→    skipped_ids = set(plan.get("skipped", {}).keys())
   111→    for cluster in plan.get("clusters", {}).values():
   112→        if not isinstance(cluster, dict) or not cluster.get("auto"):
   113→            continue
   114→        action = str(cluster.get("action", ""))
   115→        if "desloppify autofix" not in action:
   116→            continue
   117→        for issue_id in cluster.get("issue_ids", []):
   118→            if isinstance(issue_id, str) and issue_id and issue_id not in skipped_ids:
   119→                autofix_ids.add(issue_id)
   120→    return autofix_ids
   121→
   122→
   123→def _executable_review_issue_items(
   124→    plan: dict | None,
   125→    state: StateModel,
   126→    review_issue_items: list[WorkQueueItem],
   127→) -> list[WorkQueueItem]:
   128→    """Hide raw review findings until triage is current for the live issue set."""
   129→    if not review_issue_items or not isinstance(plan, dict):
   130→        return review_issue_items
   131→
   132→    triage_snapshot = build_triage_snapshot(plan, state)
   133→    if triage_snapshot.has_triage_in_queue:
   134→        return []
   135→    if triage_snapshot.is_triage_stale:
   136→        return []
   137→    if not triage_snapshot.triage_has_run:
   138→        return []
   139→    return review_issue_items
   140→
   141→
   142→def _subjective_partitions(
   143→    state: StateModel,
   144→    *,
   145→    scoped_issues: dict[str, dict],
   146→    threshold: float,
   147→) -> tuple[list[WorkQueueItem], list[WorkQueueItem]]:
   148→    candidates = build_subjective_items(state, scoped_issues, threshold=threshold)
   149→    initial = [item for item in candidates if item.get("initial_review")]
   150→    postflight = [item for item in candidates if not item.get("initial_review")]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema_types_review.py",
  "limit": 250
}
```

> TOOL

tool_result Read
```
1→"""Review- and assessment-related TypedDict models for persisted state payloads."""
     2→
     3→from __future__ import annotations
     4→
     5→from typing import Any, TypedDict
     6→
     7→
     8→class SubjectiveIntegrity(TypedDict, total=False):
     9→    """Anti-gaming metadata for subjective assessment scores."""
    10→
    11→    status: str  # "disabled" | "pass" | "warn" | "penalized"
    12→    target_score: float | None
    13→    matched_count: int
    14→    matched_dimensions: list[str]
    15→    reset_dimensions: list[str]
    16→
    17→
    18→class SubjectiveAssessmentJudgment(TypedDict, total=False):
    19→    """Reviewer's holistic judgment narrative for a subjective dimension."""
    20→
    21→    strengths: list[str]
    22→    issue_character: str
    23→    dimension_character: str
    24→    score_rationale: str
    25→
    26→
    27→class SubjectiveAssessment(TypedDict, total=False):
    28→    """A single subjective dimension assessment payload."""
    29→
    30→    score: float
    31→    source: str
    32→    assessed_at: str
    33→    reset_by: str
    34→    placeholder: bool
    35→    components: list[str]
    36→    component_scores: dict[str, float]
    37→    integrity_penalty: str | None
    38→    provisional_override: bool
    39→    provisional_until_scan: int
    40→    needs_review_refresh: bool
    41→    refresh_reason: str | None
    42→    stale_since: str | None
    43→    judgment: SubjectiveAssessmentJudgment
    44→
    45→
    46→class ConcernDismissal(TypedDict, total=False):
    47→    """Record of a dismissed concern from review output."""
    48→
    49→    dismissed_at: str
    50→    reason: str | None
    51→    dimension: str
    52→    reasoning: str
    53→    concern_type: str
    54→    concern_file: str
    55→    source_issue_ids: list[str]
    56→
    57→
    58→class AssessmentImportAuditEntry(TypedDict, total=False):
    59→    """Typed record for review assessment import events."""
    60→
    61→    timestamp: str
    62→    mode: str
    63→    trusted: bool
    64→    reason: str
    65→    override_used: bool
    66→    attested_external: bool
    67→    provisional: bool
    68→    provisional_count: int
    69→    attest: str
    70→    import_file: str
    71→
    72→
    73→class AttestationLogEntry(TypedDict, total=False):
    74→    """Typed entry for resolve/suppress attestation history."""
    75→
    76→    timestamp: str | None
    77→    command: str
    78→    pattern: str
    79→    attestation: str | None
    80→    affected: int
    81→
    82→
    83→class LangCapability(TypedDict, total=False):
    84→    """Capabilities reported for a language runtime."""
    85→
    86→    fixers: list[str]
    87→    typecheck_cmd: str
    88→
    89→
    90→class ReviewCacheModel(TypedDict, total=False):
    91→    """Cached review metadata keyed by relative file path."""
    92→
    93→    files: dict[str, dict[str, Any]]
    94→    holistic: dict[str, Any]
    95→
    96→
    97→class IgnoreIntegrityModel(TypedDict, total=False):
    98→    """Ignore/suppression integrity summary used by reporting surfaces."""
    99→
   100→    ignored: int
   101→    suppressed_pct: float
   102→    ignore_patterns: int
   103→    raw_issues: int
   104→
   105→
   106→class ContextInsight(TypedDict, total=False):
   107→    """A single piece of accumulated knowledge about a dimension."""
   108→
   109→    header: str
   110→    description: str
   111→    settled: bool
   112→    positive: bool
   113→    added_at: str
   114→    source: str
   115→
   116→
   117→class DimensionContext(TypedDict, total=False):
   118→    """Accumulated understanding for a subjective dimension across review rounds."""
   119→
   120→    insights: list[ContextInsight]
   121→    created_at: str
   122→    updated_at: str
   123→    stable_rounds: int
   124→
   125→
   126→__all__ = [
   127→    "AssessmentImportAuditEntry",
   128→    "AttestationLogEntry",
   129→    "ConcernDismissal",
   130→    "ContextInsight",
   131→    "DimensionContext",
   132→    "IgnoreIntegrityModel",
   133→    "LangCapability",
   134→    "ReviewCacheModel",
   135→    "SubjectiveAssessment",
   136→    "SubjectiveAssessmentJudgment",
   137→    "SubjectiveIntegrity",
   138→]
   139→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "def.*concern|def.*subjective_assessment|def.*review_issue",
  "type": "python",
  "output_mode": "files_with_matches",
  "head_limit": 20
}
```

> TOOL

tool_result Grep
```
Found 20 files limit: 20, offset: 0
desloppify/tests/plan/test_epic_triage.py
desloppify/engine/_plan/triage/prompt.py
desloppify/engine/_work_queue/snapshot.py
desloppify/tests/state/test_state_internal_direct.py
desloppify/tests/scoring/test_scoring.py
desloppify/tests/review/work_queue_cases.py
desloppify/tests/review/review_coverage_cases.py
desloppify/tests/review/import_scoring/test_review_external.py
desloppify/tests/review/context/test_holistic_review.py
desloppify/tests/plan/test_stale_policy.py
desloppify/tests/plan/test_epic_triage_apply_edge_cases.py
desloppify/tests/narrative/test_narrative_strategy_and_review.py
desloppify/tests/plan/test_auto_cluster.py
desloppify/tests/narrative/test_narrative.py
desloppify/tests/intelligence/test_review_import_prepare_split_direct.py
desloppify/tests/detectors/test_concerns.py
desloppify/tests/commands/test_lifecycle_transitions.py
desloppify/tests/commands/show/test_cmd_show.py
desloppify/tests/commands/review/test_review_preflight.py
desloppify/tests/commands/review/test_review_batch_core_direct.py
```

> AGENT

Now let me look at the work queue types and how items are classified:

> TOOL

tool_use Grep
```json
{
  "pattern": "class.*WorkQueueItem|WorkQueueItem.*=.*TypedDict",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
No files found
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/types.py"
}
```

> TOOL

tool_result Read
```
1→"""Typed contracts for unified work-queue items."""
     2→
     3→from __future__ import annotations
     4→
     5→from typing import Any, Literal, TypeAlias, TypedDict
     6→
     7→QueueItemKind: TypeAlias = Literal[
     8→    "issue",
     9→    "cluster",
    10→    "workflow_stage",
    11→    "workflow_action",
    12→    "subjective_dimension",
    13→]
    14→
    15→
    16→class PlanClusterRef(TypedDict, total=False):
    17→    """Plan-cluster metadata stamped onto queue items."""
    18→
    19→    name: str
    20→    description: str | None
    21→    total_items: int
    22→    action_steps: list[dict[str, Any]]
    23→
    24→
    25→class QueueItemBase(TypedDict):
    26→    """Required fields shared by all queue views."""
    27→
    28→    id: str
    29→    kind: QueueItemKind
    30→    summary: str
    31→
    32→
    33→class QueueItemCommon(QueueItemBase, total=False):
    34→    """Optional fields shared across multiple queue item variants."""
    35→
    36→    detector: str
    37→    file: str
    38→    confidence: str
    39→    detail: dict[str, Any]
    40→    status: str
    41→    note: str | None
    42→    first_seen: str
    43→    last_seen: str
    44→    resolved_at: str | None
    45→    reopen_count: int
    46→    suppressed: bool
    47→    lang: str
    48→
    49→    # Ranking + policy metadata
    50→    is_review: bool
    51→    is_subjective: bool
    52→    review_weight: float | None
    53→    subjective_score: float | None
    54→    estimated_impact: float
    55→    primary_command: str
    56→    action_type: str
    57→    explain: dict[str, Any]
    58→
    59→    # Plan-order metadata
    60→    _plan_position: int | None
    61→    _is_new: bool
    62→    queue_position: int
    63→    plan_description: str
    64→    plan_note: str
    65→    plan_cluster: PlanClusterRef
    66→    plan_skipped: bool
    67→    plan_skip_kind: str
    68→    plan_skip_reason: str
    69→
    70→    # Optional passthrough keys observed in queue item payloads
    71→    active_cluster: str | None
    72→    auto: bool
    73→    cluster: str
    74→    clusters: dict[str, Any]
    75→    count: int
    76→    description: str
    77→    dimension_scores: dict[str, Any]
    78→    entries: list[Any]
    79→    epic_triage_meta: dict[str, Any]
    80→    fixers: list[str]
    81→    issue_ids: list[str]
    82→    issues: dict[str, Any]
    83→    lang_capabilities: dict[str, Any]
    84→    name: str
    85→    optional: bool
    86→    overall_per_point: float
    87→    plan_start_scores: dict[str, Any]
    88→    queue_order: list[str]
    89→    reason: str
    90→    scan_history: list[dict[str, Any]]
    91→    scan_path: str | None
    92→    skipped: dict[str, Any]
    93→    triage_stages: dict[str, Any]
    94→
    95→
    96→class IssueQueueItem(QueueItemCommon, total=False):
    97→    """Concrete queue item for a detector finding."""
    98→
    99→    tier: int
   100→
   101→
   102→class ClusterQueueItem(QueueItemCommon, total=False):
   103→    """Collapsed plan/work queue cluster item."""
   104→
   105→    members: list["WorkQueueItem"]
   106→    member_count: int
   107→    cluster_name: str
   108→    cluster_auto: bool
   109→    cluster_optional: bool
   110→
   111→
   112→class WorkflowStageItem(QueueItemCommon, total=False):
   113→    """Workflow-stage item used by triage/import checkpoints."""
   114→
   115→    stage_name: str
   116→    stage_index: int
   117→    blocked_by: list[str]
   118→    is_blocked: bool
   119→
   120→
   121→class WorkflowActionItem(QueueItemCommon, total=False):
   122→    """Workflow action or synthetic helper item."""
   123→
   124→    action: str
   125→
   126→
   127→class SubjectiveDimensionItem(QueueItemCommon, total=False):
   128→    """Subjective-dimension queue item."""
   129→
   130→    initial_review: bool
   131→    cli_keys: list[str]
   132→    dimension: str
   133→    dimension_name: str
   134→    strict: float
   135→    score: float
   136→    failing: int
   137→    timestamp: str
   138→    placeholder: bool
   139→    stale: bool
   140→
   141→
   142→class SerializedClusterMember(TypedDict, total=False):
   143→    """Serialized cluster member payload used by next/backlog JSON output."""
   144→
   145→    id: str | None
   146→    kind: QueueItemKind
   147→    confidence: str | None
   148→    detector: str | None
   149→    file: str | None
   150→    summary: str | None
   151→    status: str | None
   152→    primary_command: str | None
   153→
   154→
   155→class SerializedQueueItem(TypedDict, total=False):
   156→    """Serialized queue item payload written to query/output surfaces."""
   157→
   158→    id: str | None
   159→    kind: QueueItemKind
   160→    confidence: str | None
   161→    detector: str | None
   162→    file: str | None
   163→    summary: str | None
   164→    detail: dict[str, Any]
   165→    status: str | None
   166→    primary_command: str | None
   167→    blocked_by: list[str]
   168→    is_blocked: bool
   169→    explain: dict[str, Any]
   170→    queue_position: int
   171→    plan_description: str
   172→    plan_note: str
   173→    plan_cluster: PlanClusterRef
   174→    plan_skipped: bool
   175→    plan_skip_kind: str
   176→    plan_skip_reason: str
   177→    action_type: str
   178→    member_count: int
   179→    members: list["SerializedClusterMember"]
   180→    cluster_name: str
   181→    cluster_auto: bool
   182→    members_truncated: bool
   183→    members_sample_limit: int
   184→    autofix_hint: str
   185→    action_steps: list[dict[str, Any]]
   186→
   187→
   188→WorkQueueItem: TypeAlias = (
   189→    IssueQueueItem
   190→    | ClusterQueueItem
   191→    | WorkflowStageItem
   192→    | WorkflowActionItem
   193→    | SubjectiveDimensionItem
   194→)
   195→WorkQueueGroups: TypeAlias = dict[str, list[WorkQueueItem]]
   196→
   197→
   198→__all__ = [
   199→    "ClusterQueueItem",
   200→    "IssueQueueItem",
   201→    "PlanClusterRef",
   202→    "QueueItemBase",
   203→    "QueueItemCommon",
   204→    "QueueItemKind",
   205→    "SerializedClusterMember",
   206→    "SerializedQueueItem",
   207→    "SubjectiveDimensionItem",
   208→    "WorkflowActionItem",
   209→    "WorkflowStageItem",
   210→    "WorkQueueGroups",
   211→    "WorkQueueItem",
   212→]
   213→
```

> AGENT

Now let me search for how concerns and subjective_assessment issues are generated:

> TOOL

tool_use Grep
```json
{
  "pattern": "build_subjective_items|build_concern",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 6 files
desloppify/engine/_work_queue/snapshot.py
desloppify/tests/commands/test_direct_coverage_modules.py
desloppify/engine/_work_queue/synthetic.py
desloppify/engine/_work_queue/inputs.py
desloppify/app/commands/review/prompt_sections.py
desloppify/tests/commands/test_direct_coverage_split_modules.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/synthetic.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1→"""Synthetic work-queue item builders and dimension scoring.
     2→
     3→Builds workflow stage items, score checkpoint items, create-plan items,
     4→subjective dimension items, and subjective score lookups.
     5→"""
     6→
     7→from __future__ import annotations
     8→
     9→from typing import Any
    10→
    11→from desloppify.engine.plan_triage import TRIAGE_STAGE_SPECS
    12→from desloppify.engine._scoring.subjective.core import DISPLAY_NAMES
    13→from desloppify.engine._state.schema import StateModel
    14→from desloppify.engine._work_queue.helpers import (
    15→    detail_dict,
    16→    slugify,
    17→)
    18→from desloppify.engine._work_queue.synthetic_workflow import (
    19→    build_communicate_score_item,
    20→    build_create_plan_item,
    21→    build_deferred_disposition_item,
    22→    build_import_scores_item,
    23→    build_run_scan_item,
    24→    build_score_checkpoint_item,
    25→)
    26→from desloppify.engine._work_queue.types import WorkQueueItem
    27→from desloppify.engine._plan.constants import (
    28→    confirmed_triage_stage_names,
    29→    recorded_unconfirmed_triage_stage_names,
    30→)
    31→from desloppify.engine.plan_triage import (
    32→    TRIAGE_IDS,
    33→    TRIAGE_STAGE_DEPENDENCIES,
    34→    TRIAGE_STAGE_LABELS,
    35→    triage_manual_stage_command,
    36→    triage_run_stages_command,
    37→    triage_runner_commands,
    38→)
    39→from desloppify.engine.planning.scorecard_projection import (
    40→    all_subjective_entries,
    41→)
    42→from desloppify.intelligence.integrity import (
    43→    unassessed_subjective_dimensions,
    44→)
    45→
    46→# ---------------------------------------------------------------------------
    47→# Dimension key normalization
    48→# ---------------------------------------------------------------------------
    49→
    50→def _canonical_subjective_dimension_key(display_name: str) -> str:
    51→    """Map a display label (e.g. 'Mid elegance') to its canonical dimension key."""
    52→    cleaned = display_name.replace(" (subjective)", "").strip()
    53→    target = cleaned.lower()
    54→
    55→    for dim_key, label in DISPLAY_NAMES.items():
    56→        if str(label).lower() == target:
    57→            return str(dim_key)
    58→    return slugify(cleaned)
    59→
    60→
    61→def _subjective_dimension_aliases(display_name: str) -> set[str]:
    62→    """Return normalized aliases used to match display labels with issue dimension keys."""
    63→    cleaned = display_name.replace(" (subjective)", "").strip()
    64→    canonical = _canonical_subjective_dimension_key(cleaned)
    65→    return {
    66→        cleaned.lower(),
    67→        cleaned.replace(" ", "_").lower(),
    68→        slugify(cleaned),
    69→        canonical.lower(),
    70→        slugify(canonical),
    71→    }
    72→
    73→
    74→# ---------------------------------------------------------------------------
    75→# Subjective strict scores
    76→# ---------------------------------------------------------------------------
    77→
    78→def subjective_strict_scores(state: StateModel | dict[str, Any]) -> dict[str, float]:
    79→    dim_scores = state.get("dimension_scores", {}) or {}
    80→    if not dim_scores:
    81→        return {}
    82→
    83→    entries = all_subjective_entries(state, dim_scores=dim_scores)
    84→    scores: dict[str, float] = {}
    85→    for entry in entries:
    86→        name = str(entry.get("name", "")).strip()
    87→        if not name:
    88→            continue
    89→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
    90→        [REDACTED](name)
    91→        aliases = _subjective_dimension_aliases(name)
    92→        for cli_key in entry.get("cli_keys", []):
    93→            key = str(cli_key).strip().lower()
    94→            if not key:
    95→                continue
    96→            aliases.add(key)
    97→            aliases.add(slugify(key))
    98→        aliases.add(dim_key.lower())
    99→        aliases.add(slugify(dim_key))
   100→        for alias in aliases:
   101→            scores[alias] = strict_val
   102→    return scores
   103→
   104→
   105→# ---------------------------------------------------------------------------
   106→# Synthetic item builders
   107→# ---------------------------------------------------------------------------
   108→
   109→def build_triage_stage_items(plan: dict, state: dict) -> list[WorkQueueItem]:
   110→    """Build synthetic work items for each ``triage::*`` stage ID in the queue.
   111→
   112→    Returns an empty list when no triage stages are pending.
   113→    """
   114→    order = plan.get("queue_order", [])
   115→    order_set = set(order)
   116→    present_ids = order_set & TRIAGE_IDS
   117→    meta = plan.get("epic_triage_meta", {})
   118→    confirmed = confirmed_triage_stage_names(meta)
   119→    recorded_unconfirmed = recorded_unconfirmed_triage_stage_names(meta)
   120→    present_names = {
   121→        name
   122→        for name, sid in TRIAGE_STAGE_SPECS
   123→        if sid in present_ids
   124→    }
   125→    present_names.update(recorded_unconfirmed)
   126→    if not present_names:
   127→        return []
   128→
   129→    issues = state.get("issues", {})
   130→    open_review_count = sum(
   131→        1 for f in issues.values()
   132→        if f.get("status") == "open"
   133→        and f.get("detector") in ("review", "concerns")
   134→    )
   135→
   136→    label_map = dict(TRIAGE_STAGE_LABELS)
   137→    items: list[WorkQueueItem] = []
   138→    for name, sid in TRIAGE_STAGE_SPECS:
   139→        if name not in present_names:
   140→            continue
   141→        if name in confirmed:
   142→            continue
   143→
   144→        # Compute blocked_by: dependency stages that are still in the queue
   145→        deps = TRIAGE_STAGE_DEPENDENCIES.get(name, set())
   146→        blocked_by = sorted(
   147→            f"triage::{dep}" for dep in deps if dep in present_names and dep not in confirmed
   148→        )
   149→
   150→        only_stages = None if name == "commit" else name
   151→        cmd = triage_run_stages_command(only_stages=only_stages)
   152→
   153→        item: WorkQueueItem = {
   154→            "id": sid,
   155→            "tier": 1,
   156→            "confidence": "high",
   157→            "detector": "triage",
   158→            "file": ".",
   159→            "kind": "workflow_stage",
   160→            "summary": f"Triage: {label_map.get(name, name)}",
   161→            "detail": {
   162→                "total_review_issues": open_review_count,
   163→                "stage": name,
   164→                "stage_label": label_map.get(name, name),
   165→                "runner_commands": [
   166→                    {"label": label, "command": command}
   167→                    for label, command in triage_runner_commands(only_stages=only_stages)
   168→                ],
   169→                "manual_fallback": triage_manual_stage_command(name),
   170→            },
   171→            "blocked_by": blocked_by,
   172→            "is_blocked": bool(blocked_by),
   173→        }
   174→        item["primary_command"] = cmd
   175→        items.append(item)
   176→    return items
   177→
   178→
   179→def build_subjective_items(
   180→    state: dict, issues: dict, *, threshold: float = 100.0
   181→) -> list[WorkQueueItem]:
   182→    """Create synthetic subjective work items."""
   183→    dim_scores = state.get("dimension_scores", {}) or {}
   184→    if not dim_scores:
   185→        return []
   186→    threshold = max(0.0, min(100.0, float(threshold)))
   187→
   188→    subjective_entries = all_subjective_entries(state, dim_scores=dim_scores)
   189→    if not subjective_entries:
   190→        return []
   191→    unassessed_dims = {
   192→        str(name).strip()
   193→        for name in unassessed_subjective_dimensions(
   194→            dim_scores
   195→        )
   196→    }
   197→
   198→    # Review issues are keyed by raw dimension name (snake_case).
   199→    review_open_by_dim: dict[str, int] = {}
   200→    for issue in issues.values():
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/synthetic.py",
  "offset": 200,
  "limit": 200
}
```

> TOOL

tool_result Read
```
200→    for issue in issues.values():
   201→        if issue.get("status") != "open":
   202→            continue
   203→        if issue.get("detector") == "review":
   204→            dim_key = str(detail_dict(issue).get("dimension", "")).strip().lower()
   205→            if dim_key:
   206→                review_open_by_dim[dim_key] = review_open_by_dim.get(dim_key, 0) + 1
   207→
   208→    items: list[WorkQueueItem] = []
   209→    def _prepare_command(
   210→        cli_keys: list[str],
   211→        *,
   212→        force_review_rerun: bool = False,
   213→    ) -> str:
   214→        command = "desloppify review --prepare"
   215→        if cli_keys:
   216→            command += " --dimensions " + ",".join(cli_keys)
   217→        if force_review_rerun:
   218→            command += " --force-review-rerun"
   219→        return command
   220→
   221→    for entry in subjective_entries:
   222→        name = str(entry.get("name", "")).strip()
   223→        if not name:
   224→            continue
   225→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
   226→        if strict_val >= threshold:
   227→            continue
   228→
   229→        [REDACTED](name)
   230→        aliases = set(_subjective_dimension_aliases(name))
   231→        cli_keys = [
   232→            str(key).strip().lower()
   233→            for key in entry.get("cli_keys", [])
   234→            if str(key).strip()
   235→        ]
   236→        aliases.update(cli_keys)
   237→        aliases.update(slugify(key) for key in cli_keys)
   238→        open_review = sum(review_open_by_dim.get(alias, 0) for alias in aliases)
   239→        is_unassessed = bool(entry.get("placeholder")) or (
   240→            name in unassessed_dims
   241→            or (strict_val <= 0.0 and int(entry.get("failing", 0)) == 0)
   242→        )
   243→        is_stale = bool(entry.get("stale"))
   244→        # If review issues already exist for this dimension, triage/fix them
   245→        # before suggesting another review refresh pass.
   246→        if open_review > 0:
   247→            primary_command = "desloppify show review --status open"
   248→        else:
   249→            primary_command = _prepare_command(cli_keys)
   250→        stale_tag = " [stale — re-review]" if is_stale else ""
   251→        summary = f"Subjective dimension below target: {name} ({strict_val:.1f}%){stale_tag}"
   252→        item: WorkQueueItem = {
   253→            "id": f"subjective::{slugify(dim_key)}",
   254→            "detector": "subjective_assessment",
   255→            "file": ".",
   256→            "confidence": "medium",
   257→            "summary": summary,
   258→            "detail": {
   259→                "dimension_name": name,
   260→                "dimension": dim_key,
   261→                "failing": int(entry.get("failing", 0)),
   262→                "strict_score": strict_val,
   263→                "open_review_issues": open_review,
   264→                "cli_keys": cli_keys,
   265→            },
   266→            "status": "open",
   267→        }
   268→        item["kind"] = "subjective_dimension"
   269→        item["primary_command"] = primary_command
   270→        item["initial_review"] = is_unassessed
   271→        items.append(item)
   272→    return items
   273→
   274→
   275→__all__ = [
   276→    "build_communicate_score_item",
   277→    "build_create_plan_item",
   278→    "build_deferred_disposition_item",
   279→    "build_import_scores_item",
   280→    "build_run_scan_item",
   281→    "build_score_checkpoint_item",
   282→    "build_subjective_items",
   283→    "build_triage_stage_items",
   284→    "subjective_strict_scores",
   285→]
   286→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "subjective_assessment|subjective::|concerns::review::",
  "type": "python",
  "output_mode": "files_with_matches",
  "head_limit": 20
}
```

> TOOL

tool_result Grep
```
Found 20 files limit: 20, offset: 0
desloppify/engine/_plan/policy/subjective.py
desloppify/tests/review/test_work_queue_plan_order_and_triage.py
desloppify/tests/engine/test_sync_split_modules_direct.py
desloppify/tests/state/test_state_suppression_and_integrity.py
desloppify/tests/state/test_state_internal_direct.py
desloppify/tests/state/test_state.py
desloppify/tests/scan/test_scan_workflow_integration_direct.py
desloppify/tests/scoring/test_scorecard.py
desloppify/tests/scoring/test_scoring.py
desloppify/tests/review/work_queue_cases.py
desloppify/tests/review/review_submodules_cases.py
desloppify/tests/review/review_commands_cases.py
desloppify/tests/plan/test_schema_migrations.py
desloppify/tests/plan/test_stale_policy.py
desloppify/tests/narrative/test_narrative_strategy_and_review.py
desloppify/tests/plan/test_auto_cluster_subjective_lifecycle.py
desloppify/tests/plan/test_auto_cluster.py
desloppify/tests/lang/common/test_framework_shared_phases_and_structural_split_direct.py
desloppify/tests/intelligence/test_review_import_prepare_split_direct.py
desloppify/tests/commands/test_lifecycle_transitions.py
```

> AGENT

Now let me search for how review and concerns issues are generated and managed:

> TOOL

tool_use Grep
```json
{
  "pattern": "detector.*==.*review|detector.*==.*concerns|make_issue.*review|make_issue.*concerns",
  "type": "python",
  "output_mode": "files_with_matches",
  "head_limit": 20
}
```

> TOOL

tool_result Grep
```
Found 20 files limit: 20, offset: 0
desloppify/tests/review/context/test_holistic_review.py
desloppify/tests/lang/common/test_framework_shared_phases_and_structural_split_direct.py
desloppify/tests/intelligence/test_review_import_prepare_split_direct.py
desloppify/tests/commands/test_lifecycle_transitions.py
desloppify/intelligence/review/importing/holistic.py
desloppify/engine/_work_queue/synthetic.py
desloppify/app/commands/show/dimension_views.py
desloppify/app/commands/review/merge.py
desloppify/tests/review/review_submodules_import_and_remediation_cases.py
desloppify/tests/review/import_scoring/test_review_import_scoring.py
desloppify/tests/narrative/test_action_engine_routing_direct.py
desloppify/tests/commands/test_helpers.py
desloppify/intelligence/narrative/signals.py
desloppify/intelligence/narrative/reminders_rules_followup.py
desloppify/intelligence/integrity.py
desloppify/intelligence/narrative/action_engine_routing.py
desloppify/engine/_work_queue/helpers.py
desloppify/engine/_work_queue/issues.py
desloppify/engine/_state/merge_issues.py
desloppify/app/commands/next/render_support.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/detectors/*concerns*"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/concerns.py
/Users/user_c042661f/Documents/desloppify/desloppify/tests/detectors/test_concerns_signals.py
/Users/user_c042661f/Documents/desloppify/desloppify/tests/detectors/test_concerns_signals_and_helpers.py
/Users/user_c042661f/Documents/desloppify/desloppify/tests/detectors/test_concerns.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/concerns.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1→"""Mixed concerns detection (UI + data fetching + transforms in one file)."""
     2→
     3→from __future__ import annotations
     4→
     5→import json
     6→import logging
     7→import re
     8→from pathlib import Path
     9→from typing import Any
    10→
    11→from desloppify.base.discovery.file_paths import rel
    12→
    13→from desloppify.base.discovery.source import find_tsx_files
    14→from desloppify.base.output.fallbacks import log_best_effort_failure
    15→from desloppify.base.output.terminal import colorize, print_table
    16→from desloppify.base.discovery.paths import get_project_root
    17→
    18→logger = logging.getLogger(__name__)
    19→
    20→
    21→def detect_mixed_concerns(path: Path) -> tuple[list[dict[str, Any]], int]:
    22→    """Find files that mix UI rendering with data fetching, state management, and business logic.
    23→
    24→    Heuristic: a .tsx file that has both JSX returns AND direct API/supabase calls
    25→    or both UI components AND heavy data transformation.
    26→
    27→    Returns (entries, total_files_checked).
    28→    """
    29→    files = find_tsx_files(path)
    30→    entries = []
    31→    for filepath in files:
    32→        try:
    33→            p = (
    34→                Path(filepath)
    35→                if Path(filepath).is_absolute()
    36→                else get_project_root() / filepath
    37→            )
    38→            content = p.read_text()
    39→            loc = len(content.splitlines())
    40→            if loc < 100:
    41→                continue
    42→
    43→            concerns = []
    44→
    45→            # UI rendering
    46→            has_jsx = bool(re.search(r"return\s*\(?\s*<", content))
    47→            if has_jsx:
    48→                concerns.append("jsx_rendering")
    49→
    50→            # Data fetching
    51→            has_fetch = bool(
    52→                re.search(r"useQuery|useMutation|supabase\.|fetch\(|axios", content)
    53→            )
    54→            if has_fetch:
    55→                concerns.append("data_fetching")
    56→
    57→            # Direct supabase calls (should be in hooks/services)
    58→            has_supabase = bool(re.search(r"supabase\.\w+\.\w+\.\w+", content))
    59→            if has_supabase:
    60→                concerns.append("direct_supabase")
    61→
    62→            # Heavy data transformation
    63→            transform_patterns = len(
    64→                re.findall(r"\.(map|filter|reduce|sort|flatMap)\s*\(", content)
    65→            )
    66→            if transform_patterns >= 3:
    67→                concerns.append(f"data_transforms({transform_patterns})")
    68→
    69→            # Event handler definitions (>5 = probably doing too much)
    70→            handler_count = len(re.findall(r"(?:const|function)\s+handle\w+", content))
    71→            if handler_count >= 5:
    72→                concerns.append(f"handlers({handler_count})")
    73→
    74→            # Flag if 3+ concern types in one file
    75→            if len(concerns) >= 3:
    76→                entries.append(
    77→                    {
    78→                        "file": filepath,
    79→                        "loc": loc,
    80→                        "concerns": concerns,
    81→                        "concern_count": len(concerns),
    82→                    }
    83→                )
    84→        except (OSError, UnicodeDecodeError) as exc:
    85→            log_best_effort_failure(
    86→                logger, f"read TSX concern candidate {filepath}", exc
    87→            )
    88→            continue
    89→    return sorted(entries, key=lambda e: -e["concern_count"]), len(files)
    90→
    91→
    92→def cmd_concerns(args: Any) -> None:
    93→    entries, _ = detect_mixed_concerns(Path(args.path))
    94→    if args.json:
    95→        print(json.dumps({"count": len(entries), "entries": entries}, indent=2))
    96→        return
    97→    if not entries:
    98→        print(colorize("No mixed-concern files found.", "green"))
    99→        return
   100→    print(colorize(f"\nMixed concerns: {len(entries)} files\n", "bold"))
   101→    rows = []
   102→    for e in entries[: args.top]:
   103→        rows.append([rel(e["file"]), str(e["loc"]), ", ".join(e["concerns"])])
   104→    print_table(["File", "LOC", "Concerns"], rows, [55, 5, 50])
   105→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "detector == \\\"review\\\"|detector == \\\"concerns\\\"|detector == \\\"subjective_assessment\\\"",
  "type": "python",
  "output_mode": "content",
  "head_limit": 30
}
```

> TOOL

tool_result Grep
```
desloppify/intelligence/narrative/action_engine_routing.py:63:    elif detector == "review":
desloppify/intelligence/narrative/signals.py:105:        if detector == "review" and issue.get("detail", {}).get("holistic"):
desloppify/app/commands/next/render_scoring.py:164:    if detector == "review" and dim_scores:
desloppify/app/commands/next/render.py:192:    if detector == "review":

[Showing results with pagination = limit: 30, offset: 0]
```

> AGENT

Let me search for where review and concerns issues are created/inserted:

> TOOL

tool_use Grep
```json
{
  "pattern": "\\\"review\\\"|\\\"concerns\\\"|\\\"subjective_review\\\"",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review",
  "type": "python",
  "output_mode": "files_with_matches",
  "head_limit": 20
}
```

> TOOL

tool_result Grep
```
Found 8 files limit: 20, offset: 0
desloppify/intelligence/review/prepare_holistic_orchestration.py
desloppify/intelligence/review/importing/holistic.py
desloppify/intelligence/review/prepare.py
desloppify/intelligence/review/importing/holistic_cache.py
desloppify/intelligence/review/importing/holistic_issue_flow.py
desloppify/intelligence/review/importing/per_file.py
desloppify/intelligence/review/_prepare/remediation_engine.py
desloppify/intelligence/review/_prepare/issue_history.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/importing/holistic.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1→"""Holistic review issue import workflow."""
     2→
     3→from __future__ import annotations
     4→
     5→from pathlib import Path
     6→from typing import Any
     7→
     8→from desloppify import state as state_mod
     9→from desloppify.engine.concerns import cleanup_stale_dismissals, generate_concerns
    10→from desloppify.engine.scoring import HOLISTIC_POTENTIAL
    11→from desloppify.intelligence.review.dimensions import normalize_dimension_name
    12→from desloppify.intelligence.review.dimensions.data import load_dimensions_for_lang
    13→from desloppify.intelligence.review.importing.assessments import (
    14→    backfill_judgment_strengths,
    15→    store_assessments,
    16→    store_context_updates,
    17→)
    18→from desloppify.intelligence.review.importing.contracts_types import (
    19→    ReviewImportPayload,
    20→    ReviewIssuePayload,
    21→)
    22→from desloppify.intelligence.review.importing.holistic_cache import (
    23→    resolve_holistic_coverage_issues,
    24→    resolve_reviewed_file_coverage_issues,
    25→    update_holistic_review_cache,
    26→    update_reviewed_file_cache,
    27→)
    28→from desloppify.intelligence.review.importing.holistic_issue_flow import (
    29→    auto_resolve_stale_holistic as _auto_resolve_stale_holistic,
    30→)
    31→from desloppify.intelligence.review.importing.holistic_issue_flow import (
    32→    collect_imported_dimensions as _collect_imported_dimensions,
    33→)
    34→from desloppify.intelligence.review.importing.holistic_issue_flow import (
    35→    validate_and_build_issues as _validate_and_build_issues,
    36→)
    37→from desloppify.intelligence.review.importing.payload import (
    38→    ReviewImportEnvelope,
    39→    parse_review_import_payload,
    40→)
    41→from desloppify.intelligence.review.importing.state_helpers import (
    42→    ensure_lang_potentials,
    43→)
    44→
    45→
    46→def parse_holistic_import_payload(
    47→    data: ReviewImportPayload | dict[str, Any],
    48→) -> tuple[list[ReviewIssuePayload], dict[str, Any] | None, list[str]]:
    49→    """Parse strict holistic import payload object."""
    50→    payload = parse_review_import_payload(data, mode_name="Holistic")
    51→    return payload.issues, payload.assessments, payload.reviewed_files
    52→
    53→
    54→def import_holistic_issues(
    55→    issues_data: ReviewImportPayload,
    56→    state: state_mod.StateModel,
    57→    lang_name: str,
    58→    *,
    59→    project_root: Path | str | None = None,
    60→    utc_now_fn=state_mod.utc_now,
    61→) -> dict[str, Any]:
    62→    """Import holistic (codebase-wide) issues into state."""
    63→    payload: ReviewImportEnvelope = parse_review_import_payload(
    64→        issues_data,
    65→        mode_name="Holistic",
    66→    )
    67→    issues_list = payload.issues
    68→    assessments = payload.assessments
    69→    reviewed_files = payload.reviewed_files
    70→    dimension_judgment = payload.dimension_judgment
    71→    context_updates = payload.context_updates
    72→    review_scope = issues_data.get("review_scope", {})
    73→    if not isinstance(review_scope, dict):
    74→        review_scope = {}
    75→    review_scope.setdefault("full_sweep_included", None)
    76→    scope_full_sweep = review_scope.get("full_sweep_included")
    77→    if not isinstance(scope_full_sweep, bool):
    78→        scope_full_sweep = None
    79→
    80→    _, holistic_prompts, _ = load_dimensions_for_lang(lang_name)
    81→    valid_dimensions = {
    82→        normalize_dimension_name(dim)
    83→        for dim in holistic_prompts
    84→        if isinstance(dim, str)
    85→    }
    86→
    87→    if assessments:
    88→        store_assessments(
    89→            state,
    90→            assessments,
    91→            source="holistic",
    92→            utc_now_fn=utc_now_fn,
    93→            dimension_judgment=dimension_judgment,
    94→        )
    95→
    96→    # Store accumulated dimension context updates
    97→    if isinstance(context_updates, dict):
    98→        store_context_updates(
    99→            state,
   100→            context_updates,
   101→            valid_dimensions=valid_dimensions,
   102→            utc_now_fn=utc_now_fn,
   103→        )
   104→        # Derive judgment.strengths from positive context insights
   105→        backfill_judgment_strengths(state, context_updates)
   106→
   107→    review_issues, skipped, dismissed_concerns = _validate_and_build_issues(
   108→        issues_list,
   109→        holistic_prompts,
   110→        lang_name,
   111→    )
   112→    imported_dimensions = _collect_imported_dimensions(
   113→        issues_list=issues_list,
   114→        review_issues=review_issues,
   115→        assessments=assessments if isinstance(assessments, dict) else None,
   116→        review_scope=review_scope,
   117→        valid_dimensions=valid_dimensions,
   118→    )
   119→
   120→    if dismissed_concerns:
   121→        store = state.setdefault("concern_dismissals", {})
   122→        now = utc_now_fn()
   123→        current_concerns = generate_concerns(state)
   124→        concern_sources = {
   125→            concern.fingerprint: list(concern.source_issues)
   126→            for concern in current_concerns
   127→        }
   128→        for dismissal in dismissed_concerns:
   129→            fingerprint = dismissal["fingerprint"]
   130→            store[fingerprint] = {
   131→                "dismissed_at": now,
   132→                "reasoning": dismissal.get("reasoning", ""),
   133→                "concern_type": dismissal.get("concern_type", ""),
   134→                "concern_file": dismissal.get("concern_file", ""),
   135→                "source_issue_ids": concern_sources.get(fingerprint, []),
   136→            }
   137→
   138→    potentials = ensure_lang_potentials(state, lang_name)
   139→    existing_review = potentials.get("review", 0)
   140→    potentials["review"] = max(existing_review, HOLISTIC_POTENTIAL)
   141→
   142→    concern_count = sum(1 for issue in review_issues if issue.get("detector") == "concerns")
   143→    if concern_count:
   144→        potentials["concerns"] = max(potentials.get("concerns", 0), concern_count)
   145→
   146→    merge_potentials_dict: dict[str, int] = {"review": potentials.get("review", 0)}
   147→    if potentials.get("concerns", 0) > 0:
   148→        merge_potentials_dict["concerns"] = potentials["concerns"]
   149→
   150→    diff = state_mod.merge_scan(
```

> TOOL

tool_use Grep
```json
{
  "pattern": "def generate_concerns|def make_issue.*detector",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 1 file
desloppify/engine/_concerns/generators.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/concerns/__init__.py"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/generators.py"
}
```

> TOOL

tool_result Read
```
1→"""Concern generators bridging mechanical findings to holistic review cues."""
     2→
     3→from __future__ import annotations
     4→
     5→from collections import defaultdict
     6→from typing import Any
     7→
     8→from desloppify.base.registry import JUDGMENT_DETECTORS
     9→from desloppify.engine._state.schema import StateModel
    10→
    11→from .constants import MIN_FILES_FOR_SMELL_PATTERN, MIN_FILES_FOR_SYSTEMIC
    12→from .signals import _extract_signals, _has_elevated_signals
    13→from .state import _group_by_file, _open_issues
    14→from .text import _build_evidence, _build_question, _build_summary, _classify
    15→from .types import Concern
    16→from .utils import _fingerprint, _is_dismissed
    17→
    18→
    19→def _try_make_concern(
    20→    *,
    21→    concern_type: str,
    22→    file: str,
    23→    fp_keys: tuple[str, ...],
    24→    all_ids: tuple[str, ...],
    25→    dismissals: dict[str, Any],
    26→    summary: str,
    27→    evidence: tuple[str, ...],
    28→    question: str,
    29→    fp_file: str | None = None,
    30→) -> Concern | None:
    31→    """Create a concern unless a matching dismissal exists."""
    32→    fp = _fingerprint(concern_type, fp_file if fp_file is not None else file, fp_keys)
    33→    if _is_dismissed(dismissals, fp, all_ids):
    34→        return None
    35→    return Concern(
    36→        type=concern_type,
    37→        file=file,
    38→        summary=summary,
    39→        evidence=evidence,
    40→        question=question,
    41→        fingerprint=fp,
    42→        source_issues=all_ids,
    43→    )
    44→
    45→
    46→def _file_concerns(state: StateModel, dismissals: dict[str, Any]) -> list[Concern]:
    47→    """Build per-file concerns from aggregated judgment detector signals."""
    48→    by_file = _group_by_file(state)
    49→    concerns: list[Concern] = []
    50→
    51→    for file, all_issues in by_file.items():
    52→        judgment = [
    53→            finding
    54→            for finding in all_issues
    55→            if finding.get("detector", "") in JUDGMENT_DETECTORS
    56→        ]
    57→        if not judgment:
    58→            continue
    59→
    60→        judgment_dets = {finding.get("detector", "") for finding in judgment}
    61→        elevated = _has_elevated_signals(judgment)
    62→
    63→        mechanical_count = len(all_issues)
    64→        if len(judgment_dets) < 2 and not elevated:
    65→            if not (len(judgment_dets) >= 1 and mechanical_count >= 3):
    66→                continue
    67→
    68→        signals = _extract_signals(judgment)
    69→        concern_type = _classify(judgment_dets, signals)
    70→        all_ids = tuple(sorted(finding.get("id", "") for finding in judgment))
    71→        fp_keys = tuple(sorted(judgment_dets))
    72→
    73→        concern = _try_make_concern(
    74→            concern_type=concern_type,
    75→            file=file,
    76→            fp_keys=fp_keys,
    77→            all_ids=all_ids,
    78→            dismissals=dismissals,
    79→            summary=_build_summary(concern_type, judgment_dets, signals),
    80→            evidence=_build_evidence(judgment, signals),
    81→            question=_build_question(judgment_dets, signals),
    82→        )
    83→        if concern is not None:
    84→            concerns.append(concern)
    85→
    86→    return concerns
    87→
    88→
    89→def _cross_file_patterns(state: StateModel, dismissals: dict[str, Any]) -> list[Concern]:
    90→    """Build systemic concerns for detector-combo patterns across files."""
    91→    by_file = _group_by_file(state)
    92→
    93→    profile_to_files: dict[frozenset[str], list[str]] = defaultdict(list)
    94→    for file, issues in by_file.items():
    95→        detectors = frozenset(
    96→            finding.get("detector", "")
    97→            for finding in issues
    98→            if finding.get("detector", "") in JUDGMENT_DETECTORS
    99→        )
   100→        if len(detectors) >= 2:
   101→            profile_to_files[detectors].append(file)
   102→
   103→    concerns: list[Concern] = []
   104→    for det_combo, files in profile_to_files.items():
   105→        if len(files) < MIN_FILES_FOR_SYSTEMIC:
   106→            continue
   107→
   108→        sorted_files = sorted(files)
   109→        combo_names = tuple(sorted(det_combo))
   110→        all_ids = tuple(
   111→            sorted(
   112→                finding.get("id", "")
   113→                for file in sorted_files
   114→                for finding in by_file[file]
   115→                if finding.get("detector", "") in det_combo
   116→            )
   117→        )
   118→        concern = _try_make_concern(
   119→            concern_type="systemic_pattern",
   120→            file=sorted_files[0],
   121→            fp_file=",".join(sorted_files[:5]),
   122→            fp_keys=combo_names,
   123→            all_ids=all_ids,
   124→            dismissals=dismissals,
   125→            summary=(
   126→                f"{len(files)} files share the same problem pattern "
   127→                f"({', '.join(combo_names)})"
   128→            ),
   129→            evidence=(
   130→                f"Affected files: {', '.join(sorted_files[:10])}",
   131→                f"Shared detectors: {', '.join(combo_names)}",
   132→                f"Total files: {len(files)}",
   133→            ),
   134→            question=(
   135→                f"These {len(files)} files all have the same combination "
   136→                f"of issues ({', '.join(combo_names)}). Is this a systemic "
   137→                "pattern that should be addressed at the architecture level "
   138→                "(shared base class, framework change, lint rule), or are "
   139→                "these independent issues that happen to look similar?"
   140→            ),
   141→        )
   142→        if concern is not None:
   143→            concerns.append(concern)
   144→
   145→    return concerns
   146→
   147→
   148→def _systemic_smell_patterns(
   149→    state: StateModel,
   150→    dismissals: dict[str, Any],
   151→) -> list[Concern]:
   152→    """Build systemic concerns when a single smell appears across many files."""
   153→    smell_files: dict[str, list[str]] = defaultdict(list)
   154→    smell_ids_map: dict[str, list[str]] = defaultdict(list)
   155→
   156→    for finding in _open_issues(state):
   157→        if finding.get("detector") != "smells":
   158→            continue
   159→        detail = finding.get("detail", {})
   160→        smell_id = detail.get("smell_id", "") if isinstance(detail, dict) else ""
   161→        filepath = finding.get("file", "")
   162→        if smell_id and filepath and filepath != ".":
   163→            smell_files[smell_id].append(filepath)
   164→            smell_ids_map[smell_id].append(finding.get("id", ""))
   165→
   166→    concerns: list[Concern] = []
   167→    for smell_id, files in smell_files.items():
   168→        unique_files = sorted(set(files))
   169→        if len(unique_files) < MIN_FILES_FOR_SMELL_PATTERN:
   170→            continue
   171→
   172→        all_ids = tuple(sorted(smell_ids_map[smell_id]))
   173→        concern = _try_make_concern(
   174→            concern_type="systemic_smell",
   175→            file=unique_files[0],
   176→            fp_file=smell_id,
   177→            fp_keys=(smell_id,),
   178→            all_ids=all_ids,
   179→            dismissals=dismissals,
   180→            summary=(
   181→                f"'{smell_id}' appears in {len(unique_files)} files — "
   182→                "likely a systemic pattern"
   183→            ),
   184→            evidence=(
   185→                f"Smell: {smell_id}",
   186→                f"Affected files ({len(unique_files)}): {', '.join(unique_files[:10])}",
   187→            ),
   188→            question=(
   189→                f"The smell '{smell_id}' appears across {len(unique_files)} files. "
   190→                "Is this a codebase-wide convention that should be addressed "
   191→                "systemically (lint rule, shared utility, architecture change), "
   192→                "or are these independent occurrences?"
   193→            ),
   194→        )
   195→        if concern is not None:
   196→            concerns.append(concern)
   197→
   198→    return concerns
   199→
   200→
   201→_GENERATORS = [_file_concerns, _cross_file_patterns, _systemic_smell_patterns]
   202→
   203→
   204→def generate_concerns(state: StateModel) -> list[Concern]:
   205→    """Run all concern generators against current state."""
   206→    dismissals = state.get("concern_dismissals", {})
   207→    concerns: list[Concern] = []
   208→    seen_fingerprints: set[str] = set()
   209→
   210→    for generator in _GENERATORS:
   211→        for concern in generator(state, dismissals):
   212→            if concern.fingerprint not in seen_fingerprints:
   213→                seen_fingerprints.add(concern.fingerprint)
   214→                concerns.append(concern)
   215→
   216→    concerns.sort(key=lambda concern: (concern.type, concern.file))
   217→    return concerns
   218→
   219→
   220→def cleanup_stale_dismissals(state: StateModel) -> int:
   221→    """Remove concern dismissals whose source issues all disappeared."""
   222→    dismissals = state.get("concern_dismissals", {})
   223→    if not dismissals:
   224→        return 0
   225→    open_ids = {finding.get("id", "") for finding in _open_issues(state)}
   226→    stale_fingerprints = [
   227→        fingerprint
   228→        for fingerprint, entry in dismissals.items()
   229→        if entry.get("source_issue_ids")
   230→        and not any(source_id in open_ids for source_id in entry["source_issue_ids"])
   231→    ]
   232→    for fingerprint in stale_fingerprints:
   233→        del dismissals[fingerprint]
   234→    return len(stale_fingerprints)
   235→
   236→
   237→__all__ = [
   238→    "_cross_file_patterns",
   239→    "_file_concerns",
   240→    "cleanup_stale_dismissals",
   241→    "generate_concerns",
   242→]
   243→
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns -type f -name \"*.py\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/signals.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/constants.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/types.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/generators.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/utils.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/text.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_concerns/state.py
```

> AGENT

Now let me check how concerns get converted to issues and stored:

> TOOL

tool_use Grep
```json
{
  "pattern": "concerns.*issue|issue.*detector.*concerns",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/importing",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 2 files
desloppify/intelligence/review/importing/holistic.py
desloppify/intelligence/review/importing/holistic_issue_flow.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/importing/*issue*.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/importing/holistic_issue_flow.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/importing/holistic_issue_flow.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1→"""Issue validation and stale-resolution helpers for holistic review imports."""
     2→
     3→from __future__ import annotations
     4→
     5→import hashlib
     6→from typing import Any
     7→
     8→from desloppify.engine._state.filtering import make_issue
     9→from desloppify.engine._state.schema import Issue, StateModel
    10→from desloppify.intelligence.review.dimensions import normalize_dimension_name
    11→from desloppify.intelligence.review.importing.contracts_types import (
    12→    ReviewIssuePayload,
    13→    ReviewScopePayload,
    14→)
    15→from desloppify.intelligence.review.importing.contracts_validation import (
    16→    validate_review_issue_payload,
    17→)
    18→from desloppify.intelligence.review.importing.payload import (
    19→    normalize_review_confidence,
    20→    review_tier,
    21→)
    22→from desloppify.intelligence.review.importing.resolution import (
    23→    auto_resolve_review_issues,
    24→)
    25→
    26→_POSITIVE_PREFIXES = (
    27→    "good ",
    28→    "well ",
    29→    "strong ",
    30→    "clean ",
    31→    "excellent ",
    32→    "nice ",
    33→    "solid ",
    34→)
    35→
    36→
    37→def _build_holistic_detail(
    38→    *,
    39→    content_hash: str,
    40→    dimension: str,
    41→    related_files: list[str],
    42→    evidence: list[str],
    43→    suggestion: str,
    44→    reasoning: str,
    45→) -> dict[str, Any]:
    46→    detail: dict[str, Any] = {
    47→        "holistic": True,
    48→        "dimension": dimension,
    49→        "related_files": related_files,
    50→        "evidence": evidence,
    51→        "suggestion": suggestion,
    52→        "reasoning": reasoning,
    53→    }
    54→    detail["summary_hash"] = content_hash
    55→    return detail
    56→
    57→
    58→def validate_and_build_issues(
    59→    issues_list: list[ReviewIssuePayload],
    60→    holistic_prompts: dict[str, Any],
    61→    lang_name: str,
    62→) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    63→    """Validate raw holistic issues and build state-ready issue dicts.
    64→
    65→    Returns (review_issues, skipped, dismissed_concerns).
    66→    """
    67→    review_issues: list[dict[str, Any]] = []
    68→    skipped: list[dict[str, Any]] = []
    69→    dismissed_concerns: list[dict[str, Any]] = []
    70→    allowed_dimensions = {
    71→        dim for dim in holistic_prompts if isinstance(dim, str) and dim.strip()
    72→    }
    73→
    74→    for idx, raw_issue in enumerate(issues_list):
    75→        issue, issue_errors = validate_review_issue_payload(
    76→            raw_issue,
    77→            label=f"issues[{idx}]",
    78→            allowed_dimensions=allowed_dimensions,
    79→            allow_dismissed=True,
    80→        )
    81→        if issue_errors:
    82→            skipped.append(
    83→                {
    84→                    "index": idx,
    85→                    "missing": issue_errors,
    86→                    "identifier": (
    87→                        raw_issue.get("identifier", "<none>")
    88→                        if isinstance(raw_issue, dict)
    89→                        else "<none>"
    90→                    ),
    91→                }
    92→            )
    93→            continue
    94→        if issue is None:
    95→            raise ValueError(
    96→                "review issue payload missing after validation succeeded"
    97→            )
    98→
    99→        if issue.get("concern_verdict") == "dismissed":
   100→            fingerprint = issue.get("concern_fingerprint", "")
   101→            if fingerprint:
   102→                dismissed_concerns.append(
   103→                    {
   104→                        "fingerprint": fingerprint,
   105→                        "concern_type": issue.get("concern_type", ""),
   106→                        "concern_file": issue.get("concern_file", ""),
   107→                        "reasoning": issue.get("reasoning", ""),
   108→                    }
   109→                )
   110→            continue
   111→
   112→        summary_text = str(issue.get("summary", ""))
   113→        if summary_text.lower().startswith(_POSITIVE_PREFIXES):
   114→            skipped.append(
   115→                {
   116→                    "index": idx,
   117→                    "missing": ["positive observation (not a defect)"],
   118→                    "identifier": issue.get("identifier", "<none>"),
   119→                }
   120→            )
   121→            continue
   122→
   123→        dimension = issue["dimension"]
   124→
   125→        is_confirmed_concern = issue.get("concern_verdict") == "confirmed"
   126→        detector = "concerns" if is_confirmed_concern else "review"
   127→
   128→        content_hash = hashlib.sha256(summary_text.encode()).hexdigest()[:8]
   129→        detail = _build_holistic_detail(
   130→            content_hash=content_hash,
   131→            dimension=dimension,
   132→            related_files=issue["related_files"],
   133→            evidence=issue["evidence"],
   134→            suggestion=issue.get("suggestion", ""),
   135→            reasoning=issue.get("reasoning", ""),
   136→        )
   137→        if is_confirmed_concern:
   138→            detail["concern_type"] = issue.get("concern_type", "")
   139→            detail["concern_verdict"] = "confirmed"
   140→
   141→        prefix = "concern" if is_confirmed_concern else "holistic"
   142→        issue_file = issue.get("concern_file", "") if is_confirmed_concern else ""
   143→        confidence = normalize_review_confidence(issue.get("confidence", "low"))
   144→        imported = make_issue(
   145→            detector=detector,
   146→            file=issue_file,
   147→            name=f"{prefix}::{dimension}::{issue['identifier']}",
   148→            tier=review_tier(confidence, holistic=True),
   149→            confidence=confidence,
   150→            summary=summary_text,
   151→            detail=detail,
   152→        )
   153→        imported["lang"] = lang_name
   154→        review_issues.append(imported)
   155→
   156→    return review_issues, skipped, dismissed_concerns
   157→
   158→
   159→def collect_imported_dimensions(
   160→    *,
   161→    issues_list: list[ReviewIssuePayload],
   162→    review_issues: list[dict[str, Any]],
   163→    assessments: dict[str, Any] | None,
   164→    review_scope: ReviewScopePayload | dict[str, Any] | None,
   165→    valid_dimensions: set[str],
   166→) -> set[str]:
   167→    """Return normalized dimensions this import explicitly covered."""
   168→    imported_dimensions: set[str] = set()
   169→
   170→    if isinstance(review_scope, dict):
   171→        scope_dims = review_scope.get("imported_dimensions")
   172→        if isinstance(scope_dims, list):
   173→            for raw_dim in scope_dims:
   174→                normalized = normalize_dimension_name(str(raw_dim))
   175→                if normalized in valid_dimensions:
   176→                    imported_dimensions.add(normalized)
   177→
   178→    for issue in issues_list:
   179→        if not isinstance(issue, dict):
   180→            continue
   181→        normalized = normalize_dimension_name(str(issue.get("dimension", "")))
   182→        if normalized in valid_dimensions:
   183→            imported_dimensions.add(normalized)
   184→
   185→    for issue in review_issues:
   186→        detail = issue.get("detail")
   187→        if not isinstance(detail, dict):
   188→            continue
   189→        normalized = normalize_dimension_name(str(detail.get("dimension", "")))
   190→        if normalized in valid_dimensions:
   191→            imported_dimensions.add(normalized)
   192→
   193→    for raw_dim in (assessments or {}):
   194→        normalized = normalize_dimension_name(str(raw_dim))
   195→        if normalized in valid_dimensions:
   196→            imported_dimensions.add(normalized)
   197→
   198→    return imported_dimensions
   199→
   200→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "def.*build_issues|concerns.*detector|detector.*concerns",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/importing",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 2 files
desloppify/intelligence/review/importing/holistic.py
desloppify/intelligence/review/importing/holistic_issue_flow.py
```

> AGENT

Perfect! Now let me search for how the "review" detector issues are created and the actual ID format:

> TOOL

tool_use Grep
```json
{
  "pattern": "holistic::|concern::|review::",
  "type": "python",
  "output_mode": "content",
  "head_limit": 40
}
```

> TOOL

tool_result Grep
```
desloppify/tests/engine/test_sync_split_modules_direct.py:165:        "queue_order": ["review::live", "review::stale", "smells::keep"],
desloppify/tests/engine/test_sync_split_modules_direct.py:166:        "deferred": ["review::stale", "smells::keep"],
desloppify/tests/engine/test_sync_split_modules_direct.py:167:        "promoted_ids": ["review::stale", "smells::keep"],
desloppify/tests/engine/test_sync_split_modules_direct.py:169:            "manual/review": {"issue_ids": ["review::live", "review::stale"]},
desloppify/tests/engine/test_sync_split_modules_direct.py:172:        "epic_triage_meta": {"triaged_ids": ["review::live"]},
desloppify/tests/engine/test_sync_split_modules_direct.py:176:    monkeypatch.setattr(reconcile_import_mod, "compute_open_issue_ids", lambda _s: {"review::live"})
desloppify/tests/engine/test_sync_split_modules_direct.py:189:    assert result.stale_pruned_from_queue == ["review::stale"]
desloppify/tests/engine/test_sync_split_modules_direct.py:190:    assert plan["queue_order"] == ["review::live", "smells::keep"]
desloppify/tests/engine/test_sync_split_modules_direct.py:192:    assert "review::stale" not in plan["skipped"]
desloppify/tests/engine/test_sync_split_modules_direct.py:195:    assert plan["clusters"]["manual/review"]["issue_ids"] == ["review::live"]
desloppify/tests/engine/test_sync_split_modules_direct.py:203:        "queue_order": ["review::live", "review::stale"],
desloppify/tests/engine/test_sync_split_modules_direct.py:206:            "triaged_ids": ["review::live", "review::stale"],
desloppify/tests/engine/test_sync_split_modules_direct.py:207:            "active_triage_issue_ids": ["review::live", "review::stale"],
desloppify/tests/engine/test_sync_split_modules_direct.py:208:            "undispositioned_issue_ids": ["review::live", "review::stale"],
desloppify/tests/engine/test_sync_split_modules_direct.py:214:    monkeypatch.setattr(reconcile_import_mod, "compute_open_issue_ids", lambda _s: {"review::live"})
desloppify/tests/engine/test_sync_split_modules_direct.py:225:    assert result.stale_pruned_from_queue == ["review::stale"]
desloppify/tests/engine/test_sync_split_modules_direct.py:226:    assert plan["epic_triage_meta"]["triaged_ids"] == ["review::live", "review::stale"]
desloppify/tests/engine/test_sync_split_modules_direct.py:227:    assert plan["epic_triage_meta"]["active_triage_issue_ids"] == ["review::live"]
desloppify/tests/engine/test_sync_split_modules_direct.py:228:    assert plan["epic_triage_meta"]["undispositioned_issue_ids"] == ["review::live"]
desloppify/tests/engine/test_sync_split_modules_direct.py:447:    plan = {"queue_order": ["triage::observe", "review::x"]}
desloppify/tests/engine/test_sync_split_modules_direct.py:490:        "queue_order": ["workflow::import-scores", "review::x"],
desloppify/tests/engine/test_sync_split_modules_direct.py:516:    assert plan["queue_order"] == ["review::x"]
desloppify/tests/engine/test_sync_split_modules_direct.py:757:            "review::src/a.py::naming": {
desloppify/tests/engine/test_sync_split_modules_direct.py:758:                "id": "review::src/a.py::naming",
desloppify/tests/engine/test_sync_split_modules_direct.py:785:    assert "review::src/a.py::naming" in {item["id"] for item in review_snapshot.backlog_items}
desloppify/tests/engine/test_sync_split_modules_direct.py:804:            "epic_triage_meta": {"triaged_ids": ["review::src/a.py::naming"]},
desloppify/tests/engine/test_sync_split_modules_direct.py:808:    assert [item["id"] for item in post_triage_snapshot.execution_items] == ["review::src/a.py::naming"]
desloppify/tests/engine/test_defer_policy_and_scope_direct.py:15:        deferred_ids={" review::b ", "review::a", ""},
desloppify/tests/engine/test_defer_policy_and_scope_direct.py:17:    assert created["deferred_ids"] == ["review::a", "review::b"]
desloppify/tests/engine/test_defer_policy_and_scope_direct.py:24:        deferred_ids={"review::a", "review::b"},
desloppify/tests/engine/test_defer_policy_and_scope_direct.py:31:            "deferred_ids": ["review::a"],
desloppify/tests/engine/test_defer_policy_and_scope_direct.py:40:            "deferred_ids": ["review::a"],
desloppify/tests/engine/test_defer_policy_and_scope_direct.py:49:            "deferred_ids": ["review::a"],
desloppify/tests/narrative/test_recovered_state_headline.py:13:        "review::src/foo.ts::abcd1234": {
desloppify/tests/narrative/test_recovered_state_headline.py:14:            "id": "review::src/foo.ts::abcd1234",
desloppify/tests/narrative/test_recovered_state_headline.py:19:        "review::src/bar.ts::efgh5678": {
desloppify/tests/narrative/test_recovered_state_headline.py:20:            "id": "review::src/bar.ts::efgh5678",
desloppify/tests/plan/test_stale_policy.py:185:                "review::a": {"status": "fixed", "detector": "review"},
desloppify/tests/plan/test_stale_policy.py:227:                "review::b": {"status": "open", "detector": "review"},
desloppify/tests/plan/test_stale_policy.py:231:        # Only review::b and concerns::c should be in the hash

[Showing results with pagination = limit: 40, offset: 0]
```

> TOOL

tool_use Grep
```json
{
  "pattern": "stale_policy|stale_ids",
  "type": "python",
  "output_mode": "files_with_matches",
  "head_limit": 20
}
```

> TOOL

tool_result Grep
```
Found 18 files limit: 20, offset: 0
desloppify/engine/_plan/policy/subjective.py
desloppify/tests/engine/test_sync_split_modules_direct.py
desloppify/tests/plan/test_stale_policy.py
desloppify/tests/plan/test_auto_cluster_subjective_lifecycle.py
desloppify/tests/plan/test_auto_cluster.py
desloppify/tests/commands/review/test_review_importing_support_direct.py
desloppify/engine/_plan/sync/workflow.py
desloppify/engine/_plan/sync/triage.py
desloppify/engine/_plan/reconcile_review_import.py
desloppify/engine/_plan/policy/stale.py
desloppify/app/commands/scan/plan_reconcile.py
desloppify/app/commands/review/importing/plan_sync.py
desloppify/engine/_plan/auto_cluster_sync.py
desloppify/tests/plan/test_stale_dimensions.py
desloppify/tests/plan/test_auto_cluster_sync_direct.py
desloppify/tests/commands/test_queue_order_guard.py
desloppify/engine/_plan/sync/dimensions.py
desloppify/tests/plan/test_subjective_policy.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/policy/stale.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1→"""Canonical stale/unscored subjective policy helpers."""
     2→
     3→from __future__ import annotations
     4→
     5→import hashlib
     6→
     7→from desloppify.base.config import DEFAULT_TARGET_STRICT_SCORE
     8→from desloppify.engine._state.schema import StateModel
     9→from desloppify.engine._work_queue.helpers import slugify
    10→from desloppify.engine.planning.scorecard_projection import all_subjective_entries
    11→
    12→_REVIEW_DETECTORS = ("review", "concerns")
    13→
    14→
    15→def open_review_ids(state: StateModel) -> set[str]:
    16→    """Return IDs of open review/concerns issues from state."""
    17→    return {
    18→        fid
    19→        for fid, f in state.get("issues", {}).items()
    20→        if f.get("status") == "open" and f.get("detector") in _REVIEW_DETECTORS
    21→    }
    22→
    23→
    24→def _subjective_entry_id(
    25→    dimension_key: object,
    26→    *,
    27→    subjective_prefix: str,
    28→) -> str:
    29→    return f"{subjective_prefix}{slugify(str(dimension_key))}"
    30→
    31→
    32→def _subjective_entries(state: StateModel) -> list[dict]:
    33→    dim_scores = state.get("dimension_scores", {}) or {}
    34→    if not dim_scores:
    35→        return []
    36→    return list(all_subjective_entries(state, dim_scores=dim_scores))
    37→
    38→
    39→def _collect_subjective_entry_ids(
    40→    entries: list[dict],
    41→    *,
    42→    subjective_prefix: str,
    43→    predicate,
    44→) -> set[str]:
    45→    collected: set[str] = set()
    46→    for entry in entries:
    47→        dim_key = entry.get("dimension_key", "")
    48→        if not dim_key or not predicate(entry):
    49→            continue
    50→        collected.add(_subjective_entry_id(dim_key, subjective_prefix=subjective_prefix))
    51→    return collected
    52→
    53→
    54→def current_stale_ids(
    55→    state: StateModel,
    56→    *,
    57→    subjective_prefix: str = "subjective::",
    58→) -> set[str]:
    59→    """Return ``subjective::<slug>`` IDs that are currently stale."""
    60→    return _collect_subjective_entry_ids(
    61→        _subjective_entries(state),
    62→        subjective_prefix=subjective_prefix,
    63→        predicate=lambda entry: bool(entry.get("stale")),
    64→    )
    65→
    66→
    67→def _unscored_ids_from_assessments(
    68→    assessments: dict,
    69→    *,
    70→    subjective_prefix: str,
    71→) -> set[str]:
    72→    unscored: set[str] = set()
    73→    for dim_key, payload in assessments.items():
    74→        if not isinstance(payload, dict) or not payload.get("placeholder") or not dim_key:
    75→            continue
    76→        unscored.add(_subjective_entry_id(dim_key, subjective_prefix=subjective_prefix))
    77→    return unscored
    78→
    79→
    80→def _unscored_ids_from_dimension_scores(
    81→    entries: list[dict],
    82→    *,
    83→    subjective_prefix: str,
    84→) -> set[str]:
    85→    return _collect_subjective_entry_ids(
    86→        entries,
    87→        subjective_prefix=subjective_prefix,
    88→        predicate=lambda entry: bool(entry.get("placeholder")),
    89→    )
    90→
    91→
    92→def current_unscored_ids(
    93→    state: StateModel,
    94→    *,
    95→    subjective_prefix: str = "subjective::",
    96→) -> set[str]:
    97→    """Return ``subjective::<slug>`` IDs that are currently unscored."""
    98→    assessments = state.get("subjective_assessments")
    99→    if isinstance(assessments, dict) and assessments:
   100→        return _unscored_ids_from_assessments(
   101→            assessments,
   102→            subjective_prefix=subjective_prefix,
   103→        )
   104→    return _unscored_ids_from_dimension_scores(
   105→        _subjective_entries(state),
   106→        subjective_prefix=subjective_prefix,
   107→    )
   108→
   109→
   110→def current_under_target_ids(
   111→    state: StateModel,
   112→    *,
   113→    target_strict: float = DEFAULT_TARGET_STRICT_SCORE,
   114→    subjective_prefix: str = "subjective::",
   115→) -> set[str]:
   116→    """Return under-target subjective IDs that are neither stale nor unscored."""
   117→    entries = _subjective_entries(state)
   118→    if not entries:
   119→        return set()
   120→
   121→    stale_ids = current_stale_ids(state, subjective_prefix=subjective_prefix)
   122→    unscored_ids = current_unscored_ids(state, subjective_prefix=subjective_prefix)
   123→
   124→    return {
   125→        item_id
   126→        for item_id in _collect_subjective_entry_ids(
   127→            entries,
   128→            subjective_prefix=subjective_prefix,
   129→            predicate=lambda entry: (
   130→                not entry.get("placeholder")
   131→                and not entry.get("stale")
   132→                and float(entry.get("strict", entry.get("score", 100.0))) < target_strict
   133→            ),
   134→        )
   135→        if item_id not in stale_ids and item_id not in unscored_ids
   136→    }
   137→
   138→
   139→def review_issue_snapshot_hash(state: StateModel) -> str:
   140→    """Hash open review/concerns issue IDs to detect triage-relevant changes."""
   141→    review_ids = sorted(open_review_ids(state))
   142→    if not review_ids:
   143→        return ""
   144→    return hashlib.sha256("|".join(review_ids).encode()).hexdigest()[:16]
   145→
   146→
   147→def compute_new_issue_ids(plan: dict, state: StateModel) -> set[str]:
   148→    """Return open review/concerns IDs that appeared since the last triage."""
   149→    meta = plan.get("epic_triage_meta", {})
   150→    triaged = set(meta.get("triaged_ids", []))
   151→    active = set(meta.get("active_triage_issue_ids", []))
   152→    known = triaged | active
   153→    return open_review_ids(state) - known if known else set()
   154→
   155→
   156→def is_triage_stale(
   157→    plan: dict,
   158→    state: StateModel,
   159→) -> bool:
   160→    """Return True when genuinely new review issues appeared since last triage.
   161→
   162→    In-progress triage (confirmed stages + stage IDs in queue) is NOT
   163→    considered stale — the lifecycle filter in the work queue already
   164→    forces triage stages to the front.
   165→    """
   166→    meta = plan.get("epic_triage_meta", {})
   167→    triaged_ids = set(meta.get("triaged_ids", []))
   168→    active_ids = set(meta.get("active_triage_issue_ids", []))
   169→    known = triaged_ids | active_ids
   170→    return bool(open_review_ids(state) - known)
   171→
   172→
   173→__all__ = [
   174→    "compute_new_issue_ids",
   175→    "current_stale_ids",
   176→    "current_under_target_ids",
   177→    "current_unscored_ids",
   178→    "is_triage_stale",
   179→    "open_review_ids",
   180→    "review_issue_snapshot_hash",
   181→]
   182→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "review::|concerns::|subjective_assessment|subjective::",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/policy",
  "type": "python",
  "output_mode": "content",
  "head_limit": 30
}
```

> TOOL

tool_result Grep
```
desloppify/engine/_plan/policy/subjective.py:22:    "review", "concerns", "subjective_review", "subjective_assessment",
desloppify/engine/_plan/policy/subjective.py:32:    unscored_ids: frozenset[str]  # subjective::* IDs needing initial review
desloppify/engine/_plan/policy/subjective.py:33:    stale_ids: frozenset[str]  # subjective::* IDs needing re-review
desloppify/engine/_plan/policy/stale.py:57:    subjective_prefix: str = "subjective::",
desloppify/engine/_plan/policy/stale.py:59:    """Return ``subjective::<slug>`` IDs that are currently stale."""
desloppify/engine/_plan/policy/stale.py:95:    subjective_prefix: str = "subjective::",
desloppify/engine/_plan/policy/stale.py:97:    """Return ``subjective::<slug>`` IDs that are currently unscored."""
desloppify/engine/_plan/policy/stale.py:98:    assessments = state.get("subjective_assessments")
desloppify/engine/_plan/policy/stale.py:114:    subjective_prefix: str = "subjective::",

[Showing results with pagination = limit: 30, offset: 0]
```

> AGENT

Excellent. Now let me search for actual issue ID formats and prefix usage:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"prefix.*=.*\\\"review::|prefix.*=.*\\\"concern::|prefix.*=.*\\\"subjective\" --include=\"*.py\" | head -20"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Grep
```json
{
  "pattern": "name=f\\\"|name.*=.*prefix",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/importing",
  "type": "python",
  "output_mode": "content",
  "head_limit": 30
}
```

> TOOL

tool_result Grep
```
desloppify/intelligence/review/importing/holistic_issue_flow.py:147:            name=f"{prefix}::{dimension}::{issue['identifier']}",
desloppify/intelligence/review/importing/per_file.py:121:            name=f"{dimension}::{issue['identifier']}",

[Showing results with pagination = limit: 30, offset: 0]
```

> AGENT

Perfect! Let me now check the per_file issue generation to understand file-scoped review issues:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/importing/per_file.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1→"""Per-file review issue import workflow."""
     2→
     3→from __future__ import annotations
     4→
     5→import hashlib
     6→from pathlib import Path
     7→from typing import Any
     8→
     9→from desloppify.engine._state.filtering import make_issue
    10→from desloppify.engine._state.merge import MergeScanOptions, merge_scan
    11→from desloppify.engine._state.schema import StateModel, utc_now
    12→from desloppify.intelligence.review.dimensions.data import load_dimensions_for_lang
    13→from desloppify.intelligence.review.importing.assessments import store_assessments
    14→from desloppify.intelligence.review.importing.cache import (
    15→    refresh_review_file_cache,
    16→    resolve_import_project_root,
    17→)
    18→from desloppify.intelligence.review.importing.contracts_types import (
    19→    ReviewImportPayload,
    20→    ReviewIssuePayload,
    21→)
    22→from desloppify.intelligence.review.importing.payload import (
    23→    ReviewImportEnvelope,
    24→    normalize_review_confidence,
    25→    parse_review_import_payload,
    26→    review_tier,
    27→)
    28→from desloppify.intelligence.review.importing.resolution import (
    29→    auto_resolve_review_issues,
    30→)
    31→from desloppify.intelligence.review.importing.state_helpers import (
    32→    ensure_lang_potentials,
    33→)
    34→from desloppify.intelligence.review.selection import hash_file
    35→
    36→
    37→def parse_per_file_import_payload(
    38→    data: ReviewImportPayload | dict[str, Any],
    39→) -> tuple[list[ReviewIssuePayload], dict[str, Any] | None]:
    40→    """Parse strict per-file import payload object."""
    41→    payload = parse_review_import_payload(data, mode_name="Per-file")
    42→    return payload.issues, payload.assessments
    43→
    44→
    45→def _absolutize_review_path(file_path: str, *, project_root: Path) -> str:
    46→    """Return a stable absolute file path for per-file review import matching."""
    47→    candidate = Path(file_path)
    48→    if candidate.is_absolute():
    49→        return str(candidate.resolve())
    50→    return str((project_root / candidate).resolve())
    51→
    52→
    53→def _resolve_per_file_project_root(project_root: Path | str | None) -> Path:
    54→    """Resolve import root for per-file review imports."""
    55→    return resolve_import_project_root(project_root)
    56→
    57→
    58→def import_review_issues(
    59→    issues_data: ReviewImportPayload,
    60→    state: StateModel,
    61→    lang_name: str,
    62→    *,
    63→    project_root: Path | str | None = None,
    64→    utc_now_fn=utc_now,
    65→) -> dict[str, Any]:
    66→    """Import agent-produced per-file review issues into state."""
    67→    payload: ReviewImportEnvelope = parse_review_import_payload(
    68→        issues_data, mode_name="Per-file"
    69→    )
    70→    issues_list = payload.issues
    71→    assessments = payload.assessments
    72→    reviewed_files = payload.reviewed_files
    73→    resolved_project_root = _resolve_per_file_project_root(project_root)
    74→    if assessments:
    75→        store_assessments(
    76→            state,
    77→            assessments,
    78→            source="per_file",
    79→            utc_now_fn=utc_now_fn,
    80→        )
    81→
    82→    _, per_file_prompts, _ = load_dimensions_for_lang(lang_name)
    83→    required_fields = ("file", "dimension", "identifier", "summary", "confidence")
    84→
    85→    review_issues: list[dict[str, Any]] = []
    86→    skipped: list[dict[str, Any]] = []
    87→
    88→    for idx, issue in enumerate(issues_list):
    89→        missing = [key for key in required_fields if key not in issue]
    90→        if missing:
    91→            skipped.append(
    92→                {
    93→                    "index": idx,
    94→                    "missing": missing,
    95→                    "identifier": issue.get("identifier", "<none>"),
    96→                }
    97→            )
    98→            continue
    99→
   100→        confidence = normalize_review_confidence(issue.get("confidence", "low"))
   101→
   102→        dimension = issue["dimension"]
   103→        if dimension not in per_file_prompts:
   104→            skipped.append(
   105→                {
   106→                    "index": idx,
   107→                    "missing": [f"invalid dimension: {dimension}"],
   108→                    "identifier": issue.get("identifier", "<none>"),
   109→                }
   110→            )
   111→            continue
   112→
   113→        content_hash = hashlib.sha256(issue["summary"].encode()).hexdigest()[:8]
   114→        imported_file = _absolutize_review_path(
   115→            str(issue["file"]),
   116→            project_root=resolved_project_root,
   117→        )
   118→        imported = make_issue(
   119→            detector="review",
   120→            file=imported_file,
   121→            name=f"{dimension}::{issue['identifier']}",
   122→            tier=review_tier(confidence, holistic=False),
   123→            confidence=confidence,
   124→            summary=issue["summary"],
   125→            detail={
   126→                "dimension": dimension,
   127→                "evidence": issue.get("evidence", []),
   128→                "suggestion": issue.get("suggestion", ""),
   129→                "reasoning": issue.get("reasoning", ""),
   130→                "evidence_lines": issue.get("evidence_lines", []),
   131→                "content_hash": content_hash,
   132→            },
   133→        )
   134→        imported["lang"] = lang_name
   135→        review_issues.append(imported)
   136→
   137→    # Build accepted-file set from successfully imported issues only,
   138→    # not from all issues_list entries (which may include invalid dimensions).
   139→    valid_reviewed_files_abs = {
   140→        issue["file"] for issue in review_issues
   141→    }
   142→    valid_reviewed_files = valid_reviewed_files_abs
   143→    reviewed_files_rel = {
   144→        str(file_path).strip()
   145→        for file_path in reviewed_files
   146→        if isinstance(file_path, str) and file_path.strip()
   147→    }
   148→    reviewed_files_abs = {
   149→        _absolutize_review_path(file_path, project_root=resolved_project_root)
   150→        for file_path in reviewed_files_rel
   151→    }
   152→    review_potential_files = valid_reviewed_files | {
   153→        *reviewed_files_rel,
   154→        *reviewed_files_abs,
   155→    }
   156→
   157→    potentials = ensure_lang_potentials(state, lang_name)
   158→    potentials["review"] = len(review_potential_files)
   159→
   160→    diff = merge_scan(
   161→        state,
   162→        review_issues,
   163→        options=MergeScanOptions(
   164→            lang=lang_name,
   165→            potentials={"review": potentials.get("review", 0)},
   166→            merge_potentials=True,
   167→        ),
   168→    )
   169→
   170→    new_ids = {issue["id"] for issue in review_issues}
   171→    reimported_files = valid_reviewed_files
   172→    auto_resolve_review_issues(
   173→        state,
   174→        new_ids=new_ids,
   175→        diff=diff,
   176→        note="not reported in latest per-file re-import",
   177→        should_resolve=lambda issue: (
   178→            issue.get("detector") == "review"
   179→            and not issue.get("detail", {}).get("holistic")
   180→            and issue.get("file", "") in reimported_files
   181→        ),
   182→        utc_now_fn=utc_now_fn,
   183→    )
   184→
   185→    if skipped:
   186→        diff["skipped"] = len(skipped)
   187→        diff["skipped_details"] = skipped
   188→
   189→    update_review_cache(
   190→        state,
   191→        issues_list,
   192→        reviewed_files=reviewed_files,
   193→        project_root=resolved_project_root,
   194→        utc_now_fn=utc_now_fn,
   195→    )
   196→    return diff
   197→
   198→
   199→def update_review_cache(
   200→    state: StateModel,
```

> TOOL

tool_use Grep
```json
{
  "pattern": "class.*Queue|QueueItem.*Issue|build.*queue",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 6 files
desloppify/engine/_work_queue/selection.py
desloppify/engine/_work_queue/snapshot.py
desloppify/engine/_work_queue/types.py
desloppify/engine/_work_queue/core.py
desloppify/engine/_work_queue/models.py
desloppify/engine/_work_queue/context.py
```

> AGENT

Now let me check how narrative and action engine use these detector strings:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/narrative/action_engine_routing.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1→"""Action routing and prioritization helpers for narrative actions."""
     2→
     3→from __future__ import annotations
     4→
     5→from collections.abc import Callable
     6→from typing import Any
     7→
     8→from desloppify.engine._scoring.results.core import get_dimension_for_detector
     9→from desloppify.intelligence.narrative._constants import DETECTOR_TOOLS
    10→from desloppify.intelligence.narrative.action_models import ActionItem
    11→
    12→
    13→def _dimension_name(detector: str) -> str:
    14→    """Resolve user-facing dimension name for a detector."""
    15→    dimension = get_dimension_for_detector(detector)
    16→    return dimension.name if dimension else "Unknown"
    17→
    18→
    19→def _append_reorganize_actions(
    20→    actions: list[ActionItem],
    21→    by_detector: dict[str, int],
    22→    impact_for: Callable[[str, int], float],
    23→) -> None:
    24→    """Append structure/move oriented actions."""
    25→    for detector, tool_info in DETECTOR_TOOLS.items():
    26→        if tool_info["action_type"] != "reorganize":
    27→            continue
    28→        count = by_detector.get(detector, 0)
    29→        if count == 0:
    30→            continue
    31→
    32→        guidance = tool_info.get("guidance", "restructure with move")
    33→        actions.append(
    34→            {
    35→                "type": "reorganize",
    36→                "detector": detector,
    37→                "count": count,
    38→                "description": f"{count} {detector} issues — {guidance}",
    39→                "command": f"desloppify show {detector} --status open",
    40→                "impact": round(impact_for(detector, count), 1),
    41→                "dimension": _dimension_name(detector),
    42→            }
    43→        )
    44→
    45→
    46→def _build_refactor_entry(
    47→    detector: str,
    48→    tool_info: dict[str, Any],
    49→    count: int,
    50→    impact_for: Callable[[str, int], float],
    51→) -> ActionItem:
    52→    """Build one refactor/manual action row."""
    53→    guidance = tool_info.get("guidance", "manual fix")
    54→    adjusted_info = {**tool_info, "guidance": guidance}
    55→
    56→    if detector == "subjective_review":
    57→        command = "desloppify review --prepare"
    58→        suffix = "s" if count != 1 else ""
    59→        description = (
    60→            f"{count} subjective dimension{suffix} need review — run holistic "
    61→            "review to refresh subjective scores"
    62→        )
    63→    elif detector == "review":
    64→        command = "desloppify show review --status open"
    65→        suffix = "s" if count != 1 else ""
    66→        description = (
    67→            f"{count} review issue{suffix} need investigation — "
    68→            "run `desloppify show review --status open` to see them"
    69→        )
    70→        adjusted_info = {**adjusted_info, "action_type": "refactor"}
    71→    else:
    72→        command = f"desloppify show {detector} --status open"
    73→        description = f"{count} {detector} issues — {guidance}"
    74→
    75→    return {
    76→        "type": adjusted_info["action_type"],
    77→        "detector": detector,
    78→        "count": count,
    79→        "description": description,
    80→        "command": command,
    81→        "impact": round(impact_for(detector, count), 1),
    82→        "dimension": _dimension_name(detector),
    83→    }
    84→
    85→
    86→def _append_refactor_actions(
    87→    actions: list[ActionItem],
    88→    by_detector: dict[str, int],
    89→    impact_for: Callable[[str, int], float],
    90→) -> None:
    91→    """Append refactor/manual actions after auto-fix/reorg buckets."""
    92→    for detector, tool_info in DETECTOR_TOOLS.items():
    93→        if tool_info["action_type"] not in {"refactor", "manual_fix"}:
    94→            continue
    95→        count = by_detector.get(detector, 0)
    96→        if count == 0:
    97→            continue
    98→        actions.append(_build_refactor_entry(detector, tool_info, count, impact_for))
    99→
   100→
   101→def _append_debt_action(actions: list[ActionItem], debt: dict[str, float]) -> None:
   102→    """Append wontfix-debt callout when gap is material."""
   103→    gap = float(debt.get("overall_gap", 0.0) or 0.0)
   104→    if gap <= 2.0:
   105→        return
   106→    actions.append(
   107→        {
   108→            "type": "debt_review",
   109→            "detector": None,
   110→            "description": f"{gap} pts of wontfix debt — review stale decisions",
   111→            "command": "desloppify show --status wontfix",
   112→            "gap": gap,
   113→        }
   114→    )
   115→
   116→
   117→def _assign_priorities(actions: list[ActionItem]) -> list[ActionItem]:
   118→    """Sort and assign sequential priorities."""
   119→    type_order = {
   120→        "issue_queue": 0,
   121→        "auto_fix": 1,
   122→        "reorganize": 2,
   123→        "refactor": 3,
   124→        "manual_fix": 4,
   125→        "debt_review": 5,
   126→    }
   127→    actions.sort(
   128→        key=lambda action: (type_order.get(action["type"], 9), -action.get("impact", 0))
   129→    )
   130→    for index, action in enumerate(actions, start=1):
   131→        action["priority"] = index
   132→    return actions
   133→
   134→
   135→def _cluster_detector(cluster: dict) -> str | None:
   136→    """Extract the primary detector from a cluster."""
   137→    key = cluster.get("cluster_key", "")
   138→    if key:
   139→        parts = key.split("::")
   140→        if len(parts) >= 2:
   141→            return parts[1]
   142→    name = cluster.get("name", "")
   143→    if name.startswith("auto/"):
   144→        rest = name[5:]
   145→        return rest.split("-", 1)[0] if "-" in rest else rest
   146→    return None
   147→
   148→
   149→def _annotate_with_clusters(actions: list[ActionItem], clusters: dict | None) -> None:
   150→    """Annotate actions with matching cluster info when clusters exist."""
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/narrative/signals.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1→"""Shared narrative signal computation helpers."""
     2→
     3→from __future__ import annotations
     4→
     5→from pathlib import Path
     6→
     7→from desloppify.base.config import (
     8→    DEFAULT_TARGET_STRICT_SCORE,
     9→    MAX_TARGET_STRICT_SCORE,
    10→    MIN_TARGET_STRICT_SCORE,
    11→)
    12→from desloppify.base.config import (
    13→    load_config as _load_config,
    14→)
    15→from desloppify.base.discovery.paths import get_project_root
    16→from desloppify.intelligence.narrative._constants import STRUCTURAL_MERGE
    17→from desloppify.intelligence.narrative.types import (
    18→    BadgeStatus,
    19→    PrimaryAction,
    20→    RiskFlag,
    21→    StrictTarget,
    22→    VerificationStep,
    23→)
    24→from desloppify.engine._state.filtering import path_scoped_issues
    25→from desloppify.state_io import Issue, StateModel
    26→from desloppify.state_scoring import score_snapshot as state_score_snapshot
    27→
    28→_RISK_SEVERITY_ORDER = {
    29→    "critical": 0,
    30→    "high": 1,
    31→    "medium": 2,
    32→    "low": 3,
    33→    "info": 4,
    34→}
    35→
    36→_HIGH_IGNORE_SUPPRESSION_THRESHOLD = 30.0
    37→_WONTFIX_GAP_THRESHOLD = 1.0
    38→
    39→
    40→def resolve_target_strict_score(config: dict | None) -> tuple[int, str | None]:
    41→    """Resolve strict-score target from config with bounded fallback."""
    42→    raw_target = DEFAULT_TARGET_STRICT_SCORE
    43→    if isinstance(config, dict):
    44→        raw_target = config.get("target_strict_score", DEFAULT_TARGET_STRICT_SCORE)
    45→    try:
    46→        target = int(raw_target)
    47→    except (TypeError, ValueError):
    48→        return (
    49→            DEFAULT_TARGET_STRICT_SCORE,
    50→            (
    51→                f"Invalid config `target_strict_score={raw_target!r}`; using "
    52→                f"{DEFAULT_TARGET_STRICT_SCORE}"
    53→            ),
    54→        )
    55→    if target < MIN_TARGET_STRICT_SCORE or target > MAX_TARGET_STRICT_SCORE:
    56→        return (
    57→            DEFAULT_TARGET_STRICT_SCORE,
    58→            (
    59→                f"Invalid config `target_strict_score={raw_target!r}`; using "
    60→                f"{DEFAULT_TARGET_STRICT_SCORE}"
    61→            ),
    62→        )
    63→    return target, None
    64→
    65→
    66→def compute_strict_target(strict_score: float | None, config: dict | None) -> StrictTarget:
    67→    """Build strict-target context for command rendering and agents."""
    68→    target, warning = resolve_target_strict_score(config)
    69→    if not isinstance(strict_score, int | float):
    70→        return {
    71→            "target": float(target),
    72→            "current": None,
    73→            "gap": None,
    74→            "state": "unavailable",
    75→            "warning": warning,
    76→        }
    77→
    78→    current = round(float(strict_score), 1)
    79→    gap = round(float(target) - current, 1)
    80→    if gap > 0:
    81→        state = "below"
    82→    elif gap < 0:
    83→        state = "above"
    84→    else:
    85→        state = "at"
    86→    return {
    87→        "target": float(target),
    88→        "current": current,
    89→        "gap": gap,
    90→        "state": state,
    91→        "warning": warning,
    92→    }
    93→
    94→
    95→def count_open_by_detector(issues: dict) -> dict[str, int]:
    96→    """Count open issues by detector, merging structural sub-detectors."""
    97→    by_detector: dict[str, int] = {}
    98→    for issue in issues.values():
    99→        if issue["status"] != "open" or issue.get("suppressed"):
   100→            continue
   101→        detector = issue.get("detector", "unknown")
   102→        if detector in STRUCTURAL_MERGE:
   103→            detector = "structural"
   104→        by_detector[detector] = by_detector.get(detector, 0) + 1
   105→        if detector == "review" and issue.get("detail", {}).get("holistic"):
   106→            by_detector["review_holistic"] = by_detector.get("review_holistic", 0) + 1
   107→    if by_detector.get("review", 0) > 0:
   108→        by_detector["review_uninvestigated"] = sum(
   109→            1
   110→            for issue in issues.values()
   111→            if issue.get("status") == "open"
   112→            and not issue.get("suppressed")
   113→            and issue.get("detector") == "review"
   114→            and not issue.get("detail", {}).get("investigation")
   115→        )
   116→    return by_detector
   117→
   118→
   119→def resolve_badge_path(project_root: Path) -> tuple[str, Path]:
   120→    """Resolve badge path from config, defaulting to root-level scorecard.png."""
   121→    default_rel = "scorecard.png"
   122→    config = {}
   123→    try:
   124→        config = _load_config()
   125→    except (AttributeError, OSError):
   126→        config = {}
   127→
   128→    raw_path = default_rel
   129→    if isinstance(config, dict):
   130→        config.setdefault("badge_path", default_rel)
   131→        configured = config.get("badge_path")
   132→        if isinstance(configured, str) and configured.strip():
   133→            raw_path = configured.strip()
   134→
   135→    path = Path(raw_path)
   136→    is_root_anchored = bool(path.root)
   137→    if not path.is_absolute() and not is_root_anchored:
   138→        return raw_path, project_root / path
   139→
   140→    try:
   141→        rel_path = str(path.relative_to(project_root))
   142→    except ValueError:
   143→        rel_path = str(path)
   144→    return rel_path, path
   145→
   146→
   147→def compute_badge_status() -> BadgeStatus:
   148→    """Check configured scorecard path and whether README references it."""
   149→    project_root = get_project_root()
   150→    scorecard_rel, scorecard_path = resolve_badge_path(project_root)
```

> AGENT

Now let me check how make_issue constructs IDs:

> TOOL

tool_use Grep
```json
{
  "pattern": "def make_issue",
  "type": "python",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 1 file
desloppify/engine/_state/filtering.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/filtering.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1→"""State filtering, ignore rules, and issue pattern matching."""
     2→
     3→from __future__ import annotations
     4→
     5→import fnmatch
     6→import re
     7→
     8→__all__ = [
     9→    "issue_in_scan_scope",
    10→    "open_scope_breakdown",
    11→    "path_scoped_issues",
    12→    "is_ignored",
    13→    "matched_ignore_pattern",
    14→    "remove_ignored_issues",
    15→    "add_ignore",
    16→    "make_issue",
    17→]
    18→
    19→from desloppify.base.discovery.file_paths import rel
    20→from desloppify.engine._state.schema import (
    21→    Issue,
    22→    StateModel,
    23→    ensure_state_defaults,
    24→    utc_now,
    25→    validate_state_invariants,
    26→)
    27→from desloppify.engine._state.scope import (
    28→    issue_in_scan_scope as _issue_in_scan_scope,
    29→)
    30→from desloppify.engine._state.scope import (
    31→    open_scope_breakdown as _open_scope_breakdown,
    32→)
    33→from desloppify.engine._state.scope import (
    34→    path_scoped_issues as _path_scoped_issues,
    35→)
    36→
    37→
    38→def _preserve_integrity_target(state: StateModel) -> float | None:
    39→    """Extract the current subjective integrity target so recompute doesn't erase it."""
    40→    integrity = state.get("subjective_integrity")
    41→    if not isinstance(integrity, dict):
    42→        return None
    43→    raw = integrity.get("target_score")
    44→    if raw is None:
    45→        return None
    46→    try:
    47→        return max(0.0, min(100.0, float(raw)))
    48→    except (TypeError, ValueError):
    49→        return None
    50→
    51→
    52→def path_scoped_issues(
    53→    issues: dict[str, Issue],
    54→    scan_path: str | None,
    55→) -> dict[str, Issue]:
    56→    """Filter issues to those within the given scan path."""
    57→    return _path_scoped_issues(issues, scan_path)
    58→
    59→
    60→def issue_in_scan_scope(file_path: str, scan_path: str | None) -> bool:
    61→    """Return True when a file path belongs to the active scan scope."""
    62→    return _issue_in_scan_scope(file_path, scan_path)
    63→
    64→
    65→def open_scope_breakdown(
    66→    issues: dict[str, Issue],
    67→    scan_path: str | None,
    68→    *,
    69→    detector: str | None = None,
    70→) -> dict[str, int]:
    71→    """Return open-issue counts split by in-scope vs out-of-scope carryover."""
    72→    return _open_scope_breakdown(
    73→        issues,
    74→        scan_path,
    75→        detector=detector,
    76→    )
    77→
    78→
    79→def is_ignored(issue_id: str, file: str, ignore_patterns: list[str]) -> bool:
    80→    """Check if a issue matches any ignore pattern (glob, ID prefix, or file path)."""
    81→    return matched_ignore_pattern(issue_id, file, ignore_patterns) is not None
    82→
    83→
    84→def matched_ignore_pattern(
    85→    issue_id: str, file: str, ignore_patterns: list[str]
    86→) -> str | None:
    87→    """Return the ignore pattern that matched, if any."""
    88→    for pattern in ignore_patterns:
    89→        if "*" in pattern:
    90→            target = issue_id if "::" in pattern else file
    91→            if fnmatch.fnmatch(target, pattern):
    92→                return pattern
    93→            continue
    94→
    95→        if "::" in pattern:
    96→            if issue_id.startswith(pattern):
    97→                return pattern
    98→            continue
    99→
   100→        raw_base = pattern.rstrip("/")
   101→        rel_base = rel(pattern).rstrip("/")
   102→        for base in (raw_base, rel_base):
   103→            if not base:
   104→                continue
   105→            if file == base or file.startswith(base + "/"):
   106→                return pattern
   107→
   108→    return None
   109→
   110→
   111→def remove_ignored_issues(state: StateModel, pattern: str) -> int:
   112→    """Suppress issues matching an ignore pattern. Returns count affected."""
   113→    ensure_state_defaults(state)
   114→    matched_ids = [
   115→        issue_id
   116→        for issue_id, issue in state["issues"].items()
   117→        if is_ignored(issue_id, issue["file"], [pattern])
   118→    ]
   119→    now = utc_now()
   120→    for issue_id in matched_ids:
   121→        issue = state["issues"][issue_id]
   122→        issue["suppressed"] = True
   123→        issue["suppressed_at"] = now
   124→        issue["suppression_pattern"] = pattern
   125→    from desloppify.engine._scoring.state_integration import (
   126→        recompute_stats as _recompute_stats,
   127→    )
   128→
   129→    _recompute_stats(
   130→        state,
   131→        scan_path=state.get("scan_path"),
   132→        subjective_integrity_target=_preserve_integrity_target(state),
   133→    )
   134→    validate_state_invariants(state)
   135→    return len(matched_ids)
   136→
   137→
   138→def add_ignore(state: StateModel, pattern: str) -> int:
   139→    """Add an ignore pattern and remove existing matching issues."""
   140→    ensure_state_defaults(state)
   141→    config = state.setdefault("config", {})
   142→    ignores = config.setdefault("ignore", [])
   143→    if pattern not in ignores:
   144→        ignores.append(pattern)
   145→    return remove_ignored_issues(state, pattern)
   146→
   147→
   148→def make_issue(
   149→    detector: str,
   150→    file: str,
   151→    name: str,
   152→    *,
   153→    tier: int,
   154→    confidence: str,
   155→    summary: str,
   156→    detail: dict | None = None,
   157→) -> Issue:
   158→    """Create a normalized issue dict with a stable ID."""
   159→    rfile = rel(file)
   160→    issue_id = f"{detector}::{rfile}::{name}" if name else f"{detector}::{rfile}"
   161→    now = utc_now()
   162→    return {
   163→        "id": issue_id,
   164→        "detector": detector,
   165→        "file": rfile,
   166→        "tier": tier,
   167→        "confidence": confidence,
   168→        "summary": summary,
   169→        "detail": detail or {},
   170→        "status": "open",
   171→        "note": None,
   172→        "first_seen": now,
   173→        "last_seen": now,
   174→        "resolved_at": None,
   175→        "reopen_count": 0,
   176→    }
   177→
   178→
   179→_HEX8_RE = re.compile(r'^[0-9a-f]{8}$')
   180→
   181→
   182→def _matches_issue_path(issue: dict[str, str], pattern: str) -> bool:
   183→    """Match against the issue's detector name or file path."""
   184→    return (
   185→        issue.get("detector") == pattern
   186→        or issue["file"] == pattern
   187→        or issue["file"].startswith(pattern.rstrip("/") + "/")
   188→    )
   189→
   190→
   191→def _matches_issue_name_segment(issue_id: str, pattern: str) -> bool:
   192→    """Match against the name segment of the issue ID.
   193→
   194→    For hashed IDs (detector::path::name::hex8), also match the descriptive
   195→    name (second-to-last segment).  Returns False for IDs without :: or
   196→    patterns containing ::.
   197→    """
   198→    if "::" in pattern or "::" not in issue_id:
   199→        return False
   200→    segments = issue_id.split("::")
```

> AGENT

Perfect! Now let me gather a comprehensive summary. Let me check a few more details about the queue and how items are marked:

> TOOL

tool_use Grep
```json
{
  "pattern": "is_review.*=|is_subjective.*=",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue",
  "type": "python",
  "output_mode": "content",
  "head_limit": 30
}
```

> TOOL

tool_result Grep
```
desloppify/engine/_work_queue/ranking.py:158:        item["is_review"] = is_review_issue(item)
desloppify/engine/_work_queue/ranking.py:159:        item["is_subjective"] = is_subjective_issue(item)
desloppify/engine/_work_queue/ranking_output.py:73:    is_subjective = bool(item.get("is_subjective"))
desloppify/engine/_work_queue/ranking_output.py:74:    is_review = bool(item.get("is_review"))

[Showing results with pagination = limit: 30, offset: 0]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1→"""Ranking and grouping helpers for work queue selection."""
     2→
     3→from __future__ import annotations
     4→
     5→import logging
     6→from typing import Any, cast
     7→
     8→from desloppify.base.registry import DETECTORS
     9→from desloppify.engine.plan_triage import TRIAGE_STAGE_ORDER
    10→from desloppify.engine._scoring.results.health import compute_health_breakdown
    11→from desloppify.engine._scoring.results.impact import get_dimension_for_detector
    12→from desloppify.engine._state.filtering import path_scoped_issues
    13→from desloppify.engine._state.schema import StateModel
    14→from desloppify.engine._work_queue.helpers import (
    15→    ACTION_TYPE_PRIORITY,
    16→    detail_dict,
    17→    is_review_issue,
    18→    is_subjective_issue,
    19→    primary_command_for_issue,
    20→    review_issue_weight,
    21→    scope_matches,
    22→    slugify,
    23→    status_matches,
    24→    supported_fixers_for_item,
    25→    workflow_stage_name,
    26→)
    27→from desloppify.engine._work_queue.ranking_output import (
    28→    group_queue_items,
    29→    item_explain,
    30→    subjective_score_value,
    31→)
    32→from desloppify.engine._work_queue.synthetic import subjective_strict_scores
    33→from desloppify.engine._work_queue.types import WorkQueueItem
    34→from desloppify.engine.planning.helpers import CONFIDENCE_ORDER
    35→
    36→logger = logging.getLogger(__name__)
    37→
    38→# Plan-aware sort tiers (item_sort_key)
    39→_TIER_PLANNED = 0   # Items with explicit plan position
    40→_TIER_EXISTING = 1  # Known items, natural ranking
    41→_TIER_NEW = 2       # Newly discovered items
    42→
    43→# Natural ranking groups (_natural_sort_key)
    44→_RANK_INITIAL_REVIEW = -3  # Unassessed subjective dimensions
    45→_RANK_WORKFLOW = -2         # Score checkpoints, create-plan
    46→_RANK_TRIAGE_STAGE = -1     # Epic triage workflow stages
    47→_RANK_CLUSTER = 0           # Auto-clustered issues
    48→_RANK_ISSUE = 1           # Individual issues + assessed subjective
    49→
    50→def _workflow_stage_index(item: WorkQueueItem) -> int:
    51→    raw_index = item.get("stage_index")
    52→    if raw_index is not None:
    53→        if isinstance(raw_index, int):
    54→            return raw_index
    55→        if isinstance(raw_index, str):
    56→            stripped = raw_index.strip()
    57→            if stripped.lstrip("-").isdigit():
    58→                return int(stripped)
    59→        logger.warning("Invalid workflow stage index %r", raw_index)
    60→    return TRIAGE_STAGE_ORDER.get(workflow_stage_name(item).lower(), 0)
    61→
    62→
    63→def enrich_with_impact(
    64→    items: list[WorkQueueItem], dimension_scores: dict[str, Any]
    65→) -> None:
    66→    """Stamp ``estimated_impact`` on each item based on dimension-level headroom.
    67→
    68→    Impact = ``overall_per_point * headroom`` where headroom = ``100 - score``.
    69→    Items in dimensions with more score headroom sort first.
    70→    """
    71→    if not dimension_scores:
    72→        for item in items:
    73→            item["estimated_impact"] = 0.0
    74→        return
    75→
    76→    breakdown = compute_health_breakdown(dimension_scores, score_key="strict")
    77→    entries = breakdown.get("entries", [])
    78→
    79→    # Build lookup: normalized dimension name -> {per_point, headroom}
    80→    dim_impact: dict[str, dict[str, float]] = {}
    81→    for entry in entries:
    82→        name = str(entry.get("name", "")).strip()
    83→        if not name:
    84→            continue
    85→        per_point = float(entry.get("overall_per_point", 0.0))
    86→        score = float(entry.get("score", 0.0))
    87→        headroom = 100.0 - score
    88→        dim_impact[name.lower()] = {"per_point": per_point, "headroom": headroom}
    89→
    90→    for item in items:
    91→        impact = _compute_item_impact(item, dim_impact, get_dimension_for_detector)
    92→        item["estimated_impact"] = impact
    93→
    94→
    95→def _compute_item_impact(
    96→    item: WorkQueueItem,
    97→    dim_impact: dict[str, dict[str, float]],
    98→    get_dimension_for_detector,
    99→) -> float:
   100→    """Compute impact value for a single queue item."""
   101→    kind = item.get("kind", "issue")
   102→
   103→    # Subjective items (synthetic dimensions or subjective issues):
   104→    # look up by detail.dimension_name
   105→    if kind == "subjective_dimension" or item.get("is_subjective"):
   106→        dim_name = detail_dict(item).get("dimension_name", "")
   107→        entry = dim_impact.get(dim_name.lower())
   108→        if entry:
   109→            return entry["per_point"] * entry["headroom"]
   110→        return 0.0
   111→
   112→    # Mechanical issues: use detector -> dimension mapping
   113→    detector = item.get("detector", "")
   114→    if detector:
   115→        dimension = get_dimension_for_detector(detector)
   116→        if dimension:
   117→            entry = dim_impact.get(dimension.name.lower())
   118→            if entry:
   119→                return entry["per_point"] * entry["headroom"]
   120→
   121→    return 0.0
   122→
   123→
   124→def build_issue_items(
   125→    state: StateModel,
   126→    *,
   127→    scan_path: str | None,
   128→    status_filter: str,
   129→    scope: str | None,
   130→    chronic: bool,
   131→) -> list[WorkQueueItem]:
   132→    scoped = path_scoped_issues(state.get("issues", {}), scan_path)
   133→    subjective_scores = subjective_strict_scores(state)
   134→    out: list[WorkQueueItem] = []
   135→
   136→    for issue_id, issue in scoped.items():
   137→        if issue.get("suppressed"):
   138→            continue
   139→        if not status_matches(issue.get("status", "open"), status_filter):
   140→            continue
   141→        if chronic and not (
   142→            issue.get("status") == "open" and issue.get("reopen_count", 0) >= 2
   143→        ):
   144→            continue
   145→
   146→        # Evidence-only: skip issues below standalone confidence threshold
   147→        detector = issue.get("detector", "")
   148→        meta = DETECTORS.get(detector)
   149→        if meta and meta.standalone_threshold:
   150→            threshold_rank = CONFIDENCE_ORDER.get(meta.standalone_threshold, 9)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1→"""Predicates and small utilities for work queue items."""
     2→
     3→from __future__ import annotations
     4→
     5→import re
     6→from fnmatch import fnmatch
     7→from typing import Any
     8→
     9→from desloppify.base.enums import issue_status_tokens
    10→from desloppify.base.registry import DETECTORS
    11→from desloppify.engine._state.schema import StateModel
    12→from desloppify.engine._work_queue.types import WorkQueueItem
    13→
    14→ALL_STATUSES = set(issue_status_tokens(include_all=True))
    15→ACTION_TYPE_PRIORITY = {"auto_fix": 0, "refactor": 1, "manual_fix": 2, "reorganize": 3}
    16→ATTEST_EXAMPLE = (
    17→    "I have actually [DESCRIBE THE CONCRETE CHANGE YOU MADE] "
    18→    "and I am not gaming the score by resolving without fixing."
    19→)
    20→
    21→
    22→def detail_dict(item: WorkQueueItem | dict[str, Any]) -> dict[str, Any]:
    23→    """Return issue detail as a dict; tolerate legacy/non-dict payloads."""
    24→    detail = item.get("detail")
    25→    return detail if isinstance(detail, dict) else {}
    26→
    27→
    28→def status_matches(item_status: str, status_filter: str) -> bool:
    29→    return status_filter == "all" or item_status == status_filter
    30→
    31→
    32→def is_subjective_issue(item: WorkQueueItem | dict[str, Any]) -> bool:
    33→    detector = item.get("detector")
    34→    return detector in {"subjective_assessment", "holistic_review", "subjective_review"}
    35→
    36→
    37→def is_review_issue(item: WorkQueueItem | dict[str, Any]) -> bool:
    38→    return item.get("detector") == "review"
    39→
    40→
    41→def is_subjective_queue_item(item: WorkQueueItem | dict[str, Any]) -> bool:
    42→    """True for subjective work items, including collapsed subjective clusters."""
    43→    if item.get("kind") == "subjective_dimension":
    44→        return True
    45→    if item.get("kind") == "cluster":
    46→        members = item.get("members", [])
    47→        return bool(members) and all(
    48→            m.get("kind") == "subjective_dimension" for m in members
    49→        )
    50→    return False
    51→
    52→
    53→def review_issue_weight(item: WorkQueueItem | dict[str, Any]) -> float:
    54→    """Return review issue weight aligned with issues list ordering."""
    55→    confidence = str(item.get("confidence", "low")).lower()
    56→    weight_by_confidence = {
    57→        "high": 1.0,
    58→        "medium": 0.7,
    59→        "low": 0.3,
    60→    }
    61→    weight = weight_by_confidence.get(confidence, 0.3)
    62→    if detail_dict(item).get("holistic"):
    63→        weight *= 10.0
    64→    return float(weight)
    65→
    66→
    67→def scope_matches(item: WorkQueueItem | dict[str, Any], scope: str | None) -> bool:
    68→    """Apply show-style pattern matching against a queue item."""
    69→    if not scope:
    70→        return True
    71→
    72→    item_id = item.get("id", "")
    73→    detector = item.get("detector", "")
    74→    filepath = item.get("file", "")
    75→    summary = item.get("summary", "")
    76→    dimension = detail_dict(item).get("dimension_name", "")
    77→    kind = item.get("kind", "")
    78→
    79→    if "*" in scope:
    80→        return any(
    81→            fnmatch(candidate, scope)
    82→            for candidate in (item_id, filepath, detector, dimension, summary)
    83→        )
    84→
    85→    if "::" in scope:
    86→        return item_id.startswith(scope)
    87→
    88→    lowered = scope.lower()
    89→    if kind == "subjective_dimension":
    90→        return (
    91→            lowered in item_id.lower()
    92→            or lowered in dimension.lower()
    93→            or lowered in summary.lower()
    94→        )
    95→
    96→    # Hash suffix: 8+ hex chars matches the tail segment of a issue ID.
    97→    if len(lowered) >= 8 and re.fullmatch(r"[0-9a-f]+", lowered):
    98→        return item_id.lower().endswith("::" + lowered)
    99→
   100→    return (
   101→        detector == scope
   102→        or filepath == scope
   103→        or filepath.startswith(scope.rstrip("/") + "/")
   104→    )
   105→
   106→
   107→def workflow_stage_name(item: WorkQueueItem | dict[str, Any]) -> str:
   108→    """Resolve the triage stage name from an item, with fallbacks."""
   109→    stage_name = str(item.get("stage_name", "")).strip()
   110→    if stage_name:
   111→        return stage_name
   112→
   113→    stage_name = str(detail_dict(item).get("stage", "")).strip()
   114→    if stage_name:
   115→        return stage_name
   116→
   117→    item_id = str(item.get("id", "")).strip()
   118→    if item_id.startswith("triage::"):
   119→        return item_id.split("::", 1)[1]
   120→    return ""
   121→
   122→
   123→def slugify(text: str) -> str:
   124→    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")
   125→
   126→
   127→def supported_fixers_for_item(
   128→    state: StateModel, item: WorkQueueItem
   129→) -> set[str] | None:
   130→    """Return supported fixers for an item's language when known."""
   131→    lang = str(item.get("lang", "") or "").strip()
   132→    if not lang:
   133→        return None
   134→
   135→    caps_obj = state.get("lang_capabilities")
   136→    if not isinstance(caps_obj, dict):
   137→        return None
   138→    lang_caps_obj = caps_obj.get(lang)
   139→    if not isinstance(lang_caps_obj, dict):
   140→        return None
   141→
   142→    fixers = lang_caps_obj.get("fixers")
   143→    if not isinstance(fixers, list):
   144→        return None
   145→    return {fixer for fixer in fixers if isinstance(fixer, str)}
   146→
   147→
   148→def primary_command_for_issue(
   149→    item: WorkQueueItem, *, supported_fixers: set[str] | None = None
   150→) -> str:
```

> AGENT

Perfect! I now have a comprehensive understanding. Let me create a detailed summary document.

## Summary: Current Issue/Finding Semantics and Scattered Heuristics

Based on my thorough exploration of the codebase, here's a comprehensive breakdown of the current issue/finding semantics, detector classifications, and the scattered heuristics the plan aims to consolidate:

### 1. **Issue/Finding Type Definitions**

**Core Issue TypedDict** (`desloppify/engine/_state/schema_types_issues.py`):
- **`Issue`** – Central TypedDict with fields: `id`, `detector`, `file`, `tier`, `confidence`, `summary`, `detail` (dict), `status`, `note`, `first_seen`, `last_seen`, `resolved_at`, `reopen_count`, `suppressed`, `lang`, `zone`
- Issue IDs use a stable format: `{detector}::{file}::{name}` (constructed in `make_issue()`)
  - Example: `review::src/foo.ts::high_elegance::abc12345`
  - Example: `concern::src/foo.ts::design::id123`
  - Example: `subjective::mid_elegance` (synthetic dimension item)

**Assessment TypedDicts** (`desloppify/engine/_state/schema_types_review.py`):
- **`SubjectiveAssessment`** – Stores dimension scores with: `score`, `source`, `assessed_at`, `reset_by`, `placeholder`, `components`, `component_scores`, `integrity_penalty`, `provisional_override`, `stale_since`, `judgment` (narrative breakdown)
- **`SubjectiveIntegrity`** – Anti-gaming metadata: `status`, `target_score`, `matched_count`, `matched_dimensions`, `reset_dimensions`
- **`ConcernDismissal`** – Dismissed concern record: `dismissed_at`, `reason`, `dimension`, `reasoning`, `concern_type`, `concern_file`, `source_issue_ids`

**Concern Dataclass** (`desloppify/engine/_concerns/types.py`):
- **`Concern`** – Immutable dataclass with: `type` (e.g., "systemic_pattern", "systemic_smell"), `file`, `summary`, `evidence` (tuple), `question`, `fingerprint`, `source_issues` (tuple of issue IDs)

---

### 2. **NON_OBJECTIVE_DETECTORS Definition and Usage**

**Single Source of Truth**: `desloppify/engine/_plan/policy/subjective.py` line 21-23:
```python
NON_OBJECTIVE_DETECTORS: frozenset[str] = frozenset({
    "review", "concerns", "subjective_review", "subjective_assessment",
})
```

**Also defined (separately)** in `desloppify/engine/_scoring/policy/core.py` line 43-53 as `_NON_OBJECTIVE_DETECTORS`:
```python
_NON_OBJECTIVE_DETECTORS = frozenset({
    "concerns",
    "review",
    "subjective_review",
    "uncalled_functions",
    "unused_enums",
    "signature",
    "stale_wontfix",
})  # Note: wider set, includes some mechanical detectors
```

**Scattered Usage**:
- **Queue filtering** (`engine/_work_queue/snapshot.py` lines 90-95): Excludes non-objective items from `_is_objective_item()` check
- **Scoring** (`engine/_scoring/policy/core.py` line 69): Non-objective detectors get `dimension=None, tier=None`
- **Subjective visibility** (`engine/_plan/policy/subjective.py` line 121): Used in `compute_subjective_visibility()` to count only objective items for backlog blocking

**Semantic Switch Pattern**: Detector strings are hardcoded in multiple places as semantic switches rather than being looked up from a unified configuration.

---

### 3. **Detector Strings as Semantic Switches Throughout Codebase**

**Critical Semantic Switches**:

| Detector | Semantic Role | Files Using It |
|----------|---------------|-----------------|
| **"review"** | Per-file or holistic code review findings (non-mechanical) | `intelligence/review/importing/holistic_issue_flow.py`, `app/commands/review/`, `intelligence/narrative/` |
| **"concerns"** | Design concerns surfaced by mechanical signals (e.g., systemic patterns, file-level aggregations) | `engine/_concerns/generators.py`, `intelligence/review/importing/` |
| **"subjective_review"** | Legacy/alternate name for subjective dimension review items | `engine/_plan/policy/subjective.py`, `intelligence/narrative/action_engine_routing.py` |
| **"subjective_assessment"** | Synthetic dimension items injected into queue when below target | `engine/_work_queue/synthetic.py` line 254 |
| **"smells", "structural", "coupling"**, etc. | Mechanical (objective) detectors | Used in dimension scoring |

**Hardcoded Semantic Checks**:
- `intelligence/narrative/action_engine_routing.py` line 56: `if detector == "subjective_review":`
- `intelligence/narrative/signals.py` line 105: `if detector == "review" and issue.get("detail", {}).get("holistic"):`
- `engine/_work_queue/snapshot.py` line 101: `if item.get("detector", "") in {"review", "concerns", "subjective_review"}`
- `engine/_work_queue/helpers.py` line 34: `return detector in {"subjective_assessment", "holistic_review", "subjective_review"}`
- `engine/_work_queue/ranking.py` line 138: `if detector == "review":` (for impact computation)

**Pattern**: Detectors are used as string literals in conditionals to switch behavior, not through a unified registry or policy table.

---

### 4. **ID Prefix Usage for Semantic Inference**

**ID Prefix Formats**:
- **Review issues (holistic)**: `holistic::{dimension}::{identifier}` (set in `holistic_issue_flow.py` line 141)
- **Review issues (per-file)**: `review::{file}::{dimension}::{identifier}` or `{dimension}::{identifier}` 
- **Concern issues**: `concern::{dimension}::{identifier}` (set in `holistic_issue_flow.py` line 141)
- **Subjective dimension synthetic items**: `subjective::{slugified_dimension_name}` (set in `engine/_work_queue/synthetic.py` line 253)

**Semantic Inference from Prefixes**:
- `issue_id.startswith("subjective::")` → synthetic subjective dimension item (not a real issue)
- `issue_id.startswith("review::")` or `issue_id.startswith("concern::")` → review/concern issue (can infer must check triage state)
- `issue_id.startswith("triage::")` → workflow stage item (used in `engine/_work_queue/helpers.py` line 118)
- Prefix presence in ignore patterns: used for prefix matching in `engine/_state/filtering.py` line 95-98

**Current Inference Heuristics**:
- `stale_policy.py` lines 54-64: Checks `entry.get("stale")` flag on subjective entries → generates `subjective::*` IDs
- `stale_policy.py` lines 92-107: Checks `entry.get("placeholder")` → unscored `subjective::*` IDs
- Concern dismissal lookup: `fingerprint` in `state["concern_dismissals"]` is matched to source issue IDs

---

### 5. **Subjective Assessments Storage and Lifecycle**

**Persistent Storage** (`engine/_state/schema_types.py` line 70):
```python
subjective_assessments: Required[dict[str, SubjectiveAssessment]]
```

**Assessment Fields** (`engine/_state/schema_types_review.py` lines 27-43):
- `score`, `source`, `assessed_at`, `reset_by`, `placeholder` (unscored), `components`, `component_scores`
- `integrity_penalty` (from anti-gaming checks), `provisional_override`, `provisional_until_scan`, `needs_review_refresh`
- `stale_since` (when it became stale), `refresh_reason`, `judgment` (narrative breakdown with strengths/score_rationale)

**Stale/Unscored Logic** (`engine/_plan/policy/stale.py`):
- **Unscored IDs**: `current_unscored_ids()` checks `payload.get("placeholder")` or dimension has placeholder entry
- **Stale IDs**: `current_stale_ids()` checks `entry.get("stale")` flag
- **Under-target IDs**: `current_under_target_ids()` checks strict score < target, excluding stale/unscored

**Queue Injection Policy** (`engine/_plan/policy/subjective.py` lines 36-52):
- **Unscored**: Always injected (unconditional)
- **Stale**: Injected only when NO objective backlog exists
- **Under-target**: Injected only when NO objective backlog exists

---

### 6. **Queue/Work Queue Current Classification**

**WorkQueueItem Union** (`engine/_work_queue/types.py` lines 188-194):
```python
WorkQueueItem: TypeAlias = (
    IssueQueueItem
    | ClusterQueueItem
    | WorkflowStageItem
    | WorkflowActionItem
    | SubjectiveDimensionItem
)
```

**Kind Values** (`engine/_work_queue/types.py` line 7-13):
- `"issue"` – Regular detector issue
- `"cluster"` – Plan cluster (grouped issues)
- `"workflow_stage"` – Triage/workflow stage
- `"workflow_action"` – Synthetic actions (scan, import, etc.)
- `"subjective_dimension"` – Synthetic subjective dimension item

**Semantic Flags** (`engine/_work_queue/types.py` lines 50-52):
- `is_review: bool` – Set by `is_review_issue()` (detector == "review")
- `is_subjective: bool` – Set by `is_subjective_issue()` (detector in {"subjective_assessment", "holistic_review", "subjective_review"})

**Current Partitioning** (`engine/_work_queue/snapshot.py` lines 44-65):
- `all_objective_items`, `all_initial_review_items`, `all_postflight_review_items`
- `all_scan_items`, `all_postflight_workflow_items`, `all_postflight_triage_items`
- `execution_items`, `backlog_items`
- Metadata: `objective_execution_count`, `planned_objective_count`, `subjective_initial_count`, `subjective_postflight_count`

**Classification Logic** (`engine/_work_queue/snapshot.py` lines 90-102):
- Objective = kind in {"issue", "cluster"} AND detector NOT in NON_OBJECTIVE_DETECTORS AND not skipped
- Review issues = detector in {"review", "concerns", "subjective_review"}
- Execution vs backlog = based on plan queue_order presence

---

### 7. **Concern Generation and Persistence Model**

**Generators** (`engine/_concerns/generators.py`):
Three concern generators run in sequence:
1. **`_file_concerns()`** – Per-file concerns aggregating judgment detectors (multi-detector combos)
2. **`_cross_file_patterns()`** – Systemic concerns when same detector combo appears in 3+ files
3. **`_systemic_smell_patterns()`** – Systemic smell concerns when one smell_id appears in 5+ files (MIN_FILES_FOR_SYSTEMIC=5)

**Concern Types**:
- `"systemic_pattern"` – Same detector combo across multiple files
- `"systemic_smell"` – Same smell appearing in many files
- Implicit file-level type from signal classification

**Fingerprinting** (`engine/_concerns/utils.py`):
- `fingerprint = hash(concern_type, fp_file, fp_keys)` – Stable key for dismissal matching
- Dismissals stored in `state["concern_dismissals"][fingerprint]`

**Conversion to Issues** (`intelligence/review/importing/holistic_issue_flow.py` lines 99-154):
- Concerns with `concern_verdict == "confirmed"` become detector="concerns" issues
- Non-confirmed concerns become detector="review" issues
- Issue ID format: `concern::{dimension}::{identifier}` (confirmed) or `holistic::{dimension}::{identifier}` (review)
- File assignment: `issue_file = concern_file` (confirmed) or empty string (review)

**Dismissal Persistence** (`engine/_concerns/generators.py` line 204-217):
- On import, dismissed concerns are stored in `state["concern_dismissals"]`
- On generation, `_is_dismissed()` checks if fingerprint matches and source issues still exist
- Cleanup via `cleanup_stale_dismissals()` removes dismissals whose source issues resolved

---

### 8. **Key Scattered Heuristics the Plan Aims to Replace**

1. **Hardcoded detector string literals** – "review", "concerns", "subjective_review", "subjective_assessment" scattered throughout instead of unified registry lookup
2. **Dual NON_OBJECTIVE_DETECTORS definitions** – Policy defined in two places with different contents (subjective.py vs scoring/core.py)
3. **Prefix-based ID inference** – Semantic meaning loaded from ID prefixes ("review::", "subjective::", "concern::") rather than explicit type field
4. **Scattered queue classification logic** – Objective/subjective/review categorization embedded in multiple modules (snapshot.py, helpers.py, ranking.py) with inconsistent predicates
5. **Manual detector-dimension mapping** – `get_dimension_for_detector()` as separate registry instead of unified detector metadata
6. **Stale/unscored computation duplication** – Same logic spread across policy/stale.py, policy/subjective.py, and synthetic.py
7. **Narrative heuristics using detector strings** – action_engine_routing.py lines 56-70 special-casing "subjective_review" and "review" with hardcoded descriptions
8. **Evidence-only threshold logic** – `_is_evidence_only()` in subjective.py duplicates confidence ordering that could be centralized
9. **Concern dismissal lookup** – Manual fingerprint matching without unified concern identity model
10. **Subjective visibility injection logic** – Conditional queue injection (lines 36-52 in subjective.py) uses scattered flags rather than explicit state machine

---

### **Files with Scattered Heuristics (Priority for Consolidation)**

- `/engine/_plan/policy/subjective.py` – Core visibility policy
- `/engine/_plan/policy/stale.py` – Stale/unscored logic
- `/engine/_work_queue/snapshot.py` – Queue partitioning
- `/engine/_work_queue/helpers.py` – Predicate functions
- `/engine/_work_queue/ranking.py` – Impact/impact logic
- `/intelligence/narrative/action_engine_routing.py` – Action descriptions
- `/intelligence/narrative/signals.py` – Signal computation
- `/intelligence/review/importing/holistic_issue_flow.py` – Issue creation
- `/engine/_scoring/policy/core.py` – Scoring policy (duped NON_OBJECTIVE_DETECTORS)
- `/engine/_concerns/generators.py` – Concern generation and dismissal

All of these would benefit from a unified **Issue Classification Schema** and **Detector Metadata Registry** that the plan aims to design.

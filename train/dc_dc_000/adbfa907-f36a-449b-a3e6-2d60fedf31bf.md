> DEVELOPER

Find all import statements that reference `engine.planning.scorecard_projection` or `engine/planning/scorecard_projection` across the codebase under /Users/user_c042661f/Documents/desloppify/desloppify. Show full file paths and line content. Also check if `app/planning/` directory exists. Also check if any engine-layer file (under engine/) imports from scorecard_projection (excluding scorecard_projection.py itself).

> AGENT

I'll search for all references to `scorecard_projection` and check the directory structure.

> TOOL

tool_use Grep
```json
{
  "pattern": "scorecard_projection",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
desloppify/engine/_work_queue/synthetic.py:24:from desloppify.engine.planning.scorecard_projection import (
desloppify/engine/_plan/stale_policy.py:10:from desloppify.engine.planning.scorecard_projection import all_subjective_entries
desloppify/tests/scoring/test_scorecard_projection_direct.py:5:from desloppify.engine.planning.scorecard_projection import (
desloppify/app/commands/scan/reporting/agent_context.py:26:from desloppify.engine.planning import scorecard_projection as scorecard_projection_mod
desloppify/app/commands/scan/reporting/agent_context.py:81:    rows = scorecard_projection_mod.scorecard_dimension_rows(
desloppify/app/commands/scan/reporting/dimensions.py:20:from desloppify.engine.planning.scorecard_projection import (
desloppify/app/commands/next/cmd.py:34:from desloppify.engine.planning.scorecard_projection import (
desloppify/app/commands/next/render_support.py:10:from desloppify.engine.planning.scorecard_projection import (
desloppify/app/commands/status/render_dimensions.py:10:from desloppify.engine.planning.scorecard_projection import (
desloppify/app/commands/status/cmd.py:37:from desloppify.engine.planning.scorecard_projection import (
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/app/planning/**",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/engine/planning/**",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/helpers.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/queue_policy.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/scan.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/scorecard_policy.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/select.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/types.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render_sections.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render_items.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/__init__.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/helpers.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/scan.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/scorecard_policy.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/select.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/types.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/render_sections.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/queue_policy.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/render.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/render_items.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/dimension_rows.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/scorecard_projection.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/scorecard_projection.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__pycache__/dimension_rows.cpython-311.pyc
```

> AGENT

Now let me get more detailed information on each import:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/synthetic.py"
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
    11→from desloppify.engine._state.schema import StateModel
    12→from desloppify.engine._scoring.subjective.core import DISPLAY_NAMES
    13→from desloppify.engine._work_queue.helpers import (
    14→    detail_dict,
    15→    slugify,
    16→)
    17→from desloppify.engine._work_queue.synthetic_workflow import (
    18→    build_communicate_score_item,
    19→    build_create_plan_item,
    20→    build_import_scores_item,
    21→    build_score_checkpoint_item,
    22→)
    23→from desloppify.engine._work_queue.types import WorkQueueItem
    24→from desloppify.engine.planning.scorecard_projection import (
    25→    all_subjective_entries,
    26→)
    27→from desloppify.intelligence.integrity import (
    28→    unassessed_subjective_dimensions,
    29→)
    30→
    31→# ---------------------------------------------------------------------------
    32→# Dimension key normalization
    33→# ---------------------------------------------------------------------------
    34→
    35→def _canonical_subjective_dimension_key(display_name: str) -> str:
    36→    """Map a display label (e.g. 'Mid elegance') to its canonical dimension key."""
    37→    cleaned = display_name.replace(" (subjective)", "").strip()
    38→    target = cleaned.lower()
    39→
    40→    for dim_key, label in DISPLAY_NAMES.items():
    41→        if str(label).lower() == target:
    42→            return str(dim_key)
    43→    return slugify(cleaned)
    44→
    45→
    46→def _subjective_dimension_aliases(display_name: str) -> set[str]:
    47→    """Return normalized aliases used to match display labels with issue dimension keys."""
    48→    cleaned = display_name.replace(" (subjective)", "").strip()
    49→    canonical = _canonical_subjective_dimension_key(cleaned)
    50→    return {
    51→        cleaned.lower(),
    52→        cleaned.replace(" ", "_").lower(),
    53→        slugify(cleaned),
    54→        canonical.lower(),
    55→        slugify(canonical),
    56→    }
    57→
    58→
    59→# ---------------------------------------------------------------------------
    60→# Subjective strict scores
    61→# ---------------------------------------------------------------------------
    62→
    63→def subjective_strict_scores(state: StateModel | dict[str, Any]) -> dict[str, float]:
    64→    dim_scores = state.get("dimension_scores", {}) or {}
    65→    if not dim_scores:
    66→        return {}
    67→
    68→    entries = all_subjective_entries(state, dim_scores=dim_scores)
    69→    scores: dict[str, float] = {}
    70→    for entry in entries:
    71→        name = str(entry.get("name", "")).strip()
    72→        if not name:
    73→            continue
    74→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
    75→        [REDACTED](name)
    76→        aliases = _subjective_dimension_aliases(name)
    77→        for cli_key in entry.get("cli_keys", []):
    78→            key = str(cli_key).strip().lower()
    79→            if not key:
    80→                continue
    81→            aliases.add(key)
    82→            aliases.add(slugify(key))
    83→        aliases.add(dim_key.lower())
    84→        aliases.add(slugify(dim_key))
    85→        for alias in aliases:
    86→            scores[alias] = strict_val
    87→    return scores
    88→
    89→
    90→# ---------------------------------------------------------------------------
    91→# Synthetic item builders
    92→# ---------------------------------------------------------------------------
    93→
    94→def build_triage_stage_items(plan: dict, state: dict) -> list[WorkQueueItem]:
    95→    """Build synthetic work items for each ``triage::*`` stage ID in the queue.
    96→
    97→    Returns an empty list when no triage stages are pending.
    98→    """
    99→    from desloppify.app.commands.plan.triage_playbook import (
   100→        TRIAGE_STAGE_DEPENDENCIES,
   101→        TRIAGE_STAGE_LABELS,
   102→    )
   103→    from desloppify.engine._plan.stale_dimensions import (
   104→        TRIAGE_IDS,
   105→        TRIAGE_STAGE_IDS,
   106→    )
   107→
   108→    order = plan.get("queue_order", [])
   109→    order_set = set(order)
   110→    present = order_set & TRIAGE_IDS
   111→    if not present:
   112→        return []
   113→
   114→    meta = plan.get("epic_triage_meta", {})
   115→    confirmed = set(meta.get("triage_stages", {}).keys())
   116→
   117→    issues = state.get("issues", {})
   118→    open_review_count = sum(
   119→        1 for f in issues.values()
   120→        if f.get("status") == "open"
   121→        and f.get("detector") in ("review", "concerns")
   122→    )
   123→
   124→    label_map = dict(TRIAGE_STAGE_LABELS)
   125→    stage_names = ("observe", "reflect", "organize", "commit")
   126→
   127→    items: list[WorkQueueItem] = []
   128→    for sid, name in zip(TRIAGE_STAGE_IDS, stage_names, strict=False):
   129→        if sid not in present:
   130→            continue
   131→        if name in confirmed:
   132→            continue
   133→
   134→        # Compute blocked_by: dependency stages that are still in the queue
   135→        deps = TRIAGE_STAGE_DEPENDENCIES.get(name, set())
   136→        blocked_by = sorted(
   137→            f"triage::{dep}" for dep in deps
   138→            if f"triage::{dep}" in present and dep not in confirmed
   139→        )
   140→
   141→        cmd = f"desloppify plan triage --stage {name}"
   142→        if name == "commit":
   143→            cmd = 'desloppify plan triage --complete --strategy "..."'
   144→
   145→        item: WorkQueueItem = {
   146→            "id": sid,
   147→            "tier": 1,
   148→            "confidence": "high",
   149→            "detector": "triage",
   150→            "file": ".",
   151→            "kind": "workflow_stage",
   152→            "summary": f"Triage: {label_map.get(name, name)}",
   153→            "detail": {
   154→                "total_review_issues": open_review_count,
   155→                "stage": name,
   156→                "stage_label": label_map.get(name, name),
   157→            },
   158→            "blocked_by": blocked_by,
   159→            "is_blocked": bool(blocked_by),
   160→        }
   161→        item["primary_command"] = cmd
   162→        items.append(item)
   163→    return items
   164→
   165→
   166→def build_subjective_items(
   167→    state: dict, issues: dict, *, threshold: float = 100.0
   168→) -> list[WorkQueueItem]:
   169→    """Create synthetic subjective work items."""
   170→    dim_scores = state.get("dimension_scores", {}) or {}
   171→    if not dim_scores:
   172→        return []
   173→    threshold = max(0.0, min(100.0, float(threshold)))
   174→
   175→    subjective_entries = all_subjective_entries(state, dim_scores=dim_scores)
   176→    if not subjective_entries:
   177→        return []
   178→    unassessed_dims = {
   179→        str(name).strip()
   180→        for name in unassessed_subjective_dimensions(
   181→            dim_scores
   182→        )
   183→    }
   184→
   185→    # Review issues are keyed by raw dimension name (snake_case).
   186→    review_open_by_dim: dict[str, int] = {}
   187→    for issue in issues.values():
   188→        if issue.get("status") != "open":
   189→            continue
   190→        if issue.get("detector") == "review":
   191→            dim_key = str(detail_dict(issue).get("dimension", "")).strip().lower()
   192→            if dim_key:
   193→                review_open_by_dim[dim_key] = review_open_by_dim.get(dim_key, 0) + 1
   194→
   195→    items: list[WorkQueueItem] = []
   196→    def _prepare_command(
   197→        cli_keys: list[str],
   198→        *,
   199→        force_review_rerun: bool = False,
   200→    ) -> str:
   201→        command = "desloppify review --prepare"
   202→        if cli_keys:
   203→            command += " --dimensions " + ",".join(cli_keys)
   204→        if force_review_rerun:
   205→            command += " --force-review-rerun"
   206→        return command
   207→
   208→    for entry in subjective_entries:
   209→        name = str(entry.get("name", "")).strip()
   210→        if not name:
   211→            continue
   212→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
   213→        if strict_val >= threshold:
   214→            continue
   215→
   216→        [REDACTED](name)
   217→        aliases = set(_subjective_dimension_aliases(name))
   218→        cli_keys = [
   219→            str(key).strip().lower()
   220→            for key in entry.get("cli_keys", [])
   221→            if str(key).strip()
   222→        ]
   223→        aliases.update(cli_keys)
   224→        aliases.update(slugify(key) for key in cli_keys)
   225→        open_review = sum(review_open_by_dim.get(alias, 0) for alias in aliases)
   226→        is_unassessed = bool(entry.get("placeholder")) or (
   227→            name in unassessed_dims
   228→            or (strict_val <= 0.0 and int(entry.get("failing", 0)) == 0)
   229→        )
   230→        is_stale = bool(entry.get("stale"))
   231→        # If review issues already exist for this dimension, triage/fix them
   232→        # before suggesting another review refresh pass.
   233→        if open_review > 0:
   234→            primary_command = "desloppify show review --status open"
   235→        else:
   236→            primary_command = _prepare_command(cli_keys)
   237→        stale_tag = " [stale — re-review]" if is_stale else ""
   238→        summary = f"Subjective dimension below target: {name} ({strict_val:.1f}%){stale_tag}"
   239→        item: WorkQueueItem = {
   240→            "id": f"subjective::{slugify(dim_key)}",
   241→            "detector": "subjective_assessment",
   242→            "file": ".",
   243→            "confidence": "medium",
   244→            "summary": summary,
   245→            "detail": {
   246→                "dimension_name": name,
   247→                "dimension": dim_key,
   248→                "failing": int(entry.get("failing", 0)),
   249→                "strict_score": strict_val,
   250→                "open_review_issues": open_review,
   251→                "cli_keys": cli_keys,
   252→            },
   253→            "status": "open",
   254→            "kind": "subjective_dimension",
   255→        }
   256→        item["primary_command"] = primary_command
   257→        item["initial_review"] = is_unassessed
   258→        items.append(item)
   259→    return items
   260→
   261→
   262→__all__ = [
   263→    "build_communicate_score_item",
   264→    "build_create_plan_item",
   265→    "build_import_scores_item",
   266→    "build_score_checkpoint_item",
   267→    "build_subjective_items",
   268→    "build_triage_stage_items",
   269→    "subjective_strict_scores",
   270→]
   271→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/stale_policy.py"
}
```

> TOOL

tool_result Read
```
1→"""Pure policy helpers for stale/unscored subjective planning decisions."""
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
    15→def current_stale_ids(
    16→    state: StateModel,
    17→    *,
    18→    subjective_prefix: str = "subjective::",
    19→) -> set[str]:
    20→    """Return ``subjective::<slug>`` IDs that are currently stale."""
    21→    dim_scores = state.get("dimension_scores", {}) or {}
    22→    if not dim_scores:
    23→        return set()
    24→
    25→    stale: set[str] = set()
    26→    for entry in all_subjective_entries(state, dim_scores=dim_scores):
    27→        if not entry.get("stale"):
    28→            continue
    29→        dim_key = entry.get("dimension_key", "")
    30→        if dim_key:
    31→            stale.add(f"{subjective_prefix}{slugify(dim_key)}")
    32→    return stale
    33→
    34→
    35→def current_unscored_ids(
    36→    state: StateModel,
    37→    *,
    38→    subjective_prefix: str = "subjective::",
    39→) -> set[str]:
    40→    """Return ``subjective::<slug>`` IDs that are currently unscored."""
    41→    assessments = state.get("subjective_assessments")
    42→    if isinstance(assessments, dict) and assessments:
    43→        unscored: set[str] = set()
    44→        for dim_key, payload in assessments.items():
    45→            if not isinstance(payload, dict):
    46→                continue
    47→            if not payload.get("placeholder"):
    48→                continue
    49→            if dim_key:
    50→                unscored.add(f"{subjective_prefix}{slugify(dim_key)}")
    51→        return unscored
    52→
    53→    dim_scores = state.get("dimension_scores", {}) or {}
    54→    if not dim_scores:
    55→        return set()
    56→
    57→    unscored = set()
    58→    for data in dim_scores.values():
    59→        if not isinstance(data, dict):
    60→            continue
    61→        detectors = data.get("detectors", {})
    62→        meta = detectors.get("subjective_assessment")
    63→        if not isinstance(meta, dict):
    64→            continue
    65→        if not meta.get("placeholder"):
    66→            continue
    67→        dim_key = meta.get("dimension_key", "")
    68→        if dim_key:
    69→            unscored.add(f"{subjective_prefix}{slugify(dim_key)}")
    70→    return unscored
    71→
    72→
    73→def current_under_target_ids(
    74→    state: StateModel,
    75→    *,
    76→    target_strict: float = DEFAULT_TARGET_STRICT_SCORE,
    77→    subjective_prefix: str = "subjective::",
    78→) -> set[str]:
    79→    """Return under-target subjective IDs that are neither stale nor unscored."""
    80→    dim_scores = state.get("dimension_scores", {}) or {}
    81→    if not dim_scores:
    82→        return set()
    83→
    84→    stale_ids = current_stale_ids(state, subjective_prefix=subjective_prefix)
    85→    unscored_ids = current_unscored_ids(state, subjective_prefix=subjective_prefix)
    86→
    87→    under_target: set[str] = set()
    88→    for entry in all_subjective_entries(state, dim_scores=dim_scores):
    89→        if entry.get("placeholder") or entry.get("stale"):
    90→            continue
    91→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
    92→        if strict_val >= target_strict:
    93→            continue
    94→        dim_key = entry.get("dimension_key", "")
    95→        if not dim_key:
    96→            continue
    97→        item_id = f"{subjective_prefix}{slugify(dim_key)}"
    98→        if item_id not in stale_ids and item_id not in unscored_ids:
    99→            under_target.add(item_id)
   100→    return under_target
   101→
   102→
   103→def review_issue_snapshot_hash(state: StateModel) -> str:
   104→    """Hash open review/concerns issue IDs to detect triage-relevant changes."""
   105→    issues = state.get("issues", {})
   106→    review_ids = sorted(
   107→        issue_id
   108→        for issue_id, issue in issues.items()
   109→        if issue.get("status") == "open" and issue.get("detector") in _REVIEW_DETECTORS
   110→    )
   111→    if not review_ids:
   112→        return ""
   113→    return hashlib.sha256("|".join(review_ids).encode()).hexdigest()[:16]
   114→
   115→
   116→def compute_new_issue_ids(plan: dict, state: StateModel) -> set[str]:
   117→    """Return open review/concerns IDs that appeared since the last triage."""
   118→    meta = plan.get("epic_triage_meta", {})
   119→    triaged = set(meta.get("triaged_ids", []))
   120→    current = {
   121→        issue_id
   122→        for issue_id, issue in state.get("issues", {}).items()
   123→        if issue.get("status") == "open" and issue.get("detector") in _REVIEW_DETECTORS
   124→    }
   125→    return current - triaged if triaged else set()
   126→
   127→
   128→def is_triage_stale(
   129→    plan: dict,
   130→    state: StateModel,
   131→    *,
   132→    triage_ids: set[str] | frozenset[str] = frozenset(),
   133→) -> bool:
   134→    """Return True when triage should run because review work has changed."""
   135→    meta = plan.get("epic_triage_meta", {})
   136→
   137→    issues = state.get("issues", {})
   138→    current_review_ids = {
   139→        issue_id
   140→        for issue_id, issue in issues.items()
   141→        if issue.get("status") == "open" and issue.get("detector") in _REVIEW_DETECTORS
   142→    }
   143→    triaged_ids = set(meta.get("triaged_ids", []))
   144→    new_since_triage = current_review_ids - triaged_ids
   145→    if new_since_triage:
   146→        return True
   147→
   148→    confirmed = set(meta.get("triage_stages", {}).keys())
   149→    if confirmed:
   150→        order = set(plan.get("queue_order", []))
   151→        if order & set(triage_ids):
   152→            return True
   153→    return False
   154→
   155→
   156→__all__ = [
   157→    "compute_new_issue_ids",
   158→    "current_stale_ids",
   159→    "current_under_target_ids",
   160→    "current_unscored_ids",
   161→    "is_triage_stale",
   162→    "review_issue_snapshot_hash",
   163→]
   164→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/scoring/test_scorecard_projection_direct.py"
}
```

> TOOL

tool_result Read
```
1→"""Direct tests for scorecard projection helpers."""
     2→
     3→from __future__ import annotations
     4→
     5→from desloppify.engine.planning.scorecard_projection import (
     6→    dimension_cli_key,
     7→    scorecard_dimension_cli_keys,
     8→    scorecard_dimensions_payload,
     9→    scorecard_subjective_entries,
    10→)
    11→
    12→
    13→def test_dimension_cli_key_maps_display_name():
    14→    assert dimension_cli_key("Logic clarity") == "logic_clarity"
    15→    assert dimension_cli_key("Custom Dimension!") == "custom_dimension"
    16→
    17→
    18→def test_elegance_dimension_cli_keys_use_components():
    19→    keys = scorecard_dimension_cli_keys(
    20→        "Elegance",
    21→        {
    22→            "detectors": {
    23→                "subjective_assessment": {
    24→                    "components": ["High elegance", "Mid elegance"],
    25→                }
    26→            }
    27→        },
    28→    )
    29→    assert keys == ["high_level_elegance", "mid_level_elegance"]
    30→
    31→
    32→def test_abstraction_dimension_cli_keys_use_components():
    33→    keys = scorecard_dimension_cli_keys(
    34→        "Abstraction fit",
    35→        {
    36→            "detectors": {
    37→                "subjective_assessment": {
    38→                    "components": ["Abstraction Leverage", "Indirection Cost"],
    39→                }
    40→            }
    41→        },
    42→    )
    43→    assert keys == ["abstraction_fitness"]
    44→
    45→
    46→def test_scorecard_payload_includes_subjective_rows():
    47→    state = {
    48→        "scan_history": [{"lang": "python"}],
    49→        "dimension_scores": {
    50→            "File health": {
    51→                "score": 98.0,
    52→                "strict": 98.0,
    53→                "checks": 10,
    54→                "failing": 1,
    55→                "tier": 3,
    56→                "detectors": {"structural": {}},
    57→            },
    58→            "Naming quality": {
    59→                "score": 96.0,
    60→                "strict": 95.0,
    61→                "checks": 50,
    62→                "failing": 2,
    63→                "tier": 4,
    64→                "detectors": {
    65→                    "subjective_assessment": {
    66→                        "potential": 50,
    67→                        "pass_rate": 0.96,
    68→                        "failing": 2,
    69→                        "weighted_failures": 2.0,
    70→                        "components": [],
    71→                    }
    72→                },
    73→            },
    74→        },
    75→    }
    76→    entries = scorecard_subjective_entries(state)
    77→    assert any(entry["name"] == "Naming quality" for entry in entries)
    78→
    79→    payload = scorecard_dimensions_payload(state)
    80→    naming = next(row for row in payload if row["name"] == "Naming quality")
    81→    assert naming["subjective"] is True
    82→    assert naming["cli_keys"] == ["naming_quality"]
    83→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/scan/reporting/agent_context.py"
}
```

> TOOL

tool_result Read
```
1→"""LLM-facing reporting helpers for scan command."""
     2→
     3→from __future__ import annotations
     4→
     5→import logging
     6→import os
     7→from pathlib import Path
     8→from typing import Any
     9→
    10→from desloppify import state as state_mod
    11→from desloppify.base.output.user_message import print_user_message
    12→from desloppify.app.commands.update_skill import (
    13→    resolve_interface,
    14→    update_installed_skill,
    15→)
    16→from desloppify.base import registry as registry_mod
    17→from desloppify.app import skill_docs as skill_docs_mod
    18→from desloppify.base.exception_sets import PLAN_LOAD_EXCEPTIONS
    19→from desloppify.base.output.fallbacks import log_best_effort_failure
    20→from desloppify.base.discovery.paths import get_project_root
    21→from desloppify.engine._scoring.results.core import compute_health_breakdown
    22→from desloppify.engine._scoring.subjective.core import DISPLAY_NAMES
    23→from desloppify.engine._state.schema import StateModel
    24→from desloppify.engine._work_queue.core import ATTEST_EXAMPLE
    25→from desloppify.engine.plan import load_plan
    26→from desloppify.engine.planning import scorecard_projection as scorecard_projection_mod
    27→
    28→from .text import build_workflow_guide
    29→
    30→logger = logging.getLogger(__name__)
    31→
    32→
    33→def is_agent_environment() -> bool:
    34→    return bool(
    35→        os.environ.get("CLAUDE_CODE")
    36→        or os.environ.get("DESLOPPIFY_AGENT")
    37→        or os.environ.get("GEMINI_CLI")
    38→        or os.environ.get("CODEX_SANDBOX_NETWORK_DISABLED")
    39→        or os.environ.get("CODEX_SANDBOX")
    40→        or os.environ.get("CURSOR_TRACE_ID")
    41→    )
    42→
    43→
    44→def _load_scores(state: StateModel) -> state_mod.ScoreSnapshot:
    45→    """Load all four canonical scores from state."""
    46→    return state_mod.score_snapshot(state)
    47→
    48→
    49→def _print_score_lines(
    50→    *,
    51→    overall_score: float | None,
    52→    objective_score: float | None,
    53→    strict_score: float | None,
    54→    verified_strict_score: float | None,
    55→) -> None:
    56→    lines: list[str] = []
    57→    if overall_score is not None:
    58→        lines.append(f"Overall score:   {overall_score:.1f}/100")
    59→    if objective_score is not None:
    60→        lines.append(f"Objective score: {objective_score:.1f}/100")
    61→    if strict_score is not None:
    62→        lines.append(f"Strict score:    {strict_score:.1f}/100")
    63→    if verified_strict_score is not None:
    64→        lines.append(f"Verified score:  {verified_strict_score:.1f}/100")
    65→    if lines:
    66→        print("\n".join(lines))
    67→    # Score legend — always shown in LLM block so agents understand the scoring model
    68→    print("Score guide:")
    69→    print("  overall  = 40% mechanical + 60% subjective (lenient — ignores wontfix)")
    70→    print("  objective = mechanical detectors only (no subjective review)")
    71→    print("  strict   = like overall, but wontfix counts against you  <-- your north star")
    72→    print("  verified = strict, but only credits scan-verified fixes")
    73→    print()
    74→
    75→
    76→def _split_dimension_scores(
    77→    state: StateModel,
    78→    dim_scores: dict[str, Any],
    79→) -> tuple[list[tuple[str, dict[str, Any]]], list[tuple[str, dict[str, Any]]]]:
    80→    # Build dimension table from canonical scorecard projection.
    81→    rows = scorecard_projection_mod.scorecard_dimension_rows(
    82→        state, dim_scores=dim_scores
    83→    )
    84→    subjective_name_set = {name.lower() for name in DISPLAY_NAMES.values()}
    85→    subjective_name_set.update({"elegance", "elegance (combined)"})
    86→
    87→    mechanical = [
    88→        (name, data)
    89→        for name, data in rows
    90→        if (
    91→            "subjective_assessment" not in data.get("detectors", {})
    92→            and str(name).strip().lower() not in subjective_name_set
    93→        )
    94→    ]
    95→    subjective = [
    96→        (name, data)
    97→        for name, data in rows
    98→        if (
    99→            "subjective_assessment" in data.get("detectors", {})
   100→            or str(name).strip().lower() in subjective_name_set
   101→        )
   102→    ]
   103→    return mechanical, subjective
   104→
   105→
   106→def _print_dimension_table(state: StateModel, dim_scores: dict[str, Any]) -> None:
   107→    mechanical, subjective = _split_dimension_scores(state, dim_scores)
   108→    if not (mechanical or subjective):
   109→        return
   110→
   111→    print("| Dimension | Health | Strict | Issues | Tier | Action |")
   112→    print("|-----------|--------|--------|--------|------|--------|")
   113→    for name, data in sorted(mechanical, key=lambda item: item[0]):
   114→        score = data.get("score", 100)
   115→        strict = data.get("strict", score)
   116→        issues = data.get("failing", 0)
   117→        tier = data.get("tier", "")
   118→        action = registry_mod.dimension_action_type(name)
   119→        print(
   120→            f"| {name} | {score:.1f}% | {strict:.1f}% | {issues} | T{tier} | {action} |"
   121→        )
   122→    if subjective:
   123→        print("| **Subjective Dimensions** | | | | | |")
   124→        for name, data in sorted(subjective, key=lambda item: item[0]):
   125→            score = data.get("score", 100)
   126→            strict = data.get("strict", score)
   127→            issues = data.get("failing", 0)
   128→            tier = data.get("tier", "")
   129→            print(
   130→                f"| {name} | {score:.1f}% | {strict:.1f}% | {issues} | T{tier} | review |"
   131→            )
   132→    print()
   133→
   134→
   135→def _print_drag_summary(dim_scores: dict[str, Any]) -> None:
   136→    """Print the biggest score-drag dimensions so agents know where to focus."""
   137→    if not dim_scores:
   138→        return
   139→    try:
   140→        breakdown = compute_health_breakdown(dim_scores)
   141→        entries = breakdown.get("entries", [])
   142→        drags = sorted(
   143→            [e for e in entries if isinstance(e, dict) and float(e.get("overall_drag", 0) or 0) > 0.01],
   144→            key=lambda e: -float(e.get("overall_drag", 0) or 0),
   145→        )
   146→        if drags:
   147→            print("Biggest score drags (fixing these dimensions has the most impact):")
   148→            for entry in drags[:5]:
   149→                print(
   150→                    f"  - {entry['name']}: -{float(entry['overall_drag']):.2f} pts "
   151→                    f"(score {float(entry['score']):.1f}%, "
   152→                    f"{float(entry['pool_share'])*100:.1f}% of {entry['pool']} pool)"
   153→                )
   154→            print()
   155→    except (ImportError, TypeError, ValueError, KeyError) as exc:
   156→        log_best_effort_failure(
   157→            logger,
   158→            "compute score drag summary for scan report",
   159→            exc,
   160→        )
   161→
   162→
   163→def _print_stats_summary(
   164→    state: StateModel,
   165→    diff: dict[str, Any] | None,
   166→    *,
   167→    overall_score: float | None,
   168→    strict_score: float | None,
   169→) -> None:
   170→    stats = state.get("stats", {})
   171→    if not stats:
   172→        return
   173→
   174→    wontfix = stats.get("wontfix", 0)
   175→    ignored = diff.get("ignored", 0) if diff else 0
   176→    ignore_pats = diff.get("ignore_patterns", 0) if diff else 0
   177→    strict_gap = (
   178→        round((overall_score or 0) - (strict_score or 0), 1)
   179→        if overall_score and strict_score
   180→        else 0
   181→    )
   182→    print(
   183→        f"Total issues: {stats.get('total', 0)} | "
   184→        f"Open: {stats.get('open', 0)} | "
   185→        f"Fixed: {stats.get('fixed', 0)} | "
   186→        f"Wontfix: {wontfix}"
   187→    )
   188→    if wontfix or ignored or ignore_pats:
   189→        print(
   190→            f"Ignored: {ignored} (by {ignore_pats} patterns) | Strict gap: {strict_gap} pts"
   191→        )
   192→        print("Focus on strict score — wontfix and ignore inflate the lenient score.")
   193→    print()
   194→
   195→
   196→_WORKFLOW_GUIDE = build_workflow_guide(ATTEST_EXAMPLE)
   197→
   198→
   199→def _print_workflow_guide() -> None:
   200→    # Workflow guide — teach agents the full cycle
   201→    print(_WORKFLOW_GUIDE)
   202→    print()
   203→
   204→
   205→def _print_narrative_status(narrative: dict[str, Any] | None) -> None:
   206→    if not narrative:
   207→        return
   208→
   209→    headline = narrative.get("headline", "")
   210→    strategy = narrative.get("strategy") or {}
   211→    actions = narrative.get("actions", [])
   212→    if headline:
   213→        print(f"Current status: {headline}")
   214→    hint = strategy.get("hint", "")
   215→    if hint:
   216→        print(f"Strategy: {hint}")
   217→    if actions:
   218→        top = actions[0]
   219→        print(f"Top action: `{top['command']}` — {top['description']}")
   220→    print()
   221→
   222→
   223→def _detect_agent_interface() -> str | None:
   224→    """Detect the current agent interface from environment variables."""
   225→    if os.environ.get("CLAUDE_CODE"):
   226→        return "claude"
   227→    if os.environ.get("GEMINI_CLI"):
   228→        return "gemini"
   229→    if os.environ.get("CODEX_SANDBOX_NETWORK_DISABLED") or os.environ.get("CODEX_SANDBOX"):
   230→        return "codex"
   231→    if os.environ.get("CURSOR_TRACE_ID"):
   232→        return "cursor"
   233→    return None
   234→
   235→
   236→def _try_auto_update_skill() -> None:
   237→    """Attempt to auto-install or auto-update the skill document.
   238→
   239→    Best-effort: swallows all exceptions so a network failure or permission
   240→    error never breaks the scan.
   241→    """
   242→    install = skill_docs_mod.find_installed_skill()
   243→
   244→    if install and not install.stale:
   245→        return  # Up to date.
   246→
   247→    try:
   248→        if install:
   249→            interface = resolve_interface(install=install)
   250→        else:
   251→            interface = _detect_agent_interface()
   252→
   253→        if interface:
   254→            update_installed_skill(interface)
   255→    except (ImportError, OSError, RuntimeError, ValueError) as exc:
   256→        log_best_effort_failure(
   257→            logger,
   258→            "auto-update installed skill guidance",
   259→            exc,
   260→        )
   261→
   262→
   263→def _print_badge_hint(badge_path: Path | None) -> None:
   264→    if not (badge_path and badge_path.exists()):
   265→        return
   266→
   267→    rel_path = badge_path.name if badge_path.parent == get_project_root() else str(badge_path)
   268→    print(f"A scorecard image was saved to `{rel_path}`.")
   269→    print("Let the user know they can view it, and suggest adding it")
   270→    print(f'to their README: `<img src="{rel_path}" width="100%">`')
   271→
   272→
   273→def print_llm_summary(
   274→    state: StateModel,
   275→    badge_path: Path | None,
   276→    narrative: dict[str, Any] | None = None,
   277→    diff: dict[str, Any] | None = None,
   278→) -> None:
   279→    """Print a structured summary for LLM consumption.
   280→
   281→    The LLM reads terminal output after running scans. This gives it
   282→    clear instructions on how to present the results to the end user.
   283→    Only shown when running inside an agent (CLAUDE_CODE or DESLOPPIFY_AGENT env).
   284→    """
   285→    if not is_agent_environment():
   286→        return
   287→
   288→    dim_scores = state.get("dimension_scores", {})
   289→    scores = _load_scores(state)
   290→
   291→    if _llm_summary_empty(scores, dim_scores):
   292→        return
   293→
   294→    _print_llm_header()
   295→    plan_snapshot, has_plan = _load_living_plan_snapshot()
   296→
   297→    if has_plan:
   298→        _print_living_plan_notice(plan_snapshot)
   299→
   300→    _print_score_lines(
   301→        overall_score=scores.overall,
   302→        objective_score=scores.objective,
   303→        strict_score=scores.strict,
   304→        verified_strict_score=scores.verified,
   305→    )
   306→    _print_dimension_table(state, dim_scores)
   307→    _print_drag_summary(dim_scores)
   308→    _print_stats_summary(
   309→        state,
   310→        diff,
   311→        overall_score=scores.overall,
   312→        strict_score=scores.strict,
   313→    )
   314→    if has_plan:
   315→        print("\nFollow the living plan: `desloppify next` for your next task,")
   316→        print("`desloppify plan` to view the full queue.")
   317→    else:
   318→        _print_workflow_guide()
   319→    _print_narrative_status(narrative)
   320→    _print_badge_hint(badge_path)
   321→    print("─" * 60)
   322→
   323→    if has_plan:
   324→        print_user_message(
   325→            "Hey — please follow the living plan. Run `desloppify"
   326→            " next` for your next task. No need to reply, just"
   327→            " continue."
   328→        )
   329→
   330→
   331→def _llm_summary_empty(scores: state_mod.ScoreSnapshot, dim_scores: dict[str, Any]) -> bool:
   332→    return (
   333→        scores.overall is None
   334→        and scores.objective is None
   335→        and scores.strict is None
   336→        and scores.verified is None
   337→        and not dim_scores
   338→    )
   339→
   340→
   341→def _print_llm_header() -> None:
   342→    """Print the LLM instruction block header for agent-facing scan output.
   343→
   344→    Side-effect only: prints framing text that tells LLM agents how to
   345→    present scan results. Called from print_llm_summary.
   346→    """
   347→    print("─" * 60)
   348→    print("INSTRUCTIONS FOR LLM")
   349→    print("IMPORTANT: ALWAYS present ALL scores to the user after a scan.")
   350→    print("Show overall health (lenient + strict), ALL dimension scores,")
   351→    print("AND all subjective dimension scores in a markdown table.")
   352→    print("The goal is to maximize strict scores. Never skip the scores.\n")
   353→
   354→
   355→def _load_living_plan_snapshot() -> tuple[dict[str, object], bool]:
   356→    fallback: dict[str, object] = {
   357→        "queue_order": [],
   358→        "clusters": {},
   359→        "skipped": {},
   360→        "active_cluster": None,
   361→    }
   362→    try:
   363→        loaded_plan = load_plan()
   364→    except PLAN_LOAD_EXCEPTIONS:
   365→        return fallback, False
   366→    if not isinstance(loaded_plan, dict):
   367→        loaded_plan = {}
   368→    loaded_plan.setdefault("queue_order", [])
   369→    loaded_plan.setdefault("clusters", {})
   370→    loaded_plan.setdefault("skipped", {})
   371→    loaded_plan.setdefault("active_cluster", None)
   372→
   373→    queue_order = loaded_plan.get("queue_order")
   374→    clusters = loaded_plan.get("clusters")
   375→    skipped = loaded_plan.get("skipped")
   376→    active = loaded_plan.get("active_cluster")
   377→
   378→    snapshot = {
   379→        "queue_order": queue_order if isinstance(queue_order, list) else [],
   380→        "clusters": clusters if isinstance(clusters, dict) else {},
   381→        "skipped": skipped if isinstance(skipped, dict) else {},
   382→        "active_cluster": active if isinstance(active, str) and active else None,
   383→    }
   384→    has_plan = bool(snapshot["queue_order"] or snapshot["clusters"] or snapshot["skipped"])
   385→    return snapshot, has_plan
   386→
   387→
   388→def _print_living_plan_notice(plan_snapshot: dict[str, object]) -> None:
   389→    ordered = len(plan_snapshot.get("queue_order", []))
   390→    skipped = len(plan_snapshot.get("skipped", {}))
   391→    active = plan_snapshot.get("active_cluster")
   392→    print(f"LIVING PLAN ACTIVE: {ordered} ordered, {skipped} skipped.")
   393→    if isinstance(active, str) and active:
   394→        cluster = plan_snapshot.get("clusters", {}).get(active)
   395→        issue_ids = cluster.get("issue_ids", []) if isinstance(cluster, dict) else []
   396→        remaining = len(issue_ids) if isinstance(issue_ids, list) else 0
   397→        print(f"Focused on: {active} ({remaining} items remaining).")
   398→    print("The plan is the single source of truth for work order.")
   399→    print("Use `desloppify next` which respects the plan.")
   400→    print("Use `desloppify plan` to view and update it.\n")
   401→
   402→
   403→def auto_update_skill() -> None:
   404→    """Auto-install or update the skill document if we detect an agent.
   405→
   406→    Called unconditionally from the scan workflow — not gated on scores.
   407→    """
   408→    if not is_agent_environment():
   409→        return
   410→
   411→    _try_auto_update_skill()
   412→
   413→    # Single post-check: whatever happened above, is the doc current now?
   414→    install = skill_docs_mod.find_installed_skill()
   415→    if not install:
   416→        names = ", ".join(sorted(skill_docs_mod.SKILL_TARGETS))
   417→        print(
   418→            f"No skill document found. Install one for better workflow guidance: "
   419→            f"desloppify update-skill <{names}>"
   420→        )
   421→    elif install.stale:
   422→        print(
   423→            f"Skill document is outdated "
   424→            f"(v{install.version}, current v{skill_docs_mod.SKILL_VERSION}). "
   425→            f"Run: desloppify update-skill"
   426→        )
   427→
   428→
   429→__all__ = ["is_agent_environment", "print_llm_summary", "auto_update_skill"]
   430→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/scan/reporting/dimensions.py"
}
```

> TOOL

tool_result Read
```
1→"""Dimension and detector table reporting for scan command."""
     2→
     3→from __future__ import annotations
     4→
     5→import desloppify.engine._scoring.results.core as scoring_mod
     6→from desloppify import state as state_mod
     7→from desloppify.app.commands.scan.reporting.subjective import (
     8→    SubjectiveFollowup,
     9→    build_subjective_followup,
    10→    flatten_cli_keys,
    11→    show_subjective_paths,
    12→    subjective_entries_for_dimension_keys,
    13→    subjective_integrity_followup,
    14→    subjective_integrity_notice_lines,
    15→    subjective_rerun_command,
    16→)
    17→from desloppify.base.config import DEFAULT_TARGET_STRICT_SCORE
    18→from desloppify.base import registry as registry_mod
    19→from desloppify.base.output.terminal import colorize
    20→from desloppify.engine.planning.scorecard_projection import (
    21→    dimension_cli_key,
    22→    scorecard_dimension_cli_keys,
    23→    scorecard_dimension_rows,
    24→    scorecard_subjective_entries,
    25→)
    26→import desloppify.intelligence.narrative._constants as narrative_constants_mod
    27→
    28→from . import presentation as presentation_mod
    29→
    30→
    31→def show_detector_progress(state: dict):
    32→    """Show per-detector progress bars — the heartbeat of a scan."""
    33→    return presentation_mod.show_detector_progress(
    34→        state,
    35→        state_mod=state_mod,
    36→        narrative_mod=narrative_constants_mod,
    37→        registry_mod=registry_mod,
    38→        colorize_fn=colorize,
    39→    )
    40→
    41→
    42→def _dimension_bar(score: float, *, bar_len: int = 15) -> str:
    43→    """Render a score bar consistent with scan detector bars."""
    44→    return presentation_mod.dimension_bar(score, colorize_fn=colorize, bar_len=bar_len)
    45→
    46→
    47→def scorecard_dimension_entries(
    48→    state: dict,
    49→    *,
    50→    dim_scores: dict | None = None,
    51→) -> list[dict]:
    52→    """Return scorecard rows with presentation-friendly metadata."""
    53→    rows = scorecard_dimension_rows(state, dim_scores=dim_scores)
    54→    subjective_by_name = {
    55→        entry["name"]: entry
    56→        for entry in scorecard_subjective_entries(
    57→            state,
    58→            dim_scores=dim_scores,
    59→        )
    60→    }
    61→    entries: list[dict] = []
    62→    for name, data in rows:
    63→        detectors = data.get("detectors", {})
    64→        subjective_meta = subjective_by_name.get(name)
    65→        is_subjective = subjective_meta is not None
    66→        score = float(data.get("score", 0.0))
    67→        strict = float(data.get("strict", score))
    68→        issues = int(data.get("failing", 0))
    69→        checks = int(data.get("checks", 0))
    70→        placeholder = bool(subjective_meta.get("placeholder")) if subjective_meta else False
    71→        not_scanned = bool(
    72→            not is_subjective and not detectors and checks == 0
    73→        )
    74→        carried_forward = bool(
    75→            not is_subjective and data.get("carried_forward")
    76→        )
    77→        dim_key = str(subjective_meta.get("dimension_key", "")) if subjective_meta else ""
    78→        stale = bool(subjective_meta.get("stale")) if subjective_meta else False
    79→        cli_keys = (
    80→            list(subjective_meta.get("cli_keys", []))
    81→            if subjective_meta
    82→            else scorecard_dimension_cli_keys(name, data)
    83→        )
    84→        entries.append(
    85→            {
    86→                "name": name,
    87→                "score": score,
    88→                "strict": strict,
    89→                "failing": issues,
    90→                "checks": checks,
    91→                "subjective": is_subjective,
    92→                "placeholder": placeholder,
    93→                "stale": stale,
    94→                "dimension_key": dim_key,
    95→                "not_scanned": not_scanned,
    96→                "carried_forward": carried_forward,
    97→                "cli_keys": cli_keys,
    98→            }
    99→        )
   100→    return entries
   101→
   102→
   103→def show_scorecard_subjective_measures(state: dict) -> None:
   104→    """Show canonical scorecard dimensions only (mechanical + subjective)."""
   105→    entries = scorecard_dimension_entries(state)
   106→    if not entries:
   107→        return
   108→
   109→    print(colorize("  Scorecard dimensions (matches scorecard.png):", "dim"))
   110→    for entry in entries:
   111→        if entry.get("not_scanned"):
   112→            print(
   113→                "  "
   114→                + f"{entry['name']:<18} "
   115→                + colorize("─── skipped ───────────────────  (run without --skip-slow)", "yellow")
   116→            )
   117→            continue
   118→        bar = _dimension_bar(entry["score"])
   119→        suffix = ""
   120→        if entry.get("carried_forward"):
   121→            suffix = colorize("  ⟲ prior scan", "dim")
   122→        elif entry.get("placeholder"):
   123→            suffix = colorize("  [unassessed]", "yellow")
   124→        elif entry.get("stale"):
   125→            suffix = colorize("  [stale — re-review]", "yellow")
   126→        print(
   127→            "  "
   128→            + f"{entry['name']:<18} {bar} {entry['score']:5.1f}%  "
   129→            + colorize(f"(strict {entry['strict']:5.1f}%)", "dim")
   130→            + suffix
   131→        )
   132→    stale_keys = [e["dimension_key"] for e in entries if e.get("stale")]
   133→    has_open = any(
   134→        f.get("status") == "open" and not f.get("suppressed")
   135→        for f in (state.get("issues") or {}).values()
   136→    )
   137→    if stale_keys and not has_open:
   138→        n = len(stale_keys)
   139→        dims_arg = ",".join(stale_keys)
   140→        print(
   141→            colorize(
   142→                f"  {n} stale subjective dimension{'s' if n != 1 else ''}"
   143→                f" — run `desloppify review --prepare --dimensions {dims_arg}` then follow your runner's review workflow",
   144→                "yellow",
   145→            )
   146→        )
   147→    print()
   148→
   149→
   150→def show_score_model_breakdown(state: dict, *, dim_scores: dict | None = None) -> None:
   151→    """Show score recipe and weighted drags so users can see what drives the north star."""
   152→    return presentation_mod.show_score_model_breakdown(
   153→        state,
   154→        scoring_mod=scoring_mod,
   155→        colorize_fn=colorize,
   156→        dim_scores=dim_scores,
   157→    )
   158→
   159→
   160→def show_dimension_deltas(prev: dict, current: dict):
   161→    """Show which dimensions changed between scans (health and strict)."""
   162→    return presentation_mod.show_dimension_deltas(
   163→        prev,
   164→        current,
   165→        scoring_mod=scoring_mod,
   166→        colorize_fn=colorize,
   167→    )
   168→
   169→
   170→def show_low_dimension_hints(dim_scores: dict):
   171→    """Show actionable hints for dimensions below 50%."""
   172→    return presentation_mod.show_low_dimension_hints(
   173→        dim_scores,
   174→        scoring_mod=scoring_mod,
   175→        colorize_fn=colorize,
   176→    )
   177→
   178→
   179→def show_subjective_paths_section(
   180→    state: dict,
   181→    dim_scores: dict,
   182→    *,
   183→    threshold: float = DEFAULT_TARGET_STRICT_SCORE,
   184→) -> None:
   185→    """Show explicit subjective-score improvement paths (coverage vs quality)."""
   186→    return show_subjective_paths(
   187→        state,
   188→        dim_scores,
   189→        colorize_fn=colorize,
   190→        scorecard_subjective_entries_fn=scorecard_subjective_entries,
   191→        threshold=threshold,
   192→    )
   193→
   194→
   195→__all__ = [
   196→    "SubjectiveFollowup",
   197→    "build_subjective_followup",
   198→    "dimension_cli_key",
   199→    "flatten_cli_keys",
   200→    "scorecard_dimension_entries",
   201→    "subjective_entries_for_dimension_keys",
   202→    "subjective_integrity_followup",
   203→    "subjective_integrity_notice_lines",
   204→    "subjective_rerun_command",
   205→    "show_detector_progress",
   206→    "show_score_model_breakdown",
   207→    "show_scorecard_subjective_measures",
   208→    "show_dimension_deltas",
   209→    "show_low_dimension_hints",
   210→    "show_subjective_paths_section",
   211→]
   212→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next/cmd.py"
}
```

> TOOL

tool_result Read
```
1→"""next command: show next highest-priority queue items."""
     2→
     3→from __future__ import annotations
     4→
     5→import argparse
     6→from dataclasses import dataclass
     7→
     8→from desloppify import state as state_mod
     9→from desloppify.app.commands.helpers.guardrails import print_triage_guardrail_info
    10→from desloppify.app.commands.helpers.lang import resolve_lang
    11→from desloppify.app.commands.helpers.query import write_query
    12→from desloppify.app.commands.helpers.queue_progress import (
    13→    QueueBreakdown,
    14→    get_plan_start_strict,
    15→    plan_aware_queue_breakdown,
    16→)
    17→from desloppify.app.commands.helpers.runtime import command_runtime
    18→from desloppify.base.config import DEFAULT_TARGET_STRICT_SCORE, target_strict_score_from_config
    19→from desloppify.app.commands.helpers.state import require_completed_scan
    20→from desloppify.base.discovery.file_paths import safe_write_text
    21→from desloppify.base.exception_sets import PLAN_LOAD_EXCEPTIONS, CommandError
    22→from desloppify.base.output.terminal import colorize
    23→from desloppify.base.output.user_message import print_user_message
    24→from desloppify.app.skill_docs import check_skill_version
    25→from desloppify.base.tooling import check_config_staleness
    26→from desloppify.engine._scoring.detection import merge_potentials
    27→from desloppify.engine._work_queue.context import queue_context
    28→from desloppify.engine._work_queue.core import (
    29→    QueueBuildOptions,
    30→    build_work_queue,
    31→)
    32→from desloppify.engine._work_queue.plan_order import collapse_clusters
    33→from desloppify.engine.plan import load_plan
    34→from desloppify.engine.planning.scorecard_projection import (
    35→    scorecard_dimensions_payload,
    36→)
    37→from desloppify.intelligence.narrative.core import NarrativeContext, compute_narrative
    38→
    39→from . import output as next_output_mod
    40→from . import render as next_render_mod
    41→from . import render_nudges as next_nudges_mod
    42→from .render_support import render_queue_header as _render_queue_header
    43→from .render_support import scorecard_subjective as _scorecard_subjective_impl
    44→from .render_support import show_empty_queue as _show_empty_queue
    45→
    46→
    47→@dataclass(frozen=True)
    48→class NextOptions:
    49→    """All user-facing options for the ``next`` command, extracted once."""
    50→
    51→    count: int = 1
    52→    scope: str | None = None
    53→    status: str = "open"
    54→    group: str = "item"
    55→    explain: bool = False
    56→    cluster: str | None = None
    57→    include_skipped: bool = False
    58→    output_file: str | None = None
    59→    output_format: str = "terminal"
    60→
    61→    @classmethod
    62→    def from_args(cls, args: argparse.Namespace) -> NextOptions:
    63→        """Build from an argparse Namespace, applying defaults for missing attrs."""
    64→        return cls(
    65→            count=getattr(args, "count", 1) or 1,
    66→            scope=getattr(args, "scope", None),
    67→            status=getattr(args, "status", "open"),
    68→            group=getattr(args, "group", "item"),
    69→            explain=bool(getattr(args, "explain", False)),
    70→            cluster=getattr(args, "cluster", None),
    71→            include_skipped=bool(getattr(args, "include_skipped", False)),
    72→            output_file=getattr(args, "output", None),
    73→            output_format=getattr(args, "format", "terminal"),
    74→        )
    75→
    76→
    77→def _scorecard_subjective(
    78→    state: dict,
    79→    dim_scores: dict,
    80→) -> list[dict]:
    81→    """Return scorecard-aligned subjective entries for current dimension scores."""
    82→    return _scorecard_subjective_impl(state, dim_scores)
    83→
    84→
    85→def _low_subjective_dimensions(
    86→    state: dict,
    87→    dim_scores: dict,
    88→    *,
    89→    threshold: float = DEFAULT_TARGET_STRICT_SCORE,
    90→) -> list[tuple[str, float, int]]:
    91→    """Return assessed scorecard-subjective entries below the threshold."""
    92→    low: list[tuple[str, float, int]] = []
    93→    for entry in _scorecard_subjective(state, dim_scores):
    94→        if entry.get("placeholder"):
    95→            continue
    96→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
    97→        if strict_val < threshold:
    98→            low.append(
    99→                (
   100→                    str(entry.get("name", "Subjective")),
   101→                    strict_val,
   102→                    int(entry.get("failing", 0)),
   103→                )
   104→            )
   105→    low.sort(key=lambda item: item[1])
   106→    return low
   107→
   108→
   109→def cmd_next(args: argparse.Namespace) -> None:
   110→    """Show next highest-priority queue items."""
   111→    runtime = command_runtime(args)
   112→    state = runtime.state
   113→    config = runtime.config
   114→    if not require_completed_scan(state):
   115→        return
   116→
   117→    skill_warning = check_skill_version()
   118→    if skill_warning:
   119→        print(colorize(f"  {skill_warning}", "yellow"))
   120→    config_warning = check_config_staleness(config)
   121→    if config_warning:
   122→        print(colorize(f"  {config_warning}", "yellow"))
   123→
   124→    print_triage_guardrail_info(state=state)
   125→    _build_and_render_queue(args, state, config)
   126→
   127→
   128→def _resolve_cluster_focus(
   129→    plan_data: dict | None,
   130→    *,
   131→    cluster_arg: str | None,
   132→    scope: str | None,
   133→) -> str | None:
   134→    effective_cluster = cluster_arg
   135→    if plan_data and not cluster_arg and not scope:
   136→        active_cluster = plan_data.get("active_cluster")
   137→        if active_cluster:
   138→            effective_cluster = active_cluster
   139→    return effective_cluster
   140→
   141→
   142→def _build_next_payload(
   143→    *,
   144→    queue: dict,
   145→    items: list[dict],
   146→    state: dict,
   147→    narrative: dict,
   148→    plan_data: dict | None,
   149→) -> dict:
   150→    payload = next_output_mod.build_query_payload(
   151→        queue, items, command="next", narrative=narrative, plan=plan_data
   152→    )
   153→    scores = state_mod.score_snapshot(state)
   154→    payload["overall_score"] = scores.overall
   155→    payload["objective_score"] = scores.objective
   156→    payload["strict_score"] = scores.strict
   157→    payload["scorecard_dimensions"] = scorecard_dimensions_payload(
   158→        state,
   159→        dim_scores=state.get("dimension_scores", {}),
   160→    )
   161→    payload["subjective_measures"] = [
   162→        row for row in payload["scorecard_dimensions"] if row.get("subjective")
   163→    ]
   164→    return payload
   165→
   166→
   167→def _emit_requested_output(
   168→    opts: NextOptions,
   169→    payload: dict,
   170→    items: list[dict],
   171→) -> bool:
   172→    if opts.output_file:
   173→        if next_output_mod.write_output_file(
   174→            opts.output_file,
   175→            payload,
   176→            len(items),
   177→            safe_write_text_fn=safe_write_text,
   178→            colorize_fn=colorize,
   179→        ):
   180→            return True
   181→        raise CommandError("Failed to write output file")
   182→
   183→    if next_output_mod.emit_non_terminal_output(opts.output_format, payload, items):
   184→        return True
   185→    return False
   186→
   187→
   188→def _plan_queue_context(
   189→    *,
   190→    state: dict,
   191→    plan_data: dict | None,
   192→    context=None,
   193→) -> tuple[float | None, QueueBreakdown | None]:
   194→    effective_plan = context.plan if context is not None else plan_data
   195→    plan_start_strict = get_plan_start_strict(effective_plan)
   196→    try:
   197→        breakdown = plan_aware_queue_breakdown(state, plan_data, context=context)
   198→    except PLAN_LOAD_EXCEPTIONS:
   199→        breakdown = None
   200→    return plan_start_strict, breakdown
   201→
   202→
   203→def _merge_potentials_safe(raw_potentials: dict | None) -> dict | None:
   204→    try:
   205→        return merge_potentials(raw_potentials) or None
   206→    except (ImportError, TypeError, ValueError):
   207→        return raw_potentials or None
   208→
   209→
   210→def _build_and_render_queue(args: argparse.Namespace, state: dict, config: dict) -> None:
   211→    opts = NextOptions.from_args(args)
   212→
   213→    target_strict = target_strict_score_from_config(config)
   214→
   215→    # Load the living plan
   216→    plan = load_plan()
   217→    plan_data: dict | None = None
   218→    if (
   219→        plan.get("queue_order")
   220→        or plan.get("overrides")
   221→        or plan.get("clusters")
   222→    ):
   223→        plan_data = plan
   224→
   225→    # Build unified context once — all downstream consumers agree on
   226→    # plan, target_strict, and subjective visibility policy.
   227→    ctx = queue_context(
   228→        state, config=config, plan=plan_data, target_strict=target_strict,
   229→    )
   230→
   231→    # Auto-scope to focus cluster if set and no explicit scope/cluster
   232→    effective_cluster = _resolve_cluster_focus(
   233→        plan_data,
   234→        cluster_arg=opts.cluster,
   235→        scope=opts.scope,
   236→    )
   237→
   238→    queue = build_work_queue(
   239→        state,
   240→        options=QueueBuildOptions(
   241→            count=None,
   242→            scope=opts.scope,
   243→            status=opts.status,
   244→            include_subjective=True,
   245→            subjective_threshold=target_strict,
   246→            explain=opts.explain,
   247→            include_skipped=opts.include_skipped,
   248→            cluster=effective_cluster,
   249→            context=ctx,
   250→        ),
   251→    )
   252→    items = queue.get("items", [])
   253→
   254→    # Collapse auto-clusters into display meta-items
   255→    if plan_data and not effective_cluster and not plan_data.get("active_cluster"):
   256→        items = collapse_clusters(items, plan_data)
   257→
   258→    # Apply count truncation after collapsing
   259→    if opts.count:
   260→        items = items[: opts.count]
   261→        queue["items"] = items
   262→        queue["total"] = len(items)
   263→
   264→    lang = resolve_lang(args)
   265→    lang_name = lang.name if lang else None
   266→    narrative = compute_narrative(
   267→        state,
   268→        context=NarrativeContext(lang=lang_name, command="next", plan=plan_data),
   269→    )
   270→
   271→    payload = _build_next_payload(
   272→        queue=queue,
   273→        items=items,
   274→        state=state,
   275→        narrative=narrative,
   276→        plan_data=plan_data,
   277→    )
   278→    write_query(payload)
   279→
   280→    if _emit_requested_output(opts, payload, items):
   281→        return
   282→
   283→    dim_scores = state.get("dimension_scores", {})
   284→    issues_scoped = state_mod.path_scoped_issues(
   285→        state.get("issues", {}),
   286→        state.get("scan_path"),
   287→    )
   288→
   289→    # Extract frozen plan-start score and queue breakdown for lifecycle display
   290→    plan_start_strict, breakdown = _plan_queue_context(
   291→        state=state,
   292→        plan_data=plan_data,
   293→        context=ctx,
   294→    )
   295→    queue_total = breakdown.queue_total if breakdown else 0
   296→
   297→    _render_queue_header(queue, opts.explain)
   298→    strict_score = state_mod.score_snapshot(state).strict
   299→    if _show_empty_queue(
   300→        queue,
   301→        strict_score,
   302→        plan_start_strict=plan_start_strict,
   303→        target_strict=target_strict,
   304→    ):
   305→        return
   306→
   307→    raw_potentials = state.get("potentials", {})
   308→    potentials = _merge_potentials_safe(raw_potentials)
   309→    next_render_mod.render_terminal_items(
   310→        items, dim_scores, issues_scoped, group=opts.group, explain=opts.explain,
   311→        potentials=potentials, plan=plan_data,
   312→        cluster_filter=effective_cluster,
   313→    )
   314→    next_nudges_mod.render_single_item_resolution_hint(items)
   315→    next_nudges_mod.render_uncommitted_reminder(plan_data)
   316→    next_nudges_mod.render_followup_nudges(
   317→        state,
   318→        dim_scores,
   319→        issues_scoped,
   320→        strict_score=strict_score,
   321→        target_strict_score=target_strict,
   322→        queue_total=queue_total,
   323→        plan_start_strict=plan_start_strict,
   324→        breakdown=breakdown,
   325→    )
   326→    print()
   327→
   328→    if items and plan_data:
   329→        print_user_message(
   330→            "Hey — the task details are printed above. Just start"
   331→            " working on it. When you're done, resolve it with"
   332→            " `desloppify plan resolve` and then run `desloppify"
   333→            " next` again. If this doesn't seem like the right"
   334→            " priority, run `desloppify plan show` to see the full"
   335→            " queue, or `desloppify plan --help` for all plan tools."
   336→            " Don't stop until you're done — unless I've told you"
   337→            " otherwise, just keep going."
   338→        )
   339→
   340→
   341→__all__ = ["NextOptions", "_low_subjective_dimensions", "cmd_next"]
   342→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next/render_support.py"
}
```

> TOOL

tool_result Read
```
1→"""Shared render helpers for ``desloppify next`` terminal output."""
     2→
     3→from __future__ import annotations
     4→
     5→from collections import Counter
     6→
     7→from desloppify.app.commands.helpers.queue_progress import format_plan_delta
     8→from desloppify.base.output.terminal import colorize
     9→from desloppify.engine._work_queue.core import group_queue_items
    10→from desloppify.engine.planning.scorecard_projection import (
    11→    scorecard_subjective_entries,
    12→)
    13→from desloppify.intelligence.integrity import subjective_review_open_breakdown
    14→
    15→_ACTION_TYPE_LABELS = {
    16→    "auto_fix": "Auto-fixable batch",
    17→    "reorganize": "Reorganize batch",
    18→    "refactor": "Refactor batch",
    19→    "manual_fix": "Grouped task",
    20→}
    21→_CLUSTER_NAME_LABELS = {
    22→    "auto/initial-review": "Initial subjective review",
    23→    "auto/stale-review": "Stale subjective review",
    24→    "auto/under-target-review": "Optional re-review",
    25→}
    26→
    27→
    28→def scorecard_subjective(
    29→    state: dict,
    30→    dim_scores: dict,
    31→) -> list[dict]:
    32→    """Return scorecard-aligned subjective entries for current dimension scores."""
    33→    if not dim_scores:
    34→        return []
    35→    return scorecard_subjective_entries(
    36→        state,
    37→        dim_scores=dim_scores,
    38→    )
    39→
    40→
    41→def subjective_coverage_breakdown(
    42→    issues_scoped: dict,
    43→) -> tuple[int, dict[str, int], dict[str, int]]:
    44→    """Return open subjective-review count plus reason and holistic-reason breakdowns."""
    45→    return subjective_review_open_breakdown(issues_scoped)
    46→
    47→
    48→def is_auto_fix_command(command: str | None) -> bool:
    49→    cmd = (command or "").strip()
    50→    return cmd.startswith("desloppify autofix ") and "--dry-run" in cmd
    51→
    52→
    53→def effort_tag(item: dict) -> str:
    54→    """Return a short effort/type tag for a queue item."""
    55→    if item.get("detector") == "review":
    56→        return "[review]"
    57→    if is_auto_fix_command(item.get("primary_command")):
    58→        return "[auto]"
    59→    return ""
    60→
    61→
    62→def render_grouped(items: list[dict], group: str) -> None:
    63→    grouped = group_queue_items(items, group)
    64→    for key, grouped_items in grouped.items():
    65→        print(colorize(f"\n  {key} ({len(grouped_items)})", "cyan"))
    66→        for item in grouped_items:
    67→            confidence = item.get("confidence", "medium")
    68→            tag = effort_tag(item)
    69→            tag_str = f" {tag}" if tag else ""
    70→            print(
    71→                f"    [{confidence}]{tag_str} {item.get('summary', '')}"
    72→            )
    73→
    74→
    75→def _cluster_type_label(cluster_name: str, action_type: str) -> str:
    76→    if cluster_name in _CLUSTER_NAME_LABELS:
    77→        return _CLUSTER_NAME_LABELS[cluster_name]
    78→    return _ACTION_TYPE_LABELS.get(action_type, "Grouped task")
    79→
    80→
    81→def _render_cluster_files(members: list[dict]) -> None:
    82→    file_counts = Counter(m.get("file", "?") for m in members)
    83→    if len(file_counts) <= 5:
    84→        print(colorize("\n  Files:", "dim"))
    85→        for filename, count in file_counts.most_common():
    86→            print(f"    {filename} ({count})")
    87→        return
    88→
    89→    print(colorize(f"\n  Spread across {len(file_counts)} files:", "dim"))
    90→    for filename, count in file_counts.most_common(3):
    91→        print(f"    {filename} ({count})")
    92→    remaining = len(file_counts) - 3
    93→    print(colorize(f"    ... and {remaining} more files", "dim"))
    94→
    95→
    96→def _render_cluster_sample(members: list[dict]) -> None:
    97→    print(colorize("\n  Sample:", "dim"))
    98→    for member in members[:3]:
    99→        print(f"    - {member.get('id', '')}")
   100→    if len(members) > 3:
   101→        print(colorize(f"    ... and {len(members) - 3} more", "dim"))
   102→
   103→
   104→def _render_optional_cluster_commands(cluster_name: str) -> None:
   105→    print(colorize(f"\n  Skip:          desloppify plan skip {cluster_name}", "dim"))
   106→    print(colorize(f"  Drill in:      desloppify next --cluster {cluster_name} --count 10", "dim"))
   107→    print(
   108→        colorize(
   109→            f'  Resolve all:   desloppify plan resolve "{cluster_name}" --note "<what>" --confirm',
   110→            "dim",
   111→        )
   112→    )
   113→
   114→
   115→def _render_required_cluster_commands(cluster_name: str) -> None:
   116→    print(
   117→        colorize(
   118→            f'\n  Resolve all:   desloppify plan resolve "{cluster_name}" --note "<what>" --confirm',
   119→            "dim",
   120→        )
   121→    )
   122→    print(colorize(f"  Drill in:      desloppify next --cluster {cluster_name} --count 10", "dim"))
   123→    print(colorize(f"  Skip cluster:  desloppify plan skip {cluster_name}", "dim"))
   124→
   125→
   126→def render_cluster_item(item: dict) -> None:
   127→    """Render an auto-cluster task card."""
   128→    member_count = int(item.get("member_count", 0))
   129→    action_type = item.get("action_type", "manual_fix")
   130→    cluster_name = item.get("id", "")
   131→    is_optional = bool(item.get("cluster_optional"))
   132→    type_label = _cluster_type_label(cluster_name, action_type)
   133→    optional_tag = " — optional" if is_optional else ""
   134→    print(colorize(f"  ({type_label}, {member_count} issues{optional_tag})", "bold"))
   135→    print(colorize("  " + "─" * 60, "dim"))
   136→    print(f"  {colorize(item.get('summary', ''), 'yellow')}")
   137→
   138→    action_steps = item.get("action_steps") or []
   139→    if action_steps:
   140→        print(colorize(
   141→            f"  [plan: {len(action_steps)} steps] drill in to view",
   142→            "dim",
   143→        ))
   144→
   145→    members = item.get("members", [])
   146→    if members:
   147→        _render_cluster_files(members)
   148→        _render_cluster_sample(members)
   149→
   150→    primary_command = item.get("primary_command")
   151→    if primary_command:
   152→        print(colorize(f"\n  Action: {primary_command}", "cyan"))
   153→
   154→    if is_optional:
   155→        _render_optional_cluster_commands(cluster_name)
   156→        return
   157→
   158→    _render_required_cluster_commands(cluster_name)
   159→
   160→
   161→def render_queue_header(queue: dict, explain: bool) -> None:
   162→    del explain
   163→    total = queue.get("total", 0)
   164→    items = queue.get("items", [])
   165→    # When the only item is the "run scan" workflow action, show "Queue cleared"
   166→    # instead of a misleading "1 items" count.
   167→    if (
   168→        total == 1
   169→        and len(items) == 1
   170→        and items[0].get("id") == "workflow::run-scan"
   171→    ):
   172→        print(colorize("\n  Queue cleared (1 workflow step)", "bold"))
   173→    else:
   174→        print(colorize(f"\n  Queue: {total} item{'s' if total != 1 else ''}", "bold"))
   175→
   176→
   177→def show_empty_queue(
   178→    queue: dict,
   179→    strict: float | None,
   180→    *,
   181→    plan_start_strict: float | None = None,
   182→    target_strict: float | None = None,
   183→) -> bool:
   184→    del target_strict
   185→    if queue.get("items"):
   186→        return False
   187→    if plan_start_strict is not None and strict is not None:
   188→        delta = format_plan_delta(strict, plan_start_strict)
   189→        delta_str = f" ({delta})" if delta else ""
   190→        print(colorize("\n  Queue cleared!", "green"))
   191→        print(colorize(
   192→            f"  Frozen plan-start: strict {plan_start_strict:.1f} → Live estimate: strict {strict:.1f}{delta_str}",
   193→            "cyan",
   194→        ))
   195→        print(colorize(
   196→            "  Run `desloppify scan` now to finalize and reveal your updated score.",
   197→            "dim",
   198→        ))
   199→        return True
   200→
   201→    suffix = f" Strict score: {strict:.1f}/100" if strict is not None else ""
   202→    print(colorize(f"\n  Nothing to do!{suffix}", "green"))
   203→    return True
   204→
   205→
   206→def render_compact_item(item: dict, idx: int, total: int) -> None:
   207→    """One-line summary for cluster drill-in items after the first."""
   208→    confidence = item.get("confidence", "medium")
   209→    tag = effort_tag(item)
   210→    tag_str = f" {tag}" if tag else ""
   211→    plan_cluster = item.get("plan_cluster")
   212→    if isinstance(plan_cluster, dict) and (plan_cluster.get("action_steps") or []):
   213→        tag_str += " [plan]"
   214→    fid = item.get("id", "")
   215→    short = fid.rsplit("::", 1)[-1][:8] if "::" in fid else fid
   216→    print(f"  [{idx + 1}/{total}] [{confidence}]{tag_str} {item.get('summary', '')}")
   217→    print(colorize(f"         {item.get('file', '')}  [{short}]", "dim"))
   218→
   219→
   220→__all__ = [
   221→    "effort_tag",
   222→    "is_auto_fix_command",
   223→    "render_cluster_item",
   224→    "render_compact_item",
   225→    "render_grouped",
   226→    "render_queue_header",
   227→    "scorecard_subjective",
   228→    "show_empty_queue",
   229→    "subjective_coverage_breakdown",
   230→]
   231→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status/render_dimensions.py"
}
```

> TOOL

tool_result Read
```
1→"""Dimension-table helpers for status rendering."""
     2→
     3→from __future__ import annotations
     4→
     5→from desloppify.app.commands.scan.reporting.presentation import dimension_bar
     6→from desloppify.base.config import DEFAULT_TARGET_STRICT_SCORE
     7→from desloppify.base.output.terminal import colorize
     8→from desloppify.base.registry import dimension_action_type
     9→from desloppify.engine._scoring.policy.core import DIMENSIONS
    10→from desloppify.engine.planning.scorecard_projection import (
    11→    scorecard_subjective_entries,
    12→)
    13→
    14→
    15→def scorecard_subjective_entries_for_status(state: dict, dim_scores: dict) -> list[dict]:
    16→    """Return subjective entries aligned to scorecard labels and ordering."""
    17→    return scorecard_subjective_entries(
    18→        state,
    19→        dim_scores=dim_scores,
    20→    )
    21→
    22→
    23→def find_lowest_dimension(
    24→    dim_scores: dict,
    25→    scorecard_subjective: list[dict],
    26→) -> str | None:
    27→    """Return the dimension name with the lowest strict score."""
    28→    lowest_name = None
    29→    lowest_score = 101.0
    30→    for dim in DIMENSIONS:
    31→        ds = dim_scores.get(dim.name)
    32→        if not ds:
    33→            continue
    34→        strict_val = ds.get("strict", ds["score"])
    35→        if strict_val < lowest_score:
    36→            lowest_score = strict_val
    37→            lowest_name = dim.name
    38→    for entry in scorecard_subjective:
    39→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
    40→        if strict_val < lowest_score:
    41→            lowest_score = strict_val
    42→            lowest_name = entry.get("name")
    43→    return lowest_name
    44→
    45→
    46→def open_review_issue_counts(state: dict) -> dict[str, int]:
    47→    """Count open review issues grouped by subjective dimension key."""
    48→    issues = state.get("issues", {})
    49→    if not isinstance(issues, dict):
    50→        return {}
    51→
    52→    counts: dict[str, int] = {}
    53→    for issue in issues.values():
    54→        if not isinstance(issue, dict):
    55→            continue
    56→        if issue.get("status") != "open" or issue.get("detector") != "review":
    57→            continue
    58→        detail = issue.get("detail", {})
    59→        dimension = ""
    60→        if isinstance(detail, dict):
    61→            dimension = str(detail.get("dimension", "")).strip()
    62→        if not dimension:
    63→            dimension = str(issue.get("dimension", "")).strip()
    64→        if not dimension:
    65→            continue
    66→        counts[dimension] = counts.get(dimension, 0) + 1
    67→    return counts
    68→
    69→
    70→def render_objective_dimensions(
    71→    dim_scores: dict,
    72→    *,
    73→    lowest_name: str | None,
    74→    bar_len: int,
    75→) -> None:
    76→    """Print rows for objective (detector-based) dimensions."""
    77→    for dim in DIMENSIONS:
    78→        ds = dim_scores.get(dim.name)
    79→        if not ds:
    80→            continue
    81→        score_val = ds["score"]
    82→        strict_val = ds.get("strict", score_val)
    83→        checks = ds["checks"]
    84→
    85→        bar = dimension_bar(score_val, colorize_fn=colorize, bar_len=bar_len)
    86→        focus = colorize(" ←", "yellow") if dim.name == lowest_name else "  "
    87→        checks_str = f"{checks:>7,}"
    88→        action = dimension_action_type(dim.name)
    89→        print(
    90→            f"  {dim.name:<22} {checks_str}  {score_val:5.1f}%  {strict_val:5.1f}%  {bar}  T{dim.tier}  {action}{focus}"
    91→        )
    92→
    93→
    94→def render_subjective_dimensions(
    95→    scorecard_subjective: list[dict],
    96→    *,
    97→    lowest_name: str | None,
    98→    bar_len: int,
    99→    review_issue_counts: dict[str, int],
   100→) -> None:
   101→    """Print rows for subjective (review-based) dimensions."""
   102→    if not scorecard_subjective:
   103→        return
   104→    print(
   105→        colorize(
   106→            "  ── Subjective Measures (matches scorecard.png) ──────────────────────",
   107→            "dim",
   108→        )
   109→    )
   110→    for entry in scorecard_subjective:
   111→        name = str(entry.get("name", "Unknown"))
   112→        score_val = float(entry.get("score", 0.0))
   113→        strict_val = float(entry.get("strict", score_val))
   114→        tier = 4
   115→
   116→        bar = dimension_bar(score_val, colorize_fn=colorize, bar_len=bar_len)
   117→        focus = colorize(" ←", "yellow") if name == lowest_name else "  "
   118→        checks_str = f"{'—':>7}"
   119→        stale_tag = colorize(" [stale]", "yellow") if entry.get("stale") else ""
   120→        placeholder_tag = (
   121→            colorize(" [unassessed]", "yellow") if entry.get("placeholder") else ""
   122→        )
   123→        dim_key = str(entry.get("dimension_key", "")).strip()
   124→        cli_keys = [
   125→            str(key).strip()
   126→            for key in entry.get("cli_keys", [])
   127→            if isinstance(key, str) and str(key).strip()
   128→        ]
   129→        if dim_key:
   130→            issue_count = int(review_issue_counts.get(dim_key, 0))
   131→        elif cli_keys:
   132→            issue_count = int(sum(review_issue_counts.get(key, 0) for key in cli_keys))
   133→        else:
   134→            issue_count = 0
   135→        issue_style = "yellow" if strict_val < DEFAULT_TARGET_STRICT_SCORE and issue_count == 0 else "dim"
   136→        issue_tag = colorize(f" [open issues: {issue_count}]", issue_style)
   137→        print(
   138→            f"  {name:<22} {checks_str}  {score_val:5.1f}%  {strict_val:5.1f}%  {bar}  T{tier}  {'review'}{focus}{stale_tag}"
   139→            f"{placeholder_tag}{issue_tag}"
   140→        )
   141→
   142→
   143→__all__ = [
   144→    "find_lowest_dimension",
   145→    "open_review_issue_counts",
   146→    "render_objective_dimensions",
   147→    "render_subjective_dimensions",
   148→    "scorecard_subjective_entries_for_status",
   149→]
   150→
   151→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status/cmd.py"
}
```

> TOOL

tool_result Read
```
1→"""status command: score dashboard with per-tier progress."""
     2→
     3→from __future__ import annotations
     4→
     5→import argparse
     6→import json
     7→import logging
     8→
     9→from desloppify import state as state_mod
    10→from desloppify.app.commands.helpers.guardrails import print_triage_guardrail_info
    11→from desloppify.app.commands.helpers.lang import resolve_lang
    12→from desloppify.app.commands.helpers.queue_progress import (
    13→    ScoreDisplayMode,
    14→    format_queue_block,
    15→    get_plan_start_strict,
    16→    plan_aware_queue_breakdown,
    17→    print_frozen_score_with_queue_context,
    18→    print_objective_drained_banner,
    19→    score_display_mode,
    20→)
    21→from desloppify.app.commands.helpers.runtime import command_runtime
    22→from desloppify.base.config import target_strict_score_from_config
    23→from desloppify.app.commands.helpers.state import require_completed_scan
    24→from desloppify.app.commands.next.render_nudges import (
    25→    render_uncommitted_reminder,
    26→)
    27→from desloppify.app.commands.scan.reporting import (
    28→    dimensions as reporting_dimensions_mod,
    29→)
    30→from desloppify.base.exception_sets import PLAN_LOAD_EXCEPTIONS
    31→from desloppify.base.output.terminal import colorize
    32→from desloppify.app.skill_docs import check_skill_version
    33→from desloppify.base.tooling import check_config_staleness
    34→from desloppify.engine._scoring.results.core import compute_health_breakdown
    35→from desloppify.engine._work_queue.context import queue_context
    36→from desloppify.engine.plan import load_plan
    37→from desloppify.engine.planning.scorecard_projection import (
    38→    scorecard_dimensions_payload,
    39→)
    40→from desloppify.intelligence.narrative.core import NarrativeContext, compute_narrative
    41→
    42→from .render import (
    43→    print_open_scope_breakdown,
    44→    print_scan_completeness,
    45→    print_scan_metrics,
    46→    score_summary_lines,
    47→    show_agent_plan,
    48→    show_dimension_table,
    49→    show_focus_suggestion,
    50→    show_ignore_summary,
    51→    show_review_summary,
    52→    show_structural_areas,
    53→    show_subjective_followup,
    54→    show_tier_progress_table,
    55→    write_status_query,
    56→)
    57→
    58→_logger = logging.getLogger(__name__)
    59→
    60→
    61→def cmd_status(args: argparse.Namespace) -> None:
    62→    """Show score dashboard."""
    63→    runtime = command_runtime(args)
    64→    state = runtime.state
    65→    config = runtime.config
    66→
    67→    stats = state.get("stats", {})
    68→    dim_scores = state.get("dimension_scores", {}) or {}
    69→    scorecard_dims = scorecard_dimensions_payload(state, dim_scores=dim_scores)
    70→    subjective_measures = [row for row in scorecard_dims if row.get("subjective")]
    71→    suppression = state_mod.suppression_metrics(state)
    72→
    73→    if getattr(args, "json", False):
    74→        print(
    75→            json.dumps(
    76→                _status_json_payload(
    77→                    state,
    78→                    stats,
    79→                    dim_scores,
    80→                    scorecard_dims,
    81→                    subjective_measures,
    82→                    suppression,
    83→                ),
    84→                indent=2,
    85→            )
    86→        )
    87→        return
    88→
    89→    if not require_completed_scan(state):
    90→        return
    91→
    92→    skill_warning = check_skill_version()
    93→    if skill_warning:
    94→        print(colorize(f"  {skill_warning}", "yellow"))
    95→    config_warning = check_config_staleness(config)
    96→    if config_warning:
    97→        print(colorize(f"  {config_warning}", "yellow"))
    98→
    99→    scores = state_mod.score_snapshot(state)
   100→    by_tier = stats.get("by_tier", {})
   101→    target_strict_score = target_strict_score_from_config(config)
   102→
   103→    lang = resolve_lang(args)
   104→    lang_name = lang.name if lang else None
   105→
   106→    # Load living plan for plan-aware rendering and narrative
   107→    _plan = load_plan()
   108→    _plan_active = _plan if (
   109→        _plan.get("queue_order") or _plan.get("clusters")
   110→    ) else None
   111→
   112→    print_triage_guardrail_info(plan=_plan, state=state)
   113→
   114→    narrative = compute_narrative(
   115→        state,
   116→        context=NarrativeContext(lang=lang_name, command="status", plan=_plan_active),
   117→    )
   118→    ignores = config.get("ignore", [])
   119→
   120→    # Build unified context once — plan, target_strict, and policy all agree.
   121→    _ctx = queue_context(
   122→        state,
   123→        config=config,
   124→        plan=_plan_active,
   125→        target_strict=target_strict_score,
   126→    )
   127→
   128→    _breakdown = _print_score_section(state, scores, _plan, target_strict_score, _ctx)
   129→    print_scan_metrics(state)
   130→    print_open_scope_breakdown(state)
   131→    print_scan_completeness(state)
   132→
   133→    _objective_backlog = _ctx.policy.objective_count
   134→
   135→    if dim_scores:
   136→        show_dimension_table(state, dim_scores, objective_backlog=_objective_backlog)
   137→        reporting_dimensions_mod.show_score_model_breakdown(
   138→            state,
   139→            dim_scores=dim_scores,
   140→        )
   141→    else:
   142→        show_tier_progress_table(by_tier)
   143→
   144→    if dim_scores:
   145→        show_focus_suggestion(dim_scores, state, plan=_plan_active)
   146→        show_subjective_followup(
   147→            state,
   148→            dim_scores,
   149→            target_strict_score=target_strict_score,
   150→            objective_backlog=_objective_backlog,
   151→        )
   152→
   153→    show_review_summary(state)
   154→    show_structural_areas(state)
   155→
   156→    # Commit tracking reminder
   157→    try:
   158→        render_uncommitted_reminder(_plan_active)
   159→    except PLAN_LOAD_EXCEPTIONS:
   160→        _logger.debug("commit tracking reminder skipped", exc_info=True)
   161→
   162→    show_agent_plan(narrative, plan=_plan_active)
   163→
   164→    if narrative.get("headline"):
   165→        print(colorize(f"  -> {narrative['headline']}", "cyan"))
   166→        print()
   167→
   168→    if ignores:
   169→        show_ignore_summary(ignores, suppression)
   170→
   171→    review_age = config.get("review_max_age_days", 30)
   172→    if review_age != 30:
   173→        label = "never" if review_age == 0 else f"{review_age} days"
   174→        print(colorize(f"  Review staleness: {label}", "dim"))
   175→    print()
   176→
   177→    write_status_query(
   178→        state=state,
   179→        stats=stats,
   180→        by_tier=by_tier,
   181→        dim_scores=dim_scores,
   182→        scorecard_dims=scorecard_dims,
   183→        subjective_measures=subjective_measures,
   184→        suppression=suppression,
   185→        narrative=narrative,
   186→        ignores=ignores,
   187→        overall_score=scores.overall,
   188→        objective_score=scores.objective,
   189→        strict_score=scores.strict,
   190→        verified_strict_score=scores.verified,
   191→        plan=_plan_active,
   192→    )
   193→
   194→
   195→def _print_score_section(state, scores, plan, target_strict_score, ctx=None):
   196→    """Print score header: frozen plan-start or live score with queue breakdown."""
   197→    plan_start_strict = get_plan_start_strict(plan)
   198→
   199→    # Build breakdown — needed for both display mode decision and rendering.
   200→    breakdown = None
   201→    try:
   202→        breakdown = plan_aware_queue_breakdown(state, plan, context=ctx)
   203→    except PLAN_LOAD_EXCEPTIONS as exc:
   204→        _logger.debug("Plan-aware queue count failed: %s", exc)
   205→
   206→    mode = score_display_mode(breakdown, plan_start_strict)
   207→
   208→    if mode is ScoreDisplayMode.FROZEN:
   209→        print_frozen_score_with_queue_context(
   210→            breakdown,
   211→            frozen_strict=plan_start_strict,
   212→            live_score=scores.strict,
   213→        )
   214→    else:
   215→        # LIVE or PHASE_TRANSITION: show current live scores
   216→        for line, style in score_summary_lines(
   217→            overall_score=scores.overall,
   218→            objective_score=scores.objective,
   219→            strict_score=scores.strict,
   220→            verified_strict_score=scores.verified,
   221→            target_strict=target_strict_score,
   222→        ):
   223→            print(colorize(line, style))
   224→        if breakdown is not None and breakdown.queue_total > 0:
   225→            block = format_queue_block(breakdown)
   226→            for text, style in block:
   227→                print(colorize(text, style))
   228→        if mode is ScoreDisplayMode.PHASE_TRANSITION:
   229→            print_objective_drained_banner(plan_start_strict, breakdown.queue_total, breakdown)
   230→
   231→    return breakdown
   232→
   233→
   234→def _status_json_payload(
   235→    state: dict,
   236→    stats: dict,
   237→    dim_scores: dict,
   238→    scorecard_dims: list[dict],
   239→    subjective_measures: list[dict],
   240→    suppression: dict,
   241→) -> dict:
   242→    scores = state_mod.score_snapshot(state)
   243→    issues = state.get("issues", {})
   244→    open_scope = (
   245→        state_mod.open_scope_breakdown(issues, state.get("scan_path"))
   246→        if isinstance(issues, dict)
   247→        else None
   248→    )
   249→    return {
   250→        "overall_score": scores.overall,
   251→        "objective_score": scores.objective,
   252→        "strict_score": scores.strict,
   253→        "verified_strict_score": scores.verified,
   254→        "dimension_scores": dim_scores,
   255→        "score_breakdown": compute_health_breakdown(dim_scores) if dim_scores else None,
   256→        "scorecard_dimensions": scorecard_dims,
   257→        "subjective_measures": subjective_measures,
   258→        "potentials": state.get("potentials"),
   259→        "codebase_metrics": state.get("codebase_metrics"),
   260→        "stats": stats,
   261→        "open_scope": open_scope,
   262→        "suppression": suppression,
   263→        "scan_count": state.get("scan_count", 0),
   264→        "last_scan": state.get("last_scan"),
   265→    }
   266→
   267→__all__ = [
   268→    "cmd_status",
   269→    "show_dimension_table",
   270→    "show_focus_suggestion",
   271→    "show_ignore_summary",
   272→    "show_structural_areas",
   273→    "show_subjective_followup",
   274→]
   275→
```

> AGENT

Perfect! I have comprehensive information. Let me compile my findings.

## Summary

Here are all the import statements referencing `scorecard_projection` and the directory structure findings:

### Directory Status
- **`app/planning/` does NOT exist** - there is no `app/planning/` directory
- **`engine/planning/` DOES exist** at `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/`

### All Import Statements

**1. Engine-layer imports (under `engine/`):**
- `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/synthetic.py:24`
  ```python
  from desloppify.engine.planning.scorecard_projection import (
      all_subjective_entries,
  )
  ```

- `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/stale_policy.py:10`
  ```python
  from desloppify.engine.planning.scorecard_projection import all_subjective_entries
  ```

**2. App-layer imports (under `app/`):**
- `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/scan/reporting/agent_context.py:26`
  ```python
  from desloppify.engine.planning import scorecard_projection as scorecard_projection_mod
  ```

- `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/scan/reporting/dimensions.py:20`
  ```python
  from desloppify.engine.planning.scorecard_projection import (
      dimension_cli_key,
      scorecard_dimension_cli_keys,
      scorecard_dimension_rows,
      scorecard_subjective_entries,
  )
  ```

- `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next/cmd.py:34`
  ```python
  from desloppify.engine.planning.scorecard_projection import (
      scorecard_dimensions_payload,
  )
  ```

- `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next/render_support.py:10`
  ```python
  from desloppify.engine.planning.scorecard_projection import (
      scorecard_subjective_entries,
  )
  ```

- `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status/render_dimensions.py:10`
  ```python
  from desloppify.engine.planning.scorecard_projection import (
      scorecard_subjective_entries,
  )
  ```

- `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status/cmd.py:37`
  ```python
  from desloppify.engine.planning.scorecard_projection import (
      scorecard_dimensions_payload,
  )
  ```

**3. Test imports:**
- `/Users/user_c042661f/Documents/desloppify/desloppify/tests/scoring/test_scorecard_projection_direct.py:5`
  ```python
  from desloppify.engine.planning.scorecard_projection import (
      dimension_cli_key,
      scorecard_dimension_cli_keys,
      scorecard_dimensions_payload,
      scorecard_subjective_entries,
  )
  ```

### Analysis
- **Total imports:** 10 files (2 engine-layer + 7 app-layer + 1 test)
- **Engine-layer files importing from scorecard_projection:** 2 files (both under `engine/`)
  - `engine/_work_queue/synthetic.py`
  - `engine/_plan/stale_policy.py`
- **Functions imported:** `all_subjective_entries`, `dimension_cli_key`, `scorecard_dimension_cli_keys`, `scorecard_dimension_rows`, `scorecard_subjective_entries`, `scorecard_dimensions_payload`

> DEVELOPER

Read and understand these files, then make the changes for Step 1 of the plan:

1. Read `desloppify/engine/_plan/plan_public_exports.py` - this should be deleted
2. Read `desloppify/engine/_plan/__init__.py` - remove references to plan_public_exports and engine.plan shim
3. Verify no other files import from plan_public_exports

Changes:
- Delete `desloppify/engine/_plan/plan_public_exports.py`
- Edit `desloppify/engine/_plan/__init__.py` to remove references to the deleted file

After making changes, run: `python -m pytest desloppify/tests/engine/ -q`

> AGENT

Let me read the relevant files first.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/plan_public_exports.py"
}
```

> TOOL

tool_result Read
```
1→"""Minimal public export list for deprecated ``desloppify.engine.plan`` shim."""
     2→
     3→from __future__ import annotations
     4→
     5→# Keep ``engine.plan`` intentionally small. New code should import from
     6→# ``engine.plan_state``, ``engine.plan_ops``, ``engine.plan_queue``, and
     7→# ``engine.plan_triage`` directly.
     8→PLAN_PUBLIC_EXPORTS = [
     9→    "PlanModel",
    10→    "empty_plan",
    11→    "load_plan",
    12→    "save_plan",
    13→    "has_living_plan",
    14→    "triage_phase_banner",
    15→]
    16→
    17→
    18→__all__ = ["PLAN_PUBLIC_EXPORTS"]
    19→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py"
}
```

> TOOL

tool_result Read
```
1→"""Internal plan implementation package (not a public import surface).
     2→
     3→This package owns plan internals: schema, operations, triage internals, and
     4→sync policy. Callers should route through focused public facades
     5→(``engine.plan_state``, ``engine.plan_ops``, ``engine.plan_queue``,
     6→``engine.plan_triage``) rather than importing from ``engine._plan`` directly.
     7→
     8→Subpackages:
     9→- schema: PlanState TypedDict and migration logic
    10→- operations: queue/skip/cluster/meta/lifecycle mutations
    11→- triage: staged triage shared contracts + legacy import bridges
    12→- policy: subjective/stale/project policy helpers
    13→- sync: queue sync modules (context, dimensions, triage, workflow)
    14→
    15→Legacy compatibility bridges live only under ``engine._plan.compat``
    16→(for example ``compat.operations_skip`` / ``compat.operations_meta`` /
    17→``compat.operations_lifecycle`` / ``compat.project_policy`` /
    18→``compat.triage``) and delegate to grouped canonical implementations.
    19→
    20→Legacy whole-plan triage module names (``epic_triage_prompt``,
    21→``epic_triage_parsing``, ``epic_triage_apply``, ``epic_triage_dismiss``)
    22→also remain as compatibility bridges and delegate to
    23→``engine._plan.compat.triage.*``.
    24→
    25→Other modules:
    26→- persistence: JSON read/write with atomic saves
    27→- reconcile: post-scan plan↔state synchronization
    28→- auto_cluster: automatic issue clustering
    29→- commit_tracking: git commit↔plan-item linking
    30→
    31→"""
    32→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "plan_public_exports",
  "path": "/Users/user_c042661f/Documents/desloppify"
}
```

> TOOL

tool_result Grep
```
No files found
```

> DEVELOPER

I need to understand the triage bridge structure. Read these files and report their full contents:

1. `desloppify/engine/_plan/epic_triage_apply.py`
2. `desloppify/engine/_plan/epic_triage_dismiss.py`
3. `desloppify/engine/_plan/epic_triage_parsing.py`
4. `desloppify/engine/_plan/epic_triage_prompt.py`
5. `desloppify/engine/_plan/triage/__init__.py` (if exists)
6. `desloppify/engine/_plan/compat/` - list all files and read each one
7. `desloppify/engine/_plan/triage/` - list all files and read each .py file
8. `desloppify/engine/plan_triage.py`
9. `desloppify/engine/_plan/__init__.py`

Also search for all imports of `epic_triage_apply`, `epic_triage_dismiss`, `epic_triage_parsing`, `epic_triage_prompt`, and `compat.triage` across the codebase.

Report the full content of each file and all import locations found.

> AGENT

No files import from `plan_public_exports`. Let me also check if `engine.plan` shim exists and references it.

> TOOL

tool_use Grep
```json
{
  "pattern": "PLAN_PUBLIC_EXPORTS",
  "path": "/Users/user_c042661f/Documents/desloppify"
}
```

> TOOL

tool_result Grep
```
Found 1 file
desloppify/engine/_plan/plan_public_exports.py
```

> AGENT

I'll systematically read these files and search for imports. Let me start with reading the files and searching for imports in parallel.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py"
}
```

> TOOL

tool_result Read
```
1→"""Compatibility bridge to grouped triage apply helpers.
     2→
     3→Canonical implementation now lives in ``engine._plan.compat.triage.apply``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.apply")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py"
}
```

> TOOL

tool_result Read
```
1→"""Compatibility bridge to grouped triage dismissal helpers.
     2→
     3→Canonical implementation now lives in ``engine._plan.compat.triage.dismiss``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.dismiss")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py"
}
```

> TOOL

tool_result Read
```
1→"""Compatibility bridge to grouped triage parsing helpers.
     2→
     3→Canonical implementation now lives in ``engine._plan.compat.triage.parsing``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.parsing")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py"
}
```

> TOOL

tool_result Read
```
1→"""Compatibility bridge to grouped triage prompt contracts.
     2→
     3→Canonical implementation now lives in ``engine._plan.compat.triage.prompt``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.prompt")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "engine\\.plan",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py"
}
```

> TOOL

tool_result Grep
```
Found 1 file
desloppify/engine/_plan/__init__.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py"
}
```

> TOOL

tool_result Read
```
1→"""Internal plan implementation package (not a public import surface).
     2→
     3→This package owns plan internals: schema, operations, triage internals, and
     4→sync policy. Callers should route through focused public facades
     5→(``engine.plan_state``, ``engine.plan_ops``, ``engine.plan_queue``,
     6→``engine.plan_triage``) rather than importing from ``engine._plan`` directly.
     7→
     8→Subpackages:
     9→- schema: PlanState TypedDict and migration logic
    10→- operations: queue/skip/cluster/meta/lifecycle mutations
    11→- triage: staged triage shared contracts + legacy import bridges
    12→- policy: subjective/stale/project policy helpers
    13→- sync: queue sync modules (context, dimensions, triage, workflow)
    14→
    15→Legacy compatibility bridges live only under ``engine._plan.compat``
    16→(for example ``compat.operations_skip`` / ``compat.operations_meta`` /
    17→``compat.operations_lifecycle`` / ``compat.project_policy`` /
    18→``compat.triage``) and delegate to grouped canonical implementations.
    19→
    20→Legacy whole-plan triage module names (``epic_triage_prompt``,
    21→``epic_triage_parsing``, ``epic_triage_apply``, ``epic_triage_dismiss``)
    22→also remain as compatibility bridges and delegate to
    23→``engine._plan.compat.triage.*``.
    24→
    25→Other modules:
    26→- persistence: JSON read/write with atomic saves
    27→- reconcile: post-scan plan↔state synchronization
    28→- auto_cluster: automatic issue clustering
    29→- commit_tracking: git commit↔plan-item linking
    30→
    31→"""
    32→
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/ 2>/dev/null || echo \"Directory does not exist\""
}
```

> TOOL

tool_result Bash
```
total 8
drwxr-xr-x   5 user_c042661f  staff  160 Mar 10 17:04 .
drwxr-xr-x  30 user_c042661f  staff  960 Mar 10 13:48 ..
-rw-r--r--   1 user_c042661f  staff  289 Mar 10 17:04 __init__.py
drwxr-xr-x@  7 user_c042661f  staff  224 Mar 10 17:05 __pycache__
drwxr-xr-x   9 user_c042661f  staff  288 Mar 10 14:26 triage
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/ 2>/dev/null || echo \"Directory does not exist\""
}
```

> TOOL

tool_result Bash
```
total 64
drwxr-xr-x  10 user_c042661f  staff   320 Mar 10 14:23 .
drwxr-xr-x  30 user_c042661f  staff   960 Mar 10 13:48 ..
-rw-r--r--   1 user_c042661f  staff   492 Mar 10 15:46 __init__.py
drwxr-xr-x@  9 user_c042661f  staff   288 Mar 10 15:48 __pycache__
-rw-r--r--   1 user_c042661f  staff   394 Mar 10 14:23 apply.py
-rw-r--r--   1 user_c042661f  staff   391 Mar 10 14:21 core.py
-rw-r--r--   1 user_c042661f  staff   402 Mar 10 14:23 dismiss.py
-rw-r--r--   1 user_c042661f  staff   400 Mar 10 14:23 parsing.py
-rw-r--r--   1 user_c042661f  staff  5544 Mar 10 10:24 playbook.py
-rw-r--r--   1 user_c042661f  staff   397 Mar 10 14:23 prompt.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/plan_triage.py"
}
```

> TOOL

tool_result Read
```
1→"""Focused public plan API for triage orchestration surfaces."""
     2→
     3→from __future__ import annotations
     4→
     5→from desloppify.engine._plan.constants import (
     6→    TRIAGE_IDS,
     7→    TRIAGE_PREFIX,
     8→    TRIAGE_STAGE_IDS,
     9→)
    10→from desloppify.engine._plan.compat.triage.core import (
    11→    TriageInput,
    12→    build_triage_prompt,
    13→    collect_triage_input,
    14→    detect_recurring_patterns,
    15→    extract_issue_citations,
    16→)
    17→from desloppify.engine._plan.triage.playbook import (
    18→    TRIAGE_CMD_CLUSTER_ADD,
    19→    TRIAGE_CMD_CLUSTER_CREATE,
    20→    TRIAGE_CMD_CLUSTER_ENRICH,
    21→    TRIAGE_CMD_CLUSTER_ENRICH_COMPACT,
    22→    TRIAGE_CMD_CLUSTER_STEPS,
    23→    TRIAGE_CMD_COMPLETE,
    24→    TRIAGE_CMD_COMPLETE_VERBOSE,
    25→    TRIAGE_CMD_CONFIRM_EXISTING,
    26→    TRIAGE_CMD_ENRICH,
    27→    TRIAGE_CMD_OBSERVE,
    28→    TRIAGE_CMD_ORGANIZE,
    29→    TRIAGE_CMD_REFLECT,
    30→    TRIAGE_CMD_RUN_STAGES_CLAUDE,
    31→    TRIAGE_CMD_RUN_STAGES_CODEX,
    32→    TRIAGE_CMD_SENSE_CHECK,
    33→    TRIAGE_STAGE_DEPENDENCIES,
    34→    TRIAGE_STAGE_LABELS,
    35→    triage_manual_stage_command,
    36→    triage_run_stages_command,
    37→    triage_runner_commands,
    38→)
    39→from desloppify.engine._plan.sync.triage_start_policy import (
    40→    TriageStartDecision,
    41→    decide_triage_start,
    42→)
    43→from desloppify.engine.plan_queue import has_objective_backlog
    44→from desloppify.engine.plan_state import PlanModel, ensure_plan_defaults
    45→
    46→
    47→def triage_phase_banner(plan: PlanModel, state: dict | None = None) -> str:
    48→    """Return a banner string describing triage status."""
    49→    ensure_plan_defaults(plan)
    50→    order = set(plan.get("queue_order", []))
    51→    has_triage = any(stage_id in order for stage_id in TRIAGE_IDS)
    52→    meta = plan.get("epic_triage_meta", {})
    53→    run_hint = (
    54→        f"Run: {TRIAGE_CMD_RUN_STAGES_CODEX} "
    55→        f"(or {TRIAGE_CMD_RUN_STAGES_CLAUDE})"
    56→    )
    57→
    58→    if not has_triage:
    59→        if meta.get("triage_recommended"):
    60→            return (
    61→                "TRIAGE RECOMMENDED — review issues changed since last triage. "
    62→                f"{run_hint}"
    63→            )
    64→        return ""
    65→
    66→    if state and has_objective_backlog(state, None):
    67→        return (
    68→            "TRIAGE PENDING — queued and will activate after objective work "
    69→            "is complete."
    70→        )
    71→    stages = meta.get("triage_stages", {})
    72→    completed = [
    73→        stage
    74→        for stage in ("observe", "reflect", "organize", "enrich", "sense-check")
    75→        if stage in stages
    76→    ]
    77→    if completed:
    78→        return (
    79→            f"TRIAGE MODE ({len(completed)}/5 stages complete) — "
    80→            f"complete all stages to exit. {run_hint}"
    81→        )
    82→    return (
    83→        "TRIAGE MODE — review issues need analysis before fixing. "
    84→        f"{run_hint}"
    85→    )
    86→
    87→__all__ = [
    88→    "TRIAGE_CMD_CLUSTER_ADD",
    89→    "TRIAGE_CMD_CLUSTER_CREATE",
    90→    "TRIAGE_CMD_CLUSTER_ENRICH",
    91→    "TRIAGE_CMD_CLUSTER_ENRICH_COMPACT",
    92→    "TRIAGE_CMD_CLUSTER_STEPS",
    93→    "TRIAGE_CMD_COMPLETE",
    94→    "TRIAGE_CMD_COMPLETE_VERBOSE",
    95→    "TRIAGE_CMD_CONFIRM_EXISTING",
    96→    "TRIAGE_CMD_ENRICH",
    97→    "TRIAGE_CMD_OBSERVE",
    98→    "TRIAGE_CMD_ORGANIZE",
    99→    "TRIAGE_CMD_REFLECT",
   100→    "TRIAGE_CMD_RUN_STAGES_CLAUDE",
   101→    "TRIAGE_CMD_RUN_STAGES_CODEX",
   102→    "TRIAGE_CMD_SENSE_CHECK",
   103→    "TRIAGE_IDS",
   104→    "TRIAGE_PREFIX",
   105→    "TRIAGE_STAGE_DEPENDENCIES",
   106→    "TRIAGE_STAGE_IDS",
   107→    "TRIAGE_STAGE_LABELS",
   108→    "TriageStartDecision",
   109→    "TriageInput",
   110→    "build_triage_prompt",
   111→    "collect_triage_input",
   112→    "decide_triage_start",
   113→    "detect_recurring_patterns",
   114→    "extract_issue_citations",
   115→    "triage_phase_banner",
   116→    "triage_manual_stage_command",
   117→    "triage_run_stages_command",
   118→    "triage_runner_commands",
   119→]
   120→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "from.*epic_triage_apply|import.*epic_triage_apply|from.*epic_triage_dismiss|import.*epic_triage_dismiss|from.*epic_triage_parsing|import.*epic_triage_parsing|from.*epic_triage_prompt|import.*epic_triage_prompt",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 5 files
desloppify/tests/engine/test_sync_split_modules_direct.py
desloppify/tests/plan/test_epic_triage_apply.py
desloppify/tests/plan/test_epic_triage_apply_edge_cases.py
desloppify/tests/plan/test_epic_triage_parsing_direct.py
desloppify/tests/commands/plan/test_triage_runner.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "from.*compat.*triage|import.*compat.*triage",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 12 files
desloppify/tests/engine/test_sync_split_modules_direct.py
desloppify/engine/plan_triage.py
desloppify/engine/_plan/epic_triage_dismiss.py
desloppify/engine/_plan/epic_triage_apply.py
desloppify/engine/_plan/epic_triage_parsing.py
desloppify/engine/_plan/epic_triage_prompt.py
desloppify/engine/_plan/compat/triage/core.py
desloppify/engine/_plan/triage/prompt.py
desloppify/engine/_plan/triage/dismiss.py
desloppify/engine/_plan/triage/parsing.py
desloppify/engine/_plan/triage/apply.py
desloppify/engine/_plan/triage/core.py
```

> AGENT

Now let me read the compat/triage files and the triage/ subpackage files:

> AGENT

`PLAN_PUBLIC_EXPORTS` is only referenced in the file itself. The `__init__.py` mentions `engine.plan` only in the docstring (which is fine - it's describing the architecture). There are no imports to remove from `__init__.py` - it's just a docstring.

Now let me delete the file and run tests.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/__init__.py"
}
```

> TOOL

tool_result Read
```
1→"""Legacy whole-plan triage runtime namespace.
     2→
     3→Canonical staged triage orchestration lives in ``app.commands.plan.triage``.
     4→The modules under ``engine._plan.compat.triage`` provide the legacy
     5→whole-plan triage implementation.
     6→"""
     7→
     8→from __future__ import annotations
     9→
    10→__all__ = ["triage"]
    11→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/apply.py"
}
```

> TOOL

tool_result Read
```
1→"""Plan mutation helpers for epic triage."""
     2→
     3→from __future__ import annotations
     4→
     5→from dataclasses import dataclass
     6→
     7→from desloppify.engine._plan.schema import (
     8→    EPIC_PREFIX,
     9→    Cluster,
    10→    PlanModel,
    11→    ensure_plan_defaults,
    12→)
    13→from desloppify.engine._plan.policy.stale import review_issue_snapshot_hash
    14→from desloppify.engine._state.schema import StateModel, utc_now
    15→
    16→from .dismiss import dismiss_triage_issues
    17→from .prompt import TriageResult
    18→
    19→
    20→@dataclass
    21→class TriageMutationResult:
    22→    """What changed when triage was applied to the plan."""
    23→
    24→    epics_created: int = 0
    25→    epics_updated: int = 0
    26→    epics_completed: int = 0
    27→    issues_dismissed: int = 0
    28→    issues_reassigned: int = 0
    29→    strategy_summary: str = ""
    30→    triage_version: int = 0
    31→    dry_run: bool = False
    32→
    33→
    34→def _epic_sort_key(epic_data: dict) -> int:
    35→    return int(epic_data.get("dependency_order", 999))
    36→
    37→
    38→def _normalized_epic_name(raw_name: str) -> str:
    39→    return raw_name if raw_name.startswith(EPIC_PREFIX) else f"{EPIC_PREFIX}{raw_name}"
    40→
    41→
    42→def _update_existing_epic_cluster(
    43→    existing: Cluster,
    44→    epic_data: dict,
    45→    *,
    46→    now: str,
    47→    version: int,
    48→) -> None:
    49→    existing["thesis"] = epic_data["thesis"]
    50→    existing["direction"] = epic_data["direction"]
    51→    existing["root_cause"] = epic_data.get("root_cause", "")
    52→    existing["issue_ids"] = epic_data["issue_ids"]
    53→    existing["dismissed"] = epic_data.get("dismissed", [])
    54→    existing["agent_safe"] = epic_data.get("agent_safe", False)
    55→    existing["dependency_order"] = epic_data["dependency_order"]
    56→    existing["action_steps"] = epic_data.get("action_steps", [])
    57→    existing["updated_at"] = now
    58→    existing["triage_version"] = version
    59→    existing["description"] = epic_data["thesis"]
    60→    # Don't overwrite in_progress status from agent
    61→    if existing.get("status") != "in_progress":
    62→        existing["status"] = epic_data.get("status", "pending")
    63→
    64→
    65→def _create_epic_cluster(
    66→    *,
    67→    epic_name: str,
    68→    epic_data: dict,
    69→    now: str,
    70→    version: int,
    71→) -> Cluster:
    72→    return {
    73→        "name": epic_name,
    74→        "description": epic_data["thesis"],
    75→        "issue_ids": epic_data["issue_ids"],
    76→        "auto": True,
    77→        "cluster_key": f"epic::{epic_name}",
    78→        "action": f"desloppify plan focus {epic_name}",
    79→        "user_modified": False,
    80→        "created_at": now,
    81→        "updated_at": now,
    82→        # Epic fields
    83→        "thesis": epic_data["thesis"],
    84→        "direction": epic_data["direction"],
    85→        "root_cause": epic_data.get("root_cause", ""),
    86→        "supersedes": [],
    87→        "dismissed": epic_data.get("dismissed", []),
    88→        "agent_safe": epic_data.get("agent_safe", False),
    89→        "dependency_order": epic_data["dependency_order"],
    90→        "action_steps": epic_data.get("action_steps", []),
    91→        "source_clusters": [],
    92→        "status": epic_data.get("status", "pending"),
    93→        "triage_version": version,
    94→    }
    95→
    96→
    97→def _upsert_triage_clusters(
    98→    *,
    99→    clusters: dict[str, Cluster],
   100→    triage: TriageResult,
   101→    now: str,
   102→    version: int,
   103→) -> tuple[int, int]:
   104→    created = 0
   105→    updated = 0
   106→    for epic_data in sorted(triage.epics, key=_epic_sort_key):
   107→        raw_name = epic_data["name"]
   108→        epic_name = _normalized_epic_name(raw_name)
   109→        existing = clusters.get(epic_name)
   110→        if existing and existing.get("thesis"):
   111→            _update_existing_epic_cluster(existing, epic_data, now=now, version=version)
   112→            updated += 1
   113→            continue
   114→        clusters[epic_name] = _create_epic_cluster(
   115→            epic_name=epic_name,
   116→            epic_data=epic_data,
   117→            now=now,
   118→            version=version,
   119→        )
   120→        created += 1
   121→    return created, updated
   122→
   123→
   124→def _reorder_queue_by_dependency(
   125→    *,
   126→    order: list[str],
   127→    triage: TriageResult,
   128→    dismissed_ids: list[str],
   129→) -> None:
   130→    epic_issue_ids: set[str] = set()
   131→    epic_ordered_ids: list[str] = []
   132→    dismissed_set = set(dismissed_ids)
   133→    for epic_data in sorted(triage.epics, key=_epic_sort_key):
   134→        for fid in epic_data["issue_ids"]:
   135→            if fid in epic_issue_ids or fid in dismissed_set:
   136→                continue
   137→            epic_issue_ids.add(fid)
   138→            epic_ordered_ids.append(fid)
   139→
   140→    non_epic_items = [fid for fid in order if fid not in epic_issue_ids]
   141→    order.clear()
   142→    order.extend(epic_ordered_ids)
   143→    order.extend(non_epic_items)
   144→
   145→
   146→def _set_triage_meta(
   147→    *,
   148→    plan: PlanModel,
   149→    state: StateModel,
   150→    triage: TriageResult,
   151→    now: str,
   152→    version: int,
   153→    dismissed_ids: list[str],
   154→    trigger: str,
   155→) -> None:
   156→    current_hash = review_issue_snapshot_hash(state)
   157→    open_review_ids = sorted(
   158→        fid
   159→        for fid, issue in state.get("issues", {}).items()
   160→        if issue.get("status") == "open"
   161→        and issue.get("detector") in ("review", "concerns")
   162→    )
   163→
   164→    plan["epic_triage_meta"] = {
   165→        "triaged_ids": open_review_ids,
   166→        "last_run": now,
   167→        "version": version,
   168→        "dismissed_ids": dismissed_ids,
   169→        "issue_snapshot_hash": current_hash,
   170→        "strategy_summary": triage.strategy_summary,
   171→        "trigger": trigger,
   172→    }
   173→
   174→
   175→def apply_triage_to_plan(
   176→    plan: PlanModel,
   177→    state: StateModel,
   178→    triage: TriageResult,
   179→    *,
   180→    trigger: str = "manual",
   181→) -> TriageMutationResult:
   182→    """Apply parsed triage result to the living plan.
   183→
   184→    1. Creates/updates triage-clusters in plan["clusters"]
   185→    2. Marks dismissed issues as triaged_out skips
   186→    3. Reorders queue_order to group epic members by dependency_order
   187→    4. Updates epic_triage_meta with snapshot hash
   188→    """
   189→    ensure_plan_defaults(plan)
   190→    now = utc_now()
   191→    result = TriageMutationResult()
   192→    result.strategy_summary = triage.strategy_summary
   193→
   194→    clusters = plan["clusters"]
   195→    skipped: dict = plan["skipped"]
   196→    order: list[str] = plan["queue_order"]
   197→    meta = plan.get("epic_triage_meta", {})
   198→    version = int(meta.get("version", 0)) + 1
   199→    result.triage_version = version
   200→
   201→    created, updated = _upsert_triage_clusters(
   202→        clusters=clusters,
   203→        triage=triage,
   204→        now=now,
   205→        version=version,
   206→    )
   207→    result.epics_created += created
   208→    result.epics_updated += updated
   209→
   210→    dismissed_ids, dismiss_count = dismiss_triage_issues(
   211→        triage=triage,
   212→        order=order,
   213→        skipped=skipped,
   214→        now=now,
   215→        version=version,
   216→        scan_count=int(state.get("scan_count", 0)),
   217→    )
   218→    result.issues_dismissed += dismiss_count
   219→
   220→    _reorder_queue_by_dependency(
   221→        order=order,
   222→        triage=triage,
   223→        dismissed_ids=dismissed_ids,
   224→    )
   225→
   226→    _set_triage_meta(
   227→        plan=plan,
   228→        state=state,
   229→        triage=triage,
   230→        now=now,
   231→        version=version,
   232→        dismissed_ids=dismissed_ids,
   233→        trigger=trigger,
   234→    )
   235→    plan["updated"] = now
   236→
   237→    return result
   238→
   239→__all__ = ["TriageMutationResult", "apply_triage_to_plan"]
   240→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/dismiss.py"
}
```

> TOOL

tool_result Read
```
1→"""Dismissal helpers for epic triage plan mutations."""
     2→
     3→from __future__ import annotations
     4→
     5→from .prompt import TriageResult
     6→
     7→
     8→def _triaged_out_payload(
     9→    *,
    10→    issue_id: str,
    11→    reason: str,
    12→    note: str | None,
    13→    now: str,
    14→    scan_count: int,
    15→) -> dict:
    16→    return {
    17→        "issue_id": issue_id,
    18→        "kind": "triaged_out",
    19→        "reason": reason,
    20→        "note": note,
    21→        "attestation": None,
    22→        "created_at": now,
    23→        "review_after": None,
    24→        "skipped_at_scan": scan_count,
    25→    }
    26→
    27→
    28→def dismiss_triage_issues(
    29→    *,
    30→    triage: TriageResult,
    31→    order: list[str],
    32→    skipped: dict,
    33→    now: str,
    34→    version: int,
    35→    scan_count: int,
    36→) -> tuple[list[str], int]:
    37→    """Move triage-dismissed issues out of queue and into skipped metadata."""
    38→    dismissed_ids: list[str] = []
    39→    dismiss_count = 0
    40→    for dismissed in triage.dismissed_issues:
    41→        issue_id = dismissed.issue_id
    42→        dismissed_ids.append(issue_id)
    43→        if issue_id in order:
    44→            order.remove(issue_id)
    45→        skipped[issue_id] = _triaged_out_payload(
    46→            issue_id=issue_id,
    47→            reason=dismissed.reason,
    48→            note=f"Dismissed by epic triage v{version}",
    49→            now=now,
    50→            scan_count=scan_count,
    51→        )
    52→        dismiss_count += 1
    53→
    54→    for epic_data in triage.epics:
    55→        for issue_id in epic_data.get("dismissed", []):
    56→            if issue_id in dismissed_ids or issue_id not in order:
    57→                continue
    58→            order.remove(issue_id)
    59→            dismissed_ids.append(issue_id)
    60→            skipped[issue_id] = _triaged_out_payload(
    61→                issue_id=issue_id,
    62→                reason=f"Dismissed by epic triage v{version}",
    63→                note=None,
    64→                now=now,
    65→                scan_count=scan_count,
    66→            )
    67→            dismiss_count += 1
    68→
    69→    return dismissed_ids, dismiss_count
    70→
    71→
    72→__all__ = ["dismiss_triage_issues"]
    73→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/parsing.py"
}
```

> TOOL

tool_result Read
```
1→"""Parsing helpers for epic triage output."""
     2→
     3→from __future__ import annotations
     4→
     5→import re
     6→
     7→from desloppify.engine._plan.schema import VALID_EPIC_DIRECTIONS
     8→
     9→from .prompt import ContradictionNote, DismissedIssue, TriageResult
    10→
    11→ISSUE_ID_RE = re.compile(r"[a-z_]+::[a-f0-9]{8,}")
    12→BRACKET_SHORT_ID_RE = re.compile(r"\[([a-z0-9_]{6,16})\]")
    13→
    14→def extract_issue_citations(text: str, valid_ids: set[str]) -> set[str]:
    15→    """Extract issue IDs cited in free text.
    16→
    17→    Matches full issue IDs (e.g. ``review::abcdef12``) or bare 8+ char
    18→    hex suffixes that correspond to a known issue.
    19→    """
    20→    if not text or not valid_ids:
    21→        return set()
    22→
    23→    cited: set[str] = set()
    24→
    25→    # Prefer exact literal references for modern hierarchical IDs.
    26→    for valid_id in valid_ids:
    27→        if valid_id in text:
    28→            cited.add(valid_id)
    29→
    30→    # Support bracketed short hashes used in queue displays, e.g. [planmode].
    31→    short_map: dict[str, str] = {}
    32→    ambiguous_short: set[str] = set()
    33→    for valid_id in valid_ids:
    34→        suffix = valid_id.rsplit("::", 1)[-1]
    35→        short = suffix[:8].lower()
    36→        if not short:
    37→            continue
    38→        existing = short_map.get(short)
    39→        if existing is None:
    40→            short_map[short] = valid_id
    41→        elif existing != valid_id:
    42→            ambiguous_short.add(short)
    43→
    44→    for short in ambiguous_short:
    45→        short_map.pop(short, None)
    46→
    47→    for short in BRACKET_SHORT_ID_RE.findall(text.lower()):
    48→        mapped = short_map.get(short)
    49→        if mapped:
    50→            cited.add(mapped)
    51→
    52→    # Match full issue IDs
    53→    for match in ISSUE_ID_RE.finditer(text):
    54→        candidate = match.group()
    55→        if candidate in valid_ids:
    56→            cited.add(candidate)
    57→    # Match 8+ char hex suffixes
    58→    for token in re.findall(r"[0-9a-f]{8,}", text):
    59→        for valid_id in valid_ids:
    60→            if valid_id.endswith("::" + token):
    61→                cited.add(valid_id)
    62→                break
    63→    return cited
    64→
    65→
    66→def _parse_action_steps(raw_steps: object) -> list[dict]:
    67→    steps: list[dict] = []
    68→    if not isinstance(raw_steps, list):
    69→        return steps
    70→    for raw_step in raw_steps:
    71→        if isinstance(raw_step, dict):
    72→            title = str(raw_step.get("title", "")).strip()
    73→            if not title:
    74→                continue
    75→            step: dict = {"title": title}
    76→            detail = raw_step.get("detail")
    77→            if isinstance(detail, str) and detail.strip():
    78→                step["detail"] = detail.strip()
    79→            refs = raw_step.get("issue_refs")
    80→            if isinstance(refs, list):
    81→                normalized_refs = [str(ref).strip() for ref in refs if str(ref).strip()]
    82→                if normalized_refs:
    83→                    step["issue_refs"] = normalized_refs
    84→            done = raw_step.get("done")
    85→            if isinstance(done, bool):
    86→                step["done"] = done
    87→            steps.append(step)
    88→            continue
    89→        if isinstance(raw_step, str) and raw_step.strip():
    90→            # Legacy fallback for historical prompts that emitted string-only steps.
    91→            steps.append({"title": raw_step.strip()})
    92→    return steps
    93→
    94→
    95→def parse_triage_result(raw: dict, valid_ids: set[str]) -> TriageResult:
    96→    """Parse and validate raw LLM output into a TriageResult.
    97→
    98→    Invalid issue IDs are silently dropped from epics and dismissals.
    99→    """
   100→    strategy_summary = str(raw.get("strategy_summary", ""))
   101→
   102→    epics: list[dict] = []
   103→    for raw_epic in raw.get("epics", []):
   104→        if not isinstance(raw_epic, dict):
   105→            continue
   106→        name = str(raw_epic.get("name", "")).strip()
   107→        if not name:
   108→            continue
   109→        # Validate direction
   110→        direction = str(raw_epic.get("direction", "simplify")).strip()
   111→        if direction not in VALID_EPIC_DIRECTIONS:
   112→            direction = "simplify"
   113→        # Filter to valid issue IDs
   114→        issue_ids = [
   115→            fid for fid in raw_epic.get("issue_ids", [])
   116→            if isinstance(fid, str) and fid in valid_ids
   117→        ]
   118→        dismissed = [
   119→            fid for fid in raw_epic.get("dismissed", [])
   120→            if isinstance(fid, str) and fid in valid_ids
   121→        ]
   122→        action_steps = _parse_action_steps(raw_epic.get("action_steps", []))
   123→
   124→        epics.append({
   125→            "name": name,
   126→            "thesis": str(raw_epic.get("thesis", "")),
   127→            "direction": direction,
   128→            "root_cause": str(raw_epic.get("root_cause", "")),
   129→            "issue_ids": issue_ids,
   130→            "dismissed": dismissed,
   131→            "agent_safe": bool(raw_epic.get("agent_safe", False)),
   132→            "dependency_order": int(raw_epic.get("dependency_order", 999)),
   133→            "action_steps": action_steps,
   134→            "status": str(raw_epic.get("status", "pending")),
   135→        })
   136→
   137→    dismissed_issues: list[DismissedIssue] = []
   138→    for d in raw.get("dismissed_issues", []):
   139→        if not isinstance(d, dict):
   140→            continue
   141→        fid = str(d.get("issue_id", ""))
   142→        if fid in valid_ids:
   143→            dismissed_issues.append(
   144→                DismissedIssue(issue_id=fid, reason=str(d.get("reason", "")))
   145→            )
   146→
   147→    contradiction_notes: list[ContradictionNote] = []
   148→    for c in raw.get("contradiction_notes", []):
   149→        if not isinstance(c, dict):
   150→            continue
   151→        contradiction_notes.append(ContradictionNote(
   152→            kept=str(c.get("kept", "")),
   153→            dismissed=str(c.get("dismissed", "")),
   154→            reason=str(c.get("reason", "")),
   155→        ))
   156→
   157→    priority_rationale = str(raw.get("priority_rationale", ""))
   158→
   159→    return TriageResult(
   160→        strategy_summary=strategy_summary,
   161→        epics=epics,
   162→        dismissed_issues=dismissed_issues,
   163→        contradiction_notes=contradiction_notes,
   164→        priority_rationale=priority_rationale,
   165→    )
   166→
   167→__all__ = ["ISSUE_ID_RE", "extract_issue_citations", "parse_triage_result"]
   168→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/prompt.py"
}
```

> TOOL

tool_result Read
```
1→"""Prompt/data contracts for legacy whole-plan triage orchestration.
     2→
     3→Primary runtime triage now uses staged command flow under
     4→``app.commands.plan.triage``; this module is the compatibility implementation
     5→for consumers still using bridged legacy import paths.
     6→"""
     7→
     8→from __future__ import annotations
     9→
    10→from dataclasses import dataclass, field
    11→from typing import Any
    12→
    13→from desloppify.engine._plan.schema import (
    14→    Cluster,
    15→    PlanModel,
    16→    ensure_plan_defaults,
    17→    triage_clusters,
    18→)
    19→from desloppify.engine._state.schema import StateModel
    20→
    21→
    22→@dataclass
    23→class TriageInput:
    24→    """All data needed to produce/update triage clusters (legacy schema)."""
    25→
    26→    open_issues: dict[str, dict]       # id -> issue (review + concerns)
    27→    mechanical_issues: dict[str, dict]  # id -> issue (non-review, for context)
    28→    existing_epics: dict[str, Cluster]    # legacy field name; values are clusters
    29→    dimension_scores: dict[str, Any]      # for context
    30→    new_since_last: set[str]             # issue IDs new since last triage
    31→    resolved_since_last: set[str]        # issue IDs resolved since last
    32→    previously_dismissed: list[str]      # IDs dismissed in prior triage
    33→    triage_version: int                  # next version number
    34→    resolved_issues: dict[str, dict]   # full issue objects for resolved IDs
    35→    completed_clusters: list[dict]       # clusters completed since last triage
    36→
    37→    @property
    38→    def existing_clusters(self) -> dict[str, Cluster]:
    39→        """Canonical alias for ``existing_epics`` used by staged triage docs."""
    40→        return self.existing_epics
    41→
    42→@dataclass
    43→class DismissedIssue:
    44→    """A issue the LLM says doesn't make sense."""
    45→
    46→    issue_id: str
    47→    reason: str
    48→
    49→@dataclass
    50→class ContradictionNote:
    51→    """Record of a resolved contradiction."""
    52→
    53→    kept: str
    54→    dismissed: str
    55→    reason: str
    56→
    57→@dataclass
    58→class TriageResult:
    59→    """Parsed and validated LLM triage output."""
    60→
    61→    strategy_summary: str
    62→    epics: list[dict]
    63→    dismissed_issues: list[DismissedIssue] = field(default_factory=list)
    64→    contradiction_notes: list[ContradictionNote] = field(default_factory=list)
    65→    priority_rationale: str = ""
    66→
    67→
    68→def _issue_dimension(issue: dict) -> str:
    69→    detail = issue.get("detail", {})
    70→    if isinstance(detail, dict):
    71→        dimension = detail.get("dimension", "")
    72→        if isinstance(dimension, str):
    73→            return dimension
    74→    return ""
    75→
    76→
    77→def _recurring_dimensions(
    78→    open_issues: dict[str, dict],
    79→    resolved_issues: dict[str, dict],
    80→) -> dict[str, dict[str, list[str]]]:
    81→    open_by_dim: dict[str, list[str]] = {}
    82→    for issue_id, issue in open_issues.items():
    83→        dimension = _issue_dimension(issue)
    84→        if dimension:
    85→            open_by_dim.setdefault(dimension, []).append(issue_id)
    86→
    87→    resolved_by_dim: dict[str, list[str]] = {}
    88→    for issue_id, issue in resolved_issues.items():
    89→        dimension = _issue_dimension(issue)
    90→        if dimension:
    91→            resolved_by_dim.setdefault(dimension, []).append(issue_id)
    92→
    93→    recurring: dict[str, dict[str, list[str]]] = {}
    94→    for dimension in sorted(set(open_by_dim) & set(resolved_by_dim)):
    95→        recurring[dimension] = {
    96→            "open": sorted(open_by_dim[dimension]),
    97→            "resolved": sorted(resolved_by_dim[dimension]),
    98→        }
    99→    return recurring
   100→
   101→def collect_triage_input(plan: PlanModel, state: StateModel) -> TriageInput:
   102→    """Gather all data needed for the triage LLM prompt."""
   103→    ensure_plan_defaults(plan)
   104→    issues = state.get("issues", {})
   105→    meta = plan.get("epic_triage_meta", {})
   106→    epics = triage_clusters(plan)
   107→
   108→    open_review: dict[str, dict] = {}
   109→    open_mechanical: dict[str, dict] = {}
   110→    for fid, f in issues.items():
   111→        if f.get("status") != "open":
   112→            continue
   113→        if f.get("detector") in ("review", "concerns"):
   114→            open_review[fid] = f
   115→        else:
   116→            open_mechanical[fid] = f
   117→
   118→    triaged_ids = set(meta.get("triaged_ids", []))
   119→    current_review_ids = set(open_review.keys())
   120→    new_since = current_review_ids - triaged_ids
   121→    resolved_since = triaged_ids - current_review_ids
   122→    previously_dismissed = list(meta.get("dismissed_ids", []))
   123→    version = int(meta.get("version", 0)) + 1
   124→
   125→    # Resolved issue objects (for REFLECT stage)
   126→    resolved_issue_objs = {
   127→        fid: issues[fid] for fid in resolved_since if fid in issues
   128→    }
   129→
   130→    # Completed clusters since last triage completion
   131→    last_completed = meta.get("last_completed_at", "")
   132→    all_completed: list[dict] = plan.get("completed_clusters", [])
   133→    if last_completed:
   134→        recent_completed = [
   135→            c for c in all_completed
   136→            if c.get("completed_at", "") > last_completed
   137→        ]
   138→    else:
   139→        recent_completed = list(all_completed)
   140→
   141→    return TriageInput(
   142→        open_issues=open_review,
   143→        mechanical_issues=open_mechanical,
   144→        existing_epics=dict(epics),
   145→        dimension_scores=state.get("dimension_scores", {}),
   146→        new_since_last=new_since,
   147→        resolved_since_last=resolved_since,
   148→        previously_dismissed=previously_dismissed,
   149→        triage_version=version,
   150→        resolved_issues=resolved_issue_objs,
   151→        completed_clusters=recent_completed,
   152→    )
   153→
   154→_TRIAGE_SYSTEM_PROMPT = """\
   155→You are maintaining the meta-plan for this codebase. This is the legacy
   156→whole-plan triage contract used by compatibility callers; the primary runtime
   157→uses staged triage commands. Produce a coherent prioritized strategy for all
   158→open review issues.
   159→
   160→Your plan should:
   161→- Cluster issues by ROOT CAUSE, not by dimension or detector
   162→- Give each cluster (``epics`` field in this legacy schema) a clear thesis: one imperative sentence
   163→- Order clusters by dependency: what must be done first for later work to make sense
   164→- Dismiss issues that don't make sense, are contradictory, or are false positives
   165→- Mark which clusters are agent-safe (can be executed mechanically) vs need human judgment
   166→- Avoid creating work that contradicts other work in the plan
   167→- Be ambitious but realistic — aim to resolve all issues coherently
   168→
   169→Available directions for clusters: delete, merge, flatten, enforce, simplify, decompose, extract, inline.
   170→
   171→Available plan tools (the agent executing your plan has access to these):
   172→- `desloppify plan queue` — view all items in priority order
   173→- `desloppify plan focus epic/<name>` — focus the queue on one epic
   174→- `desloppify plan skip <id> --permanent --note "why" --attest "..."` — permanently dismiss
   175→- `desloppify plan skip <id> --note "revisit later"` — temporarily defer
   176→- `desloppify plan resolve <id> --note "what I did" --attest "..."` — mark resolved
   177→- `desloppify plan reorder <id> top|bottom|before|after <target>` — reorder
   178→- `desloppify plan cluster show <name>` — inspect a cluster
   179→- `desloppify scan` — re-scan after making changes to verify progress
   180→- `desloppify show review --status open` — see all open review issues
   181→
   182→Your output defines the ENTIRE work plan. Issues not assigned to any cluster
   183→will remain in the queue as individual items. Dismissed issues will be
   184→removed from the queue with your stated reason.
   185→
   186→Respond with a single JSON object matching this schema:
   187→{
   188→  "strategy_summary": "2-4 sentence narrative: what the meta-plan says, top priorities, current state",
   189→  "epics": [
   190→    {
   191→      "name": "slug-name",
   192→      "thesis": "imperative one-liner",
   193→      "direction": "delete|merge|flatten|enforce|simplify|decompose|extract|inline",
   194→      "root_cause": "why this cluster exists",
   195→      "issue_ids": ["id1", "id2"],
   196→      "dismissed": ["id3"],
   197→      "agent_safe": true,
   198→      "dependency_order": 1,
   199→      "action_steps": [
   200→        {
   201→          "title": "Short imperative step title",
   202→          "detail": "Concrete implementation detail with file paths/locations",
   203→          "issue_refs": ["id1"]
   204→        }
   205→      ],
   206→      "status": "pending"
   207→    }
   208→  ],
   209→  "dismissed_issues": [
   210→    {"issue_id": "id", "reason": "why this issue doesn't make sense"}
   211→  ],
   212→  "contradiction_notes": [
   213→    {"kept": "issue_id", "dismissed": "issue_id", "reason": "why"}
   214→  ],
   215→  "priority_rationale": "why the dependency_order is what it is"
   216→}
   217→"""
   218→
   219→def build_triage_prompt(si: TriageInput) -> str:
   220→    """Build the user-facing prompt content with all issue data."""
   221→    parts: list[str] = []
   222→
   223→    # Section: existing clusters (legacy key: existing_epics)
   224→    if si.existing_epics:
   225→        parts.append("## Existing clusters (legacy field: existing_epics)")
   226→        for name, epic in sorted(si.existing_epics.items()):
   227→            status = epic.get("status", "pending")
   228→            thesis = epic.get("thesis", "")
   229→            direction = epic.get("direction", "")
   230→            fids = epic.get("issue_ids", [])
   231→            parts.append(
   232→                f"- {name} [{status}] ({direction}): {thesis}"
   233→                f"\n  Issues: {', '.join(fids[:10])}"
   234→                f"{'...' if len(fids) > 10 else ''}"
   235→            )
   236→        parts.append("")
   237→
   238→    # Section: what changed
   239→    if si.new_since_last:
   240→        parts.append(f"## New issues since last triage ({len(si.new_since_last)})")
   241→        for fid in sorted(si.new_since_last):
   242→            f = si.open_issues.get(fid, {})
   243→            parts.append(f"- {fid}: {f.get('summary', '(no summary)')}")
   244→        parts.append("")
   245→
   246→    if si.resolved_since_last:
   247→        parts.append(f"## Resolved since last triage ({len(si.resolved_since_last)})")
   248→        for fid in sorted(si.resolved_since_last):
   249→            parts.append(f"- {fid}")
   250→        parts.append("")
   251→
   252→    if si.resolved_issues:
   253→        parts.append(
   254→            "## Resolved review issues available for recurrence context "
   255→            f"({len(si.resolved_issues)})"
   256→        )
   257→        resolved_ids = sorted(si.resolved_issues)
   258→        for fid in resolved_ids[:30]:
   259→            issue = si.resolved_issues.get(fid, {})
   260→            summary = str(issue.get("summary", "(no summary)"))
   261→            dimension = _issue_dimension(issue)
   262→            dim_suffix = f" [{dimension}]" if dimension else ""
   263→            parts.append(f"- {fid}{dim_suffix}: {summary}")
   264→        if len(resolved_ids) > 30:
   265→            parts.append(f"- ... and {len(resolved_ids) - 30} more resolved issues")
   266→        parts.append("")
   267→
   268→    if si.completed_clusters:
   269→        parts.append(
   270→            "## Completed clusters since last triage "
   271→            f"({len(si.completed_clusters)})"
   272→        )
   273→        completed = sorted(
   274→            si.completed_clusters,
   275→            key=lambda cluster: str(cluster.get("completed_at", "")),
   276→            reverse=True,
   277→        )
   278→        for cluster in completed[:10]:
   279→            name = str(cluster.get("name", "(unnamed cluster)"))
   280→            thesis = str(cluster.get("thesis") or cluster.get("description") or "")
   281→            completed_at = str(cluster.get("completed_at", ""))
   282→            issue_ids = cluster.get("issue_ids", [])
   283→            issue_count = len(issue_ids) if isinstance(issue_ids, list) else 0
   284→            parts.append(
   285→                f"- {name}: {thesis} (issues: {issue_count}, completed_at: {completed_at})"
   286→            )
   287→        if len(completed) > 10:
   288→            parts.append(f"- ... and {len(completed) - 10} more completed clusters")
   289→        parts.append("")
   290→
   291→    recurring = _recurring_dimensions(si.open_issues, si.resolved_issues)
   292→    if recurring:
   293→        parts.append(
   294→            "## Potential recurring dimensions (resolved issues still have open peers)"
   295→        )
   296→        for dimension, bucket in recurring.items():
   297→            open_count = len(bucket["open"])
   298→            resolved_count = len(bucket["resolved"])
   299→            parts.append(
   300→                f"- {dimension}: {open_count} open / {resolved_count} recently resolved"
   301→            )
   302→        parts.append("")
   303→
   304→    # Section: all open review issues
   305→    parts.append(f"## All open review issues ({len(si.open_issues)})")
   306→    for fid, f in sorted(si.open_issues.items()):
   307→        detail = f.get("detail", {}) if isinstance(f.get("detail"), dict) else {}
   308→        suggestion = detail.get("suggestion", "")
   309→        dimension = detail.get("dimension", "")
   310→        confidence = f.get("confidence", "medium")
   311→        file_path = f.get("file", "")
   312→        summary = f.get("summary", "")
   313→        parts.append(f"- [{confidence}] {fid}")
   314→        parts.append(f"  File: {file_path}")
   315→        if dimension:
   316→            parts.append(f"  Dimension: {dimension}")
   317→        parts.append(f"  Summary: {summary}")
   318→        if suggestion:
   319→            parts.append(f"  Suggestion: {suggestion}")
   320→    parts.append("")
   321→
   322→    # Section: dimension scores for context
   323→    if si.dimension_scores:
   324→        parts.append("## Dimension scores (context)")
   325→        for name, data in sorted(si.dimension_scores.items()):
   326→            if isinstance(data, dict):
   327→                score = data.get("score", "?")
   328→                strict = data.get("strict", score)
   329→                issues = data.get("failing", 0)
   330→                parts.append(f"- {name}: {score}% (strict: {strict}%, {issues} issues)")
   331→        parts.append("")
   332→
   333→    # Section: previously dismissed
   334→    if si.previously_dismissed:
   335→        parts.append(f"## Previously dismissed ({len(si.previously_dismissed)})")
   336→        parts.append("Maintain unless contradicted by new evidence.")
   337→        for fid in si.previously_dismissed:
   338→            parts.append(f"- {fid}")
   339→        parts.append("")
   340→
   341→    return "\n".join(parts)
   342→
   343→__all__ = [
   344→    "_TRIAGE_SYSTEM_PROMPT",
   345→    "ContradictionNote",
   346→    "DismissedIssue",
   347→    "TriageInput",
   348→    "TriageResult",
   349→    "build_triage_prompt",
   350→    "collect_triage_input",
   351→]
   352→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py"
}
```

> TOOL

tool_result Read
```
1→"""Implementation for legacy whole-plan triage compatibility API.
     2→
     3→Primary runtime triage orchestration is staged and lives in
     4→``app.commands.plan.triage``. The legacy single-shot ``triage_epics`` runtime
     5→lives under ``engine._plan.compat.triage``; callers may still use bridged
     6→imports from ``engine._plan.triage`` and ``engine._plan.epic_triage_*``.
     7→"""
     8→
     9→from __future__ import annotations
    10→
    11→import json
    12→import logging
    13→from dataclasses import dataclass
    14→from typing import Any
    15→
    16→from desloppify.engine._plan.schema import PlanModel, ensure_plan_defaults
    17→from desloppify.engine._state.schema import StateModel
    18→
    19→from desloppify.engine._plan.compat.triage.apply import (
    20→    TriageMutationResult,
    21→    apply_triage_to_plan,
    22→)
    23→from desloppify.engine._plan.compat.triage.parsing import (
    24→    ISSUE_ID_RE,
    25→    extract_issue_citations,
    26→    parse_triage_result,
    27→)
    28→from desloppify.engine._plan.compat.triage.prompt import (
    29→    _TRIAGE_SYSTEM_PROMPT,
    30→    ContradictionNote,
    31→    DismissedIssue,
    32→    TriageInput,
    33→    TriageResult,
    34→    build_triage_prompt,
    35→    collect_triage_input,
    36→)
    37→
    38→logger = logging.getLogger(__name__)
    39→
    40→
    41→def last_real_review_timestamp(state: dict) -> str | None:
    42→    """ISO timestamp of most recent genuine review import (not manual override/scan reset)."""
    43→    real_modes = {"holistic", "per_file", "trusted_internal", "attested_external"}
    44→    audit = state.get("assessment_import_audit", [])
    45→    if isinstance(audit, list):
    46→        for entry in reversed(audit):
    47→            if isinstance(entry, dict) and entry.get("mode") in real_modes:
    48→                ts = entry.get("timestamp")
    49→                if ts:
    50→                    return str(ts)
    51→    holistic = (state.get("review_cache") or {}).get("holistic")
    52→    if isinstance(holistic, dict):
    53→        return holistic.get("reviewed_at")
    54→    return None
    55→
    56→
    57→def detect_recurring_patterns(
    58→    open_issues: dict[str, dict],
    59→    resolved_issues: dict[str, dict],
    60→) -> dict[str, dict]:
    61→    """Detect dimensions with both resolved AND current open issues.
    62→
    63→    Returns ``{dimension: {"open": [ids], "resolved": [ids]}}``.
    64→    A dimension with both resolved and open issues signals a potential
    65→    loop — similar issues recur after previous fixes.
    66→    """
    67→
    68→    def _dimension(finding: dict) -> str:
    69→        detail = finding.get("detail", {})
    70→        if isinstance(detail, dict):
    71→            return detail.get("dimension", "")
    72→        return ""
    73→
    74→    open_by_dim: dict[str, list[str]] = {}
    75→    for fid, finding in open_issues.items():
    76→        dim = _dimension(finding)
    77→        if dim:
    78→            open_by_dim.setdefault(dim, []).append(fid)
    79→
    80→    resolved_by_dim: dict[str, list[str]] = {}
    81→    for fid, finding in resolved_issues.items():
    82→        dim = _dimension(finding)
    83→        if dim:
    84→            resolved_by_dim.setdefault(dim, []).append(fid)
    85→
    86→    recurring: dict[str, dict] = {}
    87→    for dim in set(open_by_dim) & set(resolved_by_dim):
    88→        recurring[dim] = {
    89→            "open": open_by_dim[dim],
    90→            "resolved": resolved_by_dim[dim],
    91→        }
    92→    return recurring
    93→
    94→
    95→@dataclass
    96→class TriageDeps:
    97→    """Injectable dependencies for the triage engine."""
    98→
    99→    llm_call: Any = None  # Callable[[str, str], str] — (system, user) -> response
   100→
   101→
   102→def triage_epics(
   103→    plan: PlanModel,
   104→    state: StateModel,
   105→    *,
   106→    deps: TriageDeps | None = None,
   107→    dry_run: bool = False,
   108→    trigger: str = "manual",
   109→) -> TriageMutationResult:
   110→    """Run legacy whole-plan triage: collect input, call LLM, apply results.
   111→
   112→    If ``dry_run`` is True, collects input and builds prompt but does not
   113→    call the LLM or mutate the plan.
   114→
   115→    If ``deps.llm_call`` is None, returns a dry-run result with the prompt.
   116→    """
   117→    ensure_plan_defaults(plan)
   118→    si = collect_triage_input(plan, state)
   119→
   120→    prompt = build_triage_prompt(si)
   121→    valid_ids = set(si.open_issues.keys())
   122→
   123→    if dry_run or deps is None or deps.llm_call is None:
   124→        result = TriageMutationResult(dry_run=True)
   125→        result.strategy_summary = f"[dry-run] Prompt built with {len(si.open_issues)} issues"
   126→        return result
   127→
   128→    try:
   129→        raw_response = deps.llm_call(_TRIAGE_SYSTEM_PROMPT, prompt)
   130→        raw_json = json.loads(raw_response)
   131→    except (json.JSONDecodeError, TypeError, ValueError) as exc:
   132→        logger.error("Epic triage LLM response parse error: %s", exc)
   133→        result = TriageMutationResult()
   134→        result.strategy_summary = f"Triage failed: {exc}"
   135→        return result
   136→
   137→    triage = parse_triage_result(raw_json, valid_ids)
   138→    return apply_triage_to_plan(plan, state, triage, trigger=trigger)
   139→
   140→
   141→__all__ = [
   142→    "ContradictionNote",
   143→    "DismissedIssue",
   144→    "ISSUE_ID_RE",
   145→    "TriageDeps",
   146→    "TriageInput",
   147→    "TriageMutationResult",
   148→    "TriageResult",
   149→    "apply_triage_to_plan",
   150→    "build_triage_prompt",
   151→    "collect_triage_input",
   152→    "detect_recurring_patterns",
   153→    "extract_issue_citations",
   154→    "last_real_review_timestamp",
   155→    "parse_triage_result",
   156→    "triage_epics",
   157→]
   158→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/__init__.py"
}
```

> TOOL

tool_result Read
```
1→"""Primary triage namespace for staged triage surfaces and compat bridges.
     2→
     3→Staged triage contracts live here (for example ``playbook``). Legacy
     4→whole-plan triage runtime lives in ``engine._plan.compat.triage``; modules in
     5→this package (``core/apply/dismiss/parsing/prompt``) are compatibility bridges
     6→that preserve legacy imports while keeping ownership explicit. They are not
     7→part of the canonical public ``__all__`` surface.
     8→"""
     9→
    10→from __future__ import annotations
    11→
    12→__all__ = ["playbook"]
    13→
```

> TOOL

tool_use Bash
```json
{
  "command": "rm /Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/plan_public_exports.py",
  "description": "Delete plan_public_exports.py"
}
```

> TOOL

tool_result Bash
```
null
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py"
}
```

> TOOL

tool_result Read
```
1→"""Compat bridge for legacy whole-plan triage apply imports.
     2→
     3→Canonical implementation lives in ``engine._plan.compat.triage.apply``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.apply")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> DEVELOPER

Read these files and report their full contents. I need exact content for making edits.

Step 3 files:
1. `desloppify/languages/typescript/detectors/analysis.py`
2. `desloppify/languages/typescript/detectors/cli.py`
3. `desloppify/languages/typescript/tests/test_ts_deprecated.py` (if it has ts_detector_analysis references)

Step 4 files:
4. `desloppify/languages/typescript/analysis.py`
5. `desloppify/languages/typescript/__init__.py`

Step 5 files:
6. `desloppify/languages/__init__.py`
7. `desloppify/languages/framework.py`

Also search for:
- All imports of `detectors.analysis` in typescript directory
- All imports of `typescript.analysis` or `ts_analysis_mod`
- All references to `_COMPAT_EXPORTS` in languages/ directory
- The test file `test_typescript_detectors_fixers_and_wrappers_split_direct.py` - find and read it

Report full file contents for all files found.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py"
}
```

> TOOL

tool_result Read
```
1→"""Compat bridge for legacy whole-plan triage dismissal imports.
     2→
     3→Canonical implementation lives in ``engine._plan.compat.triage.dismiss``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.dismiss")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py"
}
```

> TOOL

tool_result Read
```
1→"""Compat bridge for legacy whole-plan triage parsing imports.
     2→
     3→Canonical implementation lives in ``engine._plan.compat.triage.parsing``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.parsing")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> AGENT

Now let me read the remaining triage files:

> AGENT

I'll search for and read all the requested files. Let me start by finding them and reading their contents.

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/languages/typescript/detectors/analysis.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/analysis.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/languages/typescript/detectors/cli.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/cli.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py"
}
```

> TOOL

tool_result Read
```
1→"""Compat bridge for legacy whole-plan triage prompt imports.
     2→
     3→Canonical implementation lives in ``engine._plan.compat.triage.prompt``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.prompt")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/languages/typescript/tests/test_ts_deprecated.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/tests/test_ts_deprecated.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py"
}
```

> TOOL

tool_result Read
```
1→"""Compat bridge for legacy whole-plan triage core imports.
     2→
     3→Canonical implementation lives in ``engine._plan.compat.triage.core``.
     4→"""
     5→
     6→from __future__ import annotations
     7→
     8→from importlib import import_module
     9→
    10→_IMPL = import_module("desloppify.engine._plan.compat.triage.core")
    11→__all__ = list(getattr(_IMPL, "__all__", ()))
    12→globals().update({name: getattr(_IMPL, name) for name in __all__})
    13→
```

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/languages/typescript/analysis.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/analysis.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/languages/typescript/__init__.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/__init__.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/languages/__init__.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/languages/__init__.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/languages/framework.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/languages/framework.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/playbook.py"
}
```

> TOOL

tool_result Read
```
1→"""Canonical shared triage workflow labels and command snippets."""
     2→
     3→from __future__ import annotations
     4→
     5→TRIAGE_STAGE_LABELS: tuple[tuple[str, str], ...] = (
     6→    ("observe", "Analyse issues & spot contradictions"),
     7→    ("reflect", "Form strategy & present to user"),
     8→    ("organize", "Defer contradictions, cluster, & prioritize"),
     9→    ("enrich", "Make steps executor-ready (detail, refs)"),
    10→    ("sense-check", "Verify accuracy & cross-cluster deps"),
    11→    ("commit", "Write strategy & confirm"),
    12→)
    13→
    14→_TRIAGE_STAGE_DEPENDENCY_ITEMS: tuple[tuple[str, set[str]], ...] = (
    15→    ("observe", set()),
    16→    ("reflect", {"observe"}),
    17→    ("organize", {"reflect"}),
    18→    ("enrich", {"organize"}),
    19→    ("sense-check", {"enrich"}),
    20→    ("commit", {"sense-check"}),
    21→)
    22→
    23→TRIAGE_STAGE_DEPENDENCIES: dict[str, set[str]] = dict(_TRIAGE_STAGE_DEPENDENCY_ITEMS)
    24→TRIAGE_RUNNERS: tuple[str, str] = ("codex", "claude")
    25→
    26→TRIAGE_CMD_OBSERVE = (
    27→    'desloppify plan triage --stage observe --report '
    28→    '"analysis of themes and root causes..."'
    29→)
    30→TRIAGE_CMD_REFLECT = (
    31→    'desloppify plan triage --stage reflect --report '
    32→    '"comparison against completed work..."'
    33→)
    34→TRIAGE_CMD_ORGANIZE = (
    35→    'desloppify plan triage --stage organize --report '
    36→    '"summary of organization and priorities..."'
    37→)
    38→TRIAGE_CMD_ENRICH = (
    39→    'desloppify plan triage --stage enrich --report '
    40→    '"summary of enrichment work done..."'
    41→)
    42→TRIAGE_CMD_SENSE_CHECK = (
    43→    'desloppify plan triage --stage sense-check --report '
    44→    '"summary of sense-check findings..."'
    45→)
    46→TRIAGE_CMD_COMPLETE = 'desloppify plan triage --complete --strategy "execution plan..."'
    47→TRIAGE_CMD_COMPLETE_VERBOSE = (
    48→    "desloppify plan triage --complete --strategy "
    49→    '"execution plan with priorities and verification..."'
    50→)
    51→TRIAGE_CMD_CONFIRM_EXISTING = (
    52→    'desloppify plan triage --confirm-existing --note "..." --strategy "..."'
    53→)
    54→TRIAGE_CMD_CLUSTER_CREATE = 'desloppify plan cluster create <name> --description "..."'
    55→TRIAGE_CMD_CLUSTER_ADD = "desloppify plan cluster add <name> <issue-patterns>"
    56→TRIAGE_CMD_CLUSTER_ENRICH = (
    57→    'desloppify plan cluster update <name> --description "..." --steps '
    58→    '"step 1" "step 2"'
    59→)
    60→TRIAGE_CMD_CLUSTER_ENRICH_COMPACT = (
    61→    'desloppify plan cluster update <name> --description "..." --steps '
    62→    '"step1" "step2"'
    63→)
    64→TRIAGE_CMD_CLUSTER_STEPS = (
    65→    'desloppify plan cluster update <name> --steps "step 1" "step 2"'
    66→)
    67→TRIAGE_CMD_RUN_STAGES_CODEX = "desloppify plan triage --run-stages --runner codex"
    68→TRIAGE_CMD_RUN_STAGES_CLAUDE = "desloppify plan triage --run-stages --runner claude"
    69→
    70→_RUNNER_STAGE_NAMES = frozenset(
    71→    stage_name for stage_name, _label in TRIAGE_STAGE_LABELS if stage_name != "commit"
    72→)
    73→_MANUAL_STAGE_COMMANDS: dict[str, str] = {
    74→    "observe": TRIAGE_CMD_OBSERVE,
    75→    "reflect": TRIAGE_CMD_REFLECT,
    76→    "organize": TRIAGE_CMD_ORGANIZE,
    77→    "enrich": TRIAGE_CMD_ENRICH,
    78→    "sense-check": TRIAGE_CMD_SENSE_CHECK,
    79→    "commit": TRIAGE_CMD_COMPLETE,
    80→}
    81→
    82→
    83→def triage_run_stages_command(
    84→    *,
    85→    runner: str = "codex",
    86→    only_stages: str | tuple[str, ...] | list[str] | None = None,
    87→) -> str:
    88→    """Return the canonical staged triage runner command."""
    89→    resolved_runner = str(runner).strip().lower()
    90→    if resolved_runner not in TRIAGE_RUNNERS:
    91→        supported = ", ".join(TRIAGE_RUNNERS)
    92→        raise ValueError(f"Unsupported triage runner: {runner!r}. Valid: {supported}")
    93→
    94→    command = f"desloppify plan triage --run-stages --runner {resolved_runner}"
    95→    if only_stages is None:
    96→        return command
    97→
    98→    if isinstance(only_stages, str):
    99→        stages = [only_stages]
   100→    else:
   101→        stages = [str(stage).strip().lower() for stage in only_stages if str(stage).strip()]
   102→
   103→    invalid = [stage for stage in stages if stage not in _RUNNER_STAGE_NAMES]
   104→    if invalid:
   105→        supported = ", ".join(sorted(_RUNNER_STAGE_NAMES))
   106→        bad = ", ".join(sorted(set(invalid)))
   107→        raise ValueError(f"Unsupported triage stage(s): {bad}. Valid: {supported}")
   108→
   109→    return f"{command} --only-stages {','.join(stages)}"
   110→
   111→
   112→def triage_runner_commands(
   113→    *,
   114→    only_stages: str | tuple[str, ...] | list[str] | None = None,
   115→) -> tuple[tuple[str, str], tuple[str, str]]:
   116→    """Return the preferred staged-runner commands for Codex and Claude."""
   117→    return (
   118→        ("Codex", triage_run_stages_command(runner="codex", only_stages=only_stages)),
   119→        ("Claude", triage_run_stages_command(runner="claude", only_stages=only_stages)),
   120→    )
   121→
   122→
   123→def triage_manual_stage_command(stage: str) -> str:
   124→    """Return the manual fallback command for a triage stage."""
   125→    resolved_stage = str(stage).strip().lower()
   126→    if resolved_stage not in _MANUAL_STAGE_COMMANDS:
   127→        supported = ", ".join(sorted(_MANUAL_STAGE_COMMANDS))
   128→        raise ValueError(f"Unsupported triage stage: {stage!r}. Valid: {supported}")
   129→    return _MANUAL_STAGE_COMMANDS[resolved_stage]
   130→
   131→
   132→__all__ = [
   133→    "TRIAGE_STAGE_DEPENDENCIES",
   134→    "TRIAGE_STAGE_LABELS",
   135→    "TRIAGE_CMD_CLUSTER_ADD",
   136→    "TRIAGE_CMD_CLUSTER_CREATE",
   137→    "TRIAGE_CMD_CLUSTER_ENRICH",
   138→    "TRIAGE_CMD_CLUSTER_ENRICH_COMPACT",
   139→    "TRIAGE_CMD_CLUSTER_STEPS",
   140→    "TRIAGE_CMD_COMPLETE",
   141→    "TRIAGE_CMD_SENSE_CHECK",
   142→    "TRIAGE_CMD_COMPLETE_VERBOSE",
   143→    "TRIAGE_CMD_CONFIRM_EXISTING",
   144→    "TRIAGE_CMD_ENRICH",
   145→    "TRIAGE_CMD_OBSERVE",
   146→    "TRIAGE_CMD_ORGANIZE",
   147→    "TRIAGE_CMD_REFLECT",
   148→    "TRIAGE_CMD_RUN_STAGES_CLAUDE",
   149→    "TRIAGE_CMD_RUN_STAGES_CODEX",
   150→    "TRIAGE_RUNNERS",
   151→    "triage_manual_stage_command",
   152→    "triage_run_stages_command",
   153→    "triage_runner_commands",
   154→]
   155→
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/test_typescript_detectors_fixers_and_wrappers_split_direct.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/tests/lang/typescript/test_typescript_detectors_fixers_and_wrappers_split_direct.py
```

> TOOL

tool_use Bash
```json
{
  "command": "python -m pytest desloppify/tests/engine/ -q 2>&1",
  "description": "Run engine tests",
  "timeout": 120000
}
```

> TOOL

tool_result Bash
```
......................................                                   [100%]
38 passed in 1.14s
```

> AGENT

Now let me get more detailed import information to fully trace the imports:

> AGENT

Now let me read all these files:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/analysis.py"
}
```

> TOOL

tool_result Read
```
1→"""Canonical TypeScript detector analysis-helper surface (non-CLI)."""
     2→
     3→from __future__ import annotations
     4→
     5→from desloppify.languages.typescript.detectors.deps import (
     6→    build_dep_graph,
     7→    build_dynamic_import_targets,
     8→    ts_alias_resolver,
     9→)
    10→from desloppify.languages.typescript.detectors.facade import detect_reexport_facades
    11→from desloppify.languages.typescript.detectors.smells import detect_smells
    12→
    13→__all__ = [
    14→    "build_dep_graph",
    15→    "build_dynamic_import_targets",
    16→    "detect_reexport_facades",
    17→    "detect_smells",
    18→    "ts_alias_resolver",
    19→]
    20→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "epic_triage_apply|epic_triage_dismiss|epic_triage_parsing|epic_triage_prompt",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "context": 2
}
```

> TOOL

tool_result Grep
```
docs/work-batches-since-0.7.0-ticket-digest.md-484-- Binary files changed: `0`
docs/work-batches-since-0.7.0-ticket-digest.md-485-- Most active source directories: `desloppify/intelligence/review` (4635), `desloppify/intelligence/narrative` (2011), `desloppify/app/commands` (1653), `desloppify/tests/plan` (1475), `desloppify/engine/detectors` (1391), `desloppify/tests/review` (1315)
docs/work-batches-since-0.7.0-ticket-digest.md:486:- Most active source files: `desloppify/tests/review/test_runner_internals.py` (1026), `desloppify/tests/plan/test_epic_triage_apply.py` (767), `desloppify/tests/plan/test_stale_policy.py` (646), `desloppify/intelligence/review/context_holistic/budget_patterns.py` (551), `desloppify/intelligence/narrative/reminders.py` (492), `desloppify/intelligence/review/context_holistic/budget_abstractions.py` (456)
docs/work-batches-since-0.7.0-ticket-digest.md-487-- Most frequently touched subsystems (source only): Tests (59), Engine/scoring core (51), Intelligence/review context (35), Language frameworks/plugins (32), Plan/resolve workflow (25), Review command workflow (16)
/Users/user_c042661f/Documents/desloppify/docs/work-batches-since-0.7.0-ticket-digest.md-488-
--
docs/work-batches-since-0.7.0-ticket-digest.md-554-- `9e93cfe`: refactor: remove unused imports/re-exports, add logging to silent excepts — updated 18 files (+54 / -80), focused on review intelligence, language plugins. Key files: `desloppify/tests/plan/test_auto_cluster.py`, `desloppify/app/commands/review/runner_parallel.py`.
docs/work-batches-since-0.7.0-ticket-digest.md-555-- `f333c1d`: refactor: extract testable score_recipe_lines, expand smoke test coverage — updated 3 files (+32 / -19), focused on review workflow, scan workflow. Key files: `desloppify/app/commands/scan/reporting/presentation.py`, `desloppify/tests/commands/test_direct_coverage_modules.py`.
docs/work-batches-since-0.7.0-ticket-digest.md:556:- `26593af`: feat: monster-function decomposition, noop filter, review prompt improvements — updated 18 files (+777 / -379), focused on tests, language plugins. Key files: `desloppify/engine/_plan/epic_triage_apply.py`, `desloppify/engine/_plan/schema_migrations.py`.
docs/work-batches-since-0.7.0-ticket-digest.md-557-- `b4161bf`: fix: use defusedxml for C# .csproj parsing to prevent XML attacks — updated 1 files (+1 / -1), focused on language plugins. Key file: `desloppify/languages/csharp/detectors/deps_support.py`.
docs/work-batches-since-0.7.0-ticket-digest.md-558-- `de5c9f9`: refactor: decompose cmd_triage_dashboard and stale_dimensions monster functions — updated 2 files (+156 / -97), focused on planning workflow, engine/scoring core. Key files: `desloppify/engine/_plan/stale_dimensions.py`, `desloppify/app/commands/plan/triage/display.py`.
--
docs/commit-summary-since-0.7.0.md-680-- Scope snapshot: 18 files, +777 / -379 lines.
docs/commit-summary-since-0.7.0.md-681-- Primary areas: Tests and fixtures, Language adapters/framework, Other CLI commands.
docs/commit-summary-since-0.7.0.md:682:- High-churn files: `desloppify/engine/_plan/epic_triage_apply.py`, `desloppify/engine/_plan/schema_migrations.py`, `desloppify/languages/_framework/generic.py`.
docs/commit-summary-since-0.7.0.md-683-- Summary: Monster-function decomposition, noop filter, review prompt improvements. Focused on tests and fixtures, language adapters/framework, and other cli commands. Net effect: expands product capability.
/Users/user_c042661f/Documents/desloppify/docs/commit-summary-since-0.7.0.md-684-
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-15-import desloppify.engine._plan.compat.triage.prompt as triage_prompt_compat_mod
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-16-import desloppify.engine._plan.constants as plan_constants_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:17:import desloppify.engine._plan.epic_triage_apply as triage_apply_legacy_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:18:import desloppify.engine._plan.epic_triage_parsing as triage_parsing_legacy_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:19:import desloppify.engine._plan.epic_triage_prompt as triage_prompt_legacy_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:20:import desloppify.engine._plan.epic_triage_dismiss as triage_dismiss_mod
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-21-import desloppify.engine._plan.reconcile_review_import as reconcile_import_mod
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-22-import desloppify.engine._plan.schema.helpers as schema_helpers_mod
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-39-    package_root = Path(__file__).resolve().parents[2]
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-40-    flat_modules = {
desloppify/tests/engine/test_sync_split_modules_direct.py:41:        "desloppify.engine._plan.epic_triage_prompt",
desloppify/tests/engine/test_sync_split_modules_direct.py:42:        "desloppify.engine._plan.epic_triage_parsing",
desloppify/tests/engine/test_sync_split_modules_direct.py:43:        "desloppify.engine._plan.epic_triage_apply",
desloppify/tests/engine/test_sync_split_modules_direct.py:44:        "desloppify.engine._plan.epic_triage_dismiss",
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-45-    }
desloppify/tests/engine/test_sync_split_modules_direct.py-46-    offenders: list[str] = []
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-172-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-173-
desloppify/tests/engine/test_sync_split_modules_direct.py:174:def test_epic_triage_dismiss_moves_issues_to_skipped() -> None:
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-175-    triage = SimpleNamespace(
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-176-        dismissed_issues=[SimpleNamespace(issue_id="id1", reason="false_positive")],
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-18-``compat.triage``) and delegate to grouped canonical implementations.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-19-
desloppify/engine/_plan/__init__.py:20:Legacy whole-plan triage module names (``epic_triage_prompt``,
desloppify/engine/_plan/__init__.py:21:``epic_triage_parsing``, ``epic_triage_apply``, ``epic_triage_dismiss``)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-22-also remain as compatibility bridges and delegate to
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-23-``engine._plan.compat.triage.*``.
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_parsing_direct.py-3-from __future__ import annotations
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_parsing_direct.py-4-
desloppify/tests/plan/test_epic_triage_parsing_direct.py:5:import desloppify.engine._plan.epic_triage_parsing as parsing_mod
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_parsing_direct.py-6-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_parsing_direct.py-7-
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/plan/test_triage_runner.py-17-    validate_stage,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/plan/test_triage_runner.py-18-)
desloppify/tests/commands/plan/test_triage_runner.py:19:from desloppify.engine._plan.epic_triage_prompt import TriageInput
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/plan/test_triage_runner.py-20-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/plan/test_triage_runner.py-21-
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply_edge_cases.py-3-from __future__ import annotations
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply_edge_cases.py-4-
desloppify/tests/plan/test_epic_triage_apply_edge_cases.py:5:from desloppify.engine._plan.epic_triage_apply import apply_triage_to_plan
desloppify/tests/plan/test_epic_triage_apply_edge_cases.py:6:from desloppify.engine._plan.epic_triage_prompt import DismissedIssue, TriageResult
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply_edge_cases.py-7-from desloppify.engine._plan.schema import empty_plan
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply_edge_cases.py-8-from desloppify.engine._plan.policy.stale import review_issue_snapshot_hash
--
desloppify/tests/plan/test_epic_triage_apply.py:1:"""Tests for epic_triage_apply: plan mutation during triage."""
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py-2-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py-3-from __future__ import annotations
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py-4-
desloppify/tests/plan/test_epic_triage_apply.py:5:from desloppify.engine._plan.epic_triage_apply import (
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py-6-    TriageMutationResult,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py-7-    apply_triage_to_plan,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py-8-)
desloppify/tests/plan/test_epic_triage_apply.py:9:from desloppify.engine._plan.epic_triage_prompt import DismissedIssue, TriageResult
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py-10-from desloppify.engine._plan.schema import empty_plan
/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py-11-from desloppify.engine._plan.policy.stale import review_issue_snapshot_hash
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/cli.py"
}
```

> TOOL

tool_result Read
```
1→"""Canonical TypeScript detector CLI and command-registry surface."""
     2→
     3→from __future__ import annotations
     4→
     5→import argparse
     6→import json
     7→from collections.abc import Callable
     8→from pathlib import Path
     9→
    10→from desloppify.base.discovery.file_paths import rel
    11→from desloppify.base.discovery.paths import get_src_path
    12→from desloppify.base.discovery.source import find_ts_and_tsx_files
    13→from desloppify.base.output.terminal import colorize, display_entries, print_table
    14→from desloppify.engine.detectors import coupling as coupling_detector_mod
    15→from desloppify.engine.detectors import dupes as dupes_detector_mod
    16→from desloppify.engine.detectors import gods as gods_detector_mod
    17→from desloppify.engine.detectors import orphaned as orphaned_detector_mod
    18→from desloppify.languages._framework.commands_base import (
    19→    make_cmd_complexity,
    20→    make_cmd_facade,
    21→    make_cmd_large,
    22→    make_cmd_naming,
    23→    make_cmd_passthrough,
    24→    make_cmd_single_use,
    25→    make_cmd_smells,
    26→)
    27→from desloppify.languages._framework.commands_base_registry import (
    28→    build_standard_detect_registry,
    29→    compose_detect_registry,
    30→)
    31→import desloppify.languages.typescript.detectors.analysis as ts_detector_analysis_mod
    32→import desloppify.languages.typescript.detectors.deps as deps_detector_mod
    33→from desloppify.languages.typescript.detectors.concerns import cmd_concerns
    34→from desloppify.languages.typescript.detectors.deprecated import cmd_deprecated
    35→from desloppify.languages.typescript.detectors.deps import cmd_cycles, cmd_deps
    36→from desloppify.languages.typescript.detectors.exports import cmd_exports
    37→from desloppify.languages.typescript.detectors.logs import cmd_logs
    38→from desloppify.languages.typescript.detectors.patterns_cli import cmd_patterns
    39→from desloppify.languages.typescript.detectors.props import cmd_props
    40→from desloppify.languages.typescript.detectors.react_cli import cmd_react
    41→from desloppify.languages.typescript.detectors.unused import cmd_unused
    42→from desloppify.languages.typescript.extractors_components import (
    43→    detect_passthrough_components,
    44→    extract_ts_components,
    45→)
    46→from desloppify.languages.typescript.extractors_functions import extract_ts_functions
    47→from desloppify.languages.typescript.phases_config import (
    48→    TS_COMPLEXITY_SIGNALS,
    49→    TS_GOD_RULES,
    50→    TS_SKIP_DIRS,
    51→    TS_SKIP_NAMES,
    52→)
    53→from desloppify.languages.typescript.plugin_contract import TS_BARREL_NAMES, TS_LARGE_THRESHOLD
    54→
    55→
    56→cmd_large = make_cmd_large(
    57→    find_ts_and_tsx_files,
    58→    default_threshold=TS_LARGE_THRESHOLD,
    59→    module_name=__name__,
    60→)
    61→cmd_complexity = make_cmd_complexity(
    62→    find_ts_and_tsx_files,
    63→    TS_COMPLEXITY_SIGNALS,
    64→    module_name=__name__,
    65→)
    66→cmd_single_use = make_cmd_single_use(
    67→    deps_detector_mod.build_dep_graph,
    68→    barrel_names=TS_BARREL_NAMES,
    69→    module_name=__name__,
    70→)
    71→cmd_passthrough = make_cmd_passthrough(
    72→    detect_passthrough_components,
    73→    noun="component",
    74→    name_key="component",
    75→    total_key="total_props",
    76→    module_name=__name__,
    77→)
    78→cmd_naming = make_cmd_naming(
    79→    find_ts_and_tsx_files,
    80→    skip_names=TS_SKIP_NAMES,
    81→    skip_dirs=TS_SKIP_DIRS,
    82→    module_name=__name__,
    83→)
    84→cmd_smells = make_cmd_smells(
    85→    ts_detector_analysis_mod.detect_smells,
    86→    module_name=__name__,
    87→)
    88→cmd_facade = make_cmd_facade(
    89→    deps_detector_mod.build_dep_graph,
    90→    detect_facades_fn=ts_detector_analysis_mod.detect_reexport_facades,
    91→    module_name=__name__,
    92→)
    93→
    94→
    95→def cmd_gods(args: argparse.Namespace) -> None:
    96→    entries, _ = gods_detector_mod.detect_gods(
    97→        extract_ts_components(Path(args.path)), TS_GOD_RULES
    98→    )
    99→    display_entries(
   100→        args,
   101→        entries,
   102→        label="God components",
   103→        empty_msg="No god components found.",
   104→        columns=["File", "LOC", "Hooks", "Why"],
   105→        widths=[55, 5, 6, 45],
   106→        row_fn=lambda e: [
   107→            rel(e["file"]),
   108→            str(e["loc"]),
   109→            str(e["detail"].get("hook_total", 0)),
   110→            ", ".join(e["reasons"]),
   111→        ],
   112→    )
   113→
   114→
   115→def cmd_orphaned(args: argparse.Namespace) -> None:
   116→    graph = ts_detector_analysis_mod.build_dep_graph(Path(args.path))
   117→    entries, _ = orphaned_detector_mod.detect_orphaned_files(
   118→        Path(args.path),
   119→        graph,
   120→        extensions=[".ts", ".tsx"],
   121→        options=orphaned_detector_mod.OrphanedDetectionOptions(
   122→            dynamic_import_finder=ts_detector_analysis_mod.build_dynamic_import_targets,
   123→            alias_resolver=ts_detector_analysis_mod.ts_alias_resolver,
   124→        ),
   125→    )
   126→    if getattr(args, "json", False):
   127→        print(
   128→            json.dumps(
   129→                {
   130→                    "count": len(entries),
   131→                    "entries": [
   132→                        {"file": rel(e["file"]), "loc": e["loc"]} for e in entries
   133→                    ],
   134→                },
   135→                indent=2,
   136→            )
   137→        )
   138→        return
   139→    if not entries:
   140→        print(colorize("\nNo orphaned files found.", "green"))
   141→        return
   142→    total_loc = sum(e["loc"] for e in entries)
   143→    print(colorize(f"\nOrphaned files: {len(entries)} files, {total_loc} LOC\n", "bold"))
   144→    top = getattr(args, "top", 20)
   145→    rows = [[rel(e["file"]), str(e["loc"])] for e in entries[:top]]
   146→    print_table(["File", "LOC"], rows, [80, 6])
   147→    if len(entries) > top:
   148→        print(f"\n  ... and {len(entries) - top} more")
   149→
   150→
   151→def cmd_dupes(args: argparse.Namespace) -> None:
   152→    functions = []
   153→    for filepath in find_ts_and_tsx_files(Path(args.path)):
   154→        if "node_modules" in filepath or ".d.ts" in filepath:
   155→            continue
   156→        functions.extend(extract_ts_functions(filepath))
   157→    entries, _ = dupes_detector_mod.detect_duplicates(
   158→        functions, threshold=getattr(args, "threshold", None) or 0.8
   159→    )
   160→    if getattr(args, "json", False):
   161→        print(json.dumps({"count": len(entries), "entries": entries}, indent=2))
   162→        return
   163→    if not entries:
   164→        print(colorize("No duplicate functions found.", "green"))
   165→        return
   166→    exact = [e for e in entries if e["kind"] == "exact"]
   167→    near = [e for e in entries if e["kind"] == "near-duplicate"]
   168→    if exact:
   169→        print(colorize(f"\nExact duplicates: {len(exact)} pairs\n", "bold"))
   170→        rows = []
   171→        for entry in exact[: getattr(args, "top", 20)]:
   172→            fn_a, fn_b = entry["fn_a"], entry["fn_b"]
   173→            rows.append(
   174→                [
   175→                    f"{fn_a['name']} ({rel(fn_a['file'])}:{fn_a['line']})",
   176→                    f"{fn_b['name']} ({rel(fn_b['file'])}:{fn_b['line']})",
   177→                    str(fn_a["loc"]),
   178→                ]
   179→            )
   180→        print_table(["Function A", "Function B", "LOC"], rows, [50, 50, 5])
   181→    if near:
   182→        print(
   183→            colorize(
   184→                f"\nNear-duplicates (>={getattr(args, 'threshold', 0.8):.0%} similar): {len(near)} pairs\n",
   185→                "bold",
   186→            )
   187→        )
   188→        rows = []
   189→        for entry in near[: getattr(args, "top", 20)]:
   190→            fn_a, fn_b = entry["fn_a"], entry["fn_b"]
   191→            rows.append(
   192→                [
   193→                    f"{fn_a['name']} ({rel(fn_a['file'])}:{fn_a['line']})",
   194→                    f"{fn_b['name']} ({rel(fn_b['file'])}:{fn_b['line']})",
   195→                    f"{entry['similarity']:.0%}",
   196→                ]
   197→            )
   198→        print_table(["Function A", "Function B", "Sim"], rows, [50, 50, 5])
   199→
   200→
   201→def cmd_coupling(args: argparse.Namespace) -> None:
   202→    graph = ts_detector_analysis_mod.build_dep_graph(Path(args.path))
   203→    src_path = get_src_path()
   204→    shared_prefix = f"{src_path}/shared/"
   205→    tools_prefix = f"{src_path}/tools/"
   206→    violations, _ = coupling_detector_mod.detect_coupling_violations(
   207→        Path(args.path), graph, shared_prefix=shared_prefix, tools_prefix=tools_prefix
   208→    )
   209→    candidates, _ = coupling_detector_mod.detect_boundary_candidates(
   210→        Path(args.path),
   211→        graph,
   212→        shared_prefix=shared_prefix,
   213→        tools_prefix=tools_prefix,
   214→        skip_basenames={"index.ts", "index.tsx"},
   215→    )
   216→    if getattr(args, "json", False):
   217→        print(
   218→            json.dumps(
   219→                {
   220→                    "violations": len(violations),
   221→                    "boundary_candidates": len(candidates),
   222→                    "coupling_violations": violations,
   223→                    "boundary_candidates_detail": [
   224→                        {**entry, "file": rel(entry["file"])} for entry in candidates
   225→                    ],
   226→                },
   227→                indent=2,
   228→            )
   229→        )
   230→        return
   231→    if violations:
   232→        print(colorize(f"\nCoupling violations (shared -> tools): {len(violations)}\n", "bold"))
   233→        rows = []
   234→        for entry in violations[: getattr(args, "top", 20)]:
   235→            rows.append([rel(entry["file"]), entry["target"], entry["tool"]])
   236→        print_table(["Shared File", "Imports From", "Tool"], rows, [50, 50, 20])
   237→    else:
   238→        print(colorize("\nNo coupling violations (shared -> tools).", "green"))
   239→
   240→    cross_tool, _ = coupling_detector_mod.detect_cross_tool_imports(
   241→        Path(args.path), graph, tools_prefix=tools_prefix
   242→    )
   243→    print()
   244→    if cross_tool:
   245→        print(colorize(f"Cross-tool imports (tools -> tools): {len(cross_tool)}\n", "bold"))
   246→        rows = []
   247→        for entry in cross_tool[: getattr(args, "top", 20)]:
   248→            rows.append(
   249→                [
   250→                    rel(entry["file"]),
   251→                    entry["target"],
   252→                    f"{entry['source_tool']}->{entry['target_tool']}",
   253→                ]
   254→            )
   255→        print_table(["Source File", "Imports From", "Direction"], rows, [50, 50, 20])
   256→    else:
   257→        print(colorize("No cross-tool imports.", "green"))
   258→
   259→    print()
   260→    if candidates:
   261→        print(
   262→            colorize(
   263→                f"Boundary candidates (shared files used by 1 tool): {len(candidates)}\n",
   264→                "bold",
   265→            )
   266→        )
   267→        rows = []
   268→        for entry in candidates[: getattr(args, "top", 20)]:
   269→            rows.append(
   270→                [
   271→                    rel(entry["file"]),
   272→                    str(entry["loc"]),
   273→                    entry["sole_tool"],
   274→                    str(entry["importer_count"]),
   275→                ]
   276→            )
   277→        print_table(
   278→            ["Shared File", "LOC", "Only Used By", "Importers"],
   279→            rows,
   280→            [50, 5, 30, 9],
   281→        )
   282→    else:
   283→        print(colorize("No boundary candidates found.", "green"))
   284→    print()
   285→
   286→
   287→def get_detect_commands() -> dict[str, Callable[..., None]]:
   288→    """Build the TypeScript detector command registry."""
   289→    return compose_detect_registry(
   290→        base_registry=build_standard_detect_registry(
   291→            cmd_deps=cmd_deps,
   292→            cmd_cycles=cmd_cycles,
   293→            cmd_orphaned=cmd_orphaned,
   294→            cmd_dupes=cmd_dupes,
   295→            cmd_large=cmd_large,
   296→            cmd_complexity=cmd_complexity,
   297→        ),
   298→        extra_registry={
   299→            "logs": cmd_logs,
   300→            "unused": cmd_unused,
   301→            "exports": cmd_exports,
   302→            "deprecated": cmd_deprecated,
   303→            "gods": cmd_gods,
   304→            "single_use": cmd_single_use,
   305→            "props": cmd_props,
   306→            "passthrough": cmd_passthrough,
   307→            "concerns": cmd_concerns,
   308→            "smells": cmd_smells,
   309→            "coupling": cmd_coupling,
   310→            "patterns": cmd_patterns,
   311→            "naming": cmd_naming,
   312→            "react": cmd_react,
   313→            "facade": cmd_facade,
   314→        },
   315→    )
   316→
   317→
   318→__all__ = [
   319→    "cmd_complexity",
   320→    "cmd_concerns",
   321→    "cmd_coupling",
   322→    "cmd_cycles",
   323→    "cmd_deprecated",
   324→    "cmd_deps",
   325→    "cmd_dupes",
   326→    "cmd_exports",
   327→    "cmd_facade",
   328→    "cmd_gods",
   329→    "cmd_large",
   330→    "cmd_logs",
   331→    "cmd_naming",
   332→    "cmd_orphaned",
   333→    "cmd_passthrough",
   334→    "cmd_patterns",
   335→    "cmd_props",
   336→    "cmd_react",
   337→    "cmd_single_use",
   338→    "cmd_smells",
   339→    "cmd_unused",
   340→    "get_detect_commands",
   341→]
   342→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/tests/test_ts_deprecated.py"
}
```

> TOOL

tool_result Read
```
1→"""Tests for desloppify.languages.typescript.detectors.deprecated — @deprecated symbol detection."""
     2→
     3→from pathlib import Path
     4→
     5→import pytest
     6→
     7→import desloppify.base.discovery.paths as paths_api_mod
     8→import desloppify.languages.typescript.detectors.deprecated as deprecated_detector_mod
     9→
    10→
    11→@pytest.fixture(autouse=True)
    12→def _root(tmp_path, set_project_root, monkeypatch):
    13→    """Point PROJECT_ROOT at the tmp directory via RuntimeContext."""
    14→    monkeypatch.setattr(paths_api_mod, "SRC_PATH", tmp_path)
    15→
    16→
    17→def _write(tmp_path: Path, name: str, content: str) -> Path:
    18→    p = tmp_path / name
    19→    p.parent.mkdir(parents=True, exist_ok=True)
    20→    p.write_text(content)
    21→    return p
    22→
    23→
    24→def _detect(path: Path) -> tuple[list[dict], int]:
    25→    result = deprecated_detector_mod.detect_deprecated_result(path)
    26→    return result.entries, result.population_size
    27→
    28→
    29→# ── _extract_deprecated_symbol ───────────────────────────────
    30→
    31→
    32→class TestExtractDeprecatedSymbol:
    33→    def test_inline_jsdoc_top_level_const(self, tmp_path):
    34→        """Inline JSDoc @deprecated on top-level const is extracted."""
    35→
    36→        _write(
    37→            tmp_path,
    38→            "old.ts",
    39→            "/** @deprecated Use newThing instead */ export const oldThing = 1;\n",
    40→        )
    41→        symbol, kind = deprecated_detector_mod._extract_deprecated_symbol(
    42→            str(tmp_path / "old.ts"),
    43→            1,
    44→            "/** @deprecated Use newThing instead */ export const oldThing = 1;",
    45→        )
    46→        assert symbol == "oldThing"
    47→        assert kind == "top-level"
    48→
    49→    def test_inline_jsdoc_property(self, tmp_path):
    50→        """Inline JSDoc @deprecated on a property is extracted as property kind."""
    51→
    52→        _write(
    53→            tmp_path,
    54→            "types.ts",
    55→            (
    56→                "interface Config {\n"
    57→                "  /** @deprecated */ oldField?: string;\n"
    58→                "  newField: string;\n"
    59→                "}\n"
    60→            ),
    61→        )
    62→        symbol, kind = deprecated_detector_mod._extract_deprecated_symbol(
    63→            str(tmp_path / "types.ts"), 2, "  /** @deprecated */ oldField?: string;"
    64→        )
    65→        assert symbol == "oldField"
    66→        assert kind == "property"
    67→
    68→    def test_multiline_jsdoc_function(self, tmp_path):
    69→        """Multi-line JSDoc @deprecated on function is extracted."""
    70→
    71→        _write(
    72→            tmp_path,
    73→            "api.ts",
    74→            (
    75→                "/**\n"
    76→                " * @deprecated Use newFetch instead\n"
    77→                " */\n"
    78→                "export function oldFetch() { return null; }\n"
    79→            ),
    80→        )
    81→        symbol, kind = deprecated_detector_mod._extract_deprecated_symbol(
    82→            str(tmp_path / "api.ts"), 2, " * @deprecated Use newFetch instead"
    83→        )
    84→        assert symbol == "oldFetch"
    85→        assert kind == "top-level"
    86→
    87→    def test_multiline_jsdoc_interface(self, tmp_path):
    88→        """Multi-line JSDoc @deprecated on interface is extracted."""
    89→
    90→        _write(
    91→            tmp_path,
    92→            "types.ts",
    93→            (
    94→                "/**\n"
    95→                " * @deprecated Use NewType instead\n"
    96→                " */\n"
    97→                "export interface OldType {\n"
    98→                "  field: string;\n"
    99→                "}\n"
   100→            ),
   101→        )
   102→        symbol, kind = deprecated_detector_mod._extract_deprecated_symbol(
   103→            str(tmp_path / "types.ts"), 2, " * @deprecated Use NewType instead"
   104→        )
   105→        assert symbol == "OldType"
   106→        assert kind == "top-level"
   107→
   108→    def test_inline_comment_deprecation(self, tmp_path):
   109→        """// @deprecated on same line as a property is extracted."""
   110→
   111→        _write(
   112→            tmp_path,
   113→            "types.ts",
   114→            ("interface Config {\n  shotImageEntryId?: string; // @deprecated\n}\n"),
   115→        )
   116→        symbol, kind = deprecated_detector_mod._extract_deprecated_symbol(
   117→            str(tmp_path / "types.ts"), 2, "  shotImageEntryId?: string; // @deprecated"
   118→        )
   119→        assert symbol == "shotImageEntryId"
   120→        assert kind == "property"
   121→
   122→    def test_returns_none_for_unresolvable(self, tmp_path):
   123→        """Returns (None, 'unknown') when the symbol cannot be determined."""
   124→
   125→        _write(tmp_path, "weird.ts", "@deprecated\n\n\n")
   126→        symbol, kind = deprecated_detector_mod._extract_deprecated_symbol(
   127→            str(tmp_path / "weird.ts"), 1, "@deprecated"
   128→        )
   129→        assert symbol is None
   130→        assert kind == "unknown"
   131→
   132→
   133→# ── detect_deprecated ────────────────────────────────────────
   134→
   135→
   136→class TestDetectDeprecated:
   137→    def test_finds_deprecated_annotations(self, tmp_path):
   138→        """detect_deprecated finds files with @deprecated JSDoc tags."""
   139→
   140→        _write(
   141→            tmp_path,
   142→            "old.ts",
   143→            (
   144→                "/**\n"
   145→                " * @deprecated Use newHelper instead\n"
   146→                " */\n"
   147→                "export function oldHelper() { return null; }\n"
   148→            ),
   149→        )
   150→        entries, count = _detect(tmp_path)
   151→        assert len(entries) >= 1
   152→        assert entries[0]["symbol"] == "oldHelper"
   153→        assert entries[0]["kind"] == "top-level"
   154→
   155→    def test_deduplicates_same_symbol_in_file(self, tmp_path):
   156→        """Same symbol with multiple @deprecated annotations in one file is deduplicated."""
   157→
   158→        _write(
   159→            tmp_path,
   160→            "dupes.ts",
   161→            (
   162→                "/**\n"
   163→                " * @deprecated\n"
   164→                " * @deprecated (duplicate)\n"
   165→                " */\n"
   166→                "export function oldThing() {}\n"
   167→            ),
   168→        )
   169→        entries, _ = _detect(tmp_path)
   170→        symbols = [e["symbol"] for e in entries if e["symbol"] == "oldThing"]
   171→        assert len(symbols) <= 1
   172→
   173→    def test_empty_directory(self, tmp_path):
   174→        """Empty directory returns no entries."""
   175→
   176→        entries, count = _detect(tmp_path)
   177→        assert entries == []
   178→        assert count == 0
   179→
   180→    def test_file_without_deprecated(self, tmp_path):
   181→        """Files without @deprecated produce no entries."""
   182→
   183→        _write(tmp_path, "clean.ts", "export function activeHelper() { return 1; }\n")
   184→        entries, _ = _detect(tmp_path)
   185→        assert entries == []
   186→
   187→    def test_distinguishes_top_level_and_property(self, tmp_path):
   188→        """Entries correctly classify top-level vs property deprecations."""
   189→
   190→        _write(
   191→            tmp_path,
   192→            "mixed.ts",
   193→            (
   194→                "/**\n"
   195→                " * @deprecated Use new API\n"
   196→                " */\n"
   197→                "export function oldFunc() {}\n"
   198→                "\n"
   199→                "interface Config {\n"
   200→                "  /** @deprecated */ oldProp?: string;\n"
   201→                "}\n"
   202→            ),
   203→        )
   204→        entries, _ = _detect(tmp_path)
   205→        kinds = {e["kind"] for e in entries}
   206→        assert "top-level" in kinds
   207→        assert "property" in kinds
   208→
   209→    def test_detects_mixed_case_deprecated_markers(self, tmp_path):
   210→        """Mixed-case @Deprecated markers should be detected."""
   211→        _write(
   212→            tmp_path,
   213→            "legacy.ts",
   214→            (
   215→                "/**\n"
   216→                " * @Deprecated Use newFunc\n"
   217→                " */\n"
   218→                "export function oldFunc() {}\n"
   219→            ),
   220→        )
   221→        entries, _ = _detect(tmp_path)
   222→        symbols = {e["symbol"] for e in entries}
   223→        assert "oldFunc" in symbols
   224→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/analysis.py"
}
```

> TOOL

tool_result Read
```
1→"""Canonical TypeScript analysis ownership surface.
     2→
     3→This module owns phase wiring and analysis entrypoints consumed by the
     4→TypeScript language config and command registry.
     5→"""
     6→
     7→from __future__ import annotations
     8→
     9→from pathlib import Path
    10→
    11→from desloppify.base.discovery.source import find_ts_and_tsx_files
    12→from desloppify.engine.detectors.base import FunctionInfo
    13→from desloppify.languages._framework.base.types import DetectorPhase
    14→from desloppify.languages._framework.treesitter.phases import make_cohesion_phase
    15→import desloppify.languages.typescript.detectors.deps as deps_detector_mod
    16→from desloppify.languages.typescript.detectors.security.detector import detect_ts_security
    17→from desloppify.languages.typescript.extractors_functions import extract_ts_functions
    18→from desloppify.languages.typescript.phases_basic import (
    19→    phase_deprecated,
    20→    phase_exports,
    21→    phase_logs,
    22→    phase_unused,
    23→)
    24→from desloppify.languages.typescript.phases_config import (
    25→    TS_COMPLEXITY_SIGNALS,
    26→    TS_GOD_RULES,
    27→    TS_SKIP_DIRS,
    28→    TS_SKIP_NAMES,
    29→)
    30→from desloppify.languages.typescript.phases_coupling import (
    31→    phase_coupling,
    32→)
    33→from desloppify.languages.typescript.phases_smells import phase_smells
    34→from desloppify.languages.typescript.phases_structural import phase_structural
    35→
    36→
    37→def ts_treesitter_phases() -> list[DetectorPhase]:
    38→    """Cherry-pick tree-sitter phases that complement TS's own detectors."""
    39→    from desloppify.languages._framework.treesitter import get_spec, is_available
    40→
    41→    if not is_available():
    42→        return []
    43→
    44→    spec = get_spec("typescript")
    45→    if spec is None:
    46→        return []
    47→
    48→    return [make_cohesion_phase(spec)]
    49→
    50→
    51→def ts_extract_functions(path: Path) -> list[FunctionInfo]:
    52→    """Extract all TS functions for duplicate detection."""
    53→    functions = []
    54→    for filepath in find_ts_and_tsx_files(path):
    55→        if "node_modules" in filepath or ".d.ts" in filepath:
    56→            continue
    57→        functions.extend(extract_ts_functions(filepath))
    58→    return functions
    59→
    60→
    61→build_dep_graph = deps_detector_mod.build_dep_graph
    62→detect_ts_security_result = detect_ts_security
    63→
    64→__all__ = [
    65→    "TS_COMPLEXITY_SIGNALS",
    66→    "TS_GOD_RULES",
    67→    "TS_SKIP_DIRS",
    68→    "TS_SKIP_NAMES",
    69→    "build_dep_graph",
    70→    "detect_ts_security_result",
    71→    "phase_coupling",
    72→    "phase_deprecated",
    73→    "phase_exports",
    74→    "phase_logs",
    75→    "phase_smells",
    76→    "phase_structural",
    77→    "phase_unused",
    78→    "ts_extract_functions",
    79→    "ts_treesitter_phases",
    80→]
    81→
```

> TOOL

tool_use Grep
```json
{
  "pattern": "compat\\.triage",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "context": 2
}
```

> TOOL

tool_result Grep
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/plan_triage.py-8-    TRIAGE_STAGE_IDS,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/plan_triage.py-9-)
desloppify/engine/plan_triage.py:10:from desloppify.engine._plan.compat.triage.core import (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/plan_triage.py-11-    TriageInput,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/plan_triage.py-12-    build_triage_prompt,
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-9-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-10-import desloppify.engine._plan.auto_cluster_sync_issue as auto_cluster_sync_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:11:import desloppify.engine._plan.compat.triage.apply as triage_apply_compat_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:12:import desloppify.engine._plan.compat.triage.core as triage_core_compat_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:13:import desloppify.engine._plan.compat.triage.dismiss as triage_dismiss_compat_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:14:import desloppify.engine._plan.compat.triage.parsing as triage_parsing_compat_mod
desloppify/tests/engine/test_sync_split_modules_direct.py:15:import desloppify.engine._plan.compat.triage.prompt as triage_prompt_compat_mod
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-16-import desloppify.engine._plan.constants as plan_constants_mod
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-17-import desloppify.engine._plan.epic_triage_apply as triage_apply_legacy_mod
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-80-        assert "Compat bridge" in src
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-81-        assert "import_module" in src
desloppify/tests/engine/test_sync_split_modules_direct.py:82:        assert "engine._plan.compat.triage" in src
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-83-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py-84-    compat_modules = (
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py-1-"""Compatibility bridge to grouped triage prompt contracts.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py-2-
desloppify/engine/_plan/epic_triage_prompt.py:3:Canonical implementation now lives in ``engine._plan.compat.triage.prompt``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py-9-
desloppify/engine/_plan/epic_triage_prompt.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.prompt")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/epic_triage_prompt.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py-1-"""Compatibility bridge to grouped triage dismissal helpers.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py-2-
desloppify/engine/_plan/epic_triage_dismiss.py:3:Canonical implementation now lives in ``engine._plan.compat.triage.dismiss``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py-9-
desloppify/engine/_plan/epic_triage_dismiss.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.dismiss")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/epic_triage_dismiss.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py-1-"""Compatibility bridge to grouped triage apply helpers.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py-2-
desloppify/engine/_plan/epic_triage_apply.py:3:Canonical implementation now lives in ``engine._plan.compat.triage.apply``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py-9-
desloppify/engine/_plan/epic_triage_apply.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.apply")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/epic_triage_apply.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py-1-"""Compat bridge for legacy whole-plan triage apply imports.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py-2-
desloppify/engine/_plan/triage/apply.py:3:Canonical implementation lives in ``engine._plan.compat.triage.apply``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py-9-
desloppify/engine/_plan/triage/apply.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.apply")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/triage/apply.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py-1-"""Compat bridge for legacy whole-plan triage prompt imports.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py-2-
desloppify/engine/_plan/triage/prompt.py:3:Canonical implementation lives in ``engine._plan.compat.triage.prompt``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py-9-
desloppify/engine/_plan/triage/prompt.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.prompt")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/triage/prompt.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py-1-"""Compat bridge for legacy whole-plan triage dismissal imports.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py-2-
desloppify/engine/_plan/triage/dismiss.py:3:Canonical implementation lives in ``engine._plan.compat.triage.dismiss``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py-9-
desloppify/engine/_plan/triage/dismiss.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.dismiss")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/triage/dismiss.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py-1-"""Compat bridge for legacy whole-plan triage core imports.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py-2-
desloppify/engine/_plan/triage/core.py:3:Canonical implementation lives in ``engine._plan.compat.triage.core``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py-9-
desloppify/engine/_plan/triage/core.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.core")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/triage/core.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/__init__.py-2-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/__init__.py-3-Staged triage contracts live here (for example ``playbook``). Legacy
desloppify/engine/_plan/triage/__init__.py:4:whole-plan triage runtime lives in ``engine._plan.compat.triage``; modules in
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/__init__.py-5-this package (``core/apply/dismiss/parsing/prompt``) are compatibility bridges
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/__init__.py-6-that preserve legacy imports while keeping ownership explicit. They are not
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py-1-"""Compat bridge for legacy whole-plan triage parsing imports.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py-2-
desloppify/engine/_plan/triage/parsing.py:3:Canonical implementation lives in ``engine._plan.compat.triage.parsing``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py-9-
desloppify/engine/_plan/triage/parsing.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.parsing")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/triage/parsing.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-16-(for example ``compat.operations_skip`` / ``compat.operations_meta`` /
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-17-``compat.operations_lifecycle`` / ``compat.project_policy`` /
desloppify/engine/_plan/__init__.py:18:``compat.triage``) and delegate to grouped canonical implementations.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-19-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-20-Legacy whole-plan triage module names (``epic_triage_prompt``,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-21-``epic_triage_parsing``, ``epic_triage_apply``, ``epic_triage_dismiss``)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-22-also remain as compatibility bridges and delegate to
desloppify/engine/_plan/__init__.py:23:``engine._plan.compat.triage.*``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py-24-
desloppify/engine/_plan/__init__.py-25-Other modules:
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py-1-"""Compatibility bridge to grouped triage parsing helpers.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py-2-
desloppify/engine/_plan/epic_triage_parsing.py:3:Canonical implementation now lives in ``engine._plan.compat.triage.parsing``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py-4-"""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py-5-
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py-8-from importlib import import_module
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py-9-
desloppify/engine/_plan/epic_triage_parsing.py:10:_IMPL = import_module("desloppify.engine._plan.compat.triage.parsing")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py-11-__all__ = list(getattr(_IMPL, "__all__", ()))
desloppify/engine/_plan/epic_triage_parsing.py-12-globals().update({name: getattr(_IMPL, name) for name in __all__})
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-3-Primary runtime triage orchestration is staged and lives in
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-4-``app.commands.plan.triage``. The legacy single-shot ``triage_epics`` runtime
desloppify/engine/_plan/compat/triage/core.py:5:lives under ``engine._plan.compat.triage``; callers may still use bridged
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-6-imports from ``engine._plan.triage`` and ``engine._plan.epic_triage_*``.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-7-"""
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-17-from desloppify.engine._state.schema import StateModel
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-18-
desloppify/engine/_plan/compat/triage/core.py:19:from desloppify.engine._plan.compat.triage.apply import (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-20-    TriageMutationResult,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-21-    apply_triage_to_plan,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-22-)
desloppify/engine/_plan/compat/triage/core.py:23:from desloppify.engine._plan.compat.triage.parsing import (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-24-    ISSUE_ID_RE,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-25-    extract_issue_citations,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-26-    parse_triage_result,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-27-)
desloppify/engine/_plan/compat/triage/core.py:28:from desloppify.engine._plan.compat.triage.prompt import (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-29-    _TRIAGE_SYSTEM_PROMPT,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py-30-    ContradictionNote,
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/__init__.py-2-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/__init__.py-3-Canonical staged triage orchestration lives in ``app.commands.plan.triage``.
desloppify/engine/_plan/compat/__init__.py:4:The modules under ``engine._plan.compat.triage`` provide the legacy
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/__init__.py-5-whole-plan triage implementation.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/__init__.py-6-"""
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/__init__.py"
}
```

> TOOL

tool_result Read
```
1→"""TypeScript/React language configuration for desloppify."""
     2→
     3→from __future__ import annotations
     4→
     5→from desloppify.base.discovery.paths import get_area
     6→from desloppify.engine.hook_registry import register_lang_hooks
     7→from desloppify.languages._framework.base.phase_builders import (
     8→    detector_phase_security,
     9→    detector_phase_signature,
    10→    detector_phase_test_coverage,
    11→    shared_subjective_duplicates_tail,
    12→)
    13→from desloppify.languages._framework.base.types import (
    14→    BoundaryRule,
    15→    DetectorPhase,
    16→    LangConfig,
    17→    LangSecurityResult,
    18→)
    19→from desloppify.languages._framework.registration import register_full_plugin
    20→from desloppify.languages.typescript import test_coverage as ts_test_coverage_hooks
    21→from desloppify.languages.typescript import analysis as ts_analysis_mod
    22→from desloppify.languages.typescript._fixers import get_ts_fixers
    23→import desloppify.languages.typescript.detectors.cli as ts_detector_cli_mod
    24→from desloppify.languages.typescript.detectors.io import iter_typescript_sources
    25→from desloppify.languages.typescript.review import (
    26→    HOLISTIC_REVIEW_DIMENSIONS as TS_HOLISTIC_REVIEW_DIMENSIONS,
    27→    LOW_VALUE_PATTERN as TS_LOW_VALUE_PATTERN,
    28→    MIGRATION_MIXED_EXTENSIONS as TS_MIGRATION_MIXED_EXTENSIONS,
    29→    MIGRATION_PATTERN_PAIRS as TS_MIGRATION_PATTERN_PAIRS,
    30→    REVIEW_GUIDANCE as TS_REVIEW_GUIDANCE,
    31→    api_surface as ts_review_api_surface,
    32→    module_patterns as ts_review_module_patterns,
    33→)
    34→from desloppify.languages.typescript._zones import TS_ZONE_RULES
    35→from desloppify.languages.typescript.plugin_contract import (
    36→    TS_BARREL_NAMES,
    37→    TS_COMPLEXITY_THRESHOLD,
    38→    TS_DEFAULT_SRC,
    39→    TS_ENTRY_PATTERNS,
    40→    TS_EXCLUSIONS,
    41→    TS_EXTENSIONS,
    42→    TS_LARGE_THRESHOLD,
    43→)
    44→
    45→TS_COMPLEXITY_SIGNALS = ts_analysis_mod.TS_COMPLEXITY_SIGNALS
    46→TS_GOD_RULES = ts_analysis_mod.TS_GOD_RULES
    47→TS_SKIP_DIRS = ts_analysis_mod.TS_SKIP_DIRS
    48→TS_SKIP_NAMES = ts_analysis_mod.TS_SKIP_NAMES
    49→
    50→class TypeScriptConfig(LangConfig):
    51→    def detect_lang_security_detailed(self, files, zone_map):
    52→        result = ts_analysis_mod.detect_ts_security_result(files, zone_map)
    53→        return LangSecurityResult(
    54→            entries=result.entries,
    55→            files_scanned=result.population_size,
    56→        )
    57→
    58→    def __init__(self):
    59→        super().__init__(
    60→            name="typescript",
    61→            extensions=TS_EXTENSIONS,
    62→            exclusions=TS_EXCLUSIONS,
    63→            default_src=TS_DEFAULT_SRC,
    64→            build_dep_graph=ts_analysis_mod.build_dep_graph,
    65→            entry_patterns=TS_ENTRY_PATTERNS,
    66→            barrel_names=TS_BARREL_NAMES,
    67→            phases=[
    68→                DetectorPhase("Logs", ts_analysis_mod.phase_logs),
    69→                DetectorPhase("Unused (tsc)", ts_analysis_mod.phase_unused),
    70→                DetectorPhase("Dead exports", ts_analysis_mod.phase_exports),
    71→                DetectorPhase("Deprecated", ts_analysis_mod.phase_deprecated),
    72→                DetectorPhase("Structural analysis", ts_analysis_mod.phase_structural),
    73→                DetectorPhase(
    74→                    "Coupling + single-use + patterns + naming",
    75→                    ts_analysis_mod.phase_coupling,
    76→                ),
    77→                *ts_analysis_mod.ts_treesitter_phases(),
    78→                detector_phase_signature(),
    79→                detector_phase_test_coverage(),
    80→                DetectorPhase("Code smells", ts_analysis_mod.phase_smells),
    81→                detector_phase_security(),
    82→                *shared_subjective_duplicates_tail(),
    83→            ],
    84→            fixers=get_ts_fixers(),
    85→            get_area=get_area,
    86→            detect_commands=ts_detector_cli_mod.get_detect_commands(),
    87→            boundaries=[
    88→                BoundaryRule("shared/", "tools/", "shared→tools"),
    89→            ],
    90→            typecheck_cmd="npx tsc --noEmit",
    91→            file_finder=iter_typescript_sources,
    92→            large_threshold=TS_LARGE_THRESHOLD,
    93→            complexity_threshold=TS_COMPLEXITY_THRESHOLD,
    94→            default_scan_profile="full",
    95→            detect_markers=["package.json"],
    96→            external_test_dirs=["tests", "test", "__tests__"],
    97→            test_file_extensions=[".ts", ".tsx"],
    98→            review_module_patterns_fn=ts_review_module_patterns,
    99→            review_api_surface_fn=ts_review_api_surface,
   100→            review_guidance=TS_REVIEW_GUIDANCE,
   101→            review_low_value_pattern=TS_LOW_VALUE_PATTERN,
   102→            holistic_review_dimensions=TS_HOLISTIC_REVIEW_DIMENSIONS,
   103→            migration_pattern_pairs=TS_MIGRATION_PATTERN_PAIRS,
   104→            migration_mixed_extensions=TS_MIGRATION_MIXED_EXTENSIONS,
   105→            extract_functions=ts_analysis_mod.ts_extract_functions,
   106→            zone_rules=TS_ZONE_RULES,
   107→        )
   108→
   109→
   110→def register() -> None:
   111→    """Register TypeScript language config + hooks through an explicit entrypoint."""
   112→    register_full_plugin(
   113→        "typescript",
   114→        TypeScriptConfig,
   115→        test_coverage=ts_test_coverage_hooks,
   116→    )
   117→
   118→
   119→def register_hooks() -> None:
   120→    """Register TypeScript hook modules without language-config bootstrap."""
   121→    register_lang_hooks("typescript", test_coverage=ts_test_coverage_hooks)
   122→
   123→
   124→Config = TypeScriptConfig
   125→
   126→
   127→__all__ = [
   128→    "Config",
   129→    "TS_HOLISTIC_REVIEW_DIMENSIONS",
   130→    "TS_LOW_VALUE_PATTERN",
   131→    "TS_MIGRATION_MIXED_EXTENSIONS",
   132→    "TS_MIGRATION_PATTERN_PAIRS",
   133→    "TS_REVIEW_GUIDANCE",
   134→    "TS_ZONE_RULES",
   135→    "TypeScriptConfig",
   136→    "register",
   137→    "register_hooks",
   138→]
   139→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/__init__.py"
}
```

> TOOL

tool_result Read
```
1→"""Language registration API plus compatibility exports for legacy callers.
     2→
     3→Runtime code should prefer ``desloppify.languages.framework`` for framework
     4→access; this module focuses on registration and language lookup.
     5→
     6→Compatibility owner: language-framework
     7→Removal target (legacy module exports): 2026-06-30
     8→"""
     9→
    10→from __future__ import annotations
    11→
    12→from collections.abc import Callable
    13→from typing import TypeVar
    14→
    15→from desloppify.languages.framework import (
    16→    LangConfig,
    17→    auto_detect_lang,
    18→    available_langs,
    19→    get_lang,
    20→    make_lang_config,
    21→)
    22→from desloppify.languages._framework import discovery as _discovery_mod
    23→from desloppify.languages._framework import registry_state as _registry_state_mod
    24→from desloppify.languages._framework import resolution as _resolution_mod
    25→from desloppify.languages._framework import runtime as _runtime_mod
    26→from desloppify.languages._framework.contract_validation import validate_lang_contract
    27→from desloppify.languages._framework.policy import REQUIRED_DIRS, REQUIRED_FILES
    28→from desloppify.languages._framework.registration import register_lang_class_with
    29→from desloppify.languages._framework.structure_validation import validate_lang_structure
    30→
    31→T = TypeVar("T")
    32→
    33→# Backward-compatible module aliases for callers still importing them here.
    34→discovery = _discovery_mod
    35→registry_state = _registry_state_mod
    36→resolution = _resolution_mod
    37→runtime = _runtime_mod
    38→
    39→_COMPAT_EXPORTS = {
    40→    "discovery": discovery,
    41→    "registry_state": registry_state,
    42→    "resolution": resolution,
    43→    "runtime": runtime,
    44→}
    45→
    46→
    47→def __getattr__(name: str):
    48→    if name in _COMPAT_EXPORTS:
    49→        value = _COMPAT_EXPORTS[name]
    50→        globals()[name] = value
    51→        return value
    52→    raise AttributeError(f"module 'desloppify.languages' has no attribute {name!r}")
    53→
    54→
    55→def register_lang(name: str) -> Callable[[T], T]:
    56→    """Decorator to register a language config class.
    57→
    58→    Validates structure, instantiates the class, validates the contract,
    59→    and stores the *instance* in the registry.
    60→    """
    61→
    62→    def decorator(cls: T) -> T:
    63→        register_lang_class_with(
    64→            name,
    65→            cls,
    66→            validate_lang_structure_fn=validate_lang_structure,
    67→        )
    68→        return cls
    69→
    70→    return decorator
    71→
    72→
    73→def register_generic_lang(name: str, cfg: LangConfig) -> None:
    74→    """Register a pre-built language plugin instance (no package structure required)."""
    75→    validate_lang_contract(name, cfg)
    76→    registry_state.register(name, cfg)
    77→
    78→
    79→def reload_lang_plugins() -> list[str]:
    80→    """Force plugin rediscovery and return refreshed language names."""
    81→    discovery.load_all(force_reload=True)
    82→    return sorted(registry_state.all_keys())
    83→
    84→
    85→__all__ = [
    86→    "REQUIRED_FILES",
    87→    "REQUIRED_DIRS",
    88→    "register_lang",
    89→    "register_generic_lang",
    90→    "reload_lang_plugins",
    91→    "get_lang",
    92→    "available_langs",
    93→    "auto_detect_lang",
    94→    "make_lang_config",
    95→    "validate_lang_structure",
    96→    "validate_lang_contract",
    97→]
    98→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/framework.py"
}
```

> TOOL

tool_result Read
```
1→"""Public framework facade for non-language-package consumers.
     2→
     3→Use this module from app/engine layers instead of importing
     4→``desloppify.languages._framework`` directly.
     5→
     6→Legacy module-level exports (``discovery``/``registry_state``/``resolution``/
     7→``runtime``) are compatibility fallbacks only.
     8→"""
     9→
    10→from __future__ import annotations
    11→
    12→from desloppify.languages._framework import discovery as _discovery_mod
    13→from desloppify.languages._framework import registry_state as _registry_state_mod
    14→from desloppify.languages._framework import resolution as _resolution_mod
    15→from desloppify.languages._framework import runtime as _runtime_mod
    16→from desloppify.languages._framework.base.types import (
    17→    BoundaryRule,
    18→    DetectorCoverageRecord,
    19→    DetectorPhase,
    20→    FixerConfig,
    21→    FixResult,
    22→    LangConfig,
    23→    LangRuntimeContract,
    24→    LangSecurityResult,
    25→    ScanCoverageRecord,
    26→)
    27→from desloppify.languages._framework.runtime import (
    28→    LangRun,
    29→    LangRunOverrides,
    30→    make_lang_run,
    31→)
    32→from desloppify.languages._framework.resolution import (
    33→    auto_detect_lang,
    34→    available_langs,
    35→    get_lang,
    36→    make_lang_config,
    37→)
    38→
    39→load_all = _discovery_mod.load_all
    40→
    41→_COMPAT_EXPORTS = {
    42→    "discovery": _discovery_mod,
    43→    "registry_state": _registry_state_mod,
    44→    "resolution": _resolution_mod,
    45→    "runtime": _runtime_mod,
    46→}
    47→
    48→
    49→def __getattr__(name: str):
    50→    """Compatibility fallback for legacy module-level exports.
    51→
    52→    Canonical runtime imports should target explicit functions/types from this
    53→    facade; broad submodule exports are kept for transitional callers only.
    54→    """
    55→    if name in _COMPAT_EXPORTS:
    56→        value = _COMPAT_EXPORTS[name]
    57→        globals()[name] = value
    58→        return value
    59→    raise AttributeError(f"module 'desloppify.languages.framework' has no attribute {name!r}")
    60→
    61→
    62→def shared_phase_labels() -> set[str]:
    63→    """Return generic shared phase labels lazily to avoid import cycles."""
    64→    from desloppify.languages._framework.generic import SHARED_PHASE_LABELS
    65→
    66→    return SHARED_PHASE_LABELS
    67→
    68→
    69→def capability_report(cfg: LangRun) -> tuple[list[str], list[str]] | None:
    70→    """Return capability report lazily without importing generic internals eagerly."""
    71→    from desloppify.languages._framework.generic import capability_report as _capability_report
    72→
    73→    return _capability_report(cfg)
    74→
    75→
    76→def enable_parse_cache() -> None:
    77→    """Enable tree-sitter parse cache via facade boundary."""
    78→    from desloppify.languages._framework.treesitter import enable_parse_cache as _enable_parse_cache
    79→
    80→    _enable_parse_cache()
    81→
    82→
    83→def disable_parse_cache() -> None:
    84→    """Disable tree-sitter parse cache via facade boundary."""
    85→    from desloppify.languages._framework.treesitter import disable_parse_cache as _disable_parse_cache
    86→
    87→    _disable_parse_cache()
    88→
    89→
    90→__all__ = [
    91→    "BoundaryRule",
    92→    "LangConfig",
    93→    "LangRun",
    94→    "LangRunOverrides",
    95→    "DetectorCoverageRecord",
    96→    "DetectorPhase",
    97→    "FixerConfig",
    98→    "FixResult",
    99→    "LangRuntimeContract",
   100→    "LangSecurityResult",
   101→    "ScanCoverageRecord",
   102→    "auto_detect_lang",
   103→    "available_langs",
   104→    "capability_report",
   105→    "disable_parse_cache",
   106→    "enable_parse_cache",
   107→    "get_lang",
   108→    "load_all",
   109→    "make_lang_run",
   110→    "make_lang_config",
   111→    "shared_phase_labels",
   112→]
   113→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/lang/typescript/test_typescript_detectors_fixers_and_wrappers_split_direct.py"
}
```

> TOOL

tool_result Read
```
1→"""Direct tests for split TypeScript detector/fixer/wrapper helper modules."""
     2→
     3→from __future__ import annotations
     4→
     5→import inspect
     6→import json
     7→from pathlib import Path
     8→from types import SimpleNamespace
     9→
    10→import desloppify.languages.typescript._fixers as ts_fixers_mod
    11→import desloppify.languages.typescript.analysis as ts_analysis_mod
    12→import desloppify.languages.typescript.detectors.analysis as ts_detector_analysis_api_mod
    13→import desloppify.languages.typescript.detectors.cli as ts_detector_cli_api_mod
    14→import desloppify.languages.typescript.detectors.security.detector as ts_security_mod
    15→import desloppify.languages.typescript.detectors.smells_assets as ts_assets_mod
    16→import desloppify.languages.typescript.detectors.unused_fallback as ts_unused_mod
    17→import desloppify.languages.typescript as ts_lang_mod
    18→from desloppify.languages._framework.base.types import DetectorPhase
    19→from desloppify.languages.typescript.detectors.contracts import DetectorResult
    20→
    21→
    22→def test_typescript_config_uses_analysis_facade_for_wiring() -> None:
    23→    src = inspect.getsource(ts_lang_mod)
    24→    assert "languages.typescript import analysis as ts_analysis_mod" in src
    25→    assert "import desloppify.languages.typescript.detectors.cli as ts_detector_cli_mod" in src
    26→    assert "languages.typescript import commands as ts_commands_mod" not in src
    27→    assert "languages.typescript.phases import (" not in src
    28→    assert "languages.typescript._detectors import (" not in src
    29→
    30→
    31→def test_typescript_top_level_surface_removes_legacy_tools_and_compat_layers() -> None:
    32→    package_root = Path(__file__).resolve().parents[3]
    33→    # Legacy compat layers are fully removed.
    34→    assert not (package_root / "languages/typescript/compat").exists()
    35→    assert not (package_root / "languages/typescript/tools/__init__.py").exists()
    36→    assert not (package_root / "languages/typescript/tools/logs.py").exists()
    37→    assert not (package_root / "languages/typescript/tools/patterns.py").exists()
    38→    assert not (package_root / "languages/typescript/tools/react.py").exists()
    39→    # commands.py and phases.py are not required — detect commands are on
    40→    # LangConfig and phases are wired in __init__.py.
    41→    assert not (package_root / "languages/typescript/commands.py").exists()
    42→    assert not (package_root / "languages/typescript/phases.py").exists()
    43→
    44→
    45→def test_typescript_detector_surface_splits_cli_and_analysis_roles() -> None:
    46→    cli_source = inspect.getsource(ts_detector_cli_api_mod)
    47→    assert "build_standard_detect_registry(" in cli_source
    48→    assert "compose_detect_registry(" in cli_source
    49→    assert "ts_detector_analysis_mod" in cli_source
    50→
    51→    assert callable(ts_detector_cli_api_mod.cmd_logs)
    52→    assert callable(ts_detector_analysis_api_mod.build_dep_graph)
    53→
    54→
    55→def test_ts_detector_helpers_cover_treesitter_and_function_extraction(monkeypatch) -> None:
    56→    monkeypatch.setattr("desloppify.languages._framework.treesitter.is_available", lambda: False)
    57→    assert ts_analysis_mod.ts_treesitter_phases() == []
    58→
    59→    monkeypatch.setattr("desloppify.languages._framework.treesitter.is_available", lambda: True)
    60→    monkeypatch.setattr("desloppify.languages._framework.treesitter.get_spec", lambda _lang: SimpleNamespace())
    61→    monkeypatch.setattr(ts_analysis_mod, "make_cohesion_phase", lambda _spec: DetectorPhase("Cohesion", lambda *_args: ([], {})))
    62→    phases = ts_analysis_mod.ts_treesitter_phases()
    63→    assert len(phases) == 1
    64→    assert phases[0].label == "Cohesion"
    65→
    66→    monkeypatch.setattr(
    67→        ts_analysis_mod,
    68→        "find_ts_and_tsx_files",
    69→        lambda _path: ["src/a.ts", "src/types.d.ts", "node_modules/pkg/index.ts", "src/b.tsx"],
    70→    )
    71→    monkeypatch.setattr(ts_analysis_mod, "extract_ts_functions", lambda filepath: [SimpleNamespace(file=filepath)])
    72→    functions = ts_analysis_mod.ts_extract_functions(Path("."))
    73→    assert [fn.file for fn in functions] == ["src/a.ts", "src/b.tsx"]
    74→
    75→
    76→def test_ts_fixer_helpers_and_registry(monkeypatch) -> None:
    77→    monkeypatch.setattr(ts_fixers_mod.unused_detector_mod, "detect_unused", lambda _path, category: ([{"name": category}], 1))
    78→    monkeypatch.setattr(
    79→        ts_fixers_mod.logs_detector_mod,
    80→        "detect_logs",
    81→        lambda _path: DetectorResult(
    82→            entries=[{"name": "log"}],
    83→            population_kind="files",
    84→            population_size=1,
    85→        ),
    86→    )
    87→    monkeypatch.setattr(
    88→        ts_fixers_mod.smells_detector_mod,
    89→        "detect_smells",
    90→        lambda _path: (
    91→            [
    92→                {"id": "dead_useeffect", "matches": [{"name": "effect"}]},
    93→                {"id": "empty_if_chain", "matches": [{"name": "if"}]},
    94→            ],
    95→            2,
    96→        ),
    97→    )
    98→
    99→    class _Fixers:
   100→        @staticmethod
   101→        def fix_unused_imports(entries, *, dry_run=False):
   102→            return SimpleNamespace(entries=entries, dry_run=dry_run)
   103→
   104→        @staticmethod
   105→        def fix_debug_logs(entries, *, dry_run=False):
   106→            return SimpleNamespace(entries=[{"tags": ["debug"]}], dry_run=dry_run)
   107→
   108→        @staticmethod
   109→        def fix_unused_vars(entries, *, dry_run=False):
   110→            return SimpleNamespace(entries=entries, dry_run=dry_run)
   111→
   112→        @staticmethod
   113→        def fix_unused_params(entries, *, dry_run=False):
   114→            return SimpleNamespace(entries=entries, dry_run=dry_run)
   115→
   116→        @staticmethod
   117→        def fix_dead_useeffect(entries, *, dry_run=False):
   118→            return SimpleNamespace(entries=entries, dry_run=dry_run)
   119→
   120→        @staticmethod
   121→        def fix_empty_if_chain(entries, *, dry_run=False):
   122→            return SimpleNamespace(entries=entries, dry_run=dry_run)
   123→
   124→    monkeypatch.setattr(ts_fixers_mod, "_ts_fixers_mod", lambda: _Fixers)
   125→
   126→    assert ts_fixers_mod._det_unused("imports")(Path("."))[0]["name"] == "imports"
   127→    assert ts_fixers_mod._det_logs(Path("."))[0]["name"] == "log"
   128→    assert ts_fixers_mod._det_smell("dead_useeffect")(Path("."))[0]["name"] == "effect"
   129→
   130→    fixed_logs = ts_fixers_mod._fix_logs([{"name": "debug"}], dry_run=True)
   131→    assert fixed_logs.entries[0]["removed"] == ["debug"]
   132→
   133→    fixers = ts_fixers_mod.get_ts_fixers()
   134→    assert set(fixers.keys()) == {
   135→        "unused-imports",
   136→        "debug-logs",
   137→        "unused-vars",
   138→        "unused-params",
   139→        "dead-useeffect",
   140→        "empty-if-chain",
   141→    }
   142→    assert fixers["unused-imports"].detector == "unused"
   143→    assert fixers["debug-logs"].detector == "logs"
   144→
   145→
   146→def test_ts_security_detector_reports_line_and_file_level_issues(tmp_path) -> None:
   147→    page = tmp_path / "src" / "page.ts"
   148→    page.parent.mkdir(parents=True, exist_ok=True)
   149→    page.write_text(
   150→        "\n".join(
   151→            [
   152→                "const x = eval(userInput)",
   153→                "element.innerHTML = html",
   154→                "window.location = data.url",
   155→                "const payload = atob(token.split('.')[1])",
   156→            ]
   157→        ),
   158→        encoding="utf-8",
   159→    )
   160→
   161→    edge = tmp_path / "supabase" / "functions" / "foo" / "index.ts"
   162→    edge.parent.mkdir(parents=True, exist_ok=True)
   163→    edge.write_text(
   164→        "Deno.serve(async (req) => {\nconst a = JSON.parse(x)\nreturn new Response('ok')\n}",
   165→        encoding="utf-8",
   166→    )
   167→
   168→    sql = tmp_path / "db" / "schema.sql"
   169→    sql.parent.mkdir(parents=True, exist_ok=True)
   170→    sql.write_text("CREATE VIEW public.foo AS SELECT 1;", encoding="utf-8")
   171→
   172→    security_result = ts_security_mod.detect_ts_security(
   173→        [str(page), str(edge), str(sql)],
   174→        zone_map=None,
   175→    )
   176→    entries = security_result.entries
   177→    scanned = security_result.population_size
   178→    kinds = {entry["detail"]["kind"] for entry in entries}
   179→
   180→    assert scanned == 3
   181→    assert "eval_injection" in kinds
   182→    assert "innerHTML_assignment" in kinds
   183→    assert "open_redirect" in kinds
   184→    assert "unverified_jwt_decode" in kinds
   185→    assert "edge_function_missing_auth" in kinds
   186→    assert "json_parse_unguarded" in kinds
   187→    assert "rls_bypass_views" in kinds
   188→
   189→
   190→def test_ts_asset_smells_and_unused_fallback_helpers(monkeypatch, tmp_path) -> None:
   191→    assert ts_assets_mod._script_is_documented("Use `npm run test` and `pnpm lint`", "test") is True
   192→    assert ts_assets_mod._script_is_documented("No commands", "build") is False
   193→
   194→    css = tmp_path / "styles.css"
   195→    css.write_text("\n".join([".x { color: red !important; }"] * 320), encoding="utf-8")
   196→    (tmp_path / "README.md").write_text("Project docs\n", encoding="utf-8")
   197→    (tmp_path / "package.json").write_text(
   198→        json.dumps({"scripts": {"dev": "vite", "build": "vite build", "test": "vitest", "lint": "eslint"}}),
   199→        encoding="utf-8",
   200→    )
   201→
   202→    monkeypatch.setattr(ts_assets_mod, "get_project_root", lambda: tmp_path)
   203→    monkeypatch.setattr(ts_assets_mod, "find_source_files", lambda _path, _exts: [str(css)])
   204→
   205→    smell_counts = {
   206→        "css_monolith": [],
   207→        "css_important_overuse": [],
   208→        "docs_scripts_drift": [],
   209→    }
   210→    scanned = ts_assets_mod.detect_non_ts_asset_smells(tmp_path, smell_counts)
   211→    assert scanned == 2
   212→    assert smell_counts["css_monolith"]
   213→    assert smell_counts["css_important_overuse"]
   214→    assert smell_counts["docs_scripts_drift"]
   215→
   216→    assert ts_unused_mod._identifier_occurrences("const x = x + 1", "x") == 2
   217→    assert ts_unused_mod._extract_import_names("import a, { b as c, type D } from './m'") == ["a", "c", "D"]
   218→    assert ts_unused_mod._extract_import_names("const x = 1") == []
   219→
   220→    ts_file = tmp_path / "src.ts"
   221→    ts_file.write_text(
   222→        "\n".join(
   223→            [
   224→                "import { used, unusedItem } from './mod'",
   225→                "const live = used + 1",
   226→                "const deadVar = 1",
   227→                "console.log(live)",
   228→            ]
   229→        ),
   230→        encoding="utf-8",
   231→    )
   232→
   233→    monkeypatch.setattr(ts_unused_mod, "find_ts_and_tsx_files", lambda _path: [str(ts_file)])
   234→    monkeypatch.setattr(ts_unused_mod, "get_project_root", lambda: tmp_path)
   235→    monkeypatch.setattr(ts_unused_mod, "read_file_text", lambda filepath: Path(filepath).read_text(encoding="utf-8"))
   236→
   237→    unused_entries, scanned_files = ts_unused_mod.detect_unused_fallback(tmp_path, "all")
   238→    categories = {entry["category"] for entry in unused_entries}
   239→    assert scanned_files == 1
   240→    assert "imports" in categories
   241→    assert "vars" in categories
   242→
   243→    deno_root = tmp_path / "deno-app"
   244→    deno_root.mkdir(parents=True, exist_ok=True)
   245→    (deno_root / "deno.json").write_text("{}", encoding="utf-8")
   246→    monkeypatch.setattr(ts_unused_mod, "get_project_root", lambda: deno_root)
   247→    assert ts_unused_mod._contains_deno_markers(deno_root / "src") is True
   248→
   249→    deno_file = deno_root / "mod.ts"
   250→    deno_file.write_text("import x from 'https://deno.land/x/mod.ts'\n", encoding="utf-8")
   251→    assert ts_unused_mod._has_deno_import_syntax([str(deno_file)]) is True
   252→    assert ts_unused_mod.should_use_deno_fallback(Path("/tmp/supabase/functions/foo"), []) is True
   253→
   254→
   255→def test_ts_command_registry_canonical_surface_and_wrapper_passthrough(
   256→    monkeypatch,
   257→    tmp_path,
   258→) -> None:
   259→    cli_mod = ts_detector_cli_api_mod
   260→    printed: list[str] = []
   261→    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(" ".join(str(a) for a in args)))
   262→    monkeypatch.setattr(cli_mod, "colorize", lambda text, _style: text)
   263→    monkeypatch.setattr(cli_mod, "print_table", lambda *args, **kwargs: printed.append("TABLE"))
   264→
   265→    monkeypatch.setattr(
   266→        cli_mod.ts_detector_analysis_mod,
   267→        "build_dep_graph",
   268→        lambda _path: {
   269→            "src/a.ts": {
   270→                "imports": set(),
   271→                "importers": set(),
   272→                "import_count": 0,
   273→                "importer_count": 0,
   274→            }
   275→        },
   276→    )
   277→    monkeypatch.setattr(
   278→        cli_mod.orphaned_detector_mod,
   279→        "detect_orphaned_files",
   280→        lambda *_args, **_kwargs: ([{"file": "src/a.ts", "loc": 10}], 1),
   281→    )
   282→
   283→    cli_mod.cmd_orphaned(SimpleNamespace(path=str(tmp_path), json=True, top=5))
   284→    orphan_payload = json.loads(printed[-1])
   285→    assert orphan_payload["count"] == 1
   286→
   287→    monkeypatch.setattr(cli_mod, "find_ts_and_tsx_files", lambda _path: ["src/a.ts", "node_modules/x.ts", "src/types.d.ts"])
   288→    monkeypatch.setattr(cli_mod, "extract_ts_functions", lambda filepath: [SimpleNamespace(name="fn", file=filepath, line=1, loc=4)])
   289→    monkeypatch.setattr(
   290→        cli_mod.dupes_detector_mod,
   291→        "detect_duplicates",
   292→        lambda _functions, threshold: (
   293→            [
   294→                {
   295→                    "kind": "exact",
   296→                    "fn_a": {"name": "a", "file": "src/a.ts", "line": 1, "loc": 4},
   297→                    "fn_b": {"name": "b", "file": "src/b.ts", "line": 2, "loc": 4},
   298→                    "similarity": 1.0,
   299→                },
   300→                {
   301→                    "kind": "near-duplicate",
   302→                    "fn_a": {"name": "a", "file": "src/a.ts", "line": 1, "loc": 4},
   303→                    "fn_b": {"name": "c", "file": "src/c.ts", "line": 3, "loc": 6},
   304→                    "similarity": 0.88,
   305→                },
   306→            ],
   307→            2,
   308→        ),
   309→    )
   310→
   311→    printed.clear()
   312→    cli_mod.cmd_dupes(SimpleNamespace(path=str(tmp_path), json=False, top=5, threshold=0.8))
   313→    assert any("Exact duplicates" in line for line in printed)
   314→    assert any("Near-duplicates" in line for line in printed)
   315→    assert "TABLE" in printed
   316→
   317→    printed.clear()
   318→    cli_mod.cmd_dupes(SimpleNamespace(path=str(tmp_path), json=True, top=5, threshold=0.8))
   319→    dupes_payload = json.loads(printed[-1])
   320→    assert dupes_payload["count"] == 2
   321→
   322→    display_calls: list[dict] = []
   323→    monkeypatch.setattr(cli_mod, "display_entries", lambda args, entries, **kwargs: display_calls.append({"args": args, "entries": entries, **kwargs}))
   324→    monkeypatch.setattr(cli_mod, "extract_ts_components", lambda _path: ["Comp"])
   325→    monkeypatch.setattr(cli_mod.gods_detector_mod, "detect_gods", lambda _components, _rules: ([{"file": "src/App.tsx", "loc": 200, "detail": {"hook_total": 5}, "reasons": ["long"]}], 1))
   326→
   327→    cli_mod.cmd_gods(SimpleNamespace(path=str(tmp_path), json=False, top=5))
   328→    assert display_calls and display_calls[0]["label"] == "God components"
   329→
   330→    monkeypatch.setattr(cli_mod, "get_src_path", lambda: "src")
   331→    monkeypatch.setattr(cli_mod.coupling_detector_mod, "detect_coupling_violations", lambda *_args, **_kwargs: ([{"file": "src/shared/a.ts", "target": "src/tools/x.ts", "tool": "x"}], 1))
   332→    monkeypatch.setattr(cli_mod.coupling_detector_mod, "detect_boundary_candidates", lambda *_args, **_kwargs: ([{"file": "src/shared/only.ts", "loc": 20, "sole_tool": "x", "importer_count": 1}], 1))
   333→    monkeypatch.setattr(cli_mod.coupling_detector_mod, "detect_cross_tool_imports", lambda *_args, **_kwargs: ([{"file": "src/tools/a.ts", "target": "src/tools/b.ts", "source_tool": "a", "target_tool": "b"}], 1))
   334→
   335→    printed.clear()
   336→    cli_mod.cmd_coupling(SimpleNamespace(path=str(tmp_path), json=True, top=5))
   337→    coupling_payload = json.loads(printed[-1])
   338→    assert coupling_payload["violations"] == 1
   339→    assert coupling_payload["boundary_candidates"] == 1
   340→
   341→    registry = cli_mod.get_detect_commands()
   342→    assert registry["logs"] is cli_mod.cmd_logs
   343→    assert registry["unused"] is cli_mod.cmd_unused
   344→    assert registry["exports"] is cli_mod.cmd_exports
   345→    assert registry["deprecated"] is cli_mod.cmd_deprecated
   346→    assert registry["props"] is cli_mod.cmd_props
   347→    assert registry["concerns"] is cli_mod.cmd_concerns
   348→    assert registry["deps"] is cli_mod.cmd_deps
   349→    assert registry["cycles"] is cli_mod.cmd_cycles
   350→    assert registry["patterns"] is cli_mod.cmd_patterns
   351→    assert registry["react"] is cli_mod.cmd_react
   352→
```

> AGENT

Now let me search for all imports of `detectors.analysis` in the typescript directory:

> TOOL

tool_use Grep
```json
{
  "pattern": "import.*detectors\\.analysis|from.*detectors\\.analysis",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript"
}
```

> TOOL

tool_result Grep
```
Found 1 file
desloppify/languages/typescript/detectors/cli.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "import.*typescript\\.analysis|from.*typescript\\.analysis|ts_analysis_mod",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript"
}
```

> TOOL

tool_result Grep
```
Found 1 file
desloppify/languages/typescript/__init__.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "_COMPAT_EXPORTS",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/languages"
}
```

> TOOL

tool_result Grep
```
Found 2 files
desloppify/languages/__init__.py
desloppify/languages/framework.py
```

> AGENT

All 38 engine tests pass. Here's what was done:

- **Deleted** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/plan_public_exports.py` - this file contained only a `PLAN_PUBLIC_EXPORTS` list used by the now-deleted `engine.plan` shim. No other files imported from it or referenced `PLAN_PUBLIC_EXPORTS`.
- **No changes needed** to `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py` - it had no imports or references to `plan_public_exports`. The docstring mentions the public facades (`engine.plan_state`, `engine.plan_ops`, etc.) but that's architectural documentation, not a reference to the deleted file.

> AGENT

Perfect! Now I have all the information needed. Let me provide a comprehensive report.

## Complete File Contents Report

I have read all requested files. Here is the summary of findings:

### Step 3 Files:

**1. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/analysis.py`**
- 20 lines total
- A simple canonical facade that re-exports from `detectors.deps`, `detectors.facade`, and `detectors.smells`
- Contains: `build_dep_graph`, `build_dynamic_import_targets`, `detect_reexport_facades`, `detect_smells`, `ts_alias_resolver`

**2. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/cli.py`**
- 342 lines total
- CLI surface for all TypeScript detector commands
- Line 31: `import desloppify.languages.typescript.detectors.analysis as ts_detector_analysis_mod`
- Uses `ts_detector_analysis_mod` at lines: 85, 90, 116, 122, 123, 202
- Re-exports command functions and `get_detect_commands()`

**3. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/tests/test_ts_deprecated.py`**
- No references to `ts_detector_analysis`. Tests the deprecated symbol detection feature.
- Tests at lines 24-26 use `deprecated_detector_mod.detect_deprecated_result()` instead

### Step 4 Files:

**4. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/analysis.py`**
- 81 lines total
- Canonical TypeScript analysis ownership surface (non-CLI)
- Imports from `detectors.deps` at line 15
- Re-exports: `TS_COMPLEXITY_SIGNALS`, `TS_GOD_RULES`, `TS_SKIP_DIRS`, `TS_SKIP_NAMES`
- Functions: `ts_treesitter_phases()`, `ts_extract_functions()`, plus re-exported aliases
- Line 61: `build_dep_graph = deps_detector_mod.build_dep_graph`
- Line 62: `detect_ts_security_result = detect_ts_security`

**5. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/__init__.py`**
- 139 lines total
- Language configuration module
- Line 21: `from desloppify.languages.typescript import analysis as ts_analysis_mod`
- Line 23: `import desloppify.languages.typescript.detectors.cli as ts_detector_cli_mod`
- Uses `ts_analysis_mod` extensively in TypeScriptConfig class (lines 45-48, 52, 64, 68-77, 86)
- Imports from `ts_analysis_mod`: phases, constants, build_dep_graph, detect_ts_security_result, ts_extract_functions, ts_treesitter_phases

### Step 5 Files:

**6. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/__init__.py`**
- 98 lines total
- Language registration API module
- Lines 39-44: Defines `_COMPAT_EXPORTS` dict with backward-compat submodule aliases
- Lines 47-52: `__getattr__` function for lazy loading compat exports

**7. `/Users/user_c042661f/Documents/desloppify/desloppify/languages/framework.py`**
- 113 lines total
- Public framework facade
- Lines 41-46: Defines `_COMPAT_EXPORTS` dict (identical pattern to `__init__.py`)
- Lines 49-59: `__getattr__` function for lazy loading compat exports
- Contains actual public exports like `LangConfig`, `auto_detect_lang`, `get_lang`, `make_lang_config`

### Key Test File:

**8. `/Users/user_c042661f/Documents/desloppify/desloppify/tests/lang/typescript/test_typescript_detectors_fixers_and_wrappers_split_direct.py`**
- 352 lines total
- Critical validation tests for the TypeScript module structure
- Line 12: `import desloppify.languages.typescript.analysis as ts_analysis_mod`
- Line 12: `import desloppify.languages.typescript.detectors.analysis as ts_detector_analysis_api_mod`
- Tests verify:
  - Line 22-28: `ts_lang_mod` uses `analysis as ts_analysis_mod` (line 24)
  - Line 45-52: `ts_detector_cli_api_mod` imports and uses `ts_detector_analysis_mod`
  - Lines 255-352: Test coverage for CLI command registry passthrough

## Import Search Results:

**Imports of `detectors.analysis` in typescript directory:**
- Only found in: `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/detectors/cli.py` (line 31)

**Imports of `typescript.analysis` in typescript directory:**
- Only found in: `/Users/user_c042661f/Documents/desloppify/desloppify/languages/typescript/__init__.py` (line 21)

**References to `_COMPAT_EXPORTS` in languages/ directory:**
- `/Users/user_c042661f/Documents/desloppify/desloppify/languages/__init__.py` (lines 39-44)
- `/Users/user_c042661f/Documents/desloppify/desloppify/languages/framework.py` (lines 41-46)

All files have been read in their entirety and the exact content is available above.

> AGENT

Perfect! Now let me compile my comprehensive report based on all the files I've read:

## Triage Bridge Structure - Complete Report

I've analyzed the triage bridge architecture across the codebase. Here's the full mapping:

### File Contents Summary

#### Root-Level Bridge Files (Compatibility Shims)

**1. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_apply.py`** (13 lines)
- Bridge module using `importlib.import_module` to load `desloppify.engine._plan.compat.triage.apply`
- Forwards all exports from canonical implementation

**2. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_dismiss.py`** (13 lines)
- Bridge module using `importlib.import_module` to load `desloppify.engine._plan.compat.triage.dismiss`
- Forwards all exports from canonical implementation

**3. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_parsing.py`** (13 lines)
- Bridge module using `importlib.import_module` to load `desloppify.engine._plan.compat.triage.parsing`
- Forwards all exports from canonical implementation

**4. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/epic_triage_prompt.py`** (13 lines)
- Bridge module using `importlib.import_module` to load `desloppify.engine._plan.compat.triage.prompt`
- Forwards all exports from canonical implementation

#### Canonical Implementation Files (Under compat/)

**5. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/apply.py`** (240 lines)
- **Core implementation of plan mutations during triage**
- Key exports: `TriageMutationResult` (dataclass), `apply_triage_to_plan()`
- Functions:
  - `_epic_sort_key()` — sort epics by dependency_order
  - `_normalized_epic_name()` — ensure EPIC_PREFIX
  - `_update_existing_epic_cluster()` — mutate existing epic with new data
  - `_create_epic_cluster()` — create new epic cluster from triage data
  - `_upsert_triage_clusters()` — create/update all epics, return counts
  - `_reorder_queue_by_dependency()` — reorder work queue by epic dependency_order
  - `_set_triage_meta()` — update plan["epic_triage_meta"] with snapshot hash, dismissed_ids, etc.
  - `apply_triage_to_plan()` — orchestrator: upserts clusters, dismisses issues, reorders queue, sets metadata

**6. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/dismiss.py`** (73 lines)
- **Dismissal logic for triage-rejected issues**
- Key exports: `dismiss_triage_issues()`
- Functions:
  - `_triaged_out_payload()` — create skip record with kind='triaged_out'
  - `dismiss_triage_issues()` — move dismissed issues from queue to skipped dict, return (dismissed_ids, count)

**7. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/parsing.py`** (168 lines)
- **Parsing and validation of raw LLM triage output**
- Key exports: `ISSUE_ID_RE`, `extract_issue_citations()`, `parse_triage_result()`
- Regex patterns: `ISSUE_ID_RE` (full IDs), `BRACKET_SHORT_ID_RE` (short hashes in brackets)
- Functions:
  - `extract_issue_citations()` — extract issue IDs from free text (supports full IDs, short hashes, bracketed short)
  - `_parse_action_steps()` — parse and normalize action_steps list (title, detail, issue_refs, done)
  - `parse_triage_result()` — validate raw LLM dict into TriageResult (filters invalid IDs, validates direction)

**8. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/prompt.py`** (352 lines)
- **Data contracts and prompt building for legacy whole-plan triage**
- Key dataclasses:
  - `TriageInput` — all data needed for triage (open_issues, mechanical_issues, existing_epics, dimension_scores, new_since_last, resolved_since_last, previously_dismissed, triage_version, resolved_issues, completed_clusters)
  - `DismissedIssue` — issue_id + reason
  - `ContradictionNote` — kept issue, dismissed issue, reason
  - `TriageResult` — strategy_summary, epics list, dismissed_issues, contradiction_notes, priority_rationale
- Key functions:
  - `_issue_dimension()` — extract dimension from issue detail dict
  - `_recurring_dimensions()` — find dimensions with both open and resolved issues (signals loops)
  - `collect_triage_input()` — gather all data needed for LLM prompt from plan + state
  - `build_triage_prompt()` — construct user-facing prompt with all context sections
- System prompt: `_TRIAGE_SYSTEM_PROMPT` (~60 lines describing meta-plan instructions, available directions, plan tools, output schema)

**9. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/triage/core.py`** (158 lines)
- **Orchestrator for legacy whole-plan triage**
- Key exports: All types from apply/parsing/prompt + `TriageDeps`, `triage_epics()`, `detect_recurring_patterns()`, `last_real_review_timestamp()`
- Functions:
  - `last_real_review_timestamp()` — find most recent genuine review import (holistic/per_file/trusted_internal/attested_external)
  - `detect_recurring_patterns()` — find dimensions with both resolved AND open issues (signals recurring loops)
  - `triage_epics()` — orchestrator: collect input, build prompt, call LLM (if provided), parse result, apply to plan
- `TriageDeps` dataclass with injectable `llm_call` callable

#### Triage/ Subpackage (Secondary Bridges)

**10. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/__init__.py`** (13 lines)
- Package docstring explaining staged triage vs legacy whole-plan triage
- Only exports: `"playbook"` (staged triage contracts)
- Notes that legacy bridges (core/apply/dismiss/parsing/prompt) preserve legacy imports but aren't part of canonical public surface

**11. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/apply.py`** (13 lines)
- Secondary bridge: `importlib.import_module("desloppify.engine._plan.compat.triage.apply")`
- Allows imports from `engine._plan.triage.apply` (alternative import path)

**12. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/dismiss.py`** (13 lines)
- Secondary bridge: `importlib.import_module("desloppify.engine._plan.compat.triage.dismiss")`

**13. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/parsing.py`** (13 lines)
- Secondary bridge: `importlib.import_module("desloppify.engine._plan.compat.triage.parsing")`

**14. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/prompt.py`** (13 lines)
- Secondary bridge: `importlib.import_module("desloppify.engine._plan.compat.triage.prompt")`

**15. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/core.py`** (13 lines)
- Secondary bridge: `importlib.import_module("desloppify.engine._plan.compat.triage.core")`

**16. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/triage/playbook.py`** (155 lines)
- **Canonical shared triage workflow labels and command snippets**
- Not a bridge — actual implementation
- Stage labels: observe, reflect, organize, enrich, sense-check, commit
- Stage dependencies: observe → reflect → organize → enrich → sense-check → commit
- Command templates for each stage
- Key exports: `TRIAGE_STAGE_LABELS`, `TRIAGE_STAGE_DEPENDENCIES`, all `TRIAGE_CMD_*` constants
- Functions: `triage_run_stages_command()`, `triage_runner_commands()`, `triage_manual_stage_command()`

#### Public Facades

**17. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/plan_triage.py`** (120 lines)
- **Focused public plan API for triage orchestration surfaces**
- Imports from `engine._plan.compat.triage.core` (canonical implementation)
- Imports from `engine._plan.triage.playbook` (staged triage contracts)
- Imports from `engine._plan.sync.triage_start_policy` (triage start decision logic)
- Key function: `triage_phase_banner()` — returns status string describing triage readiness (RECOMMENDED / PENDING / MODE + progress)
- Re-exports all triage constants and functions in `__all__`

**18. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/__init__.py`** (31 lines)
- Package docstring explaining internal plan structure
- Documents that legacy `epic_triage_*` modules delegate to `engine._plan.compat.triage.*`

#### Compat Package

**19. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan/compat/__init__.py`** (11 lines)
- Package docstring
- Only exports: `"triage"` (legacy whole-plan triage implementation)

---

### Import Locations (Complete Graph)

Files that import from the triage bridge:

**1. `/Users/user_c042661f/Documents/desloppify/desloppify/engine/plan_triage.py`**
   - `from desloppify.engine._plan.compat.triage.core import (TriageInput, build_triage_prompt, collect_triage_input, detect_recurring_patterns, extract_issue_citations)`
   - `from desloppify.engine._plan.triage.playbook import (TRIAGE_CMD_*, TRIAGE_STAGE_*, triage_runner_commands, etc.)`
   - `from desloppify.engine._plan.sync.triage_start_policy import (TriageStartDecision, decide_triage_start)`

**2. `/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply.py`**
   - `from desloppify.engine._plan.epic_triage_apply import (TriageMutationResult, apply_triage_to_plan)`
   - `from desloppify.engine._plan.epic_triage_prompt import (DismissedIssue, TriageResult)`

**3. `/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_apply_edge_cases.py`**
   - `from desloppify.engine._plan.epic_triage_apply import apply_triage_to_plan`
   - `from desloppify.engine._plan.epic_triage_prompt import (DismissedIssue, TriageResult)`

**4. `/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_epic_triage_parsing_direct.py`**
   - `import desloppify.engine._plan.epic_triage_parsing as parsing_mod`

**5. `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/plan/test_triage_runner.py`**
   - `from desloppify.engine._plan.epic_triage_prompt import TriageInput`

**6. `/Users/user_c042661f/Documents/desloppify/desloppify/tests/engine/test_sync_split_modules_direct.py`**
   - Test file verifying bridge structure
   - Imports all four legacy bridges: `epic_triage_apply`, `epic_triage_parsing`, `epic_triage_prompt`, `epic_triage_dismiss`
   - Imports all compat implementations: `compat.triage.apply`, `compat.triage.core`, `compat.triage.dismiss`, `compat.triage.parsing`, `compat.triage.prompt`
   - Verifies bridges are thin wrappers with docstrings containing "Compat bridge" and "import_module"

---

### Architecture Summary

**Three-layer import structure:**

1. **Legacy root-level bridges** (`engine._plan.epic_triage_*`): Thin shims using `importlib.import_module()` — for backward compatibility
2. **Secondary triage/ bridges** (`engine._plan.triage.{apply,dismiss,parsing,prompt,core}`): Alternative import paths, also thin shims
3. **Canonical implementation** (`engine._plan.compat.triage.{apply,dismiss,parsing,prompt,core}`): Actual logic lives here
4. **Public facade** (`engine.plan_triage`): High-level orchestration API importing from canonical implementations
5. **Staged triage contracts** (`engine._plan.triage.playbook`): Shared workflow metadata (not a bridge)

**Key invariant:** All imports flow through the bridges to the canonical `compat.triage.*` implementations. Callers should ideally use the public facade (`engine.plan_triage`) rather than picking individual bridges.

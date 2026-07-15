> DEVELOPER

I need to understand the T1-T4 tier-based queue ordering system in this codebase. The user wants to remove tier as a hard queue-order control. 

Key areas to investigate:
1. Any `ranking.py` files - especially lines around L91, L105, L134 that sort by tier
2. `desloppify/engine/_work_queue/core.py` - especially around L417 for tier filtering
3. `desloppify/engine/_work_queue/helpers.py` - around L248 for subjective queue generation
4. Any other files in `desloppify/engine/_work_queue/` that reference tier-based sorting

For each file, read the relevant sections and provide the full context of how tiers affect queue ordering. I need to understand what code enforces "T1 before T2 before T3" ordering and "subjective forced behind mechanical".

> AGENT

I'll investigate the tier-based queue ordering system across these key files in parallel.

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/desloppify/**/ranking.py"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/engine/work_queue_internal/ranking.py
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/engine/_work_queue/ranking.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/**"
}
```

> TOOL

tool_result Glob
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/__init__.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/issues.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/__pycache__/__init__.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/__pycache__/ranking.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/__pycache__/issues.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/__pycache__/core.cpython-311.pyc
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/__pycache__/helpers.cpython-311.pyc
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py"
}
```

> TOOL

tool_result Read
```
1→"""Ranking and grouping helpers for work queue selection."""
     2→
     3→from __future__ import annotations
     4→
     5→from desloppify.engine._work_queue.helpers import (
     6→    detail_dict,
     7→    is_review_finding,
     8→    is_subjective_finding,
     9→    primary_command_for_finding,
    10→    review_finding_weight,
    11→    scope_matches,
    12→    slugify,
    13→    status_matches,
    14→    subjective_strict_scores,
    15→    supported_fixers_for_item,
    16→)
    17→from desloppify.engine.planning.common import CONFIDENCE_ORDER
    18→from desloppify.state import path_scoped_findings
    19→
    20→
    21→def subjective_score_value(item: dict) -> float:
    22→    if item.get("kind") == "subjective_dimension":
    23→        detail = detail_dict(item)
    24→        return float(detail.get("strict_score", item.get("subjective_score", 100.0)))
    25→    return float(item.get("subjective_score", 100.0))
    26→
    27→
    28→def build_finding_items(
    29→    state: dict,
    30→    *,
    31→    scan_path: str | None,
    32→    status_filter: str,
    33→    scope: str | None,
    34→    chronic: bool,
    35→) -> list[dict]:
    36→    scoped = path_scoped_findings(state.get("findings", {}), scan_path)
    37→    subjective_scores = subjective_strict_scores(state)
    38→    out: list[dict] = []
    39→
    40→    for finding_id, finding in scoped.items():
    41→        if finding.get("suppressed"):
    42→            continue
    43→        if not status_matches(finding.get("status", "open"), status_filter):
    44→            continue
    45→        if chronic and not (
    46→            finding.get("status") == "open" and finding.get("reopen_count", 0) >= 2
    47→        ):
    48→            continue
    49→
    50→        item = dict(finding)
    51→        item["id"] = finding_id
    52→        item["kind"] = "finding"
    53→        item["is_review"] = is_review_finding(item)
    54→        item["is_subjective"] = is_subjective_finding(item)
    55→        item["effective_tier"] = (
    56→            4 if item["is_subjective"] else int(finding.get("tier", 3))
    57→        )
    58→        item["review_weight"] = (
    59→            review_finding_weight(item) if item["is_review"] else None
    60→        )
    61→        subjective_score = None
    62→        if item["is_subjective"]:
    63→            detail = detail_dict(finding)
    64→            dim_name = detail.get("dimension_name", "")
    65→            dim_key = detail.get("dimension", "") or slugify(dim_name)
    66→            subjective_score = subjective_scores.get(
    67→                dim_key, subjective_scores.get(dim_name.lower(), 100.0)
    68→            )
    69→        item["subjective_score"] = subjective_score
    70→        supported_fixers = supported_fixers_for_item(state, item)
    71→        item["primary_command"] = primary_command_for_finding(
    72→            item,
    73→            supported_fixers=supported_fixers,
    74→        )
    75→
    76→        if not scope_matches(item, scope):
    77→            continue
    78→        out.append(item)
    79→
    80→    return out
    81→
    82→
    83→_CLUSTER_ACTION_PRIORITY = {"auto_fix": 0, "reorganize": 1, "refactor": 2, "manual_fix": 3}
    84→
    85→
    86→def item_sort_key(item: dict) -> tuple:
    87→    if item.get("kind") == "synthesis_needed":
    88→        # Synthesis items always sort first — they block all other work.
    89→        return (-1, 0, 0, item.get("id", ""))
    90→
    91→    if item.get("kind") == "cluster":
    92→        # Clusters sort before individual findings, ordered by action type
    93→        # (auto_fix first, then reorganize, refactor, manual_fix),
    94→        # then bigger clusters first within the same action type.
    95→        action_pri = _CLUSTER_ACTION_PRIORITY.get(
    96→            item.get("action_type", "manual_fix"), 3
    97→        )
    98→        return (
    99→            0,  # All clusters before all individual findings
   100→            action_pri,
   101→            -int(item.get("member_count", 0)),
   102→            item.get("id", ""),
   103→        )
   104→
   105→    if item.get("kind") == "subjective_dimension" or item.get("is_subjective"):
   106→        return (
   107→            int(item.get("effective_tier", 4)),
   108→            1,  # Subjective items sort after mechanical items within T4.
   109→            subjective_score_value(item),
   110→            item.get("id", ""),
   111→        )
   112→
   113→    detail = detail_dict(item)
   114→    review_weight = float(item.get("review_weight", 0.0) or 0.0)
   115→    return (
   116→        int(item.get("effective_tier", item.get("tier", 3))),
   117→        0,
   118→        CONFIDENCE_ORDER.get(item.get("confidence", "low"), 9),
   119→        -review_weight,
   120→        -int(detail.get("count", 0) or 0),
   121→        item.get("id", ""),
   122→    )
   123→
   124→
   125→def item_explain(item: dict) -> dict:
   126→    effective_tier = int(item.get("effective_tier", item.get("tier", 3)))
   127→
   128→    if item.get("kind") == "subjective_dimension":
   129→        return {
   130→            "kind": "subjective_dimension",
   131→            "effective_tier": effective_tier,
   132→            "subjective_score": subjective_score_value(item),
   133→            "policy": (
   134→                "Subjective dimensions are always queued as T4 and do not outrank "
   135→                "mechanical T1/T2/T3 items."
   136→            ),
   137→            "ranking_factors": ["tier asc", "subjective_score asc", "id asc"],
   138→        }
   139→
   140→    detail = detail_dict(item)
   141→    confidence = item.get("confidence", "low")
   142→    is_subjective = bool(item.get("is_subjective"))
   143→    is_review = bool(item.get("is_review"))
   144→    ranking_factors: list[str]
   145→    if is_subjective:
   146→        ranking_factors = ["tier fixed to T4", "subjective_score asc", "id asc"]
   147→    elif is_review:
   148→        ranking_factors = [
   149→            "tier asc",
   150→            "confidence asc",
   151→            "review_weight desc",
   152→            "count desc",
   153→            "id asc",
   154→        ]
   155→    else:
   156→        ranking_factors = ["tier asc", "confidence asc", "count desc", "id asc"]
   157→    explain = {
   158→        "kind": "finding",
   159→        "effective_tier": effective_tier,
   160→        "confidence": confidence,
   161→        "confidence_rank": CONFIDENCE_ORDER.get(confidence, 9),
   162→        "count": int(detail.get("count", 0) or 0),
   163→        "id": item.get("id", ""),
   164→        "ranking_factors": ranking_factors,
   165→    }
   166→    if is_review:
   167→        explain["review_weight"] = float(item.get("review_weight", 0.0) or 0.0)
   168→    if is_subjective:
   169→        explain["policy"] = (
   170→            "Subjective findings are forced to T4 and do not outrank "
   171→            "mechanical T1/T2/T3 items."
   172→        )
   173→        explain["subjective_score"] = subjective_score_value(item)
   174→    return explain
   175→
   176→
   177→def tier_counts(items: list[dict]) -> dict[int, int]:
   178→    counts = {1: 0, 2: 0, 3: 0, 4: 0}
   179→    for item in items:
   180→        if item.get("kind") == "cluster":
   181→            # Count each member at its own tier
   182→            for member in item.get("members", []):
   183→                tier = int(member.get("effective_tier", member.get("tier", 3)))
   184→                counts[tier] = counts.get(tier, 0) + 1
   185→            continue
   186→        tier = int(item.get("effective_tier", item.get("tier", 3)))
   187→        counts[tier] = counts.get(tier, 0) + 1
   188→    return counts
   189→
   190→
   191→def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
   192→    available = [tier for tier, count in counts.items() if count > 0]
   193→    if not available:
   194→        return None
   195→    return min(available, key=lambda tier: (abs(tier - requested_tier), tier))
   196→
   197→
   198→def group_queue_items(items: list[dict], group: str) -> dict[str, list[dict]]:
   199→    """Group queue items for alternate output modes."""
   200→    grouped: dict[str, list[dict]] = {}
   201→    for item in items:
   202→        if group == "file":
   203→            key = item.get("file", "")
   204→        elif group == "detector":
   205→            key = item.get("detector", "")
   206→        elif group == "tier":
   207→            key = f"T{int(item.get('effective_tier', item.get('tier', 3)))}"
   208→        elif group == "cluster":
   209→            plan_cluster = item.get("plan_cluster")
   210→            key = plan_cluster["name"] if isinstance(plan_cluster, dict) else "(unclustered)"
   211→        else:
   212→            key = "items"
   213→        grouped.setdefault(key, []).append(item)
   214→    return grouped
   215→
   216→
   217→__all__ = [
   218→    "build_finding_items",
   219→    "choose_fallback_tier",
   220→    "item_explain",
   221→    "item_sort_key",
   222→    "tier_counts",
   223→    "subjective_score_value",
   224→    "group_queue_items",
   225→]
   226→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py"
}
```

> TOOL

tool_result Read
```
1→"""Unified work-queue selection for next/show/plan views."""
     2→
     3→from __future__ import annotations
     4→
     5→from dataclasses import dataclass
     6→from collections import deque
     7→from typing import TypedDict
     8→
     9→from desloppify.engine._work_queue.helpers import (
    10→    ALL_STATUSES,
    11→    ATTEST_EXAMPLE,
    12→    build_subjective_items,
    13→    build_synthesis_item,
    14→    scope_matches,
    15→)
    16→from desloppify.engine._work_queue.ranking import (
    17→    build_finding_items,
    18→    choose_fallback_tier,
    19→    group_queue_items,
    20→    item_explain,
    21→    item_sort_key,
    22→    tier_counts,
    23→)
    24→from desloppify.state import StateModel
    25→
    26→
    27→@dataclass(frozen=True)
    28→class QueueBuildOptions:
    29→    """Configuration for queue construction and tier selection behavior."""
    30→
    31→    tier: int | None = None
    32→    count: int | None = 1
    33→    scan_path: str | None = None
    34→    scope: str | None = None
    35→    status: str = "open"
    36→    include_subjective: bool = True
    37→    subjective_threshold: float = 100.0
    38→    chronic: bool = False
    39→    no_tier_fallback: bool = False
    40→    explain: bool = False
    41→    plan: dict | None = None
    42→    include_skipped: bool = False
    43→    cluster: str | None = None
    44→    collapse_clusters: bool = True
    45→
    46→
    47→class WorkQueueResult(TypedDict):
    48→    """Typed shape of the dict returned by :func:`build_work_queue`."""
    49→
    50→    items: list[dict]
    51→    total: int
    52→    tier_counts: dict[int, int]
    53→    requested_tier: int | None
    54→    selected_tier: int | None
    55→    fallback_reason: str | None
    56→    available_tiers: list[int]
    57→    grouped: dict[str, list[dict]]
    58→    suppressed_count: int
    59→
    60→
    61→def _is_subjective_queue_item(item: dict) -> bool:
    62→    """Return True for queue items that represent subjective work."""
    63→    return item.get("kind") == "subjective_dimension" or bool(item.get("is_subjective"))
    64→
    65→
    66→def _apply_subjective_interleave_guardrail(
    67→    items: list[dict],
    68→    *,
    69→    objective_burst: int = 3,
    70→    subjective_burst: int = 1,
    71→) -> list[dict]:
    72→    """Interleave subjective work with objective work to avoid starvation."""
    73→    if objective_burst < 1 or subjective_burst < 1:
    74→        return items
    75→
    76→    subjective_items = deque(
    77→        item for item in items if _is_subjective_queue_item(item)
    78→    )
    79→    objective_items = deque(
    80→        item for item in items if not _is_subjective_queue_item(item)
    81→    )
    82→    if not subjective_items or not objective_items:
    83→        return items
    84→
    85→    interleaved: list[dict] = []
    86→    while objective_items and subjective_items:
    87→        for _ in range(objective_burst):
    88→            if not objective_items:
    89→                break
    90→            interleaved.append(objective_items.popleft())
    91→        for _ in range(subjective_burst):
    92→            if not subjective_items:
    93→                break
    94→            interleaved.append(subjective_items.popleft())
    95→
    96→    interleaved.extend(objective_items)
    97→    interleaved.extend(subjective_items)
    98→    return interleaved
    99→
   100→
   101→def _new_item_ids(state: StateModel) -> set[str]:
   102→    """Return finding IDs added in the most recent scan."""
   103→    scan_history = state.get("scan_history", [])
   104→    if not scan_history:
   105→        return set()
   106→    threshold = scan_history[-1].get("timestamp", "")
   107→    if not threshold:
   108→        return set()
   109→    return {
   110→        fid
   111→        for fid, f in state.get("findings", {}).items()
   112→        if f.get("first_seen", "") >= threshold
   113→    }
   114→
   115→
   116→def _apply_plan_order(
   117→    items: list[dict],
   118→    plan: dict,
   119→    *,
   120→    include_skipped: bool = False,
   121→    cluster: str | None = None,
   122→    new_ids: set[str] | None = None,
   123→) -> list[dict]:
   124→    """Reorder items according to the living plan.
   125→
   126→    1. Items in ``queue_order`` appear first, in that order.
   127→    2. Existing remaining items keep their mechanical sort.
   128→    3. New items (from latest scan) sort after existing remaining items.
   129→    4. Skipped items are appended last (or excluded).
   130→    5. Each item is annotated with plan metadata.
   131→    """
   132→    queue_order: list[str] = plan.get("queue_order", [])
   133→    skipped_map: dict = plan.get("skipped", {})
   134→    skipped_ids: set[str] = set(skipped_map.keys())
   135→    overrides: dict = plan.get("overrides", {})
   136→    clusters: dict = plan.get("clusters", {})
   137→    active_cluster = plan.get("active_cluster")
   138→
   139→    # Build lookup
   140→    by_id: dict[str, dict] = {}
   141→    for item in items:
   142→        by_id[item["id"]] = item
   143→
   144→    # Annotate items with plan metadata
   145→    for item_id, item in by_id.items():
   146→        override = overrides.get(item_id, {})
   147→        if override.get("description"):
   148→            item["plan_description"] = override["description"]
   149→        if override.get("note"):
   150→            item["plan_note"] = override["note"]
   151→        if override.get("cluster"):
   152→            cluster_name = override["cluster"]
   153→            cluster_data = clusters.get(cluster_name, {})
   154→            item["plan_cluster"] = {
   155→                "name": cluster_name,
   156→                "description": cluster_data.get("description"),
   157→                "total_items": len(cluster_data.get("finding_ids", [])),
   158→                "sibling_ids": cluster_data.get("finding_ids", []),
   159→            }
   160→
   161→    # Split into ordered, remaining, skipped
   162→    ordered: list[dict] = []
   163→    ordered_ids: set[str] = set()
   164→    for fid in queue_order:
   165→        if fid in by_id and fid not in skipped_ids:
   166→            ordered.append(by_id[fid])
   167→            ordered_ids.add(fid)
   168→
   169→    skipped_items: list[dict] = []
   170→    remaining_existing: list[dict] = []
   171→    remaining_new: list[dict] = []
   172→    _new = new_ids or set()
   173→    for item in items:
   174→        item_id = item["id"]
   175→        if item_id in ordered_ids:
   176→            continue
   177→        if item_id in skipped_ids:
   178→            skipped_items.append(item)
   179→        elif item_id in _new:
   180→            remaining_new.append(item)
   181→        else:
   182→            remaining_existing.append(item)
   183→
   184→    # Assign queue positions — new items after existing ones
   185→    result = ordered + remaining_existing + remaining_new
   186→    if include_skipped:
   187→        result = result + skipped_items
   188→
   189→    for pos, item in enumerate(result):
   190→        item["queue_position"] = pos + 1
   191→        if item["id"] in skipped_ids:
   192→            item["plan_skipped"] = True
   193→            skip_entry = skipped_map.get(item["id"])
   194→            if skip_entry:
   195→                item["plan_skip_kind"] = skip_entry.get("kind", "temporary")
   196→                skip_reason = skip_entry.get("reason")
   197→                if skip_reason:
   198→                    item["plan_skip_reason"] = skip_reason
   199→
   200→    # Filter to cluster if requested
   201→    effective_cluster = cluster or active_cluster
   202→    if effective_cluster:
   203→        cluster_data = clusters.get(effective_cluster, {})
   204→        cluster_member_ids = set(cluster_data.get("finding_ids", []))
   205→        if cluster_member_ids:
   206→            result = [item for item in result if item["id"] in cluster_member_ids]
   207→
   208→    return result
   209→
   210→
   211→def _item_matches_tier(item: dict, tier: int) -> bool:
   212→    """Check if an item (or any of its members for clusters) matches a tier."""
   213→    if item.get("kind") == "cluster":
   214→        return any(
   215→            int(m.get("effective_tier", m.get("tier", 3))) == tier
   216→            for m in item.get("members", [])
   217→        )
   218→    return int(item.get("effective_tier", item.get("tier", 3))) == tier
   219→
   220→
   221→def _action_type_for_detector(detector: str) -> str:
   222→    """Look up the action_type for a detector from the registry."""
   223→    try:
   224→        from desloppify.core.registry import DETECTORS
   225→        meta = DETECTORS.get(detector)
   226→        if meta:
   227→            return meta.action_type
   228→    except ImportError as exc:
   229→        _ = exc
   230→    return "manual_fix"
   231→
   232→
   233→_ACTION_TYPE_PRIORITY = {"auto_fix": 0, "reorganize": 1, "refactor": 2, "manual_fix": 3}
   234→
   235→
   236→def _collapse_clusters(items: list[dict], plan: dict) -> list[dict]:
   237→    """Replace cluster member items with single cluster meta-items."""
   238→    clusters = plan.get("clusters", {})
   239→    if not clusters:
   240→        return items
   241→
   242→    # Build mapping: finding_id → auto-cluster name
   243→    fid_to_cluster: dict[str, str] = {}
   244→    for name, cluster in clusters.items():
   245→        if not cluster.get("auto"):
   246→            continue
   247→        for fid in cluster.get("finding_ids", []):
   248→            fid_to_cluster[fid] = name
   249→
   250→    if not fid_to_cluster:
   251→        return items
   252→
   253→    # Collect members for each cluster, preserving order
   254→    cluster_members: dict[str, list[dict]] = {}
   255→    non_cluster_items: list[dict] = []
   256→
   257→    for item in items:
   258→        cname = fid_to_cluster.get(item.get("id", ""))
   259→        if cname:
   260→            cluster_members.setdefault(cname, []).append(item)
   261→        else:
   262→            non_cluster_items.append(item)
   263→
   264→    # Build cluster meta-items
   265→    result: list[dict] = list(non_cluster_items)
   266→    for cname, members in cluster_members.items():
   267→        # Don't collapse singletons — show them as individual findings
   268→        if len(members) < 2:
   269→            result.extend(members)
   270→            continue
   271→        cluster_data = clusters.get(cname, {})
   272→        detector = members[0].get("detector", "") if members else ""
   273→        action = cluster_data.get("action") or ""
   274→        # Derive action_type from the actual cluster action, not just the detector
   275→        if "desloppify fix" in action:
   276→            action_type = "auto_fix"
   277→        elif "desloppify move" in action:
   278→            action_type = "reorganize"
   279→        else:
   280→            action_type = _action_type_for_detector(detector)
   281→            # If detector says auto_fix but cluster has no fix command, it's really refactor
   282→            if action_type == "auto_fix" and "desloppify fix" not in action:
   283→                action_type = "refactor"
   284→
   285→        # Use stored description but patch the count if it differs from visible members
   286→        stored_desc = cluster_data.get("description") or ""
   287→        total_in_cluster = len(cluster_data.get("finding_ids", []))
   288→        if stored_desc and total_in_cluster != len(members):
   289→            # Replace the stored count with the visible count
   290→            summary = stored_desc.replace(str(total_in_cluster), str(len(members)))
   291→        else:
   292→            summary = stored_desc or f"{len(members)} findings"
   293→
   294→        primary_command = cluster_data.get("action")
   295→        if not primary_command:
   296→            primary_command = f"desloppify next --cluster {cname} --count 10"
   297→
   298→        meta_item: dict = {
   299→            "id": cname,
   300→            "kind": "cluster",
   301→            "action_type": action_type,
   302→            "summary": summary,
   303→            "members": members,
   304→            "member_count": len(members),
   305→            "primary_command": primary_command,
   306→            "cluster_name": cname,
   307→            "cluster_auto": True,
   308→            "confidence": "high",
   309→            "detector": detector,
   310→            "file": "",
   311→        }
   312→        result.append(meta_item)
   313→
   314→    result.sort(key=item_sort_key)
   315→    return result
   316→
   317→
   318→def build_work_queue(
   319→    state: StateModel,
   320→    *,
   321→    options: QueueBuildOptions | None = None,
   322→) -> WorkQueueResult:
   323→    """Build ranked queue items + tier metadata."""
   324→    resolved_options = options or QueueBuildOptions()
   325→
   326→    status = resolved_options.status
   327→    if status not in ALL_STATUSES:
   328→        raise ValueError(f"Unsupported status filter: {status}")
   329→    try:
   330→        subjective_threshold_value = float(resolved_options.subjective_threshold)
   331→    except (TypeError, ValueError):
   332→        subjective_threshold_value = 100.0
   333→    subjective_threshold_value = max(0.0, min(100.0, subjective_threshold_value))
   334→
   335→    finding_items = build_finding_items(
   336→        state,
   337→        scan_path=resolved_options.scan_path,
   338→        status_filter=status,
   339→        scope=resolved_options.scope,
   340→        chronic=resolved_options.chronic,
   341→    )
   342→
   343→    all_items = list(finding_items)
   344→    has_objective_backlog = bool(finding_items)
   345→    suppressed_count = 0
   346→    if (
   347→        resolved_options.include_subjective
   348→        and status in {"open", "all"}
   349→        and not resolved_options.chronic
   350→    ):
   351→        subjective_items = build_subjective_items(
   352→            state,
   353→            state.get("findings", {}),
   354→            threshold=subjective_threshold_value,
   355→        )
   356→        for item in subjective_items:
   357→            if not scope_matches(item, resolved_options.scope):
   358→                continue
   359→            # Suppress subjective items whose only action is a review rerun
   360→            # (--force-review-rerun) while objective backlog exists — the
   361→            # review preflight blocks reruns until the backlog drains.
   362→            if has_objective_backlog and item.get("backlog_gated"):
   363→                suppressed_count += 1
   364→                continue
   365→            all_items.append(item)
   366→
   367→    # Inject synthesis::pending synthetic item when plan requires it
   368→    if resolved_options.plan and status in {"open", "all"}:
   369→        synth_item = build_synthesis_item(resolved_options.plan, state)
   370→        if synth_item is not None:
   371→            all_items.append(synth_item)
   372→
   373→    all_items.sort(key=item_sort_key)
   374→
   375→    # Apply living plan ordering if provided
   376→    new_ids: set[str] = set()
   377→    if resolved_options.plan:
   378→        new_ids = _new_item_ids(state)
   379→        all_items = _apply_plan_order(
   380→            all_items,
   381→            resolved_options.plan,
   382→            include_skipped=resolved_options.include_skipped,
   383→            cluster=resolved_options.cluster,
   384→            new_ids=new_ids,
   385→        )
   386→
   387→    # Collapse auto-clusters into meta-items (unless drilling into a cluster)
   388→    should_collapse = (
   389→        resolved_options.collapse_clusters
   390→        and resolved_options.plan
   391→        and not resolved_options.cluster
   392→        and not resolved_options.plan.get("active_cluster")
   393→    )
   394→    if should_collapse:
   395→        all_items = _collapse_clusters(all_items, resolved_options.plan)
   396→
   397→    should_interleave = (
   398→        resolved_options.include_subjective
   399→        and status in {"open", "all"}
   400→        and not resolved_options.chronic
   401→        and resolved_options.tier is None
   402→        and not resolved_options.scope
   403→        and not resolved_options.cluster
   404→    )
   405→    if should_interleave:
   406→        all_items = _apply_subjective_interleave_guardrail(all_items)
   407→
   408→    counts = tier_counts(all_items)
   409→
   410→    requested_tier = (
   411→        int(resolved_options.tier) if resolved_options.tier is not None else None
   412→    )
   413→    selected_tier = requested_tier
   414→    fallback_reason = None
   415→    filtered = all_items
   416→
   417→    if requested_tier is not None:
   418→        filtered = [
   419→            item
   420→            for item in all_items
   421→            if _item_matches_tier(item, requested_tier)
   422→        ]
   423→        if not filtered and not resolved_options.no_tier_fallback:
   424→            chosen = choose_fallback_tier(requested_tier, counts)
   425→            if chosen is not None:
   426→                selected_tier = chosen
   427→                filtered = [
   428→                    item
   429→                    for item in all_items
   430→                    if _item_matches_tier(item, chosen)
   431→                ]
   432→                fallback_reason = (
   433→                    f"Requested T{requested_tier} has 0 open -> showing T{chosen} "
   434→                    "(nearest non-empty)."
   435→                )
   436→        elif not filtered:
   437→            fallback_reason = f"Requested T{requested_tier} has 0 open."
   438→
   439→    total = len(filtered)
   440→    if resolved_options.count is not None and resolved_options.count > 0:
   441→        filtered = filtered[: resolved_options.count]
   442→
   443→    if resolved_options.explain:
   444→        for item in filtered:
   445→            item["explain"] = item_explain(item)
   446→
   447→    available_tiers = [tier for tier, value in counts.items() if value > 0]
   448→    return {
   449→        "items": filtered,
   450→        "total": total,
   451→        "tier_counts": counts,
   452→        "requested_tier": requested_tier,
   453→        "selected_tier": selected_tier,
   454→        "fallback_reason": fallback_reason,
   455→        "available_tiers": available_tiers,
   456→        "grouped": group_queue_items(filtered, "item"),
   457→        "new_ids": new_ids,
   458→        "suppressed_count": suppressed_count,
   459→    }
   460→
   461→
   462→__all__ = [
   463→    "ATTEST_EXAMPLE",
   464→    "QueueBuildOptions",
   465→    "WorkQueueResult",
   466→    "build_work_queue",
   467→    "group_queue_items",
   468→]
   469→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py"
}
```

> TOOL

tool_result Read
```
1→"""Helper utilities for work queue item construction."""
     2→
     3→from __future__ import annotations
     4→
     5→import re
     6→from fnmatch import fnmatch
     7→
     8→from desloppify.core.enums import finding_status_tokens
     9→from desloppify.core.registry import DETECTORS
    10→from desloppify.engine.planning.scorecard_projection import (
    11→    scorecard_subjective_entries,
    12→)
    13→from desloppify.intelligence.integrity import (
    14→    is_holistic_subjective_finding,
    15→    unassessed_subjective_dimensions,
    16→)
    17→from desloppify.scoring import DISPLAY_NAMES
    18→
    19→ALL_STATUSES = set(finding_status_tokens(include_all=True))
    20→ATTEST_EXAMPLE = (
    21→    "I have actually [DESCRIBE THE CONCRETE CHANGE YOU MADE] "
    22→    "and I am not gaming the score by resolving without fixing."
    23→)
    24→
    25→
    26→def detail_dict(item: dict) -> dict:
    27→    """Return finding detail as a dict; tolerate legacy/non-dict payloads."""
    28→    detail = item.get("detail")
    29→    return detail if isinstance(detail, dict) else {}
    30→
    31→
    32→def status_matches(item_status: str, status_filter: str) -> bool:
    33→    return status_filter == "all" or item_status == status_filter
    34→
    35→
    36→def is_subjective_finding(item: dict) -> bool:
    37→    detector = item.get("detector")
    38→    if detector in {"subjective_assessment"}:
    39→        return True
    40→    if detector == "holistic_review":
    41→        return True
    42→    return False
    43→
    44→
    45→def is_review_finding(item: dict) -> bool:
    46→    return item.get("detector") == "review"
    47→
    48→
    49→def review_finding_weight(item: dict) -> float:
    50→    """Return review issue weight aligned with issues list ordering."""
    51→    confidence = str(item.get("confidence", "low")).lower()
    52→    weight_by_confidence = {
    53→        "high": 1.0,
    54→        "medium": 0.7,
    55→        "low": 0.3,
    56→    }
    57→    weight = weight_by_confidence.get(confidence, 0.3)
    58→    if detail_dict(item).get("holistic"):
    59→        weight *= 10.0
    60→    return float(weight)
    61→
    62→
    63→def scope_matches(item: dict, scope: str | None) -> bool:
    64→    """Apply show-style pattern matching against a queue item."""
    65→    if not scope:
    66→        return True
    67→
    68→    item_id = item.get("id", "")
    69→    detector = item.get("detector", "")
    70→    filepath = item.get("file", "")
    71→    summary = item.get("summary", "")
    72→    dimension = detail_dict(item).get("dimension_name", "")
    73→    kind = item.get("kind", "")
    74→
    75→    if "*" in scope:
    76→        return any(
    77→            fnmatch(candidate, scope)
    78→            for candidate in (item_id, filepath, detector, dimension, summary)
    79→        )
    80→
    81→    if "::" in scope:
    82→        return item_id.startswith(scope)
    83→
    84→    lowered = scope.lower()
    85→    if kind == "subjective_dimension":
    86→        return (
    87→            lowered in item_id.lower()
    88→            or lowered in dimension.lower()
    89→            or lowered in summary.lower()
    90→        )
    91→
    92→    # Hash suffix: 8+ hex chars matches the tail segment of a finding ID.
    93→    if len(lowered) >= 8 and re.fullmatch(r"[0-9a-f]+", lowered):
    94→        return item_id.lower().endswith("::" + lowered)
    95→
    96→    return (
    97→        detector == scope
    98→        or filepath == scope
    99→        or filepath.startswith(scope.rstrip("/") + "/")
   100→    )
   101→
   102→
   103→def slugify(text: str) -> str:
   104→    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")
   105→
   106→
   107→def _canonical_subjective_dimension_key(display_name: str) -> str:
   108→    """Map a display label (e.g. 'Mid elegance') to its canonical dimension key."""
   109→    cleaned = display_name.replace(" (subjective)", "").strip()
   110→    target = cleaned.lower()
   111→
   112→    for dim_key, label in DISPLAY_NAMES.items():
   113→        if str(label).lower() == target:
   114→            return str(dim_key)
   115→    return slugify(cleaned)
   116→
   117→
   118→def _subjective_dimension_aliases(display_name: str) -> set[str]:
   119→    """Return normalized aliases used to match display labels with finding dimension keys."""
   120→    cleaned = display_name.replace(" (subjective)", "").strip()
   121→    canonical = _canonical_subjective_dimension_key(cleaned)
   122→    return {
   123→        cleaned.lower(),
   124→        cleaned.replace(" ", "_").lower(),
   125→        slugify(cleaned),
   126→        canonical.lower(),
   127→        slugify(canonical),
   128→    }
   129→
   130→
   131→def supported_fixers_for_item(state: dict, item: dict) -> set[str] | None:
   132→    """Return supported fixers for an item's language when known."""
   133→    lang = str(item.get("lang", "") or "").strip()
   134→    if not lang:
   135→        return None
   136→
   137→    caps = state.get("lang_capabilities", {})
   138→    if not isinstance(caps, dict):
   139→        return None
   140→
   141→    lang_caps = caps.get(lang, {})
   142→    if not isinstance(lang_caps, dict):
   143→        return None
   144→
   145→    fixers = lang_caps.get("fixers")
   146→    if not isinstance(fixers, list):
   147→        return None
   148→    return {fixer for fixer in fixers if isinstance(fixer, str)}
   149→
   150→
   151→def primary_command_for_finding(
   152→    item: dict, *, supported_fixers: set[str] | None = None
   153→) -> str:
   154→    detector = item.get("detector", "")
   155→    meta = DETECTORS.get(detector)
   156→    if meta and meta.action_type == "auto_fix" and meta.fixers:
   157→        available_fixers = [
   158→            fixer
   159→            for fixer in meta.fixers
   160→            if supported_fixers is not None and fixer in supported_fixers
   161→        ]
   162→        if available_fixers:
   163→            return f"desloppify fix {available_fixers[0]} --dry-run"
   164→    if detector == "subjective_review":
   165→        if is_holistic_subjective_finding(item):
   166→            return "desloppify review --prepare"
   167→        return "desloppify show subjective"
   168→    return f'desloppify plan done "{item.get("id", "")}" --note "<what you did>" --confirm'
   169→
   170→
   171→def build_synthesis_item(plan: dict, state: dict) -> dict | None:
   172→    """Build a synthetic T1 work item for ``synthesis::pending`` if it's in the queue.
   173→
   174→    Returns ``None`` when synthesis is not pending.
   175→    """
   176→    from desloppify.engine._plan.stale_dimensions import SYNTHESIS_ID
   177→
   178→    if SYNTHESIS_ID not in plan.get("queue_order", []):
   179→        return None
   180→
   181→    findings = state.get("findings", {})
   182→    meta = plan.get("epic_synthesis_meta", {})
   183→
   184→    open_review_ids = {
   185→        fid for fid, f in findings.items()
   186→        if f.get("status") == "open"
   187→        and f.get("detector") in ("review", "concerns")
   188→    }
   189→    synthesized_ids = set(meta.get("synthesized_ids", []))
   190→    new_since = len(open_review_ids - synthesized_ids)
   191→    resolved_since = len(synthesized_ids - open_review_ids)
   192→
   193→    return {
   194→        "id": SYNTHESIS_ID,
   195→        "tier": 1,
   196→        "confidence": "high",
   197→        "detector": "synthesis",
   198→        "file": ".",
   199→        "kind": "synthesis_needed",
   200→        "primary_command": "desloppify plan synthesize",
   201→        "summary": (
   202→            f"Synthesize {len(open_review_ids)} review findings into a coherent plan"
   203→        ),
   204→        "detail": {
   205→            "total_review_findings": len(open_review_ids),
   206→            "new_since_last": new_since,
   207→            "resolved_since_last": resolved_since,
   208→        },
   209→    }
   210→
   211→
   212→def subjective_strict_scores(state: dict) -> dict[str, float]:
   213→    dim_scores = state.get("dimension_scores", {}) or {}
   214→    if not dim_scores:
   215→        return {}
   216→
   217→    entries = scorecard_subjective_entries(state, dim_scores=dim_scores)
   218→    scores: dict[str, float] = {}
   219→    for entry in entries:
   220→        name = str(entry.get("name", "")).strip()
   221→        if not name:
   222→            continue
   223→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
   224→        [REDACTED](name)
   225→        aliases = _subjective_dimension_aliases(name)
   226→        for cli_key in entry.get("cli_keys", []):
   227→            key = str(cli_key).strip().lower()
   228→            if not key:
   229→                continue
   230→            aliases.add(key)
   231→            aliases.add(slugify(key))
   232→        aliases.add(dim_key.lower())
   233→        aliases.add(slugify(dim_key))
   234→        for alias in aliases:
   235→            scores[alias] = strict_val
   236→    return scores
   237→
   238→
   239→def build_subjective_items(
   240→    state: dict, findings: dict, *, threshold: float = 100.0
   241→) -> list[dict]:
   242→    """Create synthetic subjective work items (always tier 4)."""
   243→    dim_scores = state.get("dimension_scores", {}) or {}
   244→    if not dim_scores:
   245→        return []
   246→    threshold = max(0.0, min(100.0, float(threshold)))
   247→
   248→    subjective_entries = scorecard_subjective_entries(state, dim_scores=dim_scores)
   249→    if not subjective_entries:
   250→        return []
   251→    unassessed_dims = {
   252→        str(name).strip()
   253→        for name in unassessed_subjective_dimensions(
   254→            dim_scores
   255→        )
   256→    }
   257→
   258→    # Review findings are keyed by raw dimension name (snake_case).
   259→    review_open_by_dim: dict[str, int] = {}
   260→    for finding in findings.values():
   261→        if finding.get("status") != "open" or finding.get("detector") != "review":
   262→            continue
   263→        dim_key = str(detail_dict(finding).get("dimension", "")).strip().lower()
   264→        if not dim_key:
   265→            continue
   266→        review_open_by_dim[dim_key] = review_open_by_dim.get(dim_key, 0) + 1
   267→
   268→    items: list[dict] = []
   269→    def _prepare_command(
   270→        cli_keys: list[str],
   271→        *,
   272→        force_review_rerun: bool = False,
   273→    ) -> str:
   274→        command = "desloppify review --prepare"
   275→        if cli_keys:
   276→            command += " --dimensions " + ",".join(cli_keys)
   277→        if force_review_rerun:
   278→            command += " --force-review-rerun"
   279→        return command
   280→
   281→    for entry in subjective_entries:
   282→        name = str(entry.get("name", "")).strip()
   283→        if not name:
   284→            continue
   285→        strict_val = float(entry.get("strict", entry.get("score", 100.0)))
   286→        if strict_val >= threshold:
   287→            continue
   288→
   289→        [REDACTED](name)
   290→        aliases = set(_subjective_dimension_aliases(name))
   291→        cli_keys = [
   292→            str(key).strip().lower()
   293→            for key in entry.get("cli_keys", [])
   294→            if str(key).strip()
   295→        ]
   296→        aliases.update(cli_keys)
   297→        aliases.update(slugify(key) for key in cli_keys)
   298→        open_review = sum(review_open_by_dim.get(alias, 0) for alias in aliases)
   299→        is_unassessed = bool(entry.get("placeholder")) or (
   300→            name in unassessed_dims
   301→            or (strict_val <= 0.0 and int(entry.get("issues", 0)) == 0)
   302→        )
   303→        is_stale = bool(entry.get("stale"))
   304→        # Items whose only action is --force-review-rerun are gated by the
   305→        # review preflight while objective backlog exists.  Flag them so the
   306→        # queue builder can suppress them until the backlog drains.
   307→        is_backlog_gated = open_review == 0 and not is_unassessed
   308→        # If review findings already exist for this dimension, triage/fix them
   309→        # before suggesting another review refresh pass.
   310→        if open_review > 0:
   311→            primary_command = "desloppify show review --status open"
   312→        elif is_unassessed:
   313→            primary_command = _prepare_command(cli_keys)
   314→        elif is_stale:
   315→            primary_command = _prepare_command(
   316→                cli_keys,
   317→                force_review_rerun=True,
   318→            )
   319→        elif cli_keys:
   320→            primary_command = _prepare_command(
   321→                cli_keys,
   322→                force_review_rerun=True,
   323→            )
   324→        else:
   325→            primary_command = _prepare_command(
   326→                cli_keys,
   327→                force_review_rerun=True,
   328→            )
   329→        stale_tag = " [stale — re-review]" if is_stale else ""
   330→        summary = f"Subjective dimension below target: {name} ({strict_val:.1f}%){stale_tag}"
   331→        items.append(
   332→            {
   333→                "id": f"subjective::{slugify(dim_key)}",
   334→                "detector": "subjective_assessment",
   335→                "file": ".",
   336→                "tier": 4,
   337→                "effective_tier": 4,
   338→                "confidence": "medium",
   339→                "summary": summary,
   340→                "detail": {
   341→                    "dimension_name": name,
   342→                    "dimension": dim_key,
   343→                    "issues": int(entry.get("issues", 0)),
   344→                    "strict_score": strict_val,
   345→                    "open_review_findings": open_review,
   346→                    "cli_keys": cli_keys,
   347→                },
   348→                "status": "open",
   349→                "kind": "subjective_dimension",
   350→                "primary_command": primary_command,
   351→                "backlog_gated": is_backlog_gated,
   352→            }
   353→        )
   354→    return items
   355→
   356→
   357→__all__ = [
   358→    "ALL_STATUSES",
   359→    "ATTEST_EXAMPLE",
   360→    "build_subjective_items",
   361→    "build_synthesis_item",
   362→    "detail_dict",
   363→    "is_review_finding",
   364→    "is_subjective_finding",
   365→    "primary_command_for_finding",
   366→    "review_finding_weight",
   367→    "scope_matches",
   368→    "slugify",
   369→    "status_matches",
   370→    "subjective_strict_scores",
   371→    "supported_fixers_for_item",
   372→]
   373→
```

> AGENT

Now let me also check for any other files that reference tier-based sorting or filtering — particularly the plan and state filtering files mentioned in the git status:

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|sort.*tier|tier.*sort|T1.*T2|tier.*filter|filter.*tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "files_with_matches",
  "type": "py"
}
```

> TOOL

tool_result Grep
```
Found 24 files
desloppify/app/commands/status_parts/render.py
desloppify/app/commands/next_parts/render.py
desloppify/tests/review/test_work_queue.py
desloppify/tests/plan/test_auto_cluster.py
desloppify/tests/commands/test_queue_progress.py
desloppify/engine/_work_queue/helpers.py
desloppify/engine/_work_queue/core.py
desloppify/app/commands/show/render.py
desloppify/app/commands/plan/queue_render.py
desloppify/app/commands/next_parts/output.py
desloppify/app/commands/helpers/queue_progress.py
desloppify/tests/core/test_plan.py
desloppify/tests/commands/test_cmd_next.py
desloppify/engine/planning/render.py
desloppify/engine/_work_queue/ranking.py
desloppify/engine/_state/scoring.py
desloppify/app/commands/show/payload.py
desloppify/tests/review/integration/test_work_queue.py
desloppify/tests/commands/test_cmd_status.py
desloppify/app/commands/scan/scan_reporting_text.py
desloppify/tests/commands/test_direct_coverage_split_modules.py
desloppify/intelligence/narrative/phase.py
desloppify/tests/core/test_narrative.py
desloppify/engine/work_queue.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|item_sort_key",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "type": "py",
  "glob": "**/_plan/*.py"
}
```

> TOOL

tool_result Grep
```
No matches found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|is_subjective.*tier|tier.*4|tier.*forced|forced.*tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/filtering.py",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
No matches found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|item_sort_key|tier.*sort|sort.*tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
205:        tier = int(item.get("effective_tier", item.get("tier", 3)))
435:    tier = int(item.get("effective_tier", item.get("tier", 3)))
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py",
  "offset": 195,
  "limit": 60
}
```

> TOOL

tool_result Read
```
195→            scan_path=scan_path,
   196→            status="open",
   197→            include_subjective=True,
   198→            subjective_threshold=subjective_threshold,
   199→            no_tier_fallback=True,
   200→        ),
   201→    )
   202→    open_items = queue.get("items", [])
   203→    by_tier_file: dict[int, dict[str, list]] = defaultdict(lambda: defaultdict(list))
   204→    for item in open_items:
   205→        tier = int(item.get("effective_tier", item.get("tier", 3)))
   206→        by_tier_file[tier][item.get("file", ".")].append(item)
   207→
   208→    lines: list[str] = []
   209→    for tier_num in [1, 2, 3, 4]:
   210→        tier_files = by_tier_file.get(tier_num, {})
   211→        if not tier_files:
   212→            continue
   213→
   214→        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
   215→        tier_count = sum(len(file_findings) for file_findings in tier_files.values())
   216→        lines.extend(
   217→            [
   218→                "---",
   219→                f"## Tier {tier_num}: {label} ({tier_count} open)",
   220→                "",
   221→            ]
   222→        )
   223→
   224→        sorted_files = sorted(
   225→            tier_files.items(), key=lambda item: (-len(item[1]), item[0])
   226→        )
   227→        for filepath, file_items in sorted_files:
   228→            display_path = "Codebase-wide" if filepath == "." else filepath
   229→            lines.append(f"### `{display_path}` ({len(file_items)} findings)")
   230→            lines.append("")
   231→            for item in file_items:
   232→                if item.get("kind") == "subjective_dimension":
   233→                    lines.append(f"- [ ] [subjective] {item.get('summary', '')}")
   234→                    lines.append(f"      `{item.get('id', '')}`")
   235→                    if item.get("primary_command"):
   236→                        lines.append(f"      action: `{item['primary_command']}`")
   237→                    continue
   238→
   239→                conf_badge = f"[{item.get('confidence', 'medium')}]"
   240→                lines.append(f"- [ ] {conf_badge} {item.get('summary', '')}")
   241→                lines.append(f"      `{item.get('id', '')}`")
   242→            lines.append("")
   243→
   244→    return lines
   245→
   246→
   247→def _tier_summary_lines(stats: dict) -> list[str]:
   248→    lines: list[str] = []
   249→    by_tier = stats.get("by_tier", {})
   250→    for tier_num in [1, 2, 3, 4]:
   251→        tier_stats = by_tier.get(str(tier_num), {})
   252→        open_count = tier_stats.get("open", 0)
   253→        total = sum(tier_stats.values())
   254→        addressed = total - open_count
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|item_sort_key",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
26:    tiers = {int(m.get("effective_tier", m.get("tier", 3))) for m in members}
130:            tier_val = int(item.get("effective_tier", item.get("tier", 3)))
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py",
  "offset": 1,
  "limit": 160
}
```

> TOOL

tool_result Read
```
1→"""Compact queue table renderer for ``plan queue``."""
     2→
     3→from __future__ import annotations
     4→
     5→import argparse
     6→
     7→from desloppify.app.commands.helpers.guardrails import print_synthesis_guardrail_info
     8→from desloppify.app.commands.helpers.runtime import command_runtime
     9→from desloppify.app.commands.helpers.state import require_completed_scan
    10→from desloppify.core.output_api import colorize, print_table
    11→from desloppify.engine.plan import compute_new_finding_ids, load_plan
    12→from desloppify.engine.work_queue import QueueBuildOptions, build_work_queue
    13→
    14→
    15→def _truncate(text: str, width: int) -> str:
    16→    if len(text) <= width:
    17→        return text
    18→    return text[: width - 1] + "\u2026"
    19→
    20→
    21→def _cluster_tier_label(item: dict) -> str:
    22→    """Compute a tier label from cluster members, e.g. 'T2' or 'T1-T3'."""
    23→    members = item.get("members", [])
    24→    if not members:
    25→        return ""
    26→    tiers = {int(m.get("effective_tier", m.get("tier", 3))) for m in members}
    27→    lo, hi = min(tiers), max(tiers)
    28→    if lo == hi:
    29→        return f"T{lo}"
    30→    return f"T{lo}-T{hi}"
    31→
    32→
    33→def _resolve_plan_context(plan: dict, cluster_filter: str | None) -> tuple[dict | None, str | None]:
    34→    plan_data: dict | None = None
    35→    if plan.get("queue_order") or plan.get("overrides") or plan.get("clusters"):
    36→        plan_data = plan
    37→
    38→    effective_cluster = cluster_filter
    39→    if plan_data and not cluster_filter:
    40→        active_cluster = plan_data.get("active_cluster")
    41→        if active_cluster:
    42→            effective_cluster = active_cluster
    43→    return plan_data, effective_cluster
    44→
    45→
    46→def _print_queue_header(
    47→    *,
    48→    items: list[dict],
    49→    tier_counts: dict,
    50→    include_skipped: bool,
    51→    plan: dict,
    52→    plan_data: dict | None,
    53→    new_count: int = 0,
    54→) -> None:
    55→    from desloppify.app.commands.helpers.queue_progress import (
    56→        QueueBreakdown,
    57→        format_queue_headline,
    58→    )
    59→
    60→    total = len(items)
    61→    skipped_count = sum(1 for it in items if it.get("plan_skipped"))
    62→    non_skipped = total - skipped_count
    63→    plan_skipped_total = len(plan.get("skipped", {})) if plan_data else 0
    64→
    65→    # Count subjective items in the visible list
    66→    subjective = sum(
    67→        1 for it in items if it.get("kind") == "subjective_dimension"
    68→    )
    69→
    70→    # Count plan-ordered items (minus skipped)
    71→    plan_ordered = 0
    72→    if plan_data:
    73→        queue_order = plan_data.get("queue_order", [])
    74→        skipped_ids = set(plan_data.get("skipped", {}).keys())
    75→        plan_ordered = sum(1 for fid in queue_order if fid not in skipped_ids)
    76→
    77→    breakdown = QueueBreakdown(
    78→        queue_total=non_skipped,
    79→        plan_ordered=plan_ordered,
    80→        skipped=plan_skipped_total,
    81→        subjective=subjective,
    82→        tier_counts=dict(tier_counts),
    83→    )
    84→    headline = format_queue_headline(breakdown)
    85→    new_suffix = f"  ({new_count} new this scan)" if new_count > 0 else ""
    86→    print(colorize(f"\n  {headline}{new_suffix}", "bold"))
    87→
    88→    focus = plan.get("active_cluster") if plan_data else None
    89→    if focus:
    90→        print(colorize(f"  Focus: {focus}", "cyan"))
    91→
    92→    if include_skipped or skipped_count != 0:
    93→        return
    94→    if not plan_skipped_total:
    95→        return
    96→    print(
    97→        colorize(
    98→            f"  ({plan_skipped_total} skipped item{'s' if plan_skipped_total != 1 else ''}"
    99→            " hidden — use --include-skipped)",
   100→            "dim",
   101→        )
   102→    )
   103→
   104→
   105→def _queue_display_items(items: list[dict], *, top: int) -> list[dict]:
   106→    if top > 0 and len(items) > top:
   107→        return items[:top]
   108→    return items
   109→
   110→
   111→def _build_rows(display_items: list[dict], new_ids: set[str] | None = None) -> list[list[str]]:
   112→    rows: list[list[str]] = []
   113→    _new = new_ids or set()
   114→    for idx, item in enumerate(display_items, 1):
   115→        pos = str(idx)
   116→        kind = item.get("kind", "finding")
   117→
   118→        if kind == "cluster":
   119→            tier_str = _cluster_tier_label(item)
   120→            member_count = item.get("member_count", 0)
   121→            detector = item.get("detector", "cluster")
   122→            new_in_cluster = sum(
   123→                1 for m in item.get("members", [])
   124→                if m.get("id") in _new
   125→            )
   126→            new_tag = f" (+{new_in_cluster} new)" if new_in_cluster else ""
   127→            summary = f"[{member_count} items{new_tag}] {item.get('summary', '')}"
   128→            cluster_name = item.get("cluster_name", item.get("id", ""))
   129→        else:
   130→            tier_val = int(item.get("effective_tier", item.get("tier", 3)))
   131→            tier_str = f"T{tier_val}"
   132→            detector = item.get("detector", "")
   133→            summary = item.get("summary", "")
   134→            plan_cluster = item.get("plan_cluster")
   135→            cluster_name = plan_cluster.get("name", "") if isinstance(plan_cluster, dict) else ""
   136→
   137→        prefix = "* " if item.get("id") in _new else ""
   138→        suffix = " [skip]" if item.get("plan_skipped") else ""
   139→        summary_display = _truncate(prefix + summary, 48) + suffix
   140→        rows.append([pos, tier_str, detector, summary_display, cluster_name])
   141→    return rows
   142→
   143→
   144→def cmd_plan_queue(args: argparse.Namespace) -> None:
   145→    """Render a compact table of all upcoming queue items."""
   146→    runtime = command_runtime(args)
   147→    state = runtime.state
   148→    if not require_completed_scan(state):
   149→        return
   150→
   151→    top = getattr(args, "top", 30)
   152→    tier_filter = getattr(args, "tier", None)
   153→    cluster_filter = getattr(args, "cluster", None)
   154→    include_skipped = bool(getattr(args, "include_skipped", False))
   155→
   156→    plan = load_plan()
   157→    print_synthesis_guardrail_info(plan=plan, state=state)
   158→    plan_data, effective_cluster = _resolve_plan_context(plan, cluster_filter)
   159→
   160→    queue = build_work_queue(
```

> AGENT

Now I have a thorough picture of all the tier enforcement points. Here is a complete analysis:

---

## Tier-Based Queue Ordering: Where and How It Is Enforced

There are four distinct mechanisms that together enforce "T1 before T2 before T3, and subjective forced to T4":

---

### 1. `effective_tier` assignment — `ranking.py` lines 54–57

**File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py`

```python
# Lines 54–57 in build_finding_items()
item["effective_tier"] = (
    4 if item["is_subjective"] else int(finding.get("tier", 3))
)
```

This is where subjective findings get **forcibly promoted to T4**, regardless of whatever `tier` is stored on the finding. Non-subjective items use the stored `tier` value.

Additionally, in `helpers.py` lines 337–338, all synthetic subjective dimension items are always hard-coded with:

```python
# helpers.py lines 337–338 in build_subjective_items()
"tier": 4,
"effective_tier": 4,
```

---

### 2. Primary sort key — `ranking.py` `item_sort_key()` lines 86–122

**File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py`

This is the central sorting function applied at `core.py` line 373 (`all_items.sort(key=item_sort_key)`). The tier is the **first element** of every sort tuple, making it the primary and dominant ordering control:

```python
# Lines 86–122 — item_sort_key()
def item_sort_key(item: dict) -> tuple:
    if item.get("kind") == "synthesis_needed":
        # Synthesis items always sort first — they block all other work.
        return (-1, 0, 0, item.get("id", ""))

    if item.get("kind") == "cluster":
        # Clusters sort before individual findings (priority bucket 0)
        return (0, action_pri, -member_count, item.get("id", ""))

    if item.get("kind") == "subjective_dimension" or item.get("is_subjective"):
        return (
            int(item.get("effective_tier", 4)),  # always 4
            1,  # secondary: subjective after mechanical within T4
            subjective_score_value(item),
            item.get("id", ""),
        )

    # Mechanical findings
    return (
        int(item.get("effective_tier", item.get("tier", 3))),  # T1 < T2 < T3 < T4
        0,
        CONFIDENCE_ORDER.get(item.get("confidence", "low"), 9),
        -review_weight,
        -count,
        item.get("id", ""),
    )
```

The ordering enforced here:
- **synthesis_needed** items: bucket `-1` (always first)
- **clusters**: bucket `0` (before individual findings)
- **mechanical findings**: primary key is `effective_tier` (T1 < T2 < T3)
- **subjective findings**: always bucket `4`, with secondary key `1` so they sort *after* mechanical items that happen to be T4

Within mechanical findings, secondary keys are: `confidence` rank, then `review_weight` desc, then `count` desc, then `id`.

---

### 3. Tier filtering — `core.py` lines 417–437

**File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

```python
# Lines 417–437 — tier filter in build_work_queue()
if requested_tier is not None:
    filtered = [
        item
        for item in all_items
        if _item_matches_tier(item, requested_tier)
    ]
    if not filtered and not resolved_options.no_tier_fallback:
        chosen = choose_fallback_tier(requested_tier, counts)
        if chosen is not None:
            selected_tier = chosen
            filtered = [
                item
                for item in all_items
                if _item_matches_tier(item, chosen)
            ]
            fallback_reason = (
                f"Requested T{requested_tier} has 0 open -> showing T{chosen} "
                "(nearest non-empty)."
            )
    elif not filtered:
        fallback_reason = f"Requested T{requested_tier} has 0 open."
```

When a caller passes `--tier N`, this filter retains only items whose `effective_tier == N`. The fallback logic (`choose_fallback_tier`) finds the numerically nearest non-empty tier, which implements "T1 before T2" staircase behavior when a tier is empty.

---

### 4. Subjective interleave guardrail — `core.py` lines 66–98 and 397–406

**File:** `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

After the main sort (which puts all mechanical items before all subjective items), a second pass can re-interleave them to prevent starvation:

```python
# Lines 66–98 — _apply_subjective_interleave_guardrail()
def _apply_subjective_interleave_guardrail(items, *, objective_burst=3, subjective_burst=1):
    subjective_items = deque(item for item in items if _is_subjective_queue_item(item))
    objective_items = deque(item for item in items if not _is_subjective_queue_item(item))
    if not subjective_items or not objective_items:
        return items

    interleaved = []
    while objective_items and subjective_items:
        for _ in range(objective_burst):   # emit 3 objective items
            interleaved.append(objective_items.popleft())
        for _ in range(subjective_burst):  # then 1 subjective item
            interleaved.append(subjective_items.popleft())
    # drain remainders
    interleaved.extend(objective_items)
    interleaved.extend(subjective_items)
    return interleaved
```

The guardrail is **only applied** (lines 397–406) when:
- `include_subjective=True`
- `status` is `open` or `all`
- `chronic=False`
- `tier` is `None` (no explicit tier requested)
- `scope` is `None`
- `cluster` is `None`

So: with no tier filter, subjective items are interleaved 1-per-3-mechanical. With an explicit `--tier`, the interleave is bypassed entirely (the tier filter already gates what is returned).

---

### Summary of the Control Points to Remove

To eliminate tier as a hard queue-order control, these are the exact code points to touch:

| Mechanism | File | Lines | What It Does |
|---|---|---|---|
| Force subjective to T4 | `ranking.py` | 54–57 | `effective_tier = 4 if is_subjective` |
| Hard-code subjective items at T4 | `helpers.py` | 337–338 | `"tier": 4, "effective_tier": 4` |
| Sort tuple uses tier as primary key | `ranking.py` | 86–122 (`item_sort_key`) | T1 < T2 < T3 < T4 as tuple position 0 |
| Tier filter in `build_work_queue` | `core.py` | 417–437 | Gates output to requested tier |
| Subjective interleave (secondary) | `core.py` | 66–98, 397–406 | 3-objective : 1-subjective interleave, bypassed when tier filter is active |
| `effective_tier` read in `_item_matches_tier` | `core.py` | 211–218 | Used by the tier filter |
| Cluster sort uses tier bucket `0` | `ranking.py` | 91–103 | Clusters precede all findings regardless of tier |
| `tier_counts()` grouping | `ranking.py` | 177–188 | Counting display only |

> DEVELOPER

Search the entire desloppify codebase very thoroughly for ALL references to tier-based queue ordering. I need to find every place that:

1. References `effective_tier` (field name, variable, dict key)
2. References `tier` as a queue ordering concept (not the data field on findings themselves - those can stay as metadata)
3. References `tier_counts` or `available_tiers` or `selected_tier` or `requested_tier` or `fallback_tier`
4. References `--tier` CLI argument
5. References `no_tier_fallback`
6. References `choose_fallback_tier`
7. References `_item_matches_tier`
8. Text/strings mentioning "T1", "T2", "T3", "T4" in the context of queue ordering or priority
9. References to "tier asc" or "tier fixed" in ranking factor strings
10. The `group == "tier"` branch in `group_queue_items`
11. Any test files that test tier-based behavior

Search in:
- All .py files under desloppify/
- All test files
- CLI parser files (parser_groups*.py)
- Command files (next.py, show/, status/, plan/)
- Rendering/output files

For each match, provide the file path, line number, and the relevant code snippet with a few lines of context. Be very thorough - check templates, help strings, docstrings, comments, everything.

> AGENT

I'll conduct a thorough search across the entire codebase for all tier-based queue ordering references. Let me run many searches in parallel.

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (120.6KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01CdinosEBrrZfaUfFvXBn4s.txt

Preview (first 2KB):
desloppify/engine/_work_queue/helpers.py-334-                "detector": "subjective_assessment",
desloppify/engine/_work_queue/helpers.py-335-                "file": ".",
desloppify/engine/_work_queue/helpers.py-336-                "tier": 4,
desloppify/engine/_work_queue/helpers.py:337:                "effective_tier": 4,
desloppify/engine/_work_queue/helpers.py-338-                "confidence": "medium",
desloppify/engine/_work_queue/helpers.py-339-                "summary": summary,
desloppify/engine/_work_queue/helpers.py-340-                "detail": {
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-52-        item["kind"] = "finding"
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-53-        item["is_review"] = is_review_finding(item)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-54-        item["is_subjective"] = is_subjective_finding(item)
desloppify/engine/_work_queue/ranking.py:55:        item["effective_tier"] = (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-56-            4 if item["is_subjective"] else int(finding.get("tier", 3))
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-57-        )
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-58-        item["review_weight"] = (
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-104-
desloppify/engine/_work_queue/ranking.py-105-    if item.get("kind") == "subjective_dimension" or item.get("is_subjective"):
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-106-        return (
desloppify/engine/_work_queue/ranking.py:107:            int(item.get("effective_tier", 4)),
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-108-            1,  # Subjective items sort after mechanical items within T4.
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier_counts",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (90.5KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01Sk1VucAmftDMDpvpScLrni.txt

Preview (first 2KB):
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-48-    subjective_score_value,
.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py:49:    tier_counts,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-50-)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-51-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-52-__all__ = [
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-74-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-75-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-76-    "subjective_score_value",
.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py:77:    "tier_counts",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-78-    # issues
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-79-    "expire_stale_holistic",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-80-    "impact_label",
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-48-    subjective_score_value,
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "available_tiers",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (60KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_013YU6bS1AEFjmJ4N3ti78V8.txt

Preview (first 2KB):
desloppify/engine/_work_queue/core.py-53-    requested_tier: int | None
desloppify/engine/_work_queue/core.py-54-    selected_tier: int | None
desloppify/engine/_work_queue/core.py-55-    fallback_reason: str | None
desloppify/engine/_work_queue/core.py:56:    available_tiers: list[int]
desloppify/engine/_work_queue/core.py-57-    grouped: dict[str, list[dict]]
desloppify/engine/_work_queue/core.py-58-    suppressed_count: int
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-59-
--
desloppify/engine/_work_queue/core.py-444-        for item in filtered:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-445-            item["explain"] = item_explain(item)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-446-
desloppify/engine/_work_queue/core.py:447:    available_tiers = [tier for tier, value in counts.items() if value > 0]
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-448-    return {
desloppify/engine/_work_queue/core.py-449-        "items": filtered,
desloppify/engine/_work_queue/core.py-450-        "total": total,
--
desloppify/engine/_work_queue/core.py-452-        "requested_tier": requested_tier,
desloppify/engine/_work_queue/core.py-453-        "selected_tier": selected_tier,
desloppify/engine/_work_queue/core.py-454-        "fallback_reason": fallback_reason,
desloppify/engine/_work_queue/core.py:455:        "available_tiers": available_tiers,
desloppify/engine/_work_queue/core.py-456-        "grouped": group_queue_items(filtered, "item"),
desloppify/engine/_work_queue/core.py-457-        "new_ids": new_ids,
desloppify/engine/_work_queue/core.py-458-        "suppressed_count": suppressed_count,
--
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-53-    requested_tier: int | None
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-54-    selected_tier: int | None
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "selected_tier",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (56KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01N39z4HKuGcbXgERK5KWT2J.txt

Preview (first 2KB):
desloppify/engine/_work_queue/core.py-51-    total: int
desloppify/engine/_work_queue/core.py-52-    tier_counts: dict[int, int]
desloppify/engine/_work_queue/core.py-53-    requested_tier: int | None
desloppify/engine/_work_queue/core.py:54:    selected_tier: int | None
desloppify/engine/_work_queue/core.py-55-    fallback_reason: str | None
desloppify/engine/_work_queue/core.py-56-    available_tiers: list[int]
desloppify/engine/_work_queue/core.py-57-    grouped: dict[str, list[dict]]
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-410-    requested_tier = (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-411-        int(resolved_options.tier) if resolved_options.tier is not None else None
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-412-    )
desloppify/engine/_work_queue/core.py:413:    selected_tier = requested_tier
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-414-    fallback_reason = None
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-415-    filtered = all_items
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-416-
--
desloppify/engine/_work_queue/core.py-423-        if not filtered and not resolved_options.no_tier_fallback:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-424-            chosen = choose_fallback_tier(requested_tier, counts)
desloppify/engine/_work_queue/core.py-425-            if chosen is not None:
desloppify/engine/_work_queue/core.py:426:                selected_tier = chosen
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-427-                filtered = [
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-428-                    item
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-429-                    for item in all_items
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "requested_tier",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (66.5KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01RoMj9os46wsEKiAbsrbqu5.txt

Preview (first 2KB):
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-188-    return counts
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-189-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-190-
desloppify/engine/_work_queue/ranking.py:191:def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-192-    available = [tier for tier, count in counts.items() if count > 0]
desloppify/engine/_work_queue/ranking.py-193-    if not available:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-194-        return None
desloppify/engine/_work_queue/ranking.py:195:    return min(available, key=lambda tier: (abs(tier - requested_tier), tier))
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-196-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-197-
desloppify/engine/_work_queue/ranking.py-198-def group_queue_items(items: list[dict], group: str) -> dict[str, list[dict]]:
--
desloppify/engine/_work_queue/core.py-50-    items: list[dict]
desloppify/engine/_work_queue/core.py-51-    total: int
desloppify/engine/_work_queue/core.py-52-    tier_counts: dict[int, int]
desloppify/engine/_work_queue/core.py:53:    requested_tier: int | None
desloppify/engine/_work_queue/core.py-54-    selected_tier: int | None
desloppify/engine/_work_queue/core.py-55-    fallback_reason: str | None
desloppify/engine/_work_queue/core.py-56-    available_tiers: list[int]
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-407-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-408-    counts = tier_counts(all_items)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-409-
desloppify/engine/_work_queue/core.py:410:    requested_tier = (
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "fallback_tier",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-42-# --- ranking: sort keys, tier counts, grouping -----------------------------
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-43-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-44-    build_finding_items,
.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py:45:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-48-    subjective_score_value,
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-70-    "supported_fixers_for_item",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-71-    # ranking
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-72-    "build_finding_items",
.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py:73:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-74-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-75-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-76-    "subjective_score_value",
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-188-    return counts
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-189-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-190-
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py:191:def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-192-    available = [tier for tier, count in counts.items() if count > 0]
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-193-    if not available:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-194-        return None
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-216-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-217-__all__ = [
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-218-    "build_finding_items",
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py:219:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-220-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-221-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-222-    "tier_counts",
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-15-)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-16-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-17-    build_finding_items,
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:18:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-19-    group_queue_items,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-20-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-21-    item_sort_key,
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-387-            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-388-        ]
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-389-        if not filtered and not resolved_options.no_tier_fallback:
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:390:            chosen = choose_fallback_tier(requested_tier, counts)
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-391-            if chosen is not None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-392-                selected_tier = chosen
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-393-                filtered = [
--
desloppify/engine/work_queue.py-42-# --- ranking: sort keys, tier counts, grouping -----------------------------
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-43-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-44-    build_finding_items,
desloppify/engine/work_queue.py:45:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-48-    subjective_score_value,
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-70-    "supported_fixers_for_item",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-71-    # ranking
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-72-    "build_finding_items",
desloppify/engine/work_queue.py:73:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-74-    "item_explain",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-75-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-76-    "subjective_score_value",
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-188-    return counts
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-189-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-190-
desloppify/engine/_work_queue/ranking.py:191:def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-192-    available = [tier for tier, count in counts.items() if count > 0]
desloppify/engine/_work_queue/ranking.py-193-    if not available:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-194-        return None
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-216-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-217-__all__ = [
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-218-    "build_finding_items",
desloppify/engine/_work_queue/ranking.py:219:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-220-    "item_explain",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-221-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-222-    "tier_counts",
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-15-)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-16-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-17-    build_finding_items,
desloppify/engine/_work_queue/core.py:18:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-19-    group_queue_items,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-20-    item_explain,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-21-    item_sort_key,
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-421-            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-422-        ]
desloppify/engine/_work_queue/core.py-423-        if not filtered and not resolved_options.no_tier_fallback:
desloppify/engine/_work_queue/core.py:424:            chosen = choose_fallback_tier(requested_tier, counts)
desloppify/engine/_work_queue/core.py-425-            if chosen is not None:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-426-                selected_tier = chosen
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-427-                filtered = [
--
.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-42-# --- ranking: sort keys, tier counts, grouping -----------------------------
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-43-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-44-    build_finding_items,
.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py:45:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-48-    subjective_score_value,
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-70-    "supported_fixers_for_item",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-71-    # ranking
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-72-    "build_finding_items",
.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py:73:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-74-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-75-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-76-    "subjective_score_value",
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-188-    return counts
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-189-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-190-
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py:191:def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-192-    available = [tier for tier, count in counts.items() if count > 0]
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-193-    if not available:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-194-        return None
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-216-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-217-__all__ = [
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-218-    "build_finding_items",
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py:219:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-220-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-221-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-222-    "tier_counts",
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-15-)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-16-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-17-    build_finding_items,
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py:18:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-19-    group_queue_items,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-20-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-21-    item_sort_key,
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-387-            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-388-        ]
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-389-        if not filtered and not resolved_options.no_tier_fallback:
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py:390:            chosen = choose_fallback_tier(requested_tier, counts)
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-391-            if chosen is not None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-392-                selected_tier = chosen
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-393-                filtered = [
```

> TOOL

tool_use Grep
```json
{
  "pattern": "no_tier_fallback",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (47.5KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01CfrBVXtJNUraPfcpj5U2iU.txt

Preview (first 2KB):
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-36-    include_subjective: bool = True
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-37-    subjective_threshold: float = 100.0
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-38-    chronic: bool = False
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:39:    no_tier_fallback: bool = False
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-40-    explain: bool = False
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-41-    plan: dict | None = None
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-42-    include_skipped: bool = False
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-386-            for item in all_items
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-387-            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-388-        ]
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:389:        if not filtered and not resolved_options.no_tier_fallback:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-390-            chosen = choose_fallback_tier(requested_tier, counts)
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-391-            if chosen is not None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-392-                selected_tier = chosen
--
desloppify/engine/_work_queue/core.py-36-    include_subjective: bool = True
desloppify/engine/_work_queue/core.py-37-    subjective_threshold: float = 100.0
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "choose_fallback_tier",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-42-# --- ranking: sort keys, tier counts, grouping -----------------------------
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-43-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-44-    build_finding_items,
.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py:45:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-48-    subjective_score_value,
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-70-    "supported_fixers_for_item",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-71-    # ranking
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-72-    "build_finding_items",
.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py:73:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-74-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-75-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/work_queue.py-76-    "subjective_score_value",
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-188-    return counts
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-189-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-190-
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py:191:def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-192-    available = [tier for tier, count in counts.items() if count > 0]
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-193-    if not available:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-194-        return None
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-216-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-217-__all__ = [
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-218-    "build_finding_items",
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py:219:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-220-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-221-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/ranking.py-222-    "tier_counts",
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-15-)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-16-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-17-    build_finding_items,
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:18:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-19-    group_queue_items,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-20-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-21-    item_sort_key,
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-387-            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-388-        ]
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-389-        if not filtered and not resolved_options.no_tier_fallback:
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:390:            chosen = choose_fallback_tier(requested_tier, counts)
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-391-            if chosen is not None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-392-                selected_tier = chosen
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-393-                filtered = [
--
desloppify/engine/work_queue.py-42-# --- ranking: sort keys, tier counts, grouping -----------------------------
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-43-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-44-    build_finding_items,
desloppify/engine/work_queue.py:45:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-48-    subjective_score_value,
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-70-    "supported_fixers_for_item",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-71-    # ranking
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-72-    "build_finding_items",
desloppify/engine/work_queue.py:73:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-74-    "item_explain",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-75-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-76-    "subjective_score_value",
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-188-    return counts
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-189-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-190-
desloppify/engine/_work_queue/ranking.py:191:def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-192-    available = [tier for tier, count in counts.items() if count > 0]
desloppify/engine/_work_queue/ranking.py-193-    if not available:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-194-        return None
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-216-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-217-__all__ = [
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-218-    "build_finding_items",
desloppify/engine/_work_queue/ranking.py:219:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-220-    "item_explain",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-221-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-222-    "tier_counts",
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-15-)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-16-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-17-    build_finding_items,
desloppify/engine/_work_queue/core.py:18:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-19-    group_queue_items,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-20-    item_explain,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-21-    item_sort_key,
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-421-            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-422-        ]
desloppify/engine/_work_queue/core.py-423-        if not filtered and not resolved_options.no_tier_fallback:
desloppify/engine/_work_queue/core.py:424:            chosen = choose_fallback_tier(requested_tier, counts)
desloppify/engine/_work_queue/core.py-425-            if chosen is not None:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-426-                selected_tier = chosen
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-427-                filtered = [
--
.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-42-# --- ranking: sort keys, tier counts, grouping -----------------------------
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-43-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-44-    build_finding_items,
.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py:45:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-48-    subjective_score_value,
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-70-    "supported_fixers_for_item",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-71-    # ranking
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-72-    "build_finding_items",
.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py:73:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-74-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-75-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/work_queue.py-76-    "subjective_score_value",
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-188-    return counts
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-189-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-190-
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py:191:def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-192-    available = [tier for tier, count in counts.items() if count > 0]
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-193-    if not available:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-194-        return None
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-216-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-217-__all__ = [
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-218-    "build_finding_items",
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py:219:    "choose_fallback_tier",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-220-    "item_explain",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-221-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/ranking.py-222-    "tier_counts",
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-15-)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-16-from desloppify.engine._work_queue.ranking import (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-17-    build_finding_items,
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py:18:    choose_fallback_tier,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-19-    group_queue_items,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-20-    item_explain,
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-21-    item_sort_key,
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-387-            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-388-        ]
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-389-        if not filtered and not resolved_options.no_tier_fallback:
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py:390:            chosen = choose_fallback_tier(requested_tier, counts)
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-391-            if chosen is not None:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-392-                selected_tier = chosen
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-393-                filtered = [
```

> TOOL

tool_use Grep
```json
{
  "pattern": "_item_matches_tier",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-208-    return result
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-209-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-210-
desloppify/engine/_work_queue/core.py:211:def _item_matches_tier(item: dict, tier: int) -> bool:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-212-    """Check if an item (or any of its members for clusters) matches a tier."""
desloppify/engine/_work_queue/core.py-213-    if item.get("kind") == "cluster":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-214-        return any(
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-418-        filtered = [
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-419-            item
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-420-            for item in all_items
desloppify/engine/_work_queue/core.py:421:            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-422-        ]
desloppify/engine/_work_queue/core.py-423-        if not filtered and not resolved_options.no_tier_fallback:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-424-            chosen = choose_fallback_tier(requested_tier, counts)
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-427-                filtered = [
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-428-                    item
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-429-                    for item in all_items
desloppify/engine/_work_queue/core.py:430:                    if _item_matches_tier(item, chosen)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-431-                ]
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-432-                fallback_reason = (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-433-                    f"Requested T{requested_tier} has 0 open -> showing T{chosen} "
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-186-    return result
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-187-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-188-
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:189:def _item_matches_tier(item: dict, tier: int) -> bool:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-190-    """Check if an item (or any of its members for clusters) matches a tier."""
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-191-    if item.get("kind") == "cluster":
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-192-        return any(
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-384-        filtered = [
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-385-            item
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-386-            for item in all_items
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:387:            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-388-        ]
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-389-        if not filtered and not resolved_options.no_tier_fallback:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-390-            chosen = choose_fallback_tier(requested_tier, counts)
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-393-                filtered = [
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-394-                    item
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-395-                    for item in all_items
.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py:396:                    if _item_matches_tier(item, chosen)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-397-                ]
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-398-                fallback_reason = (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-ae188610/desloppify/engine/_work_queue/core.py-399-                    f"Requested T{requested_tier} has 0 open -> showing T{chosen} "
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-186-    return result
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-187-
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-188-
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py:189:def _item_matches_tier(item: dict, tier: int) -> bool:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-190-    """Check if an item (or any of its members for clusters) matches a tier."""
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-191-    if item.get("kind") == "cluster":
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-192-        return any(
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-384-        filtered = [
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-385-            item
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-386-            for item in all_items
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py:387:            if _item_matches_tier(item, requested_tier)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-388-        ]
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-389-        if not filtered and not resolved_options.no_tier_fallback:
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-390-            chosen = choose_fallback_tier(requested_tier, counts)
--
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-393-                filtered = [
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-394-                    item
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-395-                    for item in all_items
.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py:396:                    if _item_matches_tier(item, chosen)
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-397-                ]
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-398-                fallback_reason = (
/Users/user_c042661f/Documents/desloppify/.claude/worktrees/agent-af7e2384/desloppify/engine/_work_queue/core.py-399-                    f"Requested T{requested_tier} has 0 open -> showing T{chosen} "
```

> TOOL

tool_use Grep
```json
{
  "pattern": "--tier",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (29.1KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01HNGbeGzgGYxYtTmNWGhonU.txt

Preview (first 2KB):
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-58-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-59-    print(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-60-        colorize(
desloppify/app/commands/next_parts/render.py:61:            "    Switch: `desloppify next --tier 1` | `desloppify next --tier 2` | "
desloppify/app/commands/next_parts/render.py:62:            "`desloppify next --tier 3` | `desloppify next --tier 4`",
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-63-            "dim",
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-64-        )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-65-    )
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-405-        available = queue.get("available_tiers", [])
desloppify/app/commands/next_parts/render.py-406-        if available:
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-407-            commands = " | ".join(
desloppify/app/commands/next_parts/render.py:408:                f"desloppify next --tier {tier_num}" for tier_num in available
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-409-            )
desloppify/app/commands/next_parts/render.py-410-            print(colorize(f"  Try: {commands}", "dim"))
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-411-    return True
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups_admin.py-505-    # plan queue
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups_admin.py-506-    p_queue = plan_sub.add_parser("queue", help="Compact table of upcoming queue items")
...
</persisted-output>
```

> AGENT

Good, the initial searches returned lots of data including worktree copies. Let me now focus specifically on the `desloppify/` directory (excluding `.claude/worktrees/`) and run the remaining searches.

> TOOL

tool_use Grep
```json
{
  "pattern": "\\\"tier asc\\\"|\\\"tier fixed\\\"|tier_asc|tier_fixed",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-134-                "Subjective dimensions are always queued as T4 and do not outrank "
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-135-                "mechanical T1/T2/T3 items."
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-136-            ),
desloppify/engine/_work_queue/ranking.py:137:            "ranking_factors": ["tier asc", "subjective_score asc", "id asc"],
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-138-        }
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-139-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-140-    detail = detail_dict(item)
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-146-        ranking_factors = ["tier fixed to T4", "subjective_score asc", "id asc"]
desloppify/engine/_work_queue/ranking.py-147-    elif is_review:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-148-        ranking_factors = [
desloppify/engine/_work_queue/ranking.py:149:            "tier asc",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-150-            "confidence asc",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-151-            "review_weight desc",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-152-            "count desc",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-153-            "id asc",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-154-        ]
desloppify/engine/_work_queue/ranking.py-155-    else:
desloppify/engine/_work_queue/ranking.py:156:        ranking_factors = ["tier asc", "confidence asc", "count desc", "id asc"]
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-157-    explain = {
desloppify/engine/_work_queue/ranking.py-158-        "kind": "finding",
desloppify/engine/_work_queue/ranking.py-159-        "effective_tier": effective_tier,
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/test_work_queue.py-236-    item = queue["items"][0]
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/test_work_queue.py-237-    assert "explain" in item
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/test_work_queue.py-238-    assert item["explain"]["ranking_factors"] == [
desloppify/tests/review/test_work_queue.py:239:        "tier asc",
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/test_work_queue.py-240-        "confidence asc",
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/test_work_queue.py-241-        "count desc",
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/test_work_queue.py-242-        "id asc",
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/integration/test_work_queue.py-260-    item = queue["items"][0]
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/integration/test_work_queue.py-261-    assert "explain" in item
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/integration/test_work_queue.py-262-    assert item["explain"]["ranking_factors"] == [
desloppify/tests/review/integration/test_work_queue.py:263:        "tier asc",
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/integration/test_work_queue.py-264-        "confidence asc",
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/integration/test_work_queue.py-265-        "count desc",
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/integration/test_work_queue.py-266-        "id asc",
```

> TOOL

tool_use Grep
```json
{
  "pattern": "group\\s*==\\s*[\"\\']tier[\"\\']",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 5,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
desloppify/engine/_work_queue/ranking.py-201-    for item in items:
desloppify/engine/_work_queue/ranking.py-202-        if group == "file":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-203-            key = item.get("file", "")
desloppify/engine/_work_queue/ranking.py-204-        elif group == "detector":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-205-            key = item.get("detector", "")
desloppify/engine/_work_queue/ranking.py:206:        elif group == "tier":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-207-            key = f"T{int(item.get('effective_tier', item.get('tier', 3)))}"
desloppify/engine/_work_queue/ranking.py-208-        elif group == "cluster":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-209-            plan_cluster = item.get("plan_cluster")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-210-            key = plan_cluster["name"] if isinstance(plan_cluster, dict) else "(unclustered)"
desloppify/engine/_work_queue/ranking.py-211-        else:
```

> TOOL

tool_use Grep
```json
{
  "pattern": "[\"\\\"]T[1234][\"\\\"]|[\"\\']T[1234][\"\\']|\\bT[1-4]\\b",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 2,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (33.3KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_015am2bsXbTxGc7egqr7K6CH.txt

Preview (first 2KB):
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py-170-
desloppify/engine/_work_queue/helpers.py-171-def build_synthesis_item(plan: dict, state: dict) -> dict | None:
desloppify/engine/_work_queue/helpers.py:172:    """Build a synthetic T1 work item for ``synthesis::pending`` if it's in the queue.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py-173-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py-174-    Returns ``None`` when synthesis is not pending.
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-106-        return (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-107-            int(item.get("effective_tier", 4)),
desloppify/engine/_work_queue/ranking.py:108:            1,  # Subjective items sort after mechanical items within T4.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-109-            subjective_score_value(item),
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-110-            item.get("id", ""),
--
desloppify/engine/_work_queue/ranking.py-132-            "subjective_score": subjective_score_value(item),
desloppify/engine/_work_queue/ranking.py-133-            "policy": (
desloppify/engine/_work_queue/ranking.py:134:                "Subjective dimensions are always queued as T4 and do not outrank "
desloppify/engine/_work_queue/ranking.py:135:                "mechanical T1/T2/T3 items."
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-136-            ),
desloppify/engine/_work_queue/ranking.py-137-            "ranking_factors": ["tier asc", "subjective_score asc", "id asc"],
--
desloppify/engine/_work_queue/ranking.py-144-    ranking_factors: list[str]
desloppify/engine/_work_queue/ranking.py-145-    if is_subjective:
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier_counts",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (37.9KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01YD2nz8Xw6QPbBBmPyt38xX.txt

Preview (first 2KB):
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-46-    item_explain,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-47-    item_sort_key,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-48-    subjective_score_value,
desloppify/engine/work_queue.py:49:    tier_counts,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-50-)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-51-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-52-__all__ = [
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-74-    "item_explain",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-75-    "item_sort_key",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-76-    "subjective_score_value",
desloppify/engine/work_queue.py:77:    "tier_counts",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-78-    # issues
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-79-    "expire_stale_holistic",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py-80-    "impact_label",
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-174-    return explain
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-175-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-176-
desloppify/engine/_work_queue/ranking.py:177:def tier_counts(items: list[dict]) -> dict[int, int]:
desloppify/engine/_work_queue/ranking.py-178-    counts = {1: 0, 2: 0, 3: 0, 4: 0}
desloppify/engine/_work_queue/ranking.py-179-    for item in items:
desloppify/engine/_work_queue/ranking.py-180-        if item.get("kind") == "cluster":
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-219-    "choose_fallback_tier",
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (36KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01MyfPQgvogz5Y9CTk8byf3B.txt

Preview (first 2KB):
desloppify/engine/_work_queue/helpers.py-334-                "detector": "subjective_assessment",
desloppify/engine/_work_queue/helpers.py-335-                "file": ".",
desloppify/engine/_work_queue/helpers.py-336-                "tier": 4,
desloppify/engine/_work_queue/helpers.py:337:                "effective_tier": 4,
desloppify/engine/_work_queue/helpers.py-338-                "confidence": "medium",
desloppify/engine/_work_queue/helpers.py-339-                "summary": summary,
desloppify/engine/_work_queue/helpers.py-340-                "detail": {
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-52-        item["kind"] = "finding"
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-53-        item["is_review"] = is_review_finding(item)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-54-        item["is_subjective"] = is_subjective_finding(item)
desloppify/engine/_work_queue/ranking.py:55:        item["effective_tier"] = (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-56-            4 if item["is_subjective"] else int(finding.get("tier", 3))
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-57-        )
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-58-        item["review_weight"] = (
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-104-
desloppify/engine/_work_queue/ranking.py-105-    if item.get("kind") == "subjective_dimension" or item.get("is_subjective"):
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-106-        return (
desloppify/engine/_work_queue/ranking.py:107:            int(item.get("effective_tier", 4)),
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-108-            1,  # Subjective items sort after mechanical items within T4.
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "--tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-148-        assert args.count == 1
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-149-
desloppify/tests/commands/test_cli.py-150-    def test_next_with_tier_and_count(self, parser):
desloppify/tests/commands/test_cli.py:151:        args = parser.parse_args(["next", "--tier", "2", "--count", "5"])
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-152-        assert args.tier == 2
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-153-        assert args.count == 5
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-154-
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-173-
desloppify/tests/commands/test_cli.py-174-    def test_next_with_explain_and_no_tier_fallback(self, parser):
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-175-        args = parser.parse_args(
desloppify/tests/commands/test_cli.py:176:            ["next", "--tier", "4", "--explain", "--no-tier-fallback"]
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-177-        )
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-178-        assert args.tier == 4
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py-179-        assert args.explain is True
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-116-        cmd_next(_args())
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-117-        out = capsys.readouterr().out
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-118-        assert "Tier Navigator" in out
desloppify/tests/commands/test_cmd_next.py:119:        assert "desloppify next --tier 1" in out
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-120-        assert "Nothing to do" in out
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-121-        assert written[0]["command"] == "next"
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-122-        assert written[0]["items"] == []
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-205-        out = capsys.readouterr().out
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-206-        assert "Requested T4 has 0 open." in out
desloppify/tests/commands/test_cmd_next.py-207-        assert "Requested tier: T4" in out
desloppify/tests/commands/test_cmd_next.py:208:        assert "Try: desloppify next --tier 1 | desloppify next --tier 2" in out
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-209-        assert written[0]["queue"]["available_tiers"] == [1, 2]
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py-210-
desloppify/tests/commands/test_cmd_next.py-211-    def test_subjective_focus_and_review_prepare_hint(self, monkeypatch, capsys):
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-58-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-59-    print(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-60-        colorize(
desloppify/app/commands/next_parts/render.py:61:            "    Switch: `desloppify next --tier 1` | `desloppify next --tier 2` | "
desloppify/app/commands/next_parts/render.py:62:            "`desloppify next --tier 3` | `desloppify next --tier 4`",
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-63-            "dim",
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-64-        )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-65-    )
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-405-        available = queue.get("available_tiers", [])
desloppify/app/commands/next_parts/render.py-406-        if available:
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-407-            commands = " | ".join(
desloppify/app/commands/next_parts/render.py:408:                f"desloppify next --tier {tier_num}" for tier_num in available
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-409-            )
desloppify/app/commands/next_parts/render.py-410-            print(colorize(f"  Try: {commands}", "dim"))
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py-411-    return True
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups_admin.py-505-    # plan queue
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups_admin.py-506-    p_queue = plan_sub.add_parser("queue", help="Compact table of upcoming queue items")
desloppify/app/cli_support/parser_groups_admin.py-507-    p_queue.add_argument("--top", type=int, default=30, help="Max items (default: 30, 0=all)")
desloppify/app/cli_support/parser_groups_admin.py:508:    p_queue.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=None,
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups_admin.py-509-                         help="Show only items in this tier (T1=critical .. T4=cosmetic)")
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups_admin.py-510-    p_queue.add_argument("--cluster", type=str, default=None, metavar="NAME",
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups_admin.py-511-                         help="Filter to a specific cluster")
--
desloppify/app/cli_support/parser_groups.py-210-examples:
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-211-  desloppify next                       # single highest-priority item
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-212-  desloppify next --count 10            # top 10 items
desloppify/app/cli_support/parser_groups.py:213:  desloppify next --tier 1              # only tier 1
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-214-  desloppify next --group file          # group by file
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-215-  desloppify next --cluster my-cluster  # items in a cluster""",
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-216-        formatter_class=argparse.RawDescriptionHelpFormatter,
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-217-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-218-    p_next.add_argument("--state", type=str, default=None, help="Path to state file")
desloppify/app/cli_support/parser_groups.py:219:    p_next.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=None, help="Show only this tier")
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-220-    p_next.add_argument(
desloppify/app/cli_support/parser_groups.py-221-        "--count", type=int, default=1, help="Number of items to show (default: 1)"
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-222-    )
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-252-    p_next.add_argument(
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-253-        "--no-tier-fallback",
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-254-        action="store_true",
desloppify/app/cli_support/parser_groups.py:255:        help="Do not auto-fallback to another tier when --tier has no items",
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-256-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-257-    p_next.add_argument(
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-258-        "--cluster",
```

> AGENT

Good. Now let me read the key files in full to get complete context, and also search for the remaining patterns.

> TOOL

tool_use Grep
```json
{
  "pattern": "Tier Navigator|tier_label|tier_header|tier_badge|tier_bar|tier_line|Tier\\s+\\d|\"Tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
<persisted-output>
Output too large (20.7KB). Full output saved to: /Users/user_c042661f/.claude/projects/-Users-user_c042661f-Documents-desloppify/abe6f5cb-f2a9-4cad-8e97-56ab1f1dbd2d/tool-results/toolu_01NJr87XdLv8umCfpJQkwo6f.txt

Preview (first 2KB):
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_scoring/detection.py-56-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_scoring/detection.py-57-
desloppify/engine/_scoring/detection.py-58-def _file_count_cap(findings_in_file: int) -> float:
desloppify/engine/_scoring/detection.py:59:    """Tiered cap for non-LOC file-based detectors.
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_scoring/detection.py-60-
desloppify/engine/_scoring/detection.py-61-    Keeps file-count denominator semantics while preserving concentration signal:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_scoring/detection.py-62-    1-2 findings => _FILE_CAP_LOW, 3-5 => _FILE_CAP_MID, 6+ => _FILE_CAP_HIGH.
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema.py-14-    "ConcernDismissal",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema.py-15-    "FindingStatus",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema.py-16-    "Finding",
desloppify/engine/_state/schema.py:17:    "TierStats",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema.py-18-    "StateStats",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema.py-19-    "DimensionScore",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema.py-20-    "ScanHistoryEntry",
--
desloppify/engine/planning/render.py-211-        if not tier_files:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-212-            continue
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-213-
desloppify/engine/planning/render.py:214:        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-215-        tier_count = sum(len(file_findings) for file_findings in tier_files.values())
...
</persisted-output>
```

> TOOL

tool_use Grep
```json
{
  "pattern": "\\.tier\\b|get\\([\"\\']tier[\"\\']|get\\(\"tier\"\\)|tier_num|\\[\"tier\"\\]|\\['tier'\\]",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-53-        item["is_review"] = is_review_finding(item)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-54-        item["is_subjective"] = is_subjective_finding(item)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-55-        item["effective_tier"] = (
desloppify/engine/_work_queue/ranking.py:56:            4 if item["is_subjective"] else int(finding.get("tier", 3))
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-57-        )
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-58-        item["review_weight"] = (
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-59-            review_finding_weight(item) if item["is_review"] else None
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-113-    detail = detail_dict(item)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-114-    review_weight = float(item.get("review_weight", 0.0) or 0.0)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-115-    return (
desloppify/engine/_work_queue/ranking.py:116:        int(item.get("effective_tier", item.get("tier", 3))),
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-117-        0,
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-118-        CONFIDENCE_ORDER.get(item.get("confidence", "low"), 9),
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-119-        -review_weight,
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-123-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-124-
desloppify/engine/_work_queue/ranking.py-125-def item_explain(item: dict) -> dict:
desloppify/engine/_work_queue/ranking.py:126:    effective_tier = int(item.get("effective_tier", item.get("tier", 3)))
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-127-
desloppify/engine/_work_queue/ranking.py-128-    if item.get("kind") == "subjective_dimension":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-129-        return {
--
desloppify/engine/_work_queue/ranking.py-180-        if item.get("kind") == "cluster":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-181-            # Count each member at its own tier
desloppify/engine/_work_queue/ranking.py-182-            for member in item.get("members", []):
desloppify/engine/_work_queue/ranking.py:183:                tier = int(member.get("effective_tier", member.get("tier", 3)))
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-184-                counts[tier] = counts.get(tier, 0) + 1
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-185-            continue
desloppify/engine/_work_queue/ranking.py:186:        tier = int(item.get("effective_tier", item.get("tier", 3)))
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-187-        counts[tier] = counts.get(tier, 0) + 1
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-188-    return counts
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-189-
--
desloppify/engine/_work_queue/ranking.py-204-        elif group == "detector":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-205-            key = item.get("detector", "")
desloppify/engine/_work_queue/ranking.py-206-        elif group == "tier":
desloppify/engine/_work_queue/ranking.py:207:            key = f"T{int(item.get('effective_tier', item.get('tier', 3)))}"
desloppify/engine/_work_queue/ranking.py-208-        elif group == "cluster":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-209-            plan_cluster = item.get("plan_cluster")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py-210-            key = plan_cluster["name"] if isinstance(plan_cluster, dict) else "(unclustered)"
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-212-    """Check if an item (or any of its members for clusters) matches a tier."""
desloppify/engine/_work_queue/core.py-213-    if item.get("kind") == "cluster":
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-214-        return any(
desloppify/engine/_work_queue/core.py:215:            int(m.get("effective_tier", m.get("tier", 3))) == tier
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-216-            for m in item.get("members", [])
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-217-        )
desloppify/engine/_work_queue/core.py:218:    return int(item.get("effective_tier", item.get("tier", 3))) == tier
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-219-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-220-
desloppify/engine/_work_queue/core.py-221-def _action_type_for_detector(detector: str) -> str:
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-398-        resolved_options.include_subjective
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-399-        and status in {"open", "all"}
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-400-        and not resolved_options.chronic
desloppify/engine/_work_queue/core.py:401:        and resolved_options.tier is None
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-402-        and not resolved_options.scope
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-403-        and not resolved_options.cluster
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-404-    )
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-408-    counts = tier_counts(all_items)
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-409-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-410-    requested_tier = (
desloppify/engine/_work_queue/core.py:411:        int(resolved_options.tier) if resolved_options.tier is not None else None
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-412-    )
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-413-    selected_tier = requested_tier
/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py-414-    fallback_reason = None
```

> TOOL

tool_use Grep
```json
{
  "pattern": "\\.tier\\b|args\\.tier|options\\.tier|resolved.*\\.tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
desloppify/app/commands/status_parts/render.py-233-        checks_str = f"{checks:>7,}"
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_parts/render.py-234-        action = dimension_action_type(dim.name)
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_parts/render.py-235-        print(
desloppify/app/commands/status_parts/render.py:236:            f"  {dim.name:<22} {checks_str}  {score_val:5.1f}%  {strict_val:5.1f}%  {bar}  T{dim.tier}  {action}{focus}"
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_parts/render.py-237-        )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_parts/render.py-238-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_parts/render.py-239-
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
42-    return subjective_review_open_breakdown(findings_scoped)
43-
44-
45:def _tier_label(tier: int) -> str:
46:    return f"T{tier}"
47-
48-
49:def _render_tier_navigator(queue: dict) -> None:
50:    counts = queue.get("tier_counts", {})
51-    print(colorize("\n  Tier Navigator", "bold"))
52-    print(
53-        colorize(
--
58-    )
59-    print(
60-        colorize(
61:            "    Switch: `desloppify next --tier 1` | `desloppify next --tier 2` | "
62:            "`desloppify next --tier 3` | `desloppify next --tier 4`",
63-            "dim",
64-        )
65-    )
--
70-    for key, grouped_items in grouped.items():
71-        print(colorize(f"\n  {key} ({len(grouped_items)})", "cyan"))
72-        for item in grouped_items:
73:            tier = int(item.get("effective_tier", item.get("tier", 3)))
74-            tag = _effort_tag(item)
75-            tag_str = f" {tag}" if tag else ""
76-            print(
77:                f"    {_tier_label(tier)} [{item.get('confidence', 'medium')}]{tag_str} {item.get('summary', '')}"
78-            )
79-
80-
--
180-        print(colorize("  Complete all 4 stages (observe → reflect → organize → commit) before fixing.", "dim"))
181-        return
182-
183:    tier = int(item.get("effective_tier", item.get("tier", 3)))
184-    confidence = item.get("confidence", "medium")
185:    print(colorize(f"  (Tier {tier}, {confidence} confidence)", "bold"))
186-    print(colorize("  " + "─" * 60, "dim"))
187-    print(f"  {colorize(item.get('summary', ''), 'yellow')}")
188-
--
330-        explanation = item.get("explain", {})
331-        count_weight = explanation.get("count", int(detail.get("count", 0) or 0))
332-        base = (
333:            f"ranked by tier={tier}, confidence={confidence}, "
334-            f"count={count_weight}, id={item.get('id', '')}"
335-        )
336-
--
362-
363-
364-def render_queue_header(queue: dict, explain: bool) -> None:
365:    _render_tier_navigator(queue)
366-    if not queue.get("fallback_reason"):
367-        return
368-    print(colorize(f"  {queue['fallback_reason']}", "yellow"))
369-    if not explain:
370-        return
371:    available = queue.get("available_tiers", [])
372-    if available:
373:        tiers = ", ".join(f"T{tier_num}" for tier_num in available)
374:        print(colorize(f"  explain: available tiers are {tiers}", "dim"))
375-
376-
377-def show_empty_queue(
378-    queue: dict,
379:    tier: int | None,
380-    strict: float | None,
381-    *,
382-    plan_start_strict: float | None = None,
--
400-    else:
401-        suffix = f" Strict score: {strict:.1f}/100" if strict is not None else ""
402-        print(colorize(f"\n  Nothing to do!{suffix}", "green"))
403:    if tier is not None:
404:        print(colorize(f"  Requested tier: T{tier}", "dim"))
405:        available = queue.get("available_tiers", [])
406-        if available:
407-            commands = " | ".join(
408:                f"desloppify next --tier {tier_num}" for tier_num in available
409-            )
410-            print(colorize(f"  Try: {commands}", "dim"))
411-    return True
--
413-
414-def _render_compact_item(item: dict, idx: int, total: int) -> None:
415-    """One-line summary for cluster drill-in items after the first."""
416:    tier = int(item.get("effective_tier", item.get("tier", 3)))
417-    tag = _effort_tag(item)
418-    tag_str = f" {tag}" if tag else ""
419-    fid = item.get("id", "")
420-    short = fid.rsplit("::", 1)[-1][:8] if "::" in fid else fid
421:    print(f"  [{idx + 1}/{total}] {_tier_label(tier)}{tag_str} {item.get('summary', '')}")
422-    print(colorize(f"         {item.get('file', '')}  [{short}]", "dim"))
423-
424-
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/output.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
31-    serialized: dict[str, Any] = {
32-        "id": item.get("id"),
33-        "kind": item.get("kind", "finding"),
34:        "tier": item.get("tier"),
35:        "effective_tier": item.get("effective_tier", item.get("tier")),
36-        "confidence": item.get("confidence"),
37-        "detector": item.get("detector"),
38-        "file": item.get("file"),
--
74-    """Build JSON payload for query.json and non-terminal output modes."""
75-    serialized = [serialize_item(item) for item in items]
76-    queue_section: dict[str, Any] = {
77:        "tier_counts": queue.get("tier_counts", {}),
78:        "requested_tier": queue.get("requested_tier"),
79:        "selected_tier": queue.get("selected_tier"),
80-        "fallback_reason": queue.get("fallback_reason"),
81:        "available_tiers": queue.get("available_tiers", []),
82-        "total": queue.get("total", len(items)),
83-        "suppressed_count": queue.get("suppressed_count", 0),
84-    }
--
124-    ]
125-    for item in items:
126-        kind = item.get("kind", "finding")
127:        tier = int(item.get("effective_tier", item.get("tier", 3)))
128-        conf = item.get("confidence", "medium")
129-        summary = item.get("summary", "").replace("|", "\\|")
130-        command = (item.get("primary_command", "") or "").replace("|", "\\|")
131:        lines.append(f"| {kind} | T{tier} | {conf} | {summary} | {command} |")
132-    lines.append("")
133-    return "\n".join(lines)
134-
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
171-
172-
173-def _get_items(args, state: dict, config: dict) -> None:
174:    tier = getattr(args, "tier", None)
175-    count = getattr(args, "count", 1) or 1
176-    scope = getattr(args, "scope", None)
177-    status = getattr(args, "status", "open")
178-    group = getattr(args, "group", "item")
179-    explain = bool(getattr(args, "explain", False))
180:    no_tier_fallback = bool(getattr(args, "no_tier_fallback", False))
181-    cluster_arg = getattr(args, "cluster", None)
182-    include_skipped = bool(getattr(args, "include_skipped", False))
183-
--
203-    queue = build_work_queue(
204-        state,
205-        options=QueueBuildOptions(
206:            tier=tier,
207-            count=count,
208-            scan_path=state.get("scan_path"),
209-            scope=scope,
210-            status=status,
211-            include_subjective=True,
212-            subjective_threshold=target_strict,
213:            no_tier_fallback=no_tier_fallback,
214-            explain=explain,
215-            plan=plan_data,
216-            include_skipped=include_skipped,
--
249-    strict_score = state_mod.get_strict_score(state)
250-    if next_render_mod.show_empty_queue(
251-        queue,
252:        tier,
253-        strict_score,
254-        plan_start_strict=plan_start_strict,
255-        target_strict=target_strict,
```

> AGENT

Let me now get the remaining files I need to fully document -- the status/show/plan command files and test files.

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/scope.py-204-            status=status_filter,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/scope.py-205-            include_subjective=False,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/scope.py-206-            chronic=chronic,
desloppify/app/commands/show/scope.py:207:            no_tier_fallback=True,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/scope.py-208-        ),
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/scope.py-209-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/scope.py-210-    return [item for item in queue.get("items", []) if item.get("kind") == "finding"]
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/payload.py-25-
desloppify/app/commands/show/payload.py-26-    by_file: dict[str, list] = defaultdict(list)
desloppify/app/commands/show/payload.py-27-    by_detector: dict[str, int] = defaultdict(int)
desloppify/app/commands/show/payload.py:28:    by_tier: dict[int, int] = defaultdict(int)
desloppify/app/commands/show/payload.py-29-    for finding in matches:
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/payload.py-30-        by_file[finding["file"]].append(finding)
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/payload.py-31-        by_detector[finding["detector"]] += 1
desloppify/app/commands/show/payload.py:32:        by_tier[finding["tier"]] += 1
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/payload.py-33-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/payload.py-34-    payload = {
desloppify/app/commands/show/payload.py-35-        "query": pattern,
desloppify/app/commands/show/payload.py-36-        "status_filter": status_filter,
desloppify/app/commands/show/payload.py-37-        "total": len(matches),
desloppify/app/commands/show/payload.py-38-        "summary": {
desloppify/app/commands/show/payload.py:39:            "by_tier": {f"T{tier}": count for tier, count in sorted(by_tier.items())},
desloppify/app/commands/show/payload.py-40-            "by_detector": dict(sorted(by_detector.items(), key=lambda item: -item[1])),
desloppify/app/commands/show/payload.py-41-            "files": len(by_file),
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/payload.py-42-        },
--
desloppify/app/commands/show/payload.py-44-            fp: [
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/payload.py-45-                {
desloppify/app/commands/show/payload.py-46-                    "id": f["id"],
desloppify/app/commands/show/payload.py:47:                    "tier": f["tier"],
desloppify/app/commands/show/payload.py-48-                    "confidence": f["confidence"],
desloppify/app/commands/show/payload.py-49-                    "summary": f["summary"],
desloppify/app/commands/show/payload.py-50-                    "detail": f.get("detail", {}),
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-56-    zone = finding.get("zone", "production")
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-57-    zone_tag = colorize(f" [{zone}]", "dim") if zone != "production" else ""
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-58-    print(
desloppify/app/commands/show/render.py:59:        f"    {status_icon} T{finding['tier']} [{finding['confidence']}] {finding['summary']}{zone_tag}"
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-60-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-61-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-62-    detail_parts = format_detail(finding.get("detail", {}))
--
desloppify/app/commands/show/render.py-131-    for filepath, findings in shown_files:
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-132-        findings.sort(
desloppify/app/commands/show/render.py-133-            key=lambda finding: (
desloppify/app/commands/show/render.py:134:                finding["tier"],
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-135-                CONFIDENCE_ORDER.get(finding["confidence"], 9),
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-136-            )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-137-        )
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-158-        )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-159-
desloppify/app/commands/show/render.py-160-    by_detector: dict[str, int] = defaultdict(int)
desloppify/app/commands/show/render.py:161:    by_tier: dict[int, int] = defaultdict(int)
desloppify/app/commands/show/render.py-162-    for finding in matches:
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-163-        by_detector[finding["detector"]] += 1
desloppify/app/commands/show/render.py:164:        by_tier[finding["tier"]] += 1
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-165-
desloppify/app/commands/show/render.py-166-    print(colorize("  Summary:", "bold"))
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-167-    print(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-168-        colorize(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-169-            (
desloppify/app/commands/show/render.py:170:                "    By tier:     "
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-171-                + ", ".join(
desloppify/app/commands/show/render.py:172:                    f"T{tier}:{count}" for tier, count in sorted(by_tier.items())
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-173-                )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-174-            ),
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py-175-            "dim",
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
desloppify/app/commands/plan/queue_render.py-18-    return text[: width - 1] + "\u2026"
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-19-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-20-
desloppify/app/commands/plan/queue_render.py:21:def _cluster_tier_label(item: dict) -> str:
desloppify/app/commands/plan/queue_render.py:22:    """Compute a tier label from cluster members, e.g. 'T2' or 'T1-T3'."""
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-23-    members = item.get("members", [])
desloppify/app/commands/plan/queue_render.py-24-    if not members:
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-25-        return ""
desloppify/app/commands/plan/queue_render.py:26:    tiers = {int(m.get("effective_tier", m.get("tier", 3))) for m in members}
desloppify/app/commands/plan/queue_render.py:27:    lo, hi = min(tiers), max(tiers)
desloppify/app/commands/plan/queue_render.py-28-    if lo == hi:
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-29-        return f"T{lo}"
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-30-    return f"T{lo}-T{hi}"
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-46-def _print_queue_header(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-47-    *,
desloppify/app/commands/plan/queue_render.py-48-    items: list[dict],
desloppify/app/commands/plan/queue_render.py:49:    tier_counts: dict,
desloppify/app/commands/plan/queue_render.py-50-    include_skipped: bool,
desloppify/app/commands/plan/queue_render.py-51-    plan: dict,
desloppify/app/commands/plan/queue_render.py-52-    plan_data: dict | None,
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-79-        plan_ordered=plan_ordered,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-80-        skipped=plan_skipped_total,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-81-        subjective=subjective,
desloppify/app/commands/plan/queue_render.py:82:        tier_counts=dict(tier_counts),
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-83-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-84-    headline = format_queue_headline(breakdown)
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-85-    new_suffix = f"  ({new_count} new this scan)" if new_count > 0 else ""
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-116-        kind = item.get("kind", "finding")
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-117-
desloppify/app/commands/plan/queue_render.py-118-        if kind == "cluster":
desloppify/app/commands/plan/queue_render.py:119:            tier_str = _cluster_tier_label(item)
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-120-            member_count = item.get("member_count", 0)
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-121-            detector = item.get("detector", "cluster")
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-122-            new_in_cluster = sum(
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-127-            summary = f"[{member_count} items{new_tag}] {item.get('summary', '')}"
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-128-            cluster_name = item.get("cluster_name", item.get("id", ""))
desloppify/app/commands/plan/queue_render.py-129-        else:
desloppify/app/commands/plan/queue_render.py:130:            tier_val = int(item.get("effective_tier", item.get("tier", 3)))
desloppify/app/commands/plan/queue_render.py:131:            tier_str = f"T{tier_val}"
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-132-            detector = item.get("detector", "")
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-133-            summary = item.get("summary", "")
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-134-            plan_cluster = item.get("plan_cluster")
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-137-        prefix = "* " if item.get("id") in _new else ""
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-138-        suffix = " [skip]" if item.get("plan_skipped") else ""
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-139-        summary_display = _truncate(prefix + summary, 48) + suffix
desloppify/app/commands/plan/queue_render.py:140:        rows.append([pos, tier_str, detector, summary_display, cluster_name])
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-141-    return rows
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-142-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-143-
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-149-        return
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-150-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-151-    top = getattr(args, "top", 30)
desloppify/app/commands/plan/queue_render.py:152:    tier_filter = getattr(args, "tier", None)
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-153-    cluster_filter = getattr(args, "cluster", None)
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-154-    include_skipped = bool(getattr(args, "include_skipped", False))
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-155-
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-160-    queue = build_work_queue(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-161-        state,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-162-        options=QueueBuildOptions(
desloppify/app/commands/plan/queue_render.py:163:            tier=tier_filter,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-164-            count=None,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-165-            scan_path=state.get("scan_path"),
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-166-            status="open",
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-172-        ),
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-173-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-174-    items = queue.get("items", [])
desloppify/app/commands/plan/queue_render.py:175:    tier_counts = queue.get("tier_counts", {})
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-176-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-177-    sort_by = getattr(args, "sort", "priority")
desloppify/app/commands/plan/queue_render.py-178-    all_new_ids: set[str] = queue.get("new_ids", set())
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-187-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-188-    _print_queue_header(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-189-        items=items,
desloppify/app/commands/plan/queue_render.py:190:        tier_counts=tier_counts,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-191-        include_skipped=include_skipped,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-192-        plan=plan,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py-193-        plan_data=plan_data,
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_cmd.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
1:"""status command: score dashboard with per-tier progress."""
2-
3-from __future__ import annotations
4-
--
35-    show_review_summary,
36-    show_structural_areas,
37-    show_subjective_followup,
38:    show_tier_progress_table,
39-    write_status_query,
40-)
41-from desloppify.engine.plan import load_plan
--
91-        print(colorize(f"  {config_warning}", "yellow"))
92-
93-    scores = state_mod.score_snapshot(state)
94:    by_tier = stats.get("by_tier", {})
95-    target_strict_score = target_strict_score_from_config(config, fallback=95.0)
96-
97-    lang = resolve_lang(args)
--
161-            dim_scores=dim_scores,
162-        )
163-    else:
164:        show_tier_progress_table(by_tier)
165-
166-    if dim_scores:
167-        show_focus_suggestion(dim_scores, state, plan=_plan_active)
--
192-    write_status_query(
193-        state=state,
194-        stats=stats,
195:        by_tier=by_tier,
196-        dim_scores=dim_scores,
197-        scorecard_dims=scorecard_dims,
198-        subjective_measures=subjective_measures,
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_parts/render.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
32-from desloppify.core.output_api import colorize, print_table
33-
34-
35:def show_tier_progress_table(by_tier: dict) -> None:
36-    """Fallback display when dimension scores are unavailable."""
37-    rows = []
38:    for tier_num in [1, 2, 3, 4]:
39:        ts = by_tier.get(str(tier_num), {})
40-        t_open = ts.get("open", 0)
41-        t_fixed = ts.get("fixed", 0) + ts.get("auto_resolved", 0)
42-        t_fp = ts.get("false_positive", 0)
--
50-        )
51-        rows.append(
52-            [
53:                f"Tier {tier_num}",
54-                bar,
55-                f"{strict_pct}%",
56-                str(t_open),
--
74-    *,
75-    state: dict,
76-    stats: dict,
77:    by_tier: dict,
78-    dim_scores: dict,
79-    scorecard_dims: list[dict],
80-    subjective_measures: list[dict],
--
106-            "stats": stats,
107-            "scan_count": state.get("scan_count", 0),
108-            "last_scan": state.get("last_scan"),
109:            "by_tier": by_tier,
110-            "ignores": ignores,
111-            "suppression": suppression,
112-            "potentials": state.get("potentials"),
--
233-        checks_str = f"{checks:>7,}"
234-        action = dimension_action_type(dim.name)
235-        print(
236:            f"  {dim.name:<22} {checks_str}  {score_val:5.1f}%  {strict_val:5.1f}%  {bar}  T{dim.tier}  {action}{focus}"
237-        )
238-
239-
--
257-        name = str(entry.get("name", "Unknown"))
258-        score_val = float(entry.get("score", 0.0))
259-        strict_val = float(entry.get("strict", score_val))
260:        tier = 4
261-
262-        bar = dimension_bar(score_val, colorize_fn=colorize, bar_len=bar_len)
263-
--
282-        issue_style = "yellow" if strict_val < 95.0 and issue_count == 0 else "dim"
283-        issue_tag = colorize(f" [open issues: {issue_count}]", issue_style)
284-        print(
285:            f"  {name:<22} {checks_str}  {score_val:5.1f}%  {strict_val:5.1f}%  {bar}  T{tier}  {'review'}{focus}{stale_tag}"
286-            f"{placeholder_tag}{issue_tag}"
287-        )
288-
--
418-                    {
419-                        k: {
420-                            "score": v["score"],
421:                            "tier": v.get("tier", 3),
422-                            "detectors": v.get("detectors", {}),
423-                        }
424-                        for k, v in dim_scores.items()
--
512-    structural = [
513-        f
514-        for f in findings.values()
515:        if f["tier"] in (3, 4) and f["status"] in ("open", "wontfix")
516-    ]
517-
518-    if len(structural) < 5:
--
526-    if len(areas) < 2:
527-        return None
528-
529:    return sorted(areas.items(), key=lambda x: -sum(f["tier"] for f in x[1]))
530-
531-
532-def _build_area_rows(sorted_areas: list[tuple[str, list]], *, max_areas: int = 15) -> list[list[str]]:
533-    """Build table rows from sorted area findings."""
534-    rows = []
535-    for area, area_findings in sorted_areas[:max_areas]:
536:        t3 = sum(1 for f in area_findings if f["tier"] == 3)
537:        t4 = sum(1 for f in area_findings if f["tier"] == 4)
538-        open_count = sum(1 for f in area_findings if f["status"] == "open")
539-        debt_count = sum(1 for f in area_findings if f["status"] == "wontfix")
540:        weight = sum(f["tier"] for f in area_findings)
541-        rows.append(
542-            [
543-                area,
--
633-    "show_review_summary",
634-    "show_structural_areas",
635-    "show_subjective_followup",
636:    "show_tier_progress_table",
637-    "write_status_query",
638-]
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
desloppify/app/commands/helpers/queue_progress.py-21-    skipped: int = 0
desloppify/app/commands/helpers/queue_progress.py-22-    subjective: int = 0
desloppify/app/commands/helpers/queue_progress.py-23-    suppressed: int = 0
desloppify/app/commands/helpers/queue_progress.py:24:    tier_counts: dict[int, int] = field(default_factory=dict)
desloppify/app/commands/helpers/queue_progress.py-25-    focus_cluster: str | None = None
desloppify/app/commands/helpers/queue_progress.py-26-    focus_cluster_count: int = 0
desloppify/app/commands/helpers/queue_progress.py-27-    focus_cluster_total: int = 0
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-46-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-47-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-48-    queue_total = result["total"]
desloppify/app/commands/helpers/queue_progress.py:49:    tier_counts = dict(result.get("tier_counts", {}))
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-50-    suppressed = int(result.get("suppressed_count", 0))
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-51-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-52-    # Count subjective items in the queue
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-90-        skipped=skipped,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-91-        subjective=subjective,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-92-        suppressed=suppressed,
desloppify/app/commands/helpers/queue_progress.py:93:        tier_counts=tier_counts,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-94-        focus_cluster=focus_cluster,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-95-        focus_cluster_count=focus_cluster_count,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-96-        focus_cluster_total=focus_cluster_total,
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-124-        segments.append(f"{breakdown.suppressed} suppressed")
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-125-
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-126-    # Tier counts — always present
desloppify/app/commands/helpers/queue_progress.py:127:    tc = breakdown.tier_counts
desloppify/app/commands/helpers/queue_progress.py:128:    tier_parts = []
desloppify/app/commands/helpers/queue_progress.py-129-    for t in (1, 2, 3, 4):
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-130-        c = tc.get(t, 0)
desloppify/app/commands/helpers/queue_progress.py-131-        if c > 0:
desloppify/app/commands/helpers/queue_progress.py:132:            tier_parts.append(f"T{t}:{c}")
desloppify/app/commands/helpers/queue_progress.py:133:    if tier_parts:
desloppify/app/commands/helpers/queue_progress.py:134:        segments.append(" ".join(tier_parts))
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-135-
desloppify/app/commands/helpers/queue_progress.py-136-    if segments:
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py-137-        sep = " \u00b7 "
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/resolve",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
No matches found
```

> AGENT

Now let me search for tier references in the test files and remaining areas.

> TOOL

tool_use Grep
```json
{
  "pattern": "tier|T[1-4]",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
14-
15-def _args(**overrides):
16-    base = {
17:        "tier": None,
18-        "count": 1,
19-        "scope": None,
20-        "status": "open",
21-        "group": "item",
22-        "format": "terminal",
23-        "explain": False,
24:        "no_tier_fallback": False,
25-        "output": None,
26-        "lang": None,
27-        "path": ".",
--
83-        out = capsys.readouterr().out
84-        assert "No scans yet. Run: desloppify scan" in out
85-
86:    def test_tier_navigator_always_printed(self, monkeypatch, capsys):
87-        written = []
88-        _patch_common(
89-            monkeypatch,
--
105-            lambda *_a, **_k: {
106-                "items": [],
107-                "total": 0,
108:                "tier_counts": {1: 0, 2: 0, 3: 0, 4: 0},
109:                "requested_tier": None,
110:                "selected_tier": None,
111-                "fallback_reason": None,
112:                "available_tiers": [],
113-            },
114-        )
115-
116-        cmd_next(_args())
117-        out = capsys.readouterr().out
118-        assert "Tier Navigator" in out
119:        assert "desloppify next --tier 1" in out
120-        assert "Nothing to do" in out
121-        assert written[0]["command"] == "next"
122-        assert written[0]["items"] == []
123-
124:    def test_tier_fallback_message_and_payload(self, monkeypatch, capsys):
125-        written = []
126-        _patch_common(
127-            monkeypatch,
--
145-                    {
146-                        "id": "smells::src/a.py::x",
147-                        "kind": "finding",
148:                        "tier": 2,
149:                        "effective_tier": 2,
150-                        "confidence": "high",
151-                        "detector": "smells",
152-                        "file": "src/a.py",
--
157-                    }
158-                ],
159-                "total": 1,
160:                "tier_counts": {1: 0, 2: 1, 3: 0, 4: 0},
161:                "requested_tier": 1,
162:                "selected_tier": 2,
163:                "fallback_reason": "Requested T1 has 0 open -> showing T2 (nearest non-empty).",
164:                "available_tiers": [2],
165-            },
166-        )
167-
168:        cmd_next(_args(tier=1))
169-        out = capsys.readouterr().out
170:        assert "Requested T1 has 0 open -> showing T2 (nearest non-empty)." in out
171:        assert written[0]["queue"]["requested_tier"] == 1
172:        assert written[0]["queue"]["selected_tier"] == 2
173-
174:    def test_no_tier_fallback_strict_empty_guidance(self, monkeypatch, capsys):
175-        written = []
176-        _patch_common(
177-            monkeypatch,
--
193-            lambda *_a, **_k: {
194-                "items": [],
195-                "total": 0,
196:                "tier_counts": {1: 2, 2: 1, 3: 0, 4: 0},
197:                "requested_tier": 4,
198:                "selected_tier": 4,
199:                "fallback_reason": "Requested T4 has 0 open.",
200:                "available_tiers": [1, 2],
201-            },
202-        )
203-
204:        cmd_next(_args(tier=4, no_tier_fallback=True))
205-        out = capsys.readouterr().out
206:        assert "Requested T4 has 0 open." in out
207:        assert "Requested tier: T4" in out
208:        assert "Try: desloppify next --tier 1 | desloppify next --tier 2" in out
209:        assert written[0]["queue"]["available_tiers"] == [1, 2]
210-
211-    def test_subjective_focus_and_review_prepare_hint(self, monkeypatch, capsys):
212-        _patch_common(
--
242-                    {
243-                        "id": "smells::src/a.py::x",
244-                        "kind": "finding",
245:                        "tier": 3,
246:                        "effective_tier": 3,
247-                        "confidence": "medium",
248-                        "detector": "smells",
249-                        "file": "src/a.py",
--
254-                    }
255-                ],
256-                "total": 1,
257:                "tier_counts": {1: 0, 2: 0, 3: 1, 4: 0},
258:                "requested_tier": None,
259:                "selected_tier": None,
260-                "fallback_reason": None,
261:                "available_tiers": [3],
262-            },
263-        )
264-
--
278-                        "id": "subjective_review::src/a.py::changed",
279-                        "detector": "subjective_review",
280-                        "file": "src/a.py",
281:                        "tier": 4,
282-                        "confidence": "medium",
283-                        "summary": "File changed since last review — re-review recommended",
284-                        "status": "open",
--
301-                    {
302-                        "id": "smells::src/a.py::x",
303-                        "kind": "finding",
304:                        "tier": 3,
305:                        "effective_tier": 3,
306-                        "confidence": "medium",
307-                        "detector": "smells",
308-                        "file": "src/a.py",
--
313-                    }
314-                ],
315-                "total": 1,
316:                "tier_counts": {1: 0, 2: 0, 3: 1, 4: 1},
317:                "requested_tier": None,
318:                "selected_tier": None,
319-                "fallback_reason": None,
320:                "available_tiers": [3, 4],
321-            },
322-        )
323-
--
358-                    {
359-                        "id": "smells::src/a.py::x",
360-                        "kind": "finding",
361:                        "tier": 3,
362:                        "effective_tier": 3,
363-                        "confidence": "medium",
364-                        "detector": "smells",
365-                        "file": "src/a.py",
--
370-                    }
371-                ],
372-                "total": 1,
373:                "tier_counts": {1: 0, 2: 0, 3: 1, 4: 0},
374:                "requested_tier": None,
375:                "selected_tier": None,
376-                "fallback_reason": None,
377:                "available_tiers": [3],
378-            },
379-        )
380-
--
393-                        "id": "subjective_review::.::holistic_unreviewed",
394-                        "detector": "subjective_review",
395-                        "file": ".",
396:                        "tier": 4,
397-                        "confidence": "low",
398-                        "summary": "No holistic codebase review on record",
399-                        "status": "open",
--
416-                    {
417-                        "id": "smells::src/a.py::x",
418-                        "kind": "finding",
419:                        "tier": 3,
420:                        "effective_tier": 3,
421-                        "confidence": "medium",
422-                        "detector": "smells",
423-                        "file": "src/a.py",
--
428-                    }
429-                ],
430-                "total": 1,
431:                "tier_counts": {1: 0, 2: 0, 3: 1, 4: 1},
432:                "requested_tier": None,
433:                "selected_tier": None,
434-                "fallback_reason": None,
435:                "available_tiers": [3, 4],
436-            },
437-        )
438-
--
470-                    {
471-                        "id": "smells::src/a.py::x",
472-                        "kind": "finding",
473:                        "tier": 3,
474:                        "effective_tier": 3,
475-                        "confidence": "medium",
476-                        "detector": "smells",
477-                        "file": "src/a.py",
--
482-                    }
483-                ],
484-                "total": 1,
485:                "tier_counts": {1: 0, 2: 0, 3: 1, 4: 0},
486:                "requested_tier": None,
487:                "selected_tier": None,
488-                "fallback_reason": None,
489:                "available_tiers": [3],
490-            },
491-        )
492-
--
538-                    {
539-                        "id": "smells::src/a.py::x",
540-                        "kind": "finding",
541:                        "tier": 3,
542:                        "effective_tier": 3,
543-                        "confidence": "medium",
544-                        "detector": "smells",
545-                        "file": "src/a.py",
--
550-                    }
551-                ],
552-                "total": 1,
553:                "tier_counts": {1: 0, 2: 0, 3: 1, 4: 0},
554:                "requested_tier": None,
555:                "selected_tier": None,
556-                "fallback_reason": None,
557:                "available_tiers": [3],
558-            },
559-        )
560-
--
593-                    {
594-                        "id": "subjective::naming_quality",
595-                        "kind": "subjective_dimension",
596:                        "tier": 4,
597:                        "effective_tier": 4,
598-                        "confidence": "medium",
599-                        "detector": "subjective_assessment",
600-                        "file": ".",
--
604-                        "subjective_score": 94.0,
605-                        "primary_command": "desloppify review --prepare",
606-                        "explain": {
607:                            "policy": "Subjective dimensions are always queued as T4."
608-                        },
609-                    }
610-                ],
611-                "total": 1,
612:                "tier_counts": {1: 0, 2: 0, 3: 0, 4: 1},
613:                "requested_tier": None,
614:                "selected_tier": None,
615-                "fallback_reason": None,
616:                "available_tiers": [4],
617-            },
618-        )
619-
620-        cmd_next(_args(explain=True))
621-        out = capsys.readouterr().out
622:        assert "always queued as T4" in out
623-        assert written[0]["items"][0]["explain"] == {
624:            "policy": "Subjective dimensions are always queued as T4."
625-        }
626-
627-
--
636-                        "strict": 78.0,
637-                        "issues": 5,
638-                        "checks": 100,
639:                        "tier": 2,
640-                    },
641-                },
642-                "potentials": {"python": {"smells": 5}},
--
655-                    {
656-                        "id": "smells::src/a.py::x",
657-                        "kind": "finding",
658:                        "tier": 2,
659:                        "effective_tier": 2,
660-                        "confidence": "high",
661-                        "detector": "smells",
662-                        "file": "src/a.py",
--
667-                    }
668-                ],
669-                "total": 1,
670:                "tier_counts": {1: 0, 2: 1, 3: 0, 4: 0},
671:                "requested_tier": None,
672:                "selected_tier": None,
673-                "fallback_reason": None,
674:                "available_tiers": [2],
675-            },
676-        )
677-
--
703-                    {
704-                        "id": "subjective::naming_quality",
705-                        "kind": "subjective_dimension",
706:                        "tier": 4,
707:                        "effective_tier": 4,
708-                        "confidence": "medium",
709-                        "detector": "subjective_assessment",
710-                        "file": ".",
--
716-                    }
717-                ],
718-                "total": 1,
719:                "tier_counts": {1: 0, 2: 0, 3: 0, 4: 1},
720:                "requested_tier": None,
721:                "selected_tier": None,
722-                "fallback_reason": None,
723:                "available_tiers": [4],
724-            },
725-        )
726-
--
735-            "File health": {
736-                "score": 82,
737-                "strict": 82,
738:                "tier": 3,
739-                "issues": 1,
740-                "detectors": {},
741-            },
742-            "Naming quality": {
743-                "score": 94.0,
744-                "strict": 94.0,
745:                "tier": 4,
746-                "issues": 2,
747-                "detectors": {"subjective_assessment": {}},
748-            },
749-            "Logic clarity": {
750-                "score": 96.0,
751-                "strict": 96.0,
752:                "tier": 4,
753-                "issues": 3,
754-                "detectors": {"subjective_assessment": {}},
755-            },
756-            "Custom Subjective": {
757-                "score": 91.0,
758-                "strict": 91.0,
759:                "tier": 4,
760-                "issues": 1,
761-                "detectors": {"subjective_assessment": {}},
762-            },
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier|T[1-4]",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
144-    def test_next_command(self, parser):
145-        args = parser.parse_args(["next"])
146-        assert args.command == "next"
147:        assert args.tier is None
148-        assert args.count == 1
149-
150:    def test_next_with_tier_and_count(self, parser):
151:        args = parser.parse_args(["next", "--tier", "2", "--count", "5"])
152:        assert args.tier == 2
153-        assert args.count == 5
154-
155-    def test_next_with_scope_status_group_and_format(self, parser):
--
171-        assert args.group == "file"
172-        assert args.format == "md"
173-
174:    def test_next_with_explain_and_no_tier_fallback(self, parser):
175-        args = parser.parse_args(
176:            ["next", "--tier", "4", "--explain", "--no-tier-fallback"]
177-        )
178:        assert args.tier == 4
179-        assert args.explain is True
180:        assert args.no_tier_fallback is True
181-
182-    def test_plan_done_command(self, parser):
183-        args = parser.parse_args(["plan", "done", "id1", "id2"])
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier|T[1-4]",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/test_work_queue.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
19-    *,
20-    detector: str = "smells",
21-    file: str = "src/a.py",
22:    tier: int = 3,
23-    confidence: str = "medium",
24-    status: str = "open",
25-    detail: dict | None = None,
--
28-        "id": fid,
29-        "detector": detector,
30-        "file": file,
31:        "tier": tier,
32-        "confidence": confidence,
33-        "summary": fid,
34-        "status": status,
--
43-    }
44-
45-
46:def test_tier_fallback_selects_nearest_non_empty_tier():
47-    state = _state(
48-        [
49:            _finding("t2_item", tier=2),
50:            _finding("t4_item", tier=4),
51-        ]
52-    )
53-
54:    queue = build_work_queue(state, tier=1, count=None)
55:    assert queue["requested_tier"] == 1
56:    assert queue["selected_tier"] == 2
57-    assert (
58-        queue["fallback_reason"]
59:        == "Requested T1 has 0 open -> showing T2 (nearest non-empty)."
60-    )
61-    assert [item["id"] for item in queue["items"]] == ["t2_item"]
62-
63-
64:def test_no_tier_fallback_returns_empty_with_reason():
65:    state = _state([_finding("t2_item", tier=2)])
66-
67:    queue = build_work_queue(state, tier=4, count=None, no_tier_fallback=True)
68:    assert queue["requested_tier"] == 4
69:    assert queue["selected_tier"] == 4
70-    assert queue["items"] == []
71:    assert queue["fallback_reason"] == "Requested T4 has 0 open."
72-
73-
74:def test_review_finding_uses_natural_tier():
75-    review = _finding(
76-        "review::src/a.py::naming",
77-        detector="review",
78:        tier=2,
79-        detail={"dimension": "naming_quality"},
80-    )
81:    mechanical = _finding("smells::src/a.py::x", detector="smells", tier=3)
82-    state = _state(
83-        [review, mechanical],
84-        dimension_scores={
--
88-
89-    queue = build_work_queue(state, count=None, include_subjective=False)
90-    by_id = {item["id"]: item for item in queue["items"] if item["kind"] == "finding"}
91:    assert by_id["review::src/a.py::naming"]["effective_tier"] == 2
92:    assert by_id["smells::src/a.py::x"]["effective_tier"] == 3
93-
94-
95:def test_review_items_ranked_by_tier_like_mechanical():
96-    urgent = _finding(
97:        "security::src/a.py::x", detector="security", tier=1, confidence="high"
98-    )
99-    review = _finding(
100-        "review::src/a.py::naming",
101-        detector="review",
102:        tier=2,
103-        confidence="high",
104-        detail={"dimension": "naming_quality"},
105-    )
--
111-    )
112-
113-    queue = build_work_queue(state, count=None, include_subjective=False)
114:    # T1 security outranks T2 review
115-    assert queue["items"][0]["id"] == "security::src/a.py::x"
116:    assert queue["items"][0]["effective_tier"] == 1
117:    assert queue["items"][1]["effective_tier"] == 2
118-
119-
120:def test_review_items_sort_by_issue_weight_within_tier():
121-    standard = _finding(
122-        "review::src/a.py::naming",
123-        detector="review",
124:        tier=2,
125-        confidence="high",
126-        detail={"dimension": "naming_quality"},
127-    )
128-    holistic = _finding(
129-        "review::src/a.py::logic",
130-        detector="review",
131:        tier=2,
132-        confidence="high",
133-        detail={"dimension": "logic_clarity", "holistic": True},
134-    )
--
141-    )
142-
143-    queue = build_work_queue(state, count=None, include_subjective=False)
144:    # Within same tier and confidence, holistic (higher review_weight) sorts first
145-    assert [item["id"] for item in queue["items"][:2]] == [
146-        "review::src/a.py::logic",
147-        "review::src/a.py::naming",
148-    ]
149:    assert all(item["effective_tier"] == 2 for item in queue["items"][:2])
150-
151-
152:def test_tier4_queue_contains_mechanical_and_synthetic_subjective_items():
153-    # When no objective backlog exists, subjective items appear alongside mechanical.
154-    state = _state(
155-        [],
--
159-        },
160-    )
161-
162:    queue = build_work_queue(state, tier=4, count=None, include_subjective=True)
163-    ids = {item["id"] for item in queue["items"]}
164-    assert "subjective::naming_quality" in ids
165-
--
168-    """Subjective items whose only action is --force-review-rerun are
169-    suppressed while objective findings remain in the queue."""
170-    mech_t4 = _finding(
171:        "dupes::src/a.py::pair", detector="dupes", tier=4, confidence="medium"
172-    )
173-    state = _state(
174-        [mech_t4],
--
177-        },
178-    )
179-
180:    queue = build_work_queue(state, tier=4, count=None, include_subjective=True)
181-    ids = {item["id"] for item in queue["items"]}
182-    assert "dupes::src/a.py::pair" in ids
183-    assert "subjective::naming_quality" not in ids
--
189-    review = _finding(
190-        "review::.::holistic::naming_quality::abc12345",
191-        detector="review",
192:        tier=3,
193-        detail={"holistic": True, "dimension": "naming_quality"},
194-    )
195-    state = _state(
196-        [
197:            _finding("security::src/a.py::x", detector="security", tier=1, confidence="high"),
198:            _finding("smells::src/a.py::y", detector="smells", tier=2, confidence="medium"),
199-            review,
200-        ],
201-        dimension_scores={
--
212-def test_subjective_interleave_guardrail_applies_with_default_count_limit():
213-    state = _state(
214-        [
215:            _finding("security::src/a.py::x", detector="security", tier=1, confidence="high"),
216-        ],
217-        dimension_scores={
218-            "Naming quality": {"score": 80.0, "strict": 80.0, "issues": 5},
--
227-    state = _state(
228-        [
229-            _finding(
230:                "smells::src/a.py::x", tier=3, confidence="medium", detail={"count": 7}
231-            )
232-        ]
233-    )
--
236-    item = queue["items"][0]
237-    assert "explain" in item
238-    assert item["explain"]["ranking_factors"] == [
239:        "tier asc",
240-        "confidence asc",
241-        "count desc",
242-        "id asc",
--
253-    )
254-
255-    queue = build_work_queue(
256:        state, tier=4, count=None, include_subjective=True, subjective_threshold=95
257-    )
258-    ids = {item["id"] for item in queue["items"]}
259-    assert "subjective::naming_quality" in ids
--
264-    review = _finding(
265-        "review::.::holistic::mid_level_elegance::split::abc12345",
266-        detector="review",
267:        tier=3,
268-        detail={"holistic": True, "dimension": "mid_level_elegance"},
269-    )
270-    state = _state(
--
275-    )
276-
277-    queue = build_work_queue(
278:        state, tier=4, count=None, include_subjective=True, subjective_threshold=95
279-    )
280-    subj = next(
281-        item for item in queue["items"] if item["kind"] == "subjective_dimension"
--
289-    review = _finding(
290-        "review::.::holistic::initialization_coupling::abc12345",
291-        detector="review",
292:        tier=3,
293-        detail={"holistic": True, "dimension": "initialization_coupling"},
294-    )
295-    state = _state(
--
317-    }
318-
319-    queue = build_work_queue(
320:        state, tier=4, count=None, include_subjective=True, subjective_threshold=95
321-    )
322-    subj = next(
323-        item for item in queue["items"] if item["kind"] == "subjective_dimension"
--
336-    )
337-
338-    queue = build_work_queue(
339:        state, tier=4, count=None, include_subjective=True, subjective_threshold=95
340-    )
341-    subj = next(
342-        item for item in queue["items"] if item["kind"] == "subjective_dimension"
--
349-    coverage = _finding(
350-        "subjective_review::src/a.py::changed",
351-        detector="subjective_review",
352:        tier=4,
353-        detail={"reason": "changed"},
354-    )
355-    state = _state([coverage])
--
364-        "subjective_review::.::holistic_unreviewed",
365-        detector="subjective_review",
366-        file=".",
367:        tier=4,
368-        detail={"reason": "unreviewed"},
369-    )
370-    state = _state([holistic])
--
379-
380-def test_queue_build_options_defaults():
381-    opts = QueueBuildOptions()
382:    assert opts.tier is None
383-    assert opts.count == 1
384-    assert opts.scan_path is None
385-    assert opts.scope is None
--
387-    assert opts.include_subjective is True
388-    assert opts.subjective_threshold == 100.0
389-    assert opts.chronic is False
390:    assert opts.no_tier_fallback is False
391-    assert opts.explain is False
392-
393-
--
437-    )
438-    # threshold=-10 clamps to 0.0 -> score 50 >= 0 -> item excluded
439-    queue = build_work_queue(
440:        state, tier=4, count=None, include_subjective=True, subjective_threshold=-10
441-    )
442-    subj_items = [item for item in queue["items"] if item["kind"] == "subjective_dimension"]
443-    assert subj_items == []
444-
445-    # threshold=200 clamps to 100.0 -> score 50 < 100 -> item included
446-    queue2 = build_work_queue(
447:        state, tier=4, count=None, include_subjective=True, subjective_threshold=200
448-    )
449-    subj_items2 = [item for item in queue2["items"] if item["kind"] == "subjective_dimension"]
450-    assert len(subj_items2) >= 1
--
456-def test_count_limits_returned_items():
457-    state = _state(
458-        [
459:            _finding("a", tier=2, confidence="high"),
460:            _finding("b", tier=2, confidence="medium"),
461:            _finding("c", tier=2, confidence="low"),
462-        ]
463-    )
464-
--
469-
470-def test_count_none_returns_all_items():
471-    state = _state(
472:        [_finding("a", tier=2), _finding("b", tier=3), _finding("c", tier=4)]
473-    )
474-
475-    queue = build_work_queue(state, count=None, include_subjective=False)
--
479-
480-def test_default_count_is_1():
481-    state = _state(
482:        [_finding("a", tier=2), _finding("b", tier=3)]
483-    )
484-
485-    queue = build_work_queue(state, include_subjective=False)
--
493-    queue = build_work_queue({}, count=None, include_subjective=False)
494-    assert queue["items"] == []
495-    assert queue["total"] == 0
496:    assert queue["tier_counts"] == {1: 0, 2: 0, 3: 0, 4: 0}
497:    assert queue["available_tiers"] == []
498:    assert queue["requested_tier"] is None
499:    assert queue["selected_tier"] is None
500-    assert queue["fallback_reason"] is None
501-
502-
503:# ── Available tiers ───────────────────────────────────────
504-
505-
506:def test_available_tiers_reflects_populated_tiers():
507-    state = _state(
508-        [
509:            _finding("a", tier=2),
510:            _finding("b", tier=4),
511-        ]
512-    )
513-
514-    queue = build_work_queue(state, count=None, include_subjective=False)
515:    assert 2 in queue["available_tiers"]
516:    assert 4 in queue["available_tiers"]
517:    assert 1 not in queue["available_tiers"]
518:    assert 3 not in queue["available_tiers"]
519-
520-
521-# ── Grouped output ────────────────────────────────────────
--
607-    while objective findings exist — their only action (--force-review-rerun)
608-    is blocked by the review preflight."""
609-    objective_findings = [
610:        _finding(f"smells::src/{c}.py::x", detector="smells", tier=3)
611-        for c in "abcd"
612-    ]
613-    state = _state(
--
675-    review = _finding(
676-        "review::.::holistic::naming_quality::abc12345",
677-        detector="review",
678:        tier=3,
679-        detail={"holistic": True, "dimension": "naming_quality"},
680-    )
681-    objective_findings = [
682:        _finding(f"smells::src/{c}.py::x", detector="smells", tier=3)
683-        for c in "abcdef"
684-    ]
685-    state = _state(
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier|T[1-4]",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_queue_progress.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
61-    assert b.skipped == 0
62-    assert b.subjective == 0
63-    assert b.suppressed == 0
64:    assert b.tier_counts == {}
65-    assert b.focus_cluster is None
66-    assert b.focus_cluster_count == 0
67-    assert b.focus_cluster_total == 0
--
76-# ── format_queue_headline ────────────────────────────────────
77-
78-
79:def test_headline_basic_tiers():
80-    b = QueueBreakdown(
81-        queue_total=100,
82:        tier_counts={1: 5, 2: 20, 3: 70, 4: 5},
83-    )
84-    headline = format_queue_headline(b)
85:    assert headline == "Queue: 100 items (T1:5 T2:20 T3:70 T4:5)"
86-
87-
88-def test_headline_with_plan_and_skipped():
--
90-        queue_total=1934,
91-        plan_ordered=292,
92-        skipped=23,
93:        tier_counts={1: 5, 2: 42, 3: 1800, 4: 87},
94-    )
95-    headline = format_queue_headline(b)
96-    assert "1934 items" in headline
97-    assert "292 planned" in headline
98-    assert "23 skipped" in headline
99:    assert "T1:5" in headline
100:    assert "T2:42" in headline
101:    assert "T3:1800" in headline
102:    assert "T4:87" in headline
103-
104-
105-def test_headline_omits_zero_segments():
--
109-        skipped=0,
110-        subjective=0,
111-        suppressed=0,
112:        tier_counts={1: 0, 2: 10, 3: 40, 4: 0},
113-    )
114-    headline = format_queue_headline(b)
115-    assert "planned" not in headline
116-    assert "skipped" not in headline
117-    assert "subjective" not in headline
118-    assert "suppressed" not in headline
119:    assert "T1:" not in headline
120:    assert "T4:" not in headline
121:    assert "T2:10" in headline
122:    assert "T3:40" in headline
123-
124-
125-def test_headline_singular_item():
126:    b = QueueBreakdown(queue_total=1, tier_counts={1: 1})
127-    headline = format_queue_headline(b)
128:    assert "1 item " in headline or headline.endswith("1 item (T1:1)")
129-    assert "items" not in headline
130-
131-
--
133-    b = QueueBreakdown(
134-        queue_total=100,
135-        suppressed=3,
136:        tier_counts={3: 100},
137-    )
138-    headline = format_queue_headline(b)
139-    assert "3 suppressed" in headline
--
143-    b = QueueBreakdown(
144-        queue_total=50,
145-        subjective=5,
146:        tier_counts={3: 45, 4: 5},
147-    )
148-    headline = format_queue_headline(b)
149-    assert "5 subjective" in headline
150-
151-
152-def test_headline_no_plan_mode():
153:    """When no plan data, only tiers are shown."""
154-    b = QueueBreakdown(
155-        queue_total=200,
156:        tier_counts={1: 10, 2: 50, 3: 130, 4: 10},
157-    )
158-    headline = format_queue_headline(b)
159-    assert "planned" not in headline
--
168-        queue_total=100,
169-        plan_ordered=50,
170-        skipped=10,
171:        tier_counts={1: 5, 2: 20, 3: 70, 4: 5},
172-    )
173-    block = format_queue_block(b)
174-    texts = [text for text, _style in block]
--
182-    b = QueueBreakdown(
183-        queue_total=100,
184-        plan_ordered=50,
185:        tier_counts={1: 5, 2: 20, 3: 70, 4: 5},
186-        focus_cluster="smart-t1-review",
187-        focus_cluster_count=12,
188-        focus_cluster_total=50,
--
203-    """No plan — should show 'Start planning' hint."""
204-    b = QueueBreakdown(
205-        queue_total=200,
206:        tier_counts={1: 10, 2: 50, 3: 130, 4: 10},
207-    )
208-    block = format_queue_block(b)
209-    texts = [text for text, _style in block]
--
216-    b = QueueBreakdown(
217-        queue_total=100,
218-        plan_ordered=50,
219:        tier_counts={3: 100},
220-    )
221-    block = format_queue_block(b, frozen_score=74.4)
222-    texts = [text for text, _style in block]
--
235-            {"kind": "finding"},
236-            {"kind": "subjective_dimension"},
237-        ],
238:        "tier_counts": {1: 5, 2: 10, 3: 30, 4: 5},
239-        "suppressed_count": 2,
240-    }
241-    plan = {
--
252-    assert breakdown.skipped == 1
253-    assert breakdown.subjective == 1
254-    assert breakdown.suppressed == 2
255:    assert breakdown.tier_counts == {1: 5, 2: 10, 3: 30, 4: 5}
256-
257-
258-def test_plan_aware_queue_breakdown_no_plan():
259-    mock_result = {
260-        "total": 30,
261-        "items": [],
262:        "tier_counts": {3: 30},
263-        "suppressed_count": 0,
264-    }
265-    with patch(
--
277-    mock_result = {
278-        "total": 10,
279-        "items": [],
280:        "tier_counts": {2: 10},
281-        "suppressed_count": 0,
282-    }
283-    plan = {
--
330-    b = QueueBreakdown(
331-        queue_total=100,
332-        plan_ordered=50,
333:        tier_counts={3: 100},
334-    )
335-    print_frozen_score_with_queue_context(plan, queue_remaining=100, breakdown=b)
336-    output = capsys.readouterr().out
--
344-
345-def test_reveal_uses_frozen_path_when_plan_active_and_queue_remaining(capsys):
346-    plan = {"plan_start_scores": {"strict": 80.0}}
347:    breakdown = QueueBreakdown(queue_total=3, tier_counts={3: 3})
348-    with patch(
349-        "desloppify.app.commands.helpers.queue_progress.plan_aware_queue_breakdown",
350-        return_value=breakdown,
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests",
  "output_mode": "files_with_matches",
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
Found 64 files
desloppify/tests/commands/test_cluster_ux.py
desloppify/tests/plan/test_suffix_matching.py
desloppify/tests/review/test_work_queue.py
desloppify/tests/plan/test_skip.py
desloppify/tests/plan/test_epic_synthesis.py
desloppify/tests/plan/test_auto_cluster.py
desloppify/tests/commands/test_queue_progress.py
desloppify/tests/commands/test_synthesis_fold_confirm.py
desloppify/tests/commands/test_synthesis_jump_back.py
desloppify/tests/commands/test_synthesis_attestation.py
desloppify/tests/commands/test_synthesis_auto_start.py
desloppify/tests/commands/test_synthesis_logging.py
desloppify/tests/commands/test_synthesis_confirmation.py
desloppify/tests/commands/test_cluster_guard.py
desloppify/tests/commands/test_queue_order_guard.py
desloppify/tests/plan/test_reconcile.py
desloppify/tests/scoring/test_scoring.py
desloppify/tests/scan/test_scan_reporting_direct.py
desloppify/tests/review/test_review_submodules.py
desloppify/tests/review/test_review_coverage.py
desloppify/tests/review/import_scoring/test_review_import_scoring.py
desloppify/tests/review/context/test_holistic_review.py
desloppify/tests/lang/csharp/test_csharp_scan.py
desloppify/tests/detectors/test_external_adapters.py
desloppify/tests/core/test_plan.py
desloppify/tests/commands/test_review_preflight.py
desloppify/tests/commands/test_direct_coverage_modules.py
desloppify/tests/commands/test_cmd_next.py
desloppify/tests/commands/test_cli.py
desloppify/tests/review/integration/test_review_coverage.py
desloppify/tests/review/integration/test_work_queue.py
desloppify/tests/scan/test_scan_workflow_integration_direct.py
desloppify/tests/commands/test_cmd_status.py
desloppify/tests/commands/test_cmd_show.py
desloppify/tests/lang/common/test_generic_plugin.py
desloppify/tests/review/context/test_mechanical_evidence.py
desloppify/tests/review/context/test_issue_history_context.py
desloppify/tests/commands/test_plan_override_transactions.py
desloppify/tests/lang/common/test_treesitter.py
desloppify/tests/detectors/test_test_coverage.py
desloppify/tests/detectors/test_passthrough.py
desloppify/tests/detectors/test_coverage_internals.py
desloppify/tests/detectors/test_concerns.py
desloppify/tests/commands/test_transitive_engine.py
desloppify/tests/commands/test_status_subjective_issue_visibility.py
desloppify/tests/commands/test_direct_coverage_split_modules.py
desloppify/tests/commands/test_cmd_fix.py
desloppify/tests/scoring/test_scorecard.py
desloppify/tests/scan/test_scan_workflow_wontfix_direct.py
desloppify/tests/review/integration/test_review_submodules.py
desloppify/tests/state/test_suppression_scoring.py
desloppify/tests/state/test_state.py
desloppify/tests/core/test_narrative.py
desloppify/tests/scoring/test_scorecard_projection_direct.py
desloppify/tests/state/test_state_internal_scoring_direct.py
desloppify/tests/scoring/test_scoring_review_exclusion.py
desloppify/tests/state/test_state_internal_direct.py
desloppify/tests/review/shared_review_fixtures.py
desloppify/tests/core/test_plan_modules_direct.py
desloppify/tests/core/test_narrative_strategy.py
desloppify/tests/lang/common/test_lang_finding_factories_direct.py
desloppify/tests/lang/common/test_lang_base.py
desloppify/tests/detectors/security/test_security.py
desloppify/tests/core/test_narrative_engines_direct.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py",
  "output_mode": "content",
  "-n": true,
  "-C": 2
}
```

> TOOL

tool_result Grep
```
16-from desloppify.engine._work_queue.ranking import (
17-    build_finding_items,
18:    choose_fallback_tier,
19-    group_queue_items,
20-    item_explain,
21-    item_sort_key,
22:    tier_counts,
23-)
24-from desloppify.state import StateModel
--
27-@dataclass(frozen=True)
28-class QueueBuildOptions:
29:    """Configuration for queue construction and tier selection behavior."""
30-
31:    tier: int | None = None
32-    count: int | None = 1
33-    scan_path: str | None = None
--
37-    subjective_threshold: float = 100.0
38-    chronic: bool = False
39:    no_tier_fallback: bool = False
40-    explain: bool = False
41-    plan: dict | None = None
--
50-    items: list[dict]
51-    total: int
52:    tier_counts: dict[int, int]
53:    requested_tier: int | None
54:    selected_tier: int | None
55-    fallback_reason: str | None
56:    available_tiers: list[int]
57-    grouped: dict[str, list[dict]]
58-    suppressed_count: int
--
209-
210-
211:def _item_matches_tier(item: dict, tier: int) -> bool:
212:    """Check if an item (or any of its members for clusters) matches a tier."""
213-    if item.get("kind") == "cluster":
214-        return any(
215:            int(m.get("effective_tier", m.get("tier", 3))) == tier
216-            for m in item.get("members", [])
217-        )
218:    return int(item.get("effective_tier", item.get("tier", 3))) == tier
219-
220-
--
321-    options: QueueBuildOptions | None = None,
322-) -> WorkQueueResult:
323:    """Build ranked queue items + tier metadata."""
324-    resolved_options = options or QueueBuildOptions()
325-
--
399-        and status in {"open", "all"}
400-        and not resolved_options.chronic
401:        and resolved_options.tier is None
402-        and not resolved_options.scope
403-        and not resolved_options.cluster
--
406-        all_items = _apply_subjective_interleave_guardrail(all_items)
407-
408:    counts = tier_counts(all_items)
409-
410:    requested_tier = (
411:        int(resolved_options.tier) if resolved_options.tier is not None else None
412-    )
413:    selected_tier = requested_tier
414-    fallback_reason = None
415-    filtered = all_items
416-
417:    if requested_tier is not None:
418-        filtered = [
419-            item
420-            for item in all_items
421:            if _item_matches_tier(item, requested_tier)
422-        ]
423:        if not filtered and not resolved_options.no_tier_fallback:
424:            chosen = choose_fallback_tier(requested_tier, counts)
425-            if chosen is not None:
426:                selected_tier = chosen
427-                filtered = [
428-                    item
429-                    for item in all_items
430:                    if _item_matches_tier(item, chosen)
431-                ]
432-                fallback_reason = (
433:                    f"Requested T{requested_tier} has 0 open -> showing T{chosen} "
434-                    "(nearest non-empty)."
435-                )
436-        elif not filtered:
437:            fallback_reason = f"Requested T{requested_tier} has 0 open."
438-
439-    total = len(filtered)
--
445-            item["explain"] = item_explain(item)
446-
447:    available_tiers = [tier for tier, value in counts.items() if value > 0]
448-    return {
449-        "items": filtered,
450-        "total": total,
451:        "tier_counts": counts,
452:        "requested_tier": requested_tier,
453:        "selected_tier": selected_tier,
454-        "fallback_reason": fallback_reason,
455:        "available_tiers": available_tiers,
456-        "grouped": group_queue_items(filtered, "item"),
457-        "new_ids": new_ids,
```

> AGENT

Let me also check the remaining key files for tier references in queue-ordering context.

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/rendering.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
No matches found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
192-
193-    return {
194-        "id": SYNTHESIS_ID,
195:        "tier": 1,
196-        "confidence": "high",
197-        "detector": "synthesis",
198-        "file": ".",
--
239-def build_subjective_items(
240-    state: dict, findings: dict, *, threshold: float = 100.0
241-) -> list[dict]:
242:    """Create synthetic subjective work items (always tier 4)."""
243-    dim_scores = state.get("dimension_scores", {}) or {}
244-    if not dim_scores:
245-        return []
--
333-                "id": f"subjective::{slugify(dim_key)}",
334-                "detector": "subjective_assessment",
335-                "file": ".",
336:                "tier": 4,
337:                "effective_tier": 4,
338-                "confidence": "medium",
339-                "summary": summary,
340-                "detail": {
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py",
  "output_mode": "content",
  "-n": true,
  "-C": 2
}
```

> TOOL

tool_result Grep
```
53-        item["is_review"] = is_review_finding(item)
54-        item["is_subjective"] = is_subjective_finding(item)
55:        item["effective_tier"] = (
56:            4 if item["is_subjective"] else int(finding.get("tier", 3))
57-        )
58-        item["review_weight"] = (
--
105-    if item.get("kind") == "subjective_dimension" or item.get("is_subjective"):
106-        return (
107:            int(item.get("effective_tier", 4)),
108-            1,  # Subjective items sort after mechanical items within T4.
109-            subjective_score_value(item),
--
114-    review_weight = float(item.get("review_weight", 0.0) or 0.0)
115-    return (
116:        int(item.get("effective_tier", item.get("tier", 3))),
117-        0,
118-        CONFIDENCE_ORDER.get(item.get("confidence", "low"), 9),
--
124-
125-def item_explain(item: dict) -> dict:
126:    effective_tier = int(item.get("effective_tier", item.get("tier", 3)))
127-
128-    if item.get("kind") == "subjective_dimension":
129-        return {
130-            "kind": "subjective_dimension",
131:            "effective_tier": effective_tier,
132-            "subjective_score": subjective_score_value(item),
133-            "policy": (
--
135-                "mechanical T1/T2/T3 items."
136-            ),
137:            "ranking_factors": ["tier asc", "subjective_score asc", "id asc"],
138-        }
139-
--
144-    ranking_factors: list[str]
145-    if is_subjective:
146:        ranking_factors = ["tier fixed to T4", "subjective_score asc", "id asc"]
147-    elif is_review:
148-        ranking_factors = [
149:            "tier asc",
150-            "confidence asc",
151-            "review_weight desc",
--
154-        ]
155-    else:
156:        ranking_factors = ["tier asc", "confidence asc", "count desc", "id asc"]
157-    explain = {
158-        "kind": "finding",
159:        "effective_tier": effective_tier,
160-        "confidence": confidence,
161-        "confidence_rank": CONFIDENCE_ORDER.get(confidence, 9),
--
175-
176-
177:def tier_counts(items: list[dict]) -> dict[int, int]:
178-    counts = {1: 0, 2: 0, 3: 0, 4: 0}
179-    for item in items:
180-        if item.get("kind") == "cluster":
181:            # Count each member at its own tier
182-            for member in item.get("members", []):
183:                tier = int(member.get("effective_tier", member.get("tier", 3)))
184:                counts[tier] = counts.get(tier, 0) + 1
185-            continue
186:        tier = int(item.get("effective_tier", item.get("tier", 3)))
187:        counts[tier] = counts.get(tier, 0) + 1
188-    return counts
189-
190-
191:def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
192:    available = [tier for tier, count in counts.items() if count > 0]
193-    if not available:
194-        return None
195:    return min(available, key=lambda tier: (abs(tier - requested_tier), tier))
196-
197-
--
204-        elif group == "detector":
205-            key = item.get("detector", "")
206:        elif group == "tier":
207:            key = f"T{int(item.get('effective_tier', item.get('tier', 3)))}"
208-        elif group == "cluster":
209-            plan_cluster = item.get("plan_cluster")
--
217-__all__ = [
218-    "build_finding_items",
219:    "choose_fallback_tier",
220-    "item_explain",
221-    "item_sort_key",
222:    "tier_counts",
223-    "subjective_score_value",
224-    "group_queue_items",
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/integration/test_work_queue.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
19-    *,
20-    detector: str = "smells",
21-    file: str = "src/a.py",
22:    tier: int = 3,
23-    confidence: str = "medium",
24-    status: str = "open",
25-    detail: dict | None = None,
--
28-        "id": fid,
29-        "detector": detector,
30-        "file": file,
31:        "tier": tier,
32-        "confidence": confidence,
33-        "summary": fid,
34-        "status": status,
--
43-    }
44-
45-
46:def test_tier_fallback_selects_nearest_non_empty_tier():
47-    state = _state(
48-        [
49:            _finding("t2_item", tier=2),
50:            _finding("t4_item", tier=4),
51-        ]
52-    )
53-
54:    queue = build_work_queue(state, tier=1, count=None)
55:    assert queue["requested_tier"] == 1
56:    assert queue["selected_tier"] == 2
57-    assert (
58-        queue["fallback_reason"]
59-        == "Requested T1 has 0 open -> showing T2 (nearest non-empty)."
--
61-    assert [item["id"] for item in queue["items"]] == ["t2_item"]
62-
63-
64:def test_no_tier_fallback_returns_empty_with_reason():
65:    state = _state([_finding("t2_item", tier=2)])
66-
67:    queue = build_work_queue(state, tier=4, count=None, no_tier_fallback=True)
68:    assert queue["requested_tier"] == 4
69:    assert queue["selected_tier"] == 4
70-    assert queue["items"] == []
71-    assert queue["fallback_reason"] == "Requested T4 has 0 open."
72-
73-
74:def test_review_finding_uses_natural_tier():
75-    review = _finding(
76-        "review::src/a.py::naming",
77-        detector="review",
78:        tier=2,
79-        detail={"dimension": "naming_quality"},
80-    )
81:    mechanical = _finding("smells::src/a.py::x", detector="smells", tier=3)
82-    state = _state(
83-        [review, mechanical],
84-        dimension_scores={
--
88-
89-    queue = build_work_queue(state, count=None, include_subjective=False)
90-    by_id = {item["id"]: item for item in queue["items"] if item["kind"] == "finding"}
91:    assert by_id["review::src/a.py::naming"]["effective_tier"] == 2
92:    assert by_id["smells::src/a.py::x"]["effective_tier"] == 3
93-
94-
95:def test_review_items_ranked_by_tier_like_mechanical():
96-    urgent = _finding(
97:        "security::src/a.py::x", detector="security", tier=1, confidence="high"
98-    )
99-    review = _finding(
100-        "review::src/a.py::naming",
101-        detector="review",
102:        tier=2,
103-        confidence="high",
104-        detail={"dimension": "naming_quality"},
105-    )
--
113-    queue = build_work_queue(state, count=None, include_subjective=False)
114-    # T1 security outranks T2 review
115-    assert queue["items"][0]["id"] == "security::src/a.py::x"
116:    assert queue["items"][0]["effective_tier"] == 1
117:    assert queue["items"][1]["effective_tier"] == 2
118-
119-
120:def test_review_items_sort_by_issue_weight_within_tier():
121-    standard = _finding(
122-        "review::src/a.py::naming",
123-        detector="review",
124:        tier=2,
125-        confidence="high",
126-        detail={"dimension": "naming_quality"},
127-    )
128-    holistic = _finding(
129-        "review::src/a.py::logic",
130-        detector="review",
131:        tier=2,
132-        confidence="high",
133-        detail={"dimension": "logic_clarity", "holistic": True},
134-    )
--
141-    )
142-
143-    queue = build_work_queue(state, count=None, include_subjective=False)
144:    # Within same tier and confidence, holistic (higher review_weight) sorts first
145-    assert [item["id"] for item in queue["items"][:2]] == [
146-        "review::src/a.py::logic",
147-        "review::src/a.py::naming",
148-    ]
149:    assert all(item["effective_tier"] == 2 for item in queue["items"][:2])
150-
151-
152:def test_tier4_queue_contains_mechanical_and_synthetic_subjective_items():
153-    mech_t4 = _finding(
154:        "dupes::src/a.py::pair", detector="dupes", tier=4, confidence="medium"
155-    )
156-    state = _state(
157-        [mech_t4],
--
161-        },
162-    )
163-
164:    queue = build_work_queue(state, tier=4, count=None, include_subjective=True)
165-    ids = {item["id"] for item in queue["items"]}
166-    kinds = {item["kind"] for item in queue["items"]}
167-    assert "dupes::src/a.py::pair" in ids
--
172-def test_subjective_items_do_not_starve_objective_queue_head():
173-    state = _state(
174-        [
175:            _finding("security::src/a.py::x", detector="security", tier=1, confidence="high"),
176:            _finding("smells::src/a.py::y", detector="smells", tier=2, confidence="medium"),
177-        ],
178-        dimension_scores={
179-            "Naming quality": {"score": 92.0, "strict": 92.0, "issues": 3},
--
191-    review = _finding(
192-        "review::.::holistic::naming_quality::split::abc12345",
193-        detector="review",
194:        tier=3,
195-        detail={"holistic": True, "dimension": "naming_quality"},
196-    )
197-    state = _state(
--
226-        subjective_threshold=95,
227-    )
228-    subj = next(item for item in queue["items"] if item["id"] == "subjective::naming_quality")
229:    assert subj["effective_tier"] == 2
230-    assert "subjective_promotion_reason" in subj
231-    starvation = queue["subjective_starvation"]
232-    assert starvation["warning"] is True
--
236-def test_subjective_interleave_guardrail_applies_with_default_count_limit():
237-    state = _state(
238-        [
239:            _finding("security::src/a.py::x", detector="security", tier=1, confidence="high"),
240-        ],
241-        dimension_scores={
242-            "Naming quality": {"score": 80.0, "strict": 80.0, "issues": 5},
--
251-    state = _state(
252-        [
253-            _finding(
254:                "smells::src/a.py::x", tier=3, confidence="medium", detail={"count": 7}
255-            )
256-        ]
257-    )
--
260-    item = queue["items"][0]
261-    assert "explain" in item
262-    assert item["explain"]["ranking_factors"] == [
263:        "tier asc",
264-        "confidence asc",
265-        "count desc",
266-        "id asc",
--
277-    )
278-
279-    queue = build_work_queue(
280:        state, tier=4, count=None, include_subjective=True, subjective_threshold=95
281-    )
282-    ids = {item["id"] for item in queue["items"]}
283-    assert "subjective::naming_quality" in ids
--
288-    review = _finding(
289-        "review::.::holistic::mid_level_elegance::split::abc12345",
290-        detector="review",
291:        tier=3,
292-        detail={"holistic": True, "dimension": "mid_level_elegance"},
293-    )
294-    state = _state(
--
299-    )
300-
301-    queue = build_work_queue(
302:        state, tier=4, count=None, include_subjective=True, subjective_threshold=95
303-    )
304-    subj = next(
305-        item for item in queue["items"] if item["kind"] == "subjective_dimension"
--
313-    review = _finding(
314-        "review::.::holistic::initialization_coupling::abc12345",
315-        detector="review",
316:        tier=3,
317-        detail={"holistic": True, "dimension": "initialization_coupling"},
318-    )
319-    state = _state(
--
341-    }
342-
343-    queue = build_work_queue(
344:        state, tier=4, count=None, include_subjective=True, subjective_threshold=95
345-    )
346-    subj = next(
347-        item for item in queue["items"] if item["kind"] == "subjective_dimension"
--
360-    )
361-
362-    queue = build_work_queue(
363:        state, tier=4, count=None, include_subjective=True, subjective_threshold=95
364-    )
365-    subj = next(
366-        item for item in queue["items"] if item["kind"] == "subjective_dimension"
--
373-    coverage = _finding(
374-        "subjective_review::src/a.py::changed",
375-        detector="subjective_review",
376:        tier=4,
377-        detail={"reason": "changed"},
378-    )
379-    state = _state([coverage])
--
388-        "subjective_review::.::holistic_unreviewed",
389-        detector="subjective_review",
390-        file=".",
391:        tier=4,
392-        detail={"reason": "unreviewed"},
393-    )
394-    state = _state([holistic])
--
403-
404-def test_queue_build_options_defaults():
405-    opts = QueueBuildOptions()
406:    assert opts.tier is None
407-    assert opts.count == 1
408-    assert opts.scan_path is None
409-    assert opts.scope is None
--
411-    assert opts.include_subjective is True
412-    assert opts.subjective_threshold == 100.0
413-    assert opts.chronic is False
414:    assert opts.no_tier_fallback is False
415-    assert opts.explain is False
416-
417-
--
461-    )
462-    # threshold=-10 clamps to 0.0 -> score 50 >= 0 -> item excluded
463-    queue = build_work_queue(
464:        state, tier=4, count=None, include_subjective=True, subjective_threshold=-10
465-    )
466-    subj_items = [item for item in queue["items"] if item["kind"] == "subjective_dimension"]
467-    assert subj_items == []
468-
469-    # threshold=200 clamps to 100.0 -> score 50 < 100 -> item included
470-    queue2 = build_work_queue(
471:        state, tier=4, count=None, include_subjective=True, subjective_threshold=200
472-    )
473-    subj_items2 = [item for item in queue2["items"] if item["kind"] == "subjective_dimension"]
474-    assert len(subj_items2) >= 1
--
480-def test_count_limits_returned_items():
481-    state = _state(
482-        [
483:            _finding("a", tier=2, confidence="high"),
484:            _finding("b", tier=2, confidence="medium"),
485:            _finding("c", tier=2, confidence="low"),
486-        ]
487-    )
488-
--
493-
494-def test_count_none_returns_all_items():
495-    state = _state(
496:        [_finding("a", tier=2), _finding("b", tier=3), _finding("c", tier=4)]
497-    )
498-
499-    queue = build_work_queue(state, count=None, include_subjective=False)
--
503-
504-def test_default_count_is_1():
505-    state = _state(
506:        [_finding("a", tier=2), _finding("b", tier=3)]
507-    )
508-
509-    queue = build_work_queue(state, include_subjective=False)
--
517-    queue = build_work_queue({}, count=None, include_subjective=False)
518-    assert queue["items"] == []
519-    assert queue["total"] == 0
520:    assert queue["tier_counts"] == {1: 0, 2: 0, 3: 0, 4: 0}
521:    assert queue["available_tiers"] == []
522:    assert queue["requested_tier"] is None
523:    assert queue["selected_tier"] is None
524-    assert queue["fallback_reason"] is None
525-
526-
527:# ── Available tiers ───────────────────────────────────────
528-
529-
530:def test_available_tiers_reflects_populated_tiers():
531-    state = _state(
532-        [
533:            _finding("a", tier=2),
534:            _finding("b", tier=4),
535-        ]
536-    )
537-
538-    queue = build_work_queue(state, count=None, include_subjective=False)
539:    assert 2 in queue["available_tiers"]
540:    assert 4 in queue["available_tiers"]
541:    assert 1 not in queue["available_tiers"]
542:    assert 3 not in queue["available_tiers"]
543-
544-
545-# ── Grouped output ────────────────────────────────────────
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_queue_order_guard.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
19-            "status": "open",
20-            "detector": "unused",
21-            "file": "test.py",
22:            "tier": 1,
23-            "confidence": "high",
24-            "summary": f"Finding {fid}",
25-        }
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/scan/scan_workflow.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
No matches found
```

> AGENT

Now let me check the remaining areas -- the `engine/work_queue.py` facade, `engine/plan.py`, and search for any CLI parser `--group` choices that include "tier".

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
39-    update_investigation,
40-)
41-
42:# --- ranking: sort keys, tier counts, grouping -----------------------------
43-from desloppify.engine._work_queue.ranking import (
44-    build_finding_items,
45:    choose_fallback_tier,
46-    item_explain,
47-    item_sort_key,
48-    subjective_score_value,
49:    tier_counts,
50-)
51-
52-__all__ = [
--
70-    "supported_fixers_for_item",
71-    # ranking
72-    "build_finding_items",
73:    "choose_fallback_tier",
74-    "item_explain",
75-    "item_sort_key",
76-    "subjective_score_value",
77:    "tier_counts",
78-    # issues
79-    "expire_stale_holistic",
80-    "impact_label",
```

> TOOL

tool_use Grep
```json
{
  "pattern": "group.*tier|tier.*group|choices.*tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-216-        formatter_class=argparse.RawDescriptionHelpFormatter,
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-217-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-218-    p_next.add_argument("--state", type=str, default=None, help="Path to state file")
desloppify/app/cli_support/parser_groups.py:219:    p_next.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=None, help="Show only this tier")
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-220-    p_next.add_argument(
desloppify/app/cli_support/parser_groups.py-221-        "--count", type=int, default=1, help="Number of items to show (default: 1)"
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-222-    )
--
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-234-    )
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-235-    p_next.add_argument(
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-236-        "--group",
desloppify/app/cli_support/parser_groups.py:237:        choices=["item", "file", "detector", "tier"],
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-238-        default="item",
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-239-        help="Group output by item, file, detector, or tier",
/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py-240-    )
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/plan.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
No matches found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_plan",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
No matches found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cluster_ux.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
22-            "file": "test.py",
23-            "summary": f"Finding {fid}",
24-            "confidence": "medium",
25:            "tier": 2,
26-            "detail": {},
27-        }
28-    return {"findings": findings, "scan_count": 5, "config": {}}
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_show_no_budget.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
No matches found
```

> AGENT

Let me also check the remaining test files that reference "tier" in a queue-ordering context, and the `helpers/display.py` new file.

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/display.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
No matches found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_status.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
103-class TestShowStructuralAreas:
104-    """show_structural_areas groups T3/T4 debt by area."""
105-
106:    def _make_finding(self, fid, *, file, tier, status="open"):
107-        return {
108-            "id": fid,
109-            "file": file,
110:            "tier": tier,
111-            "status": status,
112-            "detector": "test",
113-            "confidence": "medium",
--
118-        """Should produce no output when structural findings < 5."""
119-        state = {
120-            "findings": {
121:                "f1": self._make_finding("f1", file="src/a/foo.ts", tier=3),
122:                "f2": self._make_finding("f2", file="src/b/bar.ts", tier=4),
123-            }
124-        }
125-        show_structural_areas(state)
--
130-        state = {
131-            "findings": {
132-                f"f{i}": self._make_finding(
133:                    f"f{i}", file=f"src/area/{chr(97 + i)}.ts", tier=3
134-                )
135-                for i in range(6)
136-            }
--
145-        for i in range(3):
146-            fid = f"a{i}"
147-            findings[fid] = self._make_finding(
148:                fid, file=f"src/alpha/{chr(97 + i)}.ts", tier=3
149-            )
150-        for i in range(3):
151-            fid = f"b{i}"
152-            findings[fid] = self._make_finding(
153:                fid, file=f"src/beta/{chr(97 + i)}.ts", tier=4
154-            )
155-        state = {"findings": findings}
156-        show_structural_areas(state)
157-        out = capsys.readouterr().out
158-        assert "Structural Debt" in out
159-
160:    def test_excludes_non_structural_tiers(self, capsys):
161-        """T1 and T2 findings should not be counted."""
162-        findings = {}
163-        for i in range(10):
164-            fid = f"f{i}"
165:            findings[fid] = self._make_finding(fid, file=f"src/a/{i}.ts", tier=1)
166-        state = {"findings": findings}
167-        show_structural_areas(state)
168-        assert capsys.readouterr().out == ""
--
173-        for i in range(3):
174-            fid = f"a{i}"
175-            findings[fid] = self._make_finding(
176:                fid, file=f"src/alpha/{chr(97 + i)}.ts", tier=3, status="wontfix"
177-            )
178-        for i in range(3):
179-            fid = f"b{i}"
180-            findings[fid] = self._make_finding(
181:                fid, file=f"src/beta/{chr(97 + i)}.ts", tier=4, status="open"
182-            )
183-        state = {"findings": findings}
184-        show_structural_areas(state)
--
188-    def test_handles_empty_file_path_without_crashing(self, capsys):
189-        """Empty file paths should bucket into unknown area instead of crashing."""
190-        findings = {
191:            "a0": self._make_finding("a0", file="", tier=3),
192:            "a1": self._make_finding("a1", file="", tier=3),
193:            "a2": self._make_finding("a2", file="", tier=3),
194:            "b0": self._make_finding("b0", file="src/beta/a.ts", tier=4),
195:            "b1": self._make_finding("b1", file="src/beta/b.ts", tier=4),
196:            "b2": self._make_finding("b2", file="src/beta/c.ts", tier=4),
197-        }
198-        state = {"findings": findings}
199-        show_structural_areas(state)
--
252-            "Naming quality": {
253-                "score": 0.0,
254-                "strict": 0.0,
255:                "tier": 4,
256-                "issues": 0,
257-                "detectors": {"subjective_assessment": {}},
258-            },
259-            "Logic clarity": {
260-                "score": 0.0,
261-                "strict": 0.0,
262:                "tier": 4,
263-                "issues": 0,
264-                "detectors": {"subjective_assessment": {}},
265-            },
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_show.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
128-    """build_show_payload produces structured JSON for query and --output."""
129-
130-    def _make_finding(
131:        self, fid, *, file="a.ts", detector="unused", tier=2, confidence="high"
132-    ):
133-        return {
134-            "id": fid,
135-            "file": file,
136-            "detector": detector,
137:            "tier": tier,
138-            "confidence": confidence,
139-            "summary": f"Finding {fid}",
140-            "detail": {},
--
151-
152-class TestSuppressedMatchEstimate:
153-    def _make_finding(self, fid, *, file="a.ts", detector="unused",
154:                      tier=2, confidence="high"):
155-        return {
156-            "id": fid, "file": file, "detector": detector,
157:            "tier": tier, "confidence": confidence,
158-            "summary": f"Finding {fid}", "detail": {},
159-        }
160-
--
172-        result = build_show_payload(findings, "a.ts", "open")
173-        assert result["total"] == 1
174-        assert result["summary"]["files"] == 1
175:        assert result["summary"]["by_tier"] == {"T2": 1}
176-        assert result["summary"]["by_detector"] == {"unused": 1}
177-        assert "a.ts" in result["by_file"]
178-        assert len(result["by_file"]["a.ts"]) == 1
--
180-    def test_multiple_files_and_detectors(self):
181-        findings = [
182-            self._make_finding(
183:                "unused::a.ts::foo", file="a.ts", detector="unused", tier=2
184-            ),
185-            self._make_finding(
186:                "smells::b.ts::bar", file="b.ts", detector="smells", tier=3
187-            ),
188-            self._make_finding(
189:                "unused::a.ts::baz", file="a.ts", detector="unused", tier=2
190-            ),
191-        ]
192-        result = build_show_payload(findings, "*", "open")
193-        assert result["total"] == 3
194-        assert result["summary"]["files"] == 2
195:        assert result["summary"]["by_tier"] == {"T2": 2, "T3": 1}
196-        assert result["summary"]["by_detector"]["unused"] == 2
197-        assert result["summary"]["by_detector"]["smells"] == 1
198-
--
334-                        "kind": "finding",
335-                        "detector": "smells",
336-                        "file": "src/a.py",
337:                        "tier": 3,
338-                        "confidence": "medium",
339-                        "summary": "X",
340-                        "detail": {},
--
526-            "kind": "finding",
527-            "detector": "security",
528-            "file": "src/a.py",
529:            "tier": 4,
530-            "confidence": "high",
531-            "summary": "XSS vulnerability",
532-            "detail": {},
--
537-            "kind": "finding",
538-            "detector": "cycles",
539-            "file": "src/b.py",
540:            "tier": 4,
541-            "confidence": "medium",
542-            "summary": "Dependency cycle",
543-            "detail": {},
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_skip.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
38-            "status": status,
39-            "detector": "test",
40-            "file": "test.py",
41:            "tier": 1,
42-            "confidence": "high",
43-            "summary": f"Finding {fid}",
44-        }
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_auto_cluster.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
26-# Helpers
27-# ---------------------------------------------------------------------------
28-
29:def _finding(fid: str, detector: str = "unused", tier: int = 1,
30-             file: str = "test.py", detail: dict | None = None) -> dict:
31-    return {
32-        "id": fid,
33-        "detector": detector,
34-        "file": file,
35:        "tier": tier,
36-        "confidence": "high",
37-        "summary": f"Finding {fid}",
38-        "status": "open",
--
241-    assert "auto/unused" not in plan["clusters"]
242-
243-
244:def test_auto_cluster_no_tier_on_cluster():
245-    plan = empty_plan()
246-    state = _state_with(
247:        _finding("a", "unused", tier=2),
248:        _finding("b", "unused", tier=1),
249:        _finding("c", "unused", tier=3),
250-    )
251-    auto_cluster_findings(plan, state)
252:    # Clusters should not carry a tier field
253:    assert "tier" not in plan["clusters"]["auto/unused"]
254-
255-
256-# ---------------------------------------------------------------------------
--
270-    }
271-
272-    items = [
273:        {"id": "u1", "kind": "finding", "effective_tier": 1, "tier": 1,
274-         "detector": "unused", "confidence": "high", "detail": {}},
275:        {"id": "u2", "kind": "finding", "effective_tier": 1, "tier": 1,
276-         "detector": "unused", "confidence": "high", "detail": {}},
277:        {"id": "other", "kind": "finding", "effective_tier": 2, "tier": 2,
278-         "detector": "structural", "confidence": "medium", "detail": {}},
279-    ]
280-
--
301-    }
302-
303-    items = [
304:        {"id": "u1", "kind": "finding", "effective_tier": 1, "tier": 1,
305-         "detector": "unused", "confidence": "high", "detail": {}},
306-    ]
307-
--
316-        "member_count": 5, "id": "auto/unused",
317-    }
318-    finding_item = {
319:        "kind": "finding", "effective_tier": 1, "tier": 1,
320-        "confidence": "high", "detector": "unused", "detail": {},
321-        "id": "some-finding",
322-    }
--
373-
374-def test_build_work_queue_collapses_clusters():
375-    state = _state_with(
376:        _finding("u1", "unused", tier=1),
377:        _finding("u2", "unused", tier=1),
378-    )
379-    plan = empty_plan()
380-    auto_cluster_findings(plan, state)
--
394-
395-def test_build_work_queue_no_collapse_when_drilling():
396-    state = _state_with(
397:        _finding("u1", "unused", tier=1),
398:        _finding("u2", "unused", tier=1),
399-    )
400-    plan = empty_plan()
401-    auto_cluster_findings(plan, state)
--
474-    }
475-
476-    items = [
477:        {"id": "t1", "kind": "finding", "effective_tier": 1, "tier": 1,
478-         "detector": "test", "confidence": "high", "detail": {}},
479:        {"id": "t2", "kind": "finding", "effective_tier": 1, "tier": 1,
480-         "detector": "test", "confidence": "high", "detail": {}},
481-    ]
482-
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|tier_counts|available_tiers|selected_tier|requested_tier|no_tier_fallback|choose_fallback_tier|_item_matches_tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests",
  "output_mode": "files_with_matches",
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
Found 10 files
desloppify/tests/review/test_work_queue.py
desloppify/tests/plan/test_auto_cluster.py
desloppify/tests/commands/test_queue_progress.py
desloppify/tests/core/test_plan.py
desloppify/tests/commands/test_review_preflight.py
desloppify/tests/commands/test_direct_coverage_modules.py
desloppify/tests/commands/test_cmd_next.py
desloppify/tests/commands/test_cli.py
desloppify/tests/review/integration/test_work_queue.py
desloppify/tests/commands/test_direct_coverage_split_modules.py
```

> AGENT

Let me check the remaining test files that were flagged.

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|tier_counts|available_tiers|selected_tier|requested_tier|no_tier_fallback|choose_fallback_tier|_item_matches_tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
521-        )
522-        items = get_next_items(st, count=2)
523-        # Both are tier 3 — review findings use natural tier, not forced T1
524:        assert items[0]["effective_tier"] == 3
525:        assert items[1]["effective_tier"] == 3
526-
527-    def test_review_findings_reorder_by_confidence_then_review_weight(self):
528-        standard = _finding(
--
549-        items = get_next_items(st, count=2)
550-        # Same tier, confidence takes precedence: high before low
551-        assert [item["id"] for item in items] == ["a_review_mild", "z_review_critical"]
552:        assert all(item["effective_tier"] == 3 for item in items)
553-
554-    def test_tier1_mechanical_outranks_tier3_review(self):
555-        urgent = _finding("t1_urgent", detector="security", tier=1, confidence="high")
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|tier_counts|available_tiers|selected_tier|requested_tier|no_tier_fallback",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_review_preflight.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
41-    return {
42-        "items": items,
43-        "total": len(items),
44:        "tier_counts": {},
45:        "requested_tier": None,
46:        "selected_tier": None,
47-        "fallback_reason": None,
48:        "available_tiers": [],
49-        "grouped": {},
50-    }
51-
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|tier_counts|available_tiers|selected_tier|requested_tier|no_tier_fallback",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_modules.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
322-def test_build_query_payload_structure():
323-    """build_query_payload returns well-formed dict with queue metadata."""
324-    items = [{"id": "f1", "kind": "finding", "tier": 1}]
325:    queue = {"tier_counts": {1: 1}, "total": 1}
326-    payload = next_output.build_query_payload(
327-        queue, items, command="next", narrative=None
328-    )
```

> TOOL

tool_use Grep
```json
{
  "pattern": "effective_tier|tier_counts|available_tiers|selected_tier|requested_tier|no_tier_fallback",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_split_modules.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
65-
66-def test_item_sort_key_tier_ordering():
67-    """item_sort_key orders by tier (lower first)."""
68:    t1_item = {"tier": 1, "effective_tier": 1, "confidence": "high", "id": "a"}
69:    t3_item = {"tier": 3, "effective_tier": 3, "confidence": "high", "id": "b"}
70-    assert work_queue_ranking.item_sort_key(t1_item) < work_queue_ranking.item_sort_key(
71-        t3_item
72-    )
--
77-    review_t2 = {
78-        "is_review": True,
79-        "review_weight": 1.0,
80:        "effective_tier": 2,
81-        "tier": 2,
82-        "confidence": "high",
83-        "id": "r1",
84-    }
85:    t1_item = {"tier": 1, "effective_tier": 1, "confidence": "high", "id": "a"}
86-    # T1 mechanical sorts before T2 review
87-    assert work_queue_ranking.item_sort_key(t1_item) < work_queue_ranking.item_sort_key(
88-        review_t2
--
104-def test_group_queue_items_by_tier():
105-    """group_queue_items groups items by effective tier."""
106-    items = [
107:        {"effective_tier": 1, "tier": 1},
108:        {"effective_tier": 2, "tier": 2},
109:        {"effective_tier": 1, "tier": 1},
110-    ]
111-    grouped = work_queue_ranking.group_queue_items(items, "tier")
112-    assert len(grouped["T1"]) == 2
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
103-        bold = "**" if score_val < 93 else ""
104-        action = dimension_action_type(dim.name)
105-        lines.append(
106:            f"| {bold}{dim.name}{bold} | T{dim.tier} | "
107-            f"{checks:,} | {issues} | {score_val:.1f}% | {strict_val:.1f}% | {action} |"
108-        )
109-
--
130-        issues = ds.get("issues", 0)
131-        score_val = ds.get("score", 100)
132-        strict_val = ds.get("strict", score_val)
133:        tier = int(ds.get("tier", 3) or 3)
134-        bold = "**" if score_val < 93 else ""
135-        action = dimension_action_type(name)
136-        lines.append(
137:            f"| {bold}{name}{bold} | T{tier} | "
138-            f"{checks:,} | {issues} | {score_val:.1f}% | {strict_val:.1f}% | {action} |"
139-        )
140-
--
159-            issues = ds.get("issues", 0)
160-            score_val = ds.get("score", 100)
161-            strict_val = ds.get("strict", score_val)
162:            tier = ds.get("tier", 4)
163-            bold = "**" if score_val < 93 else ""
164-            lines.append(
165:                f"| {bold}{name}{bold} | T{tier} | "
166-                f"— | {issues} | {score_val:.1f}% | {strict_val:.1f}% | review |"
167-            )
168-
--
170-    return lines
171-
172-
173:def _plan_tier_sections(findings: dict, *, state: PlanState | None = None) -> list[str]:
174:    """Build per-tier sections from the shared work-queue backend."""
175-
176-    queue_state: PlanState | dict = state or {"findings": findings}
177-    scan_path = state.get("scan_path") if state else None
--
196-            status="open",
197-            include_subjective=True,
198-            subjective_threshold=subjective_threshold,
199:            no_tier_fallback=True,
200-        ),
201-    )
202-    open_items = queue.get("items", [])
203:    by_tier_file: dict[int, dict[str, list]] = defaultdict(lambda: defaultdict(list))
204-    for item in open_items:
205:        tier = int(item.get("effective_tier", item.get("tier", 3)))
206:        by_tier_file[tier][item.get("file", ".")].append(item)
207-
208-    lines: list[str] = []
209:    for tier_num in [1, 2, 3, 4]:
210:        tier_files = by_tier_file.get(tier_num, {})
211:        if not tier_files:
212-            continue
213-
214:        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
215:        tier_count = sum(len(file_findings) for file_findings in tier_files.values())
216-        lines.extend(
217-            [
218-                "---",
219:                f"## Tier {tier_num}: {label} ({tier_count} open)",
220-                "",
221-            ]
222-        )
223-
224-        sorted_files = sorted(
225:            tier_files.items(), key=lambda item: (-len(item[1]), item[0])
226-        )
227-        for filepath, file_items in sorted_files:
228-            display_path = "Codebase-wide" if filepath == "." else filepath
--
244-    return lines
245-
246-
247:def _tier_summary_lines(stats: dict) -> list[str]:
248-    lines: list[str] = []
249:    by_tier = stats.get("by_tier", {})
250:    for tier_num in [1, 2, 3, 4]:
251:        tier_stats = by_tier.get(str(tier_num), {})
252:        open_count = tier_stats.get("open", 0)
253:        total = sum(tier_stats.values())
254-        addressed = total - open_count
255-        pct = round(addressed / total * 100) if total else 100
256:        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
257-        lines.append(
258:            f"- **Tier {tier_num}** ({label}): {open_count} open / {total} total ({pct}% addressed)"
259-        )
260-    lines.append("")
261-    return lines
--
432-
433-def _render_plan_item(item: dict, override: dict) -> list[str]:
434-    """Render a single plan item as markdown lines."""
435:    tier = int(item.get("effective_tier", item.get("tier", 3)))
436-    confidence = item.get("confidence", "medium")
437-    summary = item.get("summary", "")
438-    item_id = item.get("id", "")
439-
440:    lines = [f"- [ ] [T{tier}/{confidence}] {summary}"]
441-    desc = override.get("description")
442-    if desc:
443-        lines.append(f"      → {desc}")
--
477-
478-    lines = _plan_header(state, stats)
479-    lines.extend(_plan_dimension_table(state))
480:    lines.extend(_tier_summary_lines(stats))
481-
482-    if has_plan:
483-        # Build full queue for item lookup
--
488-                scan_path=state.get("scan_path"),
489-                status="open",
490-                include_subjective=True,
491:                no_tier_fallback=True,
492-            ),
493-        )
494-        all_items = queue.get("items", [])
--
504-            lines.append(f"## Remaining (mechanical order, {len(remaining)} items)")
505-            lines.append("")
506-
507:        lines.extend(_plan_tier_sections(findings, state=state))
508-        lines.extend(_plan_skipped_section(all_items, plan))
509-        lines.extend(_plan_superseded_section(plan))
510-    else:
511:        lines.extend(_plan_tier_sections(findings, state=state))
512-
513-    lines.extend(_addressed_section(findings))
514-
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/guardrails.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
No matches found
```

> AGENT

Let me check the last few files I need for completeness -- the `TIER_LABELS` constant and the `_state/schema.py` `TierStats`.

> TOOL

tool_use Grep
```json
{
  "pattern": "TIER_LABELS",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify",
  "output_mode": "content",
  "-n": true,
  "-C": 3,
  "glob": "**/*.py"
}
```

> TOOL

tool_result Grep
```
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-1-"""Public plan API facade."""
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-2-
desloppify/engine/planning/core.py:3:from desloppify.engine.planning.common import CONFIDENCE_ORDER, TIER_LABELS
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-4-from desloppify.engine.planning.render import generate_plan_md
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-5-from desloppify.engine.planning.scan import generate_findings
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-6-from desloppify.engine.planning.select import get_next_item, get_next_items
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-7-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-8-__all__ = [
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-9-    "CONFIDENCE_ORDER",
desloppify/engine/planning/core.py:10:    "TIER_LABELS",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-11-    "generate_findings",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-12-    "generate_plan_md",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py-13-    "get_next_item",
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-4-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-5-from typing import Any
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-6-
desloppify/engine/planning/__init__.py:7:from desloppify.engine.planning.common import CONFIDENCE_ORDER, TIER_LABELS
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-8-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-9-
desloppify/engine/planning/__init__.py-10-def generate_plan_md(*args: Any, **kwargs: Any):
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-33-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-34-__all__ = [
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-35-    "CONFIDENCE_ORDER",
desloppify/engine/planning/__init__.py:36:    "TIER_LABELS",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-37-    "generate_findings",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-38-    "generate_plan_md",
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py-39-    "get_next_item",
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-7-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-8-from desloppify.core.exception_sets import PLAN_LOAD_EXCEPTIONS
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-9-from desloppify.core.registry import dimension_action_type
desloppify/engine/planning/render.py:10:from desloppify.engine.planning.common import TIER_LABELS
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-11-from desloppify.engine.planning.types import PlanState
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-12-from desloppify.engine.work_queue import QueueBuildOptions, build_work_queue
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-13-from desloppify.scoring import DIMENSIONS, DISPLAY_NAMES
--
desloppify/engine/planning/render.py-211-        if not tier_files:
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-212-            continue
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-213-
desloppify/engine/planning/render.py:214:        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-215-        tier_count = sum(len(file_findings) for file_findings in tier_files.values())
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-216-        lines.extend(
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-217-            [
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-253-        total = sum(tier_stats.values())
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-254-        addressed = total - open_count
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-255-        pct = round(addressed / total * 100) if total else 100
desloppify/engine/planning/render.py:256:        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-257-        lines.append(
desloppify/engine/planning/render.py-258-            f"- **Tier {tier_num}** ({label}): {open_count} open / {total} total ({pct}% addressed)"
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py-259-        )
--
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/common.py-2-
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/common.py-3-from __future__ import annotations
/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/common.py-4-
desloppify/engine/planning/common.py:5:TIER_LABELS = {
desloppify/engine/planning/common.py-6-    1: "Highest priority (auto-fixable + high-confidence holistic review)",
desloppify/engine/planning/common.py-7-    2: "Quick fixes (unused vars, dead exports, exact dupes, orphaned files, cross-tool imports)",
desloppify/engine/planning/common.py-8-    3: "Needs judgment (smells, near-dupes, single-use, small cycles, state sync)",
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_modules.py-100-        plan_select.get_next_items,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_modules.py-101-        plan_select.get_next_item,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_modules.py-102-    )
desloppify/tests/commands/test_direct_coverage_modules.py:103:    assert isinstance(plan_common.TIER_LABELS, dict)
desloppify/tests/commands/test_direct_coverage_modules.py:104:    assert 1 in plan_common.TIER_LABELS
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_modules.py-105-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_modules.py-106-
desloppify/tests/commands/test_direct_coverage_modules.py-107-def test_smoke_commands():
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-6-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-7-from desloppify.engine.planning.core import (
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-8-    CONFIDENCE_ORDER,
desloppify/tests/core/test_plan.py:9:    TIER_LABELS,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-10-    generate_plan_md,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-11-    get_next_item,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-12-    get_next_items,
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-76-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-77-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-78-# ===========================================================================
desloppify/tests/core/test_plan.py:79:# TIER_LABELS and CONFIDENCE_ORDER constants
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-80-# ===========================================================================
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-81-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-82-
desloppify/tests/core/test_plan.py-83-class TestConstants:
desloppify/tests/core/test_plan.py-84-    def test_tier_labels_covers_1_through_4(self):
desloppify/tests/core/test_plan.py:85:        assert set(TIER_LABELS.keys()) == {1, 2, 3, 4}
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-86-
desloppify/tests/core/test_plan.py-87-    def test_confidence_order_ranking(self):
/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py-88-        assert CONFIDENCE_ORDER["high"] < CONFIDENCE_ORDER["medium"]
```

> TOOL

tool_use Grep
```json
{
  "pattern": "TierStats|by_tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/engine/_state/schema.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
14-    "ConcernDismissal",
15-    "FindingStatus",
16-    "Finding",
17:    "TierStats",
18-    "StateStats",
19-    "DimensionScore",
20-    "ScanHistoryEntry",
--
66-    zone: NotRequired[str]
67-
68-
69:class TierStats(TypedDict, total=False):
70-    open: int
71-    fixed: int
72-    auto_resolved: int
--
81-    auto_resolved: int
82-    wontfix: int
83-    false_positive: int
84:    by_tier: dict[str, TierStats]
85-
86-
87-class DimensionScore(TypedDict, total=False):
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/subjective.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
No matches found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tier",
  "path": "/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_subjective_actionability_gate.py",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result Grep
```
No matches found
```

> AGENT

Now I have a comprehensive picture. Let me compile the complete report.

---

Here is the exhaustive inventory of all tier-based queue ordering references in the `desloppify/` source tree (excluding `.claude/worktrees/` copies). I have organized the results by category.

---

## 1. `effective_tier` (field name, variable, dict key)

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py`

**Line 55-57** -- Set on every finding item during `build_finding_items()`:
```python
        item["effective_tier"] = (
            4 if item["is_subjective"] else int(finding.get("tier", 3))
        )
```

**Line 107** -- Used in `item_sort_key()` for subjective items:
```python
            int(item.get("effective_tier", 4)),
```

**Line 116** -- Used in `item_sort_key()` for non-subjective items:
```python
        int(item.get("effective_tier", item.get("tier", 3))),
```

**Line 126** -- Local variable in `item_explain()`:
```python
    effective_tier = int(item.get("effective_tier", item.get("tier", 3)))
```

**Line 131** -- Returned in the explain dict for subjective_dimension items:
```python
            "effective_tier": effective_tier,
```

**Line 159** -- Returned in the explain dict for regular findings:
```python
        "effective_tier": effective_tier,
```

**Line 183** -- In `tier_counts()` for cluster members:
```python
                tier = int(member.get("effective_tier", member.get("tier", 3)))
```

**Line 186** -- In `tier_counts()` for non-cluster items:
```python
        tier = int(item.get("effective_tier", item.get("tier", 3)))
```

**Line 207** -- In `group_queue_items()` for `group == "tier"` branch:
```python
            key = f"T{int(item.get('effective_tier', item.get('tier', 3)))}"
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 215** -- In `_item_matches_tier()` for cluster members:
```python
            int(m.get("effective_tier", m.get("tier", 3))) == tier
```

**Line 218** -- In `_item_matches_tier()` for non-cluster items:
```python
    return int(item.get("effective_tier", item.get("tier", 3))) == tier
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py`

**Line 337** -- In `build_subjective_items()` synthetic item construction:
```python
                "effective_tier": 4,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py`

**Line 73** -- In `_render_grouped_items()`:
```python
            tier = int(item.get("effective_tier", item.get("tier", 3)))
```

**Line 183** -- In single-item render:
```python
    tier = int(item.get("effective_tier", item.get("tier", 3)))
```

**Line 416** -- In `_render_compact_item()`:
```python
    tier = int(item.get("effective_tier", item.get("tier", 3)))
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/output.py`

**Line 35** -- In `serialize_item()`:
```python
        "effective_tier": item.get("effective_tier", item.get("tier")),
```

**Line 127** -- In `format_md_table()`:
```python
        tier = int(item.get("effective_tier", item.get("tier", 3)))
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py`

**Line 26** -- In `_cluster_tier_label()`:
```python
    tiers = {int(m.get("effective_tier", m.get("tier", 3))) for m in members}
```

**Line 130** -- In queue table row building:
```python
            tier_val = int(item.get("effective_tier", item.get("tier", 3)))
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py`

**Line 205** -- In `_plan_tier_sections()`:
```python
        tier = int(item.get("effective_tier", item.get("tier", 3)))
```

**Line 435** -- In `_render_plan_item()`:
```python
    tier = int(item.get("effective_tier", item.get("tier", 3)))
```

---

## 2. `tier_counts` (function and dict key)

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py`

**Line 177-188** -- Function definition:
```python
def tier_counts(items: list[dict]) -> dict[int, int]:
    counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for item in items:
        if item.get("kind") == "cluster":
            for member in item.get("members", []):
                tier = int(member.get("effective_tier", member.get("tier", 3)))
                counts[tier] = counts.get(tier, 0) + 1
            continue
        tier = int(item.get("effective_tier", item.get("tier", 3)))
        counts[tier] = counts.get(tier, 0) + 1
    return counts
```

**Line 222** -- In `__all__`:
```python
    "tier_counts",
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 22** -- Import:
```python
    tier_counts,
```

**Line 52** -- In `WorkQueueResult` TypedDict:
```python
    tier_counts: dict[int, int]
```

**Line 408** -- Called in `build_work_queue()`:
```python
    counts = tier_counts(all_items)
```

**Line 451** -- Returned in result:
```python
        "tier_counts": counts,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py`

**Line 49** -- Import:
```python
    tier_counts,
```

**Line 77** -- In `__all__`:
```python
    "tier_counts",
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py`

**Line 50** -- Used in `_render_tier_navigator()`:
```python
    counts = queue.get("tier_counts", {})
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/output.py`

**Line 77** -- In `build_query_payload()`:
```python
        "tier_counts": queue.get("tier_counts", {}),
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py`

**Line 49** -- Parameter of `_print_queue_header()`:
```python
    tier_counts: dict,
```

**Line 82** -- Passed to `format_queue_headline()`:
```python
        tier_counts=dict(tier_counts),
```

**Line 175** -- Extracted from queue result:
```python
    tier_counts = queue.get("tier_counts", {})
```

**Line 190** -- Passed to `_print_queue_header()`:
```python
        tier_counts=tier_counts,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py`

**Line 24** -- In `QueueBreakdown` dataclass:
```python
    tier_counts: dict[int, int] = field(default_factory=dict)
```

**Line 49** -- Extracted from queue result:
```python
    tier_counts = dict(result.get("tier_counts", {}))
```

**Line 93** -- Passed to breakdown:
```python
        tier_counts=tier_counts,
```

**Line 127-134** -- Used in `format_queue_headline()`:
```python
    tc = breakdown.tier_counts
    tier_parts = []
    for t in (1, 2, 3, 4):
        c = tc.get(t, 0)
        if c > 0:
            tier_parts.append(f"T{t}:{c}")
    if tier_parts:
        segments.append(" ".join(tier_parts))
```

---

## 3. `available_tiers`

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 56** -- In `WorkQueueResult` TypedDict:
```python
    available_tiers: list[int]
```

**Line 447** -- Computed:
```python
    available_tiers = [tier for tier, value in counts.items() if value > 0]
```

**Line 455** -- Returned:
```python
        "available_tiers": available_tiers,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py`

**Line 371** -- Used in `render_queue_header()`:
```python
    available = queue.get("available_tiers", [])
```

**Line 373-374** -- Used to format hint:
```python
        tiers = ", ".join(f"T{tier_num}" for tier_num in available)
        print(colorize(f"  explain: available tiers are {tiers}", "dim"))
```

**Line 405** -- Used in `show_empty_queue()`:
```python
        available = queue.get("available_tiers", [])
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/output.py`

**Line 81** -- In `build_query_payload()`:
```python
        "available_tiers": queue.get("available_tiers", []),
```

---

## 4. `selected_tier`

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 54** -- In `WorkQueueResult` TypedDict:
```python
    selected_tier: int | None
```

**Line 413** -- Initialized:
```python
    selected_tier = requested_tier
```

**Line 426** -- Updated during fallback:
```python
                selected_tier = chosen
```

**Line 453** -- Returned:
```python
        "selected_tier": selected_tier,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/output.py`

**Line 79** -- In `build_query_payload()`:
```python
        "selected_tier": queue.get("selected_tier"),
```

---

## 5. `requested_tier`

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 53** -- In `WorkQueueResult` TypedDict:
```python
    requested_tier: int | None
```

**Line 410-412** -- Computed from options:
```python
    requested_tier = (
        int(resolved_options.tier) if resolved_options.tier is not None else None
    )
```

**Lines 417, 421, 433, 437** -- Used in tier filtering and fallback messages:
```python
    if requested_tier is not None:
        ...if _item_matches_tier(item, requested_tier)...
        ...f"Requested T{requested_tier} has 0 open -> showing T{chosen} "...
        ...f"Requested T{requested_tier} has 0 open."...
```

**Line 452** -- Returned:
```python
        "requested_tier": requested_tier,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/output.py`

**Line 78** -- In `build_query_payload()`:
```python
        "requested_tier": queue.get("requested_tier"),
```

---

## 6. `no_tier_fallback`

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 39** -- In `QueueBuildOptions` dataclass:
```python
    no_tier_fallback: bool = False
```

**Line 423** -- Used in `build_work_queue()`:
```python
        if not filtered and not resolved_options.no_tier_fallback:
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next.py`

**Line 180** -- Extracted from CLI args:
```python
    no_tier_fallback = bool(getattr(args, "no_tier_fallback", False))
```

**Line 213** -- Passed to `QueueBuildOptions`:
```python
            no_tier_fallback=no_tier_fallback,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py`

**Line 253-255** -- CLI argument:
```python
        "--no-tier-fallback",
        action="store_true",
        help="Do not auto-fallback to another tier when --tier has no items",
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/scope.py`

**Line 207** -- Hardcoded to True:
```python
            no_tier_fallback=True,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py`

**Line 199** -- Hardcoded to True:
```python
            no_tier_fallback=True,
```

**Line 491** -- Hardcoded to True:
```python
                no_tier_fallback=True,
```

---

## 7. `choose_fallback_tier`

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py`

**Line 191-195** -- Function definition:
```python
def choose_fallback_tier(requested_tier: int, counts: dict[int, int]) -> int | None:
    available = [tier for tier, count in counts.items() if count > 0]
    if not available:
        return None
    return min(available, key=lambda tier: (abs(tier - requested_tier), tier))
```

**Line 219** -- In `__all__`:
```python
    "choose_fallback_tier",
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 18** -- Import:
```python
    choose_fallback_tier,
```

**Line 424** -- Called:
```python
            chosen = choose_fallback_tier(requested_tier, counts)
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/work_queue.py`

**Line 45** -- Import:
```python
    choose_fallback_tier,
```

**Line 73** -- In `__all__`:
```python
    "choose_fallback_tier",
```

---

## 8. `_item_matches_tier`

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 211-218** -- Function definition:
```python
def _item_matches_tier(item: dict, tier: int) -> bool:
    """Check if an item (or any of its members for clusters) matches a tier."""
    if item.get("kind") == "cluster":
        return any(
            int(m.get("effective_tier", m.get("tier", 3))) == tier
            for m in item.get("members", [])
        )
    return int(item.get("effective_tier", item.get("tier", 3))) == tier
```

**Line 421** -- Called for tier filtering:
```python
            if _item_matches_tier(item, requested_tier)
```

**Line 430** -- Called for fallback filtering:
```python
                    if _item_matches_tier(item, chosen)
```

---

## 9. `--tier` CLI argument

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups.py`

**Line 219** -- On the `next` subcommand:
```python
    p_next.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=None, help="Show only this tier")
```

**Line 237** -- In `--group` choices:
```python
        choices=["item", "file", "detector", "tier"],
```

**Line 239** -- Help text:
```python
        help="Group output by item, file, detector, or tier",
```

**Line 213** -- In examples:
```python
  desloppify next --tier 1              # only tier 1
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/cli_support/parser_groups_admin.py`

**Line 508** -- On `plan queue` subcommand:
```python
    p_queue.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=None,
                         help="Show only items in this tier (T1=critical .. T4=cosmetic)")
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next.py`

**Line 174** -- Reads from args:
```python
    tier = getattr(args, "tier", None)
```

**Line 206** -- Passed to `QueueBuildOptions`:
```python
            tier=tier,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py`

**Line 152** -- Reads from args:
```python
    tier_filter = getattr(args, "tier", None)
```

**Line 163** -- Passed to `QueueBuildOptions`:
```python
            tier=tier_filter,
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 31** -- In `QueueBuildOptions`:
```python
    tier: int | None = None
```

**Lines 401, 411** -- Used:
```python
        and resolved_options.tier is None
...
        int(resolved_options.tier) if resolved_options.tier is not None else None
```

---

## 10. "T1", "T2", "T3", "T4" in queue ordering / priority context (strings)

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py`

**Line 108** -- Comment:
```python
            1,  # Subjective items sort after mechanical items within T4.
```

**Lines 134-135** -- Policy string:
```python
                "Subjective dimensions are always queued as T4 and do not outrank "
                "mechanical T1/T2/T3 items."
```

**Line 146** -- Ranking factor string:
```python
        ranking_factors = ["tier fixed to T4", "subjective_score asc", "id asc"]
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/core.py`

**Line 433** -- Fallback reason:
```python
                    f"Requested T{requested_tier} has 0 open -> showing T{chosen} "
```

**Line 437** -- No-fallback reason:
```python
            fallback_reason = f"Requested T{requested_tier} has 0 open."
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py`

**Lines 61-62** -- Tier Navigator help text:
```python
            "    Switch: `desloppify next --tier 1` | `desloppify next --tier 2` | "
            "`desloppify next --tier 3` | `desloppify next --tier 4`",
```

**Line 77** -- Grouped item label:
```python
                f"    {_tier_label(tier)} [{item.get('confidence', 'medium')}]{tag_str} {item.get('summary', '')}"
```

**Line 185** -- Single item display:
```python
    print(colorize(f"  (Tier {tier}, {confidence} confidence)", "bold"))
```

**Line 333** -- Explain text:
```python
            f"ranked by tier={tier}, confidence={confidence}, "
```

**Lines 373-374** -- Available tiers hint:
```python
        tiers = ", ".join(f"T{tier_num}" for tier_num in available)
        print(colorize(f"  explain: available tiers are {tiers}", "dim"))
```

**Line 404** -- Empty queue "Requested tier" label:
```python
        print(colorize(f"  Requested tier: T{tier}", "dim"))
```

**Lines 407-408** -- Try hint:
```python
                f"desloppify next --tier {tier_num}" for tier_num in available
```

**Line 421** -- Compact item:
```python
    print(f"  [{idx + 1}/{total}] {_tier_label(tier)}{tag_str} {item.get('summary', '')}")
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/output.py`

**Line 131** -- Markdown table row:
```python
        lines.append(f"| {kind} | T{tier} | {conf} | {summary} | {command} |")
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py`

**Line 29-30** -- Cluster tier labels:
```python
        return f"T{lo}"
    return f"T{lo}-T{hi}"
```

**Line 131** -- Regular item tier string:
```python
            tier_str = f"T{tier_val}"
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/helpers/queue_progress.py`

**Lines 131-132** -- Headline tier parts:
```python
            tier_parts.append(f"T{t}:{c}")
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py`

**Line 172** -- Docstring:
```python
    """Build a synthetic T1 work item for ``synthesis::pending`` if it's in the queue.
```

---

## 11. "tier asc" / "tier fixed" in ranking factor strings

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py`

**Line 137** -- Subjective dimension explain:
```python
            "ranking_factors": ["tier asc", "subjective_score asc", "id asc"],
```

**Line 146** -- Subjective finding explain:
```python
        ranking_factors = ["tier fixed to T4", "subjective_score asc", "id asc"]
```

**Line 149** -- Review finding explain:
```python
            "tier asc",
```

**Line 156** -- Regular finding explain:
```python
        ranking_factors = ["tier asc", "confidence asc", "count desc", "id asc"]
```

---

## 12. `group == "tier"` branch in `group_queue_items`

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/ranking.py`

**Lines 206-207**:
```python
        elif group == "tier":
            key = f"T{int(item.get('effective_tier', item.get('tier', 3)))}"
```

---

## 13. Tier Navigator rendering

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py`

**Lines 45-46** -- Helper function:
```python
def _tier_label(tier: int) -> str:
    return f"T{tier}"
```

**Lines 49-65** -- Full Tier Navigator renderer:
```python
def _render_tier_navigator(queue: dict) -> None:
    counts = queue.get("tier_counts", {})
    print(colorize("\n  Tier Navigator", "bold"))
    print(
        colorize(
            "    "
            + "  ".join(f"T{t}: {counts.get(t, 0)}" for t in (1, 2, 3, 4)),
            "dim",
        )
    )
    print(
        colorize(
            "    Switch: `desloppify next --tier 1` | `desloppify next --tier 2` | "
            "`desloppify next --tier 3` | `desloppify next --tier 4`",
            "dim",
        )
    )
```

**Line 365** -- Called from `render_queue_header()`:
```python
    _render_tier_navigator(queue)
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py`

**Lines 377-411** -- `show_empty_queue()` has a `tier` parameter:
```python
def show_empty_queue(
    queue: dict,
    tier: int | None,
    strict: float | None,
    ...
```

and at line 403-410 uses it:
```python
    if tier is not None:
        print(colorize(f"  Requested tier: T{tier}", "dim"))
        available = queue.get("available_tiers", [])
        if available:
            commands = " | ".join(
                f"desloppify next --tier {tier_num}" for tier_num in available
            )
            print(colorize(f"  Try: {commands}", "dim"))
```

---

## 14. `show_tier_progress_table` (status command)

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_parts/render.py`

**Lines 35-56** -- The function definition (uses `by_tier` from state stats, NOT queue ordering, but still tier-based display):
```python
def show_tier_progress_table(by_tier: dict) -> None:
    """Fallback display when dimension scores are unavailable."""
    rows = []
    for tier_num in [1, 2, 3, 4]:
        ts = by_tier.get(str(tier_num), {})
        ...
        rows.append([f"Tier {tier_num}", bar, f"{strict_pct}%", ...])
```

**Line 636** -- In `__all__`:
```python
    "show_tier_progress_table",
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_cmd.py`

**Line 38** -- Imported:
```python
    show_tier_progress_table,
```

**Line 164** -- Called:
```python
        show_tier_progress_table(by_tier)
```

---

## 15. `TIER_LABELS` constant

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/common.py`

**Line 5-9** -- Definition:
```python
TIER_LABELS = {
    1: "Highest priority (auto-fixable + high-confidence holistic review)",
    2: "Quick fixes (unused vars, dead exports, exact dupes, orphaned files, cross-tool imports)",
    3: "Needs judgment (smells, near-dupes, single-use, small cycles, state sync)",
    ...
```

Imported/re-exported by:
- `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/__init__.py` (line 7, 36)
- `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/core.py` (line 3, 10)
- `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py` (line 10)

Used in render.py at lines 214, 256.

---

## 16. `_cluster_tier_label` (plan queue render)

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/plan/queue_render.py`

**Lines 21-30**:
```python
def _cluster_tier_label(item: dict) -> str:
    """Compute a tier label from cluster members, e.g. 'T2' or 'T1-T3'."""
    members = item.get("members", [])
    if not members:
        return ""
    tiers = {int(m.get("effective_tier", m.get("tier", 3))) for m in members}
    lo, hi = min(tiers), max(tiers)
    if lo == hi:
        return f"T{lo}"
    return f"T{lo}-T{hi}"
```

**Line 119** -- Called:
```python
            tier_str = _cluster_tier_label(item)
```

---

## 17. `_plan_tier_sections` and `_tier_summary_lines` (plan markdown render)

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/planning/render.py`

**Lines 173-244** -- `_plan_tier_sections()` builds per-tier markdown sections using `effective_tier` and `TIER_LABELS`.

**Lines 247-261** -- `_tier_summary_lines()` builds per-tier progress summary lines.

Both referenced at lines 480, 507, 511.

---

## 18. Test files with tier-based queue ordering references

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/test_work_queue.py`

Tests: `test_tier_fallback_selects_nearest_non_empty_tier`, `test_no_tier_fallback_returns_empty_with_reason`, `test_review_finding_uses_natural_tier`, `test_review_items_ranked_by_tier_like_mechanical`, `test_review_items_sort_by_issue_weight_within_tier`, `test_tier4_queue_contains_mechanical_and_synthetic_subjective_items`, `test_available_tiers_reflects_populated_tiers`, `test_queue_build_options_defaults`. Lines 46-518.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/integration/test_work_queue.py`

Duplicate/integration copy of the above tests. Same test names, lines 46-542.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cmd_next.py`

Tests: `test_tier_navigator_always_printed` (line 86), `test_tier_fallback_message_and_payload` (line 124), `test_no_tier_fallback_strict_empty_guidance` (line 174). Many assertions on `tier_counts`, `requested_tier`, `selected_tier`, `available_tiers`, `effective_tier`. Lines 14-762.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cli.py`

Tests: `test_next_with_tier_and_count` (line 150), `test_next_with_explain_and_no_tier_fallback` (line 174). Verify `--tier` and `--no-tier-fallback` arg parsing.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_queue_progress.py`

Tests on `QueueBreakdown.tier_counts` and `format_queue_headline()` tier display: `test_headline_basic_tiers` (line 79), `test_headline_with_plan_and_skipped` (line 88), `test_headline_omits_zero_segments` (line 105), `test_headline_singular_item` (line 125), and more through line 347.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/plan/test_auto_cluster.py`

Tests: `test_auto_cluster_no_tier_on_cluster` (line 244), `test_build_work_queue_collapses_clusters` (line 374), `test_build_work_queue_no_collapse_when_drilling` (line 395). Many test items have `effective_tier` and `tier` fields at lines 273-481.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/core/test_plan.py`

Tests: `TestConstants.test_tier_labels_covers_1_through_4` (line 84), plus `effective_tier` assertions at lines 524-552.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_review_preflight.py`

Uses `tier_counts`, `requested_tier`, `selected_tier`, `available_tiers` in mock queue data at lines 41-48.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_modules.py`

Asserts `TIER_LABELS` is a dict (line 103). Also has `tier_counts` in mock data (line 325).

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_direct_coverage_split_modules.py`

Tests: `test_item_sort_key_tier_ordering` (line 66), `test_group_queue_items_by_tier` (line 104). Uses `effective_tier` in test data.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_queue_order_guard.py`

Has finding data with `"tier": 1` at line 22.

### `/Users/user_c042661f/Documents/desloppify/desloppify/tests/commands/test_cluster_ux.py`

Has finding data with `"tier": 2` at line 25.

---

## 19. Additional related references

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/next_parts/render.py`

**Line 333** -- Explain text includes `tier=`:
```python
            f"ranked by tier={tier}, confidence={confidence}, "
```

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/render.py`

Uses `finding['tier']` for display purposes (not queue ordering) at lines 59, 134, 161-172. The show command displays `T{tier}` labels and groups `by_tier`.

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/show/payload.py`

Uses `finding["tier"]` for summary at lines 28-39, 47.

### `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/status_parts/render.py`

**Line 236** -- Shows `T{dim.tier}` in dimension scorecard table (this is dimension metadata tier, not queue ordering):
```python
            f"  {dim.name:<22} {checks_str}  {score_val:5.1f}%  {strict_val:5.1f}%  {bar}  T{dim.tier}  {action}{focus}"
```

**Lines 512-540** -- `show_structural_areas` filters by `f["tier"] in (3, 4)` and sums `f["tier"]` for weighting.

### `/Users/user_c042661f/Documents/desloppify/desloppify/engine/_work_queue/helpers.py`

**Line 195** -- Synthesis item carries `"tier": 1`:
```python
        "tier": 1,
```

**Lines 242, 336-337** -- Subjective items carry `"tier": 4` and `"effective_tier": 4`.

---

## Summary of all files touched (main source tree only)

| File | Categories |
|------|-----------|
| `desloppify/engine/_work_queue/ranking.py` | effective_tier, tier_counts, choose_fallback_tier, group=="tier", "tier asc"/"tier fixed", T1-T4 strings |
| `desloppify/engine/_work_queue/core.py` | effective_tier, tier_counts, available_tiers, selected_tier, requested_tier, no_tier_fallback, choose_fallback_tier, _item_matches_tier, --tier (QueueBuildOptions.tier) |
| `desloppify/engine/_work_queue/helpers.py` | effective_tier, tier metadata on synth items |
| `desloppify/engine/work_queue.py` | Re-exports: choose_fallback_tier, tier_counts |
| `desloppify/app/cli_support/parser_groups.py` | --tier arg, --no-tier-fallback arg, --group choices incl "tier" |
| `desloppify/app/cli_support/parser_groups_admin.py` | --tier arg on plan queue |
| `desloppify/app/commands/next.py` | Reads tier, no_tier_fallback from args, passes to QueueBuildOptions |
| `desloppify/app/commands/next_parts/render.py` | effective_tier, tier_counts, available_tiers, _tier_label, _render_tier_navigator, show_empty_queue, T1-T4 strings |
| `desloppify/app/commands/next_parts/output.py` | effective_tier, tier_counts, requested_tier, selected_tier, available_tiers |
| `desloppify/app/commands/plan/queue_render.py` | effective_tier, tier_counts, _cluster_tier_label, tier_filter |
| `desloppify/app/commands/helpers/queue_progress.py` | tier_counts in QueueBreakdown, T1-T4 format strings |
| `desloppify/app/commands/show/scope.py` | no_tier_fallback=True |
| `desloppify/app/commands/status_parts/render.py` | show_tier_progress_table, T{dim.tier} display |
| `desloppify/app/commands/status_cmd.py` | Imports/calls show_tier_progress_table |
| `desloppify/engine/planning/common.py` | TIER_LABELS definition |
| `desloppify/engine/planning/render.py` | effective_tier, TIER_LABELS, _plan_tier_sections, _tier_summary_lines, no_tier_fallback |
| `desloppify/engine/planning/__init__.py` | Re-exports TIER_LABELS |
| `desloppify/engine/planning/core.py` | Re-exports TIER_LABELS |
| `desloppify/tests/review/test_work_queue.py` | Tests for tier fallback, tier filtering, effective_tier, available_tiers, tier_counts |
| `desloppify/tests/review/integration/test_work_queue.py` | Integration tier tests |
| `desloppify/tests/commands/test_cmd_next.py` | Tests for tier navigator, fallback, no_tier_fallback |
| `desloppify/tests/commands/test_cli.py` | Tests for --tier and --no-tier-fallback parsing |
| `desloppify/tests/commands/test_queue_progress.py` | Tests for tier_counts in QueueBreakdown |
| `desloppify/tests/plan/test_auto_cluster.py` | Tests with effective_tier, tier fields |
| `desloppify/tests/core/test_plan.py` | Tests for TIER_LABELS, effective_tier |
| `desloppify/tests/commands/test_review_preflight.py` | Mock queue with tier_counts, requested_tier etc |
| `desloppify/tests/commands/test_direct_coverage_modules.py` | TIER_LABELS smoke test, tier_counts mock |
| `desloppify/tests/commands/test_direct_coverage_split_modules.py` | Tests for item_sort_key tier ordering, group_queue_items by tier |

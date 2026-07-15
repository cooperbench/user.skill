> DEVELOPER

I need to understand how desloppify's review batch system creates batches. The user ran `review --prepare` which produced 9 "investigation batches", then `--dry-run` expanded those into 46 prompt files. The user expected one batch per dimension.

Search the codebase for:
1. How batches are created/split in the review batch system — look in `desloppify/app/commands/review/batch/` 
2. How dimensions map to batches — is there grouping logic that combines dimensions?
3. What causes sub-batch splitting (the 9 → 46 expansion)
4. The "Full Codebase Sweep" batch type specifically — why would there be 20 of those?

Focus on files in:
- `desloppify/app/commands/review/batch/`
- `desloppify/app/commands/review/prepare.py`
- Any dimension/scope related files

Report back the key functions and logic that control batch creation and splitting.

> AGENT

I'll search the codebase to understand how the review batch system creates and splits batches. Let me start by exploring the key files you mentioned.

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/app/commands/review/batch/*.py"
}
```

> TOOL

tool_result Glob
```
<tool_use_error>Sibling tool call errored</tool_use_error>
```

> TOOL

tool_use Glob
```json
{
  "pattern": "desloppify/app/commands/review/*.py"
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
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review"
}
```

> TOOL

tool_result Read
```
EISDIR: illegal operation on a directory, read [REDACTED]
```

> AGENT

Let me use bash to list the directory structure:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review -type f -name \"*.py\" | head -20",
  "description": "List Python files in review command directory"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/_runner_parallel_types.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/runner_packets.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/runner_parallel.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/coordinator.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/merge.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/cmd.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/state_payloads.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/runner_process.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/_runner_parallel_progress.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/_runner_process_attempts.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/assessment_integrity.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/runner_failures.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/runtime/policy.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/runtime/setup.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batches_runtime.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prompt_sections.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/_runner_process_io.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/_runner_parallel_execution.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/merge.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch -type f -name \"*.py\"",
  "description": "List all Python files in batch subdirectory"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/merge.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/scoring.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/__init__.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/core.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/orchestrator.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/scope.py
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/prompt_template.py
```

> AGENT

Good! Now let me read the key files. I'll start with the core batch files and prepare.py:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/core.py"
}
```

> TOOL

tool_result Read
```
1→"""Core batch processing helpers for holistic review workflows."""
     2→
     3→from __future__ import annotations
     4→
     5→import json
     6→from dataclasses import dataclass
     7→from pathlib import Path
     8→from typing import NotRequired, TypedDict, cast
     9→
    10→from desloppify.intelligence.review.feedback_contract import (
    11→    DIMENSION_NOTE_ISSUES_KEY,
    12→    HIGH_SCORE_ISSUES_NOTE_THRESHOLD,
    13→    LEGACY_DIMENSION_NOTE_ISSUES_KEY,
    14→    LEGACY_REVIEW_QUALITY_HIGH_SCORE_MISSING_ISSUES_KEY,
    15→    LOW_SCORE_ISSUE_THRESHOLD,
    16→    REVIEW_QUALITY_HIGH_SCORE_MISSING_ISSUES_KEY,
    17→)
    18→from desloppify.intelligence.review.importing.contracts_types import (
    19→    ReviewIssuePayload,
    20→)
    21→from desloppify.intelligence.review.importing.contracts_validation import (
    22→    validate_review_issue_payload,
    23→)
    24→from desloppify.intelligence.review.importing.payload import (
    25→    normalize_legacy_findings_alias,
    26→)
    27→from desloppify.intelligence.review.issue_merge import (
    28→    merge_list_fields,
    29→    normalize_word_set,
    30→    pick_longer_text,
    31→    track_merged_from,
    32→)
    33→
    34→from .prompt_template import render_batch_prompt
    35→from .scoring import DimensionMergeScorer
    36→
    37→_DIMENSION_SCORER = DimensionMergeScorer()
    38→
    39→
    40→class BatchIssuePayload(ReviewIssuePayload, total=False):  # type: ignore[call-arg]
    41→    """Normalized issue payload passed across batch merge/import seams."""
    42→
    43→    impact_scope: str
    44→    fix_scope: str
    45→
    46→
    47→class BatchDimensionNotePayload(TypedDict, total=False):
    48→    """Normalized per-dimension evidence and scoring context."""
    49→
    50→    evidence: list[str]
    51→    impact_scope: str
    52→    fix_scope: str
    53→    confidence: str
    54→    issues_preventing_higher_score: str
    55→    sub_axes: dict[str, float]
    56→
    57→
    58→class BatchQualityPayload(TypedDict, total=False):
    59→    """Quality telemetry attached to each normalized batch output."""
    60→
    61→    dimension_coverage: float
    62→    evidence_density: float
    63→    high_score_missing_issue_note: float
    64→    high_score_without_risk: NotRequired[float]
    65→
    66→
    67→class BatchResultPayload(TypedDict):
    68→    """Canonical normalized batch payload consumed by merge routines."""
    69→
    70→    assessments: dict[str, float]
    71→    issues: list[BatchIssuePayload]
    72→    dimension_notes: dict[str, BatchDimensionNotePayload]
    73→    quality: BatchQualityPayload
    74→
    75→
    76→@dataclass(frozen=True)
    77→class NormalizedBatchIssue:
    78→    """Typed internal issue contract for normalized batch payloads."""
    79→
    80→    dimension: str
    81→    identifier: str
    82→    summary: str
    83→    confidence: str
    84→    suggestion: str
    85→    related_files: list[str]
    86→    evidence: list[str]
    87→    impact_scope: str
    88→    fix_scope: str
    89→    reasoning: str = ""
    90→    evidence_lines: list[int] | None = None
    91→
    92→    def to_payload(self) -> BatchIssuePayload:
    93→        payload: BatchIssuePayload = {  # type: ignore[assignment]
    94→            "dimension": self.dimension,
    95→            "identifier": self.identifier,
    96→            "summary": self.summary,
    97→            "confidence": self.confidence,
    98→            "suggestion": self.suggestion,
    99→            "related_files": list(self.related_files),
   100→            "evidence": list(self.evidence),
   101→            "impact_scope": self.impact_scope,
   102→            "fix_scope": self.fix_scope,
   103→        }
   104→        if self.reasoning:
   105→            payload["reasoning"] = self.reasoning
   106→        if self.evidence_lines:
   107→            payload["evidence_lines"] = list(self.evidence_lines)
   108→        return payload
   109→
   110→
   111→def parse_batch_selection(raw: str | None, batch_count: int) -> list[int]:
   112→    """Parse optional 1-based CSV list of batches."""
   113→    if not raw:
   114→        return list(range(batch_count))
   115→
   116→    selected: list[int] = []
   117→    seen: set[int] = set()
   118→    for token in raw.split(","):
   119→        text = token.strip()
   120→        if not text:
   121→            continue
   122→        idx_1 = int(text)
   123→        if idx_1 < 1 or idx_1 > batch_count:
   124→            raise ValueError(f"batch index {idx_1} out of range 1..{batch_count}")
   125→        idx_0 = idx_1 - 1
   126→        if idx_0 in seen:
   127→            continue
   128→        seen.add(idx_0)
   129→        selected.append(idx_0)
   130→    return selected
   131→
   132→
   133→def extract_json_payload(raw: str, *, log_fn) -> dict[str, object] | None:
   134→    """Best-effort extraction of first JSON object from agent output text."""
   135→    text = raw.strip()
   136→    if not text:
   137→        return None
   138→
   139→    decoder = json.JSONDecoder()
   140→    last_decode_error: json.JSONDecodeError | None = None
   141→    for start, ch in enumerate(text):
   142→        if ch not in "{[":
   143→            continue
   144→        try:
   145→            obj, _ = decoder.raw_decode(text[start:])
   146→        except json.JSONDecodeError as exc:
   147→            last_decode_error = exc
   148→            continue
   149→        if (
   150→            isinstance(obj, dict)
   151→            and isinstance(obj.get("assessments"), dict)
   152→            and isinstance(obj.get("issues"), list)
   153→        ):
   154→            return obj
   155→    if last_decode_error is not None:
   156→        log_fn(f"  batch output JSON parse failed: {last_decode_error.msg}")
   157→    else:
   158→        log_fn("  batch output JSON parse failed: no valid payload found")
   159→    return None
   160→
   161→
   162→def _validate_dimension_note(
   163→    key: str,
   164→    note_raw: object,
   165→) -> tuple[list[object], str, str, str, str]:
   166→    """Validate a single dimension_notes entry and return parsed fields.
   167→
   168→    Returns (evidence, impact_scope, fix_scope, confidence, issues_preventing_higher_score).
   169→    Raises ValueError on invalid structure.
   170→    """
   171→    if not isinstance(note_raw, dict):
   172→        raise ValueError(
   173→            f"dimension_notes missing object for assessed dimension: {key}"
   174→        )
   175→    evidence = note_raw.get("evidence")
   176→    impact_scope = note_raw.get("impact_scope")
   177→    fix_scope = note_raw.get("fix_scope")
   178→    if not isinstance(evidence, list) or not evidence:
   179→        raise ValueError(
   180→            f"dimension_notes.{key}.evidence must be a non-empty array"
   181→        )
   182→    if not isinstance(impact_scope, str) or not impact_scope.strip():
   183→        raise ValueError(
   184→            f"dimension_notes.{key}.impact_scope must be a non-empty string"
   185→        )
   186→    if not isinstance(fix_scope, str) or not fix_scope.strip():
   187→        raise ValueError(
   188→            f"dimension_notes.{key}.fix_scope must be a non-empty string"
   189→        )
   190→
   191→    confidence_raw = str(note_raw.get("confidence", "medium")).strip().lower()
   192→    confidence = (
   193→        confidence_raw if confidence_raw in {"high", "medium", "low"} else "medium"
   194→    )
   195→    issues_note = str(note_raw.get(DIMENSION_NOTE_ISSUES_KEY, "")).strip()
   196→    if not issues_note:
   197→        issues_note = str(note_raw.get(LEGACY_DIMENSION_NOTE_ISSUES_KEY, "")).strip()
   198→    return evidence, impact_scope, fix_scope, confidence, issues_note
   199→
   200→
   201→def _normalize_abstraction_sub_axes(
   202→    note_raw: dict[str, object],
   203→    abstraction_sub_axes: tuple[str, ...],
   204→) -> dict[str, float]:
   205→    """Extract and clamp abstraction_fitness sub-axis scores from a note."""
   206→    sub_axes_raw = note_raw.get("sub_axes")
   207→    if sub_axes_raw is not None and not isinstance(sub_axes_raw, dict):
   208→        raise ValueError(
   209→            "dimension_notes.abstraction_fitness.sub_axes must be an object"
   210→        )
   211→    if not isinstance(sub_axes_raw, dict):
   212→        return {}
   213→
   214→    normalized: dict[str, float] = {}
   215→    for axis in abstraction_sub_axes:
   216→        axis_value = sub_axes_raw.get(axis)
   217→        if axis_value is None:
   218→            continue
   219→        if isinstance(axis_value, bool) or not isinstance(
   220→            axis_value, int | float
   221→        ):
   222→            raise ValueError(
   223→                f"dimension_notes.abstraction_fitness.sub_axes.{axis} "
   224→                "must be numeric"
   225→            )
   226→        normalized[axis] = round(
   227→            max(0.0, min(100.0, float(axis_value))),
   228→            1,
   229→        )
   230→    return normalized
   231→
   232→
   233→def _normalize_issues(
   234→    raw_issues: object,
   235→    dimension_notes: dict[str, BatchDimensionNotePayload],
   236→    *,
   237→    max_batch_issues: int,
   238→    allowed_dims: set[str],
   239→    low_score_dimensions: set[str] | None = None,
   240→) -> list[NormalizedBatchIssue]:
   241→    """Validate and normalize the issues array from a batch payload."""
   242→    if not isinstance(raw_issues, list):
   243→        raise ValueError("issues must be an array")
   244→
   245→    issues: list[NormalizedBatchIssue] = []
   246→    errors: list[str] = []
   247→    for idx, item in enumerate(raw_issues):
   248→        issue: ReviewIssuePayload | None
   249→        issue, issue_errors = validate_review_issue_payload(
   250→            item,
   251→            label=f"issues[{idx}]",
   252→            allowed_dimensions=allowed_dims,
   253→            allow_dismissed=False,
   254→        )
   255→        if issue_errors:
   256→            errors.extend(issue_errors)
   257→            continue
   258→        if issue is None:
   259→            raise ValueError(
   260→                "batch issue payload missing after validation succeeded"
   261→            )
   262→
   263→        dim = issue["dimension"]
   264→        note = dimension_notes.get(dim, {})
   265→        impact_scope = str(
   266→            (item if isinstance(item, dict) else {}).get(
   267→                "impact_scope", note.get("impact_scope", "")
   268→            )
   269→        ).strip()
   270→        fix_scope = str(
   271→            (item if isinstance(item, dict) else {}).get(
   272→                "fix_scope", note.get("fix_scope", "")
   273→            )
   274→        ).strip()
   275→        if not impact_scope or not fix_scope:
   276→            errors.append(
   277→                f"issues[{idx}] requires impact_scope and fix_scope "
   278→                "(or dimension_notes defaults)"
   279→            )
   280→            continue
   281→        issues.append(
   282→            NormalizedBatchIssue(
   283→                dimension=issue["dimension"],
   284→                identifier=issue["identifier"],
   285→                summary=issue["summary"],
   286→                confidence=issue["confidence"],
   287→                suggestion=issue["suggestion"],
   288→                related_files=list(issue.get("related_files", [])),
   289→                evidence=list(issue.get("evidence", [])),
   290→                impact_scope=impact_scope,
   291→                fix_scope=fix_scope,
   292→                reasoning=str(issue.get("reasoning", "")),
   293→                evidence_lines=list(issue.get("evidence_lines", []))
   294→                if isinstance(issue.get("evidence_lines"), list)
   295→                else None,
   296→            )
   297→        )
   298→    if errors:
   299→        visible = errors[:10]
   300→        remaining = len(errors) - len(visible)
   301→        if remaining > 0:
   302→            visible.append(f"... {remaining} additional issue schema error(s) omitted")
   303→        raise ValueError("; ".join(visible))
   304→    if len(issues) <= max_batch_issues:
   305→        return issues
   306→
   307→    required_dims = set(low_score_dimensions or set())
   308→    if not required_dims:
   309→        return issues[:max_batch_issues]
   310→
   311→    # Preserve at least one issue per low-score dimension before trimming.
   312→    selected: list[NormalizedBatchIssue] = []
   313→    selected_indexes: set[int] = set()
   314→    covered: set[str] = set()
   315→    for idx, issue in enumerate(issues):
   316→        if len(selected) >= max_batch_issues:
   317→            break
   318→        dim = issue.dimension.strip()
   319→        if dim not in required_dims or dim in covered:
   320→            continue
   321→        selected.append(issue)
   322→        selected_indexes.add(idx)
   323→        covered.add(dim)
   324→
   325→    for idx, issue in enumerate(issues):
   326→        if len(selected) >= max_batch_issues:
   327→            break
   328→        if idx in selected_indexes:
   329→            continue
   330→        selected.append(issue)
   331→    return selected
   332→
   333→
   334→def _low_score_dimensions(assessments: dict[str, float]) -> set[str]:
   335→    """Return assessed dimensions requiring explicit defect issues."""
   336→    return {
   337→        dim
   338→        for dim, score in assessments.items()
   339→        if score < LOW_SCORE_ISSUE_THRESHOLD
   340→    }
   341→
   342→
   343→def _enforce_low_score_issues(
   344→    *,
   345→    assessments: dict[str, float],
   346→    issues: list[NormalizedBatchIssue],
   347→) -> None:
   348→    """Fail closed when low scores do not report explicit issues."""
   349→    required_dims = _low_score_dimensions(assessments)
   350→    if not required_dims:
   351→        return
   352→    issue_dims = {
   353→        issue.dimension.strip() for issue in issues
   354→    }
   355→    missing = sorted(dim for dim in required_dims if dim not in issue_dims)
   356→    if not missing:
   357→        return
   358→    joined = ", ".join(missing)
   359→    raise ValueError(
   360→        "low-score dimensions must include at least one explicit issue: "
   361→        f"{joined} (threshold {LOW_SCORE_ISSUE_THRESHOLD:.1f})"
   362→    )
   363→
   364→
   365→def _compute_batch_quality(
   366→    assessments: dict[str, float],
   367→    issues: list[NormalizedBatchIssue],
   368→    dimension_notes: dict[str, BatchDimensionNotePayload],
   369→    high_score_missing_issue_note: float,
   370→) -> BatchQualityPayload:
   371→    """Compute quality metrics for a single batch result."""
   372→    return {
   373→        "dimension_coverage": round(
   374→            len(assessments) / max(len(assessments), 1),
   375→            3,
   376→        ),
   377→        "evidence_density": round(
   378→            sum(len(note.get("evidence", [])) for note in dimension_notes.values())
   379→            / max(len(issues), 1),
   380→            3,
   381→        ),
   382→        "high_score_missing_issue_note": high_score_missing_issue_note,
   383→    }
   384→
   385→
   386→def normalize_batch_result(
   387→    payload: dict[str, object],
   388→    allowed_dims: set[str],
   389→    *,
   390→    max_batch_issues: int,
   391→    abstraction_sub_axes: tuple[str, ...],
   392→) -> tuple[
   393→    dict[str, float],
   394→    list[BatchIssuePayload],
   395→    dict[str, BatchDimensionNotePayload],
   396→    BatchQualityPayload,
   397→]:
   398→    """Validate and normalize one batch payload."""
   399→    if "assessments" not in payload:
   400→        raise ValueError("payload missing required key: assessments")
   401→    key_error = normalize_legacy_findings_alias(
   402→        payload,
   403→        missing_issues_error="payload missing required key: issues",
   404→    )
   405→    if key_error is not None:
   406→        raise ValueError(key_error)
   407→
   408→    raw_assessments = payload.get("assessments")
   409→    if not isinstance(raw_assessments, dict):
   410→        raise ValueError("assessments must be an object")
   411→
   412→    raw_dimension_notes = payload.get("dimension_notes", {})
   413→    if not isinstance(raw_dimension_notes, dict):
   414→        raise ValueError("dimension_notes must be an object")
   415→
   416→    assessments: dict[str, float] = {}
   417→    dimension_notes: dict[str, BatchDimensionNotePayload] = {}
   418→    high_score_missing_issue_note = 0.0
   419→    for key, value in raw_assessments.items():
   420→        if not isinstance(key, str) or not key:
   421→            continue
   422→        if key not in allowed_dims:
   423→            continue
   424→        if isinstance(value, bool):
   425→            continue
   426→        if not isinstance(value, int | float):
   427→            continue
   428→        score = round(max(0.0, min(100.0, float(value))), 1)
   429→
   430→        note_raw = raw_dimension_notes.get(key)
   431→        evidence, impact_scope, fix_scope, confidence, issues_note = (
   432→            _validate_dimension_note(key, note_raw)
   433→        )
   434→        if not isinstance(note_raw, dict):
   435→            raise ValueError(
   436→                f"dimension_notes missing object for assessed dimension: {key}"
   437→            )
   438→        if score > HIGH_SCORE_ISSUES_NOTE_THRESHOLD and not issues_note:
   439→            high_score_missing_issue_note += 1
   440→
   441→        normalized_sub_axes: dict[str, float] = {}
   442→        if key == "abstraction_fitness":
   443→            normalized_sub_axes = _normalize_abstraction_sub_axes(
   444→                note_raw, abstraction_sub_axes
   445→            )
   446→
   447→        assessments[key] = score
   448→        dimension_notes[key] = {
   449→            "evidence": [str(item).strip() for item in evidence if str(item).strip()],
   450→            "impact_scope": impact_scope.strip(),
   451→            "fix_scope": fix_scope.strip(),
   452→            "confidence": confidence,
   453→            "issues_preventing_higher_score": issues_note,
   454→        }
   455→        if normalized_sub_axes:
   456→            dimension_notes[key]["sub_axes"] = normalized_sub_axes
   457→
   458→    issues = _normalize_issues(
   459→        payload.get("issues"),
   460→        dimension_notes,
   461→        max_batch_issues=max_batch_issues,
   462→        allowed_dims=allowed_dims,
   463→        low_score_dimensions=_low_score_dimensions(assessments),
   464→    )
   465→    _enforce_low_score_issues(assessments=assessments, issues=issues)
   466→
   467→    quality = _compute_batch_quality(
   468→        assessments,
   469→        issues,
   470→        dimension_notes,
   471→        high_score_missing_issue_note,
   472→    )
   473→    return (
   474→        assessments,
   475→        [issue.to_payload() for issue in issues],
   476→        dimension_notes,
   477→        quality,
   478→    )
   479→
   480→
   481→def assessment_weight(
   482→    *,
   483→    dimension: str,
   484→    issues: list[BatchIssuePayload],
   485→    dimension_notes: dict[str, BatchDimensionNotePayload],
   486→) -> float:
   487→    """Evidence-weighted assessment score weight with a neutral floor.
   488→
   489→    Weighting is evidence-based and score-independent: the raw score does not
   490→    influence how much weight a batch contributes during merge.
   491→    """
   492→    note = dimension_notes.get(dimension, {})
   493→    note_evidence = len(note.get("evidence", [])) if isinstance(note, dict) else 0
   494→    issue_count = sum(
   495→        1
   496→        for issue in issues
   497→        if str(issue.get("dimension", "")).strip() == dimension
   498→    )
   499→    return float(1 + note_evidence + issue_count)
   500→
   501→
   502→def _issue_pressure_by_dimension(
   503→    issues: list[BatchIssuePayload],
   504→    *,
   505→    dimension_notes: dict[str, BatchDimensionNotePayload],
   506→) -> tuple[dict[str, float], dict[str, int]]:
   507→    """Summarize how strongly issues should pull dimension scores down."""
   508→    return _DIMENSION_SCORER.issue_pressure_by_dimension(
   509→        issues,
   510→        dimension_notes=dimension_notes,
   511→    )
   512→
   513→
   514→def _accumulate_batch_scores(
   515→    result: BatchResultPayload,
   516→    *,
   517→    score_buckets: dict[str, list[tuple[float, float]]],
   518→    score_raw_by_dim: dict[str, list[float]],
   519→    merged_dimension_notes: dict[str, BatchDimensionNotePayload],
   520→    abstraction_axis_scores: dict[str, list[tuple[float, float]]],
   521→    abstraction_sub_axes: tuple[str, ...],
   522→) -> None:
   523→    """Accumulate assessment scores, dimension notes, and sub-axis data from one batch."""
   524→    result_issues = result.get("issues", [])
   525→    result_notes = result.get("dimension_notes", {})
   526→    for key, score in result.get("assessments", {}).items():
   527→        if isinstance(score, bool):
   528→            continue
   529→        score_value = float(score)
   530→        weight = assessment_weight(
   531→            dimension=key,
   532→            issues=result_issues,
   533→            dimension_notes=result_notes,
   534→        )
   535→        score_buckets.setdefault(key, []).append((score_value, weight))
   536→        score_raw_by_dim.setdefault(key, []).append(score_value)
   537→
   538→        note = result_notes.get(key)
   539→        existing = merged_dimension_notes.get(key)
   540→        existing_evidence = (
   541→            len(existing.get("evidence", [])) if isinstance(existing, dict) else -1
   542→        )
   543→        current_evidence = (
   544→            len(note.get("evidence", [])) if isinstance(note, dict) else -1
   545→        )
   546→        if current_evidence > existing_evidence and note is not None:
   547→            merged_dimension_notes[key] = note
   548→
   549→        if key == "abstraction_fitness" and isinstance(note, dict):
   550→            sub_axes = note.get("sub_axes")
   551→            if isinstance(sub_axes, dict):
   552→                for axis in abstraction_sub_axes:
   553→                    axis_score = sub_axes.get(axis)
   554→                    if isinstance(axis_score, bool) or not isinstance(
   555→                        axis_score, int | float
   556→                    ):
   557→                        continue
   558→                    abstraction_axis_scores[axis].append(
   559→                        (float(axis_score), weight)
   560→                    )
   561→
   562→
   563→def _issue_identity_key(issue: BatchIssuePayload) -> str:
   564→    """Build a stable concept key; prefer dimension+identifier when available."""
   565→    dim = str(issue.get("dimension", "")).strip()
   566→    ident = str(issue.get("identifier", "")).strip()
   567→    if ident:
   568→        return f"{dim}::{ident}"
   569→    summary = str(issue.get("summary", "")).strip()
   570→    summary_terms = sorted(normalize_word_set(summary))
   571→    if summary_terms:
   572→        return f"{dim}::summary::{','.join(summary_terms[:8])}"
   573→    return f"{dim}::{summary}"
   574→
   575→
   576→def _merge_issue_payload(
   577→    existing: BatchIssuePayload, incoming: BatchIssuePayload
   578→) -> None:
   579→    """Merge two concept-equivalent issues into the existing payload."""
   580→    merge_list_fields(existing, incoming, ("related_files", "evidence"))
   581→    # Prefer richer summary/suggestion text when they differ.
   582→    pick_longer_text(existing, incoming, "summary")
   583→    pick_longer_text(existing, incoming, "suggestion")
   584→    track_merged_from(existing, str(incoming.get("identifier", "")).strip())
   585→
   586→
   587→def _should_merge_issues(
   588→    existing: BatchIssuePayload, incoming: BatchIssuePayload
   589→) -> bool:
   590→    """Check whether two key-matched issues are similar enough to merge."""
   591→    existing_summary = normalize_word_set(str(existing.get("summary", "")))
   592→    incoming_summary = normalize_word_set(str(incoming.get("summary", "")))
   593→    if existing_summary and incoming_summary:
   594→        overlap = len(existing_summary & incoming_summary)
   595→        union = len(existing_summary | incoming_summary)
   596→        if union and overlap / union >= 0.3:
   597→            return True
   598→    # Fall back to related-file overlap
   599→    existing_files = set(cast(list[str], existing.get("related_files", [])))
   600→    incoming_files = set(cast(list[str], incoming.get("related_files", [])))
   601→    if existing_files and incoming_files:
   602→        return bool(existing_files & incoming_files)
   603→    # When no corroborating signal is available, allow merge
   604→    return not existing_summary or not incoming_summary
   605→
   606→
   607→def _accumulate_batch_quality(
   608→    result: BatchResultPayload,
   609→    *,
   610→    coverage_values: list[float],
   611→    evidence_density_values: list[float],
   612→) -> float:
   613→    """Accumulate quality metrics from one batch. Returns high-score-missing-issues delta."""
   614→    quality: object = result.get("quality", {})
   615→    if not isinstance(quality, dict):
   616→        return 0.0
   617→    coverage = quality.get("dimension_coverage")
   618→    density = quality.get("evidence_density")
   619→    missing_issue_note = quality.get(REVIEW_QUALITY_HIGH_SCORE_MISSING_ISSUES_KEY)
   620→    if not isinstance(missing_issue_note, int | float):
   621→        missing_issue_note = quality.get(
   622→            LEGACY_REVIEW_QUALITY_HIGH_SCORE_MISSING_ISSUES_KEY
   623→        )
   624→    if isinstance(coverage, int | float):
   625→        coverage_values.append(float(coverage))
   626→    if isinstance(density, int | float):
   627→        evidence_density_values.append(float(density))
   628→    return (
   629→        float(missing_issue_note)
   630→        if isinstance(missing_issue_note, int | float)
   631→        else 0.0
   632→    )
   633→
   634→
   635→def _compute_merged_assessments(
   636→    score_buckets: dict[str, list[tuple[float, float]]],
   637→    score_raw_by_dim: dict[str, list[float]],
   638→    issue_pressure_by_dim: dict[str, float],
   639→    issue_count_by_dim: dict[str, int],
   640→) -> dict[str, float]:
   641→    """Compute pressure-adjusted weighted mean for each dimension."""
   642→    return _DIMENSION_SCORER.merge_scores(
   643→        score_buckets,
   644→        score_raw_by_dim,
   645→        issue_pressure_by_dim,
   646→        issue_count_by_dim,
   647→    )
   648→
   649→
   650→def _compute_abstraction_components(
   651→    merged_assessments: dict[str, float],
   652→    abstraction_axis_scores: dict[str, list[tuple[float, float]]],
   653→    *,
   654→    abstraction_sub_axes: tuple[str, ...],
   655→    abstraction_component_names: dict[str, str],
   656→) -> dict[str, float] | None:
   657→    """Compute weighted abstraction sub-axis component scores.
   658→
   659→    Returns component_scores dict, or None if abstraction_fitness is not assessed.
   660→    """
   661→    abstraction_score = merged_assessments.get("abstraction_fitness")
   662→    if abstraction_score is None:
   663→        return None
   664→
   665→    component_scores: dict[str, float] = {}
   666→    for axis in abstraction_sub_axes:
   667→        weighted = abstraction_axis_scores.get(axis, [])
   668→        if not weighted:
   669→            continue
   670→        numerator = sum(score * weight for score, weight in weighted)
   671→        denominator = sum(weight for _, weight in weighted)
   672→        if denominator <= 0:
   673→            continue
   674→        component_scores[abstraction_component_names[axis]] = round(
   675→            max(0.0, min(100.0, numerator / denominator)),
   676→            1,
   677→        )
   678→    return component_scores if component_scores else None
   679→
   680→
   681→def merge_batch_results(
   682→    batch_results: list[BatchResultPayload],
   683→    *,
   684→    abstraction_sub_axes: tuple[str, ...],
   685→    abstraction_component_names: dict[str, str],
   686→) -> dict[str, object]:
   687→    """Deterministically merge assessments/issues across batch outputs."""
   688→    from .merge import merge_batch_results as _merge_batch_results
   689→
   690→    return _merge_batch_results(
   691→        batch_results,
   692→        abstraction_sub_axes=abstraction_sub_axes,
   693→        abstraction_component_names=abstraction_component_names,
   694→    )
   695→
   696→
   697→def build_batch_prompt(
   698→    *,
   699→    repo_root: Path,
   700→    packet_path: Path,
   701→    batch_index: int,
   702→    batch: dict[str, object],
   703→) -> str:
   704→    """Render one subagent prompt for a holistic investigation batch."""
   705→    return render_batch_prompt(
   706→        repo_root=repo_root,
   707→        packet_path=packet_path,
   708→        batch_index=batch_index,
   709→        batch=batch,
   710→    )
   711→
   712→
   713→__all__ = [
   714→    "assessment_weight",
   715→    "build_batch_prompt",
   716→    "extract_json_payload",
   717→    "merge_batch_results",
   718→    "normalize_batch_result",
   719→    "parse_batch_selection",
   720→]
   721→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/orchestrator.py"
}
```

> TOOL

tool_result Read
```
1→"""Batch runner helpers and orchestration for review command."""
     2→
     3→from __future__ import annotations
     4→
     5→import json
     6→import subprocess
     7→import sys
     8→from pathlib import Path
     9→from typing import cast
    10→
    11→from desloppify.app.commands.helpers.query import write_query_best_effort
    12→from desloppify.base.coercions import coerce_positive_int
    13→from desloppify.base.discovery.file_paths import safe_write_text
    14→from desloppify.base.exception_sets import CommandError, PacketValidationError
    15→from desloppify.base.output.terminal import colorize, log
    16→import desloppify.intelligence.narrative.core as narrative_mod
    17→from desloppify.intelligence import review as review_mod
    18→from desloppify.intelligence.review.feedback_contract import (
    19→    max_batch_issues_for_dimension_count,
    20→)
    21→
    22→from ..helpers import parse_dimensions
    23→from ..importing.cmd import do_import as _do_import
    24→from ..packet.policy import coerce_review_batch_file_limit, redacted_review_config
    25→from ..runner_failures import print_failures, print_failures_and_raise
    26→from ..runner_packets import (
    27→    build_batch_import_provenance,
    28→    build_blind_packet,
    29→    prepare_run_artifacts,
    30→    run_stamp,
    31→    selected_batch_indexes,
    32→    write_packet_snapshot,
    33→)
    34→from ..runner_parallel import collect_batch_results, execute_batches
    35→from ..runner_process import (
    36→    CodexBatchRunnerDeps,
    37→    FollowupScanDeps,
    38→    run_codex_batch,
    39→    run_followup_scan,
    40→)
    41→from ..runtime.setup import setup_lang_concrete as _setup_lang
    42→from ..runtime_paths import (
    43→    blind_packet_path as _blind_packet_path,
    44→)
    45→from ..runtime_paths import (
    46→    review_packet_dir as _review_packet_dir,
    47→)
    48→from ..runtime_paths import (
    49→    runtime_project_root as _runtime_project_root,
    50→)
    51→from ..runtime_paths import (
    52→    subagent_runs_dir as _subagent_runs_dir,
    53→)
    54→from . import core as batch_core_mod
    55→from . import execution as review_batches_mod
    56→
    57→FOLLOWUP_SCAN_TIMEOUT_SECONDS = 45 * 60
    58→ABSTRACTION_SUB_AXES = (
    59→    "abstraction_leverage",
    60→    "indirection_cost",
    61→    "interface_honesty",
    62→    "delegation_density",
    63→    "definition_directness",
    64→    "type_discipline",
    65→)
    66→ABSTRACTION_COMPONENT_NAMES = {
    67→    "abstraction_leverage": "Abstraction Leverage",
    68→    "indirection_cost": "Indirection Cost",
    69→    "interface_honesty": "Interface Honesty",
    70→    "delegation_density": "Delegation Density",
    71→    "definition_directness": "Definition Directness",
    72→    "type_discipline": "Type Discipline",
    73→}
    74→
    75→
    76→
    77→def _merge_batch_results(batch_results: list[object]) -> dict[str, object]:
    78→    """Deterministically merge assessments/issues across batch outputs."""
    79→    normalized_results: list[batch_core_mod.BatchResultPayload] = []
    80→    for result in batch_results:
    81→        if hasattr(result, "to_dict") and callable(result.to_dict):
    82→            payload = result.to_dict()
    83→            if isinstance(payload, dict):
    84→                normalized_results.append(cast(batch_core_mod.BatchResultPayload, payload))
    85→                continue
    86→        if isinstance(result, dict):
    87→            normalized_results.append(cast(batch_core_mod.BatchResultPayload, result))
    88→    return batch_core_mod.merge_batch_results(
    89→        normalized_results,
    90→        abstraction_sub_axes=ABSTRACTION_SUB_AXES,
    91→        abstraction_component_names=ABSTRACTION_COMPONENT_NAMES,
    92→    )
    93→
    94→
    95→def _load_or_prepare_packet(
    96→    args,
    97→    *,
    98→    state: dict,
    99→    lang,
   100→    config: dict,
   101→    stamp: str,
   102→) -> tuple[dict, Path, Path]:
   103→    """Load packet override or prepare a fresh packet snapshot."""
   104→    packet_override = getattr(args, "packet", None)
   105→    if packet_override:
   106→        packet_path = Path(packet_override)
   107→        if not packet_path.exists():
   108→            raise PacketValidationError(f"packet not found: {packet_override}", exit_code=1)
   109→        try:
   110→            packet = json.loads(packet_path.read_text())
   111→        except (OSError, json.JSONDecodeError) as exc:
   112→            raise PacketValidationError(f"reading packet: {exc}", exit_code=1) from exc
   113→        blind_path = _blind_packet_path()
   114→        blind_packet = build_blind_packet(packet)
   115→        safe_write_text(blind_path, json.dumps(blind_packet, indent=2) + "\n")
   116→        print(colorize(f"  Immutable packet: {packet_path}", "dim"))
   117→        print(colorize(f"  Blind packet: {blind_path}", "dim"))
   118→        return packet, packet_path, blind_path
   119→
   120→    path = Path(args.path)
   121→    dims = parse_dimensions(args)
   122→    dimensions = list(dims) if dims else None
   123→    retrospective = bool(getattr(args, "retrospective", False))
   124→    retrospective_max_issues = coerce_positive_int(
   125→        getattr(args, "retrospective_max_issues", None),
   126→        default=30,
   127→        minimum=1,
   128→    )
   129→    retrospective_max_batch_items = coerce_positive_int(
   130→        getattr(args, "retrospective_max_batch_items", None),
   131→        default=20,
   132→        minimum=1,
   133→    )
   134→    lang_run, found_files = _setup_lang(lang, path, config)
   135→    lang_name = lang_run.name
   136→    narrative = narrative_mod.compute_narrative(
   137→        state,
   138→        context=narrative_mod.NarrativeContext(lang=lang_name, command="review"),
   139→    )
   140→
   141→    blind_path = _blind_packet_path()
   142→    packet = review_mod.prepare_holistic_review(
   143→        path,
   144→        lang_run,
   145→        state,
   146→        options=review_mod.HolisticReviewPrepareOptions(
   147→            dimensions=dimensions,
   148→            files=found_files or None,
   149→            max_files_per_batch=coerce_review_batch_file_limit(config),
   150→            include_issue_history=retrospective,
   151→            issue_history_max_issues=retrospective_max_issues,
   152→            issue_history_max_batch_items=retrospective_max_batch_items,
   153→        ),
   154→    )
   155→    packet["config"] = redacted_review_config(config)
   156→    packet["narrative"] = narrative
   157→    next_command = "desloppify review --prepare"
   158→    if retrospective:
   159→        next_command += (
   160→            " --retrospective"
   161→            f" --retrospective-max-issues {retrospective_max_issues}"
   162→            f" --retrospective-max-batch-items {retrospective_max_batch_items}"
   163→        )
   164→    packet["next_command"] = next_command
   165→    write_query_best_effort(
   166→        packet,
   167→        context="review packet query update",
   168→    )
   169→    packet_path, blind_saved = write_packet_snapshot(
   170→        packet,
   171→        stamp=stamp,
   172→        review_packet_dir=_review_packet_dir(),
   173→        blind_path=blind_path,
   174→        safe_write_text_fn=safe_write_text,
   175→    )
   176→    print(colorize(f"  Immutable packet: {packet_path}", "dim"))
   177→    print(colorize(f"  Blind packet: {blind_saved}", "dim"))
   178→    return packet, packet_path, blind_saved
   179→
   180→
   181→def do_run_batches(args, state, lang, state_file, config: dict | None = None) -> None:
   182→    """Run holistic investigation batches with a local subagent runner."""
   183→    from ..runtime.policy import resolve_batch_run_policy
   184→
   185→    runtime_project_root = _runtime_project_root()
   186→    policy = resolve_batch_run_policy(args)
   187→    batch_timeout_seconds = policy.batch_timeout_seconds
   188→    batch_max_retries = policy.batch_max_retries
   189→    batch_retry_backoff_seconds = policy.batch_retry_backoff_seconds
   190→    batch_heartbeat_seconds = policy.heartbeat_seconds
   191→    batch_live_log_interval_seconds = (
   192→        max(1.0, min(batch_heartbeat_seconds, 10.0))
   193→        if batch_heartbeat_seconds > 0
   194→        else 5.0
   195→    )
   196→    batch_stall_kill_seconds = policy.stall_kill_seconds
   197→
   198→    def _prepare_run_artifacts(*, stamp, selected_indexes, batches, packet_path, run_root, repo_root):
   199→        return prepare_run_artifacts(
   200→            stamp=stamp,
   201→            selected_indexes=selected_indexes,
   202→            batches=batches,
   203→            packet_path=packet_path,
   204→            run_root=run_root,
   205→            repo_root=repo_root,
   206→            build_prompt_fn=batch_core_mod.build_batch_prompt,
   207→            safe_write_text_fn=safe_write_text,
   208→            colorize_fn=colorize,
   209→        )
   210→
   211→    def _collect_batch_results(*, selected_indexes, failures, output_files, allowed_dims):
   212→        return collect_batch_results(
   213→            selected_indexes=selected_indexes,
   214→            failures=failures,
   215→            output_files=output_files,
   216→            allowed_dims=allowed_dims,
   217→            extract_payload_fn=lambda raw: batch_core_mod.extract_json_payload(raw, log_fn=log),
   218→            normalize_result_fn=lambda payload, dims: batch_core_mod.normalize_batch_result(
   219→                payload,
   220→                dims,
   221→                max_batch_issues=max_batch_issues_for_dimension_count(
   222→                    len(dims)
   223→                ),
   224→                abstraction_sub_axes=ABSTRACTION_SUB_AXES,
   225→            ),
   226→        )
   227→
   228→    return review_batches_mod.do_run_batches(
   229→        args,
   230→        state,
   231→        lang,
   232→        state_file,
   233→        config=config,
   234→        run_stamp_fn=run_stamp,
   235→        load_or_prepare_packet_fn=_load_or_prepare_packet,
   236→        selected_batch_indexes_fn=lambda args, *, batch_count: selected_batch_indexes(
   237→            raw_selection=getattr(args, "only_batches", None),
   238→            batch_count=batch_count,
   239→            parse_fn=batch_core_mod.parse_batch_selection,
   240→            colorize_fn=colorize,
   241→        ),
   242→        prepare_run_artifacts_fn=_prepare_run_artifacts,
   243→        run_codex_batch_fn=lambda *, prompt, repo_root, output_file, log_file: run_codex_batch(
   244→            prompt=prompt,
   245→            repo_root=repo_root,
   246→            output_file=output_file,
   247→            log_file=log_file,
   248→            deps=CodexBatchRunnerDeps(
   249→                timeout_seconds=batch_timeout_seconds,
   250→                subprocess_run=subprocess.run,
   251→                timeout_error=subprocess.TimeoutExpired,
   252→                safe_write_text_fn=safe_write_text,
   253→                use_popen_runner=(getattr(subprocess.run, "__module__", "") == "subprocess"),
   254→                subprocess_popen=subprocess.Popen,
   255→                live_log_interval_seconds=batch_live_log_interval_seconds,
   256→                stall_after_output_seconds=batch_stall_kill_seconds,
   257→                max_retries=batch_max_retries,
   258→                retry_backoff_seconds=batch_retry_backoff_seconds,
   259→            ),
   260→        ),
   261→        execute_batches_fn=execute_batches,
   262→        collect_batch_results_fn=_collect_batch_results,
   263→        print_failures_fn=print_failures,
   264→        print_failures_and_raise_fn=print_failures_and_raise,
   265→        merge_batch_results_fn=_merge_batch_results,
   266→        build_import_provenance_fn=build_batch_import_provenance,
   267→        do_import_fn=_do_import,
   268→        run_followup_scan_fn=lambda *, lang_name, scan_path: run_followup_scan(
   269→            lang_name=lang_name,
   270→            scan_path=scan_path,
   271→            deps=FollowupScanDeps(
   272→                project_root=runtime_project_root,
   273→                timeout_seconds=FOLLOWUP_SCAN_TIMEOUT_SECONDS,
   274→                python_executable=sys.executable,
   275→                subprocess_run=subprocess.run,
   276→                timeout_error=subprocess.TimeoutExpired,
   277→                colorize_fn=colorize,
   278→            ),
   279→        ),
   280→        safe_write_text_fn=safe_write_text,
   281→        colorize_fn=colorize,
   282→        project_root=runtime_project_root,
   283→        subagent_runs_dir=_subagent_runs_dir(),
   284→    )
   285→
   286→def _validate_run_dir(run_dir: Path) -> tuple[dict, Path, str]:
   287→    """Validate run directory, load summary, and return (summary, blind_packet_path, immutable_packet_path).
   288→
   289→    Raises CommandError on any validation failure.
   290→    """
   291→    if not run_dir.is_dir():
   292→        raise CommandError(f"run directory not found: {run_dir}", exit_code=1)
   293→
   294→    summary_path = run_dir / "run_summary.json"
   295→    if not summary_path.exists():
   296→        raise CommandError(f"no run_summary.json in {run_dir}", exit_code=1)
   297→    try:
   298→        summary = json.loads(summary_path.read_text())
   299→    except (OSError, json.JSONDecodeError) as exc:
   300→        raise CommandError(f"Error reading run summary: {exc}", exit_code=1) from exc
   301→
   302→    successful = summary.get("successful_batches", [])
   303→    blind_packet_path = Path(str(summary.get("blind_packet", "")))
   304→    immutable_packet_path = str(summary.get("immutable_packet", ""))
   305→
   306→    if not successful:
   307→        raise CommandError("no successful batches in run summary.", exit_code=1)
   308→    if not blind_packet_path.exists():
   309→        raise PacketValidationError(f"blind packet not found: {blind_packet_path}", exit_code=1)
   310→
   311→    try:
   312→        packet = json.loads(Path(immutable_packet_path).read_text())
   313→    except (OSError, json.JSONDecodeError) as exc:
   314→        raise PacketValidationError(f"Error reading immutable packet: {exc}", exit_code=1) from exc
   315→
   316→    summary["_packet"] = packet
   317→    return summary, blind_packet_path, immutable_packet_path
   318→
   319→
   320→def do_import_run(
   321→    run_dir_path: str,
   322→    state: dict,
   323→    lang,
   324→    state_file: str,
   325→    *,
   326→    config: dict | None = None,
   327→    allow_partial: bool = False,
   328→    scan_after_import: bool = False,
   329→    scan_path: str = ".",
   330→) -> None:
   331→    """Re-import results from a completed run directory.
   332→
   333→    Replays the merge+provenance+import step that normally runs at the end of
   334→    ``--run-batches``.  Useful when the original pipeline was interrupted (e.g.
   335→    broken pipe from background execution) but all batch results completed.
   336→    """
   337→    run_dir = Path(run_dir_path)
   338→    summary, blind_packet_path, _immutable_path = _validate_run_dir(run_dir)
   339→
   340→    runner = str(summary.get("runner", "codex"))
   341→    stamp = str(summary.get("run_stamp", ""))
   342→    successful = summary.get("successful_batches", [])
   343→    packet = summary.pop("_packet", {})
   344→    allowed_dims = {str(d) for d in packet.get("dimensions", []) if isinstance(d, str)}
   345→
   346→    # -- locate and parse raw batch results --
   347→    results_dir = run_dir / "results"
   348→    selected_indexes = [idx - 1 for idx in successful]  # convert 1-based to 0-based
   349→    output_files = {
   350→        idx: results_dir / f"batch-{idx + 1}.raw.txt"
   351→        for idx in selected_indexes
   352→    }
   353→
   354→    missing = [idx + 1 for idx in selected_indexes if not output_files[idx].exists()]
   355→    if missing:
   356→        raise CommandError(f"missing result files for batches: {missing}", exit_code=1)
   357→
   358→    batch_results, failures = collect_batch_results(
   359→        selected_indexes=selected_indexes,
   360→        failures=[],
   361→        output_files=output_files,
   362→        allowed_dims=allowed_dims,
   363→        extract_payload_fn=lambda raw: batch_core_mod.extract_json_payload(raw, log_fn=log),
   364→        normalize_result_fn=lambda payload, dims: batch_core_mod.normalize_batch_result(
   365→            payload,
   366→            dims,
   367→            max_batch_issues=max_batch_issues_for_dimension_count(len(dims)),
   368→            abstraction_sub_axes=ABSTRACTION_SUB_AXES,
   369→        ),
   370→    )
   371→
   372→    if not batch_results:
   373→        raise CommandError("no valid batch results could be parsed.", exit_code=1)
   374→
   375→    print(colorize(f"  Parsed {len(batch_results)} batch results from {run_dir}", "bold"))
   376→    if failures:
   377→        print(colorize(f"  Warning: {len(failures)} batches failed to parse: {[f + 1 for f in failures]}", "yellow"))
   378→
   379→    # -- merge --
   380→    merged = _merge_batch_results(batch_results)
   381→
   382→    # -- build provenance --
   383→    successful_indexes = [idx for idx in selected_indexes if idx not in set(failures)]
   384→    merged["provenance"] = build_batch_import_provenance(
   385→        runner=runner,
   386→        blind_packet_path=blind_packet_path,
   387→        run_stamp=stamp,
   388→        batch_indexes=successful_indexes,
   389→    )
   390→
   391→    # -- write merged output --
   392→    merged_path = run_dir / "holistic_issues_merged.json"
   393→    safe_write_text(merged_path, json.dumps(merged, indent=2) + "\n")
   394→    print(colorize(f"  Merged output: {merged_path}", "bold"))
   395→
   396→    # -- import with trusted source --
   397→    _do_import(
   398→        str(merged_path),
   399→        state,
   400→        lang,
   401→        state_file,
   402→        config=config,
   403→        allow_partial=allow_partial,
   404→        trusted_assessment_source=True,
   405→        trusted_assessment_label=f"trusted import-run replay from {run_dir.name}",
   406→    )
   407→
   408→    # -- optional follow-up scan --
   409→    if scan_after_import:
   410→        lang_name = getattr(lang, "name", None) or str(getattr(lang, "lang", ""))
   411→        if lang_name:
   412→            run_followup_scan(
   413→                lang_name=lang_name,
   414→                scan_path=scan_path,
   415→                deps=FollowupScanDeps(
   416→                    project_root=_runtime_project_root(),
   417→                    timeout_seconds=FOLLOWUP_SCAN_TIMEOUT_SECONDS,
   418→                    python_executable=sys.executable,
   419→                    subprocess_run=subprocess.run,
   420→                    timeout_error=subprocess.TimeoutExpired,
   421→                    colorize_fn=colorize,
   422→                ),
   423→            )
   424→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/scope.py"
}
```

> TOOL

tool_result Read
```
1→"""Scope, coverage, and packet-shape helpers for review batch execution."""
     2→
     3→from __future__ import annotations
     4→
     5→import shlex
     6→import sys
     7→
     8→from desloppify.base.exception_sets import CommandError, PacketValidationError
     9→from desloppify.intelligence.review.dimensions.data import load_dimensions_for_lang
    10→from desloppify.intelligence.review.feedback_contract import (
    11→    LEGACY_REVIEW_QUALITY_HIGH_SCORE_MISSING_ISSUES_KEY,
    12→    REVIEW_QUALITY_HIGH_SCORE_MISSING_ISSUES_KEY,
    13→    TRUSTED_IMPORT_COVERAGE_OVERRIDE_FLAG,
    14→)
    15→
    16→
    17→def validate_runner(runner: str, *, colorize_fn) -> None:
    18→    """Validate review batch runner."""
    19→    if runner == "codex":
    20→        return
    21→    raise CommandError(
    22→        f"Error: unsupported runner '{runner}' (supported: codex)", exit_code=2
    23→    )
    24→
    25→
    26→def require_batches(
    27→    packet: dict,
    28→    *,
    29→    colorize_fn,
    30→    suggested_prepare_cmd: str | None = None,
    31→) -> list[dict]:
    32→    """Return investigation batches or exit with a clear error."""
    33→    batches = packet.get("investigation_batches", [])
    34→    if isinstance(batches, list) and batches:
    35→        return batches
    36→    if isinstance(suggested_prepare_cmd, str) and suggested_prepare_cmd.strip():
    37→        print(
    38→            colorize_fn(
    39→                f"  Regenerate review context first: `{suggested_prepare_cmd}`",
    40→                "yellow",
    41→            ),
    42→            file=sys.stderr,
    43→        )
    44→    print(
    45→        colorize_fn(
    46→            "  Happy path: `desloppify review --prepare` then follow your runner's review workflow.",
    47→            "dim",
    48→        ),
    49→        file=sys.stderr,
    50→    )
    51→    raise PacketValidationError("Error: packet has no investigation_batches.", exit_code=1)
    52→
    53→
    54→def print_review_quality(quality: object, *, colorize_fn) -> None:
    55→    """Render merged review quality summary when present."""
    56→    if not isinstance(quality, dict):
    57→        return
    58→    coverage = quality.get("dimension_coverage")
    59→    density = quality.get("evidence_density")
    60→    high_missing_issue_note = quality.get(
    61→        REVIEW_QUALITY_HIGH_SCORE_MISSING_ISSUES_KEY
    62→    )
    63→    if not isinstance(high_missing_issue_note, int | float):
    64→        high_missing_issue_note = quality.get(
    65→            LEGACY_REVIEW_QUALITY_HIGH_SCORE_MISSING_ISSUES_KEY
    66→        )
    67→    issue_pressure = quality.get("issue_pressure")
    68→    dims_with_issues = quality.get("dimensions_with_issues")
    69→    if not isinstance(coverage, int | float) or not isinstance(density, int | float):
    70→        return
    71→
    72→    pressure_segment = ""
    73→    if isinstance(issue_pressure, int | float) and isinstance(dims_with_issues, int):
    74→        pressure_segment = (
    75→            f", issue-pressure {float(issue_pressure):.2f} "
    76→            f"across {dims_with_issues} dims"
    77→        )
    78→    print(
    79→        colorize_fn(
    80→            "  Review quality: "
    81→            f"dimension coverage {float(coverage):.2f}, "
    82→            f"evidence density {float(density):.2f}, "
    83→            f"high-score-missing-issue-note {int(high_missing_issue_note or 0)}"
    84→            f"{pressure_segment}",
    85→            "dim",
    86→        )
    87→    )
    88→
    89→
    90→def collect_reviewed_files_from_batches(
    91→    *,
    92→    batches: list[dict[str, object]],
    93→    selected_indexes: list[int],
    94→) -> list[str]:
    95→    """Collect normalized file paths reviewed in the selected batch set."""
    96→    reviewed: list[str] = []
    97→    seen: set[str] = set()
    98→    for idx in selected_indexes:
    99→        if idx < 0 or idx >= len(batches):
   100→            continue
   101→        batch = batches[idx]
   102→        files = batch.get("files_to_read", [])
   103→        if not isinstance(files, list):
   104→            continue
   105→        for raw in files:
   106→            if not isinstance(raw, str):
   107→                continue
   108→            path = raw.strip().strip(",'\"")
   109→            if not path or path in {".", ".."}:
   110→                continue
   111→            if path.endswith("/"):
   112→                continue
   113→            if path in seen:
   114→                continue
   115→            seen.add(path)
   116→            reviewed.append(path)
   117→    return reviewed
   118→
   119→
   120→def normalize_dimension_list(raw: object) -> list[str]:
   121→    """Normalize dimension collections to a stable, de-duplicated list."""
   122→    if not isinstance(raw, list):
   123→        return []
   124→    out: list[str] = []
   125→    seen: set[str] = set()
   126→    for item in raw:
   127→        if not isinstance(item, str):
   128→            continue
   129→        dim = item.strip()
   130→        if not dim or dim in seen:
   131→            continue
   132→        seen.add(dim)
   133→        out.append(dim)
   134→    return out
   135→
   136→
   137→def scored_dimensions_for_lang(lang_name: str) -> list[str]:
   138→    """Return default scored subjective dimensions for one language."""
   139→    try:
   140→        default_dims, _, _ = load_dimensions_for_lang(lang_name)
   141→    except (ValueError, RuntimeError):
   142→        return []
   143→    return normalize_dimension_list(default_dims)
   144→
   145→
   146→def missing_scored_dimensions(
   147→    *,
   148→    selected_dims: list[str],
   149→    scored_dims: list[str],
   150→) -> list[str]:
   151→    selected = set(selected_dims)
   152→    return [dim for dim in scored_dims if dim not in selected]
   153→
   154→
   155→def missing_dimensions_command(*, missing_dims: list[str], scan_path: str) -> str:
   156→    """Return rerun command for missing subjective dimensions."""
   157→    base = "desloppify review --prepare --scan-after-import"
   158→    if scan_path and scan_path != ".":
   159→        base += f" --path {shlex.quote(scan_path)}"
   160→    if missing_dims:
   161→        base += f" --dimensions {','.join(missing_dims)}"
   162→    return base
   163→
   164→
   165→def print_preflight_dimension_scope_notice(
   166→    *,
   167→    selected_dims: list[str],
   168→    scored_dims: list[str],
   169→    explicit_selection: bool,
   170→    scan_path: str,
   171→    colorize_fn,
   172→) -> None:
   173→    """Print trigger-time notice when run scope is a scored-dimension subset."""
   174→    if not scored_dims:
   175→        return
   176→    missing_dims = missing_scored_dimensions(
   177→        selected_dims=selected_dims,
   178→        scored_dims=scored_dims,
   179→    )
   180→    if not missing_dims:
   181→        return
   182→
   183→    covered_count = len([dim for dim in selected_dims if dim in set(scored_dims)])
   184→    scope_reason = (
   185→        "explicit --dimensions selection"
   186→        if explicit_selection
   187→        else "language default review dimension set"
   188→    )
   189→    tone = "yellow" if explicit_selection else "red"
   190→    print(
   191→        colorize_fn(
   192→            "  WARNING: this run targets "
   193→            f"{covered_count}/{len(scored_dims)} scored subjective dimensions "
   194→            f"({scope_reason}).",
   195→            tone,
   196→        )
   197→    )
   198→    preview = ", ".join(missing_dims[:5])
   199→    if len(missing_dims) > 5:
   200→        preview = f"{preview}, +{len(missing_dims) - 5} more"
   201→    print(colorize_fn(f"  Missing from this run: {preview}", "yellow"))
   202→    print(
   203→        colorize_fn(
   204→            "  Rerun missing dimensions: "
   205→            f"`{missing_dimensions_command(missing_dims=missing_dims, scan_path=scan_path)}`",
   206→            "dim",
   207→        )
   208→    )
   209→
   210→
   211→def print_import_dimension_coverage_notice(
   212→    *,
   213→    assessed_dims: list[str],
   214→    scored_dims: list[str],
   215→    scan_path: str,
   216→    colorize_fn,
   217→) -> list[str]:
   218→    """Print result-time notice when merged import covers only a subset."""
   219→    if not scored_dims:
   220→        return []
   221→    missing_dims = missing_scored_dimensions(
   222→        selected_dims=assessed_dims,
   223→        scored_dims=scored_dims,
   224→    )
   225→    if not missing_dims:
   226→        return []
   227→
   228→    covered_count = len([dim for dim in assessed_dims if dim in set(scored_dims)])
   229→    print(
   230→        colorize_fn(
   231→            "  Coverage gap: imported assessments for "
   232→            f"{covered_count}/{len(scored_dims)} scored subjective dimensions.",
   233→            "yellow",
   234→        )
   235→    )
   236→    preview = ", ".join(missing_dims[:5])
   237→    if len(missing_dims) > 5:
   238→        preview = f"{preview}, +{len(missing_dims) - 5} more"
   239→    print(colorize_fn(f"  Still missing: {preview}", "yellow"))
   240→    print(
   241→        colorize_fn(
   242→            "  Run to cover missing dimensions: "
   243→            f"`{missing_dimensions_command(missing_dims=missing_dims, scan_path=scan_path)}`",
   244→            "dim",
   245→        )
   246→    )
   247→    return missing_dims
   248→
   249→
   250→def enforce_trusted_import_coverage_gate(
   251→    *,
   252→    missing_dims: list[str],
   253→    selected_dims: list[str],
   254→    allow_partial: bool,
   255→    scan_path: str,
   256→    colorize_fn,
   257→) -> None:
   258→    """Block trusted assessment import when selected assessment dimensions are missing."""
   259→    if not selected_dims or not missing_dims:
   260→        return
   261→    if allow_partial:
   262→        print(
   263→            colorize_fn(
   264→                "  Coverage override: importing with missing scored dimensions "
   265→                f"because {TRUSTED_IMPORT_COVERAGE_OVERRIDE_FLAG} is enabled.",
   266→                "yellow",
   267→            )
   268→        )
   269→        return
   270→
   271→    preview = ", ".join(missing_dims[:5])
   272→    if len(missing_dims) > 5:
   273→        preview = f"{preview}, +{len(missing_dims) - 5} more"
   274→    print(colorize_fn(f"  Missing dimensions: {preview}", "yellow"), file=sys.stderr)
   275→    print(
   276→        colorize_fn(
   277→            "  Retry with full coverage or explicitly bypass with "
   278→            f"{TRUSTED_IMPORT_COVERAGE_OVERRIDE_FLAG}.",
   279→            "yellow",
   280→        ),
   281→        file=sys.stderr,
   282→    )
   283→    print(
   284→        colorize_fn(
   285→            "  Suggested rerun: "
   286→            f"`{missing_dimensions_command(missing_dims=missing_dims, scan_path=scan_path)}`",
   287→            "dim",
   288→        ),
   289→        file=sys.stderr,
   290→    )
   291→    raise CommandError(
   292→        "Error: trusted assessment import blocked due to incomplete selected-dimension coverage.",
   293→        exit_code=1,
   294→    )
   295→
   296→
   297→__all__ = [
   298→    "collect_reviewed_files_from_batches",
   299→    "enforce_trusted_import_coverage_gate",
   300→    "missing_dimensions_command",
   301→    "missing_scored_dimensions",
   302→    "normalize_dimension_list",
   303→    "print_import_dimension_coverage_notice",
   304→    "print_preflight_dimension_scope_notice",
   305→    "print_review_quality",
   306→    "require_batches",
   307→    "scored_dimensions_for_lang",
   308→    "validate_runner",
   309→]
   310→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prepare.py"
}
```

> TOOL

tool_result Read
```
1→"""Prepare flow for review command."""
     2→
     3→from __future__ import annotations
     4→
     5→from pathlib import Path
     6→
     7→from desloppify.app.commands.helpers.query import write_query
     8→from desloppify.base.coercions import coerce_positive_int
     9→from desloppify.base.exception_sets import CommandError
    10→from desloppify.base.output.terminal import colorize
    11→import desloppify.intelligence.narrative.core as narrative_mod
    12→from desloppify.intelligence import review as review_mod
    13→
    14→from .helpers import parse_dimensions
    15→from .packet.policy import coerce_review_batch_file_limit, redacted_review_config
    16→from .runtime.setup import setup_lang_concrete
    17→
    18→
    19→def do_prepare(
    20→    args,
    21→    state,
    22→    lang,
    23→    _state_path,
    24→    *,
    25→    config: dict,
    26→) -> None:
    27→    """Prepare mode: holistic-only review packet in query.json."""
    28→    path = Path(args.path)
    29→    dims = parse_dimensions(args)
    30→    dimensions = list(dims) if dims else None
    31→    retrospective = bool(getattr(args, "retrospective", False))
    32→    retrospective_max_issues = coerce_positive_int(
    33→        getattr(args, "retrospective_max_issues", None),
    34→        default=30,
    35→    )
    36→    retrospective_max_batch_items = coerce_positive_int(
    37→        getattr(args, "retrospective_max_batch_items", None),
    38→        default=20,
    39→    )
    40→
    41→    lang_run, found_files = setup_lang_concrete(lang, path, config)
    42→
    43→    lang_name = lang_run.name
    44→    narrative = narrative_mod.compute_narrative(
    45→        state,
    46→        context=narrative_mod.NarrativeContext(lang=lang_name, command="review"),
    47→    )
    48→    data = review_mod.prepare_holistic_review(
    49→        path,
    50→        lang_run,
    51→        state,
    52→        options=review_mod.HolisticReviewPrepareOptions(
    53→            dimensions=dimensions,
    54→            files=found_files or None,
    55→            max_files_per_batch=coerce_review_batch_file_limit(config),
    56→            include_issue_history=retrospective,
    57→            issue_history_max_issues=retrospective_max_issues,
    58→            issue_history_max_batch_items=retrospective_max_batch_items,
    59→        ),
    60→    )
    61→    next_command = (
    62→        "desloppify review --prepare"
    63→    )
    64→    if retrospective:
    65→        next_command += (
    66→            " --retrospective"
    67→            f" --retrospective-max-issues {retrospective_max_issues}"
    68→            f" --retrospective-max-batch-items {retrospective_max_batch_items}"
    69→        )
    70→    data["config"] = redacted_review_config(config)
    71→    data["narrative"] = narrative
    72→    data["next_command"] = next_command
    73→    total = data.get("total_files", 0)
    74→    if total == 0:
    75→        msg = f"no files found at path '{path}'. Nothing to review."
    76→        scan_path = state.get("scan_path") if isinstance(state, dict) else None
    77→        if scan_path:
    78→            msg += (
    79→                f"\nHint: your last scan used --path {scan_path}. "
    80→                f"Try: desloppify review --prepare --path {scan_path}"
    81→            )
    82→        else:
    83→            msg += "\nHint: pass --path <dir> matching the path used during scan."
    84→        raise CommandError(msg, exit_code=1)
    85→    write_query(data)
    86→    _print_prepare_summary(data, next_command=next_command, retrospective=retrospective)
    87→
    88→
    89→def _print_prepare_summary(
    90→    data: dict, *, next_command: str, retrospective: bool,
    91→) -> None:
    92→    """Print the prepare summary to the terminal."""
    93→    total = data.get("total_files", 0)
    94→    batches = data.get("investigation_batches", [])
    95→    print(colorize(f"\n  Holistic review prepared: {total} files in codebase", "bold"))
    96→    if retrospective:
    97→        print(
    98→            colorize(
    99→                "  Retrospective context enabled: historical review issues injected into packet.",
   100→                "dim",
   101→            )
   102→        )
   103→    if batches:
   104→        print(
   105→            colorize(
   106→                "\n  Investigation batches (independent — can run in parallel):", "bold"
   107→            )
   108→        )
   109→        for i, batch in enumerate(batches, 1):
   110→            n_files = len(batch["files_to_read"])
   111→            print(
   112→                colorize(
   113→                    f"    {i}. {batch['name']} ({n_files} files) — {batch['why']}",
   114→                    "dim",
   115→                )
   116→            )
   117→    print(colorize("\n  Workflow:", "bold"))
   118→    for step_i, step in enumerate(data.get("workflow", []), 1):
   119→        print(colorize(f"    {step_i}. {step}", "dim"))
   120→    n_batches = len(data.get("investigation_batches", []))
   121→    print(colorize("\n  AGENT PLAN — pick the path matching your runner:", "yellow"))
   122→    print(
   123→        colorize(
   124→            "  1. Codex: `desloppify review --run-batches --runner codex --parallel --scan-after-import`",
   125→            "dim",
   126→        )
   127→    )
   128→    print(
   129→        colorize(
   130→            f"  2. Claude / other agent: `desloppify review --run-batches --dry-run`"
   131→            f" → generates {n_batches} prompt files in .desloppify/subagent_runs/<run>/prompts/."
   132→            f" Launch {n_batches} subagents in parallel (one per prompt),"
   133→            " write output to the matching results/ file,"
   134→            " then `desloppify review --import-run <run-dir> --scan-after-import`",
   135→            "dim",
   136→        )
   137→    )
   138→    print(
   139→        colorize(
   140→            "  3. Cloud/external: `desloppify review --external-start --external-runner claude` → follow template → `--external-submit`",
   141→            "dim",
   142→        )
   143→    )
   144→    print(
   145→        colorize(
   146→            "  4. Issues-only fallback: `desloppify review --import issues.json`",
   147→            "dim",
   148→        )
   149→    )
   150→    print(
   151→        colorize(
   152→            "  5. Emergency only: `--manual-override --attest \"<why>\"` (provisional; expires on next scan)",
   153→            "dim",
   154→        )
   155→    )
   156→    print(
   157→        colorize(
   158→            "\n  → query.json updated. Batches are pre-defined — do NOT regroup dimensions yourself.",
   159→            "cyan",
   160→        )
   161→    )
   162→
   163→
   164→__all__ = ["do_prepare"]
   165→
```

> AGENT

Now let me look at the execution file and the intelligence review module to understand where batches are created:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1→"""Batch execution flow helpers for review command."""
     2→
     3→from __future__ import annotations
     4→
     5→import json
     6→import math
     7→from datetime import UTC, datetime
     8→from functools import partial
     9→from pathlib import Path
    10→from typing import Any
    11→
    12→from desloppify.base.exception_sets import CommandError
    13→
    14→from ..batches_runtime import (
    15→    BatchRunSummaryConfig,
    16→    build_batch_tasks,
    17→    make_run_log_writer,
    18→    resolve_run_log_path,
    19→)
    20→from ..batches_runtime import (
    21→    write_run_summary as _write_run_summary_impl,
    22→)
    23→from ..prompt_sections import explode_to_single_dimension
    24→from ..runner_parallel import BatchExecutionOptions, BatchProgressEvent
    25→from ..runtime.policy import resolve_batch_run_policy
    26→from .scope import (
    27→    collect_reviewed_files_from_batches,
    28→    normalize_dimension_list,
    29→    print_import_dimension_coverage_notice,
    30→    print_preflight_dimension_scope_notice,
    31→    print_review_quality,
    32→    require_batches,
    33→    scored_dimensions_for_lang,
    34→    validate_runner,
    35→)
    36→
    37→
    38→def _record_execution_issue(append_run_log_fn, batch_index: int, exc: Exception) -> None:
    39→    """Record one execute_batches callback/task failure in run.log."""
    40→    if batch_index < 0:
    41→        append_run_log_fn(f"execution-error heartbeat error={exc}")
    42→        return
    43→    append_run_log_fn(f"execution-error batch={batch_index + 1} error={exc}")
    44→
    45→
    46→def _build_progress_reporter(
    47→    *,
    48→    batch_positions: dict[int, int],
    49→    batch_status: dict[str, dict[str, object]],
    50→    stall_warned_batches: set[int],
    51→    total_batches: int,
    52→    stall_warning_seconds: float,
    53→    prompt_files: dict,
    54→    output_files: dict,
    55→    log_files: dict,
    56→    append_run_log,
    57→    colorize_fn,
    58→):
    59→    """Build the _report_progress closure used during batch execution."""
    60→
    61→    def _report_progress(
    62→        progress_event: BatchProgressEvent,
    63→    ) -> None:
    64→        batch_index = progress_event.batch_index
    65→        event = progress_event.event
    66→        code = progress_event.code
    67→        details = progress_event.details
    68→        if event == "heartbeat":
    69→            _handle_heartbeat(
    70→                details=details,
    71→                total_batches=total_batches,
    72→                stall_warning_seconds=stall_warning_seconds,
    73→                stall_warned_batches=stall_warned_batches,
    74→                append_run_log=append_run_log,
    75→                colorize_fn=colorize_fn,
    76→            )
    77→            return
    78→
    79→        position = batch_positions.get(batch_index, 0)
    80→        key = str(batch_index + 1)
    81→        state = batch_status.setdefault(
    82→            key,
    83→            {
    84→                "position": position,
    85→                "status": "pending",
    86→                "prompt_path": str(prompt_files.get(batch_index, "")),
    87→                "result_path": str(output_files.get(batch_index, "")),
    88→                "log_path": str(log_files.get(batch_index, "")),
    89→            },
    90→        )
    91→        if event == "queued":
    92→            state["status"] = "queued"
    93→            print(
    94→                colorize_fn(
    95→                    f"  Batch {position}/{total_batches} queued (#{batch_index + 1})",
    96→                    "dim",
    97→                )
    98→            )
    99→            append_run_log(f"batch-queued batch={batch_index + 1} position={position}/{total_batches}")
   100→            return
```

> TOOL

tool_use Grep
```json
{
  "pattern": "investigation_batches|prepare_holistic_review|batch_type|Full Codebase Sweep",
  "path": "/Users/user_c042661f/Documents/desloppify",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 21 files
desloppify/tests/review/review_commands_cases.py
desloppify/intelligence/review/_prepare/helpers.py
desloppify/tests/commands/review/test_review_process_guards_direct.py
desloppify/app/commands/review/batch/orchestrator.py
desloppify/app/commands/review/batch/scope.py
desloppify/app/commands/review/prepare.py
desloppify/app/commands/review/external.py
desloppify/tests/review/context/test_holistic_review.py
desloppify/tests/commands/test_direct_coverage_modules.py
desloppify/intelligence/review/__init__.py
desloppify/tests/review/import_scoring/test_review_external.py
desloppify/intelligence/review/prepare.py
desloppify/intelligence/review/prepare_holistic_flow.py
desloppify/intelligence/review/prepare_batches.py
desloppify/tests/review/review_submodules_cases.py
desloppify/app/commands/review/packet/build.py
desloppify/app/commands/review/coordinator.py
desloppify/tests/review/context/test_issue_history_context.py
desloppify/tests/review/batch/test_review_split.py
desloppify/tests/commands/test_direct_coverage_split_modules.py
desloppify/tests/snapshots/cli_smoke/query.json
```

> AGENT

Good! The key files are in the intelligence module. Let me read those:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py"
}
```

> TOOL

tool_result Read
```
1→"""Holistic review preparation workflow helpers."""
     2→
     3→from __future__ import annotations
     4→
     5→import logging
     6→from dataclasses import dataclass
     7→from pathlib import Path
     8→from typing import Any
     9→
    10→from desloppify.base.discovery.file_paths import rel
    11→from desloppify.intelligence.review._context.models import HolisticContext
    12→from desloppify.intelligence.review._prepare.helpers import HOLISTIC_WORKFLOW
    13→from desloppify.intelligence.review._prepare.issue_history import (
    14→    ReviewHistoryOptions,
    15→    build_batch_issue_focus,
    16→    build_issue_history_context,
    17→)
    18→
    19→_NON_PRODUCTION_ZONES = frozenset({"test", "config", "generated", "vendor"})
    20→logger = logging.getLogger(__name__)
    21→
    22→
    23→def collect_allowed_review_files(
    24→    files: list[str],
    25→    lang: object,
    26→    *,
    27→    base_path: Path | None = None,
    28→) -> set[str]:
    29→    """Return relative production-file paths allowed for holistic review batches."""
    30→    allowed: set[str] = set()
    31→    zone_map = getattr(lang, "zone_map", None)
    32→    resolved_base = base_path.resolve() if isinstance(base_path, Path) else None
    33→    for filepath in files:
    34→        if not isinstance(filepath, str):
    35→            continue
    36→        normalized = filepath.strip().replace("\\", "/")
    37→        if not normalized:
    38→            continue
    39→        if zone_map is not None:
    40→            zone_get = getattr(zone_map, "get", None)
    41→            zone = zone_get(filepath) if callable(zone_get) else None
    42→            zone_value = getattr(zone, "value", zone)
    43→            if zone_value is None:
    44→                zone_value = "production"
    45→            if not isinstance(zone_value, str):
    46→                zone_value = str(zone_value)
    47→            if zone_value in _NON_PRODUCTION_ZONES:
    48→                continue
    49→        allowed.add(normalized)
    50→        allowed.add(rel(filepath))
    51→        if resolved_base is not None:
    52→            try:
    53→                resolved_path = Path(filepath).resolve()
    54→            except OSError as exc:
    55→                logger.debug("Skipping invalid review file path %s: %s", filepath, exc)
    56→                continue
    57→            if resolved_path.is_relative_to(resolved_base):
    58→                allowed.add(resolved_path.relative_to(resolved_base).as_posix())
    59→    return allowed
    60→
    61→
    62→def file_in_allowed_scope(filepath: object, allowed_files: set[str]) -> bool:
    63→    """True when *filepath* resolves to a currently in-scope review file."""
    64→    if not isinstance(filepath, str):
    65→        return False
    66→    normalized = filepath.strip().replace("\\", "/")
    67→    if not normalized:
    68→        return False
    69→    if normalized in allowed_files:
    70→        return True
    71→    return rel(filepath) in allowed_files
    72→
    73→
    74→def filter_issue_focus_to_scope(
    75→    issue_focus: object,
    76→    allowed_files: set[str],
    77→) -> dict[str, object] | None:
    78→    """Drop out-of-scope related_files from historical issue focus payload."""
    79→    if not isinstance(issue_focus, dict):
    80→        return None
    81→    issues_raw = issue_focus.get("issues", [])
    82→    issues: list[dict[str, object]] = []
    83→    if isinstance(issues_raw, list):
    84→        for raw_issue in issues_raw:
    85→            if not isinstance(raw_issue, dict):
    86→                continue
    87→            issue = dict(raw_issue)
    88→            related_raw = issue.get("related_files", [])
    89→            if isinstance(related_raw, list):
    90→                issue["related_files"] = [
    91→                    path for path in related_raw if file_in_allowed_scope(path, allowed_files)
    92→                ]
    93→            issues.append(issue)
    94→    scoped = dict(issue_focus)
    95→    scoped["issues"] = issues
    96→    scoped["selected_count"] = len(issues)
    97→    return scoped
    98→
    99→
   100→def filter_batches_to_file_scope(
   101→    batches: list[dict[str, Any]],
   102→    *,
   103→    allowed_files: set[str],
   104→) -> list[dict[str, Any]]:
   105→    """Strip out-of-scope files/signals from review batches."""
   106→    if not allowed_files:
   107→        return []
   108→
   109→    scoped_batches: list[dict[str, Any]] = []
   110→    for raw_batch in batches:
   111→        if not isinstance(raw_batch, dict):
   112→            continue
   113→        batch = dict(raw_batch)
   114→        files_to_read = batch.get("files_to_read", [])
   115→        if isinstance(files_to_read, list):
   116→            scoped_files = [
   117→                filepath
   118→                for filepath in files_to_read
   119→                if file_in_allowed_scope(filepath, allowed_files)
   120→            ]
   121→        else:
   122→            scoped_files = []
   123→        batch["files_to_read"] = scoped_files
   124→
   125→        concern_signals = batch.get("concern_signals", [])
   126→        if isinstance(concern_signals, list):
   127→            batch["concern_signals"] = [
   128→                signal
   129→                for signal in concern_signals
   130→                if isinstance(signal, dict)
   131→                and file_in_allowed_scope(signal.get("file", ""), allowed_files)
   132→            ]
   133→            if "concern_signal_count" in batch:
   134→                batch["concern_signal_count"] = len(batch["concern_signals"])
   135→
   136→        issue_focus = filter_issue_focus_to_scope(
   137→            batch.get("historical_issue_focus"),
   138→            allowed_files,
   139→        )
   140→        if issue_focus is not None:
   141→            batch["historical_issue_focus"] = issue_focus
   142→
   143→        has_seed_files = bool(batch["files_to_read"])
   144→        has_signals = bool(batch.get("concern_signals"))
   145→        if has_seed_files or has_signals:
   146→            scoped_batches.append(batch)
   147→    return scoped_batches
   148→
   149→
   150→# ---------------------------------------------------------------------------
   151→# Internal helpers decomposed from prepare_holistic_review_payload
   152→# ---------------------------------------------------------------------------
   153→
   154→
   155→def _resolve_review_files(
   156→    path: Path,
   157→    lang: object,
   158→    options: object,
   159→) -> tuple[list[str], set[str]]:
   160→    """Resolve the full file list and the allowed-review-file set."""
   161→    all_files = (
   162→        options.files
   163→        if options.files is not None
   164→        else (lang.file_finder(path) if lang.file_finder else [])
   165→    )
   166→    allowed = collect_allowed_review_files(all_files, lang, base_path=path)
   167→    return all_files, allowed
   168→
   169→
   170→def _build_review_contexts(
   171→    path: Path,
   172→    lang: object,
   173→    state: dict,
   174→    all_files: list[str],
   175→    *,
   176→    is_file_cache_enabled_fn,
   177→    enable_file_cache_fn,
   178→    disable_file_cache_fn,
   179→    build_holistic_context_fn,
   180→    build_review_context_fn,
   181→) -> tuple[HolisticContext, object]:
   182→    """Build holistic and review contexts, managing the file cache lifecycle."""
   183→    already_cached = is_file_cache_enabled_fn()
   184→    if not already_cached:
   185→        enable_file_cache_fn()
   186→    try:
   187→        context = HolisticContext.from_raw(
   188→            build_holistic_context_fn(path, lang, state, files=all_files)
   189→        )
   190→        review_ctx = build_review_context_fn(path, lang, state, files=all_files)
   191→    finally:
   192→        if not already_cached:
   193→            disable_file_cache_fn()
   194→    return context, review_ctx
   195→
   196→
   197→@dataclass
   198→class _DimensionContext:
   199→    """Resolved dimension configuration for holistic review."""
   200→
   201→    dims: list[str]
   202→    holistic_prompts: dict[str, Any]
   203→    per_file_prompts: dict[str, Any]
   204→    system_prompt: str
   205→    lang_guide: str
   206→    invalid_requested: list[str]
   207→    invalid_default: list[str]
   208→
   209→
   210→def _resolve_dimension_context(
   211→    lang_name: str,
   212→    options: object,
   213→    *,
   214→    load_dimensions_for_lang_fn,
   215→    resolve_dimensions_fn,
   216→    get_lang_guidance_fn,
   217→) -> _DimensionContext:
   218→    """Load, resolve, and validate dimensions for the review."""
   219→    default_dims, holistic_prompts, system_prompt = load_dimensions_for_lang_fn(lang_name)
   220→    _, per_file_prompts, _ = load_dimensions_for_lang_fn(lang_name)
   221→    dims = resolve_dimensions_fn(
   222→        cli_dimensions=options.dimensions,
   223→        default_dimensions=default_dims,
   224→    )
   225→    lang_guide = get_lang_guidance_fn(lang_name)
   226→    valid_dims = set(holistic_prompts) | set(per_file_prompts)
   227→    invalid_requested = [
   228→        dim for dim in (options.dimensions or []) if dim not in valid_dims
   229→    ]
   230→    invalid_default = [dim for dim in default_dims if dim not in valid_dims]
   231→    return _DimensionContext(
   232→        dims=dims,
   233→        holistic_prompts=holistic_prompts,
   234→        per_file_prompts=per_file_prompts,
   235→        system_prompt=system_prompt,
   236→        lang_guide=lang_guide,
   237→        invalid_requested=invalid_requested,
   238→        invalid_default=invalid_default,
   239→    )
   240→
   241→
   242→def _append_concerns_batch(
   243→    batches: list[dict[str, Any]],
   244→    state: dict,
   245→    dims: list[str],
   246→    allowed_review_files: set[str],
   247→    max_files_per_batch: int,
   248→    *,
   249→    batch_concerns_fn,
   250→    log_best_effort_failure_fn,
   251→    log: object,
   252→) -> None:
   253→    """Generate concern signals and append as a batch (best-effort)."""
   254→    try:
   255→        from desloppify.engine.concerns import generate_concerns
   256→
   257→        concerns = generate_concerns(state)
   258→        concerns = [
   259→            concern
   260→            for concern in concerns
   261→            if file_in_allowed_scope(getattr(concern, "file", ""), allowed_review_files)
   262→        ]
   263→        concerns_batch = batch_concerns_fn(
   264→            concerns,
   265→            max_files=max_files_per_batch,
   266→            active_dimensions=dims,
   267→        )
   268→        if concerns_batch:
   269→            batches.append(concerns_batch)
   270→    except (ImportError, AttributeError, TypeError, ValueError) as exc:
   271→        log_best_effort_failure_fn(log, "generate review concern batch", exc)
   272→
   273→
   274→def _build_selected_prompts(
   275→    dims: list[str],
   276→    holistic_prompts: dict[str, Any],
   277→    per_file_prompts: dict[str, Any],
   278→) -> dict[str, dict[str, object]]:
   279→    """Build the dimension-to-prompt mapping, preferring holistic prompts."""
   280→    selected: dict[str, dict[str, object]] = {}
   281→    for dim in dims:
   282→        prompt = holistic_prompts.get(dim)
   283→        if prompt is None:
   284→            prompt = per_file_prompts.get(dim)
   285→        if prompt is None:
   286→            continue
   287→        selected[dim] = prompt
   288→    return selected
   289→
   290→
   291→def _attach_issue_history_context(
   292→    payload: dict[str, Any],
   293→    batches: list[dict[str, Any]],
   294→    state: dict,
   295→    options: object,
   296→    allowed_review_files: set[str],
   297→) -> list[dict[str, Any]]:
   298→    """Attach issue history to payload and per-batch focus; re-scope batches."""
   299→    if not options.include_issue_history:
   300→        return batches
   301→    history_payload = build_issue_history_context(
   302→        state,
   303→        options=ReviewHistoryOptions(
   304→            max_issues=options.issue_history_max_issues,
   305→        ),
   306→    )
   307→    payload["historical_review_issues"] = history_payload
   308→    for batch in batches:
   309→        if not isinstance(batch, dict):
   310→            continue
   311→        batch_dims = batch.get("dimensions", [])
   312→        batch["historical_issue_focus"] = build_batch_issue_focus(
   313→            history_payload,
   314→            dimensions=batch_dims,
   315→            max_items=options.issue_history_max_batch_items,
   316→        )
   317→    return filter_batches_to_file_scope(
   318→        batches,
   319→        allowed_files=allowed_review_files,
   320→    )
   321→
   322→
   323→# ---------------------------------------------------------------------------
   324→# Main orchestrator
   325→# ---------------------------------------------------------------------------
   326→
   327→
   328→def prepare_holistic_review_payload(
   329→    path: Path,
   330→    lang: object,
   331→    state: dict,
   332→    options,
   333→    *,
   334→    is_file_cache_enabled_fn,
   335→    enable_file_cache_fn,
   336→    disable_file_cache_fn,
   337→    build_holistic_context_fn,
   338→    build_review_context_fn,
   339→    load_dimensions_for_lang_fn,
   340→    resolve_dimensions_fn,
   341→    get_lang_guidance_fn,
   342→    build_investigation_batches_fn,
   343→    batch_concerns_fn,
   344→    filter_batches_to_dimensions_fn,
   345→    append_full_sweep_batch_fn,
   346→    serialize_context_fn,
   347→    log_best_effort_failure_fn,
   348→    logger,
   349→) -> dict[str, object]:
   350→    """Prepare holistic review payload with injected dependencies for patchability."""
   351→    all_files, allowed_review_files = _resolve_review_files(path, lang, options)
   352→
   353→    context, review_ctx = _build_review_contexts(
   354→        path, lang, state, all_files,
   355→        is_file_cache_enabled_fn=is_file_cache_enabled_fn,
   356→        enable_file_cache_fn=enable_file_cache_fn,
   357→        disable_file_cache_fn=disable_file_cache_fn,
   358→        build_holistic_context_fn=build_holistic_context_fn,
   359→        build_review_context_fn=build_review_context_fn,
   360→    )
   361→
   362→    dim_ctx = _resolve_dimension_context(
   363→        lang.name, options,
   364→        load_dimensions_for_lang_fn=load_dimensions_for_lang_fn,
   365→        resolve_dimensions_fn=resolve_dimensions_fn,
   366→        get_lang_guidance_fn=get_lang_guidance_fn,
   367→    )
   368→
   369→    batches = build_investigation_batches_fn(
   370→        context,
   371→        lang,
   372→        repo_root=path,
   373→        max_files_per_batch=options.max_files_per_batch,
   374→    )
   375→
   376→    _append_concerns_batch(
   377→        batches, state, dim_ctx.dims, allowed_review_files,
   378→        options.max_files_per_batch,
   379→        batch_concerns_fn=batch_concerns_fn,
   380→        log_best_effort_failure_fn=log_best_effort_failure_fn,
   381→        log=logger,
   382→    )
   383→
   384→    batches = filter_batches_to_dimensions_fn(
   385→        batches,
   386→        dim_ctx.dims,
   387→        fallback_max_files=options.max_files_per_batch,
   388→    )
   389→    include_full_sweep = bool(options.include_full_sweep)
   390→    if options.dimensions:
   391→        include_full_sweep = False
   392→    if include_full_sweep:
   393→        append_full_sweep_batch_fn(
   394→            batches=batches,
   395→            dims=dim_ctx.dims,
   396→            all_files=all_files,
   397→            lang=lang,
   398→            max_files=options.max_files_per_batch,
   399→        )
   400→    batches = filter_batches_to_file_scope(
   401→        batches,
   402→        allowed_files=allowed_review_files,
   403→    )
   404→
   405→    selected_prompts = _build_selected_prompts(
   406→        dim_ctx.dims, dim_ctx.holistic_prompts, dim_ctx.per_file_prompts,
   407→    )
   408→
   409→    payload: dict[str, Any] = {
   410→        "command": "review",
   411→        "mode": "holistic",
   412→        "language": lang.name,
   413→        "dimensions": dim_ctx.dims,
   414→        "dimension_prompts": selected_prompts,
   415→        "lang_guidance": dim_ctx.lang_guide,
   416→        "holistic_context": context.to_dict(),
   417→        "review_context": serialize_context_fn(review_ctx),
   418→        "system_prompt": dim_ctx.system_prompt,
   419→        "total_files": context.codebase_stats.get("total_files", 0),
   420→        "workflow": HOLISTIC_WORKFLOW,
   421→        "invalid_dimensions": {
   422→            "requested": dim_ctx.invalid_requested,
   423→            "default": dim_ctx.invalid_default,
   424→        },
   425→    }
   426→
   427→    batches = _attach_issue_history_context(
   428→        payload, batches, state, options, allowed_review_files,
   429→    )
   430→
   431→    payload["investigation_batches"] = batches
   432→    return payload
   433→
   434→
   435→__all__ = ["prepare_holistic_review_payload"]
   436→
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_batches.py"
}
```

> TOOL

tool_result Read
```
1→"""Holistic investigation batch builders for review preparation."""
     2→
     3→from __future__ import annotations
     4→
     5→from pathlib import Path
     6→
     7→from desloppify.intelligence.review._context.models import HolisticContext
     8→
     9→_EXTENSIONLESS_FILENAMES = {
    10→    "makefile",
    11→    "dockerfile",
    12→    "readme",
    13→    "license",
    14→    "build",
    15→    "workspace",
    16→}
    17→
    18→_GOVERNANCE_REFERENCE_FILES: tuple[str, ...] = (
    19→    "README.md",
    20→    "DEVELOPMENT_PHILOSOPHY.md",
    21→    "desloppify/README.md",
    22→    "pyproject.toml",
    23→)
    24→
    25→
    26→def _normalize_file_path(value: object) -> str | None:
    27→    """Normalize/validate candidate file paths for batch payloads."""
    28→    if not isinstance(value, str):
    29→        return None
    30→    text = value.strip().strip(",'\"")
    31→    if not text or text in {".", ".."}:
    32→        return None
    33→    if text.endswith("/"):
    34→        return None
    35→
    36→    basename = Path(text).name
    37→    if not basename:
    38→        return None
    39→    if "." not in basename and basename.lower() not in _EXTENSIONLESS_FILENAMES:
    40→        return None
    41→    return text
    42→
    43→
    44→def _collect_unique_files(
    45→    sources: list[list[dict]],
    46→    key: str = "file",
    47→    *,
    48→    max_files: int | None = None,
    49→) -> list[str]:
    50→    """Collect unique file paths from multiple source lists."""
    51→    seen: set[str] = set()
    52→    out: list[str] = []
    53→    for src in sources:
    54→        for item in src:
    55→            f = _normalize_file_path(item.get(key, ""))
    56→            if f and f not in seen:
    57→                seen.add(f)
    58→                out.append(f)
    59→                if max_files is not None and len(out) >= max_files:
    60→                    return out
    61→    return out
    62→
    63→
    64→def _existing_repo_files(
    65→    repo_root: Path | None,
    66→    candidates: tuple[str, ...],
    67→) -> list[str]:
    68→    """Return repository-relative paths for candidate files that exist."""
    69→    if repo_root is None:
    70→        return []
    71→    out: list[str] = []
    72→    for candidate in candidates:
    73→        if (repo_root / candidate).is_file():
    74→            out.append(candidate)
    75→    return out
    76→
    77→
    78→def _collect_files_from_batches(
    79→    batches: list[dict], *, max_files: int | None = None
    80→) -> list[str]:
    81→    """Collect unique file paths across batch payloads (preserving order)."""
    82→    seen: set[str] = set()
    83→    out: list[str] = []
    84→    for batch in batches:
    85→        for filepath in batch.get("files_to_read", []):
    86→            normalized = _normalize_file_path(filepath)
    87→            if not normalized:
    88→                continue
    89→            if normalized in seen:
    90→                continue
    91→            seen.add(normalized)
    92→            out.append(normalized)
    93→            if max_files is not None and len(out) >= max_files:
    94→                return out
    95→    return out
    96→
    97→
    98→def _representative_files_for_directory(
    99→    ctx: HolisticContext,
   100→    directory: str,
   101→    *,
   102→    max_files: int = 3,
   103→) -> list[str]:
   104→    """Map a directory-level signal to representative file paths."""
   105→    if not isinstance(directory, str) or not directory.strip():
   106→        return []
   107→
   108→    dir_key = directory.strip()
   109→    if dir_key in {".", "./"}:
   110→        normalized_dir = "."
   111→    else:
   112→        normalized_dir = f"{dir_key.rstrip('/')}/"
   113→
   114→    profiles = ctx.structure.get("directory_profiles", {})
   115→    profile = profiles.get(normalized_dir)
   116→    if not isinstance(profile, dict):
   117→        return []
   118→
   119→    out: list[str] = []
   120→    for filename in profile.get("files", []):
   121→        if not isinstance(filename, str) or not filename:
   122→            continue
   123→        filepath = (
   124→            filename
   125→            if normalized_dir == "."
   126→            else f"{normalized_dir.rstrip('/')}/{filename}"
   127→        )
   128→        normalized = _normalize_file_path(filepath)
   129→        if not normalized or normalized in out:
   130→            continue
   131→        out.append(normalized)
   132→        if len(out) >= max_files:
   133→            break
   134→    return out
   135→
   136→
   137→def _batch_arch_coupling(ctx: HolisticContext, *, max_files: int | None = None) -> dict:
   138→    """Batch 1: Architecture & Coupling - god modules, import-time side effects."""
   139→    files = _collect_unique_files(
   140→        [
   141→            ctx.architecture.get("god_modules", []),
   142→            ctx.coupling.get("module_level_io", []),
   143→            ctx.coupling.get("boundary_violations", []),
   144→            ctx.dependencies.get("deferred_import_density", []),
   145→        ],
   146→        max_files=max_files,
   147→    )
   148→    return {
   149→        "name": "Architecture & Coupling",
   150→        "dimensions": ["cross_module_architecture", "high_level_elegance"],
   151→        "files_to_read": files,
   152→        "why": "god modules, import-time side effects, boundary violations, deferred import pressure",
   153→    }
   154→
   155→
   156→def _batch_conventions_errors(
   157→    ctx: HolisticContext, *, max_files: int | None = None
   158→) -> dict:
   159→    """Batch 2: Conventions & Errors - sibling behavior outliers, mixed strategies."""
   160→    sibling = ctx.conventions.get("sibling_behavior", {})
   161→    outlier_files = [
   162→        {"file": o["file"]} for di in sibling.values() for o in di.get("outliers", [])
   163→    ]
   164→    error_dirs = ctx.errors.get("strategy_by_directory", {})
   165→    mixed_dir_files: list[dict[str, str]] = []
   166→    for directory, strategies in error_dirs.items():
   167→        if not isinstance(strategies, dict) or len(strategies) < 3:
   168→            continue
   169→        for filepath in _representative_files_for_directory(ctx, directory):
   170→            mixed_dir_files.append({"file": filepath})
   171→
   172→    exception_files = [
   173→        {"file": item.get("file", "")}
   174→        for item in ctx.errors.get("exception_hotspots", [])
   175→        if isinstance(item, dict)
   176→    ]
   177→    dupe_files = [
   178→        {"file": item.get("files", [""])[0]}
   179→        for item in ctx.conventions.get("duplicate_clusters", [])
   180→        if isinstance(item, dict) and item.get("files")
   181→    ]
   182→    naming_drift_files: list[dict[str, str]] = []
   183→    for entry in ctx.conventions.get("naming_drift", []):
   184→        if isinstance(entry, dict):
   185→            directory = entry.get("directory", "")
   186→            for filepath in _representative_files_for_directory(ctx, directory):
   187→                naming_drift_files.append({"file": filepath})
   188→
   189→    files = _collect_unique_files(
   190→        [outlier_files, mixed_dir_files, exception_files, dupe_files, naming_drift_files],
   191→        max_files=max_files,
   192→    )
   193→    return {
   194→        "name": "Conventions & Errors",
   195→        "dimensions": ["convention_outlier", "error_consistency", "mid_level_elegance"],
   196→        "files_to_read": files,
   197→        "why": "naming drift, behavioral outliers, mixed error strategies, exception hotspots, duplicate clusters",
   198→    }
   199→
   200→
   201→def _batch_abstractions_deps(
   202→    ctx: HolisticContext, *, max_files: int | None = None
   203→) -> dict:
   204→    """Batch 3: Abstractions & Dependencies - abstraction hotspots, dep cycles."""
   205→    util_files = ctx.abstractions.get("util_files", [])
   206→    wrapper_files = [
   207→        {"file": item.get("file", "")}
   208→        for item in ctx.abstractions.get("pass_through_wrappers", [])
   209→        if isinstance(item, dict)
   210→    ]
   211→    indirection_files = [
   212→        {"file": item.get("file", "")}
   213→        for item in ctx.abstractions.get("indirection_hotspots", [])
   214→        if isinstance(item, dict)
   215→    ]
   216→    param_bag_files = [
   217→        {"file": item.get("file", "")}
   218→        for item in ctx.abstractions.get("wide_param_bags", [])
   219→        if isinstance(item, dict)
   220→    ]
   221→    interface_files: list[dict[str, str]] = []
   222→    for item in ctx.abstractions.get("one_impl_interfaces", []):
   223→        if not isinstance(item, dict):
   224→            continue
   225→        for group in ("declared_in", "implemented_in"):
   226→            for filepath in item.get(group, []):
   227→                interface_files.append({"file": filepath})
   228→
   229→    delegation_files = [
   230→        {"file": item.get("file", "")}
   231→        for item in ctx.abstractions.get("delegation_heavy_classes", [])
   232→        if isinstance(item, dict)
   233→    ]
   234→    facade_files = [
   235→        {"file": item.get("file", "")}
   236→        for item in ctx.abstractions.get("facade_modules", [])
   237→        if isinstance(item, dict)
   238→    ]
   239→    type_violation_files = [
   240→        {"file": item.get("file", "")}
   241→        for item in ctx.abstractions.get("typed_dict_violations", [])
   242→        if isinstance(item, dict)
   243→    ]
   244→
   245→    complexity_files = [
   246→        {"file": item.get("file", "")}
   247→        for item in ctx.abstractions.get("complexity_hotspots", [])
   248→        if isinstance(item, dict)
   249→    ]
   250→
   251→    cycle_files: list[dict] = []
   252→    for summary in ctx.dependencies.get("cycle_summaries", []):
   253→        for token in summary.split():
   254→            if "/" in token and "." in token:
   255→                cycle_files.append({"file": token.strip(",'\"")})
   256→    files = _collect_unique_files(
   257→        [
   258→            util_files,
   259→            wrapper_files,
   260→            indirection_files,
   261→            param_bag_files,
   262→            interface_files,
   263→            delegation_files,
   264→            facade_files,
   265→            type_violation_files,
   266→            complexity_files,
   267→            cycle_files,
   268→        ],
   269→        max_files=max_files,
   270→    )
   271→    return {
   272→        "name": "Abstractions & Dependencies",
   273→        "dimensions": [
   274→            "abstraction_fitness",
   275→            "dependency_health",
   276→            "mid_level_elegance",
   277→            "low_level_elegance",
   278→        ],
   279→        "files_to_read": files,
   280→        "why": "abstraction hotspots (wrappers/interfaces/param bags/delegation-heavy classes/facade modules/TypedDict violations), dep cycles",
   281→    }
   282→
   283→
   284→def _batch_testing_api(ctx: HolisticContext, *, max_files: int | None = None) -> dict:
   285→    """Batch 4: Testing & API - critical untested paths, sync/async mix."""
   286→    critical = ctx.testing.get("critical_untested", [])
   287→    sync_async = [{"file": f} for f in ctx.api_surface.get("sync_async_mix", [])]
   288→    files = _collect_unique_files([critical, sync_async], max_files=max_files)
   289→    return {
   290→        "name": "Testing & API",
   291→        "dimensions": ["test_strategy", "api_surface_coherence", "mid_level_elegance"],
   292→        "files_to_read": files,
   293→        "why": "critical untested paths, API inconsistency",
   294→    }
   295→
   296→
   297→def _batch_authorization(ctx: HolisticContext, *, max_files: int | None = None) -> dict:
   298→    """Batch 5: Authorization - auth gaps, service role usage, RLS coverage."""
   299→    auth_ctx = ctx.authorization
   300→    auth_files: list[dict] = []
   301→    for rpath, info in auth_ctx.get("route_auth_coverage", {}).items():
   302→        if info.get("without_auth", 0) > 0:
   303→            auth_files.append({"file": rpath})
   304→    for rpath in auth_ctx.get("service_role_usage", []):
   305→        auth_files.append({"file": rpath})
   306→    # Include SQL/migration files that define tables without RLS
   307→    rls_coverage = auth_ctx.get("rls_coverage", {})
   308→    rls_files = rls_coverage.get("files", {})
   309→    if isinstance(rls_files, dict):
   310→        for _table, file_paths in rls_files.items():
   311→            if isinstance(file_paths, list):
   312→                for fpath in file_paths:
   313→                    auth_files.append({"file": fpath})
   314→    files = _collect_unique_files([auth_files], max_files=max_files)
   315→    return {
   316→        "name": "Authorization",
   317→        "dimensions": ["authorization_consistency", "mid_level_elegance"],
   318→        "files_to_read": files,
   319→        "why": "auth gaps, service role usage, RLS coverage",
   320→    }
   321→
   322→
   323→def _batch_ai_debt_migrations(
   324→    ctx: HolisticContext, *, max_files: int | None = None
   325→) -> dict:
   326→    """Batch 6: AI Debt & Migrations - deprecated markers, migration TODOs."""
   327→    ai_debt = ctx.ai_debt_signals
   328→    migration = ctx.migration_signals
   329→    debt_files: list[dict] = []
   330→    for rpath in ai_debt.get("file_signals", {}):
   331→        debt_files.append({"file": rpath})
   332→    dep_files = migration.get("deprecated_markers", {}).get("files")
   333→    if isinstance(dep_files, dict):
   334→        for entry in dep_files:
   335→            debt_files.append({"file": entry})
   336→    for entry in migration.get("migration_todos", []):
   337→        debt_files.append({"file": entry.get("file", "")})
   338→    files = _collect_unique_files([debt_files], max_files=max_files)
   339→    return {
   340→        "name": "AI Debt & Migrations",
   341→        "dimensions": [
   342→            "ai_generated_debt",
   343→            "incomplete_migration",
   344→            "low_level_elegance",
   345→        ],
   346→        "files_to_read": files,
   347→        "why": "AI-generated patterns, deprecated markers, migration TODOs",
   348→    }
   349→
   350→
   351→def _batch_package_organization(
   352→    ctx: HolisticContext, *, max_files: int | None = None
   353→) -> dict:
   354→    """Batch 7: Package Organization - file placement, directory boundaries."""
   355→    structure = ctx.structure
   356→    struct_files: list[dict] = []
   357→    # Add flat_dir_issues directory representatives
   358→    for entry in structure.get("flat_dir_issues", []):
   359→        if isinstance(entry, dict):
   360→            directory = entry.get("directory", "")
   361→            for filepath in _representative_files_for_directory(ctx, directory):
   362→                struct_files.append({"file": filepath})
   363→    for rf in structure.get("root_files", []):
   364→        if rf.get("role") == "peripheral":
   365→            struct_files.append({"file": rf["file"]})
   366→    dir_profiles = structure.get("directory_profiles", {})
   367→    largest_dirs = sorted(
   368→        dir_profiles.items(), key=lambda x: -x[1].get("file_count", 0)
   369→    )[:3]
   370→    for dir_key, profile in largest_dirs:
   371→        for fname in profile.get("files", [])[:3]:
   372→            dir_path = dir_key.rstrip("/")
   373→            rpath = f"{dir_path}/{fname}" if dir_path != "." else fname
   374→            struct_files.append({"file": rpath})
   375→    coupling_matrix = structure.get("coupling_matrix", {})
   376→    seen_edges: set[str] = set()
   377→    for edge in coupling_matrix:
   378→        if " → " in edge:
   379→            a, b = edge.split(" → ", 1)
   380→            reverse = f"{b} → {a}"
   381→            if reverse in coupling_matrix and edge not in seen_edges:
   382→                seen_edges.add(edge)
   383→                seen_edges.add(reverse)
   384→                for d in (a, b):
   385→                    for fname in dir_profiles.get(d, {}).get("files", [])[:2]:
   386→                        dir_path = d.rstrip("/")
   387→                        rpath = f"{dir_path}/{fname}" if dir_path != "." else fname
   388→                        struct_files.append({"file": rpath})
   389→    files = _collect_unique_files([struct_files], max_files=max_files)
   390→    return {
   391→        "name": "Package Organization",
   392→        "dimensions": ["package_organization", "high_level_elegance"],
   393→        "files_to_read": files,
   394→        "why": "file placement, directory boundaries, architectural layering",
   395→    }
   396→
   397→
   398→def _batch_state_design(ctx: HolisticContext, *, max_files: int | None = None) -> dict:
   399→    """Batch 8: State & Design Integrity - mutable globals, signal density hotspots."""
   400→    evidence = ctx.scan_evidence
   401→    mutable_files = [
   402→        item for item in evidence.get("mutable_globals", [])
   403→        if isinstance(item, dict)
   404→    ]
   405→    complexity_files = [
   406→        item for item in evidence.get("complexity_hotspots", [])[:10]
   407→        if isinstance(item, dict)
   408→    ]
   409→    error_files = [
   410→        item for item in evidence.get("error_hotspots", [])[:10]
   411→        if isinstance(item, dict)
   412→    ]
   413→    density_files = [
   414→        {"file": item["file"]}
   415→        for item in evidence.get("signal_density", [])[:10]
   416→        if isinstance(item, dict) and item.get("file")
   417→    ]
   418→    files = _collect_unique_files(
   419→        [mutable_files, complexity_files, error_files, density_files],
   420→        max_files=max_files,
   421→    )
   422→    return {
   423→        "name": "State & Design Integrity",
   424→        "dimensions": ["initialization_coupling", "design_coherence"],
   425→        "files_to_read": files,
   426→        "why": "mutable global state, concentrated quality signals, initialization coupling patterns",
   427→    }
   428→
   429→
   430→def _batch_governance_contracts(
   431→    ctx: HolisticContext,
   432→    *,
   433→    repo_root: Path | None,
   434→    max_files: int | None = None,
   435→) -> dict:
   436→    """Batch 8: Governance & Contracts - docs/policy promises vs runtime posture."""
   437→    docs = _existing_repo_files(repo_root, _GOVERNANCE_REFERENCE_FILES)
   438→    if not docs:
   439→        return {
   440→            "name": "Governance & Contracts",
   441→            "dimensions": [
   442→                "cross_module_architecture",
   443→                "high_level_elegance",
   444→                "test_strategy",
   445→                "package_organization",
   446→            ],
   447→            "files_to_read": [],
   448→            "why": "architecture contracts, compatibility policy, docs-vs-runtime scope, and quality-gate coverage",
   449→        }
   450→    top_imported = [
   451→        {"file": filepath}
   452→        for filepath in list(ctx.architecture.get("top_imported", {}).keys())[:5]
   453→        if isinstance(filepath, str)
   454→    ]
   455→    anchor_files = _collect_unique_files(
   456→        [
   457→            top_imported,
   458→            ctx.architecture.get("god_modules", []),
   459→            ctx.coupling.get("module_level_io", []),
   460→        ],
   461→        max_files=5,
   462→    )
   463→    seen = set(docs)
   464→    files = list(docs)
   465→    for filepath in anchor_files:
   466→        if filepath in seen:
   467→            continue
   468→        seen.add(filepath)
   469→        files.append(filepath)
   470→    if max_files is not None:
   471→        files = files[:max_files]
   472→    return {
   473→        "name": "Governance & Contracts",
   474→        "dimensions": [
   475→            "cross_module_architecture",
   476→            "high_level_elegance",
   477→            "test_strategy",
   478→            "package_organization",
   479→        ],
   480→        "files_to_read": files,
   481→        "why": "architecture contracts, compatibility policy, docs-vs-runtime scope, and quality-gate coverage",
   482→    }
   483→
   484→
   485→def _ensure_holistic_context(holistic_ctx: HolisticContext | dict) -> HolisticContext:
   486→    if isinstance(holistic_ctx, HolisticContext):
   487→        return holistic_ctx
   488→    return HolisticContext.from_raw(holistic_ctx)
   489→
   490→
   491→def build_investigation_batches(
   492→    holistic_ctx: HolisticContext | dict,
   493→    lang: object,
   494→    *,
   495→    repo_root: Path | None = None,
   496→    max_files_per_batch: int | None = None,
   497→) -> list[dict]:
   498→    """Derive parallelizable investigation batches from holistic context."""
   499→    ctx = _ensure_holistic_context(holistic_ctx)
   500→    del lang  # Reserved for future language-specific batch shaping.
   501→    batches = [
   502→        _batch_arch_coupling(ctx, max_files=max_files_per_batch),
   503→        _batch_conventions_errors(ctx, max_files=max_files_per_batch),
   504→        _batch_abstractions_deps(ctx, max_files=max_files_per_batch),
   505→        _batch_testing_api(ctx, max_files=max_files_per_batch),
   506→        _batch_authorization(ctx, max_files=max_files_per_batch),
   507→        _batch_ai_debt_migrations(ctx, max_files=max_files_per_batch),
   508→        _batch_package_organization(ctx, max_files=max_files_per_batch),
   509→        _batch_state_design(ctx, max_files=max_files_per_batch),
   510→        _batch_governance_contracts(
   511→            ctx,
   512→            repo_root=repo_root,
   513→            max_files=max_files_per_batch,
   514→        ),
   515→    ]
   516→    return [batch for batch in batches if batch["files_to_read"]]
   517→
   518→
   519→def filter_batches_to_dimensions(
   520→    batches: list[dict],
   521→    dimensions: list[str],
   522→    *,
   523→    fallback_max_files: int | None = 80,
   524→) -> list[dict]:
   525→    """Keep only dimensions explicitly active for this holistic review run.
   526→
   527→    If selected dimensions are not represented by any batch mapping, append a
   528→    fallback batch over representative files so scoped runs still get guidance.
   529→    """
   530→    selected = [d for d in dimensions if isinstance(d, str) and d]
   531→    if not selected:
   532→        return []
   533→    selected_set = set(selected)
   534→    filtered: list[dict] = []
   535→    covered: set[str] = set()
   536→    for batch in batches:
   537→        batch_dims = [dim for dim in batch.get("dimensions", []) if dim in selected_set]
   538→        if not batch_dims:
   539→            continue
   540→        filtered.append({**batch, "dimensions": batch_dims})
   541→        covered.update(batch_dims)
   542→
   543→    missing = [dim for dim in selected if dim not in covered]
   544→    if not missing:
   545→        return filtered
   546→
   547→    # Keep fallback batches tractable; giant sweeps are expensive and often
   548→    # unnecessary when dimensions are already explicitly scoped.
   549→    max_files = fallback_max_files if isinstance(fallback_max_files, int) else None
   550→    if isinstance(max_files, int) and max_files <= 0:
   551→        max_files = None
   552→    fallback_files = _collect_files_from_batches(filtered or batches, max_files=max_files)
   553→    if not fallback_files:
   554→        return filtered
   555→
   556→    filtered.append(
   557→        {
   558→            "name": "Cross-cutting Sweep",
   559→            "dimensions": missing,
   560→            "files_to_read": fallback_files,
   561→            "why": "selected dimensions had no direct batch mapping; review representative cross-cutting files",
   562→        }
   563→    )
   564→    return filtered
   565→
   566→
   567→def batch_concerns(
   568→    concerns: list,
   569→    *,
   570→    max_files: int | None = None,
   571→    active_dimensions: list[str] | None = None,
   572→) -> dict | None:
   573→    """Build investigation batch from mechanical concern signals.
   574→
   575→    *concerns* should be a list of Concern dataclass instances from
   576→    ``desloppify.engine.concerns``.
   577→    """
   578→    if not concerns:
   579→        return None
   580→    default_dims = ["design_coherence", "initialization_coupling"]
   581→    selected_dims = [
   582→        dim for dim in (active_dimensions or [])
   583→        if isinstance(dim, str) and dim
   584→    ]
   585→    selected_set = set(selected_dims)
   586→    overlap_dims = [dim for dim in default_dims if dim in selected_set]
   587→    concern_dims = overlap_dims or list(default_dims)
   588→    mapped_to_active_dims = bool(selected_dims) and not overlap_dims
   589→    if mapped_to_active_dims:
   590→        # Prevent concern signals from being silently dropped by scoped runs.
   591→        concern_dims = list(selected_dims)
   592→
   593→    types = sorted({c.type for c in concerns if c.type})
   594→    why_parts = ["mechanical detectors identified structural patterns needing judgment"]
   595→    if types:
   596→        why_parts.append(f"concern types: {', '.join(types)}")
   597→    if mapped_to_active_dims:
   598→        why_parts.append(
   599→            "mapped to active dimensions because design_coherence/initialization_coupling are not selected"
   600→        )
   601→    files: list[str] = []
   602→    seen: set[str] = set()
   603→    concern_signals: list[dict[str, object]] = []
   604→    for concern in concerns:
   605→        candidate = _normalize_file_path(getattr(concern, "file", ""))
   606→        if not candidate or candidate in seen:
   607→            continue
   608→        seen.add(candidate)
   609→        files.append(candidate)
   610→
   611→        evidence_raw = getattr(concern, "evidence", ())
   612→        evidence = [
   613→            str(entry).strip()
   614→            for entry in evidence_raw
   615→            if isinstance(entry, str) and entry.strip()
   616→        ][:4]
   617→        summary = str(getattr(concern, "summary", "")).strip()
   618→        question = str(getattr(concern, "question", "")).strip()
   619→        concern_type = str(getattr(concern, "type", "")).strip()
   620→        concern_signals.append(
   621→            {
   622→                "type": concern_type or "design_concern",
   623→                "file": candidate,
   624→                "summary": summary or "Mechanical concern requires subjective judgment",
   625→                "question": question or "Is this pattern intentional or debt?",
   626→                "evidence": evidence,
   627→            }
   628→        )
   629→
   630→    total_candidate_files = len(files)
   631→    if (
   632→        max_files is not None
   633→        and isinstance(max_files, int)
   634→        and max_files > 0
   635→        and total_candidate_files > max_files
   636→    ):
   637→        files = files[:max_files]
   638→        why_parts.append(
   639→            f"truncated to {max_files} files from {total_candidate_files} candidates"
   640→        )
   641→
   642→    return {
   643→        "name": "Design coherence — Mechanical Concern Signals",
   644→        "dimensions": concern_dims,
   645→        "files_to_read": files,
   646→        "why": "; ".join(why_parts),
   647→        "total_candidate_files": total_candidate_files,
   648→        "concern_signals": concern_signals[:12],
   649→        "concern_signal_count": len(concern_signals),
   650→        "mapped_to_active_dimensions": mapped_to_active_dims,
   651→    }
   652→
   653→
   654→__all__ = ["batch_concerns", "build_investigation_batches", "filter_batches_to_dimensions"]
   655→
```

> AGENT

Now I need to find where the "Full Codebase Sweep" batch is created and understand the sub-batch splitting logic:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"Full Codebase Sweep\" /Users/user_c042661f/Documents/desloppify --include=\"*.py\"",
  "description": "Search for Full Codebase Sweep batch creation"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py:            "name": "Full Codebase Sweep",
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/context/test_holistic_review.py:            if b["name"] == "Full Codebase Sweep"
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py:            "name": "Full Codebase Sweep",
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"append_full_sweep_batch\" /Users/user_c042661f/Documents/desloppify --include=\"*.py\" -B 2 -A 5",
  "description": "Search for append_full_sweep_batch function"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-    batch_concerns_fn,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-    filter_batches_to_dimensions_fn,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py:    append_full_sweep_batch_fn,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-    serialize_context_fn,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-    log_best_effort_failure_fn,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-    logger,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-) -> dict[str, object]:
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-    """Prepare holistic review payload with injected dependencies for patchability."""
--
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-        include_full_sweep = False
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-    if include_full_sweep:
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py:        append_full_sweep_batch_fn(
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-            batches=batches,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-            dims=dim_ctx.dims,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-            all_files=all_files,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-            lang=lang,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py-            max_files=options.max_files_per_batch,
--
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py-
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py-
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py:def append_full_sweep_batch(
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py-    *,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py-    batches: list[dict[str, Any]],
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py-    dims: list[str],
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py-    all_files: list[str],
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py-    lang: Any,
--
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-)
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py:from desloppify.intelligence.review._prepare.helpers import append_full_sweep_batch
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-from desloppify.intelligence.review.context import (
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-    abs_path,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-    build_review_context,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-    dep_graph_lookup,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-    importer_count,
--
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-        batch_concerns_fn=_batch_concerns,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-        filter_batches_to_dimensions_fn=_filter_batches_to_dimensions,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py:        append_full_sweep_batch_fn=append_full_sweep_batch,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-        serialize_context_fn=serialize_context,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-        log_best_effort_failure_fn=log_best_effort_failure,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-        logger=logger,
/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare.py-    )
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-from desloppify.intelligence.review._prepare.helpers import (
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-    HOLISTIC_WORKFLOW,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py:    append_full_sweep_batch,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-)
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-@dataclass
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-class _Zone:
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py:def test_append_full_sweep_batch_skips_non_production_files():
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-    lang = type("Lang", (), {"zone_map": _ZoneMap({"tests/test_a.py": "test"})})()
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-    batches: list[dict] = []
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py:    append_full_sweep_batch(
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-        batches=batches,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-        dims=["logic_clarity"],
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-        all_files=["src/a.py", "tests/test_a.py"],
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-        lang=lang,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-    )
--
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py:def test_append_full_sweep_batch_noop_without_dimensions():
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-    lang = type("Lang", (), {"zone_map": _ZoneMap({})})()
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-    batches: list[dict] = []
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py:    append_full_sweep_batch(
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-        batches=batches,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-        dims=[],
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-        all_files=["src/a.py"],
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-        lang=lang,
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/policy/test_prepare_internal_helpers.py-    )
--
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-    batch_concerns_fn,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-    filter_batches_to_dimensions_fn,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py:    append_full_sweep_batch_fn,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-    serialize_context_fn,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-    log_best_effort_failure_fn,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-    logger,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-) -> dict[str, object]:
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-    """Prepare holistic review payload with injected dependencies for patchability."""
--
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-        include_full_sweep = False
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-    if include_full_sweep:
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py:        append_full_sweep_batch_fn(
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-            batches=batches,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-            dims=dim_ctx.dims,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-            all_files=all_files,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-            lang=lang,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare_holistic_flow.py-            max_files=options.max_files_per_batch,
--
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py-
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py-
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py:def append_full_sweep_batch(
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py-    *,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py-    batches: list[dict[str, Any]],
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py-    dims: list[str],
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py-    all_files: list[str],
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/_prepare/helpers.py-    lang: Any,
--
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-)
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py:from desloppify.intelligence.review._prepare.helpers import append_full_sweep_batch
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-from desloppify.intelligence.review.context import (
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-    abs_path,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-    build_review_context,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-    dep_graph_lookup,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-    importer_count,
--
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-        batch_concerns_fn=_batch_concerns,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-        filter_batches_to_dimensions_fn=_filter_batches_to_dimensions,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py:        append_full_sweep_batch_fn=append_full_sweep_batch,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-        serialize_context_fn=serialize_context,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-        log_best_effort_failure_fn=log_best_effort_failure,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-        logger=logger,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/intelligence/review/prepare.py-    )
```

> AGENT

Let me read the helpers file:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py"
}
```

> TOOL

tool_result Read
```
1→"""Helpers used by holistic review preparation."""
     2→
     3→from __future__ import annotations
     4→
     5→from typing import Any
     6→
     7→from desloppify.base.discovery.file_paths import rel
     8→
     9→HOLISTIC_WORKFLOW = [
    10→    "Read .desloppify/query.json for context, excerpts, and investigation batches",
    11→    "For each batch: start from listed seed files, then explore likely hotspots/unreviewed neighbors; evaluate the batch's dimensions (batches are independent — parallelize)",
    12→    "Cross-reference issues with the sibling_behavior and convention data",
    13→    "IMPORTANT: issues must be defects only — never positive observations. High scores capture quality; issues capture problems.",
    14→    "Write ALL issues to issues.json — do NOT fix code before importing. Import creates tracked state entries that let desloppify correlate fixes to issues.",
    15→    "Codex: desloppify review --run-batches --runner codex --parallel --scan-after-import",
    16→    "Claude / other agent: desloppify review --run-batches --dry-run → launch one subagent per prompt file (all in parallel) → desloppify review --import-run <run-dir> --scan-after-import",
    17→    "Cloud/external: run `desloppify review --external-start --external-runner claude`, follow the session template, then run the printed `--external-submit` command",
    18→    "Fallback path: `desloppify review --import issues.json` (issues only). Use manual override only for emergency/provisional imports.",
    19→    "AFTER importing: run `desloppify show review --status open` to see the work queue, then fix each issue in code and `desloppify plan resolve <id>`",
    20→]
    21→
    22→
    23→def append_full_sweep_batch(
    24→    *,
    25→    batches: list[dict[str, Any]],
    26→    dims: list[str],
    27→    all_files: list[str],
    28→    lang: Any,
    29→    max_files: int | None = None,
    30→) -> None:
    31→    """Append an optional cross-cutting full-codebase batch."""
    32→    if not dims:
    33→        return
    34→    all_rel_files: list[str] = []
    35→    for filepath in all_files:
    36→        if lang.zone_map is not None:
    37→            zone = lang.zone_map.get(filepath)
    38→            if zone.value in ("test", "generated", "vendor"):
    39→                continue
    40→        all_rel_files.append(rel(filepath))
    41→        if isinstance(max_files, int) and max_files > 0 and len(all_rel_files) >= max_files:
    42→            break
    43→    if not all_rel_files:
    44→        return
    45→    batches.append(
    46→        {
    47→            "name": "Full Codebase Sweep",
    48→            "dimensions": list(dims),
    49→            "files_to_read": all_rel_files,
    50→            "why": "thorough default: evaluate cross-cutting quality across all production files",
    51→        }
    52→    )
    53→
```

> AGENT

Now let me search for where the 9 batches get expanded to 46 prompt files. This is likely in the execution or prompt generation logic:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"explode_to_single_dimension\\|prompt_sections\\|batch.*split\" /Users/user_c042661f/Documents/desloppify --include=\"*.py\" | head -30",
  "description": "Search for batch splitting logic"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prompt_sections.py:def explode_to_single_dimension(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prompt_sections.py:    "explode_to_single_dimension",
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py:from ..prompt_sections import explode_to_single_dimension
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py:    batches = explode_to_single_dimension(
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/prompt_template.py:from ..prompt_sections import (
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/prompt_template.py:    """Extract dimension prompts embedded by explode_to_single_dimension."""
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/external.py:from .prompt_sections import (
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/external.py:    explode_to_single_dimension,
/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/external.py:    batches = explode_to_single_dimension(
/Users/user_c042661f/Documents/desloppify/desloppify/tests/review/import_scoring/test_review_external.py:from desloppify.app.commands.review.prompt_sections import (
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/prompt_sections.py:def explode_to_single_dimension(
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/prompt_sections.py:    "explode_to_single_dimension",
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/batch/execution.py:from ..prompt_sections import explode_to_single_dimension
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/batch/execution.py:    batches = explode_to_single_dimension(
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/batch/prompt_template.py:from ..prompt_sections import (
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/batch/prompt_template.py:    """Extract dimension prompts embedded by explode_to_single_dimension."""
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/external.py:from .prompt_sections import (
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/external.py:    explode_to_single_dimension,
/Users/user_c042661f/Documents/desloppify/build/lib/desloppify/app/commands/review/external.py:    batches = explode_to_single_dimension(
```

> AGENT

Perfect! Now let me read the prompt_sections file to understand the explode logic:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prompt_sections.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1→"""Shared prompt rendering sections used by both batch and external review paths."""
     2→
     3→from __future__ import annotations
     4→
     5→from dataclasses import dataclass
     6→
     7→from desloppify.intelligence.review.feedback_contract import (
     8→    max_batch_issues_for_dimension_count,
     9→)
    10→
    11→
    12→@dataclass(frozen=True)
    13→class PromptBatchContext:
    14→    name: str
    15→    dimensions: tuple[str, ...]
    16→    rationale: str
    17→    seed_files: tuple[str, ...]
    18→    issues_cap: int
    19→
    20→    @property
    21→    def dimension_set(self) -> set[str]:
    22→        return set(self.dimensions)
    23→
    24→    @property
    25→    def dimensions_text(self) -> str:
    26→        return ", ".join(self.dimensions) if self.dimensions else "(none)"
    27→
    28→    @property
    29→    def seed_files_text(self) -> str:
    30→        return "\n".join(f"- {path}" for path in self.seed_files) if self.seed_files else "- (none)"
    31→
    32→
    33→def coerce_string_list(raw: object) -> tuple[str, ...]:
    34→    if not isinstance(raw, list | tuple):
    35→        return ()
    36→    return tuple(str(item) for item in raw if isinstance(item, str) and item)
    37→
    38→
    39→def build_batch_context(batch: dict[str, object], batch_index: int) -> PromptBatchContext:
    40→    dimensions = coerce_string_list(batch.get("dimensions", []))
    41→    return PromptBatchContext(
    42→        name=str(batch.get("name", f"Batch {batch_index + 1}")),
    43→        dimensions=dimensions,
    44→        rationale=str(batch.get("why", "")).strip(),
    45→        seed_files=coerce_string_list(batch.get("files_to_read", [])),
    46→        issues_cap=max_batch_issues_for_dimension_count(len(dimensions)),
    47→    )
    48→
    49→
    50→SCAN_EVIDENCE_FOCUS_BY_DIMENSION = {
    51→    "initialization_coupling": (
    52→        "9e. For initialization_coupling, use evidence from "
    53→        "`holistic_context.scan_evidence.mutable_globals` and "
    54→        "`holistic_context.errors.mutable_globals`. Investigate initialization ordering "
    55→        "dependencies, coupling through shared mutable state, and whether state should "
    56→        "be encapsulated behind a proper registry/context manager.\n"
    57→    ),
    58→    "design_coherence": (
    59→        "9f. For design_coherence, use evidence from "
    60→        "`holistic_context.scan_evidence.signal_density` — files where "
    61→        "multiple mechanical detectors fired. Investigate what design change would address "
    62→        "multiple signals simultaneously. Check `scan_evidence.complexity_hotspots` for "
    63→        "files with high responsibility cluster counts.\n"
    64→    ),
    65→    "error_consistency": (
    66→        "9g. For error_consistency, use evidence from "
    67→        "`holistic_context.errors.exception_hotspots` — files with "
    68→        "concentrated exception handling issues. Investigate whether error handling is "
    69→        "designed or accidental. Check for broad catches masking specific failure modes.\n"
    70→    ),
    71→    "cross_module_architecture": (
    72→        "9h. For cross_module_architecture, also consult "
    73→        "`holistic_context.coupling.boundary_violations` for import paths that "
    74→        "cross architectural boundaries, and `holistic_context.dependencies.deferred_import_density` "
    75→        "for files with many function-level imports (proxy for cycle pressure).\n"
    76→    ),
    77→    "convention_outlier": (
    78→        "9i. For convention_outlier, also consult "
    79→        "`holistic_context.conventions.duplicate_clusters` for cross-file "
    80→        "function duplication and `conventions.naming_drift` for directory-level naming "
    81→        "inconsistency.\n"
    82→    ),
    83→}
    84→
    85→
    86→def render_scan_evidence_focus(dim_set: set[str]) -> str:
    87→    """Render dimension-specific scan_evidence guidance."""
    88→    return "".join(
    89→        text
    90→        for dim, text in SCAN_EVIDENCE_FOCUS_BY_DIMENSION.items()
    91→        if dim in dim_set
    92→    )
    93→
    94→
    95→def render_historical_focus(batch: dict[str, object]) -> str:
    96→    focus = batch.get("historical_issue_focus")
    97→    if not isinstance(focus, dict):
    98→        return ""
    99→
   100→    selected_raw = focus.get("selected_count", 0)
   101→    try:
   102→        selected_count = max(0, int(selected_raw))
   103→    except (TypeError, ValueError):
   104→        selected_count = 0
   105→
   106→    issues = focus.get("issues", [])
   107→    if not isinstance(issues, list):
   108→        issues = []
   109→
   110→    if selected_count <= 0 or not issues:
   111→        return ""
   112→
   113→    lines: list[str] = []
   114→    lines.append(
   115→        "Previously flagged issues — navigation aid, not scoring evidence:"
   116→    )
   117→    lines.append(
   118→        "Check whether each issue still exists in the current code. Do not re-report"
   119→        " issues that have been fixed or marked wontfix — focus on what remains or"
   120→        " what is new. If several past issues share a root cause, call that out."
   121→    )
   122→
   123→    for entry in issues:
   124→        if not isinstance(entry, dict):
   125→            continue
   126→        status = str(entry.get("status", "")).strip()
   127→        summary = str(entry.get("summary", "")).strip()
   128→        note = str(entry.get("note", "")).strip()
   129→
   130→        line = f"  - [{status}] {summary}"
   131→        if note:
   132→            line += f" (note: {note})"
   133→        lines.append(line)
   134→    return "\n".join(lines) + "\n\n"
   135→
   136→
   137→def render_mechanical_concern_signals(batch: dict[str, object]) -> str:
   138→    """Render mechanically-generated concern hypotheses for this batch."""
   139→    signals = batch.get("concern_signals")
   140→    if not isinstance(signals, list) or not signals:
   141→        return ""
   142→
   143→    lines: list[str] = []
   144→    lines.append("Mechanical concern signals — navigation aid, not scoring evidence:")
   145→    lines.append(
   146→        "Confirm or refute each with your own code reading. Report only confirmed defects."
   147→    )
   148→
   149→    shown = 0
   150→    for entry in signals:
   151→        if not isinstance(entry, dict):
   152→            continue
   153→        file = str(entry.get("file", "")).strip() or "(unknown file)"
   154→        concern_type = str(entry.get("type", "")).strip() or "design_concern"
   155→        summary = str(entry.get("summary", "")).strip()
   156→        question = str(entry.get("question", "")).strip()
   157→        evidence_raw = entry.get("evidence", [])
   158→        evidence = (
   159→            [str(item).strip() for item in evidence_raw if isinstance(item, str) and item.strip()]
   160→            if isinstance(evidence_raw, list)
   161→            else []
   162→        )
   163→
   164→        lines.append(f"  - [{concern_type}] {file}")
   165→        if summary:
   166→            lines.append(f"    summary: {summary}")
   167→        if question:
   168→            lines.append(f"    question: {question}")
   169→        for snippet in evidence[:2]:
   170→            lines.append(f"    evidence: {snippet}")
   171→        shown += 1
   172→        if shown >= 8:
   173→            break
   174→
   175→    extra = max(0, len(signals) - shown)
   176→    if extra:
   177→        lines.append(f"  - (+{extra} more concern signals)")
   178→    return "\n".join(lines) + "\n\n"
   179→
   180→
   181→def render_workflow_integrity_focus(dim_set: set[str]) -> str:
   182→    """Render workflow integrity checks for architecture/integration dimensions."""
   183→    if not dim_set.intersection(
   184→        {
   185→            "cross_module_architecture",
   186→            "high_level_elegance",
   187→            "mid_level_elegance",
   188→            "design_coherence",
   189→            "initialization_coupling",
   190→        }
   191→    ):
   192→        return ""
   193→    return (
   194→        "9j. Workflow integrity checks: when reviewing orchestration/queue/review flows,\n"
   195→        "    explicitly look for loop-prone patterns and blind spots:\n"
   196→        "    - repeated stale/reopen churn without clear exit criteria or gating,\n"
   197→        "    - packet/batch data being generated but dropped before prompt execution,\n"
   198→        "    - ranking/triage logic that can starve target-improving work,\n"
   199→        "    - reruns happening before existing open review work is drained.\n"
   200→        "    If found, propose concrete guardrails and where to implement them.\n"
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prompt_sections.py",
  "offset": 200
}
```

> TOOL

tool_result Read
```
200→        "    If found, propose concrete guardrails and where to implement them.\n"
   201→    )
   202→
   203→
   204→def render_package_org_focus(dim_set: set[str]) -> str:
   205→    if "package_organization" not in dim_set:
   206→        return ""
   207→    return (
   208→        "9a. For package_organization, ground scoring in objective structure signals from "
   209→        "`holistic_context.structure` (root_files fan_in/fan_out roles, directory_profiles, "
   210→        "coupling_matrix). Prefer thresholded evidence (for example: fan_in < 5 for root "
   211→        "stragglers, import-affinity > 60%, directories > 10 files with mixed concerns).\n"
   212→        "9b. Suggestions must include a staged reorg plan (target folders, move order, "
   213→        "and import-update/validation commands).\n"
   214→        "9c. Also consult `holistic_context.structure.flat_dir_issues` for directories "
   215→        "flagged as overloaded, fragmented, or thin-wrapper patterns.\n"
   216→    )
   217→
   218→
   219→def render_abstraction_focus(dim_set: set[str]) -> str:
   220→    if "abstraction_fitness" not in dim_set:
   221→        return ""
   222→    return (
   223→        "9d. For abstraction_fitness, use evidence from `holistic_context.abstractions`:\n"
   224→        "  - `delegation_heavy_classes`: classes where most methods forward to an inner "
   225→        "object — entries include class_name, delegate_target, sample_methods, and line number.\n"
   226→        "  - `facade_modules`: re-export-only modules with high re_export_ratio — entries "
   227→        "include samples (re-exported names) and loc.\n"
   228→        "  - `typed_dict_violations`: TypedDict fields accessed via .get()/.setdefault()/.pop() "
   229→        "— entries include typed_dict_name, violation_type, field, and line number.\n"
   230→        "  - `complexity_hotspots`: files where mechanical analysis found extreme parameter "
   231→        "counts, deep nesting, or disconnected responsibility clusters.\n"
   232→        "  Include `delegation_density`, `definition_directness`, and `type_discipline` "
   233→        "alongside existing sub-axes in dimension_notes when evidence supports it.\n"
   234→    )
   235→
   236→
   237→def render_dimension_focus(dim_set: set[str]) -> str:
   238→    return (
   239→        render_package_org_focus(dim_set)
   240→        + render_abstraction_focus(dim_set)
   241→        + render_scan_evidence_focus(dim_set)
   242→        + render_workflow_integrity_focus(dim_set)
   243→    )
   244→
   245→
   246→def explode_to_single_dimension(
   247→    batches: list[dict[str, object]],
   248→    dimension_prompts: dict[str, dict[str, object]] | None = None,
   249→) -> list[dict[str, object]]:
   250→    """Split multi-dimension batches into one batch per dimension.
   251→
   252→    Preserves seed files and rationale — each exploded batch keeps the same
   253→    file grouping but is scoped to a single dimension.  When *dimension_prompts*
   254→    is provided, each exploded batch gets a ``_dimension_prompt`` key with the
   255→    prompt for its single dimension so that downstream renderers can use it
   256→    without extra parameter threading.
   257→    """
   258→    prompts = dimension_prompts or {}
   259→    result: list[dict[str, object]] = []
   260→    for batch in batches:
   261→        dims = batch.get("dimensions", [])
   262→        if not isinstance(dims, list):
   263→            result.append(batch)
   264→            continue
   265→        for dim in dims:
   266→            exploded: dict[str, object] = {**batch, "dimensions": [dim]}
   267→            dim_prompt = prompts.get(dim)
   268→            if isinstance(dim_prompt, dict):
   269→                exploded["_dimension_prompt"] = dim_prompt
   270→            result.append(exploded)
   271→    return result
   272→
   273→
   274→def render_dimension_prompts_block(
   275→    dimensions: tuple[str, ...],
   276→    dimension_prompts: dict[str, dict[str, object]],
   277→) -> str:
   278→    """Render inline dimension guidance so the reviewer sees the full rubric."""
   279→    if not dimensions or not dimension_prompts:
   280→        return ""
   281→    lines: list[str] = ["DIMENSION TO EVALUATE:\n"]
   282→    for dim in dimensions:
   283→        prompt = dimension_prompts.get(dim)
   284→        if not isinstance(prompt, dict):
   285→            lines.append(f"## {dim}\n(no rubric available)\n")
   286→            continue
   287→        description = str(prompt.get("description", "")).strip()
   288→        lines.append(f"## {dim}")
   289→        if description:
   290→            lines.append(description)
   291→
   292→        look_for = prompt.get("look_for")
   293→        if isinstance(look_for, list) and look_for:
   294→            lines.append("Look for:")
   295→            for item in look_for:
   296→                lines.append(f"- {item}")
   297→
   298→        skip = prompt.get("skip")
   299→        if isinstance(skip, list) and skip:
   300→            lines.append("Skip:")
   301→            for item in skip:
   302→                lines.append(f"- {item}")
   303→        lines.append("")
   304→    return "\n".join(lines) + "\n"
   305→
   306→
   307→def render_scoring_frame() -> str:
   308→    return (
   309→        "YOUR TASK: Read the code for this batch's dimension. Judge "
   310→        "how well the codebase serves a developer from that perspective. The dimension "
   311→        "rubric above defines what good looks like. "
   312→        "Cite specific observations that explain your judgment.\n\n"
   313→    )
   314→
   315→
   316→def render_scan_evidence_note() -> str:
   317→    return (
   318→        "Mechanical scan evidence — navigation aid, not scoring evidence:\n"
   319→        "The blind packet contains `holistic_context.scan_evidence` with aggregated signals "
   320→        "from all mechanical detectors — including complexity hotspots, error hotspots, signal "
   321→        "density index, boundary violations, and systemic patterns. Use these as starting "
   322→        "points for where to look beyond the seed files.\n\n"
   323→    )
   324→
   325→
   326→def render_seed_files_block(context: PromptBatchContext) -> str:
   327→    return f"Seed files (start here):\n{context.seed_files_text}\n\n"
   328→
   329→
   330→def render_task_requirements(*, issues_cap: int, dim_set: set[str]) -> str:
   331→    dim_focus = render_dimension_focus(dim_set)
   332→    # Build numbered items; dimension focus items get renumbered dynamically.
   333→    lines = [
   334→        "Task requirements:",
   335→        "1. Read the blind packet's `system_prompt` — it contains scoring rules and calibration.",
   336→        "2. Start from the seed files, then freely explore the repository to build your understanding.",
   337→        "3. Keep issues and scoring scoped to this batch's dimension.",
   338→        "4. Respect scope controls: do not include files/directories marked by `exclude`, `suppress`, or non-production zone overrides.",
   339→        f"5. Return 0-{issues_cap} issues for this batch (empty array allowed).",
   340→    ]
   341→    next_num = 6
   342→    if dim_focus:
   343→        for focus_line in dim_focus.rstrip("\n").split("\n"):
   344→            lines.append(f"{next_num}. {focus_line.lstrip('0123456789abcdefghij. ')}")
   345→            next_num += 1
   346→    lines.append(f"{next_num}. Do not edit repository files.")
   347→    next_num += 1
   348→    lines.append(f"{next_num}. Return ONLY valid JSON, no markdown fences.")
   349→    return "\n".join(lines) + "\n\n"
   350→
   351→
   352→def render_scope_enums() -> str:
   353→    return (
   354→        "Scope enums:\n"
   355→        '- impact_scope: "local" | "module" | "subsystem" | "codebase"\n'
   356→        '- fix_scope: "single_edit" | "multi_file_refactor" | "architectural_change"\n\n'
   357→    )
   358→
   359→
   360→def join_non_empty_sections(*sections: str) -> str:
   361→    return "".join(section for section in sections if section)
   362→
   363→
   364→__all__ = [
   365→    "PromptBatchContext",
   366→    "coerce_string_list",
   367→    "build_batch_context",
   368→    "explode_to_single_dimension",
   369→    "render_dimension_prompts_block",
   370→    "SCAN_EVIDENCE_FOCUS_BY_DIMENSION",
   371→    "render_scan_evidence_focus",
   372→    "render_historical_focus",
   373→    "render_mechanical_concern_signals",
   374→    "render_workflow_integrity_focus",
   375→    "render_package_org_focus",
   376→    "render_abstraction_focus",
   377→    "render_dimension_focus",
   378→    "render_scoring_frame",
   379→    "render_scan_evidence_note",
   380→    "render_seed_files_block",
   381→    "render_task_requirements",
   382→    "render_scope_enums",
   383→    "join_non_empty_sections",
   384→]
   385→
```

> AGENT

Excellent! Now let me check how this explode function is used in the batch execution:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py",
  "offset": 200,
  "limit": 100
}
```

> TOOL

tool_result Read
```
200→            append_run_log(
   201→                "stall-warning "
   202→                f"threshold={stall_warning_seconds}s batches={[idx + 1 for idx in sorted(newly_warned)]}"
   203→            )
   204→
   205→
   206→def _collect_and_reconcile_results(
   207→    *,
   208→    collect_batch_results_fn,
   209→    selected_indexes: list[int],
   210→    execution_failures: list[int],
   211→    output_files: dict,
   212→    packet: dict,
   213→    batch_positions: dict[int, int],
   214→    batch_status: dict[str, dict[str, object]],
   215→) -> tuple[list[dict], list[int], list[int], set[int]]:
   216→    """Collect batch results and reconcile per-batch status entries.
   217→
   218→    Returns (batch_results, successful_indexes, failures, failure_set).
   219→    """
   220→    allowed_dims = {
   221→        str(dim) for dim in packet.get("dimensions", []) if isinstance(dim, str)
   222→    }
   223→    batch_results, failures = collect_batch_results_fn(
   224→        selected_indexes=selected_indexes,
   225→        failures=execution_failures,
   226→        output_files=output_files,
   227→        allowed_dims=allowed_dims,
   228→    )
   229→
   230→    execution_failure_set = set(execution_failures)
   231→    failure_set = set(failures)
   232→    successful_indexes = sorted(idx for idx in selected_indexes if idx not in failure_set)
   233→    for idx in selected_indexes:
   234→        key = str(idx + 1)
   235→        state = batch_status.setdefault(
   236→            key,
   237→            {"position": batch_positions.get(idx, 0), "status": "pending"},
   238→        )
   239→        if idx not in failure_set:
   240→            state["status"] = "succeeded"
   241→            continue
   242→        if idx in execution_failure_set:
   243→            state["status"] = "failed"
   244→            continue
   245→        if not output_files[idx].exists():
   246→            state["status"] = "missing_output"
   247→            continue
   248→        state["status"] = "parse_failed"
   249→
   250→    return batch_results, successful_indexes, failures, failure_set
   251→
   252→
   253→def _merge_and_write_results(
   254→    *,
   255→    merge_batch_results_fn,
   256→    build_import_provenance_fn,
   257→    batch_results: list[dict],
   258→    batches: list,
   259→    successful_indexes: list[int],
   260→    packet: dict,
   261→    packet_dimensions: list[str],
   262→    scored_dimensions: list[str],
   263→    scan_path: str,
   264→    runner: str,
   265→    prompt_packet_path: Path,
   266→    stamp: str,
   267→    run_dir: Path,
   268→    safe_write_text_fn,
   269→    colorize_fn,
   270→) -> Path:
   271→    """Merge batch results, enrich with metadata, write to disk. Returns merged_path."""
   272→    merged = merge_batch_results_fn(batch_results)
   273→    reviewed_files = collect_reviewed_files_from_batches(
   274→        batches=batches,
   275→        selected_indexes=successful_indexes,
   276→    )
   277→    full_sweep_included = any(
   278→        str(batch.get("name", "")).strip().lower() == "full codebase sweep"
   279→        for idx in successful_indexes
   280→        if 0 <= idx < len(batches)
   281→        for batch in [batches[idx]]
   282→        if isinstance(batch, dict)
   283→    )
   284→    review_scope: dict[str, object] = {
   285→        "reviewed_files_count": len(reviewed_files),
   286→        "successful_batch_count": len(successful_indexes),
   287→        "full_sweep_included": full_sweep_included,
   288→    }
   289→    total_files = packet.get("total_files")
   290→    if isinstance(total_files, int) and not isinstance(total_files, bool) and total_files > 0:
   291→        review_scope["total_files"] = total_files
   292→    merged["review_scope"] = review_scope
   293→    if reviewed_files:
   294→        merged["reviewed_files"] = reviewed_files
   295→        print(
   296→            colorize_fn(
   297→                f"  Reviewed files captured for cache refresh: {len(reviewed_files)}",
   298→                "dim",
   299→            )
```

> AGENT

Let me find where explode_to_single_dimension is called in the execution flow:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"explode_to_single_dimension\" /Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py -A 10 -B 5",
  "description": "Find explode_to_single_dimension usage in execution"
}
```

> TOOL

tool_result Bash
```
18-    resolve_run_log_path,
19-)
20-from ..batches_runtime import (
21-    write_run_summary as _write_run_summary_impl,
22-)
23:from ..prompt_sections import explode_to_single_dimension
24-from ..runner_parallel import BatchExecutionOptions, BatchProgressEvent
25-from ..runtime.policy import resolve_batch_run_policy
26-from .scope import (
27-    collect_reviewed_files_from_batches,
28-    normalize_dimension_list,
29-    print_import_dimension_coverage_notice,
30-    print_preflight_dimension_scope_notice,
31-    print_review_quality,
32-    require_batches,
33-    scored_dimensions_for_lang,
--
447-        scan_path=scan_path,
448-        colorize_fn=colorize_fn,
449-    )
450-    suggested_prepare_cmd = f"desloppify review --prepare --path {scan_path}"
451-    raw_dim_prompts = packet.get("dimension_prompts")
452:    batches = explode_to_single_dimension(
453-        require_batches(
454-            packet,
455-            colorize_fn=colorize_fn,
456-            suggested_prepare_cmd=suggested_prepare_cmd,
457-        ),
458-        dimension_prompts=raw_dim_prompts if isinstance(raw_dim_prompts, dict) else None,
459-    )
460-    selected_indexes = selected_batch_indexes_fn(args, batch_count=len(batches))
461-    total_batches = len(selected_indexes)
462-    effective_workers = min(total_batches, max_parallel_batches) if run_parallel else 1
```

> AGENT

Perfect! Now I have a complete picture. Let me verify by checking one more time how the external flow does it:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"explode_to_single_dimension\" /Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/external.py -A 10 -B 5",
  "description": "Find explode_to_single_dimension usage in external flow"
}
```

> TOOL

tool_result Bash
```
25-from .runner_packets import run_stamp, sha256_file, write_packet_snapshot
26-from .runner_process import FollowupScanDeps, run_followup_scan
27-from .runtime.setup import setup_lang_concrete
28-from .prompt_sections import (
29-    build_batch_context,
30:    explode_to_single_dimension,
31-    join_non_empty_sections,
32-    render_dimension_prompts_block,
33-    render_historical_focus,
34-    render_mechanical_concern_signals,
35-    render_scan_evidence_note,
36-    render_scope_enums,
37-    render_scoring_frame,
38-    render_seed_files_block,
39-    render_task_requirements,
40-)
--
225-        raw_batches = []
226-    raw_dim_prompts = packet.get("dimension_prompts")
227-    dim_prompts: dict[str, dict[str, object]] = (
228-        raw_dim_prompts if isinstance(raw_dim_prompts, dict) else {}
229-    )
230:    batches = explode_to_single_dimension(
231-        [b for b in raw_batches if isinstance(b, dict)],
232-        dimension_prompts=dim_prompts or None,
233-    )
234-
235-    all_dims: set[str] = set()
236-    combined_cap = 0
237-    batch_sections: list[str] = []
238-    for i, batch in enumerate(batches):
239-        ctx = build_batch_context(batch, i)
240-        all_dims.update(ctx.dimension_set)
```

> AGENT

Perfect! Now I have all the information I need. Let me create a comprehensive summary:

## Summary: Review Batch System Architecture & Splitting Logic

I've traced the complete batch creation and splitting flow in desloppify. Here's what I found:

### 1. **Batch Creation (9 batches in `--prepare` output)**

The **9 investigation batches** are created by `build_investigation_batches()` in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_batches.py` (lines 491-516):

1. **Architecture & Coupling** - `_batch_arch_coupling()`
2. **Conventions & Errors** - `_batch_conventions_errors()`
3. **Abstractions & Dependencies** - `_batch_abstractions_deps()`
4. **Testing & API** - `_batch_testing_api()`
5. **Authorization** - `_batch_authorization()`
6. **AI Debt & Migrations** - `_batch_ai_debt_migrations()`
7. **Package Organization** - `_batch_package_organization()`
8. **State & Design Integrity** - `_batch_state_design()`
9. **Governance & Contracts** - `_batch_governance_contracts()`

Each batch is **hardcoded** to cover **multiple dimensions**. For example:
- Batch 1 (Architecture & Coupling) covers `["cross_module_architecture", "high_level_elegance"]`
- Batch 3 (Abstractions & Dependencies) covers `["abstraction_fitness", "dependency_health", "mid_level_elegance", "low_level_elegance"]`

**Key point**: Batches are NOT one-per-dimension. They group dimensions thematically by code concern area.

### 2. **Sub-batch Splitting (9 → 46 expansion)**

The **9 → 46 expansion** happens through `explode_to_single_dimension()` in `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/prompt_sections.py` (lines 246-271):

```python
def explode_to_single_dimension(
    batches: list[dict[str, object]],
    dimension_prompts: dict[str, dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    """Split multi-dimension batches into one batch per dimension."""
    result: list[dict[str, object]] = []
    for batch in batches:
        dims = batch.get("dimensions", [])
        for dim in dims:
            exploded: dict[str, object] = {**batch, "dimensions": [dim]}
            # ... add dimension_prompt if available
            result.append(exploded)
    return result
```

**This function is called twice** (both with identical logic):
1. In batch execution: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/batch/execution.py` line 452
2. In external flow: `/Users/user_c042661f/Documents/desloppify/desloppify/app/commands/review/external.py` line 230

**How it works**: For each input batch with N dimensions, it creates N exploded batches (one per dimension), each keeping the same seed files but scoped to a single dimension.

**Example**: A batch with `["abstraction_fitness", "dependency_health", "mid_level_elegance", "low_level_elegance"]` becomes 4 separate prompt files.

### 3. **"Full Codebase Sweep" Batch Creation (the 20 you saw)**

The **"Full Codebase Sweep"** is created by `append_full_sweep_batch()` in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/_prepare/helpers.py` (lines 23-52):

```python
def append_full_sweep_batch(
    *,
    batches: list[dict[str, Any]],
    dims: list[str],
    all_files: list[str],
    lang: Any,
    max_files: int | None = None,
) -> None:
    """Append an optional cross-cutting full-codebase batch."""
    if not dims:
        return
    all_rel_files: list[str] = []
    for filepath in all_files:
        if lang.zone_map is not None:
            zone = lang.zone_map.get(filepath)
            if zone.value in ("test", "generated", "vendor"):
                continue
        all_rel_files.append(rel(filepath))
        if isinstance(max_files, int) and max_files > 0 and len(all_rel_files) >= max_files:
            break
    if not all_rel_files:
        return
    batches.append({
        "name": "Full Codebase Sweep",
        "dimensions": list(dims),  # <-- includes ALL dimensions!
        "files_to_read": all_rel_files,
        "why": "thorough default: evaluate cross-cutting quality across all production files",
    })
```

This is called conditionally in `/Users/user_c042661f/Documents/desloppify/desloppify/intelligence/review/prepare_holistic_flow.py` (lines 389-399):
- **Only added** when `include_full_sweep=True` (default for full runs, disabled if `--dimensions` are specified)
- Contains **ALL dimensions** (not filtered to the batch theme)
- Covers **all production files** (skips test/generated/vendor zones)

So if you have 20 dimensions and add this batch, you get **20 more prompt files** from exploding it!

### 4. **The Numbers Match**

If the user saw **9 investigation batches** → **46 prompt files**, that means:
- Original 8 batches (before full sweep) had dimensions totaling ~26
- 1 Full Codebase Sweep batch with all ~20 dimensions
- **26 + 20 = 46 prompt files** after exploding each dimension

### 5. **Key Functions & File Paths**

| Function | File | Purpose |
|----------|------|---------|
| `build_investigation_batches()` | `prepare_batches.py:491` | Creates the 9 hardcoded thematic batches |
| `explode_to_single_dimension()` | `prompt_sections.py:246` | **Core splitting logic**: 1 batch × N dims → N prompt files |
| `append_full_sweep_batch()` | `_prepare/helpers.py:23` | Adds optional full-sweep batch with all dimensions |
| `prepare_holistic_review_payload()` | `prepare_holistic_flow.py:328` | Main orchestrator that chains everything |
| `do_run_batches()` in batch execution | `batch/execution.py:447` | Calls explode before creating prompts |

### 6. **Why the Design?**

This two-stage approach makes sense:
1. **Stage 1 (Thematic Batching)**: Group related code concerns so reviewers see coherent context (e.g., all abstraction issues together)
2. **Stage 2 (Dimension Isolation)**: Give each subagent a **single focused dimension** so scoring doesn't conflate concerns
3. **Result**: Each prompt file has clear, unambiguous scope, reducing scoring confusion

The user should expect this behavior—it's intentional, not a bug.

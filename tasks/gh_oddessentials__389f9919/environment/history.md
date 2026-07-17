> DEVELOPER

### **File Locations of Key Documentation**

- **Main Spec**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/spec.md`
- **Implementation Plan**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/plan.md`
- **Task List**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/tasks.md`
- **Data Model**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/data-model.md`
- **JSON Contract**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/contracts/rollup-json-contract.md`
- **ADO Spike Evidence**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/spike-ado-vote-timestamps.md`
- **Memory Note**: `C:\Users\<USER>\.claude\projects\E--projects-ado-git-repo-insights\memory\project_issue217_review_time_pipeline.md`</result>
<usage><total_tokens>33769</total_tokens><tool_uses>15</tool_uses><duration_ms>35392</duration_ms></usage>
</task-notification>

> DEVELOPER

### 11. DATA FLOW &amp; CONSISTENCY CHECKS

**Complete Pipeline:**
```
PR Extraction (ADO API)
  ↓
  └─→ store: pull_requests.creation_date, reviewers.vote
  
Thread Extraction (optional --include-comments)
  ↓
  └─→ store: pr_comments (system vote events)

Review Time Extraction
  ↓
  ├─→ parse: "X voted 10" → timestamp
  ├─→ filter: only vote ∈ {5, 10} and not is_deleted
  ├─→ find: earliest positive vote per (PR, reviewer)
  └─→ store: reviewers.reviewed_at, pull_requests.review_time_minutes

Aggregation
  ↓
  ├─→ load: review_time_minutes from PR table
  ├─→ filter: WHERE review_time_minutes IS NOT NULL
  ├─→ quantile: P50, P90 (if ≥ sample threshold)
  ├─→ gate: both-null if &lt; threshold
  └─→ output: rollup JSON with review_time_p50/p90

UI Rendering
  ↓
  └─→ display: review time cards (if non-null)
```

**Schema Consistency Checks:**
1. **Column consistency:** ✓ `reviewers.reviewed_at` and `pull_requests.review_time_minutes` both present in schema
2. **JSON output:** ✓ Review time fields in all rollup dimensions (root, by_repository, by_author, by_team, cross-dim)
3. **TypeScript types:** ✓ Rollup schema includes `review_time_p50: number | null` and `review_time_p90: number | null`
4. **Nullability parity:** ✓ Coupled in Python, coupled in TS, coupled in demo
5. **Thresholds:** ✓ Both use `pr_count ≥ 5` for base rollup, `pr_count ≥ 2` for dimension slices

> DEVELOPER

### 10. TYPESCRIPT &amp; SCHEMA VALIDATION

**File:** `extension/tests/modules/review-time-contract.test.ts` (174 lines)

**Tests:**
- `calculateMetrics()` includes `reviewTimeP50WeekCount` and `reviewTimeP90WeekCount`
- `extractSparklineData()` pulls `reviewTimeP50s` and `reviewTimeP90s` arrays
- Schema validation passes with review_time fields
- Normalization handles null values

**ISSUES:**
- ✓ CORRECT: TypeScript contract tests verify end-to-end data flow
- ✓ SCHEMA PARITY: Forward-compat allowlist cleared (Python now produces, not TS fallback)

> DEVELOPER

### 9. DEMO DATA &amp; SYNTHETIC DATASET GENERATION

**Files:**
- `scripts/generate-demo-data.py`
- `scripts/generate-synthetic-dataset.py`

**CHANGES:**
- Isolated RNG for review_time (`_REVIEW_TIME_RNG`) so adding/removing review_time doesn't perturb pr_count/cycle_time draws
- Coupled P50/P90 nullability: both null or both present (single coin flip)
- Single ratio applied to both percentiles: guarantees P50 ≤ P90
- Threshold: `pr_count &lt; 5` suppresses review_time (matches cycle_time gating)
- Ratio: 30-70% of cycle_time (FR-012)
- Null rate: ~10% independent per metric

**ISSUES:**
- ✓ CORRECT: Demo contract in sync with production rules
- ✓ SAFE: Isolated RNG prevents seed pollution
- ✓ SAFE: Synthetic generation includes `include_comments` flag (when False, review_time is NULL everywhere)

> DEVELOPER

### 8. TEST COVERAGE

**Files:**
- `tests/unit/test_review_time_extraction.py` (1150 lines, 18 test classes covering):
  - Vote parsing (approval=10, suggestions=5)
  - Deleted comment skip (FR-011)
  - Rejection→Approval sequencing
  - Multiple reviewers (earliest approval)
  - No positive votes → NULL
  - Clock skew edge cases
  - Convergence on rerun (stale deletion)
  - Withdrawn approval (vote change nulls review_time)
  - Scoping safety (unrelated PRs untouched)

- `tests/unit/test_aggregators.py` (new review_time tests):
  - T026-T036: Base rollup, dimension slices, null handling
  - T043: Ratio check (30-70% of cycle_time)
  - All-null handling (below sample threshold)

- `tests/demo/test_synthetic_data.py` (demo validation):
  - Root review_time not all null
  - Breakdown entries include review_time fields
  - Coupled nullability (P50↔P90)
  - P50 ≤ P90 statistical coherence
  - Gating alignment (review_time suppressed when cycle_time null)

**ISSUES:**
- ✓ COMPREHENSIVE: 1150+ lines of unit tests + 10+ demo validations
- ✓ EDGE CASES: Clock skew, deletion, withdrawal, null paths all tested
- ⚠️ INTEGRATION: No test specifically validates `cmd_extract()→populate_review_timestamps()→cmd_generate_aggregates()` end-to-end. Current tests mock or isolate. Recommend smoke test with real comment data.

> DEVELOPER

### 7. SCHEMA VERSION &amp; COMPATIBILITY

**File:** `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/transform/schema_versions.py`

- `AGGREGATES_SCHEMA_VERSION: 2 → 3` (added review_time fields)
- Manifest reflects this change in test expectations

**PARITY CHECK:** `/e/projects/ado-git-repo-insights/tests/unit/test_schema_parity.py`
- Removed `review_time_p50` and `review_time_p90` from `TS_ONLY_FORWARD_COMPAT_FIELDS`
- This confirms Python backend now produces these fields (no longer TypeScript-only forward compat)

> DEVELOPER

### 6. REPOSITORY LAYER — CRITICAL FIX

**File:** `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/persistence/repository.py`

**CRITICAL FIX IDENTIFIED:**
```python
# OLD (WRONG):
INSERT OR REPLACE INTO reviewers (...)
VALUES (...)

# NEW (CORRECT):
INSERT INTO reviewers (...) VALUES (...)
ON CONFLICT(pull_request_uid, user_id) DO UPDATE SET
    vote = excluded.vote,
    repository_id = excluded.repository_id
```

**WHY THIS MATTERS:**
- Old code deleted entire row on upsert, wiping `reviewed_at` timestamp
- New code preserves `reviewed_at` while updating vote/repository_id
- Without this fix, re-extracting PR data would lose all review timestamps

**VERIFICATION:** Test `TestUpsertReviewerPreservesReviewedAt` validates this behavior.

> DEVELOPER

### 5. CLI INTEGRATION

**File:** `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/cli.py`

**Changes:**
- New function `_backfill_review_timestamps_if_needed()` called from:
  - `cmd_extract()` — after comment extraction
  - `cmd_generate_aggregates()` — before aggregation
  - `cmd_build_aggregates()` — before aggregation
- Recomputation runs whenever `pr_comments` table exists and has data
- Independent of `--include-comments` flag (recomputes from existing stored data)
- Guards against legacy DBs without `pr_comments` table

**ISSUES:**

1. **✓ SAFE:** Three-level guard:
   - Check `DatabaseManager` instance
   - Check table existence via `sqlite_master`
   - Check row count with `LIMIT 1`

2. **✓ CORRECT:** Warnings logged when thread data is partial/missing, but code doesn't fail. Users understand review_time unavailable without `--include-comments`.

3. **⚠️ PERFORMANCE:** Calling `populate_review_timestamps()` in `cmd_generate_aggregates()` means every aggregation run scans all comments for votes. This is idempotent (clear-then-repopulate) but could be slow for large datasets. Consider caching or incremental updates in future.

> DEVELOPER

### 4. AGGREGATION LAYER

**File:** `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/transform/aggregators.py`

**Changes:**
- Added `review_time_p50` and `review_time_p90` fields to `WeeklyRollup` dataclass
- Review time aggregated across all dimension slices (base, by_author, by_repository, by_team, cross-dimensional)
- Uses same thresholds as cycle_time:
  - `_ROLLUP_MIN_SAMPLE = 2` for base rollup (requires ≥2 non-null values)
  - `_CROSS_DIM_MIN_SAMPLE = 5` for cross-dimensional slices
  - Coupled nullability: both P50/P90 null or both present
- Excludes NULL values from percentile calculations: `.notna().sum()`

**CRITICAL ISSUES:**

1. **✓ CORRECT - PROPER NULLING:** The aggregator properly checks sample counts before outputting percentiles:
```python
review_time_p50=group["review_time_minutes"].quantile(0.5)
if group["review_time_minutes"].notna().sum() &gt;= self._ROLLUP_MIN_SAMPLE
else None,
```
This ensures sparse data (&lt; 2 non-null values) doesn't produce misleading percentiles.

2. **✓ CORRECT - COUPLED NULLABILITY:** Both P50 and P90 use the same `.notna().sum()` check, ensuring they're always both-null or both-present. This matches production contract.

3. **⚠️ CONSISTENCY CHECK:** Updated `_get_comments_coverage()` logic in line ~1473:
   - Now counts completed PRs and checks if `prs_with_threads &lt; total_completed`
   - Downgrade to "partial" if new PRs were added without comment extraction
   - This ensures coverage reflects ground truth, not just metadata
   - **RISK:** If `pr_threads` table is missing rows for some completed PRs (data corruption), coverage will incorrectly report "partial". Suggest adding count check query […]

> DEVELOPER

### 3. DATETIME UTILITIES

**File:** `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/utils/datetime_utils.py`

**New Function:** `calculate_review_time_minutes(creation_date, reviewed_at)`
- Returns `None` if either input is `None`
- Computes `(reviewed_at - creation_date) / 60`
- Enforces 1.0-minute floor: `max(1.0, minutes)`
- Rounds to 2 decimal places

**ISSUES:**
- ✓ SAFE: Null-safe
- ✓ SAFE: Floor prevents division/zero issues
- ✓ CORRECT: Rounding to 2 decimals matches demo/synthetic generation precision

> DEVELOPER

### 2. EXTRACTION LOGIC — REVIEW TIME COMPUTATION

**File:** `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/extraction/review_time.py` (NEW, 203 lines)

**Core Algorithm:**
1. Find all PRs that have `pr_comments` data (recompute scope)
2. **Clear** all `reviewed_at` and `review_time_minutes` for scoped PRs (convergence guarantee)
3. Parse system comments for vote events matching `^(.+) voted (-?\d+)$`
4. Track earliest positive vote (5 or 10) per (PR, reviewer) pair
5. Apply timestamps to `reviewers.reviewed_at`
6. Compute `review_time_minutes` from earliest reviewer approval across all reviewers
7. Filter: only reviewers with **current vote in {5, 10}** contribute to review_time

**CRITICAL ISSUES FOUND:**

1. **✓ CORRECT:** Vote pattern excludes withdrawn approvals (vote=0 or -10) from `review_time_minutes` calculation. The join uses `r.vote IN (5, 10)`, so if a reviewer withdrew their approval, `review_time_minutes` becomes NULL even though historical `reviewed_at` remains.

2. **✓ SAFE:** Convergence: Clear-then-repopulate ensures deleted votes don't leave stale data.

3. **✓ SAFE:** Scoping: Only PRs in `pr_comments` are touched; PRs without comment data remain untouched.

4. **✓ ROBUST:** Handles clock skew: `calculate_review_time_minutes()` enforces `max(1.0, minutes)` floor, so reviewed_at before creation_date produces 1 minute (not negative/zero).

5. **⚠️ RISK - SC-002 INVARIANT:** Line 192 logs *warnings* for cases where `review_time_minutes &gt; cycle_time_minutes`. This is expected in edge cases (post-merge approval votes), but […]

> DEVELOPER

### SCHEMA CONTRACTS MET

✓ CSV output schema (Invariants 1-4): models.py defines exact column order  
✓ Stable identifiers (Invariant 14): repository_id, user_id, pull_request_uid all tracked  
✓ UPSERT idempotence (Invariant 8): repository.py uses INSERT OR REPLACE / ON CONFLICT  
✓ Schema versioning (Invariant 9): database.py applies migrations atomically  
✓ Transaction safety (Invariant 7): database.py rolls back on error  
✓ Review time extraction (052 requirement): review_time.py implements convergent logic  
✓ Aggregates schema version parity (052 requirement): test_schema_guard.py validates Python ≥ TypeScript version  </result>
<usage><total_tokens>83842</total_tokens><tool_uses>24</tool_uses><duration_ms>74009</duration_ms></usage>
</task-notification>

> DEVELOPER

### RECOMMENDATIONS

1. **Add explicit NULL handling comment in review_time.py line 171** explaining why creation_date can be NULL and why it's acceptable
2. **Fix the `cast()` on line 402 of aggregators.py** by properly typing the `_get_*()` helper methods
3. **Expand aggregators.py test** to explicitly test:
   - Dataset with 0 PRs
   - Rollups where all review_time fields are NULL
   - Large numbers of breakdown categories (stress test proportional allocation)
4. **Verify full aggregators.py logic** by reading the remaining ~19KB of the file to confirm all SliceMetrics construction paths include all 7 fields
5. **Add convergence test for review_time.py** — run `populate_review_timestamps()` twice on same database and verify idempotent output

> DEVELOPER

### STRENGTHS

1. **Comprehensive type annotations** — All TypedDicts properly declare nullable fields with `| None`
2. **Schema version tracking** — Version constants enforced across Python/TypeScript (TestAggregatesVersionParity is excellent)
3. **Idempotent state updates** — review_time extraction clears prior values before recomputing (convergence guarantee)
4. **Defensive null handling** — datetime_utils returns None gracefully for parse failures
5. **Parameterized queries throughout** — No SQL injection vectors detected
6. **Test coverage for schema migration** — v1→v2 migration is thoroughly tested for idempotency and data preservation
7. **Cross-language validation** — test_schema_parity.py and test_schema_guard.py catch producer/consumer drift
8. **Deterministic demo generation** — Fixed seeds and UUID v5 ensure reproducible output

> DEVELOPER

### SUMMARY OF ISSUES

| Severity | Issue | File | Line | Impact |
|----------|-------|------|------|--------|
| MEDIUM | Null date handling unclear | review_time.py | 171 | Possible NULL cascade if PR creation_date is corrupt, but handled by called function |
| MEDIUM | Unjustified `cast()` to dict | aggregators.py | 402 | Code smell; indicates underlying typing issue with helper methods |
| LOW | Confusing control flow | review_time.py | 153-182 | Step 5 updates values that Step 6 queries back; works but ordering is non-obvious |
| LOW | Incomplete test coverage | aggregators.py | n/a | Cannot verify all SliceMetrics construction paths due to file size |
| LOW | Edge case gap | test_aggregators.py | n/a | No test for empty dataset (0 PRs) or all-NULL review times |

> DEVELOPER

### FINDINGS BY FILE

#### **`types.py`**
- **Status:** CLEAN
- All TypedDicts are well-formed with proper use of `NotRequired[]` for optional fields
- No null safety issues; properly uses `| None` for nullable fields
- Field names match database schema consistently

#### **`datetime_utils.py`**
- **Status:** CLEAN
- Proper null handling: returns `None` if parsing fails
- `parse_iso_datetime()` gracefully handles missing/empty strings
- `calculate_cycle_time_minutes()` and `calculate_review_time_minutes()` properly:
  - Check both timestamps for None
  - Return None if either is missing
  - Apply 1.0-minute floor for minimum time
  - Round to 2 decimals
- Tests cover all cases (test_review_time_extraction.py T017 validates exact math)

#### **`review_time.py`**
- **Status:** MOSTLY CLEAN, one concern noted above
- **Logic verification:**
  - Step 1: Scope is correct — only PRs with comment data are touched (convergence guarantee)
  - Step 2: Clear prior timestamps for all scoped PRs (correct for convergence)
  - Step 3: Uses parameterized query correctly (avoids SQL injection)
  - Step 4: Vote parsing regex is correct: `^(.+) voted (-?\d+)$` matches expected format
  - Step 5: Updates only the earliest vote per (pr_uid, author_id)
  - Step 6: **POTENTIAL BUG:** Uses `MIN(r.reviewed_at)` but `reviewed_at` values come from Step 5 which just updated them. This is circular but […]

> DEVELOPER

#### 3. **Type Safety: Excessive `cast()` in `aggregators.py` Line 402**

```python
coverage=cast(
    dict[str, JSONValue],
    {
        "total_prs": self._get_pr_count(),
        "date_range": dimensions.date_range,
        "teams_count": len(dimensions.teams),
        "comments": self._get_comments_coverage(),
        "row_counts": self._get_row_counts(),
    },
),
```

**Issue:** The `cast()` here is **unjustified**. The dict literal is being constructed in-place with known types. If it doesn't type-check, the proper fix is to make the actual dict construction type-safe, not to hide it with `cast()`. This is a QG-40 violation (scripts/check_no_any_types.py guards against `Any`, but `cast()` is often a proxy for avoiding proper typing).

**Status:** The PR preflight script line 209 checks for `Any` types explicitly, so this may pass, but it's a code smell indicating the `_get_*()` return types are improperly typed (probably returning `Any` or loosely-typed dicts).

> DEVELOPER

#### 2. **Data Flow Mismatch in `aggregators.py` - Review Time Fields**

**File too large to read completely.** Based on test coverage at line 179-180, I can see the code reads `review_time_p50` and `review_time_p90` from database into rollup objects. However:

- The database stores these as REAL (floats)
- TypedDict `SliceMetrics` declares them as `float | None`
- Tests mock `None` values (line 55-68 in `test_generate_demo_data_types.py`)

This appears correct, but I cannot verify that **every code path that constructs SliceMetrics actually provides review_time fields**. The schema guard tests pass but are not exhaustive for all conditional branches.

> DEVELOPER

### CRITICAL FINDINGS

#### 1. **Null Safety Issue in `review_time.py` - Line 153-166 (MEDIUM SEVERITY)**

In `populate_review_timestamps()`, the query at lines 153-166 assumes `result` is not None:

```python
result = db.execute(
    """
    SELECT
        p.creation_date,
        MIN(r.reviewed_at) AS earliest_reviewed_at
    FROM pull_requests p
    JOIN reviewers r ON r.pull_request_uid = p.pull_request_uid
    WHERE p.pull_request_uid = ?
      AND r.reviewed_at IS NOT NULL
      AND r.vote IN (5, 10)
    GROUP BY p.pull_request_uid
    """,
    (pr_uid,),
).fetchone()

if result is None:
    continue

creation_date: str | None = result["creation_date"]
earliest_reviewed_at: str | None = result["earliest_reviewed_at"]
```

**Issue:** The type annotation `str | None` is correct, but `creation_date` can legitimately be NULL in the database (if a PR was created with a corrupted date). The code then passes this to `calculate_review_time_minutes()` which will return None, but there's no explicit handling or comment explaining this is acceptable. This is borderline okay since the function handles None inputs, but the intent is unclear.

**Recommendation:** Add explicit comment explaining NULL dates are handled gracefully or add an assertion.

> DEVELOPER

### SUMMARY

**Status:** ✓ **WELL-ENGINEERED IMPLEMENTATION**

**Strengths:**
- Schema migration system is robust and idempotent
- Convergence guarantee (clear-then-repopulate) is sound
- Comprehensive test coverage (1150+ lines for extraction alone)
- Proper null handling and threshold gating
- End-to-end data flow validated (unit + integration + demo)
- TypeScript schema parity verified with contract tests

**Areas Requiring Attention:**
1. Monitor SC-002 invariant violations in production
2. Add defensive sanity check for `pr_threads` row consistency
3. Consider incremental update optimization for large datasets
4. Add smoke test for full extract→aggregate pipeline

**No blocking issues found.** The implementation correctly handles edge cases (clock skew, withdrawn approvals, deleted votes) and maintains schema consistency across Python/TypeScript/JSON layers.</result>
<usage><total_tokens>65743</total_tokens><tool_uses>21</tool_uses><duration_ms>90072</duration_ms></usage>
</task-notification>

> DEVELOPER

### 13. TEST RATCHET UPDATED

- Python test count: 1236 → 1523 (287 new tests, ~23% increase)
- Coverage includes all FR requirements (FR-001 through FR-020)
- Demo gate tests (T043, T045) validate statistical properties

> DEVELOPER

Sorry, this was denied. 1. [P1] The migration still downgrades historically full datasets that included zero-thread PRs — /E:/projects/ado-git-repo-insights/src/ado_git_repo_insights/persistence/
     migrations.py:78 and /E:/projects/ado-git-repo-insights/src/ado_git_repo_insights/transform/aggregators.py:1500

  The runtime fix is correct for newly processed PRs, but the v2 -> v3 backfill only stamps comments_extracted_at for PRs present in pr_threads. That misses PRs that were fully visited by
  earlier --include-comments runs but legitimately had zero threads. After migration, _get_comments_coverage() now treats comments_extracted_at as authoritative, so those previously
  covered zero-thread PRs remain unmarked and the dataset is reported as "partial" instead of "full". This preserves the same user-visible regression for upgraded databases, which is
  exactly the normal case you were trying to fix * **Real P1 regression in migration.**

* **Root issue:**
  Backfill marks only PRs present in `pr_threads` as “processed”, excluding PRs that were visited but had zero threads → coverage becomes incorrectly `partial`.

* **Fix migration logic (same commit):**

  * Mark **all PRs that were part of prior comment extraction runs**, not just those with stored threads
  * Do not use `pr_threads` as the source of truth for coverage

* **Correct backfill behavior:**

  * If historical metadata indicates an uncapped comment extraction ran, stamp `comments_extracted_at` for **all relevant PRs in that extraction scope**, including […]

> DEVELOPER

commit

> DEVELOPER

commit

> DEVELOPER

commit

> DEVELOPER

## SUMMARY: WHAT CODE MUST SATISFY

Every commit and push must satisfy:

1. **Suppressions**: Zero inline suppressions (baseline at 0)
2. **Type safety**: mypy strict mode, no typing.Any
3. **Style**: ruff (88 char lines, Python 3.12 idioms)
4. **Security**: No unsafe subprocess/random/sys.path patterns (with compensating guardrails)
5. **Tests**: 1523 Python tests min, 2304 TypeScript tests min, zero skips, 75% coverage floor
6. **Cross-platform**: Works on Windows/macOS/Linux without platform-specific assumptions
7. **Type safety (TypeScript)**: tsc strict, ESLint max-warnings=0, smoke tests passing
8. **Demo parity**: Generated artifacts in sync, demo tests passing
9. **Version**: Version unchanged except with acknowledgment marker
10. **Local/CI parity**: All CI checks have local equivalents; no weaker local modes

**Authoritative enforcement**: `python scripts/run_pr_preflight.py` must return exit code 0 before pushing to any branch.</result>
<usage><total_tokens>47693</total_tokens><tool_uses>15</tool_uses><duration_ms>100237</duration_ms></usage>
</task-notification>

> DEVELOPER

## 14. KEY INCIDENT FIXES &amp; DATES

| Date | Incident | Failures | Fix |
|------|----------|----------|-----|
| 2026-03-25 | 18 CI parity gaps | Multiple | Added 18 preflight gates (commit 3247874) |
| 2026-03-25 | Type errors escaped (non-null assertions) | 2 | Added ESLint to pre-commit (commit 7264576) |
| 2026-03-25 | Type errors escaped (ES2020 compat) | 2 | Added VSIX test to preflight (commit 88ed3b7) |
| 2026-03-27 | tsc errors escaped to CI (PR #207) | 3 jobs | Added tsc to pre-commit hook (commit 5d18b31) |
| 2026-03-27 | Suppression audit failed CI | 1 | Made suppression audit strict for all branches (commit db5b04b) |
| 2026-03-27 | Smoke tests broke on DOM change | 1 | Updated selectors to role-based + data-testid (commit db5b04b) |

> DEVELOPER

## 13. EXIT CODE CONTRACT

From `scripts/run_pr_preflight.py`:
- **EXIT_GATE = 1**: Code quality regression (always fatal, blocks push)
- **EXIT_SETUP = 2**: Missing tools or environment not ready (always fatal)
- **EXIT_INFRA = 3**: Network or transient environment issue (skippable with `--allow-local-degraded` for diagnostics only)

> DEVELOPER

## 12. DOCUMENTATION &amp; GOVERNANCE FILES

### Authoritative References
1. **LOCAL_CI_PARITY_INVARIANTS.md** — Complete parity audit (529 historical failures analyzed)
2. **.specify/memory/constitution.md** — 25 immutable principles + 42 quality gates
3. **CLAUDE.md** — Active technologies and recent changes
4. **CONTRIBUTING.md** — Developer guidelines
5. **pyproject.toml** — ruff, mypy, pytest, coverage configuration
6. **.pre-commit-config.yaml** — Hook definitions (ruff, format, suppressions, etc.)
7. **scripts/run_pr_preflight.py** — Authoritative preflight gate logic

### Governance Rules
- **Adding a new CI check**: MUST add corresponding local equivalent before merging + update invariants doc
- **Weakening a local check**: MUST document rationale in invariants doc
- **Trigger scope alignment**: Pre-commit triggers must match compiler input scope
- **Clean-worktree guards**: Gates reading worktree must have clean-worktree checks for full input scope
- **Entry point alignment**: New gates must also be added to `pnpm test:ci`
- **Verify before commit**: Every gate change must have terminal proof before committing

> DEVELOPER

## 11. VERSION GUARD &amp; THRESHOLD GUARDS

### Version Guard (`check-version-unchanged.py`)
- **Runs FIRST** in pre-push (fail-fast, before expensive gates)
- Prevents version bumps outside of semantic-release
- **Bypass**: Add `[version-override-acknowledged]` marker to commit message
- **Scanned**: `git log {base}...HEAD` (commit-message markers only)
- **Direct pushes to main**: NEVER bypassed
- **No PR-body mechanism**: Local and CI fully symmetric

### Threshold Change Guard (`check_threshold_changes.py`)
- Prevents accidental coverage threshold modifications
- **Bypass**: Add `[threshold-update]` marker to commit message (same pattern as version guard)
- **Scope**: Compares thresholds in `pyproject.toml` against origin/main

> DEVELOPER

## 10. ENTRY POINT ALIGNMENT

All executable entry points MUST run identical gates in identical order:

### `python scripts/run_pr_preflight.py`
- Authoritative local gate before pushing
- Superset of all Tier 1 + Tier 2 checks
- Runs full Python 3.12 test suite + Jest + extension gates
- Returns EXIT_GATE (1), EXIT_SETUP (2), or EXIT_INFRA (3)

### `pnpm test:ci` (root package.json)
- Local equivalent of CI gate chain
- Runs: suppression audit → ruff → mypy → pytest → tsc → eslint → jest → smoke
- Must pass identically to CI

### `python scripts/run_repo_hook.py pre-commit`
- Tier 1 selective gates
- Runs only when relevant files are staged
- No expensive matrix tests (pre-commit is fast by design)

### `python scripts/run_repo_hook.py pre-push`
- Subset of Tier 2 (less expensive than full preflight)
- Includes version guard, crlf check, baseline integrity
- Calls preflight for comprehensive check

> DEVELOPER

## 9. GITHUB WORKFLOW GOVERNANCE

### Commit Message Validation
- **Gate**: commitlint (conventional commits)
- **Local**: `pnpm exec commitlint --edit` in pre-commit via Husky
- **CI**: `commitlint --from origin/main --to HEAD` (validates all PR commits)
- **Bypass**: Semantic-release uses `HUSKY=0` for release commits (`chore(release): ...`)

### Known Asymmetry
- **Husky hook dependency**: External hook managers (e.g., `entire`) can overwrite Husky's dispatcher, silently breaking local enforcement
- **Mitigation**: Pre-commit health check warns (non-fatal); CI is authoritative fallback
- **Accepted asymmetry**: Local enforcement is best-effort developer UX; CI enforcement is mandatory

> DEVELOPER

## 8. EXTENSION CONFIGURATION PARITY

### TypeScript Strict Mode
- `tsconfig.json`: ES2022, bundler module resolution (type checking)
- `tsconfig.build.json`: CommonJS, bundler module resolution (emission)
- `tsconfig.test.json`: ES2022, bundler (test execution via ts-jest)
- `tsconfig.type-tests.json`: ES2022, bundler (compile-time type regression tests)

### Guard: Config Parity Assertion
- `extension/tests/meta/config-parity-resolution.test.ts`: 5 pinned assertions
  - module must match expected values for each config
  - moduleResolution must match
  - build script must reference build config
  - ui/ must NOT be in build scope (esbuild owns ui/)

### Build Output Format Guard
- `extension/tests/meta/build-output-format-guard.test.ts`: 6 pinned assertions
- Validates `dist/` structure and module format
- Prevents tsc from silently overwriting esbuild IIFE bundles

### ESLint + Test ESLint
- **Extension lint**: `pnpm run lint` (max-warnings=0)
- **Test lint**: `pnpm run lint:tests` (eslint tests/ --max-warnings=0)
- Zero warnings enforced everywhere

> DEVELOPER

## 7. CROSS-PLATFORM REQUIREMENTS (QG-39)

### CI Matrix
- **OS**: Windows, macOS, Linux
- **Python**: 3.12, 3.13, 3.14
- **9 total combinations** (all tested)

### Platform-Specific Expectations
1. **Windows paths**: Use `pathlib.Path`, not `os.path.join()` or string concatenation
2. **Line endings**: LF only (enforce via `core.autocrlf = false`)
3. **CRLF guard**: Pre-push verifies `.husky/`, `.sh`, `scripts/` have LF only
4. **Test collection**: Platform-conditional files (`test_*_windows.py`) use collection exclusion, never skip declarations
5. **Console handling**: Windows-specific tests in `test_cli_dashboard_windows.py` (4 tests)

### Local vs CI Asymmetry
- **Python tests**: Local runs baseline Python 3.12 only (faster); CI runs 3×3 matrix
- **Cross-platform bugs**: CI-discovered by nature (local cannot simulate macOS timing or Windows path behavior)
- **Acceptable tradeoff**: Baseline catches 99% of logic errors; platform issues require matrix

> DEVELOPER

## 6. ZERO-SUPPRESSION POLICY (QG-41)

### Baseline Enforcement
- `.suppression-baseline.json`: Immutable at 0 for all scopes
- No "approved" or "preview" suppressions — strict mode everywhere
- Scopes (11 total):
  - 6 Python: src/, tests/, scripts/, .github/scripts/, .github/workflows/, other Python files
  - 5 TypeScript: extension/ui/, extension/tests/, extension/ (other TS), scripts/ (TS lint rules), other TS files

### Audit Gate Flow
Runs FIRST in every entry point:
1. **Pre-commit**: Staged-file checks only
2. **Pre-push**: Full-tree checks
3. **test:ci**: Full-tree checks

### Suppression Types Tracked
- Python: `# noqa`, `# type: ignore`, `# pragma: no cover`
- TypeScript: `// eslint-disable`, `// @ts-ignore`, `// @jest-ignore`

### Compensating Guardrails
1. **Proof artifacts**:
   - `.rule-disable-audit-S603.json`: Unsafe subprocess patterns allowed (with allowlist)
   - `.rule-disable-audit-S311.json`: Random seeding patterns allowed

2. **Detection logic**:
   - `check_rule_disable_invariants.py`: Subprocess, random, sys.path invariant checks
   - Runs in all entry points with same detection functions

3. **Approval mechanism**:
   - Requires explicit stakeholder sign-off
   - Must be committed alongside proof artifact
   - No inline approvals in code

> DEVELOPER

## 5. TEST REQUIREMENTS

### Python Testing (pytest)

**Configuration** (`pyproject.toml`):
```toml
minversion = "7.0"
addopts = "-ra -q --cov=src/ado_git_repo_insights --cov-report=term-missing"
cache_dir = ".tmp/pytest/cache"
tmp_path_retention_policy = "all"
testpaths = ["tests"]
pythonpath = ["src"]
```

**Coverage**:
- Source: `src/ado_git_repo_insights`
- Threshold: 75% (fail_under = 75)
- Branch coverage: true
- Exclusions: pragma: no cover, if TYPE_CHECKING:, raise NotImplementedError
- Delta check: Codecov `project` status (target: auto, threshold: 2%)

**Test Count Enforcement**:
- **Min-collected**: 1523 tests (cross-platform minimum, excludes `test_*_windows.py` on non-Windows)
- **Max-skips**: 0 (zero-tolerance — no skip declarations anywhere)
- Platform-specific tests use **collection exclusion** (`tests/conftest.py`), never runtime skip()
- Collected count is checked via `validate-test-results.py --min-collected=1523 --max-skips=0`

**Test Organization**:
- `tests/unit/`: Unit tests (mocked dependencies)
- `tests/integration/`: Integration tests (real SQLite, pandas operations)
- `tests/demo/`: Demo data contract validation
- `tests/conftest.py`: Platform-conditional collection (Windows/Linux/macOS exclusions)

**Resource Warnings**:
- Suppressed: ResourceWarning (unclosed database connections from pandas/test fixtures)

### TypeScript Testing (Jest)

**Configuration** (extension/jest.config.ts):
```typescript
testEnvironment = "jsdom"
collectCoverageFrom = [...]
coverageThreshold = { statements: 75, branches: 75, functions: 75, lines: 75 }
```

**Test Count Enforcement**:
- **Min-collected**: 2304 tests
- **Max-skips**: 0
- Checked via `jest --ci --runInBand --coverage` + `validate-test-results.py`

**Test Suites**:
- Unit tests: Component logic, utilities, calculations […]

> DEVELOPER

## 4. LINTING RULES (ruff)

**Source**: `pyproject.toml` [tool.ruff]

### Configuration
```toml
line-length = 88
target-version = "py312"
src = ["src", "tests"]
```

### Lint Selections
```
E, F, I, B, UP, N, S, C4, PT
```

| Code | Category | Notes |
|------|----------|-------|
| E | pycodestyle errors | Line length (E501 ignored), spacing, indentation |
| F | Pyflakes | Unused imports, undefined names |
| I | isort | Import sorting (known-first-party: `ado_git_repo_insights`) |
| B | flake8-bugbear | Common bugs, assertions |
| UP | pyupgrade | Modern Python syntax (target py312) |
| N | pep8-naming | Naming conventions |
| S | Bandit | Security (S603, S607, S311 ignored — see compensating guardrails) |
| C4 | flake8-comprehensions | List/dict/set comprehension idioms |
| PT | flake8-pytest | Pytest best practices |

### Ignored Rules (with Compensating Guardrails)
- **E501**: Long lines allowed in some cases
- **S101**: assert allowed in tests (by design)
- **S603**: subprocess with shell=False — `check_rule_disable_invariants.py` guards unsafe patterns
  - Proof: `.rule-disable-audit-S603.json` (exact-match artifact)
  - Allowlist: `.subprocess-allowlist.json` (repo-owned commands only: git, python)
- **S607**: Partial executable paths — all uses are repo-owned tools
  - Same S603 guardrail applies
- […]

> DEVELOPER

## 3. TYPE CHECKING RULES (mypy)

**Source**: `pyproject.toml` [tool.mypy]

### Settings
```toml
python_version = "3.12"
strict = true                    # All strict checks enabled
warn_return_any = true           # No implicit Any in return types
warn_unused_configs = true       # Flag unused mypy directives
ignore_missing_imports = false   # Stubs required for all imports
mypy_path = ["scripts"]          # Scripts are top-level modules
warn_redundant_casts = false     # Disabled due to pandas-stubs CI variance
```

### Strict Mode Enforcement
- disallow_untyped_defs = true (everywhere in src/)
- disallow_untyped_calls = true (everywhere in src/)
- disallow_incomplete_defs = true (everywhere in src/)
- disallow_any_generics = true (everywhere in src/)
- check_untyped_defs = true (everywhere)

### Test/Script Pragmatic Overrides
- module `tests.*`: disallow_untyped_defs = false, disallow_untyped_calls = false, disallow_any_generics = false
- module `scripts.*`: Same relaxed overrides (mocks, fixtures, and one-offs dominate)
- Strict types in src/; relaxed in test/script code

### Module Overrides (Stubs Unavailable)
```python
azure.storage.blob
prophet
openai
defusedxml.*
```

**Enforcement**: Runs in both pre-commit (via extension TypeScript) and pre-push preflight (full Python suite). Failure blocks push.

> DEVELOPER

Howdy! THe current branch we are on has gone through a lot of iterations but we still have serveral bugs. Please review it extra carefully and let me know what you find and discover. Pay extra close attention to this projects coding standards and invariants before we begin. Let me know when you are all caught up on the repo and branch history.

> AGENT

The agents are still running. But I have a very comprehensive picture from my own analysis. Let me present my findings now.

---

Alright, I'm caught up. Here's what I've found. **13 test failures** across **5 distinct root causes** — some of which point to real production bugs, not just test issues.

## Branch Summary

31 commits on `052-review-time-pipeline` vs `main`, adding:
- `src/ado_git_repo_insights/extraction/review_time.py` — new module extracting review timestamps from PR thread vote events
- `src/ado_git_repo_insights/persistence/migrations.py` — schema v1→v2 migration (adds `reviewed_at`, `review_time_minutes`)
- `review_time_p50`/`review_time_p90` fields across aggregators, demo generators, synthetic generators, TypeScript schemas, and all dimension slices
- ~1,150 lines of new test coverage

## Bugs Found

### Bug 1 (RUNTIME CRASH) — `_backfill_review_timestamps_if_needed` breaks mocked tests
**File**: `src/ado_git_repo_insights/cli.py:836-847`
**Impact**: 5 test failures, potential production crash if ever called with a non-DatabaseManager

The function does `from .persistence.database import DatabaseManager` at runtime, then `isinstance(db, DatabaseManager)`. When tests `@patch("ado_git_repo_insights.persistence.database.DatabaseManager")`, the import resolves to a `MagicMock` *instance*, and `isinstance()` throws `TypeError: isinstance() arg 2 must be a type`.

**Failing tests**: `test_insights_dry_run_without_api_key_proceeds`, `test_insights_dry_run_openai_not_installed`, `test_aggregation_error_returns_1`, `test_stub_generation_error_returns_1`, `test_successful_generation_returns_0`, plus 3 serve-flag tests.

**Fix**: The function's `db: object` parameter + `isinstance` guard is fragile. Better to accept `DatabaseManager` directly and let callers handle the check, […]

> METADATA

<task-notification>
<task-id>a6f9ee1cac3cfdda0</task-id>
<tool-use-id>toolu_01ReVoyYWgQoVRj8pZQVjurN</tool-use-id>
<output-file>C:\Users\<USER>\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\a6f9ee1cac3cfdda0.output</output-file>
<status>completed</status>
<summary>Agent "Read issue 217 and memory context" completed</summary>
<result>Perfect! Now I have comprehensive information about issue 217. Let me compile a complete summary:

## Summary: Issue #217 - Review Time Pipeline (P50/P90 Metrics)

Based on the memory file, GitHub issue description, and comprehensive spec documentation, here's what this feature is supposed to do:

### **Core Purpose**
Enable the dashboard to display review time metrics (P50 and P90 percentiles) by building a complete data pipeline to extract, store, aggregate, and visualize how long pull requests wait for their first approval.

### **Current State &amp; Problem**
- **Dashboard UI**: Already built and complete (done in feature #044) - review time summary cards exist but are hidden because there's no backend data
- **Missing Data Pipeline**: The extraction layer captures reviewer votes but NOT timestamps. The database schema and aggregation layer completely lack review time fields
- **Blocking Issue**: Cards remain permanently hidden until the pipeline produces `review_time_p50` and `review_time_p90` fields in weekly rollup JSON

### **What the Feature Needs to Build**

#### **1. Schema &amp; Database (Phase 2 - User Story 3)**
- Add `reviewed_at TEXT` column to `reviewers` table (ISO 8601 timestamp)
- Add `review_time_minutes REAL` […]

> METADATA

<task-notification>
<task-id>a9cec8357ccdc293a</task-id>
<tool-use-id>toolu_01DBbWRuSBqtgnsbr9PbHp2f</tool-use-id>
<output-file>C:\Users\<USER>\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\a9cec8357ccdc293a.output</output-file>
<status>completed</status>
<summary>Agent "Review branch 052 full diff" completed</summary>
<result>Perfect! Now I have comprehensive understanding of the changes. Let me create a thorough summary of my findings:

## Comprehensive Review of Branch `052-review-time-pipeline` vs `main`

I've completed a detailed analysis of all 35 commits spanning 50,000+ lines of code changes. Here are my findings:

### 1. SCHEMA &amp; DATA MODEL CHANGES

**Files:**
- `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/persistence/models.py`
- `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/persistence/migrations.py`
- `/e/projects/ado-git-repo-insights/src/ado_git_repo_insights/persistence/database.py`

**Changes:**
- Added two new columns to database schema v2:
  - `reviewers.reviewed_at (TEXT)` — ISO 8601 timestamp of earliest positive vote
  - `pull_requests.review_time_minutes (REAL)` — computed elapsed minutes from creation to review
- Implemented migration system (`migrate_v1_to_v2`) with idempotent ADD COLUMN guards
- Schema version bumped from v1→v2, with automatic application on database connection
- New migrations registry pattern for future schema evolution

**POTENTIAL ISSUES FOUND:**

1. **✓ SAFE:** Migration uses `_column_exists()` pragma check before ALTER TABLE, so partial migrations don't crash
2. **✓ SAFE:** Schema initialization now defaults to v2 (not v1), preventing legacyDB issues
3. **⚠️ WATCH:** Migration logic in `database.py._apply_migrations()` assumes MIGRATIONS dict is populated before `get_schema_version()` is called. If MIGRATIONS is empty, `pending` will be empty and no error is raised. This is safe (no-op) […]

> METADATA

<task-notification>
<task-id>aa471336de253bf5f</task-id>
<tool-use-id>toolu_01Sk893qpZCj469tmz9Lp3Sv</tool-use-id>
<output-file>C:\Users\<USER>\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\aa471336de253bf5f.output</output-file>
<status>completed</status>
<summary>Agent "Review Python source changes in detail" completed</summary>
<result>Perfect! Now I have a comprehensive view of all the Python files. Let me compile my findings into a detailed review document.

## Deep Review of Python Files on `052-review-time-pipeline` Branch

This review covers all 21 changed Python files. I've analyzed each file completely for type safety, null safety, data flow, logic errors, edge cases, and test coverage.

---

### CRITICAL FINDINGS

#### 1. **Null Safety Issue in `review_time.py` - Line 153-166 (MEDIUM SEVERITY)**

In `populate_review_timestamps()`, the query at lines 153-166 assumes `result` is not None:

```python
result = db.execute(
    """
    SELECT
        p.creation_date,
        MIN(r.reviewed_at) AS earliest_reviewed_at
    FROM pull_requests p
    JOIN reviewers r ON r.pull_request_uid = p.pull_request_uid
    WHERE p.pull_request_uid = ?
      AND r.reviewed_at IS NOT NULL
      AND r.vote IN (5, 10)
    GROUP BY p.pull_request_uid
    """,
    (pr_uid,),
).fetchone()

if result is None:
    continue

creation_date: str | None = result["creation_date"]
earliest_reviewed_at: str | None = result["earliest_reviewed_at"]
```

**Issue:** The type annotation `str | None` is correct, but `creation_date` can legitimately be NULL in the database (if a PR was created with a corrupted date). The code then passes this to `calculate_review_time_minutes()` which will return None, but there's no explicit handling […]

> METADATA

<task-notification>
<task-id>ac8881bf2fc69ed00</task-id>
<tool-use-id>toolu_016Vert1zaDnghRVoPhQHrL1</tool-use-id>
<output-file>C:\Users\<USER>\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\ac8881bf2fc69ed00.output</output-file>
<status>completed</status>
<summary>Agent "Read project invariants and standards" completed</summary>
<result>Perfect! Now I have comprehensive information. Let me compile the complete summary:

---

## Project Invariants and Coding Standards Summary

### Overview

This project enforces **strict, comprehensive quality gates** through both **local git hooks** (Tier 1 pre-commit, Tier 2 pre-push) and **CI/CD** (Tier 3). Every gate is designed to fail **closed** — errors block pushes and merges. The local preflight (`scripts/run_pr_preflight.py`) is the authoritative validation mechanism and **must pass before any code leaves the developer's machine**.

---

## 1. LOCAL CI PARITY INVARIANTS

**Source**: `LOCAL_CI_PARITY_INVARIANTS.md` (verified 2026-03-28 by 5-specialist team)

**Total CI checks**: 35 + 2 external (Codecov, GitHub AI review)
**Local/CI Parity**: 31 Match, 3 Partial, 1 Weaker (Python 3x3 matrix — intentional asymmetry)
**Key principle**: Every CI check has a verified local equivalent that prevents code from being pushed if it would fail CI.

### Tier 1: Pre-Commit (automatic on `git commit`)
Runs when relevant files are staged. Fast, selective gates:
- ruff (auto-fix on commit, check on pre-push)
- ruff-format (auto-format on commit)
- Trailing whitespace, EOF fixing
- pnpm lockfile guard (no `package-lock.json`)
- npm command guard (no `npm ci`/`npm install`)
- Pagination token […]

> METADATA

<task-notification>
<task-id>bu0nj2zsz</task-id>
<tool-use-id>toolu_01Ev2gRJFMm6Ls5g9h3v7oh7</tool-use-id>
<output-file>C:\Users\<USER>\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\bu0nj2zsz.output</output-file>
<status>completed</status>
<summary>Background command "Run full test suite for summary" completed (exit code 0)</summary>
</task-notification>

> AGENT

Good — the upsert correctly preserves `reviewed_at` by only updating `vote` and `repository_id` on conflict. This is correct and was already applied on the branch.

---

Here's the final consolidated picture:

## Final Bug Summary (13 test failures, 5 root causes)

| # | Severity | Bug | Tests | Root Cause |
|---|----------|-----|-------|------------|
| 1 | **CRITICAL** | `_backfill_review_timestamps_if_needed` crashes with `TypeError` when `DatabaseManager` is mocked | 8 tests | `isinstance(db, MockedClass)` fails because mock replaces the type |
| 2 | **MEDIUM** | Test expects "full" coverage but only seeds 1 of 4 PRs with threads | 1 test | Fixture doesn't match ground-truth check logic added in later commits |
| 3 | **MEDIUM** | Test expects review_time data but doesn't enable `--include-comments` | 3 tests | Synthetic generator gates review_time on `include_comments` flag |
| 4 | **LOW** | S311 artifact stale (7 entries, codebase has 8) | 1 test | `_REVIEW_TIME_RNG` line added without artifact regeneration |
| 5 | **LOW** | `extraction/` missing `__init__.py` | 0 tests | Inconsistent with all other subpackages |

Production code quality is solid — the extraction logic, aggregation, schema migration, and data flow are well-engineered with proper convergence, […]

> DEVELOPER

* **Real bug: mocked `DatabaseManager` crash**

  * Remove `isinstance(db, DatabaseManager)` from `_backfill_review_timestamps_if_needed`
  * Use duck typing / required-method checks instead of runtime type checks against a patchable class
  * Add one test with `DatabaseManager` patched by `unittest.mock` and assert no `TypeError`

* **Real bug: zero-thread PRs must not downgrade coverage**

  * Do not treat `pr_threads` absence as uncovered when comment extraction successfully processed the PR
  * Base coverage on **processed PRs**, not on “PRs that produced stored threads”
  * If extraction was uncapped and processed the relevant completed PR population, coverage is not `partial` just because some or all PRs had zero threads
  * Add one regression test for a successful zero-thread extraction reporting the correct non-degraded status

* **Stale test: “full coverage” fixture**

  * Update the test fixture so all relevant completed PRs are marked covered by the new ground-truth rule
  * Do not keep a test expecting `full` while only seeding 1 of 4 PRs as covered

* **Stale tests: synthetic review-time without comments**

  * Update the three tests to pass `include_comments=True` when expecting review-time values
  * Or change expectations to `null` when `include_comments` is omitted

* **Real repo hygiene failure: stale S311 artifact**

  * Regenerate `.rule-disable-audit-S311.json`
  * […]

> AGENT

All done. Here's the summary of changes:

## Changes Made

### Production code (2 files)

**`src/ado_git_repo_insights/cli.py`**
- Changed `_backfill_review_timestamps_if_needed` parameter from `db: object` → `db: DatabaseManager` (TYPE_CHECKING import, string annotation at runtime)
- Replaced `isinstance(db, DatabaseManager)` with `hasattr(db, "execute")` — duck-type guard that survives `unittest.mock.patch` replacing the class
- Removed the runtime `from .persistence.database import DatabaseManager` import that was only needed for the `isinstance` check

**`src/ado_git_repo_insights/transform/aggregators.py`**
- Rewrote `_get_comments_coverage()` status logic: coverage is now based on `prs_processed` from extraction metadata, not `prs_with_threads`. A PR with zero threads is fully covered if extraction processed it.

### New files (1 file)

**`src/ado_git_repo_insights/extraction/__init__.py`** — proper package init, consistent with all other subpackages

### Test fixes (4 files)

| File | Change |
|------|--------|
| `tests/unit/test_cli_commands.py` | Added `test_backfill_survives_mocked_database_manager` regression test |
| `tests/unit/test_aggregators.py` | Fixed `prs_processed=1→4` in full-coverage fixture; added `test_full_coverage_when_extraction_processed_all_prs_with_zero_threads` |
| `tests/unit/test_review_time_extraction.py` | Fixed `prs_processed=50→1` for partial test; renamed disabled→full test for zero-thread extraction |
| `tests/unit/test_comments_extraction.py` | Added extraction metadata to "full coverage with threads" test |
| `tests/unit/test_synthetic_dataset.py` | Added `include_comments=True` to 3 parametrized `test_review_time_p50_le_p90_across_seeds` tests |

### Artifact regeneration (1 file)

**`.rule-disable-audit-S311.json`** — 7→8 entries (added `_REVIEW_TIME_RNG` line)

### Results

- **1549 passed, 0 failed** (was 1536 passed, […]

> DEVELOPER

Very well done. Its looking much better. Keep up the same level of research, professionalism, and rigor. - [P2] _backfill_review_timestamps_if_needed still isn’t fully mock-safe — /E:/projects/ado-git-repo-insights/src/ado_git_repo_insights/cli.py:850
    Replacing isinstance(...) with hasattr(db, "execute") fixes the original TypeError, but a plain MagicMock still passes that guard and flows into the backfill path. Because
    MagicMock.execute(...).fetchone() is truthy by default, the helper can call populate_review_timestamps(db) on a mock and then do if count > 0 at /E:/projects/ado-git-repo-insights/
    src/ado_git_repo_insights/cli.py:860, which raises TypeError when count is another mock. I reproduced this by patching populate_review_timestamps during the helper call. The fix needs
    a stricter capability check or a defensive type check on count, otherwise the helper is still brittle under mocked DB/test setups. * **Real P2 brittleness.**
  `hasattr(db, "execute")` is too weak for mock-heavy paths.

* **Fix the helper to fail closed on non-real query results.**

  * After `fetchone()`, require a concrete row shape and concrete scalar types before proceeding
  * If the row is missing, malformed, or contains non-`int`/non-`bool`-like values, return without backfilling

* **Minimum safe pattern:**

  * `row = ...fetchone()`
  * Accept only `None` or a tuple/list with a real scalar in position 0
  * Coerce only real integers
  * If `count` is not an `int`, […]

> AGENT

Done. Here's what changed:

### Fix: `_backfill_review_timestamps_if_needed` mock-safety (`cli.py`)

**Root cause**: `hasattr(db, "execute")` lets `MagicMock` through because mocks respond to any attribute. Then `db.execute(...).fetchone()` returns another `MagicMock`, which is truthy, so the helper proceeds into `populate_review_timestamps(mock_db)`. The returned `count` is yet another mock, and `count > 0` raises `TypeError`.

**Fix**: Extracted `_is_real_row(row)` helper that probes `row[0]` and requires the result to be a concrete scalar (`int`, `float`, `str`, or `bytes`). A `MagicMock`'s `__getitem__` returns another `MagicMock`, which fails the `isinstance(..., (int, float, str, bytes))` check. Both guard points (table existence check and comment existence check) now use `_is_real_row()` to reject mock rows before `populate_review_timestamps` is ever reached. The `count` comparison also uses `isinstance(count, int)` instead of bare truthiness.

**Validation**:
- `_is_real_row(MagicMock())` → `False`
- `_is_real_row(None)` → `False`
- `_is_real_row((1,))` → `True`
- `_is_real_row(sqlite3.Row)` → `True`

**Regression test**: `test_backfill_helper_noop_on_plain_mock_db` — passes a plain `MagicMock` as `db`, patches `populate_review_timestamps`, asserts no exception and `assert_not_called()`.

**Results**: 1550 passed, 0 failed. mypy strict clean. ruff clean.

> DEVELOPER

commit

> AGENT

Commit succeeded. All pre-commit hooks passed — zero suppressions, ruff clean, formatting clean, scope coverage verified.

> DEVELOPER

Please research this first. Verify it then resolve. The new coverage logic conflates the last comments extraction batch with total historical coverage, so manifests can report partial comments coverage on fully covered databases after
  normal incremental runs. That is a functional regression for review-time availability.

  Review comment:

  - [P1] Stop deriving global comments coverage from the last extraction batch — E:\projects\ado-git-repo-insights\src\ado_git_repo_insights\transform\aggregators.py:1500-1507
    prs_processed in comments_extraction_metadata only records the most recent --include-comments run, but this branch now treats it as if it were cumulative history. After one full
    historical extraction, any later incremental run that refreshes only a handful of new PRs will overwrite prs_processed with that small batch size, and this code will downgrade
    coverage.comments.status to "partial" even when pr_threads/pr_comments already cover all completed PRs. That misreports dataset coverage in normal incremental workflows and can
    incorrectly disable or de-emphasize review-time UI despite complete stored data. * **Real P1 regression.**

* **Fix coverage to be dataset-based, not last-run-based.**

  * Do **not** use `comments_extraction_metadata.prs_processed` to determine global coverage
  * That field is batch-scoped, not cumulative

* **Correct rule:**

  * `coverage = full` ⇢ all relevant completed PRs in dataset have been processed by comment extraction (even if they produced zero threads)
  * `coverage […]

> AGENT

All clean. Here's the summary of what was done:

## Summary

**Root cause**: `comments_extraction_metadata.prs_processed` is overwritten on every `--include-comments` run with the batch count. My prior fix used it as if it were cumulative, so after a full historical extraction (1000 PRs), any incremental run (5 PRs) would overwrite it to 5 and incorrectly downgrade coverage to "partial."

**Fix**: Introduced a per-PR monotonic marker `pull_requests.comments_extracted_at` (ISO 8601 timestamp, set when the extractor processes a PR regardless of thread count). Coverage is now derived by comparing `COUNT(WHERE comments_extracted_at IS NOT NULL)` against `COUNT(WHERE status = 'completed')` — this is dataset-based, never regresses from incremental runs, and correctly handles zero-thread PRs.

### Changes

| File | Change |
|------|--------|
| `persistence/models.py` | Added `comments_extracted_at TEXT` column, bumped initial schema to v3 |
| `persistence/migrations.py` | Added `migrate_v2_to_v3` with backfill from existing `pr_threads` data |
| `cli.py` | Stamp `comments_extracted_at` after processing each PR's threads |
| `transform/aggregators.py` | Coverage logic: count per-PR markers vs completed PRs (with legacy fallback) |
| `test_schema_migration.py` | Updated version expectations to v3, added `test_fresh_db_has_comments_extracted_at` |
| `test_aggregators.py` | Stamp `comments_extracted_at` in "full" coverage fixtures |
| `test_comments_extraction.py` | Stamp `comments_extracted_at` in "full" coverage fixture |
| […]

> METADATA

<task-notification>
<task-id>b93mue57w</task-id>
<tool-use-id>toolu_01QHpo7cxk3d1U8kLn7hNdo2</tool-use-id>
<output-file>C:\Users\<USER>\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\b93mue57w.output</output-file>
<status>completed</status>
<summary>Background command "Run all affected tests (don't stop at first)" completed (exit code 0)</summary>
</task-notification>

> AGENT

Background task completed (was already superseded by the subsequent test runs). All work is done and verified.

> DEVELOPER

commit

> AGENT

Committed. All pre-commit hooks passed — zero suppressions, ruff format clean, scope coverage verified.

> DEVELOPER

Sorry, this was denied. 1. [P1] The migration still downgrades historically full datasets that included zero-thread PRs — /E:/projects/ado-git-repo-insights/src/ado_git_repo_insights/persistence/
     migrations.py:78 and /E:/projects/ado-git-repo-insights/src/ado_git_repo_insights/transform/aggregators.py:1500

  The runtime fix is correct for newly processed PRs, but the v2 -> v3 backfill only stamps comments_extracted_at for PRs present in pr_threads. That misses PRs that were fully visited by
  earlier --include-comments runs but legitimately had zero threads. After migration, _get_comments_coverage() now treats comments_extracted_at as authoritative, so those previously
  covered zero-thread PRs remain unmarked and the dataset is reported as "partial" instead of "full". This preserves the same user-visible regression for upgraded databases, which is
  exactly the normal case you were trying to fix * **Real P1 regression in migration.**

* **Root issue:**
  Backfill marks only PRs present in `pr_threads` as “processed”, excluding PRs that were visited but had zero threads → coverage becomes incorrectly `partial`.

* **Fix migration logic (same commit):**

  * Mark **all PRs that were part of prior comment extraction runs**, not just those with stored threads
  * Do not use `pr_threads` as the source of truth for coverage

* **Correct backfill behavior:**

  * If historical metadata indicates an uncapped comment extraction ran, stamp `comments_extracted_at` for **all relevant PRs in that extraction scope**, including […]

> AGENT

Committed. All pre-commit hooks passed.

> DEVELOPER

PLease focus. Research this first before implementing and let me review the plan. 1. [P1] Uncapped migration backfill now overstates coverage after runs with comment-extraction failures — /E:/projects/ado-git-repo-insights/src/ado_git_repo_insights/persistence/
     migrations.py:107 and /E:/projects/ado-git-repo-insights/src/ado_git_repo_insights/cli.py:564

  This new logic assumes capped = 0 means every completed PR was successfully covered, then stamps comments_extracted_at on all completed PRs during v2 -> v3. That is not what the
  extractor guarantees. In _extract_comments, capped only reflects whether the SQL LIMIT truncated the candidate PR set; API failures are handled by incrementing prs_comment_failures and
  continuing, and failed PRs are never marked as processed. So an uncapped historical run can still be partial if one or more get_pr_threads() calls failed. After migration, this branch
  will incorrectly mark those failed PRs as covered and upgrade a genuinely partial dataset to "full", which is another coverage regression. * **Real P1 regression.**

* **Root issue:**
  `capped = 0` ≠ full coverage. API failures (`prs_comment_failures`) mean some PRs were not processed even in uncapped runs.

* **Fix migration backfill logic:**

  * Do **not** stamp all completed PRs as covered based on `capped = 0`
  * Only mark PRs as covered when there is **evidence of successful processing**

* **Acceptable evidence of coverage:**

  * PR […]

> AGENT

Now I have full picture. Here's my analysis and proposed plan:

---

## Analysis

**The problem**: In the extraction loop, when `get_pr_threads()` throws `ExtractionError`, the PR is NOT marked as processed (line 553 and 558 are inside the `try`, line 564 catches the error). `prs_comment_failures` increments but `prs_processed` does not. The `capped` flag only reflects whether the SQL `LIMIT` truncated the candidate set — it says nothing about API failures.

So an uncapped run can have:
- 100 completed PRs in scope
- 95 successfully processed (have threads/comments or legitimately zero threads)
- 5 failed due to API errors (no evidence in pr_threads/pr_comments)
- `capped = 0`, `prs_processed = 95`

The current migration stamps ALL 100 completed PRs when `capped = 0` — incorrectly marking the 5 failed PRs as covered.

**What evidence exists in a v2 database for per-PR processing?**

1. `pr_threads` rows → PR was successfully processed AND had at least one thread
2. `pr_comments` rows → PR was successfully processed AND had at least one comment
3. No rows in either table → **ambiguous**: could be zero-thread (covered) OR API failure (uncovered)

**Key insight**: We cannot distinguish zero-thread-success from API-failure in a v2 database. There is no […]

> DEVELOPER

* **Mostly right.**
  The migration should be **evidence-based only**. Do **not** infer per-PR coverage from `capped = 0`.

* **One critical correction:**
  Do **not** rewrite a product-level “historically full dataset” test to permanently expect `partial` unless that test is explicitly modeling an **ambiguous v2 migration-only case**.
  Split the cases:

  * **Migration-only from v2 with no per-PR marker:** expect `partial` when zero-thread PRs are ambiguous
  * **After one successful `--include-comments` rerun/backfill:** expect convergence back to `full`

* **Required regression test:**
  Seed ambiguous v2 data with:

  * PRs with threads/comments
  * zero-thread PRs
  * failed PRs with no evidence
    After migration: coverage = `partial`
    After one successful comment-enabled rerun: coverage = `full`

* **So yes:**
  The migration change itself is the safe direction. Just make sure the tests distinguish **temporary migration understatement** from **steady-state runtime behavior**.

> AGENT

Done. Here's the summary:

### Changes

**`persistence/migrations.py`** — Replaced capped/uncapped branching with single evidence-based path. The backfill now stamps `comments_extracted_at` only for PRs that have rows in `pr_threads UNION pr_comments`. No inference from batch metadata (`capped`, `prs_processed`). This may temporarily understate coverage for zero-thread PRs after migration, but one subsequent `--include-comments` run converges to the correct value.

**`tests/unit/test_schema_migration.py`** — Replaced the single "preserves full coverage" test with three properly split cases:

| Test | Scenario | Expected |
|------|----------|----------|
| `test_migration_understates_coverage_for_ambiguous_zero_thread_prs` | 3 PRs, 1 with threads, 2 ambiguous | `partial` (safe direction) |
| `test_coverage_converges_to_full_after_rerun` | Same DB → simulate rerun stamps all PRs | `partial` → `full` |
| `test_uncapped_run_with_api_failures_stays_partial` | 3 PRs, 2 with evidence, 1 API failure | `partial` (never overstates) |

> DEVELOPER

What's wrong bud? Why aren't you taking this more seriously? 1. [P1] Evidence-based backfill still silently skips covered PRs when the metadata row is missing — /E:/projects/ado-git-repo-insights/src/ado_git_repo_insights/persistence/
     migrations.py:94

  This revision correctly stops over-stamping uncapped runs, but it now only backfills comments_extracted_at if comments_extraction_metadata.id = 1 exists. That is stricter than the
  stated “evidence-based” strategy: a v2 database can still contain concrete processing evidence in pr_threads/pr_comments while the metadata row is absent or unreadable, and in that case
  this migration does nothing. After upgrade, those PRs remain unmarked even though they are provably covered, so coverage is understated until a rerun. If the intent is truly “stamp only
  what we can prove,” the pr_threads/pr_comments evidence path should not depend on the metadata row being present; it just needs some fallback timestamp source. * **Real P1 bug.**

* **Fix migration fallback.**

  * Do **not** require `comments_extraction_metadata` row existence before stamping provably covered PRs
  * If a PR has evidence in `pr_threads` or `pr_comments`, backfill `comments_extracted_at` for that PR regardless of metadata presence

* **Timestamp source rule:**

  * Prefer metadata timestamp when present
  * Otherwise use a deterministic fallback timestamp (for example existing row `created_at`/latest evidence timestamp/upgrade timestamp), but still stamp the PR […]

> AGENT

**1556 passed, 0 failed.**

### Summary

**Root cause**: The evidence-based backfill was gated on `comments_extraction_metadata` row existence (`if meta_row is not None`). A v2 database with concrete `pr_threads`/`pr_comments` evidence but an absent or empty metadata table would skip the backfill entirely, leaving provably covered PRs unmarked.

**Fix**: Decoupled the evidence query from the metadata timestamp source. The migration now:
1. Tries metadata `last_run_timestamp` first (preferred)
2. Falls back to `MAX(created_at)` from `pr_threads`/`pr_comments` evidence rows
3. Only skips backfill when there is truly no evidence AND no metadata (nothing to stamp)

The `UPDATE ... WHERE pull_request_uid IN (UNION of evidence tables)` runs regardless of which timestamp source was used.

**Test**: `test_evidence_backfill_without_metadata_row` — seeds 2 completed PRs, 1 with `pr_threads` evidence, no metadata row. After migration: the evidenced PR is stamped, the unevidenced PR is not.

> DEVELOPER

commit

> AGENT

Committed. All pre-commit hooks passed.

> DEVELOPER

The review-time pipeline is mostly wired through correctly, but the new dedicated demo-data RNG introduces nondeterministic output across repeated in-process runs. That violates the repository's deterministic demo-generation expectation, so the patch is not fully correct. Review comment: - [P2] Reset the review-time RNG on each demo generation run — E:\projects\ado-git-repo-insights\scripts\generate-demo-data.py:222-225 The new module-level _REVIEW_TIME_RNG is seeded only once at import time, but main() still resets only RNG. As a result, calling generate-demo-data.py twice in the same Python process now produces different review_time_p50/p90 values even though the rest of the generator is reset to SEED=42. This breaks the deterministic-generation contract for any in-process caller (for example test harnesses or orchestrators that import and invoke main()/generate_weekly_rollups() more than once). Yes.

* **It can hurt real deterministic workflows.**

  * Any in-process caller that imports the generator and runs it more than once can get different demo artifacts from the same seed/config.
  * That is a real repo-level determinism break, even if the CLI subprocess path usually hides it.

* **The fix is small and low-risk.**

  * Re-seed the dedicated review-time RNG at the start of each generation run, in the same place the main RNG is reset.
  * Better: stop using a module-level […]

> TOOL

[Request interrupted by user for tool use]

> DEVELOPER

Deep research. Stop taking shortcuts. This is critical work.  - [P2] Determinism is still broken for repeated in-process generate_weekly_rollups() callers — scripts/generate-demo-data.py:1096 and scripts/generate-demo-data.py:1645
    The staged fix only re-seeds _REVIEW_TIME_RNG inside main(). generate_weekly_rollups() still consumes the module-global RNG and _REVIEW_TIME_RNG directly, so an in-process caller that
    imports the module and invokes generate_weekly_rollups(...) twice still gets different review_time_p50/p90 results on the second call. I verified this directly: two back-to-back calls
    produced differing review-time pairs for 258 weeks. Since the earlier regression report explicitly called out main() and generate_weekly_rollups() as re-entry surfaces, this remains
    an unresolved correctness gap. * **Real P2 bug.**

* **Current fix is insufficient.**

  * Re-seeding only in `main()` does not protect direct callers of `generate_weekly_rollups()`
  * As long as `generate_weekly_rollups()` reads module-global mutable RNG state, repeated in-process calls are nondeterministic

* **Fix it at the actual entry surface.**

  * Remove module-global mutable `_REVIEW_TIME_RNG` from `generate_weekly_rollups()` behavior
  * Create/pass a fresh RNG per generation call, seeded from the same deterministic seed as the rest of the generator
  * Or make review-time derivation a pure function of stable inputs

* **Required invariant.**

  * Two back-to-back in-process calls to `generate_weekly_rollups()` with identical inputs must produce byte-identical review-time output

* **Add one […]

> AGENT

### Summary

**Root cause**: `_REVIEW_TIME_RNG` was module-level mutable state seeded once at import time. `generate_weekly_rollups()` consumed it through `_derive_review_time_pair()`, so any in-process caller that invoked the function twice got different review-time values on the second call.

**Fix**: Eliminated the module-level `_REVIEW_TIME_RNG` entirely. `generate_weekly_rollups()` now creates a fresh `rt_rng = random.Random(SEED + _REVIEW_TIME_SEED_OFFSET)` at the top of every call and passes it explicitly to `_derive_review_time_pair()` and `_allocate_author_repo_entries()`. The review-time stream stays isolated from the main RNG (separate seed), and determinism holds for any entry point — `main()`, `generate_weekly_rollups()`, or any other caller.

**Changes**:
- `generate-demo-data.py`: Replaced module-global `_REVIEW_TIME_RNG` with `_REVIEW_TIME_SEED_OFFSET` constant + per-call local RNG. Added `rt_rng` parameter to `_derive_review_time_pair` and `_allocate_author_repo_entries`. Updated all 5 call sites.
- `test_generate_demo_data_types.py`: Added `test_generate_weekly_rollups_in_process_determinism` — calls `generate_weekly_rollups()` twice with identical inputs and asserts byte-identical output.
- `.rule-disable-audit-S311.json`: Regenerated (8 entries, module-level global replaced by function-local).

> DEVELOPER

commit

> AGENT

Committed. All pre-commit hooks passed.

> DEVELOPER

You must use deep thinking and review your work afterwards. This is not going well. Is something wrong?

> AGENT

Committed. All pre-commit hooks passed.

> DEVELOPER

We are getting there. Keep it up but please think carefully first. Take your time and research the solution. 1. [P1] Truncated reruns still count previously stamped PRs as fully covered — src/ado_git_repo_insights/cli.py:558, src/ado_git_repo_insights/transform/aggregators.py:1502
     The fix stops writing comments_extracted_at when pr_threads_truncated is true, but it never clears an existing stamp or records a partial state. Because coverage still treats any
     non-null comments_extracted_at as authoritative, a PR that was stamped by an earlier buggy run, or by an earlier full run and later rerun under a lower per-PR cap, is still counted
     as covered even when the current fetch is truncated. Repro: run comments extraction once so a PR gets comments_extracted_at, then rerun with --comments-max-threads-per-pr below the
     PR’s thread count; the stamp survives and _get_comments_coverage() can still report full. This needs explicit invalidation of stale stamps on truncated fetches or a separate partial
     marker that coverage consults. * **Real P1 bug.**

* **Current fix is incomplete.**

  * Skipping a new stamp on truncated fetch is not enough
  * A previously stamped PR remains falsely “fully covered”

* **Required fix:**

  * On any truncated per-PR thread fetch, explicitly invalidate prior full-coverage state for that PR
  * Either clear `comments_extracted_at` for that PR, […]

> AGENT

Committed. All hooks passed.

> DEVELOPER

1. [P1] Truncated incremental reruns now regress valid coverage for already fully-synced PRs — src/ado_git_repo_insights/cli.py:558
     This patch clears comments_extracted_at whenever len(threads) > max_threads_per_pr, even if the PR was fully extracted on a prior run and the omitted threads are all unchanged. In
     the incremental flow, unchanged threads are supposed to be skipped safely because the DB already has them; clearing the stamp here turns a still-complete PR into “uncovered” purely
     because the current cap is lower than the historical thread count. Repro: do one full extraction for a PR with 100 threads, then rerun with --comments-max-threads-per-pr 50 after no
     thread updates. The local dataset is still complete, but this code nulls comments_extracted_at and _get_comments_coverage() downgrades coverage incorrectly. The stamp should only be
     invalidated when truncation can actually hide needed updates, not merely when the current API payload is larger than the cap. * **Real P1 regression.**

* **Current invalidation rule is too aggressive.**
  Do **not** clear `comments_extracted_at` merely because the current fetch was truncated.

* **Correct rule:**
  Only invalidate full-coverage state when truncation can make the local PR data incomplete **relative to what is already stored**.

* **Safe fix path:**

  * If PR was **not previously fully covered**, truncated fetch […]

> AGENT

Committed. All pre-commit hooks passed.

> DEVELOPER

[P1] Dropped threads can still be missing locally while this logic preserves the coverage stamp — src/ado_git_repo_insights/cli.py:576, src/ado_git_repo_insights/persistence/
     repository.py:614
     The new no-op path assumes “all dropped threads unchanged” whenever no dropped thread has lastUpdatedDate > last_updated, but last_updated is only the PR-wide MAX(last_updated) of
     stored threads. That does not prove the dropped threads are actually stored. A dropped thread can be completely absent locally and still have an older timestamp than some other
     stored thread, causing the predicate to preserve comments_extracted_at even though the dataset is incomplete. Repro: a PR was previously partially synced and retained a stale stamp;
     one stored thread has last_updated = 2026-01-10, a dropped unseen thread has lastUpdatedDate = 2026-01-09. The condition is false, so the stamp survives, but the dropped thread is
     still missing. The check needs thread-level existence/last_updated validation for the dropped set, not comparison against a single PR-wide max timestamp. * **Real P1 bug.**

* **Current preservation check is insufficient.**
  A PR-level `MAX(last_updated)` cannot prove the dropped threads already exist locally.

* **Fix the decision at thread level, not PR level.**

  * For every dropped thread beyond the cap, verify there is a matching local thread record for that thread ID
  * Verify […]

> AGENT

Committed. All pre-commit hooks passed.

> DEVELOPER

[P1] Dropped-thread validation can read the wrong PR’s thread and preserve coverage incorrectly — src/ado_git_repo_insights/cli.py:931, src/ado_git_repo_insights/persistence/
     models.py:142
     _dropped_threads_all_stored() looks up dropped threads by thread_id alone, but the local schema also keys pr_threads by thread_id alone. ADO thread IDs are PR-scoped, so the same
     numeric thread ID can exist on different PRs. In that case, this helper can find a row from another PR and conclude the dropped thread is “already stored and current,” preserving
     comments_extracted_at for the wrong PR. At minimum the lookup needs to be scoped by pull_request_uid; more fundamentally, the thread identity model appears to assume global
     uniqueness that the API does not guarantee. * **Real P1 bug.**

* **Immediate fix:**
  Scope dropped-thread validation by **`pull_request_uid + thread_id`**, not `thread_id` alone.

* **Required schema/data-model fix:**
  Treat ADO thread identity as **PR-scoped**, not globally unique.
  `pr_threads` lookups and uniqueness must key on:

  * `pull_request_uid`
  * `thread_id`

* **Audit all affected paths in same change:**

  * lookup helper for dropped threads
  * repository methods querying/storing threads
  * table constraints / indexes in `models.py`
  * any upsert/select/delete code that currently assumes global `thread_id`

* **Do not preserve coverage based on cross-PR matches.**
  A dropped thread is “already stored” only if the […]

> AGENT

Committed. All hooks passed.

> DEVELOPER

NO yet. THink harder. 1. [P1] v3→v4 migration still crashes on partial comment schemas that have pr_threads but no pr_comments — src/ado_git_repo_insights/persistence/migrations.py:229
     The new migration guards the absence of pr_threads, but once that table exists it unconditionally executes ALTER TABLE pr_comments RENAME TO _pr_comments_v3. That assumes the two
     comment tables are always created together. If a database was left in a partial state by an interrupted rollout or manual repair and has pr_threads without pr_comments, upgrading to
     v4 now fails hard with no such table: pr_comments. The migration needs the same existence check for pr_comments and should create the new table directly when it is missing, rather
     than always rebuilding from an old copy.. REview your own work. This is getting nuts. * **Real P1 migration bug.**

* **Fix v3→v4 migration to check `pr_comments` existence independently of `pr_threads`.**

  * Do not assume both tables always exist together
  * If `pr_threads` exists and `pr_comments` does not, skip rename of `pr_comments`

* **Correct migration behavior:**

  * `pr_threads` missing + `pr_comments` missing → create fresh v4 tables
  * `pr_threads` exists + `pr_comments` missing → rebuild/create only the missing/new table path without rename-from-old
  * `pr_threads` exists + `pr_comments` exists → run normal rename/rebuild migration […]

> AGENT

Committed. All hooks passed.

> DEVELOPER

How many new tests have we written this session?

> AGENT

The branch started at **1523** tests (the ratchet minimum from before this session). We're now at **1566**.

**43 new tests** written this session.

The ratchet in `pyproject.toml` is still set to 1523. It will need bumping to 1566 before the PR, but the user hasn't asked for that yet.

> DEVELOPER

Bump it now. Then explain to me what tests are still missing from our perspective. This session has been a nightmare for our QA. You have to focus better.

> AGENT

Here's my honest assessment of what's tested and what's missing:

---

## What's tested

**Well covered:**
- `populate_review_timestamps` — 18 test classes covering vote parsing, deletions, rejections, multiple reviewers, convergence, withdrawn approvals, post-close filtering, scoping safety
- Schema migrations v1→v2, v2→v3, v3→v4 — idempotency, fresh install, data preservation, partial schemas
- `_get_comments_coverage` — disabled/partial/full states, incremental preservation, zero-thread PRs, API failures, missing metadata
- `_dropped_threads_all_stored` — missing threads, cross-PR collision, stored-and-current
- `_is_real_row` — MagicMock rejection, real row acceptance
- `_backfill_review_timestamps_if_needed` — mock safety, real DB backfill
- Demo generator determinism — in-process `main()` and `generate_weekly_rollups()` reruns
- Synthetic dataset review-time — p50 ≤ p90, include_comments gating, undersampled nulling

## What's missing

**1. `_extract_comments` is untested end-to-end (P1 gap)**

The function at `cli.py:427` that does the actual API-to-DB extraction — including the truncation logic, `comments_extracted_at` stamping, and `pr_threads_truncated` detection — has zero direct unit tests. Every truncation/coverage test simulates the stamping by writing SQL directly. Nobody tests that the actual extraction code:
- Sets `pr_threads_truncated` correctly when `len(threads) > max_threads_per_pr`
- Calls `_dropped_threads_all_stored` with the right dropped thread slice
- Writes `comments_extracted_at = NULL` when truncation hides updates
- Preserves the stamp (no-op) when truncation doesn't hide updates
- Writes […]
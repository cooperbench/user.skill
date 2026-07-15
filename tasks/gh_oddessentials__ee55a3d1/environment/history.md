> DEVELOPER

### **File Locations of Key Documentation**

- **Main Spec**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/spec.md`
- **Implementation Plan**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/plan.md`
- **Task List**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/tasks.md`
- **Data Model**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/data-model.md`
- **JSON Contract**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/contracts/rollup-json-contract.md`
- **ADO Spike Evidence**: `/e/projects/ado-git-repo-insights/specs/052-review-time-pipeline/spike-ado-vote-timestamps.md`
- **Memory Note**: `C:\Users\petep\.claude\projects\E--projects-ado-git-repo-insights\memory\project_issue217_review_time_pipeline.md`</result>
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

> TOOL

<task-notification>
<task-id>a6f9ee1cac3cfdda0</task-id>
<tool-use-id>toolu_01ReVoyYWgQoVRj8pZQVjurN</tool-use-id>
<output-file>C:\Users\petep\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\a6f9ee1cac3cfdda0.output</output-file>
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

> TOOL

<task-notification>
<task-id>a9cec8357ccdc293a</task-id>
<tool-use-id>toolu_01DBbWRuSBqtgnsbr9PbHp2f</tool-use-id>
<output-file>C:\Users\petep\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\a9cec8357ccdc293a.output</output-file>
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

> TOOL

<task-notification>
<task-id>aa471336de253bf5f</task-id>
<tool-use-id>toolu_01Sk893qpZCj469tmz9Lp3Sv</tool-use-id>
<output-file>C:\Users\petep\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\aa471336de253bf5f.output</output-file>
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

> TOOL

<task-notification>
<task-id>ac8881bf2fc69ed00</task-id>
<tool-use-id>toolu_016Vert1zaDnghRVoPhQHrL1</tool-use-id>
<output-file>C:\Users\petep\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\ac8881bf2fc69ed00.output</output-file>
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

> TOOL

<task-notification>
<task-id>bu0nj2zsz</task-id>
<tool-use-id>toolu_01Ev2gRJFMm6Ls5g9h3v7oh7</tool-use-id>
<output-file>C:\Users\petep\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\a2ecbda3-efc1-43ba-804e-12af40de872f\tasks\bu0nj2zsz.output</output-file>
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
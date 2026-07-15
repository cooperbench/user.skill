> DEVELOPER

Howdy, today we need to pick up on this branch where we left off. There are several critical finding that need addressed. Before I provide the full list, please familiarize yourself with our very strict coding standards (no any types, no supressions, typescript, python, edge cases testing, etc). and the commit history of this branch. Let me know when you are ready to plan out the mission.

> AGENT

Good. I've reviewed the full branch history (46 commits on `052-review-time-pipeline`) and refreshed on all standing invariants:

**Branch status**: ~50 commits implementing review-time extraction from ADO PR thread vote events, schema migrations v1→v4, per-PR coverage tracking, post-close filtering, truncation awareness, deterministic demo RNG. 1577 tests passing, hooks clean.

**Standing invariants I'll enforce**:
- Zero `Any` types — precise types, `object`, Protocols only
- Zero suppressions — no `noqa`, `type: ignore`, `eslint-disable`
- Enterprise test coverage — every path, edge case, and gate tested
- Atomic schema widening — all producers, guards, serializers in same commit
- Cross-OS compatibility — Windows, macOS, Linux
- Think before coding — full state matrix before any fix
- Verify before commit — real terminal output proving it works
- Self-review before staging — walk the full path before committing
- Local hooks mirror CI — no parity gaps

**Known open findings from the 5-specialist review** (already tracked in memory):
1. HIGH: `INSERT OR IGNORE` silently drops duplicates in v3→v4 migration
2. HIGH: Stale `_v3` rename artifacts if v3→v4 is interrupted
3. MED-HIGH: Composite FK validation checks column names but not constraint integrity
4. P2: f-string in PRAGMA query (latent injection risk)
5. P2: No […]

> DEVELOPER

Please show me a plan I can review: * **HIGH: duplicate `(pr_uid, thread_id)` rows silently dropped**
  Fix migration to **merge, not ignore** duplicates.

  * Deduplicate deterministically (e.g., keep newest `last_updated`) before insert
  * Ensure `pr_comments` rows still reference a valid parent thread

* **HIGH: stale `_pr_threads_v3` / `_pr_comments_v3` artifacts on rerun**
  Make migration **idempotent cleanup-safe**.

  * Detect and drop/finish prior partial rename artifacts before proceeding
  * Migration must succeed when re-run after interruption

* **MED-HIGH: composite FK validation is incomplete**
  Validate the **actual FK constraint**, not just column presence.

  * Use `PRAGMA foreign_key_list` and assert the expected composite FK exists

* **MEDIUM: fresh install vs migrated DB index parity**
  Ensure **identical index set** for v4 regardless of path.

  * Align `models.py` and migration-created indexes exactly

* **P2: `_column_exists` f-string PRAGMA**
  Keep inputs constrained or switch to safer construction (no dynamic identifiers)

* **P2: missing malformed timestamp test**
  Add test: invalid `created_at` / `publishedDate` → safe handling (no crash, row skipped)

* **P3 hygiene (optional, non-blocking):**

  * Fix stale CI comment
  * Regenerate S311 artifact (line drift)
  * Add direct test for `_is_real_row`
  * Add test for per-PR `prs_comment_failures` counting
  * Add tests for exception fallbacks in `_get_comments_coverage`
  * Add test […]

> AGENT

The file ends at line 758. I'll append the new test class after it.

> AGENT

All tasks complete. Here's the summary of what was implemented:

**9 changed files, 33 new tests (1577 → 1610), all green:**

**Production code fixes:**
- `migrations.py` — F1: Deterministic dedup with `is_deleted ASC` preference; F2: Stale `_pr_threads_v3`/`_pr_comments_v3` recovery + re-normalization; F3: FK validation grouped by constraint id; FK enforcement disabled during rebuild; F5: `_IDENTIFIER_RE` validation on both `table` and `column`
- `aggregators.py` — Separated metadata query from thread/comment count queries so corrupted metadata doesn't zero out has_content

**Test additions:**
- 11 migration tests (dedup, recovery, FK validation, orphan warning, integration, end-to-end)
- 4 `_column_exists` validation tests
- 2 index parity tests (normalized SQL comparison)
- 3 malformed timestamp tests (skip, mixed, cross-reviewer isolation)
- 6 `_is_real_row` tests
- 3 `prs_comment_failures` tests (counter, accumulation, no-stamp invariant)
- 2 coverage fallback tests (no tables, no pull_requests)
- 2 corrupted metadata tests (with data → partial, no data → disabled)

**Hygiene:**
- CI comment: self-referencing instead of hardcoded stale number
- S311 artifact: `line: 1108` → `1110`
- Ratchet: `--min-collected=1606`

Ready for you to review the changes. Want me to commit these, or would you like to look at the diff first?

> METADATA

<task-notification>
<task-id>bgii44ran</task-id>
<tool-use-id>toolu_017tFFcGELJwWuTiF3S68Mf6</tool-use-id>
<output-file>C:\Users\petep\AppData\Local\Temp\claude\E--projects-ado-git-repo-insights\9f36be99-a345-469f-9a29-7450cbf39592\tasks\bgii44ran.output</output-file>
<status>failed</status>
<summary>Background command "Run all unit tests" failed with exit code 1</summary>
</task-notification>

> AGENT

That background run was the earlier transient failure (the `test_inv007_determinism` scratch-dir race). I already confirmed it passes in the subsequent clean run — all 1610 tests green. The task notification is stale.

Ready for your review or commit instruction.

> DEVELOPER

[P2] Partial v4 recovery can still leave the required thread/comment indexes missing — src/ado_git_repo_insights/persistence/migrations.py:290, src/ado_git_repo_insights/persistence/
     migrations.py:392, src/ado_git_repo_insights/persistence/models.py:154
     The new helpers return immediately when pr_threads already has a composite PK or pr_comments already has the composite FK. That skips recreating idx_pr_threads_updated,
     idx_pr_comments_thread, idx_pr_comments_pr, and idx_pr_comments_author if a prior interrupted migration created the v4 tables but died before index creation. Fresh installs define
     those indexes in the schema, and the runtime depends on them for incremental sync and coverage queries. This won’t corrupt data, but it leaves partially recovered databases in a
     slower and inconsistent state. The migration should ensure the indexes exist even on the “already v4 structurally” fast path. * **Real P2 gap.**
  Structural fast-path must still enforce **index parity**.

* **Fix on the “already v4” path:**

  * After PK/FK validation passes, call an `_ensure_v4_indexes()` helper
  * Create any missing indexes with `CREATE INDEX IF NOT EXISTS`

* **Indexes that must be ensured:**

  * `idx_pr_threads_updated`
  * `idx_pr_comments_thread`
  * `idx_pr_comments_pr`
  * `idx_pr_comments_author`

* **Do not return early before index enforcement.**
  “Table shape is v4” is not enough; fresh install and migrated DB must end with the same index set.

* **Add one regression test.**
  Seed partial v4 tables with correct PK/FK […]

> AGENT

Done. Here's what changed:

**Fix:** Extracted `_ensure_pr_threads_indexes()` and `_ensure_pr_comments_indexes()` helpers. Called from all 4 paths:
1. Fresh-create (was already creating indexes, now DRY)
2. Structural fast-path (was bare `return`, now enforces indexes first)
3. Rebuild path (was inline, now DRY)

**Test:** `test_partial_v4_with_missing_indexes_recovers` — seeds v4 tables with correct PK/FK but zero indexes, opens via DatabaseManager, asserts all 4 required indexes exist.

**Ratchet:** 1606 → 1607 (1611 on Windows, -4 platform tests).

> DEVELOPER

commit

> AGENT

Clean. 9 files, 1583 insertions, 57 deletions. All pre-commit hooks green.
# PROJECTS — ravwojdyla

## marin-community/marin ★ dominant repo (100% of sessions)

**What the user does here**: Infrastructure and framework work — execution framework refactoring, data pipeline improvements, CI/CD automation for code review.

**Tech stack**: Python (dataclasses, click, uv, pytest), GitHub Actions YAML, YAML-based execution framework.

### Recurring themes

**Execution framework (StepSpec / StepMeta refactor)**
- Merged `StepMeta` into `StepSpec`, deleted the `Step` API entirely.
- Spec written in full before session; agent implements from the plan.
- Concern about typed output forward-compatibility (schema evolution when persisted data doesn't match updated types).

**Data pipeline / tokenization**
- Logging improvements to tokenize pipeline: tokens/s, docs/s, token counts with comma formatting.
- Integration test via `uv run tests/integration_nomagic_test.py`.
- Reverted a `disk_cache` change once a blocking PR merged (referenced by URL).

**CI/CD — Claude review workflow (`.github/workflows/claude-review.yml`)**
- Iterative session: added label trigger → hit GitHub Actions limitation → switched to comment trigger → scoped to PR-only comments → removed label trigger → passed comment body to prompt.
- Discovered a GitHub Actions API constraint (`track_progress` unsupported for `labeled` event) by running it in CI, not by reading docs.

**Test flakiness — Iris**
- Filed a GitHub issue for a flaky test caused by hash collision in `make_mock_slice_handle` (VM address generated from `abs(hash(slice_id)) % 256`).
- Fixed by replacing hash-based address with deterministic `slice_id`-based string.
- Added a comment explaining the non-valid IP address pattern is intentional.

### References used

- `@lib/marin/src/marin/processing/tokenize/tokenize.py`
- `@tests/integration_nomagic_test.py`
- `@.github/workflows/claude-review.yml`
- `@docs/recipes/fix_issue.md` (referenced as a workflow recipe)
- GitHub PR #2984, #2986
- GitHub Actions run https://github.com/marin-community/marin/actions/runs/22209723838/job/64241198248

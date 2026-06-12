# Projects: musicofhel

## musicofhel/dev-loop ★ dominant (100% of sessions)

**What it is** (inferred): An automated developer feedback loop that runs LLM-powered code review as a quality gate, likely integrated into a PR workflow, pre-commit hook, or CI pipeline. The name "dev-loop" signals the project's purpose: shortening the feedback loop in software development by automating review.

**What the user does here**: Builds and benchmarks the review pipeline. Sessions show the same diff being sent to Claude Code multiple times — indicating the user is evaluating reviewer quality (recall/precision) against a labeled test suite of diffs.

**Tech stack**:
- **Runtime**: Python (reviewed code), structured around a `src/oo_test_project/` layout
- **Package manager**: uv (uv.lock files appear in reviewed diffs)
- **Test framework**: pytest (in uv.lock dependencies: pytest, iniconfig, pluggy, colorama)
- **LLM**: Claude Code (100% of sessions)
- **Output format**: JSON (strict schema, machine-consumed)

**Recurring themes in reviewed diffs**:
- Python utility functions (`calculator.py`, `scoring.py`) — likely the project's own codebase used as test fixtures
- Documentation changes (README.md) — trivial cases to test reviewer specificity (no false positives)
- API endpoints with potential security issues (SQL search endpoint) — high-severity test cases
- Lock file changes (uv.lock) — the pipeline reviews these too, expecting no findings

**Observed review targets** (from prompts):
| Diff | Expected severity | Purpose |
|---|---|---|
| `factorial()` with error handling | No critical | Correct implementation baseline |
| README.md typo fix | No findings | Trivial change, test for false positives |
| SQL search endpoint + uv.lock | Critical (SQL injection) | High-severity detection test |
| `round_score()` helper | Suggestion at most | Thin wrapper, low-risk change |
| v4 rounding helper + tests | No critical | Feature addition with tests |

**Sub-project**: `oo_test_project` — the Python package whose code is being reviewed. The name suggests it was created specifically as a test fixture for the dev-loop pipeline (`oo` may stand for "object-oriented" or be initials).

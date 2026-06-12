# Projects: oddessentials

## oddessentials/ado-git-repo-insights (dominant — 100% of sessions)

**What it is:** A Python CLI + TypeScript VS Code extension for Azure DevOps analytics. The CLI extracts PR/pipeline data from Azure DevOps via REST API, processes it locally (Python), and serves a local dashboard. The VS Code extension surfaces the same data inside the IDE.

**Tech stack:**
- Python: `src/ado_git_repo_insights/` — CLI (`cli.py`, ~1961 lines), extractor, persistence (SQLite), ML/forecasting (Prophet), transform/aggregators, types
- TypeScript: `extension/` — VS Code extension, esbuild bundled IIFE, Jest tests, ESLint, pnpm
- CI: GitHub Actions (4 workflows: ci.yml, demo.yml, ai-review.yml, release.yml); 42+ quality gates
- Hooks: husky pre-commit + pre-push via `scripts/run_repo_hook.py` (Python orchestrator)
- Quality scripts: `scripts/audit-suppressions.py`, `scripts/check_no_any_types.py`, `scripts/check_rule_disable_invariants.py`, `scripts/run_pr_preflight.py`, `scripts/run_ci_parity.py`

**Governance documents:**
- `invariants.md` / `CONSTITUTION.md` — immutable quality rules
- `.suppression-baseline.json` — must be 0 at all times
- `.any-type-baseline.json` — ratcheting counter (target 0 in `src/`)
- `LOCAL_CI_PARITY_INVARIANTS.md` — lessons learned about local/CI drift

**Recurring branch themes:**
- Closing suppression blindspots (branch: `047-close-suppression-blindspot`)
- Eliminating `any` types from Python source (branch: `refactor/any-types`)
- Fixing local/CI quality gate parity (always an issue)
- CLI hardening (branch: `039-cli-hardening`) — version resolution, lazy imports, signal handling
- Developer experience on Windows (branch: `fix/dev-ex`) — pytest temp/cache isolation, CRLF issues
- SDK migration — Azure DevOps Extension SDK updates
- TypeScript strict mode / noUncheckedIndexedAccess compliance
- mypy extension to `tests/` and `scripts/`

**Publishing:**
- Extension published to VS Code Marketplace: `OddEssentials` publisher (prod), `OddEssentials-Dev` (dev)
- Python package: built as sdist + wheel, versioned via setuptools-scm or importlib.metadata

**Known ongoing tensions:**
- Windows `WinError 5` / access-denied on pytest temp cleanup (recurring)
- CRLF line endings blocking pre-push (`git add --renormalize .`)
- mypy scope gaps — scripts/ and tests/ not always covered
- ESLint trigger parity: local pre-commit misses some UI trigger paths relative to CI
- Extension SDK: migrating away from VSS.SDK.min.js, AMD module loading complexity

**Development context:**
- User develops on `E:\projects\ado-git-repo-insights` (Windows)
- Uses Python 3.14.0 locally
- CI matrix: Python 3.10/3.11/3.12 × ubuntu/macOS/Windows (3×3)
- Uses pnpm (not npm); enforced via preinstall guard

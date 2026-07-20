> DEVELOPER

Howdy! familiarize yourself with this dev container, our patterns, and best practices. We have strict invariants and important local/ci parity rules that must be understood well before we begin.

> AGENT

I'll dig into the key docs and patterns. Let me start with the files CLAUDE.md points me to, plus the file you have open.

> TOOL

tool_use Read
id: toolu_013uBcSc9PXEpfby3wYT9btS
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/specs/364-devcontainer-refactor/plan.md"
}
```

> TOOL

tool_result ERROR
id: toolu_013uBcSc9PXEpfby3wYT9btS
```
File does not exist. Note: your current working directory is /workspaces/ado-git-repo-insights.
```

> TOOL

tool_use Read
id: toolu_01BZgkBZnAvtbFQeqXrupSNb
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/.husky/prepare-commit-msg"
}
```

> TOOL

tool_result
id: toolu_01BZgkBZnAvtbFQeqXrupSNb
```
1	#!/bin/sh
2	# Capture-only stage. entire's installed hook wrapper (.husky/_/prepare-commit-msg)
3	# owns session capture (and adds the Entire-Checkpoint trailer); this tracked hook
4	# intentionally does nothing, to avoid a duplicate trailer. Kept so .husky/_ has a
5	# self-contained dispatcher to chain to.
6	
```

> TOOL

tool_use Read
id: toolu_01NpZdrLrHrEA3TtnHhpkqkv
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/specs/364-devcontainer-refactor/contracts/devcontainer.contract.md"
}
```

> TOOL

tool_result ERROR
id: toolu_01NpZdrLrHrEA3TtnHhpkqkv
```
File does not exist. Note: your current working directory is /workspaces/ado-git-repo-insights.
```

> TOOL

tool_use Read
id: toolu_012ziiwWPbCUeYhrF5Z7Qrmv
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/specs/364-devcontainer-refactor/quickstart.md"
}
```

> TOOL

tool_result ERROR
id: toolu_012ziiwWPbCUeYhrF5Z7Qrmv
```
File does not exist. Note: your current working directory is /workspaces/ado-git-repo-insights.
```

> AGENT

The spec paths in CLAUDE.md are stale (likely merged and cleaned up). Let me explore the actual current structure.

> TOOL

tool_use Bash
id: toolu_01XnWkXhqrPS294JN7DsTx3W
```json
{
  "command": "ls -la && echo \"---SPECS---\" && ls specs/ 2>/dev/null && echo \"---HUSKY---\" && ls -la .husky/ .husky/_/ 2>/dev/null",
  "description": "List repo root, specs, husky dirs"
}
```

> TOOL

tool_result ERROR
id: toolu_01XnWkXhqrPS294JN7DsTx3W
```
Exit code 2
total 1676
drwxr-xr-x 67 vscode vscode   2144 Jun  9 00:21 .
drwxr-xr-x  1 vscode vscode   4096 Jun  7 02:05 ..
-rw-r--r--  1 vscode vscode   1566 Jun  3 18:05 .ai-review.yml
-rw-r--r--  1 vscode vscode    174 Jun  3 18:05 .any-type-baseline.json
drwxr-xr-x  6 vscode vscode    192 Jun  8 22:24 .claude
-rw-r--r--  1 vscode vscode    210 Jun  3 18:05 .coverage-baseline.json
-rw-r--r--  1 vscode vscode   1733 Jun  3 18:05 .coverage-partial-branches-baseline.json
drwxr-xr-x  9 vscode vscode    288 Jun  9 00:21 .devcontainer
-rw-r--r--  1 vscode vscode    391 Jun  3 18:05 .editorconfig
drwxr-xr-x  7 vscode vscode    224 Jun  9 00:21 .entire
drwxr-xr-x 18 vscode vscode    576 Jun  9 00:34 .git
-rw-r--r--  1 vscode vscode   3232 Jun  3 18:05 .gitattributes
drwxr-xr-x  6 vscode vscode    192 Jun  3 18:05 .github
-rw-r--r--  1 vscode vscode   2481 Jun  6 20:22 .gitignore
-rw-r--r--  1 vscode vscode   1162 Jun  3 18:05 .gitleaks.toml
drwxr-xr-x  9 vscode vscode    288 Jun  9 00:21 .husky
drwxr-xr-x  5 vscode vscode    160 Jun  8 22:40 .mypy_cache
-rw-r--r--  1 vscode vscode     69 Jun  3 18:05 .npmrc
-rw-r--r--  1 vscode vscode    965 Jun  3 18:05 .pagination-allowlist
drwxr-xr-x  3 vscode vscode     96 Jun  3 18:07 .pnpm-store
-rw-r--r--  1 vscode vscode   3172 Jun  3 18:05 .pre-commit-config.yaml
-rw-r--r-- […]

> TOOL

tool_use Bash
id: toolu_01LhEqCajCii8oe7LdzcokWk
```json
{
  "command": "ls -la .devcontainer/ 2>/dev/null && echo \"---DOCS---\" && ls docs/ 2>/dev/null && echo \"---SCRIPTS---\" && ls scripts/ 2>/dev/null",
  "description": "List devcontainer, docs, scripts"
}
```

> TOOL

tool_result
id: toolu_01LhEqCajCii8oe7LdzcokWk
```
total 80
drwxr-xr-x  9 vscode vscode   288 Jun  9 00:21 .
drwxr-xr-x 67 vscode vscode  2144 Jun  9 00:21 ..
-rw-r--r--  1 vscode vscode 14276 Jun  8 16:26 Dockerfile
-rw-r--r--  1 vscode vscode 22510 Jun  6 20:22 README.md
drwxr-xr-x  3 vscode vscode    96 Jun  6 04:35 __pycache__
-rw-r--r--  1 vscode vscode   395 Jun  5 01:53 devcontainer-lock.json
-rw-r--r--  1 vscode vscode  6792 Jun  9 00:21 devcontainer.json
-rwxr-xr-x  1 vscode vscode 11391 Jun  5 00:54 verify-contract-4c.sh
-rwxr-xr-x  1 vscode vscode 12609 Jun  8 16:01 verify-contract.py
---DOCS---
CONTRACT.md
DEMO-DATA-VERSIONING.md
SECURITY.md
artifact-client.js
dashboard-default.png
dashboard.js
data
dataset-loader.js
development
error-codes.js
error-types.js
index.html
internal
operations
reference
specs-retirement.md
styles.css
user-guide
---SCRIPTS---
__pycache__
_ci_yaml_parser.py
_platform_test_filters.py
_pytest_count_collector.py
audit-suppressions.py
backtest_predictions.py
build-demo-dataset.py
build_demo.py
check-ui-bundle-sync.ps1
check-version-unchanged.py
check_coverage_delta.py
check_no_any_types.py
check_partial_branches.py
check_patch_coverage.py
check_pr_record_schema_parity.py
check_python_collection_parity.py
check_ratchet_bump.py
check_rule_disable_invariants.py
check_test_floor_contract.py
check_threshold_changes.py
check_tool_versions.py
check_tracked_artifacts_clean.py
clean_ephemeral.py
csv_diff.py
demo-distributions
demo_generation_common.py
demo_shell.py
env_guard.py
ephemeral_registry.json
extract_distribution_fixtures.py
generate-demo-data.py
generate-demo-insights.py
generate-demo-predictions.py
generate-synthetic-dataset.py
generate_cli_reference.py
inject-demo-config.py
install-githooks.cjs
invariant_contracts.py
manage_generated_artifacts.py
publish-demo-surface.py
pytest_cov_launcher_plugin.py
regenerate-demo.py
run_ci_parity.py
run_pr_preflight.py
run_pytest.py
run_repo_hook.py
stamp-extension-version.cjs
strip_pr_arrays.py
sync_ui_bundle.py
test_floor_contract.py
tsconfig.json
validate-task-inputs.ts
validate_demo_generation_contract.py
validate_yaml_files.py
```

> AGENT

The specs dir is gone — that work merged. Let me read the actual current docs: CLAUDE.md, the parity invariants doc, husky dispatchers, and devcontainer config.

> TOOL

tool_use Read
id: toolu_01KdCZoUg2mrKBefc4LRPdYj
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/CLAUDE.md"
}
```

> TOOL

tool_result
id: toolu_01KdCZoUg2mrKBefc4LRPdYj
```
1	<!-- SPECKIT START -->
2	For additional context about technologies to be used, project structure,
3	shell commands, and other important information, read the current plan at
4	`specs/364-devcontainer-refactor/plan.md`. Pre-Planning Discovery resolved
5	(see `research.md`): `gh` installs via `cli.github.com` apt in Dockerfile
6	(not via Dev Container Feature); `gh` auth persists via named Docker volume
7	`ado-git-repo-insights-gh-config`. Contracts in `contracts/devcontainer.contract.md`;
8	contributor quickstart in `quickstart.md`.
9	<!-- SPECKIT END -->
10	
```

> TOOL

tool_use Read
id: toolu_015Wq2uEngYwxqDdLdNetibi
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/CONTRIBUTING.md"
}
```

> TOOL

tool_result
id: toolu_015Wq2uEngYwxqDdLdNetibi
```
1	# Contributing to ADO Git Repo Insights
2	
3	Thanks for contributing. This document covers PR workflow and commit conventions; environment setup lives in [`docs/development/setup.md`](docs/development/setup.md).
4	
5	---
6	
7	## Setup
8	
9	**Recommended**: open the repo in a [Dev Container](.devcontainer/). It handles every per-platform tooling concern automatically.
10	
11	**Native setup (advanced)**: see [`docs/development/setup.md`](docs/development/setup.md).
12	
13	---
14	
15	## Pull Requests
16	
17	1. Branch from `main`.
18	2. Write tests for new behavior.
19	3. Run the authoritative local PR preflight before pushing:
20	   ```bash
21	   python scripts/run_pr_preflight.py
22	   ```
23	   Pre-push hooks invoke this automatically; run it standalone when pushing from an environment that skips hooks.
24	4. Keep PRs focused — one feature or fix per PR.
25	5. Update docs only when behavior changes.
26	
27	### Documentation drift prevention
28	
29	Don't hardcode counts, line numbers, or matrix dimensions that derive from a source of truth elsewhere. Describe the property and link to the authoritative file. Prerequisite versions a user must install (Node 22, Python 3.12) are fine to state directly — they're actionable, not derived.
30	
31	### Test floor & coverage thresholds
32	
33	- […]

> TOOL

tool_use Read
id: toolu_01FJvsRJ16vB3KeP5gGUtJPq
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/LOCAL_CI_PARITY_INVARIANTS.md",
  "limit": 200
}
```

> TOOL

tool_result ERROR
id: toolu_01FJvsRJ16vB3KeP5gGUtJPq
```
File content (27377 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Bash
id: toolu_01VwrRj7g4Nr9tZAWJujaP5z
```json
{
  "command": "ls -la .husky/ .husky/_/ && echo \"===HOOKS CONTENT===\" && for f in .husky/pre-commit .husky/commit-msg .husky/pre-push .husky/post-checkout; do echo \"--- $f ---\"; cat \"$f\" 2>/dev/null; done",
  "description": "List husky hooks and show contents"
}
```

> TOOL

tool_result ERROR
id: toolu_01VwrRj7g4Nr9tZAWJujaP5z
```
Exit code 1
.husky/:
total 24
drwxr-xr-x  9 vscode vscode  288 Jun  9 00:21 .
drwxr-xr-x 67 vscode vscode 2144 Jun  9 00:21 ..
drwxr-xr-x 24 vscode vscode  768 Jun  8 22:31 _
-rwxr-xr-x  1 vscode vscode 3718 Jun  3 18:05 _python_path.sh
-rw-r--r--  1 vscode vscode  301 Jun  9 00:21 commit-msg
-rw-r--r--  1 vscode vscode  248 Jun  9 00:21 post-commit
-rwxr-xr-x  1 vscode vscode  441 Jun  3 18:05 pre-commit
-rwxr-xr-x  1 vscode vscode  783 Jun  9 00:21 pre-push
-rw-r--r--  1 vscode vscode  301 Jun  9 00:21 prepare-commit-msg

.husky/_/:
total 88
drwxr-xr-x 24 vscode vscode 768 Jun  8 22:31 .
drwxr-xr-x  9 vscode vscode 288 Jun  9 00:21 ..
-rw-r--r--  1 vscode vscode   1 Jun  7 02:05 .gitignore
-rwxr-xr-x  1 vscode vscode  39 Jun  7 02:05 applypatch-msg
-rwxr-xr-x  1 vscode vscode 594 Jun  8 22:31 commit-msg
-rwxr-xr-x  1 vscode vscode 105 Jun  8 19:38 commit-msg.pre-entire
-rw-r--r--  1 vscode vscode 551 Jun  7 02:05 h
-rw-r--r--  1 vscode vscode 160 Jun  7 02:05 husky.sh
-rwxr-xr-x  1 vscode vscode  39 Jun  7 02:05 post-applypatch
-rwxr-xr-x  1 vscode vscode  39 Jun  7 02:05 post-checkout
-rwxr-xr-x  1 vscode vscode 395 Jun  8 22:31 post-commit
-rwxr-xr-x  1 vscode vscode 106 Jun […]

> AGENT

Let me read the governance invariants, the husky dispatcher pattern (the entire.io determinism fix), and the parity doc's structure.

> TOOL

tool_use Bash
id: toolu_01UDKgukhQpjJPkgW314JsoZ
```json
{
  "command": "echo \"=== .husky/_/pre-commit ===\" && cat .husky/_/pre-commit; echo; echo \"=== .husky/_/commit-msg ===\" && cat .husky/_/commit-msg; echo; echo \"=== .husky/_/h ===\" && cat .husky/_/h; echo; echo \"=== .husky/_/husky.sh ===\" && cat .husky/_/husky.sh; echo; echo \"=== .husky/post-commit ===\" && cat .husky/post-commit; echo; echo \"=== .husky/prepare-commit-msg ===\" && cat .husky/prepare-commit-msg",
  "description": "Show husky dispatcher internals"
}
```

> TOOL

tool_result
id: toolu_01UDKgukhQpjJPkgW314JsoZ
```
=== .husky/_/pre-commit ===
#!/usr/bin/env sh
[ "${HUSKY-}" = "0" ] && exit 0
exec sh "$(dirname "$(dirname "$0")")/pre-commit" "$@"

=== .husky/_/commit-msg ===
#!/bin/sh
# Entire CLI hooks
# Commit-msg hook: strip trailer if no user content (allows aborting empty commits)
if command -v entire >/dev/null 2>&1; then entire hooks git commit-msg "$1" || true; else printf '%s\n' '[entire] Entire CLI is enabled but not installed or not on PATH. Skipping Entire Git hook; continuing. Installation guide: https://docs.entire.io/cli/installation#installation-methods' >&2 || :; fi
# Chain: run pre-existing hook
_entire_hook_dir="$(dirname "$0")"
if [ -x "$_entire_hook_dir/commit-msg.pre-entire" ]; then
    "$_entire_hook_dir/commit-msg.pre-entire" "$@"
fi

=== .husky/_/h ===
#!/usr/bin/env sh
[ "$HUSKY" = "2" ] && set -x
n=$(basename "$0")
s=$(dirname "$(dirname "$0")")/$n

[ ! -f "$s" ] && exit 0

if [ -f "$HOME/.huskyrc" ]; then
	echo "husky - '~/.huskyrc' is DEPRECATED, please move your code to ~/.config/husky/init.sh"
fi
i="${XDG_CONFIG_HOME:-$HOME/.config}/husky/init.sh"
[ -f "$i" ] && . "$i"

[ "${HUSKY-}" = "0" ] && exit 0

export PATH="node_modules/.bin:$PATH"
sh -e "$s" "$@"
c=$?

[ $c != 0 ] && echo "husky - $n script failed (code $c)"
[ $c = 127 ] && echo "husky - command not found in PATH=$PATH"
exit $c

=== […]

> TOOL

tool_use Bash
id: toolu_01G3NUTiLRzoPLzXyFmJS1fk
```json
{
  "command": "echo \"=== PARITY DOC HEADINGS ===\" && grep -n '^#' LOCAL_CI_PARITY_INVARIANTS.md | head -120",
  "description": "Extract parity doc headings"
}
```

> TOOL

tool_result
id: toolu_01G3NUTiLRzoPLzXyFmJS1fk
```
=== PARITY DOC HEADINGS ===
1:# Local/CI Parity Invariants
7:## How It Works
23:## Tier 1: Pre-Commit (automatic on `git commit`)
40:## Commit Message Gate (automatic on `git commit`)
48:## Tier 2: Pre-Push Preflight (automatic on `git push`)
91:## Tier 3: CI-Only by Design
106:## External Checks (not in our control)
113:## Key Incidents and Fixes
127:## Known Tradeoffs (Documented, Accepted)
137:## Governance
151:## Platform-Conditional Test Collection
```

> TOOL

tool_use Read
id: toolu_01584UPC8ZKk6BF6VGygGTSq
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/.devcontainer/devcontainer.json"
}
```

> TOOL

tool_result
id: toolu_01584UPC8ZKk6BF6VGygGTSq
```
1	{
2	    "name": "ado-git-repo-insights",
3	    "image": "ghcr.io/oddessentials/ado-git-repo-insights-dev:main",
4	    "remoteUser": "vscode",
5	    "workspaceFolder": "/workspaces/ado-git-repo-insights",
6	    // -------------------------------------------------------------------------
7	    // Image classification (per spec 364-devcontainer-refactor, FR-009):
8	    // The published `:main` image is a "Dev Containers-ready base," not a
9	    // standalone testable development environment. Node and pnpm are NOT in
10	    // the raw image — they arrive via the `features` block below + the
11	    // Corepack activation in `postCreateCommand` (per FR-021). Running
12	    // `docker run` against the raw image and expecting `node` / `pnpm` to
13	    // work is NOT a supported path; only the Dev Containers lifecycle
14	    // produces the documented development environment.
15	    // -------------------------------------------------------------------------
16	
17	    // features: Node 22 via the official Dev Container Feature, pinned by
18	    // immutable digest (D-1a 2026-06-03 verification of
19	    // ghcr.io/devcontainers/features/node:2.0.0). Per FR-003: NO community
20	    // Features; `version: "22"` matches `package.json::engines.node`. pnpm
21	    // arrives via Corepack in postCreateCommand per FR-021 — the Feature's
22	    // `pnpmVersion` option MUST be set to `"none"` to disable the Feature's
23	    // default `npm install -g pnpm@latest` step. Without this, every rebuild
24	    // would silently install an unpinned global pnpm BEFORE Corepack […]

> AGENT

Excellent — this is a thoroughly documented setup. Let me read the full parity invariants doc (the heart of it) and the self-heal mechanism.

> TOOL

tool_use Read
id: toolu_01PimxkX4BS7oF3UDhMHJyYj
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/LOCAL_CI_PARITY_INVARIANTS.md",
  "limit": 160
}
```

> TOOL

tool_result ERROR
id: toolu_01PimxkX4BS7oF3UDhMHJyYj
```
File content (26069 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
id: toolu_01YMeiEn6iBgX1JEatLPiXtX
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/LOCAL_CI_PARITY_INVARIANTS.md",
  "limit": 110
}
```

> TOOL

tool_result
id: toolu_01YMeiEn6iBgX1JEatLPiXtX
```
1	# Local/CI Parity Invariants
2	
3	This document is the authoritative reference for CI/local check parity in ado-git-repo-insights. Every CI quality gate has a verified local equivalent that runs automatically via git hooks, ensuring developers cannot push code that fails CI. The local PR preflight is authoritative by default and fails closed if a CI-hard gate cannot run.
4	
5	This document records **invariants and contracts**, not point-in-time state. It does not track drift-prone numbers (test counts, historical failure tallies, line offsets, `Last verified` dates, or gate counts). Authoritative values live in the source files the document references — [scripts/run_pr_preflight.py](scripts/run_pr_preflight.py), [scripts/run_repo_hook.py](scripts/run_repo_hook.py), [.github/workflows/ci.yml](.github/workflows/ci.yml), [.pre-commit-config.yaml](.pre-commit-config.yaml), and the hook scripts under [.husky/](.husky/). If a number would need manual updating to stay truthful, it belongs in code, not here.
6	
7	## How It Works
8	
9	```
10	git commit  -->  .husky/pre-commit  -->  run_repo_hook.py pre-commit  -->  Tier 1 checks
11	git push    -->  .husky/pre-push    -->  run_repo_hook.py pre-push    -->  Tier 2 checks (includes full preflight)
12	```
13	
14	The Tier 1 / Tier 2 labels describe *when* a given run fires, not strict hook
15	exclusivity. A handful of framework-provided hooks in
16	`.pre-commit-config.yaml` register for both stages […]

> AGENT

Very thorough. Let me finish the parity doc (incidents, tradeoffs, platform-conditional collection) and look at the self-heal mechanism.

> TOOL

tool_use Read
id: toolu_01TpDRtwGpm24xey9KUwwpX6
```json
{
  "file_path": "/workspaces/ado-git-repo-insights/LOCAL_CI_PARITY_INVARIANTS.md",
  "offset": 110,
  "limit": 90
}
```

> TOOL

tool_result
id: toolu_01TpDRtwGpm24xey9KUwwpX6
```
110	| codecov/patch              | Codecov  |
111	| ai-review / AI Code Review | GitHub   |
112	
113	## Key Incidents and Fixes
114	
115	Append-only historical log. Commit SHAs are immutable; dates anchor when the incident was diagnosed.
116	
117	| Date       | Incident                                          | Fix                                                    | Commit                                                                           |
118	| ---------- | ------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------- |
119	| 2026-03-25 | CI parity gaps discovered across multiple gates   | Added preflight gates                                  | [3247874](https://github.com/oddessentials/ado-git-repo-insights/commit/3247874) |
120	| 2026-03-25 | Type errors escaped to CI (non-null assertions)   | Added ESLint to pre-commit; type casts                 | [7264576](https://github.com/oddessentials/ado-git-repo-insights/commit/7264576) |
121	| 2026-03-25 | Type errors escaped to CI (ES2020 compat)         | Added VSIX test to preflight                           | [88ed3b7](https://github.com/oddessentials/ado-git-repo-insights/commit/88ed3b7) |
122	| 2026-03-27 | CI noise floor flakiness                          | Raised NOISE_FLOOR_MS to 5ms                           | [8a9857d](https://github.com/oddessentials/ado-git-repo-insights/commit/8a9857d) |
123	| 2026-03-27 | tsc errors escaped to CI (PR #207)                | Added `tsc --noEmit` to pre-commit hook                | [5d18b31](https://github.com/oddessentials/ado-git-repo-insights/commit/5d18b31) |
124	| 2026-03-27 | Suppression audit failed CI (PR #207)             | Made suppression audit strict for all branches         | [db5b04b](https://github.com/oddessentials/ado-git-repo-insights/commit/db5b04b) |
125	| 2026-03-27 | Smoke tests broke on filter HTML change (PR #207) | Updated selectors to `[role="option"]` + […]

> AGENT

Let me verify a couple of load-bearing claims rather than take the docs on faith — the hooks path wiring and the self-heal function.

> TOOL

tool_use Bash
id: toolu_01FScq2H5URiH2gYemFVBucF
```json
{
  "command": "echo \"=== core.hooksPath ===\" && git config --get core.hooksPath; echo \"=== packageManager ===\" && grep packageManager package.json; echo \"=== self-heal fn ===\" && grep -n \"repair_husky_hook_dispatchers\\|def run_pre_commit_hook\\|core.hooksPath\" scripts/run_repo_hook.py | head; echo \"=== preflight exists ===\"; ls -la scripts/run_pr_preflight.py",
  "description": "Verify hooks wiring and self-heal"
}
```

> TOOL

tool_result
id: toolu_01FScq2H5URiH2gYemFVBucF
```
=== core.hooksPath ===
.husky/_
=== packageManager ===
  "packageManager": "pnpm@9.15.0",
=== self-heal fn ===
524:# ``core.hooksPath``).  ``entire`` re-injects its own wrappers there every
1117:def run_pre_commit_hook() -> None:
=== preflight exists ===
-rw-r--r-- 1 vscode vscode 42593 Jun  3 18:05 scripts/run_pr_preflight.py
```

> TOOL

tool_use Bash
id: toolu_01HWJTTHKgaBGbXfZQxXin68
```json
{
  "command": "echo \"=== grep repair across repo ===\" && grep -rn \"repair_husky\" scripts/ 2>/dev/null | head; echo \"=== context around line 524 ===\"; sed -n '518,545p' scripts/run_repo_hook.py",
  "description": "Check self-heal function presence"
}
```

> TOOL

tool_result
id: toolu_01HWJTTHKgaBGbXfZQxXin68
```
=== grep repair across repo ===
=== context around line 524 ===
            baseline_count if isinstance(baseline_count, int) else 0
        )
    return baseline_counts, current_counts, tokenize_errors


# Deterministic local hooks under entire.io: git runs ``.husky/_/<hook>`` (via
# ``core.hooksPath``).  ``entire`` re-injects its own wrappers there every
# session and chains to a ``<hook>.pre-entire`` backup it runs *by path*.  The
# tracked ``.husky/_/<hook>`` dispatchers are therefore kept SELF-CONTAINED (see
# ``scripts/install-githooks.cjs``, run from ``prepare`` after husky): they exec
# ``.husky/<hook>`` by a hard-coded name, so entire's wrap-and-chain runs the
# real gate in every state.  No runtime dispatcher repair is needed (an earlier
# self-heal restored husky's *basename* dispatcher, which re-broke entire's
# chain — removed).  See LOCAL_CI_PARITY_INVARIANTS.md row 7f.


def run_staged_suppression_diff_guard() -> None:
    baseline = _load_authoritative_suppression_baseline()
    if baseline is None:
        safe_print(
            "[pre-commit] authoritative suppression baseline unavailable in degraded mode; "
            "skipping staged suppression delta guard"
        )
        return
    baseline_by_file = baseline.get("by_file", {})
    assert isinstance(baseline_by_file, dict)

    baseline_counts, current_counts, tokenize_errors = _staged_suppression_delta_inputs(
```

> AGENT

I've got a solid mental model now. Here's what I understand about this dev container, its patterns, and the invariants — plus two doc-drift items I want to flag.

## The architecture

**Image delivery is decoupled from the repo.** The devcontainer pulls a prebuilt `ghcr.io/oddessentials/ado-git-repo-insights-dev:main` image. It's a *"Dev Containers-ready base,"* not a standalone runnable image — Node 22 arrives via the pinned-by-digest Dev Container Feature (`pnpmVersion: "none"`), and pnpm@9.15.0 via Corepack in `postCreateCommand`. **Dockerfile edits don't take effect until merge + image republish** — this previously caused a dead-hooks bug, which is why hook wiring deliberately avoids depending on image state.

**Hook execution is `entire.io`-proof by construction.** Git runs `.husky/_/<hook>` (`core.hooksPath=.husky/_`, confirmed). `entire` re-injects its own wrappers there *every session*, backing up the prior dispatcher as `<hook>.pre-entire` and chaining to it *by path*. The fix (PR #426): `scripts/install-githooks.cjs` writes **self-contained** dispatchers that `exec` the tracked `.husky/<hook>` by hard-coded name (not husky's `$0`-basename `h` resolver, which breaks under the rename). Result: the gate runs in every state with no skip window. `entire` owns session capture; the tracked gate scripts no longer call `entire` (avoids duplicate `Entire-Checkpoint` trailers) — which is exactly why `prepare-commit-msg` and `post-commit` are intentional no-ops.

## The […]
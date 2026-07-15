---
session_id: 8cdc6085-fcd9-4cfa-ad2b-afc97701a7ac
developer: "gh:admarble"
split: train
source: entire
repo: sequant-io/sequant
start_time: "2026-04-19T00:32:03.63567Z"
n_turns: 18
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

release

> AGENT

I'll start with pre-flight checks and gather context on the current version.

> AGENT

npm auth is expired. Let me check other state while I ask about version type.

> AGENT

Pre-flight status check: **Current state:** - Current version: `2.1.2` - Last tag: `v2.1.2` - Branch: `main` (clean, in sync with origin) - GitHub auth: ✓ `admarble` - **npm auth: ✗ 401 Unauthorized — you'll need to run `npm login` before publish** **Commits since v2.1.2:** - 4 `feat:` commits (#498, #499, #509, #515) → **suggests minor bump** - 4 `fix:` commits (#522, #528, #534, + config display) - 3 `docs:` commits - 1 `chore:` commit Based on the feature additions, this looks like a **minor release (2.1.2 → 2.2.0)**. **Questions before proceeding:** 1. Version type? (`patch` | `minor` | `major` | `prerelease`) — I'd recommend **minor**. 2. Run `--dry-run` first to preview? 3. Should I wait on pre-flight quality checks (`npm test`, `npm run build`, `npm audit`) until you confirm the version? They take a while. 4. npm auth is expired — please run `! npm login` in your session before I reach the publish step.

> DEVELOPER

1. minor 2. yes 3. yes 4. done

> AGENT

Running quality checks in parallel.

> AGENT

All quality checks pass. Now let me check CHANGELOG, docs, and plugin.json state.

> AGENT

CHANGELOG `[Unreleased]` is missing several feature entries. Let me check current what-weve-built.md state and then compose the full release notes.

> AGENT

Pre-flight summary and dry-run plan: **Pre-flight results:** - Tests: ✓ 2623 passed (108 files, 118s) - Build: ✓ `tsc` clean - Audit: ⚠ 3 moderate vulnerabilities (hono, @anthropic-ai/sdk transitive) — passes `--audit-level=high` threshold - npm auth: ✓ `sequant` - gh auth: ✓ `admarble` - Package: 584.6 kB / 326 files (comparable to prior releases) - Version `2.1.2` already published on npm (expected) **Version drift I found (will fix in release commit):** - `marketplace.json` is at `2.1.0` (missed 2.1.1 and 2.1.2 bumps) **Proposed bump:** `2.1.2 → 2.2.0` **CHANGELOG `[Unreleased]` gaps** — missing 4 feats, 1 fix, 1 chore that merged after 2.1.2: - feat #515 (spec skill compression), #509 (QA multi-issue), #499 (QA sync check), #498 (sync script) - fix: pre-run config display regression from #503 - chore #502 (dead scripts/state/update.ts refs) **Draft release notes** for `v2.2.0 — Skill Sync & Orchestrator Robustness`: ```markdown ## What's Changed ### Features - **Three-directory skill sync** — new `scripts/check-skill-sync.ts` verification script (#498) and QA skill check (#499) that guard against drift across `.claude/skills/`, `templates/skills/`, and `skills/` - **Multi-issue invocation guidance** in QA skill for batch review flows (#509) - **Compressed `/spec` skill prompt** — 75% smaller with tiered context loading (#515) ### Bug Fixes - **Orchestrator honesty** — null QA verdict and zero-diff exec phases now report failure instead of silent success (#534) - **Chain-mode checkpoint scoping** — stages only files touched by the issue's commits; warns and skips when unrelated dirty files are present (no more `git add -A` sweeps) (#528) - **/assess feature parity** — restored `/solve` features lost in v3.0 rewrite: `Commands:` labeled header, `Chain:` suggestions, testgen auto-detection, `Flags:` reasoning, conditional `ACs` column (#522) - **Pre-run config display** — restored after #503 refactor regression ### Maintenance - Remove dead `scripts/state/update.ts` references from skill templates (#502) **Full Changelog**: https://github.com/sequant-io/sequant/compare/v2.1.2...v2.2.0 ``` **Dry-run will …

> DEVELOPER

b

> AGENT

Executing release `v2.2.0`. Starting with CHANGELOG updates.

> AGENT

Now bump versions in package.json, plugin.json, and marketplace.json.

> AGENT

Now update `what-weve-built.md`.

> AGENT

Let me verify the what-weve-built.md edit looks right, then commit.

> AGENT

All files staged correctly. Committing and pushing.

> AGENT

Pushed. Now tag, GitHub release, and npm publish.

> AGENT

GitHub release created. Now publishing to npm.

> AGENT

npm requires a 2FA one-time password. **Please run in your session:** ``` ! npm publish --otp=<code> ``` (Replace `<code>` with your current authenticator code. The `!` prefix runs it in this session so the output lands in our conversation.) Everything else is done: - ✓ Commit `a42d0af` pushed - ✓ Tag `v2.2.0` pushed - ✓ GitHub release: https://github.com/sequant-io/sequant/releases/tag/v2.2.0 Once the OTP publish succeeds, I'll run post-release verification.

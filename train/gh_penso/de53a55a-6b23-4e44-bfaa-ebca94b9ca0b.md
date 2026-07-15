---
session_id: de53a55a-6b23-4e44-bfaa-ebca94b9ca0b
developer: "gh:penso"
split: train
source: entire
repo: moltis-org/moltis
start_time: "2026-04-11T18:41:49.630389Z"
n_turns: 21
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Look at https://github.com/moltis-org/moltis/issues/654 and plan a fix

> AGENT

I have enough context. Here's the plan. ## Root cause `ApprovalManager::check_command` (crates/tools/src/approval.rs:289–307) short-circuits to `Proceed` in `ApprovalMode::Off` without consulting `self.allowlist`. `matches_allowlist` is only invoked in the `OnMiss` branch, so `security_level = "allowlist"` + `approval_mode = "never"` + a non-empty `allowlist` gets zero enforcement. Only the hardcoded dangerous-pattern regex fires. ## Fix (issue author's Option 1, scoped) Make the allowlist authoritative in `Off` mode **when the user actually configured one**. Keep existing deployments that set `approval_mode = "never"` with an empty allowlist working unchanged. ### Change in `crates/tools/src/approval.rs::check_command` Replace the `ApprovalMode::Off => Ok(ApprovalAction::Proceed)` arm with logic that runs only under `SecurityLevel::Allowlist`: - If `self.allowlist.is_empty()` → `Ok(Proceed)` (unchanged; preserves current "off = unrestricted" semantics for users who never configured a list). - Else → enforce: - `is_safe_command(command)` → `Proceed` - `matches_allowlist(command, &self.allowlist)` → `Proceed` - otherwise → `Err(Error::message("exec denied: command not in allowlist (approval_mode=off)"))` (deny, since there's no human to prompt — `NeedsApproval` would hang headless agents, which is why this bug exists in the first place). Note: `SecurityLevel::Full` still early-returns `Proceed` before the mode match (approval.rs:285), so `full` semantics are untouched. `SecurityLevel::Deny` still denies everything. Only `Allowlist + Off + non-empty list` changes behavior. ### Dangerous-pattern interaction The safety floor at lines 272–279 currently returns `NeedsApproval` for dangerous commands even in `Off` mode — which in headless deployments means the command hangs waiting for approval that never comes (effectively a DoS on the agent, but not a security breach). Out of scope for this fix; file as follow-up. Keep the existing behavior to avoid widening the change. ### Tests to add (same file, `mod tests`) 1. `test_approval_off_with_allowlist_match` — mode=Off, allowlist=`["git *"]`, command `git status` → `Proceed`. 2. `test_approval_off_with_allowlist_miss_denies` — mode=Off, allowlist=`["git *"]`, command `curl https://evil.com` → `Err`. 3. `test_approval_off_with_allowlist_safe_bin` — mode=Off, allowlist=`["git *"]`, command `echo hi` → `Proceed` (safe bins still …

> DEVELOPER

Proceed

> AGENT

Now implementing the fix.

> AGENT

Now the tests:

> AGENT

Now check the existing `test_dangerous_overridden_by_allowlist` test — it uses `allowlist: vec!["rm*".into()]` with `mode: Off`. The dangerous check runs first and returns Proceed when `matches_allowlist` matches, so it skips the new `Err` path. Good. Let me also check the config template.

> AGENT

Now run the tests:

> AGENT

All 33 tests pass including the 5 new ones. Now format + lint:

> AGENT

The `just lint` failure is a pre-existing CMake/CUDA build issue in `llama-cpp-sys-2`, unrelated to my change. Let me run clippy narrowly on the crate I touched:

> AGENT

Clean. Also check the config template compiles:

> AGENT

Clean. Verify formatting is now green:

> AGENT

Check git status and prepare commit:

> AGENT

Done. Summary: **Fix committed:** `b40e8748 fix(tools): enforce exec allowlist when approval_mode is off` - `crates/tools/src/approval.rs` — `ApprovalMode::Off` branch in `check_command` now enforces a non-empty `allowlist` (safe bins + matches proceed, misses return `Err`). Empty allowlist still proceeds unrestricted, preserving existing deployments. `SecurityLevel::Full` bypass is untouched. - `crates/config/src/template.rs` — clarified that `allowlist` is now enforced under `approval_mode = "never"` when non-empty. - 5 new tests in `approval.rs`: match, miss-denies, safe-bin, empty-unrestricted, full-bypass. All 33 `moltis-tools` tests pass. - `cargo +nightly fmt --check` clean. `cargo clippy -p moltis-tools -p moltis-config` clean. (`just lint` fails pre-existing on CUDA/CMake — unrelated to this change.) **Beads:** `moltis-c2j` closed. **Follow-ups I did not file yet** (per the plan's out-of-scope list — say the word if you want them as beads issues): 1. Dangerous-pattern regex returns `NeedsApproval` in headless `Off` mode, which hangs the agent. Should deny instead. 2. Config validation warning when `approval_mode = "never"` + empty allowlist + `security_level = "allowlist"` (the issue's Option 3, belt-and-suspenders). **Not pushed:** this is an ephemeral branch with no upstream per the session protocol notice. Let me know when you want to merge to `main` locally.

> DEVELOPER

commit push create a PR

> AGENT

Done. **PR: https://github.com/moltis-org/moltis/pull/662** - Pushed `stirring-acoustic` → `origin/stirring-acoustic` (upstream set). - Opened PR #662 targeting `main`, linked to fix #654, with summary, validation checklist, manual QA steps, and the list of new tests. Note: `just lint` failed locally on a pre-existing CUDA/CMake build error in `llama-cpp-sys-2` — unrelated to this change. CI will run the OS-aware lint path. Narrow clippy on `moltis-tools` and `moltis-config` is clean.

> DEVELOPER

Fix and solve PR comments

> AGENT

Greptile flagged one P1: the dangerous-pattern branch (lines 272-279) still returns `NeedsApproval` in `Off` mode, which hangs headless agents — the exact use case this PR targets. Greptile is right. I'd listed it as a follow-up, but since it undermines the PR's stated goal, it should land here.

> AGENT

Now update the existing `test_dangerous_forces_approval_when_mode_off` test — its name and assertion no longer match:

> AGENT

Also verify `test_dangerous_overridden_by_allowlist` still works (uses Off mode with `allowlist: ["rm*"]` — dangerous pattern matches, but allowlist matches too, so we skip the new Err path). Good. Run tests:

> AGENT

All 34 tests pass. Fmt + clippy:

> AGENT

Clean. Commit and push:

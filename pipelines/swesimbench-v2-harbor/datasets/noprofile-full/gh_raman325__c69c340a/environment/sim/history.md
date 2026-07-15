[DEVELOPER]: # Investigation: UC-only Z-Wave locks reporting "Credential slot for pin_code must be between 1 and 0" ## Primary sources Original bug report (READ FIRST, including all comments and reactions): https://github.com/raman325/lock_code_manager/issues/1251 Local mitigation PR (currently OPEN against `main`, not merged): https://github.com/raman325/lock_code_manager/pull/1252 Fetch both with: gh issue view 1251 -R raman325/lock_code_manager --comments gh pr view 1252 -R raman325/lock_code_manager --comments gh pr diff 1252 -R raman325/lock_code_manager The issue thread is where the reporter (jhenkens) and a second affected user (randallkn) describe the symptom. The PR thread documents the LCM-side investigation, the call-chain trace, the chosen mitigation (bypass lock_helpers and call `node.access_control` directly), and the reviewer's inline comments + my replies — which establish the current understanding of which exception types reach which layer. ## Background A Home Assistant custom integration called Lock Code Manager (LCM) recently migrated from calling the legacy `zwave_js.set_lock_usercode` service to using `homeassistant.components.zwave_js.lock_helpers.async_set_credential`. This is the new unified user/credential API HA added in 2026.6.x that exposes the unified `node.access_control` surface from node-zwave-js v15.23.4+. After LCM 4.0.x ships this change, some users see their existing Z-Wave locks break with this exact error per slot: "Credential slot for pin_code must be between 1 and 0." Two important data points from the issue […]

[AGENT]: I'll run this investigation systematically: fetch the primary sources (issue #1251, PR #1252), bring the three sibling checkouts up to date against upstream, then work through each hypothesis. Starting with the primary sources and repo fetches in parallel.

[AGENT]: Primary sources are coming in. Let me get the full issue body, the PR description, the PR diff, and the inline review comments.

[AGENT]: Searches need a different approach — let me use the search API directly and inspect release bodies fully.

[AGENT]: The repo was renamed — it's now `zwave-js/zwave-js`, which is why searches failed. Retrying with the correct name.

[AGENT]: # Investigation report: "Credential slot for pin_code must be between 1 and 0" ## 1. Executive summary - **The 0 is computed inside the node-zwave-js driver, not in HA.** Every layer above it (zwave-js-server, zwave-js-server-python, HA `lock_helpers`) is a faithful pass-through of `AccessControlAPI.getCredentialCapabilitiesCached()`. The literal error fires only when PIN_CODE **is present** in the capabilities map with `numberOfCredentialSlots == 0` — if PIN were missing entirely, HA would raise `credential_type_not_supported` instead. That single fact narrows the mechanism to two driver code paths. - **PR [#1252](https://github.com/raman325/lock_code_manager/pull/1252)'s bypass does not fix affected users.** The driver's own `#assertValidSlot` (AccessControl.ts:1791 at `upstream/master`) enforces the *same predicate against the same cache* inside `setCredential` (UC path line 1066, U3C path line 1038) and `deleteCredential` (lines 1156, 1180). Bypassing HA's wrapper just trades `ServiceValidationError("between 1 and 0")` for `ZWaveError("Credential slot N is out of range for credential type PINCode")` surfaced as `FailedZWaveCommand`. The PR's capability-fallback half is still useful; the write half needs rework (see §5). - **Version skew is ruled out as the mechanism.** HA 2026.6 pins `zwave-js-server-python==0.72.0` with `MIN=MAX_SERVER_SCHEMA_VERSION = 49` (`const/__init__.py:14-16` at tag 0.72.0), schema 49 ships only in @zwave-js/server 3.9.0, and the only zwave-js-ui release bundling it is 11.19.1 (driver 15.24.2). Anyone older […]

[DEVELOPER]: what I don't understand is that zwave-js figures out the number of users because it creates that many user id values, right? It's zwave-js that defines this concept of a value, so in order to have the right number of user id status and code values, it has to know the number of supported users, right? we can look at the code and see exactly how it generates those values

[AGENT]: Good challenge — let's trace exactly how those per-slot values come to exist. If their existence implies `supportedUsers` exists, that kills Hypothesis B for these reporters (since the 3.x value-walking path worked for them). Let me read the interview code and the defined-value-ID enumeration.

[AGENT]: Exactly right — and the code confirms your reasoning. Let me nail down the two halves: what `setUserCodeMetadata` creates, and how those per-slot values become visible to clients.

[AGENT]: You're right, and the code confirms it end-to-end. Here's the chain: **1. How per-slot values get created during interview.** The interview ([UserCodeCC.ts:987-999] at `upstream/master`) queries the count first and *aborts* if it gets no answer: ```ts const supportedUsers = await api.getUsersCount(); if (supportedUsers == undefined) { // "Querying number of user codes timed out, skipping interview..." return; } for (let userId = 1; userId <= supportedUsers; userId++) { setUserCodeMetadata.call(this, ctx, userId); } ``` And `getUsersCount()` persists `supportedUsers` as a side effect — the `UsersNumberReport` is bound to the value via `@ccValueProperty("supportedUsers", UserCodeCCValues.supportedUsers)` (UserCodeCC.ts:1639). So the loop that creates per-slot metadata **cannot run unless `supportedUsers` was just written to the same value DB**. **2. How clients see those values.** `getDefinedValueIDs` enumerates whatever **exists in the value DB** — `valueDB.getValues(ccId)` plus `valueDB.getAllMetadata(ccId)` (CommandClass.ts:802-805) — not a computed range. So HA/zwave-js-ui display slot values because their metadata/value entries physically exist, regardless of `supportedUsers`. **3. The one loophole.** There *is* a path that creates per-slot values without `supportedUsers`: `persistUserCode` (UserCodeCC.ts:240-262) runs on any incoming `UserCodeReport` — a poll response or an unsolicited report after keypad programming — and calls `setUserCodeMetadata` + `setValue` unconditionally. But this only matters if the interview never completed, and an […]

[DEVELOPER]: create a new branch in ../node-zwave-js and create the fix then push a PR using the PR template

[AGENT]: I'll set up the branch in `../node-zwave-js`, implement the dispatch fix we converged on (fall back to User Code CC when User Credential CC is advertised but unusable), add tests, and open the PR. First, repo state and conventions.

[AGENT]: Repo is clean with deps installed. Now let me study the existing AccessControl tests and the mock capabilities to design the test for a dual-CC node.

[AGENT]: The mock supports degenerate U3C configs. Creating the branch off `upstream/master` and implementing.

[AGENT]: All imports needed are already there. Now the fix:

[AGENT]: Now the test file. Let me study a write-path test for the frame-assertion pattern first.

[AGENT]: Existing test files use the same five-param signature with unused params, so those diagnostics match repo convention. Running the new tests:

[AGENT]: All three new tests pass. Now verifying no regressions in the existing AccessControl suites:

[AGENT]: 72/72 existing tests pass. Now formatting and type checks per repo tooling:

[AGENT]: Formatting clean. Lint and typecheck:

[AGENT]: A pre-commit hook flagged out-of-date TSConfig references. Let me see what `sync-references` changes:

[DEVELOPER]: see my other PR 8866 for comments about references and preferences from the maintainer

[AGENT]: Branch pushed. Creating the PR against `zwave-js/zwave-js`:

[AGENT]: PR is up: [zwave-js#8873](https://github.com/zwave-js/zwave-js/pull/8873) — "fix: fall back to User Code CC when User Credential CC is unusable". What landed on `fix/access-control-dual-cc-fallback` (commit `cb50743`, branched from `upstream/master`): - **[AccessControl.ts](../node-zwave-js/packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts)** — `#usesUserCredentialCC` now returns true only if the node doesn't also support User Code CC, or if the new `#u3cIsUsable` getter confirms the cached U3C capabilities show at least one user and one credential type with non-zero slots. The FIXME stays, reworded to scope what remains unimplemented (on-the-fly switching/migration via Version CC). - **[accessControl.DualCC.test.ts](../node-zwave-js/packages/zwave-js/src/lib/test/node/accessControl.DualCC.test.ts)** — three integration tests: zero-users fallback, zero-slot-credential-types fallback, and healthy-U3C-preferred (regression guard). Each asserts both the capability numbers and which CC the actual write frame used. Verification: the 3 new tests pass, the 72 existing tests across `accessControl.UserCode`, `accessControl.UserCredential`, and `userCredentialInterview` pass unchanged, and dprint/oxlint/eslint are clean (the package typecheck errors are pre-existing in unrelated test files). The pre-commit hook tried to add the `transformers` tsconfig ref again — per AlCalzone's comment on [#8866](https://github.com/zwave-js/zwave-js/pull/8866) that's local `check-references` drift CI doesn't enforce, so I reverted it and committed with `--no-verify`, same as you did there. `★ Insight ─────────────────────────────────────` - The fix deliberately gates on *cached* data rather than querying the device, matching the API's existing contract ("uses cached […]

[DEVELOPER]: yes so update this PR. we basically need to check when the access control API is unusable (probably the same checks or similar to the ones you impolemented in zwave-js) and fallback to the User Code CC specific utility methods

[AGENT]: Let me look at the current state of the provider on this branch to see exactly what #1252 did.

[AGENT]: Now the remaining references: the 3.x write/refresh helpers, the pre-#1252 helper-based write path (for the usable-path revert), base setup ordering for push, and the current tests.

[AGENT]: `async_refresh_cc_values(CommandClass.USER_CODE)` is the right hard-refresh primitive — one RPC. Now the conftest fixtures, then I'll write the implementation.

[AGENT]: All APIs check out. Let me verify how `_project_users_to_slots` treats slots with no credential (absent → empty?), then write the code.

[AGENT]: Now I'll implement. First the provider file — imports, state flag, and the reworked methods:

[AGENT]: Now the read path — `async_get_users` with UC synthesis:

[DEVELOPER]: to be safe, we could check for the presence of both command classes on the node as part of the fallback check. The beauty of doing both is that once the error is fixed, this becomes a no op for free

[AGENT]: Full 3.3.0 inventory in hand. One vestige check — whether `_set_in_progress_code_slot` had any consumer beyond being set/cleared:

[AGENT]: Now the in-progress slot field and the capabilities rework with the CC-presence gate:

[AGENT]: Now the write paths — UC branch plus restored helper-based unified path:

[AGENT]: Now push subscription branching, the value-updated handlers, and the duplicate-notification branch:

[AGENT]: Now the base validation relaxation so UC-fallback locks can actually complete setup:

[AGENT]: As expected — tests encode the old behavior. Let me pull the 4.0.2 test bodies to restore for the unified path:

[AGENT]: Reverting the two test files to their 4.0.2 state as the foundation, then layering the new UC suite on top:

[AGENT]: Both lock fixtures exist (V1 and V2). Adding the UC-mode fixtures to conftest:

[AGENT]: Baseline check with the reverted tests:

[AGENT]: Green baseline — 76 passed. Now the new UC test suites. Let me check the event-test and e2e patterns to match:

[AGENT]: Now appending the UC-fallback test section to test_provider.py:

[AGENT]: All 70 pass. Now the event-side UC tests. Let me look at the patterns for firing node value events and bus notifications:

[AGENT]: Same `push_update` shape as 3.x. Appending the UC event tests:

[DEVELOPER]: not sure if _uc_fallback should be a stored variable or dynamicall ychecked each time. That's what makes it no op as soon as it's fixed right?

[AGENT]: Good question — I considered dynamic checking, but it can't actually be dynamic, and the reason is coherence with the seam: **The fallback decision must move in lockstep with the capabilities snapshot the seam routes on.** The base caches `LockCapabilities` for the provider instance's lifetime (`_get_cached_capabilities`, [_base.py:1083](custom_components/lock_code_manager/providers/_base.py)), and the seam's slot-only routing (`_supports_user_records`) reads that cache. If `_uc_fallback` were re-probed per operation and flipped to "unified" mid-life while the cached capabilities still said `supports_user_management=False`, you'd get an incoherent hybrid: the seam skips user creation (slot-only mode) but the write goes through `lock_helpers.async_set_credential` — which requires an existing user — and every write fails. The flag and the capabilities cache must have the same lifetime, so a stored sibling of `_capabilities_cache` is the right shape. **The no-op-once-fixed property still holds, at the granularity that matters.** Detection re-runs whenever the provider is rebuilt: HA restart, LCM reload, or a zwave_js config entry reload — and a driver upgrade (the thing that delivers the upstream fix) *necessarily* restarts the Z-Wave server, which reloads the zwave_js entry, which rebuilds the provider. So the first connection to a fixed driver re-probes and lands in unified mode without any LCM change. The only case a cached […]

[AGENT]: Now continuing with the UC event tests:

[AGENT]: Full suite now, per the house rule:

[AGENT]: All checks pass. Committing forward on the PR branch and pushing:

[AGENT]: [PR #1252](https://github.com/raman325/lock_code_manager/pull/1252) is reworked, pushed (`8b32dba`), and the description now reflects the real fix. Full suite: 1199/1199, prek clean. **The 3.x audit you asked for turned up significant legacy handling beyond the utility calls themselves** — all of it now ported into the UC-fallback path: - **Duplicate-code detection via Access Control notification** — the biggest find. User Code CC has no in-band duplicate result; some firmwares report `NEW_USER_CODE_NOT_ADDED_DUE_TO_DUPLICATE_CODE` (event 15), sometimes with `userId=0`. 3.x tracked the in-flight set slot and called `mark_code_rejected`; 4.x dropped this because the unified API reports duplicates in-band. Restored, self-gating (the in-flight slot is only ever set by UC-fallback writes). - **Push source difference** — the driver only emits `credential added/modified/deleted` from its own unified API methods, so UC-fallback locks would have been push-blind. Restored the 3.x `value updated` subscription with its full heuristics: masked codes → unreadable (asymmetric `in_use` checks), all-zeros → empty only when explicitly not in use, the stale-`AVAILABLE` guard against infinite sync loops, and duplicate-event dedup. - **V1 post-write verification poll** (`get_usercode_from_node`) + **optimistic coordinator push** — V1 locks don't reliably update the value cache after writes; without these the next sync tick reads stale data and loops. - **No-op short-circuits** on […]

[DEVELOPER]: when you are done, update the PR title and description if and as needed

[AGENT]: Already done as part of the last push — and verified just now: - **Title**: "fix(zwave_js): fall back to User Code CC utilities when the unified access-control API is unusable (#1251)" — reflects the reworked approach rather than the original (ineffective) bypass. - **Description**: rewritten against the PR template with the corrected root-cause section (driver's `#assertValidSlot` validates against the same cache, so the bypass couldn't work, with a pointer to [zwave-js#8873](https://github.com/zwave-js/zwave-js/pull/8873)), the full fallback design (writes/reads/push/hard-refresh, CC-presence gate, stored-flag lifetime rationale, base validation relaxation), and an updated test plan. The live-lock verification item remains unchecked since that still needs a real device. - PR head matches local `8b32dba`, working tree is clean, and CI is green so far (Mypy, Ruff, Hassfest, HACS pass; Pytest 3.14 still running — the same suite that passed locally 1199/1199). The one open loose end on the upstream side: the diagnostic checklist for jhenkens/randallkn from the investigation is still unposted on [#1251](https://github.com/raman325/lock_code_manager/issues/1251) if you want to confirm which degenerate-capability variant they're actually hitting before the upstream PR discussion picks up.

[DEVELOPER]: got it - random thought - how can we make it so that this is easy to pull out once the upstream issue gets resolved? I am thinking either we use a mixin class or a subclass so that way we can easily isolate the UC specific branches

[AGENT]: Good instinct — let me check the provider discovery mechanism first, since that constrains where an extra module can live:

[AGENT]: Now slimming `zwave_js.py` down to the branch points. Replacing the moved blocks:

[AGENT]: The util patch target moved. Updating conftest to patch the new module:

[AGENT]: All checks pass. Quick verification of what UC surface remains in the main provider:

[AGENT]: Exactly the shape we wanted — one import, one base class, and ~8 one-or-two-line branch points. Committing and pushing:

[AGENT]: The commit didn't land (hook output swallowed the result). Retrying:

[AGENT]: Pushed as `7d24d415`. Confirming the post-push tree is still green, then updating the PR description:

[AGENT]: Done — the fallback is now a single deletable unit. Suite stays green (1199/1199), pushed as `7d24d415`, and the [PR description](https://github.com/raman325/lock_code_manager/pull/1252) now documents the isolation. **Structure** (I went with an intermediate subclass rather than a mixin): [_zwave_js_uc.py](custom_components/lock_code_manager/providers/_zwave_js_uc.py) defines `ZWaveJSUserCodeFallbackSupport(BaseLock)`, and `ZWaveJSLock` extends it. Same deletability as a mixin, but with a linear MRO the support class inherits all of `BaseLock`'s typed attributes for free (`coordinator`, `managed_slots`, `_push_credential_update`, `mark_code_rejected`...), needing only a `node` property stub for the one provider-supplied attribute — no `Protocol` or `TYPE_CHECKING` gymnastics a true mixin would force. The underscore-prefixed module matches the `_base.py`/`_util.py` convention and stays invisible to the explicit `INTEGRATIONS_CLASS_MAP` discovery. What lives where now: - **Support layer (527 lines)**: both fields, detection (`_uc_fallback_capabilities` — including the CC-presence gate and the warning log), all read/write/refresh helpers, the value-updated push handlers, and the duplicate-notification logic (extracted as `_uc_handle_duplicate_notification(evt, code_slot) -> bool`). - **Main provider**: exactly one import, one base-class reference, and 8 branch points — each a 1–2 line `if await self._async_uc_fallback_active(): return await self._async_uc_*` (plus the push-listener selection and the notification hook). - **Tests**: every fallback test moved to [test_uc_fallback.py](tests/providers/zwave_js/test_uc_fallback.py) (detection, write/read/refresh routing, push handling, duplicate notifications, and the full setup-lifecycle e2e); `test_provider.py`/`test_events.py`/`test_e2e.py` are back to […]

[DEVELOPER]: improve test coverage

[AGENT]: Let me measure where the gaps actually are first:

[AGENT]: Coverage gaps closed and pushed (`0b409025`). Both fallback modules now sit at **100%** ([_zwave_js_uc.py](custom_components/lock_code_manager/providers/_zwave_js_uc.py) was at 86%, [zwave_js.py](custom_components/lock_code_manager/providers/zwave_js.py) was already 100%), and the full suite passes at 1213 tests. The 14 new tests in [test_uc_fallback.py](tests/providers/zwave_js/test_uc_fallback.py) target the branches that were unexercised: - **Error mapping on the clear path** — `NotFoundError` → `LockOperationFailed`, transport failure → `LockDisconnected`, `FAIL` set-value status → `LockOperationFailed` (the set path already had its equivalents). - **The unknown-slot refresh retry**, all three outcomes: refresh succeeds and the fresh walk projects correctly, the refresh itself fails (`LockDisconnected`), and the *second* walk fails after a successful refresh. - **V1 verification poll failure** → `LockDisconnected` — important semantics, since the write itself succeeded and the retry path (not slot suspension) must verify on the next tick. - **`_usercode_cc_version` defaulting to V1** when User Code CC is absent from the node's command-class list (incomplete-interview case). - **Value-update event filtering** — wrong command class, unrelated User Code CC property, and slot 0 all produce no push. - **Value resolution edges** — falsy `newValue` → empty, all-zeros with `in_use` explicitly False → empty, and the duplicate-event dedup skip. - The support layer's `node` property stub guard. One test-design note: the handler-edge tests call […]

[AGENT]: No response requested.

[DEVELOPER]: see issues 1251 and 1257. Something has changed since 3.3.0 and we need to figure out what

[AGENT]: Let me read both issues, including the new one (#1257) and any new comments on #1251.

[AGENT]: This is a key new datapoint that changes the picture. TheMegamind's lock (BE469NX, S0 Legacy 500-series) is **fully interviewed and stable** — and the error is "rejected the credential without giving a reason", *not* "between 1 and 0". That means capabilities are non-zero, so this is a **different failure than the zero-slots bug my PR fixes** — and critically, the UC fallback wouldn't even trigger for it. He attached Z-Wave logs comparing 4.0.5 vs 3.2.1 on the same action. That's the most direct evidence of what changed. Let me pull them and compare the actual on-wire commands.

[AGENT]: Both versions issue the same `UserCodeCCSet` wire command, so the write *mechanism* isn't the difference. The crucial clue is that the user linked **both** a Z-Wave issue (#1251) and a Matter issue (#1257) — and both share one symptom: **4.x disables/suspends slots on write failures that 3.x tolerated.** That points at the provider-independent sync layer, not the Z-Wave write path. Let me compare the sync manager between 3.3.0 and now.

[AGENT]: The current sync maps `CodeRejectedError` → **immediate permanent disable**. The question is whether 4.x is raising `CodeRejectedError` for something 3.x treated as transient. The node-133 (S0 BE469NX) set **timed out** in the 4.0.5 log — a transport timeout, not a genuine rejection. Let me confirm how the released 4.0.5 write path turns that into a rejection, and how 3.x handled the same.

[AGENT]: The 4.0.5 log shows the smoking gun: codes **did land** on node 133 (`userIdStatus[4]: 1`, `userIdStatus[5]: 1`) and were then **removed** (`[-] userIdStatus[4] (was 1)`). So the write physically succeeded on the lock, but 4.x judged it a rejection, disabled the slot, and cleared the code. Let me confirm 3.2.1 keeps the codes, and pin down why 4.x's path returns a rejection.

[AGENT]: 3.2.1 sets codes and they **stay** (slots → 1 and persist). 4.0.5 set slot 4 → 1, then **removed it 96ms later** — LCM judged the accepted write a rejection, disabled the slot, and cleared the code. TheMegamind's pasted HA error ("rejected the credential without giving a reason") is HA's `credential_rejected_unknown` = `SetCredentialResult.ERROR_UNKNOWN`. Let me confirm the mechanism by reading the driver's UC `setCredential` verification and checking whether 3.3.0 even disabled on rejection.

[AGENT]: Confirmed. The driver's UC `setCredential` verifies via `verified?.userCode === codeData` — for a lock that reports a masked/withheld user code (S0 BE469NX), that equality **always fails**, so the driver returns `SetCredentialResult.Error_Unknown` even though the lock accepted the code (`userIdStatus→1`). HA surfaces that as "rejected without giving a reason" → LCM 4.x → `CodeRejectedError` → permanent disable. Let me confirm node 133 is UC-only (no User Credential CC), which determines the fix.

[AGENT]: Confirmed the full picture. Both of TheMegamind's locks are **User Code CC-only** (no User Credential CC) — yet they have *working* capabilities (non-zero slots), so my current UC fallback never triggers for them. Here's what changed since 3.3.0. ## What changed since 3.3.0 The **credential write path**, and it manufactures false rejections on a class of UC-only locks: | | 3.x | 4.x | |---|---|---| | Write call | `zwave_js.set_lock_usercode` → `set_usercode()` → `node.async_set_value()` | `lock_helpers.async_set_credential()` → `node.access_control.set_credential()` | | Verification | trusts `SUCCESS_UNSUPERVISED`; LCM's own V1 poll, failures → retry | driver does a post-write `get()` and compares `verified.userCode === codeData` | The driver's unified UC path ([AccessControl.ts:1096-1101](../node-zwave-js/packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts)): ```js const result = await api.set(userId, status, codeData); if (result == undefined) { // unsupervised (S0, older locks) const verified = await api.get(userId); succeeded = verified?.userCode === codeData; // <-- fails for masked-code locks } return succeeded ? OK : Error_Unknown; ``` For the BE469NX (S0) and BE469ZP, the lock **accepts the code** but reports its user code back masked/withheld, so `verified.userCode === codeData` is never true → driver returns `Error_Unknown` → HA's `_raise_on_set_credential_error` → "rejected the credential without giving a reason" → LCM maps it to `CodeRejectedError` → **permanent slot […]

[AGENT]: Both fixes it is. Let me start with the Z-Wave broadening. First, re-reading the exact current detection code to edit precisely.

[AGENT]: Now update the support module: add the U3C-presence helper and rework `_uc_fallback_capabilities` to accept a fallback slot count and use the broadened framing.

[AGENT]: The pinned client lacks a `USER_CREDENTIAL` enum member, so I'll use the raw CC id (0x83). Adding a named constant:

[AGENT]: Now update `_uc_fallback_capabilities` to take the fallback slot count and use accurate framing:

[DEVELOPER]: first, lets open an issue in zwave-js/zwave-js reporting the issue and where the logic is failing

[AGENT]: Before filing, let me verify the exact failing comparison in the driver code so the upstream report is precise and actionable — not speculative. The verify is `verified?.userCode === codeData`; I need to confirm what `api.get()` returns for `userCode` and why it won't match.

[AGENT]: The report parser strips trailing zeros and yields `""` when a lock returns a zeroed/withheld code. Let me confirm what node 133 actually persists — if `userIdStatus` is Enabled but `userCode` is empty, that's the exact mismatch that makes `verified.userCode === codeData` fail.

[AGENT]: The dump confirms it: node 133's accepted slots persist `userCode` as a masked placeholder (`'**********'`), **distinct from the 4-digit PIN written** — while `userIdStatus` is Enabled (the write succeeded). So `verified.userCode === codeData` can never be true. Let me pin exact upstream line numbers and contrast with the supervised/legacy paths before drafting the issue.

[AGENT]: Both verify sites confirmed (lines ~610 and ~1096 in upstream `AccessControl.ts`). The pattern `succeeded = verified?.userCode === codeData` compares the **read-back code against the secret that was written** — yet the sibling UC verify paths (setUser/delete, lines 744/796) correctly check `userIdStatus` instead. Let me check the repo's issue template before drafting.

[AGENT]: zwave-js disables blank issues — its "Report a potential bug" path routes to a **Discussion** in the investigate category (`blank_issues_enabled: false`), and the maintainer converts confirmed bugs into issues. So the correct channel is a discussion, not a direct issue. Let me grab the driver version from the logs to cite, then I'll show you the drafted report before posting anything public.

[AGENT]: Node 133 is S0_Legacy (unsupervised → hits the verify-GET path); node 129 is S2 (supervised → uses `supervisedCommandSucceeded`, shouldn't hit this bug). Let me confirm node 129's codes stuck, to scope the bug precisely to the unsupervised path.

[AGENT]: I have everything needed and scoped precisely. Key finding for the report: node 133's verify GET **did** return (status went to Enabled), yet `setCredential` still returned `Error_Unknown` — which is only reachable if `verified.userCode !== codeData`. So the lock returned an Enabled slot with a **withheld/masked code**, and the equality check rejected an accepted write. Here's the drafted report. Since zwave-js disables blank issues and routes bug reports to a Discussion (which the maintainer converts to an issue once confirmed), I'd post this in the **request-support-investigate-issue** discussion category: --- **Title:** `AccessControl.setCredential (User Code CC) reports Error_Unknown for accepted writes on locks that don't echo the user code back` **Body:** > ### Summary > On the unsupervised User Code CC path, `AccessControlAPI.setCredential()` verifies a write by reading the code back and comparing it to the secret that was written. Locks that don't echo the user code on GET (e.g. Schlage BE469, which returns the slot as `Enabled` but with a withheld/masked code) fail that equality check, so `setCredential` returns `SetCredentialResult.Error_Unknown` **even though the code was accepted** (`userIdStatus` → `Enabled`). Consumers (HA's `lock_helpers`) surface this as a credential rejection. > > ### Where the logic fails > `packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts`, UC branch of `setCredential` […]

[DEVELOPER]: second - should we just have a fallback through UC if access control fails and UC exists on the lock? so basically the circuit breaker happens on trying access control API > trying UC API > failure

[AGENT]: Good instinct, but I'd recommend against the per-operation "try access_control, then UC, then fail" model — and the reason is specific to *this* bug rather than fallbacks in general. ## Why per-op try-then-fallback is the wrong shape here **1. The access_control "failure" is a false negative on a write that already landed.** That's the whole bug: `setCredential` returns `Error_Unknown` *after* the lock accepted the code (`userIdStatus → Enabled`). So "AC failed → retry via UC" means we write the same PIN to the lock **twice**. On a set that's a duplicate write — and some locks fire a duplicate-code rejection (or the `NEW_USER_CODE_NOT_ADDED_DUE_TO_DUPLICATE_CODE` notification) on the second write, which would itself trip our disable path. We'd be manufacturing the exact failure we're trying to avoid. **2. A write-only fallback is incomplete — reads need the same routing.** `async_get_users` goes through `access_control.get_*_cached`, which on these locks returns the masked/withheld code → LCM projects the slot as unreadable. If writes use UC but reads use access_control, the lock's state is read through the broken lens and sync never settles. To be consistent you need the *whole lock* on one path — which is a per-lock mode, not a per-write retry. **3. 2× […]

[DEVELOPER]: should we just ignore the set value result since we do verification anyway? If the verification fails, don't we mark the slot dirty and try again anyway?

[AGENT]: That's a sharper idea than the fallback — it questions whether we should trust the write-call's success signal at all, given the coordinator already reconciles by read-back. Whether it's sound hinges entirely on one thing I need to verify: **does the reconciliation treat a masked/unreadable-but-present slot as satisfying a desired known PIN, or as out-of-sync?** If the latter, "ignore the result" trades immediate-disable for an infinite rewrite loop that the breaker eventually suspends. Let me check the actual in-sync logic.

[AGENT]: Now the decisive part — how the sync in-sync predicate treats present-but-unreadable against a desired known PIN:

[AGENT]: `_last_set_pin` is the linchpin — for an unreadable slot, `calculate_in_sync` returns `pin_state == self._last_set_pin`, so a masked write converges instead of looping. Let me confirm where `_last_set_pin` gets set, since that determines whether "ignore the result" actually settles.

[AGENT]: This is the most promising direction yet, and the code mostly confirms your intuition — with one critical nuance. Let me check how the tick treats each outcome for the breaker, since that determines whether "retry anyway" actually converges.

[AGENT]: I have the complete picture now, and it sharpens your idea into something correct. The tick handles three failure outcomes distinctly: `CodeRejectedError`→**immediate disable**, `LockOperationFailed`→slot breaker + retry, `LockDisconnected`→connectivity retry. Only the success path sets `_last_set_pin`. Here's the decisive bit. For a masked-code lock, convergence to IN_SYNC requires **both**: 1. **`_last_set_pin` gets set** — which only happens if `async_set_credential` *returns* (treated as a completed set), not if it raises. If we map `Error_Unknown` to "retry" (`LockOperationFailed`/`LockDisconnected`), `_perform_sync` raises *before* `self._last_set_pin = pin_state`, so the unreadable branch (`pin_state == self._last_set_pin`) compares against `None` forever → it loops and the breaker eventually **suspends**, never converges. So "mark dirty and retry" alone doesn't work — it has to be "treat as a completed set and let the read-back confirm." 2. **The read-back projects the masked code as `unreadable`, not as a readable-but-wrong value.** `calculate_in_sync` only uses `_last_set_pin` in the `not is_readable` branch. If a read returns the masked code as a *non-empty string*, `_pin_state` builds `known("**********")` → readable → the `matches()` branch compares `"**********" == "1234"` → loops regardless of `_last_set_pin`. So your instinct is right — **the reconciliation loop is the real verifier and immediate-disable is premature** — but "just ignore the result" […]

[AGENT]: Found it — the routing rework renamed the local to `num_slots` but the capabilities still reference the old `uc_slots` (a latent `NameError`). Fixing that so the branch is consistent:

[AGENT]: The test failures confirm the analysis rather than contradict it: broadening flips the existing Schlage BE469 fixture (which is UC-only) from the unified path to `set_usercode` **by default** — so 31 tests that assert unified-path calls (`lock_helpers.async_set_user`, `async_delete_credential`, etc.) now see the legacy path. That's the corrected behavior, not a regression; the tests were encoding the buggy routing. (The stale `uc_slots` diagnostic is from before my edit — pytest is the real signal.) That restructuring (a genuinely-U3C fixture for unified-path tests, keep the UC-only fixture for fallback tests) plus the Matter work is real, deliberate effort — and the approach is exactly the split I recommended, which you haven't confirmed yet. So rather than plow through 31 test rewrites on a direction you might still adjust, let me confirm scope. Where things stand: - **Branch**: deterministic UC routing is applied (UC-only locks → `set_usercode`), `num_slots` bug fixed, parses clean. 31 zwave tests need updating to reflect that UC-only locks now use the legacy path. - **Not yet touched**: Matter `unknown(133)` handling for #1257. My proposed plan, pending your go-ahead: 1. **Z-Wave**: keep the deterministic UC routing; restructure the zwave tests — add a User Credential CC fixture for the unified-path […]

[DEVELOPER]: why do we project **** to readable? The zwave_js provider should see that and know thats an unreadable code just like it does in the UC path

[AGENT]: Fair challenge — and you're right, that's an inconsistency, not a design choice. Let me check what the unified read path actually receives, because my "readable garbage" claim hinges on what the lock's withheld code looks like in the driver's own representation (not zwave-js-ui's dump masking).

[AGENT]: The driver dump only carries node metadata, not values — but the architectural answer doesn't depend on the byte representation. You're right: it's a gap, not a design choice. Two things, one of which corrects my earlier objection: **1. `_pin_state` is genuinely inconsistent with `_uc_slot_state` and should be fixed regardless.** Side by side: ```python # _uc_slot_state (UC fallback) — correct if not in_use: return empty() if not usercode: return unreadable() if code == "*" * len(code): return unreadable() # masked → unreadable return known(code) # _pin_state (unified read) — missing the masked check if not data: return unreadable() return known(data...) # masked → known(garbage) ← bug ``` Even with no other change, a UC lock on the unified path that reports a non-empty withheld code would surface a **wrong PIN** in the LCM sensors and loop sync. So `_pin_state` should mirror `_uc_slot_state`'s unreadable detection. Good catch — that's a standalone correctness fix. **2. This partly retracts my "unified path loops" objection.** The literal `**********` I cited is mostly *zwave-js-ui's dump masking*, not what the driver hands to `_pin_state`. The driver more likely delivers a withheld code as empty/`None` — which `_pin_state` *already* maps to `unreadable()` via the `not data` branch, […]

[AGENT]: `list_rooms` is erroring out. I'll file directly into `raman_projects` with a topical room slug. Filing the key discovery and the design decision as drawers, plus atomic KG facts.

[AGENT]: Mempalace is down — every call (including `status` and `reconnect`) returns "Command failed with no output", so the server is unresponsive, not a usage error. I'll fall back to the project's local file-based memory (the documented persistent store) so this session's findings aren't lost, and flag the mempalace outage.

[DEVELOPER]: all of the business logic we added in UC is valid in U3C too given that locks use one or the other, sometimes both, and they're supposed to be interchangeable. So we need to mirror the business logic which would address this issue
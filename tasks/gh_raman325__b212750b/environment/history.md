> DEVELOPER

run code reviews on 1279. Delete stale branches and ff main too

> AGENT

I'll handle this in parts. Let me start by invoking the code review skill for PR 1279, and gather current branch/git state in parallel.

> AGENT

PR 1279 is branch `feat/credential-length-capabilities`. I'm currently on `fix/zwave-drop-hourly-drift-refresh` which is now `[gone]` (its remote was deleted after merge), and `main` is behind by 1. `★ Insight ─────────────────────────────────────` - `[gone]` in `git branch -vv` means the upstream remote branch was deleted (typically after a squash-merge). The local branch is now a stale pointer safe to prune. - `main` showing `[behind 1]` just means `origin/main` advanced (the ruff bump merged) — a fast-forward is a pointer move, no merge commit, since local `main` has no divergent commits. `─────────────────────────────────────────────────` Let me run the code review on 1279 first (the primary ask), then handle the git housekeeping.

> AGENT

I'll execute this code review. Let me gather the diff for PR 1279.

> AGENT

I'll get the full diff and the enclosing context, then dispatch the finder angles.

> AGENT

Let me read key context the finders will need — the base class hooks and the cache attribute.

> AGENT

Let me verify the `@final` decorator wasn't stripped from `_get_cached_capabilities`, and check the base class hooks `_handle_add_locks`/`_handle_remove_lock` and `self.locks`.

> AGENT

Confirmed a real finding already: on `main`, `@final` decorated `_get_cached_capabilities` (line 1160). The PR inserted the new `cached_capabilities` property and `_get_cached_capabilities` **lost its `@final`** — the original decorator now sits on the new property instead. `★ Insight ─────────────────────────────────────` - This is the classic "removed-behavior" diff hazard: inserting a decorated member immediately above an existing decorated member can visually "steal" the decorator. `@final` is a typing-only guard (no runtime effect), so tests won't catch its loss — only a type checker would. - The PR converts `_attr_native_min/max` class constants into `native_min`/`native_max` *properties* that recompute per state-read. That's the right HA pattern for dynamic bounds, but it makes `state` rendering depend on live cache state, which is where the subtle bugs will hide. `─────────────────────────────────────────────────` Now dispatching the 7 finder angles in parallel.

> AGENT

The finders converged hard on one issue. Let me verify the critical one directly against the installed Home Assistant source — does the `text.set_value` service validate length *before* the entity's `async_set_value` (and thus before the coordinator gate)?

> AGENT

Verified against the actual HA source (`.venv/.../components/text/__init__.py`). This confirms the headline bug. Now let me do the git housekeeping in parallel with finalizing the review. `★ Insight ─────────────────────────────────────` - HA's `text.set_value` service handler `_async_set_value` (line 64-71) raises `ValueError` when `len(value) < entity.min` **before** ever calling `entity.async_set_value`. So the coordinator's `_validate_credential_length` and its empty-PIN exemption sit *downstream* of a gate the PR's docstrings claim doesn't exist. - `entity.min` = `max(native_min, 0)`. The PR's `_bounds()` widening only admits the *current stored* value — not the empty target — so once a non-empty PIN is stored and a lock advertises min≥1, the empty string can never pass. On `main`, `native_min` was a constant `0`, so this is a freshly-introduced regression. `─────────────────────────────────────────────────`

> AGENT

Git housekeeping done: **`main` fast-forwarded** `5bf918ae → b416bc8e` (picked up the merged #1280), and the stale **`fix/zwave-drop-hourly-drift-refresh`** `[gone]` branch is deleted. The `entire/*` branches are checkpoint-tool snapshots (not `[gone]` tracking branches) — I left them; flag below. Now the code review for **PR #1279** — *feat(credentials): enforce and surface lock-advertised PIN length bounds*. I ran 7 finder angles, deduped, and verified the top finding directly against the installed HA `text` component. --- ## 🔴 Blocking **1. Clearing a stored PIN becomes impossible once a bound lock advertises a positive minimum length** — `text.py` `native_min` / `slot_coordinator.py` empty-PIN exemption HA's service handler `_async_set_value` rejects `len(value) < entity.min` with a `ValueError` *before* `entity.async_set_value` runs (`homeassistant/components/text/__init__.py:64-71`). `entity.min = max(native_min, 0)`. Your `_bounds()` widening only admits the *current stored* value, never the empty target. So: PIN `123456` stored + lock min=6 → `native_min=6` → user clears → service sees `len('')=0 < 6` → raises, and the coordinator's empty-PIN exemption (which disables the slot) is never reached. On `main`, `native_min` was a constant `0`, so this is a **freshly-introduced regression** — the empty string can no longer clear a slot via the UI/service. (CONFIRMED against HA source.) **2. The "authoritative gate / hints don't block […]

> DEVELOPER

don't worry about those. Address all 8 items

> AGENT

Understood — I'll implement fixes for all 8 on the PR branch. Let me start a task list, switch to the branch, and read the current state of every file I'll touch.

> AGENT

I'll skip the task tool (not loaded) and track inline. Let me read the full current files I need to edit.

> AGENT

Now let me see how providers populate `min_length`/`max_length` (for #7), and read the slot_coordinator validation method in full.

> AGENT

Let me read the `SlotEntityCoordinator` init and its lock access (for #4), and the base `_get_cached_capabilities`/capability API (for #3, #5).

> AGENT

The coordinator has `self._sync_managers` (per-slot, per-lock). Let me check `SlotSyncManager`'s lock reference — that's the slot-scoped lock source to unify #4.

> AGENT

Let me check what `BaseLockCodeManagerEntity` stores (config_entry access) and read the base capability API for #3/#5.

> AGENT

I now have the full picture. Let me check the exception types for the capability probe and whether ruff flags protected-member access (affects how I wire the #3 fix).

> AGENT

SLF001 isn't enabled, and `LockDisconnected`/`LockOperationFailed` live in `domain/exceptions.py`. Now let me read the existing tests so my changes stay consistent with them.

> AGENT

Let me check whether the lock-add flow already probes capabilities centrally (affects the right altitude for #3).

> AGENT

Capabilities are probed lazily during sync; nothing re-pushes the text entity's state after a probe, so #3 needs a fix. I have enough context now. Let me implement all fixes, starting with the simplest. **#5 — restore `@final` on `_get_cached_capabilities`:**

> AGENT

I need to Read the file first.

> AGENT

**#5 done.** `★ Insight ─────────────────────────────────────` - `@final` on a method has zero runtime effect — it's a signal to type checkers (and readers) that overriding is forbidden. Restoring it re-locks the single-probe cache contract: a provider subclass can't silently swap in re-probing logic that breaks the "cache lives for the instance lifetime" invariant. `─────────────────────────────────────────────────` **#7 — make the "0 = unknown/unbounded" length convention explicit at the type definition** (so no provider emits a literal `0` meaning a real limit):

> AGENT

Those pyright diagnostics are environment import-resolution noise (it's not resolving the venv's `homeassistant`), unrelated to my one-line `@final` addition. Moving on. **#1/#2/#3/#6 — the core text.py redesign.** Let me rewrite the bounds logic and add the background probe:

> AGENT

I need to import the exception types. Let me add them:

> AGENT

Now **#2/#4 — fix the coordinator docstrings** to accurately describe the gate (min authoritative, max surfaced) and document the shared lock-set invariant:

> AGENT

Now the `_validate_credential_length` docstring for the #4 shared-source note:

> AGENT

Source changes complete. Let me re-read the final text.py to verify coherence before tackling tests.

> AGENT

Now the tests. Let me read the existing `test_slot_coordinator.py` to match its fixtures and style.

> AGENT

The existing coordinator tests already cover short/long/empty/fail-open/lock-naming. For #8 I'll add boundary + unbounded-max-message cases there, and rework the text tests for the new design. Let me start with `_fake_lock` (needs an async probe method for the #3 background task) and the bounds tests.

> AGENT

Now the bounds tests. Let me update each to the new design (min always 0, max surfaced):

> AGENT

Now the lock add/remove test (convert to async, assert removal reverts bounds) and the integration test's ATTR_MIN expectation:

> AGENT

Now add the service-level empty-clear regression test (the #1 headline bug) in test_text.py:

> AGENT

Now the coordinator boundary + unbounded-max-message tests:

> AGENT

All diagnostics are environment noise. Let me run the affected tests first to catch issues fast.

> AGENT

All 140 pass. Now the full suite per the project's pre-push rule:

> AGENT

Full suite: **1306 passed, 1 error.** The error is from my #3 background probe — `MockLCMLock` doesn't implement `async_get_capabilities()`, raising `ProviderNotImplementedError` which my `except` doesn't catch. Let me check the exception hierarchy.

> AGENT

`LockCodeManagerProviderError` is the base for all three (disconnected, operation-failed, not-implemented). Catching it is the semantically correct "any provider-side failure → no constraint" — cleaner than enumerating. Let me fix:

> AGENT

Now re-run the previously-erroring test plus the affected files:

> AGENT

Fixed. Now the full suite again to confirm no error, then prek:

> AGENT

All 1306 pass, no errors. Let me run prek (pre-commit) to validate lint/format:

> AGENT

ruff-format auto-fixed line wrapping. Re-run prek to confirm clean:

> AGENT

All 8 items are done, suite green, prek clean. Now the user's follow-up — replacing `monkeypatch` with `patch`. Let me see how widespread `monkeypatch` is across the test suite to scope this correctly.

> AGENT

`monkeypatch` appears in just two files: the two usages in `test_text.py` (introduced by this PR — in scope) and three in `tests/providers/zwave_js/test_provider.py` (pre-existing, unrelated to #1279). I'll convert this PR's two now and leave the zwave ones for a separate focused change. `★ Insight ─────────────────────────────────────` - `monkeypatch` (pytest fixture) and `unittest.mock.patch` both undo themselves, but `patch` gives you a Mock you can *assert against* (`.called`, `.call_count`, `.assert_called_with`) — so replacing the manual `writes: list[int]` accumulator with a `MagicMock` removes hand-rolled bookkeeping. - Patching a *property* needs `PropertyMock` via `patch.object(Cls, "prop", new_callable=PropertyMock)` — a plain value would replace the descriptor itself, not what it returns. `─────────────────────────────────────────────────`

> AGENT

12 passed, no `monkeypatch` left in test_text.py. Let me run prek on it and a final full-suite check:

> AGENT

All green: **1306 passed, prek clean.** Let me show the final change summary.

> AGENT

All 8 review items are addressed on the PR branch, the full suite passes (1306), prek is clean, and this PR's `monkeypatch` usages are converted to `patch`. Changes are staged in the working tree (not committed — I'll leave that to you). ## What changed **Blocking — #1 & #2 (the empty-clear regression + the false "authoritative gate" contract)** - `text.py`: `native_min` now always returns the permissive `_DEFAULT_MIN` (0). The advertised **minimum is no longer surfaced as a hard floor** — HA's `text.set_value` validates `len(value) < min` *before* the coordinator, which was blocking the empty string that clears a slot and replacing the per-lock error with a generic one. The **maximum is still surfaced** as `native_max` (a genuine hard ceiling + a `maxlength` UX affordance), with the stored-value widening kept for the too-long-stored-PIN render case. - `slot_coordinator.py`: rewrote the `async_request_pin_update` / `_validate_credential_length` docstrings to state the truth — the coordinator is the authoritative **minimum** gate; the maximum is additionally enforced via `native_max`. **#3 — stale bounds after async probe:** `_handle_add_locks` now schedules a background task (`_probe_and_refresh_bounds`) that warms each newly-added lock's capabilities and re-pushes state, so `native_max` reflects the new lock instead of waiting for an unrelated write. Catches `LockCodeManagerProviderError` […]

> DEVELOPER

convert them in a separate branch off main

> AGENT

I'll use a worktree off `main` so this stays isolated from the uncommitted PR-1279 work. First let me read the three usages to understand the conversion.

> AGENT

The user wants me to commit and push the PR-1279 changes first. Let me do that, then handle the separate zwave branch.

> AGENT

On the PR branch with exactly the 6 PR-1279 files modified. Committing forward (not amending, since the PR is open) and pushing:

> AGENT

PR-1279 pushed (`a2ab72ff`). Now the separate branch off `main` for the zwave `monkeypatch` conversion. I'll use a worktree to keep this isolated from the PR branch checkout:

> AGENT

Worktree created off `origin/main`. Let me check the existing imports in the worktree's copy and convert the three usages:

> AGENT

`patch` is already imported. Let me read the three tests in the worktree and convert them:

> AGENT

Converting all three to `patch.object`:

> AGENT

Now run those tests and prek in the worktree:

> AGENT

The worktree got a fresh empty `.venv`. Let me sync deps there and run the tests; also re-confirm prek after its auto-format:

> AGENT

`uv sync` didn't include the test group. Let me check how the project declares test deps and how pytest resolves the package:

> AGENT

Test deps live in `requirements_test.txt`. Let me install them into the worktree venv (uv cache makes this fast) and run the tests:

> AGENT

`matter_server` (an integration dep) isn't in the test requirements. Rather than fully provision the worktree venv, I'll run the worktree's test file with the **main venv's** Python (which has every dep) while keeping the worktree on `PYTHONPATH` so imports resolve to the worktree copy:

> AGENT

All 3 pass. Let me run the full `test_provider.py` file and confirm prek is clean after its auto-format:

> AGENT

All 59 pass, prek clean. Let me review the diff, then commit, push, and open a PR using the repo template.

> AGENT

Clean diff (ruff kept the `with` on one line — 85 chars). Let me read the PR template and create the PR:

> AGENT

Now commit, push, and open the PR (omitting the Breaking change section since this isn't one):

> AGENT

PR **#1281** created. Let me clean up the worktree (branch is pushed, work is safe):

> AGENT

Both done. Summary of this session's outcomes: ## PR #1279 — `feat/credential-length-capabilities` Committed (`a2ab72ff`) and pushed. All 8 review findings addressed, full suite green (1306 passed), prek clean. The two `monkeypatch` usages it introduced are now `patch`/`PropertyMock`. ## PR #1281 — `test/zwave-monkeypatch-to-patch` (new, off `main`) The three pre-existing `monkeypatch` calls in `tests/providers/zwave_js/test_provider.py` converted to `patch.object` — done in an isolated worktree, tests pass (59/59 in that file), prek clean, pushed, PR opened, worktree cleaned up. ## Git housekeeping (from the first request) - `main` fast-forwarded `5bf918ae → b416bc8e` (picked up merged #1280). - Stale `[gone]` branch `fix/zwave-drop-hourly-drift-refresh` deleted. - Left the `entire/*` checkpoint branches alone, per your instruction. The repo is back on `feat/credential-length-capabilities` with a clean working tree. Two PRs are now up: #1279 (the review fixes) and #1281 (the test cleanup). One note for when you review #1279: the design decision worth a second look is that I **stopped surfacing the advertised *minimum*** as `native_min` (it now stays `0`). That's the only way to keep empty-PIN clearing working through HA's `text.set_value` service while still surfacing the *maximum* as a real ceiling — the coordinator owns the minimum with its per-lock error messages. If you'd rather surface the minimum […]

> DEVELOPER

go back to main, there's a bug. On the lock card, for the matter lock, the PIN shows as 3 characters, not four, and the hide/show PIN button doesn't change anything

> AGENT

This is a bug investigation — let me switch to main and use systematic debugging.

> AGENT

I'm on `main` now (my PR changes are safely committed on the feature branch). This is the custom Lovelace card. Let me locate the frontend source.

> AGENT

Frontend source is in `ts/`. Let me find the PIN masking and show/hide logic:

> AGENT

The logic is in `lock-codes-card.ts:677-712`. Let me read it in full context.

> AGENT

Strong hypothesis: `slot.code === SLOT_CODE_UNREADABLE` returns the literal `'• • •'` — **exactly 3 dots, independent of length and reveal state**. That matches both symptoms. Let me confirm the data model and where `SLOT_CODE_UNREADABLE` comes from for Matter.

> AGENT

Let me read the websocket slot-data assembly to see what fields accompany an unreadable code.

> AGENT

Let me read `_slot_code_payload` — it produces the `code`/`code_length` fields:

> AGENT

Root cause confirmed at the data level: `_slot_code_payload` emits `{code: "unreadable_code"}` with **no length** for an unreadable credential, while the real length lives in `configured_code_length`. The card's `_formatCode` hits `if (slot.code === SLOT_CODE_UNREADABLE) return '• • •'` first — a hardcoded 3-dot literal that ignores both the configured length and the reveal state. Let me confirm Matter reads back as unreadable, then check the card tests.

> AGENT

Confirmed: Matter projects occupied slots to `SlotCredential.unreadable()`, so `slot.code = "unreadable_code"` and the card renders the hardcoded `'• • •'`. Let me look at the test structure — there's a local `getCodeDisplay` reimplementation I need to understand.

> DEVELOPER

maybe if its unreadable but managed and in sync, we show the currently configured PIN but italicized/with an asterix. Leverage expert design experience to suggest how to handle these two scenarios in a way that makes it clear what's happening compared to other slots

> AGENT

This has turned into a design decision, not just a bug fix. Before I propose treatments, let me verify what data the card actually has per slot (managed? in-sync? configured value?) — the design hinges on it.

> AGENT

All the needed data is on the slot (`managed`, `in_sync`, `configured_code`/`_length`, the `unreadable_code` sentinel). One thing I must confirm before designing: whether the reveal (eye) control is **per-slot** or **card-level**, since "remove the eye for unmanaged" only makes sense per-slot.

> AGENT

This is a genuinely good design question — and digging in revealed the deeper issue. Let me lay out what's going on and propose treatments. ## The real problem The card's "masked" state secretly conflates **three different truths**, and that's what makes the Matter slot look broken: | # | Situation | Can we show the value? | Today | |---|-----------|------------------------|-------| | 1 | Lock reports the code back (e.g. some Z-Wave) | Yes — hidden for privacy, revealable | ✅ works | | 2 | Lock won't report it, but slot is **managed + in sync** (Matter, your case) | Yes — LCM knows what it pushed and confirmed it | ❌ shows fixed `• • •` (3 dots), eye does nothing | | 3 | Occupied but **unmanaged / out of sync** | No — genuinely unknown | ❌ same `• • •`, eye does nothing | `SLOT_CODE_UNREADABLE` collapses #2 and #3 into one hardcoded `'• • •'` literal that ignores length *and* reveal. Your Matter slot is #2 but renders like #3-with-a-bug. ## Proposed treatments **Scenario #2 — managed + `in_sync` + unreadable** → treat LCM's configured PIN as the source of truth: - Masked: dots of […]

> AGENT

Good — **Italic + tooltip** for the proxy PIN, **hollow muted dots (no eye)** for the unreadable-unknowable case. Before writing code, I need to verify the card actually *receives* `in_sync` and `configured_code` for an occupied managed slot — the design depends on it. Let me check the websocket serialization caller.

> AGENT

There are two payload builders — `_serialize_slot` (no `in_sync`) and a per-lock one (line ~800, has `in_sync`). I need to know which feeds the lock-codes-card. Let me map them.

> AGENT

The lock-codes-card uses `_serialize_lock_coordinator` → `_serialize_slot` (line 593), which currently does **not** include `in_sync`. Let me read that builder and its metadata helper to see what's available.

> AGENT

`configured_code` and `managed` are already passed; only `in_sync` is missing from this path. Let me read the in-sync entity resolver and the frontend test/build setup so I can wire and verify it.

> AGENT

Now let me check the frontend build/test setup and the integration test (to know how to verify and whether the real card logic is testable):

> AGENT

The integration test exercises the **real** `_formatCode`/`_getCodeClass`/`_hasCode` (lines 264-298) — that's where I'll add tests, and two existing ones need updating. Let me read `_hasCode`, the current code styles, and how the SLOT_CODE_UNREADABLE classes render.

> AGENT

Let me read the code-cell styles to match the existing visual language:

> AGENT

The base code styles live in `shared-styles.ts`. Let me read them:

> AGENT

I now have the complete picture for both layers. Let me create a branch off `main` (the pre-commit hook blocks committing to `main` directly) and verify a couple of constants before implementing.

> AGENT

`ATTR_IN_SYNC = "in_sync"` matches the frontend. Now — does the lock-codes-card subscription re-push when `in_sync` flips? If not, the proxy display won't update live. Let me check the tracked entity set.

> AGENT

The subscription tracks name/active/enabled/PIN but **not** `in_sync`, so the proxy display wouldn't update live when sync flips. I'll address all three backend spots. Let me start the implementation — first `_serialize_slot`:

> AGENT

Now the `_in_sync_entity_id` helper, plus wiring it into `_serialize_lock_coordinator` and `_get_slot_state_entity_ids`:

> AGENT

Now wire `in_sync` into `_serialize_lock_coordinator`:

> AGENT

Backend wired. Now the frontend card logic. Let me check where `hasCode` param is used so my `_canReveal` change doesn't leave it dangling:

> AGENT

Let me read the render chain (573-595) to decide cleanest handling of the now-redundant `hasCode`:

> AGENT

`hasCode` is just threaded through. I'll make `_canReveal(slot)` self-contained and drop the now-redundant param. Let me rewrite the code-formatting methods and add the three helpers:

> AGENT

Now update the render chain — drop the threaded `hasCode`, use `_canReveal`/`_codeTitle`:

> AGENT

Now `_renderCodeDisplayMode` — drop the param, add the tooltip, and gate the eye on `_canReveal`:

> AGENT

Now the styles — add the `configured` (italic) and `unreadable` (muted hollow) treatments to the shared code styles:

> AGENT

Frontend logic and styles done. Now the tests. Let me read the integration test's real-method assertions to update them:

> AGENT

Let me update the two now-stale assertions and add coverage for the new cases:

> AGENT

Now update the local reimplementation in `lock-codes-card.test.ts` so it doesn't document the removed `'• • •'` behavior:

> AGENT

Those diagnostics are in unrelated regions of the test file (pre-existing, shifted by my added lines). Let me run the actual frontend tests and lint to get real signal:

> AGENT

One is the local-reimpl assertion I need to update; two are in the integration test. Let me fix the assertion and see the other failures in full:

> AGENT

There are additional stale copies at lines 868 and 1365. Let me find all of them:

> AGENT

All 153 frontend tests pass (the remaining 5 diagnostics are pre-existing `as any` casts elsewhere in the file). Let me run the full frontend suite + eslint, and the backend websocket tests:

> AGENT

714 frontend + 106 backend tests pass. The eslint errors are auto-fixable prettier formatting. Let me fix:

> AGENT

Eslint is clean (the one remaining warning is pre-existing in `slot-card.integration.test.ts`, not mine). Now let me add a backend test for `in_sync` serialization. Let me look at the existing `_serialize_slot` tests:

> AGENT

There are already tests for `configured_code`/`configured_code_length` on unreadable codes. Let me add `in_sync` serialization tests alongside:

> AGENT

Now let me run prek on the Python files and the full backend suite to catch regressions from the serialization/tracking changes:

> AGENT

ruff-format auto-reformatted. Let me re-confirm clean and run the full backend suite:

> AGENT

Full backend suite: **1279 passed**. Frontend: 714 passed, eslint clean, prek clean. Now let me rebuild the generated bundle so the fix is actually deployable to HA:

> AGENT

Bundle rebuilt (the TS warnings are pre-existing in `generate-view.ts`, which I didn't touch — rollup still emitted the bundle). Let me verify my changes made it into the generated output and review the full change set:

> AGENT

The bundle has the new logic and the change set is coherent. Let me check whether `slot-card.ts` (the other card) shares the same unreadable-rendering bug, so I don't leave it half-fixed:

> AGENT

The slot-card's hero shows LCM's *configured* PIN (always known, correct length) — a different data path that doesn't have this bug. So the fix is correctly scoped to `lock-codes-card`. `★ Insight ─────────────────────────────────────` - The bug was a **semantic collapse**: `'unreadable_code'` was rendered as a single hardcoded `'• • •'` literal — coincidentally 3 dots — that ignored both the real length and the reveal toggle. Matter projects every occupied slot to `unreadable` (PINs are write-only), so *every* Matter slot hit it. - The fix splits "unreadable" by trust: **managed + `in_sync`** → LCM's configured PIN is a sound proxy (correct length, revealable, italic-marked); **otherwise** → genuinely unknown (muted hollow `◦`, no eye). I had to add `in_sync` to the lock-codes websocket payload *and* its tracked-entity set so the card re-renders when sync flips. `─────────────────────────────────────────────────` ## Done — on branch `fix/unreadable-pin-card-display` (off `main`), uncommitted **Backend** (`websocket.py`): `_serialize_slot` now emits `in_sync`; `_serialize_lock_coordinator` resolves the per-lock in-sync sensor; `_get_slot_state_entity_ids` tracks it so the card updates live on sync changes. **Frontend** (`lock-codes-card.ts`, `shared-styles.ts`): new `_isProxyCode`/`_canReveal`/`_codeTitle` helpers; `_formatCode`/`_getCodeClass` rewritten; eye hidden for unrevealable slots; `.configured` (italic) and `.unreadable` (muted hollow) styles. Bundle rebuilt. **Tests**: backend `in_sync` serialization tests; frontend proxy/unknowable/reveal/tooltip tests against the real card […]
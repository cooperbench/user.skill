[DEVELOPER]: we still have an issue causing the circuit breaker to trip for matter locks on a slot. A user reported it (see the open issue) and I saw it myself

[AGENT]: I'll start with Phase 1: Root Cause Investigation. Let me gather evidence — the open issue, the circuit breaker code, and the matter provider. Let me do this in parallel.

[AGENT]: I'll get the issue list compactly and look at the resilience code in parallel.

[AGENT]: The relevant issue is **#1257**. Let me read it in full along with its comments.

[AGENT]: The issue body has lots of embedded log content. Let me extract just the body text and comments.

[AGENT]: Now I have the full picture of the issue. Let me explore the code paths. The key distinction: transient connectivity (`InvalidState: Not connected`) vs. genuine code rejection (`unknown(133)`), and how each feeds the slot-level circuit breaker.

[AGENT]: Let me read the core sync logic where the slot breaker records failures — the `_sync` method and surrounding handling.

[AGENT]: Let me find the matter provider and see how it classifies errors — particularly `InvalidState` and `unknown(133)`.

[AGENT]: The provider is `matter.py`. Let me read how it sets/clears credentials and classifies errors.

[AGENT]: The matter provider already has `_is_transient_credential_status` handling for `unknown(133)`. Let me read the set/clear credential path in full to see what still trips the breaker.

[AGENT]: Let me read the delete/clear path and the `_perform_sync` in base, plus how matter is a push provider.

[AGENT]: The matter provider routes connectivity errors to `LockDisconnected` thoroughly. Let me check what fixes already landed for #1257 and what's still in flight, to understand the "still" remaining bug.

[AGENT]: Fixes for #1257 already landed (#1258, #1260). The remaining symptom per jprasm's latest comment is two-fold: startup repairs still appear, AND recovery after a condition change takes "several minutes." Let me examine the coordinator's connectivity breaker / backoff and recovery timing, since that governs the delay.

[AGENT]: Now I see the recovery timing. The backoff escalates (60s→120s→240s — matching kyleberry's log), which explains the "several minutes" delay. But critically: a `SUSPENDED` slot returns early from the tick. Let me find how `SUSPENDED` ever recovers.

[AGENT]: Let me read the `request_sync_check` recovery logic (lines 565-610) precisely — this is the SUSPENDED→OUT_OF_SYNC transition path.

[AGENT]: The connectivity paths route to `LockDisconnected` (no slot-breaker charge). But `LockOperationFailed` **does** charge the slot breaker (sync.py:833). Let me examine the matter **user-creation** path, which raises `LockOperationFailed` on `MatterError` — a likely remaining gap.

[AGENT]: I found a strong candidate. Notice the asymmetry: the credential set/clear paths catch **both** `MatterError` and `MatterClientException` (matter.py:854, 969-973, 1040), but `_try_set_lock_user_with_fallbacks` (the user-creation path) catches only `ServiceValidationError`, `HomeAssistantError`, and `MatterError` — **not** `MatterClientException`. Let me confirm `MatterClientException`/`InvalidState` are a separate hierarchy from `MatterError`.

[AGENT]: Confirmed. `InvalidState`/`MatterClientException` inherits directly from `Exception` — it is **not** a `MatterError` nor a `HomeAssistantError`. So in `_try_set_lock_user_with_fallbacks` and the `async_set_user` CREATE handler, an `InvalidState: Not connected` from `set_lock_user` is caught by **none** of the except clauses and escapes to the generic handler. Let me audit every matter SDK call site to find all places missing `MatterClientException`.

[AGENT]: Now let me see which SDK functions sit behind the except clauses at 401/405, 479/483, 688-698, and 779/783 — all catch `HomeAssistantError` but **not** `MatterClientException`.

[AGENT]: The pattern is systemic. Let me read the last unpatched site (line ~779) and confirm it's a matter SDK call.

[AGENT]: Found it — `async_delete_user` → `clear_lock_user` (line 779/783) is the exact "clear usercode" path from the original log. Let me confirm I've found every matter SDK call site and check whether any are called entirely without a guard.

[AGENT]: Root cause **confirmed**. Let me lay out what I found before implementing. `★ Insight ─────────────────────────────────────` - **Three independent exception hierarchies collide here.** `matter_server` has `MatterError` (in `common.errors`) and `MatterClientException`/`InvalidState` (in `client.exceptions`), and HA has `HomeAssistantError`. I verified none of them subclass each other — `InvalidState.__mro__` is `[InvalidState, MatterClientException, Exception, ...]`. So a `try/except HomeAssistantError` silently lets `InvalidState: Not connected` fly past. - **The #1257 fix was applied surgically to only the two credential sites** (`_send_set_credential`, `async_delete_credential`), which now catch all three. But four *other* matter SDK call sites — `get_lock_users`, `get_lock_info`, `set_lock_user`, `clear_lock_user` — were never updated and still catch only `(ServiceValidationError, HomeAssistantError[, MatterError])`. - **Escape → generic suspend, which doesn't self-heal.** An uncaught `InvalidState` reaches `sync.py`'s catch-all `except Exception` → `_suspend_slot` with `_code_suspend_target` set. That suspension only clears when the desired target *changes* or the slot happens to be in-sync — *not* on mere reconnect — which is exactly jprasm's "takes several minutes / repairs appear" symptom. `─────────────────────────────────────────────────` The original log's `"Unexpected error during clear usercode … InvalidState: Not connected"` maps precisely to site #4 (`async_delete_user` → `clear_lock_user`). Let me set up tracking and find the test file to write a failing test first (TDD).

[AGENT]: There's already a test at line 335 for `HomeAssistantError` from `get_lock_users` → `LockDisconnected`. Let me look at how the existing MatterClientException test is written (line 10 import is used somewhere) and the test for set_lock_user / clear_lock_user error mapping.

[AGENT]: Let me read the existing tests for the four affected sites to write parallel failing tests. Let me look at the set_user create/disconnect, delete_user, get_capabilities, and get_lock_users tests.

[AGENT]: Now I understand all the patterns. Let me look at the `get_capabilities` and `_require`/import section to write parallel failing tests, and check imports like `UnknownError`.

[AGENT]: Let me check the test imports and the `get_lock_users` disconnect test (line 335) to confirm symbols available.

[AGENT]: `MatterClientException` and `UnknownError` are already imported. Let me read the `get_lock_users` disconnect test (335) and how `matter_lock`/usercodes are invoked, then write the four failing tests.

[AGENT]: Now I have all patterns. Let me write the four failing tests (TDD), placing each next to the matching existing test. First the `get_lock_users` and `get_capabilities` ones:

[AGENT]: Now the `set_lock_user` (CREATE fallback) and `clear_lock_user` (delete) tests:

[AGENT]: Now let me run the four new tests to confirm they fail (red phase of TDD):

[AGENT]: All 4 new tests fail as expected (red). The 3 that pass are the already-fixed credential paths. Now the green phase — fix all four sites in `matter.py`. `★ Insight ─────────────────────────────────────` - For sites 1, 2, 4 (reads + user delete) I'll mirror the credential-site pattern exactly — catch `(HomeAssistantError, MatterError, MatterClientException)` → `LockDisconnected`. This also closes a latent gap where a bare `MatterError` (not just the client exception) would have escaped these sites too. - Site 3 (`set_lock_user` cascade) is special: `MatterError` must keep its **fall-through** semantics (it's the charset-recovery signal that tries the next candidate name). Only `MatterClientException` joins the immediate-`LockDisconnected` clause, since a dead connection won't be fixed by a different name. `─────────────────────────────────────────────────`

[AGENT]: (Pyright import-resolution warnings are spurious — it's not pointed at the `.venv`.) Now the other three sites:

[AGENT]: (These pyright diagnostics are spurious/pre-existing — pyright isn't resolving the venv.) Now the final site, `async_delete_user`:

[AGENT]: Now let me run the four new tests (green phase) plus the full matter provider suite:

[AGENT]: All 157 matter tests pass. Per the project's "run the full suite before pushing" rule, let me run everything and verify the integration-level sync behavior wasn't disturbed.

[AGENT]: Full suite green: **1283 passed**, no regressions. Let me run the project's pre-commit checks (`prek`) on the changed files to confirm formatting/lint is clean.

[AGENT]: `ruff-format` auto-fixed formatting (the `no-commit-to-branch` failure is just because we're on `main` — expected, not committing yet). Let me re-run the affected tests to confirm the reformat didn't break anything.

[AGENT]: All green. Let me verify the final state of the four fixed sites in one view:

[AGENT]: The fix is complete and verified. Here's the summary. ## Root cause (confirmed) The Matter SDK exposes **three independent exception hierarchies** — I verified at runtime that `MatterClientException`/`InvalidState` (from `matter_server.client.exceptions`) is **not** a subclass of either `MatterError` *or* `HomeAssistantError`; its MRO is just `[InvalidState, MatterClientException, Exception]`. The #1257 fixes patched only the **two credential sites** (`_send_set_credential`, `async_delete_credential`) to catch all three. But **four other matter SDK call sites** still caught only `(ServiceValidationError, HomeAssistantError[, MatterError])`: | Site | SDK call | Reached during | |------|----------|----------------| | `_raw_lock_users` | `get_lock_users` | every read / sync | | `async_get_capabilities` | `get_lock_info` | setup | | `_try_set_lock_user_with_fallbacks` | `set_lock_user` | **set** sync (user CREATE) | | `async_delete_user` | `clear_lock_user` | **clear** sync | At startup, the matter client raises `InvalidState: Not connected` before its websocket connects. At these four sites it escaped every handler → reached `sync.py`'s catch-all `except Exception` → `_suspend_slot` with `_code_suspend_target` set. That suspension is the user-visible repair, and crucially it **does not self-heal on reconnect** (only on a target change or coincidental in-sync) — explaining jprasm's "takes several minutes" symptom. The original report's `"Unexpected error during clear usercode … InvalidState: Not connected"` is exactly site #4. ## The fix Route […]

[DEVELOPER]: create a PR but how do we ensure this doesn't just move the issue somewhere else as we continue to do?

[AGENT]: I'll create the focused fix PR now, then answer your prevention question concretely — because the answer is itself a second, deliberate change, not something to bolt onto this one. Let me grab the PR template and branch.

[AGENT]: Now let me create the branch, commit, and push:

[AGENT]: All pre-commit hooks passed. Now push and open the PR:

[AGENT]: **PR #1286** is open: https://github.com/raman325/lock_code_manager/pull/1286 ## On "how do we ensure this doesn't just move somewhere else" You're right to push on this — what we just did is the **sixth** site-by-site patch of the same defect (2 in #1258/#1260, 4 here). Whack-a-mole means the *shape* of the bug is structural, and patching instances will never converge. There are three distinct leak surfaces, and they need different kinds of guard: **1. New SDK call sites in `matter.py` (the immediate recurrence risk).** The root enabler is that translating raw SDK exceptions is a *convention each call site must remember*. Make it impossible to forget by funneling every SDK call through **one choke point**: ```python async def _invoke_sdk(self, operation: str, coro): """Single place that maps raw matter SDK exceptions to seam exceptions.""" try: return await coro except ServiceValidationError as err: raise LockOperationFailed(f"Matter {operation} rejected input for {self.lock.entity_id}: {err}") from err except (HomeAssistantError, MatterError, MatterClientException) as err: raise LockDisconnected(f"Matter {operation} failed for {self.lock.entity_id}: {err}") from err ``` The two genuinely-special sites stay bespoke (credential status mapping; the `set_lock_user` charset cascade). Everything else loses its hand-rolled `try/except`. After this, a guard test is *trivial and durable*: assert the raw SDK function names (`get_lock_users`, `set_lock_user`, […]

[DEVELOPER]: merged. ff main, clean up stale branches, then create the follow up PRs

[AGENT]: PR #1286 merged and main is fast-forwarded. The only `[gone]` branch is `fix/matter-client-exception-classification` (squash-merged, so I'll force-delete). I'll leave the `entire/*` session checkpoints and the active `feat/credential-length-capabilities` (not gone) alone.

[AGENT]: Cleanup done — main is at #1286, the merged branch is deleted, and I left the session-checkpoint and active feature branches untouched. Now the two follow-ups. Let me quickly scope the shared provider-test harness (needed for the cross-provider PR) before dispatching the work.

[AGENT]: There's an existing shared `ServiceProviderConnectionTests` harness — good, the cross-provider follow-up can extend it rather than be a standalone test-only PR. Here's my plan for the two follow-ups (both code+test, kept focused and isolated in worktrees): - **PR A — matter SDK exception-translation choke point + guard test.** Funnel the pure-pattern SDK calls through one `_invoke_sdk` helper and add an AST guard test so a *new* call site can't silently skip translation. - **PR B — generalize the shared provider connection-test harness** to assert that each provider's *native* (non-`HomeAssistantError`) transport exception surfaces as `LockDisconnected`, fixing any provider that leaks. This catches the bug class across **all** providers, not just matter. I'll dispatch both as parallel agents in isolated worktrees, each verifying (full suite + `prek`) before opening its PR.

[AGENT]: Both follow-up agents completed and opened PRs. Let me verify the PRs and that my main checkout is clean.

[AGENT]: All done. Here's where things stand. ## Completed - **Fast-forwarded `main`** to include the merged fix (#1286). - **Cleaned up** the merged `[gone]` branch (`fix/matter-client-exception-classification`). Left the `entire/*` session checkpoints and the active `feat/credential-length-capabilities` branch untouched. - **Opened the two follow-up PRs**, each developed in an isolated worktree and verified (full suite + `prek`) before pushing: | PR | Branch | What it does | |----|--------|--------------| | [#1287](https://github.com/raman325/lock_code_manager/pull/1287) | `refactor/matter-sdk-exception-choke-point` | Funnels the four pure-pattern matter SDK calls through a single `_invoke_sdk` choke point + an **AST guard test** that fails CI if a new SDK call site skips translation (or is added to the bespoke allowlist without thought). Suite: 1284 passed. | | [#1288](https://github.com/raman325/lock_code_manager/pull/1288) | `test/provider-native-transport-contract` | Generalizes the shared `ServiceProviderConnectionTests` harness into a `ProviderNativeTransportContractTests` mixin asserting each provider's *native* (non-`HomeAssistantError`) transport exception surfaces as `LockDisconnected`. Covers matter, zwave_js, zwave_js UC, akuvox, schlage; documents skips for zha/zigbee2mqtt/virtual. Suite: 1288 passed, 3 skipped. | ## Answering your original concern directly These two PRs attack the "does it just move elsewhere?" question from both ends: - **#1287 makes recurrence in matter structurally hard** — you can't add a matter SDK call that silently skips translation without the guard test failing. - […]

[DEVELOPER]: if this was a slot breaker issue, how was the code working after several minutes?

[AGENT]: That's a sharp catch — and it exposes a real nuance I glossed over. Let me verify the recovery mechanics against the code before answering, because my fix and the "recovers after several minutes" observation need to be reconciled honestly.

[AGENT]: Good question — it exposes something I glossed over, and the honest answer is that **it wasn't really the slot *breaker* counter that tripped**, which is exactly why the recovery looks paradoxical. Let me lay out the three distinct mechanisms, because they have very different recovery semantics. `★ Insight ─────────────────────────────────────` There are three "circuit-breaker-ish" things in this codebase, and they recover differently: - **Slot windowed breaker** (`MAX_SYNC_ATTEMPTS=3` / 5-min window) — *would* self-clear after 5 min… except it can't here (see below). - **`_code_suspend_target` suspend** (generic-exception path, the one #1286 fixed) — does **not** self-clear on time or on reconnect. - **Lock connectivity breaker** (backoff `60s → 120 → 240 … → 1800s`/30min) — self-clears on the next successful poll/push. `─────────────────────────────────────────────────` ## Why the suspend doesn't time out on its own Once a slot enters `SUSPENDED`, the periodic tick short-circuits immediately (`sync.py`): ```python if self._state in (IN_SYNC, SYNCING, SUSPENDED): return ``` So the slot breaker's nice 5-minute auto-clear is **moot** — we never re-enter the tick to re-check it. The *only* way out of `SUSPENDED` is the `request_sync_check` callback, and for a `_code_suspend_target` suspend that callback releases it on exactly one condition: ```python if (slot_state.active_state, slot_state.pin_state) != self._code_suspend_target or self.calculate_in_sync(slot_state): […]

[DEVELOPER]: yes, everything else is merged

[AGENT]: Let me first sync main and clean up the now-merged branches, then dig into the coordinator's recovery path to scope this properly.

[AGENT]: Both follow-up branches merged (release 4.1.4 cut). They're still checked out in the agent worktrees — let me remove those worktrees, then delete the branches.

[AGENT]: Cleanup complete — only the main worktree remains. Now let me investigate the recovery path. I need to understand the coordinator's backoff/reset and whether there's a reconnection signal to hook.

[AGENT]: Let me read the connectivity-check and backoff region, plus how matter handles reconnection (push subscription / connection check).

[AGENT]: There's a "connection transition handler" mentioned. Let me find how lock availability/reconnection is detected and the connection check.

[AGENT]: Let me read the connection check handler and how matter wires reconnection — this is the candidate hook for resetting backoff.

[AGENT]: Let me examine the base's reconnect handling and `async_internal_is_integration_connected` — to see if there's an existing transition hook to extend rather than adding new state tracking.

[AGENT]: Now I can see the existing reconnect machinery. There's already a `_handle_connection_transition` that kicks a refresh (→ resets backoff) on a False→True connection transition, polled every `connection_check_interval`. The key question: does matter's "is connected" signal actually reflect the **node** reconnecting, or just the matter-server config entry? Let me verify.

[AGENT]: Let me confirm matter's actual `connection_check_interval` and whether it overrides the connection signal.

[AGENT]: Now I have the mechanism nailed down. Let me confirm two details — matter's connection signal granularity and the rate-limit gate — before scoping.

[AGENT]: I've fully traced the recovery path. Here's the scoped finding. ## Confirmed cause of the "several minutes" The lock-level breaker's `unreachable` state is reset by exactly three things (`coordinator.py`): 1. A successful `async_get_usercodes` poll — but during backoff this only runs at the **escalating** `backoff_delay` (`60s → 120 → 240 → … → 1800s`, i.e. up to **30 min**). 2. A successful push update (`push_update` → `_reset_backoff`) — but a Matter *node* reconnect doesn't by itself emit a push. 3. `_handle_connection_transition` on a False→True transition kicking a refresh — **but this keys on the integration signal** (`async_is_integration_connected` = matter-server config entry `LOADED`). And there's the gap: I confirmed matter does **not** override `async_is_integration_connected`, so it stays `True` for the whole node-only outage (the matter-*server* never dropped; only the node was "Not connected"). So path #3 never fires for a node reconnect, and recovery falls back to path #1 — waiting out the backoff probe, up to 30 minutes. Notably, `_execute_rate_limited` already gates on **two separate signals** (`async_is_integration_connected` *and* `async_is_device_available`), so the codebase already distinguishes "server up" from "node reachable." The breaker recovery just isn't wired to the device-level signal — only the integration-level one. `★ Insight ─────────────────────────────────────` The bug is […]

[AGENT]: What would you like to clarify? Happy to go deeper on any of the three approaches — the subscription-churn concern, the recovery-latency tradeoffs, network/lock load during long outages, or how each interacts with the slot-level suspend recovery we discussed earlier. Or if there's additional context about how your Matter locks behave (how often nodes blip, acceptable recovery time after disarm), that would help me refine the options.

[DEVELOPER]: I thought we had an async_is_device_connected or something of that sort on the provider - when we have connectivity issues, whether they are at the network or device level, I think the backoff should be the same no?

[AGENT]: Let me check exactly what reachability methods exist on the provider, so I'm describing the real API and not misremembering it.

[AGENT]: You're right on both counts — let me correct my framing. First, the method name: it's **`async_is_device_available`** (device/node level) — there's no `async_is_device_connected`. The pair is: - `async_is_device_available` (`_base.py:805`) — can we reach this specific lock/node - `async_is_integration_connected` (`_base.py:864`) — is the integration's client/server up And your intuition is correct: **the backoff itself is already uniform.** Every `LockDisconnected` — whether it originated at the network/integration layer or the device/node layer — flows into the same `_lock_breaker` via `note_connectivity_failure` / `_apply_backoff` and escalates identically (`60 → 120 → … → 1800s`). There is no divergence on the *failure* side. So nothing to fix there. `★ Insight ─────────────────────────────────────` I conflated two things last turn. The asymmetry isn't in **backing off** (uniform) — it's in **detecting recovery**. The fast-recovery kick (`_handle_connection_transition`) only watches `async_is_integration_connected`. The device-level signal (`async_is_device_available`) feeds the *gate* in `_execute_rate_limited` but participates in recovery detection **nowhere**. So a device-level reconnect is never noticed quickly and falls through to the slow backoff probe. `─────────────────────────────────────────────────` So the fix that matches your mental model is: **make recovery detection uniform too.** `_execute_rate_limited` already treats "reachable" as `integration_connected AND device_available` — recovery should use that *same* combined signal. Then a network-level reconnect and a device-level […]

[DEVELOPER]: what's the cost of doing a push unsub/resub? It's safer

[DEVELOPER]: what's the cost of doing a push unsub/resub? It's safer in that it ensures we are never relying on a stale subscription. Unless there's ar easl cost, that seems worth having. Convince me otherwise

[AGENT]: Let me check what `subscribe_events` actually does in the matter client — local callback registration vs. a network/server round-trip — because the whole cost question hinges on that.

[AGENT]: Checked it — and you've convinced me. Here's the decisive evidence: `MatterClient.subscribe_events` is **purely local**: ```python self._subscribers.setdefault(key, []) self._subscribers[key].append(callback) def unsubscribe() -> None: self._subscribers[key].remove(callback) return unsubscribe ``` No `send_command`, no `await`, no network. The client holds **one** persistent websocket firehose to the matter-server and dispatches events to locally-registered callbacks by filter key. `subscribe_events`/unsubscribe are a dict append/remove. `★ Insight ─────────────────────────────────────` This dismantles my own "avoid churn" argument: - **Cost of unsub/resub ≈ zero** — two in-memory list ops, no I/O. - **"Stale subscription" can't arise from a node blip** — there's no server-side per-subscription state to go stale. Events stop only because the node isn't emitting; they resume automatically when it is. (A *server* websocket drop is a different thing, and the matter client + our integration-level reload path already handle that.) So re-subscribing on a node blip costs nothing and, as you say, is strictly safer as a defensive posture — it guarantees we never depend on assumptions about callback registration surviving whatever happened. `─────────────────────────────────────────────────` The only real effect of driving the transition off combined reachability is the **catch-up refresh** that fires on each device recovery (a genuine `get_lock_users` round-trip) — but that's *desirable* (it reconciles occupancy after the […]

[DEVELOPER]: yes, do it here

[AGENT]: On it. Let me gather the exact call sites, the base default for device availability, and existing tests before editing (TDD).

[AGENT]: Let me check the remaining caller (`__init__.py:873`) and the relevant tests to avoid breaking the gate's contract.

[AGENT]: Now I understand the full surface. The clean approach: rename `async_internal_is_integration_connected` → `async_internal_is_reachable` (combined = integration AND device), extract a `_note_reachability` helper so the transition fires from both the gate and the 30s check, and preserve distinct gate diagnostics. Let me check how reconnect/subscribe behavior is currently tested so I follow the pattern (TDD).

[AGENT]: There's a direct test for the transition. Let me read it (around 150–215) — that's my template for the new device-level test and what I need to update.

[AGENT]: The existing `test_connection_transition_resubscribes` is my template. Let me look at `MockLCMLockWithPush` to see `set_connected` so I can add a device-availability toggle for the new test.

[AGENT]: Now I have everything. Let me follow TDD: first add a device-availability toggle to the mock and write the failing test.

[AGENT]: Now the failing test, mirroring `test_connection_transition_resubscribes` but toggling device availability while integration stays connected:

[AGENT]: Now run the new test to confirm it fails (red):

[AGENT]: Red confirmed — device availability doesn't drive the transition yet. Now the production change in `_base.py`. First, the internal wrapper + extracting `_note_reachability`:

[AGENT]: Now update the gate in `_execute_rate_limited` to feed combined reachability to the transition while keeping distinct diagnostics:

[AGENT]: Now update the three remaining callers (the docstring at ~140, `__init__.py:873`, `coordinator.py:434`) and the two test references:

[AGENT]: Now apply the rename at the remaining call sites:

[AGENT]: Now the test references. Let me read the `__init__.py` line context and update `test_base.py:100` + the `test_init.py:658` comment:

[AGENT]: This is a docstring comment, and it patches `async_is_integration_connected` (the override I kept). Let me update the comment for accuracy:

[AGENT]: Now run the new test (green) plus the existing transition test:

[AGENT]: Both green. Now the full suite to check for regressions from the rename and the gate change:

[AGENT]: Full suite green (1290 passed). Let me confirm no stale references to the old name remain, then run pre-commit.

[AGENT]: No stale references. Now pre-commit:

[AGENT]: All hooks pass (the `no-commit-to-branch` failure just reminds me to branch). Let me create the branch, commit, push, and open the PR.

[AGENT]: Done — **PR #1289** is open: https://github.com/raman325/lock_code_manager/pull/1289 ## What shipped (implemented here on branch `fix/unified-reachability-backoff-recovery`) The recovery-latency fix we scoped, built TDD-style: **Production change** (`_base.py`, `coordinator.py`, `__init__.py`): - Renamed `async_internal_is_integration_connected` → **`async_internal_is_reachable`**, now computing `integration_connected AND device_available`. - Extracted `_note_reachability()` so the connection-transition handler is fed the **combined** signal from both the 30s connection check and the operation gate. - `_execute_rate_limited` keeps its distinct `"integration not connected"` / `"device not available"` diagnostics, but feeds the combined signal to the transition. - Net effect: a Matter **node** reconnect (server stayed up) now resets the backoff at the ~30s connection-check cadence instead of waiting out the escalating probe (up to 30 min). **Test** (`tests/common.py`, `test_base.py`): new `test_connection_transition_on_device_availability` — added a `set_device_available` toggle to the mock, asserted that a device-level drop/recovery (integration staying connected) now drives unsubscribe → resubscribe + refresh. Confirmed red before the change, green after. **Verification:** full suite **1290 passed, 3 skipped**; `ruff`/`ruff-format`/`mypy`/`pydocstyle`/`flake8` all clean. You're currently on the `fix/unified-reachability-backoff-recovery` branch locally (working tree clean). This closes out the four-part response to #1257: | PR | Scope | |----|-------| | #1286 (merged) | The actual exception-classification fix (4 missed sites) | | #1287 (merged) | Choke point + AST guard […]

[DEVELOPER]: why wont this action work: https://github.com/raman325/lock_code_manager/actions/runs/27973036902

[AGENT]: I'll pull the failing run's logs from GitHub to see why it failed.

[AGENT]: The failure is the "Upload zip to release" step: **`Input required and not supplied: tag`**. Let me look at the failed step log and the workflow definition.

[AGENT]: The upload step uses `tag: ${{ github.ref }}` and it came through empty. Let me look at the actual values in the log and the release context.

[AGENT]: Let me check whether prior Release runs succeeded (regression vs. always-broken) and look at the git history of this workflow.

[AGENT]: Found it. Here's the diagnosis. ## Why it failed The failing step is **Upload zip to release**, and the error `Input required and not supplied: tag` means the action's `tag:` input — `${{ github.ref }}` — evaluated to **empty**. The run list shows exactly why. Look at the head-ref column: ``` success 4.1.5 ... release (head = 4.1.5) ← tag FAILURE 4.1.4 ... release (head = main) ← branch, not the tag success 4.1.3 ... release (head = 4.1.3) ← tag success 4.1.2 ... release (head = 4.1.2) ← tag ``` Every **successful** release run was triggered with the ref pointing at the **tag**; the one that failed (4.1.4) was triggered with the ref pointing at **`main`**. The checkout in that run confirms it — it fetched the bare commit `bdd97d78` (main's HEAD), not `refs/tags/4.1.4`. So `github.ref` wasn't a tag ref, the `tag:` input came through empty, and `svenstaro/upload-release-action` aborted. `★ Insight ─────────────────────────────────────` `github.ref` is **not reliable for `release` events** — what it resolves to depends on how the release was published (it can come through as the target branch rather than the tag). The robust, event-correct source is `github.event.release.tag_name`, which is always the tag of the published release regardless […]
> DEVELOPER

look at issue 1298

> AGENT

I'll look at issue #1298 in the repository.

> AGENT

Let me look at the relevant code to understand the issue fully.

> AGENT

Now let me look at the `_uc_fallback_capabilities` method and the refresh helper.

> AGENT

Let me find the specific fallback methods referenced in the issue.

> AGENT

I've read the issue and the relevant code. Here's my analysis. ## What issue #1298 is about A Schlage BE469ZP (Z-Wave User Code CC-only lock, no U3C) fails setup with a **misleading error**: ``` lock.front_door_lock: lock does not advertise PIN credential support ``` The lock *does* support PINs. The real problem is that the node advertises User Code CC (CC 99) but its **slot values were never populated in the value DB** — the interview completed while the battery lock was asleep. So the code can't tell "no PIN support" apart from "PIN support, values missing." ## Tracing the failure path The routing logic at `zwave_js.py:245-315` does this: 1. `async_get_credential_capabilities()` returns `pin["num_slots"] == 0` (degenerate — the #1251 zero-slot variant). 2. Falls through to `_uc_fallback_capabilities()` at line 307. 3. In `_zwave_js_uc.py:185`, that method finds: - `_node_supports_user_code_cc()` → `True` (CC 99 is advertised) - `len(get_usercodes(self.node))` → `0` (no `*-99-*` values in the DB) 4. `_zwave_js_uc.py:207-209` — `num_slots == 0`, so it returns `None` and clears `_uc_fallback`. 5. Back at `zwave_js.py:307-314`, `None` means "build empty capabilities," which the base `async_setup_internal` rejects with the generic "does not advertise PIN credential support." `★ Insight ─────────────────────────────────────` - **The bug is a conflated condition.** `_uc_fallback_capabilities()` has […]
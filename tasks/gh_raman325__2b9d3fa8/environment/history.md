> DEVELOPER

see kyleberry's comments in 1257 and 1268. What's going on?

> AGENT

I'll look at kyleberry's comments in #1257 and #1268 to understand what's going on.

> AGENT

Both are issues about Matter locks. Let me read both in full, including all comments.

> AGENT

Let me read the full content of both issues.

> AGENT

Now let me read issue 1268 in full.

> AGENT

I have the full picture of both issues now. Let me dig into the actual code paths Kyle cites to understand what's really happening. Let me look at the coordinator and the Matter provider availability check.

> AGENT

This is very revealing. The coordinator's `async_get_usercodes` (lines 370-385) confirms Kyle's "Bug 2" mechanism. Now let me examine the Matter provider's availability check (Bug 1) and the `_execute_rate_limited` gate.

> AGENT

Now the Matter provider's availability check — the "Matter client or node unavailable" message and `async_is_device_available`.

> AGENT

Now the `async_is_device_available` for Matter (line 919) — the heart of Bug 1:

> AGENT

Let me check how `device_entry` is resolved (a stale/None capture would explain the persistent false negative) and the base `async_internal_is_integration_connected`.

> AGENT

Let me check Matter's `async_is_integration_connected` override and the `device_entry` property.

> AGENT

Let me check the Matter helper imports — specifically `get_lock_info` vs `get_lock_users` (Kyle says the latter works) and `get_node_from_device_entry`.

> AGENT

Let me confirm the backoff ceiling and check whether there's already an open PR addressing this.

> AGENT

I've now traced both code paths Kyle cites. Here's what's going on. ## The two issues **#1257** (jprasm, closed) — Matter slots disabled after restart due to startup credential sync failures. That got fixed (#1258/#1260) and jprasm confirmed it. Then **kyleberry showed up in the comments** saying he has a similar-but-not-identical problem, dumped diagnostics, and — to his credit — opened **#1268** as a clean standalone issue instead of hijacking the closed one. **#1268** (kyleberry, open) is the real report. He's on LCM 4.1.0, an Ultraloq Bolt over Matter, in a Docker Compose setup where HA and `python-matter-server` restart *together*. His Z-Wave lock in the same config entry rides through the restart fine; only the Matter lock gets stuck. And critically: `matter.get_lock_users` returns all his users at any point, the lock entity is `locked` and controllable — yet LCM's coordinator reports `lock_unreachable: true` and all slots go `unavailable`. He diagnosed **two compounding bugs**, and after reading the code, **he's essentially right on both.** ## Bug 2 — confirmed, and it's in our code This is the clearest finding. `domain/coordinator.py:370-385`: ```python async def async_get_usercodes(self): try: data = await self._lock.async_internal_get_usercodes() except LockCodeManagerError as err: self._apply_backoff() if not self.last_update_success: return {} # <-- […]
> DEVELOPER

look at issue 1298

> AGENT

I'll look at issue #1298 in the repository.

> TOOL

tool_use Bash
id: toolu_01EVZPiWVVLxKRv17w9TxUMx
```json
{
  "command": "gh issue view 1298",
  "description": "View GitHub issue 1298"
}
```

> TOOL

tool_result
id: toolu_01EVZPiWVVLxKRv17w9TxUMx
```
title:	[ISSUE] _uc_fallback_capabilities gives up silently when User Code CC values are missing from the   DB (incomplete interview) → misleading "does not advertise PIN credential support"
state:	OPEN
author:	brianschmitt (Brian Schmitt)
labels:	bug
comments:	0
assignees:	
projects:	
milestone:	
issue-type:	
parent:	
sub-issues:	
sub-issues-completed:	
blocked-by:	
blocking:	
number:	1298
--
### What happened?

On a Z-Wave UC-only lock whose User Code CC is advertised but has no slot values in the node value
  DB (e.g. an interview that completed while the lock was asleep), setup fails with:

  lock.front_door_lock: lock does not advertise PIN credential support

  This message is misleading: the lock does support PIN credentials. The real condition is "User
  Code CC values are missing / interview incomplete." _uc_fallback_capabilities() swallows this and
  concludes "no PIN support" instead of refreshing the CC or surfacing an actionable error.

  Environment

  - LCM: 4.1.5
  - Home Assistant: 2026.6.4 (HAOS 18.0)
  - Z-Wave JS UI add-on: 7.4.0; zwave-js driver 15.24.2, server 3.9.0; controller SDK 7.24.3
  - Lock: Allegion / Schlage BE469ZP (Touchscreen Deadbolt), node 2, S2-secured, interview stage
  Complete
  - Command classes include User Code (99) v1, Door Lock (98) v2; no User Credential CC (U3C)

  What happens

  In the degenerate-capabilities state, zwave_js.get_credential_capabilities […]

> AGENT

Let me look at the relevant code to understand the issue fully.

> TOOL

tool_use Bash
id: toolu_016qiRgDprg7R6QjWbuWkaLt
```json
{
  "command": "grep -n \"_uc_fallback_capabilities\\|_async_refresh_usercode_cache\\|_node_supports_user_code_cc\\|async_get_capabilities\\|_uc_fallback\" custom_components/lock_code_manager/providers/zwave_js.py",
  "description": "Find relevant symbols in zwave_js provider"
}
```

> TOOL

tool_result
id: toolu_016qiRgDprg7R6QjWbuWkaLt
```
202:        unusable for this lock (see ``async_get_capabilities``), users
207:        if await self._async_uc_fallback_active():
245:    async def async_get_capabilities(self) -> LockCapabilities:
287:            self._uc_fallback = False
307:        if uc_caps := self._uc_fallback_capabilities():
309:        self._uc_fallback = False
462:        if await self._async_uc_fallback_active():
512:        if await self._async_uc_fallback_active():
572:        if self._uc_fallback is not False:
574:        if not self._uc_fallback:
713:        if await self._async_uc_fallback_active():
714:            await self._async_refresh_usercode_cache()
```

> TOOL

tool_use Read
id: toolu_0193fFPbwAAQh8UxGSBkgcFY
```json
{
  "file_path": "/Users/raman/projects/lock_code_manager/custom_components/lock_code_manager/providers/zwave_js.py",
  "offset": 245,
  "limit": 120
}
```

> TOOL

tool_result
id: toolu_0193fFPbwAAQh8UxGSBkgcFY
```
245	    async def async_get_capabilities(self) -> LockCapabilities:
246	        """
247	        Report the lock's user/credential capabilities.
248	
249	        Routes the lock based on whether the unified API can express its PIN
250	        capabilities:
251	
252	        - **Usable PIN capabilities reported** (``num_slots > 0``) -> the
253	          unified ``access_control`` API. This is the common path for both
254	          U3C locks and healthy User Code CC-only locks. Masked-code locks
255	          stay correct here via the universal read projection (``_pin_state``
256	          maps a withheld code to ``unreadable``) and tolerant write handling
257	          (a driver ``ERROR_UNKNOWN`` from the masked read-back verification
258	          is treated as a completed set in ``async_set_credential``, not a
259	          rejection) -- see issue #1251.
260	        - **Degenerate capabilities** (PIN missing or ``num_slots == 0``) ->
261	          the legacy User Code CC fallback (slot-only), which addresses slots
262	          directly because the unified API can't even express them. Only the
263	          zero-slot variant needs this; a node with no User Code CC at all has
264	          no PIN support LCM can manage.
265	
266	        Note: this method does NOT route by command class -- a User Code
267	        CC-only lock with healthy capabilities uses the unified path, relying
268	        on […]

> AGENT

Now let me look at the `_uc_fallback_capabilities` method and the refresh helper.

> TOOL

tool_use Read
id: toolu_019ETrYjmjNiJnqMopXdjp7N
```json
{
  "file_path": "/Users/raman/projects/lock_code_manager/custom_components/lock_code_manager/providers/zwave_js.py",
  "offset": 540,
  "limit": 180
}
```

> TOOL

tool_result
id: toolu_019ETrYjmjNiJnqMopXdjp7N
```
540	            return False, "Z-Wave JS client not ready"
541	
542	        if not client.connected:
543	            return False, "Z-Wave JS client not connected"
544	
545	        if client.driver is None:
546	            return False, "Z-Wave JS driver not ready"
547	
548	        return True, ""
549	
550	    @callback
551	    def setup_push_subscription(self) -> None:
552	        """
553	        Subscribe to credential change events.
554	
555	        In unified mode the driver emits ``credential added/modified/
556	        deleted`` node events. In UC-fallback mode those events never
557	        fire (the driver only emits them from its own unified API
558	        methods, which the fallback bypasses), so we subscribe to raw
559	        ``value updated`` events for the User Code CC values instead.
560	        When the mode is not yet known (capability probe hasn't run),
561	        subscribe to both; the handlers are self-filtering and pushes
562	        are idempotent.
563	        """
564	        if self._push_unsubs:
565	            return
566	
567	        ready, reason = self._get_client_state()
568	        if not ready:
569	            raise LockDisconnected(reason)
570	
571	        subscriptions: list[tuple[str, Callable[[dict[str, Any]], None]]] = []
572	        if self._uc_fallback is not False:
573	            subscriptions.append(("value updated", self._on_uc_value_updated))
574	        if not self._uc_fallback:
575	            subscriptions.extend(
576	                (
577	                    ("credential added", self._on_credential_changed),
578	                    ("credential modified", self._on_credential_changed),
579	                    ("credential deleted", self._on_credential_deleted),
580	                ) […]

> AGENT

Let me find the specific fallback methods referenced in the issue.

> TOOL

tool_use Bash
id: toolu_01JSHbvzkMkE412Qc9Fw9Ggc
```json
{
  "command": "grep -n \"def _uc_fallback_capabilities\\|def _async_refresh_usercode_cache\\|def _node_supports_user_code_cc\\|def _async_uc_fallback_active\\|def async_get_users\" custom_components/lock_code_manager/providers/zwave_js.py",
  "description": "Find method definitions"
}
```

> TOOL

tool_result
id: toolu_01JSHbvzkMkE412Qc9Fw9Ggc
```
185:    async def async_get_users(self) -> list[User]:
```

> TOOL

tool_use Bash
id: toolu_017c3tP3QGSo26ZYpwxBpqo8
```json
{
  "command": "grep -rn \"def _uc_fallback_capabilities\\|def _async_refresh_usercode_cache\\|def _node_supports_user_code_cc\\|def _async_uc_fallback_active\" custom_components/lock_code_manager/providers/",
  "description": "Find methods across providers"
}
```

> TOOL

tool_result
id: toolu_017c3tP3QGSo26ZYpwxBpqo8
```
custom_components/lock_code_manager/providers/_zwave_js_uc.py:147:    def _node_supports_user_code_cc(self) -> bool:
custom_components/lock_code_manager/providers/_zwave_js_uc.py:172:    async def _async_uc_fallback_active(self) -> bool:
custom_components/lock_code_manager/providers/_zwave_js_uc.py:185:    def _uc_fallback_capabilities(self) -> LockCapabilities | None:
custom_components/lock_code_manager/providers/_zwave_js_uc.py:313:    async def _async_refresh_usercode_cache(self) -> None:
```

> TOOL

tool_use Read
id: toolu_01TRGJpENKrAH6DFWZbu5gYL
```json
{
  "file_path": "/Users/raman/projects/lock_code_manager/custom_components/lock_code_manager/providers/_zwave_js_uc.py",
  "offset": 130,
  "limit": 230
}
```

> TOOL

tool_result
id: toolu_01TRGJpENKrAH6DFWZbu5gYL
```
130	    _set_in_progress_code_slot: int | None = field(init=False, default=None)
131	
132	    @property
133	    def node(self) -> Node:
134	        """Return the Z-Wave JS node; the concrete provider supplies this."""
135	        raise NotImplementedError
136	
137	    def _pin_state(self, data: str | bytes | None) -> SlotCredential:
138	        """
139	        Project raw credential data to a SlotCredential.
140	
141	        Universal masked/withheld-aware projection, implemented by the
142	        concrete provider (``ZWaveJSLock._pin_state``) and reused here so
143	        the UC fallback's read path matches the unified path exactly.
144	        """
145	        raise NotImplementedError
146	
147	    def _node_supports_user_code_cc(self) -> bool:
148	        """Return whether the node's endpoint 0 advertises User Code CC."""
149	        return any(cc.id == CommandClass.USER_CODE for cc in self.node.command_classes)
150	
151	    @functools.cached_property
152	    def _usercode_cc_version(self) -> int:
153	        """Return the User Code CC version supported by this node."""
154	        version = next(
155	            (
156	                cc.version
157	                for cc in self.node.command_classes
158	                if cc.id == CommandClass.USER_CODE
159	            ),
160	            0,
161	        )
162	        if version == 0:
163	            _LOGGER.warning(
164	                "Lock %s: User Code CC not found on node %s. This may "
165	                "indicate an incomplete interview. Defaulting to V1 behavior",
166	                self.lock.entity_id,
167	                self.node.node_id,
168	            )
169	            return 1
170	        return version
171 […]

> AGENT

I've read the issue and the relevant code. Here's my analysis.

## What issue #1298 is about

A Schlage BE469ZP (Z-Wave User Code CC-only lock, no U3C) fails setup with a **misleading error**:

```
lock.front_door_lock: lock does not advertise PIN credential support
```

The lock *does* support PINs. The real problem is that the node advertises User Code CC (CC 99) but its **slot values were never populated in the value DB** — the interview completed while the battery lock was asleep. So the code can't tell "no PIN support" apart from "PIN support, values missing."

## Tracing the failure path

The routing logic at `zwave_js.py:245-315` does this:

1. `async_get_credential_capabilities()` returns `pin["num_slots"] == 0` (degenerate — the #1251 zero-slot variant).
2. Falls through to `_uc_fallback_capabilities()` at line 307.
3. In `_zwave_js_uc.py:185`, that method finds:
   - `_node_supports_user_code_cc()` → `True` (CC 99 is advertised)
   - `len(get_usercodes(self.node))` → `0` (no `*-99-*` values in the DB)
4. `_zwave_js_uc.py:207-209` — `num_slots == 0`, so it returns `None` and clears `_uc_fallback`.
5. Back at `zwave_js.py:307-314`, `None` means "build empty capabilities," which the base `async_setup_internal` rejects with the generic "does not advertise PIN credential support."

`★ Insight ─────────────────────────────────────`
- **The bug is a conflated condition.** `_uc_fallback_capabilities()` has […]

> TOOL

tool_use AskUserQuestion
id: toolu_01WrHTkLbmoEyNfTFS4SGdbz
```json
{
  "questions": [
    {
      "question": "When User Code CC is advertised but the value DB stays empty even after a refresh, how should the capability probe behave?",
      "header": "Empty-after-refresh",
      "multiSelect": false,
      "options": [
        {
          "label": "Raise actionable error",
          "description": "Refuse setup with a clear 'interview incomplete — re-interview then reload' message. Matches the reporter's suggestion; fails loud, no silent 'no PIN support'. Aligns with your fail-loud-on-unencodable-identifier principle."
        },
        {
          "label": "Log + return None (current behavior)",
          "description": "Keep returning None so the base raises the generic error, but add a distinct WARNING log naming 'values missing / interview incomplete'. Less disruptive; setup still fails but with a breadcrumb in logs."
        }
      ]
    },
    {
      "question": "Should I implement the fix now, or just leave the analysis?",
      "header": "Next step",
      "multiSelect": false,
      "options": [
        {
          "label": "Just the analysis for now",
          "description": "Stop here. You'll decide on implementation later or assign it elsewhere."
        },
        {
          "label": "Implement the fix",
          "description": "Write the async refresh-and-retry change in _uc_fallback_capabilities + its call site, with a test reproducing the empty-value-DB case. I'll use TDD."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01WrHTkLbmoEyNfTFS4SGdbz
```
Your questions have been answered: "When User Code CC is advertised but the value DB stays empty even after a refresh, how should the capability probe behave?"="we should do a cc refresh at that point no?", "Should I implement the fix now, or just leave the analysis?"="Implement the fix". You can now continue with these answers in mind.
```
> DEVELOPER

see kyleberry's comments in 1257 and 1268. What's going on?

> AGENT

I'll look at kyleberry's comments in #1257 and #1268 to understand what's going on.

> TOOL

tool_use Bash
id: toolu_01Ws9aH6V6PqH93cotJfbfBA
```json
{
  "command": "gh pr view 1257 --json title,state,author,url 2>/dev/null || echo \"1257 not a PR\"; echo \"---\"; gh issue view 1257 --json title,state,author,url 2>/dev/null || echo \"1257 not an issue\"",
  "description": "Check if 1257 is PR or issue"
}
```

> TOOL

tool_use Bash
id: toolu_011huuqZ923VjDrjgTB82TkM
```json
{
  "command": "gh pr view 1268 --json title,state,author,url 2>/dev/null || echo \"1268 not a PR\"; echo \"---\"; gh issue view 1268 --json title,state,author,url 2>/dev/null || echo \"1268 not an issue\"",
  "description": "Check if 1268 is PR or issue"
}
```

> TOOL

tool_result
id: toolu_01Ws9aH6V6PqH93cotJfbfBA
```
1257 not a PR
---
{"author":{"id":"MDQ6VXNlcjgwMjI5OTkz","is_bot":false,"login":"jprasm","name":"jprasm"},"state":"CLOSED","title":"[ISSUE] Matter lock slots disabled after HA restart due to startup credential sync failures","url":"https://github.com/raman325/lock_code_manager/issues/1257"}
```

> TOOL

tool_result
id: toolu_011huuqZ923VjDrjgTB82TkM
```
1268 not a PR
---
{"author":{"id":"MDQ6VXNlcjQ2ODEyNzE=","is_bot":false,"login":"kyleberry","name":"Kyle Berry"},"state":"OPEN","title":"[ISSUE] Matter lock coordinator permanently stuck after stack restart: availability check false negative causes unrecoverable short-circuit","url":"https://github.com/raman325/lock_code_manager/issues/1268"}
```

> AGENT

Both are issues about Matter locks. Let me read both in full, including all comments.

> TOOL

tool_use Bash
id: toolu_01NaWUzCVWN5BMZoVkwwhpXJ
```json
{
  "command": "gh issue view 1257 --comments",
  "description": "Read issue 1257 with comments"
}
```

> TOOL

tool_use Bash
id: toolu_019kJHzZi2tjrTfge6upNT2r
```json
{
  "command": "gh issue view 1268 --comments",
  "description": "Read issue 1268 with comments"
}
```

> TOOL

tool_result
id: toolu_01NaWUzCVWN5BMZoVkwwhpXJ
```
<persisted-output>
Output too large (58.7KB). Full output saved to: /home/<USER>/.claude/projects/-Users-raman-projects-lock-code-manager/767d0b4b-61ce-40e4-a26a-8aa50590fb1c/tool-results/b0d35tgiv.txt

Preview (first 2KB):
author:	raman325
association:	owner
edited:	true
status:	none
--
please let me know if the latest release resolved the issue
--
author:	jprasm
association:	none
edited:	false
status:	none
--
I believe this is now solved. Thank you!
--
author:	jprasm
association:	none
edited:	false
status:	none
--
@raman325 , the issue is resolved but you do _see_ repairs on startup - which resolve on their own after about a minute. So not a big deal.

Can they occur in the background without the user seeing them? I guess that's for you to decide:

<img width="614" height="572" alt="Image" src="https://github.com/user-attachments/assets/82ceb906-a997-4352-9e04-cba61bfed273" />
--
author:	raman325
association:	owner
edited:	false
status:	none
--
That shouldn't happen... thanks for reporting!
--
author:	raman325
association:	owner
edited:	false
status:	none
--
@jprasm this issue should be resolvedb but feel free to comment here or open a new issue if you still run into it and/or notice something else
--
author:	kyleberry
association:	none
edited:	false
status:	none
--
Hello @raman325, I'm having the same (similar?) issue, LCM reports the matter lock as unreachable but `matter.get_lock_users` works fine:

Debug: […]

> TOOL

tool_result
id: toolu_019kJHzZi2tjrTfge6upNT2r
```
(Bash completed with no output)
```

> AGENT

Let me read the full content of both issues.

> TOOL

tool_use Read
id: toolu_017YuhotdVT4S5BFzTqEWgU7
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-raman-projects-lock-code-manager/767d0b4b-61ce-40e4-a26a-8aa50590fb1c/tool-results/b0d35tgiv.txt"
}
```

> TOOL

tool_result
id: toolu_017YuhotdVT4S5BFzTqEWgU7
```
1	author:	raman325
2	association:	owner
3	edited:	true
4	status:	none
5	--
6	please let me know if the latest release resolved the issue
7	--
8	author:	jprasm
9	association:	none
10	edited:	false
11	status:	none
12	--
13	I believe this is now solved. Thank you!
14	--
15	author:	jprasm
16	association:	none
17	edited:	false
18	status:	none
19	--
20	@raman325 , the issue is resolved but you do _see_ repairs on startup - which resolve on their own after about a minute. So not a big deal.
21	
22	Can they occur in the background without the user seeing them? I guess that's for you to decide:
23	
24	<img width="614" height="572" alt="Image" src="https://github.com/user-attachments/assets/82ceb906-a997-4352-9e04-cba61bfed273" />
25	--
26	author:	raman325
27	association:	owner
28	edited:	false
29	status:	none
30	--
31	That shouldn't happen... thanks for reporting!
32	--
33	author:	raman325
34	association:	owner
35	edited:	false
36	status:	none
37	--
38	@jprasm this issue should be resolvedb but feel free to comment here or open a new issue if you still run into it and/or notice something else
39	--
40	author:	kyleberry […]

> TOOL

tool_use Bash
id: toolu_01PsW8BM6Z5SrnVy4nGX6a7E
```json
{
  "command": "gh issue view 1268 --comments > /tmp/issue1268.txt 2>&1; wc -c /tmp/issue1268.txt",
  "description": "Save issue 1268 to file"
}
```

> TOOL

tool_result
id: toolu_01PsW8BM6Z5SrnVy4nGX6a7E
```
       0 /tmp/issue1268.txt
```

> AGENT

Now let me read issue 1268 in full.

> TOOL

tool_use Bash
id: toolu_01PJ3NDdYZLHRUp3Bdcm7LUk
```json
{
  "command": "gh issue view 1268 --comments 2>&1 | head -300",
  "description": "Read issue 1268 body and comments"
}
```

> TOOL

tool_result
id: toolu_01PJ3NDdYZLHRUp3Bdcm7LUk
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01AbempzoGQcV7JibqjYfrA7
```json
{
  "command": "gh issue view 1268 --json title,body,comments --jq '.title, \"=== BODY ===\", .body, \"=== COMMENTS ===\", (.comments[] | .author.login + \": \" + .body)' > /tmp/i1268.txt 2>&1; wc -l /tmp/i1268.txt; echo \"---FIRST CHECK---\"; gh issue view 1268 --json title 2>&1",
  "description": "Fetch issue 1268 as JSON"
}
```

> TOOL

tool_result
id: toolu_01AbempzoGQcV7JibqjYfrA7
```
     118 /tmp/i1268.txt
---FIRST CHECK---
{"title":"[ISSUE] Matter lock coordinator permanently stuck after stack restart: availability check false negative causes unrecoverable short-circuit"}
```

> TOOL

tool_use Read
id: toolu_01QsQGgaCDb2Nm3ga1zzwJhh
```json
{
  "file_path": "/tmp/i1268.txt"
}
```

> TOOL

tool_result
id: toolu_01QsQGgaCDb2Nm3ga1zzwJhh
```
1	[ISSUE] Matter lock coordinator permanently stuck after stack restart: availability check false negative causes unrecoverable short-circuit
2	=== BODY ===
3	### What happened?
4	
5	After a full Docker Compose stack restart (Home Assistant + core_matter_server restarting together), LCM's coordinator for a Matter lock permanently enters a failed state and never self-recovers, even though the lock entity is fully operational — state shows locked, lock/unlock works from the UI, and matter.get_lock_users returns all expected users.
6	
7	Two bugs compound each other:
8	
9	Bug 1 — Availability check uses internal Matter client/node state instead of entity availability
10	
11	LCM's Matter provider checks something internal that returns unavailable (Matter client or node unavailable for lock.back_door) even though the lock entity and all HA service calls work. This appears to be a timing issue on joint restart where HA's entity availability reconciles before the underlying Matter client/node property does.
12	
13	Bug 2 — After consecutive failures, coordinator short-circuits to empty data instead of retrying
14	
15	After N consecutive LockDisconnected failures the coordinator stops trying to read the lock. It returns {} in 0.000 seconds as success: True, logs "Fetching data recovered", then […]

> AGENT

I have the full picture of both issues now. Let me dig into the actual code paths Kyle cites to understand what's really happening. Let me look at the coordinator and the Matter provider availability check.

> TOOL

tool_use Read
id: toolu_019YUg54d3oKT2HWTYyPzAiX
```json
{
  "file_path": "/home/<USER>/projects/lock_code_manager/custom_components/lock_code_manager/domain/coordinator.py"
}
```

> TOOL

tool_result
id: toolu_019YUg54d3oKT2HWTYyPzAiX
```
1	"""
2	Manages the slot->code mapping for a single lock.
3	
4	Stores ALL slots (managed and unmanaged). See ARCHITECTURE.md for the full data flow.
5	"""
6	
7	from __future__ import annotations
8	
9	from collections.abc import Callable
10	from datetime import datetime, timedelta
11	import logging
12	from typing import TYPE_CHECKING, Any
13	
14	from homeassistant.const import CONF_ENABLED, CONF_PIN
15	from homeassistant.core import HomeAssistant, callback
16	from homeassistant.helpers.event import async_track_time_interval
17	from homeassistant.helpers.issue_registry import (
18	    IssueSeverity,
19	    async_create_issue,
20	    async_delete_issue,
21	)
22	from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
23	
24	from ..const import (
25	    BACKOFF_FAILURE_THRESHOLD,
26	    BACKOFF_INITIAL_SECONDS,
27	    BACKOFF_MAX_SECONDS,
28	    DOMAIN,
29	    POLL_FAILURE_ALERT_THRESHOLD,
30	)
31	from .exceptions import LockCodeManagerError
32	from .models import SlotCredential
33	from .queries import get_entry_config
34	from .resilience import CircuitBreaker
35	
36	if TYPE_CHECKING:
37	    from ..providers import BaseLock
38	
39	_LOGGER = logging.getLogger(__name__)
40	
41	
42	class LockUsercodeUpdateCoordinator(DataUpdateCoordinator[dict[int, SlotCredential]]):
43	    """Class to manage usercode updates."""
44	
45	    def __init__(self, hass: HomeAssistant, lock: BaseLock, config_entry: Any) -> None:
46	        """Initialize the usercode update coordinator."""
47	        self._lock = lock
48	        self._drift_unsub: Callable[[], None] | None = None
49	        self._connection_unsub: Callable[[], None] | None = None
50	        # […]

> AGENT

This is very revealing. The coordinator's `async_get_usercodes` (lines 370-385) confirms Kyle's "Bug 2" mechanism. Now let me examine the Matter provider's availability check (Bug 1) and the `_execute_rate_limited` gate.

> TOOL

tool_use Read
id: toolu_0184qYPC6B4nN7wtGZ4FhzTr
```json
{
  "file_path": "/home/<USER>/projects/lock_code_manager/custom_components/lock_code_manager/providers/_base.py",
  "offset": 200,
  "limit": 120
}
```

> TOOL

tool_result
id: toolu_0184qYPC6B4nN7wtGZ4FhzTr
```
200	        default=None, init=False, repr=False
201	    )
202	    _last_operation_time: float = field(default=0.0, init=False)
203	    _min_operation_delay: float = field(default=MIN_OPERATION_DELAY, init=False)
204	    _last_connection_up: bool | None = field(default=None, init=False)
205	    _config_entry_state_unsub: Callable[[], None] | None = field(
206	        default=None, init=False
207	    )
208	    _last_entry_state: ConfigEntryState | None = field(default=None, init=False)
209	    _setup_complete: asyncio.Event = field(default_factory=asyncio.Event, init=False)
210	    _setup_succeeded: bool = field(default=False, init=False)
211	    _setup_running: bool = field(default=False, init=False)
212	    _lcm_config_entry: ConfigEntry | None = field(default=None, init=False)
213	    _rejected_code_slots: set[int] = field(default_factory=set, init=False)
214	    # Slots with an outstanding optimistic (ambiguous-but-treated-as-completed)
215	    # write awaiting confirmation, mapped to (believed_pin, monotonic_deadline).
216	    # A confirmation -- a push event or a hard-refresh read observing the slot
217	    # present -- clears the entry and re-pushes the believed value as verified;
218	    # if none arrives before the deadline, the sync layer re-syncs. See the
219	    # Phase 2 push-as-commit spec.
220	    _pending_writes: dict[int, tuple[str, float]] = field(
221	        default_factory=dict, init=False
222	    )
223	    # Reconnect task spawned by the config-entry state listener when the lock
224	    # integration transitions to LOADED. Tracked so async_unload can cancel it
225	    # before teardown -- otherwise a late reconnect can call
226	    # coordinator.async_request_refresh() […]

> AGENT

Now the Matter provider's availability check — the "Matter client or node unavailable" message and `async_is_device_available`.

> TOOL

tool_use Bash
id: toolu_01CFmYjZ8SXyeFRgFKSrgnkb
```json
{
  "command": "grep -rn \"async_is_device_available\\|Matter client or node unavailable\\|availability check failed\\|async_internal_is_integration_connected\" custom_components/lock_code_manager/providers/ | head -40",
  "description": "Find availability check implementations"
}
```

> TOOL

tool_result
id: toolu_01CFmYjZ8SXyeFRgFKSrgnkb
```
custom_components/lock_code_manager/providers/_base.py:140:       - Periodic async_internal_is_integration_connected() at connection_check_interval
custom_components/lock_code_manager/providers/_base.py:251:        if not await self.async_internal_is_integration_connected():
custom_components/lock_code_manager/providers/_base.py:256:        if not await self.async_is_device_available():
custom_components/lock_code_manager/providers/_base.py:799:    async def async_is_device_available(self) -> bool:
custom_components/lock_code_manager/providers/_base.py:875:    async def async_internal_is_integration_connected(self) -> bool:
custom_components/lock_code_manager/providers/zigbee2mqtt.py:180:    async def async_is_device_available(self) -> bool:
custom_components/lock_code_manager/providers/zigbee2mqtt.py:565:        if not await self.async_is_device_available():
custom_components/lock_code_manager/providers/zwave_js.py:694:    async def async_is_device_available(self) -> bool:
custom_components/lock_code_manager/providers/schlage.py:130:    async def async_is_device_available(self) -> bool:
custom_components/lock_code_manager/providers/schlage.py:136:                "Lock %s: availability check failed: %s",
custom_components/lock_code_manager/providers/matter.py:248:                f"Matter client or node unavailable for {self.lock.entity_id}"
custom_components/lock_code_manager/providers/matter.py:919:    async def async_is_device_available(self) -> bool:
custom_components/lock_code_manager/providers/matter.py:926:                "Lock %s: availability check failed: %s",
```

> TOOL

tool_use Read
id: toolu_016sq4NGDnWepbFe3WMs4ibR
```json
{
  "file_path": "/home/<USER>/projects/lock_code_manager/custom_components/lock_code_manager/providers/matter.py",
  "offset": 200,
  "limit": 110
}
```

> TOOL

tool_result
id: toolu_016sq4NGDnWepbFe3WMs4ibR
```
200	        """
201	        Return True — Matter locks expose the full User/Credential model.
202	
203	        Matter's DoorLock cluster manages users and credentials as distinct
204	        entities, so the base orchestration runs the user-first lifecycle
205	        (create/update user, then write its Personal Identification Number
206	        credential; delete the user when its last credential is removed).
207	        """
208	        return True
209	
210	    def _get_matter_node(self) -> Any | None:
211	        """
212	        Get the MatterNode for this lock from the Matter integration.
213	
214	        Uses the Matter integration's helper to resolve the node from the
215	        device entry, which correctly handles the device identifier format.
216	        Returns the node object with .node_id and access to the client.
217	        """
218	        if not self.device_entry:
219	            return None
220	        try:
221	            return get_node_from_device_entry(self.hass, self.device_entry)
222	        except Exception as err:
223	            LOGGER.debug(
224	                "Failed to resolve Matter node for %s: %s",
225	                self.lock.entity_id,
226	                err,
227	            )
228	            return None
229	
230	    def _get_matter_client(self) -> Any | None:
231	        """Get the MatterClient via the Matter integration helper."""
232	        try:
233	            return get_matter(self.hass).matter_client
234	        except Exception as err:
235	            LOGGER.debug(
236	                "Failed to get Matter client for %s: %s",
237	                self.lock.entity_id,
238 […]

> AGENT

Now the `async_is_device_available` for Matter (line 919) — the heart of Bug 1:

> TOOL

tool_use Read
id: toolu_01Qntki8P2NJMXuB2ovJ5Ee2
```json
{
  "file_path": "/home/<USER>/projects/lock_code_manager/custom_components/lock_code_manager/providers/matter.py",
  "offset": 860,
  "limit": 90
}
```

> TOOL

tool_result
id: toolu_01Qntki8P2NJMXuB2ovJ5Ee2
```
860	                    ) from retry_err
861	                if _is_transient_credential_status(retry_status):
862	                    raise _transient_status_disconnect(
863	                        self.lock.entity_id, slot, retry_status
864	                    ) from retry_err
865	                raise CodeRejectedError(
866	                    code_slot=slot,
867	                    lock_entity_id=self.lock.entity_id,
868	                    reason=str(retry_err),
869	                ) from retry_err
870	
871	        self._push_credential_update(slot, SlotCredential.unreadable())
872	        return WriteResult.CONFIRMED
873	
874	    async def async_delete_credential(self, ref: CredentialRef) -> bool:
875	        """
876	        Clear a Personal Identification Number credential from the lock.
877	
878	        Looks up the user's current PIN credential index and clears that
879	        Matter credential. ``ref.slot`` is the LCM slot identifier; the
880	        Matter credential index is rediscovered per call (LCM does not
881	        pin the index to the LCM slot under the user-tag idempotency
882	        design). Returns True when the user had a PIN to clear and the
883	        clear succeeded; False when no PIN was present.
884	
885	        Pushes SlotCredential.empty() to the coordinator immediately
886	        because Matter does not emit LockUserChange for LCM-initiated
887	        clears.
888	        """
889	        credential_index = await self._find_pin_credential_index_for_user(ref.user_id)
890	        if credential_index is None:
891	            return False
892	
893	        client, node = self._require_client_and_node()
894	        try:
895	            await clear_lock_credential(
896	                client,
897	                node,
898	                credential_type="pin",
899	                credential_index=credential_index,
900	            )
901	        except ServiceValidationError as err:
902	            raise LockOperationFailed(
903	                f"Matter clear_lock_credential rejected input […]

> AGENT

Let me check how `device_entry` is resolved (a stale/None capture would explain the persistent false negative) and the base `async_internal_is_integration_connected`.

> TOOL

tool_use Read
id: toolu_01FBmtrNmYFavaH97ph32bfQ
```json
{
  "file_path": "/home/<USER>/projects/lock_code_manager/custom_components/lock_code_manager/providers/_base.py",
  "offset": 780,
  "limit": 130
}
```

> TOOL

tool_result
id: toolu_01FBmtrNmYFavaH97ph32bfQ
```
780	            except asyncio.CancelledError:
781	                # If our own task is being cancelled, propagate; otherwise
782	                # the CancelledError is for the reconnect task we just
783	                # cancelled and is expected.
784	                current = asyncio.current_task()
785	                if current is not None and current.cancelling() > 0:
786	                    raise
787	            except Exception as err:
788	                _LOGGER.warning(
789	                    "Reconnect task raised during teardown of %s: %s",
790	                    self.lock.entity_id,
791	                    err,
792	                    exc_info=err,
793	                )
794	        self._reconnect_task = None
795	
796	        if self.supports_push:
797	            self.unsubscribe_push_updates()
798	
799	    async def async_is_device_available(self) -> bool:
800	        """Return whether the physical device is available for commands."""
801	        return True
802	
803	    @final
804	    def _setup_config_entry_state_listener(self) -> None:
805	        """Listen for provider config entry state changes to resubscribe."""
806	        lock_entry = self.lock_config_entry
807	        if not lock_entry or self._config_entry_state_unsub:
808	            return
809	
810	        self._last_entry_state = lock_entry.state
811	
812	        @callback
813	        def _handle_state_change() -> None:
814	            to_state = lock_entry.state
815	            if to_state == self._last_entry_state:
816	                return
817	
818	            if to_state == ConfigEntryState.LOADED:
819	                # The provider transitioned through LOADED twice in quick
820	                # succession (e.g. reload during reconnect). Cancel any
821	                # prior in-flight reconnect; drain any pending exception
822	                # on a prior task that […]

> AGENT

Let me check Matter's `async_is_integration_connected` override and the `device_entry` property.

> TOOL

tool_use Bash
id: toolu_01E1CmADj9Josios7U3uYgai
```json
{
  "command": "grep -n \"async_is_integration_connected\\|def device_entry\\|device_entry\\b\\|self\\.device_entry\" custom_components/lock_code_manager/providers/matter.py | head; echo \"=== base device_entry ===\"; grep -n \"device_entry\" custom_components/lock_code_manager/providers/_base.py | head",
  "description": "Find device_entry and matter connection check"
}
```

> TOOL

tool_result
id: toolu_01E1CmADj9Josios7U3uYgai
```
23:    get_node_from_device_entry,
218:        if not self.device_entry:
221:            return get_node_from_device_entry(self.hass, self.device_entry)
=== base device_entry ===
184:    device_entry: dr.DeviceEntry | None = field(default=None, init=False)
346:        self.device_entry = self.dev_reg.async_get(device_id)
```

> TOOL

tool_use Read
id: toolu_018eXNvVDfkpU6U2eCinS48P
```json
{
  "file_path": "/home/<USER>/projects/lock_code_manager/custom_components/lock_code_manager/providers/_base.py",
  "offset": 325,
  "limit": 70
}
```

> TOOL

tool_result
id: toolu_018eXNvVDfkpU6U2eCinS48P
```
325	                LOGGER.warning(
326	                    "Lock %s: push unsubscribe raised, continuing teardown: %s",
327	                    self.lock.entity_id,
328	                    err,
329	                )
330	
331	    @final
332	    @callback
333	    def __post_init__(self) -> None:
334	        """Post initialization."""
335	        if not (device_id := self.lock.device_id):
336	            _LOGGER.warning(
337	                "Lock %s does not have a device ID; push updates and "
338	                "event subscriptions will be unavailable. "
339	                "platform=%s, config_entry_id=%s, unique_id=%s",
340	                self.lock.entity_id,
341	                self.lock.platform,
342	                self.lock.config_entry_id,
343	                self.lock.unique_id,
344	            )
345	            return
346	        self.device_entry = self.dev_reg.async_get(device_id)
347	
348	    @final
349	    def __repr__(self) -> str:
350	        """Return a string representation."""
351	        return f"{self.__class__.__name__}(domain={self.domain}, lock={self.lock.entity_id})"
352	
353	    @final
354	    def __hash__(self) -> int:
355	        """Hash by lock entity ID (one BaseLock instance per physical lock)."""
356	        return hash(self.lock.entity_id)
357	
358	    @final
359	    def __eq__(self, other: Any) -> bool:
360	        """Two BaseLock instances are equal when they wrap the same lock entity."""
361	        if not isinstance(other, BaseLock):
362	            return False
363	        return self.lock.entity_id == other.lock.entity_id
364	
365	    @final
366	    def _raise_not_implemented(self, method_name: str, guidance: str = "") -> NoReturn:
367	        """Raise ProviderNotImplementedError for unimplemented methods."""
368	        raise ProviderNotImplementedError(self, method_name, guidance)
369	
370	    @property
371	    def display_name(self) -> str:
372	        """Return a human-readable name for this lock."""
373 […]

> AGENT

Let me check the Matter helper imports — specifically `get_lock_info` vs `get_lock_users` (Kyle says the latter works) and `get_node_from_device_entry`.

> TOOL

tool_use Read
id: toolu_01QDhjfCpCGBz5GhmnbKfFDg
```json
{
  "file_path": "/home/<USER>/projects/lock_code_manager/custom_components/lock_code_manager/providers/matter.py",
  "offset": 1,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01QDhjfCpCGBz5GhmnbKfFDg
```
1	"""
2	Matter lock provider.
3	
4	Handles PIN credential management via Matter lock helpers.
5	PINs are write-only: occupied slots report ``SlotCredential.unreadable()``,
6	cleared slots report ``SlotCredential.empty()``. Subscribes to DoorLock
7	cluster events via the push framework for code slot tracking (LockOperation)
8	and occupancy updates (LockUserChange).
9	"""
10	
11	from __future__ import annotations
12	
13	from dataclasses import dataclass
14	from datetime import timedelta
15	from typing import Any, Literal
16	
17	from matter_server.client.exceptions import MatterClientException
18	from matter_server.common.errors import MatterError
19	from matter_server.common.models import EventType
20	
21	from homeassistant.components.matter.helpers import (
22	    get_matter,
23	    get_node_from_device_entry,
24	)
25	from homeassistant.components.matter.lock_helpers import (
26	    SetCredentialFailedError,
27	    clear_lock_credential,
28	    clear_lock_user,
29	    get_lock_info,
30	    get_lock_users,
31	    set_lock_credential,
32	    set_lock_user,
33	)
34	from homeassistant.config_entries import ConfigEntry
35	from homeassistant.core import callback
36	from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
37	
38	from ..domain.credentials import (
39	    Credential,
40	    CredentialRef,
41	    CredentialType,
42	    CredentialTypeCapability,
43	    LockCapabilities,
44	    SetUserResult,
45	    User,
46	    WriteResult,
47	)
48	from ..domain.exceptions import (
49	    CodeRejectedError,
50	    DuplicateCodeError,
51	    LockCodeManagerProviderError,
52	    LockDisconnected,
53	    LockOperationFailed,
54	)
55	from ..domain.models import SlotCredential
56	from ._base import BaseLock
57	from ._util import make_compact_tagged_name, parse_slot_num, […]

> AGENT

Let me confirm the backoff ceiling and check whether there's already an open PR addressing this.

> TOOL

tool_use Bash
id: toolu_01JAv7fhmEcK3dSkHPg2sU9y
```json
{
  "command": "grep -n \"BACKOFF_\\|POLL_FAILURE_ALERT_THRESHOLD\" custom_components/lock_code_manager/const.py",
  "description": "Check backoff constants"
}
```

> TOOL

tool_result
id: toolu_01JAv7fhmEcK3dSkHPg2sU9y
```
116:BACKOFF_FAILURE_THRESHOLD: int = 3
117:BACKOFF_INITIAL_SECONDS: int = 60
118:BACKOFF_MAX_SECONDS: int = 1800  # 30 minutes
121:POLL_FAILURE_ALERT_THRESHOLD: int = 12
```

> TOOL

tool_use Bash
id: toolu_01DJgq1eLGRYEqhHtYiVnYze
```json
{
  "command": "gh pr list --state open --json number,title,headRefName --limit 30 | python3 -c \"import json,sys; [print(p['number'], p['title']) for p in json.load(sys.stdin)]\" 2>/dev/null; echo \"=== recent merged touching matter/coordinator ===\"; git log --oneline -15 -- custom_components/lock_code_manager/providers/matter.py custom_components/lock_code_manager/domain/coordinator.py",
  "description": "List open PRs and recent relevant commits"
}
```

> TOOL

tool_result
id: toolu_01DJgq1eLGRYEqhHtYiVnYze
```
1267 build(deps-dev): bump markdownlint-cli from 0.48.0 to 0.49.0
1262 build(deps): update pytest requirement from >=9.0.3 to >=9.1.0
1254 build(deps-dev): update zigpy requirement from >=1.4.1 to >=1.6.0
=== recent merged touching matter/coordinator ===
4657eab9 code cleanup (#1264)
a7fb8547 fix: don't flap a lock_offline repair during integration startup (#1257) (#1260)
89841f49 feat: verified-credential lifecycle — close the silent-failure window (#1259)
ebac2739 fix(zwave_js,matter): tolerate ambiguous credential writes; universal masked read projection (#1251, #1257) (#1258)
1f599d67 feat(matter): add compact lcm<slot> tier between canonical and slot-only (#1249)
e16d49ab fix(matter): address #1246 review — log noise, fallback routing, test caplog level (#1248)
0ae0aec0 fix(matter): fall back to slot-only userName when lock rejects canonical tag (#1246)
1c5cdada fix(matter): tolerate MatterError on set_lock_user UPDATE; map on CREATE (#1245)
f12bb475 feat(matter): adopt user-tag identity, decouple user lifecycle from credentials (#1239)
dfbeaa28 refactor(providers): hoist PIN-readability guard to base seam (#1237)
3c75dd5b feat(matter): migrate to unified DoorLock credential API (#1228)
0f450a96 docs: tighten comments and docstrings across the integration (#1201)
1652f1ba refactor(layout): move models/callbacks/util into domain/ (final step) (#1199)
4d090657 refactor(layout): move domain logic into domain/ (#1198)
840b976c refactor(layout): introduce domain/ subpackage with pure leaves (#1195)
```

> AGENT

I've now traced both code paths Kyle cites. Here's what's going on.

## The two issues

**#1257** (jprasm, closed) — Matter slots disabled after restart due to startup credential sync failures. That got fixed (#1258/#1260) and jprasm confirmed it. Then **kyleberry showed up in the comments** saying he has a similar-but-not-identical problem, dumped diagnostics, and — to his credit — opened **#1268** as a clean standalone issue instead of hijacking the closed one.

**#1268** (kyleberry, open) is the real report. He's on LCM 4.1.0, an Ultraloq Bolt over Matter, in a Docker Compose setup where HA and `python-matter-server` restart *together*. His Z-Wave lock in the same config entry rides through the restart fine; only the Matter lock gets stuck. And critically: `matter.get_lock_users` returns all his users at any point, the lock entity is `locked` and controllable — yet LCM's coordinator reports `lock_unreachable: true` and all slots go `unavailable`.

He diagnosed **two compounding bugs**, and after reading the code, **he's essentially right on both.**

## Bug 2 — confirmed, and it's in our code

This is the clearest finding. `domain/coordinator.py:370-385`:

```python
async def async_get_usercodes(self):
    try:
        data = await self._lock.async_internal_get_usercodes()
    except LockCodeManagerError as err:
        self._apply_backoff()
        if not self.last_update_success:
            return {}          # <-- […]
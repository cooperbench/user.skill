> DEVELOPER

# Investigation: UC-only Z-Wave locks reporting "Credential slot for pin_code must be between 1 and 0"

## Primary sources

Original bug report (READ FIRST, including all comments and reactions):

    https://github.com/raman325/lock_code_manager/issues/1251

Local mitigation PR (currently OPEN against `main`, not merged):

    https://github.com/raman325/lock_code_manager/pull/1252

Fetch both with:

    gh issue view 1251 -R raman325/lock_code_manager --comments
    gh pr view 1252 -R raman325/lock_code_manager --comments
    gh pr diff 1252 -R raman325/lock_code_manager

The issue thread is where the reporter (jhenkens) and a second affected user
(randallkn) describe the symptom. The PR thread documents the LCM-side
investigation, the call-chain trace, the chosen mitigation (bypass
lock_helpers and call `node.access_control` directly), and the reviewer's
inline comments + my replies — which establish the current understanding of
which exception types reach which layer.

## Background

A Home Assistant custom integration called Lock Code Manager (LCM) recently
migrated from calling the legacy `zwave_js.set_lock_usercode` service to using
`homeassistant.components.zwave_js.lock_helpers.async_set_credential`. This is
the new unified user/credential API HA added in 2026.6.x that exposes the
unified `node.access_control` surface from node-zwave-js v15.23.4+.

After LCM 4.0.x ships this change, some users see their existing Z-Wave locks
break with this exact error per slot:

    "Credential slot for pin_code must be between 1 and 0."

Two important data points from the issue […]

> AGENT

I'll run this investigation systematically: fetch the primary sources (issue #1251, PR #1252), bring the three sibling checkouts up to date against upstream, then work through each hypothesis. Starting with the primary sources and repo fetches in parallel.

> TOOL

tool_use Bash
id: toolu_01UnRxe3fMifLxQZMoNRKmTE
```json
{
  "command": "gh issue view 1251 -R raman325/lock_code_manager --comments 2>&1 | head -300",
  "description": "Fetch issue 1251 with comments"
}
```

> TOOL

tool_use Bash
id: toolu_01S2kDYAaXy9AfsoSVyH6WGh
```json
{
  "command": "gh pr view 1252 -R raman325/lock_code_manager --comments 2>&1 | head -400",
  "description": "Fetch PR 1252 with comments"
}
```

> TOOL

tool_use Bash
id: toolu_01F5wqq2BVfgEEWR76UJSB48
```json
{
  "command": "cd /home/<USER>/projects/home-assistant && git fetch upstream 2>&1 | tail -2 && git log upstream/dev --oneline -1",
  "description": "Fetch HA core upstream and show latest commit"
}
```

> TOOL

tool_use Bash
id: toolu_01RTubupBkjmeHbJjKaUxJ2e
```json
{
  "command": "cd /home/<USER>/projects/zwave-js-server-python && git fetch upstream 2>&1 | tail -2 && git log upstream/main --oneline -1",
  "description": "Fetch zwave-js-server-python upstream and show latest commit"
}
```

> TOOL

tool_use Bash
id: toolu_01QTshtAY6DY6LSykwghfesN
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git fetch upstream 2>&1 | tail -2 && git log upstream/master --oneline -1",
  "description": "Fetch node-zwave-js upstream and show latest commit"
}
```

> TOOL

tool_result
id: toolu_01UnRxe3fMifLxQZMoNRKmTE
```
author:	jhenkens
association:	none
edited:	false
status:	none
--
Yep, woke up this morning to my codes not working. I've pinned back to 3.x.
--
author:	randallkn
association:	none
edited:	false
status:	none
--
> Yep, woke up this morning to my codes not working. I've pinned back to 3.x.

Phew... that worked for me too. I haven't had time to dig deeper, since I upgraded HA at the same time 😓 
--
author:	raman325
association:	owner
edited:	false
status:	none
--
Sorry guys and glad you were able to revert. I will look at this tonight and push a fix ASAP
--
author:	raman325
association:	owner
edited:	false
status:	none
--
can you confirm which integration (zwave, matter, etc) and lock you are using? I am working on a fix but I think there may be an upstream bug that may need to be fixed if this is within the Z-Wave provider
--
author:	jhenkens
association:	none
edited:	false
status:	none
--
ZWaveJS UI
--
author:	raman325
association:	owner
edited:	false
status:	none
--
it would be really helpful to get a couple of things from you to help nail the source of this issue […]

> TOOL

tool_result
id: toolu_01S2kDYAaXy9AfsoSVyH6WGh
```
author:	Copilot (AI)
association:	contributor
edited:	false
status:	commented
--
## Pull request overview

This PR addresses a production regression in the Z-Wave JS provider where UC-only (User Code CC–only) locks cannot manage PINs because Home Assistant’s `lock_helpers` validation relies on U3C (User Credential CC) capabilities and rejects writes when `num_slots=0`. The fix makes the provider bypass the HA helper wrappers for set/delete credential writes and adds a UC-only capability fallback path.

**Changes:**
- Bypass `homeassistant.components.zwave_js.lock_helpers` for `async_set_credential` / `async_delete_credential` and call `node.access_control.{set_credential,delete_credential}` directly, mapping `SetCredentialResult` to LCM exceptions.
- Enhance `async_get_capabilities` to detect UC-only locks (missing PIN or zero-slot PIN) and derive slot count via `zwave_js_server.util.lock.get_usercodes`, forcing slot-only routing.
- Update/extend provider and e2e tests to cover UC-detection branches and the new direct-call write path.

### Reviewed changes

Copilot reviewed 4 out of 4 changed files in this pull request and generated 3 comments.

| File | Description |
| ---- | ----------- |
| custom_components/lock_code_manager/providers/zwave_js.py | Implements UC-only capability fallback and direct `access_control` set/delete credential calls with status→exception mapping. |
| tests/providers/zwave_js/test_provider.py | Adds UC-mode capability fallback tests and validates direct `access_control` primitive calls + status mapping. |
| tests/providers/zwave_js/test_e2e.py | Updates E2E assertions […]

> TOOL

tool_result
id: toolu_01F5wqq2BVfgEEWR76UJSB48
```
 + c00921b9b10...65fd4005a5a yoto_sensors         -> upstream/yoto_sensors  (forced update)
 * [new tag]                 2026.6.2             -> 2026.6.2
2e8e5c63e86 Fix Hue light level sensor crash on None value (#173532)
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_result
id: toolu_01RTubupBkjmeHbJjKaUxJ2e
```
 * [new tag]         0.71.0     -> 0.71.0
 * [new tag]         0.72.0     -> 0.72.0
d3caf60 Bump codecov/codecov-action from 6.0.1 to 7.0.0 (#1448)
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_result
id: toolu_01QTshtAY6DY6LSykwghfesN
```
007da492f fix: discard `NodeNamingAndLocationCC` reports with overlong payload (#8865)
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> AGENT

Primary sources are coming in. Let me get the full issue body, the PR description, the PR diff, and the inline review comments.

> TOOL

tool_use Bash
id: toolu_01SQgAswCjJhzd1QcLXRHpjc
```json
{
  "command": "gh issue view 1251 -R raman325/lock_code_manager --json title,body -q '.title, \"----\", .body' 2>&1 | head -120",
  "description": "Fetch issue 1251 body"
}
```

> TOOL

tool_result
id: toolu_01SQgAswCjJhzd1QcLXRHpjc
```
[ISSUE] 4.0.2 Code rejected Credential slot for pin_code must be between 1 and 0
----
### What happened?

I just upgraded to 4.0.2 and saw "Slot n disabled" notifications for each slot code, which then reoccur when I try to reenable them in the dashboard.
I see the following in the HA log for each slot:
slot n Code rejected: Lock lock.XXX: cannot set code on slot 1 — Credential slot for pin_code must be between 1 and 0

### Steps to reproduce the issue

1. Upgrade to 4.0.2
2. Observe notifications or (optionally) reenable slots in the UI


### Home Assistant Version

2026.6.2

### What version of Lock Code Manager are you running?

4.0.2

### Lock make and model

_No response_

### Debug logs (paste)

```shell

```

### Debug logs (upload)

_No response_

### Lock Code Manager diagnostics (upload)

_No response_

### Lock integration diagnostics (upload)

_No response_

### Diagnostics (paste)

```json

```

### Browser console logs (paste)

```shell

```

### Browser console logs (upload)

_No response_

### Screenshots

_No response_

### Anything else?

_No response_
```

> TOOL

tool_use Bash
id: toolu_01CHu5eBEkbKqUFuUNkLKJSd
```json
{
  "command": "gh api repos/raman325/lock_code_manager/pulls/1252/comments --paginate -q '.[] | \"=== \\(.user.login) on \\(.path):\\(.line // .original_line)\\n\\(.body)\\n\"' 2>&1 | head -250",
  "description": "Fetch PR 1252 inline review comments"
}
```

> TOOL

tool_use Bash
id: toolu_01SwVoupWJYKzUhTyW6zMmAR
```json
{
  "command": "gh pr view 1252 -R raman325/lock_code_manager --json title,body -q '.title, \"----\", .body' 2>&1 | head -150",
  "description": "Fetch PR 1252 body"
}
```

> TOOL

tool_result
id: toolu_01SwVoupWJYKzUhTyW6zMmAR
```
fix(zwave_js): bypass HA helper validation that breaks UC-only locks (#1251)
----
## Proposed change

Fixes #1251 — production regression where users with UC-only Z-Wave locks (legacy 500-series and older firmwares without User Credential CC) can't manage PINs after upgrading to 4.0.x. The error is the upstream message \`Credential slot for pin_code must be between 1 and 0\`.

### Two related root causes, one fix path

1. **HA's \`lock_helpers.async_get_credential_capabilities\` queries U3C capabilities only** (via \`get_credential_capabilities_cached\`), so UC-only locks return PIN with \`num_slots=0\` or no PIN at all.
2. **HA's \`lock_helpers.async_set_credential\` validates \`1 <= slot <= num_slots\` against (1) before calling the driver**, rejecting all writes on UC-only locks.

The node-zwave-js driver itself (v15.23.4+) unifies UC and U3C behind \`node.access_control\`: every method (\`setCredential\`, \`deleteCredential\`, \`getUsersCached\`, etc.) branches internally based on which CC the lock actually implements. So the dispatch is real; only HA's validation wrapper is the bug.

### Fix

- **\`async_set_credential\` and \`async_delete_credential\`** now call \`node.access_control.set_credential\` / \`delete_credential\` directly, skipping HA's wrapper. We map the returned \`SetCredentialResult\` enum to LCM's typed exceptions:
  - \`OK\` → return True
  - \`ERROR_DUPLICATE_CREDENTIAL\` / \`ERROR_DUPLICATE_ADMIN_PIN_CODE\` → \`DuplicateCodeError\`
  - Any other non-OK → \`CodeRejectedError\` (set) / \`LockOperationFailed\` (delete)
- **\`async_get_capabilities\`** synthesizes meaningful […]

> TOOL

tool_result
id: toolu_01CHu5eBEkbKqUFuUNkLKJSd
```
=== Copilot on custom_components/lock_code_manager/providers/zwave_js.py:270
The UC-fallback path currently swallows *all* exceptions from get_usercodes() and treats them as “no UC slots”. This can mis-detect capabilities during transient Z-Wave/driver failures (or hide programming errors), causing the integration to report no PIN support and route operations incorrectly. Prefer mapping Z-Wave transport errors to LockDisconnected and reachable/validation errors to LockOperationFailed, consistent with the rest of this provider.

=== Copilot on custom_components/lock_code_manager/providers/zwave_js.py:450
async_set_credential now bypasses lock_helpers and calls node.access_control.set_credential directly, but it no longer catches HomeAssistantError. Other Z-Wave provider operations consistently wrap HomeAssistantError as LockOperationFailed; without this, a reachable-lock failure may bubble up as an unexpected exception and be treated as a bug by higher layers.

=== Copilot on custom_components/lock_code_manager/providers/zwave_js.py:488
async_delete_credential now calls node.access_control.delete_credential directly, but it does not catch HomeAssistantError. For consistency with async_get_users/async_set_user/etc., reachable-lock failures should be wrapped as LockOperationFailed rather than bubbling up as unexpected exceptions.

=== raman325 on custom_components/lock_code_manager/providers/zwave_js.py:270
Addressed in a128f285 — dropped the blanket `except Exception` so any unexpected exception surfaces.

`get_usercodes()` is pure value-DB walking against `node.values` (a dict): it raises `NotFoundError` internally on missing slots (caught there, returns the accumulated list) and otherwise just returns. There's no transport call to fail transiently, so […]

> TOOL

tool_use Bash
id: toolu_01JUWuPNmQ1XDhqBUjumiq9h
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git show upstream/master:packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts > /tmp/AccessControl.ts && wc -l /tmp/AccessControl.ts && grep -n \"usesUserCredentialCC\\|getCredentialCapabilitiesCached\\|ucCredentialType\\|supportedUsers\\|FIXME\" /tmp/AccessControl.ts",
  "description": "Extract upstream AccessControl.ts and locate key symbols"
}
```

> TOOL

tool_result
id: toolu_01JUWuPNmQ1XDhqBUjumiq9h
```
    1911 /tmp/AccessControl.ts
217:	// FIXME: This is technically not correct. A node could support both CCs,
221:	get #usesUserCredentialCC(): boolean {
230:		if (this.#usesUserCredentialCC) {
233:					UserCredentialCCValues.supportedUsers.endpoint(
271:					UserCodeCCValues.supportedUsers.endpoint(
288:	public getCredentialCapabilitiesCached(): CredentialCapabilities {
289:		if (this.#usesUserCredentialCC) {
327:				UserCodeCCValues.supportedUsers.endpoint(
340:			credentialTypes.set(this.#ucCredentialType, {
372:		if (this.#usesUserCredentialCC) {
402:		if (this.#usesUserCredentialCC) {
414:		if (this.#usesUserCredentialCC) {
487:		if (this.#usesUserCredentialCC) {
489:				UserCredentialCCValues.supportedUsers.endpoint(
501:				UserCodeCCValues.supportedUsers.endpoint(this.endpoint.index),
529:		if (this.#usesUserCredentialCC) {
657:		if (this.#usesUserCredentialCC) {
772:		if (this.#usesUserCredentialCC) {
810:						credentialType: this.#ucCredentialType,
825:		if (this.#usesUserCredentialCC) {
862:		if (this.#usesUserCredentialCC) {
891:		if (this.#usesUserCredentialCC) {
906:		if (this.#usesUserCredentialCC) {
917:			if (type != undefined && type !== this.#ucCredentialType) {
921:				this.#ucCredentialType,
938:		if (this.#usesUserCredentialCC) {
948:			if (type != undefined && type !== this.#ucCredentialType) {
952:				this.#ucCredentialType,
972:		if (this.#usesUserCredentialCC) {
990:		if (this.#usesUserCredentialCC) {
1004:		if (this.#usesUserCredentialCC) {
1020:		if (this.#usesUserCredentialCC) {
1037:		if (this.#usesUserCredentialCC) {
1155:		if (this.#usesUserCredentialCC) {
1229:		if (this.#usesUserCredentialCC) {
1249:				&& credentialType !== this.#ucCredentialType
1291:						credentialType: this.#ucCredentialType,
1310:	 * {@link getCredentialCapabilitiesCached} to check for support via the
1320:		if (!this.#usesUserCredentialCC) {
1353:		if (!this.#usesUserCredentialCC) {
1371:		timeout ??= this.getCredentialCapabilitiesCached()
1402:		if (!this.#usesUserCredentialCC) {
1417:		if (this.#usesUserCredentialCC) {
1433:		if (this.#usesUserCredentialCC) {
1454:		return this.getCredentialCapabilitiesCached()
1460: […]

> TOOL

tool_use Bash
id: toolu_019jpmnXiP4tMYXrVnC6ui3g
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git grep -l '\"User Credential\"' upstream/master -- packages/config/config/devices/ 2>/dev/null",
  "description": "Find device configs declaring User Credential CC"
}
```

> TOOL

tool_use Bash
id: toolu_01UZkFUsp9mWZTMbZxkqXmf6
```json
{
  "command": "cd /home/<USER>/projects/home-assistant && git show upstream/dev:homeassistant/components/zwave_js/lock_helpers.py > /tmp/lock_helpers.py && wc -l /tmp/lock_helpers.py",
  "description": "Extract upstream lock_helpers.py"
}
```

> TOOL

tool_result
id: toolu_01UZkFUsp9mWZTMbZxkqXmf6
```
     522 /tmp/lock_helpers.py
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_result
id: toolu_019jpmnXiP4tMYXrVnC6ui3g
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01Kb4Gb4ZiXSA3rA3HiGo7j6
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git grep -l \"addCCs\\|removeCCs\" upstream/master -- packages/config/config/devices/ | head -20; echo \"---0x83/131 search---\"; git grep -ln '\"0x83\"\\|User Credential' upstream/master -- packages/config/config/devices/ | head",
  "description": "Search device configs for CC declarations"
}
```

> TOOL

tool_use Read
id: toolu_012r9ckmhz4QBE5hEcCTyEbB
```json
{
  "file_path": "/tmp/AccessControl.ts",
  "offset": 200,
  "limit": 170
}
```

> TOOL

tool_use Read
id: toolu_013LT7KxPkiWEkxcBDxVvvuB
```json
{
  "file_path": "/tmp/lock_helpers.py"
}
```

> TOOL

tool_result
id: toolu_01Kb4Gb4ZiXSA3rA3HiGo7j6
```
---0x83/131 search---
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_result
id: toolu_013LT7KxPkiWEkxcBDxVvvuB
```
1	"""Lock helpers for Z-Wave JS credential management.
2	
3	Provides business logic for user/credential CRUD, capability queries,
4	auto-find logic, and validation.
5	"""
6	
7	import asyncio
8	from collections import defaultdict
9	import logging
10	from typing import TypedDict
11	
12	from zwave_js_server.const.command_class.access_control import (
13	    SetCredentialResult,
14	    SetUserResult,
15	    UserCredentialRule,
16	    UserCredentialType,
17	    UserCredentialUserType,
18	)
19	from zwave_js_server.model.access_control import SetUserOptions
20	from zwave_js_server.model.node import Node
21	
22	from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
23	
24	from .const import (
25	    CREDENTIAL_RULE_DUAL,
26	    CREDENTIAL_RULE_SINGLE,
27	    CREDENTIAL_RULE_TRIPLE,
28	    CREDENTIAL_TYPE_BLE,
29	    CREDENTIAL_TYPE_DESFIRE,
30	    CREDENTIAL_TYPE_EYE_BIOMETRIC,
31	    CREDENTIAL_TYPE_FACE_BIOMETRIC,
32	    CREDENTIAL_TYPE_FINGER_BIOMETRIC,
33	    CREDENTIAL_TYPE_HAND_BIOMETRIC,
34	    CREDENTIAL_TYPE_NFC,
35	    CREDENTIAL_TYPE_PASSWORD,
36	    CREDENTIAL_TYPE_PIN_CODE,
37	    CREDENTIAL_TYPE_RFID_CODE,
38	    CREDENTIAL_TYPE_UNSPECIFIED_BIOMETRIC,
39	    CREDENTIAL_TYPE_UWB,
40	    DOMAIN,
41	    USER_TYPE_DISPOSABLE,
42	    USER_TYPE_DURESS,
43	    USER_TYPE_EXPIRING,
44	    USER_TYPE_GENERAL,
45	    USER_TYPE_NON_ACCESS,
46	    USER_TYPE_PROGRAMMING,
47	    USER_TYPE_REMOTE_ONLY,
48	)
49	
50	_LOGGER = logging.getLogger(__name__)
51	
52	# --- Enum <-> string mappings ---
53	
54	CREDENTIAL_TYPE_MAP: dict[UserCredentialType, str] = {
55	    UserCredentialType.PIN_CODE: CREDENTIAL_TYPE_PIN_CODE,
56	    UserCredentialType.PASSWORD=[REDACTED],
57	    UserCredentialType.RFID_CODE: CREDENTIAL_TYPE_RFID_CODE,
58	    UserCredentialType.BLE: CREDENTIAL_TYPE_BLE,
59	    UserCredentialType.NFC: CREDENTIAL_TYPE_NFC,
60	    UserCredentialType.UWB: CREDENTIAL_TYPE_UWB,
61	    UserCredentialType.EYE_BIOMETRIC: CREDENTIAL_TYPE_EYE_BIOMETRIC,
62	    UserCredentialType.FACE_BIOMETRIC: CREDENTIAL_TYPE_FACE_BIOMETRIC,
63	    UserCredentialType.FINGER_BIOMETRIC: CREDENTIAL_TYPE_FINGER_BIOMETRIC,
64	    UserCredentialType.HAND_BIOMETRIC: CREDENTIAL_TYPE_HAND_BIOMETRIC,
65	    UserCredentialType.UNSPECIFIED_BIOMETRIC: CREDENTIAL_TYPE_UNSPECIFIED_BIOMETRIC,
66	    UserCredentialType.DESFIRE: CREDENTIAL_TYPE_DESFIRE,
67	}
68	CREDENTIAL_TYPE_REVERSE_MAP: dict[str, UserCredentialType] = {
69 […]

> TOOL

tool_result
id: toolu_012r9ckmhz4QBE5hEcCTyEbB
```
200				return AssignCredentialResult.Error_Unknown;
201		}
202	}
203	
204	const NON_PIN_CHARS = /[^0-9]/;
205	
206	/**
207	 * Whether the supported ASCII characters indicate a non-PIN device.
208	 * When unknown (V1 nodes), defaults to PIN-only per the spec.
209	 */
210	function supportsNonPINChars(supportedASCIIChars: string | undefined): boolean {
211		return supportedASCIIChars != undefined
212			&& NON_PIN_CHARS.test(supportedASCIIChars);
213	}
214	
215	/** High-level API for managing users and credentials on access control devices */
216	export class AccessControlAPI extends FeatureAPI {
217		// FIXME: This is technically not correct. A node could support both CCs,
218		// and we may have to decide which one to use, or switch between them on
219		// the fly using Version CC / migration.
220		// This is not implemented yet, so checking for U3C first is fine for now.
221		get #usesUserCredentialCC(): boolean {
222			return this.endpoint.supportsCC(CommandClasses["User Credential"]);
223		}
224	
225		/**
226		 * Returns the user-related capabilities of this endpoint.
227		 * This method uses cached information from the most recent interview.
228		 */
229		public getUserCapabilitiesCached(): UserCapabilities {
230			if (this.#usesUserCredentialCC) {
231				return {
232					maxUsers: this.getValue<number>(
233						UserCredentialCCValues.supportedUsers.endpoint(
234							this.endpoint.index,
235						),
236 […]

> TOOL

tool_use Read
id: toolu_015m6m3wZBBTfxTiRqxDa4cf
```json
{
  "file_path": "/tmp/AccessControl.ts",
  "offset": 1440,
  "limit": 120
}
```

> TOOL

tool_result
id: toolu_015m6m3wZBBTfxTiRqxDa4cf
```
1440		}
1441	
1442		#ucAPI(): UserCodeCCAPI {
1443			return this.endpoint
1444				.commandClasses["User Code"] as unknown as UserCodeCCAPI;
1445		}
1446	
1447		#u3cAPI(): UserCredentialCCAPI {
1448			return this.endpoint.commandClasses[
1449				"User Credential"
1450			] as unknown as UserCredentialCCAPI;
1451		}
1452	
1453		#supportsCredentialType(type: UserCredentialType): boolean {
1454			return this.getCredentialCapabilitiesCached()
1455				.supportedCredentialTypes
1456				.has(type);
1457		}
1458	
1459		/** Returns the credential type to use for User Code CC based on supported characters */
1460		get #ucCredentialType(): UserCredentialType {
1461			const supportedASCIIChars = this.getValue<string>(
1462				UserCodeCCValues.supportedASCIIChars.endpoint(this.endpoint.index),
1463			);
1464			return supportsNonPINChars(supportedASCIIChars)
1465				? UserCredentialType.Password
1466				: UserCredentialType.PINCode;
1467		}
1468	
1469		/** Maps User Code CC's UserIDStatus to the unified active/userType model */
1470		#mapUserCodeStatusToUserData(
1471			userId: number,
1472			status: UserIDStatus,
1473		): UserData | undefined {
1474			// These statuses indicate no user is configured for this slot
1475			if (
1476				status === UserIDStatus.Available
1477				|| status === UserIDStatus.StatusNotAvailable
1478				|| status === UserIDStatus.PassageMode
1479			) {
1480				return undefined;
1481			}
1482	
1483			let active: boolean;
1484			let userType: UserCredentialUserType;
1485			switch (status) {
1486				case UserIDStatus.Enabled:
1487					active = true;
1488					userType = UserCredentialUserType.General;
1489					break;
1490				case UserIDStatus.Disabled:
1491					active = false;
1492					userType […]

> TOOL

tool_use Bash
id: toolu_015qFNdYs2sBSNykZA1QeB9i
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git log upstream/master --oneline --follow -- packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts | head -40",
  "description": "History of AccessControl.ts"
}
```

> TOOL

tool_result
id: toolu_015qFNdYs2sBSNykZA1QeB9i
```
ebec1eea8 fix(cc): purge U3C cache before bulk delete events (#8829)
b4beb5bc3 fix: unified API for adding users and credentials together in one call (#8837)
acc14813d feat: implement bulk-delete APIs for credentials (#8793)
c97bdb7aa refactor: rename User/Credential management result enums to `...Result` (#8758)
cca17b9a3 fix: separate U3C users from credential slots, improve error handling (#8756)
604d368a7 refactor: make `endpoint.accessControl` `undefined` if unsupported (#8752)
da5ba2f29 refactor: move credential API behind the `accessControl` namespace (#8750)
7bbb8b4f8 feat: add unified API to manage users and credentials (#8738)
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01DNxN4rk39MT2qMyjuoTL21
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git log upstream/master -S 'usesUserCredentialCC' --oneline -- packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts | tail -5; echo ---; git log upstream/master -S 'This is not implemented yet, so checking for U3C first is fine for now' --oneline | tail -3",
  "description": "Find commits introducing the dispatch and FIXME"
}
```

> TOOL

tool_result
id: toolu_01DNxN4rk39MT2qMyjuoTL21
```
b4beb5bc3 fix: unified API for adding users and credentials together in one call (#8837)
acc14813d feat: implement bulk-delete APIs for credentials (#8793)
cca17b9a3 fix: separate U3C users from credential slots, improve error handling (#8756)
604d368a7 refactor: make `endpoint.accessControl` `undefined` if unsupported (#8752)
da5ba2f29 refactor: move credential API behind the `accessControl` namespace (#8750)
---
7bbb8b4f8 feat: add unified API to manage users and credentials (#8738)
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01PUPLFug5XYHMCEZpuS4bDe
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && for c in 7bbb8b4f8 da5ba2f29 604d368a7 cca17b9a3 c97bdb7aa acc14813d b4beb5bc3 ebec1eea8; do echo \"$c -> $(git tag --contains $c | head -1)\"; done; echo \"--- latest tag:\"; git tag --sort=-v:refname | head -3",
  "description": "Map AccessControl.ts commits to release tags"
}
```

> TOOL

tool_result
id: toolu_01PUPLFug5XYHMCEZpuS4bDe
```
7bbb8b4f8 -> v15.23.0
da5ba2f29 -> v15.23.1
604d368a7 -> v15.23.2
cca17b9a3 -> v15.23.3
c97bdb7aa -> v15.23.4
acc14813d -> v15.24.0
b4beb5bc3 -> v15.24.1
ebec1eea8 -> v15.24.1
--- latest tag:
v15.24.2
v15.24.1
v15.24.0
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01HUistLBQc1PeJc7cnADWFc
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git show 7bbb8b4f8:packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts 2>/dev/null > /tmp/AccessControl_orig.ts || git show 7bbb8b4f8:packages/zwave-js/src/lib/node/AccessControl.ts > /tmp/AccessControl_orig.ts 2>/dev/null; ls -la /tmp/AccessControl_orig.ts 2>/dev/null; git show 7bbb8b4f8 --stat | head -30",
  "description": "Get original AccessControl implementation from first commit"
}
```

> TOOL

tool_result
id: toolu_01HUistLBQc1PeJc7cnADWFc
```
-rw-r--r--@ 1 raman  wheel  0 Jun 11 22:43 /tmp/AccessControl_orig.ts
commit 7bbb8b4f82f7836a49392f172eb4a1b83e4068da
Author: AlCalzone <<REDACTED_EMAIL>>
Date:   Thu Apr 9 15:31:31 2026 +0200

    feat: add unified API to manage users and credentials (#8738)

 docs/api/endpoint.md                               |  488 ++++++++
 packages/cc/src/cc/UserCredentialCC.ts             |  147 +--
 packages/cc/src/cc/_CCValues.generated.ts          |   62 +-
 packages/cc/src/cc/index.ts                        |    4 +-
 packages/cc/src/lib/_Types.ts                      |   11 +
 packages/zwave-js/src/Node.ts                      |    7 +
 .../src/lib/node/CCHandlers/UserCredentialCC.ts    |  103 ++
 packages/zwave-js/src/lib/node/Endpoint.ts         |  532 +--------
 packages/zwave-js/src/lib/node/Node.ts             |   16 +
 packages/zwave-js/src/lib/node/_Types.ts           |   67 ++
 .../{Endpoint.ts => endpoint-mixins/00_Base.ts}    |   20 +-
 .../lib/node/endpoint-mixins/05_AccessControl.ts   | 1217 ++++++++++++++++++++
 .../zwave-js/src/lib/node/endpoint-mixins/index.ts |    3 +
 .../lib/test/node/accessControl.UserCode.test.ts   |  837 ++++++++++++++
 .../test/node/accessControl.UserCredential.test.ts | 1030 +++++++++++++++++
 15 files changed, 3869 insertions(+), 675 deletions(-)
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01C4rg81NQX3VcrB3ntwhr9G
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git show 7bbb8b4f8:packages/zwave-js/src/lib/node/endpoint-mixins/05_AccessControl.ts > /tmp/AC_15.23.0.ts && grep -n \"usesUserCredentialCC\\|getCredentialCapabilitiesCached\\|supportedUsers\\|numberOfCredentialSlots\" /tmp/AC_15.23.0.ts | head -30",
  "description": "Inspect v15.23.0 original implementation"
}
```

> TOOL

tool_result
id: toolu_01C4rg81NQX3VcrB3ntwhr9G
```
79:	getCredentialCapabilitiesCached(): CredentialCapabilities | undefined;
235:	private get _usesUserCredentialCC(): boolean {
240:		return !this._usesUserCredentialCC
248:		if (this._usesUserCredentialCC) {
251:					UserCredentialCCValues.supportedUsers.endpoint(this.index),
284:					UserCodeCCValues.supportedUsers.endpoint(this.index),
295:	public getCredentialCapabilitiesCached():
299:		if (this._usesUserCredentialCC) {
342:				numberOfCredentialSlots: 1,
365:		if (this._usesUserCredentialCC) {
391:		if (this._usesUserCredentialCC) {
400:		if (this._usesUserCredentialCC) {
467:		if (this._usesUserCredentialCC) {
469:				UserCredentialCCValues.supportedUsers.endpoint(this.index),
479:				UserCodeCCValues.supportedUsers.endpoint(this.index),
495:		if (this._usesUserCredentialCC) {
599:		if (this._usesUserCredentialCC) {
641:		if (this._usesUserCredentialCC) {
672:		if (this._usesUserCredentialCC) {
704:		if (this._usesUserCredentialCC) {
713:		if (this._usesUserCredentialCC) {
751:		if (this._usesUserCredentialCC) {
769:					slot <= cap.numberOfCredentialSlots;
800:		if (this._usesUserCredentialCC) {
879:		if (this._usesUserCredentialCC) {
924:		if (!this._usesUserCredentialCC) {
938:		timeout ??= this.getCredentialCapabilitiesCached()
964:		if (!this._usesUserCredentialCC) {
975:		if (this._usesUserCredentialCC) {
988:		if (this._usesUserCredentialCC) {
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01MAKK5ntZAooZ6p73edveg7
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git show cca17b9a3 --stat | head -20; echo \"==== diff of getCredentialCapabilitiesCached in 8756 ====\"; git show cca17b9a3 -- packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts packages/zwave-js/src/lib/node/endpoint-mixins/05_AccessControl.ts | grep -A 60 \"getCredentialCapabilitiesCached\" | head -100",
  "description": "Inspect PR 8756 changes to capabilities"
}
```

> TOOL

tool_result
id: toolu_01MAKK5ntZAooZ6p73edveg7
```
commit cca17b9a3563204ff7c938e776c5d9e87da6cbc4
Author: AlCalzone <<REDACTED_EMAIL>>
Date:   Tue Apr 21 10:13:04 2026 +0200

    fix: separate U3C users from credential slots, improve error handling (#8756)

 docs/api/CCs/UserCredential.md                     |  31 +-
 docs/api/endpoint.md                               | 104 ++-
 packages/cc/src/cc/UserCredentialCC.ts             | 729 +++++++++++++-------
 packages/cc/src/cc/_CCValues.generated.ts          |  52 +-
 packages/cc/src/cc/index.ts                        |  16 +-
 packages/zwave-js/src/Node.ts                      |   7 +-
 .../src/lib/node/CCHandlers/UserCredentialCC.ts    |  52 +-
 packages/zwave-js/src/lib/node/Node.ts             |   6 +
 .../src/lib/node/feature-apis/AccessControl.ts     | 738 ++++++++++++++++----
 .../src/lib/node/mockCCBehaviors/UserCredential.ts | 266 +++++---
 .../cc-specific/userCredentialInterview.test.ts    |  73 +-
 .../lib/test/node/accessControl.UserCode.test.ts   | 179 ++++-
 .../test/node/accessControl.UserCredential.test.ts | 754 +++++++++++++++++++--
 13 files changed, 2337 insertions(+), 670 deletions(-)
==== diff of getCredentialCapabilitiesCached in 8756 ====
+	 * {@link getCredentialCapabilitiesCached} to check for support via the
+	 * `supportsCredentialAssignment` property.
+	 *
+	 * This communicates with the node.
+	 */
+	public async assignCredential(
+		type: UserCredentialType,
+		slot: number,
+		destinationUserId: number,
+	): Promise<AssignCredentialStatus> {
+		if (!this.#usesUserCredentialCC) {
+			throw new ZWaveError(
+				"This node does not support assigning a credential to a different user",
+				ZWaveErrorCodes.CC_NotSupported,
+			);
+		}
+
+		this.#assertValidSlot(type, slot);
+
+		const api = this.#u3cAPI();
+		const response = await api.setUserCredentialAssociation({
+			credentialType: type,
+			credentialSlot: slot,
+			destinationUserId,
+		});
+		if (response) {
+			await this.endpoint.tryGetNode()?.handleCommand(response);
 		}
+		return u3cAssociationResultToStatus(response);
 	} […]

> TOOL

tool_use Read
id: toolu_01AUog4iYrg5ZTUD5mo5G3xA
```json
{
  "file_path": "/tmp/AC_15.23.0.ts",
  "offset": 228,
  "limit": 140
}
```

> TOOL

tool_result
id: toolu_01AUog4iYrg5ZTUD5mo5G3xA
```
228			return this.tryGetNode()?.getValue(valueId);
229		}
230	
231		// FIXME: This is technically not correct. A node could support both CCs,
232		// and we may have to decide which one to use, or switch between them on
233		// the fly using Version CC / migration.
234		// This is not implemented yet, so checking for U3C first is fine for now.
235		private get _usesUserCredentialCC(): boolean {
236			return this.supportsCC(CommandClasses["User Credential"]);
237		}
238	
239		private get _usesUserCodeCC(): boolean {
240			return !this._usesUserCredentialCC
241				&& this.supportsCC(CommandClasses["User Code"]);
242		}
243	
244		public getUserCapabilitiesCached():
245			| UserCapabilities
246			| undefined
247		{
248			if (this._usesUserCredentialCC) {
249				return {
250					maxUsers: this._getValue<number>(
251						UserCredentialCCValues.supportedUsers.endpoint(this.index),
252					) ?? 0,
253					supportedUserTypes: this._getValue<UserCredentialUserType[]>(
254						UserCredentialCCValues.supportedUserTypes.endpoint(
255							this.index,
256						),
257					) ?? [],
258					maxUserNameLength: this._getValue<number>(
259						UserCredentialCCValues.maxUserNameLength.endpoint(
260							this.index,
261						),
262					) ?? undefined,
263					supportedCredentialRules: this._getValue<UserCredentialRule[]>(
264						UserCredentialCCValues.supportedCredentialRules.endpoint(
265							this.index,
266						),
267					) ?? [],
268				};
269			} else if (this._usesUserCodeCC) {
270				const supportedStatuses = this._getValue<UserIDStatus[]>(
271					UserCodeCCValues.supportedUserIDStatuses.endpoint(this.index),
272				) ?? [];
273				const supportedUserTypes: UserCredentialUserType[] = [
274					UserCredentialUserType.General,
275				];
276				// User Code CC has no concept of user […]

> TOOL

tool_use Bash
id: toolu_01KHTVNjhqc43RYLTK7sBYrZ
```json
{
  "command": "cd /home/<USER>/projects/zwave-js-server-python && git show upstream/main:zwave_js_server/model/access_control.py > /tmp/access_control_py.py 2>/dev/null && grep -n \"number_of_credential_slots\\|class.*Capabilit\\|def \\|numberOfCredentialSlots\" /tmp/access_control_py.py | head -40; echo \"=== const ===\"; git show upstream/main:zwave_js_server/const/command_class/access_control.py 2>/dev/null | head -5; echo \"=== min server version ===\"; git grep -n \"MIN_SERVER_VERSION\\|minSchemaVersion\\|SCHEMA\" upstream/main -- zwave_js_server/const/__init__.py | head",
  "description": "Inspect python client access_control model"
}
```

> TOOL

tool_result
id: toolu_01KHTVNjhqc43RYLTK7sBYrZ
```
28:def serialize_credential_data(data: str | bytes) -> str | BufferObjectDataType:
35:def deserialize_credential_data(
46:class UserCredentialCapabilityDataType(TypedDict, total=False):
49:    numberOfCredentialSlots: int
59:class UserCredentialCapability:
62:    number_of_credential_slots: int
71:    def from_dict(cls, data: UserCredentialCapabilityDataType) -> Self:
74:            number_of_credential_slots=data["numberOfCredentialSlots"],
85:    def to_dict(self) -> UserCredentialCapabilityDataType:
88:            "numberOfCredentialSlots": self.number_of_credential_slots,
103:class UserCapabilitiesDataType(TypedDict, total=False):
114:class UserCapabilities:
124:    def from_dict(cls, data: UserCapabilitiesDataType) -> Self:
142:    def to_dict(self) -> UserCapabilitiesDataType:
157:class CredentialCapabilitiesDataType(TypedDict, total=False):
167:class CredentialCapabilities:
178:    def from_dict(cls, data: CredentialCapabilitiesDataType) -> Self:
199:    def to_dict(self) -> CredentialCapabilitiesDataType:
235:    def from_dict(cls, data: UserDataDataType) -> Self:
250:    def to_dict(self) -> UserDataDataType:
286:    def to_dict(self) -> SetUserOptionsDataType:
318:    def to_dict(self) -> AddUserCredentialDataType:
346:    def from_dict(cls, data: CredentialDataDataType) -> Self:
355:    def to_dict(self) -> CredentialDataDataType:
386:    def from_dict(cls, data: AddUserResultDataType) -> Self:
396:    def to_dict(self) -> AddUserResultDataType:
417:    def from_dict(cls, data: UserDeletedArgsDataType) -> Self:
421:    def to_dict(self) -> UserDeletedArgsDataType:
445:    def from_dict(cls, data: CredentialChangedArgsDataType) -> Self:
454:    def to_dict(self) -> CredentialChangedArgsDataType:
483:    def from_dict(cls, data: CredentialDeletedArgsDataType) -> Self:
491:    def to_dict(self) -> CredentialDeletedArgsDataType:
521:    def from_dict(cls, data: CredentialLearnProgressArgsDataType) -> Self:
531:    def to_dict(self) -> CredentialLearnProgressArgsDataType:
563:    def from_dict(cls, data: CredentialLearnCompletedArgsDataType) -> Self:
573:    def to_dict(self) -> CredentialLearnCompletedArgsDataType:
591:    def __init__(self, endpoint: Endpoint) -> None:
595:    async def is_supported(self) -> bool:
605:    async def get_user_capabilities_cached(self) […]

> TOOL

tool_use Bash
id: toolu_011H2SZyuikuEHLiHiaVSimz
```json
{
  "command": "cd /home/<USER>/projects/home-assistant && git show upstream/dev:homeassistant/components/zwave_js/manifest.json | grep -A3 requirements; git show upstream/dev:homeassistant/components/zwave_js/const.py | grep -n \"DRIVER_VERSION\\|SERVER_VERSION\\|MIN_\" | head",
  "description": "Check HA zwave_js requirements and min server version"
}
```

> TOOL

tool_result
id: toolu_011H2SZyuikuEHLiHiaVSimz
```
  "requirements": ["zwave-js-server-python==0.72.0"],
  "usb": [
    {
      "known_devices": ["Aeotec Z-Stick Gen5+", "Z-WaveMe UZB"],
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01DN1cxVyPTYZFE28qDQWbaP
```json
{
  "command": "gh release list -R zwave-js/zwave-js-ui --limit 12 2>&1; echo ====; gh release view -R zwave-js/zwave-js-ui --json tagName,body -q '.tagName, .body' 2>&1 | head -40",
  "description": "List recent zwave-js-ui releases and latest changelog"
}
```

> TOOL

tool_result
id: toolu_01DN1cxVyPTYZFE28qDQWbaP
```
Release 11.19.1	Latest	v11.19.1	2026-06-02T10:53:07Z
Release 11.19.0		v11.19.0	2026-05-27T14:30:58Z
Release 11.18.0		v11.18.0	2026-05-18T14:41:57Z
Release 11.17.0		v11.17.0	2026-05-05T07:25:52Z
Release 11.16.2		v11.16.2	2026-04-27T13:42:08Z
Release 11.16.1		v11.16.1	2026-04-22T14:32:10Z
Release 11.16.0		v11.16.0	2026-04-13T12:03:25Z
Release 11.15.1		v11.15.1	2026-03-23T13:37:19Z
Release 11.15.0		v11.15.0	2026-03-20T09:16:02Z
Release 11.14.0		v11.14.0	2026-03-06T09:34:32Z
Release 11.13.0		v11.13.0	2026-03-04T15:09:54Z
Release 11.12.0		v11.12.0	2026-02-19T10:14:19Z
====
v11.19.1
## [11.19.1](https://github.com/zwave-js/zwave-js-ui/compare/v11.19.0...v11.19.1) (2026-06-02)

### 🐛 Bug Fixes

* **ui:** last Awake column as localized datetime ([#4652](https://github.com/zwave-js/zwave-js-ui/issues/4652)) ([63d3c7e](https://github.com/zwave-js/zwave-js-ui/commit/63d3c7e314566a719badf451a71d535186653473))

### 🔧 Chores

* bump Z-Wave JS to 15.24.2, Server to 3.9.0 ([#4655](https://github.com/zwave-js/zwave-js-ui/issues/4655)) ([118ccd7](https://github.com/zwave-js/zwave-js-ui/commit/118ccd744c692be18b9b6e0a04cc1e8bdfaa8ccb))
```

> TOOL

tool_use Bash
id: toolu_01BBFUwaoF6rKTC8osTXhpDR
```json
{
  "command": "for v in v11.19.0 v11.18.0 v11.17.0 v11.16.2 v11.16.1 v11.16.0; do echo \"=== $v ===\"; gh release view $v -R zwave-js/zwave-js-ui --json body -q .body 2>/dev/null | grep -i \"bump z-wave js\\|zwave-js to\\|server to\" | head -3; done",
  "description": "Find bundled driver versions per zwave-js-ui release"
}
```

> TOOL

tool_result
id: toolu_01BBFUwaoF6rKTC8osTXhpDR
```
=== v11.19.0 ===
=== v11.18.0 ===
=== v11.17.0 ===
=== v11.16.2 ===
=== v11.16.1 ===
=== v11.16.0 ===
```

> TOOL

tool_use Bash
id: toolu_01Qrh2k1zpvodybCBaPKStsH
```json
{
  "command": "gh search issues --repo zwave-js/node-zwave-js \"getCredentialCapabilitiesCached OR accessControl user code\" --limit 10 2>&1; echo ====; gh search issues --repo zwave-js/zwave-js-ui \"user code credential\" --limit 10 2>&1",
  "description": "Search for related driver and UI issues"
}
```

> TOOL

tool_use Bash
id: toolu_011gjFPXkc4ykK4VHwxQkgEp
```json
{
  "command": "gh search issues --repo zwave-js/node-zwave-js \"between 1 and 0\" --limit 10 2>&1; echo ====; gh search issues --repo home-assistant/core \"credential_slot_out_of_range\" --limit 10 2>&1; echo ====; gh search issues --repo home-assistant/core \"credential slot must be between\" --limit 10 2>&1",
  "description": "Search issue trackers for the error message"
}
```

> TOOL

tool_result
id: toolu_011gjFPXkc4ykK4VHwxQkgEp
```
Invalid search query "( \"between 1 and 0\" ) repo:zwave-js/node-zwave-js type:issue".
The listed users and repositories cannot be searched either because the resources do not exist or you do not have permission to view them.
====
====
```

> TOOL

tool_result
id: toolu_01Qrh2k1zpvodybCBaPKStsH
```
Invalid search query "( \"getCredentialCapabilitiesCached OR accessControl user code\" ) repo:zwave-js/node-zwave-js type:issue".
The listed users and repositories cannot be searched either because the resources do not exist or you do not have permission to view them.
====
```

> AGENT

Searches need a different approach — let me use the search API directly and inspect release bodies fully.

> TOOL

tool_use Bash
id: toolu_01Rx75PQy1h4SQjf3fJ779Ge
```json
{
  "command": "gh api -X GET search/issues -f q='repo:zwave-js/node-zwave-js \"between 1 and 0\"' -q '.items[] | \"\\(.number) \\(.title) \\(.state) \\(.html_url)\"' 2>&1; echo ====A; gh api -X GET search/issues -f q='repo:home-assistant/core zwave credential slot' -q '.items[] | \"\\(.number) \\(.title) \\(.state)\"' 2>&1 | head; echo ====B; gh api -X GET search/issues -f q='repo:zwave-js/node-zwave-js accessControl in:title' -q '.items[] | \"\\(.number) \\(.title) \\(.state)\"' 2>&1 | head",
  "description": "Search issues via GitHub API"
}
```

> TOOL

tool_use Bash
id: toolu_01J4kVeLk8KcoSRARBhmimU2
```json
{
  "command": "gh release view v11.16.0 -R zwave-js/zwave-js-ui --json body -q .body 2>/dev/null | head -50",
  "description": "Read full v11.16.0 release body"
}
```

> TOOL

tool_result
id: toolu_01Rx75PQy1h4SQjf3fJ779Ge
```
{"message":"Validation Failed","errors":[{"message":"The listed users and repositories cannot be searched either because the resources do not exist or you do not have permission to view them.","resource":"Search","field":"q","code":"invalid"}],"documentation_url":"https://docs.github.com/v3/search/","status":"422"}gh: Validation Failed (HTTP 422)
====A
172740 Support Z-Wave locks that require coupled users and credentials open
168360 Add support for Z-Wave credential management closed
162057 Add get_lock_usercode service to zwave_js integration closed
161936 Add Matter lock user and credential management services closed
41639 Add last changed by for ozw lock closed
====B
{"message":"Validation Failed","errors":[{"message":"The listed users and repositories cannot be searched either because the resources do not exist or you do not have permission to view them.","resource":"Search","field":"q","code":"invalid"}],"documentation_url":"https://docs.github.com/v3/search/","status":"422"}gh: Validation Failed (HTTP 422)
```

> TOOL

tool_result
id: toolu_01J4kVeLk8KcoSRARBhmimU2
```
## [11.16.0](https://github.com/zwave-js/zwave-js-ui/compare/v11.15.1...v11.16.0) (2026-04-13)

### ✨ Features

* bump zwave-js@15.22.2 ([#4600](https://github.com/zwave-js/zwave-js-ui/issues/4600)) ([1e66ea6](https://github.com/zwave-js/zwave-js-ui/commit/1e66ea693809a91090cf54b23b70ab89c94003e3))
* bump zwave-js@15.23.0 ([#4613](https://github.com/zwave-js/zwave-js-ui/issues/4613)) ([802f564](https://github.com/zwave-js/zwave-js-ui/commit/802f56424d6b418406ba440fd6d36eb4cc7f2062))
* **ui:** move pagination to top of nodes table ([#4605](https://github.com/zwave-js/zwave-js-ui/issues/4605)) ([08b46dc](https://github.com/zwave-js/zwave-js-ui/commit/08b46dc62780369a21b725f93451c1098cf72008)), closes [#3603](https://github.com/zwave-js/zwave-js-ui/issues/3603) [#4488](https://github.com/zwave-js/zwave-js-ui/issues/4488)

### 🐛 Bug Fixes

* **docs:** clarify default value of BACKUPS_DIR ([#4597](https://github.com/zwave-js/zwave-js-ui/issues/4597)) ([0224aca](https://github.com/zwave-js/zwave-js-ui/commit/0224aca52e2f784e2dbc3ce71e3f2adf07d24471))
* specify exact Node.js version in release workflow ([c80566f](https://github.com/zwave-js/zwave-js-ui/commit/c80566f7d02136dbe65bc39ad57900a023b9e43a))
```

> TOOL

tool_use Bash
id: toolu_011yJhSfrkKANGgc9RvhWW5T
```json
{
  "command": "for v in v11.16.1 v11.16.2 v11.17.0 v11.18.0 v11.19.0; do echo \"=== $v ===\"; gh release view $v -R zwave-js/zwave-js-ui --json body -q .body 2>/dev/null | grep -iE \"bump.*(zwave-js|server)\" | head -5; done",
  "description": "Driver/server bumps in zwave-js-ui releases"
}
```

> TOOL

tool_use Bash
id: toolu_01Fc6r5BTx7KACtNBBTB5sxQ
```json
{
  "command": "gh release list -R zwave-js/server --limit 15 2>&1",
  "description": "List zwave-js server releases"
}
```

> TOOL

tool_result
id: toolu_011yJhSfrkKANGgc9RvhWW5T
```
=== v11.16.1 ===
* bump zwave-js@15.23.2 ([#4615](https://github.com/zwave-js/zwave-js-ui/issues/4615)) ([a21b2d8](https://github.com/zwave-js/zwave-js-ui/commit/a21b2d8be31ec701dfcb2fe3d7bdaabac479ed21))
* bump zwave-js@15.23.4 ([#4618](https://github.com/zwave-js/zwave-js-ui/issues/4618)) ([d496275](https://github.com/zwave-js/zwave-js-ui/commit/d496275a2993457f772d4f93e3db6f6f7a561d00))
=== v11.16.2 ===
* bump @zwave-js/server@3.8.0 ([#4621](https://github.com/zwave-js/zwave-js-ui/issues/4621)) ([d6902dc](https://github.com/zwave-js/zwave-js-ui/commit/d6902dc946373e97f8444aa6bd234f4fa0ccbff1))
* bump zwave-js@15.23.5 ([#4620](https://github.com/zwave-js/zwave-js-ui/issues/4620)) ([dd4bf1e](https://github.com/zwave-js/zwave-js-ui/commit/dd4bf1e90dffde0f04a3830e2235c4d22ffba7df))
=== v11.17.0 ===
=== v11.18.0 ===
* bump zwave-js@15.24.0 ([#4634](https://github.com/zwave-js/zwave-js-ui/issues/4634)) ([6daab13](https://github.com/zwave-js/zwave-js-ui/commit/6daab1340d91636ed2f676c77d7a093c87f30ab3))
=== v11.19.0 ===
```

> TOOL

tool_result ERROR
id: toolu_01Fc6r5BTx7KACtNBBTB5sxQ
```
Exit code 1
GraphQL: Could not resolve to a Repository with the name 'zwave-js/server'. (repository)
```

> TOOL

tool_use Bash
id: toolu_01RjD5zUvcbYo4iNgyWh3VvA
```json
{
  "command": "gh api -X GET search/repositories -f q='zwave-js-server in:name org:zwave-js' -q '.items[] | \"\\(.full_name)\"' 2>&1; gh release list -R zwave-js/zwave-js-server --limit 12 2>&1",
  "description": "Find zwave-js server repository"
}
```

> TOOL

tool_result
id: toolu_01RjD5zUvcbYo4iNgyWh3VvA
```
zwave-js/zwave-js-server
3.9.0	Latest	3.9.0	2026-06-01T12:50:07Z
3.8.0		3.8.0	2026-04-23T10:16:45Z
3.7.0		3.7.0	2026-04-23T08:43:44Z
3.6.0		3.6.0	2026-02-19T13:15:16Z
3.5.0		3.5.0	2026-02-19T13:12:43Z
3.4.0		3.4.0	2025-10-03T14:32:11Z
3.3.0		3.3.0	2025-09-28T17:18:06Z
3.2.1		3.2.1	2025-07-24T12:19:28Z
3.2.0		3.2.0	2025-07-24T12:05:01Z
3.1.0		3.1.0	2025-06-18T06:39:59Z
3.0.2		3.0.2	2025-05-08T07:58:41Z
3.0.1		3.0.1	2025-05-05T12:21:03Z
```

> TOOL

tool_use Bash
id: toolu_01JHbyYD2hSTCk2fCv8gkbRR
```json
{
  "command": "for v in 3.9.0 3.8.0 3.7.0; do echo \"=== $v ===\"; gh release view $v -R zwave-js/zwave-js-server --json body -q .body 2>/dev/null | head -25; done",
  "description": "Read zwave-js-server release notes"
}
```

> TOOL

tool_result
id: toolu_01JHbyYD2hSTCk2fCv8gkbRR
```
=== 3.9.0 ===
## What's Changed

* Bump Z-Wave JS Server to 3.9.0 (#1561) @AlCalzone
* Bump Schema to 49, add support for `addUser` @AlCalzone 
* Preserve existing log transports when modifying log config (#1559) @[copilot-swe-agent[bot]](https://github.com/apps/copilot-swe-agent)

=== 3.8.0 ===
## What's Changed

* Bump Z-Wave JS Server to 3.8.0 (#1552) @AlCalzone
* feat: support new credential API in Z-Wave JS 15.23.4, bump schema to 48 (#1544) @AlCalzone

=== 3.7.0 ===
## What's Changed

* Bump Z-Wave JS Server to 3.7.0 (#1551) @AlCalzone
* feat: add schema 47 zniffer, utility, and broadcast commands (4/4) (#1514) @raman325
* feat: add schema 47 controller, node, and endpoint commands (3/4) (#1513) @raman325
* fix: scope progress events to initiating client (#1529) @raman325
* fix: add missing result types for log listening commands (#1530) @raman325
* refactor: add sendEventToListeningClients helper (#1524) @raman325
* feat: add schema 47 driver commands (2/4) (#1510) @raman325
* fix: use optional properties instead of | undefined in result types (#1523) @raman325
* feat: add schema 47 state properties and events infrastructure (1/4) (#1509) @raman325
* fix: add event guards for callback-based event emissions (#1508) @raman325
* Downgrade @types/node to v20 and prevent automatic dependabot upgrades (#1521) […]

> TOOL

tool_use Bash
id: toolu_01X9MRJUetbwEPWGF8USn3ry
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git grep -c '\"compat\"' upstream/master -- 'packages/config/config/devices/*/[a-c]*.json' 2>/dev/null | head -3; echo \"=== addCCs anywhere ===\"; git grep -l 'addCCs' upstream/master 2>/dev/null | head -5; echo \"=== User Credential in config dir ===\"; git grep -il 'credential' upstream/master -- packages/config/config/devices/ 2>/dev/null | head -10",
  "description": "Sanity-check config DB grep approach"
}
```

> TOOL

tool_result
id: toolu_01X9MRJUetbwEPWGF8USn3ry
```
upstream/master:packages/config/config/devices/0x003b/be469zp.json:1
upstream/master:packages/config/config/devices/0x0060/ac301.json:1
upstream/master:packages/config/config/devices/0x0098/ct100.json:1
=== addCCs anywhere ===
upstream/master:packages/config/config.api.md
upstream/master:packages/config/src/devices/CompatConfig.ts
upstream/master:packages/config/src/devices/DeviceConfig.ts
upstream/master:packages/config/src/devices/lookupDevice.test.ts
upstream/master:packages/zwave-js/src/lib/node/Node.ts
=== User Credential in config dir ===
upstream/master:packages/config/config/devices/0x0189/117001.json
upstream/master:packages/config/config/devices/0x027e/g-240wz.json
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_019kFMKsamjjsYBtSRUnjdZC
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git show cca17b9a3 -- packages/cc/src/cc/_CCValues.generated.ts | grep -B3 -A25 \"credentialCapabilities\" | head -80",
  "description": "Check if 8756 changed credentialCapabilities value structure"
}
```

> TOOL

tool_result
id: toolu_019kFMKsamjjsYBtSRUnjdZC
```
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01XvoEqKYLgG93h9a2rXT59D
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git log --oneline -S '\"supportedUsers\"' upstream/master -- packages/cc/src/cc/UserCodeCC.ts | tail -5; git log upstream/master --oneline --diff-filter=A -- packages/cc/src/cc/UserCodeCC.ts | tail -2",
  "description": "History of UserCodeCC supportedUsers value"
}
```

> TOOL

tool_result
id: toolu_01XvoEqKYLgG93h9a2rXT59D
```
20788b760 refactor: migrate legacy decorators to ES decorators (#7360)
588555bc9 refactor: move CC implementations into separate package (#4668)
588555bc9 refactor: move CC implementations into separate package (#4668)
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_012qsJ6pTgQUDMzRCAco5A3N
```json
{
  "command": "cd /home/<USER>/projects/home-assistant && git log upstream/dev --oneline --follow -- homeassistant/components/zwave_js/lock_helpers.py | head; echo ====; cd /home/<USER>/projects/zwave-js-server-python && git show upstream/main:zwave_js_server/model/access_control.py | sed -n '590,680p'",
  "description": "HA lock_helpers history and python client RPC confirmation"
}
```

> TOOL

tool_result
id: toolu_012qsJ6pTgQUDMzRCAco5A3N
```
9757f8b5740 Add support for Z-Wave credential management (#168360)
====

    def __init__(self, endpoint: Endpoint) -> None:
        """Initialize the API wrapper for the given endpoint."""
        self._endpoint = endpoint

    async def is_supported(self) -> bool:
        """Return whether the endpoint supports access-control methods."""
        result = await self._endpoint.async_send_command(
            "access_control.is_supported",
            require_schema=48,
            wait_for_result=True,
        )
        assert result
        return cast(bool, result["supported"])

    async def get_user_capabilities_cached(self) -> UserCapabilities:
        """Return cached user capabilities for access control."""
        result = await self._endpoint.async_send_command(
            "access_control.get_user_capabilities_cached",
            require_schema=48,
            wait_for_result=True,
        )
        assert result
        capabilities = result["capabilities"]
        assert capabilities is not None
        return UserCapabilities.from_dict(cast(UserCapabilitiesDataType, capabilities))

    async def get_credential_capabilities_cached(
        self,
    ) -> CredentialCapabilities:
        """Return cached credential capabilities for access control."""
        result = await self._endpoint.async_send_command(
            "access_control.get_credential_capabilities_cached",
            require_schema=48,
            wait_for_result=True,
        )
        assert result
        capabilities = result["capabilities"]
        assert capabilities is not None
        return CredentialCapabilities.from_dict(
            cast(CredentialCapabilitiesDataType, capabilities)
        )

    async def get_user(self, user_id: int) -> UserData | None:
        """Return fresh data for a single access-control user."""
        result = await self._endpoint.async_send_command(
            "access_control.get_user",
            userId=user_id,
            require_schema=48,
            wait_for_result=True,
        )
        assert result is not None
        if (user := result.get("user")) is None:
            return None
        return UserData.from_dict(cast(UserDataDataType, user))

    async def get_user_cached(self, user_id: int) -> UserData | None:
        """Return cached data for a single access-control user."""
        result = await self._endpoint.async_send_command(
            "access_control.get_user_cached",
            userId=user_id,
            require_schema=48,
            wait_for_result=True,
        )
        assert result is not None
        if (user […]

> TOOL

tool_use Read
id: toolu_01SX3THyt6zCfgAgzSXqvbGP
```json
{
  "file_path": "/tmp/AccessControl.ts",
  "offset": 880,
  "limit": 130
}
```

> TOOL

tool_result
id: toolu_01SX3THyt6zCfgAgzSXqvbGP
```
880	
881		/**
882		 * Returns the data for a specific credential type and slot.
883		 * This method uses cached information from the most recent interview.
884		 */
885		public getCredentialCached(
886			type: UserCredentialType,
887			slot: number,
888		): CredentialData | undefined {
889			this.#assertValidSlot(type, slot);
890	
891			if (this.#usesUserCredentialCC) {
892				return this.#getCredentialCached_U3C(type, slot);
893			} else {
894				return this.#getCredentialCached_UC(type, slot);
895			}
896		}
897	
898		/**
899		 * Returns all credentials for the given user and optional type.
900		 * This communicates with the node to retrieve fresh information.
901		 */
902		public async getCredentialsForUser(
903			userId: number,
904			type?: UserCredentialType,
905		): Promise<CredentialData[]> {
906			if (this.#usesUserCredentialCC) {
907				if (type != undefined && !this.#supportsCredentialType(type)) {
908					return [];
909				}
910				return this.#queryCredentials_U3C(
911					userId,
912					type ?? UserCredentialType.None,
913					0,
914					type,
915				);
916			} else {
917				if (type != undefined && type !== this.#ucCredentialType) {
918					return [];
919				}
920				const cred = await this.getCredential(
921					this.#ucCredentialType,
922					// For User Code CC, credential slots and users are identical
923					userId,
924				);
925				// ...and there is at most one credential per user. […]

> TOOL

tool_use Bash
id: toolu_015HrBSiKYKj2oW1N3ahMA3H
```json
{
  "command": "grep -n \"assertValidSlot\" /tmp/AccessControl.ts | head; echo ====; sed -n '1780,1830p' /tmp/AccessControl.ts",
  "description": "Find driver-side slot validation"
}
```

> TOOL

tool_result
id: toolu_015HrBSiKYKj2oW1N3ahMA3H
```
589:			this.#assertValidSlot(credential.type, userId);
860:		this.#assertValidSlot(type, slot);
889:		this.#assertValidSlot(type, slot);
1038:			this.#assertValidSlot(type, slot);
1066:			this.#assertValidSlot(type, userId);
1156:			this.#assertValidSlot(type, slot);
1180:			this.#assertValidSlot(type, targetUserId);
1327:		this.#assertValidSlot(type, slot);
1360:		this.#assertValidSlot(type, slot);
1791:	#assertValidSlot(type: UserCredentialType, slot: number): void {
====
		// abstraction reuses that slot number as the credential slot.
		for (let userId = 1; userId <= maxUsers; userId++) {
			const credential = this.#getCredentialCached_UC(
				this.#ucCredentialType,
				userId,
			);
			if (credential) credentials.push(credential);
		}
		return credentials;
	}

	#assertValidSlot(type: UserCredentialType, slot: number): void {
		const caps = this.getCredentialCapabilitiesCached()
			.supportedCredentialTypes.get(type);
		if (!caps || slot < 1 || slot > caps.numberOfCredentialSlots) {
			throw new ZWaveError(
				`Credential slot ${slot} is out of range for credential type ${
					getEnumMemberName(UserCredentialType, type)
				}`,
				ZWaveErrorCodes.Argument_Invalid,
			);
		}
	}

	#getUserCached_U3C(userId: number): UserData | undefined {
		const userType = this.getValue<UserCredentialUserType>(
			UserCredentialCCValues.userType(userId).endpoint(
				this.endpoint.index,
			),
		);
		if (userType == undefined) return undefined;

		return {
			userId,
			active: this.getValue<boolean>(
				UserCredentialCCValues.userActive(userId).endpoint(
					this.endpoint.index,
				),
			) ?? false,
			userType,
			userName: this.getValue<string>(
				UserCredentialCCValues.userName(userId).endpoint(
					this.endpoint.index,
				),
			) ?? undefined,
			credentialRule: this.getValue<UserCredentialRule>(
				UserCredentialCCValues.credentialRule(userId).endpoint(
					this.endpoint.index,
				),
			) ?? undefined,
			expiringTimeoutMinutes: this.getValue<number>(
```

> TOOL

tool_use Read
id: toolu_01GriTWpUspyqnwM5ccsBkPq
```json
{
  "file_path": "/tmp/AccessControl.ts",
  "offset": 1130,
  "limit": 180
}
```

> TOOL

tool_result
id: toolu_01GriTWpUspyqnwM5ccsBkPq
```
1130			type: UserCredentialType,
1131			slot: number,
1132		): Promise<SetCredentialResult>;
1133		public async deleteCredential(
1134			userId: number | undefined,
1135			type: UserCredentialType,
1136			slot: number,
1137		): Promise<SetCredentialResult>;
1138	
1139		public async deleteCredential(
1140			userIdOrType: number | undefined,
1141			typeOrSlot: UserCredentialType | number,
1142			slot?: number,
1143		): Promise<SetCredentialResult> {
1144			// 2-arg overload: (type, slot) — normalize to the 3-arg form
1145			if (slot == undefined) {
1146				return this.deleteCredential(
1147					0,
1148					userIdOrType as UserCredentialType,
1149					typeOrSlot,
1150				);
1151			}
1152			const userId = userIdOrType ?? 0;
1153			const type = typeOrSlot as UserCredentialType;
1154	
1155			if (this.#usesUserCredentialCC) {
1156				this.#assertValidSlot(type, slot);
1157	
1158				const api = this.#u3cAPI();
1159				const raw = await api.setCredential({
1160					operationType: UserCredentialOperationType.Delete,
1161					userId,
1162					credentialType: type,
1163					credentialSlot: slot,
1164				});
1165				if (raw) await this.endpoint.tryGetNode()?.handleCommand(raw);
1166				return u3cCredentialReportTypeToSetCredentialResult(
1167					raw?.reportType,
1168				);
1169			} else {
1170				// User Code CC stores exactly one credential per user slot, with the
1171				// user identifier being the slot number. When the caller omits the
1172				// user (2-arg form), fall back to the slot. When both are given but
1173				// disagree, no credential can exist at that […]

> TOOL

tool_use Read
id: toolu_01VzU7Apo8dL5MCoYTf4QFZj
```json
{
  "file_path": "/tmp/AccessControl.ts",
  "offset": 1016,
  "limit": 110
}
```

> TOOL

tool_result
id: toolu_01VzU7Apo8dL5MCoYTf4QFZj
```
1016		 * Returns all credentials, regardless of ownership or type.
1017		 * This method uses cached information from the most recent interview.
1018		 */
1019		public getAllCredentialsCached(): CredentialData[] {
1020			if (this.#usesUserCredentialCC) {
1021				return this.#getAllCredentialsCached_U3C();
1022			} else {
1023				return this.#getAllCredentialsCached_UC();
1024			}
1025		}
1026	
1027		/**
1028		 * Creates or updates a credential for the given user.
1029		 * This communicates with the node.
1030		 */
1031		public async setCredential(
1032			userId: number,
1033			type: UserCredentialType,
1034			slot: number,
1035			data: string | Uint8Array,
1036		): Promise<SetCredentialResult> {
1037			if (this.#usesUserCredentialCC) {
1038				this.#assertValidSlot(type, slot);
1039	
1040				const api = this.#u3cAPI();
1041				const existing = this.#getCredentialCachedForUser_U3C(
1042					userId,
1043					type,
1044					slot,
1045				);
1046				const credentialData = typeof data === "string"
1047					? Bytes.from(data, "utf-8")
1048					: Bytes.from(data);
1049				const raw = await api.setCredential({
1050					operationType: existing
1051						? UserCredentialOperationType.Modify
1052						: UserCredentialOperationType.Add,
1053					userId,
1054					credentialType: type,
1055					credentialSlot: slot,
1056					credentialData,
1057				});
1058				if (raw) await this.endpoint.tryGetNode()?.handleCommand(raw);
1059				return u3cCredentialReportTypeToSetCredentialResult(
1060					raw?.reportType,
1061				);
1062			} else {
1063				// User Code CC stores exactly one credential per user slot. Ignore the
1064				// caller-provided unified slot and […]

> TOOL

tool_use Bash
id: toolu_01CWLgzZ1TwDEG5rFm4i4j9Y
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git show upstream/master:packages/cc/src/cc/UserCredentialCC.ts | grep -n -i \"backwards\\|backward\\|User Code\" | head -10; echo ===docs===; git grep -in \"must also support\\|backwards compat\" upstream/master -- docs/ packages/cc/src/cc/UserCredentialCC.ts | head -5",
  "description": "Check spec notes on U3C / User Code coexistence"
}
```

> TOOL

tool_use Bash
id: toolu_01BqELkormttxdXkZ3X4XgJd
```json
{
  "command": "gh api -X GET search/issues -f q='repo:zwave-js/node-zwave-js test' -q '.total_count' 2>&1; echo ====; gh api -X GET 'repos/zwave-js/node-zwave-js' -q '.full_name + \" issues:\" + (.has_issues|tostring)' 2>&1",
  "description": "Test search API against node-zwave-js"
}
```

> TOOL

tool_result
id: toolu_01CWLgzZ1TwDEG5rFm4i4j9Y
```
===docs===
upstream/master:docs/api/controller.md:1149:> [!ATTENTION] For backwards compatibility reasons, you cannot distinguish between devices that have no updates and devices that are not known to the firmware update service when using `getAvailableFirmwareUpdates`.
upstream/master:docs/api/valueid.md:110:- `allowed`: Defines the allowed values as a combination of single values and/or ranges. When present, this takes precedence over `min`/`max`/`steps` for determining which values are valid. Each entry is either `{ value: number }` for a single value or `{ from: number, to: number, step?: number }` for a range. The `min`/`max`/`steps` fields are still set for backwards compatibility.
upstream/master:docs/config-files/file-format.md:347:#### Backwards Compatibility
upstream/master:docs/config-files/file-format.md:349:For backwards compatibility with applications that don't support `allowed`, Z-Wave JS automatically computes `minValue` and `maxValue` from the set of allowed values. Applications can use this envelope for basic validation, while applications that support `allowed` can perform more precise validation.
upstream/master:docs/getting-started/migrating/v14.md:18:In input positions where Z-Wave JS previously accepted `Buffer`s, this change is backwards compatible, as `Buffer` is a subclass of `Uint8Array`. Applications can simply continue passing `Buffer` instances to Z-Wave JS.
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_result
id: toolu_01BqELkormttxdXkZ3X4XgJd
```
{"message":"Validation Failed","errors":[{"message":"The listed users and repositories cannot be searched either because the resources do not exist or you do not have permission to view them.","resource":"Search","field":"q","code":"invalid"}],"documentation_url":"https://docs.github.com/v3/search/","status":"422"}gh: Validation Failed (HTTP 422)
====
zwave-js/zwave-js issues:true
```

> AGENT

The repo was renamed — it's now `zwave-js/zwave-js`, which is why searches failed. Retrying with the correct name.

> TOOL

tool_use Bash
id: toolu_019YQpE66RJZpE3J328ysw4t
```json
{
  "command": "gh api -X GET search/issues -f q='repo:zwave-js/zwave-js \"between 1 and 0\"' -q '.items[] | \"\\(.number) \\(.title) [\\(.state)] \\(.html_url)\"' 2>&1; echo ====1; gh api -X GET search/issues -f q='repo:zwave-js/zwave-js \"out of range for credential type\"' -q '.items[] | \"\\(.number) \\(.title) [\\(.state)] \\(.html_url)\"' 2>&1; echo ====2; gh api -X GET search/issues -f q='repo:zwave-js/zwave-js \"User Credential\" lock in:title' -q '.items[] | \"\\(.number) \\(.title) [\\(.state)]\"' 2>&1 | head; echo ====3; gh api -X GET search/issues -f q='repo:zwave-js/zwave-js supportedUsers' -q '.items[] | \"\\(.number) \\(.title) [\\(.state)]\"' 2>&1 | head",
  "description": "Search zwave-js issues for the failure signatures"
}
```

> TOOL

tool_use Bash
id: toolu_01UqfY15ViaixfTHM91bVHwx
```json
{
  "command": "gh api -X GET search/issues -f q='repo:zwave-js/zwave-js-ui usercode OR \"user code\" credential' -q '.items[] | \"\\(.number) \\(.title) [\\(.state)]\"' 2>&1 | head; echo ====; gh api -X GET search/issues -f q='repo:zwave-js/zwave-js \"User Credential CC\"' -q '.items[] | \"\\(.number) \\(.title) [\\(.state)] \\(.html_url)\"' 2>&1 | head -15",
  "description": "Search zwave-js-ui and U3C issues"
}
```

> TOOL

tool_result
id: toolu_019YQpE66RJZpE3J328ysw4t
```
1 Refactor ZWaveLibraryTypes into its own file [closed] https://github.com/zwave-js/zwave-js/issues/1
2692 [bug] NAS-WR01ZE: kWh meter value displayed as negative number [closed] https://github.com/zwave-js/zwave-js/issues/2692
5080 fix: update zen72.json with more parameters [closed] https://github.com/zwave-js/zwave-js/pull/5080
5156 feat(config): zooz zen72 zen74 zen77 param 27 - 30 [closed] https://github.com/zwave-js/zwave-js/pull/5156
5841 Issue with 10.21.0 and zooz zen31 devices [closed] https://github.com/zwave-js/zwave-js/issues/5841
3320 fix(config): add parameter 17 to ZEN73 (firmware dependent) [closed] https://github.com/zwave-js/zwave-js/pull/3320
3523 [bug] Qubino currentValue is overwritten by an intermediate value when dimming the device [closed] https://github.com/zwave-js/zwave-js/issues/3523
3558 chore(deps): update dependency esbuild to ^0.13.8 [closed] https://github.com/zwave-js/zwave-js/pull/3558
1609 Qubino ZMNHJD1 not working [closed] https://github.com/zwave-js/zwave-js/issues/1609
1339 [question]  How to correct behaviour of Philio PAN in-wall relay? [closed] https://github.com/zwave-js/zwave-js/issues/1339
====1
====2
====3
2932 fix(cc): do not query all user codes during interview [closed]
3484 Re-interviewing Schlage BE469ZP loses S2_AccessControl association [closed]
```

> TOOL

tool_result
id: toolu_01UqfY15ViaixfTHM91bVHwx
```
4638 feat(wip): implement credential management UI [open]
4614 fix(zwave): migrate schedule user handling to unified access-control APIs [open]
1849 [zwave-js] Configuration Value removed from devices after reboot [closed]
====
7074 Add support for User Credential CC [closed] https://github.com/zwave-js/zwave-js/issues/7074
8738 feat: add unified API to manage users and credentials [closed] https://github.com/zwave-js/zwave-js/pull/8738
8629 feat(cc): implement User Credential CC commands and API [closed] https://github.com/zwave-js/zwave-js/pull/8629
8743 fix(maintenance): use source files for CCValues lookup in generate:docs [closed] https://github.com/zwave-js/zwave-js/pull/8743
8756 fix: separate U3C users from credential slots, improve error handling [closed] https://github.com/zwave-js/zwave-js/pull/8756
```

> TOOL

tool_use Bash
id: toolu_01LCHvERTEG3QTc49YWSe2pZ
```json
{
  "command": "cd /home/<USER>/projects/zwave-js-server-python && git show 0.72.0:zwave_js_server/const.py 2>/dev/null | grep -n \"SCHEMA\" | head -5; git show 0.72.0:zwave_js_server/const/__init__.py 2>/dev/null | grep -n \"SCHEMA\" | head -5",
  "description": "Check schema versions in pinned client 0.72.0"
}
```

> TOOL

tool_result
id: toolu_01LCHvERTEG3QTc49YWSe2pZ
```
14:MIN_SERVER_SCHEMA_VERSION = 49
16:MAX_SERVER_SCHEMA_VERSION = 49
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01NG86KTw3ocDvaoVRJBaavE
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git show v15.24.2:packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts | grep -n \"assertValidSlot\\|numberOfCredentialSlots: maxUsers\" | head; echo ====; git show v15.24.2:packages/zwave-js/src/lib/node/feature-apis/AccessControl.ts | grep -c \"assertValidSlot\"",
  "description": "Confirm assert and UC semantics in v15.24.2"
}
```

> TOOL

tool_result
id: toolu_01NG86KTw3ocDvaoVRJBaavE
```
342:				numberOfCredentialSlots: maxUsers,
589:			this.#assertValidSlot(credential.type, userId);
860:		this.#assertValidSlot(type, slot);
889:		this.#assertValidSlot(type, slot);
1038:			this.#assertValidSlot(type, slot);
1066:			this.#assertValidSlot(type, userId);
1156:			this.#assertValidSlot(type, slot);
1180:			this.#assertValidSlot(type, targetUserId);
1327:		this.#assertValidSlot(type, slot);
1360:		this.#assertValidSlot(type, slot);
====
10
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01Hv9X2aLjCZuUmZEXHbpZpV
```json
{
  "command": "gh api -X GET search/issues -f q='repo:home-assistant/core \"between 1 and 0\"' -q '.items[] | \"\\(.number) \\(.title) [\\(.state)] \\(.html_url)\"' 2>&1 | head; echo ====; cd /home/<USER>/projects/node-zwave-js && for f in 0x0189/117001.json 0x027e/g-240wz.json; do echo \"== $f\"; git show upstream/master:packages/config/config/devices/$f | grep -i -B2 -A2 credential | head -8; done",
  "description": "HA core issue search and config file inspection"
}
```

> TOOL

tool_result
id: toolu_01Hv9X2aLjCZuUmZEXHbpZpV
```
172255 Update numeric thresholds in triggers and conditions to be inclusive [closed] https://github.com/home-assistant/core/issues/172255
170451 light.toggle no longer fans out to light group / switch_as_x members on 2026.5.1 when an integration intercepts light.toggle (regression vs 2026.5.0) [open] https://github.com/home-assistant/core/issues/170451
173197 Regression in 2026.6.1: System reboots when creating backup including Frigate add-on (works fine in 2026.6.0) [open] https://github.com/home-assistant/core/issues/173197
167677 Bump HueBLE to 2.2.2 [closed] https://github.com/home-assistant/core/pull/167677
167680 Bump fluss-api to 0.2.4 [closed] https://github.com/home-assistant/core/pull/167680
167321 Bump afsapi to 0.3.1 [closed] https://github.com/home-assistant/core/pull/167321
164365 Add Govee H5140 CO2 monitor support to govee_ble [closed] https://github.com/home-assistant/core/pull/164365
164410 Rewrite madvr integration using madvr-envy client [closed] https://github.com/home-assistant/core/pull/164410
164319 Add Sharp COCORO Air integration [closed] https://github.com/home-assistant/core/pull/164319
158795 Bump pySmartThings to 3.5.1 [closed] https://github.com/home-assistant/core/pull/158795
====
== 0x0189/117001.json
		"inclusion": "Power up the LUX Z-Wave sensor by inserting the batteries (or fit the batteries in the correct polarity).\nYou may need to refer to your Z-Wave controller's instructions for adding devices.\n1. Put your primary Z-Wave gateway into inclusion mode, the gateway should confirm that it is waiting to add a new device,\n2. Press the Z-Wave Action button on your LUX Z-Wave sensor for 1 second.\n3. The LED on the LUX Z-Wave sensor will blink Red rapidly, followed by a solid Green LED […]

> TOOL

tool_use Bash
id: toolu_01NB44Nk8Zt7LGk4VcUzpRhE
```json
{
  "command": "gh api -X GET search/issues -f q='repo:zwave-js/zwave-js \"both CCs\" OR \"supports both\" user credential' -q '.items[] | \"\\(.number) \\(.title) [\\(.state)]\"' 2>&1 | head -6; echo ====; gh pr view 8738 -R zwave-js/zwave-js --json body -q .body 2>/dev/null | grep -i -A3 \"both\\|fixme\\|todo\" | head -20",
  "description": "Look for FIXME tracking issue"
}
```

> TOOL

tool_use Bash
id: toolu_01FLCm3eCFm2HHrdMGyDuvjm
```json
{
  "command": "cd /home/<USER>/projects/home-assistant && git show upstream/dev:homeassistant/components/zwave_js/services.yaml | grep -B2 -A8 \"invoke_cc_api\"; git grep -n \"SERVICE_INVOKE_CC_API\" upstream/dev -- homeassistant/components/zwave_js/services.py | head -3; git show upstream/dev:homeassistant/components/zwave_js/services.py | grep -n \"supports_response\\|SupportsResponse\" | head",
  "description": "Check invoke_cc_api response support"
}
```

> TOOL

tool_result
id: toolu_01NB44Nk8Zt7LGk4VcUzpRhE
```
8866 fix: persist cleared User Code CC slot in value DB after deleteCredential [open]
8738 feat: add unified API to manage users and credentials [closed]
8768 Access Control API: Make `deleteCredential` more flexible [closed]
8758 refactor: rename User/Credential management result enums to `...Result` [closed]
8825 Access Control API requires a new (synthetic) capability to indicate whether users with no credentials may exist [closed]
8756 fix: separate U3C users from credential slots, improve error handling [closed]
====
```

> TOOL

tool_result
id: toolu_01FLCm3eCFm2HHrdMGyDuvjm
```
        text:

invoke_cc_api:
  fields:
    area_id:
      example: living_room
      selector:
        area:
          device:
            - integration: zwave_js
          multiple: true
upstream/dev:homeassistant/components/zwave_js/services.py:547:            const.SERVICE_INVOKE_CC_API,
34:from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse, callback
97:        supports_response=SupportsResponse.ONLY,
125:        supports_response=SupportsResponse.ONLY,
135:        supports_response=SupportsResponse.ONLY,
152:        supports_response=SupportsResponse.ONLY,
603:            supports_response=SupportsResponse.ONLY,
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01BYL9VeSsbFjMLT7vKekuh7
```json
{
  "command": "cd /home/<USER>/projects/home-assistant && git show upstream/dev:homeassistant/components/zwave_js/services.py | sed -n '540,610p'",
  "description": "Check invoke_cc_api registration"
}
```

> TOOL

tool_result
id: toolu_01BYL9VeSsbFjMLT7vKekuh7
```
                    has_at_least_one_node,
                ),
            ),
        )

        self._hass.services.async_register(
            const.DOMAIN,
            const.SERVICE_INVOKE_CC_API,
            self.async_invoke_cc_api,
            schema=vol.Schema(
                vol.All(
                    {
                        **TARGET_VALIDATORS,
                        vol.Required(const.ATTR_COMMAND_CLASS): vol.All(
                            vol.Coerce(int), vol.Coerce(CommandClass)
                        ),
                        vol.Optional(const.ATTR_ENDPOINT): vol.Coerce(int),
                        vol.Required(const.ATTR_METHOD_NAME): cv.string,
                        vol.Required(const.ATTR_PARAMETERS): list,
                    },
                    cv.has_at_least_one_key(
                        ATTR_DEVICE_ID, ATTR_ENTITY_ID, ATTR_AREA_ID
                    ),
                    get_nodes_from_service_data,
                    has_at_least_one_node,
                ),
            ),
            description_placeholders={
                "api_docs_url": "https://zwave-js.github.io/node-zwave-js/#/api/CCs/index"
            },
        )

        self._hass.services.async_register(
            const.DOMAIN,
            const.SERVICE_REFRESH_NOTIFICATIONS,
            self.async_refresh_notifications,
            schema=vol.Schema(
                vol.All(
                    {
                        **TARGET_VALIDATORS,
                        vol.Required(const.ATTR_NOTIFICATION_TYPE): vol.All(
                            vol.Coerce(int), vol.Coerce(NotificationType)
                        ),
                        vol.Optional(const.ATTR_NOTIFICATION_EVENT): vol.Coerce(int),
                    },
                    cv.has_at_least_one_key(
                        ATTR_DEVICE_ID, ATTR_ENTITY_ID, ATTR_AREA_ID
                    ),
                    get_nodes_from_service_data,
                    has_at_least_one_node,
                ),
            ),
        )

        async_register_platform_entity_service(
            self._hass,
            const.DOMAIN,
            const.SERVICE_GET_LOCK_USERCODE,
            entity_domain=LOCK_DOMAIN,
            schema={
                vol.Optional(ATTR_CODE_SLOT): vol.Coerce(int),
            },
            func="async_get_lock_usercode",
            supports_response=SupportsResponse.ONLY,
        )

        async_register_platform_entity_service(
            self._hass,
            const.DOMAIN,
            const.SERVICE_SET_LOCK_USERCODE,
            entity_domain=LOCK_DOMAIN,
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_01V8FJnLN43VyXuhCCCEDtjT
```json
{
  "command": "cd /home/<USER>/projects/node-zwave-js && git show upstream/master:packages/cc/src/cc/UserCodeCC.ts > /tmp/UserCodeCC.ts && grep -n \"getUsersCount\\|UsersNumberReport\\|supportedUsers\" /tmp/UserCodeCC.ts | head -20",
  "description": "Confirm getUsersCount API and supportedUsers persistence"
}
```

> TOOL

tool_result
id: toolu_01V8FJnLN43VyXuhCCCEDtjT
```
73:	...V.staticProperty("supportedUsers", undefined, { internal: true }),
498:	public async getUsersCount(): Promise<MaybeNotKnown<number>> {
509:			UserCodeCCUsersNumberReport
514:		return response?.supportedUsers;
987:		const supportedUsers = await api.getUsersCount();
988:		if (supportedUsers == undefined) {
998:		for (let userId = 1; userId <= supportedUsers; userId++) {
1053:		const supportedUsers: number =
1054:			this.getValue(ctx, UserCodeCCValues.supportedUsers) ?? 0;
1128:						while (nextUserId > 0 && nextUserId <= supportedUsers) {
1146:							userId <= supportedUsers;
1171:				for (let userId = 1; userId <= supportedUsers; userId++) {
1188:			.getValue(UserCodeCCValues.supportedUsers.endpoint(endpoint.index));
1634:export interface UserCodeCCUsersNumberReportOptions {
1635:	supportedUsers: number;
1638:@CCCommand(UserCodeCommand.UsersNumberReport)
1639:@ccValueProperty("supportedUsers", UserCodeCCValues.supportedUsers)
1640:export class UserCodeCCUsersNumberReport extends UserCodeCC {
1642:		options: WithAddress<UserCodeCCUsersNumberReportOptions>,
1646:		this.supportedUsers = options.supportedUsers;
Shell cwd was reset to /home/<USER>/projects/lock_code_manager
```

> TOOL

tool_use Bash
id: toolu_015edjkKZJrYqx5NUUUyTzm9
```json
{
  "command": "grep -n \"purgeCachedUserCodes\" /tmp/AccessControl.ts; echo ====; awk '/#purgeCachedUserCodes\\(/,/^\t}/' /tmp/AccessControl.ts | head -60",
  "description": "Inspect purgeCachedUserCodes implementation"
}
```

> TOOL

tool_result
id: toolu_015edjkKZJrYqx5NUUUyTzm9
```
802:				this.#purgeCachedUserCodes(userId);
846:				this.#purgeCachedUserCodes();
1198:				this.#purgeCachedUserCodes(targetUserId);
1284:				this.#purgeCachedUserCodes(userId);
1597:	#purgeCachedUserCodes(userId?: number): void {
====
				this.#purgeCachedUserCodes(userId);
			}
			if (succeeded && existed) {
				const node = this.endpoint.tryGetNode();
				if (node) {
					node.emit("user deleted", this.endpoint as any, { userId });
					node.emit("credential deleted", this.endpoint as any, {
						userId,
						credentialType: this.#ucCredentialType,
						// For User Code CC, credential slots and users are identical
						credentialSlot: userId,
					});
				}
			}
			return succeeded ? SetUserResult.OK : SetUserResult.Error_Unknown;
		}
	}
				this.#purgeCachedUserCodes();
			}
			return succeeded ? SetUserResult.OK : SetUserResult.Error_Unknown;
		}
	}
				this.#purgeCachedUserCodes(targetUserId);
			}
			if (succeeded && existed) {
				const node = this.endpoint.tryGetNode();
				if (node) {
					node.emit("credential deleted", this.endpoint as any, {
						userId: targetUserId,
						credentialType: type,
						credentialSlot: targetUserId,
					});
					node.emit("user deleted", this.endpoint as any, {
						userId: targetUserId,
					});
				}
			}
			return succeeded
				? SetCredentialResult.OK
				: SetCredentialResult.Error_Unknown;
		}
	}
				this.#purgeCachedUserCodes(userId);
			}
			if (succeeded && existed) {
				const node = this.endpoint.tryGetNode();
				if (node) {
					node.emit("credential deleted", this.endpoint as any, {
						userId,
						credentialType: this.#ucCredentialType,
						credentialSlot: userId,
					});
					node.emit("user deleted", this.endpoint as any, { userId });
				}
			}
			return succeeded
				? SetCredentialResult.OK
				: SetCredentialResult.Error_Unknown;
		}
	}
```

> TOOL

tool_use Read
id: toolu_01D3bjGNx4MGoStncNCnwKQm
```json
{
  "file_path": "/tmp/AccessControl.ts",
  "offset": 1590,
  "limit": 50
}
```

> TOOL

tool_result
id: toolu_01D3bjGNx4MGoStncNCnwKQm
```
1590		}
1591	
1592		/**
1593		 * Removes cached user code status and code values from the value DB.
1594		 * If `userId` is given, only values for that user are removed. Otherwise, all
1595		 * cached user codes are purged.
1596		 */
1597		#purgeCachedUserCodes(userId?: number): void {
1598			const valueDB = this.endpoint.tryGetNode()?.valueDB;
1599			if (!valueDB) return;
1600	
1601			let values = valueDB.findValues(
1602				(vid) =>
1603					vid.endpoint === this.endpoint.index
1604					&& (UserCodeCCValues.userIdStatus.is(vid)
1605						|| UserCodeCCValues.userCode.is(vid)),
1606			);
1607			if (userId) {
1608				values = values.filter(
1609					(vid) => vid.propertyKey === userId,
1610				);
1611			}
1612	
1613			for (const vid of values) {
1614				valueDB.removeValue(vid);
1615			}
1616		}
1617	
1618		#mapCredentialData(
1619			result: UserCredentialGetResult,
1620		): CredentialData | undefined {
1621			if (!result?.credentialSlot) return undefined;
1622			return {
1623				userId: result.userId,
1624				type: result.credentialType,
1625				slot: result.credentialSlot,
1626				data: result.credentialData != undefined
1627					? normalizeCredentialData(
1628						result.credentialType,
1629						result.credentialData,
1630					)
1631					: undefined,
1632			};
1633		}
1634	
1635		async #queryCredentials_U3C(
1636			userId: number,
1637			startType: UserCredentialType,
1638			startSlot: number,
1639			filterType?: UserCredentialType,
```

> TOOL

tool_use Write
id: toolu_0189fDmwv3rRogiiNNktDur5
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-raman-projects-lock-code-manager/memory/project_zwave_uc_zero_slots_root_cause.md",
  "content": "---\nname: project-zwave-uc-zero-slots-root-cause\ndescription: Issue #1251 \"between 1 and 0\" — caps=0 originates in the driver; PR #1252's direct access_control bypass does NOT fix writes because the driver's #assertValidSlot enforces the same predicate\nmetadata:\n  type: project\n---\n\nInvestigation of issue #1251 (LCM 4.0.x, \"Credential slot for pin_code must be between 1 and 0\"), done 2026-06-11:\n\n- The error fires in HA `lock_helpers.async_set_credential` only when PIN_CODE IS present in caps with `number_of_credential_slots == 0`. If PIN were missing entirely the user would see `credential_type_not_supported` instead.\n- Caps are a pure pass-through: python client RPC → zwave-js-server → driver `AccessControlAPI.getCredentialCapabilitiesCached()`. The 0 is computed driver-side: UC branch returns `numberOfCredentialSlots: maxUsers` where `maxUsers = UserCodeCCValues.supportedUsers ?? 0`; U3C branch passes through stored per-type caps.\n- **PR #1252's bypass (call `node.access_control.set_credential` directly) does not unblock affected users**: the driver's `#assertValidSlot` (AccessControl.ts:1791) validates against the same cached caps inside `setCredential` (UC path line 1066, U3C line 1038) and `deleteCredential`. Affected locks get `ZWaveError: Credential slot N is out of range for credential type PINCode` → `FailedZWaveCommand` instead. The only write path that dodges the broken caps is the legacy User Code CC util (`zwave_js_server.util.lock.set_usercode` / `zwave_js.set_lock_usercode`, still present in HA).\n- Version matrix: HA 2026.6 […]

> TOOL

tool_result
id: toolu_0189fDmwv3rRogiiNNktDur5
```
File created successfully at: /home/<USER>/.claude/projects/-Users-raman-projects-lock-code-manager/memory/project_zwave_uc_zero_slots_root_cause.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_012uBZJ7g58WGSw43BLRyf2w
```json
{
  "command": "echo '- [Zwave UC zero-slots root cause (#1251)](project_zwave_uc_zero_slots_root_cause.md) — caps=0 is driver-side; PR #1252 bypass cannot fix writes (driver asserts same predicate)' >> /home/<USER>/.claude/projects/-Users-raman-projects-lock-code-manager/memory/MEMORY.md",
  "description": "Add memory index entry"
}
```

> TOOL

tool_result
id: toolu_012uBZJ7g58WGSw43BLRyf2w
```
(Bash completed with no output)
```

> AGENT

# Investigation report: "Credential slot for pin_code must be between 1 and 0"

## 1. Executive summary

- **The 0 is computed inside the node-zwave-js driver, not in HA.** Every layer above it (zwave-js-server, zwave-js-server-python, HA `lock_helpers`) is a faithful pass-through of `AccessControlAPI.getCredentialCapabilitiesCached()`. The literal error fires only when PIN_CODE **is present** in the capabilities map with `numberOfCredentialSlots == 0` — if PIN were missing entirely, HA would raise `credential_type_not_supported` instead. That single fact narrows the mechanism to two driver code paths.
- **PR [#1252](https://github.com/raman325/lock_code_manager/pull/1252)'s bypass does not fix affected users.** The driver's own `#assertValidSlot` (AccessControl.ts:1791 at `upstream/master`) enforces the *same predicate against the same cache* inside `setCredential` (UC path line 1066, U3C path line 1038) and `deleteCredential` (lines 1156, 1180). Bypassing HA's wrapper just trades `ServiceValidationError("between 1 and 0")` for `ZWaveError("Credential slot N is out of range for credential type PINCode")` surfaced as `FailedZWaveCommand`. The PR's capability-fallback half is still useful; the write half needs rework (see §5).
- **Version skew is ruled out as the mechanism.** HA 2026.6 pins `zwave-js-server-python==0.72.0` with `MIN=MAX_SERVER_SCHEMA_VERSION = 49` (`const/__init__.py:14-16` at tag 0.72.0), schema 49 ships only in @zwave-js/server 3.9.0, and the only zwave-js-ui release bundling it is 11.19.1 (driver 15.24.2). Anyone older […]
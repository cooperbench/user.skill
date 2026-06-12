---
name: scope-trim
description: Hayato immediately cuts out any feature or output the agent added that was not explicitly requested, with a single terse Japanese sentence stating what is NOT needed. Trigger when agent adds unrequested elements to its output or implementation.
---

## Behavior

When the agent adds something that wasn't asked for — a UI element, a config key with the wrong name, an unrequested behavior — Hayato sends a single Japanese sentence that names the unwanted thing and states it is unnecessary. He does not explain why. He does not soften the correction with praise.

Pattern: `[thing] は不要です` / `[thing] をするのは不要です` / specify exact name/section desired.

If the correction involves specifying the correct value (e.g., key name), he states the exact spec:
> `設定は \`ai\` セクションに \`ignore_auto_investigation_cmds\` という名称で設定したいです。`

## Verbatim examples

**Example 1** (banner scope creep):
```
Welcomeバナーにセッションキーの表示は不要です
```
(Agent had added session key display to the welcome banner; Hayato didn't ask for this)

**Example 2** (wrong config key name):
```
設定は `ai` セクションに `ignore_auto_investigation_cmds` という名称で設定したいです。
```
(Agent used a different key name; Hayato provides the exact spec)

**Example 3** (instrumentation cleanup after fix):
```
The issue has been fixed. Please clean up the instrumentation.
```
(After fix verified, tells agent to remove debug instrumentation — not part of original ask)

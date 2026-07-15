> DEVELOPER

If you look at https://github.com/moltis-org/moltis/issues/810#issuecomment-4293258745 user says it's still happening, which I don't understand since I had asked you to add a test to ensure it works.

> AGENT

Let me look at the issue and comment to understand what's being reported.

> TOOL

tool_use ToolSearch
id: toolu_01J47V521yH1FdHc2RaHxMT6
```json
{
  "query": "select:WebFetch",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_01J47V521yH1FdHc2RaHxMT6
```
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
```

> TOOL

tool_use Bash
id: toolu_01E8NHXyjHcyCk3yh9hLdAR3
```json
{
  "command": "gh issue view 810 --repo moltis-org/moltis --json title,body,comments --jq '{title: .title, body: .body, comments: [.comments[] | {author: .author.login, createdAt: .createdAt, body: .body}]}'",
  "description": "Fetch issue #810 with comments from GitHub"
}
```

> TOOL

tool_result
id: toolu_01E8NHXyjHcyCk3yh9hLdAR3
```
{"body":"### Preflight Checklist\n\n- [x] I have searched [existing issues](https://github.com/moltis-org/moltis/issues?q=is%3Aissue+label%3Abug) and this hasn't been reported yet\n- [x] I am using the latest version of Moltis\n- [x] If this happened during a chat session, I included as much full session context as possible and redacted secrets\n\n### What happened?\n\nWhen I send a message to Moltis and it is using Kimi K2.5 Turbo via Fireworks Fire Pass I get a 400 error response.\n\n### Expected behavior\n\nThe request should be made in the correct format so the server does not return the 400 error.\n\n### Steps to reproduce\n\n1. Set Moltis model to Kimi K2.5 Turbo via Fireworks Fire Pass.\n2. Send Moltis a message\n3. Confirm response code.\n\n### Did this happen during a chat session?\n\nNone\n\n### Chat session context (if applicable)\n\n```markdown\n\n```\n\n### Error messages / logs\n\n```shell\n\n```\n\n### Is this a regression?\n\nYes, this worked before\n\n### Last working version\n\n20260413.06\n\n### Moltis version\n\n20260420.02\n\n### Component\n\nAgent / LLM providers\n\n### Install method\n\nHomebrew\n\n### Operating system\n\nmacOS (Apple Silicon)\n\n### Additional context\n\n_No response_","comments":[{"author":"david-ros","body":"@penso I retested and this issue is still happening.","createdAt":"2026-04-22T03:07:31Z"}],"title":"[Bug]: 400 error response when using Moltis with Fireworks Fire Pass (Kimi K2.5 Turbo)"}
```

> TOOL

tool_use Bash
id: toolu_01ELmqoSxxp9Eh3gkHcMEZe8
```json
{
  "command": "gh issue view 810 --repo moltis-org/moltis --json labels --jq '.labels[].name'",
  "description": "Get issue labels"
}
```

> TOOL

tool_result
id: toolu_01ELmqoSxxp9Eh3gkHcMEZe8
```
bug
```

> TOOL

tool_use Bash
id: toolu_01BzZoPsQ6iqjiQDrcaDRkbc
```json
{
  "command": "git log --oneline --all --grep=\"810\" 2>/dev/null; git log --oneline --all --grep=\"fireworks\" -i 2>/dev/null; git log --oneline --all --grep=\"kimi\" -i 2>/dev/null; git log --oneline --all --grep=\"fire.pass\" -i 2>/dev/null",
  "description": "Search git history for related commits"
}
```

> TOOL

tool_result
id: toolu_01BzZoPsQ6iqjiQDrcaDRkbc
```
ae61de2d Finalize transcript for Checkpoint: e126277810b2
0f3d61ff Checkpoint: e126277810b2
c44e536d Checkpoint: 5eb5e38f13db
a6ef62e0 Merge origin/main into inexpensive-primrose
62628119 deploy: 62d05f15e613fd692d8887d8c8810d63a31b9587
4ff2cc6f deploy: 76860a82f14d1d8f6f3823f498aae781036af77e
0a2501b3 Finalize transcript for Checkpoint: ddf18105aa79
2c11be61 Checkpoint: ddf18105aa79
85537a70 feat(openclaw-import): convert non-default agents to spawn_agent presets
49682330 deploy: 98769897716a765eaef18106680757521ca55c6f
d0d0491a deploy: e611f64e3fef8106780be65277b9382521f6692e
eb68705a deploy: 46019f48f49f75ff6fed7eb7ed18100a95fbf3ad
04b7b9f1 fix(providers): disable strict tools for Fireworks Kimi router (#812)
1fe67def fix(providers): restore type annotations stripped by schema canonicalization
eee4fbf8 ci: add daily provider integration test workflow
0d98c2b0 test(providers): add Fireworks live API integration tests
d3e1a06a Merge pull request #497 from moltis-org/evanescent-bergamot
d8f518fd style(providers): address PR review for Fireworks provider
d3df8f2b feat(providers): add Fireworks.ai as primary provider
04b7b9f1 fix(providers): disable strict tools for Fireworks Kimi router (#812)
32d4bc1e Add Kimi K2.6 model to Moonshot and Kimi Code providers (#809)
f2764b3e test(providers): add Mistral, OpenRouter, and Kimi Code integration tests
4fe1eff6 test(providers): add Moonshot (Kimi) live API integration tests
6dd82f88 feat(providers): add Alibaba Cloud Coding Plan provider
d3df8f2b feat(providers): add Fireworks.ai as primary provider
2991e5bc fix(agents): sanitize model-mangled tool names from parallel calls
a5e7c116 feat(providers): Include reasoning fields for kimi models (#323)
58220f23 feat(providers): Include reasoning fields for kimi models (#323)
91b4a681 Replace RPC string dispatch with direct […]

> AGENT

The key commit is `04b7b9f1 fix(providers): disable strict tools for Fireworks Kimi router (#812)`. Let me look at that fix and understand what was done.

> TOOL

tool_use Bash
id: toolu_01CnnqF1FTWYDjW8f34fYs5v
```json
{
  "command": "git show 04b7b9f1 --stat",
  "description": "Show files changed in the fix commit"
}
```

> TOOL

tool_result
id: toolu_01CnnqF1FTWYDjW8f34fYs5v
```
commit 04b7b9f15f3020879d0148ebf4d8eea3bef8b889
Author: Fabien Penso <gpg@pen.so>
Date:   Mon Apr 20 22:53:25 2026 +0100

    fix(providers): disable strict tools for Fireworks Kimi router (#812)

 crates/providers/src/model_catalogs.rs          | 49 +++++++++++++
 crates/providers/src/openai/mod.rs              |  2 +
 crates/providers/src/openai/provider/core.rs    |  9 +++
 crates/providers/src/openai/provider/request.rs | 67 ++++++++++++++++++
 crates/providers/src/registry/registration.rs   | 14 ++++
 crates/providers/tests/fireworks_integration.rs | 93 +++++++++++++++++++++++++
 6 files changed, 234 insertions(+)
```

> TOOL

tool_use Bash
id: toolu_01Lei8n3zcNSP2t6aNZXB6yD
```json
{
  "command": "git log --oneline main..HEAD 2>/dev/null; echo \"---\"; git branch -a --contains 04b7b9f1 2>/dev/null | head -20",
  "description": "Check if the fix is on main and current branch"
}
```

> TOOL

tool_result
id: toolu_01Lei8n3zcNSP2t6aNZXB6yD
```
---
+ guiltless-wander
+ main
+ oxidized-foundation
* pointy-bike
+ precious-sunflower
+ shared-price
  remotes/origin/HEAD -> origin/main
  remotes/origin/guiltless-wander
  remotes/origin/main
  remotes/origin/similar-papyrus
```

> AGENT

The fix is on `main` and this branch. Let me look at the actual fix and the test to understand what was done, then check whether it actually addresses the 400 error.

> TOOL

tool_use Bash
id: toolu_01AZEDu2JSHBcWKugqRy61zX
```json
{
  "command": "git show 04b7b9f1 --no-stat -p",
  "description": "Show full diff of the fix commit"
}
```

> TOOL

tool_result ERROR
id: toolu_01AZEDu2JSHBcWKugqRy61zX
```
Exit code 128
fatal: unrecognized argument: --no-stat
```

> TOOL

tool_use Bash
id: toolu_01CZHkmPWH2YrfDcpGEJhSbL
```json
{
  "command": "git show 04b7b9f1 -p",
  "description": "Show full diff of the fix commit",
  "timeout": 15000
}
```

> TOOL

tool_result
id: toolu_01CZHkmPWH2YrfDcpGEJhSbL
```
commit 04b7b9f15f3020879d0148ebf4d8eea3bef8b889
Author: Fabien Penso <gpg@pen.so>
Date:   Mon Apr 20 22:53:25 2026 +0100

    fix(providers): disable strict tools for Fireworks Kimi router (#812)

diff --git a/crates/providers/src/model_catalogs.rs b/crates/providers/src/model_catalogs.rs
index ef477db9..14a7f269 100644
--- a/crates/providers/src/model_catalogs.rs
+++ b/crates/providers/src/model_catalogs.rs
@@ -58,6 +58,15 @@ pub(crate) const ZAI_MODELS: &[(&str, &str)] = &[
     ("glm-4-32b-0414-128k", "GLM-4 32B 128K"),
 ];
 
+/// Whether a model is a Fireworks Fire Pass router for Kimi/Moonshot.
+///
+/// These models proxy through Fireworks to Moonshot's Kimi API, which has
+/// different schema and message requirements (no strict tools, needs
+/// `reasoning_content`). Issue #810.
+pub(crate) fn is_fireworks_kimi_router(def: &OpenAiCompatDef, model_id: &str) -> bool {
+    def.config_name == "fireworks" && model_id.contains("/routers/") && model_id.contains("kimi")
+}
+
 /// Known Fireworks models.
 pub(crate) const FIREWORKS_MODELS: &[(&str, &str)] = &[
     (
@@ -438,4 +447,44 @@ mod tests {
             ollama.default_base_url,
         );
     }
+
+    #[test]
+    fn is_fireworks_kimi_router_detects_router_model() {
+        let fireworks = OPENAI_COMPAT_PROVIDERS
+            .iter()
+            .find(|d| d.config_name == "fireworks")
+            .expect("fireworks entry must exist");
+        assert!(is_fireworks_kimi_router(
+            fireworks,
+            "accounts/fireworks/routers/kimi-k2p5-turbo"
+        ));
+    }
+
+    #[test]
+    fn is_fireworks_kimi_router_rejects_native_model() {
+        let fireworks = OPENAI_COMPAT_PROVIDERS
+            .iter()
+            .find(|d| d.config_name == "fireworks")
+            .expect("fireworks entry must exist");
+        assert!(!is_fireworks_kimi_router(
+            fireworks,
+            "accounts/fireworks/models/deepseek-v3p2"
+        ));
+ […]

> AGENT

Now let me check if the fix is actually in the latest release the user is running. The user said they're on `20260420.02` and the issue was first reported. Let me check the commit dates and releases.

> TOOL

tool_use Bash
id: toolu_01P8TFRFwAnjH1uVdctpLpSX
```json
{
  "command": "git log --oneline --format=\"%h %ci %s\" 04b7b9f1 -1",
  "description": "Check commit date of the fix"
}
```

> TOOL

tool_result
id: toolu_01P8TFRFwAnjH1uVdctpLpSX
```
04b7b9f1 2026-04-20 22:53:25 +0100 fix(providers): disable strict tools for Fireworks Kimi router (#812)
```

> TOOL

tool_use Bash
id: toolu_01CRRnLjTrSoKKApAfWHm9WJ
```json
{
  "command": "git tag --sort=-creatordate | head -10",
  "description": "List recent tags to see releases"
}
```

> TOOL

tool_result
id: toolu_01CRRnLjTrSoKKApAfWHm9WJ
```
20260421.05
20260421.04
20260421.03
20260421.02
20260421.01
20260420.02
20260420.01
20260419.01
20260417.02
20260417.01
```

> TOOL

tool_use Bash
id: toolu_01Hz8PRGisFtgyuMrqE9DaDj
```json
{
  "command": "git log --oneline 20260420.02..20260421.01 | head -20",
  "description": "Check what's between the user's version and the next release"
}
```

> TOOL

tool_use Bash
id: toolu_01YcKg72CfG2NGK9wyZnWZqW
```json
{
  "command": "git tag --contains 04b7b9f1 | head -5",
  "description": "Which releases contain the fix commit"
}
```

> TOOL

tool_result
id: toolu_01Hz8PRGisFtgyuMrqE9DaDj
```
8ad3349a chore: prepare release 20260421.01
b4241798 fix(ci): pass safe.directory to gix via env vars in rust-ci container
d58289fa fix(ci): npm --ignore-scripts and git install ordering
7cc84596 style: rustfmt model_catalogs.rs
2054833d feat(skills): bundle 101 default skills with category UI and format fallback (#797)
04b7b9f1 fix(providers): disable strict tools for Fireworks Kimi router (#812)
a6b89853 fix(sandbox): verify image in Podman store after BuildKit build (#811)
32d4bc1e Add Kimi K2.6 model to Moonshot and Kimi Code providers (#809)
69fd2ff1 feat(web): render markdown as HTML in chat messages (#808)
7ea44ed6 feat(sandbox): install Node.js 22 LTS via NodeSource (#807)
50f2733c refactor(tools): split skill_tools.rs into submodules
ca071e4e chore(web): add @biomejs/biome 2.4.6 as devDependency
7fbb8e82 fix(ci): biome formatting and file size allowlist
723a893e chore(web): rebuild Tailwind output
582d969e feat(web): add GitHub Issues and Discussions links with count badges (#806)
b975c61d feat: self-improving agent loop — skills, memory lifecycle, deployment (#803)
3e56db20 fix(mcp): implement legacy SSE transport for endpoint discovery (#805)
01116771 fix(slack): strip leading slash from commands before gateway dispatch (#804)
b54a1895 feat: Gemini thought_signature round-tripping and schema validation fixes (#795)
034ed3fa feat(channels): centralized command registry for all channels (#794)
```

> TOOL

tool_result
id: toolu_01YcKg72CfG2NGK9wyZnWZqW
```
20260421.01
20260421.02
20260421.03
20260421.04
20260421.05
```

> AGENT

The fix is in `20260421.01` and later. The user reported the bug on version `20260420.02`, and the comment saying "still happening" was posted on April 22. Let me check if there's something the fix might have missed.

> TOOL

tool_use Agent
id: toolu_01PqwoFyjoRwW1AdzNWM6mXZ
```json
{
  "description": "Investigate Fireworks Kimi 400 bug",
  "prompt": "I need to investigate why issue #810 (400 error with Fireworks Fire Pass Kimi K2.5 Turbo) might still be happening after the fix in commit 04b7b9f1.\n\nThe fix:\n1. Added `is_fireworks_kimi_router()` detection in `model_catalogs.rs` - checks `config_name == \"fireworks\"` AND `model_id.contains(\"/routers/\")` AND `model_id.contains(\"kimi\")`\n2. In `registration.rs`, when `is_fireworks_kimi_router()` matches, sets `strict_tools(false)` and `reasoning_content(true)`\n3. Added `reasoning_content_override` field to `OpenAiProvider`\n\nPlease investigate:\n1. Read `crates/providers/src/registry/registration.rs` around line 948+ to see the full registration flow for OpenAI-compat providers, especially how the model_id is constructed. Is it possible the model_id doesn't match the pattern?\n2. Read `crates/providers/src/model_catalogs.rs` to check what model IDs are defined for Fireworks models - specifically the Kimi router models. Do the catalog entries use the full `accounts/fireworks/routers/kimi-k2p5-turbo` format?\n3. Check if there's a code path where the model could be registered WITHOUT going through the `is_fireworks_kimi_router` check (e.g., user-defined models, BYOM, or a different registration path).\n4. Check the `needs_strict_tools()` method - does it have any override logic that could re-enable strict tools?\n5. Check how `reasoning_content` is actually serialized in the request body for tool-call messages - is the override properly wired through?\n\nThis is a research task - do NOT write any code. Just report […]

> TOOL

tool_result
id: toolu_01PqwoFyjoRwW1AdzNWM6mXZ
```
Excellent! The fix is there at lines 954-963. Now I have all the information I need. Let me create my final report.

## Investigation Report: Issue #810 - Fireworks Fire Pass Kimi K2.5 Turbo 400 Error

### Summary
The fix for issue #810 (commit 04b7b9f1) has been correctly implemented in the current codebase. However, I identified **one significant gap** that could explain why the issue might still occur in certain scenarios.

---

### Findings

#### 1. **Fix Implementation: CORRECT**
The primary fix is correctly in place in `register_openai_compatible_providers()` (lines 954-963 in registration.rs):
- Detection function `is_fireworks_kimi_router()` correctly identifies routers: checks for `config_name == "fireworks"` AND `model_id.contains("/routers/")` AND `model_id.contains("kimi")`
- Model ID in catalog is correct: `"accounts/fireworks/routers/kimi-k2p5-turbo"` (model_catalogs.rs line 73)
- Settings are properly applied:
  - `with_strict_tools(false)` (line 960) - only if user didn't explicitly set it
  - `with_reasoning_content(true)` (line 962) - always enabled

#### 2. **Settings Propagation: CORRECT**
- `reasoning_content_override` field exists in `OpenAiProvider` struct (mod.rs line 31)
- `with_reasoning_content()` method exists and sets the override (provider/core.rs lines 99-102)
- Override is properly checked in `requires_reasoning_content_on_tool_messages()` (request.rs lines 112-114)
- `reasoning_content` is correctly serialized into request body for assistant messages with tool calls (request.rs lines 310-333) […]

> AGENT

Let me verify one more thing about the integration tests.

> TOOL

tool_use Read
id: toolu_01Dmxj6PSSTntUywqpWFhu58
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/pointy-bike/crates/providers/tests/fireworks_integration.rs",
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01Dmxj6PSSTntUywqpWFhu58
```
     1→//! Live integration tests for the Fireworks provider.
     2→//!
     3→//! These tests hit the real Fireworks API and require `FIREWORKS_API_KEY` in
     4→//! the environment. They are `#[ignore]`d by default so `cargo test` skips them.
     5→//!
     6→//! Run with:
     7→//!   cargo test --test fireworks_integration -- --ignored
     8→
     9→#![allow(clippy::unwrap_used, clippy::expect_used)]
    10→
    11→use std::collections::HashSet;
    12→
    13→use {
    14→    futures::StreamExt,
    15→    moltis_agents::model::{ChatMessage, LlmProvider, StreamEvent, ToolCall},
    16→    moltis_providers::openai::OpenAiProvider,
    17→    secrecy::{ExposeSecret, Secret},
    18→};
    19→
    20→const FIREWORKS_BASE_URL: &str = "https://api.fireworks.ai/inference/v1";
    21→const TEST_MODEL: &str = "accounts/fireworks/models/deepseek-v3p2";
    22→
    23→/// Known Fireworks models we catalog. Keep in sync with `FIREWORKS_MODELS` in
    24→/// `crates/providers/src/lib.rs`.
    25→const KNOWN_MODELS: &[&str] = &[
    26→    "accounts/fireworks/routers/kimi-k2p5-turbo",
    27→    "accounts/fireworks/models/deepseek-v3p2",
    28→    "accounts/fireworks/models/qwen3-235b-a22b-instruct-2507",
    29→    "accounts/fireworks/models/llama-v3p1-405b-instruct",
    30→    "accounts/fireworks/models/llama-v3p1-70b-instruct",
```

> TOOL

tool_use Grep
id: toolu_01WqkH1q5GHZdrmZxBj3RPWy
```json
{
  "pattern": "fn make_provider",
  "path": "/Users/penso/.superset/worktrees/moltis/pointy-bike/crates/providers/tests/fireworks_integration.rs",
  "output_mode": "content",
  "-A": 15
}
```

> TOOL

tool_result
id: toolu_01WqkH1q5GHZdrmZxBj3RPWy
```
41:fn make_provider(model: &str) -> OpenAiProvider {
42-    OpenAiProvider::new_with_name(
43-        api_key(),
44-        model.to_string(),
45-        FIREWORKS_BASE_URL.to_string(),
46-        "fireworks".to_string(),
47-    )
48-}
49-
50-/// Tool schema in moltis-internal flat format.
51-fn weather_tool() -> serde_json::Value {
52-    serde_json::json!({
53-        "name": "get_weather",
54-        "description": "Get current weather for a location. You MUST call this tool when asked about weather.",
55-        "parameters": {
56-            "type": "object",
```

> AGENT

Now I see the full picture. Here's what's going on:

**The most likely explanation is that the user hasn't updated.** The fix landed in version `20260421.01`, but the user reported the bug on `20260420.02`. Their comment "still happening" was posted April 22 at 03:07 UTC — they likely retested on the same version without upgrading.

That said, the investigation did find a real gap: **the integration tests don't actually test the fix path**. `make_provider()` constructs an `OpenAiProvider` directly without calling `.with_strict_tools(false)` or `.with_reasoning_content(true)`, meaning:

1. `kimi_router_tool_call_no_400` — if it passes, it's because Kimi happened to accept the request, not because strict tools were disabled
2. `kimi_router_multi_turn_tool_use` — if it passes without `reasoning_content`, it means the test isn't validating what the fix does

The tests verify the Kimi model works in general, but they don't verify that the **registration path** correctly applies the overrides. If Fireworks/Moonshot ever started rejecting those fields, the tests would fail for the wrong reason.

**What to tell the user on the issue:** They need to update to at least `20260421.01` (latest is `20260421.05`). The fix for #810 was merged after `20260420.02`.

**Separately**, want me to fix the integration tests so `make_provider()` for the Kimi router model […]

> AGENT

Those background test runs got killed — not important, the unit tests all pass (they're just detection logic tests).

To summarize my findings:

**The user likely hasn't updated.** The fix (PR #812) shipped in `20260421.01`. They reported on `20260420.02`, and their "still happening" comment was April 22 — they probably retested the same version.

**There is also a real gap in the integration tests.** `make_provider()` constructs the `OpenAiProvider` directly without applying `.with_strict_tools(false)` or `.with_reasoning_content(true)`. So the `kimi_router_tool_call_no_400` and `kimi_router_multi_turn_tool_use` tests don't actually validate the fix — they just test whether Kimi happens to accept the request regardless.

Two things to do:
1. **Reply on the issue** asking the user to confirm their version (`moltis --version`) and update to `20260421.05`
2. **Fix the integration tests** so `make_provider()` applies the Kimi router overrides, actually testing the fix path

Want me to do both?
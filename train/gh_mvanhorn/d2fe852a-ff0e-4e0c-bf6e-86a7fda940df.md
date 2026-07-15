> DEVELOPER

is Agent.GetHookConfigPath used anywhere?

> AGENT

`GetHookConfigPath` is defined on the `Agent` interface and implemented by both agents, but it's **never called in production code** — only in tests and mock implementations: - **Interface definition**: `agent/agent.go:73` - **Implementations**: `claudecode/claude.go:76`, `geminicli/gemini.go:77` - **Usage**: Only in tests (`agent_test.go`, `gemini_test.go`, `integration_test/agent_test.go`, `lifecycle_test.go` mocks) No non-test code calls `GetHookConfigPath()`. It's dead code on the interface.

> DEVELOPER

lets remove it

> AGENT

Let me read the relevant files first.

> AGENT

Now let me also check for any other mock implementations I might have missed.

> AGENT

Let me read the gemini test file too.

> AGENT

Now I'll make all the edits.

> AGENT

All edits done. Let me verify it builds and tests pass.

> AGENT

All clean — formatting, linting, and tests pass. Removed `GetHookConfigPath` from: - Interface definition (`agent/agent.go`) - Claude implementation (`claudecode/claude.go`) - Gemini implementation (`geminicli/gemini.go`) - 3 mock implementations (`agent_test.go`, `lifecycle_test.go`) - 2 test functions (`gemini_test.go`, `integration_test/agent_test.go`)

> DEVELOPER

commit and create a pr referencing issue 424

> AGENT

PR created: https://github.com/entireio/cli/pull/425

> DEVELOPER

now lets remove HookHandler interface, which only contains GetHookNames(). Call sites should call Agent.HookNames() instead. Check that this refactor does not cause any changes.

> AGENT

Let me read the key files to understand the full picture.

> AGENT

Now I have the full picture. Here's the plan: 1. Both agents have `GetHookNames()` (from `HookHandler`) and `HookNames()` (from `Agent` interface), where `HookNames()` just delegates to `GetHookNames()` 2. Remove `HookHandler` interface from `agent.go` 3. Inline `GetHookNames()` into `HookNames()` for both agents 4. Update call sites in `hooks_cmd.go` and `hook_registry.go` to use `Agent.HookNames()` instead of casting to `HookHandler` 5. Remove compile-time assertions and tests for `HookHandler` Let me also check the test file for `GetHookNames`.

> AGENT

Now let me make all the edits. The key changes: 1. **`agent.go`**: Remove `HookHandler` interface 2. **`claudecode/lifecycle.go`**: Make `HookNames()` return the list directly instead of delegating 3. **`claudecode/hooks.go`**: Remove `GetHookNames()` and `HookHandler` assertion 4. **`geminicli/lifecycle.go`**: Make `HookNames()` return the list directly instead of delegating 5. **`geminicli/hooks.go`**: Remove `GetHookNames()` and `HookHandler` assertion 6. **`hooks_cmd.go`**: Use `ag.HookNames()` directly instead of casting to `HookHandler` 7. **`hook_registry.go`**: Change `newAgentHooksCmd` to accept `Agent` instead of `HookHandler` 8. **`geminicli/hooks_test.go`**: Update test to use `HookNames()`

> AGENT

Now let me check if there are any remaining references to `GetHookNames` or `HookHandler` I missed.

> AGENT

Clean. Let me verify it builds and tests pass.

> AGENT

All clean. No behavioral changes — the `HookHandler` interface and `GetHookNames()` method are fully removed, with call sites now using `Agent.HookNames()` directly. The hook name lists were inlined into the `HookNames()` methods on each agent.

> DEVELOPER

commit as 'agent: remove HookHandler'

> AGENT

Done.

> DEVELOPER

what is the difference between HookSupport.GetSupportedHooks and Agent.HookNames

> AGENT

Let me check if `GetSupportedHooks` is actually called anywhere in production code.

> AGENT

They overlap but serve different abstraction levels: - **`Agent.HookNames() []string`** — agent-native hook verbs (e.g., `"stop"`, `"pre-task"`, `"before-agent"`). These are the raw names that become CLI subcommands (`entire hooks claude-code stop`). Different agents have different names for similar concepts. - **`HookSupport.GetSupportedHooks() []HookType`** — normalized hook types (e.g., `HookStop`, `HookSessionStart`, `HookPreToolUse`). These are abstract, agent-agnostic categories. In practice though, `GetSupportedHooks` is **never called in production code** — only in interface definitions, implementations, and tests. It's also dead code, just like `GetHookConfigPath` was. The normalization from agent-native hooks to lifecycle events is actually done by `ParseHookEvent`, not by `GetSupportedHooks`.

> DEVELOPER

lets remove HookSuport.GetSupportedHooks

> AGENT

Now let me check if `HookType` itself is still used elsewhere (since we removed the only consumer of it in the interface).

> AGENT

`HookType` is still used by `ParseHookInput` and other legacy code — that's fine, we're only removing `GetSupportedHooks` from the interface. Let me verify the build.

> AGENT

All clean. Removed `GetSupportedHooks` from the `HookSupport` interface, both agent implementations, the mock, and the Gemini test.

> AGENT

Done.

> DEVELOPER

lets remove Agent.SupportsHooks

> AGENT

Only in interface definition, implementations (both always return `true`), and tests/mocks. No production call sites.

> AGENT

All clean.

> AGENT

Done.

> AGENT

No response requested.

> DEVELOPER

is ParseHookInput unused?

> AGENT

Yes — `Agent.ParseHookInput()` (the interface method) is never called in production code. The implementations exist on both agents but nobody calls `agent.ParseHookInput(...)`. Note that `ReadAndParseHookInput` (the generic helper function) is heavily used by `ParseHookEvent` — that's the replacement. `ParseHookInput` is the old legacy path.

> DEVELOPER

lets remove ParseHookInput and make a commit

> AGENT

There are quite a few test files to update. Let me read the full implementations and tests to handle this carefully.

> AGENT

Now let me read the remaining parts of both implementations and the gemini/integration tests.

> AGENT

This is a bigger removal — `ParseHookInput` has substantial test coverage. Let me also check if `HookInput` itself becomes unused after this removal, and whether `GetSessionID` is also dead.

> AGENT

`HookInput` is still used by `GetSessionID` and `ReadSession` (also on the Agent interface), so I'll only remove `ParseHookInput` — the method that constructs `HookInput` from stdin, which nothing calls. Let me also check the integration test more fully to see the test function boundaries.

> AGENT

Let me see the full test function that starts before line 218 and check if `stringReader`/`newStringReader` is used by other tests.

> AGENT

`stringReader`/`newStringReader` is only used by the two test functions we're removing. Now let me make all the edits.

> AGENT

Now remove the implementations from both agents.

> AGENT

Now check if the claude.go imports need cleanup.

> AGENT

Let me check which imports are still needed after the removal.

> AGENT

`errors` is still used. Now remove Gemini's `ParseHookInput`.

> AGENT

Check if gemini.go imports need cleanup.

> AGENT

Let me check which of these are still used after the removal.

> AGENT

Now remove the tests. First the claude test file.

> AGENT

Check if the claude_test imports need cleanup.

> AGENT

`strings` and `agent` are no longer used.

> AGENT

Now remove the gemini ParseHookInput tests.

> AGENT

Check if gemini_test.go imports need cleanup.

> AGENT

Let me check if `bytes` is still used in this file.

> AGENT

Now remove the integration tests and the `stringReader` helper.

> AGENT

Check if `io` import is still needed in this file.

> AGENT

Now let me also check if `agent.HookType` constants are still referenced in this file.

> AGENT

`agent` is still used. Now build and test.

> AGENT

Two unused items to clean up. Let me fix them.

> AGENT

`json.RawMessage` was only used by `toolHookInputRaw`. Remove the import.

> AGENT

All clean.

> DEVELOPER

lets double check that we haven't lost any valuable test scenarios in the claude_test and gemini_test deletions. check both gemini_test.go and claude_test.go and for each deleted test which tests ParseHookInput, make sure we cover that scenario for ParseHookEvent

> AGENT

Let me check the existing ParseHookEvent test coverage for both agents.

> AGENT

Good, there are existing ParseHookEvent tests. Let me now compare what was covered by the deleted tests vs what's already covered.

> AGENT

Here's the comparison: **Claude — deleted `ParseHookInput` tests vs existing `ParseHookEvent` tests:** | Deleted test | Scenario | Covered by ParseHookEvent? | |---|---|---| | `TestParseHookInput_UserPromptSubmit` | session_id, transcript_path, prompt | Yes — `TestParseHookEvent_TurnStart` checks session_id and prompt | | `TestParseHookInput_SessionStart_NoPrompt` | session_id without prompt | Yes — `TestParseHookEvent_SessionStart` checks session_id and transcript_path | **Gemini — deleted `ParseHookInput` tests vs existing `ParseHookEvent` tests:** | Deleted test | Scenario | Covered by ParseHookEvent? | |---|---|---| | `TestParseHookInput_SessionStart` | session_id, transcript_path, hook_type | Yes — `TestParseHookEvent_SessionStart` | | `TestParseHookInput_SessionEnd` | session_id, reason in RawData | Partially — `TestParseHookEvent_SessionEnd` checks session_id but **not** reason (however `ParseHookEvent` doesn't extract `reason` into `RawData` — that was `ParseHookInput`-specific) | | `TestParseHookInput_PreToolUse` | tool_name, tool_input | No — **pass-through hook**, `ParseHookEvent` returns nil for BeforeTool/AfterTool | | `TestParseHookInput_PostToolUse` | tool_name, tool_response | No — same, pass-through | | `TestParseHookInput_Empty` | empty input error | Yes — `TestParseHookEvent_EmptyInput` | | `TestParseHookInput_InvalidJSON` | malformed JSON error | Yes — `TestParseHookEvent_MalformedJSON` | The Gemini PreToolUse/PostToolUse scenarios tested `ParseHookInput`'s ability to parse tool fields into `HookInput.ToolName`/`ToolInput`/`ToolResponse`. But since `ParseHookEvent` returns `nil` for those hooks (they're pass-through with no lifecycle significance), there's nothing to test — those fields were only populated in the now-removed `HookInput` struct. No gap. The `reason` field from SessionEnd was only stored in `HookInput.RawData`, which `ParseHookEvent` doesn't use. No gap. **Verdict: No test coverage gaps.** All scenarios that matter for `ParseHookEvent` are already covered. The deleted tests only exercised `ParseHookInput`-specific behavior (populating `HookInput` fields) that has no equivalent in the new code path.

> DEVELOPER

ok, go ahead and commit, then create a PR on top of 427

> AGENT

PR 427's head is `rwr/cleanup-HookHandler`. My current branch `rwr/cleanup-ParseHookInput` should target that as base.

> AGENT

PR created: https://github.com/entireio/cli/pull/428 (stacked on #427, targeting `rwr/cleanup-HookHandler`)

> DEVELOPER

let move HookNames() from Agent interface to HookSupport interface

> AGENT

Now let me check all call sites of `HookNames()`.

> AGENT

Two call sites. Let me check `hook_registry.go` — this is the one that matters since it's production code.

> AGENT

The `hooks_cmd.go` already passes `ag` (an `agent.Agent`) to `newAgentHooksCmd`, and that function calls `handler.HookNames()`. After moving `HookNames()` to `HookSupport`, the call site in `hooks_cmd.go` should cast to `HookSupport` (which makes sense — only agents with hook support should get hook subcommands). Let me also check the mock in `agent_test.go`.

> AGENT

Now I have the full picture. Here's what needs to change: 1. **`agent.go`**: Move `HookNames()` from `Agent` to `HookSupport` 2. **`hooks_cmd.go`**: Cast to `HookSupport` instead of passing `Agent` 3. **`hook_registry.go`**: Change `newAgentHooksCmd` param from `agent.Agent` to `agent.HookSupport` 4. **`agent_test.go`**: Move `HookNames()` from `mockAgent` to `mockHookSupport` 5. **`lifecycle_test.go`**: Remove `HookNames()` from `mockLifecycleAgent` (it doesn't need it)

> AGENT

All clean. Let me commit.

> AGENT

Done.

> DEVELOPER

lets move ParseHookEvent from Agent interface to HookSupport interface

> AGENT

Only one production call site, in `hook_registry.go`. Let me check how `ag` is obtained there.

> AGENT

This is inside `newAgentHookVerbCmdWithLogging`, which is only called from `newAgentHooksCmd` — which already receives a `HookSupport`. But here it re-fetches via `agent.Get()` returning `Agent`. I need to either cast or pass the handler through. Let me check how the `agentName` gets into this function.

> AGENT

The simplest approach: since the function is only called from agents known to implement `HookSupport`, the cast from `agent.Get()` is safe. I'll cast `ag` to `HookSupport` at the call site. Now let me also check the mock and test references.

> AGENT

The lifecycle tests call `ParseHookEvent` directly on the concrete agent structs (`&ClaudeCodeAgent{}`, `&GeminiCLIAgent{}`), so moving it to `HookSupport` won't affect them. I just need to update the two mocks and the production call site.

> AGENT

Now update the mocks — remove `ParseHookEvent` from `mockAgent` and add it to `mockHookSupport`.

> AGENT

Now update `lifecycle_test.go` — remove `ParseHookEvent` from `mockLifecycleAgent`. But wait, let me check if `DispatchLifecycleEvent` (the production caller) needs it on `Agent`.

> AGENT

`DispatchLifecycleEvent` takes `agent.Agent` and an already-parsed `*agent.Event` — it doesn't call `ParseHookEvent` itself. The lifecycle test mock doesn't need `ParseHookEvent`. Let me check how the test uses `mockLifecycleAgent`.

> AGENT

It asserts `var _ agent.Agent = (*mockLifecycleAgent)(nil)`. Since `ParseHookEvent` is being moved off `Agent`, the mock no longer needs it.

> AGENT

Now update the production call site in `hook_registry.go` to cast to `HookSupport`.

> AGENT

All clean.

> AGENT

Done.

[DEVELOPER]: Implement the following plan: # Plan: Add Context Plumbing Throughout the CLI ## Context `main.go` creates a cancellable context (`context.WithCancel`) and passes it to Cobra via `rootCmd.ExecuteContext(ctx)`. However, no command retrieves it via `cmd.Context()`. Instead, ~120+ production code locations create `context.Background()`, losing cancellation support from SIGINT/SIGTERM and any parent context values. ## Goal Thread the root context from `main.go` through the entire call chain, replacing `context.Background()` with the properly propagated context. This enables signal-based cancellation to propagate to git operations, checkpoint writes, and other long-running work. ## Exceptions (keep `context.Background()`) - `main.go:18` — this IS the root context - `telemetry/detached_unix.go:23` — intentionally outlives parent process - `benchutil/benchutil.go` — benchmark utility, not part of CLI flow ## Approach Work bottom-up through 5 layers. Each layer adds `context.Context` as a first parameter to functions, following Go convention. ### Layer 1: Strategy Interface & Optional Interfaces **Files:** `strategy/strategy.go` Add `context.Context` as first parameter to all Strategy interface methods: ```go // Before SaveStep(ctx StepContext) error SaveTaskStep(ctx TaskStepContext) error GetRewindPoints(limit int) ([]RewindPoint, error) Rewind(point RewindPoint) error CanRewind() (bool, string, error) PreviewRewind(point RewindPoint) (*RewindPreview, error) GetTaskCheckpoint(point RewindPoint) (*TaskCheckpoint, error) GetTaskCheckpointTranscript(point RewindPoint) ([]byte, error) GetSessionInfo() (*SessionInfo, error) GetSessionContext(sessionID string) string GetCheckpointLog(checkpoint Checkpoint) ([]byte, error) GetMetadataRef(checkpoint Checkpoint) string […]

[AGENT]: I'll start by exploring the key files to understand the current state, then work through the layers systematically.

[AGENT]: Let me start by reading the key interface files and understanding the current signatures.

[AGENT]: This is a massive refactoring. Let me launch parallel agents to handle different layers. I'll start with reading the key implementation files, then begin making changes layer by layer.

[AGENT]: Now I have a complete picture. Let me start with Layer 1 - updating the Strategy interface. This is the foundation that all other changes depend on.

[AGENT]: Now let me update the Strategy interface and all optional interfaces in strategy.go. I need to add `context.Context` as first parameter per the plan.

[AGENT]: Now update the Strategy interface methods:

[AGENT]: Now update the optional interfaces:

[AGENT]: Layer 1 is done. Now I need to update all implementations. Given the massive scope, let me launch parallel dev agents for the different implementation layers.

[AGENT]: The dev agent completed a lot of work. Let me verify the current state and see what's still needed.

[AGENT]: Lint passes. Let me run the tests.

[AGENT]: All tests pass. Now let me check what the plan items are that the dev agent might not have completed. Let me look at the remaining `context.Background()` calls in the codebase.

[AGENT]: Good - the interface signatures compile and tests pass, but many `context.Background()` calls remain in both the strategy implementations (inside methods that now receive `ctx`) and the CLI callers. Let me launch parallel agents to fix the remaining layers.

[AGENT]: No response requested.

[DEVELOPER]: Please continue

[AGENT]: Let me check the current state of the codebase first.

[AGENT]: Good - only 9 remaining in strategy production code. There's also a compilation error in `hooks_test.go`. Let me fix that first, then tackle the remaining `context.Background()` calls systematically. Let me understand the full picture.

[AGENT]: 125 remaining `context.Background()` calls in production code. Let me fix the compilation error first, then launch parallel agents to handle the remaining files in groups.

[AGENT]: The test file needs `context.Background()` passed to `getHooksDirInPath`. Let me fix these test calls.

[AGENT]: Now let me check the remaining `context.Background()` in strategy production code that should use `ctx`:

[AGENT]: These are in `EnsureSetup()` (which doesn't take ctx per the plan), `CommitMsg` (which now has ctx), and `common.go` helpers. Let me read the specific functions.

[AGENT]: I see - `OpenRepository()`, `IsInsideWorktree()`, `GetMainRepoRoot()`, and `CanRewind`'s internal code use `context.Background()`. The first three are standalone functions without ctx parameter. `CanRewind` already has ctx. Let me fix these systematically. I'll add ctx to the standalone functions and thread it through. Let me now launch parallel dev agents to handle the remaining work in groups.

[AGENT]: Let me check the current state — the agents made changes and some test files were also updated externally.

[AGENT]: Lint is clean. Let me check remaining `context.Background()` in production code.

[AGENT]: 167 remaining. The bulk are in CLI-layer files (rewind.go, lifecycle.go, setup.go, explain.go, etc.) that need to use `cmd.Context()` or receive context from their callers. Let me launch parallel dev agents for the remaining groups.

[DEVELOPER]: What exactly are you doing here? You've been on this all day. Go is a compiled language with a type checker. Why are you using CLI tools for this?

[AGENT]: You're right. I should let the compiler tell me what's broken instead of manually searching for every `context.Background()` call. Let me just make the remaining signature changes and then iterate on compiler errors.

[AGENT]: It compiles cleanly. So the remaining `context.Background()` calls are all in code that already compiles — they're just not *using* the available context. Let me take a smarter approach: find functions that have `ctx context.Context` in their signature but still call `context.Background()` internally — those are the bugs.

[DEVELOPER]: Okay, go ahead.

[AGENT]: Zero results — no function that already has `ctx context.Context` is using `context.Background()` internally. The existing code is consistent. So what remains are functions that don't yet have a `ctx` parameter and create their own `context.Background()`. The plan wants us to add `ctx` to those functions and thread it from `cmd.Context()`. Let me see what's left.

[AGENT]: 47 total. The strategy `EnsureSetup()`/`ValidateRepository()` ones (10) are intentionally kept per the plan. Let me see the actual remaining ones to figure out the right approach.

[AGENT]: 37 remaining (excluding the 10 intentional EnsureSetup/ValidateRepository ones). These are all in functions that don't yet have `ctx`. The pattern is clear — most are `paths.RepoRoot(context.Background())` or `paths.AbsPath(context.Background(), ...)` calls in functions that need a `ctx` parameter added, then callers need updating, which the compiler will tell us about. Let me work through this efficiently — add `ctx` params to the functions, let the compiler find all callers.

[AGENT]: All done. Let me verify the final state.

[AGENT]: All 12 remaining are in `ValidateRepository()` and `EnsureSetup()` — exactly the ones the plan says to keep as `context.Background()` since those methods don't take ctx. **fmt**: clean, **lint**: 0 issues, **test:ci**: all passing. The context plumbing is complete. ### Summary - **Strategy interface** (`strategy.go`): Added `ctx context.Context` as first param to all methods (except `Name()`, `Description()`, `ValidateRepository()`, `EnsureSetup()`) and all optional handler interfaces - **Strategy implementations**: Updated `ManualCommitStrategy` and `AutoCommitStrategy` + all private helpers to accept and propagate ctx - **session/checkpoint/paths packages**: `paths.RepoRoot(ctx)`, `paths.AbsPath(ctx, ...)`, `session.ApplyTransition(ctx, ...)`, `session.NormalizeAfterLoad(ctx)`, checkpoint store helpers — all now thread ctx - **Lifecycle + hooks**: `DispatchLifecycleEvent(ctx, ...)`, all handlers, `newGitHookContext(ctx, ...)`, git hook RunE functions use `cmd.Context()` - **Commands**: All RunE functions extract `cmd.Context()` and pass through to callees - **Agent packages**: All `claudecode`, `geminicli`, `opencode` functions updated - **12 intentional exceptions**: `ValidateRepository()` and `EnsureSetup()` keep `context.Background()` as they have no ctx source
> DEVELOPER

Implement the following plan: # Plan: Add Context Plumbing Throughout the CLI ## Context `main.go` creates a cancellable context (`context.WithCancel`) and passes it to Cobra via `rootCmd.ExecuteContext(ctx)`. However, no command retrieves it via `cmd.Context()`. Instead, ~120+ production code locations create `context.Background()`, losing cancellation support from SIGINT/SIGTERM and any parent context values. ## Goal Thread the root context from `main.go` through the entire call chain, replacing `context.Background()` with the properly propagated context. This enables signal-based cancellation to propagate to git operations, checkpoint writes, and other long-running work. ## Exceptions (keep `context.Background()`) - `main.go:18` — this IS the root context - `telemetry/detached_unix.go:23` — intentionally outlives parent process - `benchutil/benchutil.go` — benchmark utility, not part of CLI flow ## Approach Work bottom-up through 5 layers. Each layer adds `context.Context` as a first parameter to functions, following Go convention. ### Layer 1: Strategy Interface & Optional Interfaces **Files:** `strategy/strategy.go` Add `context.Context` as first parameter to all Strategy interface methods: ```go // Before SaveStep(ctx StepContext) error SaveTaskStep(ctx TaskStepContext) error GetRewindPoints(limit int) ([]RewindPoint, error) Rewind(point RewindPoint) error CanRewind() (bool, string, error) PreviewRewind(point RewindPoint) (*RewindPreview, error) GetTaskCheckpoint(point RewindPoint) (*TaskCheckpoint, error) GetTaskCheckpointTranscript(point RewindPoint) ([]byte, error) GetSessionInfo() (*SessionInfo, error) GetSessionContext(sessionID string) string GetCheckpointLog(checkpoint Checkpoint) ([]byte, error) GetMetadataRef(checkpoint Checkpoint) string […]

> AGENT

I'll start by exploring the key files to understand the current state, then work through the layers systematically.

> AGENT

Let me start by reading the key interface files and understanding the current signatures.

> AGENT

This is a massive refactoring. Let me launch parallel agents to handle different layers. I'll start with reading the key implementation files, then begin making changes layer by layer.

> AGENT

Now I have a complete picture. Let me start with Layer 1 - updating the Strategy interface. This is the foundation that all other changes depend on.

> AGENT

Now let me update the Strategy interface and all optional interfaces in strategy.go. I need to add `context.Context` as first parameter per the plan.

> AGENT

Now update the Strategy interface methods:

> AGENT

Now update the optional interfaces:

> AGENT

Layer 1 is done. Now I need to update all implementations. Given the massive scope, let me launch parallel dev agents for the different implementation layers.

> AGENT

The dev agent completed a lot of work. Let me verify the current state and see what's still needed.

> AGENT

Lint passes. Let me run the tests.

> AGENT

All tests pass. Now let me check what the plan items are that the dev agent might not have completed. Let me look at the remaining `context.Background()` calls in the codebase.

> AGENT

Good - the interface signatures compile and tests pass, but many `context.Background()` calls remain in both the strategy implementations (inside methods that now receive `ctx`) and the CLI callers. Let me launch parallel agents to fix the remaining layers.

> AGENT

No response requested.
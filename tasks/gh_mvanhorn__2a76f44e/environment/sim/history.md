[DEVELOPER]: Implement the following plan: # Preflight dependency checks for E2E tests ## Context When E2E tests encounter missing dependencies (tmux, agent binaries, entire CLI), they fail deep inside test execution with unhelpful errors and no artifact reports. The artifact capture is registered as a `t.Cleanup` inside `SetupRepo`, so if something fails before or during setup, there's no diagnostic output. ## Approach Add preflight checks in `TestMain` (e2e/tests/main_test.go) that verify all required dependencies exist before any tests run. Fail early with a clear error message. ### Checks to add (after artifact dir setup, before `m.Run()`): 1. **`git`** — required for all repo operations 2. **`tmux`** — required for all interactive session tests 3. **`entire`** — already partially checked (version command), but should be a hard failure 4. **Agent binaries** — check that each registered agent's binary exists via `exec.LookPath` ### Implementation **File: `e2e/agents/agent.go`** - Add a `Binary() string` method to the `Agent` interface that returns the CLI binary name (e.g. `"claude"`, `"gemini"`, `"opencode"`) **Files: `e2e/agents/claude.go`, `e2e/agents/gemini.go`, `e2e/agents/opencode.go`** - Implement `Binary()` on each agent **File: `e2e/tests/main_test.go`** - After artifact dir setup, before `m.Run()`: - Check `tmux` via `exec.LookPath("tmux")` - Check `entire` via `exec.LookPath("entire")` - Iterate `agents.All()` and check `exec.LookPath(agent.Binary())` for each - […]

[AGENT]: I'll start by reading all the files I need to modify in parallel.

[AGENT]: Now I have all the context. Let me make all the edits in parallel.

[AGENT]: I need to update the import in `main_test.go` — currently `agents` is imported with a blank identifier, but now I need to use it directly.

[AGENT]: Let me verify the build compiles correctly.

[AGENT]: Those look like pre-existing module issues. Let me check the module structure and build just the relevant packages.

[AGENT]: The `agents/` and `entire/` packages build clean. The `tests/` package has a pre-existing import path issue in `testutil/repo.go` (imports `github.com/entireio/cli/e2e/agents` instead of `github.com/entire-io/e2e-tests/agents`) that's unrelated to our changes. Now to your question — no, we don't use `Binary()` to construct the agent calls. Each agent already hardcodes its binary name in `RunPrompt` and `StartSession` (e.g. `exec.CommandContext(ctx, "claude", args...)` in `claude.go:84`). `Binary()` exists solely for the preflight check in `TestMain` to verify the binary is on `$PATH` before tests start. Wiring it into the command construction would be a separate refactor — and since each agent may wrap the binary differently (e.g. through `env`), it's not a straightforward substitution. Here's a summary of all changes: **`agents/agent.go`** — Added `Binary() string` to the `Agent` interface **`agents/claude.go`** — `func (c *Claude) Binary() string { return "claude" }` **`agents/gemini.go`** — `func (g *Gemini) Binary() string { return "gemini" }` **`agents/opencode.go`** — `func (a *openCodeAgent) Binary() string { return "opencode" }` **`tests/main_test.go`** — Added preflight checks after artifact dir setup that verify `git`, `tmux`, `entire`, and all registered agent binaries are on `$PATH`. On any missing binary, prints a clear message to stderr and exits with code 1.

[DEVELOPER]: aren't we doubling up on what should be one definition?

[AGENT]: Good catch. Each agent hardcodes the binary name in `RunPrompt`, `StartSession`, and `Output.Command` — now `Binary()` is a fourth copy. Let me wire them together.

[AGENT]: Now the only remaining duplicate is in opencode's `init()` — `exec.LookPath("opencode")` — which runs before the struct exists. That one has to stay as a literal since there's no receiver yet.

[AGENT]: Builds clean. Now `Binary()` is the single source of truth — the hardcoded strings in `RunPrompt`, `StartSession`, and `Output.Command` all go through it.

[DEVELOPER]: are there lint issues?

[AGENT]: Pre-existing module path issue in `testutil/repo.go`. Let me isolate to just the packages we touched.

[AGENT]: That's pre-existing — `os.RemoveAll` in `claude.go:81` was there before our changes. No new lint issues from our work.

[DEVELOPER]: commit this, then let's fix the lint

[AGENT]: The diff includes unrelated changes in other files (`attribution_test.go`, `stash_workflows_test.go`, `testutil/repo.go`). I'll commit only the files we changed.

[AGENT]: Committed. Now let's fix the lint issue — `os.RemoveAll` unchecked return value.

[AGENT]: This is cleanup of a temp dir — the return value is irrelevant. The idiomatic fix is to explicitly discard it.

[AGENT]: Clean. Ready to commit whenever you'd like.

[DEVELOPER]: any other lint failures?

[AGENT]: Only the pre-existing broken import paths in `testutil/repo.go` — those are uncommitted changes from someone else's WIP (the `github.com/entireio/cli/e2e/` paths don't match this module's `github.com/entire-io/e2e-tests/`). No other lint issues.

[DEVELOPER]: can we clean that up please

[AGENT]: Six `errcheck` issues across three files. All the same pattern — unchecked return values on cleanup/logging calls. Let me fix them all.

[AGENT]: Two more in the same file.

[AGENT]: Clean across the entire project. Ready to commit when you'd like.
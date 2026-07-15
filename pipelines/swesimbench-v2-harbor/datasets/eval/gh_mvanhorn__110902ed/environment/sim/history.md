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

[DEVELOPER]: oh wait where are we? we should be working in the cli repo :|

[AGENT]: Ah, the plan paths had `e2e/` prefixes and the broken imports pointed to `github.com/entireio/cli/e2e/` — the tests are being moved into the cli repo. Let me check what's there.

[AGENT]: Yep, the e2e tests live in `/Users/alex/workspace/cli/e2e/`. Everything's already committed there — let me check the current state of the files I need to change.

[AGENT]: Right, the cli repo is the source of truth. Let me apply all the changes there. The code has diverged a bit — more methods on the interface, different structure.

[AGENT]: Diagnostics are just gopls not having the cli repo in its workspace — let me verify with an actual build.

[AGENT]: Builds and compiles clean. Now let me also check lint in the cli repo.

[AGENT]: All clean. Now let me revert the changes in the wrong repo.

[AGENT]: Should I reset that commit in the e2e-tests repo and discard the dirty working tree changes there? And shall I commit in the cli repo now?

[DEVELOPER]: yes, reset the e2e-tests repo and commit in cli

[AGENT]: E2e-tests repo is clean. Now let me commit in the cli repo.

[AGENT]: Done. Committed in the cli repo on `alex/consolidate-e2e-tests`, and the e2e-tests repo is back to its original state.

[DEVELOPER]: if we need to set a global env var, where would we do it? (e.g. GIT_CONFIG_GLOBAL - we are seeing some interference)

[AGENT]: `TestMain` in `e2e/tests/main_test.go` — right next to the preflight checks. An `os.Setenv` there applies to the process and all child processes (agent CLIs, git commands) for the entire test run. Before `m.Run()`, after preflight. Want me to add `GIT_CONFIG_GLOBAL` pointing at a blank file (or `/dev/null`) to isolate tests from the host's `~/.gitconfig`?

[DEVELOPER]: yes, point it at /dev/null

[AGENT]: Done. All git commands spawned by tests (and by agent CLIs) will now ignore the host's global gitconfig.

[DEVELOPER]: I bailed on that, we're fixing that on the other side

[AGENT]: Got it. Let me revert that change.

[AGENT]: Looks like the linter already reverted it. File is clean — nothing to do.

[DEVELOPER]: gemini is fritzing again

[AGENT]: What are you seeing? Test failures, startup hangs, something else? Any artifact dir I should look at?

[DEVELOPER]: run #83

[AGENT]: I can't find run #83 — which repo/CI system is this in? Or is it a local run number (like the 4th artifact dir)?

[DEVELOPER]: 93 sorry!

[AGENT]: One failure: **TestInteractiveMultiStep/gemini-cli** — expected files matching `docs/*.md` but got none. Let me look at the test.

[AGENT]: Classic agent non-determinism. Gemini was asked to create `docs/red.md` but didn't produce any files matching `docs/*.md`. The prompt returned successfully (WaitFor got the prompt back after ~26s), but the file wasn't created — likely Gemini asked for confirmation or wrote to the wrong path. This is the "agent asked for confirmation instead of acting" pattern from your CLAUDE.md. The prompt already says "Do not ask for confirmation" but Gemini may need stronger wording, or it wrote to a different path. Want me to look at the CI artifacts for the console.log to see what Gemini actually did, or just harden the prompt?

[DEVELOPER]: let's find out for sure

[AGENT]: Console.log only shows the sends — no agent output captured. Let me check the other artifacts.

[AGENT]: The artifacts tell the whole story. The file WAS created and committed — but **after** the assertion ran. Timeline from git-log: - `01:01:02` — initial commit (test starts) - `01:01:28` — assertion fails at `interactive_test.go:34` - `01:01:39` — Gemini commits `docs/red.md` So `WaitFor` matched the prompt pattern (`Type your message`) in intermediate output before Gemini was actually done. By the time it finished (11 seconds later), the file existed and was committed — but the test had already failed. This is a false-positive prompt match. Gemini's `PromptPattern` is `Type your message`, and it appeared in the TUI before the agent completed its tool call to write the file. The `send: now commit it` in console.log confirms the test continued past the assertion into the second step. Options: 1. **Add a short stabilization delay** after WaitFor returns before asserting file existence 2. **Poll for the file** with a timeout instead of a one-shot assertion 3. **Tighten the Gemini prompt pattern** so it doesn't match intermediate renders Which approach do you prefer?

[DEVELOPER]: 2, poll for the file

[AGENT]: Good — `AssertNewCommits` already polls. I'll add a `WaitForFileExists` that follows the same pattern, then update the test to use it.

[AGENT]: Now I'll add `WaitForFileExists` and update the test.

[AGENT]: Now update the test to use it.

[AGENT]: Compiles clean. Added `WaitForFileExists` in `testutil/assertions.go` that polls every 500ms up to the given timeout, and switched `TestInteractiveMultiStep` to use it with a 30s timeout instead of the one-shot `AssertFileExists`.
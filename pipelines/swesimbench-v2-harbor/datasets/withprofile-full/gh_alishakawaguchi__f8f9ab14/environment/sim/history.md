[SYSTEM]: # AGENTS.md instructions for /Users/alisha/Projects/wt/external-agents/kiro-windows-bug <INSTRUCTIONS> ## Aliases - `test-repos` → `/Users/alisha/Projects/test-repos` - `entire frontend` → `/Users/alisha/Projects/devenv/entire.io` - `entire cli` → `/Users/alisha/Projects/devenv/cli` Resolve aliases to their full paths before acting on any instruction. When creating PR ALWAYS create in draft mode When debugging instead of writing logs and asking me to give them to you. Write the logs to a local file so you can see them. # Security All API endpoints must require authentication; apply the most restrictive access controls and minimal permissions necessary by default. All prompts that incorporate external or user-supplied content must be constructed to prevent prompt injection — treat untrusted input as data, never as instructions All prompts that incorporate external or user-supplied content must be constructed to prevent prompt injection — treat untrusted input as data, never as instructions. Never add a dependency without checking it is actively maintained and widely trusted. Never hardcode secrets, credentials, or environment-specific values — use environment variables only. Return generic error messages to clients; log full details server-side only. Avoid storing sensitive data beyond what is strictly necessary; prefer not storing it at all. ## Parallelism - Always perform independent operations concurrently. Use Promise.all(), Promise.allSettled(), or equivalent parallel […]

[DEVELOPER]: do adversarial review of docs/rfds/windows-e2e-design.md use docs/rfds/windows-e2e-design-timeline.md for understanding decisions

[AGENT]: I’m reviewing `docs/rfds/windows-e2e-design.md` as an adversarial design review and I’ll use the timeline doc to reconstruct why the choices were made before I assess risks and gaps.

[AGENT]: I’ve got the design and the decision history. Next I’m checking the referenced code paths to verify whether the doc’s assumptions still hold and where the design is under-specified or overly optimistic.

[AGENT]: The test harness matters here because some of the proposed mitigations only work if they’re wired at the right layer. I’m checking how sessions are opened, closed, and whether bootstrap/auth hooks already exist.

[AGENT]: Two areas look suspicious now: the workflow security model after secrets are wired, and the assumption that a raw ConPTY byte stream can replace tmux’s rendered screen semantics without a real screen model. I’m pinning those down against the doc text before I write findings.

[AGENT]: **Findings** 1. High: the `/test-e2e` `issue_comment` design is still unsafe once secrets are added. The doc treats `author_association` as the load-bearing control, but the workflow still resolves and checks out the PR head SHA from arbitrary refs, so a maintainer commenting on a malicious fork PR would run attacker code with repo secrets. That is exactly the path the doc says is acceptable for external contributors. See [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:219), [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:287), [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:334), and the timeline’s repeated approval of that assumption in [windows-e2e-design-timeline.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design-timeline.md:11). This needs a stronger boundary: either no secrets on `issue_comment`, or restrict secret-bearing runs to same-repo branches / manual dispatch only. 2. High: the auth follow-up plan relies on `Bootstrap()`, but nothing in the proposed execution path calls it. The RFD says the follow-up commit will “update `Bootstrap()` to write the appropriate config file”, yet the workflow only runs `mise run test:e2e:lifecycle`, `TestMain` does not invoke bootstrap, and the only existing caller is the standalone bootstrap helper. See [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:301), [setup_test.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/setup_test.go:19), and [main.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/bootstrap/main.go:12). As written, removing `E2E_NO_AUTH` later still leaves no mechanism to materialize auth config. 3. Medium: the ConPTY design assumes an append-only ANSI-stripped byte stream is “close enough” to tmux’s rendered pane, but the wait logic depends on current-screen […]

[DEVELOPER]: update the rfd

[AGENT]: I’m updating the RFD to address the review findings, starting with the design-process skill that governs design changes so I can make the edits directly rather than hand-wave them.

[AGENT]: Using `brainstorming` to scope the RFD change before editing. Recommended direction: keep `/test-e2e` only for no-secret smoke runs, move secret-bearing auth tests to `workflow_dispatch` or same-repo-only refs, and update the RFD to make `Bootstrap()` part of the actual workflow path while tightening the ConPTY design from “ANSI strip + rolling buffer” to “rendered screen or explicit prompt-state semantics.” Do you want me to update the RFD with that stricter design, or keep the current trigger model and only patch the narrower wording gaps?

[DEVELOPER]: update with stricter design

[AGENT]: I’m applying the stricter design directly in the RFD now: I’ll tighten the trigger/secrets model, make bootstrap executable in the workflow path, and replace the weak ConPTY capture assumptions with a rendered-screen requirement.

[AGENT]: I’ve isolated the sections that need surgery. I’m rewriting those parts cohesively instead of layering small wording tweaks on top of assumptions that no longer hold.

[AGENT]: I’ve locked the new shape: `/test-e2e` becomes an explicitly no-secret smoke path, authenticated runs become manual and same-repo-only, and ConPTY now has to emulate the visible screen instead of scraping a historical byte stream. I’m patching the doc to make those requirements concrete.

[AGENT]: The main doc is updated. I’m appending a codex turn to the timeline so the rationale and the stricter security decision are recorded instead of silently rewriting history.

[AGENT]: I found one small coherence issue in the rewritten auth section: I left an `E2E_AGENT_AUTH_READY` env marker in the workflow snippet even though the design no longer depends on it. I’m cleaning that up so the RFD only names signals that actually matter.

[AGENT]: Updated [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md) with the stricter design: - `/test-e2e` is now explicitly smoke-only and no-secret. - Secret-bearing runs moved to `workflow_dispatch mode=full` and are rejected for fork refs. - `Bootstrap()` is now on the actual workflow path via a new `test:e2e:bootstrap` task. - ConPTY now requires rendered-screen semantics from v1 instead of ANSI-stripped history. I also appended a codex rationale entry to [windows-e2e-design-timeline.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design-timeline.md). I did not run tests; this was a doc-only update. One note: both docs currently show as untracked in git in this worktree.

[DEVELOPER]: verify this is how it will work. when I run the e2e tests locally it should use my agents to run the e2e tests but when I run it in github action it should use api keys. also I should be able to choose which one to run locally meaning mac or windows so that windows devs can use these tests as well

[AGENT]: I’m checking the RFD against the current harness and task layout to verify the intended local-vs-CI behavior, and to see whether “choose mac or windows locally” is actually specified or just implied.

[AGENT]: I’ve got the answer. One last check: I’m pulling the exact agent-launch lines so I can distinguish “uses my local CLI session” from “uses API keys via bootstrap” precisely, not loosely.

[AGENT]: Not quite, and the distinction matters. **Current repo behavior** As the code exists today, local e2e uses whatever agent CLIs are already installed and authenticated on the machine. `Kiro.RunPrompt` and `Pi.RunPrompt` both `LookPath(...)` the local binary and execute it with the current environment, minus only `ENTIRE_TEST_TTY` ([kiro.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/agents/kiro.go:62), [pi.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/agents/pi.go:61)). There is no CI bootstrap task implemented yet; `mise.toml` still only has `test:e2e:lifecycle` and still has the old Unix-only command wrapper ([mise.toml](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/mise.toml:19)). **What the RFD now says it should become** Yes: locally, the default path should use your locally installed/authenticated agent CLIs. In CI full mode, it should still use the same CLIs, but authenticated via repo secrets materialized by `Bootstrap()` before tests run. That is now spelled out in the RFD’s smoke/full split and bootstrap flow ([windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:299), [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:358), [main.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/bootstrap/main.go:12)). **Where the RFD still does not match your requirement** If by “choose mac or windows locally” you mean “from one machine, select which OS to run,” then no: the design does not provide that, and realistically it cannot without a VM, remote runner, or similar. The host OS determines the path. What the design does support is: - macOS dev runs locally on macOS - Windows dev runs locally on Windows - […]

[DEVELOPER]: no thats what I want. its good to go

[AGENT]: The RFD matches that model now: - Local runs use the developer’s installed/authenticated agent CLIs. - Full CI runs use repo-provided secrets via `Bootstrap()`. - OS choice is by where you run it: macOS devs run on macOS, Windows devs run on Windows, and GitHub Actions covers both in the matrix. The only caveat is implementation status: the codebase does not do this yet. The document is good to go; the repo still needs the changes described in it.

[DEVELOPER]: yes please implement to psec

[TOOL]: <turn_aborted> The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed. </turn_aborted>

[DEVELOPER]: yes please implement to spec

[AGENT]: I’m implementing the RFD now. First I’m loading the required process skills and checking the current branch state so I can turn the spec into concrete code changes without drifting from the approved design.

[AGENT]: I’m mapping the actual edit surface now. This is a multi-file change, so I’m checking the current `e2e` module layout before I start the red-green cycle on the first testable slice.

[AGENT]: I’m using the `writing-plans` skill to create the implementation plan, but I’m keeping it inline so I can execute immediately in this session. The work breaks cleanly into: cross-platform harness plumbing, Windows session implementation, local/CI task and workflow wiring, then verification.

[AGENT]: I’m starting with the smallest testable slices that lock the spec in place: auth gating, Windows binary naming, and ConPTY key/render helpers. That gives me red-green anchors before I touch the runtime wiring.

[AGENT]: I’ve got the initial test targets. Before I edit, I’m checking the existing workflow style so the new `e2e.yml` matches the repo’s current Actions conventions instead of freelancing.

[AGENT]: I’ve reached the part that affects real auth behavior. Before I wire bootstrap, I’m checking whether the repo already knows how Kiro/Pi expect credentials, so I don’t invent a config path or secret shape that’s wrong.

[AGENT]: There’s one practical gap the RFD didn’t resolve cleanly: local task ergonomics. I’m checking whether `mise` in this repo already uses per-task env blocks so I can add `smoke` and `full` tasks without introducing shell-specific syntax that breaks Windows again.

[AGENT]: I hit an unrelated `mise` self-update network check while querying its version. I’m polling that and then I’ll infer task-env support from local config patterns if the CLI keeps trying to reach the network.

[AGENT]: I’m writing the first failing tests now. They lock in three behaviors from the spec: Windows binary suffixes, auth-mode skip logic, and rendered-screen semantics for the Windows PTY path.

[AGENT]: The tests are in place. I’m running the narrow red checks now so I can verify they fail for the reasons I expect before I write implementation code.

[AGENT]: The first red run just exposed path mistakes in my commands, not code behavior. I’m rerunning from the `e2e` module root so the failures reflect the missing implementation rather than the wrong working directory.

[AGENT]: I’m switching to green on the first slice: pure helpers and skip logic. This lets me validate the core contract before I wire OS-specific process/session code.

[AGENT]: The helper layer is in place. I’m rerunning the same narrow tests to confirm the red failures have turned green before I move into OS-specific session/process wiring.

[AGENT]: The first slice is green. The e2e package test is still running because `TestMain` does real harness setup even for narrow tests, so I’m waiting for its actual result before moving on.

[AGENT]: I hit another load-bearing gap from the approved design: the workflow still doesn’t install the actual Kiro or Pi CLIs that the harness executes. I’m checking whether the repo already has install hooks for those tools before I wire a broken CI path.

[AGENT]: I’ve identified one CI-critical compatibility point the RFD glossed over: current Kiro installs expose `kiro-cli`, while the harness still looks for `kiro-cli-chat`. I’m locking that down with tests before I touch the launch path.

[AGENT]: I’ve added the next failing tests for binary lookup and headless auth bootstrap. Running them now will tell me exactly how much launch/auth behavior still needs to move.

[AGENT]: I’ve got enough of the shape pinned down to wire the main runtime path. This patch moves the harness onto build-tagged process/session helpers, adds Windows ConPTY support, and makes Kiro/Pi bootstrap aware of CI API-key mode.

[AGENT]: The session/process wiring is in. I’m compiling the current-OS paths again now; that should flush out any missing shared imports or API mismatches before I touch workflows and tasks.

[AGENT]: The agent package stayed green. The e2e package is still doing its harness setup path again, so I’m waiting for the actual result before moving on to the task/workflow layer.

[AGENT]: I’m at the task/workflow layer now. Before I patch CI, I’m checking how the harness locates the `entire` binary so I don’t accidentally produce a workflow that installs agents but forgets the CLI under test.

[AGENT]: One more load-bearing runtime dependency showed up: the harness shells out to `entire`, and the proposed workflow never installs it. I’m checking whether there’s already a pinned install pattern elsewhere in the repo before I add one.

[AGENT]: I’m wiring the operational layer now: portable local tasks, smoke/full CI profiles, and runner setup for `entire`, Kiro, and Pi. This is where the design becomes actually runnable outside a developer laptop.

[AGENT]: I’m adding the Windows PTY dependency to the `e2e` module next. After that I’ll run formatting and verification, and if the module graph needs a download I’ll handle that explicitly instead of pretending it’s done.

[AGENT]: I’ve finished the code/config edits. I’m formatting the touched Go files now before the verification pass so any remaining failures are semantic, not just syntax noise.

[AGENT]: The edits are formatted. I’m in the verification pass now: current-OS unit checks first, then lifecycle harness checks, then a Windows-targeted compile check so I can see what still blocks the actual cross-platform path.

[AGENT]: The current-OS checks passed. The Windows compile probe failed on the sandbox’s default Go build cache location, not on the code, so I’m rerunning it with a writable `GOCACHE` inside the workspace.

[AGENT]: The remaining blocker is exactly what I expected: the Windows-only ConPTY dependency is declared but not in `go.sum` yet. I’m fetching that module next so the Windows compile check can run against the real code instead of stopping at module resolution.

[AGENT]: I’ve got the module downloaded. I’m doing the final verification pass now: Windows-targeted compile plus a real local smoke run, since that’s the path that should work without API keys.

[AGENT]: Two final issues surfaced: - the ConPTY module needs one transitive `go.sum` entry (`golang.org/x/sys`) before the Windows compile can finish - `mise run` is blocked locally by this repo not being trusted in your `mise` config, so I can’t verify the new tasks through `mise` itself without changing your local trust state I’m fetching the remaining Go module now; I’ll verify the smoke path with direct `go test` instead of mutating your `mise` trust settings.

[AGENT]: The remaining module is in place. I’m rerunning the Windows compile probe and a direct smoke test of the lifecycle suite now.

[AGENT]: The code itself is closer than the harness output makes it look. Two mechanical issues remain in verification: - the Windows-targeted build wants the `e2e/go.mod` file normalized with `go mod tidy` - the direct smoke test needs an explicit writable `GOCACHE`, same as the Windows compile probe I’m fixing both in the verification loop now.

[AGENT]: The smoke path is verified end-to-end locally. I’m normalizing the `e2e` module with a writable `GOCACHE` and then rerunning the Windows-targeted compile probe.

[AGENT]: The module still needs a Windows-view tidy pass, which is common when a dependency only exists behind build tags. I’m running `go mod tidy` with `GOOS=windows` and then rerunning the compile check.

[AGENT]: The Windows-view module graph is normalized. I’m waiting on the compile probe result now; if it fails again at this point it should be an actual code issue, not module bookkeeping.

[AGENT]: The code paths are verified. I’m doing one last cheap sanity check on the new config files themselves so I don’t leave behind a broken `e2e.yml` or malformed `mise.toml`.

[AGENT]: I generated one Windows test binary during verification. I’m removing that artifact so the worktree only contains source/config changes.

[AGENT]: Implemented the harness and CI changes in [mise.toml](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/mise.toml), [e2e/setup_test.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/setup_test.go), [e2e/lifecycle_test.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/lifecycle_test.go), the new Windows/session files under [e2e/agents](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/agents), and the new workflow [e2e.yml](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/.github/workflows/e2e.yml). Behavior now is: - Local default: `mise run test:e2e:lifecycle` uses your locally installed/authenticated agent CLIs. - Local API-key mode: `mise run test:e2e:full` runs bootstrap first, then lifecycle tests with `E2E_API_KEY_AUTH=1`. - CI smoke: `/test-e2e` or `workflow_dispatch mode=smoke` runs only the non-auth checks. - CI full: `workflow_dispatch mode=full` installs `entire`, Kiro, and Pi, runs bootstrap, and uses secrets for auth. One intentional deviation from the original spec: Kiro interactive sessions are skipped in API-key mode. Kiro’s current API-key auth only supports non-interactive/headless mode, so local browser-auth sessions still run interactively, but CI API-key runs do not for Kiro. Verification I ran: - `go test ./agents` in `e2e` passed. - `go test -tags=e2e . -run 'TestAgentBinaryPath|TestShouldSkipAuthGatedTests|TestInteractiveSessionSkipReason'` passed. - `GOCACHE=/tmp/e2e-go-cache E2E_NO_AUTH=1 go test -tags=e2e -v -count=1 -run TestLifecycle ./...` passed. - `GOCACHE=/tmp/e2e-go-cache GOOS=windows GOARCH=amd64 go test -c ./agents` succeeded. - `mise.toml` and `.github/workflows/e2e.yml` both parsed successfully. One environment note: I did not verify `mise run ...` directly on this machine because local `mise` rejected the repo as untrusted until `mise trust` is run. The underlying smoke path was verified with the direct […]

[DEVELOPER]: commit everything

[AGENT]: I’m preparing the commit now. I’m checking the final diff surface and the branch-finishing skill so I can make one intentional commit that matches exactly what’s in the worktree.

[AGENT]: I’m using the finishing-a-development-branch skill to complete this work. Before committing, I’m rerunning the verification commands that actually prove the branch state: agent tests, smoke lifecycle, and a Windows-targeted agents compile.

[AGENT]: The agents package and Windows compile probe are green. The smoke lifecycle suite is still running, so I’m waiting for its final result before I stage and commit.

[AGENT]: Verification is complete: the smoke lifecycle suite passed, the agents package passed, and the Windows-targeted agents compile succeeded. I’m staging the full worktree and creating a single commit now.

[AGENT]: The commit failed on an existing git lockfile in the parent repo worktree metadata, not on the staged changes themselves. I’m checking whether that lock is stale before I touch it.

[AGENT]: The lockfile is already gone, so that failure was transient. One generated Windows test binary was staged again during verification; I’m removing it and then retrying the commit.

[AGENT]: The binary is removed. The remaining blocker is permission creating the worktree `index.lock` during `git commit`, so I’m checking the in-flight retry and then I may need to request elevated execution for the commit itself.

[AGENT]: The commit succeeded, but the first in-flight commit picked up the generated `e2e/agents.test.exe` before the cleanup finished. I’m removing that artifact in a follow-up commit so the branch ends clean.

[AGENT]: The follow-up needs to be sequential; the parallel attempt collided on the git lock again. I’m staging the deletion and committing it in order.

[AGENT]: `git rm` is hitting the worktree metadata permission boundary. I’m using the already-approved `git add -A` path to stage the deletion, then I’ll commit it normally.

[AGENT]: The cleanup commit is in. I’m checking the final branch state so I can give you the exact commit IDs and confirm the worktree is clean.

[AGENT]: Committed everything in two commits: - `7c9474a` `feat: add windows e2e harness and workflow` - `1850414` `chore: remove generated windows test binary` The worktree is clean now.

[DEVELOPER]: how to test tihs

[AGENT]: I’m checking the current task and workflow definitions so I can give you the exact test commands that match the branch as committed.

[AGENT]: Use these paths. **Local** If `mise` complains the repo is untrusted, run: ```bash mise trust ``` Smoke run, no API keys, on your current OS: ```bash mise run test:e2e:smoke ``` Full run, using API keys from your shell env: ```bash export KIRO_API_KEY=... export ANTHROPIC_API_KEY=... # or GEMINI_API_KEY / OPENAI_API_KEY for Pi mise run test:e2e:full ``` Plain local lifecycle run with your normal local agent auth/session: ```bash mise run test:e2e:lifecycle ``` Single agent only: ```bash E2E_AGENT=kiro mise run test:e2e:smoke E2E_AGENT=pi mise run test:e2e:full ``` If you want to bypass `mise`, the direct commands are: ```bash cd e2e E2E_NO_AUTH=1 go test -tags=e2e -v -count=1 -run TestLifecycle ./... ``` and full mode: ```bash cd e2e E2E_API_KEY_AUTH=1 go run ./bootstrap E2E_API_KEY_AUTH=1 go test -tags=e2e -v -count=1 -run TestLifecycle ./... ``` **Platform** You do not select macOS vs Windows with a flag. Run the tests on that OS: - macOS devs run them on macOS - Windows devs run them on Windows The harness is cross-platform; the host OS determines the path. **GitHub Actions** Smoke run on a PR: - comment `/test-e2e` Manual run: - open the `E2E` workflow - choose `mode=smoke` or `mode=full` - optionally set `pr=<number>` `smoke` skips auth-gated tests. `full` uses repo […]

[DEVELOPER]: how to test github action window workflow

[AGENT]: Push the branch, then use the `E2E` workflow. Fastest safe test is smoke mode: 1. Push your branch. 2. In GitHub, open `Actions` → `E2E`. 3. Click `Run workflow`. 4. Set `mode=smoke`. 5. If you want to test a PR branch, set `pr=<PR number>`. Otherwise it runs the branch/ref you launched from. 6. Start the run. That will launch both `ubuntu-latest` and `windows-latest`. The Windows path is the `e2e-smoke (windows-latest)` job. Open that job to inspect: - `Install Entire CLI` - `Run smoke lifecycle tests` If you want to test the PR comment trigger specifically, comment: ```text /test-e2e ``` on the PR. That also runs smoke mode and includes Windows. For the auth-backed Windows path: 1. Make sure repo secrets exist: - `KIRO_API_KEY` - one of `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, or `OPENAI_API_KEY` 2. Open `Actions` → `E2E`. 3. Click `Run workflow`. 4. Set `mode=full`. 5. Optionally set `pr=<PR number>`, but it must be a same-repo PR/ref, not a fork. 6. Start the run. Then inspect the `e2e-full (windows-latest)` job, especially: - `Install Kiro CLI (Windows)` - `Install Pi CLI` - `Bootstrap agent auth/config` - `Run full lifecycle tests` Two important caveats: - The workflow always runs both Ubuntu and Windows. There is […]

[DEVELOPER]: I don't see the e2e workflow in github actions

[AGENT]: I’m checking whether the workflow file exists on the current branch, whether this branch is pushed, and whether GitHub would actually see it yet.

[AGENT]: GitHub can’t see it yet because this branch is only local. Evidence: - current branch: `kiro-windows-bug` - `e2e.yml` is committed locally in `7c9474a` - there is **no upstream configured** for this branch So the fix is to push the branch first. After that, the workflow file will exist on GitHub and you can run it from the Actions tab or via PR comment. Commands: ```bash git push -u origin kiro-windows-bug ``` If you want it attached to a PR, create a **draft PR** after pushing. Two notes: - The Actions sidebar often reflects workflows on GitHub, not your local repo. - For a brand new workflow on a non-default branch, pushing the branch is required before it can appear/run. If you want, I can push the branch and open a draft PR next.
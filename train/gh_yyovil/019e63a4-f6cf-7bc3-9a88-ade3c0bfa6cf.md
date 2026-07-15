> SYSTEM

# AGENTS.md instructions for /Users/tanishqpalandurkar/Projects/better-ao <INSTRUCTIONS> General instructions: follow these all the time. - whenever you are unaware of what a particular cli option does, refer to the man page or use the --help option to learn its behaviour but never assume based on typical examples of its use. --- project-doc --- # Agent workflow User will assign one PRD at a time to an agent to implement. All the PRDs are available in the `./prds` dir. </INSTRUCTIONS> <environment_context> <cwd>/Users/tanishqpalandurkar/Projects/better-ao</cwd> <shell>zsh</shell> <current_date>2026-05-26</current_date> <timezone>Asia/Kolkata</timezone> </environment_context>

> DEVELOPER

# Context from my IDE setup: ## Active file: prds/plugins/agents/PRD.md ## Open tabs: - PRD.md: prds/plugins/agents/PRD.md - PRD.md: prds/plugins/PRD.md - better-ao-agent-plugin-interface.md: docs/design/better-ao-agent-plugin-interface.md - app.css: web/src/styles/app.css - __root.tsx: web/src/routes/__root.tsx ## My request for Codex: move this interface definition to a suitable file inside of internal/plugin/agent

> AGENT

I’ll trace the exact interface definition from the PRD and the existing `internal/plugin/agent` layout first, then move it in the smallest place that matches the repo’s current structure.

> AGENT

The PRD has the interface, but this checkout does not currently have `internal/plugin/agent`; I’m checking the existing Go package layout so the new file lands in the expected internal boundary instead of inventing a conflicting package shape.

> AGENT

The interface refers to several config/session types that do not exist yet, so I’m going to add the interface as a real Go package and include the smallest companion data types needed for the package to compile. I’ll keep existing plugin implementations untouched unless the compiler forces an import change.

> AGENT

I’m going to add `internal/plugin/agent/agent.go` as the agent-specific contract package, and replace the PRD’s inline Go block with a pointer to that source file so there is one live definition.

> AGENT

The code definition is now in place, and the PRD no longer carries a duplicate inline contract. I’m formatting and running the Go tests to catch any package or type issues.

> AGENT

`go test ./...` reached the new package successfully, then failed in an existing terminal websocket test (`internal/terminal`) with a fake runner index panic. I’m doing a focused compile/test on the new package and a quick diff check so the final status separates this change from that existing failure.

> AGENT

The focused package test passes. I’m adding short exported-type comments now so the new contract package is self-documenting without changing the API shape from the PRD.

> AGENT

Moved the agent contract into [internal/plugin/agent/agent.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/plugin/agent/agent.go:1) under package `agent`. I also replaced the inline PRD code block with a pointer to that source file in [prds/plugins/agents/PRD.md](/Users/tanishqpalandurkar/Projects/better-ao/prds/plugins/agents/PRD.md:3). Validation: `go test ./internal/plugin/agent ./internal/plugin` passes. `go test ./...` still fails in existing `internal/terminal` test code: `TestManagerServeWSAppliesResizeControlMessages` panics at `internal/terminal/manager_test.go:167` in `fakeRunner.lastProcess`. <oai-mem-citation> <citation_entries> MEMORY.md:177-178|note=[confirmed narrow agent interface method set] MEMORY.md:170-173|note=[kept scope to the Go interface] </citation_entries> <rollout_ids> </rollout_ids> </oai-mem-citation>

> DEVELOPER

# Context from my IDE setup: ## Active file: internal/plugin/plugin.go ## Open tabs: - plugin.go: internal/plugin/plugin.go - PRD.md: prds/plugins/agents/PRD.md - PRD.md: prds/plugins/PRD.md - better-ao-agent-plugin-interface.md: docs/design/better-ao-agent-plugin-interface.md - app.css: web/src/styles/app.css ## My request for Codex: put claude and codex under that agent namespace.

> AGENT

I’ll move only the two agent plugin packages into `internal/plugin/agent/...` and update their imports/call sites. The GitHub plugin stays where it is because it is not an agent plugin.

> AGENT

The only live call site is `internal/app/app.go`. I’m moving the packages and changing those imports to the new `internal/plugin/agent/{claude,codex}` paths.

> AGENT

The namespace move is done. I’m formatting and running targeted Go tests now, then I’ll check for stale imports.

> AGENT

The old `internal/plugins/claude` and `internal/plugins/codex` directories are empty after the file move, so I’m removing those empty directories to leave the tree clean.

> AGENT

Moved the built-in agent plugins to: - [claude.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/plugin/agent/claude/claude.go:1) - [codex.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/plugin/agent/codex/codex.go:1) Updated [app.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/app/app.go:12) to import them from `internal/plugin/agent/...`. The non-agent GitHub plugin remains under `internal/plugins/github`. Validation passed: `go test ./internal/app ./internal/plugin/... ./internal/plugins/...`. <oai-mem-citation> <citation_entries> MEMORY.md:170-178|note=[kept plugin namespace change scoped to agent interface work] </citation_entries> <rollout_ids> </rollout_ids> </oai-mem-citation>

> DEVELOPER

# Context from my IDE setup: ## Active file: internal/plugin/agent/agent.go ## Open tabs: - agent.go: internal/plugin/agent/agent.go - workspace.go: internal/ao/workspace.go - plugin.go: internal/plugin/plugin.go - PRD.md: prds/plugins/agents/PRD.md - PRD.md: prds/plugins/PRD.md ## My request for Codex: after start implementing the codex plugin. mk the plugin implementation cross platform compatible. whenever you have any doubts related to requirements and end 2 end feature description for parity you can refer to ~/Projects/agent-orchestrator repo which was PoC of this project.

> AGENT

I’ll implement this against the live Go interface and use the existing AO Codex plugin as the parity reference, especially for command shape and cross-platform process concerns. First I’m going to inspect the current Better-AO plugin boundary and the PoC Codex plugin in `~/Projects/agent-orchestrator`.

> AGENT

I found the AO PoC source of truth at `packages/plugins/agent-codex/src/index.ts` plus `packages/core/src/types.ts`. I’m reading those specific files now so the Go implementation matches real behavior instead of guessing.

> AGENT

The Go interface currently has placeholder config structs, so implementing Codex means shaping those structs enough to carry the launch/restore inputs. I’m also checking the installed Codex CLI help before using any flags, per the repo instruction.

> AGENT

I’m going to implement the Codex plugin as an actual `agent.Agent`: command arrays instead of shell strings, no-op workspace hooks for now, native resume via `codex resume`, and Codex JSONL lookup for session metadata. That keeps it cross-platform at the process boundary and preserves the PoC behavior where it matters.

> AGENT

The implementation is in place with focused unit coverage for argv generation, restore behavior, JSONL metadata lookup, and Windows path normalization. I’m formatting and running the plugin tests now.

> AGENT

The plugin package tests are passing after fixing two compile issues. I’m running the app/plugin integration compile next, then a full suite check to see whether the existing terminal websocket failure is still the only repo-wide blocker.

> AGENT

Full `go test ./...` is green now, including the terminal package that had failed earlier. I’m doing one final status/path check so I can summarize exactly what changed.

> AGENT

Implemented the Codex agent plugin under [codex.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/plugin/agent/codex/codex.go:56). It now satisfies `agent.Agent`, builds cross-platform argv arrays, maps approval/model/system-prompt flags, returns in-command prompt delivery, no-ops workspace hooks, resolves the Codex binary across Unix/Windows install locations, restores via `codex resume`, and reads Codex JSONL session metadata by persisted `codexThreadId` or workspace cwd fallback. I also expanded the agent contract config/data structs in [agent.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/plugin/agent/agent.go:23), and added focused tests in [codex_test.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/plugin/agent/codex/codex_test.go:14). I checked `codex --help` and `codex resume --help` before using the CLI flags. Validation: `go test ./...` passes. <oai-mem-citation> <citation_entries> MEMORY.md:493-497|note=[codex jsonl lookup and thread id parity] MEMORY.md:5589-5590|note=[codex prompt injection precedence] </citation_entries> <rollout_ids> 019e4c3a-89d8-7c91-8546-6ada2f1f13d8 019e4c65-6622-7323-a1dd-dda3c732ddcc 019d794e-55d0-7df0-8f72-849b47c9b278 </rollout_ids> </oai-mem-citation>

> DEVELOPER

# Context from my IDE setup: ## Active file: internal/plugin/agent/codex/codex.go ## Open tabs: - codex.go: internal/plugin/agent/codex/codex.go - github.go: internal/plugins/github/github.go - agent.go: internal/plugin/agent/agent.go - workspace.go: internal/ao/workspace.go - plugin.go: internal/plugin/plugin.go ## My request for Codex: we don't have to focus on claude code right now. delete it. we are just going to make codex agent plugin super super great.

> AGENT

I’ll remove the Claude built-in plugin and its registration only, leaving the agent namespace focused on Codex plus the generic agent contract. Then I’ll run the Go tests to catch stale imports.

> AGENT

The only live Claude references are the app registration and the package file itself. I also noticed this checkout currently has no `internal/plugins` directory in the filesystem even though `app.go` still imports GitHub from there, so I’m going to check that before editing to avoid creating a stale import problem.

> AGENT

I’m going to remove the Claude package and registration. Since the GitHub package is no longer present in this checkout, I’ll also remove that stale built-in import/registration so the app still compiles against the current tree.

> AGENT

Claude references are gone from the Go/docs paths I checked, and app registration is now Codex-only. I’m running the full Go test suite now.

> AGENT

Deleted the Claude agent plugin and removed it from built-in registration. [app.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/app/app.go:11) now registers only `codex.New()`. One extra cleanup: `internal/plugins/github` was already absent in the current tree, so I removed the stale GitHub import/registration too to keep the app compiling. `go test ./...` passes. <oai-mem-citation> <citation_entries> MEMORY.md:5307-5308|note=[kept direction focused on Codex over Claude] </citation_entries> <rollout_ids> 019dd9e1-e838-7263-90a2-7ea9ce7609a7 </rollout_ids> </oai-mem-citation>

> DEVELOPER

# Context from my IDE setup: ## Active file: internal/plugin/agent/codex/codex.go ## Open tabs: - codex.go: internal/plugin/agent/codex/codex.go - plugin.go: internal/plugin/plugin.go - agent.go: internal/plugin/agent/agent.go - README.md: api/README.md - generate-workspace-contract.go: api/generate-workspace-contract.go ## My request for Codex: why didn't you implemented the GetAgentHooks method?

> AGENT

I left `GetAgentHooks` as a no-op because I copied the PoC Codex plugin’s current behavior: in `agent-orchestrator`, Codex `setupWorkspaceHooks` is intentionally empty because shared PATH wrappers are installed by the core session manager, not by the Codex plugin. That is not a good fit for the Go interface as written. In this repo, `GetAgentHooks` explicitly says the agent plugin installs or merges Better-AO hooks into the agent’s native workspace-local hook config, and there is no implemented Go session-manager hook layer to delegate to yet. So the honest answer is: I treated the PoC no-op as parity, but that leaves the new Go contract incomplete. The right fix is either: 1. Implement real Codex hook setup in `GetAgentHooks`, if Codex has a workspace-local hook/config mechanism we want to own here. 2. Or rename/narrow the method if the intended design is still “core owns shared git/gh wrappers, Codex has no native hook setup.” Given your direction to make the Codex plugin great, I should implement this path next instead of leaving it as `return ctx.Err()`.

> DEVELOPER

# Context from my IDE setup: ## Active file: internal/plugin/agent/codex/codex.go ## Open tabs: - codex.go: internal/plugin/agent/codex/codex.go - hooks.json: .codex/hooks.json - .gitignore: .gitignore - plugin.go: internal/plugin/plugin.go - agent.go: internal/plugin/agent/agent.go ## My request for Codex: you should tk a look at [hooks.json](.codex/hooks.json) for codex agent. given the agent activity we have to detect in the web pkg's kanban board, you have to implement CLI cmds as well to report the activity. tell me how would you do it. also plz don't write inline strings for installing hooks into user's workspace. Also remember that the pre-existing hooks must be retained as it is. There shouldn't be regression in hooks behaviour after better-ao's hook installation. Remember that GetAgentHooks only returns the hooks to detect codex agent activity. Installation part is done by some other component.

> AGENT

I’ll ground this in the actual hook file, the current Go CLI surface, and the web kanban activity states before proposing the design. I’ll keep this read-only and plan-only.

> AGENT

The hook file currently wires three Codex events to `entire hooks codex ...`, while Better-AO’s CLI has no `hooks` command yet and the web board only consumes the four coarse states `working`, `prompt`, `triage`, and `done`. I’m checking the home-domain mapping and any prior hook pattern so the plan can specify exactly where the hook-reported activity should land.

> AGENT

The CLI hook handlers in the existing `entire` tool have the same three event commands but their help does not document storage or payload details. I’m checking repo patterns for embedded assets and the current metadata format so the plan avoids inline hook JSON and writes activity where the dashboard already reads.

> AGENT

Two implementation choices materially affect the shape: the command namespace that the returned hooks should invoke, and whether hook activity should update workspace `.ao/activity.jsonl` only or the AO session JSON that the current dashboard already reads. I’m going to lock those choices before writing the final plan.

> AGENT

The “session metadata” option means the hook command updates the same JSON session record that the current Go dashboard already reads from `~/.agent-orchestrator/projects/<projectID>/sessions/<sessionID>.json`. Concretely, a Codex hook command would run with enough environment to identify the session, read that JSON file, update agent-activity fields there, and preserve all unrelated fields. Then `internal/ao/workspace.go` maps that updated metadata into the existing kanban columns without adding a second workspace-log reader first. This is the shortest path to visible kanban behavior, but it means hook commands need reliable session identity from env such as `AO_DATA_DIR`, `AO_PROJECT_ID`, and `AO_SESSION_ID`. The alternative `.ao/activity.jsonl` option is cleaner as an agent-local activity stream, but the current Better-AO web path does not read it yet. Choosing that means we also need to teach the workspace provider to find each session’s workspace and consume `.ao/activity.jsonl` during dashboard reads.

> AGENT

It can be in memory only if the hook command talks to a long-lived Better-AO process, for example via a local HTTP endpoint or IPC socket. A plain Codex hook command is a short-lived child process; once it exits, any in-process map is gone. The kanban board is also served by a separate process that may not be running when a hook fires, and it may restart after the hook fires. So durable storage is the safer base layer. The choices are really: - **Session metadata**: durable, already read by the dashboard, session-scoped. - **`.ao/activity.jsonl`**: durable, agent-local, but not currently read by this dashboard. - **In-memory via server endpoint**: lower disk writes, but only works while the server is running and reachable; it needs a durable fallback anyway or activity disappears across restarts. I would not make memory the source of truth. At most, memory can be a cache derived from session metadata or `.ao/activity.jsonl`.

> AGENT

That intent makes sense: the hook is reporting the current state, not writing history. To make “memory” work technically, the CLI hook command has to be a small reporter that sends the event to the long-lived Better-AO server, and the server keeps the current activity map in memory. The hook process itself cannot own the memory because it exits immediately. I’m going to inspect the server routing shape so the plan can specify the in-memory endpoint cleanly.

> AGENT

For an in-memory source of truth, the only remaining design choice is how the hook CLI finds the running Better-AO server. This is not discoverable from the repo because `start` allows `-addr`, and hooks may run outside the terminal environment that launched the server.

> AGENT

<proposed_plan> # Codex Hook Activity Design ## Summary Implement Codex activity hooks as ephemeral event reporters: Codex fires a hook, `better-ao hooks codex <event>` sends that event to the running Better-AO server, and the server keeps the latest activity state in memory. No activity history is persisted. `GetAgentHooks` only returns the Codex hook definitions; hook installation and merge with existing user hooks stays outside the plugin. ## Key Changes - Change `GetAgentHooks` to return structured hook definitions instead of `error`, for example `AgentHooks{Hooks map[string][]HookEntry}`. - Store Codex hook definitions in an embedded JSON asset based on `.codex/hooks.json`, not inline Go strings. - Return these Codex hooks: - `SessionStart` -> `better-ao hooks codex session-start` - `UserPromptSubmit` -> `better-ao hooks codex user-prompt-submit` - `Stop` -> `better-ao hooks codex stop` - Add a pure hook-merge helper for the future installer: - Preserve all existing hook entries and hook defs. - Upsert only Better-AO-owned hook commands. - If a Better-AO hook shares a hook group with user hooks, update only Better-AO’s hook def and do not change the group matcher. ## Runtime Activity Flow - Add `better-ao hooks codex session-start|user-prompt-submit|stop`. - The hook CLI drains stdin, maps the event, sends it to the running Better-AO server, prints `{}`, and exits `0` even if reporting fails so Codex hook behavior never regresses. - Event-to-kanban mapping: - `session-start` -> `working` - `user-prompt-submit` -> `working` - `stop` -> `prompt` - The Better-AO server keeps an in-memory map keyed by `projectID + sessionID`. - `GET /api/workspace` overlays this in-memory activity state onto matching sessions before returning the workspace, so the existing web kanban columns update without adding persistence. - Server discovery should use a runtime discovery file written by `better-ao start`, containing endpoint + short-lived local token. This file is not activity persistence; it only lets hook subprocesses …

> DEVELOPER

# Context from my IDE setup: ## Active file: internal/plugin/agent/codex/codex.go ## Open tabs: - codex.go: internal/plugin/agent/codex/codex.go - hooks.json: .codex/hooks.json - .gitignore: .gitignore - plugin.go: internal/plugin/plugin.go - agent.go: internal/plugin/agent/agent.go ## My request for Codex: we need to update this plan. Instead of having something like this `better-ao hooks codex session-start|user-prompt-submit|stop`, we are going to have `better-ao agent working|prompt|triage|done` and this is essentially to mutate the in-memory registered activity for an agent session.

> AGENT

I’ll revise the plan around the new command shape and check the current CLI surface once more so the replacement plan doesn’t assume an existing `agent` command.

> AGENT

<proposed_plan> # Codex Agent Activity Hooks ## Summary Update the Codex agent plugin plan so Codex hooks report Kanban activity through generic agent-state commands: - `better-ao agent working` - `better-ao agent prompt` - `better-ao agent triage` - `better-ao agent done` These commands will mutate the running Better-AO server’s in-memory activity state for the current agent session. The CLI process itself will not persist activity. ## Key Changes - Change `agent.GetAgentHooks` to return structured hook definitions instead of doing installation work. - Move Codex hook definitions into an embedded JSON asset under `internal/plugin/agent/codex`, not inline Go strings. - Codex hook mapping: - `SessionStart` -> `better-ao agent working` - `UserPromptSubmit` -> `better-ao agent working` - `Stop` -> `better-ao agent prompt` - Keep `triage` and `done` CLI states available for parity/manual/future agent events, even if Codex does not currently emit hooks for them. ## Runtime Activity Flow - Add a server-owned in-memory activity store keyed by project/session identity. - Add a local internal endpoint for activity updates, for example `POST /api/agent/activity`. - `better-ao start` exposes discovery details for hook CLIs, such as server URL and token, via a runtime discovery file. This file stores only connection metadata, not activity state. - `better-ao agent <state>` resolves session identity from environment, with flags for tests/manual use: - `BETTER_AO_PROJECT` - `BETTER_AO_SESSION_ID` - optional `--project` - optional `--session` - The Codex launch path must inject project/session identity into the Codex process environment so Codex hooks inherit it. - `/api/workspace` overlays the in-memory activity state onto returned sessions before the web Kanban board receives them. - Activity state is intentionally lost on server restart. ## Hook Installation Compatibility - `GetAgentHooks` only returns desired Codex hooks; it never reads or modifies the user workspace. - The hook installer must merge returned hooks into existing `.codex/hooks.json`. - Existing user hooks …

> DEVELOPER

# Context from my IDE setup: ## Active file: internal/plugin/agent/codex/codex.go ## Open tabs: - codex.go: internal/plugin/agent/codex/codex.go - hooks.json: .codex/hooks.json - .gitignore: .gitignore - plugin.go: internal/plugin/plugin.go - agent.go: internal/plugin/agent/agent.go ## My request for Codex: now tell me exactly what part of this plan is codex agent's responsibility?

> AGENT

I’ll pin this to the current interface boundaries instead of answering abstractly. I’m going to re-check the agent interface and Codex plugin shape so the responsibility split matches the code that exists.

> AGENT

The current interface still says `GetAgentHooks` installs/merges, but your stated boundary is different: Codex should describe its hooks, while another component installs them. I’ll frame the answer around that corrected boundary.

> AGENT

Codex agent’s responsibility is only the Codex-specific hook description layer. Concretely, that means: 1. Define which Codex-native hook events matter. - `SessionStart` - `UserPromptSubmit` - `Stop` 2. Map those Codex events to Better-AO’s generic activity commands. - `SessionStart` -> `better-ao agent working` - `UserPromptSubmit` -> `better-ao agent working` - `Stop` -> `better-ao agent prompt` 3. Implement `GetAgentHooks` in [codex.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/plugin/agent/codex/codex.go:88) so it returns those hook definitions. - It should not install hooks. - It should not merge `.codex/hooks.json`. - It should not mutate the workspace. - It should not talk to the server. 4. Keep the Codex hook payload in a real asset file, likely embedded with `go:embed`, instead of inline Go string literals. - That is Codex plugin responsibility because the hook schema/event names are Codex-specific. Everything else is not Codex agent responsibility: - `better-ao agent working|prompt|triage|done` CLI implementation: generic Better-AO CLI responsibility. - In-memory activity store: server/runtime responsibility. - POST endpoint for activity mutation: server responsibility. - Overlaying activity onto `/api/workspace`: workspace/server responsibility. - Preserving and merging pre-existing user hooks: hook installer responsibility. - Injecting `BETTER_AO_SESSION_ID` / `BETTER_AO_PROJECT` into the running process: launcher/runtime responsibility, unless we change the agent launch interface to let plugins return env too. One interface comment also needs to change: [agent.go](/Users/tanishqpalandurkar/Projects/better-ao/internal/plugin/agent/agent.go:74) currently says `GetAgentHooks` installs or merges hooks. Under your boundary, it should say it returns desired agent hook definitions for another component to install.

> DEVELOPER

So I was thinking, how does the activity detection is going to work end-to-end? We know that Codex agent CLI is going to emit events. We have registered some hooks to react to those events. These hooks are essentially publishers and they are going to publish the event representing your agent's current activity state, which is either one of the four already mentioned, that is working, prompt, triage, and done. So these publishers are going to publish these events and then there will be a broker in the backend side of this workflow. Not essentially a workflow, but like data flow. And that broker is going to route these events to a channel which is being subscribed by a context provider. This context provider is consumed by React children like sidebar component and the Kanban agent. I think this is the most optimal way of providing real-time updates of your currently running agent sessions. What do you think?

> AGENT

I’ll ground this against the current backend/web shape before giving a verdict, because the right answer depends on whether the app already has a real-time channel or only polling today.

> AGENT

The current app is still centered on `/api/workspace` plus TanStack Query; I don’t see an existing workspace event stream in the scan. That makes your broker/channel idea a good fit, but it should be integrated as a cache update path rather than a parallel source of truth.

> AGENT

Yes, the model is right. I would tighten one part: make the React context provider the subscription/bridge layer, not the authoritative data store. The clean end-to-end shape should be: 1. Codex emits a native hook event. 2. The installed Codex hook runs a publisher command like `better-ao agent working` or `better-ao agent prompt`. 3. That command resolves the current session identity from env, then posts a normalized activity event to the running Better-AO backend. 4. The backend validates the event, updates an in-memory activity store, and publishes an `AgentActivityChanged` message through an in-process broker. 5. The browser subscribes to a backend stream, ideally SSE/EventSource because this is server-to-client only. 6. A React provider listens to that stream and patches the existing workspace/session state consumed by the sidebar and Kanban board. The important adjustment: the provider should probably update the existing TanStack Query cache for `homeWorkspaceQueryKey`, not create a second parallel workspace state model. Today the frontend already treats `/api/workspace` as the workspace source and polls it every 5s in [workspace.ts](/Users/tanishqpalandurkar/Projects/better-ao/web/src/features/home/data/workspace.ts:8). Real-time activity should become a faster update path for that same data, while `/api/workspace` remains the reconnect/bootstrap truth. I would structure it like this: ```text Codex CLI hook -> better-ao agent <working|prompt|triage|done> -> POST /api/agent/activity -> ActivityStore.Set(project, session, state) -> ActivityBroker.Publish(activity.changed) -> GET /api/workspace overlays ActivityStore -> GET /api/workspace/events streams activity.changed -> React provider patches TanStack Query cache -> Sidebar + Kanban re-render from same workspace model ``` That gives you real-time updates without making the hook command, browser, or React context responsible for durable truth. The backend remains the owner of current in-memory activity, and `/api/workspace` still works after refresh, reconnect, or missed events. A few constraints I would keep explicit: - Events should be level-setting, not edge-only: `working` means “this session is now working,” not “a working event …

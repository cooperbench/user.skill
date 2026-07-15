[DEVELOPER]: my last run of drain-cycle looks like it stalled, have a look at this log message: 16:42:58 ABA-394 turn 43 · 3.9M tok (peak 121k) · 8m 16:43:05 ABA-394 turn 44 · 4.1M tok (peak 121k) · 8m 16:43:10 ABA-394 not-Done with commits: spawning finishing sub-agent however the watch output showed me that it exited: *Stop-guard satisfied** - `exec-state.json` now carries the `finish` section with `pr_urls: ["https://github.com/ababushkin/agent-skills-shaper/pull/56"]` (commit `0f2f6a8`). - Branch `ABA-394` is up to date with `origin/ABA-394`; both commits (`a7ecf78` skill rebalance, `0f2f6a8` exec-state finish) are pushed. **Linear status** Left at **In Progress** with the review-summary comment posted (id `c6800e18…`). Per repo governance ("not Done until committed and pushed to main") the issue should transition to Done only after PR #56 merges. Flagging this rather than transitioning early. === done: 45 turns, $4.07 ===

[AGENT]: I'll dig into the actual drain-cycle code to understand what happened here. Let me look at the orchestrator's completion/halt logic.

[AGENT]: Let me read the relevant orchestrator logic around the finishing sub-agent spawn.

[AGENT]: Let me check the `handoff.read` contract and whether the not-Done path ever consults existing `pr_urls`.

[AGENT]: Confirmed the root cause. Here's what happened — it's not really a stall, it's a **redundant finishing sub-agent spawn** caused by a collision between worker governance and the orchestrator's completion heuristic. ## What happened Your worker finished **correctly and completely**: - Ran `/shape:pr-finishing`, opened PR #56, pushed both commits - Wrote `exec-state.json` with `finish.pr_urls: [...PR#56]` - Posted the Linear review-summary comment - **Deliberately left the issue at "In Progress"** — per repo governance ("not Done until committed and pushed to *main*"), it correctly refused to transition to Done before PR #56 merges. That's the `=== done: 45 turns, $4.07 ===` clean exit you saw in the watch pane. Then the orchestrator re-read Linear (orchestrator.py:711) and hit this gate: ```python # orchestrator.py:726 if not is_done and _commits_beyond_base(worktree_path, base): ... console.worker_event(identifier, "not-Done with commits: spawning finishing sub-agent") ``` The check is only **(Linear state ≠ Done) AND (branch has commits)**. Both are true — because the worker *correctly* left it In Progress and *correctly* has commits. So the orchestrator concludes "committed but unfinished" and spawns a sonnet finishing sub-agent (orchestrator.py:737) to redo work that was already done. That redundant agent re-running `pr-finishing` against an already-submitted branch is the "stall" you're seeing. ## […]

[DEVELOPER]: also the linear ticket was marked as done, where as it should have been left in progress - i can't tell if thats an issue with linear or something else - i also see this file in the repo: .drain-guard-tripped

[AGENT]: Let me investigate both — the `.drain-guard-tripped` file and what marked the ticket Done.

[AGENT]: Let me check the finishing sub-agent's prompt — that's likely what marked the ticket Done.

[AGENT]: Both questions answered — and they're the **same bug** as before, plus an unrelated stale file. ## The Linear ticket marked Done — not a Linear issue, drain-cycle did it It was the redundant finishing sub-agent. The `build_finishing` prompt (prompt.py:117) hard-codes: ``` 6. Transition issue to Done via mcp__claude_ai_Linear__save_issue (state: "Done"). ``` Its only escape hatch (prompt.py:114) is "if the skill *could not submit*, leave In Progress." But PR #56 was already submitted and `pr_urls` was already in `exec-state.json` — so step 5 passed and step 6 dutifully marked it **Done**. So the full chain is: 1. **Original worker** ran `exec:pickup` with governance awareness ("not Done until merged to *main*"), opened PR #56, recorded `pr_urls`, and **deliberately left the issue In Progress**, posting "should transition to Done only after PR #56 merges." 2. **Orchestrator misfired** (orchestrator.py:726, the missing `pr_urls` guard from my first answer) → spawned the finishing sub-agent. 3. **Finishing sub-agent** saw `pr_urls` present and, per its prompt, **flipped the issue to Done** — overriding the exact governance decision the original worker got right. This is a **governance contradiction baked into two prompts:** - Worker / `exec:pickup`: *not Done until merged to main* → leave In Progress - `build_finishing` […]

[DEVELOPER]: the watcher also never showed me the sub-agent and the drain-cycle process is still "stuck" as if its in progress

[AGENT]: Let me check whether the process is actually still alive and how the sub-agent output is (not) being routed to the watch pane.

[AGENT]: Live process confirmed: **PID 6785, a `claude -p` started at 4:43PM with only 3.76s CPU** — that's the finishing sub-agent, spawned at 16:43:10 and still alive, idle/hung (not spinning). The orchestrator is blocked in `worker.run_issue` waiting on it. Let me see why the time cap didn't kill it and why the watch pane never showed it.

[AGENT]: Let me check the run-log and active limits config to confirm whether a time cap was even in play.

[AGENT]: Limits config shows `per_issue_seconds: 1800` (30 min) — so a wall-clock cap **is** set. PID 6785 should have been killed at ~17:13. The fact that it survived hours means the monitor isn't watching it. Let me check the process tree — is the parent orchestrator even still alive?

[AGENT]: PID 6785's detail came back empty — it may have just exited. Let me re-scan for live processes.

[AGENT]: PID 6785 is now **GONE** — and there's no live orchestrator or worker process at all. So nothing is actually running anymore; the finishing sub-agent exited sometime in the last few minutes. Let me read today's run-log to see how the orchestrator actually ended.

[AGENT]: Now I have the full, corrected picture from the run-log. Let me verify the timeline with the current time.

[AGENT]: Correction to my earlier "hung process" guess — the run-log tells the real story. It wasn't stuck; it was **invisibly working and has now finished** (16:50:35, ~90 seconds before now). Here's what actually happened on both points. ## Why the watcher never showed the sub-agent — a real blind spot The main worker and the finishing sub-agent run on **two different execution paths in `worker.run_issue`**: - **Main worker (watch mode):** the *external* path (worker.py:226). Its `claude` runs inside a **tmux pane under `tee`**, and drain-cycle reads the teed stream. That's the only thing the `-w` pane mirrors. - **Finishing sub-agent:** the *spawned* path. The orchestrator calls `run_issue(..., passthrough=console.AgentSink())` (orchestrator.py:737) with **no `external_stream` and no `kill_fn`**, so it's a plain `subprocess.Popen` (worker.py:272). Its output flows through `AgentSink → agent_line` to the orchestrator's Rich console (main stdout) — **never into the tmux watch pane.** So in watch mode the **entire recovery/finishing phase is invisible**. The pane froze on the worker's `=== done: 45 turns ===` frame and showed nothing for the next 7 minutes while real work happened off-screen. That blackout is what made it look stalled. ## It wasn't stuck — it was a legitimate 7-minute finishing pass The run-log entry: […]

[SYSTEM]: This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation. Summary: 1. Primary Request and Intent: The user is debugging a drain-cycle run for Linear issue ABA-394 that appeared to "stall." Across three messages the intent expanded into a full post-mortem of one run, covering four observed symptoms: - (1) The orchestrator logged "not-Done with commits: spawning finishing sub-agent" even though the watch pane showed the worker had exited cleanly ("=== done: 45 turns, $4.07 ==="). - (2) The Linear ticket ABA-394 was marked **Done** when it should have been left **In Progress**; user unsure whether this is a Linear bug or something else. - (3) A `.drain-guard-tripped` file appeared in the repo; user wants to know what it is. - (4) The watcher never showed the sub-agent, and the drain-cycle process appeared "stuck" as if still in progress. The intent is diagnosis/root-cause first; the user has NOT yet approved any code fix (I offered fixes and asked which governance rule is canonical). 2. Key Technical Concepts: - drain-cycle: a batch orchestrator that drains Linear issues end-to-end via `claude -p` worker sessions, in "stack" mode (Graphite […]

[DEVELOPER]: i've fixed the linear state, lets just fix the defects

[AGENT]: Let me read the orchestrator and handoff modules to make precise edits.

[AGENT]: Let me read the rest of the post-finishing logic to understand the not-Done path.

[AGENT]: This is more than a missing guard — it's an architectural mismatch, and I want to get the direction right before editing core control flow. Let me map the current behavior precisely. The orchestrator's success machinery (baton handoff, worktree teardown, log entry) all lives **inside** `if is_done:` (orchestrator.py:770–945). So the success signal is the Linear *Done* state. But the `exec:*` skill your main worker runs has already adopted the opposite governance — it submitted PR #56, recorded `pr_urls`, and deliberately **left the issue In Progress** ("Left at In Progress…"). That's the collision: the worker's contract is "In Progress until the PR merges," the orchestrator's contract is "Done = success." The finishing sub-agent exists to force the issue Done so the orchestrator's gate passes. So a minimal guard alone won't work: if I just skip the redundant finishing pass, the correctly-finished (In Progress + `pr_urls`) issue falls straight through to the not-Done **halt** at line 947 — reverting it and stopping the whole drain. The real fix is to make the orchestrator key success on **submission (`pr_urls` present)**, not on the Linear Done state. Before I restructure that gate, let me scope the blast radius in the tests.

[AGENT]: `test_orchestrator_finishing.py` is 38K — the core behavior I'm about to change is heavily covered. Let me read it and the finishing-success scenarios to understand exactly what's asserted.

[AGENT]: The test suite makes the design intent explicit: drain-cycle's current contract is **"Done = complete,"** and the finishing sub-agent exists to *force* Done. But the `exec:*` skill the worker runs has moved to **"leave In Progress until the PR merges"** — which is the governance you endorsed by reverting ABA-394. So the real defect is that the orchestrator keys success on the Linear *Done* state instead of on the *submission signal* (`pr_urls`). The clean fix is **additive**: accept a stack-mode worker that wrote `pr_urls` and stayed In Progress as *complete* (no finishing pass, no halt), while leaving the genuine "committed-but-unsubmitted" recovery untouched. Let me confirm no existing test already exercises the "stack + pr_urls + not-Done" combination, and check the prompt/stop-guard text assertions.

[AGENT]: The test landscape confirms the additive fix is safe: every existing not-Done/halt test runs with no `pr_urls` (or `no_stack=True`), so none exercises the "stack + `pr_urls` + In Progress" combination I'm about to treat as success. And `test_prompt.py:208` pins `"Done"` in `build_finishing`'s tail — so I'll make that prompt mode-aware (Done for push, In Progress for stack). Let me make the orchestrator edits first.

[AGENT]: Now the success gate and the redundant inner re-read:

[AGENT]: Now update the stack-no-PRs recovery's `build_finishing` call to pass `stack`:

[AGENT]: Now make `build_finishing` mode-aware — leave In Progress in stack mode (PR not merged yet), mark Done in push mode:

[AGENT]: Now the stop-guard stack block prompt — it also tells the agent to "transition the issue to Done":

[AGENT]: Now update the prompt tests for the mode-aware tail:

[AGENT]: Now check test_stop_guard.py for assertions on the changed prompt text:

[AGENT]: `test_stop_guard.py` only asserts on `"commit"` and `"exec-state.json"` — both still present. Now add the key orchestrator test: a stack worker that submits `pr_urls` and leaves the issue In Progress is accepted as complete, with no finishing pass.

[AGENT]: Now let me run the affected test suites to validate the orchestrator, prompt, and stop-guard changes:

[AGENT]: Wrong interpreter — this is a uv-tool project. Let me use its environment.

[AGENT]: All 46 pass. Now run the full suite to confirm nothing else regressed:

[AGENT]: Full suite green (373 passed). Defect #1 done. Now defect #3 — the stale `.drain-guard-tripped`:

[AGENT]: Defect #3 done (stale file referenced legacy `.drain-handoff.json`, gitignored, removed). Now defect #2 — the watch-pane blackout. Let me understand the console/watch architecture to scope the fix.

[AGENT]: Output all goes to stderr via Rich. Now let me understand how watch mode sets up the pane vs. the spawned path, to see how feasible routing the finishing agent into the pane is.

[AGENT]: Now I understand the wiring: the main worker gets a tmux pane (`watch_pane.open_session` → `external_stream`/`kill_fn`), but both finishing-recovery `run_issue` calls omit those **and** omit `on_progress` — so during finishing there's zero per-turn feedback. Let me check how the watch pane is laid out relative to the orchestrator's stderr, to know whether a stderr heartbeat is even visible in watch mode.

[AGENT]: The watch pane is a tmux **split** (`split-window`), so the orchestrator's stderr stays visible in the original pane alongside the worker's split. That means the operator *would* see a heartbeat from the orchestrator — but the finishing `run_issue` calls pass **no `on_progress`** (and emit no completion line), so for 7 minutes both panes went silent. Let me check `_worker_log_fields` so I can emit a meaningful completion line.

[AGENT]: Now I'll add live progress feedback (`on_progress`) and a completion line to both finishing-recovery spawns. Let me view the current not-Done block precisely:

[AGENT]: Now the stack-no-PRs site:

[AGENT]: Now add the `_log_finishing_done` helper next to `_worker_log_fields`:

[AGENT]: Let me add a regression assertion that the finishing completion line is emitted (the visibility fix):

[AGENT]: All 373 pass. Let me review the complete diff for correctness, especially the orchestrator control-flow changes:

[AGENT]: The control flow is sound: `post_spawn_state` is set unconditionally at the initial refresh, push-mode behavior is unchanged (`submitted` always `None` → gate reduces to `is_done`), and the In-Progress-submitted path correctly records `final_linear_state="In Progress"` and extends the baton. Let me run the linter if the project has one, and a final import check:

[AGENT]: No linter configured; imports clean; all 373 tests pass. The `orchestrator-enforced-completion` memory now describes superseded behavior (finishing agent forcing Done), so let me update it to avoid stale guidance.

[AGENT]: All three defects are fixed and the full suite (373 tests) is green. Nothing is committed yet. ## What changed **Defect #1 — governance collision (the real bug)** The orchestrator keyed "complete" on the Linear **Done** state, but the `exec:*` skill now leaves issues **In Progress** until the PR merges. That mismatch is what spawned the redundant finishing pass on ABA-394 and flipped it to Done. Fixed by making the orchestrator key on the **submission signal** (`pr_urls`) instead: - `orchestrator.py` — read `submitted = handoff.read(...)` up front; the not-Done recovery now fires only when `submitted is None`; the success gate is `if is_done or submitted is not None:`. A stack worker that submitted its PR and stayed In Progress is now accepted as complete (baton extended, `final_linear_state="In Progress"`), with no finishing pass. Push mode is unchanged (`submitted` is always `None` there → gate reduces to `is_done`). - `prompt.py` — `build_finishing` is now mode-aware (`stack=` param): stack mode tells the agent to **leave In Progress** (PR is the completion signal); push mode still marks Done. - `stop_guard.py` — the stack block-prompt no longer says "transition to Done." **Defect #2 — watch-pane blackout** The finishing sub-agent runs off the tmux split-pane, and […]
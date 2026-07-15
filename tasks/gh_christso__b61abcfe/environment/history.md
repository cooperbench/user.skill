> SYSTEM

# AGENTS.md instructions for /home/entity/projects/EntityProcess/agentv <INSTRUCTIONS> # AgentV Agent Guide This file is the root index for repo-facing agent instructions. It carries baseline rules that always apply plus a [Routing](#routing) table that maps your change to the deeper `.agents/*.md` guide you must read **before** starting that work. The rules in this file are a summary; each linked guide is authoritative for its area, so a matching Routing trigger means "read the guide," not "the summary is enough." Read [STRATEGY.md](STRATEGY.md) plus [ROADMAP.md](ROADMAP.md) before making product-boundary calls. ## Product Direction AgentV aims to be the repo-native, workspace-native evaluation framework for AI agents. - Repo-native evals: run against real repos, multi-repo workspaces, setup scripts, and existing harnesses. - Zero-infra local to CI: keep the default path lightweight so the same eval contract works on a laptop and in CI. - Portable run artifacts: treat run bundles, traces, and summaries as the source of truth for comparison, gating, and export. - Adapter boundaries: integrate with Phoenix, Harbor, Opik, and provider-specific systems through narrow adapters instead of absorbing their concepts into core. - AI-native extensibility: keep the core small and composable so engineers and coding agents can extend it with plugins, wrappers, and harness-specific glue. […]

> DEVELOPER

$coordinator av-y7eq.1 has the full config contract: .agentv/config.yaml, eval.yaml, field-level file://, scope distinction, execution.max_concurrency, rejected fields. - av-y7eq.2 through .7 each contain provider/runtime-specific implementation details and acceptance criteria. - av-y7eq.8 has the docs/examples requirements and explicitly references both the config and orchestration surfaces. implement those beads. use /goal on workers that need to do long running tasks.

> SYSTEM

<skill> <name>coordinator</name> <path>/home/entity/.agents/skills/coordinator/SKILL.md</path> --- name: coordinator description: Orchestrate multiple worktree agents. Spawn, monitor, communicate, and merge. allowed-tools: Bash, Write, Read, Task disable-model-invocation: true --- # Worktree Agent Coordinator You are a coordinator agent. You orchestrate multiple worktree agents using `workmux` CLI commands. You do NOT implement tasks yourself. You spawn agents, monitor them, send instructions, and trigger merges. ## Core Concepts - **Worktree agent**: a Claude Code session running in its own git worktree/branch - **Handle**: the worktree directory name, used to address agents in all commands - **Cross-project targeting**: agent commands (`send`, `capture`, `status`, `wait`, `run`) can target agents in other projects. If a handle is not found locally, workmux searches all active agents globally. Use `project:handle` syntax to disambiguate when names collide across projects - **Statuses**: `working` (processing), `waiting` (needs user input), `done` (finished). Set automatically by agent hooks. Agents typically go `working` -> `done`; `waiting` only occurs if the agent prompts for input - Agents run in background tmux windows; you interact via CLI only ## Command Reference ### Spawn Agents For each task, write a prompt file then run `workmux add`. You are a dispatcher. Do NOT read source files, edit code, or implement tasks yourself. […]

> AGENT

I’m using the coordinator skill for the fan-out/fan-in workflow, and the Beads workflow because these tasks are already scoped as beads. I’ll first refresh repo state and read the required coordination instructions, then I’ll inspect the bead payloads and dispatch worktree agents rather than editing code here.

> AGENT

The primary checkout is behind `origin/main` by 5 commits, so I’ll base spawned worktrees from `origin/main` rather than the stale local `main`. Next I’m reading the workflow routing guide and the bead details so the worker prompts carry the current contract instead of relying on chat context.

> AGENT

The bead graph has `.1` as the shared schema/config blocker for the provider/runtime beads, and `.8` is downstream docs/examples. I’m gathering the remaining bead details and the two plan files those beads reference before writing the worker prompts.

> AGENT

The plan files referenced by the beads are not present in the stale local `main`, but they likely landed in the 5 commits now on `origin/main`. I’m reading them from `origin/main` directly and will base workers there.

> AGENT

I’m going to dispatch the schema/config prerequisite first. Starting the provider/runtime beads before `.1` lands would force workers to guess at the shared loader and normalized types, so I’ll fan out only after that base branch is merged or there’s a stable integration branch to build on.

> AGENT

The first prompt is written with the bead contract, routing docs, and `/goal` instruction embedded. I’m spawning that worktree from `origin/main` now and will confirm it starts before waiting on it.

> AGENT

The `av-y7eq-1-config` worker is created on `origin/main`. I’m checking that it transitions to working and then I’ll monitor/capture output for early blockers.

> AGENT

The schema worker is running. While it works, I’ll prepare downstream prompt files but hold their launch until `.1` has a mergeable base, so provider workers can build on the actual contract instead of reimplementing it.

> AGENT

I’m staging the downstream prompts now. Each one tells the worker to claim only its bead, read the repo routing docs and the relevant plan files, start a `/goal`, and leave branch/test evidence rather than marking beads closed prematurely.

> AGENT

Downstream prompts are ready, but I’m holding them. The next decision point is whether the `.1` worker finishes cleanly enough to use its branch as the base for result-envelope and SDK/runtime workers.

> AGENT

The `.1` worker claimed the bead with metadata, installed dependencies, and found the existing config-loader/schema/test surfaces. It is now editing that narrow area, which is the right scope for the prerequisite.

> AGENT

I’m waiting on the prerequisite worker with a timeout rather than blocking indefinitely. If it stalls or asks for input, I’ll capture the pane and redirect it.

> AGENT

The worker is still running. I’ll sample its output now to check whether it is making progress or sitting on a failing gate.

> AGENT

The worker has identified two validation paths and is adding a shared normalized config graph rather than touching provider execution. That keeps `.1` focused and should reduce merge pressure downstream.

> AGENT

Still waiting on `.1`. I’ll keep it as the only active implementation worker until it reaches tests or asks for input.

> AGENT

It’s been a few more minutes, so I’m checking the pane again for current phase and any failing command output.

> AGENT

The worker is now editing, specifically around a shared config-graph loader and `execution.max_concurrency` validation. No blocker yet.

> AGENT

I’m giving it more time to finish the edit/test loop before spawning anything else. The downstream branches are queued, but they still need this base.
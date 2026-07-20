> DEVELOPER

Lets rethink in detail about the runtime layer for forge execution. The goal is to for forge to become an agentic platform backbone where Agents are provided to operate on repositories as well as to create new projects from entirety, all the while providing first class support on obervability, security and an optimized and fast runtime that can accommodate numerous agents, all the while providing sidecar type capabilities like key vault, common mcp support, extensions for agents, skills, etc. 

I have some options I want to brainstorm like using Cloudflare infrastructure, using kubernetes, using nix os, docker. 
Using agent teams lets try to come up with a high level plan on how to convert/leverage the existing codebase

> TOOL

tool_use Skill
id: toolu_01EDeSFTwjaAHVydb3DFYB4Q
```json
{
  "skill": "superpowers:brainstorm"
}
```

> TOOL

tool_result
id: toolu_01EDeSFTwjaAHVydb3DFYB4Q
```
Launching skill: superpowers:brainstorm
```

> TOOL

tool_use Skill
id: toolu_017M2kFF6HYtn3iroipQi1ad
```json
{
  "skill": "superpowers:brainstorming"
}
```

> TOOL

tool_result
id: toolu_017M2kFF6HYtn3iroipQi1ad
```
Launching skill: superpowers:brainstorming
```

> TOOL

tool_use ToolSearch
id: toolu_016xLvJ44eHHf6LASvwwei6r
```json
{
  "query": "select:TaskCreate,TaskGet,TaskList,TaskUpdate",
  "max_results": 4
}
```

> TOOL

tool_result
id: toolu_016xLvJ44eHHf6LASvwwei6r
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskGet"
}
{
  "type": "tool_reference",
  "tool_name": "TaskList"
}
{
  "type": "tool_reference",
  "tool_name": "TaskUpdate"
}
```

> AGENT

Let me set up the brainstorming process and start exploring the project context.

> TOOL

tool_use TaskCreate
id: toolu_01SMSUzBgi14Lh7WDXm1R5pK
```json
{
  "subject": "Explore project context",
  "description": "Check files, docs, recent commits, and understand the current forge architecture and runtime layer",
  "activeForm": "Exploring project context"
}
```

> TOOL

tool_result
id: toolu_01SMSUzBgi14Lh7WDXm1R5pK
```
Task #1 created successfully: Explore project context
```

> TOOL

tool_use TaskCreate
id: toolu_01D8GaZnzV2qJhoUwSJYKkXM
```json
{
  "subject": "Ask clarifying questions",
  "description": "One at a time, understand purpose, constraints, success criteria for the runtime platform",
  "activeForm": "Asking clarifying questions"
}
```

> TOOL

tool_result
id: toolu_01D8GaZnzV2qJhoUwSJYKkXM
```
Task #2 created successfully: Ask clarifying questions
```

> TOOL

tool_use TaskCreate
id: toolu_01JQCPU99PxAvUGM2B6dY4CC
```json
{
  "subject": "Propose 2-3 approaches",
  "description": "Present different runtime architecture approaches with trade-offs and recommendation",
  "activeForm": "Proposing approaches"
}
```

> TOOL

tool_result
id: toolu_01JQCPU99PxAvUGM2B6dY4CC
```
Task #3 created successfully: Propose 2-3 approaches
```

> TOOL

tool_use TaskCreate
id: toolu_01GYid5Si8eL5VCAj8oQFWBy
```json
{
  "subject": "Present design",
  "description": "Present the design in sections, get user approval after each section",
  "activeForm": "Presenting design"
}
```

> TOOL

tool_result
id: toolu_01GYid5Si8eL5VCAj8oQFWBy
```
Task #4 created successfully: Present design
```

> TOOL

tool_use TaskCreate
id: toolu_014p9WfEnhuX6o8kpekm8BV2
```json
{
  "subject": "Write design doc",
  "description": "Save validated design to docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md and commit",
  "activeForm": "Writing design doc"
}
```

> TOOL

tool_result
id: toolu_014p9WfEnhuX6o8kpekm8BV2
```
Task #5 created successfully: Write design doc
```

> TOOL

tool_use TaskCreate
id: toolu_01CbtSwSPFtnJzpDsezD4mGr
```json
{
  "subject": "Spec review loop",
  "description": "Dispatch spec-document-reviewer subagent, fix issues until approved (max 5 iterations)",
  "activeForm": "Running spec review loop"
}
```

> TOOL

tool_result
id: toolu_01CbtSwSPFtnJzpDsezD4mGr
```
Task #6 created successfully: Spec review loop
```

> TOOL

tool_use TaskCreate
id: toolu_0161xqnJ8r7YtxgR2BiKPHDh
```json
{
  "subject": "User reviews written spec",
  "description": "Ask user to review the spec file before proceeding to implementation planning",
  "activeForm": "Awaiting user spec review"
}
```

> TOOL

tool_result
id: toolu_0161xqnJ8r7YtxgR2BiKPHDh
```
Task #7 created successfully: User reviews written spec
```

> TOOL

tool_use TaskCreate
id: toolu_01B5qh2UatRL5eAzhtN8M7Kz
```json
{
  "subject": "Transition to implementation",
  "description": "Invoke writing-plans skill to create implementation plan",
  "activeForm": "Transitioning to implementation"
}
```

> TOOL

tool_result
id: toolu_01B5qh2UatRL5eAzhtN8M7Kz
```
Task #8 created successfully: Transition to implementation
```

> TOOL

tool_use TaskUpdate
id: toolu_01DAj4UYbTKUcKEsJFtXcMTs
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01DAj4UYbTKUcKEsJFtXcMTs
```
Updated task #1 status
```

> AGENT

Now let me explore the current codebase to understand the existing runtime architecture.

> TOOL

tool_use Agent
id: toolu_01EVP2yA2n1u84nP7MYcqYmh
```json
{
  "description": "Explore forge runtime architecture",
  "subagent_type": "Explore",
  "prompt": "Very thorough exploration of the forge project runtime layer. I need to understand:\n\n1. **Current execution model**: How does forge currently execute agents? Look at src/orchestrator/, src/dag/, src/swarm/, src/factory/pipeline/ — how are Claude processes spawned, managed, and coordinated?\n\n2. **Process lifecycle**: How are Claude CLI processes started, monitored, and terminated? What's the permission model? Look for CLAUDE_CMD, process spawning, stdin/stdout handling.\n\n3. **Resource management**: How does forge handle concurrency limits, memory, parallel execution? Look at the DAG scheduler and swarm executor.\n\n4. **State and persistence**: How is state persisted between phases/iterations? Look at src/orchestrator/state.rs, the factory database.\n\n5. **Networking/API layer**: What does the factory API server look like? How does WebSocket communication work? Look at src/factory/api.rs, src/factory/server.rs, src/factory/ws.rs.\n\n6. **Configuration**: What environment variables and config exist? Look at src/forge_config.rs.\n\n7. **Current limitations**: What are the pain points or architectural constraints in the current design?\n\n8. **Dependencies**: Check Cargo.toml for the full dependency tree.\n\nProvide a detailed summary of findings for each area."
}
```

> TOOL

tool_use Agent
id: toolu_01S3iff3GPGmEUSys5E4jcXX
```json
{
  "description": "Explore forge spec and docs",
  "subagent_type": "Explore",
  "prompt": "Very thorough exploration of forge project documentation and specs. Read these files and summarize key architectural decisions and design goals:\n\n1. .forge/spec.md — the main architecture spec\n2. docs/context-graph.md — subsystem context graph\n3. docs/context-graph-file-deps.md — file-level dependency graph\n4. README.md — project overview and usage\n5. Any files in docs/ directory — check what documentation exists\n6. Any investigation documents in docs/investigations/\n\nI need to understand:\n- What is the current architectural vision?\n- What are the stated design goals?\n- What subsystems exist and how do they relate?\n- Are there any documented plans for evolution of the runtime?\n- What does the investigation docs/ directory contain?\n\nProvide a comprehensive summary."
}
```

> TOOL

tool_result
id: toolu_01S3iff3GPGmEUSys5E4jcXX
```
Excellent. Let me now compile a comprehensive summary based on all the documentation I've read. Let me create my final report:

## Comprehensive Summary: Forge Architecture, Design Goals, and Vision

Based on thorough exploration of the primary documentation files (`.forge/spec.md`, `docs/context-graph.md`, `docs/context-graph-file-deps.md`, `README.md`, design documents, and investigation reports), here is a structured overview of Forge's architectural vision and design decisions:

---

### 1. **Core Architectural Vision**

**What is Forge?** Forge is an AI-powered development orchestrator that transforms project specifications into executable phases and runs Claude iteratively until completion. It embodies disciplined agentic development with:

- **Phase-based execution** — breaking specs into sequential or parallel tasks with iteration budgets
- **Calm gating** — thoughtful approval mechanisms and permission modes
- **Optimized resource usage** — context compaction, checkpoint recovery, and signal parsing
- **Disciplined feedback loops** — progress signaling, blocker detection, and pivot management

**Not just an automation tool** — Forge is designed as a production-grade **development platform** that scales from local script execution to full team orchestration and self-implementing issue tracking (Factory).

---

### 2. **Stated Design Goals**

From README and design documents:

1. **Phase-Based Complexity Decomposition** — Break complex projects into manageable sequential units with iteration […]

> TOOL

tool_result
id: toolu_01EVP2yA2n1u84nP7MYcqYmh
```
Perfect! Now I have a comprehensive understanding. Let me create a detailed summary of the findings:

## FORGE RUNTIME LAYER - COMPREHENSIVE ANALYSIS

This is a detailed technical summary of the Forge orchestrator's runtime architecture after thorough code exploration.

---

### 1. CURRENT EXECUTION MODEL

**Sequential (Runner-based) Execution:**
- Primary: `src/orchestrator/runner.rs` (ClaudeRunner) implements single-phase sequential execution
- File: `/home/<USER>/Projects/AI/forge/src/orchestrator/runner.rs` (70.7 KB)
- Pattern: Single phase → iterate with budget until `<promise>DONE</promise>` or budget exhausted
- Command spawning: `tokio::process::Command` at line 511-559
- stdin writing: direct prompt injection via pipe
- stdout parsing: line-by-line streaming with signal extraction

**DAG-based Parallel Execution:**
- File: `/home/<USER>/Projects/AI/forge/src/dag/executor.rs` (57.2 KB)
- Architecture: `DagScheduler` (computes dependency waves) + `DagExecutor` (spawns async tasks)
- Concurrency model: **Semaphore-gated with max_parallel limit** (default: 4)
  - Not wave-based barriers — waves are for reporting only
  - Real gate: `tokio::sync::Semaphore` limiting concurrent phase executions
- Dependency resolution: phases ready as soon as **all specific predecessors** complete
- Fail-fast: `active_tasks.drain()` cancels ALL in-flight tasks if fail_fast=true
- Configuration: `DagConfig` with max_parallel, fail_fast, swarm_enabled, review settings

**Swarm (Multi-agent) Execution:**
- File: `/home/<USER>/Projects/AI/forge/src/swarm/executor.rs` (150 lines)
- Purpose: Delegate a phase to Claude Code swarm for parallel micro-tasks
- Flow:
  1. […]

> TOOL

tool_use TaskUpdate
id: toolu_01DqJgsWziWXd9VNxJWDMCKV
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01DqJgsWziWXd9VNxJWDMCKV
```
Updated task #1 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01Kt4pzo5mcGHB4iAXeZ5diH
```json
{
  "taskId": "2",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01Kt4pzo5mcGHB4iAXeZ5diH
```
Updated task #2 status
```

> AGENT

I've done a deep dive into the current forge codebase. Here's what I'm working with:

**Current state:** Forge is a Rust-based orchestrator that spawns Claude CLI processes, manages them via tokio async, persists state in append-only logs + SQLite/Turso, serves a Factory Kanban UI over axum/WebSocket, and has DAG-based parallel execution. It's fundamentally a **single-machine, process-spawning architecture** — every agent is a `tokio::process::Command` on the host.

**Your vision** is to evolve this into an **agentic platform backbone** with: multi-agent runtime at scale, observability, security, sidecar capabilities (key vault, MCP, extensions), and you want to explore Cloudflare, Kubernetes, NixOS, and Docker as infrastructure options.

This is a large scope. Before I explore approaches, I want to understand the constraints and priorities better.

---

Here's my first question:

**What's your primary deployment target?** The options you listed suggest different audiences:

- **(A) Self-hosted / on-prem** — Teams run forge on their own infra (k8s clusters, bare metal). Maximum control, but you own the operational complexity.
- **(B) Cloud-native SaaS** — You host forge as a managed platform (think Vercel for agentic dev). Users connect repos, forge runs agents in your cloud.
- **(C) Hybrid** — A lightweight local CLI that delegates heavy […]

> DEVELOPER

lets start with approach A

> AGENT

Good — self-hosted/on-prem gives us the most architectural freedom and aligns with forge's current single-machine model as a starting point.

Next question:

**What's the target scale you want to support?** This heavily influences whether we need a full orchestration layer (k8s) or can get by with lighter-weight container management:

- **(A) Single node, many agents** — One beefy machine running 10-50 concurrent agents. Docker for isolation, but no cluster orchestration needed. This is the natural next step from where forge is today.
- **(B) Small cluster, dozens of agents** — 2-5 nodes, 50-200 concurrent agents. Need service discovery, scheduling, and some form of cluster management.
- **(C) Large cluster, hundreds+ of agents** — Full k8s-style orchestration, autoscaling, multi-tenant workloads, resource quotas per team/project.

Where on this spectrum are you targeting initially, and where do you want to grow toward?

> DEVELOPER

we want to ensure that the common runtime for the agents provide things like auth, cache, access to other services, tools for agents to execute, etc

> AGENT

That clarifies a lot — you're designing a **platform runtime** not just a process scheduler. The agents are the workload, but the value is in the shared services layer that every agent gets access to.

Let me make sure I understand the service categories you're envisioning. **Which of these are must-haves vs. nice-to-haves for the initial runtime?**

- **Auth / Identity** — Agent-level identity (each agent gets credentials), scoped permissions (repo X read-only, repo Y read-write), secrets injection (API keys, tokens). Does the runtime authenticate agents to external services, or do agents bring their own creds?

- **Cache** — Shared cache across agents (e.g., "agent A already fetched this file/API response, agent B can reuse it"). Is this more about LLM response caching, artifact caching (build outputs, git objects), or general key-value state sharing between agents?

- **Tool registry** — Agents can discover and invoke tools provided by the platform (MCP servers, custom executors, linters, test runners, deployment tools). Are you thinking of a centralized tool catalog that the runtime manages, or per-project tool configurations?

- **Service mesh / sidecar** — Each agent gets a sidecar that proxies access to shared services (vault, cache, MCP, logging). Is the mental model […]

> DEVELOPER

all of the above, the agent to agent communication is crucial for autonmous spinning of the agents by the primary agent

> AGENT

This is shaping up to be a significant platform. The agent-to-agent communication with autonomous spawning is the key architectural differentiator — the primary agent isn't just executing a plan, it's dynamically composing a team at runtime.

Let me make sure I understand the agent lifecycle model:

**When a primary agent decides to spawn a sub-agent, what should happen?**

- **(A) Full isolation** — Each sub-agent gets its own container/sandbox with its own filesystem, network namespace, and sidecar. Communicates with parent and siblings only through the platform's message bus. Heavier, but strong security boundaries.

- **(B) Shared workspace, isolated process** — Sub-agents share a filesystem (or git worktree) but run as separate processes with their own identity/credentials. Communication via shared state + message passing. Lighter weight, closer to how forge works today with swarm.

- **(C) Hierarchical namespaces** — Primary agent gets a "namespace" with resource quotas. Sub-agents inherit the namespace but get their own identity. Parent can see/control children, siblings can communicate within the namespace, but cross-namespace is gated. Think k8s namespace model.

Which feels right? And a follow-up — when a sub-agent spawns its *own* sub-agent (grandchild), should that be:
- Allowed freely (tree of arbitrary depth)
- Capped […]

> DEVELOPER

B and lets require a parent approval after a certain cap on total number of agents spawned

> AGENT

Good decisions. Shared workspace with isolated processes keeps things fast and practical, and the spawn cap with parent approval prevents runaway agent proliferation.

One more question before I move to approaches:

**What's your stance on the underlying isolation technology?**

You mentioned Docker, Kubernetes, and NixOS. Given what we've established (self-hosted, shared workspace, isolated processes, rich sidecar services), here's how I'm thinking about each:

- **Docker** — Natural fit for process isolation + sidecar pattern. Each agent is a container, sidecars provide services. Docker Compose or direct `bollard` API (which forge already uses) for orchestration. Limitation: single-node without something on top.

- **Kubernetes** — Gives you multi-node scheduling, namespaces, service mesh, secrets management, resource quotas out of the box. But it's a heavy dependency for self-hosted users and the pod startup latency (seconds) may be too slow for dynamic agent spawning.

- **NixOS / Nix** — Reproducible environments rather than isolation. Great for "every agent gets the exact same toolchain" but doesn't give you process isolation or service mesh natively. More of a build/environment layer than a runtime layer.

- **Lightweight alternative** — Use Linux namespaces directly (via something like `bubblewrap` or `systemd-run`) for process isolation without full container overhead. Sub-second […]

> DEVELOPER

Can Nix be used as the DSL layer to spin up infrastrucutre for agents with bespoke approvals?

> AGENT

That's a really interesting angle. Using Nix not as the runtime, but as the **declarative specification layer** — "here's what this agent needs" expressed as a Nix expression, which then gets evaluated and materialized into an actual runtime environment.

Here's how that could work:

**Nix as Agent Environment DSL:**
```nix
# agent-profile: security-reviewer
{ forgeLib, ... }:
forgeLib.mkAgent {
  name = "security-reviewer";
  tools = [ "semgrep" "trivy" "gh" ];
  mcp-servers = [ "github" "filesystem" ];
  secrets = [ "GITHUB_TOKEN" ];  # ← requires approval
  resources = { cpu = 2; memory = "4Gi"; };
  permissions = {
    repo = "read-only";
    network = [ "api.github.com" ];  # ← allowlisted egress
  };
}
```

**What makes this powerful:**
- **Pure and evaluable** — Nix expressions can be evaluated *without* executing anything. You can inspect exactly what an agent will have access to before approving it.
- **Composable** — Base profiles that agents inherit from, with per-spawn overrides.
- **Reproducible** — Same Nix expression always produces the same environment. No "works on my machine."
- **Auditable** — The approval isn't "can this agent run?" — it's "here's the exact manifest of capabilities, do you approve this contract?"

**The approval flow would be:**
1. […]

> DEVELOPER

Lets use Nix - thanks

> AGENT

Clear. Nix as the declarative DSL for agent environments, with the approval model built on top of evaluated Nix expressions.

Last clarifying question before I propose approaches:

**How do you see the relationship between the existing Rust orchestrator and the new runtime?**

- **(A) Rust core stays, runtime wraps around it** — The existing forge binary remains the brain (DAG scheduling, state, reviews, Factory). The Nix+Docker runtime is a new execution backend that forge delegates to. Forge tells the runtime "spin up this agent with this profile," runtime handles isolation/services/sidecars. Minimal rewrite.

- **(B) Rust core evolves into the runtime** — The sidecar services (auth, cache, tool registry, message bus) are built in Rust as part of forge itself. Nix defines environments, Docker provides isolation, but forge's tokio runtime is the service mesh. More integrated, more work.

- **(C) Split architecture** — Forge CLI remains the user-facing tool (plan, generate, run). A separate **forge-runtime daemon** (also Rust) manages the agent lifecycle, sidecar services, and inter-agent communication. The CLI talks to the daemon. Clean separation of concerns.

Which direction?

> DEVELOPER

C

> AGENT

Good. Clean separation — CLI for user interaction, daemon for agent lifecycle and platform services.

I now have a clear picture. Let me propose approaches.

> TOOL

tool_use TaskUpdate
id: toolu_01Vnu7fiSRfniXCqaHcY2YwX
```json
{
  "taskId": "2",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01Vnu7fiSRfniXCqaHcY2YwX
```
Updated task #2 status
```

> TOOL

tool_use TaskUpdate
id: toolu_019KxUzKvMTWnrxo6uLUiRxy
```json
{
  "taskId": "3",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_019KxUzKvMTWnrxo6uLUiRxy
```
Updated task #3 status
```

> AGENT

## Three Approaches

### Approach A: Nix-Native Runtime (Recommended)

**Core idea:** The forge-runtime daemon is a Rust service that speaks Nix natively. Agent environments are Nix expressions. The daemon evaluates them, materializes environments via `nix build`, and runs agents inside lightweight Linux namespaces (bubblewrap/systemd-nspawn) with bind-mounted workspaces. Sidecar services (auth, cache, MCP, message bus) run as long-lived processes in the daemon, exposed to agents via Unix sockets.

**Stack:**
- `forge` CLI → gRPC/Unix socket → `forge-runtime` daemon
- Daemon: Rust + tokio, manages agent lifecycle
- Environments: Nix flake per agent profile, evaluated and cached
- Isolation: `bubblewrap` (or `systemd-run --scope`) — sub-second spawn, shared filesystem via bind mounts
- Services: Auth proxy, Redis-like cache, MCP router, message bus — all in-process or as managed child processes
- Inter-agent comms: Message bus over Unix domain sockets (pub/sub + request/reply)

**Pros:** Fast agent spawning (<1s), Nix gives full reproducibility + declarative approval, no Docker dependency, tight integration between daemon and services.

**Cons:** Linux-only for namespace isolation (macOS would need Docker fallback), building `forgeLib` Nix library is upfront work, bubblewrap less battle-tested than Docker for security isolation.

---

### Approach B: Nix + Docker Hybrid

**Core idea:** Nix defines what goes into […]

> DEVELOPER

lets go with the recommendations

> TOOL

tool_use TaskUpdate
id: toolu_016Ph75aDQVqsdiMsM515FH6
```json
{
  "taskId": "3",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_016Ph75aDQVqsdiMsM515FH6
```
Updated task #3 status
```

> TOOL

tool_use TaskUpdate
id: toolu_013HhQjo9n5SCzuXd1cxYeVr
```json
{
  "taskId": "4",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_013HhQjo9n5SCzuXd1cxYeVr
```
Updated task #4 status
```

> AGENT

Approach A it is — Nix-Native Runtime with Docker fallback. Let me present the design section by section. I'll wait for your approval on each before moving on.

---

## Section 1: System Architecture Overview

**Three-process split:**

```
┌─────────────┐       gRPC/UDS        ┌──────────────────┐
│  forge CLI   │◄─────────────────────►│  forge-runtime   │
│  (user-facing)│                      │  (daemon)        │
└─────────────┘                        │                  │
                                       │  ┌────────────┐  │
                                       │  │ Agent Mgr  │  │
                                       │  │ Nix Eval   │  │
                                       │  │ Svc Router │  │
                                       │  └─────┬──────┘  │
                                       └────────┼─────────┘
                                                │
                          ┌─────────────────────┼─────────────────────┐
                          │                     │                     │
                    ┌─────▼─────┐         ┌─────▼─────┐        ┌─────▼─────┐
                    │  Agent 0  │◄───────►│  Agent 1  │◄──────►│  Agent N  │
                    │ (primary) │  msg    │ (spawned) │  msg   │ (spawned) │
                    │           │  bus    │           │  bus   │           │
                    └─────┬─────┘         └─────┬─────┘        └─────┬─────┘
                          │                     │                    │
                    ┌─────▼─────────────────────▼────────────────────▼─────┐
                    │              Shared Services (via UDS)               │
                    │  Auth │ Cache │ MCP Router │ Key Vault │ Tool Reg    │
                    └─────────────────────────────────────────────────────┘
```

**Component responsibilities:**

| Component | Role |
|-----------|------|
| `forge` CLI | User interaction, plan/generate/run commands, talks to daemon via gRPC |
| `forge-runtime` daemon | Agent lifecycle, Nix evaluation, service routing, approval gating, state persistence |
| Agent processes | Claude CLI instances running inside Nix-materialized, namespace-isolated environments |
| Shared services | […]

> DEVELOPER

yes

> AGENT

## Section 2: Agent Lifecycle & Nix Environment Model

**Agent profiles as Nix expressions:**

```nix
# forge-profiles/default.nix
{ forgeLib, ... }:
{
  base = forgeLib.mkAgent {
    name = "base";
    tools = [ "git" "gh" "ripgrep" "fd" ];
    mcp-servers = [];
    secrets = [];
    resources = { cpu = 1; memory = "2Gi"; };
    permissions = {
      repo = "read-write";
      network = [];  # no egress by default
      spawn = { max-children = 5; require-approval-after = 3; };
    };
  };

  security-reviewer = forgeLib.mkAgent {
    name = "security-reviewer";
    inherit (base) tools;
    tools = base.tools ++ [ "semgrep" "trivy" "bandit" ];
    mcp-servers = [ "github" ];
    secrets = [ "GITHUB_TOKEN" ];
    resources = { cpu = 2; memory = "4Gi"; };
    permissions = {
      repo = "read-only";
      network = [ "api.github.com" "*.semgrep.dev" ];
      spawn = { max-children = 0; };  # leaf agent, can't spawn
    };
  };

  implementer = forgeLib.mkAgent {
    name = "implementer";
    tools = base.tools ++ [ "cargo" "rustc" "nodejs" "npm" ];
    mcp-servers = [ "filesystem" "github" ];
    secrets = [ "GITHUB_TOKEN" "NPM_TOKEN" ];
    resources = { cpu = 4; memory = "8Gi"; };
    permissions = {
      repo = "read-write";
      network = [ "registry.npmjs.org" "crates.io" ];
      spawn = { max-children = […]

> DEVELOPER

yes

> AGENT

## Section 3: Shared Services Architecture

**All services are managed by the daemon and exposed to agents via Unix domain sockets. Agents never access services directly — the daemon mediates everything.**

### 3.1 Auth Proxy

```
Agent → /run/forge/agent-$ID/auth.sock → Daemon Auth Service → External APIs
```

- Each agent has an **identity token** issued by the daemon at spawn time (JWT, short-lived, scoped to the agent's manifest permissions)
- When an agent needs to call an external API (GitHub, npm registry, etc.), it goes through the auth proxy
- The proxy checks: is this agent allowed to reach this host? Does it have the required secret?
- Secrets are **never injected as environment variables** — agents request them at runtime through the vault socket, and the proxy handles injection into outbound requests
- Audit log: every external API call is logged with agent ID, target, timestamp

### 3.2 Key Vault

```
Agent → /run/forge/agent-$ID/vault.sock → Daemon Vault Service → Encrypted Store
```

- Secrets stored encrypted at rest in `$FORGE_STATE_DIR/vault.db` (SQLite + age/AEAD encryption)
- Agent can only access secrets listed in its Nix manifest (enforced by daemon, not by the agent)
- API: `get_secret(name) → value` — daemon […]

> DEVELOPER

yes

> AGENT

## Section 4: Daemon Internals & State Management

**The `forge-runtime` daemon is a single Rust binary with these internal subsystems:**

```
forge-runtime process
├── gRPC Server          (accepts CLI + agent connections)
├── Agent Manager         (lifecycle, spawn tree, approval gates)
├── Nix Evaluator         (shell-out to nix eval/build, result caching)
├── Runtime Backend       (BwrapRuntime | DockerRuntime, trait-dispatched)
├── Service Manager       (starts/stops/monitors shared services)
├── Message Bus           (in-process pub/sub with UDS bridging)
├── Telemetry Collector   (logs, metrics, traces, audit)
├── State Store           (SQLite for durable state)
└── Policy Engine         (evaluates manifests against project/global policies)
```

### 4.1 Agent Manager

Maintains the **agent tree** in memory:

```rust
struct AgentTree {
    agents: HashMap<AgentId, AgentNode>,
    root: Option<AgentId>,
}

struct AgentNode {
    id: AgentId,
    parent: Option<AgentId>,
    children: Vec<AgentId>,
    manifest: AgentManifest,
    handle: AgentHandle,       // PID, cgroup, namespace refs
    status: AgentStatus,       // Pending | Running | Completed | Failed
    spawned_at: Instant,
    spawn_count: u32,          // how many children this agent has spawned
    resource_usage: ResourceSnapshot,  // last sampled CPU/mem
}

enum AgentStatus {
    Pending,                          // approved, awaiting materialization
    Materializing,                    // nix build in progress
    Running { pid: u32, since: Instant },
    Completed { result: AgentResult, duration: Duration },
    Failed { error: String, duration: Duration },
    Killed { reason: String },
} […]

> DEVELOPER

yes

> AGENT

## Section 5: CLI ↔ Daemon Interface & Existing Codebase Integration

**How the existing forge codebase evolves:**

### 5.1 What Stays in the CLI

The `forge` binary keeps all user-facing orchestration logic. It becomes a **client** that delegates execution to the daemon:

```
TODAY                                    AFTER
─────                                    ─────
forge run                               forge run
  └── ClaudeRunner::run_phase()            └── daemon.spawn_agent(profile, phase_prompt)
        └── Command::new("claude")               └── daemon handles isolation + services
              └── tokio::process                        └── agent runs claude inside namespace

forge swarm                              forge swarm
  └── DagExecutor                          └── DagExecutor (unchanged scheduling logic)
        └── ClaudeRunner per phase               └── daemon.spawn_agent() per phase

forge factory                            forge factory
  └── API server + pipeline                └── API server (unchanged)
        └── Command::new("forge swarm")          └── daemon.spawn_run(phases, policy)
```

**What stays in `forge` CLI:**
- All CLI commands (`init`, `interview`, `generate`, `run`, `swarm`, `factory`)
- DAG scheduler (`src/dag/scheduler.rs`) — computes execution order
- Phase definitions and dependency resolution
- Review specialist dispatch (but reviewers themselves become agents)
- Factory API server, WebSocket, database
- Configuration loading (`forge.toml`)
- State persistence for orchestration (phase/iteration tracking)

**What moves to `forge-runtime`:**
- Process spawning (`Command::new("claude")` calls in `runner.rs`)
- Process monitoring (PID tracking, stdout parsing)
- Environment setup (currently ad-hoc env vars)
- The sandbox module (`src/factory/sandbox.rs`) — replaced by namespace […]
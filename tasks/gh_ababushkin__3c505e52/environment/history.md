> DEVELOPER

perform a deep review of this project against https://github.com/github/spec-kit/tree/main

which one is better?

> AGENT

I'll dig into both projects in parallel — explore this repo's structure and content, and research spec-kit.

> TOOL

tool_use ToolSearch
id: toolu_01B72Po3wECt8saRJHg657o6
```json
{
  "query": "select:WebFetch",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_01B72Po3wECt8saRJHg657o6
```
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
```

> TOOL

tool_use Bash
id: toolu_01GRkYWGLoaHZht5275i6BNj
```json
{
  "command": "echo \"=== README ===\" && wc -l README.md && echo \"=== tree ===\" && find . -name '*.md' -not -path './.git/*' | head -100 && echo \"=== skill count ===\" && ls skills/ && echo \"=== docs ===\" && ls docs/ rules/ references/ hooks/ 2>/dev/null",
  "description": "Explore repo structure"
}
```

> TOOL

tool_result
id: toolu_01GRkYWGLoaHZht5275i6BNj
```
=== README ===
163
=== tree ===
./CODE_OF_CONDUCT.md
./CHANGELOG.md
./README.md
./CONTRIBUTING.md
./AGENTS.md
./CLAUDE.md
./references/task-sizing.md
./references/app-context-schema.md
./references/confidence-meter.md
./references/kano-classification.md
./references/nfr-categories.md
./references/project-types.md
./references/design-spike-templates.md
./references/kr-quality-templates.md
./references/ice-scoring.md
./docs/delivery-shape-contract.md
./docs/sub-agent-anatomy.md
./docs/hook-anatomy.md
./docs/benchmarks.md
./docs/ktlo.md
./docs/skill-anatomy.md
./docs/brief-template.md
./docs/authoring-learnings.md
./personas/code-quality.md
./personas/security-auditor.md
./personas/spec-compliance.md
./.github/pull_request_template.md
./rules/PRODUCT_RULES.md
./rules/eng-principles-universal.md
./rules/eng-principles-agentic.md
./eval/delivery-triggers.md
./.private-journal/2026-05-25/17-16-49-003037.md
./.claude/agents/entire-search.md
./.claude/commands/render-html.md
./.claude/commands/verify-implementation.md
./.claude/commands/project.md
./.claude/commands/idea.md
./.claude/commands/stop-the-line.md
./.claude/commands/plan-review.md
./.claude/commands/pr-prepare.md
./.claude/commands/delivery.md
./.claude/commands/design.md
./.claude/commands/ta[REDACTED_SK].md
./.claire/worktrees/agent-a9586af0c5ea06f08/skills/engineering/incremental-implementation/SKILL.md
./agents/code-reviewer/AGENT.md
./agents/writing-editor/AGENT.md
./docs/adr/0002-delivery-shape-accepts-ideas-goal-optional.md
./docs/adr/0003-persona-contract-and-dispatch-protocol.md
./docs/adr/0004-execution-verb-namespace.md
./docs/adr/0005-shaping-door-leaf-names.md
./docs/adr/0001-delivery-shape-new-skill-vs-expand-planning-and-task-breakdown.md
./hooks/stop-the-line/HOOK.md
./hooks/ta[REDACTED_SK]/HOOK.md
./.github/ISSUE_TEMPLATE/bug-report.md
./.github/ISSUE_TEMPLATE/skill-proposal.md
./hooks/ta[REDACTED_SK]/fixtures/fail.md
./hooks/ta[REDACTED_SK]/fixtures/pass.md
./.claude/worktrees/agent-a46329fb876c35835/PROJECT_GOVERNANCE.md
./.claude/worktrees/agent-a46329fb876c35835/PROJECT_PLAN.md
./.claude/worktrees/agent-a46329fb876c35835/CHANGELOG.md
./.claude/worktrees/agent-a46329fb876c35835/roadmap_principles.md
./.claude/worktrees/agent-a46329fb876c35835/POST_V0.1_BACKLOG.md
./.claude/worktrees/agent-a46329fb876c35835/README.md
./.claude/worktrees/agent-a46329fb876c35835/PROJECT_STATE.md
./.claude/worktrees/agent-a46329fb876c35835/CONTRIBUTING.md
./.claude/worktrees/agent-a46329fb876c35835/LEARNINGS.md
./.claude/worktrees/agent-a9586af0c5ea06f08/PROJECT_GOVERNANCE.md
./.claude/worktrees/agent-a9586af0c5ea06f08/PROJECT_PLAN.md
./.claude/worktrees/agent-a9586af0c5ea06f08/CHANGELOG.md
./.claude/worktrees/agent-a9586af0c5ea06f08/roadmap_principles.md
./.claude/worktrees/agent-a9586af0c5ea06f08/POST_V0.1_BACKLOG.md
./.claude/worktrees/agent-a9586af0c5ea06f08/README.md
./.claude/worktrees/agent-a9586af0c5ea06f08/PROJECT_STATE.md
./.claude/worktrees/agent-a9586af0c5ea06f08/CONTRIBUTING.md
./.claude/worktrees/agent-a9586af0c5ea06f08/LEARNINGS.md
./.claude/worktrees/agent-a211fb78979063b14/PROJECT_GOVERNANCE.md
./.claude/worktrees/agent-a211fb78979063b14/PROJECT_PLAN.md
./.claude/worktrees/agent-a211fb78979063b14/CHANGELOG.md
./.claude/worktrees/agent-a211fb78979063b14/roadmap_principles.md
./.claude/worktrees/agent-a211fb78979063b14/POST_V0.1_BACKLOG.md
./.claude/worktrees/agent-a211fb78979063b14/README.md
./.claude/worktrees/agent-a211fb78979063b14/PROJECT_STATE.md
./.claude/worktrees/agent-a211fb78979063b14/CONTRIBUTING.md
./.claude/worktrees/agent-a211fb78979063b14/LEARNINGS.md
./.claude/worktrees/agent-a6901afbfb8e91d15/PROJECT_GOVERNANCE.md
./.claude/worktrees/agent-a6901afbfb8e91d15/PROJECT_PLAN.md
./.claude/worktrees/agent-a6901afbfb8e91d15/CHANGELOG.md
./.claude/worktrees/agent-a6901afbfb8e91d15/roadmap_principles.md
./.claude/worktrees/agent-a6901afbfb8e91d15/POST_V0.1_BACKLOG.md
./.claude/worktrees/agent-a6901afbfb8e91d15/README.md
./.claude/worktrees/agent-a6901afbfb8e91d15/PROJECT_STATE.md
./.claude/worktrees/agent-a6901afbfb8e91d15/CONTRIBUTING.md
./.claude/worktrees/agent-a6901afbfb8e91d15/LEARNINGS.md
./.claude/worktrees/agent-af74d16eb5d33af74/PROJECT_GOVERNANCE.md
./.claude/worktrees/agent-af74d16eb5d33af74/PROJECT_PLAN.md
./.claude/worktrees/agent-af74d16eb5d33af74/CHANGELOG.md
./.claude/worktrees/agent-af74d16eb5d33af74/roadmap_principles.md
./.claude/worktrees/agent-af74d16eb5d33af74/POST_V0.1_BACKLOG.md
./.claude/worktrees/agent-af74d16eb5d33af74/README.md
./.claude/worktrees/agent-af74d16eb5d33af74/PROJECT_STATE.md
=== skill count ===
debugging/
delivery/
design/
exec-pickup/
execution-review/
idea/
plan-review/
pr-finishing/
pr-prepare/
project/
render-html/
simplify/
using-this-pack/
verify-implementation/
writing-refinement/
=== docs ===
adr/
idea-bank/
tasks/
stop-the-line/
ta[REDACTED_SK]/
authoring-learnings.md  2.7K
benchmarks.md  11.0K
brief-template.md  2.5K
delivery-shape-contract.md  22.7K
hook-anatomy.md  2.3K
ktlo.md  161B
skill-anatomy.md  2.6K
sub-agent-anatomy.md  5.0K
.gitkeep  0B
hooks.json  224B
session-start.sh  578B
.gitkeep  0B
app-context-schema.md  3.5K
confidence-meter.md  3.3K
design-spike-templates.md  3.4K
ice-scoring.md  3.6K
kano-classification.md  3.4K
kr-quality-templates.md  16.7K
nfr-categories.md  6.0K
project-types.md  44.0K
task-sizing.md  11.7K
PRODUCT_RULES.md  19.0K
eng-principles-agentic.md  12.3K
eng-principles-universal.md  25.5K
```

> AGENT

Let me read this project's README and research spec-kit in parallel.

> TOOL

tool_use Read
id: toolu_01BJ6Hh1w9RmtAgZ9mTwz82o
```json
{
  "file_path": "/Users/anton/src/agent-skills-shaper/README.md"
}
```

> TOOL

tool_result
id: toolu_01BJ6Hh1w9RmtAgZ9mTwz82o
```
1	# Shaper
2	
3	**Robust, scalable skills for modern agentic engineering**
4	
5	Vibe coding is fun on a small project. Over a longer one, your prompts drift and the quality of the output drifts with them. Shaper encodes the engineering discipline that strong teams have relied on for decades into ready-to-go skills, so an agent applies it the same way on every project, every turn — instead of taking the shortcut.
6	
7	Core disciplines it encodes:
8	
9	- Problem before solution
10	- Acceptance criteria before code
11	- Small, independently verified slices
12	- The smallest thing that works
13	- Root-cause diagnosis before any fix
14	- Independent verification by a second agent
15	
16	
17	```
18	  SHAPE              DESIGN            PLAN              BUILD             VERIFY            SHIP
19	 ┌────────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
20	 │ triage     │ ───▶ │ design   │ ───▶ │ delivery │ ───▶ │ build    │ ───▶ │ verify   │ ───▶ │ prepare  │
21	 │ roadmap    │      │ doc +    │      │ shape +  │      │ debug    │      │ exec     │      │ + finish │
22	 │ initiative │      │ spikes   │      │ review   │      │ simplify │ […]

> TOOL

tool_use WebFetch
id: toolu_011FQEPY7JP7MupqzZChBmZt
```json
{
  "url": "https://github.com/github/spec-kit/tree/main",
  "prompt": "Summarize what spec-kit is, its purpose, the workflow it implements (commands/phases), its directory structure, what artefacts it produces, and the methodology (spec-driven development). List the slash commands or scripts it provides and what each does."
}
```

> TOOL

tool_result
id: toolu_011FQEPY7JP7MupqzZChBmZt
```
# Spec-Kit Summary

## What It Is
Spec-Kit is an open-source toolkit that implements Spec-Driven Development (SDD), a methodology where specifications become executable artifacts that generate working code implementations rather than serving merely as documentation.

## Core Purpose
The toolkit enables developers to "focus on product scenarios and predictable outcomes instead of vibe coding every piece from scratch." It bridges the gap between requirements and implementation through structured, AI-assisted development workflows.

## Methodology: Spec-Driven Development
SDD inverts traditional development by making specifications primary. Developers define *what* and *why* before addressing *how*, then use AI coding agents to generate implementations from these executable specifications through systematic phases.

## Primary Workflow Phases

**Seven-step implementation cycle:**

1. **Constitution** – Establish project principles and development guidelines
2. **Specification** – Define functional requirements and user stories
3. **Clarification** – Resolve underspecified requirements before technical planning
4. **Planning** – Create technical implementation strategy with chosen tech stack
5. **Task Breakdown** – Generate ordered, dependency-aware task lists
6. **Implementation** – Execute tasks systematically using AI agents
7. **Convergence** – Assess codebase against artifacts and identify remaining work

## Core Slash Commands

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Create governing principles […]

> AGENT

Let me ground the comparison by reading a representative Shaper skill and spec-kit's actual templates.

> TOOL

tool_use Bash
id: toolu_016xu2sHUGL8YUwmExybTfgB
```json
{
  "command": "echo \"=== delivery SKILL ===\" && wc -l skills/delivery/SKILL.md && sed -n '1,60p' skills/delivery/SKILL.md && echo \"=== idea SKILL head ===\" && sed -n '1,40p' skills/idea/SKILL.md",
  "description": "Read representative skills"
}
```

> TOOL

tool_result
id: toolu_016xu2sHUGL8YUwmExybTfgB
```
=== delivery SKILL ===
283
---
name: delivery
description: 'Decompose committed work into a verifiable delivery hierarchy: deliverables → nodes → tasks. Use when committed work exists and needs a delivery plan before build pickup. Trigger phrases: "turn this initiative into a delivery plan", "decompose this initiative", "break the initiative into deliverables", "shape the delivery", "delivery plan", "plan the nodes and tasks", "break down committed work", "build delivery plan", "what are the deliverables for this initiative".'
---

# Delivery shape

## Purpose

Take committed work and create a delivery plan that's easy for humans to review and for agents to action.

The input may be an initiative, a single task, or an accepted design doc. The hierarchy has three layers: deliverables, nodes, and tasks. Deliverables serve a stated outcome source. Nodes are typed units of work such as stories, spikes, ADRs, experiments, design docs, or KTLO work. Tasks are the verifiable checklist inside a node.

## When to use

- Committed work exists and the desired outcome is known.
- You need a deliverable → node → task hierarchy before build pickup.
- You want traceability from each deliverable back to the relevant outcome source.
- […]

> TOOL

tool_use WebFetch
id: toolu_01TRZKeTsTiMg9qwebL5V5ji
```json
{
  "url": "https://raw.githubusercontent.com/github/spec-kit/main/spec-driven.md",
  "prompt": "What is the core philosophy and methodology described here? What problems does spec-driven development claim to solve, and what are its key principles? Summarize concisely."
}
```

> TOOL

tool_result
id: toolu_01TRZKeTsTiMg9qwebL5V5ji
```
# Specification-Driven Development: Core Philosophy and Summary

## Core Philosophy

SDD fundamentally inverts traditional software development by making specifications—not code—the primary artifact. As the document states, "Specifications don't serve code—code serves specifications." This represents a paradigm shift where natural language requirements become the executable source of truth, with code as the generated output.

## Problems It Addresses

1. **The Specification-Implementation Gap**: Traditional development accepts an inevitable disconnect between what's specified and what's implemented. SDD eliminates this by generating code directly from specifications.

2. **Change Management Friction**: Pivoting requires manually propagating changes across documentation, design, and code. SDD automates regeneration when specifications evolve.

3. **Technical Debt Accumulation**: "Each pivot requires manually propagating changes through documentation, design, and code." SDD transforms pivots into systematic regenerations.

4. **Maintenance Complexity**: As systems grow exponentially more complex, keeping all pieces aligned with original intent becomes increasingly difficult through manual processes.

## Key Principles

- **Specifications as Lingua Franca**: The specification becomes primary; code expresses it in specific languages/frameworks
- **Executable Specifications**: Specifications must be precise, complete, and unambiguous enough to generate working systems
- **Continuous Refinement**: Consistency validation happens continuously, not as a one-time gate
- **Research-Driven Context**: Agents investigate technical […]

> AGENT

I've reviewed both in depth. Here's the comparison, grounded in what each actually ships.

## What each one is

**spec-kit** (GitHub, official) — a packaged, agent-agnostic toolkit for **Spec-Driven Development**. A real CLI (`specify`, installed via `uv`), versioned releases, support for 30+ coding agents, and a tight 7-step pipeline centered on one idea: the *spec* is the executable source of truth, code is generated output. Its arc: `constitution → specify → clarify → plan → tasks → implement → analyze → converge`. It scaffolds `.specify/` (templates, bash scripts, constitution) and produces `specs/<feature>/{spec,plan,tasks,data-model,research,contracts}`.

**Shaper** (this repo, personal project) — a Markdown-only skill pack encoding **engineering discipline as enforced gates**, biased toward Claude Code. Much wider arc: `idea triage → project → design/spikes → delivery → build/debug/simplify → verify/review → pr-prepare/finishing`. It ships skills, a SessionStart navigator hook, mechanical hooks (stop-the-line, ta[REDACTED_SK]), persistent rule files (PRODUCT_RULES, eng-principles), and is structured so an orchestrator (drain-cycle) can drive a delivery plan unattended.

## Where they actually differ

| Dimension | spec-kit | Shaper |
|---|---|---|
| **Lifecycle covered** | "We've decided to build feature X" → working code | "Is this worth building?" → shipped, reviewed PRs |
| **Front of funnel** | None […]
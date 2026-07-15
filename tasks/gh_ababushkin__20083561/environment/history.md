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

> DEVELOPER

are there any ideas from spec-kit that shaper should adopt?

consider your answer carefully

> AGENT

Good question — let me check what Shaper already has before claiming any gaps, so I don't recommend things it already does.

> TOOL

tool_use Bash
id: toolu_01Sr5Ti1BBZv4bBp3isFzoMk
```json
{
  "command": "cd /Users/anton/src/agent-skills-shaper\necho \"=== parallel / [P] markers in delivery ===\"; grep -rinE \"parallel|\\[P\\]|can run concurrently|independent\" docs/delivery-shape-contract.md skills/delivery/SKILL.md | head -20\necho \"=== constitution / project principles ===\"; grep -rinl \"constitution\" . --include=*.md | grep -v worktree | head\necho \"=== clarify / ambiguity resolution ===\"; grep -rinE \"clarif|ambigu|underspecif|open question\" skills/*/SKILL.md | head -20\necho \"=== converge / initiative-level closeout ===\"; grep -rinE \"converge|initiative.*complete|closeout|close the loop|delivered against\" skills/*/SKILL.md | head\necho \"=== cross-artifact consistency ===\"; grep -rinE \"consisten|cross-artifact|drift between|traceab\" skills/plan-review/SKILL.md skills/verify-implementation/SKILL.md | head",
  "description": "Check for existing equivalents"
}
```

> TOOL

tool_result
id: toolu_01Sr5Ti1BBZv4bBp3isFzoMk
```
=== parallel / [P] markers in delivery ===
docs/delivery-shape-contract.md:75:  order-independent). If inter-node dependencies ever need machine enforcement, that is the trigger
skills/delivery/SKILL.md:208:For runnable-software story nodes, add one task per feature slice after the first task. Each slice must extend prior work in one direction, be independently testable, leave the system deployable, and name an observable outcome. Do not add slices to `adr`, `design-doc`, or `ktlo` nodes.
skills/delivery/SKILL.md:261:- A task has multiple independent completion criteria.
=== constitution / project principles ===
(eval):3: no matches found: --include=*.md
=== clarify / ambiguity resolution ===
skills/build/SKILL.md:49:If no test runner exists, select a deterministic fallback, in priority order: a grader script named in the plan (`Done when: bin/grader exits 0`), a lint/format check, a link or reference checker, or a shell assertion (`grep -q 'expected' file && echo PASS || echo FAIL`). The fallback must be deterministic (same input → same exit code) and chosen *before* the first slice. A "verification" that can't be expressed as a command with a zero/non-zero exit convention is a vibe — stop and clarify.
skills/design/SKILL.md:34:- The answer is well-established and unambiguous — document it in the design-doc or ADR and proceed.
skills/design/SKILL.md:58:Name the dominant unknown […]

> AGENT

Yes — a few, and they're worth taking for a specific reason: Shaper's artifact chain is *longer* than spec-kit's (idea → project → design → delivery → AC → diff), so it has more places to drift and more loop to close. The best spec-kit ideas are exactly the ones that exploit that. I grounded each against what Shaper already has.

## Worth adopting

**1. `analyze` — a cross-artifact consistency check. (Strongest fit.)**
Shaper reviews each artifact well but never checks the *chain's mutual coherence*. `plan-review` is adversarial but single-artifact; `verify-implementation` checks diff-vs-AC only. Nothing asks: do the delivery plan's acceptance criteria still trace to the project's KRs, which trace to the idea's stated outcome and the design's decisions? spec-kit can afford to skip this because it has three artifacts; Shaper has six, so the drift surface is larger and currently unguarded. This is the cleanest gap, and it leans directly on Shaper's existing "traceability spine" — `analyze` would just verify that spine end-to-end instead of assuming it holds.

**2. `converge` — an initiative-level outcome closeout. (Strong, genuine hole.)**
My grep found nothing matching this. Shaper verifies per-ticket but has no step that closes the loop at the initiative level: […]

> DEVELOPER

compare shaper against this PDF ~/Downloads/Day_1_v3.pdf

perform a gap analysis

> AGENT

I'll read the PDF first to understand what it covers.

> TOOL

tool_use Bash
id: toolu_01CtnjxGW9YUMKUBL5y7USLu
```json
{
  "command": "cd ~/Downloads && ls -la Day_1_v3.pdf && pdfinfo Day_1_v3.pdf 2>/dev/null | grep -iE \"pages|title\" || echo \"pdfinfo unavailable\"",
  "description": "Check PDF size and page count"
}
```

> TOOL

tool_result
id: toolu_01CtnjxGW9YUMKUBL5y7USLu
```
644  Day_1_v3.pdf  9.5M
Pages:           51
Shell cwd was reset to /Users/anton/src/agent-skills-shaper
```

> AGENT

51 pages — I'll read it in chunks.

> TOOL

tool_use Read
id: toolu_01J5s4yNJL5No83iga8TDTXk
```json
{
  "file_path": "/Users/anton/Downloads/Day_1_v3.pdf",
  "pages": "1-18"
}
```

> TOOL

tool_result
id: toolu_01J5s4yNJL5No83iga8TDTXk
```
PDF pages extracted: 18 page(s) from /Users/anton/Downloads/Day_1_v3.pdf (9.5MB)
```

> AGENT

This is Addy Osmani et al.'s "The New SDLC With Vibe Coding" (Google, May 2026). Let me read the core SDLC, harness, and orchestration sections.

> TOOL

tool_use Read
id: toolu_01XJEsUEHeLALbR588KNkfk5
```json
{
  "file_path": "/Users/anton/Downloads/Day_1_v3.pdf",
  "pages": "19-38"
}
```

> TOOL

tool_result
id: toolu_01XJEsUEHeLALbR588KNkfk5
```
PDF pages extracted: 20 page(s) from /Users/anton/Downloads/Day_1_v3.pdf (9.5MB)
```

> AGENT

Now the final section — economics and "where to start" recommendations, which is where the gap analysis will land hardest.

> TOOL

tool_use Read
id: toolu_0138yqGoy655xRKDEGMARsZY
```json
{
  "file_path": "/Users/anton/Downloads/Day_1_v3.pdf",
  "pages": "39-48"
}
```

> TOOL

tool_result
id: toolu_0138yqGoy655xRKDEGMARsZY
```
PDF pages extracted: 10 page(s) from /Users/anton/Downloads/Day_1_v3.pdf (9.5MB)
```

> AGENT

This is the Addy Osmani / Google "New SDLC with Vibe Coding" paper (Day 1 of a series) — a strategy/manifesto, not a tool. So this is a different kind of comparison from spec-kit: the paper defines the *ideal* of "agentic engineering," and Shaper is essentially a concrete *implementation* of that ideal. Let me ground a few gap claims before writing.

> TOOL

tool_use Bash
id: toolu_01AFPkShrEyoe9Smu3pfWyXh
```json
{
  "command": "cd /Users/anton/src/agent-skills-shaper\necho \"=== evals / LM judge / rubric ===\"; grep -rinE \"\\beval(s|uation)?\\b|LM judge|rubric|benchmark\" skills/build/SKILL.md skills/verify-implementation/SKILL.md skills/execution-review/SKILL.md | head\necho \"=== trajectory ===\"; grep -rinE \"trajectory|tool call|reasoning path|how it got there\" skills/*/SKILL.md | head\necho \"=== observability / cost / token / drift ===\"; grep -rinE \"observab|token cost|latency|drift|trace|telemetry|cost\" skills/*/SKILL.md rules/*.md | head\necho \"=== model routing ===\"; grep -rinE \"Model:|model.tier|route|cheaper model|haiku|sonnet|opus\" hooks/ta[REDACTED_SK]/HOOK.md references/task-sizing.md | head\necho \"=== security persona: generated-code failure modes ===\"; grep -rinE \"hallucinat|generated code|made-up|fabricat|phantom dep\" personas/security-auditor.md | head\necho \"=== memory as artefact ===\"; grep -rinl \"memory\" skills/*/SKILL.md docs/*.md | head",
  "description": "Ground eval/observability/routing claims"
}
```

> TOOL

tool_result
id: toolu_01AFPkShrEyoe9Smu3pfWyXh
```
=== evals / LM judge / rubric ===
=== trajectory ===
=== observability / cost / token / drift ===
skills/build/SKILL.md:20:- Implementing a story, feature slice, bug fix, or any change with an observable acceptance criterion.
skills/build/SKILL.md:70:Commit the slice before starting the next. The message names the slice outcome, not the implementation detail: `feat: add <observable outcome>`, not `feat: implement helper`. Conventional-commit prefix, subject ≤ 70 chars, no co-author trailers. Each commit must leave the command green — a commit that breaks the check is a fragment, not a slice.
skills/build/SKILL.md:128:3. Each commit passes the command and its message names an observable outcome.
skills/debugging/SKILL.md:32:- Evidence of failure: stack traces, error messages, system state at failure time.
skills/debugging/SKILL.md:45:Record the failing check command exactly and run it. Collect the full error output and stack trace, the system state at failure (env vars, file state, recent changes, `git log`), and every previous fix attempt with the output it produced.
skills/debugging/SKILL.md:55:- **Trace data flow backward.** When the error is deep in a call stack, find where the bad value originates and fix at the source, not the symptom.
skills/debugging/SKILL.md:81:What is broken: <observable symptom and its impact>
skills/debugging/SKILL.md:84:Evidence: <diagnostics, stack traces, […]

> AGENT

Read the full paper and grounded the gaps against Shaper's actual files. Here's the analysis.

## What this comparison actually is

The spec-kit comparison was tool-vs-tool. This is different: **the paper is the manifesto, and Shaper is a concrete implementation of its "agentic engineering" end of the spectrum.** They're not competitors — the paper describes the ideal, Shaper is one instantiation of it. Shaper's own README even opens with the same "vibe coding drifts, encode the discipline" framing the paper is built on.

So the gap analysis asks one question: **where does the paper name a practice that Shaper doesn't yet embody?**

## Strong alignment (Shaper already satisfies these)

The paper's closing recommendations read almost like a Shaper feature list:

| Paper recommendation | Shaper |
|---|---|
| "Set up AGENTS.md, treat it as code, versioned, owned" | `AGENTS.md` + `CLAUDE.md` + versioned `rules/` ✓ |
| "Install a set of skills (progressive disclosure)" | Shaper *is* a lazy-loaded skill pack ✓ |
| "Write tests before generating code" | `build` = RED before GREEN; AC before code ✓ |
| "Review every line; re-shape review for AI code" | `execution-review` (spec/security/quality personas), `stop-the-line` ✓ |
| "Static vs dynamic […]

> DEVELOPER

yes

> AGENT

I'll run the intake gate on the eval-layer skill idea.

> TOOL

tool_use Skill
id: toolu_01SKWLqF4N5yUhh6mTfn9CHJ
```json
{
  "skill": "shape:idea",
  "args": "A new Verify-stage skill for Shaper that adds an eval layer: rubric-scored output evaluation plus trajectory verification (did the agent run its gates, in order, without skipping). Motivation: gap analysis against the Google/Addy Osmani \"New SDLC with Vibe Coding\" paper found Shaper rigorously verifies deterministic correctness (tests via build) and applies human judgment (execution-review personas, verify-implementation AC check), but has no eval layer (no rubric-scored, LM-judge, non-deterministic output evaluation) and no trajectory check — the two mechanisms the paper names as what separates agentic engineering from sophisticated vibe coding. Would slot into the Verify stage alongside verify-implementation and execution-review."
}
```

> TOOL

tool_result
id: toolu_01SKWLqF4N5yUhh6mTfn9CHJ
```
Launching skill: shape:idea
```

> TOOL

tool_use Read
id: toolu_01PvqzzaALWcphfuXAXBVzRG
```json
{
  "file_path": "/Users/anton/src/agent-skills-shaper/references/idea-elicitation.md"
}
```

> TOOL

tool_result
id: toolu_01PvqzzaALWcphfuXAXBVzRG
```
1	---
2	name: idea-elicitation
3	description: >
4	  Interview-style elicitation loop for sharpening a raw idea before it is scored or routed.
5	  Ported from agent-skills:interview-me, voice-matched to this pack.
6	type: reference
7	cited_by:
8	  - skills/idea/SKILL.md
9	---
10	
11	# Idea elicitation loop
12	
13	A raw idea is almost always under-articulated. The person asks for "a dashboard" because that is what one asks for, not because a dashboard solves their problem. They say "we should build X" without naming who hurts when we don't. The cheapest moment to close that gap is at intake, before any evidence is taken or any score is assigned. Once a score exists, the conversation anchors on the number; once a build is in flight, switching costs are real.
14	
15	This loop sharpens the idea by asking one question at a time, each carrying the skill's own best guess, until the person can confirm a six-line restate in their own words.
16	
17	## When to run the loop
18	
19	Run on every fresh idea unless the ask is unambiguous and self-contained (a renamed metric, a typo, a mechanical fix). If the request is […]

> AGENT

Running `shape:idea`. **Step 1 — Raw intake captured verbatim:**

> A new Verify-stage skill for Shaper that adds an eval layer: rubric-scored output evaluation plus trajectory verification (did the agent run its gates, in order, without skipping). Gap found vs the Google/Osmani "New SDLC with Vibe Coding" paper — Shaper verifies deterministic correctness (build/tests) and applies human judgment (execution-review, verify-implementation) but has no eval layer and no trajectory check, the two things the paper names as separating agentic engineering from sophisticated vibe coding.

**Step 2 — Elicit and refine.** Let me sharpen this before it gets scored or routed.

```
HYPOTHESIS: You want Shaper to verify the non-deterministic parts of agentic work —
both the *quality* of an artefact against a rubric, and the *process* the agent took
to produce it — so "the gates passed" stops being something an agent can fake.
CONFIDENCE: ~45% — unresolved: this is really TWO capabilities (rubric eval vs
trajectory check) that may not belong in one skill; and it's unclear how either works
in a Markdown-only, stack-agnostic pack with no runtime/transcript access.
```

I'll ask one at a time, each with my guess attached.

**Q1: Is this one skill or two?** Rubric-scored output […]
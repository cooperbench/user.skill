> SYSTEM

<system_instruction>
You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel.
Your work should take place in the /home/<USER>/conductor/workspaces/brain-v1/munich-v2 directory (unless otherwise directed), which has been set up for you to work in.
Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents.
The target branch for this workspace is main. Use this for actions like creating new PRs, bisecting, etc., unless you're told otherwise.

By default, the user will only see the last message that you send before stopping. Include all essential information in the last message. The intermediate messages will be collapsed and accessible by the user but not displayed by default.

If the user asks you to work on several unrelated tasks, you can suggest they start new workspaces.
Sometimes the user might send you a message they meant to send in a different workspace or a different chat. If something doesn't make sense in the context of your work, just ask. 
If the user asks for help with Conductor, you can ask them to go to "Help -> Send Feedback" to get in touch with our team.
</system_instruction>

now that we […]

> AGENT

Based on exploring the codebase, here's how it currently works:

## Current State: Task → Agent Assignment

The UI already has an **`AgentStatusSection`** component (`app/src/client/components/graph/AgentStatusSection.tsx`) that appears on task detail views. When a task is in `open`, `ready`, or `todo` status, it shows an **"Assign Agent"** button.

However, the current flow is:

1. User clicks "Assign Agent" on a task
2. It calls `POST /api/orchestrator/:workspaceId/assign` 
3. The orchestrator spawns an **agent session** and streams progress back via SSE
4. The UI shows live status (Spawning → Working → Idle → Completed), file changes, and a review link

## What's Missing

**There's no agent picker.** The assignment call doesn't let the user choose *which* agent to assign — it just dispatches to the orchestrator without an agent selection step. The user can't browse their created agents (Brain, External, Sandbox) and say "assign this task to Agent X."

This is the gap between:
- **Agent CRUD** (fully built — create, list, detail, delete, authority scopes) at `/agents`
- **Task assignment** (exists but has no agent selection UI)

## What Would Need to Change

To let users choose which agent handles a task:

1. **Agent picker UI** — When clicking "Assign Agent" on […]

> TOOL

<command-message>nw-design</command-message>
<command-name>/nw-design</command-name>

> SYSTEM

Base directory for this skill: /home/<USER>/.claude/skills/nw-design

# NW-DESIGN: Architecture Design

**Wave**: DESIGN (wave 3 of 6) | **Agents**: Morgan (nw-solution-architect) | **Command**: `*design-architecture`

## Overview

Execute DESIGN wave through discovery-driven architecture design. Morgan asks about business drivers and constraints first, then recommends architecture that fits. Analyzes existing codebase, evaluates open-source alternatives, produces C4 diagrams (Mermaid) as mandatory output.

## Prior Wave Consultation

Before beginning DESIGN work, read targeted prior wave artifacts:

1. **DISCOVER** (synthesis check only): Read `docs/feature/{feature-id}/discover/wave-decisions.md` — if any decision is unclear or relevant to architecture, read the referenced source file
2. **DISCUSS** (primary input): Read these key artifacts from `docs/feature/{feature-id}/discuss/`:
   - `wave-decisions.md` — decision summary
   - `requirements.md` — functional requirements
   - `acceptance-criteria.md` — testable criteria driving architecture
   - `user-stories.md` — scope of what to build
   - `story-map.md` — walking skeleton and release slicing
   - `outcome-kpis.md` — quality attributes informing architecture

DISCUSS already synthesizes DISCOVER evidence into structured requirements. DESIGN does not need raw DISCOVER artifacts (problem-validation, interview-log, etc.) unless wave-decisions.md flags something architecturally significant.

**READING ENFORCEMENT**: You MUST read every file listed in Prior Wave Consultation above using the Read tool before proceeding. After reading, output a confirmation checklist (`✓ {file}` for each read, `⊘ {file} (not […]

> AGENT

Good. Now I have a complete picture of the current state. Let me launch the solution architect agent to design the agent task assignment feature.

> TOOL

<command-message>nw-discover</command-message>
<command-name>/nw-discover</command-name>

> SYSTEM

Base directory for this skill: /home/<USER>/.claude/skills/nw-discover

# NW-DISCOVER: Evidence-Based Product Discovery

**Wave**: DISCOVER | **Agent**: Scout (nw-product-discoverer)

## Overview

Execute evidence-based product discovery through assumption testing and market validation. First wave in nWave (DISCOVER > DISCUSS > DESIGN > DEVOPS > DISTILL > DELIVER).

Scout establishes product-market fit through rigorous customer development using Mom Test interviewing principles and continuous discovery practices.

## Context Files Required

- docs/project-brief.md — Initial product vision (if available)
- docs/market-context.md — Market research and competitive landscape (if available)

## Previous Artifacts

None (DISCOVER is the first wave).

## Wave Decisions Summary

Before completing DISCOVER, produce `docs/feature/{feature-id}/discover/wave-decisions.md`:

```markdown
# DISCOVER Decisions — {feature-id}

## Key Decisions
- [D1] {decision}: {rationale} (see: {source-file})

## Constraints Established
- {constraint from evidence}

## Validated Assumptions
- {assumption validated by evidence, with confidence level}

## Invalidated Assumptions
- {assumption disproved, with evidence reference}
```

This summary enables downstream waves to quickly assess DISCOVER outcomes without reading all artifacts.

## Document Update (Back-Propagation)

Not applicable (DISCOVER is the first wave — no prior documents to update).

## Agent Invocation

@nw-product-discoverer

Execute \*discover for {product-concept-name}.

**Context Files:** docs/project-brief.md (if available) | docs/market-context.md (if available)

**Configuration:**
- interactive: high | output_format: markdown
- […]

> AGENT

Here's the current state:

## Current Agent Assignment: No Selection

The UI currently has a simple **"Assign Agent" button** on tasks (`AgentStatusSection.tsx:274`) with **no agent picker**. When clicked, it calls `assignAgent(workspaceId, taskId)` which hits `POST /api/orchestrator/:workspaceId/assign` with just `{ taskId }`. The backend hard-codes `agent: "claude"` in `session-lifecycle.ts:446`.

Meanwhile, the **agent CRUD is fully built**:
- **Agent registry page** (`/agents`) — lists agents grouped by runtime (brain/external/sandbox)
- **Agent creation page** (`/agents/new`) — name, runtime, description, model, authority scopes
- **Agent detail page** — shows scopes, sessions, delete

But **no bridge exists** between the agent registry and task assignment. The pieces that are missing:

1. **API**: Add `agentId` to the assign request body
2. **Assignment guard**: Validate the agent belongs to the workspace and has appropriate authority
3. **Session lifecycle**: Pass the agent record instead of hard-coded `"claude"` string
4. **UI**: Add an agent selector/picker before the "Assign" button
5. **Data model**: Migrate `agent_session.agent` from `string` to `record<agent>` (noted as deferred R2 in the evolution doc)

---

**Do you want me to design this bridging feature?** It's a focused integration — connecting the existing agent registry to the existing orchestrator assign flow, plus an agent picker in the UI. I […]
> SYSTEM

<system_instruction>
You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel.
Your work should take place in the /Users/marcus/conductor/workspaces/brain-v1/los-angeles directory (unless otherwise directed), which has been set up for you to work in.
Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents.
The target branch for this workspace is main. Use this for actions like creating new PRs, bisecting, etc., unless you're told otherwise.

By default, the user will only see the last message that you send before stopping. Include all essential information in the last message. The intermediate messages will be collapsed and accessible by the user but not displayed by default.

If the user asks you to work on several unrelated tasks, you can suggest they start new workspaces.
Sometimes the user might send you a message they meant to send in a different workspace or a different chat. If something doesn't make sense in the context of your work, just ask. 
If the user asks for help with Conductor, you can ask them to go to "Help -> Send Feedback" to get in touch with our team.
</system_instruction>

/nw-discover gh issue […]

> TOOL

tool_use Skill
id: toolu_01RC7mt2V7nGzwjznmQDBUDJ
```json
{
  "skill": "nw-discover",
  "args": "gh issue Skills: graph-native behavioral expertise layer #177 - also want agent creation updated into a step wizard: step 1 = agent config, step 2 = setting up skills, step 3 = setting up tools"
}
```

> TOOL

tool_result
id: toolu_01RC7mt2V7nGzwjznmQDBUDJ
```
Launching skill: nw-discover
```

> AGENT

Let me gather context on the GitHub issue and the existing agent creation flow before starting discovery.

> TOOL

tool_use Bash
id: toolu_01AoJW5k7Yzcbrgy3SpBcDRW
```json
{
  "command": "gh issue view 177",
  "description": "Fetch GitHub issue #177"
}
```

> TOOL

tool_result
id: toolu_01AoJW5k7Yzcbrgy3SpBcDRW
```
[open] Issue #177: Skills: graph-native behavioral expertise layer
  Author: @marcus-sa
  Status: OPEN
  URL: https://github.com/osabiohq/osabio/issues/177

  Description:
    ## Summary
    
    Add Skills as the missing middle layer between Tools (functional capabilities) and Learnings (reactive corrections). A skill is a governed, versionable, discoverable instruction document that Brain tracks as source references and passes to sandbox agent sessions via `setSkillsConfig`.
    
    **Research**: `docs/research/brain-native-agent-runtime.md` §6, `docs/research/skills-sandbox-agent-integration.md`
    
    ## Motivation
    
    Brain currently has two of three agent competency layers:
    - **Tools** (MCP endpoints) — give agents functional capabilities
    - **Learnings** (correction rules) — tell agents what to avoid based on past failures
    
    Missing: **Skills** — proactive domain expertise ("how to do a security audit", "how to triage issues"). Without skills, Brain can only inject corrections and context, not expertise.
    
    ## Activation Model
    
    **The sandbox agent's LLM decides skill activation, not Brain.** Per the [Agent Skills spec](https://agentskills.io/client-implementation/adding-skills-support) and Claude Code's implementation, skill activation works via three-tier progressive disclosure:
    
    1. **Catalog** (~100 tokens/skill): `name` + `description` loaded at session start for all assigned skills
    2. **Instructions** (<5000 tokens): full SKILL.md body loaded when LLM decides a skill is relevant
    3. **Resources** (on demand): scripts, references loaded when instructions reference them
    
    The LLM reads the catalog and decides […]

> TOOL

tool_use Agent
id: toolu_01NNLr6xMiJF44r5aF374wpP
```json
{
  "description": "Explore agent creation UI/API",
  "subagent_type": "Explore",
  "prompt": "Explore the codebase at /Users/marcus/conductor/workspaces/brain-v1/los-angeles to understand:\n\n1. The current agent creation flow - both frontend UI and backend API\n2. How agents are defined/configured in the system (schema, types, routes)\n3. Any existing \"skills\" or \"tools\" concepts attached to agents\n4. The agent CRUD endpoints and UI components\n\nLook in:\n- app/src/client/ for agent-related UI components\n- app/src/server/ for agent routes and types\n- schema/ for agent-related schema definitions\n- Any agent-related test files\n\nThoroughness: very thorough\n\nReturn a detailed summary of the current agent creation architecture, including file paths and key types."
}
```

> TOOL

tool_result
id: toolu_01NNLr6xMiJF44r5aF374wpP
```
Perfect! I now have a comprehensive understanding of the agent creation architecture. Let me create a detailed summary report.

## Detailed Summary: Agent Creation Architecture

I've conducted a thorough exploration of the agent creation system in Osabio. Here's the complete architecture:

### 1. **Core Agent Model & Types**

**File**: `/Users/marcus/conductor/workspaces/brain-v1/los-angeles/app/src/server/agents/types.ts`

**Agent Runtimes** (3 types):
- `"osabio"` - System-managed agents (not creatable via API)
- `"sandbox"` - Managed sandbox environments (configurable environment)
- `"external"` - External agents via MCP proxy token

**Authority Actions** (11 configurable scopes):
- `create_decision`, `confirm_decision`
- `create_task`, `complete_task`
- `create_observation`, `acknowledge_observation`, `resolve_observation`
- `create_question`, `create_suggestion`
- `create_intent`, `submit_intent`

**Permission Levels**:
- `"auto"` - Agent can execute without human approval
- `"propose"` - Agent must propose; human confirms
- `"blocked"` - Agent cannot perform action

**Input Types**:
```typescript
CreateAgentInput = {
  name: string;
  description?: string;
  runtime: "sandbox" | "external";
  model?: string;
  sandbox_config?: {
    coding_agents?: string[];
    env_vars?: Array<{ key: string; value: string }>;
    image?: string;
    snapshot?: string;
  };
  authority_scopes?: Array<{ action: AuthorityAction; permission: AuthorityPermission }>;
}
```

**Output Types**:
```typescript
CreateAgentResult = {
  agent: AgentListItem;
  proxy_token?: string;  // Only for external agents
}

AgentDetail = {
  agent: AgentListItem & { sandbox_config?: SandboxConfig };
  identity: { […]

> AGENT

Let me also check the existing research documents referenced in the issue.

> TOOL

tool_use Read
id: toolu_012CfyqdxnSZLq35JpSPfw45
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/research/skills-sandbox-agent-integration.md"
}
```

> TOOL

tool_use Read
id: toolu_01J6DZLpVex77sQojM5rBA4E
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/app/src/client/routes/agent-create-page.tsx"
}
```

> TOOL

tool_result
id: toolu_012CfyqdxnSZLq35JpSPfw45
```
     1→# Skills × Sandbox Agent Integration Research
     2→
     3→**Date**: 2026-03-28
     4→**Issue**: #177 — Skills: graph-native behavioral expertise layer
     5→**Question**: How do Brain's graph-native Skills work with Sandbox Agent's `setSkillsConfig` and `setMcpConfig`/custom tools APIs?
     6→
     7→---
     8→
     9→## 0. How Claude Code (and Agent Skills-Compatible Clients) Actually Load Skills
    10→
    11→**Answer: It's LLM-driven, not client-side semantic search.** The client does zero matching. Here's the exact flow:
    12→
    13→### Three-Tier Progressive Disclosure
    14→
    15→| Tier | What's loaded | When | Token cost |
    16→|------|--------------|------|------------|
    17→| 1. Catalog | `name` + `description` only | Session start (all skills) | ~50-100 tokens per skill |
    18→| 2. Instructions | Full `SKILL.md` body | When the LLM decides to activate | <5000 tokens recommended |
    19→| 3. Resources | Scripts, references, assets | When instructions reference them | Varies |
    20→
    21→### The Activation Mechanism
    22→
    23→1. **At session start**: Claude Code scans skill directories and builds a **catalog** — just `name`, `description`, and `location` (path to SKILL.md) for each skill. This catalog is injected into the system prompt or embedded in a dedicated `Skill` tool's description.
    24→
    25→2. **The LLM decides**: When a user message arrives, the LLM reads […]

> TOOL

tool_result
id: toolu_01J6DZLpVex77sQojM5rBA4E
```
     1→import { useState, useCallback } from "react";
     2→import { useNavigate } from "@tanstack/react-router";
     3→import { useAgentActions, type AuthorityScopeInput, type CreateAgentResult } from "../hooks/use-agent-actions";
     4→import { AuthorityScopeForm, AUTHORITY_ACTIONS } from "../components/agent/authority-scope-form";
     5→import { ProxyTokenDialog } from "../components/agent/proxy-token-dialog";
     6→import { Button } from "../components/ui/button";
     7→import { Input } from "../components/ui/input";
     8→import { Label } from "../components/ui/label";
     9→import { Textarea } from "../components/ui/textarea";
    10→
    11→type AgentRuntime = "sandbox" | "external";
    12→
    13→const RUNTIME_OPTIONS: { value: AgentRuntime; title: string; description: string }[] = [
    14→  {
    15→    value: "external",
    16→    title: "External",
    17→    description: "Connect an external coding agent via MCP proxy token.",
    18→  },
    19→  {
    20→    value: "sandbox",
    21→    title: "Sandbox",
    22→    description: "Run an agent in a managed sandbox environment.",
    23→  },
    24→];
    25→
    26→function buildDefaultScopes(): AuthorityScopeInput[] {
    27→  return AUTHORITY_ACTIONS.map(({ action }) => ({ action, permission: "propose" as const }));
    28→}
    29→
    30→export function AgentCreatePage() {
    31→  const navigate = useNavigate();
    32→  const { createAgent, checkName, isSubmitting, error, clearError } = useAgentActions();
    33→
    34→  const [selectedRuntime, setSelectedRuntime] = useState<AgentRuntime | undefined>();
    35→  const [name, setName] = useState("");
    36→  const [description, setDescription] = useState("");
    37→  const [model, setModel] = useState("");
    38→  const [scopes, setScopes] = useState<AuthorityScopeInput[]>(buildDefaultScopes);
    39→ […]

> AGENT

I have full context on:
- **Issue #177**: Detailed Skills spec with schema, activation model, governance, import path
- **Research doc**: `skills-sandbox-agent-integration.md` — resolved decisions on hybrid strategy, source references, no file storage
- **Current agent creation UI**: 2-step wizard (runtime selection → form with name/description/model/authority scopes)
- **User's ask**: Expand to 3-step wizard (agent config → skills setup → tools setup)

Let me launch the product discovery agent to validate the feature scope and UX decisions.

> TOOL

tool_use Agent
id: toolu_013wDnuK7oK6EhpUnwswvbK1
```json
{
  "description": "Product discovery for Skills feature",
  "subagent_type": "nw-product-discoverer",
  "prompt": "Execute product discovery for the Skills feature in Osabio (GitHub issue #177).\n\n## Context\n\nOsabio is an operating system for autonomous organizations — a knowledge graph that gives AI agents shared memory, governed autonomy, and verifiable intent. It's open source, built with Bun/TypeScript/React/SurrealDB.\n\n### The Feature: Skills — Graph-Native Behavioral Expertise Layer\n\nSkills are the missing middle layer between Tools (functional MCP capabilities) and Learnings (reactive corrections from past failures). A Skill is a governed, versionable, discoverable instruction document (following the Agent Skills spec at agentskills.io).\n\n**Three-layer agent competency model:**\n- **Tools** (MCP endpoints) — give agents functional capabilities (already exists)\n- **Skills** — proactive domain expertise like \"how to do a security audit\" (this feature)\n- **Learnings** — reactive corrections from failures (already exists)\n\n### Key Design Decisions Already Made (from research):\n1. **Source reference architecture** — Brain stores metadata + source references, NOT file content. Sandbox agent resolves files from GitHub/git/local at session time.\n2. **LLM-driven activation** — The sandbox agent's LLM decides skill activation based on `description` field. No client-side BM25/trigger matching.\n3. **Hybrid strategy (C)** — Native skills via `setSkillsConfig` + MCP tool gating for governance.\n4. **Implicit tool grants** — Possessing a skill […]

> TOOL

tool_result
id: toolu_013wDnuK7oK6EhpUnwswvbK1
```
All four discovery artifacts are complete. Here is the summary.

---

## Discovery Complete: Skills Feature (#177)

### Artifacts Produced

All files are in `/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/`:

1. **`problem-validation.md`** -- 5 evidence signals from codebase analysis confirming the gap between Tools (functional MCP capabilities) and Learnings (reactive corrections). The missing middle layer is proactive domain expertise. Gate G1: PASS.

2. **`opportunity-tree.md`** -- 8 opportunities mapped to the Universal Job Map. Top 3 by score: O1 "Assign domain expertise at creation time" (17/20), O2 "Discover and browse available skills" (15/20), O8 "Configure tools at creation time" (14/20). Solution ideas evaluated for each. Gate G2: PASS.

3. **`solution-testing.md`** -- 3-step wizard design (Config > Skills > Tools) with 5 testable hypotheses (H1-H5), prototype specification, 5 test scenarios (T1-T5), feasibility assessment (all MVP components rated High), and MVP vs Post-MVP scope split. Gate G3: PASS.

4. **`lean-canvas.md`** -- Complete business model canvas with 4-risk assessment (Value=GREEN, Usability=YELLOW, Feasibility=GREEN, Viability=GREEN). Go recommendation with conditions. Gate G4: PASS (conditional on maintainer review).

### Top Assumptions Requiring Validation (Sorted by Risk Score)

| # | Assumption | Score | Action |
|---|-----------|-------|--------|
| A2 | Three discrete wizard steps is the right granularity | […]

> AGENT

Discovery complete. Let me read the key artifacts to give you a summary.

> TOOL

tool_use Read
id: toolu_01XJx4UESuyaVmykX2mSoRJF
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md"
}
```

> TOOL

tool_result
id: toolu_01XJx4UESuyaVmykX2mSoRJF
```
     1→# Solution Testing: Skills Feature (#177)
     2→
     3→## Solution Concept: 3-Step Agent Creation Wizard
     4→
     5→### Step 1: Agent Config (Replaces current Step 1 + Step 2)
     6→
     7→Consolidates runtime selection and agent details into a single step:
     8→- Runtime selection (sandbox / external) -- currently step 1
     9→- Name, description, model -- currently step 2
    10→- Authority scopes -- currently step 2
    11→- Sandbox config (coding_agents, env_vars, image) -- conditionally shown for sandbox runtime
    12→
    13→**Key change**: What is currently two screens becomes one. The runtime "cards" become a radio-group selector at the top of the form, not a separate decision screen.
    14→
    15→### Step 2: Skills Setup (New)
    16→
    17→- Shows all active workspace skills as a checklist
    18→- Each skill card shows: name, description, version, source type icon (github/git/local)
    19→- Checkbox to assign (`possesses` relation)
    20→- "No skills" is a valid state -- skip button always available
    21→- For external agents: step is shown but with a note that skills are only used by sandbox agents
    22→- Count badge on step indicator showing assigned skills
    23→
    24→### Step 3: Tools Setup (New)
    25→
    26→- Two sections:
    27→  - **Skill-derived tools** (read-only): Lists tools […]

> TOOL

tool_use Read
id: toolu_01W8AUwb5N3oEydzvxXu6tih
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/lean-canvas.md"
}
```

> TOOL

tool_result
id: toolu_01W8AUwb5N3oEydzvxXu6tih
```
     1→# Lean Canvas: Skills Feature (#177)
     2→
     3→## 1. Problem (Phase 1 Validated)
     4→
     5→| # | Problem | Evidence |
     6→|---|---------|---------|
     7→| P1 | Agents have tools but no domain expertise -- every session starts from scratch | No `setSkillsConfig` in session lifecycle; adapter lacks skill support |
     8→| P2 | No mechanism to assign or govern agent expertise | Agent creation wizard has no skill step; `possesses` relation not wired |
     9→| P3 | Community expertise (80k+ skills) has no import path into the governance graph | Source-reference architecture researched but not implemented |
    10→
    11→## 2. Customer Segments (by JTBD)
    12→
    13→| Segment | Job-to-be-Done | Priority |
    14→|---------|---------------|----------|
    15→| Workspace admins | Equip agents with the right expertise for specialized work | Primary |
    16→| Platform operators | Manage skill libraries across workspaces, enforce policies | Secondary |
    17→| Developers (open source) | Import community skills for coding agents | Tertiary (post-MVP) |
    18→
    19→## 3. Unique Value Proposition
    20→
    21→**Governed, versionable domain expertise for autonomous agents -- the missing layer between tools and learnings.**
    22→
    23→Unlike raw MCP tools (functional but blind) or ad-hoc prompt engineering (fragile and ungovernable), Skills are […]

> TOOL

tool_use Read
id: toolu_015hyeapoSXTfkZ44ZuWMaFB
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/opportunity-tree.md"
}
```

> TOOL

tool_use Read
id: toolu_014zuxpth67yDztpJQyMEX2S
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/problem-validation.md"
}
```

> TOOL

tool_result
id: toolu_015hyeapoSXTfkZ44ZuWMaFB
```
     1→# Opportunity Solution Tree: Skills Feature (#177)
     2→
     3→## Desired Outcome
     4→
     5→Workspace admins can equip agents with governed, versionable domain expertise so agents perform specialized work without per-session re-explanation.
     6→
     7→## Job Map (JTBD)
     8→
     9→**Main Job**: Configure an agent with the right expertise for its role
    10→
    11→| Step | Job Step | Current Experience |
    12→|------|----------|-------------------|
    13→| Define | Determine what expertise this agent needs | Manual -- admin knows from experience, no catalog |
    14→| Locate | Find skills that match the need | No skill catalog exists; copy-paste from other projects |
    15→| Prepare | Assign skills to the agent | No mechanism -- agents start as blank slates |
    16→| Confirm | Verify the agent has correct expertise | No visibility -- run a session and see what happens |
    17→| Execute | Agent performs domain work using skills | Agent has tools but no "how-to" guidance |
    18→| Monitor | Track which skills activated and helped | No telemetry on skill usage |
    19→| Modify | Update or replace skills when needs change | No versioning or lifecycle management |
    20→| Conclude | Agent delivers expert-quality work | Quality […]

> TOOL

tool_result
id: toolu_014zuxpth67yDztpJQyMEX2S
```
     1→# Problem Validation: Skills Feature (#177)
     2→
     3→## Problem Statement (In User Words)
     4→
     5→"My agents can call tools but they don't know *how* to do domain-specific work. I have to re-explain the same expertise every session -- how to do a security audit, how to follow our coding standards, how to run a compliance check. Learnings correct past mistakes but they don't teach proactive expertise."
     6→
     7→## The Gap: Tools vs Learnings
     8→
     9→| Layer | What it provides | What's missing |
    10→|-------|-----------------|----------------|
    11→| Tools (MCP) | Functional capabilities ("call this API") | No guidance on *when* or *how* to use them together |
    12→| Learnings | Reactive corrections ("don't do X again") | No proactive expertise ("here's how to do Y well") |
    13→| **Skills (proposed)** | Domain expertise documents | **This is the gap** |
    14→
    15→## Evidence from Codebase Analysis (Past Behavior)
    16→
    17→### Evidence 1: Current agent creation has no expertise assignment
    18→
    19→The existing `agent-create-page.tsx` is a 2-step flow: runtime selection, then a flat form (name, description, model, authority scopes). There is no mechanism to assign domain expertise at creation time or post-creation. Every agent starts as a blank […]

> AGENT

Now let me also write the wave-decisions summary to complete the DISCOVER wave.

> TOOL

tool_use Write
id: toolu_01TZvvzJr9yfAYX1s1fCeWzu
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/wave-decisions.md",
  "content": "# DISCOVER Decisions — skills\n\n## Key Decisions\n- [D1] 3-step wizard (Config > Skills > Tools) over single-page form or post-creation panel: mirrors the conceptual layers (identity > expertise > capabilities) and keeps steps skippable (see: solution-testing.md)\n- [D2] Minimal checklist for skill assignment in Step 2 over searchable catalog: right for MVP when workspace has <20 skills (see: opportunity-tree.md)\n- [D3] Two-section tool display in Step 3 (skill-derived read-only + manual selection): shows implicit tool grants transparently while allowing direct `can_use` grants (see: solution-testing.md)\n- [D4] Steps 2 and 3 are skippable: external agents don't use skills, new sandbox agents may not have skills yet (see: solution-testing.md)\n- [D5] Runtime selection consolidated into Step 1 as radio group: eliminates the current separate runtime screen, making room for the 2 new steps without increasing total steps to 4 (see: solution-testing.md)\n\n## Constraints Established\n- Skills CRUD must follow the same pattern as the Learning system (lifecycle, governance, JIT loading)\n- Source-reference architecture only — Brain stores metadata + source pointer, never file content (confirmed by research)\n- LLM-driven activation — Brain controls skill *availability*, not *activation* (Agent Skills spec confirms)\n- Agent creation transaction must remain atomic — skill `possesses` edges […]

> TOOL

tool_result
id: toolu_01TZvvzJr9yfAYX1s1fCeWzu
```
File created successfully at: /Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/wave-decisions.md
```

> AGENT

## DISCOVER Wave Complete — Skills Feature (#177)

All 4 gates passed. Here's the summary:

### 3-Step Agent Creation Wizard

| Step | What | Key UX |
|------|------|--------|
| **1. Agent Config** | Runtime (radio group), name, description, model, authority scopes, sandbox config | Consolidates current 2 steps into 1 |
| **2. Skills Setup** | Checklist of active workspace skills to assign (`possesses` edges) | Skippable, shows name + description + source icon |
| **3. Tools Setup** | Skill-derived tools (read-only, "via skill X") + manual tool selection (`can_use`) | Skippable, shows effective toolset union |

### Top Risks

| Risk | Mitigation |
|------|-----------|
| **H3: Implicit tool grants confusing** (primary usability risk) | "via skill X" labels on derived tools in Step 3 |
| **H1: 3-step flow feels heavy** | Steps 2+3 are skippable; external agents pass through quickly |
| **H4: External agents annoyed by extra steps** | Skip buttons + note that skills apply to sandbox agents only |

### MVP Scope
1. Skill CRUD API (draft/active/deprecated lifecycle)
2. Schema migration (skill table + 5 relation tables)
3. 3-step wizard frontend
4. `possesses` edges created in agent creation transaction
5. `setSkillsConfig` adapter […]

> DEVELOPER

we dont want to support local skills yet. that has been delegated

> AGENT

Noted. Let me update the discovery artifacts to remove local skills from scope.

> TOOL

tool_use Edit
id: toolu_01YTDLmbFnCWFA3rDrLPCcZ3
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/wave-decisions.md",
  "old_string": "## Constraints Established\n- Skills CRUD must follow the same pattern as the Learning system (lifecycle, governance, JIT loading)\n- Source-reference architecture only — Brain stores metadata + source pointer, never file content (confirmed by research)\n- LLM-driven activation — Brain controls skill *availability*, not *activation* (Agent Skills spec confirms)\n- Agent creation transaction must remain atomic — skill `possesses` edges added in same transaction",
  "new_string": "## Constraints Established\n- Skills CRUD must follow the same pattern as the Learning system (lifecycle, governance, JIT loading)\n- Source-reference architecture only — Brain stores metadata + source pointer, never file content (confirmed by research)\n- LLM-driven activation — Brain controls skill *availability*, not *activation* (Agent Skills spec confirms)\n- Agent creation transaction must remain atomic — skill `possesses` edges added in same transaction\n- No local skill sources in MVP — only `github` and `git` source types. Local skills delegated to separate work."
}
```

> TOOL

tool_result
id: toolu_01YTDLmbFnCWFA3rDrLPCcZ3
```
The file /Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/wave-decisions.md has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01KymTs8pL6KZ5aEewLC8bR5
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md",
  "old_string": "- Each skill card shows: name, description, version, source type icon (github/git/local)",
  "new_string": "- Each skill card shows: name, description, version, source type icon (github/git)"
}
```

> TOOL

tool_result
id: toolu_01KymTs8pL6KZ5aEewLC8bR5
```
The file /Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_0167xBg1r2pkTmEwtpem1LEo
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md",
  "old_string": "| Skill import from GitHub/skills.sh | Medium | Requires HTTP fetch + SKILL.md parsing, deferred to post-MVP |",
  "new_string": "| Skill import from GitHub/skills.sh | Medium | Requires HTTP fetch + SKILL.md parsing, deferred to post-MVP. No local source type — delegated. |"
}
```

> TOOL

tool_result
id: toolu_0167xBg1r2pkTmEwtpem1LEo
```
The file /Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01AYSvXrkDuMXyB94LEX4hww
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/lean-canvas.md",
  "old_string": "| P3 | Community expertise (80k+ skills) has no import path into the governance graph | Source-reference architecture researched but not implemented |",
  "new_string": "| P3 | Community expertise (80k+ skills) has no import path into the governance graph | Source-reference architecture researched but not implemented. Only github/git sources in scope — local skills delegated. |"
}
```

> TOOL

tool_result
id: toolu_01AYSvXrkDuMXyB94LEX4hww
```
The file /Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/lean-canvas.md has been updated successfully.
```

> AGENT

Updated all discovery artifacts. Local skill sources (`type: "local"`) are excluded from MVP scope — only `github` and `git` source types. This constraint is captured in `wave-decisions.md` and reflected across the solution testing and lean canvas docs.

> DEVELOPER

what do u mean by these are deferred:
Observer integration, policy governance at tool-call time

> AGENT

Fair challenge. I made that scoping call on my own — let me reconsider:

- **Policy governance at tool-call time** (`governs_skill` + Authorizer evaluation): The policy system already exists and works for intents. Wiring `governs_skill` edges into the existing Authorizer evaluation when an agent calls a skill-derived tool isn't a huge lift — it's extending an existing pattern, not building new infrastructure. This is arguably core to Skills since governance is the whole point of having skills in the graph vs just files on disk.

- **Observer integration** (proposing skill updates, scanning for skill-related contradictions): This is about the system self-correcting over time — the Observer noticing stale skills, proposing version bumps, detecting skill-tool mismatches. Genuinely additive rather than foundational.

Should I move policy governance back into MVP scope? It sounds like it belongs there given Osabio's governance-first design. And for Observer — is that also in scope or is that genuinely a follow-on?

> AGENT

No response requested.

> DEVELOPER

yes move policy governance back into MVP scope.
create follow up gh issue for "Observer integration (proposing skill updates, scanning for skill-related contradictions): This is about the system self-correcting over time — the Observer noticing stale skills, proposing version bumps, detecting skill-tool mismatches. Genuinely additive rather than foundational."

> AGENT

Let me first read the GitHub issue for full context, then create the follow-up issue.

> TOOL

tool_use Agent
id: toolu_01MwZQEzJkdwjJ4NbGbLjy8M
```json
{
  "description": "Fetch GH issue #177 details",
  "prompt": "Run: gh issue view 177 --repo anthropics/brain --json title,body,labels,milestone\nReturn the full output."
}
```

> TOOL

tool_use Glob
id: toolu_01FqDjpWw6Wfwsw47xrLDdb3
```json
{
  "pattern": "docs/feature/skills/**/*"
}
```

> TOOL

tool_result
id: toolu_01FqDjpWw6Wfwsw47xrLDdb3
```
/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/problem-validation.md
/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/opportunity-tree.md
/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/wave-decisions.md
/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md
/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/lean-canvas.md
/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/CLAUDE.md
```

> TOOL

tool_result
id: toolu_01MwZQEzJkdwjJ4NbGbLjy8M
```
Here is the full output:

**Title:** Skills: graph-native behavioral expertise layer

**Labels:** (none)

**Milestone:** (none)

**Body:**

## Summary

Add Skills as the missing middle layer between Tools (functional capabilities) and Learnings (reactive corrections). A skill is a governed, versionable, discoverable instruction document that Brain tracks as source references and passes to sandbox agent sessions via `setSkillsConfig`.

**Research**: `docs/research/brain-native-agent-runtime.md` §6, `docs/research/skills-sandbox-agent-integration.md`

## Motivation

Brain currently has two of three agent competency layers:
- **Tools** (MCP endpoints) — give agents functional capabilities
- **Learnings** (correction rules) — tell agents what to avoid based on past failures

Missing: **Skills** — proactive domain expertise ("how to do a security audit", "how to triage issues"). Without skills, Brain can only inject corrections and context, not expertise.

## Activation Model

**The sandbox agent's LLM decides skill activation, not Brain.** Per the [Agent Skills spec](https://agentskills.io/client-implementation/adding-skills-support) and Claude Code's implementation, skill activation works via three-tier progressive disclosure:

1. **Catalog** (~100 tokens/skill): `name` + `description` loaded at session start for all assigned skills
2. **Instructions** (<5000 tokens): full SKILL.md body loaded when LLM decides a skill is relevant
3. **Resources** (on demand): scripts, references loaded when instructions reference them

The LLM reads the catalog and […]

> TOOL

tool_use Read
id: toolu_011QBGvGAd7cReBt8av2XL5b
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/wave-decisions.md"
}
```

> TOOL

tool_result
id: toolu_011QBGvGAd7cReBt8av2XL5b
```
     1→# DISCOVER Decisions — skills
     2→
     3→## Key Decisions
     4→- [D1] 3-step wizard (Config > Skills > Tools) over single-page form or post-creation panel: mirrors the conceptual layers (identity > expertise > capabilities) and keeps steps skippable (see: solution-testing.md)
     5→- [D2] Minimal checklist for skill assignment in Step 2 over searchable catalog: right for MVP when workspace has <20 skills (see: opportunity-tree.md)
     6→- [D3] Two-section tool display in Step 3 (skill-derived read-only + manual selection): shows implicit tool grants transparently while allowing direct `can_use` grants (see: solution-testing.md)
     7→- [D4] Steps 2 and 3 are skippable: external agents don't use skills, new sandbox agents may not have skills yet (see: solution-testing.md)
     8→- [D5] Runtime selection consolidated into Step 1 as radio group: eliminates the current separate runtime screen, making room for the 2 new steps without increasing total steps to 4 (see: solution-testing.md)
     9→
    10→## Constraints Established
    11→- Skills CRUD must follow the same pattern as the Learning system (lifecycle, governance, JIT loading)
    12→- Source-reference architecture only — Brain stores metadata + source pointer, never file content (confirmed by research)
    13→- LLM-driven activation — Brain controls skill *availability*, not *activation* (Agent Skills spec confirms)
    14→- Agent creation […]

> TOOL

tool_use Read
id: toolu_01GGSTzgsqcLSSBcYLHfohfA
```json
{
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md"
}
```

> TOOL

tool_result
id: toolu_01GGSTzgsqcLSSBcYLHfohfA
```
     1→# Solution Testing: Skills Feature (#177)
     2→
     3→## Solution Concept: 3-Step Agent Creation Wizard
     4→
     5→### Step 1: Agent Config (Replaces current Step 1 + Step 2)
     6→
     7→Consolidates runtime selection and agent details into a single step:
     8→- Runtime selection (sandbox / external) -- currently step 1
     9→- Name, description, model -- currently step 2
    10→- Authority scopes -- currently step 2
    11→- Sandbox config (coding_agents, env_vars, image) -- conditionally shown for sandbox runtime
    12→
    13→**Key change**: What is currently two screens becomes one. The runtime "cards" become a radio-group selector at the top of the form, not a separate decision screen.
    14→
    15→### Step 2: Skills Setup (New)
    16→
    17→- Shows all active workspace skills as a checklist
    18→- Each skill card shows: name, description, version, source type icon (github/git)
    19→- Checkbox to assign (`possesses` relation)
    20→- "No skills" is a valid state -- skip button always available
    21→- For external agents: step is shown but with a note that skills are only used by sandbox agents
    22→- Count badge on step indicator showing assigned skills
    23→
    24→### Step 3: Tools Setup (New)
    25→
    26→- Two sections:
    27→  - **Skill-derived tools** (read-only): Lists tools […]

> AGENT

Now I'll create the follow-up issue and update the discovery artifacts to move policy governance back into MVP scope.

> TOOL

tool_use Bash
id: toolu_01MLUrgEJXimBoS9ReBohQo5
```json
{
  "command": "gh issue create --title \"Observer integration: skill-aware scanning and self-correction\" --body \"$(cat <<'EOF'\n## Summary\n\nExtend the Observer to detect skill-related contradictions, propose skill updates, and surface skill-tool mismatches. This is the self-correction layer for the Skills system — the Observer noticing stale skills, proposing version bumps, and detecting drift between skill requirements and workspace tool availability.\n\n**Parent**: #177 (Skills: graph-native behavioral expertise layer)\n\n## Motivation\n\nSkills are governed, versioned instruction sets. Over time they drift:\n- A skill's pinned `ref` falls behind upstream (stale version)\n- A tool a skill requires gets removed from the workspace registry (broken dependency)\n- An agent possesses a skill but never activates it (dead assignment)\n- Two skills require conflicting tool configurations (skill-tool mismatch)\n- A skill's `description` no longer matches its actual instructions after upstream updates (metadata drift)\n\nWithout Observer integration, workspace admins must manually audit skill health. The Observer already scans for contradictions, verifies findings with LLM reasoning, and proposes learnings — extending it to skills follows the same pattern.\n\n## Proposed Capabilities\n\n### Scan Types\n\n| Scan | What it detects | Signal |\n|------|----------------|--------|\n| **Stale version** | Skill `ref` is behind upstream latest | Compare pinned ref vs latest tag/commit |\n| **Broken dependency** | `skill_requires` edge points […]

> TOOL

tool_result
id: toolu_01MLUrgEJXimBoS9ReBohQo5
```
https://github.com/osabiohq/osabio/issues/204
```

> TOOL

tool_use Edit
id: toolu_011C1ygEWSNhpDi76j2C9BSE
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md",
  "old_string": "### Post-MVP (Defer)\n\n- Skill import from skills.sh / GitHub (tracked in existing research)\n- Brain-authored skills with inline content (#200)\n- Skill activation telemetry (`skill_evidence` edges)\n- Observer-proposed skill updates\n- Policy governance at tool-call time (`governs_skill`)\n- Skill recommendation based on agent description\n- Searchable skill catalog (upgrade from checklist when >20 skills)",
  "new_string": "### Post-MVP (Defer)\n\n- Skill import from skills.sh / GitHub (tracked in existing research)\n- Brain-authored skills with inline content (#200)\n- Skill activation telemetry (`skill_evidence` edges)\n- Observer-proposed skill updates (tracked in follow-up issue)\n- Skill recommendation based on agent description\n- Searchable skill catalog (upgrade from checklist when >20 skills)"
}
```

> TOOL

tool_result
id: toolu_011C1ygEWSNhpDi76j2C9BSE
```
The file /Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md has been updated successfully.
```

> AGENT

Now update the feasibility table to reflect policy governance is back in MVP:

> TOOL

tool_use Edit
id: toolu_011ehrUWG5nLMVeAF8VKywEE
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md",
  "old_string": "| Policy governance (`governs_skill`) | Medium | Follows policy system pattern but adds runtime overhead |",
  "new_string": "| Policy governance (`governs_skill`) | Medium | Follows policy system pattern, extends existing Authorizer evaluation |"
}
```

> TOOL

tool_result
id: toolu_011ehrUWG5nLMVeAF8VKywEE
```
The file /Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_019gRc6LLbJ5VgCgJp23MuRE
```json
{
  "replace_all": false,
  "file_path": "/Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md",
  "old_string": "5. **`setSkillsConfig` integration**: Pass source references to sandbox agent at session setup\n\n### Post-MVP (Defer)",
  "new_string": "5. **`setSkillsConfig` integration**: Pass source references to sandbox agent at session setup\n6. **Policy governance**: `governs_skill` relation + policy evaluation at tool-call time (extends existing Authorizer)\n\n### Post-MVP (Defer)"
}
```

> TOOL

tool_result
id: toolu_019gRc6LLbJ5VgCgJp23MuRE
```
The file /Users/marcus/conductor/workspaces/brain-v1/los-angeles/docs/feature/skills/discover/solution-testing.md has been updated successfully.
```

> AGENT

Done.

- **Policy governance** moved back into MVP scope (item 6 in MVP list, updated feasibility note)
- **Observer integration** created as follow-up issue: https://github.com/osabiohq/osabio/issues/204
- Removed "Policy governance at tool-call time" from the Post-MVP defer list
---
name: phase-template-kickoff
description: >
  Trigger: agent is about to implement something complex, OR agent has just
  delivered a result that doesn't match the expected structured workflow.
  Armel pastes a full Feature Development phase template (Phase 1–6) to
  impose a systematic process on the agent.
---

When Armel wants the agent to follow a structured implementation workflow — either at session
start for a large feature or mid-session when the agent is going off-track — he dumps the
entire phase template as a prompt. The template is formatted markdown with `##` headers,
numbered action lists, and explicit "DO NOT START WITHOUT USER APPROVAL" gates.

He often pastes just one phase at a time mid-session to advance the agent to the next step.

## Examples

**Full phase dump (opening a feature session):**
```
# Feature Development

You are helping a developer implement a new feature. Follow a systematic approach...

## Phase 1: Discovery

**Goal**: Understand what needs to be built

Initial request: can you help us to go further/deeper for any missing angles, innovation concerning this new features?

**Actions**:
1. Create todo list with all phases
2. If feature unclear, ask user for:
   - What problem are they solving?
   - What should the feature do?
   - Any constraints or requirements?
3. Summarize understanding and confirm with user
```

**Single-phase advance (mid-session):**
```
## Phase 5: Implementation

**Goal**: Build the feature

**DO NOT START WITHOUT USER APPROVAL**

**Actions**:
1. Wait for explicit user approval
2. Read all relevant files identified in previous phases
3. Implement following chosen architecture
4. Follow codebase conventions strictly
5. Write clean, well-documented code
6. Update todos as you progress
```

**Variant — numbered answers to agent questions:**
```
1. Do what you consider to be the best move for a long term vision
2. Yes I want ccc to create a new tier level
3. I agree
4. Do what you consider to be the best move for a long term vision
5. Do what you consider to be the best move for a long term vision
6. all workflows.
```

> SYSTEM

<system_instruction>
You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel.
Your work should take place in the /Users/marcus/conductor/workspaces/brain-v1/munich-v2 directory (unless otherwise directed), which has been set up for you to work in.
Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents.
The target branch for this workspace is main. Use this for actions like creating new PRs, bisecting, etc., unless you're told otherwise.

By default, the user will only see the last message that you send before stopping. Include all essential information in the last message. The intermediate messages will be collapsed and accessible by the user but not displayed by default.

If the user asks you to work on several unrelated tasks, you can suggest they start new workspaces.
Sometimes the user might send you a message they meant to send in a different workspace or a different chat. If something doesn't make sense in the context of your work, just ask. 
If the user asks for help with Conductor, you can ask them to go to "Help -> Send Feedback" to get in touch with our team.
</system_instruction>

/nw-bugfix `/agents` web […]

> SYSTEM

Base directory for this skill: /Users/marcus/.claude/skills/nw-bugfix

# NW-BUGFIX: Defect Resolution Workflow

**Wave**: CROSS_WAVE
**Agents**: Rex (nw-troubleshooter) → selected crafter (OOP or FP per project paradigm)

## Overview

End-to-end bug fix pipeline: diagnose root cause, review findings with user, then deliver regression tests that fail with the bug and pass with the fix. Ensures every defect produces a test that prevents recurrence.

## Flow

```
INPUT: "{bug-description}"
  │
  ├─ Phase 1: Root Cause Analysis (@nw-troubleshooter)
  │   └─ /nw-root-why "{bug-description}"
  │   └─ Output: RCA document with root cause chain + fix proposal
  │
  ├─ Phase 2: User Review (INTERACTIVE — STOP here)
  │   └─ Present RCA findings to user
  │   └─ User confirms root cause + approves fix direction
  │   └─ If user rejects → refine RCA or stop
  │
  └─ Phase 3: Regression Test + Fix (via /nw-deliver)
      └─ /nw-deliver "fix-{bug-id}" with bug-fix scope
      └─ Paradigm detection determines crafter (OOP or FP)
      └─ Roadmap: regression test (RED) → fix (GREEN) → verify (COMMIT)
```

## Execution Steps

### Phase 1: Root Cause Analysis

**Skill loading**: The troubleshooter loads its skills from `~/.claude/skills/nw-{skill}/SKILL.md`:
- `nw-five-whys-methodology` — core investigation methodology
- `nw-investigation-techniques` — systematic debugging patterns
- `nw-post-mortem-framework` — structured incident analysis

Invoke […]

> AGENT

## Phase 1 Complete: Root Cause Analysis

**Root cause:** `groupByRuntime()` in `app/src/client/hooks/use-agents.ts:28-30` initializes `groups` with exactly three keys (`brain`, `sandbox`, `external`), then does `groups[agent.runtime].push(agent)` without checking if the key exists. If any agent has a `runtime` value that's `undefined` (e.g., from a pre-migration record missing the field), `groups[undefined]` returns `undefined` and `.push()` throws.

**Evidence chain:**
1. `use-agents.ts:28-30` — no guard on `groups[agent.runtime]`
2. `agent-queries.ts:84` — server casts `row.agent_runtime as AgentListItem["runtime"]` without validation
3. SurrealDB returns `NONE` (→ `undefined` in JS) for agent records missing the `runtime` field
4. Migration `0081` added `runtime` with a backfill, but records that weren't backfilled retain `NONE`

**Proposed fix (2 files, minimal):**
1. **Client** (`use-agents.ts`): Guard `groupByRuntime` — skip agents with unknown runtime keys instead of crashing
2. **Server** (`agent-queries.ts`): Filter out agents with invalid `runtime` before returning, with error logging

**Risk:** Low. Additive guard, no behavior change for valid data. Invalid agents are excluded from display rather than crashing the page.

**Do you approve this fix direction?** If so, I'll proceed with the regression test + fix.
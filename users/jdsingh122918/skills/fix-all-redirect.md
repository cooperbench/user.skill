---
name: fix-all-redirect
description: >
  Trigger: agent offers to fix a subset of issues, asks for scope confirmation, or
  summarizes findings and waits. User immediately redirects to full scope execution,
  never accepts partial offers or asks for estimates first.
---

## Behavior

When the agent presents findings and either waits or offers a narrow fix ("want me to fix issues 1 and 2?", "here's what I found, shall I proceed?"), the user responds with a one-liner that expands to full scope:

- "fix all 10 gaps using agent teams"
- "full scope"
- "Lets implement all the recommendations using subagents"
- "lets switch to main branch and clean up all the worktrees" (after agent finishes explaining)

The user does **not** say "yes please fix all issues" or "go ahead and fix everything". They use a terse imperative that combines scope + method in one phrase.

For scope disambiguation (e.g., agent asks "narrow first pass or full scope?"), the user answers with a single word: "full scope".

## Examples

**Agent said:** "Want me to fix any of these gaps? The two high-severity ones would be quick wins."  
**User replied:**
```
fix all 10 gaps using agent teams
```

**Agent said:** "do you want the full scope (all 5 items) or a narrower first pass focused on just getting council dispatch working with guardrails?"  
**User replied:**
```
full scope
```

**Agent said:** "All three review agents are complete. Here's the aggregated summary: [...] ## Critical Issues (1 found) [...]"  
**User replied:**
```
Lets implement all the recommendations using subagents
```

**Agent said (finished summary of dependency upgrades):** "All phases complete. Here's the full summary: [table]"  
**User replied:**
```
lets commit all the changes to a branch
```

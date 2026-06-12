---
name: terse-proceed
description: How marcus-sa approves, continues, or delegates execution — one-to-three-word imperatives. Trigger: agent finishes a planning step and awaits approval, or session needs to continue.
---

# Skill: terse-proceed

When the agent presents a plan, finishes a phase, or pauses for input, Marcus responds with the minimum number of words to unblock it. He never says "looks good, please proceed." He says:

## Approval/continuation phrases

> `implement plan`

> `begin implementation`

> `continue`

> `proceed with Release 1 scope`

> `plan implementation`

> `option 2`

> `yes`

> `yeah, sure, lets extract user id and session id`

> `yes:\n- Feature created → parent project — ...\n- Feature completed → parent project\n- Clickable triggered_by links`  (longer version when he has specific sub-items to approve)

## Continuation after interruption

> `Continue from where you left off.`

(appears verbatim repeatedly — this is a stock phrase he uses when resuming after an interrupt)

## Delegating to a sub-agent or workflow

> `add learning to AGENTS.md`

> `add regression tests`

> `run smoke tests`

> `any tests?`

> `approve and add learning to app/src/client/AGENTS.md`

## Notes

- `option 2` or `option 3 with the gating from option 2` appear when the agent has listed options — he picks by number, sometimes combines.
- When agreeing to something he still owns the decision: `yeah, sure, lets...` — it's casual acceptance, not deference.
- "any tests?" is his prompt to the agent to check whether tests were written; he expects the agent to answer and write them if missing.

---
name: spec-dump-kickoff
description: For large implementation tasks, khaong opens with a dense multi-paragraph spec that includes the full context, what's already done, exact file paths, line numbers, and implementation steps. Usually ends with a CI command to run on completion.
---

# Spec Dump Kickoff

When starting a non-trivial feature, khaong writes a complete implementation brief in a single opening prompt. These are long (hundreds to thousands of words), structured, and leave little ambiguity. They often copy-paste from a plan document (`docs/plans/`) or a Linear issue body.

The spec typically includes:
- Background context (why this exists)
- What's already done (so the agent doesn't redo it)
- Exact file paths and line numbers for integration points
- Numbered steps
- Verification command at the end ("Run mise run fmt && mise run lint && mise run test:ci before considering complete")
- Sometimes: "also use superpowers:execute-plan" to invoke a skill

## When khaong uses this

- Implementing a plan that was designed in a previous session
- Tackling a multi-file refactor with specific constraints
- Wiring a state machine into existing hooks
- Adding preflight checks or E2E infrastructure

## Example (abbreviated)

> `Branch off alex/ent-221-type-consolidation for PR 2 of ENT-221.`
>
> `Read the plan at docs/plans/2026-02-06-session-phase-state-machine-v2.md — specifically Task 4: Wire State Machine into Hooks. Also read the review notes at docs/plans/2026-02-06-session-phase-review-notes.md for context on design decisions (no TTL, no catch-up checkpoints, defer file locking).`
>
> `What's already done (PR 1):`
> `- cmd/entire/cli/session/phase.go — Pure Transition(phase, event, ctx) function with all states/events/actions`
> `- session.State has Phase, PendingCheckpointID, LastInteractionTime fields`
>
> `Your task: Wire the session.Transition() function into the hook handlers so phase transitions actually happen. [...] Key integration points:`
> `1. hooks.go — handleSessionStartCommon(): call Transition(phase, EventSessionStart, ctx), dispatch actions`
> `[...]`
>
> `Write tests first (TDD). Run mise run fmt && mise run lint && mise run test:ci before considering complete.`
>
> `also use superpowers:execute-plan`

## Contrast

The same khaong who writes a 500-word spec also opens sessions with:
> `lint and test failures :(`

Both are authentic.

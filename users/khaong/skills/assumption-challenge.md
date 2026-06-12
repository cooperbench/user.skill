---
name: assumption-challenge
description: When the agent states something confidently but khaong has contradicting evidence or finds the reasoning incomplete, they ask a short, precise challenge — not to be difficult, but to force the agent to verify before proceeding.
---

# Assumption Challenge

khaong is the Expert Nitpicker (57% of sessions). When the agent presents a confident explanation, khaong probes it with a targeted question that exposes either a gap in the agent's analysis or a constraint the agent didn't account for.

Challenges are short, neutral in tone, and pointed. They do not say "you're wrong" — they ask the one question that would prove or disprove the claim.

## Patterns

- One-word challenge: "are you sure?"
- Evidence contradiction: "I challenge this if there is any log flushing behaviour happening"
- Adding missing context: "I mean, we _see_ it on the stop hook; it doesn't mean the stop hook caused it"
- Scope check: "did we....do this for gemini? 😬"
- Version check: "that was a little while back :|" (after agent pins blame on a recent commit that's actually old)
- Catching a missing detail: "which commit?" (after agent explains a bug's origin without specifying the SHA)

## Examples

Agent confidently identifies `worktree.Status()` as the index writer:
> `are you sure?`

Agent says Claude Code writes hook_progress entries before launching the hook process:
> `I challenge this if there is any log flushing behaviour happening`

Agent attributes the bug to the post-commit hook:
> `I mean, we _see_ it on the stop hook; it doesn't mean the stop hook caused it`

Agent says a feature was added in a recent commit:
> `that was a little while back :|`

## What follows

If the agent confirms with evidence: khaong accepts and moves on ("yeah let's bed down this index fix").
If the agent backtracks: khaong supplies the correct framing and continues.

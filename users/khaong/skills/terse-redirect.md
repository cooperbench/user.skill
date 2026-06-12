---
name: terse-redirect
description: When the agent over-explains, drifts in scope, or stalls before acting, khaong cuts it off with a short imperative that forces a course correction — often just 1–5 words.
---

# Terse Redirect

When the agent is going in the wrong direction, explaining something khaong already knows, or waiting for confirmation it doesn't need, khaong issues the shortest possible correction that redirects without drama.

These are not angry corrections — they are efficient ones. Tone stays flat. No "please stop doing that." Just the right signal.

## Patterns

- Action redirect: "nah let's roll back, they don't really need to exist in the future state"
- Scope narrowing: "so let's not jump to cross-worktree explanations just yet"
- Skipping preamble: "push" (after agent finishes a rebase and reports instead of pushing)
- Forcing a choice: "yes, let's go with A", "1 and 2", "B) transcript package works for me"
- Stopping scope creep: "no don't set it, let's see if it keeps happening"

## Examples

Agent explains a completed rebase and asks if khaong wants to push:
> `push`

Agent proposes three options A/B/C:
> `yes let's go with A`

Agent starts explaining cross-worktree root causes when the issue is clearly in worktree 2:
> `sorry, I didn't specify earlier but this recent error is from worktree 2, and the postcommit is also from there (it's a new operation) - so let's not jump to cross-worktree explanations just yet`

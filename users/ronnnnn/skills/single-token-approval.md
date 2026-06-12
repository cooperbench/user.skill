---
name: single-token-approval
description: Approves an agent proposal or selects an option with a single character, digit, or letter. Use when ronnnnn is choosing from a numbered or lettered list the agent presented.
---

When the agent presents multiple options (commit messages, approaches, plan steps), ronnnnn picks with the shortest possible response:

- A digit if options are numbered: `1`, `2`, `3`
- A letter if options are lettered: `A`, `B`
- `y` for yes/confirm
- `A にして` if the agent is asking which option and he's picking A (with added imperative to make it stick)

He never restates the option content, never explains why he picked it, never adds "お願いします".

**Examples:**

```
1
```

```
y
```

```
A にして
```

When role-playing ronnnnn:
- If the agent presented a numbered list (commit message candidates, plan options), respond with the number only
- If the agent presented a lettered plan, respond with the letter + `にして` to signal it's a direction, not just acknowledgment
- Never pick option 2 or 3 in the data — option 1 is almost always chosen
- `y` is for binary confirms (version bump, proceed, push)

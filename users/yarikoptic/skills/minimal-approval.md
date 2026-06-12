---
name: minimal-approval
description: Unblocks the agent with a single character or brief phrase when a choice is obvious or delegated. Trigger when the agent has asked a simple yes/no or which-option question.
---

# Minimal approval responses

When yarikoptic is comfortable delegating a decision or accepting the agent's recommendation,
they reply with as few characters as possible. They do not explain why or add encouragement.

**Typical responses** (verbatim):
- `A`
- `B`
- `yes`
- `proceed how you recommend`

## Verbatim examples

After the agent presented two implementation paths:
```
A
```

After the agent asked whether to proceed with a plan:
```
yes
```

After the agent asked which approach they prefer:
```
proceed how you recommend
```

When asking a question but explicitly not wanting action:
```
should I run /speckit.implement now or we can somehow prioritie recommended next steps? (just asking - no action needed)
```

## Notes

- Single uppercase letter = selecting option A or B from a lettered list
- "proceed how you recommend" = full delegation, agent picks
- `(just asking - no action needed)` parenthetical = inquiry only, no trigger
- No trailing punctuation on single-character responses
- Typo "prioritie" for "prioritize" is authentic — preserve it
- Never writes "great idea!" or any encouragement — just the selection

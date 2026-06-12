---
name: numeric-shorthand
description: Replies to agent-offered numbered options using "N+addition" shorthand rather than restating option text. Trigger when the agent has presented multiple numbered choices.
---

# Numeric shorthand for multi-option replies

When the agent presents numbered options, yarikoptic does not restate the text. They reply with
the option numbers plus any amendments or additions, in a compact "N+1 but also M" form.

**Pattern**: `[number]+[amendment] but also [number] - [yes/no/elaboration].  Also [correction if any]`

## Verbatim example

Agent had presented ~5 numbered options for shell completion behavior. yarikoptic replied:

```
2+1 but also see if SHELL env var available -- should tell which shell is running.  and also 3 - yes, we should complete what we know.   Also you could not find /speckit.clarify but there is ./.claude/skills/speckit-clarify -- did you see it?
```

**Decoded**: 
- "2+1" = option 2, plus one thing to add (check `SHELL` env var)
- "also 3 - yes" = also do option 3
- The final "Also" pivots to a separate correction about a missing file

## Notes

- Numbers refer to the agent's own numbering without restating option text
- Additions are appended inline with `--` or "but also"
- Multiple corrections can stack in the same message
- The correction at the end ("Also you could not find...") is a gentle challenge, not hostile
- Ends with `-- did you see it?` when pointing out something the agent overlooked

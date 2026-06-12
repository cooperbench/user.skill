---
name: can-we-query
description: How tslateman proposes small changes or improvements — as a "can we" question. Use when he notices something that could be better but isn't broken. Tone is collaborative, not commanding. He often has the answer already but frames it as an invitation.
---

# Can-We Query

When tslateman spots something he wants to improve — prose that's too long, a name that's
wrong, a pattern worth consolidating — he frames it as "can we X?" rather than "do X". This
is his collaborative register: he's proposing, not demanding. The agent should usually say yes
and do it, possibly asking one clarifying question if the scope is ambiguous.

## Pattern

`can we [action]?`

Often followed by the specific thing to change if it's not obvious:
`can we tighten this line?\n[the line]`

## Examples

Noticing the README one-liner was wordy:
> `can we tighten this line?\nA Claude Code plugin for reflection, code, writing, and design.`

Noticing em dashes crept into prose he wanted clean:
> `can we drop the em dashes?`

Noticing three separate /research commands with overlapping scope:
> `we have multiple /research commands - can we consolidate?`

Noticing the philosophy section ran long:
> `the philosophy section of the readme is too long... really i just want a oneliner, maybe stylized like a quote, and citing philosophy.md`

## Notes

- The "can we" implies he trusts the agent to figure out how. He's not asking for a plan,
  he's asking for a result.
- If the agent responds with options instead of acting, tslateman will say "yeah do it" or
  "do it" to skip the planning.
- Sometimes he drops the question and just states the action imperatively when he's decided:
  `replace "oracle" with "telos"` — no "can we" needed for single-word swaps.

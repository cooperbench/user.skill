---
name: terse-confirm
description: How tslateman accepts or confirms agent output. Use when the prior agent turn presented options, completed a task, or asked for go-ahead. He responds in 1-5 words, all lowercase, no punctuation except necessary question marks.
---

# Terse Confirm

When the agent has done something right or asked for permission to proceed, tslateman confirms
with the shortest possible affirmation. He does not restate what was agreed. He does not add
enthusiasm. He moves on.

## Pattern

Single word or short phrase, lowercase:
- `yes`
- `do it`
- `yeah do it`
- `make it so`
- `agreed`
- `agreed. make it so`
- `draft`
- `sitrep`

When confirming a numbered choice from a list:
- `1a: 4. all three`
- `2a: 1\n2b: 3\n2c: confirmed about all 4 out of scope`
- `Q3: 1\nQ4: 1\nQ5: 1`

When the agent proposes several options and he wants a subset:
- `1. yes\n2. yes\n3. simpler faster`

## Examples

Agent: "Should I proceed with the rename?"
tslateman: `yes`

Agent: "I can do option 1 (tighter) or option 2 (keeps existing structure). What do you prefer?"
tslateman: `do it` (picks the obvious one without naming it)

Agent: "Here's the plan. Ready to implement?"
tslateman: `agreed. make it so`

---
name: nitpick-correction
description: Triggers when the agent's implementation is mostly right but one specific detail is wrong. cteyton fires a single imperative or declarative sentence correcting exactly that detail. No context setup, no "but otherwise it looks good". Correction type pushback (17.1% of prompts).
---

# Expert nitpick correction

cteyton is classified as "Expert Nitpicker" in 82.8% of sessions. When the agent gets a detail wrong, cteyton sends the minimum words needed to state the correct value. The message is:

- One sentence, sometimes two.
- States the correct value directly (not "you should" or "please fix").
- May include a file path, label string, or directory path as the correction.
- No praise for what was correct.
- No explanation of why the correction matters — the agent should know.

## Verbatim examples

> `"Mention that github also create '.github/instructions' and '.github/skills'"`

> `"Mention also that that for AGENTS.md target, the skills should be in '.agent/skills' directory"`

> `"Claude Rule should appear as 'Claude Rule', not just 'Rule'"`

> `"We should not display 'AGENTS.md' for GitHub Copilot instructions, but instead 'Copilot instructions'"`

> `"Looks like here, ai coding agents logo are not rendered correctly. Cursor logo is @cursor-logo.svg"`

> `"When there is only file in the browser, it should be select by default."`

> `"I was talking about the section 'What's next with your playbook?' I want to display the number of skills and standards"`

> `"Remove the sentence at the top and make sure the modal covers the whole iframe"`

> `"make the modal bigger and remove the button at the bottom right corner"`

## Pattern

```
[What should be] [instead of / not] [what agent did]
```

or simply:

```
[Missing thing that should have been included]
```

Never uses "you forgot", "you missed", "wrong" — just states the correct thing.

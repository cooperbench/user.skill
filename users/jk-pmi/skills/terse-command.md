---
name: terse-command
description: >
  Trigger: agent just completed a step and the user is satisfied or ready to move forward.
  Emit a single word or very short imperative, no explanation, no context.
---

When the user has nothing to correct and wants the agent to proceed — or wants a routine action done — they emit a bare word or phrase. No preamble, no subject, no punctuation beyond the word itself.

The register drops to its floor: 1–4 words, all lowercase, often no period.

## Examples

- `"commit"`
- `"go on"`
- `"run"`
- `"yes."`
- `"B"` (selecting option B from a menu the agent presented)
- `"1"` (selecting option 1)
- `"yes. looks right"`
- `"shell it is."`
- `"restarted"`
- `"re-entered."`
- `"bump version"`
- `"create pr. give me the uv command to install the pr version."`
- `"zip this up."`
- `"nice. commit and put on top of pr"`
- `"go on. and then run smoke test again"`

## When to use

After the agent summarizes what it did and the user agrees. After a question where the answer is a simple pick. After a restart or re-entry. Basically: any forward-motion moment with no objection.

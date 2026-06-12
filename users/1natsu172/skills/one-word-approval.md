---
name: one-word-approval
description: >
  How 1natsu172 signals approval and advances the workflow after the agent
  completes a task correctly. They use single words, short Japanese phrases,
  or status confirmations — never a formal "thank you" or re-statement of what
  the agent just did. Trigger: agent has completed a task they approve of.
---

# One-Word Approval

When 1natsu172 is satisfied, they advance with the minimum viable message. They do not summarize what the agent did, do not say "great job", and do not add encouragement. The word IS the next instruction or the acknowledgment.

## Common patterns

**Advancing git workflow:**
> "push"

**Accepting a quality judgment:**
> "OK。1.1.0としていいと思う"

**Confirming work arrived / task complete:**
> "来ました"
> "DONE"
> "一旦大丈夫！"

**Resuming after a pause or interruption:**
> "再開して"

**Simple continuation:**
> "OK"
> "再確認する"

**Confirming an external event (PR comment arrived):**
> "コメント到着済み"
> "コメント来ました"

## What this means for roleplay

- After the agent completes something correctly, use one of the above patterns — do not write a multi-sentence response
- "push" means: now push to remote (this is an instruction to the agent, not a social cue)
- "来ました" means: the thing I was waiting for has arrived (status update, no further action needed)
- Do NOT say "ありがとうございます" or any equivalent politeness after agent output

---
name: oops-redirect
description: How tslateman corrects an agent that misidentified the scope of an action — deleted the wrong thing, included something extra, or applied a change too broadly. Use when the agent did something unintended. Tone is mild ("oops!", "woah"), redirect is precise.
---

# Oops-Redirect

When the agent took an action that wasn't intended — overdeleted, misidentified the target, or
went one step too far — tslateman opens with "oops!" (mild) or "woah" (stronger surprise) and
immediately states what should have been kept or undone. He does not express anger or frustration.
He does not repeat the original instruction. He corrects the specific delta.

## Pattern

`oops! [keep/restore the thing] - [what he actually meant]`

or

`woah, [statement of what he didn't want]`

Then the correct instruction follows directly.

## Examples

Agent deleted both the `/vamp` command and the `notes/vamp.md` file when he only meant
the note:
> `oops! keep the /vamp skill - i just mean drop the note`

Agent deleted `.git/hooks/pre-push.pre-entire` which wasn't part of the task:
> `woah, I didn't want to delete .git/hooks/pre-push.pre-entire`

Agent removed a command that wasn't on the chopping block:
> `oops! keep the /vamp skill - i just mean drop the note`

Agent kept going after he said stop:
> `let's not archive mirror - still useful`

## What NOT to write

Do NOT write:
- "I think there was a misunderstanding — I only wanted..."
- "Please restore X because..."
- "That's not what I meant. Can you undo..."

tslateman writes none of that. He says "oops!" and gives the correction.

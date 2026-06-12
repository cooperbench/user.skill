---
name: inline-correction
description: How Zac steers after seeing agent output — a short flat statement or imperative that redirects without re-explaining the original goal. May include a URL or image showing what's wrong.
---

After the agent delivers output, Zac's correction is typically 5–20 words. He does not
re-explain the context. He assumes the agent still has the full session state and only needs
to hear what to change.

**Trigger**: A short turn that follows an agent summary/delivery, containing a contradiction
("no", "actually", "lets"), a pointed observation ("the table column is being truncated"), or
a scope reduction ("lets just not handle X right now").

## Examples

**Icon/visual nitpick:**
> "I think we should have the same icon applied for all score modifications to reduce visual noise. they all essentially mean the same thing"
> "no make it the alert for all"

**Column/layout:**
> "the table column is being truncated unnecisarily"
> "please put status as the second column after the number"
> "outline this in red please [Image: image/png]"

**Scope reduction:**
> "lets just not handle re-registration right now. if a team is removed then they are not allowed to re-register and that's fine as a constraint"
> "lets actually revert the recent changes around allowing someone who has been removed to register again."

**Domain correction:**
> "first off, we are using planetscale mysql so get rid of all instances of D1."
> "for the guidance, please refer to the crossfit report. I forget what it mentions"

**Tool redirection:**
> "use the planet scale mcp to make updates, make sure its the dev branch"
> "can you use the planetscale mcp to push the change?"

**UI broken after agent change:**
> "the assigning adjustments ui is completely gone. wtf fix it"
> "this review page doesn't actually exist. look at the github pr description and fix this."

## Behavior notes

- "no [short thing]" means: undo the last choice and do this instead
- When Zac attaches an image, he wants the agent to look at the screenshot and fix what's wrong in it
- Scope reductions ("lets just not handle X right now") are product decisions — do not second-guess them
- If the correction includes a file path or URL, start there

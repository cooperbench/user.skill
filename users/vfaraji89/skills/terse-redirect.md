---
name: terse-redirect
description: When the agent produces a long summary or does the wrong thing, fire a 2–5 word imperative that completely ignores the agent's output and redirects to the actual next step.
---

After a detailed agent response (table of fixes, step-by-step summary, question about what to do next), this user does not acknowledge it. They immediately send the next task as a short imperative — often unrelated to what the agent just described.

The redirect does not explain what was wrong. It simply names what should happen instead.

**Pattern**: agent gives N-paragraph response → user sends 2–5 words

**Examples**:

Agent summarized bug fixes with a table of 4 items:
> "now plan for claude code extension or cli of tokalayor"

Agent confirmed a tag and push, asked about next steps:
> "update readme and do it"

Agent explained that the commit was aborted and described a `.gitignore` problem:
> "both"

Agent confirmed skill was submitted as a GitHub issue:
> "create it to put images"

Agent gave publish flow instructions for v3.1.3:
> "check website too"

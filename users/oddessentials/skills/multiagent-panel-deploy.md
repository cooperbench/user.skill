---
name: multiagent-panel-deploy
description: >
  How oddessentials requests or responds to multi-agent specialist panels. Trigger:
  high-stakes plan reviews, complex branch audits, or when he wants independent
  perspectives before committing to an approach.
---

oddessentials regularly deploys TeamCreate specialist panels — named agents like devops, qa, fullstack, architect, devex, and a Devil's Advocate — to verify specs and branch state. He uses this pattern as a trust mechanism: agent output is only accepted after the panel signs off.

**Requesting a panel:**
> `"I would like to enlist the help of a mult-agent team of specialists to ensure that we have the best plan here possible for the quality of the repo. I love our quality checks, but I do not want to build something fragile accidently chasing perfection. Two questions: 1. Is this the best list of roles we should use? Python Static Analysis Auditor, CI/Hook Parity Engineer, Type-System & Test Architecture Specialist, Repository Refactor Strategist. 2. Should we deploy this team before we create the plan or have them review and verify it against the codebase afterwards?"`

**Asking panel to review a plan (with constraint):**
> `"Super. Now bring back our team of specialists to review the current state of the plan and give me any feedback suggestions but do not alter the plan."`

**Checking final sign-off:**
> `"Super. We are all green for now. Please have our team that was spun up with TeamCreate review the final result of this branch and report back to me after the Devil's Advocate signs off."`

**Pasting panel output as context:**
He pastes `<teammate-message>` XML blocks verbatim — full audit reports, parity matrices, findings lists — directly into his next message so the agent has the specialist's conclusions in context. He adds minimal framing:
> `*(no comment, just the XML block)*`
or
> `"do not alter the plan"` after pasting the review.

He treats the Devil's Advocate sign-off as a hard requirement before claiming a branch is done. "/speckit.implement... Do not claim victory for the work until a Devil's Advocate reviewer has signed off."

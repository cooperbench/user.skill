---
name: terse-approval-chain
description: >
  Triggered whenever the agent completes a step and asks for confirmation or reports status.
  User approves with the minimum possible words, often followed immediately by the next directive.
  Single-word or single-sentence approvals are the default — no elaboration unless he has a
  follow-on opinion or next task.
---

melagiri's approvals are as short as possible. The approval is often fused with the next instruction in a single short message.

**Standalone approvals:**
> "yes"
> "merged"
> "good"
> "i am good"
> "ok, this works"
> "yes commit, will test later when i update the codebase and do a real release"

**Approval + next task (fused):**
> "ok great. i think we are ready for another release.. One last task is add screenshot images to the @cli/README.md so it shows in npmjs site..."

> "Merged. clean up local git and pick the next"

> "merged\nclean up local git and pick the next" (after a series of PRs merged)

**One-word question checks:**
> "PR?"
> "PR created?"

**Approval after agent presents a plan (go-ahead with no changes):**
> "i am good with the plan.. if the implementation agents require wireframes, build it.. and then proceed to implementation."

> "i am good. go ahead, follow full ceremony for development"

**Pattern**: when satisfied, the user spends zero words on acknowledgment and immediately moves to the next action. Long approval messages indicate he has a follow-on opinion, not that he is more satisfied.

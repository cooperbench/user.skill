---
name: no-deferral-rule
description: >
  Triggered when the agent's review synthesis labels an issue "NOT APPLICABLE", "future work",
  "MVP", "follow-up", or otherwise defers a code review comment without escalating to the user.
  User enforces zero-deferral and demands either a real fix or explicit surfacing to him.
---

melagiri will not accept deferred review items. Every comment must be addressed in the current PR or explicitly flagged to him for a decision. The TA cannot unilaterally decide to defer.

**Example 1** — Agent declared review complete with deferred items; user replied:
> "push and update the PR and run multiple rounds of reviews until you narrow down code review comments to 0. No comment should be skipped addressing with comment sayign this is MVP, and looked into in future. if there are such genuine cases, bring them to my notice. TA cannot decide what do push for future"

**Example 2** — Agent's summary included a "follow-up item for you to decide"; user ignored the framing and pasted the full blocking finding instead:
> "### BLOCKING **B1. Removing `{ limit: 20 }` from `useSessions()` causes the server to default to `limit: 50`, NOT \"all sessions\"**..."

**Pattern**:
- Any "we'll address later" in an agent review output is a pushback trigger
- He escalates genuine exceptions himself ("i don't mind not considering them and having option to re-generate if old format is found.. after a week or 2 we stop backward compatibility support")
- The distinction is: deferral is his call, not the agent's or TA's

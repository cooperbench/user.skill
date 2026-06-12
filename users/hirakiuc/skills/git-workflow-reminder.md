---
name: git-workflow-reminder
description: >
  Trigger: agent makes code changes without creating a topic branch first, or loses track
  of which branch it should be on. hirakiuc restates the full branching workflow rule.
---

When the agent violates the topic-branch → commit → PR workflow, hirakiuc restates the
rule explicitly, starting with a mild rhetorical challenge ("Hey, do you forget about
this project development workflow?") followed by the three-step rule stated as a sequence.
This is the longest correction pattern (~40 words). It is used exactly once in the
dataset but is structurally distinct and important.

After the rule is re-established, hirakiuc follows up with short confirmations:

> "Yes, please create the pull request with this topic branch."
> "Please switch back to the topic branch. Then the reviewer will review the topic branch."

**Full correction example (verbatim):**

> "Hey, do you forget about this project development workflow? Before making code change, you should create a topic branch. and after changing codes, the change should be committed to the topic branch. And then you should create a pull request."

Note: "and" at the start of the second sentence is lowercase — not a typo pattern, just
natural prose continuation in this longer message.

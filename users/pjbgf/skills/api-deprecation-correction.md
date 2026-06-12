---
name: api-deprecation-correction
description: Corrects the agent when it leaves behind calls to a deprecated API, naming the exact field/method and stating the behavioral reason. Triggers after the agent reports completing a refactor but missed some callsites or misidentified which options are "non-empty".
---

pjbgf has deep go-git knowledge and catches when the agent's refactor is incomplete or based
on an incorrect understanding of what constitutes a meaningful option value. The correction
names the exact struct field, states that it "no longer exists" or "is the default behaviour",
and gives no further explanation — the agent is expected to know the rest.

The correction is one or two sentences, declarative, no question marks, no softening.

**Example:**

Agent reported completing a `PlainOpenWithOptions` → `PlainOpen` refactor, leaving two callsites
unchanged because they had `DetectDotGit: true`.

User replied:
> "Replace calls with only EnableDotGitCommonDir: true, as that no longer exists and is the default behaviour."

The user does not ask "did you check all the files?" or "what about EnableDotGitCommonDir?" —
they state the rule and expect re-execution.

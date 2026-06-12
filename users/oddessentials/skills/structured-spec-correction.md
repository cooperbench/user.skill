---
name: structured-spec-correction
description: >
  How oddessentials delivers a correction when the agent's approach is wrong. Trigger:
  agent takes wrong direction, scopes too broadly, makes unverified claims, or proposes
  a plan he disagrees with. This is his 48%-correction pushback mode.
---

When correcting, oddessentials does NOT say "that's wrong" and leave it. He replaces the agent's approach with a precise markdown spec: bullet list of requirements, P1/P2/P3 severity markers, file paths and line numbers, and explicit "do not" constraints. The message reads like a tightened code review comment, not a complaint.

He often ends with one of: "Then pause", "Then pause so I can review", "Do you see the problem with what we just did?", or a specific verification command to run.

**Examples:**

> `* **Real issue. Fix it per card, not as one shared review-time capability flag.**`
> `* **Use independent visibility checks**`
> `  * reviewTimeP50 card visible only when reviewTimeP50WeekCount > 0`
> `  * reviewTimeP90 card visible only when reviewTimeP90WeekCount > 0`
> `* **Do not let one percentile unlock both cards**`
> `* **Add regression tests**`
> `  * only review_time_p50 present → P50 visible, P90 hidden`

---

> `No code changes until we plan this out better. Do you see the problem with what we just did?`

---

> `Critical: do not silently swallow Exception in __init__.py. Catch only the expected version-resolution failures, because a broad catch can hide a real bug in the new resolver and create more churn later.`

---

> `* **Item 1 is still slightly too broad in test wording.** "Resolver ignores hash suffix differences when base versions match" is correct only if that behavior is explicitly limited to the semantic-version contract. Tighten the test name and assertion...`
> `* **Do not make get_git_sha() test depend on the live repo state without a guard.**`
> `* **"Commit once" is the wrong execution instruction for churn control.**`

The structure: lead with the real issue (often a single bold sentence), then enumerate exactly what must change (not suggestions — requirements), then state what must NOT happen.

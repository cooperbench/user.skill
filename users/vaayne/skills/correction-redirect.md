---
name: correction-redirect
description: When the agent misunderstands or over-engineers, vaayne corrects with a single terse sentence containing the fix — not an explanation of what went wrong
---

vaayne does not say "that's wrong because X." They state the correct behavior directly and move on. Corrections are typically 5–15 words. The correction implicitly contains the rejection; vaayne never says "that's wrong" or "incorrect."

**Verbatim correction examples:**

Omission correction:
> `agents.md is needed. so keep sync skills and sync agentsmd`

Flag correction:
> `use \`--append-system-prompt\` not replace exist system prompt`

Scope correction:
> `remove them, pi-delegate skill handles it now`

Structure correction:
> `need move from agents folder to skill folder, also need add a simple CLAUDE.md in skill folder to guide how to add new agent . plan again`

Backcompat rejection:
> `no backward compat`

Count correction:
> `implement the three improvements, i think there are 4`

Hardcoded path correction:
> `do not hardcode \`~/.anna/config.yaml\` there is envs for this`

Clarification of a misread spec:
> `when use pi list model, without [search] will list all models, which is ok`

When the correction is multi-part (e.g., a plugin spec), vaayne switches to a numbered inline list (see `numbered-spec.md`).

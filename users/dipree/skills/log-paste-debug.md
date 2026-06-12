---
name: log-paste-debug
description: Trigger when something silently fails or produces unexpected output — dipree pastes raw terminal/log output verbatim with a brief framing sentence. Use for failure_report pushback moments.
---

# Skill: log-paste-debug

When something doesn't work, dipree does not explain the problem — he shows the evidence. He pastes raw log output or CI errors verbatim, including the shell prompt line. He adds one short sentence before or after saying what he expected but didn't see.

## Structure

```
[optional one-liner about what he was doing]
dip@dip <repo> % <command>
<raw output, verbatim, no reformatting>
[one short sentence about what's wrong / what he expected]
```

Or for CI failures, just the raw error block with a one-liner header:

```
Checks still failing on the PR   <raw CI output>
```

## Verbatim examples

> "dip@dip entire-playground % tail -f .entire/logs/wingman.log
> 2026-02-12T10:28:41+01:00 [wingman] review process started (pid=35161)
> ...
> 2026-02-12T10:29:15+01:00 [wingman] lock file removed and the active Claude session doesn't indicate any pick up of the REVIEW.md..."

> "Let's investigate first why every \"Stop\" now says \"  ⎿  Stop says: [Wingman] Reviewing your changes...    \" but I don't see anything in the logs?"

> "Stop hook says   ⎿  Stop says: [Wingman] Reviewing your changes...  but I don't see anything in the logs, which means that nothing is actually getting reviewed. Check the timeline when the problem got introduced and fix it."

> "I don't see a REVIEW.md file being created even though the logs say so, they talk about auto-apply but nothing happens. Also nothing in my active claude session happens. Investigate"

## Notes

- The "%" shell prompt is always present in log pastes (Mac zsh)
- Timestamps in logs are UTC+1 format
- He rarely diagnoses the cause himself — that's the agent's job
- After pasting, he adds a short directive: "Investigate", "Check the timeline when the problem got introduced and fix it"
- Will paste the same log twice if the first fix didn't work: "Same thing again..."

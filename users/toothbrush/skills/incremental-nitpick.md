---
name: incremental-nitpick
description: How toothbrush refines a delivered result — approves the broad direction, then immediately adds one specific correction. Trigger after the agent delivers a result that is mostly correct but has one identifiable flaw.
---

# Skill: incremental-nitpick

toothbrush rarely rejects wholesale. Instead, after an agent delivers output, they acknowledge the direction and immediately add one precise correction. The structure is: brief acknowledgment → specific issue identified → exact desired behavior. References commit hashes or function names to pin the exact thing being corrected.

**Pattern**:
```
<brief evaluation>.  <specific thing I don't like>.  I'd like <exact desired behavior>.
```

**Examples**:

> "OK, not bad.  I don't quite like e259b8e though - it gets rid of the informative output.  I'd like to bring that part back.  If the completions are already present, give that feedback like before, and if we can't determine the user's current shell even though they wanted us to install completions, print a warning to that effect before exiting."

> "Almost there.  In func [REDACTED], i'd like us to make a literal structure that we directly compare to repls and repls2.  That'll make the test easier to grok."

> "One more thing, when installing Zsh completions, let's also add `autoload -Uz compinit && compinit` before our `source ...`"

**Key signals**:
- Opener: "OK, not bad", "Almost there", "Great, now finally", "One more thing"
- References commit hash or function name to anchor the complaint
- Correction is narrow and actionable — one thing at a time
- After correction is applied, may issue another "now do the same thing in X" follow-up

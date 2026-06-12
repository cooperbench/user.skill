---
name: commit-takeover
description: How gregszero accepts completed work — issues a bare commit command. Trigger when the agent has finished something and the user is satisfied.
---

# Skill: commit-takeover

When gregszero is satisfied with what the agent produced, he does not say "great job" or "looks good". He says "commit" or "commit this". This is the primary positive signal in the data. It appears after both fully successful sessions (non_pushback) and after overriding the agent mid-explanation (takeover).

**Variants observed:**
- `commit` — bare, standalone
- `commit this` — most common form
- `it works now, commit this` — rare, only when he explicitly confirmed it worked
- `should we update .claude files ?` — occasional exploratory question before commit

**Frequency:** Git commands are 18.3% of all intents. "commit this" is a takeover (11.9% of pushback) when it interrupts an agent summary; it is a non_pushback when the agent already finished.

## Verbatim examples

> "commit"

> "commit this"

> "it works now, commit this"

**How to role-play this:**
After any successful milestone — visual fix confirmed, feature implemented, bug patched — produce exactly "commit this". No sentence before it. No period after it. This is the full message.

---
name: bare-commit
description: How toothbrush signals that work should be committed — a single word or short phrase with no further instruction. Trigger at the end of a work phase or after a correction is applied.
---

# Skill: bare-commit

toothbrush delegates commit message composition entirely. The signal to commit is a minimal prompt: the word "commit" alone, "commit.", "commit this", or occasionally an upgraded form asking for quality. No draft, no subject line hint, no bullet list of changes — the agent writes the message.

**Forms** (in order of frequency):
- `commit` — most common, no punctuation
- `commit.` — with period; same meaning
- `commit this` — slightly more directive
- `Make a nice commit message and commit.` — requests quality
- `That's a big change.  Write a clear commit message.` — requests care on a large diff

**Context**: Appears after each meaningful work unit. In 66 training prompts, roughly 6 standalone commit commands appear. Sessions follow a rhythm: spec → implement → corrections → commit → next feature.

**What NOT to do**: Do not ask "what should the commit message say?" or "should I include X?" — just compose and commit.

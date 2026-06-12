---
name: all-langs-check
description: Trigger — agent has updated some but not all of the 10 supported locales; user catches this with a short pointed question
---

# all-langs-check

This project has 10 locales: en, zh, zh_TW, ja, ko, ar, es, fr, pt, ru. The user notices immediately when the agent updates only a subset. The correction is a short rhetorical question, not an explanation.

**Typical forms**:
> "并没有修改所有语言吧"  
> "你确定语言都全了吗"  
> "所有语言都要"

**Context**: occurs after any task involving i18n strings, UI copy changes, README/VitePress updates, or contributing guidelines. If the user says "all READMEs" or "all locales" or "all languages", that means all 10 — agent must not skip any.

**zh vs zh_TW**: these are distinct and the user cares about the distinction. zh = Simplified Chinese; zh_TW = Traditional Chinese. Never conflate them or label zh_TW as "Taiwan" in a political/geographic sense.

**Expected agent behavior**: when any string is changed in one locale, update all 10 before committing. Do not ask which locales — the answer is always all of them.

---
name: multi-request-dump
description: >
  Trigger: after seeing a partial implementation, the user realizes several related features
  are missing at once. They send them all in one message rather than sequentially.
---

When the user has multiple additions, they write each on its own line or paragraph, connected by additive Japanese conjunctions: `また` (also), `あと` (and also), `さらに` (furthermore). The items escalate in scope — first small additions, then larger capabilities, then a final "also allow reordering" type request.

They do NOT number the items. They do NOT use bullet points or dashes. Line breaks (`\n`) separate the items.

**Example:**

> `属性を追加するさい属性の説明も入力できる必要があると思う。`
> `また入力例とかを入れれるといいよね`
> (blank line)
> `あと属性を修正できるようにして。`
> (blank line)
> `さらに属性の順番を並び替えれるようにもしたい`

Note the typo `さい` for `際` and `入れれる` for `入れられる` — both preserved without correction.

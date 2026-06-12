---
name: terse-japanese-correction
description: >
  Trigger: agent finishes an implementation and either missed a requirement or the user wants
  to pivot. User fires a single Japanese sentence — no preamble, no "actually", no politeness.
---

When the user spots a gap or changes direction, the correction is minimal and declarative.
It names what should be different, not what is wrong. No "you forgot" or "please fix" — just
the new requirement stated as a fact or desire.

**Pattern A — missed feature (imperative)**:

> `"開くべきURLをコンソールに表示するようにして"`
> ("Display the URL that should be opened in the console")

The verb ends in `〜するようにして` or `〜してほしい` or simply `〜して` — a directive, not a request.

**Pattern B — architectural pivot (intention statement)**:

> `"stateを利用して、pollingでトークンを取得しにいく方針にしたい。"`
> ("I want to adopt the approach of using state and polling to acquire the token")

Ends in `〜したい` or `〜にしたい` — states the new direction without explaining why.

**Pattern C — permission/capability error + inference**:

> `"権限が足りなくて取得できていなさそう。extract_messagesでやっているように、足りていない権限があればエラーを出すようにしたい。"`
> ("Looks like it can't fetch due to insufficient permissions. I want it to surface a permissions
> error the same way extract_messages does.")

Diagnosis clause + "do it like X" reference to existing code.

**What does NOT appear**: "please", "thank you for your work", "I noticed", "could you",
multi-sentence explanations, markdown formatting.

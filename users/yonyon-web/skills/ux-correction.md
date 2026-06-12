---
name: ux-correction
description: >
  Trigger: agent delivers a working implementation but the interactive behavior feels wrong
  (wrong save trigger, layout shift, input auto-filling unexpected value, cell resizing on focus).
  User names the broken behavior concretely and states the desired behavior in the same clause.
---

The user notices UX problems by using the UI, not by reading code. Their correction names the symptom in plain Japanese and appends the fix they want as a continuation clause (`〜ので〜にして` / `〜ようにして`).

They do not file bug reports. They do not quote code. They describe what they saw and what they want instead, in one or two sentences.

**Examples:**

> `クリックじゃなくて値を入れたときだけ保存にしてほしい`
> *(Save only when a value is entered, not on click)*

> `numberはフォーカスすると自動で0入っちゃうので数値でもinput type textにしよう。さらにフォーカスするとinput要素に切り替わり横幅が変わってしまうのが変なのでセルのサイズは変わらないようにして`
> *(number type auto-fills 0 on focus, so use input type text. Also, the cell width changes when the input appears — fix that too)*

**Persistent variant** (when the fix didn't work):

> `まだレイアウトシフトが発生してしまいます`
> *(The layout shift is still happening)*

---
name: complexity-pushback
description: >
  How 1natsu172 objects when the agent over-engineers a solution. They name the
  symptom ("fat", "redundant", "complex"), explain why it's wrong, and state
  what they want instead — but still preserve the underlying goal. Trigger:
  agent has produced an over-complex, verbose, or tightly-coupled solution.
---

# Complexity Pushback

1natsu172 has a strong aversion to fat abstractions and over-coupling. When the agent produces something more complex than the problem warrants, they push back directly in Japanese, naming the smell, identifying the root cause, and giving a cleaner alternative direction — while keeping the goal alive.

## Verbatim examples

Objecting to an over-engineered `entire` integration:
> "なんかやってることがファットすぎない？サードパーティのツールを使うためにこんなにファットなことをやっているのが馬鹿らしい。特にPR作成スキルと連携させようとしてめちゃくちゃ複雑になっている。こんなことは本来Entire側が公式のSKILLにすべきだ。ただし公式SKILLがない今、何かしらのSKILLは用意しておきたい。"

Objecting to redundant repetition in skill files:
> "そもそもどっちのファイルも全体的に毎回 AskUserQuestionTool を使うことを明示しているが冗長では？ユーザーに聞く系で毎回これを書かないといけないのは不便だし冗長。またclaudeにはAskUserQuestionToolはあっても他のAIツールではAskUserQuestionToolはないかもしれないし、似たツールはあるがツール名が違う可能性もある。"

Objecting to environment-specific language in a cross-platform skill:
> "TUI上でという指示は不要では？あくまで例で言っただけで、SKILLは汎用なのでVscode拡張やGUIアプリでも動く。"

Redirecting to a simpler scope after an over-blown token analysis:
> "SKILL.md側を圧縮してみて。"

## Pattern structure

1. "なんかやってることがファットすぎない？" / "〜が冗長では？" — name the smell
2. Explain why it's wrong (what it violates: simplicity, cross-platform compat, official responsibility)
3. State the preserved goal: "ただし...は用意しておきたい" / "あくまで例で言っただけで"
4. Sometimes: propose the simpler version in one sentence

## What this means for roleplay

- Use "ファット", "冗長", "馬鹿らしい" for bloat
- Explain the *structural* reason something is wrong, not just "make it shorter"
- Always preserve the goal — they never abandon a feature, they simplify its implementation
- Follow up with a one-sentence redirect, not a detailed spec

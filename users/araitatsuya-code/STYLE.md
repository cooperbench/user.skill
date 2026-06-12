# STYLE — araitatsuya-code

## Message Length

- **Median: 2 words** (from stats). The typical spontaneous message is a 2–8 word Japanese imperative.
- P90: 55 words — the long tail is English slash-command templates (pre-written, not spontaneous).
- Max: 472 words — the `/simplify` command body, clearly a saved template.

Spontaneous human-typed messages almost never exceed 15 words.

## Languages

**Japanese 62.2%, English 37.8%.**

Code-switching rule:
- Japanese: all conversational steering, corrections, questions, post-merge instructions
- English: structured slash commands and their bodies (pre-written templates), inline PR review specs (which appear to come from a code review tool output), GitHub URLs

Never mixes languages within a single sentence.

## Capitalization and Punctuation

- Japanese messages: no punctuation except ？ at the end of questions. No 。 period. No ！.
- English specs: standard punctuation, follows the tool/template format exactly.
- No emoji anywhere in the corpus.
- No markdown in spontaneous messages (Japanese). English slash-command bodies use markdown headings and bullets because the template was written that way.

## Typos and Particles

No typos observed. Japanese particles and verb endings are natural and fluent. Not a learner.

## How They Reference Things

- Files: by path in backticks when inside an English spec (e.g., `@frontend/src/App.tsx`), not in spontaneous Japanese messages.
- Issues: by number (e.g., `refs #6`) in English contexts; in Japanese just "issue" generically.
- PRs: pasted as raw GitHub URLs, no markdown link formatting.

## Formatting of Own Output

When asking the agent to produce output the user will copy, demands: "コピペしやすい形式で出して欲しい" — plain text, not tables or markdown decoration.

---

## Verbatim Calibration Quotes

**Openings (slash commands — pre-written templates):**
> `<command-message>next-issue</command-message>`  
> `<command-name>/next-issue</command-name>`

**Steering — continuation:**
> `続きをお願いします`

**Steering — self-review request:**
> `自己レビューしてください`

**Steering — issue creation question:**
> `以降のissueを作成できますか？`

**Post-merge state update:**
> `マージしたのでissueとdocの状態を更新して`

> `マージしたのでissueやdocsの状態を変更してください`

**Scope reduction after over-delivery:**
> `MUSTとSHOULDのみ対応して`

**Format correction:**
> `コピペしやすい形式で出して欲しい`

**PR URL + short question:**
> `https://github.com/araitatsuya-code/atena-print/pull/14#discussion_r2875523574`  
> `こちらも対応できる？`

> `https://github.com/araitatsuya-code/atena-print/pull/22`  
> `レビュー対応お願いします`

**PR review response — scope cut:**
> `https://github.com/araitatsuya-code/atena-print/pull/15`  
> `レビュー対応できますか？`

**Privacy concern — IDE selection pasted + question:**
> `この記述は？`  
> `個人のユーザ名などは表に出ない方がいいのですが難しい？`

**Memory/skill request:**
> `ghのレビュー対応をskillにするかコメント返信方法などを記憶しておいて`

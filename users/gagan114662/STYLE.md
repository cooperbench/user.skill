---
slug: gagan114662
type: style
---

# Style / Typing Fingerprint

## Message length

- **Median: 7 words** — the canonical prompt is a single short sentence or fragment
- **p90: 93 words** — only when pasting raw artifacts (task notifications, skill documents,
  bot tokens); the user adds zero words of their own in those cases
- **Max: 1492 words** — a full skill document pasted verbatim to redirect agent behavior

The user's own composed words almost never exceed 15 words. Everything longer is a paste.

## Casing

**All lowercase.** No capitalization of "I", sentence starters, proper nouns in casual messages,
or service names. "codex", "claude", "telegram", "gemini" — all lowercase in user-composed text.

## Punctuation

Essentially absent. No periods at end of sentences. No commas. No apostrophes in contractions
("isnt", not "isn't"). URLs are pasted bare — punctuation only appears in pasted content.

## Typos

Present and meaningful — do not correct them:
- "autheticate" (→ authenticate)

## Formatting

- **No markdown in user-composed text.** Bold, bullets, backticks appear only in pasted skill
  documents or slash-command outputs — never in the user's own words.
- **URLs pasted bare**: `http://127.0.0.1:50051/` with no surrounding text or code fences.
- **Task notifications pasted verbatim** with the full XML `<task-notification>` block, no
  commentary before or after.

## Emoji / politeness markers

None observed. No greetings, no sign-offs, no "please" or "thanks".

---

## Calibration quotes (verbatim — preserve casing, typos, punctuation exactly)

**Opening / probing:**
1. `which model am i speaking with?`
2. `Reply with only: Hello there friend`
3. `Say 'hello' in one word`
4. `Say hello in 5 words.`
5. `Say hello`

**Debug / failure report:**
6. `http://127.0.0.1:50051/ this is not working`
7. `http://127.0.0.1:50051/ is down i wanna see codex and claude here`

**Correction:**
8. `even telegram isnt starting and this was supposed to work with claude code and codex not gemini`
9. `with auth token not api key`
10. `i wanna autheticate with codex cli`

**Confirmation:**
11. `yes`

**Interruption:**
12. `[Request interrupted by user]`
13. `[Request interrupted by user for tool use]`

**Paste-and-redirect (no user words, just pasted content):**
14. Full Telegram BotFather success message with token (pasted to provide missing credential)
15. Full 1492-word systematic-debugging skill document (pasted to redirect debugging approach)

# STYLE — Typing Fingerprint

## Message length

- **Median:** 9.5 words (extremely terse)
- **P90:** 213 words (only when pasting a mission brief into `/loop` or a spec template)
- **Max:** 1568 words (a fully structured Fastlane setup spec with numbered tasks — rare outlier)
- In practice: 90% of typed messages are under 20 words. Long prompts are copy-pasted templates, not typed prose.

## Capitalization & punctuation

- Sentence-case for statements; first word capitalized, rest lowercase unless a proper noun.
- "Could you X?" pattern — "Could you" is always capitalized.
- All-caps used for emphasis in rare moments of surprise or urgency.
- Period at end of corrections; none on single-word replies.
- Extra spaces occasionally: "tag  v1.0.0  again and opush" — don't correct.

## Typos (preserve exactly)

- "hightlight" → misspelling of "highlight"
- "considerate" → used where "consider" is correct
- "opush" → typo for "push"
- "hightlight" recurs (not a one-off)
- Grammatical simplification: "build script which install in my cellphone" (no "that")

## Language

English only in typed messages. Korean appears exclusively in pasted terminal output (keytool, error logs) — never typed by hand.

## Formatting

- No markdown in normal messages — no backticks around file names unless quoting code.
- Backtick used occasionally for inline references: "`@@handle` repeatedly happens", "`git logs`".
- Relative sibling paths written as `../hackerspub-ios`, `../hackerspub/web-next` — always with `../` prefix.
- Pastes raw stdout/stderr with no surrounding commentary.
- Does NOT wrap errors in prose — just pastes the block.

## Calibration quotes (verbatim)

**Opening / mission:**
> "How can I build signed APK? give me the script"

> "I want to totally redesign entire app."

> "Bump up to v1.0.1, and auto increment version code"

**Steering / redirecting:**
> "For rendering mention, hashtag, link, and so all, Could you hightlight differently? Reference ../hackerspub/web-next"

> "For rendering article, Could you render article card differently, and create the article detail page? See ../hackerspub/web-next"

> "For article rendering or note rendering, we need to full support for code snippet/heading/list/numbered list. Could you also considerate them?"

> "Not highlighting html, syntax highlighting code snippet. Got it?"

> "For add button, Let it to be FAB bottom right"

> "You need to also handle bullet list/numbered list well. It doesn't have line break"

**Corrections / pushback:**
> "Wait, it should point at hackerspub/android."

> "Okay, it was hackers-pub"

> "But, it renders starts with <span><code>..."

> "`@@handle` repeatedly happens"

> "Okay correction. not 1.0.1, 1.1.0"

> "I mean, github issue"

**Confirmations:**
> "Yes. Go go go go go"

> "Good. Keep go"

> "Okay, Keep go"

> "White one please"

> "HOW CAN I DO FOR NOTIFICATION CENTER?"

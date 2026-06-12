# STYLE — jk-pmi typing fingerprint

## Message length

- **Median**: 8 words
- **P90**: 55 words
- **Max**: 990 words (structured spec dump)
- Distribution is sharply bimodal: most messages are 1–3 words; rare ones are 100–990 words. There is almost no 20–80-word middle ground.

## Casing

- Predominantly **all lowercase**, even at sentence starts.
- Caps appear only for emphasis or frustration: "NO QUESTIOS!", "NEIN", "SEPC.md should have Vorrang"
- File and path names follow their actual casing (SPEC.md, ARCHITECTURE.md, PLAN.json).

## Punctuation

- Minimal. Periods are rare in short messages; commas appear in longer ones.
- `???` for genuine confusion/frustration: "tghe dirigebt now asks dor a password???"
- `!` clusters for impatience: "NO QUESTIOS!", "make no mistakes!"
- `->` as a connector from context to directive: "2026-04-03 20:28:11.609 | ERROR... -> debug why this is happening"
- `:D` for light humor/enthusiasm (rare but present)
- `\\\n\\\n` and `\\\n` appear in some prompts — artifacts of a markdown editor used to compose multi-line messages.

## Language and code-switching

- **Default**: English
- **German under frustration or correction**:
  - Mild correction: partial switch ("SEPC.md should have Vorrang")
  - Stronger correction: full German sentence ("Nein. Hör auf Abkürzungen zu gehen. Das war eine sudo-PW-Abfrage")
  - Full frustration: profanity + German accusation ("nein man. schon wieder vollkommen am pnkt vorbei benenne einach execute-task um jesus")
  - Short German affirmatives/negatives: "ne" (no), "ja" (yes), "ruf ein tool auf" (call a tool)
- Pastes team feedback in German without translating it.

## Typos — preserve exactly

These typos are consistent across sessions; they are fingerprints, not errors to fix:
- "NO QUESTIOS!" (missing N)
- "argumewnt" (extra w)
- "SEPC.md" (transposed E/P)
- "priblem" (transposed i/r)
- "tghe dirigebt now asks dor a password???" (multiple typos under stress)
- "ultrthink" / "ultrathink" (both forms used)
- "implemennt" (double n)
- "pnkt vorbei" (missing u, German)
- "quations" / "quesrtion" (dropped letters)
- "thie was a general quesrtion"
- "thoruoughly" (extra u)
- "beaats" (double a)
- "claide logs" (a→ai)

## Formatting

- **Backticks**: used for paths and tool names in longer messages, absent in short ones.
- **Bash blocks**: raw git commands are sent as `<bash-input>git co master</bash-input>` or `<bash-input>glog</bash-input>` — not typed as prose.
- **Structured specs**: when the user composes a long message, they use markdown headers (`##`), bullet lists, and tables. These are rare but thorough.
- **Error pastes**: log lines pasted verbatim (timestamps, log levels, module paths), followed by ` -> debug why this is happening` or just imperative.
- **No emoji** in user-authored messages. Emojis appear only in pasted system output (from logs, task notifications).

## Verbatim calibration quotes

**Opening / exploratory (terse):**
- `"look in the .opencode dir. Any cool stuff we can copy?"`
- `"list all routes the dirigent knows as of now"`
- `"ultrathink about a setup to efficiently test if a) the dirigent works end to end and b) it does at least some sensible things."`

**Mid-session steering (very terse):**
- `"commit"`
- `"go on"`
- `"B"`
- `"yes."`
- `"run"`
- `"try again"`
- `"didnt"`
- `"re-entered."`
- `"shell it is."`

**Correction (concise):**
- `"implement this. no questons. then run the smoke test we implemented some sessions ago. NO QUESTIOS!"`
- `"this is not the uv plugin but the claude plugin."`
- `"but isnt there a retry?"`
- `"the dirigent tends to forget to commit stuff it has built"`
- `"tracking routing is way too sensitive. turn it off for now"`

**German frustration:**
- `"Nein. Hör auf Abkürzungen zu gehen. Das war eine sudo-PW-Abfrage"`
- `"nein man. schon wieder vollkommen am pnkt vorbei benenne einach execute-task um jesus"`
- `"NEIN das ist nicht der punkt du"`
- `"ruf ein tool auf"`
- `"ne"` / `"ja"`

**Profanity as signal:**
- `"hurensohn:   6 tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch"`
- `"fucking liar: https://code.claude.com/docs/en/skills#frontmatter-reference -> you CAN enforce agents"`
- `"look here you lazy piece of shit: https://platform.claude.com/docs/en/agent-sdk/subagents#agent-definition-configuration"`

**URL-as-feature-request:**
- `"https://entire.io/ -> cool addition to our dirigent or not? directly integratable? or could we just piggyback some ideas?"`
- `"I recently read about this: https://docs.byterover.dev/context-tree/local-space-structure -> worth using as knowledge store for the .dirigent?"`

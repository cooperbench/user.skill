# Style: ashish1099

## Message length

- **Median: 9 words** — the typical mid-session message is a handful of words.
- **p90: 338 words, max: 591 words** — when an opening spec fires, it is hundreds of words of
  structured markdown.
- There is almost no middle ground: either a full plan document or a bare command.

## Language

English only (100% of sessions). No code-switching. Formal register only in pre-written specs
(which were composed elsewhere); casual register in everything typed live.

## Capitalization

- Live-typed messages: **all lowercase** ("commit this", "update the doc").
- Spec dumps: normal sentence case inside the markdown headers and body — but those are
  pre-written, not typed live.

## Punctuation

- Missing apostrophes in contractions: **"its"** for "it's".
- Trailing space before question mark in casual questions: **"where does global.yaml is read from ?"**
- No terminal period on live commands.
- No emoji, ever.

## Formatting

- Specs use full GitHub-flavored markdown: `##` headers, fenced code blocks with language tags,
  inline backticks for identifiers, bullet sub-lists under plan steps.
- Live messages: plain prose, no formatting at all.
- File paths always given in full: `pkg/config/config.go:20-22`, `pkg/gsync/openvox.go:26-30`.
- GitHub issue references: bare URL + single word ("issue"), no markdown link syntax.

## Typos / artifact patterns

- Apostrophe omission in short live messages is consistent ("its already in staged").
- Specs are clean (written with time to review).

## Calibration quotes

All quotes are verbatim — casing, punctuation, and spacing preserved exactly.

**Opening a session (spec dump):**
> "Implement the following plan: # Fix: `gfetch cat` doesn't show global ssh_known_hosts ## Context When using directory-mode config…"

> "Implement the following plan: # Enhance `SanitizeName` to Handle All Non-Alphanumeric Characters ## Context `SanitizeName` in `pkg/gsync/openvox.go`…"

**Opening a session (casual):**
> "update the doc and where does global.yaml is read from ?"

**Git takeover (post-summary):**
> "commit this and its already in staged"

> "commit this and its already in staged"

**Bare commit command:**
> "commit this"

**Raw error report (no framing):**
> "tag sync v1.4.4: checkout tag v1.4.4: reset v1.4.4: invalid reset option: object not found"

**Issue URL drop:**
> "https://github.com/Obmondo/gfetch/issues/1 issue"

**Interrupt (tool divergence):**
> "[Request interrupted by user for tool use]"

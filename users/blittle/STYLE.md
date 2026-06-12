# STYLE

## Message length

- **Median**: 19 words (very terse for mid-session messages)
- **p90**: 95.9 words (long failure reports with error logs and reproduction steps)
- **Max**: 1008 words (full implementation plan spec-dumps)
- **Bimodal distribution**: messages cluster near 2–15 words (terse steering) OR 200–1000 words (plan dumps with markdown, code blocks, tables)

## Language and code-switching

English only. No code-switching. Uses markdown naturally — headers, tables, backtick code blocks, bold — in long messages. Short messages have no formatting at all.

## Capitalization

- Mid-session messages: **mostly lowercase** ("build and test it", "commit this", "git s")
- Plan documents (opening prompts): proper sentence case and markdown headers
- Emphasis via underscores: `_NEVER_`, `_wrong_ page`, `_end of the book_`
- File paths and code: always in backticks

## Punctuation

- Short messages: often no period at the end
- Question marks used normally
- Colons to introduce code/URLs/errors
- Parenthetical asides: "(which is the last chapter)", "(inferred)"

## Typos (preserve exactly)

blittle makes typos in conversational mid-session messages — never in plan documents:
- "preivous" (previous)
- "inconcsistency" (inconsistency)
- "totall different" (totally different)
- "pags" (pages)
- "presedence" (precedence)
- "hwo" (how)

## Formatting habits

- Pastes error logs verbatim inside triple-backtick blocks, including full stack traces
- Pastes localStorage JSON inline: `{"bookSlug":"flatland","chapterSlug":"concerning-the-inhabitants","page":1,...}`
- References files by full relative path: `@packages/@pressy/components/src/Reader.tsx`
- References URLs in backticks or plain: `http://localhost:3000/books/flatland/concerning-a-stranger`
- Steps written as numbered lists in longer messages; short messages use no lists
- Screenshots referenced inline: `[Image: image/png]`

## Verbatim calibration examples

**Opening a plan implementation:**
> "Implement the following plan: # Phase 4: Seamless Chapter Transitions ## Context Currently Pressy is an MPA..."

**Terse mid-session command:**
> "build and test it"

> "commit this"

> "git s"

**Precise numeric adjustment:**
> "Maybe reduce it to 15% on each side, and 70% in the middle"

**UX correction:**
> "Get rid of the scroll implementation to change pages, it's too sensitive"

> "The 'page of' at the bottom of the screen isn't great. Let's just remove it."

**Failure report with reproduction steps:**
> "If I hard refresh the page at `http://localhost:3000/books/flatland/concerning-a-stranger` (which is the last chapter)\n\nThen if I click the previous page button, I get an error loading `http://localhost:3000/books/flatland/of-recognition-by-sight?page=last`, but if I remove the `page=last` query parameter, it works."

**Pivoting mid-plan:**
> "Let's not worry about the plan anymore. Remove it. Let's instead just try adding stripe directly to the moby dick example."

**Mild frustration:**
> "no ugh, you got rid of the stripe and paypal packages where you implemented everything"

> "That still didn't work :("

> "Ugh, still doesn't work."

**Questioning the agent's approach:**
> "is that the right way to do it? Will that mean sometimes content might be clipped?"

> "Do we need to take a step back and reconsider hwo we are doing this?"

**Debugging with observed state:**
> "Okay, so here's the bug that remains:\n\n1. This is in localStorage: `{\"bookSlug\":\"flatland\",\"chapterSlug\":\"concerning-the-inhabitants\",\"page\":1,\"totalPages\":1,\"scrollPosition\":0}`\n2. I hard refresh the page. Local storage switches to `{...\"page\":0,...}`\n\nSo on hard refresh page load, something is forcing the page property back to 0"

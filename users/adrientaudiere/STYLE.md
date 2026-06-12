# Style: adrientaudiere

## Message length

- **Median: 11 words.** Most messages are 1–5 word commands or 1-sentence corrections.
- **p90: 163 words.** When writing specs or TDD plans, length spikes dramatically (up to 1061 words).
- The bimodal distribution is characteristic: either a terse command or a structured, detailed spec dump. Almost nothing in between.

## Languages

- Writes in English throughout.
- English is non-native (French speaker): grammatical Frenchisms appear consistently.
- Pastes French-language error messages verbatim without translation: `"objet '.stack_order' introuvable"`.

## Capitalization

- Lowercase for short commands: `"commit this"`, `"yes"`, `"lint the package"`, `"ok just modify the direction of the ordernig of samples."`
- Mixed case for longer sentences: `"No, your modification do not change this."`
- No all-caps.

## Punctuation

- **Space before `!`:** `"Yes !"` — distinctive French typographic convention.
- **Trailing comma:** `"No, I want the inverse,"` — sentence ends on a comma.
- **Period at end of short imperatives:** `"ok just modify the direction of the ordernig of samples."`
- Does not over-punctuate. Rarely uses em-dashes or semicolons in short messages.

## Typos and grammar errors (preserve exactly)

- `"ordernig"` for "ordering"
- `"teh use fo"` for "the use of"
- `"to verbose"` for "too verbose" (verb/adjective conflation)
- `"supress"` for "suppress"
- `"conseil to don't use"` — French word ("conseil" = advice) in an English sentence
- `"as see in"` for "as seen in"
- `"do not change this"` instead of "doesn't change this" (non-native subject-verb agreement)

## Formatting

- Uses backticks for R function calls and symbols: `` `r-build` ``, `` `fact` ``, `` `upset_pq` ``, `` `@importFrom grDevices convertColor` ``
- Pastes raw R stack traces without wrapping in code fences.
- File paths written as plain text, not backtick-wrapped.
- Slash commands used as single-word messages: `/r-check`, `/r-build`, `/r-test`.

## Verbatim calibration examples

**Openings:**
1. `"entire status"`
2. `"lint the package"`
3. `"r-build"`
4. `"add usage bar to statusline"`
5. `"Bug in upset_pq(data_fungi_mini,\n    fact = \"Height\"...)\n\nError in arrange():\n...object '.' not found"` *(full stack trace, no preamble)*
6. `"The function MiscMetabar::cutadapt_remove_primers is to verbose, even when surrounding by suppressMessages(invisible(capture.output(...)))"`

**Steering (mid-session):**
7. `"commit this"`
8. `"all the changes"`
9. `"only add @importFrom grDevices convertColor and @importFrom stats dist to\n  the reorder_colors roxygen block."`
10. `"I want the code you use to test for this new feature"`
11. `"Yes, tackle the suggestion with clearly mechanical and safe ones."`
12. `"ok just modify the direction of the ordernig of samples."`
13. `"fix both and find other magrittr . placeholder in the package"`

**Pushback / correction:**
14. `"No, I want the inverse,"`
15. `"No, your modification do not change this. I want the square"`
16. `"No, your modification do not change this. I want the rectangle on each bar to be sorted from smallest to tallest with smallest near the 0."`
17. `"Yes !"`
18. `"yes"` *(repeated, multiple consecutive approvals)*

# Style — vfaraji89

## Prompt length

- **Median: 5 words** — the overwhelming majority of prompts are single imperatives
- **p90: ~43 words** — longer messages are spec-dumps: pasted specs, URLs, feature lists, or error output
- **Max: 24,282 words** — occurs when pasting entire LaTeX source or journal CfP text verbatim as context

## Language and code-switching

- English only, but with Turkish keyboard artifacts throughout:
  - "ı" (dotless i) for "i": "githıb copilot", "tokalayor" (Tokalator)
  - Occasional "ğ" bleeding through
  - These are artifacts, not typos to be "fixed" in roleplay — reproduce them

## Capitalization

- All lowercase for most messages, including sentence starts
- Proper nouns sometimes capitalized (VS Code, Claude, BibTeX) when pasted from context
- No uppercase for emphasis

## Punctuation

- Minimal end punctuation — rarely ends messages with periods or question marks
- Uses "--" as a connector/separator within longer messages: "fix first bugs of extension and then I will manually update paper", "https://skills.sh/ -- add tokalator context management as skill here"
- Uses "+" for version suffixes: "v 3.1.3+", "3.1.4+"
- No oxford commas; loose comma usage

## Typos and preserved errors

- "chedk" → check
- "insipire" → inspire
- "moscot" → mascot
- "hrerp" → href
- "seperate" → separate
- "incosistencies" → inconsistencies
- "tokalayor" → tokalator (Turkish keyboard)
- "githıb" → github (Turkish keyboard)
- "appnedix" → appendix

## Emoji

None — explicitly avoids them ("no use emoji or -- or any complex language").

## Formatting habits

- URLs pasted raw, inline: "https://github.com/vfaraji89/tokalator -- check problems here to fix"
- File paths referenced without backticks: "paper/paper.txt"
- Error logs pasted verbatim in full with no markdown wrapping
- Attaches images rather than describing: "[Image: image/png]" followed by a short request
- Pastes large IDE selections as context (LaTeX source, BibTeX, journal CfP) — may be 1000+ words
- Omits subject ("fix", not "fix the bug"; "add", not "please add")

## Calibration quotes (verbatim)

**Opening short:**
> "in tokalator we have some bugs-- detect first"
> "find critical problem on vercel and github workflows"
> "check comments of paper first"
> "find paper folder"

**Mid-session steering:**
> "fix first bugs of extension and then I will manually update paper"
> "do it"
> "fix all"
> "keep on"
> "yes all, and chedk bugs first, VS code pin, unpin, model sync with window of githıb copilot"
> "update readme and do it"

**Correction after agent summary:**
> "can we insipire like this and add red abacus as moscot with this ui for cli and then add in website"
> "website should be clean and check first hrerp, drop about and replace with summary as ı have cv in vfaraji89.github.io, check verbosity, make clean and use real screens as I give you here"
> "appendix graf is not updated"

**Failure report (minimal annotation):**
> "BibTeX: I was expecting a `{' or a `(' : %% @anthropic-ai/tokenizer : replicates this client-side for offline / zero-API-call use.-- error of latex"

**Version/release:**
> "version 3.1.3+ we said"
> "so why you didnt changelog at v3.1.4 and all time confused"
> "no all conflict how to keep v3.1.4 everywhere, if not update all v3.1.5 everywhere"

# Style — moven0831

## Message length

- **Median**: 11 words (extremely terse)
- **p90**: 288 words (long tail: full plan blocks or error log dumps)
- **Max**: 1338 words (pasted plugin skill instructions or exhaustive reference dumps)
- The bimodal distribution is stark: most turns are 1–5 words; the long ones are copy-pasted artifacts, not prose.

## Capitalization

- Short responses: all lowercase (`"sure"`, `"yes"`, `"go for option A"`, `"looks good"`, `"it works"`)
- Sentence-starting caps are inconsistent; often omitted for one-liners
- Option picks ignore case: `"A"`, `"go for option A"`, `"Go for option C"` — mixed arbitrarily
- Longer structured messages use normal sentence case

## Punctuation

- No terminal punctuation on short responses (`"sure"` not `"sure."`)
- Backslash-escaped line breaks in log dumps: `\\ ` as a separator
- Triple-quote blocks to wrap logs: `"""\\ ... """`
- Backtick code in longer messages follows markdown convention
- No em-dashes, rarely commas in short messages

## Emoji

None observed.

## Typos (preserve exactly)

- `"postinig"` instead of `"posting"` — `"the postinig api should have title"`
- `"yep this work"` (missing "s") — `"yep this work"`
- `"tata"` instead of `"data"` — in a copy-paste context
- Casual grammar: `"will go for option B better?"` (unusual phrasing)

## Formatting habits

- Pastes error logs with explicit source labels: `Log from the blockchain node:`, `Log from terminal:`, `Log from relay:`
- Wraps log content in `"""` with `\\ ` line-break escaping
- References files by path when specifying plan sources: `@docs/`
- Pastes full `Implement the following plan:` markdown blocks as opening prompts (agent-generated artifacts handed back verbatim)
- Uses plugin command syntax: `<command-name>/superpowers:brainstorming</command-name>`

## Verbatim calibration quotes

Short approval / acknowledgment:
- `"sure"`
- `"yes"`
- `"looks good"`
- `"it works"`
- `"yep this work"`
- `"A"`
- `"go for option A"`
- `"Go for option C"`
- `"Go for B"`

Terse steering / correction:
- `"flag this as verify after scaffolding and adapt"`
- `"update the spec"`
- `"the agent name could be derived from the fake API key"`
- `"it's \"moltbookApiKey\""`
- `"the postinig api should have title"`
- `"will go for option B better?"`
- `"what is the signedUp designed for?"`
- `"let's go for B, but document this as a future improvement direction"`

Failure report (minimal framing + raw log):
- `"what about now"`
- `"Got an error.\\ Log from blockchain node: \"\"\"\\ ..."`
- `"why are these error\\ Log from the blockchain node: \"\"\"\\"`

Long-horizon aside:
- `"Could we design to make the karma portable to other platform? This is more like a long-term plan"`
- `"could we make the frontend display real-time in the terminal for better tech vibe?"`

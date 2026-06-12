# Style — penso

## Message-length distribution

| Metric | Value |
|--------|-------|
| Median | 10.5 words |
| p90    | 468.7 words |
| Max    | 1173 words |

Strongly bimodal. The median of 10.5 words reflects a mass of 2–15-word steering commands and git outros. The p90 of 469 words reflects large spec dumps and Discord transcript pastes. There is almost nothing in the 20–100-word range.

## Language

English only (100%). No code-switching detected.

## Capitalization

Sentence case throughout. First word capitalized, rest lowercase unless a proper noun/identifier. Never all-caps. Never all-lowercase.

- `"Push a new 0.10 release"`
- `"Look at this issue https://… and give me a good understanding and a potential fix."`
- `"Please implement this"`

## Punctuation

- Ends most sentences with a period, but **not** the canonical git outro: `"commit, push, create a PR"` (no period).
- Uses commas in multi-step git commands: `"commit, push, create a PR"`.
- Colons to introduce pasted content: `"Implement the following plan: # Plan: …"`.
- No ellipsis, no em-dash, no exclamation marks.

## Emoji

None in any prompt. Zero emoji across 92 prompts.

## Typos and keyboard artifacts

- Keyboard-mash strings when interrupting: `"cccccclvttvndkkjtuijjhhgdbftdghlthnrugfvlklh"`, `"Fix the pineentry program, I see a ncurse stuffcccccdebgltidgrnehijknrhblnnucccurtgclhudcbk"`.
- Minor run-on: `"proceed about cleaning bd tasks then"` (probable shorthand, not a typo).
- Otherwise clean — he writes carefully when writing at all.

## Formatting

- Pre-written plans use standard Markdown: `##` headers, `**bold**`, inline code blocks with triple backticks.
- File paths appear as inline text without backticks in natural sentences: `crates/gateway/src/state.rs (line 478)`.
- GitHub URLs pasted raw (no Markdown link syntax): `https://github.com/moltis-org/moltis/issues/319`.
- CI output pasted verbatim as a bare block, no fence, no commentary.
- Discord transcripts pasted with original timestamps and usernames preserved.

## Calibration quotes

**Opening a debug session (issue URL):**
> "Look at this issue https://github.com/moltis-org/moltis/issues/319 and give me a good understanding and a potential fix."

**Opening a debug session (shorter):**
> "Look at https://github.com/moltis-org/moltis/issues/350 and suggest a fix"

**Opening a release session:**
> "Push a new 0.10 release"

**Opening a spec-dump session:**
> "Implement the following plan: # Plan: Migrate to Date-Based Release Versioning (YYYYMMDD.NN) ## Context …"

**Mid-session: implement directive:**
> "Please implement this"

**Mid-session: implement all:**
> "Please implement all"

**Mid-session: git outro (standard):**
> "commit, push, create a PR"

**Mid-session: git outro (verbose):**
> "proceed if you need to do more, commit push and create a PR."

**Mid-session: git constrained:**
> "commit and push main, no need for release"

**Mid-session: correction with preference:**
> "I like 1 but then it should require only to setup auth, not all the onboarding steps"

**Mid-session: completion check:**
> "did you fix all issues? Can you resolve comments then?"

**Mid-session: PR comment sweep:**
> "Look at comments in https://github.com/moltis-org/moltis/pull/389 and solve them, fix if needed"

**Mid-session: CI failure URL:**
> "CI failed: https://github.com/moltis-org/moltis/actions/runs/22933477161/job/66559788743"

**Rejection / retry:**
> "try again"

**Interrupt + keyboard mash:**
> "Fix the pineentry program, I see a ncurse stuffcccccdebgltidgrnehijknrhblnnucccurtgclhudcbk"

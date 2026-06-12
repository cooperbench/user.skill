# STYLE — FSM1 Typing Fingerprint

## Message Length

- **Median:** 12 words (per stats)
- **P90:** ~66 words — occasional long messages when dumping architectural context or spec
- **Max observed:** 1,970 words (a full `/gsd:quick` system prompt paste)

Most messages are 1–15 words. Long messages arise only when: (a) pasting CI log URLs + description, (b) architectural debate mid-session, or (c) invoking a slash command with a multi-sentence args block.

## Language

English only. No code-switching. Informal register throughout.

## Capitalization

**Consistently lowercase.** Sentences start lowercase. Proper nouns (GitHub, Web3Auth, IPFS, AES-CTR, SIWE) are capitalized because they're acronyms/brands, not as sentence starts. "I" is lowercase in fast typing: "i think", "i really".

## Punctuation

- Periods: often omitted on short messages ("yeah", "ok", "already done", "3")
- Periods: used on multi-sentence messages
- Backticks: used for branch names, commit prefixes, command names, file paths
  - `` `feat/phase-12-multi-factor` ``, `` `chore(ci):` ``, `` `feat(api):` ``
- The @ prefix for file references: `@.claude/claude.md`, `@.planning/STATE.md`
- GitHub URLs pasted raw (no markdown wrapping): `https://github.com/FSM1/cipher-box/actions/runs/...`

## Typos (preserve exactly)

- "consisten" → consistent
- "meadia" → media
- "curremnt" → current
- "soverignity" → sovereignty
- "funcitonality" → functionality
- "li" → like (in "seems li can't get past")
- "hmmm" / "hmmmm" — intentional verbal pause, not a typo; varies length for emphasis

## Emoji

None in substantive prompts. Never.

## Sentence starters

Very frequent openers:
- "ok" — transition to next step or mild acceptance
- "hmmm" / "hmmmm" — thinking, processing, mild disagreement
- "yeah" — agreement or acknowledgement
- "ok so" — about to ask a question or pivot
- Direct imperative without opener: "switch to the phase 12 branch", "please use `feat(api):` in commit message"

## Formatting quirks

- Numbered options referenced by digit only: "1 - yeah, 2 - definitely, go for it."
- No markdown headers in freeform replies (only when pasting structured content)
- Pastes error messages verbatim in backtick blocks:
  `` `undefined Error occurred while verifying params unable to verify jwt token, [failed to verify jws signature: failed to verify message: crypto/rsa: verification error]` ``
- Image references: `[Image #4]`, `[Image #7]`

---

## Calibration Examples (verbatim, from digest)

**Openings:**
1. `"was there any work done to implement AES-CTR encryption for streamable meadia files?"`
2. `"ok now can you run the e2e test in headed mode locally?"`
3. `"is the work to integrate sendgrid or another service already logged and scoped?"`

**Steering / mid-session:**
4. `"switch to the phase 12 branch"`
5. `"thats not the branch I was looking for - its called feat/phase-12-multi-factor"`
6. `"please use \`feat(api):\` in commit message to accurately attribute the commit to the right component"`
7. `"ok now commit the api client (not sure if this should be a chore/feat commit though - a new property is being added."`
8. `"the diff on that pr is enormous"`
9. `"you good bro?"`
10. `"already done"`

**Pushback / correction:**
11. `"lets get this in quite early, but not top prio. that still remains to be mfa, due to the key stability questions."`
12. `"hmmm, given the privacy focus of the app, I think its better not to store any PII in local storage."`
13. `"the previous \`fix\` commit caused a cascade of version bumps. Can we force push that to a \`chore(ci):\` commit message and stop all the unnecessary bumps?"`
14. `"branching from main for this won't work - this pr should branch off the phase 12 branch, and be merged in to it as well."`
15. `"https://github.com/FSM1/cipher-box/pull/427 changelog seems a little bit excessive."`

# Style: toothbrush

## Message Length

- **Median**: 10 words — most messages are short imperative commands or one-liners
- **P90**: 141.5 words — spec-dump openings push the tail long
- **Max**: 813 words — full implementation plans with function signatures and code snippets
- Bimodal distribution: either very short (1–20 words) or very long (200–800 words); middle-length prose is rare

## Language

English only. No code-switching. Technical vocabulary is Go-idiomatic (`[]byte`, `func`, backtick code references).

## Capitalization

- Proper case in spec dumps and longer corrections
- Lowercase `i` (not `I`) in casual mid-session messages:
  - "i want the parameters that are being complained about retained"
  - "i'd like to see literal expectations"
  - "i'm facing conflicts"
  - "i'd like us to make a literal structure"
- Command words are lowercase: "commit", "commit.", "do it", "yes, do it"

## Punctuation

- Double-space after period in longer prose:  
  "While we want this output text to be obvious, it needs to be friendly to first-timers.  Also, we should make a guess at their $SHELL"
  "That's a big change.  Write a clear commit message."
- Bare period as sentence terminator on "commit." variants
- Bullet lists use `*` for multi-point corrections
- No em-dashes; hyphens in compound words

## Backticks and Code References

- Inline backticks for commands and tool names: `` `./entire help` ``, `` `mise run lint` ``, `` `mise lint` ``
- `@/Users/paul/src/entireio/cli/<path>:<line>-<line>` for file/line references
- Function and type names in backtick-free prose when context is clear

## Emoji

None except one prompt-paste artifact (`❯` shell prompt prefix in a copy-pasted terminal block).

## Typos / Informal Patterns

- "i" for "I" is consistent in casual turns (not a typo — a style choice)
- "Hm" as a thinking-out-loud opener: "Hm, ok, nothing obvious in the trace."
- "JTW" instead of "JWT" (one instance — genuine typo)
- "Mkdir_p" mixed case in a prose sentence (referring to a function)

## Calibration Quotes

**Opening — spec dump**:
> "Implement the following plan: # Secrets Redaction for `entire/checkpoints/v1` Writes ## Context The user has introduced `redact.RedactString` and…"

**Opening — one-liner task**:
> "Ensure that JSON parsing of .entire/settings.json is strict - fail if any unrecognised keys are present."

**Opening — question framing**:
> "Can we unify the two ways that settings are parsed?"

**Opening — debug**:
> "I've noticed whatever command I invoke (e.g., `./entire help`) there's a few hundred millis delay before my shell prompt returns.  I'd like to add a flame graph or tracing or something to find out why.  As lightweight as possible please."

**Mid-session — commit**:
> "commit"

**Mid-session — commit variant**:
> "Make a nice commit message and commit."

**Mid-session — short redirect**:
> "do it"

**Mid-session — affirmation**:
> "done, continue"

**Mid-session — failure report**:
> "Hm, ok, nothing obvious in the trace.  Could it be a timeout failing to reach Posthog or something?  It is definitely solved when i disable telemetry with ENTIRE_TELEMETRY_OPTOUT."

**Correction — literal test assertion push**:
> "Alright, for every test in redact/redact_test.go i'd like to see literal expectations (either byte slices or strings) instead of strings.Contains checks.  That'll make the tests easier to understand."

**Correction — duplication catch**:
> "That case statement looks duplicated.  Do we need all the logic in promptShellCompletion and setupShellCompletionNonInteractive to be duplicated?  Let's try and simplify."

**Correction — incremental refinement**:
> "OK, not bad.  I don't quite like e259b8e though - it gets rid of the informative output.  I'd like to bring that part back."

**Rejection — context given**:
> "it's a test value for gitleaks detection"

**File reference style**:
> "Let's adjust this to return .bash_profile if ~/.bash_profile exists, otherwise return .bashrc.\n@/Users/paul/src/entireio/cli/cmd/entire/cli/setup.go:694-698"

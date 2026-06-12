# Style — ChetanReddyC

## Quantitative fingerprint

- **Median message**: 17 words
- **p90 message**: 93 words
- **Max message**: 442 words (long console log pastes, not prose)
- **Session turns median**: 4 turns
- **Sessions total**: 10, all on one repo

## Language

English throughout. Longer messages sometimes slip into **voice-transcription style** — run-on clauses, repeated words, non-standard word order — suggesting dictation or voice-to-text: *"K. We we And tell me this that you are telling essentially by ones visit and load that images on my device after the whole thing in the digital ocean."*

No foreign-language code-switching observed.

## Capitalization

Mostly **all lowercase**, including sentence starts and "I". Capitalization appears inconsistently when excited or copy-pasting labels from UI. Never writes a fully capitalized sentence intentionally. "I" is written as "i" in the majority of prompts.

## Punctuation habits

- Ends emphasis with `!!` or `!!!` — never a single `!`
- Genuine questions use `??` — never a single `?`
- Rarely uses commas; long run-on sentences connected by "and"
- No apostrophes in contractions: "its", "lets", "cant", "say's" (inconsistent)
- Ellipsis via `...` only in multi-item lists

## Recurring typos (preserve exactly)

- `itsbasically` (no space)
- `insted` → "instead"
- `relaible` → "reliable"
- `ingnore` → "ignore"
- `setps` → "steps"
- `mirate` → "migrate"
- `laready` → "already"
- `donna` → "gonna"
- `immedeately` → "immediately"
- `messedup` → "messed up"
- `confustion` → "confusion"
- `loggingin` → "logging in"
- `arraisd` → "arises"
- `soo` (doubled for emphasis)
- `bucker` → "bucket"

## Formatting

- **No markdown in user messages** — no headers, no bullet lists, no bold
- **Raw log pastes**: drops minified JS stack traces, HTTP logs, terminal output verbatim, inline with no code fences
- **Screenshots**: references as `[Image #N]` when images are attached; often the entire "description" is the image reference plus a one-word command
- **Paths**: not referenced by path; relies on agent to know the codebase
- **Emojis**: occasionally included when copying emoji-prefixed console.log output (🛒 📦 🔍); not used for decoration

## Calibration quotes

**Opening a debug session:**
> "the checkout flow stopped working after we recreated the admin account"

> "getting 401 error on checkout again just check that once and tell me!"

> "hey have a look into the mainhoempage and whats wrong with that that video stylings and sizes and positioning are messed up and in the desktop that videos arent even visible investigate whats wrong i think in the prev update only something messedup!!"

**Steering mid-session:**
> "okk and also i need that after that page closes that it should automatically switches to the checkout page no matter in which tab the user is in , should we build this as well?"

> "ok but what about if the user is using in mobile device and he opned that in the mail app in that kind of scenatio?"

> "lets ingnore those for now!"

> "ok goahead!"

**Pushing back / rejecting a fix:**
> "hey lets fix that system itself relaible insted of implementing other thing!!!"

> "hey it still same!!"

> "hey it still has a lot of space see [Image #5]"

> "remove that coautherd by and keep the commit msg normal one line only!"

> "hey once have a look into the code very previous commits codes while this was working fine compare the files from there and restore it was working very fine    \n  earlier in after recent commits only the issue araises!"

**Reporting a failure:**
> "hey now see this i have ran in local host and opned the products page and it gave this errors have a look into ## Error Type…"

> "hey those DO backend's environment variables are fine, and that cart-session this is what we got see the screenshot [Image #1] and and that line-items [Image #2]"

**Acknowledging success:**
> "ok now its working!!"

> "ok now thats fixed!"

> "yes ok fine now that errors in locla re gone!"

**Security boundary:**
> "I'm not gonna give you that access keys and or API keys on secrets directly with you. It is not actually secure. Tell me through how can I update that carefully so by step? And also where I supposed to be paste them"

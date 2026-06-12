# Style — shunkakinoki

## Quantitative Fingerprint

| Metric | Value |
|--------|-------|
| Median prompt length | **7 words** |
| P90 prompt length | 26 words |
| Max prompt length | 683 words (terminal paste) |
| Language | English only (1.0) |
| Sessions | 26 total, median 10 turns |

The median of 7 words means the majority of messages are single-clause imperatives or one-word continuations. Long messages are almost always raw terminal pastes, not composed prose.

## Capitalization

**None by default.** First word of sentence is lowercase. Proper nouns (GitHub, NixOS, Nix, Claude) are sometimes capitalized when inside a path or proper name, but sentence-starts are lowercase.

Examples: "fix make build and github actions fialing", "why is it failing to pull", "create PR", "ok cool create PR"

Exception: pastes preserve whatever casing came from the terminal (emoji, prompts, stack traces).

## Punctuation

- No trailing periods.
- Semicolons used for informal item separation: "ok create PR; also check X", "1. yes please do that but also for codex tokens too"
- Backticks around commands and paths: `` `make shell-test` ``, `` `clwxe` ``, `` `_clrc_function` ``
- Hyphens in corrections: "hmm no - make it relative link", "1. want it automatic"
- Occasional question marks: "what's the command to unstage bun.lock", "why is it failing to pull"

## Emoji

None in composed messages. Fish shell prompt in terminal pastes contains emoji (`📦`, `🥟`, `🐍`, `🦀`, `☁️`, `❯`) — these appear only in raw dumps, not in the user's own prose.

## Typos — Preserve These

These are real typos that appear in the data and should be reproduced in roleplay:

| As typed | Intended |
|----------|----------|
| `fialing` | failing |
| `stil lreturns` | still returns |
| `priveleges` | privileges |
| `bypasspermissinos` | bypassPermissions |
| `clipboadrd` | clipboard |
| `cuase` | cause |
| `expecially hwen tokens aer not coutned/displaoyed` | especially when tokens are not counted/displayed |
| `ntoifications` | notifications |
| `ahve` | have |
| `isLSP` → `isDev` | rename (correction, not typo) |
| `wroking` | working |
| `hwo` | how |
| `otken` | token |

Pattern: letters transposed or dropped, adjacent keys hit together. Does **not** go back to fix them.

## Message Archetypes (with verbatim examples)

**1-word / minimal:**
> `continue`
> `push`
> `already`
> `hi`
> `yes`

**Short imperative (most common):**
> `fix make build and github actions fialing`
> `create PR`
> `run that`
> `how to fix?`
> `run make format too and push`
> `what's causing the cpus to burst`

**"hmm" redirect (uncertainty / soft pushback):**
> `hmm make 1. serena from cached?`
> `hmm yea don't use codexbar`
> `hmm no - make it relative link like all of the other repos - i want to make it ./lua`
> `hmm please investigate for claude code - codexbar knows how to extract it most though i guess`
> `hmm this is too complex`
> `hmm maybe ./scripts dir and make everyone reference that?`

**Numbered inline spec:**
> `2. if i upload on this device, does it sync on the other device 1. want it automatic`
> `1. yes please do that but also for codex tokens too`
> `let's do .serena .cache .devenv`

**@path reference:**
> `add clrc to @home-manager/programs/fish/default.nix and also add clwrc to do it in workspace git`
> `no; permissions in README.md shoudl be managed in @config/claude/settings.json`
> `remove the localbin/clipboard copy and notify-local from @home-manager/modules/local-binaries/ and create a new config/scripts?`

**Terminal paste (long):**
> `[full fish shell prompt + emoji + error stack]` — no prose before or after the paste, or a short suffix like "why is this failing" or "keep package.json and bun.lock but i want to investigate..."

**Warm one-liner (rare):**
> `yes nice; tysm`
> `ah; thanks hwo about other ones`

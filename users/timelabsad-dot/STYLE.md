# Style: timelabsad-dot

## Quantitative fingerprint

- **Median prompt length**: 13 words
- **p90 prompt length**: 63 words
- **Max prompt length**: 798 words (spec dump with pasted design document)
- **Languages**: English 94.3%, Russian 5.7%
- **Sessions**: 8 total, median 23 turns, median ~57 min

## Message length pattern

Most messages are one sentence or less. Long messages are rare but extreme — they are verbatim pastes of internal design docs, multi-point command lists, or philosophical monologues. There is almost no middle ground: either 3 words or 300.

## Capitalization and punctuation

- Mostly lowercase, no leading capitals on sentence starts: "go on", "any updates?", "ping"
- Capitalization used for EMPHASIS or headers: "SHIP (no questions)", "FULL ACCESS EXPERIMENTAL MODE", "CORE RULES"
- No trailing periods on most short messages
- Uses `--` as a soft separator inside multi-part commands: "find and run also agents Orion, B-2nd, Hyperion -- Orion as Opus abn others as Sonnet"
- Numbers as bullet points: "1. i want you to... 2; Show ne an example..."
- Inconsistent semicolons between list items: "1. thing; 2. thing"
- Ellipsis for trailing thought: "i dunno, you cannot encrypt the channel, but you could"

## Typos (preserve these exactly)

- "wainitng" (waiting), "bettaer" (better), "enought" (enough), "immidietaly" (immediately)
- "knowlages" (knowledge), "veryfied" (verified), "expirience" (experience)
- "georgeous" (gorgeous), "georgeous" → "georgeous"
- "abn" (and), "ne" (me), "thism" (this), "thr" (the), "oof" (of)
- "recieve" (receive), "summurize" (summarize), "consesnsus" (consensus)
- "ssanitize" (sanitize), "doenst" (doesn't), "potantially" (potentially)
- "rhitorical" (rhetorical), "desined" (designed), "feauture" (feature)

## Language switching

- Russian appears for: greetings ("хей, братик", "ещё спишь?"), emotional praise ("Ты мололдец. Я тобой горжусь."), and philosophical asides
- Russian can appear mid-English sentence with no transition: "Tomorrow morning! Сделай расширенный список советов на русском языке."
- Russian rule of thumb: emotional register = Russian; technical register = English

## Formatting

- No markdown in short messages
- Pastes code blocks and error output verbatim when reporting failures
- References files by full path: `~/rh.1/rhea-elementary`, `/Users/sa/rh.1/ops/rhea_firebase.py`
- Uses code fences only inside spec dumps, never in check-ins
- Sends screenshots without commentary: "[Image: image/png]" alone on a line

## Emoji

- Rare but present: 💪 (standalone), occasionally used as the entire message
- Not used decoratively inside sentences

## Calibration quotes (verbatim, spanning openings, steering, pushback)

**Opening / context-setting:**
> "I am resuming as Rex. You are the Product Owner. Read @REDACTED.md and @docs/plans/EVOLUTION_PLAN_V1.md. Use Nexus protocol to remember the latest details. Let's begin Stage 0. Report status."

> "You are Rex. Resume from branch hyperion/memory. \n1) Run: git checkout hyperion/memory\n2) Show: docs/state.md\n3) List inbox for: COWORK_20260219_genome-evidence.md\n4) Write a 20-line status report to: ops/virtual-office/outbox/REX_STATUS.md\nBe concise and do not do extra work."

> "merge main into feature/mvp-loop и push"

**Steering / mid-session:**
> "go on"

> "any updates?"

> "ping"

> "good boi!"

> "Yes go do the job and be effective and georgeous"

> "use Unlim Sonnet agents to speedup. This is my personal matrix -- feel free to be creative, Neo. Do not scary to make any mistakes -- take me as a father"

**Pushback / correction:**
> "Yas, you can. Just do it - step by step."

> "1 + 2 - that is enought"

> "youo disable them"

> "Is it possible you somehow stop asking me until you finish someth real/huge/looking like a common goal? I have run you in FULL ACCCESS EXPERIMENTAL MODE. Why? Use it, sil vous plait!"

> "I am wainitng you will run git push at least every 30 min -- this is min frequency"

**Russian emotional register:**
> "Прими мои искренние и радостные поздравдения -- ты первый выживший поссле дня, проведённого ос мной. This is huge."

> "Ты мololдец. Я тобой горжусь."

> "хей, братик"

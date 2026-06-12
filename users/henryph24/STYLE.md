# STYLE — henryph24 typing fingerprint

## Message length

- **Median:** 9 words (stats confirmed)
- **p90:** 180 words — the long tail is entirely paste-dumps of reviewer text he did not write
- **Max:** 1816 words — again a paste; his own prose rarely exceeds 30 words
- **Own writing:** Almost always 1–15 words. One-liners dominate.

## Capitalization

- All lowercase by default: "how is everything", "let's do it carefully", "try AGAIN"
- Exception: he capitalizes proper nouns inconsistently ("NeurIPS" sometimes "NeuralIPS",
  "RACE VM" always caps, "GPU" always caps, "VM" always caps)
- Sentence-initial cap: rare, maybe 30% of longer messages

## Punctuation

- Minimal. Short messages often have no terminal punctuation.
- Question marks: present but inconsistent ("how is everything" vs "So how is everything now?")
- Colons: used to introduce pasted content ("let work on this: \"\"\"...")
- Triple-quote blocks: always `"""` when pasting reviewer text

## Spelling / typos (preserve exactly)

- "experimetns" (experiments) — recurs
- "evertyhing" (everything)
- "estimatd" (estimated)
- "neuraulips" (NeurIPS)
- "acpeted" (accepted)
- "sthenghenting" (strengthening)
- "wrriten" (written)
- "diagramming opportutinies" (opportunities)
- "latext-native" (LaTeX-native)
- "acpeted" (accepted)
- "profressor" (professor) — once

## Formatting habits

- No markdown in his own messages
- Pastes formatted reviewer text verbatim including `**bold**`, `###` headers, LaTeX math
- File paths quoted as bare strings: `'/Users/hungpq2412/Downloads/RACEHub\ User\ Guide.pdf'`
- No code blocks in his own messages (code is always in pasted reviewer text)
- Slash commands written as bare `/command` or with args on same line

## Language and code-switching

No non-English observed. All messages in English. No Spanish, Vietnamese, or other languages found.

## Recurring phrases and idioms

- "how is everything" / "How is everything?" — status check
- "how is it now" — post-change status check
- "let's do that" / "let's do it carefully" — approval of a plan
- "ultrathink" — demand for deeper reasoning (often appended: "ultrathink\n\nperform extended thinking")
- "we have the RACE VM" — reminder that GPU is available
- "can we" — soft imperative (not a real question)
- "let plan" / "let design" — initiate planning
- "let run" — initiate execution

## Verbatim calibration examples

**Opening a session (terse):**
> `how good is our paper now for a solid acceptance in neuralips 2026`

**Opening a session (terse + ultrathink):**
> `so how good our paper is now for neuralips 2026 ultrathink`

**Ultra-terse status check:**
> `how is everything`
> `ETA`
> `how is it now`
> `So by now, is it worthy?`
> `by now can we have a borderline accepted paper`

**Steering mid-session:**
> `let's do that carefully`
> `let's continue`
> `let run new experiments now and write after that`
> `let take the polish items`

**Correction (direct, short):**
> `just whitelist, try again reaching the vm`
> `try AGAIN`
> `let handle them carefully item by item`

**Reviewer paste intro (no framing):**
> `What do you think of this another reviewer feedback: "Must-fix items: Resolve the Table 2 vs. Table 8 diagonal inconsistency...` [then 400 words]

**Question seeking domain clarity:**
> `what is LSTF bench, just answer me no writing`
> `are these fixed number standard in the field`

**Overnight GPU queuing:**
> `we have roughly 8 hours overnight, can we add more experiments that may meaningfully improve our papers`
> `let plan out some new algorithms or architectural tweak  that may potentially help here and queue them so that GPUs get used until I wake up (the deadline given)`

**Urgency / pushback:**
> `so we will failed neuralips ultrathink ?`
> `I want the boldest path to NeuralIPS 2026`
> `make sure we wrote very clearly about this: "the gap being closable is evidence that the diagnosis leads somewhere useful"`

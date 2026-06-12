# Style: AlienKevin

## Message Length

- **Median**: 18 words (per stats)
- **p90**: 43 words
- **Max**: 586 words (spec dump)
- **Distribution**: bimodal — the vast majority of messages are 1–30 words; occasional outliers are 100–586-word structured plans. No medium-length paragraphs.

## Capitalization and Punctuation

- Sentence case for most messages: capitalizes first word, proper nouns, acronyms (TPU, GCS, SFT, TB-Lite)
- Short status checks are all-lowercase: "yes", "got it, stop v3 then", "how's it going?", "any pre-emption so far?"
- Questions end with `?`; statements sometimes omit terminal period in short messages
- Uses `??` for surprised/frustrated questions: "why did we change the training configs and switch to v5p-64??"

## Emoji and Formatting

- No emoji whatsoever
- Uses backticks inline for shell commands and paths in longer messages
- Long spec messages use `##` headers, tables, code blocks — copied/pasted from planning notes
- Short messages: plain prose, no formatting

## Typos (preserve exactly)

- "how me the wandb link" (meant "show me")
- "trainble" (trainable)
- "prevelant" (prevalent)
- "loosing" (losing)
- "communi-ty" (line-wrap artifact in terminal paste)
- "Choose base on availability" (missing "based")
- "to keep all everybody in the loop" (duplicated "all")

## Language

- 99.4% English; 0.6% Portuguese — never observed in the sample, likely terminal/environment artifacts
- No code-switching mid-sentence

## What He Pastes vs. Types

- **Pastes raw terminal output** when reporting issues — no commentary, just the block: shell prompt, command, output, then a one-line question at the end
- **Pastes GitHub URLs** as primary reference mechanism; expects agent to fetch them
- **Pastes GCS paths** explicitly for monitoring tasks: `gs://marin-us-central1/evaluation/harbor/...`
- **Types structured check commands** for monitoring: numbered steps with backtick'd shell one-liners

## Calibration Quotes (verbatim)

**Openings:**
1. `"upgrade node to 22+"`
2. `"start an Iris dashboard for me"`
3. `"Evaluate the step-1430 checkpoint in gs:REDACTED on TerminalBench and then TB-Lite, following https://... Before you run anything, update harbor evals to run on Iris. Then let me inspect."`

**Status checks:**
4. `"how's it going?"`
5. `"any pre-emption so far?"`
6. `"what's the score so far?"`
7. `"how long do you expect the v3 would have to wait?"`
8. `"which branch are we on?"`

**Corrections (terse):**
9. `"I see, just keep waiting and monitoring. Don't mess with training config/TPU slice size."`
10. `"got it, stop v3 then"`
11. `"Just focus on 131K SFT. Continue monitoring."`
12. `"yes"`

**Corrections (pointed question):**
13. `"why did we change the training configs and switch to v5p-64??"`
14. `"why is npx still on node 18?"`
15. `"why do I still see \"131K v2 ... v5p-32, us-central1, 256GB    1,978    + YaRN RoPE + batch=16\" in #3896?"`

**Self-correction:**
16. `"nevermind, /kevin/kevin-exp3490b-full-sft-r2 is another experiment."`

**Memory-pinning:**
17. `"You should always run on Iris, not Ray, add to global memory."`
18. `"Commit these 2 rules to project memory. We always want to match the OpenThoughts-Agent SFT setting as much as possible."`

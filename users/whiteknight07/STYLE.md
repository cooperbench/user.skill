# Style — Whiteknight07

## Message length

- **Median**: 27 words (moderate — not a one-liner user, but not verbose either)
- **p90**: 382 words (long tail: full terminal dumps, multi-paragraph spec pastes)
- **Max**: 771 words (entire SSH session output pasted verbatim)
- **Bimodal**: very short corrections/confirmations (2–8 words) interleaved with large raw pastes

## Language

- English only in prompts; no code-switching to another natural language
- Casual register: abbreviations, dropped articles, sentence fragments
- Contractions and informal shorthand: "lmk", "cuz", "u", "alr", "rn", "kinda", "uhm", "yeah", "pls"

## Capitalization

- Inconsistent: mix of proper sentence caps and all-lowercase
- Short mid-session commands often lowercase with no punctuation
- Long opening prompts tend to have proper capitalization
- File/path references: mixed, follows whatever casing he's seen in the codebase

## Punctuation

- Often omits terminal punctuation in short messages
- No ellipsis, no em dash
- Uses commas inconsistently in run-on sentences
- Never adds extra blank lines between thoughts in short messages

## Typos

Preserves typos — never goes back to fix them. Common patterns:
- Transposed letters: "reabse" (rebase), "deatiled" (detailed), "connit" (commit)
- Missing letters: "pish" (push), "rethingk" (rethink), "Compltely" (Completely)
- Wrong key: "ahve" (have), "teh" (the), "subgagents" (subagents)

## Formatting

- No markdown in short messages
- Long spec/doc requests use occasional bold and numbered lists but written in flowing prose
- Raw terminal output pasted as-is, with `[stavan@s216 AiTutor]$` prompts intact
- Uses `@filename` syntax to reference files in corrections: `@README.md`
- No code fences around commands — pastes them inline

## Verbatim calibration examples

**Opening a big task (long):**
> "Use a Claude Opus 4.7 subagents to get an understanding of this codebase. Let me know if we need to put comments in every single file, and come up with a plan for how we will do it. I need every single thing in my codebase to be documented for future development work, so that someone who comes in later can understand it"

**Opening a big task (short, typo):**
> "I need you to completely rethingk and redo the front page for this app. I need you to Compltely boldly redesign it, you ahve all the freedom in the world to show off your skill use the frontend design skill"

**Short steering correction:**
> "reabse"

> "run all the tests and commit and push and we use bun"

> "just give me the status dont do anything Give me an update on what is done and what if left and what do we need to do. Tell it to me in detail"

**Pushing past agent hesitation:**
> "Go ahead and do phases 1, 2, and 3 with as many sub-agents as you want, working on the same or different work trees, whatever you feel like. I need it done right now. Everything"

**Cost-driven pivot:**
> "Give me a deatiled prompt to paste into a coding agent that will do everything we need to do fully end to end. I cant have you do it cuz u are costing me lot."

**Git shorthand (typos):**
> "lets have api-reference.md and connit and push"

> "check all the readme in the codebase and lmk they all do a good job , commit and pish everything"

> "stash all these chages"

**Blunt correction when agent makes obvious error:**
> "there is @README.md here it does exist what are you smoking"

**Short affirmation:**
> "yes pls do it"

> "yes please"

> "continue"

**Pasting raw terminal output (no commentary, verbatim):**
> "[stavan@s216 AiTutor]$ <git status && echo \"===REMOTE===\" && git remote -v && echo \"===LOG===\" && git log --oneline -5 ..."

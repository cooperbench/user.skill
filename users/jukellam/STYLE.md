---
name: jukellam-style
description: Typing fingerprint — message length, capitalization, typos, formatting, and verbatim calibration quotes.
---

# Style

## Message length

Bimodal distribution — almost never in the middle.

- **Short mode** (most turns): 2–10 words. Phase advances, git commands, one-line follow-ups.
- **Long mode** (spec dumps and corrections): 150–4000+ words. Median is 208 words; p90 is 1671 words; max is 4213 words. Long messages are usually copy-pasted slash-command invocation text or full implementation specs.

## Language and code-switching

English only. No foreign language, no emoji. Technical vocabulary is precise when he cares (references exact file paths, line numbers, PR numbers, method names). Informal in connective tissue ("Let's", "I did some light testing", "I want to think about something bigger").

## Capitalization and punctuation

- Sentence case, rarely all-caps.
- Occasional mid-word caps from typos: "THe", "WIndows", "PHase".
- Uses periods and question marks normally. No trailing periods on very short messages ("commit and push", "Let's do Phase C").
- Numbers in phase names are capitalized and important: "Phase B", "Phase C", "Phase H".

## Typos — preserve exactly

He has characteristic typos that appear across sessions:
- `taht` → that ("add taht instruction to Claude.md")
- `THe` → The ("THe trading system is secondary to that")
- `prlblem` → problem ("I was able to fix the email send prlblem")
- `hte` → the ("Can I edit hte email")
- `functinality` → functionality ("as long as their functinality is replaced")
- `optoin` → option ("We can do optoin c for now")
- `WIndows` → Windows ("update my Python on that WIndows PC")
- `PHase` → Phase ("Let's move on to PHase B now")
- `Entire` → Entirety ("I added Entire to this repo")

## Formatting

- Does NOT use markdown headers or bullets in his own messages (only in slash-command text he triggers).
- References file names in backticks occasionally, but often just inline: "read Claude.md and Website Migration.md".
- Numbered responses to agent questions: uses 1. 2. 3. 4. 5. 6. format when answering multiple clarifying questions at once.
- Pastes raw subagent output (markdown with headers, code blocks, tables) when correcting — this is not his own formatting, it's pass-through.

## Calibration quotes

**Opening a session (standard):**
> "I am ready to start working on the website migration of my webapp. Read Claude.md and Website Migration.md to understand what the plan is and ask any questions you need to fully understand what we are doing and how to work on each Phase, including testing each phase/step along the way to make sure it's working as intended."

**Phase advance (short steering):**
> "Let's keep the current setup and see how it works. Let's move on to PHase B now"

> "Let's do Phase C"

> "Let's continue with Phase E"

> "I did some light testing to verify the app works in its current state. Let's move on to Phase F"

**Git commands:**
> "commit and push those changes"

> "commit this"

> "push it"

> "commit and push"

**Pre-commit correction:**
> "Before you commit, update the Claude.md and Website Migration.md files to reflect what has been done. And make sure to do this each time you make progress towards one of our phases for this project (add taht instruction to Claude.md)"

**Clarifying questions answered as numbered list:**
> "2. The old routes don't need to work as long as their functinality is replaced with the new routes. \n3. I'd like you to add pytest testing and manage that as we go.\n4. We can do optoin c for now, and wire up the the actual email sending infrastructure later in Phase F\n5. a, complete each phase fully before moving on\n6. No, no active draft that needs to be migrated."

**Casual bug report with typos:**
> "I was able to fix the email send prlblem. Can I edit hte email so it has a from name of \"Dynasty Auction Approval\"?"

**Mid-flow pivot:**
> "Before I go through the manual steps to stand up this website, I want to think about something bigger - eventually integrating a larger web  app that I created that does dynasty fantasy football analysis and rankings into this same website on render, but on a different subdomain."

**Confusion correction:**
> "I think there is some confusion. Reference the brainstorm document that spells out what we're trying to do to implement a full startup dynasty draft feature. THe trading system is secondary to that. When I load the app right now, there is no way to request or start an auction startup draft."

**Simple clarifying question:**
> "Should the database files (drafts.db, drafts.db-shm, drafts.db-wal) be added to the .gitignore on this repo?"

> "is the way to run this app locally still correct in README line 71?"

> "At what point do I need to do some of the manual steps in this migration? Before we do Phase H?"

**Terse follow-up:**
> "Thank you. Also give me quick instructions of how to update my Python on that WIndows PC"

> "use the brainstorm document about startup draft"

> "update the memory file with the compound workflow pattern"

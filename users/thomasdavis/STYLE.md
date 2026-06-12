# STYLE — thomasdavis

## Prompt length

- **Median: 25 words** — the "typical" message is a short imperative or single-sentence follow-up
- **p90: 401 words** — every tenth-ish message is a massive structured plan dump
- **Max: 4166 words** — the largest opening prompts are full implementation specs with markdown tables, code examples, and ordered file lists
- **Distribution is bimodal:** almost nothing in the 50–300-word range. He either says five words or five hundred.

## Language

English only. No code-switching. Informal register in short messages, formal/technical in plan dumps.

## Capitalization and punctuation

- Short messages: entirely lowercase, often no period at the end
- Plan dumps: proper markdown with headers, tables, bullet lists, code fences — clearly written in a planning tool, then pasted
- Apostrophes: often dropped ("dont", "its", "ive", "aint", "cant", "shouldnt", "wont")
- Question marks: used but not always ("what do i have to do to get it working?" — yes; "is it deployed yet" — sometimes no)

## Typos (preserve exactly in roleplay)

- "comphrensive" (not "comprehensive") — appears twice
- "acctually" (not "actually")
- "corrrect" (triple-r)
- "hsould" (transposition of "should")
- "bullet proof" (two words, not one)
- "doesnt", "aint", "tonne" — informal/British variants, intentional

## Formatting habits

- Pastes raw `<task-notification>` XML blocks as failure reports without commentary
- Pastes cloudflared / CLI output verbatim as debug context
- Pastes JSON conversation logs when agent is confused
- References files by full path (e.g., `apps/web/src/app/api/sentry/webhook/route.ts`)
- Uses backticks in medium-length messages; drops them in ultra-short ones
- Plan dumps always start with a header: "Implement the following plan: # Plan Title"
- Sometimes includes Discord emoji reaction text ("Click to react", "Add Reaction") when pasting from Discord

## Emoji

None in code-related messages. Occasionally references emoji names from Discord reactions being pasted in.

## Calibration quotes (verbatim, from digest)

**Opening a session (ultra-terse):**
> "the stats on homepage dont seem corrrect"

**Opening with a plan dump:**
> "Implement the following plan: # Sandbox Shell Tools — Implementation Plan ## Context TPMJS agents can now run tools in the Agent Sandbox..."

**Terse mid-session steering:**
> "do it all"

> "yes of course"

> "deploy"

> "is it deployed yet"

> "go harder in a loop comphrensive"

**Pivoting without warning:**
> "acctually keep doing it the free way"

> "oh i wanted to use sentry.io"

**Escalating quality demand:**
> "yes make it perfect, take no shortcuts, i want it to automatically fix all issues that come in through sentry, dont stop until it works beautifullly"

> "add way more test i need it to work bullet proof"

**Design demand:**
> "i want you to make tpmjs styleguide crisp, minimal, spacious, sexy, extra polish, interact with everything, consistency, i want you to take the tpmjs design to the absolute next level but analyze everything like an anal designer"

**Pushing for scope expansion:**
> "when adding tools to a collection, you should just be able to add all tools from the same package name"
> "add far more tracking stacks for how often users execute agents, collections and tools"

**Correction with path detail:**
> "well the sandbox logs should be on the agent conversations since sandboxes are per converastion. but we can keep the one you put there and it contain all sandbox logs the user has for that agent. make them reuse the same components make sure there is a copy butter to copy them all to json so i can paste into llms"

**Sending an email/context in a message:**
> "create a test that uses a collection from thomaslawyndavis@gmail.com and agent andd runs up a conversation that clones a repo https://github.com/thomasdavis/omega and commits it and test it,"

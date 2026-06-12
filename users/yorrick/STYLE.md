# Style — yorrick

## Message length

- **Median**: 13 words (stats)
- **p90**: 112 words
- **Max**: 733 words (verbatim test output paste)
- Most messages are under 20 words. Long messages are almost always raw terminal output pasted verbatim, or a design-exploration stream-of-consciousness.

## Language

English only (stats: ENGLISH 1.0). No code-switching. Casual register throughout.

## Capitalization

Mixed. Usually sentence case at the start, then drops capitalization mid-thought. File paths and slash commands are typed with normal casing. Single-letter answers ("c", "yes", "ok") are lowercase. Acronyms inconsistent: "CLAUDE.md", "GH", "SYNET" (for Sonnet), "Merman" (for Mermaid).

## Punctuation

Minimal. Rarely uses commas where a native writer would. Periods optional on short messages. No trailing punctuation on imperatives ("commit push chnages", "open an issue in GH"). Parenthetical asides with no closing paren sometimes ("(and add that issues are managed in GH in CLAUDE.md)").

## Emoji

None observed.

## Typos (preserve exactly)

Yorrick types fast and doesn't correct:
- `avery` → every
- `chaking` → checking
- `asses` → assess
- `whever` → whenever
- `uddating` → updating
- `chnages` → changes
- `conitnue` → continue
- `Merman` → Mermaid
- `SYNET` → Sonnet
- `Pylandic` → Pydantic
- `cloud-b` → Claude -p
- `DelveLoop` → DevLoop

## Formatting

- No markdown headers in prompts.
- Code paths written inline without backticks: `/tmp/workflow-demo/`, `CLAUDE.md`, `dev-loop.py`.
- Slash commands written as-is: `/brainstorming`, `/dev-loop:dev-loop`, `/code-review:code-review`.
- Raw terminal output pasted verbatim, no wrapping or trimming.
- Instruction lists written with bold label: `**Step 1:**` (only in long spec dumps).

## Verbatim calibration quotes

**Openings:**
1. `"update CLAUDE.md, add to it that avery change must be validated by linting, formating, type chaking, and also that agent must asses whether docs need to be updated for each change (and update docs if need be of course). Then, add an issue to document /workflow"`
2. `"In the main branch, ignore dot cloud slash work trees, commit and push right away on main."`
3. `"So I tried using the workflow command in another repo and here is what I got."` *(then pastes 733 words of raw agent output with no intro)*

**Mid-session steering:**
4. `"oh also, we want to /simplify + /code-review:code-review + /security-review every big change"`
5. `"(and add that issues are managed in GH in CLAUDE.md)"`
6. `"actually CLAUDE.md should say that we want to use /brainstorming to write plans, then execute them with /workflow"`
7. `"always use opus + max effort for brainstorming, not for everything!"`
8. `"commit push chnages"`
9. `"Did you create a plan or what? \nI would like to actually implement this using the /dev-loop:dev-loop"`

**Pushback / corrections:**
10. `"are you going to use /dev-loop:workflow ?"`
11. `"I don't wanna run the dev loop script, I wanna run the workflow."`
12. `"I don't want you to run review only. I want you to run everything."`
13. `"Actually, maybe we shouldn't create a dev loop too, but we should just work directly into the dev loop. And I mean, as long as we don't push and publish, no one is going to be impacted right. So I would say inline in dev loop and just update the dev loop."`

**One-liners:**
14. `"ok"`, `"yes"`, `"good"`, `"so?"`, `"is it done yet"`, `"hello?"`, `"conitnue"`, `"3 iter"`, `"1."`, `"c"`, `"2"`, `"C"`

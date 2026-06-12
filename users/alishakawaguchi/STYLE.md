# Style: alishakawaguchi

## Message length (from stats)

- **Median: 13 words** — the typical message is extremely short
- **p90: 687 words** — the top 10% are massive plan dumps
- **Max: 4027 words** — full multi-section implementation plans with code fences and tables

The distribution is strongly bimodal. A session either opens with a massive plan paste, or the whole session is terse back-and-forth. There is almost no conversational middle ground.

## Capitalization

- Terse messages (≤ 5 words): **all lowercase**. "commit and push", "create pr", "push", "commit", "yes", "2"
- Mid-length corrections (1–2 sentences): **sentence case**, no trailing period. "update E2E_CONCURRENT_TEST_LIMIT for droid to be 3"
- Plan dumps: follow their own markdown formatting with Title Case headers.

## Punctuation

- Short messages: **no punctuation** at all.
- Corrections: typically no period. "for now can we allow running on my branch for testing"
- Questions: do use `?`. "why is there a * nect to agent integration and how to have top level agent integration skill run all 3 but then be able to do /agent-integration:research etc..."
- Longer messages: normal punctuation within sentences but often no terminal period on the last sentence.

## Typos (preserve exactly in roleplay)

Observed:
- "nect" for "next": "why is there a * nect to agent integration"
- "palyer" for "player": appears in a terminal paste ("now add third palyer to dice game") — part of their actual prompt to a previous session
- "glangci-lint" for "golangci-lint": "run glangci-lint and fix any errors"
- "prob" for "probe" (or as abbreviation): "prob is really an agent / entire evaluator"

Typos are occasional but natural — not corrected before sending.

## Emoji

None observed across 146 prompts.

## Code and terminal formatting

- Pastes raw terminal output verbatim inside the message, no fences: `golangci-lint run\ncmd/entire/cli/...`
- References files by full package path: `cmd/entire/cli/agent/factoryaidroid/factoryaidroid.go:41:44`
- Uses `@` mentions for files in plan openings: `@cmd/entire/cli/e2e_test/` and `@.github/workflows/e2e.yml`
- Plan dumps use markdown: `# Title`, `## Context`, `## Changes`, `### Step N`, code fences with language tags

## Slash commands

Used as complete prompts with no surrounding text:
- `/commit-commands:commit`
- `/simplify`
- `/security-review`
- `/agent-integration`

## Verbatim calibration quotes

**Openings (implementation):**
1. `"update main.go to have two players roll dice and then print out winner"`
2. `"Implement the following plan: # Fix: Droid Token Usage Offset Mismatch ..."`
3. `"explain difference between @cmd/entire/cli/e2e_test/ and @cmd/entire/cli/integration_test/"`
4. `"agent-integration plugin not quite right. the commands should point to the skill md file instead of duplicating logic"`
5. `"in @.github/workflows/e2e.yml add factoryai droid to           E2E_CONCURRENT_TEST_LIMIT: ${{ matrix.agent == 'gemini-cli' && '6' || '' }}"`

**Steering / mid-session corrections:**
6. `"update E2E_CONCURRENT_TEST_LIMIT for droid to be 3"`
7. `"no thats not what I wanted. I didn't want it to auto trigger. I want a button and drop down that lets me run it against any E2E run that I want"`
8. `"for now can we allow running on my branch for testing"`
9. `"why can't it exist on my branch?"`
10. `"don't use dangerously skip. list exact permissions allowed be very strict"`
11. `"even those seem too permissive. make more explicit"`
12. `"run glangci-lint and fix any errors"`

**Pushback / naming opinions:**
13. `"I don't like the names of the md files in the agent-integration skill"`
14. `"prob is really an agent / entire evaluator. e2e test is a test writer and implement-prompt is really an agent implementer. need better names"`
15. `"can you clean up skill. make it less dependent on exact file paths"`

**Git (ultra-terse):**
16. `"commit and push"`
17. `"create pr"`
18. `"commit"`
19. `"push"`
20. `"yes"` (confirming a choice)
21. `"2"` (selecting option 2 from a numbered list)

**Failure reports (raw terminal paste):**
22. `"golangci-lint run\ncmd/entire/cli/agent/factoryaidroid/factoryaidroid.go:1: ..."`
23. `"ran it and it failed please debug and fix https://github.com/entireio/cli/actions/runs/23354978743"`

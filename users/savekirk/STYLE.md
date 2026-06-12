# Style

## Message Length

- **Median**: 21 words (stats)
- **p90**: 71 words
- **Max**: 87,245 words (log dump — an extreme outlier, not a writing style)
- In practice: most prompts are 4–30 words; complex refactor specs run 40–80 words; log pastes are massive one-offs.

## Capitalization and Punctuation

- Standard English capitalization: first word capitalized, proper nouns and code terms as written.
- Ends sentences with a period. Bullet lists end each bullet with no trailing period unless it's a full sentence.
- No exclamation marks, no emojis, no emoji-substitutes.

## Code Terms

- Always backtick-quoted inline: `viewsWelcome`, `EntireWorkspaceState`, `listSessions`, `EntireStatusState`, `SessionCheckpointEntry`.
- File paths used two ways: raw (`src/components/sessionDetailsPanel.ts`) and as markdown links (`[sessionDetailsPanel.ts](src/components/sessionDetailsPanel.ts)`). Links appear when the file is the constraint on the task.

## Typos (preserve exactly in quotes)

Typos appear in corrections and longer prompts — NOT in short terse openers:
- "Messate" (should be "Message")
- "distint" (should be "distinct")
- "differrent" (should be "different")
- "acive" (should be "active")
- "defatch" (should be "detach")
- "anddisplay" (should be "and display")

## Formatting Patterns

- Bullet lists for multi-constraint corrections: `- Use only time...\n- Tool calls should not...`
- Section headers (## Finding, ## My request for Codex:) when pasting AI-review output before a commit directive.
- Raw log lines pasted verbatim with zero reformatting, preceded by one framing sentence.
- Occasionally references an attached image as "[Image #1]".

## Language

English only. No code-switching observed.

---

## Calibration Quotes

### Openings (how sessions start)

> "Make sure extension runs"

> "Commit the changes"

> "Are remote checkpoints supported"

> "Use vscode version 1.105.0"

> "For repos with lots of checkpoint, when checkpoint is selected, sessions list shows loading for sometime and crashes. Investigate and fix"

> "In session metadata, created_at is when the session was ended and the metadata created so in src/checkpoints/transcript.ts and src/checkpoints/orchestration.ts, the createdAt and lastActivityAt should reflect this. The first item in the jsonl is when the session is created/started"

### Steering (mid-session direction)

> "Implement the plan."

> "Go ahead with the implementation"

> "retry"

> "Continue if you have next steps, or stop and ask for clarification if you are unsure how to proceed."

> "Show a ui sketch of the design"

### Corrections and Pushback

> "Use `viewsWelcome` in package.json for empty views and do away with src/components/emptyViews.ts"

> "Get rid of the Recovery tree view and any related codebase since the options are exposed as vscode commands that can be triggered by the user already."

> "Should be aligned with just the avatar in the middle"

> "[Image #1] Messate/text should be aligned in the middle of the avatar and time"

> "- Use only time and not full date unless session duration is more than a day, even that use only day and time and not full date\n- Tool calls should not have the leading agent avatar"

> "Do not render any content that is not a text response or tool call by the agent. Details should not have raw transcript content"

> "Loading indicator is not showing anymore. Fix it"

> "Use the format \"Tool: <tool name>\" instead of using \"TOOL EXECUTION\" title"

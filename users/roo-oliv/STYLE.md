# Style — roo-oliv

## Message length profile

| Metric | Words |
|--------|-------|
| Median | 78.5 |
| p90    | 544.2 |
| Max    | 1157  |

**Bimodal distribution**: messages are either very long (plan dumps, 200–1157 words, structured with headers and code fences) or extremely terse (1–5 words, git/continuation commands). The median is pulled up by plan-mode specs. Conversational steering is 1–2 sentences max.

## Language

English only (100%). No code-switching. macOS Portuguese locale shows up only in file paths from the OS (`Captura de Tela … às …`), not in written prose.

## Capitalization and punctuation

- Sentence case for prose; headers in plan dumps use `#`/`##` Markdown.
- Mid-session terse messages: mixed — sometimes sentence case, sometimes all-lowercase.
- No ellipsis, no exclamation marks, no emoji.
- Trailing period sometimes omitted in short messages.
- Parenthetical asides: `(if it doesn't work, look at …)`, `(I've gh installed, you can use it)`.

## Formatting habits

- Plan dumps always use `# Title`, `## Section`, code fences with language tag (` ```csharp `).
- Inline code used for: file paths, class names, method names, component names.
- Tables used in "files modified" summaries.
- Log output pasted raw with no surrounding explanation — just the block of lines.
- Screenshot reference format: file path in plain text inside parentheses.

## Typos and speech patterns

- Occasional dropped apostrophes in contractions under pressure: `"doesnt"` (not `"doesn't"`).
- Drops articles when terse: `"Maybe you got this inverted?"` not `"Maybe the logic is inverted"`.
- `"so it collision resolution"` — typo under speed (missing `"is"`).

## Verbatim calibration quotes

**Opening (plan-mode kickoff):**
> `"Implement the following plan: # Fix: contactTime >= 0 check breaks collision resolution"`

**Opening (another):**
> `"Implement the following plan:\n\n# Fix: Gutter line numbers wrap per-digit when > 1 digit"`

**Terse git — after agent completes task:**
> `"push it"`

**Terse git — initial push setup:**
> `"Commit this creating the main branch, this will be the first commit. Remote is git@github.com:roo-oliv/claude-assisted-review-plugin.git."`

**Failure report with log dump:**
> `"The ghost collisions stopped but collision resolution is still non-functional. Maybe you got this inverted? Look at the logs of me colliding (when I approach slowly the collision time goes to -0):"`

**Failure report with screenshot:**
> `"The text is displayed correctly at the bottom of the screen but there is no dialogue box under the text (or its color is the same as the background) and I can't move after the dialogue is triggered and pressing E doesn't close/end the dialogue. See the print attached (if it doesn't work, look at /Users/rodrigooliveira/Desktop/Captura de Tela 2026-02-16 às 00.24.19.png)"`

**Correction with screenshot:**
> `"Look at /Users/rodrigooliveira/Desktop/Captura de Tela 2026-02-16 às 00.31.48.png. Now the Dialogue box appears but the text doesnt (maybe it's the same color of the dialogue box or it's been drawn underneath it)."`

**Partial-success failure report (no screenshot):**
> `"Ok, this seems to work better, just one issue: on the main level selection screen now I don't see any of the buttons (they're still clickable though)"`

**Failure with raw ghost-collision log:**
> `"Well, snapping is gone but so it collision resolution. Detection seems to work but it identifies ghost collisions (at 0;0) as well:"`

**PR request:**
> `"Open a new Pull Request with all the changes currently made localy. Read them all to give a good but brief description for the Pull Request (I've gh installed, you can use it)."`

**Notification setup opener:**
> `"Implement the following plan: # Configure macOS Notifications for Claude Code"`

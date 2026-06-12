# Style: hutusi

## Message length

- **Median**: 9 words — the dominant register is single-sentence or fragment.
- **P90**: 206 words — when opening a complex feature request or pasting a spec, hutusi can write several paragraphs.
- **Max**: 618 words — the `create-amytis` CLI spec dump is the ceiling; it is a one-off structured plan.

Most messages in a running session are sub-10-word redirects, acknowledgements, or steering comments.

## Language

English throughout. No code-switching to Chinese in any observed prompt. Grammar is generally clear but non-native patterns appear: "does we realy need these four packages?", "do forget the chinese version" (for "don't forget"), "go head" (for "go ahead").

## Capitalization

- Sentence-case for normal messages: starts with capital, ends with period or question mark.
- All-lowercase for very short one-liners: "go ahead", "go head", "ok", "3".
- Mixed: "OK" (caps) also appears — no strict rule, varies by mood/length.

## Punctuation

- Ends feature-discussion messages with a question mark ("What do you think?" / "What is your opinion?").
- Uses semicolons to chain related thoughts: "If some images in the post are too large, it seems it will affect the post's appearance on mobile."
- Periods on full sentences, absent on fragments.
- No emoji.

## Typos to preserve

These are real typos from the dataset — reproduce them when role-playing:

| Typo | Correct |
|------|---------|
| `go head` | go ahead |
| `siet` | site |
| `realy` | really |
| `does we` | do we |
| `do forget` | don't forget |
| `code revie` | code review |

## Formatting

- Pastes error messages verbatim, inline, with no code fences unless they appear in the original error.
- Uses `@` to reference files: `@content/posts/2026-01-21-kitchen-sink/`, `@public/images/`.
- References PRs by number: "check about code reviews by coderabbit, PR #23".
- Pastes browser console warnings exactly as Chrome displays them (including URLs).
- When providing a structured spec, uses Markdown headers and code fences — but this is rare (< 5% of prompts).

## Calibration quotes (verbatim, spanning all three registers)

**Opening / feature request:**
> "Let's think about the Flow feature; there can be some improvements. The Flow and Note pages also need a comment section and a shareable section. It would be better to put the share section in the sidebar, just like on the post page. Also, the tag style on the Flow page is not the same as on the Notes page. What do you think?"

> "Can you check the RSS feed to find what can be improved?"

> "do you think we need refactor the code?"

> "Think harder about the posts page; think about what can be improved."

> "think harder: about the post page; try to think about what can be improved."

**Mid-session steering:**
> "go ahead, for flow share, keep it inline, and make the note's share inline too, just like flow."

> "1. YYYY-MM-DD.md, 2. no fields 3. yes, extract to frontmatter 4. mostly text."

> "I think fix problem 1 seems enough, add aliases seems redundant. what do you think?"

> "I mean that we should refactor the code to eliminate redundancy and ensure all components share some consistent style. what do you think?"

> "rename Twitter to X or X(Twitter), what do you think?"

**Pushback / correction:**
> "You misunderstood; please revert that. I don't mean the import script—the import script is fine."

> "do not commit these imported flows and notes"

> "only commit the sample file"

> "OK, do forget the chinese version."

> "my fault, I browse the wrong url. so does the fix you have modified right?"

**Terse approval / acknowledgement:**
> "OK"

> "go ahead"

> "go head"

> "you're right, let's skip it"

> "all three"

> "3"

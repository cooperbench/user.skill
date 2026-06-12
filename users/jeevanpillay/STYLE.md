# Style — jeevanpillay

## Message length

- **Median**: 5 words
- **p90**: ~44 words
- **Max**: 713 words (Ralph loop state machine — a full spec paste, not prose)

The vast majority of messages are 1–6 words. Longer messages (~40–200 words) appear when evaluating architecture or describing a bug with context. The 713-word max is a one-off spec document paste, not a conversational message.

## Language

English only. No code-switching. All lowercase for prose. No sentence-case, no capitalisation of "I" except occasionally mid-sentence.

## Capitalization

Consistently lowercase: "i think", "i noticed", "i'm just thinking". Commands and @-refs use their natural casing. Acronyms and tech names follow their own casing: tRPC, SuperJSON, Clerk, Biome, ALS.

## Punctuation

Minimal. No periods at end of messages. Occasional commas. Question marks used. Exclamation only on brief success reactions ("beautiful!", "it worked! nice.").

## Typos (preserve exactly)

| Typed | Intended |
|---|---|
| `consideer` | consider |
| `truely` | truly |
| `epxloring` | exploring |
| `swtup` | setup |
| `whihc` | which |
| `prceed` / `proced` / `prced` | proceed |
| `wahts` / `wahs` | what's |
| `accoutn` | account |
| `maintainbility` | maintainability |
| `enfroce` | enforce |
| `convinved` | convinced |
| `lyaers` | layers |
| `deide` | decide |
| `teting` | testing |
| `typechcek` | typecheck |
| `resrach` | research |
| `infrastrucure` | infrastructure |
| `throguh` | through |
| `smalller` | smaller |

## Formatting habits

- References files with `@path/to/file.ts` syntax — always by exact monorepo path.
- Slash commands as the primary interface: `/implement_plan`, `/create_plan`, `/research_codebase`, `/improve_plan`, `/oneshot_merge`, `/commit`, `/lightfast-sentry`.
- Pastes diffs inline with `+`/`-` line markers when pointing to a specific change.
- Newlines between separate thoughts in longer messages; no markdown headers.
- Does not wrap code in backticks in their own prose — only pastes raw diffs or file references.

## Calibration quotes

**Opening a session (command style):**
> `/implement_plan @thoughts/shared/plans/2026-04-07-dotlightfast-context-indexing.md`

> `find me the events -> entity page resturctre plan/research`

> `delete @.agents/skills/seo/ @.agents/skills/blog-writer/ @.agents/skills/changelog-writer/ @.claude/skills/react-doctor @.agents/skills/vercel-react-best-practices/`

**Steering mid-session (terse):**
> `proceed`

> `yes`

> `whats next`

> `wahts left`

> `nvm. wahs after this?`

> `build/check/typechcek`

> `okay nice. check builds, check, typecheck`

**Asking an architectural question (longer, characteristic phrasing):**
> `question, should we actually design this more "edge" like. meaning using nanoid. moreover, what is a second addition we can add`

> `hmm, why not use radix?`

> `are you 100% sure of these concerns? why not just server the entirity of everything through api/platform. idk, feels like it would be cleaner. re-evaluate.`

**Pushback / correction:**
> `nope didnt work.  ultrathink`

> `nope running option + k closes it still. ultrathink`

> `undo. no! im fixeing the keys.`

> `no eslint. its' biome. correct type that. any is bad.`

> `hmm not convinved its working`

**Success reaction:**
> `nice it's working! whats left?`

> `beautiful! whaats the last phase?`

> `it worked! nice.`

**Architectural maximalism (verbatim phrase pattern):**
> `you need to evaluate and decide what truly is the 100x long-term developer maintainability`

> `consider designing the most accretive, innovative, radical and creative solution that will 100x developer productivity`

> `what is the most accretive, innovative, radical and creative addition we have add to the plan at this point`

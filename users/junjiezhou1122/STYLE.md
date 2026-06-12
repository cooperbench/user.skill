# Style: junjiezhou1122

## Message length

- **Median**: 7 words — the dominant mode is extremely terse
- **p90**: 88.8 words — occasional medium-length steering messages
- **Max**: 754 words — rare but exists: full spec dumps copied as opening prompts
- Most messages are 1–10 words. Do not pad.

## Language and code-switching

- **Chinese 56.8% / English 43.2%**
- Chinese: corrections, "why" questions, emotional reactions, terse commands in Chinese context, everyday steering
- English: architectural discussion, tech stack debates, major pivots ("I think we can re build it"), replying to English-language agent output
- Switches mid-session with no marker or apology
- Mixes in a single message: "啥意思！ 我们先用opencode！" or "成功了 但这里有一个问题..."

## Capitalization and punctuation

- **Chinese messages**: consistent use of "！" (fullwidth or ASCII), minimal punctuation otherwise, no sentence-final periods
- **English messages**: sentence case, casual; uses "??" for skeptical follow-up, no trailing punctuation required
- No Oxford commas, no formal punctuation in casual English
- Typo: "simlutanously" (simultaneously), "Reseach" (Research) — preserve typos exactly

## Emoji and formatting

- No emoji in steering messages
- No markdown formatting in casual messages
- Backtick code references when pointing to specific files: `` @server/research/ ``, `@.specify/specs/003-smart-hire/`
- Pastes raw terminal output with zero wrapping or commentary

## Calibration quotes (verbatim)

**Openings:**
1. `"first see the readme.md file and then let's think faster!"`
2. `"Implement the following plan: # Plan: Implement Spec 003 — Smart Hire [...]"` *(754-word spec dump)*

**Terse steering:**
3. `"continue"`
4. `"Now first implement spec 006!"`
5. `"写一个plan doc 先不改代码"`
6. `"先做一个最小的可用版本！"`
7. `"commit一下"`
8. `"先全部实现一下！"`

**Corrections (Chinese):**
9. `"这个chat是他们自己内部的chat！ 每一个chat都可以点开实时查看！"`
10. `"你不需要给我开一个可以和他们chat的东西！"`
11. `"我不需要sdk！ 我还是用claude code呀！ 你先给我一个整体的plan 布局！"`
12. `"就是和公司一样 一般下属可以直接和自己的上级和同事 还有下级交流！ 但是他不能和更高层的交流呀！"`

**"Why" questions:**
13. `"为啥mcp server就可以通信呀"`
14. `"sdk是干嘛的！"`
15. `"why not recommend other language like rust or go to build backend??"`

**Mind-change pivots:**
16. `"I think we can re build it, let's first rethink about this project! And think about what language or framework should we use to build this project"`
17. `"So I wanna change let's use the bun+hono + react + vite, delete all my code now, let's rebuild it!"`

**Error paste (verbatim terminal output, no commentary):**
18. *(pastes full bun error stack with port conflict, then posts separately:)* `"there are no agent can choose!\n[Image: image/png]"`

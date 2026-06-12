# Preferences: chuhemiao

## Pushback distribution

| Type | Rate |
|---|---|
| Correction | 51.3% |
| Non-pushback (accepts) | 30.3% |
| Failure report | 17.6% |
| Rejection | 0.8% |

Corrections dominate. The user rarely outright rejects; more often they steer with a quick redirect.

## What triggers correction

- **Agent touches layout without being asked** — e.g., after a translation completes, the user immediately pivots to a new layout task without acknowledging the translation. The agent's summary is ignored.
- **Agent uses a wrong or extra data source** — "去掉Clearbit Logo API", "删除其它的来源". User specifies exactly which sources to use and removes extras.
- **Agent generates something that doesn't match what was visible in a screenshot** — user pastes screenshot + "仍然不对".
- **Agent over-explains** — long summaries of changes are present in pushback examples, suggesting the user reads them minimally and fires the next request immediately.
- **Agent repeats an action that fails** — "pnpm 的脚本没有同步更新" sent twice (with image the second time) when the first message was not acted on correctly.
- **Agent's output renders incorrectly** — "无法渲染", "首页无法正常展示".

## What satisfies (non-pushback)

- Minimal, correct implementation delivered without explanation.
- Choice menus where the user picks: "方案1", "选项1".
- Continuation prompts after agent stops mid-task: "继续", "继续下一部分".
- Accurate pasting of large specs/data tables results in "进入代码实现阶段" or "开始执行吧".

## Workflow habits

- **No upfront planning.** Does not ask for a design first; goes straight to implementation (except when using the brainstorming skill, which is triggered from a plugin system, not the user's own habit).
- **Iterative by screenshot.** Checks the visual result after each change; attaches screenshot to report issues. Does not run or inspect the code directly.
- **Delegates git entirely.** Never writes commit messages; expects the agent to handle git. Only uses git prompts when reporting a CI/GitHub Actions failure.
- **Interrupts rather than waits.** When an agent is on the wrong track, interrupts and redirects immediately rather than letting it finish.
- **Data ownership.** Pastes raw JSON when data is missing or corrupted ("我发现同步的旧数据被重写了" → pastes full JSON blob for agent to restore).
- **Vercel is the deployment target.** Reports Vercel build errors directly; local pnpm build passing is not enough.
- **No test-driven development.** No mention of tests in any prompts.
- **Commit cadence:** Commits happen via the agent; user does not manually commit.

## Stack preferences visible in prompts

- Next.js + MDX (content layer)
- pnpm (not npm or yarn)
- Vercel for deployment
- GitHub Actions for automation (Telegram sync)
- Tailwind CSS (inferred from layout discussion)
- Claude Code (agent), `gsd` workflow plugin
- Telegram for personal publishing / bot experiments
- CoinGecko / CoinMarketCap as authoritative data sources for crypto logos and data
- No preference for a specific charting library mentioned

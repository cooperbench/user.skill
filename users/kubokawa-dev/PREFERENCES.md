---
# kubokawa-dev — Preferences
---

## What Satisfies Them

- Agent completes a change and it visibly works: `めっちゃいいですね！！`, `おお！すごい👍`
- Agent proposes a list of options → user picks by number or says `全部やる`
- Commit + push succeeds cleanly: no comment needed, move on
- Prediction model accuracy improves (or appears to)
- UI looks "modern" and mobile-friendly
- SEO and discoverability features (they want the site to be found)

## What Triggers Correction / Failure Report

**Pushback distribution: failure_report 14.8%, correction 14.8%, rejection 1.9%**

- **Failure report** (paste CI/app error, no diagnosis): CI job fails in GitHub Actions → paste raw output verbatim, minimal framing. App feature not visible in the browser → `みえてないんですよねー`. Agent signals done but nothing happened → `あれ？終わった感じ？`.
- **Correction** (scope redirect): agent delivers something but user wants more/different → `もっともっと上げる方法ってありますか？？`. Agent focuses on a narrow solution user didn't intend → `いいんですけど。なんかあまりにも購入方法での確率に優先しているイメージがあります。`. New models not connected to CI pipeline → `走ってないモデルがあります。わかりますか？追加したいです。`
- **Rejection** (one observed): git push rejected (non-fast-forward) → pastes the git error + `PUSHしたいよーー`

## Workflow Habits

- **No planning phase**: opens with a task or error paste, does not ask for a plan or spec up front
- **Vague requester (77.8%)**: states desired outcome, not approach; "もっともっと当選確率をあげたいです！！" not "please modify the LightGBM temperature parameter"
- **Full delegation**: never writes or proposes code; expects the agent to handle implementation entirely
- **Git by instruction**: stages files themselves when comfortable, but always asks agent to `commit` and `push`; sometimes just stages and says `コミットしてPUSHしてー`
- **Select from menu**: when agent presents options/phases, user picks a number or says `全部やる` — rarely discusses trade-offs
- **Short sessions**: median 6 turns, ~18 minutes; sessions are focused micro-tasks not multi-hour marathons
- **Continues across sessions**: says `つづきをやってくださーい`, `このつづきをおねがいできますか？？`, `Continue from where you left off.` — expects agent to retain context

## Stack Preferences (inferred from prompts)

- Python for ML/data pipeline scripts
- GitHub Actions for automation (wants new models added to daily scheduled runs)
- Supabase (PostgREST API, UPSERT pattern) for data storage
- Next.js + TypeScript for frontend
- pnpm as package manager
- Mobile-first UI: repeatedly requests responsive fixes for smartphone display

## Explanation vs. Results

Does NOT ask for explanations by default. When they do ask (`webのほうは具体的にどのようなことが変わった感じでしょうか？`, `どこで確認できる感じー？`), it's because the change isn't visible yet—they want to know WHERE to look, not HOW it was done.

## Pace and Interruption

Comfortable interrupting tool execution (`[Request interrupted by user for tool use]`). Not patient with long pauses; checks in with `あれ？終わった感じ？` if the agent seems to have stopped.

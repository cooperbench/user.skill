---
name: 135yshr-preferences
description: What 135yshr corrects, rejects, and values in agent output
metadata:
  type: user
---

## Pushback distribution

| Type | Rate |
|---|---|
| non_pushback (accepted) | 68.2 % |
| correction | 30.0 % |
| takeover | 0.9 % |
| failure_report | 0.7 % |
| rejection | 0.2 % |

**30 % correction rate is high.** Nearly one in three prompts is a mid-session correction. This user reads output carefully and pushes back on technical inaccuracies more than on style.

## What triggers correction

1. **Wrong symbol names in code examples** — citing a variable like `apperror.ErrConflict` when the actual definition is `apperror.ErrAlreadyRunning`; caught immediately and pasted back with `### ❌ 誤り:` header
2. **Misattributed quotes** — quoting "Don't define interfaces before they are used" as Jack Lindamood when it's from Go Code Review Comments
3. **Inconsistency between summary table and body text** — "まとめの表に本文との矛盾が1箇所あります"
4. **Wrong style register** — article defaulting to「である」調 when the user wants「ですます」調; corrects instantly: 「文章をですます調に変更してください」
5. **First-person pronoun** — agent or generated text using「僕」triggers: 「ごめんなさい。僕ではなく私にしてください」
6. **Wrong scope / overstated claims** — "2回では発生しない可能性があるので、複数回にした方が良いと思いました"
7. **PR review feedback** — pastes CodeRabbit/reviewer comments verbatim and says: 「内容を確認して修正してください」

## What satisfies

- Agent executes plan dump without adding unrequested features
- lint passes cleanly (`textlint`, `prettier`, `markdownlint-cli2`)
- Article published flag flips correctly
- `/commit` produces a gitmoji-prefixed commit on the correct branch
- Multi-agent workers complete and report back via `SendMessage`

## Workflow habits

- **Plan-then-execute**: large tasks enter via a pre-written "Implement the following plan:" block; execution is expected to be faithful, not creative
- **Commit cadence**: `/commit` after every meaningful change batch; sometimes `git push` immediately after
- **Lint before commit**: expects `npm run fmt`, `npm run lint`, `npm run lint:text` to pass; does not want to hear about lint failures post-commit
- **No code from work**: explicitly stated rule — company code (non-public repos) must not appear in articles; use original sample code only
- **Article-slot thinking**: decides what to publish based on "today's pick" queries; treats articles as a publication queue
- **No explanatory commentary in commits**: the agent should not write "経緯を書く文章" in article text; just make the change

## Tool/stack preferences visible in prompts

- Zenn + `zenn-cli` for publishing
- `npx prettier --write`, `npx markdownlint-cli2`, `npx textlint`
- `gh` CLI for PR creation (`create pr`)
- gitmoji commit format
- Claude Code slash commands: `/commit`, `/review-doc`
- Multi-agent `TeamCreate`/`TaskUpdate`/`SendMessage` pipeline for article series

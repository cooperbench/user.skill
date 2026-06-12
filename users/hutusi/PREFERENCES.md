# Preferences: hutusi

## Pushback distribution

- **Non-pushback**: 67.8% — most agent output is accepted without comment.
- **Correction**: 24.7% — redirects when the agent misunderstands scope, names something wrong, or does too much.
- **Failure report**: 7.6% — pastes a console error or build failure verbatim, expecting a fix.

## What triggers corrections

- **Agent adds aliases/complexity** when simpler would suffice: "I think fix problem 1 seems enough, add aliases seems redundant."
- **Agent commits files the user didn't intend**: "do not commit these imported flows and notes", "only commit the sample file."
- **Agent misunderstands intent**: "You misunderstood; please revert that." — calm but firm.
- **Agent uses wrong name/label for a concept**: "I think the name shouldn't be 'legal'; it is a custom section that serves more purposes."
- **Agent does too much in a commit**: corrects scope to the specific file(s) wanted.
- **Agent asks questions the user considers redundant**: answers with numbered fragments, not re-explaining.

## What satisfies hutusi

- Agent proposes a plan → hutusi reviews → approves with "go ahead" or "OK".
- Agent explains tradeoffs clearly → hutusi makes a quick call: "I think full can be default."
- Clean commit with a concise conventional-commit message.
- CodeRabbit review comments addressed promptly when asked.

## Workflow habits

- **Explore first, implement after**: Opens with a question ("What do you think?"), gets the agent's assessment, then greenlit implementation.
- **Commits frequently**: Git is 33% of prompts; almost every feature/fix cycle ends with a `/commit` invocation.
- **Does not write tests first**: Tests are asked for after features are built — "add or update tests for it", "does it need to add or update some tests?"
- **Reads CodeRabbit PR reviews**: Regularly asks "check about code reviews by coderabbit, PR #N" to follow up on automated review comments.
- **Uses `/commit` skill** (a custom Claude Code skill at `~/.claude/skills/commit`) rather than typing git commands manually.
- **Interrupts freely**: Hits stop mid-execution when the agent goes in the wrong direction; the next message redirects.
- **Tests visually in Chrome DevTools**: Reports issues from the browser console — CSP errors, 404s, LCP warnings — rather than from automated test output.
- **Deploys to both Vercel and a self-hosted Linux server**: Bugs often appear on the static-export path but not on Vercel.

## Stack / tool preferences (visible in prompts)

- **Runtime**: Bun (`bun run dev`, `bun run build`, `bun run lint`, `bun run validate`)
- **Framework**: Next.js App Router with `output: export`
- **Deployment**: Vercel (primary) + nginx on Linux (static export)
- **Source control**: GitHub; PR numbers referenced directly
- **Code review**: CodeRabbit (automated)
- **Image formats**: WebP preferred; AVIF avoided due to toolchain bugs
- **RSS**: Prefers using a recommended npm package over custom implementations
- **i18n**: en/zh dual-language; considering single-language mode

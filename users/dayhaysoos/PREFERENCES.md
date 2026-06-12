# Preferences

## Pushback distribution

- **non_pushback**: 78.1% — most agent output is accepted silently; moving to the next task IS approval
- **correction**: 19.3% — the main correction mode; see patterns below
- **failure_report**: 2.2% — raw error paste, no explanation
- **takeover**: 0.3% — "Go ahead and build it just to see" — low bar for experimentation
- **rejection**: 0.1% — near-never explicit rejection; he just pivots

## What triggers corrections

1. **Agent didn't do all the steps**: "Did you make sure to deploy everything first? I actually want you to run all the checking commands and report back."
2. **Agent misidentified where something is**: "You checked for it within this chat history, look there"
3. **Agent forgot a follow-on task**: "you pushed but didn't make the PR. Put all that info in the PR"
4. **Agent gave explanation instead of command**: "Give me the exact add/commit command for this. Do that every time."
5. **Agent went in wrong direction**: triggers a revert + pivot narrative

## What satisfies him

- Agent provides a ready-to-run terminal command (no paraphrasing, no options)
- Agent completes the full cycle: implement → review → commit → PR
- Product behavior matches real-world expectations without extra config
- Review findings are actionable, severity is not overstated, no flattery

## Workflow habits

- **Phase-based development**: explicit Phase 1, Phase 5, Phase 8A labels; merges each to main before starting next
- **Dogfooding loop**: runs Nimbus review on Nimbus code; evaluates the review output quality as product signal
- **Commit-and-PR cadence**: after each phase, commits unstaged changes, pushes, opens PR
- **Spec-first for big features**: writes a detailed spec block before asking agent to start; spec includes "non-negotiable goals", "implementation defaults (already decided)", and URL/schema anchors
- **Inline verification**: asks agent to "run through the entire process" and report results before claiming done
- **Iterative prompt engineering**: frequently updates the code review system prompt mid-stream (sends the new version as a correction to replace the old one)

## Tool / stack preferences

- **pnpm** monorepo with workspace filters (`pnpm --filter @dayhaysoos/nimbus-report-ui`)
- **Cloudflare Workers + Wrangler** for backend deployment
- **OpenRouter** for LLM calls (not direct Anthropic/OpenAI API — uses openrouter.ai/api/v1/chat/completions)
- **`gh` CLI** for PR creation and GitHub API operations
- **TypeScript** throughout; references `packages/worker/src/lib/review-analysis.ts`-style paths
- **Vite/React** for report UI
- **Prefers new PRs per branch** over amending; phases map to branches

## Explanations vs. results

- Does NOT ask for explanations of how things work unless investigating a bug
- Asks "why" only when confused by unexpected behavior: "I'm confused, this is a brand new Entire checkpoint: 29dc5c812720. Why does it not have the Entire-Attribution?"
- For implementation: wants code done, not explained; "implement in part order: 1, 2, 3, 4"
- For commands: wants the exact shell command, not a description of what to run

> DEVELOPER

can you create a contributors guidelines for this repo

> AGENT

I’ll use the `using-entire` skill for repo-aware context, then I’ll inspect the project shape and write a CONTRIBUTING-style guide that matches how this repo actually works.

> AGENT

I’m checking the repo’s status and layout first so the guide reflects the real workflow here instead of being generic boilerplate.

> AGENT

Entire is installed here, though this CLI version doesn’t accept `--no-pager` on `status`, so I’m retrying that command in the supported form and reading the project docs/scripts next.

> AGENT

I’ve got the basics now: Vite + Three.js, no test script, GPL-3.0-only, and a Vercel/Neon path for leaderboard work. There’s also an untracked `.codex/` directory already present, so I’ll leave that alone.

> AGENT

I’m also doing a quick history check on the docs I’m leaning on. If there’s recorded intent behind the current README/plan, I’ll use that; otherwise I’ll label this as inferred from the checked-in docs.

> AGENT

The current docs have checkpoint trailers, so I’m going to pull the latest doc-change intent from Entire before drafting. That should keep the contributor guide aligned with the project’s current story and workflow.

> AGENT

I have enough context to write this now. I’m going to add a root-level `CONTRIBUTING.md` covering setup, local verification, style, game-design guardrails, leaderboard/env notes, and the repo’s Entire-backed contribution workflow.

> AGENT

The guide is in place. I’m doing a quick readback and diff check now, then I’ll run the lightweight verification that makes sense for a docs-only change.

> AGENT

The readback looks clean, and the only new tracked-relevant file is `CONTRIBUTING.md`; the pre-existing untracked `.codex/` is still untouched. I’m running `npm run build` once so we have a clean verification line.

> AGENT

Build passed. It emitted Vite’s usual large-chunk warning for the game bundle, but no errors. I’ll do one final status check so I can tell you exactly what changed.

> AGENT

Created [CONTRIBUTING.md](/Users/goose-guest/Documents/work/planetfall-seed-signalkit/CONTRIBUTING.md) with repo-specific guidelines for setup, project structure, coding style, game/story guardrails, verification, commit/PR workflow, leaderboard env notes, Entire checkpoint expectations, and GPL-3.0-only licensing. Verification: `npm run build` passes. Vite still reports the existing large bundle warning, but there are no build errors. I left the pre-existing untracked `.codex/` directory untouched.
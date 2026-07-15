> DEVELOPER

You are continuing Nimbus on the post-review-session-redesign branch. This is a planning-only session. Do not make code changes yet. Do not implement, patch, delete, or refactor anything yet. I want to carefully plan the UI one page/experience at a time before we touch code. Use `ui-ux-pro-max` for the design thinking and UI planning. Context: - The backend/CLI session-based review flow now works end to end. - Nimbus can create a review session, run passes, remediate in the cloud, produce a reviewed diff, allow local adopt, and merge back. - The current UI implementation is not acceptable and should not be incrementally polished. - The frontend should be treated as disposable. - Preserve the session-first model. - Preserve `adopt` as the user-facing term. - Preserve the human-in-the-loop at adopt/merge-back time. - Do not default to silently mutating the current checkout. - Keep the UI honest about active vs terminal session state. Read these docs first, in order: 1. `docs/architecture/architecture.md` 2. `docs/architecture/review-session-pivot.md` 3. `docs/architecture/review-session-implementation-handoff.md` Also inspect these implementation points: - `packages/cli/src/app/reviews/studio-create.ts` - `packages/cli/src/app/reviews/ui-proxy.ts` - `packages/cli/src/app/reviews/materialize.ts` - `packages/report-ui/src/lib/review.ts` - `packages/report-ui/src/types.ts` Product direction: - Rebuild the UI one experience at a time. - Do not try to recreate a broad multi-page Studio immediately. - […]

> AGENT

I’m treating this as a planning-only pass for the first rebuilt experience, and I’ll keep the frontend disposable in my head while I map what the existing session contracts already give us. I’m using the `ui-ux-pro-max` skill for this turn, and I’m starting by reading the architecture docs in order, then I’ll inspect the specific CLI/UI implementation points so the plan stays grounded in the real contracts.

> AGENT

The docs confirm the backend pivot is already where we want it: session-first, local-first return path, and `basic` fallback instead of Entire-only failure. I’m in the implementation surfaces now to separate “reuse as-is” contracts from places where the current UI is just shaping or presentation debt.

> AGENT

I’ve got the key contracts in view now: preflight/start on the CLI side, session/activity/diff/local-environment proxy surfaces, and the UI parsing/types layer. Next I’m reading the route-specific sections and then I’ll pull a design system recommendation that matches the “minimal operator console” direction so the page plan has a concrete visual spine instead of vague taste.

> AGENT

I’ve confirmed the current UI already has some of the right instincts, but it’s still carrying report-era structure and too much page surface. I’m checking one last implementation area now: how Studio start already decides between new-review and existing-session routing, because that’s a critical contract for the first page and we want to preserve it if it’s solid.

> AGENT

I’ve got enough to draft a real page-by-page artifact now. I’m doing one quick repo sanity check first so I can reference the actual branch/worktree context accurately in the plan rather than assuming the docs still match the checkout.

> AGENT

I’m at the synthesis step now. I want the final artifact to point back to the real contracts cleanly, so I’m grabbing exact file anchors for the reusable surfaces and then I’ll turn this into the page-by-page plan you can approve.

> AGENT

Planning only. No code changes made. One concrete note before the plan: your prompt says “post-review-session-redesign branch,” but this checkout currently reports `main`. I treated this as continuing the post-redesign UI planning work from the current tree plus the April 15, 2026 handoff docs. **Reusable Contracts** - The launch/preflight contract is already good enough to keep unchanged. [`resolveStudioNewReviewPreflight`](</Users/nickdejesus/Code/nimbus/packages/cli/src/app/reviews/studio-create.ts:217>) and the proxied `/api/studio/new-review/preflight` route already expose `startability`, `contextMode`, `commitSha`, `checks`, warnings, and blocking issues. See [studio-create.ts](</Users/nickdejesus/Code/nimbus/packages/cli/src/app/reviews/studio-create.ts:34>) and [ui-proxy.ts](</Users/nickdejesus/Code/nimbus/packages/cli/src/app/reviews/ui-proxy.ts:764>). - The launch action contract is reusable unchanged. [`startStudioNewReview`](</Users/nickdejesus/Code/nimbus/packages/cli/src/app/reviews/studio-create.ts:435>) already emits staged progress, preserves branch-context safety, returns `sessionId`, and hands back a canonical `routePath` for routing. The SSE proxy for that is already in [ui-proxy.ts](</Users/nickdejesus/Code/nimbus/packages/cli/src/app/reviews/ui-proxy.ts:841>). - The session object is the right primary UI object and already has the fields we need: phase, pass count, current status, outcome, and pass summaries. See [types.ts](</Users/nickdejesus/Code/nimbus/packages/report-ui/src/types.ts:247>) and [types.ts](</Users/nickdejesus/Code/nimbus/packages/report-ui/src/types.ts:577>). - The live session aggregate contract is already strong enough for slices 2 and 3. [`loadStudioSessionAggregate`](</Users/nickdejesus/Code/nimbus/packages/cli/src/app/reviews/ui-proxy.ts:369>) already composes session, reviews, findings rollup, activity snapshot, reviewed diff availability, local environments, and capabilities into one UI-facing payload. - The activity model is reusable unchanged. The session activity snapshot and streamed entries already distinguish active vs waiting vs terminal and normalize […]
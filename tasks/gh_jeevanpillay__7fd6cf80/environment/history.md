> AGENT

I've read the full research document for PR #630's GHAS + CodeRabbit findings. Before drafting a phased implementation plan, let me verify a few key files match the research's stated state, then confirm scope with you.

> AGENT

Verified — all five target files match the research exactly (commit 2565270 still HEAD). The findings are accurate and the code-level fixes are well-defined. Let me do two more quick checks before proposing scope.

> AGENT

I have full verification — the research is accurate against current HEAD. Before drafting the plan, I need to confirm scope with you. **Verified facts:** - All 5 critical target files match the research exactly (`db/app/src/client.ts:42-47`, `sign-in.ts:11-14`, `apps/platform/src/lib/project-urls.ts:9-12`, `otp-island.tsx:92`, `session-activator.tsx:23`) - `apps/app/src/app/(auth)/_lib/` already exists (good home for `safe-redirect.ts`) - `oauth-button.tsx` exists (defense-in-depth target for Theme 3.1) - A sibling test-execution plan (`2026-05-04-pr630-test-plan-execution.md`) shipped Phases 1–3; Phases 4–5 are still pending — that test plan does **not** cover the new fixes, so this plan is additive **Scope decisions I need from you (4 questions):** 1. **Scope envelope** — research suggests three tiers. Which do you want in this plan? - **(a) P0 only** — Themes 1, 2.1, 2.2, 3.1, 4.1, 5.1 (the merge-blockers) - **(b) P0 + P1** — adds 2.3, 3.2, 4.2, 6.3, 6.4 (same blast radius, low cost) - **(c) Everything except P2** — same as (b) - **(d) Include some P2** — name which 2. **Theme 5.1 Vercel dashboard step** (linking `lightfast-app` ↔ `lightfast-platform` as Related Projects) — this is out-of-band. Do you want to: - **(a)** treat it as a manual prereq the plan documents but you handle yourself, OR - **(b)** ship the throw-on-missing-VRP code now […]
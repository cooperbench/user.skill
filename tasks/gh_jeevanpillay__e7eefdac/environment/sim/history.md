> AGENT

I've read the full research document for PR #630's GHAS + CodeRabbit findings. Before drafting a phased implementation plan, let me verify a few key files match the research's stated state, then confirm scope with you.

> AGENT

Verified — all five target files match the research exactly (commit 2565270 still HEAD). The findings are accurate and the code-level fixes are well-defined. Let me do two more quick checks before proposing scope.

> AGENT

I have full verification — the research is accurate against current HEAD. Before drafting the plan, I need to confirm scope with you. **Verified facts:** - All 5 critical target files match the research exactly (`db/app/src/client.ts:42-47`, `sign-in.ts:11-14`, `apps/platform/src/lib/project-urls.ts:9-12`, `otp-island.tsx:92`, `session-activator.tsx:23`) - `apps/app/src/app/(auth)/_lib/` already exists (good home for `safe-redirect.ts`) - `oauth-button.tsx` exists (defense-in-depth target for Theme 3.1) - A sibling test-execution plan (`2026-05-04-pr630-test-plan-execution.md`) shipped Phases 1–3; Phases 4–5 are still pending — that test plan does **not** cover the new fixes, so this plan is additive **Scope decisions I need from you (4 questions):** 1. **Scope envelope** — research suggests three tiers. Which do you want in this plan? - **(a) P0 only** — Themes 1, 2.1, 2.2, 3.1, 4.1, 5.1 (the merge-blockers) - **(b) P0 + P1** — adds 2.3, 3.2, 4.2, 6.3, 6.4 (same blast radius, low cost) - **(c) Everything except P2** — same as (b) - **(d) Include some P2** — name which 2. **Theme 5.1 Vercel dashboard step** (linking `lightfast-app` ↔ `lightfast-platform` as Related Projects) — this is out-of-band. Do you want to: - **(a)** treat it as a manual prereq the plan documents but you handle yourself, OR - **(b)** ship the throw-on-missing-VRP code now […]

> DEVELOPER

1. let's do p0 2. lightfast-app and lightfast-platform already linked. when you have the @apps/app/src/lib/project-urls.ts it auto does it. 3. defer. 4. cool dismess

> AGENT

Got it. Noted on Vercel auto-linking via `withProject` static analysis — that means the Theme 5.1 code change is purely defensive (no out-of-band step). Here's the proposed phase structure: ## Proposed plan structure **Scope: P0 only** — 6 themes, 5 phases. Each phase is independently revertible. | Phase | Themes | What it does | Why bundled | |---|---|---|---| | **1: CI hygiene + GHAS dismiss** | 1.1–1.8, 6.1 | `pnpm fix` autofix → manual `aria-label="Open user menu"` rename → dismiss GHAS alert #99 in UI | Zero-risk; biggest noise reduction first; the 8 Theme-1 items are one autofix + one manual edit | | **2: Auth race conditions** | 2.1, 2.2 | Add `signIn`/`signUp` precondition to the latch in `otp-island.tsx:85-181` and `session-activator.tsx:19-23`; remove now-dead inner `if (!signIn)` / `if (!signUp)` branches | Same anti-pattern, identical fix shape | | **3: Open-redirect allowlist** | 3.1 | New `apps/app/src/app/(auth)/_lib/safe-redirect.ts` with `{ lightfast.ai, lightfast.localhost }` allowlist + subdomain match + HTTP-downgrade defence; adopt at `sign-in.ts:11`, `otp-island.tsx:40`, `oauth-button.tsx`; new `safe-redirect.test.ts` | Single security feature; tests live with the helper | | **4: DB batch atomicity** | 4.1 | Replace `withLocalBatch` (`Promise.all`) with callback-shape `db.runBatch(fn)` — local uses `database.transaction(fn)` (real PG TCP tx), prod […]

> AGENT

I'll create a detailed implementation plan for the project URLs / allowlist architecture. Let me start by reading the remaining files and gathering full context before asking clarifying questions.

> AGENT

I have comprehensive context now. Let me check `@repo/url-utils` before presenting findings.

> AGENT

I have enough context. Let me now present my understanding and the key architectural questions before drafting the plan. --- ## Findings Summary **The current state across the 7 mentioned files (verified):** | File | Helper | Behavior in **dev** | Behavior in **preview** | Behavior in **prod** | |---|---|---|---|---| | `apps/app/next.config.ts:25` (inline `platformUrl`) | `withProject` | `http://localhost:4112` | `https://lightfast-platform.vercel.app` ⚠️ | `https://lightfast-platform.vercel.app` | | `apps/app/src/lib/project-urls.ts` (`platformUrl`) | `withProject` | same | same ⚠️ | same | | `apps/app/src/lib/microfrontends.ts` (`wwwUrl`) | `resolveProjectUrl` | portless URL | `microfrontends.json` fallback `https://lightfast.ai` ⚠️ | same | | `apps/www/src/lib/project-urls.ts` (`appUrl`) | `resolveProjectUrl` | portless URL | `https://lightfast.ai` ⚠️ | same | | `apps/platform/src/lib/project-urls.ts` (`appUrl`) | `withProject` | `http://localhost:3024` | `https://lightfast.ai` ⚠️ (BUG — hits prod from preview) | `https://lightfast.ai` | | `api/platform/src/lib/project-urls.ts` (`appUrl`) | `withProject` | same | same ⚠️ | same | **Why every preview row is broken:** `VERCEL_RELATED_PROJECTS` is only injected when `vercel.json` declares `relatedProjects`. **None of the three `apps/*/vercel.json` files declare it** — they only have `ignoreCommand`. So `withProject` always returns `defaultHost`, and `resolveProjectUrl`'s non-dev branch always returns the `microfrontends.json` `development.fallback` (literally `"https://lightfast.ai"` for both apps). Additionally, `resolveProjectUrl` **does not consult `VERCEL_RELATED_PROJECTS` at all** — only `withProject` does. The two helpers […]
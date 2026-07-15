> AGENT

I'll research the current state of `apps/desktop` and what's needed for prod readiness. Let me start by reading the directly relevant plan/memory files and the key desktop config files in parallel.

> AGENT

I have the key context from the pre-release plan. Let me read the rest and the current state of key desktop files in parallel.

> AGENT

I have full context on the pre-release plan. Now let me read the current state of the key desktop files and the relevant memory files in parallel.

> AGENT

Let me now check the current state of key files in parallel — using the Bash and Read tools.

> AGENT

Now I'll spawn 4 parallel research agents to fill in the gaps — auth/sign-in flow on the app side, renderer/IPC contracts, recent thoughts on desktop prod work, and security/CSP/distribution coverage.

> AGENT

Research doc written to `thoughts/shared/research/2026-05-05-desktop-prod-readiness.md`. **TL;DR — apps/desktop is code-complete; ship is gated on credentials, not code.** The release pipeline (signed/notarized arm64+x64 .dmg/.zip, Sentry source-map upload, Squirrel.Mac feed, build provenance) is wired and active on `main` (PR #621, 2026-04-24). The four `package.json` placeholders are stamped at CI time by design. **What's actually needed for v0.1.0:** 1. **Provision 12 GitHub repo entries** (Phase A from the pre-release plan): - 8 Apple secrets: `APPLE_SIGNING_IDENTITY`, `APPLE_TEAM_ID`, `APPLE_CERT_BASE64`, `APPLE_CERT_PASSWORD`, `APPLE_API_KEY_ID`, `APPLE_API_ISSUER`, `APPLE_API_KEY_CONTENT`, `KEYCHAIN_PASSWORD` - 2 Sentry secrets: `SENTRY_DSN`, `SENTRY_AUTH_TOKEN` - 2 Sentry vars: `SENTRY_ORG`, `SENTRY_PROJECT` - Prereq: Apple Developer Program enrollment + Developer ID cert + ASC API key 2. **Cut `@lightfast/desktop@0.1.0-rc.1` tag** to fire the workflow and verify end-to-end. 3. **Make `Desktop CI / Typecheck + package (unsigned)` a required check** on `main` (manual repo-settings). **Env layer (apps/desktop/src/env/main.ts)** is 5 keys, all main-process: `SENTRY_DSN`, `SPARKLE_FEED_URL`, `SQUIRREL_FEED_URL`, `LIGHTFAST_APP_ORIGIN` (dev-only; prod hardcodes `https://lightfast.ai`), `LIGHTFAST_REMOTE_DEBUG_PORT`. The renderer reads zero env vars — everything routes through `window.lightfastBridge` from preload. `LIGHTFAST_APP_ORIGIN` is auto-injected in dev by `scripts/with-desktop-env.mjs`. **Open questions worth surfacing before release** (in the doc): (1) Clerk `lightfast-desktop` JWT template expiry — the desktop persists the token but never refreshes it; (2) CORS behavior from Electron's internal […]

> DEVELOPER

question, why is this tapping into keychain and shit? is this what other electron apps do?

> AGENT

Yes, this is the standard Electron pattern. There are two distinct keychain interactions happening — easy to conflate them: **1. CI temp keychain (`desktop-release.yml`, "Import Apple signing certificate")** This isn't optional — it's how Apple codesigning works. `codesign` reads identities from the macOS Keychain. On your Mac you have a login keychain with the Developer ID cert; CI runners don't, so you create a throwaway `build.keychain`, import the `.p12`, unlock it, run `codesign`. Slack, VS Code, Discord, Linear, Codex, Figma — every codesigned Mac Electron app's CI does exactly this. The exact `security create-keychain → import → set-key-partition-list` sequence in our workflow is copy-paste from Apple's own GitHub Actions docs. **2. Runtime `safeStorage` (`auth-store.ts`)** The JWT isn't *stored* in Keychain — Electron's `safeStorage.encryptString()` encrypts the blob using a key that's kept in the OS credential store (Keychain on macOS, DPAPI on Windows, libsecret/kwallet on Linux), and the encrypted blob lands in `<userData>/auth.bin`. So Keychain holds one app-scoped key, not one entry per token. This is the recommended Electron pattern for any app handling credentials: - **Slack** — keychain for tokens (via legacy `keytar`) - **VS Code** — keychain for sync auth and Copilot tokens - **Linear** — same pattern - […]
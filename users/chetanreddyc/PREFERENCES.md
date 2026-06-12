# Preferences — ChetanReddyC

## Pushback distribution

- **Correction**: 36.6% — agent proposed the wrong approach, user redirects
- **Failure report**: 35.2% — fix was tried and still doesn't work, user pastes new evidence
- **Non-pushback**: 28.2% — agent answer accepted or task acknowledged

Net takeaway: nearly **72% of mid-session prompts are negative signals**. This user rarely says "looks good, continue." If the agent doesn't nail diagnosis on the first or second try, expect escalating failure reports.

## What triggers correction

1. **Workarounds instead of root fixes** — "hey lets fix that system itself relaible insted of implementing other thing!!!"
2. **Fix didn't actually change anything** — "hey it still same!!" repeated multiple times until visually different
3. **Agent proposes adding another service** — "hey why do we need to have an another service? and can we just do that with the existing postgress db??"
4. **Verbose commit messages or co-author lines** — "remove that coautherd by and keep the commit msg normal one line only!"
5. **Agent asks for secrets directly** — immediately rejects; asks for step-by-step safe update instructions instead
6. **Agent reading .env files** — "dont ever look into the .env files just tell me what to check if needed in that file i will let u know!"

## What satisfies them

- Fix works on first attempt → "ok now its working!!" and the session ends or pivots to the next issue
- Clear numbered steps for DO/infra tasks ("give me steps clearly")
- Brief walkthroughs to find settings: "give me brief walktrough to where to find them!!"
- Agent reverting to last-known-good git state when deep in a regression

## Workflow habits

- **No planning phase** — skips discussion and goes straight to "do it"
- **Tests in production or staging**, not primarily in localhost (though does run local to confirm after prod issues)
- **Iterates by redeploying** to DO, then reports back with new console output if broken
- **Sends screenshots** as the primary medium for UI bugs; the screenshot replaces a description
- **Interrupts agents** when they are taking too long or reading files that feel irrelevant
- **Git**: uses feature branches (e.g. `fixingmajorissues`); pushes when ready; wants one-line commit messages; no co-authored-by lines
- **Env var discipline**: keeps `.env` files local and gitignored; stores production values in DO app-level environment variables; also mirrors some in GitHub Secrets
- **Session cadence**: long sessions (median ~113 min) with only 4 turns — meaning each turn is a multi-step exchange

## Stack preferences

- **Hosting**: DigitalOcean App Platform (migrated from GCP)
- **Object storage**: DigitalOcean Spaces (S3-compatible); previously GCS
- **Session/KV storage**: Cloudflare KV (primary), Upstash Redis (secondary, optional)
- **Backend**: Medusa.js v2 (headless commerce)
- **Frontend**: Next.js (App Router, Turbopack)
- **DB**: PostgreSQL (managed on DO)
- **Commit style**: plain one-line imperative, no attribution lines
- **Prefers minimal changes** — "lets ignore those for now" when side issues arise mid-debug

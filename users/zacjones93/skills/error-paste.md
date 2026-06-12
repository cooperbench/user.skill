---
name: error-paste
description: How Zac reports failures — pastes raw stack traces, server logs, or console errors with minimal or no framing, expecting the agent to diagnose and fix.
---

Zac pastes error output verbatim. He may prepend a one-line observation or just drop the log
block. He does not explain what he was doing when the error occurred, assuming the agent
already has that context from the session.

**Trigger**: Any message containing a raw stack trace, server log block, or `installHook.js`
error, OR a short observation like "I don't see any ui for..." or "pretty sure the submission
page is saying..."

## Examples

**Stack trace drop (no framing):**
> "installHook.js:1 Error: serverFn is not a function
>     at athletes:77:11397
>     at athletes:77:11563
>
> The above error occurred in the <MatchInnerImpl> component."

**Server log paste with setup:**
> "I see these server logs but not1hing in the stripe webhook logs [vite] hot updated: virtual:cloudflare/worker-entry
> [INFO] [Registration] Payment initiation started {
>   competitionId: 'comp_yl7qp5curpr8753z9orzo0lb', ..."

**Full error with drizzle/mysql:**
> "zacjones@MacBookPro wodsmith-start % pnpm db:push
> ...
> Error: unknown error: Code: UNAVAILABLE
> server does not allow insecure connections..."

**Short observation as failure report:**
> "pretty sure the submission page is saying a submission is reviewed when it is not"
> "I don't see any ui for selecting major or minor penalty.."
> "please figure out why the shader isn't rendering....."

## Behavior notes

- After pasting a log, Zac expects the agent to identify the root cause and fix it — not ask for more context
- The "......" trailing dots signal frustration — the bug has probably been present for a while
- Zac will follow up with "yes please fix this" if the agent correctly identifies the problem but doesn't act

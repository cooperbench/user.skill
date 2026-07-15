> DEVELOPER

I want to use a new domain: mc.ainaive.com to replace the old one monecraft.vercel.app , what do you think?

> AGENT

I'll explore the codebase to understand where the old domain is referenced and what a domain switch actually touches (Vercel config, metadata, PWA, and especially the multiplayer/online + Fly.io CORS setup).

> AGENT

Both exploration agents are running. I'll wait for their findings before drafting the plan.

> AGENT

Repo has both a `server/` dir (the Fly.io game server) and `.env.example`. I'll let the agents finish mapping the domain references rather than duplicate their reads.

> TOOL

<task-notification> <task-id>abac23f9fe76c78a2</task-id> <tool-use-id>toolu_01C3qds88MRWuhRZ8epCFrVg</tool-use-id> <output-file>/private/tmp/claude-501/-Users-hutusi-workspace-ai-david-monecraft/b9223e1f-c7d2-43a2-9c4c-e7b163f4a002/tasks/abac23f9fe76c78a2.output</output-file> <status>completed</status> <summary>Agent "Find domain and URL references" finished</summary> <note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note> <result>I have a complete picture. No CSP config exists (the "csp" grep hits are false positives — base64 noise in `bun.lock` and the substring "ati**cSp**awn" in spawn-director code), and there is no `vercel.json`. Here are the findings. ## Search results by category ### 1. Literal `monecraft.vercel.app` Exactly one occurrence in the whole repo (docs only): - `/Users/hutusi/workspace/ai/david/monecraft/docs/deploy.md:127` ``` | `BETTER_AUTH_URL` | the deployed origin, e.g. `https://monecraft.vercel.app` | ``` Related context in the same table/notes (no literal domain, but about this env var): - `docs/deploy.md:138` — "&gt; Ordering / chicken-and-egg: `BETTER_AUTH_URL` is your Vercel origin and…" ### 2. Other `*.vercel.app` / hardcoded `https://` production URLs - No other `*.vercel.app` literals anywhere. - The production game-server URL (Fly.io) is hardcoded only in docs/tests, never in app code: - `/Users/hutusi/workspace/ai/david/monecraft/docs/deploy.md:108` — `https://monecraft-server.fly.dev` (browser connects over `wss://`) - `docs/deploy.md:115` — `curl https://monecraft-server.fly.dev/health` - `docs/deploy.md:129` — `` | `NEXT_PUBLIC_GAME_SERVER_URL` | `wss://monecraft-server.fly.dev` … | `` - `docs/deploy.md:148` — `curl […]

> AGENT

Agent 1 is done — the codebase is essentially domain-agnostic (app origin is derived from `window.location.origin`; only `BETTER_AUTH_URL` hardcodes the origin, via env). Waiting on the online/CORS agent to confirm the Fly.io server side.

> AGENT

The deploy doc already anticipates custom domains (line 141-142). Now I need agent 2's confirmation on whether the Fly.io game server validates the `Origin` header of incoming WS connections. Waiting on it.

> AGENT

No `origin`/`cors`/`access-control` matches in the server dir — the game server authenticates via HMAC join tickets, not Origin checks. Let me confirm by reading the WS upgrade handler.

> AGENT

Confirmed: the game server (`server/index.ts:74-99`) authenticates purely via HMAC join tickets — **no Origin check**, so the Fly.io side needs zero changes for a frontend domain switch. Let me quickly verify the invite-link builder and whether the README links to the live site.

> AGENT

I now have a complete, confirmed picture from both explorations plus the key source files. Here's the short version of what I found before I ask you two quick decisions. **My take: yes, do it — this is a low-risk switch.** The codebase is almost entirely domain-agnostic: - Invite links, the auth client, and the service-worker cache scope all derive from `window.location.origin` at runtime (`lib/online/onlineClient.ts:66`, `lib/auth/client.ts:20`, `public/sw.js:42`) — they follow whatever domain serves the page, automatically. - The Fly.io game server does **no** Origin/CORS check (`server/index.ts:74-99`) — admission is purely the signed join ticket. So the WebSocket/server layer needs **zero** changes. - `NEXT_PUBLIC_GAME_SERVER_URL` points at Fly (`wss://monecraft-server.fly.dev`), independent of the web domain — leave it as-is. **The only functional coupling is one env var:** `BETTER_AUTH_URL` (read at `lib/auth/server.ts:18`). It must become `https://mc.ainaive.com`, or sign-in hangs (that's the documented failure mode at `docs/deploy.md:191`). Everything else is Vercel-dashboard + DNS work, which is yours to do (I can't touch your Vercel/DNS). The one stale in-repo reference is the example value at `docs/deploy.md:127`. Two decisions will finalize the plan:

> AGENT

The user stepped away. I'll proceed with the recommended defaults — **redirect old → new** and **doc example + note + CHANGELOG** — and write the final plan. These are the low-risk choices and can be adjusted on approval.

> AGENT

The plan is written. Here's the summary: ## Domain switch to `mc.ainaive.com` — plan ready **Verdict: go for it.** This is a low-risk switch because the codebase is domain-agnostic. Only **one** functional value is tied to the frontend origin (`BETTER_AUTH_URL`); everything else — invite links, auth client, service-worker scope — derives from `window.location.origin` at runtime, and the Fly.io game server does no Origin/CORS check at all, so the whole WebSocket/server layer needs zero changes. **What actually happens (mostly Vercel + DNS, which you do):** 1. Add `mc.ainaive.com` in Vercel, set it as primary. 2. DNS: `CNAME mc → cname.vercel-dns.com` at your `ainaive.com` provider. 3. Redirect `monecraft.vercel.app → mc.ainaive.com` (keeps already-shared invite links working). 4. Set Production `BETTER_AUTH_URL = https://mc.ainaive.com` and redeploy. (Leave `NEXT_PUBLIC_GAME_SERVER_URL` on Fly, untouched.) **What I change in the repo** (proceeding with the recommended scope since you were away — adjustable): fix the stale example at `docs/deploy.md:127`, extend the custom-domain note there, and add a `CHANGELOG.md` entry. No app/server/config code. Two decisions I picked defaults for (you can override on approval): **redirect** the old domain (vs. keep both / hard cutover), and **doc + note + CHANGELOG** as the repo scope.

> AGENT

Sure — let me re-present those two decisions.

> AGENT

Both selections match the plan as written (redirect old → new; doc example + note + CHANGELOG). The plan file is already aligned, so no edits needed.

> AGENT

Plan approved. Let me make the two in-repo changes. First I'll read the relevant sections of the files.

> AGENT

Now I'll make the edits. First, the `docs/deploy.md` example value and the custom-domain note:

> AGENT

Now the CHANGELOG entry under the Unreleased `### Changed` section:

> AGENT

Now let me run the format check (docs-only edits, so this is the relevant gate):

> AGENT

The deploy.md edit needs reformatting (likely the table alignment). Let me fix it with Prettier:

> AGENT

Formatting passes. Let me review the staged diff and commit to `main` (docs-only, minor single-purpose change):

> AGENT

Committed to `main` (`3e24f39`). Here's where things stand. ## Done (in-repo) - **`docs/deploy.md`** — fixed the `BETTER_AUTH_URL` example to `https://mc.ainaive.com` and added a **Custom domain** subsection with the exact procedure. - **`CHANGELOG.md`** — entry under Unreleased → Changed. - Prettier clean; committed straight to `main` per the workflow (docs-only). **Not pushed** — that's yours to do. ## Your turn (Vercel + DNS — I can't touch these) 1. **Vercel → Settings → Domains** → add `mc.ainaive.com`, set it **primary**. 2. **DNS** at ainaive.com: `CNAME mc → cname.vercel-dns.com` (use the exact target Vercel shows). 3. **Redirect** `monecraft.vercel.app → mc.ainaive.com` (308, path-preserving) — keeps already-shared invite links alive. 4. **Env**: set Production `BETTER_AUTH_URL = https://mc.ainaive.com`, leave `NEXT_PUBLIC_GAME_SERVER_URL` alone, then **redeploy**. ## Why this is low-risk (the finding worth remembering) The codebase is domain-agnostic. Invite links, the auth client, and the SW cache scope all derive from `window.location.origin` at runtime, and the Fly game server (`server/index.ts`) does **no** Origin/CORS check — admission is purely the HMAC join ticket. So the WebSocket/server layer needs zero changes. The only thing tied to the web origin is `BETTER_AUTH_URL`; if it doesn't match, sign-in hangs. ## Verify after cutover - `curl -I https://monecraft.vercel.app/` → 308 to `https://mc.ainaive.com/` […]
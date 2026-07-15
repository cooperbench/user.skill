> DEVELOPER

analyse the auxilio-extension, and check for any performance issues, memory leak or any other issue that can cause the system resource excess consumption, slow down or crash of browser or webpage or the extension itself, give me a detailed report.

> AGENT

I'll analyze the auxilio-extension for performance issues, memory leaks, and resource consumption problems. Let me start by exploring its structure.

> AGENT

Let me read the core files — the content script (most performance-sensitive since it runs on Google Calendar), the background worker, and the sync logic.

> AGENT

Let me read the rest of the content script and the other performance-critical files in parallel.

> AGENT

Now the sync logic and the side panel app, plus the supporting libs.

> AGENT

Now the side panel React app, hooks, and the auth/people/engine libs.

> AGENT

Now the main React panel component and the remaining libs.

> AGENT

Let me verify a few specifics: dead code, the QueryClient config, manifest, and `innerText` usage in hot paths.

> AGENT

Let me confirm the unused helpers are truly dead and check the people-cache write pattern and `runSync` concurrency once more.

> AGENT

I've now read the full extension — content script (1843 lines), background worker, sync engine, calendar/auth/people libs, and the side-panel React app. Here is the detailed report. --- # Performance & Resource Audit — `auxilio-extension` (v0.14.1) ## Scope and method I read every runtime file: the content script that runs on `calendar.google.com` (`entrypoints/calendar.content.ts`), the MV3 service worker (`entrypoints/background.ts`), the sync engine (`lib/calendar-sync.ts`, `lib/calendar.ts`), auth/people libs, and the side-panel React app (`features/visit/*`, `lib/*`). The content script is by far the highest-risk surface because it lives inside Google Calendar — a heavy, constantly-mutating SPA — so most findings concentrate there. **Overall:** the code is defensively written (sync coalescing, burst caps, throttles, bounded 90-day window, TTL'd caches, orphan-context guards). There is **no catastrophic leak or runaway loop**. But there are a handful of real, fixable hot paths — one of which (full-page `innerText` on a timer) will cause noticeable jank on the low-end Android-class hardware your constraints target, and a lot of avoidable steady-state work. --- ## HIGH severity ### H1 — Full-page `document.body.innerText` on a recurring timer while editing an event `entrypoints/calendar.content.ts` - `readSurface()` returns `{ el: document.body, eid }` for the URL-eid case and the full-screen editor case (`calendar.content.ts:282` and `:287`). […]
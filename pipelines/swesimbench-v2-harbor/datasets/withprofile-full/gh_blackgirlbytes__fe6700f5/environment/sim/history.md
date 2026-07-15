[DEVELOPER]: there will be people running a booth where other people play this game..let's create a simple guide for them..it shouldnt be anything too crazy. , if you can hand off to someone tech on the booth so they know how to set up the leaderboard and the game on the day https://play-planetfall.vercel.app https://play-planetfall.vercel.app/leaderboard

[AGENT]: I’ll keep this lightweight and booth-friendly, then add a short technical handoff section for the person setting up screens and devices. I’m going to quickly inspect the repo and the live pages so the guide matches the actual game flow.

[AGENT]: I found this is a compact Vite game with a Vercel leaderboard API, so the guide can live cleanly as a Markdown handoff in the repo. I’m reading the existing README and leaderboard code now to make sure the day-of setup instructions are accurate.

[AGENT]: The leaderboard API creates its own table on first use and accepts either `DATABASE_URL` or `POSTGRES_URL`, which is nice for a handoff. I’m going to turn that into a practical “what to do before doors open” checklist, with a non-technical booth runbook up front.

[AGENT]: One small live-check note: the `/leaderboard` route is a real display route, while the API test needs the URL quoted in zsh because of the `?limit=...` query string. I’m checking the API response and then I’ll write the guide.

[AGENT]: The live API is reachable, but the current board appears to contain test or stale scores, so I’m going to include a tiny pre-event reset/sanity step for the tech handoff. I won’t touch production data; this should be an explicit day-of choice by whoever owns the database.

[TOOL]: <turn_aborted> The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed. </turn_aborted>

[DEVELOPER]: i think all i may need to say is on the arcade screen ..go to https://play-planetfall.vercel.app on the leaderboard screen go to https://play-planetfall.vercel.app/leaderboard

[AGENT]: Yep, that is probably the right level: two clear screens, two URLs, no ceremony. I’ll make the guide match that and keep the tech handoff to “open these, fullscreen them, refresh if needed.”

[AGENT]: I added the small guide as `BOOTH_GUIDE.md`. I’ll do one quick status check so I can tell you exactly what changed and leave the repo tidy.

[AGENT]: Done. I added a very simple booth handoff at [BOOTH_GUIDE.md](/Users/goose-guest/Documents/work/planetfall-seed-signalkit/BOOTH_GUIDE.md). It says exactly the key thing: - arcade/player screen: `https://play-planetfall.vercel.app` - leaderboard screen: `https://play-planetfall.vercel.app/leaderboard` Plus a tiny tech-person checklist to test one saved score and refresh the leaderboard. No tests run since this was docs-only.
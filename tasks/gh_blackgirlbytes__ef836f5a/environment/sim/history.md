> DEVELOPER

hmm does the leaderboard screen automatically refresh

> AGENT

I’ll take a quick look through the code path for the leaderboard screen so I can answer from the implementation rather than vibes. I’m using the `using-entire` skill for repo exploration context.

> AGENT

I found the likely UI files: `src/leaderboard.js` and `src/leaderboardPanel.js`, plus the API. I’m checking both the current code and whether there’s recorded implementation intent for this area.

> AGENT

Current panel code has no timer or polling visible so far. I’m tracing where `showBoard` and `loadLeaderboard` are called, because refresh behavior might live outside the panel itself.

> AGENT

The route handler is the key bit: it loads once when the `/leaderboard` route is opened. I’m reading that exact block now to see whether there’s any repeat load on focus, visibility, or interval.

> AGENT

Answer’s shaping up: it refreshes on open and after a save response, but it does not poll while sitting open. I’m grabbing line numbers so I can point you straight at the spots.

> AGENT

Nope, it does **not** automatically refresh while the leaderboard screen is open. It fetches once when opened via `showTitleLeaderboard()` in [src/main.js](/Users/goose-guest/Documents/work/planetfall-seed-signalkit/src/main.js:246), and the `/leaderboard` route calls that once on page load at [src/main.js](/Users/goose-guest/Documents/work/planetfall-seed-signalkit/src/main.js:278). After saving a score, it re-renders using the updated entries returned by the POST response in [src/leaderboardPanel.js](/Users/goose-guest/Documents/work/planetfall-seed-signalkit/src/leaderboardPanel.js:163). So: open screen = fresh load, save score = updated board, but if someone else submits while you’re staring at it, it won’t update until you reopen or reload.
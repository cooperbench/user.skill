[DEVELOPER]: @docs/quick-wins-todo.md /teach read then lets start

[AGENT]: Great, I've read your todo list. You've already knocked out #1 (trailer embed) — nice work! The next unchecked item is **#2: Show streaming links on detail page**. Before we dive in, let me ask you a couple of questions to see where your head's at: 1. **Where do streaming links come from?** The todo says "Already in detail response" — do you know which part of the Jikan anime detail response contains streaming info? 2. **Have you looked at how you implemented the trailer embed?** Since that's already done, the pattern for streaming links will be very similar. Can you describe the general flow of how data gets from Jikan → your Express backend → the detail page frontend? Take a look at your detail page code if you need to refresh your memory. Which file would you check first?

[DEVELOPER]: yeah done that lets start

[AGENT]: Alright, let's get into it. First question: **What does the streaming data actually look like in the Jikan response?** You can figure this out a couple of ways: - Check your existing controller that fetches anime details — what does the Jikan response shape look like? - Or hit the Jikan API directly in your browser: `https://api.jikan.moe/v4/anime/1` and search for "streaming" Once you know the shape of the data, you'll know what you're working with on the frontend. What do you find?

[DEVELOPER]: there is no result about "streaming"

[AGENT]: Good catch — let me verify what's actually in the response. Let me take a quick look at what your detail controller is fetching.

[AGENT]: OK so your detail page is actually at `public/entity/`. You're right that "streaming" might not be a key in the basic Jikan anime detail endpoint. Here's the thing — the Jikan `/v4/anime/{id}` response has a field called **`streaming`** but it might be empty for some anime. It's also possible it shows up as an array of objects with `name` and `url`. **But here's a better approach to investigate:** Try hitting the Jikan API in your browser for an anime you know has streaming links. Try: `https://api.jikan.moe/v4/anime/21` (One Piece) Look through the JSON response — do you see a `streaming` key? What's inside it? This is an important skill: **always check the actual API response** before writing code that depends on it.

[DEVELOPER]: there is non check

[DEVELOPER]: check again

[AGENT]: You were right — there's **no `streaming` data** in the main anime detail endpoint. The key exists but it's `null`. So here's the real question: **Jikan has a separate endpoint for streaming links.** Check the Jikan docs — the pattern is: `/v4/anime/{id}/streaming` Knowing that, you have a decision to make: 1. **Do you make a second fetch call** from your frontend to get streaming data separately? 2. **Or do you add a new Express proxy route** that hits `/v4/anime/{id}/streaming`? Think about how your app is architected (look at CLAUDE.md if you need a reminder). Which approach fits the project's pattern?

[DEVELOPER]: data 0 name "Crunchyroll" url "http://www.crunchyroll.com/series-257631" 1 name "Netflix" url "https://www.netflix.com/title/80107103" 2 name "Shahid" url "https://shahid.mbc.net/en/series/One-Piece/series-826519"

[AGENT]: Nice, you found the data! So `/v4/anime/21/streaming` returns an array of objects, each with a `name` and `url` — Crunchyroll, Netflix, Shahid, etc. Now, back to my question — looking at how your app works: **Frontend never calls Jikan directly. All API calls go through the Express server.** So what do you need to do first — frontend or backend? And what would that backend route look like?

[DEVELOPER]: guide me step by step

[AGENT]: Alright, let's go step by step. **Step 1: Add a new Express proxy route** You need a new route in your backend that your frontend can call to get streaming data. - Which file holds your API routes? - Looking at your existing routes (like `/api/anime-details/:id`), what would you name a route for streaming links? Go find that routes file and tell me what you see.

[DEVELOPER]: guide me

[AGENT]: OK, here's what you're working with. Look at line 23: ``` router.get("/api/:entityType/:id", animeDetails); ``` That's your existing detail route. Now you need a **new route** for streaming links. Here's your step-by-step plan: **Step 1 (backend — route):** Add a new route in `router.js`. Think about: - It needs the entity type and the anime ID, just like the detail route - It should follow the same naming pattern — something like `/api/:entityType/:id/streaming` - Where should it go relative to line 23? (Hint: order matters with Express routes) **Step 2 (backend — controller):** Create a controller function that fetches from Jikan's `/v4/anime/{id}/streaming` endpoint. Look at your existing `animeDetails` controller for the pattern — it'll be almost identical. Start with **Step 1**. Add that route to `router.js`. What Jikan endpoint will it need to call? And do you need a new controller or can you reuse `animeDetails`?

[DEVELOPER]: guide me again

[AGENT]: OK, let's get very specific. **Step 1: Create the controller function** 1. Open `src/controllers/anime-details.js` 2. You already have `animeDetails` there — you'll add a **new function** right below it 3. Name it something like `animeStreaming` 4. It should do the same thing as `animeDetails` but fetch from a different URL: `https://api.jikan.moe/v4/anime/{id}/streaming` 5. Don't forget to **export** it Hints: - Copy the pattern from `animeDetails` (lines 1-14) - You only need `req.params.id` — no `entityType` needed since streaming is anime-only - Same `.then()` / `.catch()` chain **Step 2: Add the route** 1. Open `src/router.js` 2. Import your new function at the top alongside `animeDetails` 3. Add a new route **above** line 23 (`/api/:entityType/:id`), because that route would match first otherwise 4. The route: `/api/anime/:id/streaming` Go try Step 1 first — write that controller function, then tell me when you're ready for me to check it.
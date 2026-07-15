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
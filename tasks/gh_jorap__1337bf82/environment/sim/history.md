[DEVELOPER]: improve quality of scale-clues that would be applicable to a family setting with no possibility to answer in a adult response. it must be applicable to people of all walks of life

[AGENT]: <think></think>

[AGENT]: I'll look at how `scale-clues` are defined in the randomizer data and what they're used for.

[AGENT]: <think></think>

[AGENT]: Reviewing the scoring logic and past curation notes to see what makes a prompt family-safe and universally answerable.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Auditing the full list for adult-only framing, role-specific prompts, and near-duplicates, then replacing weak entries with family-safe alternatives.

[AGENT]: <think></think>

[AGENT]: Writing a curation pass: replace adult-only and role-specific prompts, dedupe overlaps, and add family-safe alternatives.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Writing a focused curation script with targeted replacements and a modest set of new family-safe prompts.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Cleaning up near-duplicates and replacing the repetitive micro-scenario batch with a tighter, higher-quality set.

[AGENT]: <think></think>

[AGENT]: Writing a proper curation script to avoid the repetitive-template problem.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Fixing the last two age-specific prompts and updating the curation script for future runs.

[AGENT]: <think></think>

[AGENT]: **Ranking prompts** (`scale-clues`) are now tuned for mixed-age family play — any player can name a concrete clue without needing an adult frame of reference. ### What changed **Removed or reframed adult-only framing** (~40 prompts), including: - Work/meeting prompts → group-friendly versions (“speaking in front of a group”, “group project”) - Parent/grandparent/teenager framing → age-neutral (“fun at any age”, “someone much older or younger”) - Niche or privilege-heavy scenarios → universal ones (“long trip sitting still” instead of “long flight”, “quick errand run” instead of “pharmacy run”) - Age-gated prompts (“before age thirty”, “as an adult”, “five-year-old”) → open wording **Added ~120 family-table prompts**, such as: - Mixed-age board games and party games - Backyard, camping, and road-trip situations - Classic kid-party games (hide-and-seek, musical chairs, pin the tail) - Everyday household moments anyone can answer (“toast burns”, “remote batteries die”) **Updated play copy** so the deck signals family use: - Tagline: *“Name one example anyone at the table could say…”* - Play hint: *“Give one real example a kid or grown-up could both mean…”* ### Examples | Before | After | |--------|-------| | Things that would make you laugh in a serious meeting. | Things that would make you […]
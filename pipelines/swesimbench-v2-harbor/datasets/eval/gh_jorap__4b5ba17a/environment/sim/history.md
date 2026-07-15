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

[DEVELOPER]: Mixed-age board games and party games replace because many are not board game savvy. Classic kid-party games (hide-and-seek, musical chairs, pin the tail) ensure that the games used are the very obvious games

[AGENT]: <think></think>

[AGENT]: I'll find board-game and party-game prompts in `scale-clues` and swap anything niche for very obvious games everyone knows.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Replacing board-game-catalog prompts with obvious games everyone knows, and dropping obscure party-game names.

[AGENT]: <think></think>

[AGENT]: Fixing a duplicate and restoring the item count to 300.

[AGENT]: <think></think>

[AGENT]: The string to replace was not found in the file.

[AGENT]: <think></think>

[AGENT]: Restoring two dropped items and updating the curation scorer.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Done. Board-game-hobbyist prompts are out; game prompts now point at things everyone already knows. ### Removed (board-game savvy / obscure) - All meta board-game prompts (“mixed ages”, “bluffing”, “under twenty minutes”, “non-gamers”, etc.) - Obscure party games: duck duck goose, musical statues, capture the flag, mother may I, leapfrog, follow the leader ### Replaced with obvious games **No rules to learn:** - tag, hide-and-seek, Simon says, red light green light, freeze tag, freeze dance - musical chairs, pin the tail on the donkey, hot potato, charades - rock paper scissors, twenty questions, catch, I spy - hopscotch, jump rope, tic-tac-toe, thumb war, arm wrestling **Classic tabletop (household names, not hobby games):** - checkers, snakes and ladders, cards together **Open prompts (name any familiar game):** - “Games that need no equipment at all” - “Card games everyone already knows” - “Games you could explain in one sentence” - “Games a child and a grandparent both already know” Still 300 prompts. The curation scorer now penalizes hobbyist board-game wording and boosts named obvious games like hide-and-seek and musical chairs.
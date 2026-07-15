[DEVELOPER]: for scale clues, have no categories, have 500 items

[AGENT]: I'll inspect how scale clues are defined in the randomizer data and how categories are used.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Restructuring scale-clues to a flat list and generating 500 items. Updating the JS so ranked-prompts play directly without categories.

[AGENT]: <think></think>

[AGENT]: Checking the generated YAML — PyYAML may have altered formatting and some filler items look weak.

[AGENT]: <think></think>

[AGENT]: The YAML structure broke — `personal-scales` was nested under `scale-clues`. Fixing the file structure and verifying the item count.

[AGENT]: <think></think>

[AGENT]: Build succeeded. Updating the page copy since no collection uses categories anymore.

[AGENT]: Done. Here's what changed: **`scale-clues` (Ranking prompts)** - Removed the 3 categories (15 prompts total) - Flat `items` list with **500** ranking prompts (template-generated, family-friendly) - Tapping the collection goes straight to shuffle — same flow as personal icebreakers and spectrums **`randomizer.js`** - `ranked-prompts` is now direct-play (no category step) - Collection card shows "500 prompts" instead of category count **`randomizer.md`** - Page copy updated — no mention of choosing categories Examples from the new set: - "Jobs from least to most stressful on a Monday morning." - "Worst to best snacks to eat in a quiet room." - "Board games from quickest to longest to finish." - "Moving furniture from least to most likely to need teamwork."
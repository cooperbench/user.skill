[DEVELOPER]: for scale clues, I am not seeing them. can you find ways to use this db?

[AGENT]: <think></think>

[AGENT]: Investigating how scale clues are defined and rendered in the randomizer.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Identifying the bug: the template uses Tailwind's `hidden` class (`display: none`) while JS only toggles the HTML `hidden` attribute, so prompts stay invisible. Removing the conflicting `hidden` classes from the template.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Found the bug. The data was fine — **500 prompts** in `scale-clues` — but nothing showed on screen. **Cause:** The play card used Tailwind’s `hidden` class (`display: none`) on the prompt, scale, and poles elements. The JS only toggled the HTML `hidden` attribute, so the CSS class kept everything invisible for all three collections (Ranking prompts, Personal icebreakers, Concept spectrums). **Fix:** Removed the `hidden` class from those elements in `layouts/randomizer.html` and rely on the `hidden` attribute only, which the JS already controls. After a refresh, **Ranking prompts** (`?set=scale-clues`) should show prompts like *"Things you'd want to do when you're very tired"* when you shuffle. Personal and spectrum decks should work too. **Note:** The collection is labeled **“Ranking prompts”** on the home screen (id is still `scale-clues`). The 1–100 instructions live in the play hint above the card, but that hint is hidden in focus mode during play. If you want a persistent “Rank 1 to 100” line on the card like personal icebreakers have, say the word and we can add a `scale_label` for that deck.
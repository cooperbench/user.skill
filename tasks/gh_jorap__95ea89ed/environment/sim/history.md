[DEVELOPER]: for personal-scales compare with the game fun facts

[AGENT]: <think></think>

[AGENT]: I'll look up how `personal-scales` and game fun facts are defined in the randomizer data and compare them.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: I'll pull the Fun Facts examples from the session history and analyze how `personal-scales` prompts are structured.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Here’s how **personal-scales** lines up with the real **Fun Facts** game (Repos / Asmodee). ## What matches | Aspect | Fun Facts (game) | personal-scales (yours) | |--------|------------------|-------------------------| | Core vibe | Self-reflective icebreaker about real people at the table | Same — tagline says “real habits, preferences, and memories” | | Scale cards | Some cards are explicitly 0–100 | All cards assume 1–100 (`scale_label` in UI) | | Play loop | Everyone writes a secret number, group orders low→high | Same mechanic works; `play_hint: Answer honestly.` | | No categories | Flat deck, draw and read | Flat 500-item list, direct play | | Family-safe subset | Rules say skip cards that don’t fit the group | Entire deck is family-friendly | Overlap examples that *do* feel like Fun Facts cards: - “How long can you go without checking your phone?” - “How competitive are you at board games?” - “How much do you enjoy making lists?”-style enjoyment questions (you have many “How much do you enjoy…”) ## Where it diverges ### 1. Two card types in Fun Facts, one type in yours Fun Facts mixes: - **0–100 scale** — “How lazy are you?”, “To what degree are […]
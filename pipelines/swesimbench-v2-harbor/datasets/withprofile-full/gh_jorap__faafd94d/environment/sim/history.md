[DEVELOPER]: can you suggest other collections to add here?

[AGENT]: Reviewing existing collections in `randomizer.yaml` and how they're used so suggestions fit the current structure.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: You have three top-level collections today, each mapped to a play mode the JS already supports: | Collection | Mode | Core mechanic | |---|---|---| | **Ranking prompts** | `ranked-prompts` | Name one example; group ranks it 1–100 | | **Personal icebreakers** | `personal` | Honest self-rating 1–100 | | **Concept spectrums** | `spectrum` | One clue word on a hidden spot between two poles | The engine also supports a fourth shape — collections with **categories** — but nothing uses it yet. Your original design had a “quick facts” deck that never shipped as its own collection. Here are additions worth considering, ordered by fit. ### Strong fits (no code changes) **1. Would you rather** (`mode: ranked-prompts`, new `play_hint`) Binary dilemmas, not spectrums. Everyone picks a side and defends it. ```yaml - id: would-you-rather title: Either-or dilemmas mode: ranked-prompts tagline: Two options, one choice. Pick a side and say why. play_hint: Read both options aloud. Everyone picks one — no middle ground. Best argument wins. items: - "Always be ten minutes early, or always be ten minutes late?" - "Never use a phone again, or never watch a screen again?" - "Know how every story ends, or forget every […]
[DEVELOPER]: for spectrum, compare with wavelength board game

[AGENT]: <think></think>

[AGENT]: I'll look at how Spectrum is defined in the randomizer and compare it to the Wavelength board game.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: ## Concept spectrums vs Wavelength Your **Concept spectrums** collection is modeled on Wavelength’s **spectrum cards** — the left/right pole pairs — not the full boxed game. That’s the right layer to compare. ### What matches Wavelength | Piece | Wavelength | Your spectrum mode | |--------|------------|-------------------| | Card format | Two opposing concepts (e.g. Hot ↔ Cold) | Same: `left` / `right` pairs | | Clue idea | One clue that sits *somewhere* on the line between the poles | Play hint asks for one noun/phrase on that line | | No categories | Draw a card, read the poles, play | Collection → shuffle, no category step | | Family-friendly poles | Mix of normal + “weird” sides | Generic, worldwide-friendly opposites | The UI shows exactly what a Wavelength card shows: two poles and a bridge between them. ```1017:1024:data/randomizer.yaml - id: spectrum title: Concept spectrums mode: spectrum tagline: Two opposing ideas — no categories, no questions. Name one word or phrase that sits in the grey area between them. play_hint: Think of a single noun or short phrase that lands between these extremes. Expect a friendly group debate. spectrums: - left: Hot right: Cold ``` The strong pairs […]
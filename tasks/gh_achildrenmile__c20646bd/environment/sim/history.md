[DEVELOPER]: Implement the following plan: # Plan: Neue Sektion "Funkbetrieb" auf der Startseite ## Context BOS-ARSA führt zwei regelmäßige Funkübungen durch, die auf der Website prominent dargestellt werden sollen: 1. **BOS-ARSA Krisenkommunikationsübung** — Jeden Sonntag ab 18:45 Lokalzeit. Start am OE8XNK (Gerlitzen) auf 145.7625 MHz, -0.6 MHz Offset. Abfrage auf Kärntner Repeatern, dann Direktfrequenz. Österreichweit über den OE-Link-Verbund. 2. **Notfunk Runde Österreich** — Jeden 1. Mittwoch im Monat, 17:15 UTC auf 3643 kHz ± QRM. ## Platzierung Neue Sektion **zwischen "Ziele" (#ziele) und "Mitglied werden" (#mitglied)**. Logischer Fluss: "Wofür wir stehen" → "Was wir regelmäßig tun" → "Werde Teil davon". - Section-ID: `#funkbetrieb` - Stil: `.section section--alt` (leicht abgesetzter heller Hintergrund, da Ziele-Sektion davor dunkel ist) - Nav-Label: "Funkbetrieb" — zwischen "Ziele" und "Mitglied werden" ## Design Zwei Karten nebeneinander im 2-Spalten-Grid: ``` ┌──────────────────────────────┐ ┌──────────────────────────────┐ │ 📻 Krisenkommunikations- │ │ 🌐 Notfunk Runde │ │ übung │ │ Österreich │ │ │ │ │ │ Jeden Sonntag │ │ Jeden 1. Mittwoch/Monat │ │ ab 18:45 Lokalzeit │ │ 17:15h UTC │ │ │ │ │ │ ▸ OE8XNK 145.7625 MHz │ │ ▸ 3643 kHz ± QRM │ │ -0.6 MHz Offset │ │ │ │ │ │ Monatliche Notfunk-Runde […]

[AGENT]: I'll implement the "Funkbetrieb" section. Let me start by reading the relevant files.

[AGENT]: Now I have all the context. Let me implement the three changes in parallel.

[AGENT]: Now I'll make all three file changes:

[AGENT]: Now add the responsive rules for the schedule grid:

[AGENT]: Now let me build to verify:

[AGENT]: Build successful. Let me quickly verify the output contains the new section in the right place:

[AGENT]: The section order is correct: Ziele (line 223) → Funkbetrieb (line 265) → Mitglied werden (line 302).

[AGENT]: All done. Here's what was implemented: **`src/index.njk`** — New `<section id="funkbetrieb">` between Ziele and Mitglied werden with: - Section header (label, title, intro text) - Two-column grid with schedule cards: - **Krisenkommunikationsübung** — Jeden Sonntag, 18:45 Lokalzeit, OE8XNK 145.7625 MHz - **Notfunk Runde Österreich** — Jeden 1. Mittwoch/Monat, 17:15 UTC, 3643 kHz **`src/css/index.css`** — New styles: - `.schedule-grid` — 2-column grid, collapses to 1 column at 1024px - `.schedule-card` — Based on feature-card style with gold bottom-bar hover effect - `.schedule-card__freq` — Monospace font, gold color, left-border accent block - `.schedule-card__badge` — Pill-shaped tag for schedule info **`src/_includes/nav.njk`** — "Funkbetrieb" nav link added between "Ziele" and "Mitglied werden" Build passes cleanly (7 files written).
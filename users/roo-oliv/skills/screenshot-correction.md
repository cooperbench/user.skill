---
name: screenshot-correction
description: >
  Trigger: a visual bug in the running game — wrong rendering, invisible
  element, wrong z-order, wrong color. roo-oliv attaches a macOS screenshot
  and states one specific observation about what differs from expected.
---

# Behavior: screenshot-correction

roo-oliv runs the game, sees a visual discrepancy, takes a macOS screenshot (filename in Portuguese: `Captura de Tela YYYY-MM-DD às HH.MM.SS.png`), and sends a message that:
1. References the file path (absolute, under `/Users/rodrigooliveira/Desktop/`).
2. States one or two specific visual observations — what is visible vs. what should be.
3. Often offers a hypothesis in parentheses: `"(maybe it's the same color of the dialogue box or it's been drawn underneath it)"`.

The message is short — 1–3 sentences max. No build output, no code. Just what they saw.

## Verbatim examples

**Example 1 (dialogue box + text bug):**
> `"The text is displayed correctly at the bottom of the screen but there is no dialogue box under the text (or its color is the same as the background) and I can't move after the dialogue is triggered and pressing E doesn't close/end the dialogue. See the print attached (if it doesn't work, look at /Users/rodrigooliveira/Desktop/Captura de Tela 2026-02-16 às 00.24.19.png)"`

**Example 2 (text invisible after box fix):**
> `"Look at /Users/rodrigooliveira/Desktop/Captura de Tela 2026-02-16 às 00.31.48.png. Now the Dialogue box appears but the text doesnt (maybe it's the same color of the dialogue box or it's been drawn underneath it)."`

**Example 3 (invisible buttons, no screenshot):**
> `"Ok, this seems to work better, just one issue: on the main level selection screen now I don't see any of the buttons (they're still clickable though)"`

## Simulation instructions

When role-playing a roo-oliv visual bug report: lead with the file path or "See the print attached", state what's visible vs. missing, add a parenthetical hypothesis about the rendering cause. Keep it under 3 sentences. Preserve Portuguese macOS screenshot naming.

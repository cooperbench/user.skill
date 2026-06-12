---
name: screenshot-debug
description: basher83 reports UI or auth failures by sending a screenshot with one short sentence of context — no stack traces, no error text typed out. Trigger: agent asks what the user is seeing or a UI/OAuth flow is stuck.
---

When a UI flow breaks (OAuth redirect, page stuck, button not working), basher83 describes the symptom in the fewest possible words and attaches a screenshot. He does not copy browser console output, does not describe UI elements, and does not explain what he expected. The image is the evidence.

Characteristics:
- One sentence of context, lowercase, often without a period
- Screenshot attached immediately after
- No further elaboration unless the agent asks specifically
- Will send a second screenshot if the first one didn't resolve it
- If consulting another tool, will paste the other tool's output verbatim and prefix with attribution

**Examples:**

> "hmm I click auth button but dont get the redirect to token"

> "same page stuck"
> [Image: image/png]

> "I get stuck here. This is an incognito window."
> [Image: image/png]

> [Image: source: REDACTED 2026-02-12 at 9.19.31 AM.png]  *(sent without any text when another screenshot was requested)*

**When pasting a second opinion from another tool:**

> "I used Claude and Chrome directly, and here's what he said. I found the issue! The console shows an error: 'Invalid request format' that's occurring when the Authorize button is clicked. [... full output pasted verbatim ...]"

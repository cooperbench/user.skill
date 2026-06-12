---
name: screenshot-ui-correction
description: Triggers when cteyton notices a UI display problem. The message is a single short sentence describing what's wrong, followed by one or more "[Image: image/png]" inline screenshots. No setup, no explanation of how to reproduce.
---

# Screenshot + one-liner UI correction

cteyton attaches screenshots to UI bug reports without narrating them. The pattern is always:

1. One sentence (sometimes imperative, sometimes observational) stating what's wrong
2. `[Image: image/png]` — one or two screenshots at the end

The sentence is specific about what's wrong but does not describe steps to reproduce, browser version, or expected vs. actual in structured form. The screenshot is the evidence.

## Verbatim examples

> `"Looks like here, ai coding agents logo are not rendered correctly. \n[Image: image/png]"`

> `"I still have weird display issues in the 'Remediate' tab \n[Image: image/png]"`

> `"For a remediation I've selected both Cursor as agent and target rendering. After clicking on 'Execute Remediation', the modals shows me 'copilot'. Investigate why and fix this bug\n[Image: image/png]\n[Image: image/png]"`

> `"Make these two button 'List / Tree' more visible, on the left side, and maybe create a frame that encompass the whole content below ? \n[Image: image/png]"`

> `"it should not be in the header but instead below, currently the repo is displayed in the header bar \n[Image: image/png]"`

> `"The packmind section should be visible when reaching the remediate tab: . And at anytime even after display/hiding elements in the page \n[Image: image/png]"`

> `"Something should also appear in the 'Latest page' \n[Image: image/png]"`

## Key traits

- Sentence before screenshot is never more than 2 lines.
- Uses `"Investigate why and fix this bug"` phrasing when the cause is unclear.
- Uses `"make"` / `"remove"` / `"should"` phrasing for design change requests accompanied by a screenshot.
- Trailing `?` appears rarely — only for suggestions, not bug reports.

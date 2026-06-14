---
name: report-what-you-notice
description: Report a bug or unexpected behavior the developer would notice, the way they report it. Use when the just-finished work plausibly has a defect, a UI/behavior mismatch, or a failing test the user would catch.
---

# Report what you notice (move: bug_report)

Developers spot problems and report them — often tersely, often pasting the evidence with little
commentary. This is a distinct move from pushback: it's "this is broken", not "you did it wrong".

How to do it like this user:
- Decide a plausible defect given what was just built and the real project state (read the repo if
  available): a UI element not responding, an error on a path, a test that would fail, a behavior
  that doesn't match the spec.
- Report it in their register (`STYLE.md`):
  - Some paste a raw stack trace / error with a 2–5 word prefix and nothing else.
  - Some describe the symptom in one line: "the avatar doesnt update on theme change".
  - Some say only "still broken" / "still the same issue" when a prior fix didn't work.
- Don't over-explain. Don't propose the fix unless this user does.

Only report a bug that is plausible for the current code — not a generic complaint.

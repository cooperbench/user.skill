> DEVELOPER

why do i see this error when i try to grade my drain-cycle runs? drain-cycle grade: warning: ABA-406 is a draft — excluded from rate

> AGENT

I'll find where that warning comes from in the grade code.

> AGENT

The warning lives in `drain_cycle/grade.py:108`. Let me read the surrounding logic.

> AGENT

This is a benign warning, not an error. Here's what's happening. `grade` reads every grade file in `~/.drain-cycle/grades/*.md`. Each file has a frontmatter `status:` field that is either `confirmed` or `draft`. Only `confirmed` files count toward the pass-rate. For any file that is *not* `confirmed`, it prints this warning to stderr and excludes it (`grade.py:98-110`). So you're seeing this because the grade file for **ABA-406** has `status: draft` (or no `status` field — the default is `draft` per line 99). Let me confirm by looking at the actual file:

> AGENT

Confirmed. It's exactly as expected — not an error. `~/.drain-cycle/grades/ABA-406.md` has `status: draft` in its frontmatter. The `grade` command splits files into `confirmed` vs everything-else, and warns + excludes anything not yet confirmed so it doesn't pollute the pass-rate (`grade.py:100-110`). Let me check what flips a grade from `draft` → `confirmed`, so you know how to clear the warning:

> AGENT

That's the full picture. Here's the answer. ## Why you see the warning It's **not an error** — it's `grade` telling you ABA-406's grade hasn't been reviewed yet, so it's left out of the pass-rate math. The flow: 1. After a drain run, drain-cycle auto-writes a grade file at `~/.drain-cycle/grades/ABA-406.md` with `status: draft` and unchecked KR checkboxes (`grade_draft.py:77`, `_render`). 2. `grade` reads every file in that dir. Only files with `status: confirmed` count toward the rate; anything else is a draft, gets the stderr warning, and is excluded (`grade.py:100-110`). 3. ABA-406's file currently reads: ``` --- issue: ABA-406 status: draft --- ``` It was just generated today (run finished `2026-06-18T11:49`), so it hasn't been confirmed yet. ## How to clear it Review the draft and promote it. Open `~/.drain-cycle/grades/ABA-406.md`, fill in the `## KR check` checkboxes, and change `status: draft` → `status: confirmed`. On the next `grade` run the warning disappears and ABA-406 counts toward the rate. This is by design — the draft/confirmed split is the human-in-the-loop gate so an unreviewed run can't silently inflate (or deflate) your initiative pass-rate. It's the same mechanism the silent-Done violation check is built on (`grade.py` module docstring).
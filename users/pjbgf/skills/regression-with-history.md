---
name: regression-with-history
description: Reports a regression by anchoring it in git history ("N commits ago"), including the error message verbatim, and requesting both diagnosis and fix ideas. Triggers when a previously working feature breaks after recent commits.
---

pjbgf reports regressions by saying when something last worked in terms of commit distance,
quoting the error output directly (with placeholder `'...'` for variable parts), and issuing
a two-part request: "Find the problem and provide ideas on resolving it."

This is one of the longer message types — typically 2–4 sentences. The tone stays flat; no
frustration markers beyond the factual description of breakage.

**Example:**

> "The resume logic seem to have stopped working. The last time I checked it was 10 commits ago. Now when entire resume is executed we get \"Session '...' found in commit trailer but session log not available. Find the problem and provide ideas on resolving it."

Note "seem" (not "seems") — preserve this in role-play.

The phrase "Find the problem and provide ideas on resolving it" implies the user wants a
diagnosis + options list, not an immediate autonomous fix — they will pick the approach.

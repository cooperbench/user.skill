---
name: terse-scope-correction
description: When the agent finishes but missed part of the scope or acted on the wrong thing, petercr adds or redirects in one terse clause — no preamble. Trigger when the agent declares success on an incomplete or mis-scoped task.
---

petercr does not re-explain the full task. They identify the gap in one phrase and expect Claude to understand what was meant. If the agent asks a clarifying question, petercr answers with just the missing fact (often a path or filename in quotes).

**Patterns:**
- Missed file/ref: "also change [thing the agent missed]"
- Agent asks a question → bare answer: `"apps/frontend/public/favicon-dark.png"`
- Self-correction when they realize they caused the gap: "i forgot to upload new icons. i have added them, they work. now can we get the favicon to swap out for a different one in dark mode"
- Pointing to a file they already fixed: "ref in this file but i fixed it: /home/peterc/ccw/apps/frontend/src/lib/seo.ts"

**Examples:**

> "also change the web-app-manifest files and refs in the webmanifest"

> "also do og-image"

> "ref in this file but i fixed it: /home/peterc/ccw/apps/frontend/src/lib/seo.ts"

> "\"apps/frontend/public/favicon-dark.png\""

> "we need to adjust the headerPill size to be less than the formCard size. like we did with the rest of the headers"

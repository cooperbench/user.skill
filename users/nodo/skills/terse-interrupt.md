---
name: terse-interrupt
description: Ultra-short (1–3 word) steering messages mid-session. Triggered after interrupting the agent, after accepting a partial result, or when extending a fix to another file/area.
---

nodo frequently interrupts the agent mid-run and steers with minimal words. These messages are never capitalized and contain no punctuation beyond backticks for symbols. They assume full context from the conversation — nodo does not re-explain anything.

**Common forms:**

- Resume after interruption: `"resume"` / `"continue"`
- Accept and confirm: `"yes"`
- Extend to another file (using same pattern): `"same for \`cmd/entire/cli/agent/cursor/lifecycle_test.go\`"` / `"same for cmd/entire/cli/agent/cursor/transcript.go"`
- Ask what's left: `"which other outstanding issues we have?"`

**Verbatim examples:**

> `"resume"`

> `"continue"`

> `"yes"`

> `"same for \`cmd/entire/cli/agent/cursor/lifecycle_test.go\`"`

> `"same for cmd/entire/cli/agent/cursor/transcript.go"`

> `"which other outstanding issues we have?"`

> `"can you add a test for it?"`

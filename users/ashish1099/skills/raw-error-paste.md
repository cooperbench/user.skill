---
name: raw-error-paste
description: Reports a runtime failure by pasting the bare error string verbatim, no framing — triggered when the agent claims success but the program fails.
---

When the agent declares "everything builds and all tests pass" but a runtime error surfaces,
ashish1099 does not write "I got this error:" or "it failed with:". They paste the raw error
string exactly as it appeared — usually a colon-separated chain of context frames as produced
by Go's `fmt.Errorf` wrapping — and nothing else.

The absence of framing is itself information: it means "you said it worked, it didn't, here is
the evidence." The expectation is that the agent reads the error, identifies the root cause, and
fixes it without further prompting.

**Example:**
> "tag sync v1.4.4: checkout tag v1.4.4: reset v1.4.4: invalid reset option: object not found"

This led directly to a new session opening with a full annotated-tag-peeling fix plan,
suggesting ashish1099 diagnosed the root cause themselves and came back with the solution.

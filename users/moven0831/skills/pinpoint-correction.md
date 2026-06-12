---
name: pinpoint-correction
description: >
  Triggered when the agent states a specific fact incorrectly — wrong parameter name, missing
  field, wrong API shape, wrong key name. moven0831 corrects with surgical precision in one
  sentence or phrase, no explanation of impact.
---

When the agent gets a concrete detail wrong, moven0831 fires back with only the correct fact.
No "actually" or "I think". Just the correction, as if finishing a sentence.

**Verbatim examples**:

```
it's "moltbookApiKey"
```
(agent had used wrong parameter name in curl example)

```
the postinig api should have title
```
(agent listed post fields but omitted `title`; note: typo "postinig" preserved)

```
the agent name could be derived from the fake API key
```
(agent described a different derivation; user states the correct one)

```
flag this as verify after scaffolding and adapt
```
(agent was about to lock in an assumption; user redirects to defer verification)

```
what is the signedUp designed for?
```
(agent referred to a field without explaining it; user asks to surface the intent)

**Key traits**:
- The correction IS the full message — no pleasantries, no context
- Often reads like a fragment because the shared context is assumed
- May include a typo (user types fast and doesn't review)
- Does not explain why the agent was wrong or what the consequence would be

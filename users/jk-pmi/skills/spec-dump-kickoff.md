---
name: spec-dump-kickoff
description: >
  Trigger: user is starting a large, multi-file feature and wants to anchor the agent with
  a complete structured spec before it begins. One of the rare 200–990-word messages.
---

When the feature is too complex to describe tersely, the user writes a full structured spec. These are rare (~1% of messages) but highly distinctive: they look like a product requirements document with assumptions, out-of-scope items, numbered steps, and sometimes markdown tables.

Characteristics:
- Markdown headers (`##`) and bullet points
- Explicit "assumptions" and "out_of_scope" sections
- Numbered implementation steps
- Written in fluent English (not terse)
- Often also appears as a correction when the agent asked for the PLAN.json and the user dumps the real spec instead

## Example (opening a new-code session — 990 words total, truncated here)

```
{ "title": "Tenant Settings & Superuser Admin Pages",
  "summary": "Bring admin functionality from standalone tools/admin-ui/ into the main Next.js app...",
  "assumptions": [
    "The existing /admin/* endpoints in admin_api.py are unauthenticated — we will create new authenticated wrappers rather than modifying the existing ones",
    "The /auth/me endpoint exists but does not return is_superuser — we will extend it",
    ...
  ],
  "out_of_scope": [
    "Deleting or modifying tools/admin-ui/",
    "Mobile responsive design",
    ...
  ]
}
```

## Example (opening — feature concept, ~80 words)

```
Add a step to the dirigent. After finishing. Called "Entropy minimization". Its purpose is to align code and docs. As it stands today, agents write barely acceptable code and do nothing to reduce the entropy in your repository. What happens is that they change function X to have behavior B instead of behavior A, but all documentation still references behavior A. Your agent is not going to fix that for you.
Repeat this 100 times and you end up with an unmaintainable repository...
```

## Example (correction as spec — contract quality, ~376 words)

```
revamp the contract generation. it has two problems: 1. it is not agreed upon by executor and reviewer. 2. one run in the wild yielded useless grep-based criteria. acceptance criteria MUST BE USER BASED:
## What this contract actually tested
**File-level structural checks** — "does this string exist in this file?" That's it. Every verification is a grep or file_exists...
## What it missed entirely
| Gap | Example |
|-----|---------|
| **Request/response correctness** | Does `GET /tenants/1/settings` return valid JSON with all 8 fields? |
...
```

## When to use

After several terse sessions have accumulated context, when the user decides the next step is too important to leave vague. Or when the agent just proved it doesn't understand what's needed and the user writes the spec to eliminate ambiguity.

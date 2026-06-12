---
name: raw-paste-kickoff
description: When camkeith has a well-formed spec or raw artifact, he pastes it verbatim without cleanup or framing. Triggered for large design specs, error logs, YAML configs, LinkedIn data dumps, or CloudFront access logs.
---

When camkeith knows exactly what he wants (rare) or needs to hand off raw content, he pastes it directly — no fencing, no curation, no commentary. The agent receives it and must figure out what to do.

**Contexts where this appears:**
- **Design specs:** A 500–1000 word plan already written, pasted with just "Implement the following plan:" as a prefix
- **Error logs:** Browser console errors or AWS CloudFront logs pasted wholesale, no curation
- **Build configs:** Raw YAML (`amplify.yml`) pasted inline
- **Raw data:** LinkedIn skills blob (1,091 words including HTML artifacts and repetitions) followed by a cleanup instruction

**Examples:**

> `"Implement the following plan: # Fix Green Accents + Terminal Auto-Boot Redesign..."` (549+ words)

> `"why does grok send me here: http://localhost:3000/..."` followed by raw chat output and CloudFront log lines

> Pastes a 1,091-word LinkedIn skills blob, then: `"remove any duplicates, rank them by importance, and discard any irrelevant ones:"`

> Pastes `amplify.yml` YAML without explanation after a deployment failure discussion

When playing camkeith: paste the raw artifact with a short (≤5 word) prefix or no prefix. Do not clean it up. Do not explain what it is.

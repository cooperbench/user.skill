---
name: security-finding-dump
description: Trigger — schmalle pastes an individual security review finding (OWASP category, CWE, file path, line number, code snippet, recommended fix) as his entire prompt and expects implementation.
---

## Behavior

After running a full parallel security audit (4 sub-agents covering crypto, injection, file handling, frontend), schmalle receives a structured security report. He then pastes individual findings back — one per prompt or a comma-separated list of finding IDs — and expects the agent to implement the fix.

Findings are structured markdown from the agent's own output, which schmalle pastes back verbatim. He does not rephrase them or add commentary. The finding already contains everything needed.

**Single finding paste** — the entire finding as markdown:
> `### H-05: JWKS Validation Falls Back to Unverified JWT Parsing`  
> `**File:** .../JwksValidationService.kt (lines 52-55, 253-268)`  
> `**Description:** When no JWKS URI is configured...`  
> `**Recommended Fix:** Return null (reject the token) when JWKS URI is not configured...`

**Finding ID list** — terse, expects the agent to look up context:
> `implement findings HI-3, HI-5, HI-9, HI-10, ME-1, ME-2, ME-3, ME-4, ME-5, ME-7-HI-7, HI-1, HI-4, HI-8`

**Severity-scoped batch**:
> `& fix vulns with prio 0 (vulns 1,2,3,4,5)`  
> `now fix all prio 3 vulnerabilities`  
> `fix all findings identified`

## Simulation rule

When playing schmalle in a security session, paste the full finding markdown exactly as the agent produced it. Do NOT rephrase. Do NOT add "please" or "can you". Do NOT explain why the finding matters — the agent's own finding already did that. For batches, use comma-separated IDs or severity group labels.

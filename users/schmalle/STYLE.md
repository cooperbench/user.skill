---
name: schmalle-style
description: Typing fingerprint — message length, casing, punctuation, typos, image references, verbatim calibration quotes.
---

## Message length

| Stat | Value |
|------|-------|
| Median | **37 words** (bimodal: either <10 words or 300–2900 word plan pastes) |
| p90 | 455 words |
| Max | 2901 words |

Schalle's messages are bimodal. Mid-session steering is extremely terse (1–10 words). Opening prompts are either similarly terse (a screenshot + 1 sentence) OR enormous plan-pastes verbatim from speckit output (300–2900 words, fully structured markdown with file paths, code blocks, and numbered steps). There is almost no middle ground.

## Language
English only. Non-native: occasional wrong prepositions ("mapped to two" → "mapped to"), missing articles, subject–verb agreement looseness.

## Capitalization
- **Personal pronoun "i"**: always lowercase.
- **Sentence starts**: usually lowercase unless the message is a pasted plan (agent-generated markdown).
- **CVE IDs, OWASP categories, file paths**: correctly cased as written in context.
- **Product names**: CrowdStrike, AWS, Kotlin, React — correctly cased.

## Punctuation
- Periods: often omitted at end of short messages.
- Commas: used but sometimes missing.
- Apostrophes: **almost never** — "dont", "havent", "cant", "ive", "im".
- Question marks: used when explicitly asking a question, but many questions have no `?`.
- No exclamation marks.
- No emoji.

## Typo patterns (preserve exactly)
| Typed | Intended |
|-------|----------|
| ownershop | ownership |
| execption | exception |
| Doamin | Domain |
| depencenies | dependencies |
| fi | fix |
| two | to |
| prio | priority |
| havent | haven't |
| dont | don't |
| cant | can't |

## Image references
Attaches images with no preamble (`[Image: image/png]`) or with minimal context like "see image" or "see the image". Often the image IS the bug report with no other text.

## Formatting
- Long prompts use the agent's generated markdown exactly (headers, code blocks, file paths).
- Short prompts use plain prose, no markdown.
- File paths: referenced by name (`AssetManagement.tsx`, `application.yml`) without surrounding backticks in short messages.
- Numbered finding IDs: uses compound notation like "HI-3, HI-5, HI-9" or "vulns 1,2,3,4,5".

---

## Calibration quotes (verbatim, spanning openings, steering, and pushback)

**Terse opening (screenshot + sentence):**
> `please fix this warnings`  
> `[Image: image/png]`

> `add an account-id column in the table and populate it`  
> `[Image: image/png]`

> `fix this bug in the export function, i tried exporting vulnerabilies and exporting assets`  
> `[Image: image/png]`

**Short instructional opening:**
> `if an instance id from AWS is available, also show this in the UI`  
> `[Image: image/png]`

> `i want to be able to download all reviews (if a reviewer answered CHANGE or NOGO including comments) in an Excel speedsheet, named Review.(ReleaseNumber).Date.xlsx (Use the relevant release number)`  
> `[Image: image/png]`

**Mid-session one-liners (non-pushback):**
> `yes`

> `b`

> `A`

> `fix all findings identified`

> `now fix all prio 3 vulnerabilities`

> `& fix vulns with prio 0 (vulns 1,2,3,4,5)`

**Mid-session correction (terse redirect):**
> `also hide Doamin vulns for users with ADMIN role`

> `rename Days open to Open`  
> `[Image: image/png]`

> `save to database button must only be visible for admins`  
> `[Image: image/png]`

> `upgrade all dependecnies in the frontend where possible`

**Failure report:**
> `i dont see the change in the UI ? See the image, i would expect a listbox below the domain to select one of the available domaina`  
> `[Image: image/png]`

> `as secmanadmin (pw is secmanadmin also) i have assigned the ownershop of an asset to to secmanuser, but when i log into secmanuser, i can see only 0 assets. Please evaluate, why this assignment of assets is not working.`

> `something is wrong, i tried to approve an exception, but i still see it, but at the same time I see 0 pending exceptions, please carefully review the behavior and propose a fi.`  
> `[Image: image/png]`

**Analytical opening (longer):**
> `please have a look at the UI, there are vulnerabilities shown, which are less than 30 days open and already shown as overdue. I havent imported new Crowdstrike data here for ages, maybe something in the import is wrong, maybe only the UI calculation is wrong. Please propose a holistic fixing plan`  
> `[Image: image/png]`

> `please carefully analyze this misbehavior, i just wanted from the command line to list a bucket with mappings and i get after the listing an error in regards of a failed requirement ID migration at start. When using the CLI i dont expect after executing the s3 related behavior to see any requirement related migrations. Please carefully create a plan how to this fix. Propose options, give recommendations.`

**Serial iteration (chained corrections):**
> `if a user, who is not ADMIN or SECCHAMPION, has no workgroups, the subitem "WG vulns" under Vulnerability management must not be shown`

> `if a user, who is not ADMIN or SECCHAMPION, has no AWS accounts (direct or shared), the subitem "Account vulns" under Vulnerability management must not be shown`

> `if a user, who is not ADMIN or SECCHAMPION, has no domains mapped (direct or shared), the subitem "Domain vulns" under Vulnerability management must not be shown`

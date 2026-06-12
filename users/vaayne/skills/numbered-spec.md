---
name: numbered-spec
description: When vaayne has 4+ requirements to communicate at once, they write a dense inline numbered list with no surrounding prose
---

For complex multi-point corrections or specs, vaayne drops into a numbered list with no introductory sentence. Numbers run without line breaks — it reads like a stream of requirements. Each point is terse; some have sub-detail, most are a single phrase. Numbering is inconsistent (sometimes "6.  olny" with double space, sometimes "7 support" without a period).

**Verbatim example (plugin spec, 7 points):**

> `1. go plugin start with tool + lifecycle 2. expose some basic APIs. 3. yes, the config should have more field like path from local or remote, plugin config it self or anything plugin needed. 4. start with simple, fit anna project. 5. js should have same management with go. 6.  olny with granted API. 7 support local go file first, same as js, start from simple, only support local go and js file as plugin`

**Characteristics:**
- No line breaks between numbered items
- No introductory sentence ("here are my requirements:")
- Typos preserved in each item (olny, complie, etc.)
- Period usage inconsistent — some items end with a period, some don't
- Can mix affirmation ("yes, the config should...") mid-list when agreeing with a prior agent suggestion

> DEVELOPER

CLAUDE_CODE_NEW_INIT=true

> AGENT

Ready.

> AGENT

The CLAUDE.md already exists and is shown in context. Let me check for any gaps by looking at additional config files.

> AGENT

The existing CLAUDE.md is comprehensive. Key gaps I found:

1. **Node/npm versions are stale** — package.json requires `>=v24.13.0` / `>=11.0.0`, not v22/v10
2. **No single-test command** — requested by /init
3. **Named parameters rule missing** — copilot instructions mandate named-only params
4. **DB read/write pattern not shown** — copilot has concrete example
5. **BigQuery missing** from key dependencies

Here are the targeted changes:

> AGENT

Now add single-test commands to the Key Commands section:

> AGENT

Now add the named parameters rule and DB read/write pattern to the Common Patterns / Development Rules section:

> AGENT

Now add BigQuery to key dependencies:

> AGENT

Done. Changes made to CLAUDE.md:

1. **Node.js** `>=v22.14.0` → `>=v24.13.0`, **npm** `>=10.9.2` → `>=11.0.0`
2. **Single test commands** added under Testing section
3. **Named parameters rule** added as a critical section under Development Rules
4. **DB read/write pattern** with code example added
5. **BigQuery** added to key dependencies

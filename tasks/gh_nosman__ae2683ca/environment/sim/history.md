> DEVELOPER

Let's show token usage for each session, anywhere there is a sessions table

> AGENT

Let me explore the session display code to understand what's currently shown.

> AGENT

Now let me check how `tokens_used` is stored in the DB and how sessions are queried:

> AGENT

Now let me check how `tokens_used` is populated from JSONL/ingest:

> AGENT

Let me check the ingest pipeline to see how sessions are inserted:

> AGENT

Now I have a clear picture. `tokens_used` is in the DB schema but never populated. I'll: 1. Add `tokens_used` to `DisplaySession`, fetching from DB and computing from local JSONL files 2. Show it in both session list TUIs

> AGENT

Now update `query_db` to fetch `tokens_used` from the DB:

> AGENT

Now update the SQL `cols` to include `tokens_used`:

> AGENT

Now update `ParsedJsonl` to include `tokens_used` and compute it in `parse_jsonl`:

> AGENT

Now update `augment_with_jsonls` to apply `tokens_used` from parsed JSONL:

> AGENT

Now update the `sessions.push` for new untracked sessions to include `tokens_used`:

> AGENT

Now add the tokens column to `sessions.rs` `draw()`:

> AGENT

Now add the tokens column to the line rendering in `sessions.rs`:

> AGENT

Now do the same for `status.rs` `draw_sessions()`:

> AGENT

Now build to check for errors:

> AGENT

Clean build. Now install:

> AGENT

Done. Token usage is now shown in both session list TUIs. Here's what changed: - **`session_list.rs`**: Added `tokens_used: i64` to `DisplaySession`, a `fmt_tokens()` helper (`45k`, `1.2M`, etc.), DB column fetch, and JSONL parsing that sums `output_tokens` across all assistant turns - **`sessions.rs`** and **`status.rs`**: Both `draw` functions now compute a `tokens_w` column (only non-zero if any session has token data) and render it right-aligned in dim text before the session ID/timestamp The column only appears when at least one session has token data. Sessions that are only in the DB (never locally cached as JSONL) will show blank until the indexing pipeline is updated to populate `tokens_used`.
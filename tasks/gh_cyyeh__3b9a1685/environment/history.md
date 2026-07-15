> DEVELOPER

in ui agent mode, if thinking block content is too wide, make it scrollable instead of expanding to the global view

> AGENT

Let me explore the codebase to find the relevant UI components for the thinking block in agent mode.

> AGENT

Now let me read the key files to understand the exact current styling and identify what needs to change.

> AGENT

Now let me also check the AgentPanel and App styles to understand the parent container constraints.

> AGENT

I can see the issue. The thinking block's expanded content (`.message-bubble__thinking-body`) has no overflow constraint, and the parent `.message-bubble__segment--thinking` also has no `overflow` or `min-width: 0` set. This means wide content (long code lines, wide tables) will push the entire layout wider. The fix needs to: 1. Add `overflow-x: auto` to the thinking body so wide content scrolls 2. Add `min-width: 0` to the thinking segment to allow it to shrink within flex layouts

> AGENT

Also need to ensure the message bubble itself constrains its children in agent mode. Let me also add `overflow: hidden` and `min-width: 0` to the message bubble for assistant messages, since it's in a flex layout too.

> AGENT

Now let me also check if the messages container needs a fix - it has `overflow-y: auto` but no width constraint that would prevent horizontal expansion.

> AGENT

The `.agent-panel__messages` container should also be constrained. Let me add `overflow-x: hidden` to prevent horizontal expansion at the messages container level.

> AGENT

Here's a summary of the changes: **`MessageBubble.css`:** - `.message-bubble__segment--thinking` — added `overflow: hidden; min-width: 0;` so the thinking block container constrains its children - `.message-bubble__segments` — added `min-width: 0;` to allow flex shrinking - `.message-bubble__thinking-body` — added `overflow-x: auto; min-width: 0;` so wide content inside the expanded thinking block scrolls horizontally instead of pushing the layout wider **`AgentPanel.css`:** - `.agent-panel__messages` — added `overflow-x: hidden; min-width: 0;` to prevent any child content from expanding the messages container horizontally The key idea: the thinking body now scrolls horizontally (`overflow-x: auto`) for wide content, while its parent uses `overflow: hidden` to act as a containment boundary. The `min-width: 0` on flex children prevents the default behavior where flex items refuse to shrink below their content size.

> DEVELOPER

now the issue is that query result content is too wide

> AGENT

Let me check the InlineQueryResult component and its styles.

> AGENT

The `.inline-query__table-wrapper` already has `overflow-x: auto`, which is correct. The problem is that `.inline-query` itself has `overflow: hidden` but no width constraint — when it's inside the thinking block, it can still push its parent wider because there's no `max-width` or `min-width: 0` to contain it within the flex layout. The fix: the `.inline-query` container and its parent `.message-bubble__tool-segment` need to be constrained so they don't expand beyond their parent.

> AGENT

Also, the `.inline-query` needs `min-width: 0` and the table inside needs to not force `width: 100%` when the content is wider than the container.

> AGENT

Now let me re-read the current state of both files to verify everything looks correct.

> AGENT

The changes look good. Here's what was added to fix the wide query result content: **`MessageBubble.css`** — `.message-bubble__tool-segment`: added `min-width: 0; overflow: hidden;` so the tool segment wrapper constrains the inline query result within the thinking block's bounds. **`InlineQueryResult.css`** — `.inline-query`: added `min-width: 0; max-width: 100%;` so the query result card respects its parent's width. The overflow chain now works correctly: wide table content scrolls inside `.inline-query__table-wrapper` (which already had `overflow-x: auto`), and the parent containers are properly constrained so nothing pushes the global layout wider.

> DEVELOPER

try it out

> AGENT

Both servers are running. The app is available at **http://localhost:5173/**. Go ahead and test it in your browser — try a query that produces wide results (like `SELECT * FROM titanic`) and check that the content scrolls within the thinking block instead of expanding the view.
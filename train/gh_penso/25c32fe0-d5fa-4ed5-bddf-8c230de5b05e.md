> DEVELOPER

All channels have a bunch of commands like /new /compact etc. I think Matrix does not, plan to add all those commands in Matrix too.

> AGENT

Let me explore the existing channel command implementations and the Matrix channel to understand the gap.

> AGENT

Now let me look at the Matrix handler and a simple reference (WhatsApp) to understand the exact code changes needed.

> AGENT

Now I have a clear picture. The key insertion point is in `handle_room_message` around line 319-376 where the text message is dispatched to chat. I need to add a slash command check before `sink.dispatch_to_chat()`, similar to WhatsApp/Teams. Let me also check how Matrix sends text responses.

> AGENT

Now I have the full picture. Let me also check the Telegram help handler to understand what help text looks like, since we should add a local `/help` handler for Matrix too.

> AGENT

Now let me also check the Telegram `should_intercept_slash_command` to understand the full command interception pattern.

> AGENT

Good. Now I have a complete understanding. Let me plan the implementation. The pattern is straightforward — in `handle_room_message`, right before `sink.dispatch_to_chat()` (line 376), I need to intercept slash commands, dispatch them via `sink.dispatch_command()`, and send the response back via `send_text()`. I'll also handle `/help` locally like Telegram does. Let me also check if there's anything in the text message flow between access check and dispatch that I need to be careful about (like the ack reaction — commands should probably still get the ack).

> AGENT

Now let me implement the slash command handling. The insertion point is in `handle_room_message`, right after the text message kind check and before `sink.dispatch_to_chat()`. I need to intercept `/` prefixed text messages. Looking at the code flow (lines 319-377), the text dispatch happens inside `if let Some(sink) = &event_sink { ... }`. The slash command check should go right before the `sink.dispatch_to_chat(&body, reply_to, meta).await;` call on line 376, after the location coordinate check.

> AGENT

Now I'll add the slash command interception right before `dispatch_to_chat`:

> AGENT

Now I need to add the `HELP_TEXT` constant. Let me add it near the top of the file, after the existing constant:

> AGENT

Let me verify the code compiles:

> AGENT

Compiles clean. Now let me add tests. Let me look at existing tests in the Matrix handler to follow the same patterns:

> AGENT

Now let me see the end of the test file to add new tests:

> AGENT

The tests in this file are unit tests for helper functions. The command interception I added is inline in the async handler, so I should add a test for `HELP_TEXT` content and verify the command detection logic. But actually, the core logic is simple — it just checks `body.strip_prefix('/')` and calls `dispatch_command`. The integration test coverage comes from the gateway's `dispatch_command` tests. Let me add a test for `HELP_TEXT` and the command detection pattern:

> AGENT

All tests pass. Now let me run the format check and clippy:

> AGENT

The clippy failure is from CUDA (pre-existing, not related to my change). Let me fix the formatting and run clippy just on the matrix crate:

> AGENT

Clean. Let me verify the final state of the changes:

> AGENT

Here's a summary of the changes: **`crates/matrix/src/handler.rs`** — two additions: 1. **`HELP_TEXT` constant** (line 51): Lists all 12 slash commands with descriptions, matching Telegram's help text but also including `/peek` and `/stop`. 2. **Command interception** (line 390): Before `dispatch_to_chat()`, checks if a text message starts with `/`. If it's `/help`, returns the local help text. For all other commands, delegates to `sink.dispatch_command()` — the same gateway dispatcher that WhatsApp, Teams, Telegram, Discord, and Slack all use. Sends the response (or error) back to the room via `send_text()`. 3. **Two tests**: Verifies `HELP_TEXT` mentions all 12 commands and that the slash prefix detection logic works. The pattern follows the simplest approach used by WhatsApp and Teams (text-based `/` prefix detection), which is the natural fit for Matrix.

> AGENT

Ready to commit when you'd like — single file change, 72 lines added to `crates/matrix/src/handler.rs`.

> DEVELOPER

commit push create a PR

> AGENT

PR created: https://github.com/moltis-org/moltis/pull/590

> DEVELOPER

Fix PR comments

> AGENT

Valid point — `starts_with("help")` would match `/helpme`, `/helper`, etc. I'll use the gateway idiom of extracting the command name via `split_whitespace`.

> AGENT

All 95 tests pass, formatting clean.

> AGENT

Pushed. The fix extracts the command name with `split_whitespace().next()` before comparing to `"help"`, so `/helpme` etc. won't incorrectly match.

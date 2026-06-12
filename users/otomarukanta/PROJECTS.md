# Projects — otomarukanta

## otomarukanta/slk ★ dominant repo (100% of sessions)

**What it is**: A personal Rust CLI tool for reading and exporting Slack thread messages.
Name is likely short for "slack".

**Tech stack**:
- Language: Rust
- HTTP: system `curl` (no async runtime, no HTTP crate)
- JSON: custom `json::parse` (no `serde_json`)
- TLS: `rustls` + `rcgen` (added during OAuth work)
- Auth: `SLACK_TOKEN` env var, with `slk login` OAuth flow added
- Config: XDG config dir (`~/.config/slk/`), credentials stored at `0o600`

**Module structure** (visible from specs):
- `src/main.rs` — CLI entrypoint, argument parsing, `run()`, `resolve_user_names()`
- `src/message.rs` — message parsing, `extract_messages()`, `resolve_user_name()`, `format_messages()`
- `src/slack_api.rs` — Slack API calls via curl (`fetch_thread_replies()`, `fetch_user_info()`)
- `src/error.rs` — `SlkError` type
- `src/json.rs` — JSON parser
- `src/url.rs` — URL utilities
- `src/config.rs` — config dir, token load/save, client credentials (added during OAuth work)
- `src/oauth.rs` — OAuth flow (added during OAuth work)

**Recurring themes**:
- Slack API error handling: checking `ok` field, surfacing `needed`/`provided` scopes on permission errors
- OAuth flow iteration: went through manual URL paste → HTTPS local server → state+polling
- User display name resolution: mapping `U`-prefixed IDs to `@display_name` via `users.info` API
- Permission error propagation: converting silent failures into explicit `Result` errors

**Development pattern**: user plans each feature in Japanese detail, implements via agent,
commits immediately, then discovers a runtime or API issue and iterates.

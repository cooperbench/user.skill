---
session_id: 3a0d6abe-a088-44ee-affe-e84d4a2975fb
developer: "gh:penso"
split: train
source: entire
repo: moltis-org/moltis
start_time: "2026-04-14T10:43:42.721801Z"
n_turns: 21
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Check https://github.com/moltis-org/moltis/issues/543 and plan a fix

> AGENT

The issue is clear: Slack socket mode fails because `tungstenite` (the WebSocket library used by `slack-morphism`) doesn't have TLS enabled. Let me investigate the dependency chain.

> AGENT

Found it. Let me check the `slack-morphism` features more closely, and look at what features it needs for TLS.

> AGENT

Now I can see the full picture. Let me verify the `tokio-tungstenite` workspace dep to confirm it's missing TLS features.

> AGENT

Let me check what version of `tokio-tungstenite` slack-morphism actually depends on and verify the feature chain.

> AGENT

Now I have the complete picture. Let me verify one more thing to check if newer `slack-morphism` versions fix this.

> AGENT

Here's the analysis and plan. ## Root Cause `slack-morphism`'s `rustls-native-certs` feature (enabled by both `axum` and `hyper` features) maps to: ``` tokio-tungstenite/rustls-native-certs → only dep:rustls-native-certs (cert resolver) ``` But what's actually needed for `wss://` connections is: ``` tokio-tungstenite/rustls-tls-native-roots → __rustls-tls + rustls-native-certs (full TLS stack) ``` The resolved features on `tokio-tungstenite` 0.28.0 confirm it — `rustls`, `tokio-rustls`, and `tungstenite/__rustls-tls` are all missing: ``` Resolved: ["connect", "default", "handshake", "rustls-native-certs", "stream"] Missing: ["__rustls-tls", "rustls", "rustls-pki-types", "tokio-rustls"] ``` This is an upstream bug in `slack-morphism` (present in both 2.6 and 2.18). ## Fix Add `tokio-tungstenite` 0.28 with the correct feature to `crates/slack/Cargo.toml`. Cargo's feature unification will enable the full TLS stack on the same 0.28.0 that `slack-morphism` already pulls in: ```toml # Workaround: slack-morphism enables tokio-tungstenite/rustls-native-certs # (cert resolver only) instead of rustls-tls-native-roots (full TLS stack). # This forces the correct feature on the unified tokio-tungstenite 0.28. tokio-tungstenite = { version = "0.28", features = ["rustls-tls-native-roots"] } ``` This can't go through `workspace = true` since the workspace dep is 0.26 (used by `providers`, `httpd`, `node-host`). The 0.26 and 0.28 versions are semver-incompatible and resolve separately — this only affects the 0.28 instance used by `slack-morphism`. We should also file an upstream issue on `slack-morphism` so the feature mapping gets fixed at the source. Want me to implement this fix?

> DEVELOPER

Is this blocking slack use at all? Is a newer version already available for slack-morphism?

> AGENT

**Yes, this completely blocks Slack socket mode.** Without TLS, the WebSocket client can't connect to `wss://wss-primary.slack.com` at all — there's no fallback. As for versions — `slack-morphism` 2.20.0 is the latest on crates.io, and we're resolving 2.18.0 (workspace declares `^2.6`). But as I showed, even 2.18.0 has the same broken feature mapping (`tokio-tungstenite/rustls-native-certs` instead of `rustls-tls-native-roots`). Let me quickly check if 2.20.0 fixes it.

> AGENT

This confirms it — **version 2.20.0 fixes the bug.** The `rustls-native-certs` feature in 2.20.0 adds the missing `tokio-tungstenite/rustls-tls-native-roots`: | Version | `rustls-native-certs` feature enables | |---------|--------------------------------------| | 2.18.0 | `tokio-tungstenite/rustls-native-certs` (cert resolver only) | | 2.20.0 | `tokio-tungstenite/rustls-native-certs` **+ `tokio-tungstenite/rustls-tls-native-roots`** (full TLS) | So the fix simplifies to just bumping the version constraint in the workspace `Cargo.toml`: ```toml slack-morphism = { features = ["axum", "hyper"], version = "2.20" } ``` No workaround dependency needed. We should check for any breaking API changes between 2.18 and 2.20 in `crates/slack/`, but given it's the same major version it's likely compatible. Want me to implement this?

> DEVELOPER

proceed

> AGENT

Now let me check for any API usage that might break with the version bump, then apply the fix.

> AGENT

The API usage is all via `slack_morphism::prelude::*` — standard types that are stable across 2.x. The bump should be safe. Let me apply the fix.

> AGENT

Now let me update the lockfile and verify it compiles.

> AGENT

Resolved cleanly — `slack-morphism` 2.18.0 → 2.20.0, and it pulled in `tokio-tungstenite` 0.29.0 (newer than 0.28). Let me verify the TLS features are now enabled.

> AGENT

The full TLS stack is now enabled: `__rustls-tls`, `rustls`, `tokio-rustls`, `rustls-tls-native-roots`. Let me verify it compiles.

> AGENT

Compiles cleanly with zero warnings. Let me also run the slack tests.

> AGENT

All 70 tests pass. Let me close the issue and commit.

> AGENT

Done. Here's the summary: **Fix:** Bumped `slack-morphism` from `2.6` (resolved 2.18.0) to `2.20` in workspace `Cargo.toml`. **Root cause:** `slack-morphism` 2.18's `rustls-native-certs` feature only enabled `tokio-tungstenite/rustls-native-certs` (the certificate resolver), not `tokio-tungstenite/rustls-tls-native-roots` (the full TLS stack). Version 2.20 adds the missing feature flag. **Verification:** - `tokio-tungstenite` now resolves to 0.29.0 with full TLS features: `__rustls-tls`, `rustls`, `tokio-rustls`, `rustls-tls-native-roots` - `cargo check -p moltis-slack` — clean - All 70 slack tests pass The changes are in `Cargo.toml` (version bump) and `Cargo.lock` (dependency update). Ready to commit when you'd like.

> DEVELOPER

commit push create a PR

> AGENT

PR created: https://github.com/moltis-org/moltis/pull/707

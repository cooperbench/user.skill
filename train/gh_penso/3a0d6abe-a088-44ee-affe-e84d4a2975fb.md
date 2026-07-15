> DEVELOPER

Check https://github.com/moltis-org/moltis/issues/543 and plan a fix

> TOOL

tool_use Bash
id: toolu_01XqtQ2BPMXQBJHDR47Hx6LP
```json
{
  "command": "gh issue view 543 --json title,body,labels,state,comments",
  "description": "Fetch GitHub issue #543 details"
}
```

> TOOL

tool_result
id: toolu_01XqtQ2BPMXQBJHDR47Hx6LP
```
{"body":"### Preflight Checklist\n\n- [x] I have searched [existing issues](https://github.com/moltis-org/moltis/issues?q=is%3Aissue+label%3Abug) and this hasn't been reported yet\n- [x] I am using the latest version of Moltis\n- [ ] If this happened during a chat session, I included as much full session context as possible and redacted secrets\n\n### What happened?\n\nFollowing the [guide](https://docs.moltis.org/slack.html?highlight=slack#slack) and setting up Slack with socket mode. I keep getting:\n\n```\n11:20:28 AM.836\nERROR\nslack_morphism::hyper_tokio::socket_mode::tungstenite_wss_client\n[1/1/0] Unable to connect wss://wss-primary.slack.com/link/<truncated>: Url(TlsFeatureNotEnabled) slack_wss_client_id=1/1/0\n```\n\n It seems the Tls feature needs to enabled.\n\nAn LLM suggested the following:\nThis is a build configuration bug — the tungstenite websocket crate used by slack_morphism for Socket Mode doesn't have TLS enabled.\n\nThe situation:\n- You're on the latest release (20260328.03)\n- --version showing 0.1.0 is a cosmetic issue (hardcoded in Cargo.toml)\n- The Slack TLS error is a real bug that needs to be reported\n\n### Expected behavior\n\nIt should connect to slack correctly.\n\n### Steps to reproduce\n\nConfigure this with correct credentials:\n```\n[channels.slack.my-bot]\nbot_token = \"[REDACTED_SLACK]\"\napp_token = \"xapp-your-app-token\"\n```\n\nRun moltis, check logs\n\n### Did this happen during a chat session?\n\nNo\n\n### Chat session context (if applicable)\n\n```markdown\n\n```\n\n### Error messages / logs\n\n```shell\n11:20:28 AM.836\nERROR\nslack_morphism::hyper_tokio::socket_mode::tungstenite_wss_client\n[1/1/0] Unable to connect wss://wss-primary.slack.com/link/<truncated>: Url(TlsFeatureNotEnabled) slack_wss_client_id=1/1/0\n```\n\n### Is this a regression?\n\nI don't know\n\n### Last working version\n\n_No response_\n\n### Moltis version\n\nmoltis 0.1.0\n\n### Component\n\nChannels (Telegram, Discord, etc.)\n\n### Install method\n\nOther\n\n### Operating system\n\nUbuntu / Debian\n\n### Additional context\n\nInstalled using `curl -fsSL https://www.moltis.org/install.sh | sh`","comments":[],"labels":[{"id":"LA_kwDOREW6tc8AAAACWauzgQ","name":"bug","description":"Something isn't working","color":"d73a4a"}],"state":"OPEN","title":"[Bug]: Slack Client Built Without TLS support"}
```

> AGENT

The issue is clear: Slack socket mode fails because `tungstenite` (the WebSocket library used by `slack-morphism`) doesn't have TLS enabled. Let me investigate the dependency chain.

> TOOL

tool_use Grep
id: toolu_01VtRCskfMm6rw4V1QQ6LFM3
```json
{
  "pattern": "slack.morphism|slack_morphism",
  "glob": "**/Cargo.toml",
  "output_mode": "content"
}
```

> TOOL

tool_use Grep
id: toolu_01Fff85aBFteo1mCyUwGV1HF
```json
{
  "pattern": "tungstenite",
  "glob": "**/Cargo.toml",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01Fff85aBFteo1mCyUwGV1HF
```
Cargo.toml:188:tokio-tungstenite = "0.26"
crates/providers/Cargo.toml:38:tokio-tungstenite = { workspace = true }
crates/httpd/Cargo.toml:54:tokio-tungstenite     = { workspace = true }
crates/node-host/Cargo.toml:21:tokio-tungstenite = { workspace = true }
```

> TOOL

tool_result
id: toolu_01VtRCskfMm6rw4V1QQ6LFM3
```
Cargo.toml:217:slack-morphism     = { features = ["axum", "hyper"], version = "2.6" }
crates/slack/Cargo.toml:20:slack-morphism  = { workspace = true }
```

> AGENT

Found it. Let me check the `slack-morphism` features more closely, and look at what features it needs for TLS.

> TOOL

tool_use Read
id: toolu_01TeoJfWBBvKg9tpmeE3rFQh
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/Cargo.toml",
  "offset": 210,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01TeoJfWBBvKg9tpmeE3rFQh
```
   210→nostr-sdk          = { features = ["nip04", "nip44"], version = "0.44" }
   211→open               = "5.3"
   212→rand               = "0.10"
   213→regex              = "1"
   214→secrecy            = { features = ["serde"], version = "0.8" }
   215→serenity           = { features = ["cache", "client", "gateway", "model", "rustls_backend"], version = "0.12" }
   216→sha2               = "0.10"
   217→slack-morphism     = { features = ["axum", "hyper"], version = "2.6" }
   218→sled               = "0.34"
   219→sysinfo            = "0.34"
   220→teloxide           = { features = ["macros"], version = "0.13" }
   221→# WhatsApp (sqlite-storage disabled to avoid libsqlite3-sys conflict with sqlx;
   222→# re-enable once sqlx 0.9 stabilises).
   223→wacore                         = "0.2"
   224→wacore-binary                  = "0.2"
```

> TOOL

tool_use Bash
id: toolu_01EeDttL96KtxQTKdSXU4oJC
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '.packages[] | select(.name == \"slack-morphism\") | .features' 2>/dev/null | head -40",
  "description": "Check slack-morphism available features"
}
```

> TOOL

tool_use Read
id: toolu_018JWwKiDiovqpX4qZKsmgjo
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack/Cargo.toml"
}
```

> TOOL

tool_result
id: toolu_01EeDttL96KtxQTKdSXU4oJC
```
{
  "axum": [
    "axum-base",
    "hyper-base",
    "rustls-native-certs"
  ],
  "axum-base": [
    "hyper-base",
    "dep:axum",
    "dep:tower"
  ],
  "default": [],
  "hyper": [
    "hyper-base",
    "rustls-native-certs"
  ],
  "hyper-base": [
    "dep:tokio",
    "dep:http-body-util",
    "dep:hyper",
    "dep:hyper-rustls",
    "dep:hyper-util",
    "dep:tokio-stream",
    "dep:tokio-tungstenite",
    "dep:signal-hook",
    "dep:signal-hook-tokio",
    "signature-verifier"
  ],
  "rustls-native-certs": [
    "tokio-tungstenite/rustls-native-certs",
    "hyper-rustls/rustls-native-certs",
    "hyper-rustls/ring"
  ],
  "signature-verifier": [
    "dep:sha2",
    "dep:subtle",
    "dep:hmac"
  ]
}
```

> TOOL

tool_result
id: toolu_018JWwKiDiovqpX4qZKsmgjo
```
     1→[package]
     2→edition.workspace = true
     3→name              = "moltis-slack"
     4→version.workspace = true
     5→
     6→[dependencies]
     7→async-trait     = { workspace = true }
     8→base64          = { workspace = true }
     9→bytes           = { workspace = true }
    10→hmac            = { workspace = true }
    11→http            = { workspace = true }
    12→moltis-channels = { workspace = true }
    13→moltis-common   = { workspace = true }
    14→moltis-metrics  = { optional = true, workspace = true }
    15→reqwest         = { workspace = true }
    16→secrecy         = { workspace = true }
    17→serde           = { workspace = true }
    18→serde_json      = { workspace = true }
    19→sha2            = { workspace = true }
    20→slack-morphism  = { workspace = true }
    21→tokio           = { workspace = true }
    22→tokio-util      = { workspace = true }
    23→tracing         = { workspace = true }
    24→
    25→[features]
    26→metrics = ["dep:moltis-metrics"]
    27→
    28→[lints]
    29→workspace = true
    30→
```

> AGENT

Now I can see the full picture. Let me verify the `tokio-tungstenite` workspace dep to confirm it's missing TLS features.

> TOOL

tool_use Read
id: toolu_01GX1VQyTcyGEGdT4cF7RkxZ
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/Cargo.toml",
  "offset": 185,
  "limit": 5
}
```

> TOOL

tool_result
id: toolu_01GX1VQyTcyGEGdT4cF7RkxZ
```
   185→tokio-util   = "0.7"
   186→# Config formats
   187→serde_yaml        = "0.9"
   188→tokio-tungstenite = "0.26"
   189→toml              = "0.8"
```

> AGENT

Let me check what version of `tokio-tungstenite` slack-morphism actually depends on and verify the feature chain.

> TOOL

tool_use Bash
id: toolu_01TJZN2uuZwM7g7vpzQPYNU4
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '[.packages[] | select(.name == \"slack-morphism\") | .dependencies[] | select(.name == \"tokio-tungstenite\")]'",
  "description": "Check slack-morphism's tokio-tungstenite dependency"
}
```

> TOOL

tool_use Bash
id: toolu_01JGtAUw9J2HCdunV95A1bnt
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '[.packages[] | select(.name == \"tokio-tungstenite\") | {name, version, features}]'",
  "description": "Check tokio-tungstenite versions and features"
}
```

> TOOL

tool_result
id: toolu_01TJZN2uuZwM7g7vpzQPYNU4
```
[
  {
    "name": "tokio-tungstenite",
    "source": "registry+https://github.com/rust-lang/crates.io-index",
    "req": "^0.28.0",
    "kind": null,
    "rename": null,
    "optional": true,
    "uses_default_features": true,
    "features": [],
    "target": null,
    "registry": null
  }
]
```

> TOOL

tool_result
id: toolu_01JGtAUw9J2HCdunV95A1bnt
```
[
  {
    "name": "tokio-tungstenite",
    "version": "0.21.0",
    "features": {
      "__rustls-tls": [
        "rustls",
        "rustls-pki-types",
        "tokio-rustls",
        "stream",
        "tungstenite/__rustls-tls",
        "handshake"
      ],
      "connect": [
        "stream",
        "tokio/net",
        "handshake"
      ],
      "default": [
        "connect",
        "handshake"
      ],
      "handshake": [
        "tungstenite/handshake"
      ],
      "native-tls": [
        "native-tls-crate",
        "tokio-native-tls",
        "stream",
        "tungstenite/native-tls",
        "handshake"
      ],
      "native-tls-crate": [
        "dep:native-tls-crate"
      ],
      "native-tls-vendored": [
        "native-tls",
        "native-tls-crate/vendored",
        "tungstenite/native-tls-vendored"
      ],
      "rustls": [
        "dep:rustls"
      ],
      "rustls-native-certs": [
        "dep:rustls-native-certs"
      ],
      "rustls-pki-types": [
        "dep:rustls-pki-types"
      ],
      "rustls-tls-native-roots": [
        "__rustls-tls",
        "rustls-native-certs"
      ],
      "rustls-tls-webpki-roots": [
        "__rustls-tls",
        "webpki-roots"
      ],
      "stream": [],
      "tokio-native-tls": [
        "dep:tokio-native-tls"
      ],
      "tokio-rustls": [
        "dep:tokio-rustls"
      ],
      "webpki-roots": [
        "dep:webpki-roots"
      ]
    }
  },
  {
    "name": "tokio-tungstenite",
    "version": "0.26.2",
    "features": {
      "__rustls-tls": [
        "rustls",
        "rustls-pki-types",
        "tokio-rustls",
        "stream",
        "tungstenite/__rustls-tls",
        "handshake"
      ],
      "connect": [
        "stream",
        "tokio/net",
        "handshake"
      ],
      "default": [
        "connect",
        "handshake"
      ],
      "handshake": [
        "tungstenite/handshake"
      ],
      "native-tls": [
        "native-tls-crate",
        "tokio-native-tls",
        "stream",
        "tungstenite/native-tls",
        "handshake"
      ],
      "native-tls-crate": [
        "dep:native-tls-crate"
      ],
      "native-tls-vendored": [
        "native-tls",
        "native-tls-crate/vendored",
        "tungstenite/native-tls-vendored"
      ],
      "rustls": [
        "dep:rustls"
      ],
      "rustls-native-certs": [
        "dep:rustls-native-certs"
      ],
      "rustls-pki-types": [
        "dep:rustls-pki-types"
      ],
      "rustls-tls-native-roots": [
        "__rustls-tls",
        "rustls-native-certs"
      ],
      "rustls-tls-webpki-roots": [
        "__rustls-tls",
        "webpki-roots"
      ],
      "stream": [],
      "tokio-native-tls": [
        "dep:tokio-native-tls"
      ],
      "tokio-rustls": [
        "dep:tokio-rustls"
      ],
      "url": [
        "tungstenite/url"
      ],
      "webpki-roots": [
        "dep:webpki-roots"
      ]
    }
  },
  {
    "name": "tokio-tungstenite",
    "version": "0.28.0",
    "features": {
      "__rustls-tls": [
        "rustls",
        "rustls-pki-types",
        "tokio-rustls",
        "stream",
        "tungstenite/__rustls-tls",
        "handshake"
      ],
      "connect": [
        "stream",
        "tokio/net",
        "handshake"
      ],
      "default": [
        "connect",
        "handshake"
      ],
      "handshake": [
        "tungstenite/handshake"
      ],
      "native-tls": [
        "native-tls-crate",
        "tokio-native-tls",
        "stream",
        "tungstenite/native-tls",
        "handshake"
      ],
      "native-tls-crate": [
        "dep:native-tls-crate"
      ],
      "native-tls-vendored": [
        "native-tls",
        "native-tls-crate/vendored",
        "tungstenite/native-tls-vendored"
      ],
      "rustls": [
        "dep:rustls"
      ],
      "rustls-native-certs": [
        "dep:rustls-native-certs"
      ],
      "rustls-pki-types": [
        "dep:rustls-pki-types"
      ],
      "rustls-tls-native-roots": [
        "__rustls-tls",
        "rustls-native-certs"
      ],
      "rustls-tls-webpki-roots": [
        "__rustls-tls",
        "webpki-roots"
      ],
      "stream": [],
      "tokio-native-tls": [
        "dep:tokio-native-tls"
      ],
      "tokio-rustls": [
        "dep:tokio-rustls"
      ],
      "url": [
        "tungstenite/url"
      ],
      "webpki-roots": [
        "dep:webpki-roots"
      ]
    }
  }
]
```

> TOOL

tool_use Bash
id: toolu_01MiibLwGYwEBQ4skWEHPMXh
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '[.packages[] | select(.name == \"slack-morphism\") | .dependencies[] | select(.name == \"tungstenite\")]'",
  "description": "Check slack-morphism's tungstenite dep"
}
```

> TOOL

tool_use Bash
id: toolu_014zSoythpeTznAyFaFLSTCw
```json
{
  "command": "cargo search slack-morphism 2>/dev/null | head -5",
  "description": "Check latest slack-morphism version"
}
```

> TOOL

tool_result
id: toolu_01MiibLwGYwEBQ4skWEHPMXh
```
[]
```

> TOOL

tool_use Bash
id: toolu_011Rt255rUApizvLrEWdk93j
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '.resolve.nodes[] | select(.id | contains(\"slack-morphism\")) | .deps[] | select(.name | contains(\"tungstenite\"))'",
  "description": "Check resolved features on slack-morphism's tungstenite"
}
```

> TOOL

tool_result
id: toolu_014zSoythpeTznAyFaFLSTCw
```
slack-morphism = "2.20.0"           # Slack Morphism is a modern client library for Slack Web/Events API/Socket Mode and Block Ki…
opencrabs = "0.3.7"                 # The autonomous, self-improving AI agent. Single Rust binary. Every channel. Install with: c…
slack-morphism-hyper = "0.41.0"     # Slack Morphism Hyper/Tokio support library
slack-morphism-models = "0.41.0"    # Slack Morphism Models
```

> TOOL

tool_result
id: toolu_011Rt255rUApizvLrEWdk93j
```
{
  "name": "tokio_tungstenite",
  "pkg": "registry+https://github.com/rust-lang/crates.io-index#tokio-tungstenite@0.28.0",
  "dep_kinds": [
    {
      "kind": null,
      "target": null
    }
  ]
}
```

> TOOL

tool_use Bash
id: toolu_01Qm1kwUW3yUug3uinCmDwua
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '.resolve.nodes[] | select(.id | contains(\"tokio-tungstenite@0.28\")) | .features'",
  "description": "Check resolved features on tokio-tungstenite 0.28"
}
```

> TOOL

tool_use Bash
id: toolu_01ES3Z3kfPcxH5TgdSXYhK5m
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '[.packages[] | select(.name == \"slack-morphism\") | .version]'",
  "description": "Check resolved slack-morphism version"
}
```

> TOOL

tool_result
id: toolu_01Qm1kwUW3yUug3uinCmDwua
```
[
  "connect",
  "default",
  "handshake",
  "rustls-native-certs",
  "stream"
]
```

> TOOL

tool_result
id: toolu_01ES3Z3kfPcxH5TgdSXYhK5m
```
[
  "2.18.0"
]
```

> AGENT

Now I have the complete picture. Let me verify one more thing to check if newer `slack-morphism` versions fix this.

> TOOL

tool_use Bash
id: toolu_01BuUzvDX5jkexbGqhzM46dy
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '[.packages[] | select(.name == \"slack-morphism\") | {version, features}]'",
  "description": "Check resolved slack-morphism features"
}
```

> TOOL

tool_result
id: toolu_01BuUzvDX5jkexbGqhzM46dy
```
[
  {
    "version": "2.18.0",
    "features": {
      "axum": [
        "axum-base",
        "hyper-base",
        "rustls-native-certs"
      ],
      "axum-base": [
        "hyper-base",
        "dep:axum",
        "dep:tower"
      ],
      "default": [],
      "hyper": [
        "hyper-base",
        "rustls-native-certs"
      ],
      "hyper-base": [
        "dep:tokio",
        "dep:http-body-util",
        "dep:hyper",
        "dep:hyper-rustls",
        "dep:hyper-util",
        "dep:tokio-stream",
        "dep:tokio-tungstenite",
        "dep:signal-hook",
        "dep:signal-hook-tokio",
        "signature-verifier"
      ],
      "rustls-native-certs": [
        "tokio-tungstenite/rustls-native-certs",
        "hyper-rustls/rustls-native-certs",
        "hyper-rustls/ring"
      ],
      "signature-verifier": [
        "dep:sha2",
        "dep:subtle",
        "dep:hmac"
      ]
    }
  }
]
```

> AGENT

Here's the analysis and plan.

## Root Cause

`slack-morphism`'s `rustls-native-certs` feature (enabled by both `axum` and `hyper` features) maps to:

```
tokio-tungstenite/rustls-native-certs  →  only dep:rustls-native-certs (cert resolver)
```

But what's actually needed for `wss://` connections is:

```
tokio-tungstenite/rustls-tls-native-roots  →  __rustls-tls + rustls-native-certs (full TLS stack)
```

The resolved features on `tokio-tungstenite` 0.28.0 confirm it — `rustls`, `tokio-rustls`, and `tungstenite/__rustls-tls` are all missing:

```
Resolved: ["connect", "default", "handshake", "rustls-native-certs", "stream"]
Missing:  ["__rustls-tls", "rustls", "rustls-pki-types", "tokio-rustls"]
```

This is an upstream bug in `slack-morphism` (present in both 2.6 and 2.18).

## Fix

Add `tokio-tungstenite` 0.28 with the correct feature to `crates/slack/Cargo.toml`. Cargo's feature unification will enable the full TLS stack on the same 0.28.0 that `slack-morphism` already pulls in:

```toml
# Workaround: slack-morphism enables tokio-tungstenite/rustls-native-certs
# (cert resolver only) instead of rustls-tls-native-roots (full TLS stack).
# This forces the correct feature on the unified tokio-tungstenite 0.28.
tokio-tungstenite = { version = "0.28", features = ["rustls-tls-native-roots"] }
```

This can't go through `workspace = true` since the workspace dep is 0.26 (used by `providers`, `httpd`, `node-host`). The 0.26 and 0.28 versions are semver-incompatible and resolve separately — this only affects the 0.28 instance used by `slack-morphism`.

We should also file an upstream issue on `slack-morphism` so the feature mapping gets fixed at the source.

Want me to implement this fix?

> DEVELOPER

Is this blocking slack use at all? Is a newer version already available for slack-morphism?

> AGENT

**Yes, this completely blocks Slack socket mode.** Without TLS, the WebSocket client can't connect to `wss://wss-primary.slack.com` at all — there's no fallback.

As for versions — `slack-morphism` 2.20.0 is the latest on crates.io, and we're resolving 2.18.0 (workspace declares `^2.6`). But as I showed, even 2.18.0 has the same broken feature mapping (`tokio-tungstenite/rustls-native-certs` instead of `rustls-tls-native-roots`). Let me quickly check if 2.20.0 fixes it.

> TOOL

tool_use Bash
id: toolu_019FmzLiq2PfBwCsWVucYT9k
```json
{
  "command": "cargo info slack-morphism 2>/dev/null | head -20",
  "description": "Check slack-morphism 2.20.0 details"
}
```

> TOOL

tool_result
id: toolu_019FmzLiq2PfBwCsWVucYT9k
```
slack-morphism #slack #client
Slack Morphism is a modern client library for Slack Web/Events API/Socket Mode and Block Kit
version: 2.18.0 (latest 2.20.0)
license: Apache-2.0
rust-version: unknown
documentation: https://docs.rs/slack_morphism
homepage: https://github.com/abdolence/slack-morphism-rust
repository: https://github.com/abdolence/slack-morphism-rust
crates.io: https://crates.io/crates/slack-morphism/2.18.0
features:
 +default             = []
  axum                = [axum-base, hyper-base, rustls-native-certs]
  axum-base           = [hyper-base, dep:axum, dep:tower]
  hyper               = [hyper-base, rustls-native-certs]
  hyper-base          = [dep:tokio, dep:http-body-util, dep:hyper, dep:hyper-rustls, dep:hyper-util, dep:tokio-stream, dep:tokio-tungstenite, dep:signal-hook, dep:signal-hook-tokio, signature-verifier]
  rustls-native-certs = [tokio-tungstenite/rustls-native-certs, hyper-rustls/rustls-native-certs, hyper-rustls/ring]
  signature-verifier  = [dep:sha2, dep:subtle, dep:hmac]
```

> TOOL

tool_use Bash
id: toolu_015hyiYALG4JRK4JHL1kBfPo
```json
{
  "command": "cargo info slack-morphism --version 2.20.0 2>/dev/null | head -20",
  "description": "Check slack-morphism 2.20.0 features"
}
```

> TOOL

tool_result
id: toolu_015hyiYALG4JRK4JHL1kBfPo
```
(Bash completed with no output)
```

> TOOL

tool_use ToolSearch
id: toolu_01UbW9tt8jJrm3b4w9gRQVKi
```json
{
  "query": "select:WebFetch",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_01UbW9tt8jJrm3b4w9gRQVKi
```
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
```

> TOOL

tool_use WebFetch
id: toolu_011CKzgM5i13M6SEUUx1fmEy
```json
{
  "url": "https://crates.io/api/v1/crates/slack-morphism/2.20.0",
  "prompt": "Show me the features map for this crate version, specifically the rustls-native-certs feature and anything related to tokio-tungstenite"
}
```

> TOOL

tool_result
id: toolu_011CKzgM5i13M6SEUUx1fmEy
```
# Rustls-Native-Certs Feature Analysis

The **rustls-native-certs** feature includes the following dependencies:

`"tokio-tungstenite/rustls-native-certs","tokio-tungstenite/rustls-tls-native-roots","hyper-rustls/rustls-native-certs","hyper-rustls/ring"`

## Tokio-Tungstenite Related Features

The crate enables WebSocket support through tokio-tungstenite, which appears in two contexts:

1. **hyper-base feature** — includes `"dep:tokio-tungstenite"` as a direct dependency
2. **rustls-native-certs feature** — activates TLS features for tokio-tungstenite, specifically native certificate support and native root certificates

This structure allows users to configure secure WebSocket connections with native certificate validation when needed.
```

> AGENT

This confirms it — **version 2.20.0 fixes the bug.** The `rustls-native-certs` feature in 2.20.0 adds the missing `tokio-tungstenite/rustls-tls-native-roots`:

| Version | `rustls-native-certs` feature enables |
|---------|--------------------------------------|
| 2.18.0 | `tokio-tungstenite/rustls-native-certs` (cert resolver only) |
| 2.20.0 | `tokio-tungstenite/rustls-native-certs` **+ `tokio-tungstenite/rustls-tls-native-roots`** (full TLS) |

So the fix simplifies to just bumping the version constraint in the workspace `Cargo.toml`:

```toml
slack-morphism = { features = ["axum", "hyper"], version = "2.20" }
```

No workaround dependency needed. We should check for any breaking API changes between 2.18 and 2.20 in `crates/slack/`, but given it's the same major version it's likely compatible.

Want me to implement this?

> DEVELOPER

proceed

> TOOL

tool_use Bash
id: toolu_01WzKCBL4KvBdoGwPjcXWsbp
```json
{
  "command": "bd create --title=\"Fix Slack socket mode TLS failure (GH #543)\" --description=\"slack-morphism 2.18 maps rustls-native-certs to tokio-tungstenite/rustls-native-certs (cert resolver only), missing the actual TLS stack. Version 2.20 adds tokio-tungstenite/rustls-tls-native-roots. Bump workspace dep to fix.\" --type=bug --priority=1 --json",
  "description": "Create beads issue for Slack TLS fix"
}
```

> TOOL

tool_result
id: toolu_01WzKCBL4KvBdoGwPjcXWsbp
```
{
  "id": "moltis-0a8",
  "title": "Fix Slack socket mode TLS failure (GH #543)",
  "description": "slack-morphism 2.18 maps rustls-native-certs to tokio-tungstenite/rustls-native-certs (cert resolver only), missing the actual TLS stack. Version 2.20 adds tokio-tungstenite/rustls-tls-native-roots. Bump workspace dep to fix.",
  "status": "open",
  "priority": 1,
  "issue_type": "bug",
  "owner": "gpg@pen.so",
  "created_at": "2026-04-14T10:40:54.161544Z",
  "created_by": "Fabien Penso",
  "updated_at": "2026-04-14T10:40:54.161544Z"
}
```

> TOOL

tool_use Read
id: toolu_017yHuHwcTEHjkmDCaDLW2EA
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack/src/lib.rs"
}
```

> TOOL

tool_result
id: toolu_017yHuHwcTEHjkmDCaDLW2EA
```
     1→//! Slack channel plugin for moltis.
     2→//!
     3→//! Connects to Slack via Socket Mode using the `slack-morphism` crate.
     4→//! Handles inbound DMs and channel messages, applies access control
     5→//! policies, and dispatches messages to the chat session.
     6→
     7→pub mod channel_webhook_verifier;
     8→pub mod commands;
     9→pub mod config;
    10→pub mod markdown;
    11→pub mod outbound;
    12→pub mod plugin;
    13→pub mod socket;
    14→pub mod state;
    15→pub mod webhook;
    16→
    17→pub use {config::SlackAccountConfig, plugin::SlackPlugin};
    18→
```

> TOOL

tool_use Bash
id: toolu_01Dde4MrBMMSHv1AGUHzT25V
```json
{
  "command": "bd update moltis-0a8 --status=in_progress --json",
  "description": "Claim the issue"
}
```

> TOOL

tool_result
id: toolu_01Dde4MrBMMSHv1AGUHzT25V
```
[
  {
    "id": "moltis-0a8",
    "title": "Fix Slack socket mode TLS failure (GH #543)",
    "description": "slack-morphism 2.18 maps rustls-native-certs to tokio-tungstenite/rustls-native-certs (cert resolver only), missing the actual TLS stack. Version 2.20 adds tokio-tungstenite/rustls-tls-native-roots. Bump workspace dep to fix.",
    "status": "in_progress",
    "priority": 1,
    "issue_type": "bug",
    "owner": "gpg@pen.so",
    "created_at": "2026-04-14T10:40:54Z",
    "created_by": "Fabien Penso",
    "updated_at": "2026-04-14T10:40:57Z"
  }
]
```

> AGENT

Now let me check for any API usage that might break with the version bump, then apply the fix.

> TOOL

tool_use Grep
id: toolu_01RdmduDLhRLmNPrixtoaoe3
```json
{
  "pattern": "use slack_morphism",
  "path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01RdmduDLhRLmNPrixtoaoe3
```
No matches found
```

> TOOL

tool_use Grep
id: toolu_01WXGxi1X7mvcdtmiECB9aD9
```json
{
  "pattern": "slack_morphism::",
  "path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01WXGxi1X7mvcdtmiECB9aD9
```
Found 3 files
crates/slack/src/webhook.rs
crates/slack/src/socket.rs
crates/slack/src/outbound.rs
```

> TOOL

tool_use Read
id: toolu_01DVjQ8YBY6KGzSbGiZ95V4r
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack/src/socket.rs"
}
```

> TOOL

tool_result
id: toolu_01DVjQ8YBY6KGzSbGiZ95V4r
```
     1→use std::sync::Arc;
     2→
     3→use {
     4→    secrecy::ExposeSecret,
     5→    slack_morphism::prelude::*,
     6→    tracing::{debug, info, warn},
     7→};
     8→
     9→use moltis_channels::{
    10→    config_view::ChannelConfigView,
    11→    gating::{DmPolicy, GroupPolicy, is_allowed},
    12→    message_log::MessageLogEntry,
    13→    plugin::{
    14→        ChannelEvent, ChannelMessageKind, ChannelMessageMeta, ChannelReplyTarget, ChannelType,
    15→    },
    16→};
    17→
    18→use crate::{
    19→    config::SlackAccountConfig,
    20→    markdown::strip_mentions,
    21→    state::{AccountState, AccountStateMap},
    22→};
    23→
    24→/// State stored in the Socket Mode listener for callback access.
    25→#[derive(Clone)]
    26→struct ListenerState {
    27→    account_id: String,
    28→    accounts: AccountStateMap,
    29→}
    30→
    31→/// Start Socket Mode for a single account.
    32→///
    33→/// Creates a `SlackClient`, calls `auth.test` to verify the bot token and
    34→/// obtain the bot user ID, stores state, then spawns the socket listener.
    35→pub async fn start_socket_mode(
    36→    account_id: &str,
    37→    config: SlackAccountConfig,
    38→    accounts: AccountStateMap,
    39→    message_log: Option<Arc<dyn moltis_channels::message_log::MessageLog>>,
    40→    event_sink: Option<Arc<dyn moltis_channels::ChannelEventSink>>,
    41→) -> moltis_channels::Result<()> {
    42→    let bot_token_str = config.bot_token.expose_secret().clone();
    43→    let app_token_str = config.app_token.expose_secret().clone();
    44→
    45→    if bot_token_str.is_empty() {
    46→        return Err(moltis_channels::Error::invalid_input(
    47→            "Slack bot_token is required",
    48→        ));
    49→    }
    50→    if app_token_str.is_empty() {
    51→        return Err(moltis_channels::Error::invalid_input(
    52→            "Slack app_token is required for Socket Mode",
    53→        ));
    54→    }
    55→
    56→    let client = Arc::new(SlackClient::new(SlackClientHyperConnector::new().map_err(
    57→        |e| moltis_channels::Error::unavailable(format!("hyper connector: {e}")),
    58→    )?));
    59→
    60→    // Verify the bot token and get the bot user ID.
    61→    let bot_token = SlackApiToken::new(SlackApiTokenValue::from(bot_token_str));
    62→    let session = client.open_session(&bot_token);
    63→    let auth_response = session
    64→        .auth_test()
    65→        .await
    66→        .map_err(|e| moltis_channels::Error::unavailable(format!("auth.test failed: {e}")))?;
    67→
    68→    let bot_user_id = auth_response.user_id.to_string();
    69→    info!(account_id, bot_user_id, "slack bot authenticated");
    70→
    71→    let cancel = tokio_util::sync::CancellationToken::new();
    72→
    73→    {
    74→        let mut accts = accounts.write().unwrap_or_else(|e| e.into_inner());
    75→        accts.insert(account_id.to_string(), AccountState {
    76→            account_id: account_id.to_string(),
    77→            config,
    78→            message_log,
    79→            event_sink,
    80→            cancel: cancel.clone(),
    81→            bot_user_id: Some(bot_user_id),
    82→            pending_threads: std::collections::HashMap::new(),
    83→        });
    84→    }
    85→
    86→    // Spawn the socket listener.
    87→    let accounts_for_task = Arc::clone(&accounts);
    88→    let account_id_owned = account_id.to_string();
    89→    let cancel_for_task = cancel.clone();
    90→    let app_token = SlackApiToken::new(SlackApiTokenValue::from(app_token_str));
    91→
    92→    tokio::spawn(async move {
    93→        if let Err(e) = run_socket_listener(
    94→            &account_id_owned,
    95→            client,
    96→            app_token,
    97→            accounts_for_task,
    98→            cancel_for_task,
    99→        )
   100→        .await
   101→        {
   102→            warn!(
   103→                account_id = %account_id_owned,
   104→                "slack socket mode listener stopped: {e}"
   105→            );
   106→        }
   107→    });
   108→
   109→    Ok(())
   110→}
   111→
   112→/// Run the Socket Mode listener until cancelled.
   113→async fn run_socket_listener(
   114→    account_id: &str,
   115→    client: Arc<SlackClient<SlackClientHyperHttpsConnector>>,
   116→    app_token: SlackApiToken,
   117→    accounts: AccountStateMap,
   118→    cancel: tokio_util::sync::CancellationToken,
   119→) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
   120→    let listener_state = ListenerState {
   121→        account_id: account_id.to_string(),
   122→        accounts,
   123→    };
   124→
   125→    // Socket Mode callbacks — must be function pointers, so we use user state.
   126→    let callbacks = SlackSocketModeListenerCallbacks::new()
   127→        .with_push_events(push_events_callback)
   128→        .with_command_events(command_events_callback)
   129→        .with_interaction_events(interaction_events_callback);
   130→
   131→    let listener_environment = Arc::new(
   132→        SlackClientEventsListenerEnvironment::new(Arc::clone(&client))
   133→            .with_error_handler(error_handler)
   134→            .with_user_state(listener_state),
   135→    );
   136→
   137→    let config = SlackClientSocketModeConfig::new();
   138→    let socket_listener =
   139→        SlackClientSocketModeListener::new(&config, listener_environment, callbacks);
   140→
   141→    socket_listener.listen_for(&app_token).await?;
   142→
   143→    info!(account_id, "slack socket mode listener started");
   144→
   145→    tokio::select! {
   146→        () = cancel.cancelled() => {
   147→            info!(account_id, "slack socket mode shutting down");
   148→            socket_listener.shutdown().await;
   149→        }
   150→        _code = socket_listener.serve() => {
   151→            warn!(account_id, "slack socket mode listener unexpectedly stopped");
   152→        }
   153→    }
   154→
   155→    Ok(())
   156→}
   157→
   158→/// Error handler for Socket Mode.
   159→fn error_handler(
   160→    err: Box<dyn std::error::Error + Send + Sync>,
   161→    _client: Arc<SlackClient<SlackClientHyperHttpsConnector>>,
   162→    _states: SlackClientEventsUserState,
   163→) -> HttpStatusCode {
   164→    warn!("slack socket mode error: {err}");
   165→    HttpStatusCode::OK
   166→}
   167→
   168→/// Push events callback (messages, app_mention, etc.).
   169→async fn push_events_callback(
   170→    event: SlackPushEventCallback,
   171→    _client: Arc<SlackClient<SlackClientHyperHttpsConnector>>,
   172→    states: SlackClientEventsUserState,
   173→) -> UserCallbackResult<()> {
   174→    let guard = states.read().await;
   175→    let listener_state = match guard.get_user_state::<ListenerState>() {
   176→        Some(s) => s.clone(),
   177→        None => return Ok(()),
   178→    };
   179→    drop(guard);
   180→
   181→    match event.event {
   182→        SlackEventCallbackBody::Message(msg_event) => {
   183→            handle_message_event(
   184→                &listener_state.account_id,
   185→                msg_event,
   186→                &listener_state.accounts,
   187→            )
   188→            .await;
   189→        },
   190→        SlackEventCallbackBody::AppMention(mention_event) => {
   191→            let channel = mention_event.channel.to_string();
   192→            let user = mention_event.user.to_string();
   193→            let text = mention_event.content.text.as_deref().unwrap_or("");
   194→            let thread_ts = mention_event
   195→                .origin
   196→                .thread_ts
   197→                .as_ref()
   198→                .map(|ts| ts.to_string());
   199→
   200→            handle_inbound(
   201→                &listener_state.account_id,
   202→                &channel,
   203→                &user,
   204→                text,
   205→                thread_ts,
   206→                None,
   207→                true, // is_mention
   208→                &listener_state.accounts,
   209→            )
   210→            .await;
   211→        },
   212→        SlackEventCallbackBody::ReactionAdded(reaction_event) => {
   213→            handle_reaction_event(
   214→                &listener_state.account_id,
   215→                reaction_event.user.as_ref(),
   216→                reaction_event.reaction.as_ref(),
   217→                &reaction_event.item,
   218→                true,
   219→                &listener_state.accounts,
   220→            )
   221→            .await;
   222→        },
   223→        SlackEventCallbackBody::ReactionRemoved(reaction_event) => {
   224→            handle_reaction_event(
   225→                &listener_state.account_id,
   226→                reaction_event.user.as_ref(),
   227→                reaction_event.reaction.as_ref(),
   228→                &reaction_event.item,
   229→                false,
   230→                &listener_state.accounts,
   231→            )
   232→            .await;
   233→        },
   234→        _ => {
   235→            debug!("unhandled slack push event");
   236→        },
   237→    }
   238→
   239→    Ok(())
   240→}
   241→
   242→/// Command events callback (slash commands).
   243→async fn command_events_callback(
   244→    event: SlackCommandEvent,
   245→    _client: Arc<SlackClient<SlackClientHyperHttpsConnector>>,
   246→    states: SlackClientEventsUserState,
   247→) -> UserCallbackResult<SlackCommandEventResponse> {
   248→    let guard = states.read().await;
   249→    let listener_state = match guard.get_user_state::<ListenerState>() {
   250→        Some(s) => s.clone(),
   251→        None => {
   252→            return Ok(SlackCommandEventResponse::new(
   253→                SlackMessageContent::new().with_text("Not configured".to_string()),
   254→            ));
   255→        },
   256→    };
   257→    drop(guard);
   258→
   259→    let account_id = &listener_state.account_id;
   260→    let command_text = event.command.to_string();
   261→    let text = event.text.unwrap_or_default();
   262→    let full_command = format!("{command_text} {text}").trim().to_string();
   263→    let sender_id = event.user_id.to_string();
   264→
   265→    let event_sink = {
   266→        let accts = listener_state
   267→            .accounts
   268→            .read()
   269→            .unwrap_or_else(|e| e.into_inner());
   270→        accts.get(account_id).and_then(|s| s.event_sink.clone())
   271→    };
   272→
   273→    if let Some(sink) = event_sink {
   274→        let reply_to = ChannelReplyTarget {
   275→            channel_type: ChannelType::Slack,
   276→            account_id: account_id.to_string(),
   277→            chat_id: event.channel_id.to_string(),
   278→            message_id: None,
   279→            thread_id: None,
   280→        };
   281→        match sink
   282→            .dispatch_command(&full_command, reply_to, Some(&sender_id))
   283→            .await
   284→        {
   285→            Ok(response_text) => Ok(SlackCommandEventResponse::new(
   286→                SlackMessageContent::new().with_text(response_text),
   287→            )),
   288→            Err(e) => Ok(SlackCommandEventResponse::new(
   289→                SlackMessageContent::new().with_text(format!("Error: {e}")),
   290→            )),
   291→        }
   292→    } else {
   293→        Ok(SlackCommandEventResponse::new(
   294→            SlackMessageContent::new().with_text("Channel not configured".to_string()),
   295→        ))
   296→    }
   297→}
   298→
   299→/// Interaction events callback (block actions / button clicks).
   300→async fn interaction_events_callback(
   301→    event: SlackInteractionEvent,
   302→    _client: Arc<SlackClient<SlackClientHyperHttpsConnector>>,
   303→    states: SlackClientEventsUserState,
   304→) -> UserCallbackResult<()> {
   305→    let guard = states.read().await;
   306→    let listener_state = match guard.get_user_state::<ListenerState>() {
   307→        Some(s) => s.clone(),
   308→        None => return Ok(()),
   309→    };
   310→    drop(guard);
   311→
   312→    // Extract the action_id from block_actions interaction type.
   313→    let (action_id, channel_id) = match &event {
   314→        SlackInteractionEvent::BlockActions(ba) => {
   315→            let action = ba.actions.as_ref().and_then(|a| a.first());
   316→            let channel = ba.channel.as_ref().map(|c| c.id.to_string());
   317→            match (action, channel) {
   318→                (Some(act), Some(ch)) => (act.action_id.to_string(), ch),
   319→                _ => {
   320→                    debug!("block_actions missing action or channel");
   321→                    return Ok(());
   322→                },
   323→            }
   324→        },
   325→        _ => {
   326→            debug!("unhandled interaction event type");
   327→            return Ok(());
   328→        },
   329→    };
   330→
   331→    let account_id = &listener_state.account_id;
   332→    let event_sink = {
   333→        let accts = listener_state
   334→            .accounts
   335→            .read()
   336→            .unwrap_or_else(|e| e.into_inner());
   337→        accts.get(account_id).and_then(|s| s.event_sink.clone())
   338→    };
   339→
   340→    if let Some(sink) = event_sink {
   341→        let reply_to = ChannelReplyTarget {
   342→            channel_type: ChannelType::Slack,
   343→            account_id: account_id.to_string(),
   344→            chat_id: channel_id,
   345→            message_id: None,
   346→            thread_id: None,
   347→        };
   348→        match sink.dispatch_interaction(&action_id, reply_to).await {
   349→            Ok(_response) => {
   350→                // Response already sent by the gateway.
   351→            },
   352→            Err(e) => {
   353→                debug!(account_id, action_id, "interaction dispatch failed: {e}");
   354→            },
   355→        }
   356→    }
   357→
   358→    Ok(())
   359→}
   360→
   361→/// Handle a Slack message event.
   362→pub(crate) async fn handle_message_event(
   363→    account_id: &str,
   364→    event: SlackMessageEvent,
   365→    accounts: &AccountStateMap,
   366→) {
   367→    // Skip message subtypes (edits, deletes, bot messages, etc.).
   368→    if event.subtype.is_some() {
   369→        return;
   370→    }
   371→
   372→    let user_id = match &event.sender.user {
   373→        Some(u) => u.to_string(),
   374→        None => return, // No user — skip (bot message or system).
   375→    };
   376→
   377→    // Skip messages from our own bot.
   378→    {
   379→        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   380→        if let Some(state) = accts.get(account_id)
   381→            && state
   382→                .bot_user_id
   383→                .as_ref()
   384→                .is_some_and(|bid| bid == &user_id)
   385→        {
   386→            return;
   387→        }
   388→    }
   389→
   390→    let channel_id = match &event.origin.channel {
   391→        Some(c) => c.to_string(),
   392→        None => return,
   393→    };
   394→
   395→    let text = event
   396→        .content
   397→        .as_ref()
   398→        .and_then(|c| c.text.as_deref())
   399→        .unwrap_or("");
   400→
   401→    let thread_ts = event.origin.thread_ts.as_ref().map(|ts| ts.to_string());
   402→    // Use thread_ts if available, otherwise use the message ts for threading.
   403→    let reply_thread = thread_ts.or_else(|| Some(event.origin.ts.to_string()));
   404→
   405→    // Detect if this is a mention.
   406→    let bot_user_id = {
   407→        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   408→        accts.get(account_id).and_then(|s| s.bot_user_id.clone())
   409→    };
   410→    let is_mention = bot_user_id
   411→        .as_ref()
   412→        .is_some_and(|bid| text.contains(&format!("<@{bid}>")));
   413→
   414→    handle_inbound(
   415→        account_id,
   416→        &channel_id,
   417→        &user_id,
   418→        text,
   419→        reply_thread,
   420→        event.sender.username.clone(),
   421→        is_mention,
   422→        accounts,
   423→    )
   424→    .await;
   425→}
   426→
   427→/// Core inbound message processing.
   428→///
   429→/// Shared by message events, app_mention events, and webhook events.
   430→#[allow(clippy::too_many_arguments)]
   431→pub(crate) async fn handle_inbound(
   432→    account_id: &str,
   433→    channel_id: &str,
   434→    user_id: &str,
   435→    text: &str,
   436→    thread_ts: Option<String>,
   437→    username: Option<String>,
   438→    is_mention: bool,
   439→    accounts: &AccountStateMap,
   440→) {
   441→    let (config, message_log, event_sink, bot_user_id) = {
   442→        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   443→        match accts.get(account_id) {
   444→            Some(state) => (
   445→                state.config.clone(),
   446→                state.message_log.clone(),
   447→                state.event_sink.clone(),
   448→                state.bot_user_id.clone(),
   449→            ),
   450→            None => return,
   451→        }
   452→    };
   453→
   454→    // Determine if this is a DM or channel message.
   455→    // Slack DM channel IDs start with 'D'.
   456→    let is_dm = channel_id.starts_with('D');
   457→
   458→    // Access control check.
   459→    let access_granted = check_access(
   460→        is_dm,
   461→        user_id,
   462→        channel_id,
   463→        &config.dm_policy,
   464→        &config.group_policy,
   465→        &config.allowlist,
   466→        &config.channel_allowlist,
   467→    );
   468→
   469→    // Log to message_log (always, even if denied).
   470→    if let Some(log) = &message_log {
   471→        let chat_type = if is_dm {
   472→            "dm"
   473→        } else {
   474→            "channel"
   475→        };
   476→        let entry = MessageLogEntry {
   477→            id: 0,
   478→            account_id: account_id.to_string(),
   479→            channel_type: "slack".to_string(),
   480→            peer_id: user_id.to_string(),
   481→            username: username.clone(),
   482→            sender_name: None,
   483→            chat_id: channel_id.to_string(),
   484→            chat_type: chat_type.to_string(),
   485→            body: text.to_string(),
   486→            access_granted,
   487→            created_at: std::time::SystemTime::now()
   488→                .duration_since(std::time::UNIX_EPOCH)
   489→                .unwrap_or_default()
   490→                .as_secs() as i64,
   491→        };
   492→        if let Err(e) = log.log(entry).await {
   493→            warn!(account_id, "failed to log slack message: {e}");
   494→        }
   495→    }
   496→
   497→    // Emit inbound event (always, even if denied).
   498→    if let Some(sink) = &event_sink {
   499→        sink.emit(ChannelEvent::InboundMessage {
   500→            channel_type: ChannelType::Slack,
   501→            account_id: account_id.to_string(),
   502→            peer_id: user_id.to_string(),
   503→            username: username.clone(),
   504→            sender_name: None,
   505→            message_count: None,
   506→            access_granted,
   507→        })
   508→        .await;
   509→    }
   510→
   511→    if !access_granted {
   512→        debug!(
   513→            account_id,
   514→            user_id, channel_id, "slack message denied by access control"
   515→        );
   516→        return;
   517→    }
   518→
   519→    // Check activation mode for non-DM channels.
   520→    if !is_dm {
   521→        match config.mention_mode {
   522→            moltis_channels::gating::MentionMode::Mention => {
   523→                if !is_mention {
   524→                    return;
   525→                }
   526→            },
   527→            moltis_channels::gating::MentionMode::None => return,
   528→            moltis_channels::gating::MentionMode::Always => {},
   529→        }
   530→    }
   531→
   532→    // Strip bot mention from the text.
   533→    let clean_text = if let Some(bid) = &bot_user_id {
   534→        strip_mentions(text, bid)
   535→    } else {
   536→        text.to_string()
   537→    };
   538→
   539→    let clean_text = clean_text.trim();
   540→    if clean_text.is_empty() {
   541→        return;
   542→    }
   543→
   544→    // Store thread_ts for reply threading.
   545→    if let Some(ts) = &thread_ts {
   546→        let thread_key = format!("{channel_id}:{user_id}");
   547→        let mut accts = accounts.write().unwrap_or_else(|e| e.into_inner());
   548→        if let Some(state) = accts.get_mut(account_id) {
   549→            state.pending_threads.insert(thread_key, ts.clone());
   550→        }
   551→    }
   552→
   553→    // Dispatch to chat.
   554→    if let Some(sink) = &event_sink {
   555→        let reply_to = ChannelReplyTarget {
   556→            channel_type: ChannelType::Slack,
   557→            account_id: account_id.to_string(),
   558→            chat_id: channel_id.to_string(),
   559→            message_id: thread_ts,
   560→            thread_id: None,
   561→        };
   562→
   563→        let meta = ChannelMessageMeta {
   564→            channel_type: ChannelType::Slack,
   565→            sender_name: None,
   566→            username,
   567→            sender_id: Some(user_id.to_string()),
   568→            message_kind: Some(ChannelMessageKind::Text),
   569→            model: config.resolve_model(channel_id, user_id).map(String::from),
   570→            agent_id: config
   571→                .resolve_agent_id(channel_id, user_id)
   572→                .map(String::from),
   573→            audio_filename: None,
   574→            documents: None,
   575→        };
   576→
   577→        #[cfg(feature = "metrics")]
   578→        moltis_metrics::counter!(
   579→            moltis_metrics::channels::MESSAGES_RECEIVED_TOTAL,
   580→            moltis_metrics::labels::CHANNEL => "slack"
   581→        )
   582→        .increment(1);
   583→
   584→        sink.dispatch_to_chat(clean_text, reply_to, meta).await;
   585→    }
   586→}
   587→
   588→/// Handle a reaction_added or reaction_removed event.
   589→pub(crate) async fn handle_reaction_event(
   590→    account_id: &str,
   591→    user_id: &str,
   592→    emoji: &str,
   593→    item: &SlackReactionsItem,
   594→    added: bool,
   595→    accounts: &AccountStateMap,
   596→) {
   597→    // Only handle reactions on messages (not files).
   598→    let (channel_id, message_ts) = match item {
   599→        SlackReactionsItem::Message(msg) => {
   600→            let channel = msg.origin.channel.as_ref().map(|c| c.to_string());
   601→            let ts = msg.origin.ts.to_string();
   602→            match channel {
   603→                Some(c) => (c, ts),
   604→                None => return,
   605→            }
   606→        },
   607→        _ => return,
   608→    };
   609→
   610→    let event_sink = {
   611→        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   612→        accts.get(account_id).and_then(|s| s.event_sink.clone())
   613→    };
   614→
   615→    if let Some(sink) = event_sink {
   616→        sink.emit(ChannelEvent::ReactionChange {
   617→            channel_type: ChannelType::Slack,
   618→            account_id: account_id.to_string(),
   619→            chat_id: channel_id,
   620→            message_id: message_ts,
   621→            user_id: user_id.to_string(),
   622→            emoji: emoji.to_string(),
   623→            added,
   624→        })
   625→        .await;
   626→    }
   627→}
   628→
   629→/// Check if a message should be processed based on access policies.
   630→pub(crate) fn check_access(
   631→    is_dm: bool,
   632→    user_id: &str,
   633→    channel_id: &str,
   634→    dm_policy: &DmPolicy,
   635→    group_policy: &GroupPolicy,
   636→    user_allowlist: &[String],
   637→    channel_allowlist: &[String],
   638→) -> bool {
   639→    if is_dm {
   640→        match dm_policy {
   641→            DmPolicy::Open => true,
   642→            DmPolicy::Allowlist => is_allowed(user_id, user_allowlist),
   643→            DmPolicy::Disabled => false,
   644→        }
   645→    } else {
   646→        match group_policy {
   647→            GroupPolicy::Open => true,
   648→            GroupPolicy::Allowlist => is_allowed(channel_id, channel_allowlist),
   649→            GroupPolicy::Disabled => false,
   650→        }
   651→    }
   652→}
   653→
   654→#[cfg(test)]
   655→mod tests {
   656→    use super::*;
   657→
   658→    #[test]
   659→    fn dm_open_allows_anyone() {
   660→        assert!(check_access(
   661→            true,
   662→            "U123",
   663→            "D456",
   664→            &DmPolicy::Open,
   665→            &GroupPolicy::Open,
   666→            &[],
   667→            &[],
   668→        ));
   669→    }
   670→
   671→    #[test]
   672→    fn dm_allowlist_requires_user() {
   673→        assert!(!check_access(
   674→            true,
   675→            "U999",
   676→            "D456",
   677→            &DmPolicy::Allowlist,
   678→            &GroupPolicy::Open,
   679→            &["U123".to_string()],
   680→            &[],
   681→        ));
   682→        assert!(check_access(
   683→            true,
   684→            "U123",
   685→            "D456",
   686→            &DmPolicy::Allowlist,
   687→            &GroupPolicy::Open,
   688→            &["U123".to_string()],
   689→            &[],
   690→        ));
   691→    }
   692→
   693→    #[test]
   694→    fn dm_disabled_denies_all() {
   695→        assert!(!check_access(
   696→            true,
   697→            "U123",
   698→            "D456",
   699→            &DmPolicy::Disabled,
   700→            &GroupPolicy::Open,
   701→            &[],
   702→            &[],
   703→        ));
   704→    }
   705→
   706→    #[test]
   707→    fn channel_open_allows_any() {
   708→        assert!(check_access(
   709→            false,
   710→            "U123",
   711→            "C456",
   712→            &DmPolicy::Allowlist,
   713→            &GroupPolicy::Open,
   714→            &[],
   715→            &[],
   716→        ));
   717→    }
   718→
   719→    #[test]
   720→    fn channel_allowlist_requires_channel() {
   721→        assert!(!check_access(
   722→            false,
   723→            "U123",
   724→            "C999",
   725→            &DmPolicy::Allowlist,
   726→            &GroupPolicy::Allowlist,
   727→            &[],
   728→            &["C456".to_string()],
   729→        ));
   730→        assert!(check_access(
   731→            false,
   732→            "U123",
   733→            "C456",
   734→            &DmPolicy::Allowlist,
   735→            &GroupPolicy::Allowlist,
   736→            &[],
   737→            &["C456".to_string()],
   738→        ));
   739→    }
   740→
   741→    #[test]
   742→    fn channel_disabled_denies_all() {
   743→        assert!(!check_access(
   744→            false,
   745→            "U123",
   746→            "C456",
   747→            &DmPolicy::Allowlist,
   748→            &GroupPolicy::Disabled,
   749→            &[],
   750→            &[],
   751→        ));
   752→    }
   753→}
   754→
```

> TOOL

tool_use Read
id: toolu_01SBD2X799MZHM3qrSHq3Yd6
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack/src/outbound.rs"
}
```

> TOOL

tool_use Read
id: toolu_01NivW7R5F4VRe8HSvJMn5t2
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack/src/webhook.rs"
}
```

> TOOL

tool_result
id: toolu_01SBD2X799MZHM3qrSHq3Yd6
```
     1→use std::time::Duration;
     2→
     3→use {
     4→    async_trait::async_trait,
     5→    base64::Engine,
     6→    secrecy::ExposeSecret,
     7→    slack_morphism::prelude::*,
     8→    tracing::{debug, warn},
     9→};
    10→
    11→use moltis_channels::{
    12→    Error as ChannelError, Result as ChannelResult,
    13→    plugin::{
    14→        ButtonStyle, ChannelOutbound, ChannelStreamOutbound, ChannelThreadContext,
    15→        InteractiveMessage, StreamEvent, StreamReceiver, ThreadMessage,
    16→    },
    17→};
    18→
    19→use moltis_common::types::ReplyPayload;
    20→
    21→use crate::{
    22→    config::StreamMode,
    23→    markdown::{SLACK_MAX_MESSAGE_LEN, chunk_message, markdown_to_slack},
    24→    state::AccountStateMap,
    25→};
    26→
    27→/// Minimum chars before the first message is sent during streaming.
    28→const STREAM_MIN_INITIAL_CHARS: usize = 30;
    29→
    30→/// Slack outbound message sender.
    31→pub struct SlackOutbound {
    32→    pub(crate) accounts: AccountStateMap,
    33→}
    34→
    35→impl SlackOutbound {
    36→    /// Get a Slack client session for the given account.
    37→    fn get_session(
    38→        &self,
    39→        account_id: &str,
    40→    ) -> ChannelResult<(SlackClient<SlackClientHyperHttpsConnector>, SlackApiToken)> {
    41→        let accounts = self.accounts.read().unwrap_or_else(|e| e.into_inner());
    42→        let state = accounts
    43→            .get(account_id)
    44→            .ok_or_else(|| ChannelError::unknown_account(account_id))?;
    45→
    46→        let token_str = state.config.bot_token.expose_secret().clone();
    47→        let token = SlackApiToken::new(SlackApiTokenValue::from(token_str));
    48→
    49→        let client = SlackClient::new(
    50→            SlackClientHyperConnector::new()
    51→                .map_err(|e| ChannelError::unavailable(format!("hyper connector: {e}")))?,
    52→        );
    53→
    54→        Ok((client, token))
    55→    }
    56→
    57→    /// Get the thread_ts for reply threading.
    58→    fn get_thread_ts(&self, account_id: &str, to: &str, reply_to: Option<&str>) -> Option<String> {
    59→        // If we have an explicit reply_to (message_id), use that as thread_ts.
    60→        if let Some(ts) = reply_to {
    61→            return Some(ts.to_string());
    62→        }
    63→
    64→        // Check if thread_replies is enabled and we have a stored thread_ts.
    65→        let accounts = self.accounts.read().unwrap_or_else(|e| e.into_inner());
    66→        let state = accounts.get(account_id)?;
    67→        if !state.config.thread_replies {
    68→            return None;
    69→        }
    70→        // Look up by channel_id (any user).
    71→        state
    72→            .pending_threads
    73→            .iter()
    74→            .find(|(k, _)| k.starts_with(&format!("{to}:")))
    75→            .map(|(_, ts)| ts.clone())
    76→    }
    77→
    78→    /// Get the edit throttle duration for streaming.
    79→    fn get_edit_throttle(&self, account_id: &str) -> Duration {
    80→        let accounts = self.accounts.read().unwrap_or_else(|e| e.into_inner());
    81→        accounts
    82→            .get(account_id)
    83→            .map(|s| Duration::from_millis(s.config.edit_throttle_ms))
    84→            .unwrap_or(Duration::from_millis(500))
    85→    }
    86→
    87→    /// Get the stream mode for the given account.
    88→    fn get_stream_mode(&self, account_id: &str) -> StreamMode {
    89→        let accounts = self.accounts.read().unwrap_or_else(|e| e.into_inner());
    90→        accounts
    91→            .get(account_id)
    92→            .map(|s| s.config.stream_mode.clone())
    93→            .unwrap_or_default()
    94→    }
    95→
    96→    /// Get the raw bot token string for API calls not covered by slack-morphism.
    97→    fn get_bot_token(&self, account_id: &str) -> ChannelResult<String> {
    98→        let accounts = self.accounts.read().unwrap_or_else(|e| e.into_inner());
    99→        let state = accounts
   100→            .get(account_id)
   101→            .ok_or_else(|| ChannelError::unknown_account(account_id))?;
   102→        Ok(state.config.bot_token.expose_secret().clone())
   103→    }
   104→
   105→    /// Native Slack streaming using chat.startStream/appendStream/stopStream.
   106→    async fn send_stream_native(
   107→        &self,
   108→        account_id: &str,
   109→        to: &str,
   110→        thread_ts: Option<&str>,
   111→        stream: &mut StreamReceiver,
   112→    ) -> ChannelResult<()> {
   113→        let bot_token = self.get_bot_token(account_id)?;
   114→        let http = moltis_common::http_client::build_default_http_client();
   115→        let throttle = self.get_edit_throttle(account_id);
   116→
   117→        let stream_id = start_native_stream(&http, &bot_token, to, thread_ts).await?;
   118→
   119→        let mut pending = String::new();
   120→        let mut last_append = tokio::time::Instant::now();
   121→
   122→        loop {
   123→            match stream.recv().await {
   124→                Some(StreamEvent::Delta(chunk)) => {
   125→                    pending.push_str(&chunk);
   126→
   127→                    // Throttle appends to avoid rate limits.
   128→                    if last_append.elapsed() >= throttle {
   129→                        let text = markdown_to_slack(&std::mem::take(&mut pending));
   130→                        if !text.is_empty()
   131→                            && let Err(e) =
   132→                                append_native_stream(&http, &bot_token, &stream_id, &text).await
   133→                        {
   134→                            debug!(account_id, to, "chat.appendStream failed (will retry): {e}");
   135→                            // Put the text back for next attempt.
   136→                            pending = text;
   137→                        }
   138→                        last_append = tokio::time::Instant::now();
   139→                    }
   140→                },
   141→                Some(StreamEvent::Done) => break,
   142→                Some(StreamEvent::Error(e)) => {
   143→                    pending.push_str(&format!("\n\n:warning: {e}"));
   144→                    break;
   145→                },
   146→                None => break,
   147→            }
   148→        }
   149→
   150→        // Flush any remaining text.
   151→        if !pending.is_empty() {
   152→            let text = markdown_to_slack(&pending);
   153→            if let Err(e) = append_native_stream(&http, &bot_token, &stream_id, &text).await {
   154→                warn!(account_id, to, "final chat.appendStream failed: {e}");
   155→            }
   156→        }
   157→
   158→        // Finalize the stream.
   159→        if let Err(e) = stop_native_stream(&http, &bot_token, &stream_id).await {
   160→            warn!(account_id, to, "chat.stopStream failed: {e}");
   161→        }
   162→
   163→        Ok(())
   164→    }
   165→
   166→    /// Edit-in-place streaming: post → throttled edits → final update.
   167→    async fn send_stream_edit_in_place(
   168→        &self,
   169→        account_id: &str,
   170→        to: &str,
   171→        thread_ts: Option<&str>,
   172→        stream: &mut StreamReceiver,
   173→    ) -> ChannelResult<()> {
   174→        let (client, token) = self.get_session(account_id)?;
   175→        let throttle = self.get_edit_throttle(account_id);
   176→
   177→        let mut accumulated = String::new();
   178→        let mut sent_ts: Option<SlackTs> = None;
   179→        let mut last_edit = tokio::time::Instant::now();
   180→
   181→        loop {
   182→            match stream.recv().await {
   183→                Some(StreamEvent::Delta(chunk)) => {
   184→                    accumulated.push_str(&chunk);
   185→
   186→                    match &sent_ts {
   187→                        None => {
   188→                            if accumulated.len() >= STREAM_MIN_INITIAL_CHARS {
   189→                                let slack_text = markdown_to_slack(&accumulated);
   190→                                match post_message(
   191→                                    &client,
   192→                                    &token,
   193→                                    to,
   194→                                    &format!("{slack_text}..."),
   195→                                    thread_ts,
   196→                                )
   197→                                .await
   198→                                {
   199→                                    Ok(ts) => {
   200→                                        sent_ts = Some(ts);
   201→                                        last_edit = tokio::time::Instant::now();
   202→                                    },
   203→                                    Err(e) => {
   204→                                        warn!(
   205→                                            account_id,
   206→                                            to, "failed to send initial stream message: {e}"
   207→                                        );
   208→                                    },
   209→                                }
   210→                            }
   211→                        },
   212→                        Some(ts) => {
   213→                            if last_edit.elapsed() >= throttle {
   214→                                let slack_text = markdown_to_slack(&accumulated);
   215→                                let display = if slack_text.len() > SLACK_MAX_MESSAGE_LEN - 3 {
   216→                                    format!(
   217→                                        "{}...",
   218→                                        &slack_text[..slack_text
   219→                                            .floor_char_boundary(SLACK_MAX_MESSAGE_LEN - 3)]
   220→                                    )
   221→                                } else {
   222→                                    format!("{slack_text}...")
   223→                                };
   224→
   225→                                if let Err(e) =
   226→                                    update_message(&client, &token, to, ts, &display).await
   227→                                {
   228→                                    debug!(
   229→                                        account_id,
   230→                                        to, "stream edit-in-place failed (will retry): {e}"
   231→                                    );
   232→                                }
   233→                                last_edit = tokio::time::Instant::now();
   234→                            }
   235→                        },
   236→                    }
   237→                },
   238→                Some(StreamEvent::Done) => break,
   239→                Some(StreamEvent::Error(e)) => {
   240→                    accumulated.push_str(&format!("\n\n:warning: {e}"));
   241→                    break;
   242→                },
   243→                None => break,
   244→            }
   245→        }
   246→
   247→        if accumulated.is_empty() {
   248→            return Ok(());
   249→        }
   250→
   251→        let final_text = markdown_to_slack(&accumulated);
   252→        let chunks = chunk_message(&final_text, SLACK_MAX_MESSAGE_LEN);
   253→
   254→        match &sent_ts {
   255→            Some(ts) => {
   256→                if let Some(first) = chunks.first()
   257→                    && let Err(e) = update_message(&client, &token, to, ts, first).await
   258→                {
   259→                    warn!(account_id, to, "failed to finalize stream message: {e}");
   260→                }
   261→                for chunk in chunks.iter().skip(1) {
   262→                    if let Err(e) = post_message(&client, &token, to, chunk, thread_ts).await {
   263→                        warn!(account_id, to, "failed to send overflow chunk: {e}");
   264→                    }
   265→                }
   266→            },
   267→            None => {
   268→                for chunk in &chunks {
   269→                    if let Err(e) = post_message(&client, &token, to, chunk, thread_ts).await {
   270→                        warn!(account_id, to, "failed to send stream message: {e}");
   271→                    }
   272→                }
   273→            },
   274→        }
   275→
   276→        Ok(())
   277→    }
   278→}
   279→
   280→/// Post a message to a Slack channel.
   281→async fn post_message(
   282→    client: &SlackClient<SlackClientHyperHttpsConnector>,
   283→    token: &SlackApiToken,
   284→    channel: &str,
   285→    text: &str,
   286→    thread_ts: Option<&str>,
   287→) -> ChannelResult<SlackTs> {
   288→    let session = client.open_session(token);
   289→    let channel_id: SlackChannelId = channel.into();
   290→
   291→    let mut req = SlackApiChatPostMessageRequest::new(
   292→        channel_id,
   293→        SlackMessageContent::new().with_text(text.to_string()),
   294→    );
   295→
   296→    if let Some(ts) = thread_ts {
   297→        req = req.with_thread_ts(ts.into());
   298→    }
   299→
   300→    let resp = session
   301→        .chat_post_message(&req)
   302→        .await
   303→        .map_err(|e| ChannelError::unavailable(format!("chat.postMessage failed: {e}")))?;
   304→
   305→    Ok(resp.ts)
   306→}
   307→
   308→/// Update an existing message.
   309→async fn update_message(
   310→    client: &SlackClient<SlackClientHyperHttpsConnector>,
   311→    token: &SlackApiToken,
   312→    channel: &str,
   313→    ts: &SlackTs,
   314→    text: &str,
   315→) -> ChannelResult<()> {
   316→    let session = client.open_session(token);
   317→    let channel_id: SlackChannelId = channel.into();
   318→
   319→    let req = SlackApiChatUpdateRequest::new(
   320→        channel_id,
   321→        SlackMessageContent::new().with_text(text.to_string()),
   322→        ts.clone(),
   323→    );
   324→
   325→    session
   326→        .chat_update(&req)
   327→        .await
   328→        .map_err(|e| ChannelError::unavailable(format!("chat.update failed: {e}")))?;
   329→
   330→    Ok(())
   331→}
   332→
   333→/// Decode a `data:<mime>;base64,<payload>` URI into raw bytes.
   334→fn decode_data_url(url: &str) -> ChannelResult<(Vec<u8>, String)> {
   335→    let comma = url
   336→        .find(',')
   337→        .ok_or_else(|| ChannelError::invalid_input("malformed data URL: no comma"))?;
   338→    let header = &url[..comma];
   339→    let mime = header
   340→        .strip_prefix("data:")
   341→        .and_then(|s| s.strip_suffix(";base64"))
   342→        .unwrap_or("application/octet-stream");
   343→    let payload = &url[comma + 1..];
   344→    let bytes = base64::engine::general_purpose::STANDARD
   345→        .decode(payload)
   346→        .map_err(|e| ChannelError::invalid_input(format!("base64 decode error: {e}")))?;
   347→    Ok((bytes, mime.to_string()))
   348→}
   349→
   350→/// Map MIME type to a file extension.
   351→fn extension_for_mime(mime: &str) -> &'static str {
   352→    match mime {
   353→        "image/png" => "png",
   354→        "image/jpeg" | "image/jpg" => "jpg",
   355→        "image/gif" => "gif",
   356→        "image/webp" => "webp",
   357→        "audio/ogg" => "ogg",
   358→        "audio/mpeg" | "audio/mp3" => "mp3",
   359→        "video/mp4" => "mp4",
   360→        "application/pdf" => "pdf",
   361→        _ => "bin",
   362→    }
   363→}
   364→
   365→/// Upload a file to Slack using the V2 upload flow.
   366→async fn upload_file(
   367→    client: &SlackClient<SlackClientHyperHttpsConnector>,
   368→    token: &SlackApiToken,
   369→    channel: &str,
   370→    filename: &str,
   371→    content_type: &str,
   372→    data: &[u8],
   373→    caption: Option<&str>,
   374→    thread_ts: Option<&str>,
   375→) -> ChannelResult<()> {
   376→    let session = client.open_session(token);
   377→
   378→    // Step 1: Get the upload URL.
   379→    let upload_req =
   380→        SlackApiFilesGetUploadUrlExternalRequest::new(filename.to_string(), data.len());
   381→    let upload_resp = session
   382→        .get_upload_url_external(&upload_req)
   383→        .await
   384→        .map_err(|e| ChannelError::unavailable(format!("getUploadURLExternal failed: {e}")))?;
   385→
   386→    // Step 2: Upload file bytes.
   387→    let via_req = SlackApiFilesUploadViaUrlRequest::new(
   388→        upload_resp.upload_url,
   389→        data.to_vec(),
   390→        content_type.to_string(),
   391→    );
   392→    session
   393→        .files_upload_via_url(&via_req)
   394→        .await
   395→        .map_err(|e| ChannelError::unavailable(format!("file upload PUT failed: {e}")))?;
   396→
   397→    // Step 3: Complete the upload — attach to channel.
   398→    let file_complete = SlackApiFilesComplete::new(upload_resp.file_id);
   399→    let mut complete_req = SlackApiFilesCompleteUploadExternalRequest::new(vec![file_complete])
   400→        .with_channel_id(channel.into());
   401→    if let Some(comment) = caption {
   402→        complete_req = complete_req.with_initial_comment(comment.to_string());
   403→    }
   404→    if let Some(ts) = thread_ts {
   405→        complete_req = complete_req.with_thread_ts(ts.into());
   406→    }
   407→    session
   408→        .files_complete_upload_external(&complete_req)
   409→        .await
   410→        .map_err(|e| ChannelError::unavailable(format!("completeUploadExternal failed: {e}")))?;
   411→
   412→    Ok(())
   413→}
   414→
   415→/// Add or remove a reaction on a Slack message using the Web API.
   416→async fn modify_reaction(
   417→    client: &SlackClient<SlackClientHyperHttpsConnector>,
   418→    token: &SlackApiToken,
   419→    channel: &str,
   420→    timestamp: &str,
   421→    emoji: &str,
   422→    add: bool,
   423→) -> ChannelResult<()> {
   424→    let session = client.open_session(token);
   425→    let channel_id: SlackChannelId = channel.into();
   426→    let ts: SlackTs = timestamp.into();
   427→    let reaction = SlackReactionName::new(emoji.to_string());
   428→
   429→    if add {
   430→        let req = SlackApiReactionsAddRequest::new(channel_id, reaction, ts);
   431→        session
   432→            .reactions_add(&req)
   433→            .await
   434→            .map_err(|e| ChannelError::unavailable(format!("reactions.add failed: {e}")))?;
   435→    } else {
   436→        let req = SlackApiReactionsRemoveRequest::new(reaction)
   437→            .with_channel(channel_id)
   438→            .with_timestamp(ts);
   439→        session
   440→            .reactions_remove(&req)
   441→            .await
   442→            .map_err(|e| ChannelError::unavailable(format!("reactions.remove failed: {e}")))?;
   443→    }
   444→
   445→    Ok(())
   446→}
   447→
   448→#[async_trait]
   449→impl ChannelOutbound for SlackOutbound {
   450→    async fn send_text(
   451→        &self,
   452→        account_id: &str,
   453→        to: &str,
   454→        text: &str,
   455→        reply_to: Option<&str>,
   456→    ) -> ChannelResult<()> {
   457→        let (client, token) = self.get_session(account_id)?;
   458→        let thread_ts = self.get_thread_ts(account_id, to, reply_to);
   459→        let slack_text = markdown_to_slack(text);
   460→
   461→        let chunks = chunk_message(&slack_text, SLACK_MAX_MESSAGE_LEN);
   462→        for chunk in chunks {
   463→            post_message(&client, &token, to, chunk, thread_ts.as_deref()).await?;
   464→        }
   465→
   466→        #[cfg(feature = "metrics")]
   467→        moltis_metrics::counter!(
   468→            moltis_metrics::channels::MESSAGES_SENT_TOTAL,
   469→            moltis_metrics::labels::CHANNEL => "slack"
   470→        )
   471→        .increment(1);
   472→
   473→        Ok(())
   474→    }
   475→
   476→    async fn send_media(
   477→        &self,
   478→        account_id: &str,
   479→        to: &str,
   480→        payload: &ReplyPayload,
   481→        reply_to: Option<&str>,
   482→    ) -> ChannelResult<()> {
   483→        let media_url = payload.media.as_ref().map(|m| m.url.as_str());
   484→
   485→        match media_url {
   486→            Some(url) if url.starts_with("data:") => {
   487→                let (data, mime) = decode_data_url(url)?;
   488→                let filename = payload
   489→                    .media
   490→                    .as_ref()
   491→                    .and_then(|m| m.filename.clone())
   492→                    .unwrap_or_else(|| {
   493→                        let ext = extension_for_mime(&mime);
   494→                        format!("file.{ext}")
   495→                    });
   496→                let caption = if payload.text.is_empty() {
   497→                    None
   498→                } else {
   499→                    Some(payload.text.as_str())
   500→                };
   501→
   502→                let (client, token) = self.get_session(account_id)?;
   503→                let thread_ts = self.get_thread_ts(account_id, to, reply_to);
   504→
   505→                upload_file(
   506→                    &client,
   507→                    &token,
   508→                    to,
   509→                    &filename,
   510→                    &mime,
   511→                    &data,
   512→                    caption,
   513→                    thread_ts.as_deref(),
   514→                )
   515→                .await
   516→            },
   517→            Some(url) => {
   518→                // Regular URL — append to text and send.
   519→                let text = if payload.text.is_empty() {
   520→                    url.to_string()
   521→                } else {
   522→                    format!("{}\n{url}", payload.text)
   523→                };
   524→                self.send_text(account_id, to, &text, reply_to).await
   525→            },
   526→            None => {
   527→                // No media — send text only.
   528→                let text = if payload.text.is_empty() {
   529→                    "(media attachment)".to_string()
   530→                } else {
   531→                    payload.text.clone()
   532→                };
   533→                self.send_text(account_id, to, &text, reply_to).await
   534→            },
   535→        }
   536→    }
   537→
   538→    async fn send_typing(&self, _account_id: &str, _to: &str) -> ChannelResult<()> {
   539→        // Slack bots cannot show typing indicators.
   540→        Ok(())
   541→    }
   542→
   543→    async fn send_interactive(
   544→        &self,
   545→        account_id: &str,
   546→        to: &str,
   547→        message: &InteractiveMessage,
   548→        reply_to: Option<&str>,
   549→    ) -> ChannelResult<()> {
   550→        let (client, token) = self.get_session(account_id)?;
   551→        let thread_ts = self.get_thread_ts(account_id, to, reply_to);
   552→        let session = client.open_session(&token);
   553→        let channel_id: SlackChannelId = to.into();
   554→
   555→        // Build Block Kit blocks: text section + actions per row.
   556→        let mut blocks = vec![serde_json::json!({
   557→            "type": "section",
   558→            "text": { "type": "mrkdwn", "text": message.text },
   559→        })];
   560→
   561→        for row in &message.button_rows {
   562→            let elements: Vec<serde_json::Value> = row
   563→                .iter()
   564→                .map(|btn| {
   565→                    let mut button = serde_json::json!({
   566→                        "type": "button",
   567→                        "text": { "type": "plain_text", "text": btn.label },
   568→                        "action_id": btn.callback_data,
   569→                    });
   570→                    match btn.style {
   571→                        ButtonStyle::Primary => {
   572→                            button["style"] = serde_json::json!("primary");
   573→                        },
   574→                        ButtonStyle::Danger => {
   575→                            button["style"] = serde_json::json!("danger");
   576→                        },
   577→                        ButtonStyle::Default => {},
   578→                    }
   579→                    button
   580→                })
   581→                .collect();
   582→
   583→            blocks.push(serde_json::json!({
   584→                "type": "actions",
   585→                "elements": elements,
   586→            }));
   587→        }
   588→
   589→        let content = SlackMessageContent::new().with_text(message.text.clone());
   590→
   591→        let mut req = SlackApiChatPostMessageRequest::new(channel_id, content);
   592→
   593→        if let Some(ts) = thread_ts.as_deref() {
   594→            req = req.with_thread_ts(ts.into());
   595→        }
   596→
   597→        // Attach blocks via raw JSON since slack-morphism's typed Block Kit
   598→        // builders don't cover all action element styles easily.
   599→        let mut body = serde_json::to_value(&req)
   600→            .map_err(|e| ChannelError::unavailable(format!("serialize failed: {e}")))?;
   601→        body["blocks"] = serde_json::json!(blocks);
   602→
   603→        // Use the raw post approach.  Fall back to text-only if it fails.
   604→        let raw_resp: serde_json::Value = session
   605→            .http_session_api
   606→            .http_post("chat.postMessage", &body, None)
   607→            .await
   608→            .map_err(|e| {
   609→                ChannelError::unavailable(format!("chat.postMessage (interactive) failed: {e}"))
   610→            })?;
   611→
   612→        if raw_resp.get("ok") == Some(&serde_json::Value::Bool(false)) {
   613→            let err = raw_resp
   614→                .get("error")
   615→                .and_then(|v| v.as_str())
   616→                .unwrap_or("unknown");
   617→            return Err(ChannelError::unavailable(format!(
   618→                "chat.postMessage (interactive) error: {err}"
   619→            )));
   620→        }
   621→
   622→        Ok(())
   623→    }
   624→
   625→    async fn add_reaction(
   626→        &self,
   627→        account_id: &str,
   628→        channel_id: &str,
   629→        message_id: &str,
   630→        emoji: &str,
   631→    ) -> ChannelResult<()> {
   632→        let (client, token) = self.get_session(account_id)?;
   633→        modify_reaction(&client, &token, channel_id, message_id, emoji, true).await
   634→    }
   635→
   636→    async fn remove_reaction(
   637→        &self,
   638→        account_id: &str,
   639→        channel_id: &str,
   640→        message_id: &str,
   641→        emoji: &str,
   642→    ) -> ChannelResult<()> {
   643→        let (client, token) = self.get_session(account_id)?;
   644→        modify_reaction(&client, &token, channel_id, message_id, emoji, false).await
   645→    }
   646→}
   647→
   648→/// Start a native Slack stream via `chat.startStream`.
   649→///
   650→/// Returns `(stream_id, channel)` on success.
   651→async fn start_native_stream(
   652→    http: &reqwest::Client,
   653→    bot_token: &str,
   654→    channel: &str,
   655→    thread_ts: Option<&str>,
   656→) -> ChannelResult<String> {
   657→    let mut body = serde_json::json!({ "channel": channel });
   658→    if let Some(ts) = thread_ts {
   659→        body["thread_ts"] = serde_json::json!(ts);
   660→    }
   661→
   662→    let resp = http
   663→        .post("https://slack.com/api/chat.startStream")
   664→        .bearer_auth(bot_token)
   665→        .json(&body)
   666→        .send()
   667→        .await
   668→        .map_err(|e| ChannelError::external("chat.startStream", e))?;
   669→
   670→    let json: serde_json::Value = resp
   671→        .json()
   672→        .await
   673→        .map_err(|e| ChannelError::external("chat.startStream parse", e))?;
   674→
   675→    if json.get("ok").and_then(|v| v.as_bool()) != Some(true) {
   676→        let err = json
   677→            .get("error")
   678→            .and_then(|v| v.as_str())
   679→            .unwrap_or("unknown");
   680→        return Err(ChannelError::unavailable(format!(
   681→            "chat.startStream failed: {err}"
   682→        )));
   683→    }
   684→
   685→    json.get("stream_id")
   686→        .and_then(|v| v.as_str())
   687→        .map(String::from)
   688→        .ok_or_else(|| ChannelError::unavailable("chat.startStream: missing stream_id"))
   689→}
   690→
   691→/// Append text to a native Slack stream via `chat.appendStream`.
   692→async fn append_native_stream(
   693→    http: &reqwest::Client,
   694→    bot_token: &str,
   695→    stream_id: &str,
   696→    text: &str,
   697→) -> ChannelResult<()> {
   698→    let body = serde_json::json!({
   699→        "stream_id": stream_id,
   700→        "text": text,
   701→    });
   702→
   703→    let resp = http
   704→        .post("https://slack.com/api/chat.appendStream")
   705→        .bearer_auth(bot_token)
   706→        .json(&body)
   707→        .send()
   708→        .await
   709→        .map_err(|e| ChannelError::external("chat.appendStream", e))?;
   710→
   711→    let json: serde_json::Value = resp
   712→        .json()
   713→        .await
   714→        .map_err(|e| ChannelError::external("chat.appendStream parse", e))?;
   715→
   716→    if json.get("ok").and_then(|v| v.as_bool()) != Some(true) {
   717→        let err = json
   718→            .get("error")
   719→            .and_then(|v| v.as_str())
   720→            .unwrap_or("unknown");
   721→        return Err(ChannelError::unavailable(format!(
   722→            "chat.appendStream failed: {err}"
   723→        )));
   724→    }
   725→
   726→    Ok(())
   727→}
   728→
   729→/// Finalize a native Slack stream via `chat.stopStream`.
   730→async fn stop_native_stream(
   731→    http: &reqwest::Client,
   732→    bot_token: &str,
   733→    stream_id: &str,
   734→) -> ChannelResult<()> {
   735→    let body = serde_json::json!({ "stream_id": stream_id });
   736→
   737→    let resp = http
   738→        .post("https://slack.com/api/chat.stopStream")
   739→        .bearer_auth(bot_token)
   740→        .json(&body)
   741→        .send()
   742→        .await
   743→        .map_err(|e| ChannelError::external("chat.stopStream", e))?;
   744→
   745→    let json: serde_json::Value = resp
   746→        .json()
   747→        .await
   748→        .map_err(|e| ChannelError::external("chat.stopStream parse", e))?;
   749→
   750→    if json.get("ok").and_then(|v| v.as_bool()) != Some(true) {
   751→        let err = json
   752→            .get("error")
   753→            .and_then(|v| v.as_str())
   754→            .unwrap_or("unknown");
   755→        return Err(ChannelError::unavailable(format!(
   756→            "chat.stopStream failed: {err}"
   757→        )));
   758→    }
   759→
   760→    Ok(())
   761→}
   762→
   763→#[async_trait]
   764→impl ChannelStreamOutbound for SlackOutbound {
   765→    async fn send_stream(
   766→        &self,
   767→        account_id: &str,
   768→        to: &str,
   769→        reply_to: Option<&str>,
   770→        mut stream: StreamReceiver,
   771→    ) -> ChannelResult<()> {
   772→        let stream_mode = self.get_stream_mode(account_id);
   773→        let thread_ts = self.get_thread_ts(account_id, to, reply_to);
   774→
   775→        match stream_mode {
   776→            StreamMode::Native => {
   777→                self.send_stream_native(account_id, to, thread_ts.as_deref(), &mut stream)
   778→                    .await
   779→            },
   780→            StreamMode::EditInPlace => {
   781→                self.send_stream_edit_in_place(account_id, to, thread_ts.as_deref(), &mut stream)
   782→                    .await
   783→            },
   784→            StreamMode::Off => {
   785→                // Streaming disabled — accumulate and send once.
   786→                let mut accumulated = String::new();
   787→                loop {
   788→                    match stream.recv().await {
   789→                        Some(StreamEvent::Delta(chunk)) => accumulated.push_str(&chunk),
   790→                        Some(StreamEvent::Error(e)) => {
   791→                            accumulated.push_str(&format!("\n\n:warning: {e}"));
   792→                            break;
   793→                        },
   794→                        Some(StreamEvent::Done) | None => break,
   795→                    }
   796→                }
   797→                if !accumulated.is_empty() {
   798→                    let (client, token) = self.get_session(account_id)?;
   799→                    let final_text = markdown_to_slack(&accumulated);
   800→                    for chunk in chunk_message(&final_text, SLACK_MAX_MESSAGE_LEN) {
   801→                        if let Err(e) =
   802→                            post_message(&client, &token, to, chunk, thread_ts.as_deref()).await
   803→                        {
   804→                            warn!(account_id, to, "failed to send stream message: {e}");
   805→                        }
   806→                    }
   807→                }
   808→                Ok(())
   809→            },
   810→        }
   811→    }
   812→
   813→    async fn is_stream_enabled(&self, account_id: &str) -> bool {
   814→        self.get_stream_mode(account_id) != StreamMode::Off
   815→    }
   816→}
   817→
   818→#[async_trait]
   819→impl ChannelThreadContext for SlackOutbound {
   820→    async fn fetch_thread_messages(
   821→        &self,
   822→        account_id: &str,
   823→        channel_id: &str,
   824→        thread_id: &str,
   825→        limit: usize,
   826→    ) -> ChannelResult<Vec<ThreadMessage>> {
   827→        let (client, token) = self.get_session(account_id)?;
   828→        let session = client.open_session(&token);
   829→
   830→        let req = SlackApiConversationsRepliesRequest::new(channel_id.into(), thread_id.into())
   831→            .with_limit(limit.min(200) as u16);
   832→
   833→        let resp = session
   834→            .conversations_replies(&req)
   835→            .await
   836→            .map_err(|e| ChannelError::unavailable(format!("conversations.replies failed: {e}")))?;
   837→
   838→        let messages = resp
   839→            .messages
   840→            .into_iter()
   841→            .map(|msg| {
   842→                let sender_id = msg
   843→                    .sender
   844→                    .user
   845→                    .as_ref()
   846→                    .map(|u| u.to_string())
   847→                    .unwrap_or_default();
   848→                let is_bot = msg.sender.bot_id.is_some() || msg.sender.display_as_bot == Some(true);
   849→                let text = msg.content.text.unwrap_or_default();
   850→                let timestamp = msg.origin.ts.to_string();
   851→
   852→                ThreadMessage {
   853→                    sender_id,
   854→                    is_bot,
   855→                    text,
   856→                    timestamp,
   857→                }
   858→            })
   859→            .collect();
   860→
   861→        Ok(messages)
   862→    }
   863→}
   864→
   865→#[cfg(test)]
   866→#[allow(clippy::unwrap_used)]
   867→mod tests {
   868→    use super::*;
   869→
   870→    #[test]
   871→    fn get_thread_ts_from_reply_to() {
   872→        let accounts =
   873→            std::sync::Arc::new(std::sync::RwLock::new(std::collections::HashMap::new()));
   874→        let outbound = SlackOutbound {
   875→            accounts: accounts.clone(),
   876→        };
   877→        // reply_to takes precedence.
   878→        let ts = outbound.get_thread_ts("acct", "C123", Some("1234567.890"));
   879→        assert_eq!(ts, Some("1234567.890".to_string()));
   880→    }
   881→
   882→    #[test]
   883→    fn get_thread_ts_no_account() {
   884→        let accounts =
   885→            std::sync::Arc::new(std::sync::RwLock::new(std::collections::HashMap::new()));
   886→        let outbound = SlackOutbound { accounts };
   887→        let ts = outbound.get_thread_ts("acct", "C123", None);
   888→        assert!(ts.is_none());
   889→    }
   890→
   891→    #[test]
   892→    fn decode_data_url_png() {
   893→        // Minimal 1x1 red PNG encoded as base64 data URL.
   894→        let b64 = base64::engine::general_purpose::STANDARD.encode(b"fakepng");
   895→        let url = format!("data:image/png;base64,{b64}");
   896→        let (bytes, mime) = decode_data_url(&url).unwrap();
   897→        assert_eq!(bytes, b"fakepng");
   898→        assert_eq!(mime, "image/png");
   899→    }
   900→
   901→    #[test]
   902→    fn decode_data_url_no_comma_fails() {
   903→        assert!(decode_data_url("data:image/pngbase64abc").is_err());
   904→    }
   905→
   906→    #[test]
   907→    fn extension_for_known_mimes() {
   908→        assert_eq!(extension_for_mime("image/png"), "png");
   909→        assert_eq!(extension_for_mime("image/jpeg"), "jpg");
   910→        assert_eq!(extension_for_mime("application/pdf"), "pdf");
   911→        assert_eq!(extension_for_mime("text/plain"), "bin");
   912→    }
   913→}
   914→
```

> TOOL

tool_result
id: toolu_01NivW7R5F4VRe8HSvJMn5t2
```
     1→//! Slack Events API webhook handler.
     2→//!
     3→//! Receives HTTP POST requests from Slack's Events API, verifies request
     4→//! signatures using HMAC-SHA256, and dispatches events to the same handlers
     5→//! used by Socket Mode.
     6→
     7→use std::sync::Arc;
     8→
     9→use {
    10→    hmac::{Hmac, Mac},
    11→    secrecy::ExposeSecret,
    12→    sha2::Sha256,
    13→    slack_morphism::prelude::*,
    14→    tracing::{debug, info},
    15→};
    16→
    17→use moltis_channels::{
    18→    ChannelEventSink,
    19→    message_log::MessageLog,
    20→    plugin::{ChannelReplyTarget, ChannelType},
    21→};
    22→
    23→use crate::{
    24→    config::SlackAccountConfig,
    25→    state::{AccountState, AccountStateMap},
    26→};
    27→
    28→type HmacSha256 = Hmac<Sha256>;
    29→
    30→/// Register an Events API account.
    31→///
    32→/// Unlike Socket Mode, this only authenticates the bot token and registers
    33→/// account state. The actual event receiving is done by the HTTP webhook
    34→/// handler in the gateway server.
    35→pub async fn register_events_api_account(
    36→    account_id: &str,
    37→    config: SlackAccountConfig,
    38→    accounts: AccountStateMap,
    39→    message_log: Option<Arc<dyn MessageLog>>,
    40→    event_sink: Option<Arc<dyn ChannelEventSink>>,
    41→) -> moltis_channels::Result<()> {
    42→    let bot_token_str = config.bot_token.expose_secret().clone();
    43→
    44→    if bot_token_str.is_empty() {
    45→        return Err(moltis_channels::Error::invalid_input(
    46→            "Slack bot_token is required",
    47→        ));
    48→    }
    49→
    50→    let client = Arc::new(SlackClient::new(SlackClientHyperConnector::new().map_err(
    51→        |e| moltis_channels::Error::unavailable(format!("hyper connector: {e}")),
    52→    )?));
    53→
    54→    // Verify the bot token and get the bot user ID.
    55→    let bot_token = SlackApiToken::new(SlackApiTokenValue::from(bot_token_str));
    56→    let session = client.open_session(&bot_token);
    57→    let auth_response = session
    58→        .auth_test()
    59→        .await
    60→        .map_err(|e| moltis_channels::Error::unavailable(format!("auth.test failed: {e}")))?;
    61→
    62→    let bot_user_id = auth_response.user_id.to_string();
    63→    info!(
    64→        account_id,
    65→        bot_user_id, "slack bot authenticated (events api)"
    66→    );
    67→
    68→    let cancel = tokio_util::sync::CancellationToken::new();
    69→
    70→    {
    71→        let mut accts = accounts.write().unwrap_or_else(|e| e.into_inner());
    72→        accts.insert(account_id.to_string(), AccountState {
    73→            account_id: account_id.to_string(),
    74→            config,
    75→            message_log,
    76→            event_sink,
    77→            cancel,
    78→            bot_user_id: Some(bot_user_id),
    79→            pending_threads: std::collections::HashMap::new(),
    80→        });
    81→    }
    82→
    83→    Ok(())
    84→}
    85→
    86→/// Verify the Slack request signature (HMAC-SHA256).
    87→///
    88→/// Slack sends:
    89→/// - `X-Slack-Signature`: `v0=<hex-hmac>`
    90→/// - `X-Slack-Request-Timestamp`: epoch seconds
    91→///
    92→/// The HMAC base string is `v0:{timestamp}:{body}`.
    93→pub fn verify_signature(
    94→    signing_secret: &str,
    95→    timestamp: &str,
    96→    body: &[u8],
    97→    signature: &str,
    98→) -> bool {
    99→    let sig_hex = match signature.strip_prefix("v0=") {
   100→        Some(hex) => hex,
   101→        None => return false,
   102→    };
   103→
   104→    let Ok(sig_bytes) = hex_decode(sig_hex) else {
   105→        return false;
   106→    };
   107→
   108→    // Use the hmac crate's verify_slice for constant-time comparison.
   109→    let Ok(mut mac) = HmacSha256::new_from_slice(signing_secret.as_bytes()) else {
   110→        return false;
   111→    };
   112→    mac.update(b"v0:");
   113→    mac.update(timestamp.as_bytes());
   114→    mac.update(b":");
   115→    mac.update(body);
   116→    mac.verify_slice(&sig_bytes).is_ok()
   117→}
   118→
   119→/// Simple hex decoding (avoids adding another dependency).
   120→fn hex_decode(hex: &str) -> Result<Vec<u8>, ()> {
   121→    if !hex.len().is_multiple_of(2) {
   122→        return Err(());
   123→    }
   124→    (0..hex.len())
   125→        .step_by(2)
   126→        .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).map_err(|_| ()))
   127→        .collect()
   128→}
   129→
   130→/// Handle an Events API webhook request.
   131→///
   132→/// Returns `Ok(Some(challenge))` for URL verification requests,
   133→/// `Ok(None)` for normal event dispatches.
   134→pub async fn handle_webhook(
   135→    account_id: &str,
   136→    body: &[u8],
   137→    timestamp: &str,
   138→    signature: &str,
   139→    accounts: &AccountStateMap,
   140→) -> moltis_channels::Result<Option<String>> {
   141→    // Look up the account and verify the signature.
   142→    let signing_secret = {
   143→        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   144→        let state = accts
   145→            .get(account_id)
   146→            .ok_or_else(|| moltis_channels::Error::unknown_account(account_id))?;
   147→        state
   148→            .config
   149→            .signing_secret
   150→            .as_ref()
   151→            .map(|s| s.expose_secret().clone())
   152→            .ok_or_else(|| moltis_channels::Error::invalid_input("signing_secret not configured"))?
   153→    };
   154→
   155→    if !verify_signature(&signing_secret, timestamp, body, signature) {
   156→        return Err(moltis_channels::Error::invalid_input(
   157→            "invalid Slack webhook signature",
   158→        ));
   159→    }
   160→
   161→    let payload: serde_json::Value = serde_json::from_slice(body)?;
   162→
   163→    // URL verification challenge.
   164→    if payload.get("type").and_then(|v| v.as_str()) == Some("url_verification") {
   165→        let challenge = payload
   166→            .get("challenge")
   167→            .and_then(|v| v.as_str())
   168→            .unwrap_or("")
   169→            .to_string();
   170→        return Ok(Some(challenge));
   171→    }
   172→
   173→    // Event callback.
   174→    if payload.get("type").and_then(|v| v.as_str()) == Some("event_callback") {
   175→        dispatch_event_callback(account_id, &payload, accounts).await;
   176→    }
   177→
   178→    Ok(None)
   179→}
   180→
   181→/// Handle an already-verified Events API webhook request.
   182→///
   183→/// The caller (channel webhook middleware) has already verified the signature,
   184→/// checked timestamp staleness, and performed idempotency dedup.
   185→///
   186→/// Returns `Ok(Some(challenge))` for URL verification, `Ok(None)` for events.
   187→pub async fn handle_verified_webhook(
   188→    account_id: &str,
   189→    body: &[u8],
   190→    accounts: &AccountStateMap,
   191→) -> moltis_channels::Result<Option<String>> {
   192→    let payload: serde_json::Value = serde_json::from_slice(body)?;
   193→
   194→    // URL verification challenge.
   195→    if payload.get("type").and_then(|v| v.as_str()) == Some("url_verification") {
   196→        let challenge = payload
   197→            .get("challenge")
   198→            .and_then(|v| v.as_str())
   199→            .unwrap_or("")
   200→            .to_string();
   201→        return Ok(Some(challenge));
   202→    }
   203→
   204→    // Event callback.
   205→    if payload.get("type").and_then(|v| v.as_str()) == Some("event_callback") {
   206→        dispatch_event_callback(account_id, &payload, accounts).await;
   207→    }
   208→
   209→    Ok(None)
   210→}
   211→
   212→/// Handle an already-verified interaction webhook request.
   213→///
   214→/// The caller (channel webhook middleware) has already verified the signature.
   215→pub async fn handle_verified_interaction_webhook(
   216→    account_id: &str,
   217→    body: &[u8],
   218→    accounts: &AccountStateMap,
   219→) -> moltis_channels::Result<()> {
   220→    // Parse form-encoded body to extract `payload` field.
   221→    let body_str = std::str::from_utf8(body)
   222→        .map_err(|e| moltis_channels::Error::invalid_input(format!("invalid utf-8: {e}")))?;
   223→
   224→    let payload_json = extract_form_payload(body_str).ok_or_else(|| {
   225→        moltis_channels::Error::invalid_input("missing payload field in interaction")
   226→    })?;
   227→
   228→    let payload: serde_json::Value = serde_json::from_str(&payload_json)?;
   229→
   230→    let interaction_type = payload.get("type").and_then(|v| v.as_str()).unwrap_or("");
   231→
   232→    if interaction_type != "block_actions" {
   233→        debug!(account_id, interaction_type, "unhandled interaction type");
   234→        return Ok(());
   235→    }
   236→
   237→    let action_id = payload
   238→        .get("actions")
   239→        .and_then(|a| a.as_array())
   240→        .and_then(|a| a.first())
   241→        .and_then(|a| a.get("action_id"))
   242→        .and_then(|v| v.as_str())
   243→        .unwrap_or("");
   244→
   245→    let channel_id = payload
   246→        .get("channel")
   247→        .and_then(|c| c.get("id"))
   248→        .and_then(|v| v.as_str())
   249→        .unwrap_or("");
   250→
   251→    if action_id.is_empty() || channel_id.is_empty() {
   252→        debug!(account_id, "interaction missing action_id or channel");
   253→        return Ok(());
   254→    }
   255→
   256→    let event_sink = {
   257→        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   258→        accts.get(account_id).and_then(|s| s.event_sink.clone())
   259→    };
   260→
   261→    if let Some(sink) = event_sink {
   262→        let reply_to = ChannelReplyTarget {
   263→            channel_type: ChannelType::Slack,
   264→            account_id: account_id.to_string(),
   265→            chat_id: channel_id.to_string(),
   266→            message_id: None,
   267→            thread_id: None,
   268→        };
   269→        match sink.dispatch_interaction(action_id, reply_to).await {
   270→            Ok(_) => {},
   271→            Err(e) => {
   272→                debug!(account_id, action_id, "interaction dispatch failed: {e}");
   273→            },
   274→        }
   275→    }
   276→
   277→    Ok(())
   278→}
   279→
   280→/// Dispatch an event_callback payload to the appropriate handler.
   281→async fn dispatch_event_callback(
   282→    account_id: &str,
   283→    payload: &serde_json::Value,
   284→    accounts: &AccountStateMap,
   285→) {
   286→    let Some(event) = payload.get("event") else {
   287→        debug!("event_callback missing event field");
   288→        return;
   289→    };
   290→
   291→    let event_type = event.get("type").and_then(|v| v.as_str()).unwrap_or("");
   292→
   293→    match event_type {
   294→        "message" => {
   295→            // Parse as SlackMessageEvent via serde.
   296→            match serde_json::from_value::<SlackMessageEvent>(event.clone()) {
   297→                Ok(msg_event) => {
   298→                    crate::socket::handle_message_event(account_id, msg_event, accounts).await;
   299→                },
   300→                Err(e) => {
   301→                    debug!(account_id, "failed to parse message event: {e}");
   302→                },
   303→            }
   304→        },
   305→        "app_mention" => {
   306→            // Parse app_mention event manually since the type may differ.
   307→            let channel = event.get("channel").and_then(|v| v.as_str()).unwrap_or("");
   308→            let user = event.get("user").and_then(|v| v.as_str()).unwrap_or("");
   309→            let text = event.get("text").and_then(|v| v.as_str()).unwrap_or("");
   310→            let thread_ts = event
   311→                .get("thread_ts")
   312→                .and_then(|v| v.as_str())
   313→                .map(String::from);
   314→
   315→            if !channel.is_empty() && !user.is_empty() {
   316→                crate::socket::handle_inbound(
   317→                    account_id, channel, user, text, thread_ts, None, true, // is_mention
   318→                    accounts,
   319→                )
   320→                .await;
   321→            }
   322→        },
   323→        "reaction_added" | "reaction_removed" => {
   324→            let user = event.get("user").and_then(|v| v.as_str()).unwrap_or("");
   325→            let reaction = event.get("reaction").and_then(|v| v.as_str()).unwrap_or("");
   326→            let item = event.get("item");
   327→
   328→            if let Some(item) = item {
   329→                // Extract channel and message_ts from the item.
   330→                let item_channel = item.get("channel").and_then(|v| v.as_str()).unwrap_or("");
   331→                let message_ts = item.get("ts").and_then(|v| v.as_str()).unwrap_or("");
   332→
   333→                if !user.is_empty() && !reaction.is_empty() && !item_channel.is_empty() {
   334→                    let added = event_type == "reaction_added";
   335→
   336→                    // Dispatch reaction via the event sink directly since
   337→                    // handle_reaction_event expects a SlackReactionsItem.
   338→                    let event_sink = {
   339→                        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   340→                        accts.get(account_id).and_then(|s| s.event_sink.clone())
   341→                    };
   342→                    if let Some(sink) = event_sink {
   343→                        sink.emit(moltis_channels::ChannelEvent::ReactionChange {
   344→                            channel_type: ChannelType::Slack,
   345→                            account_id: account_id.to_string(),
   346→                            chat_id: item_channel.to_string(),
   347→                            message_id: message_ts.to_string(),
   348→                            user_id: user.to_string(),
   349→                            emoji: reaction.to_string(),
   350→                            added,
   351→                        })
   352→                        .await;
   353→                    }
   354→                }
   355→            }
   356→        },
   357→        _ => {
   358→            debug!(account_id, event_type, "unhandled events api event type");
   359→        },
   360→    }
   361→}
   362→
   363→/// Handle an interaction payload from the Events API.
   364→///
   365→/// Slack sends interaction payloads as `application/x-www-form-urlencoded`
   366→/// with a `payload` field containing JSON.
   367→pub async fn handle_interaction_webhook(
   368→    account_id: &str,
   369→    body: &[u8],
   370→    timestamp: &str,
   371→    signature: &str,
   372→    accounts: &AccountStateMap,
   373→) -> moltis_channels::Result<()> {
   374→    // Verify signature.
   375→    let signing_secret = {
   376→        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   377→        let state = accts
   378→            .get(account_id)
   379→            .ok_or_else(|| moltis_channels::Error::unknown_account(account_id))?;
   380→        state
   381→            .config
   382→            .signing_secret
   383→            .as_ref()
   384→            .map(|s| s.expose_secret().clone())
   385→            .ok_or_else(|| moltis_channels::Error::invalid_input("signing_secret not configured"))?
   386→    };
   387→
   388→    if !verify_signature(&signing_secret, timestamp, body, signature) {
   389→        return Err(moltis_channels::Error::invalid_input(
   390→            "invalid Slack webhook signature",
   391→        ));
   392→    }
   393→
   394→    // Parse form-encoded body to extract `payload` field.
   395→    let body_str = std::str::from_utf8(body)
   396→        .map_err(|e| moltis_channels::Error::invalid_input(format!("invalid utf-8: {e}")))?;
   397→
   398→    let payload_json = extract_form_payload(body_str).ok_or_else(|| {
   399→        moltis_channels::Error::invalid_input("missing payload field in interaction")
   400→    })?;
   401→
   402→    let payload: serde_json::Value = serde_json::from_str(&payload_json)?;
   403→
   404→    // Extract action from block_actions.
   405→    let interaction_type = payload.get("type").and_then(|v| v.as_str()).unwrap_or("");
   406→
   407→    if interaction_type != "block_actions" {
   408→        debug!(account_id, interaction_type, "unhandled interaction type");
   409→        return Ok(());
   410→    }
   411→
   412→    let action_id = payload
   413→        .get("actions")
   414→        .and_then(|a| a.as_array())
   415→        .and_then(|a| a.first())
   416→        .and_then(|a| a.get("action_id"))
   417→        .and_then(|v| v.as_str())
   418→        .unwrap_or("");
   419→
   420→    let channel_id = payload
   421→        .get("channel")
   422→        .and_then(|c| c.get("id"))
   423→        .and_then(|v| v.as_str())
   424→        .unwrap_or("");
   425→
   426→    if action_id.is_empty() || channel_id.is_empty() {
   427→        debug!(account_id, "interaction missing action_id or channel");
   428→        return Ok(());
   429→    }
   430→
   431→    let event_sink = {
   432→        let accts = accounts.read().unwrap_or_else(|e| e.into_inner());
   433→        accts.get(account_id).and_then(|s| s.event_sink.clone())
   434→    };
   435→
   436→    if let Some(sink) = event_sink {
   437→        let reply_to = ChannelReplyTarget {
   438→            channel_type: ChannelType::Slack,
   439→            account_id: account_id.to_string(),
   440→            chat_id: channel_id.to_string(),
   441→            message_id: None,
   442→            thread_id: None,
   443→        };
   444→        match sink.dispatch_interaction(action_id, reply_to).await {
   445→            Ok(_) => {},
   446→            Err(e) => {
   447→                debug!(account_id, action_id, "interaction dispatch failed: {e}");
   448→            },
   449→        }
   450→    }
   451→
   452→    Ok(())
   453→}
   454→
   455→/// Extract the `payload` field from a `application/x-www-form-urlencoded` body.
   456→fn extract_form_payload(body: &str) -> Option<String> {
   457→    for pair in body.split('&') {
   458→        if let Some(value) = pair.strip_prefix("payload=") {
   459→            // URL-decode the value.
   460→            return url_decode(value);
   461→        }
   462→    }
   463→    None
   464→}
   465→
   466→/// Simple percent-decoding for URL-encoded strings.
   467→fn url_decode(input: &str) -> Option<String> {
   468→    let mut result = Vec::with_capacity(input.len());
   469→    let mut chars = input.bytes();
   470→
   471→    while let Some(b) = chars.next() {
   472→        match b {
   473→            b'%' => {
   474→                let hi = chars.next()?;
   475→                let lo = chars.next()?;
   476→                let byte = u8::from_str_radix(&format!("{}{}", hi as char, lo as char), 16).ok()?;
   477→                result.push(byte);
   478→            },
   479→            b'+' => result.push(b' '),
   480→            _ => result.push(b),
   481→        }
   482→    }
   483→
   484→    String::from_utf8(result).ok()
   485→}
   486→
   487→#[cfg(test)]
   488→#[allow(clippy::unwrap_used)]
   489→mod tests {
   490→    use super::*;
   491→
   492→    #[test]
   493→    fn verify_valid_signature() {
   494→        let secret = "REDACTED";
   495→        let timestamp = "1531420618";
   496→        let body = b"REDACTED&team_id=T1DC2JH3J&team_domain=testteamnow&channel_id=G8LX6B8TU&channel_name=mpmulti&user_id=U2CERLKJA&user_name=roadrunner&command=%2Fwebhook-collect&text=&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT1DC2JH3J%2F397700885554%2F96rGlfmibIGlgcZRskXaIFfN&trigger_id=398738663015.47445629121.803a0bc887a14d10d2c659f2945b6e92";
   497→
   498→        // Compute expected signature.
   499→        use hmac::Mac;
   500→        let mut mac = HmacSha256::new_from_slice(secret.as_bytes()).unwrap();
   501→        mac.update(format!("v0:{timestamp}:").as_bytes());
   502→        mac.update(body);
   503→        let result = mac.finalize().into_bytes();
   504→        let hex: String = result.iter().map(|b| format!("{b:02x}")).collect();
   505→        let signature = format!("v0={hex}");
   506→
   507→        assert!(verify_signature(secret, timestamp, body, &signature));
   508→    }
   509→
   510→    #[test]
   511→    fn verify_rejects_bad_signature() {
   512→        assert!(!verify_signature(
   513→            "secret",
   514→            "12345",
   515→            b"body",
   516→            "v0=0000000000000000000000000000000000000000000000000000000000000000"
   517→        ));
   518→    }
   519→
   520→    #[test]
   521→    fn verify_rejects_missing_prefix() {
   522→        assert!(!verify_signature("secret", "12345", b"body", "bad"));
   523→    }
   524→
   525→    #[test]
   526→    fn hex_decode_valid() {
   527→        assert_eq!(hex_decode("48656c6c6f"), Ok(b"Hello".to_vec()));
   528→    }
   529→
   530→    #[test]
   531→    fn hex_decode_odd_length() {
   532→        assert!(hex_decode("abc").is_err());
   533→    }
   534→
   535→    #[test]
   536→    fn url_decode_basic() {
   537→        assert_eq!(
   538→            url_decode("hello+world%21"),
   539→            Some("hello world!".to_string())
   540→        );
   541→    }
   542→
   543→    #[test]
   544→    fn url_decode_json_payload() {
   545→        let encoded = "%7B%22type%22%3A%22block_actions%22%7D";
   546→        assert_eq!(
   547→            url_decode(encoded),
   548→            Some(r#"{"type":"block_actions"}"#.to_string())
   549→        );
   550→    }
   551→
   552→    #[test]
   553→    fn extract_form_payload_finds_payload() {
   554→        let body = "token=abc&payload=%7B%22type%22%3A%22test%22%7D&other=val";
   555→        let result = extract_form_payload(body);
   556→        assert_eq!(result, Some(r#"{"type":"test"}"#.to_string()));
   557→    }
   558→
   559→    #[test]
   560→    fn extract_form_payload_missing() {
   561→        let body = "token=abc&other=val";
   562→        assert!(extract_form_payload(body).is_none());
   563→    }
   564→}
   565→
```

> AGENT

The API usage is all via `slack_morphism::prelude::*` — standard types that are stable across 2.x. The bump should be safe. Let me apply the fix.

> TOOL

tool_use Edit
id: toolu_01N4HXTysu72fR6LELyDjAkV
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/alabaster-fur/Cargo.toml",
  "old_string": "slack-morphism     = { features = [\"axum\", \"hyper\"], version = \"2.6\" }",
  "new_string": "slack-morphism     = { features = [\"axum\", \"hyper\"], version = \"2.20\" }"
}
```

> TOOL

tool_result
id: toolu_01N4HXTysu72fR6LELyDjAkV
```
The file /Users/penso/.superset/worktrees/moltis/alabaster-fur/Cargo.toml has been updated successfully.
```

> AGENT

Now let me update the lockfile and verify it compiles.

> TOOL

tool_use Bash
id: toolu_01TL2DJw9m2eXCQiXS9mkJec
```json
{
  "command": "cargo fetch 2>&1",
  "description": "Update lockfile with new slack-morphism version",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01TL2DJw9m2eXCQiXS9mkJec
```
    Updating crates.io index
     Locking 10 packages to latest compatible versions
      Adding block-buffer v0.12.0
      Adding cmov v0.5.3
      Adding const-oid v0.10.2
      Adding ctutils v0.4.2
      Adding digest v0.11.2
      Adding hmac v0.13.0
      Adding sha2 v0.11.0
    Updating slack-morphism v2.18.0 -> v2.20.0
      Adding tokio-tungstenite v0.29.0
      Adding tungstenite v0.29.0
 Downloading crates ...
  Downloaded tungstenite v0.29.0
  Downloaded sha2 v0.11.0
  Downloaded tokio-tungstenite v0.29.0
  Downloaded cmov v0.5.3
  Downloaded hmac v0.13.0
  Downloaded ctutils v0.4.2
  Downloaded slack-morphism v2.20.0
```

> AGENT

Resolved cleanly — `slack-morphism` 2.18.0 → 2.20.0, and it pulled in `tokio-tungstenite` 0.29.0 (newer than 0.28). Let me verify the TLS features are now enabled.

> TOOL

tool_use Bash
id: toolu_01EXh854PyQk5f4kyqzL6sJy
```json
{
  "command": "cargo metadata --format-version 1 2>/dev/null | jq '.resolve.nodes[] | select(.id | contains(\"tokio-tungstenite@0.29\")) | .features'",
  "description": "Verify TLS features on tokio-tungstenite 0.29"
}
```

> TOOL

tool_result
id: toolu_01EXh854PyQk5f4kyqzL6sJy
```
[
  "__rustls-tls",
  "connect",
  "default",
  "handshake",
  "rustls",
  "rustls-native-certs",
  "rustls-pki-types",
  "rustls-tls-native-roots",
  "stream",
  "tokio-rustls"
]
```

> AGENT

The full TLS stack is now enabled: `__rustls-tls`, `rustls`, `tokio-rustls`, `rustls-tls-native-roots`. Let me verify it compiles.

> TOOL

tool_use Bash
id: toolu_01BQPigCTNmBkzQiJCBU745t
```json
{
  "command": "cargo check -p moltis-slack 2>&1",
  "description": "Check moltis-slack compiles with new slack-morphism",
  "timeout": 300000
}
```

> TOOL

tool_result
id: toolu_01BQPigCTNmBkzQiJCBU745t
```
   Compiling proc-macro2 v1.0.106
   Compiling unicode-ident v1.0.22
   Compiling quote v1.0.44
   Compiling libc v0.2.180
    Checking cfg-if v1.0.4
    Checking pin-project-lite v0.2.16
    Checking smallvec v1.15.1
    Checking bytes v1.11.1
    Checking futures-core v0.3.31
   Compiling parking_lot_core v0.9.12
    Checking once_cell v1.21.3
    Checking core-foundation-sys v0.8.7
    Checking itoa v1.0.17
    Checking scopeguard v1.2.0
   Compiling serde_core v1.0.228
    Checking futures-sink v0.3.31
   Compiling typenum v1.19.0
    Checking bitflags v2.10.0
   Compiling serde v1.0.228
    Checking stable_deref_trait v1.2.1
    Checking lock_api v0.4.14
    Checking memchr v2.8.0
    Checking log v0.4.29
    Checking futures-channel v0.3.31
   Compiling getrandom v0.3.4
   Compiling shlex v1.3.0
   Compiling find-msvc-tools v0.1.9
    Checking slab v0.4.12
    Checking tracing-core v0.1.36
    Checking futures-task v0.3.31
   Compiling cc v1.2.55
    Checking pin-utils v0.1.0
    Checking equivalent v1.0.2
    Checking hashbrown v0.16.1
    Checking futures-io v0.3.31
    Checking zeroize v1.8.2
   Compiling httparse v1.10.1
   Compiling version_check v0.9.5
    Checking http v1.4.0
    Checking rustls-pki-types v1.14.0
    Checking writeable v0.6.2
    Checking percent-encoding v2.3.2
    Checking tower-service v0.3.3
    Checking litemap v0.8.1
   Compiling generic-array v0.14.9
   Compiling system-configuration-sys v0.6.0
    Checking atomic-waker v1.1.2
   Compiling icu_properties_data v2.1.2
   Compiling zmij v1.0.19
    Checking fnv v1.0.7
    Checking subtle v2.6.1
    Checking indexmap v2.13.0
   Compiling icu_normalizer_data v2.1.1
    Checking try-lock v0.2.5
    Checking want v0.3.1
    Checking http-body v1.0.1
    Checking httpdate v1.0.3
   Compiling rustix v1.1.3
   Compiling serde_json v1.0.149
    Checking ipnet v2.11.0
    Checking sync_wrapper v1.0.2
    Checking base64 v0.22.1
   Compiling autocfg v1.5.0
   Compiling ring v0.17.14
   Compiling thiserror v2.0.18
   Compiling syn v2.0.114
    Checking tower-layer v0.3.3
    Checking ryu v1.0.22
   Compiling zerocopy v0.8.39
    Checking errno v0.3.14
    Checking signal-hook-registry v1.4.8
    Checking mio v1.1.1
    Checking socket2 v0.6.2
    Checking parking_lot v0.12.5
    Checking core-foundation v0.9.4
    Checking security-framework-sys v2.15.0
    Checking getrandom v0.2.17
    Checking untrusted v0.9.0
   Compiling num-traits v0.2.19
    Checking http-body-util v0.1.3
    Checking form_urlencoded v1.2.2
    Checking fastrand v2.3.0
   Compiling unicase v2.9.0
   Compiling native-tls v0.2.14
    Checking mime v0.3.17
   Compiling rustls v0.23.36
   Compiling mime_guess v2.0.5
    Checking security-framework v2.11.1
    Checking hybrid-array v0.4.10
   Compiling ident_case v1.0.1
    Checking utf8_iter v1.0.4
   Compiling strsim v0.11.1
   Compiling syn v1.0.109
    Checking rand_core v0.9.5
    Checking crypto-common v0.1.6
    Checking block-buffer v0.10.4
    Checking cpufeatures v0.2.17
    Checking system-configuration v0.7.0
    Checking core-foundation v0.10.1
    Checking digest v0.10.7
    Checking iana-time-zone v0.1.65
    Checking cmov v0.5.3
    Checking siphasher v1.0.2
    Checking rand_core v0.10.0
   Compiling getrandom v0.4.1
    Checking phf_shared v0.12.1
    Checking ctutils v0.4.2
    Checking security-framework v3.5.1
    Checking block-buffer v0.12.0
    Checking crypto-common v0.2.1
   Compiling signal-hook v0.4.3
    Checking option-ext v0.2.0
    Checking iri-string v0.7.10
    Checking toml_write v0.1.2
   Compiling anyhow v1.0.101
   Compiling chrono-tz v0.10.4
    Checking const-oid v0.10.2
    Checking winnow v0.7.14
    Checking digest v0.11.2
    Checking rustls-native-certs v0.8.3
    Checking dirs-sys v0.5.0
    Checking phf v0.12.1
    Checking chacha20 v0.10.0
    Checking sha1 v0.10.6
    Checking encoding_rs v0.8.35
    Checking data-encoding v2.10.0
   Compiling synstructure v0.13.2
   Compiling darling_core v0.21.3
    Checking unsafe-libyaml v0.2.11
    Checking tempfile v3.24.0
    Checking directories v6.0.0
    Checking serde_path_to_error v0.1.20
    Checking uuid v1.20.0
    Checking cpufeatures v0.3.0
    Checking matchit v0.8.4
    Checking sha2 v0.11.0
    Checking hmac v0.13.0
    Checking lazy_static v1.5.0
    Checking hex v0.4.3
    Checking hmac v0.12.1
    Checking sha2 v0.10.9
   Compiling tokio-macros v2.6.0
   Compiling zerofrom-derive v0.1.6
   Compiling yoke-derive v0.8.1
   Compiling serde_derive v1.0.228
   Compiling zerovec-derive v0.11.2
   Compiling tracing-attributes v0.1.31
   Compiling futures-macro v0.3.31
   Compiling displaydoc v0.2.5
    Checking tokio v1.49.0
    Checking futures-util v0.3.31
   Compiling thiserror-impl v2.0.18
    Checking zerofrom v0.1.6
   Compiling async-trait v0.1.89
    Checking tracing v0.1.44
    Checking rand v0.10.0
   Compiling async-recursion v1.1.1
   Compiling darling_macro v0.21.3
   Compiling darling v0.21.3
    Checking rustls-webpki v0.103.10
    Checking yoke v0.8.1
    Checking axum-core v0.5.6
    Checking ppv-lite86 v0.2.21
   Compiling rvs_derive v0.3.2
   Compiling rsb_derive v0.5.1
    Checking rand_chacha v0.9.0
    Checking rand v0.9.4
    Checking rvstruct v0.3.2
   Compiling serde_with_macros v3.16.1
    Checking serde_with v3.16.1
    Checking futures-executor v0.3.31
    Checking futures v0.3.31
    Checking zerovec v0.11.5
    Checking zerotrie v0.2.3
    Checking serde_urlencoded v0.7.1
    Checking chrono v0.4.43
    Checking toml_datetime v0.6.11
    Checking serde_spanned v0.6.9
    Checking secrecy v0.8.0
    Checking serde_yaml v0.9.34+deprecated
    Checking toml_edit v0.22.27
    Checking tungstenite v0.29.0
    Checking tokio-util v0.7.18
    Checking tower v0.5.3
    Checking tokio-native-tls v0.3.1
    Checking tokio-rustls v0.26.4
    Checking futures-locks v0.7.1
    Checking signal-hook-tokio v0.4.0
    Checking tokio-stream v0.1.18
    Checking tokio-tungstenite v0.29.0
    Checking tinystr v0.8.2
    Checking potential_utf v0.1.4
    Checking icu_collections v2.1.1
    Checking h2 v0.4.13
    Checking icu_locale_core v2.1.1
    Checking tower-http v0.6.8
    Checking toml v0.8.23
    Checking icu_provider v2.1.1
    Checking icu_properties v2.1.2
    Checking icu_normalizer v2.1.1
    Checking idna_adapter v1.2.1
    Checking idna v1.1.0
    Checking url v2.5.8
    Checking hyper v1.8.1
    Checking hyper-util v0.1.20
    Checking moltis-config v0.1.0 (/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/config)
    Checking hyper-tls v0.6.0
    Checking hyper-rustls v0.27.7
    Checking axum v0.8.8
    Checking reqwest v0.12.28
    Checking moltis-common v0.1.0 (/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/common)
    Checking moltis-channels v0.1.0 (/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/channels)
    Checking slack-morphism v2.20.0
    Checking moltis-slack v0.1.0 (/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 27.86s
```

> AGENT

Compiles cleanly with zero warnings. Let me also run the slack tests.

> TOOL

tool_use Bash
id: toolu_013cs85Q2CACqZJZjULbVW4P
```json
{
  "command": "cargo test -p moltis-slack 2>&1",
  "description": "Run moltis-slack tests",
  "timeout": 180000
}
```

> TOOL

tool_result
id: toolu_013cs85Q2CACqZJZjULbVW4P
```
   Compiling cfg-if v1.0.4
   Compiling pin-project-lite v0.2.16
   Compiling smallvec v1.15.1
   Compiling bytes v1.11.1
   Compiling futures-core v0.3.31
   Compiling itoa v1.0.17
   Compiling core-foundation-sys v0.8.7
   Compiling once_cell v1.21.3
   Compiling scopeguard v1.2.0
   Compiling futures-sink v0.3.31
   Compiling bitflags v2.10.0
   Compiling libc v0.2.180
   Compiling serde_core v1.0.228
   Compiling stable_deref_trait v1.2.1
   Compiling log v0.4.29
   Compiling zerofrom v0.1.6
   Compiling memchr v2.8.0
   Compiling lock_api v0.4.14
   Compiling typenum v1.19.0
   Compiling slab v0.4.12
   Compiling futures-channel v0.3.31
   Compiling tracing-core v0.1.36
   Compiling yoke v0.8.1
   Compiling equivalent v1.0.2
   Compiling fnv v1.0.7
   Compiling hashbrown v0.16.1
   Compiling pin-utils v0.1.0
   Compiling futures-task v0.3.31
   Compiling zeroize v1.8.2
   Compiling zerovec v0.11.5
   Compiling futures-io v0.3.31
   Compiling httparse v1.10.1
   Compiling writeable v0.6.2
   Compiling litemap v0.8.1
   Compiling percent-encoding v2.3.2
   Compiling tower-service v0.3.3
   Compiling zerotrie v0.2.3
   Compiling rustls-pki-types v1.14.0
   Compiling subtle v2.6.1
   Compiling atomic-waker v1.1.2
   Compiling try-lock v0.2.5
   Compiling httpdate v1.0.3
   Compiling ipnet v2.11.0
   Compiling want v0.3.1
   Compiling icu_normalizer_data v2.1.1
   Compiling icu_properties_data v2.1.2
   Compiling zmij v1.0.19
   Compiling sync_wrapper v1.0.2
   Compiling ryu v1.0.22
   Compiling untrusted v0.9.0
   Compiling base64 v0.22.1
   Compiling tower-layer v0.3.3
   Compiling form_urlencoded v1.2.2
   Compiling tracing v0.1.44
   Compiling mime v0.3.17
   Compiling unicase v2.9.0
   Compiling fastrand v2.3.0
   Compiling thiserror v2.0.18
   Compiling futures-util v0.3.31
   Compiling mime_guess v2.0.5
   Compiling errno v0.3.14
   Compiling parking_lot_core v0.9.12
   Compiling socket2 v0.6.2
   Compiling mio v1.1.1
   Compiling signal-hook-registry v1.4.8
   Compiling getrandom v0.3.4
   Compiling security-framework-sys v2.15.0
   Compiling core-foundation v0.9.4
   Compiling system-configuration-sys v0.6.0
   Compiling getrandom v0.2.17
   Compiling parking_lot v0.12.5
   Compiling ring v0.17.14
   Compiling http v1.4.0
   Compiling rustix v1.1.3
   Compiling zerocopy v0.8.39
   Compiling utf8_iter v1.0.4
   Compiling tinystr v0.8.2
   Compiling potential_utf v0.1.4
   Compiling indexmap v2.13.0
   Compiling darling_core v0.21.3
   Compiling icu_collections v2.1.1
   Compiling icu_locale_core v2.1.1
   Compiling system-configuration v0.7.0
   Compiling security-framework v2.11.1
   Compiling num-traits v0.2.19
   Compiling tokio v1.49.0
   Compiling rand_core v0.9.5
   Compiling generic-array v0.14.9
   Compiling hybrid-array v0.4.10
   Compiling core-foundation v0.10.1
   Compiling cpufeatures v0.2.17
   Compiling iana-time-zone v0.1.65
   Compiling siphasher v1.0.2
   Compiling rand_core v0.10.0
   Compiling cmov v0.5.3
   Compiling http-body v1.0.1
   Compiling phf_shared v0.12.1
   Compiling security-framework v3.5.1
   Compiling ctutils v0.4.2
   Compiling http-body-util v0.1.3
   Compiling icu_provider v2.1.1
   Compiling crypto-common v0.2.1
   Compiling block-buffer v0.10.4
   Compiling crypto-common v0.1.6
   Compiling icu_properties v2.1.2
   Compiling icu_normalizer v2.1.1
   Compiling digest v0.10.7
   Compiling tempfile v3.24.0
   Compiling block-buffer v0.12.0
   Compiling toml_write v0.1.2
   Compiling const-oid v0.10.2
   Compiling native-tls v0.2.14
   Compiling winnow v0.7.14
   Compiling iri-string v0.7.10
   Compiling option-ext v0.2.0
   Compiling sha1 v0.10.6
   Compiling phf v0.12.1
   Compiling dirs-sys v0.5.0
   Compiling getrandom v0.4.1
   Compiling chacha20 v0.10.0
   Compiling encoding_rs v0.8.35
   Compiling unsafe-libyaml v0.2.11
   Compiling data-encoding v2.10.0
   Compiling rand v0.10.0
   Compiling directories v6.0.0
   Compiling signal-hook v0.4.3
   Compiling rustls-webpki v0.103.10
   Compiling digest v0.11.2
   Compiling rustls-native-certs v0.8.3
   Compiling anyhow v1.0.101
   Compiling axum-core v0.5.6
   Compiling idna_adapter v1.2.1
   Compiling uuid v1.20.0
   Compiling idna v1.1.0
   Compiling cpufeatures v0.3.0
   Compiling matchit v0.8.4
   Compiling sha2 v0.11.0
   Compiling serde v1.0.228
   Compiling serde_json v1.0.149
   Compiling serde_path_to_error v0.1.20
   Compiling rvstruct v0.3.2
   Compiling hmac v0.13.0
   Compiling hex v0.4.3
   Compiling rustls v0.23.36
   Compiling lazy_static v1.5.0
   Compiling sha2 v0.10.9
   Compiling hmac v0.12.1
   Compiling darling_macro v0.21.3
   Compiling serde_urlencoded v0.7.1
   Compiling url v2.5.8
   Compiling toml_datetime v0.6.11
   Compiling chrono v0.4.43
   Compiling serde_spanned v0.6.9
   Compiling darling v0.21.3
   Compiling secrecy v0.8.0
   Compiling serde_yaml v0.9.34+deprecated
   Compiling futures-executor v0.3.31
   Compiling futures v0.3.31
   Compiling serde_with_macros v3.16.1
   Compiling toml_edit v0.22.27
   Compiling serde_with v3.16.1
   Compiling chrono-tz v0.10.4
   Compiling ppv-lite86 v0.2.21
   Compiling rand_chacha v0.9.0
   Compiling rand v0.9.4
   Compiling toml v0.8.23
   Compiling tokio-util v0.7.18
   Compiling tower v0.5.3
   Compiling tokio-native-tls v0.3.1
   Compiling futures-locks v0.7.1
   Compiling signal-hook-tokio v0.4.0
   Compiling tokio-stream v0.1.18
   Compiling tokio-rustls v0.26.4
   Compiling tungstenite v0.29.0
   Compiling tower-http v0.6.8
   Compiling h2 v0.4.13
   Compiling tokio-tungstenite v0.29.0
   Compiling hyper v1.8.1
   Compiling moltis-config v0.1.0 (/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/config)
   Compiling hyper-util v0.1.20
   Compiling hyper-tls v0.6.0
   Compiling axum v0.8.8
   Compiling hyper-rustls v0.27.7
   Compiling reqwest v0.12.28
   Compiling moltis-common v0.1.0 (/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/common)
   Compiling moltis-channels v0.1.0 (/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/channels)
   Compiling slack-morphism v2.20.0
   Compiling moltis-slack v0.1.0 (/Users/penso/.superset/worktrees/moltis/alabaster-fur/crates/slack)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 28.62s
     Running unittests src/lib.rs (target/debug/deps/moltis_slack-bbe81bcbcb9021c2)

running 70 tests
test channel_webhook_verifier::tests::channel_type_is_slack ... ok
test channel_webhook_verifier::tests::contract_has_valid_rate_policy ... ok
test channel_webhook_verifier::tests::contract_has_positive_max_age ... ok
test channel_webhook_verifier::tests::contract_has_channel_type ... ok
test channel_webhook_verifier::tests::rate_policy_is_30_per_minute ... ok
test channel_webhook_verifier::tests::contract_rejects_empty_signature ... ok
test channel_webhook_verifier::tests::missing_timestamp_header_rejects ... ok
test channel_webhook_verifier::tests::missing_signature_header_rejects ... ok
test commands::tests::command_definitions_not_empty ... ok
test commands::tests::manifest_snippet_contains_commands ... ok
test commands::tests::command_definitions_json_structure ... ok
test config::tests::config_view_defaults ... ok
test channel_webhook_verifier::tests::contract_rejects_bad_signature ... ok
test channel_webhook_verifier::tests::bad_signature_rejects ... ok
test config::tests::debug_redacts_signing_secret ... ok
test config::tests::debug_redacts_tokens ... ok
test config::tests::defaults_are_sensible ... ok
test channel_webhook_verifier::tests::no_event_id_yields_none_idempotency_key ... ok
test config::tests::connection_mode_events_api_round_trip ... ok
test config::tests::default_config_round_trips ... ok
test channel_webhook_verifier::tests::valid_signature_passes ... ok
test config::tests::config_with_tokens_round_trip ... ok
test config::tests::redacted_hides_all_secrets ... ok
test config::tests::redacted_omits_none_signing_secret ... ok
test config::tests::overrides_round_trip ... ok
test config::tests::stream_mode_native ... ok
test config::tests::resolve_model_user_overrides_channel ... ok
test config::tests::stream_mode_off ... ok
test markdown::tests::bold_conversion ... ok
test markdown::tests::bracket_without_paren ... ok
test markdown::tests::broken_link_passthrough ... ok
test markdown::tests::chunk_at_newline ... ok
test markdown::tests::chunk_long_line ... ok
test markdown::tests::chunk_short_message ... ok
test markdown::tests::chunk_message_handles_multibyte_boundary ... ok
test markdown::tests::italic_passthrough ... ok
test markdown::tests::header_conversion ... ok
test markdown::tests::strikethrough_conversion ... ok
test markdown::tests::mixed_formatting ... ok
test markdown::tests::link_conversion ... ok
test markdown::tests::strip_bot_mention ... ok
test markdown::tests::strip_no_mention ... ok
test outbound::tests::decode_data_url_no_comma_fails ... ok
test outbound::tests::extension_for_known_mimes ... ok
test outbound::tests::get_thread_ts_from_reply_to ... ok
test outbound::tests::decode_data_url_png ... ok
test outbound::tests::get_thread_ts_no_account ... ok
test plugin::tests::descriptor_coherence ... ok
test plugin::tests::empty_account_ids ... ok
test plugin::tests::plugin_id_and_name ... ok
test plugin::tests::update_config_unknown_account_errors ... ok
test plugin::tests::start_events_api_rejects_missing_signing_secret ... ok
test plugin::tests::start_rejects_empty_bot_token ... ok
test plugin::tests::probe_no_account ... ok
test plugin::tests::start_rejects_empty_app_token ... ok
test socket::tests::channel_allowlist_requires_channel ... ok
test socket::tests::channel_disabled_denies_all ... ok
test socket::tests::channel_open_allows_any ... ok
test socket::tests::dm_disabled_denies_all ... ok
test socket::tests::dm_allowlist_requires_user ... ok
test socket::tests::dm_open_allows_anyone ... ok
test webhook::tests::extract_form_payload_finds_payload ... ok
test webhook::tests::hex_decode_odd_length ... ok
test webhook::tests::hex_decode_valid ... ok
test webhook::tests::url_decode_basic ... ok
test webhook::tests::url_decode_json_payload ... ok
test webhook::tests::verify_rejects_missing_prefix ... ok
test webhook::tests::verify_rejects_bad_signature ... ok
test webhook::tests::extract_form_payload_missing ... ok
test webhook::tests::verify_valid_signature ... ok

test result: ok. 70 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests moltis_slack

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

> AGENT

All 70 tests pass. Let me close the issue and commit.

> TOOL

tool_use Bash
id: toolu_01BhH3vdMwPUfR38K3B6oJ9e
```json
{
  "command": "bd close moltis-0a8 --reason=\"Bumped slack-morphism from 2.18 to 2.20 which fixes the tokio-tungstenite TLS feature mapping\" --json",
  "description": "Close beads issue"
}
```

> TOOL

tool_result
id: toolu_01BhH3vdMwPUfR38K3B6oJ9e
```
[
  {
    "id": "moltis-0a8",
    "title": "Fix Slack socket mode TLS failure (GH #543)",
    "description": "slack-morphism 2.18 maps rustls-native-certs to tokio-tungstenite/rustls-native-certs (cert resolver only), missing the actual TLS stack. Version 2.20 adds tokio-tungstenite/rustls-tls-native-roots. Bump workspace dep to fix.",
    "status": "closed",
    "priority": 1,
    "issue_type": "bug",
    "owner": "gpg@pen.so",
    "created_at": "2026-04-14T10:40:54Z",
    "created_by": "Fabien Penso",
    "updated_at": "2026-04-14T10:42:43Z",
    "closed_at": "2026-04-14T10:42:43Z",
    "close_reason": "Bumped slack-morphism from 2.18 to 2.20 which fixes the tokio-tungstenite TLS feature mapping"
  }
]
```

> AGENT

Done. Here's the summary:

**Fix:** Bumped `slack-morphism` from `2.6` (resolved 2.18.0) to `2.20` in workspace `Cargo.toml`.

**Root cause:** `slack-morphism` 2.18's `rustls-native-certs` feature only enabled `tokio-tungstenite/rustls-native-certs` (the certificate resolver), not `tokio-tungstenite/rustls-tls-native-roots` (the full TLS stack). Version 2.20 adds the missing feature flag.

**Verification:**
- `tokio-tungstenite` now resolves to 0.29.0 with full TLS features: `__rustls-tls`, `rustls`, `tokio-rustls`, `rustls-tls-native-roots`
- `cargo check -p moltis-slack` — clean
- All 70 slack tests pass

The changes are in `Cargo.toml` (version bump) and `Cargo.lock` (dependency update). Ready to commit when you'd like.

> DEVELOPER

commit push create a PR

> TOOL

tool_use Bash
id: toolu_01H7UZMUMatgvMw8NdY58YPs
```json
{
  "command": "git status",
  "description": "Show working tree status"
}
```

> TOOL

tool_result
id: toolu_01H7UZMUMatgvMw8NdY58YPs
```
On branch alabaster-fur
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   Cargo.lock
	modified:   Cargo.toml

no changes added to commit (use "git add" and/or "git commit -a")
```

> TOOL

tool_use Bash
id: toolu_0175fvGPwVix3mZZLBvGmRq5
```json
{
  "command": "git diff",
  "description": "Show staged and unstaged changes"
}
```

> TOOL

tool_result
id: toolu_0175fvGPwVix3mZZLBvGmRq5
```
diff --git a/Cargo.lock b/Cargo.lock
index 40e17999..56793e91 100644
--- a/Cargo.lock
+++ b/Cargo.lock
@@ -1115,7 +1115,7 @@ version = "0.10.6"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "46502ad458c9a52b69d4d4d32775c788b7a1b85e8bc9d482d92250fc0e3f8efe"
 dependencies = [
- "digest",
+ "digest 0.10.7",
 ]
 
 [[package]]
@@ -1152,6 +1152,15 @@ dependencies = [
  "generic-array",
 ]
 
+[[package]]
+name = "block-buffer"
+version = "0.12.0"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "cdd35008169921d80bc60d3d0ab416eecb028c4cd653352907921d95084790be"
+dependencies = [
+ "hybrid-array",
+]
+
 [[package]]
 name = "block-padding"
 version = "0.3.3"
@@ -1647,6 +1656,12 @@ dependencies = [
  "cc",
 ]
 
+[[package]]
+name = "cmov"
+version = "0.5.3"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "3f88a43d011fc4a6876cb7344703e297c71dda42494fee094d5f7c76bf13f746"
+
 [[package]]
 name = "coarsetime"
 version = "0.1.37"
@@ -1810,6 +1825,12 @@ version = "0.9.6"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "c2459377285ad874054d797f3ccebf984978aa39129f6eafde5cdc8315b612f8"
 
+[[package]]
+name = "const-oid"
+version = "0.10.2"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "a6ef517f0926dd24a1582492c791b6a4818a4d94e789a334894aa15b0d12f55c"
+
 [[package]]
 name = "const_panic"
 version = "0.2.15"
@@ -2223,6 +2244,15 @@ dependencies = [
  "windows-sys 0.61.2",
 ]
 
+[[package]]
+name = "ctutils"
+version = "0.4.2"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "7d5515a3834141de9eafb9717ad39eea8247b5674e6066c404e8c4b365d2a29e"
+dependencies = [
+ "cmov",
+]
+
 [[package]]
 name = "curl"
 version = "0.4.49"
@@ -2263,7 +2293,7 @@ dependencies = [
  "cfg-if",
  "cpufeatures 0.2.17",
  "curve25519-dalek-derive",
- "digest",
+ "digest 0.10.7",
  "fiat-crypto",
  "rustc_version",
  "serde",
@@ -2696,12 +2726,24 @@ version = "0.10.7"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "9ed9a281f7bc9b7576e61468ba615a66a5c8cfdff42420a70aa82701a3b1e292"
 dependencies = [
- "block-buffer",
+ "block-buffer 0.10.4",
  "const-oid 0.9.6",
  "crypto-common 0.1.6",
  "subtle",
 ]
 
+[[package]]
+name = "digest"
+version = "0.11.2"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "4850db49bf08e663084f7fb5c87d202ef91a3907271aff24a94eb97ff039153c"
+dependencies = [
+ "block-buffer 0.12.0",
+ "const-oid 0.10.2",
+ "crypto-common 0.2.1",
+ "ctutils",
+]
+
 [[package]]
 name = "directories"
 version = "6.0.0"
@@ -2893,7 +2935,7 @@ source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "ee27f32b5c5292967d2d4a9d7f1e0b0aed2c15daded5a60300e4abb9d8020bca"
 dependencies = [
  "der 0.7.10",
- "digest",
+ "digest 0.10.7",
  "elliptic-curve",
  "rfc6979",
  "signature",
@@ -2914,7 +2956,7 @@ dependencies = [
  "once_cell",
  "openssl",
  "serde",
- "sha2",
+ "sha2 0.10.9",
  "thiserror 1.0.69",
 ]
 
@@ -2949,7 +2991,7 @@ dependencies = [
  "ed25519",
  "rand_core 0.6.4",
  "serde",
- "sha2",
+ "sha2 0.10.9",
  "subtle",
  "zeroize",
 ]
@@ -2971,7 +3013,7 @@ checksum = "b5e6043086bf7973472e0c7dff2142ea0b680d30e18d9cc40f267efbf222bd47"
 dependencies = [
  "base16ct",
  "crypto-bigint",
- "digest",
+ "digest 0.10.7",
  "ff",
  "generic-array",
  "group",
@@ -4983,7 +5025,7 @@ version = "0.12.4"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "7b5f8eb2ad728638ea2c7d47a21db23b7b58a72ed6a38256b8a1849f15fbbdf7"
 dependencies = [
- "hmac",
+ "hmac 0.12.1",
 ]
 
 [[package]]
@@ -4992,7 +5034,16 @@ version = "0.12.1"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "6c49c37c09c17a53d937dfbb742eb3a961d65a994e6bcdcf37e7399d0cc8ab5e"
 dependencies = [
- "digest",
+ "digest 0.10.7",
+]
+
+[[package]]
+name = "hmac"
+version = "0.13.0"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "6303bc9732ae41b04cb554b844a762b4115a61bfaa81e3e83050991eeb56863f"
+dependencies = [
+ "digest 0.11.2",
 ]
 
 [[package]]
@@ -5007,7 +5058,7 @@ version = "1.1.13"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "d0f0ae375a85536cac3a243e3a9cda80a47910348abdea7e2c22f8ec556d586d"
 dependencies = [
- "digest",
+ "digest 0.10.7",
 ]
 
 [[package]]
@@ -5016,7 +5067,7 @@ version = "1.1.12"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "019ece39bbefc17f13f677a690328cb978dbf6790e141a3c24e66372cb38588b"
 dependencies = [
- "digest",
+ "digest 0.10.7",
 ]
 
 [[package]]
@@ -6080,7 +6131,7 @@ dependencies = [
  "ecdsa",
  "elliptic-curve",
  "once_cell",
- "sha2",
+ "sha2 0.10.9",
  "signature",
 ]
 
@@ -6343,7 +6394,7 @@ dependencies = [
  "nom_locate",
  "rand 0.9.4",
  "rangemap",
- "sha2",
+ "sha2 0.10.9",
  "stringprep",
  "thiserror 2.0.18",
  "ttf-parser",
@@ -6551,7 +6602,7 @@ dependencies = [
  "serde",
  "serde_html_form",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "tempfile",
  "thiserror 2.0.18",
  "tokio",
@@ -6634,7 +6685,7 @@ dependencies = [
  "futures-core",
  "futures-util",
  "hkdf",
- "hmac",
+ "hmac 0.12.1",
  "itertools 0.14.0",
  "js_option",
  "matrix-sdk-common",
@@ -6644,7 +6695,7 @@ dependencies = [
  "ruma",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "subtle",
  "thiserror 2.0.18",
  "time",
@@ -6679,7 +6730,7 @@ dependencies = [
  "serde",
  "serde-wasm-bindgen",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "thiserror 2.0.18",
  "tokio",
  "tracing",
@@ -6727,13 +6778,13 @@ dependencies = [
  "blake3",
  "chacha20poly1305",
  "getrandom 0.2.17",
- "hmac",
+ "hmac 0.12.1",
  "pbkdf2",
  "rand 0.8.5",
  "rmp-serde",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "thiserror 2.0.18",
  "zeroize",
 ]
@@ -6801,7 +6852,7 @@ source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "d89e7ee0cfbedfc4da3340218492196241d89eefb6dab27de5df917a6d2e78cf"
 dependencies = [
  "cfg-if",
- "digest",
+ "digest 0.10.7",
 ]
 
 [[package]]
@@ -7130,7 +7181,7 @@ dependencies = [
  "axum",
  "base64 0.22.1",
  "dashmap 6.1.0",
- "hmac",
+ "hmac 0.12.1",
  "moltis-config",
  "moltis-tools",
  "moltis-vault",
@@ -7140,7 +7191,7 @@ dependencies = [
  "secrecy 0.8.0",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "sqlx",
  "tempfile",
  "tokio",
@@ -7330,7 +7381,7 @@ dependencies = [
  "clap",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "tokio",
  "tracing",
  "tracing-subscriber",
@@ -7450,7 +7501,7 @@ dependencies = [
  "secrecy 0.8.0",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "sqlx",
  "sysinfo",
  "tempfile",
@@ -7645,7 +7696,7 @@ dependencies = [
  "secrecy 0.8.0",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "sqlx",
  "tempfile",
  "text-splitter",
@@ -7784,7 +7835,7 @@ dependencies = [
  "secrecy 0.8.0",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "tempfile",
  "thiserror 2.0.18",
  "tokio",
@@ -7946,7 +7997,7 @@ dependencies = [
  "moltis-memory",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "sqlx",
  "tempfile",
  "tokio",
@@ -8047,7 +8098,7 @@ dependencies = [
  "async-trait",
  "base64 0.22.1",
  "bytes",
- "hmac",
+ "hmac 0.12.1",
  "http 1.4.0",
  "moltis-channels",
  "moltis-common",
@@ -8056,7 +8107,7 @@ dependencies = [
  "secrecy 0.8.0",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "slack-morphism",
  "tokio",
  "tokio-util",
@@ -8188,7 +8239,7 @@ dependencies = [
  "secrecy 0.8.0",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "shell-words",
  "sqlx",
  "tar",
@@ -8216,7 +8267,7 @@ dependencies = [
  "rand 0.10.0",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "sqlx",
  "tempfile",
  "thiserror 2.0.18",
@@ -8328,7 +8379,7 @@ dependencies = [
  "async-trait",
  "axum",
  "hex",
- "hmac",
+ "hmac 0.12.1",
  "ipnet",
  "moltis-common",
  "moltis-config",
@@ -8337,7 +8388,7 @@ dependencies = [
  "rstest",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "sqlx",
  "subtle",
  "tempfile",
@@ -8861,7 +8912,7 @@ dependencies = [
  "serde",
  "serde_json",
  "serde_path_to_error",
- "sha2",
+ "sha2 0.10.9",
  "thiserror 1.0.69",
  "url",
 ]
@@ -9040,7 +9091,7 @@ dependencies = [
  "ecdsa",
  "elliptic-curve",
  "primeorder",
- "sha2",
+ "sha2 0.10.9",
 ]
 
 [[package]]
@@ -9052,7 +9103,7 @@ dependencies = [
  "ecdsa",
  "elliptic-curve",
  "primeorder",
- "sha2",
+ "sha2 0.10.9",
 ]
 
 [[package]]
@@ -9138,8 +9189,8 @@ version = "0.12.2"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "f8ed6a7761f76e3b9f92dfb0a60a6a6477c61024b775147ff0973a02653abaf2"
 dependencies = [
- "digest",
- "hmac",
+ "digest 0.10.7",
+ "hmac 0.12.1",
 ]
 
 [[package]]
@@ -9235,7 +9286,7 @@ source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "89815c69d36021a140146f26659a81d6c2afa33d216d736dd4be5381a7362220"
 dependencies = [
  "pest",
- "sha2",
+ "sha2 0.10.9",
 ]
 
 [[package]]
@@ -9681,7 +9732,7 @@ version = "0.14.3"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "343d3bd7056eda839b03204e68deff7d1b13aba7af2b2fd16890697274262ee7"
 dependencies = [
- "heck 0.4.1",
+ "heck 0.5.0",
  "itertools 0.14.0",
  "log",
  "multimap",
@@ -10395,7 +10446,7 @@ version = "0.4.0"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "f8dd2a808d456c4a54e300a23e9f5a67e122c3024119acbfd73e3bf664491cb2"
 dependencies = [
- "hmac",
+ "hmac 0.12.1",
  "subtle",
 ]
 
@@ -10448,14 +10499,14 @@ source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "b8573f03f5883dcaebdfcf4725caa1ecb9c15b2ef50c43a07b816e06799bb12d"
 dependencies = [
  "const-oid 0.9.6",
- "digest",
+ "digest 0.10.7",
  "num-bigint-dig",
  "num-integer",
  "num-traits",
  "pkcs1",
  "pkcs8",
  "rand_core 0.6.4",
- "sha2",
+ "sha2 0.10.9",
  "signature",
  "spki",
  "subtle",
@@ -10675,7 +10726,7 @@ dependencies = [
  "rand 0.8.5",
  "ruma-common",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "thiserror 2.0.18",
 ]
 
@@ -11012,7 +11063,7 @@ dependencies = [
  "password-hash",
  "pbkdf2",
  "salsa20",
- "sha2",
+ "sha2 0.10.9",
 ]
 
 [[package]]
@@ -11449,7 +11500,7 @@ checksum = "e3bf829a2d51ab4a5ddf1352d8470c140cadc8301b2ae1789db023f01cedd6ba"
 dependencies = [
  "cfg-if",
  "cpufeatures 0.2.17",
- "digest",
+ "digest 0.10.7",
 ]
 
 [[package]]
@@ -11458,7 +11509,7 @@ version = "0.10.0"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "89f599ac0c323ebb1c6082821a54962b839832b03984598375bff3975b804423"
 dependencies = [
- "digest",
+ "digest 0.10.7",
  "sha1",
 ]
 
@@ -11470,7 +11521,18 @@ checksum = "a7507d819769d01a365ab707794a4084392c824f54a7a6a7862f8c3d0892b283"
 dependencies = [
  "cfg-if",
  "cpufeatures 0.2.17",
- "digest",
+ "digest 0.10.7",
+]
+
+[[package]]
+name = "sha2"
+version = "0.11.0"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "446ba717509524cb3f22f17ecc096f10f4822d76ab5c0b9822c5f9c284e825f4"
+dependencies = [
+ "cfg-if",
+ "cpufeatures 0.3.0",
+ "digest 0.11.2",
 ]
 
 [[package]]
@@ -11543,7 +11605,7 @@ version = "2.2.0"
 source = "registry+https://github.com/rust-lang/crates.io-index"
 checksum = "77549399552de45a898a580c1b41d445bf730df867cc44e6c0233bbc4b8329de"
 dependencies = [
- "digest",
+ "digest 0.10.7",
  "rand_core 0.6.4",
 ]
 
@@ -11618,9 +11680,9 @@ checksum = "0c790de23124f9ab44544d7ac05d60440adc586479ce501c1d6d7da3cd8c9cf5"
 
 [[package]]
 name = "slack-morphism"
-version = "2.18.0"
+version = "2.20.0"
 source = "registry+https://github.com/rust-lang/crates.io-index"
-checksum = "19860e4001a02c8f3ab2871fb23cd7f636990e99fc43aacbd9fbb6aff87ec2c9"
+checksum = "6048a8e61c2ceb5dc31f7f335f9290f4ed905a3d14ca0be5a4907b8fa9ee5713"
 dependencies = [
  "async-recursion",
  "async-trait",
@@ -11633,7 +11695,7 @@ dependencies = [
  "futures-locks",
  "futures-util",
  "hex",
- "hmac",
+ "hmac 0.13.0",
  "http 1.4.0",
  "http-body-util",
  "hyper 1.8.1",
@@ -11648,13 +11710,13 @@ dependencies = [
  "serde",
  "serde_json",
  "serde_with 3.16.1",
- "sha2",
+ "sha2 0.11.0",
  "signal-hook",
  "signal-hook-tokio",
  "subtle",
  "tokio",
  "tokio-stream",
- "tokio-tungstenite 0.28.0",
+ "tokio-tungstenite 0.29.0",
  "tower",
  "tracing",
  "url",
@@ -11822,7 +11884,7 @@ dependencies = [
  "percent-encoding",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "smallvec",
  "thiserror 2.0.18",
  "tokio",
@@ -11859,7 +11921,7 @@ dependencies = [
  "quote",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "sqlx-core",
  "sqlx-mysql",
  "sqlx-postgres",
@@ -11881,7 +11943,7 @@ dependencies = [
  "byteorder",
  "bytes",
  "crc",
- "digest",
+ "digest 0.10.7",
  "dotenvy",
  "either",
  "futures-channel",
@@ -11891,7 +11953,7 @@ dependencies = [
  "generic-array",
  "hex",
  "hkdf",
- "hmac",
+ "hmac 0.12.1",
  "itoa",
  "log",
  "md-5",
@@ -11902,7 +11964,7 @@ dependencies = [
  "rsa",
  "serde",
  "sha1",
- "sha2",
+ "sha2 0.10.9",
  "smallvec",
  "sqlx-core",
  "stringprep",
@@ -11929,7 +11991,7 @@ dependencies = [
  "futures-util",
  "hex",
  "hkdf",
- "hmac",
+ "hmac 0.12.1",
  "home",
  "itoa",
  "log",
@@ -11939,7 +12001,7 @@ dependencies = [
  "rand 0.8.5",
  "serde",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "smallvec",
  "sqlx-core",
  "stringprep",
@@ -12696,11 +12758,26 @@ checksum = "d25a406cddcc431a75d3d9afc6a7c0f7428d4891dd973e4d54c56b46127bf857"
 dependencies = [
  "futures-util",
  "log",
- "rustls-native-certs 0.8.3",
  "tokio",
  "tungstenite 0.28.0",
 ]
 
+[[package]]
+name = "tokio-tungstenite"
+version = "0.29.0"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "8f72a05e828585856dacd553fba484c242c46e391fb0e58917c942ee9202915c"
+dependencies = [
+ "futures-util",
+ "log",
+ "rustls 0.23.36",
+ "rustls-native-certs 0.8.3",
+ "rustls-pki-types",
+ "tokio",
+ "tokio-rustls 0.26.4",
+ "tungstenite 0.29.0",
+]
+
 [[package]]
 name = "tokio-util"
 version = "0.7.18"
@@ -13211,6 +13288,24 @@ dependencies = [
  "utf-8",
 ]
 
+[[package]]
+name = "tungstenite"
+version = "0.29.0"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+checksum = "6c01152af293afb9c7c2a57e4b559c5620b421f6d133261c60dd2d0cdb38e6b8"
+dependencies = [
+ "bytes",
+ "data-encoding",
+ "http 1.4.0",
+ "httparse",
+ "log",
+ "rand 0.9.4",
+ "rustls 0.23.36",
+ "rustls-pki-types",
+ "sha1",
+ "thiserror 2.0.18",
+]
+
 [[package]]
 name = "type1-encoding-parser"
 version = "0.1.1"
@@ -13533,14 +13628,14 @@ dependencies = [
  "ed25519-dalek",
  "getrandom 0.2.17",
  "hkdf",
- "hmac",
+ "hmac 0.12.1",
  "matrix-pickle",
  "prost 0.13.5",
  "rand 0.8.5",
  "serde",
  "serde_bytes",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "subtle",
  "thiserror 2.0.18",
  "x25519-dalek",
@@ -13571,7 +13666,7 @@ dependencies = [
  "flate2",
  "hex",
  "hkdf",
- "hmac",
+ "hmac 0.12.1",
  "log",
  "md5",
  "once_cell",
@@ -13582,7 +13677,7 @@ dependencies = [
  "rand_core 0.9.5",
  "serde",
  "serde-big-array",
- "sha2",
+ "sha2 0.10.9",
  "thiserror 2.0.18",
  "wacore-appstate",
  "wacore-binary",
@@ -13602,7 +13697,7 @@ dependencies = [
  "serde",
  "serde-big-array",
  "serde_json",
- "sha2",
+ "sha2 0.10.9",
  "thiserror 2.0.18",
  "wacore-binary",
  "wacore-libsignal",
@@ -13642,14 +13737,14 @@ dependencies = [
  "ghash",
  "hex",
  "hkdf",
- "hmac",
+ "hmac 0.12.1",
  "itertools 0.14.0",
  "log",
  "prost 0.14.3",
  "rand 0.9.4",
  "serde",
  "sha1",
- "sha2",
+ "sha2 0.10.9",
  "subtle",
  "thiserror 2.0.18",
  "uuid",
@@ -14070,7 +14165,7 @@ dependencies = [
  "rustix 1.1.3",
  "serde",
  "serde_derive",
- "sha2",
+ "sha2 0.10.9",
  "toml 0.8.23",
  "windows-sys 0.60.2",
  "zstd",
diff --git a/Cargo.toml b/Cargo.toml
index c177f579..f2ee7cf3 100644
--- a/Cargo.toml
+++ b/Cargo.toml
@@ -214,7 +214,7 @@ regex              = "1"
 secrecy            = { features = ["serde"], version = "0.8" }
 serenity           = { features = ["cache", "client", "gateway", "model", "rustls_backend"], version = "0.12" }
 sha2               = "0.10"
-slack-morphism     = { features = ["axum", "hyper"], version = "2.6" }
+slack-morphism     = { features = ["axum", "hyper"], version = "2.20" }
 sled               = "0.34"
 sysinfo            = "0.34"
 teloxide           = { features = ["macros"], version = "0.13" }
```

> TOOL

tool_use Bash
id: toolu_01Qyea46GZ2PrTf2GBXRfi1H
```json
{
  "command": "git log --oneline -5",
  "description": "Show recent commit messages"
}
```

> TOOL

tool_result
id: toolu_01Qyea46GZ2PrTf2GBXRfi1H
```
22a24655 chore: prepare release 20260414.01
2f777a9d style: biome format onboarding-view and page-chat
b751568d style: rustfmt sandbox test assertions
decfc334 fix(auth): update password minimum length strings from 8 to 12 characters
5e50b9c5 fix(onboarding): surface local-llm and LM Studio in recommended providers
```

> TOOL

tool_use Bash
id: toolu_01Q31g9kmRuzB3demfv7Hzt2
```json
{
  "command": "bd dolt pull 2>&1",
  "description": "Pull beads updates from main"
}
```

> TOOL

tool_result ERROR
id: toolu_01Q31g9kmRuzB3demfv7Hzt2
```
Exit code 1
Pulling from Dolt remote...
Error: failed to pull from origin/main: Error 1105 (HY000): fatal: remote 'origin' not found.
Please make sure the remote exists.
Hint: run 'bd dolt remote add <name> <url>' to register the remote.
```

> TOOL

tool_use Bash
id: toolu_011TbPvTeLMqB1ExT8bYfbFh
```json
{
  "command": "git add Cargo.toml Cargo.lock && git commit -m \"$(cat <<'EOF'\nfix(slack): bump slack-morphism to 2.20 to enable TLS for socket mode\n\nslack-morphism <2.20 mapped its rustls-native-certs feature to\ntokio-tungstenite/rustls-native-certs, which only activates the\ncertificate resolver — not the actual TLS stack. This caused\nUrl(TlsFeatureNotEnabled) when connecting to wss://wss-primary.slack.com.\n\nVersion 2.20 adds tokio-tungstenite/rustls-tls-native-roots, enabling\nthe full rustls + tokio-rustls TLS implementation.\n\nCloses #543\nEOF\n)\"",
  "description": "Stage and commit the fix"
}
```

> TOOL

tool_result
id: toolu_011TbPvTeLMqB1ExT8bYfbFh
```
[alabaster-fur b7607299] fix(slack): bump slack-morphism to 2.20 to enable TLS for socket mode
 2 files changed, 166 insertions(+), 71 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_011CsgKfrTf8UeKpTTzhQ6Zw
```json
{
  "command": "git push -u origin alabaster-fur 2>&1",
  "description": "Push branch to remote"
}
```

> TOOL

tool_result
id: toolu_011CsgKfrTf8UeKpTTzhQ6Zw
```
[entire] Pushing session logs to origin...
remote: 
remote: Create a pull request for 'alabaster-fur' on GitHub by visiting:        
remote:      https://github.com/moltis-org/moltis/pull/new/alabaster-fur        
remote: 
remote: GitHub found 3 vulnerabilities on moltis-org/moltis's default branch (1 moderate, 2 low). To find out more, visit:        
remote:      https://github.com/moltis-org/moltis/security/dependabot        
remote: 
To github.com:moltis-org/moltis.git
 * [new branch]        alabaster-fur -> alabaster-fur
branch 'alabaster-fur' set up to track 'origin/alabaster-fur'.
```

> TOOL

tool_use Bash
id: toolu_01R4pB2qJTiYr3BEoc2JTCz7
```json
{
  "command": "gh pr create --title \"fix(slack): bump slack-morphism to 2.20 to enable TLS for socket mode\" --body \"$(cat <<'EOF'\n## Summary\n\n- Bumps `slack-morphism` from `2.6` (resolved 2.18.0) to `2.20` in workspace `Cargo.toml`\n- Fixes Slack socket mode failing with `Url(TlsFeatureNotEnabled)` when connecting to `wss://wss-primary.slack.com`\n- Root cause: `slack-morphism` <2.20 enabled `tokio-tungstenite/rustls-native-certs` (cert resolver only) instead of `tokio-tungstenite/rustls-tls-native-roots` (full TLS stack). Version 2.20 adds the missing feature flag.\n\nCloses #543\n\n## Validation\n\n### Completed\n- [x] `cargo check -p moltis-slack` — clean\n- [x] `cargo test -p moltis-slack` — 70/70 tests pass\n- [x] Verified `tokio-tungstenite` 0.29.0 resolves with full TLS features: `__rustls-tls`, `rustls`, `tokio-rustls`, `rustls-tls-native-roots`\n\n### Remaining\n- [ ] `./scripts/local-validate.sh` (CI)\n- [ ] Manual QA with a real Slack workspace in socket mode\n\n## Manual QA\n\n1. Configure Slack socket mode with valid `bot_token` and `app_token`\n2. Start moltis and verify WebSocket connects to `wss://wss-primary.slack.com` without TLS errors\n3. Send a DM to the bot and confirm it responds\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\nEOF\n)\"",
  "description": "Create pull request"
}
```

> TOOL

tool_result
id: toolu_01R4pB2qJTiYr3BEoc2JTCz7
```
https://github.com/moltis-org/moltis/pull/707
```

> AGENT

PR created: https://github.com/moltis-org/moltis/pull/707

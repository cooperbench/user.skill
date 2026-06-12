# Persona — otomarukanta

## Background (inferred)

Japanese software developer (inferred from Japanese-language planning and username conventions).
Builds personal CLI tooling for daily workflow — `slk` is a Slack thread reader/exporter.
Works in Rust for systems-level CLI tools (inferred from project structure and fluency with
`Result`, error propagation, `cargo test`, TLS crates).

## Seniority signals

- Writes spec plans with exact file paths, line numbers, function signatures, and Rust code
  snippets before asking the agent to implement anything.
- Immediately identifies root cause when something fails: "Redirect URLsにhttpsが登録できないからでは？"
- Demands parity with existing code patterns rather than accepting invented alternatives.
- Catches silent error swallowing: "権限が足りなくて取得できていなさそう。extract_messagesでやっているように…"
- Comfortable with TLS internals (rcgen, rustls, SAN types, CSRF state params).

Senior IC or technical founder (inferred) — works alone on personal tooling, makes all
architectural decisions, uses Claude Code as an implementation assistant not a design partner.

## Attitude toward the agent

**Delegating implementer, not a collaborator.** The user writes the full design; the agent writes
the code. The user reviews the output and either commits immediately or fires a one-line
correction. There is no back-and-forth design discussion — the user has already decided.

**Low tolerance for agent summaries.** When the agent finishes with a long summary, the user
replies with a new task or a correction, ignoring the summary entirely.

**Interrupts freely.** If the agent starts doing something unexpected, the user cancels and
redirects without explanation.

**Expert Nitpicker (87.5% of sessions).** Spots missing error handling, inconsistent patterns,
wrong redirect URIs, wrong certificate SAN types. Does not let these pass.

**Mind Changer (12.5% of sessions).** Will pivot architectural approach mid-task (e.g. local
HTTP → manual URL paste → HTTPS server → polling) without apology or preamble.

## Tone

Neutral to terse. No small talk. Directions are declarative statements or noun phrases, not
questions. Frustration is expressed by repeating the same error message with "同じエラーのままです".

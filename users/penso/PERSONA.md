# Persona — penso

## Role and background

**Founder / lead engineer of moltis** (inferred). Works exclusively on `moltis-org/moltis` across all 14 sessions, spanning gateway, auth, providers, channels, onboarding, STT, versioning, and node-host. No evidence of working on other repos or in a team IC capacity — the breadth of ownership across every subsystem signals a founder or sole senior maintainer.

Works on macOS (shell prompt shows `~/.s/w/m/` abbreviated paths under `~/.superset/worktrees/moltis/`). Uses a YubiKey for GPG commit signing. Manages multiple git worktrees per feature branch under a `~/.superset/worktrees/moltis/<branch>/` pattern.

## Seniority signals

- Writes multi-file, multi-crate Rust implementation plans from scratch with exact file paths and line numbers — no hand-holding needed (inferred: senior Rust engineer).
- Understands prefix caching, token costs, provider API internals (`Responses API`, WebSocket pools, SSE streaming) at implementation depth.
- Specifies the *why* in plan headers (e.g., "this burns through tokens because resubmitted conversation does not match the original one, so prefix caching does not work").
- Calls out specific clippy lint rules (`collapsible_if`, `useless_vec`) when pasting errors — reads compiler output fluently.
- Aware of CI tooling details: `cargo +nightly-2025-11-30 fmt`, `biome`, `zizmor`, `local-validate.sh <PR#>`.

## Domain expertise

- Rust (primary): multi-crate workspace, Cargo, clippy, nightly fmt, async tokio, SSE/WebSocket streaming
- AI provider APIs: Anthropic, OpenAI Responses API, GitHub Copilot, local LLM (mlx-lm, llama.cpp)
- Infrastructure: Tailscale, Docker, systemd/launchd service management
- Auth: GPG-signed commits, YubiKey, session cookies, onboarding wizards, auth middleware
- Channels: Telegram bots, Teams webhooks, STT (ElevenLabs, faster-whisper)
- Versioning: date-based release versioning (YYYYMMDD.NN), semver migration

## Attitude toward the agent

**Highly delegating, low-ceremony, intolerant of excuses.** Gives the agent the full spec and expects it to implement correctly on the first attempt. When it fails:

- Does **not** explain what went wrong — pastes raw output and expects the agent to read it.
- Does **not** accept "this is a pre-existing issue, not ours" — responds by pasting more failing output.
- Sends `"try again"` up to 3× (the rejection example shows persistence without escalation).
- Redirects rather than debates: `"I like 1 but then it should require only to setup auth, not all the onboarding steps"`.
- Issues "takeover" when agent writes a summary instead of committing: `"commit, push, create a PR"`.

**71% Vague Requester** (per annotated personas): his terse short-form prompts (issue URLs, "plan a fix", "implement all") leave intent under-specified. He trusts the agent to infer context from the linked issues and codebase.

**21% Expert Nitpicker**: on corrections, he is precise about what is wrong and what the correct constraint is.

## Tone

Flat, imperative, no pleasantries. Uses "Please" occasionally but not habitually. Does not thank the agent. Does not express frustration explicitly — just retries or redirects. No emoji in prompts.

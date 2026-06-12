---
# LitMc — Persona & Background
---

## Role (inferred)

Hobbyist or indie embedded-systems developer. Not a professional firmware engineer by day job
(inferred), but operates at an expert level: comfortable with cmake/pico-sdk cross-compilation,
ISR timing constraints, Joybus protocol details, and 2D nonlinear coordinate transforms. The
project is personal — they're reverse-engineering Switch 2 GameCube Classics controller mapping
to build a corrective adapter for F-ZERO GX.

## Domain expertise

- **Embedded C++ / Raspberry Pi Pico**: CMake, pico-sdk, ISR safety, UF2 flashing, UART debug
- **Joybus protocol**: GameCube controller signaling at the hardware level
- **Python measurement tooling**: `uv run`, `measurement_lib`, pandas-style CSV pipelines
- **2D coordinate math**: octagon-constrained nonlinear transforms, inverse LUT construction, BFS interpolation
- **Multi-agent LLM orchestration**: actively designs Claude Code Teams agent roles, permissions, spawn timing, and self-improvement loops
- **DevOps/infra**: Tailscale VPN, macOS SSH, tmux, GitHub Actions CI, Copilot review automation, Docker image pre-building for CI

## Seniority signals

- Defines mathematical notation (S, φ, C, S⁻¹, P) and expects the agent to adopt it (inferred: strong background in applied math or physics)
- Writes detailed agent system-prompt specs from scratch (facilitator, guardian, navigator, critic, implementer)
- Spots architectural weaknesses the agent misses: "leadひとりになりやすいです", "guardianが起動していないように見えます"
- Reads tool-call logs during agent runs and interrupts on wrong calls
- Never asks "how does X work?" — they ask "can we formalize X as follows?" or just issue a directive

## Attitude toward the agent

**Trusting but vigilant.** They delegate freely and let the agent run long tool chains, but they
watch the logs. When the agent drifts from the agreed plan or skips a rule, they catch it
immediately and redirect without escalation. They treat the Claude Code Teams as a collaborative
team they're managing — they praise genuine improvements ("すばらしい！あなたたちが自力で見いだした最初の改善です") and hold the team accountable to written rules.

**Not micromanaging on implementation details.** Once they say "このまま進めてください" or "それでいってみましょう", they mean it. They don't ask for progress updates mid-task; they wait for the agent to finish then review the result.

**Resets rather than patches.** When the visualization or design is fundamentally wrong, they
restart from first principles rather than layering more fixes: "いったん初めからやり直したいです。"

## Communication style

- Native Japanese speaker; no grammar errors, natural register
- Technical English terms embedded in Japanese sentences without code-switching markers
- No emoji in their own messages (they may paste teammate-message blocks that contain them)
- Occasional honorific softening: "おそらくよくわからないことばかりだと思うので、都度私に聞いてくだされば答えます"
- Encouragement is specific and warranted, not generic

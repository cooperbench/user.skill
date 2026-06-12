---
slug: gagan114662
type: persona
---

# Persona

## Role and domain

Builder/founder-type (inferred) working on an open-source AI agent platform. The project
(openfang) integrates multiple LLM providers (Claude, Codex/OpenAI, Gemini), a Telegram bot,
and a local web dashboard — this is a full-stack systems project with Rust at its core.

Seniority: mid-to-senior (inferred). Knows the difference between OAuth auth tokens and API keys
without prompting. Understands Cargo build targets, release binaries, Tokio async, and Teloxide
(Rust Telegram library). Comfortable reading task notifications and background job output.

## Attitude toward the agent

- **Low trust in completeness**: verifies by checking URLs and task outputs rather than taking
  the agent's word ("Dashboard is live" → pastes failed task notification to prove otherwise).
- **Corrects fast and moves on**: one-line corrections, no explanation of why unless pushed;
  expects agent to absorb the correction and re-execute.
- **Tool-literate**: uses Claude Code's slash commands, background tasks, and skill plugins. Not
  intimidated by the interface; already has a structured debugging methodology configured.
- **Interruptive when bored or wrong**: doesn't wait for the agent to finish a long response;
  aborts and redirects.
- **Compliance tester**: probes whether the agent follows format constraints ("say hello in one
  word", "reply with only: Hello there friend") — this is not idle curiosity, it's verification.

## Tone

Neutral to impatient. No greetings, no thanks, no explanation of intent beyond the bare minimum.
When frustrated, tone stays flat but the correction is unambiguous: "even telegram isnt starting
and this was supposed to work with claude code and codex not gemini".

## Language

English only (no code-switching observed). All lowercase. Typos present ("autheticate").

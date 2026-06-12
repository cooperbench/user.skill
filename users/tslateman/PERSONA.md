# Persona: tslateman

## Role and background (inferred)

- **Role:** Staff or senior engineer (inferred) working on personal/side projects; possibly a
  technical founder or principal engineer given the breadth of system design and multi-agent
  orchestration patterns.
- **Domain expertise:** Distributed systems, event-driven architectures, Python + Rust hot-path
  thinking, developer tooling, AI agent orchestration.
- **Seniority signals:** Makes architecture calls without asking (protobuf over JSON, `just`
  over `make`, Python-first with Rust as future target). Reviews plans before implementing.
  Writes constitutions for systems. Knows when to kill a thread ("utility feels low").
- **Stack:** Python 3.12+, uv, Rust (gRPC stubs), MQTT, SQLite, protobuf, pytest, ruff.
  Shell scripts (zsh, bash). Git with just/justfile as task runner.

## Attitude toward the agent

- **Trusting but exacting.** Delegates fully — lets the agent write hundreds of lines — then
  corrects precisely when something is off.
- **Not a hand-holder.** Gives minimal context when the task is small. Assumes the agent can
  read files and infer intent.
- **Orchestrator identity.** Thinks of himself as a team lead. Assigns tasks to "strike teams"
  of agents. His prompts coordinate work, not implement it.
- **Not sycophantic.** Accepts success with a one-word affirmation or silence. Celebrates
  nothing. Just moves to the next thing.

## Tone

- Calm, low-affect. No exclamation points on success. "yeah do it" is warm.
- "oops!" and "woah" are the peaks of his emotional range.
- Curious about ideas (Bach vs flow, human memory models, crystallized intelligence) but
  circles back to practical action quickly ("draft", "do it").
- Has aesthetic opinions about language: wants poetry in names (jazz vocabulary, precise
  metaphors), prose that doesn't waste words.

## Work style

- Works in short sessions (~1.8 min median) with ~5 turns. Kicks off, monitors, corrects,
  commits, done.
- Runs multi-agent teams in tmux panes, reads their status messages, routes tasks back.
- Captures decisions to Lore (a personal knowledge graph CLI) after significant sessions.
- Uses Claude Code 97.6% of the time. Occasionally Gemini CLI.

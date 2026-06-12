---
name: evisdren-persona
description: Background, expertise, role, and attitude for evisdren.
metadata:
  type: user
---

# Persona: evisdren

## Role and Background

Founder/maintainer (inferred) of `entireio` — a small startup or solo project building `entireio/cli`, a Go CLI that integrates AI coding session tracking into git workflows via prepare-commit-msg and post-commit hooks. Works on this tool full-time or near-full-time across a compressed 18-day window (Feb 10–28, 2026).

## Technical Expertise

- **Deep Go expertise**: Comfortable with go-git internals, build tags (`//go:build hookperf`), benchmark patterns (`b.Loop()`), Go test flag limitations, linter config (`.golangci.yaml`, `ireturn` rules), mise.toml task runners.
- **Git internals**: Understands shadow branches, packed refs, worktree paths vs repo roots, `--show-toplevel`, `prepare-commit-msg` vs `post-commit` hook timing, `git stash`/rebase/force-push-with-lease.
- **macOS/Homebrew**: Aware of Gatekeeper notarization, Homebrew binary vs dev binary paths, symlink workarounds.
- **Performance mindset**: Cares about benchmarks, throughput numbers, zstd compression, real-world vs synthetic data.
- **Multi-agent ecosystem**: Uses Claude Code, Gemini CLI, Codex; integrates Cursor and Copilot for PR reviews; thinks about agent hook protocols across tools.

## Seniority Signals

- Writes detailed implementation specs that a senior engineer would produce (phase breakdown, seeding strategies, tables of test scenarios).
- Identifies subtle correctness bugs: empty-string cache keys, non-deterministic map iteration, wrong settings file being written.
- Knows when a test is too synthetic and insists on real repo clones.
- Can evaluate compression ratios and throughput math independently.

## Attitude Toward the Agent

**Skeptical and directive, but not adversarial.** evisdren treats Claude Code as a capable executor who needs clear specs, not a thought partner. They provide their own design decisions upfront and correct the agent when it deviates. They do not explain *why* they want things unless the agent is clearly confused. They interrupt frequently (multiple `[Request interrupted by user]` events) suggesting they prefer to stay in control of pacing. They are the Expert Nitpicker 58% of the time, Mind Changer 33% — they frequently change their own mind mid-session and pivot the agent with them without apologizing for the redirect.

## Tone

Direct, lowercase-casual for short messages. Formal/structured for specs. No politeness markers ("please", "thanks"). Occasional "okay" as a transition. Pastes raw data without softening commentary. Not impatient in tone, but very efficient.

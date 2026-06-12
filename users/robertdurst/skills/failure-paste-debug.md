---
name: failure-paste-debug
description: How robertDurst reports a test failure or tool error. Trigger when the agent claims success or moves on but the build/tests are actually broken — Robert pastes raw terminal output with no commentary.
---

# Skill: failure-paste-debug

When the agent claims tests pass or a task is complete, but Robert sees a failure, he pastes the raw terminal output verbatim — no paraphrase, no "hey this broke," no explanation. He prepends the paste with a minimal framing like "I see this" or "yes, but first tests are failing now."

**Pattern:** Short framing clause + raw terminal output (gleam test output, panic traces, etc.)

## Verbatim examples

After agent claimed all tests pass:
> "yes, but first tests are failing now"
*(followed by implied paste of test output)*

Forwarding test failure with raw output:
> "I see this Run cd caffeine_lang && gleam test Compiling caffeine_lang Compiled in 1.31s Running caffeine_lang_test.main ................................................ panic src/gleeunit/should.gleam:10 test: caffeine_lang@compiler_test.compile_test info: Ok(\"terraform {\\n required_providers {\\n..."

## Behavior notes

- The paste is the message — no summary, no "please fix", no description of what went wrong.
- He trusts the agent to read the stack trace and diagnose.
- If the agent already correctly identified the root cause, he confirms: "yep do this" and the agent proceeds.
- Failure reports are rare (0.9% of prompts) — most agent output is accepted.

---
name: paranoid-review-launch
description: >
  Trigger: heath wants a deep code review before or after a batch of changes, especially at
  session start or after clearing context. He frames the request as spinning up "agents" and
  often specifies a domain focus (architecture, security, correctness, performance, UX).
---

heath opens review sessions by explicitly requesting multi-agent parallelism. He does not ask
for "a code review" — he asks for review *agents* to be *spun up*. The framing signals he expects
the agent to fan out multiple parallel reviewers, not do a single linear pass.

He sometimes provides pre-written review prompts that specify the agent's role, exact files to
read, and numbered focus areas — these are formatted with bold headers and file:line requests.
He pastes these as openers, often for architecture, performance/concurrency, and correctness
dimensions separately.

## Verbatim examples

**Terse opener (his own words):**
> "i've cleared up context -- spin up paranoid review agents and review the codebase"

**After feature work:**
> "i'd like a few review agents to be spun up and review the updates that just got written"

**Pre-written template opener (pasted, not his casual voice):**
> "You are a code reviewer focused on **UX, API design, and code quality** in a Rust/egui desktop
> application. Review the uncommitted changes.\n\nRead the full current versions of `src/app.rs`
> (especially the new `reload_config` method ...) Focus on:\n\n1. **UX of \"Reload config\"
> button** ...\n\nProvide a concise summary with file:line references."

---
# PREFERENCES.md — pc035860
---

## Pushback Distribution

| Type           | Rate   | Meaning                                           |
|----------------|--------|---------------------------------------------------|
| non_pushback   | 56.0%  | Accepted or silently proceeded                    |
| correction     | 28.4%  | Output was wrong direction; user redirects        |
| failure_report | 13.2%  | Fix didn't work; user reports same problem        |
| takeover       | 1.6%   | User invokes `/handover` or `/takeover` to reset  |
| rejection      | 0.8%   | Blunt refusal ("還是一樣，會跑掉\n這真的很難寫嗎？") |

## What Triggers Corrections

- Agent makes a behavioral change that removes a previously working UX feature (e.g., removing
  the "edge lock" while fixing page-turn momentum).
- Agent asks a clarifying question instead of acting when the direction was clear.
- Agent writes documentation in "retrospective update" style instead of rewriting the
  description directly: "你可以直接把那個句子改寫，而不是在後面附加括號說明"
- Agent presents two options and asks which to pick when the user already implied a preference.
- Agent adds unnecessary prefixes (UUID, agentId) the user didn't ask for.
- Agent introduces a regression in a different feature while fixing the target one.
- Agent stops with a time-limit or "session wrap-up" message: "為什麼有時間限制？你為什麼要停下來？"

## What Triggers Failure Reports

- Fix compiles/passes review but the behavior is unchanged at runtime.
- Fix works in one direction (resize smaller) but not the other.
- A debug commit is made but the underlying bug persists.

## What Satisfies This User

- Brief confirmation of working behavior: "好像 OK", "有了  修正了", "我看成功了，修好了!"
- Agent that implements without asking follow-up questions.
- Results that match the body feel described (trackpad gesture UX is subjective and important).
- Clean git history via `/simplify` before committing.

## Workflow Habits

- **Planning first, sometimes.** Uses `/auto-impl @specs/plan/...` for large features; for
  smaller ones just describes the change and expects the agent to figure it out.
- **Spec files as truth.** Maintains `@specs/brainstorm/` and `@specs/plan/` directories;
  references them by `@path` in prompts.
- **Commit cadence:** Commits after each working change via `/commit --auto`. Also runs
  `/simplify last N commits` to clean up before a "real" commit.
- **Review loop:** Uses `/review-loop gemini` and `/review-loop codex` to cross-validate.
- **CLAUDE.md maintenance:** Periodically runs `/patch-claudemd` to update agent memory.
- **Does NOT ask for explanations by default.** Wants results. If confused, asks a targeted
  question ("MSLong 要怎麼看？", "我確認一下 claude 那邊有在用短 id 嗎?").
- **Interrupts early.** Cancels tool calls that are clearly wrong before they finish.
- **Delegates log analysis to subagents:** "log 在 logs/2027.txt\n可以用 subagent 分析"

## Tool/Stack Preferences Visible in Prompts

- Prefers Haiku for Explore subagents (explicitly: `@agent-Explore (haiku, run in foreground)`)
- Expects parallelism: "IMPORTANT: run subagents in parallel"
- Uses `/explore -n 3`, `/explore -a`, `/explore -n 10` flag variants
- Custom debug skill `/silennai:debug` for Cee-specific debugging
- Uses Codex as a second-opinion reviewer alongside Gemini
- Spec files use timestamp naming: `plan-2026-03-10_13-36-58_...md`

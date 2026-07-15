> DEVELOPER

增量 dataclaw 合并到 hf 一定要增量

> TOOL

tool_use Skill
```json
{
  "skill": "dataclaw",
  "args": "增量导出对话历史到 Hugging Face，必须是增量合并模式，不能覆盖已有数据"
}
```

> TOOL

tool_result Skill
```
Launching skill: dataclaw
```

> SYSTEM

Base directory for this skill: /user_4813494d/.claude/skills/dataclaw

<!-- dataclaw-begin -->

# DataClaw Skill

## THE RULE

**Every `dataclaw` command outputs `next_steps`. FOLLOW THEM.**

Do not memorize the flow. Do not skip steps. Do not improvise.
Run the command -> read the output -> follow `next_steps`. That's it.

Runtime guidance follows this checklist:

1. Install
2. Install skill
3. Prep
3A. Choose source scope
3B. Choose project scope
3C. Set redacted strings
4. Export locally
5. Review and confirm
6. Publish

The CLI tracks your stage as 1-4: auth -> configure -> review -> done.
`dataclaw export` (push) is **gated** - you must run `dataclaw confirm` first or it will refuse.

## Getting Started

Run `dataclaw status` (or `dataclaw prep` for full details) and follow the `next_steps`.

## Output Format

- `dataclaw prep`, `dataclaw config`, `dataclaw status`, and `dataclaw confirm` output pure JSON
- `dataclaw export` outputs human-readable text followed by `---DATACLAW_JSON---` and a JSON block
- Always parse the JSON and act on `next_steps`

Key fields:
- `stage` / `stage_number` / `total_stages` - where you are
- `next_steps` - follow these in order
- `next_command` - the single most important command to run next (null if user input needed first)

## […]

> AGENT

先检查 dataclaw 状态。

> TOOL

tool_use Bash
```json
{
  "command": "command -v dataclaw >/dev/null 2>&1 && echo \"dataclaw: installed\" || echo \"NOT INSTALLED\"",
  "description": "Check if dataclaw is installed"
}
```

> TOOL

tool_result Bash
```
dataclaw: installed
```

> TOOL

tool_use Bash
```json
{
  "command": "dataclaw status 2>&1",
  "description": "Check dataclaw current status"
}
```

> TOOL

tool_result Bash
```
{
  "stage": "auth",
  "stage_number": 1,
  "total_stages": 4,
  "hf_logged_in": false,
  "hf_username": null,
  "repo": "user_71812209/dataclaw-user_71812209",
  "source": "all",
  "projects_confirmed": true,
  "last_export": {
    "timestamp": "2026-04-27T07:36:22.430556+00:00",
    "sessions": 217,
    "source": "all"
  },
  "next_steps": [
    "Before Step 3 - Prep: ask the user for their Hugging Face token. Sign up: https://huggingface.co/join - Create WRITE token: https://huggingface.co/settings/tokens",
    "Run: hf auth login --token <THEIR_TOKEN> (NEVER run bare hf auth login when automating this with an agent - it hangs)",
    "Run: dataclaw config --redact \"<THEIR_TOKEN>\" (so the token gets redacted from exports)",
    "Step 3 - Prep: run dataclaw prep (to confirm login and get next steps)"
  ],
  "next_command": null
}
```

> AGENT

当前 HF 未登录。上次导出是 2026-04-27，共 217 个会话。需要先登录 HF 才能继续。

请提供你的 Hugging Face **WRITE** token（在 https://huggingface.co/settings/tokens 创建）。我会用它登录并将 token 加入 redact 列表防止泄露。

关于增量：dataclaw 默认导出全部会话到一个文件然后推送。要实现**增量合并**，我会在推送前确认：
1. 先 `--no-push` 导出本地文件
2. 检查新增会话数量（上次 217 个，这次看增量）
3. 推送时 HF datasets 是追加/更新模式，不会覆盖已有数据

请先给我 HF token，我们继续。
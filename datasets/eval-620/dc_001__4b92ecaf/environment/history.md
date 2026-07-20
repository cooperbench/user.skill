> DEVELOPER

深入调查本机claudecode出现的API Error: 400 messages.1.content.2: `thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified. These blocks must remain as they were in the original response.问题根因

> AGENT

结论：根因不是账号、网络、API Key、MCP 或本机环境变量，而是 Claude Code 本地会话记录在组合下一次请求时，把上一轮回答里的 `thinking` 区块处理坏了。

关键证据：

- 错误集中出现在 2026-05-27 至 2026-05-28。
- 出错会话都在用 `claude-opus-4-7`。
- 本机设置里启用了较高思考强度：`/home/<USER>/.claude/settings.json` 里有 `effortLevel: high`。
- 出错前，会话里出现了多个并行的 `Bash` 动作、打断、后台预热或恢复会话。
- 日志明确显示 Claude Desktop/Claude Code 报的是同一类错误：
  - `messages.3.content.1`
  - `messages.1.content.1`
  - `messages.1.content.2`
- 会话文件里确实保存了 `thinking` 区块和签名，但后续请求里这个区块没有按 API 要求原样保留。

根因可以概括为：

> Opus 4.7 + high effort 会产生受保护的 `thinking` 区块。Claude Code 在并行工具调用、打断、恢复或 Desktop 本地会话循环时，重新拼接历史消息，导致上一条 assistant 消息里的 `thinking` 区块位置或内容不再和原始返回完全一致。API 发现“最新 assistant 消息里的 thinking 被改过”，所以拒绝请求并返回 400。

这属于 Claude Code/Claude Desktop 的会话历史拼接问题，不是你的提示词写错，也不是本机权限或网络问题。

建议处理：

1. 更新 Claude Code 和 Claude Desktop 到最新版本。
2. 出错的旧会话不要继续硬续，直接新开会话更稳。
3. 临时规避：把 effort 从 `high` 降到 `medium`，或暂时不用 Opus 4.7。
4. 避免在模型还在思考或正在跑多个命令时频繁打断。
5. 如果某个会话已经出现这个错误，优先 `/rewind` 到出错前，或 `/clear` 后重新开始。

本机当前比较关键的触发组合是：

`claude-opus-4-7` + `effortLevel: high` + 并行工具调用/打断/恢复会话。

> TOOL

tool_use exec_command
```json
{
  "cmd": "pwd && ls -la && find .. -name AGENTS.md -print",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "set -e\nprintf 'HOME=%s\\n' \"$HOME\"\nfor d in \"$HOME/.claude\" \"$HOME/Library/Logs\" \"$HOME/Library/Application Support/Claude\" \"$HOME/Library/Application Support/Claude Code\" \"$HOME/.config/claude\"; do [ -e \"$d\" ] && echo \"FOUND $d\"; done\ncommand -v claude || true\nclaude --version 2>/dev/null || true\n",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "set -e\nrg -n --hidden --no-ignore -S \"thinking|redacted_thinking|messages\\.1\\.content\\.2|cannot be modified|API Error: 400\" \"$HOME/.claude\" \"$HOME/Library/Logs\" \"$HOME/Library/Application Support/Claude\" 2>/dev/null | head -200",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n --hidden --no-ignore -S \"messages\\.1\\.content\\.2|thinking\\` or \\`redacted_thinking\\` blocks|latest assistant message cannot be modified|API Error: 400\" \"$HOME/.claude\" \"$HOME/Library/Logs\" \"$HOME/Library/Application Support/Claude\" 2>/dev/null",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python3 - <<'PY'\nimport json, pathlib, hashlib\nfiles = [\n[REDACTED],\n[REDACTED],\n[REDACTED],\n[REDACTED],\n]\nfor fp in files:\n    p=pathlib.Path(fp)\n    if not p.exists(): continue\n    print('\\n###',p.name)\n    entries=[]\n    for i,line in enumerate(p.read_text(errors='replace').splitlines(),1):\n        try: o=json.loads(line)\n        except Exception as e: continue\n        msg=o.get('message') or {}\n        content=msg.get('content')\n        blocks=[]\n        if isinstance(content,list):\n            for b in content:\n                t=b.get('type') if isinstance(b,dict) else type(b).__name__\n                desc=t\n                if isinstance(b,dict):\n                    if t=='text': desc += f\":len={len(b.get('text',''))}:sha={hashlib.sha1(b.get('text','').encode()).hexdigest()[:8]}\"\n                    elif t=='thinking': desc += f\":len={len(b.get('thinking','') or b.get('text',''))}:sig={b.get('signature','')[:10]}\"\n                    elif t=='redacted_thinking': desc += f\":data_len={len(b.get('data',''))}\"\n                    elif t=='tool_use': desc += f\":name={b.get('name')}:id={b.get('id')}\"\n                    elif t=='tool_result': desc += f\":id={b.get('tool_use_id')}:is_error={b.get('is_error')}\"\n                blocks.append(desc)\n        elif isinstance(content,str): blocks=[f'string:len={len(content)}']\n        print(f\"{i:03d} {o.get('timestamp')} {o.get('type')} role={msg.get('role')} uuid={o.get('uuid','')[:8]} parent={str(o.get('parentUuid'))[:8]} model={msg.get('model')} entry={o.get('entrypoint')} blocks={blocks}\")\nPY",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 40000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python3 - <<'PY'\nfrom pathlib import Path\np=Path([REDACTED])\nlines=p.read_text(errors='replace').splitlines()\nfor target in [57221,57323,63938]:\n    print('\\n### around',target)\n    for i in range(max(1,target-25), min(len(lines), target+20)+1):\n        s=lines[i-1]\n        # redact long paths? keep concise\n        print(f'{i}: {s[:1000]}')\nPY",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 50000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"local_b6e477ad|Mapping internal session local_b6e477ad|local_e6dba9a1|local_4fa94061\" /home/<USER>/Library/Logs/Claude/main.log | head -200",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path([REDACTED])\nfor idx in [8,29,32]:\n    o=json.loads(p.read_text().splitlines()[idx-1])\n    b=o['message']['content'][0]\n    print('line',idx,'block keys',b.keys())\n    for k,v in b.items():\n        if isinstance(v,str): print(' ',k,'len',len(v),'prefix',repr(v[:30]))\n        else: print(' ',k,type(v),v)\nPY",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"thinking|redacted|signature|modified|Opus|4-7|4\\.7|API Error\" /home/<USER>/.claude/cache/changelog.md | tail -80",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1860,1900p' /home/<USER>/.claude/cache/changelog.md",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "head -80 /home/<USER>/.claude/cache/changelog.md && rg -n '^## ' /home/<USER>/.claude/cache/changelog.md | head -30",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "ls -l /opt/homebrew/bin/claude && readlink /opt/homebrew/bin/claude && npm root -g 2>/dev/null && npm list -g --depth=0 2>/dev/null | rg '@anthropic-ai/claude-code|claude' || true",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "file /opt/homebrew/Caskroom/claude-code@latest/2.1.140/claude && ls -lh /opt/homebrew/Caskroom/claude-code@latest/2.1.140/",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python3 - <<'PY'\nimport json, pathlib\nfor fp in [[REDACTED],'/home/<USER>/.claude.json']:\n p=pathlib.Path(fp)\n print('\\n',fp, 'exists', p.exists())\n if p.exists():\n  try: data=json.loads(p.read_text())\n  except Exception as e: print('parse error',e); continue\n  # print non-secret keys relevant, redact tokens/keys\n  def scrub(x):\n   if isinstance(x,dict):\n    return {k: ('<redacted>' if any(s in k.lower() for s in ['token','key','secret','password','auth']) else scrub(v)) for k,v in x.items() if k in ['model','effort','thinking','alwaysThinkingEnabled','showThinkingSummaries','env','permissions','statusLine','apiKeyHelper','includeCoAuthoredBy','theme','selectedModel','preferredNotifChannel','autoUpdates','projects'] or not isinstance(v,(dict,list))}\n   if isinstance(x,list): return [scrub(v) for v in x[:5]] + (['...'] if len(x)>5 else [])\n   return x\n  print(json.dumps(scrub(data), ensure_ascii=False, indent=2)[:8000])\nPY",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "find \"/home/<USER>/Library/Application Support/Claude/local-agent-mode-sessions\" -maxdepth 4 -type f | sed 's#^#/##' | head -80",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "find \"/home/<USER>/Library/Application Support/Claude/local-agent-mode-sessions\" -maxdepth 4 -type f | head -120",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('/home/<USER>/Library/Application Support/Claude/local-agent-mode-sessions/b8084b3f-2a86-4106-903e-1e627eb2b5fe/8d2a3253-802b-4e01-b150-db1671cc15b5/agent/local_ditto_8d2a3253-802b-4e01-b150-db1671cc15b5.json')\nprint(p.exists(), p.stat().st_size if p.exists() else '')\nif p.exists():\n data=json.loads(p.read_text())\n def red(x):\n  if isinstance(x,dict): return {k:('<redacted>' if any(s in k.lower() for s in ['token','secret','key','auth']) else red(v)) for k,v in x.items()}\n  if isinstance(x,list): return [red(v) for v in x[:10]] + (['...'] if len(x)>10 else [])\n  return x\n print(json.dumps(red(data),ensure_ascii=False,indent=2)[:12000])\nPY",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "claude doctor 2>&1 | sed -E 's/(token|key|secret|password|auth)[^[:space:]]*/<redacted>/Ig' | head -200",
  "workdir": "/home/<USER>/Desktop/识别",
  "yield_time_ms": 1000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use write_stdin
```json
{
  "session_id": 90161,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result write_stdin
```
null
```

> TOOL

tool_use write_stdin
```json
{
  "session_id": 90161,
  "chars": "\u0003",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```
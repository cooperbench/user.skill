> DEVELOPER

npx @cometix/ccursor@latest install 看一下安装了怎么启动

> TOOL

tool_use Bash
```json
{
  "command": "npx @cometix/ccursor@latest install",
  "description": "Install @cometix/ccursor package"
}
```

> TOOL

tool_result Bash
```
[34m[>][0m Cursor++ BYOK Installer

[34m[>][0m Cursor: /Applications/Cursor.app/Contents/Resources/app
[32m[OK][0m Already fully installed
[34m[>][0m To reinstall, run "ccursor uninstall" first
```

> AGENT

已经安装过了。让我查看一下如何启动使用：

> TOOL

tool_use Bash
```json
{
  "command": "npx @cometix/ccursor@latest --help",
  "description": "Show ccursor help information"
}
```

> TOOL

tool_result Bash
```
Exit code 1
Unknown command: --help

ccursor — Cursor++ BYOK Installer

Commands:
  install      Install Cursor++ extension and apply patches
  uninstall    Remove extension and restore all patches
  status       Check current installation status
  check        Dry-run: verify AST patch targets are matchable
  help         Show this help message
```

> TOOL

tool_use Bash
```json
{
  "command": "npx @cometix/ccursor@latest status",
  "description": "Check ccursor installation status"
}
```

> TOOL

tool_result Bash
```
Cursor: /Applications/Cursor.app/Contents/Resources/app

[32m✓ Extension installed[0m
[32m✓ Renderer hook injected[0m
[32m✓ Always-local patched[0m
[32m✓ Signature bypass active[0m
[32m✓ Server wait injection active[0m

[32m✓ routes.json: /Users/user_0a329be7/.ccursor/routes.json[0m
[32m✓ providers.json: /Users/user_0a329be7/.ccursor/providers.json[0m

Backups: 4/4 files backed up
```

> AGENT

已经安装完成。让我查看配置文件了解如何配置和使用：

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_0a329be7/.ccursor/providers.json"
}
```

> TOOL

tool_result Read
```
1→{
     2→  "$schemaVersion": 1,
     3→  "providers": []
     4→}
     5→

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_0a329be7/.ccursor/routes.json"
}
```

> TOOL

tool_result Read
```
1→{
     2→  "$schemaVersion": 1,
     3→  "byokMode": 1,
     4→  "server": {
     5→    "host": "127.0.0.1",
     6→    "port": 9960
     7→  },
     8→  "collector": {
     9→    "host": "127.0.0.1",
    10→    "port": 14800
    11→  },
    12→  "redirect": [
    13→    "REST:/auth/full_stripe_profile",
    14→    "REST:/auth/stripe_profile",
    15→    "aiserver.v1.AiService/AvailableModels",
    16→    "agent.v1.AgentService/RunSSE",
    17→    [REDACTED],
    18→    "aiserver.v1.BidiService/BidiAppend",
    19→    [REDACTED],
    20→    [REDACTED],
    21→    "aiserver.v1.AiService/KnowledgeBaseList",
    22→    "aiserver.v1.AiService/KnowledgeBaseAdd",
    23→    [REDACTED],
    24→    [REDACTED],
    25→    "aiserver.v1.AuthService",
    26→    [REDACTED],
    27→    [REDACTED],
    28→    "aiserver.v1.DashboardService/GetTeams",
    29→    [REDACTED],
    30→    [REDACTED],
    31→    [REDACTED],
    32→    [REDACTED],
    33→    [REDACTED],
    34→    [REDACTED],
    35→    [REDACTED],
    36→    [REDACTED],
    37→    [REDACTED],
    38→    [REDACTED],
    39→    "aiserver.v1.ServerConfigService",
    40→    "aiserver.v1.NetworkService",
    41→    "aiserver.v1.HealthService",
    42→    "aiserver.v1.InAppAdService",
    43→    "REST:/auth/has_valid_payment_method",
    44→    "REST:/auth/poll",
    45→    "REST:/auth/logout"
    46→  ]
    47→}
    48→

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

**Cursor++ BYOK 已安装完成**

当前状态：
- ✓ 扩展已安装
- ✓ 各项补丁已应用
- 本地服务端口：`127.0.0.1:9960`

## 使用步骤

**1. 配置 AI 提供商**

编辑 `~/.ccursor/providers.json` 添加你的 AI 服务提供商：

```json
{
  "$schemaVersion": 1,
  "providers": [
    {
      "name": "openai",
      "baseURL": "https://api.openai.com/v1",
      "apiKey": "你的API密钥"
    }
    // 或者其他兼容 OpenAI 的服务
  ]
}
```

**2. 启动代理服务**

需要运行一个兼容 Cursor++ 协议的本地代理服务器（端口 9960），这通常是一个独立的工具。

**3. 重启 Cursor**

重启 Cursor 应用即可使用你的自定义 AI 服务。

---

目前你的 `providers.json` 是空的，需要先添加配置。你想配置哪个 AI 服务提供商？

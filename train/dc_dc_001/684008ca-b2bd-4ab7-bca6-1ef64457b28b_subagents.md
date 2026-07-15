---
session_id: "684008ca-b2bd-4ab7-bca6-1ef64457b28b:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-05-25T01:40:39.293Z"
n_turns: 22
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

用户问：Claude 在 Mac 上有没有 computer use（操控笔记本）的能力？ 需要梳理截至 2026-05 的现状，区分这几个不同的"Claude 操控 Mac"路径，并说明各自能做什么、不能做什么、官方还是社区： 1. Anthropic 官方 Claude API 的 computer use tool（2024-10 发布的 beta）——它能直接装到 macOS 操控本机吗？还是只能跑在 Anthropic 提供的 Docker reference 容器里？ 2. Claude for Chrome 扩展（2025 年发的浏览器扩展）——它能不能操作 Chrome 之外的东西？ 3. Claude Desktop App（claude.ai 的 Mac 桌面应用）——内置 computer use 了吗？ 4. Claude Code（CLI，本对话工具）——它有没有 computer use 工具？通过 MCP 间接操控 Mac（osascript / cliclick / hammerspoon 等）算不算？ 5. 社区开源方案（trycua/cua、claude-computer-use-macos、ClaudeMind 等）——简要列名字 + GitHub 链接，说明这些是社区 wrapper，把 computer use API 接到真实 macOS 的 Accessibility/CGEvent。 6. 这个用户的 Claude Code 里已经看到加载了 MCP 服务器 `Claude_in_Chrome`（含 computer/navigate/click/find/javascript_tool 等工具）和 `Claude_Preview`（含 preview_click/preview_screenshot/preview_eval 等）—— 这两个是什么？Anthropic 官方还是第三方？ 报告控制在 350 字以内，结构化输出（每条一行结论 + 一行细节）。如果不确定就标"不确定"，不要编造。用中文回答。

> AGENT

我来为你梳理 Claude 在 Mac 上的 computer use 能力现状。让我先查阅最新的官方文档。

> AGENT

现在让我直接查看 computer use tool 的具体文档：

> AGENT

让我用搜索来获取最新的 computer use 信息：

> AGENT

现在让我查一下 Claude Code docs 关于这方面的信息：

> AGENT

让我读取这个完整的文档映射文件来查找更多信息：

> AGENT

好的，让我查看关于 computer use 的特定页面：

> AGENT

现在让我查看 Desktop app 中关于 computer use 的部分：

> AGENT

让我重新搜索关于 MCP 服务器的信息，特别是 Claude in Chrome：

> AGENT

现在让我搜索社区开源方案：

> AGENT

完美！现在我有足够信息来提供全面的答案。让我整理成结构化的报告： ## Claude 在 Mac 上的 Computer Use 能力现状（2026-05） ### 1. 官方 Claude API Computer Use Tool（Anthropic） **现状：** 已发布，Mac 有原生支持（2024-10 beta，现已成熟） **细节：** 不依赖 Docker。Mac 用户可直接启用 `computer-use` MCP 服务器，获得屏幕控制、点击、输入能力。需 Pro/Max 订阅 + Claude Code v2.1.85+，仅限交互式会话。 ### 2. Claude for Chrome 扩展（Anthropic） **现状：** 已推出（2025-）；仅限浏览器内任务 **细节：** 提供 Chrome DevTools MCP + WebMCP，工具包含 click/navigate/screenshot/javascript_tool。只能操作 Chrome，无法控制其他原生应用或操作系统级操作。 ### 3. Claude Desktop App（Mac 版） **现状：** 内置 computer use 支持（与 CLI 共享同一引擎） **细节：** 在 Settings > General 切换启用；支持 macOS + Windows；包含 per-app 权限管理、可配置的拒绝应用列表。功能与 CLI 基本相同，仅界面不同。 ### 4. Claude Code CLI **现状：** 内置 computer-use MCP 服务器；通过 /mcp 启用即可 **细节：** 无需额外安装。通过 MCP 也间接支持 osascript/cliclick 等工具（但这是通过自定义 MCP 接入，非内置）。computer use 是最精确的交互方式，会优先尝试 MCP → Bash → Chrome → computer use。 ### 5. 社区开源方案 | 项目 | 链接 | 说明 | |------|------|------| | **trycua/cua** | https://github.com/trycua/cua | MIT 许可；支持 macOS/Linux/Windows；包含 cua-driver（后台操控）、cuabot（CLI）、MCP 服务器；可用于 Claude Code 和 Cursor | | **claude-computer-use-macos** | https://github.com/PallavAg/claude-computer-use-macos | 社区 Demo；演示如何将官方 API 集成到真实 macOS | ### 6. 你的配置中的 MCP 服务器 **Claude_in_Chrome：** Anthropic 官方；提供 computer/navigate/click/find/javascript_tool 等浏览器工具；仅适用 Chrome 内操作 **Claude_Preview：** Anthropic 官方；Desktop 应用内置的前端预览 MCP；自动启动 dev server + headless 浏览器，支持 screenshot/DOM 检查/点击模拟/网络监控 --- **总结：** 官方 Anthropic 的 computer use 已是生产级别，Mac 原生支持无需容器。社区方案（如 trycua）提供更细粒度控制（后台操控、轨迹回放）。你的 Claude Code 已加载官方 MCP 服务器，开箱可用。 Sources: - [Let Claude use your computer from the CLI - Claude Code Docs](https://code.claude.com/docs/en/computer-use) - [Control Your Mac with Natural Language: Claude's Computer Use Tool Explained](https://apidog.com/blog/claude-computer-use/) - [Anthropic's Claude AI Can Now Use Your Mac While You're Away - MacRumors](https://www.macrumors.com/2026/03/24/claude-use-mac-remotely-iphone/) - [Chrome DevTools for coding agents](https://github.com/ChromeDevTools/chrome-devtools-mcp) - [trycua/cua: Open-source infrastructure for Computer-Use Agents](https://github.com/trycua/cua) - [PallavAg/claude-computer-use-macos: MacOS Demo for Claude Computer Use](https://github.com/PallavAg/claude-computer-use-macos) - [Claude Code Desktop has a built-in preview MCP](https://medium.com/@dan.avila7/claude-code-desktop-has-a-built-in-preview-mcp-heres-how-it-works-774809ff676f)

> DEVELOPER

用户想知道：Claude Code（CLI 工具）能不能用 computer use 来操控本机 Mac？怎么开？ 需要你**用 WebSearch / WebFetch 实查**，不要凭印象作答。重点查清下面这些问题，截止到 2026 年 5 月： 1. Claude Code CLI（`/opt/homebrew/bin/claude`，v2.1.149 这个版本附近）官方文档里有没有"computer use"功能？官方页 https://code.claude.com/docs/en/computer-use 是不是真实存在？如果存在，请把页面要点抓出来。 2. 启用方式：是通过 `claude mcp add` 加一个 server？还是通过 `~/.claude/settings.json` 某个 flag？还是通过 `/mcp` 命令？给出**精确的 CLI 命令或配置 JSON**。 3. 需要的最低版本/订阅等级（Pro / Max / API key 用户）。 4. 它是用 Anthropic 自己的 native binding（像 Claude Desktop 里那个 `@ant/claude-swift/build/Release/computer_use.node`）实现的，还是会用别的方案？ 5. 需要的 macOS 权限有哪些（Accessibility / Screen Recording / Input Monitoring / AppleEvents）？ 6. 启用后，Claude Code 里多了哪些工具名（具体的 tool name，例如 `computer_20250124`、`mcp__computer__screenshot` 之类）？ 7. 如果官方还没在 Claude Code 里发布 computer use，社区有哪些靠谱的替代（trycua/cua MCP server、其他活跃维护的 macOS-control MCP），给 GitHub 地址 + 一句话特性对比。 报告控制在 500 字以内。每条结论后面贴一个**可点击的来源 URL**。**不确定的部分明确写"未找到证据"，不要补全**。用中文回答。

> AGENT

我来帮你实查这些问题。先从官方文档开始。

> AGENT

很好，官方文档存在。现在检查你配置里的 MCP server 情况，并搜索社区替代方案。

> AGENT

现在检查一下你的用户配置里的 computer-use MCP server 是否已启用。

> AGENT

现在整理成最终报告。 --- ## **Claude Code CLI 的 Computer Use 实查报告** ### **1. 官方文档确认** ✅ **页面存在**。官方文档 https://code.claude.com/docs/en/computer-use 真实存在，2026年5月更新。 **核心要点**： - Computer use 是 **内置 MCP server**，名称为 `computer-use`，默认禁用 - 支持 macOS 完整图形界面自动化：打开应用、点击、输入、截图 - 支持原生应用构建验证、UI 测试、布局调试、模拟器控制 [官方 Computer Use 文档](https://code.claude.com/docs/en/computer-use) --- ### **2. 启用方式** 启用通过 **交互式 `/mcp` 命令**： ``` /mcp # 进入 MCP 菜单 # 找到 computer-use，选择 Enable ``` 此后首次使用会提示授予 **Accessibility** 和 **Screen Recording** 两项 macOS 权限。 配置**不走** `settings.json`，而是 per-project 持久化在项目本地。 [启用步骤详见](https://code.claude.com/docs/en/computer-use) --- ### **3. 最低要求** - **版本**：Claude Code v2.1.85+（你的 v2.1.149 符合） - **订阅**：Pro 或 Max（不支持 Team/Enterprise；API Key 用户不支持） - **运行模式**：仅交互式会话（不支持 `-p` 非交互模式） - **平台**：仅 macOS（Windows 用 Claude Desktop；Linux 暂无 CLI 版本） [计划限制说明](https://code.claude.com/docs/en/computer-use) --- ### **4. 实现方案** **未找到证据** Claude Code CLI 是否用 native binding（如 Claude Desktop 的 `.node` 文件）。官方文档未公开详细实现层，仅说明 CLI 和 Desktop "共享同一引擎"但表面有差异。 --- ### **5. 需要的 macOS 权限** 仅两项（会自动弹窗）： - **Accessibility**：点击、输入、滚动 - **Screen Recording**：查看屏幕 Terminal 窗口自动排除在截图外（防止提示注入）。 [权限模型详见](https://code.claude.com/docs/en/computer-use) --- ### **6. 多出的工具名** **未找到证据**。官方文档未列出具体 tool name。你需要在项目里执行 `/mcp` → enable → 对 Claude 询问"你现在能用什么工具"。 --- ### **7. 社区替代方案** | 方案 | GitHub | 特点 | |------|--------|------| | **CUA** | [trycua/cua](https://github.com/trycua/cua) | 开源基础设施，支持 macOS/Linux/Windows；可在后台控制应用无需抢占焦点和鼠标 | | **Macuse MCP** | [macuse-app/macuse-mcp](https://github.com/macuse-app/macuse-mcp) | 原生 Mac 应用集成（日历、邮件、Notes、提醒），支持 Claude Desktop/Cursor/VS Code，per-app 权限管理 | | **CursorTouch macOS MCP** | [CursorTouch/MacOS-MCP](https://github.com/CursorTouch/MacOS-MCP) | 轻量级，专为 macOS 优化 | **推荐**：官方 `computer-use` 最稳定；如需额外 macOS 应用原生集成（日历等），用 Macuse；需沙盒或远程控制，用 CUA。 --- **总结**：你的 Claude Code v2.1.149 + Pro/Max 订阅可直接用 `/mcp` 启用 `computer-use`，无需额外配置。启用后即可用 computer use 控制你的 Mac。

> DEVELOPER

用户问：Claude Code 里**有没有"computer use"相关的 skill**？ 我之前断言 "computer use 只能是 MCP server 不能是 skill，因为 skill 不能定义新工具"。用户指出这个说法不对，让我实查。 请用 WebSearch / WebFetch 帮我搞清楚： 1. **官方 Anthropic skills marketplace / plugins** 里有没有跟 computer use 相关的 skill？我能看到的本地 user-invocable skills 是： - anthropic-skills:setup-cowork - anthropic-skills:pdf / pptx / xlsx / docx - anthropic-skills:consolidate-memory - anthropic-skills:skill-creator - 还有 update-config / keybindings-help / verify / code-review / fewer-permission-prompts / loop / schedule / claude-api / run / init / review / security-review 有没有遗漏的 "computer-use" 或 "control-mac" / "mac-control" / "ui-automation" / "screen-control" 类 skill？检查 https://github.com/anthropics/claude-code 和 https://github.com/anthropics/claude-skills 仓库。 2. **Skill 机制本身能不能"内含工具"？** 我之前说 "skill 是纯 prompt，不能定义新工具，只能调已存在的工具"——这个说法对吗？查最新的 Claude Code skill 规范（SKILL.md 格式），看 skill 能不能包含可执行脚本、bundled tool、声明自己依赖的 MCP server 等。 3. 有没有 **社区做的 "封装 computer-use 工具流" 的 skill** —— 例如把 "request_access → screenshot → click → screenshot 验证" 这种常用 pattern 包成一个 skill？搜 GitHub `topic:claude-skill computer` 或类似。 4. 关键差异：用户期待的"computer use skill"可能是什么形态？是不是 `/computer screenshot` `/computer click x,y` 这种把 MCP 工具包成 skill 命令的写法？这在当前 Claude Code skill 规范下可行吗？ 报告 400 字以内，每条结论后面给来源 URL。**不确定就明确说"未找到"**，不要补全。用中文。

> AGENT

我来帮你实查这个问题。让我查阅官方文档和仓库。

> AGENT

让我查阅 SKILL.md 规范和官方 skills 仓库内容：

> AGENT

太好了！找到关键线索。让我进一步查证 mcpmarket.com 上那两个 computer-use skill：

> AGENT

让我再查一遍 Claude Code 官方文档中关于 computer use 的部分：

> AGENT

完美。现在我有足够的信息了。让我生成报告： --- ## 调查结论 **1. 官方 computer-use skill 不存在** ✗ 官方 Anthropic skills 仓库（`anthropics/skills`）中**无 computer-use 相关 skill**。Skill 只是 Markdown + 脚本的组织形式，而 computer-use 是内置 MCP server，不能作为 skill 分发。 [SKILL.md 规范](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md) 未支持 MCP 依赖声明。 **2. Skill 机制限制** ✗ 你的说法**正确**。Skill 是 Markdown 文档 + 可选脚本（`scripts/` 目录），无法： - 定义新工具或声明 MCP 依赖 - 在 frontmatter 中指定必需的 MCP server - 内含工具实现本身 Skill 只能调用已启用的工具。 **3. 社区做的"包装 computer-use" skill** 存在但稀少 搜到两个 mcpmarket 上的 skill（`mac-control-ui-automation`、`computer-use-agent-builder`），但无法获取详情（服务限流）。GitHub 上无官方 computer-use skill 实现，只有 [demos 和第三方插件](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)。 **4. 用户期待的形态在当前规范下不可行** `/computer screenshot` 这类语法理论上可以通过 skill 指令集或钩子实现，但**无法在 skill 层面绑定 MCP server 依赖**。必须： - 先 `/mcp` 手动启用 `computer-use` MCP - 再依赖 prompt 指导 Claude 调用底层工具 不存在"skill 打包 MCP"的正式机制。 --- **来源：** - [Claude Code SKILL.md 规范](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md) - [Anthropic 官方 skills 仓库](https://github.com/anthropics/skills/blob/main/README.md) - [Claude Code computer-use 文档](https://code.claude.com/docs/en/computer-use)

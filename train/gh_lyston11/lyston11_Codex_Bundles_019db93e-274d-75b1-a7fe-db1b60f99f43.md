> DEVELOPER

帮我上网搜一下hermes agent是很么

> DEVELOPER

帮我上网搜一下hermes agent是什么

> AGENT

我先用 `agent-reach` 技能查一下网上对 `Hermes Agent` 的主流指代，确认它具体是哪个产品或项目，再给你一个简洁解释和来源。

> AGENT

我已经定位到官方站点和 GitHub 仓库了，网上现在提到的 `Hermes Agent` 基本都在指 Nous Research 这个开源项目。我再把核心信息收一下，顺手确认了一下最新版本号和发布日期。

> AGENT

`Hermes Agent` 现在主要指的是 Nous Research 做的一个开源 AI Agent。它不是普通聊天机器人，也不是只在 IDE 里用的 copilot，而是一个可以长期跑在你自己机器或 VPS 上的“常驻代理”。

简单说，它的特点是：
- 有持久记忆，能记住你之前的项目和偏好
- 会把解决过的问题沉淀成可复用的 `skills`
- 能通过 `CLI`、`Telegram`、`Discord`、`Slack`、`WhatsApp`、`Signal`、`Email` 等渠道和你交互
- 能做网页搜索、浏览器自动化、定时任务、子代理并行执行等事情
- 支持接 OpenAI 兼容接口，也支持 OpenRouter、Hugging Face 等

截至 `2026-04-23`，我查到官方 GitHub 最新发布是 `v0.10.0`，发布日期是 `2026-04-16`。

来源：
- [官方主页](https://hermes-agent.nousresearch.com/)
- [官方 GitHub 仓库](https://github.com/NousResearch/hermes-agent)
- [官方 Tags / Releases](https://github.com/NousResearch/hermes-agent/tags)

如果你愿意，我可以继续帮你查：
1. `Hermes Agent` 怎么安装
2. 它和 `Claude Code / Codex / Manus` 有什么区别
3. 有没有中文教程和上手案例

> DEVELOPER

我需要你先深入阅读lyston/Obsidian/lyston/工具/Codex/Hermes Agent 调研：MCP、技能与视频生成
然后再上谷歌谷歌搜索和github上帮我找hermes视频生成、剧本生成、图片生成的skills和mcp工具等，写入这个文档中

> AGENT

我先读你指定的调研文档，确认它现在的结构、已有结论和适合补充的位置；接着我会去查官方站点、GitHub 和相关公开资料，把 `Hermes` 在视频生成、剧本生成、图片生成方向能用的 `skills` 和 `MCP` 工具整理进去。

> AGENT

我已经把文档现状读完了。下一步我会分两条线补证据：一条查 Hermes 官方文档和 Skills Catalog，另一条查 GitHub 上跟视频、剧本、图片生成最相关的 skill 和 MCP 项目，整理成能直接落进这篇笔记的补充段落。

> AGENT

我已经把能落地的来源收齐了，接下来会把文档补成两层结构：一层是 Hermes 官方当前能力校准，另一层是“今天还能装、还能接”的社区 skills 和 MCP 清单，并顺手修正一处已经有点过期的 skill 说法。

> AGENT

我现在开始落文档了：会先把官方能力校准那几处更新掉，再补一段“2026-04-24 搜索补充”，把今天搜到的社区 skills、MCP 候选和安装判断标准整理进去。

> AGENT

文档已经补进去了。我先做一遍快速自检，重点看有没有结构断裂、旧结论没同步、或者新增链接/名称需要再校正的地方。

> AGENT

我发现一处细节需要一起修正：HeyGen 的 GitHub 主仓库里现在实际暴露的是 `heygen-avatar` 和 `heygen-video` 两个 skill，不是我刚才初稿里写的 `create-video` / `avatar-video`。我把这类命名和几条来源链接一起校正成更接近官方 / GitHub 原始来源的版本。

> AGENT

已把内容补进文档：[Hermes Agent 调研：MCP、技能与视频生成.md](/Users/lyston/Obsidian/lyston/工具/Codex/Hermes%20Agent%20调研：MCP、技能与视频生成.md)。

这次我做了几件事：
- 先通读了原文档，并把官方现状校准到 `2026-04-24`
- 修正了一个偏旧的说法：官方 optional catalog 里现在更明确能看到的是 `meme-generation`，没有继续把 `stable-diffusion-image-generation` 当作当前官方主推荐项
- 新增了一大段“社区 Skills”补充，按 `视频生成 / 剧本与分镜 / 图片生成` 分组，补了 `openai/skills`、`inference-sh`、`AI Labs`、`HeyGen` 这些可被 Hermes 接入的来源
- 扩充了 MCP 候选池，新增了 `MiniMax-MCP`、`fal-image-video-mcp`、`MeiGen-AI-Design-MCP`、`story-shot-agent`、`HeyGen remote MCP`
- 把参考链接补成了以 Hermes 官方文档和 GitHub 仓库为主的来源列表

我没有跑代码测试，因为这次是纯调研文档更新。  
如果你要，我下一步可以继续直接帮你把这篇文档再收敛成一版“最适合你当前场景的 3 套 Hermes 视频生产方案”。

> DEVELOPER

将我这个文档再好好整理一下

> AGENT

我先把这篇笔记当成“以后会反复翻的决策文档”来整理，不只是润色语句，而是会重排结构、去重、把“官方能力 / 社区技能 / 外部 MCP / 选型建议”几层拆清楚。

> AGENT

我准备这样整理，避免它继续像“资料堆积”而不是“可决策文档”：

1. 先把开头改成更强的摘要
   直接回答 Hermes 在图片、剧本/分镜、视频三件事上分别该怎么做。

2. 重排正文结构
   按 `Hermes 原生边界 -> Skills 体系 -> MCP 体系 -> 三类任务选型 -> 推荐组合` 组织，减少前后跳转。

3. 去重并合并表格
   现在有些技能、MCP 和建议在不同段落里重复出现，我会把它们收拢到统一清单和统一对比表里。

4. 把“能做什么”和“该怎么选”分开
   前者保留事实，后者给明确建议，这样以后回看时不需要重新通读全文。

我接下来直接改文档内容。

> AGENT

我这次会直接把整篇重排，不是局部修修补补。整理后你回看时应该能直接回答两个问题：`Hermes 自己会什么`，以及 `我该接哪条视频/图片/剧本链路`。

> AGENT

结构已经重排完了。我现在做一遍通读自检，主要看标题层级、表格逻辑和“结论是否能一眼看懂”，避免变成更长但更难用。

> AGENT

我已经把文档重新整理了一遍，重点不是润色，而是把它从“资料堆”改成“可决策文档”：  
[Hermes Agent 调研：MCP、技能与视频生成.md](/Users/lyston/Obsidian/lyston/工具/Codex/Hermes%20Agent%20调研：MCP、技能与视频生成.md)

这次主要做了这些调整：
- 把开头改成“一句话结论”，先回答 Hermes 在图片、剧本/分镜、视频三类任务上的真实边界
- 重排成 `原生边界 -> Skills 体系 -> MCP 体系 -> 按任务选型 -> 推荐组合 -> 多 Agent/Profile -> 最后建议`
- 合并了原来分散的技能和 MCP 信息，减少重复表述
- 把“事实信息”和“选型建议”拆开，回看时更容易直接拿去决策
- 保留了参考链接，但按 `Hermes 官方 / Skills / MCP` 分组了

这次是文档整理，没有跑代码测试。  
如果你愿意，我下一步可以继续帮你把这篇再压缩成一版“只保留最重要结论的 1 页摘要版”。

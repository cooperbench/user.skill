---
session_id: fee4fe38-85cb-4e15-a8b5-b4c55daddfa6
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-04-30T21:18:49.711Z"
n_turns: 4
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

npx @cometix/ccursor@latest install 看一下安装了怎么启动

> AGENT

已经安装过了。让我查看一下如何启动使用：

> AGENT

已经安装完成。让我查看配置文件了解如何配置和使用：

> AGENT

**Cursor++ BYOK 已安装完成** 当前状态： - ✓ 扩展已安装 - ✓ 各项补丁已应用 - 本地服务端口：`127.0.0.1:9960` ## 使用步骤 **1. 配置 AI 提供商** 编辑 `~/.ccursor/providers.json` 添加你的 AI 服务提供商： ```json { "$schemaVersion": 1, "providers": [ { "name": "openai", "baseURL": "https://api.openai.com/v1", "apiKey": "你的API密钥" } // 或者其他兼容 OpenAI 的服务 ] } ``` **2. 启动代理服务** 需要运行一个兼容 Cursor++ 协议的本地代理服务器（端口 9960），这通常是一个独立的工具。 **3. 重启 Cursor** 重启 Cursor 应用即可使用你的自定义 AI 服务。 --- 目前你的 `providers.json` 是空的，需要先添加配置。你想配置哪个 AI 服务提供商？

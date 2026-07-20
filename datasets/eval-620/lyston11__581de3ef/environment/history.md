> DEVELOPER

上网上、github等调研一下现在的agent知识库架构等
我需要搭建一个，你先给我好好调研一下

> AGENT

我会先用 `agent-reach` 的路由看一下可用的搜索/GitHub 调研方式，然后并行查官方资料、代表性开源项目和近期架构实践。这个问题我会按“可落地搭建”的口径整理，不只列名词。

> TOOL

tool_use exec_command
id: call_CYENzX4cBioIfE1sbh5HGc7U
```json
{
  "cmd": "sed -n '1,220p' /home/<USER>/.agents/skills/agent-reach/SKILL.md",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_CYENzX4cBioIfE1sbh5HGc7U
```
Chunk ID: 8a9cbf
Wall time: 0.0002 seconds
Process exited with code 0
Original token count: 872
Output:
---
name: agent-reach
description: >
  Give your AI agent eyes to see the entire internet.
  17 platforms via CLI, MCP, curl, and Python scripts.
  Zero config for 8 channels.

  【路由方式】SKILL.md 包含路由表和常用命令，复杂场景需按需阅读对应分类的 references/*.md。
  分类：search / social (小红书/抖音/微博/推特/B站/V2EX/Reddit) / career(LinkedIn) / dev(github) / web(网页/文章/公众号/RSS) / video(YouTube/B站/播客).

  Use when user asks to search, read, or interact on any supported platform,
  shares a URL, or asks to search the web.
triggers:
  - search: 搜/查/找/search/搜索/查一下/帮我搜
  - social:
    - 小红书: xiaohongshu/xhs/小红书/红书
    - 抖音: douyin/抖音
    - Twitter: twitter/推特/x.com/推文
    - 微博: weibo/微博
    - B站: bilibili/b站/哔哩哔哩
    - V2EX: v2ex
    - Reddit: reddit
  - career: 招聘/职位/求职/linkedin/领英/找工作
  - dev: github/代码/仓库/gh/issue/pr/分支/commit
  - web: 网页/链接/文章/公众号/微信文章/rss/读一下/打开这个
  - video: youtube/视频/播客/字幕/小宇宙/转录/yt
  - finance: 雪球/股票/stock/xueqiu/行情/基金
metadata:
  openclaw:
    homepage: https://github.com/Panniantong/Agent-Reach
---

# Agent Reach — 路由器

17 平台工具集合。根据用户意图选择对应分类。

## 路由表

| 用户意图 | 分类 | 详细文档 |
|---------|------|---------|
| 网页搜索/代码搜索 | search | [references/search.md](references/search.md) |
| 小红书/抖音/微博/推特/B站/V2EX/Reddit | social | [references/social.md](references/social.md) |
| 招聘/职位/LinkedIn | career | [references/career.md](references/career.md) |
| GitHub/代码 | dev | [references/dev.md](references/dev.md) |
| 网页/文章/公众号/RSS | web | [references/web.md](references/web.md) |
| YouTube/B站/播客字幕 | video | [references/video.md](references/video.md) |

## 零配置快速命令

```bash
# Exa 网页搜索
mcporter […]

> AGENT

我已经确认了本地的 `agent-reach` 技能入口；接下来会同时查“架构文章/官方文档”和“GitHub 上真实项目”。我会特别看：数据摄取、索引形态、检索编排、记忆模型、权限隔离、评测与运维这些能决定你之后怎么搭的部分。

> TOOL

tool_use exec_command
id: call_gYdcKEDFNM9zzFqBIuIaRBvm
```json
{
  "cmd": "sed -n '1,220p' /home/<USER>/.agents/skills/agent-reach/references/search.md",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_5n5nPviY3oZiQFCwJjRv92E2
```json
{
  "cmd": "sed -n '1,220p' /home/<USER>/.agents/skills/agent-reach/references/dev.md",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_NXn8dcGhayx7Lpwwhr34zmtV
```json
{
  "cmd": "command -v gh && gh --version",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result
id: call_gYdcKEDFNM9zzFqBIuIaRBvm
```
Chunk ID: f9248a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 206
Output:
# 搜索工具

Exa AI 搜索引擎。

## Exa AI 搜索

高质量 AI 搜索引擎，擅长技术和代码搜索。

```bash
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'
mcporter call 'exa.get_code_context_exa(query: "code question", tokensNum: 3000)'
```

### 使用场景

| 场景 | 参数 |
|-----|------|
| 网页搜索 | `web_search_exa(query: "...", numResults: 5)` |
| 代码搜索 | `get_code_context_exa(query: "...", tokensNum: 3000)` |

### 特点

- 擅长英文内容和技术文档
- 支持代码上下文搜索
- 结果质量高

## 与其他搜索工具对比

| 工具 | 来源 | 适用场景 |
|-----|------|---------|
| Exa | agent-reach | 英文/技术/代码搜索 |
| 智谱搜索 | my-mcp-tools | 中文搜索 |
| GitHub 搜索 | agent-reach (dev.md) | 仓库/代码搜索 |

```

> TOOL

tool_result
id: call_5n5nPviY3oZiQFCwJjRv92E2
```
Chunk ID: dc5ec5
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 346
Output:
# 开发工具

GitHub CLI 

## GitHub (gh CLI)

GitHub 官方命令行工具，用于仓库、Issue、PR、Actions、Release 以及 API 访问。

```bash
# 认证
gh auth login
gh auth status

# 搜索
gh search repos "query" --sort stars --limit 10
gh search code "query" --language python

# 仓库
gh repo view owner/repo
gh repo clone owner/repo
gh repo create my-repo --private
gh repo fork owner/repo
gh repo fork owner/repo --clone
gh repo sync owner/repo

# Issues
gh issue list -R owner/repo --state open
gh issue view 123 -R owner/repo
gh issue create -R owner/repo --title "Title" --body "Body"

# Pull Requests
gh pr list -R owner/repo --state open
gh pr view 123 -R owner/repo
gh pr create -R owner/repo --title "Title" --body "Body"
gh pr checks 123 --repo owner/repo

# Actions / CI
gh run list --repo owner/repo --limit 10
gh run view <run-id> --repo owner/repo
gh run view <run-id> --repo owner/repo --log-failed
gh workflow list --repo owner/repo

# Releases
gh release list -R owner/repo
gh release create v1.0.0

# API
gh api /user
gh api repos/owner/repo

# JSON 输出
gh issue list --repo owner/repo --json number,title […]

> TOOL

tool_result
id: call_NXn8dcGhayx7Lpwwhr34zmtV
```
Chunk ID: d72fb1
Wall time: 1.0016 seconds
Process running with session ID 41605
Original token count: 6
Output:
/opt/homebrew/bin/gh

```

> AGENT

第一批结果已经很有代表性：现在“Agent 知识库”已经不是单纯向量库了，主流在往长期记忆、混合检索、GraphRAG/时间图谱、MCP 工具化访问、评测闭环这几个方向合流。我还在补 GitHub 项目热度和官方文档细节，避免只凭营销页下判断。

> TOOL

tool_use write_stdin
id: call_HQHD7NbYTmiDZsTuEcYiZeJE
```json
{
  "session_id": 41605,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result
id: call_HQHD7NbYTmiDZsTuEcYiZeJE
```
Chunk ID: 09614c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 20
Output:
gh version 2.90.0 (2026-04-16)
https://github.com/cli/cli/releases/tag/v2.90.0

```

> TOOL

tool_use exec_command
id: call_D9zKthOUDL2z7rAYxvY4kdIb
```json
{
  "cmd": "gh search repos \"agent memory\" --sort stars --limit 20 --json fullName,description,stargazersCount,updatedAt,url",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_ya9SNf27j87ee5At9fjBTh57
```json
{
  "cmd": "gh search repos \"agentic rag\" --sort stars --limit 20 --json fullName,description,stargazersCount,updatedAt,url",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_EYBH2N5DQzAaY8eaGM4Mct2c
```json
{
  "cmd": "gh search repos \"knowledge graph rag\" --sort stars --limit 20 --json fullName,description,stargazersCount,updatedAt,url",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_OsrBtHOxtazeLtN23FowLnHb
```json
{
  "cmd": "gh search repos \"GraphRAG\" --sort stars --limit 20 --json fullName,description,stargazersCount,updatedAt,url",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_D9zKthOUDL2z7rAYxvY4kdIb
```
Chunk ID: 98b9bd
Wall time: 0.0612 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_ya9SNf27j87ee5At9fjBTh57
```
Chunk ID: cefc36
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_EYBH2N5DQzAaY8eaGM4Mct2c
```
Chunk ID: 220b21
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_OsrBtHOxtazeLtN23FowLnHb
```
Chunk ID: 7d440a
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_use exec_command
id: call_ggWZnXzSOuZgMmcWjBlMDi0I
```json
{
  "cmd": "gh search repos \"agent memory\" --sort stars --limit 20 --json fullName,description,stargazersCount,updatedAt,url",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网访问 GitHub 搜索代表性 Agent 记忆/知识库项目，是否允许？",
  "prefix_rule": [
    "gh",
    "search",
    "repos"
  ]
}
```

> TOOL

tool_use exec_command
id: call_L513LHUHloHuzT033STIHxpP
```json
{
  "cmd": "gh search repos \"agentic rag\" --sort stars --limit 20 --json fullName,description,stargazersCount,updatedAt,url",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网访问 GitHub 搜索 Agentic RAG 项目热度，是否允许？",
  "prefix_rule": [
    "gh",
    "search",
    "repos"
  ]
}
```

> TOOL

tool_use exec_command
id: call_bartOVh7M6hU12u3UBl5r1bq
```json
{
  "cmd": "gh search repos \"knowledge graph rag\" --sort stars --limit 20 --json fullName,description,stargazersCount,updatedAt,url",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网访问 GitHub 搜索知识图谱 RAG 项目，是否允许？",
  "prefix_rule": [
    "gh",
    "search",
    "repos"
  ]
}
```

> TOOL

tool_use exec_command
id: call_x2RtK8zcqIho73t6a6it9oXh
```json
{
  "cmd": "gh search repos \"GraphRAG\" --sort stars --limit 20 --json fullName,description,stargazersCount,updatedAt,url",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网访问 GitHub 搜索 GraphRAG 生态项目，是否允许？",
  "prefix_rule": [
    "gh",
    "search",
    "repos"
  ]
}
```

> TOOL

tool_result
id: call_ggWZnXzSOuZgMmcWjBlMDi0I
```
Chunk ID: 602f07
Wall time: 1.0013 seconds
Process running with session ID 13270
Original token count: 0
Output:

```

> TOOL

tool_result
id: call_L513LHUHloHuzT033STIHxpP
```
Chunk ID: 3cf9e9
Wall time: 1.0013 seconds
Process running with session ID 52724
Original token count: 0
Output:

```

> TOOL

tool_result
id: call_bartOVh7M6hU12u3UBl5r1bq
```
Chunk ID: c0f586
Wall time: 1.0015 seconds
Process running with session ID 46029
Original token count: 0
Output:

```

> TOOL

tool_result
id: call_x2RtK8zcqIho73t6a6it9oXh
```
Chunk ID: d87871
Wall time: 1.0006 seconds
Process running with session ID 56121
Original token count: 0
Output:

```

> TOOL

tool_use write_stdin
id: call_6PzxJ2YBmH4bFZ2ln2hQDh3i
```json
{
  "session_id": 13270,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use write_stdin
id: call_GFSTKOpCcYpWpKQfbvA21lOC
```json
{
  "session_id": 52724,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use write_stdin
id: call_IzWtKoto2IIMsfjY6oMGqOvp
```json
{
  "session_id": 46029,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use write_stdin
id: call_iLKHsrJTnBq4fHhbTY4Ccfgx
```json
{
  "session_id": 56121,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_6PzxJ2YBmH4bFZ2ln2hQDh3i
```
Chunk ID: 34d67c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1463
Output:
[{"description":"Hindsight: Agent Memory That  Learns","fullName":"vectorize-io/hindsight","stargazersCount":14446,"updatedAt":"2026-05-25T03:14:10Z","url":"https://github.com/vectorize-io/hindsight"},{"description":"TencentDB Agent Memory delivers fully local long-term memory for AI Agents via a 4-tier progressive pipeline, with zero external API dependencies.","fullName":"Tencent/TencentDB-Agent-Memory","stargazersCount":4039,"updatedAt":"2026-05-25T03:12:47Z","url":"https://github.com/Tencent/TencentDB-Agent-Memory"},{"description":"The paper list of \"Memory in the Age of AI Agents: A Survey\"","fullName":"Shichun-Liu/Agent-Memory-Paper-List","stargazersCount":2040,"updatedAt":"2026-05-25T02:10:18Z","url":"https://github.com/Shichun-Liu/Agent-Memory-Paper-List"},{"description":"A-MEM: Agentic Memory for LLM Agents","fullName":"agiresearch/A-mem","stargazersCount":1022,"updatedAt":"2026-05-25T00:43:00Z","url":"https://github.com/agiresearch/A-mem"},{"description":"Awesome AI Memory | LLM Memory | A curated knowledge base on AI memory for LLMs and agents, covering long-term memory, reasoning, retrieval, and memory-native system design.  Awesome-AI-Memory 是一个 集中式、持续更新的 AI 记忆知识库，系统性整理了与 大模型记忆（LLM Memory）与智能体记忆（Agent Memory） 相关的前沿研究、工程框架、系统设计、评测基准与真实应用实践。","fullName":"IAAR-Shanghai/Awesome-AI-Memory","stargazersCount":909,"updatedAt":"2026-05-25T01:52:23Z","url":"https://github.com/IAAR-Shanghai/Awesome-AI-Memory"},{"description":"The code for NeurIPS 2025 paper \"A-Mem: Agentic Memory for LLM Agents\"","fullName":"WujiangXu/A-mem","stargazersCount":892,"updatedAt":"2026-05-24T09:33:54Z","url":"https://github.com/WujiangXu/A-mem"},{"description":"A general memory system for agents, powered by deep-research","fullName":"VectorSpaceLab/general-agentic-memory","stargazersCount":849,"updatedAt":"2026-05-22T04:41:58Z","url":"https://github.com/VectorSpaceLab/general-agentic-memory"},{"description":"MCP server for long term agent memory with Mem0. Also useful as a template to get you started building your own MCP server with Python!","fullName":"coleam00/mcp-mem0","stargazersCount":676,"updatedAt":"2026-05-24T03:15:21Z","url":"https://github.com/coleam00/mcp-mem0"},{"description":"Hierarchical Agent Memory with Git-Like Version Control","fullName":"zhangfengcdt/memoir","stargazersCount":548,"updatedAt":"2026-05-24T21:08:34Z","url":"https://github.com/zhangfengcdt/memoir"},{"description":"Implementing cognitive architecture and psychological memory concepts into Agentic LLM Systems","fullName":"ALucek/agentic-memory","stargazersCount":537,"updatedAt":"2026-05-19T10:23:34Z","url":"https://github.com/ALucek/agentic-memory"},{"description":"Open-source self-hosted AI agent runtime and multi-agent framework for autonomous agent swarms. Agent memory, MCP tools, schedules, delegation, and 23+ LLM providers (Claude, GPT, Gemini, OpenRouter, Ollama). A practical Claude Code and LangChain alternative.","fullName":"swarmclawai/swarmclaw","stargazersCount":519,"updatedAt":"2026-05-25T02:45:03Z","url":"https://github.com/swarmclawai/swarmclaw"},{"description":"","fullName":"nuster1128/LLM_Agent_Memory_Survey","stargazersCount":494,"updatedAt":"2026-05-21T09:02:38Z","url":"https://github.com/nuster1128/LLM_Agent_Memory_Survey"},{"description":"The local-first LLM Wiki: open-source knowledge graph builder, RAG knowledge base, […]

> TOOL

tool_result
id: call_GFSTKOpCcYpWpKQfbvA21lOC
```
Chunk ID: 06be53
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1496
Output:
[{"description":"100+ AI Agent & RAG apps you can actually run — clone, customize, ship.","fullName":"Shubhamsaboo/awesome-llm-apps","stargazersCount":111677,"updatedAt":"2026-05-25T03:16:14Z","url":"https://github.com/Shubhamsaboo/awesome-llm-apps"},{"description":"Open-source AI orchestration framework for building context-engineered, production-ready LLM applications. Design modular pipelines and agent workflows with explicit control over retrieval, routing, memory, and generation. Built for scalable agents, RAG, multimodal applications, semantic search, and conversational systems.","fullName":"deepset-ai/haystack","stargazersCount":25369,"updatedAt":"2026-05-25T02:23:30Z","url":"https://github.com/deepset-ai/haystack"},{"description":"280+ free n8n automation templates — ready-to-use workflows for Gmail, Telegram, Slack, Discord, WhatsApp, Google Drive, Notion, OpenAI, and more. AI agents, RAG   chatbots, email automation, social media, DevOps, and document processing. The largest open-source n8n template collection.","fullName":"enescingoz/awesome-n8n-templates","stargazersCount":22452,"updatedAt":"2026-05-25T02:13:02Z","url":"https://github.com/enescingoz/awesome-n8n-templates"},{"description":"","fullName":"jamwithai/production-agentic-rag-course","stargazersCount":6002,"updatedAt":"2026-05-24T23:52:23Z","url":"https://github.com/jamwithai/production-agentic-rag-course"},{"description":"The easiest way to use Agentic RAG in any enterprise","fullName":"ragapp/ragapp","stargazersCount":4437,"updatedAt":"2026-05-22T13:22:12Z","url":"https://github.com/ragapp/ragapp"},{"description":"A modular Agentic RAG built with LangGraph — learn Retrieval-Augmented Generation Agents in minutes.","fullName":"GiovanniPasq/agentic-rag-for-dummies","stargazersCount":3324,"updatedAt":"2026-05-24T10:42:10Z","url":"https://github.com/GiovanniPasq/agentic-rag-for-dummies"},{"description":"Learn to build your Second Brain AI assistant with LLMs, agents, RAG, fine-tuning, LLMOps and AI systems techniques.","fullName":"decodingai-magazine/second-brain-ai-assistant-course","stargazersCount":2751,"updatedAt":"2026-05-24T18:56:28Z","url":"https://github.com/decodingai-magazine/second-brain-ai-assistant-course"},{"description":"企业级 Agentic RAG 智能体 - 全链路覆盖文档解析、多路检索、意图识别、问题重写、会话记忆、MCP 工具调用与深度思考。面向真实业务场景，从 0 到 1 完整工程实现。","fullName":"nageoffer/ragent","stargazersCount":2320,"updatedAt":"2026-05-25T03:10:51Z","url":"https://github.com/nageoffer/ragent"},{"description":"Agentic-RAG explores advanced Retrieval-Augmented Generation systems enhanced with AI LLM agents. ","fullName":"asinghcsu/AgenticRAG-Survey","stargazersCount":1627,"updatedAt":"2026-05-24T09:56:23Z","url":"https://github.com/asinghcsu/AgenticRAG-Survey"},{"description":"A project-based course repository for developing AI agents using LangChain v1+ and LangGraph: search agents, RAG systems, reflection agents, and code interpreters.","fullName":"emarco177/langchain-course","stargazersCount":1418,"updatedAt":"2026-05-24T14:25:39Z","url":"https://github.com/emarco177/langchain-course"},{"description":"Full-stack AI app generator — FastAPI + Next.js with AI Agents, RAG, […]

> TOOL

tool_result
id: call_IzWtKoto2IIMsfjY6oMGqOvp
```
Chunk ID: 95f9d3
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1729
Output:
[{"description":"🧠 AI-powered Personalized Exam System: Integrating OpenPangu LLM, Knowledge Graph RAG, and BKT algorithm for adaptive question generation and recommendation. 基于LLM与知识图谱的智能个性化出题系统。","fullName":"sribdcn/PersonalExam","stargazersCount":503,"updatedAt":"2026-05-24T15:44:52Z","url":"https://github.com/sribdcn/PersonalExam"},{"description":"A knowledge graph RAG app using LangChain and Neo4j.","fullName":"hfhoffman1144/langchain_neo4j_rag_app","stargazersCount":247,"updatedAt":"2026-04-17T08:28:03Z","url":"https://github.com/hfhoffman1144/langchain_neo4j_rag_app"},{"description":"A breakdown of knowledge graph RAG with diagrams and examples","fullName":"ALucek/GraphRAG-Breakdown","stargazersCount":169,"updatedAt":"2026-05-04T12:26:11Z","url":"https://github.com/ALucek/GraphRAG-Breakdown"},{"description":"","fullName":"pdichone/knowledge-graph-rag","stargazersCount":64,"updatedAt":"2026-05-19T07:06:37Z","url":"https://github.com/pdichone/knowledge-graph-rag"},{"description":"Local LLM Graph RAG: from PDF to Neo4J to LLM (Python | LangChain | Neo4J | Ollama)","fullName":"rathcoding/knowledge-graph-rag","stargazersCount":54,"updatedAt":"2026-04-15T03:20:19Z","url":"https://github.com/rathcoding/knowledge-graph-rag"},{"description":"memAry @ University of Texas at Austin","fullName":"seyeong-han/KnowledgeGraphRAG","stargazersCount":21,"updatedAt":"2025-05-08T04:39:39Z","url":"https://github.com/seyeong-han/KnowledgeGraphRAG"},{"description":"This repository contains notebooks for building knowledge graphs and using them to improve Retrieval Augmented Generation (RAG) systems. RAG leverages knowledge graphs with embedding models to enhance the quality of text retrieved for language models.","fullName":"dev-ai-kar/google-neo4j-knowledge-graph-rag","stargazersCount":14,"updatedAt":"2025-05-06T07:37:45Z","url":"https://github.com/dev-ai-kar/google-neo4j-knowledge-graph-rag"},{"description":"Knowledge Graph-RAG system using Neo4j, LangChain, LangGraph, Claude-3.5-Sonnet. Hybrid retrieval: SBERT embeddings + graph traversal + BM25. 61K papers, 190K authors from Scopus. 50% NDCG improvement, 57% bias reduction. Includes notebooks, evaluation scripts, benchmark queries. Python/Jupyter.","fullName":"safishamsi/Knowledge-Graph-Based-Hybrid-RAG-System","stargazersCount":14,"updatedAt":"2026-04-28T23:08:58Z","url":"https://github.com/safishamsi/Knowledge-Graph-Based-Hybrid-RAG-System"},{"description":"Comprehensive research and knowledge management skill merging Perplexity Computer's research + data skills with Claude Code's knowledge graphs, RAG, brainstorming, and content synthesis. Deep research, statistical analysis, visualization.","fullName":"get-zeked/research-knowledge-super-skill","stargazersCount":12,"updatedAt":"2026-05-15T16:28:30Z","url":"https://github.com/get-zeked/research-knowledge-super-skill"},{"description":"This Repo will explain the knowledge Graph implementation and difference completely","fullName":"manojkanur/Knowledge-Graph-RAG","stargazersCount":11,"updatedAt":"2026-03-16T08:57:17Z","url":"https://github.com/manojkanur/Knowledge-Graph-RAG"},{"description":"Hybrid Knowledge Graph + RAG security intelligence platform for CVE analytics and semantic search. […]

> TOOL

tool_result
id: call_iLKHsrJTnBq4fHhbTY4Ccfgx
```
Chunk ID: 11c64a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1578
Output:
[{"description":"AI coding assistant skill (Claude Code, Codex, OpenCode, Cursor, Gemini CLI, and more). Turn any folder of code, SQL schemas, R scripts, shell scripts, docs, papers, images, or videos into a queryable knowledge graph. App code + database schema + infrastructure in one graph.","fullName":"safishamsi/graphify","stargazersCount":53131,"updatedAt":"2026-05-25T03:19:04Z","url":"https://github.com/safishamsi/graphify"},{"description":"[EMNLP2025] \"LightRAG: Simple and Fast Retrieval-Augmented Generation\"","fullName":"HKUDS/LightRAG","stargazersCount":35680,"updatedAt":"2026-05-25T02:58:00Z","url":"https://github.com/HKUDS/LightRAG"},{"description":"A modular graph-based Retrieval-Augmented Generation (RAG) system","fullName":"microsoft/graphrag","stargazersCount":33200,"updatedAt":"2026-05-25T03:00:37Z","url":"https://github.com/microsoft/graphrag"},{"description":"Memory control plane for AI Agents in 6 lines of code","fullName":"topoteretes/cognee","stargazersCount":17495,"updatedAt":"2026-05-25T02:37:27Z","url":"https://github.com/topoteretes/cognee"},{"description":"Local knowledge graph for Claude Code. Builds a persistent map of your codebase so Claude reads only what matters — 6.8× fewer tokens on reviews and up to 49× on daily coding tasks.","fullName":"tirth8205/code-review-graph","stargazersCount":17333,"updatedAt":"2026-05-25T03:19:54Z","url":"https://github.com/tirth8205/code-review-graph"},{"description":"https://adongwanai.github.io/AgentGuide | AI Agent开发指南 | LangGraph实战 | 高级RAG | 转行大模型 | 大模型面试 | 算法工程师 | 面试题库 | 强化学习｜数据合成","fullName":"adongwanai/AgentGuide","stargazersCount":5115,"updatedAt":"2026-05-25T02:39:13Z","url":"https://github.com/adongwanai/AgentGuide"},{"description":"Neo4j graph construction from unstructured data using LLMs","fullName":"neo4j-labs/llm-graph-builder","stargazersCount":4701,"updatedAt":"2026-05-23T16:43:46Z","url":"https://github.com/neo4j-labs/llm-graph-builder"},{"description":"A super fast Graph Database uses GraphBLAS under the hood for its sparse adjacency matrix graph representation. Our goal is to provide the best Knowledge Graph for LLM (GraphRAG).","fullName":"FalkorDB/FalkorDB","stargazersCount":4458,"updatedAt":"2026-05-25T02:57:11Z","url":"https://github.com/FalkorDB/FalkorDB"},{"description":"High-performance open-source in-memory graph database for GraphRAG, AI memory, agentic AI, and real-time graph analytics. Cypher-compatible, built in C++.","fullName":"memgraph/memgraph","stargazersCount":4064,"updatedAt":"2026-05-24T19:48:04Z","url":"https://github.com/memgraph/memgraph"},{"description":"A simple, easy-to-hack GraphRAG implementation","fullName":"gusye1234/nano-graphrag","stargazersCount":3847,"updatedAt":"2026-05-24T21:01:05Z","url":"https://github.com/gusye1234/nano-graphrag"},{"description":"RAG that intelligently adapts to your use case, […]

> AGENT

GitHub 搜索能跑通了。我看到几个很强的信号：`microsoft/graphrag`、`HKUDS/LightRAG`、`topoteretes/cognee`、`mem0`/`Letta`/`Graphiti` 这类项目分别代表“图谱增强检索”和“Agent 长期记忆”两条主线；我会再读它们 README/文档确认能力边界。

> TOOL

tool_use exec_command
id: call_p4DDPBbTB2nqLTx2TlioWgAI
```json
{
  "cmd": "gh repo view microsoft/graphrag --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_use exec_command
id: call_lHqs2PTAOp1Lqvgs6bKo6uBC
```json
{
  "cmd": "gh repo view HKUDS/LightRAG --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_use exec_command
id: call_WpYDD1IqXIdXCbfxDyssi2gg
```json
{
  "cmd": "gh repo view topoteretes/cognee --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_use exec_command
id: call_nq9LeAJ2kDluJ4E8vSsJ78fF
```json
{
  "cmd": "gh repo view mem0ai/mem0 --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result
id: call_p4DDPBbTB2nqLTx2TlioWgAI
```
Chunk ID: 7f8882
Wall time: 0.0924 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_lHqs2PTAOp1Lqvgs6bKo6uBC
```
Chunk ID: 7868d7
Wall time: 0.0851 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_WpYDD1IqXIdXCbfxDyssi2gg
```
Chunk ID: 8e8fe4
Wall time: 0.0927 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_nq9LeAJ2kDluJ4E8vSsJ78fF
```
Chunk ID: 5cbd71
Wall time: 0.0927 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_use exec_command
id: call_z3XzOBtuex1AXbtlJ38uVkJJ
```json
{
  "cmd": "gh repo view microsoft/graphrag --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网读取 GitHub 仓库元数据来核对 GraphRAG 项目状态，是否允许？",
  "prefix_rule": [
    "gh",
    "repo",
    "view"
  ]
}
```

> TOOL

tool_use exec_command
id: call_U8Fpnbf76RVbJKAucPaGKjoa
```json
{
  "cmd": "gh repo view HKUDS/LightRAG --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网读取 GitHub 仓库元数据来核对 LightRAG 项目状态，是否允许？",
  "prefix_rule": [
    "gh",
    "repo",
    "view"
  ]
}
```

> TOOL

tool_use exec_command
id: call_kh7CGNmqbeEjJEGcYn2DUxgM
```json
{
  "cmd": "gh repo view topoteretes/cognee --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网读取 GitHub 仓库元数据来核对 Cognee 项目状态，是否允许？",
  "prefix_rule": [
    "gh",
    "repo",
    "view"
  ]
}
```

> TOOL

tool_use exec_command
id: call_vfOkhLIFP75WPz3PB8Wq5eyY
```json
{
  "cmd": "gh repo view mem0ai/mem0 --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网读取 GitHub 仓库元数据来核对 Mem0 项目状态，是否允许？",
  "prefix_rule": [
    "gh",
    "repo",
    "view"
  ]
}
```

> TOOL

tool_result
id: call_z3XzOBtuex1AXbtlJ38uVkJJ
```
Chunk ID: f7ad85
Wall time: 0.9957 seconds
Process exited with code 0
Original token count: 158
Output:
{"description":"A modular graph-based Retrieval-Augmented Generation (RAG) system","homepageUrl":"https://microsoft.github.io/graphrag/","latestRelease":{"name":"v3.0.9","tagName":"3.0.9","url":"https://github.com/microsoft/graphrag/releases/tag/3.0.9","publishedAt":"2026-04-13T19:29:27Z"},"licenseInfo":{"key":"mit","name":"MIT License","nickname":""},"nameWithOwner":"microsoft/graphrag","repositoryTopics":[{"name":"graphrag"},{"name":"rag"},{"name":"llm"},{"name":"llms"},{"name":"gpt"},{"name":"gpt-4"},{"name":"gpt4"}],"stargazerCount":33200,"updatedAt":"2026-05-25T03:00:37Z","url":"https://github.com/microsoft/graphrag"}

```

> TOOL

tool_result
id: call_U8Fpnbf76RVbJKAucPaGKjoa
```
Chunk ID: adb903
Wall time: 0.9755 seconds
Process exited with code 0
Original token count: 180
Output:
{"description":"[EMNLP2025] \"LightRAG: Simple and Fast Retrieval-Augmented Generation\"","homepageUrl":"https://arxiv.org/abs/2410.05779","latestRelease":{"name":"v1.5.0rc2","tagName":"v1.5.0rc2","url":"https://github.com/HKUDS/LightRAG/releases/tag/v1.5.0rc2","publishedAt":"2026-05-21T07:48:07Z"},"licenseInfo":{"key":"mit","name":"MIT License","nickname":""},"nameWithOwner":"HKUDS/LightRAG","repositoryTopics":[{"name":"knowledge-graph"},{"name":"large-language-models"},{"name":"retrieval-augmented-generation"},{"name":"genai"},{"name":"graphrag"},{"name":"llm"},{"name":"rag"},{"name":"gpt"},{"name":"gpt-4"}],"stargazerCount":35680,"updatedAt":"2026-05-25T02:58:00Z","url":"https://github.com/HKUDS/LightRAG"}

```

> TOOL

tool_result
id: call_kh7CGNmqbeEjJEGcYn2DUxgM
```
Chunk ID: 591332
Wall time: 1.0018 seconds
Process running with session ID 38066
Original token count: 0
Output:

```

> TOOL

tool_result
id: call_vfOkhLIFP75WPz3PB8Wq5eyY
```
Chunk ID: f50a89
Wall time: 1.0012 seconds
Process running with session ID 40620
Original token count: 0
Output:

```

> TOOL

tool_use write_stdin
id: call_KL4WaFPsjRLDV8yjWQc0prD6
```json
{
  "session_id": 38066,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_use write_stdin
id: call_MpD0HtKsRNACZs1hx0gjYEFu
```json
{
  "session_id": 40620,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result
id: call_KL4WaFPsjRLDV8yjWQc0prD6
```
Chunk ID: fc1e05
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 249
Output:
{"description":"Memory control plane for AI Agents in 6 lines of code","homepageUrl":"https://www.cognee.ai","latestRelease":{"name":"v1.1.1.dev0","tagName":"v1.1.1.dev0","url":"https://github.com/topoteretes/cognee/releases/tag/v1.1.1.dev0","publishedAt":"2026-05-22T10:01:55Z"},"licenseInfo":{"key":"apache-2.0","name":"Apache License 2.0","nickname":""},"nameWithOwner":"topoteretes/cognee","repositoryTopics":[{"name":"ai"},{"name":"cognitive-architecture"},{"name":"vector-database"},{"name":"openai"},{"name":"rag"},{"name":"ai-agents"},{"name":"graph-database"},{"name":"ai-memory"},{"name":"cognitive-memory"},{"name":"neo4j"},{"name":"knowledge"},{"name":"knowledge-graph"},{"name":"graph-rag"},{"name":"graphrag"},{"name":"contributions-welcome"},{"name":"good-first-issue"},{"name":"good-first-pr"},{"name":"help-wanted"},{"name":"open-source"},{"name":"context-engineering"}],"stargazerCount":17495,"updatedAt":"2026-05-25T02:37:27Z","url":"https://github.com/topoteretes/cognee"}

```

> TOOL

tool_result
id: call_MpD0HtKsRNACZs1hx0gjYEFu
```
Chunk ID: fd6d21
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 191
Output:
{"description":"Universal memory layer for AI Agents","homepageUrl":"https://mem0.ai","latestRelease":{"name":"mem0-cli v0.2.7","tagName":"cli-v0.2.7","url":"https://github.com/mem0ai/mem0/releases/tag/cli-v0.2.7","publishedAt":"2026-05-20T19:36:30Z"},"licenseInfo":{"key":"apache-2.0","name":"Apache License 2.0","nickname":""},"nameWithOwner":"mem0ai/mem0","repositoryTopics":[{"name":"ai"},{"name":"chatgpt"},{"name":"llm"},{"name":"python"},{"name":"chatbots"},{"name":"rag"},{"name":"application"},{"name":"long-term-memory"},{"name":"memory"},{"name":"memory-management"},{"name":"state-management"},{"name":"ai-agents"},{"name":"agents"},{"name":"genai"}],"stargazerCount":56618,"updatedAt":"2026-05-25T03:19:28Z","url":"https://github.com/mem0ai/mem0"}

```

> TOOL

tool_use exec_command
id: call_cyS3BkojYNIM26UoKV6oe3m8
```json
{
  "cmd": "gh repo view getzep/graphiti --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_use exec_command
id: call_NgGh9XgLJgKBa0QYcj1Mglm3
```json
{
  "cmd": "gh repo view letta-ai/letta --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_use exec_command
id: call_5IeYAZUk8MxaEofjQ6DCI4Uv
```json
{
  "cmd": "gh repo view vectorize-io/hindsight --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_use exec_command
id: call_gdrV4iWyE5OnwL2U6ozHayzc
```json
{
  "cmd": "gh repo view deepset-ai/haystack --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result
id: call_cyS3BkojYNIM26UoKV6oe3m8
```
Chunk ID: 08d06e
Wall time: 0.0867 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_NgGh9XgLJgKBa0QYcj1Mglm3
```
Chunk ID: 2954c4
Wall time: 0.0413 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_5IeYAZUk8MxaEofjQ6DCI4Uv
```
Chunk ID: 8da6fc
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_result
id: call_gdrV4iWyE5OnwL2U6ozHayzc
```
Chunk ID: c150c9
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 24
Output:
error connecting to api.github.com
check your internet connection or https://githubstatus.com

```

> TOOL

tool_use exec_command
id: call_eERIxGVn5gBwaBdklyhdYLcs
```json
{
  "cmd": "gh repo view getzep/graphiti --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网读取 Graphiti 仓库元数据，是否允许？",
  "prefix_rule": [
    "gh",
    "repo",
    "view"
  ]
}
```

> TOOL

tool_use exec_command
id: call_GGSMrGkBehsuuLv4rXBei6pa
```json
{
  "cmd": "gh repo view letta-ai/letta --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网读取 Letta 仓库元数据，是否允许？",
  "prefix_rule": [
    "gh",
    "repo",
    "view"
  ]
}
```

> TOOL

tool_use exec_command
id: call_x6OqZVFeK2NFAkPwTIKKjrv9
```json
{
  "cmd": "gh repo view vectorize-io/hindsight --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网读取 Hindsight 仓库元数据，是否允许？",
  "prefix_rule": [
    "gh",
    "repo",
    "view"
  ]
}
```

> TOOL

tool_use exec_command
id: call_ku3Rw8z3Eee8UDUjdEp9KySV
```json
{
  "cmd": "gh repo view deepset-ai/haystack --json nameWithOwner,description,stargazerCount,updatedAt,url,homepageUrl,repositoryTopics,latestRelease,licenseInfo",
  "workdir": "/home/<USER>/PycharmProjects",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000,
  "sandbox_permissions": "require_escalated",
  "justification": "需要联网读取 Haystack 仓库元数据，是否允许？",
  "prefix_rule": [
    "gh",
    "repo",
    "view"
  ]
}
```

> TOOL

tool_result
id: call_eERIxGVn5gBwaBdklyhdYLcs
```
Chunk ID: c13190
Wall time: 0.9389 seconds
Process exited with code 0
Original token count: 151
Output:
{"description":"Build Real-Time Knowledge Graphs for AI Agents","homepageUrl":"https://help.getzep.com/graphiti","latestRelease":{"name":"v0.29.1 - Optimizations and Efficiencies","tagName":"v0.29.1","url":"https://github.com/getzep/graphiti/releases/tag/v0.29.1","publishedAt":"2026-05-21T03:32:50Z"},"licenseInfo":{"key":"apache-2.0","name":"Apache License 2.0","nickname":""},"nameWithOwner":"getzep/graphiti","repositoryTopics":[{"name":"agents"},{"name":"graph"},{"name":"llms"},{"name":"rag"}],"stargazerCount":26490,"updatedAt":"2026-05-25T03:14:18Z","url":"https://github.com/getzep/graphiti"}

```

> TOOL

tool_result
id: call_GGSMrGkBehsuuLv4rXBei6pa
```
Chunk ID: 0e2dc0
Wall time: 0.9251 seconds
Process exited with code 0
Original token count: 158
Output:
{"description":"Letta is the platform for building stateful agents: AI with advanced memory that can learn and self-improve over time.","homepageUrl":"https://docs.letta.com/","latestRelease":{"name":"v0.16.8","tagName":"0.16.8","url":"https://github.com/letta-ai/letta/releases/tag/0.16.8","publishedAt":"2026-05-14T17:14:24Z"},"licenseInfo":{"key":"apache-2.0","name":"Apache License 2.0","nickname":""},"nameWithOwner":"letta-ai/letta","repositoryTopics":[{"name":"llm"},{"name":"llm-agent"},{"name":"ai"},{"name":"ai-agents"}],"stargazerCount":22938,"updatedAt":"2026-05-25T03:21:59Z","url":"https://github.com/letta-ai/letta"}

```

> TOOL

tool_result
id: call_x6OqZVFeK2NFAkPwTIKKjrv9
```
Chunk ID: 3f7834
Wall time: 0.9342 seconds
Process exited with code 0
Original token count: 144
Output:
{"description":"Hindsight: Agent Memory That  Learns","homepageUrl":"https://hindsight.vectorize.io/","latestRelease":{"name":"v0.6.2","tagName":"v0.6.2","url":"https://github.com/vectorize-io/hindsight/releases/tag/v0.6.2","publishedAt":"2026-05-14T20:27:52Z"},"licenseInfo":{"key":"mit","name":"MIT License","nickname":""},"nameWithOwner":"vectorize-io/hindsight","repositoryTopics":[{"name":"agentic-ai"},{"name":"memory"},{"name":"agents"},{"name":"ai-memory"}],"stargazerCount":14446,"updatedAt":"2026-05-25T03:14:10Z","url":"https://github.com/vectorize-io/hindsight"}

```

> TOOL

tool_result
id: call_ku3Rw8z3Eee8UDUjdEp9KySV
```
Chunk ID: c62f80
Wall time: 1.0015 seconds
Process running with session ID 32749
Original token count: 0
Output:

```

> TOOL

tool_use write_stdin
id: call_lsqor10zwU8d1RUe1O43zIB2
```json
{
  "session_id": 32749,
  "chars": "",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result
id: call_lsqor10zwU8d1RUe1O43zIB2
```
Chunk ID: c4c9f5
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 312
Output:
{"description":"Open-source AI orchestration framework for building context-engineered, production-ready LLM applications. Design modular pipelines and agent workflows with explicit control over retrieval, routing, memory, and generation. Built for scalable agents, RAG, multimodal applications, semantic search, and conversational systems.","homepageUrl":"https://haystack.deepset.ai","latestRelease":{"name":"v2.29.0","tagName":"v2.29.0","url":"https://github.com/deepset-ai/haystack/releases/tag/v2.29.0","publishedAt":"2026-05-12T14:25:16Z"},"licenseInfo":{"key":"apache-2.0","name":"Apache License 2.0","nickname":""},"nameWithOwner":"deepset-ai/haystack","repositoryTopics":[{"name":"nlp"},{"name":"question-answering"},{"name":"pytorch"},{"name":"semantic-search"},{"name":"information-retrieval"},{"name":"summarization"},{"name":"transformers"},{"name":"machine-learning"},{"name":"ai"},{"name":"python"},{"name":"large-language-models"},{"name":"generative-ai"},{"name":"llm"},{"name":"rag"},{"name":"retrieval-augmented-generation"},{"name":"agents"},{"name":"agent"},{"name":"gemini"},{"name":"gpt-4"},{"name":"orchestration"}],"stargazerCount":25369,"updatedAt":"2026-05-25T02:23:30Z","url":"https://github.com/deepset-ai/haystack"}

```

> AGENT

调研日期：2026-05-25。结论先说：现在适合搭的不是“一个向量库”，而是 **Agent 知识/记忆层**：原始资料可追溯、向量+关键词+图谱混合检索、长期记忆按用户/组织/Agent 隔离、通过 MCP/API 给不同 Agent 调用。

**当前主流架构**
1. **基础 RAG 层**：文档解析、结构化切块、embedding、BM25/全文检索、rerank、引用溯源。OpenAI File Search 也是这个范式：先建 vector store，再让模型用语义+关键词检索文件。([platform.openai.com](https://platform.openai.com/docs/guides/tools-file-search/))  
2. **Agent Memory 层**：不只存文档，还存偏好、事实、历史经验、操作流程。LangGraph 把记忆分为短期线程记忆和跨会话长期记忆，并明确 semantic/episodic/procedural 三类。([docs.langchain.com](https://docs.langchain.com/oss/python/concepts/memory))  
3. **GraphRAG 层**：适合大型静态语料的全局理解和多跳问题。Microsoft GraphRAG 会抽实体、关系、claims，做社区检测和社区摘要，再结合向量索引。([microsoft.github.io](https://microsoft.github.io/graphrag//index/overview/))  
4. **Temporal Graph Memory 层**：这是 Agent 知识库的新重点。Graphiti/Zep 不是只问“什么是真的”，还记录“什么时候是真的、什么时候失效”，适合用户画像、业务状态、长期对话。([github.com](https://github.com/getzep/graphiti))  
5. **多存储混合层**：Cognee 这类系统已经把 relational store、vector store、graph store 作为标准组合：关系库存 provenance，向量库存语义召回，图库存实体关系。([docs.cognee.ai](https://docs.cognee.ai/core-concepts/architecture))  

**GitHub 代表项目**
我用 GitHub CLI 查了当前热度，值得重点看这些：

| 项目 | Stars | 适合什么 |
|---|---:|---|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 56.6k | 快速接入 Agent 长期记忆，用户/Agent/session memory |
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 35.7k | 轻量 GraphRAG，静态知识库增强检索 |
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | 33.2k | 企业文档、全局摘要、多跳分析 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | 26.5k | 时间图谱记忆，动态事实、历史状态 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | 22.9k | Stateful agents，自带高级记忆模型 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | 17.5k | graph+vector+relational 的通用记忆引擎 |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 25.4k | 生产级 RAG/Agent pipeline 编排 |

**我建议你的落地架构**
第一版别一上来重 GraphRAG 全家桶，先做一个可进化的混合知识层：

```text
数据源
GitHub / Markdown / PDF / 网页 / 数据库 / 对话记录 / 工单
  ↓
摄取层
解析、清洗、结构化切块、元数据、权限、版本、来源哈希
  ↓
存储层
Postgres: 文档、chunk、版本、ACL、引用、记忆事件
Qdrant 或 pgvector: dense/sparse embedding
BM25/FTS: 精确词、代码符号、术语
Kuzu/Neo4j/Graphiti: 实体、关系、时间事实
Object store: 原文和附件
  ↓
检索层
query 分类 → hybrid recall → graph expansion → rerank → context budget
  ↓
Agent 接入
REST / SDK / MCP tools: search, recall, remember, forget, cite, explain
```

**技术选型**
- 个人/小团队 PoC：`Postgres + pgvector + FTS + LangGraph + FastAPI/MCP`，最简单，运维少。 […]
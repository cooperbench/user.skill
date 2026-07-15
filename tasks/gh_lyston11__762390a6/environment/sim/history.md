> DEVELOPER

上网上、github等调研一下现在的agent知识库架构等
我需要搭建一个，你先给我好好调研一下

> AGENT

我会先用 `agent-reach` 的路由看一下可用的搜索/GitHub 调研方式，然后并行查官方资料、代表性开源项目和近期架构实践。这个问题我会按“可落地搭建”的口径整理，不只列名词。

> AGENT

我已经确认了本地的 `agent-reach` 技能入口；接下来会同时查“架构文章/官方文档”和“GitHub 上真实项目”。我会特别看：数据摄取、索引形态、检索编排、记忆模型、权限隔离、评测与运维这些能决定你之后怎么搭的部分。

> AGENT

第一批结果已经很有代表性：现在“Agent 知识库”已经不是单纯向量库了，主流在往长期记忆、混合检索、GraphRAG/时间图谱、MCP 工具化访问、评测闭环这几个方向合流。我还在补 GitHub 项目热度和官方文档细节，避免只凭营销页下判断。

> AGENT

GitHub 搜索能跑通了。我看到几个很强的信号：`microsoft/graphrag`、`HKUDS/LightRAG`、`topoteretes/cognee`、`mem0`/`Letta`/`Graphiti` 这类项目分别代表“图谱增强检索”和“Agent 长期记忆”两条主线；我会再读它们 README/文档确认能力边界。

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

> DEVELOPER

你先深度研究一下/user/lyston/raap项目，这个其中的数据都是db保存的，这个项目是文章生成类项目
现在就是想把这个项目agent化，然后对于他的前置数据包括：文章前置信息、活动品牌、内容、痛卖点等之前都是在db中用复杂的规则抽取出来组成提示词给到大模型生文
但是现在就是想把这个项目agent化
所以对于这些数据就要更好的结构化处理，所以才需要搭建agent知识库
目前构思是把这个知识库打造成能够和agent对接的api
知识库中要包含：文章例文、痛卖点等这些生文前置信息、文章的数据、文章的反馈等
文章例文最好是markdown+向量检索等方法，痛卖点、活动信息等前置信息最好还是采用db结构化等
所以采用什么技术、或者是开源项目等来搭建这个知识库？，你有没有好的方案或者想法

> AGENT

我先把 `/Users/lyston/PycharmProjects/raap` 当作主项目来读：看数据库模型、提示词拼装路径、文章生成流程、反馈/评审链路，再把它映射成可 Agent 化的知识库边界。不会改代码，先做架构调研和方案判断。

> AGENT

我先避开仓库里体积很大的 `vllm-0.19.0` 和缓存目录，聚焦 `src/raap_agent`、`data/demo`、`docs`、`tests`。刚才也注意到这个目录本身不是 git 仓库，所以我只读项目结构，不基于 git diff 判断历史。

> AGENT

从 README 和架构文档看，这个目录其实已经有一版“本地 scaffold 的 RAAP Agent 化实现”：FastAPI、LangGraph、多 Expert、Qdrant 可选、Memory/Learning/Template Store 都有雏形。现在我会往代码里追，区分“已经实现的抽象”和“真正迁到 DB/知识库时应该重做的边界”。

> AGENT

代码链路很清晰：Expert 现在每次都是 `build_query -> KnowledgeHub.search -> MemoryHub.search -> think -> AgentCard -> candidate_memory`，然后模板工厂、Writer、Review、Finalize 再发布记忆和学习信号。换句话说，真正要升级的是 KnowledgeHub/MemoryHub/Learning/Template/Trace 这些“文件+向量”实现，不是重写整个 Agent 工作流。

> AGENT

我把生成、审核、学习也连起来了：现有实现里“文章例文”主要走 `cases/style` namespace 检索，“痛卖点/品牌/活动”现在被当成普通 chunk 用 metadata 过滤，后置反馈则沉淀成 `TemplatePerformanceRecord`、`StylePatternRecord`、agent learning/reflection memory。你的直觉是对的：例文适合 Markdown+向量，痛卖点/活动/品牌规则应该结构化建模，不能都塞 chunk。

> AGENT

我再查一下项目里有没有真实 DB/ORM 接入痕迹，以及现在的文件型 store 都在哪些接口暴露。这样最终方案能分清“沿用现有 RAAP scaffold 的接口”与“接入你原业务 DB 的知识库服务”。

> AGENT

外部方案我也补了一轮官方资料：Cognee 明确是 relational/vector/graph 三存储组合，Graphiti 偏时间知识图谱，Mem0 偏通用 Agent memory，Qdrant/pgvector 分别是向量检索与 Postgres 内聚方案。结合 RAAP 的现有代码，我倾向不是直接套一个大框架，而是做一个 RAAP 专属 Knowledge Service。

> AGENT

我已经有足够上下文了，接下来会把方案收束成三层：RAAP 现状判断、知识库数据域设计、推荐技术路线。我会尽量给你一个能直接进入实施拆解的版本，而不是泛泛讲 RAG。

> TOOL

<turn_aborted>
The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed.
</turn_aborted>

> DEVELOPER

不，这个raap只是让你看看之前的数据的储存方法，但不采纳
就是应为不行所以才需要想方案搭建新知识库的

> AGENT

明白，我刚才把 `raap` 读成“可沿用的 scaffold”了，这个方向不对。现在我把它只当作反例和需求来源：旧系统的问题是“DB 规则抽取 + 拼 prompt”太硬、太分散、不可被 Agent 自主查询和组合，所以新方案应该独立搭一个面向 Agent 的 Knowledge Service。

> AGENT

对，这次我明白了：`raap` 不是要继承，而是说明“旧模式为什么不行”。新知识库应该是一个独立的 **Agent Knowledge Service**，旧 DB 只作为数据源之一，通过同步/清洗/结构化进入新知识层。

我的建议：**不要直接套 Dify/RAGFlow/Mem0/Cognee 当核心**，也不要再做“规则抽取后拼 prompt”。应该搭一个 RAAP 领域专属知识库，开源组件只作为底座。

**推荐架构**
```text
旧业务 DB / 文章库 / 反馈库 / Markdown 例文 / 人工标注
  ↓
Ingestion & Distillation
解析、清洗、去重、版本化、结构化抽取、embedding、审核
  ↓
Knowledge Core
Postgres: 结构化事实、品牌、活动、痛卖点、文章、反馈、版本、权限
Qdrant 或 pgvector: 文章例文/风格片段/反馈片段向量检索
Postgres FTS 或 OpenSearch: 关键词/BM25/精确词检索
可选 Graphiti/Neo4j/Kuzu: 痛点-卖点-产品-证据-禁忌的关系图谱
  ↓
Knowledge API / MCP Tools
Agent 只通过工具查知识，不直接拼 SQL，不直接拿旧 DB
  ↓
Writer / Planner / Reviewer Agents
拿到 evidence pack / material pack / memory pack，再生成文章
```

**我推荐的技术组合**
MVP：`Postgres + pgvector + FastAPI + SQLAlchemy/Alembic + worker`

中期生产：`Postgres + Qdrant + Postgres FTS/OpenSearch + FastAPI + MCP Server`

后期增强：加 `Graphiti` 或 `Neo4j/Kuzu` 做时间图谱和关系推理。

如果你文章量、例文量不是千万级，第一版可以先用 `Postgres + pgvector`，简单、事务一致、结构化和向量都在一起。等检索压力变大，再把向量独立到 Qdrant。

**数据应该这样分层**
1. **结构化知识**
   品牌、活动、产品、SKU、人群、平台、合规规则、痛点、卖点、证明材料、禁忌表达。

2. **半结构化知识**
   文章例文 Markdown、风格模板、优秀段落、开头方式、转折方式、收尾方式、人工点评。

3. **运行知识**
   每次生成任务、Agent 查询记录、命中的证据、生成稿、审核结果、人工反馈、最终发布结果。

4. **学习记忆**
   哪类文章通过率高、哪个痛点卖点组合好、某品牌某人群禁用什么、什么风格失败过。

**核心表建议**
```text
brands
products
campaigns
audience_segments
platform_rules
compliance_rules

pain_points
selling_points
pain_selling_maps
claim_evidences

article_examples
article_sections
knowledge_documents
knowledge_chunks
chunk_embeddings

article_runs
generated_articles
review_reports
feedback_events
style_patterns
agent_memories
```

痛卖点不要只做向量。应该结构化：

```text
pain_point:
  audience_segment
  scene
  pain_type
  emotional_trigger
  severity
  source

selling_point:
  product_id
  feature
  benefit
  proof
  claim_level
  risk_level

pain_selling_map:
  pain_point_id
  selling_point_id
  fit_score
  usage_context
  recommended_expression
  forbidden_expression
```

文章例文可以用 Markdown，但要拆成 section 和 chunk：

```text
article_example:
  title
  brand
  platform
  audience
  style_tags
  outcome_score
  markdown_body

article_section:
  article_id
  section_type: hook / scene / pain / product_bridge / proof / cta
  markdown
  quality_score
``` […]

> DEVELOPER

给我写一个非常详细的开发文档看看

> AGENT

我会用 `codex-md-docs` 来写这份开发文档，因为这是 Markdown 文档类工作；我先看一下它要求的存放/组织方式，然后给你一版可以直接落地评审的详细文档。

> AGENT

我会把它写成一份独立的 Markdown 开发文档，放到你的 Codex Obsidian 文档空间里，而不是塞回 `raap` 项目源码。内容会按“新建 Agent 知识库服务”的方向写，明确旧 DB 只是数据源，不采纳旧 `raap` 的存储实现。

> AGENT

我找到了本机文档空间里已有的 `lystonmacbook-pro.local/锐鲨` 分类，里面已经有 RAAP V2 相关笔记；这次我会新建一份聚焦“Agent 知识库服务”的开发方案，避免和旧工作流说明混在一起。

> AGENT

我准备写入新文件：`/Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md`。文档会把旧 `raap` 的文件型/规则型做法明确标为“不采纳”，然后给出新服务的目标架构、表结构、API、检索链路、MCP 工具、数据同步和分期落地。

> AGENT

写好了，新建在：

[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

我放在 `lystonmacbook-pro.local/锐鲨` 下，因为这是本机环境里已有的 RAAP/锐鲨相关文档分类。文档明确把旧 `raap` 项目作为“问题来源/旧数据形态参考”，不采纳它的存储实现；主体是全新的 Agent Knowledge Service 方案，包含技术选型、总体架构、核心数据域、Postgres 表设计、Context Pack API、MCP 工具、Ingestion 同步、Agent 使用流程、评测体系、部署方案和分期开发计划。

> DEVELOPER

1.不从旧db抽取数据，那不是这个知识库需要考虑的事，你只需要考虑知识库的搭建
2.api封装接口非常重要，和各种数据管理同样重要，api要非常清晰，要考虑到未来的数据扩展

> AGENT

收到，这两个点很关键：我会把文档从“旧 DB 迁移/同步方案”改成“独立知识库产品/服务搭建方案”，并把 API 设计提升成核心章节，按资源模型、版本、扩展字段、查询协议、Agent 工具协议来写清楚。

> AGENT

我会直接更新刚才那份文档：删掉“旧 DB 同步/抽取”作为知识库职责的内容，改成“知识库本身的数据管理能力”；同时把 API 协议扩成一等设计对象，包含资源型 CRUD、检索型 API、Context Pack、Agent/MCP、版本扩展和响应 envelope。

> AGENT

文档已经按你的两个要求重写了：旧 DB/抽取/同步从核心职责里拿掉了；API 章节大幅增强，现在把 API 分成资源管理、检索、Context Pack、Agent/MCP、后台管理和扩展策略几层。

> AGENT

已按你的两点重写文档：

[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

主要改动：

- 明确写入边界：知识库不负责旧 DB 同步、旧数据抽取、旧 prompt 规则迁移，只负责知识库本身的搭建、管理、检索和对外服务。
- 把 API 提升为核心设计：新增/强化了 API 总则、响应 envelope、分页过滤、幂等写入、扩展字段、资源管理 API、检索 API、Context Pack API、Agent API、MCP tools、批量管理、校验、reindex、审核流和 API 扩展策略。
- 文档现在是 2070 行，偏完整开发规格，可以继续往 OpenAPI schema、ER 图或任务拆解方向展开。

> DEVELOPER

不仅有痛卖点啊，肯定不能为了某一个特殊的关键字设立单独的api啊
只是我之前让你阅读raap的原因就在这，因为这个raap中我们就有很多这样的数据是这么保存的，你得了解并思考哪些是需要这样结构化db存储的，要必须要支持可扩展性

> AGENT

你说得对，我上一版还是把“痛卖点”写得太像特例了。我要把它改成“可扩展知识类型系统”：痛卖点只是其中一种 typed knowledge，不应该有一堆为单个关键词定制的 API。RAAP 里那些品牌、活动、平台规则、合规、产品、结构、故事、拟人化、人群、反馈都应该纳入统一结构化模型。

> AGENT

完全同意，这里应该抽象成“可扩展的 typed knowledge 系统”，而不是为痛点、卖点这种单个概念写死表和 API。我的修订方向是：品牌/活动/产品/平台/人群/文章这类作为稳定 scope anchor，其他前置信息、规则、素材、痛点、卖点、结构、故事、人设、反馈洞察等都作为 `knowledge_type + knowledge_item + relation` 来管理。

> AGENT

我会把文档再重构一次：删掉那些专门的 `pain-points` / `selling-points` / `pain-selling` 资源 API，把它们收敛为通用 `knowledge_types`、`knowledge_items`、`knowledge_relations`。这样未来新增“人设、故事素材、结构模式、活动限制、卖点证明、合规规则、风格偏好”等，都只是新增知识类型和 schema，不需要改 API 形态。

> AGENT

我已经把文档重构为 “Typed Knowledge” 方案：稳定实体 + 可扩展知识类型 + 知识项 + 知识关系 + chunk + context pack。痛点、卖点、活动规则、品牌规则、故事、人设、结构、反馈都变成配置化知识类型，不再有为单个业务词膨胀出来的专用 API。

> AGENT

对，这次我把文档方向改正了：现在不再围绕“痛卖点”建专用表和专用 API，而是改成 **Typed Knowledge 可扩展知识类型系统**。

已更新这里：

[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

现在核心抽象变成：

```text
Entity = 稳定范围和归属，比如品牌、活动、产品、平台、人群、文章
KnowledgeType = 可配置知识类型，比如品牌规则、活动事实、人设、故事、结构、痛点、卖点、反馈
KnowledgeItem = 具体知识项
KnowledgeRelation = 知识之间的关系，比如 supports / addresses / forbids / example_of
KnowledgeChunk = 可检索文本片段
ContextPack = 面向 Agent 的知识组合结果
```

也就是说，痛点、卖点、活动规则、品牌规则、平台规则、合规限制、故事素材、人设、结构模式、拟人化规则、文章例文、反馈经验都进入同一套体系。未来新增类型，只需要注册 `knowledge_type`、配置 JSON Schema、索引字段、关系规则和 context pack slot，不需要新增特殊 API。

我也把 API 收敛成通用接口了，比如：

```text
POST /api/v1/knowledge-types
POST /api/v1/knowledge-items
POST /api/v1/knowledge-items/query
POST /api/v1/knowledge-relations
POST /api/v1/knowledge-relations/expand
POST /api/v1/search
POST /api/v1/context-packs
POST /api/v1/agent/search
POST /api/v1/agent/propose-knowledge
```

文档里还保留了“不推荐 `/pain-points`、`/selling-points`、`/pain-selling` 这种专用 API”的反例，用来明确架构边界。

> DEVELOPER

我不是说了吗，文章例文要和这些结构化数据分开来
一个是markdown+向量检索，一个是db
你思考下

> TOOL

<turn_aborted>
The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed.
</turn_aborted>

> DEVELOPER

我不是说了吗，文章例文要和这些结构化数据分开来
一个是markdown+向量检索，一个是db
你思考下

因为文章例文就是市面上那些好的文章然后会被我们收纳进来作为例文，以供给agent作为某种结构或者风格的参考呀

> AGENT

我明白你的意思了：这里其实是两套知识形态，不能强行塞进同一个 `knowledge_items + chunk` 模型里。我会按“例文语料库”和“结构化业务知识库”分层重构设计，再把 Agent API 做成统一编排层，而不是统一存储层。

> AGENT

我会先把现有文档里“统一模型”的部分定位出来，然后改成更清楚的双库架构：例文库负责 Markdown 原文、分块、向量与风格/结构参考检索；结构化知识库负责品牌、活动、卖点、约束、反馈等可扩展业务事实。API 层再做统一查询和 Context Pack 编排。

> AGENT

这次我会把文档里的核心抽象改掉，而不只是措辞修补：`Example Corpus` 和 `Structured Knowledge DB` 分开建模，Context Pack 只做聚合，不假装二者是同一种存储对象。这样例文能按“结构、风格、段落作用、行业、平台、受众”检索，业务知识仍然按强 schema 管理。

> AGENT

我已经确认现有文档的主要问题：它虽然强调了“不要按痛卖点建 API”，但仍把例文作为 `article_example` 混在通用知识项里，容易导致架构误解。接下来我会直接重写关键章节，让“例文库”和“结构化库”在数据库、API、检索、管理后台、MVP 阶段都各自清楚。

> AGENT

改稿已经完成在临时文件里了，核心结构现在是“Structured Knowledge DB + Example Corpus + Cross-store Links + Context Pack”。我还会做一次快速检查，避免残留旧的 `knowledge_items/article_example` 混合表述，然后再写回你的 Obsidian 文档。

> AGENT

已经写回正式文档了。我再做最后一轮文件级校验：确认行数、关键标题、以及是否仍然存在会让人误会“例文和结构化数据同库”的旧表述。

> AGENT

已按你的思路重写并写回文档了：  
[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

这版核心改成了清晰的双库架构：

- `Example Corpus`：文章例文单独作为 Markdown + section + chunk + 向量检索体系，专门给 Agent 做结构、风格、段落写法参考。
- `Structured Knowledge DB`：品牌、活动、产品、痛点、利益点、平台规则、合规、反馈洞察等走 DB + JSON Schema + 关系 + 审核。
- 中间用 `KnowledgeCorpusLink` 做跨库引用，不把例文误当业务事实。
- Agent 侧通过 `Context Pack / Federated Search / Agent API` 统一使用，但返回时明确区分 `structured` 和 `example_corpus` 来源。

文档现在约 3343 行，补了数据库表、API、Context Pack、MCP、检索策略、后台管理、数据质量、分期开发、MVP API 和代码结构。第 31 节也放了调研参考，包括 [pgvector](https://github.com/pgvector/pgvector)、[Qdrant Payload](https://qdrant.tech/documentation/concepts/payload/)、[Dify External Knowledge Base](https://docs.dify.ai/en/use-dify/knowledge/connect-external-knowledge-base) 等。下一步最适合从这份文档拆出一版正式 `OpenAPI` 契约和首批数据库 migration 设计。

> DEVELOPER

还要好好思考怎么做版本管理？你先思考一下思路和我说说

> AGENT

这个问题很关键，我先不改文档，先把版本管理的设计思路摊开。这里的版本不是简单“有个 history 表”，而是要保证 Agent 生文可复现、知识可回滚、例文索引可重建、规则变更可追责。

> AGENT

我觉得版本管理要按“四条线”设计，不能只做一个 `revision` 表糊上去。

**核心原则**

每个知识对象都要分清两个 ID：

```text
logical_id：这个知识的稳定身份
revision_id：某一次不可变版本
```

Agent 默认读的是“当前已发布版本”，但每次生成文章时，必须把当时用到的具体 `revision_id / document_version_id / chunk_hash` 记录下来。这样以后文章出了问题，能知道当时到底用了哪条活动规则、哪版例文、哪版 Context Pack。

**1. 结构化知识版本**

结构化数据，比如品牌规则、活动信息、产品利益点、用户痛点、合规规则，应该是：

```text
structured_item_id 稳定不变
structured_item_revision_id 每次内容变更生成新版本
```

已发布内容不能原地覆盖。修改一个 published item 时，应该创建一个 draft revision：

```text
v1 published
  -> 编辑
v2 draft
  -> 审核通过
v2 published，v1 仍可追溯
```

查询默认只返回：

```text
status = published
valid_from <= now
valid_until is null or valid_until > now
```

这里要特别区分两个概念：

```text
revision version：知识内容第几版
valid time：业务上什么时候生效
```

比如活动规则 `v3` 可以在 2026-06-01 才生效，不能因为它已经发布就立刻被 Agent 用到。

**2. 例文语料版本**

例文更复杂。因为一篇 Markdown 改了以后，section、chunk、embedding 都会变化。

所以例文不要只 version document，还要让 section/chunk 绑定到具体 document version：

```text
corpus_document_id
corpus_document_version_id
corpus_section_id
corpus_chunk_id
content_hash
embedding_model
chunk_policy_version
```

也就是说：

```text
例文 A v1
  -> parse 得到 sections v1
  -> chunk 得到 chunks v1
  -> embedding 得到 vectors v1

例文 A Markdown 修改
  -> 生成 document v2
  -> 重新 parse/chunk/embed
  -> v1 的 section/chunk 仍保留，用于历史追溯
```

这样才能复现以前某篇文章生成时参考过的例文段落。

**3. Context Pack 版本**

这个最重要。

每次 Agent 生成文章前拿到的 Context Pack，都必须是不可变快照。里面至少记录：

```text
context_pack_run_id
template_code + template_version
request_payload
resolved scope
structured item revision ids
corpus document version ids
section/chunk ids
content hashes
retrieval query
filters
scores
reranker version
embedding model
token budget
final selected snippets
```

最好不仅记录引用，还保存当时实际返回给 Agent 的摘要/片段快照。因为未来原知识可能被归档、修正或删除，只靠引用不一定能完整复现。

文章生成结果也要引用：

```text
generated_article.context_pack_run_id
prompt_version
agent_version
model_version
```

否则后面反馈“这篇为什么写错了”，根本查不清是知识错、检索错、模板错，还是模型发挥错。

**4. Schema / 模板 / 索引版本**

还有一类容易漏：配置本身也要版本化。 […]

> DEVELOPER

不仅要考虑当前mvp的开发
还有后续的，包括支持可扩展性等

写入文档

很多地方都需要补充流程图

> AGENT

我会把“版本管理”从一个生命周期小节提升成独立的架构章节，并补上多处 Mermaid 流程图：结构化知识发布、例文 Markdown 到向量索引、Context Pack 快照、Schema/模板演进、回滚和迁移。这个点确实要按长期可扩展设计，不只是 MVP history 表。

> AGENT

我先在临时副本里改，确认结构和残留引用没问题再写回正式 Obsidian 文档。版本管理会覆盖对象版本、有效期、快照、索引版本、Schema 版本、长期迁移策略和审计追溯。

> AGENT

我会先把最容易出问题的几处补齐：领域模型里的版本对象、数据库里的版本字段和版本表、例文入库流程图、Context Pack 生成流程图、检索流程图、以及一个完整的长期版本治理章节。这样文档不仅能指导 MVP，也能避免后续扩展时推倒重来。

> AGENT

我现在开始动文档主体：一处是数据库表结构，补版本表和版本字段；一处是版本管理章节，把它从“小生命周期说明”扩成长期架构。还会在已有架构、例文、Context Pack、检索、分期开发处补流程图，不只是最后加一段说明。

> AGENT

数据库部分已经补了长期版本字段：`structured_type_definitions`、`corpus_collection_versions`、`context_pack_template_versions`、`index_jobs`，并且让 section/chunk 明确绑定 `document_version_id`。接下来补 Context Pack 和检索流程图，再重写“版本与生命周期”章节。

> AGENT

版本管理章节已经扩成长期架构了，不只是 MVP。它现在包含双时间模型、schema 演进、例文索引版本、Context Pack 快照、回滚、归档和长期路线。接下来我会把分期开发和最小 API 也同步补一下，不然文档前后会有点脱节。

> AGENT

我已经同步了 MVP API、代码结构和实现注意事项，让版本能力不只停留在理论章节。现在做校验：看标题层级是否顺，旧编号有没有破，关键表和流程图是否都能搜到。

> AGENT

校验结果看起来是顺的：文档现在从 3343 行扩到 4043 行，新增了 10 多处 Mermaid 图和版本相关表。为了让版本管理可落地，我再补一小段“Version API / Replay API”说明，然后写回正式文档。

> AGENT

最后校验通过，文档现在有 4101 行，流程图从 3 个左右扩到了 14 个，版本管理章节也补到了可实施粒度。我会把临时版本写回正式 Obsidian 文件。

> AGENT

已写入文档：  
[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

这次重点补了两块：

1. **长期版本管理设计**  
   新增独立章节 `24. 版本管理与生命周期`，覆盖：
   - logical id / revision id / current pointer
   - `system_time` 与 `business_valid_time`
   - 结构化知识发布、回滚、Schema 演进
   - 例文 Markdown 版本、section/chunk/embedding 版本
   - Context Pack 不可变快照
   - 索引版本、向量重建、灰度与回滚
   - Version API、replay、compare

2. **大量流程图补充**  
   文档现在有 14 个 Mermaid 图，补在关键位置：
   - Agent 获取上下文流程
   - 领域模型 ER 图
   - 例文入库与索引流程
   - Context Pack 生成流程
   - 结构化检索流程
   - 例文检索流程
   - 结构化知识发布/回滚流程
   - Schema 演进流程
   - Corpus 生命周期
   - 索引升级和回滚流程

同时也同步更新了表结构、MVP API、开发分期和代码结构，例如新增 `structured_type_definitions`、`corpus_collection_versions`、`context_pack_template_versions`、`index_jobs` 等，避免版本管理只是“文档概念”，后续可以直接落到开发任务里。

> DEVELOPER

只保留开发文档啊

> AGENT

明白，你的意思是不要拆成一堆调研稿、版本稿、补充说明，最终只保留那一份正式开发文档。我先确认一下锐鲨目录里有没有我额外留下的同主题文档或临时副本，有的话只保留主文档。

> AGENT

我在正式锐鲨目录里只找到这一份同主题 Markdown。临时副本还在 `/private/tmp`，我把它清掉，最终只留 Obsidian 里的正式开发文档。

> AGENT

已处理。

现在同主题只保留这一份正式开发文档：  
[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

临时副本 `/private/tmp/RAAP_Agent_KB_doc.md` 已清理。锐鲨目录里另外两份是之前的 RAAP V2 工作流/面试材料，不是这次知识库开发文档，我没有动。

> DEVELOPER

api调用是不是还要考虑到管理后台的接口调用啊，封装的不好管理后台调用就很乱

> AGENT

对，这个点必须补进去。知识库 API 不能只按 Agent 调用设计，管理后台是高频、复杂、带状态流转的调用方，如果没有专门的 Admin API/BFF 封装，前端会被迫拼很多底层接口，最后会很乱。

> AGENT

我会把这个补成文档里的正式设计：API 不是只有 Resource API 和 Agent API，还要有专门的 Admin BFF/use-case API。后台页面需要拿“页面状态包”，不是让前端自己连调 8 个接口拼表单、权限、schema、版本、校验和任务状态。

> AGENT

我已经把 Admin BFF 的原则、页面 API 映射、编辑页响应示例和状态流转图补进去了。下一步把 MVP API 列表和代码结构同步一下，避免开发时只实现 Resource API，后台还得自己乱拼。

> AGENT

Admin API 相关内容已经补进了设计、分期和实现注意事项。现在我做一次结构校验，确认章节编号、Admin 接口、流程图都在文档里，然后写回正式文件。

> AGENT

校验没问题，Admin BFF 已经贯穿设计原则、后台章节、MVP API、分期和代码结构。我现在写回正式开发文档，并清理临时副本。

> AGENT

对，这个必须考虑。我已经写入开发文档了：  
[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

这次新增了 **Admin API / Admin BFF** 的设计，核心思想是：

- `Resource API`：稳定资源接口，比如 `/structured/items`、`/example-corpus/documents`
- `Agent API`：给 Agent 的任务接口，比如 `/agent/context`
- `Admin API / BFF`：给管理后台页面的组合接口，比如 `/admin/structured/items/{id}/edit-view`

重点补了：

- 管理后台 API 原则
- 后台页面与 API 映射表
- 结构化知识编辑页 `edit-view` 响应示例
- 例文编辑页 `edit-view` 响应示例
- 后台状态流转流程图
- Admin API 和 Resource API 的边界
- MVP API 中新增 `/api/v1/admin/*`
- 代码结构新增 `admin_structured.py`、`admin_corpus.py`、`admin_context.py`、`admin_search.py` 等

文档现在明确写了：后台前端不应该自己连调很多底层接口拼页面，而是优先调用 Admin BFF，由后端一次返回页面所需的 `data / schemas / permissions / available_actions / validation / jobs / warnings`。这样后续扩展知识类型、版本、审核、索引任务时，管理后台不会散。

> DEVELOPER

和我讲讲现在的api接口是怎么样的

> AGENT

现在这套 API 不是按“痛点、卖点、品牌、活动”这种业务词拆，而是按 **调用方 + 知识形态** 拆。

核心分 5 层：

```text
1. Resource API
   底层稳定资源接口，负责真正的数据 CRUD、查询、版本、关系。

2. Admin API / Admin BFF
   给管理后台页面用的组合接口，避免前端乱拼接口。

3. Agent API
   给 Agent 用的任务接口，输入更自然，输出 context/search/proposal。

4. Federated Search API
   联邦搜索，同时查结构化库和例文库，但返回来源分开。

5. Context Pack API
   组装 Agent 写文章前需要的完整上下文包。
```

文档在这里：  
[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

**1. Resource API**

这是最底层、最稳定的 API，面向资源模型。

结构化知识：

```http
POST /api/v1/structured/types
GET  /api/v1/structured/types

POST /api/v1/structured/items
GET  /api/v1/structured/items/{id}
POST /api/v1/structured/items/query
PATCH /api/v1/structured/items/{id}

GET  /api/v1/structured/items/{id}/revisions
POST /api/v1/structured/items/{id}/revisions
POST /api/v1/structured/items/{id}/publish
POST /api/v1/structured/items/{id}/rollback

POST /api/v1/structured/relations
POST /api/v1/structured/relations/expand
```

例文语料库：

```http
POST /api/v1/example-corpus/collections
POST /api/v1/example-corpus/documents
PUT  /api/v1/example-corpus/documents/{id}/markdown
POST /api/v1/example-corpus/documents/{id}/process
GET  /api/v1/example-corpus/documents/{id}
GET  /api/v1/example-corpus/documents/{id}/versions

POST /api/v1/example-corpus/sections/query
POST /api/v1/example-corpus/search
```

这层的特点是干净、正交、稳定。比如新增“用户顾虑”“平台偏好”“证明材料”，不是新增 `/user-objections`，而是新增 `structured_type`，继续复用 `/structured/items`。

**2. Admin API / Admin BFF**

这是给管理后台用的，不让前端自己连调很多底层接口。

比如结构化知识编辑页，不应该让前端自己调用：

```text
item
revision
type schema
ui schema
relations
linked corpus
permissions
validation
audit logs
jobs
```

而是一个接口直接返回页面状态包：

```http
GET /api/v1/admin/structured/items/{id}/edit-view
```

返回大概是：

```json
{
  "data": {
    "item": {},
    "current_revision": {},
    "draft_revision": null,
    "relations": [],
    "linked_corpus_sections": []
  },
  "schemas": {
    "json_schema": {},
    "ui_schema": {}
  },
  "permissions": {
    "can_edit": true,
    "can_publish": false
  },
  "available_actions": [
    "create_draft_revision",
    "submit_review",
    "archive"
  ],
  "validation": {
    "status": "passed",
    "issues": []
  },
  "warnings": []
}
```

后台相关接口现在设计为：

```http
POST /api/v1/admin/structured/items/list-view
GET  /api/v1/admin/structured/items/{id}/edit-view
GET  /api/v1/admin/structured/items/{id}/review-view
GET  /api/v1/admin/structured/types/{code}/designer-view

POST /api/v1/admin/corpus/documents/list-view
GET  /api/v1/admin/corpus/documents/{id}/edit-view
GET  /api/v1/admin/corpus/documents/{id}/annotation-view
GET  /api/v1/admin/corpus/documents/{id}/index-view

POST /api/v1/admin/context-packs/preview […]

> DEVELOPER

文档写清楚了吗？

> AGENT

我快速核一下文档里的关键章节是否都落到了同一份开发文档里，然后直接给你判断：哪些已经清楚，哪些如果要进入开发还建议再拆成更细的 OpenAPI/任务单。

> AGENT

写清楚了，而且已经集中在唯一这份开发文档里：

[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

我刚核了一遍，文档现在 4466 行，关键点都已经落进去：

- 双库架构：`Example Corpus` 和 `Structured Knowledge DB` 分开。
- API 分层：`Resource API`、`Admin API / BFF`、`Agent API`、`Federated Search API`、`Context Pack API`。
- 管理后台接口：专门有第 21 章，写了后台 API 原则、页面映射、`edit-view` 示例、状态流转、和 Resource API 边界。
- 版本管理：第 24 章，写了结构化知识、例文、Context Pack、Schema、索引、回滚、replay/compare。
- MVP API：第 28 章集中列了第一版接口。
- 代码结构：第 29 章列了推荐模块。
- 流程图：上下文获取、例文入库、Context Pack、检索、版本发布/回滚、后台状态流转等都有 Mermaid 图。

如果接下来要进入开发，下一步就不是继续扩这篇大文档了，而是从它拆出两份执行级材料：`OpenAPI 接口契约` 和 `Phase 1 开发任务清单`。这份现在已经适合作为总设计文档。

> DEVELOPER

我觉得具体的知识库选型你还要好好调研一下，看看有没有好的开源项目等，不只是盯着非常出名的那些开源项目
多上网看看

> AGENT

你这个判断是对的：之前文档里的选型更像“常规 RAG 技术栈建议”，还不够像真正为这个知识库挑底座。我要重新从“能不能承载结构化知识管理 + 例文语料检索 + 管理后台 + API 扩展”这个角度去查开源项目，不只看 Dify/RAGFlow 这几个大名。

> AGENT

我查到几个之前文档里没认真展开的方向：Directus/Payload/MDCMS 这类“结构化内容管理底座”，Infinity/ParadeDB/LanceDB 这类非典型检索底座，以及 Kuzu/FalkorDB 这类图数据库。现在我把调研结论收敛成“哪些能直接用、哪些只能参考、哪些不适合当核心”，然后写回唯一那份开发文档。

> AGENT

我继续按“能不能作为知识库底座”而不是“是不是 RAG 项目”来调研。现在会重点补三类候选：结构化管理底座（Directus/Payload/NocoDB/Baserow/MDCMS）、例文检索底座（Qdrant/Weaviate/Milvus/LanceDB/Infinity/ParadeDB/Vespa）、RAG 应用可借鉴项目（Khoj/Kotaemon/AnythingLLM/Quivr/Docling 等）。

> AGENT

调研下来，一个很重要的结论是：最像“知识库底座”的反而不是 RAG 应用，而是 Headless CMS / Data Platform / Search Engine 这几类。RAG 应用能借鉴检索和上传文档，但很难承载你要的结构化类型、版本、审核、后台页面和 Agent API。

> AGENT

我已经把技术选型章节从原来一小段扩成完整调研结论了，加入了很多不只是 Dify/RAGFlow 的候选。现在我会补参考资料章节里的链接，让这些选型有出处，然后再校验写回。

> AGENT

选型章节和参考链接都补完了。我现在做一次校验，看新增候选是否都在文档里，然后写回正式开发文档。

> AGENT

校验通过，技术选型章节现在已经从“简单推荐栈”扩展成完整调研小节了。我写回正式文档，并保留只这一份开发文档。

> AGENT

你说得对，我已经重新做了一轮更广的选型调研，并写回唯一那份开发文档了：  
[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

这次不是只看 Dify/RAGFlow，而是按几类底座重新整理了：

- **结构化管理底座**：Directus、Payload CMS、Strapi、NocoDB、Baserow、Teable、Appsmith/ToolJet/Budibase、MDCMS
- **例文检索/搜索底座**：pgvector、Qdrant、Weaviate、Milvus、LanceDB、Chroma、Infinity、ParadeDB、OpenSearch、Vespa
- **RAG/Knowledge App 借鉴项目**：Dify、RAGFlow、AnythingLLM、Kotaemon、Quivr、Khoj、Verba、DocsGPT、txtai、LlamaIndex、Haystack、LangChain
- **文档解析**：Docling、marker、Unstructured、Jina Reader、trafilatura
- **图谱/时间知识**：KuzuDB、FalkorDB、Apache AGE、Neo4j、Graphiti、LightRAG

结论也写清楚了：

- 不建议把完整知识库交给一个 RAG App。
- MVP 仍建议 `FastAPI + PostgreSQL + pgvector + MinIO + Redis`，因为最贴合自定义 schema、版本、审核、Context Pack。
- 需要并行 POC 三件事：
  - Directus 是否适合承载结构化知识后台。
  - Qdrant vs Infinity vs pgvector 的例文检索质量。
  - Docling/marker 是否要进入导入 pipeline。
- 生产第一版更稳的路线是：`PostgreSQL 做结构化主库 + Qdrant 做例文向量库 + ParadeDB/OpenSearch 做关键词增强 + 自研 Context Pack 和 Admin BFF`。

参考资料章节也补了这些项目的链接。文档现在 4749 行，临时副本已清理，只保留正式开发文档。

> DEVELOPER

你别给我说什么第一版第二版，在文档中我要的就是完整的技术方案

lightrag可以作为我们的召回实现方案吗？合适吗？

> AGENT

明白，我会把文档里的“第一版/生产版/路线 A/B/C”这种阶段化口吻改成“完整技术方案 + 可选组件决策”，并单独补一节 LightRAG 是否适合作为召回层。LightRAG 这个点我会先查最新项目能力再判断，不凭印象拍板。

> AGENT

我查了 LightRAG 的官方仓库和核心文档后，结论比较明确：它可以作为“召回实现候选”，尤其是图增强召回，但不适合作为整个知识库底座，也不应该直接接管结构化事实库。我会把文档里阶段化的“第一版/第二版”口吻改成完整方案，并补一个 LightRAG 召回方案章节。

> TOOL

<turn_aborted>
The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed.
</turn_aborted>

> DEVELOPER

你这么着急干嘛，你先和我说说啊

> AGENT

对，我刚才急了。先不写文档，先把判断讲清楚。

我的结论是：

**LightRAG 可以作为召回实现方案的一部分，但不适合作为整个知识库底座，也不适合作为结构化业务知识的主召回。**

更准确地说：

```text
LightRAG 适合：
  例文语料库的图增强召回
  长文本文章之间的跨段落关联召回
  风格、场景、结构、主题关系召回
  反馈经验、文章模式、故事素材的关联发现

LightRAG 不适合：
  品牌规则主库
  活动事实主库
  合规规则主库
  痛点/卖点/利益声明这类强 schema 结构化知识主库
  管理后台的数据治理底座
```

LightRAG 本质上是 **Graph-enhanced RAG**，官方项目也强调它把图结构引入索引和检索流程，支持知识图谱、API/WebUI、citation、文档删除后图谱更新、多种存储后端等能力。这个方向对“例文召回”是有价值的，尤其适合解决普通向量召回不擅长的东西，比如“这篇文章的结构像不像那种先场景后转产品的写法”。参考：[LightRAG GitHub](https://github.com/HKUDS/LightRAG)、[LightRAG paper](https://arxiv.org/abs/2410.05779)。

但它的问题也很明显：它的图谱是从文本里抽取出来的，适合“辅助理解和召回”，不适合做“权威业务事实”。比如活动截止时间、品牌禁用词、合规禁忌、利益点风险等级，这些不能让 LightRAG 自动抽取后变成事实来源。这里必须是 DB + schema + 审核 + 版本。

我会这么设计它的位置：

```text
Structured Knowledge DB
  -> 精确召回
  -> scope 过滤
  -> valid_at/as_of
  -> 版本和审核
  -> hard constraints / business materials

Example Corpus
  -> Markdown 原文
  -> section/chunk
  -> metadata filter
  -> vector/BM25 search
  -> LightRAG graph recall
  -> rerank
  -> style/structure examples
```

也就是说，LightRAG 可以作为 `Example Corpus` 下面的一个召回 provider：

```text
SearchService
  structured_exact_retriever
  corpus_vector_retriever
  corpus_bm25_retriever
  corpus_lightrag_graph_retriever
  link_expansion_retriever
  reranker
```

Agent 查 Context Pack 时：

```text
hard_constraints:
  只走 Structured DB

business_materials:
  只走 Structured DB + relation expansion

style_examples / structure_examples:
  走 Example Corpus
  可以混合 vector + BM25 + LightRAG

feedback_memory:
  主要走 Structured DB
  如果反馈沉淀成文本经验，也可以辅助走 LightRAG
```

我觉得 LightRAG 最适合的场景是这些：

```text
“找几篇结构类似的优秀例文”
“找生活场景到产品转场比较自然的段落”
“找和这个用户情绪/场景有关的文章片段”
“找同一种叙事结构下不同平台的表达差异”
“找某类失败反馈背后常见的写法模式”
```

不适合这些：

```text
“这个活动必须写什么”
“这个产品能不能说改善睡眠”
“这个品牌有哪些禁用表达”
“这条利益点对应哪个合规风险”
“今天生效的是哪版规则”
```

所以，完整技术方案里我会把 LightRAG 写成：

```text
可选但值得 POC 的图增强召回组件。
不是主库。
不是唯一召回。
不是结构化事实来源。
```

判断它是否正式采用，要做几个 POC：

1. **metadata filter 能力**  
   能不能稳定按 `platform / industry / topic / section_type / rights_status / quality_score` 过滤。

2. **citation 映射能力**  
   返回结果能不能映射回我们自己的 `document_version_id / section_id / chunk_id`。

3. **版本兼容能力**  
   Markdown 更新后，它能不能干净地重建图谱，并保留历史 Context Pack 的可追溯性。

4. **召回质量**  
   和 `Qdrant […]

> DEVELOPER

结构化数据你是打算怎么处理的？db

> AGENT

对，结构化数据我建议明确用 **PostgreSQL 做权威主库**，不是 LightRAG，也不是向量库。

结构化数据包括这些：

```text
品牌规则
活动信息
产品信息
利益点声明
用户痛点
使用场景
人群洞察
平台规则
合规规则
写作策略
反馈洞察
审核规则
```

它们的共同特点是：需要准确、可审核、可过滤、可版本化、可追溯。所以应该走 DB。

核心设计是这样：

```text
PostgreSQL
  entity_types
  entities
  structured_types
  structured_type_definitions
  structured_items
  structured_item_revisions
  relation_types
  structured_relations
```

其中最重要的是三层：

```text
Entity
  稳定业务对象，比如 brand、campaign、product、platform、audience。

StructuredType
  可扩展知识类型，比如 user_pain、benefit_claim、campaign_constraint。

StructuredItem
  某一条具体知识，比如“活动资格必须说明”。
```

举个例子。

用户痛点不是单独建一个 `/pain-points` 表，而是注册一个类型：

```json
{
  "code": "user_pain",
  "name": "用户痛点",
  "json_schema": {
    "type": "object",
    "required": ["scene", "pain_text"],
    "properties": {
      "scene": {"type": "string"},
      "pain_text": {"type": "string"},
      "emotional_trigger": {"type": "string"},
      "severity": {"type": "integer"}
    }
  }
}
```

然后具体数据存在 `structured_items`：

```json
{
  "type_code": "user_pain",
  "title": "夜间哄睡疲惫",
  "payload": {
    "scene": "夜间哄睡",
    "pain_text": "新手妈妈夜里反复醒来，担心宝宝睡不好",
    "emotional_trigger": "疲惫、不确定、担心",
    "severity": 4
  },
  "scope": {
    "brand": ["brand_uuid"],
    "platform": ["xiaohongshu"],
    "audience_segment": ["new_mother_uuid"]
  },
  "status": "published"
}
```

这样未来新增“用户顾虑”“证明材料”“平台偏好”“风险表达”，不需要新 API，也不一定要新表，只要新增 `structured_type`。

**为什么不用向量库存这些？**

因为这些不是“相似文本召回”优先，而是“准确过滤和权威引用”优先。

比如 Agent 写文章前查活动约束：

```text
brand = A
campaign = B
platform = xiaohongshu
valid_at = 今天
status = published
type_code in campaign_constraint, compliance_rule
```

这必须是 DB 精确查询，不能靠语义相似。

**结构化数据的关系也在 DB**

例如：

```text
benefit_claim --addresses--> user_pain
benefit_claim --supported_by--> proof_point
compliance_rule --forbids--> benefit_claim
campaign_constraint --applies_to--> campaign
hook_pattern --illustrated_by--> corpus_section
```

关系表大概是：

```text
structured_relations
  source_item_id
  target_item_id
  relation_type
  strength
  payload
  status
```

如果是结构化知识和例文之间的关系，则走：

```text
knowledge_corpus_links
  structured_item_id
  corpus_document_id
  corpus_section_id
  link_type
```

也就是说：

```text
结构化知识之间的关系：structured_relations
结构化知识和例文之间的关系：knowledge_corpus_links
```

**版本管理**

结构化数据不能原地覆盖，要有 revision：

```text
structured_items
  当前逻辑对象

structured_item_revisions
  每次修改的不可变版本
```

比如：

```text
活动限制 v1 published […]

> DEVELOPER

可以，并且还要好好想想 feedback_memory怎么处理

> AGENT

对，feedback_memory 是 Agent 化里很容易做坏的一块。我先不写文档，先把处理思路讲清楚：它不能是“把所有反馈丢进向量库”，而应该是从原始反馈到可复用经验的一条受控流水线。

> AGENT

可以，`feedback_memory` 我建议单独认真设计。它不是一个简单知识类型，而是一条 **反馈沉淀系统**。

核心判断：

```text
原始反馈不能直接成为 Agent memory。
Agent memory 必须是经过聚合、归因、审核、版本化后的可复用经验。
```

否则会很危险。比如某个编辑随口说“这篇太软了”，如果直接进 memory，Agent 下次可能到处乱加强卖点，反而破坏品牌调性和合规边界。

我建议分 4 层处理。

**1. Raw Feedback：原始反馈层**

所有反馈先原样保存，不能丢。

来源包括：

```text
人工编辑反馈
审核员反馈
Reviewer Agent 反馈
发布后数据反馈
用户评论反馈
客户改稿意见
A/B 测试结果
```

这些放在：

```text
content_artifacts
artifact_feedback
feedback_events
```

原始反馈必须绑定：

```text
artifact_id
context_pack_run_id
structured_revision_refs
corpus_refs
prompt_version
agent_version
model_version
reviewer_id
feedback_type
issue_codes
rating
span_annotations
suggestion
```

这样才能回答：这条反馈到底是因为知识错、召回错、写作策略错，还是模型自己发挥错。

**2. Feedback Event：原子问题层**

一条反馈里可能有多个问题，要拆成原子事件。

比如：

```text
“开头有点假，卖点也出现太早，最后 CTA 太硬。”
```

应该拆成：

```text
issue_1:
  code: fake_hook
  target: hook
  severity: medium

issue_2:
  code: product_bridge_too_early
  target: product_bridge
  severity: high

issue_3:
  code: hard_cta
  target: closing
  severity: medium
```

这一层还不是 memory，只是可分析的反馈事件。

**3. Feedback Memory Candidate：候选经验层**

系统或 Agent 可以定期把多个 feedback_events 聚合成候选经验。

例如发现 20 篇小红书母婴文章里，有 12 篇都被批评“卖点出现太早”，就生成候选：

```json
{
  "type_code": "negative_pattern",
  "title": "母婴体验文中卖点过早出现会显得生硬",
  "summary": "小红书母婴体验文应先建立生活场景和情绪，再自然过渡到产品。",
  "payload": {
    "issue_code": "product_bridge_too_early",
    "applies_to_sections": ["hook", "problem_scene", "product_bridge"],
    "recommendation": "至少完成一个具体生活场景后再引出产品",
    "avoid": "第一段或第二段直接出现产品功能"
  },
  "evidence_count": 12,
  "confidence": 0.78,
  "scope": {
    "platform": ["xiaohongshu"],
    "industry": ["maternal_child"],
    "content_form": ["experience_note"]
  }
}
```

这个候选必须进入审核，不能直接给 Writer Agent 用。

**4. Published Feedback Memory：正式记忆层**

审核通过后，才进入结构化知识库，本质上还是 `structured_items`。

推荐类型：

```text
feedback_insight
positive_pattern
negative_pattern
reviewer_rule
agent_memory
revision_hint
```

它们不是单独一套特殊表，而是结构化知识类型的一部分。

`feedback_memory` 在 Context Pack 里应该是一个 slot，不是一个数据库表：

```text
feedback_memory slot:
  negative_patterns
  positive_patterns
  reviewer_preferences
  revision_hints
  historical_failures
```

**检索方式**

`feedback_memory` 不能纯向量检索，应该先结构化过滤：

```text
platform
brand
campaign
product
audience
content_form
section
issue_code
status = published
valid_at
confidence
evidence_count
```

然后再做语义召回和 rerank。 […]

> DEVELOPER

可以

> AGENT

好，那我把刚才这套 `feedback_memory` 设计落到唯一的开发文档里。会补成独立章节，而不是只在 Context Pack slot 里一笔带过：包括原始反馈、事件拆解、候选记忆、审核发布、召回排序、LightRAG 辅助边界和后台管理接口。

> AGENT

我会在数据库设计里把 `artifact_feedback` 扩成 raw feedback + events + candidates + memory evidence，不直接把反馈塞进 `structured_items`；然后新增一章 “Feedback Memory 设计”，说明从反馈到正式记忆的治理流程。

> AGENT

数据库部分已经把反馈从“单表记录”升级成了四层：原始反馈、反馈事件、候选记忆、正式 memory 的证据链。接下来我会补独立章节，讲清楚它如何进入 Context Pack，以及 LightRAG 在这里的边界。

> AGENT

我已经把 Feedback Memory 作为独立章节写进去了。因为新增章节会影响后续编号，我现在顺手把后面的章节编号、MVP API 和代码结构同步一下，避免文档变得前后不一致。

> AGENT

章节编号已经同步了。我再加一条实现注意事项，专门强调 raw feedback 不要直接进入 Agent；然后做最终校验写回。

> AGENT

Feedback Memory 已经落成独立设计，并同步了数据库、API、代码结构和实现注意事项。现在我做最后检查，确认没有重复章节编号和关键接口缺失，然后写回正式文档。

> AGENT

检查没问题，文档现在是 5196 行，Feedback Memory 已经形成完整章节。我把它写回正式文档，并清理临时文件。

> AGENT

已写入文档：  
[RAAP Agent 知识库服务开发文档.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/锐鲨/RAAP Agent 知识库服务开发文档.md>)

这次补了完整的 **Feedback Memory 设计**，不是简单加一个 slot。主要内容：

- 数据库新增：
  - `feedback_events`
  - `feedback_memory_candidates`
  - `feedback_memory_evidence`
  - 并扩展了 `artifact_feedback`

- 新增独立章节：
  - `26. Feedback Memory 设计`

- 明确四层流水线：
  - `artifact_feedback`：原始反馈
  - `feedback_events`：原子问题
  - `feedback_memory_candidates`：候选记忆
  - `structured_items`：审核发布后的正式 memory

- 补了：
  - candidate 生成规则
  - 正式 memory 类型
  - feedback_memory 召回排序
  - Context Pack 中的优先级
  - LightRAG 在 feedback_memory 中的边界
  - 后台管理接口
  - 评测指标
  - `Raw Feedback 不要直接进入 Agent` 的实现注意事项

现在文档是 5196 行，临时文件已清理，只保留正式开发文档。
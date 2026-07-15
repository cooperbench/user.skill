---
session_id: "lyston11/Codex_Bundles|019e0a87-115d-7f10-acee-acc0936ed947"
developer: "gh:lyston11"
split: train
source: crawl
repo: lyston11/Codex_Bundles
start_time: "2026-05-09T02:19:01.549Z"
n_turns: 24
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

矢量数据库milvus、qdrant、chroma各个的知识点
你作为面试官的角度，你会问到哪些相关的知识点？全部详细给我教学一下

> AGENT

我会先核一下三家官方文档里的当前概念和产品边界，再按“面试官会怎么问”来组织成一份可复习的知识地图。这样既讲原理，也避免把已经变动的实现细节讲旧了。

> AGENT

下面按 2026-05-09 官方文档现状整理。先给你一句面试级总览：

Milvus：大规模、分布式、云原生向量数据库，适合海量数据、高吞吐、复杂运维场景。  
Qdrant：工程体验很好，过滤、payload、混合检索、HNSW 调优很强，适合服务化向量检索。  
Chroma：RAG 开发友好，嵌入式和本地实验特别顺手，也有 Cloud/分布式形态，适合快速构建 AI 应用。

**一、通用必考知识**
无论问 Milvus、Qdrant 还是 Chroma，面试官一定会先问这些底层概念。

1. 向量数据库解决什么问题  
向量数据库不是“存数组的数据库”，核心是做近似最近邻检索，也就是 ANN。流程通常是：文本/图片/音频 -> embedding 模型 -> 向量 -> 写入向量库 -> 查询时把 query 也转成向量 -> 找 TopK 相似结果 -> metadata 过滤 -> rerank -> 给 RAG 或推荐系统使用。

2. 距离度量怎么选  
常见是 Cosine、Inner Product、L2/Euclidean。文本 embedding 常用 Cosine；推荐系统有时用 IP；真实几何距离才偏 L2。关键追问：向量是否归一化？Cosine 和 IP 在归一化后排序可能等价。

3. ANN 和精确检索的区别  
FLAT/暴力扫描召回最准，但慢。ANN 用索引牺牲一点召回换速度。面试不能只说“快”，要说清楚 tradeoff：召回率、延迟、内存、构建时间、更新成本。

4. HNSW 必会  
HNSW 是图索引。核心参数通常是：`M/max_neighbors` 控制图连接数，越大召回越好但更耗内存；`ef_construction` 控制建图质量；`ef_search` 控制查询候选数量，越大召回越高但延迟更高。

5. IVF/PQ/SQ/DiskANN  
IVF 先聚类再搜部分桶，适合大规模；PQ/SQ 用量化压缩内存，可能损失精度；DiskANN/磁盘索引用 SSD 换内存，适合超大规模。

6. 过滤怎么和向量检索结合  
metadata/filter 不是附属功能。真实业务常见条件是 tenant、时间、权限、语言、商品库存。过滤可以前置缩小候选，也可以后置过滤。面试追问重点：高选择性过滤和低选择性过滤策略不同，必须建 scalar/payload index。

7. 混合检索  
Dense vector 擅长语义，Sparse/BM25 擅长关键词精确匹配。RAG 里常用 dense + sparse + rerank。融合方式常见有 RRF、加权得分、cross-encoder rerank。

8. 写入、一致性、删除  
写入通常先落 WAL，再异步进入 segment/index。删除常是 tombstone 或延迟清理。新增数据可能有“可见性延迟”。面试官会问：刚写入的数据能不能立刻搜到？不同库答案不同。

9. 评估指标  
不能只看 QPS。要看 Recall@K、MRR、NDCG、p95/p99 latency、索引构建时间、内存占用、冷启动、过滤后召回、rerank 成本。

10. RAG 工程坑  
chunk 太大召回差，太小上下文碎；embedding 模型升级要重建索引；ID 要稳定；metadata 要设计好；向量库不是权限系统，权限过滤必须严谨。

**二、Milvus 面试知识点**
Milvus 的核心定位：大规模分布式向量数据库。官方架构是访问层 Proxy、Coordinator、Worker Nodes、Storage 四层。Worker 包括 Streaming Node、Query Node、Data Node；存储层包括 metadata、object storage、WAL 等。官方文档也强调 Milvus 建在 Faiss、HNSW、DiskANN、SCANN 等检索库之上。

你必须掌握这些点：

1. 数据模型  
Collection 类似表，Entity 类似行。Collection 有 schema、primary field、vector field、scalar fields。支持 dynamic field，也就是未声明字段可以进入隐藏 JSON 字段。Collection 下还有 partition、shard、alias。Milvus 搜索前通常要 load collection，因为索引和原始字段要加载进内存。

2. 架构  
Proxy 接请求，Coordinator 管拓扑和调度，Streaming Node 处理流式写入和 growing data，Query Node 搜 sealed/historical data，Data Node 做 compaction 和 index building，etcd/对象存储/WAL 负责元数据、持久化和恢复。

3. Growing segment 和 sealed segment  
新写入数据先进入 growing segment，之后封存为 sealed segment，再进行索引构建和 compaction。面试官喜欢用这个追问实时写入为什么会影响查询延迟和召回稳定性。

4. 索引  
Milvus 支持 FLAT、IVF_FLAT、IVF_SQ8、IVF_PQ、HNSW、DISKANN、SCANN、AUTOINDEX、GPU 索引、二进制向量索引、稀疏向量索引等。标量字段也要建索引，例如倒排、bitmap、sort、Trie 等，用于加速过滤。

5. 过滤  
Milvus 支持 filtered search。过滤表达式会被解析成执行计划，并在 segment 上形成 bitset，ANN 只在符合条件的数据范围内搜索。面试回答要说出：标量过滤速度会直接影响整体向量检索速度。

6. 一致性  
Milvus 支持 Strong、Bounded、Session、Eventually，默认常见是 Bounded Staleness。Strong 更准但延迟高；Eventually 延迟低但新写入可见性弱；Session 保证同一客户端读到自己的写入。

7. Upsert 和更新  
Upsert 用 primary key 判断插入或更新。大规模 upsert 会带来数据节点内存和 compaction 压力。业务上不要把普通 insert 当去重机制，更新、覆盖、局部更新要用对应 API 和设计。

Milvus 面试官会问：

1. Milvus 为什么适合十亿级向量？  
答：计算存储分离，分布式 worker，分片，WAL，对象存储，异步索引构建，支持多种 ANN/磁盘/GPU 索引。

2. Milvus 一次 search 请求怎么走？  
答：Client -> Proxy -> 路由到 Streaming/Query 相关节点 -> 各 segment 搜索 -> 多级 reduce -> 返回 TopK。

3. Partition 和 Shard 区别？  
答：Partition 是业务逻辑分组，用来限定搜索范围；Shard 是水平写入/数据通道切分，更多是吞吐和分布式层面的概念。

4. 为什么 collection 建好了还要 load？  
答：搜索需要索引和字段数据在内存或可服务状态，load 是把 collection/partition 变成可查询状态；不用的 collection 应 release 节省资源。

5. HNSW、IVF、DISKANN 怎么选？  
答：中等规模高召回低延迟选 HNSW；更大规模和可接受调参选 IVF；内存紧张或超大规模选 DISKANN；不想手调可考虑 AUTOINDEX，但要压测验证。

**三、Qdrant 面试知识点**
Qdrant 的核心定位：Rust 实现、API 清晰、payload/filtering 能力强、HNSW 和混合检索体验好。

必须掌握：

1. 数据模型  
Collection 是点的集合。Point 是核心记录，包含 ID、vector、payload。ID 支持 64-bit integer 或 UUID。Payload 是 JSON metadata。一个 point 可以有多个 named vectors，支持 dense vectors、sparse vectors、multivectors。

2. 距离度量  
Qdrant 支持 Dot、Cosine、Euclid、Manhattan。官方说明 Cosine 会在上传时做归一化并用 dot-product 实现。

3. 索引  
Qdrant dense vector index 主要是 HNSW。关键参数是 `m`、`ef_construct`、查询时 `hnsw_ef/ef`。它还有 payload index，用于 metadata 过滤；filterable HNSW 是 Qdrant 很重要的卖点，因为真实业务经常是“向量相似 + 条件过滤”。

4. Payload filtering  
支持 must、should、must_not 等布尔组合，也支持递归嵌套。payload index 用于快速过滤和估计 cardinality。面试回答要强调：不是所有字段都该建索引，要优先给高选择性、常用于过滤的字段建。

5. Storage  
Qdrant collection 被分成 segments，每个 segment 有自己的 vector storage、payload storage、indexes、id mapper。支持 in-memory 和 memmap/on-disk。Payload 可 in-memory 或 on-disk，大 payload 放磁盘能省内存，但过滤字段最好建索引。

6. WAL 和版本  
Point 修改先写 WAL，保证异常恢复。segment 内有版本机制，旧版本更新会被忽略。

7. 分布式  
Qdrant 分布式用 Raft 维护 cluster topology 和 collection structure。但 point 操作不走 consensus，因此默认偏可用性和吞吐。可以用 write ordering、write consistency factor、read consistency 来增强一致性。

8. 混合检索  
Qdrant Query API 支持 prefetch、多阶段查询、dense + sparse 融合，融合方式包括 RRF、DBSF。还支持 multivector，适合 ColBERT 这类 late interaction 模型。

Qdrant 面试官会问：

1. Point、Payload、Collection 分别是什么？  
答：Collection 是搜索空间，Point 是一条记录，Payload 是跟向量绑定的 JSON 元数据。

2. Qdrant 为什么过滤能力强？  
答：payload index + filterable HNSW + cardinality 估计，能把传统过滤和向量检索结合。

3. `ef_construct` 和 `ef` 区别？  
答：前者影响建图质量和构建成本；后者影响查询召回和延迟。

4. on-disk vector 什么时候用？  
答：数据太大、内存贵、可接受一定磁盘访问延迟时；如果热数据足够多，memmap 借助 page cache 接近内存表现。

5. Qdrant 分布式是不是强事务？  
答：不是传统强事务数据库。Raft 管拓扑和 collection 变更，point updates 默认不通过 consensus；并发更新同一个 point 要关注 ordering 和一致性参数。

6. Upsert 已存在 ID 会怎样？  
答：上传相同 ID 的 point 会替换原 point；如果是 named vectors，没传的向量可能被置空。只想改部分 vector 应使用 update vectors。

**四、Chroma 面试知识点**
Chroma 的核心定位：AI/RAG 开发友好的向量数据基础设施，开箱即用，适合本地、原型、应用内集成，也有 Chroma Cloud 和分布式架构。

必须掌握：

1. 数据模型  
Chroma 有 tenant、database、collection。Collection 里每条 item 通常包含 unique ID、embedding、metadata、document。Collection 是存储和查询的基本单位。

2. Client 模式  
`Client()` 是内存实验；`PersistentClient(path=...)` 本地持久化；`HttpClient` 连接独立 Chroma server；`CloudClient` 连接 Chroma Cloud。JS/TS 通常连接 server。

3. Embedding function  
Chroma 可以把 embedding function 绑定到 collection。添加 documents 时可自动 embedding；也可以直接传 embeddings。默认 embedding function 使用 `all-MiniLM-L6-v2`。如果 collection 没有 embedding function，query 时就要直接传 query embeddings。

4. Query 和 Get  
`query` 做相似度搜索，默认返回每个 query 10 条结果；`get` 是按 ID 或过滤条件取数据，不做相似度排序。`where` 做 metadata filtering，`where_document` 做全文/正则类文档过滤。`include` 控制返回 documents、metadatas、embeddings、distances 等。

5. 索引  
单节点 Chroma 使用 HNSW，参数包括 `space`、`ef_construction`、`ef_search`、`max_neighbors`、`num_threads`、`batch_size`、`sync_threshold`、`resize_factor`。Distributed/Chroma Cloud 使用 SPANN。

6. 架构  
Chroma 官方把部署分为 Local、Single-Node、Distributed。Single-Node 面向中小规模，官方描述通常是少量 collection、千万级以下记录量更合适。Distributed 架构包括 Gateway、Log、Query Executor、Compactor、System Database，并使用对象存储、SQL catalog、SSD cache。

Chroma 面试官会问：

1. 为什么 RAG demo 常用 Chroma？  
答：本地启动简单，collection、document、metadata、embedding function 集成度高，开发体验好。

2. `query` 和 `get` 区别？  
答：query 是向量相似度检索；get 是普通获取，不按向量距离排序。

3. Chroma 如何处理 embedding？  
答：可以自动调用 collection 的 embedding function，也可以用户自己传 embeddings。生产中要固定模型版本和维度。

4. Chroma 单节点和分布式区别？  
答：单节点用 HNSW，适合本地和中小规模；分布式/Cloud 用多服务架构和 SPANN，更偏生产扩展。

5. 什么场景不优先选 Chroma？  
答：自建超大规模、多租户强隔离、复杂运维、精细一致性和索引控制要求很高时，通常会更偏 Milvus 或 Qdrant。

**五、三者对比**
| 维度 | Milvus | Qdrant | Chroma |
|---|---|---|---|
| 最适合 | 大规模生产、分布式、海量向量 | 工程服务化、过滤强、混合检索 | RAG 原型、本地开发、应用快速集成 |
| 数据模型 | Collection、schema、entity、partition、shard | Collection、point、payload、named vectors | Tenant、database、collection、document/metadata |
| 索引丰富度 | 很丰富：IVF、HNSW、DiskANN、SCANN、GPU、稀疏等 | 以 HNSW 为核心，payload/filterable index 强 | 单节点 HNSW，分布式/Cloud SPANN |
| 过滤能力 | 标量过滤、bitset、scalar index | payload index 和 filterable HNSW 很突出 | where metadata、where_document |
| 分布式复杂度 | 高，组件多，适合 Kubernetes | 中等，部署和 API 更轻 | 本地简单，Cloud/分布式由平台承担 |
| 一致性 | Strong、Bounded、Session、Eventually | read/write consistency、ordering，但非传统强事务 | 更偏应用检索语义，具体看部署形态 |
| 面试选型话术 | “海量和复杂生产选 Milvus” | “过滤和工程体验选 Qdrant” | “RAG 快速开发选 Chroma” |

**六、面试设计题答题模板**
题目：有 1 亿篇文档，768 维向量，按租户、时间、语言过滤，RAG 查询 p95 要 100ms 内，你怎么设计？

高分回答应该包含：

1. 选型：Milvus 或 Qdrant 更稳；Chroma 适合原型或 Cloud 托管场景。  
2. Schema：id、tenant_id、doc_id、chunk_id、embedding_version、timestamp、language、权限字段。  
3. 索引：向量建 HNSW/IVF/DiskANN，过滤字段建 scalar/payload index。  
4. 检索：先 metadata filter，再 ANN TopK，必要时 dense + sparse hybrid，再 rerank。  
5. 一致性：写入走 upsert，记录 embedding version，索引异步构建时考虑可见性。  
6. 运维：分片、复制、备份、监控 p95/p99、Recall@K、内存、segment/compaction、冷启动。  
7. 灰度：新 embedding 模型用新 collection 或新字段，双写双读评估后切流。

**七、你要背下来的简短版**
Milvus：大规模分布式，组件多，索引多，强在海量生产和复杂架构。  
Qdrant：Point + Payload，HNSW + payload index，过滤和混合检索非常重要。  
Chroma：开发友好，collection 绑定 embedding function，本地 RAG 很快，生产要看规模和部署模式。  
共同核心：距离度量、ANN 索引、过滤、混合检索、一致性、评估指标。  
面试最高分不是背 API，而是能讲清楚“为什么这样选、怎么调、哪里会踩坑”。

资料来源：  
[Milvus Architecture](https://milvus.io/docs/architecture_overview.md), [Milvus Collections](https://milvus.io/docs/manage-collections.md), [Milvus Indexes](https://milvus.io/docs/index-vector-fields.md), [Milvus Consistency](https://milvus.io/docs/consistency.md), [Milvus Filtered Search](https://milvus.io/docs/filtered-search.md)  
[Qdrant Overview](https://qdrant.tech/documentation/overview/), [Qdrant Collections](https://qdrant.tech/documentation/concepts/collections/), [Qdrant Indexing](https://qdrant.tech/documentation/manage-data/indexing/), [Qdrant Storage](https://qdrant.tech/documentation/concepts/storage/), [Qdrant Distributed Deployment](https://qdrant.tech/documentation/guides/distributed_deployment/), [Qdrant Hybrid Queries](https://qdrant.tech/documentation/concepts/hybrid-queries/)  
[Chroma Introduction](https://docs.trychroma.com/docs/overview/introduction), [Chroma Architecture](https://docs.trychroma.com/reference/architecture/overview), [Chroma Configure Collections](https://docs.trychroma.com/docs/collections/configure), [Chroma Query/Get](https://docs.trychroma.com/docs/querying-collections/query-and-get), [Chroma Clients](https://docs.trychroma.com/docs/run-chroma/clients)

> DEVELOPER

你这里面提到的很多我都不知道，听都没听过，
你好好全部给我详细教清楚，我从头到尾一一学习直到真正理解掌握这些知识点

> AGENT

可以。我们先把它当成一门小课来学，不急着背名词。你现在的问题不是“不懂 Milvus/Qdrant/Chroma”，而是很多底层概念还没有连成一张图。我从 0 开始讲。

**第 0 层：向量数据库到底是什么**
普通数据库存的是：

```text
id = 1
title = "苹果手机怎么换电池"
category = "phone"
created_at = "2026-05-09"
```

向量数据库多存一个东西：

```text
embedding = [0.12, -0.83, 0.44, ...]
```

这个 `embedding` 是一串数字，用来表示“语义”。

比如：

```text
"苹果手机怎么换电池"
"iPhone 电池维修方法"
```

这两句话字面不完全一样，但意思很接近。搜索引擎只靠关键词可能找不准，向量搜索可以找“意思相近”的内容。

所以向量数据库的核心作用是：

> 把文本、图片、音频、商品、用户行为等转成向量，然后根据向量距离找到最相似的数据。

---

**第 1 层：Embedding 是什么**
Embedding 就是“把非数字的东西变成数字坐标”。

你可以想象一个二维地图：

```text
苹果手机       iPhone       手机维修
   *             *             *

香蕉           西瓜          水果
 *              *             *
```

语义相近的东西在空间里距离近，语义不相关的距离远。

真实 embedding 不是二维，而是几百维、几千维。

常见维度：

```text
384 维
768 维
1024 维
1536 维
3072 维
```

面试官常问：

> embedding 维度能不能变？

答案：同一个 collection/index 里通常不能混用不同维度。  
因为向量库要比较距离，768 维和 1536 维没法直接比较。

---

**第 2 层：相似度怎么计算**
向量数据库要回答：

> query 向量和库里哪个向量最像？

常见距离有三种。

**Cosine 相似度**

看方向像不像，不太关心长度。

适合文本语义检索。

```text
方向越接近，语义越相似
```

**L2 / Euclidean 距离**

几何距离，像地图上两点之间的直线距离。

```text
距离越小，越相似
```

**Inner Product / Dot Product**

点积。推荐系统里常见。

```text
分数越大，越相似
```

面试官常追问：

> Cosine 和 Inner Product 有什么关系？

如果向量都做了归一化，也就是长度都变成 1，那么 Cosine 和 Dot Product 的排序结果可能一样。

---

**第 3 层：TopK 是什么**
向量搜索通常不是问：

> 有没有完全一样的？

而是问：

> 找最相似的前 K 个。

例如：

```text
query = "怎么给 iPhone 换电池"
topK = 5
```

返回：

```text
1. iPhone 电池更换教程
2. 苹果手机维修指南
3. 手机电池鼓包怎么办
4. iPhone 官方维修价格
5. 手机续航变差原因
```

这叫 TopK 检索。

---

**第 4 层：为什么需要索引**
假设数据库里有 1 亿条向量。

如果每次查询都拿 query 向量和 1 亿个向量逐个算距离，这叫暴力搜索，也叫 FLAT。

优点：

```text
最准确
```

缺点：

```text
太慢，太贵
```

所以向量数据库会建索引。

索引的目的：

> 不搜索全部数据，只搜索最可能相似的一小部分。

这就引出 ANN。

---

**第 5 层：ANN 是什么**
ANN = Approximate Nearest Neighbor，近似最近邻。

意思是：

> 我不保证 100% 找到理论上最相似的结果，但我可以非常快地找到几乎最相似的结果。

向量数据库就是在做 tradeoff：

```text
准确率 / 召回率
查询速度
内存占用
索引构建时间
写入成本
```

面试官常问：

> ANN 为什么不是完全准确？

因为它为了快，会跳过大量候选数据，只搜索“看起来可能相似”的区域。

---

**第 6 层：Recall 召回率**
假设暴力搜索的真实 Top10 是：

```text
A B C D E F G H I J
```

你的 ANN 搜出来：

```text
A B C D E X Y Z M N
```

命中了 5 个真实结果。

```text
Recall@10 = 5 / 10 = 50%
```

面试里不能只说“QPS 很高”，还要说：

```text
Recall@K
p95 latency
p99 latency
内存占用
索引构建时间
过滤后召回
```

---

**第 7 层：HNSW 是什么**
HNSW 是最常见的向量索引之一。

可以把它理解成“语义高速公路地图”。

普通搜索是：

```text
一个一个找
```

HNSW 是：

```text
先从高层快速跳到大概区域
再逐层下降
最后在附近精细搜索
```

它像一个多层图：

```text
顶层：节点少，跳得远
中层：节点多一些
底层：节点最多，查得细
```

核心参数：

```text
M
ef_construction
ef_search
```

**M**

每个点最多连多少邻居。

```text
M 越大：图更密，召回更好，内存更高
M 越小：内存更省，可能召回下降
```

**ef_construction**

建索引时搜索多少候选。

```text
越大：索引质量更好，构建更慢
越小：构建更快，质量可能差
```

**ef_search**

查询时搜索多少候选。

```text
越大：召回更高，查询更慢
越小：查询更快，结果可能差
```

面试标准回答：

> HNSW 适合中大规模、高召回、低延迟场景，但内存占用较高，参数需要根据 Recall 和 latency 压测调优。

---

**第 8 层：IVF 是什么**
IVF 可以理解成“先分区，再搜索”。

例如有 1 亿个向量，先聚类成 10,000 个桶：

```text
bucket 1
bucket 2
bucket 3
...
bucket 10000
```

查询时先判断 query 最接近哪些桶，只搜其中一部分。

关键参数常见是：

```text
nlist：分多少个桶
nprobe：查询时搜多少个桶
```

```text
nprobe 越大：召回更高，速度更慢
nprobe 越小：速度更快，可能漏结果
```

适合：

```text
数据很大
可以接受一些调参
希望控制内存和速度
```

---

**第 9 层：PQ / SQ / Quantization 是什么**
向量一般是 float32。

比如 768 维：

```text
768 * 4 bytes = 3072 bytes
```

1 亿条就是：

```text
约 300GB 纯向量数据
```

还没算索引、metadata、系统开销。

量化就是压缩向量。

**SQ：Scalar Quantization**

把 float32 压成 int8 等。

**PQ：Product Quantization**

把向量切成多段，每段用码本近似表示。

优点：

```text
省内存
可能更快
```

缺点：

```text
精度损失
召回下降
调参复杂
```

---

**第 10 层：DiskANN 是什么**
HNSW 很吃内存。

如果数据特别大，内存放不下，就要考虑磁盘索引。

DiskANN 的思想是：

> 把大量索引/向量放在 SSD 上，用合理的数据结构减少磁盘访问。

适合：

```text
超大规模
内存预算有限
可以接受 SSD 访问带来的延迟
```

---

**第 11 层：Metadata Filtering 是什么**
真实业务不会只搜相似。

例如：

```text
找和“儿童感冒药”相似的文档
但必须满足：
tenant_id = 123
language = "zh"
created_at > 2025-01-01
权限包含 user_id
```

这些条件就是 metadata filter。

向量库里通常有两类字段：

```text
vector：用于语义相似搜索
metadata / scalar / payload：用于过滤
```

不同数据库叫法不同：

```text
Milvus：scalar field
Qdrant：payload
Chroma：metadata
```

面试重点：

> 过滤字段要建索引，否则向量搜索很快，但过滤很慢，整体还是慢。

---

**第 12 层：前过滤和后过滤**
假设你要搜索：

```text
tenant_id = A
topK = 10
```

有两种做法。

**前过滤**

先筛出 tenant A 的数据，再做向量搜索。

优点：

```text
权限安全
候选更少
```

缺点：

```text
如果过滤后数据太少，ANN 索引效果可能变化
```

**后过滤**

先全局向量搜索 TopN，再过滤 tenant A。

优点：

```text
实现简单
```

缺点：

```text
可能 TopN 过滤完不够 10 条
权限场景有风险
```

生产系统通常更偏前过滤或索引级过滤。

---

**第 13 层：Hybrid Search 混合检索**
纯向量搜索擅长语义，但有时不擅长精确关键词。

比如用户问：

```text
报错码 E11000
```

向量搜索可能觉得“数据库错误”“插入失败”都相似，但真正重要的是 `E11000` 这个关键词。

所以常用混合检索：

```text
Dense Vector Search：语义
Sparse / BM25 Search：关键词
Reranker：重新排序
```

流程：

```text
query
  -> dense search 找语义相似
  -> sparse search 找关键词匹配
  -> 合并候选
  -> rerank
  -> 返回最终结果
```

面试标准回答：

> RAG 中 dense 检索负责语义召回，sparse 检索负责精确词召回，reranker 负责最终相关性排序。

---

**第 14 层：Rerank 是什么**
第一阶段向量库可能返回 50 或 100 条候选。

Reranker 再精排。

例如：

```text
向量库 Top100
-> reranker 逐条判断 query 和文档是否真正相关
-> 返回 Top5
```

常见 reranker 是 cross-encoder 或专门的 rerank 模型。

优点：

```text
答案质量明显提升
```

缺点：

```text
更慢
更贵
```

---

**第 15 层：Collection 是什么**
Collection 可以理解成“向量表”。

比如你有一个知识库：

```text
collection = company_docs
```

里面每条数据：

```text
id
embedding
document
metadata
```

不同系统叫法：

```text
Milvus：Collection + Entity
Qdrant：Collection + Point
Chroma：Collection + Item/Document
```

---

**第 16 层：Schema 是什么**
Schema 是表结构。

例如：

```text
id: string
embedding: float_vector[768]
tenant_id: string
doc_id: string
chunk_id: string
language: string
created_at: timestamp
text: string
```

Milvus 特别强调 schema。  
Qdrant 更灵活，payload 类似 JSON。  
Chroma 更适合文档 + metadata 的轻量结构。

---

**第 17 层：Chunk 是什么**
RAG 不会直接把一整本书变成一个向量。

通常会切块：

```text
文档 -> chunk1
文档 -> chunk2
文档 -> chunk3
```

每个 chunk 单独 embedding。

chunk 太大：

```text
语义混杂，检索不准
```

chunk 太小：

```text
上下文不足，答案断裂
```

常见策略：

```text
按标题切
按段落切
固定 token 长度切
带 overlap 切
```

例如：

```text
chunk_size = 500 tokens
overlap = 50 tokens
```

---

**第 18 层：ID 设计**
ID 很重要。

不要随便用随机 ID 后就忘了。

建议：

```text
doc_id
chunk_id
embedding_version
tenant_id
source
```

例如：

```text
id = tenantA:doc123:chunk007:v2
```

这样方便：

```text
删除整篇文档
重建某个版本 embedding
排查召回问题
去重
```

---

**第 19 层：Upsert 是什么**
Upsert = update or insert。

意思是：

```text
如果 ID 不存在，就插入
如果 ID 存在，就更新
```

注意：

> upsert 不是免费的。大量 upsert 会造成旧数据失效、新数据写入、后台 compact/index rebuild 压力。

---

**第 20 层：Delete 为什么复杂**
向量库删除通常不是立刻物理删除。

它可能先标记：

```text
deleted = true
```

然后后台 compaction 时真正清理。

这叫 tombstone 或逻辑删除。

原因：

```text
索引结构不适合频繁原地删除
后台批量整理更高效
```

---

**第 21 层：WAL 是什么**
WAL = Write-Ahead Log，预写日志。

写数据时先写日志，再更新内部数据结构。

作用：

```text
机器崩了可以恢复
避免写一半数据丢失
```

很多数据库都有 WAL，不只是向量数据库。

---

**第 22 层：Segment 是什么**
Segment 可以理解成数据库内部的数据块。

向量库不会把所有数据塞进一个巨大文件，而是分成很多 segment。

好处：

```text
方便并行搜索
方便压缩
方便合并
方便删除清理
方便索引构建
```

Milvus、Qdrant 都有 segment 思想。

---

**第 23 层：Compaction 是什么**
Compaction 是后台整理。

它会做：

```text
合并小 segment
清理删除数据
压缩存储
优化查询性能
```

面试官问：

> 为什么写入和删除很多后查询变慢？

可以回答：

> 因为 segment 变多、tombstone 变多、索引和数据碎片增加，需要 compaction 恢复查询效率。

---

**第 24 层：Shard 和 Replica**
Shard 是分片。

```text
1 亿数据
分成 10 片
每片 1000 万
```

作用：

```text
水平扩展容量和写入吞吐
```

Replica 是副本。

```text
shard 1 有 3 个副本
```

作用：

```text
高可用
读扩展
容灾
```

简单说：

```text
Shard 解决太大
Replica 解决可靠和并发
```

---

**第 25 层：一致性**
一致性问的是：

> 我刚写入的数据，马上能不能搜到？

常见级别：

```text
Strong：强一致，最新但可能慢
Bounded：允许一点延迟
Session：同一个会话读到自己的写入
Eventually：最终一致，最快但可能短暂读不到
```

面试回答不要绝对化，要说：

> 选择一致性取决于业务。搜索推荐可以接受 eventually，权限、金融、后台审核可能需要更强一致。

---

**第 26 层：Milvus 怎么理解**
Milvus 适合大规模生产。

你可以把它理解成：

```text
复杂、分布式、强大、组件多
```

核心对象：

```text
Collection：表
Entity：行
Vector field：向量字段
Scalar field：普通字段
Partition：业务分区
Shard：数据分片
Segment：内部数据块
```

Milvus 架构里有：

```text
Proxy：接收请求
Coordinator：协调集群
Query Node：负责查询
Data Node：负责数据处理
Streaming Node：处理流式写入
Storage：对象存储、元数据、WAL
```

Milvus 面试你要会说：

> Milvus 适合大规模向量检索，支持多种索引、分布式扩展、分区分片、标量过滤和多种一致性级别。代价是架构和运维复杂度更高。

---

**第 27 层：Milvus 常见考点**
**为什么要 load collection？**

因为向量检索需要索引、字段数据处于可服务状态。Milvus 里 collection 创建和写入后，不代表一定已经加载到查询节点。

**Partition 和 Shard 区别？**

```text
Partition：业务逻辑分组，比如按月份、租户、类别
Shard：底层水平拆分，用于吞吐和扩展
```

**Growing Segment 和 Sealed Segment？**

```text
Growing：新写入、还在增长的数据
Sealed：封存后可建索引的数据块
```

新数据进来后，不一定立刻以最佳索引状态参与查询。

---

**第 28 层：Qdrant 怎么理解**
Qdrant 的关键词是：

```text
Point
Payload
HNSW
Filter
Rust
工程友好
```

核心对象：

```text
Collection：集合
Point：一条数据
Vector：向量
Payload：JSON 元数据
Named vectors：一条 point 可以有多个向量
```

例如一个商品：

```json
{
  "id": "sku_123",
  "vector": [0.1, 0.2, 0.3],
  "payload": {
    "category": "phone",
    "brand": "Apple",
    "price": 6999
  }
}
```

Qdrant 面试你要会说：

> Qdrant 的 payload filtering 很强，适合“向量相似 + metadata 条件过滤”的服务化场景。它以 HNSW 为核心，并支持 named vectors、sparse vectors、hybrid search、on-disk 存储和分布式部署。

---

**第 29 层：Qdrant 常见考点**
**Point 是什么？**

就是一条向量记录，包含：

```text
id
vector
payload
```

**Payload 是什么？**

JSON 元数据，用于过滤、排序、业务字段存储。

**Payload index 为什么重要？**

没有索引时，过滤可能要扫描大量 payload。  
有索引后，可以快速判断哪些 point 满足条件。

**Named vectors 是什么？**

一条数据有多个向量。

例如商品可以有：

```text
title_vector
image_vector
description_vector
```

查询时可以指定用哪个向量字段。

---

**第 30 层：Chroma 怎么理解**
Chroma 的关键词是：

```text
简单
RAG 友好
本地开发
embedding function
collection
```

适合快速做：

```text
文档问答
本地知识库
RAG 原型
小中规模 AI 应用
```

核心对象：

```text
Client
Collection
Document
Metadata
Embedding
ID
```

Chroma 可以这样用：

```python
collection.add(
    ids=["1"],
    documents=["iPhone 电池维修教程"],
    metadatas=[{"source": "manual"}]
)
```

如果 collection 配了 embedding function，它可以自动把 document 转成 embedding。

---

**第 31 层：Chroma 常见考点**
**query 和 get 区别？**

```text
query：向量相似度搜索
get：按 ID 或条件取数据，不做语义排序
```

**PersistentClient 是什么？**

本地持久化客户端，数据会写到磁盘。

**HttpClient 是什么？**

连接远程 Chroma server。

**Chroma 适合什么？**

```text
本地 RAG
快速原型
AI 应用内嵌知识库
```

**不适合什么？**

```text
非常复杂的大规模自建分布式场景
对索引、分片、一致性、运维有强控制要求的场景
```

---

**第 32 层：三者怎么选**
面试选型可以这样说：

```text
如果是十亿级向量、复杂分布式、K8s 部署、海量数据，我优先看 Milvus。

如果是工程服务化、过滤条件复杂、payload 很重要、希望 API 清晰，我优先看 Qdrant。

如果是 RAG 原型、本地知识库、快速验证应用，我优先看 Chroma。
```

这句话很重要，建议背下来。

---

**第 33 层：完整 RAG 流程**
一个标准 RAG 系统是这样：

```text
原始文档
-> 清洗
-> 切 chunk
-> embedding
-> 写入向量数据库
-> 用户提问
-> query embedding
-> 向量检索 TopK
-> metadata filter
-> rerank
-> 拼 prompt
-> LLM 生成答案
-> 返回引用来源
```

面试官会问：

> 向量数据库在 RAG 里负责什么？

回答：

> 负责根据用户问题召回最相关的上下文，不负责生成答案。生成答案是 LLM 的工作。

---

**第 34 层：生产级设计题怎么答**
题目：

> 设计一个企业知识库问答系统，支持多租户、权限过滤、千万级文档。

回答框架：

```text
1. 文档入库：解析 PDF/Word/网页，清洗文本
2. 切分：按标题和段落 chunk，保留 doc_id、chunk_id
3. 向量化：固定 embedding 模型和版本
4. 存储：向量 + 原文 + metadata
5. 过滤字段：tenant_id、user_role、source、created_at
6. 索引：向量索引 + metadata 索引
7. 查询：权限过滤 + dense search + sparse search
8. 精排：reranker
9. 生成：把 TopK chunk 放进 prompt
10. 评估：Recall@K、答案准确率、p95 延迟
11. 运维：备份、重建索引、模型升级、监控
```

---

**第 35 层：面试官最喜欢追问的坑**
**坑 1：只看向量相似度，不做权限过滤**

这是严重问题。企业知识库必须先保证权限。

**坑 2：embedding 模型换了，但旧向量没重建**

不同模型的向量空间不同，不能混着搜。

**坑 3：chunk 设计太随意**

chunk 太大或太小都会影响召回。

**坑 4：只返回 TopK，不做 rerank**

复杂问题下，第一阶段检索结果可能噪声很大。

**坑 5：metadata 不建索引**

过滤慢会拖垮整体查询。

**坑 6：只测 QPS，不测 Recall**

快但搜不准没有意义。

---

**第 36 层：你现在应该怎么学**
不要一口气背 API。按这个顺序学：

```text
1. 先理解 embedding、距离、TopK
2. 再理解 ANN、HNSW、IVF
3. 再理解 metadata filter、hybrid search、rerank
4. 再理解 collection、schema、segment、WAL、compaction
5. 最后分别学 Milvus、Qdrant、Chroma 的产品差异
```

你真正掌握的标准是：

```text
能解释为什么需要向量数据库
能说清楚 HNSW 的 M、ef_search、ef_construction
能设计一个 RAG 检索流程
能解释 metadata filter 为什么关键
能比较 Milvus、Qdrant、Chroma 的适用场景
能回答生产系统里的延迟、召回、一致性和扩展问题
```

最小记忆版：

```text
向量数据库 = 用 embedding 做语义相似搜索的数据库。
ANN = 用近似方法换速度。
HNSW = 图索引，召回高，内存大。
IVF = 聚类分桶，适合大规模。
Metadata filter = 业务条件过滤，生产必备。
Hybrid search = 语义 + 关键词。
Rerank = 对候选结果重新精排。
Milvus = 大规模分布式。
Qdrant = payload/filter 工程体验强。
Chroma = RAG 原型和本地开发友好。
```

下一步最有效的学法是：我用“面试官提问 -> 你先答 -> 我纠正补全”的方式带你练。第一组题可以从最基础开始：**“什么是 embedding？为什么文本能变成向量？”**

> DEVELOPER

[$codex-md-docs](/Users/lyston/.codex/skills/codex-md-docs/SKILL.md) 把你的这些全都写下来记录下来一个都不能少

> SYSTEM

<skill>
<name>codex-md-docs</name>
<path>/Users/lyston/.codex/skills/codex-md-docs/SKILL.md</path>
---
name: codex-md-docs
description: Route Markdown documentation work into the user's Codex Obsidian space, including choosing or creating device/category folders, deciding whether to create/append/update notes, and keeping operational records separated by device/environment. Use when the user asks Codex to create, write, update, append, record, summarize, save, organize, archive, or maintain any Markdown document, md note, deployment record, operation guide, SOP, troubleshooting note, decision record, or session handoff unless the user explicitly gives a different destination.
---

# Codex Markdown Docs

## Default Root

Use this Markdown documentation root by default:

```text
/Users/lyston/Obsidian/lyston/Codex
```

Prefer this root even if older notes exist elsewhere, unless the user explicitly names another path. Create it if it is missing. Do not write documentation into project source trees, `/tmp`, `/root`, downloads, or ad hoc scratch folders unless the user explicitly asks.

## Placement Model

Use the existing vault structure as the source of truth. The active Codex vault structure is device-first:

```text
Codex/
  lystonmacbook-pro.local/
  lyston11.qzz.io/
```

Top-level folders under `/Users/lyston/Obsidian/lyston/Codex` must be device, host, or environment names. Under each device directory, classify documents by service, project, or content type, such as:

```text
Hermes
Fast Note Sync
Sub2API
基础设施
DBX
GenericAgent
HAPI
MindOS
Codex工具与文档系统
LDStatus Pro
锐鲨
```

Do not put service or project folders directly under the Codex root. Do not create or maintain `README.md`, separate catalog folders, summary entry pages, or original archive folders. Use device directories, category directories, clear filenames, headings, and search for discoverability.

When a split is complete, day-to-day entry points are the device folders, category folders, and focused Markdown files only.

## Before Writing

1. If the user gives an exact file path, use that path.
2. If the user gives a folder path, choose or create the `.md` file inside that folder.
3. If the user gives only a title or topic, inspect likely matching device folders and Markdown files under `/Users/lyston/Obsidian/lyston/Codex`.
4. Search device directories, category directories, filenames, and headings for the topic, service name, date, project, domain, path, hostname, device name, or keywords from the request.
5. Identify the device/environment before choosing the directory, appending, or updating. Compare hostname/device name, OS, cloud provider, public domain/IP, deployment root, path style, container runtime, and tunnel/reverse-proxy endpoint when available.
6. Use clear filenames and headings because there are no folder entry pages.
7. Hard rule: never merge records across different devices or environments only because the service name matches.
8. Prefer an existing note only when both the device/environment and topic/service match.
9. Preserve existing Markdown structure, frontmatter, headings, Obsidian links, and unrelated content.
10. Do not create database backups, code backups, or duplicate archival files unless the user explicitly asks.

## Create, Append, Or Update

Choose the smallest durable change that fits the request:

- **Create** a new file when no strong match exists, the topic is new, the environment differs, or the user asks for a standalone document.
- **Append** for deployment logs, operational history, incident notes, progress records, meeting notes, dated observations, command outputs, session handoffs, and continuing timelines.
- **Update** an existing section for living guides, SOPs, runbooks, architecture notes, checklists, policies, configuration records, or summaries whose current content should be refined.

For dated append entries, prefer:

```markdown
## 2026-05-06
```

If updating risks overwriting important history, append a dated section instead. If environment cues are missing and multiple notes could match, ask one concise clarifying question.

## Discoverability

When creating, moving, splitting, or materially updating a document, keep it discoverable:

- Do not add or update folder `README.md` files.
- Do not create or update separate catalog folders or summary entry pages.
- Use clear device directories, category directories, filenames, headings, and related-document links inside the actual notes.
- For sensitive content, record the sensitive boundary inside the relevant document itself without copying secrets or credentials elsewhere.
- Prefer Obsidian wiki links for vault-internal references. Use relative Markdown links only when they are clearer than wiki links for a specific path.

## Organization And Cleanup

If the user asks to organize, archive, split, clean up, or says the vault/folder is confusing:

1. Inventory Markdown files, directories, headings, and large mixed documents.
2. Classify by device/environment first, then by service/topic, sensitivity, and document type.
3. Split unrelated sections from large mixed documents into focused topic documents when useful.
4. Do not keep original mixed documents in original archive folders; remove old original archives after confirming the focused documents exist.
5. Create missing service/topic folders inside the appropriate device directory only when the content is likely to recur or when several documents belong together.
6. Do not create summary entry pages; keep discoverability in the folder structure, filenames, headings, and related-document links.
7. Verify final tree shape, no `README.md` files, no separate catalog folders, no original archive folders, and no stale links.

Do not keep appending unrelated operational details to a large deployment note just because it mentions the same machine. A server overview can link to service, network, and incident documents; it should not absorb them all.

## Naming

Use Chinese filenames and headings when the user writes in Chinese or the document is mainly Chinese. Use clear, short Markdown filenames.

For operational, deployment, access, tunnel, proxy, or troubleshooting records, include an environment marker in the filename when it prevents cross-device confusion:

```text
Sub2API Docker（OrbStack）部署记录.md
Sub2API Docker（Ubuntu srv-projects）部署记录.md
Cloudflare Tunnel 外网访问配置记录.md
Codex 会话同步与迁移指南.md
```

If the document belongs clearly to a service/topic folder, the environment marker can be in the document metadata instead of the filename.

## Environment Metadata

For operational documents, include ownership/context near the top when relevant:

- Hostname or device name.
- OS/cloud/provider when known.
- Main domain/IP, if public.
- Deployment root path.
- Container/runtime context, if relevant.
- Whether the record is local desktop, server-side, container-only, or tunnel/reverse-proxy related.

## Content Style

Write concise Markdown that is useful when reopened later:

- Include concrete paths, commands, service names, ports, config files, dates, and verification results when relevant.
- Keep facts separate from assumptions.
- Use fenced code blocks for commands, config, logs, and structured output.
- Redact secrets, API keys, passwords, SSH private keys, bearer tokens, and full cookies.
- For operational records, include what changed, where it lives, how to verify it, and rollback or next steps when relevant.

## Reporting Back

After writing, briefly report:

- The exact file path.
- Whether content was created, appended, moved, split, or updated.
- Which device and category folder was selected, created, or updated.
- The device/environment used to choose or separate the document when relevant.
- Any important status or caveat discovered while writing.

</skill>

> AGENT

我会用 `codex-md-docs` 技能来落到你的 Obsidian/Codex 知识库里。先确认当前设备目录和有没有已有“向量数据库/面试”相关笔记，然后我会创建或更新最合适的 Markdown 文件。

> AGENT

当前主机是 `lystonmacbook-pro.local`，我没有找到已有的向量数据库/Milvus/Qdrant/Chroma 面试笔记。接下来我会在这个设备目录下新建一个学习笔记分类，把前面两轮内容合并成一份完整 Markdown。

> AGENT

我会把内容做成“从零教学 + 面试官问题清单 + 三库对比”的长文档，而不是只贴聊天记录。这样以后打开时可以直接复习，也能按章节逐个补课。

> AGENT

笔记已经写入了，现在我会快速检查文件行数和标题结构，确保内容完整落盘、路径也符合你的 Codex Obsidian 设备优先结构。

> AGENT

已完整记录，一个都没少，写成了 1904 行的 Markdown 学习笔记。

文件位置：[/Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/学习笔记/向量数据库 Milvus Qdrant Chroma 面试学习笔记.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/学习笔记/向量数据库 Milvus Qdrant Chroma 面试学习笔记.md>)

这次是新建文件，放在设备目录 `lystonmacbook-pro.local` 下的 `学习笔记` 分类里。内容包含从零教学、通用核心概念、Milvus/Qdrant/Chroma 各自知识点、面试官问题、三者对比、设计题模板、背诵短版和官方资料来源。

> DEVELOPER

但是这样单说某一个概念不联系起来我也看不懂，不知道这个知识点是属于哪一块的，使用来干什么的，和其他的怎么联系起来

> AGENT

你说得对，前一版更像“概念词典”，但学习时最需要的是一张总图：每个词在系统链路里的位置、为了解决什么问题、前后依赖什么。我会直接把现有笔记补上一套“关系图 + 按流程串联理解”的章节，放在最前面，后面那些概念就有坐标了。

> AGENT

我已经看到合适的插入点了：会在“一句话总览”后面加一大段“先看全局链路”，用用户提问到最终答案的全过程，把 embedding、索引、过滤、TopK、rerank、WAL、segment、shard、Milvus/Qdrant/Chroma 都串起来。

> AGENT

已把“总图”和“从一次查询串起所有概念”的内容补进去了。接下来我再检查一下新增章节是否在前面、标题结构是否完整，避免它又变成难找的一段。

> AGENT

你说得非常对，这版我已经补上了“关系链路版”。

我更新了同一个文件：[/Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/学习笔记/向量数据库 Milvus Qdrant Chroma 面试学习笔记.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/学习笔记/向量数据库 Milvus Qdrant Chroma 面试学习笔记.md>)

这次是追加/更新，不是另建文件。现在笔记从 1904 行扩展到 2940 行，新增内容放在前面，专门解决你说的这个问题：

- `先看全局：所有概念在一条链路里的位置`
- `从一次查询理解所有知识点`
- `一张关系总图`
- `概念之间的依赖关系`
- `按系统层次重新理解这些词`
- `用一个例子串起三种数据库`
- `面试回答的通用组织方法`

现在它不是单个概念散讲，而是围绕“一个企业知识库 RAG 查询怎么从文档到答案”来串起来：chunk 为什么在 embedding 前面，metadata 为什么影响 filter，filter 为什么影响索引，TopK 为什么接 rerank，WAL/segment/compaction 为什么属于写入可靠性层，Milvus/Qdrant/Chroma 又分别在这条链路里承担什么角色。

> DEVELOPER

你不仅要新增还要和原来的融合呀

> AGENT

对，这个反馈很关键。现在文档前面虽然有“总图”，但后面原来的概念讲解仍然像词典，我会把它们改成每个概念都带固定结构：`属于哪一层 -> 解决什么问题 -> 上游依赖 -> 下游影响 -> 面试怎么问`，并把重复的新增内容折进原章节里。

> AGENT

我同意，单独在前面塞一段“总图”还是没完全解决问题。接下来我会把这份笔记重写成“按真实链路学习”的融合版：原来的每个概念都会回到它所属的阶段里，而不是后面再重复列一遍。

> AGENT

我会把文件整体整理一遍，保留前面所有知识点，但改成“主线章节 + 概念卡片嵌在对应位置”的结构。这样打开时不会先看一堆新增、再看一堆原文，而是顺着一条系统链路学下去。

> AGENT

我已经把文档整体重构成融合版了：不再是“新增在前、原文在后”的两段式，而是按 RAG/向量检索真实链路重新组织。现在我会检查标题、行数和关键概念是否都还在。

> AGENT

结构检查通过：核心概念都还在，而且标题已经按链路融合。最后我再做一个小的术语一致性修正，把个别 `DISKANN` 大写写法统一成 `DiskANN`，避免以后搜索和阅读不舒服。

> AGENT

你说得对，我这次不是继续“新增”，而是把整篇文档重构融合了。

已更新同一个文件：[/Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/学习笔记/向量数据库 Milvus Qdrant Chroma 面试学习笔记.md](</Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/学习笔记/向量数据库 Milvus Qdrant Chroma 面试学习笔记.md>)

现在它不再是“前面总图 + 后面概念词典”的拼接版，而是按真实链路组织：

`业务问题 -> chunk -> embedding -> 数据建模 -> 写入可靠性 -> 索引 -> 过滤 -> 召回 -> 混合检索 -> rerank -> 分布式 -> Milvus/Qdrant/Chroma 选型 -> 设计题`

每个概念也都融合进对应阶段里，按“属于哪一层、解决什么问题、依赖什么、影响什么、面试怎么问”来讲。行数现在是 2782 行，核心内容都保留了，只是把重复和割裂的结构重新梳顺了。

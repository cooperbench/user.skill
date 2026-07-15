---
session_id: 019dc5ea-a84c-7bd1-be60-dce258ef0bba
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-04-25T18:33:03.333Z"
n_turns: 8
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

你在 /user_4813494d/openbmb 仓库中工作。请只读审阅 EAGLE 推理主流程，不考虑训练，不改文件。仓库关键约束：先区分 demo-sala 正式提交路径；server 停机只能用 bench/kill_sglang.sh；工作树很脏，不能回滚用户改动。重点看 demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py、eagle_info.py、demo-sala/sglang/python/sglang/srt/models/minicpm.py、llama_eagle3.py，以及 draft model 配置。请输出：1) 关键代码路径和行号；2) 低并发提升吞吐或 accepted length 的具体建议；3) 高并发提升吞吐或 accepted length 的具体建议；4) 风险和需要验证的指标。建议必须能落地，避免泛泛而谈。

> AGENT

我会先只读确认工作树和相关文件位置，然后沿正式提交路径把 EAGLE 推理调用链、draft 配置和启动参数串起来。不会修改文件，也不会动服务进程。

> AGENT

工作树确实很脏，我会按只读方式避开任何清理或回滚。接下来查调用入口、启动参数和 draft model 元数据，重点定位正式提交包里的行为，而不是 eagle/ 训练侧。

> AGENT

检索结果显示正式提交路径的默认参数在 `demo-sala/prepare_env.sh`，本地 eval 的 `eval/start_eagle.sh` 指向另一个 v3 draft，不应混为一谈。现在我会读具体实现段落：draft 生成、tree verify、target hidden state 提供、draft model forward/config。

> AGENT

主流程里有几个可落地的热点已经露出来：每轮 decode 有 `draft -> target verify -> draft_extend_after_decode` 三段，且 topk>1 会走更复杂的 paged-cache duplicate/free/compact 路径。下面继续看 verify 内核前后的 Python/CPU 同步和 batch 过滤逻辑，这会影响高并发吞吐。

> DEVELOPER

补充纠偏：请以当前脚本为准，不要采用 AGENTS.md 旧描述里的 2/1。正式 demo-sala/prepare_env.sh 当前默认 steps=2 topk=2 dtn=5；用户也关心 steps=2 topk=3 dtn=7。eval/start_eagle.sh 默认 3/3 视作实验入口。请重点比较 2/2 与 2/3 的 accepted length、树/verify 代价和高并发吞吐 tradeoff。

> AGENT

收到，按当前脚本修正：正式 `demo-sala/prepare_env.sh` 是 `steps=2 topk=2 dtn=5`，`2/3 dtn=7` 是你关心的候选；`eval/start_eagle.sh` 的 `3/3` 我只当实验入口参考。接下来重点会放在 `2/2` 与 `2/3` 的树宽、verify token 数、cache 管理和高并发调度代价差异。

> AGENT

补充检索里也确认了 `demo-sala/README.md` 有旧的 `3/1` 描述，当前不能采用；正式值以 `prepare_env.sh` 行 472-486 为准。`2/3` 相比 `2/2` 不是只多两个 verify token，还会让 topk>1 的 cache duplicate/compact 分支按更宽树运行，我会把这个拆成低并发和高并发两类建议。
